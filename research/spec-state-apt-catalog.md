# State APT catalog: the major nation-state hacking groups and their sponsors

The first batch of the threat-actor catalog - the principal **state-sponsored APT groups**, each wired to its sponsoring service, the vendor/government that attributed it, and its signature operations. This is the **espionage/sabotage** branch of the malware lineage (distinct from criminal ransomware and commercial spyware).

## China
- **APT1** = PLA **Unit 61398** - Mandiant's landmark 2013 report; DOJ indicted 5 officers (2014); years of IP-theft espionage. The first public naming of a state military hacking unit.
- **Volt Typhoon** - PRC **pre-positioning** (living-off-the-land) inside US critical infrastructure (power, water, comms, transport, Guam) for disruption in a Taiwan crisis (CISA 2023-24). A strategic shift from *stealing* to *readiness to disrupt*.
- **Salt Typhoon** (MSS-linked) - breached 9+ US telecom carriers (Verizon, AT&T, T-Mobile, Lumen), incl. the **lawful-intercept/wiretap** systems - a historic counterintelligence compromise (2024-25).

## Russia
- **APT28** (Fancy Bear) = **GRU** Unit 26165 - 2016 DNC hack, WADA, TV5Monde, Bundestag (DOJ 2018).
- **APT29** (Cozy Bear) = **SVR** - DNC (2015-16), COVID vaccine theft, and the **SolarWinds "Sunburst"** supply-chain campaign (2020): a trojanized Orion update reached ~18,000 customers, breaching Treasury/Commerce/DHS + tech firms, and abused Golden-SAML into Microsoft 365/Azure AD. Behind EO 14028.
- **Sandworm** = **GRU** Unit 74455 - Ukraine grid blackouts (2015/2016), **NotPetya** (2017), Olympic Destroyer, wartime wipers. The most destructive state unit; the only confirmed cyber-caused blackouts.
- **Turla** (Snake) - FSB-linked decades-long espionage; the Snake implant was dismantled by the FBI's Operation MEDUSA (2023).

## North Korea
- **Lazarus** (Hidden Cobra) = DPRK (RGB) - uniquely **revenue-driven**: Sony (2014), WannaCry (2017), SWIFT heists (Bangladesh Bank $81M), and the largest crypto thefts (Ronin $625M, Bybit 2025) funding the regime.
- **Kimsuky** (APT43) - DPRK espionage; spear-phishing think-tanks, academics, nuclear/foreign-policy targets (OFAC-sanctioned 2023).

## Iran
- **APT35** (Charming Kitten) - IRGC-linked credential phishing of journalists, academics, dissidents, and election-adjacent targets.

## United States
- **Equation Group** = NSA Tailored Access Operations - the most sophisticated known toolset (firmware implants; Stuxnet-linked tooling); exposed by Kaspersky (2015) and the Shadow Brokers leak.

## Honest limits
Attribution is **probabilistic**: naming differs per vendor (Fancy Bear = APT28 = Sofacy = Forest Blizzard), and a "group" is a **cluster of activity**, not a fixed roster. This block records the widely-accepted consensus attributions with their sources (indictments, sanctions, CISA advisories, vendor reports); it does not assert individual identities beyond public indictments, and consolidates aliases to one node each.

*Sources: Mandiant APT1 (2013); DOJ indictments (PLA 2014; GRU 2018/2020); CrowdStrike Bear/Panda/Chollima/Kitten taxonomy; CISA advisories (Volt/Salt Typhoon); Kaspersky (Equation 2015); UN Panel of Experts (DPRK); OFAC. Cross-refs: NSA, MSS, PLA, GRU, SVR, China, Russia, North_Korea, Iran, Sandworm, Lazarus_Group, SaltTyphoon, Equation_Group, Power_Grid, TMobile, Malware_Lineage.*
