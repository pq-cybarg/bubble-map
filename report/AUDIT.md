# Consistency & Coverage Audit

Canonical numbers (from data/*.json — the source of truth):

- `core_scc_robust` = **11**
- `core_scc_all` = **12**
- `cycles` = **16**
- `nvda_headline_pct` = **57**
- `nvda_funded_pct` = **11**
- `home_gold_idx_2026` = **19**
- `sp500_gold_chg` = **-69**
- `nvda_gold_chg` = **1985**
- `base_gap` = **1090**

## Inventory
- models: 38 (z3 .py: 10) + TLA + Alloy
- research: 89 json / 93 md
- data outputs: 21
- reports: 9

## JSON validity
- ALL VALID

## Cross-document consistency flags
- none — consistent

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