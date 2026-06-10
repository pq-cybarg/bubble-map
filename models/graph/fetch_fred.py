#!/usr/bin/env python3
"""
fetch_fred.py - pull MONTHLY series from FRED's keyless CSV endpoint and cache to
data/fred_monthly.json (with provenance). No API key required. Reproducible: re-run to
refresh; build_charts.py reads the cache so the site renders even offline.

Series: DGS2 (2Y Treasury), FEDFUNDS (effective fed funds), DGS3MO (3M), DGS10 (10Y),
DFEDTARU (target upper). Daily series are aggregated to monthly average by FRED (fq/fam).
"""
import os, json, urllib.request, subprocess, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); os.makedirs(DATA,exist_ok=True)
OUT=os.path.join(DATA,"fred_monthly.json")
COSD="2015-01-01"
# (series_id, needs daily->monthly aggregation?)
SERIES=[("DGS2",True),("FEDFUNDS",False),("DGS3MO",True),("DGS10",True),("DFEDTARU",True)]
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

def main():
    data={}; meta={"fetched": None, "source":"FRED keyless CSV (fredgraph.csv)", "cosd": COSD, "series_urls":{}}
    try:
        for sid,agg in SERIES:
            vals,url=fetch(sid,agg); data[sid]=vals; meta["series_urls"][sid]=url
        meta["fetched"]= "live-fetch (re-run fetch_fred.py to refresh)"
        json.dump({"meta":meta,"data":data}, open(OUT,"w"), indent=1)
        n=min(len(v) for v in data.values())
        print(f"wrote {OUT}: {len(data)} series, ~{n} monthly points each (since {COSD}).")
    except Exception as e:
        if os.path.exists(OUT):
            print(f"fetch failed ({e}); keeping existing cache {OUT}.")
        else:
            print(f"fetch failed ({e}); no cache present. Run with network to populate.")

if __name__=="__main__": main()
