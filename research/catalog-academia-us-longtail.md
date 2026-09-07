# US higher-education long-tail (chunk 1): coverage layer

A **coverage/enumeration layer** extending the R1-core academia block to the broader US university landscape - state flagships, major publics, notable privates, and HBCUs.

## What's here
~85 real, verifiable institutions (IPEDS/Carnegie): all 50-state flagship/land-grant universities, additional major publics (Purdue, the UC campuses, ASU, Virginia Tech, etc.), notable privates (NYU, Cornell, Duke, Penn, USC, Vanderbilt, Rice, Georgetown, etc.), and HBCUs (Howard, Morehouse, Spelman, FAMU, NC A&T). Each is a flat node with a `member` edge to the **US_Higher_Education** hub; the hub ties to **US_Government** (federal research funding).

## Documented signal ties (not just enumeration)
- **Penn State** -> Applied Research Lab (Navy UARC); **Texas A&M** -> nuclear/hypersonics/defense; **UMD** -> IC-adjacent research (ARLIS UARC); **Purdue** -> semiconductors/AI; **ASU** -> largest public + AI-in-education (OpenAI deal); **Johns Hopkins** APL (largest UARC, core node).

## Honest limits
This is **coverage, not exhaustive** - the US has ~4,000 degree-granting institutions; this chunk is ~85 flagships/majors/privates/HBCUs. Community colleges, for-profits, and the small-college long-tail are **deliberately excluded** (adding thousands of single-edge nodes would dilute the map). The `member` edges are **enumeration, not relationship claims**; only the handful of signal ties assert real connections. Everything is in the **academia** bucket, so it can be hidden via the bubble-map **Layers** panel. Further chunks can extend coverage if wanted.

*Sources: IPEDS / Carnegie Classification (existence); NSF HERD + federal-R&D + UARC records (signal ties). Cross-refs: US_Higher_Education, US_Government, AI, catalog-academia-core, catalog-academia-abroad, catalog-university-ip.*
