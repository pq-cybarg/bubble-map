# The AI power & grid bottleneck — transformers, turbines, interconnection, fuel

*Web-verified 2026-06-11. Structured + sources: `macro-ai-power-grid-bottleneck.json`. Overlay — evidence-graded, excluded from the proofs, but mirrors the machine-proven `power_adequacy` P1 (AI power demand > supply through 2028). Connects to `energy_web`, [[fin-ai-depreciation-debttrap]], [[geopolitics-russia-energy-arctic]] (HALEU), [[fin-coreweave-oracle]].*

The AI build is **power-constrained, not just capital-constrained.** ~**$650B+** of hyperscaler 2026 capex (Alphabet/Amazon/Meta/Microsoft) collides with **multi-year lead times** for the physical grid — and **nearly half of US data-center projects may be delayed or cancelled** due to grid + component bottlenecks. The money isn't the binding constraint; the grid is.

## The bottlenecks
- **Transformers.** High-voltage transformer lead times went from **~50 weeks to ~127 weeks** (some critical units **3–4 years**); HV substations **3–5 years**; the global shortage is expected to last **to at least 2029**. Domestic supply is short, so developers **import — including from China**, adding a geopolitical-supply risk to the grid itself.
- **Gas turbines.** The "big three" (GE Vernova, Siemens Energy, Mitsubishi) are effectively **sold out for years**; new firm gas capacity pushes toward **~2028–2029** — the same window as the demand.
- **Interconnection.** US interconnection queues delay projects for years; utilities warn of **regional capacity shortages as early as 2026.**
- **Fuel.** Both "clean firm power" answers have chokepoints: **nuclear/SMR fuel (HALEU) is ~Russia-gated** ([[geopolitics-russia-energy-arctic]]; `power_adequacy` P2 UNSAT to ~2029), and gas needs turbines + pipelines that are themselves backlogged.

## The workaround — "Bring Your Own Power"
Because the grid can't connect them in time, hyperscalers go **BYOP** — behind-the-meter on-site generation (gas turbines, fuel cells, **nuclear restarts** like Three Mile Island, SMRs). This bypasses the HV-transformer + interconnection bottleneck, but (a) still needs **turbines/fuel that are backlogged or gated**, and (b) moves the AI build **off the regulated grid into self-supplied power** — privatizing the energy chokepoint.

## Most-stranded ranking *(added 2026-06-16, #50)*
The tell, on the record — Nadella: *"you may actually have a bunch of chips sitting in inventory that I can't plug in."* The binding constraint flipped from GPUs to **power and warm shells**. Ranking by exposure to *stranding* — announced compute vs **secured firm power**, worst for those who **lease and don't self-generate**:

| # | Who | 2026 capex | Secured firm power | Stranding signal |
|---|---|---|---|---|
| **1** | **Oracle / Stargate** | ~$50B | ~10 GW claimed, **>90% partner-funded**; **leases, doesn't generate**; Abilene off-grid gas via Crusoe | **scrapped 600 MW** Abilene expansion; single-customer (OpenAI); thinnest cushion |
| **2** | **CoreWeave / neoclouds** | ~$30–35B | only **850 MW active vs 3.1 GW contracted** (energization gap); pure lessee | capex 100% tied to contracts + circular Nvidia financing |
| **3** | **Microsoft** | ~$190B | TMI/Crane **835 MW** nuclear PPA (~2028) | **strongest evidence** — Nadella + ~2 GW LOI walk-away + 1.5 GW self-build freeze; but best balance sheet |
| **4** | **Meta** | ~$125–145B | **most self-reliant**: Hyperion funds **10 Entergy gas plants >7 GW** + 2.5 GW renewables | huge *concentrated* single-site bet ($27B); risk is execution, not procurement |
| **5** | **Amazon/AWS** | ~$200B | best **matched**: Talen/Susquehanna **1,920 MW** nuclear to 2042, front-of-meter 2026 | customer-committed capex — low near-term stranding |
| **6** | **Google** | ~$175–185B | efficient TPUs + strong sheet; clean-power **long-dated** (Kairos SMR ~2030; fusion early-2030s) | lowest near-term stranding |

**The split is balance-sheet + self-generation.** The lessees who don't generate (Oracle, CoreWeave) strand worst; the cash-rich self-generators (Meta gas, Amazon nuclear) carry *execution* risk, not *procurement* risk.

## Idle-GPU cost model *(added 2026-06-16, #50)*
What an idle GPU costs while it waits for power. *Arithmetic is fact; input ranges sourced; the honest ~3-yr economic life is the contested assumption ([[fin-ai-depreciation-debttrap]]).*

- **Inputs:** GB200 NVL72 rack **~$3.0M / 72 GPUs → ~$41,700/GPU**, **~120–132 kW/rack**; H100 ~$30k; rental (opportunity cost) ~$3/GPU-hr neocloud (~$7/hr hyperscaler on-demand); a **100k-GB200 cluster needs ~150–180 MW** for the GPUs alone.
- **Carrying cost (accrues whether it runs or not):** at an honest 3-yr life + 10% WACC, **~$49.5/GPU/day** (~$38 depreciation + ~$11 carry) → **~$3,562/day per idle rack.** *(At the 6-yr accounting life it books only ~$30/day — the ~$19/day gap **is** the depreciation trap, made physical.)*
- **A stranded 100k-GB200 cluster** (~1,389 racks, **~$4.17B** of silicon): **~$4.95M/DAY (~$1.8B/yr)** in pure carry while unpowered — **up to ~$12M/day** including ~$7.2M/day forgone rental. A 100k-H100 cluster ≈ $3.56M/day.
- **The point:** power arrives on a **3–5-yr** clock; GPUs decay on a **~2–3-yr** clock. A cluster that lands before its power **burns ~$5M/day on a $4.2B asset that is aging out the whole time it waits.** Nadella's "chips I can't plug in" is that loss being taken in real time.

## Why it matters to the map
1. **Physical mirror of the financial thesis.** The $650B+ capex and the **$1.4T** of OpenAI compute commitments ([[fin-microsoft-openai]]) assume power on a **3–5-year delivery clock** the 2026–2027 buildout can't meet — so a large share of *announced capacity* is, like the marks, **a promise ahead of deliverable substance.**
2. **It compounds the depreciation trap** ([[fin-ai-depreciation-debttrap]]): GPUs that economically age in ~2–3 years, sitting idle waiting for power they can't get, are **stranded, fast-depreciating capital** — debt-financed assets dying before they're energized.
3. **It hands leverage** to whoever controls **turbines** (a few firms), **transformers** (a strained global supply incl. China), and **fuel** (Russia/HALEU, gas) — **the energy chokepoint behind the compute chokepoint.** The AI build can't buy past the grid any faster than it can buy past Taiwan.
