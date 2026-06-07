# zkage — prove "age ≥ 18" without revealing who you are

A **real, runnable, dependency-free** zero-knowledge proof that a person is over 18 **without
disclosing their birth year, exact age, or identity** — the privacy-preserving alternative to the
centralized digital-ID / ID-upload / facial-scan age verification this project documents
(`research/digitalid-*`).

The whole "freedom" stake in the analysis is that age/identity verification is being built as
**centralized surveillance** when it doesn't have to be. The fight isn't *ID vs no-ID* — it's
**centralized identity vs zero-knowledge proof.** This is a one-file demonstration that the
privacy-preserving version is buildable by one person.

## Run it
```bash
python3 zkage/zk_age_proof.py
```
Expected: `ALL CHECKS PASSED` (exit 0). No packages required (pure Python stdlib).

## What it proves (and hides)
- **Reveals:** only the boolean `age ≥ 18`.
- **Hides:** birth year, exact age, and identity — they live only inside perfectly-hiding
  Pedersen commitments; recovering them would require breaking the discrete-log problem.
- **Verified properties** (in the self-test): a valid adult passes; exactly-18 passes; a **minor
  cannot produce an honest proof**; a **forged (non-issuer-signed) credential is rejected**; a
  **tampered proof is rejected**; and **no secret scalar appears in the transcript**.

## How it works
- **Group:** prime-order-q subgroup of Z_p* using the RFC 3526 2048-bit safe prime; `g=4`, `h`
  hash-derived (unknown relative discrete log).
- **Credential:** an issuer (who checks your ID once, offline) **Schnorr-signs** a Pedersen
  commitment `Cby = g^birthyear · h^r` — attesting your age claim without learning a reusable identifier.
- **Presentation:** for year `Y`, the verifier derives `Cv = g^(Y-18) · Cby⁻¹ = commit(age-18, -r)`.
  The holder proves `Cv` opens to a value in `[0, 2⁷)` via **per-bit OR-proofs** (each committed bit
  is 0 or 1) plus an **equality/composition proof** — all made non-interactive with Fiat–Shamir.
- **Result:** the verifier learns `age ≥ 18 = true`, nothing else, with no server and no callback.

## Honest limitations
- Reference/education code — **not audited, not production**. Real deployments should use vetted
  libraries (BBS+ selective disclosure, Bulletproofs range proofs) and hardware-backed credentials.
- It does not solve issuance trust (who vouches for the birth year) or revocation — those are
  policy/PKI problems on top of the cryptography.
- It demonstrates the *principle*: predicate proofs can replace identity disclosure.

## Why it's in this repo
Because the highest-leverage move for a skilled individual (see `report/UNMASKING.md` and the
project's premise) is to **lower the cost of the privacy-preserving option** so the surveillance
version loses on merit. Fork it, harden it, ship it.
