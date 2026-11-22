from pathlib import Path
import json,csv

P=Path(__file__).resolve().parents[1]
events=[json.loads(z) for z in (P/'events.jsonl').read_text().splitlines() if z.strip()]
def val(x):return x if isinstance(x,str) else json.dumps(x,ensure_ascii=False)
fields=['event_id','system','original_url','catalog_entity','work_recording_release_or_real_object','organization_department','project_distribution_version','function','use_substitutability','editor_reason','opposing_reason','original_external_id_target','source_ids','unverified']
with (P/'identity-layers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for e in events:
  if not e['primary_sample']:continue
  a=e['identity_layers']
  row=dict(event_id=e['event_id'],system=e['system'],original_url=a.get('url',a.get('original_url','미확인')),catalog_entity=a.get('catalog_entity','미확인'),work_recording_release_or_real_object=a.get('work_recording_release',a.get('real_object','해당 없음')),organization_department=a.get('legal_org_vs_department','해당 없음'),project_distribution_version=a.get('project_distribution_version','해당 없음'),function=a.get('function',e.get('required_function_version',e.get('old_reference_use','자료의 사용 목적 열 참조'))),use_substitutability=a.get('use_substitutability','미확인'),editor_reason=e.get('editor_reason','미확인'),opposing_reason=e.get('opposing_reason','미확인'),original_external_id_target=a.get('external_id_target',a.get('external_identifier',e.get('external_ids','고정 archive/recipe는 사건 원장 참조; 별도 발급기관 원문 미검증'))),source_ids=e['source_ids'],unverified=e.get('unknowns',[]))
  w.writerow({k:val(v) for k,v in row.items()})
with (P/'restoration.csv').open('w',newline='') as f:
 fields=['event_id','dimension','record_based_assessment','source_ids','automatic_restoration_execution_verified','interpretation_limit']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for e in events:
  if not e['primary_sample']:continue
  for dim in ['labels','external_ids','citations','version','multiple_successors']:
   w.writerow(dict(event_id=e['event_id'],dimension=dim,record_based_assessment=val(e.get('restoration',{}).get(dim,'UNVERIFIED_RECORD')),source_ids=val(e['source_ids']),automatic_restoration_execution_verified=False,interpretation_limit='AUTO/auto는 보존된 필드의 추출 가능성에 대한 해석. 자동 복원 실행/모든 소비자 이관 성공 아님. 접근 실패·관계 미기록·실제 손실을 구별.'))
print('18 independent identity rows; 90 attribute restoration rows')
