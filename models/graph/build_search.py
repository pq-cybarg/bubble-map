#!/usr/bin/env python3
"""build_search.py - render docs/search.html: a unified site search (#108-style feature).

One box, instant client-side results across three indexes, built here and lazy-fetched:
  * research blocks  - title + a source/summary snippet + theme (links to r-<stub>.html)
  * graph entities   - id/label + sector + degree (links to bubblemap.html#node=<id>)
  * people           - name + role + BLUF snippet (links to persons.html#p-<slug>)
No backend, no hallucination: it only finds and links what exists. Writes docs/search.html
(light shell) + docs/search-index.json (fetched on load). Regenerable; run from new-research.sh.
"""
import json, os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "docs")
import nav as _nav

def clean(s, n=320):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return (s[:n] + "...") if len(s) > n else s

# theme per block (from the atlas theme index)
theme_of = {}
try:
    tb = json.load(open(os.path.join(DOCS, "theme-blocks.json")))
    for tid, arr in tb.items():
        for e in arr: theme_of[e.get("b")] = tid
except Exception: pass

rpages = set(os.path.basename(p)[2:-5] for p in glob.glob(os.path.join(DOCS, "r-*.html")))

# ---- blocks ----
BLOCKS = []
for fn in sorted(glob.glob(os.path.join(RES, "*.json"))):
    stub = os.path.basename(fn)[:-5]
    if stub not in rpages: continue
    try: d = json.load(open(fn))
    except Exception: continue
    md = d if isinstance(d, dict) else {}
    meta = md.get("metadata") or {}
    title = md.get("title") or meta.get("title") or stub
    snip = md.get("source") or md.get("summary") or md.get("description") or meta.get("frame") or meta.get("provenance") or ""
    BLOCKS.append({"s": stub, "t": clean(title, 160), "x": clean(snip, 300), "th": theme_of.get(stub, "")})

# ---- entities ----
G = json.load(open(os.path.join(ROOT, "data", "graph.json")))
deg = {}
for e in G["edges"]:
    deg[e["from"]] = deg.get(e["from"], 0) + 1; deg[e["to"]] = deg.get(e["to"], 0) + 1
ENTS = []
for nid, m in G["entities"].items():
    ENTS.append({"id": nid, "l": nid.replace("_", " "), "sec": (m or {}).get("sector", "other"), "d": deg.get(nid, 0)})

# ---- people ----
PPL = []
try:
    for p in json.load(open(os.path.join(ROOT, "data", "persons.json")))["persons"]:
        nm = p.get("name", "")
        if not nm: continue
        slug = "p-" + re.sub(r"[^a-z0-9]+", "-", nm.lower()).strip("-")
        PPL.append({"n": nm, "r": clean(p.get("role", ""), 90), "x": clean(p.get("bluf", ""), 180), "sl": slug})
except Exception: pass

IDX = {"blocks": BLOCKS, "ents": ENTS, "ppl": PPL}

STYLE = (
    "body{background:#faf8f2;color:#1c1b19;font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 50px}"
    "main{max-width:880px;margin:0 auto;padding:0 18px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:30px;margin:22px 0 2px}"
    ".sub{color:#6b665d;font-size:14px;margin:0 0 14px}"
    "a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:13px}"
    "#q{width:100%;box-sizing:border-box;padding:13px 15px;font-size:17px;border:1px solid #c9bfa5;border-radius:9px;font-family:inherit}"
    ".tabs{margin:12px 0 4px}.tab{display:inline-block;font-size:13px;padding:5px 11px;margin:0 6px 4px 0;border:1px solid #e4ddcc;border-radius:14px;cursor:pointer;color:#4a453c;background:#fffdf8}"
    ".tab.on{background:#1f4e79;color:#fff;border-color:#1f4e79}"
    "h2{color:#7b2d26;font-family:Georgia,serif;font-size:19px;margin:22px 0 6px;border-bottom:1px solid #e4ddcc;padding-bottom:4px}"
    ".hit{background:#fffdf8;border:1px solid #e4ddcc;border-radius:8px;padding:10px 13px;margin:7px 0}"
    ".hit .ti{font-weight:600}.hit .mt{font-size:12px;color:#8a8378;margin-left:6px}"
    ".hit .sn{font-size:13.5px;color:#4a453c;margin-top:3px}"
    "mark{background:#f3e08a;padding:0 1px}.pill{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;background:#efe9da;color:#4a453c;margin-left:5px}"
    ".muted{color:#6b665d;font-size:13px}"
)

