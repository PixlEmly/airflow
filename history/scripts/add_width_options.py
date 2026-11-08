import bpy,os,shutil
ROOT=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(ROOT,'clearance-options');path=os.path.join(OUT,'XLR8-all-options-toggle.blend')
shutil.copy2(path,os.path.join(OUT,'XLR8-all-options-before-width-additions.blend'))
bpy.ops.wm.open_mainfile(filepath=path);scene=bpy.context.scene
source=bpy.data.collections['OPTION 1 | base 30in | depth 25.6in']
for num,trim in [(6,15),(7,17),(8,19)]:
 edge=.95-trim*.0254;width=edge+1.5
 col=bpy.data.collections.new(f'OPTION {num} | width -{trim}in | full depth | LEFT HOOD OUTSIDE');scene.collection.children.link(col)
 col['tree_side_trim_inches']=trim;col['width_inches']=width/.0254;col['depth_inches']=.65/.0254;col['base_inches']=12
 col['limitation']='Left 10-inch hood is not fully contained. Requires separate connection/treatment; this option is an exterior geometry study only.'
 for original in source.objects:
  o=original.copy();o.data=original.data.copy();col.objects.link(o);o.name=f'Option {num} | '+original.name.split('|',1)[-1].strip()
  coords=[o.matrix_world@v.co for v in o.data.vertices]
  for v,co in zip(o.data.vertices,coords):
   co.x=-1.5+(co.x+1.5)*width/2.45
   co.z=.3048+(co.z-.762)*(2.18-.3048)/(2.18-.762)
   v.co=co
  o.matrix_world.identity();o.data.update()
 col.hide_viewport=True;col.hide_render=True
notes='''\nADDED WIDTH-ONLY OPTIONS 6-8\nAll retain full 25.6-inch depth and 12-inch ground clearance. Only the tree-side end is moved inward; opposite end stays fixed.\nOPTION 6: trim 15 inches; resulting width approximately 81.5 inches. Near-clearance geometry study.\nOPTION 7: trim 17 inches; resulting width approximately 79.5 inches.\nOPTION 8: trim 19 inches; resulting width approximately 77.5 inches.\nIMPORTANT: every width-only option places the left 10-inch vent hood partly or wholly outside the enclosure. These require a separate duct connection or separate treatment for that hood. They are NOT full-coverage enclosure solutions as drawn. No duct reroute is modeled.\nOriginal options 1-5 and shared references are unchanged. Options 6-8 start hidden; use monitor/camera toggles to compare in place.\n'''
bpy.data.texts['START HERE - visibility toggles'].write(notes)
# Create previews without changing the saved initial visibility choice.
opts=[c for c in scene.collection.children if c.name.startswith('OPTION ')]
state={c:(c.hide_viewport,c.hide_render) for c in opts}
for num in [6,7,8]:
 for c in opts:c.hide_render=not c.name.startswith(f'OPTION {num} |')
 scene.render.filepath=os.path.join(OUT,f'option-{num}-width-only.png');bpy.ops.render.render(write_still=True)
for c,(viewport,render) in state.items():c.hide_viewport=viewport;c.hide_render=render
scene.render.filepath=os.path.join(OUT,'selected-option.png');bpy.ops.wm.save_as_mainfile(filepath=path)
for c in opts:print(c.name,len(c.objects),c.hide_viewport,c.hide_render)
