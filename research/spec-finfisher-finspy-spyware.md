# FinFisher / FinSpy: German-made "lawful intercept" spyware, and the repression apparatus it served

FinFisher/FinSpy is commercial **"lawful intercept"** spyware sold by the **Gamma Group** (Gamma International, UK/Germany; **FinFisher GmbH**, Munich, with **FinFisher Labs** and partner **Elaman GmbH**) to governments. The suite is a full-device implant: calls, messages, keystrokes, files, mic, camera, location. It was marketed as a crime-fighting tool. The documented deployments are against **journalists, lawyers, opposition, and diaspora activists**.

This block was thin. The missing piece is not another product description. It is the **harm pattern** that human-rights litigators keep stating in the same words: **digital surveillance is often followed by imprisonment and torture** ([ECCHR](https://www.ecchr.eu/en/case/surveillance-software-germany-turkey-finfisher/)). FinSpy is the collection layer. The client state's security service is the action layer. People then disappear into incommunicado detention, political prison, prison-labor / re-education systems, or death in custody. That pipeline is **documented as a pattern**. A courtroom-grade proof that *this specific implant caused that specific death* is **rare**, and is graded as such.

> **Method.** Targeting and C2 geography = FACT (Citizen Lab scans; Amnesty forensics; leaked contracts; court filings). Client-state prison, disappearance, torture, and death-in-custody records = FACT from HRW/Amnesty/BICI/ECRF, independent of any one implant. The join - "FinSpy mapped the network, then the apparatus took people" - is the **strong, repeated inference** of the rights orgs who sued Gamma; it is **not** a forensic kill-list. No private tipsters. No conflation with NSO/Pegasus (Khashoggi is a Pegasus case).

## 1. The product (2011 SpyFiles -> 2020 Mac/Linux)

WikiLeaks **SpyFiles** (2011) published Gamma's own brochures. The stack was never "one trojan":

- **FinSpy** - the implant (Windows first; later Android/iOS/BlackBerry/Symbian; **macOS and Linux** first published by [Amnesty, Sep 2020](https://www.amnesty.org/en/latest/research/2020/09/german-made-finspy-spyware-found-in-egypt-and-mac-and-linux-versions-revealed/)).
- **FinFly USB / FinFly Web / FinFly ISP** - delivery. FinFly ISP is the important one: **network-injection at the ISP**, so the target does not even have to open a malicious attachment. Citizen Lab later found equipment consistent with this class of injection in Egypt.
- Modular spying: keylog, file theft, Skype/audio, webcam, geolocation, remote command. Amnesty's 2020 Mac sample (`Jabuka.app`) and Linux sample (`PDF`) used LLVM-Obfuscator and a multi-stage loader.

Gamma said it sold only to governments. That is the vendors' framing, and it is also why the abuse cases are **state** cases.

## 2. Global proliferation (Citizen Lab)

[You Only Click Twice](https://citizenlab.ca/2013/03/you-only-click-twice-finfishers-global-proliferation-2/) (Mar 2013) found **FinSpy C2 in 25 countries**, including Bahrain, Ethiopia, Turkmenistan, UAE, Vietnam, plus Western hosting. Later scanning ([Pay No Attention to the Server Behind the Proxy](https://citizenlab.ca/2015/10/pay-no-attention-to-the-server-behind-the-proxy-mapping-finfisher-and-anonymizer/), Report 64) raised that to **~32 countries / 33 likely government users**, with named entities where the IP could be tied to a department:

- **Egypt** - Technology Research Department (TRD)
- **Indonesia** - National Encryption Body (Lembaga Sandi Negara)
- **Bangladesh** - Directorate General of Forces Intelligence
- **Kenya** - National Intelligence Service
- plus Ethiopia, Italy (multiple), Saudi Arabia, Venezuela, Angola, Belgium (federal police), and others.

C2 in a country is **not** by itself a confession that the interior ministry ran a given campaign. Citizen Lab grades that carefully; so does this block. It **is** evidence of a government-grade deployment, because Gamma sold to governments.

## 3. The harm pattern (what "disappeared / imprisoned / died" actually means here)

Do not collapse five different facts into one conspiracy:

1. **FinSpy was in the hands of those governments** (C2, samples, contracts, court files) = FACT.
2. **Those governments independently run enforced-disappearance, torture, political-prison, and in some cases prison-labor / re-education systems** = FACT, with huge denominators, sourced below.
3. **The product's purpose is to map a target's files, contacts, movement, and conversations** = FACT (Gamma's own marketing; forensic modules).
4. **Rights orgs (HRW, ECCHR, Privacy International, Amnesty) describe the join**: once a device is owned, the security service has the graph of the person and the people around them, and in these states that graph feeds interrogation, arrest, and incommunicado detention. ECCHR's sentence is the through-line: *digital surveillance is often followed by imprisonment and torture.*
5. **A named person's death or camp sentence caused by a named FinSpy sample** is usually **not** in a forensic report. That last step is **inferred from (1)+(2)+(3)+(4)**. Grade it. Do not pretend a kill-list exists.

"Labor camp" in this corpus means the **client state's existing detention system** - Ethiopia's political prisons (Maekelawi and after), Egypt's NSA incommunicado sites, Bahrain's Jau, Turkey's post-coup mass detention, Vietnam's imprisonment of bloggers (and the historical re-education system), Turkmenistan's prison-labor colonies (Ovadan-Depe). It does **not** mean FinSpy shipped people to a camp as a software feature.

## 4. Bahrain (2011-2012) - the first public abuse case

In 2012 Citizen Lab and Bahrain Watch unpacked a **suspicious-email campaign targeting Bahraini activists**. The attachments were FinSpy. Between 2010 and 2012 Bahrain used FinFisher against **lawyers, journalists, activists, and opposition leaders**, in-country and in the diaspora ([Citizen Lab Report 64](https://citizenlab.ca/2015/10/pay-no-attention-to-the-server-behind-the-proxy-mapping-finfisher-and-anonymizer/); [The Verge, 2015](https://www.theverge.com/2015/1/21/7861645/finfisher-spyware-let-bahrain-government-hack-political-activist)).

That campaign sat on top of a repression wave the **Bahrain Independent Commission of Inquiry** had already documented after the 2011 Pearl Roundabout crackdown: systematic torture, deaths in custody, mass detention. The spyware did not create Jau Prison. It is the collection tool used against the people still trying to organize after it.

Accountability, such as it is:

- **2015:** the UK National Contact Point for the OECD Guidelines found **Gamma International in breach seven times** - the first piece of software the OECD process had ever dinged on human-rights grounds.
- **Feb 2023:** UK High Court allowed **Dr. Saeed Shehabi** and **Moosa Mohammed** (London-based Bahraini activists; Mohammed had been arrested, detained, and tortured in Bahrain before fleeing) to sue Bahrain over **September 2011 FinSpy infections** of their UK laptops ([The Record](https://therecord.media/finspy-finfisher-bahrain-activists-spyware-uk-high-court-ruling)).
- **Jul 2026:** UK Supreme Court, 3-2, held that remotely infecting a computer **physically in the UK** is an act in the UK, **stripping Bahrain of state immunity** for that civil claim.

Those two men were not disappeared. They were in Britain. The case matters because it is the first major court path for *extraterritorial* FinSpy targeting, and because Mohammed's prior torture is the in-country half of the same apparatus.

## 5. Ethiopia - FinSpy on the diaspora, prisons at home

Ethiopia is the best-documented **FinSpy + domestic-repression** pair.

- Citizen Lab: a FinSpy sample using **Ginbot 7** (banned opposition) imagery as bait, talking to a C2 on **Ethio Telecom**, the state monopoly.
- [HRW, Mar 2014, *They Know Everything We Do*](https://www.hrw.org/news/2014/03/25/ethiopia-telecom-surveillance-chills-rights): Ethiopia combined **Chinese ZTE** one-click wiretapping of the national phone network with **Gamma FinFisher** and **Hacking Team RCS** against the diaspora in the US, UK, Norway, and Switzerland. Intercepted Skype showed up on pro-government sites. Recorded calls were **played in abusive interrogations**. Torture of political prisoners is independently documented. Phone networks were shut during protests; locations were pinned from mobiles.
- Concrete diaspora hit: **Yohannes Alemu** (Norwegian citizen, Ginbot 7). Security detained his wife while she visited family in Addis Ababa. He then received a FinFisher-infected email ([HRW](https://www.hrw.org/news/2014/04/07/ethiopias-borderless-cyberespionage)).
- **Kidane v. Ethiopia** (EFF, D.D.C. 2014; *Doe v. FDRE*, 189 F. Supp. 3d 6): a US citizen in Silver Spring, Maryland, had FinSpy on his home PC **31 Oct 2012 - 18 Mar 2013** (it went quiet days after Citizen Lab's public disclosure). It recorded dozens of Skype calls, emails, and even his son's middle-school web search. Traces pointed at an Ethiopian C2. The Wiretap Act / FSIA claims were **dismissed** - Ethiopia is immune, not "the infection didn't happen." The plaintiff used a community pseudonym **to protect family in Ethiopia**. That safety reason is the point.

Ethiopia later added **Cyberbit** (Israeli) to the same targeting program ([Citizen Lab / VOA, 2017](https://www.voanews.com/a/ethiopia-targeted-dissidents-journalists-in-20-countries-with-israeli-spyware/4154014.html)) - at least the **third** spyware vendor HRW counted since 2013. The Oromo protest years (2014-16) saw **hundreds killed** by security forces; that body count is a state-violence fact, not a FinSpy autopsy.

*Grade:* FinSpy in Ethiopian government hands, used on named diaspora targets = FACT. That the same security services tortured and disappeared people inside Ethiopia = FACT. That FinSpy's contact-graph made some of those domestic arrests possible = **strong inference, not a named-victim forensic chain**.

## 6. Egypt - contracts in the SSI vault, then the disappearance machine

When protesters broke into **State Security Investigations** offices in 2011, they found **contracts for the sale of FinSpy to Egyptian authorities** ([Amnesty, Sep 2020](https://www.amnesty.org/en/latest/research/2020/09/german-made-finspy-spyware-found-in-egypt-and-mac-and-linux-versions-revealed/)). Citizen Lab later named Egypt's **Technology Research Department** as a FinFisher user.

Amnesty's 2020 Security Lab work then found:

- **NilePhish** distributing **FinSpy for Windows** via a fake Adobe Flash download, aimed at Egyptian independent media and civil society.
- Previously unpublished **macOS and Linux** FinSpy samples on a *different* operator's exposed server.

**Honest limit, in Amnesty's own words:** they have **not** documented human-rights violations by NilePhish *directly linked* to FinFisher products. The Windows distribution is a targeting fact. The disappearance campaign is a parallel fact.

The parallel fact is large. Under Sisi, the NSA (the renamed SSI) has run **enforced disappearance as a method**: incommunicado detention from days to **23 months**, torture to produce confessions, then terrorism prosecutions. The Egyptian Commission for Rights and Freedoms' **Stop Enforced Disappearance** campaign documented **~2,700** cases over five years. Amnesty's *Officially, You Do Not Exist* and HRW's *We Do Unreasonable Things Here* (2017) describe the same pipeline. EIPR and partners count **4,202 death sentences** (2013-23) and **448 executions**, many on torture-tainted confessions; Rabaa (14 Aug 2013, **>=817** killed in one day) is a massacre, not a spyware event, and is not blamed on FinSpy here.

*Grade:* FinSpy sold to Mubarak-era SSI, still in the Egyptian stack, used in 2019-20 civil-society targeting = FACT. Egypt's disappearance / torture / death-in-custody system = FACT. Join = the same inference as Ethiopia and Bahrain, and Amnesty refuses to over-claim the NilePhish link.

## 7. Turkey - unlicensed German export, then the post-coup cage

FinSpy appeared in Turkey in **summer 2017** on a **fake opposition-campaign website**, disguised as an app for anti-government demonstrators ([ECCHR](https://www.ecchr.eu/en/case/surveillance-software-germany-turkey-finfisher/)). That is mass-targeting of protesters, not a single dissident email.

Germany has **issued no export licences for intrusion software since 2015** (EU dual-use / Wassenaar). GFF, RSF, ECCHR, and netzpolitik.org filed a **criminal complaint in July 2019**. Munich prosecutors searched FinFisher offices in Germany and Romania (Oct 2020), **seized company accounts**, and the group (**FinFisher GmbH, FinFisher Labs, Elaman**) **filed insolvency in March 2022**. In **May 2023** they **charged four managers** with intentionally exporting dual-use spyware to non-EU countries without a licence - the Turkey sale is the centre of that indictment.

The client-state half: after the **July 2016** coup attempt, Turkey **arrested >50,000**, **fired ~140,000**, and shut hundreds of media outlets. Journalists and opposition are the documented FinSpy target class. Again: the spyware maps; the emergency-decree state cages.

## 8. Vietnam, Turkmenistan, UAE, and the rest of the C2 atlas

These are **C2 / sample facts** plus **independently documented prison systems**. They are listed so the atlas is not just Bahrain/Ethiopia/Egypt/Turkey. They are **not** a claim that every C2 host ran a FinSpy-to-camp conveyor.

- **Vietnam.** Citizen Lab found an **Android FinSpy Mobile** sample with a Vietnamese C2 that also **exfiltrated SMS to a local phone number** - a strong in-country-operator tell. Vietnam imprisons bloggers and democracy activists; it also has a historical **re-education / prison-labor** system. Join: graded inference, not a named-camp roster.
- **Turkmenistan.** Persistent FinSpy C2 in one of the most closed states on earth. Independent reporting on **Ovadan-Depe** and prison-labor colonies is a state-violence fact. No public FinSpy-victim forensic report was located for this block.
- **UAE.** Documented FinSpy targeting of HRDs (Amnesty/Citizen Lab list). Later UAE cases (Ahmed Mansoor, etc.) are **Pegasus**, which is a different vendor - do not mix them.
- **Uganda, Myanmar** - later FinSpy versions kept turning up after the German licensing wall, which is why Munich prosecutors treated "no licence issued" as the crime.

## 9. What happened to the vendor

- **2011** WikiLeaks SpyFiles.
- **2012-15** Citizen Lab / Bahrain Watch / Privacy International / ECCHR OECD complaints (Gamma UK + Trovicor).
- **2015** OECD UK NCP breach finding; EU intrusion-software licensing.
- **2019-23** German criminal case; **2022 insolvency**; **2023 charges** against four managers.
- **2023-26** UK Bahrain civil litigation, immunity stripped.

FinFisher-the-company is dead. The **dual-use export gap** is not: ECCHR notes updated FinSpy still appearing in Turkey, Egypt, and Myanmar after 2015, and the rest of the mercenary market (NSO/Pegasus, Intellexa/Predator, Paragon, Candiru) filled any hole Gamma left. See [[spec-spyware-vendor-catalog]] and [[spec-citizen-lab]].

## Honest limits

- **"Lawful intercept"** is vendor copy. Documented targeting of journalists and opposition is the dual-use gap.
- **Operator attribution** (which agency, which campaign) is usually infrastructure + bait + victim, not a confession.
- Amnesty, Citizen Lab, HRW, ECCHR, Privacy International, GFF, RSF are **research + advocacy parties**. Their forensics are heavily corroborated (samples, C2, court files). Their framing is evidence, not a verdict.
- **Kidane** is a court pseudonym; this block uses it the way the docket does. No private biographical detail.
- This is **not** the Pegasus/Khashoggi file. Different vendor, different kill-chain, different evidence grade.
- Overlay edges. Excluded from the SCC / Z3 / TLA+ proofs.

## What is NOT asserted

- FinSpy does not "kill people" as a software function.
- There is no unified FinSpy kill-list, and none is inferred from adjacency.
- A specific named death, execution, or labor-camp sentence is **not** attributed to a specific implant unless a court or forensic report already says so. None of the primary sources above make that last-mile claim for a named decedent.
- Egypt's Rabaa massacre and Ethiopia's Oromo-protest killings are **state-violence facts** in client states, not FinSpy autopsies.
- No private source, tipster, or underground persona is cited.

*Sources: [Amnesty Security Lab, Sep 2020 (Egypt; Mac/Linux)](https://www.amnesty.org/en/latest/research/2020/09/german-made-finspy-spyware-found-in-egypt-and-mac-and-linux-versions-revealed/); [Citizen Lab, You Only Click Twice, 2013](https://citizenlab.ca/2013/03/you-only-click-twice-finfishers-global-proliferation-2/); [Citizen Lab Report 64, 2015](https://citizenlab.ca/2015/10/pay-no-attention-to-the-server-behind-the-proxy-mapping-finfisher-and-anonymizer/); [HRW Ethiopia telecom surveillance, 2014](https://www.hrw.org/news/2014/03/25/ethiopia-telecom-surveillance-chills-rights); [HRW Ethiopia borderless cyberespionage](https://www.hrw.org/news/2014/04/07/ethiopias-borderless-cyberespionage); [EFF, Kidane v. Ethiopia](https://www.eff.org/cases/kidane-v-ethiopia); [ECCHR FinFisher/Turkey case](https://www.ecchr.eu/en/case/surveillance-software-germany-turkey-finfisher/); [GFF criminal complaint / insolvency](https://freiheitsrechte.org/en/themen/freiheit-im-digitalen-zeitalter/export-von-uberwachungssoftware); [EDRi on account seizure](https://edri.org/our-work/criminal-complaint-against-illegal-export-of-surveillance-software-is-making-an-impact-the-finfisher-group-of-companies-ceases-business-operations-after-its-accounts-are-seized-by-public-prosecutor/); [UK High Court Bahrain FinSpy suit, 2023](https://therecord.media/finspy-finfisher-bahrain-activists-spyware-uk-high-court-ruling); [The Verge, A Spy in the Machine, 2015](https://www.theverge.com/2015/1/21/7861645/finfisher-spyware-let-bahrain-government-hack-political-activist); [HRW, We Do Unreasonable Things Here (Egypt, 2017)](https://www.hrw.org/report/2017/09/06/we-do-unreasonable-things-here/torture-and-national-security-al-sisis-egypt); [Amnesty, Officially You Do Not Exist (Egypt disappearances)](https://www.amnestyusa.org/wp-content/uploads/2017/04/embargoed_13_july__egypt_officially_you_do_not_exist.pdf). Cross-refs: Gamma_Group, FinSpy, Commercial_Spyware_Market, Dual_Use_Export_Gap, Enforced_Disappearance, Citizen_Lab, Hacking_Team, NSO_Group, Intellexa, WikiLeaks, Malware_Lineage, Egypt, Ethiopia, Bahrain, Turkey, Vietnam, Turkmenistan, UAE.*
