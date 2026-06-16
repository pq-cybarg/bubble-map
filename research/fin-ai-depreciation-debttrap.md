# The depreciation & duration-mismatch trap: useful-life as the fifth self-marked number

*Compiled 2026-06-10, triggered by the [justdario.com](https://justdario.com/2026/06/the-unhappy-ending-of-the-whole-ai-dream/) piece "The Unhappy Ending of the Whole AI Dream." Formalized in `models/z3/depreciation_trap.py`. Overlay claims graded `fact | contested | weak | unsupported`; the Z3 result is a proof. Cross-refs `spec-sec-filings-primary`, `macro-bank-htm-marks`, `reflexive_marks`, `self_marked_value`, `spec-unwind-timing`.*

The article's checkable claims **verify against primary data**, and it supplies a mechanism this project had not yet formalized: **AI compute depreciates faster (~2–3 yr) than the debt and leases financing it (5–19 yr).** So even if the promised revenue arrives, *the asset is gone before the loan is repaid* — and the "useful life" assumption that hides this is the **same defect** as the machine-proven self-marked-value theorem, applied to depreciation. Useful life is the **fifth self-marked number**.

## What the article argues (and how it grades)
justdario's thesis: the US AI buildout is **debt-financed, fast-depreciating, winner-take-all capital waste with no graceful exit** — abandoning triggers a Meta-metaverse-style stock crash, continuing demands perpetual capital, and (unlike Meta's *cash*-funded metaverse) the **debt** impairs the balance sheet and legacy operations when it unwinds; QE won't rescue it because debt service eats the cash flow. This is **strongly aligned** with the project's machine-proven circular core + insolvency-at-zero-inflow, and adds the depreciation and asset-light→asset-heavy angles (**fact**: the alignment). The "inevitable collapse" framing is the author's — this project proves **structure, not date** (`spec-unwind-timing`).

