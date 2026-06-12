#!/usr/bin/env python3
"""
build_bubblemap.py - the interactive 'Bubble Map' the project is named for: a draggable, zoomable
d3 force-directed graph of data/graph.json (189 entities / 198 directed edges). Nodes sized by
degree, colored by sector-bucket; financial edges solid, structural edges faint/dashed; the
circular core (Tarjan SCC) ring-highlighted. Click a bubble for a detail panel (sector, neighbours,
the research blocks documenting it, and any matching Persons-of-Interest profile). Self-contained
HTML (d3 v7 from CDN; data embedded), light academic theme, shared nav. Writes docs/bubblemap.html.
"""
import json, os, html
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs"); REP=os.path.join(ROOT,"report")

def load(n):
    try: return json.load(open(os.path.join(ROOT,"data",n)))
    except Exception: return {}
g=load("graph.json"); P=load("persons.json")
ents=g.get("entities",{}); edges=g.get("edges",[]); an=g.get("analysis",{})
scc=set(an.get("core_scc_all",[])); scc_robust=set(an.get("core_scc_robust_excl_cancelable",[]))

# sector -> bucket -> colour
BUCKET={ "ai":["ai_lab","hyperscaler","chip_vendor","ai_infra","neocloud","semiconductor","ai_data","tech","bigtech_asia"],
 "capital":["financier","private_credit","insurance","bank","creditor","central_bank","financial_infra","sink","exogenous_source"],
 "crypto":["crypto_infra","stablecoin","exchange","dlt","crypto_firm"],
 "defense":["defense","defense_tech","state_intel","security_research","threat_actor"],
 "state":["state","regulator","commission","political","statistical_agency"],
 "commodity":["commodity","commodity_market","critical_minerals","energy","industrial","space_real_economy"],
 "identity":["surveillance","privacy_tool","standards","ip_rightsholder","telecom","satellite","journalism"],
 "macro":["macro_factor","statistic","labor","labor_platform","data_provider","retail"],
 "pqc":["pqc_quantum"], "person":["person"], "other":["other","spv","offshore"] }
SEC2BUCKET={s:b for b,ss in BUCKET.items() for s in ss}
COLORS={"ai":"#1f4e79","capital":"#7b2d26","crypto":"#b8860b","defense":"#2e8b57","state":"#c0392b",
 "commodity":"#8a5a2b","identity":"#5e35b1","macro":"#138a8a","pqc":"#6b3b16","person":"#d35400","other":"#8a8378"}
BLABEL={"ai":"AI core","capital":"Capital / credit","crypto":"Crypto","defense":"Defense / security",
 "state":"State / regulator","commodity":"Commodities / energy","identity":"Identity / telecom",
 "macro":"Macro / data","pqc":"PQC / quantum","person":"Person","other":"Infra / other"}

# degree + incident research blocks per node
deg={}; blocks={}
for e in edges:
    a,b=e.get("from"),e.get("to")
    deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
    sf=e.get("source_file","")
    if sf.endswith(".json"):
        stub=sf[:-5]
        for x in (a,b): blocks.setdefault(x,set()).add(stub)

# org/name -> person(s): match person.name==id, or any of person.orgs contains id (or id contains an org token)
def match_persons(node):
    out=[]
    nl=node.lower()
    for p in P.get("persons",[]):
        if p["name"].lower()==nl: out.append(p["name"]); continue
        for o in p.get("orgs",[]):
            ol=o.lower()
            # token overlap: the node name appears in an org string or vice-versa (len>=3 guard)
            if len(nl)>=3 and (nl in ol or any(tok==nl for tok in ol.replace("/"," ").replace(","," ").split())):
                out.append(p["name"]); break
    return sorted(set(out))

nodes=[]
for name,meta in ents.items():
    sec=(meta or {}).get("sector","other"); bucket=SEC2BUCKET.get(sec,"other")
    nodes.append({"id":name,"sector":sec,"bucket":bucket,"deg":deg.get(name,0),
                  "scc": name in scc, "robust": name in scc_robust,
                  "blocks":sorted(blocks.get(name,[])),"persons":match_persons(name)})
