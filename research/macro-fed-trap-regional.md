# The Fed's impossible position + regional divergence + hidden leverage

*Built 2026-06-07 from `models/z3/fed_policy_trap.py`, `models/graph/regional_leverage.py` (reading `data/bank_exposure.json`). This is the formalization of the thesis: a single policy rate cannot fix a multi-dimensional (regional × sectoral × global) divergence.*

## 1. The monetary-policy trap (Tinbergen, proven UNSAT)
To stabilize N independent targets you need ≥ N independent instruments. The Fed has ~1 (the funds rate; ~2 with the balance sheet). The targets pull in opposite directions:

| Target | Rate it "wants" | Why |
|---|---|---|
| Inflation / dollar defense | **≥4.5%** | record gold, de-dollarization → tightness |
| Regional banks / CRE / HTM | **≤2.0%** | CRE unwind + securities losses → cuts |
| AI financial stability | ~4.0% | don't reflate the capex bubble |
| Sovereign fiscal / debt service | ~2.5% | Treasury issuance wall → low rates |
| Global carry (JPY) | ~3.5% | avoid forcing the yen-carry unwind |

**Z3 results:**
- **F1 UNSAT:** no `r` with `r≥4.5 ∧ r≤2.0` — inflation defense and bank rescue are *directly contradictory*.
- **F2 UNSAT:** no `r` within ±1.0pt of all five targets (spread 2.0–4.5 > 2×tol).
- **F3 UNSAT:** even *two* instruments (rate + QT/QE) can't independently satisfy *five* targets — the system is over-determined.
- **Best case:** the Chebyshev-optimal single rate is **r\* = 3.25%**, and it *still* leaves a target **~1.25 points mis-set**. Raising toward 4.5% pushes regional banks/CRE/fiscal toward crisis; cutting toward 2.0% reflates inflation/AI/gold.

**Conclusion:** monetary policy cannot *fix* a divergence crisis — it can only **choose which part of the system to sacrifice.** That is the formal trap, and it is why "raise or lower the rate" has no solution.

## 2. Regional divergence (the empirical input)
Aggregating the top-200 banks by state (`regional_leverage.py`): **average CRE-concentration/Tier-1 ranges 37% → 336% across states** — a **~300-point dispersion** (KY 351%, SC 349%, WV 339%, MT 336% at the top; coastal/large-bank states far lower). Bank stress is **geographically divergent**: the CRE/HTM pain concentrates in specific states/regions while the AI-driven asset inflation concentrates in others (coastal tech hubs). A single national rate is the wrong tool for a map this uneven — the cities/suburbs/rural and state-by-state divergence observed is real in the call-report data.

## 3. Hidden vs surfaced leverage (the masked risk)
`reported_leverage = assets/equity`; `hidden_leverage = assets/(equity + HTM_loss + AFS_loss)` (mark securities losses to capital). The gap is the un-marked HTM hole:

| Bank | Reported | HTM-adjusted | ×inflation | HTM/eq |
|---|---|---|---|---|
| **Charles Schwab Bank** | 13.3× | **35.9×** | ×2.7 | −43% |
| Bank of Hawaii | 13.5× | 23.9× | ×1.8 | −35% |
| **Bank of America** | 11.1× | 16.9× | ×1.5 | −34% |
| Frost Bank | 11.7× | 16.6× | ×1.4 | −4%* |

A bank can report a comfortable ~11–13× leverage while its *true* mark-to-market leverage is 17–36×. **This is precisely the leverage that a single rate move cannot safely unwind**: cutting rates relieves it (securities recover) but reflates the bubble; holding/raising rates keeps these books underwater.

**Honesty caveat:** the model also flags several names with negative adjusted equity — but those are **US branches/agencies of foreign banks** (Standard Chartered, Bank of China, BBVA, State Bank of India, Bank of Baroda, Bank Hapoalim), whose reported "equity" is a **branch-accounting artifact** (they're capitalized by the parent abroad). That is **not** a solvency signal and is excluded from the vulnerability read — flagged to avoid a false alarm.

## 4. Why this closes the loop
The single-instrument trap is the macro mirror of the Layer-1 finding: just as the AI core is "solvent only while external capital flows" (Z3 T4), the banking system is "stable only at a rate that doesn't exist." Both are constraint systems with **no feasible interior solution** — they resolve only by a transfer (more capital in, or a chosen sacrifice). The divergence spans regions, sectors, wealth classes and continents; a scalar policy rate is, provably, the wrong dimensionality of tool.
