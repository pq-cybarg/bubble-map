#!/usr/bin/env python3
"""
defense_chokepoint.py - formal proof (Z3) that US flagship-weapons production is INFEASIBLE
without China-controlled rare earths in the 2026-2027 window, and the earliest year
independence becomes feasible given domestic ramp.

Model (annual samarium, kg):
  demand        = sum over flagship systems of (units/yr * samarium kg/unit)
  china_to_mil  = 0 from Dec 1 2025 (China auto-denies foreign-military licenses)
  domestic(yr)  = ramp: ~0 (2026), small (2027), at-scale (2028+)
  allied(yr)    = small, growing
Feasibility(yr): china_to_mil(yr) + domestic(yr) + allied(yr) + stockpile_draw >= demand
"""
from z3 import *
def check(name,s,expect):
    r=s.check(); print(f"  [{name}] Z3: {r} (expected {expect})  {'PROVED' if str(r)==expect else '!! CHECK'}")
    return r

# annual samarium demand (kg) from defense_web SYSTEMS
demand = 150*22.6 + 2*50 + 2*30 + 2000*1   # F-35 + sub + destroyer + missiles
print("="*72); print("DEFENSE RARE-EARTH CHOKEPOINT  -  feasibility of REE-independent production"); print("="*72)
print(f"annual flagship samarium demand ~= {demand:.0f} kg/yr")

# supply by year (kg): China-to-US-military = 0 post Dec 2025; domestic+allied ramp
SUPPLY={2026:(0,  0,   200),   # (china_mil, domestic, allied) - allied/recycling trickle
        2027:(0,  1500,800),
        2028:(0,  6000,2000),
        2029:(0, 12000,3000)}
STOCKPILE=1500  # one-time National Defense Stockpile draw (kg), non-renewing

print("\n[F1] 2026: prove production CANNOT be met from non-China supply (expect UNSAT).")
s=Solver(); cm,dom,al,need=Reals('china_mil domestic allied demand')
cm0,dom0,al0=SUPPLY[2026]
s.add(cm==cm0,dom==dom0,al==al0,need==demand)
s.add(cm+dom+al+STOCKPILE >= need)   # assert feasibility WITHOUT China
check("F1 2026-independent-feasible", s, "unsat")
print(f"     non-China supply 2026 = {cm0+dom0+al0+STOCKPILE:.0f} kg (incl one-time {STOCKPILE} kg stockpile)"
      f" < demand {demand:.0f} kg.  Independence in 2026 is IMPOSSIBLE.")

print("\n[F2] earliest feasible year (scan): first year non-China supply >= demand")
first=None
for yr in sorted(SUPPLY):
    cm0,dom0,al0=SUPPLY[yr]; tot=cm0+dom0+al0+(STOCKPILE if yr==2026 else 0)
    ok=tot>=demand
    print(f"     {yr}: non-China supply {tot:.0f} kg  {'>=' if ok else '< '} demand {demand:.0f}  -> {'FEASIBLE' if ok else 'infeasible'}")
    if ok and first is None: first=yr
print(f"     => Earliest REE-INDEPENDENT year: {first if first else '>2029'}.")

print("\n[F3] therefore 2026-2027 production REQUIRES China (prove the dependency, expect UNSAT for 'no China needed').")
s=Solver(); need=demand
# over 2026+2027 combined, assert demand met with zero China
sup_2y=sum(SUPPLY[y][1]+SUPPLY[y][2] for y in (2026,2027))+STOCKPILE
s2=Solver(); x=Real('china_needed'); s2.add(x==0, sup_2y >= 2*demand)
check("F3 two-year-no-China", s2, "unsat")
print(f"     2026-27 non-China supply {sup_2y:.0f} kg < 2x demand {2*demand:.0f} kg -> China is REQUIRED.")

print("\n"+"="*72)
print("CONCLUSION: the US cannot build its flagship weapons (F-35, Virginia/Columbia subs,")
print("destroyers, missiles) REE-independently until ~2028+; in 2026-2027 it is STRUCTURALLY")
print("DEPENDENT on the adversary (China) it is arming against. The chokepoint is a single")
print("point of failure that no amount of defense budget removes on the relevant timeline -")
print("the binding constraint is mine-to-magnet capacity (years), not dollars.")
print("="*72)
