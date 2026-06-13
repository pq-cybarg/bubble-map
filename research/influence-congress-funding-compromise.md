# Congress as a funding/compromise surface — committees of jurisdiction, non-linear bill flow, and the documented money-and-leverage map

*Built 2026-06-12 from `research/influence-congress-funding-compromise.json` + `data/congress_committees.json`. Sources: House/Senate rules + Congress.gov (jurisdiction & bill histories), the Congressional Record / conference reports & the Federal Register (term-changes & resulting rulemakings), FEC + OpenSecrets (money), House Clerk / Senate financial disclosures incl. STOCK Act periodic transaction reports (personal holdings & trades), and Lobbying Disclosure Act filings (staff→lobbyist chains). `fetch_fec.py` wires the FEC API behind an env-gated key.*

> **Evidentiary discipline (read first).** Donation + vote alignment is **correlation, not a bribe**. Adjacency is **not** intent. This block builds a transparent **leverage/exposure** map from public records and grades every cell. It does **not** assert that any named member is "bought." "Degree of exposure" is a structural index (the rubric below), never a corruption verdict. All overlay edges (`pac_funding`, `revolving_door`, `regulatory_legal`) are **excluded from the SCC/Z3/TLA+ proofs**. Dollar figures not yet pulled from primary FEC/disclosure data are marked **REQUIRES-INGEST** and are **not fabricated**.

## 1. Why model Congress as a system, not a list
The financial/AI/surveillance fights are won or lost in legalese, in **three moves the public record under-reports**:

1. **Committees of jurisdiction are chokepoints.** Each regulated industry's bills live in a specific committee; the membership of that committee is *where the money concentrates by construction* — finance PACs fund the Banking/Financial-Services seats regardless of who holds them.
2. **Bill flow is non-linear.** A bill's operative terms are written, gutted, and re-inserted across subcommittee markup, manager's amendments, floor amendments, conference, and — the lowest-visibility vehicle — **lame-duck omnibus attachments**. The headline ("sweeping reform" / "modernization") is written at introduction; the **terms that bind** are often changed later, with far less coverage.
3. **Members carry documented financial exposure** — industry donations, household securities/commodity/real-estate/debt positions, and post-office employment — that constitutes **leverage**, not proof of a quid pro quo.

## 2. The exposure rubric (a hypothesis generator, not a verdict)
A reproducible **leverage/exposure index** for a member on a policy domain. Every component is a public-record fact; the composite is explicitly an interpretation.

| | Component | What it measures | Strength |
|---|---|---|---|
| **C1** | Industry money | share of receipts from the regulated industry's PACs/employees vs. chamber median (FEC) | **weakest** — industry funds the seat, not the disposition |
| **C2** | Personal position | household securities/commodity/real-estate/debt in the industry; trade timing vs. nonpublic committee info (STOCK Act PTRs) | strong when timing is anomalous |
| **C3** | Revolving door | prior/【post】-office employment by the industry | **strongest, cleanest** |
| **C4** | Vote/term alignment | authored **amendments that change operative terms** in the industry's favor (the misreported layer) | strong |
| **C5** | Family/affiliate & staff | household trades; former staff turned industry lobbyists; leadership-PAC overlap | structural |
| **C6** | External leverage | documented threats/kompromat/foreign-agent ties/debt to interested parties | high-grade-required; mostly **unsupported**, left so |

**High composite = high structural exposure = incentives aligned by construction.** It tells you *where to read the primary record*, not *that a crime occurred*. **C3 and C2 survive scrutiny most often; C1 alone is near-noise.**

## 3. Committees of jurisdiction → the industries they gate
*(full membership rosters in `data/congress_committees.json`; chairs profiled in the Persons tab)*

- **Senate Banking / House Financial Services** → banks, Fed, SEC/CFTC, CFPB, stablecoins, crypto, housing. *"The cash committee."* Top sectors: securities & investment, insurance, commercial banks, real estate.
- **Senate Finance / House Ways & Means** → taxation, trade/tariffs, **carried interest** (PE/hedge funds), R&D/depreciation (AI capex), chip export schedules.
- **House/Senate Judiciary** → antitrust, Section 230, **FISA**, crypto enforcement, Big Tech.
- **House/Senate Intelligence** → IC oversight, **FISA 702**, TikTok/RESTRICT, cyber attribution.
- **Armed Services** → the **NDAA** must-pass vehicle (defense-AI, space, procurement).
- **Energy & Commerce / Energy** → **data-center power & grid**, critical minerals, spectrum.

## 4. Bill flow — the non-linear, misreported term-changes (case studies)
These are the cases where the **operative term** entered or changed **after** the headline was written.

