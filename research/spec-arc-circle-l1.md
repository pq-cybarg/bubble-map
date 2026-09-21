# Circle's Arc L1 - the issuer-run, permissioned "Wall Street blockchain"

**Arc** is a USDC-native Layer-1 built and controlled by **Circle** (USDC issuer; NYSE: CRCL). Introduced 12 Aug 2025, public testnet 28 Oct 2025, founding validators named 5 Aug 2026, **mainnet 16 Sep 2026** - one day after the CLARITY Act cloture vote failed.

## Architecture (fact)
- **Consensus:** Malachite (Tendermint-derived BFT, by Informal Systems) - deterministic finality <500ms, no reorg risk (a genuine institutional-settlement advantage over probabilistic chains).
- **Execution:** Reth (Rust Ethereum client) - fully EVM-compatible (Solidity/Foundry/Hardhat).
- **Gas:** **USDC is the native gas token** (fees ~$0.01, EIP-1559 smoothed). ~3,000 TPS at 20 validators (reported benchmark).

## Institutional backing
- **11 permissioned validators:** BlackRock, DTCC, Galaxy, Global Payments, ICE (NYSE parent), Mastercard, MoneyGram, SBI, Standard Chartered, Sumitomo, Visa - plus Circle.
- **Commitments:** DTCC to tokenize DTC-custodied assets on Arc (2027); BlackRock to migrate its ~$2.87B **BUIDL** tokenized-Treasury fund.
- **Token:** ARC presale reported ~$222M at ~$3B (a16z crypto lead; BlackRock + Apollo backers); 10B ARC minted as a technical milestone, **no committed public launch**.

## Credibility - read it straight
1. **Permissioned, not decentralized.** Arc is **proof-of-authority**: eleven Circle-chosen institutions (plus Circle) produce blocks. Branding it a "public blockchain" is a stretch - it is a consortium settlement network. That is a *defensible design choice* for institutional settlement, but it is materially different from a permissionless L1, and it concentrates censorship/control power in a named set. *(fact of PoA; "most concentrated validator set ever" = reported; the branding critique = interpretation.)*
2. **Issuer-run conflict.** Circle **issues USDC, operates the chain where USDC is gas, and captures the fees** - the same vertical-integration pattern as Tether/Cantor and Stripe/Tempo. Efficient, but it fuses issuer, infrastructure, and toll-collector. *(structural fact; conflict framing interpretation.)*
3. **Token uncertainty.** 10B ARC minted, no committed public launch - the presale valuation is speculative until/unless a token actually trades. *(fact.)*
4. **Regulatory dependence.** The compliance-first, KYC-gated design bets on CLARITY/GENIUS-style clarity; launching the day after the failed cloture vote underscores that dependence. *(fact of timing; interpretation of the bet.)*

## Surrounding efforts (the stablecoin-L1 race)
Arc (issuer-run) vs **Tempo** (Stripe/Paradigm, processor-run) are the two flagships; the wider field includes Tether's **Plasma/Stable**, Ripple, and Codex. The pattern: everyone who touches stablecoins now wants to own the settlement layer - and capture the float + fees on top of the reserve income.

*Sources: Circle Arc announcements (Aug 2025 - Sep 2026); crypto-press (cryptonomist, crypto.news, cryptotimes, mexc). Several figures are third-party (presale, benchmarks, migrations) - graded reported/varies; verify against Circle filings for high-stakes use. Cross-refs: Circle, USDC, Tempo, BlackRock, DTCC, Visa, Mastercard, Standard_Chartered, SBI, Andreessen_Horowitz, Apollo, CLARITY_Act, Stablecoins.*
