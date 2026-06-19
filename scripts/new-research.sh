#!/usr/bin/env bash
# Re-review ALL prior findings after adding/editing any research/*.json (project standing rule).
set -e; cd "$(dirname "$0")/.."
python3 models/graph/build_graph.py >/dev/null
python3 models/audit.py
echo "----"
python3 models/cross_review.py
python3 models/graph/build_dashboard.py >/dev/null
python3 models/graph/fetch_fred.py >/dev/null 2>&1 || true
python3 models/graph/fetch_yahoo.py >/dev/null 2>&1 || true
python3 models/graph/fetch_tape.py >/dev/null 2>&1 || true   # FINRA TRACE corporate aggregates (needs FINRA_API_* env; tolerates absence)
python3 models/graph/fetch_fec.py >/dev/null 2>&1 || true    # FEC campaign-finance summaries (needs FEC_API_KEY env; tolerates absence)
python3 models/graph/fetch_ofac.py >/dev/null 2>&1 || true   # OFAC SDN crypto addresses (env-free; tolerates absence)
if [ ! -f data/fdic_qbp.json ] || [ -z "$(find data/fdic_qbp.json -mtime -80 2>/dev/null)" ]; then
  python3 models/graph/fetch_fdic_qbp.py >/dev/null 2>&1 || true  # FDIC QBP multi-year aggregates (refresh only if cache missing/>80d; env-free, tolerant)
fi
python3 models/graph/cross_section.py >/dev/null 2>&1 || true # cross-sectional analysis (dispersion / RV z / PC1 common factor)
python3 models/graph/build_charts.py >/dev/null
python3 models/graph/build_persons.py >/dev/null   # Persons of Interest dossier tab
python3 models/graph/build_bubblemap.py >/dev/null # interactive funding-graph bubble map
python3 models/graph/build_theme_index.py          # theme->blocks index for the flagship/atlas zoom
echo "==> Re-review done. Read report/AUDIT.md + report/CROSS-REVIEW.md and reconcile flags before committing."
