# The efficiency counter-thesis — DeepSeek, Jevons, and China's domestic AI stack

*Web-verified 2026-06-11. Structured + sources: `fin-ai-efficiency-counter-thesis.json`. Overlay — evidence-graded, excluded from the proofs. The honest steelman of the strongest challenge to this project's own thesis. Connects to [[fin-microsoft-openai]] (the $1.4T), [[fin-ai-depreciation-debttrap]], [[geopolitics-chip-chokepoint-war]], [[macro-ai-power-grid-bottleneck]].*

A zero-trust project has to doubt **its own** thesis too. The strongest argument against "the AI build is an over-leveraged bubble" is **efficiency**: if intelligence gets radically cheaper, maybe the brute-force compute build is either unnecessary (bearish for the spenders) or about to be swamped by demand (bullish). We hold both — and flag the tell.

## The DeepSeek shock
**DeepSeek R1** (late Jan 2025) delivered frontier-comparable performance at a small fraction of the claimed training cost. Markets read it as "compute is over-valued" — **Nvidia lost ~$600B of market cap in a single day**, the largest one-day loss in history (**fact**). Two readings followed, both fact-based:
- **Bear (efficiency obviates brute force):** if a model this good costs ~1/10–1/50 the compute, the **$1.4T** of OpenAI compute commitments + ~$600B/yr hyperscaler capex looks **over-built** — supporting the "largest misallocation of capital in history" view ([[fin-ai-depreciation-debttrap]]).
- **Bull (Jevons paradox):** cheaper intelligence → demand explodes. Satya Nadella tweeted *"Jevons paradox strikes again!"*; Goldman's 2026 forecast says at ~**$0.02/kWh**, AI inference is cheaper than human labor for ~**23% of service jobs.**

## The tell
What happened next is the diagnostic: **despite DeepSeek, 2026 hyperscaler capex grew to ~$602B (+36% YoY).** The narrative resolved **bullish either way** — when compute was scarce you "needed to build more"; when DeepSeek made it cheap, **Jevons** said you "needed to build more." **A thesis that justifies the same action under opposite facts is unfalsifiable** — the structural signature of a *bubble narrative*, not an analysis. (This doesn't *prove* over-building; it flags that "efficiency = bullish" is being **asserted, not demonstrated.**)

## China routes around the chokepoint
China is building an AI stack **separate from Nvidia/CUDA**, eroding the export-control moat ([[geopolitics-chip-chokepoint-war]]) from **two sides at once**:
- **Efficiency:** DeepSeek does more with less (a Huawei-led team **post-trained DeepSeek V4-Pro, a 1.6-trillion-parameter model, on ~1,000 Ascend 910C** chips).
- **Brute force with subsidized power:** Huawei plans **~600,000 Ascend 910C chips in 2026** (~1.6M Ascend dies total; customers Alibaba/Tencent/DeepSeek). The **CloudMatrix 384** rivals Nvidia's NVL72 on inference but draws **~560kW vs ~145kW** (4.1× the power for ~1.7× the compute) — inefficient, but China **subsidizes energy** for priority industries, so it's viable.

CSIS/RAND debate whether DeepSeek **undermines or reinforces** the case for export controls; a US lawmaker alleged (Jan 2026) that **Nvidia co-designed** the DeepSeek model (**contested**). Either way, *smarter algorithms need fewer chips, and a domestic (power-hungry) stack supplies the rest.*

## The honest assessment (where it leaves the bubble thesis)
Crucially, the project's **machine-proven** results don't hinge on this. The **circular-funding**, **self-marked-value**, and **depreciation** proofs are about how the build is **financed and accounted for** — defective *regardless of end-demand*. The efficiency debate bears on a *different* question — *"is the capex justified by real demand?"* — and there, intellectual honesty requires saying: **it is genuinely uncertain, the Jevons case is real, and the project does NOT claim the demand is fake.** What it *can* say:
1. The **unfalsifiable "build-more-either-way" narrative** is bubble-shaped.
2. Efficiency makes the **depreciation trap worse** — today's expensive brute-force GPUs are obsoleted *faster* by tomorrow's efficiency ([[fin-ai-depreciation-debttrap]]).
3. China's efficiency + domestic stack **undercut the chip-chokepoint moat** the bull case leans on.

## The distillation-by-proxy wrinkle (2025-2026)

A live wrinkle in the efficiency story: US labs allege part of the Chinese cost gap comes from **distilling their models via proxied access**. OpenAI flagged **DeepSeek** (2025); Anthropic (24 Feb 2026) named **DeepSeek, Moonshot AI, and MiniMax** - estimating **~16M exchanges from ~24,000 fraudulently-created accounts** (MiniMax the largest, ~13M) - and later added **Alibaba/Qwen**. Because Anthropic and OpenAI sell **no API in China**, the requests were allegedly **routed to the US providers through commercial proxies + overseas shell accounts** - i.e. Chinese AI pipelines quietly pointing at American models. *Fact that the allegations were made; **contested** per-firm culpability - the named firms have not confirmed.*

**Why it matters here.** It partially undercuts the cleanest reading of DeepSeek: some efficiency may be **free-riding on US models' training signal**, not purely novel algorithm. But it does **not** collapse the counter-thesis - DeepSeek's architectural gains (MoE, MLA, FP8, Huawei-Ascend post-training) are independently documented, and distillation is a standard, cheap technique regardless of source. **Both hold: real efficiency AND unauthorized distillation-by-proxy.**

**Honesty guards.** (1) *Composition fallacy* - "Chinese labs" is not one mind; the evidence differs per firm. (2) The dispute is **narrow** - using a *competitor's* model + circumventing ToS/geo-limits, not distillation itself (which Anthropic/OpenAI/Google all do to their *own* models). (3) Anthropic's own detection drew backlash: per the Washington Post (Mar 2026) it quietly deployed software to unmask China-based users, then pulled it after privacy criticism - a surveilling-its-own-customers episode that cuts against a clean-hands framing. See [[spec-china-ai-stack-censorship]] for the graph edges + fuller account.

*Sources: [CNBC - Anthropic joins OpenAI in flagging distillation by Chinese AI firms (2026-02-24)](https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html); [CNBC - Anthropic's distillation battle turns to the dark web (2026-09-03)](https://www.cnbc.com/2026/09/03/anthropic-distillation-battle-turns-to-dark-web-china-concerns-swell.html).*
