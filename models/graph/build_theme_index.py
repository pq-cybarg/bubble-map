#!/usr/bin/env python3
"""
build_theme_index.py - auto-group the research corpus under the ~14 themes of the
flagship/atlas meta-map (docs/themes.js). Scans research/*.md, derives each block's
title + rendered page (docs/r-<base>.html), classifies it to its best-fit theme by
keyword score, and writes docs/theme-blocks.json:  { themeId: [{t:title, h:href}], ... }

This powers the Atlas theme->blocks zoom. It is a NAVIGATION aid (best-fit grouping),
not a claim; blocks can touch several themes. Regenerable; run from new-research.sh.
"""
import os, glob, json, re
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS=os.path.join(ROOT,"docs")

# theme id -> keyword patterns (checked against basename + title, lowercased). Order = tie-break priority.
RULES=[
 ("antidote",   ["vitalik","post-quantum","postquantum","crqc","quantum","decentral","self-sovereign","cypherpunk","d/acc","formal-verif","zk","zero-knowledge"]),
 ("control",    ["digitalid","digital-id","surveillance","worldcoin","age-verif","cbdc","biometric","eidas","chat-control","identity","censorship","adtech"]),
 ("epistemic",  ["reproducib","integrity","arxiv","ai-slop","slop","benchmark","eval-","disinformation","lens-reread","strategic-lens","-lenses","reread"]),
 ("techtransfer",["research-security","tech-transfer","tech-transfer","csc","scholarship","talent","espionage"]),
 ("minerals",   ["rare-earth","rare_earth","critical-mineral","critical_mineral","antimony","eudialyte","critical-minerals","lithium","cobalt","mineral","commodities","-metals"]),
 ("compute",    ["chip","semiconductor","euv","tsmc","asml","hbm","silicon","lithography","fab"]),
 ("defense",    ["defense","defence","geopolitic","taiwan","russia","iran","-war","arctic","cable","contested-resource","military","space-layer","drone","telecom","satellite","attribution","lazarus","unc-nk","nk-"]),
 ("insurance",  ["insurance","healthcare","health-care","pbm","disability","medicare","medicaid","denial","health"]),
 ("banking",    ["fdic","-cre","real-estate","bank","credit","htm","mortgage","regional-leverage","contagion","duration","fed-trap","firstbrands","ubs","dereg","municipal","public-finance","basis-trade","treasury-basis"]),
 ("stablecoin", ["stablecoin","tether","usdc","crypto","blockchain","altcoin","onchain","on-chain","settlement","ripple","hedera","genius","exchange","scam-fara","tornado","samourai","mixer"]),
 ("capital",    ["gulf","sovereign","mgx","pif","softbank","private-credit","apollo","blackstone","blackrock","stargate","datacenter","capex","-capital","family-office","family-offices","pension","ldi"]),
 ("legitimacy", ["person","influence","governance","legitimacy","conversion","lobby","fara","epstein","tbi","labour","political","disclosure","prediction-market","manufactured","network-overlay","sec-filing","filings","anomalous","disappearance","deaths"]),
 ("hardmoney",  ["gold","silver","hard-money","official-data","cpi","rent-","inflation","data-integrity","reprice","gig-labor","futures-vs-physical","cross-sectional"]),
 ("ai-loop",    ["fin-","nvidia","openai","oracle","coreweave","anthropic","hyperscaler","ai-core","circular","carry-trade","cross-system","speculation","power-grid","grid-bottleneck"]),
]
THEME_IDS=[r[0] for r in RULES]

def title_of(md):
    try:
        for line in open(md,encoding="utf-8",errors="ignore"):
            s=line.strip()
            if s.startswith("# "): return re.sub(r'\s+',' ',s[2:].strip())
    except Exception: pass
    return os.path.basename(md)[:-3]

def classify(base, title):
    hay=(base+" "+title).lower()
    best,score=None,0
    for tid,pats in RULES:
        sc=sum(1 for p in pats if p in hay)
        if sc>score: best,score=tid,sc
    return best  # may be None

out={t:[] for t in THEME_IDS}
unmatched=[]
for md in sorted(glob.glob(os.path.join(ROOT,"research","*.md"))):
    base=os.path.basename(md)[:-3]
    page=os.path.join(DOCS,"r-"+base+".html")
    if not os.path.exists(page): continue          # only blocks with a rendered page
    title=title_of(md)
    tid=classify(base,title)
    if tid is None:
        unmatched.append(base); tid="ai-loop"       # default bucket
    out[tid].append({"t":title,"h":"r-"+base+".html","b":base})

for t in out: out[t].sort(key=lambda x:x["t"].lower())
json.dump(out, open(os.path.join(DOCS,"theme-blocks.json"),"w"), ensure_ascii=False, indent=0)
tot=sum(len(v) for v in out.values())
print(f"[THEME-INDEX] {tot} blocks grouped across {len(THEME_IDS)} themes | unmatched(default-bucketed): {len(unmatched)}")
print("  " + " ".join(f"{t}:{len(out[t])}" for t in THEME_IDS))
if unmatched: print("  unmatched:", ", ".join(unmatched[:20]))
