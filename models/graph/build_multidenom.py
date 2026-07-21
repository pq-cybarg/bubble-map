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

NAV=('<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:11px 16px;'
     'font:13.5px/1.7 -apple-system,Segoe UI,Roboto,sans-serif;text-align:center">'
     +"".join(f'<a href="{h}" style="margin:0 9px;color:#1f4e79;text-decoration:none">{t}</a>'
              for h,t in [("index.html","Home"),("dashboard.html","Dashboard"),("charts.html","Charts"),
                          ("bubblemap.html","Bubble Map"),("leadership.html","Leadership"),("research.html","Research")])
     +'</div>')
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
</script></body></html>"""
open(os.path.join(DOCS,"multidenom.html"),"w").write(HTML)
print("wrote docs/multidenom.html  (%d assets, %d GSR years)"%(len(grid),len(gsr)))
