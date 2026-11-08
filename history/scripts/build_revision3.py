import os
root=os.path.dirname(os.path.abspath(__file__))
revision=open(os.path.join(root,'build_revision2.py'),encoding='utf-8').read()
revision=revision.replace("'revision-2'","'revision-3'").replace('XLR8-straight-corner-v2','XLR8-enclosed-baffles-v3')
extra="""
replace('d*.60','d*.50')
replace('d*.40','d*.50')
replace('End gaps 260 mm (10.2 inches); these remain smaller than a one-foot target.', 'Each internal baffle projects 325 mm, exactly half the 650 mm enclosure depth, leaving a 325 mm end gap. Top and bottom attach to the OUTER enclosure wall; middle attaches to the BUILDING wall. The exterior is fully closed on its face and ends; only the bottom is open for discharge. Cutaway images deliberately hide the outer face for explanation; they do not depict exterior access or storage shelves.')
replace('XLR8 revision 2 — straight corner, outside/inside/outside shelves','XLR8 revision 3 — enclosed system with half-depth internal baffles')
"""
revision=revision.replace('exec(compile(src,',extra+'\nexec(compile(src,')
exec(compile(revision,os.path.join(root,'build_revision2.py'),'exec'))
