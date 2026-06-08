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
- **Meta** — 22 files
- **Google** — 18 files
- **Oracle** — 13 files
- **OpenAI** — 13 files
- **Amazon** — 12 files
- **Microsoft** — 11 files
- **Anthropic** — 10 files
- **Stargate** — 9 files
- **NVIDIA** — 9 files
- **JPMorgan** — 8 files
- **a16z** — 7 files
- **SEALSQ** — 7 files

## Under-connected entities (appear in only ONE file — candidates for new cross-links)
- BRICS, CLARITY, DPRK, InQTel, Lazarus, PIF, PsiQuantum, Quantinuum, QuantumComputingInc, ScaleAI, TerraPower, TrailOfBits, Vistra

## Newest file `fin-hedera-connections.json` — related files by shared entities (verify cross-refs exist)
- altcoin-lens.json: 13 shared entities
- macro-crqc-quantum-landscape.json: 9 shared entities
- spec-crypto-sec-epstein.json: 9 shared entities
- fin-sealsq-wisekey-global.json: 7 shared entities
- energy-power.json: 7 shared entities
- temporal-bridges.json: 7 shared entities
- sec-filings.json: 6 shared entities
- fin-google-amazon-anthropic-meta.json: 5 shared entities