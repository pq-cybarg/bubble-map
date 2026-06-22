#!/usr/bin/env python3
"""
build_bubblemap.py - the interactive 'Bubble Map' the project is named for: a draggable, zoomable
d3 force-directed graph of data/graph.json (189 entities / 198 directed edges). Nodes sized by
degree, colored by sector-bucket; financial edges solid, structural edges faint/dashed; the
circular core (Tarjan SCC) ring-highlighted. Click a bubble for a detail panel (sector, neighbours,
the research blocks documenting it, and any matching Persons-of-Interest profile). Self-contained
HTML (d3 v7 from CDN; data embedded), light academic theme, shared nav. Writes docs/bubblemap.html.
"""
import json, os, html, glob
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs"); REP=os.path.join(ROOT,"report")
_MD_HAVE=set(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ROOT,"research","*.md")))

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
 "pqc":["pqc_quantum","research"], "person":["person"], "other":["other","spv","offshore"] }
BUCKET["commodity"].append("logistics")
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
        if stub in _MD_HAVE:
            for x in (a,b): blocks.setdefault(x,set()).add(stub)

# org/name -> person(s): match person.name==id, or any of person.orgs contains id (or id contains an org token)
def _norm(x): return " ".join(x.lower().replace("_"," ").replace("/"," ").replace(","," ").split())
def match_persons(node):
    out=[]; nn=_norm(node)
    if len(nn)<3: return []
    for p in P.get("persons",[]):
        if _norm(p["name"])==nn: out.append(p["name"]); continue
        for o in p.get("orgs",[]):
            on=_norm(o)
            # whole-phrase match (word-boundary) or a single org token equal to the node
            if nn==on or (" "+nn+" ") in (" "+on+" ") or any(tok==nn for tok in on.split()):
                out.append(p["name"]); break
    return sorted(set(out))

# ---- readable display labels (canonical underscore IDs -> human names) ----
ACR={"US","AI","SEC","CFTC","FDIC","OCC","FOMC","DTCC","LBMA","CME","ICE","JPM","MGX","GIC","CIC","REE",
 "HALEU","XPU","TPU","USD1","WLFI","IPO","SPV","NRO","FBI","CIA","DNI","PIF","UAE","UK","EU","PRC","HBM",
 "RPO","ETF","NSA","GCHQ","MI5","MI6","BIS","ECB","BOJ","RBI","RBA","BOC","NK","DPRK","IRGC","TSMC","ASML",
 "AMD","ARM","FTX","JV","NPC","OER","CPI","PCE","GDP","SETT"}
MIXED={"CoreWeave","OpenAI","SpaceX","BlackRock","BlueOwl","xAI","iFinex","SoftBank","WiseKey","SEALSQ",
 "DeepSeek","ByteDance","NVIDIA","macOS","iPhone","YouTube","WhatsApp"}
