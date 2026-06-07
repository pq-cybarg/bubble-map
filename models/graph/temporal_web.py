#!/usr/bin/env python3
"""
temporal_web.py - the META-graph: how the separate webs (AI core, banking/dereg, crypto,
identity, defense, private credit, Epstein, sovereigns) INTERWEAVE, and which nodes BRIDGE
them across three eras:
   E1 1998-2007  dereg / dotcom / PayPal origin
   E2 2008-2019  GFC / QE / consolidation / crypto birth
   E3 2020-2026  AI capex loop / stablecoins / digital identity

Computes, with pure-stdlib graph algorithms:
  - Brandes betweenness centrality  -> the "weavers" (who connects otherwise-separate webs)
  - cross-LAYER span per node        -> the bridges (nodes touching the most distinct layers)
  - cross-ERA span per node          -> who persists/recurs across eras
  - recurring STRUCTURES (vendor financing, off-balance-sheet SPVs, mark-to-market revenue,
    too-interconnected-to-fail) mapped from their historical origin to their modern instance
Outputs data/temporal_web.json + a printed report.

Edges are tagged evidence = doc (documented relationship) | assoc (documented association,
not causation) | struct (structural/lineage). NOTHING here is a proof of conspiracy; it is a
map of documented connections + their recurrence. Sources in research/temporal-bridges.json.
"""
import json, os
from collections import defaultdict, deque
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

