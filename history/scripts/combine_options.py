import bpy,os
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options')
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'option-1-exterior-study.blend'))
scene=bpy.context.scene
# Remove camera captions; collection names identify options in the shared scene.
for col in list(bpy.data.collections):
 if col.name.startswith('OPTION LABELS'):
  for o in list(col.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(col)
shell=bpy.data.collections['03 Proposed enclosure - editable concept']
shell.name='OPTION 1 | base 30in | depth 25.6in'
names={2:'OPTION 2 | base 36in | depth 25.6in',3:'OPTION 3 | base 24in | depth 22.6in',4:'OPTION 4 | base 12in | depth 20.3in',5:'OPTION 5 | base 12in | depth 18.3in'}
for n in range(2,6):
 path=os.path.join(OUT,f'option-{n}-exterior-study.blend')
 with bpy.data.libraries.load(path,link=False) as (source,target):
  target.collections=['03 Proposed enclosure - editable concept']
 col=target.collections[0];scene.collection.children.link(col);col.name=names[n]
 col.hide_viewport=True;col.hide_render=True
 for o in col.objects:o.name=f'Option {n} | '+o.name
for o in shell.objects:o.name='Option 1 | '+o.name
# Keep common context separate, so switching options changes only the enclosure.
common=bpy.data.collections.new('SHARED | building, vents, tree, ground');scene.collection.children.link(common)
reference=bpy.data.collections.new('REFERENCE | scans and prior internal layout');scene.collection.children.link(reference)
for col in list(scene.collection.children):
 if col in [common,reference] or col.name.startswith('OPTION '):continue
 if col.name.startswith(('01 ','02 ','05 ')):
  scene.collection.children.unlink(col);common.children.link(col)
 elif col.name.startswith(('04 ','06 ','07 ','08 ','09 ')):
  scene.collection.children.unlink(col);reference.children.link(col)
reference.hide_viewport=True;reference.hide_render=True
scene.name='XLR8 | compare five enclosure options'
scene['visibility_help']='Enable exactly one OPTION collection. Monitor icon controls viewport; camera icon controls render. Shared reference stays visible. Options are in identical coordinates.'
instructions='''FIVE OPTIONS IN ONE SCENE
All enclosure options occupy the same coordinates and use the same tree/building references.
Only OPTION 1 is visible initially.
In the Outliner, use the monitor icons to turn off the current OPTION and turn on another. If monitor icons are not visible, enable Disable in Viewports in the Outliner filter (funnel) menu. Camera icons independently control render visibility. Enable exactly one option for normal comparison.
SHARED contains the building, vents, merged tree and ground.
REFERENCE holds both source scans, the prior internal baffle layout and section helpers. It is hidden. These are exterior clearance options; internal baffles have NOT been redesigned for each option.
Option 1: bottom 30 inches; depth 25.6 inches.
Option 2: bottom 36 inches; depth 25.6 inches.
Option 3: bottom 24 inches; depth 22.6 inches.
Option 4: bottom 12 inches; depth 20.3 inches (near contact).
Option 5: bottom 12 inches; depth 18.3 inches.
'''
bpy.data.texts.new('START HERE - visibility toggles').write(instructions)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='OUTLINER':
   area.spaces.active.show_restrict_column_viewport=True;area.spaces.active.show_restrict_column_render=True
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
   area.spaces.active.region_3d.view_location=(0,.45,1.35)
   area.spaces.active.region_3d.view_distance=6
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath=os.path.join(OUT,'combined-scene-check.png');bpy.ops.render.render(write_still=True)
bpy.ops.file.pack_all();scene.render.filepath=os.path.join(OUT,'selected-option.png')
path=os.path.join(OUT,'XLR8-all-options-toggle.blend');bpy.ops.wm.save_as_mainfile(filepath=path)
for col in scene.collection.children:print('COLLECTION',col.name,'viewport_hidden',col.hide_viewport,'render_hidden',col.hide_render,'objects',len(col.objects))
print('SAVED',path)
