# NDFI-to-regulated-bank contagion via collateral fraud

*Event date October 2025; recorded 2026-10-15 as documented history. Companion to `spec-regional-bank-ndfi-fraud.json`. This is the concrete, named case of a channel the corpus otherwise tracks abstractly: stress in non-bank lending reaching a regulated bank's balance sheet. Grading is per-claim: fact | allegation | interpretation.*

## Disambiguation first

The "Cantor Group" borrower here is a **commercial-real-estate fund group** - it is **not Cantor Fitzgerald** (the Lutnick firm). They are unrelated. The map nodes it as `Cantor_Group_CRE` to keep them apart.

## What happened (fact)

In mid-October 2025, two regional banks disclosed losses on loans to the same borrower group:

- **Zions Bancorporation** filed to report "apparent misrepresentations and contractual defaults" on two related commercial-and-industrial loans totaling about **$60M** from its California Bank & Trust division. It took a provision for the full amount and **charged off about $50M** in Q3 2025, and sued to recover more than $60M lent to investment funds **Cantor II and Cantor IV**, which had drawn revolving credit facilities to buy **distressed commercial-mortgage loans**.
- **Western Alliance**, the next day, disclosed it had sued the same leadership group (including **Cantor Group V**), alleging **forged title-insurance documents** that concealed overlapping liens, and sought roughly **$100M**.

The alleged mechanics: borrowers secretly subordinated or transferred collateral (stripping the banks' security interests) and forged title documents to hide overlapping claims. These are **allegations** - the litigation was pending and the borrowers were not adjudicated.

## Market reaction (fact)

Zions fell about **12%** and Western Alliance about **11%**; the KBW Nasdaq Regional Banking Index dropped about **4%**, with spillover to Great Southern Bancorp, Customers Bancorp, and Hingham. Commentators drew comparisons to the 2023 SVB / First Republic episode.

## The backdrop (fact + labeled interpretation)

Days earlier, JPMorgan's Jamie Dimon had cited the **Tricolor** (subprime auto) and **First Brands** (auto parts) bankruptcies: *"when you see one cockroach, there's probably more."* The Zions/Western Alliance disclosures landed into that credit-anxiety backdrop, which is why an idiosyncratic two-loan fraud triggered a sector-wide move. Whether it is a leading indicator of systemic NDFI contagion or an isolated fraud is **contested**:

- **Isolated read** (recorded): Zions said its total criticized assets were *lower* than at June 30, 2025; Western Alliance affirmed guidance; Stephens' analyst said the loans were unconnected to the recent bankruptcies and sat in an independent fund. Analysts later called the selloff "overblown."
- **Contagion read** (recorded): the episode made bank lending to **non-depository financial institutions (NDFIs)** the post-October-2025 watch item - the channel by which a regulated bank absorbs the credit and collateral risk originated by a non-bank fund.

## Why it is in the map

It is the documented instance of the exact linkage the corpus models between private credit / NDFIs and regulated banks (`macro-private-credit-bdc-stress`, `macro-uncovered-risk-pools`, `macro-cre-privatecredit`). The two bank-to-fund loans are carried as real financial edges; the funds' use of proceeds (buying distressed commercial mortgages) ties the episode to the CRE and mortgage-market threads. These nodes are isolated from the AI-compute circular core, so the published financial SCC is unchanged.

## Cross-references

`macro-private-credit-bdc-stress` and `macro-uncovered-risk-pools` (the NDFI channel) | `macro-cre-privatecredit` (the CRE/private-credit overlap) | `spec-auto-credit-unwind` and `macro-firstbrands-ubs` (the Tricolor / First Brands "cockroaches" Dimon referenced) | `macro-fdic` (the regulated-bank backdrop).
