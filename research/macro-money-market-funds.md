# Money market funds (~$7.9T) — the constant-NAV run vehicle the bank lens misses

*Built 2026-06-14. Structured data + edges: `macro-money-market-funds.json`. Companion to [[macro-uncovered-risk-pools]] and [[macro-stablecoin-failures-manipulation]].*

> Money market funds are a **~$7.9T cash pool outside the FDIC bank lens** that dominate repo and the Treasury-bill market and run by **redemption, not credit** — the institutional analogue of stablecoins (constant-value, redeemable-at-par, T-bill-backed, no FDIC).

## 1. Size & composition — *fact (ICI)*
- **~$7.87T** total (week of June 10, 2026) — a record; up from ~$7.0T (Mar 2025) and ~$4.5T at the 2022 rate-hike start. The pool roughly **doubled in four years**.
- Split: **government ~$6.5T (~82%)**, prime ~$1.23T (~16%; institutional prime only ~$241B), tax-exempt ~$145B (~2%). The **largest segment is the least reform-constrained**.
- Retail ~$3.10T; institutional ~$4.78T — the institutional tranche is the faster-moving, more run-prone cash.

## 2. The reforms shifted risk, didn't remove it
- **2014** (effective 2016): institutional prime floats its NAV → **~$1T+ migrated** prime → government.
- **2023**: removed gates; added a mandatory liquidity fee when daily net redemptions exceed 5% of NAV; raised liquidity minimums (25% daily / 50% weekly).
- **Residual:** government MMFs (~82%) keep a stable $1.00 NAV with **no fees/gates** — and government-fund redemptions, not credit, were the March-2020 channel.

## 3. The run mechanism is proven — twice, each backstopped
- **2008:** the $62.6B Reserve Primary Fund broke the buck (NAV $0.97) on $785M of Lehman paper; >$40B redeemed in two days; Treasury guaranteed MMFs via the ~$50B ESF.
- **March 2020:** prime MMFs lost ~$125B (~11%) in <3 weeks — a pure liquidity run, no default. The Fed's **MMLF** drew ~$53B and stopped it.

## 4. Repo & Treasury plumbing — the shock-absorber is gone
- The Fed's **ON-RRP peaked >$2.5T (Dec 2022)** and **drained to ~$22B (early Sept 2025)** — the excess-liquidity buffer is exhausted.
- MMFs hold **~40% of outstanding T-bills** (largest marginal buyer) into a deficit-driven supply surge (net bill issuance ~$475B Q3-2025, ~$416B Q1-2026).
- **2025-26 stress:** Dec 31, 2025 repo prints ~4.0%; the **Standing Repo Facility was tapped ~$74.6B** (highest since COVID) before reversing to ~zero by Jan 2026. QT ended Dec 2025; the Fed began reserve-management T-bill purchases — the first real test of post-RRP-drain plumbing.

## 5. The stablecoin analogy — same collateral, weaker backstop
- Major fiat stablecoins are **T-bill/repo-backed, redeemable at par, run-prone, with no FDIC and no stable-NAV legal backstop** — a constant-NAV money fund without Rule 2a-7 protections. USDC depegged to ~$0.87 (Mar 2023) on SVB fears.
- The **GENIUS Act** (July 2025) requires ≥1:1 reserves in cash/T-bills/T-bill repo/government MMFs but exempts issuers from bank capital and gives holders no FDIC coverage. Issuers bought **~$109B of T-bills (2025)** — putting stablecoins and MMFs into the **same bill/repo collateral pool**, so a run in either forces the same fire-sale.

## Synthesis
At ~$7.9T, MMFs are the **single biggest non-bank cash pool**, the dominant repo lender, and the largest marginal T-bill holder — with the RRP cushion gone. The same long-rate move that re-opens the bank HTM hole ([[macro-bank-htm-marks]]) drives MMF *and* stablecoin redemptions into one shared bill/repo market.

## What is NOT asserted
- No MMF is currently breaking the buck — the point is structural run-proneness + a drained RRP cushion.
- The ~40% T-bill share and ~$109B stablecoin figure are widely cited but approximate (contested); exact shares live in OFR/Fed data.
- The stablecoin-MMF link is a structural analogy + shared-collateral channel, not a legal equivalence.
- Overlay edges are **excluded** from the SCC / Z3 / TLA+ proofs.

---
*Sources: [ICI money-market-fund assets](https://www.ici.org/research/stats/mmf); [SEC 2014 reform](https://www.sec.gov/newsroom/press-releases/2014-143) & [2023 reform](https://www.sec.gov/newsroom/press-releases/2023-129); [Reserve Primary Fund](https://en.wikipedia.org/wiki/Reserve_Primary_Fund); [Fed FEDS — prime-MMF behavior](https://www.federalreserve.gov/econres/notes/feds-notes/investor-base-and-prime-money-market-fund-behavior-20220419.html); [Boston Fed — MMLF](https://www.bostonfed.org/publications/risk-and-policy-analysis/2021/the-money-market-mutual-fund-liquidity-facility.aspx); [FRED — ON RRP](https://fred.stlouisfed.org/series/RRPONTTLD); [Treasury refunding / bill supply](https://www.pgpf.org/article/news-from-the-quarterly-treasury-refunding-statement/); [GENIUS Act text](https://www.congress.gov/bill/119th-congress/senate-bill/394/text); [Brookings — stablecoins](https://www.brookings.edu/articles/next-steps-for-genius-payment-stablecoins/); [Wolf Street — year-end SRF](https://wolfstreet.com/2026/01/05/feds-standing-repo-facility-srf-drops-to-zero-from-75-billion-on-the-last-balance-sheet-as-yearend-liquidity-turmoil-dissolves/).*
