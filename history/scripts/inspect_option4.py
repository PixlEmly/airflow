import bpy,os
from mathutils import Vector
p=os.path.join(os.path.dirname(__file__),'clearance-options','XLR8-all-options-toggle.blend')
bpy.ops.wm.open_mainfile(filepath=p)
for c in bpy.data.collections:
 if c.name.startswith(('OPTION 4','04 ','02 ')):
  for o in c.all_objects:
   if o.type=='MESH':
    v=[o.matrix_world@Vector(x) for x in o.bound_box]
    print(o.name, 'MIN',tuple(min(x[i] for x in v) for i in range(3)), 'MAX',tuple(max(x[i] for x in v) for i in range(3)))
