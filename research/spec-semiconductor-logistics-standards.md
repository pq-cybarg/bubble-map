# The physical substrate — semiconductor supply chain, global logistics/shipping, and the standards-setting bodies

*Built 2026-06-21 from `research/spec-semiconductor-logistics-standards.json`. The physical layer under the AI bubble. Companion to `macro-pqc-chips`, `fin-google-amazon-anthropic-meta` (the chip cohort), `macro-critical-minerals` (upstream materials), `spec-cross-system-contagion`, `spec-quantum-computing-competitive-landscape` (the GlobalFoundries fab chokepoint).*

> **Frame.** The AI bubble rests on a physical substrate that **narrows to single points of failure**: (1) a semiconductor chain with **one** EUV maker (ASML), **one** optics maker inside it (ZEISS), **one** advanced foundry (TSMC), **one** packaging bottleneck (CoWoS); (2) a logistics network through a handful of **maritime chokepoints**; (3) the **standards bodies** (ISO/IEC/IEEE/IMDRF/...) that write the rules every product must meet.
>
> **Lenses.** Chokepoint concentration, dual-use, **Sun Tzu** (control the terrain / deny foreknowledge), the **composition-fallacy guard** (an industry *acting* ≠ an industry with one *mind*), and grading. Concentration here is **fact**; "systemic + geopolitical leverage" is **graded interpretation**; no intent imputed.

## 1. The lithography chokepoint (the narrowest point in the economy)

**ASML** (Netherlands) is the **sole** maker of EUV lithography — no advanced (<7nm) logic exists without it. Inside ASML is a **deeper** chokepoint: **Carl Zeiss SMT** exclusively makes the EUV optics/mirrors (picometer flatness, nanometer multilayer coatings — objects no one else can build); **ASML owns 24.9% / €1B** of Zeiss SMT and calls it its most important strategic partner. **Cymer** (ASML subsidiary) makes the EUV light source. **High-NA EUV** (NA>0.5) extends scaling. EUV is **export-controlled** — ASML **cannot sell EUV to China** (the single most consequential tech-sanction lever). Nikon/Canon make only **DUV** (Canon pushing nanoimprint/NIL). *Fact.*

## 2. The foundry & packaging chokepoint

**TSMC** (Taiwan) fabricates **~90%** of the most-advanced logic — the **Taiwan-Strait** concentration is the defining geopolitical risk of the AI era. But the **acute 2025-26 bottleneck is not wafers (2nm) — it's advanced packaging**: TSMC's **CoWoS** (CoWoS-S/-L) is **fully booked, 52-78 week lead times**; **Nvidia holds >70% of CoWoS-L**, with Google/Apple/Meta/Anthropic/OpenAI/ByteDance fighting for the rest. Upstream: the **WFE oligopoly** (Applied Materials, Lam Research, Tokyo Electron, KLA), the **materials** majors (Shin-Etsu, SUMCO wafers; JSR, Tokyo Ohka photoresist), **HBM** memory (SK Hynix, Samsung, Micron; JEDEC-standardized), and the **EDA/IP** chokepoint (Synopsys, Cadence, Siemens EDA, Arm — also export-controlled to China). **SMIC** is China's sanctioned foundry (7nm via DUV). *Fact.*

## 3. The logistics layer

Physical goods move through a concentrated maritime network: the **ocean-carrier oligopoly** (Maersk, MSC, CMA CGM, Hapag-Lloyd, COSCO, ONE) and **3PL majors** (DHL, Kuehne+Nagel, DSV, FedEx, UPS, C.H. Robinson) funnel through a few **chokepoints** — **Suez** (Red Sea/Houthi reroutes), **Panama** (drought), **Malacca**, **Hormuz**, and the **Taiwan Strait**. A disruption at any one cascades into cost/lead-time/inventory shocks — the just-in-time fragility the 2021-22 shock exposed. *Firms/chokepoints fact; fragility read interpretation.*

## 4. The standards layer (the least-visible power)

Standards bodies write the rules every product must meet, and **whoever writes the standard shapes the market** (China's "**Standards 2035**" targets exactly this terrain). **ISO + IEC** run **ISO/IEC JTC 1**, whose subcommittees include **SC 42** (Artificial Intelligence — ~45 standards, the AI-governance battleground) and **SC 27** (IT security / the PQC channel). Adjacent: **IEEE, ITU, ETSI, 3GPP** (telecom), **SEMI, JEDEC** (semiconductor/memory), **ANSI, BIPM, Codex Alimentarius**. Medical devices: the **GHTF** → **IMDRF** lineage harmonizing **ISO 13485** (QMS) + **ISO 14971** (risk). **NIST** feeds international AI + cryptography standards. Standards are **chokepoints of legitimacy** — controlling them is controlling the terrain (Sun Tzu) without firing a shot. *Bodies/scopes fact; soft-power framing interpretation.*

## 5. The composition caveat

An industry coordinating around a standard, or concentrating at a chokepoint, is institutional **action** — it does **not** imply a unitary industry **mind** or conspiracy. The concentration emerges from economies of scale, decades of unrepeatable co-development (ASML/Zeiss), and network effects — **structural causes, not necessarily designed ones**. The finding is **fragility + leverage, not intent**.

*Sources: [ASML — €1B / 24.9% Zeiss SMT EUV partnership](https://www.asml.com/en/news/press-releases/2016/zeiss-and-asml-strengthen-partnership-for-next-generation-of-euv-lithography); [Wikipedia — Carl Zeiss SMT](https://en.wikipedia.org/wiki/Carl_Zeiss_SMT); [DigiTimes — CoWoS the AI bottleneck](https://www.digitimes.com/news/a20260410VL204/packaging-capacity-tsmc-nvidia-demand.html); [Silicon Analysts — TSMC allocation 2026](https://siliconanalysts.com/analysis/foundry-allocation-status-q1-2026); [ISO/IEC JTC 1/SC 42 — AI](https://www.iso.org/committee/6794475.html); [IMDRF](https://www.imdrf.org/).*
