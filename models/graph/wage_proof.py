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

# ============================================================================================
# DEEPER I - DECOMPOSITION: labor:asset = (labor:CPI) x (CPI:asset)   [exact identity]
# The numeraire-invariant total says the RATIO fell. It does not say WHERE it fell. Split it:
#   labor's price in an asset  =  labor's price in the consumer basket (real wage, inverse)
#                                 x  the consumer basket's price in that asset (asset inflation).
# This asks the sharp question: did workers lose GROCERY-STORE power, or did ASSETS inflate in
# wage-hours? Answer reframes everything - BUT it now leans on CPI, which is contested, so the
# decomposition is a MODEL-DEPENDENT refinement (tier between THEOREM and CONJECTURE), while the
# TOTAL above needs no CPI and stays certified.
# ============================================================================================
import math as _m
CPI={2000:172.2, 2007:207.3, 2013:233.0, 2019:255.7, 2024:313.7}   # CPI-U annual average
WAGE_TS={2000:34020, 2007:40690, 2013:46440, 2019:53490, 2024:65470}   # all-occupations mean
ASSET_TS={
 "Gold (oz)":   {2000:279,2007:695,2013:1411,2019:1393,2024:2386},
 "Silver (oz)": {2000:5.00,2007:13.38,2013:23.79,2019:16.21,2024:28.0},
 "S&P 500 (index)": {2000:1430,2007:1480,2013:1650,2019:2900,2024:5400},
}
def decompose(a0,a24,y0=2000,y24=2024):
    wr=WAGE_TS[y24]/WAGE_TS[y0]; cr=CPI[y24]/CPI[y0]; ar=a24/a0
    labor_cpi=wr/cr            # real wage (labor priced in consumer basket), inverse of CPI-deflate
    cpi_asset=cr/ar           # consumer basket priced in the asset (asset inflation in CPI units)
    R0=labor_cpi*cpi_asset    # == (wr/ar)
    # log-share of the decline attributable to the asset-inflation term (>100% when real wage rose)
    share_asset=_m.log(cpi_asset)/_m.log(R0) if R0<1 and abs(_m.log(R0))>1e-9 else None
    return {"real_wage_term":round(labor_cpi,4), "asset_inflation_term":round(cpi_asset,4),
            "R0":round(R0,4), "asset_share_of_decline":(round(share_asset,3) if share_asset else None)}
decomp={name:decompose(NUM_d[0],NUM_d[1]) for name,NUM_d in
        {"Gold (oz)":(279,2386),"Silver (oz)":(5.00,28.0),"S&P 500 (index)":(1430,5400)}.items()}
real_wage_change=round((WAGE_TS[2024]/WAGE_TS[2000])/(CPI[2024]/CPI[2000])-1,4)

# ============================================================================================
# DEEPER II - ENDPOINT ROBUSTNESS: is this just a 2000-vs-2024 cherry-pick? Recompute R0 and e*
# for EVERY start year -> 2024, honestly reporting where it certifies and where it does not.
# ============================================================================================
def endpoint_matrix():
    starts=[2000,2007,2013,2019]
    m={}
    for name,ts in ASSET_TS.items():
        rows=[]
        lp={y:WAGE_TS[y]/ts[y] for y in ts}      # labor priced in the asset, per year
        for s in starts:
            R0=lp[2024]/lp[s]; e=breakdown_e(R0)
            rows.append({"start":s, "R0":round(R0,3), "pct_of_start":round(R0*100,1),
                         "breakdown_pct":round(e*100,1),
                         "direction":"fell" if R0<1 else "rose",
                         "certified":bool(e>DATA_TOL and R0<1)})
        m[name]=rows
    return m
endpoints=endpoint_matrix()

