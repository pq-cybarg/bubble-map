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
</script></body></html>"""
open(os.path.join(DOCS,"multidenom.html"),"w").write(HTML)
print("wrote docs/multidenom.html  (%d assets, %d GSR years)"%(len(grid),len(gsr)))
