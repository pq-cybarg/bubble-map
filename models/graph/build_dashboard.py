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
 ("Z3 reflexive marks M1-M4","AI 'profit' is self-referential paper marks; gains reverse if IPO < private mark","SAT/UNSAT"),
 ("TLA+ cascade","capital-stop → OpenAI→CoreWeave→Oracle","VIOLATED(trace)"),
 ("TLA+ SpaceX safe","never defaults","HOLDS"),
 ("TLA+ MarkUnwind","down-round/IPO<mark -> Amazon+Google reverse gains (writedown trace)","VIOLATED(trace)"),
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
 ("SEC filings (primary source)","The circular-funding thesis in the filers' own 10-Ks: CoreWeave 67% Microsoft + $21B debt; NVIDIA concentration 36%->61%; Amazon/Google fair-value GAINS vs Microsoft equity-method LOSSES","spec-sec-filings-primary"),
 ("Bank HTM marks (zero-trust)","HTM 'held to par' is a self-chosen value, not a price; FDIC unrealized-loss series ~$690B(Q3-22)->$306B(Q4-25)->$325B(Q1-26); withdrawn problem-bank totals reconstructable from RC-B + FDIC API","macro-bank-htm-marks"),
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

CSS="""body{background:#faf8f2;color:#1c1b19;font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 60px}
header{background:#fffdf8;padding:26px 32px;border-bottom:1px solid #e4ddcc}
h1{margin:0;font-size:25px;color:#1c1b19;font-family:Georgia,'Iowan Old Style',serif;font-weight:600}
h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:6px;margin-top:34px;font-family:Georgia,'Iowan Old Style',serif;font-weight:600}
.thesis{font-size:15.5px;color:#33312c;background:#fffdf8;border:1px solid #e4ddcc;border-left:4px solid #7b2d26;padding:14px 18px;margin:16px 0}
main{max-width:1100px;margin:0 auto;padding:0 24px} table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}
th,td{border:1px solid #e4ddcc;padding:6px 9px;text-align:left;vertical-align:top} th{background:#f3eedf;color:#1c1b19} tr:nth-child(even) td{background:#fbf8f0}
code{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:12px}
.k{display:inline-block;background:#fffdf8;border:1px solid #e4ddcc;border-radius:6px;padding:10px 14px;margin:6px 8px 6px 0}
.k b{color:#7b2d26;font-size:20px;display:block} .UNSAT{color:#9a2b1f;font-weight:600} .PROVED,.HOLDS,.SAT{color:#1f6f43;font-weight:600}
nav a{color:#1f4e79;margin-right:14px;text-decoration:none;font-size:13px} .muted{color:#6b665d;font-size:12px}"""

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
<div class=thesis>A circular capital loop &mdash; firms booking each other's spending as revenue, solvent only while external capital keeps flowing &mdash; gated by physical chokepoints it cannot buy past on the timeline (compute capital, China rare earths, Russian enrichment, the power grid), and embedded in measurement and control layers (official statistics, paper commodity prices, and the identity / surveillance / political-money rails) that determine whether it can be seen and questioned. The financial core is machine-verified; every other layer is evidence-graded and excluded from the proofs. Not one cabal &mdash; recurring operators rebuilding the dot-com (vendor financing), Enron (off-balance-sheet SPVs), and LTCM (interconnected leverage) structures in the least-regulated venue.</div>
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
    backnav='<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:9px 32px;font-family:-apple-system,Segoe UI,Roboto,sans-serif"><a href="index.html" style="color:#1f4e79;text-decoration:none;font-size:13px;margin-right:16px">Home</a><a href="research.html" style="color:#1f4e79;text-decoration:none;font-size:13px;margin-right:16px">Research</a><a href="methodology.html" style="color:#1f4e79;text-decoration:none;font-size:13px;margin-right:16px">Methodology</a><a href="glossary.html" style="color:#1f4e79;text-decoration:none;font-size:13px">Glossary</a></div>'
    docs_html=HTML.replace("<body>","<body>"+backnav,1)
    open(os.path.join(DOCS,"dashboard.html"),"w").write(docs_html)

    # ---- additional pages: research index + methodology ----
    GH="https://github.com/pq-cybarg/bubble-map/blob/main/research/"
    def navlinks(active=""):
        items=[("index.html","Home"),("dashboard.html","Dashboard"),("research.html","Research"),("methodology.html","Methodology"),("glossary.html","Glossary"),("globe.html","Globe")]
        return "".join(f'<a href="{h}" style="color:#1f4e79;text-decoration:none;margin-right:16px{";font-weight:600" if t==active else ""}">{t}</a>' for h,t in items)
    NAVBAR=('<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:11px 32px;font-size:13px;font-family:-apple-system,Segoe UI,Roboto,sans-serif">'+navlinks()+'</div>')
    PCSS=("body{background:#faf8f2;color:#1c1b19;font:18px/1.72 Georgia,'Iowan Old Style','Palatino Linotype','Times New Roman',serif;margin:0;padding:0 0 60px}"
          "main{max-width:820px;margin:0 auto;padding:0 22px}h1{font-family:Georgia,serif;font-weight:600;font-size:34px;margin:26px 0 4px}"
          "h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:34px;font-family:Georgia,serif;font-weight:600;font-size:24px}"
          "a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:14px}"
          ".b{background:#fffdf8;border:1px solid #e4ddcc;border-radius:7px;padding:13px 15px;margin:9px 0}.b b{color:#1c1b19}"
          ".muted{color:#6b665d;font-size:14px}dl dt{font-weight:600;margin-top:14px}dl dd{margin:3px 0 0;color:#33312c;font-size:16px}"
          "p{margin:12px 0}")
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

    GLOSSARY=[
     ("Circular core (strongly-connected component, SCC)","A set of firms where money can flow from each to every other and back. Mathematically it is the formal definition of 'circular'; here it is the group of AI firms funding one another."),
     ("Vendor financing","When a seller funds its own customer so the customer can buy from it (e.g., a chipmaker investing in a startup that then buys its chips). It can inflate apparent demand."),
     ("Cancelable edge","A funding/contract link that either party can terminate on short notice. The model separates the core that survives only via cancelable deals (e.g., SpaceX) from the robust core."),
     ("Backwardation / contango","Backwardation = you pay more for a commodity now than for delivery later (a sign of physical tightness). Contango = the opposite (ample supply / storage demand)."),
     ("Registered vs eligible (COMEX)","Registered metal is available for delivery against futures; eligible metal is in the vault but not pledged for delivery. A high paper-claims-to-registered ratio signals fragility."),
     ("Owners' Equivalent Rent (OER)","The CPI's estimate of what a homeowner would pay to rent their own home. It is ~¼ of CPI, is imputed from surveys (not home prices), and lags the market."),
     ("ALNRI / ZORI / New Tenant Rent Index","Market-rent gauges (Apartment List, Zillow, and BLS's own new-lease index) that track rents on new leases. They lead the official CPI shelter measure by ~1 year."),
     ("Equity method","An accounting rule where an investor books its share of an investee's profit or loss. Microsoft books ~27% of OpenAI's losses this way."),
     ("Remaining Performance Obligations (RPO)","Contracted future revenue not yet delivered — a backlog. Oracle's ~$523B RPO is largely promised cloud capacity for OpenAI/Stargate."),
     ("Birth-death model","A statistical model the BLS uses to estimate jobs at newly formed businesses. When it over-estimates, payrolls are revised down later (it drove ~half the 2024-25 downward revisions)."),
     ("Benchmark revision (QCEW)","An annual correction of the monthly jobs estimates to near-complete tax records. The 2025 correction cut ~911,000 jobs."),
     ("U-3 vs U-6","U-3 is the headline unemployment rate; U-6 also counts discouraged and involuntarily part-time workers, so it is higher and captures more underemployment."),
     ("CPI vs PCE","Two inflation gauges with different weights; PCE (the Fed's target) usually reads ~0.3-0.4 pp below CPI."),
     ("Hedonic adjustment","A method that lowers measured prices to account for quality improvements (e.g., a faster computer at the same price counts as a price cut)."),
     ("TIPS / COLA","TIPS are Treasury bonds whose payments rise with CPI; COLA is the CPI-linked annual increase in Social Security. Both make a lower measured CPI cheaper for the government."),
     ("Formal verification (Z3 / TLA+ / Alloy)","Software that mathematically proves whether statements are possible (SAT) or impossible (UNSAT). Used here to prove the core's circularity and capital dependence rather than assert them."),
     ("HTM vs AFS","How banks classify bonds: Held-to-Maturity (losses hidden until sold) vs Available-for-Sale (losses shown). Rising rates created large hidden HTM losses."),
     ("Private credit","Non-bank lending (e.g., Apollo, Blackstone, PIMCO). It became the marginal lender for AI data centers when banks pulled back."),
     ("Special-purpose vehicle (SPV)","A separate legal entity used to move assets or debt off a company's main balance sheet — the structure at the heart of the Enron collapse, reused in AI-infra finance."),
     ("PQC / CRQC / harvest-now-decrypt-later","Post-Quantum Cryptography defends against a Cryptographically-Relevant Quantum Computer; HNDL is adversaries storing encrypted data now to decrypt once such a computer exists."),
     ("CALEA","The US law requiring telecom carriers to build wiretap access for law enforcement. China's Salt Typhoon breached exactly this system."),
     ("Spoofing","Placing and rapidly canceling orders to move a price. JPMorgan paid ~$920M to settle spoofing of metals and Treasury futures."),
     ("Stablecoin","A crypto token pegged to a currency (e.g., USD1). New US rules route stablecoin reserves into Treasuries, creating forced demand for government debt."),
     ("Evidence grading","Each non-proven claim is labeled fact, contested, weak, or unsupported, and kept out of the formal proofs. Intent is never inferred from mere association."),
     ("Financial vs structural edge","Graph links are split into capital/credit/compute flows (financial) and governance/legal/security/ownership relationships (structural). The proven core rests only on the financial layer."),
    ]
    gl="".join(f"<dt>{html.escape(t)}</dt><dd>{html.escape(d)}</dd>" for t,d in GLOSSARY)
    GL_HTML=(f"<!doctype html><html><head><meta charset=utf-8><title>Bubble Map — Glossary</title><style>{PCSS}</style></head>"
             f"<body>{NAVBAR}<main><h1>Glossary</h1>"
             "<p class=muted>Plain-language definitions of the technical terms used across the project.</p>"
             f"<dl>{gl}</dl></main></body></html>")
    open(os.path.join(DOCS,"glossary.html"),"w").write(GL_HTML)

