#!/usr/bin/env python3
"""
build_graph.py - Consolidate heterogeneous research/*.json into ONE canonical
funding graph, then run structural formal analysis:
  - alias normalization + edge dedupe (+ 'cancelable' flag)
  - Tarjan strongly-connected components (the formal definition of "circular")
  - DUAL SCC: all edges vs. excluding-cancelable -> shows SpaceX entering/leaving the core
  - elementary cycle enumeration
  - circularity-exposure metric per node
  - NVIDIA vendor-financing self-funding ratio (funded vs headline)
Outputs: data/graph.json, data/edges.csv, data/entities.csv + printed proof report.
Pure stdlib.
"""
import json, glob, csv, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

ALIAS = {
 "nvidia":"NVIDIA","NVIDIA":"NVIDIA","openai":"OpenAI","OpenAI":"OpenAI","OPENAI":"OpenAI",
 "microsoft":"Microsoft","Microsoft":"Microsoft","MSFT":"Microsoft","oracle":"Oracle","Oracle":"Oracle","ORCL":"Oracle",
 "coreweave":"CoreWeave","CoreWeave":"CoreWeave","CRWV":"CoreWeave","GOOGL":"Google","Google":"Google","Alphabet":"Google",
 "AMZN":"Amazon","Amazon":"Amazon","AWS":"Amazon","ANTHROPIC":"Anthropic","Anthropic":"Anthropic",
 "AVGO":"Broadcom","Broadcom":"Broadcom","AMD":"AMD","META":"Meta","Meta":"Meta","META_HYPERION_JV":"Meta_Hyperion_SPV",
 "xAI":"xAI","XAI":"xAI","SoftBank":"SoftBank","softbank":"SoftBank","stargate":"Stargate","Stargate":"Stargate",
 "mgx":"MGX","MGX":"MGX","Intel":"Intel","Nokia":"Nokia","Mistral":"Mistral","Nscale":"Nscale","nscale":"Nscale",
 "lambda":"Lambda","Lambda":"Lambda","crusoe":"Crusoe","Crusoe":"Crusoe","nebius":"Nebius","Nebius":"Nebius",
 "vantage":"Vantage","Vantage":"Vantage","Disney":"Disney",
 "Disney+NBCUniversal+WarnerBrosDiscovery":"Disney_Studios_Coalition","Midjourney":"Midjourney",
 "blackstone":"Blackstone","Blackstone":"Blackstone","BLUEOWL":"BlueOwl","PIMCO":"PIMCO","BLACKROCK":"BlackRock",
 "APOLLO_BLACKSTONE":"Apollo_Blackstone","Apollo":"Apollo","GIC":"GIC","jpmorgan":"JPMorgan",
 "balance_sheet":"SINK_debt","bondholders":"SINK_bondmarket","BONDMARKET":"SINK_bondmarket","lenders":"SINK_lenders",
 "CAPEX":"SINK_capex","AI_BACKLOG":"SINK_backlog","AVGO_XPU_PLATFORM":"Broadcom","ANTHROPIC_INVESTORS":"SINK_investors",
 "US commercial banks":"US_Banks",
 "SpaceX":"SpaceX","SpaceX_IPO_Public_Markets":"SpaceX_IPO_Public","Starlink_Subscribers":"Starlink_Subscribers",
 "US_Government":"US_Government","MP_Materials":"MP_Materials","Defense_Primes":"Defense_Primes","Apple":"Apple",
}
def canon(n):
    n=(n or "?").strip()
    if n in ALIAS: return ALIAS[n]
    return ALIAS.get(n.split("(")[0].strip(), n.split("(")[0].strip())

