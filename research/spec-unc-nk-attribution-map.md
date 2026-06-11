# The attribution layer: how UNC#### clusters graduate, and where North Korea fits

*Compiled 2026-06-10. Overlay — evidence-graded (`fact | contested | weak | unsupported`), excluded from the formal proofs. Cross-refs `spec-supplychain-shaihulud-extortion`, `blockchain_web` (Lazarus/Tornado Cash), and the altcoin/exchange threads.*

Two things at once: **how** attribution actually works (the UNC → APT/FIN pipeline), and **where** North Korea's unusual *financially-motivated state* hacking sits within it. The first is an epistemic-honesty device worth understanding on its own; the second shows why a rigid taxonomy needs it.

## How UNC attribution works (and why it's good epistemics)
Mandiant/Google use **UNC ("uncategorized")** for a cluster of intrusion activity — infrastructure, tools, tradecraft — **anchored on a defining characteristic**, often from a single incident, that they are **not yet ready** to label APT or FIN (**fact**). As evidence accumulates, a cluster may move **UNC → TEMP** (a temporary codename) **→ APT####** (nation-state) or **FIN####** (financially motivated). Clusters **grow, merge, and split**, and graduation can take **years** (**fact**).

The point: the framework is **built to avoid premature "who" claims** — it joins discrete evidence under a neutral label until confidence is earned. That is precisely the discipline this project applies (zero-trust; never infer intent from adjacency). **A UNC number is not a name and not a country** — equating "UNC####" with a nation in a headline is the exact error the system exists to prevent. The attribution layer itself models the epistemics the rest of this map tries to keep.

## The DPRK clusters
- **TraderTraitor** = Jade Sleet = **UNC4899** = Pukchong, a North Korea–aligned Lazarus subgroup (**fact**). Heists: **Ronin/Axie ~$625M** (Mar 2022), **DMM Bitcoin ~$308M** (May 2024), and **Bybit ~$1.5B** (21 Feb 2025) — the **largest crypto heist on record** (**fact**, FBI-attributed). The Bybit method was a **supply-chain compromise of Safe{Wallet}**: phish a Safe admin, malware on the dev machine, inject JavaScript served *specifically to Bybit* — Bybit's own infrastructure was never directly breached. The **FBI/IC3 PSA of 26 Feb 2025** publicly attributed it to DPRK/TraderTraitor.
- **Contagious Interview**: a DPRK **job-lure** campaign — fake freelance/dev interviews trick targets into running malicious **npm packages / Docker containers** that drop the **BeaverTail** stealer + InvisibleFerret (**fact**). Critically, this uses the **same npm-supply-chain vector** as the criminal Shai-Hulud / Team PCP worms — **same technique, different attribution** (state vs crime). The map must not collapse them.
- **IT-worker fraud**: DPRK operatives use **stolen/borrowed identities** + laptop farms to get hired at Western firms, remitting wages to the regime and sometimes planting access (**fact**). The stolen artifact here is a **hirable identity** — the same identity-theft mechanism as the supply-chain block.
- **Scale**: Chainalysis put DPRK's 2025 crypto theft at a record ~**$2B**; TRM Labs estimates DPRK at ~**76% of all crypto-hack value in 2026** via just two attacks (**contested** — firm estimates, methodology-dependent, but directionally consistent across firms).

## The financial-vs-espionage split (why DPRK is the odd state)
Most APTs steal **secrets** (espionage). DPRK's signature is that a **nation-state steals money** — crypto heists and IT-worker wages that fund the regime and its weapons programs under sanctions. So DPRK clusters sit **between APT (state) and FIN (financial)**: state-directed but profit-seeking. That hybrid is exactly why a rigid APT/FIN taxonomy needs the neutral **UNC** staging area.

## The through-line
Across the criminal clusters (`spec-supplychain-shaihulud-extortion`) and the DPRK clusters here, the recurring prize is an **identity/trust artifact** — an npm token, an OAuth grant, a developer's machine, a hirable identity, a wallet-admin session. Different motives (extortion, regime funding, grudge); **one attack surface: trust attached to identity.** That is the security mirror of the digital-ID concentration thesis (`digitalid-worldcoin-eid-convergence`): **centralizing identity raises the payoff of stealing it.**
