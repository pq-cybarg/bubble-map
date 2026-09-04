# Ransomware & eCrime catalog: the crews, their signature attacks, and the crypto rails

Batch 2 of the threat-actor catalog - **financially-motivated** criminal groups (mostly Russia-based / Russia-tolerated) running **Ransomware-as-a-Service** and big-game hunting. Distinct from state APTs (espionage) and commercial spyware.

## The crews and their marquee attacks
- **Ryuk -> Conti** (Wizard Spider) - pioneered big-game hunting; Conti's 2022 **"Conti Leaks"** exposed a corporate-style org after it backed Russia's invasion; later fragmented into Black Basta / Royal.
- **REvil** (Sodinokibi) - **Kaseya** (Jul 2021, ~1,500 downstream via MSPs) and **JBS** (~$11M paid).
- **DarkSide** - **Colonial Pipeline** (May 2021), East-Coast fuel panic, ~$4.4M paid, **DOJ clawed back ~$2.3M** - proof crypto ransoms are seizable.
- **LockBit** - the most prolific RaaS; disrupted by **Operation Cronos** (NCA/FBI/Europol, Feb 2024).
- **Cl0p** (TA505) - mass-exploited the **MOVEit** zero-day (May 2023): 2,700+ orgs, ~95M people - pure data-extortion.
- **BlackCat/ALPHV** - **Change Healthcare** (Feb 2024); UnitedHealth paid **~$22M**, after which ALPHV **exit-scammed** its own affiliate and faked a takedown.
- **Scattered Spider** (native-English, tied to "The Com") - **MGM** and **Caesars** (~$15M) in Sep 2023, as an **ALPHV affiliate** - Western social-engineering access-brokers renting Russian ransomware.
- **RansomHub** (2024) - absorbed ALPHV/LockBit affiliates post-takedown; deploys **EDRKillShifter** (see the DoubleAgent/BYOVD block).
- **FIN7 / Carbanak** - $1B+ in bank/retail heists via the Carbanak backdoor; later pivoted to ransomware/tooling.
- **Evil Corp** (Maksim Yakubets; Dridex) - OFAC-sanctioned 2019; 2024 UK/US sanctions + a named LockBit link.

## The rails and the counter-force
Ransomware runs on **crypto rails** - paid in Bitcoin (increasingly mixers/Monero), then laundered. **Chainalysis/TRM** trace the flows, enabling seizures (Colonial clawback) and the annual payment tallies; **OFAC** designations (Evil Corp) make paying certain crews a sanctions violation, reshaping the ransom/insurance calculus.

## Honest limits
**RaaS is a franchise:** the operator (brand) and the affiliate (who actually breaks in) are separable, so attributing an intrusion to a brand really means attributing it to whoever used the kit. Brands **rebrand and exit-scam** (Conti->Black Basta/Royal; DarkSide->BlackMatter; ALPHV faked its own death), blurring continuity. "Russia-based" is well-established but often an inference from geography + non-prosecution. Amounts are as-disclosed/reported.

*Sources: DOJ (Colonial clawback; REvil; LockBit Operation Cronos); OFAC (Evil Corp 2019); NCA; company disclosures (UnitedHealth/Change Healthcare, MGM, Caesars, JBS); Chainalysis; the 2022 Conti Leaks. Cross-refs: Russia, Bitcoin, OFAC, DOJ, FBI, UnitedHealth, EDR_Killer/BYOVD (#240), Malware_Lineage.*
