import bpy,os,math,shutil
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-before-roof-silencer.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
for col in list(bpy.data.collections):
 if col.name.startswith(('OPTION 6 |','OPTION 7 |','OPTION 8 |')):
  for o in list(col.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(col)
shared=bpy.data.collections['SHARED | building, vents, tree, ground'];shared.name='SHARED | building, tree, roof, vents and silencer'
duct=bpy.data.collections.new('SHARED DUCT | 6in elbow, vertical silencer, rain hood');shared.children.link(duct)
roofcol=bpy.data.collections.new('SHARED ROOF | clean 10ft plane - pitch provisional');shared.children.link(roofcol)
def mat(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m
metal=mat('Duct galvanized steel',(.64,.7,.73));bodymat=mat('Silencer casing',(.5,.61,.66));seammat=mat('Silencer spiral seam',(.35,.43,.47));roofmat=mat('Clean roof surface',(.19,.23,.25))
def assign(o,name,col,m):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);o.data.materials.append(m);return o
def cyl(name,loc,r,depth,m=metal):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=loc);o=assign(bpy.context.object,name,duct,m)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o
def curve(name,pts,r,m):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=4;c.resolution_u=24;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,co in zip(s.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);duct.objects.link(o);c.materials.append(m);return o
X=-.181;Z=1.769;R=.2286;START=.035;Y=START+R;RAD=.0762
# Hollow quarter-circle elbow with constant six-inch nominal bore.
N=32;K=48;vs=[]
for r in [RAD+.0015,RAD]:
 for j in range(N+1):
  a=math.pi*.5*j/N;center=Vector((X,START+R*math.sin(a),Z+R*(1-math.cos(a))))
  side=Vector((0,-math.sin(a),math.cos(a)))
  for i in range(K):
   b=2*math.pi*i/K;p=center+Vector((1,0,0))*r*math.cos(b)+side*r*math.sin(b);vs.append(tuple(p))
fs=[];offset=(N+1)*K
for j in range(N):
 for i in range(K):
  q=(j*K+i,j*K+(i+1)%K,(j+1)*K+(i+1)%K,(j+1)*K+i);fs.append(q);fs.append(tuple(reversed(tuple(k+offset for k in q))))
for j in [0,N]:
 for i in range(K):a=j*K+i;b=j*K+(i+1)%K;fs.append((a,b,b+offset,a+offset))
me=bpy.data.meshes.new('Round six-inch quarter bend');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('90 DEG ELBOW | 6in bore | provisional 9in center radius',me);duct.objects.link(o);me.materials.append(metal)
for p in me.polygons:p.use_smooth=True
bottom=2.48;length=23.625*.0254;top=bottom+length
cyl('6in vertical riser through soffit and roof',(X,Y,(Z+R+bottom)/2),RAD+.0015,bottom-(Z+R))
cyl('LD6 SILENCER | body diameter 10.25in | body length 23.625in',(X,Y,(bottom+top)/2),10.25*.0254/2,length,bodymat)
cyl('Silencer lower 6in spigot',(X,Y,bottom-.025),RAD+.002,.05)
cyl('Silencer upper 6in spigot',(X,Y,top+.035),RAD+.002,.07)
for z in [bottom,bottom+.045,top-.045,top]:
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=8,major_radius=10.25*.0254/2,minor_radius=.004,location=(X,Y,z));assign(bpy.context.object,'Silencer casing band',duct,metal)
pts=[]
for i in range(241):
 a=i/240*math.pi*2*4;pts.append((X+.131*math.cos(a),Y+.131*math.sin(a),bottom+.02+(length-.04)*i/240))
curve('Silencer spiral seam - illustrative',pts,.0025,seammat)
cyl('Rain hood outlet neck',(X,Y,top+.095),RAD+.002,.12)
capz=top+.20
bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=.175,radius2=.025,depth=.09,location=(X,Y,capz+.045));assign(bpy.context.object,'RAIN HOOD | generic cap, dimensions provisional',duct,metal)
for angle in [0,2*math.pi/3,4*math.pi/3]:
 x=X+.095*math.cos(angle);y=Y+.095*math.sin(angle);curve('Rain hood support',[(x,y,top+.10),(x,y,capz)],.006,metal)
