# Blockchain registry — public-record flags, not a legitimacy score

*Built 2026-08-22 from `research/blockchain-registry.json`. Overlay; excluded from the financial proofs. Companion to `blockchain-leg` (stablecoin→Treasury + Fairshake), `altcoin-lens` (utility vs accrual — a *different* axis), `spec-blockchain-ecosystem` (foundations/infra), `spec-crypto-collapse-cluster` (2022 cascade), `spec-exchanges-asia`.*

> **Discipline.** This page does **not** sort "good actors" vs "bad actors." It sorts on **public-document flags**: criminal convictions, civil-fraud judgments, OFAC listings, bankruptcies/insolvencies, open-source vs custodial, US-public-company status, documented government/defense *facts* (contracts, council seats, state stablecoins, PAC funding), and explicit **none documented**. Pedigree, VC backing, and council adjacency are recorded as facts. Intent is not inferred. Composition guard: a foundation is not its token holders; an exchange is not its listed assets.

The live UI is the **Blockchain** tab (`docs/blockchain.html`).

## Quantum readiness (third axis)

Public-record flags and altcoin-lens utility grades do **not** say whether a chain still signs with ECDSA. That is a separate, load-bearing fact: Bitcoin, Ethereum, Solana, XRP, and most L2s authorize spend with **ECC** (harvest-now / forge-later). The tab joins every chain we can match against the **Blockchain Quantum Readiness Index** ([qrindex.org](https://qrindex.org/)), scraped on each `fetch_qri.py` run.

**There is no stable API.** HTML `data-*` attributes, visible table cells, and per-project `llms.txt` are parsed defensively (`models/graph/qri_parse.py`). A Scrapy spider (`qri_spider.py`) is used when scrapy is importable; otherwise stdlib + curl (macOS cert store). JSON paths on the site, if they appear, are **not** a contract.

**QRL is the reference Stage-4 L1 in this corpus:** mandatory **XMSS** (NIST SP 800-208) since genesis, QRI **98.5 / Stage 4** (evaluated 2026-08-20, medium confidence, draft). Mochimo, Tidecoin, and Abelian also sit at Stage 4 on the same index. That is cryptographic-readiness, not adoption. `altcoin-lens` still grades QRL **speculative-niche on token-accrual** — both can be true.

Fetcher: `python3 models/graph/fetch_qri.py` → `data/qri_index.json` (plus `data/qri_raw/index.html` snapshot). Prefers Scrapy when importable; otherwise stdlib HTML + curl. Cache is kept if the scrape fails. Index is AI-assisted and pre-release; scores are not proofs.

CEX/DEX rows usually have **no venue-level QRI**. The tab then shows host-chain scores (BTC/ETH for a CEX; Solana for Jupiter/Raydium; TRON for SunSwap). That is listed-asset spend-auth exposure, not a cleanliness rating of the exchange.

Slug map is best-effort (XRP Ledger is `xrp` not `ripple`; BNB Chain is `bnb`; TON is `toncoin`). When qrindex changes slugs, update `MAP` in `fetch_qri.py`.

## Why a tab (the map gap)

The bubble map had a **crypto colour bucket** and a **blockchain-leg** (GENIUS rail + Fairshake cycle) but:

1. **Bitcoin the protocol was not a node.** Only `Bitcoin_Strategic_Reserve`, `Bitcoin_Policy_Institute`, and `IBIT` existed — policy/ETF wrappers with nothing to point at.
2. **Bitfinex** and **Bybit** were sector `other` (mixing).
3. Major L1s/L2s/CEXes sitting in prose (`spec-blockchain-ecosystem`) were not bubbles: Cardano, Polkadot, Aptos, TON, Base, Arbitrum, Optimism, OKX, dYdX, Curve.
4. Definitive **adjudicated schemes** marketed as coins (OneCoin, BitConnect, PlusToken) were absent, so the 2022-cascade frauds looked like the whole "scam" set.

## What the flags mean (objective)

| Flag | On if |
|---|---|
| Adjudicated criminal | A court of record convicted a controlling person *in connection with this entity* (FTX/SBF, Celsius/Mashinsky, Terraform/Do Kwon, OneCoin, BitConnect, PlusToken). Developers charged but not convicted are **not** this flag (Tornado/Samourai: presumed innocent except where adjudicated). |
| Civil-fraud judgment | Final civil fraud judgment or equivalent. |
| OFAC SDN | The *entity* is on the SDN list (Tornado Cash). Monero is not. |
| Insolvency | Bankruptcy, liquidation, or court rehabilitation (Mt. Gox, Voyager, BlockFi, 3AC, FTX). |
| Open-source protocol | The chain/DEX code is public; not a custodian. |
| Custodial | Users do not hold keys (CEX, yield platform, some stables). |
| US public company | Exchange/issuer listed in the US (Coinbase; Voyager was). |

Government/defense is a **typed note**, not a boolean "tied to the Pentagon":

- `state_policy` — e.g. US Bitcoin reserve, Wyoming WYST via LayerZero, El Salvador legal tender
- `council_seat` — e.g. Boeing on Hedera's Governing Council (**not** a DoD contract)
- `institutional_rail` — SWIFT/DTCC/BlackRock tokenized funds
- `political_pac` — Fairshake funders (Coinbase, Ripple, Uniswap Labs, a16z, Jump)
- `ofac` / `enforcement` — sanctions or live DOJ cases
- `none_documented` — searched this corpus; no defense contract found

**Closest defense adjacency in the corpus:** Hedera council includes **Boeing**. That is labeled `council_seat`. No public L1 in this registry has a documented US DoD procurement for the chain itself.

## Keep separate (not aliases)

| Cluster | Why they are different bubbles |
|---|---|
| Ripple / XRPL / Ripple Prime / XRPLF | Company vs ledger vs prime broker vs independent foundation |
| Ethereum / Ethereum Foundation / ConsenSys / MetaMask / Infura / Linea | Protocol vs steward vs commercial spine vs products |
| Chainlink / Chainlink Labs | Network vs operating company |
| AI **Stargate** / LayerZero's UI also named Stargate | Unrelated (already footnoted in `spec-blockchain-ecosystem`) |
| Gemini / Gemini Earn | Exchange vs the Genesis-frozen yield product |
| Bitcoin / Strategic Reserve / Policy Institute / IBIT | Protocol vs US policy vs think tank vs ETF |

## Venue coverage (expanded 2026-08-22)

The first draft only had the household-name CEXes. The registry now carries **93 CEX** and **54 DEX/venue** rows: CMC/CoinGecko/CryptoRank 2026 volume tables (Binance, OKX, Bybit, MEXC, Gate, Bitget, KuCoin, HTX, Crypto.com, Upbit, LBank, Toobit, BingX, WhiteBIT, CoinW, Bitunix, Zoomex, Hyperliquid as a *DEX*), plus regional KR/JP/IN/SE Asia/LatAm/Africa/MENA/TR/AU/CA on-ramps, US institutional (EDX, Bakkt, itBit), and the dead/sanctioned set (QuadrigaCX, Cryptopia, BTC-e, Thodex, Garantex, Bittrex wind-down, FTX.US, Zipmex, Vauld, Liquid, Paxful).

**Volume is not a cleanliness score.** CMC's own 11-venue tape is ~85% top-five; wash-trading on some alt venues is a known measurement problem and is not turned into a flag here.

**Name collisions kept un-aliased:** `Stargate_Finance` (LayerZero bridge) ≠ AI `Stargate`; `Binance` ≠ `Binance_US` ≠ `Binance_TR`; `Coinbase` ≠ `Coinbase_International` ≠ `Deribit`; `HTX` is Huobi's successor name.

## CEX and DEX histories (one line each, from corpus)

- **Mt. Gox** — 2014 collapse; civil rehabilitation; repayments still slipping (Oct 31 2026). McCaleb founded then sold; Karpeles was CEO at failure.
- **Binance** — 2023 $4.3B BSA settlement; CZ plea + 2025 pardon (fine stands); MGX $2B in USD1.
- **Coinbase / Kraken** — US-regulated pole; SEC suits dropped 2025; Coinbase is a Fairshake funder.
- **FTX** — adjudicated customer-fund theft; 25-year sentence. Not a blockchain failure.
- **Uniswap** — non-custodial AMM; Uniswap Labs funds Fairshake; chose Wormhole over LayerZero on security.

DEX vs CEX is a **custody flag**, not a moral one.

## Failed businesses vs adjudicated schemes

The 2022 cascade (`spec-crypto-collapse-cluster`) mixed **leverage insolvency** (3AC, Voyager) with **adjudicated fraud** (FTX, Celsius, Terraform). This registry splits those flags so they can be filtered apart. OneCoin / BitConnect / PlusToken are **court-found schemes marketed as coins** — they were never L1s in the Bitcoin/Ethereum sense.

## Known-good / known-bad (why we refuse the labels)

"Good actor" in market speech usually means *still operating and listed.* "Bad actor" usually means *someone already lost money.* That collapses:

- a **protocol** (Bitcoin) with an **exchange failure** (Mt. Gox) that used it
- a **BSA fine** (Binance) with **customer theft** (FTX)
- a **privacy tool under OFAC** (Tornado) with a **Ponzi** (BitConnect)

The tab therefore exposes the flags and lets the reader sort. `altcoin-lens` remains the place for *utility vs token-accrual* grades — a separate axis, still not a character judgment.

## Graph review leftovers (not in this PR)

Thin or still-missing: MakerDAO/Aave/Compound, PancakeSwap, zkSync/Starknet/Scroll, Filecoin/Arweave as tab rows (they live in the ecosystem block), Kraken leadership dossiers. Overlay edges here are directional into protocols/sinks and do not close a financial cycle (gate: `structural_edges_add_no_cycle` must stay true; financial SCC stays 12).
