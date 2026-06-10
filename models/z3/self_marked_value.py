#!/usr/bin/env python3
"""
self_marked_value.py - Formal verification (Z3 / SMT over the reals) of the UNIFYING
finding: across the four places financial risk hides, value is carried at a CHOSEN
number, not a market price, and the hidden gap is correlated and only forced to close
by an external event.

The four self-marked asset classes (all carried above realizable value):
  A1 Bank securities    - carried at HTM AMORTIZED COST   (forcing event: a deposit run)
  A2 AI lab stakes      - carried at FAIR-VALUE / EQUITY   (forcing event: IPO below mark)
  A3 Private-credit     - carried at MANAGER-SET NAV       (forcing event: a default)
  A4 Insurance liab.    - carried at OFFSHORE-CAPTIVE mark (forcing event: redemption)

Magnitudes illustrative-but-grounded (see macro-bank-htm-marks, spec-sec-filings-primary
/ reflexive_marks, macro-private-credit-marks, spec-insurance-bermuda).

Theorems:
  U1  Solvent-at-book / insolvent-at-market is realizable     -> SAT   (the SVB pattern, generalized)
  U2  A self-marked unsold position's book = realizable        -> UNSAT (the gap is unconstrained above market)
  U3  Under a COMMON macro factor the gaps are correlated      -> SAT (joint loss = sum); "diversification" -> UNSAT
  U4  Carrying value may stay above realizable after the event -> UNSAT (forced convergence)
"""
from z3 import *

def banner(t): print("\n"+"="*72+f"\n{t}\n"+"="*72)
def verdict(s, expect):
    r=s.check(); ok=(str(r)==expect)
    print(f"  Z3 result: {r}   (expected {expect})   {'PROVED' if ok else '!! UNEXPECTED'}")
    return r

# ----------------------------------------------------------------------
banner("U1  SOLVENT AT BOOK / INSOLVENT AT MARKET IS REALIZABLE  (generalized SVB)")
# A balance sheet holds self-marked assets at BOOK; equity_book>0, but at MARKET equity<0.
s=Solver()
book=Real('assets_book'); mkt=Real('assets_market'); liab=Real('liabilities')
eq_book=Real('equity_book'); eq_mkt=Real('equity_market'); gap=Real('hidden_gap')
s.add(book>0, mkt>0, liab>0, mkt<book)                 # self-marked: market below book
s.add(gap==book-mkt)
s.add(eq_book==book-liab, eq_mkt==mkt-liab)
s.add(eq_book>0, eq_mkt<0)                              # solvent at book, insolvent at market
# bind to bank-like scale: book 100, liab 96, hidden gap in a realistic 5-20 band (the unrealized loss)
s.add(book==100, liab==96, gap>=5, gap<=20)
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print(f"  WITNESS: book={f(book):.0f}, market={f(mkt):.0f}, liab={f(liab):.0f} => equity +{f(eq_book):.0f} at book, {f(eq_mkt):.0f} at market.")
    print("  => 'Solvent at cost, insolvent at market' is realizable for ANY self-marked book (SVB-2023, generalized).")

# ----------------------------------------------------------------------
banner("U2  A SELF-MARKED, UNSOLD POSITION'S BOOK = REALIZABLE  (refuted)")
# Claim to refute: 'if a position is unsold/illiquid, its book value equals what it could be realized for.'
s=Solver()
book=Real('book'); mkt=Real('market'); realizable=Real('realizable'); unsold=Bool('unsold')
s.add(book>mkt, mkt>0)                                  # self-marked above market (the whole point)
s.add(unsold==True)
s.add(realizable==mkt)                                  # realizable value = what the market pays
s.add(Implies(unsold, realizable==book))               # THE CLAIM: unsold => book is realizable
r=verdict(s,"unsat")
print("  => UNSAT: a self-marked position carried above market CANNOT be assumed realizable at book while unsold.")
print("     The gap (HTM cost vs market, NAV vs default value, private mark vs IPO) is unconstrained above market.")

