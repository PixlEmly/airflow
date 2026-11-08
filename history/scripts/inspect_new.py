import os
base=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(base,'inspect_scan.py')).read()
src=src.replace("root=os.path.dirname(os.path.abspath(__file__))", "root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'new-scan')")
src=src.replace("'obj','11_2_2026.obj'", "'11_7_2026.obj'")
exec(src)
