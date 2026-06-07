# Global Digital Identity + Age Verification / Age Assurance Regulatory Wave (2023-2026)

**Analyst brief — prepared 2026-06-05.** Jurisdiction-by-jurisdiction map of the digital-identity and age-assurance regulatory wave, with effective dates, what is mandated, the technology required, current enforcement status, and primary/credible sources.

**Cross-cutting theme — the AI/biometric driver:** A large share of these mandates do not prescribe a single method, but require "highly effective" / "accurate, robust, reliable, fair" age checks that exceed self-declaration. In practice that pushes platforms toward **facial age estimation (AI inference on a selfie)**, **ID-document + selfie/liveness matching (biometric)**, and **reusable digital-ID wallets**. Facial age estimation is the largest new source of AI-inference demand because it is the lowest-friction compliant option for the mass consumer web. Australia's official trial (Sept 2025) found age-estimation error commonly ~18 months and worse for girls, First Nations people and lower-socioeconomic groups — i.e., the tech is being mandated faster than it is proven.

---

## United Kingdom

### Online Safety Act 2023 + Ofcom "highly effective age assurance" (HEAA)
- **Instrument:** Online Safety Act 2023; Ofcom Protection of Children Codes & age-assurance guidance.
- **Key dates:** OSA received Royal Assent Oct 2023. Ofcom's children's codes finalised; **age checks became enforceable from 25 July 2025** for pornography providers (Part 5) and user-to-user/search services hosting content "harmful to children" (self-harm, suicide, eating-disorder, pornographic content).
- **Mandated:** Pornography sites and platforms serving harmful content to children must deploy **"highly effective age assurance" (HEAA)** — "technically accurate, robust, reliable and fair." Self-certification / tick-box is explicitly **not** sufficient.
- **Tech required (Ofcom non-exhaustive list):** photo-ID matching + facial recognition/liveness; **facial age estimation (AI)**; open-banking checks; mobile-network-operator (MNO) age checks; credit-card checks; **reusable digital identity / digital-ID wallets**; email-based age estimation.
- **Status (June 2026):** In force and being enforced. Ofcom has opened dozens of investigations (reported ~76 sites under investigation) and issued fines exceeding £1m for non-compliance/failure to respond to information notices.
- **Sources:**
  - https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online
  - https://www.ofcom.org.uk/online-safety/protecting-children/online-age-checks-must-be-in-force-from-tomorrow
  - https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/age-assurance
  - https://merlin.obs.coe.int/article/10358

### "BritCard" national digital ID (Starmer government, 2025)
- **Instrument:** Government policy announcement (not yet primary legislation as of mid-2026).
- **Key dates:** PM Keir Starmer announced the digital ID scheme ("BritCard"/"Brit Card") on **25 September 2025**; first live credential (a digital Veteran Card) launched **17 October 2025**; full scheme targeted for end of the parliamentary term (**2029**).
- **Mandated:** Initially proposed as **mandatory to prove right to work** (anti-illegal-migration framing) and to ease access to public services. **Government backed off compulsion in January 2026**, saying other ID forms would remain acceptable for right-to-work.
- **Tech required:** Smartphone-based digital identity wallet credential.
- **Status:** Contested. A UK Parliament petition against mandatory digital ID exceeded ~2.9m signatures (Oct 2025). Civil-liberties opposition (Big Brother Watch) strong.
- **Sources:**
  - https://en.wikipedia.org/wiki/UK_Digital_ID
  - https://www.nbcnews.com/world/united-kingdom/uk-says-will-introduce-digital-id-cards-reviving-contentious-idea-rcna233839
  - https://www.aljazeera.com/news/2025/9/29/why-is-the-uk-introducing-digital-ids-and-why-are-they-so-controversial
  - https://blogs.lse.ac.uk/europpblog/2025/10/09/britcard-uk-digital-id-scheme-eu-mistakes-identity-wallet/

---

## Australia

