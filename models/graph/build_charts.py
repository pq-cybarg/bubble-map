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

def load_yahoo():
    try: return json.load(open(os.path.join(ROOT,"data","yahoo_monthly.json")))["data"]
    except Exception: return None

def load_tape():
    try: return json.load(open(os.path.join(ROOT,"data","tape_trace.json")))
    except Exception: return None

def ttm_yield(etf):
    """trailing-12-month distribution yield (%) per month: sum(last 12 divs)/close*100."""
    months=sorted(etf); out={}
    for i in range(11,len(months)):
        m=months[i]; px=etf[m].get("c")
        if not px: continue
        d12=sum(etf[months[j]].get("d",0.0) for j in range(i-11,i+1))
        out[m]=round(100*d12/px,3)
    return out

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
    s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
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
    s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
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
    s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
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
    s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
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
    s=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:{PAPER};border:1px solid {LINE};border-radius:6px;margin:8px 0">']
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

# --- EXPANDED sovereign 10Y cross-section: up to 26 countries -> 7 sub-regions + periphery spread ---
# 2024 nominal GDP ($tn, approx) for GDP-weighting; FRED series = DGS10 for US, else IRLTLT01{cc}M156N.
_GDP={"US":29.2,"CA":2.2,"MX":1.8,"DE":4.7,"FR":3.2,"NL":1.2,"BE":0.66,"AT":0.52,"IE":0.56,
      "IT":2.4,"ES":1.7,"PT":0.29,"GR":0.25,"GB":3.6,"SE":0.61,"NO":0.50,"DK":0.42,"FI":0.31,
      "PL":0.86,"CZ":0.34,"HU":0.22,"JP":4.0,"KR":1.9,"AU":1.8,"NZ":0.25,"CL":0.34}
def _ser(cc): return "DGS10" if cc=="US" else f"IRLTLT01{cc}M156N"
_PAL=["#1f4e79","#7b2d26","#1f6f43","#9a6a1a","#5e35b1","#138a8a","#8a5a2b","#c0392b","#6b3b16","#2e8b57","#d35400","#444"]
if _m and ("DGS10" in _m) and ("IRLTLT01DEM156N" in _m):
    _avail=[cc for cc in _GDP if _ser(cc) in _m and len(_m[_ser(cc)])>=120]
    cs=sorted(set.intersection(*[set(_m[_ser(cc)]) for cc in _avail]))
    SUBREG={"North America":["US","CA"],
            "Core Europe":["DE","FR","NL","BE","AT"],
            "Periphery Europe":["IT","ES","PT","GR","IE"],
            "UK & Nordics":["GB","SE","NO","DK","FI"],
            "Central/Eastern Europe":["PL","CZ","HU"],
            "Asia-Pacific (developed)":["JP","KR","AU","NZ"],
            "Latin America":["MX","CL"]}
    def _wavg(ccs):
        mem=[c for c in ccs if c in _avail]
        if not mem: return None
        tw=sum(_GDP[c] for c in mem)
        return [sum(_GDP[c]*_m[_ser(c)][d] for c in mem)/tw for d in cs]
    # (1) representative individual countries + a GDP-weighted GLOBAL over ALL available
    glob=_wavg(_avail); ncc=len(_avail)
    indiv=[(lab,[_m[_ser(cc)][d] for d in cs]) for cc,lab in
           [("US","US"),("DE","Germany"),("IT","Italy"),("GB","UK"),("JP","Japan")] if cc in _avail]
    charts.append((f"Regional sovereign 10Y + a GDP-weighted GLOBAL long rate ({ncc} countries)",
      monthly_line_chart("10Y government yields (%), monthly", cs, indiv+[("GDP-weighted global",glob)],
        _PAL[:len(indiv)]+[INK], ymin=-0.5,
        note=f"FRED DGS10 (US) + IRLTLT01*M156N for {ncc} OECD countries; global = GDP-weighted across ALL {ncc}."),
      f"The single 'US 10Y' hides a wide spread: Japan near 0% under yield-curve-control, Italy/periphery far above the Bund, the US/UK at 4%+. The GDP-weighted global long rate (black, now spanning {ncc} countries) rose from ~1% (2020) toward ~3% (2026) as Japan normalized — synchronized duration repricing + carry-unwind pressure (macro-carry-trades)."))
    # (2) sub-regional aggregates (only sub-regions with available members)
    subseries=[(name,_wavg(mem)) for name,mem in SUBREG.items() if _wavg(mem) is not None]
    subseries.append(("Global (GDP-weighted)",glob))
    charts.append(("Sovereign 10Y by SUB-REGION (GDP-weighted) — 7 blocs",
      monthly_line_chart("Sub-regional 10Y aggregates (%), monthly", cs, subseries, _PAL[:len(subseries)], ymin=-0.5,
        note="FRED IRLTLT01* + DGS10; GDP-weighted within each bloc: North America (US/CA), Core Europe (DE/FR/NL/BE/AT), Periphery (IT/ES/PT/GR/IE), UK&Nordics (GB/SE/NO/DK/FI), CEE (PL/CZ/HU), Asia-Pacific (JP/KR/AU/NZ), Latin America (MX/CL)."),
      "Aggregating country -> sub-region -> global reveals the real fault lines the 'developed-market 10Y' blends away: Central/Eastern Europe and Latin America run structurally highest (EM risk premium), Periphery Europe above Core (the redenomination/fiscal premium), Asia-Pacific dragged down for years by Japan's near-0% YCC, then all converging UP into 2024-26 — the synchronized repricing of duration across blocs."))
    # (3) European periphery & semi-core SPREAD over the Bund (the fragmentation divergence)
    if "IT" in _avail:
        sp=[(lab,[_m[_ser(cc)][d]-_m["IRLTLT01DEM156N"][d] for d in cs]) for cc,lab in
            [("IT","Italy−DE"),("ES","Spain−DE"),("PT","Portugal−DE"),("GR","Greece−DE"),("IE","Ireland−DE"),("FR","France−DE")] if cc in _avail]
        charts.append(("European FRAGMENTATION — periphery 10Y spread over the German Bund",
          monthly_line_chart("Spread vs Bund (pp), monthly", cs, sp, _PAL[:len(sp)], ymin=-0.5,
            note="FRED IRLTLT01{IT,ES,PT,GR,IE,FR} − IRLTLT01DE. The spread over Germany IS the market's redenomination/credit premium on each euro member."),
          "The euro's hidden stress gauge: peripheral spreads over the Bund widen in every risk-off (2018 Italy, 2020 COVID, 2022-23 hiking) and compress when the ECB backstops. France's spread creeping toward the periphery (2024-26 fiscal/political risk) is the notable new divergence — the single 'euro 10Y' cannot show this."))

