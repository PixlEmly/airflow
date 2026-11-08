import bpy,os,numpy as np,json
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'roof-study','out2','roof-scan.blend'))
o=bpy.data.objects['out2'];v=np.array([o.matrix_world@p.co for p in o.data.vertices]);cent=[];areas=[];norm=[]
for p in o.data.polygons:
 if p.area<1e-8:continue
 cent.append(o.matrix_world@p.center);areas.append(p.area);norm.append(o.matrix_world.to_3x3()@p.normal)
c=np.array(cent);a=np.array(areas);n=np.array(norm)
results={}
for label,mask in [('upper corrugated',(c[:,2]>.78)&(abs(n[:,2])>.65)),('white lower horizontal',(c[:,2]>.59)&(c[:,2]<.76)&(abs(n[:,2])>.65))]:
 q=c[mask];w=a[mask];A=np.column_stack([q[:,:2],np.ones(len(q))]);fit=np.linalg.lstsq(A*np.sqrt(w[:,None]),q[:,2]*np.sqrt(w),rcond=None)[0]
 for i in range(10):
  residual=q[:,2]-A@fit;ww=w*np.minimum(1,.015/np.maximum(abs(residual),1e-9));fit=np.linalg.lstsq(A*np.sqrt(ww[:,None]),q[:,2]*np.sqrt(ww),rcond=None)[0]
 results[label]={'coefficients':fit.tolist(),'triangles':len(q),'x_run':float(np.ptp(q[:,0])),'rms_m':float(np.sqrt(np.average((q[:,2]-A@fit)**2,weights=w)))}
print(json.dumps(results,indent=2));json.dump(results,open(os.path.join(ROOT,'roof-study','roof-average.json'),'w'),indent=2)
