"""Validate package hashes and required files; --write-manifest refreshes inventory."""
from pathlib import Path
import hashlib,json,sys,struct,re
ROOT=Path(__file__).resolve().parents[1]
def files():
 local_draft = ROOT/'drawings/option-4-dimensioned.pdf'
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and p != local_draft and '.git' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts and p.suffix not in ['.blend1','.blend2'] and p.name!='MANIFEST.json')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
required=['README.md','AGENTS.md','models/XLR8-all-options-toggle.blend','models/option-4-lined-review.glb','models/model-audit.json','drawings/current-exterior.png','drawings/option-4-lined-baffles-cutaway.png','drawings/option-4-section.svg','calculations/airflow-screening.json','docs/CHAT-HANDOFF.md']
for name in required:assert (ROOT/name).is_file(),f'Missing {name}'
if '--write-manifest' in sys.argv:
 inventory=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files()]
 (ROOT/'MANIFEST.json').write_text(json.dumps({'snapshot_date':'2026-11-08','files':inventory},indent=2),encoding='utf-8')
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
for row in manifest['files']:
 p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],f'Changed: {row["path"]}'
assert {r['path'] for r in manifest['files']}=={p.relative_to(ROOT).as_posix() for p in files()},'Manifest file list differs'
assert max(r['bytes'] for r in manifest['files'])<100*1024**2,'File exceeds GitHub regular-file size limit'
with (ROOT/'models/option-4-lined-review.glb').open('rb') as f:
 magic,version,length=struct.unpack('<4sII',f.read(12));assert magic==b'glTF' and version==2 and length==(ROOT/'models/option-4-lined-review.glb').stat().st_size
 chunk_length,chunk_type=struct.unpack('<I4s',f.read(8));assert chunk_type==b'JSON'
 gltf=json.loads(f.read(chunk_length))
 assert len(gltf.get('meshes',[]))>0
 assert not any(n.get('name','').startswith(('Option 1 |','Option 2 |','Option 3 |','Option 5 |')) for n in gltf.get('nodes',[])),'Hidden option leaked into GLB'
for mtl in (ROOT/'references/scans').rglob('*.mtl'):
 for line in mtl.read_text(encoding='utf-8').splitlines():
  if line.startswith('map_Kd '):assert (mtl.parent/line[7:].strip()).is_file(),f'Missing texture referenced by {mtl}'
for md in [ROOT/'README.md',*(ROOT/'docs').glob('*.md')]:
 for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
  if not target.startswith(('https://','http://','#')):assert (md.parent/target).exists(),f'Broken local link {target}'
audit=json.loads((ROOT/'models/model-audit.json').read_text())
assert len(audit['option_visibility'])==5
assert [o for o in audit['option_visibility'] if not o['hidden_viewport']][0]['name'].startswith('OPTION 4 |')
assert all(i['packed'] for i in audit['images']),'External image dependency remains'
print(f'PASS: {len(manifest["files"])} files, {sum(r["bytes"] for r in manifest["files"])/1024**2:.1f} MiB; hashes, GLB header, default option and image packing verified.')