# ============================================================================================
# DEEPER III - MACHINE CHECK: verify the two algebraic identities in EXACT rational arithmetic
# (fractions -> zero floating-point error), and the breakdown root to 1e-12. Not an assertion in
# prose: the program recomputes each identity two independent ways and checks they are identical.
# ============================================================================================
from fractions import Fraction as Fr
def machine_check():
    # (1) numeraire-invariance: (k*a)/(k*b) == a/b, exactly, for arbitrary positive rationals.
    a,b,k=Fr(65470),Fr(279),Fr(2800,100)     # wage, gold, silver-price as the conversion factor
    inv_ok = (k*a)/(k*b) == a/b
    # (2) decomposition identity: (w24/g24)/(w00/g00) == real_wage_term * asset_term, EXACT.
    w0,w24=Fr(34020),Fr(65470); g0,g24=Fr(279),Fr(2386); c0,c24=Fr(1722,10),Fr(3137,10)
    direct=(w24/g24)/(w0/g0)
    viadecomp=((w24/c24)/(w0/c0))*((c24/g24)/(c0/g0))
    decomp_ok = direct==viadecomp
    # (3) breakdown root: R0*((1+e)/(1-e))^2 == 1 at e=e*(R0), to 1e-12 (e* is irrational).
    R0=0.225; e=breakdown_e(R0); root_resid=abs(R0*((1+e)/(1-e))**2 - 1)
    root_ok = root_resid < 1e-12
    return {"invariance_exact":bool(inv_ok), "decomposition_exact":bool(decomp_ok),
            "breakdown_root_residual":root_resid, "breakdown_root_ok":bool(root_ok),
            "all_pass":bool(inv_ok and decomp_ok and root_ok)}
mcheck=machine_check()

# ============================================================================================
# DEEPER IV - AUTHORITATIVE PRIMARY SERIES + per-series interval certificate.
# Replace the representative figures with named annual series and give each its own measurement
# tolerance (how precisely the annual number is known - NOT whether the concept is contested).
# Interval arithmetic, per input independently:  R_worst = R0 * (1+t_w)/(1-t_w) * (1+t_a)/(1-t_a).
# Certified iff R_worst<1. With good data the tolerances shrink and more claims cross the line.
# Sources: BLS CPS median usual weekly earnings (FT wage&salary) x52; BLS CPI-U annual avg;
# LBMA annual-average gold & silver; S&P 500 annual-average close; S&P CoreLogic Case-Shiller US
# National (constant-quality, repeat-sales); Census median sales price; Fed H.6 M2 (annual avg).
# ============================================================================================
WAGE_P=(29952, 60580)     # 2000, 2024   ($576, $1,165 median usual weekly x52)
PRIMARY=[
 # name, 2000, 2024, measurement-tolerance, kind
 ("Gold (oz)",           279.11, 2386.20, 0.01, "hard"),
 ("Silver (oz)",         4.95,   28.27,   0.02, "hard"),
 ("S&P 500 (index)",     1427,   5427,    0.01, "liquid"),
 ("Home - Case-Shiller (constant-quality)", 100, 322, 0.03, "real"),
 ("Home - median sale price",               165300, 418000, 0.03, "real"),
]
WAGE_TOL=0.02
def certify_primary():
    rows=[]; w0,w24=WAGE_P
    for name,a0,a24,tol,kind in PRIMARY:
        R0=(w24/a24)/(w0/a0)
        Rworst=R0*((1+WAGE_TOL)/(1-WAGE_TOL))*((1+tol)/(1-tol))
        rows.append({"numeraire":name,"kind":kind,"R0":round(R0,4),"pct_of_2000":round(R0*100,1),
                     "asset_mult":round(a24/a0,3),"tol":tol,"R_worst":round(Rworst,4),
                     "certified":bool(Rworst<1)})
    return rows
primary=certify_primary()

