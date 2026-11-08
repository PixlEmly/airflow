import bpy,numpy as np,os,json
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'new-scan')
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'scan-detail.blend'))
v=np.concatenate([np.array([o.matrix_world@p.co for p in o.data.vertices]) for o in bpy.context.scene.objects if o.type=='MESH'])
p=v[(v[:,0]>.65)&(v[:,2]>-1.2)&(v[:,2]<.1)]; rng=np.random.default_rng(1);best=None
for i in range(1000):
 a,b=p[rng.choice(len(p),2,replace=False),:2];d=b-a
 if np.linalg.norm(d)<.3:continue
 n=np.array([-d[1],d[0]]);n/=np.linalg.norm(n)
 if n[0]<0:n=-n
 if n[0]<.95:continue
 off=a@n;count=(abs(p[:,:2]@n-off)<.015).sum()
 if best is None or count>best[0]:best=(int(count),n,off)
print('WALL',best)
for z in [-1.3,-1.,-.5,0,.5,1.]:
 p=v[(abs(v[:,2]-z)<.08)&(v[:,0]<.45)&(v[:,1]>.3)&(v[:,1]<1.3)]
 if len(p):print('TREE',z,len(p),np.percentile(p,[2,50,98],axis=0).tolist())
for y in [-1,-.5,0,.5,1]:
 p=v[(abs(v[:,1]-y)<.1)&(v[:,2]>.45)&(v[:,2]<.85)&(v[:,0]>.0)]
 if len(p):print('ROOF',y,np.percentile(p,[2,50,98],axis=0).tolist())
