# Leadership map — schema + ingestion pipeline (#117)

A **separate subsystem** from the investigative funding graph. It does **not** touch `research/*.json`,
`models/graph/build_graph.py`, or `data/graph.json` — so it can never bloat or break the formally-verified
SCC (which must stay `core_scc_all=12 / core_scc_robust=11`). Leadership data lives in its own files and
renders to its own page (`docs/leadership.html`). It is a **point-in-time directory**, not a proof input.

## Why separate

"Every official at every level" (federal → state → ~3,143 counties → ~18,000 police departments → school
boards) is potentially hundreds of thousands of records. Folding that into the SCC graph would swamp the
investigation's character and the proofs. So leadership is an **overlay directory** with its own builder.

## Pipeline

```
data/leadership/sources/*.json   (curated, sourced record lists)
data/leadership/sources/*.csv    (bulk authoritative datasets, e.g. @unitedstates congress-legislators)
        │
        ▼  models/leadership/build_leadership.py   (stdlib only)
        │
data/leadership/leadership.json  (normalized + deduped records + stats)
docs/leadership.html             (browsable directory, grouped by branch/level/jurisdiction)
```

Run: `python3 models/leadership/build_leadership.py`. It is **not** wired into `scripts/new-research.sh`
(the SCC gate) on purpose — run it standalone so leadership updates never interact with the graph gate.

## Record schema (one official per record)

| field | required | meaning |
|---|---|---|
| `id` | yes | stable slug, e.g. `us-pres-trump-2025` (builder dedupes on this) |
| `person` | yes | full name (a real, sourced person — never fabricated) |
| `role` | yes | office title, e.g. "Secretary of the Treasury" |
| `jurisdiction` | yes | "United States", "U.S. Senate", a state, county, or city |
| `branch` | yes | `executive` \| `legislative` \| `judicial` \| `independent` \| `military` \| `law_enforcement` \| `state` \| `local` |
| `level` | yes | `federal` \| `state` \| `county` \| `municipal` \| `special_district` |
| `status` | yes | `incumbent` \| `acting` \| `nominated` \| `former` |
| `party` | no | party affiliation if applicable |
| `start` | no | ISO date or year the person took the role |
| `end` | no | ISO date / year, or omit if incumbent |
| `as_of` | yes | the date this record was last verified (point-in-time stamp) |
| `source_url` | yes | authoritative source for the record |
| `source_dataset` | yes | which dataset/file it came from |

## Ingestion contract for bulk expansion (#118-132)

The builder auto-ingests these when dropped into `data/leadership/sources/`:

- **`legislators-current.csv`** (the open-source [@unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) dataset) → maps `last_name/first_name/type(sen|rep)/state/party/...` to all 535 members (#121). No API key needed; it is the authoritative open roster.
- Any `*.json` whose entries already match the record schema above (curated tiers: executive #118-119, judiciary #122, IC/military #123, state execs #124, etc.).
- State/county/municipal rosters are added the same way: drop a conforming `*.json` or a `*.csv` + a sibling `<name>.map.json` column-mapping, then re-run. This makes the exhaustive tiers an **append + re-run**, not a rewrite.

## Discipline

- **No fabricated names.** Every record carries a `source_url`; the builder warns on any missing one.
- **Dated.** Roles churn (e.g., AG Bondi → Blanche acting, Apr 2026; DHS Noem → Mullin, Mar 2026); every record is `as_of`-stamped and `status`-typed so the directory is honestly point-in-time.
- **Institutional ACTION ≠ MIND** (composition guard): a roster of officeholders is not a claim about collective intent.
