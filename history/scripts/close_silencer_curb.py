import bpy,os,shutil
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-before-full-silencer-enclosure.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
col=next(c for c in bpy.data.collections if c.name.startswith('SHARED ROOF CURB'))
body=next(o for o in scene.objects if o.name.startswith('LD6 SILENCER'))
bodytop=max((body.matrix_world@Vector(v)).z for v in body.bound_box)
top=bodytop+.012;X=-.181;Y=.035+.1524;W=.4064
for o in list(col.objects):
 if o.name.startswith('Square curb side'):
  oldtop=max(v.co.z for v in o.data.vertices)
  for v in o.data.vertices:
   if abs(v.co.z-oldtop)<.001:v.co.z=top
  o.data.update()
 elif o.name.startswith('Square curb top'):bpy.data.objects.remove(o,do_unlink=True)
me=bpy.data.meshes.new('Full silencer enclosure top');me.from_pydata([(X-W/2,Y-W/2,top),(X+W/2,Y-W/2,top),(X+W/2,Y+W/2,top),(X-W/2,Y+W/2,top)],[],[(0,1,2,3)]);me.update()
o=bpy.data.objects.new('Square enclosure lid | only reduced 6in neck exposed',me);col.objects.link(o);me.materials.append(bpy.data.materials['Roof curb - folded metal'])
mod=o.modifiers.new('Sheet thickness','SOLIDIFY');mod.thickness=.004;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.080,depth=.3,location=(X,Y,top));cutter=bpy.context.object
mod=o.modifiers.new('Reduced neck opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
roof=next(o for o in scene.objects if o.name.startswith('ROOF | 10ft'));roofz=2.26+(.65-Y)*roof.get('pitch_rise_per_12',0)/12
col.name='SHARED ROOF CHASE | full silencer body concealed';col['height_above_roof_inches']=(top-roofz)/.0254
note='Square roof enclosure extended above the full large-diameter silencer casing. Top opening reduced to the six-inch connector; only the reduced neck and inward-facing elbow are exposed. Width remains 16 inches; height is approximately %.1f inches above roof. Silencer retained inside as a separate object.'%((top-roofz)/.0254)
bpy.data.texts.new('LATEST - full silencer body concealed').write(note);bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
view('roof-silencer-overview',(4,7,4.5),(0,-.45,1.65),6.2)
view('roof-curb-detail',(-2,4,4.2),(X,Y,2.48),1.5)
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
bpy.ops.object.select_all(action='DESELECT');scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.wm.save_as_mainfile(filepath=path);print(note)