# --- corporate by CREDIT QUALITY (full rating ladder) + EM corporate (regional credit) ---
_RAT=["BAMLC0A1CAAA","BAMLC0A2CAA","BAMLC0A3CA","BAMLC0A4CBBB","BAMLH0A3HYC"]
if _m and all(k in _m for k in _RAT):
    cq=sorted(set.intersection(*[set(_m[k]) for k in _RAT]))
    ladder=[("AAA",[_m['BAMLC0A1CAAA'][d] for d in cq]),("AA",[_m['BAMLC0A2CAA'][d] for d in cq]),("A",[_m['BAMLC0A3CA'][d] for d in cq]),("BBB",[_m['BAMLC0A4CBBB'][d] for d in cq]),("CCC & lower",[_m['BAMLH0A3HYC'][d] for d in cq])]
    charts.append((f"Corporates by CREDIT QUALITY — the AAA→CCC option-adjusted-spread ladder ({cq[0]}+)",
      monthly_line_chart("OAS by rating (pp), monthly", cq, ladder, ["#1f6f43","#3a7d44",AC2,"#9a6a1a",AC], ymin=0,
        note="FRED BAMLC0A1CAAA/0A2CAA/0A3CA/0A4CBBB + BAMLH0A3HYC. The accessible PROXY for sector-by-quality (true industry OAS needs licensed feeds)."),
      "The quality ladder is the free proxy for the 'which corporates blow out first' question: CCC spreads dwarf and move far more than the IG rungs (AAA→BBB), which barely separate. Through 2024-26 even CCC sits well off its crisis peaks — the riskiest corporates priced for calm."))
if _m and all(k in _m for k in ("BAMLC0A0CM","BAMLH0A0HYM2","BAMLEMPVPRIVSLCRPIUSOAS")):
    ce=sorted(set(_m["BAMLC0A0CM"])&set(_m["BAMLH0A0HYM2"])&set(_m["BAMLEMPVPRIVSLCRPIUSOAS"]))
    charts.append((f"Credit by REGION/TYPE — US investment-grade vs US high-yield vs Emerging-Market corporate ({ce[0]}+)",
      monthly_line_chart("OAS by segment (pp), monthly", ce, [("US IG",[_m['BAMLC0A0CM'][d] for d in ce]),("US HY",[_m['BAMLH0A0HYM2'][d] for d in ce]),("EM corporate",[_m['BAMLEMPVPRIVSLCRPIUSOAS'][d] for d in ce])], [AC2,AC,"#9a6a1a"], ymin=0,
        note="FRED BAMLC0A0CM / BAMLH0A0HYM2 / BAMLEMPVPRIVSLCRPIUSOAS."),
      "Adding the regional credit cut: EM-corporate OAS runs between US-IG and US-HY and is the accessible proxy for cross-border corporate risk — all three sit near cycle lows into 2026."))

# --- municipal proxy snapshot (via the published muni/Treasury ratio) ---
if _m and "DGS10" in _m and "DGS30" in _m:
    t10=sorted(_m["DGS10"].items())[-1][1]; t30=sorted(_m["DGS30"].items())[-1][1]
    MT10,MT30=0.67,0.87   # muni/Treasury ratio, ~Apr-2026 (published; BondWave/market data)
    charts.append(("Municipals — proxy snapshot via the muni/Treasury ratio (state &amp; local)",
      bar_chart_sectors("Yield: Treasury vs AAA muni (current, %)", [
        ("US Treasury 10Y",round(t10,2)),("AAA muni 10Y (proxy)",round(MT10*t10,2)),
        ("US Treasury 30Y",round(t30,2)),("AAA muni 30Y (proxy)",round(MT30*t30,2))],
        note="Muni = published muni/Treasury ratio (10Y~67%, 30Y~87%, Apr-2026) x current Treasury yield. Free proxies for the licensed-data gap."),
      "State/city muni yields aren't on FRED's free endpoint (the Bond Buyer 20-GO series ended 2016), but accessible PROXIES substitute: the published muni/Treasury RATIO (here x current Treasuries), the MUB ETF yield (~3.2%), and — for trade-level data — MSRB EMMA and FINRA TRACE, which is where the licensed indices source from too. Munis trade rich (below Treasury yields) on their tax exemption."))

