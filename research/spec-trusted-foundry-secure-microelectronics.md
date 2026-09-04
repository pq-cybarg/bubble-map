# Trusted foundry & secure microelectronics: who is allowed to fabricate the chips

Who is permitted to make the silicon that goes into weapons, cryptographic roots-of-trust, and critical infrastructure - and how states force that capacity **onshore** or into **"trusted"** hands. This block exists partly to fix a graph gap: `Trusted_Foundry` was a near-isolated (degree-1) node despite being a major topic. It now wires into the semiconductor, defense-prime, CHIPS-Act, foundry (TSMC/Intel/GF/Samsung), PQC, and geopolitics threads.

## The US DoD regime
- **DMEA / TAPO.** The Defense Microelectronics Activity's Trusted Access Program Office has run the **Trusted Foundry Program since 2003**; the mission **moved from the NSA to DMEA in 2015** - the same NSA-to-defense-microelectronics lineage that recurs across the surveillance threads. DMEA accredits the **whole chain**: design, mask, foundry, packaging/assembly, test, broker. Its point is **guaranteed, low-volume, trusted** access for defense - both classified and unclassified.
- **Accredited suppliers** include **GlobalFoundries** (Malta NY / ex-IBM East Fishkill), **Intel Foundry**, **IBM** (Trusted Supplier accreditation; secured manufacturing flows + embedded security under Trusted Foundry Access II, 2022-23), **SkyWater** (US-owned, Minnesota; trailing-edge/specialty), and **BAE Systems'** Nashua NH rad-hard center.
- **RAMP-C.** Rapid Assured Microelectronics Prototypes - Commercial (launched Sep-2021, **completed** by Intel) built the IP/EDA ecosystem on **Intel 18A** (RibbonFET + PowerVia), taped out and tested defense prototypes, and onboarded DIB customers (Trusted Semiconductor Solutions, Reliable MicroSystems). Awarded via the **S2MARTS** Other Transaction Authority under OUSD R&E's Trusted & Assured Microelectronics office. It targets domestic **leading-edge** - directly answering the Taiwan dependency.
- **Secure Enclave** funds a dedicated walled leading-edge Intel capability for DoD; **SHIP** covers advanced 2.5D/3D **packaging** + chiplets (assurance is not just the fab). The **Trusted Foundry Access III** solicitation (DMEA, 2026, ~$576M ceiling) generalizes the "trusted enclave inside a commercial fab" model.
- **DARPA** feeds trust/assurance research (ERI; provenance) in; **defense primes** (Lockheed, RTX) are the demand side that justifies the whole regime.

## The EU
- **EU Chips Act + IPCEI ME/CT** (EUR 21.8B; EUR 13.7B state aid) span the value chain; ~**EUR 69B catalysed** by Oct-2025. **Chips Act 2.0** (adopted **3 Jun 2026**) pivots to **supply-chain resilience** (a B2B semiconductor supply platform), and a **third IPCEI** is being designed.
- Europe's real leverage is **equipment**: **ASML's** EUV monopoly (Draghi urged a fast-track lithography IPCEI). **ESMC Dresden** (TSMC JV with Bosch/Infineon/NXP) onshores a leading foundry, mirroring US CHIPS.

## The UK
- **National Semiconductor Strategy** (GBP 1B / 10yr, up to GBP 200M in 2023-25) is deliberately **niche** - design, compound semiconductors, R&D - **not** leading-edge fabrication. Small vs the US/EU.
- **NSI Act 2021.** The marquee intervention: the UK ordered divestment of **86% of Newport Wafer Fab** (Nov-2022) - held by **Nexperia** (Dutch-incorporated, ultimately China-owned via **Wingtech**) after two prior clearances. Nexperia said it was "shocked" and **disputed** the national-security basis (both accounts noted). The fab was sold to US-based **Vishay** for ~$177M (Mar-2024). The pattern extends: the UK ordered a Chinese consortium to sell **80.2% of chipmaker FTDI** by Feb-2027 (legal challenges failed).

## Allied layer
- **Rapidus** (METI-backed, Hokkaido) targets **2nm using IBM technology** - Japan's onshoring/allied leading-edge bet (yield/timeline unproven). The **IBM microelectronics lineage** (behind GF, DMEA trusted services, and now Rapidus) threads through the whole allied stack.
- **Pax Silica** - reports that the EU and member states are preparing to join a **US-led** initiative aligning AI-chip supply chains among trusted partners. Resilience via trusted partnership, not autarky.

## Honest limits
"Trusted" is a **supply-chain-integrity** designation, not a claim that a fab is technically superior. Accreditation and onshoring **reduce but do not eliminate** risk: leading-edge remains concentrated at **TSMC/Taiwan** (the chokepoint the whole regime hedges), and most domestic trusted capacity is **trailing-edge / low-volume**. NSI-Act divestments are government **actions** whose stated basis is national security; companies dispute it - motive is read from what the orders say, not imputed.

*Sources: DMEA.osd.mil (Trusted IC / TAPO; NSA->DMEA 2015); Intel + IBM newsrooms (RAMP-C completion, Intel 18A, Secure Enclave; DMEA Trusted Supplier 2022-23); Trusted Foundry Access III solicitation (DMEA 2026); EU Chips Act 2.0 (EUR-Lex 52026PC0504, 3-Jun-2026), IPCEI ME/CT, SEMI Europe, Draghi report; UK National Semiconductor Strategy (2023); UK NSI Act orders (Newport 2022; FTDI 2026, Caixin); Vishay / Nexperia releases; Rapidus / METI / IBM 2nm. Cross-refs: spec-globalfoundries, spec-semiconductor-logistics-standards, geopolitics-taiwan-silicon-shield, geopolitics-chip-chokepoint-war, spec-defense-primes-pqc, macro-pqc-chips, spec-defense-industrial-base.*
