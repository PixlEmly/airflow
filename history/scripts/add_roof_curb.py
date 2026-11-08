import bpy,os,shutil
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-before-square-roof-curb.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
shared=next(c for c in bpy.data.collections if c.name.startswith('SHARED |'))
col=bpy.data.collections.new('SHARED ROOF CURB | square enclosure around silencer base');shared.children.link(col)
roof=next(o for o in scene.objects if o.name.startswith('ROOF | 10ft'));grade=roof.get('pitch_rise_per_12',0)/12
X=-.181;Y=.035+.1524;W=.4064;H=.2032;roofz=lambda y:2.26+(.65-y)*grade;TOP=roofz(Y)+H
metal=bpy.data.materials.new('Roof curb - folded metal');metal.diffuse_color=(.46,.52,.55,1)
def meshobj(name,v,f):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);me.materials.append(metal);return o
corners=[(X-W/2,Y-W/2),(X+W/2,Y-W/2),(X+W/2,Y+W/2),(X-W/2,Y+W/2)]
for i in range(4):
 a=corners[i];b=corners[(i+1)%4]
 o=meshobj('Square curb side %d'%(i+1),[(a[0],a[1],roofz(a[1])-.008),(b[0],b[1],roofz(b[1])-.008),(b[0],b[1],TOP),(a[0],a[1],TOP)],[(0,1,2,3)])
 mod=o.modifiers.new('Sheet thickness - illustrative','SOLIDIFY');mod.thickness=.003
# Flat curb lid with a round clearance hole for the silencer body.
o=meshobj('Square curb top | opening around silencer',[(x,y,TOP) for x,y in corners],[(0,1,2,3)])
mod=o.modifiers.new('Top thickness','SOLIDIFY');mod.thickness=.004;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.137,depth=.3,location=(X,Y,TOP));cutter=bpy.context.object
mod=o.modifiers.new('Silencer opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Simple surrounding apron follows the roof slope.
A=W+.1016;outer=[(X-A/2,Y-A/2),(X+A/2,Y-A/2),(X+A/2,Y+A/2),(X-A/2,Y+A/2)]
v=[(x,y,roofz(y)+.004) for x,y in outer+corners]
meshobj('Curb flashing apron | schematic',v,[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)])
col['width_inches']=16;col['height_above_roof_inches']=8;col['status']='Concept enclosure only; dimensions and flashing details provisional.'
note='Added square roof curb/chase around the lower silencer body, shared by all enclosure options. Illustrative dimensions: 16 x 16 inches, 8 inches high above roof at center; roof-following base, flat top with round silencer opening, schematic flashing apron. Upper silencer and inward-facing short-radius elbow remain exposed. This represents appearance and space envelope, not a specified weatherproofing/thermal-clearance assembly.'
bpy.data.texts.new('LATEST - square roof curb').write(note);bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
view('roof-silencer-overview',(4,7,4.5),(0,-.45,1.65),6.2)
view('roof-curb-detail',(-2,4,4.2),(X,Y,2.48),1.5)
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
bpy.ops.object.select_all(action='DESELECT');scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.wm.save_as_mainfile(filepath=path)
