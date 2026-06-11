#!/usr/bin/env python3
"""
depreciation_trap.py - Formal verification (Z3 / SMT over the reals) of the AI-capex
DEPRECIATION + DURATION-MISMATCH trap: the fifth place a "chosen number" inflates reported
health. Useful-life is an assumption, not a price; stretching it borrows earnings from the
future, and when an AI asset's true ~2-3yr economic life is shorter than the 5-19yr debt /
lease financing it, the residual must be written off while the debt is still outstanding.

Grounded (graded) in:
  - Michael Burry (Nov 2025): hyperscalers depreciate Nvidia GPUs over 5-6yr vs a true ~2-3yr
    economic life -> ~$176B understated depreciation / overstated profit 2026-2028; ~$50-60B/yr
    if true life is 3 not 6. Meta raised server life to 5.5yr (cut dep $2.3B over 9mo 2025);
    MSFT $17B GPU over 6yr not 3 -> ~$2.9B/yr earnings overstatement.
  - Oracle FY2026 8-K: free cash flow NEGATIVE ~$23.7B, ~$50B capex, >$108B debt (+$30B raised),
    $523B RPO (>half OpenAI/Stargate), and $248B off-balance-sheet datacenter LEASES of 15-19yr
    term - against GPUs that economically age in ~2-3yr ("yesterday's data centers, tomorrow's debt").
  - justdario.com (2026-06): the asset-light->asset-heavy pivot + the no-graceful-exit debt trap.

This is the same defect as self_marked_value (U1-U4): a chosen carrying assumption held above
realizable until a forcing event. Here the chosen number is USEFUL LIFE and the event is RETIREMENT.

Theorems:
  D1  Optimistic life can report positive profit              -> SAT   (the headline earnings)
  D2  Honest (short) life leaves profit >= optimistic profit  -> UNSAT (overstatement is structural)
  D3  Equity stays whole when asset life < financing tenor    -> UNSAT (the duration mismatch)
  D4  A life choice avoids profit losses AND a writedown      -> UNSAT (depreciation is only timing)
"""
from z3 import *

def banner(t): print("\n"+"="*72+f"\n{t}\n"+"="*72)
def verdict(s, expect):
    r=s.check(); ok=(str(r)==expect)
    print(f"  Z3 result: {r}   (expected {expect})   {'PROVED' if ok else '!! UNEXPECTED'}")
    return r

# ----------------------------------------------------------------------
banner("D1  OPTIMISTIC USEFUL LIFE CAN REPORT POSITIVE PROFIT  (the headline)")
# reported_profit = revenue - cash_opex - capex/useful_life (straight-line depreciation).
s=Solver()
R=Real('revenue'); C=Real('cash_opex'); K=Real('capex'); Lb=Real('life_book'); prof=Real('profit_book')
s.add(R>0,C>0,K>0,Lb>0)
s.add(prof==R-C-K/Lb)
# illustrative MSFT-like GPU tranche: gross margin before depreciation = 4, capex 17, booked life 6yr
s.add(R-C==4, K==17, Lb==6)
s.add(prof>0)                                   # claim: still profitable on the optimistic schedule
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print(f"  WITNESS: dep=K/Lb={17/6:.2f}/yr -> reported profit = +{f(prof):.2f} on a 6yr life.")
    print("  => With a long enough assumed life, the same asset prints a profit. The life is the free parameter.")

# ----------------------------------------------------------------------
banner("D2  HONEST (SHORTER) LIFE LEAVES PROFIT >= OPTIMISTIC PROFIT  (refuted)")
# Claim to refute: 'using the true, shorter economic life does not lower reported profit.'
s=Solver()
K=Real('capex'); Lt=Real('life_true'); Lb=Real('life_book')
pt=Real('profit_true'); pb=Real('profit_book'); base=Real('ebitda_pre_dep')
s.add(K>0, Lt>0, Lb>0, Lt<Lb)                   # true economic life is SHORTER than the booked life
s.add(pb==base-K/Lb, pt==base-K/Lt)
s.add(pt>=pb)                                   # THE CLAIM: honest life doesn't reduce profit
r=verdict(s,"unsat")
print("  => UNSAT: since Lt<Lb and K>0, K/Lt > K/Lb, so honest depreciation STRICTLY lowers profit.")
# quantify the overstatement gap = K*(1/Lt - 1/Lb)
s2=Solver(); gap=Real('overstatement'); K2=Real('K'); Lt2=Real('Lt'); Lb2=Real('Lb')
s2.add(K2==17, Lt2==3, Lb2==6, gap==K2*(1/Lt2-1/Lb2))
s2.check(); m=s2.model(); g=float(m[gap].as_fraction())
print(f"  WITNESS (MSFT-like): K=17, true 3yr vs booked 6yr -> annual overstatement = ${g:.2f}B (~Burry's $2.9B/yr).")
print("  => Industry-scale (Burry): ~$176B understated depreciation / overstated profit 2026-2028.")

