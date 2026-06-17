# The CRQC / quantum-advantage landscape — what's really happening

*Web-verified 2026-06-07. Full structured data + sources: `macro-crqc-quantum-landscape.json`. Pairs with `macro-quantum-computing.json` (equities/threat) and `macro-pqc-chips.json` (PQC/defense).*

## The claims are noisy — even the proofs get forged
- **Trail of Bits (Apr 17 2026)** *"We beat Google's zero-knowledge proof of quantum cryptanalysis"* — exploited memory-safety + logic bugs in Google's Rust **zkVM** and **forged a proof** claiming better quantum-circuit performance than Google's own. **The verification infrastructure behind the claim was unsound.** (On-thesis: claims need *real* verification.)
- Broader skepticism: Sycamore (2019)/Willow (2024) "supremacy/advantage" repeatedly narrowed by **classical tensor-network spoofing**; IBM disputed the 2019 claim; the sampled distribution is hard to verify; classical advantage returns beyond ~a few hundred qubits.

## The threat is real and *compressing* — and the loss is already happening
- **CRQC vs RSA-2048:** ~**2030 ±3**, but resource estimates fell from **~20M qubits → <1M → possibly ~100k** (2025-26 papers) — the clock is moving toward us.
- **Harvest-Now-Decrypt-Later (NSA, 2021):** adversaries are **collecting encrypted data now** to decrypt later. ~**95–100% of government-classified** and ~**98–100% of healthcare** data encrypted today is exposed to retroactive decryption. *The damage to long-lived secrets is already incurred; only the decryption is deferred.*

