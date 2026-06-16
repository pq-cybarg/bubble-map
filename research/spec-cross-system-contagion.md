# Cross-system contagion & interconnection — the channels between the bubbles

*Built 2026-06-14. Synthesis of the cited blocks plus primary reconciliations. All edges here are **structural overlay** (directional transmission links, no cycles) — they enrich the bubble map and connector analysis but are **excluded from the SCC / Z3 / TLA+ proofs**, which run on the financial layer only.*

> Every other block maps one subsystem. This one draws the **edges between them** — the channels along which a shock in one bubble propagates to the rest. Each channel's links are documented facts; the **firing** of the cascade is contingent (and, for the Fed channel, interruptible). It also **canonicalizes** three figures that appear in more than one form across blocks, and states the highest-value **open questions** plainly so they aren't mistaken for settled facts.

## 1. Crypto → Treasury → banks → AI marks *(the missing cascade)*
Stablecoins, Treasuries, banks, and AI capex are **one system, not four**. Mechanism: stablecoin reserves (Tether ~$140B+, USDC) are **T-bill-concentrated** → a peg break / redemption run forces a **T-bill fire-sale** → **front-end yields spike** → the rate move **deepens banks' unrealized HTM losses** (already ~$300B+ and re-widening, [[macro-bank-htm-marks]]) → stressed banks **pull credit / raise equity** → the **marginal lender to the AI/data-center buildout retrenches**, pressuring the very marks the core depends on ([[fin-ai-depreciation-debttrap]]). Each link is documented; the cascade firing depends on a peg break. *Fact (links) + contingent (firing).* New edges: `Stablecoins→US_Treasuries`, `Tether→US_Treasuries`, `US_Treasuries→US_Banks`, `US_Banks→SINK_lenders` (the WLFI↔Binance ~87% USD1 custody concentration is already edged `Binance→World_Liberty_Financial` in [[spec-exchanges-asia]]).

## 2. Yen carry → the AI core *(the hidden funding leg)*
Cheap **yen** is the world's funding currency; as **JGB yields escape yield-curve control** (0% → ~2.66% in 2026), crowded carry-funded longs unwind ([[macro-carry-trades]]). **SoftBank** — a major OpenAI/Stargate financier — is **yen-funded and yen-refinancing-exposed**, so a Tokyo rates move is an **AI-core funding shock** arriving exactly as its commitments peak. *Fact (mechanism) + contingent (magnitude).* New edges: `SoftBank→Stargate`, `SoftBank→OpenAI` (carry-exposure overlay).

## 3. Chip ↔ private credit *(a second circular structure)*
Chip vendors are now **infrastructure financiers**. **Broadcom** (custom XPUs for Google/Meta/OpenAI/Anthropic + two unnamed customers — analyst-flagged **Apple**/ByteDance) anchors a **~$35B+ XPU compute-financing platform with Apollo/Blackstone** (already edged `Apollo_Blackstone→Broadcom` in [[fin-google-amazon-anthropic-meta]]); Meta funds Hyperion via a **Blue Owl** SPV. **Private credit** ([[macro-cre-privatecredit]] / [[macro-private-credit-marks]]) thus finances the data centers that buy the chips — a second circular structure beside the equity loop, and a second place a private-credit mark-down would bite. New edge: `Apple→Broadcom` (unconfirmed, *weak*) ties Apple capex into that stack.

## 4. China leverage, made legible *(node merge)*
Merging the fragmented China nodes makes one actor's **concentration of chokepoints** visible: the same China node gates **rare earths/magnets + antimony** to the defense-industrial base ([[spec-rare-earth-statecraft]]), is the prime suspect in **Baltic/Taiwan undersea-cable cuts** and the **Royal Mint Court comms-siting** exposure ([[geopolitics-cables-space-layer]]), and runs the **export-licensing faucet** ([[geopolitics-chip-chokepoint-war]]). *Fact (each chokepoint) + labeled interpretation (concentration as leverage).* New edge: `China→Defense_Primes`.

## 5. The Fed circuit-breaker *(the missing node)*
Every cascade above can be **interrupted or amplified** by Fed policy, so any unwind thesis that assumes policy inaction is incomplete. If the crypto→Treasury→bank cascade fires, the playbook is a **BTFP-style facility** (banks borrow at par, suppressing the HTM forced-sale spiral) plus **QE / cuts** to cap the yield spike. This does not prevent the loss — it **socializes and delays** it — but it changes the timing and form of any unwind. Read the trigger panel ([[spec-unwind-timing]]) against this reaction function. New edges: `Federal_Reserve→US_Banks`, `Federal_Reserve→US_Treasuries`.

## The Fed reaction-function decision-tree *(added 2026-06-16, #57)*
The circuit-breaker node, made formal: given **which** cascade fires, what the Fed does, in what order, gated by what. *Tools + precedents are fact; thresholds + branch model are labeled. The binding constraint is the inflation gate — the Z3 "no single rate fits the targets" ([[macro-fed-trap-regional]]) rendered as a tree.*

