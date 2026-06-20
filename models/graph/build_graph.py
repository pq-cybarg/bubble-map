#!/usr/bin/env python3
"""
build_graph.py - Consolidate heterogeneous research/*.json into ONE canonical
funding graph, then run structural formal analysis:
  - alias normalization + edge dedupe (+ 'cancelable' flag)
  - Tarjan strongly-connected components (the formal definition of "circular")
  - DUAL SCC: all edges vs. excluding-cancelable -> shows SpaceX entering/leaving the core
  - elementary cycle enumeration
  - circularity-exposure metric per node
  - NVIDIA vendor-financing self-funding ratio (funded vs headline)
Outputs: data/graph.json, data/edges.csv, data/entities.csv + printed proof report.
Pure stdlib.
"""
import json, glob, csv, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "research"); DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

ALIAS = {
 "nvidia":"NVIDIA","NVIDIA":"NVIDIA","openai":"OpenAI","OpenAI":"OpenAI","OPENAI":"OpenAI",
 "microsoft":"Microsoft","Microsoft":"Microsoft","MSFT":"Microsoft","oracle":"Oracle","Oracle":"Oracle","ORCL":"Oracle",
 "coreweave":"CoreWeave","CoreWeave":"CoreWeave","CRWV":"CoreWeave","GOOGL":"Google","Google":"Google","Alphabet":"Google",
 "AMZN":"Amazon","Amazon":"Amazon","AWS":"Amazon","ANTHROPIC":"Anthropic","Anthropic":"Anthropic",
 "AVGO":"Broadcom","Broadcom":"Broadcom","AMD":"AMD","META":"Meta","Meta":"Meta","META_HYPERION_JV":"Meta_Hyperion_SPV",
 "xAI":"xAI","XAI":"xAI","SoftBank":"SoftBank","softbank":"SoftBank","stargate":"Stargate","Stargate":"Stargate",
 "mgx":"MGX","MGX":"MGX","Intel":"Intel","Nokia":"Nokia","Mistral":"Mistral","Nscale":"Nscale","nscale":"Nscale",
 "lambda":"Lambda","Lambda":"Lambda","crusoe":"Crusoe","Crusoe":"Crusoe","nebius":"Nebius","Nebius":"Nebius",
 "vantage":"Vantage","Vantage":"Vantage","Disney":"Disney",
 "Disney+NBCUniversal+WarnerBrosDiscovery":"Disney_Studios_Coalition","Midjourney":"Midjourney",
 "blackstone":"Blackstone","Blackstone":"Blackstone","BLUEOWL":"BlueOwl","PIMCO":"PIMCO","BLACKROCK":"BlackRock",
 "APOLLO_BLACKSTONE":"Apollo_Blackstone","Apollo":"Apollo","GIC":"GIC","jpmorgan":"JPMorgan",
 "Aladdin":"Aladdin","ALADDIN":"Aladdin","AIP":"AI_Infrastructure_Partnership","AI Infrastructure Partnership":"AI_Infrastructure_Partnership",
 "GIP":"GIP","Global Infrastructure Partners":"GIP","HPS":"HPS","HPS Investment Partners":"HPS",
 "IBIT":"IBIT","iShares Bitcoin Trust":"IBIT","Aligned":"Aligned_Data_Centers","Aligned Data Centers":"Aligned_Data_Centers",
 # quantum competitive landscape
 "IonQ":"IonQ","IONQ":"IonQ","Rigetti":"Rigetti","RGTI":"Rigetti","D-Wave":"D_Wave","DWave":"D_Wave","QBTS":"D_Wave","D_Wave":"D_Wave",
 "Quantinuum":"Quantinuum","QuEra":"QuEra","Atom Computing":"Atom_Computing","AtomComputing":"Atom_Computing","Atom_Computing":"Atom_Computing",
 "Pasqal":"Pasqal","IQM":"IQM","Quandela":"Quandela","Alice & Bob":"Alice_Bob","Alice and Bob":"Alice_Bob","Alice_Bob":"Alice_Bob","OQC":"OQC","Xanadu":"Xanadu",
 "Oxford Ionics":"Oxford_Ionics","Oxford_Ionics":"Oxford_Ionics","Vector Atomic":"Vector_Atomic","Vector_Atomic":"Vector_Atomic",
 "Origin Quantum":"Origin_Quantum","OriginQuantum":"Origin_Quantum","Origin_Quantum":"Origin_Quantum","USTC":"USTC",
 "RIKEN":"RIKEN","Riken":"RIKEN","Fujitsu":"Fujitsu","Honeywell":"Honeywell","GlobalFoundries":"GlobalFoundries","GLOBALFOUNDRIES":"GlobalFoundries","GF":"GlobalFoundries",
 "Temasek":"Temasek","QIA":"QIA","Qatar Investment Authority":"QIA","Australia":"Australia","EU Quantum Flagship":"EU_Quantum_Flagship",
 # blockchain ecosystem
 "Ethereum":"Ethereum","ETH":"Ethereum","Ethereum_Foundation":"Ethereum_Foundation","Ethereum Foundation":"Ethereum_Foundation","EF":"Ethereum_Foundation",
 "Consensys":"ConsenSys","ConsenSys":"ConsenSys","CONSENSYS":"ConsenSys","MetaMask":"MetaMask","Metamask":"MetaMask","Infura":"Infura","Linea":"Linea",
 "Mysten Labs":"Mysten_Labs","Mysten":"Mysten_Labs","Mysten_Labs":"Mysten_Labs","Sui":"Sui",
 "QRL":"QRL","Quantum Resistant Ledger":"QRL","QRL Foundation":"QRL_Foundation","QRL_Foundation":"QRL_Foundation",
 "XRPL":"XRPL","XRP Ledger":"XRPL","XRPLF":"XRPLF","XRP Ledger Foundation":"XRPLF","XRPL Labs":"XRPL_Labs","XRPL_Labs":"XRPL_Labs",
 "Ripple Prime":"Ripple_Prime","Hidden Road":"Ripple_Prime","Ripple_Prime":"Ripple_Prime","RLUSD":"RLUSD","Vitalik":"Vitalik","Vitalik Buterin":"Vitalik","Solana":"Solana","SOL":"Solana",
 # decentralized storage + stellar + privacy
 "Protocol Labs":"Protocol_Labs","Protocol_Labs":"Protocol_Labs","IPFS":"IPFS","Filecoin":"Filecoin","FIL":"Filecoin","Arweave":"Arweave","AR":"Arweave",
 "Sia":"Sia","Siacoin":"Sia","Walrus":"Walrus","DePIN_Storage":"DePIN_Storage",
 "Stellar":"Stellar","XLM":"Stellar","Stellar Development Foundation":"Stellar_Development_Foundation","Stellar_Development_Foundation":"Stellar_Development_Foundation","SDF":"Stellar_Development_Foundation",
 "Franklin Templeton":"Franklin_Templeton","Franklin_Templeton":"Franklin_Templeton","Zano":"Zano","Monero":"Monero","XMR":"Monero","Financial_Privacy":"Financial_Privacy",
 # oracles / interop / sidechains / more L1s / more privacy-PQ coins
 "Chainlink Labs":"Chainlink_Labs","Chainlink_Labs":"Chainlink_Labs","Band Protocol":"Band_Protocol","Band_Protocol":"Band_Protocol","BAND":"Band_Protocol",
 "SEDA":"SEDA","Flare":"Flare","FLR":"Flare","Axelar":"Axelar","AXL":"Axelar","Oracle_Interop":"Oracle_Interop",
 "Cosmos":"Cosmos","ATOM":"Cosmos","VeChain":"VeChain","VET":"VeChain","VeChain Foundation":"VeChain_Foundation","VeChain_Foundation":"VeChain_Foundation",
 "Xahau":"Xahau","XRPL EVM":"XRPL_EVM","XRPL_EVM":"XRPL_EVM","Salvium":"Salvium","Mochimo":"Mochimo",
 # omnichain interop + state/institutional collabs
 "LayerZero":"LayerZero","Wormhole":"Wormhole","WYST":"WYST","Wyoming":"Wyoming","DTCC":"DTCC","ICE":"ICE","Intercontinental Exchange":"ICE",
 "MAS":"MAS","Citadel Securities":"Citadel_Securities","Citadel_Securities":"Citadel_Securities","Securitize":"Securitize",
 "Uniswap":"Uniswap","VanEck":"VanEck","Hamilton Lane":"Hamilton_Lane","Hamilton_Lane":"Hamilton_Lane",
 # crypto-enforcement actors (persons + bodies)
 "Gary Gensler":"Gary_Gensler","Gensler":"Gary_Gensler","Gary_Gensler":"Gary_Gensler","William Hinman":"William_Hinman","Hinman":"William_Hinman","William_Hinman":"William_Hinman",
 "Jay Clayton":"Jay_Clayton","Clayton":"Jay_Clayton","Jay_Clayton":"Jay_Clayton","Damian Williams":"Damian_Williams","Damian_Williams":"Damian_Williams",
 "Caroline Crenshaw":"Caroline_Crenshaw","Caroline_Crenshaw":"Caroline_Crenshaw","Elizabeth Warren":"Elizabeth_Warren","Warren":"Elizabeth_Warren","Elizabeth_Warren":"Elizabeth_Warren",
 "Letitia James":"Letitia_James","Letitia_James":"Letitia_James","Rostin Behnam":"Rostin_Behnam","Rostin_Behnam":"Rostin_Behnam",
 "Paul Atkins":"Paul_Atkins","Paul_Atkins":"Paul_Atkins","Hester Peirce":"Hester_Peirce","Hester_Peirce":"Hester_Peirce","John Deaton":"John_Deaton","John_Deaton":"John_Deaton",
 "Brad Garlinghouse":"Brad_Garlinghouse","Brad_Garlinghouse":"Brad_Garlinghouse","Stuart Alderoty":"Stuart_Alderoty","Stuart_Alderoty":"Stuart_Alderoty",
 "SEC Crypto Task Force":"SEC_Crypto_Task_Force","SEC_Crypto_Task_Force":"SEC_Crypto_Task_Force","NCET":"NCET",
 "Operation Choke Point 2.0":"Operation_Choke_Point_2","Operation_Choke_Point_2":"Operation_Choke_Point_2","Simpson Thacher":"Simpson_Thacher","Simpson_Thacher":"Simpson_Thacher",
 # crypto founders / builders + projects
 "David Schwartz":"David_Schwartz","David_Schwartz":"David_Schwartz","JoelKatz":"David_Schwartz","Jed McCaleb":"Jed_McCaleb","Jed_McCaleb":"Jed_McCaleb",
 "Arthur Britto":"Arthur_Britto","Arthur_Britto":"Arthur_Britto","Evan Cheng":"Evan_Cheng","Evan_Cheng":"Evan_Cheng","Sam Blackshear":"Sam_Blackshear","Sam_Blackshear":"Sam_Blackshear",
 "Keonne Rodriguez":"Keonne_Rodriguez","Keonne_Rodriguez":"Keonne_Rodriguez","William L Hill":"William_L_Hill","William Lonergan Hill":"William_L_Hill","William_L_Hill":"William_L_Hill",
 "Zooko":"Zooko_Wilcox","Zooko Wilcox":"Zooko_Wilcox","Zooko_Wilcox":"Zooko_Wilcox","Jeremy Kauffman":"Jeremy_Kauffman","Jeremy_Kauffman":"Jeremy_Kauffman",
 "Zcash":"Zcash","ZEC":"Zcash","Electric Coin Company":"Electric_Coin_Company","Electric_Coin_Company":"Electric_Coin_Company","ECC":"Electric_Coin_Company","Odysee":"Odysee",
 "balance_sheet":"SINK_debt","bondholders":"SINK_bondmarket","BONDMARKET":"SINK_bondmarket","lenders":"SINK_lenders",
 "CAPEX":"SINK_capex","AI_BACKLOG":"SINK_backlog","AVGO_XPU_PLATFORM":"Broadcom",
 "US commercial banks":"US_Banks",
 "SpaceX":"SpaceX","SpaceX_IPO_Public_Markets":"SpaceX_IPO_Public","Starlink_Subscribers":"Starlink_Subscribers",
 "US_Government":"US_Government","MP_Materials":"MP_Materials","Defense_Primes":"Defense_Primes","Apple":"Apple",
 # de-fragmentation merges (same entity referenced under two spellings across blocks -> one node, interleaving the subgraphs)
 "China_state":"China","China (PRC)":"China","PRC":"China",
 "Russia_elite_environment":"Russia","Russian_state":"Russia",
 "TornadoCash":"Tornado_Cash","SamouraiWallet":"Samourai_Wallet",
 "WorldLibertyFinancial":"World_Liberty_Financial","WLFI":"World_Liberty_Financial","USD1":"World_Liberty_Financial",
 "Federal Reserve":"Federal_Reserve","FederalReserve":"Federal_Reserve","FOMC":"Federal_Reserve",
 # duplicate-node merges (same entity under two spellings -> one bubble)
 "Lazarus":"Lazarus_Group","Lazarus Group":"Lazarus_Group",
 "AI data centers":"AI_Datacenters","AI Datacenters":"AI_Datacenters","AI_Data_Centers":"AI_Datacenters",
 "Private-credit funds":"PrivateCredit_Funds","Private credit funds":"PrivateCredit_Funds",
}
def canon(n):
    n=(n or "?").strip()
    if n in ALIAS: return ALIAS[n]
    return ALIAS.get(n.split("(")[0].strip(), n.split("(")[0].strip())

