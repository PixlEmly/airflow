import bpy,os,shutil,json,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
backup=os.path.join(OUT,'XLR8-before-option4-one-inch-lining.blend')
if not os.path.exists(backup):shutil.copy2(path,backup)
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
opt=next(c for c in scene.collection.children if c.name.startswith('OPTION 4 |'))
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box]
 return [min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]
front=next(o for o in opt.objects if 'Outer panel' in o.name);D=bounds(front)[0][1];base=bounds(front)[0][2]
ends=sorted([bounds(o) for o in opt.objects if 'Square end cap' in o.name],key=lambda b:b[0][0]);xmin=ends[0][1][0];xmax=ends[1][0][0]
for c in list(opt.children):
 if c.name.startswith(('OPTION 4 BAFFLES','OPTION 4 LINING')):
  for o in list(c.all_objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(c)
bc=bpy.data.collections.new('OPTION 4 BAFFLES | 1in lining included');opt.children.link(bc)
lc=bpy.data.collections.new('OPTION 4 LINING | 1in finished surfaces');opt.children.link(lc)
mat=bpy.data.materials.new('One inch lining | product and facing TBD');mat.diffuse_color=(.69,.56,.30,1)
coremat=bpy.data.materials.new('Baffle structural allowance');coremat.diffuse_color=(.25,.29,.32,1)
L=.0254;T=.08;ymin=L;ymax=D-L;xlo=xmin+L;xhi=xmax-L;W=xhi-xlo;gap=(ymax-ymin)/2;mid=(ymax+ymin)/2
def box(name,lo,hi,col,material=mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=tuple((lo[i]+hi[i])/2 for i in range(3)));o=bpy.context.object;o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.dimensions=tuple(hi[i]-lo[i] for i in range(3));bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);return o
top=next(o for o in opt.objects if 'Top closure' in o.name);zt=bounds(top)[0][2]
fl=box('Lining | OUTER panel | hide with panel for cutaway',(xmin,D-L,base),(xmax,D,zt),lc)
box('Lining | left end',(xmin,0,base),(xmin+L,D-L,zt),lc)
box('Lining | right end',(xmax-L,0,base),(xmax,D-L,zt),lc)
wall=box('Lining | building wall | vent penetrations',(xlo,0,base),(xhi,L,zt),lc)
def cut(target,cutter):
 m=target.modifiers.new('Existing vent opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter;bpy.context.view_layer.objects.active=target;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
for x,z,r in [(.204,1.759,.127),(-.181,1.769,.0762),(.65,1.759,.127)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=.15,location=(x,L/2,z),rotation=(math.pi/2,0,0));cut(wall,bpy.context.object)
for x0,x1,z0,z1 in [(-1.39,-.75,1.2,1.84),(.44,.86,1.55,1.97)]:cut(wall,box('temporary hood recess',(x0,-.04,z0),(x1,.08,z1),lc))
# Copy the existing perforated top closure so the duct opening remains open.
roofline=top.copy();roofline.data=top.data.copy();lc.objects.link(roofline);roofline.name='Lining | ceiling | existing duct opening retained'
v=[roofline.matrix_world@p.co for p in roofline.data.vertices];z0=min(p.z for p in v);z1=max(p.z for p in v)
for p,co in zip(roofline.data.vertices,v):co.z=zt-L+(co.z-z0)/(z1-z0)*L;p.co=co
roofline.matrix_world.identity();roofline.data.materials.clear();roofline.data.materials.append(mat)
for i in range(3):
 z=base+T/2+(2-i)*(T+gap);outside=i!=1;a,b=(mid,ymax) if outside else (ymin,mid);tip=mid
 prefix=f'Baffle {i+1} | '+('OUTER' if outside else 'BUILDING')
 box(prefix+' | upper 1in lining',(xlo,a,z+T/2-L),(xhi,b,z+T/2),bc)
 box(prefix+' | lower 1in lining',(xlo,a,z-T/2),(xhi,b,z-T/2+L),bc)
 ca,cb=(a,a+L) if outside else (b-L,b)
 box(prefix+' | tip 1in lining',(xlo,ca,z-T/2+L),(xhi,cb,z+T/2-L),bc)
 ca,cb=(a+L,b) if outside else (a,b-L)
 core=box(prefix+' | core 1.15in allowance',(xlo,ca,z-T/2+L),(xhi,cb,z+T/2-L),bc,coremat);core['total_lined_thickness_inches']=T/.0254
area=W*gap/.3048**2;oldarea=(xmax-xmin)*D/2/.3048**2;vel=9900/area;ratio=oldarea/area
note=f'''OPTION 4: ONE-INCH INTERIOR LINING ALLOWANCE
Design flow 9,900 CFM (three at 3,300). Six-inch roof duct excluded.
One inch added inward on building wall, outer face, ends and ceiling; existing vent/duct openings retained. Baffles have 1in on upper/lower faces and free tips. Existing 80mm total baffle envelope retained, leaving 29.2mm (1.15in) structural allowance; actual construction remains to be selected. No extra lining is added on top of the former lining-inclusive 80mm thickness.
Finished clear width {W/.0254:.2f}in; depth {(D-2*L)/.0254:.2f}in.
Finished half-depth projection and tip gap {gap/.0254:.2f}in; vertical gaps matched to {gap/.0254:.2f}in.
Lowest finished underside remains 12in above ground. Top/middle/bottom center elevations: {', '.join(f'{(base+T/2+(2-i)*(T+gap))/.0254:.2f}' for i in range(3))}in.
Nominal controlling full-width area {area:.3f}ft2, versus {oldarea:.3f}ft2 previously: {(1-area/oldarea)*100:.1f}% reduction.
Mean velocity at 9,900 CFM {vel:.0f}fpm, versus {9900/oldarea:.0f}fpm: {(ratio-1)*100:.1f}% increase.
Velocity-squared factor {ratio**2:.3f}: about {(ratio**2-1)*100:.0f}% higher dynamic pressure at equal flow. This is NOT a calculated total system pressure loss or predicted flow reduction. Loss coefficients, lining surface, turns, hood inlets, ground/tree discharge and fan curve are unverified.
To retain the former nominal passage area at the new finished width would require {oldarea*.3048**2/W/.0254:.2f}in clear gaps. With symmetric half-depth baffles and one inch lining on both walls, raw internal depth would need {2*(oldarea*.3048**2/W+L)/.0254:.2f}in, an increase of {(2*(oldarea*.3048**2/W+L)-D)/.0254:.2f}in over current geometry. That conflicts with the tree-driven depth constraint unless the enclosure location/width changes.
FRK identifies a facing, not a verified internal acoustic liner. Exact product, airstream-facing orientation, temperature and moisture suitability require confirmation. No absorption rating or acoustic improvement assigned. Manufacturer reference: https://www.jm.com/content/dam/jm/global/en/insulation-systems/products/assets/data-sheet/jm-hvac-superduct-rc-ds-en.pdf
Other options remain unchanged and hidden. Hide both Option 4 Outer panel and Lining OUTER panel for cutaway. Option 4 stays default.
'''
with open(os.path.join(OUT,'option-4-one-inch-lining.txt'),'w',encoding='utf-8') as f:f.write(note)
t=bpy.data.texts.get('OPTION 4 - baffle sizing and flow allowance');t.clear();t.write(note)
bpy.data.texts['START HERE - visibility toggles'].write('\nLATEST: One inch interior lining modeled. Hide both outer panel and its lining for cutaway. See OPTION 4 - baffle sizing and flow allowance. Previous standalone airflow report describes the unlined-wall version.\n')
scene['scope']='Option 4 with 1in interior lining; 9900CFM allowance; pressure loss unverified'
for c in scene.collection.children:
 if c.name.startswith('OPTION '):c.hide_viewport=c.hide_render=(c!=opt)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
front.hide_render=fl.hide_render=True
view('option-4-lined-baffles-cutaway',(-3.8,7,3.6),(-.2,.2,1.24),4.5)
front.hide_render=fl.hide_render=False
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=path)
assert len(bc.objects)==12
print(note)
