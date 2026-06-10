# Jobs, inflation, and the Fed vs the bond market

*Web-verified 2026-06-09. Data + sourcing behind **[docs/charts.html](https://pq-cybarg.github.io/bubble-map/charts.html)**. All series annual, public (FRED/BLS/Treasury/BIS/BOJ), rounded; verify at the cited series. Overlay; not used in the proofs. The "Fed follows the 2Y, not the mandate" reading is a **strong, labeled interpretation** — the co-movement is fact, the intent is inference.*

## Two claims the charts test
1. A single "jobs number" and "inflation number" **hide opposite trends** — you must disambiguate to see the truth.
2. The Fed's policy rate **tracks the bond market (the 2-year yield)** far more tightly than its statutory **dual mandate** (2% inflation + maximum employment).

## Disambiguating "employment"
- **Headline payrolls overstated, revised late:** the QCEW benchmarks cut **~1.5M** jobs across 2024–25 (−818k, −911k), arriving 6–18 months after the prints that drove decisions.
- **U-3 vs U-6:** the headline ran 3.6–4.4%; **U-6** (discouraged + involuntary part-time) ran **~3–5 pts higher** (6.8–8.1%) — the slack "maximum employment" omits.
- **Sectoral divergence:** recent growth is concentrated in **health care, leisure/hospitality, and state/local government**, while **manufacturing, information (tech), temp help, and federal government shrank.** One aggregate masks opposite trends.
- **Gig:** full-time independents **13.6M → 27.7M**; multiple-jobholders inflate the count (`macro-gig-labor`).

## Disambiguating "inflation"
- **CPI vs core PCE** differ by weight/scope (PCE ~0.3–0.4 pt lower); **neither sat at 2%** for most of the decade (~0% in 2015, 4–8% in 2021–23, ~3% in 2024–26).
- **CPI shelter (~⅓ of CPI) lags market rents ~1 year** (ALNRI/Zillow/NTRI, `macro-rent-cpi-divergence`) — misstating turning points both ways.
- **In gold, a US home is −81% since 1998** (`macro-gold-silver-reprice`) — "2% inflation" is an artifact relative to debasement.

## The Fed follows the bond market — *co-movement FACT; "responding to bonds" interpretation*
- The funds target and the **2-year Treasury yield move together, and the 2Y turns first** at every pivot: it fell below the funds rate ahead of the **2019** and **2024** cuts and rose ahead of/with the **2022** hikes. The Fed *ratifies* the market's expectation.
- If it steered to the **mandate**, the funds rate would track 2% + full employment — instead it sat at **0.25% through 3.6% core PCE** (2021) and stayed **≥4.5–5.5%** as core PCE fell to ~2.8% and U-6 rose (2023–25).
- The long end and the **global bond market** bind it too: US 10Y/30Y, **Baa ~6%**, and the **10Y JGB escaping YCC (0% → 2.0% Dec-2025 → ~2.66% 2026)** — raising the cost of the yen carry trade that funds crowded longs (`macro-carry-trades`).
- **Z3 (`macro-fed-trap`):** there is **no single feasible rate** satisfying the divergent targets — so the mandate cannot be what sets the rate; financial conditions / the bond market do.

## Rate differentials — sharp/fast vs smooth/delayed (measured)
Different spreads trade off noise against lead horizon (computed on the monthly cache, predicting the subsequent fed-funds change):

| Differential | Noise (Δσ, pp) | Best lead horizon | Corr |
|---|---|---|---|
| **3M − funds** | **0.10** | **~1 mo** | +0.72 |
| **2Y − funds** | 0.20 | **~8 mo** | **+0.77** |
| **2Y − 3M (policy-path)** | 0.17 | ~9 mo | +0.66 |
| **10Y − 2Y (2s10s)** | 0.12 | **~18 mo+** | +0.38 |
| **10Y − 3M (3m10s)** | 0.21 | ~18 mo+ | +0.54 |

The **horizon lengthens from the short end to the curve** (1–8 months → 18+ months) — the fast-vs-delayed axis. Noise is *not* monotonic (the 3M−funds gap is the cleanest; the 2Y−funds and 10Y−3M are jumpiest). **Use the right differential for the question:** 3M−funds for the fastest clean read on an imminent move, 2Y−funds for the strongest read on the Fed's direction, the 2s10s curve for the smoothest (most delayed) cycle/recession read. Charts: [docs/charts.html](https://pq-cybarg.github.io/bubble-map/charts.html).

## Bond-market breakdowns (charts page)
The differentials extend across the curve and the bond universe — sliced by **geography** (region → sub-region → country, GDP-weighted: US/CA, DE/GB/FR/IT, JP/AU → global) and **type/quality** (sovereign 10Y, corporate Baa/Aaa, household 30Y-mortgage, and corporate OAS by rating AAA/BBB/CCC). Plus **30Y term-premium** differentials and **credit spreads** (Baa−10Y full history; HY/IG OAS recent). Where a licensed feed would be needed, **accessible proxies are substituted** (the licensed indices source from the same public tape anyway): industry-sector → the free **AAA→CCC rating ladder + EM-corporate OAS** (true industry via **FINRA TRACE**, free trade tape); state/city munis → the published **muni/Treasury ratio snapshot + MUB ETF + FRED's WSLB20 (to 2016)** (full series via **MSRB EMMA**, free trade tape). The **per-institution** cut already exists in the repo via the FDIC BankFind API (`models/graph/bank_exposure.py`). Full provenance table on the [charts page](https://pq-cybarg.github.io/bubble-map/charts.html).

## Bottom line
Disambiguation dissolves the official story, and the rate path maps onto the **2-year yield**, not onto 2% inflation or full employment. The evidence supports the thesis: **the Fed steers to the bond market / financial conditions, with the "dual mandate" as the public framing.**