### Social Media Minimum Age (under-16 ban)
- **Instrument:** Online Safety Amendment (Social Media Minimum Age) Act 2024 (amends Online Safety Act 2021).
- **Key dates:** Passed Parliament **29 November 2024**; **commenced 10 December 2025**.
- **Mandated:** "Age-restricted social media platforms" must take **"reasonable steps"** to prevent under-16s from holding accounts. Covered platforms (as of commencement): Facebook, Instagram, Threads, TikTok, Snapchat, Reddit, X, YouTube, Twitch, Kick. Penalties up to ~A$49.5m for systemic failure.
- **Tech required:** Not prescribed ("reasonable steps"), but in practice **age assurance** — age inference/estimation, ID checks, or third-party verification. eSafety guidance discourages relying solely on government ID.
- **Status:** In force. eSafety reported platforms removed access to ~4.7m under-16 accounts by mid-December 2025. OAIC co-regulates privacy provisions (Part 4A s.63F).
- **Sources:**
  - https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions
  - https://en.wikipedia.org/wiki/Online_Safety_Amendment_(Social_Media_Minimum_Age)_Act_2024
  - https://www.infrastructure.gov.au/media-communications/internet/online-safety/social-media-minimum-age
  - https://privacymatters.dlapiper.com/2026/02/australias-social-media-ban-and-the-esafety-commissioners-social-media-minimum-age-regulatory-guidance/

### Age Assurance Technology Trial
- **Key dates:** Final report published **September 2025**.
- **Findings:** Tested 48 vendors / 60+ technologies. Concluded age assurance is "viable" but no single ubiquitous solution; **facial age estimation error commonly ~18 months**, worse for girls, First Nations people, lower-socioeconomic groups; tools "cannot be considered infallible." Forms the evidence base for the under-16 ban.
- **Tech relevance:** Direct test of **AI facial age estimation** + ID verification.
- **Sources:**
  - https://www.infrastructure.gov.au/department/media/publications/age-assurance-technology-trial-final-report
  - https://ageassurance.com.au/
  - https://www.biometricupdate.com/202509/australia-releases-age-assurance-technology-trial-final-report

### Digital ID Act 2024
- **Instrument:** Digital ID Act 2024 + Accreditation Rules/Data Standards.
- **Key dates:** Signed 2024; **commenced 1 December 2024** (instruments 30 Nov 2024). Phased private-sector expansion targeted **December 2026**.
- **Mandated:** Voluntary accreditation scheme for digital-ID providers; standards for identity-verification levels, privacy, security. Government system (AGDIS) built on **myID** (provider), RAM (attributes), Services Australia (exchange).
- **Tech required:** Accredited digital identity with identity-proofing levels (document verification, biometric face-matching at higher assurance levels).
- **Status:** Live. >15m myIDs and ~80m verified transactions by Dec 2025. **ACCC** is Digital ID Regulator; OAIC handles privacy.
- **Sources:**
  - https://www.digitalidsystem.gov.au/what-is-digital-id/digital-id-act-2024
  - https://ministers.finance.gov.au/financeminister/media-release/2025/12/04/more-15-million-australians-choose-simpler-safer-digital-id
  - https://www.accc.gov.au/by-industry/digital-platforms-and-services/digital-id-regulation

---

## European Union

### eIDAS 2.0 / European Digital Identity (EUDI) Wallet
- **Instrument:** Regulation (EU) 2024/1183 (eIDAS 2.0) establishing the European Digital Identity Framework.
- **Key dates:** In force 2024; **Member States must offer EUDI Wallets to all citizens by end of 2026**.
- **Mandated:** Each Member State must make available at least one EUDI Wallet; large platforms/relying parties must accept it for authentication where strong user identification is required.
- **Tech required:** Interoperable digital identity wallet; selective disclosure; supports age attestation.
- **Status:** Toolbox / Architecture Reference Framework being finalised; national wallet rollouts ramping into 2026.
- **Sources:**
  - https://digital-strategy.ec.europa.eu/en/policies/eudi-wallet-toolbox
  - https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/694487738/EU+Digital+Identity+Wallet+Home

