# Historical bubble analogues, the post-2008 deregulation chain, and market-manipulation enforcement

*Built from `research/macro-history-dereg-manipulation.json` (web-verified: CNBC, DOJ/CFTC/SEC press, Fortune, Roosevelt Institute, The Hill, Marketplace) + the FDIC time series in `macro-fdic`.*

> **Thesis.** Every bubble cycle moves risk into a **less-regulated venue** and uses an **accounting/financing device** that books revenue or hides leverage until a discrete unwind. AI 2025–26 rhymes precisely with **dotcom (vendor financing)** and **2008 (off-balance-sheet leverage)** — enabled by post-2008 deregulation and a documented market-manipulation record.

## 1. The analogues — same devices, larger scale
| Era | Device | What happened | Modern parallel |
|---|---|---|---|
| **Dotcom 1999–2002** | **Vendor financing** | Lucent/Nortel/Cisco extended billions of credit to customers to buy the vendors' own gear, booking financed sales as revenue (Lucent ~$8B of commitments; loans soured as carriers failed in 2001). Nasdaq **−78%** peak-to-trough. | **NVIDIA → OpenAI/CoreWeave/xAI/neocloud** equity + take-or-pay backstops that fund customers' GPU purchases. Same structure, larger scale (NVIDIA self-funding ratio ~18–56%, `data/graph.json`). |
| **GFC 2008** | **Off-balance-sheet leverage** (SIVs, CDOs, ABCP) | Risk warehoused in vehicles invisible until 2007–08. FDIC failures spiked to 30 (2008), 148 (2009), 157 (2010). Glass-Steagall already repealed (1999). | **AI datacenters via SPVs/JVs** (Stargate, Meta-Hyperion/Blue Owl ~$27B) and **private credit** kept off the hyperscalers' balance sheets (`macro-cre-privatecredit`; First Brands the canary, `macro-firstbrands-ubs`). |
| **2022–23 rate-shock + crypto** | **HTM accounting + uninsured-deposit runs + crypto leverage** | Fed hiking created huge unrealized securities losses (FDIC peak **−$517B**, 2024Q1); **SVB (~$209–220B), Signature (~$110B), First Republic (~$229B)** failed; Silvergate wound down; FTX collapsed (Nov 2022). 2023 failed-bank assets ~$532B. | The **HTM/AFS overhang persists** (−$325B, 2026Q1; HTM −$214.5B **not** marked to AOCI — the SVB failure mode), re-widened by rising long rates from the AI-debt issuance wave. |

**All three devices are present simultaneously now** — the novelty is scale and the speed/abstraction of the financing, not the mechanism.

## 2. The deregulation chain (1999 → 2018 → 2023)
- **1999 — Gramm-Leach-Bliley** repeals Glass-Steagall → merges commercial + investment banking; sets up scale/concentration.
- **2010 — Dodd-Frank** → enhanced prudential standards for banks **>$50B** (stress tests, liquidity, resolution plans).
- **2018 — EGRRCPA** raises the enhanced-supervision/SIFI threshold **$50B → $250B**, exempting SVB and dozens of mid-size banks from regular stress testing and enhanced liquidity/resolution. **SVB CEO Greg Becker had lobbied for this since 2015.**
- **2023 — consequence:** **SVB (~$209–220B, below the $250B line) failed having escaped enhanced oversight** — the direct dereg→failure causal chain. Critics (Warren/Porter, Roosevelt Institute) tie the rollback to the collapse. *(Causal weight is contested; the threshold change is fact — cross-ref `influence-congress-funding-compromise` S.2155.)*

## 3. The market-manipulation record (venues move, the pattern repeats)
- **JPMorgan precious-metals & Treasuries spoofing (2008–2016):** hundreds of thousands of spoof orders in gold/silver/platinum/palladium/Treasury futures. **Record $920.2M settlement (Sep 29 2020, DOJ+CFTC+SEC)**; traders Nowak & Smith convicted (2022). Venue: COMEX/CME, US Treasuries. **Fact (adjudicated).**
- **LME nickel / Tsingshan short squeeze (Mar 2022):** Xiang Guangda's Tsingshan held a massive nickel short; a squeeze spiked prices and the **LME suspended trading and cancelled ~$12B of trades** (highly controversial; litigation followed). Separately, JPMorgan held LME nickel warrants that turned out to be **"bags of rocks"** (fake, 2023). Venue: London Metal Exchange. **Fact.**
- **SHFE / Chinese futures manipulation:** recurring crackdowns; the LME/SHFE/COMEX arbitrage is a repeated stress point (see the 2025–26 COMEX-LME gold/copper dislocations in `commodities-metals`). **Fact (pattern).**

## 4. Synthesis
The AI bubble is **not novel in mechanism, only in scale and in the speed/abstraction of its financing.** Vendor financing (dotcom) + off-balance-sheet leverage (2008) + an HTM/AFS rate-shock overhang (2023) are **all present simultaneously now**, layered on a banking system deregulated at the margin (2018) and markets with a documented manipulation record (JPM/LME/SHFE). The formal cascade model (`models/tla`) treats these as the **channels** through which an AI-core shock propagates into the banking/credit system.

*Sources: [Dot-com bubble](https://en.wikipedia.org/wiki/Dot-com_bubble), [FDIC Quarterly Banking Profile](https://www.fdic.gov/quarterly-banking-profile), [EGRRCPA / SVB](https://fortune.com/2023/03/11/silicon-valley-bank-svb-ceo-greg-becker-dodd-frank-trump-rollback-systemically-important-fdic/), [Roosevelt Institute — 2018 rollback & SVB](https://rooseveltinstitute.org/blog/how-2018-regulatory-rollbacks-set-the-stage-for-the-silicon-valley-bank-collapse-and-how-to-change-course/), [CFTC — JPM $920M spoofing](https://www.cftc.gov/PressRoom/PressReleases/8260-20), [DOJ — JPM traders sentenced](https://www.justice.gov/archives/opa/pr/former-jp-morgan-precious-metals-traders-sentenced-prison), [Fortune — LME "bag of rocks"](https://fortune.com/2023/03/21/jpmorgan-fake-nickel-london-metal-exchange-bag-of-rocks/).*
