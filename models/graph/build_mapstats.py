#!/usr/bin/env python3
"""build_mapstats.py - render docs/mapstats.html: the 'Map health / by the numbers' page (#108-style).

A data-driven snapshot of the corpus's integrity, straight from data/graph.json + theme-blocks.json
+ the research blocks + persons.json: headline tiles (nodes, financial/structural edges, the circular
SCC 12/11, research blocks, themes, people), the circular-core members, theme distribution, node-sector
distribution, the top cross-layer bridge connectors, NVIDIA's self-funding ratio, and a grading mix
(a keyword tally of edge notes - labelled as indicative, not exact). House palette; static SVG bars.
Writes docs/mapstats.html. Regenerable; run from new-research.sh.
"""
import json, os, re, glob
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

INK="#1c1b19"; MUT="#6b665d"; LINE="#e4ddcc"; PAPER="#fffdf8"; AC="#7b2d26"; AC2="#1f4e79"
G = json.load(open(os.path.join(ROOT, "data", "graph.json")))
A = G["analysis"]; ents = G["entities"]
rpages = set(os.path.basename(p)[2:-5] for p in glob.glob(os.path.join(DOCS, "r-*.html")))
try: theme_blocks = json.load(open(os.path.join(DOCS, "theme-blocks.json")))
except Exception: theme_blocks = {}
try: n_people = len(json.load(open(os.path.join(ROOT, "data", "persons.json")))["persons"])
except Exception: n_people = 0

