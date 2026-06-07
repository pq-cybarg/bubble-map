#!/usr/bin/env python3
"""
regional_leverage.py - Hidden vs surfaced leverage, and REGIONAL divergence, from the
per-bank FDIC pull (data/bank_exposure.json).

  reported_leverage  = assets / equity                      (the surfaced number)
  hidden_leverage    = assets / (equity + HTM_loss + AFS_loss)   (mark securities losses to capital)
The gap = how much true leverage is masked by the un-marked HTM hole (the SVB blind spot).

Then aggregate vulnerability BY STATE to show the regional dispersion the single Fed rate
cannot address (input intuition for fed_policy_trap.py).
"""
import json, os
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
banks=json.load(open(os.path.join(ROOT,"data","bank_exposure.json")))["banks"]

for b in banks:
    eq=b["equity_b"] or 0
    adj_eq=eq + (b["htm_loss_b"] or 0) + (b["afs_loss_b"] or 0)   # losses are negative
    b["reported_leverage"]=round(b["assets_b"]/eq,1) if eq>0 else None
    b["hidden_leverage"]=round(b["assets_b"]/adj_eq,1) if adj_eq>0 else (9999 if adj_eq<=0 else None)
    b["leverage_inflation_x"]=round(b["hidden_leverage"]/b["reported_leverage"],2) if (b["reported_leverage"] and isinstance(b["hidden_leverage"],(int,float)) and b["hidden_leverage"]<9999) else None

print("="*90)
print("HIDDEN vs SURFACED LEVERAGE  (assets/equity vs assets/[equity marked for securities losses])")
print("="*90)
print("Largest leverage understatement (HTM/AFS losses masking true leverage):")
ranked=[b for b in banks if b["leverage_inflation_x"]]
for b in sorted(ranked,key=lambda x:-x["leverage_inflation_x"])[:12]:
    print(f"  {b['name'][:30]:<30} {b['state']}  reported {b['reported_leverage']:>5}x -> hidden {b['hidden_leverage']:>6}x "
          f"(x{b['leverage_inflation_x']})  HTMloss/eq={b['htm_loss_to_eq_pct']}%")
insolv=[b for b in banks if b["hidden_leverage"]==9999]
if insolv:
    print("\n  *** Banks whose equity is WIPED OUT if HTM+AFS losses were marked (negative adj. equity):")
    for b in insolv: print(f"      {b['name'][:34]:<34} {b['state']}  reported {b['reported_leverage']}x  HTMloss/eq={b['htm_loss_to_eq_pct']}%")

print("\n"+"="*90)
print("REGIONAL DIVERGENCE  -  bank stress aggregated by state (top 200 banks by assets)")
print("="*90)
st=defaultdict(lambda:{"n":0,"assets":0.0,"vuln":0,"cre_sum":0.0,"cre_n":0,"htm_sum":0.0,"htm_n":0,"unins_sum":0.0,"unins_n":0})
for b in banks:
    s=st[b["state"]]; s["n"]+=1; s["assets"]+=b["assets_b"]; s["vuln"]+=1 if b["vulnerable"] else 0
    if b["total_cre_to_t1_pct"] is not None: s["cre_sum"]+=b["total_cre_to_t1_pct"]; s["cre_n"]+=1
    if b["htm_loss_to_eq_pct"] is not None: s["htm_sum"]+=b["htm_loss_to_eq_pct"]; s["htm_n"]+=1
    if b["uninsured_ratio_pct"] is not None: s["unins_sum"]+=b["uninsured_ratio_pct"]; s["unins_n"]+=1
rows=[]
for state,s in st.items():
    rows.append((state,s["n"],s["assets"],s["vuln"],
                 s["cre_sum"]/s["cre_n"] if s["cre_n"] else 0,
                 s["htm_sum"]/s["htm_n"] if s["htm_n"] else 0,
                 s["unins_sum"]/s["unins_n"] if s["unins_n"] else 0))
print(f"{'ST':<4}{'#bk':>4}{'assets$B':>10}{'#vuln':>6}{'avgCRE/T1%':>11}{'avgHTM/eq%':>11}{'avgUnins%':>10}")
for r in sorted(rows,key=lambda x:-x[4])[:18]:
    print(f"{r[0]:<4}{r[1]:>4}{r[2]:>10.0f}{r[3]:>6}{r[4]:>11.0f}{r[5]:>11.1f}{r[6]:>10.0f}")
spread=[r[4] for r in rows if r[1]>=2]
if spread:
    print(f"\n  Regional CRE-concentration spread across states: {min(spread):.0f}% .. {max(spread):.0f}%  "
          f"(range {max(spread)-min(spread):.0f} pts)")
    print("  => A SINGLE national policy rate faces a wide regional dispersion of bank stress.")
    print("     This is the empirical input to fed_policy_trap.py: one instrument, many divergent regions.")
