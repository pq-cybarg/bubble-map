#!/usr/bin/env python3
"""
fetch_yahoo.py - keyless Yahoo Finance chart-API ingest of bond-ETF prices+dividends ->
data/yahoo_monthly.json. Used to build PER-STATE municipal yield proxies (and corporate
cuts) that FRED's free endpoint and the licensed TRACE/EMMA feeds don't expose cheaply.

For each ETF we store monthly close + that month's dividend; build_charts.py computes a
trailing-12-month DISTRIBUTION YIELD = sum(last 12 monthly dividends)/price as the yield proxy.
This is a proxy (not the official AAA-GO curve / SEC yield), labeled as such.

Tickers: MUB (national muni), CMF (California muni), NYF (New York muni), HYD (high-yield muni),
         LQD (IG corporate), HYG (HY corporate), VCSH/VCIT/VCLT (short/int/long IG corporate).
curl-primary (sandbox-portable) with urllib fallback. Re-run to refresh.
"""
import os, json, subprocess, shutil, urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); os.makedirs(DATA,exist_ok=True)
OUT=os.path.join(DATA,"yahoo_monthly.json")
TICKERS=["MUB","CMF","NYF","HYD","LQD","HYG","VCSH","VCIT","VCLT",
         # equity SECTOR (GICS industry) ETFs for the industry cross-section (normalized price)
         "XLK","XLF","XLE","XLV","XLU","XLI","XLP","XLY","XLB","XLRE","XLC","SMH"]
BASE="https://query1.finance.yahoo.com/v8/finance/chart/"

def _get(url):
    if shutil.which("curl"):
        try:
            r=subprocess.run(["curl","-s","--max-time","40","-A","Mozilla/5.0",url],capture_output=True,text=True,timeout=60)
            if r.returncode==0 and r.stdout.strip(): return r.stdout
        except Exception: pass
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def ym(ts):
    import datetime
    return datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc).strftime("%Y-%m")

def fetch(tic):
    txt=_get(f"{BASE}{tic}?range=10y&interval=1mo&events=div")
    j=json.loads(txt); r=j["chart"]["result"][0]
    tss=r["timestamp"]; adj=r["indicators"].get("adjclose",[{}])[0].get("adjclose") or r["indicators"]["quote"][0]["close"]
    out={}
    for t,c in zip(tss,adj):
        if c is None: continue
        out[ym(t)]={"c":round(c,4),"d":0.0}
    for ts,ev in (r.get("events",{}).get("dividends",{}) or {}).items():
        m=ym(ev.get("date",ts));
        if m in out: out[m]["d"]=round(out[m].get("d",0.0)+ev["amount"],5)
        else: out[m]={"c":None,"d":round(ev["amount"],5)}
    return out

def main():
    data={}; meta={"source":"Yahoo Finance chart API (keyless)","range":"10y","interval":"1mo",
                    "note":"distribution-yield proxy = trailing-12mo dividends / price; not SEC yield / AAA-GO curve","tickers":TICKERS}
    try:
        import time
        for tic in TICKERS:
            try:
                data[tic]=fetch(tic); time.sleep(1.0)
            except Exception as e:
                print(f"  {tic} failed ({e})")
        if data:
            json.dump({"meta":meta,"data":data}, open(OUT,"w"), indent=1)
            print(f"wrote {OUT}: {len(data)} ETFs, ~{min(len(v) for v in data.values())} monthly points each.")
        elif os.path.exists(OUT): print("no data fetched; keeping existing cache.")
        else: print("no data fetched and no cache; re-run with network.")
    except Exception as e:
        print(f"yahoo fetch failed ({e}); "+("kept cache" if os.path.exists(OUT) else "no cache"))

if __name__=="__main__": main()
