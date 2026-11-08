import bpy,os,math,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');os.makedirs(OUT,exist_ok=True)
options=[(1,'Raise base to 30 inches',30,0,'Approx. 3/4 inch tree clearance'),(2,'Raise base to 36 inches',36,0,'Approx. 2 inches tree clearance'),(3,'Raise base + reduce depth',24,3,'Approx. 2 1/2 inches tree clearance'),(4,'Reduce depth by 5 1/4 inches',12,5.25,'Near-contact fit; essentially no allowance'),(5,'Reduce depth by 7 1/4 inches',12,7.25,'Approx. 2 inches tree clearance')]
for num,title,base_in,reduction,clear in options:
 bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'revision-4','XLR8-merged-tree-v4.blend'))
 scene=bpy.context.scene;cam=scene.camera;D=.65-reduction*.0254;B=base_in*.0254;TOP=2.18
 shell=bpy.data.collections['03 Proposed enclosure - editable concept']
 for o in shell.objects:
  # Transform all shell vertices in world coordinates so panels and returns retain a simple rectangular footprint.
  coords=[o.matrix_world@v.co for v in o.data.vertices]
  for v,co in zip(o.data.vertices,coords):
   co.y*=D/.65;co.z=B+(co.z-.3048)*(TOP-B)/(TOP-.3048);v.co=co
  o.matrix_world.identity();o.data.update()
 # Clearance study: omit the interior layout, which needs redesign for high base variants.
 baff=bpy.data.collections['04 Three alternating lined baffles'];baff.hide_render=True;baff.hide_viewport=True
 bpy.data.collections['07 Diagram arrows'].hide_render=True;bpy.data.collections['07 Diagram arrows'].hide_viewport=True
 cam.location=(4,7,4.4);target=Vector((0,.45,1.35));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=5.3
 scene.render.resolution_x=1500;scene.render.resolution_y=1500;scene.render.resolution_percentage=100
 labels=bpy.data.collections.new('OPTION LABELS - exterior study only');scene.collection.children.link(labels)
 ink=bpy.data.materials.new('Caption ink');ink.diffuse_color=(.025,.055,.075,1)
 def text(name,body,x,y,size):
  c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.space_character=1.05
  o=bpy.data.objects.new(name,c);labels.objects.link(o);o.parent=cam;o.location=(x,y,-.5);o.rotation_euler=(0,0,0);c.materials.append(ink)
 text('Option title',f'OPTION {num}  |  {title}',-2.42,2.35,.135)
 text('Option dimensions',f'Bottom: {base_in:g}" above ground   |   Projection: {D/.0254:.1f}"   |   Depth reduction: {reduction:g}"',-2.42,2.12,.087)
 text('Clearance note',clear+'*',-2.42,-2.23,.105)
 text('Qualification','*Approximate merged-scan geometry. Exterior study; internal baffles require review.',-2.42,-2.42,.073)
 scene.render.filepath=os.path.join(OUT,f'option-{num}.png');bpy.ops.render.render(write_still=True)
 scene['option_description']=title;scene['base_height_inches']=base_in;scene['depth_reduction_inches']=reduction;scene['scope']='Exterior clearance study. Existing baffles hidden and NOT redesigned.'
 bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,f'option-{num}-exterior-study.blend'))
print('DONE',OUT)