### EU Age-Verification "mini-wallet" / blueprint
- **Instrument:** European Commission age-verification blueprint / app (subset of EUDI Wallet).
- **Key dates:** First blueprint **14 July 2025**; v2 (passport/ID-card onboarding, Digital Credentials API) **10 October 2025**; "technical readiness" announced ~**15 April 2026** (von der Leyen); app-store distribution in pilot countries expected **summer 2026**; native integration into national wallets late 2026.
- **Mandated:** Provides an age-verification app ahead of full wallets. **Pilot Member States:** France, Denmark, Greece, Italy, Spain, Cyprus, Ireland.
- **Tech required:** On-device verification using **zero-knowledge proofs (ZKP)** — platform receives a cryptographic yes/no; no identifying data leaves the phone. Onboarding via eID/passport/ID card.
- **Status:** Pilot phase, pre-mass-deployment.
- **Sources:**
  - https://ageverification.dev/
  - https://digital-strategy.ec.europa.eu/en/news/commission-makes-available-age-verification-blueprint
  - https://www.biometricupdate.com/202507/eu-moves-forward-on-age-verification-with-release-of-guidelines-software

### DSA Article 28 — protection of minors / age-assurance pressure
- **Instrument:** Digital Services Act, Art. 28(1); Commission Guidelines on protection of minors.
- **Key dates:** Guidelines published **14 July 2025**.
- **Mandated:** Platforms accessible to minors must take "appropriate and proportionate" measures (age assurance, default settings, recommender-system limits, etc.). Age-assurance methods should be "accurate, reliable, robust, non-intrusive, non-discriminatory." Following guidelines is **voluntary but used as the compliance benchmark**; the **mini-ID wallet is presented as the recommended EU age-verification solution**.
- **Tech required:** Age assurance up to age verification; ZKP-based mini-wallet preferred.
- **Status:** Guidance live; Commission using DSA enforcement (e.g., investigations into adult and other platforms) to push age verification.
- **Sources:**
  - https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors
  - https://fpf.org/blog/the-eu-commissions-approach-to-age-verification-mobile-apps-dsa-enforcement-and-challenging-national-social-media-bans/

### "Chat Control" / CSAM Regulation (CSAR)
- **Instrument:** Proposed Regulation laying down rules to prevent and combat child sexual abuse (CSAR).
- **Key dates:** Council reached political agreement on a softened text **26 November 2025**; now in **trilogue** with Parliament/Commission.
- **Mandated (current compromise):** **Mandatory scanning of (encrypted) messages dropped**; scanning becomes **voluntary**. Providers must take "all reasonable mitigation measures" — explicitly including **age verification and age assessment**.
- **Tech required:** Age verification/assessment now a core mitigation; client-side scanning no longer compelled (but voluntary scanning contested; the interim derogation expires 2026).
- **Status:** Not final — trilogue ongoing; outcome uncertain.
- **Sources:**
  - https://www.eff.org/deeplinks/2025/12/after-years-controversy-eus-chat-control-nears-its-final-hurdle-what-know
  - https://tuta.com/blog/chat-control-criticism

---

## United States

### Free Speech Coalition v. Paxton (SCOTUS)
- **Instrument:** SCOTUS decision upholding Texas HB 1181 age-verification law.
- **Key dates:** Decided **27 June 2025**, 6-3 (Thomas majority; Kagan dissent).
- **Holding:** State age-verification mandates for sites where >1/3 of content is "harmful to minors" only "incidentally" burden adults' speech; reviewed under **intermediate scrutiny** and upheld. Removes the principal First Amendment obstacle to state porn age-verification laws.
- **Tech relevance:** Greenlights state laws that in practice require **government-ID upload / digital-ID / age-estimation** age checks.
- **Status:** Binding; >20 states now have such laws.
- **Sources:**
  - https://supreme.justia.com/cases/federal/us/606/23-1122/
  - https://www.congress.gov/crs-product/LSB11354
  - https://en.wikipedia.org/wiki/Free_Speech_Coalition_v._Paxton

