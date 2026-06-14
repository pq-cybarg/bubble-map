# Defense leg — primes + defense-tech × the rare-earth chokepoint

*Built from `research/defense-rare-earth.json` (web-verified: CSIS, Modern War Institute/West Point, GAO/CRS-cited reporting, DoD FY26 budget, Arnold/Dura Magnetics). Per-unit REE figures are widely-cited GAO/CRS-lineage estimates — treat as order-of-magnitude. Models: `models/graph/defense_web.py`, `models/z3/defense_chokepoint.py`.*

> **Thesis.** US weapons systems are **materially dependent on rare-earth magnets China controls** — and China has moved from owning the supply to **explicitly denying it to foreign militaries.** This is the hard, near-term national-security chokepoint behind the defense-contractor leg.

## 1. The per-system dependency (order-of-magnitude)
| System | REE kg/unit | Samarium kg | Note |
|---|---|---|---|
| **F-35** | ~418 (~900 lb) | 22.6 | SmCo magnets for high-temp (missile nose cones); Lockheed = largest US samarium user. Block-4 upgrade slipped 2026→2031, +$6B. |
| **Virginia-class sub** | ~4,200 (~9,200 lb) | 50 | |
| **Arleigh Burke destroyer** | ~2,360 | 30 | |
| **Tomahawk / JDAM / Predator / radar** | ~5 | ~1 | small per-unit, **huge in volume** |

## 2. China's control — and the weaponization
- **Mining ~70%, processing ~90%, heavy-REE separation ~99%, samarium ~100%.**
- **Apr 2025:** export licenses required on 7 heavy REEs (Sm, Gd, Tb, Dy, Lu, Sc, Y) + magnets.
- **Dec 1 2025:** entities affiliated with **foreign militaries (incl. the US) largely DENIED** licenses; military-use requests auto-rejected.
- **Nov 7 2025 Trump–Xi deal** paused the *broad* controls for a year but **retained the military-end-use denials** — the chokepoint stays shut for defense.

This is exactly the condition the Z3 `defense_chokepoint` model encodes: **REE independence is UNSAT until ~2028** (the earliest the domestic Mountain Pass heavy-REE + magnet capacity and allied separation can plausibly close the gap).

## 3. The domestic/allied response
The same state-circular financing as `macro-critical-minerals` (MP Materials: DoD as largest shareholder + $110/kg NdPr floor + 10-yr offtake), plus magnet-makers (Arnold, Dura), and the DoD FY26 budget lines — a **quasi-nationalized** supply build racing the ~2028 horizon. Cross-ref `macro-critical-minerals`, `geopolitics-defense-industrial-base`, `geopolitics-contested-resource-states`.

## 4. Limits
Per-unit REE figures are **estimates** (GAO/CRS lineage) — directional, not precise. The pace of domestic/allied capacity is the swing variable; the Z3 model treats ~2028 as the binding date.

*Sources: [MWI West Point — China's REE weaponization](https://mwi.westpoint.edu/minerals-magnets-and-military-capability-chinas-rare-earth-weaponization-should-be-a-wake-up-call/); [CSIS — consequences of China's export restrictions](https://www.csis.org/analysis/consequences-chinas-new-rare-earths-export-restrictions); Modern Diplomacy / Karve International on per-system dependency.*