def iclass(instr):
    s=(instr or "").lower()
    if "warrant" in s: return "warrant"
    if "backstop" in s or "take-or-pay" in s: return "backstop"
    if "gpu_purchase" in s or "systems purchases" in s or ("gpu" in s and "purchase" in s): return "gpu_purchase"
    if "equity_method_loss" in s: return "equity_method_loss"
    if "revenue_share" in s or "revenue share" in s: return "revenue_share"
    if "ipo_proceeds" in s: return "ipo_proceeds"
    if "exogenous_revenue" in s: return "exogenous_revenue"
    if "ip_litigation" in s: return "ip_litigation"
    if "ip_license" in s: return "ip_license"
    if "cease" in s: return "ip_cease_desist"
    # structural / relationship classes (NON money-flow) - classify before generic 'equity'
    if "governance" in s or "council" in s: return "governance"
    if any(k in s for k in ["enforcement","prosecution","conviction","sanction","pardon","foia","pause_order","pause letter","pause_letter","transparency_act","guidance_contradict","plea","subpoena"]): return "regulatory_legal"
    if "litigation" in s and "ip" not in s: return "regulatory_legal"
    if any(k in s for k in ["breach","backbone_tap","prism","bullrun","backdoor","honeypot","wiretap","laundering","leak_disclosure","_641a"]): return "surveillance_security"
    if any(k in s for k in ["code_donation","built_on","launch","adoption","etf","mou","subsidy","grant","research_commission","military","starshield","kaband","direct_to_cell","stablecoin","registry","cia_seed","iso20022","ccip","tokenization_poc","pause"]): return "relationship"
    # money-flow (financial) classes
    if "equity" in s: return "equity"
    if any(k in s for k in ["debt","bond","loan","credit line","credit lines","private credit","private-credit","credit_loss","finance_loss","finance loss","credit facilit"]): return "debt"
    if any(k in s for k in ["compute","cloud","azure","aws","capacity","tpu","xpu","silicon","accelerator","backlog"]): return "compute_commitment"
    if "offtake" in s: return "offtake"
    if "capital expenditure" in s or "capex" in s: return "capex"
    if "acquisition" in s or "acquire" in s: return "acquisition"
    if "merger" in s or "merge" in s: return "merger"
    if "divestiture" in s: return "divestiture"
    if "pac_funding" in s or "pac funding" in s: return "pac_funding"
    if "repayment" in s: return "repayment"
    if any(k in s for k in ["investment","invest","backer","seed","strategic_commitment","strategic commitment","commercial_agreement","tech_build","settlement_pilot","stake"]): return "investment"
    return "other"

