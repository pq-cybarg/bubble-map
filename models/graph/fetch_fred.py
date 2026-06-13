#!/usr/bin/env python3
"""
fetch_fred.py - pull MONTHLY series from FRED's keyless CSV endpoint and cache to
data/fred_monthly.json (with provenance). No API key required. Reproducible: re-run to
refresh; build_charts.py reads the cache so the site renders even offline.

Series: DGS2 (2Y Treasury), FEDFUNDS (effective fed funds), DGS3MO (3M), DGS10 (10Y),
DFEDTARU (target upper). Daily series are aggregated to monthly average by FRED (fq/fam).
"""
import os, json, time, urllib.request, subprocess, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); os.makedirs(DATA,exist_ok=True)
OUT=os.path.join(DATA,"fred_monthly.json")
OUT_D=os.path.join(DATA,"fred_daily.json")
COSD="2015-01-01"
# (series_id, needs daily->monthly aggregation?)
SERIES=[("DGS2",True),("FEDFUNDS",False),("DGS3MO",True),("DGS10",True),("DFEDTARU",True),
        ("DGS30",True),("BAA",True),("AAA",True),("BAMLH0A0HYM2",True),("BAMLC0A0CM",True),
        ("IRLTLT01DEM156N",False),("IRLTLT01GBM156N",False),("IRLTLT01JPM156N",False),
        ("IRLTLT01FRM156N",False),("IRLTLT01ITM156N",False),("IRLTLT01CAM156N",False),("IRLTLT01AUM156N",False),
        ("BAMLC0A1CAAA",True),("BAMLC0A4CBBB",True),("BAMLH0A3HYC",True),("MORTGAGE30US",True)]
# Expanded sovereign 10Y cross-section (OECD long-term gov-bond yields, monthly, keyless). Any that
# are discontinued/empty get skipped per-series (the loop is resilient); we use whatever returns.
SERIES += [(f"IRLTLT01{cc}M156N", False) for cc in
           ["ES","NL","BE","AT","CH","IE","PT","FI","SE","NO","DK","PL","CZ","HU","KR","NZ","MX","CL","GR"]]
DAILY=["DGS2","EFFR","DGS3MO"]   # daily 2Y, daily effective fed funds (EFFR; DFF often 504s on fredgraph), daily 3M
BASE="https://fred.stlouisfed.org/graph/fredgraph.csv"

def _get(url):
    # Prefer curl (portable in restricted sandboxes); fall back to urllib.
    if shutil.which("curl"):
        try:
            r=subprocess.run(["curl","-s","--max-time","40",url],capture_output=True,text=True,timeout=60)
            if r.returncode==0 and r.stdout.strip(): return r.stdout
        except Exception: pass
    req=urllib.request.Request(url, headers={"User-Agent":"bubble-map/1.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def fetch(sid, agg):
    url=f"{BASE}?id={sid}&cosd={COSD}"+("&fq=Monthly&fam=avg" if agg else "")
    txt=_get(url)
    out={}
    for ln in txt.splitlines()[1:]:
        parts=ln.split(",")
        if len(parts)<2: continue
        d,v=parts[0],parts[1].strip()
        if v in ("",".","NaN"): continue
        out[d[:7]]=float(v)         # key by YYYY-MM
    return out, url

def fetch_daily(sid):
    url=f"{BASE}?id={sid}&cosd={COSD}"
    txt=_get(url); out={}
    for ln in txt.splitlines()[1:]:
        parts=ln.split(",")
        if len(parts)<2: continue
        d,v=parts[0],parts[1].strip()
        if v in ("",".","NaN"): continue
        out[d]=float(v)             # key by YYYY-MM-DD
    return out, url

def main():
    data={}; meta={"fetched": None, "source":"FRED keyless CSV (fredgraph.csv)", "cosd": COSD, "series_urls":{}}
    try:
        for sid,agg in SERIES:
            try:
                vals,url=fetch(sid,agg)
                if vals: data[sid]=vals; meta["series_urls"][sid]=url
                else: print(f"  (empty, skipped: {sid})")
            except Exception as se:
                print(f"  (skip {sid}: {se})")
            time.sleep(1.0)
        if not data: raise RuntimeError("no series returned")
        meta["fetched"]= "live-fetch (re-run fetch_fred.py to refresh)"
        json.dump({"meta":meta,"data":data}, open(OUT,"w"), indent=1)
        n=min(len(v) for v in data.values())
        print(f"wrote {OUT}: {len(data)} series, ~{n} monthly points each (since {COSD}).")
    except Exception as e:
        if os.path.exists(OUT): print(f"monthly fetch failed ({e}); keeping existing cache {OUT}.")
        else: print(f"monthly fetch failed ({e}); no cache present. Run with network to populate.")
    # daily cache (for tick-by-tick 2Y vs funds lead-lag)
    dd={}; dmeta={"source":"FRED keyless CSV (fredgraph.csv)","cosd":COSD,"frequency":"daily","series_urls":{}}
    try:
        for sid in DAILY:
            vals,url=fetch_daily(sid); dd[sid]=vals; dmeta["series_urls"][sid]=url; time.sleep(1.2)
        json.dump({"meta":dmeta,"data":dd}, open(OUT_D,"w"), indent=1)
        n=min(len(v) for v in dd.values())
        print(f"wrote {OUT_D}: {len(dd)} series, ~{n} daily points each (since {COSD}).")
    except Exception as e:
        if os.path.exists(OUT_D): print(f"daily fetch failed ({e}); keeping existing cache {OUT_D}.")
        else: print(f"daily fetch failed ({e}); no daily cache. Re-run with network to populate.")

if __name__=="__main__": main()
