#!/usr/bin/env python3
"""
build_blockchain.py — Blockchain tab.

Public-record flags (conviction / OFAC / insolvency / custody) plus a scraped
Quantum Readiness Index (qrindex.org) join. QRI is a third-party, AI-assisted,
pre-release score — not a legitimacy verdict and not a proof.

Writes docs/blockchain.html.
"""
import json, os, re, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "docs")
sys_path_insert = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, sys_path_insert)
import nav as _nav

REG = json.load(open(os.path.join(ROOT, "research", "blockchain-registry.json")))
records = REG.get("records", [])
try:
    QRI = json.load(open(os.path.join(ROOT, "data", "qri_index.json")))
except Exception:
    QRI = {}
projects = QRI.get("projects") or {}
MAP = QRI.get("map") or {}
try:
    ENT = set(json.load(open(os.path.join(ROOT, "data", "graph.json"))).get("entities", {}).keys())
except Exception:
    ENT = set()

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

SOLANA_DEX = {"Jupiter","Raydium","Orca","Phoenix","Drift","Meteora","PumpSwap"}
HOST_CHAIN = {
    "cex": ["Bitcoin", "Ethereum"],
    "lender": ["Bitcoin", "Ethereum"],
    "stablecoin": ["Ethereum"],
}

def project_by_slug(slug):
    return projects.get(slug) if slug else None

def qri_for(rec):
    rid = rec.get("id") or ""
    mapped = MAP.get(rid)
    cand = []
    if mapped:
        cand.append(mapped)
    cand.append(rid.lower().replace("_", "-"))
    cand.append(rid.lower())
    if rid == "XRPL":
        cand.extend(["xrp", "ripple"])
    if rid == "TON":
        cand.extend(["toncoin", "the-open-network"])
    if rid == "BNB_Chain":
        cand.extend(["bnb", "binancecoin"])
    if rid == "QRL_Foundation":
        cand.append("quantum-resistant-ledger")
    for c in cand:
        if c in projects:
            return projects[c]
    name = (rid or "").replace("_", " ").lower()
    for p in projects.values():
        pn = (p.get("project_name") or "").lower()
        sy = (p.get("symbol") or "").lower()
        if pn == name or sy == rid.lower() or pn.replace(" ", "-") == rid.lower().replace("_", "-"):
            return p
        if rid == "QRL" and "quantum resistant" in pn:
            return p
        if rid in ("XRPL", "Ripple") and "xrp ledger" in pn:
            return p
    return None

def pack_qri(q):
    if not q:
        return None
    stage = q.get("qri_stage")
    try:
        stage = int(stage) if stage is not None else None
    except Exception:
        stage = None
    return {
        "slug": q.get("slug"),
        "score": q.get("qri_score"),
        "stage": stage,
        "stage_label": q.get("stage_label") or "",
        "confidence": q.get("confidence") or "",
        "evaluated": q.get("evaluated") or "",
        "url": q.get("canonical_url") or "",
        "summary": q.get("summary") or "",
        "symbol": q.get("symbol") or "",
        "type": q.get("project_type") or "",
    }

def inherited_for(rec):
    rid = rec.get("id") or ""
    kind = rec.get("kind")
    hosts = []
    if kind == "dex":
        hosts = ["Solana"] if rid in SOLANA_DEX else ["Ethereum"]
        if rid in {"Osmosis","THORChain","Maya_Protocol","dYdX_v4"}:
            hosts = ["Cosmos"]
        if rid in {"PancakeSwap"}:
            hosts = ["BNB_Chain"]
        if rid in {"SunSwap"}:
            hosts = ["TRON"]
    elif kind in HOST_CHAIN:
        hosts = list(HOST_CHAIN[kind])
        if rid in {"RLUSD"}:
            hosts = ["XRPL", "Ethereum"]
        if rid in {"Tether"}:
            hosts = ["TRON", "Ethereum", "Bitcoin"]
    out = []
    for h in hosts:
        fake = {"id": h}
        q = pack_qri(qri_for(fake))
        if q:
            q["host"] = h
            out.append(q)
    return out

