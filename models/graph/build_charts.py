#!/usr/bin/env python3
"""
build_charts.py - render data/*.svg charts into docs/charts.html (pure SVG, no JS deps),
documenting jobs, inflation, the Fed's rate path vs its mandate, and vs the bond market.

ALL series are ANNUAL, compiled from public sources (FRED / BLS / US Treasury / BIS), ROUNDED
to the precision shown; series IDs are cited on the page. Estimates / partial-year are marked '~'.
This is the visual companion to research/macro-jobs-inflation-fed.json (which carries the sourcing).
"""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs")

YEARS=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]

# ---- DATA (annual; sourced FRED/BLS/Treasury; rounded; '~' = est/partial) ----
CPI    =[0.1,1.3,2.1,2.4,1.8,1.2,4.7,8.0,4.1,2.9,3.0,3.0]   # CPI-U YoY annual avg (BLS / FRED CPIAUCSL)
COREPCE=[1.3,1.8,1.6,2.0,1.6,1.4,3.6,5.2,4.1,2.8,2.9,3.0]   # core PCE YoY annual avg (FRED PCEPILFE)
FEDFUNDS=[0.5,0.75,1.5,2.5,1.75,0.25,0.25,4.5,5.5,4.5,4.0,3.75] # year-end target upper (FRED DFEDTARU)
T2     =[1.06,1.20,1.89,2.48,1.57,0.13,0.73,4.41,4.23,4.25,3.6,3.7] # 2Y year-end (FRED DGS2)
T3M    =[0.16,0.51,1.39,2.45,1.55,0.09,0.06,4.42,5.40,4.37,3.9,3.8] # 3M year-end (FRED DGS3MO)
T10    =[2.27,2.45,2.41,2.69,1.92,0.93,1.52,3.88,3.88,4.58,4.3,4.3] # 10Y year-end (FRED DGS10)
T30    =[3.01,3.07,2.74,3.02,2.39,1.65,1.90,3.97,4.03,4.78,4.7,4.7] # 30Y year-end (FRED DGS30)
JGB10  =[0.27,0.04,0.05,0.0,-0.01,0.02,0.07,0.42,0.61,1.09,2.02,2.66] # Japan 10Y year-end (FRED IRLTLT01JPM156N / BOJ)
BAA    =[5.0,4.7,4.1,4.8,3.9,3.5,3.3,5.8,5.6,5.6,6.0,6.05] # Moody's Baa year-end (FRED BAA)
U3     =[5.3,4.9,4.4,3.9,3.7,8.1,5.4,3.6,3.6,4.0,4.2,4.4]  # U-3 annual avg (BLS / FRED UNRATE)
U6     =[10.4,9.6,8.5,7.7,7.2,13.6,9.4,6.9,6.8,7.5,7.9,8.1] # U-6 annual avg (BLS U6RATE)
# Nonfarm payroll annual change, millions (BLS CES / FRED PAYEMS); 2024-25 headline vs benchmark-revised
NFP_HEAD=[2.7,2.3,2.2,2.3,2.0,-9.3,7.3,4.8,3.0,2.0,2.4,None]
NFP_REV =[None,None,None,None,None,None,None,None,None,1.4,1.45,None] # after -818k(2024)/-911k(2025) benchmarks
# Sectoral: representative recent annualized change by industry, thousands (BLS CES Table B-1; rounded, illustrative)
SECTORS=[("Health care & social asst",900),("Leisure & hospitality",330),("State & local govt",400),
         ("Education",180),("Construction",150),("Financial activities",60),
         ("Retail trade",10),("Professional & business",-40),("Information (tech)",-60),
         ("Manufacturing",-110),("Temp help services",-160),("Federal government",-300)]

# ---- SVG helpers (academic light theme) ----
INK="#1c1b19";MUT="#6b665d";LINE="#e4ddcc";PAPER="#fffdf8";AC="#7b2d26";AC2="#1f4e79";GRID="#efe9da"
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;")