### State pornography age-verification laws (Louisiana onward)
- **Instrument:** Louisiana Act 440 (HB 142) and 20+ state successors (TX HB 1181, plus UT, AR, MS, AZ, SC, VA, etc.).
- **Key dates:** Louisiana **effective 1 January 2023** — first in nation. Wave of copycat laws 2023-2026.
- **Mandated:** Sites with ≥1/3 material "harmful to minors" must verify users' age. Penalties (LA): up to $5,000/day plus $10,000/violation.
- **Tech required:** **Government-ID verification** (e.g., Louisiana's **LA Wallet** digital-ID app / driver's license); commercial age-verification vendors (ID upload, **facial age estimation**, transactional data).
- **Status:** Broadly in force post-Paxton; some platforms geo-block non-compliant states.
- **Sources:**
  - https://www.moderntreatise.com/the-americas/louisiana-first-state-to-enact-age-verification-requirements-for-pornography-sites
  - https://veratad.com/regulatory-compliance/la-act-440-compliance

### App Store Accountability Acts (Utah, Texas, et al.)
- **Instrument:** Utah SB 142 (first); Texas SB 2420; plus Louisiana, Alabama, California (modified Digital Age Assurance Act).
- **Key dates:** Utah signed **March 2025**, effective **7 May 2025**, compliance deadline **6 May 2026**. Texas SB 2420 signed **27 May 2025**. Texas law **enjoined** ~late Dec 2025 (before 1 Jan 2026 effective date); **5th Circuit stayed the injunction 28 May 2026 — Texas law now in effect** pending merits. Texas App Store age verification became operational ~early June 2026.
- **Mandated:** App stores must **verify users' age at account creation** and obtain **parental consent for minors** before app downloads / in-app purchases, and share age/consent signals with developers.
- **Tech required:** Age verification at the OS/app-store layer (age category determination, ID or inference) + parental-consent flows.
- **Status:** Utah in effect (compliance ramp to May 2026); Texas in effect under stay; both face ongoing First Amendment litigation.
- **Sources:**
  - https://le.utah.gov/~2025/bills/static/SB0142.html
  - https://fpf.org/blog/comparing-enacted-app-store-accountability-acts/
  - https://appleinsider.com/articles/26/06/03/age-verification-now-mandatory-for-app-store-users-in-texas
  - https://www.bassberry.com/news/apps-and-minors-new-compliance-frontiers-and-risks-in-louisiana-utah-and-texas/

### KOSA (federal, Kids Online Safety Act)
- **Instrument:** S.1748 (Senate, 119th Cong.); H.R.6484; folded into House KIDS Act (Bilirakis).
- **Key dates:** Reintroduced **14 May 2025** (Blackburn/Blumenthal). House KIDS Act advanced out of E&C subcommittee **March 2026** (House Republicans reworked/"gutted" KOSA per critics).
- **Mandated (if enacted):** "Duty of care" + safeguards for "known" minors; differing House/Senate "knowledge" standards. Not an explicit age-verification mandate but pushes age-knowledge inference.
- **Status:** **Not enacted.** Senate and House versions diverge; uncertain outlook.
- **Sources:**
  - https://www.congress.gov/bill/119th-congress/senate-bill/1748/text
  - https://www.biometricupdate.com/202603/house-republicans-gut-kosa-as-they-advance-new-child-safety-bill