payload = []
for r in records:
    flags = r.get("flags") or {}
    gov = r.get("gov_or_defense") or []
    gov_kinds = sorted({g.get("kind") for g in gov if g.get("kind")})
    qri = pack_qri(qri_for(r))
    inherited = inherited_for(r) if not qri else []
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
        "qri": qri,
        "qri_inherited": inherited,
        "highlight": r["id"] == "QRL",
    })

# QRI ranking table (all scraped projects, not only registry)
qri_rank = sorted(
    [
        {
            "slug": p.get("slug"),
            "name": p.get("project_name"),
            "symbol": p.get("symbol") or "",
            "score": p.get("qri_score"),
            "stage": p.get("qri_stage"),
            "stage_label": p.get("stage_label") or "",
            "url": p.get("canonical_url") or "",
            "type": p.get("project_type") or "",
            "evaluated": p.get("evaluated") or "",
        }
        for p in projects.values()
        if p.get("qri_score") is not None
    ],
    key=lambda x: (-(x["score"] or 0), x.get("name") or ""),
)
qri_meta = {
    "fetched_at": QRI.get("fetched_at") or "",
    "source": QRI.get("source") or "none",
    "n": QRI.get("n_projects") or len(projects),
    "n_stage4": QRI.get("n_stage4") or sum(1 for p in projects.values() if (p.get("qri_stage") or 0) >= 4),
    "disclaimer": QRI.get("disclaimer") or "",
}

CSS = """
:root{--cream:#faf8f2;--ink:#1c1b19;--ac:#7b2d26;--link:#1f4e79;--line:#e4ddcc;--mut:#6b665d;--card:#fffdf8;--pq:#1f6f43}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);font:16.5px/1.55 -apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1120px;margin:0 auto;padding:8px 18px 72px}
h1{font:600 34px/1.15 Georgia,serif;margin:22px 0 6px}
h2{font:600 22px/1.2 Georgia,serif;color:var(--ac);margin:36px 0 8px;padding-top:8px;border-top:2px solid var(--line)}
.deck{color:#33312c;font:18px/1.55 Georgia,serif;margin:0 0 14px}
.lead{background:#f3eedf;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 16px;font:15.5px/1.55 Georgia,serif}
.lead b{color:var(--ac)}
.callout{background:#e8f4ec;border:1px solid #b7d4c0;border-radius:10px;padding:16px 18px;margin:0 0 18px}
.callout h2{border:0;margin:0 0 6px;padding:0;color:var(--pq);font-size:20px}
.callout .score{font:700 28px/1 Georgia,serif;color:var(--pq)}
.toolbar{position:sticky;top:52px;z-index:40;background:var(--cream);padding:8px 0 10px;border-bottom:1px solid var(--line);margin-bottom:12px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{border:1px solid #d9d0bc;background:#fff;border-radius:999px;padding:4px 10px;font-size:12.5px;cursor:pointer;color:#4a463f}
.chip.on{background:#1f4e79;color:#fff;border-color:#1f4e79}
.chip.flag.on{background:#7b2d26;border-color:#7b2d26}
.chip.qri.on{background:#1f6f43;border-color:#1f6f43}
input[type=search]{width:100%;max-width:420px;padding:8px 10px;border:1px solid #d9d0bc;border-radius:8px;font:14px/1.4 inherit;background:#fff}
.meta{color:var(--mut);font-size:13px;margin:6px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 13px;cursor:pointer}
.card.open{border-color:#c9b896;box-shadow:0 6px 18px rgba(60,50,30,.08)}
.card.hl{border-color:#1f6f43;box-shadow:0 0 0 2px rgba(31,111,67,.18)}
.who{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.nm{font:600 16px/1.25 Georgia,serif}
.kl{color:var(--mut);font-size:12px}
.qrib{font:700 20px/1 Georgia,serif;color:#1f4e79;min-width:2.4em;text-align:right}
.qrib.s4{color:var(--pq)}
.qrib.s3{color:#2e7d32}
.qrib.s2{color:#8a5a2b}
.qrib.s1,.qrib.s0{color:#7b2d26}
.qrib.na{color:#8a8378;font-weight:500;font-size:13px}
.pills{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 0}
.pill{font-size:10.5px;letter-spacing:.03em;text-transform:uppercase;border-radius:4px;padding:2px 6px;background:#eee8d8;color:#4a463f}
.pill.crim{background:#f4d6d0;color:#7b2d26}
.pill.ofac{background:#eadcf3;color:#5e35b1}
.pill.ins{background:#f3e4c8;color:#8a5a2b}
.pill.ok{background:#dceee3;color:#1f6f43}
.pill.gov{background:#d6e4f2;color:#1f4e79}
.pill.pq{background:#dceee3;color:#1f6f43}
.body{display:none;margin-top:10px;font-size:13.5px;color:#33312c;border-top:1px solid var(--line);padding-top:10px}
.card.open .body{display:block}
.row{margin:5px 0}
.row b{color:#1c1b19}
a{color:var(--link);text-decoration:none}
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:10px 0 18px}
td,th{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f3eedf}
tr.s4{background:#eef6f0}
footer{color:var(--mut);font:13px/1.5 Georgia,serif;border-top:2px solid var(--line);margin-top:36px;padding-top:14px}
.note{font:15.5px/1.55 Georgia,serif;color:#33312c}
"""

