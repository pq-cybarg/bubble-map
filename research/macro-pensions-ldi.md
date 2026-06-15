# Pensions & LDI — the retirement balance sheet inside private markets

*Built 2026-06-14. Structured data + edges: `macro-pensions-ldi.json`. Companion to [[macro-uncovered-risk-pools]], [[macro-private-credit-marks]], and [[self_marked_value]].*

> Pension funds have migrated **~a third of the two largest US funds into manager-marked illiquids** and use leveraged liability-driven investing (LDI) that **already broke once** — the UK September 2022 gilt doom-loop.

## 1. The UK 2022 LDI doom loop — the live precedent
- The 23 Sep 2022 mini-budget spiked 30yr gilt yields ~120bp+; leveraged LDI funds posted gilts as collateral, so falling prices triggered **margin calls → forced gilt selling → higher yields → more calls** (the BoE's *"vicious spiral"*).
- UK DB liabilities hedged via LDI grew ~£400bn (2011) → **~£1.5T (2020)**, ~two-thirds of GDP. The BoE pledged up to £5bn/day (the **"£65bn" headline = the 13-day ceiling**) but **actually bought ~£19.3bn** — mostly an announcement effect.
- Margin calls **>£70bn**; forced LDI gilt sales **>£36bn** (23 Sep-14 Oct). Reform: leveraged LDI must hold a **≥250bp** yield-resilience buffer + operational buffer. A 2025 gilt sell-off re-tested it — wider buffers held.

## 2. US public pensions — ~a third in valuation-priced illiquids
- Funded ratio **~80% (2024) → ~82.5% (2025)**; unfunded **~$1.27T**. FY2025 returns averaged ~9.5% vs an assumed **~6.9%** — the improvement is return-driven, so it reverses in a drawdown.
- Alts rose **~11% (2006) → ~26% (2016) → ~34% (2022)** as public equity fell below 50%.
- **CalPERS (~$556B, Jun 2025):** PE ~17.7%, real assets ~13.1%, private debt ~3.8% (new private-credit target ~8%) → **~34% illiquid**. **CalSTRS (~$370B):** PE 15.1%, real estate 12.8% → **~28% illiquid**.

## 3. The denominator / self-marking problem
- Private-market values are **manager/valuation-priced, not market-priced** — the self-marked-value defect on the retirement balance sheet ([[self_marked_value]]). Stale marks lag public drawdowns, so **>50% of US plans were over-allocated to PE** in 2025 (S&P Global).
- H1-2025 secondaries: LP portfolios traded **~90% of NAV**, tail-end (>10yr) **below 75%**, distressed sellers 25%+ discounts (Jefferies) — direct evidence the marks **overstate realizable value**.

## 4. Corporate DB (opposite sign) & the drawdown
- Milliman 100 funded ratio **~108% (end-2025)** — corporate plans are *overfunded*, driving LDI de-risking and **pension risk transfer** (annuity buyouts that relocate liabilities onto life insurers, [[spec-insurance-bermuda]]). Do **not** conflate with underfunded public plans.
- Public plans run **net cash outflow ~1.7% of assets** (2024); mature plans pay benefits by selling assets — and you can't sell privates at NAV, so stress hits the **liquid sleeve** (or secondaries at a discount).

## Synthesis
Pensions are where leveraged rate-hedging (LDI, proven fragile in 2022) and manager-marked illiquids meet the household's retirement claim. The same ~91% common factor ([[macro-cross-sectional-analysis]]) that prices the bank HTM hole and private-credit NAVs also prices pension alts and gilt/Treasury LDI collateral — and the demographic outflow removes the buy-and-hold cushion.

## What is NOT asserted
- No claim US public pensions are insolvent (~82% funded) — the point is leverage + self-marked illiquids + net outflow.
- "£65bn" is the BoE *ceiling*; actual purchases ~£19.3bn.
- Corporate DB (~108%) and public DB (~82%) cut opposite directions — not conflated.
- Forced-selling-in-stress is graded *weak* (analytical), not a realized loss.
- Overlay edges are **excluded** from the proofs.

---
*Sources: [Bank of England — gilt market operation](https://www.bankofengland.co.uk/news/2022/september/bank-of-england-announces-gilt-market-operation); [SUERF — UK LDI lessons](https://www.suerf.org/publications/suerf-policy-notes-and-briefs/putting-out-the-nbfire-lessons-from-the-uks-liability-driven-investment-crisis/); [TPR — LDI guidance](https://www.thepensionsregulator.gov.uk/en/media-hub/press-releases/2023-press-releases/new-ldi-guidance-published-by-tpr--to-ensure-schemes-minimise-risk); [Equable — State of Pensions 2025](https://equable.org/state-of-pensions-2025/); [Pew — pension investment risk](https://www.pew.org/en/research-and-analysis/issue-briefs/2025/04/increased-risk-complex-investment-landscape-require-prudent-pension-management-practices); [CalPERS facts](https://www.calpers.ca.gov/documents/facts-investments/download); [CalSTRS portfolio](http://www.calstrs.com/investment-portfolio); [Milliman PFI Jan 2026](https://www.milliman.com/en/insight/pension-funding-index-january-2026); [PBGC FY2024](https://www.pbgc.gov/news/press/releases/pr24-040); [S&P — pensions over PE target](https://www.spglobal.com/market-intelligence/en/news-insights/articles/2025/5/more-than-half-of-pension-funds-exceed-private-equity-allocation-targets-89164143); [Jefferies — H1-2025 secondaries](https://www.jefferies.com/wp-content/uploads/sites/4/2025/08/Jefferies-Global-Secondary-Market-Review-July-2025.pdf).*
