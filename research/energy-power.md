# Energy / power leg — the AI + defense power bottleneck, nuclear/SMR PPAs, the turbine wall, and the Russia-enrichment chokepoint

*Built from `research/energy-power.json` (web-verified: IEA Energy & AI; US DOE; PJM auction releases; Utility Dive/GE Vernova; Centrus 8-Ks; DOE/NRC on the Russian-uranium ban). Models: `models/graph/energy_web.py`, `models/z3/power_adequacy.py`. Power demand/grid charted elsewhere.*

> **Thesis.** Power is a **binding physical constraint** on the AI buildout, not a footnote. New firm supply lags AI demand every year through 2028; the hyperscalers are racing into nuclear/SMR PPAs; gas turbines have a multi-year backlog; and the fuel for advanced reactors runs through a **Russia-controlled enrichment chokepoint.**

## 1. Demand — AI is ~half of US load growth
- Data centers: **~4.4% of US electricity (2023) → 6.7–12% (2028)**; **~half of all US load growth to 2030**; global DC **~945 TWh by 2030**.
- **PJM capacity auction hit its cap three auctions running** ($329 → **$333.44/MW-day**); ~$9.3B of the increase is data-center-driven — the grid is already repricing scarcity.

## 2. The hyperscaler nuclear/SMR scramble
- **Microsoft** — 835 MW, ~$16B 20-yr PPA (~2028, Constellation/Three Mile Island restart).
- **Amazon** — 1,920 MW through 2042 + SMR exploration.
- **Google** — 500 MW, first corporate SMR-fleet deal (50 MW by 2030).
- **Meta** — nuclear procurement (Datacenter Frontier).

These are the AI core reaching for **firm, carbon-free baseload** — but most SMR capacity is **late-decade**, behind the demand curve.

## 3. The supply walls
- **Gas turbines:** GE Vernova **~80 GW backlog into 2029**; heavy-duty lead time ~3 yr, CCGT 5–7 yr; ~80 GW of orders vs ~30 GW/yr capacity. Crusoe ordered 19 turbines (behind-the-meter gas). The turbine wall is a hard near-term ceiling.
- **HALEU / enrichment (the Russia chokepoint):** Russia is **~44% of global enrichment**, ~35% of US imports, 27% of US enriched-uranium demand (2023); **HALEU for SMRs was ~100% Russia.** The *Prohibiting Russian Uranium Imports Act* (May 2024, eff. Aug 11 2024, waivers to 2027) banned imports — and **Russia retaliated with export curbs.** Domestic **Centrus produces ~900 kg/yr HALEU** (Piketon, OH) — far short of fleet need. **Midstream (conversion + enrichment) is the real chokepoint**, not mining.

## 4. The formal results
- **Z3 `power_adequacy` P1 — UNSAT:** new firm power supply < AI demand **every year through 2028** (2026: 18 vs 25 GW; 2028: 34 vs 80 GW — the gap *widens*). Earliest balanced year is **>2028**.
- **Z3 P2 — UNSAT:** domestic HALEU is short of SMR-fleet need through 2029 → the US stays **dependent on Russia-controlled enrichment** — the energy analogue of the rare-earth chokepoint.

## 5. Why on-thesis
Power is one of the **three physical chokepoints** (capital, rare earths, power+HALEU), and two of the three are adversary-controlled. Cross-ref `macro-ai-power-grid-bottleneck`, `macro-ai-datacenter-water-siting`, `geopolitics-russia-energy-arctic`, `defense-rare-earth`.

*Sources: [DOE — data-center electricity demand](https://www.energy.gov/oe/clean-energy-resources-meet-data-center-electricity-demand); [Utility Dive — PJM auction](https://www.utilitydive.com/news/pjm-interconnection-capacity-auction-data-center/808264/); [Utility Dive — Russian uranium ban / HALEU](https://www.utilitydive.com/news/congress-passes-russian-uranium-import-ban-haleu-nuclear-fuel-advanced-reactors/715256/); [Centrus — 900 kg HALEU milestone](https://www.centrusenergy.com/news/centrus-achieves-key-production-milestone-with-delivery-of-900-kilograms-of-haleu-to-the-department-of-energy/).*
