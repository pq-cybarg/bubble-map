#!/usr/bin/env python3
"""
fetch_sources.py - PROVENANCE layer. Pull the proof's inputs from authoritative primary sources
(FRED keyless CSV = St. Louis Fed mirror of BLS/LBMA/S&P CoreLogic/Census/Fed) and write
data/sources_manifest.json: for each series, the source id, URL, unit, last-observation date, and
the annual value at each benchmark year. The build (wage_proof.py) reads this committed manifest,
so the site is reproducible OFFLINE while every number is traceable to a named series and vintage.

Run this when online to refresh:  python3 models/graph/fetch_sources.py
Series FRED does not host keyless (silver LBMA, long-history S&P 500) are recorded as DOCUMENTED
snapshots with fetched=false + citation - flagged honestly, never silently mixed with live data.
"""
import json, os, urllib.request, ssl
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")
CTX=ssl.create_default_context()
BENCH=[1989,1995,2000,2007,2013,2019,2024]

FRED={  # id -> (human description, unit)
 "CPIAUCSL":       ("CPI-U, all items, seasonally adj (BLS via FRED)", "index 1982-84=100"),
 "LEU0252881500Q": ("Median usual weekly earnings, full-time wage & salary (BLS via FRED)", "USD/week"),
 "CSUSHPINSA":     ("S&P CoreLogic Case-Shiller US National Home Price Index", "index Jan2000=100"),
 "MSPUS":          ("Median sales price of houses sold, US (Census/HUD via FRED)", "USD"),
 "M2SL":           ("M2 money stock, seasonally adj (Federal Reserve H.6 via FRED)", "USD billions"),
 "TNWBSHNO":       ("Households & nonprofits net worth (Federal Reserve Z.1 via FRED)", "USD millions"),
 "WFRBSTP1300":    ("Net worth share held by the Top 0.1% (Fed Distributional Financial Accounts)", "percent"),
 "WFRBST01134":    ("Net worth share held by the Top 1% (Fed DFA)", "percent"),
 "WFRBSB50215":    ("Net worth share held by the Bottom 50% (Fed DFA)", "percent"),
 "CUUR0000SEHA":   ("CPI rent of primary residence (BLS via FRED)", "index 1982-84=100"),
 "LABSHPUSA156NRUG":("Labor share of GDP, United States (Penn World Table via FRED)", "fraction"),
}
URL="https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"

def fetch(series_id):
    req=urllib.request.Request(URL%series_id, headers={"User-Agent":"provenance-fetch/1.0"})
    raw=urllib.request.urlopen(req, timeout=25, context=CTX).read().decode("utf-8","replace")
    if raw.lstrip().startswith("<"): raise ValueError("not CSV (series unavailable)")
    by_year=defaultdict(list); last=None
    for line in raw.splitlines()[1:]:
        if "," not in line: continue
        d,v=line.split(",",1); v=v.strip()
        if v in ("",".","NA"): continue
        try: val=float(v)
        except ValueError: continue
        yr=int(d[:4]); by_year[yr].append(val); last=d
    annual={y: round(sum(by_year[y])/len(by_year[y]),4) for y in by_year}   # annual mean
    return annual, last

manifest={"generated_note":"annual means from FRED keyless CSV; refresh via fetch_sources.py",
          "benchmarks":BENCH, "series":{}}
print("="*80); print("FETCHING PRIMARY SERIES"); print("="*80)
for sid,(desc,unit) in FRED.items():
    entry={"desc":desc,"unit":unit,"url":URL%sid,"fetched":False,"values":{}}
    try:
        annual,last=fetch(sid)
        entry["fetched"]=True; entry["as_of"]=last
        entry["values"]={str(y):annual[y] for y in BENCH if y in annual}
        got=",".join(f"{y}:{annual[y]:g}" for y in BENCH if y in annual)
        print(f"  [OK] {sid:<17} {got}")
    except Exception as e:
        print(f"  [--] {sid:<17} {e}")
    manifest["series"][sid]=entry

# series FRED does not host keyless (discontinued LBMA feeds / copyrighted IMF) -> documented, flagged
manifest["series"]["GOLD_LBMA"]={"desc":"Gold price, London fixing (LBMA; FRED feed discontinued 2022)","unit":"USD/oz",
  "url":"https://www.lbma.org.uk/prices-and-data/precious-metal-prices","fetched":False,
  "source_type":"documented snapshot (LBMA annual average)","values":{
    "1989":381,"1995":384,"2000":279.11,"2007":695.39,"2013":1411.23,"2019":1392.60,"2024":2386.20}}
manifest["series"]["SILVER_LBMA"]={"desc":"Silver price, London fixing (LBMA)","unit":"USD/oz",
  "url":"https://www.lbma.org.uk/prices-and-data/precious-metal-prices","fetched":False,
  "source_type":"documented snapshot (LBMA annual average)","values":{"2000":4.95,"2024":28.27}}
manifest["series"]["SP500_ANNUAL"]={"desc":"S&P 500 index, annual average close","unit":"index",
  "url":"https://www.spglobal.com/spdji/en/indices/equity/sp-500/","fetched":False,
  "source_type":"documented snapshot (annual-average close)","values":{
    "1989":323,"1995":542,"2000":1427,"2007":1477,"2013":1643,"2019":2913,"2024":5427}}

json.dump(manifest, open(os.path.join(DATA,"sources_manifest.json"),"w"), indent=2)
nf=sum(1 for s in manifest["series"].values() if s["fetched"])
print(f"\nwrote data/sources_manifest.json  ({nf} live-fetched, "
      f"{len(manifest['series'])-nf} documented-snapshot)")
