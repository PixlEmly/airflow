import bpy, math, os, json
from mathutils import Vector, Matrix
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(ROOT,'initial-model');os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS'
def collection(name):
 c=bpy.data.collections.new(name);scene.collection.children.link(c);return c
context=collection('01 Reference geometry - scan-derived approximations')
vents=collection('02 Vents - nominal diameters, approximate centers')
shell=collection('03 Proposed enclosure - editable concept')
baffles=collection('04 Three alternating lined baffles')
treecol=collection('05 Tree proxy - scan-derived envelope')
scan_col=collection('06 Original textured scan - toggle for comparison')
annotations=collection('07 Diagram arrows')
def assign(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
wallmat=mat('Existing wall / slate',(0.40,.49,.54));roofmat=mat('Existing soffit / light stone',(.73,.74,.69))
panelmat=mat('Proposed shell / blue',(.12,.39,.54));bafflemat=mat('Baffle lining / warm ochre',(.78,.51,.19))
dark=mat('Vent interior',(.035,.06,.07));rim=mat('Vent rim / galvanized',(.65,.71,.73))
bark=mat('Tree envelope / bark',(.32,.23,.14));groundmat=mat('Ground datum',(.75,.76,.72));arrowmat=mat('Intended airflow',(.05,.65,.65))
def finish(o,name,col,material):
 o.name=name;assign(o,col);o.data.materials.append(material);return o
def box(name,loc,dim,col,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,col,material)
def prism(name,poly,z0,z1,col,material):
 n=len(poly);v=[(x,y,z) for z in (z0,z1) for x,y in poly];f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(v,[],f);mesh.update();o=bpy.data.objects.new(name,mesh);col.objects.link(o);o.data.materials.append(material);return o
def tube(name,center,radius,depth,col,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=center,rotation=(math.pi/2,0,0));return finish(bpy.context.object,name,col,material)
wall=box('Wall plane | fitted from scan',(0,-.055,1.13),(3.15,.11,2.26),context,wallmat)
soffit=box('Soffit reference | approx 650 mm projection',(0,.325,2.22),(3.25,.65,.08),context,roofmat)
box('Ground reference | local approximate datum',(0,.8,-.035),(4.0,2.8,.07),context,groundmat)
# Visible openings: center estimates from orthographic textured scan, diameters supplied by user.
for name,x,z,d in [('10 inch vent',-.204,1.759,.254),('6 inch vent',.181,1.769,.1524)]:
 tube(name+' nominal opening',(x,.014,z),d/2,.025,vents,dark)
 bpy.ops.mesh.primitive_torus_add(major_radius=d/2+.009,minor_radius=.009,major_segments=64,minor_segments=12,location=(x,.035,z),rotation=(math.pi/2,0,0));finish(bpy.context.object,name+' rim',vents,rim)
box('Large existing hood | scan-derived envelope',(1.07,.19,1.52),(.64,.38,.64),vents,rim)
box('Hood downward outlet',(1.07,.19,1.192),(.52,.28,.016),vents,dark)
# Tapered leaning trunk and root-flare proxy in transformed scan coordinates.
rings=[(.03,-.77,1.24,.57),(.25,-.78,1.22,.44),(.55,-.81,1.24,.33),(1.05,-.81,1.27,.25),(1.55,-.76,1.27,.22),(2.05,-.74,1.28,.21),(2.65,-.65,1.25,.20),(3.1,-.60,1.25,.19)]
verts=[];N=40
for z,x,y,r in rings:
 for i in range(N):
  a=2*math.pi*i/N;rr=r*(1+.05*math.sin(5*a));verts.append((x+rr*math.cos(a),y+rr*math.sin(a),z))
faces=[tuple(reversed(range(N))),tuple(range((len(rings)-1)*N,len(rings)*N))]
for j in range(len(rings)-1):
 for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
mesh=bpy.data.meshes.new('Tree proxy mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Tree | approximate trunk and root flare',mesh);treecol.objects.link(o);o.data.materials.append(bark)
# Face line jogs toward wall near tree. All dimensions editable in this script.
front=[(-1.5,.65),(-1.30,.65),(-1.10,.36),(-.58,.36),(-.35,.65),(1.5,.65)]
BOTTOM=.3048;TOP=2.18;T=.04
panels=[]
for i,(a,b) in enumerate(zip(front,front[1:])):
 dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
 p=box('Outer panel %02d | removable for cutaway'%(i+1),((a[0]+b[0])/2,(a[1]+b[1])/2,(BOTTOM+TOP)/2),(L,T,TOP-BOTTOM),shell,panelmat);p.rotation_euler.z=math.atan2(dy,dx);panels.append(p)
for x in [-1.5,1.5]:box('End return '+str(x),(x,.325,(BOTTOM+TOP)/2),(T,.65,TOP-BOTTOM),shell,panelmat)
prism('Top closure following tree recess',[(-1.5,0),(1.5,0)]+list(reversed(front)),TOP-.035,TOP,shell,panelmat)
# 40 percent local gap gives alternating overlap even in shallow recessed bay.
for idx,z in enumerate([1.08,.77,.46]):
 if idx%2==0:
  poly=[(-1.5,0),(1.5,0)]+[(x,d*.60) for x,d in reversed(front)]
 else:poly=[(x,d*.40) for x,d in front]+list(reversed(front))
 prism('Baffle %d | %s mounted | lining allowance included'%(idx+1,'wall' if idx%2==0 else 'outer-face'),poly,z-.04,z+.04,baffles,bafflemat)
def line(name,pts,r,col,material):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,co in zip(s.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);col.objects.link(o);o.data.materials.append(material);return o
flow=[(.5,.12,1.73),(.5,.49,1.40),(.5,.52,.97),(.5,.12,.92),(.5,.12,.65),(.5,.52,.60),(.5,.52,.29),(.5,.52,.12)]
line('Indicative airflow only - not simulated',flow,.018,annotations,arrowmat)
bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=0,radius2=.065,depth=.14,location=(.5,.52,.10));finish(bpy.context.object,'Airflow down arrow',annotations,arrowmat)
# Keep original geometry in the same coordinates; hide from concept views.
bpy.ops.wm.obj_import(filepath=os.path.join(ROOT,'new-scan','11_7_2026.obj'))
transform=Matrix(((0,-1,0,0),(-1,0,0,.823),(0,0,1,1.55),(0,0,0,1)))
for o in list(bpy.context.selected_objects):
 o.matrix_world=transform@o.matrix_world;assign(o,scan_col);o.name='SCAN original | '+o.name
