# The NVIDIA <-> OpenAI Circular-Funding Web

**Forensic compilation — as of 2026-06-05.** Every figure carries a source URL. Status is classified as: **closed** (money/contract executed), **committed** (binding definitive agreement, not yet fully funded), **signed-LOI** (letter of intent / non-binding), or **reported-rumored** (press reporting only). "Circular" flags a round-trip: a supplier puts capital/credit into a customer that then buys the supplier's product.

---

## Executive narrative

In 2025–2026 NVIDIA became both the dominant supplier of AI compute **and** an equity investor in many of the customers buying that compute. The clearest documented round-trips:

- **NVIDIA -> OpenAI:** The headline "up to $100B progressive equity" announcement (Sept 22, 2025) was a **letter of intent**, tied to deploying 10GW of NVIDIA systems, paid in progressively as each GW deployed. **It never reached a definitive agreement** — CFO Colette Kress confirmed no signed deal (Dec 2025); WSJ reported talks "on ice" (Jan/Feb 2026). It was effectively **replaced** by a clean $30B direct equity check from NVIDIA into OpenAI's Feb/Mar 2026 mega-round (no GW conditionality). So the famous $100B figure is **rumor/LOI that lapsed**; the real, closed NVIDIA->OpenAI number is **$30B**.
- **NVIDIA -> CoreWeave:** ~7% equity stake plus a **take-or-pay backstop** — under the April 2023 MSA, a Sept 9, 2025 order form (initial value **$6.3B**) obligates NVIDIA to buy CoreWeave's *residual unsold cloud capacity* through **April 13, 2032**. CoreWeave buys NVIDIA GPUs; NVIDIA guarantees CoreWeave's revenue. Textbook circular.
- **NVIDIA -> xAI:** ~$2B into xAI's $20B Series E; the round's SPV literally exists to buy NVIDIA GPUs for Colossus 2. Explicitly circular.
- **NVIDIA -> Anthropic:** up to **$10B** (with Microsoft up to $5B), Nov 18, 2025; Anthropic commits **$30B to Azure** and up to 1GW, "powered by NVIDIA." Circular.
- **NVIDIA -> Intel ($5B, closed Dec 2025), Nokia ($1B, Oct 2025), Nscale, Mistral** — vendor/strategic investments, several into entities that buy NVIDIA silicon.

On the **OpenAI demand side**, OpenAI has stacked ~**$1.4 trillion** of disclosed compute commitments (Altman, Nov 2025) against a ~**$20B revenue run-rate** (end-2025) and large losses ($13.5B net loss in H1 2025 alone). The commitment web: Microsoft ($250B incremental Azure), Oracle/Stargate (~$300B), AMD (6GW + 160M-share warrant), Broadcom (10GW custom XPUs), CoreWeave (~$22.4B), and NVIDIA GPU purchases.

**The skeptic's core point:** suppliers (NVIDIA, AMD, Microsoft, Oracle) are funding the buyer (OpenAI/Anthropic/xAI), who recycles that capital straight back into the suppliers' products — inflating both sides' revenue/valuation optics.

---

## Edge table

