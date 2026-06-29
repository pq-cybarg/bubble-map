#!/usr/bin/env python3
"""
build_leadership.py  (#117) — the leadership-map ingestion pipeline.

SEPARATE from the investigative funding graph: it does NOT read research/*.json or write
data/graph.json, so it can never affect the formally-verified SCC. It ingests curated/bulk
source files from data/leadership/sources/ and emits:
  - data/leadership/leadership.json   (normalized + deduped records + stats)
  - docs/leadership.html              (browsable point-in-time directory)

Run standalone:  python3 models/leadership/build_leadership.py
(Intentionally NOT wired into scripts/new-research.sh — leadership updates stay decoupled
 from the graph gate.)

Ingestion contract (see models/leadership/SCHEMA.md):
  *.json  -> a list of records already matching the schema.
  legislators-current.csv -> the open @unitedstates/congress-legislators roster (all 535);
            columns last_name/first_name/type(sen|rep)/state/party/... are auto-mapped.
"""
import json, os, glob, csv, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC  = os.path.join(ROOT, "data", "leadership", "sources")
OUT_JSON = os.path.join(ROOT, "data", "leadership", "leadership.json")
OUT_HTML = os.path.join(ROOT, "docs", "leadership.html")

REQUIRED = ["id", "person", "role", "jurisdiction", "branch", "level", "status", "as_of", "source_url", "source_dataset"]
VALID_BRANCH = {"executive","legislative","judicial","independent","military","law_enforcement","state","local"}
VALID_LEVEL  = {"federal","state","county","municipal","special_district"}

def slug(s):
    return re.sub(r"[^a-z0-9]+","-", (s or "").lower()).strip("-")

def load_json_sources():
    recs=[]
    for fn in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        try:
            data=json.load(open(fn))
        except Exception as e:
            print(f"[leadership] WARN bad json {os.path.basename(fn)}: {e}"); continue
        if isinstance(data, list):
            recs.extend(data)
        else:
            print(f"[leadership] WARN {os.path.basename(fn)} is not a list; skipped")
    return recs

def load_congress_csv():
    """Auto-ingest the @unitedstates/congress-legislators 'legislators-current.csv' if present."""
    recs=[]
    for fn in glob.glob(os.path.join(SRC, "legislators-current.csv")):
        try:
            rows=list(csv.DictReader(open(fn, newline="", encoding="utf-8")))
        except Exception as e:
            print(f"[leadership] WARN bad csv {os.path.basename(fn)}: {e}"); continue
        for r in rows:
            typ=(r.get("type") or "").strip().lower()
            first=(r.get("first_name") or "").strip(); last=(r.get("last_name") or "").strip()
            name=(r.get("full_name") or "").strip() or (first+" "+last).strip()  # prefer full_name (middle/suffix/nickname)
            if not name: continue
            is_sen = typ=="sen"
            bioguide=(r.get("bioguide_id") or r.get("bioguide") or slug(name)).strip()
            st=(r.get("state") or "").strip()
            party=(r.get("party") or "").strip()
            party={"Democrat":"Democratic"}.get(party, party)  # normalize to seed-file convention
            recs.append({
                "id": "congress-"+bioguide,
                "person": name,
                "role": ("U.S. Senator" if is_sen else "U.S. Representative") + (f" ({st}-{r.get('district')})" if (not is_sen and r.get('district')) else (f" ({st})" if st else "")),
                "jurisdiction": "U.S. Senate" if is_sen else "U.S. House of Representatives",
                "branch": "legislative", "level": "federal", "status": "incumbent",
                "party": party,
                "as_of": "from-dataset",
                "source_url": "https://github.com/unitedstates/congress-legislators",
                "source_dataset": "congress-legislators",
            })
    return recs

def validate(recs):
    seen={}; clean=[]; warns=0
    for r in recs:
        miss=[k for k in REQUIRED if not r.get(k)]
        if miss:
            print(f"[leadership] WARN record missing {miss}: {r.get('person') or r.get('id')}"); warns+=1
            continue
        if r["branch"] not in VALID_BRANCH: print(f"[leadership] WARN bad branch '{r['branch']}' ({r['person']})"); warns+=1
        if r["level"]  not in VALID_LEVEL:  print(f"[leadership] WARN bad level '{r['level']}' ({r['person']})"); warns+=1
        rid=r["id"]
        if rid in seen:  # dedupe on id; keep first
            continue
        seen[rid]=1; clean.append(r)
    return clean, warns

def esc(s): return html.escape(str(s or ""))

