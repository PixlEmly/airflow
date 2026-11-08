import bpy, math, os
from mathutils import Vector
root=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.wm.obj_import(filepath=os.path.join(root,'obj','11_2_2026.obj'))
scan=bpy.context.selected_objects[0]
print('SCAN',scan.name, list(scan.dimensions), [list(scan.matrix_world@Vector(v)) for v in scan.bound_box])
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO'; scene.display.shading.color_type='TEXTURE'
scene.display.shading.show_shadows=False; scene.display.shading.show_cavity=True
scene.display.shading.background_type='WORLD'; scene.world.color=(0.16,0.16,0.16)
scene.render.resolution_x=1400; scene.render.resolution_y=1100; scene.render.resolution_percentage=100
bpy.ops.object.camera_add(); cam=bpy.context.object; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=11
for name, pos in [('front',(0,-15,5)),('back',(0,15,5)),('left',(-15,0,5)),('right',(15,0,5)),('top',(0,0,16))]:
 cam.location=pos; cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=os.path.join(root,'scan_'+name+'.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'scan-inspection.blend'))
