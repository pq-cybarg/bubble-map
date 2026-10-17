# The AI-datacenter nuclear buildout

*As of 2026-10-16. Companion to `spec-ai-nuclear-smr-buildout.json`. Supply-side complement to `energy-power` (which carries the buyer-side PPA summary). Overlay/structural edges only - PPA terms and dollar figures live in notes, so the financial proof core is untouched. Grading is per-claim: fact | interpretation | caveat.*

## The headline

Every major AI hyperscaler has signed at least one nuclear power agreement for datacenter load. Trackers count roughly **13 announced projects totaling more than 9.8 GW** - the largest corporate nuclear-procurement wave on record. Two distinct structures: **restart/PPA** of existing reactors (nearer-term) and **new-build SMRs** (2030-2035), with a subset where the hyperscaler also takes **equity in the reactor developer**.

## The deals (fact)

- **Microsoft - Constellation (Three Mile Island / Crane):** a 20-year, ~$16B PPA to restart TMI Unit 1 (835 MW, rebranded the Crane Clean Energy Center); FERC transmission waiver approved **June 1, 2026**; first power targeted **H2 2027**. The most-advanced deal and the first new capacity that will actually serve datacenter load.
- **Amazon - X-energy + Talen:** Amazon invested **~$700M in X-energy** (up to 12 Xe-100 reactors) **and** bought an AWS campus beside Talen's Susquehanna plant (PA), buying up to **1,920 MW via the grid** through 2042 - after FERC **rejected** the original behind-the-meter interconnection amendment (Nov 2024).
- **Google - Kairos Power:** a master agreement, 50 MW demo scaling to **~500 MW by 2030** (KP-FHR molten-salt reactors) - the first corporate next-gen-SMR fleet deal.
- **Meta** (the largest commitment, up to ~6.6 GW): **TerraPower** Natrium (~8 plants, ~2.8 GW, Gates-backed) + **Oklo** (~1.2 GW Aurora) + a 20-year PPA for **~1,121 MW from the Clinton plant**.
- **Oracle:** a 1 GW datacenter design powered by 3 SMRs (permits secured).

## The vendor-financing loop (interpretation, labeled)

The structural echo of the chip thread: in the **equity-stake subset**, a hyperscaler funds the reactor builder it will then buy power from. **Amazon - X-energy** ($700M stake + offtake) is the clearest case; **Sam Altman's chairmanship of Oklo** (via his AltC SPAC, from which he stepped down in April 2025 to clear a path for potential OpenAI-Oklo dealings) is the governance version - OpenAI's power demand on one side, an Altman-chaired reactor developer on the other. This loop applies to the equity subset, **not** to the pure PPAs, and intent is not asserted.

## The critical caveat (fact)

**No datacenter anywhere yet runs on a new reactor built for it.** The first new capacity online is the TMI restart in H2 2027; the SMR fleet deals deliver roughly 2030-2035. And SMR economics are unproven at scale: **NuScale** has the first NRC-certified SMR design, but its flagship UAMPS/Carbon Free Power Project was **canceled in 2023** on cost overruns. A further gating constraint is **HALEU** fuel - the Xe-100 and most advanced SMRs need high-assay low-enriched uranium, a supply bottleneck historically dominated by Russia. So the buildout is, today, overwhelmingly **commitments, not delivered power**.

## How it wires into the map

New supply-side nodes: `X_energy`, `Kairos_Power`, `Talen_Energy`, `NuScale` (joining existing `Oklo`, `TerraPower`, `Constellation_Energy`, `Vistra`, `Nuclear_SMR`, `HALEU_Enrichment`). Edges run hyperscaler -> developer/utility (the deals), `Sam_Altman -> Oklo` (the governance tie), `X_energy -> HALEU_Enrichment` (the fuel bottleneck), `NuScale -> Nuclear_SMR` (the cautionary cancellation), and `Nuclear_SMR -> AI_Datacenters` (the thesis, with the not-yet-delivered caveat). All structural overlay.

## Cross-references

`energy-power` (buyer-side PPA table + grid demand) | `macro-ai-power-grid-bottleneck` (the grid-interconnection wall) | `spec-datacenter-ratepayer-costshift` (the Susquehanna FERC fight and ratepayer cost-allocation) | `fin-nvidia-openai` (the chip vendor-financing loop this mirrors on the power side) | `spec-oracle-ai-credit-lynchpin` (Oracle's 1 GW / 3-SMR design in the credit context).
