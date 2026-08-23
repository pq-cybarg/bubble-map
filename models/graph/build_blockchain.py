#!/usr/bin/env python3
"""
build_blockchain.py — Blockchain tab.

A filterable registry of chains / CEX / DEX / stables / foundations / adjudicated
schemes. Sort is on public-record FLAGS (conviction, OFAC, insolvency, custody,
open-source, US listing, documented gov/defense type) — not a legitimacy score.

Reads research/blockchain-registry.json. Writes docs/blockchain.html.
"""
import json, os, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "docs")
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav as _nav

REG = json.load(open(os.path.join(ROOT, "research", "blockchain-registry.json")))
records = REG.get("records", [])
review = REG.get("graph_review", {})
try:
    ENT = set(json.load(open(os.path.join(ROOT, "data", "graph.json"))).get("entities", {}).keys())
except Exception:
    ENT = set()
try:
    PERSONS = {p["name"] for p in json.load(open(os.path.join(ROOT, "data", "persons.json"))).get("persons", [])}
except Exception:
    PERSONS = set()

KIND_LAB = {
    "l1": "L1 protocol", "l2": "L2", "enterprise_dlt": "Enterprise DLT",
    "cex": "CEX", "dex": "DEX", "stablecoin": "Stablecoin",
    "lender": "Custodial lender", "hedge_fund": "Fund",
    "mixer": "Mixer / privacy tool", "adjudicated_scheme": "Adjudicated scheme",
    "oracle": "Oracle", "interop": "Interop", "infra": "Infra / operator",
    "foundation": "Foundation",
}

def slug(s):
    return "b-" + re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")

def pslug(name):
    return "p-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

payload = []
for r in records:
    flags = r.get("flags") or {}
    gov = r.get("gov_or_defense") or []
    gov_kinds = sorted({g.get("kind") for g in gov if g.get("kind")})
    payload.append({
        "id": r["id"],
        "kind": r["kind"],
        "kind_lab": KIND_LAB.get(r["kind"], r["kind"]),
        "launched": r.get("launched"),
        "status": r.get("operating_status"),
        "flags": flags,
        "enforcement": r.get("enforcement") or [],
        "gov": gov,
        "gov_kinds": gov_kinds,
        "leaders": r.get("leaders") or [],
        "foundation": r.get("foundation"),
        "blocks": r.get("blocks") or [],
        "notes": r.get("notes") or "",
        "in_map": r["id"] in ENT or r["id"].replace(".", "_") in ENT,
        "slug": slug(r["id"]),
        "region": r.get("region") or "",
        "venue": r.get("venue") or "",
    })

CSS = """
:root{--cream:#faf8f2;--ink:#1c1b19;--ac:#7b2d26;--link:#1f4e79;--line:#e4ddcc;--mut:#6b665d;--card:#fffdf8}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);font:16.5px/1.55 -apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:8px 18px 72px}
h1{font:600 34px/1.15 Georgia,serif;margin:22px 0 6px}
.deck{color:#33312c;font:18px/1.55 Georgia,serif;margin:0 0 14px}
.lead{background:#f3eedf;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 16px;font:15.5px/1.55 Georgia,serif}
.lead b{color:var(--ac)}
.toolbar{position:sticky;top:52px;z-index:40;background:var(--cream);padding:8px 0 10px;border-bottom:1px solid var(--line);margin-bottom:12px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{border:1px solid #d9d0bc;background:#fff;border-radius:999px;padding:4px 10px;font-size:12.5px;cursor:pointer;color:#4a463f}
.chip.on{background:#1f4e79;color:#fff;border-color:#1f4e79}
.chip.flag.on{background:#7b2d26;border-color:#7b2d26}
input[type=search]{width:100%;max-width:420px;padding:8px 10px;border:1px solid #d9d0bc;border-radius:8px;font:14px/1.4 inherit;background:#fff}
.meta{color:var(--mut);font-size:13px;margin:6px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 13px;cursor:pointer}
.card.open{border-color:#c9b896;box-shadow:0 6px 18px rgba(60,50,30,.08)}
.who{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.nm{font:600 16px/1.25 Georgia,serif}
.kl{color:var(--mut);font-size:12px}
.pills{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 0}
.pill{font-size:10.5px;letter-spacing:.03em;text-transform:uppercase;border-radius:4px;padding:2px 6px;background:#eee8d8;color:#4a463f}
.pill.crim{background:#f4d6d0;color:#7b2d26}
.pill.ofac{background:#eadcf3;color:#5e35b1}
.pill.ins{background:#f3e4c8;color:#8a5a2b}
.pill.ok{background:#dceee3;color:#1f6f43}
.pill.gov{background:#d6e4f2;color:#1f4e79}
.body{display:none;margin-top:10px;font-size:13.5px;color:#33312c;border-top:1px solid var(--line);padding-top:10px}
.card.open .body{display:block}
.row{margin:5px 0}
.row b{color:#1c1b19}
a{color:var(--link);text-decoration:none}
.rev{margin:28px 0 8px;font:600 22px/1.2 Georgia,serif;color:var(--ac)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
td,th{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f3eedf}
footer{color:var(--mut);font:13px/1.5 Georgia,serif;border-top:2px solid var(--line);margin-top:36px;padding-top:14px}
"""

