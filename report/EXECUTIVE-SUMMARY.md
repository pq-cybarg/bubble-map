# Executive Summary — Unmasking the AI Earnings Bubble

*Auto-generated 2026-06-11 from the live models. Full analysis: `report/UNMASKING.md` + `report/TEMPORAL-WEB.md`. Open `report/INDEX.html` for the dashboard. Each figure carries a source URL in the matching `research/*.json`. Checked by `models/audit.py` + `models/cross_review.py` (current: 0 flags).*

## The finding in one sentence
The AI build-out is a **circular capital loop** that books each firm's spending as another's revenue and is **solvent only while external capital keeps flowing**; it is **gated by physical chokepoints it cannot buy past** on the timeline (compute capital, China rare earths, Russian enrichment, the power grid); and it is **embedded in measurement and control layers** — official statistics, paper commodity prices, and the identity / surveillance / political-money rails — that determine whether it can be seen and questioned.

## Headline findings
1. **The self-marked-value machine (proven)** — in the four places risk hides (bank securities at HTM *cost*, AI stakes at *fair-value* marks, private-credit loans at *manager* NAVs, insurance liabilities at *offshore captive* marks) value is a chosen number, not a market price, held until a forcing event prices it (First Brands ≥100¢→33¢; Tricolor AAA→12¢; SVB solvent-at-cost-insolvent-at-market). `self_marked_value` U1–U4 formalizes it: the four are one defect, their gaps correlate under a common factor (no diversification), and carrying value is forced to converge on the event.
2. **AI "profit" is partly self-referential (proven)** — Amazon/Google book mark-to-market *gains* by funding the rounds that set the marks (Amazon +$9.5B on Anthropic) while Microsoft books equity-method *losses*; `reflexive_marks` M1–M4 + `MarkUnwind` show the gains must reverse if an IPO prices below the mark.
3. **Who holds the bag: annuities and 401(k)s** — risk migrates to PE-owned insurers (>$700B, ~25% of US life) → annuities on manager-marked private credit (~⅕ affiliated-fund loans) → Bermuda captives the same group controls (~60% offshore = internal "transfer"); an Aug-2025 EO opens 401(k)s to it.
4. **Timing: structure certain, date unknowable** — insolvency at zero inflow is proven; the date is unforecastable in principle (reflexivity/Minsky/Keynes). Watch the trigger panel + the staged SpaceX cliffs (Google's Sep 30 2026 delivery-miss right; 90-day notice from Dec 31 2026).

## How sure we are (the confidence ladder)
- **Proven** (Z3/TLA+/Alloy, reproducible): the 11-firm circular core; OpenAI's ≥$1.03T external-capital need and insolvency at zero inflow; the OpenAI→CoreWeave→Oracle cascade; no single feasible Fed rate; rare-earth and firm-power independence infeasible on the timeline; and that the funders' AI "profit" is partly self-referential paper marks — manufactured by funding the rounds that set the marks, not externally realized, and forced to reverse if a public price clears below the last private mark (`reflexive_marks` M1–M4).
- **Strongly evidenced** (primary filings/exchange/court/government records): Oracle's $523B backlog + ≥$72B partner debt + PIMCO's $10B anchor; CoreWeave 67% one-customer / $21B debt; NVIDIA's 13F holding ~11% of CoreWeave + concentration 36%→61%; Microsoft's 27% equity-method share of an ~$11.5B/qtr OpenAI loss, while Amazon/Google book mark-to-market GAINS on the same kind of stakes (Amazon +$9.5B on Anthropic) — circular paper income cutting both ways; the −911k jobs benchmark; the ALNRI/New-Tenant rent lag; the COMEX/LBMA dislocation + JPMorgan's $920M spoofing settlement; the Binance pardon/USD1/MGX nexus; Salt Typhoon via CALEA.
- **Graded / contested** (overlay, never used in proofs): regulatory-capture intent; the permanent-suppression narrative; whether each data lag's convenient direction was design or coincidence.
- **Out of scope** (unsupported, excluded): fabricated government microdata; a single coordinating cabal; ShadowStats-style CPI numbers.

## What is machine-proven (not asserted)
- **An 11-firm circular core** (Tarjan SCC): NVIDIA, OpenAI, Oracle, CoreWeave, Microsoft, Amazon, Anthropic, AMD, Crusoe, Lambda + lenders; **16 round-trip cycles**.
- **OpenAI needs ≥ $1.03 trillion of external capital** to honor its commitments (Z3 T3, UNSAT); the **core is insolvent at zero external inflow** (T4) — the formal signature of a bubble.
- **NVIDIA vendor-financing self-funding: 11% funded-only / 57% headline.**
- **SpaceX is separable** — the only node circular *solely via cancelable edges* — but **financially cross-held** by Google's ~$100B equity stake + the xAI merger.
- **A single capital shock cascades** OpenAI→CoreWeave→Oracle (TLA+ trace); SpaceX never defaults.
- **The Fed has no feasible single rate** (Z3 F1–F3, UNSAT) — it can only choose what to sacrifice.
- **Three physical chokepoints**, two adversary-controlled: capital (trap), **rare earths/China** (independence ~2028), **power+HALEU/Russia** (~2028-29) — none liftable by dollars on the timeline.

## The hard-money lens
Re-priced in gold, most "gains" are debasement: a US home is **−81% in gold** since 1998; CRE peaked in gold ~2001; the **$1-trillion defense budget buys ~25%** of the gold the 1998 one did; OpenAI's $1.4T is **0.53× all of TARP** in gold. In gold the broad market is **−69%** since 2000 while **NVIDIA is +1,985%** — debasement vs real concentration; a US home is **−81% in gold**.

## The honest answer to "is it all connected?"
**Not one cabal — a small elite operator-network + recurring structures + regulatory arbitrage.** The temporal meta-graph (1998→2026) shows the weavers (OpenAI, a16z, the PayPal-mafia/Thiel, Circle/USDC, BlackRock, the SPV structure, Larry Summers as the literal dereg→AI→Epstein bridge) and the recurring devices (LTCM interconnection, Enron off-balance-sheet SPVs + mark-to-market, dotcom vendor financing) rebuilt in each era's least-regulated venue. Intent is never inferred from adjacency; sensitive threads (Epstein, Waters, foreign influence) are graded and quarantined from the proofs.

## Identity / age-verification (corrected stance)
Reject age verification as a category — *futile-under-breach* (`models/z3/ageverif_futility.py`: effective gating UNSAT once IDs are breached or credentials shared), a *predator honeypot*, and *adult surveillance by construction*; **ZK does not save it** (hides the input, not the issuer, the presence/absence metadata, or the breach dynamics). `zkage/` is a steelman-then-refutation, not a solution. The futile-under-breach claim is now backed by an unbroken **2025–26 breach record**: Discord's age-verification pipeline leaked **~70,000 government IDs** (5CA, Oct 2025); its vendor **Persona** (Founders Fund/Thiel-backed) exposed code revealing an "age check" is a **financial-intelligence + watchlist + biometric-retention** pipeline (Feb 2026); the **EU's own age-verification app was broken in under two minutes** on release day (Apr 2026); and the **European Commission's Europa systems were breached** (Mar 2026) — the very body mandating identity wallets for ~450M people by Dec 2026. Centralizing identity (Persona/EUDI/World) concentrates the honeypot, it does not remove the attacker (the security mirror in `spec-supplychain-shaihulud-extortion`). Full case: `research/age-verification-abolition.md` + `research/digitalid-corporate.md` §7.

## The broader map (evidence-graded overlays, kept OUT of the proofs)
Beyond the proven core, the corpus documents — each graded `fact|contested|weak|unsupported`: **regulatory capture** (SEC/SDNY/FDIC: Choke Point 2.0 FOIA, Ripple-timing, the Kraken/Binance/LBRY enforcement sweep + 2025 reversal, ~$169M Fairshake money); **privacy-tool prosecutions** (Tornado Cash + Samourai — real Lazarus laundering vs theories courts rejected vs developers jailed); **exchanges + Asia/Gulf** (Mt.Gox, the Binance CZ-pardon/USD1/MGX nexus, SBI/Ripple, Ant's paused HKDA, ByteDance/TikTok→Oracle+MGX); the **telecom + satellite/ISR** rail (Salt Typhoon breaking the mandated CALEA backdoor; Amazon/Apple absorbing Globalstar; Starshield/NRO); and the **disclosures/surveillance** overlay (Snowden Bullrun/Dual_EC/Room 641A, In-Q-Tel/Palantir, DARPA–Trail of Bits, FBI ANOM, the Epstein Files Act, Pandora Papers). These extend the picture; they are never used to assert the proofs.

## Primary sources
Claims cite primary government and court records: SCOTUS opinions, DOJ/SDNY releases, Treasury/OFAC, the Fifth Circuit, SEC, Congress.gov, FDIC FOIA disclosures, ICIJ, NIST. `models/audit.py` and `models/cross_review.py` run via `scripts/new-research.sh`; current audit 0 flags.

## Reproduce
`bash run_all.sh` runs the Z3 engines, TLA+, Alloy, and the graph/bank/temporal/gold/defense/energy/contagion models (38 runnable models). 146 cited research blocks in `research/`.