| From | To | Instrument | Amount (USD) | Date | Status | Circular | Confidence |
|---|---|---|---|---|---|---|---|
| NVIDIA | OpenAI | Progressive equity (10GW LOI) | up to 100B | 2025-09-22 | **signed-LOI (lapsed)** | yes | high |
| NVIDIA | OpenAI | Direct equity (mega-round) | 30B | 2026-02-27 / closed 2026-03-31 | **closed** | yes | high |
| NVIDIA | CoreWeave | Equity stake (~7%) | ~0.35B at-cost; ~7% | pre-IPO 2025 | closed | yes | high |
| NVIDIA | CoreWeave | Take-or-pay backstop (residual capacity) | 6.3B initial | 2025-09-09 (MSA 2023) | committed (thru 2032) | yes | high |
| NVIDIA | xAI | Equity (Series E) | up to 2B | 2025 (Series E $20B) | committed/closed | yes | high |
| NVIDIA | Anthropic | Equity | up to 10B | 2025-11-18 | committed | yes | high |
| NVIDIA | Intel | Common stock (~4%) | 5B | announced 2025-09-18; closed 2025-12 | closed | partial | high |
| NVIDIA | Nokia | Equity (directed share issue) | 1B | 2025-10-28 | committed/closed | partial | high |
| NVIDIA | Nscale | Equity | ~0.5–0.7B | 2025-09 | committed | partial | med |
| NVIDIA | Mistral | Equity (Series C participation) | undisclosed (round EUR1.7B) | 2025-09 | closed | partial | med |
| OpenAI | Microsoft | Azure compute commitment (incremental) | 250B | 2025-10-28 | committed | yes | high |
| OpenAI | Oracle | Cloud/compute (Stargate, ~4.5GW) | ~300B | 2025-07/09 | committed | no | high |
| OpenAI | CoreWeave | Compute contracts (cumulative) | ~22.4B | 2025-03 / 05 / 09 | committed | no | high |
| OpenAI | AMD | 6GW Instinct + warrant (up to 160M sh @ $0.01) | ~tens of B rev; ~10% warrant | 2025-10-05/06 | committed (warrant issued) | no | high |
| OpenAI | Broadcom | 10GW custom AI accelerators (XPU) | undisclosed (est. 150–200B) | 2025-10-13 | committed | no | high |
| OpenAI | NVIDIA | GPU/systems purchases (10GW) | part of $1.4T | 2025-09-22 onward | committed | yes | high |
| SoftBank | OpenAI | Equity ($40B round + $30B follow-on) | 41B funded + 30B follow-on | 2025 (closed Dec 2025) / 2026-02-27 | closed + committed | no | high |
| Amazon | OpenAI | Equity (mega-round) | 50B (15B initial + 35B) | 2026-02-27 | committed | no | high |

---

## Entity snapshot

- **OpenAI** — recapitalized Oct 28, 2025 into **OpenAI Group PBC** (controlled by nonprofit foundation). Microsoft holds ~**27%** (~$135B). Valuation: ~$500B (Oct 2025 secondary) -> ~$840B post-money (Feb 27, 2026, $110B round at $730B pre) -> ~**$852B** after $122B round closed Mar 31, 2026. Revenue run-rate ~**$20B** (end-2025); net loss ~$13.5B in H1 2025. ~**$1.4T** disclosed compute commitments over ~8 years.
- **NVIDIA** — supplier turned strategic investor across the customer base ("vendor financing"/round-trip pattern flagged by analysts).
- **CoreWeave** — NVIDIA ~7% holder; revenue backstopped by NVIDIA take-or-pay through 2032.
- **AMD** — issued OpenAI a warrant for up to 160M shares (~10%) at $0.01, vesting on GPU-purchase milestones (1GW first tranche, full at 6GW).

---

## Documented circular dollars (defensible)

Counting supplier->customer capital flows that recycle into supplier products:

- NVIDIA->OpenAI **$30B** (closed equity) — circular (OpenAI buys NVIDIA).
- NVIDIA->CoreWeave **$6.3B** backstop (+ ~7% stake) — circular.
- NVIDIA->xAI **~$2B** — circular (SPV buys NVIDIA GPUs).
- NVIDIA->Anthropic **up to $10B** (+ Microsoft $5B) against $30B Azure/NVIDIA spend — circular.

**Conservative documented NVIDIA-side circular total: ~$48B closed/committed** (excluding the lapsed $100B LOI and the indirect Intel/Nokia/Nscale/Mistral cases). If the lapsed $100B LOI is included as "announced," the headline circular figure cited in press is ~$110B+.

---

## What could NOT be verified / caveats

- **Broadcom 10GW dollar value** — financial terms officially **undisclosed**; "$150–200B" is a Mizuho *estimate*, not company-confirmed.
- **NVIDIA->xAI exact amount** — reported "up to $2B"; precise funded amount not separately confirmed in a filing.
- **Nscale** — sources conflict (£500M vs $667M); treat as ~$0.5–0.7B.
- **Mistral** — NVIDIA's specific check size within the EUR1.7B round not disclosed.
- **The $100B NVIDIA->OpenAI LOI** — never became a definitive agreement; no money changed hands under it (WSJ, CNBC, CFO confirmation). Do **not** count as closed.
- **$1.4T commitment figure** — Altman's verbal characterization (Nov 2025), not a single audited schedule; mixes binding and framework deals across ~8 years.