def iclass(instr):
    s=(instr or "").lower()
    if "warrant" in s: return "warrant"
    if "backstop" in s or "take-or-pay" in s: return "backstop"
    if "gpu_purchase" in s or "systems purchases" in s or ("gpu" in s and "purchase" in s): return "gpu_purchase"
    if "equity_method_loss" in s: return "equity_method_loss"
    if "revenue_share" in s or "revenue share" in s: return "revenue_share"
    if "ipo_proceeds" in s: return "ipo_proceeds"
    if "exogenous_revenue" in s: return "exogenous_revenue"
    if "equity" in s: return "equity"
    if "debt" in s or "bond" in s or "loan" in s: return "debt"
    if "ip_litigation" in s: return "ip_litigation"
    if "ip_license" in s: return "ip_license"
    if "cease" in s: return "ip_cease_desist"
    if any(k in s for k in ["compute","cloud","azure","aws","capacity","tpu","xpu","silicon","accelerator","backlog"]): return "compute_commitment"
    if "offtake" in s: return "offtake"
    if "capital expenditure" in s or "capex" in s: return "capex"
    return "other"

NODE_META = {
 "NVIDIA":("chip_vendor",True),"AMD":("chip_vendor",True),"Broadcom":("chip_vendor",True),"Intel":("chip_vendor",True),
 "OpenAI":("ai_lab",False),"Anthropic":("ai_lab",False),"xAI":("ai_lab",False),"Mistral":("ai_lab",False),
 "Microsoft":("hyperscaler",True),"Google":("hyperscaler",True),"Amazon":("hyperscaler",True),"Meta":("hyperscaler",True),
 "Oracle":("hyperscaler",True),"CoreWeave":("neocloud",False),"Nscale":("neocloud",False),"Lambda":("neocloud",False),
 "Crusoe":("neocloud",False),"Nebius":("neocloud",False),"Vantage":("neocloud",False),
 "SpaceX":("space_real_economy",True),"SoftBank":("financier",True),"MGX":("financier",True),"GIC":("financier",True),
 "Blackstone":("private_credit",True),"BlueOwl":("private_credit",True),"PIMCO":("private_credit",True),
 "BlackRock":("private_credit",True),"Apollo":("private_credit",True),"Apollo_Blackstone":("private_credit",True),
 "JPMorgan":("bank",True),"US_Banks":("bank",True),"Stargate":("spv",False),"Meta_Hyperion_SPV":("spv",False),
 "Disney":("ip_rightsholder",True),"Disney_Studios_Coalition":("ip_rightsholder",True),"Midjourney":("ai_lab",False),
 "Nokia":("telecom",True),"US_Government":("state",True),"MP_Materials":("critical_minerals",True),
 "Defense_Primes":("defense",True),"Apple":("hyperscaler",True),
}

edges=[]
def add(frm,to,instr,amt,status,circ,src,note="",cancelable=False):
    f,t=canon(frm),canon(to)
    if f==t: return
    edges.append({"from":f,"to":t,"instrument":iclass(instr),"raw_instrument":instr,
        "amount_usd":amt if isinstance(amt,(int,float)) else None,"status":status or "",
        "declared_circular":bool(circ),"cancelable":bool(cancelable),"source_file":src,"note":note})

for fn in glob.glob(os.path.join(RES,"*.json")):
    try: d=json.load(open(fn))
    except: continue
    base=os.path.basename(fn)
    for e in (d.get("edges") or []):
        add(e.get("from"),e.get("to"),e.get("raw_instrument") or e.get("instrument"),
            e.get("amount_usd"),e.get("status"),e.get("circular"),base,e.get("notes",""),e.get("cancelable"))
    for e in (d.get("chain_edges") or []):
        add(e.get("from"),e.get("to"),e.get("instrument"),e.get("amount_usd"),e.get("date",""),False,base,e.get("notes",""))

# critical-minerals STATE-circularity (parallel structure; deliberately NOT part of the AI SCC)
edges += [
 {"from":"US_Government","to":"MP_Materials","instrument":"equity","raw_instrument":"DoD $400M convertible pref ~15% + $110/kg NdPr price floor + $150M loan","amount_usd":400000000,"status":"closed","declared_circular":True,"cancelable":False,"source_file":"macro-critical-minerals.json","note":"STATE as circular vendor-financier of the supply chain"},
 {"from":"MP_Materials","to":"Defense_Primes","instrument":"offtake","raw_instrument":"10yr 100% DoD offtake -> magnets for missiles/F-35/radar","amount_usd":None,"status":"committed","declared_circular":True,"cancelable":False,"source_file":"macro-critical-minerals.json","note":""},
 {"from":"Apple","to":"MP_Materials","instrument":"offtake","raw_instrument":"$500M recycled-magnet supply deal","amount_usd":500000000,"status":"committed","declared_circular":False,"cancelable":False,"source_file":"macro-critical-minerals.json","note":""},
]

