# ShinyHunters + the Florida DMV (FLHSMV/DAVID) extortion claim

## The actor (documented)
**ShinyHunters** is a data-theft + extortion collective active since ~2020, tied to operating successive **BreachForums** incarnations. Its major campaigns:
- **2024 Snowflake wave** - stolen/infostealer credentials against ~165 Snowflake customer tenants (no Snowflake product flaw), hitting Ticketmaster, AT&T, Santander and others; one of the largest data-theft waves on record (some activity co-attributed to UNC5537).
- **2025 Salesforce/Salesloft "Drift" wave** - voice-phishing + abused OAuth tokens to exfiltrate many companies' Salesforce data, then extort them.
- Overlaps the loose English-speaking **"The Com"** milieu (which also produced **Scattered Spider** and **LAPSUS$**); 2025 saw joint "Scattered LAPSUS$ Hunters" branding. Cross-crew attribution is fluid - graded.

The throughline: a pivot from encryption-ransomware to **pure data-theft extortion** (exfiltrate -> name-and-shame -> pay-or-leak).

## The Florida DMV claim (reported / UNVERIFIED, 2026-09-07)
Per breachnews.com (2026-09-07), ShinyHunters posted an **extortion claim** to have breached **FLHSMV's DAVID** (Driver And Vehicle Information Database): driver's-license data, license **photo + signature**, address and vehicle records, with a **2026-09-11** contact deadline.

Honest status:
- **FLHSMV had not confirmed any breach** at publication.
- The only public "proof" was a **single DAVID screenshot** (a Jeffrey Epstein record) whose authenticity/provenance is **contested** - it could derive from previously disclosed investigative material rather than fresh DAVID access.
- A possible tie to a larger **"Nexus" 153M+ license-record dataset** was floated but **unconfirmed**.
- Record count and breach vector were **not disclosed**.

Treat as a **live, unverified claim**, not an established breach.

## Why a DMV compromise matters (the surveillance pipeline)
DAVID is a single-point repository of resident identity data. The map already documents the downstream flows that a DMV breach short-circuits:
- **DMV -> ICE / law enforcement** - DMV records + license photos accessed by immigration enforcement, including facial-recognition searches (documented nationally; FL specifics graded).
- **DMV -> data brokers** - state DMVs have sold/shared motor-vehicle records under DPPA "permissible use" carve-outs, feeding the commercial identity-data economy (national pattern; FL specifics graded).
- **DMV -> facial recognition** - license-photo databases are among the largest de-facto biometric databases of ordinary residents, so a DMV compromise is a **biometric**-exposure event, not just PII.

## Honest limits
The actor's prior campaigns and the existence of the extortion post are documented; the Florida breach **itself is unverified**; the downstream DMV-data pipelines are documented national patterns with Florida-specific details graded. No coordinated-plan claim is made.

*Sources: ShinyHunters/BreachForums/Snowflake/Salesforce incident reporting (Mandiant, Google TI, press); breachnews.com 2026-09-07; DPPA + DMV-data-sale reporting (Vice/404 Media); Georgetown Law facial-recognition research. Cross-refs: The_Com, Scattered_Spider, Data_Brokers, ICE, Facial_Recognition, LexisNexis, Private_Surveillance.*
