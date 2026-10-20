#!/usr/bin/env python3
"""build_timeline.py - render docs/timeline.html: a chronological view of the corpus (#108-style).

Pulls every STRUCTURED date in the research blocks - edge/chain-edge `date` fields and block
`event_date`s - and lays them out as a year-grouped timeline, each event linking to its research
page and the entities involved. Dates are taken only from recorded fields (no parsing of prose, no
fabrication). A per-year count histogram sits on top. House palette; static, server-rendered.
Writes docs/timeline.html. Regenerable; run from new-research.sh.
"""
import json, os, re, glob
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

INK="#1c1b19"; MUT="#6b665d"; LINE="#e4ddcc"; PAPER="#fffdf8"; AC="#7b2d26"; AC2="#1f4e79"
esc = lambda s: (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
rpages = set(os.path.basename(p)[2:-5] for p in glob.glob(os.path.join(DOCS, "r-*.html")))
DATE = re.compile(r"((?:19|20)\d{2})(?:-(\d{2}))?(?:-(\d{2}))?")

def short(s, n=150):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return (s[:n] + "...") if len(s) > n else s

def norm(dt):
    m = DATE.match(str(dt or "").strip())
    if not m: return None
    y, mo, da = m.group(1), m.group(2) or "00", m.group(3) or "00"
    return (f"{y}-{mo}-{da}", int(y))

events = []  # (sortkey, display-date, year, html-desc, stub)
seen = set()
for fn in sorted(glob.glob(os.path.join(RES, "*.json"))):
    stub = os.path.basename(fn)[:-5]
    try: d = json.load(open(fn))
    except Exception: continue
    title = d.get("title") or (d.get("metadata") or {}).get("title") or stub
    ed = norm(d.get("event_date"))
    if ed:
        key = (ed[0], stub, "block")
        if key not in seen:
            seen.add(key); events.append((ed[0], ed[0], ed[1], f"<b>{esc(short(title,110))}</b> <span class=k>block</span>", stub))
    for e in (d.get("edges") or []) + (d.get("chain_edges") or []):
        nd = norm(e.get("date"))
        if not nd: continue
        f_, t_ = e.get("from"), e.get("to")
        inst = e.get("instrument", "")
        note = short(e.get("notes") or e.get("note") or e.get("raw_instrument") or "", 150)
        key = (nd[0], f_, t_, inst)
        if key in seen: continue
        seen.add(key)
        link = f'<a href="bubblemap.html#node={esc(f_)}">{esc(str(f_).replace("_"," "))}</a> &rarr; <a href="bubblemap.html#node={esc(t_)}">{esc(str(t_).replace("_"," "))}</a>'
        desc = f'{link} <span class=pill>{esc(inst)}</span>' + (f'<div class=nt>{esc(note)}</div>' if note else "")
        events.append((nd[0], nd[0], nd[1], desc, stub))
events.sort(key=lambda x: x[0], reverse=True)   # newest first
by_year = defaultdict(list)
for sk, disp, y, desc, stub in events: by_year[y].append((disp, desc, stub))
years = sorted(by_year, reverse=True)
yr_counts = [(y, len(by_year[y])) for y in sorted(by_year)]

def hist():
    if not yr_counts: return ""
    W = 720; bw = max(10, (W - 60) // max(1, len(yr_counts))); H = 150; base = 110; hi = max(c for _, c in yr_counts) or 1
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:7px;margin:8px 0">']
    s.append(f'<text x="14" y="20" font-size="13" font-weight="700" fill="{INK}" font-family="Georgia,serif">Dated events per year</text>')
    for i, (y, c) in enumerate(yr_counts):
        x = 40 + i * bw; h = (base - 24) * c / hi
        s.append(f'<rect x="{x}" y="{base-h:.0f}" width="{bw-4}" height="{h:.0f}" rx="2" fill="{AC2}"/>')
        s.append(f'<text x="{x+(bw-4)/2:.0f}" y="{base+13}" font-size="9" fill="{MUT}" text-anchor="middle" font-family="sans-serif" transform="rotate(0)">{y}</text>')
        s.append(f'<text x="{x+(bw-4)/2:.0f}" y="{base-h-3:.0f}" font-size="8.5" fill="{INK}" text-anchor="middle" font-family="sans-serif">{c}</text>')
    s.append("</svg>"); return "".join(s)

STYLE = (f"body{{background:#faf8f2;color:{INK};font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 50px}}"
         "main{max-width:880px;margin:0 auto;padding:0 18px}h1{font-family:Georgia,serif;font-weight:600;font-size:30px;margin:22px 0 2px}"
         f".sub{{color:{MUT};font-size:14px;margin:0 0 10px}}a{{color:{AC2}}}"
         f"h2{{color:{AC};font-family:Georgia,serif;font-size:22px;margin:24px 0 2px;border-bottom:1px solid {LINE};padding-bottom:4px}}"
         ".chips{margin:8px 0}.chip{display:inline-block;font-size:12.5px;color:#1f4e79;background:#fffdf8;border:1px solid #e4ddcc;border-radius:13px;padding:3px 10px;margin:2px 5px 2px 0}"
         f".ev{{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #efe9da}}.ev .dt{{flex:0 0 92px;color:{AC};font-weight:600;font-size:13px;font-variant-numeric:tabular-nums}}"
         f".ev .bd{{flex:1;font-size:14px}}.ev .nt{{color:{MUT};font-size:12.5px;margin-top:2px}}"
         ".pill{display:inline-block;font-size:10.5px;padding:1px 6px;border-radius:9px;background:#efe9da;color:#4a453c;margin-left:4px}"
         ".k{font-size:10.5px;color:#8a8378}.src{font-size:11px;color:#8a8378;margin-left:6px}")

def build():
    chips = "".join(f'<a class=chip href="#y{y}">{y} ({len(by_year[y])})</a>' for y in years)
    secs = []
    for y in years:
        rows = "".join(f'<div class=ev><div class=dt>{esc(disp)}</div><div class=bd>{desc}'
                       + (f'<a class=src href="r-{esc(stub)}.html">{esc(stub)}</a>' if stub in rpages else f'<span class=src>{esc(stub)}</span>')
                       + "</div></div>" for disp, desc, stub in by_year[y])
        secs.append(f'<h2 id="y{y}">{y} <span class=sub style="font-weight:400">({len(by_year[y])} events)</span></h2>{rows}')
    html = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Timeline - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Timeline", disclaimer=True) + "<main><h1>Timeline</h1>"
            + f"<p class=sub>Every <b>dated</b> event in the corpus - {len(events)} items drawn only from recorded edge/block date fields (no prose parsing), newest first. Each links to its research block and the entities involved.</p>"
            + hist() + f"<div class=chips>{chips}</div>" + "".join(secs) + "</main></body></html>")
    open(os.path.join(DOCS, "timeline.html"), "w").write(html)
    print(f"[build_timeline] wrote timeline.html: {len(events)} dated events across {len(years)} years")

if __name__ == "__main__":
    build()