# layer split: which edges are real capital/credit/compute FLOWS (the substrate of the formal
# proofs) vs non-economic governance/legal/security/relationship edges (graded overlay context).
FINANCIAL_CLASSES={"equity","debt","compute_commitment","gpu_purchase","backstop","warrant","offtake",
 "exogenous_revenue","ipo_proceeds","capex","revenue_share","equity_method_loss","ip_license",
 "acquisition","merger","divestiture","investment","pac_funding","repayment"}
def layer_of(ic): return "financial" if ic in FINANCIAL_CLASSES else "structural"

NODE_META = {
 "NIST":("standards",False),"Cryptography_Standards":("standards",False),"ANTHROPIC_INVESTORS":("financier",False),
 "David_Sacks":("person",False),"Bitcoin_Strategic_Reserve":("crypto_infra",False),
 "NVIDIA":("chip_vendor",True),"AMD":("chip_vendor",True),"Broadcom":("chip_vendor",True),"Intel":("chip_vendor",True),
 "OpenAI":("ai_lab",False),"Anthropic":("ai_lab",False),"xAI":("ai_lab",False),"Mistral":("ai_lab",False),
 "Microsoft":("hyperscaler",True),"Google":("hyperscaler",True),"Amazon":("hyperscaler",True),"Meta":("hyperscaler",True),
 "Oracle":("hyperscaler",True),"CoreWeave":("neocloud",False),"Nscale":("neocloud",False),"Lambda":("neocloud",False),
 "Crusoe":("neocloud",False),"Nebius":("neocloud",False),"Vantage":("neocloud",False),
 "SpaceX":("space_real_economy",True),"SoftBank":("financier",True),"MGX":("financier",True),"GIC":("financier",True),
 "Blackstone":("private_credit",True),"BlueOwl":("private_credit",True),"PIMCO":("private_credit",True),
 "BlackRock":("private_credit",True),"Apollo":("private_credit",True),"Apollo_Blackstone":("private_credit",True),
 "Aladdin":("financial_infra",False),"GIP":("private_credit",True),"HPS":("private_credit",True),
 "AI_Infrastructure_Partnership":("spv",False),"Aligned_Data_Centers":("ai_infra",False),"IBIT":("crypto_infra",False),
 "JPMorgan":("bank",True),"US_Banks":("bank",True),"Stargate":("spv",False),"Meta_Hyperion_SPV":("spv",False),
 "Disney":("ip_rightsholder",True),"Disney_Studios_Coalition":("ip_rightsholder",True),"Midjourney":("ai_lab",False),
 "Nokia":("telecom",True),"US_Government":("state",True),"MP_Materials":("critical_minerals",True),
 "Defense_Primes":("defense",True),"Apple":("hyperscaler",True),
 # exchanges / crypto firms
 "Binance":("exchange",True),"Coinbase":("exchange",True),"Kraken":("exchange",True),"MtGox":("exchange",False),
 "Ripple":("crypto_infra",True),"SBI":("financier",True),"LBRY":("crypto_firm",False),
 "TornadoCash":("privacy_tool",False),"SamouraiWallet":("privacy_tool",False),"USD1":("stablecoin",False),"HKDA":("stablecoin",False),
 # DLT / crypto-infra
 "Hedera":("dlt",True),"Hashgraph_Association":("dlt",False),"Hiero_LFDT":("dlt",False),"Chainlink":("crypto_infra",True),
 # blockchain ecosystem — protocols (dlt) + dev shops/infra (crypto_infra) + foundations
 "Ethereum":("dlt",False),"Ethereum_Foundation":("dlt",False),"MetaMask":("crypto_infra",False),"Infura":("crypto_infra",False),
 "Linea":("crypto_infra",False),"Mysten_Labs":("crypto_infra",False),"Sui":("dlt",False),"Solana":("dlt",False),
 "QRL":("dlt",False),"QRL_Foundation":("dlt",False),"XRPL":("dlt",False),"XRPLF":("dlt",False),"XRPL_Labs":("crypto_infra",False),
 "Ripple_Prime":("crypto_infra",True),"RLUSD":("stablecoin",False),"Vitalik":("person",False),
 # decentralized storage (DePIN) + stellar + privacy
 "Protocol_Labs":("crypto_infra",False),"IPFS":("crypto_infra",False),"Filecoin":("dlt",False),"Arweave":("dlt",False),
 "Sia":("dlt",False),"Walrus":("crypto_infra",False),"DePIN_Storage":("crypto_infra",False),
 "Stellar":("dlt",False),"Stellar_Development_Foundation":("dlt",False),"Franklin_Templeton":("financier",True),
 "Zano":("privacy_tool",False),"Monero":("privacy_tool",False),"Financial_Privacy":("privacy_tool",False),
 "Salvium":("privacy_tool",False),"Mochimo":("privacy_tool",False),
 # oracles / interop / sidechains / alt-L1s
 "Chainlink_Labs":("crypto_infra",False),"Band_Protocol":("crypto_infra",False),"SEDA":("crypto_infra",False),"Flare":("dlt",False),
 "Axelar":("crypto_infra",False),"Oracle_Interop":("crypto_infra",False),"Cosmos":("dlt",False),"VeChain":("dlt",False),
 "VeChain_Foundation":("dlt",False),"Xahau":("dlt",False),"XRPL_EVM":("dlt",False),
 # omnichain interop + state/institutional collabs
 "LayerZero":("crypto_infra",False),"Wormhole":("crypto_infra",False),"WYST":("stablecoin",False),"Wyoming":("state",True),
 "DTCC":("financial_infra",True),"ICE":("exchange",True),"MAS":("regulator",True),"Citadel_Securities":("financier",True),
 "Securitize":("crypto_infra",True),"Uniswap":("crypto_infra",False),"VanEck":("financier",True),"Hamilton_Lane":("financier",True),
 # crypto-enforcement actors (persons) + bodies
 "Gary_Gensler":("person",False),"William_Hinman":("person",False),"Jay_Clayton":("person",False),"Damian_Williams":("person",False),
 "Caroline_Crenshaw":("person",False),"Elizabeth_Warren":("person",False),"Letitia_James":("person",False),"Rostin_Behnam":("person",False),
 "Paul_Atkins":("person",False),"Hester_Peirce":("person",False),"John_Deaton":("person",False),"Brad_Garlinghouse":("person",False),"Stuart_Alderoty":("person",False),
 "SEC_Crypto_Task_Force":("regulator",False),"NCET":("regulator",False),"Operation_Choke_Point_2":("state",False),"Simpson_Thacher":("other",False),
 # crypto founders / builders (persons) + projects
 "David_Schwartz":("person",False),"Jed_McCaleb":("person",False),"Arthur_Britto":("person",False),"Evan_Cheng":("person",False),"Sam_Blackshear":("person",False),
 "Keonne_Rodriguez":("person",False),"William_L_Hill":("person",False),"Zooko_Wilcox":("person",False),"Jeremy_Kauffman":("person",False),
 "Zcash":("privacy_tool",False),"Electric_Coin_Company":("crypto_infra",False),"Odysee":("crypto_infra",False),
 "SEALCOIN":("crypto_infra",False),"ConsenSys":("crypto_infra",True),"WeCan_Group":("crypto_infra",False),"Canary":("financier",True),
 # PQC / quantum / semiconductor
 "SEALSQ":("pqc_quantum",True),"SEALSQ_Murcia_Hub":("pqc_quantum",False),"ICALPS":("pqc_quantum",True),"EeroQ":("pqc_quantum",False),
 # quantum competitive landscape — public pure-plays (exogenous=public-market revenue) + private builders + research/state
 "IonQ":("pqc_quantum",True),"Rigetti":("pqc_quantum",True),"D_Wave":("pqc_quantum",True),"Quantinuum":("pqc_quantum",True),
 "QuEra":("pqc_quantum",False),"Pasqal":("pqc_quantum",False),"Atom_Computing":("pqc_quantum",False),"IQM":("pqc_quantum",False),
 "Quandela":("pqc_quantum",False),"Alice_Bob":("pqc_quantum",False),"OQC":("pqc_quantum",False),"Xanadu":("pqc_quantum",False),
 "Oxford_Ionics":("pqc_quantum",False),"Vector_Atomic":("pqc_quantum",False),"Origin_Quantum":("pqc_quantum",False),
 "USTC":("research",False),"RIKEN":("research",False),"Fujitsu":("tech",True),"Honeywell":("industrial",True),
 "GlobalFoundries":("semiconductor",True),"Temasek":("financier",True),"QIA":("financier",True),
 "Australia":("state",True),"EU_Quantum_Flagship":("state",False),
 "ColibriTD":("pqc_quantum",False),"Miraex":("pqc_quantum",False),"Kaynes_SemiCon":("semiconductor",True),"SEALKAYNESQ":("pqc_quantum",False),
 "IBM":("tech",True),"LG":("tech",True),"Dell":("tech",True),"ScaleAI":("ai_data",True),
 # telecom + satellite
 "Verizon":("telecom",True),"ATT":("telecom",True),"TMobile":("telecom",True),"DeutscheTelekom":("telecom",True),"US_Telecoms":("telecom",True),
 "Globalstar":("satellite",True),"Telesat":("satellite",True),"AST_SpaceMobile":("satellite",False),"WISeSat":("satellite",False),
 "Swift":("financial_infra",True),
 # finance / markets / asia-gulf bigtech
 "Nomura":("bank",True),"StandardBank":("bank",True),"LSEG":("financial_infra",True),"NSE_India":("financial_infra",True),
 "Jefferies":("bank",True),"SilverLake":("financier",True),"a16z":("financier",True),"UBS_OConnor":("financier",True),
 "AntGroup":("bigtech_asia",True),"ByteDance":("bigtech_asia",True),"TikTok_US":("bigtech_asia",True),
 # regulators / state / intel / threat
 "SEC":("regulator",True),"FDIC":("regulator",True),"SDNY":("regulator",True),"DOJ":("regulator",True),"OFAC":("regulator",True),
 "FinCEN":("regulator",True),"Treasury":("regulator",True),"PBoC":("regulator",True),"Congress":("state",True),
 "Government_of_Gujarat":("state",True),"Spanish_Government_SETT":("state",True),"Georgia_MoJ":("state",True),
 "NSA":("state_intel",True),"FBI":("state_intel",True),"DARPA":("state_intel",True),"NRO":("state_intel",True),"InQTel":("state_intel",True),
 "Palantir":("defense_tech",True),"ANOM":("surveillance",False),"Crypto_Standards":("standards",False),"US_Allied_Military":("defense",True),
 "SaltTyphoon":("threat_actor",False),"Lazarus":("threat_actor",False),"Lazarus_Group":("threat_actor",False),"Boeing":("defense",True),
 # PACs / journalism / offshore
 "Fairshake":("political",False),"ICIJ":("journalism",False),"Offshore_Finance":("offshore",False),
 # statistical agencies / statistics / data-integrity layer
 "BLS":("statistical_agency",True),"BEA":("statistical_agency",True),"Census":("statistical_agency",True),
 "CBO":("statistical_agency",True),"SSA":("statistical_agency",True),"Boskin_Commission":("commission",False),
 "Federal_Reserve":("central_bank",True),"WhiteHouse":("state",True),
 "CPI_Methodology":("statistic",False),"Jobs_Headline":("statistic",False),"PCE":("statistic",False),"QCEW_Benchmark":("statistic",False),
 "CPI_Rent":("statistic",False),"BLS_NTRI":("statistic",False),"ApartmentList_ALNRI":("data_provider",False),"Zillow_ZORI":("data_provider",False),
 # commodities / exchanges / labor
 "COMEX":("exchange",True),"Metals_Futures":("commodity_market",False),"Silver_Physical":("commodity",False),"Copper":("commodity",False),
 "US_Tariff_Policy":("state",True),"Gig_Platforms":("labor_platform",False),"Contingent_Labor":("labor",False),
 "Rate_Shock":("macro_factor",False),
 "PrivateCredit_Funds":("private_credit",True),"AI_Datacenters":("ai_infra",False),"Insurers_Annuities":("insurance",True),"Retail_401k":("retail",False),
 "PE_Insurers":("insurance",True),"Bermuda_Captives":("insurance",False),"Annuity_Holders":("retail",False),
 "Bond_Market_2Y":("macro_factor",False),"Federal_Reserve":("central_bank",True),"Dual_Mandate":("statistic",False),
 "GENIUS_Act":("state",False),"Stablecoins":("stablecoin",False),"Tether":("stablecoin",True),"Circle":("stablecoin",True),"US_Treasuries":("statistic",False),"WorldLibertyFinancial":("stablecoin",False),"Gold":("commodity",False),"China":("state",True),
 # persons / misc
 "CZ":("person",False),"Pertsev":("person",False),"RomanStorm":("person",False),"Trump":("person",False),"VanLoon":("person",False),
 "Netherlands":("state",True),"TechCompanies":("tech",True),"Oklo":("energy",True),"TrailOfBits":("security_research",False),
 "Jefferies":("bank",True),"First_Brands":("industrial",False),"Creditors":("creditor",False),
 # uncovered / out-of-scope risk pools (overlay context; not part of the AI SCC)
 "Money_Market_Funds":("financier",True),"Repo_Market":("financial_infra",True),"Treasury_Market":("financial_infra",True),
 "Hedge_Funds":("financier",True),"Pension_Funds":("financier",True),"PrivateEquity_Funds":("private_credit",True),
 "UK_LDI_Funds":("financier",True),"Life_Insurers":("insurance",True),
 "GSEs_FannieFreddie":("financial_infra",True),"FHLB_System":("financial_infra",True),"Mortgage_Market":("financial_infra",True),
 "Family_Offices":("financier",True),"Prime_Brokers":("bank",True),
 "Mortgage_REITs":("financier",True),"Agency_MBS_Market":("financial_infra",True),"CRE_Market":("financial_infra",True),
 "BaaS_Middleware":("financial_infra",False),"Sponsor_Banks":("bank",True),"Neobanks":("financial_infra",False),
 "Subprime_Auto_ABS":("private_credit",False),"Tricolor_Holdings":("private_credit",False),"BNPL_Phantom_Debt":("private_credit",False),
 "Municipal_Debt":("financial_infra",True),"Federal_Transfers":("state",True),"US_household_credit":("retail",True),
 "Credit_Unions":("bank",True),"ILCs":("bank",True),"Foreign_Bank_US_Branches":("bank",True),
 # digital-ID OS/hardware enforcement layer (overlay)
 "EUDI_Wallet":("standards",False),"Device_Age_Attestation":("surveillance",False),
 "Secure_Element_Vendors":("semiconductor",True),"Alternative_OS_Exclusion":("surveillance",False),
 "UK_Digital_ID":("state",False),"Labour_Together":("political",False),
 # hidden / off-book sovereign debt (overlay)
 "Developing_State_Infrastructure":("state",False),"Distressed_Sovereigns":("state",False),
 "LGFV_Debt":("creditor",False),"US_Contingent_Liabilities":("creditor",False),
 # device-ownership erosion -> OS identity (overlay)
 "Device_Ownership_Erosion":("surveillance",False),"AI_Native_OS":("tech",False),"Age_Assurance_Issuers":("surveillance",False),
 # uncovered-pool deep digs (overlay)
 "Corporate_Credit_Unions":("bank",True),"NCUSIF":("regulator",True),"BDCs":("private_credit",True),
 "Commercial_Parents":("industrial",False),"Farm_Credit_System":("financial_infra",True),"FFCB_Funding":("financial_infra",True),
 "US_Farmland":("commodity",False),"CoBank":("bank",True),"Rural_Infrastructure":("industrial",False),"Japanese_Banks":("bank",True),
 # commodities / energy physical-chokepoint cluster (overlay; deliberately NOT part of the AI SCC)
 "Crude_Oil":("commodity",True),"Antimony":("commodity",True),"Rare_Earths":("commodity",True),
 "Perpetua_Resources":("critical_minerals",False),"United_States_Antimony":("critical_minerals",True),
 "Ucore":("critical_minerals",False),
}

