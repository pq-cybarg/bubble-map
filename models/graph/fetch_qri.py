#!/usr/bin/env python3
"""
fetch_qri.py — scrape the Blockchain Quantum Readiness Index (qrindex.org).

There is NO stable API. The site's JSON paths (if any) and HTML class names
change. This fetcher:

  1. GETs the public homepage HTML and parses the ranking table defensively
     (data-* attributes when present, visible cells otherwise).
  2. Optionally GETs each project's llms.txt for summary / date / confidence
     (plain text, still not a contract).
  3. If scrapy is importable, prefers the spider in qri_spider.py.
  4. Snapshots raw homepage HTML to data/qri_raw/ so a selector break is auditable.

Never required: /api/projects.json or report.json.

Writes data/qri_index.json. Network-tolerant: on failure, keeps the last cache.
QRI is a third-party, AI-assisted, pre-release index — not a Bubble Map proof.
"""
from __future__ import annotations
import json, os, sys, time, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qri_parse import parse_index_html, parse_llms_project, parse_llms_index, STAGE_LABEL  # noqa: E402

DATA = os.path.join(ROOT, "data")
RAW = os.path.join(DATA, "qri_raw")
OUT = os.path.join(DATA, "qri_index.json")
INDEX = "https://qrindex.org/"
UA = "BubbleMap-QRI-scrape/1.0 (+https://github.com/pq-cybarg/bubble-map; research cache)"

# registry id -> qrindex slug (best-effort; unmatched chains stay qri:null)
MAP = {
    "Bitcoin": "bitcoin", "Ethereum": "ethereum", "Solana": "solana",
    "XRPL": "xrp", "Ripple": "xrp", "Hedera": "hedera-hashgraph",
    "Stellar": "stellar", "Sui": "sui", "Aptos": "aptos", "Cardano": "cardano",
    "Avalanche": "avalanche-2", "Polkadot": "polkadot", "Cosmos": "cosmos",
    "TON": "toncoin", "QRL": "quantum-resistant-ledger",
    "Monero": "monero", "Zcash": "zcash", "Arbitrum": "arbitrum",
    "Optimism": "optimism", "Polygon": "polygon-ecosystem-token",
    "Hyperliquid": "hyperliquid", "Uniswap": "uniswap", "Tether": "tether",
    "Circle": "usd-coin", "RLUSD": "ripple-usd", "Mochimo": "mochimo",
    "Algorand": "algorand", "NEAR": "near", "BNB": "bnb", "BNB_Chain": "bnb",
    "Dogecoin": "dogecoin", "Bitcoin_Cash": "bitcoin-cash",
    "Starknet": "starknet", "Aave": "aave", "MakerDAO": "dai",
    "Compound": "compound-governance-token", "Chainlink": "chainlink",
    "Abelian": "abelian", "Cellframe": "cellframe", "Tidecoin": "tidecoin",
    "QuantumCoin": "quantumcoin", "Nervos": "nervos-network",
    "MCM": "mochimo", "QRL_Foundation": "quantum-resistant-ledger",
    "dYdX": "dydx-chain", "Jupiter": "jupiter-exchange-solana",
    "Worldcoin": "worldcoin-wld", "TRON": "tron", "Litecoin": "litecoin",
    "Kaspa": "kaspa", "IOTA": "iota", "Canton": "canton",
    "Internet_Computer": "internet-computer", "Fetch_AI": "fetch-ai",
    "Injective": "injective-protocol", "XDC": "xdce-crowd-sale",
    "Ethereum_Classic": "ethereum-classic", "Quranium": "quranium",
    "QANplatform": "qanplatform", "Naoris": "naoris-protocol",
    "Midnight": "midnight-3", "Mantle": "mantle",
    "PancakeSwap": "pancakeswap-token",
    "SushiSwap": "sushi", "Curve": "curve-dao-token", "Lido": "lido-dao",
    "Bittensor": "bittensor", "Filecoin": "filecoin",
    "Flare": "flare-networks",
    "Nervos_Network": "nervos-network", "BitcoinCash": "bitcoin-cash",
}


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*"})
    ctx = None
    try:
        import ssl, certifi  # type: ignore
        ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        try:
            import ssl
            ctx = ssl.create_default_context()
        except Exception:
            ctx = None
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read(), r.headers.get_content_charset() or "utf-8"
    except Exception:
        # macOS system Python often lacks certs; curl uses the OS store
        import subprocess
        p = subprocess.run(
            ["curl", "-sS", "-L", "-A", UA, "--max-time", str(timeout), url],
            capture_output=True, check=False,
        )
        if p.returncode != 0:
            raise RuntimeError(p.stderr.decode("utf-8", "replace")[:300])
        return p.stdout, "utf-8"


def load_cache():
    try:
        return json.load(open(OUT))
    except Exception:
        return {}


