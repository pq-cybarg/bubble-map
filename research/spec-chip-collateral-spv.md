# Chip-collateralized SPV leaseback - moving AI compute (and its debt) off the balance sheet

*(Circular-financing / off-balance-sheet thread. The newest wrinkle in the AI-capital loop: don't just borrow to buy chips - put the chips in a separate vehicle, let outside investors own the debt, and lease the same hardware back. The operator keeps the compute; the balance sheet keeps the optics.)*

## The structure (fact of the mechanism)
1. An operator has (or wants) billions in AI chips.
2. The chips go into a **special-purpose vehicle (SPV)**.
3. The SPV **issues debt** to outside investors (private credit, insurers, annuity funds) to fund the chips; investors may also get a slice of equity.
4. The operator **leases the chips back** and keeps running them.
5. Result: the hardware - **and the debt that paid for it** - sits off the operator's balance sheet. Reported assets rise more slowly, return-on-asset ratios look stronger, and **residual-value risk** (chips that can lose value in months) shifts to the investors.

## The named deals
- **Amazon, ~$8B (REPORTED / UNCONFIRMED):** per the FT (2026), Amazon is in talks to spin ~$8B of **NVIDIA Grace Blackwell** chips already in its US data centers into an SPV and lease them back; outside investors would hold the debt plus up to ~10% equity, with **Amazon retaining no ownership**. Described as **under discussion, not signed.** *(This is Amazon's own vehicle - the reporting does **not** name Apollo as the counterparty.)*
- **Anthropic, ~$35B - Apollo + Blackstone "AI XPV" (FACT, closed 9 Jun 2026):** a **hardware-collateralized** vehicle - one of the largest private-credit deals ever - that buys **Broadcom-codesigned Google TPUs**, leases them to Anthropic, and keeps the ~$35B off Anthropic's balance sheet. Funded largely by **insurance + annuity** capital; **Broadcom backstops the senior tranches** (the chip vendor underwriting the financing of its own chips).
- **xAI, ~$3.5B - Apollo + Valor (FACT, Jan 2026):** Apollo-managed funds led a ~$3.5B capital solution into **Valor Compute Infrastructure (VCI)** for its ~$5.4B acquisition-and-lease of **NVIDIA GB200** compute to an xAI subsidiary via a **triple-net lease** - powering a large Grok cluster.

## On the "Amazon/Apollo" question (honest correction)
There is **no confirmed Amazon-Apollo deal.** Two true things got conflated: **(a)** Amazon's *own* reported $8B chip-SPV leaseback, and **(b)** **Apollo**, which is the archetypal operator of the *same mechanism* for **Anthropic** and **xAI**. Same playbook - chips in an SPV, leased back, off balance sheet - **different names.** NVIDIA has also named Apollo among **six** institutions tapped to mobilize **>$500B** of third-party AI-infra capital (Aug 2026), so Apollo is the connective tissue of this layer even where it isn't Amazon's counterparty.

## Why it matters (the thesis)
- **It extends the circular loop.** Chip vendors (NVIDIA/Broadcom) sell the chips; vendor-adjacent capital helps **finance** the buyers; the chips are **collateral** for debt that **insurers/annuities** hold; the AI firms lease the chips back. Value and risk circle within the same ecosystem - now with a financing layer that makes the leverage **less visible.** *(circularity read = interpretation, labeled.)*
- **The collateral is the catch.** GPUs/TPUs **depreciate fast** - Amazon itself cut assumed server life from **6 to 5 years** (early-2025 filing) citing AI's pace. If residual values fall faster than the leases amortize, the collateral under the debt erodes - **concentrated, correlated, maturity-clustered** (the same fragility as the neocloud refinancing wall).
- **Regulators have noticed.** The **BIS** has warned about **"shadow borrowing"** in exactly these structures - leverage that doesn't show up where you'd look for it.
- **It rhymes with the real-estate side.** Meta's **Hyperion** datacenter uses a **Blue Owl / Beignet** off-balance-sheet SPV on the **land/building** side; chip-collateral SPVs do it on the **silicon** side. The off-balance-sheet AI buildout now spans **both**.

## Honest limits
The Apollo/Blackstone (Anthropic) and Apollo/Valor (xAI) deals = **fact** (closed, reported with terms). The Amazon chip-SPV = **reported/unconfirmed** (FT; under discussion). "Hiding data-center **losses**" is the popular framing; more precisely these are **off-balance-sheet, asset-light optics + residual-value-risk transfer + financing** - whether that is prudent risk-distribution or opacity that hides leverage is **contested** (BIS leans toward the latter). The circularity + systemic-fragility reads are **interpretation**, labeled. No cabal asserted - this is a *convergent market structure*, several firms independently reaching for the same balance-sheet tool.

*Sources: FT (Amazon $8B chip SPV, 2026) via Finimize/AOL; Apollo + Blackstone AI XPV / Anthropic (Jun 2026); Apollo + Valor / VCI / xAI (Jan 2026); NVIDIA six-institution >$500B announcement (Aug 2026); BIS shadow-borrowing warning; Amazon 10-K/Q server-life change (2025). Cross-refs: Amazon, Apollo, Blackstone, Broadcom, Anthropic, xAI, NVIDIA, Chip_Collateral_SPV, AI_XPV_Platform, Valor_Compute, AI_Datacenters, Beignet_Investor, PrivateCredit_Funds, Neocloud_Refinancing_Wall.*
