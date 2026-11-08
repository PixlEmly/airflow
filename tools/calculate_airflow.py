"""Geometry-only screening; no fan operating point or acoustic performance prediction."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
IN=.0254;FT=.3048
Q=9900;bare_width=2.410000026;bare_depth=.500752985;liner=IN;thickness=.08;base=.3048
width=bare_width-2*liner;depth=bare_depth-2*liner;gap=depth/2
area=width*gap/FT**2;previous=bare_width*bare_depth/2/FT**2;v=Q/area;pv=(v/4005)**2
options=[]
for n,b,r in [(1,30,0),(2,36,0),(3,24,3),(4,12,5.25),(5,12,7.25)]:
 projection=.65-r*IN;bare=projection*(1-.02/.65);tip=(bare-2*liner)/2
 vertical_upper=(1.184-b*IN-3*thickness)/2
 options.append({'option':n,'base_inches':b,'projection_inches':projection/IN,'lined_tip_gap_inches':tip/IN,'vertical_gap_upper_bound_inches':vertical_upper/IN,'note':'Upper bound leaves zero hood approach clearance. Exterior-only alternatives are not internally designed.'})
data={'basis':'9900 CFM conservative user allowance; standard-density pressure scaling; no fan data','geometry_source':'Current Blender finished faces, 2026-11-08; update constants if model changes','flow_cfm':Q,'clear_width_inches':width/IN,'clear_depth_inches':depth/IN,'gap_inches':gap/IN,'area_sqft':area,'previous_area_sqft':previous,'velocity_fpm':v,'velocity_pressure_in_water':pv,'area_reduction_percent':100*(1-area/previous),'velocity_increase_percent':100*(previous/area-1),'velocity_pressure_increase_percent':100*((previous/area)**2-1),'hypothetical_K_sensitivity_NOT_prediction':[{'K':k,'loss_in_water':k*pv} for k in [1,3,5]],'options':options}
(ROOT/'calculations/airflow-screening.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(f'Area {area:.3f}ft2; velocity {v:.0f}fpm; velocity pressure {pv:.3f}in water (NOT total pressure loss)')
# Vector section schematic; dimensions describe finished faces, not a shop drawing.
scale=18;x0=150;x1=x0+depth/IN*scale;bottom=900;ground=bottom+12*scale
def z(y):return bottom-(y-base)/IN*scale
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1250" viewBox="0 0 1100 1250"><rect width="1100" height="1250" fill="#f6f5ef"/><g font-family="Arial,sans-serif" fill="#172f3a"><text x="45" y="48" font-size="28">OPTION 4 — LINED BAFFLE SECTION</text><text x="45" y="79" font-size="17">Schematic through the baffles; not a fabrication drawing. Dimensions in inches.</text><text x="45" y="110" font-size="16">Outside / building / outside. Width into page: 92.88 finished clear.</text>']
svg += [f'<rect x="{x0-30}" y="170" width="12" height="{bottom-170}" fill="#526775"/><rect x="{x0-18}" y="170" width="18" height="{bottom-170}" fill="#c8ac6c"/>',f'<rect x="{x1}" y="170" width="18" height="{bottom-170}" fill="#c8ac6c"/><rect x="{x1+18}" y="170" width="12" height="{bottom-170}" fill="#526775"/>']
for i in range(3):
 center=base+thickness/2+(2-i)*(thickness+gap);out=i!=1;a=(x0+x1)/2 if out else x0;b=x1 if out else (x0+x1)/2;y=z(center+thickness/2);h=thickness/IN*scale
 svg.append(f'<rect x="{a}" y="{y}" width="{b-a}" height="{h}" fill="#c8ac6c" stroke="#846c37"/><text x="560" y="{y+24}" font-size="19">{i+1}: {"OUTER" if out else "BUILDING"} mounted</text><text x="560" y="{y+47}" font-size="16">Center: {center/IN:.2f} above ground</text>')
svg += [f'<text x="155" y="155" font-size="18">Clear depth: {depth/IN:.2f}</text>',f'<text x="560" y="235" font-size="18">1.00 lining on interior walls</text><text x="560" y="265" font-size="18">1.00 lining on baffle faces and tips</text><text x="560" y="295" font-size="18">3.15 total baffle thickness</text><text x="560" y="325" font-size="18">1.15 remaining core allowance</text><text x="560" y="365" font-size="18">Tip and vertical gaps: {gap/IN:.2f}</text><text x="560" y="395" font-size="18">No overlap at finished tips</text>',f'<line x1="80" y1="{ground}" x2="970" y2="{ground}" stroke="#526775" stroke-width="5"/><text x="560" y="1000" font-size="19">12.00 base clearance to ground</text><text x="560" y="1030" font-size="16">Bottom outlet on building side</text><text x="90" y="1180" font-size="18">9,900 CFM allowance | 5.713 ft² nominal passage | 1,733 ft/min</text><text x="90" y="1210" font-size="16">Pressure loss, acoustic performance, core/support design and tree clearance unverified.</text></g></svg>']
(ROOT/'drawings/option-4-section.svg').write_text('\n'.join(svg),encoding='utf-8')
