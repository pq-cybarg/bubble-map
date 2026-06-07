#!/usr/bin/env python3
"""
ageverif_futility.py - a formal (Z3) statement of why population-scale age verification fails:
the benefit is conditional and self-defeating, while the surveillance harm is unconditional.
This is a STRUCTURAL/logical argument (not an empirical claim about a specific system); it makes
the brief's logic explicit. Companion: research/age-verification-abolition.md.
"""
from z3 import *
def check(name,s,expect):
    r=s.check(); print(f"  [{name}] Z3: {r} (expected {expect})  {'PROVED' if str(r)==expect else '!! CHECK'}")

mandate        = Bool('mandate_enforced')
unforgeable    = Bool('credentials_unforgeable')
nontransferable= Bool('credentials_nontransferable')
effective      = Bool('gating_effective')          # system distinguishes minors from adults
surveillance   = Bool('mass_surveillance_exists')  # identity<->behavior linkage / DB of minors
forgeable      = Bool('breached_so_forgeable')
transferable   = Bool('shared_or_stolen')

base=[
    effective == And(unforgeable, nontransferable),   # effective ONLY if creds can't be forged or lent
    Implies(forgeable, Not(unforgeable)),             # a breach makes them forgeable
    Implies(transferable, Not(nontransferable)),      # sharing/theft makes them transferable
    Implies(mandate, surveillance),                   # the surveillance layer exists whenever the mandate is enforced
]
print("="*72); print("AGE-VERIFICATION FUTILITY  -  benefit self-defeating, harm unconditional"); print("="*72)

print("\n[A] Once credentials are forgeable OR transferable, effective gating is IMPOSSIBLE.")
s=Solver(); s.add(base); s.add(Or(forgeable,transferable)); s.add(effective)
check("A effective-under-breach", s, "unsat")
print("     => post-breach (or with normal sharing/theft), the gate cannot distinguish authorized")
print("        from unauthorized: kids use adult creds, adults use kid creds. Stated purpose: FAILS.")

print("\n[B] You cannot enforce the mandate WITHOUT the mass-surveillance layer.")
s=Solver(); s.add(base); s.add(mandate); s.add(Not(surveillance))
check("B mandate-without-surveillance", s, "unsat")
print("     => the surveillance harm is UNCONDITIONAL (holds whether or not gating ever works).")

print("\n[C] The realistic world (mandate + breach + sharing) yields surveillance AND a broken gate.")
o=Solver(); o.add(base); o.add(mandate, forgeable, transferable)
print("  Z3:",o.check())
if o.check()==sat:
    m=o.model()
    print(f"     gating_effective = {m.eval(effective)}   mass_surveillance_exists = {m.eval(surveillance)}")
    print("     => SATISFIABLE only as: surveillance EXISTS, gating DOES NOT WORK. That is the steady state.")

print("\n"+"="*72)
print("CONCLUSION: age verification is a structure whose benefit (effective gating) is destroyed by")
print("the first breach or ordinary credential-sharing, while its harm (population-scale identity")
print("surveillance + a database of minors) is permanent and unconditional. No mechanism - including")
print("zero-knowledge proofs (see zkage/) - changes this; ZK hides the input, not the issuer, the")
print("presence/absence metadata, or the breach/honeypot dynamics. Oppose the requirement, not the lock.")
print("="*72)
