#!/usr/bin/env python3
"""
scenario.py - parameterized SCENARIO ENGINE over the formal core. Dial the assumptions and
watch the verdicts + chokepoint timelines change. Z3 discharges the feasibility predicates
(OpenAI self-finance, core solvency at a given capital tap); arithmetic scans the chokepoint
years and the gold re-pricing. Three presets: BASE / BULL / BEAR(stress).

Edit a scenario dict (or add your own) and re-run:  python3 models/z3/scenario.py
"""
from z3 import *
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMAND_SM=5550   # kg/yr samarium-equiv (defense)

SCENARIOS={
 "BASE":{  # roughly today
   "gold":4300,"oai_rev0":20,"oai_growth":1.0,"oai_margin":0.5,"oai_commit":1400,
   "ext_capital":1100,"carry_stress":False,
   "allied_sep":{2026:800,2027:1500,2028:6000,2029:12000},
   "power_supply":{2026:18,2027:23,2028:34},"power_demand":{2026:25,2027:50,2028:80},
   "haleu_dom":{2027:900,2028:2500,2029:6000},"haleu_need":{2027:2000,2028:6000,2029:12000}},
 "BULL":{  # AI delivers, capital ample, allies ramp fast, rates ease
   "gold":3000,"oai_rev0":30,"oai_growth":1.5,"oai_margin":0.6,"oai_commit":1200,
   "ext_capital":1500,"carry_stress":False,
   "allied_sep":{2026:1200,2027:4000,2028:9000,2029:15000},
   "power_supply":{2026:25,2027:55,2028:90},"power_demand":{2026:25,2027:50,2028:80},
   "haleu_dom":{2027:1500,2028:5000,2029:12000},"haleu_need":{2027:1500,2028:5000,2029:10000}},
 "BEAR":{  # carry unwind cuts the capital tap, growth stalls, gold spikes, ramps slip
   "gold":6000,"oai_rev0":18,"oai_growth":0.4,"oai_margin":0.35,"oai_commit":1400,
   "ext_capital":300,"carry_stress":True,
   "allied_sep":{2026:600,2027:1000,2028:3000,2029:7000},
   "power_supply":{2026:15,2027:20,2028:28},"power_demand":{2026:28,2027:55,2028:90},
   "haleu_dom":{2027:700,2028:1800,2029:4000},"haleu_need":{2027:2500,2028:7000,2029:14000}},
}

def ops_funds_5y(r0,g,m): return m*r0*sum((1+g)**i for i in range(5))
def first_year(supply,need_const=None,need_map=None):
    for yr in sorted(supply):
        nd=need_const if need_const is not None else need_map[yr]
        if supply[yr]>=nd: return yr
    return None

def feasible(pred_constraints):
    s=Solver(); [s.add(c) for c in pred_constraints]; return str(s.check())

rows=[]; out={}
for name,p in SCENARIOS.items():
    ops=ops_funds_5y(p["oai_rev0"],p["oai_growth"],p["oai_margin"])
    gap=p["oai_commit"]-ops
    # Z3: can OpenAI self-finance? (assert ops>=commit)  ; can core stay solvent at this tap? (ext>=gap)
    selffin=feasible([RealVal(ops)>=RealVal(p["oai_commit"])])            # sat => self-financing possible
    solvent=feasible([RealVal(p["ext_capital"])>=RealVal(max(gap,0))])     # sat => solvent at this tap
    ree_yr=first_year(p["allied_sep"],need_const=DEMAND_SM)
    pow_yr=first_year({y:p["power_supply"][y] for y in p["power_supply"]},need_map=p["power_demand"])
    haleu_yr=first_year(p["haleu_dom"],need_map=p["haleu_need"])
    commit_gold=p["oai_commit"]*1e9/p["gold"]/1e6
    if solvent!="sat":            verdict="BREAKS"        # available capital can't cover the gap -> cascade
    elif gap<200 and not p["carry_stress"]: verdict="RESILIENT"  # near self-financing, tap not stressed
    else:                          verdict="FRAGILE"      # solvent ONLY while the capital tap stays open
    rows.append([name,f"${gap:,.0f}B",selffin.upper(),"YES" if solvent=="sat" else "NO",
                 ree_yr or ">2029",pow_yr or ">2028",haleu_yr or ">2029",f"{commit_gold:.0f}Moz",verdict])
    out[name]={"capital_gap_usd_b":round(gap),"self_finance":selffin,"solvent_at_tap":solvent=="sat",
               "ree_independent_year":ree_yr,"power_adequate_year":pow_yr,"haleu_year":haleu_yr,
               "commitments_gold_Moz":round(commit_gold),"verdict":verdict}

print("="*104)
print("SCENARIO ENGINE  -  formal verdicts under different assumptions (Z3 feasibility + chokepoint scans)")
print("="*104)
hdr=["scenario","OpenAI cap gap","self-fin?","solvent@tap","REE indep","power ok","HALEU ok","commit(gold)","VERDICT"]
print("  "+"".join(f"{h:<15}" for h in hdr))
for r in rows: print("  "+"".join(f"{str(c):<15}" for c in r))
print("\n  self-fin? = can OpenAI cover commitments from 5y ops (Z3 sat=yes). solvent@tap = ext capital >= gap.")
print("  BASE: needs the capital tap open + allies hit 2028 -> FRAGILE (works only while capital flows).")
print("  BULL: AI delivers + ample capital + fast allied ramp -> closest to self-sustaining.")
print("  BEAR: carry-unwind shuts the tap (ext $300B << gap), gold spikes, ramps slip -> BREAKS (the cascade).")
json.dump({"demand_samarium_kg":DEMAND_SM,"scenarios":out},open(os.path.join(ROOT,"data","scenarios.json"),"w"),indent=2)
print("\nwrote data/scenarios.json")
