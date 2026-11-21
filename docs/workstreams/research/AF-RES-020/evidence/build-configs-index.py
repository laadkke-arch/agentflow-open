"""Render assembly choices and index proposals; does not select or apply a design."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def read(n):return json.loads((P/n).read_text())
def write(n,o):(P/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def cell(x):return str(x).replace('|','\\|').replace('\n',' ')
def table(h,rr):return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(cell(x) for x in r)+' |' for r in rr])
cfg=read('evidence/configs-data.json')
for c in cfg:
 c['evidence_level']='H — 선택 가능한 시작 구성; 효과·최종 설계 미선정'
 c['adoption_modes']={b:'기능·평가 또는 보존 원칙 채택' for b in c['included_bundles']}
 if c['id'] in ['C0','C1']:
  c['included_bundles']=sorted(set(c['included_bundles']+['B06']))
  c['adoption_modes']['B06']='정의 계약만: 좁은 주장·주어/배포/판·극성/수식·근거 위치를 요청별 판정에 연결; 자체 후보 자료집·전역 주장 원장 미도입'
 if c['id']=='C0':
  c['day_one_preserve']='원 질문·선택 범위·필수/선호, 실제 질의와 변환 판, 후보 원 URL/도착 URL, 좁은 주장과 주어·배포/판·부정/제외 범위, 원문 위치·불변 판(있을 때)·25단어 이하 인용·확인 시각, proposed_use·설정, 원 E/H/T 판정·판정자·규칙 판·이유, 거절·미판정·검색 실패. 요청별 검토 기록으로 보존.'
  c['conditional_feature_policy']='B12 역할 분류를 추가하지 않는 현재 C0에서는 역할별 성능 층화를 하지 않는다. B14는 전체 범위 판정원 민감도만 본다. 역할별 지표를 켜려면 B12 원 라벨·형태/기여 대상·판정자·코드북 판을 먼저 보존한다.'
 elif c['id']=='C1':
  c['day_one_preserve']='C0의 원 E/H/T·판정자·규칙 판을 포함한 요청 기록에 더해 원 링크/fragment, 대상 범위·배포·버전, 원 설명과 수정 이력, form 원판정·코드북 판·이견, 별칭/병합 전 ID. contribution은 원 질문의 선택 범위×답/제안×후보/사용에 연결하며 단일 후보 속성으로 덮지 않음.'
  c['conditional_feature_policy']='B06의 의미 계약은 카드의 좁은 조건 메모와 요청별 판정 기록으로 충족한다. 독립 주장 정정이 반복될 때만 C2 방식의 관리로 확대한다. 역할별 지표는 B12 코딩 전제를 충족하는 관측에 한정한다.'
 else:
  c['included_bundles']=sorted(set(c['included_bundles']+['B11']))
  c['adoption_modes']['B11']='정의·관측 계약: 질문 선택 범위와 답/제안 단위 보존. 실제 답 gold를 쓸 때만 accepted·사용 보고·통합 성공 사건을 분리; 011 자료집의 상시 수집을 의미하지 않음'
  c['day_one_preserve']='원 질문 위치/판·선택 범위와 실제 검색 입력·변환 판, 원 설명·부정/수식어, 주장과 근거 위치/판/확인시각·적용시점, 추출·판정 규칙 판·작성자·원 E/H/T/미확인, form 대상 배포물/문서 판, contribution의 원 질문×답/제안×후보/사용 연결과 원 라벨·코더, 정정·제외 전후 기록. 실제 답을 쓰면 답 위치/관측시각과 accepted·사용·통합을 분리.'
  c['failure_signals']=c['failure_signals'].replace('주장 분해 자체가 부정 범위를 오독(C02)','주장 분해 자체가 부정 범위를 오독(B06의 managed backups 반례)')
  c['conditional_feature_policy']='B11의 질문·제안 단위는 B12/B23의 전제다. 실제 답 기준 평가를 하지 않으면 B11→B14의 반응 자료 경로는 꺼 두고 문서 근거 판정만 보고한다. 과거 원 질문 판을 못 얻었으면 unknown을 유지한다.'
write('evidence/configs-data.json',cfg)
headers=['구성','포함 묶음','첫날부터 보존할 자료','되돌리기 어려운 결정','실패 신호','다른 구성으로의 이행 경로','주요 비용','미확인']
def included(c):return ', '.join(b+(' (정의 계약)' if '정의' in c['adoption_modes'].get(b,'') else '') for b in c['included_bundles'])
rows=[[c['id']+' '+c['name'],included(c),c['day_one_preserve'],c['hard_to_reverse'],c['failure_signals'],c['migration_path'],c['major_costs'],c['unknowns']] for c in cfg]
s='''# 시작 구성안 — 최종 선택 없음

## 1. 비교 단위

세 구성은 서로 다른 비용 지불 시점을 갖는다. C0는 요청마다 검증하고, C1은 재방문 설명을 미리 만들며, C2는 반복 정정·재사용할 주장과 판단을 관리한다. 같은 제품의 필수 발전 단계로 두지 않는다. 003 RESEARCH §1·§6(B05/B06/B20), 009 GAP §3·§5(B09/B10), 004 PROTOCOL L24–46(B07)이 내부 근거다. 구체 조합·이행 경로는 이번 작업자의 H다. 외부에서는 X01·X02의 학습에 따른 대안 축소, X03의 같은 예산 비교, X07의 실제 교체 권리·비용, X18·X23의 대안 유지 비용·가역성을 비교했다([CROSSFIELD](CROSSFIELD.md)).

## 2. 구성 비교

‘정의 계약’은 해당 묶음에서 판단에 필요한 의미만 채택하는 것이다. 전체 저장·수집 구현을 도입하는 것과 다르다. 이렇게 표시해야 가벼운 구성이 숨은 의존을 감추지 않는다.

'''+table(headers,rows)+'\n'
for c in cfg:
 s+=f"\n### {c['id']} — {c['name']}\n\n{c['principle']}\n\n**맞는 조건:** {c['appropriate_conditions']}\n\n**조건부 기능 경계:** {c['conditional_feature_policy']}\n"
s+='''
## 3. 공통 보존 의미와 숨은 전제의 충족

원 질문 → 실제 검색 입력 → 후보 원 위치 → 검토한 좁은 주장·근거 위치/판 → 제안한 사용·설정 → 원 E/H/T 판정·판정자·규칙 판·이유의 연결을 남긴다. 이는 요청별 짧은 기록으로도 표현할 수 있다. 원 문장의 부정과 제외 범위를 독립 필드로 만들지 않더라도, 나중 읽는 사람이 복원할 수 있게 원 위치와 의미를 함께 보존해야 한다.

| 경로 | C0 | C1 | C2 |
| --- | --- | --- | --- |
| B06→B07 주장 범위·근거 | 요청별 기록의 좁은 주장·E/H/T | 카드의 조건 메모와 요청별 기록 연결 | 주장·근거·판정 행 연결 |
| B11→B12 선택 범위·제안 단위 | 역할 층화 기능 보류 | 원 질문×답/제안×후보/사용에 contribution 연결 | 같은 연결과 형태 대상 판을 별도 보존 |
| B12→B14 역할 지표 | B12 없을 때 전체 지표만; 역할별 지표 보류 | 원 코드북·코더·라벨이 있는 층만 | 코더·코드북·원 라벨을 보존한 층만 |
| B11→B14 실제 답 gold | 실제 답을 쓰면 accepted/사용/통합 분리 | 같은 관측 계약 | 실제 답을 쓰지 않으면 이 경로 비활성; 문서 판정만 |
| B11→B23 질문 변환 | 선택 범위·원문/요약·변환 판·실제 입력 | 동일 + 카드/요청 연결 | 동일 + 근거 판·답 반응 출처 |

별도 모델 `gpt-6.2-sol`이 초기 구성의 누락을 지적했고 위 의미 계약으로 보강했다([검토 원문](evidence/internal-review-sol.md)). 특정 묶음 전체를 넣지 않는 것과 그 묶음이 드러낸 정의를 없애는 것을 구별했다. 제품 성능을 별도 모델이 승인했다는 뜻은 아니다.

확인 시각만으로 과거 live 문서를 복원할 수 없다(B05,003 RESEARCH §5 L107–111). 결정에 중요한 조건은 불변 판 위치를 우선하고, 없으면 25단어 이하 인용·적용 범위·확인 시각을 함께 남긴다. 이것으로 원문의 모든 문맥을 복구할 수는 없다. 전문 보관은 이번 범위 밖이며 공개 권한·후속 보존 계약을 따로 검토한다.

**작아 보이는 비가역 결정의 반례:** C1의 단일 role이 형태와 기여를 압축하고 원 판정 근거를 버리면 이후 두 축으로 분리해도 잃은 해석은 복원되지 않는다. 원 라벨과 사용 문맥이 따로 있으면 단일 표시 필드 자체가 비가역적인 것은 아니다. C2에서도 managed backups 미제공을 backup 없음으로 분해하면 구조화가 의미를 손상한다. C0에서 거절 후보·검색 실패 기록을 버리면 이후 누락과 도구 실패를 구별할 수 없다. 원 결과는 이 정보 손실 경로를 지지하지만 실제 이행 비용을 측정한 것은 아니다.

## 4. 대안을 닫는 조건

기각은 동일 질문·예산·근거 범위에서 확인한다. H1의 탐색/검토 가치, H2의 변경 후 재검토 가치, 원거리 원리의 적용 가치를 따로 비교한다. 각 구성의 실패 신호와 DECISIONS의 최소 증거가 축소·보류의 입력이다. 추가 자료집 관리가 검토를 줄이지 못하면 C1/C2를 축소할 수 있고, 반복 재검토가 지배 비용이면 C0만으로 충분하다는 가정을 다시 연다. AF-RES-017~019는 대기 중인 입력으로만 두고 읽지 않았다.

보관된 대안과 활성 개발 중인 대안도 구별한다. 원 결정·기각 근거를 보관하는 일은 모든 대안을 동시에 개발하는 일과 다른 비용을 가진다. QOC 실제 팀 연구(X11), 옵션 유지 실험(X18), 변경 가능 결과의 만족 비용(X19)은 장기 보류가 공짜라는 가정을 반박한다. 세 구성을 동시에 구현하거나 어느 한 구성을 최종 추천하지 않는다.

## 한계

구성의 적합 조건·이행 경로는 H이며 구현·사용자 시험을 수행하지 않았다. 013은 기준선만, 012·014는 고정 자료집 내부 검색 변형을 비교했다. 실제 비용 우위·검토 부담·판정 개선은 해당 최소 비교를 수행해야 확인된다. DB/API/검색 스택과 유지 주기는 열린 결정이다.
'''
(P/'CONFIGS.md').write_text(s)
# Index is a proposal only. Existing fixed sources remain pinned; future aggregate result uses explicit branch link.
bundles=read('bundles.json')['bundles'];fixed=read('evidence/fixed-inputs.json');own='docs/workstreams/research/AF-RES-020';base='https://github.com/laadkke-arch/agentflow-open';branch=f'{base}/tree/work/research-af-res-020/{own}'
s='''# 공통 색인 반영 제안 — 미적용

## 1. 편집 기준

읽은 색인은 foundation `7b4334e55a0563225295618eaf3ad299b415d9f7`의 docs/research/INDEX.md다. 그 문서가 요구하는 고유 ID / 답하는 질문 / 현재 상태 / 파일 / 핵심 의존·충돌 열을 그대로 제안한다. ‘새 제품 연구 미배정·아직 없음’은 당시 설명이며 현재 배정을 취소하지 않는다. 원본 전체를 색인에 복제하지 않고 개별 고정 결과로 연결한다.

020의 최종 RESULT·HANDOFF는 이 제안 뒤의 별도 커밋에서 만들어진다. 아래020 행은 명시적인 작업 브랜치 링크다. **편집 담당은 최종 HANDOFF 커밋과 acceptance 파일을 확인한 뒤 이 링크를 해당 결과 SHA로 고정한다.** 이미 완성된24묶음 링크는 묶음 완료 커밋 `aa0b4050f82116e3c18553f8a179e40e6bdf54e9`로 고정했다. 사용자 요청에 따라 공통 색인·진행표·계약은 수정하지 않았다.

## 2. 대표 행 한 개

'''
row=['AF-RES-020','001~016의 결과를 어떤 독립 묶음으로 채택·보류·교체하고 다시 조합할 수 있는가','REVIEW_READY_WITH_GAPS — 연구 산출 조건과 운영 절차 미충족을 분리; 최종 설계 미선정',f'[RESULT·HANDOFF·묶음]({branch})','12고정 입력; 24묶음·276쌍·16충돌·3구성; proposed_use 누락·평가 정의·전환 보존 조건; 017~019 대기']
s+=table(['고유 ID','답하는 질문','현재 상태','파일','핵심 의존·충돌'],[row])+'\n\n## 3. 개별 묶음으로 바로 읽을 행\n\n대표 행 아래 별도 하위 색인으로 둘 수 있다. 공통 색인에24행을 모두 넣을 필요는 없으며 bundles.json을 진입점으로 써도 된다. 수용 상태는020 인계와 함께 읽고, 내용의 채택 여부는 최상위 설계자가 결정한다.\n\n'
rows=[]
for b in bundles:
 state='빈칸 포함·추가 사례 필요' if b['id'] in ['B19','B21'] else '조건부 검토 가능·효과/최종 선택 아님'
 conflict='; '.join(x['id'] for x in read('evidence/conflicts-data.json') if b['id'] in x['bundles']) or '직접 충돌 미선정'
 rows.append([b['id'],b['decision'],state,f"[{b['title']}]({base}/blob/aa0b4050f82116e3c18553f8a179e40e6bdf54e9/{own}/bundles/{b['id']}.md)",conflict+'; 선행·조건은 RELATIONS'])
s+=table(['고유 ID','답하는 질문','현재 상태','파일','핵심 의존·충돌'],rows)+'\n\n## 4. 통합되지 않은 원 결과의 고정 진입점\n\n원 결과는 foundation 작업 트리에 없을 수 있으므로 브랜치 HEAD 대신 지정 result_commit을 사용한다. 원 인계 상태를 이번 표준 어휘로 덮어쓰지 않는다. 이 목록은 독립 연구의 승인 목록이 아니다.\n\n'
rows=[]
for t,sha in fixed['fixed'].items():
 state='원 HANDOFF 확인; 문서·실행·효과 범위 구분'
 if t=='AF-RES-013':state='원 BLOCKED — SITE_CAP_CASES; DONE과 정합성은 별도 인수 확인'
 if t=='AF-RES-016':state='원 core_artifacts_complete_with_blocked_named_original_reading; 고전0/2 미열람'
 rows.append([t,sha,f'[{t} HANDOFF]({base}/blob/{sha}/docs/workstreams/research/{t}/HANDOFF.md)',state])
s+=table(['원 작업','고정 result_commit','인계 파일','상태 주의'],rows)
s+='''

## 5. 편집 담당의 다음 첫 행동

최종020 HANDOFF 커밋에서 RESULT·SELF_CHECK·acceptance-evidence를 함께 연다. 연구 내용의 재사용 범위와 운영 절차 두 미충족을 따로 확인하고 대표 행의 브랜치 링크를 검토한 SHA로 고정한다. 그런 다음 원013/016의 DONE 처리에 대응하는 인수 기록이 있는지 진행 담당에게 확인할 질문을 남긴다. 이 연구에서 질문을 전송하거나 상태를 변경하지 않았다.

## 한계

색인의 최종 계층·통합 커밋·정규화 정책은 편집 담당의 결정이다. 현재 파일은 적용 가능한 행 제안이며 공통 파일을 수정한 결과가 아니다. 이름이 비슷한 역할·gold·완료 상태를 단일 라벨로 합치지 않는다. ADR X10의 이력 보존과 근거 지도 X14·X15의 범위/빈칸 분리는 편집 제안의 방법 근거이며 상태의 외부 검증은 아니다.
'''
(P/'INDEX_PROPOSAL.md').write_text(s)
print('rendered configs',len(cfg),'index bundle rows',len(bundles))