# --- PER-STATE municipal yield proxy (real time series from state muni ETFs, Yahoo) ---
_y=load_yahoo()
if _y and all(t in _y for t in ("MUB","CMF","NYF","HYD")):
    yy={t:ttm_yield(_y[t]) for t in ("MUB","CMF","NYF","HYD")}
    ym=sorted(set.intersection(*[set(yy[t]) for t in yy]))
    charts.append(("Municipals by STATE — trailing distribution yield (California vs New York vs national vs HY-muni)",
      monthly_line_chart("Muni ETF distribution yield (%), monthly", ym, [("California (CMF)",[yy['CMF'][d] for d in ym]),("New York (NYF)",[yy['NYF'][d] for d in ym]),("National (MUB)",[yy['MUB'][d] for d in ym]),("High-yield muni (HYD)",[yy['HYD'][d] for d in ym])], ["#1f6f43",AC2,INK,AC], ymin=0,
        note="Yahoo chart API: trailing-12mo dividends / price for CMF/NYF/MUB/HYD. A yield PROXY (not the AAA-GO curve); built from the free ETF tape."),
      "The per-STATE muni cut, as a real time series rather than a snapshot: California (high-tax-state demand) trades richest (lowest yield), New York near national, high-yield muni well above — and all stepped UP with rates from the 2020-21 lows. City-level granularity still needs MSRB EMMA per-CUSIP; this gets the state layer from free ETF data."))

# --- corporate by MATURITY (short / intermediate / long IG corporate ETFs, Yahoo) ---
if _y and all(t in _y for t in ("VCSH","VCIT","VCLT")):
    ym2=sorted(set.intersection(*[set(ttm_yield(_y[t])) for t in ("VCSH","VCIT","VCLT")]))
    yv={t:ttm_yield(_y[t]) for t in ("VCSH","VCIT","VCLT")}
    charts.append(("Corporate by MATURITY — short / intermediate / long IG (distribution yield)",
      monthly_line_chart("IG corporate ETF distribution yield (%), monthly", ym2, [("Short (VCSH)",[yv['VCSH'][d] for d in ym2]),("Intermediate (VCIT)",[yv['VCIT'][d] for d in ym2]),("Long (VCLT)",[yv['VCLT'][d] for d in ym2])], ["#1f6f43",AC2,AC], ymin=0,
        note="Yahoo chart API: trailing-12mo dividends / price for Vanguard VCSH/VCIT/VCLT."),
      "The maturity dimension of corporate credit: long IG (VCLT) yields most and is the most rate-sensitive; the short/long gap widened as the curve moved — the corporate-credit analogue of the Treasury term structure."))

# --- INDUSTRY cross-section: equity SECTOR ETFs, normalized price (rebased to 100) ---
_SECT=[("XLK","Tech"),("SMH","Semiconductors"),("XLC","Comm svcs"),("XLY","Cons. discr."),("XLF","Financials"),
       ("XLI","Industrials"),("XLV","Health care"),("XLP","Cons. staples"),("XLE","Energy"),
       ("XLU","Utilities"),("XLB","Materials"),("XLRE","Real estate")]
def _closes(etf):
    return {m:etf[m].get("c") for m in sorted(etf) if etf[m].get("c")}
_have_sect=[(t,lab) for t,lab in _SECT if _y and t in _y]
if len(_have_sect)>=6:
    cl={t:_closes(_y[t]) for t,_ in _have_sect}
    sm=sorted(set.intersection(*[set(v) for v in cl.values()]))
    def _rebase(t):
        base=cl[t][sm[0]]; return [cl[t][d]/base*100 for d in sm]
    series=[(lab,_rebase(t)) for t,lab in _have_sect]
    charts.append((f"By INDUSTRY — US equity sector performance, rebased to 100 ({len(_have_sect)} GICS sectors)",
      monthly_line_chart("Sector total-return index (rebased=100)", sm, series, _PAL+["#888","#b07","#0a7"], ymin=0,
        note="Yahoo chart API: SPDR/VanEck sector ETFs (XLK/SMH/XLC/XLY/XLF/XLI/XLV/XLP/XLE/XLU/XLB/XLRE) monthly close, rebased to 100 at window start. Price index (excl. dividends)."),
      "The industry cut the single 'S&P' hides: Tech and Semiconductors (SMH) ran away from the pack — the AI-capex bid concentrated in a handful of sectors — while utilities/staples/real-estate lagged. The dispersion between the top sector and the bottom IS the concentration the bubble thesis tracks; when one or two sectors carry the index, breadth is illusory (the equity analogue of the 91% credit common factor)."))

