import bpy,os,json,numpy as np
from mathutils import Matrix,Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'revision-4');os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'revision-3','XLR8-enclosed-baffles-v3.blend'))
scene=bpy.context.scene;treecol=bpy.data.collections['05 Tree proxy - scan-derived envelope']
for o in list(treecol.objects):bpy.data.objects.remove(o,do_unlink=True)
treecol.name='05 Tree envelope - combined aligned scans'
data=json.load(open(os.path.join(ROOT,'merged-tree','tree-envelope.json')))
verts=[(-x,y,z) for x,y,z in data['vertices']];faces=data['faces']
mesh=bpy.data.meshes.new('Combined measured tree cross-sections');mesh.from_pydata(verts,[],faces);mesh.update();tree=bpy.data.objects.new('Tree | combined scan envelope | interpolated between measured slices',mesh);treecol.objects.link(tree)
mesh.materials.append(bpy.data.materials['Tree envelope / bark']);uncertain=bpy.data.materials.new('Inferred closure or unobserved angular gap');uncertain.diffuse_color=(.5,.49,.44,1);mesh.materials.append(uncertain)
for p,flag in zip(mesh.polygons,data['inferred_faces']):p.material_index=int(flag)
# Below the lowest reliable trunk slice, show an explicitly inferred plinth to local ground.
N=64;skirtverts=verts[:N]+[(x,y,0) for x,y,z in verts[:N]];skirtfaces=[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
ms=bpy.data.meshes.new('Unmeasured base transition');ms.from_pydata(skirtverts,[],skirtfaces);ms.update();skirt=bpy.data.objects.new('INFERRED base below 250 mm - gray',ms);treecol.objects.link(skirt);ms.materials.append(uncertain)
reg=json.load(open(os.path.join(ROOT,'merged-tree','registration.json')))
bpy.ops.wm.obj_import(filepath=os.path.join(ROOT,'obj','11_2_2026.obj'))
oldcol=bpy.data.collections.new('09 Earlier scan aligned to new scan - comparison');scene.collection.children.link(oldcol)
T=Matrix(((0,1,0,0),(-1,0,0,.823),(0,0,1,1.55),(0,0,0,1)))@Matrix(reg['old_to_new'])
for o in list(bpy.context.selected_objects):
 o.matrix_world=T@o.matrix_world
 for c in list(o.users_collection):c.objects.unlink(o)
 oldcol.objects.link(o);o.name='ALIGNED OLD SCAN | '+o.name
oldcol.hide_render=True;oldcol.hide_viewport=True
p=np.array(verts);inside=p[(p[:,0]>=-1.52)&(p[:,0]<=.97)&(p[:,1]>=-.02)&(p[:,1]<=.67)&(p[:,2]>=.3048)&(p[:,2]<=2.18)]
report={'registration':reg,'tree_cross_sections':data['cross_sections'],'tree_envelope_vertices_in_proposed_box':len(inside)}
if len(inside):report['overlap_bounds_m']=[inside.min(0).tolist(),inside.max(0).tolist()]
json.dump(report,open(os.path.join(OUT,'tree-measurements.json'),'w'),indent=2);print('RESULT',json.dumps(report))
cam=scene.camera
def render(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
shell=bpy.data.collections['03 Proposed enclosure - editable concept'];panels=[o for o in shell.objects if 'Outer panel' in o.name]
render('01-exterior',(4,7,4.4),(0,.45,1.4),4.6)
for o in panels:o.hide_render=True
render('02-cutaway',(-3,7,3.8),(0,.35,1.35),4.6)
for o in panels:o.hide_render=False
soffit=next(o for o in scene.objects if o.name.startswith('Soffit reference'));soffit.hide_render=True
for o in shell.objects:
 if 'Top closure' in o.name:o.hide_render=True
render('04-plan',(0,.75,8),(0,.75,0),4.0)
soffit.hide_render=False
for o in shell.objects:o.hide_render=False
render('01-exterior',(4,7,4.4),(0,.45,1.4),4.6)
notes='''Revision 4: tree envelope derived from both scans, aligned rigidly using common building surfaces. No independent scale change. Median matched-building surface distance approximately 22 mm; this is registration agreement, not absolute accuracy.
Tree outline rebuilt from combined cross-sections at 0.25 to 2.95 m above the approximate ground datum. Cross-sections are convex outlines lofted between heights, not an exact bark surface. Gray marks inferred end caps, angular gaps and the base transition below 0.25 m. Original scans retained in hidden collections 06 and 09.
At 1.45 m above datum, combined section is approximately 0.67 m perpendicular to wall by 0.60 m along wall (26.5 by 23.6 inches). Root flare is substantially wider. Scan registration uncertainty and local bark/ground ambiguity remain.
Enclosure dimensions, straight tree-side end cap, half-depth baffles and outer/inner/outer attachments are unchanged. Tree measurements and any envelope overlap with the provisional box are recorded in tree-measurements.json.
'''
txt=bpy.data.texts.new('REVISION 4 - merged tree');txt.write(notes);open(os.path.join(OUT,'README.txt'),'w').write(notes)
bpy.ops.object.select_all(action='DESELECT')
for col in scene.collection.children:
 if col.name.startswith(('01 ','02 ','03 ','04 ','05 ')):
  for o in col.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'XLR8-merged-tree-v4.glb'),export_format='GLB',use_selection=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'XLR8-merged-tree-v4.blend'))