# node -> (layer, era_first, kind)
N = {
 # --- 1998 origin / payments mafia ---
 "PayPal":("payments","E1","org"),"Peter Thiel":("payments","E1","person"),
 "Elon Musk":("payments","E1","person"),"Reid Hoffman":("payments","E1","person"),
 "Max Levchin":("payments","E1","person"),"David Sacks":("payments","E1","person"),
 # --- finance / deregulation ---
 "GLBA 1999":("finance_dereg","E1","event"),"Glass-Steagall":("finance_dereg","E1","law"),
 "Larry Summers":("finance_dereg","E1","person"),"Robert Rubin":("finance_dereg","E1","person"),
 "Alan Greenspan":("finance_dereg","E1","person"),"Phil Gramm":("finance_dereg","E1","person"),
 "Dodd-Frank 2010":("finance_dereg","E2","law"),"EGRRCPA 2018":("finance_dereg","E2","law"),
 "Citigroup":("banking","E1","org"),
 # --- recurring crisis templates / structures ---
 "LTCM 1998":("structure","E1","event"),"Enron 2001":("structure","E1","event"),
 "Dotcom 2000":("structure","E1","event"),"GFC 2008":("structure","E2","event"),
 "Too-Interconnected-to-Fail":("structure","E1","pattern"),
 "Off-Balance-Sheet SPV":("structure","E1","pattern"),
 "Vendor Financing":("structure","E1","pattern"),
 "Mark-to-Market Revenue":("structure","E1","pattern"),
 # --- AI core ---
 "OpenAI":("ai_core","E2","org"),"Sam Altman":("ai_core","E2","person"),
 "NVIDIA":("ai_core","E3","org"),"Jensen Huang":("ai_core","E3","person"),
 "Microsoft":("ai_core","E1","org"),"Oracle":("ai_core","E1","org"),
 "CoreWeave":("ai_core","E3","org"),"Anthropic":("ai_core","E3","org"),
 "Amazon":("ai_core","E1","org"),"Google":("ai_core","E1","org"),
 "xAI":("ai_core","E3","org"),"SoftBank":("sovereign","E2","org"),
 "Stargate":("ai_core","E3","spv"),"Founders Fund":("ai_core","E1","org"),
 "Greylock":("ai_core","E1","org"),"SpaceX":("defense","E1","org"),
 # --- crypto ---
 "Bitcoin":("crypto","E2","proto"),"Ethereum":("crypto","E2","proto"),
 "Vitalik Buterin":("crypto","E2","person"),"Thiel Fellowship":("crypto","E2","prog"),
 "Worldcoin/World ID":("identity","E2","org"),"Circle/USDC":("crypto","E2","org"),
 "Ripple":("crypto","E1","org"),"Stellar":("crypto","E2","org"),"Jed McCaleb":("crypto","E1","person"),
 "Mt. Gox":("crypto","E1","org"),"William Hinman":("crypto","E2","person"),
 "Simpson Thacher":("crypto","E1","org"),"Bullish/Bitmine":("crypto","E3","org"),
 # --- identity / influence ---
 "Larry Ellison":("identity","E1","person"),"Tony Blair Institute":("identity","E3","org"),
 "UK Digital ID":("identity","E3","policy"),"Palantir":("defense","E1","org"),
 "Meta":("identity","E1","org"),"Digital Childhood Alliance":("identity","E3","org"),
 "TikTok US":("identity","E3","org"),
 # --- defense / critical minerals ---
 "Anduril":("defense","E3","org"),"Palmer Luckey":("defense","E3","person"),
 "MP Materials":("defense","E3","org"),"DoD":("defense","E1","gov"),
 # --- private credit / banking ---
 "BlackRock":("private_credit","E2","org"),"Larry Fink":("private_credit","E2","person"),
 "Blackstone":("private_credit","E1","org"),"Apollo":("private_credit","E1","org"),
 "Leon Black":("private_credit","E1","person"),"PIMCO":("private_credit","E2","org"),
 "Blue Owl":("private_credit","E3","org"),"First Brands":("private_credit","E3","org"),
 "UBS":("banking","E1","org"),"JPMorgan":("banking","E1","org"),
 "SVB 2023":("banking","E3","event"),"GENIUS Act 2025":("banking","E3","law"),
 "ICBA":("banking","E2","org"),"ABA":("banking","E1","org"),
 "Joint Bank Stablecoin":("banking","E3","org"),
 # --- sovereign / Gulf ---
 "MGX":("sovereign","E3","org"),"PIF/Mubadala":("sovereign","E2","org"),
 # --- Epstein nexus ---
 "Jeffrey Epstein":("epstein","E1","person"),"Bill Gates":("epstein","E1","person"),
 # --- Japan cluster ---
 "MUFG":("banking","E1","org"),"SBI Holdings":("crypto","E1","org"),"Arm":("ai_core","E2","org"),
 # --- a16z ---
 "a16z":("crypto","E2","org"),
 # --- China tech / Naspers / games-media ---
 "Tencent":("china_tech","E1","org"),"Alibaba":("china_tech","E1","org"),"Ant Group":("china_tech","E2","org"),
 "Naspers/Prosus":("china_tech","E1","org"),"Riot Games":("games_media","E2","org"),"Epic Games":("games_media","E2","org"),
 "Universal Music":("games_media","E2","org"),"Reddit":("games_media","E3","org"),"SCMP":("games_media","E2","org"),"UnionPay":("payments_infra","E2","org"),
 # --- payments infrastructure / BIS / WEF ---
 "Visa":("payments_infra","E1","org"),"Mastercard":("payments_infra","E1","org"),"EMVCo":("payments_infra","E2","org"),
 "Swift":("payments_infra","E1","org"),"BIS":("payments_infra","E1","org"),"Project Agora":("payments_infra","E3","proj"),
 "WEF":("identity","E1","org"),
 # --- more intl banks / lenders / congress ---
 "Jefferies":("private_credit","E1","org"),"HSBC":("banking","E1","org"),"Collective Shout":("identity","E3","org"),
 "Maxine Waters":("congress","E2","person"),"HFSC":("congress","E1","gov"),"OneUnited Bank":("banking","E2","org"),
 # --- crypto exchanges / policy / PACs ---
 "Coinbase":("crypto","E2","org"),"Kraken":("crypto","E2","org"),"Binance":("crypto","E2","org"),
 "Hedera":("crypto","E2","org"),"CLARITY Act":("crypto","E3","law"),"Fairshake PAC":("crypto","E3","pac"),
 # --- crypto crime / nation-state threat actors ---
 "Tornado Cash":("threat_actor","E2","mixer"),"Samourai Wallet":("threat_actor","E2","mixer"),
 "Lazarus Group":("threat_actor","E2","group"),"DPRK":("threat_actor","E1","state"),"UNC threat actors":("threat_actor","E2","group"),
 # --- geopolitical settlement blocs ---
 "BRICS":("sovereign","E2","bloc"),"mBridge":("payments_infra","E3","proj"),"Russia":("threat_actor","E1","state"),
}