NAV = _nav.navbar("Blockchain", disclaimer=True)
DATA = json.dumps(payload, ensure_ascii=False)
QRANK = json.dumps(qri_rank, ensure_ascii=False)
QMETA = json.dumps(qri_meta, ensure_ascii=False)
fetched = H.escape((qri_meta.get("fetched_at") or "")[:19].replace("T", " ") + " UTC")
src = H.escape(qri_meta.get("source") or "unfetched")

html_out = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Blockchain registry — Bubble Map</title>
<meta name=description content="Chains, venues, public-record flags, and scraped quantum-readiness scores. Not a legitimacy rating.">
<style>{CSS}</style>
</head><body>
{NAV}
<main>
<h1>Blockchain registry</h1>
<p class=deck>Public-record flags for chains and venues, plus a <b>quantum-readiness</b> join from the Blockchain Quantum Readiness Index. Not a good/bad score.</p>

<div class="callout" id="qrl">
  <h2>Quantum-ready reference: QRL</h2>
  <p><span class="score" id="qrl-score">—</span> <span id="qrl-stage"></span></p>
  <p class=note>The Quantum Resistant Ledger is the only large-theme L1 in this corpus that was <b>post-quantum at genesis</b> (mandatory XMSS, NIST SP 800-208). Bitcoin, Ethereum, and almost every other production chain still authorize spend with ECDSA/Schnorr — harvest-now, forge-later. QRI Stage 4 is a <i>cryptographic-readiness</i> fact. It is not an adoption, liquidity, or token-accrual claim (<a href="r-altcoin-lens.html">altcoin-lens</a> remains the utility axis; <a href="r-spec-blockchain-ecosystem.html">spec-blockchain-ecosystem</a> is the TNFL write-up).</p>
  <p class=meta>Source: <a href="https://qrindex.org/projects/quantum-resistant-ledger/">qrindex.org / quantum-resistant-ledger</a> · scraped {fetched} ({src}). Index is AI-assisted and pre-release.</p>
</div>

<div class=lead>
A conviction, an OFAC listing, a bankruptcy, a BitLicense, a Boeing council seat, and a Fairshake donation are <b>different facts</b>.
This tab does not collapse them into “legitimate.” Pedigree is not validation. Defense links are typed.
Quantum-readiness is a third axis, scraped from <a href="https://qrindex.org/">qrindex.org</a> (no stable API; HTML is expected to change).
Method: <a href="r-blockchain-registry.html">blockchain-registry</a> ·
<a href="r-blockchain-leg.html">blockchain-leg</a> ·
<a href="r-macro-pqc-chips.html">macro-pqc-chips</a> ·
<a href="r-macro-crqc-quantum-landscape.html">macro-crqc</a>.
</div>

<div class=toolbar>
<input type=search id=q placeholder="Search name, leader, QRI, agency…">
<div class=chips id=qristages></div>
<div class=chips id=kinds></div>
<div class=chips id=regions></div>
<div class=chips id=flags></div>
<div class=meta id=count></div>
</div>
<div class=grid id=grid></div>

