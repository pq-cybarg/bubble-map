#!/usr/bin/env python3
"""
altcoin_lens.py - apply the same lens (real value capture vs debasement/narrative-beta, and
token-value accrual vs mere usage) to a basket of altcoins, and map each to the analysis threads.
Honest grading, NOT price prediction. Sources web-verified 2026-06-07.
"""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# name: (what, real-adoption evidence, token-value accrual, thread tie, GRADE)
TOK={
 "XRP (Ripple)":("cross-border payments / RLUSD stablecoin",
   "SBI ~9% owner; bank corridors (RippleNet); RLUSD; spot ETF; SEC case won in part (2023)",
   "moderate (payments volume != token demand; XRP largely speculative)",
   "payments/Japan (SBI) + SEC selective-enforcement thread (Hinman ETH vs XRP)","REAL-USE / weak-accrual"),
 "LINK (Chainlink)":("oracle + cross-chain (CCIP) for tokenization",
   "SWIFT (11,500 banks; tokenized-bond milestone Apr-2026), Euroclear, UBS, JPM Kinexys, Mastercard, Ondo; ~$75B secured; CRE runtime live",
   "improving (staking/CCIP fees) but value-accrual still debated",
   "THE tokenization 'picks & shovels' -> BIS Project Agora / stablecoin rails","REAL-INFRA (strongest utility)"),
 "HBAR (Hedera)":("enterprise DLT, RWA settlement",
   "31-member council (Google/IBM/Boeing/FedEx/Standard Bank); >$10B RWA settled; SWIFT ISO20022 test; SEC/CFTC 'digital commodity'; acquired Hyperledger Fabric IP",
   "WEAK ('enterprise adoption means nothing when token holders get ~zero revenue' - the core critique)",
   "enterprise tokenization + temporal-web (Google council member)","REAL-ADOPTION / weak-accrual"),
 "ALGO (Algorand)":("L1 (Micali); CBDC/tokenization pilots",
   "~$0.09, mcap ~$0.8B (#62); Revolut staking, PostFinance; classified 'digital commodity'",
   "weak (token languished despite solid tech)","tokenization/CBDC rails","SOLID-TECH / modest-traction"),
 "Story / IP (Story Protocol)":("L1 to tokenize INTELLECTUAL PROPERTY for the AI era",
   "a16z $80M Series B at $2.25B val; 'IP Legos'; Bieber/BTS/Blackpink/Adidas; pitched as creator defense vs LLMs",
   "early/speculative; narrative-led",
   "AI x IP provenance -> DIRECTLY the Disney/Sora thread; a16z = the connective weaver node","THEMATIC-SPECULATIVE (AI-IP)"),
 "QRL (Quantum Resistant Ledger)":("post-quantum L1 (XMSS -> SPHINCS+/FIPS205)",
   "live since 2018; +45% spikes on quantum-risk headlines (Mar-2026); tiny mcap",
   "narrative-driven; thin liquidity","quantum thread -> same narrative as LAES/WKEY (PQC chips)","THEMATIC-SPECULATIVE (quantum)"),
 "MCM (Mochimo)":("post-quantum PoW coin (since 2018)",
   "niche PQ community; minimal institutional use","narrative/speculative","quantum thread (with QRL)","SPECULATIVE-NICHE"),
 "POL (Polygon)":("Ethereum scaling L2 / 'agg' network (ex-MATIC)",
   "large ecosystem, payments push; broad DeFi/enterprise pilots","moderate; competitive/commoditized scaling","Ethereum-scaling infra","INFRA / commoditized"),
 "POLY (Polymath)":("security-token issuance platform (ST-20)",
   "~$0.02, faded; security-token thesis never scaled","weak/dormant","tokenization-of-securities (early, stalled)","FADED-NARRATIVE"),
 "XLM (Stellar)":("payments/remittance + RWA tokenization",
   "MoneyGram; USDC on Stellar; Franklin Templeton BENJI tokenized money-market fund runs on Stellar; co-founded by Jed McCaleb",
   "moderate; large foundation-held supply",
   "payments + RWA tokenization + the McCaleb Mt.Gox->Ripple->Stellar lineage (spec-crypto-sec-epstein)","REAL-USE / weak-accrual"),
 "SUI (Mysten Labs)":("Move-based high-throughput L1",
   "built by ex-Meta DIEM/Novi engineers (Mysten Labs); a16z-backed (FTX historically); DeFi/gaming throughput",
   "moderate; heavy insider/VC unlocks",
   "DIRECT Meta/Diem-stablecoin lineage (the Facebook coin that died, reborn as Sui) + a16z connective node","VC-L1 / Diem-lineage"),
}
THREADS={
 "tokenization (BIS Agora / RWA)":["LINK (Chainlink)","HBAR (Hedera)","ALGO (Algorand)","POLY (Polymath)","XLM (Stellar)"],
 "payments (Japan/SBI, banks)":["XRP (Ripple)","XLM (Stellar)"],
 "AI x IP provenance (Disney/Sora, a16z)":["Story / IP (Story Protocol)"],
 "quantum (PQC chips LAES/WKEY)":["QRL (Quantum Resistant Ledger)","MCM (Mochimo)"],
 "Ethereum scaling":["POL (Polygon)"],
 "Meta/Diem lineage (a16z VC L1s)":["SUI (Mysten Labs)"],
 "McCaleb lineage (Mt.Gox->Ripple->Stellar)":["XRP (Ripple)","XLM (Stellar)"],
}

print("="*98); print("ALTCOIN LENS  -  real value capture vs narrative-beta, + token-value accrual, mapped to threads"); print("="*98)
out={}
for t,(what,adopt,accr,thread,grade) in TOK.items():
    print(f"\n{t}  [{grade}]")
    print(f"   what:      {what}")
    print(f"   adoption:  {adopt}")
    print(f"   token val: {accr}")
    print(f"   thread:    {thread}")
    out[t]={"what":what,"adoption":adopt,"token_value_accrual":accr,"thread":thread,"grade":grade}
print("\n"+"="*98)
print("THE LENS (meta-finding):")
print(" - REAL-INFRA for tokenization exists (LINK strongest; HBAR/ALGO real enterprise use) - but TOKEN-VALUE")
print("   ACCRUAL is consistently WEAK: institutions use the rails; the token rarely captures the value.")
print(" - The 'thematic' alts (Story=AI-IP, QRL/MCM=quantum) ride the SAME narratives as the equity micro-caps")
print("   (LAES/WKEY quantum, CRML minerals): real macro theme, speculative vehicle, a16z often the connective node.")
print(" - In GOLD: only BTC is durably up (real monetization); most alts are debasement-beta or narrative spikes.")
print(" - NET: like the equity split (NVDA up in gold vs S&P down), crypto splits into a few real-utility rails")
print("   (now wired to Treasuries via stablecoins) and a long tail of narrative-beta tracking the same themes.")
out["_meta"]={"threads":THREADS,"finding":"Real tokenization/payments infra (LINK/HBAR/XRP/ALGO) with weak token-value accrual; thematic alts (Story/QRL/MCM) ride the same AI-IP/quantum narratives as equity microcaps; only BTC durably up in gold. a16z is a recurring connective node (Story, Fairshake, Worldcoin)."}
json.dump(out,open(os.path.join(ROOT,"data","altcoin_lens.json"),"w"),indent=2)
print("\nwrote data/altcoin_lens.json")