# (src, dst, era, relation, evidence)
E = [
 # PayPal origin
 ("Peter Thiel","PayPal","E1","cofounder","doc"),("Elon Musk","PayPal","E1","cofounder","doc"),
 ("Reid Hoffman","PayPal","E1","founding-team","doc"),("Max Levchin","PayPal","E1","cofounder","doc"),
 ("David Sacks","PayPal","E1","exec","doc"),
 ("Peter Thiel","Palantir","E1","cofounder-2003","doc"),("Peter Thiel","Founders Fund","E1","founder-2005","doc"),
 ("Peter Thiel","Meta","E1","first-investor-2004","doc"),("Founders Fund","SpaceX","E2","investor","doc"),
 ("Founders Fund","Anduril","E3","seed-2017","doc"),("Founders Fund","Palantir","E1","investor","doc"),
 ("Peter Thiel","Thiel Fellowship","E2","founder","doc"),("Thiel Fellowship","Vitalik Buterin","E2","grant-2014","doc"),
 ("Vitalik Buterin","Ethereum","E2","cofounder","doc"),("Peter Thiel","Bullish/Bitmine","E3","backer","doc"),
 ("Palmer Luckey","Anduril","E3","cofounder","doc"),("Anduril","DoD","E3","contractor","doc"),
 ("Palantir","DoD","E2","contractor","doc"),("Palantir","UK Digital ID","E3","gov-identity-vendor","assoc"),
 # Musk cluster
 ("Elon Musk","SpaceX","E1","founder","doc"),("Elon Musk","xAI","E3","founder","doc"),
 ("SpaceX","xAI","E3","MERGED (+invest)","doc"),("SpaceX","Google","E3","compute-cancelable","doc"),
 ("Google","SpaceX","E3","~$100B-equity-6pct","doc"),
 ("SpaceX","Anthropic","E3","compute-cancelable","doc"),("SpaceX","NVIDIA","E3","gpu-purchase","doc"),
 ("Elon Musk","OpenAI","E2","cofounder-2015","doc"),
 # Hoffman cluster
 ("Reid Hoffman","Microsoft","E3","board-2017","doc"),("Reid Hoffman","OpenAI","E2","board-till-2023","doc"),
 ("Reid Hoffman","Worldcoin/World ID","E3","investor","doc"),("Reid Hoffman","Greylock","E2","partner","doc"),
 # OpenAI / Altman
 ("Sam Altman","OpenAI","E2","cofounder-CEO","doc"),("Sam Altman","Worldcoin/World ID","E2","cofounder","doc"),
 ("Peter Thiel","OpenAI","E2","early-donor-2015","doc"),
 ("Microsoft","OpenAI","E3","investor-27pct","doc"),("NVIDIA","OpenAI","E3","equity","doc"),
 ("OpenAI","Oracle","E3","compute-Stargate","doc"),("OpenAI","CoreWeave","E3","compute","doc"),
 ("NVIDIA","CoreWeave","E3","equity+backstop","doc"),("NVIDIA","xAI","E3","equity","doc"),
 ("NVIDIA","Anthropic","E3","equity","doc"),("Amazon","Anthropic","E3","equity+compute","doc"),
 ("Google","Anthropic","E3","equity+TPU","doc"),("Jensen Huang","NVIDIA","E3","CEO","doc"),
 ("SoftBank","OpenAI","E3","equity","doc"),("SoftBank","Stargate","E3","equity","doc"),
 ("OpenAI","Stargate","E3","JV","doc"),("Oracle","Stargate","E3","JV","doc"),("MGX","Stargate","E3","JV","doc"),
 ("MGX","OpenAI","E3","equity","doc"),("MGX","Anthropic","E3","equity","doc"),("MGX","xAI","E3","equity","doc"),
 # Summers - the three-era bridge
 ("Larry Summers","GLBA 1999","E1","Treasury-architect","doc"),("Larry Summers","OpenAI","E3","board-2023-2025","doc"),
 ("Larry Summers","Jeffrey Epstein","E2","correspondence","doc"),
 ("Robert Rubin","GLBA 1999","E1","Treasury","doc"),("Robert Rubin","Citigroup","E1","exec-after","doc"),
 ("Alan Greenspan","GLBA 1999","E1","Fed-support","doc"),("Phil Gramm","GLBA 1999","E1","sponsor","doc"),
 ("GLBA 1999","Glass-Steagall","E1","repealed","doc"),("GLBA 1999","GFC 2008","E2","enabled-consolidation","struct"),
 ("Dodd-Frank 2010","GFC 2008","E2","response","doc"),("EGRRCPA 2018","Dodd-Frank 2010","E2","rollback","doc"),
 ("EGRRCPA 2018","SVB 2023","E3","exempted->failed","struct"),
 # recurring structures (origin -> modern instance)
 ("LTCM 1998","Too-Interconnected-to-Fail","E1","template","doc"),
 ("Too-Interconnected-to-Fail","GFC 2008","E2","recurs","struct"),
 ("Too-Interconnected-to-Fail","OpenAI","E3","recurs-AI-core","struct"),
 ("Enron 2001","Off-Balance-Sheet SPV","E1","origin-LJM/Raptor","doc"),
 ("Enron 2001","Mark-to-Market Revenue","E1","origin","doc"),
 ("Off-Balance-Sheet SPV","Stargate","E3","recurs","struct"),("Off-Balance-Sheet SPV","First Brands","E3","recurs","struct"),
 ("Off-Balance-Sheet SPV","Blue Owl","E3","recurs-Hyperion","struct"),
 ("Mark-to-Market Revenue","Oracle","E3","recurs-RPO","struct"),
 ("Dotcom 2000","Vendor Financing","E1","origin-Lucent/Nortel","doc"),
 ("Vendor Financing","NVIDIA","E3","recurs","struct"),
 # private credit / Epstein
 ("Larry Fink","BlackRock","E2","CEO","doc"),("BlackRock","Circle/USDC","E3","manages-reserves","doc"),
 ("BlackRock","Stargate","E3","AI-datacenter-credit","assoc"),("Apollo","Anthropic","E3","datacenter-credit","doc"),
 ("Apollo","xAI","E3","datacenter-credit","doc"),("Leon Black","Apollo","E1","cofounder","doc"),
 ("Leon Black","Jeffrey Epstein","E2","$158-170M-payments","doc"),("Jeffrey Epstein","Bill Gates","E2","association","doc"),
 ("Bill Gates","Tony Blair Institute","E3","funder","doc"),("Blackstone","CoreWeave","E3","debt","doc"),
 ("Blue Owl","Meta","E3","Hyperion-SPV","doc"),("PIMCO","Blue Owl","E3","anchor-lender","doc"),
 ("First Brands","UBS","E3","supply-chain-finance-loss","doc"),
 # identity / Ellison
 ("Larry Ellison","Oracle","E1","founder","doc"),("Larry Ellison","Tony Blair Institute","E3","~$348M-funder","doc"),
 ("Tony Blair Institute","UK Digital ID","E3","advocate","doc"),("Oracle","UK Digital ID","E3","infra-frontrunner","assoc"),
 ("Oracle","TikTok US","E3","algorithm-operator","doc"),("Meta","Digital Childhood Alliance","E3","covert-funder","doc"),
 ("Digital Childhood Alliance","UK Digital ID","E3","age-verification-push","struct"),
 ("Worldcoin/World ID","UK Digital ID","E3","proof-of-personhood","struct"),
 # crypto / SEC
 ("Jed McCaleb","Mt. Gox","E1","founder","doc"),("Jed McCaleb","Ripple","E1","cofounder","doc"),
 ("Jed McCaleb","Stellar","E2","cofounder","doc"),("William Hinman","Simpson Thacher","E1","pension","doc"),
 ("William Hinman","Ethereum","E2","ETH-not-security-2018","doc"),("Simpson Thacher","Ethereum","E2","EEA-member","assoc"),
 # banking lobby / stablecoin
 ("GENIUS Act 2025","Circle/USDC","E3","regulates","doc"),("ICBA","GENIUS Act 2025","E3","lobbied-guardrails","doc"),
 ("ABA","GENIUS Act 2025","E3","lobbied","doc"),("JPMorgan","Joint Bank Stablecoin","E3","consortium","doc"),
 ("BlackRock","Joint Bank Stablecoin","E3","reserve-economics","assoc"),
 ("PIF/Mubadala","MGX","E3","sovereign-parent","doc"),("SoftBank","PIF/Mubadala","E2","Vision-Fund-LP","doc"),
 # --- Japan cluster ---
 ("SoftBank","SBI Holdings","E1","spawned-1999","doc"),("SoftBank","Arm","E2","owns","doc"),("Arm","NVIDIA","E3","chip-IP","struct"),
 ("SBI Holdings","Ripple","E2","~9pct-largest-external","doc"),("MUFG","Ripple","E2","RippleNet","doc"),
 ("SBI Holdings","Circle/USDC","E3","RLUSD-Japan","assoc"),
 # --- a16z bridges crypto + identity + AI ---
 ("a16z","Worldcoin/World ID","E3","investor","doc"),("a16z","Ripple","E3","XRP-Tokyo","assoc"),
 ("a16z","OpenAI","E3","investor","doc"),("a16z","Anduril","E3","investor","assoc"),("a16z","Ethereum","E2","backer","assoc"),
 # --- China tech / Naspers / games-media ---
 ("Naspers/Prosus","Tencent","E1","~23pct-stake","doc"),("Tencent","Riot Games","E2","100pct","doc"),
 ("Tencent","Epic Games","E2","~40pct","doc"),("Tencent","Reddit","E3","stake","doc"),("Tencent","Universal Music","E3","stake","doc"),
 ("Alibaba","Ant Group","E2","affiliate","doc"),("Ant Group","Ethereum","E2","early-experiment","assoc"),("Alibaba","SCMP","E2","owns","doc"),
 # --- payments infra / BIS / WEF ---
 ("Visa","EMVCo","E2","member","doc"),("Mastercard","EMVCo","E2","member","doc"),("UnionPay","EMVCo","E2","member","doc"),
 ("PayPal","Visa","E1","rails","struct"),("Mastercard","Project Agora","E3","participant","doc"),("BIS","Project Agora","E3","leads","doc"),
 ("JPMorgan","Project Agora","E3","participant","doc"),("UBS","Project Agora","E3","participant","doc"),
 ("Swift","Project Agora","E3","participant","doc"),("HSBC","Project Agora","E3","participant","doc"),
 ("Visa","Circle/USDC","E3","stablecoin-settle","doc"),("Mastercard","Circle/USDC","E3","stablecoin-settle","doc"),
 ("Mastercard","Joint Bank Stablecoin","E3","TCH-tokenization","assoc"),
 ("Collective Shout","Visa","E3","payment-censor","doc"),("Collective Shout","Mastercard","E3","payment-censor","doc"),
 ("WEF","UK Digital ID","E3","digital-ID-advocacy","assoc"),("WEF","Tony Blair Institute","E3","Davos-aligned","assoc"),
 ("Jefferies","First Brands","E3","lender","doc"),
 # --- congress / Waters (documented; ethics-cleared) ---
 ("Maxine Waters","HFSC","E2","ranking-member","doc"),("Maxine Waters","OneUnited Bank","E2","husband-stock-ethics-cleared","doc"),
 ("OneUnited Bank","GFC 2008","E2","TARP-12.1M","doc"),("HFSC","GENIUS Act 2025","E3","jurisdiction","doc"),
 ("HFSC","ICBA","E3","lobby-target","assoc"),("HFSC","ABA","E3","lobby-target","assoc"),("Maxine Waters","GENIUS Act 2025","E3","opposed","doc"),
 # --- crypto exchanges / policy / PACs (crypto money -> Congress) ---
 ("Coinbase","Circle/USDC","E2","USDC-cofounder","doc"),("Coinbase","Fairshake PAC","E3","top-funder","doc"),
 ("a16z","Fairshake PAC","E3","funder","doc"),("Ripple","Fairshake PAC","E3","funder","doc"),
 ("Fairshake PAC","HFSC","E3","elects-pro-crypto","assoc"),("Fairshake PAC","GENIUS Act 2025","E3","backed","assoc"),
 ("HFSC","CLARITY Act","E3","jurisdiction","doc"),("Maxine Waters","CLARITY Act","E3","opposed","doc"),("Coinbase","CLARITY Act","E3","industry-backed","assoc"),
 ("Google","Hedera","E2","governing-council","assoc"),("Kraken","Fairshake PAC","E3","funder","assoc"),
 # --- crypto crime / nation-state ---
 ("DPRK","Lazarus Group","E1","state-sponsor","doc"),("Lazarus Group","Tornado Cash","E2","launders-via","doc"),
 ("Lazarus Group","Ethereum","E2","exploits/Bybit-Ronin","doc"),("Tornado Cash","Ethereum","E2","mixer-on","struct"),
 ("Samourai Wallet","Bitcoin","E2","privacy-mixer-DOJ","doc"),("Binance","DPRK","E2","laundering-conduit-alleged","assoc"),
 ("DPRK","UNC threat actors","E2","attribution-overlap","assoc"),("UNC threat actors","Coinbase","E3","targets-exchanges","assoc"),
 # --- geopolitical settlement blocs: West (Agora/SWIFT) vs BRICS (mBridge/UnionPay) ---
 ("BRICS","Swift","E3","alternative-to","struct"),("BRICS","mBridge","E3","cross-border-CBDC","assoc"),
 ("mBridge","BIS","E2","incubated-then-exited","doc"),("BRICS","UnionPay","E3","de-dollar-rails","assoc"),
 ("Project Agora","mBridge","E3","parallel-rival-bloc","struct"),("Russia","BRICS","E2","member-sanctioned","doc"),("Russia","DPRK","E3","aligned","assoc"),
]

