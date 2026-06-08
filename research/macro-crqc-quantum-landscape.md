# The CRQC / quantum-advantage landscape — what's really happening

*Web-verified 2026-06-07. Full structured data + sources: `macro-crqc-quantum-landscape.json`. Pairs with `macro-quantum-computing.json` (equities/threat) and `macro-pqc-chips.json` (PQC/defense).*

## The claims are noisy — even the proofs get forged
- **Trail of Bits (Apr 17 2026)** *"We beat Google's zero-knowledge proof of quantum cryptanalysis"* — exploited memory-safety + logic bugs in Google's Rust **zkVM** and **forged a proof** claiming better quantum-circuit performance than Google's own. **The verification infrastructure behind the claim was unsound.** (On-thesis: claims need *real* verification.)
- Broader skepticism: Sycamore (2019)/Willow (2024) "supremacy/advantage" repeatedly narrowed by **classical tensor-network spoofing**; IBM disputed the 2019 claim; the sampled distribution is hard to verify; classical advantage returns beyond ~a few hundred qubits.

## The threat is real and *compressing* — and the loss is already happening
- **CRQC vs RSA-2048:** ~**2030 ±3**, but resource estimates fell from **~20M qubits → <1M → possibly ~100k** (2025-26 papers) — the clock is moving toward us.
- **Harvest-Now-Decrypt-Later (NSA, 2021):** adversaries are **collecting encrypted data now** to decrypt later. ~**95–100% of government-classified** and ~**98–100% of healthcare** data encrypted today is exposed to retroactive decryption. *The damage to long-lived secrets is already incurred; only the decryption is deferred.*

## The geopolitical race
| Power | Spend | Edge |
|---|---|---|
| **China** | ~$15B + a **$138B** (1T-yuan) AI/quantum/H2 VC fund | **leads quantum comms** (~12,000 km network + 2 Micius satellites) + sensing |
| **US** | NQI ~$1.2B→$1.8B; DOE $625M | computing + PQC + sensing |
| **EU** | Quantum Flagship €1B + **AGILE** defense roadmap | coordination + defense |
| **UK** | £2.5B (2024-34) + **£2B** (Mar 2026) | computing/procurement |
| **Russia** | ≥100B rubles | comms + sensing |

Increasingly **military** (sensing/PNT for GPS-denied navigation, secure comms, codebreaking). Corporate: **IBM** (roadmap → "Starling" fault-tolerant ~2029) and **Google** (Willow) lead; IonQ/Quantinuum/PsiQuantum/Rigetti/D-Wave/Microsoft(Majorana)/Amazon(Ocelot); China USTC/Origin. *(Broadcom is custom-AI-silicon, not quantum — see `fin-meta-family`/`fin-google-amazon-anthropic-meta`.)*

## The counter-migration (deadlines)
- **NSA CNSA 2.0:** NSS quantum-safe by **Jan 2027**, app-layer **2030**, full infra **2035**.
- **NIST:** RSA-2048/ECC deprecated **2030**, disallowed **2035** (FIPS 203/204/205 replace them).
- **EU:** national strategies + crypto inventories by **end-2026**; critical financial infra PQC by **2030** (DORA/NIS2/PCI-DSS 4.0).
- **G7** (US Treasury + Bank of England) urging banks/insurers/exchanges; **Trump 2026 Cyber Strategy** mandates PQC. Hybrid (classical+PQC) dominates rollouts.

## The city / infrastructure layer
Sub-national action is mostly **research/industry clusters** (Chicago Quantum Exchange; **Illinois Quantum & Microelectronics Park**, PsiQuantum anchor ~$500M; Maryland "Capital of Quantum"; Colorado "Elevate Quantum") **plus** a migration **burden** landing on under-resourced **municipal critical infrastructure** (utilities, water, transit, hospitals, courts) that must inventory + migrate crypto before 2030. *Cities are exposed nodes, not yet coordinated actors.*

## What's really happening (synthesis)
Three things at once: **(1) a claims problem** — advantage assertions are contested and even Google's ZK proof was forged, so "how close is Q-Day" is hype-prone; **(2) a real, compressing CRQC threat** whose harvest-now-decrypt-later loss to today's secrets is **already locked in**; **(3) a geopolitical race** — China leads comms/sensing and outspends via a $138B vehicle, the US/EU/UK lead compute + drive the PQC migration (2027–2035 deadlines). For this repo: **separate the real (HNDL, programs, PQC mandates, IBM/Google/IonQ engineering) from the hype (800×-sales pure-plays, forged proofs, "Q-Day next year" marketing).**
