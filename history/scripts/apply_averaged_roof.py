import bpy,os,json,math
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
fits=json.load(open(os.path.join(ROOT,'roof-study','roof-average.json')))
grade=(fits['upper corrugated']['coefficients'][0]+fits['white lower horizontal']['coefficients'][0])/2
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
roof=next(o for o in scene.objects if o.name.startswith('ROOF | 10ft'))
for v in roof.data.vertices:
 run=.65-v.co.y;v.co.z+=run*(grade-2/12)
roof.data.update();roof.name='ROOF | 10ft run | averaged scan slope approx -0.23:12';roof['pitch_rise_per_12']=grade*12;roof['slope_basis']='Equal average of robust area-weighted planes fitted to corrugated upper patch and white horizontal soffit patch; crossfall leveled at existing soffit front. Approximate, not surveyed.'
roofcol=roof.users_collection[0];roofcol.name='SHARED ROOF | 10ft plane | scan-averaged slope'
collar=next(o for o in scene.objects if o.name.startswith('Roof penetration collar'));collar.location.z+=(.65-collar.location.y)*(grade-2/12)
note=f'''ROOF SLOPE UPDATE\nUser requested flattening/averaging corrugated and white scan sections. Robust area-weighted plane fits give depth grades {fits['upper corrugated']['coefficients'][0]:.4f} and {fits['white lower horizontal']['coefficients'][0]:.4f}. Equal mean {grade:.4f}, or {grade*12:.2f}:12 ({math.degrees(math.atan(grade)):.2f} degrees). The modeled back edge is {abs(grade)*120:.2f} inches LOWER over the 10-foot run, anchored at the existing soffit front. Crossfall along the soffit is leveled. This replaces the provisional 2:12 roof.\nThe surviving patches span only about 0.6 m in depth and have approximately 20 mm fit scatter. Slope magnitude and direction are uncertain; this is a scan-derived illustration, not a confirmed drainage pitch.\n'''
bpy.data.texts.new('LATEST - roof averaged from scan').write(note)
bpy.data.texts['START HERE - visibility toggles'].write('\n'+note)
cam=scene.camera
def view(name,pos,target,scale):
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=os.path.join(OUT,name+'.png');bpy.ops.render.render(write_still=True)
view('roof-silencer-overview',(4,7,4.5),(0,-.45,1.65),6.2)
front=[o for o in bpy.data.collections['OPTION 1 | base 30in | depth 25.6in'].objects if 'Outer panel' in o.name]
for o in front:o.hide_render=True
view('roof-silencer-cutaway',(-3,7,3.8),(0,.2,1.7),4.8)
for o in front:o.hide_render=False
cam.location=(4,7,4.5);cam.rotation_euler=(Vector((0,-.45,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=6.2
scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.wm.save_as_mainfile(filepath=path)
print(note)