LABELS={  # explicit overrides (sinks, SPVs, compounds)
 "SINK_lenders":"Lenders","SINK_bondmarket":"Bond market","SINK_debt":"Debt / balance sheet",
 "SINK_capex":"Capex","SINK_backlog":"AI backlog","SINK_investors":"Wiped investors (Terra/LUNA)","ANTHROPIC_INVESTORS":"Anthropic investors",
 "SINK_treasury_basis":"Treasury basis trade","SINK_scam_victims":"Scam victims",
 "AI_Datacenters":"AI data centers","PrivateCredit_Funds":"Private-credit funds","Lazarus_Group":"Lazarus Group",
 "US_Treasuries":"US Treasuries","US_Banks":"US banks","US_Government":"US government",
 "MP_Materials":"MP Materials","Apollo_Blackstone":"Apollo / Blackstone","Defense_Primes":"Defense primes",
 "World_Liberty_Financial":"World Liberty Financial (USD1)","Meta_Hyperion_SPV":"Meta Hyperion SPV",
 "AI_Infrastructure_Partnership":"AI Infrastructure Partnership","Aligned_Data_Centers":"Aligned Data Centers",
 "IBIT":"IBIT (iShares Bitcoin Trust)","GIP":"Global Infrastructure Partners","HPS":"HPS Investment Partners",
 "Aladdin":"Aladdin (risk engine, ~$25T)",
 # quantum competitive landscape
 "D_Wave":"D-Wave","Atom_Computing":"Atom Computing","Alice_Bob":"Alice & Bob","Oxford_Ionics":"Oxford Ionics",
 "Vector_Atomic":"Vector Atomic","Origin_Quantum":"Origin Quantum (China)","EU_Quantum_Flagship":"EU Quantum Flagship",
 "USTC":"USTC / CAS (China)","RIKEN":"RIKEN (Japan)",
 # blockchain ecosystem
 "Ethereum_Foundation":"Ethereum Foundation","Mysten_Labs":"Mysten Labs (Sui)","QRL_Foundation":"QRL Foundation (post-quantum)",
 "QRL":"QRL (Quantum Resistant Ledger)","XRPL_Labs":"XRPL Labs (Xaman)","XRPLF":"XRP Ledger Foundation","Ripple_Prime":"Ripple Prime (ex-Hidden Road)",
 "Protocol_Labs":"Protocol Labs (IPFS/Filecoin)","DePIN_Storage":"Decentralized storage (DePIN)","Stellar_Development_Foundation":"Stellar Development Foundation",
 "Franklin_Templeton":"Franklin Templeton","Financial_Privacy":"Financial privacy / censorship-resistance",
 "Chainlink_Labs":"Chainlink Labs","Band_Protocol":"Band Protocol","Oracle_Interop":"Oracles & cross-chain interop",
 "VeChain_Foundation":"VeChain Foundation","XRPL_EVM":"XRPL EVM sidechain","Xahau":"Xahau (XRPL sidechain)",
 "WYST":"WYST (Wyoming stable token)","Citadel_Securities":"Citadel Securities","Hamilton_Lane":"Hamilton Lane","MAS":"MAS (Singapore) / Project Guardian",
 "ICE":"ICE / NYSE","DTCC":"DTCC",
 # crypto-enforcement actors
 "Gary_Gensler":"Gary Gensler (ex-SEC chair)","William_Hinman":"William Hinman (ex-SEC)","Jay_Clayton":"Jay Clayton (ex-SEC / SDNY)","Damian_Williams":"Damian Williams (ex-SDNY)",
 "Caroline_Crenshaw":"Caroline Crenshaw (SEC)","Elizabeth_Warren":"Sen. Elizabeth Warren","Letitia_James":"Letitia James (NY AG)","Rostin_Behnam":"Rostin Behnam (CFTC)",
 "Paul_Atkins":"Paul Atkins (SEC chair)","Hester_Peirce":"Hester Peirce ('Crypto Mom')","John_Deaton":"John Deaton (XRP advocate)","Brad_Garlinghouse":"Brad Garlinghouse (Ripple CEO)",
 "Stuart_Alderoty":"Stuart Alderoty (Ripple CLO)","SEC_Crypto_Task_Force":"SEC Crypto Task Force","NCET":"DOJ NCET (disbanded 2025)","Operation_Choke_Point_2":"Operation Choke Point 2.0","Simpson_Thacher":"Simpson Thacher (Hinman's firm)",
 # crypto founders / builders
 "David_Schwartz":"David Schwartz (XRPL/Ripple CTO)","Jed_McCaleb":"Jed McCaleb (XRPL/Stellar/Mt.Gox)","Arthur_Britto":"Arthur Britto (XRPL co-creator)",
 "Evan_Cheng":"Evan Cheng (Mysten CEO)","Sam_Blackshear":"Sam Blackshear (Move/Sui)","Keonne_Rodriguez":"Keonne Rodriguez (Samourai)","William_L_Hill":"William L. Hill (Samourai)",
 "Zooko_Wilcox":"Zooko Wilcox (Zcash/ECC)","Electric_Coin_Company":"Electric Coin Company (Zcash)","Jeremy_Kauffman":"Jeremy Kauffman (LBRY)","Odysee":"Odysee (LBRY video)",
 # 2022 collapse cluster
 "Sam_Bankman_Fried":"Sam Bankman-Fried (FTX)","Caroline_Ellison":"Caroline Ellison (Alameda)","Do_Kwon":"Do Kwon (Terra)","Alex_Mashinsky":"Alex Mashinsky (Celsius)",
 "Barry_Silbert":"Barry Silbert (DCG)","Su_Zhu":"Su Zhu (3AC)","Kyle_Davies":"Kyle Davies (3AC)","Brian_Armstrong":"Brian Armstrong (Coinbase)",
 "Winklevoss_Twins":"Winklevoss twins (Gemini)","Justin_Sun":"Justin Sun (Tron)","Arthur_Hayes":"Arthur Hayes (BitMEX)",
 "Alameda_Research":"Alameda Research","Gemini_Earn":"Gemini Earn","DCG":"Digital Currency Group",
 # crypto market-makers + political money
 "Jump_Crypto":"Jump Crypto","Tai_Mo_Shan":"Tai Mo Shan (Jump sub)","Jane_Street":"Jane Street","Cumberland_DRW":"Cumberland (DRW)",
 "Crypto_Market_Makers":"Crypto market-makers","Kanav_Kariya":"Kanav Kariya (Jump)",
 # semiconductor / logistics / standards
 "ZEISS_SMT":"Carl Zeiss SMT (EUV optics)","Semiconductor_Equipment":"Semiconductor equipment (WFE)","Semiconductor_Materials":"Semiconductor materials","EDA_Tools":"EDA tools / IP",
 "CoWoS":"CoWoS (advanced packaging)","HBM":"HBM (high-bandwidth memory)","Samsung_Foundry":"Samsung Foundry","SK_Hynix":"SK Hynix","Applied_Materials":"Applied Materials","Lam_Research":"Lam Research","Tokyo_Electron":"Tokyo Electron","Tokyo_Ohka":"Tokyo Ohka","Shin_Etsu":"Shin-Etsu","Siemens_EDA":"Siemens EDA",
 "CMA_CGM":"CMA CGM","Hapag_Lloyd":"Hapag-Lloyd","Ocean_Shipping":"Ocean shipping (carriers)","Logistics_3PL":"3PL / freight forwarders","Kuehne_Nagel":"Kuehne+Nagel",
 "Suez_Canal":"Suez Canal","Panama_Canal":"Panama Canal","Strait_of_Malacca":"Strait of Malacca","Strait_of_Hormuz":"Strait of Hormuz","Taiwan_Strait":"Taiwan Strait","Shipping_Chokepoints":"Maritime chokepoints",
 "ISO_IEC_JTC1":"ISO/IEC JTC 1","SC42_AI":"ISO/IEC SC 42 (AI standards)","SC27_Security":"ISO/IEC SC 27 (security)","Standards_Bodies":"Standards bodies","Codex_Alimentarius":"Codex Alimentarius","Medical_Device_Standards":"Medical-device standards","ISO_13485":"ISO 13485","ISO_14971":"ISO 14971",
 # East Asia
 "South_Korea":"South Korea","South_Africa":"South Africa","Samsung_Group":"Samsung Group (chaebol)","SK_Group":"SK Group","Lee_Family":"Lee family (Samsung)","Zaibatsu_Keiretsu":"Zaibatsu / keiretsu",
 "LDP":"LDP (Japan)","Soka_Gakkai":"Soka Gakkai","Unification_Church":"Unification Church","CDP_Japan":"CDP (Japan opposition)","Shinzo_Abe":"Shinzo Abe","Shigeru_Ishiba":"Shigeru Ishiba",
 "People_Power_Party":"People Power Party (Korea)","Democratic_Party_Korea":"Democratic Party (Korea)","Yoon_Suk_yeol":"Yoon Suk Yeol","Lee_Jae_myung":"Lee Jae-myung",
 "Apartheid_Honorary_Whites":"Apartheid 'honorary whites'","Toyoko_Kids":"Toyoko kids","Host_Club_Debt":"Host-club debt trap","Japan_Sex_Industry":"Japan sex industry (harms)",
 # China AI stack
 "Zhipu_AI":"Zhipu AI (GLM)","Moonshot":"Moonshot (Kimi)","01_AI":"01.AI (Yi)","Alibaba":"Alibaba (Qwen)","Baidu":"Baidu (Ernie)","Tencent":"Tencent (Hunyuan)","Xiaomi":"Xiaomi (MiMo)","Huawei":"Huawei (Ascend)",
 "Moore_Threads":"Moore Threads","CAC":"CAC (Cyberspace Admin)","China_AI_Labs":"China AI labs","China_AI_Hardware":"China AI hardware (Ascend)","China_AI_Censorship":"China AI censorship (CAC)",
 # local / uncensored / decentralized AI
 "llama_cpp":"llama.cpp","LM_Studio":"LM Studio","Stability_AI":"Stability AI (Stable Diffusion)","Black_Forest_Labs":"Black Forest Labs (Flux)","Hugging_Face":"Hugging Face","Nous_Research":"Nous Research","AllenAI_OLMo":"Allen AI (OLMo)",
 "Eric_Hartford":"Eric Hartford (Dolphin)","Venice_AI":"Venice.ai (VVV)","Erik_Voorhees":"Erik Voorhees","Local_AI_Tooling":"Local AI tooling","Uncensored_AI":"Uncensored AI (abliteration)","Decentralized_AI":"Decentralized AI compute","Open_Local_AI":"Open / local AI ecosystem",
 "Fhenix":"Fhenix (FHE L2)","Biconomy":"Biconomy (account abstraction)",
 "Disney_Studios_Coalition":"Disney studios coalition","Russian_energy_executives":"Russian energy executives",
 "SpaceX_IPO_Public":"SpaceX IPO (public markets)","Starlink_Subscribers":"Starlink subscribers",
 "Federal_Reserve":"Federal Reserve","Tornado_Cash":"Tornado Cash","Samourai_Wallet":"Samourai Wallet",
 "Government_of_Gujarat":"Government of Gujarat","Spanish_Government_SETT":"Spanish government (SETT)",
 "UK_Labour_government":"UK Labour government","UK_government_cloud":"UK government (cloud)",
 "China":"China","Russia":"Russia","Liberty Strategic Capital":"Liberty Strategic Capital",
 # uncovered / out-of-scope risk pools
 "Money_Market_Funds":"Money market funds","Repo_Market":"Repo market","Treasury_Market":"Treasury market",
 "Hedge_Funds":"Hedge funds","Pension_Funds":"Pension funds","PrivateEquity_Funds":"Private equity funds",
 "UK_LDI_Funds":"UK LDI funds","Life_Insurers":"Life insurers",
 "GSEs_FannieFreddie":"GSEs (Fannie / Freddie)","FHLB_System":"FHLB system","Mortgage_Market":"Mortgage market",
 "Family_Offices":"Family offices","Prime_Brokers":"Prime brokers",
 "Mortgage_REITs":"Mortgage REITs","Agency_MBS_Market":"Agency MBS market","CRE_Market":"CRE market",
 "BaaS_Middleware":"BaaS middleware","Sponsor_Banks":"Sponsor banks","Neobanks":"Neobanks",
 "Subprime_Auto_ABS":"Subprime auto ABS","Tricolor_Holdings":"Tricolor Holdings","BNPL_Phantom_Debt":"BNPL phantom debt",
 "Municipal_Debt":"Municipal debt","Federal_Transfers":"Federal transfers","US_household_credit":"US household credit",
 "Credit_Unions":"Credit unions","ILCs":"ILCs","Foreign_Bank_US_Branches":"Foreign-bank US branches",
 # digital-ID OS/hardware layer
 "EUDI_Wallet":"EU Digital Identity Wallet","Device_Age_Attestation":"Device / OS age attestation",
 "Secure_Element_Vendors":"Secure-element / eUICC vendors","Alternative_OS_Exclusion":"Alternative-OS exclusion",
 "UK_Digital_ID":"UK digital ID (BritCard / One Login)","Labour_Together":"Labour Together",
 # hidden / off-book sovereign debt
 "Developing_State_Infrastructure":"Developing-state infrastructure","Distressed_Sovereigns":"Distressed sovereigns (swap-line)",
 "LGFV_Debt":"China LGFV debt","US_Contingent_Liabilities":"US contingent liabilities",
 # device-ownership erosion -> OS identity
 "Device_Ownership_Erosion":"Device-ownership erosion","AI_Native_OS":"AI-native OS","Age_Assurance_Issuers":"Age-assurance issuers",
 # uncovered-pool deep digs
 "Corporate_Credit_Unions":"Corporate credit unions","NCUSIF":"NCUSIF (CU insurance fund)","BDCs":"BDCs",
 "Commercial_Parents":"Commercial / fintech parents","Farm_Credit_System":"Farm Credit System","FFCB_Funding":"FFCB Funding Corp",
 "US_Farmland":"US farmland","CoBank":"CoBank","Rural_Infrastructure":"Rural infrastructure (coops)","Japanese_Banks":"Japanese banks"}
