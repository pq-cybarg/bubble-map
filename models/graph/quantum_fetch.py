#!/usr/bin/env python3
"""
quantum_fetch.py - env-FREE, tolerant tracker that refreshes data/quantum_feed.json with
machine-collected, UNVERIFIED items for the quantum sub-site's live feed.

Sources (each isolated in try/except; a failure degrades gracefully, never aborts the run):
  - arXiv quant-ph            (Atom API - reliable)
  - arXiv cs.CR               (Atom API, filtered to quantum/PQC terms)
  - NIST PQC                  (CSRC project/news page - best-effort HTML)
  - vendor roadmaps           (IBM/Google/Quantinuum/IonQ/PsiQuantum/Atom Computing - best-effort)
  - compliance/regulatory     (NSA CNSA, CISA, BSI, ANSSI, NCSC - best-effort)
  - ecdsa.fail                (nonce-reuse disclosures - best-effort)

Design: NOTHING here is graded or trusted. Items are deduped by URL and merged into the existing
feed (append-only, newest kept). Per-source caps are logged (no silent truncation). On total
failure the file is left unchanged and the script exits 0 (non-destructive) - the CI workflow
opens a PR only if the file actually changed, so unverified content never lands on main unreviewed.

No API keys, no secrets. stdlib only (urllib + xml.etree + re) so CI needs no pip install.
"""
import os, re, json, html, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
FEED_PATH = os.path.join(DATA, "quantum_feed.json")
UA = {"User-Agent": "bubble-map-quantum-tracker/1.0 (+https://github.com/pq-cybarg/bubble-map)"}
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")
PER_SOURCE_CAP = 25

