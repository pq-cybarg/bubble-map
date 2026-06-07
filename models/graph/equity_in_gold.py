#!/usr/bin/env python3
"""
equity_in_gold.py - re-price public equities in GOLD to separate REAL value capture from
monetary debasement. Result: the broad market and 'old economy' are roughly flat-to-down in
gold (debasement), while the AI-chip/platform oligopoly is genuinely UP in gold (real, and
that very concentration is the systemic concern). Completes the hard-money lens across the stack.
Annual-average levels (approx; S&P/Nasdaq, company market caps); gold from LBMA/macrotrends.
"""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GOLD={2000:279,2007:695,2009:972,2013:1411,2016:1251,2019:1393,2020:1770,2021:1799,2022:1801,2023:1943,2024:2386,2025:3300,2026:4300}
SP500={2000:1430,2007:1480,2009:950,2013:1650,2016:2040,2019:2900,2020:3230,2021:4480,2022:3840,2023:4280,2024:5400,2025:6200,2026:6800}
NVDA={2016:60,2019:140,2020:320,2021:730,2022:360,2023:1000,2024:3000,2025:3500,2026:4300}   # market cap $B
MAG7_2026=18000.0   # combined market cap $B (~$18T)
PRIMES_2026=450.0   # LMT+RTX+NOC+GD combined $B

def reprice(series,label,unit):
    print(f"\n[{label}]  nominal vs in gold (idx to first year = 100)")
    yrs=sorted(series); b_nom=series[yrs[0]]; b_g=series[yrs[0]]/GOLD[yrs[0]]
    rows=[]
    for y in yrs:
        g=series[y]/GOLD[y]
        print(f"  {y}  {unit}{series[y]:>7,.0f}   gold {g:>8.3f}   $idx {series[y]/b_nom*100:>4.0f}   GOLD idx {g/b_g*100:>4.0f}")
        rows.append({"year":y,"level":series[y],"in_gold":round(g,3),"idx_nominal":round(series[y]/b_nom*100),"idx_gold":round(g/b_g*100)})
    return rows

print("="*78); print("EQUITIES IN HARD MONEY  -  real value capture vs debasement"); print("="*78)
out={}
out["sp500"]=reprice(SP500,"S&P 500 (broad market)","")
out["nvda"]=reprice(NVDA,"NVIDIA market cap ($B)","$")
sp_g_2000=SP500[2000]/GOLD[2000]; sp_g_2026=SP500[2026]/GOLD[2026]
nv_g_2016=NVDA[2016]/GOLD[2016]; nv_g_2026=NVDA[2026]/GOLD[2026]
print("\n"+"="*78)
print("THE SPLIT (the honest reveal):")
print(f"  S&P 500 in gold: {sp_g_2000:.2f} oz (2000) -> {sp_g_2026:.2f} oz (2026)  =  {sp_g_2026/sp_g_2000*100-100:+.0f}% in gold")
print(f"    => the BROAD market is ~{abs(sp_g_2026/sp_g_2000*100-100):.0f}% LOWER in gold than 2000 - a lost quarter-century in hard money.")
print(f"  NVIDIA in gold: {nv_g_2016:.2f}B oz (2016) -> {nv_g_2026:.2f}B oz (2026)  =  {nv_g_2026/nv_g_2016*100-100:+.0f}% in gold")
print(f"    => the AI-CHIP oligopoly is massively UP even in gold - REAL value capture, not debasement.")
print(f"  Mag-7 combined ~$18T = {MAG7_2026*1e9/GOLD[2026]/1e9:.1f}B oz gold;  Defense primes ~$450B = {PRIMES_2026*1e9/GOLD[2026]/1e6:.0f}M oz gold.")
print("\nINTERPRETATION: the gold lens SPLITS the market. Housing, CRE, the S&P, and the defense")
print("budget are flat-to-down in gold (monetary debasement). The AI-chip/platform oligopoly (NVDA,")
print("Mag-7) is genuinely up in gold - real value, concentrated into a handful of names. So the")
print("'everything bubble' is two things at once: (1) broad debasement, and (2) a real, extreme")
print("CONCENTRATION of hard-money value into the very oligopoly whose funding is circular (Layer 1).")
out["split"]={"sp500_gold_change_pct_2000_2026":round(sp_g_2026/sp_g_2000*100-100),
              "nvda_gold_change_pct_2016_2026":round(nv_g_2026/nv_g_2016*100-100),
              "mag7_gold_Boz":round(MAG7_2026*1e9/GOLD[2026]/1e9,1),"primes_gold_Moz":round(PRIMES_2026*1e9/GOLD[2026]/1e6)}
json.dump(out,open(os.path.join(ROOT,"data","equity_in_gold.json"),"w"),indent=2)
print("\nwrote data/equity_in_gold.json")