def disp_label(nid):
    if nid in LABELS: return LABELS[nid]
    if nid in MIXED: return nid
    s=nid[5:] if nid.startswith("SINK_") else nid
    parts=s.replace("_"," ").split()
    out=[]
    for p in parts:
        if p in MIXED: out.append(p)
        elif p.upper() in ACR: out.append(p.upper())
        elif p.isupper() and len(p)>1: out.append(p)  # already an acronym
        else: out.append(p[:1].upper()+p[1:])
    return " ".join(out)

# ---- stub -> readable block title (for "documented in") ----
TITLES={}
for _f in glob.glob(os.path.join(ROOT,"research","*.json")):
    try: TITLES[os.path.basename(_f)[:-5]]=(json.load(open(_f)).get("metadata",{}).get("title") or "")[:120]
    except Exception: pass

# ---- per-node cross-project description ----
BDESC={"ai":"AI model labs, hyperscalers, chip vendors and neoclouds","capital":"financiers, private credit, banks, central banks","crypto":"exchanges, stablecoins, DLT","defense":"defense primes, intel, threat actors","state":"states, regulators, commissions","commodity":"commodities, energy, minerals, industrial","identity":"surveillance, telecom, satellite, standards","macro":"macro factors, data, labor","pqc":"post-quantum / quantum","person":"individuals","other":"infrastructure / other"}
out_e={}; in_e={}
for e in edges:
    out_e.setdefault(e["from"],[]).append(e); in_e.setdefault(e["to"],[]).append(e)
