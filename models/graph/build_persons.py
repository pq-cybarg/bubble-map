#!/usr/bin/env python3
"""
build_persons.py - generate the "Persons of Interest" tab: a contacts-list / dossier UI over
data/persons.json. Each entry is a structured leadership-analysis assessment (BLUF, drivers,
worldview, decision/risk profile, track record, vulnerabilities/levers, relationships, outlook,
confidence) that expands inline. Search + domain-filter chips. Self-contained HTML (data embedded),
light academic theme, shared site nav. Writes docs/persons.html and report/PERSONS.html.
"""
import json, os, html, re
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs"); REP=os.path.join(ROOT,"report")
def slug(name): return "p-"+re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
import glob as _glob
MD_HAVE=set(os.path.basename(f)[:-3] for f in _glob.glob(os.path.join(ROOT,"research","*.md")))
try: ENT_IDS=set(json.load(open(os.path.join(ROOT,"data","graph.json"))).get("entities",{}).keys())
except Exception: ENT_IDS=set()
def graph_nodes(p):
    out=set()
    for o in p.get("orgs",[]):
        if o in ENT_IDS: out.add(o)
        for t in o.replace("/"," ").replace("(", " ").replace(")"," ").split(","):
            t=t.strip()
            if t in ENT_IDS: out.add(t)
    return sorted(out)

def load():
    try: return json.load(open(os.path.join(ROOT,"data","persons.json")))
    except Exception: return {"meta":{},"persons":[]}

D=load(); persons=D.get("persons",[]); meta=D.get("meta",{})

DOMAIN_COLORS={"AI":"#1f4e79","Capital":"#7b2d26","Crypto":"#b8860b","Defense":"#2e8b57",
 "Digital-ID":"#5e35b1","State/Policy":"#c0392b","Macro/Finance":"#138a8a","Sovereign":"#d35400",
 "Geopolitics":"#8a5a2b","Markets":"#6b3b16"}
def dcolor(d): return DOMAIN_COLORS.get(d,"#6b665d")

NAV=('<div class=nav><div class=wrap style="padding:0">'
 '<a href="index.html">Home</a><a href="dashboard.html">Dashboard</a><a href="charts.html">Charts</a>'
 '<a href="research.html">Research</a><a href="persons.html" class=active>Persons</a>'
 '<a href="bubblemap.html">Bubble Map</a>'
 '<a href="methodology.html">Methodology</a><a href="glossary.html">Glossary</a><a href="globe.html">Globe</a>'
 '</div></div>')

# rows of the dossier body, in display order, with their label
FIELDS=[("bluf","Bottom line"),("drivers","Drivers & motivations"),("worldview","Worldview & origins"),
        ("decision_style","Decision-making & risk"),("track_record","Track record"),
        ("vulnerabilities","Vulnerabilities & levers"),("relationships","Relationships & rivalries"),
        ("outlook","Outlook & indicators"),("confidence","Confidence"),("grade","Grading")]

def initials(name):
    parts=[p for p in name.replace("(","").replace(")","").split() if p[:1].isalpha()]
    if len(parts)>=2: return (parts[0][0]+parts[-1][0]).upper()
    return name[:2].upper()

GH="https://github.com/pq-cybarg/bubble-map/blob/main/research/"
CSS="""
:root{--bg:#faf8f2;--paper:#fffdf8;--ink:#1c1b19;--mut:#6b665d;--line:#e4ddcc;--ac:#7b2d26;--ac2:#1f4e79}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif}
.nav{background:var(--paper);border-bottom:1px solid var(--line);padding:11px 22px;font-size:14px}
.nav a{color:var(--ac2);text-decoration:none;margin-right:18px}.nav a:hover{text-decoration:underline}
.nav a.active{font-weight:700}
.wrap{max-width:900px;margin:0 auto;padding:0 22px}
header.h{background:var(--paper);border-bottom:1px solid var(--line);padding:30px 22px 22px}
h1{margin:0 0 4px;font-size:30px;font-weight:600;font-family:Georgia,serif}
.sub{color:var(--mut);font-size:15px;margin:0 0 12px}
.note{background:#fff8e8;border:1px solid #e8dcb8;border-radius:8px;padding:12px 15px;font-size:13.5px;color:#5b4a1a;margin:8px 0 0}
.note b{color:#7a5a12}
.controls{position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 0 8px;border-bottom:1px solid var(--line);margin-bottom:8px}
#q{width:100%;padding:11px 14px;font-size:15px;border:1px solid var(--line);border-radius:8px;background:var(--paper);font-family:inherit}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.chip{font-size:12.5px;padding:5px 11px;border-radius:20px;border:1px solid var(--line);background:var(--paper);color:var(--mut);cursor:pointer;user-select:none}
.chip.on{color:#fff;border-color:transparent}
.count{color:var(--mut);font-size:13px;margin:10px 0 4px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;margin:10px 0;overflow:hidden}
.row{display:flex;align-items:center;gap:14px;padding:14px 16px;cursor:pointer}
.row:hover{background:#fbf8f0}
.av{flex:0 0 auto;width:46px;height:46px;border-radius:50%;color:#fff;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center}
.who{flex:1 1 auto;min-width:0}
.who .nm{font-weight:600;font-size:16.5px}
.who .rl{color:var(--mut);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:5px}
.tag{font-size:11px;padding:2px 8px;border-radius:10px;color:#fff}
.exp{flex:0 0 auto;color:var(--mut);font-size:18px;transition:transform .15s}
.card.open .exp{transform:rotate(90deg)}
.body{display:none;padding:4px 18px 18px;border-top:1px solid var(--line)}
.card.open .body{display:block}
.fld{margin:13px 0}
.fld .lab{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ac);font-weight:700;margin-bottom:3px}
.fld .val{font-size:15px;color:#26241f}
.fld.bluf .val{font-size:15.5px;font-weight:500;border-left:3px solid var(--ac);padding-left:12px}
.src{margin-top:12px;font-size:13px;color:var(--mut)}
.src a{color:var(--ac2);text-decoration:none;margin-right:10px}
.empty{color:var(--mut);text-align:center;padding:40px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px;color:var(--mut);font-size:13px;text-align:center}
"""

