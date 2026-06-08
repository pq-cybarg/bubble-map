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
- models: 25 (z3 .py: 7) + TLA + Alloy
- research: 38 json / 28 md
- data outputs: 12
- reports: 7

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