def build_html(recs, by_branch, by_level, current_as_of):
    css="body{background:#faf8f2;color:#1c1b19;font:16px/1.6 Georgia,'Iowan Old Style','Times New Roman',serif;margin:0;padding:0 0 60px}main{max-width:900px;margin:0 auto;padding:0 22px}h1{font-family:Georgia,serif;font-weight:600;font-size:32px;margin:26px 0 4px}h2{color:#7b2d26;border-bottom:1px solid #e4ddcc;padding-bottom:6px;margin-top:30px;font-size:22px}h3{font-size:17px;margin:18px 0 4px;color:#33312c}a{color:#1f4e79}.muted{color:#6b665d;font-size:14px}table{border-collapse:collapse;width:100%;margin:8px 0 18px;font:14px/1.45 -apple-system,Segoe UI,Roboto,sans-serif}th,td{border-bottom:1px solid #e9e2d2;padding:6px 9px;text-align:left;vertical-align:top}th{color:#7b2d26}.s-incumbent{color:#2e6b2e}.s-acting{color:#b8860b}.s-former{color:#a33;text-decoration:line-through}.s-nominated{color:#1f4e79}.pill{font:11px sans-serif;background:#f2ede0;border:1px solid #e4ddcc;border-radius:10px;padding:1px 7px;color:#6b3b16}"
    rows_by = {}
    for r in recs:
        rows_by.setdefault((r["level"], r["branch"]), []).append(r)
    order_level=["federal","state","county","municipal","special_district"]
    order_branch=["executive","legislative","judicial","independent","military","law_enforcement","state","local"]
    parts=[f"<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Leadership map</title><style>{css}</style></head><body><main>"]
    parts.append("<h1>Leadership map</h1>")
    parts.append(f"<p class=muted>A point-in-time directory of officeholders (current as of <b>{esc(current_as_of)}</b>). "
                 f"{len(recs)} records across {len(by_level)} levels. Separate overlay — NOT part of the formally-verified funding graph. "
                 f"Every record carries a source. Roles churn; <span class=s-acting>acting</span> / <span class=s-former>former</span> are marked. "
                 f"<a href='index.html'>&larr; back to the map</a></p>")
    counts=" &middot; ".join(f"{esc(k)}: <b>{v}</b>" for k,v in sorted(by_branch.items(), key=lambda x:-x[1]))
    parts.append(f"<p class=muted>By branch: {counts}</p>")
    for lvl in order_level:
        lvl_rows=[(b,rows_by.get((lvl,b),[])) for b in order_branch if rows_by.get((lvl,b))]
        if not lvl_rows: continue
        parts.append(f"<h2>{esc(lvl.capitalize())}</h2>")
        for br, rs in lvl_rows:
            parts.append(f"<h3>{esc(br.replace('_',' ').capitalize())} <span class=muted>({len(rs)})</span></h3>")
            parts.append("<table><tr><th>Office</th><th>Person</th><th>Party</th><th>Since</th><th>Status</th><th>Source</th></tr>")
            for r in sorted(rs, key=lambda x:(x.get("jurisdiction",""), x.get("role",""))):
                st=r.get("status","")
                note=f"<br><span class=muted><i>{esc(r['note'])}</i></span>" if r.get("note") else ""
                since=esc(r.get("start","")) + (f" &ndash; {esc(r['end'])}" if r.get("end") else "")
                parts.append(
                    f"<tr><td>{esc(r['role'])}<br><span class=muted>{esc(r['jurisdiction'])}</span>{note}</td>"
                    f"<td>{esc(r['person'])}</td><td>{esc(r.get('party',''))}</td>"
                    f"<td>{since}</td>"
                    f"<td class=s-{esc(st)}>{esc(st)}</td>"
                    f"<td><a href='{esc(r['source_url'])}' rel=nofollow>src</a></td></tr>")
            parts.append("</table>")
    parts.append("</main></body></html>")
    return "".join(parts)

def main():
    recs = load_json_sources() + load_congress_csv()
    recs, warns = validate(recs)
    by_branch={}; by_level={}
    for r in recs:
        by_branch[r["branch"]]=by_branch.get(r["branch"],0)+1
        by_level[r["level"]]=by_level.get(r["level"],0)+1
    current_as_of=max([r["as_of"] for r in recs if r.get("as_of") and r["as_of"]!="from-dataset"] or ["n/a"])
    out={"generated_from":"data/leadership/sources/","count":len(recs),"current_as_of":current_as_of,
         "by_branch":by_branch,"by_level":by_level,"records":recs}
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(out, open(OUT_JSON,"w"), ensure_ascii=False, indent=1)
    open(OUT_HTML,"w").write(build_html(recs, by_branch, by_level, current_as_of))
    print(f"[LEADERSHIP] {len(recs)} records | by_level={by_level} | by_branch={by_branch} | warns={warns} | as_of={current_as_of}")

if __name__=="__main__":
    main()