def card_html(i,p):
    doms=p.get("domains",[])
    tags="".join(f'<span class=tag style="background:{dcolor(d)}">{html.escape(d)}</span>' for d in doms)
    body=[]
    for k,lab in FIELDS:
        v=p.get(k)
        if not v: continue
        cls="fld bluf" if k=="bluf" else "fld"
        body.append(f'<div class="{cls}"><div class=lab>{lab}</div><div class=val>{html.escape(str(v))}</div></div>')
    blocks=p.get("blocks",[])
    if blocks:
        links=" ".join((f'<a href="r-{html.escape(b)}.html">{html.escape(b)}</a>' if b in MD_HAVE
                        else f'<code>{html.escape(b)}</code>') for b in blocks)
        body.append(f'<div class=src><b>Documented in:</b> {links}</div>')
    gn=graph_nodes(p)
    if gn:
        gl=" &middot; ".join(f'<a href="bubblemap.html#node={html.escape(n)}">{html.escape(n)}</a>' for n in gn)
        body.append(f'<div class=src><b>In the Bubble Map:</b> {gl}</div>')
    av=dcolor(doms[0]) if doms else "#6b665d"
    hay=html.escape(" ".join([p.get("name",""),p.get("role",""),
        " ".join(p.get("orgs",[]))," ".join(doms),p.get("bluf","")]).lower())
    return (f'<div class=card id="{slug(p.get("name",""))}" data-domains="{html.escape("|".join(doms))}" data-hay="{hay}">'
            f'<div class=row onclick="this.parentNode.classList.toggle(\'open\')">'
            f'<div class=av style="background:{av}">{html.escape(initials(p.get("name","?")))}</div>'
            f'<div class=who><div class=nm>{html.escape(p.get("name",""))}</div>'
            f'<div class=rl>{html.escape(p.get("role",""))}</div>'
            f'<div class=tags>{tags}</div></div>'
            f'<div class=exp>&#9656;</div></div>'
            f'<div class=body>{"".join(body)}</div></div>')

alldoms=sorted({d for p in persons for d in p.get("domains",[])})
chips="".join(f'<span class=chip data-d="{html.escape(d)}" style="--c:{dcolor(d)}">{html.escape(d)}</span>' for d in alldoms)
cards="".join(card_html(i,p) for i,p in enumerate(persons))

HTML=f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Persons of Interest — Bubble Map</title><style>{CSS}</style></head><body>
{NAV}
<header class=h><div class=wrap>
<h1>Persons of Interest</h1>
<p class=sub>{html.escape(meta.get("subtitle","Leadership & strategic-behavior assessments"))} &middot; {len(persons)} profiles &middot; generated {html.escape(meta.get("generated",""))}</p>
<div class=note><b>Method &amp; limits.</b> {html.escape(meta.get("method",""))}</div>
</div></header>
<div class=wrap>
<div class=controls>
<input id=q type=search placeholder="Search name, role, organisation, or assessment&hellip;" autocomplete=off>
<div class=chips id=chips>{chips}</div>
</div>
<div class=count id=count></div>
<div id=list>{cards}</div>
<div class=empty id=empty style="display:none">No matching profiles.</div>
</div>
<footer>Behavioral &amp; strategic assessments from the public record &middot; not clinical diagnosis &middot; inference labeled, facts cited &middot; excluded from the formal proofs &middot; contact resistant@tuta.com</footer>
<script>
const cards=[...document.querySelectorAll('.card')], q=document.getElementById('q'),
 count=document.getElementById('count'), empty=document.getElementById('empty');
let active=new Set();
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{{
 const d=c.dataset.d;
 if(active.has(d)){{active.delete(d);c.classList.remove('on');c.style.background='';}}
 else{{active.add(d);c.classList.add('on');c.style.background=c.style.getPropertyValue('--c');}}
 apply();}}));
q.addEventListener('input',apply);
function apply(){{
 const s=q.value.trim().toLowerCase(); let n=0;
 cards.forEach(card=>{{
  const okText=!s||card.dataset.hay.includes(s);
  const doms=card.dataset.domains.split('|');
  const okDom=active.size===0||[...active].every(d=>doms.includes(d));
  const show=okText&&okDom; card.style.display=show?'':'none'; if(show)n++;
 }});
 count.textContent=n+' of '+cards.length+' profiles';
 empty.style.display=n?'none':'block';
}}
apply();
function openHash(){{if(!location.hash)return;const el=document.querySelector(location.hash);
 if(el&&el.classList.contains('card')){{q.value='';active.clear();
  document.querySelectorAll('.chip.on').forEach(c=>{{c.classList.remove('on');c.style.background='';}});apply();
  el.classList.add('open');setTimeout(()=>el.scrollIntoView({{block:'center',behavior:'smooth'}}),60);}}}}
window.addEventListener('hashchange',openHash);openHash();
</script></body></html>"""

open(os.path.join(DOCS,"persons.html"),"w").write(HTML)
print(f"wrote docs/persons.html ({len(HTML)} bytes, {len(persons)} profiles)")
if os.path.isdir(REP):
    open(os.path.join(REP,"PERSONS.html"),"w").write(HTML)
