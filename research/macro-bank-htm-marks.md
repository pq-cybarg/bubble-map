# Bank securities marks under zero-trust — "held to par" is a choice, not a price

*Web-verified 2026-06-09. Structured + edges + sources: `macro-bank-htm-marks.json`. The asset-side mirror of the AI paper-marks proof (`reflexive_marks`). **Honest update:** aggregate unrealized losses **fell** through 2025 — the point is structural fragility + opacity, not a current acute hole.*

## The numbers — full FDIC QBP series — *STRONG where FDIC-stated*
Unrealized losses on HTM + AFS securities (the hole tracks **long rates** and reopens whenever they rise):

| Period | Unrealized loss | Note |
|---|---|---|
| **2019–2021** | net **gains** / ~0 | ultra-low rates kept bonds at/above par |
| **Q3-2022** | **~$690B (peak)** | fastest rate-hike cycle in 40 yrs (FDIC: "highest levels") |
| **Q4-2022** | **$620B** | FDIC-stated |
| **Q3-2023** | **~$684B** | second spike (SVB era) |
| **Q4-2023** | ~$478B | rates eased |
| **Q4-2024** | **~$482B** | ~8.6% of fair value (OFR) |
| **Q1-2025** | **$413.2B** | problem banks 63; net income $70.6B |
| **Q2-2025** | $395.3B | |
| **Q3-2025** | $337.1B | |
| **Q4-2025** | **$306.1B** | lowest since Q1-2022 |
| **Q1-2026** | **$325.1B** | **+$19.0B (+6.2%)** — 30-yr mortgage rate rose in March → MBS fell |

*Confidence: Q4-2022 / Q4-2024 / all 2025–26 quarters are FDIC-stated; the Q3-2022 (~$690B) peak and Q3-2023 ($684B) / Q4-2023 ($478B) are widely-reported approximations; 2019–21 is qualitative. Exact per-quarter figures live in each QBP PDF.*

- The 2025 **decline was driven by falling long rates**, not accounting; the **Q1-2026 reversal** (losses up as the 30-yr mortgage rate rose) proves it's rate-dependent and not gone.
- **HTM** = carried at **amortized cost** (value doesn't move with the market unless sold); **AFS** = marked-to-market through AOCI (and, for big banks, regulatory capital).
- **Profits hit records** alongside this (Q1-2026 net income **$80.5B**, ROA **1.26%**), and the **problem-bank count fell to 54** — but the FDIC **stopped publishing problem-bank *asset* totals** in 2025, so the *size* of concentrated exposure is no longer disclosed.
- The **BTFP** — the Fed facility that let banks borrow against underwater bonds **at par** — **expired March 2024**, removing the explicit 2023 backstop.

## The zero-trust read
- **HTM is a choice.** Whether a loss appears depends on a classification the bank picks. Move a bond to HTM and the mark-to-market loss leaves reported equity. "Book equity" and HTM "held-to-par" are **self-reported solvency, not prices** — the same critique applied to government statistics and to AI fair-value marks, now on the asset side of banks.
- **Unrealized until forced.** The loss stays invisible only while the bank isn't forced to sell. A deposit run forces sales, realizes the loss, and can taint the whole HTM book — **the SVB 2023 mechanism: solvent at cost, insolvent at market, dead in a weekend.**
- **Opacity.** The FDIC **stopped publishing problem-bank asset totals** in 2025 (`macro-fdic`) — the aggregate is visible, the concentration is not.
- **Symmetry with the AI marks.** AI funders hold private stakes **up** at self-set marks and book gains (`reflexive_marks` M2a); banks hold bonds **at cost** and avoid losses. Both are *"carried at a chosen value, not a market price, until an external event forces realization"* — an **IPO below the mark** for the AI side, a **deposit run** for the bank side.

## Exposing what the withdrawn aggregate hides
The FDIC dropped the problem-bank **asset total**, but that's cosmetic — the facts are still recoverable:

**Reconstruct it directly (the number wasn't deleted, just the summary):**
- **Per-bank Call Reports (FFIEC 031/041, Schedule RC-B)** report HTM **amortized cost *and* fair value**, AFS fair value, and pledged securities — so each bank's unrealized HTM loss = *fair value − amortized cost* is **computable per institution, every quarter.**
- **FDIC BankFind Suite API** (`banks.data.fdic.gov`, no registration) serves institution-level financials incl. securities, equity, and **uninsured deposits**. **This repo already does it:** `models/graph/bank_exposure.py` pulls the API and computes per-bank HTM-loss/equity (e.g., BofA HTM −$81B ≈ −34% of equity).
- **Uninsured-deposit share** (call report) — the run-risk metric (SVB was ~94%); high uninsured % + big HTM loss = the SVB setup.

**Funding-stress proxies (FDIC-aggregate-free):**
- **FHLB advances** — the "lender of next-to-last-resort": system advances **$742.8B (Jun 2025)** vs $736.7B (YE 2024), peaked Mar 2023; growth at higher-risk banks is a tell.
- **Fed discount window / H.4.1** — aggregate primary credit weekly; **spikes flag stress** even though names lag ~2 years.
- **BTFP run-off** (expired Mar 2024) mapped who was underwater; **brokered/hot-money deposits** show funding fragility.

**Market proxies (front-run the accounting):** KBW regional-bank index (KRE), single-name drawdowns, **bank CDS spreads**, options skew, rating watch lists — and the FDIC still publishes the problem-bank **count** and the **failed-bank list**.

> **Opacity of the aggregate ≠ opacity of the facts.** The per-bank RC-B + FDIC API rebuild the exact number that was withdrawn (`bank_exposure.py` does), and FHLB advances / discount-window spikes / CDS / uninsured-deposit share give independent stress signals.

## Posture
Read "book equity" and HTM "held-to-par" as the **most solvent admissible presentation**, and stress-test at market (AFS + HTM marked) and under forced-sale — not at cost.
