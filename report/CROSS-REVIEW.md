# Cross-Review — re-review of all prior findings

## JSON validity
- ALL VALID

## Edge-amount reconcile (same from->to, materially different amounts across files)
- ⚠ **AMZN → Anthropic** (equity): $8.0B [fin-google-amazon-anthropic-meta.json]; $25.0B [fin-google-amazon-anthropic-meta.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)
- ⚠ **Blackstone → CoreWeave** (debt): $2.3B [fin-coreweave-oracle.json]; $7.5B [fin-coreweave-oracle.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)
- ⚠ **GOOGL → Anthropic** (equity): $3.0B [fin-google-amazon-anthropic-meta.json]; $40.0B [fin-google-amazon-anthropic-meta.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)
- ⚠ **Microsoft → OpenAI** (equity): $135.0B [fin-microsoft-openai.json]; $13.0B [fin-microsoft-openai.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)
- ⚠ **NVIDIA → CoreWeave** (equity): $2.0B [fin-coreweave-oracle.json]; $0.3B [fin-nvidia-openai.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)
- ⚠ **NVIDIA → OpenAI** (equity): $100.0B [fin-coreweave-oracle.json]; $100.0B [fin-nvidia-openai.json]; $30.0B [fin-nvidia-openai.json]  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)

## Connectors (entities appearing across the most files)
- **Meta** — 24 files
- **Google** — 19 files
- **Oracle** — 14 files
- **OpenAI** — 14 files
- **Amazon** — 13 files
- **Microsoft** — 11 files
- **Anthropic** — 11 files
- **Stargate** — 10 files
- **a16z** — 9 files
- **JPMorgan** — 9 files
- **NVIDIA** — 9 files
- **SoftBank** — 8 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- BRICS, CLARITY, InQTel, PIF, PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, TrailOfBits, Vistra

## Newest file `spec-exchanges-asia.json` — related files by shared entities (verify cross-refs exist)
- temporal-bridges.json: 14 shared entities
- fin-hedera-connections.json: 12 shared entities
- altcoin-lens.json: 11 shared entities
- spec-crypto-sec-epstein.json: 11 shared entities
- spec-sec-sdny-regulatory.json: 10 shared entities
- fin-google-amazon-anthropic-meta.json: 9 shared entities
- spec-network-overlay.json: 9 shared entities
- fin-coreweave-oracle.json: 8 shared entities