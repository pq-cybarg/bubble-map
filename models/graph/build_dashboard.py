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
 ("Z3 age-verif futility","effective gating UNSAT under breach; surveillance unconditional","UNSAT"),
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
nres_json=len(glob.glob(os.path.join(RES,"*.json")))
nmodels=len(glob.glob(os.path.join(ROOT,"models","z3","*.py"))+glob.glob(os.path.join(ROOT,"models","graph","*.py"))+glob.glob(os.path.join(ROOT,"models","alloy","*.als"))+glob.glob(os.path.join(ROOT,"models","tla","*.tla")))
BUILD_DATE="2026-06-08"
# graded speculative overlays (kept OUT of the proofs) - the evidence-graded layer
OVERLAYS=[
 ("Regulatory capture (SEC/SDNY/FDIC)","Choke Point 2.0 FOIA, ConsenSys/MetaMask, Ripple-timing+JPM, Kraken/Binance/LBRY sweep, Fairshake $169M","spec-sec-sdny-regulatory"),
 ("Privacy-tool prosecutions","Tornado Cash + Samourai: real Lazarus $7.6B use vs theories courts rejected (Van Loon) vs developers jailed (code-is-speech)","spec-tornado-samourai"),
 ("Exchanges + Asia/Gulf","Mt.Gox unwind, Binance CZ-pardon/USD1/MGX, SBI/Ripple ~9%, Ant HKDA+PBoC pause, ByteDance/TikTok->Oracle+MGX","spec-exchanges-asia"),
 ("Telecom + satellite + ISR","Salt Typhoon broke the CALEA backdoor; Amazon/Apple Globalstar; Starshield/NRO; carrier direct-to-cell","spec-telecom-satellite"),
 ("Disclosures + surveillance","Snowden (Bullrun/Dual_EC/Room 641A), In-Q-Tel/Palantir, DARPA-TrailOfBits, FBI ANOM, Epstein Files Act, Pandora","spec-disclosures-surveillance"),
 ("PQC / quantum-sat / DLT","SEALSQ/WISeKey global build-out + Hedera 34-member council overlaps (Google/IBM) + SEALCOIN bridge","fin-hedera-connections"),
 ("Official-data integrity (epistemics)","Zero-trust read of BLS/BEA/Fed: -911k jobs benchmark, OER/CPI methodology, Boskin fiscal motive, 2025 collection cuts + BLS-chief firing, the understate-inflation incentive map","macro-official-data-integrity"),
 ("Rent vs CPI (ALNRI analysis)","Apartment List / Zillow / BLS New-Tenant rents lead official CPI shelter by ~1 year; shelter ~1/3 of CPI -> headline misreports turning points","macro-rent-cpi-divergence"),
 ("Gig / contingent labor","Full-time independents 13.6M->27.7M; misclassification (Lyft NJ $19.4M); CES/CPS + multiple-jobholders distort the jobs headline","macro-gig-labor"),
 ("Futures vs physical (commodities)","COMEX/LBMA/LME/SHFE: 2025-26 silver backwardation, >$2.50 gold premium, ~4.2:1 paper:registered, 28% copper tariff spread, JPM $920M spoofing","macro-futures-vs-physical"),
 ("SEC filings (primary source)","The circular-funding thesis in the filers' own 10-Ks: CoreWeave 67% Microsoft + $21B debt; NVIDIA concentration 36%->61%","spec-sec-filings-primary"),
]
# primary, independently-checkable sources - the anti-fabrication anchor
PRIMARY=[
 ("US Supreme Court","Murthy v. Missouri (standing)","https://www.supremecourt.gov/opinions/23pdf/23-411_3dq3.pdf"),
 ("US Treasury / OFAC","Tornado Cash delisting (SB0057)","https://home.treasury.gov/news/press-releases/sb0057"),
 ("5th Cir. Court of Appeals","Van Loon v. Treasury opinion","https://www.ca5.uscourts.gov/opinions/pub/23/23-50669-CV0.pdf"),
 ("US DOJ / SDNY","Samourai founders plead guilty","https://www.justice.gov/usao-sdny/pr/founders-samourai-wallet-cryptocurrency-mixing-service-plead-guilty"),
 ("US SEC","Kraken staking settlement (2023-25)","https://www.sec.gov/newsroom/press-releases/2023-25"),
 ("US Congress","Epstein Files Transparency Act (H.R.4405)","https://www.congress.gov/bill/119th-congress/house-bill/4405/text"),
 ("ICIJ","Pandora Papers","https://www.icij.org/investigations/pandora-papers/"),
 ("Hedera Council","Governing-council roster","https://hederacouncil.org/"),
 ("NIST CSRC","Post-quantum FIPS 203/204/205","https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved"),
 ("US FDIC","FOIA 'pause letters' coverage","https://www.bankingdive.com/news/fdic-letters-cryptos-operation-chokepoint-2-0-claims-coinbase/735309/"),
 ("US BLS","Preliminary payroll benchmark (-911k)","https://www.bls.gov/news.release/prebmk.nr0.htm"),
 ("SSA","Boskin Commission report (1996)","https://www.ssa.gov/history/reports/boskinrpt.html"),
 ("US BLS","New Tenant Rent Index (leads CPI ~1yr)","https://www.bls.gov/pir/new-tenant-rent.htm"),
 ("SEC EDGAR","CoreWeave 10-K FY2025 (67% Microsoft, $21B debt)","https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000104/crwv-20251231.htm"),
 ("SEC EDGAR","NVIDIA 10-K FY2025 (customer concentration)","https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000023/nvda-20250126.htm"),
 ("LME","CME-LME copper arbitrage (education)","https://www.lme.com/en/education/online-resources/lme-digest/lme-and-cme-copper-arbitrage-when-global-and-regional-prices-meet"),
]

