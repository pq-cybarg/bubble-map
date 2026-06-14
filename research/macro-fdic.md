# FDIC Aggregate US Banking Industry — what the data shows

*Narrative compiled 2026-06-06 from `macro-fdic.json` (FDIC BankFind financials API `https://api.fdic.gov/banks/financials`, cross-checked vs the published Quarterly Banking Profile). Validation: computed unrealized-securities figure matched FDIC's published QBP to within $0.2B (2026Q1: −$325.3B computed vs −$325.1B published).*

## 1. The unrealized securities-loss hole (the rate-shock overhang)
The industry still carries a large **negative AOCI / unrealized loss on securities** (AFS+HTM) from the 2022 rate shock — it has improved but **not healed**:

| Quarter | Unrealized securities loss |
|---|---|
| 2024Q1 | **−$517B** (peak of this window) |
| 2024Q4 | −$481B |
| 2025Q2 | −$396B |
| 2025Q4 | −$306B |
| **2026Q1** | **−$325B** (ticked back up) |

Three years after the SVB failure the system still sits on **~$325B of underwater securities** — a latent capital hole that re-widens whenever long rates rise. This is the channel through which *macro stress (rates) → bank capital* — and it interacts with everything below.

## 2. CRE: slow grind, not (yet) a break
- CRE loans roughly **flat at ~$2.34–2.39T** across the window (banks are not growing CRE; they're managing it down).
- **CRE noncurrent ratio crept from ~1.00% (2023Q4) to ~1.22–1.27%** — deterioration, but orderly at the aggregate. *(The pain is concentrated in office + specific regional banks, which the aggregate masks — see `macro-cre-privatecredit.md`: office CMBS delinquency hit a record 11.76%.)*
- Industry **reserve coverage fell from 202% (2023Q4) to 165% (2026Q1)** — banks are letting coverage erode as charge-offs normalize, leaving less cushion.
- **The CRE/Tier-1 tail (computed, `data/bank_exposure.json`, n=194):** the aggregate "flat CRE" hides a concentrated tail — **46 banks at total CRE/Tier-1 ≥ 300%, 6 ≥ 400%** (Metropolitan Commercial **575%**, Live Oak 491%, Simmons 461%, OceanFirst 432%, Provident 420%, Heritage 401%), almost all **regional/community** banks. >300% is the supervisory concentration flag; six banks carry CRE books ~4–6× their core capital — the names where a CRE markdown is solvency, not earnings.

## 3. Consolidation and failures (1999 → now)
- **Number of FDIC-insured institutions: 10,344 (1999) → 4,352 (2026Q1)** — a **~58% collapse** in the count of banks over 27 years. Concentration into the giants is structural.
- Failure spikes line up with crises: **148 (2009), 157 (2010)** post-GFC; a small **2023 cluster** (SVB/Signature/First Republic — $532B failed assets that year). 2024–2026: only ~2/yr, low.
- **Problem Bank List: ~52→68→54** banks over the window (manageable). **Note:** the FDIC *stopped publishing problem-bank asset totals in Feb 2025* — a transparency reduction worth flagging.

## 4. Deposits and the DIF
- Total deposits **$18.9T → $20.7T**; **uninsured deposits ~$8.4T (2026Q1)** — still a large run-prone base (the SVB failure mode).
- **DIF reserve ratio recovered to 1.43%** (2026Q1) from the post-2023 dip — the insurance fund is rebuilt.

## 5. Coverage gaps — what sits below reporting thresholds or outside FDIC data entirely
The FDIC aggregate is the *visible* layer; several pools of comparable risk are below threshold or out of scope, and are worth digging into separately:
- **The suppressed problem-bank *asset* total.** Since **Q4 2024 — the first time since 1990** — the FDIC publishes only the problem-bank **count**, not the **assets** (it cited the risk that disclosure could trigger a "disorderly run"). The size of the troubled set is now deliberately below disclosure; the per-bank reconstruction above partly recovers it.
- **Credit unions (NCUA, not FDIC).** A **parallel ~$2.3T system** under a different regulator (Call Report Form 5300), with its **own HTM/AFS unrealized losses, CRE and member-business-lending concentration, and CECL treatment** — entirely absent from FDIC data. Some large credit-union failures already occurred; their securities/CRE tail is uncovered here.
- **The small-bank long tail.** This dataset is the **top-194 by assets**; there are still **~4,352** FDIC institutions — the smallest thousands (community/de-novo) aren't pulled, and stress historically *starts* there.
- **Non-bank lenders / NDFIs / private credit / BDCs.** Outside FDIC entirely — the risk that *migrated off* bank balance sheets (bank loans to NDFIs ~$1.97T) lives here, only partly visible (BDCs via SEC; much private). See `macro-cre-privatecredit.md`.
- **Scope mismatches:** **bank-entity** data here vs **holding-company FR Y-9C** (off-balance-sheet at the holdco); **FHLB advances** (a public liquidity-stress signal, not in this set); **industrial loan companies (ILCs)**, the **Farm Credit System**, and **foreign-bank US branches** (separate/partial reporting).

> The honest read: the FDIC number is a floor on the *banking* slice of a larger pool. Credit unions and NDFIs are the two biggest uncovered reservoirs of the same HTM/CRE/duration risk; the suppressed problem-bank asset total is the deliberately-hidden distribution.

## Read for the bubble thesis
The banking system is **not in acute distress**, but it carries two slow-burn vulnerabilities that the AI-capex story plugs into: (1) a **$325B unrealized-loss sensitivity to rates** — and the AI buildout is issuing a wall of new corporate/datacenter debt that pressures long rates; (2) the real CRE/credit risk has **migrated off bank balance sheets into nonbanks/private credit** — which is exactly where AI-datacenter financing now lives (see `macro-cre-privatecredit.md`: bank loans to NDFIs ~$1.97T). The banks look clean partly because the risk moved to where the AI money is.
