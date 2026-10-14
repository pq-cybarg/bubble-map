# Academia catalog: US elite / R1 core

*Companion to `catalog-academia-core.json`. Structural overlay layer (universities wired to already-mapped companies and people); every edge is graded in its note. This is the elite/R1 core chunk of the academia catalog - the broader long-tail of US institutions is a separate, ongoing chunk and is not claimed complete here.*

## What this block maps

Sixteen elite / R1 universities as nodes - Stanford, Harvard, MIT, UC Berkeley, Carnegie Mellon, Caltech, Princeton, Columbia, Yale, University of Chicago, Johns Hopkins, University of Washington, Georgia Tech, UT Austin, University of Michigan, UIUC, University of Pennsylvania - connected to entities already in the graph by three structural edge types. No dollar flows; these are origin, affiliation, and research-relationship ties, not funding edges.

## Edge types and grading

- **founder_origin** (fact): a company was founded out of a university's research or by its students. Stanford to Google (Brin and Page; the PageRank patent US6285999B1 is assigned to Stanford and was exclusively licensed to Google) and to Palantir (Thiel and Karp met at Stanford Law); Harvard to Meta (Zuckerberg) and Microsoft (Gates left in 1975); Princeton to Amazon (Bezos, BSE 1986); UIUC to a16z (Andreessen, from NCSA Mosaic to Netscape).
- **alumni_affiliation** (fact, except where marked): a named founder/leader holds a degree from the institution. Stanford to NVIDIA (Jensen Huang, MSEE 1992), Thiel (BA 1989, JD 1992), and a nominal tie to Musk (enrolled in a Stanford PhD in 1995, left within days); Caltech to Intel (Gordon Moore, PhD 1954); Penn to Musk (BA economics + BS physics, 1997). The Yale-to-Palantir tie is marked **weak** (illustrative of the PayPal-mafia network, not a founding fact).
- **federal_research_relationship** (fact vs contested): DARPA/DoD research performed at the institution. Strong, specific ties graded **fact** - MIT, Johns Hopkins (APL, a DoD UARC), CMU (robotics; the SEI FFRDC), Georgia Tech (GTRI), Stanford (SRI heritage), UC Berkeley, Caltech (and Caltech-managed JPL). For UW, Michigan, UIUC (NCSA), Columbia, Princeton, and UT Austin the general R1 federal-research status is fact but the **specific DARPA share is graded contested** - these are not asserted as DARPA-dominated.
- **talent_pipeline** (weak / contested): a university as a recurring source of AI-lab research talent - UChicago and Stanford and CMU into OpenAI, Berkeley into Anthropic. These are affiliation signals, **not funding**, and most are graded **weak**; the Stanford-to-OpenAI pipeline is graded **contested-strength** (real but hard to size).

## How to read it

The point is not that a university controls a company. The edges are **origin and affiliation provenance** - where founders trained, where foundational IP was assigned, which labs the government funds - carried as documented ties with their strength labeled. Talent-pipeline edges in particular are the weakest class and are flagged as such so they are not over-read as influence or money.

## Cross-references

`catalog-academia-abroad` (non-US institutions + tech-transfer ties) | `catalog-university-ip` (the patent/IP layer: PQC, biometrics, AI, surveillance assignments) | `catalog-crosslink-pass` (wiring the catalogs into the Digital-ID / AI / surveillance blocks) | `spec-palantir-surveillance`, `fin-nvidia-openai` (the destination entities).
