#!/usr/bin/env python3
"""Split opaque editorial inputs; combine actual reviewed reductions only."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def prepare():
 source=load('judging/normalization-input.json');rows=source['rows'];manifest=[]
 for start in range(0,len(rows),60):
  batch=start//60+1;selected=rows[start:start+60];inp=f'judging/editor-inputs/batch-{batch:02d}.json'
  save(inp,{'rule':source['rule'],'output_schema':{'editor':'actual internal editor label','rows':[{'row_id':'unchanged opaque ID','reason':'at most30 English whitespace words','note':'what was retained or condensed','scope_loss':'none, or specific unavoidable lost qualification'}]},'rows':selected})
  manifest.append({'batch':batch,'input':inp,'output':f'judging/editor-raw/batch-{batch:02d}.json','row_ids':[r['row_id'] for r in selected]})
 save('judging/editor-manifest.json',manifest);print({'rows':len(rows),'batches':len(manifest)})
def combine():
 manifest=load('judging/editor-manifest.json');overrides={};audit=[]
 for b in manifest:
  v=load(b['output']);rows=v['rows'];assert v.get('editor')
  assert len(rows)==len(b['row_ids']) and {r['row_id'] for r in rows}==set(b['row_ids'])
  for r in rows:
   assert r['row_id'] not in overrides and 0<len(r['reason'].split())<=30
   assert r.get('note') and r.get('scope_loss')
   overrides[r['row_id']]={k:r[k] for k in ['reason','note','scope_loss']}|{'editor':v['editor'],'editor_file':b['output']}
  audit.append({'batch':b['batch'],'rows':len(rows),'editor':v['editor'],'file':b['output']})
 expected={r['row_id'] for r in load('judging/normalization-input.json')['rows']}
 assert set(overrides)==expected
 save('judging/overrides.json',overrides);save('judging/editor-coverage.json',audit)
 print({'reviewed_overflows':len(overrides),'all_covered':True})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--combine',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 if a.combine:combine()
