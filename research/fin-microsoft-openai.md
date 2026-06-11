# Microsoft ↔ OpenAI

*Generated 2026-06-06. Compiled from primary sources (Microsoft/OpenAI blogs, SEC 8-K ex99 accession 000119312525256310, accounting analyses) + flagged knowledge fills.*

## The arrangement

- **Cumulative investment ~$13B** (from ~$1B in 2019 through 2023). A **large portion delivered as Azure credits**, not cash — so OpenAI "spends" Microsoft's investment back into Microsoft's own cloud. *[exact cash/credit split never itemized — med confidence]*
- **Oct 28 2025 restructuring** (definitive): Microsoft holds **~27% of the new OpenAI Group PBC**, reported value **~$135B**. IP rights through **~2032**; reciprocal revenue-share (reported cap **~$38B**); **Azure right-of-first-refusal removed** (OpenAI free to use Oracle/CoreWeave/Google).
- **OpenAI's incremental $250B Azure commitment** — a quarter-trillion-dollar purchase pledge to the cloud of its own 27% owner.
- **Apr 27 2026 "next phase" deal** supersedes the Oct 2025 terms; the equity + Azure-commitment architecture persists.

## The round-trips (why this is circular)

1. **Credits round-trip:** Microsoft funds OpenAI partly in Azure credits → OpenAI consumes Azure → Microsoft books it as Azure revenue. Microsoft both funds and is paid by the same dollar.
2. **Commitment round-trip:** OpenAI raises cash (SoftBank, Nvidia, sovereigns) → pledges $250B to Azure → Azure buys Nvidia GPUs (Nvidia also funds OpenAI). The dollar circles supplier→customer→supplier.
3. **Equity-method drag (the honest counterweight):** OpenAI's *net loss* flows onto Microsoft's income statement. **Q1 FY26 hit: $3.1B / $0.41 EPS**, up **6×** from $523M / $0.07 a year earlier. OpenAI's burn is now a visible, accelerating cost to Microsoft GAAP earnings — the circularity cuts both ways.

## Scale anchors

| Item | Value | Period |
|---|---|---|
| MSFT stake in OpenAI | ~27% (~$135B) | Oct 2025 |
| OpenAI → Azure commitment (incremental) | **$250B** | Oct 2025 |
| MSFT FY25 capex (P&E, excl. leases) | **$64.55B** (FY24 $44.48B) | FY2025 |
| MSFT commercial RPO | **$631B** | Q2 FY26 |
| OpenAI equity-method loss to MSFT | **$3.1B/qtr** | Q1 FY26 |
| OpenAI revenue run-rate vs commitments | ~$13–20B vs **~$1.4T** | 2025–26 |

The last row is the crux: OpenAI has pledged on the order of **$1.4 trillion** in compute (Azure $250B + Oracle ~$300B + CoreWeave ~$22B + Broadcom/AMD/Nvidia/SoftBank) against a revenue run-rate **~70× smaller**. Every node in the web has booked a slice of that $1.4T as backlog/RPO/expected revenue.

## The asset behind the backlog ages out *(added 2026-06-11)*
That $1.4T of "expected revenue" is also $1.4T of compute someone must *build* with debt- and lease-financed GPUs — and those GPUs economically age in **~2–3 years** while the financing runs 5–19 (Microsoft itself depreciates GPUs over ~6yr; on honest lives that overstates profit by ~$2.9B/yr on one tranche). So even the "real assets" side of this web carries the duration-mismatch defect ([[fin-ai-depreciation-debttrap]], [[depreciation_trap]] D1–D4): the backlog is promised against compute that depreciates faster than the loans that bought it amortize. The equity-method drag above (OpenAI's loss flowing onto MSFT GAAP at $3.1B/qtr) is the *visible* cost; the *deferred* one is the depreciation that a long assumed useful life is borrowing from a future writedown.
