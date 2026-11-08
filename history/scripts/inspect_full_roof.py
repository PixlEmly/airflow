import os
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,'inspect_roof.py')).read().replace("'roof-study');","'roof-study','full');").replace("r'C:\\Users\\Emily\\Desktop\\out.obj'","os.path.join(ROOT,'roof-study','full','11_7_2026.obj')")
src=src.replace("scene.display.shading.color_type='MATERIAL'","scene.display.shading.color_type='TEXTURE'")
exec(src)
