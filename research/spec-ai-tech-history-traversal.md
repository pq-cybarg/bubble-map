# The true tech-history of AI - a graph traversal across the sciences

*(AI-chronology Tab, #249. **Central claim: "AI" is not "LLM."** AI is a broad field of many branches - logic/search, statistical ML, reinforcement learning, computer vision, robotics, protein folding. **LLMs (transformers, 2017+) are the currently-dominant branch, not the field.** Below is a followable walk of the lineage, breadth-first across roots, then depth-first down each branch.)*

## Roots (the shared substrate)
- **Mathematical logic** (Boole, Frege, Turing, Church, 1850s-1936) formalized *computation* itself.
- **Probability + statistics** (Bayes, Fisher) gave *learning from data* its footing.
- **Information theory** (Shannon, 1948) quantified information (entropy, likelihood).
- **Cybernetics + control** (Wiener, 1948) framed feedback + goal-seeking systems.
- **Neuroscience abstraction** (McCulloch-Pitts neuron, 1943) modeled the brain as computation.

## Branch A - Symbolic AI (the first paradigm)
Logic -> the **Dartmouth 1956** program coins "AI" -> **search, theorem-proving, LISP** -> **expert systems** (MYCIN, DENDRAL, 1970s-80s), commercial AI's first wave -> **AI winter** when hand-coded rules proved brittle. *Lesson that echoes forward: rules don't scale; learn from data instead.*

## Branch B - Connectionism (the branch that won, eventually)
Cybernetics + McCulloch-Pitts -> **Perceptron** (Rosenblatt, 1958), the first trainable net -> frozen by **Minsky-Papert (1969)** -> revived by **backpropagation** (Rumelhart/Hinton/Williams, 1986) for multi-layer nets -> stalled again on compute until...

## The hardware unlock (the cross-cutting edge)
**GPUs + CUDA (2007)** made deep-net training practical - hardware, not just algorithms, opened the modern era. It fed *multiple* branches at once:
- -> **ImageNet + AlexNet (2012)**: deep learning crushes *vision* (not language). The deep-learning era begins.
- -> **Deep reinforcement learning**: DQN (2013) -> **AlphaGo (2016)** (deep RL + tree search) -> **AlphaFold (2020-24)** solves protein structure (a Nobel). **These are superhuman AI systems that are NOT LLMs** - the clearest proof the field is bigger than language models.

## Branch C - Sequences -> attention -> LLMs
Vision deep learning spread to sequences (**RNN/LSTM**) -> **attention** -> the **Transformer (Vaswani et al., 2017)** -> scaling laws -> **GPT/BERT -> ChatGPT (2022) -> the frontier race**. This is the branch now soaking up attention + capital - but trace the tree: **LLMs are one branch (C) of deep learning, itself one branch of ML, itself one branch of AI.** Branches A (symbolic) and B/RL (AlphaGo/AlphaFold) are alive and, in domains like science, ahead.

## Why the walk matters
Treating "AI" as synonymous with "LLM" mis-reads both the risk surface and the history: the capital + safety-regulation fight ([[spec-ai-lab-chronology-ea-pathways]]) centers on LLMs, but the field's biggest scientific wins came from other branches, and its future may too. Keeping the taxonomy honest is the point of this Tab.

*Sources: standard histories of computing, AI, ML, and the contributing fields. All edges are established lineage (fact); the "LLMs are one branch" framing is a taxonomy claim, not a value judgment. Cross-refs: Mathematical_Logic, Information_Theory, Cybernetics, Perceptron, Symbolic_AI, Expert_Systems, Backpropagation, GPU_Compute, ImageNet_AlexNet, Transformer, Reinforcement_Learning, AlphaGo_AlphaFold, Deep_Learning.*
