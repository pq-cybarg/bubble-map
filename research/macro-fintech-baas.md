# Fintech, BaaS & neobanks — the Synapse collapse and the "FDIC-insured" ledger trap

*Built 2026-06-14. Structured data + edges: `macro-fintech-baas.json`. Companion to [[macro-uncovered-risk-pools]] and [[macro-bank-htm-marks]].*

> Most neobanks are **not banks** — they ride a handful of small sponsor banks through middleware that keeps the sub-ledger of who owns what. When **Synapse** failed (2024), **~100,000+ customers were frozen and ~$85-96M went missing** despite "FDIC-insured" marketing, because pass-through insurance covers **bank failure, not a ledger collapse**.

## 1. The Synapse collapse
- **The model:** Synapse (Chapter 11, April 2024) sat between fintech apps (Yotta, Juno, Copper) and partner banks (Evolve, AMG, American, Lineage), routing money into pooled **"for-benefit-of" (FBO) accounts** while keeping the per-customer sub-ledger itself.
- **The shortfall:** >100,000 customers frozen from May 2024; users owed **~$265M** but partner banks held only **~$180M** — a shortfall first reported at **~$85M** (trustee **Jelena McWilliams**, former FDIC Chair, June 2024), later **"up to ~$95M."** Evolve had moved **>$300M** of balances to other banks while severing the relationship — a reconciliation rupture.
- **Unrecoverable:** the trustee — *with subpoena power* — still could not find the money; the case was **dismissed Nov 2025**, estate administratively insolvent.

## 2. The "FDIC-insured" gap
- Pass-through FDIC insurance covers **bank failure only** — not middleware/ledger failure — and requires beneficial-owner records (which Synapse lacked). **No partner bank failed, so insurance never triggered.**
- **Rulemaking:** FDIC amended Part 328 (false-advertising/misrepresentation; compliance Jan 2025) and proposed **"Recordkeeping for Custodial Accounts"** (Oct 2024) — but **no final custodial rule** as of mid-2026. OCC/Fed/FDIC issued a July-2024 joint statement warning third-party arrangements can mislead on FDIC coverage.
- **Partial bailout:** the CFPB allocated **~$46.2M** from its Civil Penalty Fund to victims (Nov 2025) — roughly half the frozen amount, the first-ever fintech "bailout" via the CPF.

## 3. The sponsor-bank consent-order wave
- **≥8 BaaS sponsor banks** hit with FDIC/OCC/Fed orders in 2024: **Evolve** (Fed C&D, June 2024), **Cross River** (2023), **Blue Ridge** (OCC "troubled condition," 2024 — exited BaaS, **displacing ~70 fintech partners**), Lineage, Piermont, Sutton (Feb 2024), Thread (May 2024). BaaS banks were ~18% of FDIC enforcement actions since Jan 2024.
- **Concentration:** one sponsor bank often supports hundreds of fintech programs; a single order or exit cascades to millions of end users.

## 4. Neobank scale — apps on top of banks
- **Chime** (>8.6M members; IPO June 2025, ~$864M) holds deposits at The Bancorp Bank and Stride. **Cash App** (~57M users) uses Sutton / Wells Fargo pass-through. **Dave** rides a sponsor bank (FTC sued Nov 2024). **Varo** is the **only** neobank with its own OCC charter — and its deposits (~$300M) and losses are deteriorating.
- **2025 repeat:** **Solid Financial Technologies** (BaaS middleware, >100 programs) filed Chapter 11 in April 2025 — the Synapse pattern again, a year later.

## Synthesis
BaaS turned "FDIC-insured" into a marketing claim conditional on accurate beneficial-owner records and a solvent middleware — neither guaranteed. Tech-mediated balances flow across pooled FBO accounts at several small sponsor banks via a private sub-ledger; severing one relationship can break reconciliation system-wide, and a former-FDIC-Chair trustee still couldn't find the money. The same **trust-the-ledger defect** this project documents in self-marked balance sheets appears here as **literal missing deposits**.

## What is NOT asserted
- No claim pass-through insurance is invalid — it works when a *bank* fails and records are accurate; the gap is middleware/ledger failure.
- The shortfall is ~$85-96M (a range that grew); the custodial-recordkeeping rule was **not** finalized as of mid-2026.
- Choice Bank / First Fed could not be confirmed with 2023-25 BaaS orders; the confirmed set is Cross River, Blue Ridge, Lineage, Piermont, Sutton, Thread, Evolve.
- Overlay edges are **excluded** from the proofs.

---
*Sources: [CNBC — trustee: $85M missing](https://www.cnbc.com/2024/06/07/synapse-bankruptcy-trustee-85-million-of-customer-savings-is-missing.html); [Banking Dive — shortfall](https://www.bankingdive.com/news/synapse-85-million-shortfall-partner-banks-mcwilliams/718796/); [Bloomberg Law — case dismissed](https://news.bloomberglaw.com/bankruptcy-law/synapse-bankruptcy-dismissed-after-fintechs-failed-sale-effort); [Fed — Evolve C&D](https://www.federalreserve.gov/newsevents/pressreleases/enforcement20240614a.htm); [FDIC — custodial recordkeeping NPR](https://www.fdic.gov/news/press-releases/2024/fdic-proposes-deposit-insurance-recordkeeping-rule-banks-third-party); [Interagency RFI on bank-fintech arrangements](https://www.federalregister.gov/documents/2024/07/31/2024-16838/request-for-information-on-bank-fintech-arrangements-involving-banking-products-and-services); [American Banker — CFPB $46M refund](https://www.americanbanker.com/news/cfpb-to-refund-46-million-to-synapse-victims); [SEC — Chime S-1](https://www.sec.gov/Archives/edgar/data/0001795586/000162828025025059/exhibit1021-sx1.htm); [FintechFutures — Solid Chapter 11](https://www.fintechfutures.com/baas/baas-fintech-solid-files-for-chapter-11-bankruptcy-protection).*
