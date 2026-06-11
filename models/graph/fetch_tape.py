#!/usr/bin/env python3
"""
fetch_tape.py - per-CUSIP trade-tape ingest for the two cuts that need the underlying tapes:
  (A) FINRA TRACE  -> individual CORPORATE bond trades, aggregated to industry-sector spreads
  (B) MSRB EMMA    -> individual MUNICIPAL bond trades, per issuer/city

HONEST ACCESS NOTE (probed 2026-06): neither tape is keyless.
  - EMMA (emma.msrb.org) returns HTTP 403 to automated clients (WAF/bot protection). It works from
    a browser / unblocked IP, or via the MSRB subscription feed. This script will succeed only from
    an unblocked environment.
  - FINRA TRACE via api.finra.org is reachable but requires a (free) FINRA API account: OAuth2
    client-credentials. Set FINRA_API_CLIENT and FINRA_API_SECRET in the environment.

When access exists, this writes data/tape_*.json; build_charts.py will pick them up. Without access
it prints what is required and exits 0 (non-destructive) - the free ETF proxies (Yahoo) stand in.
"""
import os, json, base64, subprocess, shutil, urllib.request, urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

def _curl(url, headers=None, data=None):
    if not shutil.which("curl"): return None,None
    cmd=["curl","-s","--max-time","45","-A","Mozilla/5.0","-w","\n%{http_code}"]
    for k,v in (headers or {}).items(): cmd+=["-H",f"{k}: {v}"]
    if data is not None: cmd+=["--data",data]
    cmd.append(url)
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=70)
        body,_,code=r.stdout.rpartition("\n"); return code.strip(), body
    except Exception: return None,None

# ---- (A) FINRA TRACE corporate aggregates (OAuth2 client-credentials) ----
# The free "basic" FINRA API credential exposes TRACE *aggregates* (group=fixedIncomeMarket):
#   corporateMarketBreadth / corporateMarketSentiment  - corporate (IG / HY / convertibles)
#   agencyMarketBreadth   / agencyMarketSentiment      - agency debt
#   corporate144AMarketBreadth / ...Sentiment          - Rule 144A corporate
# Breadth is broken down by QUALITY TIER (productCategory: investment grade / high yield /
# convertibles / all). Sentiment is broken down by TRADE TYPE (customer/affiliate/inter-dealer).
# This is real TRACE data by quality tier - NOT per-CUSIP, and NOT GICS industry (industry needs
# the per-CUSIP TRACE file-download entitlement at download.finratraqs.org). Documented honestly.
TRACE_TOKEN_URL="https://ews.fip.finra.org/fip/rest/ews/oauth2/access_token?grant_type=client_credentials"
def _trace_token():
    cid=os.environ.get("FINRA_API_CLIENT"); sec=os.environ.get("FINRA_API_SECRET")
    if not (cid and sec): return None
    tok_auth="Basic "+base64.b64encode(f"{cid}:{sec}".encode()).decode()
    code,body=_curl(TRACE_TOKEN_URL,headers={"Authorization":tok_auth},data="")
    if code!="200" or not body: return None
    try: return json.loads(body).get("access_token")
    except Exception: return None

def _trace_pull(token,name,limit=20000):
    code,body=_curl(f"https://api.finra.org/data/group/fixedIncomeMarket/name/{name}?limit={limit}",
                    headers={"Authorization":f"Bearer {token}","Accept":"application/json"})
    if code in ("200","204") and body:
        try: return json.loads(body)
        except Exception: return []
    return []

def _monthly_breadth(rows):
    # rows: {tradeReportDate, productCategory, advances, declines, unchanged, totalVolume, totalTrades}
    out={}
    for r in rows:
        cat=r.get("productCategory","?"); ym=(r.get("tradeReportDate") or "")[:7]
        if not ym: continue
        b=out.setdefault(cat,{}).setdefault(ym,{"adv":0,"dec":0,"unch":0,"vol":0.0,"trades":0,"days":0})
        b["adv"]+=r.get("advances",0) or 0; b["dec"]+=r.get("declines",0) or 0
        b["unch"]+=r.get("unchanged",0) or 0; b["vol"]+=r.get("totalVolume",0) or 0
        b["trades"]+=r.get("totalTrades",0) or 0; b["days"]+=1
    for cat in out:
        for ym,b in out[cat].items():
            b["vol"]=round(b["vol"],1)
            b["ad_ratio"]=round(b["adv"]/b["dec"],3) if b["dec"] else None
    return out

