# Ethena / USDe - the synthetic "delta-neutral" dollar + the stablecoin risk taxonomy

USDe (Ethena Labs, founder Guy Young) completes the map's stablecoin picture by adding the **third mechanism class**. It is neither fiat-backed nor over-collateralized - it is a **synthetic dollar held to peg by a delta-neutral basis trade**.

## The three stablecoin mechanism classes
1. **Fiat-backed** (USDC, USDT, USD1) - cash + T-bill reserves; risk = reserve quality, issuer solvency, freeze/censorship. *Reserve-income business.*
2. **Synthetic / delta-neutral** (USDe) - long staked-ETH/LSTs + spot BTC, short an equal notional of perps; peg from the hedge + arbitrage. Risk = **funding-rate flips, CEX counterparty, depeg-contagion**. *Basis-trade business.*
3. **Algorithmic** (Terra/UST - collapsed 2022) - reflexive mint/burn seigniorage; risk = death spiral. *USDe is often mis-compared to this and is mechanically different - but that does not make it risk-free.*

## How USDe works (fact)
For ~$1 of USDe, Ethena holds ~$1 of long crypto (mostly Lido stETH earning ~3% + spot BTC) and an **equal short perp** on Binance/Bybit/OKX/Deribit. The hedge cancels price exposure; **perp funding + staking yield** flow to **sUSDe** stakers (~7.1% APY Jun 2026, down from ~9.4% in Apr; 7-day unstake cooldown). Reserves have diversified toward **USDtb** (Ethena's tokenized Treasuries) as a stable buffer, plus a **Reserve Fund** (~$73M, ~1.7% of supply). Supply figures conflict (~$4.4B vs ~$5.5-6B across dates) - treat as a snapshot.

## The honest risks
- **Negative funding is the core risk.** In a bear/deleveraging regime the shorts *pay* instead of receive - and **Ethena itself says no one knows how long the protocol can absorb sustained negative funding** before it contracts below viable scale.
- **CEX counterparty.** Hedges sit on centralized exchanges; an exchange failure could block closing a short. The Bybit hack + Oct flash crash tested this.
- **Depeg / contagion.** Brief 50-100bps depegs have occurred + resolved via arbitrage; but USDe is heavily integrated as DeFi collateral (Aave, Pendle), so a severe depeg could cascade.
- **Regulatory gap.** Because backing is a derivatives trade, USDe is **not a "payment stablecoin" under GENIUS** - so the yield prohibition constraining USDC never touches it. It pays yield legally, with billions sitting in an unsettled classification (security? commodity? new class?).

## Why it's on the map
The stablecoin-Treasury rail (USDC/USDT/USD1/Arc/Tempo/Plasma) is the *fiat-backed* story; USDe is the *synthetic* story riding on crypto leverage + CEX plumbing. It even loops back to Treasuries via USDtb, and layers onto Plasma. The taxonomy matters because "stablecoin" is not one risk - it is at least three.

*Sources: Ethena docs + dashboard; Coin Metrics; Forbes; DeFiLlama. Mechanism/gap = fact; supply/APY = reported/varies; contagion severity = interpretation. Cross-refs: Ethena, USDe, sUSDe, USDtb, Ethereum, Binance, Bybit, Aave, US_Treasuries, GENIUS_Act, Terraform_Labs, Plasma, Stablecoins.*
