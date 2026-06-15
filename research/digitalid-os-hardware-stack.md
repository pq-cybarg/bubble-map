# Digital ID at the OS / app-store / hardware layer — the device-attestation enforcement chokepoint

*Built 2026-06-14. Structured data + edges: `digitalid-os-hardware-stack.json`. The technical enforcement layer under [[digitalid-regulatory]] and the UK push in [[spec-uk-labour-tbi-influence]]. Companion to [[digitalid-orchestration-real-incentive]] and [[age-verification-abolition]]. (WebFetch was unavailable during research; figures are from search extracts of the cited primary sources — some exact dates graded contested.)*

> Digital identity and age verification are being pushed **down from websites to the operating system, app store, and hardware** — where enforcement is binding and anonymity is hard. The EU wallet must bind to a **certified secure element**; the EU age app and US app-store laws route the duty through **Google Play Integrity** and **Apple App Attest / Declared Age Range**; the **Google-Apple mobile-OS duopoly** becomes the de facto age authority. This is the layer that turns "optional" digital ID into something a device can make binding.

## 1. eIDAS 2.0 / EUDI wallet — hardware binding
- **WSCD = the hardware root of trust.** The EU's Architecture & Reference Framework requires the wallet to bind credentials to a **Wallet Secure Cryptographic Device** (secure enclave / embedded SE / eUICC / HSM / external smartcard) sufficient to reach **Level of Assurance "High"** — which the Regulation mandates. Device-binding is proven via Wallet Unit Attestation / Wallet Trust Evidence. *Fact.*
- **Mandatory availability.** Regulation **(EU) 2024/1183** (in force May 2024) requires every member state to offer ≥1 EUDI wallet free to citizens — widely reported as **~end-2026** (exact month contested). Use is voluntary; alternatives must remain. *Fact + contested (date).*

## 2. The EU age-verification app — the Google/Apple dependency
- **Blueprint + pilots.** The Commission released a white-label age-verification app on **14 Jul 2025** (v2 Oct 2025), built by **Scytales + T-Systems**; 2025 pilots in **Denmark, France, Greece, Italy, Spain**. It uses **zero-knowledge proofs** to prove "over-18" without revealing date of birth. *Fact.*
- **The dependency.** The reference Android app plans to integrate **Google Play Integrity** (which checks for a Google-licensed OS + Play-Store install and **excludes GrapheneOS/custom ROMs**); future versions reference **Apple App Attestation**; v2 adds the **W3C Digital Credentials API**. Scytales says it "should not be restricted" to Google/Apple APIs — but Play Integrity is the documented path. *Fact (planned) + contested (Google-free alternative is intent, not shipped).*

## 3. Android — attestation, on-device mDL, OS age signals
- **Play Integrity** (replaced SafetyNet; migration ended 20 May 2025) verifies a genuine app on a **certified** device; **hardware-backed signals required from May 2025**, hard for rooted/custom-ROM devices to pass.
- **Credential Manager + ISO 18013-5 mDL** on device; **Keystore attestation** reports Software / TEE / **StrongBox** (dedicated secure element). The **W3C Digital Credentials API shipped in Chrome 141 (Sept 2025)** — websites can request an OS-issued credential for identity *and age*.
- **Play Age Signals API** gives developers users' age range/verification/supervision status; rollout began **Brazil 17 Mar 2026**, Utah May 2026, Louisiana Jul 2026. OS/store-level age determination for all downstream apps.

## 4. Apple — OS-level age sharing on Secure-Enclave attestation
- **Declared Age Range API** (WWDC 2025 / **iOS 26**): apps get an age bracket (under-13 / 13-15 / 16+) without the birth date (which "stays with Apple"); a **Feb-2026** update returns the assurance method and whether a regulation applies (Brazil, Australia, Singapore, Utah, Louisiana).
- **App Attest / DeviceCheck** generates a key in the **Secure Enclave**; Apple attests it came from a genuine device. App Store age-rating bands overhauled 2025 with per-country requirements.

