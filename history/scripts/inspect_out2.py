import os
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,'inspect_roof.py')).read().replace("'roof-study');","'roof-study','out2');").replace('Desktop\\out.obj','Desktop\\out2.obj').replace("cam.data.ortho_scale=7","cam.data.ortho_scale=3").replace("scene.display.shading.color_type='MATERIAL'","scene.display.shading.color_type='TEXTURE'")
exec(src)