## HNDL's integrity twin — "Trust Now, Forge Later" (TNFL)
HNDL breaks **confidentiality** (collect ciphertext now, decrypt later). Its twin breaks **integrity**: once a CRQC (Shor) derives private keys from public keys, previously-issued **digital signatures become forgeable** — old certificates, signed identity assertions, and ePassport Passive-Authentication signatures can be **retroactively forged/impersonated**. HNDL breaks secrecy; **TNFL breaks authentication — which is exactly what a digital ID is *for*.** This is the mechanism under the **identity-proof paradox** in `spec-uk-labour-tbi-influence` (#68): the credential's whole value inverts into impersonability at Q-Day.

## Digital-ID PQC migration status — almost nothing is quantum-safe yet *(added 2026-06-16)*
*Empirical backing for the identity-proof paradox (#68) and "governments change slower than the threat." Web-verified 2026-06 (prompted by a shared Grok exchange whose checkable claims all verify).* **As of mid-2026 essentially no major deployed national/consumer digital-ID system is post-quantum** — the vast majority still run **RSA/ECC**.

- **Still classical (the majority):** the **EU EUDI Wallet** (eIDAS 2.0 prototypes use RSA/ECC; ENISA EU-wide cert only *after* 2026 — yet offered to all citizens 2026, businesses must accept from 2027, i.e. **mass rollout on breakable crypto**); **ICAO eMRTDs** (Doc 9303 Passive Authentication = RSA/ECDSA; quantum-safe update in progress, deployed docs classical); **national eIDs** (Estonia, India **Aadhaar**) and most **blockchain DIDs/SSI**.
- **Ahead (pilots/enablers, not deployed national IDs):** the **GSA PIV PQC experiment** with Unifyia (Dilithium L2/3/5 + hybrid — an *experiment*, with OS/browser/hardware auth gaps); **Microsoft SymCrypt** shipping **ML-KEM + ML-DSA in production** (Azure/M365/Win11/Server 2025, Nov-2025) with **AD CS ML-DSA cert issuance GA May 2026** — PQC reaching the **PKI backend**; **SEALSQ QS7001** post-quantum secure-element chip (the corpus's own `fin-sealsq-wisekey-global` / `macro-pqc-chips` node — real silicon, early ramp); **Wultra PQA** (vendor claim).
- **So what:** the migration is **barely begun for the exact systems being mandated now**. Every credential issued today on classical crypto is a **TNFL liability** (forgeable post-Q-Day), and re-issuing at population scale after a break is the **bootstrap-without-a-trusted-anchor** problem in #68. The things that are ahead are *backends* (Microsoft PKI), *experiments* (GSA), or *chips* (SEALSQ) — not the national wallets.

## Q-Day's silent-window asymmetry — the deadlines assume a break you'll be told about *(added 2026-06-16)*
The game theory the public deadlines ignore. *Underlying facts (HNDL incurred, deadlines public, the forged ZK proof, the documented collection apparatus) are fact; the concealment logic is labeled strategic reasoning — **no claim that any actor has a CRQC today**.*

- **The defender's assumption:** NIST 2030/2035 and CNSA 2.0 implicitly treat Q-Day as **observable** — that you'll know a CRQC exists in time to finish migrating. The whole deadline structure is a **defender's clock.**
- **The concealment incentive:** whoever reaches CRQC first has a **dominant strategy of silence** — revealing it would (a) trigger the world's immediate PQC migration, slamming the window shut, and (b) forfeit the live intelligence windfall (decrypt the HNDL backlog + forge signatures via TNFL). **The first CRQC is the one you're least likely to hear about; the public Q-Day lags the real one.**
- **The harvest-side advantage:** value accrues to whoever *also* harvested the most ciphertext/credentials → optimal play is **harvest now (cheap), decrypt/forge silently later.** Best-positioned = actors with **both** collection reach (NSA/Five-Eyes upstream + Room 641A lineage; China; the City-fibre/embassy vantage and Salt-Typhoon-style telecom breaches — `spec-disclosures-surveillance`, `spec-telecom-satellite`, `spec-uk-labour-tbi-influence`) **and** a credible CRQC path (US labs/Google/IBM; China). Even a months-long lead is decisive for long-lived secrets and identity credentials.
- **The verification double-bind:** you also can't **verify** a rival's capability — Google's own ZK proof of quantum cryptanalysis was **forged by Trail of Bits**, and supremacy results are repeatedly spoofed/contested. So neither does the attacker reveal **nor** can defenders confirm: the exact signal you'd use to trigger an emergency migration is the one that's suppressed, unreliable, *and* hype-saturated. **Double opacity.**
- **Conclusion:** **"we have until 2030/2035" is the most dangerous assumption in the whole quantum file.** The defender migrates on a *public* clock, the attacker exploits on a *private* one, the HNDL/TNFL loss is *already* accruing, and the trigger signal is unverifiable. The rational deadline is "as early as possible," not "by the published date" — yet essentially nothing is migrated. **The gap between the private real clock and the public deferred one is the window, and it's open now.**

## Card expiry, reissuance & the rural-equity problem *(added 2026-06-16)*
The most **concrete, sympathetic** version of the argument. Physical eID cards / ePassports bake their crypto (RSA/ECC keys + signatures) into the chip **at issuance** with multi-year validity — you can't generally OTA-swap a chip's signing *algorithm* — so the only migration path is **reissuance** (or remote re-keying). *Facts verified; the equity read labeled.*

- **The mechanism:** ICAO Doc 9303 Passive Authentication = RSA/ECDSA (Shor-breakable); smartcard upgrade cycles often **exceed a decade**, so the deployed base ages on classical crypto. Planned fix = hybrid/composite keys (classical + ML-DSA) **at reissuance**.
- **The kernel of goodness:** the normal **5–10-yr expiry cycle is itself the migration vehicle** — swap RSA→PQC at the renewal you'd do anyway. Expiry is the fix, not only the problem.
- **It already happened once (Estonia ROCA, 2017):** the Infineon **ROCA** flaw let attackers recover RSA private keys from public keys; Estonia found **~750,000–760,000** national eID cards affected (issued 2014–2017) and **suspended their certificates on 4 Nov 2017** — then fixed it by a **remote certificate update (Gemalto), not a physical reprint.** Proof that a deployed national ID's internal crypto can become a sudden mass liability — *and* that remote re-keying can substitute for reprinting (the template the cost argument leans on).
- **The rural-equity problem:** reissuance burden **and** residual vulnerability both concentrate on the **least-resourced** — rural populations renew slowest (distance to biometric-capture centres, thin connectivity, older cards), so they hold the **oldest, most quantum-fragile credentials longest**, and rural verifiers (border posts, clinics, banks) are slowest to update to *check* new PQC credentials. The digital-divide twin of the municipal-infrastructure burden above.

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
- **NIST:** RSA-2048/ECC deprecated **2030**, disallowed **2035**. Replacements **FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA)** finalized Aug 2024; **HQC** (code-based backup KEM) selected **Mar 11 2025** (draft 2026 / finalize ~2027); **FN-DSA (Falcon)** in process.
- **EU:** national strategies + crypto inventories by **end-2026**; critical financial infra PQC by **2030** (DORA/NIS2/PCI-DSS 4.0).
- **G7** (US Treasury + Bank of England) urging banks/insurers/exchanges; **Trump 2026 Cyber Strategy** mandates PQC. Hybrid (classical+PQC) dominates rollouts.

## The city / infrastructure layer
Sub-national action is mostly **research/industry clusters** (Chicago Quantum Exchange; **Illinois Quantum & Microelectronics Park**, PsiQuantum anchor ~$500M; Maryland "Capital of Quantum"; Colorado "Elevate Quantum") **plus** a migration **burden** landing on under-resourced **municipal critical infrastructure** (utilities, water, transit, hospitals, courts) that must inventory + migrate crypto before 2030. *Cities are exposed nodes, not yet coordinated actors.*

## What's really happening (synthesis)
Three things at once: **(1) a claims problem** — advantage assertions are contested and even Google's ZK proof was forged, so "how close is Q-Day" is hype-prone; **(2) a real, compressing CRQC threat** whose harvest-now-decrypt-later loss to today's secrets is **already locked in**; **(3) a geopolitical race** — China leads comms/sensing and outspends via a $138B vehicle, the US/EU/UK lead compute + drive the PQC migration (2027–2035 deadlines). For this repo: **separate the real (HNDL, programs, PQC mandates, IBM/Google/IonQ engineering) from the hype (800×-sales pure-plays, forged proofs, "Q-Day next year" marketing).**