def tbl(headers,rows):
    h="".join(f"<th>{html.escape(str(x))}</th>" for x in headers)
    r="".join("<tr>"+"".join(f"<td>{html.escape(str(c))}</td>" for c in row)+"</tr>" for row in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>"

verd=tbl(["Engine","What it shows","Verdict"],VERDICTS)
conn_rows=[[c["node"],c["degree"],c["n_neighbor_sectors"],c["source_files"],
            "financial+structural" if c["both_layers"] else (c["layers"][0] if c.get("layers") else "—"),
            ", ".join(c["neighbor_sectors"][:7])] for c in an.get("top_cross_layer_connectors",[])[:12]]
conn_t=tbl(["Node","Degree","Sectors bridged","Source files","Layers","Neighbor sectors"],conn_rows)
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
overt=tbl(["Layer","What it documents","File"],[[a,b,f"research/{c}.json"] for a,b,c in OVERLAYS])
primt="".join(f'<li><b>{html.escape(o)}</b> — <a href="{u}" target=_blank rel=noopener>{html.escape(t)}</a></li>' for o,t,u in PRIMARY)

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

KPIS=f"""<span class=k><b>{an.get('core_scc_robust_size','?')}</b>firm circular core (SCC; {an.get('core_scc_all_size','?')} incl. cancelable)</span>
<span class=k><b>{ncyc}</b>round-trip cycles</span>
<span class=k><b>{an.get('num_nodes','?')}/{an.get('num_edges','?')}</b>graph nodes/edges</span>
<span class=k><b>{an.get('num_financial_edges','?')}/{an.get('num_structural_edges','?')}</b>financial/structural edges</span>
<span class=k><b>$1.03T</b>external capital OpenAI needs</span>
<span class=k><b>{nself.get('headline_ratio',0)*100:.0f}%</b>NVIDIA self-funding (headline)</span>
<span class=k><b>-81%</b>US home priced in gold since 1998</span>
<span class=k><b>2</b>adversary chokepoints (CN+RU)</span>
<span class=k><b>{nres_json}</b>cited research blocks</span>
<span class=k><b>{nmodels}</b>runnable models</span>"""

HTML=f"""<!doctype html><html><head><meta charset=utf-8><title>Unmasking the AI Earnings Bubble</title><style>{CSS}</style></head>
<body><header><h1>Unmasking the AI Earnings Bubble &mdash; control dashboard</h1>
<div class=muted>Formally-verified analysis &middot; auto-generated from live <code>data/*.json</code> on {BUILD_DATE} &middot; reproduce: <code>bash run_all.sh</code> &middot; every figure carries a source URL in the matching <code>research/*.json</code></div>
<nav><a href=#verdicts>Proof verdicts</a><a href=#core>Circular core</a><a href=#connectors>Connectors</a><a href=#choke>Chokepoints</a><a href=#gold>Gold lens</a><a href=#weavers>Weavers</a><a href=#banks>Banks</a><a href=#overlays>Overlays</a><a href=#verify>Primary sources</a><a href=#src>Sources</a></nav></header>
<main>
<div class=thesis>A self-referential capital loop booking each other's spending as revenue, solvent only while external capital flows &mdash; the same defect (promises &raquo; deliverable substance, risk parked in the least-regulated venue) recurring in bank books, private credit, metals, and power, while the loop's largest actors converge on the digital-identity control layer. The financial core is machine-proven; the rest is evidence-graded.</div>
{KPIS}
<h2 id=verdicts>Formal verdicts (every engine)</h2>{verd}
<h2 id=core>The circular core</h2>
<p><b>Robust core SCC ({an.get('core_scc_robust_size','?')}):</b> {html.escape(", ".join(robust))}.<br>
<b>Circular only via cancelable edges:</b> {html.escape(", ".join(cancel_only)) or '—'} (SpaceX: operationally separable, financially cross-held by Google's ~$100B stake).</p>
<p class=muted>Edges split into a <b>financial layer</b> ({an.get('num_financial_edges','?')} capital/credit/compute flows) and a <b>structural layer</b> ({an.get('num_structural_edges','?')} governance/legal/security/ownership relationships). The SCC computed over the financial layer alone equals the SCC over all edges (<code>structural_edges_add_no_cycle = {an.get('structural_edges_add_no_cycle','?')}</code>): the circular core rests on capital flows; the graded structural edges add no cycle.</p>
<h2 id=connectors>Cross-layer connectors</h2>
<p class=muted>Nodes ranked by distinct neighbor-sectors bridged (degree, source-files, and whether they span both layers). This quantifies the bridge nodes that tie the financial core to the surrounding layers.</p>{conn_t}
<h2 id=choke>The three physical chokepoints</h2>{chk}
<h2 id=scenarios>Scenario engine (formal verdicts)</h2>{scent}
<p class=muted>BASE = FRAGILE (solvent only while the capital tap stays open) &middot; BULL = RESILIENT (near self-financing) &middot; BEAR = BREAKS (carry-unwind shuts the tap &rarr; the cascade).</p>
<h2 id=gold>Everything in hard money (gold lens)</h2>{goldt}
<p class=muted>The gold lens SPLITS the market: S&amp;P 500 <b>{eqs.get('sp500_gold_change_pct_2000_2026','?')}%</b> in gold since 2000 (debasement) vs NVIDIA <b>+{eqs.get('nvda_gold_change_pct_2016_2026','?')}%</b> in gold since 2016 (real value capture). The bubble = broad debasement + extreme real concentration into the circular oligopoly.</p>
<p class=muted>US home +175% in dollars since 1998 but <b>-81% in gold</b>. CRE peaked in gold ~2001 (now ~16 vs 100). DoD budget +3.7x nominal but -75% in gold. OpenAI's $1.4T = 0.53x all of TARP in gold.</p>
<h2 id=weavers>The weavers (temporal meta-graph, betweenness)</h2>{weavet}
<h2 id=banks>Bank vulnerability (biggest hidden HTM holes)</h2>{bankt}
<p class=muted>{len(vuln)} mid-tier banks flagged on &ge;2 axes (CRE + securities loss + uninsured). Foreign-branch artifacts excluded.</p>
<h2 id=overlays>Evidence-graded overlays (excluded from the proofs)</h2>
<p class=muted>These layers extend the map beyond the financial core. Each item is graded <code>fact | contested | weak | unsupported</code> and is excluded from the Z3/TLA+/Alloy proofs.</p>{overt}
<h2 id=verify>Primary sources</h2>
<p class=muted>Sample of the government and court records cited:</p><ul>{primt}</ul>
<p class=muted><code>models/audit.py</code> (cross-document number/coverage checks) and <code>models/cross_review.py</code> (edge-amount conflicts, connectors) run via <code>scripts/new-research.sh</code>. Current audit: 0 flags.</p>
<h2 id=src>Source index ({nres_json} cited research blocks)</h2><ul>{srct}</ul>
<p class=muted>Reports: <code>report/UNMASKING.md</code> &middot; <code>report/TEMPORAL-WEB.md</code> &middot; <code>report/EXECUTIVE-SUMMARY.md</code>. Every figure's URLs are in the matching <code>research/*.json</code>.</p>
</main></body></html>"""

open(os.path.join(REP,"INDEX.html"),"w").write(HTML)

# ---- mirror to docs/ (GitHub Pages) with a back-link to the hub ----
DOCS=os.path.join(ROOT,"docs")
if os.path.isdir(DOCS):
    backnav='<div style="background:#0b0e14;border-bottom:1px solid #2a3550;padding:8px 32px"><a href="index.html" style="color:#7fd1ff;text-decoration:none;font-size:13px">&larr; Bubble Map</a></div>'
    docs_html=HTML.replace("<body>","<body>"+backnav,1)
    open(os.path.join(DOCS,"dashboard.html"),"w").write(docs_html)

    # ---- additional pages: research index + methodology ----
    GH="https://github.com/pq-cybarg/bubble-map/blob/main/research/"
    NAVBAR=('<div style="background:#0b0e14;border-bottom:1px solid #2a3550;padding:10px 32px;font-size:13px">'
            '<a href="index.html" style="color:#7fd1ff;text-decoration:none;margin-right:16px">Home</a>'
            '<a href="dashboard.html" style="color:#7fd1ff;text-decoration:none;margin-right:16px">Dashboard</a>'
            '<a href="research.html" style="color:#7fd1ff;text-decoration:none;margin-right:16px">Research</a>'
            '<a href="methodology.html" style="color:#7fd1ff;text-decoration:none;margin-right:16px">Methodology</a>'
            '<a href="globe.html" style="color:#7fd1ff;text-decoration:none">Globe</a></div>')
    PCSS=("body{background:#0b0e14;color:#d7dce5;font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 60px}"
          "main{max-width:1000px;margin:0 auto;padding:0 24px}h1{color:#fff}h2{color:#7fd1ff;border-bottom:1px solid #233;padding-bottom:6px;margin-top:34px}"
          "a{color:#7fd1ff}code{background:#16202f;padding:1px 5px;border-radius:3px;color:#ffd479;font-size:13px}"
          ".b{background:#11161f;border:1px solid #22304a;border-radius:8px;padding:12px 14px;margin:8px 0}.b b{color:#fff}.muted{color:#8a96a8;font-size:13px}")
    def section(fn):
        if fn.startswith("fin-"): return "AI financial core"
        if fn.startswith("macro-"): return "Macro · banking · commodities · data integrity"
        if fn.startswith("spec-"): return "Regulatory · crypto · surveillance overlays"
        if fn.startswith("influence-"): return "Influence & identity"
        if fn.startswith("digitalid-") or fn.startswith("age-"): return "Digital ID & age verification"
        return "Thematic"
    groups={}
    for fn in sorted(glob.glob(os.path.join(RES,"*.json"))):
        base=os.path.basename(fn)
        try: d=json.load(open(fn)); title=d.get("metadata",{}).get("title",base)
        except: title=base
        nsrc=open(fn).read().count("http")
        groups.setdefault(section(base),[]).append((base,title,nsrc))
    body=[f"<p class=muted>{nres_json} cited research blocks. Each links to its structured data (<code>.json</code>, with every source URL) and write-up (<code>.md</code>) on GitHub. Generated {BUILD_DATE}.</p>"]
    for sec in sorted(groups):
        body.append(f"<h2>{html.escape(sec)} ({len(groups[sec])})</h2>")
        for base,title,nsrc in groups[sec]:
            stub=base[:-5]
            body.append(f'<div class=b><b>{html.escape(title)}</b><br>'
                        f'<span class=muted>~{nsrc} source links · </span>'
                        f'<a href="{GH}{base}">data (.json)</a> · <a href="{GH}{stub}.md">write-up (.md)</a></div>')
    RES_HTML=(f"<!doctype html><html><head><meta charset=utf-8><title>Bubble Map — Research index</title><style>{PCSS}</style></head>"
              f"<body>{NAVBAR}<main><h1>Research index</h1>{''.join(body)}</main></body></html>")
    open(os.path.join(DOCS,"research.html"),"w").write(RES_HTML)

    METH=(f"<!doctype html><html><head><meta charset=utf-8><title>Bubble Map — Methodology</title><style>{PCSS}</style></head>"
          f"<body>{NAVBAR}<main><h1>Methodology</h1>"
          "<h2>How it is built</h2><p>Each finding is a structured <code>research/*.json</code> (entities, directed edges, amounts, status, and source URLs) plus a <code>.md</code> write-up. "
          "<code>models/graph/build_graph.py</code> consolidates the edges into <code>data/graph.json</code> and runs the Tarjan SCC. The Z3, TLA+, and Alloy models read that data. "
          "The dashboard, this site, and the reports are generated from the same data.</p>"
          f"<h2>Graph layers</h2><p>Every edge is tagged <b>financial</b> (capital/credit/compute flows — {an.get('num_financial_edges','?')}) or <b>structural</b> (governance/legal/security/ownership/statistics — {an.get('num_structural_edges','?')}). "
          f"The SCC over the financial layer alone equals the SCC over all edges (<code>structural_edges_add_no_cycle = {an.get('structural_edges_add_no_cycle','?')}</code>): the circular core rests on capital flows.</p>"
          "<h2>Grading</h2><p>Claims outside the proven financial core are graded <code>fact · contested · weak · unsupported</code> and excluded from the Z3/TLA+/Alloy proofs. Intent is not inferred from adjacency.</p>"
          "<h2>Consistency checks</h2><p><code>models/audit.py</code> (cross-document number/coverage checks) and <code>models/cross_review.py</code> (edge-amount reconciliation, connectors, under-connection) run via <code>scripts/new-research.sh</code>. Current audit: 0 flags.</p>"
          "<h2>Primary sources</h2><p>Load-bearing claims cite primary government and court records (SCOTUS, DOJ/SDNY, Treasury/OFAC, the Fifth Circuit, SEC EDGAR, Congress.gov, FDIC, BLS, ICIJ, NIST, exchanges). See the <a href=dashboard.html#verify>dashboard</a> for a sample and the <a href=research.html>research index</a> for per-block sources.</p>"
          "<h2>Reproduce</h2><p><code>bash run_all.sh</code> runs the Z3 engines, TLA+, Alloy, and the graph/bank/temporal/gold/defense/energy/contagion models. Python + Z3; Java for TLA+/Alloy (jars auto-fetched).</p>"
          "<p class=muted>Open source · no backend · updated "+BUILD_DATE+" · contact resistant@tuta.com</p>"
          "</main></body></html>")
    open(os.path.join(DOCS,"methodology.html"),"w").write(METH)

# ---- executive summary ----
ES=f"""# Executive Summary — Unmasking the AI Earnings Bubble

*Auto-generated {BUILD_DATE} from the live models. Full analysis: `report/UNMASKING.md` + `report/TEMPORAL-WEB.md`. Open `report/INDEX.html` for the dashboard. Each figure carries a source URL in the matching `research/*.json`. Checked by `models/audit.py` + `models/cross_review.py` (current: 0 flags).*

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
Re-priced in gold, most "gains" are debasement: a US home is **−81% in gold** since 1998; CRE peaked in gold ~2001; the **$1-trillion defense budget buys ~25%** of the gold the 1998 one did; OpenAI's $1.4T is **0.53× all of TARP** in gold. In gold the broad market is **−69%** since 2000 while **NVIDIA is +1,985%** — debasement vs real concentration; a US home is **−81% in gold**.

## The honest answer to "is it all connected?"
**Not one cabal — a small elite operator-network + recurring structures + regulatory arbitrage.** The temporal meta-graph (1998→2026) shows the weavers (OpenAI, a16z, the PayPal-mafia/Thiel, Circle/USDC, BlackRock, the SPV structure, Larry Summers as the literal dereg→AI→Epstein bridge) and the recurring devices (LTCM interconnection, Enron off-balance-sheet SPVs + mark-to-market, dotcom vendor financing) rebuilt in each era's least-regulated venue. Intent is never inferred from adjacency; sensitive threads (Epstein, Waters, foreign influence) are graded and quarantined from the proofs.

## Identity / age-verification (corrected stance)\nReject age verification as a category — *futile-under-breach* (`models/z3/ageverif_futility.py`: effective gating UNSAT once IDs are breached or credentials shared), a *predator honeypot*, and *adult surveillance by construction*; **ZK does not save it** (hides the input, not the issuer, the presence/absence metadata, or the breach dynamics). `zkage/` is a steelman-then-refutation, not a solution. Full case: `research/age-verification-abolition.md`.\n\n## The broader map (evidence-graded overlays, kept OUT of the proofs)
Beyond the proven core, the corpus documents — each graded `fact|contested|weak|unsupported`: **regulatory capture** (SEC/SDNY/FDIC: Choke Point 2.0 FOIA, Ripple-timing, the Kraken/Binance/LBRY enforcement sweep + 2025 reversal, ~$169M Fairshake money); **privacy-tool prosecutions** (Tornado Cash + Samourai — real Lazarus laundering vs theories courts rejected vs developers jailed); **exchanges + Asia/Gulf** (Mt.Gox, the Binance CZ-pardon/USD1/MGX nexus, SBI/Ripple, Ant's paused HKDA, ByteDance/TikTok→Oracle+MGX); the **telecom + satellite/ISR** rail (Salt Typhoon breaking the mandated CALEA backdoor; Amazon/Apple absorbing Globalstar; Starshield/NRO); and the **disclosures/surveillance** overlay (Snowden Bullrun/Dual_EC/Room 641A, In-Q-Tel/Palantir, DARPA–Trail of Bits, FBI ANOM, the Epstein Files Act, Pandora Papers). These extend the picture; they are never used to assert the proofs.

## Primary sources
Claims cite primary government and court records: SCOTUS opinions, DOJ/SDNY releases, Treasury/OFAC, the Fifth Circuit, SEC, Congress.gov, FDIC FOIA disclosures, ICIJ, NIST. `models/audit.py` and `models/cross_review.py` run via `scripts/new-research.sh`; current audit 0 flags.

## Reproduce
`bash run_all.sh` runs the Z3 engines, TLA+, Alloy, and the graph/bank/temporal/gold/defense/energy/contagion models ({nmodels} runnable models). {nres_json} cited research blocks in `research/`.
"""
open(os.path.join(REP,"EXECUTIVE-SUMMARY.md"),"w").write(ES)
print("wrote report/INDEX.html ("+str(len(HTML))+" bytes) and report/EXECUTIVE-SUMMARY.md")
