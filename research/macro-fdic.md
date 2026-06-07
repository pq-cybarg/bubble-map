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

## 3. Consolidation and failures (1999 → now)
- **Number of FDIC-insured institutions: 10,344 (1999) → 4,352 (2026Q1)** — a **~58% collapse** in the count of banks over 27 years. Concentration into the giants is structural.
- Failure spikes line up with crises: **148 (2009), 157 (2010)** post-GFC; a small **2023 cluster** (SVB/Signature/First Republic — $532B failed assets that year). 2024–2026: only ~2/yr, low.
- **Problem Bank List: ~52→68→54** banks over the window (manageable). **Note:** the FDIC *stopped publishing problem-bank asset totals in Feb 2025* — a transparency reduction worth flagging.

## 4. Deposits and the DIF
- Total deposits **$18.9T → $20.7T**; **uninsured deposits ~$8.4T (2026Q1)** — still a large run-prone base (the SVB failure mode).
- **DIF reserve ratio recovered to 1.43%** (2026Q1) from the post-2023 dip — the insurance fund is rebuilt.

## Read for the bubble thesis
The banking system is **not in acute distress**, but it carries two slow-burn vulnerabilities that the AI-capex story plugs into: (1) a **$325B unrealized-loss sensitivity to rates** — and the AI buildout is issuing a wall of new corporate/datacenter debt that pressures long rates; (2) the real CRE/credit risk has **migrated off bank balance sheets into nonbanks/private credit** — which is exactly where AI-datacenter financing now lives (see `macro-cre-privatecredit.md`: bank loans to NDFIs ~$1.97T). The banks look clean partly because the risk moved to where the AI money is.
