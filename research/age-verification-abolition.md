# The case against age verification — even with zero-knowledge proofs

*Position brief, 2026-06-07. Claims graded; empirical facts separated from argument. Formal core:
`models/z3/ageverif_futility.py`. Companion: `zkage/` (the strongest crypto case for age
verification — and why even it fails).*

**Thesis:** population-scale age verification / "age assurance" is **futile-under-breach, a predator
honeypot, adult surveillance by construction, and not rescued by zero-knowledge proofs.** The correct
posture is to **oppose the requirement, not optimize the mechanism.** Building a "privacy-preserving"
version mainly *legitimizes the mandate*.

## 1. Futility under breach (formal — `ageverif_futility.py`)
A gate is *effective* only if credentials are **unforgeable AND nontransferable**. But:
- Every population-scale identity system is **eventually breached** → credentials become **forgeable**.
- Humans **share and steal** credentials → credentials are **transferable** (kids use adult creds;
  adults use kid creds).

Therefore, post-breach, the system **cannot distinguish authorized from unauthorized** — it fails at
its *stated* purpose. Z3 result: *"mandate effective AND (forgeable OR transferable)"* is **UNSAT**.
**The benefit is conditional and self-defeating; the surveillance infrastructure is unconditional.**
Once IDs are breached even once, IDs become meaningless for gatekeeping — anyone can be anyone.
(Grade: **STRONG** — structural + empirical.)

## 2. The honeypot externality
Mandates create **centralized linkage of real identity ↔ online behavior** and **databases of minors**
— precisely the target predators and hostile states want. **The mandate manufactures the very
vulnerability it claims to prevent**, and by (1) it *will* leak. "Verify the kids" builds the kid-finder.
(Grade: **STRONG**.)

## 3. Adult surveillance by construction
You **cannot verify a child without processing every adult**. The architecture surveils *everyone*;
"protect the children" is the politically unassailable wrapper. This repo documents who actually
benefits — Meta covertly funding the age-verification astroturf (`influence-meta-childsafety`),
Oracle/Ellison→Tony Blair Institute (`influence-tbi-policy`), Altman/World ID (`digitalid-corporate`):
the **ID-surveillance complex**, not children. (Grade: **STRONG** on architecture; beneficiary-steering
documented.)

## 4. Zero-knowledge proofs do **not** save it
ZK improves the *cryptographic* disclosure of the input — not the *systemic* harms:
- **(a) Predicate leakage:** a proof of `age≥18` still reveals that bit.
- **(b) Presence/absence metadata:** *that* you were asked, **where and when**, and whether you complied
  is behavioral surveillance — independent of the cryptography.
- **(c) Issuer centralization:** a ZK credential still needs a trusted **issuer = a centralized identity
  root** = the breach point and coercion lever from (1)/(2).
- **(d) Normalization:** it trains the **credential-presentation reflex** everywhere.
- **(e) The legitimization trap:** a "private" version is wielded to *pass* the mandate ("see, it can be
  done safely"), **accelerating adoption** of the surveillance regime.

`zkage/` demonstrates the best-case cryptography *and* its insufficiency. (Grade: **STRONG**.)

## 5. Accuracy harms (empirical)
Facial age estimation errs materially and **unequally**: Australia's own 2025 trial found ~**±18 months**
error, worse for girls, First Nations, and low-SES users (`digitalid-regulatory.json`). Result: false
gating and **discriminatory exclusion** layered on top of the surveillance. (Grade: **STRONG**, sourced.)

## 6. On intent (steelmanned, and why it doesn't matter)
The harms in (1)–(5) follow from the **architecture**, *regardless of anyone's intent*. So the case does
not depend on proving a "deliberate dystopia" — that's the stronger argument: even granting good faith,
the system surveils adults, endangers children, and fails at its goal. (Grade: intent **not required**.)

## 7. What to support instead (the alternative model)
- **Device/OS-level, family-controlled tools** — controls the *user/parent* owns, on the device, with
  no platform or state identity layer.
- **Default-private, minimize-by-design** products; **no population-scale identity** prerequisite.
- **Digital literacy / education**; **liability for demonstrated harms** (the tort path, not the ID path).
- **Oppose mandates** in notice-and-comment rulemaking and the courts. It works: the UK "BritCard" digital-ID
  compulsion was **walked back after a 2.9M-signature petition** (`influence-tbi-policy`).

## Bottom line
Don't build a better age gate. **Argue the category out of existence** — it cannot be made safe, it
cannot be made to work, and the "private" version is the trojan horse. Optimize *opposition*, not the lock.

## Why the mandate keeps coming anyway *(added 2026-06-11)*
The futility case explains why age verification *can't work*; it doesn't explain why it keeps being
mandated. That "why" is the control-rail incentive in [[digitalid-orchestration-real-incentive]]: age
verification is the **lever that de-anonymizes speech and money** under an unbeatable child-protection
frame — one track of the converging identity + programmable-money stack in
[[digitalid-worldcoin-eid-convergence]] (Worldcoin → eIDAS wallets → Digital Euro → Chat Control's
age-verification pivot → the UK Online Safety Act). Read together: this file shows the gate is *futile
and harmful*; the orchestration block shows *who benefits from building it anyway and why they can't say so*.

**Sources:** EFF and privacy-research consensus on age verification; this repo's `digitalid-regulatory.json`,
`digitalid-corporate.json`, `influence-meta-childsafety.json`, `influence-tbi-policy.json`,
`influence-ad-censorship.json`; formal: `models/z3/ageverif_futility.py`.
