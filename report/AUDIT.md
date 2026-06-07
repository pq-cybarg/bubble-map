# Consistency & Coverage Audit

Canonical numbers (from data/*.json — the source of truth):

- `core_scc_robust` = **11**
- `core_scc_all` = **12**
- `cycles` = **15**
- `nvda_headline_pct` = **56**
- `nvda_funded_pct` = **10**
- `home_gold_idx_2026` = **19**
- `sp500_gold_chg` = **-69**
- `nvda_gold_chg` = **1985**
- `base_gap` = **1090**

## Inventory
- models: 23 (z3 .py: 6) + TLA + Alloy
- research: 29 json / 19 md
- data outputs: 12
- reports: 6

## JSON validity
- ALL VALID

## Cross-document consistency flags
- ⚠ -81% home gold: NOT found in report/UNMASKING.md
- ⚠ +1985 nvda gold: NOT found in docs/index.html
- ⚠ -69 sp500 gold: NOT found in docs/index.html

## Leg coverage (research present?)
- AI core: ✓
- banking: ✓
- CRE/credit: ✓
- commodities: ✓
- defense: ✓
- energy: ✓
- blockchain: ✓
- altcoins: ✓
- influence: ✓
- temporal: ✓
- gold-lens: ✓
- speculation: ✓

## Research files lacking any 'source' field
- none