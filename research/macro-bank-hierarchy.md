# US bank hierarchical exposure — the vulnerable subset, HTM vs AFS, and the stablecoin squeeze

*Built 2026-06-07 from FDIC per-institution call reports (2026Q1) via `models/graph/bank_exposure.py` → `data/bank_exposure.json` (top 200 banks). Aggregate series from `macro-fdic.json`. Stablecoin/policy via GENIUS Act + ICBA.*

## 1. The HTM-vs-AFS divergence (your thesis — confirmed)
Two facts from the FDIC aggregate series, both as you suspected:

| | 2024Q1 | 2025Q1 | 2025Q4 | 2026Q1 | 2yr narrowing |
|---|---|---|---|---|---|
| **AFS** unrealized loss | −$212B | −$152B | −$99B | **−$111B** | ~**−48%** (faster) |
| **HTM** unrealized loss | −$305B | −$262B | −$207B | **−$214B** | ~**−30%** (slower) |

- **HTM losses are narrowing slower than AFS** — and **both worsened QoQ into 2026Q1** (long rates backed up on the AI-debt issuance wave + fiscal supply; see `macro-history-dereg-manipulation.json`).
- **Why it matters:** AFS losses flow through AOCI and (for large banks) into regulatory capital; **HTM losses do NOT** — they're the *un-marked* hole. A bank can look well-capitalized while its HTM book is deeply underwater. **This is the exact SVB blind spot.** HTM is also stickier (selling any taints the whole portfolio's held-to-maturity intent), so it heals only as securities roll to par — slowly.

## 2. The hierarchy (tiered by the data, not by reputation)
From `data/bank_exposure.json` (2026Q1). The vulnerability is **not uniform** — it concentrates by tier:

- **Tier 1 — G-SIB/mega (JPM, BofA, Citi, Wells, GS; ~$11.2T):** *mostly resilient*, with one glaring exception. **BofA HTM −$81B = −34% of equity**; **Wells HTM −$33B = −19%**, Wells investor-CRE/T1 52%. JPM is the fortress (HTM −5%, CRE 20%) — but uninsured 65%. In a stress, deposits flee *toward* these names (2023 SVB→JPM), which is the structural "squeeze": the mega-banks gain funding precisely when mid-tier banks lose it.
- **Tier 2 — super-regionals (~$7.7T):** mixed. US Bank flagged (HTM −14%, uninsured 51%); custody banks BNY Mellon/State Street carry **90%+ uninsured** (institutional cash) + HTM −10/−15%.
- **Tier 3 — large regionals (~$1.3T): the CRE-concentration cohort.** Western Alliance 175%, Webster 175%, East West 168%, Old National 178%, Zions 140% investor-CRE/Tier-1. These are the banks most exposed to the **CRE + housing unwind in major cities** (`macro-cre-privatecredit.md`: office CMBS delinquency record 11.76%).
- **Tier 5 — community (CRE-heaviest by ratio):** S&T 266%, Tri-Counties 243%, EagleBank 238%, Amerant 215% — small in dollars, but these are where the >300% supervisory flag bites first.

### The biggest "hidden" HTM holes (un-marked, as % of equity)
USAA −50% · **Charles Schwab Bank −43%** · Bank of Hawaii −35% · **BofA −34% (−$81B)** · Morgan Stanley PBNA −23% · Wells −19%. *(Schwab and USAA are deposit-franchise-specific; BofA is the systemically large one.)*

### Flagged vulnerable subset (≥2 of CRE>300% / secs-loss>15%eq / uninsured>50%)
Frost Bank (TX), First Hawaiian, City NB of Florida, Banco Popular (PR), Citizens Business Bank (CA), US Bank, Washington Trust, Farmers & Merchants (CA) — the securities-loss + run-risk overlap. The CRE-heavy regionals (Western Alliance/Zions/Webster) are a **second watch-list**: high CRE concentration but (so far) smaller securities holes.

## 3. The squeeze: mega vs mid, and the stablecoin/tokenized-deposit shift
- **Mega-banks can squeeze/absorb mid-tier banks** structurally: in any run, uninsured deposits migrate to the perceived-safe G-SIBs; mid-tier banks with CRE concentration + HTM holes + high uninsured ratios are the fragile node (the SVB/First Republic 2023 pattern, now mapped per-bank above).
- **GENIUS Act (Jul 2025) — the new pressure:** payment stablecoins must be **100% reserve-backed** (Treasuries/cash/insured deposits) and **cannot pay yield**; **tokenized deposits** (bank-issued, yield-bearing) are preserved. **ICBA lobbied specifically against community-bank *disintermediation*.** Mechanism: full-reserve stablecoins + Treasuries pull deposits *out* of fractional-reserve banks → shrinks the cheap-deposit base that funds CRE/housing → **tightens funding on exactly the CRE-exposed mid/small banks** while they're already absorbing CRE and housing unwinds. Big banks (and the stablecoin issuers, often partnered with them) can ride the shift; thin-capital regionals/neobanks cannot.
- **Neobanks/fintech banks** (e.g. SoFi in the data: CRE 0%, HTM 0%, uninsured 8%) have the *opposite* risk profile — little CRE/securities risk but funding-model and 1:1-backing-margin sensitivity. A "tech bank" reliant on deposit spread is squeezed by the no-yield-stablecoin / tokenized-deposit shift compressing its leverage economics.

## 4. Community-bank politics (additional items, graded)
- **ICBA** (Independent Community Bankers of America) is the documented small-bank lobby that shaped GENIUS Act guardrails — *verified*.
- A **structural dynamic** worth noting: a vulnerable mid/community bank's leadership opposing the stablecoin shift while larger banks benefit — consistent with the call-report data and the ICBA disintermediation fight. Specific individual identities advanced in some accounts of this dynamic are **unverified** in public sources and are not named here. Graded **plausible-structural.**

## 5. Limits (honesty)
True **bilateral interbank exposures** (who owes whom) are **not publicly granular** — only aggregates (Fed funds, FHLB advances, the H.8 NDFI line ~$1.97T, brokered deposits). This hierarchy is built from each bank's *own* balance-sheet risk (CRE, HTM/AFS, uninsured), which is the right proxy for run/CRE-unwind vulnerability, but it is **not** a contagion-netting map. The TLA+ cascade (`models/tla`) models contagion at the *system-tier* level instead.
