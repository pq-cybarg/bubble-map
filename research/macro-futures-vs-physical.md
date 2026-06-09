# Futures vs physical, across exchanges, over time

*Web-verified 2026-06-08. Structured + edges + sources: `macro-futures-vs-physical.json`. **Source discipline:** much commodity commentary is perma-bull/manipulation-themed (SchiffGold, Sprott, DiscoveryAlert, 24/7) — used only for market-structure facts checkable against exchange/CFTC data. Documented enforcement is fact; blanket "suppression" is graded contested. Overlay, not used in the proofs.*

## The idea: price is made in paper, the good is delivered in physical
The headline commodity price is set in **leveraged futures** on one venue; the **deliverable** good trades on others (LBMA, LME, SGE/SHFE, DGCX, physical spot) at **different** prices. The divergence tells you where paper ≠ physical:
- **Backwardation** (spot > futures) — you pay up for metal *now* vs a promise later.
- **Cross-exchange premia** — the "same" asset priced differently in NY / London / Shanghai; arbitrage that won't close means metal can't move.
- **Registered vs open interest** — how many paper ounces claim each deliverable ounce.
- **Lease rates** — the cost to borrow physical.

## Gold & silver (2025–26) — *structure facts strong; suppression contested*
- **Silver backwardation** — reported first sustained instance **since 1980** (Dec-2025 ≈ $47.62 vs spot ≈ $47.67).
- **LBMA–COMEX premium** blew out to **>$2.50** (usually cents); London interbank physical seized, lease rates spiked.
- **COMEX futures-to-registered ≈ 4.2** paper claims per deliverable oz; much "eligible" metal is allocated (ETFs/industrial/banks), not freely deliverable.
- **Shanghai (SGE) ≈ 12–13% physical premium** over Western futures (Q4 2025+) — the East pulls physical.
- Earlier 2025: a **London→COMEX gold airlift** on US tariff/positioning fears.
- **Documented manipulation (fact):** JPMorgan paid **~$920M** (Sept 2020, CFTC/DOJ) for **spoofing** precious-metals + Treasury futures. *This is the factual anchor — manipulation occurred — but it was short-horizon spoofing, not proof of a decades-long price cap.*

## Copper (2025) — *strong (exchange + policy record)*
- **July 30 2025:** a US **50% tariff on copper semis** (cathode/concentrate exempt). Before the carve-out was known, the **COMEX–LME spread widened to >28%**, driving cross-exchange arbitrage and US pre-positioning.
- On the announcement, **COMEX copper fell >18% in a day — a record** — as the premium collapsed.
- **Venue split:** CME in contango (tariff distortion) while LME ran backwardation in nearby months; SHFE arbitrage transmits into LME–SHFE spreads.
- *Lesson:* one policy action blew a **>28% wedge** between two exchanges pricing the same metal — the "price" is venue- and policy-contingent, not a single physical truth.

## Oil — *structure fact; live differentials deferred to primary series*
Three benchmarks price "oil" differently: **WTI** (US light-sweet), **Brent** (waterborne), **Dubai** (Asia sour). Physical differentials (sulfur/density/freight) mean the futures benchmark isn't the barrel a refiner buys; curve shape (contango/backwardation) across the three signals tightness vs glut. Exact 2025 WTI–Brent–Dubai spreads belong to EIA/CME/DGCX/Platts series (`macro-oil-backwardation` holds the prior episode).

## Zero-trust conclusion
Treat the **futures print like a BLS headline** — the most *tradable*, not necessarily the most *physical*, number — and cross-check it against **backwardation, cross-exchange premia, registered/eligible stocks, lease rates, and the Eastern physical bid**. This complements the gold lens (`macro-gold-silver-reprice`): not only are nominal gains debasement, the metal price itself is a paper construct that physical periodically overrides.
