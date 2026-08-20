#!/usr/bin/env python3
"""
wealth_concentration.py - show HOW the standard government income buckets structurally hide
concentration, and what the fuller government data (Fed Distributional Financial Accounts, SCF,
IRS SOI) reveals once you stop using them. Writes data/wealth_concentration.json.

Honesty stance (this matters): the charge is not that anyone fabricated numbers. It is that the
MOST-HEADLINED instrument - the Census money-income bracket table - is built so it *cannot* show
the top tail (fine bins at the bottom, one open bin at the top, top-coding, income-not-wealth,
capital gains excluded, tail-insensitive Gini). Whether those choices (privacy, sample
reliability) amount to "a lie" is a judgment the reader makes; what is demonstrable is (1) the
mechanism of concealment and (2) that other US-government series publish the tail the popular one
erases. We show both and let the gap speak. We do NOT impute a single deceptive intent to a
diffuse agency (that would be the composition fallacy).

Ties to the wage proof: the asset-price inflation that cost labor its wage-hours (gold, equities,
housing) accrued to asset OWNERS as wealth - and Census money income, which excludes capital gains
and unrealized appreciation, is blind to exactly that gain. The instrument misses the transfer by
construction.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

# --- 1. The Census household income brackets: fine at the bottom, one OPEN bin at the top -------
# Representative CPS ASEC household shares (approx, normalized). width_k = bin width in $000s
# (None = open-ended). This asymmetry is the whole point: high resolution where there is no
# concentration, zero resolution where all of it lives.
BRACKETS=[
 ("Under $15k", 8.6, 15), ("$15-25k", 8.0, 10), ("$25-35k", 8.2, 10), ("$35-50k", 11.4, 15),
 ("$50-75k", 16.2, 25), ("$75-100k", 12.4, 25), ("$100-150k", 15.6, 50), ("$150-200k", 8.6, 50),
 ("$200k and over", 11.0, None),   # OPEN: holds the affluent through the billionaire, undistinguished
]

# --- 2. Concept switch: same country, INCOME Gini vs WEALTH Gini --------------------------------
GINI={"income_census_2023": 0.488, "wealth_scf_2022": 0.85}

# --- 3. What the Fed's own data (Distributional Financial Accounts, ~2024) shows -----------------
# net-worth share by group; the tail the income bracket cannot resolve.
WEALTH_SHARES=[
 ("Bottom 50%", 2.5), ("50th-90th", 30.2), ("90th-99th", 36.5), ("Top 1%", 30.8),
]
TOP_0_1=13.8   # the top 0.1% alone (a subset of Top 1%)

# --- 4. Who owns the assets that inflated (SCF): the wage-proof windfall's destination -----------
OWNERSHIP=[
 ("Corporate equities & mutual funds", 89, "top 1% alone hold ~54%"),
 ("Private business equity",           88, "closely-held firms"),
 ("Financial assets (all)",            71, "stocks, bonds, funds, cash"),
 ("Real estate (owner + investment)",  45, "housing is the broadest-held asset"),
]

# --- 5. Top income share: what the bracket table can show vs the truth (IRS/WID) ----------------
TOP_INCOME={"census_bracket_ceiling":"top 5% ~23%  (top 1% not shown at all)",
            "irs_wid_top1":19.0, "irs_wid_top1_capital_gains_incl":22.0}

# --- 6. The structural distortions, each with its mechanism and an honest real/defensible tag ----
DISTORTIONS=[
 ("Open top bin", "The highest bracket is '$200k and over' - unbounded. Everyone from comfortable "
  "to billionaire is one undifferentiated 11%. No top-1%, 0.1%, 0.01% is visible.", "distortion"),
 ("Top-coding", "Public-use CPS incomes above a threshold are replaced with swap/ceiling values, "
  "mechanically capping the very tail that carries the concentration.", "distortion (privacy-motivated)"),
 ("Income, not wealth", "Census measures a yearly FLOW. Concentration lives in the STOCK (net "
  "worth); the wealth Gini (0.85) is nearly double the income Gini (0.49).", "distortion"),
 ("Capital gains excluded", "Census money income omits realized AND unrealized capital gains - "
  "where the top's resources actually accrue (buy-borrow-die). The asset boom is invisible to it.", "distortion"),
 ("Quintiles dissolve the tail", "Slicing into five 20%-of-population buckets averages the top "
  "0.1% in with the merely-affluent; the action is inside the top bucket's top sliver.", "distortion"),
 ("Gini is tail-insensitive", "A single scalar dominated by the middle of the distribution; large "
  "moves in the top 0.1% share barely move it, so the headline gauge under-reports tail dynamics.", "statistical fact"),
 ("Household, not person", "Bucketing by household without size-adjustment; more earners per "
  "household and shrinking household size flatter measured 'household income' growth.", "confounder"),
]

# --- 7. Gini tail-insensitivity, DEMONSTRATED on a synthetic population (illustrative) -----------
def gini(x):
    x=sorted(x); n=len(x); s=sum(x)
    if s==0: return 0.0
    cum=0.0
    for i,v in enumerate(x,1): cum+=i*v
    return (2*cum)/(n*s)-(n+1)/n
def tail_demo():
    # 100000 households, rough US-like income shape (lognormal-ish via deterministic quantiles).
    n=100000; k=n//1000
    # monotone US-like shape (no RNG - scripts ban Random); calibrated to income Gini ~0.46
    base=[ 8000 + 110000*((i/n)**2.3) for i in range(1,n+1) ]
    for j in range(n-k, n):
        base[j]*= 6 + (j-(n-k))/k*30      # top 0.1% pulled up steeply
    g0=gini(base); t0=sum(base[-k:])/sum(base)*100
    # now DOUBLE the top 0.1% incomes (concentration shock), holding the rest fixed
    shocked=base[:]
    for j in range(n-k, n): shocked[j]*=2
    g1=gini(shocked); t1=sum(shocked[-k:])/sum(shocked)*100
    return {"base_gini":round(g0,3),"base_top01_share":round(t0,1),
            "shocked_gini":round(g1,3),"shocked_top01_share":round(t1,1),
            "gini_rise_pct":round((g1-g0)/g0*100,1),"topshare_rise_pct":round((t1-t0)/t0*100,1)}
TAIL=tail_demo()

out={
 "brackets":[{"label":l,"share":s,"width_k":w,"open":w is None} for l,s,w in BRACKETS],
 "gini":GINI,
 "wealth_shares":[{"group":g,"share":s} for g,s in WEALTH_SHARES],"top_0_1_share":TOP_0_1,
 "ownership":[{"asset":a,"top10_share":t,"note":n} for a,t,n in OWNERSHIP],
 "top_income":TOP_INCOME,
 "distortions":[{"name":n,"mechanism":m,"tag":t} for n,m,t in DISTORTIONS],
 "gini_tail_demo":TAIL,
 "sources":"Census CPS ASEC income tables; Federal Reserve Distributional Financial Accounts & "
           "Survey of Consumer Finances; IRS SOI / World Inequality Database. Figures approximate, "
           "recent-year, directional.",
}

# --- console ---
print("="*92); print("WEALTH CONCENTRATION vs the bucket that hides it"); print("="*92)
print(f"income Gini (Census) {GINI['income_census_2023']}  ->  wealth Gini (SCF) {GINI['wealth_scf_2022']}  "
      f"(x{GINI['wealth_scf_2022']/GINI['income_census_2023']:.2f} on a concept switch alone)")
print("Fed net-worth shares:", ", ".join(f"{g} {s}%" for g,s in WEALTH_SHARES), f" | top 0.1% = {TOP_0_1}%")
print("asset ownership by top 10%:", ", ".join(f"{a.split(' (')[0]} {t}%" for a,t,_ in OWNERSHIP))
print(f"top income share - bracket can show: {TOP_INCOME['census_bracket_ceiling']}; "
      f"truth (IRS/WID) top1 ~{TOP_INCOME['irs_wid_top1']}%")
print(f"\nGINI TAIL-INSENSITIVITY (synthetic): top 0.1% share {TAIL['base_top01_share']}% -> "
      f"{TAIL['shocked_top01_share']}% (+{TAIL['topshare_rise_pct']}%), but Gini only "
      f"{TAIL['base_gini']} -> {TAIL['shocked_gini']} (+{TAIL['gini_rise_pct']}%).")
print("  => doubling the tail barely moves the headline gauge - the metric is built to look calm.")
print("\nDISTORTIONS:")
for n,m,t in DISTORTIONS: print(f"  [{t}] {n}: {m[:80]}...")

json.dump(out, open(os.path.join(DATA,"wealth_concentration.json"),"w"), indent=2)
print("\nwrote data/wealth_concentration.json")
