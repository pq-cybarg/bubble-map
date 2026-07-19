# Research brief — Dialog (organization)

> **Durable working brief.** This file exists so the Dialog research survives OS/session/context loss.
> It is the source of truth for scope + status. The live task list mirrors it as tasks #189–#195.
> Requested by user 2026-07-18. Not yet integrated into the bubble-map graph.

## What Dialog is (seed facts)

- **Dialog** — private, invitation-only society; "Bilderberg meets Silicon Valley salon." Off-the-record forum for executives, elected officials, academics.
- **Founded** 2006 by **Peter Thiel** and **Auren Hoffman**. **Executive Director: Raffi Grinberg**.
- **Ethos (as stated):** avoid "status signalling"; "shared preoccupation with artificial intelligence, longevity, and the near future"; "bi-partisan, albeit heavily libertarian-leaning." Topics span AI/healthcare/politics AND intimate themes (caregiving, relationships, mental health, the afterlife).
- **Membership grades A/B/C** set pricing/perceived value. **AI-built member dossiers** track political leanings, AUM, and discussion contributions.
- **Seed affiliates:** Thiel Foundation, Andreessen Horowitz, Founders Fund, NATO Defense College Foundation.
- **Venues:** Bacara Resort (Santa Barbara CA), Ritz-Carlton Dove Mountain (AZ), San Clemente Palace (Venice), Powerscourt Estate (Dublin). **Planned campus near Washington DC / Langley VA.**
- **Fees** reported >$10k/retreat (varies by grade).
- **Seed participants (leaked directories, ~110+):** Elon Musk, Eric Schmidt, Garry Kasparov, Ted Cruz, Cory Booker, Jonathan Haidt, Steven Pinker, Tulsi Gabbard, Jens Spahn, Ida Auken, Stanley A. McChrystal.
- **THE LEAK:** reporting references leaked member directories; user recalls a "Thiel files"-type leak. Provenance/scope/outlet to be pinned down (Dimension 1).

Seed source: https://en.wikipedia.org/wiki/Dialog_(organization)

## Epistemic standard (project rules)

- Grade every claim **documented vs claimed/rumored**; cite source URLs.
- **Presumption of innocence** — attendance/membership ≠ wrongdoing.
- **Composition/division guard** — the group's stated ethos is not each member's mind; don't impute the whole's traits to individuals or vice-versa. Institutional ACTION ≠ institutional MIND.
- **Confidentiality == concealment is ONE act** — read intent from what organizers SAY (and conspicuously omit), not from secrecy alone; absence cuts both ways.
- **No fabrication** of names, files, or citations.

## Dimensions (→ tasks)

| # | Task | Dimension | Status |
|---|------|-----------|--------|
| 1 | #190 | People (founders, leadership, associates, the leaked directory + leak provenance) | dispatched |
| 2 | #191 | Affiliates & institutional ties (Thiel network, a16z, Founders Fund, NATO DCF) | dispatched |
| 3 | #192 | Subentities, governance & membership mechanics (A/B/C grades, AI dossiers, legal form) | dispatched |
| 4 | #193 | Funding & structural/financial mapping (fees, backers, ownership chain, campus buy) | dispatched |
| 5 | #194 | Territorial resources & geographic footprint (venues + DC/Langley campus) | dispatched |
| 6 | #195 | Psychological group mentality / operational doctrine (secrecy, cohesion, ideology) | dispatched |

Synthesis EPIC **#189** is blocked by all six; on completion → build `research/spec-dialog-org.json` graph block + `research/*.md` writeup, integrate into bubble-map, hold SCC/audit/cross_review gate.

## Collected findings

_Agents return findings in their final message (background agents cannot write to disk). As each dimension lands, its structured output is pasted below and the status table updated._

### Dimension 1 — People — _COMPLETE (task #190)_

**THE LEAK (documented).** On **15 June 2026**, Swiss hacktivist **maia arson crimew** (prior: US No Fly List exposure, Verkada breach) found the members-only **dialog.org** had a "Directory List" of **113 names hardcoded in plaintext in the page HTML** — no credential/intrusion needed; underlying data sat in an inadequately access-controlled **Airtable** reachable by completing a web form. crimew tipped **WIRED**, which verified and published **16 June 2026**. A **separate anonymous source** gave WIRED the **222-person registration list** for the **2026 retreat** (Powerscourt Hotel, near Dublin, Aug 12–16 2026; 87 first-timers), tagged by status (active member / guest). Exposed dossier fields: biography, home city, email/mobile, birthdate, assistants' contacts, **political leanings**, **matchmaking/"looking for love" data** (dating.dialog.org), and private access tokens usable as login credentials (WIRED withheld these). Reporting (WIRED, The Dissent, Security Affairs) described an internal **A/B/C rating** tied to fame/wealth/influence/"political fit" (setting cost + seating; C-graded reportedly the most famous/influential) plus 1–4 contribution scores. Dialog called it an "attack" by a "well-known criminal wanted in the United States"; WIRED found no break-in was needed.

