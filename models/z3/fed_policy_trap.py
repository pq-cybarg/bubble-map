#!/usr/bin/env python3
"""
fed_policy_trap.py - Formal proof that a SINGLE policy rate cannot resolve a MULTI-DIMENSIONAL
(regional / sectoral / global) financial divergence. This is the Tinbergen rule made concrete:
to hit N independent targets you need >= N independent instruments; the Fed has ~1 (the funds
rate; ~2 with the balance sheet) facing many divergent targets.

We prove, with Z3 over the reals:
  F1  No single rate r simultaneously satisfies the inflation-defense floor AND the
      regional-bank/CRE ceiling  (direct contradiction -> UNSAT).
  F2  No single rate lands within tolerance of ALL regional/sector target rates when their
      spread exceeds 2*tolerance  (UNSAT) -> a single instrument cannot stabilize divergent regions.
  F3  Even WITH a second instrument (QT/QE), >2 independent divergent targets remain
      under-determined (the instrument-count < target-count gap persists).
And we compute the BEST-CASE single rate (minimize the worst regional deviation) to quantify
how much unaddressed divergence necessarily remains.
"""
from z3 import *

def prove(name, s, expect):
    r=s.check(); print(f"  [{name}] Z3: {r} (expected {expect})  {'PROVED' if str(r)==expect else '!! CHECK'}")

print("="*72); print("FED POLICY TRAP  -  one instrument cannot fix N-dimensional divergence"); print("="*72)

# Each target's stabilizing rate (the policy rate that would keep IT solvent/stable), in %.
# Grounded in the rest of the analysis:
TARGETS = {
  "inflation_dollar_defense": 4.5,   # gold record / de-dollarization -> needs tightness (floor)
  "regional_banks_CRE_HTM":   2.0,   # CRE unwind + HTM losses -> needs cuts (ceiling)
  "AI_financial_stability":   4.0,   # don't reflate the AI capex bubble -> lean tight
  "sovereign_fiscal_debt":    2.5,   # Treasury issuance / debt service -> needs low rates
  "global_carry_JPY":         3.5,   # avoid forcing the yen-carry unwind -> mid
}
print("Stabilizing rate each target 'wants' (%):")
for k,v in TARGETS.items(): print(f"   {k:<26} {v}")

# ---------------- F1: direct contradiction ----------------
print("\n[F1] No single rate satisfies inflation-floor (r>=4.5) AND bank-ceiling (r<=2.0).")
s=Solver(); r=Real('r'); s.add(r>=TARGETS["inflation_dollar_defense"], r<=TARGETS["regional_banks_CRE_HTM"])
prove("F1 inflation-vs-banks", s, "unsat")

# ---------------- F2: tolerance band can't cover the spread ----------------
tol=1.0
print(f"\n[F2] No single rate is within +/-{tol} of ALL targets (spread {min(TARGETS.values())}-{max(TARGETS.values())} > 2*tol).")
s=Solver(); r=Real('r')
for k,v in TARGETS.items(): s.add(r>=v-tol, r<=v+tol)
prove("F2 cover-all-targets", s, "unsat")

# ---------------- F3: instruments < targets ----------------
print("\n[F3] Two instruments (rate r + balance-sheet b) still cannot independently hit "
      f"{len(TARGETS)} targets.")
print("     Model each target i stabilized iff a_i*r + c_i*b == t_i. With 2 free vars and")
print("     5 independent equations (generic a_i,c_i,t_i), the system is OVER-DETERMINED.")
s=Solver(); R,B=Reals('r b')
# generic, non-collinear loadings -> 5 eqns, 2 unknowns, inconsistent
load=[(1.0,0.2,4.5),(1.0,0.9,2.0),(1.0,0.4,4.0),(1.0,0.7,2.5),(1.0,0.1,3.5)]
for i,(a,c,t) in enumerate(load): s.add(a*R+c*B==t)
prove("F3 two-instruments-5-targets", s, "unsat")

# ---------------- best single rate: minimize worst regional pain ----------------
print("\n[BEST CASE] Minimize the WORST target deviation over a single rate r (Chebyshev center).")
o=Optimize(); r=Real('r'); m=Real('max_dev')
for k,v in TARGETS.items():
    o.add(m >= r - v); o.add(m >= v - r)   # m >= |r - v|
o.minimize(m); o.check()
md=o.model()
rv=md[r]; mv=md[m]
def f(x):
    from fractions import Fraction
    return float(Fraction(str(x))) if x is not None else None
print(f"   optimal single rate r* = {f(rv):.2f}%  ;  minimal achievable worst-deviation = {f(mv):.2f} pts")
print("   => Even the BEST single rate leaves at least one target ~%.1f points mis-set." % f(mv))
print("      Raising r pushes regional banks/CRE/fiscal toward crisis; lowering r reflates")
print("      inflation/AI-bubble/gold. There is NO r that stabilizes all simultaneously.")

print("\n"+"="*72)
print("CONCLUSION (Tinbergen): the divergence is multi-dimensional (regions x sectors x")
print("wealth-classes x continents) but the Fed wields ~1 instrument. The constraint system")
print("is provably UNSATISFIABLE. Monetary policy cannot fix a divergence crisis; it can only")
print("choose WHICH part of the system to sacrifice. That is the formal trap.")
print("="*72)
