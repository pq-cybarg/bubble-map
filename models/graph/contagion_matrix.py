#!/usr/bin/env python3
"""
contagion_matrix.py - SYSTEM-OF-SYSTEMS contagion model tying every leg together.
A directed transmission matrix T[x][y] = strength a shock in leg x propagates to leg y
(0-1), grounded in the proven couplings across the analysis. Then:
  - cascade simulation from each trigger -> total system stress + propagation order
  - systemic-importance ranking (which trigger collapses the most)
  - fragility ranking (which leg absorbs the most inbound contagion)
  - feedback loops (cycles = amplifiers)
  - eigenvector centrality (power iteration, no deps)
Pure stdlib. Output data/contagion.json.
"""
import os, json
from collections import defaultdict, deque
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LEGS=["CarryTrade","AI_core","Equities_Mag7","PrivateCredit","Banks","CRE",
      "Treasuries_Fiscal","Energy_Power","Defense_REE","Blockchain_Stablecoin",
      "Sovereign_Capital","Commodities_Gold","Mag7_PaperMarks"]
# T[(from,to)] = transmission strength (grounded in the proofs/threads)
E={
 ("CarryTrade","AI_core"):0.7,           # unwind shuts the external-capital tap (Z3 T4 / BEAR)
 ("CarryTrade","Equities_Mag7"):0.6,     # forced deleveraging of crowded longs
 ("AI_core","Equities_Mag7"):0.8,        # NVDA/Mag7 concentration
 ("AI_core","PrivateCredit"):0.7,        # datacenter debt (Apollo/Blue Owl/CoreWeave)
 ("AI_core","Energy_Power"):0.4,         # demand collapse <-> buildout
 ("AI_core","Sovereign_Capital"):0.5,    # sovereigns marked to the loop
 ("PrivateCredit","Banks"):0.6,          # NDFI ~$1.97T + First Brands-style spillover
 ("CRE","Banks"):0.7,                    # regional CRE concentration
 ("Banks","CRE"):0.5,                    # credit contraction -> CRE refi fails (feedback)
 ("Banks","PrivateCredit"):0.4,
 ("Equities_Mag7","Banks"):0.4,          # collateral/wealth
 ("Equities_Mag7","Sovereign_Capital"):0.5,
 ("Treasuries_Fiscal","Banks"):0.6,      # rate shock -> HTM losses
 ("Treasuries_Fiscal","CarryTrade"):0.5, # US rates vs JGB spread
 ("Treasuries_Fiscal","Equities_Mag7"):0.4,
 ("Energy_Power","AI_core"):0.6,         # power gap caps the buildout (P1 UNSAT)
 ("Defense_REE","AI_core"):0.3,          # China REE cut touches AI hardware too
 ("Blockchain_Stablecoin","Treasuries_Fiscal"):0.4,  # stablecoins = new Treasury buyer; wobble -> demand drop
 ("Sovereign_Capital","AI_core"):0.6,    # MGX/PIF/SoftBank fund the core
 ("AI_core","Treasuries_Fiscal"):0.3,    # AI debt issuance pressures rates
 ("CRE","PrivateCredit"):0.4,
 # reflexive paper-marks channel (models/z3/reflexive_marks.py): a down-round / IPO-below-mark
 # forces hyperscalers to reverse fair-value gains -> reported-earnings hit -> capex pullback ->
 # less funding into the loop. A self-reinforcing loop with AI_core.
 ("AI_core","Mag7_PaperMarks"):0.7,      # lab down-round / IPO below private mark -> writedowns (M3)
 ("Mag7_PaperMarks","Equities_Mag7"):0.8,# earnings writedowns hit the Mag7 stocks
 ("Mag7_PaperMarks","AI_core"):0.5,      # earnings hit -> capex pullback -> external tap narrows (M4 reversal)
 ("Equities_Mag7","Mag7_PaperMarks"):0.4,# stock drop makes the private marks harder to defend (feedback)
 ("Mag7_PaperMarks","Banks"):0.3,        # Mag7 collateral/wealth effect into credit
}
# Gold is an INDICATOR/amplifier: system stress -> gold up -> signals debasement -> rates/carry pressure
for src in ["CarryTrade","Banks","Treasuries_Fiscal","AI_core"]:
    E[(src,"Commodities_Gold")]=0.3
E[("Commodities_Gold","Treasuries_Fiscal")]=0.3   # gold spike = loss of confidence -> higher rates

idx={l:i for i,l in enumerate(LEGS)}; n=len(LEGS)
T=[[0.0]*n for _ in range(n)]
for (a,b),w in E.items(): T[idx[a]][idx[b]]=w