**Caveats.** WIRED cautioned the 113-name directory **does not indicate member vs participant vs past guest** (includes prior-year speakers/guests). The **Jeffrey Epstein / 2014 invite** claim was **RETRACTED** by WIRED & The Guardian — invite went to physicist Lisa Randall; the "Jeff Epstein" on the attendee list was a different person (ex-Oracle exec). Attendance ≠ wrongdoing.

**Roster (~73 documented names).** Founders **Peter Thiel** (Founders Fund/Palantir) + **Auren Hoffman** (chairman, Flex Capital); ED **Raffi Grinberg**. Government/policy: Scott Bessent (Treasury Sec), Ted Cruz, Cory Booker, Jared Kushner, Tulsi Gabbard (DNI), Dan Driscoll (Army Sec), Jim Himes, Larry Summers, Julian Castro, Randy Kroszner, Hallie Hoffman, Robert Hur, Jim O'Neill, Gen. Alexus Grynkewich (NATO SACEUR), Stanley McChrystal. Tech/VC: Musk, Marc Andreessen, Reid Hoffman, Joe Lonsdale, Greg Brockman, Jason Kwon (OpenAI), Chamath, Neal Mohan, Adam D'Angelo, Astro Teller, Jonathan Ross (Groq), Shivon Zilis, **Pete Shadbolt (PsiQuantum)**, Howie Liu (Airtable), Immad Akhund (Mercury), Meyer Malka, Matt Cohler, Jim Breyer, Eric Schmidt, Alex Karp (Palantir), Palmer Luckey (Anduril), Tom Lue (DeepMind), Yasmin Green (Jigsaw). Academics/media/culture: Haidt, Pinker, Kasparov, Bryan Johnson, Sam Harris, Ezra Klein, Bret Stephens, Souad Mekhennet, Roger Myerson, Jonathan Levin (Stanford pres), Anne-Marie Slaughter, Lisa Randall, Susan Athey, Rick Warren, Joseph Gordon-Levitt, Sophia Bush, Josh Brolin, Sarah Bond, Jonathan Greenblatt (ADL), Peter Goettler (Cato), Ryan Stowers (Koch Fdn), Simon Stevens (ex-NHS), Reema Al-Saud, Ali Jehangir Siddiqui, Jens Spahn (5×), Ida Auken. Full graded JSON (73 objects) in agent output — to fold into spec-dialog-org.json.

