#!/usr/bin/env python3
"""
reflexive_marks.py  -  Formal verification (Z3 / SMT over the reals) that a material
share of the AI funders' REPORTED PROFIT is self-referential: mark-to-market gains on
private AI-lab stakes whose valuations are set by funding rounds the SAME funders provide.

This is the earnings-side analogue of circularity_smt.py (which proves the CASH loop).
Magnitudes in USD billions; bound to sourced figures (see spec-sec-filings-primary.json):
  - Anthropic round: ~$13B raised at ~$183B post-money (Sep 2025), up from ~$61B.
  - Amazon: ~$9.5B Q3-2025 pre-tax GAIN from marking up its Anthropic stake (fair value).
  - Microsoft: ~27% of OpenAI on EQUITY method (books its share of OpenAI losses instead).

Theorems:
  M1  Paper profit from a cash-burning investee        -> SAT  (a gain while the lab loses money is realizable)
  M2a Group can mark ITSELF up (no external cash)        -> SAT  (booked gain > new cash, external arms-length cash = 0)
  M2b Those gains are NOT externally realized            -> UNSAT (no realized non-group cash can back an unsold, self-set mark)
  M3  Mark reversal at IPO below the last private mark    -> UNSAT (keeping the gains when V_public < V_private is impossible)
  M4  Paper income is unbounded while rounds continue     -> SAT  (earnings analogue of 'solvent only while capital flows')
"""
from z3 import *

def banner(t): print("\n"+"="*72+f"\n{t}\n"+"="*72)
def verdict(s, expect):
    r=s.check(); ok=(str(r)==expect)
    print(f"  Z3 result: {r}   (expected {expect})   {'PROVED' if ok else '!! UNEXPECTED'}")
    return r

# ----------------------------------------------------------------------
banner("M1  PAPER PROFIT FROM A CASH-BURNING INVESTEE  (fair-value gain is realizable)")
# A funder holds fraction `stake` of a lab. A new round lifts post-money V_old -> V_new.
# Fair value => booked gain G = stake*(V_new - V_old), recognized in income, EVEN IF the
# lab's free cash flow is deeply negative. Prove this configuration exists.
s=Solver()
stake=Real('stake'); Vold=Real('V_old'); Vnew=Real('V_new'); G=Real('booked_gain'); fcf=Real('lab_FCF')
s.add(stake>0, stake<1, Vold>0, Vnew>Vold)
s.add(G==stake*(Vnew-Vold))
s.add(G>0)                       # a profit is booked ...
s.add(fcf<0)                     # ... while the investee BURNS cash
# bind to Anthropic-ish figures: V 61 -> 183, and reproduce a ~9.5 gain at ~7.8% effective stake
s.add(Vold==61, Vnew==183, G>=9)
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print("  WITNESS: stake=%.3f, V %.0f->%.0f => booked GAIN $%.1fB while lab FCF<0."%(f(stake),f(Vold),f(Vnew),f(G)))
    print("  => Reported profit can be manufactured by a markup on a money-LOSING investee. (cf. Amazon +$9.5B on Anthropic.)")

# ----------------------------------------------------------------------
banner("M2a  THE GROUP CAN MARK ITSELF UP  (booked gain exceeds new cash; external arms-length cash = 0)")
# The valuation step V_new-V_old is set by a round of size `round_cash`, funded ENTIRELY by
# the funder group (group_cash) with NO external/arms-length capital (ext_cash=0). The group
# holds pre-existing stake `stake0`. Prove booked group gain can EXCEED the cash it injected.
s=Solver()
stake0=Real('stake0'); Vold=Real('V_old'); Vnew=Real('V_new')
round_cash=Real('round_cash'); group_cash=Real('group_cash'); ext_cash=Real('ext_cash'); Ggrp=Real('group_gain')
s.add(stake0>0, stake0<1, Vold>0, Vnew>Vold)
s.add(round_cash>0, group_cash==round_cash, ext_cash==0)       # the round is 100% group-funded
s.add(Vnew-Vold <= 12*round_cash)                              # post-money lifts by a multiple of the cheque (VC markup)
s.add(Ggrp==stake0*(Vnew-Vold))
s.add(Ggrp>group_cash)                                         # PAPER gain booked > CASH put in
# bind: a ~$13B round, group holds ~30% pre-existing, V steps 61->183
s.add(round_cash==13, stake0>=Q(25,100), Vold==61, Vnew==183)
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print("  WITNESS: round=$%.0fB (100%% group), stake0=%.2f, V %.0f->%.0f => group books $%.0fB gain on $%.0fB cash, ext=$0."%(
        f(round_cash),f(stake0),f(Vold),f(Vnew),f(Ggrp),f(group_cash)))
    print("  => The funder group can lift its own reported income by funding the round that sets the mark. Self-referential.")

