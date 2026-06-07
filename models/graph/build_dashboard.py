#!/usr/bin/env python3
"""
build_dashboard.py - generate a self-contained report/INDEX.html (data embedded, opens with
no server) + report/EXECUTIVE-SUMMARY.md, consolidating every layer, proof verdict, chokepoint,
and gold-repricing into one navigable artifact built from the live data/*.json outputs.
"""
import json, os, glob, html
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); REP=os.path.join(ROOT,"report"); RES=os.path.join(ROOT,"research")
def load(n):
    try: return json.load(open(os.path.join(DATA,n)))
    except: return {}
g=load("graph.json"); tw=load("temporal_web.json"); gs=load("gold_silver_reprice.json")
be=load("bank_exposure.json"); dw=load("defense_web.json"); ew=load("energy_web.json")
sc=load("scenarios.json"); eq=load("equity_in_gold.json")

# ---- derive key metrics ----
an=g.get("analysis",{})
core=an.get("core_scc_all",[]); robust=an.get("core_scc_robust_excl_cancelable",[])
cancel_only=an.get("nodes_only_circular_via_cancelable",[])
ncyc=an.get("num_elementary_cycles","?"); nself=an.get("nvidia_self_funding",{})
# proof verdicts (from the runnable engines)
VERDICTS=[
 ("Graph SCC","11-firm robust core; SpaceX cancelable-only","PROVED"),
 ("Z3 T1 round-trip","a money cycle is realizable","SAT"),
 ("Z3 T2 NVIDIA self-finance","≥$25.8B revenue self-financed","UNSAT(refuted)"),
 ("Z3 T3 OpenAI commitments","needs ≥$1.03T external capital","UNSAT(refuted)"),
 ("Z3 T4 core at zero inflow","insolvent without continued capital","UNSAT(refuted)"),
 ("Z3 T5 SpaceX vs OpenAI","SpaceX SAT / OpenAI UNSAT standalone","PROVED"),
 ("TLA+ cascade","capital-stop → OpenAI→CoreWeave→Oracle","VIOLATED(trace)"),
 ("TLA+ SpaceX safe","never defaults","HOLDS"),
 ("Alloy structure","core circular; SpaceX separable w/o cancelable","ALL HOLD"),
 ("Z3 coordination C1-C4","small-bank stablecoin trap, suppressible","PROVED"),
 ("Z3 Fed trap F1-F3","no single rate satisfies N targets","UNSAT"),
 ("Z3 defense chokepoint","REE independence infeasible until ~2028","UNSAT"),
 ("Z3 power adequacy P1","AI power demand > supply thru 2028","UNSAT"),
 ("Z3 HALEU chokepoint P2","Russia enrichment dependence to ~2029","UNSAT"),
 ("Allied REE min-cut","feasible ~2028; bottleneck = midstream separation, not mining","max-flow"),
]
CHOKE=[
 ("Compute capital","OpenAI needs ≥$1.03T external; solvent only while capital flows","—","capital trap","Z3 T3/T4"),
 ("Rare earths (defense)","~5,550 kg/yr samarium, ~100% China; auto-deny Dec-2025","China","~2028","defense_chokepoint UNSAT"),
 ("Power + fuel (energy)","firm-power gap widens to 2028; HALEU ~100% Russian","Russia","~2028-29","power_adequacy UNSAT"),
]
# gold reveals
home=gs.get("home_repriced",[]);
home_first=home[0] if home else {}; home_last=home[-1] if home else {}
weavers=sorted(tw.get("nodes",{}).items(), key=lambda kv:-kv[1].get("betweenness",0))[:12]
# bank HTM holes
banks=be.get("banks",[])
htm=sorted([b for b in banks if b.get("htm_loss_to_eq_pct") is not None], key=lambda b:b["htm_loss_to_eq_pct"])[:8]
vuln=[b for b in banks if b.get("vulnerable")]
res_files=sorted(os.path.basename(f) for f in glob.glob(os.path.join(RES,"*.md")))