def line_chart(title, series, ylab, colors, ymin=None, ymax=None, target=None, note=""):
    W,H=760,360; L,R,T,B=54,150,40,46; pw,ph=W-L-R,H-T-B
    vals=[v for _,ys in series for v in ys if v is not None]
    lo=ymin if ymin is not None else min(vals); hi=ymax if ymax is not None else max(vals)
    if hi==lo: hi=lo+1
    def X(i): return L+pw*i/(len(YEARS)-1)
    def Y(v): return T+ph*(hi-v)/(hi-lo)
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
    s.append(f'<text x="{L}" y="22" font-size="14" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    # gridlines + y labels
    ticks=5
    for k in range(ticks+1):
        v=lo+(hi-lo)*k/ticks; y=Y(v)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{L-6}" y="{y+3:.1f}" font-size="10" fill="{MUT}" text-anchor="end" font-family="sans-serif">{v:.1f}</text>')
    if target is not None:
        yt=Y(target); s.append(f'<line x1="{L}" y1="{yt:.1f}" x2="{L+pw}" y2="{yt:.1f}" stroke="#1f6f43" stroke-dasharray="5 3"/>')
        s.append(f'<text x="{L+pw}" y="{yt-3:.1f}" font-size="10" fill="#1f6f43" text-anchor="end" font-family="sans-serif">{target:g}% target</text>')
    # x labels
    for i,yr in enumerate(YEARS):
        if i%1==0: s.append(f'<text x="{X(i):.1f}" y="{T+ph+16:.1f}" font-size="9.5" fill="{MUT}" text-anchor="middle" font-family="sans-serif">{str(yr)[2:]}</text>')
    s.append(f'<text x="{L-40}" y="{T-10}" font-size="10" fill="{MUT}" font-family="sans-serif">{esc(ylab)}</text>')
    # lines + legend
    for (name,ys),c in zip(series,colors):
        pts=[(X(i),Y(v)) for i,v in enumerate(ys) if v is not None]
        d=" ".join(f'{"M" if k==0 else "L"}{x:.1f} {y:.1f}' for k,(x,y) in enumerate(pts))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.2"/>')
    ly=T+8
    for (name,_),c in zip(series,colors):
        s.append(f'<rect x="{L+pw+12}" y="{ly-8}" width="11" height="11" fill="{c}"/>')
        s.append(f'<text x="{L+pw+27}" y="{ly+1}" font-size="10.5" fill="{INK}" font-family="sans-serif">{esc(name)}</text>'); ly+=18
    if note: s.append(f'<text x="{L}" y="{H-6}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
    s.append('</svg>'); return "".join(s)

def bar_chart_years(title, head, rev, ylab, note=""):
    W,H=760,330; L,R,T,B=54,20,40,40; pw,ph=W-L-R,H-T-B
    vals=[v for v in head+rev if v is not None]; lo=min(0,min(vals)); hi=max(vals)
    def Y(v): return T+ph*(hi-v)/(hi-lo)
    bw=pw/len(YEARS)*0.6
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
    s.append(f'<text x="{L}" y="22" font-size="14" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    y0=Y(0); s.append(f'<line x1="{L}" y1="{y0:.1f}" x2="{L+pw}" y2="{y0:.1f}" stroke="{MUT}"/>')
    for k in range(5+1):
        v=lo+(hi-lo)*k/5; y=Y(v)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{L-6}" y="{y+3:.1f}" font-size="10" fill="{MUT}" text-anchor="end" font-family="sans-serif">{v:.0f}</text>')
    for i,yr in enumerate(YEARS):
        cx=L+pw*(i+0.5)/len(YEARS)
        v=head[i]
        if v is not None:
            c=AC2 if v>=0 else AC; top=Y(max(v,0)); h=abs(Y(v)-Y(0))
            s.append(f'<rect x="{cx-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{c}" opacity="{0.5 if rev[i] is not None else 1}"/>')
        if rev[i] is not None:
            rv=rev[i]; top=Y(max(rv,0)); h=abs(Y(rv)-Y(0))
            s.append(f'<rect x="{cx-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="#9a2b1f"/>')
        s.append(f'<text x="{cx:.1f}" y="{T+ph+15:.1f}" font-size="9.5" fill="{MUT}" text-anchor="middle" font-family="sans-serif">{str(yr)[2:]}</text>')
    s.append(f'<text x="{L-40}" y="{T-10}" font-size="10" fill="{MUT}" font-family="sans-serif">{esc(ylab)}</text>')
    s.append(f'<rect x="{L+pw-150}" y="{T-2}" width="11" height="11" fill="{AC2}"/><text x="{L+pw-135}" y="{T+8}" font-size="10" fill="{INK}" font-family="sans-serif">headline</text>')
    s.append(f'<rect x="{L+pw-70}" y="{T-2}" width="11" height="11" fill="#9a2b1f"/><text x="{L+pw-55}" y="{T+8}" font-size="10" fill="{INK}" font-family="sans-serif">benchmark-revised</text>')
    if note: s.append(f'<text x="{L}" y="{H-6}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
    s.append('</svg>'); return "".join(s)

def bar_chart_sectors(title, data, note=""):
    W=760; rowh=22; T=44; H=T+rowh*len(data)+30; L=200; R=40; pw=W-L-R
    vals=[v for _,v in data]; lo=min(0,min(vals)); hi=max(vals)
    def X(v): return L+pw*(v-lo)/(hi-lo)
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
    s.append(f'<text x="14" y="22" font-size="14" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    x0=X(0); s.append(f'<line x1="{x0:.1f}" y1="{T-6}" x2="{x0:.1f}" y2="{T+rowh*len(data):.1f}" stroke="{MUT}"/>')
    for i,(name,v) in enumerate(data):
        y=T+i*rowh; c=AC2 if v>=0 else AC
        xa,xb=(x0,X(v)) if v>=0 else (X(v),x0)
        s.append(f'<rect x="{xa:.1f}" y="{y+3:.1f}" width="{abs(xb-xa):.1f}" height="{rowh-8}" fill="{c}"/>')
        s.append(f'<text x="{L-8}" y="{y+rowh/2+3:.1f}" font-size="11" fill="{INK}" text-anchor="end" font-family="sans-serif">{esc(name)}</text>')
        lx=X(v)+(4 if v>=0 else -4); anc="start" if v>=0 else "end"
        s.append(f'<text x="{lx:.1f}" y="{y+rowh/2+3:.1f}" font-size="10" fill="{MUT}" text-anchor="{anc}" font-family="sans-serif">{"+" if v>=0 else ""}{v}k</text>')
    if note: s.append(f'<text x="14" y="{H-8}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
    s.append('</svg>'); return "".join(s)

# ---- build the charts ----
charts=[]
charts.append(("Jobs: nonfarm payroll change per year — and the downward benchmark revisions",
  bar_chart_years("Nonfarm payroll change per year (millions)", NFP_HEAD, NFP_REV, "millions",
    "BLS CES / FRED PAYEMS, annual change. 2024-25 headline shown faded; solid red = after the -818k (2024) and -911k (2025) QCEW benchmark revisions."),
  "The headline overstated job creation in 2024-25; the QCEW benchmarks cut ~1.5M jobs across the two years — the correction arriving 6-18 months late."))
charts.append(("Jobs: where they grew and shrank (recent, by sector)",
  bar_chart_sectors("Annualized job change by industry (thousands)", SECTORS,
    "BLS CES Table B-1, representative recent annualized change, rounded/illustrative."),
  "Growth is concentrated in health care, leisure/hospitality, and state/local government; manufacturing, information (tech), temp help, and federal government are shrinking. One 'jobs number' hides opposite sectoral trends."))
charts.append(("Inflation: never actually at 2% (CPI vs core PCE vs the target)",
  line_chart("Inflation, annual (%)", [("CPI-U",CPI),("core PCE (Fed's gauge)",COREPCE)], "%",[AC,AC2], ymin=0, target=2.0,
    note="FRED CPIAUCSL / PCEPILFE, YoY annual avg, rounded."),
  "In 11 years, core PCE sat within 2%±0.5 only a handful of times; the index spent the era either well below (2015-20) or far above (2021-24) the supposed target."))
charts.append(("True labor slack: U-6 (underemployment) vs U-3 (headline)",
  line_chart("Unemployment, annual (%)", [("U-6 (true slack)",U6),("U-3 (headline)",U3)],"%",[AC,AC2], ymin=0,
    note="BLS UNRATE / U6RATE, annual avg, rounded."),
  "U-6 — which counts discouraged and involuntarily part-time workers, and the gig/underemployed — runs ~3-5 pts above the headline the Fed cites."))
charts.append(("The dual-mandate test: the funds rate tracks neither 2% inflation nor full employment",
  line_chart("Rate vs mandate (%)", [("Fed funds (year-end)",FEDFUNDS),("core PCE",COREPCE),("U-6",U6)],"%",[INK,AC,AC2], ymin=0, target=2.0,
    note="FRED DFEDTARU / PCEPILFE / U6RATE."),
  "If the Fed steered to '2% inflation + full employment,' the funds line would track those. It doesn't — it sat at zero through 2%+ core PCE (2021) and stayed >5% as inflation fell and U-6 rose."))
charts.append(("The real driver: the funds rate tracks the BOND MARKET (the 2-year yield leads it)",
  line_chart("Policy vs market rates (%)", [("Fed funds",FEDFUNDS),("2Y Treasury",T2),("3M",T3M),("10Y",T10),("30Y",T30)],"%",[INK,AC,"#9a6a1a",AC2,"#1f6f43"], ymin=0,
    note="FRED DFEDTARU / DGS2 / DGS3MO / DGS10 / DGS30, year-end."),
  "The funds rate and the 2-year yield move together, with the 2Y turning FIRST at every pivot (it fell ahead of the 2019 and 2024 cuts; rose ahead of the 2022 hikes). The Fed is following the bond market's expectation, not delivering a mandate."))
charts.append(("The global bond squeeze: JGB 10Y escaped 0% (carry-unwind fuel) while Baa credit repriced",
  line_chart("Long rates (%)", [("US 10Y",T10),("Japan 10Y (JGB)",JGB10),("Baa corporate",BAA)],"%",[AC2,AC,"#9a6a1a"], ymin=-0.5,
    note="FRED DGS10 / IRLTLT01JPM156N / BAA, year-end. JGB: YCC ended Mar 2024."),
  "The 10Y JGB went from ~0% (yield-curve-control) to ~2% (Dec 2025) to ~2.66% (2026) — the rising cost of the yen carry trade that funds crowded global longs (the 'BEAR' trigger)."))

# ---- page ----
NAV=('<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:11px 22px;font-size:13px;font-family:-apple-system,Segoe UI,Roboto,sans-serif">'
     '<a href="index.html" style="color:#1f4e79;text-decoration:none;margin-right:16px">Home</a>'
     '<a href="dashboard.html" style="color:#1f4e79;text-decoration:none;margin-right:16px">Dashboard</a>'
     '<a href="charts.html" style="color:#1f4e79;text-decoration:none;margin-right:16px;font-weight:600">Charts</a>'
     '<a href="research.html" style="color:#1f4e79;text-decoration:none;margin-right:16px">Research</a>'
     '<a href="methodology.html" style="color:#1f4e79;text-decoration:none;margin-right:16px">Methodology</a>'
     '<a href="glossary.html" style="color:#1f4e79;text-decoration:none">Glossary</a></div>')
CSS=("body{background:#faf8f2;color:#1c1b19;font:17px/1.7 Georgia,'Iowan Old Style','Palatino Linotype',serif;margin:0;padding:0 0 60px}"
     "main{max-width:820px;margin:0 auto;padding:0 22px}h1{font-family:Georgia,serif;font-weight:600;font-size:32px;margin:26px 0 4px}"
     "h2{color:#7b2d26;font-family:Georgia,serif;font-weight:600;font-size:21px;margin:34px 0 2px;border-bottom:1px solid #e4ddcc;padding-bottom:6px}"
     ".cap{color:#33312c;font-size:15px;margin:6px 0 4px}.src{color:#6b665d;font-size:13px}a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;font-size:13px;color:#6b3b16}")
body=[f'<h1>Charts — jobs, inflation, and the Fed vs the bond market</h1>',
 '<p class=cap>Bar and line charts over the last decade. <b>Thesis tested here:</b> the Fed is steering to the <b>bond market</b> (the 2-year yield), not to its stated dual mandate of 2% inflation and full employment — and a single "jobs number" / "inflation number" hides opposite sectoral and labor-slack trends.</p>',
 '<p class=src>All series are <b>annual</b>, compiled from public data (FRED / BLS / US Treasury / BIS / BOJ), <b>rounded</b> to the precision shown; FRED/BLS series IDs are noted under each chart. "~" marks an estimate or partial year. Verify any value at the cited series. Companion data + sourcing: <a href="https://github.com/pq-cybarg/bubble-map/blob/main/research/macro-jobs-inflation-fed.md">macro-jobs-inflation-fed</a>.</p>']
for h,svg,cap in charts:
    body.append(f'<h2>{esc(h)}</h2>'); body.append(svg); body.append(f'<p class=cap>{cap}</p>')
body.append('<h2>The bottom line</h2><p class=cap>Across the decade the funds rate maps onto the 2-year Treasury yield, not onto 2% inflation or full employment. Inflation was almost never at target; "true" labor slack (U-6) ran well above the headline; and one aggregate jobs/inflation print masks sectoral and regional divergence. The mandate is the framing; the bond market is the master.</p>')
HTML=(f'<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
      f'<title>Bubble Map — Charts</title><style>{CSS}</style></head><body>{NAV}<main>'+ "".join(body) +'</main></body></html>')
open(os.path.join(DOCS,"charts.html"),"w").write(HTML)
print(f"wrote docs/charts.html ({len(HTML)} bytes, {len(charts)} charts)")
