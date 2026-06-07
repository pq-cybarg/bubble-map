#!/usr/bin/env python3
"""
blockchain_web.py - the BLOCKCHAIN leg (set aside at the start, now formalized): two circular
loops + the wire into the fiscal core.

  LOOP A (policy capture):  Fairshake PAC (a16z/Coinbase/Ripple $) -> elect pro-crypto Congress
                            -> GENIUS/CLARITY favorable law -> token/exchange/stablecoin value up
                            -> more PAC money.  (a directed cycle, like the AI core)
  LOOP B (deficit rail):    GENIUS mandates Treasury backing -> stablecoin growth forces T-bill
                            buying -> funds the US deficit / lowers borrowing cost -> enables more
                            debt -> dollar liquidity -> more stablecoin demand.

Plus tokens re-priced in GOLD (which crypto is 'real' vs debasement-beneficiary), and the honest
grading link to spec-crypto-sec-epstein.json (selective enforcement, McCaleb, threat actors).
"""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GOLD={2015:1160,2018:1268,2021:1799,2024:2386,2026:4300}

print("="*82); print("BLOCKCHAIN LEG  -  two circular loops + the wire into the fiscal core"); print("="*82)

# ---- LOOP A: policy capture (directed cycle) ----
LOOP_A=[("a16z/Coinbase/Ripple","Fairshake PAC","funds ($193M war chest; $133M spent 2024)"),
        ("Fairshake PAC","pro-crypto Congress","elects/defeats candidates"),
        ("pro-crypto Congress","GENIUS/CLARITY","favorable legislation"),
        ("GENIUS/CLARITY","token+exchange value","legitimizes/derisks the asset class"),
        ("token+exchange value","a16z/Coinbase/Ripple","enriches the funders -> back to PAC")]
print("\n[LOOP A - POLICY CAPTURE] a documented directed cycle:")
for a,b,n in LOOP_A: print(f"   {a:<26} -> {b:<22} {n}")
print("   => closes into a self-reinforcing cycle (industry money -> law -> value -> money).")

# ---- LOOP B: stablecoin -> Treasury deficit rail (quantified) ----
SC={"mktcap_2020":25,"mktcap_jul2025":200,"mktcap_now":315,"tbills_bought":109,
    "usdt":189,"usdc":78,"bessent_treasury_demand":2000,"bessent_mktcap_2030":3000,"bessent_savings_yr":114}
print("\n[LOOP B - STABLECOIN DEFICIT RAIL] (Treasury-Secretary-confirmed):")
print(f"   stablecoin mkt cap: $25B (2020) -> $200B (Jul-2025) -> ~${SC['mktcap_now']}B now (USDT ${SC['usdt']}B, USDC ${SC['usdc']}B)")
print(f"   T-bills already bought to meet GENIUS 1:1 mandate: ~${SC['tbills_bought']}B")
print(f"   Bessent: up to ${SC['bessent_treasury_demand']}B Treasury demand; ${SC['bessent_mktcap_2030']}B mkt by 2030; ~${SC['bessent_savings_yr']}B/yr saved")
print("   => GENIUS makes stablecoin GROWTH structurally force TREASURY buying -> a NEW deficit-financing")
print("      rail for the $38T debt the Fed cannot manage with one rate (fed_policy_trap.py).")
print("      Blockchain is thus WIRED INTO the fiscal/debasement core, not separate from it.")

# ---- tokens in gold (which crypto is 'real') ----
BTC={2015:0.3,2018:7,2021:47,2024:95,2026:120}   # $k
ETH={2018:0.7,2021:3.7,2024:3.3,2026:4.0}         # $k
print("\n[TOKENS IN GOLD]  ratio = price / gold (oz of gold per coin):")
print("   BTC:", {y:round(BTC[y]*1000/GOLD[y],1) for y in BTC}, "oz gold  (up vs gold = real adoption, like NVDA)")
print("   ETH:", {y:round(ETH[y]*1000/GOLD[y],2) for y in ETH}, "oz gold  (peaked ~2021 in gold; flat-down since)")
print("   => BTC is one of the FEW assets up in gold (real monetization story); most alts are debasement-beta.")

# ---- honest grading link ----
print("\n[HONEST GRADING] (see spec-crypto-sec-epstein.json):")
print("   - SEC selective enforcement (Hinman ETH-pass vs XRP suit): facts STRONG, corrupt-intent CONTESTED.")
print("   - McCaleb Mt.Gox->Ripple->Stellar: common-founder lineage, NOT coordinated fraud.")
print("   - DPRK/Lazarus -> Tornado Cash -> Ethereum: the illicit/national-security edge of the same rails.")
print("   - Verdict: blockchain is BOTH a captured-policy asset class AND a real deficit-financing rail;")
print("     its systemic role is now MONETARY (stablecoins->Treasuries), tying it back to Layers 1-3.")

out={"loop_a_policy_capture":[{"from":a,"to":b,"note":n} for a,b,n in LOOP_A],
     "loop_b_stablecoin_treasury":SC,
     "btc_gold_oz":{str(y):round(BTC[y]*1000/GOLD[y],1) for y in BTC},
     "eth_gold_oz":{str(y):round(ETH[y]*1000/GOLD[y],2) for y in ETH}}
json.dump(out,open(os.path.join(ROOT,"data","blockchain_web.json"),"w"),indent=2)
print("\nwrote data/blockchain_web.json")
