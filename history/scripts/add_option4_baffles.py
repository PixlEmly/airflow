import bpy,os,shutil,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
backup=os.path.join(OUT,'XLR8-before-option4-baffles.blend')
if not os.path.exists(backup):shutil.copy2(path,backup)
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
opt=next(c for c in scene.collection.children if c.name.startswith('OPTION 4 |'))
for c in scene.collection.children:
 if c.name.startswith('OPTION '):c.hide_viewport=c.hide_render=(c!=opt)
for c in list(bpy.data.collections):
 if c.name.startswith('OPTION 4 BAFFLES'):
  for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(c)
col=bpy.data.collections.new('OPTION 4 BAFFLES | outside - inside - outside');opt.children.link(col)
front=next(o for o in opt.objects if 'Outer panel' in o.name)
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box]
 return [min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]
D=bounds(front)[0][1];ends=sorted([bounds(o) for o in opt.objects if 'Square end cap' in o.name],key=lambda b:b[0][0]);xmin=ends[0][1][0];xmax=ends[1][0][0];W=xmax-xmin
base=bounds(front)[0][2];T=.08;gap=D/2
mat=bpy.data.materials.new('Option 4 | lined baffles warm ochre');mat.diffuse_color=(.72,.43,.12,1)
for i in range(3):
 z=base+T/2+(2-i)*(T+gap);outer=i!=1;y0=gap if outer else 0;y1=D if outer else gap
 bpy.ops.mesh.primitive_cube_add(size=1,location=((xmin+xmax)/2,(y0+y1)/2,z));o=bpy.context.object
 o.name=f'Option 4 | Baffle {i+1} | '+('OUTER wall' if outer else 'BUILDING wall')+' | 80mm lined envelope'
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.dimensions=(W,y1-y0,T);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 o['lining_included']=True;o['provisional_thickness_mm']=80;o['clear_tip_gap_inches']=gap/.0254;o['attachment']='outer enclosure wall' if outer else 'building wall'
area=W*gap/(.3048**2);velocity=9900/area
data={'design_flow_cfm':9900,'outlets':3,'flow_per_outlet_cfm':3300,'clear_internal_width_inches':W/.0254,'clear_internal_depth_inches':D/.0254,'baffle_projection_inches':gap/.0254,'clear_tip_and_vertical_gap_inches':gap/.0254,'baffle_total_thickness_inches':T/.0254,'nominal_passage_area_sqft':area,'nominal_passage_velocity_fpm':velocity,'baffle_centers_inches':[(base+T/2+(2-i)*(T+gap))/.0254 for i in range(3)],'fan_static_pressure':'unknown','status':'Concept only; pressure loss and maintained fan flow unverified'}
with open(os.path.join(OUT,'option-4-airflow-check.json'),'w') as f:json.dump(data,f,indent=2)
report=f'''# Option 4 — provisional baffle layout

Design allowance: three outlets at 3,300 CFM each = 9,900 CFM total. The separate six-inch roof silencer route is excluded. User states this allowance exceeds actual flow and includes a buffer. Available fan static pressure is unknown.

Option 4 is the only visible option on opening. Options 1, 2, 3 and 5 remain in the same file, hidden in viewport and render. Baffles are a child collection of Option 4, so they follow its visibility. Hide its outer panel for a cutaway.

Three full-width internal baffles attach in order from top to bottom: OUTER wall / BUILDING wall / OUTER wall. Their 80 mm (3.15 in) solid envelopes include the provisional lining allowance. The lowest baffle underside is at the 12 in enclosure base. The enclosure face and ends remain closed; there is no external shelf access.

| Geometric check | Value |
|---|---:|
| Clear width between end panels | {W/.0254:.2f} in |
| Clear depth to inside of outer panel | {D/.0254:.2f} in |
| Each baffle projection | {gap/.0254:.2f} in |
| Each tip gap and inter-baffle vertical gap | {gap/.0254:.2f} in |
| Nominal full-width passage area | {area:.2f} sq ft |
| Mean passage velocity at 9,900 CFM | {velocity:.0f} ft/min |
| Top / middle / bottom baffle center above ground | {' / '.join(f'{v:.2f}' for v in data['baffle_centers_inches'])} in |

The top baffle upper face is approximately {(1.184-(base+T+2*(T+gap)))/.0254:.2f} in below the lowest modeled large-hood outlet. This is a local inlet clearance requiring review, not a validated inlet flow area. The lower half-depth baffle leaves a nominal half-depth bottom outlet. Ground, tree, supports, actual lining and nonuniform flow can reduce effective areas further. No additional full-wall lining allowance has been deducted.

Velocity sensitivity (illustrative comparisons, not acceptance criteria):

| Desired mean passage velocity | Required free area at 9,900 CFM | Required gap at current clear width |
|---|---:|---:|
'''
for v in [500,750,1000,1500]:report+=f'| {v} ft/min | {9900/v:.2f} sq ft | {(9900/v)/(W/.3048)*12:.2f} in |\n'
report+='''
Area divided by flow does not establish pressure loss or acoustic performance. Turns, contractions, lining roughness and discharge conditions add loss; the fan curve and total system resistance determine delivered flow. No zero-restriction claim is made. Half-depth baffles meet at the same depth coordinate without overlap; sound attenuation is not established by this layout. Increasing overlap would further reduce free area.

Before dimensions are treated as final, obtain a fan curve or measure airflow/static pressure and assess the complete inlet, turn and outlet path. Option 4 retains its previously modeled near-contact tree fit; no new tree clearance is claimed.

Reference: ASHRAE Fans, https://handbook.ashrae.org/Handbooks/S24/IP/S24_Ch21/S24_Ch21_ip.aspx
'''
with open(os.path.join(OUT,'option-4-airflow-check.md'),'w',encoding='utf-8') as f:f.write(report)
t=bpy.data.texts.get('OPTION 4 - baffle sizing and flow allowance') or bpy.data.texts.new('OPTION 4 - baffle sizing and flow allowance');t.clear();t.write(report)
t=bpy.data.texts.get('START HERE - visibility toggles');t.clear();t.write('OPTION 4 IS DEFAULT. Other options retained but hidden. Enable only one OPTION collection in viewport and render. SHARED remains visible. Option 4 contains three provisional internal baffles. Hide its Outer panel for a cutaway. See OPTION 4 - baffle sizing and flow allowance for dimensions and limitations. REFERENCE remains hidden.\n')
scene['scope']='Option 4 provisional lined baffles; 9900 CFM allowance; fan performance unverified';scene['design_flow_cfm']=9900
scene['visibility_help']='Option 4 visible by default. Toggle OPTION collections with monitor and camera icons. Baffles nested within Option 4.'
cam=scene.camera;scene.render.resolution_x=1600;scene.render.resolution_y=1500;scene.render.resolution_percentage=100
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
front.hide_render=True
view('option-4-baffles-cutaway',(-3.8,7,3.6),(-.2,.2,1.24),4.5)
front.hide_render=False
view('option-4-default',(4,7,4.5),(0,-.45,1.65),6.2)
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion();a.spaces.active.region_3d.view_location=(0,.1,1.4);a.spaces.active.region_3d.view_distance=6
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=path)
assert len(col.objects)==3
assert all(c.hide_render==(c!=opt) and c.hide_viewport==(c!=opt) for c in scene.collection.children if c.name.startswith('OPTION '))
print('VERIFIED',json.dumps(data));print('SAVED',path)
