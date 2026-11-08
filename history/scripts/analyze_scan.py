exec(open(__file__.replace('analyze_scan.py','inspect_scan.py')).read().split('for name, pos')[0])
import numpy as np,json
v=np.array([scan.matrix_world@p.co for p in scan.data.vertices])
mask=(v[:,2]>-1.2)&(v[:,2]<0.6)&(v[:,0]>1)
p=v[mask]; rng=np.random.default_rng(12); best=None
for i in range(1500):
 a,b=p[rng.choice(len(p),2,replace=False),:2]; d=b-a
 if np.linalg.norm(d)<0.5:continue
 n=np.array([-d[1],d[0]]); n/=np.linalg.norm(n)
 if abs(n[0])<0.9:continue
 off=a@n; dist=abs(p[:,:2]@n-off); count=(dist<.025).sum()
 if best is None or count>best[0]:best=(int(count),n,off)
print('WALLFIT',best)
near=v[abs(v[:,:2]@best[1]-best[2])<.05]; print('WALLBOUND',np.percentile(near,[1,50,99],axis=0))
cam.location=(-15,0,0);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=8
scene.render.resolution_x=2000;scene.render.resolution_y=1400
scene.render.filepath=os.path.join(root,'scan_wall_detail.png');bpy.ops.render.render(write_still=True)
json.dump({'normal':best[1].tolist(),'offset':float(best[2])},open(os.path.join(root,'wall_fit.json'),'w'))
