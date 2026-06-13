# On-chain address tracking — threat actors, state actors, sanctioned entities, and government-seized wallets

*Built 2026-06-12 from `research/spec-onchain-threat-actor-addresses.json`. Attributions **verified this pass** against FBI PSAs, OFAC SDN designations, Treasury releases, DOJ filings, and chain-forensics (Chainalysis/Elliptic/TRM/Arkham).*

> **Attribution grade.** Government attributions (FBI PSA, OFAC SDN, Treasury, DOJ) are **high-grade primary**. Chain-forensics **clustering** is strong but **probabilistic/labeled**. This block does **not** hand-transcribe long hex addresses (error risk) — it cites the **authoritative machine-readable lists** (OFAC SDN "Digital Currency Address" fields; FBI PSA IOC lists) and records cluster-level facts. Sanction status is **time-varying** and dated. Overlay edges excluded from the proofs.

## 1. Why track on-chain identities
Crypto's transparency cuts both ways: **threat actors, governments, and sanctioned entities all hold traceable on-chain addresses.** State-grade theft (DPRK), sanctions evasion (Russia/Iran), mixing (Tornado Cash), and **state seizure** (US government BTC) are all legible on-chain — a first-class data source, not a press summary.

## 2. North Korea — Lazarus Group (TraderTraitor / APT38)
The most prolific state-grade thief; proceeds fund the DPRK weapons program (UN Panel of Experts; US Treasury).
- **Bybit — Feb 21 2025 — $1.5B (401,000 ETH).** Compromised a **Safe{Wallet} developer machine**, injected malicious JS into the multisig UI to alter transaction targets — **the largest crypto heist ever.** FBI PSA confirmed Lazarus/TraderTraitor and **published 51 ETH laundering addresses**. *Fact (FBI primary).*
- **Ronin/Axie bridge — Mar 2022 — ~$625M.** OFAC added the hacker's ETH address to the **SDN list (Apr 2022)** — the first OFAC-sanctioned hacker address. *Fact.*
- **Harmony Horizon — Jun 2022 — ~$100M.** Laundered via Tornado Cash + Railgun. *Fact (FBI).*
- **Atomic Wallet / Stake.com / WazirX cluster (2023–24)** — $100M+ combined, FBI/forensics attributed to DPRK. *Fact/contested.*

**Address source:** per-incident FBI PSA IOC lists + OFAC SDN entries; cluster tracking by Chainalysis/Elliptic/Arkham.

## 3. Russia — sanctioned exchanges, darknet, ransomware
- **Garantex** — OFAC-sanctioned (Apr 2022); 2025 international action seized infrastructure and froze ~$28M+ USDT. *Fact (SDN).*
- **Hydra Market** — largest darknet market, sanctioned + seized (Apr 2022, US-German); SDN entry carries 100+ addresses. *Fact.*
- **Ransomware (Conti, LockBit…)** — OFAC has sanctioned specific ransomware-linked addresses/processors (SUEX, Chatex, Bitzlato). *Fact (SDN).*

## 4. Iran — Nobitex and a state-on-state strike
- **Nobitex** — Iran's largest exchange. On **Jun 18 2025** the pro-Israel **Predatory Sparrow (Gonjeshke Darande)** drained **~$90M and burned it to vanity/burner addresses with no private keys** — a **political** act, not theft-for-profit. **Treasury then designated Nobitex** for terror-finance/sanctions-evasion; forensics tied it to IRGC-adjacent flows. *Fact (Treasury + forensics).*

## 5. Mixers and the "can you sanction code?" whipsaw
- **Tornado Cash** — OFAC sanctioned it **Aug 2022** (~$7B laundered since 2019, incl. DPRK), adding **immutable smart-contract addresses** to the SDN list — the first sanctioning of code. The **5th Circuit vacated** it (Nov 2024); **Treasury lifted** it **Mar 21 2025**. Developer Roman Storm prosecuted. The central test of whether code is sanctionable. *Fact (OFAC + courts).*
- **Blender.io / Sinbad.io** — BTC mixers sanctioned for DPRK laundering. *Fact.*
- **Samourai Wallet** — operators charged 2024 (see `spec-tornado-samourai`) — the criminalization of privacy tooling. *Fact (DOJ).*

## 6. The government as an on-chain holder (seizures → reserve)
- **Bitfinex 2016 hack** — ~120,000 BTC stolen; DOJ seized **~$3.6B (Feb 2022)**; **Lichtenstein & Heather "Razzlekhan" Morgan** pleaded guilty (2023). Seized coins sit in government wallets, **moved on-chain periodically** (publicly tracked). *Fact (DOJ).*
- **Silk Road** — **~$3.36B** seized from James Zhong (Nov 2022) + the 2020 ~69,370 BTC forfeiture; courts cleared the government to **sell** (2025). *Fact.*
- **US holdings & Strategic Bitcoin Reserve** — by 2024–25 the government controlled on the order of **~200k BTC (~1% of supply)**; a **2025 executive order** established a **Strategic Bitcoin Reserve** (retain seized BTC, don't sell). The state is now a large, **on-chain-visible** BTC holder — a market and policy variable. *Fact.*

## 7. Limits & ingest — and the free-access ceiling (important)
This is an **attribution + source-pointer** layer, not a raw address dump. Government attributions are high-grade; clustering is labeled. `fetch_ofac.py` (env-free) ingests the **free OFAC Advanced XML** (SDN + Consolidated) into `data/ofac_crypto_addresses.json` — **757 addresses** (522 BTC / 127 TRON / 97 ETH / 10 LTC / 1 XMR), all from the SDN list (the Consolidated list carries none).

**The 757 is a FREE-ACCESS FLOOR, not the full universe.** It captures only addresses OFAC has **formally designated**. It deliberately does **not** include:
- **(a)** per-incident **FBI/CISA PSA IOC lists** — e.g., the **51 Bybit-laundering ETH addresses** the FBI published separately — authoritative but absent from the SDN XML;
- **(b)** un-sanctioned-but-attributed clusters tracked by **commercial forensics (Chainalysis/Elliptic/TRM/Arkham)** — **paywalled**, and how most DPRK/laundering hops are actually traced;
- **(c)** anything OFAC publishes only in non-machine-readable form.

So the on-chain identity picture here is a **lower bound**; full coverage requires the FBI PSA IOC feeds **plus a paid forensics subscription**. Sanction status is also dated (Tornado Cash 2022 → vacated 2024 → lifted 2025), so a static list overstates what is *currently* sanctioned.

*Verification sources: [FBI/Bybit attribution](https://www.picussecurity.com/resource/blog/fbi-north-korean-lazarus-group-bybit-crypto-heist), [Tornado Cash sanctions lifted](https://www.venable.com/insights/publications/2025/04/a-legal-whirlwind-settles), [Silk Road $3.36B](https://www.occrp.org/en/news/us-doj-announces-historic-336b-crypto-seizure), [Nobitex hack](https://www.elliptic.co/blog/iranian-crypto-exchange-nobitex-hacked-pro-israel-group), [US BTC holdings](https://bitcoinmagazine.com/markets/us-government-continues-bitcoin-seizures-controls-nearly-1-of-circulating-supply-).*