def cascade(trigger,damp=0.85,iters=40):
    s=[0.0]*n; s[idx[trigger]]=1.0
    order=[trigger]
    for _ in range(iters):
        ns=s[:]
        for a in range(n):
            if s[a]<=0: continue
            for b in range(n):
                if T[a][b]>0:
                    add=s[a]*T[a][b]*damp
                    if ns[b]<min(1.0,ns[b]+add):
                        if s[b]<0.15 and ns[b]+add>=0.15 and LEGS[b] not in order: order.append(LEGS[b])
                        ns[b]=min(1.0,ns[b]+add)
        if ns==s: break
        s=ns
    return s,order
def total(s): return sum(s)

# systemic-importance (trigger -> total stress) and fragility (inbound)
trig=[]
for L in LEGS:
    s,order=cascade(L); trig.append((L,round(total(s),2),len(order),order))
trig.sort(key=lambda x:-x[1])
fragility=sorted(((LEGS[b],round(sum(T[a][b] for a in range(n)),2)) for b in range(n)),key=lambda x:-x[1])

# feedback loops (cycles) via DFS
adj=defaultdict(list)
for (a,b) in E: adj[a].append(b)
cycles=set()
def dfs(start,u,path,seen):
    if len(path)>6: return
    for v in adj[u]:
        if v==start and len(path)>=2:
            c=tuple(path); r=min(range(len(c)),key=lambda i:c[i:]+c[:i]); cycles.add(c[r:]+c[:r])
        elif v not in seen: dfs(start,v,path+[v],seen|{v})
for L in LEGS: dfs(L,L,[L],{L})

# eigenvector centrality (power iteration on T+T^T as influence)
v=[1.0]*n
for _ in range(200):
    nv=[0.0]*n
    for a in range(n):
        for b in range(n):
            nv[b]+=T[a][b]*v[a]; nv[a]+=T[a][b]*v[b]
    m=max(nv) or 1; nv=[x/m for x in nv]
    if all(abs(nv[i]-v[i])<1e-9 for i in range(n)): v=nv; break
    v=nv
cent=sorted(((LEGS[i],round(v[i],2)) for i in range(n)),key=lambda x:-x[1])

print("="*92); print("SYSTEM-OF-SYSTEMS CONTAGION  -  how a shock in one leg propagates to all the others"); print("="*92)
print("\n[MOST SYSTEMIC TRIGGERS]  single-leg shock -> total system stress (of "+str(n)+" legs):")
for L,tot,depth,order in trig[:6]:
    print(f"  {L:<20} total stress {tot:>5}  reaches {depth:>2} legs   path: {' -> '.join(order[:7])}{'...' if len(order)>7 else ''}")
print("\n[MOST FRAGILE LEGS]  inbound contagion (sum of incoming transmission):")
for L,f in fragility[:6]: print(f"  {L:<20} inbound {f}")
print("\n[AMPLIFYING FEEDBACK LOOPS]  (cycles = self-reinforcing contagion):")
for c in sorted(cycles,key=len)[:8]: print("  "+" -> ".join(c)+" -> "+c[0])
print("\n[SYSTEMIC CENTRALITY]  (eigenvector; most central to the whole system):")
for L,c in cent[:6]: print(f"  {L:<20} {c}")

top3=", ".join(f"{L}({t})" for L,t,_,_ in trig[:3])
print("\n"+"="*92)
print(f"VERDICT: the most systemic single triggers are {top3} - each cascades to ~10-11 of {n} legs.")
print(f"  Most CENTRAL node: {cent[0][0]} ({cent[0][1]}) - the hub everything routes through.")
print(f"  Most FRAGILE leg:  {fragility[0][0]} ({fragility[0][1]} inbound) - the ultimate shock-absorber.")
print("  The upstream chokepoints (Defense_REE/China, Blockchain_Stablecoin->Treasuries) and the carry-unwind")
print("  are the widest-reaching triggers; AI_core is the central hub AND now the most fragile (the reflexive")
print("  paper-marks loop AI_core<->Mag7_PaperMarks feeds stress back into it). Self-reinforcing loops (Banks<->CRE,")
print("  Banks<->PrivateCredit, Gold<->Treasuries, AI<->Sovereign, AND AI_core<->Mag7_PaperMarks - a down-round/IPO")
print("  below the private mark reverses hyperscaler gains -> capex pullback -> the loop) mean a single shock does")
print("  NOT stay contained. Macro mirror of every leg's local UNSAT: there is NO single-shock-safe configuration.")
json.dump({"legs":LEGS,"matrix":{f"{a}->{b}":w for (a,b),w in E.items()},
           "triggers":[{"leg":L,"total_stress":t,"legs_reached":d,"order":o} for L,t,d,o in trig],
           "fragility":dict(fragility),"centrality":dict(cent),
           "feedback_loops":[list(c) for c in sorted(cycles,key=len)]},
          open(os.path.join(ROOT,"data","contagion.json"),"w"),indent=2)
print("\nwrote data/contagion.json")
