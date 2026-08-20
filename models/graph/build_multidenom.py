#!/usr/bin/env python3
"""
build_multidenom.py - render docs/multidenom.html: the multi-denomination (USD / gold-oz /
silver-oz) value analysis. A 3D plot (year x money-plane x indexed value, one trace per asset),
the gold/silver ratio line, and breakdown tables. Reads data/multi_denomination.json (written
by multi_denomination.py); data is inlined so the page is self-contained on GitHub Pages.

Palette validated with the dataviz six-checks (light surface): categorical, all PASS.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data"); DOCS=os.path.join(ROOT,"docs")
d=json.load(open(os.path.join(DATA,"multi_denomination.json")))
grid=d["denomination_grid"]; gsr=d["gold_silver_ratio"]

# validated categorical palette (fixed order = asset order in the grid)
PAL=["#2b6cb0","#dd6b20","#38a169","#c53030","#805ad5","#0d9488"]
colors={row["asset"]:PAL[i%len(PAL)] for i,row in enumerate(grid)}
DATA_JSON=json.dumps({"grid":grid,"gsr":gsr,"colors":colors})

# breakdown table (endpoint index base=100)
def split_rows():
    out=[]
    for row in grid:
        z=row["years"][-1]; b=row["base_year"]
        out.append(f"<tr><td>{row['asset']}</td><td>{b}</td><td>{row['usd'][-1]:.0f}</td>"
                   f"<td>{(row['gold'][-1] or 0):.0f}</td><td>{(row['silver'][-1] or 0):.0f}</td></tr>")
    return "".join(out)
def gsr_rows():
    return "".join(f"<tr><td>{r['year']}</td><td>${r['gold']:,}</td><td>${r['silver']:.2f}</td><td>{r['ratio']:.1f}</td></tr>" for r in gsr)

# --- WAGES (labor-side companion; written by wages.py) --------------------------------------
w=json.load(open(os.path.join(DATA,"wages_denominated.json")))
WAGE_JSON=json.dumps(w)
WY=w["years"]
_mw=w["minimum_wage"]; _all=next(r for r in w["occupations"] if r["name"].startswith("All occ"))
_food=next(r for r in w["occupations"] if r["name"].startswith("Food"))
def wage_rows():
    rows=[_mw]+w["occupations"]
    out=[]
    for r in rows:
        z=-1
        out.append(f"<tr><td>{r['name']}</td><td>${r['usd'][0]:,.0f}</td><td>${r['usd'][z]:,.0f}</td>"
                   f"<td>{r['usd_idx'][z]:.0f}</td><td>{r['gold'][0]:.0f}</td><td>{r['gold'][z]:.0f}</td>"
                   f"<td>{r['gold_idx'][z]:.0f}</td><td>{r['silver_idx'][z]:.0f}</td></tr>")
    return "".join(out)
def region_rows():
    return "".join(f"<tr><td>{r['name']}</td><td>${r['usd'][0]:,.0f}</td><td>${r['usd'][-1]:,.0f}</td>"
                   f"<td>{r['usd_idx'][-1]:.0f}</td><td>{r['gold'][0]:.0f}</td><td>{r['gold'][-1]:.0f}</td>"
                   f"<td>{r['gold_idx'][-1]:.0f}</td></tr>" for r in w["regions"])
def gig_rows():
    return "".join(f"<tr><td>{k}</td><td>${v['usd']:,.0f}</td><td>{v['gold']:.1f}</td><td>{v['silver']:.0f}</td></tr>"
                   for k,v in w["gig"].items())
def comp_rows():
    c=w["composition"]; ys=c["years"]
    head="".join(f"<th>{y}</th>" for y in ys)
    body="".join("<tr><td>"+g+"</td>"+"".join(f"<td>{v:.1f}%</td>" for v in vals)+"</tr>"
                 for g,vals in c["groups"].items())
    return head, body
_comp_head,_comp_body=comp_rows()

# --- PROOF (what actually survives every objection; written by wage_proof.py) ---------------
pf=json.load(open(os.path.join(DATA,"wage_proof.json")))
PROOF_JSON=json.dumps(pf)
_ptol=pf["data_tol"]*100
def proof_rows(labor):
    out=[]
    for r in pf["labor"][labor]:
        badge=('<b style="color:#0ca30c">CERTIFIED</b>' if r["certified"]
               else '<span style="color:#8a8378">fell — not certified</span>')
        out.append(f"<tr><td>{r['numeraire']}</td><td>{r['labor_per_asset_2000']:.3g}</td>"
                   f"<td>{r['labor_per_asset_2024']:.3g}</td><td>{r['pct_of_2000']:.0f}%</td>"
                   f"<td>{r['breakdown_pct']:.0f}%</td><td>{badge}</td></tr>")
    return "".join(out)
_realwage=pf["real_wage_change_2000_2024"]*100
_mck=pf["machine_check"]
def endpoint_table():
    m=pf["endpoint_matrix"]; assets=list(m); starts=[r["start"] for r in m[assets[0]]]
    head="".join(f"<th>from {s}</th>" for s in starts)
    body=""
    for a in assets:
        cells=""
        for r in m[a]:
            sty="font-weight:700;color:#0ca30c" if r["certified"] else ("color:#8a8378" if r["direction"]=="fell" else "color:#c53030")
            mark=" ★" if r["certified"] else ""
            cells+=f'<td style="{sty}">{r["pct_of_start"]:.0f}%{mark}</td>'
        body+=f"<tr><td>{a}</td>{cells}</tr>"
    return head, body
_ep_head,_ep_body=endpoint_table()
def _badge(ok, yes="CERTIFIED", no="within noise", nocol="#8a8378"):
    return (f'<b style="color:#0ca30c">{yes}</b>' if ok else f'<span style="color:{nocol}">{no}</span>')
def primary_rows():
    return "".join(f"<tr><td>{r['numeraire']}</td><td>×{r['asset_mult']:.2f}</td><td>{r['pct_of_2000']:.0f}%</td>"
                   f"<td>±{r['tol']*100:.0f}%</td><td>{r['R_worst']:.2f}</td><td>{_badge(r['certified'])}</td></tr>"
                   for r in pf["primary"])
def alnri_rows():
    return "".join(f"<tr><td>{h['lens']}</td><td>×{h['home_mult']:.2f}</td>"
                   f"<td>{h['pct_of_2000']:.0f}%</td><td>{h['breakdown_pct']:.0f}%</td>"
                   f"<td>{_badge(h['certified'])}</td><td class=muted>{h['note']}</td></tr>" for h in pf["homes_alnri"])
def money_rows():
    return "".join(f"<tr><td>{r['item']}</td><td>×{r['mult']:.2f}</td><td>{r['vs_m2']:.2f}×</td></tr>"
                   for r in pf["money"]["rows"])
_hp=pf["home_payments"]; _m2=pf["money"]["m2_mult"]

# --- WEALTH CONCENTRATION (bucket-bias critique; written by wealth_concentration.py) ---------
wc=json.load(open(os.path.join(DATA,"wealth_concentration.json")))
WC_JSON=json.dumps(wc)
_gI=wc["gini"]["income_census_2023"]; _gW=wc["gini"]["wealth_scf_2022"]
_t01=wc["top_0_1_share"]; _b50=next(g["share"] for g in wc["wealth_shares"] if g["group"]=="Bottom 50%")
_td=wc["gini_tail_demo"]
def distortion_rows():
    col={"distortion":"#c53030","statistical fact":"#8a8378","confounder":"#8a8378"}
    out=[]
    for d in wc["distortions"]:
        c=next((v for k,v in col.items() if d["tag"].startswith(k)),"#8a8378")
        out.append(f'<tr><td><b>{d["name"]}</b></td><td>{d["mechanism"]}</td>'
                   f'<td style="color:{c};white-space:nowrap">{d["tag"]}</td></tr>')
    return "".join(out)

# --- WEALTH DYNAMICS (trajectory + index family; written by wealth_dynamics.py) --------------
wd=json.load(open(os.path.join(DATA,"wealth_dynamics.json")))
WD_JSON=json.dumps(wd)
# conservation identity (from wage_proof.json)
_cons=pf["conservation"]
def conservation_rows():
    return "".join(f"<tr><td>{r['asset']}</td><td>{r['claim_ratio']:.2f}</td>"
                   f"<td>{r['transfer_to_holders']*100:.0f}%</td></tr>" for r in _cons["rows"])
def family_rows():
    return "".join(f"<tr><td>{r['index']}</td><td>{r['base']:.3f}</td><td>{r['shocked']:.3f}</td>"
                   f"<td>+{r['change_pct']:.0f}%</td></tr>" for r in wd["index_family"])

# --- CAUSAL MECHANISM (written by causal_model.py) -------------------------------------------
cm=json.load(open(os.path.join(DATA,"causal_model.json")))
CM_JSON=json.dumps(cm)
_eq=cm["equities"]; _ho=cm["housing"]; _go=cm["gold"]; _ls=cm["labor_share"]
def matrix_rows():
    col={"strong":"#0ca30c","partial":"#eda100","none":"#c53030","n_a":"#8a8378"}
    lab={"strong":"strong","partial":"partial","none":"none","n_a":"n/a"}
    out=[]
    for r in cm["matrix"]["rows"]:
        cells="".join(f'<td style="color:{col[c]};font-weight:600">{lab[c]}</td>' for c in r[1:])
        out.append(f"<tr><td>{r[0]}</td>{cells}</tr>")
    return "".join(out)
# --- PROVENANCE (from wage_proof.json) -------------------------------------------------------
_prov=pf.get("provenance",{})
def prov_rows():
    out=[]
    for s in _prov.get("series",[]):
        live=('<b style="color:#0ca30c">live</b>' if s["fetched"] else '<span style="color:#8a8378">documented</span>')
        aso=s.get("as_of") or "-"
        out.append(f'<tr><td><code>{s["id"]}</code></td><td>{s["desc"]}</td><td>{live}</td>'
                   f'<td>{aso}</td><td><a href="{s["url"]}" rel="noopener">source ↗</a></td></tr>')
    return "".join(out)
_recon_max=_prov.get("max_abs_delta_pct"); _nlive=_prov.get("n_live",0); _ntot=_prov.get("n_total",0)
_dataver=max((s.get("as_of") or "" for s in _prov.get("series",[])), default="") or "snapshot"

import nav as _nav
NAV=_nav.navbar("Metals")
DISC=('<div style="background:#faf8f2;color:#8a8378;font:11px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;'
      'text-align:center;padding:6px 16px;border-bottom:1px solid #e4ddcc">Independent research &amp; opinion. '
      'Annual-average metal prices (LBMA/USGS); 2025–26 ~approx and provisional. Denomination is an overlay lens, not proof. '
      '<a href="methodology.html" style="color:#6b665d">Methodology</a>.</div>')

HTML=f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Value in three monies — USD / gold / silver</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
 body{{background:#faf8f2;color:#1c1b19;margin:0;font:17px/1.68 Georgia,'Iowan Old Style','Palatino Linotype',serif}}
 main{{max-width:1000px;margin:0 auto;padding:0 22px 70px}}
 h1{{font-weight:600;font-size:32px;margin:26px 0 6px}}
 h2{{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:7px;margin-top:40px;font-weight:600;font-size:23px}}
 p{{margin:13px 0}} .muted{{color:#6b665d;font-size:14.5px}}
 table{{border-collapse:separate;border-spacing:0;width:100%;margin:16px 0;font:14.5px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;border:1px solid #e4ddcc;border-radius:8px;overflow:hidden}}
 th,td{{border-bottom:1px solid #e4ddcc;padding:9px 13px;text-align:right}} th:first-child,td:first-child{{text-align:left}}
 td+td,th+th{{border-left:1px solid #e4ddcc}} tr:last-child td{{border-bottom:none}} thead th{{background:#f3eedf}} tbody tr:nth-child(even){{background:#fbf9f3}}
 .plot{{background:#fcfcfb;border:1px solid #e4ddcc;border-radius:10px;margin:14px 0;padding:6px}}
 .k{{display:inline-block;background:#fffdf8;border:1px solid #e4ddcc;border-radius:6px;padding:9px 13px;margin:6px 8px 6px 0;font:13.5px/1.4 -apple-system,Segoe UI,Roboto,sans-serif}}
 .k b{{font-size:19px;color:#7b2d26}}
 a{{color:#1f4e79}}
 main.wide{{max-width:1580px}}
 .split{{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(0,0.98fr);gap:40px;align-items:start}}
 .col{{min-width:0}}
 .colhead{{font:12px/1.3 -apple-system,Segoe UI,Roboto,sans-serif;letter-spacing:.13em;text-transform:uppercase;color:#9a8f7a;margin:24px 0 0}}
 .col-story{{background:#fffdf8;border:1px solid #e9e2d2;border-radius:12px;padding:4px 28px 32px}}
 .col-story h1{{font-size:29px}}
 .col-story h2{{color:#1f4e79;font-size:20px;border:0;padding:0;margin-top:32px}}
 .col-story p{{font-size:16.5px;line-height:1.74}}
 .lead{{font-size:19px;line-height:1.6;color:#33312c}}
 .aud{{background:#f7f9fc;border:1px solid #cbd8ea;border-radius:9px;padding:11px 15px;margin:10px 0;font-size:15.5px;line-height:1.62}}
 .aud .who{{display:block;color:#1f4e79;font-weight:700;margin-bottom:3px}}
 .story-tag{{display:inline-block;font:11px/1 -apple-system,Segoe UI,Roboto,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#7b2d26;background:#f3eedf;border-radius:20px;padding:6px 11px;margin:6px 0 2px}}
 @media(max-width:1000px){{ .split{{grid-template-columns:1fr;gap:16px}} .col-story{{padding:4px 18px 24px}} }}
</style></head><body>{NAV}{DISC}
<main class=wide>
<div class=split>
<section class="col col-data">
<div class=colhead>The evidence — data, proof &amp; its limits</div>
<h1>Value in three monies</h1>
<p class=muted>Every asset indexed to its base year (=100), then held to a constant monetary unit — US&nbsp;dollars, then ounces of gold, then ounces of silver, at the price prevailing in each year. A number that climbs in dollars often sits flat or falls once the money itself stops moving.</p>

<div>
<span class=k>S&amp;P 500 since 2000<br><b>×4.8</b> in USD · <b>×0.31</b> in gold</span>
<span class=k>US median home since 2000<br><b>×2.5</b> in USD · <b>×0.16</b> in gold</span>
<span class=k>NVIDIA since 2016<br><b>×72</b> in USD · <b>×21</b> in gold</span>
<span class=k>Gold/silver ratio<br><b>{gsr[0]['ratio']:.0f} → {gsr[-1]['ratio']:.0f}</b></span>
</div>

<h2>The three money-planes (3D)</h2>
<p class=muted>Each asset draws a line across three parallel planes — USD, gold, silver. Log vertical scale (the range from a home at ~16 to NVIDIA at ~2,000 needs it). Drag to rotate; click a legend entry to toggle an asset; hover any point for the exact index.</p>
<div id=plot3d class=plot style="height:560px"></div>

<h2>Gold / silver ratio</h2>
<p class=muted>Ounces of silver to buy one ounce of gold. A high ratio = silver historically cheap versus gold; the classic hard-money gauge. Annual averages.</p>
<div id=gsr class=plot style="height:340px"></div>

<h2>Breakdown — endpoint index (base year = 100)</h2>
<table><thead><tr><th>Asset</th><th>Base</th><th>USD</th><th>Gold-oz</th><th>Silver-oz</th></tr></thead><tbody>{split_rows()}</tbody></table>
<p class=muted>Read across a row: dollars rose the most, gold least, silver between. Only NVIDIA rises in every money — genuine value capture, not debasement. The broad market, housing and commercial real estate are all <b>down two-thirds or more in gold</b> since 2000.</p>

<h2>Gold / silver ratio — annual</h2>
<table><thead><tr><th>Year</th><th>Gold $/oz</th><th>Silver $/oz</th><th>GSR</th></tr></thead><tbody>{gsr_rows()}</tbody></table>

<h1 style="margin-top:56px">Wages in three monies</h1>
<p class=muted>The same lens, turned on labor. A year's <b>pay</b> — by occupation, by region, gig versus traditional — held to US dollars, then to ounces of gold, then to ounces of silver at the price prevailing in each year. Wages roughly <b>doubled in dollars</b> since 2000. In gold they fell to a fifth. Figures are representative BLS annual means (occupations, regions) and the federal statutory minimum; approximate and directional, denomination is an overlay lens not proof.</p>

<div>
<span class=k>Federal minimum wage, a year's work<br><b>{_mw['gold'][0]:.0f} oz → {_mw['gold'][-1]:.0f} oz</b> gold ·  +{_mw['usd_idx'][-1]-100:.0f}% in USD</span>
<span class=k>All occupations (mean), a year's work<br><b>{_all['gold'][0]:.0f} oz → {_all['gold'][-1]:.0f} oz</b> gold ·  +{_all['usd_idx'][-1]-100:.0f}% in USD</span>
<span class=k>Food prep &amp; serving — rose most in $<br><b>+{_food['usd_idx'][-1]-100:.0f}%</b> USD · yet <b>{_food['gold_idx'][-1]:.0f}</b> in gold (2000=100)</span>
<span class=k>Gig driver (net) vs full-time median, 2024<br><b>{w['gig']['Gig driver — net of costs']['gold']:.0f} oz</b> vs <b>{w['gig']['Traditional full-time (median)']['gold']:.0f} oz</b> gold</span>
</div>

<h2>A year of work, in three monies (3D)</h2>
<p class=muted>Five benchmark earners — top, middle, floor, and the minimum wage — indexed to their year-2000 value (=100) across the USD / gold / silver planes. Every line rises steeply in dollars and collapses toward the floor in gold. Drag to rotate; toggle a series in the legend.</p>
<div id=wage3d class=plot style="height:540px"></div>

<h2>What a year's wage buys in gold — 2024 vs 2000</h2>
<p class=muted>Each bar = a year's pay measured in ounces of gold, as a share of its own year-2000 purchasing power (dashed line = 100 = held even with gold). Ordered worst-first. <b>Not one occupation kept pace with gold</b>; the lowest-paid lost the most ground, and the federal minimum wage lost most of all.</p>
<div id=wagegold class=plot style="height:640px"></div>

<h2>By region — dollars up, gold down, everywhere</h2>
<p class=muted>Census-region annual mean wage, indexed to 2000 (=100), in dollars (rose ~2×) beside gold-ounces (fell to ~a quarter). The regional spread barely matters once the money is held constant.</p>
<div id=wageregion class=plot style="height:360px"></div>
<table><thead><tr><th>Region</th><th>USD 2000</th><th>USD 2024</th><th>USD idx</th><th>Gold-oz 2000</th><th>Gold-oz 2024</th><th>Gold idx</th></tr></thead><tbody>{region_rows()}</tbody></table>

<h2>Gig vs traditional — a year's earnings in metal (2024)</h2>
<p class=muted>Ounces of gold bought by a year of traditional full-time work (median) versus gig driving — gross, then net of vehicle and fuel costs. Gig work is a post-2010 category, so this is a 2024 snapshot; net figures are estimates and vary widely by market and hours.</p>
<div id=waggig class=plot style="height:320px"></div>
<table><thead><tr><th>Category (2024)</th><th>USD</th><th>Gold-oz</th><th>Silver-oz</th></tr></thead><tbody>{gig_rows()}</tbody></table>

<h2>Who earns — composition of work over time</h2>
<p class=muted>Share of US employment by super-group, 2000→2024. The growing slices are the ones that also held the most gold value (management/professional, computer &amp; math, healthcare); the shrinking slices — sales &amp; office, blue-collar — are where the gold-denominated wage fell hardest. Composition and repricing move together: the workforce is tilting toward the few roles that outran debasement.</p>
<div id=wagecomp class=plot style="height:420px"></div>
<table><thead><tr><th>Super-group</th>{_comp_head}</tr></thead><tbody>{_comp_body}</tbody></table>

<h2>Wages — endpoint index &amp; ounces (2000=100)</h2>
<table><thead><tr><th>Occupation</th><th>USD 2000</th><th>USD 2024</th><th>USD idx</th><th>Gold-oz 2000</th><th>Gold-oz 2024</th><th>Gold idx</th><th>Silver idx</th></tr></thead><tbody>{wage_rows()}</tbody></table>
<p class=muted>Read the two gold columns: a year's minimum-wage work bought {_mw['gold'][0]:.0f} ounces of gold in 2000 and {_mw['gold'][-1]:.0f} in 2024; the average job, {_all['gold'][0]:.0f} then {_all['gold'][-1]:.0f}. The USD-index column climbs past 190 for almost every row — the same wage, told in two monies, tells opposite stories.</p>

<h1 style="margin-top:56px">What can actually be proven</h1>
<p class=muted>Everything above is an <i>overlay</i>. "Wages fell in gold" is nearly a tautology — it only re-denominates, and it privileges gold, so a critic answers "gold bubbled." This section keeps only what survives <i>every</i> such objection, and certifies exactly how un-handwavable that core is. Three tiers of certainty; the wage figures are representative and rounded, so only <b>directions</b>, never magnitudes, are claimed as proven.</p>

<div class=k style="display:block;background:#f7f9fc;border-color:#cbd8ea">
<b style="color:#256abf">Theorem — relative price is numeraire-invariant.</b> For any two goods A, B priced in a common money <i>m</i>, the exchange ratio p<sub>A</sub>/p<sub>B</sub> = (k·p<sub>A</sub>)/(k·p<sub>B</sub>) for any positive conversion <i>k</i> — the money cancels. So "a year of labor exchanges for fewer ounces of gold, fewer shares of the S&amp;P 500, less silver than in 2000" is a fact about <b>labor's relative price</b>. It needs no trust in the dollar, or gold, or any single asset being "sound"; to deny it you must deny the exchange ratios themselves. <span class=muted>Executable check: labor→gold computed with dollars-as-money equals the same figure with silver-as-money to machine precision ({pf['invariance_check']['via_usd']:.4f} oz), confirming the cancellation.</span>
</div>

<h2>The robustness certificate</h2>
<p class=muted>Because the levels are approximate, a bare ratio is not enough. Model each of the four inputs (labor 2000, labor 2024, asset 2000, asset 2024) as known only to within a uniform relative error, and push all four <b>at once</b> in the direction most favorable to "no decline." The <b>breakdown error e*</b> is the answer to: <i>how wrong would every number have to be, simultaneously, to make the decline disappear?</i> A claim is <b>CERTIFIED</b> only if e* clears the assumed data tolerance of {_ptol:.0f}%.</p>
<div id=proofbar class=plot style="height:360px"></div>
<p class=muted>Bars past the dashed {_ptol:.0f}% line are un-handwavable even granting my numbers could each be off by that much: against <b>gold, silver and equities</b> a year of average labor buys 22-51% of its 2000 exchange value, and overturning that needs 17-36% error in every input at once. Against <b>housing and commercial real estate</b> labor also fell — but by too little (e* of 3-7%) to certify at this data quality, so it is <i>stated, not proven</i>.</p>

<table><thead><tr><th>Numeraire</th><th>labor buys, 2000</th><th>labor buys, 2024</th><th>% of 2000</th><th>breakdown e*</th><th>verdict</th></tr></thead><tbody>{proof_rows("All occupations (mean wage)")}</tbody></table>
<p class=muted>Same test on the federal minimum wage is stronger still (it fell furthest): certified against gold, silver and the S&amp;P; the two hard-money columns need &gt;33% uniform error to overturn.</p>

<h2>Deeper — <i>where</i> did the decline happen? (real wages vs asset inflation)</h2>
<p class=muted>The invariance theorem says the ratio fell; it does not say where. Any labor:asset ratio factors <b>exactly</b> into two observable pieces — labor priced in the <i>consumer basket</i> (the real wage) times the consumer basket priced in the <i>asset</i> (asset inflation in wage-hours):</p>
<div class=k style="display:block;background:#f7fbf7;border-color:#bfe0bf">
labor:asset&nbsp;=&nbsp;<b style="color:#0ca30c">(labor:CPI)</b>&nbsp;×&nbsp;<b style="color:#c53030">(CPI:asset)</b>. &nbsp;By the CPI lens the real consumption wage <b style="color:#0ca30c">rose {_realwage:+.1f}%</b> from 2000 to 2024 — workers did <b>not</b> lose grocery-store power. The entire labor:asset collapse is the second term: <b style="color:#c53030">asset prices inflated 2×-5× in wage-hours</b>. Labor's claim on the <i>consumption</i> economy held; its claim on the <i>store-of-value</i> economy collapsed.
</div>
<div id=decompbar class=plot style="height:340px"></div>
<p class=muted><b>This split is model-dependent</b> — it trusts the CPI, which is contested (hedonic and substitution adjustments; alternative indices show higher inflation). If true inflation were understated, more of the fall would be lost real wages and less would be asset inflation. So the decomposition sits <i>below</i> the theorem in certainty: illuminating, but resting on a disputed deflator. The <b>total</b> labor:asset decline uses no CPI at all and stays certified.</p>

<h2>Deeper — is it just a cherry-picked endpoint?</h2>
<p class=muted>Recompute labor's relative price for <i>every</i> start year → 2024, not only 2000. Cells show the 2024 value as a share of that start year (★ = certified, e* &gt; {_ptol:.0f}%).</p>
<table><thead><tr><th>Numeraire</th>{_ep_head}</tr></thead><tbody>{_ep_body}</tbody></table>
<p class=muted>Honest reading: the decline is strongest and certified from a <b>2000 or 2007</b> base (and, for equities, 2013). Measured from the <b>recent decade</b> it is milder and <i>not</i> certified — gold and silver were already elevated by 2013, so labor roughly held or even gained against them since. This is therefore a <b>long-horizon</b> (quarter-century) claim, and it is stated as one — it is not a claim that labor collapsed against hard money over the last ten years.</p>

<h2>Deeper — the theorem is machine-checked</h2>
<p class=muted>The two algebraic identities are not asserted in prose; the build recomputes each one two independent ways in <b>exact rational arithmetic</b> (Python <code>fractions</code>, zero floating-point error) and checks they are identical:</p>
<div class=k style="display:block;background:#f7f9fc;border-color:#cbd8ea;font:13.5px/1.7 -apple-system,Segoe UI,Roboto,sans-serif">
<b>{'✓' if _mck['invariance_exact'] else '✗'}</b> numeraire-invariance &nbsp;(k·p<sub>A</sub>)/(k·p<sub>B</sub>) = p<sub>A</sub>/p<sub>B</sub> — exact<br>
<b>{'✓' if _mck['decomposition_exact'] else '✗'}</b> decomposition &nbsp;(w<sub>24</sub>/g<sub>24</sub>)/(w<sub>00</sub>/g<sub>00</sub>) = (labor:CPI)·(CPI:gold) — exact<br>
<b>{'✓' if _mck['breakdown_root_ok'] else '✗'}</b> breakdown root &nbsp;R₀·((1+e*)/(1−e*))² = 1 — residual {_mck['breakdown_root_residual']:.0e}<br>
<b style="color:#0ca30c">ALL CHECKS PASS = {str(_mck['all_pass']).upper()}</b> &nbsp;<span class=muted>(re-verified on every site build)</span>
</div>

<h2>Deeper — authoritative series close the gap</h2>
<p class=muted>The 15% tolerance above was a stand-in for rough figures. Swap in named primary series — BLS median usual weekly earnings, LBMA gold &amp; silver, S&amp;P annual close, S&amp;P CoreLogic Case-Shiller (constant-quality) and Census median home — each with its own <i>measurement</i> tolerance (how precisely the annual number is known), and run the certificate as exact interval arithmetic per input. R<sub>worst</sub> = R₀·(1+t<sub>w</sub>)/(1−t<sub>w</sub>)·(1+t<sub>a</sub>)/(1−t<sub>a</sub>); certified iff R<sub>worst</sub>&lt;1.</p>
<table><thead><tr><th>Numeraire (primary source)</th><th>asset ×</th><th>labor buys</th><th>tol</th><th>R<sub>worst</sub></th><th>verdict</th></tr></thead><tbody>{primary_rows()}</tbody></table>
<p class=muted>With authoritative-precision data the tolerances shrink from 15% to 1-3%, and the earlier hold-outs cross the line: <b>homes now certify too</b> — even the raw median, where a year of labor buys 80% of the house it did in 2000 and the decline survives the joint measurement error. The certified basket is no longer just hard money and equities; it is <b>every</b> independent store of value measured here.</p>

<h2>Homes, honestly measured</h2>
<p class=muted>"Median home price" hides several things, so reprice a home in wage-hours under each honest lens — constant-quality (repeat-sales), raw median, price-per-square-foot, and the monthly mortgage carry:</p>
<div id=alnribar class=plot style="height:340px"></div>
<table><thead><tr><th>Home lens</th><th>home ×</th><th>labor buys</th><th>e*</th><th>verdict</th><th>note</th></tr></thead><tbody>{alnri_rows()}</tbody></table>
<div class=k style="display:block;background:#fbf7f7;border-color:#e2cccc">
The house <b>price</b> in wage-hours fell on every lens (constant-quality worst: a year of labor buys 63% of the home it did). But the monthly <b>mortgage payment</b> in wage-hours barely moved — <b>${_hp['pay_2000_mo']:,}/mo → ${_hp['pay_2024_mo']:,}/mo</b>, ×{_hp['carry_mult']:.2f} against wages up ×2.02 — because mortgage rates in 2000 were ~8% too. <b>Housing's squeeze is a down-payment / wealth-accumulation problem far more than a monthly-cashflow one</b> — a distinction the single "median price" number erases, and the reason "just rent the same payment" and "priced out of ownership" are both true at once.
</div>
<h3>The rent signal the headline lags — ALNRI</h3>
<p class=muted>Renters feel the same measurement gap. The official CPI rent line above (BLS <code>CUUR0000SEHA</code>) is a <b>~1-year-stale lagging print</b>: new-lease market indices — the Apartment List National Rent Index (ALNRI) and the BLS New Tenant Rent Index (NTRI/R-CPI-NTR) — <b>led it by ~16 months</b> (Dec 2021: ALNRI +18% YoY while official CPI rent showed ~3%). The lag cuts both ways and was invoked whichever way fit the moment — leading data in 2022 to argue disinflation, the still-high lagged print in 2024 to justify higher-for-longer — the cleanest BLS-confirmed case of "doubt the headline." <a href="r-macro-rent-cpi-divergence.html">Full analysis</a>.</p>

<h2>Deeper — did money do it? (the causal question, honestly)</h2>
<p class=muted>Proof of <i>cause</i> is outside what an exchange ratio can give, but the leading candidate — monetary expansion — can be probed as an <b>association</b>. Compare each multiple to M2 money-supply growth (Fed H.6, ×{_m2:.2f} over 2000→2024):</p>
<div id=moneybar class=plot style="height:340px"></div>
<table><thead><tr><th>Item</th><th>× 2000→2024</th><th>vs M2</th></tr></thead><tbody>{money_rows()}</tbody></table>
<p class=muted>The result cuts <i>both</i> simplistic stories. M2 grew ×{_m2:.2f}; consumer prices (×1.82) and wages (×2.02) rose under half as fast, while assets absorbed the gap and gold/silver <i>exceeded</i> it. That is exactly the footprint of monetary expansion showing up in assets rather than the shopping cart — <b>strong association, and the most plausible mechanism.</b> But it is <b>not proof</b>: no single money aggregate explains the cross-asset dispersion (gold ran ~2× M2, homes ~0.7×), and globalisation's goods-disinflation, interest rates, financialisation, EM central-bank gold buying and real-earnings growth are all uncontrolled confounders. "They printed money" is supported as a <i>partial</i> driver and refuted as a <i>complete</i> one.</p>

<h2>Deeper — the mechanism: decompose each asset's rise</h2>
<p class=muted>Proof of cause is beyond an exchange ratio, but each asset's rise splits — by <b>price identity</b> — into observable drivers, and that discriminates between the "why" stories far better than one M2 number. Equities: price = earnings × P/E. Housing: price = rent × price-to-rent. Gold: no cashflow, so its rise is monetary by elimination.</p>
<div>
<span class=k>Equities ×{_eq['price_mult']:.1f}<br>= earnings <b>×{_eq['eps_mult']:.1f}</b> · P/E <b>×{_eq['pe_mult']:.2f}</b> (contracted)</span>
<span class=k>Housing ×{_ho['price_mult']:.1f}<br>= rent <b>×{_ho['rent_mult']:.1f}</b> · price/rent <b>×{_ho['p2r_mult']:.2f}</b></span>
<span class=k>Gold ×{_go['price_mult']:.1f}<br>no earnings — <b>{_go['vs_m2']:.1f}×</b> M2, monetary residual</span>
<span class=k>Labor share of GDP<br><b>{_ls['share_2000']:.3f} → {_ls['share_last']:.3f}</b> ({_ls['rel_change_pct']:.1f}%, to {_ls['y_last']})</span>
</div>
<div id=mechbar class=plot style="height:320px"></div>
<p class=muted><b>Equities rose on earnings, not monetary multiple</b> — the P/E actually <i>contracted</i>; real profits roughly doubled (×{_eq['real_eps_mult']:.1f}). <b>Housing is mostly rents</b> plus a rate/supply multiple. <b>Gold alone is purely monetary.</b> So the mono-causal stories both fail: "all money printing" cannot explain equities (multiples shrank), and "all fundamentals" cannot explain gold (it has none).</p>

<h3>Which cause explains which asset</h3>
<table><thead><tr><th>Candidate cause</th><th>Gold</th><th>Equities</th><th>Housing</th></tr></thead><tbody>{matrix_rows()}</tbody></table>
<p class=muted>{cm['matrix']['reading']} The one cause that links <b>wages</b> to an asset gain is the <b>labor→capital income-share shift</b>: labor's share of GDP fell ~{abs(_ls['rel_change_pct']):.0f}% ({_ls['pt_change']:.1f} points to {_ls['y_last']}), and the mirror is a rising profit share — the accounting bridge to the equity earnings that lifted the market. That is documented national-accounts arithmetic, not intent. <span class=muted>Tier: the price identities are exact; the driver attributions are accounting decompositions plus association, not proof of cause; confounders (buybacks, globalisation, demographics, tax, foreign demand) are uncontrolled.</span></p>

<h2>Deeper — what R₀ actually is: a conservation identity</h2>
<p class=muted>One more level down, the ratio has a meaning that turns "the wage-hours went to owners" from rhetoric into an identity. The stock of an asset — shares of equity, ounces of gold above ground, housing units — is roughly fixed in the short run, and ownership shares of it sum to exactly 1. A price change creates <b>no new units</b>; it only revalues existing claims. One year of labor's real savings claims a fraction of that stock; at the higher price it claims R₀ of what it used to, and the complementary <b>(1−R₀)</b> is not destroyed — it stays with, i.e. transfers to, the existing holders.</p>
<table><thead><tr><th>Asset (fixed stock)</th><th>labor's unit-claim R₀</th><th>transferred to holders (1−R₀)</th></tr></thead><tbody>{conservation_rows()}</tbody></table>
<p class=muted>So R₀ is not merely "labor bought less gold" — it is the shrunken share of a fixed pie that a year of work can pull from current owners, and the rest accrues to them. The <b>transfer is definitional</b> (a THEOREM, machine-checked: the unit-claim ratio equals the price-cross form exactly), <b>who the owners are is empirical</b> (the top-heavy ownership above), and <b>why the price rose is unproven</b>. Two honest caveats: real asset-unit growth (~1-2%/yr) is a small first-order correction, and the aggregate pie did grow — real US household net worth roughly <b>doubled</b> (×{_cons['real_aggregate_nw_growth']:.1f}). The claim is about labor's shrinking <i>share-claim</i> on that pie and its concentration, not "no wealth was created."</p>

<h2>Falsify it yourself — the live certificate</h2>
<p class=muted>Do not trust the numbers above; move them. Set your own wage growth, asset growth, and the tolerance you would grant the data, and the certificate recomputes: R₀ (labor's relative price), the breakdown error e*, the adversarial worst case, and the verdict. The claim is only as good as its ability to survive your inputs.</p>
<div style="background:#f7f9fc;border:1px solid #cbd8ea;border-radius:10px;padding:14px 16px;margin:14px 0;font:14px/1.7 -apple-system,Segoe UI,Roboto,sans-serif">
 <div style="display:flex;flex-wrap:wrap;gap:14px 26px;align-items:center">
  <label>Wage grew ×<input id=fx_w type=number value=2.02 step=0.01 min=0.1 style="width:74px"></label>
  <label>Asset grew ×<input id=fx_a type=number value=8.55 step=0.01 min=0.1 style="width:74px"></label>
  <label>Data tolerance ±<input id=fx_t type=number value=5 step=1 min=0 max=45 style="width:60px">%</label>
 </div>
 <div id=fx_out style="margin-top:12px;font-size:15px"></div>
</div>

<h2>Where the proof stops — on purpose</h2>
<p class=muted>The certified core is narrow by design. It does <b>not</b> establish:</p>
<ul class=muted style="margin:6px 0 0 4px;line-height:1.7">
<li><b>That the dollar was "debased."</b> A fallen labor:gold ratio and a risen gold price are the same fact seen two ways; which one you name the mover is a modelling choice, not a theorem.</li>
<li><b>That any actor, policy or institution caused it.</b> This is correlation across series, not a mechanism.</li>
<li><b>Any moral claim</b> — "exploitation," "theft," intent. None follow from an exchange ratio.</li>
<li><b>The exact magnitudes.</b> Levels are representative and rounded; only the directions above are claimed, and only where e* clears {_ptol:.0f}%.</li>
</ul>
<p class=muted>What remains, fully proven — stated as precisely as the evidence permits: <b>over 2000→2024, a year of ordinary US labor came to command materially less of every liquid, independent store of value — gold, silver, equities — and against hard money that decline cannot be dismissed as a single-asset bubble (it holds across gold and silver), as data noise (it survives &gt;26% simultaneous error in every input), or as a cherry-picked endpoint (it also certifies from a 2007 base).</b> With authoritative primary series the certified basket widens to include <b>homes on every price lens</b> (median, constant-quality, per-square-foot). The sharper, CPI-dependent reading: real <i>consumption</i> wages roughly held; what collapsed was labor's claim on <i>assets</i> — the price of the store-of-value economy, measured in wage-hours, inflated several-fold — though the monthly mortgage <i>carry</i> is the one exception that stayed within noise, so the housing squeeze is about the down-payment, not the payment. On cause, monetary expansion is a supported <i>partial</i> driver, not a proven complete one. Every statement here carries its own certainty tier, and the honest boundary — long-horizon not last-decade, total not decomposition, price not carry, association not cause — is drawn exactly where each one fails.</p>

<h1 style="margin-top:56px">The instrument hides the concentration</h1>
<p class=muted>The proof above measures the <i>typical</i> worker. But the asset-price inflation that cost labor its wage-hours did not vanish — it accrued to whoever <b>owned</b> the assets. To see that transfer you have to look at wealth concentration, and here the most-cited government statistic is built so it <b>cannot show you</b>. This is not a claim that anyone fabricated a number; it is that the popular instrument — the Census money-income bracket table — has fine resolution where there is no concentration and none where all of it lives, while the Fed's own data shows the tail plainly. Judge "lie" versus "choice" yourself; the mechanism is demonstrable.</p>

<div>
<span class=k>Same country, switch the question<br>income Gini <b>{_gI}</b> → wealth Gini <b>{_gW}</b> &nbsp;(×{_gW/_gI:.2f})</span>
<span class=k>Bottom half of America<br>owns <b>{_b50}%</b> of the wealth</span>
<span class=k>Top 0.1% (Fed data)<br>owns <b>{_t01}%</b> — invisible to the income brackets</span>
<span class=k>Owners of the assets that inflated<br>top 10% hold <b>~89%</b> of equities</span>
</div>

<h2>The open bucket — fine at the bottom, infinite at the top</h2>
<p class=muted>The standard Census household-income table resolves the bottom in $10-15k steps, then dumps everyone from the comfortable to the billionaire into one open-ended "$200k and over" bin. No top 1%, 0.1% or 0.01% can exist in it — the concentration is quite literally off the chart, by construction.</p>
<div id=bracketbar class=plot style="height:360px"></div>

<h2>What the Fed's own data shows</h2>
<p class=muted>The Federal Reserve's Distributional Financial Accounts — also US government data — resolves the tail the income table erases. Net-worth share by group; the top 1% (dark) contains a top 0.1% of {_t01}% on its own, and the bottom half of the country holds {_b50}%.</p>
<div id=wealthbar class=plot style="height:300px"></div>

<h2>Where the wage-hours went — who owns the inflated assets</h2>
<p class=muted>This closes the loop with the proof. The gold, equities and housing that rose several-fold in wage-hours are owned overwhelmingly at the top (Survey of Consumer Finances). The purchasing power labor lost to asset prices is the wealth asset-holders gained — and Census money income, which excludes capital gains, never records it.</p>
<div id=ownbar class=plot style="height:300px"></div>

<h2>Why the headline gauge stays calm — the Gini hides the tail</h2>
<p class=muted>Even the inequality number itself is built to under-react. On a synthetic US-shaped income distribution, <b>doubling</b> the income of the top 0.1% raises that group's share by <b>+{_td['topshare_rise_pct']:.0f}%</b> — but the headline Gini moves only from <b>{_td['base_gini']}</b> to <b>{_td['shocked_gini']}</b> (<b>+{_td['gini_rise_pct']:.0f}%</b>, a drift it makes over a normal decade). A metric dominated by the middle cannot register a tail event; reported alone, it reads as stability during a concentration.</p>

<h2>The structural distortions, itemised</h2>
<table><thead><tr><th>Bucket choice</th><th>How it conceals</th><th>honest tag</th></tr></thead><tbody>{distortion_rows()}</tbody></table>
<p class=muted>Read the tags honestly: several are genuine <span style="color:#c53030">distortions</span> of what a reader thinks they are seeing; one is a plain <span style="color:#8a8378">statistical fact</span> about the Gini; one is a <span style="color:#8a8378">confounder</span>. Some choices have defensible motives (top-coding protects privacy; open bins protect small-sample reliability). The demonstrable point stands regardless of motive: <b>the most-headlined instrument cannot show the concentration, and the government's own fuller series can</b>. What you conclude about intent is your call — this page only draws the receipts.</p>

<h2>The concentration, moving (1989 → 2024)</h2>
<p class=muted>Not two snapshots — the trajectory. Federal Reserve net-worth shares over 35 years: the top 0.1% and top 1% climb while the bottom half flatlines near the floor (and briefly near zero after 2008). The same span, mirrored: a year of median labor fell from 100 to <b>{wd['labor_sp_index'][-1]:.0f}</b> in S&amp;P-shares (1989=100). Concentration up, labor's asset-claim down, together.</p>
<div id=dfabar class=plot style="height:360px"></div>

<h2>The number is a choice — how each index sees the same tail</h2>
<p class=muted>Take one distribution and <b>double</b> the income of the top 0.1%. Every inequality measure registers it differently, because each weights the tail differently. The Gini — the one almost always reported — moves least; top-share and Theil measures move most. Reporting a calm Gini during a tail event is not wrong arithmetic, it is a choice of instrument.</p>
<div id=familybar class=plot style="height:360px"></div>
<table><thead><tr><th>Index</th><th>base</th><th>after top-0.1% doubles</th><th>change</th></tr></thead><tbody>{family_rows()}</tbody></table>
<p class=muted>Atkinson at high inequality-aversion moves little too — but for the opposite reason: it looks at the <i>bottom</i>, not the top. The lesson is the same: no single scalar captures a distribution, and which one is headlined decides whether a concentration looks like a crisis or a calm.</p>

<h1 style="margin-top:56px">Provenance &amp; durability</h1>
<p class=muted>Every number here is traceable. Of the {_ntot} inputs, <b>{_nlive} are fetched live</b> from the St. Louis Fed's keyless CSV mirror of the primary agencies (BLS, S&amp;P CoreLogic, Census/HUD, Federal Reserve), refreshed by a committed script; the rest are documented snapshots (LBMA gold &amp; silver, long-history S&amp;P, S&amp;P earnings) with citations. The figures reasoned from earlier <b>reconcile with the live sources to within {_recon_max:.1f}%</b> — the hand estimates were right.</p>
<table><thead><tr><th>Series ID</th><th>What it is</th><th>type</th><th>as of</th><th>link</th></tr></thead><tbody>{prov_rows()}</tbody></table>

<h2>Cached to your browser — in case the data disappears</h2>
<p class=muted>Government pages get revised, moved, and sometimes deleted. So on first view this page <b>archives its full dataset to your browser's local storage</b>, keeping the earliest copy you ever loaded alongside the latest. If the sources later change or vanish, your archived copy remains — and you can export it to a file.</p>
<div style="background:#f7f9fc;border:1px solid #cbd8ea;border-radius:10px;padding:14px 16px;margin:14px 0;font:14px/1.7 -apple-system,Segoe UI,Roboto,sans-serif">
 <div id=cache_status>archiving…</div>
 <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:10px">
  <button id=cache_export style="cursor:pointer;background:#1f4e79;color:#fff;border:0;border-radius:6px;padding:8px 14px;font-size:13px">Download my archived copy (JSON)</button>
  <button id=cache_first style="cursor:pointer;background:#fffdf8;color:#1f4e79;border:1px solid #cbd8ea;border-radius:6px;padding:8px 14px;font-size:13px">Export first-seen snapshot</button>
 </div>
</div>

<p class=muted style="margin-top:34px">Overlay, not proof: repricing strips monetary debasement out of a nominal figure, but it does not by itself establish cause. 2025–26 metal prices are annual-average approximations and provisional.</p>
</section>

<aside class="col col-story">
<div class=colhead>In plain terms — what it means &amp; what to do</div>
<h1>The paycheck still works. The ladder moved.</h1>
<p class=lead>The charts on the left are careful and hedged. Here is what they add up to for an ordinary person, in plain language — what is happening, why, how, where it goes, and what actually helps, depending on who you are.</p>

<span class=story-tag>What is happening</span>
<h2>Your wage buys groceries. It no longer buys the future.</h2>
<p>Measured against the everyday basket — food, gas, rent — a typical paycheck buys about what it did around 2000; by the official measure it even edged up a little (real wages roughly {_realwage:+.0f}%). So day to day, work still works.</p>
<p>What changed is the price of the things that turn income into <b>lasting wealth</b> — a slice of the stock market, an ounce of gold, a home. Measured in <i>hours of work</i>, those pulled away. A year of the average job bought about <b>{_all['gold'][0]:.0f} ounces of gold in 2000 and roughly {_all['gold'][-1]:.0f} today</b>; a year at the federal minimum, {_mw['gold'][0]:.0f} ounces then, about {_mw['gold'][-1]:.0f} now. You can still live on wages. Turning wages into ownership is what got harder — and the people who already owned those assets grew wealthier as the prices climbed.</p>

<span class=story-tag>Why it happened</span>
<h2>Endogenous, not engineered — and no single cabal.</h2>
<p>The tempting story — "they just printed money" — is only part of it, and the map's evidence says so. Money did grow about <b>{_m2:.1f}×</b> since 2000 while shelf prices rose less than half that, so the new money pooled in <b>assets</b>, not groceries; corporate profits climbed as labor's share of national income fell about <b>{abs(_ls['rel_change_pct']):.0f}%</b>. But the deeper pattern is the one Minsky named: stability breeds leverage, leverage breeds fragility, and the system manufactures its own instability from the inside. Around that sit a small <b>operator-network</b> and a few <b>recurring structures</b> — the same self-referential funding loops and off-balance-sheet marks, rebuilt in each era's least-regulated venue. Not one hidden hand; a shape the machinery keeps returning to. (Consistent with the rest of the investigation, intent is never inferred from who stands next to whom.)</p>

<span class=story-tag>How it works</span>
<h2>Self-marked value — and yardsticks built not to show it.</h2>
<p>Two mechanics do most of the work. First, the transfer: the pile of real assets is roughly fixed, so when its price rises no new shares or acres appear — ownership just becomes worth more to whoever already holds it, and dearer to anyone buying in with a paycheck. Second, the <b>mark</b>: in the places risk hides — bank bonds at cost, AI stakes at self-set marks, private-credit loans at the manager's own valuation, insurance liabilities in offshore captives — value is a <i>chosen number, not a market price</i>, held until a forcing event prices it. And much of that risk has been quietly moved onto <b>ordinary retirement money</b> — pension, annuity and 401(k) exposure to manager-marked private credit — so the people least able to check the number are the ones holding it.</p>
<p>The instruments we are handed are built not to reveal this. Official rent (CPI shelter) trails real market rents by roughly a year — new-lease measures such as the Apartment List index led it by about <b>16 months</b> — so the shelter figure can be quoted whichever way suits the moment. The jobs count gets revised down by hundreds of thousands after the headlines fade. The income table tops out at "$200,000 and over," and the Gini index barely moves when the very top doubles. The concentration is real — the Federal Reserve's own data puts the wealth gap ({_gW}) far above the income gap ({_gI}), the bottom half holding about <b>{_b50}%</b> and the top 0.1% about <b>{_t01}%</b> — the popular gauges just aren't built to show it. In the one unit that cannot be marked to myth — gold — most "gains" vanish: a year of the average job bought about {_all['gold'][0]:.0f} ounces in 2000 and roughly {_all['gold'][-1]:.0f} today.</p>

<span class=story-tag>The history</span>
<h2>Fifty years, in one breath.</h2>
<p>1971: the dollar leaves gold. Decades of financialization follow. 2000: the dot-com peak. 2008: the crisis, then central banks buy assets on a vast scale, lifting their prices. 2020: pandemic stimulus. 2021-24: inflation, then the sharpest rate spike in decades. Every step nudged value toward those who already held assets — not by a single plan, but by the shape of the machinery.</p>

<span class=story-tag>Where it goes</span>
<h2>Structure certain, date unknowable.</h2>
<p>The map is careful here, and so is this: the <i>structure</i> is provable — a capital loop solvent only while fresh money keeps flowing, marks that must reverse once something forces a real price — but the <i>date</i> is not (that is Minsky and Keynes; dot-com, 2008 and SVB were all visible for years, then broke suddenly on a catalyst no one timed). Extend the trend and the on-ramp to real ownership keeps narrowing for anyone starting from zero. But the thing that breaks first is the one the map treats as decisive: <b>legitimacy — trust</b>. When the scoreboard stops matching what people live, consent erodes; and trust is far harder to rebuild than a price.</p>

<span class=story-tag>What to do</span>
<h2>Depending on who you are.</h2>
<div class=aud><span class=who>If you're starting out, or can barely save</span><b>Verify, don't trust; own, don't rent.</b> Anchor your footing in things that can't be marked to myth — real skills, a hard-money yardstick, tools and (when reachable) a home you actually <i>own and can repair</i> — not a nominal figure someone else can reset. Cut your own fragility (Minsky at the kitchen table): avoid leverage and high-interest debt, keep a margin of safety, and understand where your retirement money's risk actually sits before you trust it. Resist the lock-ins that quietly turn ownership back into rental — parts-pairing, bricking subscriptions, account-bound devices — and the surveillance rails (age-verification, digital-ID) you can still refuse. If real ownership is out of reach today, that is a structural constraint, not a personal failing — name it, and push on the fixes below.</div>
<div class=aud><span class=who>If you're raising a family</span>Pass on real value and the <b>habit of verification</b>, not just cash: repairable tools you own, a hard-money yardstick, and the reflex to doubt the headline number. Teach that a mark is not a price.</div>
<div class=aud><span class=who>If you build things — tech, finance, tools</span>Build to <b>minimize required trust and preserve ownership</b>: verifiable, self-custodial, open, repairable, decentralized. Every unit of trust you replace with proof is legitimacy restored. And don't build the "privacy-preserving" version of a surveillance mandate — a cleaner honeypot still legitimizes the mandate.</div>
<div class=aud><span class=who>If you already own a great deal</span>Your center of gravity is <b>legitimacy</b>, not the balance sheet — and self-marked gains reverse when a real price finally arrives. Broad real ownership, marks that meet the market, and honest measurement even when it stings are what keep the system's consent — which protects your stake too.</div>
<div class=aud><span class=who>If you set policy</span>Stop letting the gauge become the target: fix the shelter-rent lag, the jobs benchmark and the open-topped income bucket, and publish the tail plainly. Mark risk to market, not to management, and keep it off retirees' accounts. Protect the right to repair and to own; reject population-scale identity mandates; reduce systemic leverage; build real housing so real assets aren't kept artificially scarce. Restore the yardstick, and the consent.</div>

<span class=story-tag>The goal</span>
<h2>A verifiable stake — and beyond.</h2>
<p>Protecting the least-protected who are genuinely trying means making the <b>first rung reachable and real</b>: a durable, verifiable stake in things you actually own — not a nominal number that debases, nor a mark someone can reset, nor a life rented from the platforms. The American Dream, honestly updated, isn't a figure on a screen; it is <i>ownership you can verify and repair</i>, plus the legitimacy that lets ordinary effort compound. Beyond that is the real fork of the decade: as AI makes the asset base far more productive, those gains can be pulled further into the loop, or spread through broad, verifiable ownership. The data can't make that choice — it can only make it impossible to pretend we didn't see it.</p>
<p class=muted>This column is interpretation — graded overlay, corrigible, in the map's own discipline: only the machine-verified core (left, and the wider investigation) carries the weight of "proven"; nothing here asserts a coordinated cabal, and intent is never inferred from adjacency. See the <a href="lenses.html">lenses</a> and <a href="methodology.html">methodology</a>. The facts are the starting point, not the verdict.</p>
</aside>
</div>
</main>
<script>
const D={DATA_JSON};
const PLANES=["USD","Gold-oz","Silver-oz"], KEY=["usd","gold","silver"];
const ink="#33312c", grid_c="#e4ddcc";
// 3D: one trace per asset, points across (year, plane, log index)
const traces=[];
D.grid.forEach(row=>{{
  const xs=[],ys=[],zs=[],txt=[];
  KEY.forEach((k,pi)=>{{
    row.years.forEach((yr,i)=>{{
      const v=row[k][i]; if(v==null) return;
      xs.push(yr); ys.push(pi); zs.push(v);
      txt.push(row.asset+"<br>"+yr+" · "+PLANES[pi]+"<br>index "+v.toFixed(0));
    }});
    xs.push(null);ys.push(null);zs.push(null);txt.push(null); // break line between planes
  }});
  traces.push({{type:"scatter3d",mode:"lines+markers",name:row.asset,
    x:xs,y:ys,z:zs,text:txt,hoverinfo:"text",
    line:{{color:D.colors[row.asset],width:4}},marker:{{size:3,color:D.colors[row.asset]}},
    visible: (row.asset.indexOf("self")>-1)?"legendonly":true}});
}});
Plotly.newPlot("plot3d",traces,{{
  margin:{{l:0,r:0,t:6,b:0}},paper_bgcolor:"#fcfcfb",
  legend:{{font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}},orientation:"h",y:-0.02}},
  scene:{{
    xaxis:{{title:"year",gridcolor:grid_c,color:ink,tickformat:"d"}},
    yaxis:{{title:"money",tickvals:[0,1,2],ticktext:PLANES,gridcolor:grid_c,color:ink}},
    zaxis:{{title:"index (base=100, log)",type:"log",gridcolor:grid_c,color:ink}},
    camera:{{eye:{{x:1.7,y:-1.5,z:0.9}}}}
  }}
}},{{displayModeBar:false,responsive:true}});
// GSR 2D line
Plotly.newPlot("gsr",[{{type:"scatter",mode:"lines+markers",
  x:D.gsr.map(r=>r.year),y:D.gsr.map(r=>r.ratio),
  line:{{color:"#7b2d26",width:2}},marker:{{size:6,color:"#7b2d26"}},
  hovertemplate:"%{{x}}<br>GSR %{{y:.1f}}<extra></extra>"}}],{{
  margin:{{l:44,r:14,t:10,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
  xaxis:{{gridcolor:grid_c,color:ink,tickformat:"d"}},
  yaxis:{{title:"oz silver per oz gold",gridcolor:grid_c,color:ink,rangemode:"tozero"}}
}},{{displayModeBar:false,responsive:true}});

// ===================== WAGES =====================
const W={WAGE_JSON};
// validated categorical (dataviz reference theme): blue, aqua, yellow, green, violet, red
const CAT=["#2a78d6","#1baf7a","#eda100","#008300","#4a3aa7","#e34948"];
const LOSS="#e34948", GAIN="#2a78d6", NEUT="#8a8378";
const occ=n=>W.occupations.find(r=>r.name.indexOf(n)===0);

// --- 3D: five benchmark earners across the three money-planes (base 2000 = 100, log) ---
(function(){{
  const picks=[occ("Management"),occ("Computer"),occ("All occ"),occ("Food"),W.minimum_wage];
  const IDX=["usd_idx","gold_idx","silver_idx"];
  const tr=[];
  picks.forEach((row,ci)=>{{
    const xs=[],ys=[],zs=[],txt=[];
    IDX.forEach((k,pi)=>{{
      row.years.forEach((yr,i)=>{{
        xs.push(yr);ys.push(pi);zs.push(row[k][i]);
        txt.push(row.name+"<br>"+yr+" · "+PLANES[pi]+"<br>index "+row[k][i].toFixed(0));
      }});
      xs.push(null);ys.push(null);zs.push(null);txt.push(null);
    }});
    const c=CAT[ci%CAT.length];
    tr.push({{type:"scatter3d",mode:"lines+markers",name:row.name,x:xs,y:ys,z:zs,
      text:txt,hoverinfo:"text",line:{{color:c,width:4}},marker:{{size:3,color:c}}}});
  }});
  Plotly.newPlot("wage3d",tr,{{margin:{{l:0,r:0,t:6,b:0}},paper_bgcolor:"#fcfcfb",
    legend:{{font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}},orientation:"h",y:-0.02}},
    scene:{{xaxis:{{title:"year",gridcolor:grid_c,color:ink,tickformat:"d"}},
      yaxis:{{title:"money",tickvals:[0,1,2],ticktext:PLANES,gridcolor:grid_c,color:ink}},
      zaxis:{{title:"index (2000=100, log)",type:"log",gridcolor:grid_c,color:ink}},
      camera:{{eye:{{x:1.7,y:-1.5,z:0.9}}}}}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Horizontal bar: gold index 2024 (2000=100), ordered worst-first; ref line at 100 ---
(function(){{
  const rows=[W.minimum_wage].concat(W.occupations).map(r=>({{n:r.name,v:r.gold_idx[r.gold_idx.length-1]}}));
  rows.sort((a,b)=>a.v-b.v);
  Plotly.newPlot("wagegold",[{{type:"bar",orientation:"h",
    x:rows.map(r=>r.v),y:rows.map(r=>r.n),
    marker:{{color:rows.map(r=>r.v>=100?GAIN:LOSS)}},
    text:rows.map(r=>r.v.toFixed(0)),textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}}<br>%{{x:.0f}} of 2000 gold value<extra></extra>"}}],{{
    margin:{{l:180,r:40,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"a year's wage in gold, 2024 (2000 = 100)",gridcolor:grid_c,color:ink,range:[0,112],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    shapes:[{{type:"line",x0:100,x1:100,y0:-0.5,y1:rows.length-0.5,line:{{color:NEUT,width:1.5,dash:"dash"}}}}],
    annotations:[{{x:100,y:rows.length-1,xanchor:"right",yshift:2,showarrow:false,
      text:"100 = kept pace with gold (none did)",font:{{color:"#8a8378",size:10.5}},
      bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Regions: grouped bars, USD index vs gold index (2000=100) ---
(function(){{
  const names=W.regions.map(r=>r.name);
  Plotly.newPlot("wageregion",[
    {{type:"bar",name:"USD (2000=100)",x:names,y:W.regions.map(r=>r.usd_idx[r.usd_idx.length-1]),
      marker:{{color:CAT[0]}},text:W.regions.map(r=>r.usd_idx[r.usd_idx.length-1].toFixed(0)),
      textposition:"outside",textfont:{{color:ink,size:11}},
      hovertemplate:"%{{x}} · USD idx %{{y:.0f}}<extra></extra>"}},
    {{type:"bar",name:"Gold-oz (2000=100)",x:names,y:W.regions.map(r=>r.gold_idx[r.gold_idx.length-1]),
      marker:{{color:CAT[2]}},text:W.regions.map(r=>r.gold_idx[r.gold_idx.length-1].toFixed(0)),
      textposition:"outside",textfont:{{color:ink,size:11}},
      hovertemplate:"%{{x}} · gold idx %{{y:.0f}}<extra></extra>"}}
  ],{{barmode:"group",bargap:0.28,bargroupgap:0.12,
    margin:{{l:44,r:14,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    legend:{{orientation:"h",y:1.14,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}}}},
    xaxis:{{color:ink}},yaxis:{{title:"index (2000 = 100)",gridcolor:grid_c,color:ink,
      range:[0,Math.max.apply(null,W.regions.map(r=>r.usd_idx[r.usd_idx.length-1]))*1.16]}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Gig vs traditional: gold-oz per year of work (2024) ---
(function(){{
  const keys=Object.keys(W.gig), vals=keys.map(k=>W.gig[k].gold);
  Plotly.newPlot("waggig",[{{type:"bar",x:keys,y:vals,
    marker:{{color:[CAT[3],CAT[2],LOSS]}},
    text:vals.map(v=>v.toFixed(1)+" oz"),textposition:"outside",textfont:{{color:ink,size:12}},
    hovertemplate:"%{{x}}<br>%{{y:.1f}} oz gold / yr<extra></extra>"}}],{{
    margin:{{l:52,r:14,t:16,b:52}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{color:ink,automargin:true}},yaxis:{{title:"oz gold per year of work (2024)",gridcolor:grid_c,color:ink,
      range:[0,Math.max.apply(null,vals)*1.16]}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Composition: stacked area, employment share by super-group over time ---
(function(){{
  const c=W.composition, ys=c.years, groups=Object.keys(c.groups);
  const tr=groups.map((g,i)=>({{type:"scatter",mode:"lines",name:g,x:ys,y:c.groups[g],
    stackgroup:"one",line:{{width:0.5,color:"#fcfcfb"}},fillcolor:CAT[i%CAT.length],
    hovertemplate:g+"<br>%{{x}} · %{{y:.1f}}%<extra></extra>"}}));
  Plotly.newPlot("wagecomp",tr,{{margin:{{l:44,r:14,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    legend:{{orientation:"h",y:-0.14,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:11.5}}}},
    xaxis:{{color:ink,tickformat:"d",tickvals:ys}},
    yaxis:{{title:"share of US employment (%)",gridcolor:grid_c,color:ink,range:[0,100]}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Proof: breakdown error e* per numeraire; dashed line at the data tolerance ---
(function(){{
  const P={PROOF_JSON}, tol=P.data_tol*100;
  const rows=P.labor["All occupations (mean wage)"].slice().sort((a,b)=>b.breakdown_pct-a.breakdown_pct);
  Plotly.newPlot("proofbar",[{{type:"bar",orientation:"h",
    x:rows.map(r=>r.breakdown_pct),y:rows.map(r=>r.numeraire),
    marker:{{color:rows.map(r=>r.certified?"#0ca30c":"#8a8378")}},
    text:rows.map(r=>r.breakdown_pct.toFixed(0)+"%"+(r.certified?"  certified":"  not certified")),
    textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}}<br>overturning needs >%{{x:.0f}}% error in every input<extra></extra>"}}],{{
    margin:{{l:150,r:120,t:8,b:40}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"breakdown error e* — uniform input error needed to overturn the decline",
      gridcolor:grid_c,color:ink,range:[0,54],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    shapes:[{{type:"line",x0:tol,x1:tol,y0:-0.5,y1:rows.length-0.5,line:{{color:"#c53030",width:1.5,dash:"dash"}}}}],
    annotations:[{{x:tol,y:rows.length-0.5,text:"data tolerance "+tol.toFixed(0)+"%",showarrow:false,
      yshift:12,xanchor:"left",font:{{color:"#c53030",size:11}},bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Decomposition: per asset, real-wage term (labor:CPI) vs asset-inflation term (CPI:asset) ---
(function(){{
  const P={PROOF_JSON}, dc=P.decomposition, names=Object.keys(dc);
  Plotly.newPlot("decompbar",[
    {{type:"bar",name:"real wage (labor : CPI)",x:names,y:names.map(n=>dc[n].real_wage_term),
      marker:{{color:"#0ca30c"}},text:names.map(n=>"×"+dc[n].real_wage_term.toFixed(2)),
      textposition:"outside",textfont:{{color:ink,size:11}},
      hovertemplate:"%{{x}}<br>real wage ×%{{y:.3f}}<extra></extra>"}},
    {{type:"bar",name:"asset price in wage-hours (CPI : asset)",x:names,y:names.map(n=>dc[n].asset_inflation_term),
      marker:{{color:"#c53030"}},text:names.map(n=>"×"+dc[n].asset_inflation_term.toFixed(2)),
      textposition:"outside",textfont:{{color:ink,size:11}},
      hovertemplate:"%{{x}}<br>asset inflation ×%{{y:.3f}}<extra></extra>"}}
  ],{{barmode:"group",bargap:0.3,bargroupgap:0.12,
    margin:{{l:44,r:14,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    legend:{{orientation:"h",y:1.14,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}}}},
    xaxis:{{color:ink}},yaxis:{{title:"multiplier on labor's asset-price (2000→2024)",gridcolor:grid_c,color:ink,rangemode:"tozero"}},
    shapes:[{{type:"line",x0:-0.5,x1:names.length-0.5,y0:1,y1:1,line:{{color:"#8a8378",width:1.5,dash:"dash"}}}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Home lenses: a year of labor buys X% of the home it did in 2000 (carry = the exception) ---
(function(){{
  const H=({PROOF_JSON}).homes_alnri.slice().sort((a,b)=>a.pct_of_2000-b.pct_of_2000);
  Plotly.newPlot("alnribar",[{{type:"bar",orientation:"h",
    x:H.map(h=>h.pct_of_2000),y:H.map(h=>h.lens.split(" (")[0]),
    marker:{{color:H.map(h=>h.certified?LOSS:"#8a8378")}},
    text:H.map(h=>h.pct_of_2000.toFixed(0)+"%"+(h.certified?"  certified":"  within noise")),
    textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}}<br>labor buys %{{x:.0f}}% of the 2000 home<extra></extra>"}}],{{
    margin:{{l:210,r:120,t:8,b:38}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"a year of labor buys this share of the year-2000 home",gridcolor:grid_c,color:ink,range:[0,110],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    shapes:[{{type:"line",x0:100,x1:100,y0:-0.5,y1:H.length-0.5,line:{{color:"#8a8378",width:1.5,dash:"dash"}}}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Money: each multiple as a share of M2 growth; reference at 1.0 (= tracked money) ---
(function(){{
  const M=({PROOF_JSON}).money, rows=M.rows.slice().sort((a,b)=>b.vs_m2-a.vs_m2);
  Plotly.newPlot("moneybar",[{{type:"bar",x:rows.map(r=>r.item),y:rows.map(r=>r.vs_m2),
    marker:{{color:rows.map(r=>r.vs_m2>=1?CAT[2]:CAT[0])}},
    text:rows.map(r=>r.vs_m2.toFixed(2)+"×"),textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{x}}<br>%{{y:.2f}}× the growth of M2<extra></extra>"}}],{{
    margin:{{l:44,r:14,t:8,b:80}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{color:ink,tickangle:-30,automargin:true}},
    yaxis:{{title:"growth 2000→2024, as a multiple of M2 growth",gridcolor:grid_c,color:ink,rangemode:"tozero"}},
    shapes:[{{type:"line",x0:-0.5,x1:rows.length-0.5,y0:1,y1:1,line:{{color:"#c53030",width:1.5,dash:"dash"}}}}],
    annotations:[{{x:rows.length-1,y:1,text:"= tracked M2",showarrow:false,yshift:11,xanchor:"right",font:{{color:"#c53030",size:11}},bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// ===================== WEALTH CONCENTRATION =====================
const WC={WC_JSON};
// --- Census brackets: share per bin; the open top bin flagged red ---
(function(){{
  const B=WC.brackets;
  Plotly.newPlot("bracketbar",[{{type:"bar",x:B.map(b=>b.label),y:B.map(b=>b.share),
    marker:{{color:B.map(b=>b.open?"#c53030":"#2a78d6")}},
    text:B.map(b=>b.open?b.share.toFixed(0)+"%  ← OPEN":b.share.toFixed(0)+"%"),
    textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{x}}<br>%{{y:.1f}}% of households"+"<extra></extra>"}}],{{
    margin:{{l:44,r:14,t:16,b:72}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{color:ink,tickangle:-35,automargin:true}},
    yaxis:{{title:"share of US households (%)",gridcolor:grid_c,color:ink,
      range:[0,Math.max.apply(null,B.map(b=>b.share))*1.22]}},
    annotations:[{{x:B.length-1,y:B[B.length-1].share,yshift:30,showarrow:true,arrowcolor:"#c53030",ax:0,ay:-6,
      xanchor:"right",text:"$200k → billionaire,<br>one undivided bin",align:"right",
      font:{{color:"#c53030",size:11}},bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Fed net-worth shares; top 1% dark, with a top-0.1% marker ---
(function(){{
  const S=WC.wealth_shares;
  Plotly.newPlot("wealthbar",[{{type:"bar",orientation:"h",
    x:S.map(s=>s.share),y:S.map(s=>s.group),
    marker:{{color:S.map(s=>s.group==="Top 1%"?"#7b2d26":(s.group==="Bottom 50%"?"#c53030":"#805ad5"))}},
    text:S.map(s=>s.share.toFixed(1)+"%"),textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}} hold %{{x:.1f}}% of net worth<extra></extra>"}}],{{
    margin:{{l:90,r:80,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"share of US net worth (%)",gridcolor:grid_c,color:ink,range:[0,42],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    annotations:[{{x:WC.top_0_1_share,y:"Top 1%",showarrow:true,arrowcolor:"#7b2d26",ax:36,ay:-4,
      xanchor:"left",text:"of which top 0.1% = "+WC.top_0_1_share+"%",font:{{color:"#7b2d26",size:11}},
      bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Ownership of the inflated assets by the top 10% ---
(function(){{
  const O=WC.ownership.slice().sort((a,b)=>a.top10_share-b.top10_share);
  Plotly.newPlot("ownbar",[{{type:"bar",orientation:"h",
    x:O.map(o=>o.top10_share),y:O.map(o=>o.asset),
    marker:{{color:"#805ad5"}},text:O.map(o=>o.top10_share+"%"),textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}}<br>top 10% hold %{{x}}%  (%{{customdata}})<extra></extra>",
    customdata:O.map(o=>o.note)}}],{{
    margin:{{l:210,r:60,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"share held by the top 10% (%)",gridcolor:grid_c,color:ink,range:[0,100],zeroline:false}},
    yaxis:{{color:ink,automargin:true}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// ===================== WEALTH DYNAMICS =====================
const WD={WD_JSON};
// --- DFA net-worth share trajectory 1989->2024 ---
(function(){{
  const yr=WD.dfa_years, col={{"Top 0.1%":"#7b2d26","Top 1%":"#805ad5","Top 10%":"#2a78d6","Bottom 50%":"#c53030"}};
  const tr=Object.keys(WD.dfa).map(g=>({{type:"scatter",mode:"lines+markers",name:g,x:yr,y:WD.dfa[g],
    line:{{color:col[g],width:2}},marker:{{size:6,color:col[g]}},
    hovertemplate:g+" %{{x}}: %{{y:.1f}}% of net worth<extra></extra>"}}));
  Plotly.newPlot("dfabar",tr,{{margin:{{l:44,r:14,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    legend:{{orientation:"h",y:1.12,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}}}},
    xaxis:{{color:ink,tickformat:"d",tickvals:yr}},
    yaxis:{{title:"share of US net worth (%)",gridcolor:grid_c,color:ink,rangemode:"tozero"}}
  }},{{displayModeBar:false,responsive:true}});
}})();
// --- inequality-index family: % change to the same top-0.1% doubling ---
(function(){{
  const F=WD.index_family;
  Plotly.newPlot("familybar",[{{type:"bar",orientation:"h",
    x:F.map(r=>r.change_pct),y:F.map(r=>r.index),
    marker:{{color:F.map(r=>r.index==="Gini"?"#c53030":(r.index.indexOf("share")>-1?"#0ca30c":"#805ad5"))}},
    text:F.map(r=>"+"+r.change_pct.toFixed(0)+"%"),textposition:"outside",textfont:{{color:ink,size:11}},
    hovertemplate:"%{{y}}: +%{{x:.0f}}% when the top 0.1% doubles<extra></extra>"}}],{{
    margin:{{l:130,r:96,t:8,b:40}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"movement when the top 0.1% income doubles (%)",gridcolor:grid_c,color:ink,
      zeroline:false,range:[0,Math.max.apply(null,F.map(r=>r.change_pct))*1.18]}},
    yaxis:{{color:ink,automargin:true}},
    annotations:[{{x:F.find(r=>r.index==="Gini").change_pct,y:"Gini",showarrow:true,arrowcolor:"#c53030",
      ax:78,ay:0,xanchor:"left",text:"the one<br>always reported",align:"left",
      font:{{color:"#c53030",size:11}},bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Interactive falsifier: recompute the certificate from the reader's own inputs ---
(function(){{
  const W=document.getElementById("fx_w"),A=document.getElementById("fx_a"),
        T=document.getElementById("fx_t"),O=document.getElementById("fx_out");
  function bd(R0){{const s=Math.sqrt(R0);return R0<1?(1-s)/(1+s):(s-1)/(s+1);}}
  function calc(){{
    const w=parseFloat(W.value),a=parseFloat(A.value),t=parseFloat(T.value)/100;
    if(!(w>0)||!(a>0)||!(t>=0)){{O.innerHTML="<span style='color:#c53030'>enter positive numbers</span>";return;}}
    const R0=w/a, e=bd(R0), Rworst=R0*((1+t)/(1-t))*((1+t)/(1-t)), fell=R0<1, cert=fell&&Rworst<1;
    const verdict = !fell ? "<b style='color:#0ca30c'>labor GAINED against this asset</b>"
      : cert ? "<b style='color:#0ca30c'>CERTIFIED decline</b> — survives your tolerance"
             : "<b style='color:#c53030'>fell, NOT certified</b> at your tolerance";
    O.innerHTML="a year of labor now buys <b>"+(R0*100).toFixed(0)+"%</b> of the asset it did "
      +"&nbsp;·&nbsp; breakdown error e* = <b>"+(e*100).toFixed(0)+"%</b> "
      +"&nbsp;·&nbsp; adversarial worst case R<sub>worst</sub> = <b>"+Rworst.toFixed(2)+"</b> "
      +"&nbsp;·&nbsp; "+verdict;
  }}
  [W,A,T].forEach(el=>el.addEventListener("input",calc)); calc();
}})();

// --- Mechanism: price multiple vs its principal fundamental driver ---
(function(){{
  const M={CM_JSON};
  const names=["Gold","Equities (S&P)","Housing"];
  const price=[M.gold.price_mult,M.equities.price_mult,M.housing.price_mult];
  const fund =[M.gold.m2_mult,M.equities.eps_mult,M.housing.rent_mult];        // gold's driver = M2 (monetary anchor)
  const dlab =["M2 (money)","earnings","rent"];
  const dcol =["#8a8378","#0ca30c","#0ca30c"];   // gold driver greyed: monetary, not a real fundamental
  Plotly.newPlot("mechbar",[
    {{type:"bar",name:"total price ×",x:names,y:price,marker:{{color:"#805ad5"}},
      text:price.map(v=>"×"+v.toFixed(2)),textposition:"outside",textfont:{{color:ink,size:11}},
      hovertemplate:"%{{x}} price ×%{{y:.2f}}<extra></extra>"}},
    {{type:"bar",name:"principal driver × (earnings / rent / money)",x:names,y:fund,marker:{{color:dcol}},
      text:fund.map((v,i)=>"×"+v.toFixed(2)),textposition:"outside",textfont:{{color:ink,size:11}},
      customdata:dlab,hovertemplate:"%{{x}} driver ×%{{y:.2f}} (%{{customdata}})<extra></extra>"}}
  ],{{barmode:"group",bargap:0.32,bargroupgap:0.12,
    margin:{{l:48,r:16,t:14,b:36}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    legend:{{orientation:"h",y:1.16,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}}}},
    xaxis:{{color:ink}},
    yaxis:{{title:"growth multiple 2000→2024",gridcolor:grid_c,color:ink,
      range:[0,Math.max.apply(null,price)*1.16]}},
    annotations:[{{xref:"paper",yref:"paper",x:0.16,y:0.97,xanchor:"center",showarrow:false,
      text:"gold has no cashflow —<br>its driver is monetary (M2)",align:"center",
      font:{{color:"#8a8378",size:10.5}},bgcolor:"rgba(255,253,248,0.94)",bordercolor:"#e4ddcc",borderpad:3}}]
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Durability: archive the full dataset to localStorage (first-seen + latest) + export ---
(function(){{
  const VER="{_dataver}";
  const bundle={{version:VER, denom:D, wages:W, proof:{PROOF_JSON}, wealth:WC, dynamics:WD, causal:{CM_JSON}}};
  const S=document.getElementById("cache_status");
  function iso(){{try{{return new Date().toISOString().slice(0,19).replace("T"," ")+" UTC";}}catch(e){{return "now";}}}}
  let firstAt=null, ok=false;
  try{{
    const KF="eb_archive_first", KL="eb_archive_latest";
    if(!localStorage.getItem(KF)) localStorage.setItem(KF, JSON.stringify({{savedAt:iso(),version:VER,data:bundle}}));
    localStorage.setItem(KL, JSON.stringify({{savedAt:iso(),version:VER,data:bundle}}));
    firstAt=JSON.parse(localStorage.getItem(KF)).savedAt; ok=true;
  }}catch(e){{}}
  S.innerHTML = ok
    ? "✓ archived to this browser · data vintage <b>"+VER+"</b> · first saved here <b>"+firstAt+"</b>. "
      +"Your copy survives even if the source pages change or are removed."
    : "<span style='color:#c53030'>local storage unavailable (private mode?) — the dataset is still inlined in this page.</span>";
  function dl(key,fname){{
    let payload;
    try{{payload=localStorage.getItem(key);}}catch(e){{}}
    if(!payload) payload=JSON.stringify({{savedAt:iso(),version:VER,data:bundle}});
    const blob=new Blob([payload],{{type:"application/json"}}), u=URL.createObjectURL(blob);
    const a=document.createElement("a"); a.href=u; a.download=fname; a.click(); URL.revokeObjectURL(u);
  }}
  document.getElementById("cache_export").addEventListener("click",()=>dl("eb_archive_latest","bubble-map-metals-data-latest.json"));
  document.getElementById("cache_first").addEventListener("click",()=>dl("eb_archive_first","bubble-map-metals-data-first-seen.json"));
}})();
</script></body></html>"""
open(os.path.join(DOCS,"multidenom.html"),"w").write(HTML)
print("wrote docs/multidenom.html  (%d assets, %d GSR years)"%(len(grid),len(gsr)))
