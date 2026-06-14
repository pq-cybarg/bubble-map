# Temporal-web bridge facts (1998 → 2026) — sources for the meta-graph

*Built from `research/temporal-bridges.json` — the source facts behind `models/graph/temporal_web.py` / `data/temporal_web.json` (the betweenness "weavers" of the 1998→2026 meta-graph). Each fact graded **doc | assoc | struct**. Sensitive items (Epstein/Waters/threat-actor) are **documented-association only.***

> **What this is.** The structural patterns of this cycle are not new — they **bridge prior cycles** through recurring people, devices, and institutions. This block holds the **dated, sourced bridge facts** that the temporal-web model uses to compute which actors/structures connect 1998, 2001, 2008, 2023, and 2025–26. It is a **chronology of rhymes**, graded — not a claim that the same hands ran each cycle.

## The bridge facts (representative; full set in the JSON)
- **`summers-bridge` (doc):** Larry Summers was **Treasury Secretary during the 1999 Glass-Steagall repeal** (GLBA, signed Nov 12 1999); **joined OpenAI's board Nov 2023**; **resigned the board (and a Harvard role) Nov 19 2025** after the House Oversight Committee released Epstein correspondence. One person bridging the 1999 deregulation and the 2023–25 AI core. *Documented chronology — not a claim of intent.*
- **`ltcm-1998` (doc):** Sept 23 1998 — 14 banks/brokers put **$3.625B into LTCM** in a Fed-facilitated private rescue; LTCM had ~$5B equity on >$125B borrowed (~30:1) — the **"too-interconnected-to-fail" template** that recurs in 2008 and after.
- **`enron-spe` (doc):** Enron (collapsed Dec 2001) used **off-balance-sheet SPEs (LJM1/2, Chewco, JEDI, Raptors) + mark-to-market accounting** to hide debt and book future/artificial profit — the **structural ancestor of today's AI SPVs** (Stargate/Hyperion) and RPO-as-revenue.
- Further bridges (graded): the GLBA→2008 deregulation chain (`macro-history-dereg-manipulation`), the vendor-financing rhyme (dotcom → NVIDIA), and the recurring-institution weavers the betweenness model surfaces.

## How it's used (and bounded)
`temporal_web.py` computes **betweenness centrality** over the dated bridges to find the actors/structures that **connect the most eras** — the "weavers." Crucially:
- The output is **structural** (who/what recurs), graded **doc/assoc/struct**;
- **Sensitive personal threads are documented-association only** and are **excluded from the formal proofs** (they live here and in `spec-network-overlay` / `spec-crypto-sec-epstein`, not in the SCC/Z3 core);
- Recurrence is a **rhyme, not a proof of continuity of intent.**

*Sources: [CNBC — Summers/Epstein/OpenAI](https://www.cnbc.com/2025/11/19/larry-summers-epstein-openai.html); [Fed History — LTCM near-failure](https://www.federalreservehistory.org/essays/ltcm-near-failure); Enron SPE chronology (Wikipedia/uncontested). See `macro-history-dereg-manipulation`, `spec-network-overlay`.*
