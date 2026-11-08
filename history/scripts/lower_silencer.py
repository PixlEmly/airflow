import bpy,os,math,shutil
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-before-lowered-silencer.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
duct=next(c for c in bpy.data.collections if c.name.startswith('SHARED DUCT'))
X=-.181;Y=.035+.2286;elbowtop=1.769+.2286;newbottom=elbowtop+.05;drop=2.48-newbottom;newtop=newbottom+23.625*.0254
for o in list(duct.objects):
 if o.name.startswith(('6in vertical riser','Rain hood','RAIN HOOD','Silencer upper 6in spigot')):
  bpy.data.objects.remove(o,do_unlink=True)
 elif o.name.startswith(('LD6 SILENCER','Silencer lower 6in spigot','Silencer casing band','Silencer spiral seam')):
  o.location.z-=drop
# Remove small collar and replace with a body-sized roof opening/collar.
for o in list(duct.objects):
 if o.name.startswith('Roof penetration collar'):bpy.data.objects.remove(o,do_unlink=True)
metal=bpy.data.materials['Duct galvanized steel']
def assign(o,name):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 duct.objects.link(o);o.data.materials.append(metal);return o
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.0777,depth=.06,location=(X,Y,newtop+.03));assign(bpy.context.object,'Upper 6in connector to 120 degree rain bend')
# Bend starts vertically, turns outward, and continues to 30 degrees below horizontal.
R=.2286;N=48;K=48;startz=newtop+.06;vs=[]
for radius in [.0777,.0762]:
 for j in range(N+1):
  a=math.radians(120)*j/N;center=Vector((X,Y+R*(1-math.cos(a)),startz+R*math.sin(a)))
  side=Vector((0,math.cos(a),-math.sin(a)))
  for i in range(K):
   b=2*math.pi*i/K;vs.append(tuple(center+Vector((1,0,0))*radius*math.cos(b)+side*radius*math.sin(b)))
offset=(N+1)*K;faces=[]
for j in range(N):
 for i in range(K):
  q=(j*K+i,j*K+(i+1)%K,(j+1)*K+(i+1)%K,(j+1)*K+i);faces.append(q);faces.append(tuple(reversed([p+offset for p in q])))
for j in [0,N]:
 for i in range(K):a=j*K+i;b=j*K+(i+1)%K;faces.append((a,b,b+offset,a+offset))
me=bpy.data.meshes.new('Hollow 120 degree rain bend');me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new('RAIN OUTLET | 6in tube | 120deg bend | 30deg downward',me);duct.objects.link(o);me.materials.append(metal)
for p in me.polygons:p.use_smooth=True
o['bend_degrees']=120;o['centerline_radius_inches']=9;o['outlet_direction']='Away from wall, 30 degrees below horizontal'
# Expand schematic roof, soffit and top-closure penetrations for the silencer casing.
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.143,depth=1.4,location=(X,Y,2.25));cutter=bpy.context.object
targets=[o for o in scene.objects if o.type=='MESH' and (o.name.startswith(('ROOF | 10ft','Soffit reference')) or 'Top closure at soffit edge' in o.name)]
for o in targets:
 mod=o.modifiers.new('Silencer body clearance opening - schematic','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.context.view_layer.objects.active=o
 try:bpy.ops.object.modifier_apply(modifier=mod.name)
 except RuntimeError:pass
bpy.data.objects.remove(cutter,do_unlink=True)
roof=next(o for o in scene.objects if o.name.startswith('ROOF | 10ft'));grade=roof.get('pitch_rise_per_12',0)/12;roofz=2.26+(.65-Y)*grade
bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=12,major_radius=.143,minor_radius=.012,location=(X,Y,roofz+.014));assign(bpy.context.object,'Silencer roof collar | schematic, body-sized')
duct.name='SHARED DUCT | lowered silencer and 120deg rain bend'
note=f'''LOWERED SILENCER UPDATE\nBody lowered {drop/.0254:.2f} inches. Lower six-inch spigot meets the outlet of the original 90-degree elbow. Silencer casing now passes through the soffit/roof; penetrations enlarged schematically. Body dimensions remain 10.25-inch diameter by 23.625-inch length.\nRain cap replaced with hollow six-inch 120-degree return bend, provisional nine-inch centerline radius. Starts vertically, turns away from wall, discharges 30 degrees below horizontal. No end cap. This is geometry for design discussion, not a weatherproofing or installation detail.\n'''
bpy.data.texts.new('LATEST - lowered silencer and rain bend').write(note);bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
view('roof-silencer-overview',(4,7,4.5),(0,-.45,1.65),6.2)
front=[o for o in bpy.data.collections['OPTION 1 | base 30in | depth 25.6in'].objects if 'Outer panel' in o.name]
for o in front:o.hide_render=True
view('roof-silencer-cutaway',(-3,7,3.8),(0,.2,1.65),4.9)
for o in front:o.hide_render=False
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=path);print(note)
