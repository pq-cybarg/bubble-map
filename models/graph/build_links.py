#!/usr/bin/env python3
"""build_links.py - render docs/links.html: the Links tab.

Curated recommended reading from research/catalog-recommended-links.json
(outbound URLs + in-corpus r-*.html pages). Started with the right-to-repair /
Rossmann / FUTO / FULU / Consumer Rights Wiki cluster. Regenerable.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

SRC = os.path.join(RES, "catalog-recommended-links.json")

STYLE = (
    "body{background:#faf8f2;color:#1c1b19;font:18px/1.72 Georgia,'Iowan Old Style',"
    "'Palatino Linotype','Times New Roman',serif;margin:0;padding:0 0 60px}"
    "main{max-width:920px;margin:0 auto;padding:0 22px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:34px;margin:24px 0 4px}"
    "h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:34px;"
    "font-family:Georgia,serif;font-weight:600;font-size:24px}"
    "a{color:#1f4e79}.muted{color:#6b665d;font-size:14px}p{margin:12px 0}"
    ".card{background:#fffdf8;border:1px solid #e4ddcc;border-radius:7px;padding:11px 14px;margin:8px 0}"
    ".card b{color:#1c1b19}.notes{color:#4a453c;font-size:15px;margin:4px 0 0}"
    ".rel{font:13px -apple-system,Segoe UI,sans-serif;color:#6b665d;margin-top:6px}"
    ".rel a{margin-right:8px}"
    ".toc{background:#fffdf8;border:1px solid #e4ddcc;border-radius:8px;padding:10px 16px;margin:14px 0}"
    ".toc a{display:inline-block;margin:3px 10px 3px 0}"
    ".ext:after{content:' \\2197';font-size:12px;color:#8a8378}"
)

def esc(s):
    s = str(s or "")
    for a, b in [("\u2014", "-"), ("\u2013", "-"), ("\u2019", "'"), ("\u2018", "'"),
                 ("\u201c", '"'), ("\u201d", '"'), ("\u2026", "...")]:
        s = s.replace(a, b)
    s = s.encode("ascii", "ignore").decode("ascii")
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rel_links(item):
    stubs = item.get("related") or ([] if not item.get("stub") else [])
    bits = []
    for st in stubs:
        href = f"r-{st}.html"
        if os.path.exists(os.path.join(DOCS, href)):
            bits.append(f'<a href="{href}">{esc(st)}</a>')
    return ('<div class=rel>in corpus: ' + " ".join(bits) + "</div>") if bits else ""

def render_item(item, internal=False):
    stub = item.get("stub")
    if stub:
        href = f"r-{stub}.html"
        name = esc(item.get("name") or stub)
        title = f'<a href="{href}"><b>{name}</b></a>' if os.path.exists(os.path.join(DOCS, href)) else f"<b>{name}</b>"
        cls = "card"
    else:
        url = item.get("url") or ""
        name = esc(item.get("name") or url)
        title = f'<a class=ext href="{esc(url)}" rel="noopener"><b>{name}</b></a>'
        cls = "card"
    notes = esc(item.get("notes") or "")
    extra = rel_links(item)
    return f'<div class="{cls}">{title}<div class=notes>{notes}</div>{extra}</div>'

def main():
    d = json.load(open(SRC, encoding="utf-8"))
    groups = d.get("groups") or []
    n = sum(len(g.get("items") or []) for g in groups)
    toc = ['<div class=toc><b>On this page:</b> ']
    sections = []
    for g in groups:
        gid = esc(g.get("id") or "g")
        title = esc(g.get("title") or gid)
        toc.append(f'<a href="#{gid}">{title}</a>')
        cards = "".join(render_item(it, internal=bool(g.get("internal"))) for it in (g.get("items") or []))
        sections.append(f'<h2 id="{gid}">{title}</h2>' + cards)
    toc.append("</div>")
    intro = (
        "<h1>Recommended links</h1>"
        "<p class=muted>A living catalog of labs, leak archives, statutes, data sources, "
        "advocacy orgs, OEM/lobby pages, and in-corpus research. Started with right-to-repair; "
        "swept the rest of the graph for visitor-facing primaries (Citizen Lab, ATT&amp;CK, "
        "FRED/BIS/EDGAR, Chat Control/ID explainers). "
        f"{n} links in {len(groups)} groups. URL existence is fact; site framing is the publisher's. "
        "Advocacy wikis and manufacturer newsrooms both belong here, labeled.</p>"
        '<p>Spyware index: <a href="r-spec-uwu-apt-leads.html">UwU leads (not a source)</a>. '
        'Ownership: <a href="r-spec-rossmann-futo-ownership.html">Rossmann / FUTO / FULU</a>. '
        'Source JSON: <code>research/catalog-recommended-links.json</code>.</p>'
    )
    html = ("<!doctype html><html lang=en><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Links - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Links", disclaimer=True)
            + "<main>" + intro + "".join(toc) + "".join(sections)
            + "<p class=muted style='margin-top:40px;border-top:1px solid #e4ddcc;padding-top:12px'>"
            "Add groups/items in <code>research/catalog-recommended-links.json</code> and rebuild. "
            "See <a href=methodology.html>methodology</a>.</p>"
            "</main></body></html>")
    open(os.path.join(DOCS, "links.html"), "w").write(html)
    print(f"[build_links] wrote links.html: {n} items in {len(groups)} groups")

if __name__ == "__main__":
    main()