edges=[]
def add(frm,to,instr,amt,status,circ,src,note="",cancelable=False):
    f,t=canon(frm),canon(to)
    if f==t: return
    ic=iclass(instr)
    edges.append({"from":f,"to":t,"instrument":ic,"layer":layer_of(ic),"raw_instrument":instr,
        "amount_usd":amt if isinstance(amt,(int,float)) else None,"status":status or "",
        "declared_circular":bool(circ),"cancelable":bool(cancelable),"source_file":src,"note":note})

for fn in glob.glob(os.path.join(RES,"*.json")):
    try: d=json.load(open(fn))
    except: continue
    base=os.path.basename(fn)
    for e in (d.get("edges") or []):
        add(e.get("from"),e.get("to"),e.get("raw_instrument") or e.get("instrument"),
            e.get("amount_usd"),e.get("status"),e.get("circular"),base,e.get("notes",""),e.get("cancelable"))
    for e in (d.get("chain_edges") or []):
        add(e.get("from"),e.get("to"),e.get("instrument"),e.get("amount_usd"),e.get("date",""),False,base,e.get("notes",""))

# critical-minerals STATE-circularity (parallel structure; deliberately NOT part of the AI SCC)
edges += [
 {"from":"US_Government","to":"MP_Materials","instrument":"equity","raw_instrument":"DoD $400M convertible pref ~15% + $110/kg NdPr price floor + $150M loan","amount_usd":400000000,"status":"closed","declared_circular":True,"cancelable":False,"source_file":"macro-critical-minerals.json","note":"STATE as circular vendor-financier of the supply chain"},
 {"from":"MP_Materials","to":"Defense_Primes","instrument":"offtake","raw_instrument":"10yr 100% DoD offtake -> magnets for missiles/F-35/radar","amount_usd":None,"status":"committed","declared_circular":True,"cancelable":False,"source_file":"macro-critical-minerals.json","note":""},
 {"from":"Apple","to":"MP_Materials","instrument":"offtake","raw_instrument":"$500M recycled-magnet supply deal","amount_usd":500000000,"status":"committed","declared_circular":False,"cancelable":False,"source_file":"macro-critical-minerals.json","note":""},
]

