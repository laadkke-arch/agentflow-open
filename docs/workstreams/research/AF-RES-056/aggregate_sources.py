"""Merge observation logs without counting sections, mirrors or failures as works."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,re
P=Path(__file__).resolve().parent
LEDGERS=['evidence/schema-pre/sources.jsonl','evidence/schema-pre/standard-sources.jsonl','evidence/ld-pre/sources.jsonl','evidence/catalog-pre/sources.jsonl','evidence/ld-tests/sources.jsonl','evidence/authority/sources.jsonl','evidence/windows/sources.jsonl','evidence/schema-diagnostics/sources.jsonl','evidence/ld-suppliers/sources.jsonl','evidence/inputs/sources.jsonl','evidence/review/sources.jsonl','evidence/review/source-audit-sources.jsonl']
REQUIRED=['source_id','work_id','자료종류','원본_URL','최종_URL','발행자','확인_UTC','판_또는_SHA','쪽_절_행_셀','관련_Q와_사례_ID','확인한_내용','확인범위와_한계','지지_또는_반증','직접열람_상태','중복_계보']
ALLOCATIONS={
 'questions':['SCH-Q05','SCH-Q07','SCH-Q08','SCH-Q09','LDQ-01','LDQ-03','LDQ-05','LDQ-07'],
 'catalogs_editorial':['CAT002','CAT006','CAT007','CAT010'],
 'standards_tests':['SCH-STD-VALID07','SD001','LD-STD-API','LD-TEST-01'],
 'suppliers':['SD009','SD014','LD-SUP-JS-DOC','LD-SUP-PY-DOC'],
 'authority_records':['AUTH-LC1','AUTH-LC2','AUTH-AAT1','AUTH-AAT2']}
def canonical(w):
 w=re.sub(r'^(?:stackoverflow|so)-question-','so-question-',w)
 if w in ('SCH-SUITE','JSON-SCHEMA-TEST-SUITE'):return 'JSON-SCHEMA-TEST-SUITE'
 if w.startswith('jsonldjs-'):return 'SUP-JSONLDJS'
 if w.startswith('pyld-'):return 'SUP-PYLD'
 if w.startswith('SUP-SC032'):return 'SUP-SC032'
 return w
def classify(r):
 state=str(r['직접열람_상태']).lower();kind=r['자료종류'];work=r['work_id'];sid=r['source_id']
 if '실패' in state or 'fail' in state or '접근 실패' in kind:return 'failed'
 if sid.startswith(('INPUT-','DEP052-','EXEC-')) or work.lower().startswith('af-res-056') or '실제 실행' in kind or '자체 실행' in kind:return 'internal_or_execution'
 if sid=='AUTH-LOC-PDF':return 'mirror_republication'
 if sid=='AUTH-GETTY-SOURCEREC' or 'synonyms' in work or 'ALIASES' in sid or 'metadata' in kind.lower() or '메타데이터' in kind or '재사용 허가' in kind or '라이선스' in kind or 'license' in kind.lower():return 'metadata_or_license'
 if r.get('primary_external') is False:return 'internal_or_execution'
 return 'direct_primary'
def main():
 rows=[];seen=set()
 for path in LEDGERS:
  for i,line in enumerate((P/path).read_text().splitlines(),1):
   r=json.loads(line);assert all(k in r for k in REQUIRED),(path,i,'missing fields')
   assert r['source_id'] not in seen,('duplicate source_id',r['source_id']);seen.add(r['source_id'])
   r['origin_ledger']=path;r['origin_line']=i
   old=r['work_id'];r['work_id']=canonical(old)
   if old!=r['work_id']:r['original_work_id']=old
   r['counting_class']=classify(r);r['required_allocation']=next((k for k,v in ALLOCATIONS.items() if r['source_id'] in v),'')
   if r['source_id']=='WIN-07':r['counting_class']='mirror_republication'
   rows.append(r)
 (P/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 byid={r['source_id']:(i,r) for i,r in enumerate(rows,1)};works=defaultdict(list)
 for i,r in enumerate(rows,1):
  if r['counting_class']=='direct_primary':works[r['work_id']].append((i,r))
 allocated=[];alloccounts={};already=set()
 for bucket,ids in ALLOCATIONS.items():
  selected=[]
  for id in ids:
   line,r=byid[id];assert r['counting_class']=='direct_primary',(id,r['counting_class'])
   assert r['work_id'] not in already,('duplicate allocated work',r['work_id']);already.add(r['work_id'])
   selected.append({'source_id':id,'work_id':r['work_id'],'sources_line':line,'url':r['원본_URL'],'location':r['쪽_절_행_셀']})
  alloccounts[bucket]={'required':len(ids),'obtained':len(selected),'unit':'unique primary works','status':'met','works':selected};allocated.extend(selected)
 counts={'observation_rows':len(rows),'row_classes':dict(Counter(r['counting_class'] for r in rows)),'unique_direct_primary_works':len(works),'required_primary_works':24,'allocated_unique_primary_works':len(already),'allocations':alloccounts,'counting_rules':['question IDs identify author works even when batched API transport','same manual/implementation/test-harness/release family conservatively merged for supplier unique counts','Schema core and validation each merge draft variants','W3C suite mirrors/version copies share work_id','catalog data+renderer one work; standalone data contract and submission form separate editorial works','LOC annual PDF and Getty bibliographic record are not extra concept works','failures/search/metadata/internal receipts excluded from unique primary minimum'],'remaining_gaps':['historical tag alias/deleted/retagged population reconstruction unconfirmed','source quota does not imply same-window implementation completeness','source metadata location correction recorded in SCOPE and SCH-STD-VALID20-RECHECK']}
 assert len(already)==24
 (P/'evidence/source-counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
 with (P/'evidence/primary-works.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['work_id','representative_source_id','representative_url','sources_lines','source_ids','required_allocation'],lineterminator='\n');writer.writeheader()
  for work,items in sorted(works.items()):
   first=items[0][1];writer.writerow({'work_id':work,'representative_source_id':first['source_id'],'representative_url':first['원본_URL'],'sources_lines':';'.join(str(i) for i,r in items),'source_ids':';'.join(r['source_id'] for i,r in items),'required_allocation':next((r['required_allocation'] for i,r in items if r['required_allocation']),'')})
 print(json.dumps({k:counts[k] for k in ['observation_rows','row_classes','unique_direct_primary_works','allocated_unique_primary_works']},ensure_ascii=False))
if __name__=='__main__':main()
