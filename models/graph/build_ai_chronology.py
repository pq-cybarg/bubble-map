#!/usr/bin/env python3
"""build_ai_chronology.py - render docs/ai.html: the "AI" Tab.

A curated CHRONOLOGY of the AI field - lab focus-shifts + capability milestones, the
EA / Open-Philanthropy / safety-regulatory-arbitrage pathways, the open-weight /
abliterator / redistributor counter-ecosystem - plus a tech-history-traversal subsection
tracing the science across all contributing fields.

CENTRAL FRAMING (kept visible): "AI" is a broad field of many branches; LLMs (transformers,
2017+) are ONE currently-dominant branch, not AI itself.

Renders from the AI research/*.md blocks (single source of truth) with a compact markdown
renderer, so the Tab stays in sync with the graph-gated research. Self-contained page,
consistent with build_catalog / the rest of the static site.
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

# section order on the page: (research-basename, section-heading)
SECTIONS = [
    ("spec-ai-tech-history-traversal", "The true tech-history of AI (LLMs are one branch)"),
    ("spec-ai-capability-timeline", "AI capability timeline (2012-2026) - by branch"),
    ("spec-ai-lab-chronology-ea-pathways", "AI-lab chronology - focus, capability + the EA / safety-reg pathways"),
    ("spec-ai-safety-evals-ecosystem", "AI safety-evals ecosystem + the EA money map (incl. DataRepublican)"),
    ("spec-ai-oss-redistributor-chronology", "Open-weight AI, abliterators + redistributors"),
]

def _md2html(md):
    """Compact markdown -> HTML (headings, bold/italic/code, [[wikilinks]]->r-*.html, links,
    lists, tables, hr, blockquote). Mirrors build_dashboard's renderer, standalone."""
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    def wl(m):
        n = m.group(1)
        return f'<a href="r-{n}.html">{n}</a>' if os.path.exists(os.path.join(DOCS, f"r-{n}.html")) else n
    def inline(t):
        t = esc(t)
        t = re.sub(r'\[\[([^\]]+)\]\]', wl, t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<i>\1</i>', t)
        return t.replace("**", "")
    lines = md.split("\n"); out = []; i = 0
    bullet = lambda s: bool(re.match(r'^\s*[-*]\s', s))
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"): rows.append(lines[i]); i += 1
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            th = "".join(f"<th>{inline(c)}</th>" for c in cells(rows[0]))
            trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>" for r in rows[2:])
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"); continue
        if re.match(r'^#{1,6}\s', ln):
            lvl = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{lvl}>{inline(ln.lstrip('#').strip())}</h{lvl}>"); i += 1; continue
        if ln.strip() == "---": out.append("<hr>"); i += 1; continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"): buf.append(lines[i].lstrip(">").strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>"); continue
        if bullet(ln):
            buf = []
            while i < len(lines) and (bullet(lines[i]) or (lines[i].strip() == "" and i+1 < len(lines) and bullet(lines[i+1]))):
                if bullet(lines[i]): buf.append(f"<li>{inline(re.sub(r'^\\s*[-*]\\s','',lines[i]))}</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>"); continue
        if ln.strip() == "": i += 1; continue
        buf = [ln]; i += 1
        while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith(("#", "|", ">", "-", "*")):
            buf.append(lines[i]); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)

STYLE = ("body{background:#faf8f2;color:#1c1b19;font:18px/1.72 Georgia,'Iowan Old Style',"
    "'Palatino Linotype','Times New Roman',serif;margin:0;padding:0 0 60px}"
    "main{max-width:900px;margin:0 auto;padding:0 22px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:34px;margin:24px 0 4px}"
    "h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:38px;"
    "font-family:Georgia,serif;font-weight:600;font-size:25px}"
    "h3{color:#1f4e79;font-family:Georgia,serif;font-size:20px;margin-top:22px}a{color:#1f4e79}"
    ".muted{color:#6b665d;font-size:14px}p{margin:12px 0}code{background:#f0ebdd;padding:1px 5px;border-radius:4px;font-size:15px}"
    "blockquote{border-left:3px solid #c9bfa5;margin:12px 0;padding:4px 14px;color:#4a453c;font-style:italic}"
    "table{border-collapse:collapse;width:100%;margin:12px 0;font-size:15px}th,td{border:1px solid #e4ddcc;padding:6px 9px;text-align:left}"
    "th{background:#f4efe3}ul{margin:10px 0}li{margin:4px 0}"
    ".tax{background:#fffdf8;border:1px solid #c9bfa5;border-left:4px solid #7b2d26;border-radius:7px;"
    "padding:12px 16px;margin:16px 0;font-size:16px}"
    ".toc{background:#fffdf8;border:1px solid #e4ddcc;border-radius:8px;padding:10px 16px;margin:14px 0}"
    ".toc a{display:inline-block;margin:3px 10px 3px 0}")

def main():
    body = ['<h1>AI - chronology &amp; true tech-history</h1>',
        '<p class=muted>A curated chronology of the AI field - lab focus-shifts, capability milestones, '
        'the Effective-Altruism / Open-Philanthropy / safety-regulatory-arbitrage pathways, and the '
        'open-weight / abliterator / redistributor counter-ecosystem - plus a walk through the science '
        'that produced it. Rendered from graph-gated research blocks.</p>',
        '<div class=tax><b>Taxonomy, kept honest:</b> "AI" is a broad field of many branches - logic/search, '
        'statistical ML, reinforcement learning, computer vision, robotics, protein folding. '
        '<b>LLMs (transformer language models, 2017+) are one currently-dominant branch, not AI itself.</b> '
        'DeepMind\'s AlphaGo and AlphaFold are superhuman AI systems that are not LLMs.</div>']
    toc = ['<div class=toc><b>On this page:</b> ']
    sections = []; n_ok = 0
    for base, heading in SECTIONS:
        mdp = os.path.join(RES, base + ".md")
        if not os.path.exists(mdp):
            continue
        n_ok += 1
        anchor = base
        toc.append(f'<a href="#{anchor}">{heading}</a>')
        md = open(mdp, encoding="utf-8").read()
        # drop the file's own H1 (we provide the section H2)
        md = re.sub(r'^#\s.*\n', '', md, count=1)
        link = f'<a href="r-{base}.html">full research page &amp;raquo;</a>' if os.path.exists(os.path.join(DOCS, f"r-{base}.html")) else ''
        sections.append(f'<h2 id="{anchor}">{heading}</h2>'
                        f'<p class=muted>{link}</p>' + _md2html(md))
    toc.append('</div>')
    html = ("<!doctype html><html lang=en><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>AI - chronology &amp; tech-history - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("AI", disclaimer=True)
            + "<main>" + "".join(body) + "".join(toc) + "".join(sections)
            + "<p class=muted style='margin-top:40px;border-top:1px solid #e4ddcc;padding-top:12px'>"
            "Chronology + history are graded overlays (fact / interpretation per claim); "
            "see the linked research pages + <a href=methodology.html>methodology</a>.</p>"
            "</main></body></html>")
    open(os.path.join(DOCS, "ai.html"), "w").write(html)
    print(f"[build_ai_chronology] wrote ai.html: {n_ok} sections")

if __name__ == "__main__":
    main()