# ensure every edge carries a layer (static minerals edges above are added raw)
for e in edges: e.setdefault("layer",layer_of(e["instrument"]))

# dedupe by (from,to,instrument): keep MAX amount, OR the flags, merge sources
dd={}
for e in edges:
    k=(e["from"],e["to"],e["instrument"])
    if k not in dd: dd[k]=e
    else:
        o=dd[k]
        if (e["amount_usd"] or 0)>(o["amount_usd"] or 0): o["amount_usd"]=e["amount_usd"]; o["raw_instrument"]=e["raw_instrument"]
        o["declared_circular"]=o["declared_circular"] or e["declared_circular"]
        o["cancelable"]=o.get("cancelable") or e.get("cancelable")
        if e["source_file"] not in o["source_file"]: o["source_file"]+=","+e["source_file"]
E=list(dd.values())
nodes=sorted({e["from"] for e in E}|{e["to"] for e in E})

def meta(n):
    if n.startswith("SINK_"): return ("sink",True)
    if n in NODE_META: return NODE_META[n]
    if "Starlink" in n or "SpaceX_IPO" in n: return ("exogenous_source",True)
    return ("other",True)
entities={n:{"sector":meta(n)[0],"has_exogenous_revenue":meta(n)[1]} for n in nodes}

# ---- Tarjan SCC as a function over an edge subset ----
sys.setrecursionlimit(100000)
def scc_core(edge_list):
    adj=defaultdict(list)
    for e in edge_list: adj[e["from"]].append(e["to"])
    idx={};low={};onstk={};stk=[];comps=[];c=[0]
    def sc(v):
        idx[v]=low[v]=c[0];c[0]+=1;stk.append(v);onstk[v]=True
        for w in adj[v]:
            if w not in idx: sc(w);low[v]=min(low[v],low[w])
            elif onstk.get(w): low[v]=min(low[v],idx[w])
        if low[v]==idx[v]:
            comp=[]
            while True:
                w=stk.pop();onstk[w]=False;comp.append(w)
                if w==v:break
            comps.append(comp)
    for v in {e["from"] for e in edge_list}|{e["to"] for e in edge_list}:
        if v not in idx: sc(v)
    sccs=[c2 for c2 in comps if len(c2)>1]; sccs.sort(key=len,reverse=True)
    core=set().union(*sccs) if sccs else set()
    return sccs,core,adj

