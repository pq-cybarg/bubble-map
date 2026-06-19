# Bubble Map — a formally-verified anatomy of the AI capital loop

[![Live](https://img.shields.io/badge/live-pq--cybarg.github.io%2Fbubble--map-7fd1ff)](https://pq-cybarg.github.io/bubble-map/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![Reproduce](https://img.shields.io/badge/reproduce-bash%20run__all.sh-7CFC9B)](run_all.sh) [![Proofs](https://img.shields.io/badge/proofs-Z3%20%C2%B7%20TLA%2B%20%C2%B7%20Alloy-ffd479)](#formal-engines-models)

A forensic, **formally-verified** analysis of the AI earnings bubble: the circular funding among
NVIDIA / OpenAI / Microsoft / Oracle / CoreWeave / Anthropic / Amazon (+ the SpaceX/SPCX edge),
and the macro, commodity, banking, and political-economy systems around it.

**Start here:** [`report/UNMASKING.md`](report/UNMASKING.md) — the full analysis.
**🌐 Live:** https://pq-cybarg.github.io/bubble-map/ · 📊 [Dashboard](https://pq-cybarg.github.io/bubble-map/dashboard.html) · 🌍 [Globe](https://pq-cybarg.github.io/bubble-map/globe.html) · ✍️ [Sign the poll](https://github.com/pq-cybarg/bubble-map/issues/1)

**Verify:** [`CONTRIBUTING.md`](CONTRIBUTING.md) · **Reproduce everything:** `bash run_all.sh`

**Hard-money split (gold lens):** S&P 500 **−69%** vs **NVIDIA +1,985% (1985)** in gold; US median home **−81%** in gold since 1998 — broad debasement + real concentration into the circular oligopoly.

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
This repository and the published site are **independent research, analysis, and opinion** offered for public-interest discussion and education. They are **not** financial, legal, or investment advice.

**Automated / LLM-assisted grading — hallucination risk.** The evidence gradings (`fact | contested | weak | unsupported`) and much of the synthesis are produced with the help of large language models and automated tooling. **LLM output can be wrong or hallucinated.** A "fact" grade is an automated, best-effort assessment of public sources — **not** a guarantee of truth. Verify any figure against its cited primary source before relying on it. Only the explicitly-marked **proof core** is machine-verified (Z3 / TLA+ / Alloy); everything else is interpretive overlay.

**No accusations; public records + good-faith interpretation.** Statements about identifiable people or organizations are drawn from public records and presented as **opinion and analysis, not assertions of fact** — and specifically **not** allegations of criminal conduct, fraud, or other unlawful behavior by any named party. Intent is **never** inferred from association or adjacency; where wrongdoing or intent would be the claim, it is marked unverified and not asserted. Behavioral notes on public figures are interpretation of the public record, not clinical diagnosis.

**Good faith & corrections.** This is a good-faith effort that may contain errors. If you are named or referenced and believe something is inaccurate, unfair, or should be removed, please open an issue on this repository and it will be reviewed and corrected promptly.

Structural analysis, not financial advice. Figures are cited to public sources; speculative threads are graded and kept out of the formal proofs.

## Age verification: steelmanned & refuted (`zkage/` + the brief)
`zkage/` builds the strongest cryptographic case for age verification (a real ZK proof of age≥18) **to demonstrate that even it must be opposed** — predicate + presence/absence leakage, issuer centralization, futility-under-breach, honeypot, and the legitimization trap. Read [`research/age-verification-abolition.md`](research/age-verification-abolition.md); formal: [`models/z3/ageverif_futility.py`](models/z3/ageverif_futility.py). Run: `python3 zkage/zk_age_proof.py`.
