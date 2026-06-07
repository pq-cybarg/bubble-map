#!/usr/bin/env python3
"""
build_globe.py - generate report/GLOBE.html: a draggable/rotatable d3 orthographic globe
plotting the geographic spine of the analysis - chokepoints, supply responses, capital hubs,
settlement blocs - plus great-circle arcs for the key dependencies and capital flows.
Self-contained HTML; loads d3 v7 + topojson + world-atlas from CDN (needs internet to render map).
Data points are baked in from the analysis so the picture ties to the proofs.
"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP=os.path.join(ROOT,"report")

# [name, lat, lon, type, note]   type -> color/legend
POINTS=[
 ["China (REE processing)",39.9,116.4,"choke","~90% rare-earth processing, ~100% samarium; auto-denies foreign-military licenses (Dec 2025)"],
 ["Russia (U enrichment)",55.75,37.6,"choke","~44% of global uranium enrichment; HALEU chokepoint for SMRs"],
 ["Kazakhstan (U mining)",51.1,71.4,"choke","Kazatomprom ~38-40% of global uranium mining"],
 ["Taiwan (advanced chips)",25.0,121.5,"choke","TSMC - the leading-edge AI-chip fabrication chokepoint"],
 ["DR Congo (cobalt)",-4.3,15.3,"choke","~70% of cobalt (battery/grid metal); China-controlled offtake"],
 ["North Korea (Lazarus)",39.0,125.7,"threat","DPRK/Lazarus crypto theft (Ronin/Bybit) via Tornado Cash on Ethereum"],
 ["Greenland (CRML/Tanbreez)",60.9,-45.9,"supply","Critical Metals Corp REE; pre-revenue ~2028-29; US/EXIM interest"],
 ["Australia (Lynas REE)",-31.95,115.86,"supply","Lynas - largest ex-China REE; allied supply response"],
 ["Mountain Pass CA (MP)",35.48,-115.53,"supply","MP Materials - DoD ~15% equity + price floor; magnets ~2027"],
 ["Piketon OH (Centrus HALEU)",39.0,-83.0,"supply","Centrus American Centrifuge ~900 kg/yr HALEU (vs fleet need)"],
 ["San Francisco (AI core)",37.77,-122.4,"capital","OpenAI/Anthropic/NVIDIA/hyperscalers - the circular core"],
 ["Washington DC (DoD/Fed)",38.9,-77.0,"capital","$1T DoD budget; Fed (no feasible single rate); HFSC"],
 ["New York (Wall St)",40.7,-74.0,"capital","BlackRock/Apollo/Blackstone - private credit + USDC reserves"],
 ["Abu Dhabi (MGX)",24.45,54.38,"capital","MGX sovereign capital -> OpenAI/Anthropic/xAI/Stargate"],
 ["Riyadh (PIF)",24.7,46.7,"capital","Public Investment Fund - Gulf capital into the AI loop"],
 ["Tokyo (SoftBank/SBI)",35.68,139.69,"capital","SoftBank->OpenAI/Stargate/Arm; SBI ~9% of Ripple"],
 ["London (LBMA/TBI)",51.5,-0.12,"policy","LBMA gold; Tony Blair Institute->UK digital ID; Ofcom"],
 ["Basel (BIS)",47.55,7.59,"policy","BIS Project Agora - Western tokenized 'unified ledger'"],
 ["Abilene TX (Stargate)",32.45,-99.73,"datacenter","Stargate flagship AI datacenter (OpenAI/Oracle/SoftBank SPV)"],
 ["Memphis (xAI Colossus)",35.1,-90.0,"datacenter","xAI Colossus supercluster (now merged w/ SpaceX)"],
 ["Three Mile Island PA",40.15,-76.7,"datacenter","MSFT-Constellation nuclear restart (835MW, ~2028)"],
]
# [from_lat,from_lon,to_lat,to_lon,kind,label]
ARCS=[
 [39.9,116.4,38.9,-77.0,"choke","China rare earths -> US defense (independence ~2028)"],
 [55.75,37.6,39.0,-83.0,"choke","Russia enrichment -> US HALEU/SMR fuel"],
 [51.1,71.4,55.75,37.6,"choke","Kazakhstan uranium -> Russia/processing"],
 [25.0,121.5,37.77,-122.4,"choke","Taiwan chips -> US AI core"],
 [24.45,54.38,37.77,-122.4,"capital","MGX (UAE) -> AI core"],
 [24.7,46.7,37.77,-122.4,"capital","PIF (Saudi) -> AI core"],
 [35.68,139.69,37.77,-122.4,"capital","SoftBank (Japan) -> AI core"],
 [37.77,-122.4,32.45,-99.73,"flow","AI core -> Stargate datacenter"],
 [51.5,-0.12,38.9,-77.0,"policy","Ellison/TBI -> US/UK digital-ID policy"],
 [60.9,-45.9,35.48,-115.53,"supply","Greenland REE -> US processing (supply response)"],
 [-31.95,115.86,35.48,-115.53,"supply","Australia (Lynas) -> US (allied supply)"],
 [39.0,125.7,40.7,-74.0,"threat","DPRK crypto theft -> Western exchanges"],
]
COLORS={"choke":"#ff5a5a","threat":"#ff2bd6","supply":"#5ad17a","capital":"#5ab0ff","policy":"#c08bff","datacenter":"#ffd479","flow":"#8a96a8"}

HTML="""<!doctype html><html><head><meta charset=utf-8><title>AI Bubble - Geographic Chokepoint Globe</title>
<style>
body{margin:0;background:#05080f;color:#cfe;font:13px -apple-system,Segoe UI,Roboto,sans-serif;overflow:hidden}
#hud{position:fixed;top:12px;left:14px;z-index:5;max-width:320px}
h1{font-size:16px;color:#fff;margin:0 0 4px} .sub{color:#8a96a8;font-size:11px;margin-bottom:8px}
#legend span{display:block;margin:2px 0} .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
#tip{position:fixed;pointer-events:none;background:#0f1622e8;border:1px solid #2a3550;border-radius:6px;padding:7px 10px;max-width:280px;font-size:12px;display:none;z-index:10}
#tip b{color:#7fd1ff} .note{color:#8a96a8;position:fixed;bottom:8px;left:14px;font-size:11px}
.err{position:fixed;top:50%;left:0;right:0;text-align:center;color:#ff8a8a}
</style></head><body>
<div id=hud><h1>AI-bubble geographic chokepoints</h1><div class=sub>drag to rotate &middot; hover a node &middot; the spatial spine of the proofs</div>
<div id=legend></div></div>
<div id=tip></div><div class=note>red = adversary chokepoint &middot; green = supply response &middot; blue = capital hub &middot; purple = policy &middot; needs internet for basemap</div>
<svg id=g></svg>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3"></script>
<script>
const POINTS=__POINTS__, ARCS=__ARCS__, COLORS=__COLORS__;
const W=innerWidth,H=innerHeight, R=Math.min(W,H)/2-30;
const svg=d3.select('#g').attr('width',W).attr('height',H);
const proj=d3.geoOrthographic().scale(R).translate([W/2,H/2]).rotate([-10,-20]);
const path=d3.geoPath(proj); const tip=d3.select('#tip');
const leg=d3.select('#legend'); const seen={};
[['choke','adversary chokepoint'],['supply','supply response'],['capital','capital hub'],['policy','policy node'],['datacenter','datacenter'],['threat','threat actor']].forEach(([k,t])=>{
 leg.append('span').html('<span class=dot style="background:'+COLORS[k]+'"></span>'+t);});
svg.append('circle').attr('cx',W/2).attr('cy',H/2).attr('r',R).attr('fill','#07101f').attr('stroke','#1b2740');
const gGrat=svg.append('path').attr('fill','none').attr('stroke','#13203a').attr('stroke-width',.5);
const grat=d3.geoGraticule10();
let countries=null;
d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(world=>{
 countries=topojson.feature(world,world.objects.countries);
 render();
}).catch(e=>{d3.select('body').append('div').attr('class','err').text('basemap failed to load (needs internet) - markers still render');render();});
const gCountry=svg.append('g'), gArc=svg.append('g'), gPt=svg.append('g');
function visible(lon,lat){const c=proj.invert([W/2,H/2]);return d3.geoDistance([lon,lat],c)<Math.PI/2;}
function render(){
 gGrat.attr('d',path(grat));
 if(countries){gCountry.selectAll('path').data(countries.features).join('path').attr('d',path)
   .attr('fill','#0e1b30').attr('stroke','#1f3152').attr('stroke-width',.4);}
 gArc.selectAll('path').data(ARCS).join('path')
   .attr('d',d=>path({type:'LineString',coordinates:[[d[1],d[0]],[d[3],d[2]]]}))
   .attr('fill','none').attr('stroke',d=>COLORS[d[4]]).attr('stroke-width',1.1).attr('opacity',.55);
 gPt.selectAll('circle').data(POINTS).join('circle')
   .attr('transform',d=>{const p=proj([d[2],d[1]]);return p?`translate(${p[0]},${p[1]})`:'translate(-99,-99)';})
   .attr('r',d=>d[3]==='choke'?6:4.5).attr('fill',d=>COLORS[d[3]])
   .attr('stroke','#05080f').attr('stroke-width',1)
   .attr('opacity',d=>visible(d[2],d[1])?1:0)
   .on('mousemove',(e,d)=>{tip.style('display','block').style('left',(e.clientX+12)+'px').style('top',(e.clientY+12)+'px')
     .html('<b>'+d[0]+'</b><br>'+d[4]);})
   .on('mouseout',()=>tip.style('display','none'));
}
let v0,r0;
svg.call(d3.drag()
 .on('start',e=>{v0=[e.x,e.y];r0=proj.rotate();})
 .on('drag',e=>{const k=75/proj.scale();proj.rotate([r0[0]+(e.x-v0[0])*k,r0[1]-(e.y-v0[1])*k]);render();}));
let spin=true; svg.on('mousedown',()=>spin=false);
d3.timer(()=>{if(spin){const r=proj.rotate();proj.rotate([r[0]+0.18,r[1]]);render();}});
</script></body></html>"""
HTML=(HTML.replace("__POINTS__",json.dumps(POINTS))
          .replace("__ARCS__",json.dumps(ARCS))
          .replace("__COLORS__",json.dumps(COLORS)))
open(os.path.join(REP,"GLOBE.html"),"w").write(HTML)
print("wrote report/GLOBE.html ("+str(len(HTML))+" bytes) - "+str(len(POINTS))+" nodes, "+str(len(ARCS))+" arcs")
