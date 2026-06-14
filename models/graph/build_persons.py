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

# Optional FEC campaign-finance overlay (data/fec_summary.json from fetch_fec.py). Maps a member's
# display name -> aggregate receipts / PAC totals so the dossier can show the real money on record.
def _load_fec():
    try: F=json.load(open(os.path.join(ROOT,"data","fec_summary.json")))
    except Exception: return {}
    out={}
    for c in F.get("candidates",[]):
        cyc=[x for x in c.get("cycles",[]) if x.get("receipts")]
        if not cyc: continue
        tot=sum(x.get("receipts") or 0 for x in cyc)
        pac=sum(x.get("pac_contributions") or 0 for x in cyc)
        out[c["name"]]={"cid":c.get("candidate_id"),"total":tot,"pac":pac,"n":len(cyc)}
    return out
FEC=_load_fec()
def _usd(v):
    v=v or 0
    if v>=1e9: return f"${v/1e9:.1f}B"
    if v>=1e6: return f"${v/1e6:.1f}M"
    if v>=1e3: return f"${v/1e3:.0f}k"
    return f"${v:.0f}"

DOMAIN_COLORS={"AI":"#1f4e79","Capital":"#7b2d26","Crypto":"#b8860b","Defense":"#2e8b57",
 "Digital-ID":"#5e35b1","State/Policy":"#c0392b","Macro/Finance":"#138a8a","Sovereign":"#d35400",
 "Geopolitics":"#8a5a2b","Markets":"#6b3b16",
 "Regulator":"#1b6b6b","Executive":"#8e2b1b","Judiciary":"#4a3f8a",
 "Intelligence":"#37474f","Legislature":"#7a4a6e"}
def dcolor(d): return DOMAIN_COLORS.get(d,"#6b665d")

def _navlinks(active=""):
    items=[("index.html","Home"),("dashboard.html","Dashboard"),("charts.html","Charts"),("research.html","Research"),
           ("persons.html","Persons"),("bubblemap.html","Bubble Map"),("globe.html","Globe"),
           ("methodology.html","Methodology"),("glossary.html","Glossary"),
           ("https://github.com/pq-cybarg/bubble-map","Source ↗")]
    a=lambda h,t:f'<a href="{h}" style="color:{"#7b2d26" if t==active else "#1f4e79"};text-decoration:none;margin:0 9px;white-space:nowrap;font-weight:{700 if t==active else 400}">{html.escape(t)}</a>'
    return ('<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:11px 16px;'
            'font:13.5px/1.7 -apple-system,Segoe UI,Roboto,sans-serif;text-align:center">'+"".join(a(h,t) for h,t in items)+'</div>')