# ---- build undirected adjacency ----
adj=defaultdict(set)
for s,d,*_ in E:
    if s in N and d in N: adj[s].add(d); adj[d].add(s)
nodes=list(N.keys())

# ---- Brandes betweenness centrality (unweighted, undirected) ----
bet=dict.fromkeys(nodes,0.0)
for s in nodes:
    S=[]; P={w:[] for w in nodes}; sigma=dict.fromkeys(nodes,0.0); sigma[s]=1.0
    dist=dict.fromkeys(nodes,-1); dist[s]=0; Q=deque([s])
    while Q:
        v=Q.popleft(); S.append(v)
        for w in adj[v]:
            if dist[w]<0: dist[w]=dist[v]+1; Q.append(w)
            if dist[w]==dist[v]+1: sigma[w]+=sigma[v]; P[w].append(v)
    delta=dict.fromkeys(nodes,0.0)
    while S:
        w=S.pop()
        for v in P[w]:
            delta[v]+=(sigma[v]/sigma[w])*(1+delta[w])
        if w!=s: bet[w]+=delta[w]
for k in bet: bet[k]/=2.0   # undirected

# ---- cross-layer + cross-era span ----
layer_span={}; era_span={}; deg={}
for n in nodes:
    nbr_layers={N[m][0] for m in adj[n]} | {N[n][0]}
    nbr_eras={N[m][1] for m in adj[n]} | {N[n][1]}
    layer_span[n]=len(nbr_layers); era_span[n]=len(nbr_eras); deg[n]=len(adj[n])

