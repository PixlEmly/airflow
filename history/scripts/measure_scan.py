import bpy,numpy as np,os
from mathutils import Vector
root=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'scan-inspection.blend'))
o=bpy.data.objects['Object'];v=np.array([o.matrix_world@p.co for p in o.data.vertices])
for name,m in [('trunk',(v[:,0]<1.4)&(v[:,0]>0)&(v[:,1]>.1)&(v[:,1]<1.4)&(v[:,2]>-.6)&(v[:,2]<.4)),('soffit',(v[:,0]>.5)&(v[:,0]<1.75)&(v[:,1]>-1.8)&(v[:,1]<0)&(v[:,2]>.3)&(v[:,2]<.8))]:
 print(name,len(v[m]),np.percentile(v[m],[2,50,98],axis=0))
