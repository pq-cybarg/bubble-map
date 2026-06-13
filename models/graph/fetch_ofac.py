#!/usr/bin/env python3
"""
fetch_ofac.py - env-FREE ingest of OFAC SDN crypto ("Digital Currency Address") entries for the
on-chain threat-actor block (research/spec-onchain-threat-actor-addresses.json).

Source: the OFAC SDN Advanced XML (sanctions.treasury.gov / ofac.treasury.gov), which carries
'Digital Currency Address - XBT/ETH/...' features on sanctioned parties. No API key needed.

Robust-by-pattern: rather than parse OFAC's full DistinctParty/Feature/ReferenceValueSet schema
(brittle, schema-versioned), this streams the XML and extracts strings that match known crypto
address shapes (BTC base58/bech32, ETH/EVM hex, TRON, XMR, etc.), deduped. That reliably answers
'which addresses are on the SDN list' for cross-referencing graph entities, and degrades gracefully:
on any network/parse failure it prints what is required and exits 0 (non-destructive), leaving the
block's address layer as the documented source-pointer rather than a fabricated list.
"""
import os, re, json, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
# Primary + fallback locations for the SDN Advanced XML (OFAC has migrated hosts over time).
URLS = [
    "https://sanctionslistservice.ofac.treas.gov/api/download/sdn_advanced.xml",
    "https://www.treasury.gov/ofac/downloads/sdn_advanced.xml",
    "https://ofac.treasury.gov/system/files/126/sdn_advanced.xml",
]
# Conservative crypto-address patterns (avoid false positives; tuned to OFAC's listed asset types).
PATTERNS = {
    "ETH/EVM": re.compile(r"\b0x[0-9a-fA-F]{40}\b"),
    "BTC": re.compile(r"\b(?:bc1[0-9ac-hj-np-z]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b"),
    "TRON": re.compile(r"\bT[1-9A-HJ-NP-Za-km-z]{33}\b"),
    "XMR": re.compile(r"\b4[0-9AB][0-9a-zA-Z]{93}\b"),
    "LTC": re.compile(r"\b(?:ltc1[0-9ac-hj-np-z]{11,71}|[LM][a-km-zA-HJ-NP-Z1-9]{26,33})\b"),
}

def _download():
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "ignore"), url
        except Exception as e:
            print(f"  ! {url} -> {e}")
    return None, None

def main():
    text, src = _download()
    if not text:
        print("fetch_ofac.py: SDN Advanced XML unreachable - skipping (non-destructive).")
        print("  The on-chain block cites the OFAC SDN 'Digital Currency Address' set as the")
        print("  authoritative source; re-run when sanctionslistservice.ofac.treas.gov is reachable.")
        return 0
    # Sanity-check we actually got the SDN XML (not an error/redirect page).
    if not re.search(r"sdn|DistinctParty|sanction|FeatureType", text, re.I) or len(text) < 50000:
        print(f"fetch_ofac.py: downloaded content does not look like the SDN XML "
              f"(len={len(text)}) - skipping (non-destructive).")
        return 0
    # In the Advanced XML the address VALUES live in Feature/VersionDetail elements, not next to
    # the literal label, so scan the whole document with strict address patterns. The patterns are
    # specific enough (0x+40hex; BTC base58/bech32; TRON/XMR/LTC) that structured XML IDs/UUIDs
    # don't match. Restrict to text inside XML element values to further cut noise.
    vals = re.findall(r">([^<>]{20,120})<", text)
    scan = "\n".join(v for v in vals if any(c.isalnum() for c in v))
    if len(scan) < 1000:  # element-value extraction failed; fall back to whole doc
        scan = text
    found = {}
    for kind, pat in PATTERNS.items():
        for a in set(pat.findall(scan)):
            found.setdefault(a, kind)
    out = {"metadata": {"source": src, "note": "Addresses present on the OFAC SDN list "
            "('Digital Currency Address' features), pattern-extracted. For authoritative party "
            "attribution, resolve each against the full SDN entry.", "count": len(found)},
           "addresses": [{"address": a, "asset_guess": k} for a, k in sorted(found.items())]}
    path = os.path.join(DATA, "ofac_crypto_addresses.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(found)} SDN crypto addresses from {src})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
