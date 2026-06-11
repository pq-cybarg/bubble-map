# The AI Neocloud + Stargate Debt & Capacity-Commitment Circularity

**Forensic credit map — CoreWeave (CRWV), Oracle (ORCL), Stargate JV, and the neocloud complex.**
Prepared 2026-06-05. Every figure is cited inline. Where a figure is a third-party estimate, a press leak, or a non-binding "letter of intent," it is flagged explicitly.

---

## Executive thesis

The AI buildout is being financed disproportionately by **debt and capacity commitments**, not by cash flow or equity. Morgan Stanley estimates ~$3T of hyperscaler/data-center capex through 2028, with internal cash funding only ~half and a **~$1.5T financing gap** to be filled by credit markets ([Energynow/Bloomberg](https://energynow.com/2026/02/the-3-trillion-ai-data-center-build-out-becomes-all-consuming-for-debt-markets/)). The collateral is GPUs, whose useful life Moody's pegs at **4-6 years** versus 10-15 year leases — an asset/liability duration mismatch ([Yahoo/Moody's](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html)).

The keystone circular structure: **NVIDIA invests equity in / backstops neoclouds → neoclouds borrow against the GPUs they buy from NVIDIA → they sell that capacity to OpenAI → NVIDIA separately funds OpenAI**, which also commits ~$300B to Oracle, which is itself debt-financing the chips it rents at ~14% gross margin. The same dollar of NVIDIA capital and the same GPU appear as revenue, collateral, and demand at multiple nodes.

---

## 1. CoreWeave (CRWV)

### IPO (March 2025)
- Priced **37.5M Class A shares at $40.00** on 2025-03-27 (below the $47-$55 marketed range), raising **~$1.5B** — the biggest US tech IPO since 2021. Trading began 2025-03-28 on Nasdaq under CRWV. ([CoreWeave PR](https://www.coreweave.com/news/coreweave-announces-pricing-of-initial-public-offering); [CNBC](https://www.cnbc.com/2025/03/27/coreweave-prices-ipo-at-40-a-share-below-expected-range.html))

### Revenue & customer concentration
- FY2024 revenue **$1.9B**, net loss **$863M** ([levelheadedinvesting](https://www.levelheadedinvesting.com/p/when-growth-runs-on-debt-the-coreweave-case-study)). FY2025 revenue **$5,131M**, net loss **$(1,167)M** ([CoreWeave Q4/FY25 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx)).
- **Microsoft = 62% of FY2024 revenue; two customers = 77%** ([mlq.ai](https://mlq.ai/research/coreweave/); [ainvest](https://www.ainvest.com/news/coreweave-ipo-house-cards-built-gpus-microsoft-2506/)). **Microsoft = 67% of FY2025 revenue** per the FY2025 10-K, with mgmt expecting it to fall below 50% as OpenAI/Meta ramp ([CRWV 10-K FY2025](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000104/crwv-20251231.htm); [indexbox](https://www.indexbox.io/blog/coreweaves-2025-revenue-hits-51b-amid-21b-debt-and-customer-risks/)).

### OpenAI contracts (cumulative ~$22.4B)
- Mar 2025: initial deal up to **$11.9B** ([CoreWeave](https://www.coreweave.com/news/coreweave-announces-agreement-with-openai-to-deliver-ai-infrastructure)).
- May 2025: expansion up to **$4B**.
- Sep 2025: further **$6.5B** expansion → cumulative **~$22.4B** ([CoreWeave PR](https://www.coreweave.com/news/coreweave-expands-agreement-with-openai-by-up-to-6-5b); [Bloomberg](https://www.bloomberg.com/news/articles/2025-09-25/coreweave-expands-deals-with-openai-to-as-much-as-22-4-billion)).

### Backlog / RPO
- Revenue backlog **$30B (Q2'25) → $55.6B (Q3'25, +271% YoY) → $66.8B (12/31/2025)** ([CRWV Q3'25 8-K](https://www.sec.gov/Archives/edgar/data/0001769628/000176962825000059/coreweave3q25earningspress.htm); [Fortune](https://fortune.com/2025/11/10/coreweave-earnings-infrastructure-debt-ai-bubble/); [FY25 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx)).
- Q3'25: no single customer >~35% of backlog; >60% investment-grade. Q3 added Meta **~$14.2B** and Poolside ([Nasdaq](https://www.nasdaq.com/articles/can-coreweave-convert-its-55b-backlog-profitable-growth)).

### Debt — total and GPU-collateralized facilities
- **Total debt 12/31/2025 = $21,373M** ($6,708M current + $14,665M non-current); cash ~$3.1B; capex FY2025 = **$10,309M** ([CoreWeave FY25 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx); [CNBC Q4](https://www.cnbc.com/2026/02/26/coreweave-crwv-q4-earnings-report-2025.html)). Up from >$8B at YE2024 ([levelheadedinvesting](https://www.levelheadedinvesting.com/p/when-growth-runs-on-debt-the-coreweave-case-study)).
- **DDTL 1.0** — Aug 2023: **$2.3B** GPU-collateralized facility (Blackstone, Magnetar) ([ABF Journal](https://www.abfjournal.com/magnetar-and-blackstone-provide-7-5b-in-debt-financing-facility-for-coreweave/)).
- **DDTL 2.0** — May 2024: **$7.5B** facility led by Blackstone & Magnetar (w/ Coatue), secured against the NVIDIA GPU fleet ([Blackstone PR](https://www.blackstone.com/news/press/coreweave-secures-7-5-billion-debt-financing-facility-led-by-blackstone-and-magnetar/); [CNBC](https://www.cnbc.com/2024/05/17/ai-startup-coreweave-raises-7point5-billion-in-debt-blackstone-leads.html)).
- **DDTL 4.0** — closed ~Jan 2026: **$8.5B** delayed-draw term loan, rated **A3 (Moody's) / A (low) (DBRS)** — the first investment-grade GPU-backed financing, secured by HPC infrastructure + an associated customer contract ([CoreWeave PR](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Closes-Landmark-8-5-Billion-Financing-Facility-Achieving-First-Investment-Grade-Rated-GPU-backed-Financing/default.aspx)).
- Aggregate GPU-backed debt estimated **~$10B** ([Yahoo/Chanos](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html)).

### NVIDIA ties (equity + backstop)
- **Equity:** NVIDIA held ~24.3M shares (~$3.96B, its largest equity holding, ~91% of its portfolio) at end of Q2'25 ([Motley Fool](https://www.fool.com/investing/2025/09/19/nvidias-63-billion-deal-with-coreweave-signals-som/)). Added **$2.0B** at $87.20/sh (22,935,780 shares) completed 2026-01-23 ([CRWV 8-K](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000044/ex991pressrelease_final.htm)).
- **Backstop / take-or-pay:** NVIDIA obligated to buy unsold CoreWeave capacity up to **$6.3B through April 2032** — agreement signed 2023, disclosed in SEC filing Sep 2025 ([Coindesk](https://www.coindesk.com/markets/2025/09/15/coreweave-stock-climbs-7-after-usd6-3b-cloud-capacity-deal-with-nvidia); [Yahoo](https://finance.yahoo.com/news/coreweaves-6-3-billion-backstop-103000258.html)).

---

## 2. Oracle (ORCL)

### The ~$300B OpenAI contract
- ~$300B over 5 years, **~$30B/yr**, 4.5 GW incremental Stargate capacity, commencing **2027** ([Built In](https://builtin.com/articles/openai-300b-cloud-deal-oracle-20250911); [OpenAI](https://openai.com/index/five-new-stargate-sites/); [DCD](https://www.datacenterdynamics.com/en/news/openai-confirmed-to-be-behind-30bn-a-year-oracle-cloud-deal-45gw-expected-across-multiple-data-center-sites/)).

### RPO surge
- RPO **$317B (Q4 FY25) → $455B (Q1 FY26, +359% YoY)**; cloud RPO +~500%; ~33% to convert within 12 months. Catz: RPO likely >$500B ([Oracle Q1 FY26 PR](https://www.oracle.com/news/announcement/q1fy26-earnings-release-2025-09-09/); [DCD](https://www.datacenterdynamics.com/en/news/oracle-has-455bn-in-remaining-performance-obligations-at-end-of-q1-2026/)).
- OCI revenue guided $18B (FY26) → $32B → $73B → $114B → **$144B** over following years ([Oracle PR](https://www.oracle.com/news/announcement/q1fy26-earnings-release-2025-09-09/)).

### Capex & debt financing
- **$18B notes issued 2025-09-26** (maturities 2030-2065, coupons 4.450%-6.100%) to pre-fund the AI buildout ([Oracle 424B2](https://www.sec.gov/Archives/edgar/data/0001341439/000119312525217490/d37885d424b2.htm); [DCD](https://www.datacenterdynamics.com/en/news/oracle-takes-on-18bn-in-debt-ahead-of-ai-data-center-build-out/)).
- ~**$91.3B senior unsecured borrowings outstanding** as of 2025-08-31 ([Oracle 10-Q FY26 Q1](https://www.sec.gov/Archives/edgar/data/0001341439/000119312525200095/orcl-20250831.htm)).

### Thin/negative AI cloud margins
- Internal docs (via The Information, Oct 2025): in the 3 months to Aug 2025, ~$900M of Nvidia-GPU rental revenue produced only ~$125M gross profit = **~14% gross margin** (vs ~70% legacy software). Average AI-cloud deal margin reportedly ~16%; struggling to clear 25% on 1-2 year-old chips ([CNBC](https://www.cnbc.com/2025/10/07/oracle-stock-nvidia-chip-margins.html); [DCD](https://www.datacenterdynamics.com/en/news/internal-documents-show-oracles-average-profit-margin-for-ai-cloud-deals-was-16-report/); [The Information](https://www.theinformation.com/articles/oracle-assures-investors-ai-cloud-margins-struggles-profit-older-nvidia-chips)).

---

## 3. Stargate JV

- Announced 2025-01-21: company to invest **$500B over 4 years**; **$100B initial** ([OpenAI](https://openai.com/index/announcing-the-stargate-project/)).
- **Equity (committed):** SoftBank and OpenAI **$19B each (40% each)**; Oracle and MGX **$7B each** ([S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/research/softbabnk-openai-oracle-and-mgx-commit-to-100b-for-stargate-ai-infrastructure); [Wikipedia/Stargate LLC](https://en.wikipedia.org/wiki/Stargate_LLC)). SoftBank = financial lead; OpenAI = operational lead; Masayoshi Son chairman.
- **Announced vs committed:** $500B/10 GW is a target by 2029; the headline includes already-announced projects. By Sep 2025, OpenAI/Oracle/SoftBank said five new sites + Abilene push the program to ~7 GW and >$400B over three years ([OpenAI](https://openai.com/index/five-new-stargate-sites/)).
- **Sites & SPV financing:** Flagship **Abilene, TX** built by **Crusoe / Primary Digital Infrastructure / Blue Owl Capital** JV, leased to Oracle ([Wikipedia](https://en.wikipedia.org/wiki/Stargate_LLC)). **JPMorgan lent $2.3B** (2025-05-22) to the Abilene project ([Wikipedia](https://en.wikipedia.org/wiki/Stargate_LLC)). **Vantage Data Centers** taking on **~$38B of debt** for two sites (TX, WI) ([wheresyoured.at](https://www.wheresyoured.at/oracle-openai/)).

---

## 4. Other neoclouds & circular NVIDIA ties

- **Crusoe:** ~$425M GPU-backed debt ([Yahoo/Chanos](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html)); NVIDIA participated in $1.4B Series E (Oct 2025) at $10B valuation ([TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/)).
- **Lambda:** ~$500M GPU-backed debt; NVIDIA backstop **$1.5B** capacity deal; NVIDIA in $480M Series D ([Yahoo](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html); [TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/)).
- **Nscale:** NVIDIA **$433M SAFE** + £500M commitment (Oct 2025); soared to $14.6B valuation ([TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/); [DCK](https://www.datacenterknowledge.com/servers/nvidia-backed-nscale-soars-to-14-6b-valuation-after-latest-funding-round)).
- **Nebius:** Microsoft contract up to **$19.4B** (Sep 2025); NVIDIA in $700M raise (Dec 2024) and a further **$2B** NVIDIA investment ([SEC 6-K](https://www.sec.gov/Archives/edgar/data/0001513845/000110465925088312/tm2525580d1_6k.htm); [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-and-nebius-partner-to-scale-full-stack-ai-cloud)).
- NVIDIA also separately backs **$860M** of a partner data center's lease obligations ([DCD](https://www.datacenterdynamics.com/en/news/nvidia-backs-860m-lease-obligations-of-partner-data-center/)).

---

## 5. Systemic: how much is debt-financed + GPU-depreciation risk

- **Morgan Stanley:** ~$3T data-center capex through 2028; cash funds ~half; **~$1.5T financing gap** to credit markets across secured/unsecured/structured/securitized ([Energynow](https://energynow.com/2026/02/the-3-trillion-ai-data-center-build-out-becomes-all-consuming-for-debt-markets/); [Morgan Stanley](https://www.morganstanley.com/insights/articles/ai-market-trends-institute-2026)).
- **Moody's:** **$662B** of not-yet-commenced hyperscaler lease commitments (Amazon, Meta, Alphabet, Microsoft, Oracle) = **113% of their combined adjusted debt**; $969B total undiscounted future lease commitments at YE2025. AI semis useful life **4-6 yrs** vs 10-15 yr leases ([Yahoo/Moody's](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html)).
- **GPU ABS:** First GPU-backed ABS (~$1.1B shelf) in early 2025, AAA notes inside ~110 bps; issuance forecast **~$8B (2025) → ~$25B (2028)** ([airealist](https://www.airealist.ai/p/two-markets-one-asset-the-gpu-debt); [Medium](https://medium.com/@Elongated_musk/silicon-to-securities-how-gpus-became-aaa-rated-abs-assets-c0e75199327a)).
- **Short-seller flag:** Jim Chanos warns of "debt defaults" in the GPU-collateral debt market ([Yahoo](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html)).

---

## Debt table

| Borrower | Instrument | Amount | Date | Collateral / notes | Status | Source |
|---|---|---|---|---|---|---|
| CoreWeave | Total debt (balance sheet) | $21,373M | 12/31/2025 | $6.71B current / $14.67B non-current | Outstanding | [FY25](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx) |
| CoreWeave | DDTL 1.0 | $2.3B | Aug 2023 | GPU-collateralized (Blackstone, Magnetar) | Closed | [ABF](https://www.abfjournal.com/magnetar-and-blackstone-provide-7-5b-in-debt-financing-facility-for-coreweave/) |
| CoreWeave | DDTL 2.0 | $7.5B | May 2024 | Secured vs NVIDIA GPU fleet (Blackstone/Magnetar/Coatue) | Closed | [Blackstone](https://www.blackstone.com/news/press/coreweave-secures-7-5-billion-debt-financing-facility-led-by-blackstone-and-magnetar/) |
| CoreWeave | DDTL 4.0 | $8.5B | ~Jan 2026 | GPU/HPC + customer contract; IG-rated A3/A(low) | Closed | [CRWV](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Closes-Landmark-8-5-Billion-Financing-Facility-Achieving-First-Investment-Grade-Rated-GPU-backed-Financing/default.aspx) |
| CoreWeave | Revolving credit | $2.5B | Q4 2025 | Expanded RCF | Available | [FY25](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx) |
| Oracle | Senior notes | $18B | 9/26/2025 | Unsecured, fund AI capex | Issued | [424B2](https://www.sec.gov/Archives/edgar/data/0001341439/000119312525217490/d37885d424b2.htm) |
| Oracle | Senior unsecured borrowings (total) | ~$91.3B | 8/31/2025 | Unsecured | Outstanding | [10-Q](https://www.sec.gov/Archives/edgar/data/0001341439/000119312525200095/orcl-20250831.htm) |
| Stargate/Abilene | JPMorgan loan | $2.3B | 5/22/2025 | Abilene TX project (Crusoe/Blue Owl SPV) | Committed | [Wiki](https://en.wikipedia.org/wiki/Stargate_LLC) |
| Vantage (OpenAI sites) | Project debt | ~$38B | 2025 | TX + WI sites | Reported | [wheresyoured.at](https://www.wheresyoured.at/oracle-openai/) |
| Lambda | GPU-backed debt | ~$500M | 2025 | GPUs as collateral | Outstanding | [Yahoo](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html) |
| Crusoe | GPU-backed debt | ~$425M | 2025 | GPUs as collateral | Outstanding | [Yahoo](https://finance.yahoo.com/news/famed-short-seller-jim-chanos-sees-risks-in-growing-debt-market-backed-by-nvidias-ai-chips-theres-going-to-be-debt-defaults-110013557.html) |

## Edge (relationship) table

| From | To | Instrument | Amount | Date | Circular? | Status | Source |
|---|---|---|---|---|---|---|---|
| NVIDIA | CoreWeave | Equity | $2.0B (+~$3.96B prior holding) | 1/23/2026 | Yes | Completed | [8-K](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000044/ex991pressrelease_final.htm) |
| NVIDIA | CoreWeave | Take-or-pay backstop | $6.3B | thru 4/2032 (signed 2023) | Yes | Active | [Coindesk](https://www.coindesk.com/markets/2025/09/15/coreweave-stock-climbs-7-after-usd6-3b-cloud-capacity-deal-with-nvidia) |
| CoreWeave | NVIDIA | GPU purchases | (capex $10.3B FY25) | FY2025 | Yes | Ongoing | [FY25](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx) |
| OpenAI | CoreWeave | Compute contract | ~$22.4B | 2025 | Yes | Active | [Bloomberg](https://www.bloomberg.com/news/articles/2025-09-25/coreweave-expands-deals-with-openai-to-as-much-as-22-4-billion) |
| Microsoft | CoreWeave | Compute (62% '24 / 67% '25 rev) | n/a | FY24-25 | No | Active | [10-K](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000104/crwv-20251231.htm) |
| NVIDIA | OpenAI | Equity (LOI "up to") | up to $100B → ~$30B actual | 9/22/2025 / Feb 2026 | Yes | Partly funded | [CNBC](https://www.cnbc.com/2025/09/22/nvidia-openai-data-center.html) |
| OpenAI | Oracle | Compute contract | ~$300B | 2025, starts 2027 | Yes | Contracted | [Built In](https://builtin.com/articles/openai-300b-cloud-deal-oracle-20250911) |
| Oracle | NVIDIA | GPU purchases (~14% GM) | n/a | 2025 | Yes | Ongoing | [CNBC](https://www.cnbc.com/2025/10/07/oracle-stock-nvidia-chip-margins.html) |
| SoftBank/OpenAI/Oracle/MGX | Stargate JV | Equity | $19B/$19B/$7B/$7B | 2025 | Partial | Committed | [S&P](https://www.spglobal.com/market-intelligence/en/news-insights/research/softbabnk-openai-oracle-and-mgx-commit-to-100b-for-stargate-ai-infrastructure) |
| NVIDIA | Nscale | SAFE/equity | $433M + £500M | Oct 2025 | Yes | Funded | [TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/) |
| NVIDIA | Lambda | Backstop + equity | $1.5B + Series D | 2025 | Yes | Active | [TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/) |
| NVIDIA | Crusoe | Equity (Series E) | part of $1.4B | Oct 2025 | Yes | Funded | [TechCrunch](https://techcrunch.com/2026/01/02/nvidias-ai-empire-a-look-at-its-top-startup-investments/) |
| NVIDIA | Nebius | Equity | $0.7B + $2B | 2024-25 | Yes | Funded | [NVIDIA](https://nvidianews.nvidia.com/news/nvidia-and-nebius-partner-to-scale-full-stack-ai-cloud) |
| Microsoft | Nebius | Compute contract | up to $19.4B | Sep 2025 | No | Active | [6-K](https://www.sec.gov/Archives/edgar/data/0001513845/000110465925088312/tm2525580d1_6k.htm) |

---

## Unverifiable / soft data
- Vantage's "~$38B" project debt is sourced to commentary (wheresyoured.at) citing reporting, not a primary filing.
- Lambda/Crusoe GPU-backed debt amounts (~$500M / ~$425M) are from a Chanos-referencing aggregation, not the borrowers' filings.
- NVIDIA→OpenAI "$100B" was a **letter of intent**; only ~$30B was reportedly finalized (Feb 2026, part of OpenAI's ~$110B round) — figure still firming.
- Stargate's $500B is a multi-year **target**; only ~$100B/initial $52B of equity is committed; the rest is announced, not funded.
- The Information's Oracle margin docs (14%/16%) are leaked internal documents, not audited disclosures.

## The duration-mismatch layer *(added 2026-06-11)*
The debt table above understates the problem, because it counts the *financing* but not the *useful life of what it bought*. Oracle's **FY2026 8-K** shows the pivot in stark form: free cash flow **−$23.7B**, ~$50B capex, >$108B debt (+$30B raised), and **$248B of additional 15–19-year datacenter leases**, substantially off-balance-sheet — all against GPUs whose **economic life is ~2–3 years**. That gap is the subject of the [[fin-ai-depreciation-debttrap]] block and the [[depreciation_trap]] Z3 proof (D1–D4): when asset life < financing tenor, there is an interval where the asset is worthless but the debt is still owed, and the "useful life" hyperscalers book (5–6 yr) is itself a self-marked number inflating today's profit (~$176B industry overstatement 2026–28, per Burry). So the CoreWeave/Oracle leverage here is not just *concentrated* (67% one customer; >half the $523B backlog on OpenAI) — the **real assets backing it amortize slower in the accounts than they age out in reality.** CNBC's framing — *"building yesterday's data centers with tomorrow's debt"* — is the duration mismatch in one line.
