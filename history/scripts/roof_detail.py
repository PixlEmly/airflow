import bpy,os,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'roof-study','full')
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'roof-scan.blend'))
sc=bpy.context.scene;c=sc.camera;c.location=(-10,0,.4);c.rotation_euler=(Vector((-.3,0,.1))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=2.7;sc.render.filepath=os.path.join(OUT,'detail.png');bpy.ops.render.render(write_still=True)
o=bpy.data.objects['Object'];v=np.array([o.matrix_world@p.co for p in o.data.vertices]);rng=np.random.default_rng(9);p=v[(v[:,0]<-.15)&(v[:,2]>.65)]
best=None
for i in range(1000):
 a,b,c=p[rng.choice(len(p),3,replace=False)];n=np.cross(b-a,c-a);mag=np.linalg.norm(n)
 if mag<1e-7:continue
 n/=mag
 if n[2]<0:n=-n
 if n[2]<.8:continue
 d=n@a;inliers=abs(p@n-d)<.015;count=inliers.sum()
 if best is None or count>best[0]:best=(count,n,d,inliers)
q=p[best[3]];fit=np.linalg.lstsq(np.column_stack([q[:,0],q[:,1],np.ones(len(q))]),q[:,2],rcond=None)[0]
print('ROOF_FIT',fit.tolist(),'bounds',q.min(0).tolist(),q.max(0).tolist(),'count',len(q))
