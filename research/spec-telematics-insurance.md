# Car-insurance telematics / surveillance pricing — UBI apps, the covert automaker→LexisNexis/Verisk→insurer data pipeline, FTC v. GM, and Arity's phone-SDK tracking (both sides, dated)

*Built 2026-06-28 from `research/spec-telematics-insurance.json`. The auto/surveillance/insurance nexus (sub-block of the auto epic #177). Cross-links `GM`, `FTC`, `State_AGs`, `US_Auto_Makers`, and the surveillance/ownership-erosion thread.*

> **Frame.** Usage-based insurance (UBI) telematics (Progressive Snapshot, Allstate Drivewise, State Farm, Root) tracks speed/braking/miles/phone-use/**location** via dongles or always-on phone apps. The bigger story is the **covert pipeline**: automakers (GM OnStar "Smart Driver"; also Honda/Hyundai/Kia) **sold** driving + geolocation data to data brokers **LexisNexis Risk Solutions + Verisk**, who repackaged it into insurance risk scores → **premium hikes without consent** (NYT, Mar 2024). Enforcement followed: **FTC v. GM/OnStar** (order finalized Jan 2026), **California AG** ($12.75M), **Texas AG v. Allstate/Arity** (Jan 2025).
>
> **Discipline.** Products, the covert sales, and the enforcement are **fact**. The two supplied framings ("location-inference price discrimination" and "no-alternative collective coercion") are **graded** — neither adopted as asserted fact nor dismissed. Overlay; excluded from the proofs.

## 1. The UBI apps (fact)

Insurers offer "discounts" for installing a **dongle or always-on phone app** that scores driving — **Progressive Snapshot, Allstate Drivewise, State Farm Drive Safe & Save, Root**. The apps read phone sensors and can run **continuously** (location/movement even when not driving the insured car). Surveys show most non-users decline over privacy and would only opt in if insurers promised **not to sell** the data + gave deletion control. *Fact (the products + the continuous-collection capability).*

## 2. The covert pipeline (fact)

The scandal (**NYT / Kashmir Hill, Mar 2024**): automakers collected detailed driving + **precise geolocation** (GM's OnStar "Smart Driver" as often as **every ~3 seconds**) and **sold** it to brokers **LexisNexis Risk Solutions** and **Verisk Analytics**, which packaged it into risk reports **sold to insurers** — and premiums rose on data drivers never knowingly shared (one driver's premium reportedly **jumped ~80%** from 603 logged trips). **Honda, Hyundai, Kia** were also implicated. GM made **~$20M** and gave consumers **no notice**. *Fact.*

## 3. The enforcement (fact)

1. **FTC v. GM + OnStar** — order **finalized Jan 2026**: a **5-year ban** on sharing geolocation/driver-behavior data with consumer-reporting agencies + ~20-year consent/transparency requirements.
2. **California AG** — a **$12.75M** settlement (CCPA data-minimization/purpose-limitation).
3. **Texas AG** — sued **Allstate + its data subsidiary Arity** (**Jan 2025**) for unlawfully collecting/selling location + movement data from **45M+ trips**; Arity embedded **SDKs in third-party phone apps** (e.g. Life360, GasBuddy) to harvest movement data from people with **no insurance relationship**.

*Fact.*

## 4. The price-discrimination risk (graded)

The first supplied framing: continuous geolocation enables **inferring behavior/health** and pricing on it (e.g., regular pharmacy visits could proxy a health condition). This is a **documented capability/risk** the pipeline creates — **not** an asserted current insurer practice. Per **read-words-for-intent**: insurers **say** UBI is voluntary/discount-only and that they "don't sell" data, yet the **covert automaker sales + Arity's app-SDK harvesting** show data flowing **without consent** into risk scoring — so stated intent and documented conduct diverge, which is the warranted finding; the specific "punish you for being sick via pharmacy visits" mechanism is **plausible-but-unproven**. *Grade: the price-discrimination capability is documented; a specific health-punishment practice is **unverified** (flagged, not adopted).*

## 5. The "no alternative" claim (graded)

The second framing — "insurers force telematics by offering no alternative" — is **partly true / partly overstated**. Non-telematics insurers still exist (so "all force it" is **unsupported**), **but** three structural facts make opting out leaky: **(a)** the **shared data-broker layer** — LexisNexis/Verisk score drivers **across** insurers, so declining one company's app doesn't escape the broker score; **(b)** the **covert car pipeline** meant your vehicle reported you regardless of any insurance app; **(c)** the industry trend is telematics-as-default + surveillance-priced books. So the "collective" effect is real **via shared infrastructure + parallel conduct** — **not** necessarily coordinated collusion (composition guard: parallel conduct + a shared broker layer ≠ a single "insurer mind"). *Grade: "no alternative at all" unsupported; "shared-infrastructure coercion/leakiness" documented.*

## 6. The honest reading

Car-insurance telematics is **real surveillance pricing**, and the worst of it was **covert**: automakers (led by GM/OnStar) sold precise driving + geolocation data to LexisNexis/Verisk, who scored drivers for insurers who raised premiums on data consumers never knowingly shared — until the **FTC (Jan 2026)**, **California**, and **Texas (v. Allstate/Arity)** intervened. The two concerns grade out as: (1) location-based price discrimination is a documented **capability** the pipeline enables (a specific health-punishment practice is plausible-but-unproven, flagged not asserted), and (2) the "no alternative" coercion is real **not** as a literal universal mandate but via the **shared data-broker layer + the covert car pipeline** (parallel conduct + shared infrastructure, not proven collusion). Read by read-words-for-intent: insurers' "voluntary / we don't sell" framing **diverges** from the documented covert sales. Both sides retained with dates. Overlay; excluded from the proofs.

*Sources: [NYT — automakers quietly shared drivers' data with insurers (Mar 2024)](https://www.nytimes.com/2024/03/11/technology/carmakers-driver-tracking-insurance.html); [FTC — action against GM/OnStar over geolocation/driving data](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-gm-onstar-harvesting-selling-drivers-precise-geolocation-driving-behavior); [TechCrunch — FTC GM data order settled (Jan 2026)](https://techcrunch.com/2026/01/14/the-ftcs-data-sharing-order-against-gm-is-finally-settled/); [Hunton — California AG $12.75M GM settlement (CCPA)](https://www.hunton.com/privacy-and-cybersecurity-law-blog/california-ag-announces-record-12-75m-settlement-with-gm-over-ccpa-data-minimization-and-purpose-limitation-violations); [Texas AG — sues Allstate & Arity (Jan 2025)](https://www.texasattorneygeneral.gov/news/releases/attorney-general-ken-paxton-sues-allstate-and-arity-illegally-collecting-and-selling-data); [Edmunds — phone apps selling driving data (Arity SDK)](https://www.edmunds.com/car-news/report-finds-apps-are-selling-your-driving-data-to-insurance-companies.html).*
