"""Run with Blender: blender -b --python tools/export_review.py"""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
model=ROOT/'models/XLR8-all-options-toggle.blend'
bpy.ops.wm.open_mainfile(filepath=str(model));scene=bpy.context.scene
options=[c for c in scene.collection.children if c.name.startswith('OPTION ')]
for c in options:c.hide_viewport=c.hide_render=not c.name.startswith('OPTION 4 |')
opt=next(c for c in options if c.name.startswith('OPTION 4 |'))
front=next(o for o in opt.objects if 'Outer panel' in o.name)
lining=next(o for o in opt.all_objects if o.name.startswith('Lining | OUTER panel'))
front.hide_render=lining.hide_render=False
bpy.ops.file.pack_all()
images=[]
for im in bpy.data.images:
 if im.source=='FILE':images.append({'name':im.name,'packed':bool(im.packed_file or im.packed_files),'external_file_exists':Path(bpy.path.abspath(im.filepath)).is_file()})
assert all(i['packed'] or i['external_file_exists'] for i in images),'Missing image resource'
cam=scene.camera;cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
scene.render.filepath=str(ROOT/'drawings/current-exterior.png');bpy.ops.render.render(write_still=True)
scene.render.filepath=str(ROOT/'drawings/option-4-default.png');bpy.ops.render.render(write_still=True)
cam.location=(-2,4,4.2);cam.rotation_euler=(Vector((-.181,.1874,2.53))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.35
scene.render.filepath=str(ROOT/'drawings/roof-curb-detail.png');bpy.ops.render.render(write_still=True)
front.hide_render=lining.hide_render=True
cam.location=(-3.8,7,3.6);cam.rotation_euler=(Vector((-.2,.2,1.24))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=4.5
scene.render.filepath=str(ROOT/'drawings/option-4-lined-baffles-cutaway.png');bpy.ops.render.render(write_still=True)
front.hide_render=lining.hide_render=False
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
bpy.ops.object.select_all(action='DESELECT')
selected=[]
for o in scene.objects:
 if o.type=='MESH' and o.visible_get() and not o.hide_render:o.select_set(True);selected.append(o.name)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'models/option-4-lined-review.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_apply=True)
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath='//../drawings/current-exterior.png'
bpy.ops.wm.save_as_mainfile(filepath=str(model),check_existing=False)
audit={'blender_version':bpy.app.version_string,'units':scene.unit_settings.system,'option_visibility':[{'name':c.name,'hidden_viewport':c.hide_viewport,'hidden_render':c.hide_render} for c in options],'images':images,'glb_mesh_objects':selected,'object_count':len(scene.objects),'lining_and_baffle_object_count':len([o for o in opt.all_objects if o.name.startswith(('Baffle ','Lining |'))])}
assert len(options)==5 and sum(not c.hide_render for c in options)==1
assert not front.hide_render and not lining.hide_render
(ROOT/'models/model-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('REVIEW EXPORT COMPLETE',len(selected),'mesh objects')