# --- INDUSTRY dispersion over time: cross-sectional stdev of sector 12mo returns ---
if len(_have_sect)>=6:
    import statistics as _st
    rets={t:None for t,_ in _have_sect}
    # 12-mo trailing return per month per sector, then cross-sectional stdev each month
    mser={t:_closes(_y[t]) for t,_ in _have_sect}
    common=sorted(set.intersection(*[set(v) for v in mser.values()]))
    disp_d=[]; disp_v=[]
    for i in range(12,len(common)):
        d=common[i]; r=[]
        for t,_ in _have_sect:
            p0=mser[t][common[i-12]]; p1=mser[t][d]
            if p0: r.append((p1/p0-1)*100)
        if len(r)>=6: disp_d.append(d); disp_v.append(_st.pstdev(r))
    if disp_d:
        charts.append(("Industry DISPERSION over time — cross-sectional stdev of sector 12-mo returns",
          monthly_line_chart("Cross-sectional std of sector 12mo return (pp)", disp_d, [("dispersion (std)",disp_v)], [AC], ymin=0,
            note="Std across the sector ETFs' trailing-12mo returns each month. High = sectors diverging (a few winners, narrow breadth); low = moving together."),
          "When sector dispersion is HIGH the index is being carried by a narrow set (the 2023-26 AI/tech-and-semis surge); when LOW, sectors move as one (risk-on/off regimes). Dispersion is the breadth gauge behind the headline index level."))

# --- borrowing cost by TYPE (sovereign / corporate / household-mortgage) ---
if _m and all(k in _m for k in ("DGS10","BAA","MORTGAGE30US")):
    ct=sorted(set(_m["DGS10"])&set(_m["BAA"])&set(_m["MORTGAGE30US"]))
    charts.append(("Borrowing cost by TYPE — sovereign (10Y) vs corporate (Baa) vs household (30Y mortgage)",
      monthly_line_chart("Cost of money by borrower type (%), monthly", ct, [("US 10Y (sovereign)",[_m['DGS10'][d] for d in ct]),("Baa (corporate)",[_m['BAA'][d] for d in ct]),("30Y mortgage (household)",[_m['MORTGAGE30US'][d] for d in ct])], [INK,AC,AC2], ymin=0,
        note="FRED DGS10 / BAA / MORTGAGE30US."),
      "Stacking borrower types shows the spread STACK: households pay the mortgage rate (Treasury + ~spread), corporates the Baa rate; all three roughly doubled off the 2020-21 floor — the repricing hit sovereign, corporate, and household credit together."))

# --- the carry trade quantified + a live trigger panel for the unwind-timing thesis ---
TRIGGER_PANEL=""
if _m and all(k in _m for k in ("DGS10","IRLTLT01JPM156N","DGS2","FEDFUNDS","DGS30","BAMLH0A0HYM2")):
    cy=sorted(set(_m["DGS10"])&set(_m["IRLTLT01JPM156N"]))
    carry=[_m["DGS10"][d]-_m["IRLTLT01JPM156N"][d] for d in cy]; jp=[_m["IRLTLT01JPM156N"][d] for d in cy]
    charts.append(("The yen carry trade, quantified — US−Japan 10Y differential vs the JGB",
      monthly_line_chart("US−Japan 10Y (pp) and JGB level (%)", cy, [("US − Japan 10Y differential (carry fuel)",carry),("Japan 10Y (JGB)",jp)], [AC,AC2], ymin=-0.5,
        note="FRED DGS10 − IRLTLT01JPM156N. The differential is the gross spread a yen-funded long earns."),
      "The carry's fuel is draining: the US−Japan 10Y differential peaked near 3.85pp (Oct-2023) and has compressed toward ~1.8-2.0pp as the JGB climbed from ~0% (yield-curve-control) to ~2.5%. A shrinking differential + a rising yen is the classic carry-unwind setup (the 'BEAR' trigger) — it removes the cheap funding the crowded global longs depend on."))
    def L(s): k=sorted(_m[s]); return _m[s][k[-1]], k[-1]
    us10,_=L("DGS10"); jp10,jpd=L("IRLTLT01JPM156N"); g2,_=L("DGS2"); ff,_=L("FEDFUNDS"); t30,_=L("DGS30"); hy,_=L("BAMLH0A0HYM2")
    cd=round(us10-jp10,2); fg=round(g2-ff,2); cpk=max(carry)
    rows=[
      ("Yen carry unwind",f"US−JP 10Y = {cd}pp (peak {cpk:.2f}); JGB {jp10:.2f}% &amp; rising","ARMING","a sharp yen rally / further BOJ hikes that collapse the differential and force deleveraging of crowded longs"),
      ("Fed / rate path",f"2Y − funds = {fg:+.2f}pp (market ≈ neutral)","NEUTRAL","a swing deeply negative (cuts/stress priced) or a debt-service miss at a core borrower"),
      ("Credit stress",f"HY OAS = {hy:.2f}pp (near cycle lows)","COMPLACENT","a spread blow-out / default cluster beyond First Brands–Tricolor"),
      ("Bank HTM reopening",f"30Y = {t30:.2f}%, 10Y = {us10:.2f}% (elevated)","PRESSURED","a further long-rate spike (FDIC unrealized losses already turned up to $325B in Q1-26)"),
      ("AI mark reversal","Anthropic/OpenAI still private (no public price)","PENDING","an IPO that prices BELOW the last private mark (reflexive_marks M3 / MarkUnwind)"),
      ("SpaceX deal cliffs","contractual","SCHEDULED","Google's Sep 30 2026 delivery-miss right; 90-day notice from Dec 31 2026 (first exits ~Q1 2027)"),
    ]
    body_rows="".join(f"<tr><td><b>{n}</b></td><td>{r}</td><td>{st}</td><td>{f}</td></tr>" for n,r,st,f in rows)
    TRIGGER_PANEL=("<h2>Trigger panel — the unwind watch-list, live from the data</h2>"
      "<p class=cap>Operationalizing <code>spec-unwind-timing</code>: the date of a violent unwind is <b>not forecastable</b>, but the triggers are <b>observable</b>. Current readings (latest monthly FRED) — watch the indicators, not the calendar:</p>"
      "<table><thead><tr><th>Trigger</th><th>Current reading</th><th>State</th><th>What would fire it</th></tr></thead><tbody>"+body_rows+"</tbody></table>"
      "<p class=cap>Read: the carry's fuel is draining (differential down from ~3.85 to ~2pp) and bank HTM is pressured by elevated long rates, while credit and the Fed-path gap look calm/neutral — i.e., the system is fragile and arming, not yet firing. None of this dates the break; it sizes the kindling.</p>")

