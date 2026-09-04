# MS_Nightmare / "Nightmare Eclipse" (2026): an uncoordinated Microsoft zero-day campaign (persona claims UNVERIFIED)

In 2026 an anonymous actor - aliases **Nightmare Eclipse / Chaotic Eclipse / MSNightmare** - ran an aggressive **uncoordinated** disclosure campaign against Microsoft, publishing working proof-of-concept exploits (mostly Windows/**Defender** local privilege escalation) roughly every **~10 days**, then moving to self-hosted infrastructure after repeated takedowns.

- **The exploits (reported):** RedSun, UnDefend, BlueHammer, YellowKey, GreenPlasma, MiniPlasma, then **RoguePlanet** (a Defender LPE reproduced on a fully-patched Windows 11, Jun 2026). Attackers began exploiting BlueHammer/RedSun/UnDefend **soon after** the PoCs went public.
- **The dispute:** Microsoft says none were reported via official channels first and called uncoordinated disclosure "never justifiable"; it vaguely threatened its **Digital Crimes Unit**, then backed down after backlash.

**Honest limits (important).** The persona's **claims are self-published and UNVERIFIED** - that they are a former Microsoft employee, that MSRC deleted their account, that bounties went unpaid despite silent patches. This block does **not** assert the actor's identity, employment, or the truth of the grievances, and does **not** host or link exploit code. The provided channels (`x.com/MSNightmare2000`, `github.com/MSNightmare`, `git.projectnightcrawler.dev`) are the actor's own self-published outlets / PoC-distribution infrastructure - treated as unverified self-claims. The value here is mapping the **dispute** and the pattern (public PoCs -> in-the-wild exploitation), not endorsing either side.

It ties to the insider-threat / weaponized-disclosure branch of the lineage: like the Shadow Brokers, a case of offensive capability entering the wild - here framed as researcher-vs-vendor protest rather than theft or sale.

*Sources: The Register (May-Jun 2026); TechRadar; vendor analyses (Picus, PurpleSec, Cyderes); Microsoft public statement. Cross-refs: Microsoft, Microsoft_Defender, Coordinated_Disclosure_Norms, Malware_Lineage.*