links=[{"source":e["from"],"target":e["to"],"layer":e.get("layer","financial"),
        "instrument":e.get("raw_instrument") or e.get("instrument",""),"circular":bool(e.get("declared_circular")),
        "cancelable":bool(e.get("cancelable")),"note":(e.get("note") or "")[:200],
        "block":(e.get("source_file","")[:-5] if e.get("source_file","").endswith(".json") else "")} for e in edges]

NAV=('<div class=nav><a href="index.html">Home</a><a href="dashboard.html">Dashboard</a>'
 '<a href="charts.html">Charts</a><a href="research.html">Research</a><a href="persons.html">Persons</a>'
 '<a href="bubblemap.html" class=active>Bubble Map</a><a href="globe.html">Globe</a>'
 '<a href="methodology.html">Methodology</a><a href="glossary.html">Glossary</a></div>')
legend="".join(f'<span class=lg><i style="background:{COLORS[b]}"></i>{html.escape(BLABEL[b])}</span>' for b in BLABEL)

HTML="""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Bubble Map — the AI capital loop graph</title>
<style>
:root{--bg:#faf8f2;--paper:#fffdf8;--ink:#1c1b19;--mut:#6b665d;--line:#e4ddcc;--ac:#7b2d26;--ac2:#1f4e79}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;overflow:hidden}
.nav{background:var(--paper);border-bottom:1px solid var(--line);padding:10px 18px;font-size:14px}
.nav a{color:var(--ac2);text-decoration:none;margin-right:16px}.nav a.active{font-weight:700}.nav a:hover{text-decoration:underline}
#stage{position:relative;width:100%;height:calc(100vh - 41px);overflow:hidden}
svg{display:block;width:100%;height:100%;cursor:grab}svg:active{cursor:grabbing}
#hud{position:absolute;top:12px;left:14px;z-index:5;max-width:300px;background:#fffdf8e8;border:1px solid var(--line);border-radius:9px;padding:12px 14px}
#hud h1{font:600 16px Georgia,serif;margin:0 0 2px}.sub{color:var(--mut);font-size:11.5px;margin-bottom:9px}
#q{width:100%;padding:8px 10px;font-size:13px;border:1px solid var(--line);border-radius:6px;margin-bottom:8px;font-family:inherit}
.tog{display:block;font-size:12.5px;color:#33312c;margin:4px 0;cursor:pointer;user-select:none}
.tog input{vertical-align:-1px;margin-right:6px}
#legend{display:flex;flex-wrap:wrap;gap:3px 10px;margin-top:9px}
.lg{font-size:11px;color:#33312c;white-space:nowrap}.lg i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px;vertical-align:middle}
#panel{position:absolute;top:12px;right:14px;z-index:6;width:300px;max-height:calc(100% - 24px);overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:none;box-shadow:0 6px 22px #0002}
#panel h2{margin:0 0 2px;font:600 17px Georgia,serif}#panel .pr{color:var(--mut);font-size:12px;margin-bottom:8px}
#panel .k{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--ac);font-weight:700;margin:11px 0 3px}
#panel a{color:var(--ac2);text-decoration:none}#panel a:hover{text-decoration:underline}
#panel .pill{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;color:#fff;margin:0 4px 4px 0}
#panel ul{margin:4px 0;padding-left:18px}#panel li{font-size:12.5px;margin:2px 0}
#close{position:absolute;top:8px;right:10px;cursor:pointer;color:var(--mut);font-size:18px;line-height:1}
.note{position:absolute;bottom:10px;left:14px;font-size:11px;color:var(--mut);background:#fffdf8c8;padding:4px 8px;border-radius:5px}
text.lab{font-size:9px;fill:#3a382f;pointer-events:none}
</style></head><body>__NAV__
<div id=stage>
<div id=hud><h1>Bubble Map</h1><div class=sub>the AI capital loop, as a graph &middot; drag bubbles &middot; scroll to zoom &middot; click for detail</div>
<input id=q placeholder="Find an entity&hellip;" autocomplete=off>
<label class=tog><input type=checkbox id=tStruct checked> structural edges (governance/legal)</label>
<label class=tog><input type=checkbox id=tCore> dim all but the circular core</label>
<label class=tog><input type=checkbox id=tLab> show labels</label>
<div id=legend>__LEGEND__</div></div>
<div id=panel><span id=close>&times;</span><div id=pbody></div></div>
<div class=note>__N__ entities &middot; __E__ edges &middot; gold ring = the 11-firm circular core (Tarjan SCC) &middot; solid = financial flow, dashed = structural</div>
<svg id=g></svg></div>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
const NODES=__NODES__, LINKS=__LINKS__, COLORS=__COLORS__;
const W=()=>document.getElementById('stage').clientWidth, H=()=>document.getElementById('stage').clientHeight;
const svg=d3.select('#g'); const root=svg.append('g');
svg.append('defs').selectAll('marker').data(['fin','struct']).join('marker')
 .attr('id',d=>'arr-'+d).attr('viewBox','0 -5 10 10').attr('refX',18).attr('refY',0)
 .attr('markerWidth',5).attr('markerHeight',5).attr('orient','auto')
 .append('path').attr('d','M0,-4L8,0L0,4').attr('fill',d=>d==='fin'?'#9a8f78':'#cdc6b4');
const id2n=new Map(NODES.map(n=>[n.id,n]));
const link=root.append('g').selectAll('line').data(LINKS).join('line')
 .attr('stroke',d=>d.layer==='financial'?(d.circular?'#c0392b':'#9a8f78'):'#d8d0bd')
 .attr('stroke-width',d=>d.circular?1.7:(d.layer==='financial'?1.1:0.7))
 .attr('stroke-dasharray',d=>d.layer==='structural'?'3,3':null).attr('opacity',.55)
 .attr('marker-end',d=>'url(#arr-'+(d.layer==='financial'?'fin':'struct')+')');
const rad=d=>4+Math.sqrt(d.deg)*2.2;
const node=root.append('g').selectAll('g').data(NODES).join('g').style('cursor','pointer').on('click',(e,d)=>showPanel(d));
node.append('circle').attr('r',rad).attr('fill',d=>COLORS[d.bucket]||'#8a8378')
 .attr('stroke',d=>d.scc?'#d4a017':'#fffdf8').attr('stroke-width',d=>d.scc?2.6:1);
node.append('title').text(d=>d.id+'  ('+d.sector+', deg '+d.deg+')');
const labels=root.append('g').selectAll('text').data(NODES).join('text').attr('class','lab')
 .attr('dx',d=>rad(d)+2).attr('dy',3).text(d=>d.id).style('display','none');
const sim=d3.forceSimulation(NODES)
 .force('link',d3.forceLink(LINKS).id(d=>d.id).distance(d=>d.layer==='financial'?70:95).strength(.25))
 .force('charge',d3.forceManyBody().strength(-160))
 .force('center',d3.forceCenter(W()/2,H()/2)).force('collide',d3.forceCollide().radius(d=>rad(d)+3))
 .on('tick',tick);
function tick(){
 link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
 node.attr('transform',d=>`translate(${d.x},${d.y})`);
 labels.attr('x',d=>d.x).attr('y',d=>d.y);
}
node.call(d3.drag().on('start',(e,d)=>{if(!e.active)sim.alphaTarget(.3).restart();d.fx=d.x;d.fy=d.y;})
 .on('drag',(e,d)=>{d.fx=e.x;d.fy=e.y;}).on('end',(e,d)=>{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}));
svg.call(d3.zoom().scaleExtent([.2,6]).on('zoom',e=>root.attr('transform',e.transform)));
// controls
document.getElementById('tStruct').onchange=e=>{const on=e.target.checked;
 link.style('display',d=>d.layer==='structural'&&!on?'none':null);};
document.getElementById('tLab').onchange=e=>labels.style('display',e.target.checked?null:'none');
document.getElementById('tCore').onchange=e=>{const on=e.target.checked;
 node.style('opacity',d=>!on||d.scc?1:.12); link.style('opacity',d=>!on?.55:((id2n.get(typeof d.source==='object'?d.source.id:d.source).scc&&id2n.get(typeof d.target==='object'?d.target.id:d.target).scc)?.7:.05));};
const q=document.getElementById('q');
q.oninput=()=>{const s=q.value.trim().toLowerCase();
 node.select('circle').attr('stroke',d=>{if(s&&d.id.toLowerCase().includes(s))return '#1f4e79';return d.scc?'#d4a017':'#fffdf8';})
  .attr('stroke-width',d=>{if(s&&d.id.toLowerCase().includes(s))return 3.4;return d.scc?2.6:1;});};
document.getElementById('close').onclick=()=>document.getElementById('panel').style.display='none';
function neighbors(d){const ins=[],outs=[];LINKS.forEach(l=>{const s=typeof l.source==='object'?l.source.id:l.source,t=typeof l.target==='object'?l.target.id:l.target;
 if(s===d.id)outs.push({n:t,i:l.instrument,c:l.circular}); if(t===d.id)ins.push({n:s,i:l.instrument,c:l.circular});});return {ins,outs};}
function showPanel(d){const p=document.getElementById('panel'),b=document.getElementById('pbody');
 const {ins,outs}=neighbors(d);
 const blk=d.blocks.map(x=>`<a href="r-${x}.html">${x}</a>`).join(' &middot; ')||'<span style="color:#6b665d">—</span>';
 const per=d.persons.length?d.persons.map(x=>`<a href="persons.html">${x}</a>`).join(', '):'';
 const nb=a=>a.length?('<ul>'+a.slice(0,14).map(x=>`<li>${x.c?'<b style=color:#c0392b>↻</b> ':''}${x.n} <span style=color:#6b665d>(${x.i||'—'})</span></li>`).join('')+(a.length>14?`<li style=color:#6b665d>+${a.length-14} more…</li>`:'')+'</ul>'):'<div style="color:#6b665d;font-size:12px">—</div>';
 b.innerHTML=`<h2>${d.id}</h2><div class=pr>${d.sector} &middot; degree ${d.deg}${d.scc?' &middot; <b style=color:#9a6a1a>circular core'+(d.robust?' (robust)':' (via cancelable)')+'</b>':''}</div>`
  +`<span class=pill style="background:${COLORS[d.bucket]}">${d.bucket}</span>`
  +(per?`<div class=k>Key person</div><div>${per}</div>`:'')
  +`<div class=k>Outflows (${outs.length})</div>${nb(outs)}`
  +`<div class=k>Inflows (${ins.length})</div>${nb(ins)}`
  +`<div class=k>Documented in</div><div style=font-size:12.5px>${blk}</div>`;
 p.style.display='block';}
</script></body></html>"""
HTML=(HTML.replace("__NAV__",NAV).replace("__LEGEND__",legend)
      .replace("__N__",str(len(nodes))).replace("__E__",str(len(links)))
      .replace("__NODES__",json.dumps(nodes)).replace("__LINKS__",json.dumps(links))
      .replace("__COLORS__",json.dumps(COLORS)))
open(os.path.join(DOCS,"bubblemap.html"),"w").write(HTML)
print(f"wrote docs/bubblemap.html ({len(HTML)} bytes) - {len(nodes)} nodes, {len(links)} links, {len(scc)} in core")
if os.path.isdir(REP): open(os.path.join(REP,"BUBBLEMAP.html"),"w").write(HTML)
