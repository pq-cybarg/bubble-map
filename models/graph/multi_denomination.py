#!/usr/bin/env python3
"""
multi_denomination.py - denominate the key asset panel in THREE monies (USD, gold-oz,
silver-oz) at the price prevailing in each year, index each to its base year (=100), and
add the GOLD/SILVER RATIO series (currently absent from data/gold_silver_reprice.json).

The point (hard-money lens): a figure that "rose" in dollars is often FLAT or DOWN once the
monetary unit itself is held constant. Silver is the more volatile monetary metal, so the
gold-oz and silver-oz trajectories bracket the debasement. The gold/silver ratio (GSR) is the
classic hard-money gauge — a high GSR = silver historically cheap vs gold. Overlay, not proof.

DATA = annual-average $/oz and annual levels, sourced; 2025-26 metals ~approx (the 2025-26
spike makes annual averages provisional; 2026 intraday peaks noted). Reuses the same series as
gold_silver_reprice.py / equity_in_gold.py so the two stay consistent.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

GOLD={2000:279,2007:695,2009:972,2013:1411,2016:1251,2019:1393,2020:1770,2021:1799,2022:1801,2023:1943,2024:2386,2025:3300,2026:4300}
SILVER={2000:5.00,2007:13.38,2009:14.67,2013:23.79,2016:17.14,2019:16.21,2020:20.55,2021:25.14,2022:21.73,2023:23.35,2024:28.0,2025:35.0,2026:70.0}

# Asset panel (nominal levels; annual approx). Each priced in USD, then converted to metal ounces.
# S&P 500 index level; NVIDIA + Mag-7 market cap ($B); US median home ($); Green Street CRE CPPI (2007=100 nominal).
PANEL={
 "S&P 500 (index)":        {2000:1430,2007:1480,2009:950,2013:1650,2016:2040,2019:2900,2020:3230,2021:4480,2022:3840,2023:4280,2024:5400,2025:6200,2026:6800},
 "NVIDIA (mkt cap $B)":    {2016:60,2019:140,2020:320,2021:730,2022:360,2023:1000,2024:3000,2025:3500,2026:4300},
 "US median home ($)":     {2000:165000,2007:247000,2009:216000,2013:258000,2016:306000,2019:327000,2020:336000,2021:423000,2022:457000,2023:430000,2024:420000,2025:415000,2026:418000},
 "Commercial RE (CPPI)":   {2000:57,2007:100,2009:69,2013:92,2016:118,2019:132,2020:128,2021:148,2022:155,2023:126,2024:124,2025:127,2026:129},
 "Gold (self, $/oz)":      dict(GOLD),
 "Silver (self, $/oz)":    dict(SILVER),
}

def metal(series, table):
    """convert a $-series to ounces of the metal whose annual price is `table` (only where both exist)."""
    return {y: series[y]/table[y] for y in series if y in table}

def index_to_base(series):
    ys=sorted(series); b=series[ys[0]]
    return {y: round(series[y]/b*100, 1) for y in ys}, ys[0]

out={"gold":GOLD, "silver":SILVER}

# --- Gold/Silver Ratio (the missing gauge) ---
years=sorted(set(GOLD)&set(SILVER))
gsr=[{"year":y, "gold":GOLD[y], "silver":SILVER[y], "ratio":round(GOLD[y]/SILVER[y],1)} for y in years]
out["gold_silver_ratio"]=gsr
lo=min(gsr,key=lambda r:r["ratio"]); hi=max(gsr,key=lambda r:r["ratio"])
print("="*84); print("GOLD / SILVER RATIO  (oz of silver to buy 1 oz of gold)"); print("="*84)
for r in gsr: print(f"  {r['year']}   gold ${r['gold']:>5,}   silver ${r['silver']:>6.2f}   GSR {r['ratio']:>6.1f}")
print(f"  range: low {lo['ratio']} ({lo['year']})  ->  high {hi['ratio']} ({hi['year']}); a HIGH GSR = silver cheap vs gold.")

# --- Three-money index grid, per asset ---
print("\n"+"="*84); print("ASSET PANEL indexed to base year (=100) in USD, GOLD-oz, SILVER-oz"); print("="*84)
grid=[]
for name, ser in PANEL.items():
    usd_idx, base = index_to_base(ser)
    gold_idx,_ = index_to_base(metal(ser, GOLD))
    silv_idx,_ = index_to_base(metal(ser, SILVER))
    ys=sorted(usd_idx)
    row={"asset":name, "base_year":base, "years":ys,
         "usd":[usd_idx[y] for y in ys],
         "gold":[gold_idx.get(y) for y in ys],
         "silver":[silv_idx.get(y) for y in ys]}
    grid.append(row)
    a,z = ys[0], ys[-1]
    print(f"\n[{name}]  base {base}=100")
    print(f"   {z}:  USD {usd_idx[z]:>6.0f}   gold {gold_idx.get(z,float('nan')):>6.0f}   silver {silv_idx.get(z,float('nan')):>6.0f}   (idx, {base}=100)")
out["denomination_grid"]=grid

# --- The honest split, in one line per asset ---
print("\n"+"="*84); print("THE SPLIT (endpoint index, base=100): dollars flatter than they look in hard money"); print("="*84)
for row in grid:
    z=row["years"][-1]
    print(f"  {row['asset']:<24} USD {row['usd'][-1]:>6.0f}   GOLD {row['gold'][-1]:>6.0f}   SILVER {row['silver'][-1]:>6.0f}")

json.dump(out, open(os.path.join(DATA,"multi_denomination.json"),"w"), indent=2)
print("\nwrote data/multi_denomination.json")
