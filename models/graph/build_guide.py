#!/usr/bin/env python3
"""build_guide.py - render docs/guide.html: the Bubble-Map Guide (#108).

A self-contained helper to chat about / navigate the map + corpus. It builds a compact
client-side index from data/graph.json (nodes, sectors, degree, adjacency, edge notes) plus the
research-block titles, and ships a DETERMINISTIC question-answer engine that returns only real
graph facts + links (no hallucination): entity lookup, who-funds / connections, A->B path-finding,
the circular core, and corpus search. An OPTIONAL "bring your own key" panel can call any
OpenAI-compatible endpoint; when used, the model is given ONLY the retrieved context as grounding
and its output is clearly labelled AI-generated. With no key the guide is fully offline + factual.

Regenerable; run from new-research.sh. Writes docs/guide.html.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DOCS = os.path.join(ROOT, "data"); OUTDIR = os.path.join(ROOT, "docs")
import nav as _nav
import glob

G = json.load(open(os.path.join(ROOT, "data", "graph.json")))
ents = G["entities"]; edges = G["edges"]; analysis = G.get("analysis", {})

# which research stubs have a rendered on-site page (r-<stub>.html) + their titles
rpages = set(os.path.basename(p)[2:-5] for p in glob.glob(os.path.join(OUTDIR, "r-*.html")))
def block_title(stub):
    for ext in (".json",):
        fp = os.path.join(RES, stub + ext)
        if os.path.exists(fp):
            try:
                d = json.load(open(fp)); return (d.get("title") or (d.get("metadata") or {}).get("title") or stub)
            except Exception: pass
    # fall back to the .md H1
    mp = os.path.join(RES, stub + ".md")
    if os.path.exists(mp):
        for line in open(mp, encoding="utf-8", errors="ignore"):
            if line.startswith("# "): return line[2:].strip()
    return stub

# ---- compact client index ----
deg = {}; adj = {}; blocks_of = {}
def short(s, n=140):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return (s[:n] + "...") if len(s) > n else s
for e in edges:
    f, t = e["from"], e["to"]
    deg[f] = deg.get(f, 0) + 1; deg[t] = deg.get(t, 0) + 1
    note = short(e.get("note") or e.get("raw_instrument") or "")
    adj.setdefault(f, []).append([t, e.get("instrument", ""), e.get("layer", ""), "out", note])
    adj.setdefault(t, []).append([f, e.get("instrument", ""), e.get("layer", ""), "in", note])
    for sf in str(e.get("source_file", "")).split(","):
        sf = sf.strip()
        if sf.endswith(".json"): sf = sf[:-5]
        if sf:
            blocks_of.setdefault(f, set()).add(sf); blocks_of.setdefault(t, set()).add(sf)

NODES = {}
for nid, meta in ents.items():
    bl = sorted(b for b in blocks_of.get(nid, set()) if b in rpages)[:14]
    NODES[nid] = {"s": (meta or {}).get("sector", "other"), "d": deg.get(nid, 0), "b": bl}
# adjacency capped per node for payload size, keep highest-signal (financial first, then by note length)
ADJ = {}
for nid, lst in adj.items():
    lst.sort(key=lambda x: (0 if x[2] == "financial" else 1, -len(x[4])))
    ADJ[nid] = lst[:40]
BLOCK_TITLES = {s: block_title(s) for s in sorted(rpages)}
CORE = sorted(analysis.get("core_scc_all", []))
ROBUST = sorted(analysis.get("core_scc_robust_excl_cancelable", []))
IDX = {"nodes": NODES, "adj": ADJ, "blocks": BLOCK_TITLES, "core": CORE, "robust": ROBUST,
       "nfin": analysis.get("num_financial_edges"), "nstr": analysis.get("num_structural_edges")}

STYLE = (
    "body{background:#faf8f2;color:#1c1b19;font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 0 40px}"
    "main{max-width:860px;margin:0 auto;padding:0 18px}"
    "h1{font-family:Georgia,serif;font-weight:600;font-size:30px;margin:22px 0 2px}"
    ".sub{color:#6b665d;font-size:14px;margin:0 0 14px}"
    "a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;color:#6b3b16;font-size:13px}"
    "#log{margin:14px 0}.msg{margin:10px 0;padding:11px 14px;border-radius:10px;max-width:92%}"
    ".u{background:#1f4e79;color:#fff;margin-left:auto;border-bottom-right-radius:3px}"
    ".a{background:#fffdf8;border:1px solid #e4ddcc;border-bottom-left-radius:3px}"
    ".a b{color:#7b2d26}.a .lbl{font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:#8a8378}"
    ".a ul{margin:6px 0 2px;padding-left:18px}.a li{margin:3px 0}"
    ".pill{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;background:#efe9da;color:#4a453c;margin:0 4px 2px 0}"
    ".hop{font-size:12px;color:#6b665d}"
    "#bar{display:flex;gap:8px;position:sticky;bottom:0;background:#faf8f2;padding:10px 0}"
    "#q{flex:1;padding:11px 13px;font-size:15px;border:1px solid #c9bfa5;border-radius:8px;font-family:inherit}"
    "#send{padding:0 18px;font-size:15px;background:#1f4e79;color:#fff;border:0;border-radius:8px;cursor:pointer}"
    ".chips{margin:4px 0 2px}.chip{display:inline-block;font-size:12.5px;color:#1f4e79;background:#fffdf8;border:1px solid #e4ddcc;"
    "border-radius:14px;padding:5px 11px;margin:3px 5px 3px 0;cursor:pointer}"
    ".llm{border-left:3px solid #7b2d26;padding-left:9px}.llmwarn{font-size:11px;color:#7b2d26}"
    "details{margin:10px 0;font-size:13px;color:#4a453c}summary{cursor:pointer;color:#1f4e79}"
    "input[type=text],input[type=password]{width:100%;box-sizing:border-box;padding:7px 9px;margin:3px 0;border:1px solid #c9bfa5;border-radius:6px;font-family:inherit;font-size:13px}"
)

CHIPS = ["What is NVIDIA?", "How does OpenAI connect to Oracle?", "Who funds CoreWeave?",
         "Show the circular core", "What documents Palantir?", "Oracle"]

JS = r"""
let IDX = null;
const EL = id => document.getElementById(id);
const esc = s => (s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const human = id => id.replace(/_/g,' ');
const bmap = id => `<a href="bubblemap.html#node=${encodeURIComponent(id)}">${esc(human(id))}</a>`;
const rpage = s => IDX.blocks[s] ? `<a href="r-${esc(s)}.html">${esc(IDX.blocks[s])}</a>` : esc(s);

let NODES={}, ADJ={}, IDLIST=[], LOWER={};
function buildIndexLocals(){
  NODES=IDX.nodes; ADJ=IDX.adj||{}; IDLIST=Object.keys(NODES); LOWER={};
  IDLIST.forEach(id=>{LOWER[id.toLowerCase()]=id; LOWER[human(id).toLowerCase()]=id;});
}

function resolve(term){
  term=term.trim(); if(!term) return [];
  const t=term.toLowerCase();
  if(LOWER[t]) return [LOWER[t]];
  // startswith / includes ranked by degree
  let starts=[], incl=[];
  for(const id of IDLIST){
    const h=human(id).toLowerCase(), l=id.toLowerCase();
    if(h===t||l===t) return [id];
    if(h.startsWith(t)||l.startsWith(t)) starts.push(id);
    else if(h.includes(t)||l.includes(t)) incl.push(id);
  }
  const byDeg=(a,b)=>(NODES[b].d-NODES[a].d);
  starts.sort(byDeg); incl.sort(byDeg);
  return starts.concat(incl).slice(0,8);
}

function coreStatus(id){
  if(IDX.core.includes(id)) return IDX.robust.includes(id)
     ? 'in the <b>circular-financing core</b> (robust SCC of '+IDX.robust.length+')'
     : 'in the <b>circular-financing core</b> (headline SCC of '+IDX.core.length+'; drops from the robust set)';
  return null;
}

function entityAnswer(id){
  const n=NODES[id], a=ADJ[id]||[];
  const out=a.filter(x=>x[3]==='out'), inc=a.filter(x=>x[3]==='in');
  const fin=x=>x[2]==='financial';
  let h=`<div class=lbl>entity</div><b>${esc(human(id))}</b> &mdash; sector <span class=pill>${esc(n.s)}</span> degree <b>${n.d}</b>`;
  const cs=coreStatus(id); if(cs) h+=`<br><span style="color:#7b2d26">${cs}</span>`;
  function block(title, arr){
    if(!arr.length) return '';
    let s=`<div class=lbl style="margin-top:8px">${title}</div><ul>`;
    arr.slice(0,8).forEach(x=>{ s+=`<li>${bmap(x[0])} <span class=pill>${esc(x[1]||'link')}</span>${fin(x)?'':' <span class=hop>(overlay)</span>'}`+
        (x[4]?`<div class=hop>${esc(x[4])}</div>`:'')+`</li>`; });
    return s+'</ul>';
  }
  h+=block('points to / funds / commits', out);
  h+=block('pointed to by / funded by', inc);
  if(n.b.length){ h+='<div class=lbl style="margin-top:8px">documented in</div><ul>'+n.b.map(s=>`<li>${rpage(s)}</li>`).join('')+'</ul>'; }
  h+=`<div class=hop style="margin-top:6px">Open in the <a href="bubblemap.html#node=${encodeURIComponent(id)}">bubble map</a>.</div>`;
  return h;
}

function pathAnswer(a,b){
  // BFS over undirected adjacency; reconstruct with direction + instrument per hop
  const prev={}, seen={[a]:true}, q=[a];
  while(q.length){ const v=q.shift(); if(v===b) break;
    for(const x of (ADJ[v]||[])){ const w=x[0]; if(!seen[w]){ seen[w]=true; prev[w]=[v,x]; q.push(w); } } }
  if(!(b in prev) && a!==b) return `<div class=lbl>path</div>No connecting path found between ${bmap(a)} and ${bmap(b)} in the mapped edges.`;
  let chain=[], cur=b; while(cur!==a){ const [p,x]=prev[cur]; chain.unshift([p,cur,x]); cur=p; }
  let h=`<div class=lbl>path</div>${bmap(a)}`;
  chain.forEach(([p,c,x])=>{ const arrow=x[3]==='out'?'&rarr;':'&larr;'; h+=` <span class=hop>${arrow} <i>${esc(x[1]||'link')}</i> ${arrow}</span> ${bmap(c)}`; });
  h+=`<div class=hop style="margin-top:6px">${chain.length} hop(s). Arrows show edge direction; italics = instrument. Overlay/structural edges are documented ties, not money flows.</div>`;
  return h;
}

function coreAnswer(){
  let h=`<div class=lbl>circular-financing core</div>The headline core is the Tarjan strongly-connected component over the <b>financial</b> edge layer (${IDX.nfin} financial edges). `;
  h+=`Headline SCC = <b>${IDX.core.length}</b> firms; robust (excluding cancelable) = <b>${IDX.robust.length}</b>.<ul>`;
  h+=IDX.core.map(id=>`<li>${bmap(id)}${IDX.robust.includes(id)?'':' <span class=hop>(headline only)</span>'}</li>`).join('');
  h+='</ul><div class=hop>See the <a href="core-robustness.html">robustness certificate</a> and <a href="methodology.html">methodology</a>.</div>';
  return h;
}

function searchAnswer(q){
  const t=q.toLowerCase();
  const toks=t.split(/[^a-z0-9]+/).filter(x=>x.length>2);
  const nodeHits=resolve(q).slice(0,6);
  let blkHits=[];
  for(const s in IDX.blocks){ const ti=IDX.blocks[s].toLowerCase(); let sc=0; toks.forEach(k=>{ if(ti.includes(k)) sc++; }); if(sc) blkHits.push([s,sc]); }
  blkHits.sort((a,b)=>b[1]-a[1]); blkHits=blkHits.slice(0,8);
  if(!nodeHits.length && !blkHits.length) return `<div class=lbl>no match</div>I couldn't find that in the graph or the research blocks. Try an entity name (e.g. <code>Oracle</code>), two entities for a path, or a keyword.`;
  let h='';
  if(nodeHits.length){ h+=`<div class=lbl>entities</div><ul>`+nodeHits.map(id=>`<li>${bmap(id)} <span class=pill>${esc(NODES[id].s)}</span></li>`).join('')+'</ul>'; }
  if(blkHits.length){ h+=`<div class=lbl style="margin-top:8px">research blocks</div><ul>`+blkHits.map(([s])=>`<li>${rpage(s)}</li>`).join('')+'</ul>'; }
  return h;
}

// intent routing (deterministic)
function answer(q){
  const t=q.toLowerCase().trim();
  if(/\b(circular|core|scc|loop)\b/.test(t) && !/\bfund|connect|path\b/.test(t)) return coreAnswer();
  // path: "A to B", "connect A and B", "path from A to B", "between A and B"
  let m=t.match(/(?:path|connect(?:ion|ed)?|link|between|from)\b/);
  if(m){
    const parts=q.split(/\bto\b|\band\b|\bwith\b|\bbetween\b|->|,/i).map(s=>s.replace(/\b(path|connect(ion|ed)?|link|from|how|does|between|the)\b/ig,'').trim()).filter(Boolean);
    if(parts.length>=2){ const a=resolve(parts[0])[0], b=resolve(parts[1])[0]; if(a&&b) return pathAnswer(a,b); }
  }
  // who funds X / connections of X
  m=t.match(/(?:who funds|funds|funded by|invest(?:s|ors)? in|connections? (?:of|to)|backers of)\s+(.+)/);
  if(m){ const c=resolve(m[1])[0]; if(c) return entityAnswer(c); }
  // what is X / tell me about X
  m=t.match(/(?:what is|who is|tell me about|about|what's)\s+(.+)/);
  if(m){ const cand=resolve(m[1].replace(/[?.!]+$/,'')); if(cand.length===1) return entityAnswer(cand[0]); if(cand.length>1) return searchAnswer(m[1]); }
  // bare entity
  const r=resolve(q.replace(/[?.!]+$/,''));
  if(r.length===1) return entityAnswer(r[0]);
  if(r.length>1 && r[0] && human(r[0]).toLowerCase()===t) return entityAnswer(r[0]);
  return searchAnswer(q);
}

// retrieved context for optional LLM grounding
function context(q){
  const lines=[]; const ids=new Set();
  (resolve(q)||[]).slice(0,4).forEach(id=>ids.add(id));
  const m=q.toLowerCase().match(/\b([a-z0-9_]+)\b/g)||[]; // also exact-id tokens
  ids.forEach(id=>{
    const n=NODES[id]; lines.push(`NODE ${human(id)} | sector=${n.s} degree=${n.d}${IDX.core.includes(id)?' | in circular core':''}`);
    (ADJ[id]||[]).slice(0,10).forEach(x=>lines.push(`  ${x[3]==='out'?human(id)+' -> '+human(x[0]):human(x[0])+' -> '+human(id)} [${x[1]}${x[2]==='financial'?'':'/overlay'}]${x[4]?' : '+x[4]:''}`));
    n.b.forEach(s=>lines.push(`  documented-in: ${IDX.blocks[s]} (r-${s}.html)`));
  });
  return lines.join('\n').slice(0,6000);
}

function add(who,html){ const d=document.createElement('div'); d.className='msg '+who; d.innerHTML=html; EL('log').appendChild(d); window.scrollTo(0,document.body.scrollHeight); return d; }

async function ask(q){
  if(!q.trim()) return;
  add('u', esc(q));
  const det=answer(q);
  add('a', det);
  // optional grounded LLM
  const key=localStorage.getItem('guide_key'), ep=localStorage.getItem('guide_ep')||'https://api.openai.com/v1/chat/completions', model=localStorage.getItem('guide_model')||'gpt-4o-mini';
  if(key){
    const box=add('a','<div class=llm><span class=lbl>AI (grounded, beta)</span><br>thinking&hellip;</div>');
    try{
      const ctx=context(q);
      const r=await fetch(ep,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},
        body:JSON.stringify({model,temperature:0,messages:[
          {role:'system',content:'You are a guide to a research knowledge-graph. Answer ONLY using the CONTEXT below. If the answer is not in the context, say you do not have it in the map. Be concise; never invent entities, numbers, or relationships. CONTEXT:\n'+ctx},
          {role:'user',content:q}]})});
      const j=await r.json(); const txt=(j.choices&&j.choices[0]&&j.choices[0].message.content)||(j.error&&j.error.message)||'no response';
      box.innerHTML='<div class=llm><span class=lbl>AI (grounded, beta)</span><br>'+esc(txt).replace(/\n/g,'<br>')+'<div class=llmwarn>AI-generated from the retrieved context above - may still be wrong; verify against the linked blocks.</div></div>';
    }catch(e){ box.innerHTML='<div class=llm><span class=lbl>AI</span><br>Request failed: '+esc(e.message)+'</div>'; }
  }
}

window.addEventListener('DOMContentLoaded',async ()=>{
  // settings (available immediately)
  ['ep','key','model'].forEach(k=>{ const v=localStorage.getItem('guide_'+k); if(v&&EL('set_'+k)) EL('set_'+k).value=v; });
  EL('savekey').onclick=()=>{ ['ep','key','model'].forEach(k=>{ const v=EL('set_'+k).value.trim(); if(v) localStorage.setItem('guide_'+k,v); else localStorage.removeItem('guide_'+k); }); add('a','<span class=lbl>settings</span><br>Saved locally in your browser. '+(EL('set_key').value.trim()?'AI grounding is ON.':'AI grounding is OFF (deterministic mode).')); };
  const greet=add('a','<div class=lbl>guide</div>Loading the graph index&hellip;');
  try{
    const r=await fetch('guide-index.json'); IDX=await r.json(); buildIndexLocals();
  }catch(e){ greet.innerHTML='<div class=lbl>guide</div>Could not load the graph index ('+esc(e.message)+'). Try reloading.'; return; }
  EL('send').onclick=()=>{ const q=EL('q').value; EL('q').value=''; ask(q); };
  EL('q').addEventListener('keydown',e=>{ if(e.key==='Enter'){ EL('send').click(); } });
  document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{ EL('q').value=c.textContent; EL('send').click(); });
  greet.innerHTML='<div class=lbl>guide</div>Ask about any mapped entity, how two entities connect, who funds whom, the circular-financing core, or a keyword. Answers are built <b>directly from the graph</b> ('+IDLIST.length+' entities) and link to the bubble map + research blocks. No data leaves your browser unless you add an API key in Settings.';
});
"""

def build():
    chips = "".join(f'<span class=chip>{c}</span>' for c in CHIPS)
    settings = ('<details><summary>Settings - optional AI grounding (bring your own key)</summary>'
        '<p class=sub>By default the guide is fully deterministic and offline (it only reports graph facts + links). '
        'If you add an OpenAI-compatible endpoint + key, your question plus the <i>retrieved graph context</i> are sent to that endpoint; '
        'the model is instructed to answer only from that context. The key is stored in your browser (localStorage) and used only for your requests.</p>'
        '<label>Endpoint <input type=text id=set_ep placeholder="https://api.openai.com/v1/chat/completions"></label>'
        '<label>Model <input type=text id=set_model placeholder="gpt-4o-mini"></label>'
        '<label>API key <input type=password id=set_key placeholder="sk-... (optional; stays in your browser)"></label>'
        '<button id=savekey style="margin-top:6px;padding:6px 12px;border:1px solid #c9bfa5;border-radius:6px;background:#fffdf8;color:#1f4e79;cursor:pointer">Save</button></details>')
    json.dump(IDX, open(os.path.join(OUTDIR, "guide-index.json"), "w"), separators=(",", ":"), ensure_ascii=False)
    js = JS
    html = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Guide - Bubble Map</title><style>{STYLE}</style></head><body>"
            + _nav.navbar("Guide", disclaimer=True)
            + "<main><h1>Bubble-Map Guide</h1>"
            + f"<p class=sub>Ask the map. Answers are generated from the graph ({len(NODES)} entities, {IDX['nfin']} financial + {IDX['nstr']} structural edges) and link straight to the bubble map and the research blocks - deterministic and offline by default.</p>"
            + f"<div class=chips>{chips}</div>"
            + "<div id=log></div>"
            + "<div id=bar><input id=q type=text placeholder='Ask about an entity, a connection, who funds whom, or the circular core...' autocomplete=off><button id=send>Ask</button></div>"
            + settings
            + f"<script>{js}</script></main></body></html>")
    open(os.path.join(OUTDIR, "guide.html"), "w").write(html)
    import os as _os
    kb = round(_os.path.getsize(os.path.join(OUTDIR, "guide-index.json")) / 1024)
    print(f"[build_guide] wrote guide.html (shell) + guide-index.json ({kb}KB): {len(NODES)} nodes, {len(BLOCK_TITLES)} blocks, core={len(CORE)}/{len(ROBUST)}")

if __name__ == "__main__":
    build()