| Trigger (symptom) | Tool order (cheapest→most) | Threshold | Precedent | Cost |
|---|---|---|---|---|
| **B1 Funding-market stress** — repo/front-end bill yield spikes (stablecoin run dumps bills; basis-trade unwind clogs repo) | SRF → expand → outright bill buys | SOFR-IORB blows out | 2019 repo; SRF permanent 2021 | low-signaling, fast; doesn't touch solvency |
| **B2 Bank solvency / deposit run** — yield spike reopens HTM (~$300B+); SVB-mode realization | discount window → **BTFP-style par lending** → FDIC systemic-risk exception | a bank fails / uninsured outflows accelerate | **BTFP Mar-2023** | **socializes** the mark; moral hazard |
| **B3 Treasury-market dysfunction** — dealers can't absorb the fire-sale | **QE restart** → SLR/eSLR relief (ties [[macro-history-dereg-manipulation]] #77) | liquidity breaks / failed-auction tail | Mar-2020 dash-for-cash + SLR exclusion | balance-sheet expansion; SLR lever already half-pulled (eSLR cut Nov-2025) |
| **B4 Broad credit contraction / recession** — banks pull AI credit; unemployment rises | **rate cuts** → guidance | labor breaks (U-3; cf. [[macro-gig-labor]] hidden slack) | every easing cycle | slowest; collides with the inflation gate |

**The inflation gate (the binding constraint).** With CPI ~4.2% ([[macro-official-data-integrity]]), easing to backstop the cascade reignites inflation while holding to fight inflation lets the cascade run — the Fed can't cap the yield spike, protect bank capital, *and* hold inflation with one rate (the Z3 UNSAT result). So the reaction function is **asymmetric**: liquidity tools **B1–B3** fire **fast** (framed as "plumbing, not stimulus"); the rate-cut lever **B4** is inflation-gated and fires **slow**.

**Terminal insight.** The Fed never *prevents* the loss in any branch — it **socializes and delays** it (B2/B3) or **trades inflation** for it (B4). So the unwind's timing/form is set by **which constraint binds first**: a plumbing break (fast, inflationary), a solvency break (par-lending, moral hazard), or a labor break (cuts, gated). Any unwind thesis assuming policy *inaction* is incomplete; any assuming a *clean rescue* ignores the inflation gate.

## Cross-file reconciliations (canonical values)
- **NVIDIA → OpenAI.** The "$100B" was a **milestone-linked letter of intent** (22 Sep 2025), later called "never a commitment" by Huang; the **closed** figure is **$30B direct equity**, part of OpenAI's ~$110B round at a **$730B pre-money** valuation (27 Feb 2026; SoftBank +$30B, Amazon +$50B). Canonical in [[fin-nvidia-openai]].
- **Oracle RPO.** **$455B** at end of **Q1 FY2026** (quarter ended 31 Aug 2025; reported 9 Sep 2025), **+359% YoY** (vs ~$99B a year earlier). The **$317B** is the **prior quarter** (Q4 FY2025) — so $317B→$455B is the QoQ step and +359% is the YoY rate; no discrepancy once periods are labeled.
- **Anthropic Series G.** Closed **12 Feb 2026** at **$350B pre / $380B post**; the round **expanded from a ~$20B target to $30B** on demand (led by GIC and Coatue). "$350B/$380B" = pre vs post; "$10–30B" = target vs final — one event, not conflicting rounds.

## Open questions (genuine gaps, with what resolves each)
- **Cancelable-deal terms** (SpaceX↔Google $920M/mo; OpenAI↔Oracle/CoreWeave) — contracts / commitment disclosures; sets how fast the robust SCC sheds nodes.
- **Google's contingent $30B in Anthropic** — what milestones gate it (a round disclosure); a miss could collapse the second funding ring.
- **CoreWeave debt maturities** (~$21.4B; $6.7B current) — 10-K MD&A; the 2026–27 bullets as the Microsoft revenue share falls below 50%.
- **Broadcom's two unnamed XPU customers** — Apple and/or ByteDance? (export-control question) — earnings/capex confirmation.
- **SoftBank's yen refinancing need** 2026–27 vs its AI commitments — debt schedule; sizes the carry-unwind transmission.

## What is NOT asserted
- These transmission edges are **not** new money-flows and do **not** enter the formal proofs.
- **No** cascade is asserted to fire — each is a documented mechanism with a contingent (and possibly Fed-interrupted) trigger.
- China-concentration is **leverage/exposure**, not an assertion of intent to use every chokepoint.
- The reconciliations correct period/stage/labeling confusion; they allege no error by any source.

---
*Sources: [NVIDIA–OpenAI 10GW partnership](https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems), [Fortune — Huang: "never a commitment"](https://fortune.com/2026/02/02/jensen-huang-nvidia-ceo-on-openai-investment-never-a-commitment/), [Oracle Q1 FY2026 results](https://www.oracle.com/news/announcement/q1fy26-earnings-release-2025-09-09/), [Anthropic — $30B Series G at $380B post](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation), [TechCrunch — Anthropic Series G](https://techcrunch.com/2026/02/12/anthropic-raises-another-30-billion-in-series-g-with-a-new-value-of-380-billion/).*