**Bubble-map hooks:** PsiQuantum (Shadbolt) → task #105; Palantir/Founders Fund/a16z/OpenAI/Anduril/DeepMind all already-modeled AI-capital-loop nodes. Strong integration surface.
> **KEY CORRECTION TO SEED PICTURE:** Dialog is operated by **Stonebrick, LLC** — a **for-profit LLC owned by co-founder Auren Hoffman** (address Mamaroneck, NY), NOT a chartered society/nonprofit. **Peter Thiel is co-founder + namesake but reportedly "has no hand in running Dialog"** (arm's length). ED **Raffi Grinberg** + managing director **Juliette Levine** run day-to-day. No 501(c)/990/state-registration for "Dialog" itself has surfaced. (Byline Times, single investigative outlet + public-records inference — but consistent across the funding & governance agents.)

> **A/B/C GRADE DIRECTION IS DISPUTED.** Governance + funding agents (WIRED-sourced) report **C = top tier** (most famous/influential, ~1 in 7), B = default majority (141/192 in leak), A = "polite holding pen" for older established-but-less-notable members. The mentality agent flagged other outlets frame it the opposite way. **What is well-documented: a wealth/fame-weighted ranking exists and drives price/seating/reinvitation; which letter is "top" is contested — present both.**

### Dimension 2 — Affiliates — _COMPLETE (#191)_ → `research/dialog/dimension2-affiliates.json`
Thin documented institutional ties (no website/statutes). **Thiel Foundation** = only Thiel entity with sourced direct tie (VA campus build-out). **Founders Fund + a16z** = documented as *participant/ideological backers* per the NATO Defense College Foundation paper (Spagnuolo), NOT formal funders. **Palantir (Karp), Anduril (Luckey), BlackRock (Fink), DeepMind/YouTube, Cato/Koch** = member-employers via named attendees only. **NATO Defense College Foundation is an OBSERVER** (its analyst published *on* Dialog) — routinely mischaracterized as an affiliate. Thiel Capital/Fellowship/portfolio firms = real corporate web but only *inferred* re: Dialog. Venue partners: Ritz-Carlton (Bacara + Dove Mountain), San Clemente Palace, Sundance, MHL/Powerscourt.

### Dimension 3 — Governance & dossiers — _COMPLETE (#192)_ → `research/dialog/dimension3-governance.json`
Two products: **membership (1,000+)** + **retreats (2,500+ lifetime)**. **AI-generated dossier on every member/prospect**, stored in a commercial **Airtable** (the leak vector). Dossier fields: **AUM** (e.g. "$30 billion in AUM"), a **1–4 value-add score** (averaged across staff), **moderation-trust**, **culture-fit**, **staff-adjusted political leanings**, plus heavy PII (home address, private phone, DOB, emergency contacts, allergies, Instagram counts). An internal algorithm asks whether "the average person" would recognize someone (benchmarked vs a Fortune 500 firm / "top celebrity"). **Specific AI vendor/engineer NOT named.** Off-the-record but **no NDAs** — confidentiality is cultural/reputational, not contractual. Removal for "Value Add Too Low" / "Poor Culture Fit" / slipped grade. Internal format sub-brand: **"Soapbox" sessions**. Adjacent (not sub-units): Hereticon, Teneo, Thiel Fellows, Per Aspera.

### Dimension 4 — Funding & structure — _COMPLETE (#193)_ → `research/dialog/dimension4-funding.json`
**Ownership chain: Dialog → Stonebrick, LLC → Auren Hoffman.** Fees graded: full price >$10k for lower grades ~70% of the time; concrete example = **2022 CA invitation showed $16,846** reduced ~70% by a discount code. High-grade VIPs often comped (e.g. ex-MEP Marietje Schaake paid nothing). Reporting states **"Dialog does not have a money-making business model"** → implies subsidy, but **no specific outside funder is documented**; Thiel Capital/Founders Fund/a16z **NOT** documented as funders (unverified). Thiel Foundation tied to the VA campus only via analyst commentary (no documented grant). **Campus cost/financing/acreage/buyer entity = documentation gap**; status conflicts (Axios/Semafor "purchased" vs implicator.ai/Byline "in negotiation").

### Dimension 5 — Territory — _COMPLETE (#194)_ → `research/dialog/dimension5-territory.json`
One retreat/year at luxury, secluded, high-security venues; bi-continental (US: CA/AZ/UT; Europe: Venice/Ireland; + a Turkey Bitcoin event). **All venues to date RENTED** — reporting calls Dialog "nomadic," which the VA campus is meant to end. Well-documented: Ritz-Carlton Bacara (Dec 1–4 2022, per leaked $16,846 Gelman invitation), Ritz-Carlton Dove Mountain, San Clemente Palace (Venice, incl. 2025 summit). **Powerscourt (Ireland), booked Aug 12–16 2026, CANCELLED July 2026** after the leak + a Palestine-solidarity campaign. **DC-area campus = reported intent (single Axios tipster, Aug 2025)**; Fairfax/Loudoun speculated; **CIA-Langley/Pentagon proximity is analyst framing (Spagnuolo), not confirmed**.

### Dimension 6 — Group mentality — _COMPLETE (#195)_ → `research/dialog/dimension6-mentality.json`
A **curated elite-cohesion machine** (doctrine graded at org level, not imputed to members — composition guard held). Load-bearing norm = **manufactured psychological safety** (off-record, "nonobvious" comments) — framed as candor-enabling; same design keeps elite deliberation outside public accountability (no gov emails, outside records laws) → intent read from what organizers say AND omit. Defining tension: **"avoid status signalling" sitting atop a quantified A/B/C + AI-dossier apparatus** — read as *function* (status settled administratively so it needn't be performed), not mere hypocrisy. Throughline = AI + longevity + near-future, but documented **mood is pessimistic-futurist** (labor displacement, "AI winter," data-center attacks, religious revival) → anticipatory elite positioning, not utopian ideology. **Intimacy as cohesion tech** (confessional sessions + dating.dialog.org matchmaking) distinguishes it from Bilderberg's deal/policy register. Referral-gated in/out-group → high homophily + the fragility the leak exposed. Caveat: nearly all specifics from a single (WIRED-verified) leak corpus; Dialog hasn't confirmed the documents.

---

## Synthesis status (EPIC #189)

All 6 dimensions COMPLETE (2026-07-18). Next: build `research/spec-dialog-org.json` graph block (nodes: Dialog, Stonebrick LLC, Thiel/Hoffman/Grinberg, Thiel Foundation, member-employer orgs already in graph — Palantir/Founders Fund/a16z/OpenAI/Anduril/PsiQuantum/BlackRock/DeepMind; edges INTO a Dialog sink-hub to stay cycle-safe per bubblemap-graph-integrity), add person dossiers to `data/persons.json` for any minted person-nodes (persons-list-vs-bubblemap rule), write `research/*.md` writeup, then hold the SCC/audit/cross_review gate. **Presumption of innocence throughout — attendance ≠ wrongdoing; the Epstein/2014 claim is RETRACTED and must not be repeated.**
