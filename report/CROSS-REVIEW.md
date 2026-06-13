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
- **Meta** — 37 files
- **Google** — 30 files
- **OpenAI** — 27 files
- **Oracle** — 23 files
- **Amazon** — 21 files
- **Microsoft** — 20 files
- **Stargate** — 16 files
- **NVIDIA** — 16 files
- **Anthropic** — 16 files
- **Chainlink** — 15 files
- **FDIC** — 15 files
- **SpaceX** — 14 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- CLARITY, PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, Vistra

## Newest file `spec-cambodia-scam-fara-paid-influence.json` — related files by shared entities (verify cross-refs exist)
- spec-unc-nk-attribution-map.json: 2 shared entities
- geopolitics-allied-intel-nodes.json: 2 shared entities
- spec-tornado-samourai.json: 2 shared entities
- temporal-bridges.json: 2 shared entities
- spec-onchain-threat-actor-addresses.json: 2 shared entities
- spec-exchanges-asia.json: 1 shared entities
- influence-tbi-policy.json: 1 shared entities
- fin-hedera-connections.json: 1 shared entities