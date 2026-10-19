# Agentic browsers - the AI that browses and acts as you

*As of 2026-10-17. Companion to `spec-agentic-browsers.json`. Overlay/structural edges only; new nodes are isolated from the AI-financial SCC (unchanged). Grading is per-claim: fact | interpretation.*

## What they are

A new product category where the browser itself is an AI agent that can read every page you visit and **act on your behalf** - clicking, filling forms, shopping, navigating - including on sites you are **already signed in to**.

- **OpenAI ChatGPT Atlas** - launched macOS-first on **2025-10-21**. ChatGPT is embedded in every page ("Ask ChatGPT" sidebar) plus an **Agent Mode** (preview, paid) that completes multi-step tasks autonomously, operates in logged-in mode, and uses "browser memories" of your prior visits. OpenAI's framing: a step toward "a true super-assistant that understands your world." It ships safeguards (no code execution, downloads, extension installs, or filesystem access) and openly disclosed prompt-injection risk.
- **Perplexity Comet** - launched **2025-07-09**. The 2025 AI Agent Index rates it **L4-L5 autonomy** - it proceeds autonomously once initiated, with fewer approval gates than ChatGPT's agent.
- **Google** is embedding Gemini agentic features into **Chrome**, which makes agentic browsing a mass-market default rather than a niche.

## The unsolved hole: indirect prompt injection (fact)

The defining security problem. When the agent is asked to "summarize this page," it feeds the page's content to its LLM **without a trust boundary** between the user's instructions and the untrusted page text. So hidden instructions on a web page become **commands the agent executes**:

- **Brave Security (Aug 2025)** demonstrated Comet reading a malicious Reddit post, then opening the user's **logged-in Gmail**, triggering an account-recovery flow, and exfiltrating the code. Payloads hide as white-on-white text, HTML comments, or text inside images/screenshots.
- **Why normal browser security doesn't help:** same-origin policy and sandboxes don't apply - the agent has **legitimate, credentialed, multi-domain access**, so it is abusing authority it was *given*, not exploiting a browser bug.
- **Systemic, not a single bug:** Brave concluded indirect prompt injection is a **category-wide** challenge. **LayerX** disclosed "CometJacking" (one crafted URL exfiltrates email/calendar/connected-service data); Perplexity reportedly marked reports "no security impact"; a Brave-reported fix was later defeated. **Trail of Bits** (pre-launch audit) found four prompt-injection techniques exfiltrating Gmail.

Even the leaders treat it as an open frontier - OpenAI disclosed the risk at launch and its CISO has publicly called prompt injection unsolved (`spec-heif-heist-openai-ciso`).

## Why it's in the map (interpretation, labeled)

An agent that **sees all of your browsing and acts with your credentials** concentrates enormous data and authority in a single AI vendor - a qualitatively new **surveillance/control surface** compared with a passive browser, and a new high-value **attack surface**. No claim is made that any vendor misuses the data; the point is the concentration and the attack surface, not asserted intent. This is the centralized mirror-image of the local/uncensored-AI counter-ecosystem (`spec-local-uncensored-ai`).

## Nodes and edges

New nodes: `Agentic_Browsers` (the category), `Prompt_Injection` (the hole), `Perplexity`, `Brave` (the lead discloser). Edges run vendor -> `Agentic_Browsers` (OpenAI/Perplexity/Google), `Agentic_Browsers -> Prompt_Injection`, `Prompt_Injection -> OpenAI` (acknowledged frontier), `Brave -> Prompt_Injection` (disclosure), and `Agentic_Browsers -> Private_Surveillance` (the control-surface read). All structural overlay.

## Cross-references

`spec-heif-heist-openai-ciso` (prompt injection as an acknowledged frontier at OpenAI) | `spec-palantir-surveillance` and the surveillance layer (the data-concentration lens) | `spec-local-uncensored-ai` (the decentralized counter-ecosystem) | `spec-ai-capability-timeline` (where agentic browsing sits on the capability curve).
