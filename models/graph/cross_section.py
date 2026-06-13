#!/usr/bin/env python3
"""
cross_section.py - cross-sectional analysis across (1) the bond/credit universe, (2) the bank
universe, (3) the funding-graph layers, and (4) a unified normalized snapshot. For every
cross-section we compute the standard quant-credit toolkit:

  - dispersion over time      cross-sectional std / range across segments each period (a stress gauge)
  - relative-value z-scores   each segment's latest level vs its OWN trailing history (rich / cheap)
  - snapshot ranking          latest period, every segment side by side, ranked
  - cross-sectional corr      average pairwise correlation + PCA first-principal-component share
                              (PC1 share = the empirical 'common factor' signature)

Literature anchors (so the choices are not ad hoc):
  * Collin-Dufresne, Goldstein & Martin (2001), "The Determinants of Credit Spread Changes"
    (Journal of Finance 56(6)): monthly credit-spread CHANGES are dominated by a single common
    (systematic) factor that the usual structural variables (leverage, vol, rates, slope) do not
    explain - their PCA finds one factor explaining the bulk of the residual covariance. A high PC1
    share on Delta-OAS is exactly that factor.
  * Cross-sectional spread DISPERSION compresses in calm regimes and blows out in stress / recession
    (credit-dispersion-as-stress-gauge; cf. distress-risk and credit-cycle literature).
  * Relative value by z-score / percentile vs a security's own trailing history is standard desk RV.
  * Sovereign-yield dispersion across a currency/region bloc is a fragmentation gauge (euro-area
    periphery literature).

DISAGREEMENT WITH THE LITERATURE (reported, not hidden): mean-variance portfolio theory assumes that
holding many different credits diversifies idiosyncratic risk away. When PC1 explains most of the
cross-sectional variance - i.e. the segments move as ONE - that diversification is illusory at the
system level. That is precisely the project's self-marked-value claim (U1-U4): "the gaps correlate
under a common factor; there is no netting." We compute the PC1 share and label it against that claim.

Pure Python stdlib (no numpy). Top eigenvalue via power iteration on the correlation matrix
(sum of a correlation matrix's eigenvalues = n, so PC1 share = lambda1 / n). Writes
data/cross_section.json. Tolerates missing inputs; only emits the cross-sections it can build.
"""
import json, os, math
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(ROOT,"data")

def _load(n):
    try: return json.load(open(os.path.join(DATA,n)))
    except Exception: return None

# ---------- small stats (stdlib only) ----------
def _mean(xs): return sum(xs)/len(xs) if xs else float("nan")
def _std(xs):
    if len(xs)<2: return 0.0
    m=_mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def _pearson(a,b):
    n=min(len(a),len(b))
    if n<3: return 0.0
    a,b=a[:n],b[:n]; ma,mb=_mean(a),_mean(b)
    num=sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    da=math.sqrt(sum((x-ma)**2 for x in a)); db=math.sqrt(sum((x-mb)**2 for x in b))
    return num/(da*db) if da and db else 0.0
def _zscore(x, hist):
    s=_std(hist); return round((x-_mean(hist))/s,2) if s else None
def _pct_rank(x, hist):
    if not hist: return None
    return round(100*sum(1 for h in hist if h<=x)/len(hist),0)
def _chg(seq): return [seq[i]-seq[i-1] for i in range(1,len(seq))]

def _top_eig_share(R):
    """PC1 variance share of an n x n correlation matrix via power iteration.
    Eigenvalues of a correlation matrix sum to n -> share = lambda1 / n."""
    n=len(R)
    if n<2: return None,None
    v=[1.0/math.sqrt(n)]*n
    for _ in range(400):
        w=[sum(R[i][j]*v[j] for j in range(n)) for i in range(n)]
        nrm=math.sqrt(sum(x*x for x in w)) or 1.0
        v=[x/nrm for x in w]
    Rv=[sum(R[i][j]*v[j] for j in range(n)) for i in range(n)]
    lam=sum(v[i]*Rv[i] for i in range(n))            # Rayleigh quotient
    return lam, lam/n

