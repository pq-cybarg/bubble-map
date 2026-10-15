# The AI-bubble skeptic / short case

*As of 2026-10-15. Companion to `spec-ai-bubble-skeptics.json`. This is the deliberate adversarial check on the AI-capex map - the steelman of the bear case, with its own honest caveats. Structural overlay only; the financial proof core is untouched. Grading is per-claim: fact | caveat | interpretation.*

## Why this block exists

The rest of the corpus maps the AI-financing machine in detail. Good practice is to steelman the case that it is *wrong* - that the buildout is a bubble - and to grade that case as honestly as the bull case. The point is not to assert the skeptics are right; it is to record who is betting against it, what they cite, and where their argument is weak.

## The short: Michael Burry / Scion (fact, with caveats)

Scion's Q3-2025 13F (filed around November 2025) disclosed put options on about **5M Palantir shares (~$912M notional)** and **1M NVIDIA shares (~$187M notional)** - together roughly **80% of the disclosed book**. Burry later detailed and expanded the structure (NVIDIA puts struck $110 expiring 2027; Palantir puts struck $100 for December 2026 and $50 for June 2027, plus a direct short) and added shorts on **Oracle**, the **SOXX** semis ETF, and **QQQ**.

His stated thesis: AI capex is a dot-com-fiber-style overbuild, and hyperscalers **understate depreciation by extending the useful life** of compute that runs on a 2-3 year product cycle - which he called "one of the more common frauds of the modern era."

**The honest caveats, recorded:**
- 13F put **notional is not capital-at-risk** and can be a hedge, not a naked directional bet.
- The positions took **immediate paper losses** as both stocks kept rising after the filing date.
- Burry's **timing record is mixed** - his 2021 Tesla puts preceded a doubling of the stock.

## The analytical frame: David Cahn's "$600B Question" (fact, with a crucial caveat)

Sequoia's David Cahn works backward from NVIDIA run-rate revenue (x2 for GPUs being ~half of datacenter total cost of ownership, x2 again for a ~50% end-user gross margin) to the revenue the buildout must eventually produce. That required figure went from a "$200B question" (2023) to "$600B" (2024) to an implied **~$800B+ annual gap by 2026**, with Allianz pegging the capex-vs-revenue divergence at ~46% versus ~32% in the 2001 telecom bubble.

**The caveat that is usually dropped:** Cahn explicitly framed this as a **time-lag, not a bubble**, and stayed long-term bullish. His argument is that the revenue will come but the capital is running ahead of it - the question is who survives the gap, not whether it all collapses.

## The demand-side evidence: MIT "GenAI Divide" (fact)

MIT's Project NANDA "State of AI in Business 2025" (August 2025) found that about **95% of enterprise GenAI pilots delivered zero measurable P&L impact** despite ~$30-40B of spend; only ~5% created significant value, with external vendor tools succeeding about twice as often as internal builds.

## The genuine tension (both true at once)

Real enterprise AI consumption **is** accelerating (spend growth, budgets exhausted early) **and** realized ROI is **weak** (most pilots show no P&L impact). The gap between heavy spending and demonstrated value is the single most fragile point in the edifice - and it is exactly what the capex-vs-revenue and depreciation arguments target.

## How it wires into the map

The skeptic case is modeled as one concept node, `AI_Bubble_Skeptic_Case`, with documented bearish bets/claims pointing at the entities they target: NVIDIA, Palantir, and Oracle (Burry's disclosed shorts), AI data centers (the depreciation + MIT-ROI critique, which maps onto the existing `fin-ai-depreciation-debttrap` Z3 proof), OpenAI (Cahn's revenue-gap frame), CoreWeave (where the market is already pricing part of the bear case), and the AI-compute credit layer (where the skeptic case converges with the BIS/IMF official-sector warnings and the robustness/off-balance-sheet findings). Individuals are named in the graded edge notes rather than as nodes.

## Cross-references

`fin-ai-efficiency-counter-thesis` (the DeepSeek/Jevons efficiency challenge - the *other* bear argument) | `fin-ai-depreciation-debttrap` (the depreciation/duration-mismatch proof Burry's critique maps onto) | `spec-oracle-ai-credit-lynchpin`, `spec-coreweave-credit-stress-2026` (named credit-stress cases) | `spec-offbalancesheet-ai-financing` + the core-robustness certificate (the structure the skeptics say is fragile) | `spec-blankfein-ai-2008-analogy` (a top-banker drawing the same analogy).