scan_col.hide_render=True;scan_col.hide_viewport=True
# Restore scan handedness: raw Y becomes model X, raw -X becomes outward Y.
mirror=Matrix.Diagonal((-1,1,1,1))
for o in list(scene.objects):o.matrix_world=mirror@o.matrix_world
scene.render.engine='BLENDER_WORKBENCH';s=scene.display.shading;s.light='STUDIO';s.studiolight_rotate_z=.4;s.color_type='MATERIAL';s.show_shadows=True;s.show_cavity=True;s.cavity_type='BOTH';s.curvature_ridge_factor=1.25;s.curvature_valley_factor=1.1;s.show_object_outline=True;s.background_type='WORLD';scene.world.color=(.88,.89,.88)
scene.render.resolution_x=1600;scene.render.resolution_y=1300;scene.render.resolution_percentage=100
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Discussion view camera';scene.camera=cam;cam.data.type='ORTHO'
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
annotations.hide_render=True
view('01-exterior',(4,7,4.4),(0,.45,1.4),4.6)
for p in panels:p.hide_render=True
view('02-cutaway',(-3,7,3.8),(0,.35,1.35),4.6)
annotations.hide_render=False
treecol.hide_render=True
import bmesh
sectioncol=collection('08 Section slices - hidden after rendering')
original_vis={o:o.hide_render for col in [context,vents,shell,baffles] for o in col.objects}
for o in original_vis:
 if o.type!='MESH':continue
 o.hide_render=True
 if 'Ground' in o.name:continue
 copy=o.copy();copy.data=o.data.copy();sectioncol.objects.link(copy);copy.hide_render=False
 bm=bmesh.new();bm.from_mesh(copy.data);bm.transform(copy.matrix_world);copy.matrix_world=Matrix.Identity(4)
 for point,normal in [((.174,0,0),(-1,0,0)),((.234,0,0),(1,0,0))]:
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=point,plane_no=normal,clear_outer=True,clear_inner=False)
 boundary=[e for e in bm.edges if e.is_boundary]
 if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(copy.data);bm.free()
view('03-section',(7,.35,1.15),(0,.35,1.15),3.3)
sectioncol.hide_render=True;sectioncol.hide_viewport=True
for o,h in original_vis.items():o.hide_render=h
treecol.hide_render=False;annotations.hide_render=True
# Plan with soffit/top lifted out of view so recess and tree can be compared.
soffit.hide_render=True
for o in shell.objects:
 if 'Top closure' in o.name:o.hide_render=True
for p in panels:p.hide_render=False
view('04-plan',(0,.75,8),(0,.75,0),4.0)
soffit.hide_render=False
for o in shell.objects:o.hide_render=False
view('01-exterior',(4,7,4.4),(0,.45,1.4),4.6)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion();area.spaces.active.region_3d.view_distance=6;area.spaces.active.region_3d.view_location=(0,.5,1.4);area.spaces.active.shading.color_type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
for col in [context,vents,shell,baffles,treecol]:
 for o in col.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'XLR8-initial-concept.glb'),export_format='GLB',use_selection=True)
bpy.ops.file.pack_all()
notes='''XLR8 initial discussion model — 7 November 2026
SOURCE: new 11_7_2026 textured OBJ. Earlier scan NOT used.
Units: metres, provisionally retained from Space scan. Visual opening sizes consistent with nominal diameters, not a certified scale calibration.
REFERENCE: wall fitted in raw Blender coordinates approximately x - 0.01854*y = 0.823. Simplified model uses x=0.823, ground z=-1.55. Scan remains aligned in hidden collection 06.
Circular vents: nominal 254 mm and 152.4 mm diameter supplied by user; centers visually located in scan. Hood simplified to envelope.
PROPOSAL: 3 m width (cropped scan coverage, not confirmed total required coverage), 650 mm typical projection, 360 mm projection at tree recess. Bottom 304.8 mm above local ground datum. Tree is approximate trunk/root-flare proxy, not a clearance survey.
Three lined baffle envelopes: centers 1080, 770, 460 mm above ground; 80 mm total thickness each. Alternating wall/front/wall attachment. End gaps 40% of local depth = 260 mm typical, 144 mm at recess; THESE ARE NOT ONE-FOOT GAPS. Their restricted area needs review. No airflow or acoustic performance has been calculated.
No bottom closure. Roof/soffit reference approximated as horizontal. Existing hood included inside enclosure. Proposed hot-gas reroute omitted pending dimensions and confirmation; separate from this airflow concept.
Use named collections to hide outer panels, inspect baffles, or compare original scan. Geometry and materials individually editable. GLB contains simplified model only. Blend includes packed scan textures.
'''
bpy.data.texts.new('READ ME - assumptions and dimensions').write(notes)
open(os.path.join(OUT,'README.txt'),'w',encoding='utf-8').write(notes)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'XLR8-initial-concept.blend'))
print('DONE',OUT)