# dedupe by (from,to,instrument): keep MAX amount, OR the flags, merge sources
dd={}
for e in edges:
    k=(e["from"],e["to"],e["instrument"])
    if k not in dd: dd[k]=e
    else:
        o=dd[k]
        if (e["amount_usd"] or 0)>(o["amount_usd"] or 0): o["amount_usd"]=e["amount_usd"]; o["raw_instrument"]=e["raw_instrument"]
        o["declared_circular"]=o["declared_circular"] or e["declared_circular"]
        o["cancelable"]=o.get("cancelable") or e.get("cancelable")
        if e["source_file"] not in o["source_file"]: o["source_file"]+=","+e["source_file"]
E=list(dd.values())
nodes=sorted({e["from"] for e in E}|{e["to"] for e in E})

def meta(n):
    if n.startswith("SINK_"): return ("sink",True)
    if n in NODE_META: return NODE_META[n]
    if "Starlink" in n or "SpaceX_IPO" in n: return ("exogenous_source",True)
    return ("other",True)
entities={n:{"sector":meta(n)[0],"has_exogenous_revenue":meta(n)[1]} for n in nodes}

# ---- Tarjan SCC as a function over an edge subset ----
sys.setrecursionlimit(100000)
def scc_core(edge_list):
    adj=defaultdict(list)
    for e in edge_list: adj[e["from"]].append(e["to"])
    idx={};low={};onstk={};stk=[];comps=[];c=[0]
    def sc(v):
        idx[v]=low[v]=c[0];c[0]+=1;stk.append(v);onstk[v]=True
        for w in adj[v]:
            if w not in idx: sc(w);low[v]=min(low[v],low[w])
            elif onstk.get(w): low[v]=min(low[v],idx[w])
        if low[v]==idx[v]:
            comp=[]
            while True:
                w=stk.pop();onstk[w]=False;comp.append(w)
                if w==v:break
            comps.append(comp)
    for v in {e["from"] for e in edge_list}|{e["to"] for e in edge_list}:
        if v not in idx: sc(v)
    sccs=[c2 for c2 in comps if len(c2)>1]; sccs.sort(key=len,reverse=True)
    core=set().union(*sccs) if sccs else set()
    return sccs,core,adj

sccs_all,core_all,adj=scc_core(E)
sccs_robust,core_robust,_=scc_core([e for e in E if not e.get("cancelable")])

# elementary cycles (bounded) over full graph
cycset=set();cyclist=[]
def dfs(start,v,path,seen):
    if len(path)>8: return
    for w in adj[v]:
        if w==start and len(path)>=2:
            cyc=tuple(path);rot=min(range(len(cyc)),key=lambda i:cyc[i:]+cyc[:i]);key=cyc[rot:]+cyc[:rot]
            if key not in cycset: cycset.add(key);cyclist.append(list(key))
        elif w in core_all and w not in seen: dfs(start,w,path+[w],seen|{w})
for s in core_all: dfs(s,s,[s],{s})
cyclist.sort(key=len)

def amt(e): return e["amount_usd"] or 0
expo={}
for n in nodes:
    tot=sum(amt(e) for e in E if e["from"]==n or e["to"]==n)
    cir=sum(amt(e) for e in E if (e["from"]==n or e["to"]==n) and e["from"] in core_all and e["to"] in core_all)
    expo[n]={"total_usd":tot,"circular_usd":cir,"circularity_ratio":round(cir/tot,3) if tot else 0.0,
             "in_core_scc":n in core_all,"in_robust_core":n in core_robust}

nvda_funded=sum(amt(e) for e in E if e["from"]=="NVIDIA" and e["instrument"] in("equity","backstop","warrant") and e["to"] in core_all and (e["amount_usd"] or 0)<=35e9)
nvda_head=sum(amt(e) for e in E if e["from"]=="NVIDIA" and e["instrument"] in("equity","backstop","warrant") and e["to"] in core_all)
nvda_rev=215.9e9
selffund={"funded_usd":nvda_funded,"headline_usd":nvda_head,"nvidia_fy26_revenue_usd":nvda_rev,
          "funded_ratio":round(nvda_funded/nvda_rev,3),"headline_ratio":round(nvda_head/nvda_rev,3)}

