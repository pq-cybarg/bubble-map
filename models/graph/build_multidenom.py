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
</style></head><body>{NAV}{DISC}
<main>
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

<h2>Where the proof stops — on purpose</h2>
<p class=muted>The certified core is narrow by design. It does <b>not</b> establish:</p>
<ul class=muted style="margin:6px 0 0 4px;line-height:1.7">
<li><b>That the dollar was "debased."</b> A fallen labor:gold ratio and a risen gold price are the same fact seen two ways; which one you name the mover is a modelling choice, not a theorem.</li>
<li><b>That any actor, policy or institution caused it.</b> This is correlation across series, not a mechanism.</li>
<li><b>Any moral claim</b> — "exploitation," "theft," intent. None follow from an exchange ratio.</li>
<li><b>The exact magnitudes.</b> Levels are representative and rounded; only the directions above are claimed, and only where e* clears {_ptol:.0f}%.</li>
</ul>
<p class=muted>What remains, fully proven — stated as precisely as the evidence permits: <b>over 2000→2024, a year of ordinary US labor came to command materially less of every liquid, independent store of value — gold, silver, equities — and against hard money that decline cannot be dismissed as a single-asset bubble (it holds across gold and silver), as data noise (it survives &gt;26% simultaneous error in every input), or as a cherry-picked endpoint (it also certifies from a 2007 base).</b> The sharper, CPI-dependent reading: real <i>consumption</i> wages roughly held; what collapsed was labor's claim on <i>assets</i> — the price of the store-of-value economy, measured in wage-hours, inflated several-fold. Both statements carry their own certainty tier, and the honest boundary — long-horizon not last-decade, total not decomposition, correlation not cause — is drawn exactly where each one fails.</p>

<p class=muted style="margin-top:34px">Overlay, not proof: repricing strips monetary debasement out of a nominal figure, but it does not by itself establish cause. 2025–26 metal prices are annual-average approximations and provisional.</p>
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
    margin:{{l:180,r:36,t:8,b:34}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{title:"a year's wage in gold, 2024 (2000 = 100)",gridcolor:grid_c,color:ink,range:[0,30],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    shapes:[{{type:"line",x0:100,x1:100,y0:-0.5,y1:rows.length-0.5,line:{{color:NEUT,width:1.5,dash:"dash"}}}}]
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
    legend:{{orientation:"h",y:1.12,font:{{family:"-apple-system,Segoe UI,Roboto,sans-serif",size:12}}}},
    xaxis:{{color:ink}},yaxis:{{title:"index (2000 = 100)",gridcolor:grid_c,color:ink,rangemode:"tozero"}}
  }},{{displayModeBar:false,responsive:true}});
}})();

// --- Gig vs traditional: gold-oz per year of work (2024) ---
(function(){{
  const keys=Object.keys(W.gig), vals=keys.map(k=>W.gig[k].gold);
  Plotly.newPlot("waggig",[{{type:"bar",x:keys,y:vals,
    marker:{{color:[CAT[3],CAT[2],LOSS]}},
    text:vals.map(v=>v.toFixed(1)+" oz"),textposition:"outside",textfont:{{color:ink,size:12}},
    hovertemplate:"%{{x}}<br>%{{y:.1f}} oz gold / yr<extra></extra>"}}],{{
    margin:{{l:52,r:14,t:8,b:52}},paper_bgcolor:"#fcfcfb",plot_bgcolor:"#fcfcfb",
    xaxis:{{color:ink,automargin:true}},yaxis:{{title:"oz gold per year of work (2024)",gridcolor:grid_c,color:ink,rangemode:"tozero"}}
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
      gridcolor:grid_c,color:ink,range:[0,46],zeroline:false}},
    yaxis:{{color:ink,automargin:true}},
    shapes:[{{type:"line",x0:tol,x1:tol,y0:-0.5,y1:rows.length-0.5,line:{{color:"#c53030",width:1.5,dash:"dash"}}}}],
    annotations:[{{x:tol,y:rows.length-0.5,text:"data tolerance "+tol.toFixed(0)+"%",showarrow:false,
      yshift:10,font:{{color:"#c53030",size:11}}}}]
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
</script></body></html>"""
open(os.path.join(DOCS,"multidenom.html"),"w").write(HTML)
print("wrote docs/multidenom.html  (%d assets, %d GSR years)"%(len(grid),len(gsr)))