---

## Sources

- NVIDIA->OpenAI LOI: https://blogs.nvidia.com/blog/openai-nvidia/ ; https://www.cnbc.com/2025/09/22/nvidia-openai-data-center.html
- LOI lapsed / replaced: https://www.cnbc.com/2026/02/03/nvidia-openai-stalled-on-their-mega-deal-ai-giants-need-each-other.html ; https://gizmodo.com/the-100-billion-openai-nvidia-deal-is-not-happening-2000729749
- OpenAI mega-round ($110B/$122B, $30B NVIDIA): https://www.cnbc.com/2026/02/27/open-ai-funding-round-amazon.html ; https://www.cnbc.com/2026/03/31/openai-funding-round-ipo.html ; https://www.bloomberg.com/news/articles/2026-03-31/openai-valued-at-852-billion-after-completing-122-billion-round
- NVIDIA->CoreWeave backstop (SEC 8-K): https://www.sec.gov/Archives/edgar/data/0001769628/000176962825000047/crwv-20250909.htm
- CoreWeave ~7% / $6.3B context: https://invezz.com/news/2025/09/15/coreweave-shares-jump-7-after-unveiling-6-3-billion-nvidia-deal/
- NVIDIA->xAI: https://x.ai/news/series-e ; https://finance.yahoo.com/news/nvidia-reportedly-invest-2bn-elon-101712438.html
- NVIDIA/Microsoft->Anthropic: https://blogs.microsoft.com/blog/2025/11/18/microsoft-nvidia-and-anthropic-announce-strategic-partnerships/ ; https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships
- NVIDIA->Intel $5B: https://fortune.com/2025/09/18/nvidia-intel-5-billion-investment/ ; https://www.tomshardware.com/tech-industry/nvidia-gives-intel-a-lifeline-with-usd5-billion-common-stock-deal-september-deal-gets-ftc-approval-for-more-than-217-4-million-intel-shares-at-usd23-28-per-share
- NVIDIA->Nokia $1B: https://www.nokia.com/newsroom/inside-information-nvidia-to-make-usd-1-billion-equity-investment-in-nokia-in-addition-to-new-strategic-partnership-nokias-board-resolved-on-directed-share-issuance-to-nvidia/
- NVIDIA->Nscale/Mistral: https://www.cnbc.com/2026/01/26/nvidia-ai-startup-investments-europe-chips-jensen-huang.html ; https://www.nscale.com/press-releases/nscale-series-b
- OpenAI->Microsoft ($250B Azure, 27% stake, PBC): https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ ; https://www.geekwire.com/2025/microsoft-secures-27-stake-in-openai-in-new-deal-with-commitment-for-250b-in-azure-usage/ ; https://www.cnbc.com/2025/10/28/open-ai-for-profit-microsoft.html
- OpenAI->Oracle (~$300B Stargate): https://openai.com/index/five-new-stargate-sites/ ; https://www.datacenterdynamics.com/en/news/openai-signs-300bn-cloud-deal-with-oracle-report/
- OpenAI->CoreWeave (~$22.4B): https://www.coreweave.com/news/coreweave-expands-agreement-with-openai-by-up-to-6-5b
- OpenAI->AMD (6GW + warrant, SEC 8-K): https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/d28189d8k.htm ; https://www.cnbc.com/2025/10/06/openai-amd-chip-deal-ai.html
- OpenAI->Broadcom (10GW XPU): https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10 ; https://www.servethehome.com/broadcom-and-openai-announce-a-10gw-custom-xpu-deal/
- SoftBank->OpenAI: https://group.softbank/en/news/press/20251231 ; https://group.softbank/en/news/press/20260227 ; https://www.cnbc.com/2025/12/30/softbank-openai-investment.html
- OpenAI $1.4T commitments / $20B ARR: https://techcrunch.com/2025/11/06/sam-altman-says-openai-has-20b-arr-and-about-1-4-trillion-in-data-center-commitments/
- OpenAI losses / burn skepticism: https://fortune.com/2025/11/12/openai-cash-burn-rate-annual-losses-2028-profitable-2030-financial-documents/
