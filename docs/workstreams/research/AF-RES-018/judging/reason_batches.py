#!/usr/bin/env python3
"""Prepare a separate condition-hidden audit of reasons for frozen strictN probes."""
import argparse,hashlib,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def prepare():
 assert (ROOT/'judging/key.json').exists(),'Primary and secondary judging must finish before this follow-on reason audit'
 checks={q['qid']:q['checks'] for q in load('gold/checks.json')['questions']}
 source_options={r['id']:r for r in load('sources.json')['sources']}
 groups=[]
 for q in sorted(checks):
  eligible=[(i,c) for i,c in enumerate(checks[q]) if c['eligible_current_strict_N_denominator']]
  if not eligible:continue
  assert len(eligible)==1
  i,g=eligible[0];normalized={r['row_id']:r for r in load(f'judging/normalized/{q}.json')['rows']}
  rows=[]
  for cond in ['A','P']:
   rid='R'+hashlib.sha256(f'18018|{q}|{cond}|check|{i}'.encode()).hexdigest()[:16]
   rows.append(normalized[rid])
  random.Random(18018+len(groups)).shuffle(rows)
  official=list(g.get('official_evidence',[]))
  for sid in g.get('source_ids',[]):
   if sid in source_options:official.append({k:source_options[sid].get(k) for k in ['url','sections_read','confirmed','limits','accessed_at_utc']})
  groups.append({'qid':q,'question_input':f'judging/question-inputs/{q}.json','probe_name':g['name'],
                 'frozen_violation':g.get('violated_condition',g.get('required_condition')),
                 'frozen_explanation':g['reason'],'frozen_scope':g.get('scope',g.get('limits',g.get('limitations'))),
                 'frozen_official_observations':official,'rows':rows})
 random.Random(18018).shuffle(groups);manifest=[]
 for start in range(0,len(groups),4):
  n=start//4+1;selected=groups[start:start+4];inp=f'judging/reason-inputs/batch-{n:02d}.json';out=f'judging/reason-raw/batch-{n:02d}.json'
  save(inp,{'batch':n,'questions':selected,'output':out,
    'instructions':'Separate internal audit of the stated reason, with condition and keep/exclude decision hidden. Read only this packet, judging/RULES.md and its listed question inputs. The registered probe is a scoped near miss; the frozen explanation is a comparison target, not an instruction to agree. Check accessible current official documents. For each opaque row, determine whether its normalized reason correctly identifies an actual core violation of the question in the named version/configuration. Absence of support or generic caution alone is not a correct rejection reason. Mark incorrect for a wrong reason and unclear when evidence or normalization prevents deciding. Record any disagreement with the frozen violation separately. Do not infer A/P or read prior judgments/gold/keys/runs.',
    'reading_fields':['url','accessed_at_utc','title','version_or_date','sections_read','confirmed','limits','level'],
    'output_schema':{'judge':'actual internal auditor and model label','rows':[{'row_id':'opaque ID','verdict':'correct|incorrect|unclear','frozen_violation_supported':'true|false|unknown','reason':'reason assessment','evidence_urls':[],'checked_at_utc':'actual UTC','limitations':'scope and access limits'}],
                     'raw_response':'original assessment prose','readings':[],'excluded_readings':[],'queries':[]}})
  manifest.append({'batch':n,'input':inp,'output':out,'qids':[q['qid'] for q in selected],'row_ids':[r['row_id'] for q in selected for r in q['rows']]})
 save('judging/reason-manifest.json',manifest);print({'questions':len(groups),'rows':sum(len(x['row_ids']) for x in manifest),'batches':len(manifest)})
def combine():
 rows=[];seen=set()
 for b in load('judging/reason-manifest.json'):
  v=load(b['output']);assert v.get('judge') and v.get('raw_response')
  assert len(v['rows'])==len(b['row_ids']) and {r['row_id'] for r in v['rows']}==set(b['row_ids'])
  for r in v['rows']:
   assert r['row_id'] not in seen and r['verdict'] in ['correct','incorrect','unclear'];seen.add(r['row_id'])
   for f in ['frozen_violation_supported','reason','evidence_urls','checked_at_utc','limitations']:assert f in r
   rows.append({**r,'judge':v['judge'],'source_file':b['output']})
 expected=2*sum(c['eligible_current_strict_N_denominator'] for q in load('gold/checks.json')['questions'] for c in q['checks'])
 assert len(rows)==expected
 save('judging/reason-audit.json',{'rows':rows,'limits':'Independent internal reason matching after normalized blind relevance judgments. Frozen denominators are retained; disagreement with frozen truth is separately visible.'})
 print({'reason_rows':len(rows)})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--combine',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 if a.combine:combine()
