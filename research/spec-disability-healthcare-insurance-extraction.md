# Disability healthcare access & the insurance value-extraction stack — *is insurance a scam?* (the actuarial core vs. the operations layer where the extraction actually lives)

*Built 2026-06-18 from `research/spec-disability-healthcare-insurance-extraction.json`.*

> **Two interlocking questions.** **(A) Is insurance structurally a scam?** Graded precisely: **no** categorically — the actuarial core sells variance-reduction/ruin-avoidance, is solvent without growth, and is **not a Ponzi** — but **yes on a measurable spectrum** (loss ratio + denial behavior + insurability), with credit-life / junk-warranty / investment-dressed-life products at the scam end. **(B) Where does the real extraction live?** Not in the pool math but in the **operations layer**: PBM middleman rent, algorithmic **denial-as-margin**, and health-**data exploitation** — and it falls **hardest on patients with disabilities.** The scam isn't the risk pool; it's the **friction and the middlemen** bolted onto it.

## 1. Is insurance a scam? — the actuarial core

**The accounting identity is real.** Over any pool/period: `claims_paid ≤ premiums + float income − expenses − profit`. You cannot have everyone pay in *and* everyone draw out more than they put in. Insurance is **negative-sum in expected dollars by construction** — the premium is priced *above* expected loss, and the gap funds overhead, profit, and the cut. The **float** (collect now, pay later, keep the investment income between) is a primary profit source.