sccs_all,core_all,adj=scc_core(E)
sccs_robust,core_robust,_=scc_core([e for e in E if not e.get("cancelable")])
# PROOF-INTEGRITY CHECK: the circular core must rest on capital/credit/compute FLOWS, not on
# governance/legal/security relationships. Compute the SCC over financial-layer edges only.
_,core_financial,_=scc_core([e for e in E if e.get("layer")=="financial"])
structural_adds_no_cycle=(core_financial==core_all)

# elementary cycles (bounded) over full graph
cycset=set();cyclist=[]
def dfs(start,v,path,seen):
    if len(path)>8: return
    for w in adj[v]:
        if w==start and len(path)>=2:
            cyc=tuple(path);rot=min(range(len(cyc)),key=lambda i:cyc[i:]+cyc[:i]);key=cyc[rot:]+cyc[:rot]
            if key not in cycset: cycset.add(key);cyclist.append(list(key))
        elif w in core_all and w not in seen: dfs(start,w,path+[w],seen|{w})
for s in core_all: dfs(s,s,[s],{s})
cyclist.sort(key=len)

def amt(e): return e["amount_usd"] or 0
expo={}
for n in nodes:
    tot=sum(amt(e) for e in E if e["from"]==n or e["to"]==n)
    cir=sum(amt(e) for e in E if (e["from"]==n or e["to"]==n) and e["from"] in core_all and e["to"] in core_all)
    expo[n]={"total_usd":tot,"circular_usd":cir,"circularity_ratio":round(cir/tot,3) if tot else 0.0,
             "in_core_scc":n in core_all,"in_robust_core":n in core_robust}

