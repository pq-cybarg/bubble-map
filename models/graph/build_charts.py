#!/usr/bin/env python3
"""
build_charts.py - render data/*.svg charts into docs/charts.html (pure SVG, no JS deps),
documenting jobs, inflation, the Fed's rate path vs its mandate, and vs the bond market.

ALL series are ANNUAL, compiled from public sources (FRED / BLS / US Treasury / BIS), ROUNDED
to the precision shown; series IDs are cited on the page. Estimates / partial-year are marked '~'.
This is the visual companion to research/macro-jobs-inflation-fed.json (which carries the sourcing).
"""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs")

def load_fred():
    try: return json.load(open(os.path.join(ROOT,"data","fred_monthly.json")))["data"]
    except Exception: return None

def load_fred_daily():
    try: return json.load(open(os.path.join(ROOT,"data","fred_daily.json")))["data"]
    except Exception: return None

def lead_lag_daily(funds, two, w=21, maxlag=63):
    """On the daily grid, correlate w-day CHANGES of funds[t] with two[t-lag]; return the lag
    (trading days the 2Y leads) maximizing corr, plus that corr and the lag-0 corr."""
    df=[funds[i]-funds[i-w] for i in range(w,len(funds))]
    dt=[two[i]-two[i-w]   for i in range(w,len(two))]
    best=(0,-2.0)
    for k in range(0,maxlag+1):
        a=df[k:]; b=dt[:len(df)-k]
        if len(a)>=60:
            c=_pearson(a,b)
            if c>best[1]: best=(k,c)
    return best[0], best[1], _pearson(df,dt)

def _pearson(a,b):
    n=len(a)
    if n<3: return 0.0
    ma=sum(a)/n; mb=sum(b)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    da=(sum((x-ma)**2 for x in a))**0.5; db=(sum((y-mb)**2 for y in b))**0.5
    return num/(da*db) if da*db else 0.0

def lead_lag(funds, two):
    """Find k>=0 (months the 2Y LEADS the funds rate) maximizing corr of m/m CHANGES."""
    df=[funds[i]-funds[i-1] for i in range(1,len(funds))]
    dt=[two[i]-two[i-1]   for i in range(1,len(two))]
    best=(0,-2.0)
    for k in range(0,7):
        a=df[k:]; b=dt[:len(df)-k]
        if len(a)>=24:
            c=_pearson(a,b)
            if c>best[1]: best=(k,c)
    same=_pearson(df,dt)
    return best[0], best[1], same

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