<h2>Quantum readiness (scraped index)</h2>
<p class=note>Every index row is listed. Stage 4 = migration complete / quantum-ready on the index’s own rubric. Bitcoin (~20, Stage 2) and Ethereum (~17, Stage 2) have <i>proposals</i> (BIP-360/361, EF 2029 talk) and still sign with ECC in production. CEX/DEX cards without their own score show <b>host-chain QRI</b> as an exposure note — a BitLicense does not migrate ECDSA.</p>
<p class=meta id="qri-meta"></p>
<table>
<thead><tr><th>#</th><th>QRI</th><th>Project</th><th>Stage</th><th>Type</th></tr></thead>
<tbody id="qri-body"></tbody>
</table>

<h2>How to read the three axes</h2>
<p class=note><b>Public-record flags</b> (cards) = court, OFAC, insolvency, custody, listing. <b>QRI</b> (pills / table) = third-party quantum-attack readiness of production cryptography. <b>altcoin-lens</b> = institutional utility vs token-accrual. A Stage-4 chain can be illiquid. A NYDFS-licensed CEX can be fully ECC-exposed. FTX’s conviction is not a property of Ethereum.</p>
<p class=note>ECDSA/Schnorr over secp256k1 is the default spend-auth of BTC, ETH, SOL, XRP, and most L2s. A cryptographically relevant quantum computer derives the private key from a <i>revealed</i> public key. Address reuse and P2PK outputs make that exposure permanent. That is the harvest-now / forge-later (TNFL) problem in <a href="r-spec-blockchain-ecosystem.html">the ecosystem block</a> — QRL does not have it on native spend.</p>

<h2>Foundations and stewards</h2>
<p class=note>A foundation is not the token holders and not the exchange that lists the token. These are the steward names attached to registry rows (public bios / corporate sites). Empty means the row is a protocol, a defunct venue, or we have not yet attached a steward without guessing.</p>
<table>
<thead><tr><th>Steward</th><th>Registry rows</th></tr></thead>
<tbody id="found-body"></tbody>
</table>

<h2>Map notes</h2>
<p class=note>Bitcoin the protocol was missing as a bubble (only the US reserve, a think tank, and IBIT existed). Bitfinex and Bybit were mis-bucketed as <code>other</code>. Keep un-aliased: Ripple / XRPL / Ripple Prime / XRPLF; Ethereum / Foundation / ConsenSys / Infura; AI Stargate vs LayerZero’s bridge app also named Stargate; Binance vs Binance.US vs Binance.TR. Overlay edges into LayerZero/Palantir/Google are not used here — they close cycles with the financial SCC. Venue rows on this tab do not all become map bubbles.</p>