NAV = _nav.navbar("Blockchain", disclaimer=True)
DATA = json.dumps(payload, ensure_ascii=False)
REVIEW = json.dumps(review, ensure_ascii=False)

html_out = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Blockchain registry — Bubble Map</title>
<meta name=description content="Public-record flags for chains, exchanges, DEXes, stables, and adjudicated schemes. Not a legitimacy score.">
<style>{CSS}</style>
</head><body>
{NAV}
<main>
<h1>Blockchain registry</h1>
<p class=deck>Chains, CEXes, DEXes, stables, foundations, and court-found schemes — sorted on <b>public-record flags</b>, not on a good/bad score.</p>
<div class=lead>
A conviction, an OFAC listing, a Chapter-11, a BitLicense, a Boeing council seat, and a Fairshake donation are <b>different facts</b>.
This tab does not collapse them into “legitimate” or “illegitimate.” Pedigree is not validation.
Defense links are typed (<i>contract / council seat / none documented</i>). Intent is not inferred.
Full method: <a href="r-blockchain-registry.html">blockchain-registry</a> · related <a href="r-blockchain-leg.html">blockchain-leg</a>,
<a href="r-altcoin-lens.html">altcoin-lens</a>, <a href="r-spec-crypto-collapse-cluster.html">2022 cascade</a>.
</div>
<div class=toolbar>
<input type=search id=q placeholder="Search name, leader, flag, agency…">
<div class=chips id=kinds></div>
<div class=chips id=regions></div>
<div class=chips id=flags></div>
<div class=meta id=count></div>
</div>
<div class=grid id=grid></div>
<h2 class=rev>Graph hygiene (this pass)</h2>
<p class=deck style="font-size:16px">Bitcoin was not a bubble. Bitfinex/Bybit were sector <code>other</code>.
LayerZero’s bridge UI named “Stargate” is not the AI SPV. Details in the research block.</p>
<div id=review></div>
</main>
<footer>Overlay only — excluded from the financial SCC proofs. Flags are public documents, not character judgments.</footer>
<script>
const ROWS = {DATA};
const REVIEW = {REVIEW};
const KINDS = [...new Set(ROWS.map(r=>r.kind))];
const FLAG_CHIPS = [
  ["adjudicated_criminal","Criminal conviction"],
  ["civil_fraud_judgment","Civil-fraud judgment"],
  ["ofac_sdn","OFAC SDN"],
  ["insolvency_or_bankruptcy","Insolvency"],
  ["open_source_protocol","Open-source protocol"],
  ["custodial","Custodial"],
  ["us_public_company","US public company"],
];
const kindOn = new Set();
const flagOn = new Set();
const regionOn = new Set();
const kindsEl = document.getElementById('kinds');
const flagsEl = document.getElementById('flags');
const regionsEl = document.getElementById('regions');
const REGIONS = [...new Set(ROWS.map(r=>r.region).filter(Boolean))].sort();
REGIONS.forEach(k=>{{
  const b=document.createElement('span'); b.className='chip'; b.textContent=k;
  b.onclick=()=>{{regionOn.has(k)?regionOn.delete(k):regionOn.add(k); b.classList.toggle('on'); draw();}};
  regionsEl.appendChild(b);
}});
KINDS.forEach(k=>{{
  const b=document.createElement('span'); b.className='chip'; b.textContent=k;
  b.onclick=()=>{{kindOn.has(k)?kindOn.delete(k):kindOn.add(k); b.classList.toggle('on'); draw();}};
  kindsEl.appendChild(b);
}});
FLAG_CHIPS.forEach(([id,lab])=>{{
  const b=document.createElement('span'); b.className='chip flag'; b.textContent=lab;
  b.onclick=()=>{{flagOn.has(id)?flagOn.delete(id):flagOn.add(id); b.classList.toggle('on'); draw();}};
  flagsEl.appendChild(b);
}});
function hay(r){{
  return [r.id,r.kind,r.status,r.notes,(r.leaders||[]).map(x=>x.name).join(' '),
    (r.enforcement||[]).map(e=>e.agency+' '+e.outcome).join(' '),
    (r.gov||[]).map(g=>g.kind+' '+g.note).join(' ')].join(' ').toLowerCase();
}}
function pills(r){{
  const f=r.flags||{{}}; const out=[];
  if(f.adjudicated_criminal) out.push(['crim','criminal conviction']);
  if(f.civil_fraud_judgment) out.push(['crim','civil fraud judgment']);
  if(f.ofac_sdn) out.push(['ofac','OFAC SDN']);
  if(f.insolvency_or_bankruptcy) out.push(['ins','insolvent']);
  if(f.open_source_protocol) out.push(['ok','open-source']);
  if(f.custodial) out.push(['ins','custodial']);
  if(f.us_public_company) out.push(['ok','US public co.']);
  (r.gov_kinds||[]).forEach(k=>{{ if(k && k!=='none_documented') out.push(['gov',k.replaceAll('_',' ')]); }});
  if((r.gov_kinds||[]).includes('none_documented') && !(r.gov_kinds||[]).some(k=>k!=='none_documented'))
    out.push(['','no gov/defense doc.']);
  return out.map(([c,t])=>`<span class="pill ${{c}}">${{t}}</span>`).join('');
}}
function usd(n){{ if(n==null) return ''; if(n>=1e9) return '$'+(n/1e9).toFixed(1)+'B'; if(n>=1e6) return '$'+(n/1e6).toFixed(0)+'M'; return '$'+n; }}
function body(r){{
  const enf=(r.enforcement||[]).map(e=>`<div class=row><b>${{e.year}} ${{e.agency}}:</b> ${{e.outcome}} ${{usd(e.amount_usd)}}</div>`).join('')
    || '<div class=row><b>Enforcement:</b> none recorded in this registry</div>';
  const gov=(r.gov||[]).map(g=>`<div class=row><b>${{(g.kind||'').replaceAll('_',' ')}}:</b> ${{g.note}}</div>`).join('');
  const leaders=(r.leaders||[]).map(l=>l.name).join(', ') || '—';
  const blocks=(r.blocks||[]).map(b=>`<a href="r-${{b}}.html">${{b}}</a>`).join(' · ') || '—';
  const map = r.in_map ? `<a href="bubblemap.html#node=${{encodeURIComponent(r.id)}}">open in Bubble Map</a>` : 'not yet a map node (will be after graph rebuild)';
  return `<div class=row><b>Status:</b> ${{r.status}} · launched ${{r.launched||'—'}}</div>
    <div class=row><b>Leaders:</b> ${{leaders}}</div>
    <div class=row><b>Foundation / steward:</b> ${{r.foundation||'—'}}</div>
    ${{enf}}${{gov}}
    <div class=row><b>Notes:</b> ${{r.notes||''}}</div>
    <div class=row><b>Documented in:</b> ${{blocks}}</div>
    <div class=row>${{map}}</div>`;
}}
function draw(){{
  const q=(document.getElementById('q').value||'').toLowerCase();
  const vis=ROWS.filter(r=>{{
    if(kindOn.size && !kindOn.has(r.kind)) return false;
    if(regionOn.size && !regionOn.has(r.region)) return false;
    for(const f of flagOn){{ if(!(r.flags||{{}})[f]) return false; }}
    if(q && !hay(r).includes(q)) return false;
    return true;
  }});
  document.getElementById('count').textContent = vis.length+' of '+ROWS.length+' records';
  document.getElementById('grid').innerHTML = vis.map(r=>`
    <div class=card id="${{r.slug}}" onclick="this.classList.toggle('open')">
      <div class=who><div><div class=nm>${{r.id.replaceAll('_',' ')}}</div><div class=kl>${{r.kind_lab}} · ${{r.status}} · ${{r.region||''}} ${{r.venue||''}}</div></div></div>
      <div class=pills>${{pills(r)}}</div>
      <div class=body>${{body(r)}}</div>
    </div>`).join('');
}}
document.getElementById('q').addEventListener('input', draw);
draw();
(function(){{
  const r=REVIEW;
  const miss=(r.missing_nodes_added||[]).join(', ');
  const sep=(r.not_aliases||[]).map(x=>`<tr><td>${{(x.keep_separate||[]).join(' / ')}}</td><td>${{x.why}}</td></tr>`).join('');
  const corr=(r.sector_corrections||[]).map(x=>`<tr><td>${{x.id}}</td><td>${{x.was}} → ${{x.now}}</td></tr>`).join('');
  document.getElementById('review').innerHTML = `
    <table><thead><tr><th>Keep as separate bubbles</th><th>Why</th></tr></thead><tbody>${{sep}}</tbody></table>
    <p class=meta>Nodes added this pass: ${{miss||'—'}}</p>
    <table><thead><tr><th>Sector correction</th><th></th></tr></thead><tbody>${{corr}}</tbody></table>
    <p class=meta>Still thin: ${{(r.still_missing_or_thin||[]).join(' · ')}}</p>`;
}})();
</script>
</body></html>
"""
# the f-string doubled braces for JS; Python will have consumed {{ -> {
open(os.path.join(DOCS, "blockchain.html"), "w").write(html_out)
print(f"wrote docs/blockchain.html ({len(html_out)} bytes, {len(payload)} records)")
