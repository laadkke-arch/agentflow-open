"""Apply the independent post-adjudication review; sealed A files are untouched."""
import json,pathlib
P=pathlib.Path(__file__).resolve().parent
post=json.loads((P/'post.json').read_text());r=next(x for x in post if x['number']==4911)
r.update({'B_status':'data_ambiguous','B_value':None,'B_value_display':'첫 OP 댓글이 전송 진행 중과 중단 뒤 메모리를 모두 기술하여, 봉인 질문의 특정 관측시점 Boolean으로 고정할 수 없음','B_exact_original_value_time':'unknown; edited comment contains multiple observation stages','advice_B':'한 값의 B를 구성할 수 없어 봉인한 두 조건부 후보를 유지. 개별 버퍼 사용 종료와 모든 전송 완료는 같은 조건이 아니므로 mmap 절로 선택의 정오를 판정하지 않음.','post_adjudication_A_field_already_present':None,'A_pre_vs_post_disagreement':'첫 사후판정은 A의 전송 중 표현만으로 이미 답이 있다고 보아 FP=1로 세었으나, 교차검토가 특정 관측시점 및 버퍼/전체전송 단위 불일치를 지적하여 판정불가로 낮춤. 봉인 A는 수정하지 않음.','independent_correctness':'unknown: RCL-D1의 조건은 개별 transfer buffer가 더는 쓰이지 않는 시점이며, 선정 필드인 모든 전송 완료 여부와 동치가 아님','false_positive_adjudicable':False,'false_positive':None,'false_positive_reason':'A에 전송 중 문맥은 있지만 선정한 특정 관측시점의 전체전송 종료 여부까지 독립적으로 고정되지 않음. 두 Boolean값에서 권고가 같은지도 판별절로 입증되지 않음.','strict_effect_exclusion':'사전 문서 노출 예산 이탈 + 실제 설치판 조건부 + 단일 B값 불확정 + 판별조건 단위 불일치','diagnostic_false_positive_denominator':False,'audit_review':'ripgrep 담당 교차검토 수용; 기존 FP1/1 주장 철회','initial_post_decision_superseded':'redundant_value_not_new; diagnostic FP1/1; 현재 원장에서는 사용하지 않음'})
(P/'post.json').write_text(json.dumps(post,ensure_ascii=False,indent=2))
out=json.loads((P/'outcomes.json').read_text());o=next(x for x in out if x['outcome_id']=='RCL-4911-O1');o.update({'B_status':'data_ambiguous','recommendation_change':'unobservable','apparent_uncertainty_resolution':None,'diagnostic_false_positive_denominator':False,'false_positive':None,'exclusion_reason':r['strict_effect_exclusion'],'post_review_note':'첫 사후 FP1/1 판단 철회; 특정 관측시점 불확정 및 개별버퍼/전체전송 조건 불일치'})
cf=next(x for x in out if x['outcome_id']=='RCL-4911-CF1');cf['counterfactual_validity']='unknown; 개별버퍼 종료와 전체전송 종료의 동치가 입증되지 않음'
(P/'outcomes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
events=json.loads((P/'events.json').read_text());e=next(x for x in events if x['event_id']=='RCL-4911-C756886973');e['selected_field_relation']='first_same_author_candidate_temporally_ambiguous';e['summary']='OP가 단일전송·진행 중 상승·중단 뒤 잔류·힙 프로파일을 한 응답에 보고. 특정 관측시점을 고정할 수 없어 Boolean B를 넣지 않음.'
(P/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
s=(P/'counterexamples.md').read_text()
if '## 가장 강한 반례:' in s:
 a=s.index('## 가장 강한 반례:');b=s.index('## 값 하나가 알려져도',a)
 replacement='''## 교차검토로 낮춘 판정: 전송 중 문맥과 특정 관측시점은 다르다

사전 교대 순위1인 #4911에서 연구자는 높은 메모리를 본 순간 모든 전송이 끝났는지 묻는 필드를 봉인했다. 복구된 최초글 L2-L3에는 전송 중의 높은 메모리·할당 오류가 쓰여 있다. 첫 사후판정은 이것만으로 A에 답이 이미 있었다고 보고 오탐1/1을 제시했다. 그러나 교차검토에서 이 표현은 증상의 전송 중 문맥을 주지만, 봉인한 질문이 가리키는 특정 관측시점의 전체전송 종료 여부까지 고정하지 않는다는 문제가 확인됐다. 첫 OP 댓글도 진행 중 상승과 중단 뒤 잔류를 함께 기술한다. 어느 하나만 골라 Boolean값을 넣으면 시간 맥락을 연구자가 더하게 된다.

또한 RCL-D1의 --use-mmap 절은 개별 전송 버퍼가 더는 쓰이지 않을 때 OS로 반환될 수 있다고 설명한다. 이는 모든 전송이 완료됐는지라는 필드와 동치가 아니다. 따라서 새 B는 data_ambiguous, 오탐은 판정불가로 낮추고 오탐 분모에서 제외한다. 엄격층과 진단층 모두 이 행에서 판정 가능한 오탐 분모가0이므로 N/A이며, 오탐0건을 실측한 것이 아니다. A에 있던 맥락을 연구자가 놓쳤을 가능성은 남지만, 그 가능성을 확정 오탐으로 바꾸지 않는다. 봉인 A는 수정하지 않았다.

'''
 (P/'counterexamples.md').write_text(s[:a]+replacement+s[b:])
