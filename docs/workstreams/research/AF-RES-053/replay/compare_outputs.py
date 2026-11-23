#!/usr/bin/env python3
"""Structural post-render differences; no mutation or new prediction."""
from pathlib import Path
import datetime
import hashlib
import json
import xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parent
def load(n):return json.loads((BASE/'outputs'/n).read_text())
def diff(a,b,p=''):
    if a==b:return []
    if isinstance(a,dict) and isinstance(b,dict):
        return [r for k in sorted(a.keys()|b.keys()) for r in diff(a.get(k),b.get(k),p+'/'+k)]
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,p+'/'+str(i))]
    return [{'path':p,'A':a,'B':b}]
def xml_flat(n):
    root=ET.parse(BASE/'outputs'/n).getroot();rows=[]
    def walk(node,p):
        rows.append({'path':p,'tag':node.tag,'attributes':node.attrib,'text':node.text})
        for i,c in enumerate(node):walk(c,p+'/'+str(i))
    walk(root,'/');return rows
v03_compile=diff(load('V03-fixed-A.vega.json'),load('V03-fixed-B.vega.json'))
v03_svg=diff(xml_flat('V03-fixed-A.svg'),xml_flat('V03-fixed-B.svg'))
v03_scene=diff(load('V03-fixed-A.scenegraph.json'),load('V03-fixed-B.scenegraph.json'))
normal_svg=(BASE/'outputs/V02-normal-A.svg').read_bytes()==(BASE/'outputs/V02-normal-B.svg').read_bytes()
normal_compile=diff(load('V02-normal-A.vega.json'),load('V02-normal-B.vega.json'))
a=load('V02-normal-A.cell-checks.json');b=load('V02-boundary-A.cell-checks.json')
coordinates=[]
for x,y in zip(a,b):
    coordinates.append({'cell':x['cell'],'local_point_positions_equal':
      [(p['x_position'],p['y_position']) for p in x['observed_values']]==
      [(p['x_position'],p['y_position']) for p in y['observed_values']]})
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Parse preserved actual outputs; no full expected SVG exists.',
     'V02_normal_A_B_SVG_byte_equal':normal_svg,'V02_normal_compile_differences':normal_compile,
     'V02_normal_boundary_A_local_point_coordinates':coordinates,
     'coordinate_limit':'Local plot coordinates only. Global spacing/text extent is not asserted identical.',
     'V03_compile_A_B_differences':v03_compile,'V03_SVG_A_B_differences':v03_svg,'V03_scenegraph_A_B_differences':v03_scene}
(BASE/'output-differences.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'normal_svg_equal':normal_svg,'normal_compile_diff_count':len(normal_compile),
                  'V03_compile_diff_count':len(v03_compile),'V03_svg_diff_count':len(v03_svg),
                  'V03_scenegraph_diff_count':len(v03_scene),'V02_equal_local_cells':sum(x['local_point_positions_equal'] for x in coordinates)},ensure_ascii=False))