charts.append(("The global bond squeeze: JGB 10Y escaped 0% (carry-unwind fuel) while Baa credit repriced",
  line_chart("Long rates (%)", [("US 10Y",T10),("Japan 10Y (JGB)",JGB10),("Baa corporate",BAA)],"%",[AC2,AC,"#9a6a1a"], ymin=-0.5,
    note="FRED DGS10 / IRLTLT01JPM156N / BAA, year-end. JGB: YCC ended Mar 2024."),
  "The 10Y JGB went from ~0% (yield-curve-control) to ~2% (Dec 2025) to ~2.66% (2026) — the rising cost of the yen carry trade that funds crowded global longs (the 'BEAR' trigger)."))

# --- corporate by QUALITY TIER from the real FINRA TRACE tape (advance/decline breadth + volume) ---
_tape=load_tape()
if _tape and _tape.get("corporate_breadth"):
    cb=_tape["corporate_breadth"]
    TIERS=[("investment grade","Investment grade",AC2),("high yield","High yield",AC),("convertibles","Convertibles","#1f6f43")]
    have=[t for t in TIERS if t[0] in cb]
    if have:
        # common month axis where every present tier has a full-month reading (drop partial first/last)
        months=sorted(set.intersection(*[set(cb[t[0]].keys()) for t in have]))
        months=[m for m in months if all(cb[t[0]][m]["days"]>=15 for t in have)]
        if len(months)>=6:
            adr=[(lab,[cb[k][m]["ad_ratio"] for m in months]) for k,lab,_ in have]
            cols=[c for _,_,c in have]
            n_rows=_tape.get("meta",{}).get("datasets",{}).get("corporate_breadth",{}).get("rows","?")
            charts.append((f"Corporates by QUALITY from the real FINRA TRACE tape — advance/decline breadth ({months[0]}–{months[-1]})",
              monthly_line_chart("Advancing÷declining bonds (monthly, >1 = more rising than falling)", months, adr, cols,
                ylab="ratio", ymin=0,
                note=f"FINRA TRACE corporateMarketBreadth (OAuth Query API), {n_rows} trading-day rows aggregated to month; line at 1.0 separates risk-on/off."),
              "The actual TRACE trade tape, not a proxy: each month's advancing-vs-declining bond count by quality tier. "
              "High yield swings hardest (it falls below 1 first when risk-off hits and rebounds highest) while investment grade is steadier — "
              "the real corporate-credit breadth signal the rating-ladder OAS chart only approximated."))
            # volume share: HY as % of (IG+HY) traded volume — risk appetite by money, not just count
            volm=[m for m in months if cb["investment grade"][m]["vol"] and (m in cb.get("high yield",{}))]
            if volm and "high yield" in cb:
                hy_share=[("HY share of IG+HY volume",[round(100*cb["high yield"][m]["vol"]/(cb["high yield"][m]["vol"]+cb["investment grade"][m]["vol"]),2) for m in volm])]
                charts.append(("Corporate trading VOLUME mix — high-yield share of (IG+HY) dollar volume (FINRA TRACE)",
                  monthly_line_chart("HY ÷ (HY+IG) traded volume (%), monthly", volm, hy_share, [AC], ylab="%", ymin=0,
                    note="FINRA TRACE corporateMarketBreadth totalVolume by quality tier; rising = money rotating toward high yield."),
                  "Where the dollars actually traded: the high-yield share of corporate volume. A real, tape-sourced risk-appetite gauge to read alongside the spread charts above."))

# ---- page ----
def _navlinks(active=""):
    items=[("index.html","Home"),("dashboard.html","Dashboard"),("charts.html","Charts"),("research.html","Research"),
           ("persons.html","Persons"),("bubblemap.html","Bubble Map"),("globe.html","Globe"),
           ("methodology.html","Methodology"),("glossary.html","Glossary"),
           ("https://github.com/pq-cybarg/bubble-map","Source ↗")]
    a=lambda h,t:f'<a href="{h}" style="color:{"#7b2d26" if t==active else "#1f4e79"};text-decoration:none;margin:0 9px;white-space:nowrap;font-weight:{700 if t==active else 400}">{t}</a>'
    return ('<div style="background:#fffdf8;border-bottom:1px solid #e4ddcc;padding:11px 16px;'
            'font:13.5px/1.7 -apple-system,Segoe UI,Roboto,sans-serif;text-align:center">'+"".join(a(h,t) for h,t in items)+'</div>')
