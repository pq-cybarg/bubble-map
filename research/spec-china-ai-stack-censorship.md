# China's AI stack beyond DeepSeek — the full domestic LLM field, the Huawei Ascend hardware push, and the built-in state-alignment / censorship layer

*Built 2026-06-21 from `research/spec-china-ai-stack-censorship.json`. Fixes the "efficiency counter-thesis only names DeepSeek" gap. Companion to `fin-google-amazon-anthropic-meta` (the Jevons/efficiency thesis), `spec-semiconductor-logistics-standards` (SMIC/export controls), `macro-crqc-quantum-landscape` (China programs), and the planned local/uncensored-AI block.*

> **Frame.** China fields a **deep, competitive, largely open-weight** LLM ecosystem **and** a mandatory state-alignment layer baked into all of it. Three layers: **(1) the labs**, **(2) the Huawei Ascend hardware push** to escape US export controls, **(3) the CAC censorship layer**. The twist: many models are **open-weight**, so the censorship is **de-censorable** downstream — the bridge to the uncensored-AI counter-ecosystem.
>
> **Discipline.** Labs/models/specs/shares/CAC facts are **fact** (web-verified). The "capability real **and** censorship built-in" duality is the **graded finding**. Composition guard: "China's models" = many independent labs under a common regulator, not one mind. Overlay; excluded from the proofs.

## 1. The labs (far beyond DeepSeek)

- **Alibaba — Qwen** (Qwen3.5, Apache 2.0): the most-used open-weight family globally.
- **DeepSeek** (High-Flyer; V3.2/R-series): the efficiency standard-bearer.
- The **"AI Tigers"** startups: **Zhipu AI** (GLM-4.6/GLM-5 — *trained entirely on Huawei Ascend*), **Moonshot** (Kimi K2.x — agentic-benchmark leader), **MiniMax** (M2.x — frontier-adjacent at **~1/20th cost**, MIT), **StepFun**, **01.AI** (Yi, Kai-Fu Lee), **Baichuan**.
- Incumbents: **Baidu** (Ernie), **Tencent** (Hunyuan), **ByteDance** (Doubao), **Xiaomi** (MiMo — reportedly **~21% of OpenRouter weekly tokens** in Q2-2026, ~3× OpenAI), **iFlytek** (Spark).

Market signal: by April 2026, **Xiaomi+Alibaba+MiniMax+Zhipu+DeepSeek+StepFun > ~45%** of weekly token volume on OpenRouter. *Fact.*

## 2. The hardware push (sovereign silicon, incomplete)

To escape US export controls China is building a domestic accelerator stack. **Huawei Ascend** leads: the **910C** (96GB HBM2e, ~A100-class FP16, **SMIC 7nm**) targets **~600k units in 2026** (up to ~1.6M dies), with **950PR** (Q1-26) and **950DT** (Q4-26) + SuperPoD interconnect next. **Cambricon, Biren, Moore Threads** round out the field; **SMIC** fabs them.

**Reality check:** substitution is **incomplete** — **DeepSeek's R2 was delayed** by Ascend training instabilities, forcing a return to **Nvidia H800s** for critical runs; **HBM is the bottleneck**. Real-and-improving, not yet achieved. *Fact.*

## 3. The censorship layer (alignment by state mandate)

Every public generative-AI service must **(a)** register its algorithm with the **CAC** + pass a security assessment (**748 services filed** by Dec 2025), and **(b)** uphold **"Core Socialist Values"** — no content that could "subvert state power, harm national security, or undermine social stability." CAC **tests** models (ByteDance, Alibaba, …) on **Xi Jinping** and sensitive topics; models refuse/deflect on **Tiananmen 1989, Taiwan, Xinjiang, Hong Kong** by design. This is **alignment-by-state-mandate** — structurally different from Western corporate/voluntary RLHF safety. *Fact (Interim Measures 2023; registration count; socialist-values testing).*

## 4. The open-weight paradox

The censorship lives in the **weights + serving layer** — but most models ship **open-weight** (Qwen Apache 2.0; GLM/MiniMax MIT; Hugging Face). Open weights can be **fine-tuned / "abliterated"** to remove refusals downstream (de-censoring tooling like **Heretic**; uncensored re-releases). So Chinese models are **both** censored-when-served-from-China **and** de-censorable raw material once public — the paradox bridging to the **local/uncensored-AI counter-ecosystem**. *Open licenses fact; de-censorability demonstrated but quality-variable (contested).*

## 5. The honest reading

Both true at once: **(1)** Chinese AI **capability** is real, plural, fast, and unusually **open** — not one DeepSeek but a dozen competitive labs, several frontier-adjacent at far lower cost, increasingly on domestic silicon; **(2)** the **censorship** is real, mandatory, and **built-in** — a state-alignment layer Western models lack. The **efficiency/Jevons** counter-thesis holds (cheap, abundant, open models accelerate diffusion) **with the control caveat** (abundance is state-aligned at the source) — and the **open-weight paradox** means that control is **leaky** once weights escape.

*Sources: [Interconnects — Chinese open model builders](https://www.interconnects.ai/p/chinas-top-19-open-model-labs); [DigitalApplied — Chinese AI Q2 2026 market share](https://www.digitalapplied.com/blog/chinese-ai-models-q2-2026-market-share-report); [Huawei 600k Ascend 910C in 2026](https://www.huaweicentral.com/huawei-plans-600000-ascend-910c-chips-by-2026-to-block-nvidia-in-china/); [SemiAnalysis — Ascend ramp / HBM bottleneck](https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp); [CAC Interim Measures for Generative AI](https://en.wikipedia.org/wiki/Interim_Measures_for_the_Management_of_Generative_AI_Services); [Euronews — 'core socialist values' testing](https://www.euronews.com/next/2024/07/18/communist-ai-china-using-censors-to-test-if-ai-models-embody-core-socialist-values-report).*
