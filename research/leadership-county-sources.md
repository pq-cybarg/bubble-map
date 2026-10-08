# County-tier leadership sources - provenance, confidence, and bias audit

*(Methodology for the county-government tiers of the leadership map (#196-199: county executives/boards, row officers, district attorneys, coroners/MEs). No single source is simultaneously authoritative, free, all-county, current, and inclusive of the odd offices - so the plan is a labeled combination, and EVERY ingested record will carry its source + a confidence tag + a vintage. This doc states, for each source: what it is, what it is justifiably good for (and NOT), who publishes it and why, and the biases that follow from that. It is deliberately even-handed - including about sources whose own framing is partisan.)*

## Why this audit exists
Mapping officeholders is only as honest as its sources. Three failure modes to pre-empt: **(1) staleness** (a 2019/2021 roster read as "current"); **(2) coverage bias** (large/urban counties over-covered, rural under-covered, skewing any demographic/partisan read); **(3) framing bias** (an advocacy publisher's selection + coding choices quietly importing its conclusion). Each source below is tagged for all three. The leadership map is a **separate overlay - NOT part of the formally-verified funding graph or any proof** - and these are **public elected officials** (public record); the composition/apophenia guards still apply (do not impute collective intent from a directory).

## 1. US Census of Governments (US Census Bureau)
- **Provenance:** Federal statistical agency; the Census of Governments runs every 5 years (years ending in 2 and 7). Public domain.
- **Justifiably good for (HIGH confidence):** the **universe + structure** - how many county governments exist (~3,069), which offices are elective vs appointed **by state**, board/commission structure, county type. The authoritative denominator against which to measure coverage.
- **NOT good for:** **named individuals** - it does not publish incumbents. Zero confidence for "who holds office."
- **Publisher interest / bias:** nonpartisan benchmark production; low ideological bias. Real biases are **definitional** (what counts as a "general-purpose government"), **timing lag** (5-year cycle - structure can change between waves), and **self-report** (governments report their own structure). Budget/political pressure on the Bureau is a background risk, not a visible tilt. Its goal is consistent statistics, not a narrative.
- **Use here:** scaffold the office taxonomy + the per-state "which county offices are elected" map, and bound coverage honestly.

## 2. American Local Government Elections Database (ALGED)
- **Provenance:** Peer-reviewed academic - de Benedictis-Kessner (Harvard), Lee & Velez (Columbia), Warshaw (GWU); *Scientific Data* 10:912 (2023); archived on **OSF, DOI 10.17605/OSF.IO/MV5E6**, **CC-BY-NC-SA 4.0**. ~78k candidates / 57.5k contests; offices incl. **County Executive, County Legislature, Sheriff, Prosecutor** (plus mayor/council/school board), 1990-2021/22.
- **Justifiably good for (HIGH for large counties; MODERATE for "current"):** **election returns + candidates** in counties **>50k population** (~1,005 counties). Peer-reviewed and cross-validated against Ballotpedia + Reflective Democracy, so the data quality is high **for what it covers**. Confidence drops to MODERATE for "current incumbent" because it is **returns through ~2021** - a 2020 winner may since have lost, resigned, or termed out.
- **NOT good for:** **small counties (<50k)** - systematically absent; **coroners + row officers** (clerks/treasurers/assessors/recorders) - not among its seven offices; **anything after ~2021-22**.
- **Publisher interest / bias:** academic incentives (publication, methodological novelty) push toward accuracy, but the research program is **urban/representation politics**, so the **>50k-population cutoff is a structural bias** that over-represents urban/suburban counties and **under-represents rural ones** - which materially skews partisan + demographic composition if used as if national. It inherits upstream **vendor biases** (Ballotpedia notability thresholds; official-returns gaps). The authors study representation/polarization, so their **variable choices** (demographic + partisan coding) reflect those interests - the **raw returns** are neutral; the **derived demographic fields** carry more researcher judgment. Funding is academic (low commercial bias).
- **Use here:** county executives, county legislatures, sheriffs, prosecutors in >50k-pop counties, every record stamped "ALGED, election-year YYYY, large-county universe, may be stale."

## 3. Reflective Democracy Campaign (wholeads.us)
- **Provenance:** A research + **advocacy** project of the **Women Donors Network** (a progressive donor network). Published datasets on the **demographics of elected prosecutors** (2,800+, 2019) and city officials **including coroners** (1,180). **Status caveat:** the site is **currently "under construction"**; datasets are now **by request** (hello@wholeads.us), not direct download.
- **Justifiably good for (MODERATE, dated):** a genuine **named compilation** of elected prosecutors + some coroners as of **2019** - usable to cross-check names, not as a current roster.
- **NOT good for:** currency (6 years stale), completeness (office-selective), or neutral interpretation.
- **Publisher interest / bias (declared, strong):** its **explicit mission** is documenting the over-representation of white men in elected power to motivate **demographic-representation reform** - a **progressive viewpoint**, openly stated. Consequences: **office selection** emphasizes where disparities are starkest; **demographic coding** is by observation/inference (error-prone and itself a judgment); **donor-network funding** creates an incentive to foreground disparity. The underlying "who is the elected DA in county X" roster is a real primary compilation and usable **with attribution**; any **interpretive** claim about representation is **viewpoint**, labeled as such - not laundered into fact. (This is the same treatment the project gives any advocacy source, left or right.)
- **Use here:** secondary cross-reference for DA/coroner **names (2019)**, explicitly viewpoint-sourced + dated; verify against official .gov pages where possible before publishing a name.

## 4. NACo County Explorer (National Association of Counties)
- **Provenance:** NACo is the **membership + lobbying association** for US counties (est. 1935). County Explorer is offered "as-is, noncommercial public use."
- **Justifiably good for (MODERATE-HIGH):** county **structure** (which offices are elected, board composition, county classification) - they represent counties, so structural data is reliable.
- **NOT good for:** a neutral read on county finance/policy, or (largely) named individuals.
- **Publisher interest / bias:** a **trade association** whose purpose is to **advance counties' interests** - more federal funding, fewer unfunded mandates, more local control. Structural/definitional data is low-bias; any **finance or policy framing** tilts **pro-county-government** (counties as capable, under-resourced, deserving autonomy). Reliable on "what the office is," not a disinterested judge of "how well counties govern."
- **Use here:** corroborate the office taxonomy from source #1; not a names source.

## The currency alternative not chosen (for the record)
**Ballotpedia** (nonprofit Lucy Burns Institute) is the only option that is **current + comprehensive** (~15k offices, bulk CSV/JSON or geo-API), generally well-regarded for factual officeholder data and broadly nonpartisan in its officeholder tables; its limits are **commercial licensing** (paid) and **local rows refreshed ~annually** (a currency caveat, not a bias). It is the recommended **upgrade path** if/when a license is provided - it would replace the stale/partial free rosters with current names while this doc's bias tags still apply to any demographic overlays.

## How records will be graded on ingestion
Every county-tier record will carry: **source** (which of the above), **as_of** (dataset vintage or election year), **universe** (e.g., ">50k-pop only"), **status** (incumbent/term-dates where known), and a **confidence** tag derived from this audit:
- **HIGH** = structure from Census (#1), or a large-county officeholder cross-confirmed against an official .gov page.
- **MODERATE** = ALGED large-county returns treated as current (staleness risk), or a single-source name.
- **LOW / viewpoint-labeled** = Reflective Democracy names (2019) or any demographic/representation overlay.
- Small counties (<50k) and coroners/row officers will be marked **coverage-gap** until a current bulk source (Ballotpedia or official-site pulls) fills them - **no fabricated names.**

## Honest limits
This is a sourcing + bias audit, not an ingestion. The combination is **free and openly citable but dated and partial**; it will be labeled as such on every record. The biggest residual bias is the **large-county skew** (ALGED's >50k cutoff) plus the **2019/2021 vintages** - both disclosed, neither hidden. Advocacy-sourced material (Reflective Democracy) is usable for names with attribution but its framing is viewpoint, not fact. No officeholder name will be published that cannot be tied to a cited source.

*Sources: US Census of Governments (census.gov); de Benedictis-Kessner, Lee, Velez & Warshaw, "American Local Government Elections Database," Sci Data 10:912 (2023), OSF DOI 10.17605/OSF.IO/MV5E6, CC-BY-NC-SA 4.0; Reflective Democracy Campaign / Women Donors Network (wholeads.us); NACo County Explorer (explorer.naco.org); Ballotpedia / Lucy Burns Institute (ballotpedia.org). Cross-refs: leadership-map-analysis, the leadership map overlay.*
