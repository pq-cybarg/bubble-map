# SEC filings — primary-source pass

*Web-verified 2026-06-08. Structured + EDGAR links: `spec-sec-filings-primary.json`. Re-anchors the proven core to the companies' **own mandatory disclosures** instead of press. Filings corroborate the proofs; they don't change them. "As-reported" is itself contestable (non-GAAP add-backs, segment definitions) — the same scrutiny the data-integrity block applies to government numbers applies here.*

## CoreWeave 10-K (FY2025) — CIK 1769628 · [EDGAR](https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000104/crwv-20251231.htm) — *STRONG*
- Revenue **~$5.1B**.
- **Customer concentration: ~67% from Microsoft**; backlog anchored to a few counterparties — OpenAI **~$22.4B**, Meta **~$35.2B** implied, Anthropic, Jane Street.
- **Debt > $21B** (from **<$8B** in 2024); large portion **variable-rate ~11%**; **Q4-2025 interest $388M ≈ ⅓ of revenue**.
- **Net loss ~$1.2B**; 43 sites, >850 MW; continued dependence on financing + stable power.
- Risk factors explicitly flag few-customer dependence, contract renegotiation/cancellation, and customers building in-house compute.

> This is the **cascade node** the TLA+ trace runs through: a neocloud that is ~⅔ one customer with ~$21B of variable-rate debt eating ⅓ of revenue. The 10-K's own concentration + leverage language *is* the `OpenAI → CoreWeave → Oracle` fragility, in legalese.

## NVIDIA 10-K (FY2025) — CIK 1045810 · [EDGAR](https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000023/nvda-20250126.htm) — *STRONG*
- Customer concentration disclosed: **Direct Customer A ~12%, B ~11%, C ~11%** (each ≥10%).
- Subsequent: **top-4 ≈ 61%** of Q3-FY2026 sales; concentration grew **~36% → ~61%** in a year.
- Risk factor: *"a significant amount of our revenue stems from a limited number of partners and distributors… revenue could be adversely affected if we lose… any of these end customers."*

> NVIDIA's filing confirms the **demand side of the loop** is a handful of buyers — the same hyperscalers/neoclouds it invests in. The 36%→61% tightening is the **SCC tightening**, and it corroborates the vendor-financing self-funding metric (~10% funded / ~56% headline).

## Pull queue (next primary documents)
Microsoft 10-Q (OpenAI equity-method losses; the $135B-marked vs $13B-cash gap) · Oracle 10-K/Q (RPO backlog jump + Stargate-linked capacity + capex debt) · MSFT/AMZN/GOOG 10-K (capex run-rate; Amazon's Anthropic carrying value) · SpaceX/SPCX S-1 (CIK 1181412) · 13F cross-holdings (the equity edges of the SCC).

## Takeaway
The strongest corroboration of the circular-funding thesis is the **firms' own SEC risk factors**: CoreWeave and NVIDIA disclose the concentration and leverage the models formalize. The caveat is symmetrical with the data-integrity block — *"as reported" deserves the same zero-trust reading as the government's headline numbers.*
