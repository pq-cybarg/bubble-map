# Shai-Hulud npm worm (2025-26): self-replicating supply-chain compromise + the Mini variant

Shai-Hulud is a **self-propagating npm worm**: it steals a maintainer's publish token, injects a malicious install hook into all their packages, republishes an incremented patch, and repeats - turning the open-source dependency graph into a spreading medium. (This block also fixes a graph gap - the prior Shai-Hulud write-up was prose-only.)

- **First wave (Sep 16, 2025)** - ~187 packages (incl. several tied to CrowdStrike). Harvests secrets with **TruffleHog**, exfiltrates to attacker-created **public GitHub repos**, and registers victims as self-hosted GitHub Actions runners.
- **Second wave / V2 - "Sha1-Hulud: The Second Coming" (Nov 21-24, 2025)** - **700+ packages, 27,000+ malicious repos, ~14,000 secrets across 487 orgs** (counts vary by vendor and grew post-detection). Escalations: runs during **pre-install** (not post-install), uses the **Bun** runtime, and carries a **destructive dead-man's switch**. Hit Zapier, ENS, AsyncAPI, PostHog, Postman, Browserbase.
- **Mini Shai-Hulud (4th-gen; Apr-May 2026, actor "TeamPCP")** - targets the **AI-developer supply chain**, with **provenance-attestation forgery** and **AI-coding-agent persistence** - deliberately defeating the two controls (software provenance + AI dev workflows) adopted after 2025.

**Honest limits.** Totals differ by vendor and evolved as detection continued (ranges shown, not single numbers); ultimate operator attribution is not established. GitHub - the exfiltration and propagation surface - is owned by Microsoft.

It marks the **return of the worm at ecosystem scale**, but through the software supply chain (registries + CI/CD + AI agents) rather than email (ILOVEYOU) or SMB (EternalBlue).

*Sources: Palo Alto Unit42; eSentire; Zscaler; Arctic Wolf; Checkmarx; Cloud Security Alliance; Invicti/Lumific. Cross-refs: npm_Ecosystem, GitHub, Microsoft, Malware_Lineage.*