# ---------- time-series cross-section (credit / sovereign / muni) ----------
def ts_cross_section(segments, label, units, rv_window=36, note=""):
    """segments: {name: {YYYY-MM: value}}. Returns the full toolkit dict, or None if too thin."""
    segments={k:v for k,v in segments.items() if v}
    if len(segments)<2: return None
    dates=sorted(set.intersection(*[set(v) for v in segments.values()]))
    if len(dates)<6: return None
    names=list(segments.keys())
    M={k:[segments[k][d] for d in dates] for k in names}     # aligned levels

    # dispersion over time (cross-sectional std/range/mean each period)
    disp=[]
    for i,d in enumerate(dates):
        col=[M[k][i] for k in names]
        disp.append({"date":d,"mean":round(_mean(col),3),"std":round(_std(col),3),
                     "min":round(min(col),3),"max":round(max(col),3),"range":round(max(col)-min(col),3)})
    disp_std_series=[r["std"] for r in disp]
    disp_now=disp[-1]["std"]; disp_z=_zscore(disp_now, disp_std_series)
    disp_pct=_pct_rank(disp_now, disp_std_series)

    # relative value: latest vs own trailing window
    rv={}
    for k in names:
        hist=M[k][-rv_window:] if len(M[k])>=rv_window else M[k]
        full=M[k]; latest=M[k][-1]
        rv[k]={"latest":round(latest,3),"mean":round(_mean(hist),3),"std":round(_std(hist),3),
               "z":_zscore(latest,hist),"pct":_pct_rank(latest,full),
               "window":min(rv_window,len(M[k]))}

    # snapshot ranking (latest date), richest spread/yield first
    ranking=sorted([{"segment":k,"latest":rv[k]["latest"],"z":rv[k]["z"],"pct":rv[k]["pct"]}
                    for k in names], key=lambda r:-(r["latest"] if r["latest"] is not None else -1e9))

    # cross-sectional correlation + common factor on monthly CHANGES (CDGM basis)
    ch={k:_chg(M[k]) for k in names}
    R=[[_pearson(ch[a],ch[b]) for b in names] for a in names]
    pair=[R[i][j] for i in range(len(names)) for j in range(i+1,len(names))]
    avg_corr=round(_mean(pair),3) if pair else None
    lam1,pc1=_top_eig_share(R)
    cm={"n":len(names),"basis":"monthly change (Delta) - Collin-Dufresne-Goldstein-Martin",
        "avg_pairwise_corr":avg_corr,
        "pc1_eigenvalue":round(lam1,3) if lam1 is not None else None,
        "pc1_share":round(pc1,3) if pc1 is not None else None,
        "matrix":{names[i]:{names[j]:round(R[i][j],2) for j in range(len(names))} for i in range(len(names))}}

    return {"label":label,"units":units,"note":note,"segments":names,
            "n_dates":len(dates),"date_first":dates[0],"date_last":dates[-1],
            "dispersion":disp,
            "dispersion_now":{"std":round(disp_now,3),"z_vs_history":disp_z,"pct_of_history":disp_pct,
                              "reading":("compressed" if (disp_z is not None and disp_z<-0.5) else
                                         "elevated" if (disp_z is not None and disp_z>0.5) else "mid-range")},
            "relative_value":rv,"ranking":ranking,"common_factor":cm}

# ---------- helpers to assemble inputs ----------
def _ttm_yield(etf):
    months=sorted(etf); out={}
    for i in range(11,len(months)):
        m=months[i]; px=etf[m].get("c")
        if not px: continue
        d12=sum(etf[months[j]].get("d",0.0) for j in range(i-11,i+1))
        out[m]=round(100*d12/px,3)
    return out

