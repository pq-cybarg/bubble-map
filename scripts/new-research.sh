#!/usr/bin/env bash
# Re-review ALL prior findings after adding/editing any research/*.json (project standing rule).
set -e; cd "$(dirname "$0")/.."
python3 models/graph/build_graph.py >/dev/null
python3 models/audit.py
echo "----"
python3 models/cross_review.py
python3 models/graph/build_dashboard.py >/dev/null
python3 models/graph/build_charts.py >/dev/null
echo "==> Re-review done. Read report/AUDIT.md + report/CROSS-REVIEW.md and reconcile flags before committing."
