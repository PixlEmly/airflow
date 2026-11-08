"""Raise the shared chase to enclose the full silencer casing; run in Blender."""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'models/XLR8-all-options-toggle.blend'
bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box]
 return ([min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)])
col=next(c for c in bpy.data.collections if c.name.startswith(('SHARED ROOF CURB','SHARED ROOF CHASE')))
body=next(o for o in scene.objects if o.name.startswith('LD6 SILENCER'))
lo,hi=bounds(body);X=(lo[0]+hi[0])/2;Y=(lo[1]+hi[1])/2;top=hi[2]+.010;W=.4064
bands=[o for o in scene.objects if o.name.startswith('Silencer casing band')]
bandtop=max(bounds(o)[1][2] for o in bands)
assert top-.004>bandtop
for o in list(col.objects):
 if o.name.startswith('Square curb side'):
  points=[o.matrix_world@v.co for v in o.data.vertices];oldtop=max(p.z for p in points)
  for v,p in zip(o.data.vertices,points):
   if abs(p.z-oldtop)<.001:p.z=top
   v.co=p
  o.matrix_world.identity();o.data.update()
 elif o.name.startswith(('Square curb top','Square enclosure lid')):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.mesh.primitive_cube_add(size=1,location=(X,Y,top-.002));lid=bpy.context.object;lid.name='Square enclosure lid | full casing covered | reduced neck opening'
for c in list(lid.users_collection):c.objects.unlink(lid)
col.objects.link(lid);lid.dimensions=(W,W,.004);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);lid.data.materials.append(bpy.data.materials['Roof curb - folded metal'])
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.080,depth=.2,location=(X,Y,top));cutter=bpy.context.object
m=lid.modifiers.new('Reduced connector opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter;bpy.context.view_layer.objects.active=lid;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
col.name='SHARED ROOF CHASE | full silencer body concealed';col['lid_top_z_m']=top;col['casing_top_z_m']=hi[2]
connector=next(o for o in scene.objects if o.name.startswith('Upper 6in connector'));connector.name='Upper 6in connector to inward short-radius 90'
note=f'Roof surround corrected to cover the entire wide casing and its upper band. Lid top Z={top:.6f}m; casing body top={hi[2]:.6f}m; upper band top={bandtop:.6f}m. Six-inch connector and inward90 elbow remain above. Opening radius80mm is schematic clearance; construction details provisional.'
t=bpy.data.texts.get('LATEST - full silencer body concealed') or bpy.data.texts.new('LATEST - full silencer body concealed');t.clear();t.write(note)
bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=str(path))
(ROOT/'models/roof-chase-check.json').write_text(json.dumps({'lid_top_z_m':top,'lid_bottom_z_m':top-.004,'casing_top_z_m':hi[2],'band_top_z_m':bandtop,'square_width_inches':16,'lid_opening_diameter_inches':.16/.0254,'body_covered':True},indent=2))
print(note)
