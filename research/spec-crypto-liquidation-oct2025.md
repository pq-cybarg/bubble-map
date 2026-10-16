# The October 10-11, 2025 crypto deleveraging crash

*Event date 2025-10-10/11; recorded 2026-10-15 as documented history. Companion to `spec-crypto-liquidation-oct2025.json`. Overlay/structural market-event edges only; the new nodes are isolated from the AI-financial SCC, which is unchanged. Grading is per-claim: fact | estimate | interpretation.*

## What happened

On Friday October 10, 2025, President Trump announced a **100% tariff on Chinese imports**. Equities and commodities sold off, and the cross-asset deleveraging cascaded into crypto - which was carrying heavy leverage. Over the next 24 hours it became, per Coinglass, the **largest liquidation event in crypto history**.

- **~$19.1B liquidated** in 24 hours (~$16.7B of it **longs**), across roughly **1.6 million** trader accounts. Coinglass later said the true nominal total was likely **$30-40B** once slower-reporting exchanges (Binance, Bybit data-feed disruptions) were folded in - **10-20x** any prior liquidation day (April 2021 was ~$10B).
- **Bitcoin** fell ~14% from a ~$122,574 Friday high to a ~$104,783 low; **Ether** -12.2% to ~$3,436. Total crypto market cap fell ~**$400B** (~$4.15T to ~$3.74T).

## The amplifiers

- **Perpetual futures** were the mechanism, not spot selling. Open interest across major venues dropped ~**43% in a day** ($217B to $123B).
- **Hyperliquid** saw the sharpest contraction - OI down ~**57%** ($14B to $6B) - and a ~**$203M ETH/USDT long** was liquidated, the **largest DEX liquidation ever recorded**.
- A **secondary trigger**: on Binance the synthetic-dollar stablecoin **USDe briefly fell to ~$0.65**, forcing further liquidations across liquid-staking tokens, alt-L1s, and derivatives - the synthetic-dollar fragility mapped in `spec-ethena-usde-synthetic-dollar` amplifying the cascade. USDe broadly repegged afterward.

## The other side (recorded for balance)

The infrastructure **mostly held**. Stablecoins broadly repegged, major exchanges processed billions in forced sales without failing, and DeFi protocols liquidated bad loans without accumulating toxic debt - no 2022-style insolvency cascade (`spec-crypto-collapse-cluster`). Whether the episode was **systemic or idiosyncratic** is contested: it exposed real fragility (hidden leverage, perp-DEX auto-deleveraging, oracle/stablecoin-depeg mechanics) but did not produce lasting institutional failures.

## How it wires into the map

An event node, `Crypto_Liquidation_Oct2025`, carries the cascade: Trump's tariff as the trigger; the price hits to Bitcoin and Ether; the perp-futures and Hyperliquid contraction; the USDe depeg (as a secondary trigger pointing *into* the event); and a resilience edge to DeFi protocols. New nodes `Hyperliquid`, `Perpetual_Futures`, and `DeFi_Protocols` are added. All edges are structural market-event links, excluded from the proofs.

## Cross-references

`spec-ethena-usde-synthetic-dollar` (the USDe depeg mechanism) | `spec-crypto-collapse-cluster` (the 2022 contrast - insolvency cascade vs this liquidation-only event) | `macro-carry-trades`, `spec-unwind-timing` (leverage unwind dynamics) | `spec-exchanges-asia` (Binance and the Asia venue layer).