# Clean roof: span matches existing reconstructed soffit; ten-foot horizontal run backward.
WIDTH=3.25;RUN=3.048;PITCH=2/12;EAVE_Y=.65;EAVE_Z=2.26
verts=[(-WIDTH/2,EAVE_Y,EAVE_Z),(WIDTH/2,EAVE_Y,EAVE_Z),(WIDTH/2,EAVE_Y-RUN,EAVE_Z+RUN*PITCH),(-WIDTH/2,EAVE_Y-RUN,EAVE_Z+RUN*PITCH)]
me=bpy.data.meshes.new('Clean roof plane');me.from_pydata(verts,[],[(0,1,2,3)]);me.update();roof=bpy.data.objects.new('ROOF | 10ft run | 2:12 provisional pitch | existing soffit width',me);roofcol.objects.link(roof);me.materials.append(roofmat)
roof['pitch_rise_per_12']=2.;roof['run_feet']=10.;roof['width_basis']='Existing reconstructed soffit span, 3.25 m. New scan fragment is not a full-width measurement.'
solid=roof.modifiers.new('Roof thickness for display','SOLIDIFY');solid.thickness=.035
bpy.context.view_layer.objects.active=roof;roof.select_set(True);bpy.ops.object.modifier_apply(modifier=solid.name)
# Explicitly show duct penetration in roof and existing soffit/top closures.
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=RAD+.012,depth=1.2,location=(X,Y,2.25));cutter=bpy.context.object;cutter.name='Temporary roof penetration tool'
targets=[roof]+[o for o in scene.objects if o.type=='MESH' and (o.name.startswith('Soffit reference') or 'Top closure at soffit edge' in o.name)]
for o in targets:
 mod=o.modifiers.new('6in duct penetration - allowance provisional','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.context.view_layer.objects.active=o
 try:bpy.ops.object.modifier_apply(modifier=mod.name)
 except RuntimeError:pass
bpy.data.objects.remove(cutter,do_unlink=True)
# Flashing shown as a simple raised collar, not a construction detail.
roof_z=EAVE_Z+(EAVE_Y-Y)*PITCH
cyl('Roof penetration collar - schematic',(X,Y,roof_z+.035),RAD+.025,.07)
# Preserve supplied cleaned fragments separately as hidden source references.
reference=bpy.data.collections['REFERENCE | scans and prior internal layout']
rc=bpy.data.collections.new('Roof scan fragments | out2 | native coordinates, not registered');reference.children.link(rc)
bpy.ops.wm.obj_import(filepath=r'C:\Users\Emily\Desktop\out2.obj')
for o in list(bpy.context.selected_objects):
 for c in list(o.users_collection):c.objects.unlink(o)
 rc.objects.link(o)
rc.hide_viewport=True;rc.hide_render=True
notes='''ROOF AND DUCT ADDITION\nOptions 6, 7 and 8 removed at user request. Options 1-5 retained.\nSHARED DUCT: six-inch round elbow connects to the six-inch opening beside the right square hood; elbow center radius provisionally 9 inches. Straight riser passes through soffit/roof, followed by vertical silencer and generic rain hood. Silencer body uses supplied 10.25-inch diameter and 23.625-inch length with six-inch spigots. Spigot lengths, elbow radius, mounting elevation and cap dimensions are illustrative.\nSHARED ROOF: clean plane starts at the existing soffit top/front edge, spans the existing reconstructed soffit width of 3.25 m, extends backward 10 feet horizontally. Pitch 2:12 is PROVISIONAL because the surviving roof patch does not establish reliable pitch. New out2 scan confirms wedge hood/soffit form but is a cropped 1.26 m-wide fragment; it is not used to shrink the full-width reference. Flawed scan surfaces and giant plane omitted from modeled geometry.\nRoof/soffit penetrations are schematic. Performance, support, heat and installation clearances not assessed.\n'''
bpy.data.texts.new('ROOF AND DUCT - assumptions').write(notes)
start=bpy.data.texts['START HERE - visibility toggles'];old=start.as_string();old=old.split('ADDED WIDTH-ONLY OPTIONS')[0];start.clear();start.write(old+'\n'+notes)
cam=scene.camera;cam.location=(4,7,4.5);target=Vector((0,-.45,1.65));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
scene.render.resolution_x=1700;scene.render.resolution_y=1500
scene.render.filepath=os.path.join(OUT,'roof-silencer-overview.png');bpy.ops.render.render(write_still=True)
# Close cutaway view revealing connection from 6-inch opening.
option1=bpy.data.collections['OPTION 1 | base 30in | depth 25.6in'];front=[o for o in option1.objects if 'Outer panel' in o.name]
for o in front:o.hide_render=True
cam.location=(-3,7,3.8);target=Vector((0,.2,1.7));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=4.8
scene.render.filepath=os.path.join(OUT,'roof-silencer-cutaway.png');bpy.ops.render.render(write_still=True)
for o in front:o.hide_render=False
cam.location=(4,7,4.5);target=Vector((0,-.45,1.65));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_location=(0,-.3,1.6);a.spaces.active.region_3d.view_distance=7
bpy.ops.object.select_all(action='DESELECT');scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=path)
print('UPDATED',path)
