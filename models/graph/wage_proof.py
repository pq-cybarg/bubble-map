#!/usr/bin/env python3
"""
wage_proof.py - separate what is PROVABLE from what is not, and certify how un-handwavable the
provable core is. Writes data/wage_proof.json (inlined by build_multidenom.py).

The page's wage panel makes an easy claim ("wages fell in gold") that is nearly a tautology and
privileges gold as 'real money' - a critic just answers "gold bubbled." This module builds to the
strongest claim that survives every such objection, and states plainly where proof stops.

THREE TIERS OF CERTAINTY
------------------------
  TAUTOLOGY   A change of units. "In gold, wages bought less." True given the numbers, but it
              only re-denominates and singles out gold; not deep, and not un-handwavable (the
              numeraire itself is in dispute).

  THEOREM     Numeraire-invariance of relative price. For any two goods A,B priced in a common
              money m, the exchange ratio p_A/p_B is invariant to the choice of m, because
                  p_A/p_B = (k*p_A)/(k*p_B)   for any positive conversion factor k.            [1]
              Therefore "a year of labor exchanges for fewer ounces of gold / fewer shares of the
              S&P 500 / less silver than in 2000" is a statement about LABOR'S RELATIVE PRICE. It
              does not require trusting the dollar, or gold, or any single asset, to be 'sound.'
              The only way to deny it is to deny the exchange ratios themselves (the data), not
              the monetary interpretation. That is the un-handwavable core.

  CONJECTURE  Everything causal or moral: that the dollar was 'debased', that the Fed / policy /
              any actor CAUSED it, that anyone was 'exploited.' Not decidable from these series.
              Rising asset prices and a fallen labor:asset ratio are the SAME fact seen two ways;
              which one you name the mover is a modelling choice, not a theorem.

THE ROBUSTNESS CERTIFICATE (the honesty bridge for approximate data)
--------------------------------------------------------------------
The wage & asset levels here are representative and rounded, so a bare ratio is not enough. Model
each of the four inputs (labor_2000, labor_2024, asset_2000, asset_2024) as only known to within a
uniform relative error e, and push all four in the direction MOST favorable to "no decline":

  R0 = (labor_2024/asset_2024) / (labor_2000/asset_2000)      (labor's relative price, 2024 vs 2000)
  R_worst(e) = R0 * ((1+e)/(1-e))**2                          (all four inputs adversarial)        [2]

The conclusion "labor's relative price FELL" (R0<1) survives until R_worst(e)=1, i.e. at the
BREAKDOWN ERROR
  e* = (1 - sqrt(R0)) / (1 + sqrt(R0))     for R0<1   (symmetric form for R0>1).                    [3]

e* is the answer to "how wrong would EVERY number have to be, at once, to make this go away?"
A claim is CERTIFIED (un-handwavable at this data quality) iff e* exceeds the assumed data
tolerance DATA_TOL. Claims below DATA_TOL are real but NOT certified - said so explicitly.
"""
import json, os, math
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

DATA_TOL=0.15   # assumed max uniform relative error in these representative figures (honest guess)

# Benchmark levels (2000, 2024) - mirror multi_denomination.py / wages.py (single source of truth).
LABOR={
 "All occupations (mean wage)": (34020, 65470),
 "Federal minimum wage (yr)":   (10712, 15080),
}
# Numeraires: independent stores of value. hard = monetary metal; liquid = tradable financial asset.
NUM=[
 ("Gold (oz)",          279,   2386,  "hard"),
 ("Silver (oz)",        5.00,  28.0,  "hard"),
 ("S&P 500 (index)",    1430,  5400,  "liquid"),
 ("US median home",     165000,420000,"real"),
 ("Commercial RE (CPPI)",57,   124,   "real"),
]

def breakdown_e(R0):
    """max uniform relative error e on all 4 inputs before the sign of (R0-1) flips (eq [3])."""
    s=math.sqrt(R0)
    return (1-s)/(1+s) if R0<1 else (s-1)/(s+1)

