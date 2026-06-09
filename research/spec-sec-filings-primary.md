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

## Microsoft 10-Q (FY2026 Q1, qtr ended 2025-09-30) — CIK 789019 · [EDGAR](https://www.sec.gov/Archives/edgar/data/0000789019/000119312526191507/msft-20260331.htm) — *STRONG*
- **~27% of OpenAI** (as-converted), **equity method**; **$13B** committed, **$11.6B funded** as of Sep 30 2025.
- OpenAI's losses flow through "other income (expense), net" — Q1-FY2026 other income showed a **~$683M loss**, "primarily… net recognized losses on equity method investments, including OpenAI."
- External reporting infers Microsoft's share implies an **OpenAI quarterly loss ≈ $11.5B+**.

> Primary confirmation of the Z3 result (**OpenAI needs ≥$1.03T external; insolvent at zero inflow**): Microsoft books its 27% share of OpenAI's losses, and the implied ~$11.5B/qtr burn is the cash the loop must keep raising. Reconciles the **$13B-cash vs ~$135B-marked** gap.

## Oracle 10-Q / 8-K (FY2026, qtr ended 2025-11-30) — CIK 1341439 · [EDGAR](https://www.sec.gov/Archives/edgar/data/0001341439/000119312525315925/orcl-20251130.htm) — *STRONG*
- **RPO ~$523.3B** (Nov 30 2025; +~359% YoY in a prior quarter) — a backlog **dominated by OpenAI/Stargate** cloud capacity.
- OCI revenue guided on a hockey-stick: **$18B → $32B → $73B → $114B → $144B**.
- **≥$72B of data-center partner debt** for Stargate: **$16.3B** Michigan (largest single-facility tech debt ever), **~$38B** Texas/Wisconsin, **~$18B** New Mexico.
- **PIMCO anchored ~$10B** of the Michigan bond **after US banks retreated**.
- FY2026 capex **~$50B** (>2× prior year); **$18B of public bonds sold in a single day** (Sep 2025) to fund OpenAI data centers.

> The clearest primary picture of the loop's funding mechanics: a **$523B backlog that is largely one circular counterparty** (OpenAI/Stargate), financed by **≥$72B partner debt + $50B capex + $18B bonds** — with **private credit (PIMCO) the marginal lender** when banks pull back. This *is* "solvent only while capital keeps flowing," in Oracle's own filings.

## Amazon (CIK 1018724) & Alphabet (CIK 1652044) — *STRONG*
- **Amazon:** ~**$200B** 2025 capex (mostly AI); booked a **~$9.5B pre-tax gain** in Q3-2025 from **marking up its Anthropic stake** after Anthropic's $13B raise at a **$183B** valuation; committed up to a further **$25B** (Apr 2026).
- **Alphabet:** 2026 capex guided **$180–190B** (raised from $175–185B), 2027 to "significantly increase"; also a fair-value Anthropic stake (billions in gains) and **~$100B SpaceX** equity.

> **Key accounting finding.** The *same* circular AI stakes distort hyperscaler earnings in **opposite** directions by method. **Fair value** (Amazon, Google on Anthropic): a higher private round = a **gain** booked to profit — Amazon's Q3-2025 profit got a **$9.5B lift from revaluing a company it is simultaneously funding**. **Equity method** (Microsoft on OpenAI): the investor books its **share of losses** (~$11.5B/qtr implied). So the loop flatters Amazon/Google reported profit and drags Microsoft's — and the Anthropic IPO will finally test those private marks against a public price. *Treat hyperscaler "AI gains" as partly self-referential paper marks.*

## NVIDIA 13F-HR (Q4 2025) — CIK 1045810 — *STRONG*
- **~11% of CoreWeave** (~47.2M shares, **~$3.66B**; added ~$2B in Q4); **Intel ~$7.9B** (~50% of the 13F portfolio — funding a rival/foundry); **Nebius ~$100M**; plus Synopsys, Nokia, Coherent; exited Applied Digital, Arm, Recursion, WeRide.

> The vendor-financing loop in NVIDIA's **own** filing: it owns ~11% of CoreWeave — a neocloud that is ~67% Microsoft and exists to buy NVIDIA GPUs. The equity edges of the SCC, disclosed by the chipmaker itself.

## Oil / Dubai note
The commodities block (`macro-futures-vs-physical`) now carries the **Brent–Dubai EFS** (the sour/Asia differential): it narrowed and flipped **negative (−11¢, Aug 2025)**, expected to widen in 2026 on OPEC+ sour supply.

## Pull queue (remaining)
The eventual **Anthropic / OpenAI S-1** (will test the private marks) · SpaceX S-1 (summarized in `fin-spacex-spcx`) · full 13F text parse for MSFT/AMZN/GOOGL institutional cross-holdings.

## Takeaway
The strongest corroboration of the circular-funding thesis is the **firms' own SEC risk factors**: CoreWeave and NVIDIA disclose the concentration and leverage the models formalize. The caveat is symmetrical with the data-integrity block — *"as reported" deserves the same zero-trust reading as the government's headline numbers.*
