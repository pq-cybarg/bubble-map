# Foreign-bank US branches (~$3T+) — the dollar-funding node, the yen carry, and the IHC gap

*Built 2026-06-15. Structured data + edges: `macro-foreign-bank-branches.json`. Deep companion to [[macro-uncovered-risk-pools]] §5. (WebFetch unavailable; aggregate totals are primary Fed series (solid); per-bank-by-country and the line-item split are weak — the Fed publishes aggregates, not a league table. The "$2T+" premise is outdated — actual ~$3.0-3.4T.)*

> US branches and agencies of foreign banks are a **~$3.0-3.4T** book — **not** FDIC-insured, funded through wholesale dollar markets and intra-firm "net due," **~87% concentrated in New York.** The sharpest live channel is **Japanese**: Japanese banks hold the largest US-resident claims of any banking system and fund US assets (Treasuries, CLOs, leveraged loans) **synthetically via yen/FX swaps** — so BoJ normalization drove the **Aug-5-2024 carry unwind** and **Norinchukin's ~$63B forced bond sale.** And the Dodd-Frank IHC ring-fence **EXCLUDES branches** — leaving the ~$3T book outside the US consolidated capital/liquidity regime.

## 1. Size & funding
- **~$3.04T** in US assets (Fed IBA, Sep 30 2024), **NY ~87% (~$2.64T)**; the broader "foreign-related institutions" H.8 series ~$3.39T (Mar 2026). The node has grown well past the commonly-cited "$2T+."
- **Funding fragility:** branches are **not FDIC-insured** and have no retail base — they fund via large-time/brokered deposits, fed funds/repo, and **"net due to related institutions"** (intra-firm parent funding). Confidence-sensitive and dollar-denominated. *(Exact cash/securities/loans/net-due split is weak — needs H.8 Table 10.)*

## 2. By country
- **Japanese banks dominate** — the largest US-resident claims of any banking system (BIS): MUFG, SMBC, Mizuho (MUFG sold Union Bank's CA retail to U.S. Bancorp in 2022, shifting toward wholesale/branch). **Canadian** (TD, RBC, BMO, Scotiabank) and **European** (Barclays, Deutsche, BNP, Credit Agricole, Santander) operate more via IHC-held subsidiaries; **Chinese** (ICBC, BoC, CCB) have a smaller NY footprint. *(Per-bank dollar sizes weak — Fed aggregates only.)*

## 3. The yen-carry channel (the live risk)
- **BoJ path:** out of negative rates Mar 2024 (−0.1%→0) → 0.25% (Jul 31 2024) → 0.5% (mid-2025) → **~0.75% (Dec 19 2025, a 30-year high; 10y JGB past 2%).** The Jul-2024 hike triggered the **Aug-5-2024 unwind**: Nikkei **−12.4%** (worst day since 1987), yen surged, yen-funded leveraged longs force-unwound.
- **Norinchukin:** announced (Jun 2024) it would sell **~¥10T (~$63B)** of US Treasuries + EU sovereigns (~⅙ of its global portfolio) to stem unrealized losses (~¥2.19T at Mar 2024); posted a **~$12.6B FY2024 net loss** and replaced its CEO. The concrete case of a Japanese institution force-selling Treasuries on the rate turn.
- **The channel:** Japanese banks run USD assets > USD liabilities, relying on **synthetic dollar funding (FX swaps / the cross-currency basis)** — off-balance-sheet forward dollar obligations not in standard debt stats (BIS/IMF flag this). Rising yen rates + a weaker basis raise their USD funding cost and pressure Treasury/CLO demand — a transmission line from BoJ policy to the US Treasury market.

## 4. Repo, Fed backstop & the IHC gap
- **IOR arbitrage:** FBOs account for the bulk of IORB arbitrage — not FDIC-insured, looser leverage rules, so they borrow cheaply (esp. from FHLBs) and park reserves at the Fed; marginal repo intermediaries.
- **Fed backstop:** dollar swap lines peaked **~$449B (May 2020; 82% BoJ + ECB)**; the **FIMA repo facility** (2020, standing since 2021) lets foreign central banks repo Treasuries for dollars — backstops for this same node.
- **The IHC gap:** Reg YY requires an FBO with ≥$50B in US **non-branch** assets to form a US Intermediate Holding Company (Basel III, CCAR, liquidity) — but the threshold counts non-branch assets only, so **branches and agencies are EXCLUDED** from the IHC and its consolidated regime. The ~$3T branch book sits **outside the US ring-fence.**

## Synthesis
A **~$3T**, NY-concentrated, FDIC-uninsured, wholesale-funded node **outside the Dodd-Frank IHC ring-fence.** The sharpest live risk is the **yen-carry/synthetic-dollar channel**: Japanese banks (the largest US claimants) fund Treasuries/CLOs via FX swaps, so BoJ normalization transmits straight to the US Treasury market (Aug-2024 unwind; Norinchukin's ~$63B sale). The offshore-dollar transmission line in the uncovered stack — and the reason the Fed's swap-line/FIMA backstops exist.

## What is NOT asserted
- No claim of current FBO distress — the point is the size (~$3T+, not $2T), wholesale-funding fragility, the yen-carry transmission, and the IHC exclusion of branches.
- Per-bank by-country sizes and the line-item split are weak (Fed aggregates only).
- Overlay edges are **excluded** from the proofs.

---
*Sources: [Fed — Assets & Liabilities of US Branches & Agencies of Foreign Banks (IBA)](https://www.federalreserve.gov/data/assetliab/current.htm); [FRED — foreign-related institutions assets](https://fred.stlouisfed.org/series/TLAFRIW027NBOG); [BIS CGFS — Japanese-bank US claims / FX-swap funding](https://www.bis.org/publ/cgfs65.pdf); [CNBC — BoJ Dec-2025 hike](https://www.cnbc.com/2025/12/19/bank-of-japan-boj-rate-cpi-inflation-takaichi-ueda.html); [CNBC — Aug-5-2024 Asia markets](https://www.cnbc.com/2024/08/05/asia-markets.html); [Bloomberg — Norinchukin $63B bond sale](https://www.bloomberg.com/news/articles/2024-06-18/norinchukin-bank-to-sell-63-billion-of-bonds-to-stem-losses); [NBER — 2020 swap-line usage](https://www.nber.org/system/files/working_papers/w29982/w29982.pdf); [Fed — FIMA repo facility](https://www.federalreserve.gov/newsevents/pressreleases/monetary20200729b.htm); [Cornell LII — 12 CFR 252.153 (IHC)](https://www.law.cornell.edu/cfr/text/12/252.153).*