def certify(labor_name, l0, l24):
    rows=[]
    for name, a0, a24, kind in NUM:
        R0=(l24/a24)/(l0/a0)
        e=breakdown_e(R0)
        rows.append({
            "numeraire":name, "kind":kind,
            "labor_per_asset_2000": l0/a0, "labor_per_asset_2024": l24/a24,
            "R0": round(R0,4), "pct_of_2000": round(R0*100,1),
            "breakdown_e": round(e,4), "breakdown_pct": round(e*100,1),
            "direction": "fell" if R0<1 else "rose",
            "certified": bool(e>DATA_TOL and R0<1),
        })
    return rows

# Executable confirmation of theorem [1]: labor:gold computed via USD vs via silver-as-money agree.
def invariance_check():
    l0,l24=LABOR["All occupations (mean wage)"]
    g0,g24=279,2386; s0,s24=5.00,28.0
    via_usd_2024   = l24/g24                       # oz gold per yr, dollars as money
    via_silver_2024= (l24/s24)/(g24/s24)           # oz gold per yr, SILVER as money (units cancel)
    return {"via_usd": via_usd_2024, "via_silver": via_silver_2024,
            "identical": abs(via_usd_2024-via_silver_2024) < 1e-9}

out={
 "data_tol": DATA_TOL,
 "theorem": ("Relative price is numeraire-invariant: p_A/p_B = (k p_A)/(k p_B) for any positive k, "
             "so labor's exchange ratio against an asset does not depend on which money it is quoted in."),
 "invariance_check": invariance_check(),
 "labor": {name: certify(name,*lv) for name,lv in LABOR.items()},
 "not_proven": [
   "That the US dollar was 'debased' (gold/asset rises may have independent real causes).",
   "That any actor, policy, or institution CAUSED the change (correlation, not mechanism).",
   "Any moral claim - 'exploitation', 'theft', intent - none follow from an exchange ratio.",
   "The exact magnitudes: levels are representative & rounded; only the certified DIRECTIONS are claimed.",
 ],
}

# --- console proof ---
L="="*94
print(L); print("WAGE PROOF - what survives every objection, and how un-handwavable it is"); print(L)
ic=out["invariance_check"]
print(f"THEOREM check (labor:gold via dollars vs via silver-as-money): "
      f"{ic['via_usd']:.6f} vs {ic['via_silver']:.6f}  -> identical={ic['identical']}")
for name, rows in out["labor"].items():
    print("\n"+"-"*94); print(f"LABOR = {name}   (relative price 2024 vs 2000; e* = breakdown error)")
    print(f"  {'numeraire':<22}{'2000':>10}{'2024':>10}{'R0':>8}{'% of 2000':>11}{'e*':>8}   verdict")
    for r in rows:
        v="CERTIFIED" if r["certified"] else ("fell, not certified" if r["direction"]=="fell" else "rose")
        print(f"  {r['numeraire']:<22}{r['labor_per_asset_2000']:>10.3f}{r['labor_per_asset_2024']:>10.3f}"
              f"{r['R0']:>8.3f}{r['pct_of_2000']:>10.1f}%{r['breakdown_pct']:>7.0f}%   {v}")
    hard=[r for r in rows if r['kind']=='hard']
    minhard=min(r['breakdown_pct'] for r in hard)
    allfell=all(r['direction']=='fell' for r in rows)
    print(f"  => labor fell against ALL {len(rows)} numeraires: {allfell}. "
          f"Against hard money (gold & silver), overturning needs >{minhard:.0f}% uniform error in every input.")
print("\nNOT PROVEN:", *("\n  - "+x for x in out["not_proven"]))

json.dump(out, open(os.path.join(DATA,"wage_proof.json"),"w"), indent=2)
print("\nwrote data/wage_proof.json")
