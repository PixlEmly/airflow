import bpy,os,json,numpy as np,math
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'merged-tree')
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'aligned-scans.blend'))
points=np.concatenate([np.array([o.matrix_world@v.co for v in o.data.vertices]) for o in bpy.context.scene.objects if o.type=='MESH'])
def hull(ps):
 ps=sorted(set(map(tuple,ps)))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 low=[];up=[]
 for p in ps:
  while len(low)>=2 and cross(low[-2],low[-1],p)<=0:low.pop()
  low.append(p)
 for p in reversed(ps):
  while len(up)>=2 and cross(up[-2],up[-1],p)<=0:up.pop()
  up.append(p)
 return np.array(low[:-1]+up[:-1])
verts=[];faces=[];unknown=[];reports=[];N=64
levels=[-1.30,-1.20,-1.05,-.85,-.60,-.35,-.10,.15,.40,.65,.90,1.15,1.40]
for z in levels:
 xmax=.5 if z<-1.1 else (.25 if z<-.8 else .10)
 ymax=1.6 if z<-1.1 else (1.5 if z<-.8 else 1.35)
 p=points[(abs(points[:,2]-z)<.055)&(points[:,0]>-1.15)&(points[:,0]<xmax)&(points[:,1]>.4)&(points[:,1]<ymax),:2]
 h=hull(p);center=(h.min(0)+h.max(0))/2;angles=np.arctan2(p[:,1]-center[1],p[:,0]-center[0])
 reports.append({'height_above_datum_m':z+1.55,'scan_x_extent_m':float(np.ptp(h[:,0])),'along_wall_extent_m':float(np.ptp(h[:,1])),'points':len(p)})
 missing=[]
 for i in range(N):
  a=2*math.pi*i/N;d=np.array([math.cos(a),math.sin(a)]);hits=[]
  for j in range(len(h)):
   edge=h[(j+1)%len(h)]-h[j]
   M=np.column_stack((d,-edge))
   if abs(np.linalg.det(M))<1e-9:continue
   t,u=np.linalg.solve(M,h[j]-center)
   if t>=0 and 0<=u<=1:hits.append(t)
  xy=center+d*min(hits);verts.append([-float(xy[1]),.823-float(xy[0]),z+1.55])
  angular=np.abs(np.arctan2(np.sin(angles-a),np.cos(angles-a)))
  missing.append(bool(angular.min()>math.radians(18)))
 unknown.append(missing)
face_uncertain=[]
for j in range(len(levels)-1):
 for i in range(N):
  faces.append([j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i]);face_uncertain.append(unknown[j][i] or unknown[j+1][i])
faces.extend([list(reversed(range(N))),list(range((len(levels)-1)*N,len(levels)*N))]);face_uncertain.extend([True,True])
data={'vertices':verts,'faces':faces,'inferred_faces':face_uncertain,'cross_sections':reports,'method':'Convex outlines of combined trunk slices; 110 mm height bands, lofted between levels. Unobserved angular gaps >18 degrees and end caps flagged. Lowest modeled section is 250 mm above datum; roots below that remain available in scan references, not extrapolated.'}
json.dump(data,open(os.path.join(OUT,'tree-envelope.json'),'w'),indent=2)
print(json.dumps(reports,indent=2))
