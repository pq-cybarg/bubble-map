# Foundry Networks → Brocade → Broadcom — the pre-cloud router/switch lineage and where the IP went (dated)

*Built 2026-06-26 from `research/spec-foundry-brocade-broadcom.json`. The networking-hardware lineage flagged for the backlog. Cross-links the existing `Broadcom` node + the semiconductor/networking supply-chain thread. (Companion to the queued networking & security industry block.)*

> **Frame.** Foundry Networks was a hot dot-com-era maker of high-performance Ethernet routers/switches (**BigIron, ServerIron, FastIron, NetIron**) for carrier/datacenter/enterprise backbones — the **pre-AWS** world where you *bought* the iron. It was absorbed in two consolidation steps: **Brocade** (the Fibre-Channel SAN leader) bought Foundry in **2008**; **Broadcom** bought Brocade in **2017**, **kept** the Fibre-Channel SAN business, and **divested** the IP-networking lines (Ruckus/ICX → Arris → CommScope; Vyatta → AT&T).
>
> **Discipline.** The acquisitions, prices, dates, the kept-vs-divested split, and the FTC consent order are **fact** (SEC filings, FTC, trade press). Overlay; excluded from the proofs.

## 1. The origin (fact)

**Foundry Networks** (founded 1996, Bobby Johnson) rode the late-1990s internet build-out with high-performance Ethernet: **BigIron** chassis switch/routers, **ServerIron** load balancers/ADCs, **FastIron/NetIron**. Its **1999 IPO** was one of the era's hottest. In the pre-cloud architecture, enterprises and carriers **owned and operated** this gear in their own datacenters and backbones — the antithesis of today's rent-the-cloud (AWS) model. *Fact.*

## 2. The Brocade step (fact)

**Brocade Communications** (the dominant Fibre-Channel **storage**-area-network switch vendor) agreed to acquire Foundry on **21 Jul 2008** for **~$3B** (cash+stock) to add IP/Ethernet to its SAN franchise; amid the financial crisis a **$400M financing tranche fell through**, so the deal was **repriced to ~$2.6B all-cash** (7 Nov 2008) and closed **18 Dec 2008**. *Fact (SEC filings).*

## 3. The Broadcom step (fact)

**Broadcom** acquired Brocade (announced Nov 2016; **~$5.5B equity + ~$0.4B net debt = ~$5.9B** at **$12.75/share**; **FTC consent order Jul 2017**; closed **17 Nov 2017**). Broadcom **kept** Brocade's **Fibre-Channel SAN switching** (a high-margin, sticky datacenter franchise that complements its chips) and **divested** the IP-networking business. *Fact (SEC/FTC).*

## 4. The scatter — where the IP went (fact)

Brocade's IP-networking — including the recently-acquired **Ruckus Wireless** and the **ICX campus-switching** line (Foundry's enterprise heritage) — was sold to **Arris** (2017), which was itself acquired by **CommScope** (2019); the **Vyatta** SDN/software-router assets went to **AT&T** (2017). So the Foundry/Ethernet lineage is now split across **CommScope** (campus/wireless) and a carrier (**Vyatta → AT&T**), while the **SAN core sits inside Broadcom**. *Fact.*

## 5. The honest reading

Foundry is a clean case study in how the pre-cloud, buy-the-iron networking industry consolidated into a few hands: a hot standalone innovator (Foundry) → folded into a storage-networking peer (Brocade) → absorbed by a semiconductor giant (Broadcom) that kept the profitable SAN core and sold off the rest. The throughline to the corpus: the same **Broadcom** that now anchors AI-datacenter silicon also quietly owns the **Fibre-Channel SAN switching** that moves enterprise storage — another chokepoint consolidated under one roof. No scandal here; the value is the dated consolidation map and the cross-link to Broadcom. Overlay; excluded from the proofs.

*Sources: [Wikipedia — Foundry Networks](https://en.wikipedia.org/wiki/Foundry_Networks); [Network World — Brocade to buy Foundry for $3B (2008)](https://www.networkworld.com/article/2273874/brocade-to-buy-foundry-for--3-billion.html); [SDxCentral — Broadcom buys Brocade for $5.9B](https://www.sdxcentral.com/news/broadcom-buys-brocade-communications-for-59b/); [FTC — consent order, Broadcom/Brocade (Jul 2017)](https://www.ftc.gov/news-events/news/press-releases/2017/07/ftc-accepts-proposed-consent-order-broadcom-limiteds-59-billion-acquisition-brocade-communications).*