## 5. App-store mandates + the duopoly chokepoint
- **App Store Accountability Acts:** **Utah SB 142** (first; effective 7 May 2025, compliance 6 May 2026), **Texas** (1 Jan 2026), **Louisiana** — all put age-verification + parental-consent duty on the **app-store operator** (Apple/Google).
- **UK Online Safety Act:** "highly effective age assurance" from **25 Jul 2025**; **90+ Ofcom investigations** by Feb 2026; fines up to **£18m or 10% of global turnover** plus blocking.
- **The chokepoint:** these laws + Play Age Signals + Declared Age Range concentrate enforcement at the **two mobile-OS gatekeepers** — the OS/store becomes the age-attestation authority for every downstream app and (via the Digital Credentials API) website.

## 6. The SIM / secure-element layer (parallel hardware root)
- **eSIM/eUICC** is GSMA-rooted and listed in the ARF as a valid local WSCD. But it's **not unbreakable**: in 2025 **Security Explorations** extracted private ECC keys from a consumer GSMA **Kigen eUICC**, undermining the "non-extractable hardware" premise for that case. *Fact.*

## 7. The civil-liberties cost
- **Alternative-OS exclusion.** Play Integrity's strong checks are tied to Google's hardware attestation, which can treat **GrapheneOS/custom ROMs as uncertified**; apps have already blocked modified firmware. Apps *can* whitelist alt-OS keys via the standard attestation API, but Play Integrity does not by default.
- **Attestation as gatekeeping.** Once sites/apps require device attestation for age/identity, only "approved" OS+hardware can access services — **ending anonymity** and threatening **sideloading** and alternative OSes. *Contested (advocacy/analysis).*

## Synthesis
The digital-ID debate is usually argued at the policy/website level, but **enforcement is migrating to the device**: eIDAS "high" assurance *requires* a certified secure element; the EU age app and US app-store laws route the duty through Google's Play Integrity and Apple's App Attest/Declared Age Range; and the Digital Credentials API lets any website demand an OS-issued credential. That makes the **Google-Apple mobile-OS duopoly the de facto identity/age authority** and turns "optional" digital ID (UK, [[spec-uk-labour-tbi-influence]]) into something the device can make binding — while attestation quietly excludes anonymity and alternative OSes.

## What is NOT asserted
- Secure-element binding/attestation is genuine security engineering — the point is it **also** becomes an access-control chokepoint.
- The EU wallet / UK digital ID is not (yet) universally mandatory at the OS level; the capability is being mandated piecemeal (app-store laws).
- Exact dates (EUDI month; iOS 26 GA; Play Age Signals per-jurisdiction) are snippet-sourced (contested); Titan M2/Tensor branding, the EU AV-app "2-minute hack", a Knox/TPM age tie-in, and a direct EFF quote are weak/under-sourced.
- Overlay edges are **excluded** from the SCC / Z3 / TLA+ proofs.

---
*Sources: [EU Digital Identity ARF (GitHub)](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/architecture-and-reference-framework-main.md); [eudi.dev high-level requirements](https://eudi.dev/1.9.0/annexes/annex-2/annex-2-high-level-requirements/); [Regulation (EU) 2024/1183](https://en.wikipedia.org/wiki/Regulation_(EU)_2024/1183); [EU age-verification blueprint (v2)](https://digital-strategy.ec.europa.eu/en/news/commission-releases-enhanced-second-version-age-verification-blueprint); [EU age-verification policy](https://digital-strategy.ec.europa.eu/en/policies/eu-age-verification); [Android Play Integrity](https://developer.android.com/google/play/integrity/overview); [Android Keystore attestation](https://developer.android.com/identity/digital-credentials/credential-issuer/keystore-attestation); [Play Age Signals](https://developer.android.com/google/play/age-signals/overview); [Chrome Digital Credentials API](https://developer.chrome.com/blog/digital-credentials-api-shipped); [Apple Declared Age Range (WWDC 2025)](https://developer.apple.com/videos/play/wwdc2025/299/); [Apple App Attest](https://developer.apple.com/documentation/devicecheck/dcappattestservice); [Apple age-assurance update (Feb 2026)](https://www.biometricupdate.com/202602/apple-updates-declared-age-range-api-for-national-state-level-age-assurance-laws); [Utah SB 142](https://le.utah.gov/Session/2025/bills/enrolled/SB0142.pdf); [Ofcom age checks](https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online); [GSMA eUICC](https://www.gsma.com/solutions-and-impact/industry-services/device-services/gsma-euicc-identity-scheme); [Security Explorations — eSIM](https://security-explorations.com/esim-security.html); [GrapheneOS attestation](https://grapheneos.org/articles/attestation-compatibility-guide).*
