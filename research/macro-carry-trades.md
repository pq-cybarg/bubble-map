# Yen (and developing EUR/CHF) reverse carry trade — the deleveraging trigger

*Built from `research/macro-carry-trades.json` (web-verified: BOJ reporting, Investing.com, Deriv, Stapleton AM, EBC, Mesirow, Capital.com). Quantified live in the Charts tab (the US−Japan 10Y differential and JGB level).*

> **Thesis.** The AI / mega-cap trade is the crowded "risk-on" destination funded, at the margin, by **cheap carry borrowing**. As the cheapest funding currencies (JPY, then CHF) normalize, the carry math breaks and forced deleveraging can hit **FX, equities, and credit simultaneously** — the clearest *exogenous* trigger that could force-sell the AI bubble.

## 1. The mechanism
Borrow JPY/CHF near zero → convert → buy higher-yielding/risk assets (US tech/AI prominent). Rising BOJ rates plus **~2.8% JGB 10Y yields** (highest since 1997) shrink the spread *and* strengthen the yen, forcing position liquidation. Because the carry is **leveraged and crowded**, the unwind is **non-linear and correlation-spiking** — it deleverages the most crowded longs (Mag7/AI) **regardless of fundamentals**.

## 2. The yen leg (the primary vector)
- **BOJ path:** 0.5% (Jan 2025) → 0.75% (Dec 19 2025) → **~1.0% expected (mid-2026)**. JGB 10Y **~2.8%**. *Fact.*
- **Carry size:** estimated peak **$300–500B**. *Estimate (graded).*
- **Unwind window:** peak repatriation **Nov 2025–Feb 2026**; added pressure into the **Japanese fiscal year-end (Mar 2026)**.
- **Precedent (proof the channel transmits globally in hours):** **Aug 5 2024** — a sharp yen-carry unwind crashed the Nikkei (**~−12% in a day**) and spiked global volatility. *Fact.*

## 3. The developing EUR/CHF leg (secondary vector)
The **Swiss franc** is the classic secondary funding currency; the **SNB is expected to hold ~0%** well into 2026, anchoring cheap CHF funding (EUR/CHF ~0.94). A second carry vector builds as euro-area growth firms. *Graded: developing.*

## 4. Why it matters to the bubble (the exogenous-shock channel)
This is the cleanest **exogenous shock node** for the formal cascade model (`models/tla`): a carry-unwind / rate-shock that simultaneously
1. **raises the discount rate** on the AI core's back-loaded RPO/backlog,
2. **re-widens bank HTM unrealized losses** (`macro-fdic`, `macro-bank-htm-marks`), and
3. **forces selling of the crowded AI trade** —

any one of which can flip the circular core from "solvent-while-inflows-continue" to "insolvent" (the Z3 theorem T4 condition). It is tracked live on the **unwind watch-list** (`spec-unwind-timing`): the US−Japan 10Y differential has compressed from a peak ~3.85pp (Oct 2023) toward ~1.8–2.0pp as the JGB climbed — *the carry's fuel draining* is the "ARMING" state, not yet "firing."

## 5. Limits
Carry-trade **size is an estimate** (positions are not centrally reported); the unwind's **timing is not forecastable** (only its triggers are observable — see `spec-unwind-timing`). The Aug-2024 episode is the empirical proof-of-mechanism; the 2025–26 normalization is the live test.

*Sources: [Investing.com — BOJ/carry](https://www.investing.com/analysis/the-boj-just-pulled-the-trigger-markets-brace-for-carry-trade-chaos-200672097), [Deriv — USDJPY carry breakdown](https://deriv.com/blog/posts/usdjpy-carry-trade-breaking-down), [Stapleton AM — reverse carry & global consequences](https://stapletonam.com/the-unwind-of-the-yen-carry-trade-understanding-the-reverse-carry-trade-and-its-global-consequences/), [Mesirow — the quiet engine of global risk](https://www.mesirow.com/insights/quiet-engine-global-risk), [Capital.com — EUR/CHF](https://capital.com/en-int/analysis/eur-to-chf-forecast).*
