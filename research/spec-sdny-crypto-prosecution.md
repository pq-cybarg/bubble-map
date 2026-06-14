# SDNY/DOJ crypto-privacy prosecution practices — Samourai, Roman Storm/Tornado Cash, Pertsev, and the broader pattern (neutral)

*Built 2026-06-13 from `research/spec-sdny-crypto-prosecution.json`. Verified: DOJ/SDNY + IRS-CI press, CoinDesk/Bitcoin Magazine/crypto.news (the FinCEN call + Brady motion), Mayer Brown/National Law Review (verdict analysis), Dutch court reporting (Pertsev), Coin Center (the code/privacy critique), FinCEN's 2019 guidance.*

> **Neutral by design.** This maps **both** the prosecution's rationale (real laundering, incl. DPRK; the unlicensed-money-transmitter statute) **and** the defense/critique (FinCEN's own view that non-custodial software isn't a transmitter; an alleged Brady non-disclosure; a DOJ policy memo rejecting this model that SDNY proceeded against anyway; "criminalizing neutral code"; a jury that hung on the serious counts). **"Malicious prosecution / corruption" is your framing — recorded as the open question, not asserted.** The counterweight (Tornado Cash laundered $1B+ incl. for Lazarus) is given equal billing.

## 1. Samourai Wallet (SDNY)
**US v. Rodriguez & Hill** — founders of the **non-custodial** Bitcoin mixing wallet; charged Apr 2024 (money-laundering conspiracy + unlicensed money-transmitting).
- **Prosecution:** Whirlpool/Ricochet used to launder **>$100M** of criminal proceeds; operating as an unlicensed transmitter.
- **The exculpatory FinCEN call (fact):** on **Aug 23 2023**, FinCEN personnel told prosecutors they did **not** believe Samourai was a "money-transmitting business" because it's **non-custodial** (consistent with FinCEN's **2019 guidance**). Charges were filed ~6 months later anyway.
- **Alleged Brady violation (fact):** defense said DOJ withheld that call for **~14 months**; the motion to dismiss was **denied without a written opinion** (May 2025).
- **Blanche memo vs continuation (fact):** Apr 2025 — DOJ disbanded the National Cryptocurrency Enforcement Team and told prosecutors to **stop targeting mixers/non-custodial wallets** for users' conduct. Samourai prosecutors sought a 16-day extension to consider dropping — **but did not drop it.**
- **Outcome:** Rodriguez & Hill pleaded guilty; **sentenced to 5 and 4 years (Judge Cote, Nov 2025)** — i.e., the prosecution proceeded to conviction **despite FinCEN's stated view and the DOJ policy memo** rejecting this model.

## 2. Roman Storm / Tornado Cash (SDNY)
- **Verdict (Aug 6 2025):** convicted on **conspiracy to operate an unlicensed money-transmitting business**; the jury **hung** (after Allen charges) on the **more serious** money-laundering and sanctions-evasion conspiracy counts. **DOJ requested a retrial** (Mar 2026, proposed Oct 2026).
- **Prosecution:** Tornado Cash laundered **>$1B**, incl. **DPRK/Lazarus Ronin** proceeds; Storm knowingly operated/profited.
- **Critique:** the contracts are **immutable, non-custodial** — Coin Center argues prosecuting this **"criminalizes the publication of software code."** SDNY argued the FinCEN/Samourai opinion was **"irrelevant"** to Storm (disputed). The **hung counts** themselves bear on the theory's strength. **Developer-liability precedent: unsettled.**

## 3. Alexey Pertsev (Netherlands)
Tornado Cash co-developer **convicted (May 2024), 64 months**, for facilitating **~$1.2B** of laundering; a judge called the tool primarily criminal. Released pending appeal (electronic monitor). *Fact.*

## 4. The broader pattern (and its tensions)
- **The money-transmitter theory on non-custodial software** — applying the unlicensed-transmitter statute to devs who never custody funds, **in tension with FinCEN's 2019 guidance.** The central unsettled question. *Contested.*
- **The OFAC track (separate):** OFAC sanctioned the Tornado Cash **immutable code** (Aug 2022); the **5th Circuit vacated** it (Nov 2024) and Treasury lifted it (Mar 2025) — **a court rejecting the parallel sanctions theory even as the criminal cases proceeded** (`spec-onchain-threat-actor-addresses`). *Fact.*
- **Chilling effect:** privacy-wallet/mixer operators (Wasabi/zkSNACKs, Phoenix) restricted or exited the US. *Fact.*
- **Selective-enforcement concern:** incumbent banks ran dollar tokens (JPM Coin) while crypto-native privacy devs faced criminal charges (cf. the Ripple-vs-JPM-Coin asymmetry, `spec-crypto-banking-debanking`). *Contested concern.*
- **Policy whipsaw:** the 2025 deregulatory posture (Blanche memo, OFAC vacatur, the SEC/CFTC reset) sits awkwardly beside **SDNY continuing Samourai to a guilty plea** — the executive saying "stop" while a US Attorney's office proceeded. *Fact (the tension).*

## 5. The counterweight (neutrality)
The harm was real: Tornado Cash processed **>$1B** of illicit flows including DPRK/Lazarus proceeds; Samourai mixed criminal funds; **Pertsev (Dutch) and Storm (one count) were convicted.** The defensible prosecution interest — money-laundering and sanctions evasion — is real. **The dispute is whether the money-transmitter/developer-liability *theory* is the lawful way to reach it, and whether *these specific prosecutions'* conduct (the FinCEN non-disclosure; proceeding against the policy memo) was proper.** Both sides stated; **neither "corruption" nor "pure persecution" is asserted as a finding.**

*Sources: [DOJ SDNY — Samourai founders sentenced 5/4 years](https://www.justice.gov/usao-sdny/pr/founders-samourai-wallet-cryptocurrency-mixing-service-sentenced-five-and-four-years); [CoinDesk — Samourai files to dismiss citing FinCEN guidance](https://www.coindesk.com/policy/2025/05/30/samourai-wallet-files-to-dismiss-doj-case-citing-fincen-guidance); [CoinDesk — prosecutors weigh dropping under new DOJ priorities](https://www.coindesk.com/policy/2025/04/29/samourai-wallet-prosecutors-are-considering-dropping-charges-under-new-doj-crypto-enforcement-priorities-filing); [CoinDesk — Roman Storm guilty (partial verdict)](https://www.coindesk.com/policy/2025/08/06/roman-storm-guilty-of-unlicensed-money-transmitting-conspiracy-in-partial-verdict); [Mayer Brown — the mixed verdict & developer liability](https://www.mayerbrown.com/en/insights/publications/2025/08/the-tornado-cash-trials-mixed-verdict-implications-for-developer-liability); [Decrypt — Pertsev released pending appeal](https://decrypt.co/304723/tornado-cash-developer-alexey-perstev-leaving-prison); [Coin Center — Tornado Cash is a privacy/free-speech tool](https://www.coincenter.org/tornado-cash-is-no-golem-its-a-tool-for-privacy-and-free-speech/).*
