import bpy, os, json, numpy as np, math
from mathutils import Matrix,Vector,kdtree
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'merged-tree');os.makedirs(OUT,exist_ok=True)
def load(path):
 bpy.ops.wm.obj_import(filepath=path);obs=list(bpy.context.selected_objects)
 points=[];normals=[]
 for o in obs:
  points.extend([o.matrix_world@v.co for v in o.data.vertices]);normals.extend([o.matrix_world.to_3x3()@v.normal for v in o.data.vertices])
 return obs,np.array(points,dtype=float),np.array(normals,dtype=float)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
old,op,on=load(os.path.join(ROOT,'obj','11_2_2026.obj'));new,np_,nn=load(os.path.join(ROOT,'new-scan','11_7_2026.obj'))
def sample(p,n,mask,voxel=.035):
 p=p[mask];n=n[mask];_,ix=np.unique(np.floor(p/voxel).astype(int),axis=0,return_index=True);return p[ix],n[ix]
a,an=sample(op,on,(op[:,0]>.95)&(op[:,1]>-2.25)&(op[:,1]<1.8)&(op[:,2]>-1.35)&(op[:,2]<.85))
b,bn=sample(np_,nn,(np_[:,0]>.03)&(np_[:,2]>-1.2)&(np_[:,2]<.9))
kd=kdtree.KDTree(len(b))
for i,p in enumerate(b):kd.insert(p,i)
kd.balance()
def exp(w):
 angle=np.linalg.norm(w)
 if angle<1e-12:return np.eye(3)
 k=w/angle;K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
 return np.eye(3)+math.sin(angle)*K+(1-math.cos(angle))*K@K
results=[]
for y0 in [0,.15,.30,.45,.60]:
 R=np.eye(3);t=np.array([-.89,y0,.17])
 for iteration in range(70):
  p=a@R.T+t;norm=an@R.T;matches=[kd.find(x) for x in p];idx=np.array([m[1] for m in matches]);dist=np.array([m[2] for m in matches]);q=b[idx];n=bn[idx]
  keep=(dist<(.22 if iteration<15 else .10))&(abs((norm*n).sum(1))>.65)
  pp=p[keep];qq=q[keep];nm=n[keep];res=((pp-qq)*nm).sum(1)
  weight=np.minimum(1,.025/np.maximum(abs(res),1e-8));A=np.concatenate([np.cross(pp,nm),nm],axis=1)
  step=np.linalg.lstsq(A*weight[:,None],-res*weight,rcond=None)[0]
  if np.linalg.norm(step[:3])>.08:step*=.08/np.linalg.norm(step[:3])
  dR=exp(step[:3]);R=dR@R;t=dR@t+step[3:]
  if np.linalg.norm(step)<1e-7:break
 p=a@R.T+t;ds=np.array([kd.find(x)[2] for x in p]);inliers=ds[ds<.08];score=float(np.median(inliers));count=len(inliers)
 results.append((count,score,R,t));print('FIT',y0,count,score,R.tolist(),t.tolist())
best=max(results,key=lambda r:r[0]);_,score,R,t=best
trans=np.eye(4);trans[:3,:3]=R;trans[:3,3]=t
json.dump({'old_to_new':trans.tolist(),'overlap_median_distance_m':score,'inliers_under_80mm':best[0],'note':'Rigid ICP on common wall, soffit and hood only; scale unchanged.'},open(os.path.join(OUT,'registration.json'),'w'),indent=2)
for o in old:o.matrix_world=Matrix(trans.tolist())@o.matrix_world
# Render the registration before extracting a trunk.
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';s=scene.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.show_cavity=True;s.show_shadows=False;s.background_type='WORLD';scene.world.color=(.16,.16,.16)
for o in old:o.color=(.9,.45,.12,1)
for o in new:o.color=(.1,.55,.85,1)
scene.render.resolution_x=1600;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=4.1
for name,loc,target in [('front',(-10,0,0),(0,0,0)),('top',(0,0,10),(0,0,0)),('angle',(-7,-5,4),(0,0,0))]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=os.path.join(OUT,'aligned-'+name+'.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'aligned-scans.blend'))
# Print combined trunk samples in scan coordinates, for choosing extraction bounds.
allp=np.concatenate([op@R.T+t,np_])
for z in [-1.3,-1.,-.5,0,.5,1.,1.4]:
 pts=allp[(abs(allp[:,2]-z)<.05)&(allp[:,0]<.3)&(allp[:,1]>.2)&(allp[:,1]<1.4)]
 if len(pts):print('TRUNK',z,len(pts),np.percentile(pts,[0,10,50,90,100],axis=0).tolist())