### State mobile driver's license / mobile ID (mDL)
- **Instrument:** State DMV programs; ISO/IEC 18013-5 standard; AAMVA guidelines; DHS/TSA acceptance.
- **Key dates:** ISO 18013-5 published 2021; rapid state rollout 2023-2026. As of ~Jan 2026, **21 states + Puerto Rico** have TSA-accepted mDL programs.
- **Mandated:** Voluntary credential, but increasingly the rails for age verification (e.g., LA Wallet) and identity. California issued ~2.65m mDLs (Aug 2025); Illinois launched Apple Wallet IDs Nov 2025 with **selfie + facial/liveness checks**.
- **Tech required:** ISO 18013-5 cryptographically signed mobile credential (Apple/Google/Samsung Wallet); enrollment often uses **facial matching/liveness**.
- **Status:** Expanding; verifier ecosystem and privacy norms still maturing.
- **Sources:**
  - https://www.biometricupdate.com/202605/us-states-deepen-mobile-id-rollouts-as-focus-shifts-to-verification-and-privacy
  - https://en.wikipedia.org/wiki/Mobile_driver's_license
  - https://www.federalregister.gov/documents/2024/10/25/2024-23881/minimum-standards-for-drivers-licenses-and-identification-cards-acceptable-by-federal-agencies-for

---

## China

### National network ID ("CyberID" / 网号·网证)
- **Instrument:** Measures for the Administration of National Network Identity Authentication Public Services.
- **Key dates:** Final measures promulgated **19 May 2025** (MPS, CAC + four ministries); **took effect 15 July 2025**.
- **Mandated:** State-operated centralized real-name authentication. Issues a **网号 (network number)** and **网证 (network credential)** so users authenticate to online services without handing real names/ID numbers to each platform. Officially voluntary but positioned to become the default real-name layer.
- **Tech required:** Government-issued cryptographic ID token; app-based authentication; underpinned by existing real-name + facial-recognition infrastructure.
- **Status:** Live; ~6m IDs issued by May 2025.
- **Sources:**
  - https://www.loc.gov/item/global-legal-monitor/2025-07-09/china-centralized-internet-id-system-officially-launched/
  - https://en.wikipedia.org/wiki/National_online_identity_authentication
  - https://technode.com/2025/07/16/china-rolls-out-national-online-id-card-platform-for-secure-digital-identity-verification/

### Real-name registration + minors "anti-addiction" / Minor Mode
- **Instrument:** Cybersecurity Law real-name rules; Regulations on Protection of Minors in Cyberspace; CAC "Minor Mode" guidelines.
- **Key dates:** Game time limits since 2021. Minor Mode guidelines released Nov 2024; **Minor Mode launched 29 April 2025**.
- **Mandated:** Minors' online gaming restricted to **1 hour, 8-9pm, weekends/holidays only**; device/app/app-store-level "minor mode" with daily limits, 10pm-6am blackout, 30-min break reminders, content filters. Real-name registration required across platforms.
- **Tech required:** Real-name verification (ID + facial recognition for gaming login spot-checks). Note: ~77% of surveyed minors evade via relatives' identities.
- **Status:** In force; enforcement uneven.
- **Sources:**
  - https://itif.org/publications/2025/05/09/chinas-minors-mode-blueprint-or-cautionary-tale/
  - https://www.chinalawtranslate.com/en/overview-of-protections-for-minors-online/

---

## Russia

### Digital ID, MAX messenger, SIM-to-Gosuslugi binding, VPN crackdown
- **Instrument:** Presidential decree (June 2025) on the state messenger; Ministry of Digital Development rules; SIM-registration law; VPN restrictions.
- **Key dates:** SIM-to-Gosuslugi binding mandatory since **1 January 2025**; state messenger **MAX mandatory pre-install on devices sold from 1 September 2025**; digital-ID pilot inside MAX (linked to Gosuslugi) underway late 2025-2026.
- **Mandated:** Every SIM must be tied to a **Gosuslugi** (state services) account — unregistered SIMs deactivated. Gosuslugi mobile access being funneled through MAX (SMS logins phased out). State-linked **digital ID** piloted via MAX.
- **Tech required:** State identity binding (Gosuslugi); government messenger as identity/auth chokepoint; deep-packet inspection (TSPU) for enforcement.
- **Status:** Active and tightening. Roskomnadzor reported blocking 469 VPN services (Feb 2026); international call restrictions proposed; Telegram/WhatsApp throttled to push MAX.
- **Sources:**
  - https://cyberinsider.com/russia-makes-state-backed-max-messenger-mandatory-on-devices/
  - https://en.zona.media/article/2026/04/07/russian_internet_censorship_2026
  - https://www.hrw.org/news/2026/03/12/russia-digital-iron-curtain-falls-on-internet-freedom-protection-day
  - https://www.myprivacy.blog/russia-pilots-state-linked-digital-id-through-max-app-a-deep-dive-into-digital-surveillance/