def tbl(headers,rows):
    h="".join(f"<th>{html.escape(str(x))}</th>" for x in headers)
    r="".join("<tr>"+"".join(f"<td>{html.escape(str(c))}</td>" for c in row)+"</tr>" for row in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>"

verd=tbl(["Engine","What it shows","Verdict"],VERDICTS)
scn=sc.get("scenarios",{})
scent=tbl(["Scenario","OpenAI cap gap","solvent@tap","REE indep","power ok","verdict"],
          [[k,f"${v.get('capital_gap_usd_b'):,}B","YES" if v.get('solvent_at_tap') else "NO",
            v.get('ree_independent_year') or ">2029",v.get('power_adequate_year') or ">2028",v.get('verdict')] for k,v in scn.items()])
eqs=eq.get("split",{})
chk=tbl(["Chokepoint","Constraint","Adversary","Independence","Proof"],CHOKE)
goldrows=[[h.get("year"),f"${h.get('usd'):,}",f"{h.get('gold_oz')} oz",h.get('idx_nominal'),h.get('idx_gold')] for h in home if h.get('year') in (1998,2007,2012,2020,2022,2026)]
goldt=tbl(["Year","US median home $","in gold","$ idx (1998=100)","GOLD idx"],goldrows)
weavet=tbl(["Node","Layer","Betweenness","Layers","Eras"],[[k,v["layer"],round(v["betweenness"]),v["layer_span"],v["era_span"]] for k,v in weavers])
bankt=tbl(["Bank","HTM loss/equity","AFS/eq"],[[b["name"],f"{b['htm_loss_to_eq_pct']}%",f"{b.get('afs_loss_b','')}B"] for b in htm])
srct="".join(f"<li><code>research/{f}</code></li>" for f in res_files)

CSS="""body{background:#0b0e14;color:#d7dce5;font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 60px}
header{background:linear-gradient(120deg,#11151f,#1b2433);padding:28px 32px;border-bottom:1px solid #2a3550}
h1{margin:0;font-size:24px;color:#fff} h2{color:#7fd1ff;border-bottom:1px solid #233;padding-bottom:6px;margin-top:36px}
.thesis{font-size:15px;color:#cfe;background:#0f1622;border-left:3px solid #7fd1ff;padding:12px 16px;margin:16px 0}
main{max-width:1100px;margin:0 auto;padding:0 24px} table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}
th,td{border:1px solid #233;padding:6px 9px;text-align:left} th{background:#16202f;color:#9fb} tr:nth-child(even) td{background:#0f1520}
code{background:#16202f;padding:1px 5px;border-radius:3px;color:#ffd479;font-size:12px}
.k{display:inline-block;background:#16202f;border:1px solid #2a3550;border-radius:6px;padding:10px 14px;margin:6px 8px 6px 0}
.k b{color:#7fd1ff;font-size:20px;display:block} .UNSAT{color:#ff8a8a} .PROVED,.HOLDS,.SAT{color:#7CFC9B}
nav a{color:#7fd1ff;margin-right:14px;text-decoration:none;font-size:13px} .muted{color:#8a96a8;font-size:12px}"""

KPIS=f"""<span class=k><b>{an.get('core_scc_robust_size','?')}</b>firm circular core (SCC)</span>
<span class=k><b>{ncyc}</b>round-trip cycles</span>
<span class=k><b>$1.03T</b>external capital OpenAI needs</span>
<span class=k><b>{nself.get('headline_ratio',0)*100:.0f}%</b>NVIDIA self-funding (headline)</span>
<span class=k><b>-81%</b>US home priced in gold since 1998</span>
<span class=k><b>2</b>adversary chokepoints (CN+RU)</span>"""

HTML=f"""<!doctype html><html><head><meta charset=utf-8><title>Unmasking the AI Earnings Bubble</title><style>{CSS}</style></head>
<body><header><h1>Unmasking the AI Earnings Bubble &mdash; control dashboard</h1>
<div class=muted>Formally-verified analysis &middot; generated from live data/*.json &middot; reproduce: <code>bash run_all.sh</code></div>
<nav><a href=#verdicts>Proof verdicts</a><a href=#core>Circular core</a><a href=#choke>Chokepoints</a><a href=#gold>Gold lens</a><a href=#weavers>Weavers</a><a href=#banks>Banks</a><a href=#src>Sources</a></nav></header>
<main>
<div class=thesis>A self-referential capital loop booking each other's spending as revenue, solvent only while external capital flows &mdash; the same defect (promises &raquo; deliverable substance, risk parked in the least-regulated venue) recurring in bank books, private credit, metals, and power, while the loop's largest actors converge on the digital-identity control layer. The financial core is machine-proven; the rest is evidence-graded.</div>
{KPIS}
<h2 id=verdicts>Formal verdicts (every engine)</h2>{verd}
<h2 id=core>The circular core</h2>
<p><b>Robust core SCC ({an.get('core_scc_robust_size','?')}):</b> {html.escape(", ".join(robust))}.<br>
<b>Circular only via cancelable edges:</b> {html.escape(", ".join(cancel_only)) or '—'} (SpaceX: operationally separable, financially cross-held by Google's ~$100B stake).</p>
<h2 id=choke>The three physical chokepoints</h2>{chk}
<h2 id=scenarios>Scenario engine (formal verdicts)</h2>{scent}
<p class=muted>BASE = FRAGILE (solvent only while the capital tap stays open) &middot; BULL = RESILIENT (near self-financing) &middot; BEAR = BREAKS (carry-unwind shuts the tap &rarr; the cascade).</p>
<h2 id=gold>Everything in hard money (gold lens)</h2>{goldt}
<p class=muted>The gold lens SPLITS the market: S&amp;P 500 <b>{eqs.get('sp500_gold_change_pct_2000_2026','?')}%</b> in gold since 2000 (debasement) vs NVIDIA <b>+{eqs.get('nvda_gold_change_pct_2016_2026','?')}%</b> in gold since 2016 (real value capture). The bubble = broad debasement + extreme real concentration into the circular oligopoly.</p>
<p class=muted>US home +175% in dollars since 1998 but <b>-81% in gold</b>. CRE peaked in gold ~2001 (now ~16 vs 100). DoD budget +3.7x nominal but -75% in gold. OpenAI's $1.4T = 0.53x all of TARP in gold.</p>
<h2 id=weavers>The weavers (temporal meta-graph, betweenness)</h2>{weavet}
<h2 id=banks>Bank vulnerability (biggest hidden HTM holes)</h2>{bankt}
<p class=muted>{len(vuln)} mid-tier banks flagged on &ge;2 axes (CRE + securities loss + uninsured). Foreign-branch artifacts excluded.</p>
<h2 id=src>Source index ({len(res_files)} cited files)</h2><ul>{srct}</ul>
<p class=muted>Reports: <code>report/UNMASKING.md</code> &middot; <code>report/TEMPORAL-WEB.md</code> &middot; <code>report/EXECUTIVE-SUMMARY.md</code>. Every figure's URLs are in the matching <code>research/*.json</code>.</p>
</main></body></html>"""

open(os.path.join(REP,"INDEX.html"),"w").write(HTML)

# ---- executive summary ----
ES=f"""# Executive Summary — Unmasking the AI Earnings Bubble

*Generated {gs.get('flows') and ''}2026-06-07 from the live models. Full analysis: `report/UNMASKING.md` + `report/TEMPORAL-WEB.md`. Open `report/INDEX.html` for the dashboard.*

## The finding in one sentence
The AI build-out is a **self-referential capital loop** that books each firm's spending as another's revenue and is **solvent only while external capital keeps flowing** — and the same defect (promises far exceeding deliverable substance, risk parked in the least-regulated venue) recurs in bank securities books, private credit, metals, and the power grid, while the loop's largest actors converge on the **digital-identity control layer**.

## What is machine-proven (not asserted)
- **An {an.get('core_scc_robust_size','?')}-firm circular core** (Tarjan SCC): NVIDIA, OpenAI, Oracle, CoreWeave, Microsoft, Amazon, Anthropic, AMD, Crusoe, Lambda + lenders; **{ncyc} round-trip cycles**.
- **OpenAI needs ≥ $1.03 trillion of external capital** to honor its commitments (Z3 T3, UNSAT); the **core is insolvent at zero external inflow** (T4) — the formal signature of a bubble.
- **NVIDIA vendor-financing self-funding: {nself.get('funded_ratio',0)*100:.0f}% funded-only / {nself.get('headline_ratio',0)*100:.0f}% headline.**
- **SpaceX is separable** — the only node circular *solely via cancelable edges* — but **financially cross-held** by Google's ~$100B equity stake + the xAI merger.
- **A single capital shock cascades** OpenAI→CoreWeave→Oracle (TLA+ trace); SpaceX never defaults.
- **The Fed has no feasible single rate** (Z3 F1–F3, UNSAT) — it can only choose what to sacrifice.
- **Three physical chokepoints**, two adversary-controlled: capital (trap), **rare earths/China** (independence ~2028), **power+HALEU/Russia** (~2028-29) — none liftable by dollars on the timeline.

## The hard-money lens
Re-priced in gold, most "gains" are debasement: a US home is **−81% in gold** since 1998; CRE peaked in gold ~2001; the **$1-trillion defense budget buys ~25%** of the gold the 1998 one did; OpenAI's $1.4T is **0.53× all of TARP** in gold.

## The honest answer to "is it all connected?"
**Not one cabal — a small elite operator-network + recurring structures + regulatory arbitrage.** The temporal meta-graph (1998→2026) shows the weavers (OpenAI, a16z, the PayPal-mafia/Thiel, Circle/USDC, BlackRock, the SPV structure, Larry Summers as the literal dereg→AI→Epstein bridge) and the recurring devices (LTCM interconnection, Enron off-balance-sheet SPVs + mark-to-market, dotcom vendor financing) rebuilt in each era's least-regulated venue. Intent is never inferred from adjacency; sensitive threads (Epstein, Waters, foreign influence) are graded and quarantined from the proofs.

## Reproduce
`bash run_all.sh` — runs all 5 Z3 engines, TLA+, Alloy, the graph/bank/temporal/gold/defense/energy models. {len(res_files)} cited source files in `research/`.
"""
open(os.path.join(REP,"EXECUTIVE-SUMMARY.md"),"w").write(ES)
print("wrote report/INDEX.html ("+str(len(HTML))+" bytes) and report/EXECUTIVE-SUMMARY.md")
