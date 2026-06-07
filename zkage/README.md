# zkage — the strongest cryptographic case for age verification, and why even it fails

> **This is a STEELMAN, not an endorsement.** `zkage/` builds the *best-possible* privacy-preserving
> age check — a real zero-knowledge proof of "age ≥ 18" that reveals nothing about the birth year —
> precisely to show that **even this is not good enough**, and that population-scale age verification
> should be **opposed as a category, not optimized**. Read the argument: [`../research/age-verification-abolition.md`](../research/age-verification-abolition.md) · formal: [`../models/z3/ageverif_futility.py`](../models/z3/ageverif_futility.py).

## Run it
```bash
python3 zkage/zk_age_proof.py
```
It prints the working proof **and** the reasons it still fails. (Pure Python stdlib; `ALL CHECKS PASSED` = the crypto is sound — which is the point: sound crypto, unsound system.)

## What the code shows (the steelman)
A genuine non-interactive ZK age proof: an issuer Schnorr-signs a Pedersen commitment to the birth
year; the verifier derives `Cv = g^(Y-18)·Cby⁻¹` and the holder proves `Cv ∈ [0, 2⁷)` via per-bit
OR-proofs + an equality proof (Fiat–Shamir). Verified: adult passes, exactly-18 passes, **minor is
refused**, **forged credential rejected**, **tampered proof rejected**, and **no secret scalar (birth
year / age / blinding) appears in the transcript**. Cryptographically, this is about as good as it gets.

## Why even this fails (the refutation — see the brief)
1. **Predicate leakage** — it still reveals the `age≥18` bit.
2. **Presence/absence metadata** — *that* you were asked, **where and when**, and whether you complied
   is behavioral surveillance the cryptography can't touch.
3. **Issuer centralization** — it still needs a trusted issuer = a centralized identity root = the
   breach point and coercion lever.
4. **Futility under breach** — once any population-scale identity system is breached or credentials are
   shared/stolen, the gate can't distinguish authorized from unauthorized (`ageverif_futility.py`: UNSAT).
5. **Honeypot** — the mandate manufactures a database of minors / identity↔behavior linkage.
6. **Legitimization trap** — a "private" version is used to *pass* the mandate, accelerating the
   surveillance regime. Shipping this as a *solution* would do harm; shipping it as a *refutation* does not.

## Use
Cite it when someone claims "age verification can be done privately with ZK." Yes — and it still
surveils adults, endangers children, and fails at its goal. **Oppose the requirement, not the lock.**