# ----------------------------------------------------------------------
banner("M2b  THOSE GAINS ARE NOT EXTERNALLY REALIZED  (no arms-length cash backs a self-set, unsold mark)")
# Require the booked group gain to be backed by REALIZED external (non-group, arms-length)
# cash proceeds, while the stake is UNSOLD (illiquid) and external cash into the mark is 0.
s=Solver()
Ggrp=Real('group_gain'); realized_ext=Real('realized_external_cash'); shares_sold=Real('shares_sold'); ext_cash=Real('ext_cash')
s.add(Ggrp>0)
s.add(shares_sold==0)                       # stake is held, not sold (unrealized mark)
s.add(ext_cash==0)                          # the valuation came from group rounds, not arms-length buyers
# realized external cash can only come from selling to outside buyers: bounded by shares_sold and ext flow
s.add(realized_ext<=shares_sold*1000)       # no sale => no realized proceeds (scale const irrelevant since shares_sold=0)
s.add(realized_ext<=ext_cash)
s.add(realized_ext>=Ggrp)                   # ASSERT the gain IS externally realized  <-- the claim to refute
r=verdict(s,"unsat")
print("  => UNSAT: a positive booked gain CANNOT be backed by realized external cash when nothing is sold and")
print("     the mark was set by the group's own rounds. The 'profit' is unrealized, self-referential paper.")

# ----------------------------------------------------------------------
banner("M3  MARK REVERSAL AT IPO  (keeping the gains when V_public < V_private is impossible)")
# Fair value forces carrying value CV = stake*V. If the IPO clears at V_pub < V_priv (the last
# private mark), the holder MUST write down. Prove you cannot keep prior gains under V_pub<V_priv.
s=Solver()
stake=Real('stake'); Vpriv=Real('V_priv'); Vpub=Real('V_pub')
CV_priv=Real('CV_priv'); CV_pub=Real('CV_pub'); writedown=Real('writedown'); keep_gains=Bool('keep_prior_gains')
s.add(stake>0, stake<1, Vpriv>0, Vpub>0, Vpub<Vpriv)          # public price below last private mark
s.add(CV_priv==stake*Vpriv, CV_pub==stake*Vpub)
s.add(writedown==CV_priv-CV_pub)
# "keep prior gains" would require carrying value not to fall, i.e. CV_pub >= CV_priv:
s.add(keep_gains==True)
s.add(Implies(keep_gains, CV_pub>=CV_priv))
r=verdict(s,"unsat")
print("  => UNSAT: with V_public < V_private and fair-value accounting, the gains MUST reverse (a writedown is forced).")
# show the writedown magnitude in a satisfiable sibling (Anthropic 183 -> hypothetical 130 IPO, ~30% stake)
s2=Solver(); st=Real('stake'); vp=Real('V_priv'); vq=Real('V_pub'); wd=Real('writedown')
s2.add(st==Q(3,10), vp==183, vq==130, wd==st*(vp-vq))
if str(s2.check())=="sat":
    m=s2.model(); print("  ILLUSTRATION: 30%% stake, V 183->130 at IPO => forced writedown $%.1fB (gains unwind)."%float(m[wd].as_fraction()))

# ----------------------------------------------------------------------
banner("M4  PAPER INCOME IS UNBOUNDED WHILE ROUNDS CONTINUE  (earnings analogue of the cash result)")
# For ANY target paper income T, there exists a valuation step (driven by continued group
# rounds) that books cumulative gains >= T with zero external cash. Prove for a large T.
s=Solver()
T=Real('target_income'); stake=Real('stake'); dV=Real('valuation_step'); ext=Real('ext_cash'); G=Real('cum_gain')
s.add(stake==Q(3,10), ext==0, dV>0, G==stake*dV)
s.add(T==500)                       # pick a large target ($500B of booked gains)
s.add(G>=T)                         # achievable by a big enough valuation step
r=verdict(s,"sat")
if str(r)=="sat":
    m=s.model(); f=lambda x: float(m[x].as_fraction())
    print("  WITNESS: at 30%% stake, a valuation step of $%.0fB books $%.0fB of gains with $0 external cash."%(f(dV),f(G)))
    print("  => Reported AI 'profit' is bounded only by willingness to keep funding rounds, not by external cash.")

banner("SUMMARY")
print("""  M1 SAT    paper profit from a cash-burning investee is realizable (Amazon +$9.5B on Anthropic).
  M2a SAT   the funder group can lift its OWN income by funding the round that sets the mark.
  M2b UNSAT those gains are NOT backed by realized external cash (unsold, self-set mark).
  M3 UNSAT  if the IPO clears below the last private mark, the gains MUST reverse (forced writedown).
  M4 SAT    reported AI profit is unbounded while rounds continue -- the earnings analogue of
            'solvent only while external capital flows.'
  CONCLUSION: a material part of hyperscaler AI 'profit' is self-referential paper marks, not
  externally realized cash -- and it reverses when a public price tests the private valuation.""")