# ---- cross-layer connector analysis: which nodes BRIDGE the most distinct sectors/files ----
nbrs=defaultdict(set); efiles=defaultdict(set); elayers=defaultdict(set); deg=defaultdict(int)
for e in E:
    f,t=e["from"],e["to"]; nbrs[f].add(t); nbrs[t].add(f)
    deg[f]+=1; deg[t]+=1
    for n in (f,t):
        for sf in str(e["source_file"]).split(","): efiles[n].add(sf.strip())
        elayers[n].add(e.get("layer","financial"))
connectors={}
for n in nodes:
    nb_sectors=sorted({entities[x]["sector"] for x in nbrs[n]})
    connectors[n]={"degree":deg[n],"neighbor_sectors":nb_sectors,"n_neighbor_sectors":len(nb_sectors),
        "source_files":len(efiles[n]),"layers":sorted(elayers[n]),"both_layers":len(elayers[n])>1}
# bridge score: distinct neighbor-sectors + distinct source-files + cross-layer bonus
def bscore(n):
    c=connectors[n]; return c["n_neighbor_sectors"]*2+c["source_files"]+(3 if c["both_layers"] else 0)
top_connectors=sorted(nodes,key=bscore,reverse=True)[:18]

nfin=sum(1 for e in E if e.get("layer")=="financial"); nstr=len(E)-nfin

