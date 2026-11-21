#!/usr/bin/env python3
"""Describe observable treatment-record adherence without repairing frozen runs."""
import argparse,collections,json
from common import ROOT,load,save
def retrieval_records(value,path=''):
 out=[]
 if isinstance(value,dict):
  if '--emit ' in str(value.get('command','')):
   out.append({'field_path':path,'command':value['command'],'status':value.get('status'),
               'recorded_hashes':{k:v for k,v in value.items() if 'sha256' in k.lower()},
               'recorded_times':{k:v for k,v in value.items() if k.endswith('_utc')}})
  for k,v in value.items():out.extend(retrieval_records(v,path+'.'+k))
 elif isinstance(value,list):
  for i,v in enumerate(value):out.extend(retrieval_records(v,path+f'[{i}]'))
 return out
def main(partial=False):
 meta={q['id']:q for q in load('questions/metadata.json')};rows=[]
 for d in load('questions/dispatch.json')['order']:
  r=load(d['output'])
  if not r or len(r.get('checks',[]))!=3:
   if partial:continue
   raise AssertionError(('incomplete run',d['output']))
  q,c=d['qid'],d['condition'];issues=[];serialized=json.dumps(r,ensure_ascii=False)
  record={'condition':c,'qid':q,'source_file':d['output'],'input_mode':meta[q]['input_mode'],
          'frozen_question_hash_occurs_in_record':meta[q]['sha256'] in serialized,
          'original_retrieval_assertions':retrieval_records(r),
          'code_search_record_fields':[k for k in r if 'code' in k.lower()],
          'query_document_records':len(r['queries'])+len(r['opened_documents'])}
  if c=='P':
   decomp=r.get('decomposition',[])
   if not isinstance(decomp,list):issues.append('Decomposition is not the specified list');decomp=[]
   items={v.get('item') for v in decomp};missing=sorted({'I'+str(i) for i in range(1,9)}-items)
   if missing:issues.append('Missing decomposition items '+','.join(missing))
   missing_locations=[i for i,x in enumerate(decomp) if not x.get('source_location')]
   if missing_locations:issues.append('Missing source locations '+str(missing_locations))
   fields=['form','contribution','must_checks','L','E','H','T','label']
   missing_fields=[{'rank':x['rank'],'fields':[f for f in fields if f not in x]} for x in r['candidates']]
   missing_fields=[v for v in missing_fields if v['fields']]
   if missing_fields:issues.append('Candidate fields absent: '+json.dumps(missing_fields))
   mismatches=[x['rank'] for x in r['candidates'] if x.get('label')=='SURFACE_OR_CONSTRAINT_MISMATCH']
   record.update(decomposition_items=sorted(v for v in items if v),decomposition_rows=len(decomp),
                 candidate_field_coverage=len(r['candidates'])-len(missing_fields),candidate_count=len(r['candidates']),
                 returned_mismatch_label_ranks=mismatches,
                 declared_labels=dict(collections.Counter(x.get('label','missing') for x in r['candidates'])))
  record['structural_issues']=issues;rows.append(record)
 report={'runs':len(rows),'P_runs':sum(r['condition']=='P' for r in rows),'rows':rows,
         'limits':'Presence of fields and self-recorded retrieval hashes is not proof of semantic correctness, complete network instrumentation, or OS-isolated context. No frozen answer is repaired by this audit. Missing hashes require record review and are not automatically treated as retrieval failures.'}
 if not partial:save('analysis/protocol-audit.json',report)
 print(json.dumps({'runs':len(rows),'P_runs':report['P_runs'],'structural_issues':[r for r in rows if r['structural_issues']],
                   'original_inputs_without_hash_in_run':[r['source_file'] for r in rows if r['input_mode']=='original' and not r['frozen_question_hash_occurs_in_record']]},ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();main(a.partial)