JS = r"""
let IDX=null; const EL=id=>document.getElementById(id);
const esc=s=>(s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
let TYPE='all';
function toks(q){return q.toLowerCase().split(/[^a-z0-9]+/).filter(x=>x.length>1);}
function hl(s,ts){ let o=esc(s); ts.forEach(t=>{ o=o.replace(new RegExp('('+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>'); }); return o; }
function scoreText(hay, ts){ hay=hay.toLowerCase(); let sc=0; ts.forEach(t=>{ if(hay.includes(t)) sc+= hay.startsWith(t)?3:1; }); return sc; }
function run(){
  const q=EL('q').value.trim(); const ts=toks(q); const out=EL('out');
  if(!q){ out.innerHTML='<p class=muted>Type to search research blocks, entities, and people across the whole corpus.</p>'; return; }
  if(!ts.length){ out.innerHTML=''; return; }
  const show={all:1,blocks:TYPE==='all'||TYPE==='blocks',ents:TYPE==='all'||TYPE==='ents',ppl:TYPE==='all'||TYPE==='ppl'};
  let html='';
  if(show.blocks){
    let r=IDX.blocks.map(b=>[b, scoreText(b.t,ts)*4+scoreText(b.x,ts)+scoreText(b.s,ts)*2]).filter(x=>x[1]>0).sort((a,b)=>b[1]-a[1]).slice(0,40);
    if(r.length){ html+=`<h2>Research blocks <span class=muted>(${r.length})</span></h2>`+r.map(([b])=>
      `<div class=hit><div><a class=ti href="r-${esc(b.s)}.html">${hl(b.t,ts)}</a>${b.th?`<span class=pill>${esc(b.th)}</span>`:''}</div><div class=sn>${hl(b.x,ts)}</div></div>`).join(''); }
  }
  if(show.ents){
    let r=IDX.ents.map(e=>[e, scoreText(e.l,ts)*4+scoreText(e.sec,ts)]).filter(x=>x[1]>0).sort((a,b)=>b[1]-a[1]||b[0].d-a[0].d).slice(0,40);
    if(r.length){ html+=`<h2>Entities <span class=muted>(${r.length})</span></h2>`+r.map(([e])=>
      `<div class=hit><a class=ti href="bubblemap.html#node=${encodeURIComponent(e.id)}">${hl(e.l,ts)}</a><span class=pill>${esc(e.sec)}</span><span class=mt>degree ${e.d}</span> &middot; <a class=mt href="guide.html">ask the guide</a></div>`).join(''); }
  }
  if(show.ppl){
    let r=IDX.ppl.map(p=>[p, scoreText(p.n,ts)*4+scoreText(p.r,ts)+scoreText(p.x,ts)]).filter(x=>x[1]>0).sort((a,b)=>b[1]-a[1]).slice(0,40);
    if(r.length){ html+=`<h2>People <span class=muted>(${r.length})</span></h2>`+r.map(([p])=>
      `<div class=hit><div><a class=ti href="persons.html#${esc(p.sl)}">${hl(p.n,ts)}</a><span class=mt>${hl(p.r,ts)}</span></div><div class=sn>${hl(p.x,ts)}</div></div>`).join(''); }
  }
  out.innerHTML = html || '<p class=muted>No matches. Try a different term, or <a href="guide.html">ask the Guide</a> about an entity or connection.</p>';
}
window.addEventListener('DOMContentLoaded',async()=>{
  EL('out').innerHTML='<p class=muted>Loading search index&hellip;</p>';
  try{ const r=await fetch('search-index.json'); IDX=await r.json(); }
  catch(e){ EL('out').innerHTML='<p class=muted>Could not load the search index ('+esc(e.message)+').</p>'; return; }
  EL('q').addEventListener('input',run);
  document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{ document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); t.classList.add('on'); TYPE=t.dataset.t; run(); });
  const p=new URLSearchParams(location.search).get('q'); if(p){ EL('q').value=p; } EL('q').focus(); run();
});
"""

def build():
    tabs = ('<div class=tabs><span class="tab on" data-t=all>All</span>'
            f'<span class=tab data-t=blocks>Blocks ({len(BLOCKS)})</span>'
            f'<span class=tab data-t=ents>Entities ({len(ENTS)})</span>'
            f'<span class=tab data-t=ppl>People ({len(PPL)})</span></div>')
    json.dump(IDX, open(os.path.join(DOCS, "search-index.json"), "w"), separators=(",", ":"), ensure_ascii=False)
    html = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Search - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Search", disclaimer=True)
            + "<main><h1>Search</h1>"
            + f"<p class=sub>One box across the whole corpus - {len(BLOCKS)} research blocks, {len(ENTS)} entities, {len(PPL)} people. Results link to the research pages, the bubble map, and the persons dossiers. Everything is found, nothing is generated.</p>"
            + "<input id=q type=text placeholder='Search blocks, entities, people...' autocomplete=off>"
            + tabs + "<div id=out></div>"
            + f"<script>{JS}</script></main></body></html>")
    open(os.path.join(DOCS, "search.html"), "w").write(html)
    kb = round(os.path.getsize(os.path.join(DOCS, "search-index.json")) / 1024)
    print(f"[build_search] wrote search.html + search-index.json ({kb}KB): {len(BLOCKS)} blocks, {len(ENTS)} entities, {len(PPL)} people")

if __name__ == "__main__":
    build()
