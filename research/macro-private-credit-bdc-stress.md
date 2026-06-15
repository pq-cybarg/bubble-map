# Private credit / BDC stress signals — the public-price vs private-mark gap

*Built 2026-06-15. Structured data + edges: `macro-private-credit-bdc-stress.json`. Deep companion to [[macro-private-credit-marks]] and [[macro-cre-privatecredit]]; the third self-marked number in [[self_marked_value]]. (WebFetch unavailable; figures from search surfacing of the cited sources. Both directions are live — Moody's/KBRA argue marks may OVERstate stress — so the thesis is graded contested.)*

> The tells that the manager-set NAVs are too high: **listed BDCs trade ~20% below NAV while non-traded BDCs hold marks near par**; PIK income is ~12% and rising; defaults climb (Fitch 5.8%) even as reported non-accruals stay optically low (impaired loans get *restructured with PIK*, not marked); the same loan is marked **9 points apart** by two lenders; and retail money is being **gated in** just as redemptions spike.

## 1. Discount-to-NAV — the market voting against the marks
- Listed BDCs trade at **~20% average discount to NAV** (2025-26), some near ~50%: Blue Owl (OBDC) ~21% ($11.77 vs NAV $14.89, Sept 2025); FS Specialty ~27%; Barings ~23%; even Ares Capital (ARCC) slipped to a slight discount. **Non-traded BDCs hold valuations near par** — the core public-price/private-mark gap.
- **Cross-lender gap:** Medallia — **HPS marked the loan 69¢ (Feb 2026); Blackstone marked the SAME credit 77.75¢ (Dec 2025)** — a ~9-point gap on one loan. A recurring pattern: a senior loan deeply discounted while a second (often PIK) loan to the same borrower is held at par.

## 2. Managers & PIK
- **Largest vehicles:** BCRED (Blackstone) is the largest BDC of any kind — **$82.2B investments / $47.6B NAV** (Dec 2025), perpetual non-traded; ARCC (Ares) the largest *listed* (~$30.7B); OBDC (Blue Owl) #2; OCIC (Blue Owl) ~$36B; HLEND (HPS); GCRED (Golub ~$8.6B). Ares firm AUM $644.3B.
- **PIK + defaults:** PIK was **~11.7%** of BDC loans (Q2 2024) and rising — a marks-quality red flag (BDCs must distribute 90% of income whether cash or PIK: "covered, not collected"). **Fitch private-credit default rate 5.8%** (Jan 2026); **~65% of 2025 defaults were distressed restructurings, 7 of 11 introduced PIK** in lieu of cash. Reported non-accruals stay <~1.5% *precisely because* impaired loans get restructured with PIK rather than marked non-accrual.

## 3. The bank-to-NDFI chain
- Banks held **~$1.32T funded NDFI loans** (FDIC, Q3 2025) **+ ~$987B unfunded commitments (~$2.3T)**; the segment grew **~50% in 2024-25** (vs ~4% for total bank loans). JPMorgan ~$50B, Wells Fargo ~$36-85B (to funds), Citi ~$22B. The Fed flags the shift toward **credit LINES** as raising liquidity-call interconnection. *(The "$1.97T" figure sits between funded-only and funded-plus-commitments.)*

## 4. Retail access & the gates firing
- **EO 14330** (Aug 7 2025) eases PE/private-credit into 401(k)s (DOL rule advancing Apr 2026). The **evergreen/interval universe is ~$431-500B** — *not* the ~$644B sometimes cited (that's Ares firm AUM).
- **Mismatch:** evergreen funds cap redemptions at ~5%/quarter while a target-date fund trades daily. In **Q1 2026 the gates fired**: Blue Owl OTIC (tech, $6.2B) redemption requests **40.7%**, OCIC ($36B) 21.9%, OBDC II 17% (→ wind-down); the firm filled only ~5%. Cliffwater CCLFX ($33B) **~14%** (record). Private credit's first real liquidity test.

## 5. Stress events vs the bull case
- **First Brands** (Ch.11, Sept 2025): 15 BDCs hold ~$237M (~0.05% of ~$503B BDC AUM) — small direct hit, but UBS ~$500M / Jefferies ~$715M exposed via factoring/funds ([[macro-consumer-abs-subprime]]). **Tricolor** was bank-financed, little BDC exposure.
- **The honest other side:** Moody's (June 2026) and KBRA (Q1 2026) argue marks may **OVERstate** stress and non-accruals stay low; Lincoln is launching monthly valuation indices. The "marks are too high" thesis is **contested**, not fact.

## Synthesis
Private credit is the **third self-marked number** ([[self_marked_value]]): the listed-BDC discount is the market pricing the same loans ~20% below where managers carry them; PIK + restructure-don't-mark keeps non-accruals low; retail money is gated in; and the exposure runs back to the GSIBs via ~$2.3T of loans+lines. Whether that is over- or under-stated stress is genuinely contested — but the **gap between the public vote and the private mark** is the signal the corpus has argued all along.

## What is NOT asserted
- No claim private credit is in crisis — non-accruals low; Moody's/KBRA argue marks may overstate stress.
- The ~20% sector-average discount and the general cross-lender pattern are contested; named cases (OBDC, Medallia, Blue Owl gates) are fact.
- Bank NDFI exposure ~$1.32T funded / ~$2.3T with commitments (definition-dependent); the ~$644B "evergreen" is Ares firm AUM.
- Overlay edges are **excluded** from the proofs.

---
*Sources: [Octus — BDCs at discounts / non-accruals](https://octus.com/resources/blog/bdcs-trading-at-50-discount-to-nav-but-nonaccruals-ticking-downward/); [Mercer — public prices, private marks](https://mercercapital.com/insights/posts/2026/public-prices-private-marks-what-bdc-discounts-are-signaling/); [InvestmentNews — BDC discounts](https://www.investmentnews.com/alternatives/rejiggered-bdcs-trading-at-sharp-discounts/263115); [Benzinga — PIK "covered not collected"](https://www.benzinga.com/Opinion/26/06/53065817/covered-not-collected-pik-income-and-the-q1-2026-bdc-distribution-stack); [Funds Society — Fitch PCDR 5.8%](https://www.fundssociety.com/en/news/alternatives/u-s-private-credit-default-rate-continues-to-climb/); [FDIC — bank lending to NDFIs](https://www.fdic.gov/analysis/bank-lending-nondepository-financial-institutions.pdf); [FA-Mag — banks tally $100B+ private-credit loans](https://www.fa-mag.com/news/banks-tally--100-billion-of-private-credit-loans-as-calm-urged-86633.html); [White House — EO 14330](https://www.whitehouse.gov/presidential-actions/2025/08/democratizing-access-to-alternative-assets-for-401k-investors/); [Dakota — evergreen markets](https://www.dakota.com/reports-blog/top-10-evergreen-fund-markets-brief); [CNBC — Blue Owl redemptions](https://www.cnbc.com/2026/04/02/blue-owl-private-credit-funds-redemptions-requests.html); [Octus — Medallia marks gap](https://octus.com/resources/articles/medallia-advised-by-kirkland-ellis-lenders-working-with-latham-watkins-for-debt-for-equity-swap-deal/).*
