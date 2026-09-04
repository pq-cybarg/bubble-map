# ILOVEYOU / Love Bug (2000): the mass-mailer worm that outran the law

May 2000: a VBScript email worm spread to **~45 million machines in ~24 hours**, one of the first truly global malware events. It matters on the map for two reasons.

- **The mechanism (fact).** A VBScript attachment - `LOVE-LETTER-FOR-YOU.TXT.vbs`, hidden by Windows' default "hide known extensions" - auto-mailed itself to the victim's entire Outlook address book and overwrote local media files. Windows Scripting Host + pure social engineering ("ILOVEYOU").
- **The law gap (fact).** The author, a Manila student, was arrested but **released** - the Philippines had no applicable computer-crime statute in 2000, so charges were dropped. This directly catalyzed the Philippine **E-Commerce Act (RA 8792)** weeks later and fed the global push for cybercrime law (Budapest Convention, 2001).

Damage estimates run **~$5.5B-$15B** (analyst estimates, wide spread). It's the archetypal mass-mailer - the direct ancestor of later email worms and today's phishing / supply-chain lures - and the first big demonstration of **jurisdiction-arbitrage cybercrime**: attacker in one state, victims worldwide, no extraditable offense.

*Sources: CERT/CC advisories; contemporaneous press; Philippine RA 8792. Cross-refs: Malware_Lineage, Cybercrime_Law_Gap, spec-shadow-brokers-eternalblue, spec-shai-hulud-npm-worm.*
