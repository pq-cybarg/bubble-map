#!/usr/bin/env python3
"""
defense_web.py - the DEFENSE leg: primes + defense-tech (Anduril/Palantir/SpaceX) x the
rare-earth chokepoint, dollar-weighted and gold-priced.

Shows:
  1. The capital web (DoD budget -> primes/defense-tech; VC -> defense-tech).
  2. The rare-earth single-point-of-failure: ~all flagship US weapons depend on China-
     controlled samarium / heavy-REE magnets, and China auto-denies foreign-military use
     from Dec 1 2025, while domestic supply isn't at scale until 2027-2028.
  3. The DEBASEMENT reveal: the "$1 trillion military" buys FAR less gold than the 1998 one.
Sources in research/defense-rare-earth.json.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")
GOLD={1998:294,2008:872,2016:1251,2020:1770,2024:2386,2026:4300}

# --- capital web (USD B; market cap / valuation / contract where noted) ---
NODES={
 "DoD":("buyer","FY26 topline ~$1,000B ($838.7B approp + $150B OBBB); FY27 request ~$1,500B"),
 "Lockheed Martin":("prime","~$100B mkt cap; largest US samarium user (F-35)"),
 "RTX":("prime","~$190B; missiles/radar"),"Northrop Grumman":("prime","~$80B; B-21/ICBM"),
 "General Dynamics":("prime","~$80B; subs/land"),"Boeing Defense":("prime","segment of BA"),
 "Anduril":("defense_tech","$30.5B (Jun-2025 Series G) -> $61B (May-2026 Series H); rev ~$2.2B 2025"),
 "Palantir":("defense_tech","~$350B mkt cap (approx); Army Maven / ~$10B enterprise deal"),
 "SpaceX Starshield":("defense_tech","mil Starlink; part of SpaceX (SPCX)"),
 "Founders Fund":("financier","led Anduril $2.5B Series G - $1B largest-ever FF check"),
 "a16z":("financier","co-led Anduril $5B Series H"),"Thrive Capital":("financier","co-led Series H"),
 "China REE":("chokepoint","~70% mining, ~90% processing, ~100% samarium, ~99% heavy-REE separation"),
 "MP Materials":("domestic","DoD ~15% equity + $110/kg NdPr floor; magnets ~2027"),
 "USA Rare Earth":("domestic","magnet plant; ~2027-2028"),
}
# dollar-weighted capital edges (USD B)
CAPITAL=[
 ("DoD","Lockheed Martin","contract",70,"largest DoD vendor (F-35 etc.)"),
 ("DoD","RTX","contract",40,"missiles/radar"),("DoD","Northrop Grumman","contract",30,"B-21/Sentinel"),
 ("DoD","General Dynamics","contract",30,"subs/land"),("DoD","Anduril","contract",22,"Army IVAS reassigned + enterprise"),
 ("DoD","Palantir","contract",10,"Army enterprise/Maven"),("DoD","MP Materials","equity+floor",0.55,"~15% + price floor + loan"),
 ("Founders Fund","Anduril","equity",1.0,"largest FF check"),("a16z","Anduril","equity",2.5,"Series H co-lead (part of $5B)"),
 ("Thrive Capital","Anduril","equity",2.5,"Series H co-lead (part of $5B)"),
]
# rare-earth dependency: kg of REE per unit, and samarium kg/unit; China share of that input
SYSTEMS={
 "F-35":{"ree_kg":418,"samarium_kg":22.6,"annual_units":150},
 "Virginia-class sub":{"ree_kg":4200,"samarium_kg":50,"annual_units":2},
 "Arleigh Burke destroyer":{"ree_kg":2360,"samarium_kg":30,"annual_units":2},
 "Tomahawk / missiles":{"ree_kg":5,"samarium_kg":1,"annual_units":2000},
}
CHINA_SHARE={"samarium":1.00,"heavy_ree_processing":0.90,"ndfeb_magnets":0.90}

print("="*88)
print("DEFENSE WEB  -  primes + defense-tech x the rare-earth chokepoint")
print("="*88)
print("\n[CAPITAL FLOWS] dollar-weighted ($B/yr contract or one-time equity):")
flows=[]
for s,d,k,amt,note in CAPITAL:
    g=amt*1e9/GOLD[2026]/1e6
    print(f"  {s:<16} -> {d:<18} {k:<12} ${amt:>5}B  ({g:.1f} M oz gold)  {note}")
    flows.append({"from":s,"to":d,"kind":k,"usd_b":amt,"gold_Moz":round(g,2),"note":note})

print("\n[RARE-EARTH CHOKEPOINT] annual samarium demand vs the China single-point-of-failure:")
total_sm=0.0
for sys,v in SYSTEMS.items():
    sm=v["samarium_kg"]*v["annual_units"]; total_sm+=sm
    print(f"  {sys:<26} {v['annual_units']:>5}/yr x {v['samarium_kg']:>5} kg Sm = {sm:>8.0f} kg/yr  (REE {v['ree_kg']} kg/unit)")
print(f"  {'TOTAL annual samarium demand':<26} {'':>5}    {'':>5}      {total_sm:>8.0f} kg/yr")
print(f"  China share of samarium supply: {CHINA_SHARE['samarium']*100:.0f}%   ->  ex-China supply to US military TODAY ~ 0 kg")
print(f"  China auto-DENIES foreign-military export licenses from Dec 1 2025; US magnet scale ~2027-2028.")
print(f"  => 100% of these flagship systems have a CHINA single-point-of-failure in 2026 (see defense_chokepoint.py).")

print("\n[DEBASEMENT REVEAL] the US defense budget in gold (nominal up 3.7x, but DOWN ~75% in gold):")
DOD={1998:270,2008:612,2016:580,2020:721,2024:842,2026:1000}
base=DOD[1998]/GOLD[1998]
for yr in sorted(DOD):
    g=DOD[yr]*1e9/GOLD[yr]/1e6
    print(f"  {yr}  ${DOD[yr]:>5}B   {g:>6.0f} M oz gold   (gold idx 1998=100: {(DOD[yr]/GOLD[yr])/base*100:>3.0f})")
print(f"  => The '$1 trillion military' (2026) buys ~{(DOD[2026]/GOLD[2026])/base*100:.0f}% of the GOLD the 1998")
print("     (~$270B) military did. In hard money, US defense purchasing power has shrunk ~75% while the")
print("     critical-mineral inputs are controlled by the adversary it is arming against.")

json.dump({"nodes":{k:{"role":v[0],"note":v[1]} for k,v in NODES.items()},"capital_flows":flows,
           "systems":SYSTEMS,"china_share":CHINA_SHARE,
           "dod_budget":{str(y):DOD[y] for y in DOD},"gold":{str(y):GOLD[y] for y in GOLD}},
          open(os.path.join(DATA,"defense_web.json"),"w"),indent=2)
print("\nwrote data/defense_web.json")