out={"eras":{"E1":"1998-2007 dereg/dotcom/PayPal","E2":"2008-2019 GFC/QE/crypto-birth","E3":"2020-2026 AI/identity/stablecoin"},
     "n_nodes":len(nodes),"n_edges":len([e for e in E if e[0] in N and e[1] in N]),
     "nodes":{n:{"layer":N[n][0],"era_first":N[n][1],"kind":N[n][2],
                 "betweenness":round(bet[n],1),"degree":deg[n],
                 "layer_span":layer_span[n],"era_span":era_span[n]} for n in nodes},
     "edges":[{"from":s,"to":d,"era":er,"relation":r,"evidence":ev} for s,d,er,r,ev in E if s in N and d in N]}
json.dump(out,open(os.path.join(DATA,"temporal_web.json"),"w"),indent=2)

def top(metric,k=15): return sorted(nodes,key=lambda n:-metric[n])[:k]
print("="*82); print("TEMPORAL META-GRAPH  -  who weaves the webs together, across 1998->2026"); print("="*82)
print(f"nodes={len(nodes)}  edges={out['n_edges']}  layers={len({N[n][0] for n in nodes})}")
print("\n[THE WEAVERS]  highest betweenness centrality (connect otherwise-separate webs):")
for n in top(bet):
    print(f"  {n:<26} betw={bet[n]:>6.1f}  deg={deg[n]:>2}  layers={layer_span[n]}  eras={era_span[n]}  [{N[n][0]}]")
print("\n[CROSS-LAYER BRIDGES]  touch the most distinct layers:")
for n in sorted(nodes,key=lambda n:(-layer_span[n],-bet[n]))[:12]:
    print(f"  {n:<26} layers={layer_span[n]}  (own={N[n][0]}, era1={N[n][1]})  betw={bet[n]:.1f}")
print("\n[CROSS-ERA PERSISTENCE]  nodes whose connections span all 3 eras:")
for n in sorted(nodes,key=lambda n:(-era_span[n],-bet[n])):
    if era_span[n]>=3: print(f"  {n:<26} eras={era_span[n]}  layers={layer_span[n]}  [{N[n][0]}]")
print("\n[RECURRING STRUCTURES]  origin era -> modern instance:")
for s,d,er,r,ev in E:
    if N.get(s,('',))[0]=="structure" and N.get(d,('',))[0]!="structure" and ev=="struct":
        print(f"  {s:<28} -> {d:<14} ({r})")
print("\nwrote data/temporal_web.json")
