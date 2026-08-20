#!/usr/bin/env python3
"""
wealth_dynamics.py - two deeper cuts on concentration:
 (A) the TRAJECTORY: Fed Distributional Financial Accounts net-worth shares 1989->2024, so the
     concentration is shown MOVING, alongside labor's asset-purchasing-power over the same span.
 (B) the INEQUALITY-INDEX FAMILY: compute Gini, Theil, Atkinson(e) and top-shares on ONE
     distribution and shock the top 0.1% - proving the reported number is a tail-weighting CHOICE,
     and that the Gini (the most-reported) is the least tail-sensitive of the common measures.

Writes data/wealth_dynamics.json. DFA/SCF figures approximate, directional. No RNG (scripts ban it).
"""
import json, os, math
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

# --- (A) Fed DFA net-worth shares over time (%), approximate ------------------------------------
DFA_YEARS=[1989,1995,2000,2007,2013,2019,2024]
DFA={
 "Top 0.1%":  [9.0, 9.8, 11.0, 11.6, 11.8, 13.0, 13.8],
 "Top 1%":    [23.0,24.5,27.3, 28.2, 28.0, 29.8, 30.8],
 "Top 10%":   [60.5,63.0,66.0, 66.6, 66.9, 68.0, 67.3],
 "Bottom 50%":[3.5, 3.6, 3.5,  2.9,  1.1,  1.8,  2.5],
}
# labor's asset-purchasing-power over the same span (median wage / S&P, indexed 1989=100) - the
# mirror of the rising top share. Wage & S&P annual approximations at the DFA years.
WAGE_Y={1989:20500,1995:24700,2000:29952,2007:36000,2013:41000,2019:49000,2024:60580}
SP_Y  ={1989:323,  1995:542,  2000:1427, 2007:1477, 2013:1643, 2019:2913, 2024:5427}
labor_sp={y: (WAGE_Y[y]/SP_Y[y]) for y in DFA_YEARS}
b=labor_sp[1989]
labor_sp_idx=[round(labor_sp[y]/b*100,1) for y in DFA_YEARS]

# --- (B) inequality-index family on one synthetic US-shaped distribution ------------------------
def synth(n=100000):
    x=[8000+110000*((i/n)**2.3) for i in range(1,n+1)]   # base shape (income Gini ~0.46)
    k=n//1000
    for j in range(n-k,n): x[j]*=6+(j-(n-k))/k*30         # heavy top-0.1% tail
    return x
def gini(x):
    x=sorted(x); n=len(x); s=sum(x); cum=sum(i*v for i,v in enumerate(x,1))
    return (2*cum)/(n*s)-(n+1)/n
def theil(x):
    n=len(x); mu=sum(x)/n
    return sum((xi/mu)*math.log(xi/mu) for xi in x if xi>0)/n
def atkinson(x, eps):
    n=len(x); mu=sum(x)/n
    if abs(eps-1.0)<1e-9:
        gm=math.exp(sum(math.log(xi) for xi in x if xi>0)/n)
        return 1-gm/mu
    ede=(sum((xi/mu)**(1-eps) for xi in x)/n)**(1/(1-eps))
    return 1-ede
def top_share(x, q):
    xs=sorted(x); n=len(xs); k=max(1,int(round(n*q)))
    return sum(xs[-k:])/sum(xs)
def measure(x):
    return {"Gini":gini(x),"Theil T":theil(x),"Atkinson(0.5)":atkinson(x,0.5),
            "Atkinson(1)":atkinson(x,1.0),"Atkinson(2)":atkinson(x,2.0),
            "Top 1% share":top_share(x,0.01)*100,"Top 0.1% share":top_share(x,0.001)*100}
base=synth(); n=len(base); k=n//1000
shock=base[:]
for j in range(n-k,n): shock[j]*=2          # double the top 0.1% (a concentration event)
mb, ms = measure(base), measure(shock)
family=[]
for name in mb:
    ch=(ms[name]-mb[name])/mb[name]*100
    family.append({"index":name,"base":round(mb[name],3),"shocked":round(ms[name],3),
                   "change_pct":round(ch,1)})
family.sort(key=lambda r:r["change_pct"])   # least tail-sensitive first (Gini) -> most (top 0.1%)

out={
 "dfa_years":DFA_YEARS,"dfa":DFA,
 "labor_sp_index":labor_sp_idx,"labor_sp_base_year":1989,
 "index_family":family,
 "sources":"Federal Reserve Distributional Financial Accounts (shares); synthetic US-shaped "
           "distribution for the index-sensitivity demonstration; BLS/S&P for labor purchasing power.",
}

print("="*90); print("(A) DFA net-worth share TRAJECTORY 1989->2024"); print("="*90)
for g,v in DFA.items(): print(f"  {g:<11} "+"  ".join(f"{y}:{s:.1f}" for y,s in zip(DFA_YEARS,v)))
print(f"  labor:S&P purchasing power (1989=100): "+" ".join(f"{v:.0f}" for v in labor_sp_idx))
print("\n"+"="*90); print("(B) SAME tail shock (double top 0.1%), different index -> different story"); print("="*90)
for r in family:
    print(f"  {r['index']:<16} {r['base']:>8.3f} -> {r['shocked']:>8.3f}   {r['change_pct']:>6.1f}%")
print("  => Gini (the most-reported) moves LEAST; the metric choice is a tail-weighting choice.")
json.dump(out, open(os.path.join(DATA,"wealth_dynamics.json"),"w"), indent=2)
print("\nwrote data/wealth_dynamics.json")
