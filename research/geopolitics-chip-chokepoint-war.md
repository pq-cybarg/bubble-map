# The two-sided chip-chokepoint war — Western equipment vs China's materials (and who's racing to break it)

*Web-verified 2026-06-11. Structured + sources: `geopolitics-chip-chokepoint-war.json`. Overlay — evidence-graded, excluded from the proofs. Sits upstream of [[geopolitics-taiwan-silicon-shield]]; connects to [[geopolitics-allied-intel-nodes]], [[macro-critical-minerals-equities]], `defense_chokepoint`, [[macro-crqc-quantum-landscape]].*

Upstream of Taiwan's fabs the chain is a **two-sided chokepoint war**: the West controls the **equipment** to make advanced chips and denies it to China; China controls the **raw materials** the West's fabs and weapons need and retaliates. Each side holds a gun to the other's supply chain. But — per the caution the question rightly raises — the chokepoint is **sticky, not permanent**: China and others are racing to break it, and the deepest moat is the one nobody can fully see.

## Side 1 — the Western equipment chokepoint (NL + DE + JP)
- **ASML's EUV monopoly (Netherlands):** the **sole** maker of EUV lithography — ~100% of EUV, no competitor — and EUV is required below ~7nm. ~**80% of ASML's EUV sales go to TSMC** (**fact**).
- **Zeiss optics (Germany):** ASML's EUV optics come from a *single* partner, Zeiss SMT; ~**80% of all microchips** are made with Zeiss optics + ASML systems. **High-NA EUV** enters series production in 2026 — an even narrower chokepoint. A monopoly resting on a monopoly.
- **Export controls + a reported kill switch:** since 2019 the US + Netherlands have barred advanced EUV (and increasingly immersion DUV) from China — "the single most consequential decision in protecting Western AI dominance"; 2026 curbs tightened further. ASML reportedly built a **remote kill switch** into TSMC's EUV machines, able to disable them via a maintenance update if China invades (**contested** — reported, not confirmed). Implication: seizing Taiwan would *not* hand China working EUV — but it would brick the world's leading edge.
- **Japan** adds a parallel chokepoint: etch/deposition tools (Tokyo Electron) and **>50% of 14 critical materials** (~75% of high-end photoresist).

## Side 2 — China's materials counter-leverage
- **The bans:** 3 Dec 2024 China banned **gallium, germanium, antimony** + superhard materials to the US (direct chip-control retaliation); 4 Apr 2025 added **seven heavy rare earths** (Tb, Dy, Sm, Gd, Lu, Sc, Y) — the magnets for motors and weapons.
- **Extraterritorial reach (9 Oct 2025):** modeled on the US Foreign Direct Product Rule — **any** foreign product with **≥0.1% Chinese-origin rare earths**, or made using Chinese processing tech, needs a Chinese license. Beijing extended its writ across the whole global chain (**fact**).
- **The truce:** Nov 2025 China *suspended* the US-focused controls until **27 Nov 2026** — but the architecture remains and is reinstatable (same "suspend but keep the gun loaded" pattern as the antimony ban in [[macro-critical-minerals-equities]]). It bites because China processes ~90% of REE/antimony and most gallium/germanium/graphite.

## Can the chokepoint be broken? China's indigenous push + alternatives + the tacit-knowledge wall
This is where it would be wrong to treat the Western lock as permanent — the question's caution is correct.

- **China's multi-track EUV effort (graded — reported/projected):**
  - **LDP-EUV** (Huawei + SMEE + Harbin Institute): a **Laser-Induced Discharge Plasma** EUV source reportedly hit **100–150 W in mid-2025** (vs ASML's 250W+ for high-volume manufacturing) — enough for "first-light" testing of 5nm-class logic. A Shenzhen "whole-of-nation" prototype coordinated with **SiCarrier** is reportedly in testing. *Reported* timelines (SMIC "EUV-refined" chips ~late 2026; 2nm by 2028; parity "by end of decade") are **aggressive and contested** — treat as ambition, not delivery.
  - **SSMB-EUV** (Tsinghua): a radically different path using a **steady-state-micro-bunching particle accelerator (synchrotron)** to generate a continuous high-power EUV beam — a potential leapfrog if it works, years out.
  - **DUV multipatterning:** SMIC already ships **7nm** (Huawei Mate 60) without EUV via DUV multipatterning — at a yield/cost penalty; the near-term workaround.
- **Alternative approaches (anyone, graded):** **Canon Nanoimprint (NIL)** — its FPA-1200NZ2C "stamps" patterns at ~14nm linewidth (~5nm-node), with a path toward ~10nm (~2nm-node), at **~1/10th the cost of an EUV scanner** and ~90% less power; China is chasing NIL as an ASML alternative (300+ firms mobilized, first domestic NIL tool shipped). **But** the consensus (SemiAnalysis, Bits&Chips) is NIL **won't rival EUV at the leading edge for the foreseeable future** — defectivity/overlay/throughput problems "without a clear way forward." **Silicon photonics / photonic computing** is floated as a longer-shot *bypass* (compute without bleeding-edge transistors) — **speculative**. The quantum/**CRQC** frontier ([[macro-crqc-quantum-landscape]], [[macro-quantum-computing]]) has its *own* manufacturing bottlenecks (cryogenics, error correction, qubit fab) and is not a near-term substitute.
- **The deepest bottleneck — tacit knowledge & trade secrets (the "unknown unknowns"):** the hardest moat isn't a machine you can reverse-engineer; it's the **undocumented institutional know-how** — process recipes, yield engineering, metrology, the thousands of supplier-ecosystem relationships, and decades of embodied expertise inside ASML, Zeiss, TSMC, and the Japanese materials houses. **Espionage and reverse-engineering get you blueprints, not the recipe.** This is *why* the chokepoint is sticky (years, not months) — and also why it is **not permanent**: tacit knowledge erodes under a sustained, well-funded "whole-of-nation" effort, talent poaching, and time. The honest read: the West's lead is real and measured in **years**, not in a permanent switch; China is climbing the curve on multiple tracks at once, and at least one (SSMB) could change the slope. *Anyone claiming the chokepoint is permanent — or that China is one breakthrough away — is overstating a genuinely uncertain race.*

## The two-sided deterrence, and the full stack
Mutual chokepoint deterrence: the West can deny China the machines to **make** advanced chips (and reportedly kill-switch the ones in Taiwan); China can deny the West the materials to **run** its fabs and build its weapons. Each "suspension" is a truce over a loaded weapon, not disarmament — and both sides are racing to make the other's chokepoint obsolete.

The complete stack — each step in a different jurisdiction, most a single point of failure, all assumed open at once by the machine-verified AI loop:

| Step | Chokepoint holder |
|---|---|
| Raw critical minerals (REE/antimony/gallium) | **China** (~90%) |
| Refined chip materials (photoresist/wafers/gases) | **Japan** (>50% of 14) |
| Lithography (EUV) + optics | **Netherlands** (ASML) + **Germany** (Zeiss) |
| Deposition/etch + EDA | **US** / **Japan** |
| Fabrication (≤7nm) | **Taiwan** (TSMC ~95%) |
| Advanced packaging (CoWoS) | **Taiwan** |
| HBM | **South Korea** (SK Hynix/Samsung) |

Seven steps, seven jurisdictions, one assumption: that they all stay open, and cooperative, simultaneously.
