#!/usr/bin/env python3
"""
core_robustness.py - a concrete-metric re-evaluation of the circular-financing core.

The published headline core (build_graph.py) is a single unweighted Tarjan SCC over the
edges we CLASSIFIED as "financial", with the robust (11) vs headline (12) split resting on a
hand-set `cancelable` flag. This module does NOT touch that computation. Instead it recomputes
the strongly-connected core under a FAMILY of objective, field-based filters and reports:

  * the core under each filter (sensitivity),
  * a per-node robustness score = fraction of filters that keep the node in the core,
  * the certified core (score == 1.0 across all filters) and the plausible core (union),
  * dollar-weighted magnitude + counterparty concentration of the baseline core,
  * the core WITH vs WITHOUT off-balance-sheet rolling (obs_edges from the OBS block),

so "which nodes are unavoidably circular" is answered by measurement, not perception.

Reads   : data/graph.json (financial edges), research/spec-offbalancesheet-ai-financing.json (obs_edges)
Writes  : data/core_robustness.json, report/CORE-ROBUSTNESS.md
Additive: changes nothing in the existing pipeline; safe to run after build_graph.py.
"""
import json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GRAPH = os.path.join(ROOT, "data", "graph.json")
OBS = os.path.join(ROOT, "research", "spec-offbalancesheet-ai-financing.json")
OUT_JSON = os.path.join(ROOT, "data", "core_robustness.json")
OUT_MD = os.path.join(ROOT, "report", "CORE-ROBUSTNESS.md")

sys.setrecursionlimit(100000)

def scc_core(edge_list):
    """Return (set-of-nodes-in-any-nontrivial-SCC, list-of-components)."""
    adj = defaultdict(list)
    nodes = set()
    for e in edge_list:
        adj[e["from"]].append(e["to"]); nodes.add(e["from"]); nodes.add(e["to"])
    idx = {}; low = {}; onstk = {}; stk = []; comps = []; c = [0]
    def sc(v):
        idx[v] = low[v] = c[0]; c[0] += 1; stk.append(v); onstk[v] = True
        for w in adj[v]:
            if w not in idx: sc(w); low[v] = min(low[v], low[w])
            elif onstk.get(w): low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = stk.pop(); onstk[w] = False; comp.append(w)
                if w == v: break
            comps.append(comp)
    for v in nodes:
        if v not in idx: sc(v)
    sccs = [c2 for c2 in comps if len(c2) > 1]
    sccs.sort(key=len, reverse=True)
    core = set().union(*sccs) if sccs else set()
    return core, sccs

# ---- objective field-based filters (predicates on a financial edge) -------------------------
SOFT = ("loi", "announced", "proposed", "guidance", "projection", "implied", "planned",
        "cancel", "weak", "in-progress", "in progress", "pilot", "backer", "marginal",
        "disputed", "2yr projection")
def is_soft(e):
    s = str(e.get("status", "")).lower()
    return any(tok in s for tok in SOFT)
def amt(e):
    a = e.get("amount_usd")
    return a if isinstance(a, (int, float)) else 0

FILTERS = {
    "all":               lambda e: True,                       # baseline (= published headline 12)
    "exclude_cancelable":lambda e: not e.get("cancelable"),    # (= published robust 11)
    "hard_status_only":  lambda e: not is_soft(e),             # drop LOI/announced/projection/cancelled
    "declared_circular": lambda e: bool(e.get("declared_circular")),  # only edges a source called circular
    "sized_only":        lambda e: amt(e) > 0,                 # only edges with a disclosed dollar figure
    "amount>=1B":        lambda e: amt(e) >= 1e9,
    "amount>=5B":        lambda e: amt(e) >= 5e9,
    "amount>=10B":       lambda e: amt(e) >= 10e9,
}
# the non-magnitude ("qualitative") family - robustness that does not depend on a dollar cutoff
QUALITATIVE = ["all", "exclude_cancelable", "hard_status_only", "declared_circular", "sized_only"]

def fmt_usd(x):
    if not x: return "$0"
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if abs(x) >= div: return f"${x/div:.1f}{unit}"
    return f"${x:.0f}"

