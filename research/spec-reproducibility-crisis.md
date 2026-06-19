# When verification costs more than production — the reproducibility crisis, AI eval-gaming, and the integrity floods drowning science, open source, and security

*Built 2026-06-18 from `research/spec-reproducibility-crisis.json`. Companion to `spec-research-security-tech-transfer` (the "deliberately-degraded process" question resolves here) and the AI-bubble blocks.*

> **One mechanism, six collapses.** An open or trust-based system stays healthy only while *producing* a contribution costs at least as much as *verifying* it. Generative AI drove the cost of producing plausible artifacts — papers, pull requests, bug reports, benchmark-beating outputs, **even live faces and voices** — toward **zero**, while the cost of verifying them barely moved. The **effort-based backpressure** that gated every open system disappears, and the gate buckles. The same asymmetry now hits **science**, **AI's own evals**, **scientific publishing**, **open source**, **security**, and **live audiovisual identity** (the Arup deepfake-CFO fraud).

## 1. The law: backpressure collapse

Every open, trust-based system — peer review, open-source contribution, coordinated vulnerability disclosure, public preprint servers, capability benchmarks — implicitly relied on **effort as backpressure**: a plausible submission cost about as much as evaluating it, so submission rates self-limited and reviewers kept up.

Generative AI **inverted the asymmetry**: one contributor + an agent emits 5–50 plausible items in the time a maintainer evaluates one. This isn't five problems — it's **one mechanism** (`verification_cost > production_cost`) hitting five systems. And wherever *"looks legitimate"* is cheap while *"is legitimate"* is expensive to confirm, the degradation is **indistinguishable, item by item, from honest error or deliberate sabotage**. The maintainers name it themselves: Hashimoto's "effort-based backpressure," Stenberg's "AI is DDoSing open source."

## 2. Science: replication and fraud (the pre-existing wound)

