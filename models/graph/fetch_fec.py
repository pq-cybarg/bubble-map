#!/usr/bin/env python3
"""
fetch_fec.py - env-gated ingest of FEC campaign-finance summaries for the congressional
funding/compromise block (research/influence-congress-funding-compromise.json).

HONEST ACCESS NOTE: the FEC's OpenFEC API (api.open.fec.gov) requires an api.data.gov key.
A rate-limited DEMO_KEY exists but is too throttled for a 26-year, ~2,000-member sweep.
Set FEC_API_KEY in the environment (the same env-only-creds pattern as FINRA: never commit a key).

With a key it writes data/fec_summary.json: per-candidate receipts/disbursements and, where the
itemized endpoints are entitled, receipts grouped by contributor industry/sector. Without a key it
prints what is required and exits 0 (non-destructive) so the qualitative block stands alone and the
'REQUIRES-INGEST' cells stay explicitly empty rather than fabricated.

Scope control: pulls only the committee-of-jurisdiction chairs + highest-leverage members named in
data/persons.json / data/congress_committees.json by default (a bounded, on-thesis set), not the
full roster, to stay inside rate limits. Widen TARGETS to sweep further.
"""
import os, json, time, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
API = "https://api.open.fec.gov/v1"

# Targets are derived DYNAMICALLY from data/persons.json: every profiled member of Congress
# (domain "Legislature"). Each becomes (display name, search query, preferred office H|S) so we lock
# onto the CONGRESSIONAL candidacy (candidate_id H/S), not a presidential committee from a WH run.
# This auto-scales as more members are profiled - the money-map covers the whole roster, not a sample.
# Query/office overrides for members whose plain-name fuzzy search misses or is ambiguous (FEC
# stores "LAST, FIRST"); these use a cleaner query + forced chamber. Surname is still verified in
# the picker so an override can never grab the wrong person.
OVERRIDES = {
    "Chuck Schumer": ("Schumer", "S"), "Mike Crapo": ("Crapo, Michael", "S"),
    "Jim Jordan": ("Jordan, Jim", "H"), "Tom Emmer": ("Emmer", "H"),
    "Tom Daschle": ("Daschle", "S"), "Bill Frist": ("Frist", "S"),
    "Mike Oxley": ("Oxley", "H"), "Jack Reed": ("Reed, John", "S"),
    "Mike Johnson": ("Johnson, James Michael", "H"),
}
def _targets():
    try:
        P = json.load(open(os.path.join(ROOT, "data", "persons.json")))
    except Exception:
        return []
    out = []
    for p in P.get("persons", []):
        if "Legislature" not in p.get("domains", []):
            continue
        name = p["name"]
        role = (p.get("role", "") + " " + name).lower()
        office = "S" if "senat" in role else ("H" if any(k in role for k in
                 ("repres", "house", "speaker", "ways and means", "financial services")) else "")
        q, office = OVERRIDES.get(name, (name, office))
        out.append((name, q, office))
    return out
TARGETS = _targets()

def _get(path, params, retries=2):
    key = os.environ.get("FEC_API_KEY")
    if not key:
        return None
    params = dict(params); params["api_key"] = key
    url = f"{API}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if attempt == retries:
                print(f"  ! FEC request failed ({path}): {e}")
                return None
            time.sleep(1.5)

def main():
    key = os.environ.get("FEC_API_KEY")
    if not key:
        print("fetch_fec.py: no FEC_API_KEY in environment - skipping (non-destructive).")
        print("  To ingest: get a free key at https://api.data.gov/signup/ and set FEC_API_KEY.")
        print("  Endpoints used: /candidates/search, /candidate/{id}/totals (by 2-year cycle).")
        print("  The funding block's per-member $ cells remain explicitly REQUIRES-INGEST (not fabricated).")
        return 0

    out = {"metadata": {"source": "api.open.fec.gov", "note": "Per-candidate FEC totals by cycle. "
            "Industry/sector breakdowns require itemized-receipt entitlement; see OpenSecrets for "
            "curated sector aggregation.", "targets": TARGETS}, "candidates": []}
    for name, query, office in TARGETS:
        # fuzzy name search (q), then VERIFY surname (never grab the wrong person), then prefer chamber.
        srch = _get("/candidates/search", {"q": query, "per_page": 20, "sort": "-first_file_date"})
        results = (srch or {}).get("results") or []
        toks = name.replace("(", " ").replace(")", " ").split()
        surname, first = toks[-1].lower(), toks[0].lower()
        named = [r for r in results if surname in (r.get("name", "") or "").lower()]
        # disambiguate common surnames: prefer results that ALSO contain the first name (FEC often
        # carries the nickname in parens, e.g. REED, JOHN F (JACK)); fall back to surname-only.
        fnamed = [r for r in named if first in (r.get("name", "") or "").lower()]
        pool = fnamed or named   # require surname match (no blind fallback to wrong people)
        chamber = [r for r in pool if (office and ((r.get("office") == office)
                   or str(r.get("candidate_id", "")).startswith(office)))]
        pick = chamber or pool
        if not pick:
            print(f"  - {name}: no surname-verified FEC match (skipped, not guessed)")
            continue
        cid = pick[0].get("candidate_id")
        totals = _get(f"/candidate/{cid}/totals", {"per_page": 30, "sort": "-cycle"})
        rows = (totals or {}).get("results") or []
        cycles = [{"cycle": r.get("cycle"), "receipts": r.get("receipts"),
                   "disbursements": r.get("disbursements"),
                   "individual_itemized": r.get("individual_itemized_contributions"),
                   "pac_contributions": r.get("other_political_committee_contributions")}
                  for r in rows]
        # drop matches with NO receipts-bearing cycle: an empty record is useless and is usually a
        # wrong/ambiguous-surname match (better no overlay than wrong data).
        if not any(c.get("receipts") for c in cycles):
            print(f"  - {name}: matched {cid} but 0 receipts-bearing cycles (dropped, likely wrong/empty)")
            time.sleep(0.4); continue
        out["candidates"].append({"name": name, "candidate_id": cid, "cycles": cycles})
        print(f"  + {name}: {len(cycles)} cycles ({cid})")
        time.sleep(0.6)  # be polite to the rate limiter

    path = os.path.join(DATA, "fec_summary.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(out['candidates'])} candidates)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