def build():
    fm=(_load("fred_monthly.json") or {}).get("data",{})
    ya=(_load("yahoo_monthly.json") or {}).get("data",{})
    out={"meta":{"generator":"models/graph/cross_section.py",
                 "methods":["dispersion_over_time","relative_value_zscore","snapshot_ranking",
                            "cross_sectional_correlation_pca_pc1"],
                 "literature":["Collin-Dufresne Goldstein Martin 2001 (common factor in credit-spread changes)",
                               "credit-spread dispersion as a stress/credit-cycle gauge",
                               "sovereign-yield dispersion as a fragmentation gauge",
                               "z-score/percentile relative value (desk standard)"],
                 "diversification_caveat":("high PC1 share => segments move as one => cross-sectional "
                               "diversification is illusory at the system level (self_marked_value U1-U4: "
                               "'gaps correlate under a common factor; no netting')")},
           "cross_sections":{}}
    cs=out["cross_sections"]

    # (1a) CREDIT - ICE BofA OAS rating ladder + IG/HY/EM aggregates (whatever is cached)
    LADDER=[("AAA","BAMLC0A1CAAA"),("AA","BAMLC0A2CAA"),("A","BAMLC0A3CA"),("BBB","BAMLC0A4CBBB"),
            ("BB","BAMLH0A1HYBB"),("B","BAMLH0A2HYB"),("CCC","BAMLH0A3HYC"),
            ("IG (all)","BAMLC0A0CM"),("HY (all)","BAMLH0A0HYM2"),("EM corp","BAMLEMPVPRIVSLCRPIUSOAS")]
    credit={lab:fm[sid] for lab,sid in LADDER if sid in fm and fm[sid]}
    r=ts_cross_section(credit,"US corporate credit - option-adjusted spread (rating ladder + aggregates)","pp (OAS)",
        note="ICE BofA OAS by rating. Dispersion = the spread between quality buckets (credit discrimination).")
    if r: cs["credit_oas"]=r

    # (1b) SOVEREIGN - 10Y yields across the FULL available cross-section (dynamic, up to 26 countries)
    _CCNAME={"DE":"Germany","GB":"UK","FR":"France","IT":"Italy","JP":"Japan","CA":"Canada","AU":"Australia",
             "ES":"Spain","NL":"Netherlands","BE":"Belgium","AT":"Austria","CH":"Switzerland","IE":"Ireland",
             "PT":"Portugal","FI":"Finland","SE":"Sweden","NO":"Norway","DK":"Denmark","PL":"Poland",
             "CZ":"Czechia","HU":"Hungary","KR":"Korea","NZ":"New Zealand","MX":"Mexico","CL":"Chile","GR":"Greece"}
    SOV=[("US","DGS10")]+[(_CCNAME[cc],f"IRLTLT01{cc}M156N") for cc in _CCNAME]
    sov={lab:fm[sid] for lab,sid in SOV if sid in fm and fm[sid] and len(fm[sid])>=120}
    r=ts_cross_section(sov,"Sovereign 10Y yield (global cross-section)","% yield",
        note=f"{len(sov)}-country cross-section. Dispersion = sovereign fragmentation; PC1 = the global rates common factor.")
    if r: cs["sovereign_10y"]=r

    # (1c) MUNICIPAL - per-state/segment ETF distribution yields
    MUNI=[("CA (CMF)","CMF"),("NY (NYF)","NYF"),("National (MUB)","MUB"),("HY muni (HYD)","HYD")]
    muni={lab:_ttm_yield(ya[t]) for lab,t in MUNI if t in ya and ya[t]}
    r=ts_cross_section(muni,"Municipal bond distribution yield (per-state / quality ETFs)","% dist. yield",
        rv_window=24, note="Trailing-12mo distribution yield; dispersion across states & quality.")
    if r: cs["muni_yield"]=r

    # (1d) CREDIT TIERS from the real FINRA TRACE tape (advance/decline breadth ratio)
    tape=_load("tape_trace.json") or {}
    cb=tape.get("corporate_breadth",{})
    if cb:
        TIERS=["investment grade","high yield","convertibles"]
        seg={t.title():{m:cb[t][m]["ad_ratio"] for m in cb[t] if cb[t][m].get("ad_ratio") is not None and cb[t][m]["days"]>=15}
             for t in TIERS if t in cb}
        r=ts_cross_section(seg,"Corporate breadth by quality tier (FINRA TRACE advance/decline ratio)","ratio",
            rv_window=12, note="Real TRACE tape: advancing/declining bonds by quality tier; PC1 = shared risk-on/off.")
        if r: cs["trace_breadth"]=r

    # (2) BANK cross-section (point-in-time across institutions) ----
    be=_load("bank_exposure.json") or {}
    banks=[b for b in be.get("banks",[]) if b.get("bkclass")!="OI"]
    if banks:
        # metrics where HIGHER = MORE vulnerable (sign-flip htm/secs losses which are negative)
        def m_htm(b): return -(b.get("htm_loss_to_eq_pct") or 0.0)      # bigger positive = bigger hole
        def m_unins(b): return b.get("uninsured_ratio_pct") or 0.0
        def m_cre(b): return b.get("total_cre_to_t1_pct") or 0.0
        METS=[("htm_hole","HTM loss / equity",m_htm),("uninsured","Uninsured-deposit %",m_unins),
              ("cre","CRE / Tier-1 %",m_cre)]
        for key,_,fn in METS:
            vals=[fn(b) for b in banks]
            mu,sd=_mean(vals),_std(vals)
            for b in banks:
                b.setdefault("_z",{})[key]=round((fn(b)-mu)/sd,2) if sd else 0.0
        for b in banks:
            b["_composite_z"]=round(_mean([b["_z"][k] for k,_,_ in METS]),2)
        for b in banks:
            comp=[bb["_composite_z"] for bb in banks]
            b["_pct"]=_pct_rank(b["_composite_z"],comp)
        ranked=sorted(banks,key=lambda b:-b["_composite_z"])[:15]
        # dispersion of HTM holes across the system
        htm_vals=[m_htm(b) for b in banks]
        cs["banks"]={"label":"Bank vulnerability cross-section (FDIC, per institution)","units":"z-score (peer-relative)",
            "n_banks":len(banks),"metrics":[m[1] for m in METS],
            "note":"Cross-sectional z per metric (higher=worse), composite = mean of the three; percentile vs peers.",
            "dispersion_now":{"htm_hole_std_pp":round(_std(htm_vals),2),"htm_hole_max_pp":round(max(htm_vals),2),
                              "reading":"how unequal the hidden HTM holes are across the system"},
            "ranking":[{"bank":b["name"],"state":b.get("state"),"assets_b":b.get("assets_b"),
                        "htm_loss_to_eq_pct":b.get("htm_loss_to_eq_pct"),"uninsured_ratio_pct":b.get("uninsured_ratio_pct"),
                        "total_cre_to_t1_pct":b.get("total_cre_to_t1_pct"),
                        "composite_z":b["_composite_z"],"pct":b["_pct"]} for b in ranked]}

    # (3) GRAPH cross-layer connectors (bridging cross-section) ----
    g=_load("graph.json") or {}
    con=g.get("analysis",{}).get("top_cross_layer_connectors",[])
    if con:
        degs=[c.get("degree",0) for c in con]; secs=[c.get("n_neighbor_sectors",0) for c in con]
        md,sd_d=_mean(degs),_std(degs); ms,sd_s=_mean(secs),_std(secs)
        rows=[]
        for c in con:
            zd=(c.get("degree",0)-md)/sd_d if sd_d else 0.0
            zs=(c.get("n_neighbor_sectors",0)-ms)/sd_s if sd_s else 0.0
            bridge=round(zd+zs+(0.5 if c.get("both_layers") else 0.0),2)   # bridging score
            rows.append({"node":c["node"],"degree":c.get("degree"),"n_neighbor_sectors":c.get("n_neighbor_sectors"),
                         "both_layers":c.get("both_layers"),"bridge_score":bridge})
        rows.sort(key=lambda r:-r["bridge_score"])
        cs["graph_connectors"]={"label":"Funding-graph cross-layer connectors (bridging cross-section)",
            "units":"bridging z-score","n_nodes":len(rows),
            "note":"bridge_score = z(degree) + z(distinct neighbor-sectors) + 0.5 if the node spans both layers.",
            "ranking":rows}

    # (4) UNIFIED snapshot - latest RV z across the time-series cross-sections, normalized side by side
    uni=[]
    for csk in ("credit_oas","sovereign_10y","muni_yield","trace_breadth"):
        block=cs.get(csk)
        if not block: continue
        for seg,rvd in block["relative_value"].items():
            uni.append({"cross_section":block["label"].split(" - ")[0],"segment":seg,
                        "latest":rvd["latest"],"units":block["units"],"rv_z":rvd["z"],"pct":rvd["pct"]})
    if uni:
        rich=sorted([u for u in uni if u["rv_z"] is not None],key=lambda u:-(u["rv_z"]))
        cf={csk:cs[csk]["common_factor"]["pc1_share"] for csk in ("credit_oas","sovereign_10y","muni_yield","trace_breadth") if csk in cs}
        cs["unified"]={"label":"Unified cross-sectional snapshot (all segments, RV z-scored)",
            "note":"Every segment's latest level z-scored vs its own history, so credit / sovereign / muni / "
                   "breadth read side by side. Positive rv_z = wide/cheap vs own history (more stress priced).",
            "rows":rich,
            "common_factor_by_cross_section":cf,
            "most_stressed":rich[0] if rich else None,"least_stressed":rich[-1] if rich else None}

    json.dump(out,open(os.path.join(DATA,"cross_section.json"),"w"),indent=1)
    # console summary
    print("== cross-sectional analysis ==")
    for k,v in cs.items():
        if "common_factor" in v:
            cf=v["common_factor"]; d=v.get("dispersion_now",{})
            print(f"  {k:16s} n={cf['n']:2d}  avgcorr={cf['avg_pairwise_corr']}  PC1share={cf['pc1_share']}  "
                  f"disp={d.get('reading','-')} (z={d.get('z_vs_history')})")
        elif k=="banks":
            print(f"  {k:16s} n={v['n_banks']}  HTM-hole std={v['dispersion_now']['htm_hole_std_pp']}pp  top={v['ranking'][0]['bank']}")
        elif k=="graph_connectors":
            print(f"  {k:16s} n={v['n_nodes']}  top bridge={v['ranking'][0]['node']} ({v['ranking'][0]['bridge_score']})")
        elif k=="unified":
            ms=v.get("most_stressed"); print(f"  {k:16s} rows={len(v['rows'])}  most-stressed={ms['segment'] if ms else '-'}")
    print("wrote data/cross_section.json")

if __name__=="__main__": build()
