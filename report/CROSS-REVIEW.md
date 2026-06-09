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
- ✓ **NVIDIA → CoreWeave** (equity): $2.0B [fin-coreweave-oracle.json]; $0.3B [fin-nvidia-openai.json] — reconciled: early ~$0.3B stake vs later ~$2B marked holding (distinct dates)
- ✓ **NVIDIA → OpenAI** (equity): $100.0B [fin-coreweave-oracle.json]; $100.0B [fin-nvidia-openai.json]; $30.0B [fin-nvidia-openai.json] — reconciled: $100B LOI/intent vs the $30B closed/committed tranche (LOI-vs-closed)

## Connectors (entities appearing across the most files)
- **Meta** — 27 files
- **Google** — 23 files
- **Oracle** — 16 files
- **Amazon** — 16 files
- **OpenAI** — 16 files
- **Anthropic** — 14 files
- **Microsoft** — 12 files
- **Stargate** — 11 files
- **Chainlink** — 10 files
- **JPMorgan** — 10 files
- **NVIDIA** — 10 files
- **a16z** — 9 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- BRICS, CLARITY, PIF, PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, Vistra

## Newest file `macro-gig-labor.json` — related files by shared entities (verify cross-refs exist)
- spec-crypto-sec-epstein.json: 5 shared entities
- fin-hedera-connections.json: 5 shared entities
- spec-sec-filings-primary.json: 5 shared entities
- fin-meta-family.json: 4 shared entities
- macro-crqc-quantum-landscape.json: 4 shared entities
- sec-filings.json: 4 shared entities
- fin-google-amazon-anthropic-meta.json: 4 shared entities
- spec-telecom-satellite.json: 4 shared entities