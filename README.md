# Bubble Map — a formally-verified anatomy of the AI capital loop

[![Live](https://img.shields.io/badge/live-pq--cybarg.github.io%2Fbubble--map-7fd1ff)](https://pq-cybarg.github.io/bubble-map/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![Reproduce](https://img.shields.io/badge/reproduce-bash%20run__all.sh-7CFC9B)](run_all.sh) [![Proofs](https://img.shields.io/badge/proofs-Z3%20%C2%B7%20TLA%2B%20%C2%B7%20Alloy-ffd479)](#formal-engines-models)

A forensic, **formally-verified** analysis of the AI earnings bubble: the circular funding among
NVIDIA / OpenAI / Microsoft / Oracle / CoreWeave / Anthropic / Amazon (+ the SpaceX/SPCX edge),
and the macro, commodity, banking, and political-economy systems around it.

**Start here:** [`report/UNMASKING.md`](report/UNMASKING.md) — the full analysis.
**🌐 Live:** https://pq-cybarg.github.io/bubble-map/ · 📊 [Dashboard](https://pq-cybarg.github.io/bubble-map/dashboard.html) · 🌍 [Globe](https://pq-cybarg.github.io/bubble-map/globe.html) · ✍️ [Sign the poll](https://github.com/pq-cybarg/bubble-map/issues/1)

**Verify:** [`CONTRIBUTING.md`](CONTRIBUTING.md) · **Reproduce everything:** `bash run_all.sh`

## What is proven vs. evidenced
- **Layer 1 — AI circular core: PROVEN** by four independent engines (below).
- **Layer 2 — banking/credit: STRONG** primary data + **two PROVEN sub-claims** (coordination trap, Fed policy trap).
- **Layer 3 — commodities/geopolitics: STRONG–MODERATE.**
- **Layer 4 — influence/identity: GRADED** (fact vs. speculation kept separate; nothing here feeds the formal proofs).

## Formal engines (`models/`)
| File | Engine | Proves |
|---|---|---|
| `graph/build_graph.py` | Tarjan SCC (pure Python) | 11-firm circular core; SpaceX circular *only* via cancelable edges |
| `z3/circularity_smt.py` | Z3 / SMT | round-trip realizable; OpenAI needs ≥$1.03T external capital; core insolvent at zero inflow; SpaceX separable |
| `z3/coordination_game.py` | Z3 / SMT | small-bank stablecoin coalition is a profitable-to-suppress coordination trap (C1–C4) |
| `z3/fed_policy_trap.py` | Z3 / SMT | one policy rate cannot satisfy N divergent targets — UNSAT (F1–F3) |
| `tla/BubbleCascade.tla` | TLA+ / TLC | a single capital-shock cascades OpenAI→CoreWeave→Oracle; SpaceX never defaults |
| `alloy/BubbleStructure.als` | Alloy (+`RunAlloy.java`) | core circular; SpaceX separable without cancelable edges |
| `graph/bank_exposure.py` | FDIC API | per-bank CRE / HTM-AFS / uninsured hierarchy (194 US banks) |
| `graph/regional_leverage.py` | — | hidden (HTM-adjusted) vs reported leverage; regional divergence by state |

## Data (`data/`)
`graph.json` (canonical entities/edges + SCC analysis) · `edges.csv` · `entities.csv` · `bank_exposure.json`.

## Sources (`research/`)
22 cited files in four groups — **every figure carries its source URLs**:
- `fin-*` — the AI funding web (NVIDIA/OpenAI, CoreWeave/Oracle, MSFT, Google/Amazon/Anthropic/Meta, Disney/Sora, SpaceX).
- `macro-*` — FDIC, bank hierarchy, CRE/private-credit, First Brands/UBS, carry trades, commodities/oil/backwardation, critical minerals, PQC chips, dereg/manipulation history, Fed-trap/regional.
- `influence-*` — Meta child-safety, China-tech, Tony Blair Institute/digital-ID, ad/censorship, Congress/HFSC.
- `spec-*` — explicitly-graded speculative overlays (crypto/SEC/Epstein). **Never used in proofs.**

## Headline findings
- **Circularity is structural:** an 11-firm SCC; OpenAI's ~$1.4T commitments require **≥$1.03T external capital** (Z3); the core is **solvent only while capital flows in**.
- **SpaceX is separable:** the *only* node circular **solely via cancelable contracts**, on a durable Starlink revenue base — your prior, formally confirmed.
- **The bubble's pattern recurs everywhere:** promises ≫ deliverable substance in AI compute (RPO≫cash), bank books (HTM hole), private credit (First Brands), and metals (silver backwardation).
- **The Fed cannot fix it** with one instrument (UNSAT); it can only choose what to sacrifice.
- **The real identity-layer "relationship":** not a cabal, but the same incumbents (Altman/Worldcoin, Meta/age-verification astroturf, Oracle-Ellison/Tony Blair Institute) converging on digital-ID control — graded, documented, kept out of the proofs.

## Requirements
`python3` with `z3-solver`; `java` (TLA+ `tla2tools.jar` and Alloy `org.alloytools.alloy.dist.jar` are fetched on first run / vendored in `models/`). No network needed except the live FDIC pull in `bank_exposure.py`.

## Honesty
Forward-looking items (SpaceX pricing, BOJ June hike), reversible "commitments" (Disney proved it), and unverified specifics are flagged in-line. Bilateral interbank exposures are not public; intent of named actors is not inferred from outcomes. See the honesty ledger in `report/UNMASKING.md §9`.

## Disclaimer
Structural analysis, not financial advice. Figures are cited to public sources; speculative threads are graded and kept out of the formal proofs.