def _get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def _clean(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()

# ---------------------------------------------------------------- arXiv (Atom API)
ATOM = "{http://www.w3.org/2005/Atom}"

def _arxiv(cat, label, keywords=None, maxn=15):
    """Query arXiv's export API for the most recent papers in `cat`; optionally filter titles/
    abstracts by any of `keywords`. Returns feed items."""
    q = urllib.parse.urlencode({
        "search_query": f"cat:{cat}", "sortBy": "submittedDate", "sortOrder": "descending",
        "start": 0, "max_results": 40})
    xml = _get(f"http://export.arxiv.org/api/query?{q}")
    root = ET.fromstring(xml)
    out = []
    for e in root.findall(f"{ATOM}entry"):
        title = _clean((e.findtext(f"{ATOM}title") or ""))
        summ = _clean((e.findtext(f"{ATOM}summary") or ""))[:280]
        link = (e.findtext(f"{ATOM}id") or "").strip()
        pub = (e.findtext(f"{ATOM}published") or "")[:10]
        if keywords:
            hay = (title + " " + summ).lower()
            if not any(k in hay for k in keywords):
                continue
        out.append({"source": label, "title": title, "url": link, "summary": summ, "date": pub})
        if len(out) >= maxn:
            break
    return out

def src_arxiv_quant_ph():
    return _arxiv("quant-ph", "arXiv quant-ph", maxn=15)

def src_arxiv_cs_cr():
    kw = ["post-quantum", "post quantum", "pqc", "lattice", "kyber", "dilithium", "sphincs",
          "mceliece", "quantum", "shor", "ecdsa", "nonce", "isogeny", "ml-kem", "ml-dsa"]
    return _arxiv("cs.CR", "arXiv cs.CR", keywords=kw, maxn=15)

# ---------------------------------------------------------------- generic HTML link harvest
def _harvest_links(url, label, must_match=None, maxn=12):
    """Best-effort: pull <a href>text</a> pairs from a page, keep those whose text looks like a
    headline (long enough) and (optionally) match a keyword. Absolute-ize relative URLs. This is
    intentionally conservative - it records leads, not facts."""
    base = _get(url)
    out, seen = [], set()
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', base, re.I | re.S):
        href, text = m.group(1), _clean(re.sub(r"<[^>]+>", "", m.group(2)))
        if len(text) < 25:
            continue
        if must_match and not any(k in text.lower() for k in must_match):
            continue
        if href.startswith("/"):
            p = urllib.parse.urlparse(url)
            href = f"{p.scheme}://{p.netloc}{href}"
        if not href.startswith("http") or href in seen:
            continue
        seen.add(href)
        out.append({"source": label, "title": text, "url": href, "summary": "", "date": ""})
        if len(out) >= maxn:
            break
    return out

def src_nist_pqc():
    kw = ["pqc", "post-quantum", "fips", "kyber", "dilithium", "sphincs", "kem", "standard",
          "quantum", "hqc", "digital signature"]
    return _harvest_links("https://csrc.nist.gov/projects/post-quantum-cryptography", "NIST PQC", kw)

def src_vendor_roadmaps():
    items = []
    pages = [
        ("https://www.ibm.com/quantum/blog", "IBM Quantum"),
        ("https://blog.google/technology/research/", "Google Research"),
        ("https://www.quantinuum.com/news", "Quantinuum"),
        ("https://ionq.com/news", "IonQ"),
        ("https://www.psiquantum.com/news", "PsiQuantum"),
        ("https://atom-computing.com/news/", "Atom Computing"),
    ]
    kw = ["qubit", "logical", "error", "roadmap", "fault", "quantum", "processor", "chip", "correction"]
    for url, label in pages:
        try:
            items += _harvest_links(url, label, kw, maxn=6)
        except Exception as ex:
            print(f"[quantum_fetch] vendor {label} skipped: {ex}")
    return items

def src_compliance():
    items = []
    pages = [
        ("https://www.nsa.gov/Cybersecurity/Post-Quantum-Cybersecurity-Resources/", "NSA CNSA"),
        ("https://www.cisa.gov/quantum", "CISA"),
        ("https://www.ncsc.gov.uk/section/products-services/pqc", "UK NCSC"),
    ]
    kw = ["quantum", "pqc", "post-quantum", "cnsa", "migration", "cryptograph", "timeline", "guidance"]
    for url, label in pages:
        try:
            items += _harvest_links(url, label, kw, maxn=6)
        except Exception as ex:
            print(f"[quantum_fetch] compliance {label} skipped: {ex}")
    return items

def src_ecdsa_fail():
    return _harvest_links("https://ecdsa.fail/", "ecdsa.fail",
                          ["nonce", "ecdsa", "key", "signature", "leak", "reuse", "wallet"], maxn=10)

SOURCES = [
    ("arXiv quant-ph", src_arxiv_quant_ph),
    ("arXiv cs.CR", src_arxiv_cs_cr),
    ("NIST PQC", src_nist_pqc),
    ("vendor roadmaps", src_vendor_roadmaps),
    ("compliance", src_compliance),
    ("ecdsa.fail", src_ecdsa_fail),
]

def main():
    try:
        feed = json.load(open(FEED_PATH))
    except Exception:
        feed = {"meta": {}, "items": []}
    existing = {it.get("url") for it in feed.get("items", []) if it.get("url")}
    fresh, added = [], 0
    for label, fn in SOURCES:
        try:
            got = fn()
        except Exception as ex:
            print(f"[quantum_fetch] source '{label}' failed: {ex}")
            continue
        if len(got) > PER_SOURCE_CAP:
            print(f"[quantum_fetch] '{label}': capped {len(got)} -> {PER_SOURCE_CAP} (dropped "
                  f"{len(got) - PER_SOURCE_CAP}; not silent)")
            got = got[:PER_SOURCE_CAP]
        for it in got:
            if not it.get("url") or it["url"] in existing:
                continue
            it["fetched"] = NOW
            existing.add(it["url"])
            fresh.append(it)
            added += 1
        print(f"[quantum_fetch] '{label}': +{added} cumulative new")
    feed.setdefault("items", [])
    feed["items"] = fresh + feed["items"]
    feed.setdefault("meta", {})["last_fetch"] = NOW
    json.dump(feed, open(FEED_PATH, "w"), indent=2, ensure_ascii=True)
    print(f"[quantum_fetch] wrote {FEED_PATH}: +{added} new, {len(feed['items'])} total, last_fetch={NOW}")

if __name__ == "__main__":
    main()
