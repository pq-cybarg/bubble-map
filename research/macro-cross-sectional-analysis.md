# Cross-sectional analysis — dispersion, relative value, and the common factor

*Computed 2026-06-10 by `models/graph/cross_section.py` → `data/cross_section.json`. Rendered on **[docs/charts.html#xsec](https://pq-cybarg.github.io/bubble-map/charts.html#xsec)** and the **[dashboard](https://pq-cybarg.github.io/bubble-map/dashboard.html#xsec)**. The computation is fact (re-runs from the cached data); the diversification reading is a labeled interpretation. Not used in the formal proofs.*

Most of the charts elsewhere are **time-series** (one rate through time). This block is **cross-sectional**: at each moment it compares the whole *cross-section* of segments — every credit-rating bucket, every developed sovereign, every muni state — and asks three questions the desk literature asks:

1. **How dispersed** is the cross-section (and is that compressed or stretched vs its own history)?
2. **Which segments are rich or cheap** vs their own trailing history (relative value)?
3. **How much of the co-movement is one shared factor** (the common-factor / PC1 share)?

It runs over four cross-sections, in the order requested.

## Method (and why)
For each time-series cross-section we compute, on a common monthly date grid:
- **Dispersion over time** — the cross-sectional standard deviation / range across segments each month. It **compresses in calm regimes and blows out in stress** (the credit-dispersion-as-stress gauge). We also z-score the *current* dispersion vs its own history (compressed / mid-range / elevated).
- **Relative-value z-scores** — each segment's latest level vs its **own** trailing history (z-score + percentile). Standard desk relative value: positive z = wide/cheap vs its history (more stress priced), negative = rich/tight.
- **Snapshot ranking** — the latest month, every segment side by side, ranked.
- **Cross-sectional correlation + PC1 share** — Pearson correlation of monthly **changes** (the Collin-Dufresne–Goldstein–Martin basis), plus the **first-principal-component variance share** via power iteration on the correlation matrix (a correlation matrix's eigenvalues sum to *n*, so PC1 share = λ₁ ⁄ *n*). The PC1 share is the empirical signature of a single common factor.

**Literature anchors.** Collin-Dufresne, Goldstein & Martin (2001), *The Determinants of Credit Spread Changes* (J. Finance 56(6)) found that monthly credit-spread changes are dominated by **one common systematic factor** the usual structural variables (leverage, vol, rates, slope) don't explain. Cross-sectional spread **dispersion** is a standard stress/credit-cycle gauge; **sovereign-yield dispersion** across a bloc is a fragmentation gauge; **z-score/percentile vs own history** is desk-standard relative value.

## Results (2026-06-10 snapshot)

| Cross-section | Segments | Avg pairwise corr | **PC1 share** | Dispersion now |
|---|---|---|---|---|
| **US corporate credit** (OAS rating ladder) | 5 | 0.88 | **91%** | elevated |
| Developed sovereign 10Y | 8 | 0.63 | 70% | mid-range |
| Municipal (per-state/quality) | 4 | 0.47 | 70% | compressed |
| Corporate breadth by tier (FINRA TRACE) | 3 | 0.81 | 87% | compressed |

- **US credit's ~91% PC1 share** (and ~0.88 average pairwise correlation on monthly OAS changes) is a textbook confirmation of the CDGM common factor: the AAA/BBB/CCC/IG/HY buckets move almost as one. The credit-spread change **correlation heatmap** (on the charts page) is nearly solid red.
- **TRACE breadth** (the real trade-tape advance/decline ratio by IG/HY/convertibles) shows the same one-factor risk-on/off (87%).
- **Sovereigns** load on a global-rates common factor (70%), with the **unified snapshot** flagging **Japan** as the most stretched segment vs its own history — consistent with the JGB escaping yield-curve-control.

**Bank cross-section (FDIC, 194 institutions).** Each bank is z-scored against its peers on three axes — HTM loss/equity, uninsured-deposit %, CRE/Tier-1 — and a **composite z** ranks system vulnerability with a percentile. The cross-sectional **standard deviation of HTM holes ≈ 7.5 pp of equity**: the hidden losses are highly *unequal* across the system (the SVB lesson — the average is benign while the tail is not).

**Funding-graph connectors.** The cross-layer connectors are re-scored with a **bridge_score = z(degree) + z(distinct neighbor-sectors) + 0.5 if the node spans both the financial and structural layers** — surfacing the structural keystones that tie the proven financial core to the surrounding webs.

**Unified snapshot.** Every time-series segment is z-scored vs its own history so credit, sovereign, muni, and breadth read on one scale, ranked from most- to least-stressed.

## Where the data *disagrees* with the literature
Mean-variance portfolio theory says holding many different credits diversifies idiosyncratic risk away. When **PC1 explains ~91% of the cross-sectional variance, that diversification is illusory at the system level** — the segments are one trade. That is the empirical agreement with the project's machine-checked **self-marked-value** result (`models/z3/self_marked_value.py`, U1–U4): the gaps across the four self-marked asset classes **correlate under a common factor, so there is no netting**, and carrying value is forced to converge on a forcing event. The cross-section is not a portfolio; it is a single position wearing many labels.

## Reproduce
`python3 models/graph/cross_section.py` (pure stdlib; recomputes from `data/fred_monthly.json`, `data/yahoo_monthly.json`, `data/tape_trace.json`, `data/bank_exposure.json`, `data/graph.json`). Wired into `run_all.sh` and `scripts/new-research.sh`. Full charts, heatmap, and tables: [docs/charts.html#xsec](https://pq-cybarg.github.io/bubble-map/charts.html#xsec).
