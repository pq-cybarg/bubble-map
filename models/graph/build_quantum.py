#!/usr/bin/env python3
"""
build_quantum.py - render the dedicated QUANTUM sub-site from data/quantum.json (curated + graded)
and data/quantum_feed.json (machine-collected, UNVERIFIED live feed written by quantum_fetch.py).

Emits under docs/:
  quantum.html                  - hub (overview, threat, aggregates, links to sub-pages, feed teaser)
  quantum-hardware.html         - qubit modalities, best-known designs, fidelity leaderboard
  quantum-error-correction.html - codes, thresholds/overhead, milestones
  quantum-pqc.html              - post-quantum crypto by subarea + NIST standards
  quantum-compliance.html       - PQC mandates/timelines/restrictions by region
  quantum-feed.html             - the live UNVERIFIED tracker feed

Self-contained pages (inlined data), consistent with the rest of the static GitHub Pages site.
Grades are color-badged; nothing on the feed page is presented as fact.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

Q = json.load(open(os.path.join(DATA, "quantum.json")))
try:
    FEED = json.load(open(os.path.join(DATA, "quantum_feed.json")))
except Exception:
    FEED = {"meta": {}, "items": []}

GRADE_COLOR = {"fact": "#1f7a4d", "demo": "#b8860b", "target": "#1f4e79",
               "estimate": "#7a5b1f", "interp": "#7b2d26", "": "#6b665d"}

def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def badge(g):
    if not g:
        return ""
    c = GRADE_COLOR.get(g, "#6b665d")
    return (f'<span style="display:inline-block;font:600 10.5px/1.4 -apple-system,Segoe UI,sans-serif;'
            f'color:#fff;background:{c};border-radius:4px;padding:1px 6px;margin-left:6px;'
            f'text-transform:uppercase;letter-spacing:.03em">{esc(g)}</span>')

STYLE = ("body{background:#faf8f2;color:#1c1b19;font:18px/1.72 Georgia,'Iowan Old Style',"
    "'Palatino Linotype','Times New Roman',serif;margin:0;padding:0 0 60px}"
    "main{max-width:900px;margin:0 auto;padding:0 22px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:34px;margin:26px 0 4px}"
    "h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:34px;"
    "font-family:Georgia,serif;font-weight:600;font-size:24px}"
    "h3{font-family:Georgia,serif;font-weight:600;font-size:19px;margin:22px 0 4px;color:#33312c}"
    "a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:14px}"
    ".b{background:#fffdf8;border:1px solid #e4ddcc;border-radius:7px;padding:13px 15px;margin:9px 0}"
    ".b b{color:#1c1b19}.muted{color:#6b665d;font-size:14px}p{margin:12px 0}"
    "table{border-collapse:separate;border-spacing:0;width:100%;margin:16px 0;font-size:15px;"
    "font-family:-apple-system,Segoe UI,Roboto,sans-serif;border:1px solid #e4ddcc;border-radius:8px;overflow:hidden}"
    "th,td{border-bottom:1px solid #e4ddcc;padding:9px 13px;text-align:left;vertical-align:top;line-height:1.5}"
    "td+td,th+th{border-left:1px solid #e4ddcc}tr:last-child td{border-bottom:none}"
    "thead th{background:#f3eedf}tbody tr:nth-child(even){background:#fbf9f3}"
    ".subnav{background:#fffdf8;border-bottom:1px solid #e4ddcc;text-align:center;padding:8px 12px;"
    "font:13.5px/1.6 -apple-system,Segoe UI,Roboto,sans-serif}"
    ".subnav a{margin:0 8px;text-decoration:none;white-space:nowrap}"
    ".warn{background:#fbeee6;border:1px solid #e4ddcc;border-left:4px solid #b8860b;border-radius:7px;"
    "padding:12px 15px;margin:14px 0;color:#5a4a2a;font-size:15px}")

SUBTABS = [("quantum.html", "Overview"), ("quantum-hardware.html", "Hardware"),
           ("quantum-error-correction.html", "Error correction"), ("quantum-pqc.html", "PQC"),
           ("quantum-compliance.html", "Compliance"), ("quantum-feed.html", "Live feed")]

def subnav(active):
    def a(h, t):
        cur = (h == active)
        return (f'<a href="{h}" style="color:{"#7b2d26" if cur else "#1f4e79"};'
                f'font-weight:{700 if cur else 400}">{t}</a>')
    return '<div class=subnav>' + "".join(a(h, t) for h, t in SUBTABS) + '</div>'

def page(fname, title, body):
    html = ("<!doctype html><html><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{esc(title)} - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Quantum") + subnav(fname)
            + "<main>" + body
            + "<p class=muted style='margin-top:40px;border-top:1px solid #e4ddcc;padding-top:12px'>"
            "Curated + graded knowledge base, aggregated from the research corpus and refreshed by a "
            "scheduled tracker. Grades: "
            + " ".join(f"{badge(g)}" for g in ["fact", "demo", "target", "estimate", "interp"])
            + ". The live feed is machine-collected and unverified. contact resistant@tuta.com</p>"
            "</main></body></html>")
    open(os.path.join(DOCS, fname), "w").write(html)

# ---------------------------------------------------------------- Overview / hub
def build_overview():
    m = Q["meta"]; t = Q["threat"]
    aggs = "".join(
        f'<div class=b><a href="r-{esc(a["file"])}.html"><b>{esc(a["title"])}</b></a>'
        f' <span class=muted>{esc(a["note"])}</span></div>' for a in Q["aggregates"])
    feed_n = len(FEED.get("items", [])); lf = (FEED.get("meta") or {}).get("last_fetch") or "not yet run"
    body = (f"<h1>{esc(m['title'])}</h1><p>{esc(m['subtitle'])}</p>"
            f"<p class=muted>As of {esc(m['as_of'])}. {esc(m['honesty'])}</p>"
            "<h2>The threat, briefly</h2>"
            f"<div class=b><b>CRQC.</b> {esc(t['crqc'])}</div>"
            f"<div class=b><b>Timelines (estimate).</b> {esc(t['estimates'])}</div>"
            f"<div class=b><b>Harvest-now, decrypt-later.</b> {esc(t['harvest_now'])}</div>"
            f"<div class=b><b>The classical bridge.</b> {esc(t['classical_bridge'])}</div>"
            "<h2>Sections</h2>"
            "<div class=b><a href=quantum-hardware.html><b>Hardware &rarr;</b></a> "
            "<span class=muted>Six qubit modalities, best-known designs, fidelity leaderboard.</span></div>"
            "<div class=b><a href=quantum-error-correction.html><b>Error correction &rarr;</b></a> "
            "<span class=muted>Codes, thresholds/overhead, below-threshold milestones.</span></div>"
            "<div class=b><a href=quantum-pqc.html><b>Post-quantum cryptography &rarr;</b></a> "
            "<span class=muted>PQC by subarea + NIST standards.</span></div>"
            "<div class=b><a href=quantum-compliance.html><b>Compliance &rarr;</b></a> "
            "<span class=muted>Mandates, timelines, restrictions by region.</span></div>"
            "<div class=b><a href=quantum-feed.html><b>Live feed &rarr;</b></a> "
            f"<span class=muted>{feed_n} machine-collected items (unverified). Last fetch: {esc(lf)}.</span></div>"
            "<h2>From the research corpus</h2>" + aggs)
    page("quantum.html", "Quantum tracker", body)

# ---------------------------------------------------------------- Hardware
def build_hardware():
    h = Q["hardware"]
    mods = ""
    for mo in h["modalities"]:
        rows = "".join(
            f"<tr><td>{esc(b['who'])}</td><td>{esc(b['metric'])}</td><td>{esc(b['value'])}</td>"
            f"<td>{esc(b['date'])}{badge(b.get('grade'))}</td></tr>" for b in mo["best_known"])
        mods += (f"<h3>{esc(mo['name'])}</h3>"
                 f"<p>{esc(mo['principle'])}</p>"
                 f"<div class=b><b>Leaders:</b> {esc(', '.join(mo['leaders']))}<br>"
                 f"<b>Strengths:</b> {esc(mo['strengths'])}<br>"
                 f"<b>Weaknesses:</b> {esc(mo['weaknesses'])}</div>"
                 "<table><thead><tr><th>Who</th><th>Metric</th><th>Best known</th><th>Date</th></tr></thead>"
                 f"<tbody>{rows}</tbody></table>"
                 f"<p class=muted><b>Roadmap:</b> {esc(mo['roadmap'])}</p>")
    fl = h["fidelity_leaderboard"]
    flrows = "".join(f"<tr><td>{esc(r['who'])}</td><td>{esc(r['value'])}</td><td>{esc(r['modality'])}</td></tr>"
                     for r in fl["rows"])
    body = ("<h1>Quantum hardware</h1>" + f"<p>{esc(h['intro'])}</p>" + mods
            + f"<h2>2Q gate-fidelity leaderboard <span class=muted>({esc(fl['date'])})</span></h2>"
            f"<p class=muted>{esc(fl['note'])}</p>"
            "<table><thead><tr><th>Who</th><th>Fidelity</th><th>Modality</th></tr></thead>"
            f"<tbody>{flrows}</tbody></table>")
    page("quantum-hardware.html", "Quantum hardware", body)

# ---------------------------------------------------------------- Error correction
def build_ec():
    e = Q["error_correction"]
    concepts = "".join(f"<div class=b><b>{esc(c['term'])}.</b> {esc(c['def'])}</div>" for c in e["concepts"])
    coderows = "".join(
        f"<tr><td><b>{esc(c['name'])}</b></td><td>{esc(c['family'])}</td><td>{esc(c['threshold'])}</td>"
        f"<td>{esc(c['overhead'])}</td><td>{esc(c['status'])}</td></tr>" for c in e["codes"])
    milrows = "".join(
        f"<tr><td>{esc(m['date'])}</td><td>{esc(m['who'])}</td><td>{esc(m['claim'])}{badge(m.get('grade'))}</td>"
        f"<td class=muted>{esc(m['source'])}</td></tr>" for m in e["milestones"])
    body = ("<h1>Quantum error correction</h1>" + f"<p>{esc(e['intro'])}</p>"
            "<h2>Concepts</h2>" + concepts
            + "<h2>Code families</h2>"
            "<table><thead><tr><th>Code</th><th>Family</th><th>Threshold</th><th>Overhead</th><th>Status</th></tr></thead>"
            f"<tbody>{coderows}</tbody></table>"
            "<h2>Milestones</h2>"
            "<table><thead><tr><th>Date</th><th>Who</th><th>Claim</th><th>Source</th></tr></thead>"
            f"<tbody>{milrows}</tbody></table>")
    page("quantum-error-correction.html", "Quantum error correction", body)

# ---------------------------------------------------------------- PQC
def build_pqc():
    p = Q["pqc"]
    subs = ""
    for s in p["subareas"]:
        subs += (f"<h3>{esc(s['family'])}</h3>"
                 f"<div class=b><b>Schemes:</b> {esc(', '.join(s['schemes']))}<br>"
                 f"<b>Status:</b> {esc(s['status'])}<br>"
                 f"<b>Note:</b> {esc(s['note'])}</div>")
    strows = "".join(
        f"<tr><td><code>{esc(x['id'])}</code></td><td>{esc(x['name'])}</td><td>{esc(x['date'])}</td>"
        f"<td class=muted>{esc(x['note'])}</td></tr>" for x in p["standards"])
    body = ("<h1>Post-quantum cryptography</h1>" + f"<p>{esc(p['intro'])}</p>"
            "<h2>By subarea</h2>" + subs
            + "<h2>NIST standards</h2>"
            "<table><thead><tr><th>ID</th><th>Name</th><th>Date</th><th>Note</th></tr></thead>"
            f"<tbody>{strows}</tbody></table>")
    page("quantum-pqc.html", "Post-quantum cryptography", body)

# ---------------------------------------------------------------- Compliance
def build_compliance():
    c = Q["compliance"]
    rows = "".join(
        f"<tr><td><b>{esc(r['region'])}</b></td><td>{esc(r['authority'])}</td><td>{esc(r['mandate'])}</td>"
        f"<td class=muted>{esc(r['note'])}{badge(r.get('grade'))}</td></tr>" for r in c["regions"])
    body = ("<h1>PQC compliance &amp; regional mandates</h1>" + f"<p>{esc(c['intro'])}</p>"
            "<table><thead><tr><th>Region</th><th>Authority</th><th>Mandate / timeline</th><th>Notes</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")
    page("quantum-compliance.html", "PQC compliance", body)

# ---------------------------------------------------------------- Live feed (UNVERIFIED)
def build_feed():
    fm = FEED.get("meta", {}); items = FEED.get("items", [])
    warn = ("<div class=warn><b>Unverified, machine-collected.</b> "
            + esc(fm.get("warning", "Auto-collected from public sources; not verified or graded."))
            + f" Last fetch: <b>{esc(fm.get('last_fetch') or 'not yet run')}</b>.</div>")
    srcs = ""
    if fm.get("sources"):
        srcs = ("<h2>Sources polled</h2><table><thead><tr><th>Source</th><th>Kind</th><th>Note</th></tr></thead><tbody>"
                + "".join(f"<tr><td>{esc(s['name'])}</td><td>{esc(s['kind'])}</td><td class=muted>{esc(s['note'])}</td></tr>"
                          for s in fm["sources"]) + "</tbody></table>")
    if items:
        # newest first if a date is present
        def keyf(it):
            return it.get("date") or it.get("fetched") or ""
        rows = "".join(
            f"<tr><td>{esc(it.get('date') or it.get('fetched') or '')}</td>"
            f"<td>{esc(it.get('source',''))}</td>"
            f"<td><a href=\"{esc(it.get('url',''))}\" rel=noopener>{esc(it.get('title','(untitled)'))}</a>"
            + (f"<br><span class=muted>{esc(it.get('summary',''))}</span>" if it.get('summary') else "")
            + "</td></tr>"
            for it in sorted(items, key=keyf, reverse=True))
        table = ("<h2>Feed</h2><table><thead><tr><th>Date</th><th>Source</th><th>Item</th></tr></thead>"
                 f"<tbody>{rows}</tbody></table>")
    else:
        table = ("<h2>Feed</h2><div class=b class=muted>No items yet. The scheduled tracker "
                 "(<code>.github/workflows/quantum-tracker.yml</code>) populates this file and opens a "
                 "pull request for review before anything is merged.</div>")
    body = "<h1>Quantum live feed</h1>" + warn + table + srcs
    page("quantum-feed.html", "Quantum live feed", body)

def main():
    for f in (build_overview, build_hardware, build_ec, build_pqc, build_compliance, build_feed):
        f()
    print(f"[build_quantum] wrote {len(SUBTABS)} pages; feed items={len(FEED.get('items', []))}")

if __name__ == "__main__":
    main()
