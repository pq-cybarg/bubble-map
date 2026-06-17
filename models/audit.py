#!/usr/bin/env python3
"""audit.py - cross-document consistency + coverage + validity audit. Writes report/AUDIT.md."""
import json,os,glob,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(p):
    try:return json.load(open(os.path.join(ROOT,"data",p)))
    except:return {}
g=J("graph.json");gs=J("gold_silver_reprice.json");eq=J("equity_in_gold.json");sc=J("scenarios.json")
an=g.get("analysis",{})
canon={
 "core_scc_robust": an.get("core_scc_robust_size"),
 "core_scc_all": an.get("core_scc_all_size"),
 "cycles": an.get("num_elementary_cycles"),
 "nvda_headline_pct": round(an.get("nvidia_self_funding",{}).get("headline_ratio",0)*100),
 "nvda_funded_pct": round(an.get("nvidia_self_funding",{}).get("funded_ratio",0)*100),
 "home_gold_idx_2026": (gs.get("home_repriced") or [{}])[-1].get("idx_gold"),
 "sp500_gold_chg": eq.get("split",{}).get("sp500_gold_change_pct_2000_2026"),
 "nvda_gold_chg": eq.get("split",{}).get("nvda_gold_change_pct_2016_2026"),
 "base_gap": sc.get("scenarios",{}).get("BASE",{}).get("capital_gap_usd_b"),
}
out=["# Consistency & Coverage Audit\n",f"Canonical numbers (from data/*.json — the source of truth):\n"]
for k,v in canon.items(): out.append(f"- `{k}` = **{v}**")
# counts
nmodels=len(glob.glob(ROOT+"/models/**/*.py",recursive=True))+len(glob.glob(ROOT+"/models/**/*.tla",recursive=True))+len(glob.glob(ROOT+"/models/**/*.als",recursive=True))
npy_z3=len(glob.glob(ROOT+"/models/z3/*.py"))
nres=len(glob.glob(ROOT+"/research/*.json")); nresmd=len(glob.glob(ROOT+"/research/*.md"))
ndata=len(glob.glob(ROOT+"/data/*.json")); nrep=len(glob.glob(ROOT+"/report/*"))
out+=["\n## Inventory",f"- models: {nmodels} (z3 .py: {npy_z3}) + TLA + Alloy",
      f"- research: {nres} json / {nresmd} md",f"- data outputs: {ndata}",f"- reports: {nrep}"]
# JSON validity
bad=[]
for f in glob.glob(ROOT+"/research/*.json")+glob.glob(ROOT+"/data/*.json"):
    try:json.load(open(f))
    except Exception as e:bad.append(os.path.basename(f)+": "+str(e))
out+=["\n## JSON validity",("- ALL VALID" if not bad else "\n".join("- BAD "+b for b in bad))]
# cross-doc figure consistency: do reports mention the canonical core size + key %s?
texts={p:open(os.path.join(ROOT,p),encoding="utf-8",errors="ignore").read().replace("\u2212","-").replace(",","") for p in
       ["README.md","report/UNMASKING.md","report/EXECUTIVE-SUMMARY.md","report/INDEX.html","docs/index.html"] if os.path.exists(os.path.join(ROOT,p))}
checks=[("core-size",[str(canon["core_scc_robust"])+"-firm",str(canon["core_scc_robust"])+"-node",str(canon["core_scc_robust"])+" firm"]),("-81% home gold","-81"),
        ("+1985 nvda gold","1985"),("-69 sp500 gold","69"),("$1.03T",["1.03","1,03","1028","1,028"])]
flags=[]
for label,needle in checks:
    needles=needle if isinstance(needle,list) else [needle]
    for p,t in texts.items():
        if not any(n in t for n in needles): flags.append(f"{label}: NOT found in {p}")
# stale model/source counts in prose
for p,t in texts.items():
    for m in re.findall(r"(\d+)\s+(?:runnable )?models",t):
        if abs(int(m)-nmodels)>2: flags.append(f"stale model count '{m}' in {p} (actual ~{nmodels})")
    for m in re.findall(r"(\d+)\s+cited (?:source|research)",t):
        if abs(int(m)-nres)>2: flags.append(f"stale source count '{m}' in {p} (actual {nres})")
out+=["\n## Cross-document consistency flags",("- none — consistent" if not flags else "\n".join("- ⚠ "+f for f in flags))]
# leg coverage matrix
legs={"AI core":"fin-nvidia","banking":"macro-fdic","CRE/credit":"macro-cre","commodities":"commodities-metals",
      "defense":"defense-rare-earth","energy":"energy-power","blockchain":"blockchain-leg","altcoins":"altcoin-lens",
      "influence":"influence-tbi","temporal":"temporal-bridges","gold-lens":"macro-gold-silver","speculation":"spec-crypto"}
out.append("\n## Leg coverage (research present?)")
for leg,stub in legs.items():
    present=bool(glob.glob(ROOT+f"/research/{stub}*"))
    out.append(f"- {leg}: {'✓' if present else '✗ MISSING'}")
# research files missing sources
nosrc=[os.path.basename(f) for f in glob.glob(ROOT+"/research/*.json") if '"source"' not in open(f).read() and '"sources"' not in open(f).read() and 'source' not in open(f).read().lower()]
out.append("\n## Research files lacking any 'source' field")
out.append("- none" if not nosrc else "\n".join("- "+x for x in nosrc))
# composition/division-fallacy advisory: collective-noun + intent/belief verb.
# ADVISORY ONLY (not counted in flags). Verify each hit is institutional ACTION (attributable)
# or a graded/attributed claim - NOT an unhedged assertion of a unitary institutional MIND
# (composition: parts->whole intent; division: whole->parts intent). Names the guard so it stays clean.
_collectives=r"China|Beijing|the CCP|the NSA|the Fed|the government|the state|Labour|Wall ?Street|the banks|the architects|the West|the EU|Moscow|Washington|the CIA|the FBI|the Treasury|the regime|the elite"
_intent=r"wants?|wanted|intends?|intended|seeks?|fears?|believes?|hopes?|desires?|aims? to|plans? to|wishes?|is trying to|are trying to"
_cd=re.compile(r"\b("+_collectives+r")\s+("+_intent+r")\b", re.I)
_mentionq=set("'‘’")  # single quotes = the phrase is MENTIONED/quoted (e.g. rejecting "'the NSA wants X' is a fiction"), not ASSERTED
cdhits=[]
for f in sorted(glob.glob(ROOT+"/research/*.json")):
    txt=open(f,encoding="utf-8",errors="ignore").read()
    for m in _cd.finditer(txt):
        if m.start()>0 and txt[m.start()-1] in _mentionq:
            continue  # quoted mention, not an asserted unitary mind -> skip false positive
        cdhits.append(f"{os.path.basename(f)}: '{m.group(0)}'")
out.append("\n## Composition/division review (advisory — collective-intent phrasing; confirm institutional ACTION or graded claim, not asserted unitary MIND)")
out.append("- none" if not cdhits else "\n".join("- ⚑ "+h for h in cdhits)+f"\n  ({len(cdhits)} advisory hit(s) to verify)")
open(os.path.join(ROOT,"report","AUDIT.md"),"w").write("\n".join(out))
print("\n".join(out))
print("\n[AUDIT] flags:",len(flags),"| bad json:",len(bad),"| models:",nmodels,"| research:",nres)
