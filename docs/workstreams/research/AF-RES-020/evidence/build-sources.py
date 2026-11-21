"""Merge source ledgers without counting duplicate fixed files as new readings."""
import json,collections,urllib.parse,subprocess,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def read(n):return json.loads((P/n).read_text())
def write(n,o):(P/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
fixed=read('evidence/fixed-inputs.json')
gov=[]
items=[('AGENTS.md','전체','역할·작업 경로와 세션 계약 검사 규칙을 읽었다.'),('STATE.md','전체','foundation 당시 작업 공간과 상태 설명을 확인했다. 미배정 문구로 현 배정을 취소하지 않았다.'),('docs/DOT_AUTOMATION.md','작업 진행·인수·브랜치 규칙','진행표 갱신은 진행 담당 책임이며 작업자의 owned_path 제한과 인수 근거를 확인했다.'),('docs/RESEARCH_WORKFLOW.md','특히 §4–5; 전체 규칙','연구 묶음 8항목, 근거와 가설의 구별, 색인·인계의 역할을 확인했다.'),('docs/product/RESEARCH_BRIEF.md','8개 브리프 질문·제약','scope·identity·storage·retrieval·input·maintenance·evaluation·assembly의 질문 범위를 확인했다.'),('docs/research/INDEX.md','현재 색인 전체','공통 색인을 직접 고치지 않고 고정 결과 링크와 행 추가 제안을 만들기 위한 열 구조를 확인했다.'),('docs/automation/dot-control.json','AF-RES-020 및 depends_on 12항목의 상태·result_commit; 관련 policy 필드만','020의 고정 의존 결과와 운영 상태·인수 근거 정책을 확인했다. 다른 새 연구의 결과 본문은 읽지 않았다.')]
for i,(path,sections,confirmed) in enumerate(items,1):
 sha=fixed['source_commit'];b=subprocess.check_output(['git','show',sha+':'+path]);gov.append({'id':f'G{i:02d}','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{sha}/{path}','accessed_at_utc':'2026-11-21','access_time_precision':'UTC 일자; 시작 단계 직접 열람, 현재 해시 재확인','source_type':'internal_governance','title':path,'version_or_date':sha,'sections_read':sections,'confirmed':confirmed,'limits':'운영 계약·당시 상태이며 연구의 경험적 성능 근거가 아니다. 이후 브랜치 상태를 대신하지 않는다.','level':'D1','used_in':['Q1','Q6','Q7'],'access_method':'git show '+sha+':'+path,'content_sha256':hashlib.sha256(b).hexdigest()})
for i,name in enumerate(['REVIEW-2.md','REVIEW-3.md','REVIEW-4.md'],8):
 path='docs/workstreams/planning/'+name;sha=fixed['planning_commit'];b=subprocess.check_output(['git','show',sha+':'+path]);gov.append({'id':f'G{i:02d}','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{sha}/{path}','accessed_at_utc':'2026-11-21','source_type':'internal_planning_review','title':name,'version_or_date':sha,'sections_read':'전체; REVIEW-4 §3의11지점과§4–6 인계·색인 상태','confirmed':'충돌 후보와 통합·인계의 빈칸을 찾는 출발점으로 사용했다. 수치와 원 주장의 사실 근거는 별도로 고정 원 결과를 열었다.','limits':'계획 검토의 요약은 원 연구의 대체 근거가 아니다. 계획 권고를 실제 효과로 인용하지 않는다.','level':'D1','used_in':['Q1','Q3','Q4','Q6','Q7'],'access_method':'git show '+sha+':'+path,'content_sha256':hashlib.sha256(b).hexdigest()})
write('evidence/sources-governance.json',{'sources':gov,'excluded':[]})
all_sources=[];excluded=[]
for part in ['early','late','root','governance','external']:
 d=read(f'evidence/sources-{part}.json')
 for s in d['sources']:
  s=dict(s)
  if s['url'].split('#')[0].endswith('.py'):
   s['level']='D2';s['level_note']='고정 판 코드 본문 대조; 원 실행을 재수행했다는 뜻은 아님';s['source_type']='internal_fixed_code'
  all_sources.append(s)
 excluded.extend(d['excluded'])
ids=[s['id'] for s in all_sources];assert len(ids)==len(set(ids))
required=['id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in']
for s in all_sources+excluded:assert all(k in s and s[k] not in ['',None,[]] for k in required),s['id']
# Site domains: Amazon investor-relations CDN is the same institution for this cap.
def site(s):
 h=urllib.parse.urlsplit(s['url']).hostname.removeprefix('www.')
 return 'amazon.com + investor-relations CDN' if h in ['aboutamazon.com','s2.q4cdn.com'] else h
external=[s for s in all_sources if s['id'].startswith('X')];counts=collections.Counter(site(s) for s in external);assert max(counts.values())<=3
internals=[s for s in all_sources if s['source_type'] in ['internal_result','internal_evidence','internal_fixed_code']]
unique={(s['version_or_date'],s['url'].split('#')[0].split('/blob/')[-1]) for s in internals}
orig_tasks=sorted({s['url'].split('/research/')[1].split('/')[0] for s in internals})
required_files={
'001':['HANDOFF.md','RESEARCH.md'],'002':['HANDOFF.md','RESEARCH.md'],'003':['HANDOFF.md','RESEARCH.md'],'004':['HANDOFF.md','PROTOCOL.md'],'009':['HANDOFF.md','GAP.md','LANDSCAPE.md'],'010':['HANDOFF.md','REPRESENTATIONS.md','TRANSFER_CASES.md'],'011':['HANDOFF.md','CODEBOOK.md','CASES.json'],'012':['HANDOFF.md','RESULTS.md'],'013':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'014':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'015':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'016':['HANDOFF.md','RESULT.md','VOCAB_MAP.md','evidence/vocab-map-data.json','CODEBOOK.md']}
missing=[]
for t,files in required_files.items():
 for f in files:
  path=f'docs/workstreams/research/AF-RES-{t}/{f}';sha=fixed['fixed']['AF-RES-'+t]
  if not any(s['version_or_date']==sha and s['url'].split('#')[0].endswith('/'+path) for s in internals):missing.append(path)
assert not missing,missing
categories=collections.defaultdict(list)
for s in external:
 for c in s.get('method_categories',[]):categories[c].append(s['id'])
summary={'source_records':len(all_sources),'unique_fixed_original_files':len(unique),'original_tasks':orig_tasks,'required_primary_files':sum(map(len,required_files.values())),'required_primary_missing':missing,'external_primary_bodies':len(external),'external_conservative_lineages':20,'external_site_counts':dict(counts),'external_categories':dict(categories),'excluded':len(excluded),'duplicate_rule':'동일 SHA/경로의 반복 읽기 항목은 문서 수에 다시 넣지 않는다. 외부 문헌·작업 원자료·운영 문서 수는 합쳐 최소20을 채우지 않는다.','interpretation':'24개 원문은24회 독립 효과 검증이 아니며 이 계보를 보수적으로 묶어도20문헌군. 접근 실패·D0는 제외.'}
write('sources.json',{'schema_version':'1.0','summary':summary,'sources':all_sources,'excluded':excluded})
write('evidence/source-audit.json',summary)
print(json.dumps(summary,ensure_ascii=False))
