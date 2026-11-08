import bpy,os,math,shutil
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-before-short-radius-bends.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene;duct=next(c for c in bpy.data.collections if c.name.startswith('SHARED DUCT'))
X=-.181;Z=1.769;OLD_R=.2286;R=.1524;OLD_Y=.035+OLD_R;Y=.035+R;delta=R-OLD_R
metal=bpy.data.materials['Duct galvanized steel']
for o in list(duct.objects):
 if o.name.startswith(('90 DEG ELBOW','RAIN OUTLET','Silencer roof collar')):bpy.data.objects.remove(o,do_unlink=True)
 else:
  o.location.y+=delta;o.location.z+=delta
def elbow(name,top=False):
 N=40;K=64;vs=[];bottom=Z+R+.05;bodytop=bottom+23.625*.0254
 for radius in [.0777,.0762]:
  for j in range(N+1):
   a=math.pi/2*j/N
   if top:
    center=Vector((X,Y-R*(1-math.cos(a)),bodytop+.06+R*math.sin(a)));side=Vector((0,math.cos(a),math.sin(a)))
   else:
    center=Vector((X,.035+R*math.sin(a),Z+R*(1-math.cos(a))));side=Vector((0,-math.sin(a),math.cos(a)))
   for i in range(K):
    b=2*math.pi*i/K;vs.append(tuple(center+Vector((1,0,0))*radius*math.cos(b)+side*radius*math.sin(b)))
 off=(N+1)*K;fs=[]
 for j in range(N):
  for i in range(K):
   q=(j*K+i,j*K+(i+1)%K,(j+1)*K+(i+1)%K,(j+1)*K+i);fs.append(q);fs.append(tuple(reversed([k+off for k in q])))
 for j in [0,N]:
  for i in range(K):a=j*K+i;b=j*K+(i+1)%K;fs.append((a,b,b+off,a+off))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);duct.objects.link(o);me.materials.append(metal)
 for p in me.polygons:p.use_smooth=True
 o['nominal_diameter_inches']=6;o['centerline_radius_inches']=6;o['bend_degrees']=90
 return o
elbow('LOWER ELBOW | short-radius 90deg | 6in nominal CLR')
elbow('TOP ELBOW | short-radius 90deg | aimed inward over roof',True)
# Rebuild the clean roof and soffit so the earlier penetration does not remain as an extra hole.
roof=next(o for o in scene.objects if o.name.startswith('ROOF | 10ft'));grade=roof.get('pitch_rise_per_12',0)/12
def replace_mesh(o,verts,faces):
 mats=list(o.data.materials);me=bpy.data.meshes.new(o.name+' updated');me.from_pydata(verts,[],faces);me.update();o.data=me
 for m in mats:me.materials.append(m)
replace_mesh(roof,[(-1.625,.65,2.26),(1.625,.65,2.26),(1.625,.65-3.048,2.26+3.048*grade),(-1.625,.65-3.048,2.26+3.048*grade)],[(0,1,2,3)])
mod=roof.modifiers.new('Roof thickness','SOLIDIFY');mod.thickness=.035;bpy.context.view_layer.objects.active=roof;bpy.ops.object.modifier_apply(modifier=mod.name)
soffit=next(o for o in scene.objects if o.name.startswith('Soffit reference'))
# Primitive mesh coordinates match original local 3.25 x .65 x .08 box.
verts=[(x,y,z) for x in [-1.625,1.625] for y in [-.325,.325] for z in [-.04,.04]]
replace_mesh(soffit,verts,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)])
# Roof top closures are very thin hidden option parts; replace prior holes using each mesh bounding box.
tops=[o for o in scene.objects if 'Top closure at soffit edge' in o.name and o.type=='MESH']
for o in tops:
 coords=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(p[k] for p in coords) for k in range(3)];hi=[max(p[k] for p in coords) for k in range(3)]
 vs=[(x,y,z) for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]]
 replace_mesh(o,vs,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]);o.matrix_world.identity()
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.143,depth=1.5,location=(X,Y,2.25));cutter=bpy.context.object
for o in [roof,soffit]+tops:
 mod=o.modifiers.new('Relocated silencer opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.context.view_layer.objects.active=o
 try:bpy.ops.object.modifier_apply(modifier=mod.name)
 except RuntimeError:pass
bpy.data.objects.remove(cutter,do_unlink=True)
roofz=2.26+(.65-Y)*grade
bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=12,major_radius=.143,minor_radius=.012,location=(X,Y,roofz+.014));o=bpy.context.object;o.name='Silencer roof collar | relocated for short-radius elbow'
for c in list(o.users_collection):c.objects.unlink(o)
duct.objects.link(o);o.data.materials.append(metal)
duct.name='SHARED DUCT | short-radius 90s | top aimed inward'
note='Both bends now modeled as short-radius 90-degree elbows, six-inch nominal centerline radius for six-inch duct. Upper outlet aims inward over the roof, horizontally. Silencer shifted three inches toward the wall and three inches lower to remain directly seated on the smaller lower elbow. Penetrations relocated. Nominal elbow envelope follows the supplied visual reference, not a verified manufacturer drawing. Upper 120-degree rain bend superseded.'
bpy.data.texts.new('LATEST - short-radius inward elbows').write(note);bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
view('roof-silencer-overview',(4,7,4.5),(0,-.45,1.65),6.2)
front=[o for o in bpy.data.collections['OPTION 1 | base 30in | depth 25.6in'].objects if 'Outer panel' in o.name]
for o in front:o.hide_render=True
view('roof-silencer-cutaway',(-3,7,3.8),(0,.2,1.65),4.9)
for o in front:o.hide_render=False
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=path)
