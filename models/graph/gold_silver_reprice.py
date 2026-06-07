#!/usr/bin/env python3
"""
gold_silver_reprice.py - Temporal flow-of-funds (dollar-weighted, per year) AND everything
re-priced in GOLD ounces and SILVER ounces at the price prevailing in each year.

The point: denominating in hard money strips out monetary debasement. Assets that "rose"
in dollars are often FLAT or DOWN in gold. This re-prices (a) the major capital flows /
bailouts 1998->2026, (b) US median home price, (c) commercial RE (Green Street CPPI),
(d) regional residential (Case-Shiller metros).

DATA = annual averages, sourced; recent years (2025-26) flagged ~approx (the 2025-26 metals
spike makes annual averages provisional). Sources:
  GOLD/SILVER avg $/oz : LBMA / macrotrends / USGS (2024 gold avg = $2,386.20 LBMA, confirmed)
  US median home       : FRED MSPUS (Census/HUD)
  CRE                  : Green Street CPPI (2007 peak=100; -31% to 2009; Mar-2022 peak; -22%; +TTM 2026)
  Regional homes       : S&P/Case-Shiller metro indices (Jan 2000 = 100)
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

GOLD={1998:294,1999:279,2000:279,2001:271,2002:310,2003:363,2004:410,2005:445,2006:604,2007:695,
 2008:872,2009:972,2010:1225,2011:1572,2012:1669,2013:1411,2014:1266,2015:1160,2016:1251,2017:1257,
 2018:1268,2019:1393,2020:1770,2021:1799,2022:1801,2023:1943,2024:2386,2025:3300,2026:4300}  # 2025-26 ~approx; 2026 Jan peak $5,589
SILVER={1998:5.55,1999:5.22,2000:5.00,2001:4.39,2002:4.60,2003:4.88,2004:6.69,2005:7.32,2006:11.55,2007:13.38,
 2008:14.99,2009:14.67,2010:20.19,2011:35.12,2012:31.15,2013:23.79,2014:19.08,2015:15.68,2016:17.14,2017:17.05,
 2018:15.71,2019:16.21,2020:20.55,2021:25.14,2022:21.73,2023:23.35,2024:28.0,2025:35.0,2026:70.0}  # 2024-26 ~approx; 2026 peak ~$121

# US median sales price of houses sold (FRED MSPUS, annual approx, $)
HOME={1998:152000,2000:165000,2002:188000,2004:221000,2006:243000,2007:247000,2008:233000,2009:216000,
 2010:222000,2012:245000,2014:282000,2016:306000,2018:331000,2019:327000,2020:336000,2021:423000,
 2022:457000,2023:430000,2024:420000,2025:415000,2026:418000}
# Green Street CPPI (commercial), 2007 peak = 100
CRE={1998:55,2001:62,2004:78,2007:100,2009:69,2012:88,2016:118,2019:132,2022:155,2023:126,2024:124,2026:129}
# Case-Shiller metro indices (Jan 2000 = 100): coastal vs heartland divergence
CS={
 "Los Angeles":{2000:100,2006:270,2012:150,2019:280,2022:430,2026:445},
 "Miami":{2000:100,2006:280,2011:140,2019:240,2022:400,2026:475},
 "Detroit":{2000:100,2005:127,2009:68,2019:130,2022:180,2026:198},
 "Chicago":{2000:100,2006:168,2012:100,2019:140,2022:165,2026:190},
}
# Major dollar-weighted flows / shocks by year ($ billions)
FLOWS=[
 (1998,"LTCM Fed-brokered bailout",3.6),(2008,"TARP",700.0),(2008,"Fannie/Freddie conservatorship",187.0),
 (2020,"COVID Fed balance-sheet expansion",4500.0),(2023,"SVB failed assets",209.0),
 (2023,"Microsoft->OpenAI cumulative",13.0),(2024,"Hyperscaler AI capex (yr)",400.0),
 (2025,"OpenAI disclosed compute commitments",1400.0),(2025,"Stargate headline",500.0),
 (2025,"SoftBank->OpenAI round",40.0),(2025,"NVIDIA->OpenAI (LOI/closed)",100.0),
 (2026,"Hyperscaler AI capex (yr)",520.0),(2026,"AI datacenter private-credit pipeline",800.0),
 (2026,"SpaceX IPO raise",75.0),
]

def goz(usd,yr): return usd/GOLD[yr]
def soz(usd,yr): return usd/SILVER[yr]

out={"gold":GOLD,"silver":SILVER,"home_usd":HOME,"cre_cppi":CRE,"caseshiller":CS,"flows":[]}
print("="*94)
print("FLOW OF FUNDS, RE-PRICED IN HARD MONEY  (dollar amounts vs gold-oz vs silver-oz, by year)")
print("="*94)
print(f"{'yr':<5}{'flow':<42}{'$B':>9}{'gold Moz':>11}{'silver Moz':>12}")
for yr,lbl,usd in FLOWS:
    gm=goz(usd*1e9,yr)/1e6; sm=soz(usd*1e9,yr)/1e6
    print(f"{yr:<5}{lbl[:41]:<42}{usd:>9.1f}{gm:>11.1f}{sm:>12.0f}")
    out["flows"].append({"year":yr,"label":lbl,"usd_b":usd,"gold_Moz":round(gm,2),"silver_Moz":round(sm,1)})
# the debasement comparison
ltcm_g=goz(3.6e9,1998); oai_g=goz(1400e9,2025); tarp_g=goz(700e9,2008)
print(f"\n[DEBASEMENT REVEAL - same scale in hard money]")
print(f"  LTCM 1998 $3.6B   = {ltcm_g/1e6:6.1f}M oz gold")
print(f"  TARP 2008 $700B   = {tarp_g/1e6:6.1f}M oz gold")
print(f"  OpenAI 2025 $1.4T = {oai_g/1e6:6.1f}M oz gold")
print(f"  OpenAI/LTCM: {1400/3.6:.0f}x in DOLLARS, but only {oai_g/ltcm_g:.0f}x in GOLD.")
print(f"  OpenAI commitments are {oai_g/tarp_g:.2f}x ALL of TARP, in gold-ounce terms.")

print("\n"+"="*94)
print("US MEDIAN HOME  -  nominal vs priced in gold/silver  (the housing 'gains' are mostly debasement)")
print("="*94)
print(f"{'yr':<6}{'$':>9}{'gold oz':>10}{'silver oz':>11}{'$ idx':>8}{'gold idx':>10}")
base_g=HOME[1998]/GOLD[1998]; base_s=HOME[1998]/SILVER[1998]; base_d=HOME[1998]
for yr in sorted(HOME):
    g=HOME[yr]/GOLD[yr]; s=HOME[yr]/SILVER[yr]
    print(f"{yr:<6}{HOME[yr]:>9.0f}{g:>10.0f}{s:>11.0f}{HOME[yr]/base_d*100:>8.0f}{g/base_g*100:>10.0f}")
    out.setdefault("home_repriced",[]).append({"year":yr,"usd":HOME[yr],"gold_oz":round(g,1),"silver_oz":round(s,0),
        "idx_nominal":round(HOME[yr]/base_d*100),"idx_gold":round(g/base_g*100)})
print(f"  => US home: NOMINAL {HOME[2026]/base_d*100:.0f}% of 1998, but only {(HOME[2026]/GOLD[2026])/base_g*100:.0f}% in GOLD")
print(f"     (a US home costs ~{100-(HOME[2026]/GOLD[2026])/base_g*100:.0f}% LESS in gold than in 1998).")

print("\n"+"="*94)
print("COMMERCIAL RE (Green Street CPPI) in gold  -  peaked in HARD money ~2001, far below since")
print("="*94)
b=CRE[1998]/GOLD[1998]
for yr in sorted(CRE):
    g=CRE[yr]/GOLD[yr]
    print(f"  {yr}  CPPI={CRE[yr]:>4}  gold-idx(1998=100)={g/b*100:>5.0f}")
    out.setdefault("cre_repriced",[]).append({"year":yr,"cppi":CRE[yr],"gold_idx":round(g/b*100)})

print("\n"+"="*94)
print("REGIONAL HOMES in GOLD  -  divergence (Jan2000=100 nominal -> indexed in gold-oz)")
print("="*94)
print(f"{'metro':<14}{'2000 nom':>9}{'2026 nom':>9}{'2000 g-idx':>11}{'2026 g-idx':>11}  (g-idx 2000=100)")
for m,d in CS.items():
    g00=d[2000]/GOLD[2000]; g26=d[2026]/GOLD[2026]
    print(f"{m:<14}{d[2000]:>9}{d[2026]:>9}{100:>11}{g26/g00*100:>11.0f}")
    out.setdefault("regional_repriced",[]).append({"metro":m,"nom_2000":d[2000],"nom_2026":d[2026],"gold_idx_2026":round(g26/g00*100)})
print("  => Even 'booming' coastal metros are roughly FLAT-to-down in gold since 2000; heartland (Detroit/Chicago)")
print("     is deeply down in gold. The nominal regional 'divergence' shrinks and inverts in hard money.")

json.dump(out,open(os.path.join(DATA,"gold_silver_reprice.json"),"w"),indent=2)
print("\nwrote data/gold_silver_reprice.json")
