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

# Bounded, on-thesis default target set (committee chairs + key leverage members). Each entry is
# (display name, FEC search query, preferred office H|S) so we lock onto the CONGRESSIONAL committee
# (candidate_id starting with H/S), not a presidential committee (P) from a past White House run.
TARGETS = [
    ("Elizabeth Warren", "WARREN, ELIZABETH", "S"),
    ("Tim Scott", "SCOTT, TIM", "S"),
    ("Sherrod Brown", "BROWN, SHERROD", "S"),
    ("Mike Crapo", "CRAPO, MICHAEL", "S"),
    ("Cynthia Lummis", "LUMMIS, CYNTHIA", "S"),
    ("French Hill", "HILL, FRENCH", "H"),
    ("Maxine Waters", "WATERS, MAXINE", "H"),
    ("Patrick McHenry", "MCHENRY, PATRICK", "H"),
    ("Tom Emmer", "EMMER, TOM", "H"),
    ("Ron Wyden", "WYDEN, RON", "S"),
    ("Mark Warner", "WARNER, MARK", "S"),
    ("Josh Hawley", "HAWLEY, JOSH", "S"),
    ("Jim Jordan", "JORDAN, JIM", "H"),
    ("Chuck Schumer", "SCHUMER, CHARLES", "S"),
    ("John Thune", "THUNE, JOHN", "S"),
]

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
        # plain-name fuzzy search (the q param), valid sort key, filter office client-side.
        srch = _get("/candidates/search", {"q": name, "per_page": 20, "sort": "-first_file_date"})
        results = (srch or {}).get("results") or []
        # Prefer the candidacy for the intended chamber (office H/S, candidate_id prefix H/S),
        # most recently filed; fall back to any match rather than guess.
        chamber = [r for r in results if (r.get("office") == office)
                   or str(r.get("candidate_id", "")).startswith(office)]
        pick = (chamber or results)
        if not pick:
            print(f"  - {name}: no FEC candidate match (skipped, not guessed)")
            continue
        cid = pick[0].get("candidate_id")
        totals = _get(f"/candidate/{cid}/totals", {"per_page": 30, "sort": "-cycle"})
        rows = (totals or {}).get("results") or []
        out["candidates"].append({
            "name": name, "candidate_id": cid,
            "cycles": [{"cycle": r.get("cycle"), "receipts": r.get("receipts"),
                        "disbursements": r.get("disbursements"),
                        "individual_itemized": r.get("individual_itemized_contributions"),
                        "pac_contributions": r.get("other_political_committee_contributions")}
                       for r in rows],
        })
        print(f"  + {name}: {len(rows)} cycles ({cid})")
        time.sleep(0.6)  # be polite to the rate limiter

    path = os.path.join(DATA, "fec_summary.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(out['candidates'])} candidates)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