nvda_funded=sum(amt(e) for e in E if e["from"]=="NVIDIA" and e["instrument"] in("equity","backstop","warrant") and e["to"] in core_all and (e["amount_usd"] or 0)<=35e9)
nvda_head=sum(amt(e) for e in E if e["from"]=="NVIDIA" and e["instrument"] in("equity","backstop","warrant") and e["to"] in core_all)
nvda_rev=215.9e9
selffund={"funded_usd":nvda_funded,"headline_usd":nvda_head,"nvidia_fy26_revenue_usd":nvda_rev,
          "funded_ratio":round(nvda_funded/nvda_rev,3),"headline_ratio":round(nvda_head/nvda_rev,3)}

graph={"entities":entities,"edges":E,"analysis":{
    "num_nodes":len(nodes),"num_edges":len(E),
    "num_financial_edges":nfin,"num_structural_edges":nstr,
    "core_scc_all":sorted(core_all),"core_scc_all_size":len(core_all),
    "core_scc_robust_excl_cancelable":sorted(core_robust),"core_scc_robust_size":len(core_robust),
    "core_scc_financial_only":sorted(core_financial),"structural_edges_add_no_cycle":structural_adds_no_cycle,
    "nodes_only_circular_via_cancelable":sorted(core_all-core_robust),
    "num_elementary_cycles":len(cyclist),"elementary_cycles":cyclist,
    "circularity_exposure":expo,"nvidia_self_funding":selffund,
    "top_cross_layer_connectors":[{"node":n,**connectors[n]} for n in top_connectors]}}
json.dump(graph,open(os.path.join(DATA,"graph.json"),"w"),indent=2)
with open(os.path.join(DATA,"edges.csv"),"w",newline="") as f:
    w=csv.writer(f);w.writerow(["from","to","instrument","amount_usd","status","declared_circular","cancelable","source_file"])
    for e in sorted(E,key=lambda x:-(x["amount_usd"] or 0)):
        w.writerow([e["from"],e["to"],e["instrument"],e["amount_usd"],e["status"],e["declared_circular"],e["cancelable"],e["source_file"]])
with open(os.path.join(DATA,"entities.csv"),"w",newline="") as f:
    w=csv.writer(f);w.writerow(["node","sector","has_exogenous_revenue","in_core_scc","in_robust_core","circularity_ratio"])
    for n in nodes: w.writerow([n,entities[n]["sector"],entities[n]["has_exogenous_revenue"],expo[n]["in_core_scc"],expo[n]["in_robust_core"],expo[n]["circularity_ratio"]])

print("="*74+"\nSTRUCTURAL FORMAL ANALYSIS  -  AI circular-funding graph\n"+"="*74)
print(f"nodes={len(nodes)}  edges={len(E)}  (financial={nfin}, structural={nstr})")
print(f"\n[S0] PROOF-INTEGRITY: SCC over FINANCIAL-layer edges only == SCC over all edges? {structural_adds_no_cycle}")
print(f"     => the circular core rests on capital/credit/compute flows; governance/legal/security edges add no cycle.")
print(f"\n[S1] Core SCC (ALL edges): |SCC|={len(core_all)}")
print("     "+", ".join(sorted(core_all)))
print(f"\n[S1b] Core SCC (EXCLUDING cancelable contracts): |SCC|={len(core_robust)}")
print("     "+", ".join(sorted(core_robust)))
print(f"\n[S1c] Nodes circular ONLY via CANCELABLE edges: {sorted(core_all-core_robust)}")
print("      => These are conditionally entangled; their circularity can be unwound by contract termination.")
print(f"\n[S2] Elementary directed cycles (len<=8): {len(cyclist)}.  Shortest:")
for c in cyclist[:12]: print("    "+" -> ".join(c)+" -> "+c[0])
print(f"\n[METRIC] Circularity exposure (core nodes):")
for n in sorted(core_all,key=lambda x:-expo[x]["circularity_ratio"]):
    tag="" if n in core_robust else "  <-- cancelable-only"
    print(f"    {n:<16} ratio={expo[n]['circularity_ratio']:.2f}  circ=${expo[n]['circular_usd']/1e9:,.0f}B{tag}")
print(f"\n[METRIC] SpaceX vs core:")
for n in ["SpaceX","NVIDIA","OpenAI","CoreWeave","Oracle"]:
    if n in expo: print(f"    {n:<10} in_core_all={expo[n]['in_core_scc']}  in_robust_core(excl-cancelable)={expo[n]['in_robust_core']}  exo_rev={entities[n]['has_exogenous_revenue']}")
print(f"\n[METRIC] NVIDIA vendor-financing self-funding ratio:")
print(f"    funded-only  ${selffund['funded_usd']/1e9:,.0f}B / ${nvda_rev/1e9:,.0f}B = {selffund['funded_ratio']:.1%}")
print(f"    headline     ${selffund['headline_usd']/1e9:,.0f}B / ${nvda_rev/1e9:,.0f}B = {selffund['headline_ratio']:.1%}")
print(f"\n[METRIC] Top cross-layer connectors (bridge distinct sectors/files/layers):")
for n in top_connectors[:12]:
    c=connectors[n]; lyr="F+S" if c["both_layers"] else (c["layers"][0][0].upper() if c["layers"] else "-")
    print(f"    {n:<20} deg={c['degree']:<3} sectors={c['n_neighbor_sectors']:<2} files={c['source_files']:<2} layers={lyr}  [{', '.join(c['neighbor_sectors'][:6])}]")
print("\nwrote data/graph.json, data/edges.csv, data/entities.csv")
