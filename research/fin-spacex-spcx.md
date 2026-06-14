# SpaceX / SPCX IPO + cancelable AI-compute deals (Google, Anthropic)

*Built from `research/fin-spacex-spcx.json` (web-verified: TechCrunch, Yahoo Finance, Reuters-sourced aggregators, VC Corner S-1 teardown). S-1 figures are from the prospectus — treat valuation/price as the offering range until priced. Supersedes the earlier `sec-filings.json` "not yet filed" status (the S-1 became public 2026-05-20).*

> **The key structural point.** SpaceX is the **separable node** in the bubble graph: it connects to the AI core through **cancelable** compute deals, so it **enters or leaves the circular core (Tarjan SCC) depending on whether those edges are counted** — the dual-SCC test the project runs. SpaceX has its own **exogenous revenue** (Starlink subscribers, launch, Starshield), which is why it is *not* trapped in the self-funding loop the way the AI-core firms are.

## 1. The S-1 facts
- **S-1 filed 2026-05-20**, S-1/A 2026-06-01; Nasdaq / Nasdaq Texas ticker **SPCX** (CIK 1181412).
- **~$135/share, 555.6M shares (all primary); $1.75T–$2T target valuation; ~$75B raise.**
- **2025 revenue $18.67B** — Starlink/connectivity ~$10–11.4B, launch ~$6.4B, Starshield ~$1.8B.
- **10.3M Starlink subscribers, 9,600+ satellites, ~50% YoY growth.**

## 2. The cancelable AI-compute edges
- **Google → SpaceX:** a ~$100B equity stake (2015-invested, 2026-marked, *held*) plus a reported **$920M/month compute** arrangement (TechCrunch, Jun 2026).
- **Anthropic / others:** additional compute-and-capacity deals.
- These are flagged **cancelable** in the graph (`cancelable: true`), which is exactly why the **dual-SCC analysis** in `build_graph.py` shows SpaceX **dropping out of the circular core** when cancelable edges are excluded — the formal demonstration that SpaceX is *attached to*, not *trapped in*, the AI loop.

## 3. Why it matters to the thesis
The project's circularity proof (Z3 T1–T5) is careful to show **SpaceX is separable**: it has real exogenous cash flows (Starlink/launch/Starshield) and its links to the core are contractual and cancelable. Treating it as part of the self-funding loop would *overstate* the core — so the model excludes it from the robust SCC. The SPCX IPO (a ~$1.75T+ all-primary raise) is itself a **major liquidity event** that could either absorb or strain the capital pool the AI core competes for. Cross-ref `spec-telecom-satellite`, `geopolitics-cables-space-layer`, `data/graph.json` (dual SCC).

## 4. Limits
Valuation/price are the **offering range** until priced; the Google compute figure is reported, not filed. The "separability" is a **structural (graph) result**, not a claim about SpaceX's business quality.

*Sources: [TechCrunch — Google $920M/mo to SpaceX](https://techcrunch.com/2026/06/05/google-will-pay-spacex-920m-per-month-for-compute/); [Yahoo Finance — SpaceX IPO prospectus](https://finance.yahoo.com/markets/article/spacex-files-ipo-prospectus-offering-a-peek-into-its-finances-205406189.html); [The VC Corner — SPCX S-1 teardown](https://www.thevccorner.com/p/spacex-spcx-ipo-s1-teardown-valuation-2026).*
