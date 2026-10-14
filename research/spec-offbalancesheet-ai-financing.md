# Off-balance-sheet AI financing - the rolling

*As of 2026-10-14. Companion to `spec-offbalancesheet-ai-financing.json`. The block's main edges are structural overlay; it also carries a dedicated `obs_edges` ledger that is deliberately NOT ingested into the main financial graph (so the published financial SCC stays 12). The core-robustness harness reads `obs_edges` to compute the circular core WITH vs WITHOUT off-balance-sheet rolling. Grading is per-claim: fact | estimate | interpretation.*

## The mechanism

The AI buildout's capex is enormous, and much of it is structured so it does **not** appear as debt on the hyperscaler parent's balance sheet. Three forms:

- **Operating leases** - the parent leases datacenter capacity instead of owning it; the commitment shows up in lease-commitment footnotes, not as funded debt.
- **SPVs / JVs** - a bankruptcy-remote vehicle, funded by outside equity and private credit, builds the facility and leases it back to the parent.
- **Chip-collateralized SPVs** - the same idea at the hardware level: a vehicle holds the GPUs and the parent (or a neocloud) rents access.

Accounting for these structures is permitted under GAAP. The point here is not that anything is concealed illegally - it is that the **economic leverage is real and the rating agencies and the BIS are adding it back**.

## The open-record figures

- **Oracle** - S&P added roughly **$260B of uncommenced lease commitments** (FY2027-2029) plus about **$13B of unconditional purchase obligations** to Oracle's adjusted debt in the July 2026 BBB- downgrade (Oracle 10-K FY2026; S&P).
- **The hyperscaler aggregate** - Moody's tallies about **$969B of total future lease commitments** across Amazon, Meta, Alphabet, Microsoft, and Oracle, of which about **$662B is uncommenced** - roughly **1.13x their combined adjusted debt**.
- **Amazon** - a roughly **$8B chip-collateralized SPV** for rented-out chip access, kept off balance sheet.
- **Meta** - the **Hyperion** datacenter in Louisiana, financed through a roughly **$27-30B SPV** (Blue Owl equity about 80%, a PIMCO-led debt tranche, via the Beignet investor vehicle), structured to stay largely off Meta's balance sheet.
- **The private-credit roster** - NVIDIA named Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs, and KKR to mobilize over **$500B** of third-party AI-compute capital, much of it insurance- and annuity-funded (Apollo/Athene, KKR/Global Atlantic). The BIS flagged this off-balance-sheet "shadow borrowing" in its March 2026 Quarterly Review.
- **CoreWeave** - GPU-collateralized bankruptcy-remote SPVs (an **$8.5B** fourth delayed-draw term loan; a **$2.6B** loan with a Cash Trap Event clause).

## Why it is modeled separately

The existing published circular-financing core (the SCC of 12, robust 11) is computed over the **on-balance-sheet** financial edges only. Promoting the off-balance-sheet structures straight into that graph would silently change the headline number. Instead the `obs_edges` ledger is kept out of the main graph and fed to the robustness harness, which reports the core **with and without** the rolling - so the effect of off-balance-sheet financing on the circular core is **measured, not assumed**. Each `obs_edge` carries the money-flow direction in both legs where a real return flow exists (capacity out, rent or revenue back), so any cycle the harness finds is a real economic loop, not an artifact.

## What the harness is expected to show

The hypothesis - stated as a hypothesis, to be confirmed by the numbers in `report/CORE-ROBUSTNESS.md` - is that off-balance-sheet rolling (a) sharply increases the dollar weight on the existing core nodes (Amazon, Oracle, Meta, Microsoft) and (b) pulls the financiers and SPV/insurer nodes (Apollo, Blackstone, Blue Owl, PIMCO, Athene, the chip-collateral SPV, Beignet/Hyperion) toward the strongly-connected core via the lease-back return legs. The report states which of those actually happens.

## Cross-references

`spec-chip-collateral-spv` (the hardware leaseback) | `spec-ai-compute-credit-risk` (the private-credit / insurance funding + rating treatment) | `spec-oracle-ai-credit-lynchpin` and `spec-coreweave-credit-stress-2026` (named cases) | `fin-meta-family` and `macro-cre-privatecredit` (Hyperion SPV) | `fin-coreweave-oracle` (the Moody's lease-commitment tally).