# ----------------------------------------------------------------------
banner("D3  EQUITY STAYS WHOLE WHEN ASSET LIFE < FINANCING TENOR  (refuted: the duration mismatch)")
# Debt-financed asset: book value depreciates over La; debt/lease amortizes over Ld>La.
# At a time t in (La, Ld): asset book = 0 but debt outstanding > 0 -> negative contribution to equity.
s=Solver()
K=Real('capex'); D=Real('debt'); La=Real('asset_life'); Ld=Real('financing_tenor'); t=Real('t')
asset=Real('asset_book'); debt=Real('debt_outstanding')
s.add(K>0, D==K, La>0, Ld>La, t>La, t<Ld)               # debt-financed; we look between the two horizons
s.add(La==3, Ld==15, t==9)                              # GPU ~3yr vs Oracle-style 15-19yr lease; midpoint
s.add(asset==If(t<=La, K*(1-t/La), 0))                  # straight-line to zero by La, then nothing left
s.add(debt==D*(1-t/Ld))                                 # straight amortization of the financing
s.add(asset>=debt)                                      # THE CLAIM: the asset still covers the debt
r=verdict(s,"unsat")
s3=Solver()  # exhibit the hole explicitly
K3=17.0; Ld3=15.0; tt=9.0; debt_left=K3*(1-tt/Ld3)
print(f"  => UNSAT: at t=9yr the GPU asset is fully depreciated (book 0) while ~${debt_left:.1f}B of its 15yr")
print("     financing is still outstanding. Asset life < financing tenor => a residual liability with NO asset.")
print("     This is Oracle's $248B of 15-19yr datacenter leases against ~3yr GPUs ('tomorrow's debt').")

# ----------------------------------------------------------------------
banner("D4  A LIFE CHOICE AVOIDS BOTH PROFIT LOSSES AND A WRITEDOWN  (refuted: depreciation is only timing)")
# Total depreciation over an asset's life is fixed (=K); a longer book life just defers expense.
# By retirement at La, cumulative depreciation booked = K * (La/Lb). The un-depreciated RESIDUAL
# = K*(1 - La/Lb) must be written off when the (now worthless) asset is retired -> a catch-up.
s=Solver()
K=Real('capex'); La=Real('asset_life'); Lb=Real('book_life'); residual=Real('residual_writedown')
s.add(K>0, La>0, Lb>0, Lb>La)                           # stretch the booked life beyond the true life
s.add(residual==K*(1-La/Lb))                            # what is left un-expensed at retirement
s.add(residual<=0)                                      # THE CLAIM: no catch-up writedown remains
r=verdict(s,"unsat")
print("  => UNSAT: stretching book life beyond true life ALWAYS leaves a positive residual that must be")
print("     written off at retirement. Depreciation is timing only - a long life borrows earnings from the")
print("     future, and the asset's economic death forces the catch-up. No schedule escapes it.")

banner("SUMMARY  -  the depreciation / duration-mismatch trap")
print("""  D1 SAT    a long assumed useful life makes the same asset print a profit (life is the free parameter).
  D2 UNSAT  the true, shorter economic life strictly lowers profit - the overstatement is structural,
            ~$2.9B/yr for one MSFT GPU tranche, ~$176B industry-wide 2026-2028 (Burry).
  D3 UNSAT  when asset life (~3yr GPUs) < financing tenor (5-7yr bonds, 15-19yr leases), equity cannot
            stay whole - there is an interval with a live debt and a dead asset (Oracle's $248B leases).
  D4 UNSAT  no depreciation-life choice avoids BOTH near-term losses and a retirement writedown -
            depreciation is timing; a stretched life only defers the loss and forces a catch-up.
  CONCLUSION: 'useful life' is the fifth self-marked number (cf. self_marked_value U1-U4). Stretching it
  inflates today's AI earnings and hides that debt-financed, fast-obsoleting compute is underwater before
  it is paid for - the formal core of the justdario asset-heavy / no-graceful-exit thesis.""")
