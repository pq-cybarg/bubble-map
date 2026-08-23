#!/usr/bin/env python3
"""
fetch_qri.py — pull the Blockchain Quantum Readiness Index (qrindex.org).

Primary: GET https://qrindex.org/api/projects.json (CoinGecko-id keyed compact index).
Enrichment: GET https://qrindex.org/projects/<id>/report.json for chains we track.
Fallback: scrapy crawl of qrindex.org/ if the API is down (see qri_spider.py).

Writes data/qri_index.json. Network-tolerant: on failure, keeps the last cache.
QRI is a third-party, AI-assisted, pre-release index — not a Bubble Map proof.
"""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "qri_index.json")
API = "https://qrindex.org/api/projects.json"
UA = "BubbleMap-QRI-fetch/1.0 (+https://github.com/pq-cybarg/bubble-map; research; cache-only)"

# registry id -> qrindex / CoinGecko id
MAP = {
    "Bitcoin": "bitcoin", "Ethereum": "ethereum", "Solana": "solana",
    "XRPL": "ripple", "Ripple": "ripple", "Hedera": "hedera-hashgraph",
    "Stellar": "stellar", "Sui": "sui", "Aptos": "aptos", "Cardano": "cardano",
    "Avalanche": "avalanche-2", "Polkadot": "polkadot", "Cosmos": "cosmos",
    "TON": "the-open-network", "QRL": "quantum-resistant-ledger",
    "Monero": "monero", "Zcash": "zcash", "Arbitrum": "arbitrum",
    "Optimism": "optimism", "Polygon": "polygon-ecosystem-token",
    "Hyperliquid": "hyperliquid", "Uniswap": "uniswap", "Tether": "tether",
    "Circle": "usd-coin", "RLUSD": "ripple-usd", "Mochimo": "mochimo",
    "Algorand": "algorand", "NEAR": "near", "BNB": "binancecoin",
    "Dogecoin": "dogecoin", "Bitcoin_Cash": "bitcoin-cash",
    "Starknet": "starknet", "Aave": "aave", "MakerDAO": "dai",
    "Compound": "compound-governance-token", "Chainlink": "chainlink",
    "Abelian": "abelian", "Cellframe": "cellframe", "Tidecoin": "tidecoin",
    "QuantumCoin": "quantumcoin", "Nervos": "nervos-network",
    "MCM": "mochimo", "QRL_Foundation": "quantum-resistant-ledger",
    "Linea": "linea", "Base": "base", "dYdX": "dydx-chain",
    "PancakeSwap": "pancakeswap-token", "SushiSwap": "sushi",
    "Curve": "curve-dao-token", "Lido": "lido-dao",
    "Bittensor": "bittensor", "Filecoin": "filecoin",
    "Flare": "flare-networks", "Internet_Computer": "internet-computer",
}

STAGE_LABEL = {
    0: "Stage 0 — Unassessed / no evidence",
    1: "Stage 1 — Quantum risk assessed",
    2: "Stage 2 — Mitigation / development",
    3: "Stage 3 — Migration live",
    4: "Stage 4 — Migration complete / quantum-ready",
}


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/plain,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def load_cache():
    try:
        return json.load(open(OUT))
    except Exception:
        return {}


def fetch_api():
    raw = _get(API)
    projects = json.loads(raw.decode("utf-8"))
    if not isinstance(projects, dict) or not projects:
        raise RuntimeError("empty QRI API")
    return projects


def fetch_report(pid):
    url = f"https://qrindex.org/projects/{pid}/report.json"
    try:
        return json.loads(_get(url, timeout=20).decode("utf-8"))
    except Exception:
        return None


def scrape_fallback():
    """HTML fallback via scrapy if installed, else stdlib parse of the homepage + llms.txt."""
    try:
        from qri_spider import scrape_qrindex  # type: ignore
        return scrape_qrindex()
    except Exception:
        pass
    # llms.txt is structured enough to rebuild the compact index
    try:
        text = _get("https://qrindex.org/llms.txt", timeout=30).decode("utf-8", "replace")
    except Exception:
        return {}
    import re
    out = {}
    for m in re.finditer(
        r"\[([^\]]+) QRI report\]\(https://qrindex.org/projects/([^/]+)/llms\.txt\): "
        r"QRI ([0-9.]+)/100; Stage (\d+)",
        text,
    ):
        name, pid, score, stage = m.group(1), m.group(2), float(m.group(3)), int(m.group(4))
        out[pid] = {
            "project_name": name,
            "canonical_url": f"https://qrindex.org/projects/{pid}/",
            "qri_score": score,
            "qri_stage": stage,
        }
    return out


def enrich(projects, want_pids, limit=80):
    reports = {}
    n = 0
    for pid in want_pids:
        if n >= limit:
            break
        if pid not in projects:
            continue
        rep = fetch_report(pid)
        n += 1
        time.sleep(0.12)
        if not rep:
            continue
        reports[pid] = {
            "score": rep.get("score"),
            "stage": rep.get("stage"),
            "stage_label": rep.get("stage_label"),
            "confidence": rep.get("confidence"),
            "evaluation_date": rep.get("evaluation_date"),
            "review_status": rep.get("review_status"),
            "symbol": rep.get("symbol"),
            "summary": (rep.get("summary") or "")[:900],
            "critical_blockers": (rep.get("critical_quantum_blockers") or rep.get("critical_blockers") or [])[:6],
            "tags": rep.get("tags") or [],
            "user_urgency": rep.get("user_urgency_status"),
            "category_scores": rep.get("category_scores") or {},
            "network": rep.get("network"),
        }
    return reports


def main():
    os.makedirs(DATA, exist_ok=True)
    cache = load_cache()
    source = "api"
    try:
        projects = fetch_api()
    except Exception as e:
        print(f"[qri] API failed ({e}); trying scrape/llms fallback", file=sys.stderr)
        source = "scrape"
        try:
            projects = scrape_fallback()
        except Exception as e2:
            print(f"[qri] fallback failed ({e2}); keeping cache", file=sys.stderr)
            if cache:
                print(f"[qri] cache has {len(cache.get('projects') or {})} projects")
                return 0
            return 1
        if not projects:
            print("[qri] empty fallback; keeping cache", file=sys.stderr)
            return 0 if cache else 1

    want = sorted(set(MAP.values()) | set(projects.keys()))
    # Always enrich Stage-4 plus mapped registry chains
    stage4 = [pid for pid, v in projects.items() if (v.get("qri_stage") or 0) >= 4]
    mapped = list(MAP.values())
    reports = {}
    try:
        reports = enrich(projects, list(dict.fromkeys(stage4 + mapped)))
    except Exception as e:
        print(f"[qri] report enrich partial ({e})", file=sys.stderr)

    out = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": source,
        "api": API,
        "disclaimer": "QRI is a third-party, AI-assisted, pre-release index (qrindex.org). Scores are not market ratings and are not Bubble Map proofs. Interpret with evaluation date, confidence, and critical blockers.",
        "stage_labels": STAGE_LABEL,
        "map": MAP,
        "projects": projects,
        "reports": reports,
        "n_projects": len(projects),
        "n_stage4": sum(1 for v in projects.values() if (v.get("qri_stage") or 0) >= 4),
    }
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"wrote {OUT}  projects={out['n_projects']} stage4={out['n_stage4']} reports={len(reports)} source={source}")
    qrl = projects.get("quantum-resistant-ledger") or {}
    print(f"  QRL  score={qrl.get('qri_score')} stage={qrl.get('qri_stage')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