- **Replication rates are low:** ~**10–25%** of preclinical/life-science effects reproduce robustly (many only partially; most fail); behavioral science ~**50%**. Whether "55% is too low" is itself debated — *contested magnitude, documented direction.*
- **Fabrication:** a 2024 meta-analysis across ~**75,000** studies estimated as many as **1 in 7** may be at least partially faked (prior estimates ~2–8%) — non-trivial under any estimate.
- **Accelerating:** a 2025 Northwestern study found **fraudulent science is *outpacing* the growth of legitimate publication**, via organized **paper-mill** networks.
- **Root causes** predate AI — positive-result bias, underpowered studies, selective reporting, analytical flexibility (Ioannidis' "most published findings are false") — but **AI accelerates** them (cheap plausible manuscripts, AI-assisted mills). **Grade: fact** (crisis + causes); *contested magnitude* on exact rates.

## 3. The mirror: AI's *own* reproducibility crisis

The accelerant has the disease. The capability claims driving the bubble rest on benchmarks that are themselves **contaminated and harness-dependent**:
- Data contamination inflates scores **~5–15+ points**; the same weights **swing 10–20 points** by eval harness; frontier models reproduce gold patches/problem statements **verbatim from a task ID**; scores **collapse when questions are perturbed**. "Every popular static benchmark is contaminated to some degree."
- So *"models are improving exponentially"* is **partly a measurement artifact** — an in-practice-**unfalsifiable** claim that justifies capex. Producing impressive numbers is cheap; clean, held-out, perturbed verification is expensive and rare. **The reproducibility crisis wearing an AI badge.** **Grade: fact** (contamination/harness-swing documented); *inference* on the exact degree it props up capex.

## 4. arXiv: the gate buckles

**Oct 31 2025** — arXiv's **Computer Science** category will **no longer accept review articles, surveys, and position papers** unless already peer-reviewed/accepted, reversing a 34-year moderator-discretion norm. Cause: a flood of **hundreds of AI-generated review papers per month**. Moderator Thomas G. Dietterich: *"We were driven to this decision by a big increase in LLM-assisted survey papers… We don't have the moderator resources to examine these submissions."* The open preprint backbone partially closed — **not because the math failed, but because moderation throughput couldn't scale against near-free production.** **Grade: fact.**

## 5. Open source: the slop flood

Maintainers are drowning in AI-generated PRs/issues — verbose, nonsensical, unexplainable when questioned. ~**96% of codebases** depend on open source, so this layer is load-bearing for the whole software economy.
- **Jazzband** (major Python collective) **shut down entirely**, citing unsustainable AI-spam volume.
- **Godot** (Remi Verschelde): triaging AI slop "draining and demoralizing."
- **Ghostty** (Mitchell Hashimoto, Jan 2026): restricted AI contributions to pre-approved issues/maintainers — explicitly because *"agentic programming has removed the effort-based backpressure that previously limited low-quality submissions."*

The mechanism is **throughput asymmetry**: review that took 15 minutes now takes a full day against 20–50 slop items/week; unpaid triage crowds out real work and accelerates burnout. Tooling (e.g. **SlopGuard**) tries to quarantine slop PRs — an arms race. **Grade: fact.**

## 6. Security: bug-bounty collapse

**curl** is the canonical case. Pre-AI: ~**1 security report/week**. 2025: **one every ~48 hours** — volume doubled, quality cratered, with **~1 in 5** submissions "AI slop": confident, polite prose, zero substance, **hallucinated functions that don't exist** (an HTTP/3 "stream dependency cycle exploit" with fabricated GDB sessions referencing a function not in curl). curl **shut its HackerOne bounty** (Feb 2026), reopened, then **paused reports entirely** (July 2026). Stenberg: *"AI is DDoSing open source."*

**The new twist:** even once reports became *accurate*, **duplicates** exploded — different researchers prompt the same model, get the same answer, submit identical reports. Accuracy didn't fix the throughput asymmetry; it **relocated** it. Coordinated vulnerability disclosure — a pillar of defensive security — degrades when noise is free and signal is expensive to confirm. **Grade: fact** (curl/Stenberg, dated changes); *prediction* on the broader death of open bounties.

## 6a. The sixth collapse: live audiovisual identity (the Arup deepfake-CFO fraud)

The purest instance — because **the verification step itself was the attack surface.** In **January 2024**, a finance worker in the Hong Kong office of **Arup** (the British engineering firm behind the Sydney Opera House and Beijing's "Bird's Nest") got a phishing email impersonating the UK **CFO**. He did the *careful* thing — asked to confirm on a **video call**. The CFO and several recognized colleagues joined; they looked and sounded right. **Every one of them was a deepfake**, built from public footage (earnings calls, online meetings, scraped clips). He made **15 transfers totaling HK$200M (~$25.6M)** to five accounts over a week. The only real person on the call was the victim. (Reported to HK police Jan 2024; named by CNN May 2024; **money never recovered, no one charged.**)

The standard anti-fraud control — *"don't trust the email; verify live on video"* — assumed a face and a voice are **expensive to fake.** They no longer are: Arup's own global CIO Rob Greig later **deepfaked himself with free tools in 45 minutes.** So *"looks like the CFO"* became free while *"is the CFO"* stayed expensive — the exact `verify-cost > produce-cost` inversion, now hitting **identity itself.**

This is also the empirical face of the **digital-ID identity-proof paradox** (`digitalid-orchestration-real-incentive`): biometric "liveness" (face + voice) is **forgeable**, so biometric verification inherits the same defeat-by-cheap-forgery problem — an argument for verifying *cryptography*, not *appearance*. **Grade: fact** (CNN 2024-05-16; Arup CIO on record; HK$200M/~$25.6M, never recovered).

## 7. Where the "deliberately-degraded process" question resolves

This is the home of the sabotage question from the research-security block. **You cannot distinguish a deliberately-poisoned process from an honest-but-non-reproducible one** for the *same reason* you cannot distinguish an AI-slop bug report from a real one without doing the full verification: **when verification cost exceeds production cost, the categories collapse at the point of observation.** Sabotage, fraud, honest-fragility, and hallucination all *look alike* in the artifact.

So **intent is unrecoverable from the artifact alone** — and the rational posture is **intent-independent**: re-introduce verification/backpressure (reproduce before trusting; proof-of-effort; provenance; gated submission) rather than try to read minds from outputs. Same conclusion the rest of the corpus keeps reaching: *verify, don't trust.*

## 8. What re-introduces backpressure (and its price)

- **Gating** — peer-review-first for low-novelty content (arXiv); pre-approval for contributions (Ghostty).
- **Provenance + proof-of-effort** — disclosed AI assistance, reproducible artifacts, human attestation/stake that *costs* the submitter something.
- **Verify-don't-trust** — independent reproduction / perturbed evals before relying on a result or a benchmark (the AI-eval fix mirrors the science fix).
- **Economic re-pricing** — *pay* the reviewers/maintainers (the unpaid-triage layer is the real bottleneck), or charge submitters to restore cost symmetry.
- **Detection arms-race** (weakest) — AI-slop classifiers; useful but gameable.

**The honest cost:** every one of these **re-closes openness** to some degree. The price of the flood is the **partial loss of the open commons** — open preprints, open contribution, open disclosure — and it is **already being paid.**

## 9. Limits
**Documented:** the science replication/fabrication crisis and its acceleration (magnitudes stated as contested); benchmark contamination and harness-dependence; the dated arXiv CS policy and its stated cause; the named OSS casualties and the maintainer-named backpressure mechanism; the curl/HackerOne collapse and the duplicate-report twist. **Graded as prediction:** the broader death of open bounties/submission. **Synthesis (not separately proven):** that one mechanism underlies all five, and that it's the same wall that makes deliberate sabotage indistinguishable from honest non-reproducibility. *"AI" is a cost-shifting tool, not an intending agent; harms are emergent from incentives.* Overlay edges excluded from the proofs.

*Sources: [C&EN — replication crisis coverage](https://cen.acs.org/research-integrity/reproducibility/Amid-White-House-claims-research/103/web/2025/06); [arXiv blog — updated practice for review/position papers (Oct 31 2025)](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/); [404 Media — arXiv changes rules after AI-paper spam](https://www.404media.co/arxiv-changes-rules-after-getting-spammed-with-ai-generated-research-papers/); [BleepingComputer — curl ending bug bounty after AI slop](https://www.bleepingcomputer.com/news/security/curl-ending-bug-bounty-program-after-flood-of-ai-slop-reports/); [The New Stack — curl's Stenberg: AI is DDoSing open source](https://thenewstack.io/curls-daniel-stenberg-ai-is-ddosing-open-source-and-fixing-its-bugs/); [LeadDev — open source's AI slop problem](https://leaddev.com/software-quality/open-source-has-a-big-ai-slop-problem); [The New Stack — maintainers drowning in AI PRs](https://thenewstack.io/ai-generated-code-crisis/); [arXiv — Benchmark Data Contamination of LLMs: A Survey](https://arxiv.org/pdf/2406.04244); [CNN — Arup revealed as victim of $25M deepfake video-call scam (Hong Kong, 2024-05-16)](https://www.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk).*
