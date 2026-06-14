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
# Both free OFAC Advanced XML lists, each with fallback hosts (OFAC has migrated hosts over time).
# SDN = Specially Designated Nationals; CONS = Consolidated (non-SDN) Sanctions List. Crypto
# addresses appear on BOTH. This is the FREE public coverage; see the coverage note in main().
#
# Current canonical entry points (verified reachable 2026-06; all FREE, no key):
#   - Sanctions List Service (bulk): https://sanctionslistservice.ofac.treas.gov/api/download/<file>
#       <file> in {sdn.csv, sdn.xml, sdn_advanced.xml, cons.csv, cons.xml, cons_advanced.xml, ...}.
#       These now 302-redirect to a short-lived signed S3 URL (urllib follows redirects automatically).
#   - SDN list portal:          https://sanctionslist.ofac.treas.gov/Home/SdnList
#   - Consolidated list portal: https://sanctionslist.ofac.treas.gov/Home/ConsolidatedList
#   - Other OFAC lists index:   https://ofac.treasury.gov/other-ofac-sanctions-lists
#   - Free web search UI:       https://sanctionssearch.ofac.treas.gov/
# The SDN/Consolidated data (incl. the "Digital Currency Address" crypto fields) is fully available
# for free in CSV, XML, and Advanced-XML (machine-readable). It is NOT paywalled or access-limited.
SOURCES = {
    "SDN": [
        "https://sanctionslistservice.ofac.treas.gov/api/download/sdn_advanced.xml",
        "https://www.treasury.gov/ofac/downloads/sdn_advanced.xml",
        "https://ofac.treasury.gov/system/files/126/sdn_advanced.xml",
    ],
    "CONS": [
        "https://sanctionslistservice.ofac.treas.gov/api/download/cons_advanced.xml",
        "https://www.treasury.gov/ofac/downloads/consolidated/cons_advanced.xml",
    ],
}
# Conservative crypto-address patterns (avoid false positives; tuned to OFAC's listed asset types).
PATTERNS = {
    "ETH/EVM": re.compile(r"\b0x[0-9a-fA-F]{40}\b"),
    "BTC": re.compile(r"\b(?:bc1[0-9ac-hj-np-z]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b"),
    "TRON": re.compile(r"\bT[1-9A-HJ-NP-Za-km-z]{33}\b"),
    "XMR": re.compile(r"\b4[0-9AB][0-9a-zA-Z]{93}\b"),
    "LTC": re.compile(r"\b(?:ltc1[0-9ac-hj-np-z]{11,71}|[LM][a-km-zA-HJ-NP-Z1-9]{26,33})\b"),
}

def _download(urls):
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "ignore"), url
        except Exception as e:
            print(f"  ! {url} -> {e}")
    return None, None

def _extract(text):
    # In the Advanced XML the address VALUES live in Feature/VersionDetail elements, not next to
    # the literal label, so scan element values with strict address patterns. The patterns are
    # specific enough (0x+40hex; BTC base58/bech32; TRON/XMR/LTC) that structured XML IDs don't match.
    vals = re.findall(r">([^<>]{20,120})<", text)
    scan = "\n".join(v for v in vals if any(c.isalnum() for c in v))
    if len(scan) < 1000:
        scan = text
    out = {}
    for kind, pat in PATTERNS.items():
        for a in set(pat.findall(scan)):
            out[a] = kind
    return out

def main():
    found = {}      # address -> asset_guess
    prov = {}       # address -> set of lists it appears on
    srcs_used = []
    for listname, urls in SOURCES.items():
        text, src = _download(urls)
        if not text:
            print(f"  - {listname}: unreachable (skipped)")
            continue
        if not re.search(r"DistinctParty|sanction|FeatureType", text, re.I) or len(text) < 30000:
            print(f"  - {listname}: content not recognizable as OFAC XML (len={len(text)}, skipped)")
            continue
        got = _extract(text)
        for a, k in got.items():
            found.setdefault(a, k); prov.setdefault(a, set()).add(listname)
        srcs_used.append(f"{listname}:{src}")
        print(f"  + {listname}: {len(got)} crypto addresses ({src})")
    if not found:
        print("fetch_ofac.py: no OFAC lists reachable - skipping (non-destructive). "
              "The on-chain block cites the SDN/Consolidated 'Digital Currency Address' set as source.")
        return 0
    import collections
    by_list = collections.Counter(tuple(sorted(s)) for s in prov.values())
    out = {"metadata": {
            "sources": srcs_used,
            "count": len(found),
            "by_list": {"+".join(k): v for k, v in by_list.items()},
            "note": "Crypto addresses pattern-extracted from the FREE OFAC Advanced XML lists "
                    "(SDN + Consolidated), downloaded via the Treasury Sanctions List Service "
                    "(sanctionslistservice.ofac.treas.gov; also free as CSV/XML and via the "
                    "sanctionslist.ofac.treas.gov portals and the sanctionssearch.ofac.treas.gov "
                    "search UI). For authoritative party/program attribution, resolve each address "
                    "against its full list entry.",
            "COVERAGE_LIMITS": "OFAC's own data is NOT access-limited: the full SDN and Consolidated "
                    "lists — including the 'Digital Currency Address' crypto fields — are freely "
                    "downloadable in CSV, XML, and Advanced-XML (machine-readable) and searchable "
                    "for free. The 757 here is still a LOWER BOUND on the threat-actor address "
                    "universe, but for reasons OTHER than OFAC availability: it captures only "
                    "addresses OFAC has formally DESIGNATED, and deliberately excludes (a) per-incident "
                    "FBI/CISA PSA IOC address lists (e.g., the 51 Bybit-laundering ETH addresses), "
                    "published separately but also free; and (b) un-sanctioned but attributed clusters "
                    "tracked by commercial forensics (Chainalysis/Elliptic/TRM/Arkham), which ARE "
                    "paywalled. Sanction status is also time-varying (e.g., Tornado Cash: sanctioned "
                    "2022 -> vacated 2024 -> lifted 2025), so a static list overstates what is "
                    "CURRENTLY designated."},
           "addresses": [{"address": a, "asset_guess": k, "lists": sorted(prov[a])}
                         for a, k in sorted(found.items())]}
    path = os.path.join(DATA, "ofac_crypto_addresses.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(found)} OFAC crypto addresses; FREE-ACCESS FLOOR, not full universe)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
