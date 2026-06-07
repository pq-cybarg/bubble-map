#!/usr/bin/env python3
"""
energy_web.py - the ENERGY/POWER leg: the AI+defense power bottleneck, the hyperscaler
nuclear/SMR PPA web, the gas-turbine lead-time wall, and the Russia uranium-enrichment
chokepoint - dollar-weighted and gold-priced.

Completes the THREE physical chokepoints of the buildout:
  compute capital (Layer 1) -> rare earths/China (defense leg) -> POWER + nuclear fuel/Russia (here).
Sources in research/energy-power.json.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); GOLD2026=4300

# hyperscaler -> power deals (MW, $ where disclosed)
POWER_DEALS=[
 ("Microsoft","Constellation/Three Mile Island","nuclear restart",835,16.0,"20yr PPA, ~2028 online"),
 ("Amazon","Talen/Susquehanna","nuclear PPA",1920,None,"through 2042 + SMR exploration"),
 ("Google","Kairos Power","SMR",500,None,"first corp SMR fleet deal; 50MW by 2030"),
 ("Meta","Oklo","SMR",1200,None,"1.2GW campus; +RFP 1-4GW nuclear"),
 ("Oracle","SMR (3 reactors)","SMR",1000,None,"gigawatt datacenter design"),
 ("Crusoe","GE Vernova","gas turbines",None,None,"19 turbines ordered (behind-the-meter gas)"),
]
# speculative supplier vehicles riding the energy/defense/minerals narrative (user-flagged)
SPEC_SUPPLIERS={
 "TMC":"deep-sea Ni/Cu/Co/Mn nodules - BATTERY/grid metals; Trump seabed EO; pre-commercial",
 "CRML":"Tanbreez Greenland REE - magnets for grid/defense; pre-revenue (~2028-29)",
 "LAES/WKEY":"SEALSQ/WISeKey PQC chips + WISeSat sats on SpaceX rideshare; narrative microcaps",
 "SPCX":"SpaceX - Starshield (defense) + Starlink (power-hungry LEO) + compute reselling",
}

print("="*86); print("ENERGY / POWER LEG  -  the AI+defense power bottleneck"); print("="*86)
print("\n[HYPERSCALER POWER DEALS] (MW; $ where disclosed; gold where priced):")
deals=[]
for who,src,kind,mw,usd,note in POWER_DEALS:
    g=f"{usd*1e9/GOLD2026/1e6:.1f} M oz" if usd else "-"
    print(f"  {who:<10} <- {src:<28} {kind:<16} {str(mw)+' MW' if mw else '   -':>8}  ${usd if usd else '-':>5}B ({g})  {note}")
    deals.append({"buyer":who,"source":src,"kind":kind,"mw":mw,"usd_b":usd,"note":note})
print("  Big tech has signed 10GW+ of new US nuclear in the past year; SMR mkt $6.9B(2025)->$13.8B(2032).")

print("\n[DEMAND vs the GRID]  AI data centers:")
print("  US data-center share of electricity: 4.4% (2023, DOE) -> 6.7-12% by 2028; ~HALF of US load growth to 2030.")
print("  PJM capacity auction hit the CAP 3x running ($329->$333.44/MW-day); ~$9.3B of the increase is data-center driven.")
pjm=333.44; print(f"  PJM cap ${pjm}/MW-day  =  {pjm/GOLD2026:.3f} oz gold/MW-day  (the price of firm capacity, in hard money).")

print("\n[THE FIRM-SUPPLY WALLS]")
print("  Gas turbines: GE Vernova ~80 GW backlog into 2029; heavy-duty lead ~3yr, CCGT 5-7yr; ~80GW orders vs ~30GW/yr capacity.")
print("  Nuclear restarts: ~2028 (TMI). SMRs: ~2030+ (Kairos/Oklo). => new FIRM power lags AI demand by years.")
print("  Nuclear FUEL chokepoint: Russia ~44% of global enrichment; HALEU for SMRs was ~100% Russia;")
print("    domestic Centrus ~900 kg/yr (American Centrifuge, Piketon OH) - tiny vs an SMR fleet. (see power_adequacy.py)")

print("\n[SPECULATIVE SUPPLIER VEHICLES riding the narrative] (graded elsewhere):")
for t,note in SPEC_SUPPLIERS.items(): print(f"  {t:<10} {note}")

print("\n[THE PARALLEL]  TWO adversary chokepoints on ONE buildout:")
print("  Defense  -> CHINA controls rare earths (samarium/REE) -> independence ~2028 (defense_chokepoint.py)")
print("  Energy   -> RUSSIA controls uranium enrichment (HALEU) -> independence ~2028-2030 (power_adequacy.py)")
print("  The AI+defense complex is physically gated by BOTH strategic rivals simultaneously.")

json.dump({"power_deals":deals,"spec_suppliers":SPEC_SUPPLIERS,"pjm_cap_usd_mwday":pjm,
           "datacenter_share_2023_pct":4.4,"datacenter_share_2028_pct":"6.7-12"},
          open(os.path.join(DATA,"energy_web.json"),"w"),indent=2)
print("\nwrote data/energy_web.json")