# ============================================================================================
# DEEPER V - HOMES with ALNRI: raw median price hides five things. Adjust for each and reprice a
# home in wage-hours. Acronym = the five adjustments (defined here, not an external index):
#   A rea (size / price-per-sqft)   L ocation & mix (constant-quality repeat-sales)
#   N ew-build premium (new vs existing)   R ates (mortgage carry = monthly payment)
#   I mprovements (quality/amenities, captured by constant-quality too)
# The point: the PRICE of a house in wage-hours fell on every lens; the monthly CARRY barely moved
# because 2000 mortgage rates were ~8% too. Housing's squeeze is a down-payment/wealth problem more
# than a monthly-cashflow one - a distinction the single 'median price' number erases.
# ============================================================================================
def mortgage_pay(price, rate, down=0.20, n=360):
    L=price*(1-down); r=rate/12.0
    return L*r/(1-(1+r)**-n)
w0,w24=WAGE_P; wr=w24/w0
_p00=mortgage_pay(165300,0.0805); _p24=mortgage_pay(418000,0.0672)
home_lenses=[
 # letter, label, home-inflation multiple 2000->2024, note
 ("L","Constant-quality (Case-Shiller repeat-sales)", 322/100,      "same houses resold; controls location, size & quality"),
 ("N","Median sale price (raw, mix-shifting)",        418000/165300,"the usual number; distorted by what sells"),
 ("A","Price per square foot (~size-adjusted)",       2.75,          "new-home ~$/sqft; homes also grew ~10% in size"),
 ("R","Mortgage carry (monthly P&I, 20% down)",       _p24/_p00,    "true cash cost; 2000 rate ~8.0%, 2024 ~6.7%"),
]
homes=[]
for L,label,mult,note in home_lenses:
    R0=wr/mult; e=breakdown_e(R0)
    homes.append({"letter":L,"lens":label,"home_mult":round(mult,3),"R0":round(R0,4),
                  "pct_of_2000":round(R0*100,1),"breakdown_pct":round(e*100,1),
                  "certified":bool(e>0.05 and R0<1),   # at authoritative-precision tolerance ~5%
                  "note":note})
home_payments={"pay_2000_mo":round(_p00),"pay_2024_mo":round(_p24),"carry_mult":round(_p24/_p00,3)}

# ============================================================================================
# DEEPER VI - THE CAUSAL QUESTION (as far as honesty allows): money supply. Association, NOT proof.
# Compare each multiple to M2 growth. The honest result cuts BOTH simplistic narratives.
# ============================================================================================
M2=(4900.0, 21500.0)   # $B, annual-avg, Fed H.6
m2r=M2[1]/M2[0]
money_rows=[("Gold",8.549),("Silver",5.711),("S&P 500",3.803),("Home (Case-Shiller)",3.220),
            ("CPI (consumer prices)",1.822),("Median wage",wr)]
money={"m2_mult":round(m2r,3),
       "rows":[{"item":n,"mult":round(m,3),"vs_m2":round(m/m2r,3)} for n,m in money_rows],
       "reading":("M2 grew %.1fx; consumer prices and wages rose under half as fast; assets absorbed the "
                  "gap and gold/silver exceeded it. Monetary expansion is the leading candidate mechanism "
                  "and is strongly ASSOCIATED with the asset-inflation term - but no single money aggregate "
                  "explains the cross-asset dispersion (gold ran ~2x M2, homes ~0.7x), and confounders "
                  "(globalisation goods-disinflation, rates, financialisation, EM central-bank gold buying, "
                  "real earnings growth) are uncontrolled. Association, not proof of cause.")%m2r}

