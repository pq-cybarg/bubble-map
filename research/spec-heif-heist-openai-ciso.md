# HEIF Heist + OpenAI: a real bug-bounty report, a burned disclosure, then an apology

On **25 Jul 2026**, three researchers at **Hacktron AI** (Harsh Jaiswal, Mohan Pedhapati, Rahul Maini) chained a **libheif** heap overflow in **Discourse** (the software behind **community.openai.com**) with an **OpenAI SSO** flaw, took over employee **ChatGPT / Codex** sessions, and proved access to OpenAI's internal GitHub monorepo by having an employee's Codex open a **harmless PR** (`#1186742` in `openai/openai`). They stopped. OpenAI patched its side in **~14 hours** and later paid **$6,500**. Discourse patched in a weekend.

That is the **technical** story ([Hacktron](https://www.hacktron.ai/blog/hacking-openai); [heif-heist.com](https://heif-heist.com); WSJ via [The Verge](https://www.theverge.com/ai-artificial-intelligence/997444/openai-hack-claude-heif-heist) / [TechCrunch](https://techcrunch.com/2026/09/18/researchers-used-anthropics-claude-to-hack-into-openai/)).

The **process** story is why this block exists. **LiveOverflow** (Fabian Faessler; acknowledged on the Hacktron post) published a 19-post thread on **19 Sep 2026** arguing OpenAI's **CISO fumbled the disclosure**: no thank-you, a demand for a written inventory of data accessed, anger at a Black Hat/DEF CON screenshot of a non-sensitive PR, "$6,500 and community.openai.com is out of scope," then calling a draft report a **"stunt hacking document."** Hacktron flipped to **malicious compliance** (OpenAI-only headline, `not-openai` GitHub mirror, YouTube clip the CISO did not want shared). Advice from others pushed them to journalists; it became a **WSJ exclusive**. LiveOverflow contrasts **Vercel** (collaborative Next.js/libheif disclosure) and his own **Google-sponsored vuln videos**. He also notes OpenAI **never threatened legal action**, they still talked to lawyers, and this sat **right after the Hugging Face eval-incident**. **Later the same day, the CISO reached out and apologized**; LiveOverflow says they are good, and that the thread was **his personal opinion**, not the disclosure plan, because he felt **@rootxharsh** and **@S1r1u5_** were treated unkindly.

> **Grade the thread as a primary-source *account*, not a verdict.** Technical chain + bounty + patches = FACT (Hacktron, Discourse GHSA, Bugcrowd scope note, WSJ). The CISO's tone and "fumble" = LiveOverflow's labeled opinion, later partially walked back by the apology. Do not infer OpenAI corporate intent from one security lead's Slack. Overlay; excluded from the proofs.

## 1. The chain (architecture only - no exploit)

Hacktron's own diagram, restated as a dependency stack (the xkcd 2347 point):

1. **libheif** (and **libde265**) - native C/C++ HEIF/HEIC/AVIF decoder. A heap overflow / OOB R+W on crafted overlay image items (CVE-2026-32882 in secondary write-ups; upstream had changed the code a year earlier **without marking it a security fix**, so **Debian 12/13** shipped vulnerable 1.19.7/1.19.8).
2. **ImageMagick** `magick` - Discourse's fallback when **FastImage** cannot handle HEIF.
3. **Discourse** image upload on **community.openai.com**.
4. **OpenAI SSO** (`auth.openai.com` / "Sign in with OpenAI") - the **escalation that is actually OpenAI's**. Hacktron: Discourse was *one* proof; any compromised first- or third-party service on that SSO would have given the same ChatGPT/Codex access.
5. Employee **ChatGPT / Codex** with a **GitHub** connector.
6. Internal monorepo **`openai/openai`**. Proof: Codex-opened PR, no code read. WSJ sources called the repo a store of "algorithmic secrets"; that phrase is **WSJ's sourcing**, not a Hacktron inventory.

Time: Opus 4.8 found the missing backport; **Opus 5** (released that evening) produced a working ASLR-on exploit in hours; RCE on Discourse Cloud by 10:00 UTC 25 Jul; OpenAI instance the same window; **<72 hours** discovery-to-monorepo-proof. HEIF Heist as a **two-month** campaign across Slack, Meta, GitHub Enterprise, Next.js, Rails, etc. cost **<$3,000 in tokens**, three people. Only **Shopify** (of the named targets) detected the probing. GPT-5.6 Sol later cut per-target adaption to ~1-3 days.

**This is the inverse of the curl slop problem** ([[spec-reproducibility-crisis]]). There, AI made *fake* reports free. Here, AI made a *real* memory-corruption campaign cheap enough for a three-person shop. Both break the old assumption that "turning a public parser bug into a reliable exploit is too expensive for ordinary attackers."

The blast-radius rhyme is old: **ImageTragick**, **ForcedEntry** (Pegasus / iMessage), **libwebp BLASTPASS** (Citizen Lab). HEIF Heist cites all three. An image parser is a privileged process sitting under every upload and every thumbnail.

## 2. What OpenAI actually did on the bug (fact)

- Bugcrowd report **25 Jul ~08:00-10:00 UTC**.
- OpenAI-side fix confirmed **22:49 UTC** the same day (~14h).
- Discourse: HackerOne Saturday, reply Sunday, fix Monday, GHSA-vhm9-85gw-x335 **28 Jul**, ImageMagick sandboxing as defense-in-depth.
- **1 Sep 2026:** **$6,500** bounty. OpenAI's written scope note: testing **community.openai.com was explicitly out of program**; the award is the **SSO/OpenAI-side** finding, not the Discourse RCE.

A $6,500 payout against employee-account takeover plus a path into the monorepo is the number the thread and the press keep repeating. It is a **fact of the award**, not a proof that OpenAI "undervalued" the bug - that valuation complaint is **opinion**.

## 3. The LiveOverflow thread (19 Sep 2026) - process, graded

Public thread: [x.com/LiveOverflow/status/2101252692635004997](https://x.com/LiveOverflow/status/2101252692635004997). Screenshots of Slack. Personal opinion, later qualified.

Documented beats, in order:

| Beat | What he says happened | Grade |
|---|---|---|
| Shared Slack after the report | CISO "pretty sad" they tested GitHub via the PR; that was beyond "establish good faith security research"; **no thank-you** | LiveOverflow's account of a private Slack (screenshots). Treat as **his contemporaneous record**, not a transcript we independently hold. |
| Data-accessed write-up | Ask for a timeline and "written description of data accessed or downloaded" | Fair IR request **and** felt antagonistic; later **WSJ confirmed they didn't do anything bad** |
| Black Hat / DEF CON | Shared a PR screenshot with OpenAI employees; recreation shows nothing sensitive; bugs already fixed; CISO unhappy again | Account |
| Mid/late August | Tried to keep a working relationship; no reaction. Then shared HEIF Heist publication plans (OpenAI as **one of many** stories) | Account |
| @S1r1u5_ outreach | Tried to turn it into a positive story; "Hacktron is a meaningless small company to them" | Account + labeled bitterness |
| 1 Sep bounty | $6,500 / community OOS "felt like confirmation they really don't like us"; ChatGPT itself cannot read the Bugcrowd policy cleanly | Award = fact. Feeling = opinion. Policy-misread anecdote = weak. |
| Draft share | CISO called it unprofessional, a **"stunt hacking document,"** asked if they believed it was objective/unbiased/free of hyperbole | Account of a private reaction. The phrase is the load-bearing quote of the thread. |
| Legal chill | **OpenAI never threatened legal action.** They still got scared and talked to lawyers. | Important non-claim, from him. |
| Malicious compliance | You don't want the screenshot -> make it explicit. You don't want OpenAI in a multi-target title -> **make the article only about OpenAI**. You don't want the PR link -> [github.com/not-openai/openai/issues/1186742](https://github.com/not-openai/openai/issues/1186742). YouTube: [gjHh9g7yo9Y](https://www.youtube.com/watch?v=gjHh9g7yo9Y). "Hello Streisand strategy." | Observable publication choices = fact. "Streisand" = his frame. |
| WSJ | Others said call journalists; "what could have been yet another boring vulnerability disclosure" became a WSJ exclusive; "all just because CISO was pissed (**my opinion**)" | WSJ existence = fact. Causal "because CISO was pissed" = **his labeled opinion**. |
| Hugging Face context | "Right after the Hugging Face incident"; can understand if the CISO was stressed and "didn't want to deal with three random guys" | HF incident is a separate, documented OpenAI eval/safety event. Stress-as-excuse = speculation he himself hedges. |
| Counterexamples | **Vercel** CEO/CTO collaboration on the Next.js/libheif reproduction ([Vercel blog](https://vercel.com/blog/reproducing-disclosing-and-fixing-the-libheif-vulnerability-with-hacktron-and-the-maintainers)). His Google-Cloud sponsored vuln videos. | Contrast = fact of those disclosures. |
| Close | "Sad for us at Hacktron... attempt to get a foot in the door... CISO got pissed and the bridge we wanted to build was burnt... maximum publicity" | Motive statement from him. |
| Same-day follow-up | **"CISO reached out and apologized. We are good."** Thread was **not** part of the disclosure plan; personal opinion; he wanted to say Harsh and Sirius were treated unkindly. | Walk-back is part of the public record. Do not freeze the story at "bridge burned." |

## 4. Why it is on this map

- **OpenAI** is already a core node. This is the **security-process** overlay: a frontier lab that ships Codex, pays bounties, and still produced a disclosure conversation its own later apology implies went badly.
- **HEIF Heist** is a **parser-under-the-app** class, same family as ForcedEntry / BLASTPASS - a link into the spyware/malware lineage without claiming Hacktron is a spyware vendor.
- **Anthropic Claude (Opus 4.8/5) and GPT-5.6 Sol** compressed exploit development. That is an **AI-security economics** fact sitting next to the funding graph, not a "Claude attacked OpenAI" cartoon. Hacktron used the models; the models are tools.
- **Bug-bounty scope games** (community.openai.com OOS while SSO sat behind it) are the dual of the curl slop collapse: one side cannot process noise, the other side **narrowed the program until a path into employee GitHub was a $6,500 SSO finding**.
- **Streisand / WSJ** is what happens when a vendor wins the argument in Slack and loses it in public. Vercel is the control case.

## Honest limits

- LiveOverflow is a **party** (Hacktron-adjacent; named in the blog acknowledgements). Screenshots are his. The apology is also his report of a private message.
- Hacktron's **July blog voice** thanks OpenAI for speed; the **September thread** is the sour aftertaste. Both are on the record; do not collapse them.
- No private Slack is in this repo. No employee names, no repo contents, no exploit.
- "Algorithmic secrets" is **WSJ anonymous sourcing**, not a file listing.
- CISO identity: public-role **Dane Stuckey** is OpenAI's CISO in the Hugging Face postmortem coverage; LiveOverflow's thread does **not** name him. This block does not treat the Slack quotes as a named-person dossier.
- Overlay. Not in SCC / Z3 / TLA+.

## What is NOT asserted

- OpenAI did not "cover up" a breach. They patched in 14 hours and paid a bounty.
- The researchers did not dump the monorepo. They opened a proof PR and stopped. WSJ: they did not do anything bad.
- The CISO's apology is not erased by the thread, and the thread is not erased by the apology.
- This is not a FinSpy/Pegasus campaign. Image-parser **rhyme** only.
- No unified "OpenAI vs researchers" conspiracy.

*Sources: [LiveOverflow thread, 19 Sep 2026](https://x.com/LiveOverflow/status/2101252692635004997); [Hacktron, Hacking OpenAI, 13 Sep 2026](https://www.hacktron.ai/blog/hacking-openai); [HEIF Heist](https://heif-heist.com); [Discourse GHSA-vhm9-85gw-x335](https://github.com/discourse/discourse/security/advisories/GHSA-vhm9-85gw-x335); [Vercel / Hacktron libheif write-up](https://vercel.com/blog/reproducing-disclosing-and-fixing-the-libheif-vulnerability-with-hacktron-and-the-maintainers); [The Verge / WSJ](https://www.theverge.com/ai-artificial-intelligence/997444/openai-hack-claude-heif-heist); [TechCrunch](https://techcrunch.com/2026/09/18/researchers-used-anthropics-claude-to-hack-into-openai/); [YouTube gjHh9g7yo9Y](https://www.youtube.com/watch?v=gjHh9g7yo9Y); [not-openai issue 1186742](https://github.com/not-openai/openai/issues/1186742); [OpenAI Bugcrowd](https://bugcrowd.com/engagements/openai). Cross-refs: OpenAI, Anthropic, Hugging_Face, Vercel, Discourse, libheif, HEIF_Heist, Hacktron_AI, LiveOverflow, Bugcrowd, Dual_Use_Export_Gap is the wrong analog - this is bounty-scope; spec-reproducibility-crisis (bug-bounty collapse); spec-finfisher-finspy-spyware / Citizen_Lab (ForcedEntry, BLASTPASS as parser-blast-radius rhymes).*
