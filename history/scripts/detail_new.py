import bpy,os,numpy as np
from mathutils import Vector
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'new-scan')
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'scan-inspection.blend'))
scene=bpy.context.scene;cam=scene.camera
cam.location=(-15,0,0); cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=4.2
scene.render.resolution_x=1800;scene.render.resolution_y=1600
scene.render.filepath=os.path.join(root,'wall_detail.png');bpy.ops.render.render(write_still=True)
vs=[]
for o in scene.objects:
 if o.type=='MESH':
  v=np.array([o.matrix_world@p.co for p in o.data.vertices]);vs.append(v); print(o.name,len(v),v.min(0),v.max(0))
v=np.concatenate(vs)
for name,mask in [('wall',(v[:,2]>-.9)&(v[:,2]<.1)),('soffit',(v[:,2]>.7)&(v[:,2]<1.2))]:
 h,e=np.histogram(v[mask,0],bins=60);inds=h.argsort()[-5:];print(name,[(float(e[i]),int(h[i])) for i in inds])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'scan-detail.blend'))