def node_desc(name,bucket):
    L=disp_label(name)
    bits=[f"<b>{html.escape(L)}</b> — {BDESC.get(bucket,'')}."]
    if name in scc:
        bits.append("Part of the <b>circular core</b> (Tarjan SCC)" + (" — robust." if name in scc_robust else ", via a cancelable link."))
    oe=sorted(out_e.get(name,[]),key=lambda x:(x.get("amount_usd") or 0),reverse=True)
    ie=sorted(in_e.get(name,[]),key=lambda x:(x.get("amount_usd") or 0),reverse=True)
    def cp(es,verb,dirn):
        seen=[]
        for e in es:
            other=disp_label(e[dirn]); instr=e.get("instrument","")
            if other not in [s[0] for s in seen]: seen.append((other,instr))
            if len(seen)>=3: break
        if not seen: return ""
        return verb+" "+", ".join(f"{o} ({i})" for o,i in seen)
    flow=[s for s in (cp(oe,"Funds/supplies","to"),cp(ie,"Funded/supplied by","from")) if s]
    if flow: bits.append("; ".join(flow)+".")
    blks=[TITLES.get(b,b) for b in sorted(blocks.get(name,[]))][:4]
    if blks: bits.append("Documented in: "+ "; ".join(html.escape(b) for b in blks)+".")
    return " ".join(bits)

nodes=[]
for name,meta in ents.items():
    sec=(meta or {}).get("sector","other"); bucket=SEC2BUCKET.get(sec,"other")
    nodes.append({"id":name,"label":disp_label(name),"desc":node_desc(name,bucket),
                  "sector":sec,"bucket":bucket,"deg":deg.get(name,0),
                  "scc": name in scc, "robust": name in scc_robust,
                  "blocks":sorted(blocks.get(name,[])),"persons":match_persons(name)})
def _amt(v):
    if not v: return ""
    try: v=float(v)
    except Exception: return ""
    if v>=1e9: return f"${v/1e9:.1f}B"
    if v>=1e6: return f"${v/1e6:.0f}M"
    if v>=1e3: return f"${v/1e3:.0f}k"
    return f"${v:.0f}"
links=[{"source":e["from"],"target":e["to"],"layer":e.get("layer","financial"),
        "instrument":e.get("raw_instrument") or e.get("instrument",""),"iclass":e.get("instrument",""),
        "circular":bool(e.get("declared_circular")),"cancelable":bool(e.get("cancelable")),
        "note":(e.get("note") or "")[:240],"amount":_amt(e.get("amount_usd")),"status":e.get("status",""),
        "block":(e.get("source_file","")[:-5] if e.get("source_file","").endswith(".json") else "")} for e in edges]
# first source-file (stub) per node, for the panel's primary block link
SEC2BUCKET_DESC={"ai":"AI model labs, hyperscalers, chip vendors and neoclouds","capital":"financiers, private credit, banks, central banks","crypto":"exchanges, stablecoins, DLT","defense":"defense primes, intel, threat actors","state":"states, regulators, commissions","commodity":"commodities, energy, minerals, industrial","identity":"surveillance, telecom, satellite, standards","macro":"macro factors, data, labor","pqc":"post-quantum / quantum","person":"individuals","other":"infrastructure / other"}

NAV=('<div class=nav><a href="index.html">Home</a><a href="atlas.html">Atlas</a><a href="dashboard.html">Dashboard</a>'
 '<a href="charts.html">Charts</a><a href="research.html">Research</a><a href="persons.html">Persons</a>'
 '<a href="bubblemap.html" class=active>Bubble Map</a><a href="globe.html">Globe</a><a href="lenses.html">Lenses</a>'
 '<a href="methodology.html">Methodology</a><a href="glossary.html">Glossary</a>'
 '<a href="https://github.com/pq-cybarg/bubble-map">Source &#8599;</a></div>'
 '<div style="background:#faf8f2;color:#8a8378;font:11px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;text-align:center;padding:6px 16px;border-bottom:1px solid #e4ddcc">Independent research &amp; opinion. Gradings are automated / LLM-assisted and may contain errors or hallucinations; nothing here is a statement of fact, financial advice, or an accusation of wrongdoing by any party. Claims about identifiable people or organizations reflect public records + good-faith interpretation; intent is not inferred from association. <a href="methodology.html" style="color:#6b665d;text-decoration:underline">Methodology &amp; disclaimer</a>.</div>')
legend="".join(f'<span class=lg data-b="{b}"><i style="background:{COLORS[b]}"></i>{html.escape(BLABEL[b])}</span>' for b in BLABEL)

