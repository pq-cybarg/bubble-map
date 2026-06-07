# Executive Summary — Unmasking the AI Earnings Bubble

*Generated 2026-06-07 from the live models. Full analysis: `report/UNMASKING.md` + `report/TEMPORAL-WEB.md`. Open `report/INDEX.html` for the dashboard.*

## The finding in one sentence
The AI build-out is a **self-referential capital loop** that books each firm's spending as another's revenue and is **solvent only while external capital keeps flowing** — and the same defect (promises far exceeding deliverable substance, risk parked in the least-regulated venue) recurs in bank securities books, private credit, metals, and the power grid, while the loop's largest actors converge on the **digital-identity control layer**.

## What is machine-proven (not asserted)
- **An 11-firm circular core** (Tarjan SCC): NVIDIA, OpenAI, Oracle, CoreWeave, Microsoft, Amazon, Anthropic, AMD, Crusoe, Lambda + lenders; **15 round-trip cycles**.
- **OpenAI needs ≥ $1.03 trillion of external capital** to honor its commitments (Z3 T3, UNSAT); the **core is insolvent at zero external inflow** (T4) — the formal signature of a bubble.
- **NVIDIA vendor-financing self-funding: 10% funded-only / 56% headline.**
- **SpaceX is separable** — the only node circular *solely via cancelable edges* — but **financially cross-held** by Google's ~$100B equity stake + the xAI merger.
- **A single capital shock cascades** OpenAI→CoreWeave→Oracle (TLA+ trace); SpaceX never defaults.
- **The Fed has no feasible single rate** (Z3 F1–F3, UNSAT) — it can only choose what to sacrifice.
- **Three physical chokepoints**, two adversary-controlled: capital (trap), **rare earths/China** (independence ~2028), **power+HALEU/Russia** (~2028-29) — none liftable by dollars on the timeline.

## The hard-money lens
Re-priced in gold, most "gains" are debasement: a US home is **−81% in gold** since 1998; CRE peaked in gold ~2001; the **$1-trillion defense budget buys ~25%** of the gold the 1998 one did; OpenAI's $1.4T is **0.53× all of TARP** in gold.

## The honest answer to "is it all connected?"
**Not one cabal — a small elite operator-network + recurring structures + regulatory arbitrage.** The temporal meta-graph (1998→2026) shows the weavers (OpenAI, a16z, the PayPal-mafia/Thiel, Circle/USDC, BlackRock, the SPV structure, Larry Summers as the literal dereg→AI→Epstein bridge) and the recurring devices (LTCM interconnection, Enron off-balance-sheet SPVs + mark-to-market, dotcom vendor financing) rebuilt in each era's least-regulated venue. Intent is never inferred from adjacency; sensitive threads (Epstein, Waters, foreign influence) are graded and quarantined from the proofs.

## Reproduce
`bash run_all.sh` — runs all 5 Z3 engines, TLA+, Alloy, the graph/bank/temporal/gold/defense/energy models. 19 cited source files in `research/`.
