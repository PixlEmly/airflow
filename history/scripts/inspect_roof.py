import bpy,os,numpy as np,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'roof-study');os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.wm.obj_import(filepath=r'C:\Users\Emily\Desktop\out.obj')
obs=list(bpy.context.selected_objects)
for o in obs:
 v=np.array([o.matrix_world@p.co for p in o.data.vertices]);print(o.name,len(v),v.min(0),v.max(0))
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_cavity=True;scene.display.shading.show_shadows=False;scene.world.color=(.16,.16,.16);scene.display.shading.background_type='WORLD'
scene.render.resolution_x=1400;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=7
for name,pos in [('front',(0,-12,3)),('back',(0,12,3)),('left',(-12,0,3)),('top',(0,0,12))]:
 cam.location=pos;cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'roof-scan.blend'))
