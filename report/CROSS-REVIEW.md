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
- **Meta** — 25 files
- **Google** — 21 files
- **Oracle** — 15 files
- **OpenAI** — 15 files
- **Amazon** — 14 files
- **Anthropic** — 12 files
- **Microsoft** — 11 files
- **Stargate** — 10 files
- **a16z** — 9 files
- **JPMorgan** — 9 files
- **NVIDIA** — 9 files
- **FDIC** — 9 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- BRICS, CLARITY, PIF, PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, Vistra

## Newest file `macro-official-data-integrity.json` — related files by shared entities (verify cross-refs exist)
- macro-cre-privatecredit.json: 2 shared entities
- fin-google-amazon-anthropic-meta.json: 1 shared entities
- fin-meta-family.json: 1 shared entities
- macro-history-dereg-manipulation.json: 1 shared entities
- macro-fdic.json: 1 shared entities
- spec-sec-sdny-regulatory.json: 1 shared entities
- fin-hedera-connections.json: 1 shared entities
- macro-carry-trades.json: 1 shared entities