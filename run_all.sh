#!/usr/bin/env bash
# run_all.sh - reproduce every analysis and proof in this repo, end to end.
# Requires: python3 (+z3 bindings), java (for TLA+/Alloy). All jars are vendored after first run.
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"
JAVA="${JAVA:-$(command -v java || echo /Applications/Android\ Studio.app/Contents/jbr/Contents/Home/bin/java)}"
hr(){ printf '\n\033[1m%s\033[0m\n%s\n' "$1" "============================================================"; }

hr "[1/8] Build canonical funding graph + structural SCC analysis"
python3 models/graph/build_graph.py

hr "[1a2] Consistency re-review (audit + cross-review)"
python3 models/audit.py | tail -3
python3 models/cross_review.py | tail -3

hr "[1b] Temporal META-graph (1998->2026) + betweenness 'weavers'"
python3 models/graph/temporal_web.py | sed -n '1,40p'

hr "[2/8] Z3 - quantitative circularity proofs (T1-T5)"
python3 models/z3/circularity_smt.py

hr "[2b] Z3 - reflexive mark-to-market proofs (M1-M4: self-referential AI 'profit')"
python3 models/z3/reflexive_marks.py | grep -E "M[0-9]|Z3 result|WITNESS|UNSAT:|ILLUSTRATION" | head -24

hr "[2c] Z3 - self-marked-value theorem (U1-U4: bank HTM / AI marks / private credit / insurance = same defect)"
python3 models/z3/self_marked_value.py | grep -E "U[0-9]|Z3 result|WITNESS|UNSAT:|CONCLUSION" | head -22

hr "[3/8] Z3 - small-bank coordination game (C1-C4)"
python3 models/z3/coordination_game.py

hr "[4/8] Z3 - Fed single-instrument policy trap (F1-F3 + Chebyshev best rate)"
python3 models/z3/fed_policy_trap.py

hr "[5/8] FDIC per-bank hierarchical exposure (live API pull)"
python3 models/graph/bank_exposure.py

hr "[6/8] Hidden vs surfaced leverage + regional divergence"
python3 models/graph/regional_leverage.py

hr "[6b] Flow of funds + housing/CRE re-priced in GOLD & SILVER (1998-2026)"
python3 models/graph/gold_silver_reprice.py

hr "[6c] Defense leg: primes/Anduril/Palantir x rare-earth chokepoint"
python3 models/graph/defense_web.py | tail -20
hr "[6d] Z3: defense rare-earth chokepoint (independence UNSAT until ~2028)"
python3 models/z3/defense_chokepoint.py | tail -16
hr "[6e] Energy leg: power bottleneck + nuclear/SMR web + Russia HALEU chokepoint"
python3 models/graph/energy_web.py | tail -14
hr "[6f] Z3: power adequacy (UNSAT) + HALEU chokepoint (UNSAT)"
python3 models/z3/power_adequacy.py | tail -14

hr "[7/8] TLA+ - bubble unwind cascade (TLC model-check)"
[ -f models/tla/tla2tools.jar ] || curl -sL -o models/tla/tla2tools.jar https://github.com/tlaplus/tlaplus/releases/latest/download/tla2tools.jar 2>/dev/null
if [ -f models/tla/tla2tools.jar ]; then
  ( cd models/tla
    echo "--- Inv_NoCoreCollapse (expect VIOLATED = the cascade trace) ---"
    "$JAVA" -cp tla2tools.jar tlc2.TLC -config cascade.cfg BubbleCascade.tla 2>&1 | grep -E 'Error: Invariant|State [0-9]|status =|tap =|states generated' | head -40
    echo "--- Inv_SpaceXSafe (expect HOLDS) ---"
    "$JAVA" -cp tla2tools.jar tlc2.TLC -config spacex.cfg BubbleCascade.tla 2>&1 | grep -E 'No error|Error: Invariant'
    echo "--- MarkUnwind Inv_MarksHold (expect VIOLATED = the paper-marks writedown trace) ---"
    "$JAVA" -cp tla2tools.jar tlc2.TLC -config markunwind.cfg MarkUnwind.tla 2>&1 | grep -E 'Error: Invariant|State [0-9]|round =|mark =|lab =|states generated' | head -28 )
else echo "tla2tools.jar missing - fetch from https://github.com/tlaplus/tlaplus/releases/latest/download/tla2tools.jar"; fi

hr "[8/8] Alloy - relational structure checks"
[ -f models/alloy/alloy.jar ] || curl -sL -o models/alloy/alloy.jar https://github.com/AlloyTools/org.alloytools.alloy/releases/download/v6.2.0/org.alloytools.alloy.dist.jar 2>/dev/null
if [ -f models/alloy/alloy.jar ]; then
  ( cd models/alloy
    [ -f RunAlloy.class ] || "${JAVA%java}javac" -cp alloy.jar RunAlloy.java
    "$JAVA" -cp "alloy.jar:." RunAlloy BubbleStructure.als 2>&1 | grep -E '===|assertion|instance' )
else echo "alloy.jar missing - fetch org.alloytools.alloy.dist.jar v6.2.0"; fi

hr "[6g] Allied-vs-adversary REE min-cut (bottleneck = midstream)"
python3 models/graph/allied_mincut.py | tail -12

hr "[6g3] Blockchain leg: policy-capture loop + stablecoin deficit rail"
python3 models/graph/blockchain_web.py | tail -16

hr "[6g2] Equities re-priced in gold (real value vs debasement)"
python3 models/graph/equity_in_gold.py | tail -12

hr "[6g4] Altcoin lens (real-utility vs narrative-beta)"
python3 models/graph/altcoin_lens.py | tail -10

hr "[6h] Scenario engine (BASE/BULL/BEAR formal verdicts)"
python3 models/z3/scenario.py | sed -n "1,12p"

hr "[6i] System-of-systems contagion matrix (cross-leg cascade)"
python3 models/graph/contagion_matrix.py | tail -28

hr "[6j2] Age-verification FUTILITY theorem (why even ZK fails)"
python3 models/z3/ageverif_futility.py | tail -8

hr "[6k] ZK age-proof self-test (privacy-preserving age verification)"
python3 zkage/zk_age_proof.py | tail -20

hr "[7b] Build dashboard + globe"
python3 models/graph/build_dashboard.py
python3 models/graph/build_globe.py
python3 models/graph/fetch_fred.py || true   # refresh monthly FRED cache (tolerates offline; build_charts uses cache)
python3 models/graph/fetch_yahoo.py || true  # ETF distribution-yield proxies (per-state muni, corporate by maturity)
python3 models/graph/fetch_tape.py || true   # FINRA TRACE corporate aggregates (needs FINRA_API_CLIENT/SECRET env; tolerates absence)
python3 models/graph/build_charts.py

hr "DONE"
echo "Report:   report/UNMASKING.md"
echo "Data:     data/graph.json, data/edges.csv, data/bank_exposure.json"
echo "Sources:  research/*.json (every figure carries its source URLs)"
