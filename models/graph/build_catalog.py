#!/usr/bin/env python3
"""
build_catalog.py - render docs/catalog.html: a browsable index of the CATALOG layers
(academia, foundations, elite groups, billionaires, quiet money, university IP, threat actors)
plus pointers to the Persons dossiers + the Quantum sub-site.

Reads the relevant research/*.json (title + node/edge counts) and links each to its generated
r-<name>.html page. Self-contained page consistent with the rest of the static site.
"""
import json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

def esc(s):
    s = str(s or "")
    # normalize common unicode punctuation to ASCII (keep first-party output ASCII-clean)
    for a, b in [("\u2014", "-"), ("\u2013", "-"), ("\u2019", "'"), ("\u2018", "'"),
                 ("\u201c", '"'), ("\u201d", '"'), ("\u2026", "..."), ("\u2192", "->")]:
        s = s.replace(a, b)
    s = s.encode("ascii", "ignore").decode("ascii")
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def block(fn):
    """Return (title, nodes, edges) for a research json path; tolerant of schema variants."""
    try:
        d = json.load(open(fn))
    except Exception:
        return None
    title = (d.get("metadata", {}) or {}).get("title") or d.get("title") or os.path.basename(fn)
    nodes = len(d.get("nodes") or [])
    edges = len(d.get("edges") or [])
    return (title, nodes, edges, os.path.basename(fn)[:-5])

# curated groupings (basename without .json). Order = display order.
GROUPS = [
    ("Academia & IP", [
        "catalog-academia-core", "catalog-academia-abroad", "catalog-university-ip"]),
    ("Money & power", [
        "catalog-nonprofits-foundations", "catalog-elite-groups", "catalog-billionaires",
        "catalog-quiet-money", "catalog-quiet-money-2", "catalog-quiet-money-3",
        "catalog-crosslink-pass"]),
    ("Threat actors & cyber", [
        "spec-state-apt-catalog", "spec-ransomware-ecrime-catalog", "spec-hacktivist-catalog",
        "spec-spyware-vendor-catalog", "spec-citizen-lab", "spec-av-edr-subversion-doubleagent",
        "spec-cyber-notable-individuals", "spec-cyber-notable-individuals-2",
        "spec-iloveyou-worm", "spec-shadow-brokers-eternalblue", "spec-finfisher-finspy-spyware",
        "spec-shai-hulud-npm-worm", "spec-msnightmare-disclosure", "spec-inqtel-portfolio",
        "spec-palantir-surveillance", "spec-niantic-geospatial"]),
    ("Quantum & PQC", [
        "spec-ecdsa-nonce-failure-tracker", "macro-crqc-quantum-landscape", "macro-pqc-chips",
        "spec-defense-primes-pqc", "spec-quantum-computing-competitive-landscape",
        "spec-trusted-foundry-secure-microelectronics"]),
]

STYLE = ("body{background:#faf8f2;color:#1c1b19;font:18px/1.72 Georgia,'Iowan Old Style',"
    "'Palatino Linotype','Times New Roman',serif;margin:0;padding:0 0 60px}"
    "main{max-width:900px;margin:0 auto;padding:0 22px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:34px;margin:26px 0 4px}"
    "h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:34px;"
    "font-family:Georgia,serif;font-weight:600;font-size:24px}a{color:#1f4e79}"
    ".muted{color:#6b665d;font-size:14px}p{margin:12px 0}"
    ".card{background:#fffdf8;border:1px solid #e4ddcc;border-radius:7px;padding:11px 14px;margin:8px 0;"
    "display:flex;justify-content:space-between;align-items:baseline;gap:12px}"
    ".card b{color:#1c1b19}.count{color:#6b665d;font:13px -apple-system,Segoe UI,sans-serif;white-space:nowrap}"
    ".hero{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0}"
    ".stat{background:#fffdf8;border:1px solid #e4ddcc;border-radius:8px;padding:10px 16px;text-align:center}"
    ".stat b{display:block;font-size:26px;color:#7b2d26}.stat span{font-size:12.5px;color:#6b665d}")

def main():
    total_n = total_e = total_blocks = 0
    body = ["<h1>Catalogs</h1>",
            "<p>Cross-cutting reference layers - the people, institutions, money, and threat actors "
            "woven through the map. Each block links to its full research page; individuals link to the "
            "<a href=persons.html>Persons</a> dossiers, and the quantum material has its own "
            "<a href=quantum.html>sub-site</a>.</p>"]
    sections = []
    for gname, names in GROUPS:
        rows = []
        for nm in names:
            fn = os.path.join(RES, nm + ".json")
            b = block(fn)
            if not b:
                continue
            title, nodes, edges, base = b
            total_n += nodes; total_e += edges; total_blocks += 1
            rows.append(f'<div class=card><span><a href="r-{esc(base)}.html"><b>{esc(title)}</b></a></span>'
                        f'<span class=count>{nodes} nodes &middot; {edges} edges</span></div>')
        if rows:
            sections.append(f"<h2>{esc(gname)}</h2>" + "".join(rows))
    hero = (f'<div class=hero><div class=stat><b>{total_blocks}</b><span>catalog blocks</span></div>'
            f'<div class=stat><b>{total_n}</b><span>catalog nodes</span></div>'
            f'<div class=stat><b>{total_e}</b><span>catalog edges</span></div></div>')
    html = ("<!doctype html><html><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Catalogs - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Catalogs")
            + "<main>" + body[0] + body[1] + hero + "".join(sections)
            + "<p class=muted style='margin-top:40px;border-top:1px solid #e4ddcc;padding-top:12px'>"
            "Catalog layers are graded overlays (fact / contested / interpretation per edge); "
            "documented ties, not asserted intent. See <a href=methodology.html>methodology</a>.</p>"
            "</main></body></html>")
    open(os.path.join(DOCS, "catalog.html"), "w").write(html)
    print(f"[build_catalog] wrote catalog.html: {total_blocks} blocks, {total_n} nodes, {total_e} edges")

if __name__ == "__main__":
    main()