esc = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
def hbar(title, data, note="", color=AC2, unit=""):
    # data = [(label, value, display)]; single-series, direct-labeled
    W = 720; rowh = 26; T = 42; L = 230; R = 92; H = T + rowh * len(data) + (30 if note else 14)
    hi = max([v for _, v, _ in data] or [1]) or 1
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:7px;margin:8px 0">']
    s.append(f'<text x="14" y="24" font-size="13.5" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    for i, (lab, v, disp) in enumerate(data):
        y = T + i * rowh; bw = (W - L - R) * (v / hi)
        s.append(f'<text x="{L-8}" y="{y+rowh/2+3:.0f}" font-size="11" fill="{INK}" text-anchor="end" font-family="sans-serif">{esc(lab)}</text>')
        if bw > 0: s.append(f'<rect x="{L}" y="{y+3:.0f}" width="{bw:.1f}" height="{rowh-9}" rx="3" fill="{color}"/>')
        s.append(f'<text x="{L+bw+6:.1f}" y="{y+rowh/2+3:.0f}" font-size="10.5" font-weight="700" fill="{INK}" font-family="sans-serif">{esc(disp)}</text>')
    if note: s.append(f'<text x="14" y="{H-9}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
    s.append("</svg>"); return "".join(s)

# ---- data ----
n_blocks = len(rpages)
sectors = Counter((m or {}).get("sector", "other") for m in ents.values())
themes = [(t, len(v)) for t, v in theme_blocks.items()]
themes.sort(key=lambda x: -x[1])
grade = Counter()
for fn in glob.glob(os.path.join(RES, "*.json")):
    try: d = json.load(open(fn))
    except Exception: continue
    for e in (d.get("edges") or []):
        t = str(e.get("notes") or e.get("note") or "").lower()
        for g in ("fact", "contested", "interpretation", "speculation", "estimate", "allegation", "weak", "rumor"):
            if re.search(r"\b" + g, t): grade[g] += 1
conn = A.get("top_cross_layer_connectors", [])[:12]
nsf = A.get("nvidia_self_funding", {})

def tiles():
    items = [("entities (nodes)", f"{A['num_nodes']:,}"), ("directed edges", f"{A['num_edges']:,}"),
             ("financial-layer edges", f"{A['num_financial_edges']:,}"), ("structural-layer edges", f"{A['num_structural_edges']:,}"),
             ("circular core (SCC)", f"{A['core_scc_all_size']}"), ("robust core (excl. cancelable)", f"{A['core_scc_robust_size']}"),
             ("research blocks (on-site)", f"{n_blocks:,}"), ("atlas themes", f"{len(theme_blocks)}"),
             ("people (dossiers)", f"{n_people:,}"), ("elementary cycles (bounded)", f"{A.get('num_elementary_cycles','?')}")]
    return ("<div style='display:flex;flex-wrap:wrap;gap:10px;margin:14px 0'>" +
            "".join(f"<div style='flex:1 1 150px;min-width:140px;background:{PAPER};border:1px solid {LINE};border-radius:9px;padding:12px 14px'>"
                    f"<div style='font-size:26px;font-weight:700;color:{AC}'>{v}</div>"
                    f"<div style='font-size:12px;color:{MUT}'>{esc(k)}</div></div>" for k, v in items) + "</div>")

STYLE = (f"body{{background:#faf8f2;color:{INK};font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 50px}}"
         "main{max-width:880px;margin:0 auto;padding:0 18px}h1{font-family:Georgia,serif;font-weight:600;font-size:30px;margin:22px 0 2px}"
         f"h2{{color:{AC};font-family:Georgia,serif;font-size:21px;margin:26px 0 4px;border-bottom:1px solid {LINE};padding-bottom:5px}}"
         f".sub{{color:{MUT};font-size:14px;margin:0 0 6px}}a{{color:{AC2}}}code{{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:13px}}"
         f".core{{background:{PAPER};border:1px solid {LINE};border-radius:8px;padding:10px 14px;margin:8px 0;font-size:14px}}"
         f".core a{{display:inline-block;margin:2px 7px 2px 0}}")

def build():
    core_links = " ".join(f'<a href="bubblemap.html#node={n}">{esc(n.replace("_"," "))}</a>' +
                          ("" if n in A["core_scc_robust_excl_cancelable"] else " <span style='color:#8a8378;font-size:12px'>(headline only)</span>")
                          for n in sorted(A["core_scc_all"]))
    body = ["<h1>Map health - by the numbers</h1>",
            f"<p class=sub>A live snapshot of the corpus's structure and integrity, generated directly from <code>data/graph.json</code>. The headline circular-financing core is the Tarjan SCC over the <b>financial</b> edge layer; it cannot be manufactured by structural edges. See the <a href=core-robustness.html>robustness certificate</a> and <a href=methodology.html>methodology</a>.</p>",
            tiles(),
            "<h2>The circular-financing core</h2>",
            f"<p class=sub>Headline SCC = <b>{A['core_scc_all_size']}</b> firms; robust (excluding cancelable edges) = <b>{A['core_scc_robust_size']}</b>. Structural edges add no extra financial cycle by construction.</p>",
            f"<div class=core>{core_links}</div>",
            "<h2>Research blocks by theme</h2>",
            hbar("On-site research blocks per atlas theme", [(t, c, str(c)) for t, c in themes], note="Best-fit grouping (a block can touch several themes); from the atlas theme index.", color=AC2),
            "<h2>Entities by sector</h2>",
            hbar("Graph nodes per sector (top 14)", [(k, v, str(v)) for k, v in sectors.most_common(14)], note="Sector is the node's primary bucket; 'other' = infrastructure / uncategorised.", color=AC),
            "<h2>Top cross-layer bridge connectors</h2>",
            f"<p class=sub>Nodes that bridge the most distinct sectors across both the financial and structural layers - the hubs whose removal would fragment the map most.</p>",
            hbar("Distinct neighbour-sectors bridged", [(c["node"].replace("_", " "), c["n_neighbor_sectors"], f'{c["n_neighbor_sectors"]} sec / deg {c["degree"]}') for c in conn], note="From the connector analysis (degree shown alongside).", color=AC2),
            "<h2>Edge grading mix</h2>",
            f"<p class=sub>How edges are hedged in their notes - an <b>indicative keyword tally</b> across all research-block edge notes (not an exact classification; many edges carry several tags or none).</p>",
            hbar("Edge-note grade keywords (count)", [(k, v, str(v)) for k, v in grade.most_common()], note="Keyword occurrences in edge notes; 'fact' dominates, with interpretation/contested/estimate labelled where claims are softer.", color=AC),
            ]
    if nsf:
        body += ["<h2>NVIDIA self-funding ratio</h2>",
                 f"<p class=sub>How much of NVIDIA's FY26 revenue (~${nsf.get('nvidia_fy26_revenue_usd',0)/1e9:.0f}B) is recycled into the circular core it also sells into - the vendor-financing concern, sized.</p>",
                 hbar("NVIDIA capital into the circular core vs its revenue", [
                     ("closed / funded", round(nsf.get("funded_ratio", 0) * 100, 1), f"{nsf.get('funded_ratio',0)*100:.1f}% (~${nsf.get('funded_usd',0)/1e9:.1f}B)"),
                     ("incl. headline LOIs", round(nsf.get("headline_ratio", 0) * 100, 1), f"{nsf.get('headline_ratio',0)*100:.1f}% (~${nsf.get('headline_usd',0)/1e9:.0f}B)")],
                     note="Share of NVIDIA FY26 revenue; closed-deal figure vs the headline incl. letters-of-intent that never closed.", color=AC2)]
    html = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Map health - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Stats", disclaimer=True) + "<main>" + "".join(body) + "</main></body></html>")
    open(os.path.join(DOCS, "mapstats.html"), "w").write(html)
    print(f"[build_mapstats] wrote mapstats.html: {A['num_nodes']} nodes, {n_blocks} blocks, {len(theme_blocks)} themes, core {A['core_scc_all_size']}/{A['core_scc_robust_size']}")

if __name__ == "__main__":
    build()