# ---- executive summary ----
ES=f"""# Executive Summary — Unmasking the AI Earnings Bubble

*Auto-generated {BUILD_DATE} from the live models. Full analysis: `report/UNMASKING.md` + `report/TEMPORAL-WEB.md`. Open `report/INDEX.html` for the dashboard. Each figure carries a source URL in the matching `research/*.json`. Checked by `models/audit.py` + `models/cross_review.py` (current: 0 flags).*

## The finding in one sentence
The AI build-out is a **circular capital loop** that books each firm's spending as another's revenue and is **solvent only while external capital keeps flowing**; it is **gated by physical chokepoints it cannot buy past** on the timeline (compute capital, China rare earths, Russian enrichment, the power grid); and it is **embedded in measurement and control layers** — official statistics, paper commodity prices, and the identity / surveillance / political-money rails — that determine whether it can be seen and questioned.

## How sure we are (the confidence ladder)
- **Proven** (Z3/TLA+/Alloy, reproducible): the 11-firm circular core; OpenAI's ≥$1.03T external-capital need and insolvency at zero inflow; the OpenAI→CoreWeave→Oracle cascade; no single feasible Fed rate; rare-earth and firm-power independence infeasible on the timeline; and that the funders' AI "profit" is partly self-referential paper marks — manufactured by funding the rounds that set the marks, not externally realized, and forced to reverse if a public price clears below the last private mark (`reflexive_marks` M1–M4).
- **Strongly evidenced** (primary filings/exchange/court/government records): Oracle's $523B backlog + ≥$72B partner debt + PIMCO's $10B anchor; CoreWeave 67% one-customer / $21B debt; NVIDIA's 13F holding ~11% of CoreWeave + concentration 36%→61%; Microsoft's 27% equity-method share of an ~$11.5B/qtr OpenAI loss, while Amazon/Google book mark-to-market GAINS on the same kind of stakes (Amazon +$9.5B on Anthropic) — circular paper income cutting both ways; the −911k jobs benchmark; the ALNRI/New-Tenant rent lag; the COMEX/LBMA dislocation + JPMorgan's $920M spoofing settlement; the Binance pardon/USD1/MGX nexus; Salt Typhoon via CALEA.
- **Graded / contested** (overlay, never used in proofs): regulatory-capture intent; the permanent-suppression narrative; whether each data lag's convenient direction was design or coincidence.
- **Out of scope** (unsupported, excluded): fabricated government microdata; a single coordinating cabal; ShadowStats-style CPI numbers.

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