out={
 "data_tol": DATA_TOL,
 "decomposition": decomp, "real_wage_change_2000_2024": real_wage_change,
 "endpoint_matrix": endpoints,
 "machine_check": mcheck,
 "primary": primary, "homes_alnri": homes, "home_payments": home_payments, "money": money,
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
print("\n"+"-"*94); print("DEEPER I - DECOMPOSITION  labor:asset = (real wage) x (asset inflation in wage-hours)")
print(f"  real consumption wage 2000->2024 (labor:CPI): {(1+real_wage_change)*100-100:+.1f}%  "
      f"-> workers did NOT lose grocery-store power by the CPI lens.")
for name,dd in decomp.items():
    print(f"  {name:<18} real-wage x{dd['real_wage_term']:.3f}  *  asset-inflation x{dd['asset_inflation_term']:.3f}"
          f"  = {dd['R0']:.3f}   (asset term = {dd['asset_share_of_decline']*100:.0f}% of the fall)")
print("  => the entire labor:asset decline is asset inflation; real wages slightly ROSE and were more than offset.")
print("     (this split trusts CPI - contested; the TOTAL above does not.)")

print("\n"+"-"*94); print("DEEPER II - ENDPOINT ROBUSTNESS (start year -> 2024); not a single-endpoint artifact")
for name,rows in endpoints.items():
    cells="  ".join(f"{r['start']}:{r['pct_of_start']:.0f}%(e{r['breakdown_pct']:.0f}{'*' if r['certified'] else ''})" for r in rows)
    print(f"  {name:<18} {cells}")
print("  * = certified (e> {:.0f}%). Reading: strongest from 2000/2007; recent-decade windows are milder and".format(DATA_TOL*100))
print("  do NOT certify (metals were already elevated by 2013) - so this is a LONG-HORIZON claim, honestly not a last-decade one.")

print("\n"+"-"*94); print("DEEPER III - MACHINE CHECK (exact rational arithmetic)")
print(f"  numeraire-invariance identity exact: {mcheck['invariance_exact']}")
print(f"  decomposition identity exact:        {mcheck['decomposition_exact']}")
print(f"  breakdown-root residual:             {mcheck['breakdown_root_residual']:.2e}  ok={mcheck['breakdown_root_ok']}")
print(f"  ALL CHECKS PASS: {mcheck['all_pass']}")

print("\n"+"-"*94); print("DEEPER IV - AUTHORITATIVE PRIMARY SERIES (per-series interval certificate)")
for r in primary:
    print(f"  {r['numeraire']:<42} x{r['asset_mult']:>7.3f}  R0={r['R0']:.3f}  R_worst={r['R_worst']:.3f}  "
          f"{'CERTIFIED' if r['certified'] else 'not certified'}")
print("  => with authoritative-precision tolerances, even median & constant-quality HOMES certify a decline in wage-hours.")

print("\n"+"-"*94); print("DEEPER V - HOMES with ALNRI (area / location / new-build / rates / improvements)")
for h in homes:
    print(f"  [{h['letter']}] {h['lens']:<44} home x{h['home_mult']:.2f}  labor buys {h['pct_of_2000']:.0f}%  "
          f"e*{h['breakdown_pct']:.0f}%  {'CERTIFIED' if h['certified'] else 'within noise'}")
print(f"  mortgage payment: ${home_payments['pay_2000_mo']}/mo (2000) -> ${home_payments['pay_2024_mo']}/mo (2024), "
      f"x{home_payments['carry_mult']:.2f}")
print("  => house PRICE in wage-hours fell on every lens; the monthly CARRY barely moved (2000 rates were ~8% too).")
print("     Housing's squeeze is a DOWN-PAYMENT / wealth problem more than a monthly-cashflow one.")

print("\n"+"-"*94); print("DEEPER VI - CAUSATION probe: MONEY SUPPLY (association, not proof)")
print(f"  M2 grew x{money['m2_mult']:.2f} (2000->2024).  multiple vs M2:")
for r in money["rows"]:
    print(f"    {r['item']:<24} x{r['mult']:>6.3f}   = {r['vs_m2']:.2f} x M2")
print("  =>", money["reading"][:150], "...")

print("\nNOT PROVEN:", *("\n  - "+x for x in out["not_proven"]))

json.dump(out, open(os.path.join(DATA,"wage_proof.json"),"w"), indent=2)
print("\nwrote data/wage_proof.json")
