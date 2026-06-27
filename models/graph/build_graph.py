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
 # 2022 collapse cluster — persons
 "SBF":"Sam_Bankman_Fried","Sam Bankman-Fried":"Sam_Bankman_Fried","Sam Bankman Fried":"Sam_Bankman_Fried","Sam_Bankman_Fried":"Sam_Bankman_Fried",
 "Caroline Ellison":"Caroline_Ellison","Caroline_Ellison":"Caroline_Ellison","Do Kwon":"Do_Kwon","Do_Kwon":"Do_Kwon","DoKwon":"Do_Kwon",
 "Alex Mashinsky":"Alex_Mashinsky","Mashinsky":"Alex_Mashinsky","Alex_Mashinsky":"Alex_Mashinsky","Barry Silbert":"Barry_Silbert","Barry_Silbert":"Barry_Silbert",
 "Su Zhu":"Su_Zhu","Su_Zhu":"Su_Zhu","Kyle Davies":"Kyle_Davies","Kyle_Davies":"Kyle_Davies","Brian Armstrong":"Brian_Armstrong","Brian_Armstrong":"Brian_Armstrong",
 "Winklevoss":"Winklevoss_Twins","Winklevoss Twins":"Winklevoss_Twins","Winklevoss_Twins":"Winklevoss_Twins","Justin Sun":"Justin_Sun","Justin_Sun":"Justin_Sun","Arthur Hayes":"Arthur_Hayes","Arthur_Hayes":"Arthur_Hayes",
 # 2022 collapse cluster — firms
 "Alameda":"Alameda_Research","Alameda Research":"Alameda_Research","Alameda_Research":"Alameda_Research","Celsius":"Celsius","Voyager":"Voyager","BlockFi":"BlockFi",
 "Genesis":"Genesis","DCG":"DCG","Digital Currency Group":"DCG","Grayscale":"Grayscale","Gemini":"Gemini","Gemini Earn":"Gemini_Earn","Gemini_Earn":"Gemini_Earn",
 "Tron":"Tron","TRX":"Tron","BitMEX":"BitMEX","3AC":"Three_Arrows_Capital","Three Arrows Capital":"Three_Arrows_Capital",
 # crypto market-makers + political money
 "Jump Crypto":"Jump_Crypto","Jump Trading":"Jump_Crypto","Jump":"Jump_Crypto","Jump_Crypto":"Jump_Crypto","Tai Mo Shan":"Tai_Mo_Shan","Tai_Mo_Shan":"Tai_Mo_Shan",
 "Jane Street":"Jane_Street","Jane_Street":"Jane_Street","Wintermute":"Wintermute","Cumberland":"Cumberland_DRW","Cumberland DRW":"Cumberland_DRW","Cumberland_DRW":"Cumberland_DRW","DRW":"Cumberland_DRW",
 "GSR":"GSR","Crypto_Market_Makers":"Crypto_Market_Makers","Kanav Kariya":"Kanav_Kariya","Kanav_Kariya":"Kanav_Kariya",
 # semiconductor supply chain
 "ASML":"ASML","Carl Zeiss SMT":"ZEISS_SMT","Zeiss SMT":"ZEISS_SMT","ZEISS":"ZEISS_SMT","Zeiss":"ZEISS_SMT","ZEISS_SMT":"ZEISS_SMT","Cymer":"Cymer",
 "TSMC":"TSMC","TSM":"TSMC","Samsung Foundry":"Samsung_Foundry","Samsung":"Samsung_Foundry","Samsung_Foundry":"Samsung_Foundry","SMIC":"SMIC","Nikon":"Nikon","Canon":"Canon",
 "Applied Materials":"Applied_Materials","AMAT":"Applied_Materials","Applied_Materials":"Applied_Materials","Lam Research":"Lam_Research","Lam_Research":"Lam_Research","Tokyo Electron":"Tokyo_Electron","TEL":"Tokyo_Electron","Tokyo_Electron":"Tokyo_Electron","KLA":"KLA",
 "Semiconductor_Equipment":"Semiconductor_Equipment","Shin-Etsu":"Shin_Etsu","Shin Etsu":"Shin_Etsu","Shin_Etsu":"Shin_Etsu","SUMCO":"SUMCO","JSR":"JSR","Tokyo Ohka":"Tokyo_Ohka","TOK":"Tokyo_Ohka","Tokyo_Ohka":"Tokyo_Ohka","Semiconductor_Materials":"Semiconductor_Materials",
 "Synopsys":"Synopsys","Cadence":"Cadence","Siemens EDA":"Siemens_EDA","Siemens_EDA":"Siemens_EDA","Mentor":"Siemens_EDA","Arm":"Arm","ARM":"Arm","EDA_Tools":"EDA_Tools",
 "CoWoS":"CoWoS","ASE":"ASE","Amkor":"Amkor","JCET":"JCET","OSAT":"OSAT","SK Hynix":"SK_Hynix","SK_Hynix":"SK_Hynix","Hynix":"SK_Hynix","Micron":"Micron","HBM":"HBM",
 # logistics / shipping
 "Maersk":"Maersk","MSC":"MSC","CMA CGM":"CMA_CGM","CMA_CGM":"CMA_CGM","Hapag-Lloyd":"Hapag_Lloyd","Hapag Lloyd":"Hapag_Lloyd","Hapag_Lloyd":"Hapag_Lloyd","COSCO":"COSCO","Ocean_Shipping":"Ocean_Shipping",
 "DHL":"DHL","Kuehne+Nagel":"Kuehne_Nagel","Kuehne Nagel":"Kuehne_Nagel","Kuehne_Nagel":"Kuehne_Nagel","DSV":"DSV","FedEx":"FedEx","UPS":"UPS","Logistics_3PL":"Logistics_3PL",
 "Suez Canal":"Suez_Canal","Suez_Canal":"Suez_Canal","Panama Canal":"Panama_Canal","Panama_Canal":"Panama_Canal","Strait of Malacca":"Strait_of_Malacca","Strait_of_Malacca":"Strait_of_Malacca","Strait of Hormuz":"Strait_of_Hormuz","Strait_of_Hormuz":"Strait_of_Hormuz","Taiwan Strait":"Taiwan_Strait","Taiwan_Strait":"Taiwan_Strait","Shipping_Chokepoints":"Shipping_Chokepoints",
 # standards bodies
 "ISO":"ISO","IEC":"IEC","ISO/IEC JTC1":"ISO_IEC_JTC1","ISO IEC JTC1":"ISO_IEC_JTC1","ISO_IEC_JTC1":"ISO_IEC_JTC1","SC 42":"SC42_AI","SC42":"SC42_AI","SC42_AI":"SC42_AI","SC 27":"SC27_Security","SC27":"SC27_Security","SC27_Security":"SC27_Security",
 "IEEE":"IEEE","ITU":"ITU","ETSI":"ETSI","3GPP":"3GPP","SEMI":"SEMI","JEDEC":"JEDEC","ANSI":"ANSI","BIPM":"BIPM","Codex Alimentarius":"Codex_Alimentarius","Codex_Alimentarius":"Codex_Alimentarius","Standards_Bodies":"Standards_Bodies",
 "GHTF":"GHTF","IMDRF":"IMDRF","ISO 13485":"ISO_13485","ISO_13485":"ISO_13485","ISO 14971":"ISO_14971","ISO_14971":"ISO_14971","Medical_Device_Standards":"Medical_Device_Standards",
 # East Asia — conglomerates + politics + social-harm
 "South Korea":"South_Korea","South_Korea":"South_Korea","Japan":"Japan","South Africa":"South_Africa","South_Africa":"South_Africa",
 "Chaebol":"Chaebol","Samsung Group":"Samsung_Group","Samsung_Group":"Samsung_Group","Hyundai":"Hyundai","SK Group":"SK_Group","SK_Group":"SK_Group","Lotte":"Lotte","Hanwha":"Hanwha","Lee Family":"Lee_Family","Lee_Family":"Lee_Family",
 "Zaibatsu":"Zaibatsu_Keiretsu","Keiretsu":"Zaibatsu_Keiretsu","Zaibatsu_Keiretsu":"Zaibatsu_Keiretsu","Mitsubishi":"Mitsubishi","Mitsui":"Mitsui","Sumitomo":"Sumitomo",
 "LDP":"LDP","Liberal Democratic Party":"LDP","Komeito":"Komeito","Soka Gakkai":"Soka_Gakkai","Soka_Gakkai":"Soka_Gakkai","Unification Church":"Unification_Church","Unification_Church":"Unification_Church","CDP":"CDP_Japan","CDP_Japan":"CDP_Japan",
 "Shinzo Abe":"Shinzo_Abe","Shinzo_Abe":"Shinzo_Abe","Shigeru Ishiba":"Shigeru_Ishiba","Shigeru_Ishiba":"Shigeru_Ishiba",
 "People Power Party":"People_Power_Party","People_Power_Party":"People_Power_Party","Democratic Party Korea":"Democratic_Party_Korea","Democratic_Party_Korea":"Democratic_Party_Korea","Yoon Suk Yeol":"Yoon_Suk_yeol","Yoon Suk-yeol":"Yoon_Suk_yeol","Yoon_Suk_yeol":"Yoon_Suk_yeol","Lee Jae-myung":"Lee_Jae_myung","Lee Jae myung":"Lee_Jae_myung","Lee_Jae_myung":"Lee_Jae_myung",
 "Apartheid_Honorary_Whites":"Apartheid_Honorary_Whites","Kabukicho":"Kabukicho","Toyoko Kids":"Toyoko_Kids","Toyoko_Kids":"Toyoko_Kids","Host Club Debt":"Host_Club_Debt","Host_Club_Debt":"Host_Club_Debt","Japan_Sex_Industry":"Japan_Sex_Industry",
 # China AI stack + censorship
 "DeepSeek":"DeepSeek","Alibaba":"Alibaba","Qwen":"Alibaba","Baidu":"Baidu","Ernie":"Baidu","Tencent":"Tencent","Xiaomi":"Xiaomi","iFlytek":"iFlytek",
 "Zhipu":"Zhipu_AI","Zhipu AI":"Zhipu_AI","Zhipu_AI":"Zhipu_AI","GLM":"Zhipu_AI","Moonshot":"Moonshot","Kimi":"Moonshot","MiniMax":"MiniMax","StepFun":"StepFun","01.AI":"01_AI","01_AI":"01_AI","Yi":"01_AI","Baichuan":"Baichuan",
 "Huawei":"Huawei","Ascend":"Huawei","Cambricon":"Cambricon","Biren":"Biren","Moore Threads":"Moore_Threads","Moore_Threads":"Moore_Threads",
 "CAC":"CAC","Cyberspace Administration of China":"CAC","MIIT":"MIIT","China_AI_Labs":"China_AI_Labs","China_AI_Hardware":"China_AI_Hardware","China_AI_Censorship":"China_AI_Censorship",
 # local / uncensored / decentralized AI
 "llama.cpp":"llama_cpp","llama_cpp":"llama_cpp","Ollama":"Ollama","vLLM":"vLLM","LM Studio":"LM_Studio","LM_Studio":"LM_Studio","GPT4All":"GPT4All","Jan":"Jan","ComfyUI":"ComfyUI",
 "Stability AI":"Stability_AI","Stability_AI":"Stability_AI","Stable Diffusion":"Stability_AI","Black Forest Labs":"Black_Forest_Labs","Black_Forest_Labs":"Black_Forest_Labs","Flux":"Black_Forest_Labs","Hugging Face":"Hugging_Face","HuggingFace":"Hugging_Face","Hugging_Face":"Hugging_Face",
 "EleutherAI":"EleutherAI","Nous Research":"Nous_Research","Nous_Research":"Nous_Research","AllenAI":"AllenAI_OLMo","OLMo":"AllenAI_OLMo","AllenAI_OLMo":"AllenAI_OLMo",
 "Heretic":"Heretic","Dolphin":"Dolphin","Eric Hartford":"Eric_Hartford","Eric_Hartford":"Eric_Hartford",
 "Bittensor":"Bittensor","TAO":"Bittensor","Akash":"Akash","Render":"Render","Octra":"Octra","Venice":"Venice_AI","Venice.ai":"Venice_AI","Venice_AI":"Venice_AI","Erik Voorhees":"Erik_Voorhees","Erik_Voorhees":"Erik_Voorhees","FUTO":"FUTO",
 "Local_AI_Tooling":"Local_AI_Tooling","Uncensored_AI":"Uncensored_AI","Decentralized_AI":"Decentralized_AI","Open_Local_AI":"Open_Local_AI",
 "Fhenix":"Fhenix","FHEnix":"Fhenix","Biconomy":"Biconomy","TapBit":"TapBit",
 # surveillance & cyber-threat layer
 "VoltTyphoon":"VoltTyphoon","Volt Typhoon":"VoltTyphoon","Salt Typhoon":"SaltTyphoon","MSS":"MSS","APT28":"APT28_FancyBear","Fancy Bear":"APT28_FancyBear","APT28_FancyBear":"APT28_FancyBear","APT29":"APT29_CozyBear","Cozy Bear":"APT29_CozyBear","APT29_CozyBear":"APT29_CozyBear","Sandworm":"Sandworm","Kimsuky":"Kimsuky","Equation Group":"Equation_Group","Equation_Group":"Equation_Group",
 "Unit 8200":"Unit_8200","Unit_8200":"Unit_8200","North Korea":"North_Korea","North_Korea":"North_Korea","Israel":"Israel","APT_State_Actors":"APT_State_Actors","CALEA_Backdoor":"CALEA_Backdoor","Viasat":"Viasat",
 "NSO Group":"NSO_Group","NSO_Group":"NSO_Group","Pegasus":"Pegasus","Intellexa":"Intellexa","Cytrox":"Cytrox","Predator":"Predator","Paragon":"Paragon","Cellebrite":"Cellebrite","Commercial_Spyware":"Commercial_Spyware",
 "LockBit":"LockBit","ALPHV":"ALPHV_BlackCat","BlackCat":"ALPHV_BlackCat","ALPHV_BlackCat":"ALPHV_BlackCat","Scattered Spider":"Scattered_Spider","Scattered_Spider":"Scattered_Spider","Cl0p":"Cl0p","Clop":"Cl0p","Ransomware_RaaS":"Ransomware_RaaS",
 "Clearview":"Clearview_AI","Clearview AI":"Clearview_AI","Clearview_AI":"Clearview_AI","Anduril":"Anduril","ImmigrationOS":"ImmigrationOS","ICE":"ICE","Private_Surveillance":"Private_Surveillance",
 "CrowdStrike":"CrowdStrike","Mandiant":"Mandiant","Recorded Future":"Recorded_Future","Recorded_Future":"Recorded_Future","Cyber_Defense":"Cyber_Defense",
 # SE Asia scam/crime nexus
 "SE_Asia_Scam_Complex":"SE_Asia_Scam_Complex","Chen Zhi":"Chen_Zhi","Chen_Zhi":"Chen_Zhi","KK Park":"KK_Park","KK_Park":"KK_Park","Qingsong Park":"Qingsong_Park","Qingsong_Park":"Qingsong_Park","Thai Hoa Garden":"Qingsong_Park",
 "Zhao Wei":"Zhao_Wei","Zhao_Wei":"Zhao_Wei","Kings Romans":"Kings_Romans","Kings_Romans":"Kings_Romans","Golden Triangle SEZ":"Golden_Triangle_SEZ","Golden_Triangle_SEZ":"Golden_Triangle_SEZ","GTSEZ":"Golden_Triangle_SEZ",
 "POGO":"POGO","POGOs":"POGO","Tudou Guarantee":"Tudou_Guarantee","Tudou_Guarantee":"Tudou_Guarantee","Tudou":"Tudou_Guarantee","Starlink":"Starlink",
 "Myanmar":"Myanmar","Laos":"Laos","Philippines":"Philippines","Thailand":"Thailand",
 # Russia state network
 "Putin":"Putin","Vladimir Putin":"Putin","Siloviki":"Siloviki","Silovik":"Siloviki","Gazprom":"Gazprom","Rosneft":"Rosneft","Igor Sechin":"Igor_Sechin","Sechin":"Igor_Sechin","Igor_Sechin":"Igor_Sechin",
 "Shadow_Fleet":"Shadow_Fleet","Shadow Fleet":"Shadow_Fleet","Wagner":"Wagner","Wagner Group":"Wagner","Africa Corps":"Africa_Corps","Africa_Corps":"Africa_Corps",
 "FSB":"FSB","GRU":"GRU","SVR":"SVR","Russian_Intel":"Russian_Intel","Bortnikov":"Bortnikov","Kostyukov":"Kostyukov","Naryshkin":"Naryshkin","Sberbank":"Sberbank","Ukraine":"Ukraine",
 # Ukraine war economy
 "Zelensky":"Zelensky","Zelenskyy":"Zelensky","Volodymyr Zelensky":"Zelensky","Ukraine_Minerals":"Ukraine_Minerals","US_Ukraine_Reconstruction_Fund":"US_Ukraine_Reconstruction_Fund","Reconstruction Investment Fund":"US_Ukraine_Reconstruction_Fund",
 "Western_Aid_Ukraine":"Western_Aid_Ukraine","EU":"EU","European Union":"EU","Ukraine_Drone_Industry":"Ukraine_Drone_Industry","Brave1":"Brave1","Energoatom":"Energoatom",
 "NABU":"NABU","Operation Midas":"Operation_Midas","Operation_Midas":"Operation_Midas","Mindich":"Mindich","Timur Mindich":"Mindich","Halushchenko":"Halushchenko",
 # Iran state network
 "Iran":"Iran","Khamenei":"Khamenei","IRGC":"IRGC","Bonyads":"Bonyads","Bonyad":"Bonyads","Iran_Oil":"Iran_Oil","Chinese_Teapots":"Chinese_Teapots","Teapot Refineries":"Chinese_Teapots",
 "Axis_of_Resistance":"Axis_of_Resistance","Axis of Resistance":"Axis_of_Resistance","Hezbollah":"Hezbollah","Hamas":"Hamas","Houthis":"Houthis","Syria":"Syria","Iran_Nuclear_Program":"Iran_Nuclear_Program","IAEA":"IAEA",
 # China party-state
 "CCP":"CCP","Chinese Communist Party":"CCP","Xi":"Xi","Xi Jinping":"Xi","Politburo Standing Committee":"Politburo_Standing_Committee","Politburo_Standing_Committee":"Politburo_Standing_Committee","PSC":"Politburo_Standing_Committee","Fourth Plenum":"Fourth_Plenum","Fourth_Plenum":"Fourth_Plenum",
 "CMC":"CMC","Central Military Commission":"CMC","PLA":"PLA","State Council":"State_Council","State_Council":"State_Council","15th Five Year Plan":"15th_Five_Year_Plan","15th_Five_Year_Plan":"15th_Five_Year_Plan","15th FYP":"15th_Five_Year_Plan",
 "SASAC":"SASAC","Central SOEs":"Central_SOEs","Central_SOEs":"Central_SOEs","Military-Civil Fusion":"Military_Civil_Fusion","Military_Civil_Fusion":"Military_Civil_Fusion","MCF":"Military_Civil_Fusion",
 "Provincial Governments":"Provincial_Governments","Provincial_Governments":"Provincial_Governments","Ant Group":"Ant_Group","Ant_Group":"Ant_Group","DiDi":"DiDi","Didi":"DiDi","China_Tech_Crackdown":"China_Tech_Crackdown",
 # Australia
 "Albanese":"Albanese","Anthony Albanese":"Albanese","AUKUS":"AUKUS","UK":"UK","United Kingdom":"UK","SSN_AUKUS":"SSN_AUKUS","SSN-AUKUS":"SSN_AUKUS","US_Australia_Minerals_Framework":"US_Australia_Minerals_Framework",
 "Critical_Minerals_Strategic_Reserve":"Critical_Minerals_Strategic_Reserve","Lynas":"Lynas","BHP":"BHP","Rio Tinto":"Rio_Tinto","Rio_Tinto":"Rio_Tinto","Fortescue":"Fortescue","Superannuation_Funds":"Superannuation_Funds","Superannuation":"Superannuation_Funds",
 # India
 "India":"India","Modi":"Modi","Narendra Modi":"Modi","BJP":"BJP","Adani_Group":"Adani_Group","Adani":"Adani_Group","Gautam Adani":"Gautam_Adani","Gautam_Adani":"Gautam_Adani","Reliance":"Reliance","Ambani":"Ambani","Mukesh Ambani":"Ambani",
 "UPI":"UPI","Aadhaar":"Aadhaar","India_DPI":"India_DPI","BRICS":"BRICS","Quad":"Quad","IMEC":"IMEC",
 # BRICS+ / de-dollarization
 "Brazil":"Brazil","Egypt":"Egypt","Ethiopia":"Ethiopia","UAE":"UAE","United Arab Emirates":"UAE","Indonesia":"Indonesia","Saudi_Arabia":"Saudi_Arabia","Saudi Arabia":"Saudi_Arabia","BRICS_Partners":"BRICS_Partners",
 "NDB":"NDB","New Development Bank":"NDB","BRICS_Pay":"BRICS_Pay","BRICS Pay":"BRICS_Pay","BRICS_Unit":"BRICS_Unit","BRICS Unit":"BRICS_Unit","De_Dollarization":"De_Dollarization","De-Dollarization":"De_Dollarization",
 # CLARITY Act fight
 "CLARITY_Act":"CLARITY_Act","CLARITY Act":"CLARITY_Act","Digital Asset Market Clarity Act":"CLARITY_Act","Catholic_Coalition":"Catholic_Coalition","Law_Enforcement_Coalition":"Law_Enforcement_Coalition","Crypto_AML_Gap":"Crypto_AML_Gap",
 # opioid crisis
 "Opioid_Crisis":"Opioid_Crisis","Purdue_Pharma":"Purdue_Pharma","Purdue":"Purdue_Pharma","Sackler_Family":"Sackler_Family","Sacklers":"Sackler_Family","Big_Three_Distributors":"Big_Three_Distributors","JNJ":"JNJ","Johnson & Johnson":"JNJ","J&J":"JNJ",
 "Pharmacies":"Pharmacies","Fentanyl":"Fentanyl","SCOTUS":"SCOTUS","Supreme Court":"SCOTUS","State_AGs":"State_AGs",
 # defense primes + QRL patent
 "Lockheed_Martin":"Lockheed_Martin","Lockheed Martin":"Lockheed_Martin","LMT":"Lockheed_Martin","RTX":"RTX","Raytheon":"Raytheon","Leonardo":"Leonardo","Leonardo S.p.A.":"Leonardo","Finmeccanica":"Leonardo","Leonardo_DRS":"Leonardo_DRS","Leonardo DRS":"Leonardo_DRS",
 "MEF":"MEF","FOCI_Proxy":"FOCI_Proxy","ELSAG":"ELSAG","AgustaWestland_Scandal":"AgustaWestland_Scandal","QRL_XMSS_Patent":"QRL_XMSS_Patent",
 # 3D-stacking scaling race
 "IBM_Nanostack":"IBM_Nanostack","Nanostack":"IBM_Nanostack","Huawei_Tau_Scaling":"Huawei_Tau_Scaling","Tau Scaling":"Huawei_Tau_Scaling","LogicFolding":"Huawei_Tau_Scaling","CFET":"CFET","IMEC":"IMEC",
 # PFAS forever chemicals
 "PFAS":"PFAS","3M":"3M","DuPont":"DuPont","Chemours":"Chemours","Corteva":"Corteva","AFFF_MDL":"AFFF_MDL","EPA":"EPA","EPA_PFAS_Rule":"EPA_PFAS_Rule","Public_Water_Systems":"Public_Water_Systems","PFAS_Suppression":"PFAS_Suppression",
 # J&J talc / Texas two-step / liability engineering
 "Talc_Litigation":"Talc_Litigation","LTL_Red_River":"LTL_Red_River","Texas_Two_Step":"Texas_Two_Step","Divisive_Merger":"Divisive_Merger","Bankruptcy_Courts":"Bankruptcy_Courts","Liability_Engineering":"Liability_Engineering",
 # asbestos mass tort
 "Asbestos":"Asbestos","Asbestos_Trusts":"Asbestos_Trusts","Johns_Manville":"Johns_Manville","Johns-Manville":"Johns_Manville","Mesothelioma_Claims":"Mesothelioma_Claims","EPA_Asbestos_Ban":"EPA_Asbestos_Ban","Asbestos_Trust_Transparency":"Asbestos_Trust_Transparency",
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
 # right-to-repair umbrella (overlay)
 "Right_to_Repair":"Right_to_Repair","Right to Repair":"Right_to_Repair","R2R":"Right_to_Repair",
 "FULU_Foundation":"FULU_Foundation","FULU":"FULU_Foundation","Louis_Rossmann":"Louis_Rossmann","Louis Rossmann":"Louis_Rossmann","Rossmann":"Louis_Rossmann",
 "Consumer_Rights_Wiki":"Consumer_Rights_Wiki","Consumer Rights Wiki":"Consumer_Rights_Wiki","iFixit":"iFixit",
 "DMCA_1201":"DMCA_1201","DMCA §1201":"DMCA_1201","Section_1201":"DMCA_1201","Copyright_Office":"Copyright_Office","US Copyright Office":"Copyright_Office",
 "State_R2R_Laws":"State_R2R_Laws","EU_R2R_Directive":"EU_R2R_Directive","Parts_Pairing":"Parts_Pairing","Parts-Pairing":"Parts_Pairing","R2R_Opposition":"R2R_Opposition",
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
 # 2022 collapse cluster — persons + firms
 "Sam_Bankman_Fried":("person",False),"Caroline_Ellison":("person",False),"Do_Kwon":("person",False),"Alex_Mashinsky":("person",False),
 "Barry_Silbert":("person",False),"Su_Zhu":("person",False),"Kyle_Davies":("person",False),"Brian_Armstrong":("person",False),
 "Winklevoss_Twins":("person",False),"Justin_Sun":("person",False),"Arthur_Hayes":("person",False),
 "Alameda_Research":("crypto_firm",False),"Celsius":("crypto_firm",False),"Voyager":("crypto_firm",False),"BlockFi":("crypto_firm",False),
 "Genesis":("crypto_firm",False),"DCG":("financier",False),"Grayscale":("financier",True),"Gemini":("exchange",True),"Gemini_Earn":("crypto_firm",False),
 "Tron":("dlt",False),"BitMEX":("exchange",True),
 # crypto market-makers + political money
 "Jump_Crypto":("financier",True),"Tai_Mo_Shan":("financier",False),"Jane_Street":("financier",True),"Wintermute":("financier",True),
 "Cumberland_DRW":("financier",True),"GSR":("financier",True),"Crypto_Market_Makers":("financier",False),"Kanav_Kariya":("person",False),
 # semiconductor supply chain (sector 'semiconductor' -> AI bucket)
 "ASML":("semiconductor",True),"ZEISS_SMT":("semiconductor",False),"Cymer":("semiconductor",False),"TSMC":("semiconductor",True),"Samsung_Foundry":("semiconductor",True),"SMIC":("semiconductor",True),
 "Nikon":("semiconductor",True),"Canon":("semiconductor",True),"Applied_Materials":("semiconductor",True),"Lam_Research":("semiconductor",True),"Tokyo_Electron":("semiconductor",True),"KLA":("semiconductor",True),"Semiconductor_Equipment":("semiconductor",False),
 "Shin_Etsu":("semiconductor",True),"SUMCO":("semiconductor",True),"JSR":("semiconductor",True),"Tokyo_Ohka":("semiconductor",True),"Semiconductor_Materials":("semiconductor",False),
 "Synopsys":("semiconductor",True),"Cadence":("semiconductor",True),"Siemens_EDA":("semiconductor",True),"Arm":("semiconductor",True),"EDA_Tools":("semiconductor",False),
 "CoWoS":("semiconductor",False),"ASE":("semiconductor",True),"Amkor":("semiconductor",True),"JCET":("semiconductor",True),"OSAT":("semiconductor",False),"SK_Hynix":("semiconductor",True),"Micron":("semiconductor",True),"HBM":("semiconductor",False),
 # logistics / shipping (sector 'logistics' -> commodity bucket)
 "Maersk":("logistics",True),"MSC":("logistics",True),"CMA_CGM":("logistics",True),"Hapag_Lloyd":("logistics",True),"COSCO":("logistics",True),"Ocean_Shipping":("logistics",False),
 "DHL":("logistics",True),"Kuehne_Nagel":("logistics",True),"DSV":("logistics",True),"FedEx":("logistics",True),"UPS":("logistics",True),"Logistics_3PL":("logistics",False),
 "Suez_Canal":("logistics",False),"Panama_Canal":("logistics",False),"Strait_of_Malacca":("logistics",False),"Strait_of_Hormuz":("logistics",False),"Taiwan_Strait":("logistics",False),"Shipping_Chokepoints":("logistics",False),
 # standards bodies (sector 'standards' -> identity bucket)
 "ISO":("standards",False),"IEC":("standards",False),"ISO_IEC_JTC1":("standards",False),"SC42_AI":("standards",False),"SC27_Security":("standards",False),
 "IEEE":("standards",False),"ITU":("standards",False),"ETSI":("standards",False),"3GPP":("standards",False),"SEMI":("standards",False),"JEDEC":("standards",False),"ANSI":("standards",False),"BIPM":("standards",False),"Codex_Alimentarius":("standards",False),"Standards_Bodies":("standards",False),
 "GHTF":("standards",False),"IMDRF":("standards",False),"ISO_13485":("standards",False),"ISO_14971":("standards",False),"Medical_Device_Standards":("standards",False),
 # East Asia — conglomerates + politics + social-harm
 "South_Korea":("state",True),"Japan":("state",True),"South_Africa":("state",True),
 "Chaebol":("industrial",False),"Samsung_Group":("industrial",True),"Hyundai":("industrial",True),"SK_Group":("industrial",True),"Lotte":("industrial",True),"Hanwha":("industrial",True),"Lee_Family":("person",False),
 "Zaibatsu_Keiretsu":("industrial",False),"Mitsubishi":("industrial",True),"Mitsui":("industrial",True),"Sumitomo":("industrial",True),
 "LDP":("political",False),"Komeito":("political",False),"Soka_Gakkai":("political",False),"Unification_Church":("political",False),"CDP_Japan":("political",False),"Shinzo_Abe":("person",False),"Shigeru_Ishiba":("person",False),
 "People_Power_Party":("political",False),"Democratic_Party_Korea":("political",False),"Yoon_Suk_yeol":("person",False),"Lee_Jae_myung":("person",False),
 "Apartheid_Honorary_Whites":("state",False),"Kabukicho":("other",False),"Toyoko_Kids":("other",False),"Host_Club_Debt":("other",False),"Japan_Sex_Industry":("other",False),
 # China AI stack + censorship
 "DeepSeek":("ai_lab",False),"Zhipu_AI":("ai_lab",False),"Moonshot":("ai_lab",False),"MiniMax":("ai_lab",False),"StepFun":("ai_lab",False),"01_AI":("ai_lab",False),"Baichuan":("ai_lab",False),"iFlytek":("ai_lab",False),
 "Alibaba":("bigtech_asia",True),"Baidu":("bigtech_asia",True),"Tencent":("bigtech_asia",True),"Xiaomi":("bigtech_asia",True),"Huawei":("bigtech_asia",True),
 "Cambricon":("chip_vendor",True),"Biren":("chip_vendor",False),"Moore_Threads":("chip_vendor",False),
 "CAC":("regulator",True),"MIIT":("regulator",True),"China_AI_Labs":("ai_lab",False),"China_AI_Hardware":("chip_vendor",False),"China_AI_Censorship":("surveillance",False),
 # local / uncensored / decentralized AI
 "llama_cpp":("ai_infra",False),"Ollama":("ai_infra",False),"vLLM":("ai_infra",False),"LM_Studio":("ai_infra",False),"GPT4All":("ai_infra",False),"Jan":("ai_infra",False),"ComfyUI":("ai_infra",False),
 "Stability_AI":("ai_lab",False),"Black_Forest_Labs":("ai_lab",False),"Hugging_Face":("ai_infra",True),"EleutherAI":("ai_lab",False),"Nous_Research":("ai_lab",False),"AllenAI_OLMo":("ai_lab",False),
 "Heretic":("ai_infra",False),"Dolphin":("ai_lab",False),"Eric_Hartford":("person",False),
 "Bittensor":("crypto_infra",False),"Akash":("crypto_infra",False),"Render":("crypto_infra",False),"Octra":("crypto_infra",False),"Venice_AI":("crypto_infra",False),"Erik_Voorhees":("person",False),"FUTO":("ai_infra",False),
 "Local_AI_Tooling":("ai_infra",False),"Uncensored_AI":("ai_infra",False),"Decentralized_AI":("ai_infra",False),"Open_Local_AI":("ai_infra",False),
 "Fhenix":("crypto_infra",False),"Biconomy":("crypto_infra",False),"TapBit":("exchange",True),
 # surveillance & cyber-threat layer
 "VoltTyphoon":("threat_actor",False),"APT28_FancyBear":("threat_actor",False),"APT29_CozyBear":("threat_actor",False),"Sandworm":("threat_actor",False),"Kimsuky":("threat_actor",False),"Equation_Group":("threat_actor",False),"APT_State_Actors":("threat_actor",False),
 "MSS":("state_intel",True),"Unit_8200":("state_intel",True),"North_Korea":("state",True),"Israel":("state",True),"CALEA_Backdoor":("surveillance",False),"Viasat":("satellite",False),
 "NSO_Group":("surveillance",False),"Pegasus":("surveillance",False),"Intellexa":("surveillance",False),"Cytrox":("surveillance",False),"Predator":("surveillance",False),"Paragon":("surveillance",False),"Cellebrite":("surveillance",False),"Commercial_Spyware":("surveillance",False),
 "LockBit":("threat_actor",False),"ALPHV_BlackCat":("threat_actor",False),"Scattered_Spider":("threat_actor",False),"Cl0p":("threat_actor",False),"Ransomware_RaaS":("threat_actor",False),
 "Clearview_AI":("surveillance",False),"Anduril":("defense_tech",True),"ImmigrationOS":("surveillance",False),"ICE":("state",True),"Private_Surveillance":("surveillance",False),
 "CrowdStrike":("security_research",True),"Mandiant":("security_research",False),"Recorded_Future":("security_research",False),"Cyber_Defense":("security_research",False),
 # SE Asia scam/crime nexus
 "SE_Asia_Scam_Complex":("threat_actor",False),"Chen_Zhi":("person",False),"Zhao_Wei":("person",False),"KK_Park":("threat_actor",False),"Qingsong_Park":("threat_actor",False),"POGO":("threat_actor",False),
 "Golden_Triangle_SEZ":("other",False),"Kings_Romans":("other",False),"Tudou_Guarantee":("crypto_infra",False),"Starlink":("satellite",True),
 "Myanmar":("state",True),"Laos":("state",True),"Philippines":("state",True),"Thailand":("state",True),
 # Russia state network
 "Putin":("person",False),"Siloviki":("state",False),"Gazprom":("energy",True),"Rosneft":("energy",True),"Igor_Sechin":("person",False),
 "Shadow_Fleet":("logistics",False),"Wagner":("defense",False),"Africa_Corps":("defense",False),
 "FSB":("state_intel",True),"GRU":("state_intel",True),"SVR":("state_intel",True),"Russian_Intel":("state_intel",False),
 "Bortnikov":("person",False),"Kostyukov":("person",False),"Naryshkin":("person",False),"Sberbank":("bank",True),"Ukraine":("state",True),
 # Ukraine war economy
 "Zelensky":("person",False),"Ukraine_Minerals":("critical_minerals",False),"US_Ukraine_Reconstruction_Fund":("spv",False),"Western_Aid_Ukraine":("financier",False),"EU":("state",True),
 "Ukraine_Drone_Industry":("defense",True),"Brave1":("defense",False),"Energoatom":("energy",True),"NABU":("regulator",True),"Operation_Midas":("regulator",False),"Mindich":("person",False),"Halushchenko":("person",False),
 # Iran state network
 "Iran":("state",True),"Khamenei":("person",False),"IRGC":("defense",True),"Bonyads":("industrial",False),"Iran_Oil":("energy",True),"Chinese_Teapots":("energy",True),
 "Axis_of_Resistance":("defense",False),"Hezbollah":("defense",False),"Hamas":("defense",False),"Houthis":("defense",False),"Syria":("state",True),"Iran_Nuclear_Program":("defense",False),"IAEA":("regulator",True),
 # China party-state
 "CCP":("state",False),"Xi":("person",False),"Politburo_Standing_Committee":("state",False),"Fourth_Plenum":("state",False),"CMC":("defense",True),"PLA":("defense",True),"State_Council":("state",False),"15th_Five_Year_Plan":("state",False),
 "SASAC":("regulator",True),"Central_SOEs":("industrial",False),"Military_Civil_Fusion":("defense",False),"Provincial_Governments":("state",False),"Ant_Group":("bigtech_asia",True),"DiDi":("bigtech_asia",True),"China_Tech_Crackdown":("regulator",False),
 # Australia
 "Albanese":("person",False),"AUKUS":("defense",False),"UK":("state",True),"SSN_AUKUS":("defense",False),"US_Australia_Minerals_Framework":("state",False),
 "Critical_Minerals_Strategic_Reserve":("critical_minerals",False),"Lynas":("critical_minerals",True),"BHP":("industrial",True),"Rio_Tinto":("industrial",True),"Fortescue":("industrial",True),"Superannuation_Funds":("financier",True),
 # India
 "India":("state",True),"Modi":("person",False),"BJP":("political",False),"Adani_Group":("industrial",True),"Gautam_Adani":("person",False),"Reliance":("industrial",True),"Ambani":("person",False),
 "UPI":("financial_infra",False),"Aadhaar":("surveillance",False),"India_DPI":("financial_infra",False),"BRICS":("state",False),"Quad":("state",False),"IMEC":("state",False),
 # BRICS+ / de-dollarization
 "Brazil":("state",True),"Egypt":("state",True),"Ethiopia":("state",True),"UAE":("state",True),"Indonesia":("state",True),"Saudi_Arabia":("state",True),"BRICS_Partners":("state",False),
 "NDB":("financier",True),"BRICS_Pay":("financial_infra",False),"BRICS_Unit":("financial_infra",False),"De_Dollarization":("financial_infra",False),
 # CLARITY Act fight
 "CLARITY_Act":("state",False),"Catholic_Coalition":("political",False),"Law_Enforcement_Coalition":("regulator",False),"Crypto_AML_Gap":("financial_infra",False),
 # opioid crisis
 "Opioid_Crisis":("other",False),"Purdue_Pharma":("industrial",False),"Sackler_Family":("person",False),"Big_Three_Distributors":("industrial",True),"JNJ":("industrial",True),
 "Pharmacies":("industrial",True),"Fentanyl":("commodity",False),"SCOTUS":("regulator",True),"State_AGs":("regulator",False),
 # defense primes + QRL patent
 "Lockheed_Martin":("defense",True),"RTX":("defense",True),"Raytheon":("defense",True),"Leonardo":("defense",True),"Leonardo_DRS":("defense",True),
 "MEF":("state",False),"FOCI_Proxy":("state",False),"ELSAG":("surveillance",False),"AgustaWestland_Scandal":("defense",False),"QRL_XMSS_Patent":("pqc_quantum",False),
 # 3D-stacking scaling race
 "IBM_Nanostack":("semiconductor",False),"Huawei_Tau_Scaling":("semiconductor",False),"CFET":("semiconductor",False),"IMEC":("semiconductor",False),
 # PFAS forever chemicals
 "PFAS":("commodity",False),"3M":("industrial",True),"DuPont":("industrial",True),"Chemours":("industrial",True),"Corteva":("industrial",True),
 "AFFF_MDL":("regulator",False),"EPA":("regulator",True),"EPA_PFAS_Rule":("regulator",False),"Public_Water_Systems":("other",False),"PFAS_Suppression":("other",False),
 # J&J talc / Texas two-step / liability engineering
 "Talc_Litigation":("other",False),"LTL_Red_River":("industrial",False),"Texas_Two_Step":("other",False),"Divisive_Merger":("other",False),"Bankruptcy_Courts":("regulator",True),"Liability_Engineering":("other",False),
 # asbestos mass tort
 "Asbestos":("commodity",False),"Asbestos_Trusts":("financial_infra",False),"Johns_Manville":("industrial",False),"Mesothelioma_Claims":("other",False),"EPA_Asbestos_Ban":("regulator",False),"Asbestos_Trust_Transparency":("other",False),
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
 # right-to-repair umbrella (overlay; DAG into sinks, excluded from proofs)
 "Right_to_Repair":("other",False),"Consumer_Rights_Wiki":("other",False),"Parts_Pairing":("other",False),
 "FULU_Foundation":("political",False),"R2R_Opposition":("political",False),"Louis_Rossmann":("person",False),
 "iFixit":("industrial",False),"DMCA_1201":("state",False),"State_R2R_Laws":("state",False),"EU_R2R_Directive":("state",False),
 "Copyright_Office":("regulator",True),"FTC":("regulator",True),
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