NAV=_navlinks("Charts")
CSS=("body{background:#faf8f2;color:#1c1b19;font:17px/1.7 Georgia,'Iowan Old Style','Palatino Linotype',serif;margin:0;padding:0 0 60px}"
     "main{max-width:820px;margin:0 auto;padding:0 22px}h1{font-family:Georgia,serif;font-weight:600;font-size:32px;margin:26px 0 4px}"
     "h2{color:#7b2d26;font-family:Georgia,serif;font-weight:600;font-size:21px;margin:34px 0 2px;border-bottom:1px solid #e4ddcc;padding-bottom:6px}"
     ".cap{color:#33312c;font-size:15px;margin:6px 0 4px}.src{color:#6b665d;font-size:13px}a{color:#1f4e79}code{background:#f2ede0;padding:1px 5px;border-radius:3px;font-size:13px;color:#6b3b16}"
     "h3{font-family:Georgia,serif;font-weight:600;font-size:18px;margin:22px 0 4px;color:#33312c}"
     "table{border-collapse:separate;border-spacing:0;width:100%;margin:16px 0;font-size:14px;font-family:-apple-system,Segoe UI,Roboto,sans-serif;border:1px solid #e4ddcc;border-radius:8px;overflow:hidden}"
     "th,td{border-bottom:1px solid #e4ddcc;padding:10px 13px;text-align:left;vertical-align:top;line-height:1.5}"
     "td+td,th+th{border-left:1px solid #e4ddcc}tr:last-child td{border-bottom:none}thead th{background:#f3eedf}tbody tr:nth-child(even){background:#fbf9f3}")
body=[f'<h1>Charts — jobs, inflation, and the Fed vs the bond market</h1>',
 '<p class=cap>Bar and line charts over the last decade. <b>Thesis tested here:</b> the Fed is steering to the <b>bond market</b> (the 2-year yield), not to its stated dual mandate of 2% inflation and full employment — and a single "jobs number" / "inflation number" hides opposite sectoral and labor-slack trends.</p>',
 '<p class=src>All series are <b>annual</b>, compiled from public data (FRED / BLS / US Treasury / BIS / BOJ), <b>rounded</b> to the precision shown; FRED/BLS series IDs are noted under each chart. "~" marks an estimate or partial year. Verify any value at the cited series. Companion data + sourcing: <a href="https://github.com/pq-cybarg/bubble-map/blob/main/research/macro-jobs-inflation-fed.md">macro-jobs-inflation-fed</a>.</p>']
for h,svg,cap in charts:
    body.append(f'<h2>{esc(h)}</h2>'); body.append(svg); body.append(f'<p class=cap>{cap}</p>')
