#!/usr/bin/env python3
"""
causal_model.py - MECHANISM, as far as honesty allows. Proof of cause is outside what an exchange
ratio can give, but each asset's rise can be DECOMPOSED into observable drivers via price identities,
and that discriminates between the competing "why" stories far better than one M2 number:

  Equities:  price = earnings x (P/E multiple)        [identity]
  Housing:   price = rent x (price-to-rent multiple)  [identity]
  Gold:      no cashflow -> rise is monetary / store-of-value demand (a residual, by elimination)

The honest payoff: there is NO single cause. Gold is monetary; equities are real earnings (whose
growth partly reflects the labor->capital income-share shift - the one mechanism that directly ties
wage stagnation to asset gains); housing is mostly rents plus a rate/supply multiple. Any monocausal
story ("it's all money printing") fails an asset it cannot explain (equity multiples did NOT expand).

Reads data/sources_manifest.json (live FRED) + documented S&P earnings. Writes data/causal_model.json.
Tier: identities are exact; driver attributions are accounting decompositions + association, NOT proof
of cause; confounders are listed. Labor-share series (Penn/FRED) ends 2019 - stated.
"""
import json, os, math
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")
try: MAN=json.load(open(os.path.join(DATA,"sources_manifest.json")))["series"]
except Exception: MAN={}
def mv(sid, y, fb=None):
    return MAN.get(sid,{}).get("values",{}).get(str(y), fb)

def logshare(total_mult, parts):
    """attribute a total multiplicative growth to its factors by share of log-growth."""
    lt=math.log(total_mult)
    return [{"factor":n,"mult":round(m,3),"log_share_pct":round(math.log(m)/lt*100,1)} for n,m in parts]

# --- Equities: price = EPS x P/E -------------------------------------------------------------
sp0,sp24=mv("SP500_ANNUAL",2000,1427), mv("SP500_ANNUAL",2024,5427)
EPS0,EPS24=50.0,210.0          # S&P 500 as-reported EPS (S&P Dow Jones Indices; documented snapshot)
eps_mult=EPS24/EPS0; price_mult=sp24/sp0; pe_mult=price_mult/eps_mult
cpi0,cpi24=mv("CPIAUCSL",2000,172.2), mv("CPIAUCSL",2024,313.7); cpir=cpi24/cpi0
equities={"price_mult":round(price_mult,3),"eps_mult":round(eps_mult,3),"pe_mult":round(pe_mult,3),
          "real_eps_mult":round(eps_mult/cpir,3),
          "decomp":logshare(price_mult,[("earnings (EPS)",eps_mult),("multiple (P/E)",pe_mult)]),
          "reading":"equities rose on EARNINGS, not multiple expansion - P/E actually contracted; "
                    "real profits ~x2.3. This is real value capture, not pure monetary inflation."}

# --- Housing: price = rent x price/rent ------------------------------------------------------
cs0,cs24=mv("CSUSHPINSA",2000,104.78), mv("CSUSHPINSA",2024,321.35)
rent0,rent24=mv("CUUR0000SEHA",2000,183.9), mv("CUUR0000SEHA",2024,420.1)
home_mult=cs24/cs0; rent_mult=rent24/rent0; p2r_mult=home_mult/rent_mult
housing={"price_mult":round(home_mult,3),"rent_mult":round(rent_mult,3),"p2r_mult":round(p2r_mult,3),
         "decomp":logshare(home_mult,[("rents",rent_mult),("price-to-rent multiple (rates/supply)",p2r_mult)]),
         "reading":"most of home appreciation is RENTS (a fundamental); the rest is a price-to-rent "
                   "multiple driven by the mortgage-rate cycle and chronic underbuilding - a mix, not monetary alone."}

# --- Gold: no cashflow -> monetary residual vs M2 --------------------------------------------
g0,g24=mv("GOLD_LBMA",2000,279.11), mv("GOLD_LBMA",2024,2386.20)
m20,m224=mv("M2SL",2000,4792.05), mv("M2SL",2024,21134.69)
gold_mult=g24/g0; m2_mult=m224/m20
gold={"price_mult":round(gold_mult,3),"m2_mult":round(m2_mult,3),"vs_m2":round(gold_mult/m2_mult,3),
      "reading":"gold has no earnings or rent to decompose; its x%.1f rise ran ~%.1fx M2 growth - "
                "monetary / store-of-value demand plus crisis premium, by elimination."%(gold_mult,gold_mult/m2_mult)}