graph={"entities":entities,"edges":E,"analysis":{
    "num_nodes":len(nodes),"num_edges":len(E),
    "core_scc_all":sorted(core_all),"core_scc_all_size":len(core_all),
    "core_scc_robust_excl_cancelable":sorted(core_robust),"core_scc_robust_size":len(core_robust),
    "nodes_only_circular_via_cancelable":sorted(core_all-core_robust),
    "num_elementary_cycles":len(cyclist),"elementary_cycles":cyclist,
    "circularity_exposure":expo,"nvidia_self_funding":selffund}}
json.dump(graph,open(os.path.join(DATA,"graph.json"),"w"),indent=2)
with open(os.path.join(DATA,"edges.csv"),"w",newline="") as f:
    w=csv.writer(f);w.writerow(["from","to","instrument","amount_usd","status","declared_circular","cancelable","source_file"])
    for e in sorted(E,key=lambda x:-(x["amount_usd"] or 0)):
        w.writerow([e["from"],e["to"],e["instrument"],e["amount_usd"],e["status"],e["declared_circular"],e["cancelable"],e["source_file"]])
with open(os.path.join(DATA,"entities.csv"),"w",newline="") as f:
    w=csv.writer(f);w.writerow(["node","sector","has_exogenous_revenue","in_core_scc","in_robust_core","circularity_ratio"])
    for n in nodes: w.writerow([n,entities[n]["sector"],entities[n]["has_exogenous_revenue"],expo[n]["in_core_scc"],expo[n]["in_robust_core"],expo[n]["circularity_ratio"]])

print("="*74+"\nSTRUCTURAL FORMAL ANALYSIS  -  AI circular-funding graph\n"+"="*74)
print(f"nodes={len(nodes)}  edges={len(E)}")
print(f"\n[S1] Core SCC (ALL edges): |SCC|={len(core_all)}")
print("     "+", ".join(sorted(core_all)))
print(f"\n[S1b] Core SCC (EXCLUDING cancelable contracts): |SCC|={len(core_robust)}")
print("     "+", ".join(sorted(core_robust)))
print(f"\n[S1c] Nodes circular ONLY via CANCELABLE edges: {sorted(core_all-core_robust)}")
print("      => These are conditionally entangled; their circularity can be unwound by contract termination.")
print(f"\n[S2] Elementary directed cycles (len<=8): {len(cyclist)}.  Shortest:")
for c in cyclist[:12]: print("    "+" -> ".join(c)+" -> "+c[0])
print(f"\n[METRIC] Circularity exposure (core nodes):")
for n in sorted(core_all,key=lambda x:-expo[x]["circularity_ratio"]):
    tag="" if n in core_robust else "  <-- cancelable-only"
    print(f"    {n:<16} ratio={expo[n]['circularity_ratio']:.2f}  circ=${expo[n]['circular_usd']/1e9:,.0f}B{tag}")
print(f"\n[METRIC] SpaceX vs core:")
for n in ["SpaceX","NVIDIA","OpenAI","CoreWeave","Oracle"]:
    if n in expo: print(f"    {n:<10} in_core_all={expo[n]['in_core_scc']}  in_robust_core(excl-cancelable)={expo[n]['in_robust_core']}  exo_rev={entities[n]['has_exogenous_revenue']}")
print(f"\n[METRIC] NVIDIA vendor-financing self-funding ratio:")
print(f"    funded-only  ${selffund['funded_usd']/1e9:,.0f}B / ${nvda_rev/1e9:,.0f}B = {selffund['funded_ratio']:.1%}")
print(f"    headline     ${selffund['headline_usd']/1e9:,.0f}B / ${nvda_rev/1e9:,.0f}B = {selffund['headline_ratio']:.1%}")
print("\nwrote data/graph.json, data/edges.csv, data/entities.csv")
