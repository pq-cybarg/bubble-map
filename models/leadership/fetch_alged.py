#!/usr/bin/env python3
"""
fetch_alged.py - download the American Local Government Elections Database (ALGED) into
data/leadership/sources/ so build_leadership.load_alged() can ingest it.

Source: de Benedictis-Kessner, Lee, Velez & Warshaw, "American Local Government Elections
Database", Scientific Data 10:912 (2023). OSF DOI 10.17605/OSF.IO/MV5E6, CC-BY-NC-SA 4.0.
Provenance + bias/confidence audit: research/leadership-county-sources.md.

Network-tolerant (mirrors the models/graph/fetch_*.py pattern): if OSF is unreachable it prints
a notice and exits 0 so the build still passes. The OSF project GUID is 'mv5e6'; the OSF API is
queried for the osfstorage file list and each CSV is saved as alged_<name>.csv. Some sandboxed
environments block OSF egress - in that case download the file manually from
https://osf.io/mv5e6/ and drop it in data/leadership/sources/ as alged*.csv.

Run:  python3 models/leadership/fetch_alged.py
"""
import os, sys, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC  = os.path.join(ROOT, "data", "leadership", "sources")
API  = "https://api.osf.io/v2/nodes/mv5e6/files/osfstorage/?page%5Bsize%5D=100"
UA   = {"User-Agent": "bubble-map-leadership-etl/1.0 (+research; noncommercial)"}

def _get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def main():
    os.makedirs(SRC, exist_ok=True)
    try:
        manifest = json.loads(_get(API))
    except Exception as e:
        print(f"[fetch_alged] OSF unreachable ({e.__class__.__name__}: {e}); skipping. "
              f"Manual: download from https://osf.io/mv5e6/ -> {SRC}/alged*.csv")
        return 0
    saved = 0
    for f in manifest.get("data", []):
        a = f.get("attributes", {})
        if a.get("kind") != "file":
            continue
        name = (a.get("name") or "").strip()
        if not name.lower().endswith(".csv"):
            continue  # only the tabular returns; skip docs/dta/zip here
        dl = (f.get("links") or {}).get("download")
        if not dl:
            continue
        out = os.path.join(SRC, "alged_" + name if not name.lower().startswith("alged") else name)
        try:
            data = _get(dl)
            open(out, "wb").write(data)
            saved += 1
            print(f"[fetch_alged] saved {os.path.basename(out)} ({len(data):,} bytes)")
        except Exception as e:
            print(f"[fetch_alged] WARN could not download {name}: {e}")
    if not saved:
        print("[fetch_alged] no CSV files found/saved; nothing ingested (build still passes).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
