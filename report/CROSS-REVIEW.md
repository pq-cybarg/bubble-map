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
- **Meta** — 52 files
- **Google** — 35 files
- **FDIC** — 31 files
- **OpenAI** — 30 files
- **Oracle** — 29 files
- **Microsoft** — 25 files
- **Chainlink** — 23 files
- **Amazon** — 22 files
- **NVIDIA** — 22 files
- **Stargate** — 19 files
- **JPMorgan** — 18 files
- **Anthropic** — 18 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, Vistra

## Newest file `digitalid-orchestration-real-incentive.json` — related files by shared entities (verify cross-refs exist)
- digitalid-corporate.json: 9 shared entities
- macro-pqc-chips.json: 7 shared entities
- spec-network-overlay.json: 7 shared entities
- spec-disclosures-surveillance.json: 7 shared entities
- macro-crqc-quantum-landscape.json: 7 shared entities
- temporal-bridges.json: 7 shared entities
- fin-hedera-connections.json: 6 shared entities
- spec-uk-labour-tbi-influence.json: 6 shared entities