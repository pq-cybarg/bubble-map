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
- **Meta** — 61 files
- **Google** — 41 files
- **OpenAI** — 34 files
- **FDIC** — 32 files
- **Oracle** — 31 files
- **Chainlink** — 28 files
- **Microsoft** — 27 files
- **Amazon** — 27 files
- **NVIDIA** — 27 files
- **Stargate** — 21 files
- **Anthropic** — 21 files
- **JPMorgan** — 18 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- ScaleAI, TerraPower, Vistra

## Newest file `spec-australia-state-network.json` — related files by shared entities (verify cross-refs exist)
- spec-quantum-computing-competitive-landscape.json: 2 shared entities
- macro-crqc-quantum-landscape.json: 1 shared entities
- spec-rare-earth-statecraft.json: 1 shared entities
- macro-critical-minerals.json: 1 shared entities
- macro-quantum-computing.json: 1 shared entities
- defense-rare-earth.json: 1 shared entities
- spec-network-overlay.json: 1 shared entities
- fin-sealsq-wisekey-global.json: 1 shared entities