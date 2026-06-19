#!/usr/bin/env python3
"""
fetch_fdic_qbp.py - build a multi-year industry time series from the FDIC BankFind
Suite financials API (api.fdic.gov), approximating the Quarterly Banking Profile (QBP)
aggregates by summing institution-level call-report data per quarter and computing
industry ratios from the sums. Caches to data/fdic_qbp.json for build_charts.py.

Env-free, public API. Tolerates network absence (leaves any existing cache in place).
Source: https://api.fdic.gov/banks/financials  (fields are call-report codes, $000).
"""
import json, os, time, urllib.request, urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT=os.path.join(ROOT,"data","fdic_qbp.json")
API="https://api.fdic.gov/banks/financials"
FIELDS=["ASSET","NETINCQ","EQ","ERNAST","NIMY","ROA","ROE","NCLNLS","LNLSGR","NTLNLSQ","LNATRES","DEP"]
YEARS=range(2011,2027)
QENDS=["0331","0630","0930","1231"]

def fetch_quarter(repdte):
    rows=[]; off=0
    while True:
        q=urllib.parse.urlencode({"filters":f"REPDTE:{repdte}","fields":",".join(FIELDS),
            "limit":10000,"offset":off,"format":"json"})
        with urllib.request.urlopen(f"{API}?{q}",timeout=60) as r:
            j=json.load(r)
        d=[x["data"] for x in j.get("data",[])]
        rows+=d
        if len(d)<10000: break
        off+=10000
    return rows

def num(x):
    try: return float(x)
    except (TypeError,ValueError): return None

def agg(rows):
    A=NI=EQs=ERN=NCL=LNL=NCO=RES=DEPs=0.0
    roaW=roeW=nimW=0.0
    for r in rows:
        a=num(r.get("ASSET")); e=num(r.get("EQ")); er=num(r.get("ERNAST"))
        if a: A+=a
        if e: EQs+=e
        if er: ERN+=er
        for k,acc in (("NETINCQ","NI"),("NCLNLS","NCL"),("LNLSGR","LNL"),("NTLNLSQ","NCO"),("LNATRES","RES"),("DEP","DEPs")):
            v=num(r.get(k))
            if v is not None:
                if acc=="NI": NI+=v
                elif acc=="NCL": NCL+=v
                elif acc=="LNL": LNL+=v
                elif acc=="NCO": NCO+=v
                elif acc=="RES": RES+=v
                elif acc=="DEPs": DEPs+=v
        roa=num(r.get("ROA")); roe=num(r.get("ROE")); nim=num(r.get("NIMY"))
        if roa is not None and a: roaW+=roa*a
        if roe is not None and e: roeW+=roe*e
        if nim is not None and er: nimW+=nim*er
    R=lambda x,n:round(x,n)
    return {
        "institutions": len(rows),
        "assets_t":    R(A/1e9,3),                       # $000 -> $ trillions
        "net_income_b":R(NI/1e6,2),                      # $000 -> $ billions (quarterly)
        "roa":         R(roaW/A,3) if A else None,        # asset-weighted %
        "roe":         R(roeW/EQs,2) if EQs else None,    # equity-weighted %
        "nim":         R(nimW/ERN,3) if ERN else None,    # earning-asset-weighted %
        "noncurrent_rate": R(NCL/LNL*100,3) if LNL else None,
        "nco_rate":    R(NCO*4/LNL*100,3) if LNL else None,   # annualized quarterly
        "coverage":    R(RES/NCL*100,1) if NCL else None,     # reserves / noncurrent
        "deposits_t":  R(DEPs/1e9,3),
    }

def main():
    quarters=[]; series={}
    metrics=["institutions","assets_t","net_income_b","roa","roe","nim","noncurrent_rate","nco_rate","coverage","deposits_t"]
    for m in metrics: series[m]=[]
    for y in YEARS:
        for qe in QENDS:
            rep=f"{y}{qe}"
            try:
                rows=fetch_quarter(rep)
            except Exception as e:
                print(f"[FDIC-QBP] skip {rep}: {e}"); continue
            if not rows: continue
            a=agg(rows)
            lab=f"{y}-Q{QENDS.index(qe)+1}"
            quarters.append(lab)
            for m in metrics: series[m].append(a[m])
            print(f"[FDIC-QBP] {lab}: {a['institutions']} banks, NI ${a['net_income_b']}B, ROA {a['roa']}, noncur {a['noncurrent_rate']}%")
            time.sleep(0.3)
    if not quarters:
        print("[FDIC-QBP] no data fetched; leaving existing cache untouched"); return
    out={"asof":quarters[-1],"source":"FDIC BankFind Suite financials API (api.fdic.gov); industry aggregates summed from institution call reports",
         "quarters":quarters,"series":series}
    json.dump(out,open(OUT,"w"),indent=0)
    print(f"[FDIC-QBP] wrote {OUT}: {len(quarters)} quarters {quarters[0]}..{quarters[-1]}")

if __name__=="__main__": main()
