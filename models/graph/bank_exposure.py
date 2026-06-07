#!/usr/bin/env python3
"""
bank_exposure.py - Per-institution US bank vulnerability hierarchy from FDIC call-report data.
Pulls the largest banks (covering the vast majority of system assets), computes the three
vulnerability axes the analysis cares about, tiers them, and flags the exposed subset.

Axes:
  1. INVESTOR-CRE concentration vs Tier-1 capital  (construction + non-owner-occupied CRE) / RBCT1J
     -- the >300% supervisory flag; the CRE-unwind exposure.
  2. SECURITIES unrealized loss vs equity, split HTM vs AFS
     -- HTM losses are NOT in AOCI/regulatory capital (the SVB blind spot).
  3. UNINSURED deposit ratio (DEP-DEPINS)/DEP
     -- the run-risk fuel (SVB failure mode).
A bank is FLAGGED VULNERABLE if it is mid-tier AND scores high on >=2 axes.

FDIC fields ($000): ASSET, DEP, DEPINS(insured), EQ, RBCT1J(tier1), LNRECONS(construction),
  LNRENRES(nonfarm nonres), LNRENROT(non-owner-occ CRE), SCHA/SCHF(HTM cost/fair), SCAA/SCAF(AFS cost/fair).
"""
import json, urllib.request, os

ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); os.makedirs(DATA,exist_ok=True)
PERIOD="20260331"
FIELDS="CERT,NAME,STALP,BKCLASS,ASSET,DEP,DEPINS,EQ,RBCT1J,LNRECONS,LNRENRES,LNRENROT,SCHA,SCHF,SCAA,SCAF"
URL=(f"https://api.fdic.gov/banks/financials?filters=REPDTE:{PERIOD}"
     f"&fields={FIELDS}&sort_by=ASSET&sort_order=DESC&limit=200&format=json")

req=urllib.request.Request(URL,headers={"User-Agent":"bank-exposure-research research@example.com"})
raw=json.load(urllib.request.urlopen(req,timeout=60))
rows=[r["data"] for r in raw["data"]]

def g(r,k):
    v=r.get(k); return float(v) if v is not None else 0.0

banks=[]
EXCLUDED=0
for r in rows:
    # Exclude insured US BRANCHES of foreign banks (BKCLASS 'OI') - their 'equity' is a
    # branch-accounting artifact (capitalized by the overseas parent), not a US-bank balance sheet.
    # Also drop any row with non-positive assets or equity (leverage undefined).
    if r.get("BKCLASS")=="OI" or g(r,"ASSET")<=0 or g(r,"EQ")<=0:
        EXCLUDED+=1; continue
    asset=g(r,"ASSET"); eq=g(r,"EQ"); t1=g(r,"RBCT1J") or eq; dep=g(r,"DEP")
    investor_cre=g(r,"LNRECONS")+g(r,"LNRENROT")           # construction + non-owner-occupied
    total_cre=g(r,"LNRECONS")+g(r,"LNRENRES")
    htm_loss=g(r,"SCHF")-g(r,"SCHA")                        # fair - cost (neg = underwater)
    afs_loss=g(r,"SCAF")-g(r,"SCAA")
    secs_loss=htm_loss+afs_loss
    uninsured=dep-g(r,"DEPINS")
    b={"cert":int(g(r,"CERT")),"name":r.get("NAME"),"state":r.get("STALP"),"bkclass":r.get("BKCLASS"),
       "assets_b":round(asset/1e6,1),"equity_b":round(eq/1e6,2),
       "investor_cre_to_t1_pct":round(investor_cre/t1*100,0) if t1 else None,
       "total_cre_to_t1_pct":round(total_cre/t1*100,0) if t1 else None,
       "htm_loss_b":round(htm_loss/1e6,2),"afs_loss_b":round(afs_loss/1e6,2),
       "htm_loss_to_eq_pct":round(htm_loss/eq*100,1) if eq else None,
       "secs_loss_to_eq_pct":round(secs_loss/eq*100,1) if eq else None,
       "uninsured_ratio_pct":round(uninsured/dep*100,0) if dep else None}
    banks.append(b)

def tier(a):
    if a>=700: return "1_GSIB_mega"
    if a>=100: return "2_super_regional"
    if a>=50:  return "3_large_regional"
    if a>=10:  return "4_regional"
    return "5_community"
for b in banks: b["tier"]=tier(b["assets_b"])

# vulnerability flag: mid-tier banks scoring high on >=2 of 3 axes
def flags(b):
    f=[]
    if (b["investor_cre_to_t1_pct"] or 0)>=300: f.append("CRE>300%")
    if abs(b["secs_loss_to_eq_pct"] or 0)>=15: f.append("secs_loss>15%eq")
    if (b["uninsured_ratio_pct"] or 0)>=50: f.append("uninsured>50%")
    return f
for b in banks:
    b["flags"]=flags(b)
    b["vulnerable"]= (b["tier"] in ("2_super_regional","3_large_regional","4_regional")) and len(b["flags"])>=2

json.dump({"period":PERIOD,"source":"https://api.fdic.gov/banks/financials","n":len(banks),"banks":banks},
          open(os.path.join(DATA,"bank_exposure.json"),"w"),indent=2)

# ---- report ----
print("="*92)
print(f"US BANK HIERARCHICAL EXPOSURE  (FDIC call reports {PERIOD}; {len(banks)} US banks; "
      f"{EXCLUDED} foreign-branch/invalid rows excluded)")
print("="*92)
from collections import defaultdict
byt=defaultdict(list)
for b in banks: byt[b["tier"]].append(b)
for t in sorted(byt):
    ts=byt[t]; ta=sum(x["assets_b"] for x in ts)
    print(f"\n### TIER {t}  ({len(ts)} banks, ${ta/1000:.2f}T assets)")
    for b in sorted(ts,key=lambda x:-x["assets_b"])[:8]:
        print(f"  {b['name'][:34]:<34} ${b['assets_b']/1000:>5.2f}T  CRE/T1={str(b['investor_cre_to_t1_pct'])+'%':>6}"
              f"  HTMloss/eq={str(b['htm_loss_to_eq_pct'])+'%':>7}  unins={str(b['uninsured_ratio_pct'])+'%':>5}")

print("\n"+"="*92+"\n[BIGGEST HTM HOLES] HTM unrealized loss as % of equity (the un-marked SVB blind spot):")
for b in sorted(banks,key=lambda x:(x['htm_loss_to_eq_pct'] or 0))[:10]:
    print(f"  {b['name'][:34]:<34} HTM ${b['htm_loss_b']:>7.1f}B = {b['htm_loss_to_eq_pct']}% of equity   (AFS {b['afs_loss_b']:.1f}B)")

vuln=[b for b in banks if b["vulnerable"]]
print("\n"+"="*92+f"\n[VULNERABLE SUBSET] {len(vuln)} mid-tier banks flagged on >=2 axes (CRE unwind + securities loss + run risk):")
for b in sorted(vuln,key=lambda x:-(x['investor_cre_to_t1_pct'] or 0)):
    print(f"  {b['name'][:30]:<30} {b['state']}  ${b['assets_b']:>6.0f}B  {', '.join(b['flags'])}")
print(f"\nwrote data/bank_exposure.json   (full {len(banks)}-bank table)")
