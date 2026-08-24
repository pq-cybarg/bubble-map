# Connected-car & ALPR surveillance data streams -> data brokers -> ICE

**The pipeline in one line:** telemetry sold as "safety" becomes an enforcement-grade location dossier, because the same data-broker backbone that prices your insurance also sells person-search access to immigration enforcement.

## The five legs

1. **Connected vehicles emit precise data.** GM's OnStar (+ "Smart Driver") collected geolocation as often as every 3 seconds plus hard-braking/speeding/late-night behavior across Chevrolet/GMC/Cadillac/Buick.
2. **Automakers sold it to consumer-reporting brokers.** GM/OnStar sold that data to **LexisNexis Risk Solutions** and **Verisk**, which repackaged it for auto insurers (premium hikes and denials - one driver saw +80% after 603 shared entries). The FTC's final order (Jan 14 2026) bars GM from sharing geolocation/behavior data with consumer-reporting agencies for five years; **MDL No. 3115** (N.D. Ga.) names GM, OnStar, LexisNexis, and Verisk.
3. **The same brokers sell to ICE.** LexisNexis holds ICE contracts (Accurint Virtual Crime Center, ~$16.8M 2021; LEIDS ~$22.1M 2021-2026) for data on 276M+ people from 10,000+ sources. **Thomson Reuters CLEAR** has supplied DHS/ICE since 2017; a **$125M** 5-year deal (2026) adds voter-registration data. LexisNexis Risk sits under **RELX PLC**, structurally walled from its Legal & Professional arm.
4. **ALPR networks feed location history.** **Flock Safety**'s license-plate-reader network was accessed for ~4,000 immigration searches via local police acting for ICE ("side-door"), plus a CBP pilot (May-Aug 2025) halted after backlash; the University of Washington documented "back-door" access to 10+ Washington agencies' cameras. **Motorola Solutions** (Vigilant ALPR + body-cam/real-time-crime-center stack) is the other major plate-history source.
5. **Convergence in Palantir.** These feeds land inside ICE's Palantir-built case systems (Investigative Case Management / ImmigrationOS - see the Palantir deep dive), where disparate identifiers are fused into a single targetable profile.

## Grading

Corporate and contract facts are documented (FTC orders, procurement records, The Intercept/404 Media/UW reporting). The **"direct ICE access"** to Flock is graded on documented *indirect* access through local police; Flock disputes any hidden back door and says sharing is customer-controlled. Thomson Reuters denies its CLEAR data requires a warrant. Intent is not inferred from the existence of a data pathway - the point is that the pathway exists and is being used.

*Cross-refs: spec-palantir-surveillance (#216), spec-inqtel-portfolio (#218), car-insurance telematics (#184). Sources: every figure's URLs are in the matching `research/spec-auto-connected-surveillance.json`.*