def main():
    g = json.load(open(GRAPH))
    fin = [e for e in g["edges"] if e.get("layer") == "financial"]

    # per-filter cores + per-node robustness score
    cores = {name: scc_core([e for e in fin if pred(e)])[0] for name, pred in FILTERS.items()}
    all_core_nodes = sorted(set().union(*cores.values()) if cores else set())
    n_filters = len(FILTERS)
    robustness = {}
    for n in all_core_nodes:
        hits = [name for name in FILTERS if n in cores[name]]
        qual_hits = [name for name in QUALITATIVE if n in cores[name]]
        robustness[n] = {
            "score": round(len(hits) / n_filters, 3),
            "filters_in_core": hits,
            "qualitative_score": round(len(qual_hits) / len(QUALITATIVE), 3),
            "in_published_headline": n in cores["all"],
            "in_published_robust": n in cores["exclude_cancelable"],
        }
    certified = sorted([n for n in all_core_nodes if robustness[n]["score"] == 1.0])
    qualitative_certified = sorted([n for n in all_core_nodes if robustness[n]["qualitative_score"] == 1.0])
    plausible = all_core_nodes

    # dollar weighting of the baseline core
    base_core = cores["all"]
    intra = [e for e in fin if e["from"] in base_core and e["to"] in base_core]
    headline_usd = sum(amt(e) for e in intra)
    committed_usd = sum(amt(e) for e in intra if not is_soft(e))
    pair_usd = defaultdict(float)
    for e in intra:
        if amt(e): pair_usd[(e["from"], e["to"])] += amt(e)
    top_pairs = sorted(pair_usd.items(), key=lambda kv: kv[1], reverse=True)[:8]
    concentration = round(max(pair_usd.values()) / committed_usd, 3) if (pair_usd and committed_usd) else 0.0
    node_circ = {}
    for n in sorted(base_core):
        cin = sum(amt(e) for e in intra if e["to"] == n)
        cout = sum(amt(e) for e in intra if e["from"] == n)
        node_circ[n] = {"circular_in_usd": cin, "circular_out_usd": cout, "circular_throughput_usd": cin + cout}

    # WITH vs WITHOUT off-balance-sheet rolling
    obs_edges = []
    if os.path.exists(OBS):
        obs_edges = json.load(open(OBS)).get("obs_edges", [])
    core_without_obs = base_core                      # == published headline set
    core_with_obs, _ = scc_core(fin + obs_edges)
    obs_added = sorted(core_with_obs - core_without_obs)
    obs_intra = [e for e in (fin + obs_edges) if e["from"] in core_with_obs and e["to"] in core_with_obs]
    obs_headline_usd = sum(amt(e) for e in obs_intra)

    result = {
        "note": "Additive concrete-metric re-evaluation of the circular-financing core. Does NOT replace the "
                "published headline SCC (12) / robust SCC (11) in data/graph.json analysis; it certifies/stresses it.",
        "n_financial_edges": len(fin),
        "filters": {name: sorted(cores[name]) for name in FILTERS},
        "filter_core_sizes": {name: len(cores[name]) for name in FILTERS},
        "per_node_robustness": robustness,
        "certified_core": certified,
        "certified_core_size": len(certified),
        "qualitative_certified_core": qualitative_certified,
        "qualitative_certified_core_size": len(qualitative_certified),
        "plausible_core": plausible,
        "plausible_core_size": len(plausible),
        "published_headline": sorted(cores["all"]),
        "published_robust": sorted(cores["exclude_cancelable"]),
        "dollar_weight_baseline_core": {
            "headline_usd": headline_usd, "committed_usd": committed_usd,
            "largest_counterparty_pair": [list(top_pairs[0][0]), top_pairs[0][1]] if top_pairs else None,
            "largest_pair_share_of_committed": concentration,
            "top_pairs": [[list(k), v] for k, v in top_pairs],
            "per_node_circular_throughput": node_circ,
        },
        "off_balance_sheet": {
            "n_obs_edges": len(obs_edges),
            "core_without_obs": sorted(core_without_obs),
            "core_with_obs": sorted(core_with_obs),
            "nodes_added_by_obs": obs_added,
            "core_with_obs_intra_usd": obs_headline_usd,
        },
    }
    json.dump(result, open(OUT_JSON, "w"), indent=1)
    write_md(result)
    print(f"[core_robustness] headline={len(cores['all'])} robust={len(cores['exclude_cancelable'])} "
          f"certified={len(certified)} qual_certified={len(qualitative_certified)} "
          f"plausible={len(plausible)} | +obs adds {len(obs_added)}: {obs_added}")