def fetch_trace():
    token=_trace_token()
    if not token:
        print("[TRACE] Needs a free FINRA API account. Set FINRA_API_CLIENT / FINRA_API_SECRET, then re-run.")
        print("        Register: https://developer.finra.org -> Query API -> Fixed Income (TRACE).")
        return False
    out={"meta":{"source":"FINRA TRACE aggregates (api.finra.org, group=fixedIncomeMarket, OAuth2)",
                 "note":"Real TRACE corporate aggregates by QUALITY TIER (IG/HY/convertibles) and TRADE TYPE; "
                        "not per-CUSIP and not GICS industry (those need the per-CUSIP file entitlement).",
                 "datasets":{}}}
    for label,name in [("corporate_breadth","corporateMarketBreadth"),
                       ("corporate_sentiment","corporateMarketSentiment"),
                       ("corporate144A_breadth","corporate144AMarketBreadth"),
                       ("agency_breadth","agencyMarketBreadth")]:
        rows=_trace_pull(token,name)
        out["meta"]["datasets"][label]={"name":name,"rows":len(rows)}
        if label.endswith("breadth"):
            out[label]=_monthly_breadth(rows)
        else:
            # sentiment: monthly volume/transactions by tradeType (quality) and productCategory (trade side)
            agg={}
            for r in rows:
                ym=(r.get("tradeReportDate") or "")[:7]
                if not ym: continue
                key=r.get("tradeType","?")
                if r.get("productCategory")!="all securities":  # keep the quality cut, side='all'
                    continue
                m=agg.setdefault(key,{}).setdefault(ym,{"vol":0.0,"tx":0,"trades":0})
                m["vol"]+=r.get("totalVolume",0) or 0; m["tx"]+=r.get("totalTransactions",0) or 0
                m["trades"]+=r.get("totalTrades",0) or 0
            for k in agg:
                for ym,m in agg[k].items(): m["vol"]=round(m["vol"],1)
            out[label]=agg
    dates=[]
    for lab in ("corporate_breadth",):
        for cat,series in out.get(lab,{}).items(): dates+=list(series.keys())
    out["meta"]["months"]=sorted(set(dates))
    json.dump(out,open(os.path.join(DATA,"tape_trace.json"),"w"),indent=1)
    nb=out["meta"]["datasets"].get("corporate_breadth",{}).get("rows",0)
    print(f"[TRACE] wrote data/tape_trace.json - corporate breadth rows={nb}, "
          f"months {out['meta']['months'][0] if out['meta']['months'] else '-'}..{out['meta']['months'][-1] if out['meta']['months'] else '-'} "
          f"(quality tiers: {sorted(out.get('corporate_breadth',{}).keys())})")
    return True

# ---- (B) MSRB EMMA per-CUSIP municipal trades ----
def fetch_emma(cusips=None):
    # Example: a city's GO CUSIPs would be passed in; EMMA's security/trade endpoints are 403 to bots here.
    code,_=_curl("https://emma.msrb.org/")
    if code=="403" or code is None:
        print("[EMMA] HTTP 403 / blocked from this environment (WAF). Run from an unblocked IP/browser session,")
        print("       or use the MSRB real-time feed. Per-CUSIP trade JSON: emma.msrb.org/Security/Details/<CUSIP>.")
        return False
    print("[EMMA] reachable - implement per-CUSIP pull for the supplied issuer CUSIPs.")
    return False

def main():
    print("== per-CUSIP tape ingest (TRACE corporates by sector / EMMA munis by issuer) ==")
    a=fetch_trace(); b=fetch_emma()
    if not (a or b):
        print("\nNo tape ingested (access-gated). Free ETF proxies (Yahoo: CMF/NYF/MUB/HYD, rating ladder, EM) stand in.")

if __name__=="__main__": main()
