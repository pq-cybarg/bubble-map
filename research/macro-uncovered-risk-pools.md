# Below-threshold & out-of-scope risk pools — what the FDIC bank lens misses

*Built 2026-06-14. Sources: NCUA Quarterly Data Summaries + press (2025) & Ceto (CU failures); Fed FEDS note / NY Fed / Morgan Stanley / With Intelligence (private credit & BDCs); CRS R46489 + ICBA (ILCs); Farm Credit Funding / FCS results; Federal Reserve IBA release (foreign-bank branches); Wolf Street (FDIC problem-bank suppression). Full URLs at the bottom.*

> The FDIC bank aggregate is **one slice** of US credit. This maps the comparable HTM / CRE / duration / credit risk that sits **outside or below** that lens — a different regulator, a smaller size cut, or no public disclosure at all — so "banks look clean" isn't mistaken for "the system is clean." Companion to [[macro-fdic]] §5 and [[macro-bank-htm-marks]].

## 1. Credit unions (NCUA — a ~$2.43T parallel system, different regulator)
- **Size & capital:** federally-insured CUs held **~$2.43T** at Q4 2025 (+$126B / +5.4% YoY); aggregate **net-worth ratio ~11.26%** — well-capitalized in aggregate.
- **Rising stress:** delinquency **91bp (Q2) → 95bp (Q3) → 103bp (Q4)**, up ~5bp YoY; CRE/non-commercial-RE delinquency **~88bp** (+10bp YoY).
- **Failure cluster:** **6 credit-union failures Apr–Aug 2025 — the largest cluster in ~7 years**, ending a near-two-year no-liquidation stretch; all small (largest ~$58.5M), weak profitability + credit + governance.
- **Why it's a blind spot:** CUs file **NCUA Form 5300** (not FDIC), carry their **own HTM/AFS unrealized losses and CRE/member-business-lending concentration**, CECL-covered — none of it in the FDIC aggregate the bubble thesis usually cites.

## 2. Private credit / NDFIs (the biggest uncovered reservoir)
The risk that **migrated off bank balance sheets** — and where AI-datacenter financing now lives.
- **Size:** US private credit **~$1.7T** (some scopes $2.3–3T), projected **~$5T by 2029** (Morgan Stanley) — ~5× since 2009.
- **Vehicles:** **BDCs ~$500B**; private-wealth vehicles (BDC/interval/tender) >$400B; **evergreen funds ~$644B** (Jun 2025, +28% H1) — **manager-set NAVs**, the third self-marked number ([[macro-private-credit-marks]]).
- **Bank linkage:** banks lend to NDFIs **~$1.97T** (Fed) — bank risk didn't vanish, it moved one step out and turned opaque ([[macro-cre-privatecredit]]).

## 3. Industrial loan companies (FDIC-insured, Fed-*un*supervised)
- **Size:** total ILC assets **~$247.7B** (2025), up from ~$25.1B (1997); **~23 active charters**, 6 over $10B, **largest ~$116.3B**.
- **The loophole:** ILCs are **FDIC-insured yet their commercial parents escape Fed consolidated (BHC) supervision** — the basis of the ICBA "close the loophole" campaign and of fintech (Square et al.) and retail/auto interest in the charter.

## 4. Farm Credit System (a federal GSE off the FDIC map)
- A GSE lending complex (funded via the Federal Farm Credit Banks Funding Corp) holding roughly **~$188B farm real-estate + ~$81B non-RE farm loans** at YE2024 — a **~$400B+ asset** GSE.
- **Exposure:** concentrated in **farmland values and ag commodity cycles**; a farmland correction or trade-war ag shock is its tail — distinct from the bank/CRE map.

## 5. Foreign-bank US branches (a ~$2T+ dollar-funding node)
- US **branches/agencies of foreign banks** hold **~$2T+** in US assets (Fed **IBA** release), heavily in **wholesale dollar funding and repo** — a transmission node for offshore-dollar stress, outside the FDIC domestic-bank set.

## 6. The suppressed problem-bank total (hidden even within FDIC scope)
- Since **Q4 2024 — the first time since 1990** — the FDIC publishes only the problem-bank **count** (~54), not the **asset total**, citing the risk of a "disorderly run." The distribution is deliberately below disclosure; the per-bank reconstruction in [[macro-bank-htm-marks]] partly recovers it.

## Synthesis — the FDIC bank number is a floor, not the system
Stack the pools beyond the FDIC bank aggregate: **~$2.43T credit unions** (rising delinquency + a 7-yr-high failure cluster), **~$1.7–3T private credit/NDFIs** (manager-marked, AI-datacenter-heavy), **~$248B ILCs** (insured-but-unsupervised), a **~$400B+ Farm Credit GSE**, and **~$2T+ foreign-bank US branches** — each with its own HTM/CRE/duration/credit risk, mostly outside the lens "banks look clean" relies on. The **same ~91% common factor** ([[macro-cross-sectional-analysis]]) that prices the bank HTM hole also prices credit-union securities, private-credit NAVs, and farmland — so "the banks are fine" understates a **correlated, larger pool.** Credit unions and private credit are the two biggest, and both show rising stress now.

## What is NOT asserted
- No claim any pool is insolvent system-wide — CUs and the FCS are well-capitalized in aggregate; the point is they're **uncovered** by the FDIC lens and carry **correlated** risk.
- Private-credit size is **scope-dependent ($1.7T–$3T)** — a range, not false precision.
- The ILC "loophole" is a **documented policy debate**, not an allegation against any ILC.
- FBO/FCS exact totals live in their primary releases; figures here are as-reported approximations.
- Overlay edges are **excluded from the SCC / Z3 / TLA+ proofs**.

---
*Sources: [NCUA — Q4 2025 system performance](https://ncua.gov/newsroom/press-release/2026/ncua-releases-fourth-quarter-2025-credit-union-system-performance-data), [Ceto — credit-union failures hit a 7-year high in 2025](https://www.ceto.com/blog/credit-union-failures-in-2025), [Fed FEDS — bank lending to private credit](https://www.federalreserve.gov/econres/notes/feds-notes/bank-lending-to-private-credit-size-characteristics-and-financial-stability-implications-20250523.html), [Morgan Stanley — private credit to ~$5T by 2029](https://www.morganstanley.com/ideas/private-credit-outlook-considerations), [CRS R46489 — Industrial Loan Companies](https://www.congress.gov/crs-product/R46489), [Farm Credit Funding — earnings/investor materials](https://www.farmcreditfunding.com/ffcb_live/current/InvestorPresentation.pdf), [Federal Reserve — Assets & Liabilities of US Branches & Agencies of Foreign Banks (IBA)](https://www.federalreserve.gov/data/assetliab/current.htm), [Wolf Street — FDIC ends disclosing problem-bank assets](https://wolfstreet.com/2025/02/26/fdic-ends-disclosing-total-assets-of-banks-on-problem-bank-list-as-disclosure-might-suddenly-trigger-a-disorderly-run/).*
