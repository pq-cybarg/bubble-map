# CoreWeave credit stress (H2 2026)

*As of 2026-10-14. Companion to `spec-coreweave-credit-stress-2026.json`. Overlay/structural layer only - all dollar and credit figures are in edge notes, so the formal solvency core is untouched. Grading is per-claim: fact | potential | interpretation.*

## What happened, plainly

CoreWeave has not defaulted and has not taken a new formal rating downgrade on 2026-10-14. What has happened is a **market-priced credit repricing**: its debt now trades at junk-level yields, its credit-default swaps earlier priced coin-flip default odds, and it is funding itself with dilutive equity and convertibles. The pure-play neocloud is showing, in live market prices, the same fragility the corpus maps structurally in `spec-oracle-ai-credit-lynchpin` (the investment-grade version) and `spec-ai-compute-credit-risk` (the private-credit and rating-treatment version).

## The facts

- **Debt priced as junk.** A 2031 unsecured bond yields in the low-to-mid teens - roughly a **15% cost of credit** by mid-October 2026. CDS priced about a **50% five-year default probability** in late July 2026. (CDS is a sentiment, liquidity, and fundamentals signal - not a prediction of default.)
- **Leverage.** Roughly **$51.6B of total debt against ~$5.5B of cash**, net leverage about **6.8x**, first-half adjusted-EBITDA interest coverage about **2.7x**, negative net margin.
- **Dilutive capital stack.** A **35-million-share at-the-market** equity program plus a **$3.0B** private offering of convertible senior notes due 2033. Dilution fear drove the October stock drop; the convertible also cuts interest cost - both are true.
- **Stock.** Down roughly **25% over six months**, gapping about **-4.4% on Oct 13** and about **-8% on Oct 8** amid an OpenAI-revenue report and an Asian-chip rout.

## The covenant channel (potential, not realized)

A **$2.6B loan**'s documents let a serious breach of a backing **customer** contract - a service-level or uptime failure that gives the customer the right to terminate - trigger a **"Cash Trap Event"** that traps cash and can accelerate repayment (Yahoo Finance / Benzinga, 2026-10-07). This is a concrete channel from an operational failure to credit acceleration. The clause is fact; it is a **trigger, not a declared event**.

## The Core Scientific entanglement

- The **CoreWeave-Core Scientific merger terminated** on 2025-10-30 after a failed Core Scientific shareholder vote.
- Core Scientific was later identified (WSJ, 2025-12-15) as the **delayed third-party data-center developer** behind CoreWeave's lowered 2025 guidance - multiple same-provider sites affected.
- The dependency runs **both ways**: CoreWeave funds part of Core Scientific's capex (about **$129.9M of $389.2M**) through colocation agreements. A builder's schedule slip feeds a cloud's guidance cut, while the cloud's cash backstops the builder.
- Core Scientific itself refinanced heavily in 2026: a **$3.3B 7.75% senior-secured-notes** offering due 2031 (2026-05-06) repaying its term loan and a **$1.0B delayed-draw bridge**, plus an August 2026 **$100M revolver + $500M letter-of-credit** facility - a crypto-mining balance sheet reused as AI-datacenter collateral.

## The other side

The credit picture is not all red: a reported **~$103.7B backlog** reduces demand uncertainty, interest is covered about **2.7x**, there is no liquidity crisis yet, and the convertible lowers interest cost. These are recorded so the thread is not one-sided. The open risks are customer renewals and GPU residual values against long-dated financing.

## How it sits in the map

CoreWeave is wired as a **source** into the structural concept-nodes it exemplifies: the AI-compute credit layer (the market-priced stress), the chip-collateral SPV (its GPU-secured delayed-draw loans are the archetype; the Cash Trap Event is the operational-to-credit channel), and - via the pre-existing edge - the neocloud refinancing wall. The new **Core Scientific** node points into CoreWeave (the merger-collapse and datacenter-delay entanglement) and into AI data centers (its crypto-to-AI collateral reuse).

## Cross-references

`spec-oracle-ai-credit-lynchpin` (the investment-grade analogue) | `spec-ai-compute-credit-risk` (rating treatment + private-credit/insurance layer) | `spec-chip-collateral-spv` (the GPU-SPV structure) | `spec-neocloud-refinancing-wall` (the maturity-clustered wall) | `fin-coreweave-oracle` (the Stargate-debt and capacity-commitment map) | `fin-nvidia-openai` (the vendor-financing loop CoreWeave sits inside).
