# Consumer & auto ABS & subprime — the household-credit tail, and the collateral-fraud failure mode

*Built 2026-06-14. Structured data + edges: `macro-consumer-abs-subprime.json`. Companion to [[macro-uncovered-risk-pools]] and [[macro-cre-privatecredit]].*

> Household debt hit **~$18.8T** (Q1 2026) with a benign 4.8% aggregate delinquency that masks a stressed subprime tail: **subprime auto 60+ delinquency at a 32-year high (6.74%)**, repossessions at 2009 levels, student-loan delinquency re-priced from ~0 to 7.7%+, and **~$400B of invisible BNPL "phantom debt."** Tricolor and First Brands (both 2025) showed the failure mode is **collateral fraud in the funding chain**, not just borrower default.

## 1. Tricolor & First Brands — collateral double-pledged across financiers
- **Tricolor:** subprime auto lender (Chapter 7 ~Sept 2025) amid *"systemic levels of fraud."* DOJ (Dec 2025) charged execs with a *"continuing financial crimes enterprise,"* allegedly **double-pledging collateral** (the trustee's review found **~$548M double-pledged across ~31,000 loans**; the broader alleged fraud is larger) with duplicate VINs and falsified loan tapes. **JPMorgan took a ~$170M writedown** (Q3 2025); Fifth Third flagged ~$200M; Barclays exposed.
- **First Brands:** auto-parts supplier (Chapter 11, Sept 28, 2025): ~$5B sales, >$9B liabilities, $12M cash. **~$2.5B of invoices unmatched to real sales** (fabricated/double-pledged receivables); DOJ-SDNY charges; ex-CFO pleaded guilty (Mar 2026).
- **What they revealed:** the ABS and factoring chains relied on **trust in self-reported loan tapes/invoices**; the same collateral pledged across multiple warehouse lines/factors went undetected — a verification failure at the **funding layer**, the same trust-the-self-report defect this project tracks in marks.

## 2. Auto stress — the canary
- Total auto debt **~$1.69T** (Q1 2026). **Subprime auto 60+ delinquency 6.74%** (Dec 2025, Fitch) — a 32-year high. ~**1.73M repossessions** in 2024 (Cox) — highest since 2009; 2025 projected >3M (*weak* projection); 2024 default rate 3.13% (highest since 2011).

## 3. Cards, BNPL, student loans — the K-shaped consumer
- **Cards ~$1.25T**; flow into serious delinquency ~7.04% (Q1 2025), early-transition ~8.6% (Q1 2026) — elevated but plateauing; stress concentrated in subprime.
- **BNPL:** US GMV ~$122B (2025); **~$400B of balances largely invisible to bureaus** (phantom debt); 47% of users reported a late payment (Mar 2026, up from 41%); ~8% used BNPL for groceries. Affirm 30+ delinquency ~2.8%; Klarna trades below its Sept-2025 IPO price with rising losses.
- **Student loans ~$1.66T:** the on-ramp ended Sept 2024, bureau reporting resumed Feb 2025 → **90+ delinquency jumped to ~7.74%** (Q1 2025) from <1%; >2.2M borrowers' scores fell >100 points; the national average fell ~717→715, the sharpest drop since the Great Recession.

## 4. The ABS chain
- Total US ABS **~$358B YTD 2025** (+16.8%, auto-driven, record); auto ABS ~$127B. Subprime auto + unsecured consumer credit is originated, warehoused by banks (JPMorgan, Fifth Third, Barclays), then securitized off balance sheet into ABS bought by asset managers/insurers — banks retain **warehouse-line tail risk** (the Tricolor channel).

## Synthesis
Household debt is at a record $18.8T with a placid 4.8% aggregate delinquency — but the tail is at multi-decade highs and ~$400B of leverage is invisible. Tricolor/First Brands show the acute failure mode is **collateral fraud in the funding chain** — the same "trust the self-reported number" defect that runs through the bank-HTM, private-credit-NAV, and pension-mark threads. The off-balance-sheet ABS chain disperses the loss while hiding collateral quality.

## What is NOT asserted
- No claim of system-wide household-credit insolvency — aggregate delinquency is benign; the point is a stressed, partly-invisible tail + a collateral-fraud failure mode.
- BNPL "~$400B phantom debt" and "47% late" rest on survey/secondary sources (contested); ">3M 2025 repossessions" is a projection (weak).
- Tricolor's double-pledge (~$548M per the trustee) is distinct from JPMorgan's ~$170M writedown; Fifth Third's ~$200M is potential, not finalized.
- Overlay edges are **excluded** from the proofs.

---
*Sources: [NY Fed — Household Debt & Credit Q1 2026](https://www.newyorkfed.org/newsevents/news/research/2026/20260512); [CNBC — Tricolor charges](https://www.cnbc.com/2025/12/17/tricolor-execs-charged-with-systematic-fraud-after-subprime-auto-lender-roiled-banking-sector.html); [DOJ-SDNY — First Brands](https://www.justice.gov/usao-sdny/pr/first-brands-executives-charged-multibillion-dollar-fraud); [Auto Finance News — subprime 60+ at 32-yr high](https://www.autofinancenews.net/allposts/risk-management/60-plus-day-subprime-auto-dqs-hit-32-year-high/); [Carscoops — repossessions at 2009 levels](https://www.carscoops.com/2025/03/car-repossessions-return-to-great-recession-levels-just-in-time-for-another-one/); [Affirm fiscal Q3 filing](https://www.sec.gov/Archives/edgar/data/0001820953/000182095325000050/affirmfq325designedshare.htm); [CFPB — BNPL market report](https://files.consumerfinance.gov/f/documents/cfpb_bnpl-market-report_2025-12.pdf); [NY Fed — Q1 2025 student-loan spike](https://www.newyorkfed.org/newsevents/news/research/2025/20250513); [Asset Securitization Report — unsecured consumer ABS records](https://asreport.americanbanker.com/news/unsecured-consumer-loan-abs-issuance-sets-records-in-2025).*
