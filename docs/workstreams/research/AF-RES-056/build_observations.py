"""Build the post-ranking observation ledger from frozen slots and receipts.

No network calls. Empty slots never become invented trials. Reusing a stored
README in multiple trial paths is explicit; conjunction across paths is banned.
"""
from pathlib import Path
import csv,json
P=Path(__file__).resolve().parent
W=P/'evidence/windows'
SHA='d5199551f758ba067612979ae32ec35693640ccf'
BASE='https://github.com/pboettch/json-schema-validator/blob/'+SHA+'/'
def csvread(name):return list(csv.DictReader((P/name).open()))
def write(name,rows,fields=None):
 with (P/name).open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
def main():
 windows=[];judgments=[]
 fields=['window_id','comparison_id','case_id','method','slot','catalog_id','posted_rank','trial_id','action_index','trial_action_count','original_url','final_url','section_or_range','window_status','source_id','snapshot_sha_or_hash','same_trial','C1','C2','combined','note']
 originals={'WIN-01':'https://github.com/pboettch/json-schema-validator','WIN-02':'http://json-schema.org/','WIN-03':'http://json-schema.org/schema'}
 finals={'WIN-01':BASE+'README.md','WIN-02':'https://json-schema.org/','WIN-03':'https://json-schema.org/draft/2020-12/schema'}
 locations={'WIN-01':'README L3–106 / rendered500 words; v1 raw500=visible487 retained','WIN-02':'web L6–105 / rendered500 words; v1 raw500=visible479 retained','WIN-03':'JSON문서; 제목 기준 창 미확인'}
 digests={'WIN-01':SHA,'WIN-02':json.loads((P/'evidence/review/SC-032-home-rendered-window-v2.json').read_text())['v2_window_sha256_without_terminal_LF'],'WIN-03':'41da76f5afb7ce062d248f762463a92f7ca47e4e0f905b224ba6afeef91ded0f'}
 source_versions={'WIN-01':'WIN-01-V2','WIN-02':'WIN-02-V2','WIN-03':'WIN-03'}
 for s in csvread('slots.csv'):
  case,method,slot=s['case_id'],s['method'],s['slot'];cid=case+'-'+method;candidate=s['catalog_id']
  if not candidate:
   d=dict.fromkeys(fields,'');d.update(window_id=cid+'-EMPTY-'+slot,comparison_id=cid,case_id=case,method=method,slot=slot,window_status=s['status'],same_trial='해당 없음',C1='해당 없음',C2='해당 없음',combined='해당 없음',note='빈 매치45자리/후보풀소진2자리; 원문열람 실패와 구분');windows.append(d);continue
  assert cid=='JS-4-V' and candidate=='SC-032'
  for trial,sources in [('P1',['WIN-01']),('P2',['WIN-01','WIN-02']),('P3',['WIN-01','WIN-03'])]:
   trial_id=cid+'-'+trial
   for i,source in enumerate(sources,1):
    d=dict.fromkeys(fields,'');d.update(window_id=trial_id+'-A'+str(i),comparison_id=cid,case_id=case,method=method,slot=slot,catalog_id=candidate,posted_rank=s['original_rank'],trial_id=trial_id,action_index=i,trial_action_count=len(sources),original_url=originals[source],final_url=finals[source],section_or_range=locations[source],window_status='직접 열람/경계 확정 v2; 기계추출 사후 정정 공개' if source!='WIN-03' else '전송복구/제목없는 JSON 경계 미확인',source_id=source_versions[source],snapshot_sha_or_hash=digests[source],same_trial='yes; only within '+trial_id,C1='미확인',C2='미확인',combined='미확인',note='README fixed response reused across trials; no cross-trial conjunction; v1/v2 same outcome' if source=='WIN-01' else '표준/소개 문서; 구현판의 두 조건을 입증하지 않음');windows.append(d)
   judgments.append({'judgment_id':'J-'+trial_id,'comparison_id':cid,'case_id':case,'method':method,'catalog_id':candidate,'trial_id':trial_id,'C1_status':'미확인','C2_status':'미확인','same_implementation_version':'README '+SHA+('; 두번째 문서는 구현 아님' if len(sources)>1 else '; 두번째 동작 없음'),'environment':'후보C++ / 원문Python3; 교체가능성 명시없음','within_budget':('행동수2 준수; JSON창경계 미확인' if trial=='P3' else '행동수/렌더500단어 준수; 경계 사후 기계정정 공개'),'classification':'미확인','judgment_urls':' ; '.join(finals[x] for x in sources),'source_ids':';'.join(source_versions[x] for x in sources),'rationale':'일반 validation 설명만 있으며 동적 pii 제약과 datatype enum을 같은 창에서 함께 확인하지 못함; v1/v2 모두 같은 판정','not_claimed':'구현 전체에서 C1 또는 C2 불가능/번역의미오류라고 단정하지 않음'})
 for c in csvread('matches.csv'):
  if int(c['total_matches'])==0:
   judgments.append({'judgment_id':'J-'+c['comparison_id']+'-EMPTY','comparison_id':c['comparison_id'],'case_id':c['case_id'],'method':c['method'],'catalog_id':'','trial_id':'','C1_status':'해당 없음','C2_status':'해당 없음','same_implementation_version':'해당 없음','environment':'요구 환경 유지','within_budget':'해당 없음: 후보0','classification':'빈 반환','judgment_urls':'','source_ids':'','rationale':'고정 검색필드와 사전용어로 매치0; 실행/기능부재와 구분','not_claimed':'실제 구현 부재 또는 접근 실패가 아님'})
 ex=json.loads((W/'sc032-execution.json').read_text())
 assert ex['build_exit_code']==0 and ex['run_exit_code']==0
 judgments.append({'judgment_id':'J-JS4-DIAG-C2','comparison_id':'JS-4-V','case_id':'JS-4','method':'diagnostic','catalog_id':'SC-032','trial_id':'OUTSIDE-BUDGET','C1_status':'연구자가 작성한 C2-only schema에서 근접음성 수락; 전체 라이브러리 불가능 미입증','C2_status':'세 문자열 enum의 양성/근접음성 실행 확인','same_implementation_version':SHA+' build2.4.1 + nlohmann55f93686... v3.12.0','environment':'g++14.2.0 C++; original Python program 미실행','within_budget':'no','classification':'한 조건만(예산 밖 연구 fixture)','judgment_urls':BASE+'src/json-validator.cpp#L551-L560','source_ids':'WIN-06;EXEC-SC032','rationale':'string 허용,array 거절,존재하지 않는 pii는수락. 조건 하나를 전체요구로 올리는 추론의 반례','not_claimed':'원본문 프로그램/동적 C1/값존재 guard/허용창 완결을 입증하지 않음'})
 write('windows.csv',windows,fields);write('judgments.csv',judgments)
 assert len(windows)==52 and len(judgments)==19
 print(json.dumps({'window_rows':len(windows),'main_trials':3,'unique_main_representatives':1,'logical_actions':5,'unique_arrival_urls':3,'empty_slots':47,'judgment_rows':len(judgments)}))
if __name__=='__main__':main()
