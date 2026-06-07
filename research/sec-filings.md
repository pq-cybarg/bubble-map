# SEC EDGAR Primary-Source Figures — AI-Capex Cluster

*Generated 2026-06-06. Primary EDGAR XBRL/filing pulls. Numbers below marked **[primary]** are filing-derived; **[press/knowledge]** are clearly flagged fills.*

EDGAR XBRL pattern: `https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json`

| Company | Metric | Value | Period | Source basis |
|---|---|---|---|---|
| NVIDIA (CIK 1045810) | Revenue | **$215.9B** | FY2026 (end 2026-01-25) | [primary] us-gaap:Revenues |
| NVIDIA | Net income | **$120.1B** (~56% margin) | FY2026 | [primary] NetIncomeLoss |
| NVIDIA | **Capex** | **$6.04B** (~3% of rev) | FY2026 | [primary] PaymentsToAcquireProductiveAssets |
| NVIDIA | Customer concentration | **2 direct customers each >25%** | FY2026 | [primary] 10-K text |
| Microsoft (789019) | **RPO** | **$631B** | Q2 FY26 (2025-12-31) | [primary] RevenueRemainingPerformanceObligation |
| Microsoft | Capex (P&E, excl. leases) | **$64.55B** (FY24 $44.48B) | FY2025 | [primary] 8-K ex99 |
| Microsoft | OpenAI equity-method loss | **$3.1B / $0.41 EPS** (yr-ago $523M/$0.07) | Q1 FY26 | [primary] 8-K ex99 |
| Oracle (1341439, now TX) | **RPO** | **$552.6B** (was $130.2B) | Q3 FY26 | [primary] 10-Q |
| Oracle | RPO due within 12 mo | **~12% only** | Q3 FY26 | [primary] 10-Q |
| Oracle | Total borrowings | **$134.6B** (was $92.6B FY25) | Q3 FY26 | [primary] 10-Q balance sheet |
| Oracle | New bond issuance | **~$44B+** | FY26 | [primary] cash-flow/financing |
| Alphabet (1652044) | RPO | **$467.6B** | FY2025 | [primary] RevenueRemainingPerformanceObligation |
| CoreWeave (1769628) | Backlog | **$66.8B** (Q3 $55.6B; RPO tag ~$98.8B) | Dec 2025 | [primary, w/ caveat] |
| Amazon (1018724) | AWS RPO | low–mid $200B (unresolved) | FY2025 | [press] tag switched, not primary-verified |
| Hyperscaler aggregate | Capex | **~$400B (2025) → ~$500–650B (2026 guide)** | CY | [press/guidance] |

## The depreciation lever (synchronized, earnings-flattering)

All four hyperscalers **extended server/GPU useful lives** 2023–2025, which lowers annual depreciation and **inflates reported operating income now**:

- **Meta** → **5.5 years**, effective **Jan 1 2025** (extended from ~4–5)
- **Amazon** → servers/networking **5–6 years**
- **Alphabet** → servers/network equipment **6 years**
- **Microsoft** → computer/server equipment **2–6 years**

This is a key "hidden earnings" mechanism: Blackwell-era GPUs plausibly obsolesce in **3–4 years** of frontier training duty, yet are being depreciated over **5–6**. If real economic life is shorter than book life, current earnings are overstated and a depreciation/impairment cliff is deferred, not avoided.

## SpaceX IPO ("SPCX") status

**No S-1 / DRS / registration for "Space Exploration Technologies" exists in EDGAR as of 2026-06-06.** SpaceX is **not yet a public filer**. This is consistent with a **confidential draft registration (DRS)** ahead of an imminent pricing (confidential DRS is not visible on EDGAR until ~15 days pre-roadshow). All SpaceX IPO valuation/structure figures circulating are **press-reported, not filed** — treat as such until the S-1 is public.

> **Structural read:** NVIDIA earns $120B net on $6B capex; its customers (MSFT, ORCL, GOOGL, AMZN, META, CoreWeave) carry **$1.6T+ of combined RPO** and are levering up (Oracle +$42B debt in a year) to fund the buildout that becomes NVIDIA's revenue. The capital intensity, the debt, and the back-loaded promises sit **downstream** of the chip vendor. That asymmetry is the engine the formal model will quantify.
