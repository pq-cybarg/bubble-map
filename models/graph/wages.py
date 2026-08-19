#!/usr/bin/env python3
"""
wages.py - denominate WAGES in three monies (USD / gold-oz / silver-oz) and build the
labor-side companion to the asset panel. Answers: what does a year of work actually BUY once
the money is held constant, how does that differ by occupation / region / gig-vs-traditional,
and how has the COMPOSITION of who-earns-what shifted over time.

Writes data/wages_denominated.json (inlined by build_multidenom.py so the page is self-contained).

DATA = representative BLS OES national/regional annual figures, rounded, plus the federal
statutory minimum wage (hourly x 2080). Wage levels are approximate and directional (mean vs
median vary by source and year); the metals series is the SAME one used by multi_denomination.py
so the two panels stay consistent. Denomination is an overlay lens, not proof; gig figures are
net-of-cost estimates and vary widely. All clearly caveated on the page.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

# --- same annual-average metal prices as multi_denomination.py (keep in sync) ---
GOLD   = {2000:279, 2007:695, 2013:1411, 2019:1393, 2024:2386}
SILVER = {2000:5.00, 2007:13.38, 2013:23.79, 2019:16.21, 2024:28.0}
YEARS  = [2000, 2007, 2013, 2019, 2024]   # benchmark years present in both metal series

# --- Occupation groups: BLS OES national annual MEAN wage (USD, approx, rounded) ---
# order = roughly high-pay -> low-pay; keys are the 5 benchmark years above.
OCC = {
 "Legal":                         [68000, 96470, 99620, 108610, 128840],
 "Management":                    [67160, 96430, 110550, 123460, 138800],
 "Computer & mathematical":       [55000, 72190, 82010, 93710, 112690],
 "Architecture & engineering":    [52000, 71430, 83340, 91010, 105420],
 "Healthcare practitioners":      [49930, 65020, 76010, 84300, 97880],
 "Education & library":           [39130, 46410, 51500, 57920, 65440],
 "All occupations (mean)":        [34020, 40690, 46440, 53490, 65470],
 "Construction & extraction":     [34870, 42350, 46600, 51290, 62030],
 "Protective service":            [30410, 39250, 43510, 48520, 57070],
 "Sales & related":               [28920, 34740, 38200, 42450, 51290],
 "Production":                    [27600, 32320, 35490, 39160, 47810],
 "Office & admin support":        [27430, 32220, 35530, 39180, 47490],
 "Transportation & moving":       [25940, 31000, 33860, 37310, 45900],
 "Healthcare support":            [21000, 26340, 28300, 32350, 39610],
 "Personal care & service":       [20330, 24120, 27050, 29740, 37150],
 "Building & grounds cleaning":   [20090, 24140, 26610, 30330, 38680],
 "Farming, fishing & forestry":   [19630, 22980, 25160, 30140, 38290],
 "Food prep & serving":           [16130, 19010, 21580, 25470, 34600],
}

# --- Federal minimum wage: statutory hourly at each benchmark year x 2080 hrs ---
MINWAGE_HR = {2000:5.15, 2007:5.85, 2013:7.25, 2019:7.25, 2024:7.25}
MINWAGE = [round(MINWAGE_HR[y]*2080) for y in YEARS]

# --- Regions: BLS annual mean wage by Census region (USD, approx, rounded) ---
REGION = {
 "Northeast": [37500, 46000, 53000, 61000, 77000],
 "West":      [34500, 43000, 50000, 58500, 72500],
 "Midwest":   [31500, 38000, 43500, 50000, 61500],
 "South":     [30500, 37000, 42500, 49500, 61000],
}

# --- Gig vs traditional (2024 snapshot; gig work is a post-2010 category) ---
# traditional = median full-time wage & salary worker (~$1,165/wk x 52); gig = representative
# NET annual for active rideshare/delivery drivers after vehicle costs (estimates vary widely).
GIG_2024 = {
 "Traditional full-time (median)": 60580,
 "Gig driver — gross":            46000,
 "Gig driver — net of costs":     24000,
}

# --- Composition: share of US employment by super-group (%), per benchmark year ---
# 6 super-groups collapsing the 18 OES major groups; columns = YEARS; each column sums to ~100.
COMPOSITION = {
 "Management & professional": [21.5, 22.0, 22.5, 23.2, 24.0],
 "Computer & math":           [ 2.2,  2.6,  3.0,  3.5,  4.2],
 "Healthcare":                [ 6.0,  6.6,  7.4,  8.4,  9.6],
 "Service":                   [17.3, 17.6, 18.2, 18.8, 19.2],
 "Sales & office":            [26.0, 25.2, 24.0, 22.6, 20.8],
 "Blue-collar":               [27.0, 26.0, 24.9, 23.5, 22.2],
}

def denom(series):
    """given [usd per benchmark year], return usd / gold-oz / silver-oz absolute arrays."""
    gold   = [round(series[i]/GOLD[y], 2)   for i, y in enumerate(YEARS)]
    silver = [round(series[i]/SILVER[y], 1) for i, y in enumerate(YEARS)]
    return {"usd": series, "gold": gold, "silver": silver}

def indexed(arr):
    b = arr[0]
    return [round(v/b*100, 1) for v in arr]

def pack(name, series):
    d = denom(series)
    return {
        "name": name, "years": YEARS,
        "usd": d["usd"], "gold": d["gold"], "silver": d["silver"],
        "usd_idx": indexed(d["usd"]), "gold_idx": indexed(d["gold"]), "silver_idx": indexed(d["silver"]),
    }

out = {"years": YEARS, "gold": GOLD, "silver": SILVER}
out["occupations"] = [pack(n, s) for n, s in OCC.items()]
out["minimum_wage"] = pack("Federal minimum wage", MINWAGE)
out["regions"] = [pack(n, s) for n, s in REGION.items()]
out["gig"] = {k: {"usd": v, "gold": round(v/GOLD[2024], 2), "silver": round(v/SILVER[2024], 1)}
              for k, v in GIG_2024.items()}
out["composition"] = {"years": YEARS, "groups": COMPOSITION}

# --- console summary (the money shot) ---
def line(row):
    z = -1
    return (f"  {row['name']:<30} USD idx {row['usd_idx'][z]:>6.0f}   "
            f"GOLD idx {row['gold_idx'][z]:>5.0f}   ({row['gold'][0]:.0f}oz -> {row['gold'][z]:.0f}oz)")

print("="*92)
print("WAGES IN THREE MONIES  (2000=100; oz = ounces of the metal a year's wage buys)")
print("="*92)
print(line(out["minimum_wage"]))
for r in out["occupations"]:
    print(line(r))
print("-"*92)
print("Regions:")
for r in out["regions"]:
    print(line(r))
print("-"*92)
print("Gig vs traditional (2024):")
for k, v in out["gig"].items():
    print(f"  {k:<32} ${v['usd']:>7,}   {v['gold']:>6.2f} oz gold   {v['silver']:>7.1f} oz silver")

json.dump(out, open(os.path.join(DATA, "wages_denominated.json"), "w"), indent=2)
print("\nwrote data/wages_denominated.json  (%d occupations, %d regions)" %
      (len(out["occupations"]), len(out["regions"])))