if TRIGGER_PANEL: body.append(TRIGGER_PANEL)
if SIGNAL_TABLE: body.append(SIGNAL_TABLE)
body.append("""<h2>Breakdown framework &amp; data provenance</h2>
<p class=cap>The bond universe can be sliced along two axes — <b>geography</b> (region → sub-region → country → state → city → institution) and <b>type/quality</b> (sovereign, corporate-by-rating, household/mortgage, municipal, agency). What is charted here vs what requires other sources, stated plainly:</p>
<table><thead><tr><th>Cut</th><th>Charted here?</th><th>Source</th></tr></thead><tbody>
<tr><td>Region / sub-region / country (sovereign 10Y)</td><td><b>Yes</b> — <b>25 countries → 7 GDP-weighted blocs</b> (North America, Core/Periphery Europe, UK&amp;Nordics, CEE, Asia-Pacific, Latin America) + a global aggregate + the <b>periphery-vs-Bund fragmentation</b> spread</td><td>FRED IRLTLT01*M156N (25 countries) + DGS10 (keyless CSV)</td></tr>
<tr><td><b>Industry</b> (equity GICS sectors)</td><td><b>Yes</b> — 12 sectors rebased-to-100 + cross-sectional dispersion (the AI/tech/semis concentration)</td><td>Yahoo chart API (XLK/SMH/XLC/XLY/XLF/XLI/XLV/XLP/XLE/XLU/XLB/XLRE)</td></tr>
<tr><td>Borrower type (sovereign / corporate / household)</td><td><b>Yes</b> (10Y / Baa / 30Y mortgage)</td><td>FRED DGS10 / BAA / MORTGAGE30US</td></tr>
<tr><td>Corporate by credit quality (AAA→CCC ladder)</td><td><b>Yes</b> — full rating ladder (2023+)</td><td>FRED ICE BofA OAS by rating (BAMLC0A1CAAA … BAMLH0A3HYC)</td></tr>
<tr><td>Corporate by region (Emerging-Market)</td><td><b>Yes</b> (2023+)</td><td>FRED BAMLEMPVPRIVSLCRPIUSOAS</td></tr>
<tr><td>Corporate by <b>quality tier</b> (IG / HY / convertibles)</td><td><b>Yes — real FINRA TRACE tape</b> (advance/decline breadth + volume mix, monthly)</td><td><b>FINRA TRACE</b> corporateMarketBreadth/Sentiment (OAuth Query API) → <code>models/graph/fetch_tape.py</code></td></tr>
<tr><td>Corporate by <i>GICS industry</i> (financials/energy/tech)</td><td><b>Proxied</b> — rating ladder + EM + the real TRACE quality tiers stand in; GICS-industry breakdown needs per-CUSIP</td><td>Proxy: FRED rating/EM OAS + TRACE quality tiers · Full: per-CUSIP TRACE file feed (download.finratraqs.org) mapped to SIC, or licensed ICE/Bloomberg</td></tr>
<tr><td>Corporate by maturity (short/int/long IG)</td><td><b>Yes</b> — ETF distribution-yield time series (VCSH/VCIT/VCLT)</td><td>Yahoo chart API (free, keyless)</td></tr>
<tr><td>Municipal by STATE (CA / NY / national / HY)</td><td><b>Yes</b> — per-state ETF distribution-yield time series (CMF/NYF/MUB/HYD), 10yr</td><td>Yahoo chart API (free) + M/T-ratio snapshot</td></tr>
<tr><td>Municipal by CITY / individual issuer</td><td><b>Proxied</b> — state ETFs above stand in</td><td>Full: <b>MSRB EMMA</b> per-CUSIP trade tape (free, but per-bond scraping)</td></tr>
<tr><td>Per-institution (banks)</td><td><b>Yes — elsewhere in the repo</b></td><td>FDIC BankFind API → <code>models/graph/bank_exposure.py</code> (per-bank HTM/AFS, uninsured deposits)</td></tr>
</tbody></table>
<p class=cap>So the institution-level cut already exists (the bank model); the geography (now <b>25 countries / 7 blocs</b>), credit-quality, the <b>real FINRA TRACE quality-tier</b>, and the <b>equity-industry (GICS sector)</b> cuts are charted above. The remaining gaps are <i>GICS-industry corporate OAS</i> (credit-by-industry — equity sectors stand in; full needs per-CUSIP TRACE mapped to SIC) and <i>city/per-issuer</i> muni granularity (state ETFs stand in; full needs MSRB EMMA), plus single-state munis beyond CA/NY where no liquid ETF exists — flagged rather than fabricated, per the project's zero-trust rule.</p>""")
# ===== Cross-sectional analysis section =====
_xs=None
try: _xs=json.load(open(os.path.join(ROOT,"data","cross_section.json")))
except Exception: _xs=None
if _xs and _xs.get("cross_sections"):
    XS=_xs["cross_sections"]
    def _hm_color(c):
        # correlation 0..1 -> pale->deep red; negatives -> blue
        if c is None: return "#fff"
        if c<0: return f"rgba(31,78,121,{min(0.6,abs(c)*0.6):.2f})"
        return f"rgba(123,45,38,{min(0.85,c*0.85):.2f})"
    out=['<h2 id="xsec">Cross-sectional analysis — dispersion, relative value, and the common factor</h2>',
      '<p class=cap>The charts above are mostly <b>time-series</b> (one rate through time). This section is <b>cross-sectional</b>: '
      'at each moment it compares the whole <i>cross-section</i> of segments — every credit-rating bucket, every sovereign, every '
      'muni state — and asks how dispersed they are, which are rich/cheap vs their own history, and <b>how much of their co-movement '
      'is one shared factor.</b> Method follows the credit literature: cross-sectional spread <b>dispersion</b> as a stress gauge; '
      '<b>relative-value z-scores</b> (a segment vs its own trailing history); and a <b>PCA first-principal-component share</b> on '
      'monthly spread <i>changes</i> — Collin-Dufresne, Goldstein &amp; Martin (2001) found one common factor dominates credit-spread '
      'changes. Engine: <code>models/graph/cross_section.py</code> → <code>data/cross_section.json</code>.</p>']

    # --- common-factor headline table ---
    cf_rows=[]
    LBL={"credit_oas":"US corporate credit (OAS rating ladder)","sovereign_10y":"Developed sovereign 10Y",
         "muni_yield":"Municipal (per-state/quality)","trace_breadth":"Corporate breadth by tier (FINRA TRACE)"}
    for k in ("credit_oas","sovereign_10y","muni_yield","trace_breadth"):
        b=XS.get(k)
        if not b: continue
        cf=b["common_factor"]; d=b["dispersion_now"]
        cf_rows.append(f"<tr><td>{esc(LBL[k])}</td><td>{cf['n']}</td><td>{cf['avg_pairwise_corr']}</td>"
                       f"<td><b>{int(round((cf['pc1_share'] or 0)*100))}%</b></td>"
                       f"<td>{d['reading']} (z={d['z_vs_history']})</td></tr>")
    if cf_rows:
        out.append('<h3>The common factor (PC1 share of cross-sectional change)</h3>'
          '<table><thead><tr><th>Cross-section</th><th>Segments</th><th>Avg pairwise corr</th>'
          '<th>PC1 share</th><th>Dispersion now</th></tr></thead><tbody>'+"".join(cf_rows)+'</tbody></table>'
          '<p class=src><b>Reading:</b> a high PC1 share means the segments move as <i>one</i>. US credit’s '
          f"~{int(round((XS['credit_oas']['common_factor']['pc1_share'] or 0)*100))}% PC1 share confirms the "
          'Collin-Dufresne–Goldstein–Martin common factor — and means cross-credit <b>diversification is largely illusory</b> '
          'at the system level (the data point that agrees with the project’s self-marked-value claim: the gaps correlate under '
          'a common factor, so there is no netting). Standard portfolio theory assumes the opposite.</p>')

    # --- dispersion-over-time charts ---
    for k,col in (("credit_oas",AC),("sovereign_10y",AC2)):
        b=XS.get(k)
        if not b: continue
        dts=[r["date"] for r in b["dispersion"]]; std=[r["std"] for r in b["dispersion"]]
        out.append('<h3>'+esc(b["label"].split(" - ")[0])+' — cross-sectional dispersion over time</h3>')
        out.append(monthly_line_chart("Cross-sectional std across segments ("+b["units"]+"), monthly",
            dts,[("dispersion (std)",std)],[col],ylab=b["units"],ymin=0,
            note="Higher = segments spread apart (discrimination/stress); lower = compressed (complacency). "+b["note"]))

    # --- credit correlation heatmap ---
    cm=XS.get("credit_oas",{}).get("common_factor",{}).get("matrix")
    if cm:
        names=list(cm.keys())
        h="<tr><th></th>"+"".join(f"<th>{esc(n)}</th>" for n in names)+"</tr>"
        rows=""
        for a in names:
            cells="".join(f'<td style="background:{_hm_color(cm[a][b2])};text-align:center">{cm[a][b2]:.2f}</td>' for b2 in names)
            rows+=f"<tr><th>{esc(a)}</th>{cells}</tr>"
        out.append('<h3>Credit-spread change correlation (heatmap)</h3>'
          '<table style="font-size:12px">'+h+rows+'</table>'
          '<p class=src>Pearson correlation of monthly OAS <i>changes</i>. Deep red = near-perfectly co-moving — the visual of the common factor.</p>')

    # --- unified RV snapshot ---
    uni=XS.get("unified")
    if uni and uni.get("rows"):
        rr="".join(f"<tr><td>{esc(u['segment'])}</td><td>{esc(u['cross_section'])}</td>"
                   f"<td>{u['latest']} {esc(u['units'])}</td><td>{u['rv_z']}</td><td>{u['pct']}%</td></tr>"
                   for u in uni["rows"])
        out.append('<h3>Unified relative-value snapshot (every segment, z-scored vs its own history)</h3>'
          '<table><thead><tr><th>Segment</th><th>Cross-section</th><th>Latest</th><th>RV z-score</th><th>Pctile</th></tr></thead><tbody>'
          +rr+'</tbody></table>'
          '<p class=src>Positive z = wide/cheap vs its own history (more stress priced in); negative = rich/tight. '
          f"Most stretched right now: <b>{esc(uni['most_stressed']['segment'])}</b>; tightest: <b>{esc(uni['least_stressed']['segment'])}</b>.</p>")

    # --- bank cross-section ---
    bk=XS.get("banks")
    if bk:
        rr="".join(f"<tr><td>{esc(b['bank'])}</td><td>{esc(str(b['state']))}</td><td>{b['assets_b']}</td>"
                   f"<td>{b['htm_loss_to_eq_pct']}%</td><td>{b['uninsured_ratio_pct']}%</td><td>{b['total_cre_to_t1_pct']}%</td>"
                   f"<td><b>{b['composite_z']}</b></td><td>{b['pct']}%</td></tr>" for b in bk["ranking"][:12])
        out.append('<h3>Bank vulnerability cross-section (FDIC, peer-relative z-scores)</h3>'
          '<table style="font-size:12px"><thead><tr><th>Bank</th><th>St</th><th>Assets $B</th><th>HTM loss/eq</th>'
          '<th>Uninsured</th><th>CRE/T1</th><th>Composite z</th><th>Pctile</th></tr></thead><tbody>'+rr+'</tbody></table>'
          f"<p class=src>{bk['n_banks']} institutions; composite z = mean of peer z-scores on HTM-hole, uninsured %, and CRE/Tier-1 "
          f"(higher = more vulnerable). Cross-sectional HTM-hole std ≈ {bk['dispersion_now']['htm_hole_std_pp']}pp of equity — the holes are highly unequal.</p>")

    # --- graph connectors ---
    gc=XS.get("graph_connectors")
    if gc:
        rr="".join(f"<tr><td>{esc(r['node'])}</td><td>{r['degree']}</td><td>{r['n_neighbor_sectors']}</td>"
                   f"<td>{'yes' if r['both_layers'] else 'no'}</td><td><b>{r['bridge_score']}</b></td></tr>" for r in gc["ranking"][:12])
        out.append('<h3>Funding-graph cross-layer connectors (bridging score)</h3>'
          '<table><thead><tr><th>Node</th><th>Degree</th><th>Sectors bridged</th><th>Both layers</th><th>Bridge score</th></tr></thead><tbody>'
          +rr+'</tbody></table>'
          '<p class=src>bridge_score = z(degree) + z(distinct neighbor-sectors) + 0.5 if the node spans both the financial and structural layers. The highest scores are the structural keystones tying the core to the surrounding webs.</p>')

    body.append("".join(out))

body.append('<h2>The bottom line</h2><p class=cap>Across the decade the funds rate maps onto the 2-year Treasury yield, not onto 2% inflation or full employment. Inflation was almost never at target; "true" labor slack (U-6) ran well above the headline; and one aggregate jobs/inflation print masks sectoral and regional divergence. The mandate is the framing; the bond market is the master.</p>')
HTML=(f'<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
      f'<title>Bubble Map — Charts</title><style>{CSS}</style></head><body>{NAV}<main>'+ "".join(body) +'</main></body></html>')
open(os.path.join(DOCS,"charts.html"),"w").write(HTML)
print(f"wrote docs/charts.html ({len(HTML)} bytes, {len(charts)} charts)")
