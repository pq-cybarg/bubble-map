# Cross-Review — re-review of all prior findings

## JSON validity
- ALL VALID

## Edge-amount reconcile (same from->to, materially different amounts across files)
- none unreconciled — all material edge-amount differences are documented below

### Reconciled (reviewed, intentional — distinct tranches / LOI-vs-closed / marked-value)
- ✓ **AMZN → Anthropic** (equity): $8.0B [fin-google-amazon-anthropic-meta.json]; $25.0B [fin-google-amazon-anthropic-meta.json] — reconciled: staged rounds: initial up-to-$8B then expanded to $25B (cumulative, distinct dates)
- ✓ **Blackstone → CoreWeave** (debt): $2.3B [fin-coreweave-oracle.json]; $7.5B [fin-coreweave-oracle.json] — reconciled: distinct debt facilities ($2.3B and $7.5B), not the same loan
- ✓ **GOOGL → Anthropic** (equity): $3.0B [fin-google-amazon-anthropic-meta.json]; $40.0B [fin-google-amazon-anthropic-meta.json] — reconciled: initial $3B stake vs expanded ~$40B cumulative commitment (distinct dates)
- ✓ **Microsoft → OpenAI** (equity): $135.0B [fin-microsoft-openai.json]; $13.0B [fin-microsoft-openai.json] — reconciled: $13B cumulative cash invested vs ~$135B marked stake value post-2025 restructuring
- ✓ **NVIDIA → CoreWeave** (equity): $2.0B [fin-coreweave-oracle.json]; $0.3B [fin-nvidia-openai.json]; $3.7B [spec-sec-filings-primary.json] — reconciled: early ~$0.3B stake vs later ~$2B marked holding (distinct dates)
- ✓ **NVIDIA → OpenAI** (equity): $100.0B [fin-coreweave-oracle.json]; $100.0B [fin-nvidia-openai.json]; $30.0B [fin-nvidia-openai.json] — reconciled: $100B LOI/intent vs the $30B closed/committed tranche (LOI-vs-closed)

## Connectors (entities appearing across the most files)
- **Meta** — 79 files
- **Chainlink** — 57 files
- **Google** — 51 files
- **OpenAI** — 41 files
- **FDIC** — 35 files
- **Oracle** — 33 files
- **Amazon** — 32 files
- **NVIDIA** — 30 files
- **Microsoft** — 30 files
- **Anthropic** — 24 files
- **Stargate** — 23 files
- **JPMorgan** — 22 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- Vistra

## Newest file `spec-stablecoin-yield-fight.json` — related files by shared entities (verify cross-refs exist)
- spec-crypto-banking-debanking.json: 4 shared entities
- influence-congress-funding-compromise.json: 4 shared entities
- spec-sdny-crypto-prosecution.json: 3 shared entities
- temporal-bridges.json: 3 shared entities
- blockchain-registry.json: 3 shared entities
- macro-stablecoin-treasury-rail.json: 2 shared entities
- macro-stablecoin-failures-manipulation.json: 2 shared entities
- digitalid-orchestration-real-incentive.json: 2 shared entities