</main>
<footer>Overlay research. Flags are public documents. QRI is scraped from qrindex.org and will break when their markup changes — the fetcher is written for that. Nothing here is financial advice or an accusation of wrongdoing.</footer>
<script>
const ROWS = {DATA};
const QRANK = {QRANK};
const QMETA = {QMETA};
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
const qriOn = new Set();
const kindsEl = document.getElementById('kinds');
const flagsEl = document.getElementById('flags');
const regionsEl = document.getElementById('regions');
const qriEl = document.getElementById('qristages');
[['s4','QRI Stage 4 (quantum-ready)'],['s3','Stage 3 (migration live)'],['s2','Stage 2'],['s1','Stage 1'],['s0','Stage 0'],['none','No QRI join']].forEach(([id,lab])=>{{
  const b=document.createElement('span'); b.className='chip qri'; b.textContent=lab;
  b.onclick=()=>{{qriOn.has(id)?qriOn.delete(id):qriOn.add(id); b.classList.toggle('on'); draw();}};
  qriEl.appendChild(b);
}});
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
  const q=r.qri||{{}};
  return [r.id,r.kind,r.status,r.notes,(r.leaders||[]).map(x=>x.name).join(' '),
    (r.enforcement||[]).map(e=>e.agency+' '+e.outcome).join(' '),
    q.score,q.stage_label,q.summary,q.symbol].join(' ').toLowerCase();
}}
function pills(r){{
  const f=r.flags||{{}}; const out=[];
  if(r.highlight) out.push(['pq','PQ-native (XMSS)']);
  const q=r.qri;
  if(q && q.stage===4) out.push(['pq','QRI stage 4']);
  else if(q && q.stage===3) out.push(['ok','QRI stage 3']);
  if(f.adjudicated_criminal) out.push(['crim','criminal conviction']);
  if(f.civil_fraud_judgment) out.push(['crim','civil fraud judgment']);
  if(f.ofac_sdn) out.push(['ofac','OFAC SDN']);
  if(f.insolvency_or_bankruptcy) out.push(['ins','insolvent']);
  if(f.open_source_protocol) out.push(['ok','open-source']);
  if(f.custodial) out.push(['ins','custodial']);
  if(f.us_public_company) out.push(['ok','US public co.']);
  (r.gov_kinds||[]).forEach(k=>{{ if(k && k!=='none_documented') out.push(['gov',k.replaceAll('_',' ')]); }});
  return out.map(([c,t])=>`<span class="pill ${{c}}">${{t}}</span>`).join('');
}}
function usd(n){{ if(n==null) return ''; if(n>=1e9) return '$'+(n/1e9).toFixed(1)+'B'; if(n>=1e6) return '$'+(n/1e6).toFixed(0)+'M'; return '$'+n; }}
function qriBadge(r){{
  const q=r.qri;
  if(!q || q.score==null) return '<div class="qrib na">no QRI</div>';
  const sc=typeof q.score==='number'? (q.score%1? q.score.toFixed(1): q.score): q.score;
  return `<div class="qrib s${{q.stage}}">${{sc}}</div>`;
}}
function body(r){{
  const q=r.qri;
  const inh=(r.qri_inherited||[]).map(h=>`${{h.host}} ${{h.score}} (stage ${{h.stage}})`).join('; ');
  const qblock = q ? `<div class=row><b>QRI (this asset/chain):</b> ${{q.score}} / 100 · Stage ${{q.stage}} (${{q.stage_label||''}})
    · ${{q.confidence||'confidence n/a'}} · evaluated ${{q.evaluated||'—'}}
    · <a href="${{q.url}}" target="_blank" rel="noopener">qrindex report</a></div>
    <div class=row>${{q.summary||''}}</div>`
    : (inh
        ? `<div class=row><b>QRI:</b> no venue-level score. Host-chain QRI (spend-auth of listed assets, not a CEX/DEX rating): ${{inh}}. A licensed venue can be fully ECC-exposed.</div>`
        : '<div class=row><b>QRI:</b> not in the scraped index.</div>');
  const enf=(r.enforcement||[]).map(e=>`<div class=row><b>${{e.year}} ${{e.agency}}:</b> ${{e.outcome}} ${{usd(e.amount_usd)}}</div>`).join('')
    || '<div class=row><b>Enforcement:</b> none recorded in this registry</div>';
  const gov=(r.gov||[]).map(g=>`<div class=row><b>${{(g.kind||'').replaceAll('_',' ')}}:</b> ${{g.note}}</div>`).join('');
  const leaders=(r.leaders||[]).map(l=>l.name).join(', ') || '—';
  const blocks=(r.blocks||[]).map(b=>`<a href="r-${{b}}.html">${{b}}</a>`).join(' · ') || '—';
  const map = r.in_map ? `<a href="bubblemap.html#node=${{encodeURIComponent(r.id)}}">open in Bubble Map</a>` : 'not a map node (tab row only — overlay edges that would cycle the SCC are omitted)';
  return `${{qblock}}
    <div class=row><b>Status:</b> ${{r.status}} · launched ${{r.launched||'—'}}</div>
    <div class=row><b>Leaders:</b> ${{leaders}}</div>
    <div class=row><b>Foundation / steward:</b> ${{r.foundation||'—'}}</div>
    ${{enf}}${{gov}}
    <div class=row><b>Notes:</b> ${{r.notes||''}}</div>
    <div class=row><b>Documented in:</b> ${{blocks}}</div>
    <div class=row>${{map}}</div>`;
}}
function qriKey(r){{
  if(!r.qri) return 'none';
  return 's'+r.qri.stage;
}}
function draw(){{
  const q=(document.getElementById('q').value||'').toLowerCase();
  const vis=ROWS.filter(r=>{{
    if(kindOn.size && !kindOn.has(r.kind)) return false;
    if(regionOn.size && !regionOn.has(r.region)) return false;
    if(qriOn.size && !qriOn.has(qriKey(r))) return false;
    for(const f of flagOn){{ if(!(r.flags||{{}})[f]) return false; }}
    if(q && !hay(r).includes(q)) return false;
    return true;
  }}).sort((a,b)=>{{
    const as=a.qri&&a.qri.score!=null?a.qri.score:-1;
    const bs=b.qri&&b.qri.score!=null?b.qri.score:-1;
    if(bs!==as) return bs-as;
    if(a.highlight!==b.highlight) return a.highlight?-1:1;
    return a.id.localeCompare(b.id);
  }});
  document.getElementById('count').textContent = vis.length+' of '+ROWS.length+' records (sorted by QRI when joined)';
  document.getElementById('grid').innerHTML = vis.map(r=>`
    <div class="card ${{r.highlight?'hl':''}}" id="${{r.slug}}" onclick="this.classList.toggle('open')">
      <div class=who>
        <div><div class=nm>${{r.id.replaceAll('_',' ')}}</div>
        <div class=kl>${{r.kind_lab}} · ${{r.status}}${{r.qri? ' · '+ (r.qri.stage_label||('stage '+r.qri.stage)): ''}}</div></div>
        ${{qriBadge(r)}}
      </div>
      <div class=pills>${{pills(r)}}</div>
      <div class=body>${{body(r)}}</div>
    </div>`).join('');
}}
document.getElementById('q').addEventListener('input', draw);
draw();