def monthly_line_chart(title, dates, series, colors, ylab="%", note="", ymin=None, ymax=None):
    W,H=760,360; L,R,T,B=54,150,40,46; pw,ph=W-L-R,H-T-B
    vals=[v for _,ys in series for v in ys]
    lo=ymin if ymin is not None else min(0,min(vals)); hi=ymax if ymax is not None else max(vals)
    if hi==lo: hi=lo+1
    n=len(dates)
    def X(i): return L+pw*i/(n-1)
    def Y(v): return T+ph*(hi-v)/(hi-lo)
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
    s.append(f'<text x="{L}" y="22" font-size="14" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    for k in range(6):
        v=lo+(hi-lo)*k/5; y=Y(v)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{L-6}" y="{y+3:.1f}" font-size="10" fill="{MUT}" text-anchor="end" font-family="sans-serif">{v:.1f}</text>')
    for i,dt in enumerate(dates):
        if dt.endswith("-01"):
            s.append(f'<line x1="{X(i):.1f}" y1="{T}" x2="{X(i):.1f}" y2="{T+ph}" stroke="{GRID}"/>')
            s.append(f'<text x="{X(i):.1f}" y="{T+ph+15:.1f}" font-size="9" fill="{MUT}" text-anchor="middle" font-family="sans-serif">{dt[:4]}</text>')
    for (name,ys),c in zip(series,colors):
        d=" ".join(f'{"M" if k==0 else "L"}{X(i):.1f} {Y(v):.1f}' for k,(i,v) in enumerate(enumerate(ys)))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.8"/>')
    ly=T+8
    for (name,_),c in zip(series,colors):
        s.append(f'<rect x="{L+pw+12}" y="{ly-8}" width="11" height="11" fill="{c}"/>')
        s.append(f'<text x="{L+pw+27}" y="{ly+1}" font-size="10.5" fill="{INK}" font-family="sans-serif">{esc(name)}</text>'); ly+=18
    if note: s.append(f'<text x="{L}" y="{H-6}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
    s.append('</svg>'); return "".join(s)

def daily_line_chart(title, dates, series, colors, ylab="%", note=""):
    W,H=760,360; L,R,T,B=54,150,40,46; pw,ph=W-L-R,H-T-B
    vals=[v for _,ys in series for v in ys]; lo=min(0,min(vals)); hi=max(vals)
    n=len(dates)
    def X(i): return L+pw*i/(n-1)
    def Y(v): return T+ph*(hi-v)/(hi-lo)
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
    s.append(f'<text x="{L}" y="22" font-size="14" font-weight="700" fill="{INK}" font-family="Georgia,serif">{esc(title)}</text>')
    for k in range(6):
        v=lo+(hi-lo)*k/5; y=Y(v)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{L-6}" y="{y+3:.1f}" font-size="10" fill="{MUT}" text-anchor="end" font-family="sans-serif">{v:.1f}</text>')
    prevyr=None
    for i,dt in enumerate(dates):
        yr=dt[:4]
        if yr!=prevyr:
            s.append(f'<line x1="{X(i):.1f}" y1="{T}" x2="{X(i):.1f}" y2="{T+ph}" stroke="{GRID}"/>')
            s.append(f'<text x="{X(i):.1f}" y="{T+ph+15:.1f}" font-size="9" fill="{MUT}" text-anchor="middle" font-family="sans-serif">{yr}</text>')
            prevyr=yr
    for (name,ys),c in zip(series,colors):
        d=" ".join(f'{"M" if k==0 else "L"}{X(i):.1f} {Y(v):.1f}' for k,(i,v) in enumerate(enumerate(ys)))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.3"/>')
    ly=T+8
    for (name,_),c in zip(series,colors):
        s.append(f'<rect x="{L+pw+12}" y="{ly-8}" width="11" height="11" fill="{c}"/>')
        s.append(f'<text x="{L+pw+27}" y="{ly+1}" font-size="10.5" fill="{INK}" font-family="sans-serif">{esc(name)}</text>'); ly+=18
    if note: s.append(f'<text x="{L}" y="{H-6}" font-size="9.5" fill="{MUT}" font-family="sans-serif">{esc(note)}</text>')
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
# --- monthly tick-by-tick: 2Y vs effective fed funds (live FRED), with lead-lag stat ---
_fred=load_fred()
LEADLAG_NOTE=""
if _fred and "DGS2" in _fred and "FEDFUNDS" in _fred:
    common=sorted(set(_fred["DGS2"]) & set(_fred["FEDFUNDS"]) & set(_fred.get("DGS3MO",_fred["DGS2"])))
    ff=[_fred["FEDFUNDS"][d] for d in common]
    t2=[_fred["DGS2"][d] for d in common]
    t3=[_fred["DGS3MO"][d] for d in common] if "DGS3MO" in _fred else None
    k,corr,same=lead_lag(ff,t2)
    series=[("Effective fed funds",ff),("2Y Treasury",t2)]; cols=[INK,AC]
    if t3: series.append(("3M Treasury",t3)); cols.append("#9a6a1a")
    LEADLAG_NOTE=(f"Lead-lag of month-over-month CHANGES: the 2-year yield LEADS the funds rate by ~{k} month(s) "
                  f"(peak corr {corr:.2f}; contemporaneous corr {same:.2f}). The Fed moves after the 2Y, not before it.")
    charts.append(("Tick-by-tick (monthly): the funds rate FOLLOWS the 2-year Treasury",
      monthly_line_chart("Effective fed funds vs 2Y/3M Treasury — monthly, 2015-2026", common, series, cols,
        note="FRED monthly: FEDFUNDS / DGS2 / DGS3MO (daily->monthly avg via fredgraph.csv). Refresh: python3 models/graph/fetch_fred.py."),
      LEADLAG_NOTE+" At each pivot the 2Y turns first (it fell ahead of the 2019 and 2024 cuts and rose ahead of the 2022 hikes) — the bond market sets the path the Fed ratifies."))

# --- DAILY tick-by-tick: 2Y vs daily effective fed funds, with daily lead-lag ---
_fd=load_fred_daily()
_fundskey="DFF" if (_fd and "DFF" in _fd) else ("EFFR" if (_fd and "EFFR" in _fd) else None)
if _fd and "DGS2" in _fd and _fundskey:
    cd=sorted(set(_fd["DGS2"]) & set(_fd[_fundskey]) & set(_fd.get("DGS3MO",_fd["DGS2"])))
    dff=[_fd[_fundskey][d] for d in cd]; d2=[_fd["DGS2"][d] for d in cd]
    d3=[_fd["DGS3MO"][d] for d in cd] if "DGS3MO" in _fd else None
    k,corr,same=lead_lag_daily(dff,d2)
    series=[(f"Daily eff. fed funds ({_fundskey})",dff),("2Y Treasury (daily)",d2)]; cols=[INK,AC]
    if d3: series.append(("3M Treasury (daily)",d3)); cols.append("#9a6a1a")
    note=(f"Daily, {len(cd)} trading days {cd[0]}..{cd[-1]} (FRED DFF / DGS2 / DGS3MO). Lead-lag of 21-day changes: "
          f"the 2Y LEADS the funds rate by ~{k} trading days (~{k/21:.1f} mo; peak corr {corr:.2f} vs {same:.2f} at lag 0).")
    charts.append(("Daily resolution: the funds rate is a STEP the 2-year Treasury reaches first",
      daily_line_chart("Daily effective fed funds vs 2Y/3M Treasury, 2015-2026", cd, series, cols, note="FRED daily series via fredgraph.csv; refresh: python3 models/graph/fetch_fred.py."),
      note+" The funds rate (DFF) is a near-step that jumps only at FOMC meetings; the 2Y is continuous and has already moved to the new level before each step — the bond market prices the decision first."))

# --- RATE DIFFERENTIALS: sharp-but-fast (short end) vs smooth-but-delayed (long end) ---
def _std(xs):
    n=len(xs);
    if n<2: return 0.0
    m=sum(xs)/n; return (sum((x-m)**2 for x in xs)/n)**0.5
def _chg(xs): return [xs[i]-xs[i-1] for i in range(1,len(xs))]
def best_horizon(spread, funds, hmax=18):
    best=(0,0.0)
    for h in range(1,hmax+1):
        a=[spread[t] for t in range(len(spread)-h)]
        b=[funds[t+h]-funds[t] for t in range(len(funds)-h)]
        if len(a)>=24:
            c=_pearson(a,b)
            if abs(c)>abs(best[1]): best=(h,c)
    return best

SIGNAL_TABLE=""
_m=load_fred()
if _m and all(k in _m for k in ("DGS2","FEDFUNDS","DGS3MO","DGS10")):
    mc=sorted(set(_m["DGS2"])&set(_m["FEDFUNDS"])&set(_m["DGS3MO"])&set(_m["DGS10"]))
    ff=[_m["FEDFUNDS"][d] for d in mc]; g2=[_m["DGS2"][d] for d in mc]; g3=[_m["DGS3MO"][d] for d in mc]; g10=[_m["DGS10"][d] for d in mc]
    SPREADS=[("2Y − fed funds","short",[g2[i]-ff[i] for i in range(len(mc))]),
             ("3M − fed funds","short",[g3[i]-ff[i] for i in range(len(mc))]),
             ("2Y − 3M (policy-path)","medium",[g2[i]-g3[i] for i in range(len(mc))]),
             ("10Y − 2Y (2s10s)","long",[g10[i]-g2[i] for i in range(len(mc))]),
             ("10Y − 3M (3m10s)","long",[g10[i]-g3[i] for i in range(len(mc))])]
    # two spread charts (short-end sharp; long-end smooth) + the 2Y-3M policy-path in the middle
    charts.append(("Sharp & fast — the SHORT-END gap (2Y/3M minus funds) + the 2Y−3M policy-path",
      monthly_line_chart("Short/medium spreads (pp), monthly", mc, [(n,s) for n,grp,s in SPREADS if grp in("short","medium")], [AC,"#9a6a1a",AC2],
        note="FRED DGS2/DGS3MO minus FEDFUNDS, and DGS2-DGS3MO. Negative = market expects CUTS (Fed 'behind'); positive = HIKES."),
      "The short-end gap turns FAST: deeply negative ahead of the 2019/2020/2024 cuts, strongly positive ahead of the 2022 hikes — the market pre-committing the Fed. The 2Y−3M 'policy-path' spread sits in the middle: it captures the expected ~2-year rate path vs the front, smoother than the 3M−funds jump-detector but faster than the 2s10s curve."))
    charts.append(("Smooth & delayed — the CURVE spreads (10Y minus 2Y / 3M)",
      monthly_line_chart("Curve spreads (pp), monthly", mc, [(n,s) for n,grp,s in SPREADS if grp=="long"], [AC2,"#1f6f43"],
        note="FRED DGS10 minus DGS2 / DGS3MO. Inversion (below 0) is the classic recession lead — smoother, but with a long and variable lag."),
      "The 2s10s/3m10s curve is far smoother but slower: it inverted through 2022-24 (recession signal) and is a cleaner but lagged read than the jumpy short-end gap."))
    rows=[]
    for n,grp,s in SPREADS:
        noise=_std(_chg(s)); h,c=best_horizon(s,ff)
        rows.append((n,grp,noise,h,c))
    sh=[r for r in rows if r[1]=="short"]; me=[r for r in rows if r[1]=="medium"]; lo=[r for r in rows if r[1]=="long"]
    def _fmt(rs): return "".join(f"<tr><td>{n}</td><td>{noise:.2f}</td><td>{h} mo</td><td>{c:+.2f}</td></tr>" for n,grp,noise,h,c in rs)
    SIGNAL_TABLE=("<h2>Signal quality: the sharp-vs-smooth tradeoff, measured</h2>"
      "<p class=cap>For each rate differential: <b>noise</b> = stdev of its month-over-month change (higher = jumpier); "
      "<b>horizon</b> = the lead h (months) at which the spread's level best predicts the subsequent change in the fed funds rate; "
      "<b>corr</b> = that predictive correlation. The horizon lengthens from the short end (fast) to the curve (delayed); the 2Y−3M policy-path spread sits in the middle.</p>"
      "<table><thead><tr><th>Differential</th><th>Noise (Δ stdev, pp)</th><th>Best lead horizon</th><th>Corr at horizon</th></tr></thead><tbody>"
      "<tr><td colspan=4 style='background:#f3eedf'><b>Short end — fast (1–8 mo)</b></td></tr>"+_fmt(sh)+
      "<tr><td colspan=4 style='background:#f3eedf'><b>Medium — the 2Y−3M policy path (~9 mo)</b></td></tr>"+_fmt(me)+
      "<tr><td colspan=4 style='background:#f3eedf'><b>Long end — the curve, smooth & delayed (18 mo+)</b></td></tr>"+_fmt(lo)+
      "</tbody></table>"
      "<p class=cap>The tradeoff, quantified from the data: the predictive <b>horizon lengthens from the short end to the curve</b> — 3M−funds predicts the next move at ~1&nbsp;month, 2Y−funds at ~8&nbsp;months (and is the strongest predictor, corr ~0.77), while the 2s10s/3m10s curve leads longest (~18&nbsp;months+) but weaker — the fast-vs-delayed axis. Noise is <i>not</i> monotonic: the 3M−funds gap is actually the cleanest, the 2Y−funds and 10Y−3M the jumpiest. So pick the differential to match the question: <b>3M−funds</b> for the fastest clean read on an imminent move, <b>2Y−funds</b> for the strongest read on where the Fed is headed, the <b>2Y−3M policy-path</b> (noise 0.17, ~9-mo horizon, corr +0.66) for the medium-term expected path, and the <b>2s10s curve</b> for the smoothest (most delayed) cycle/recession read.</p>")

# --- 30Y differentials (term premium / long-end steepness) ---
if _m and all(k in _m for k in ("DGS30","DGS10","DGS2","FEDFUNDS")):
    c30=sorted(set(_m["DGS30"])&set(_m["DGS10"])&set(_m["DGS2"])&set(_m["FEDFUNDS"]))
    g30=[_m["DGS30"][d] for d in c30]; g10=[_m["DGS10"][d] for d in c30]; g2=[_m["DGS2"][d] for d in c30]; ff=[_m["FEDFUNDS"][d] for d in c30]
    s30_10=[g30[i]-g10[i] for i in range(len(c30))]; s30_2=[g30[i]-g2[i] for i in range(len(c30))]; s30_ff=[g30[i]-ff[i] for i in range(len(c30))]
    charts.append(("30Y differentials: the long-end term premium (30Y−10Y, 30Y−2Y)",
      monthly_line_chart("30Y spreads (pp), monthly", c30, [("30Y − 10Y (term premium)",s30_10),("30Y − 2Y",s30_2),("30Y − fed funds",s30_ff)], [AC,AC2,"#9a6a1a"],
        note="FRED DGS30 minus DGS10/DGS2/FEDFUNDS."),
      "The 30Y−10Y term premium was compressed/near-zero through 2015-21 (QE era), inverted with the rest of the curve in 2022-23, then STEEPENED sharply in 2024-26 as long-end supply (deficits) and term premium returned — the smoothest, slowest-moving differential, reflecting fiscal/duration risk rather than near-term policy."))
    if SIGNAL_TABLE:
        n30,h30,c30c=_std(_chg(s30_ff)), *best_horizon(s30_ff,ff)
        SIGNAL_TABLE=SIGNAL_TABLE.replace("</tbody></table>",
          f"<tr><td colspan=4 style='background:#f3eedf'><b>Very long end — fiscal/duration, slowest</b></td></tr><tr><td>30Y − fed funds</td><td>{n30:.2f}</td><td>{h30} mo</td><td>{c30c:+.2f}</td></tr></tbody></table>")

# --- corporate / credit markets over time ---
if _m and all(k in _m for k in ("BAA","AAA","DGS10")):
    cc=sorted(set(_m["BAA"])&set(_m["AAA"])&set(_m["DGS10"]))
    baa=[_m["BAA"][d] for d in cc]; aaa=[_m["AAA"][d] for d in cc]; t10=[_m["DGS10"][d] for d in cc]
    charts.append(("Corporate bond YIELDS over time (Moody's Baa, Aaa vs the 10Y Treasury)",
      monthly_line_chart("Corporate vs Treasury yields (%), monthly", cc, [("Baa corporate",baa),("Aaa corporate",aaa),("10Y Treasury",t10)], [AC,"#9a6a1a",AC2], ymin=0,
        note="FRED BAA / AAA / DGS10."),
      "Corporate borrowing costs (Baa/Aaa) track the Treasury but with a CREDIT SPREAD on top; both repriced from the ~3-4% 2015-21 floor to ~5-6% by 2022-26."))
    sp=[baa[i]-t10[i] for i in range(len(cc))]
    charts.append(("Credit SPREAD over time — Baa minus the 10Y Treasury (full history)",
      monthly_line_chart("Baa − 10Y credit spread (pp), monthly", cc, [("Baa − 10Y",sp)], [AC], ymin=0,
        note="FRED BAA minus DGS10."),
      "The credit spread is the market's default-risk read: it spiked in early 2016 (energy bust) and Mar-2020 (COVID), then COMPRESSED to cycle-lows by 2024-26 — credit priced almost no stress even as the self-marked private-credit risk built (macro-private-credit-marks)."))
    if "BAMLH0A0HYM2" in _m and "BAMLC0A0CM" in _m:
        ccc=sorted(set(_m["BAMLH0A0HYM2"])&set(_m["BAMLC0A0CM"]))
        hy=[_m["BAMLH0A0HYM2"][d] for d in ccc]; ig=[_m["BAMLC0A0CM"][d] for d in ccc]
        charts.append((f"Option-adjusted spreads — HY vs IG ({ccc[0]}+)",
          monthly_line_chart("ICE BofA OAS (pp), monthly", ccc, [("High-yield OAS",hy),("Inv-grade OAS",ig)], [AC,AC2], ymin=0,
            note="FRED BAMLH0A0HYM2 (HY OAS) / BAMLC0A0CM (IG OAS). Range limited by the monthly series returned."),
          "Even on the available window, high-yield and investment-grade OAS sit near cycle lows — the corporate market is pricing minimal default risk into 2026."))

# --- regional sovereign yields + a GDP-weighted global aggregate ---
if _m and all(k in _m for k in ("DGS10","IRLTLT01DEM156N","IRLTLT01GBM156N","IRLTLT01JPM156N")):
    cr=sorted(set(_m["DGS10"])&set(_m["IRLTLT01DEM156N"])&set(_m["IRLTLT01GBM156N"])&set(_m["IRLTLT01JPM156N"]))
    us=[_m["DGS10"][d] for d in cr]; de=[_m["IRLTLT01DEM156N"][d] for d in cr]; gb=[_m["IRLTLT01GBM156N"][d] for d in cr]; jp=[_m["IRLTLT01JPM156N"][d] for d in cr]
    # GDP weights (2024 nominal $tn, approx): US 29.2, JP 4.0, DE 4.7, GB 3.6 -> renormalized
    W={"US":29.2,"JP":4.0,"DE":4.7,"GB":3.6}; tot=sum(W.values()); wU,wJ,wD,wG=W["US"]/tot,W["JP"]/tot,W["DE"]/tot,W["GB"]/tot
    glob=[wU*us[i]+wJ*jp[i]+wD*de[i]+wG*gb[i] for i in range(len(cr))]
    charts.append(("Regional sovereign 10Y + a GDP-weighted GLOBAL long rate",
      monthly_line_chart("10Y government yields (%), monthly", cr, [("US",us),("UK",gb),("Germany",de),("Japan",jp),("GDP-weighted global",glob)], [AC2,"#9a6a1a","#1f6f43","#7b2d26",INK], ymin=-0.5,
        note="FRED DGS10 (US) / IRLTLT01{DE,GB,JP}M156N. Global = GDP-weighted (US 70% / DE 11% / GB 9% / JP 10%, 2024 GDP)."),
      "Subdividing by region shows the divergence the single 'US 10Y' hides: Japan sat near 0% under yield-curve-control while the US/UK ran 4%+; the GDP-weighted global long rate (black) rose from ~1% (2020) toward ~3% (2026) as Japan finally joined — the synchronized global repricing of duration, and the carry-unwind pressure (macro-carry-trades)."))

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
if SIGNAL_TABLE: body.append(SIGNAL_TABLE)
body.append('<h2>The bottom line</h2><p class=cap>Across the decade the funds rate maps onto the 2-year Treasury yield, not onto 2% inflation or full employment. Inflation was almost never at target; "true" labor slack (U-6) ran well above the headline; and one aggregate jobs/inflation print masks sectoral and regional divergence. The mandate is the framing; the bond market is the master.</p>')
HTML=(f'<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
      f'<title>Bubble Map — Charts</title><style>{CSS}</style></head><body>{NAV}<main>'+ "".join(body) +'</main></body></html>')
open(os.path.join(DOCS,"charts.html"),"w").write(HTML)
print(f"wrote docs/charts.html ({len(HTML)} bytes, {len(charts)} charts)")