- **GLBA (1999).** The repeal of bank/securities/insurance separation was never in doubt; the *fought* terms were CRA scope and the umbrella-supervisor question — and the consequential **omission was any systemic-risk supervisor at all**, the gap 2008 exposed. Reported as "modernization"; reality, it ratified conglomerates already built (Citicorp-Travelers) and policed none of them. **Grade: fact.**
- **CFMA (2000).** The decisive term — **exempting OTC derivatives/swaps from CFTC and SEC oversight** (plus the "Enron loophole") — was attached as a ~262-page rider to an **11,000-page lame-duck omnibus** after the election, bypassing committee scrutiny. The clearest case of operative terms entering through a low-visibility vehicle; it foreclosed Brooksley Born's 1998 warning. **Grade: fact.**
- **SOX (2002).** A rare reversal: WorldCom's mid-process collapse shifted leverage to the **stronger Senate (Sarbanes) version**, which prevailed in conference over the industry-friendlier House text. Targeted accounting fraud, not leverage — so it did nothing for 2008. **Grade: fact.**
- **Dodd-Frank (2010).** As **passed** it was materially weaker than as **introduced**: the Brown-Vitter hard size-cap **failed**, the Volcker Rule gained loopholes, and the Lincoln **swaps push-out was repealed in 2014 via a Citigroup-drafted rider** in a must-pass spending bill. The real fights then **migrated to ~400 Federal-Register rulemakings** — the layer press coverage never follows. **Grade: fact.**
- **JOBS Act (2012).** Lowered the public-disclosure floor for "emerging growth companies" and legalized general solicitation — quietly reducing the disclosure burden on exactly the **pre-IPO tech cohort** now central to the AI cycle. **Grade: fact.**
- **S.2155 (2018).** One operative change — raising the SIFI threshold **$50B → $250B** — removed **SVB (~$210B), Signature, First Republic** from the strict regime. Sold as "community-bank relief"; the beneficiaries were large regionals, and the **2023 failures are the empirical test**. **Grade: fact; the causal link to 2023 is contested.**
- **CHIPS (2022).** Stripped from the broad USICA/COMPETES bills to a ~$52B subsidy + ITC + China guardrails — a **direct state vendor-financing of the chip supply chain** (the same circular state-as-financier pattern as critical minerals). Recipients (Intel, TSMC Arizona, Samsung, Micron) map to the chip-chokepoint block. **Grade: fact.**
- **FIT21 / GENIUS (2024–25).** The decisive terms — **which tokens are CFTC "commodities" (light) vs SEC "securities" (heavy)**, and the 100%-reserve/yield-free stablecoin model — were drawn **toward the lighter regime with direct industry input** (Coinbase, Circle, a16z). The "regulation" is also a grant of legitimacy and a shield from the prior enforcement posture. **Grade: fact + labeled interpretation.**

## 5. The documented money-and-leverage findings (graded)
- **Chair → regulated megabank revolving door (C3, cleanest).** Phil Gramm (GLBA/CFMA author) → **UBS** vice-chairman; Jeb Hensarling (HFS chair) → **UBS** vice-chairman; John Dugan (OCC) → **Citigroup** chairman; Robert Rubin (Treasury) → **Citigroup**. **Grade: fact.**
- **Member → the exact firm later distressed.** Barney Frank (Dodd-Frank co-author) → **Signature Bank** board; regulators seized Signature in March 2023. Irony, **not** causation. **Grade: fact.**
- **Member → aligned media/crypto-treasury vehicle.** Devin Nunes (House Intel chair) → **CEO of Trump Media** (Bitcoin treasury / Truth.Fi). **Grade: fact.**
- **Congressional trading vs. committee information (C2).** The **Pelosi household's** well-timed mega-cap-tech option exercises (the engine of the bipartisan trading-ban push) and **Sen. Richard Burr's** (Intel chair) Feb-2020 pandemic-timed equity sales (DOJ/SEC inquiry, closed without charges). Trades and inquiries are public record; **intent unproven**. **Grade: fact (record); intent unproven.**
- **Sector-donation concentration (C1, weakest).** Banking/Financial-Services members draw securities/insurance/bank/real-estate PAC money far above the chamber median — *because the seat regulates those industries*. Near-noise as evidence of disposition. **Per-member dollar totals are REQUIRES-INGEST (FEC/OpenSecrets), not asserted here without the primary pull.**
- **Leadership PACs & the staff→lobbyist pipeline (C5).** Chairs redistribute industry money via leadership PACs (buying intra-caucus influence), and senior staff become LDA-registered lobbyists who **draft the very term-changes** in §4. Exhaustive staff→lobbyist mapping is **REQUIRES-INGEST** (LDA + employment records).

## 6. Coverage & honest limits
**Here now:** the jurisdiction map, the non-linear bill histories with their misreported term-changes, the cleanest leverage findings, a transparent rubric, the committee-membership roster layer (`data/congress_committees.json`), and overlay edges into the bubble map (revolving-door / PAC, **excluded from the proofs**).

**REQUIRES-INGEST (wired, not fabricated):** per-member FEC/OpenSecrets dollar totals by industry across 26 years; full STOCK-Act PTR parsing; exhaustive staff→lobbyist (LDA) chains; per-member real-estate/debt disclosures. `fetch_fec.py` calls the FEC API behind an **env-gated `FEC_API_KEY`** (the FINRA pattern — no key in the repo) and tolerates absence, so the quantitative layer is reproducible.

**By design:** the full **~2,000-member roster across 13 Congresses** is delivered as a **roster-data layer + this analytical block**, not as 2,000 hand-authored dossiers (the accepted roster-segmentation approach). The committee chairs and the highest-leverage members **are** profiled at depth in the Persons tab. **Nothing here is a corruption verdict — it is a leverage/exposure surface for reading the primary record.**
