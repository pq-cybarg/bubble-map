# ECDSA weak-nonce failure tracker — the "ECDSA.fail" thread

ECDSA is the signature scheme securing Bitcoin, Ethereum, and most non-PQC chains (via the **secp256k1** curve). It leaks the **private key** whenever the per-signature nonce `k` is reused, biased, or algebraically related across signatures. This is a **live, recurring failure class** — not a one-off — catalogued by disclosure projects (the "ECDSA.fail" thread) and a decade-plus of peer-reviewed blockchain scans. It matters twice over, on two different clocks.

## The mechanism (theorem, not opinion)
`r` in an ECDSA signature depends only on `k`, and `s` mixes `k` with the private key `d` in one linear equation. So the nonce is a **one-time mask over the private key** — and if the mask slips, the key shows through:
- **Reuse** — two signatures with the same `k` share the same `r`; that's two linear equations in two unknowns → **closed-form** recovery of `d`.
- **Bias / partial leakage** — if `k` is only partly random (fixed high bits, timing/power side-channel), a **lattice attack** on the Hidden Number Problem recovers `d` from many signatures.
- **Related nonces** — nonces needn't be identical, only *related*: the 2023 **Polynonce** attack breaks keys whose nonces follow a recurrence; the 2025 **two-affinely-related-nonces** result gives closed-form recovery from just **two** signatures under a known affine offset.

None of this is a weakness in elliptic-curve hardness — it's a **nonce-handling failure** (bad RNG, buggy library, weak embedded entropy).

## What's been found in the wild (fact, per study)
| Study | Scale / finding |
|---|---|
| **Brengel & Rossow** (RAID 2018) | Parsed **647,110,920** BTC signatures; **1,068** reused `r`-values across **4,433** keys. |
| **Biased Nonce Sense** (Breitner & Heninger, FC 2019) | Recovered **hundreds** of BTC + **dozens** of ETH/Ripple/SSH/HTTPS keys via lattice attacks on biased nonces. |
| **"Half-half" Bitcoin nonces** (IACR 2023/841) | A custom implementation (nonce = half message-hash bits + half secret-key bits) let attackers **empty hundreds** of BTC addresses for years; single-signature lattice recovery. |
| **Polynonce** (Kudelski, 2023) | Recurrence-related nonces; scan flagged **~1,000** BTC/ETH addresses. |
| **Chain Reactions** (arXiv 2026) | Nonce collisions compromising **Polygon MEV searcher** bots specifically. |
| **Sleep Reveals the Nonce** (arXiv 2026) | Sleep-based **power side-channel** leaking partial `k` → lattice recovery. |
| **SlowMist — `elliptic` JS library** (2025) | Malformed-input flaw: two distinct messages collapse to the same `k` → key leak from one `(r,s1),(r,s2)` pair. |

Historical anchors: the **PS3 fail0verflow** break (Sony used a *constant* `k`) and the **2013 Android SecureRandom** bug (predictable `k` drained real Bitcoin wallets).

## The honest limits
- **Most flagged addresses are already empty.** Multiple entities continuously scan chains for repeated `r`-values and sweep vulnerable keys, so "compromised" rarely means "currently drainable."
- **This is implementation failure, not an ECDSA break.** Correctly implemented **deterministic ECDSA (RFC 6979)** — `k = HMAC(message-hash, secret-key)` — or **EdDSA (Ed25519)**, which derives the nonce deterministically by design, closes the reuse/bias vector entirely.
- **The `ECDSA.fail` project's own headline counts** should be treated as *its* reported findings pending primary confirmation; this block anchors on the published/peer-reviewed scans above.

## Why it's on the map — the two-clock argument
ECDSA fragility is the **present-tense evidence** under the **future quantum threat**, and both point the same way:
1. **Now:** nonce-handling errors leak keys via bad randomness/side-channels/buggy libs — happening continuously.
2. **Later:** a cryptographically-relevant quantum computer running **Shor's algorithm** recovers ECDSA keys **directly from public keys** — no nonce error required — which is the "harvest-now, decrypt-later" logic for exposed on-chain pubkeys.

Different mechanisms, different timelines, **same migration.** RFC 6979 / EdDSA fix the classical footgun; the **PQC migration** (NIST **ML-DSA / SLH-DSA**, hash-based signatures) is the durable answer to *both*. **QRL**'s stateful hash-based **XMSS** design is the explicit post-ECDSA bet — niche in adoption, but its "ECDSA chains are structurally fragile" thesis is precisely what the nonce-failure record documents.

*Sources: Brengel & Rossow (RAID 2018); Breitner & Heninger "Biased Nonce Sense" (FC 2019); "half-half" Bitcoin nonces (IACR 2023/841); Kudelski "Polynonce" (2023); "Breaking ECDSA with Two Affinely Related Nonces" (IACR 2025/705); Buchanan "ECDSA Cracking Methods" (IACR 2025/654); "Chain Reactions" Polygon MEV (arXiv 2605.21498); "Sleep Reveals the Nonce" (arXiv 2602.01491); SlowMist "elliptic" analysis; RFC 6979; PS3 fail0verflow; 2013 Android SecureRandom. Cross-refs: macro-crqc-quantum-landscape, macro-quantum-computing, macro-pqc-chips, spec-defense-primes-pqc, spec-blockchain-ecosystem, blockchain-registry (QRL/XMSS).*
