#!/usr/bin/env python3
"""
cross_review.py - RE-REVIEW past findings whenever a research block is added/changed.
Run this (with models/audit.py) on every corpus change. It:
  1. re-validates all research JSON,
  2. flags cross-file EDGE conflicts (same from->to with materially different amounts),
  3. builds the entity co-occurrence map -> suggests missing cross-links + names the connectors,
  4. flags entities that appear in only one file (potentially under-connected).
Writes report/CROSS-REVIEW.md. Exit 0 always (advisory); read the flags and reconcile before commit.
"""
import json,glob,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES=os.path.join(ROOT,"research")

ALIAS={ "nvidia":"NVIDIA","openai":"OpenAI","microsoft":"Microsoft","msft":"Microsoft","oracle":"Oracle",
 "coreweave":"CoreWeave","anthropic":"Anthropic","amazon":"Amazon","aws":"Amazon","google":"Google","alphabet":"Google",
 "meta":"Meta","facebook":"Meta","amd":"AMD","broadcom":"Broadcom","avgo":"Broadcom","spacex":"SpaceX","spcx":"SpaceX",
 "xai":"xAI","softbank":"SoftBank","mgx":"MGX","blackrock":"BlackRock","apollo":"Apollo","blackstone":"Blackstone",
 "blue owl":"BlueOwl","pimco":"PIMCO","ellison":"Ellison","a16z":"a16z","andreessen":"a16z","worldcoin":"Worldcoin",
 "world id":"Worldcoin","tencent":"Tencent","alibaba":"Alibaba","ant group":"AntGroup","naspers":"Naspers","prosus":"Naspers",
 "ripple":"Ripple","xrp":"Ripple","stellar":"Stellar","xlm":"Stellar","mccaleb":"McCaleb","coinbase":"Coinbase",
 "fairshake":"Fairshake","genius act":"GENIUS","clarity act":"CLARITY","stargate":"Stargate","disney":"Disney",
 "epstein":"Epstein","summers":"Summers","thiel":"Thiel","palantir":"Palantir","anduril":"Anduril","mp materials":"MP_Materials",
 "crml":"CRML","tmc":"TMC","sealsq":"SEALSQ","laes":"SEALSQ","wisekey":"WISeKey","wkey":"WISeKey","chainlink":"Chainlink",
 "link":"Chainlink","hedera":"Hedera","hbar":"Hedera","algorand":"Algorand","sui":"Sui","mysten":"Sui","tony blair":"TBI",
 "first brands":"FirstBrands","ubs":"UBS","jpmorgan":"JPMorgan","jpm":"JPMorgan","fdic":"FDIC","centrus":"Centrus",
 "lazarus":"Lazarus","dprk":"DPRK","bis":"BIS","swift":"SWIFT","brics":"BRICS","tiktok":"TikTok","circle":"Circle","usdc":"Circle",
 "waters":"Waters","hfsc":"HFSC","in-q-tel":"InQTel","mubadala":"MGX","pif":"PIF",
 "ibm":"IBM","ionq":"IonQ","rigetti":"Rigetti","d-wave":"DWave","qbts":"DWave","qubt":"QuantumComputingInc","scale ai":"ScaleAI","scaleai":"ScaleAI","oklo":"Oklo","quantinuum":"Quantinuum","psiquantum":"PsiQuantum","trail of bits":"TrailOfBits","terrapower":"TerraPower","vistra":"Vistra","nist":"NIST","nsa":"NSA","crqc":"CRQC","instagram":"Meta","whatsapp":"Meta","threads":"Meta"}

def iclass(instr):
    t=(instr or "").lower()
    for k in ["equity","debt","backstop","take-or-pay","compute","cloud","azure","aws","tpu","gpu","warrant","revenue","ipo","offtake","equity_method"]:
        if k in t: return {"take-or-pay":"backstop","azure":"compute","aws":"compute","cloud":"compute","tpu":"compute","gpu":"gpu_purchase","equity_method":"equity_method"}.get(k,k)
    return "other"
files=sorted(glob.glob(os.path.join(RES,"*.json")))
ent_files={}        # entity -> set(files)
edges={}            # (from,to) -> list[(amount,file,instrument)]
bad=[]
def canon(s): return ALIAS.get(s.strip().lower().split("(")[0].strip(), None)
for fp in files:
    name=os.path.basename(fp)
    try: d=json.load(open(fp))
    except Exception as e: bad.append(f"{name}: {e}"); continue
    text=open(fp,encoding="utf-8").read().lower()
    for k,v in ALIAS.items():
        if re.search(r"(?<![a-z])"+re.escape(k)+r"(?![a-z])",text): ent_files.setdefault(v,set()).add(name)
    def walk(o):
        if isinstance(o,dict):
            if "from" in o and "to" in o:
                a=o.get("amount_usd");
                if isinstance(a,(int,float)):
                    ins=o.get("instrument","") or o.get("raw_instrument","")
                    edges.setdefault((canon(str(o["from"])) or o["from"], canon(str(o["to"])) or o["to"], iclass(ins)),[]).append((a,name,ins))
            for x in o.values(): walk(x)
        elif isinstance(o,list):
            for x in o: walk(x)
    walk(d)

out=["# Cross-Review — re-review of all prior findings\n"]
out.append("## JSON validity"); out.append("- ALL VALID" if not bad else "\n".join("- BAD "+b for b in bad))
# edge conflicts
out.append("\n## Edge-amount reconcile (same from->to, materially different amounts across files)")
conf=0
for (a,b,cls),lst in sorted(edges.items()):
    amts={round(x[0]/1e9,1) for x in lst}
    if len(amts)>1 and (max(amts)/(min(amts) or 1))>=1.5:
        conf+=1
        det="; ".join(f"${x[0]/1e9:.1f}B [{x[1]}]" for x in lst)
        out.append(f"- ⚠ **{a} → {b}** ({cls}): {det}  (same-instrument differing amounts — reconcile: LOI vs closed / cumulative / date?)")
if not conf: out.append("- none — edge amounts consistent (or differences explained by instrument/date)")
# connectors
out.append("\n## Connectors (entities appearing across the most files)")
for e,fs in sorted(ent_files.items(),key=lambda kv:-len(kv[1]))[:12]:
    out.append(f"- **{e}** — {len(fs)} files")
# under-connected
solo=[e for e,fs in ent_files.items() if len(fs)==1]
out.append("\n## Under-connected entities (appear in only ONE file — candidates for new cross-links)")
out.append("- "+", ".join(sorted(solo)) if solo else "- none")
# per-file related (shared-entity) suggestions for the most-recently-modified file
newest=max(files,key=os.path.getmtime); nb=os.path.basename(newest)
nents={e for e,fs in ent_files.items() if nb in fs}
rel={}
for e in nents:
    for f in ent_files[e]:
        if f!=nb: rel[f]=rel.get(f,0)+1
out.append(f"\n## Newest file `{nb}` — related files by shared entities (verify cross-refs exist)")
for f,c in sorted(rel.items(),key=lambda kv:-kv[1])[:8]: out.append(f"- {f}: {c} shared entities")
open(os.path.join(ROOT,"report","CROSS-REVIEW.md"),"w").write("\n".join(out))
print("\n".join(out))
print(f"\n[CROSS-REVIEW] edge-conflicts={conf} bad-json={len(bad)} entities={len(ent_files)} solo={len(solo)} newest={nb}")
