# Turning the guard into the attacker: DoubleAgent, BYOVD, and AV/EDR subversion

A recurring class of attack weaponizes the **security product itself** - abusing legitimate OS features or signed drivers to hijack or kill antivirus/EDR. Same theme as the MS_Nightmare Defender exploits: the defender is the attack surface.

## DoubleAgent (Cybellum, March 2017)
DoubleAgent abuses Microsoft's **Application Verifier** - a legitimate Windows runtime-verification tool. An attacker registers a malicious **"verifier provider" DLL** for a target process; Windows then loads that DLL into the process on **every start** - persistent, pre-boot code injection into arbitrary processes. The marquee abuse is hijacking the **antivirus process itself**: the 2017 PoC weaponized/neutralized most major AV/endpoint products (Avast, AVG, Avira, Bitdefender, ESET, F-Secure, Kaspersky, Malwarebytes, McAfee, Norton, Panda, Trend Micro, Comodo).

- **Honest limit:** it requires prior admin/code-exec to register the provider - a persistence + injection + defense-evasion technique, **not** a remote break on its own.
- **Mitigation:** run AV/EDR as a **Protected Process Light (PPL)** so non-PPL code can't inject into the security service.

## BYOVD & EDR-killers
**Bring-Your-Own-Vulnerable-Driver** loads a legitimately **signed but vulnerable** kernel driver to gain kernel execution and disable protections - the engine behind most **EDR-killers** (e.g. **AuKill**; **EDRKillShifter**, tied by IR vendors to the **RansomHub** ecosystem), used to blind endpoint defense before ransomware detonation. Microsoft's counter is the **Vulnerable Driver Blocklist** (HVCI/WDAC), but coverage lags newly-abused drivers.

## Why it's on the map
This is the **living-off-the-land / defense-evasion** branch of the malware lineage: abuse trusted OS mechanisms (Application Verifier; later AppInit/IFEO/COM hijacks; signed drivers) rather than novel exploits. DoubleAgent (2017, user-mode) and the 2026 MS_Nightmare Defender LPEs are two eras of the same idea - **weaponize the guard**.

*Sources: Cybellum DoubleAgent disclosure (Mar 2017); Microsoft Application Verifier docs + PPL; MITRE ATT&CK (defense evasion); IR vendor reporting on BYOVD + AuKill/EDRKillShifter. Cross-refs: Microsoft, Microsoft_Defender, MS_Nightmare, Malware_Lineage.*