HTML="""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Bubble Map — the AI capital loop graph</title>
<style>
:root{--bg:#faf8f2;--paper:#fffdf8;--ink:#1c1b19;--mut:#6b665d;--line:#e4ddcc;--ac:#7b2d26;--ac2:#1f4e79}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;overflow:hidden}
.nav{background:var(--paper);border-bottom:1px solid var(--line);padding:10px 18px;font-size:14px;text-align:center}
.nav a{margin:0 9px!important}
.nav a{color:var(--ac2);text-decoration:none;margin-right:16px}.nav a.active{font-weight:700}.nav a:hover{text-decoration:underline}
#stage{position:relative;width:100%;height:calc(100vh - 41px);overflow:hidden}
svg{display:block;width:100%;height:100%;cursor:grab}svg:active{cursor:grabbing}
#hud{position:absolute;top:12px;left:14px;z-index:5;max-width:300px;background:#fffdf8e8;border:1px solid var(--line);border-radius:9px;padding:12px 14px}
#hud h1{font:600 16px Georgia,serif;margin:0 0 2px}.sub{color:var(--mut);font-size:11.5px;margin-bottom:9px}
#q{width:100%;padding:8px 10px;font-size:13px;border:1px solid var(--line);border-radius:6px;margin-bottom:0;font-family:inherit}
#qres{max-height:300px;overflow:auto;margin:4px 0 8px;border-radius:6px;border:1px solid var(--line);display:none;background:#fffdf8}
#qres.on{display:block}
#qres .ri{padding:6px 9px;cursor:pointer;border-bottom:1px solid #efe9da;font-size:12.5px;line-height:1.3}
#qres .ri:last-child{border-bottom:none}
#qres .ri:hover,#qres .ri.sel{background:#1f4e7912}
#qres .ri b{color:#1f4e79}
#qres .ri .rm{color:var(--mut);font-size:11px}
#qres .ri .rs{float:right;color:#9a8f78;font-size:10.5px;margin-left:6px}
#qres .rnone{padding:7px 9px;color:var(--mut);font-size:12px}
.tog{display:block;font-size:12.5px;color:#33312c;margin:4px 0;cursor:pointer;user-select:none}
.tog input{vertical-align:-1px;margin-right:6px}
#legend{display:flex;flex-wrap:wrap;gap:3px 10px;margin-top:9px}
.lg{font-size:11px;color:#33312c;white-space:nowrap}.lg i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px;vertical-align:middle}
#panel{position:absolute;top:12px;right:14px;z-index:6;width:300px;max-height:calc(100% - 24px);overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:none;box-shadow:0 6px 22px #0002}
#panel h2{margin:0 0 2px;font:600 17px Georgia,serif}#panel .pr{color:var(--mut);font-size:12px;margin-bottom:8px}
#panel .desc{font-size:12.5px;line-height:1.55;color:#33312c;margin:10px 0 4px;border-top:1px solid var(--line);padding-top:9px}
#panel .desc b{color:#1c1b19}
#panel .k{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--ac);font-weight:700;margin:11px 0 3px}
#panel a{color:var(--ac2);text-decoration:none}#panel a:hover{text-decoration:underline}
#panel .pill{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;color:#fff;margin:0 4px 4px 0}
#panel ul{margin:4px 0;padding-left:18px}#panel li{font-size:12.5px;margin:2px 0}
#close{position:absolute;top:8px;right:10px;cursor:pointer;color:var(--mut);font-size:18px;line-height:1}
.note{position:absolute;bottom:10px;left:14px;font-size:11px;color:var(--mut);background:#fffdf8c8;padding:4px 8px;border-radius:5px}
text.lab{font-size:9px;fill:#3a382f;pointer-events:none;paint-order:stroke;stroke:#faf8f2;stroke-width:3px;stroke-linejoin:round}
.lg{cursor:pointer;padding:1px 4px;border-radius:9px;border:1px solid transparent;transition:.12s}
.lg:hover{background:#00000008}.lg.off{opacity:.32}.lg.solo{border-color:var(--ac2);background:#1f4e7912}
#tip{position:absolute;z-index:9;pointer-events:none;display:none;max-width:280px;background:#1c1b19f2;color:#f5f1e6;font-size:12px;line-height:1.45;padding:8px 10px;border-radius:7px;box-shadow:0 4px 14px #0004}
#tip b{color:#f0c674}#tip .cl{color:#e07b6b}
#btns{position:absolute;bottom:10px;right:14px;z-index:6;display:flex;gap:6px}
#btns button{font:12px inherit;cursor:pointer;background:var(--paper);color:var(--ac2);border:1px solid var(--line);border-radius:6px;padding:6px 10px}
#btns button:hover{background:#1f4e7910}
line{vector-effect:non-scaling-stroke}
line.hl{stroke:#1f4e79!important;opacity:.95!important}
#panel .ea{color:#9a6a1a;font-weight:600}#panel .amt{color:#2e6b3e;font-weight:600}
</style></head><body>__NAV__
<div id=stage>
<div id=hud><h1>Bubble Map</h1><div class=sub>the AI capital loop, as a graph &middot; drag bubbles &middot; scroll to zoom &middot; click a bubble to focus its network &middot; hover an edge for the deal</div>
<input id=q placeholder="Find an entity or person&hellip;" autocomplete=off>
<div id=qres></div>
<label class=tog><input type=checkbox id=tStruct checked> structural / overlay edges (governance, legal, revolving-door, PAC)</label>
<label class=tog><input type=checkbox id=tCore> dim all but the circular core</label>
<label class=tog><input type=checkbox id=tLab checked> show labels</label>
<div id=legend>__LEGEND__</div>
<div class=sub style="margin:8px 0 0">Click a legend colour to isolate a sector.</div></div>
<div id=panel><span id=close>&times;</span><div id=pbody></div></div>
<div id=tip></div>
<div id=btns><button id=bFit>Fit to view</button><button id=bReset>Reset focus</button></div>
<div class=note>__N__ entities &middot; __E__ edges &middot; gold ring = the circular core (Tarjan SCC) &middot; solid = financial flow, dashed = structural/overlay &middot; <b style=color:#c0392b>red</b> = declared circular</div>
<svg id=g></svg></div>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
const NODES=__NODES__, LINKS=__LINKS__, COLORS=__COLORS__, BTITLE=__BTITLE__;
const NLABEL={}; NODES.forEach(n=>NLABEL[n.id]=n.label||n.id);
const blockLink=s=>`<a href="r-${s}.html">${BTITLE[s]?BTITLE[s].replace(/&/g,'&amp;').replace(/</g,'&lt;'):s}</a>`;
const W=()=>document.getElementById('stage').clientWidth, H=()=>document.getElementById('stage').clientHeight;
const svg=d3.select('#g'); const root=svg.append('g');
svg.append('defs').selectAll('marker').data(['fin','struct']).join('marker')
 .attr('id',d=>'arr-'+d).attr('viewBox','0 -5 10 10').attr('refX',18).attr('refY',0)
 .attr('markerWidth',5).attr('markerHeight',5).attr('orient','auto')
 .append('path').attr('d','M0,-4L8,0L0,4').attr('fill',d=>d==='fin'?'#9a8f78':'#cdc6b4');
const id2n=new Map(NODES.map(n=>[n.id,n]));
const pslug=s=>'p-'+s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const tip=document.getElementById('tip');
const lerp=(a,b)=>typeof a==='object'?a.id:a; // source/target id helper
const link=root.append('g').selectAll('line').data(LINKS).join('line')
 .attr('stroke',d=>d.layer==='financial'?(d.circular?'#c0392b':'#9a8f78'):'#d8d0bd')
 .attr('stroke-width',d=>d.circular?1.9:(d.layer==='financial'?1.15:0.75))
 .attr('stroke-dasharray',d=>d.layer==='structural'?'3,3':null).attr('opacity',.55)
 .attr('marker-end',d=>'url(#arr-'+(d.layer==='financial'?'fin':'struct')+')');
// invisible wide hit-layer so thin edges are hoverable -> deal tooltip
const linkHit=root.append('g').selectAll('line').data(LINKS).join('line')
 .attr('stroke','transparent').attr('stroke-width',9).style('cursor','help')
 .on('mouseover',(e,d)=>{const i=link.filter(x=>x===d);i.classed('hl',true);
   tip.style.display='block';
   tip.innerHTML=`<b>${lerp(d.source)} → ${lerp(d.target)}</b><br>${d.instrument||d.iclass||'—'}`
    +(d.amount?` &nbsp;<span style="color:#7fd99a">${d.amount}</span>`:'')
    +(d.status?` &middot; ${d.status}`:'')
    +(d.circular?' <span class=cl>&middot; ↻ circular</span>':'')
    +(d.cancelable?' &middot; cancelable':'')
    +(d.note?`<br><span style="color:#cfc8b8">${d.note}</span>`:'')
    +(d.block?`<br><span style="color:#9fb6d6">block: ${d.block}</span>`:'');})
 .on('mousemove',e=>{tip.style.left=(e.clientX+14)+'px';tip.style.top=(e.clientY+12)+'px';})
 .on('mouseout',(e,d)=>{link.classed('hl',false);tip.style.display='none';});
const rad=d=>4+Math.sqrt(d.deg)*2.2;
const node=root.append('g').selectAll('g').data(NODES).join('g').style('cursor','pointer').on('click',(e,d)=>{showPanel(d);egoFocus(d);});
node.append('circle').attr('r',rad).attr('fill',d=>COLORS[d.bucket]||'#8a8378')
 .attr('stroke',d=>d.scc?'#d4a017':'#fffdf8').attr('stroke-width',d=>d.scc?2.6:1);
node.append('title').text(d=>d.label+'  ('+d.sector+', deg '+d.deg+')');
const labels=root.append('g').selectAll('text').data(NODES).join('text').attr('class','lab')
 .attr('dx',d=>rad(d)+2).attr('dy',3).text(d=>d.label);  // labels ON by default
let fitted=false, curK=1, pendingFocus=null;
const baseW=d=>d.circular?1.9:(d.layer==='financial'?1.15:0.75);
const sim=d3.forceSimulation(NODES)
 .force('link',d3.forceLink(LINKS).id(d=>d.id).distance(d=>d.layer==='financial'?64:88).strength(.28))
 .force('charge',d3.forceManyBody().strength(-140).distanceMax(520))
 .force('center',d3.forceCenter(W()/2,H()/2))
 .force('x',d3.forceX(W()/2).strength(.06)).force('y',d3.forceY(H()/2).strength(.06))
 .force('collide',d3.forceCollide().radius(d=>rad(d)+13).strength(.9))
 .on('tick',tick);
function tick(){
 const px=s=>s.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
 px(link);px(linkHit);
 node.attr('transform',d=>`translate(${d.x},${d.y})`);
 labels.attr('x',d=>d.x).attr('y',d=>d.y);
 if(sim.alpha()<0.06){                                   // settled
   if(pendingFocus){const t=pendingFocus;pendingFocus=null;fitted=true;focusNode(t);}  // deep-link: center on node
   else if(!fitted){fitted=true; fit();}                  // else auto-frame (kills empty space)
 }
}
// keep node/line sizes usable at any zoom: enlarge when zoomed OUT (k<1), constant lines via CSS
function rescale(k){curK=k; const s=k<1?Math.min(1/k,3.2):1;
 node.selectAll('circle').attr('r',d=>rad(d)*s).attr('stroke-width',d=>(d.scc?2.6:1)*s);
 link.attr('stroke-width',d=>baseW(d)*s);
 labels.style('font-size',(9*Math.min(s,2.2))+'px').attr('dx',d=>rad(d)*s+2);}
// node hover: enlarge + reveal its label
node.on('mouseenter',function(e,d){d3.select(this).select('circle').attr('r',rad(d)*(curK<1?Math.min(1/curK,3.2):1)+3);
  d3.select(this).raise();})
 .on('mouseleave',function(e,d){d3.select(this).select('circle').attr('r',rad(d)*(curK<1?Math.min(1/curK,3.2):1));});
// DRAG: container=root so pointer is in the ZOOMED data space (fixes 'grab makes it fly away');
// pin where dropped so nodes stay put (Reset focus unpins).
node.call(d3.drag().container(function(){return root.node();})
 .on('start',(e,d)=>{if(!e.active)sim.alphaTarget(.12).restart();d.fx=d.x;d.fy=d.y;})
 .on('drag',(e,d)=>{d.fx=e.x;d.fy=e.y;})
 .on('end',(e,d)=>{if(!e.active)sim.alphaTarget(0);/* leave fx/fy: pinned where dropped */}));
const zoomB=d3.zoom().scaleExtent([.35,6]).on('zoom',e=>{root.attr('transform',e.transform);rescale(e.transform.k);});
svg.call(zoomB);
// controls
document.getElementById('tStruct').onchange=e=>{const on=e.target.checked;
 link.style('display',d=>d.layer==='structural'&&!on?'none':null);};
document.getElementById('tLab').onchange=e=>labels.style('display',e.target.checked?null:'none');
document.getElementById('tCore').onchange=e=>{const on=e.target.checked;
 node.style('opacity',d=>!on||d.scc?1:.12); link.style('opacity',d=>!on?.55:((id2n.get(typeof d.source==='object'?d.source.id:d.source).scc&&id2n.get(typeof d.target==='object'?d.target.id:d.target).scc)?.7:.05));};
const q=document.getElementById('q'), qres=document.getElementById('qres');
// ---- fuzzy search: ranked, clickable, and indexes PERSONS + descriptions ----
const _strip=h=>(h||'').replace(/<[^>]*>/g,' ').replace(/&[a-z]+;/g,' ');
const _norm=s=>(s||'').toLowerCase().replace(/[_\\/]/g,' ').replace(/[^a-z0-9 ]/g,' ').replace(/\\s+/g,' ').trim();
const _bg=s=>{s=_norm(s).replace(/ /g,'');const o=[];for(let i=0;i<s.length-1;i++)o.push(s.slice(i,i+2));return o;};
const _dice=(a,b)=>{if(!a.length||!b.length)return 0;const m={};a.forEach(x=>m[x]=(m[x]||0)+1);let h=0;b.forEach(x=>{if(m[x]>0){m[x]--;h++;}});return 2*h/(a.length+b.length);};
NODES.forEach(d=>{d._lab=_norm(d.label);d._id=_norm(d.id);d._per=(d.persons||[]).map(_norm);
  d._desc=_norm(_strip(d.desc));d._blk=(d.blocks||[]).map(s=>_norm(BTITLE[s]||s)).join(' ');d._lbg=_bg(d.label);});
function scoreNode(d,qn,qbg,qtok){
  let sc=Math.max(d._lab.includes(qn)?0.96:0, _dice(qbg,d._lbg), d._id.includes(qn)?0.9:0);
  const hay=d._lab+' '+d._id+' '+d._desc+' '+d._blk; let tk=0;
  qtok.forEach(t=>{if(t.length>1&&hay.includes(t))tk++;}); if(qtok.length)sc=Math.max(sc,tk/qtok.length*0.82);
  let pbest=0,via=''; d._per.forEach((p,i)=>{let ptk=0;qtok.forEach(t=>{if(t.length>1&&p.includes(t))ptk++;});
    const psc=Math.max(p.includes(qn)?0.97:_dice(qbg,_bg(p)), qtok.length?ptk/qtok.length*0.9:0);
    if(psc>pbest){pbest=psc;via=d.persons[i];}});
  return pbest>sc?{s:pbest,via:'person:'+via}:{s:sc,via:''};
}
let qsel=-1, qhits=[];
function resetStroke(){node.select('circle').attr('stroke',d=>d.scc?'#d4a017':'#fffdf8').attr('stroke-width',d=>d.scc?2.6:1);}
function markSel(){Array.from(qres.querySelectorAll('.ri')).forEach((el,i)=>el.classList.toggle('sel',i===qsel));}
function pickHit(d){focusNode(d.id);qres.className='';qres.innerHTML='';qhits=[];}
function runSearch(){
  const raw=q.value.trim();
  if(raw.length<2){qres.className='';qres.innerHTML='';qhits=[];resetStroke();return;}
  const qn=_norm(raw),qbg=_bg(raw),qtok=qn.split(' ').filter(Boolean),TH=0.30;
  qhits=NODES.map(d=>{const r=scoreNode(d,qn,qbg,qtok);return {d,s:r.s,via:r.via};})
    .filter(x=>x.s>=TH).sort((a,b)=>b.s-a.s).slice(0,12);
  qres.className='on';
  if(!qhits.length){qres.innerHTML='<div class=rnone>No match &ge;30% similarity. Try a partial name.</div>';resetStroke();return;}
  qsel=0;
  qres.innerHTML=qhits.map((x,i)=>{const vp=x.via.indexOf('person:')===0?` &middot; ${x.via.slice(7)}`:'';
    return `<div class=ri data-i="${i}"><span class=rs>${Math.round(x.s*100)}%</span><b>${x.d.label}</b> <span class=rm>${x.d.sector}${vp}</span></div>`;}).join('');
  Array.from(qres.querySelectorAll('.ri')).forEach(el=>el.onclick=()=>pickHit(qhits[+el.dataset.i].d));
  markSel();
  const hit=new Set(qhits.map(x=>x.d.id));
  node.select('circle').attr('stroke',d=>hit.has(d.id)?'#1f4e79':(d.scc?'#d4a017':'#fffdf8'))
    .attr('stroke-width',d=>hit.has(d.id)?3.4:(d.scc?2.6:1));
}
q.oninput=runSearch;
q.onkeydown=e=>{if(!qhits.length)return;
  if(e.key==='ArrowDown'){e.preventDefault();qsel=Math.min(qsel+1,qhits.length-1);markSel();}
  else if(e.key==='ArrowUp'){e.preventDefault();qsel=Math.max(qsel-1,0);markSel();}
  else if(e.key==='Enter'){e.preventDefault();if(qhits[qsel])pickHit(qhits[qsel].d);}
  else if(e.key==='Escape'){q.value='';runSearch();}};
document.addEventListener('click',e=>{if(!e.target.closest('#hud'))qres.className='';});
document.getElementById('close').onclick=()=>{document.getElementById('panel').style.display='none';clearEgo();soloB=null;};
function neighbors(d){const ins=[],outs=[];LINKS.forEach(l=>{const s=lerp(l.source),t=lerp(l.target);
 if(s===d.id)outs.push({n:t,i:l.instrument||l.iclass,c:l.circular,a:l.amount}); if(t===d.id)ins.push({n:s,i:l.instrument||l.iclass,c:l.circular,a:l.amount});});
 const key=z=>(z.a?1:0); outs.sort((p,q)=>key(q)-key(p)); ins.sort((p,q)=>key(q)-key(p)); return {ins,outs};}
function showPanel(d){const p=document.getElementById('panel'),b=document.getElementById('pbody');
 const {ins,outs}=neighbors(d);
 const blk=d.blocks.map(blockLink).join(' &middot; ')||'<span style="color:#6b665d">—</span>';
 const per=d.persons.length?d.persons.map(x=>`<a href="persons.html#${pslug(x)}">${x}</a>`).join(', '):'';
 const nb=a=>a.length?('<ul>'+a.slice(0,16).map(x=>`<li>${x.c?'<b class=ea>↻</b> ':''}<a href="bubblemap.html#node=${encodeURIComponent(x.n)}" onclick="event.preventDefault();focusNode('${x.n.replace(/'/g,"\\\\'")}');">${NLABEL[x.n]||x.n}</a> <span style=color:#6b665d>(${x.i||'—'})</span>${x.a?` <span class=amt>${x.a}</span>`:''}</li>`).join('')+(a.length>16?`<li style=color:#6b665d>+${a.length-16} more…</li>`:'')+'</ul>'):'<div style="color:#6b665d;font-size:12px">—</div>';
 b.innerHTML=`<h2>${d.label}</h2><div class=pr>${d.sector} &middot; degree ${d.deg}${d.scc?' &middot; <b style=color:#9a6a1a>circular core'+(d.robust?' (robust)':' (via cancelable)')+'</b>':''}</div>`
  +`<span class=pill style="background:${COLORS[d.bucket]}">${d.bucket}</span>`
  +(d.desc?`<div class=desc>${d.desc}</div>`:'')
  +(per?`<div class=k>Key person</div><div>${per}</div>`:'')
  +`<div class=k>Outflows (${outs.length})</div>${nb(outs)}`
  +`<div class=k>Inflows (${ins.length})</div>${nb(ins)}`
  +`<div class=k>Documented in</div><div style=font-size:12.5px>${blk}</div>`;
 p.style.display='block';}
function centerOn(d){const k=Math.max(curK,1.4);const tx=W()/2-k*d.x,ty=H()/2-k*d.y;
 svg.transition().duration(550).call(zoomB.transform,d3.zoomIdentity.translate(tx,ty).scale(k));}
function focusNode(id){const d=id2n.get(id);if(!d)return;showPanel(d);egoFocus(d);centerOn(d);q.value='';}
// ----- adjacency for ego-focus -----
const ADJ=new Map(NODES.map(n=>[n.id,new Set([n.id])]));
LINKS.forEach(l=>{const s=lerp(l.source),t=lerp(l.target);ADJ.get(s)&&ADJ.get(s).add(t);ADJ.get(t)&&ADJ.get(t).add(s);});
let egoOn=null;
function egoFocus(d){egoOn=d.id;const keep=ADJ.get(d.id)||new Set([d.id]);
 node.style('opacity',n=>keep.has(n.id)?1:.08);
 labels.style('display',n=>keep.has(n.id)?null:'none');
 const vis=l=>keep.has(lerp(l.source))&&keep.has(lerp(l.target));
 link.style('opacity',l=>vis(l)?.85:.04);
 linkHit.style('pointer-events',l=>vis(l)?null:'none');
 node.select('circle').attr('stroke',n=>n.id===d.id?'#1f4e79':(n.scc?'#d4a017':'#fffdf8'))
  .attr('stroke-width',n=>n.id===d.id?4.5:(n.scc?2.6:1));}
function clearEgo(){egoOn=null;
 node.style('opacity',1);link.style('opacity',.55);linkHit.style('pointer-events',null);
 labels.style('display',document.getElementById('tLab').checked?null:'none');  // ALWAYS restore (fixes vanishing names)
 node.select('circle').attr('stroke',n=>n.scc?'#d4a017':'#fffdf8').attr('stroke-width',n=>n.scc?2.6:1);
 document.querySelectorAll('.lg').forEach(x=>x.classList.remove('off','solo'));}
// ----- clickable legend: isolate a sector bucket -----
let soloB=null;
document.querySelectorAll('.lg').forEach(el=>el.onclick=()=>{const b=el.dataset.b;
 if(soloB===b){soloB=null;clearEgo();return;}
 soloB=b;egoOn=null;
 document.querySelectorAll('.lg').forEach(x=>{x.classList.toggle('solo',x.dataset.b===b);x.classList.toggle('off',x.dataset.b!==b);});
 node.style('opacity',n=>n.bucket===b?1:.08);
 labels.style('display',n=>(n.bucket===b&&document.getElementById('tLab').checked)?null:'none');
 const vis=l=>{const s=id2n.get(lerp(l.source)),t=id2n.get(lerp(l.target));return (s&&s.bucket===b)||(t&&t.bucket===b);};
 link.style('opacity',l=>vis(l)?.7:.04);});
// ----- fit-to-view + reset -----
function fit(){const xs=NODES.map(n=>n.x),ys=NODES.map(n=>n.y);
 const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
 const w=x1-x0||1,h=y1-y0||1,pad=60;
 const k=Math.min((W()-pad)/w,(H()-pad)/h,2.4);
 const tx=W()/2-k*(x0+x1)/2,ty=H()/2-k*(y0+y1)/2;
 svg.transition().duration(450).call(zoomB.transform,d3.zoomIdentity.translate(tx,ty).scale(k));}
document.getElementById('bFit').onclick=fit;
document.getElementById('bReset').onclick=()=>{clearEgo();soloB=null;document.getElementById('panel').style.display='none';
 NODES.forEach(n=>{n.fx=null;n.fy=null;});fitted=false;sim.alpha(.5).restart();};  // unpin dropped nodes + re-settle/fit
svg.on('dblclick.zoom',null).on('dblclick',()=>{clearEgo();soloB=null;});
function fromHash(){const m=/^#node=(.+)$/.exec(location.hash);if(!m)return;
 const id=decodeURIComponent(m[1]);
 if(sim.alpha()<0.06){focusNode(id);}   // already settled -> focus + center now
 else{pendingFocus=id;}                  // still settling -> focus when settled (tick)
}
window.addEventListener('hashchange',fromHash);fromHash();
</script></body></html>"""
HTML=(HTML.replace("__NAV__",NAV).replace("__LEGEND__",legend)
      .replace("__N__",str(len(nodes))).replace("__E__",str(len(links)))
      .replace("__NODES__",json.dumps(nodes)).replace("__LINKS__",json.dumps(links))
      .replace("__BTITLE__",json.dumps(TITLES))
      .replace("__COLORS__",json.dumps(COLORS)))
open(os.path.join(DOCS,"bubblemap.html"),"w").write(HTML)
print(f"wrote docs/bubblemap.html ({len(HTML)} bytes) - {len(nodes)} nodes, {len(links)} links, {len(scc)} in core")
if os.path.isdir(REP): open(os.path.join(REP,"BUBBLEMAP.html"),"w").write(HTML)