**But it is not a Ponzi** — the bright line. A Ponzi *requires growth* (pays old investors with new investors' money; insolvent by construction). Insurance **pre-funds** via legally-mandated **reserves**: a closed book with zero new customers still pays every valid claim if priced right, because claims come from the *same cohort's* premiums + reserves + float, **not new entrants.** Pooling (law of large numbers) is mathematically sound for genuinely random, independent, insurable risks.

**And negative-EV ≠ scam.** Insurance is a bad bet in dollars *on purpose* — it sells **variance reduction / ruin-avoidance**, not return. Concave utility makes trading a small *certain* loss (premium) to avoid a large *random* ruinous one (house fire, $2M cancer bill) rational: it raises expected **utility** while lowering expected wealth. A real economic good. The "scam" enters only when a product is mis-sold (whole-life as an *investment*), insures non-risks, or is engineered to minimize payout. **Grade: fact;** "almost all insurance is a scam" is **false as stated** — but points at a real spectrum.

## 2. The loss-ratio spectrum — which products *are* scams

The discriminating instrument is the **loss ratio** (claims ÷ premiums) + denial behavior + insurability:

| Product | Loss ratio | Read |
|---|---|---|
| Well-run P&C (auto/home) | ~95–100%+ combined | Often profits **only** on float — refutes "they keep most of it" |
| ACA health | **≥80–85% floor** (MLR; rebate the rest) | Modest headline load — extraction is in *denials/PBMs*, not the ratio |
| Term life | high | Legitimate ruin-cover |
| Extended warranties | ~40–60% | Half retained — scam-adjacent |
| **Credit life / junk indemnity** | **~20–40%** (60–80% retained) | **This is the "scam" characterization — fair here** |

**Verdict:** false categorically, but correctly pointing at a spectrum — legitimate at one end (P&C/term-life), scam at the other (credit-life/junk-warranty/investment-dressed-life). **Grade: fact.**

## 3. PBM value-extraction — the clearest documented rent

Pharmacy Benefit Managers are the cleanest extraction layer. **6 PBMs manage ~95% of US prescriptions**; the **Big 3 — CVS Caremark, Express Scripts (Cigna), OptumRx (UnitedHealth)** — are vertically integrated with insurers *and* pharmacies. Documented (FTC interim reports, Jul 2024 / Jan 2025):
- **Spread pricing** — bill plans more than they pay pharmacies; ~**$1.4B** from spread on just 51 generic specialty drugs over ~5 years.
- **Vertical-integration markups** — marked up specialty generics at their *own* affiliated pharmacies by hundreds-to-thousands of percent, **>$7.3B** above acquisition cost (2017–2022).
- **Rebate-aggregator opacity** — PBM-owned aggregators capture rebates, deduct fees first, and the plan sponsor is often never told the original total.
- **Inverse incentive** — PBMs can profit *more* when list prices rise (a % of a bigger number), misaligning the middleman from the payer.

**Enforcement:** FTC suit against the Big 3 + their GPOs over insulin rebating; a **Feb 2026 Express Scripts settlement** requiring transparency changes. **Grade: fact.**

## 4. Denial-as-margin — the operations-layer abuse

The health-insurance extraction isn't the actuarial load; it's **denial-as-margin** — delay/deny legitimate claims, externalize the cost of contesting onto patients/providers. Two documented, litigated cases:

- **Cigna PXDX** (ProPublica): an auto-flag system rejected claims not matching a pre-set list; medical directors then denied them **without opening patient files** — one doctor denying up to **60,000 claims/month at ~1.2 seconds each**; **>300,000** rejected in two months of 2022. Congressional inquiry + class action (state law requires individual physician review).
- **UnitedHealth / nH Predict** (naviHealth, Optum, acquired 2020): allegedly overrode physicians to deny elderly post-acute Medicare Advantage care, with a claimed **~90% error rate** (9 of 10 denials reversed on appeal). The **Senate PSI (Oct 2024)** documented UHC's skilled-nursing denial rate rising **~9×** and post-acute prior-auth denials going **8.7% → 22.7% (2019–2022)**, tracking naviHealth's rollout. In 2026 a federal court ordered UnitedHealth to **produce broad discovery / disclose the algorithm.**

**The friction externality:** denial-as-margin works *because* the cost of appealing is dumped on the patient. A 90%-reversed rate means the denials were mostly wrong — but most people never appeal, so the wrongful denial **sticks as margin.** **Grade: fact** (ProPublica; PSI figures; court orders); the nH Predict error-rate/intent claims are **active-litigation allegations.**

## 5. Why patients with disabilities bear it most

The friction model lands hardest on the disabled — highest utilization, most prior-auth touchpoints, most DME dependence, so every denial/delay/gap compounds:
- **Prior-auth denials:** Medicaid managed-care denied **~1 in 8** requests (2019); some MCOs **>25%** — similar concerns in Medicare Advantage.
- **DME hurdles:** power wheelchairs need face-to-face eval + medical-necessity prescription + approved supplier + prior auth; miss any step → denial; plus annual caps.
- **Coverage gaps:** Medicare classifies wheelchair **ramps** as home modifications, *not* DME — **not covered**, leaving **$1,500–$15,000** out of pocket to make a covered wheelchair usable.
- **Admin burden** is especially hard to navigate for people with disabilities (Urban Institute).

**Grade: fact.**

## 6. Data extraction & surveillance pricing

A third layer: health-data brokering feeding pricing/underwriting. **LexisNexis Risk Solutions** markets a ~5-decade multi-source dataset — de-identified claims, clinical/consumer data, **social-determinants-of-health** data — plus "socioeconomic health and readmission risk scores" that "predict health risk **independent of traditional healthcare data**," and (for life insurance) richer inputs for "more precise pricing and more accurate mortality predictions at scale."

This is the infrastructure for **surveillance pricing**: scoring individuals from non-clinical/consumer data to price, segment, or steer them — shifting insurance from broad **risk-pooling** toward **individualized prediction**, which erodes the cross-subsidy (the healthy funding the sick) that makes pooling a social good. The disabled/chronically-ill are exactly the population such scoring most readily prices up or screens around. **Grade: fact** (the products are public); "erodes the cross-subsidy" is a documented-direction concern.

## 7. Synthesis — where the scam actually is

The actuarial **core** (pooling for ruin-avoidance) is legitimate and **not a Ponzi**. The **extraction** lives in the **operations layer** bolted onto it: **PBM rent** (spread/markups/opaque rebates), **denial-as-margin** (algorithmic + friction), and **surveillance pricing**. The scam isn't the pool — it's the **friction and the middlemen** — and by design it falls hardest on those who need care most.

So the honest answer to *"is insurance a scam?"*: **the math isn't; the loss-ratio spectrum tells you which products are; and the operations layer is where ordinary insurance is turned *into* extraction** — documented, measurable, and **reformable** (loss-ratio floors, PBM transparency/divestiture, denial-rate accountability, data-broker limits), not inevitable.

## 8. Limits
**Documented:** the actuarial economics (identity, float, reserves-not-entrants, variance-reduction, loss-ratio spectrum); the PBM mechanisms + FTC enforcement; Cigna PXDX and the UnitedHealth/nH Predict denial figures (with the 90%-error/intent claims labeled active-litigation allegations); the disability DME/prior-auth barriers and coverage gaps; the LexisNexis data/risk-score products. **Graded:** "almost all insurance is a scam" = false categorically, true on a spectrum; "surveillance pricing erodes the cross-subsidy" = documented-direction concern. *Institutional action documented; incentives — not an asserted unitary corporate mind — explain the behavior; no individual blamed.* Overlay edges excluded from the proofs.

*Sources: [FTC — Pharmacy Benefit Managers report](https://www.ftc.gov/reports/pharmacy-benefit-managers-report); [FTC — second interim PBM staff report (Jan 2025)](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-releases-second-interim-staff-report-prescription-drug-middlemen); [ProPublica — How Cigna saves millions having its doctors reject claims without reading them](https://www.propublica.org/article/cigna-pxdx-medical-health-insurance-rejection-claims); [CBS — UnitedHealth AI denial lawsuit](https://www.cbsnews.com/news/unitedhealth-lawsuit-ai-deny-claims-medicare-advantage-health-insurance-denials/); [Becker's — court orders UnitedHealth discovery in AI denial case](https://www.beckerspayer.com/legal/judge-orders-unitedhealth-to-hand-over-broad-discovery-in-ai-coverage-denial-case/); [Urban Institute — Barriers to Accessing Medical Equipment for adults with disabilities (PDF)](https://www.urban.org/sites/default/files/2024-03/Barriers%20to%20Accessing%20Medical%20Equipment%20and%20Other%20Health%20Services%20and%20Supports%20within%20Households%20of%20Adults%20with%20Disabilities.pdf); [Medicare.gov — wheelchairs & scooters coverage](https://www.medicare.gov/coverage/wheelchairs-scooters); [LexisNexis Risk Solutions — healthcare market data](https://risk.lexisnexis.com/healthcare/healthcare-market-data).*