def rows_to_projects(rows):
    projects = {}
    for r in rows:
        slug = r.get("slug")
        if not slug:
            continue
        stage = r.get("stage")
        try:
            stage = int(stage) if stage is not None else None
        except Exception:
            stage = None
        projects[slug] = {
            "slug": slug,
            "project_name": r.get("name") or slug,
            "symbol": r.get("symbol") or "",
            "qri_score": r.get("score"),
            "qri_stage": stage,
            "stage_label": r.get("stage_label") or STAGE_LABEL.get(stage or -1, ""),
            "project_type": r.get("type") or "",
            "canonical_url": r.get("url") or f"https://qrindex.org/projects/{slug}/",
            "evaluated": r.get("evaluated"),
            "confidence": r.get("confidence"),
            "review_status": r.get("review_status"),
            "summary": r.get("summary") or "",
            "rank": r.get("rank"),
        }
    return projects


def scrape_stdlib(enrich_slugs, enrich_cap=40):
    raw, enc = _get(INDEX)
    html = raw.decode(enc, "replace")
    os.makedirs(RAW, exist_ok=True)
    open(os.path.join(RAW, "index.html"), "w").write(html)
    rows = parse_index_html(html)
    # fill gaps from llms.txt index (plain text; still unofficial)
    try:
        llms_raw, enc2 = _get("https://qrindex.org/llms.txt")
        llms = parse_llms_index(llms_raw.decode(enc2, "replace"))
        by_slug = {r["slug"]: r for r in rows}
        for r in llms:
            cur = by_slug.get(r["slug"])
            if not cur:
                rows.append(r)
            else:
                if cur.get("score") is None:
                    cur["score"] = r.get("score")
                if cur.get("stage") is None:
                    cur["stage"] = r.get("stage")
                if not cur.get("stage_label"):
                    cur["stage_label"] = r.get("stage_label")
                if r.get("evaluated"):
                    cur["evaluated"] = r.get("evaluated")
                if r.get("confidence"):
                    cur["confidence"] = r.get("confidence")
                if r.get("name") and not cur.get("name"):
                    cur["name"] = r.get("name")
    except Exception as e:
        print(f"[qri] llms.txt index skipped ({e})", file=sys.stderr)

    projects = rows_to_projects(rows)
    # enrich tracked + stage-4 slugs via per-project llms.txt
    want = []
    for slug, p in projects.items():
        if (p.get("qri_stage") or 0) >= 4 or slug in set(MAP.values()):
            want.append(slug)
    want = list(dict.fromkeys(want))[:enrich_cap]
    for slug in want:
        url = f"https://qrindex.org/projects/{slug}/llms.txt"
        try:
            body, enc3 = _get(url, timeout=20)
            extra = parse_llms_project(body.decode(enc3, "replace"))
            p = projects[slug]
            if extra.get("score") is not None:
                p["qri_score"] = extra["score"]
            if extra.get("stage") is not None:
                p["qri_stage"] = extra["stage"]
                p["stage_label"] = extra.get("stage_label") or STAGE_LABEL.get(extra["stage"], p.get("stage_label"))
            for k in ("evaluated", "confidence", "review_status", "summary"):
                if extra.get(k):
                    p[k] = extra[k]
            time.sleep(0.15)
        except Exception:
            continue
    return projects, "stdlib-html"


def scrape_scrapy():
    try:
        from qri_spider import scrape_qrindex
    except Exception:
        return None, None
    got = scrape_qrindex()
    if not got:
        return None, None
    return rows_to_projects(list(got.values())), "scrapy"


def main():
    os.makedirs(DATA, exist_ok=True)
    cache = load_cache()
    projects, source = None, None
    try:
        projects, source = scrape_scrapy()
    except Exception as e:
        print(f"[qri] scrapy path skipped ({e})", file=sys.stderr)
        projects = None
    if not projects:
        try:
            projects, source = scrape_stdlib(set(MAP.values()))
        except Exception as e:
            print(f"[qri] HTML scrape failed ({e}); keeping cache", file=sys.stderr)
            if cache.get("projects"):
                print(f"[qri] cache has {len(cache['projects'])} projects")
                return 0
            return 1

    out = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": source,
        "parser_version": 1,
        "index_url": INDEX,
        "disclaimer": (
            "QRI is a third-party, AI-assisted, pre-release index scraped from qrindex.org. "
            "The site has no stable API; HTML and any JSON paths are expected to change. "
            "A QRI score is not a rating of market quality, adoption, or general merit, "
            "and is not a Bubble Map proof. Read with evaluation date, confidence, and blockers."
        ),
        "stage_labels": STAGE_LABEL,
        "map": MAP,
        "projects": projects,
        "n_projects": len(projects),
        "n_stage4": sum(1 for v in projects.values() if (v.get("qri_stage") or 0) >= 4),
    }
    json.dump(out, open(OUT, "w"), indent=2)
    print(f"wrote {OUT}  projects={out['n_projects']} stage4={out['n_stage4']} source={source}")
    qrl = projects.get("quantum-resistant-ledger") or {}
    print(f"  QRL  score={qrl.get('qri_score')} stage={qrl.get('qri_stage')}  {qrl.get('stage_label')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