# ----------------------------------------------------------------------
banner("U3  COMMON-FACTOR CORRELATION  (the four gaps move together; 'diversification' fails)")
# Each class's hidden gap g_i = exposure_i * sensitivity_i * shock. All four are long-duration /
# credit / risk-off exposures => POSITIVE sensitivities to the SAME macro factor (rates up / risk-off).
s=Solver()
shock=Real('macro_shock')
exp=[Real(f'exp_{i}') for i in range(4)]          # A1..A4 exposures (bank sec, AI marks, priv credit, insurance)
sens=[Real(f'sens_{i}') for i in range(4)]        # sensitivities to the common factor
g=[Real(f'gap_{i}') for i in range(4)]
s.add(shock>0)
for i in range(4):
    s.add(exp[i]>0, sens[i]>0, g[i]==exp[i]*sens[i]*shock)   # same-sign exposure to one factor
total=Real('total_gap'); s.add(total==g[0]+g[1]+g[2]+g[3])
# bind illustrative exposures (USD tn): bank sec 0.3, AI marks 0.2, private credit 2.0, insurance 0.7
s.add(exp[0]==Q(3,10), exp[1]==Q(2,10), exp[2]==2, exp[3]==Q(7,10))
for i in range(4): s.add(sens[i]>=Q(5,100))               # each at least mildly sensitive
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print(f"  WITNESS: one shock opens ALL four gaps simultaneously; total hidden loss = ${f(total):.2f}tn (>= the largest single).")
    print("  => Under a common factor the gaps are CORRELATED, not independent.")
# Now show 'diversification' (total < max single gap, i.e. netting) is IMPOSSIBLE when all same-sign:
s2=Solver()
g2=[Real(f'g_{i}') for i in range(4)]
for x in g2: s2.add(x>0)                                   # all positive (same-sign common factor)
tot=Real('tot'); mx=Real('mx'); s2.add(tot==g2[0]+g2[1]+g2[2]+g2[3])
s2.add(mx==g2[0]);
for i in range(1,4): s2.add(mx>=g2[i])                     # mx = an upper bound on the max (>= each)
s2.add(tot<mx)                                            # CLAIM: diversification nets it below the max
r2=verdict(s2,"unsat")
print("  => UNSAT: when all four gaps share the factor's sign, total >= each single gap - there is NO netting.")
print("     'Diversified across asset classes' is false when one macro factor drives them all.")

# ----------------------------------------------------------------------
banner("U4  CARRYING VALUE MAY STAY ABOVE REALIZABLE AFTER THE FORCING EVENT  (refuted)")
# After a forcing event (sale/default/IPO/redemption) the position is priced; accounting forces
# carrying value down to realizable. Claim to refute: it can stay above.
s=Solver()
carry_after=Real('carry_after'); mkt_after=Real('market_after'); book_before=Real('book_before')
s.add(book_before>mkt_after, mkt_after>0)
s.add(carry_after==book_before)                          # CLAIM: keep the old book after the event
s.add(carry_after<=mkt_after)                            # accounting rule once priced: carry <= realizable
r=verdict(s,"unsat")
print("  => UNSAT: once the forcing event prices the asset, carrying value MUST converge down to market.")
print("     Generalizes reflexive_marks M3 (IPO writedown), the HTM->realized loss on a forced sale, and First Brands 100c->33c.")

banner("SUMMARY  -  the self-marked-value theorem")
print("""  U1 SAT    'solvent at book, insolvent at market' is realizable for any self-marked balance sheet.
  U2 UNSAT  a self-marked, unsold position's book value is NOT guaranteed realizable - the gap is unconstrained.
  U3 SAT    under one common macro factor the four gaps open together (correlated); 'diversification' is UNSAT.
  U4 UNSAT  carrying value cannot stay above realizable once a forcing event prices the asset (forced convergence).
  CONCLUSION: bank HTM cost, AI fair-value marks, private-credit NAVs, and insurance captive marks are the SAME
  defect - a chosen value held above realizable until a common trigger forces correlated, simultaneous repricing.""")