def write_md(r):
    L = []
    L.append("# Circular-financing core - concrete-metric robustness certificate")
    L.append("")
    L.append("*Additive re-evaluation. This does NOT replace the published headline core (SCC of 12) or "
             "robust core (11) - it stress-tests them against a family of objective, field-based filters so "
             "the core is justified by measurement rather than by the hand-set `cancelable` / `declared_circular` "
             "flags alone. Generated by `models/graph/core_robustness.py`.*")
    L.append("")
    L.append("## Method")
    L.append("")
    L.append("Each filter is a predicate on a financial edge using only recorded fields "
             "(`amount_usd`, `status`, `cancelable`, `declared_circular`). For each filter the strongly-connected "
             "core is recomputed (Tarjan). A node's **robustness score** is the fraction of filters that keep it in "
             "the core. The **certified core** is the set of nodes with score 1.0 (in the core under *every* lens); "
             "the **plausible core** is the union (in the core under *any* lens).")
    L.append("")
    L.append("## Core size under each filter")
    L.append("")
    L.append("| filter | core size | nodes |")
    L.append("|---|---|---|")
    for name in FILTERS:
        nodes = sorted(r["filters"][name])
        L.append(f"| `{name}` | {len(nodes)} | {', '.join(nodes) if nodes else '(none)'} |")
    L.append("")
    L.append("## Per-node robustness")
    L.append("")
    L.append("Score = fraction of all 8 filters keeping the node in the core. "
             "`qual` = fraction of the 5 non-magnitude filters (dollar cutoffs excluded). "
             "H/R = in published Headline (12) / Robust (11).")
    L.append("")
    L.append("| node | score | qual | H | R |")
    L.append("|---|---|---|---|---|")
    for n in sorted(r["per_node_robustness"], key=lambda x: (-r["per_node_robustness"][x]["score"], x)):
        d = r["per_node_robustness"][n]
        L.append(f"| {n} | {d['score']:.2f} | {d['qualitative_score']:.2f} | "
                 f"{'yes' if d['in_published_headline'] else '-'} | {'yes' if d['in_published_robust'] else '-'} |")
    L.append("")
    L.append(f"**Certified core** (score 1.0, {r['certified_core_size']}): "
             f"{', '.join(r['certified_core']) if r['certified_core'] else '(none)'}")
    L.append("")
    L.append(f"**Qualitative-certified core** (1.0 across the 5 non-magnitude filters, "
             f"{r['qualitative_certified_core_size']}): "
             f"{', '.join(r['qualitative_certified_core']) if r['qualitative_certified_core'] else '(none)'}")
    L.append("")
    L.append(f"**Plausible core** (union, {r['plausible_core_size']}): {', '.join(r['plausible_core'])}")
    L.append("")
    dw = r["dollar_weight_baseline_core"]
    L.append("## Dollar weight of the baseline core")
    L.append("")
    L.append(f"- Intra-core committed (hard-status) value: **{fmt_usd(dw['committed_usd'])}**")
    L.append(f"- Intra-core headline value (incl. soft/LOI): **{fmt_usd(dw['headline_usd'])}**")
    if dw["largest_counterparty_pair"]:
        p = dw["largest_counterparty_pair"]
        L.append(f"- Largest single counterparty edge: **{p[0][0]} -> {p[0][1]}** at {fmt_usd(p[1])} "
                 f"(**{dw['largest_pair_share_of_committed']*100:.0f}%** of committed intra-core value) - concentration signal")
    L.append("")
    L.append("Top intra-core edges by disclosed value:")
    L.append("")
    for k, v in dw["top_pairs"]:
        L.append(f"- {k[0]} -> {k[1]}: {fmt_usd(v)}")
    L.append("")
    obs = r["off_balance_sheet"]
    L.append("## With vs without off-balance-sheet rolling")
    L.append("")
    L.append(f"The off-balance-sheet ledger (`spec-offbalancesheet-ai-financing.json`, {obs['n_obs_edges']} "
             f"`obs_edges`, not ingested into the published graph) is added to the financial edge set and the core "
             f"recomputed.")
    L.append("")
    L.append(f"- Core WITHOUT off-balance-sheet (= published headline): **{len(obs['core_without_obs'])}** - "
             f"{', '.join(obs['core_without_obs'])}")
    L.append(f"- Core WITH off-balance-sheet: **{len(obs['core_with_obs'])}** - {', '.join(obs['core_with_obs'])}")
    L.append(f"- Nodes pulled into the core BY off-balance-sheet rolling: "
             f"**{', '.join(obs['nodes_added_by_obs']) if obs['nodes_added_by_obs'] else '(none)'}**")
    L.append(f"- Intra-core value with off-balance-sheet included: **{fmt_usd(obs['core_with_obs_intra_usd'])}**")
    L.append("")
    L.append("*Interpretation of the with/without delta is labeled: operating-lease and SPV accounting is "
             "permitted under GAAP; the added nodes/edges represent economic exposure the rating agencies and the "
             "BIS add back, not a legal finding of concealment.*")
    L.append("")
    open(OUT_MD, "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    main()
