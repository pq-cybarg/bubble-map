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
- **Meta** — 87 files
- **Chainlink** — 59 files
- **Google** — 56 files
- **OpenAI** — 45 files
- **Microsoft** — 42 files
- **FDIC** — 37 files
- **Amazon** — 35 files
- **Oracle** — 33 files
- **NVIDIA** — 32 files
- **Anthropic** — 27 files
- **a16z** — 23 files
- **Ripple** — 23 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- Vistra

## Newest file `catalog-quiet-money-2.json` — related files by shared entities (verify cross-refs exist)
- spec-telecom-satellite.json: 1 shared entities
- spec-surveillance-cyber-threat-layer.json: 1 shared entities
- spec-spyware-vendor-catalog.json: 1 shared entities
- digitalid-corporate.json: 1 shared entities
- fin-ai-depreciation-debttrap.json: 1 shared entities
- influence-meta-childsafety.json: 1 shared entities
- fin-spacex-spcx.json: 1 shared entities
- macro-crqc-quantum-landscape.json: 1 shared entities