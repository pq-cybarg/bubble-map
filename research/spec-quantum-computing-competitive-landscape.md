# Quantum computing — the full competitive landscape: modalities, the public pure-plays, the big-tech programs, and the US/China/EU/India/Japan race

*Built 2026-06-19 from `research/spec-quantum-computing-competitive-landscape.json`. The **entity map** companion to `macro-crqc-quantum-landscape` (the Q-Day clock, HNDL/TNFL, PQC counter-migration). Pairs with `macro-quantum-computing` (equities) and `macro-pqc-chips` / `fin-sealsq-wisekey-global` (PQC silicon).*

> **Frame.** WHO is building quantum computers, by WHICH physical modality, with WHOSE money, in WHICH country — and where the **engineering is real** vs. where the **equity is narrative-beta**. The organizing spine is the **modality**, because no architecture has won yet — and that uncertainty *is* the investment risk.
>
> **Discipline.** Company facts, funding, tickers, qubit counts and national-program figures are **fact** (web-verified). Supremacy claims inherit the **contested** grade from the companion block (Google's ZK cryptanalysis proof was *forged* by Trail of Bits). The "no settled winner / narrative-beta bubble" conclusion is **graded interpretation.** Overlay; excluded from the proofs.

## 1. The modality spine — six bets, no winner

Quantum computing is not one technology; it is **six-plus competing physical wagers**, none yet dominant. The race is as much *which qubit* as *which company*.

| Modality | Trade-off | Who |
|---|---|---|
| **Superconducting** transmon | fast gates (ns), short coherence (µs), millikelvin fridges | IBM, Google, **Rigetti**, **IQM** (FI), **Fujitsu**, China's **USTC** (Zuchongzhi) + **Origin Quantum** |
| **Trapped ion** | superb coherence (s) + fidelity, slow gates (ms) | **IonQ**, **Quantinuum** (Honeywell), **Oxford Ionics** (now IonQ), AQT, eleQtron, Universal Quantum |
| **Photonic** | room-temp, networking-native, fab-manufacturable, probabilistic gates | **PsiQuantum**, **Xanadu** (CA), **Quandela** (FR), Orca, China's **USTC** (Jiuzhang) |
| **Neutral-atom / Rydberg** | highly scalable, strong for logical qubits | **QuEra**, **Pasqal** (FR), **Atom Computing**, Infleqtion, planqc |
| **Topological** | error-resistant *if* it works — physically unproven | **Microsoft** (Majorana 1, 2025) |
| **Quantum annealing** | optimization-only, not universal | **D-Wave** |

Plus spin/diamond-NV (Quantum Brilliance, Diraq) and the **cloud aggregators** reselling all of it (Amazon **Braket**, Azure **Quantum**, **Nvidia CUDA-Q / DGX Quantum**). The honest read: a **portfolio of unsettled physics**, not a product category.

## 2. The public pure-plays — narrative, not cash flow

The listed pure-plays trade on story. **IonQ** (IONQ) leads by revenue (~$130M 2025; 2026 guide $225-245M) and is the most acquisitive. **Rigetti** (RGTI) posted Q1-2026 revenue of just **~$4.4M**. **D-Wave** (QBTS) and **Quantum Computing Inc** (QUBT) are smaller. **Quantinuum** (Honeywell-majority) filed to IPO at **~$12.7B**.

The structural fact: **multi-billion market caps on single-digit-to-low-hundreds-of-millions of revenue** — the same 800x-sales narrative-beta flagged for SEALSQ/WISeKey in the companion block. A May-2026 ~$931M warning and sharp IONQ/RGTI/QBTS drawdowns underline the volatility. **Grade: fact** (the figures); *bubble* is the interpretation.

**Consolidation.** IonQ is rolling up trapped-ion + sensing: **Oxford Ionics** (UK) for **~$1.075B** (announced Jun, closed Sep 2025) and intent to buy **Vector Atomic** (sensing). Roadmap: 256 qubits 2026 → >10,000 physical 2027 → 2M by 2030. Note the geopolitics — **a UK champion absorbed by a US firm: UK invents, US acquires.**

## 3. The big-tech programs

- **IBM** — the "realest" large-cap: Condor/Heron → **'Starling'** fault-tolerant target ~2029; Heron deployed externally (RIKEN Kobe).
- **Google** — Willow; supremacy claims repeatedly narrowed/spoofed; its ZK cryptanalysis proof **forged** by Trail of Bits (Apr 2026). Also a **QuEra** investor (neutral-atom hedge).
- **Microsoft** — two bets: topological **Majorana 1** (2025) long-shot **and** Azure Quantum partnering (logical-qubit demos with **Quantinuum** 2024 and **Atom Computing**).
- **Amazon** — **Ocelot** cat-qubit chip + **Braket** aggregator.
- **Nvidia** — not a qubit-maker but the **connective tissue**: CUDA-Q / DGX Quantum, NVentures stakes in PsiQuantum + Quantinuum, RIKEN AI+quantum supercomputers — the "sell shovels to all sides" play repeated from AI compute.

## 4. The national race — and the state as shareholder

- **United States** — NQI ~$1.2B (2019-24) + ~$1.8B reauth (2025-29); DARPA QBI/US2QC (PsiQuantum → Phase 3, Nov 2025). **New and significant:** reports (May 2026) of a **~$2B program that TAKES EQUITY STAKES** in quantum firms — the same **state-as-shareholder** pattern as MP Materials (DoD) and Intel, now extended to IonQ/Rigetti/D-Wave. Stocks spiked. *Equity-stake details still reported/contested.*
- **China** — leads **communications** (Micius satellites, ~12,000 km) and now matches the West on **superconducting compute**: USTC's **Zuchongzhi 3.0** (105 qubits, 2025) claims sampling ~10¹⁵× the top supercomputer and ~10⁶× past Google's Oct-2024 result; the photonic **Jiuzhang** line (Jiuzhang-3, 255 photons; 4.0 targeting 2,000+). **Origin Quantum** is the commercial champion (Wukong cloud, 180-qubit **Wukong-180**, 2026). ~CNY 2.2B raised in **Q1-2026 alone**; the **15th Five-Year Plan** names quantum **first** of seven "future industries," atop a ~$138B national VC fund.
- **European Union** — Quantum Flagship €1B (2018-28) + the 2026 AGILE defense plan. Deepest bench of independents: **IQM** (FI), **Pasqal** (FR, SPAC via Bleichroeder, ~$300M+, ~100% 2025 revenue growth, ~$80M booked), **Quandela** (FR), **Alice & Bob** (FR, cat qubits), **OQC** (UK). Risk: strong science, **thin capital** — and champions get acquired out.
- **United Kingdom** — National Quantum Strategy £2.5B (2024-34) + £2B procurement (Mar 2026): Oxford Ionics (→IonQ), OQC, **Riverlane** (error-correction), Quantinuum's Cambridge roots.
- **Japan** — deepest Asian commercial footprint ex-China: **RIKEN** hybrid quantum-HPC with Quantinuum **'Reimei'**, an IBM 156-qubit **Heron** at Kobe, **Fujitsu** superconducting (256-qubit 2025 → 1,000-qubit 2026); Nvidia+RIKEN supercomputers.
- **India** — National Quantum Mission (50-1,000-qubit by 2031); ~**1,000 km** quantum-comms link (2026, QNu/VIAVI); a domestic quantum chip (May 2026); Andhra Pradesh targeting three modalities + 1,000 logical qubits.
- **Others** — **Australia** (~A$1B anchoring PsiQuantum Brisbane; Silicon Quantum Computing, Diraq, Quantum Brilliance); **Canada** (Xanadu, D-Wave roots); Israel, South Korea, Singapore (**Temasek/QIA** as cross-border quantum capital). Cumulative global quantum investment has passed **~$50B.**

## 5. The manufacturing chokepoint (the least-hyped, most-real node)

Photonic and some superconducting players depend on **conventional semiconductor fabs.** PsiQuantum's **Omega** silicon-photonic chipset is built by **GlobalFoundries** on 300mm wafers in **New York** — the quantum supply chain runs through the **same foundry chokepoints** as classical chips (cf. `macro-pqc-chips`). "Utility scale" is gated by **fab capacity, dilution-refrigerator supply, helium-3, and cryo-electronics** — physical bottlenecks the equity story rarely prices.

## 6. The honest reading

1. **The engineering is real and accelerating** — IBM/Google roadmaps, IonQ/Quantinuum fidelity, neutral-atom logical-qubit records (QuEra: **96 logical from 448 atoms**, *Nature*, Jan 2026), photonic fault-tolerance bets — but **no modality has won**, so company-level winner-picking is genuinely premature.
2. **The equity is largely narrative-beta** — multi-billion caps on single-digit-millions of revenue. Separate the **builders** (IBM, Google, IonQ, Quantinuum, PsiQuantum, the neutral-atom cohort) from the **pure-play lottery tickets.**
3. **The state has entered as shareholder and customer on both sides** — US equity stakes + DARPA, China's $138B fund + national champions, EU/UK/India/Japan programs — turning quantum into **industrial policy** *and* a **HNDL/TNFL national-security race** at once.

**The bubble and the breakthrough are the same companies.** The discipline is to grade each *claim*, not the *sector*. Overlay edges excluded from the formal proofs.

*Sources: [The Quantum Insider — IonQ/Oxford Ionics $1.075B](https://thequantuminsider.com/2025/06/09/ionq-acquires-uk-based-oxford-ionics-for-1-075-billion/); [PsiQuantum $1B Series E](https://thequantuminsider.com/2025/09/10/psiquantum-raises-1-billion-to-build-million-qubit-scale-fault-tolerant-quantum-computers/); [PsiQuantum / DARPA US2QC / $100M Commerce LOI](https://thequantuminsider.com/2026/05/21/psiquantum-signs-100-million-letter-of-intent-with-the-u-s-department-of-commerce/); [CNBC — US quantum equity stakes](https://www.cnbc.com/2026/05/21/quantum-stocks--us-taking-equity-stakes.html); [Phys.org — Zuchongzhi 3.0](https://phys.org/news/2025-03-superconducting-quantum-processor-prototype-faster.html); [Quantum Zeitgeist — China quantum companies](https://quantumzeitgeist.com/china-quantum-computing-companies/); [BusinessWire — Pasqal SPAC / neutral-atom market](https://www.businesswire.com/news/home/20260304923225/en/); [Quantinuum — RIKEN Reimei](https://www.quantinuum.com/press-releases/riken-scales-quantum-supercomputing-in-japan-with-quantinuum-system-upgrade); [Quantum Computing Report — India NQM 1,000 km](https://quantumcomputingreport.com/indias-national-quantum-mission-achieves-1000-km-milestone-via-qnu-labs-and-viavi-validation/); [The Quantum Insider — leading quantum countries 2026](https://thequantuminsider.com/2026/03/26/leading-quantum-computing-countries/).*