# --- Labor -> capital income-share shift (the bridge from wages to equity earnings) ----------
ls0=mv("LABSHPUSA156NRUG",2000,0.6371); ls_last_y=2019; ls_last=mv("LABSHPUSA156NRUG",2019,0.5918)
labor_share={"y0":2000,"share_2000":round(ls0,4),"y_last":ls_last_y,"share_last":round(ls_last,4),
             "rel_change_pct":round((ls_last-ls0)/ls0*100,1),"pt_change":round((ls_last-ls0)*100,1),
             "reading":"labor's share of GDP fell ~%.1f%% (%.1f points, 2000->%d; Penn/FRED series ends %d); "
                       "the mirror is a rising capital/profit share - the accounting bridge from wage "
                       "stagnation to the equity EARNINGS that lifted the market."%(
                       abs((ls_last-ls0)/ls0*100),abs((ls_last-ls0)*100),ls_last_y,ls_last_y)}

# --- Hypothesis-discrimination matrix: cause x asset (which story explains which) -------------
# strength: strong / partial / none / n_a
MATRIX={
 "columns":["Gold","Equities (S&P)","Housing"],
 "rows":[
  ["Monetary expansion (M2)",        "strong","partial","partial"],
  ["Real earnings / fundamentals",   "n_a","strong","partial"],   # equities=EPS; housing=rents
  ["Rate suppression (low discount)","partial","partial","strong"],
  ["Labor->capital share shift",     "none","strong","none"],
  ["Supply constraint",              "none","none","strong"],      # underbuilding
 ],
 "reading":"No row explains all three; no column is explained by one row. 'It's all money printing' "
           "fails equities (multiples contracted); 'it's all fundamentals' fails gold (it has none). "
           "The only cause that links WAGES to an asset gain is the labor->capital share shift, via "
           "equity earnings - documented accounting, not intent."}

out={"equities":equities,"housing":housing,"gold":gold,"labor_share":labor_share,"matrix":MATRIX,
     "tier":"Price identities are exact; driver attributions are accounting decompositions + association, "
            "not proof of cause. Confounders (globalisation, demographics, buybacks, financialisation, "
            "tax policy, foreign demand) are uncontrolled.",
     "sources":"FRED (S&P CoreLogic Case-Shiller, CPI rent, M2, labor share); S&P Dow Jones Indices "
               "(as-reported EPS, documented); LBMA gold (documented)."}

print("="*88); print("MECHANISM - decompose each asset's rise into its actual driver"); print("="*88)
print(f"EQUITIES  price x{price_mult:.2f} = EPS x{eps_mult:.2f} * P/E x{pe_mult:.2f}   (real EPS x{eps_mult/cpir:.2f})")
print(f"HOUSING   price x{home_mult:.2f} = rent x{rent_mult:.2f} * price/rent x{p2r_mult:.2f}")
print(f"GOLD      price x{gold_mult:.2f} = monetary residual ({gold_mult/m2_mult:.2f}x M2); no cashflow to decompose")
print(f"LABOR SHARE  {ls0:.3f} (2000) -> {ls_last:.3f} ({ls_last_y})  = {(ls_last-ls0)/ls0*100:+.1f}%  (bridge to equity earnings)")
print("\nHYPOTHESIS x ASSET:")
print(f"  {'cause':<34}{'Gold':>8}{'Equities':>10}{'Housing':>9}")
for r in MATRIX["rows"]:
    print(f"  {r[0]:<34}{r[1]:>8}{r[2]:>10}{r[3]:>9}")
print("  =>", MATRIX["reading"][:130], "...")
json.dump(out, open(os.path.join(DATA,"causal_model.json"),"w"), indent=2)
print("\nwrote data/causal_model.json")
