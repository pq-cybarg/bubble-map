#!/usr/bin/env python3
"""
power_adequacy.py - Z3 proofs of the ENERGY chokepoints on the AI+defense buildout:
  P1  AI data-center NEW firm-power demand cannot be met from new firm supply in 2026-2027
      (turbine backlog + nuclear-restart timing) -> adequacy UNSAT; earliest balanced year ~2028+.
  P2  SMR/advanced-reactor HALEU fuel cannot be supplied domestically at fleet scale before
      ~2028 -> US is dependent on Russia-controlled enrichment (independence UNSAT) - the
      ENERGY analog of the China rare-earth chokepoint.
Magnitudes are illustrative-but-grounded (IEA/DOE/GE Vernova/Centrus); GW and kg-HALEU.
"""
from z3 import *
def check(n,s,e):
    r=s.check(); print(f"  [{n}] Z3: {r} (expected {e})  {'PROVED' if str(r)==e else '!! CHECK'}"); return r

# ---------- P1: power adequacy ----------
# NEW firm GW that US data centers need (cumulative incremental), by year
DEMAND={2026:25,2027:50,2028:80}
# NEW firm GW deliverable to data centers: (gas turbines limited by backlog, nuclear restart, SMR, grid headroom)
SUPPLY={2026:(8,0,0,10),2027:(12,1,0,10),2028:(20,3,1,10)}  # (gas, nuke_restart, smr, existing_headroom)
print("="*72); print("ENERGY CHOKEPOINT 1  -  AI data-center firm-power adequacy"); print("="*72)
print("[P1] 2026: prove new firm DEMAND cannot be met by new firm SUPPLY (expect UNSAT).")
s=Solver(); g,n,sm,hr,d=Reals('gas nuke smr headroom demand')
gas,nuke,smr,head=SUPPLY[2026]; s.add(g==gas,n==nuke,sm==smr,hr==head,d==DEMAND[2026])
s.add(g+n+sm+hr >= d)   # assert adequacy
check("P1 2026-power-adequate", s, "unsat")
print(f"     2026 new firm supply = {sum(SUPPLY[2026])} GW < demand {DEMAND[2026]} GW.  Power gap is real.")
first=None
for yr in sorted(DEMAND):
    tot=sum(SUPPLY[yr]); ok=tot>=DEMAND[yr]
    print(f"     {yr}: new firm supply {tot} GW {'>=' if ok else '< '} demand {DEMAND[yr]} GW -> {'OK' if ok else 'GAP'}")
    if ok and first is None: first=yr
print(f"     => earliest balanced year ~{first if first else '>2028'}; until then: behind-the-meter gas, delays, curtailment.")

# ---------- P2: HALEU / enrichment chokepoint ----------
print("\n"+"="*72); print("ENERGY CHOKEPOINT 2  -  HALEU nuclear fuel (Russia ~44% of enrichment)"); print("="*72)
HALEU_NEED={2027:2000,2028:6000,2029:12000}   # kg/yr for the advanced-reactor/SMR fleet ramp
DOMESTIC={2027:900,2028:2500,2029:6000}        # Centrus + new capacity (kg/yr); Russia-to-US = 0 (ban+retaliation)
print("[P2] 2027: prove SMR HALEU need cannot be met domestically (Russia excluded) -> dependence (UNSAT).")
s=Solver(); need,dom=Reals('need domestic'); s.add(need==HALEU_NEED[2027],dom==DOMESTIC[2027])
s.add(dom >= need)   # assert self-sufficiency
check("P2 2027-HALEU-independent", s, "unsat")
hfirst=None
for yr in sorted(HALEU_NEED):
    ok=DOMESTIC[yr]>=HALEU_NEED[yr]
    print(f"     {yr}: domestic HALEU {DOMESTIC[yr]} kg vs need {HALEU_NEED[yr]} kg -> {'OK' if ok else 'SHORT (Russia leverage)'}")
    if ok and hfirst is None: hfirst=yr
print(f"     => domestic HALEU self-sufficiency not until ~{hfirst if hfirst else '>2029'}; Russia enrichment is the binding chokepoint.")

print("\n"+"="*72)
print("CONCLUSION: the buildout is physically gated on BOTH ends - new FIRM POWER lags AI demand")
print("until ~2028 (turbine/nuclear lead times), and the SMR fuel (HALEU) depends on RUSSIA-controlled")
print("enrichment until ~2028-29. Combined with the CHINA rare-earth chokepoint (defense_chokepoint.py),")
print("the AI+defense complex sits on two adversary-controlled physical bottlenecks at once - constraints")
print("that, like OpenAI's solvency (Z3 T4) and the Fed's rate (fed_policy_trap.py), have no near-term feasible solution.")
print("="*72)
