"""Make one source ledger with explicit, conservative lineage counts."""
from pathlib import Path
import json,re,datetime
P=Path(__file__).resolve().parent
def rows(p):return [json.loads(x)for x in p.read_text().splitlines()if x.strip()]
out=[];seen=set()
files=sorted(f for f in (P/'streams').rglob('*sources*.jsonl')if '.workbench'not in f.parts)
for f in files:
 for r in rows(f):
  sid=r.get('source_id',r.get('id'))
  if not sid:raise ValueError(f'no source id:{f}')
  if sid in seen:raise ValueError(f'duplicate source id:{sid}')
  seen.add(sid)
  typ=r.get('source_type',r.get('material_type',r.get('source_kind',r.get('type',''))))
  count=any(r.get(k)is True for k in ['countable','count_as_independent_work','counts_as_independent_work','counts_minimum'])
  opened=r.get('opened_utc',r.get('directly_opened_utc',r.get('checked_utc')))
  direct=r.get('directly_read',bool(opened))
  downstream=(r.get('downstream_original',False)or r.get('downstream_authored_work',False)or bool(re.search(r'consumer|downstream',typ,re.I)))
  guide=downstream and bool(re.search(r'guide|tutorial|example|manual',typ,re.I))
  n={'source_id':sid,'lineage_id':r.get('lineage_id',r.get('independent_work_id')),'source_type':typ,'url':r.get('url',r.get('original_url')),'fixed_version':r.get('fixed_version',r.get('commit',r.get('tag',r.get('edition','retrieval snapshot')))),'location':r.get('location',r.get('section',r.get('path',''))),'lines':r.get('lines'),'opened_utc':opened,'questions':r.get('questions',r.get('related_questions',[])),'cases':r.get('cases',r.get('case_ids',[])),'observed':r.get('observed',r.get('confirmed',r.get('finding',''))),'limitations':r.get('limitations',r.get('limits',r.get('limits_unknowns',r.get('limitation','')))),'supports_or_refutes':r.get('supports_or_refutes',r.get('claim_relation',{'supports':r.get('supports',[]),'refutes':r.get('refutes',[])})),'directly_read':direct,'countable':count and direct,'count_reason':r.get('count_reason',r.get('countable_reason','같은 lineage_id는 한 번만 산입. source 원장의 산입 flag를 보존.')),'downstream_authored':downstream,'downstream_guide':guide,'sha256':r.get('sha256',r.get('content_sha256')),'stream_file':str(f.relative_to(P)),'historical_http_arrival':r.get('historical_arrival',r.get('history_http_arrival',r.get('historical_http_destination','역사적 도착 미확인')))}
  for k in ['opened_utc_precision','read_utc','visual_read_utc','hash_acquired_utc','read_again_utc','acquired_utc','sealed_before_acquisition_commit','section_sha256','snapshot_path','bytes','web_ref','repository','tag','commit']:
   if k in r:n[k]=r[k]
  n.setdefault('opened_utc_precision','원 스트림에 기록된 열람 시각; 추가 정밀도 주장 없음')
  n['direct_read_utc']=r.get('read_utc',r.get('visual_read_utc',r.get('directly_opened_utc',opened)))
  n['time_field_note']='opened_utc는 원 스트림의 최초 열기/취득 시각일 수 있음. 별도 read_utc 또는 visual_read_utc가 있으면 direct_read_utc에 보존. UTC 상한 precision은 exact second로 승격하지 않음.'
  if not n['fixed_version']:
   n['fixed_version']='retrieval snapshot at '+str(opened)+'; original issue/comment has no commit pin'
  correction_file=P/'streams/gis/postseal/corrections.jsonl'
  if correction_file.exists():
   corrections=[c for c in rows(correction_file)if c.get('row_id')==sid]
   if corrections:n['postseal_corrections']=corrections
  out.append(n)
(P/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n'for r in out))
attempt=[]
for f in sorted((P/'streams').rglob('*attempts*.jsonl')):
 if '.workbench'in f.parts:continue
 for r in rows(f):r['stream_file']=str(f.relative_to(P));r['counts_minimum']=False;attempt.append(r)
(P/'attempts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n'for r in attempt))
works={r['lineage_id']for r in out if r['countable']}
strict={r['lineage_id']for r in out if r['countable']and not re.search(r'implementation|test|packag|build|ci.config|environment|dependenc|metadata|receipt',r['source_type'],re.I)}
guides={r['lineage_id']for r in out if r['countable']and r['downstream_guide']}
summary={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'direct_source_rows':len(out),'countable_independent_lineages':len(works),'countable_lineage_ids':sorted(works),'strict_lineages_excluding_implementation_test_config':len(strict),'strict_lineage_ids':sorted(strict),'downstream_guide_lineages':len(guides),'downstream_guide_ids':sorted(guides),'attempt_rows_excluded':len(attempt),'threshold_independent_works':20,'threshold_downstream_originals':6,'source_count_is_not_core_sample_count':True}
(P/'evidence/source-counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