---

## Iran

### National Information Network, SIM/device-ID binding, "white SIMs," VPN ban
- **Instrument:** Supreme Council of Cyberspace decisions; National Information Network (NIN) program; pending VPN-criminalization bill.
- **Key dates:** NIN built out since ~2013; **"white SIM" tiered-access system formally instituted July 2025**; near-total blackout Jan 2026 during protests with NIN-only whitelisted access.
- **Mandated:** SIM cards/devices linked to national identity records; **two-tier internet** — government-approved individuals get unrestricted "white SIM" access while the public is filtered/throttled. VPN production/use criminalized (since 2022; bill strengthens).
- **Tech required:** Identity-bound SIM registration; NIN as sovereign network layer; whitelisting; VPN detection/neutralization.
- **Status:** Active, intensified through the 2025-2026 protest period.
- **Sources:**
  - https://circleid.com/posts/iran-expands-digital-dragnet-after-crushing-protests
  - https://carnegieendowment.org/research/2026/03/iran-wields-wartime-internet-access-as-a-political-tool
  - https://en.wikipedia.org/wiki/Internet_censorship_in_Iran

---

## India

### Aadhaar + DPDP Act 2023 / DPDP Rules 2025 (children's data & age-gating)
- **Instrument:** Digital Personal Data Protection Act 2023; DPDP Rules 2025 (esp. Rule 10).
- **Key dates:** DPDP Rules **brought into effect 13 November 2025**.
- **Mandated:** Anyone under **18 is a child** (bright line). Platforms need **verifiable parental consent** before processing children's data and must take active steps to confirm the parent is an adult, the child is a minor, and a genuine parent-child relationship — going beyond checkboxes. **Behavioral profiling / targeted ads to children prohibited.** Penalties up to ₹200 crore.
- **Tech required:** Identity/age verification; **Aadhaar-linked DigiLocker tokens designated as the authoritative credential**; virtual tokens from authorized entities. Aadhaar (~1.4bn enrolled) is the underlying identity rail.
- **Status:** Rules in force; compliance ramp ongoing; parental-consent mechanics debated as impractical/over-broad.
- **Sources:**
  - https://www.dpdpa.com/dpdparules/rule10.html
  - https://ksandk.com/data-protection-and-data-privacy/childrens-data-protection-under-indias-dpdp-rules/
  - https://www.medianama.com/2025/11/223-parental-consent-children-indias-data-protection-rules/

---

## The biometric / AI facial-age-estimation throughline

Mandates that in practice drive **AI facial age estimation** demand (selfie -> inferred age band): UK HEAA; Australia under-16 ban + age-assurance trial; EU DSA Art. 28 / mini-wallet (though EU prefers ZKP cryptographic proofs over raw biometrics); US state porn laws and app-store laws (vendors offer face estimation as low-friction option); mDL enrollment uses facial **matching/liveness** (verification, not estimation).

Mandates that drive **cryptographic digital-ID / wallet** demand (not necessarily biometric at point of use): EU EUDI wallet + ZKP mini-wallet; UK BritCard; Australia Digital ID Act/myID; US mDL; China CyberID; Russia Gosuslugi/MAX; India Aadhaar/DigiLocker.

The net effect: a structural, recurring-demand tailwind for (1) AI age-inference models and liveness/anti-spoofing, and (2) verifiable-credential / wallet infrastructure — with biometrics concentrated at onboarding and the highest-assurance checks.
