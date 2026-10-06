# Open-weight AI, abliterators, redistributors + hosting - the de-censoring counter-ecosystem

*(AI-chronology Tab, #247. Taxonomy: these are mostly **LLMs** - one branch of AI - but they define the open-weight vs closed-frontier split.)*

## Chronology (fact)
- **2023:** Meta's **Llama** opens the **open-weight** era - downloadable models anyone can run + fine-tune, splitting the field from closed frontier APIs. **Mistral** (France) follows with permissive releases.
- **2024-2026:** **Qwen** (Alibaba, Apache-2.0) becomes one of the most-used open families; **DeepSeek** (R1/V-series) makes efficient open weights a frontier-adjacent force ([[fin-ai-efficiency-counter-thesis]]).
- Throughout: **Hugging Face** is the dominant **redistributor/hub** (mirrors + versions the weights); **OpenRouter** is the **API aggregator** (by Q2 2026, Chinese open models crossed ~30% of its developer token traffic); **Ollama** + llama.cpp make **local, offline** running trivial.

## The de-censoring layer (fact of technique; quality varies)
- **Abliteration** (automated by tools like **Heretic**) edits an open model's weights to **remove refusal behavior** - converting a censored-when-served model into an uncensored local one.
- Fine-tuning + abliteration produce the "uncensored" re-releases that populate the local-AI ecosystem, where served-model guardrails simply don't apply.

## The open-weight paradox (interpretation, labeled)
Once weights are public, they are **de-censorable downstream** - so served-model safety and frontier-model regulation are **structurally leaky**. Chinese open models sharpen the paradox: **censored-at-source** when served from China, yet **freely de-censorable** once downloaded. This is the honest check on the safety-regulation story from the [[spec-ai-lab-chronology-ea-pathways]] block: you can regulate the API and the frontier lab, but not the weights already in the wild.

## Honest limits
Releases, licenses, hubs, and the abliteration technique are **fact**; de-censoring quality is **variable**; "undercuts served-model safety / frontier regulation is leaky" is **interpretation** (though the leak is demonstrated). Structural overlay - no financial-core edges.

*Sources: model releases (Llama/Mistral/Qwen/DeepSeek); Hugging Face / Ollama / OpenRouter; abliteration research + Heretic. Cross-refs: Meta, Llama, Alibaba, Qwen, DeepSeek, Mistral, Hugging_Face, OpenRouter, Ollama, Heretic, Abliteration, Uncensored_AI, AI_Safety_Regulation.*
