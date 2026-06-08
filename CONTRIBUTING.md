# Contributing & How to Verify

This project's whole point is that its core claims are **reproducible and machine-checked**.
You don't have to trust it — you can run it.

## Reproduce everything (one command)
```bash
git clone https://github.com/pq-cybarg/bubble-map && cd bubble-map
bash run_all.sh
```
Requirements: `python3` with the `z3-solver` package (`pip install z3-solver`), and `java`
(for TLA+/Alloy — the jars auto-download on first run). Only `models/graph/bank_exposure.py`
needs the network (a live FDIC API pull).

## What each engine proves
- `models/z3/circularity_smt.py` — the circular core can't self-finance; OpenAI needs ≥$1.03T
  external capital; core insolvent at zero inflow; SpaceX separable. (SAT/UNSAT verdicts.)
- `models/z3/coordination_game.py` — small-bank stablecoin coalition is a suppressible coordination trap.
- `models/z3/fed_policy_trap.py` — no single policy rate satisfies the divergent targets (UNSAT).
- `models/z3/defense_chokepoint.py` / `power_adequacy.py` — rare-earth (China) & power/HALEU (Russia)
  chokepoints; independence infeasible until ~2028 (UNSAT).
- `models/z3/scenario.py` — parameterized BASE/BULL/BEAR verdicts; dial the assumptions.
- `models/tla/BubbleCascade.tla` — the unwind cascade (TLC trace) + SpaceX-safe invariant.
- `models/alloy/BubbleStructure.als` — relational structure checks.
- `models/graph/*.py` — the consolidated funding graph, FDIC bank model, temporal meta-graph,
  gold re-pricing, defense/energy/blockchain sub-webs, allied min-cut, contagion matrix, dashboards.

Every figure cites its source URLs in the matching `research/*.json`.

## How to contribute
1. **Fork, branch, PR.** Keep changes reproducible — if you change a number, change its source citation.
2. **Cite primary sources** (filings, regulators, exchanges) where possible.
3. **Grade speculation.** Mark claims fact / strong / moderate / weak / speculative. Never infer
   intent from adjacency. Keep speculative threads in `spec-*`/graded sections, out of the proofs.
4. **No price predictions or financial advice.** This is structural analysis, not investment guidance.
5. **Improve the tooling** — the highest-leverage contributions lower the cost for others to verify
   or coordinate (better data pulls, privacy-preserving identity reference code, clearer visualizations).

## Opsec note
This is a **pseudonymous** project. Please don't add personal identifying information (names,
emails, real-world locations) to commits, files, or metadata. Use a throwaway identity for contributions.

## License
See `LICENSE` (or open an issue if none is set yet).

## Re-review on every change (REQUIRED)
Whenever you add or edit a `research/*.json` block, **re-review all prior findings before committing**:
```bash
bash scripts/new-research.sh   # runs build_graph + audit + cross_review + dashboard
```
Then read `report/AUDIT.md` and `report/CROSS-REVIEW.md` and **reconcile every flag** — sync counts, resolve same-instrument edge conflicts (LOI vs closed / cumulative / date), and add missing cross-links. The repo's integrity depends on each new block being checked against the whole corpus.