## Verified primary claims
**Burry's depreciation critique (fact, Nov 2025).** Hyperscalers (Meta, Amazon, Microsoft, Google, Oracle) depreciate Nvidia GPUs over **5–6 years** when the true economic life is closer to **2–3 years** — **~$176B of understated depreciation / overstated profit 2026–2028**, ~$50–60B/yr if the true life is 3 not 6. Concrete instances: **Meta** raised most server/network useful life to **5.5 yr**, cutting depreciation ~**$2.3B over 9 months of 2025**; **Microsoft**'s ~**$17B** GPU purchases booked over 6 yr instead of 3 → ~**$2.9B/yr** earnings overstatement. The consensus read: *"probably not fraud, but almost certainly optimistic estimates that will require adjustment"* — i.e., **useful life is a discretionary assumption** (that part is fact; the $176B is Burry's estimate, **contested**).

**Oracle's asset-light → asset-heavy pivot (fact, FY2026 8-K).** Free cash flow **negative ~$23.7B**, ~**$50B** capex, **>$108B** debt (plus **$30B** raised early 2026 in IG bonds + mandatory convertible preferred). The **$523B RPO** rests **>half on one customer** (OpenAI via the ~$300B Stargate deal); $75B of the big AI contracts are customer-prepaid or customer-supplied GPUs. And **$248B of additional datacenter/cloud leases of 15–19-yr term**, substantially **off the balance sheet** — long-tenor financing against ~3-yr-life GPUs. CNBC's framing: *"Oracle is building yesterday's data centers with tomorrow's debt."*

**Geopolitical color (weaker).** China's ~**$295bn** state-directed AI buildout (80%+ domestic semiconductors) — roughly one year of Google's spend (**contested**, single-source figure). US operational datacenters reportedly exceed all other countries combined / ~10× Germany (**weak**, magnitude unverified here).

## The cluster's unified useful-life table + forward rate *(added 2026-06-15, #54)*
A per-company audit of the disclosed server/GPU useful life and its earnings effect:

| Company | Server/GPU useful life | Key change | Disclosed effect |
|---|---|---|---|
| **Microsoft** | 6 yr (was 4–5) | FY23 (eff. Jul 2022) | ~**$3.7B** FY23 benefit (CFO guide) |
| **Alphabet/Google** | servers 6 yr; network 6 yr | Jan 2023 | ~**$3.9B** FY23 lower depreciation / ~$3.0B higher net income |
| **Amazon/AWS** | 6 yr (2022) → a subset **back to 5 yr** (Jan 2025) | **reversal Jan 2025**, cites AI/ML pace | ~**$700M** FY25 op-income hit + ~$920M early-retirement (~$1.3B total) |
| **Meta** | ~**5.5 yr** (4 → 4.5 → 5 → 5.5) | Jan 2025 | ~**$2.9B** FY25 lower depreciation |
| **Oracle** | ~5 yr | 2023 | central to the OCI-margin / earnings-quality debate |
| **CoreWeave** | GPUs **6 yr** | since 2023 | shifting to 4 yr adds ~$315M/qtr → **flips to a loss** |
| **Nebius** | GPUs **4 yr** | current | ~50% higher depreciation rate than CoreWeave |
| **Lambda** | GPUs ~5 yr | current | between the two |

- **The Amazon reversal is the tell.** Amazon is the **only** hyperscaler to publicly *cut* a useful-life category (6→5 yr, Jan 2025), its filing citing *"an increased pace of technology development, particularly in … artificial intelligence and machine learning"* — an **inside-the-filings admission** that the extend-life / harvest-profit trend is reversing.
- **The CoreWeave-vs-Nebius natural experiment.** Identical neocloud business models, GPUs over **6 yr (CoreWeave) vs 4 yr (Nebius)** — a ~50% depreciation-rate gap from the useful-life *choice* alone; at 4 yr CoreWeave's reported operating profit flips negative. The cleanest demonstration that useful-life *manufactures* profitability.
- **Burry/Scion (Nov 2025), graded.** ~**$176B** understated depreciation 2026-2028; Oracle earnings overstated ~**26.9%**, Meta ~**20.8%** by 2028; ~$1.1B notional Nvidia+Palantir puts (later wound down, fund closed). **Nvidia's rebuttal** (Kress: six-year-old A100s "still running at full utilization") vs Burry (utilization ≠ value; older chips far less power-efficient → continued use reflects scarcity, not retained value). **All changes are disclosed estimate changes (prospective)** — "fraud" is rhetorical/contested, not adjudicated.
- **The unified forward rate.** The cluster sits at a **~6-yr accounting life** for servers/GPUs while a defensible **blended GPU economic life is ~3–4 yr** (training-edge ~1.5–2 yr; inference tail ~3–4 yr) against Nvidia's ~annual cadence (Hopper→Blackwell→Rubin). Marking GPU-heavy fleets from ~6 yr to ~3–4 yr raises annual depreciation **~50–100%** on the affected base. **Key tension:** the accounting life is set on *blended* fleets (incl. 15+-yr data-center shell/power); the GPUs are the fast-decaying subset the blended life **masks** — exactly the D2/D4 mechanism below.

## The mechanism, formalized (`models/z3/depreciation_trap.py`)
- **D1 (SAT)** — a long *assumed* life makes the same asset print a profit: `profit = revenue − opex − capex/life`. The life is the **free parameter**.
- **D2 (UNSAT)** — the true, shorter economic life **strictly lowers** profit; the overstatement is structural, = `capex·(1/Lₜᵣᵤₑ − 1/Lᵦₒₒₖ)` ≈ **$2.9B/yr** for one MSFT-like GPU tranche, **~$176B** industry-wide 2026–2028.
- **D3 (UNSAT)** — the **duration mismatch**: when asset life (~3-yr GPUs) < financing tenor (5–7-yr bonds, 15–19-yr leases), equity cannot stay whole — there is an interval with a **live debt and a dead asset** (Oracle's $248B of 15–19-yr leases).
- **D4 (UNSAT)** — **depreciation is only timing**: no life choice avoids *both* near-term losses *and* a retirement writedown; a stretched life just defers the loss and forces a catch-up when the asset is retired.

## Why this matters to the map
Useful life joins **HTM cost, AI fair-value marks, private-credit NAVs, and insurance captive marks** as a **chosen number held above realizable until a forcing event** (`self_marked_value` U1–U4) — here the event is **retirement / obsolescence**, not a deposit run or an IPO. It is the cleanest answer to "but the AI firms have *real assets* backing the debt": the real assets **age out faster than the debt amortizes**, and the accounting that makes today's earnings look positive is **borrowing those earnings from a future writedown**. That is the formal spine under justdario's asset-heavy / no-graceful-exit thesis.
