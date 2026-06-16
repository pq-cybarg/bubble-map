# ALNRI analysis — market rents vs official CPI shelter

*Web-verified 2026-06-08. Structured + edges + sources: `macro-rent-cpi-divergence.json`. The deep-dive on the CPI-shelter strand of `macro-official-data-integrity`. **The lag is documented BLS fact; the "convenient direction" is the analytical (contested) layer.***

## The series being compared
| Series | What it tracks | Lead/lag vs CPI |
|---|---|---|
| **ALNRI** — Apartment List National Rent Index | new-lease median rents | leads CPI rent ~**16 months** |
| **ZORI** — Zillow Observed Rent Index | asking rents, repeat-rent, quality-controlled | leads |
| **NTRI** — BLS New Tenant Rent Index (R-CPI-NTR) | *official CPI microdata*, turnover units only, dated to when the price changed | leads CPI rent ~**4 quarters** |
| **CPI rent** — CUUR0000SEHA + OER | what *all* renters pay this month (full lease stock) | the official, lagging series |

Shelter (rent + OER) is **~⅓ of CPI** — so a one-year lag in this component drives the whole headline at turning points.

## The divergence — *STRONG (independent series + BLS's own NTRI)*
- **Dec 2021: ALNRI +18% YoY while official CPI rent showed ~3%** — a ~15pp gap.
- **Zillow ZORI ~15%** (late 2021) vs **CPI rent ~5.5%**.
- ALNRI YoY peaked **Nov 2021**, leading the rent-CPI peak by **~16 months**.
- **BLS's own NTRI** — same microdata, turnover units, correctly dated — **leads official CPI rent by ~4 quarters.** BLS built it precisely because the headline shelter series lags.
- **Mechanism:** official CPI shelter measures what *all* renters pay; most leases reset only annually, so a market-rent shock enters the index slowly, smeared over ~12 months.

## The two-phase bias — *lag FACT; "conveniently directional" CONTESTED*
- **2021–22 (understatement):** market rents +15–18%, official CPI shelter only ~3–5.5%, while the funds rate was still ~0% → the lag helped justify staying loose too long ("transitory").
- **2023–25 (overstatement):** market rents cooled (ALNRI/ZORI flat-to-negative) but official CPI shelter stayed elevated for ~a year → lagged shelter was a large part of the 2024 "inflation is resurging" narrative that kept policy restrictive.

The most-weighted CPI component is structurally **~1 year stale**, so it biases the headline in whichever direction is 12 months out of date — and in 2021–25 that error ran in the **policy-convenient** direction at each phase. *Convenient or coincidental is the contested part; the lag and its sign are fact.*

## When policy cited which shelter series — the chronology *(added 2026-06-16, #53)*
Tracking *which framing the Fed reached for* as the stance changed. *Speech-page rows are verified primaries; FOMC-presser rows are flagged for quote re-verification.*

| Date | Who | Shelter framing | Series leaned on |
|---|---|---|---|
| **2021-08-27** | Powell (Jackson Hole) | "transitory", durable goods — **surging market rents absent** | lagged-**low** official (by omission) ✔︎ verified |
| **2022-03-24** | Gov. **Waller** | earliest explicit lag: CPI rents "slow to reflect market conditions"; CoreLogic +12% / RealPage +15%; CPI rent would "double in 2022" | **leading** market rents, to argue inflation would **rise** ✔︎ verified |
| 2022-11-02 | Powell (presser) | new-lease series "very pro-cyclical … now coming down faster" | both; leading already falling — *quote unverified* |
| **2022-11-30** | Powell (Brookings) | "the market rate on new leases is a **timelier indicator**"; new-lease ~20% "falling sharply since mid-year" | both; leading → forecast lagged ✔︎ verified |
| **2023-08-25** | Powell (Jackson Hole) | slowing new-lease rents "**in the pipeline** … over the coming year" | **leading** as forward signal ✔︎ verified |
| 2024-04 / 05 | Powell + minutes | "**lack of further progress**"; shelter sluggish → higher-for-longer | **lagged-high** official — *even though market rents had normalized in late 2023* — *quote unverified* |
| 2025–26 | Powell (pressers) | disinflation "slow and bumpy", then "come down steadily" | lagged official, now cooperating |

**The asymmetry (the thesis).** 2021 leaned on lagged-**low** shelter to support "transitory" (downplay); 2022 used the **leading** new-lease data *because it predicted disinflation* (useful); but by 2024 — with leading rents already cooled — Powell leaned on the **lagged, still-high** official measure to justify higher-for-longer. **The Fed invoked whichever shelter framing fit the stance.** Notably, Powell never named the BLS New Tenant Rent Index by label — though the Fed's *own* Reserve Banks (Cleveland WP 22-38R / EC 2024-17, Richmond, Boston, Minneapolis) flagged the lag in real time. The cleanest evidence is that gap between Reserve-Bank research and FOMC rhetoric. *(Anchor public quotes on the four verified speech pages; confirm presser wording before relying on exact words.)*

## Why it matters beyond the print
Shelter feeds **COLA (CPI-W), TIPS, and bracket indexation** (`macro-official-data-integrity`) — a smoothed series also avoided the spike that would have forced larger COLA/TIPS payouts at the 2021–22 peak. And **CRE/multifamily valuations and private-credit marks** depend on *actual* rents (`macro-cre-privatecredit`), not the lagged CPI proxy — so the same lag that flatters the inflation print can mask stress in apartment/CRE collateral.

## Posture
Read **ALNRI / ZORI / NTRI** for the real shelter signal; treat official **CPI shelter (CUUR0000SEHA / OER)** as a ~1-year-stale, policy-relevant lagging print — the single clearest, BLS-confirmed example of "doubt the headline."