NAV=_navlinks("Persons")

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
#segnav{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.segchip{font-size:12px;padding:4px 10px;border-radius:7px;border:1px solid var(--line);background:var(--paper);color:#33312c;text-decoration:none;cursor:pointer}
.segchip:hover{background:#1f4e7910;border-color:var(--ac2)}.segchip b{color:var(--ac2);margin-left:3px}
.segtools{font-size:12px;color:var(--ac2);margin-top:7px}.segtools span{cursor:pointer}.segtools span:hover{text-decoration:underline}
.seg{margin:18px 0 4px;scroll-margin-top:140px}
.seghdr{font:600 15px Georgia,serif;color:#2a2823;margin:0 0 6px;padding:7px 2px;border-bottom:2px solid var(--line);cursor:pointer;user-select:none;position:sticky;top:0;background:var(--bg);z-index:2}
.seghdr .caret{display:inline-block;transition:transform .15s;color:var(--mut);font-size:12px}
.seg.collapsed .caret{transform:rotate(-90deg)}.seg.collapsed .segbody{display:none}
.segcount{font:600 12px -apple-system,sans-serif;color:#fff;background:var(--ac2);border-radius:10px;padding:1px 8px;margin-left:6px;vertical-align:1px}
.seg.nomatch{display:none}
@keyframes pop{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
.card.pop{animation:pop .2s ease}
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

# ---- segmentation: assign each profile ONE primary segment (priority order) for the roster view ----
SEG_DEFS=[
 ("regulators","Financial regulators — Fed · Treasury · SEC · CFTC · FDIC · OCC",lambda d:"Regulator" in d),
 ("executive","Executive — Presidents & administrations",lambda d:"Executive" in d),
 ("judiciary","Judiciary — the Supreme Court",lambda d:"Judiciary" in d),
 ("intelligence","Intelligence — CIA · FBI · DNI",lambda d:"Intelligence" in d),
 ("legislature","Congress — leadership, committees & members",lambda d:"Legislature" in d),
 ("ai","AI labs, hyperscalers & chips",lambda d:"AI" in d),
 ("crypto","Crypto & stablecoins",lambda d:"Crypto" in d),
 ("capital","Capital, markets & macro-finance",lambda d:any(x in d for x in ("Capital","Markets","Macro/Finance"))),
 ("defense","Defense & security",lambda d:"Defense" in d),
 ("digitalid","Digital-ID & surveillance",lambda d:"Digital-ID" in d),
 ("sovereign","Sovereign wealth & Gulf capital",lambda d:"Sovereign" in d),
 ("geopolitics","Heads of state & geopolitics",lambda d:"Geopolitics" in d),
 ("statepolicy","State & policy",lambda d:"State/Policy" in d),
 ("other","Other",lambda d:True),
]
def segments_of(p):
    """ALL segments a person belongs to (a person in multiple domains shows under EACH category).
    'other' only if nothing else matches."""
    d=set(p.get("domains",[]))
    segs=[k for k,_lab,test in SEG_DEFS if k!="other" and test(d)]
    return segs or ["other"]
def segment_of(p):  # primary segment = first match (kept for the avatar colour etc.)
    return segments_of(p)[0]
SEG_LABEL={k:lab for k,lab,_ in SEG_DEFS}

def card_html(i,p,seg=None,primary=True):
    doms=p.get("domains",[])
    if seg is None: seg=segment_of(p)
    tags="".join(f'<span class=tag style="background:{dcolor(d)}">{html.escape(d)}</span>' for d in doms)
    body=[]
    for k,lab in FIELDS:
        v=p.get(k)
        if not v: continue
        cls="fld bluf" if k=="bluf" else "fld"
        body.append(f'<div class="{cls}"><div class=lab>{lab}</div><div class=val>{html.escape(str(v))}</div></div>')
    fec=FEC.get(p.get("name",""))
    if fec:
        body.append(f'<div class="fld"><div class=lab>Campaign finance (FEC, primary)</div>'
                    f'<div class=val>~{_usd(fec["total"])} total receipts across {fec["n"]} cycles; '
                    f'~{_usd(fec["pac"])} from PACs &middot; FEC candidate <code>{html.escape(fec["cid"] or "")}</code>. '
                    f'<span style="color:#6b665d">Public FEC totals (api.open.fec.gov); industry/sector breakdown requires itemized-receipt ingest — money is leverage/exposure, not proof of a quid pro quo (see r-influence-congress-funding-compromise).</span></div></div>')
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
    base=slug(p.get("name",""))
    cid=base if primary else f'{base}--{seg}'   # primary keeps the canonical anchor; duplicates get unique ids
    return (f'<div class=card id="{cid}" data-person="{base}" data-seg="{seg}" data-domains="{html.escape("|".join(doms))}" data-hay="{hay}">'
            f'<div class=row onclick="this.parentNode.classList.toggle(\'open\')">'
            f'<div class=av style="background:{av}">{html.escape(initials(p.get("name","?")))}</div>'
            f'<div class=who><div class=nm>{html.escape(p.get("name",""))}</div>'
            f'<div class=rl>{html.escape(p.get("role",""))}</div>'
            f'<div class=tags>{tags}</div></div>'
            f'<div class=exp>&#9656;</div></div>'
            f'<div class=body>{"".join(body)}</div></div>')

alldoms=sorted({d for p in persons for d in p.get("domains",[])})
chips="".join(f'<span class=chip data-d="{html.escape(d)}" style="--c:{dcolor(d)}">{html.escape(d)}</span>' for d in alldoms)
# group profiles into segments (MULTI-category: a person shows under EVERY segment they belong to),
# preserving SEG_DEFS order. The first segment is 'primary' (keeps the canonical #anchor id).
from collections import defaultdict as _dd
_buckets=_dd(list)
for i,p in enumerate(persons):
    segs=segments_of(p)
    for k in segs: _buckets[k].append((i,p,k==segs[0]))
seg_order=[k for k,_,_ in SEG_DEFS if _buckets.get(k)]
segnav="".join(f'<a class=segchip href="#seg-{k}" data-seg="{k}">{html.escape(SEG_LABEL[k])}<b>{len(_buckets[k])}</b></a>' for k in seg_order)
sections=""
for k in seg_order:
    body_cards="".join(card_html(i,p,k,primary) for i,p,primary in _buckets[k])
    sections+=(f'<section class=seg id="seg-{k}" data-seg="{k}">'
               f'<h3 class=seghdr onclick="this.parentNode.classList.toggle(\'collapsed\')">'
               f'<span class=caret>&#9662;</span> {html.escape(SEG_LABEL[k])}'
               f'<span class=segcount>{len(_buckets[k])}</span></h3>'
               f'<div class=segbody>{body_cards}</div></section>')

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
<div id=segnav>{segnav}</div>
<div class=segtools><span id=expandAll>Expand all</span> &middot; <span id=collapseAll>Collapse all</span> &middot; <span class=sub>{len(seg_order)} segments</span></div>
</div>
<div class=count id=count></div>
<div id=list>{sections}</div>
<div class=empty id=empty style="display:none">No matching profiles.</div>
</div>
<footer>Behavioral &amp; strategic assessments from the public record &middot; not clinical diagnosis &middot; inference labeled, facts cited &middot; excluded from the formal proofs &middot; contact resistant@tuta.com</footer>
<script>
const cards=[...document.querySelectorAll('.card')], q=document.getElementById('q'),
 count=document.getElementById('count'), empty=document.getElementById('empty'),
 sections=[...document.querySelectorAll('.seg')];
let active=new Set(), searching=false, booted=false;
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{{
 const d=c.dataset.d;
 if(active.has(d)){{active.delete(d);c.classList.remove('on');c.style.background='';}}
 else{{active.add(d);c.classList.add('on');c.style.background=c.style.getPropertyValue('--c');}}
 apply();}}));
q.addEventListener('input',apply);
// show a card with a one-shot fade-in only when it newly appears (cheap + smooth)
function setShown(card,show){{
 if(show){{ if(booted && card.style.display==='none'){{card.classList.add('pop');
   card.addEventListener('animationend',()=>card.classList.remove('pop'),{{once:true}});}} card.style.display=''; }}
 else card.style.display='none';
}}
const TOTAL_PEOPLE=new Set(cards.map(c=>c.dataset.person)).size;  // distinct persons (cards are multi-category)
function apply(){{
 const s=q.value.trim().toLowerCase(); searching=!!s||active.size>0; const shownPeople=new Set();
 cards.forEach(card=>{{
  const okText=!s||card.dataset.hay.includes(s);
  const doms=card.dataset.domains.split('|');
  const okDom=active.size===0||[...active].every(d=>doms.includes(d));
  const show=okText&&okDom; setShown(card,show); if(show)shownPeople.add(card.dataset.person);
 }});
 // per-section counts; hide empty sections; auto-expand sections with matches while searching
 sections.forEach(sec=>{{
  const vis=[...sec.querySelectorAll('.card')].filter(c=>c.style.display!=='none').length;
  sec.classList.toggle('nomatch',vis===0);
  sec.querySelector('.segcount').textContent=vis;
  if(searching) sec.classList.remove('collapsed');
 }});
 const n=shownPeople.size;
 count.textContent=n+' of '+TOTAL_PEOPLE+' people'+(searching?' (filtered) · people appear under every category they belong to':' · shown under every category they belong to');
 empty.style.display=n?'none':'block';
}}
apply(); booted=true;
document.getElementById('expandAll').onclick=()=>sections.forEach(s=>s.classList.remove('collapsed'));
document.getElementById('collapseAll').onclick=()=>sections.forEach(s=>s.classList.add('collapsed'));
// segnav chip -> expand + smooth-scroll to its section
document.querySelectorAll('.segchip').forEach(a=>a.addEventListener('click',e=>{{e.preventDefault();
 const sec=document.getElementById('seg-'+a.dataset.seg); if(!sec)return;
 sec.classList.remove('collapsed','nomatch'); sec.scrollIntoView({{behavior:'smooth',block:'start'}});}}));
function openHash(){{if(!location.hash)return;const el=document.querySelector(location.hash);
 if(el&&el.classList.contains('card')){{q.value='';active.clear();
  document.querySelectorAll('.chip.on').forEach(c=>{{c.classList.remove('on');c.style.background='';}});apply();
  const sec=el.closest('.seg'); if(sec){{sec.classList.remove('collapsed','nomatch');}}
  el.classList.add('open');setTimeout(()=>el.scrollIntoView({{block:'center',behavior:'smooth'}}),80);}}}}
window.addEventListener('hashchange',openHash);openHash();
</script></body></html>"""

open(os.path.join(DOCS,"persons.html"),"w").write(HTML)
print(f"wrote docs/persons.html ({len(HTML)} bytes, {len(persons)} profiles)")
if os.path.isdir(REP):
    open(os.path.join(REP,"PERSONS.html"),"w").write(HTML)