(function(){{
  const qrl=ROWS.find(r=>r.id==='QRL');
  if(qrl&&qrl.qri){{
    const sc=qrl.qri.score;
    document.getElementById('qrl-score').textContent = (typeof sc==='number'?(sc%1?sc.toFixed(1):sc):sc)+' / 100';
    document.getElementById('qrl-stage').textContent = 'Stage '+(qrl.qri.stage)+' — '+(qrl.qri.stage_label||'Migration complete / quantum-ready');
  }} else {{
    const row=QRANK.find(x=>(x.symbol||'').toUpperCase()==='QRL' || /quantum resistant/i.test(x.name||''));
    if(row){{
      document.getElementById('qrl-score').textContent = row.score+' / 100';
      document.getElementById('qrl-stage').textContent = 'Stage '+row.stage+' — '+(row.stage_label||'');
    }}
  }}
  document.getElementById('qri-meta').textContent =
    (QMETA.n||0)+' projects scraped · '+(QMETA.n_stage4||0)+' Stage 4 · '+
    (QMETA.source||'')+' · '+(QMETA.fetched_at||'').slice(0,19).replace('T',' ')+' UTC. '+
    'Scores are not market ratings.';
  const fnd={{}};
  ROWS.forEach(r=>{{ const f=(r.foundation||'').trim(); if(f && f!=='—' && f.toLowerCase()!=='none'){{ (fnd[f]=fnd[f]||[]).push(r.id); }} }});
  document.getElementById('found-body').innerHTML = Object.keys(fnd).sort().map(k=>
    `<tr><td>${{k}}</td><td>${{fnd[k].map(id=>id.replaceAll('_',' ')).join(', ')}}</td></tr>`).join('');
  document.getElementById('qri-body').innerHTML = QRANK.map((r,i)=>`
    <tr class="${{r.stage===4?'s4':''}}">
      <td>${{i+1}}</td>
      <td><b>${{r.score}}</b></td>
      <td><a href="${{r.url}}" target="_blank" rel="noopener">${{r.name}}</a> ${{r.symbol? '<small>'+r.symbol+'</small>':''}}</td>
      <td>Stage ${{r.stage}} — ${{r.stage_label||''}}</td>
      <td>${{r.type||''}}</td>
    </tr>`).join('');
}})();
</script>
</body></html>
"""
open(os.path.join(DOCS, "blockchain.html"), "w").write(html_out)
joined = sum(1 for r in payload if r.get("qri"))
print(f"wrote docs/blockchain.html ({len(html_out)} bytes, {len(payload)} records, {joined} with QRI, {len(qri_rank)} index rows)")
