#!/usr/bin/env python3
"""Render the required ordered tables from committed-style JSONL/CSV ledgers."""
from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent
def jl(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def link(label,url):return f'[{label}]({url})' if url else label
def cell(v):return str(v).replace('|','／').replace('\n',' ')
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(cell(x) for x in row)+' |\n' for row in rows)+'\n'
rows=jl(P/'chains.jsonl');initial={x['case_id']:x for x in jl(P/'initial.jsonl')}
counts=json.loads((P/'evidence/denominators.json').read_text())['groups']
sc=json.loads((P/'evidence/source-counts.json').read_text())['counts']
providers={}
for stream in ['matplotlib','xarray','duckdb']:
 for r in jl(P/'streams'/stream/'providers.jsonl'):providers[r['source_id']]=r
pm={
'M01':['M-P01','M-P02'],'M02':['M-EVENT-24869'],'M03':['M-P03','M-P03-SOURCE'],'M04':['M-P04'],
'M05':['M-P05'],'M06':['M-P06'],'M07':['M-P07','M-P09','M-P10'],'M08':['M-P08'],'MB09':['M-P11'],
'X01':['XD01','XD06'],'X02':['XD01','XD02'],'X03':['XD02'],'X04':['XD09b','XD05'],'X07':['XD04'],
'XB03':['XD11'],'XB14':['XD07','XD08'],'D01':['DP06'],'D02':['DP05'],'D03':['DP07'],
'D04':['DP08'],'D05':['DP02'],'D06':['DP09'],'D08':['DP01'],'DB04':['DP03'],'DB07':['DP04']}
candidate={
'M01':'전: 구체 후보 없음. 후: 같은 지원자가 재현 가능하다고 확인. 다른 공급자의 dtype 승격 수리는 별도.',
'M02':'전/후: wx toolbar 문구 폭 문제의 공급자 수정. 작성자 선택변화 자료 없음.',
'M03':'전: addfont 후보. 작성자는 세션 한정이라 거절. 후: 다른 지원자들의 폰트 cache 설명을 받아 삭제.',
'M04':'전/후: 공식 Tk 예제처럼 pyplot 대신 Figure 직접 생성. 같은 최초 안내를 실행.',
'M05':'전/후: 실질 응답 없음. PGF 소스 읽기로 원인·해결을 확정할 수 없음.',
'M06':'전/후: pandas 내부 clear를 근거로 해당 프로젝트에 신고 안내. 작성자는 root 예제를 편집.',
'M07':'전: Seaborn 신고 여부 질문과 범례 탐색 설명. 후: 다른 공급자의 move_legend 등 논의. 원작성자값 회수 없음.',
'M08':'전: 축소 재현 요청/draw_idle 가설. 후: 같은 지원자가 toolkit 통일 원칙 설명. 요청조건 미충족 부분입력 뒤 변화.',
'X01':'전: 구체 제안 없음. 후: 명시 encoding이 기존 설정을 대체하므로 원 encoding dict 직접 수정 안내.',
'X02':'전: mode=w 또는 tmp_path 조건부 안내. 후: 자발적 S3+moto 공개로 초기 추정 철회, 오류 요청으로 이동.',
'X03':'전: 제안 없음. 후: 임시 Dataset을 거쳐 to_dask_dataframe. 사용자는 Series 목적을 보충.',
'X04':'전: 질문과 동시에 rasterio engine 직접 호출. 후: 같은 후보의 entrypoint/list_engines 설명. 성공 보고가 설명보다 먼저.',
'X05':'전/후: DataTree shallow copy/parent 설계 제안 동의. 후발 copy 의미 질문은 새로운 설계 논의.',
'X06':'전/후: 실질 응답 없음. private S3/open_datatree 사용 가능성 미확인.',
'X07':'전/후: 유지관리자 요청의 최소 pure-xarray 예제 의미를 기여자가 물음. 후보 제안 없음.',
'X08':'전: Dataset dict 분리 설계. 후: Coordinates wrapper 설계 의견. 기존 환경의 단일값 회수와 구별.',
'D01':'전: 공급자 수정 계획. 후: 미지원 예외로 제한. 수정판을 원작성자가 실행한 자료 없음.',
'D02':'전: 구체 권고 없는 기술 설명. 후: 다중 query 논거를 인용해 설명 수정 및 query-aware 설계를 처음 제안.',
'D03':'전/후: 대화 응답 없음. list-comprehension 공급자 PR 존재는 사용자 실행과 별도.',
'D04':'전/후: 대화 응답 없음. DST interval 공급자 PR 본문 결정만 확인.',
'D05':'전: 실제 연결 timezone 질문. 후: 지원자가 Kolkata를 추정하고 ICU 수정. 작성자 답 없음.',
'D06':'전/후: 대화 응답 없음. ARRAY/list_zip 공급자 PR 본문 결정만 확인.',
'D07':'전/후: pandas 경유 NaN 처리와 다른 API 설명. 요청자 수락·실행 및 당시 전체 변환 계약 미확인.',
'D08':'전: last 함수와 frame 안내. 후: 작성자 성공 보고 뒤 같은 지원자가 alias/frame 설명 일부를 정정.',
'MB09':'전/후: 환경 질문과 함께 새 conda 환경 생성 제안. 환경값 답 없이 그 행동을 실행, 지원자 후속 없음.',
'XB03':'전: 구체 제안 없음. 후: array API의 혼합 배열 범위 설명과 선호 재질문, 다른 지원자의 명시 변환 제안.',
'XB06':'root30/90에는 제안 없음. 16개월 뒤 synchronizer 전달과 xarray 고유 여부 진단. 다른 판의 실패는 late question30.',
'XB08':'전: 구체 제안 없음. 후: 복사/CFTimeIndex 진단과 engine=flox 제안. 버전값 때문에 후보를 바꿨다는 명시 연결 없음.',
'XB13':'전: 구체 후보 없음. 후: 독립 open_dataset 및 netcdf4 engine 시험. 다른 파일 성공은 원입력 성공이 아님.',
'XB14':'전: backend/remote 질문. 후: NFS와 HTTPS 용어를 설명해 같은 변수 재질문. 다른 지원자가 retry 코드를 제시.',
'DB04':'전: quoted/unquoted 실제 CSV 확인. 후: 동일 지원자 권고 없음. 한 달 뒤 공급자 시험은 초기판 성능 보장이 아님.',
'DB07':'전: 일반 ORDER BY 설명과 원하는 순서 확인. 후: 구체 index 열을 처음 제안. 후발 방법 수정은 새로 공개된 임의 relation/row-number 안과 연결.'}
case_table=[]
for r in rows:
 cid=r['case_id'];i=initial[cid]
 first=f"{cid} · {r['sample']} · {r['created_utc']}"
 goal=f"@{r['author']} · {i['goal']}. 현재본문 값: {i['current_root_values']}. 원판 {r['original_grade']}(전체복원 아님). "+link('본문',r['root_url'])
 qparts=[]
 for q in r['questions']:
  tag='정보질문' if q['is_information_request_to_original_author'] else '설계·실행·역방향/fit 질문(엄격 분모 제외)'
  if cid=='M03':tag='첫 응답의 후보 적합성 질문(정보질문 분모 제외)'
  if not q['root30']:tag+=' / root30 밖'
  summary=q.get('summary') or i['first_response_summary']
  qparts.append(f"{tag}: {summary} 변수={','.join(q['variables'])}. "+link(q['question_id'],q['url']))
 if not qparts:qparts=[f"정보질문 없음. 최초={i['first_strategy']}: {i['first_response_summary'] or '실질 응답 없음'}. "+link('첫 응답',i['first_response_url'])]
 apart=[]
 for a in r['answers']:
  author='원작성자' if a['is_original_author'] else '제3자(작성자값 아님)'
  apart.append(f"{author} {a['utc']}: {a.get('summary','')} [{a['answer_class']}]. "+link('답',a['url']))
 if not apart:apart=['질문 있음: 관측된 작성자값 없음' if r['root30']['information_question'] else '해당 없음: 주 창의 정보질문 없음']
 refs=[]
 for e in r['recommendations']:
  if e.get('url'):refs.append(link('전후 발화',e['url']))
 official='; '.join(link(x,providers[x]['url']) for x in pm.get(cid,[])) or '당시 공식판/전체 적합 미확인; 원판·환경 또는 해당 API 계약을 다음에 확인'
 rec=candidate[cid]+' '+' / '.join(dict.fromkeys(refs))+' 공식 제한근거: '+official
 actions=[]
 for e in r['executions']:
  tag='새 동일목적 실행' if e['new_original_goal_execution'] else '진단·회상·계획·다른입력(주 성공분자 제외)'
  if not e['root90']:tag+=' / root90 밖'
  actions.append(tag+': '+e.get('summary','')+' '+link('행동',e.get('url')))
 if not actions:actions=['원작성자 새 동일목적 실행 미확인.']
 if r['late_history']:
  actions.append('90일 밖 후속은 chains.jsonl late_history에 별도; 주 분자 불산입.')
 actions.append(f"root30 성공={int(r['root30']['new_execution_success'])}, 실패={int(r['root30']['new_execution_failure'])}; 상세 미확인·다음 자료: "+link(cid+' 원장',r['stream_file']))
 case_table.append([first,goal,' / '.join(qparts),' / '.join(apart),rec,' / '.join(actions)])

den_rows=[]
labels={'A_all':'A 전체; 제외 없음','A_information_question':'A root30 정보질문 있음; fit·새 설계·역방향 제외','A_direct_answer':'A 같은 변수 기존값 직접답','A_same_goal_execution':'A 같은 목적 후속 실행 보고; 성공·실패 모두 포함','A_same_goal_execution_success':'A 새 동일목적 한정성공 보고만','B_all':'선정 B 전체; A 대체/발생률 보강 금지','B_information_question':'B root30 정보질문 있음; XB06 late 제외','B_direct_answer':'B 같은 변수 기존값 직접답','B_same_goal_execution':'B 같은 목적 후속 실행 보고; 성공·실패 모두 포함','B_same_goal_execution_success':'B 새 동일목적 한정성공 보고만'}
for key,label in labels.items():
 g=counts[key];sample=key[0]
 current=len(g['current_overlap_cases'])
 wait='해당 없음' if g['strict_wait_min_hours'] is None else f"직접답 생성시각 {g['strict_wait_min_hours']:.4f}–{g['strict_wait_max_hours']:.4f}h"
 den_rows.append([label,f"사례 {g['n']}",f"현재중복 {current}/{g['n']}; 질문전 공개 확정0, 시점 미확인{current}",f"{g['same_variable_answer']}/{g['n']} 사례; 변수{g['strict_answer_variable_count']}·왕복{g['strict_answer_roundtrips']}",f"{g['linked_recommendation_change']}/{g['same_variable_answer']} 직접답 사례" if g['same_variable_answer'] else '해당 없음(직접답0)',f"{g['new_execution_success']}/{g['n']} · {g['new_execution_failure']}/{g['n']}; 전체목표{g['full_goal_success']}/{g['n']}",f"질문에 작성자답 전무 {g['no_author_reply_to_any_information_question']}사례; 값 없는 답은 별도. 현재창 관측불능0, 과거 미표시 삭제 미확인",f"직접 {g['strict_answer_roundtrips']}·정보질문 관련 작성자 반응 {g['any_author_reply_roundtrips']}왕복(비직접답 포함); {wait}; 편집범위 wait-audit.csv"])
den_rows.extend([
 ['질문발화/변수 별도 분모; root30','A 8발화/8episode, B 10발화/9episode','원판 전체0/32; 현재값을 최초값으로 대치하지 않음','A 3/9변수(9중 traceback1 시점미확인); B 8/11변수','A 0/3, B 0/6 직접답 사례','A/B 합쳐 성공률 만들지 않음','작성자 무응답 발화 A2, B1(DB07 후발). XB06은 창 종료 뒤 첫질문','미답 question30 각각720h 관측; root30 censor 별도. 클릭·읽기·대신할 노동 전부 미확인'],
 ['A 원판 전체 O 확인 하위집합','사례 0','해당 없음','해당 없음','해당 없음','해당 없음','전 사례 원판 미복원. Q부분인용은 전체 O 아님','해당 없음'],
 ['엄격 변경을 거친 동일목적 성공','A 직접답3 / B 직접답6','별도 중복분모와 같지 않음','A3 / B6','A0/3 / B0/6','완전사슬 A0/3 / B0/6','기존 후보 없음·연결 미확인·실행 미보고를 구분','0은 질문 효용 부재의 추정치가 아님'],
])

cp=list(csv.DictReader((P/'comparison-results.csv').open()))
contrast=[]
for r in cp:
 q=initial[r['question_case']];c=initial.get(r['comparison_case'])
 wording=link(r['question_case']+' '+q['first_response_summary'],r['question_url'])
 if c:wording+=' / '+link(r['comparison_case']+' '+c['first_response_summary'],r['comparison_url'])
 else:wording+=' / 대조 해당 없음'
 contrast.append([r['pair_id']+' · 사전: 같은 원장·분기·종류, 정보차≤1, 시각최단',wording,r['version_goal_information_difference'],r['provider_support'],r['actual_followup'],r['overturning_condition_or_unknown']])
contrast.extend([
 ['후발 X02 · 사전짝 없음','초기 조건부 '+link('X02','https://github.com/pydata/xarray/issues/7408#issuecomment-1369732703')+'; 후발 오류 질문','질문 최초8 집합과 root30 정보질문8 집합은 다름. M03 빠지고 X02 추가.','XD01/02; 오류 최초문구 시점 미확인','자발적 S3+moto 공개가 초기 권고를 바꿈. 뒤 질문에는 나중에 제공하겠다는 답만.','성공/실패를 본 뒤 새 짝을 만들지 않음. 오류 요청 원판이 다음 자료.'],
 ['E-M04 · 사후 반례, 짝 아님',link('공식 예제 1링크+API 안내',initial['M04']['first_response_url']),'Tk 종료 문제의 구체 코드와 목적이 있음','M-P04, 실제 첫응답 URL은 질문에서행동까지 표 참조',link('Figure 교체 후 해결 보고','https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370981028'),'클릭한 링크/읽기시간 미확인. 이 한 사례를 모든 정보 충분 요청에 일반화하지 않음.'],
 ['E-D08 · 사후 반례, 짝 아님',link('질문 없는 frame 안내','https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203075138'),'첫 답은 링크2개이며 함수/alias 설명 일부 오류','DP01; 뒤 공급자 정정도 함께 읽음',link('작성자 기대결과 실행','https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203153988'),'어느 링크·문장이 성공을 일으켰는지 미확인. 성공과 설명의 정확성은 별도.'],
 ['E-MB09 · 선정 B 반례',link('환경 질문+즉시 새환경 제안','https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496053940'),'옛 환경의 실제 package 값 미답','M-P11, 0.21.0문서/0.21.1신고 patch 차이',link('새 conda 환경에서 정상','https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688'),'직접답 없으면 진전도 없다는 규칙을 반증. 환경질문 단독효과는 모름.'],
 ['E-MB21 · 비선정 screening; A/B율 불산입',link('기존 버전답','https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146')+' → '+link('재질문','https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506278627'),'동일 shell PySide6.5.0를 다시 물음. 최초본문 이력과 달리 선행 댓글로 중복 확인','DES-P01 IPython backend mapping. 실제 환경 판/설정은 별도',link('재답','https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1507190964')+'; 뒤 직접 debugging과 다른 지원자 qt6 안내','중복 질문에도 진행함. 버전 재답만의 대기/노동을 복합 진단 비용에서 분리할 수 없음.'],
 ['E-MB07 · 비선정 screening; A/B율 불산입',link('후발 목적 질문','https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496169583')+' → '+link('canvas 밖 axes 목표','https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496337035'),'첫답은 즉답. 그 뒤 목적을 밝히고 다른 사람 설명·작성자 코드가 매개','M-P12/13, 내부 _tight_bbox 안정성 보장 없음',link('같은 지원자 안내','https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498195823')+' → '+link('새 영상 코드/출력','https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774'),'질문이 도움이 될 수 없다는 보편명제를 반증하지만 한 변수 단독효과는 분리되지 않음.'],
 ['E-XB25 · 비선정 screening; A/B율 불산입',link('직접 설정 안내와 후속','https://github.com/pydata/xarray/issues/7782'),'float 성공과 uint8/int8 새 문제를 나눔','XD10, 당시 conventions.py','mask_and_scale 안내→부분실행→같은 지원자 decode_cf→작성자 작동 보고','질문 없이도 실행 결과가 다음 추천 입력이 될 수 있음. 원자료 전체 정확성은 미확인.'],
])

text='# AF-RES-030 · 실제로 물은 한 변수가 작성자의 다음 선택을 바꿨는가\n\n'
text+=table(['사례 ID·A/B·시각','최초 목적·이미 있는 값과 URL','실제 질문·변수·URL','작성자 값·시각·URL','이전/이후 후보·용도·근거','당사자 행동·미확인'],case_table)
text+='## 2. 분모별 결과 및 비용\n\n'+table(['표본·제외 기준','분모 단위·수','이미 있던 값','같은 변수 직접 답','연결된 권고 변경','새 실행 성공/실패','무응답·관측 불능','왕복·대기 범위'],den_rows)
text+='## 3. 실제 반례·대조\n\n'+table(['짝 ID·선정 기준','묻기/즉답/조건부 원문','판·목적·정보량의 차이','공식 지지','실제 후속','결론이 깨지는 조건·미확인'],contrast)

text+='''## 판정의 의미와 핵심 결론

위 표의 발화는 한국어 요약이다. 실제 문구·시각은 각 원문 링크와 `questions.csv`의 `actual_question_excerpt_ref`, `question-audit.csv`, stream 원장에 연결했다. 첫 표의 현재본문 값은 **질문 전 최초값을 복원했다는 뜻이 아니다.** Q등급도 첫 답이 인용한 일부 문자열의 호환성만 보강한다. 모든 비율의 판정 주체는 담당 stream 판독자와 root 통합 검토자이며, 동일 댓글의 변수 여러 개를 독립 사람이나 독립 왕복으로 세지 않았다.

**A24에서 root30 정보질문은8건, 같은 변수 기존값 직접답은3/8건이다. B8에서는 root30 질문7건 중6건이 직접답을 받았다. 그 직접답이 같은 지원자의 기존 구체 권고 변경과 새 동일목적 실행으로 이어졌음을 엄격하게 확인한 완전사슬은 A0/3, B0/6이다.** 공개 대화는 질문이 실제로 있었고 답에 정보가 들어 있다는 점을 보여 주지만, 이 표본에서는 질문한 변수 하나가 기존 권고를 바꿨다는 연결을 분리해 보여 주지 못했다. 이것을 질문의 가치가 없다는 결론으로 바꾸면 안 된다.

관측된 진전은 여러 형태였다. [M01](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368556640)은 지원자의 재현 불가가 가능으로 바뀌었다. [D02](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686)는 답 묶음 안의 다중 query 논거가 기존 설명을 바꾸었고 첫 구체 설계가 나왔다. [XB13](https://github.com/pydata/xarray/issues/7754#issuecomment-1509585164)은 답 이후 진단 호출을 처음 제안했다. [XB14](https://github.com/pydata/xarray/issues/7758#issuecomment-1509899180)는 후보보다 질문에 쓴 용어의 설명이 달라졌다. 모두 실제 변화이지만, 앞선 구체 후보의 변경이라는 분자와는 다르다.

같은 목적의 후속 실행 보고 전체는 성공과 실패를 합쳐 A5건(M03/M04/M08/X04/D08), B2건(MB09/XB13)이다. 이 실행 분모에서 성공은 A4/5·B1/2, 실패는 A1/5·B1/2이며, 성공만 남긴 별도 하위집합 A4/B1과 구별한다. 이 비율도 실행을 보고한 사례의 기술적 결과일 뿐 전략의 효과가 아니다.

질문 없이도 새 실행 보고가 있었다. A의 한정성공4건 중 M04와 D08은 처음 안내를 실행했고, M03은 후보 적합성 질문 뒤 다른 지원자의 cache 설명을 사용했다. X04는 질문과 동시에 제공받은 호출을 실행한 뒤 설명을 더 받았다. B의 성공 MB09는 물은 기존 환경값에 답하지 않고 같은 첫 답에 들어 있던 새 환경 생성 행동을 수행했다. 따라서 **직접답 회수 여부를 진행의 유일한 문턱으로 삼는 규칙은 이 사례들과 맞지 않는다.** 성공 분자는 당사자의 구체 작업·결과 보고를 뜻하며, 이번 조사자가 요청자 기계에서 재현한 결과를 뜻하지 않는다.

### Q1. 모집틀, 목적을 처음 공개한 주체, 제외

최초 고정 창은 2023Q1와2024Q3이다. matplotlib/matplotlib, pydata/xarray, duckdb/duckdb 각각에서 같은 창의 생성시각 순 최초 적격4건을 뽑아 A24를 만들었다. 닫힘·답수·인기·수락은 선정 키가 아니다. 목적·사용·설계를 포함한 bug/feature 요청을 포함하고 공지·중복·설치/빌드 관리·문서 housekeeping 등은 이유를 남겼다. 주 원장의 접근 실패 시 공식 대체 원장과 다음 기간 순서도 SCOPE에 먼저 정했으나 A 대체는 필요하지 않았다. `frame.csv`는 전체 후보 metadata670행이며, 이를 직접 읽은 원문670개라고 세지 않는다.

B는2023년4월의 적격 루트에서 M27/X27/D26을 사전 interleave하여 처음80개로 상한을 고정했다. 첫 실질 응답의 환경·목표·입력 질문 조건만으로14개가 적격했고, 전역 순서의 최초8개를 선정했다. 작성자의 답·성공을 확인해8개를 채우지 않았다. 선정순은 XB03, DB04, XB06, DB07, XB08, MB09, XB13, XB14이다. 남은72개와 제외·상한밖 우연열람은 별도 범주이며 A발생률을 보충하지 않는다. B80 모두의30/90일 창 감사는 각 stream의 `screening-followups.jsonl`과 선정 `chains.jsonl`의 합집합으로 재현된다.

최초 목적의 주체는 root 작성자 계정으로 식별했다. 이는 실제 사람의 독립성을 증명하지 않는다. 유지관리자가 요청자이거나 다른 사람의 설계를 전달하는 X07/X08 같은 경우를 별도 표시했다. X07에서 후속 답자는 원 요청자인 유지관리자이며 질문자는 새 기여자다. 목적을 설명한 답을 일반 사용자 지원 성공으로 읽지 않았다. D02의 장애 경험은 기존 사실의 새 공개, DB07의 native 미지원도 수용 가능하다는 답과 XB03의 special-case 선호는 이전부터 있던 선호인지 새로 형성된 선호인지 미확인이다.

### Q2. 최초판 재구성과 미래정보 노출

원판 전체 O확인은0/32이다. A의 Q부분보강은 M04/X01, B는 DB04/DB07이고 나머지는 U다. 공개 HTML/API의 현 본문, 첫 응답의 인용, 편집/rename 사건, 첨부 또는 버전 흔적을 읽었지만 전체 최초본문 revision을 복원하지 못했다. `updated_at`을 곧 최초편집시점으로 쓰지 않았다. 현재 본문의 값으로 목적·시도·환경·출력·선호/필수/금지를 절 위치에 연결하되 최초값과 섞지 않았다. xarray의 `initial-field-audit.jsonl`13건은 봉인 cache와 hash가 일치하지만 **필드별 보강 매핑을 후속 판독 뒤 작성**했으므로 완전한 사전 독립 코딩으로 주장하지 않는다.

봉인 시 보였던 미래정보는 A의 D01/D04/M06/X01이다. 후속에서 B의 DB04 제목 개명과 XB08 버전 추가가 확인되어 효과적 노출을 추가했다. 그래서 엄격 미노출 하위집합은 A20/B6이다. M01의 현재 NumPy1.24와 후속1.24.0, XB03의 문제 초점, DB07의 순서 목표는 현재 본문과 중복되지만 그 값이 질문 전부터 공개됐는지는 세 사례 모두 미확인이다. DB07 첫 답의 인용은 재정렬 현상일 뿐 원하는 순서 계약의 값은 아니다. XB08처럼 질문 뒤 추가됐다는 명시 증거가 있으면 이전 공개값으로 세지 않았다.

### Q3–Q5. 실제 질문, 변수, 답과 관측 창

첫 응답 전략은 A에서 추가 정보요청3, 조건부 즉시행동1, 단정적 안내10, 복합5, 실질 응답없음5다. 넓은 첫 질문은8건이지만 M03의 후보 fit 평가를 제외한 첫 정보질문은7건이다. 이후 X02의 첫 오류 요청을 포함하면 root30 정보질문8건이 된다. **첫 질문8건과 전체 정보질문8건은 같은 집합이 아니다.** B는 첫 질문 기준8건 모두 적격이나 XB06의 첫 응답이16개월 뒤여서 root30/90 질문 분모에서는7건이다. 해당 창은 이미 끝났고 기록을 읽을 수 있으므로 XB06을 관측불능으로 처리하지 않는다.

A의 기존값 직접답은 M01 판, D02 실제 장애 경험, X07 최소 재현의 의미다. B는 DB04 실제 quoted null, DB07 원하는 순서, XB03 문제 초점, XB08 버전, XB13 실제 파일 위치·이름, XB14 backend·원격접근 방식이다. B의8개 변수 답은7왕복/6사례다. XB13 두 변수는 한 답에 들어 있으므로1왕복, XB14 두 변수는 용어 재설명을 거친2왕복이다. xarray의 공개 댓글 API에는 reply-to ID가 없어 같은 스레드의 인용·어휘·작성자·시간 순서로 연결했으며 이를 서버가 보증한 reply-to라고 쓰지 않았다.

X04의 답은 제안받은 새 호출의 실행을 포함하므로 엄격 기존값 답에서 제외한다. 이를 확장 정의에 넣으면 A직접답4/8이 되지만 권고변경0은 그대로다. M08은 축소 코드를 줬으나 요청한 단일 GUI toolkit 조건을 충족하지 못했다. X02는 오류값 없이 나중에 제공하겠다는 답, MB09는 기존 환경값 없이 새 환경 실행이다. D05의 Kolkata는 지원자의 추정이지 요청자 답이 아니다. XB13의 local은 실제 파일 답에 연결했고, 뒤 다른 파일 성공을 처음 파일의 값/성공으로 대체하지 않았다.

질문에 작성자 응답 자체가 없던 A사례는 M07/D05 두 건이다. 나머지 비직접답을 무응답으로 부르지 않았다. B의 초기 질문에는 작성자 반응이 있지만 DB07의 후발 row-number 배치 질문에는 답이 없다. 현재 공개 댓글 pagination에서는 누락/삭제 placeholder를 관측하지 않았고 창은 모두 종료됐다. 과거에 표시 없이 삭제된 내용의 부재는 미확인이다. root30와 root90의 엄격 직접답·변경·성공/실패 분자는 같으며, root90 밖 XB08의9월 성능 보고와 XB06의2024년 실패는 별도 late history다.

### Q6. 기술적 지지와 사용자 선택의 구분

공식 근거는 판/commit을 고정해 제한된 명제에만 붙였다. NumPy1.24의 정수변환 경고는 M01의 가능 경로를 지지하지만 경고 설정과 판 답의 기여를 나누지 못한다. Matplotlib3.6.2의 Tk 예제는 Figure 직접 생성 사용을 지지하지만 Windows 환경을 여기서 실행한 증거는 아니다. D08 당시 window 문서는 frame 안 마지막 값과 경계를 지지하며, 처음 지원자의 alias 설명 오류와 후속 정정도 같이 보존한다. DB07의 당시 plan_window 코드는 blocking/streaming 순서를 읽는 근거이지 모든 임의 relation의 원행순서를 보장하는 증거가 아니다.

공급자가 뒤에 만든 기능·PR·테스트는 별도 열/원장으로 둔다. M02의 toolbar 수정, D01의 미지원 예외, D03/D04/D06의 기능/수정 PR, DB04 한 달 뒤 CSV 테스트는 원작성자가 새 판을 설치해 성공했다는 자료가 아니다. DP08/DP09는 PR 본문 결정기록만 직접 읽고 상세 패치·실행은 읽지 않았다고 표시했다. XD05의4월 backend 문서를1월 설치환경의 보장으로 사용하지 않는다. M07의 ncols setter 존재만으로 기존 legend가 즉시 재배치된다고 승인하지 않는다. 당시 데이터·판·실행이 부족한 기술 적합은 sources의 한계 및 다음 자료에 미확인으로 남겼다.

### Q7. 대조, 반례, 관측 비용

사전 대조 규칙은 같은 원장·분기·요청종류, 현재본문 정보점수 차≤1, 즉답/조건부 첫 응답 중 생성시각 최단이다. M01–M02, M08–M06, X04–X03, D02–D01, D05–D07의5쌍과 미성립3건을 봉인했다. 점수는 원판을 복원한 충분도 점수가 아니라 현재본문 proxy다. 목적·난도·판·입력은 다르다. D05의 다른 후보 D08이 성공했다고 사후 교체하지 않았다. X02 후발 질문에는 사전짝이 없어 새로 붙이지 않았다. 다섯 질문 쪽에서 관측한정성공1, 실패1이 있고 대조 쪽은 새 실행보고가 없지만, 미보고를 실패로 바꿔 성공률 우열을 계산할 수 없다.

직접답 생성시각 간격은 A0.101944–24.528611시간, B0.0247–12.166944시간이다. 편집된 답에서는 값의 공개시각이 생성시각과 같다는 보장이 없다. D02는24.5286–24.7264시간, XB13은6.7919–7.5264시간, XB14 첫 답은2.7572–9.9650시간 범위를 함께 보존했다. XB14 remote 값의89초는 재표현 뒤 간격이고 처음 질문부터는11.7547시간이다. X02/XB06 질문문구는 답 뒤 편집돼 정확한 문구 대기는 미확인이다. 미답은 question30의720시간과 root30의 잔여 관측시간을 각각 적었다. 이 숫자들은 공개 댓글 사이의 경과시간이다. 읽기시간·클릭·대신할 수 있었던 노동 또는 질문 때문에 발생한 순증지연은 측정하지 않았다.

선정 밖에서 MB07의 후발 목적 질문→여러 설명과 작성자 코드→같은 질문자의 _tight_bbox 안내→새 영상 출력은 질문이 도움이 될 수 없다는 일반화를 깨뜨린다. 반면 MB21은 버전 답이 이미 있는 댓글 뒤 같은 값을 다시 물었고 작성자는 재답했다. 두 사례 모두 다른 진단과 자발적 실행이 섞여 단일 질문의 효과를 분리할 수 없다. XB25의 설정 안내→새 결과→다음 설정 제안은 질문 없이 실행 보고가 다음 분기의 입력이 될 수 있음을 보인다. 비선정 자료를 A/B 분자에 보태지 않았다.

### 다른 두 분야의 원문과 반증

[온라인 참고상담 원대화 분석(C-L1)](https://journals.ala.org/index.php/rusq/article/viewFile/3946/4432)의 익명 실제 장면에서는 이름 식별을 바로잡는 답, 학년 질문에 값 대신 허용 반응만 온 답, 정확한 양식 식별자에 곧바로 링크를 주고 대화가 끝난 경우가 구별된다. diving/driving 정정은 잠재 목표의 새 형성보다 오기 정정에 가깝다. 링크 전송·종료만으로 다운로드/사용을 확인할 수 없다. [UC24/7 평가 절차(C-L2)](https://libraries.universityofcalifornia.edu/wp-content/uploads/2012/08/24.7_interim_report_july_09_final.pdf)는 참고면담, 자료, 교육, 종료를 별도 평가하고 해당 없음도 허용한다. 완료 대화만 뽑은 평가틀의 선택 한계를 현재 표본에 그대로 옮기지 않았다.

[Census/RTI 행정기록 인지면접(C-S1)](https://www2.census.gov/library/working-papers/2023/adrm/cbsm/rsm2023-12.pdf)의 Q18에서는 토론/재독 후 중립 답이 바뀐 사례가 있고 Q20에서는 설명 맥락에 따라 찬반이 달라졌다. 그 값이 처음부터 고정된 선호였는지 분리할 수 없다. 연구진 문항 삭제 제안과 공급자의 유지 결정도 별도다. [BLS 여행 회상 프로토콜(C-S2)](https://www.reginfo.gov/public/do/DownloadDocument?objectID=135305101)은 자유회상 뒤 day-trip·선불·누락·중복 비용을 묻는 절차를 직접 보여 주지만 실제 참여자 답을 보여 주는 자료는 아니다. 두 자료를 같은 연구의 실험군처럼 결합하지 않았다.

[CDC/NCHS NHIS 인지면접(C-S4)](https://wwwn.cdc.gov/QBank/report/Wilmot_2023_NCHS_NHIS1.pdf)의 solvents 장면은 정의를 들은 뒤 No→Yes가 의도한 범위 이해와 연결된다. 같은 보고서의 vision rehabilitation 장면에서는 probe 뒤 Yes가 되었어도 약/추적 방문을 잘못 포함할 수 있었다. **답 변경 자체가 더 정확한 답이라는 보증은 없다.** 공개 보고서에는 모든 즉흥 probe의 앞뒤 원문이 실려 있지 않아 완전한 회화 순서를 복원한 것으로 쓰지 않았다.

[BLS 2003 회고 probe 연구(C-S5)](https://www.bls.gov/osmr/research-papers/2003/pdf/st030270.pdf)는 이해했다고 말하는 것과 상세 확인에서 나타나는 회상/해석의 차이를 보여 주며, [2025 probing 연구(C-S3)](https://majournals.bib.uni-mannheim.de/mda/article/download/2025.02/384/747)는 directive probe에 대한 동의 편향을 다룬다. 후자의 표4 예시는 가상 예시여서 실제 발화로 세지 않았다. 반대 방향으로 [BLS1999 통제 연구(C-S6)](https://www.bls.gov/osmr/research-papers/1999/pdf/st990270.pdf)는 정답을 정의한 복잡한 가상 상황에서 명료화가 정확도에 도움이 되면서 시간이 늘 수 있음을 보여 준다. 기존 집단 재사용·과제 차이·현실 사용과 가상 시나리오의 차이를 남겼다. 이 근거들은 GitHub 전략 효과의 추정치를 제공하지 않고, ‘답 회수=진실 회수’, ‘답 변화=목표 달성’, ‘질문=불필요 지연’이라는 성급한 규칙을 각각 반증한다.

### Q8. 설계자에게 넘길 범위

`DESIGN_RULES.md`의 사용자용10개 문장은 연구자가 만든 **미전송·미검사 예시**다. 실제 원발화와 출처를 분리했다. 다음 규칙은 효과가 검증된 정책이 아니라 이 자료와 모순되지 않는 설계 후보이다.

1. 물을 변수 하나와 두 가능한 값에 따라 달라질 후보·용도·설명·다음 행동을 먼저 적는다. 두 값 모두 같은 안전한 제한 행동으로 이어지면 현재 확인된 조건과 근거 링크를 제시할 수 있다.
2. 현재 본문에 값이 있어도 버전/주체/실제 입력의 동일성과 공개 시점을 확인한다. 반복된 값이 이미 선행 댓글에 있으면 같은 질문을 반복하기보다 빠진 다른 변수를 특정한다.
3. 답하기 어려운 용어는 질문 안에서 관측 가능한 차이로 풀어 쓴다. “원격인가?”보다 “파일을 NFS로 마운트해서 읽는가, HTTPS 주소를 바로 여는가?”처럼 구분하되 예시는 연구자 작성임을 표시한다.
4. 목적을 설명하는 답과 지금 새로 정한 선호를 분리한다. “지금 선택하면 어느 쪽이 필요한가”라는 합의와 “원래부터 필수였는가”라는 이력 확인은 다른 질문이다.
5. 조건부 설명에 즉시 실행할 행동을 넣었다면 이후 성공을 질문의 답 효과로 돌리지 않는다. 새 실행 보고 자체가 다음 분기의 입력이 될 수 있다.
6. 기술 문서의 지지 범위, 당사자 수락, 실제 실행 출력, 공급자 새 기능을 별도 상태로 유지한다. 감사·close만으로 적용을 확정하지 않는다.

예를 들어 X04에서 가져온 연구자 작성 조건부 안내는 “rioxarray가 설치되어 있다면 `open_mfdataset(paths, engine='rasterio')`로 직접 여는 경로를 확인하고, intake에서만 실패한다면 실제 전달한 경로목록을 보여 달라”이다. 이는 최초 환경과 metadata 전체 보존을 승인하는 말이 아니다. MB21 반례에서 가져온 질문 예시는 “지금 실행한 IPython 세션에서 선택된 backend 이름은 무엇인가?”이며 이미 알려진 PySide 판을 다시 묻지 않는다. D05의 질문 예시는 “같은 연결에서 `current_setting('TimeZone')` 값은 무엇인가?”로 literal UTC offset을 실제 연결 zone으로 대치하지 않게 한다. 이 예시는 발송하지 않았다.

## 민감도, 독립성, 남은 식별 한계

'''
sens=list(csv.DictReader((P/'sensitivity.csv').open()))
text+=table(['제외 규칙','사례','정보질문','직접답','엄격 권고변경','새 한정성공 / 실패','원목표 전체 성공'],[[r['subset'],r['cases'],r['information_question'],r['direct_answer'],r['strict_change'],r['execution_success']+' / '+r['execution_failure'],r['full_goal_success'] if r['cases']!='0' else '해당 없음'] for r in sens])
text+='''원작성자 handle 중복 제거는 각 A/B 내부의 생성시각 최초1건을 남긴 규칙이다. 유지관리자 여부는 공개 association/역할 판정이며 실제 사람의 신원을 확인한 결과가 아니다. 반복 지원자가 선택한 응답은 독립 시행으로 보지 않는다. 미래노출·유지관리자·반복 원작성자를 제외해도 관측된 엄격 변경은0이다. 원판 O하위집합은0이어서 해당 없음이지0%가 아니다.

현재중복으로 식별된 A1/B2의 과거 공개시점을 모두 처음부터 있었다/없었다로 두면 확정중복의 민감도는 A0–1/B0–2다. 질문뒤 추가가 확인된 XB08은 상한에 넣지 않는다. A에서 보고된 부분성공2건의 전체 목적 충족을 양끝으로 두면 관측 실행보고 중 전체성공은2–4/24다. 미보고19건까지 임의로 성공/실패로 대치하는 비증거 시나리오는2–23/24, B는1–7/8까지 넓어진다. 이 값들은 결과 분자에 넣지 않았다. 삭제/비공개 실행/원판을 복원하지 못하면 실제 사용의 성공은 좁게 식별되지 않는다. 공개된 명시 연결 없이 가상 댓글을 채워 넣어 권고변경 양성을 만들 수 없고, 질문이 없었을 경우 같은 사람이 무엇을 했을지는 여전히 관측되지 않는다.

첫 제안이 답 뒤에 나온 사례는 질문이 후보 선택을 도왔을 가능성이 있지만, 답 전에 다른 후보가 실제로 제안된 적이 없어 ‘바뀜’을 비교할 수 없다. 질문/즉답의 선택은 난도·지원자·작성자의 준비도와 섞이고, 같은 요청의 다른 전략을 시행하지 않았다. 대기시간 역시 실제 필요 진단·시간대·휴일·관심도를 통제한 순수 질문 비용이 아니다. 이것이 이 관측 짝 결과로 전략의 반사실적 효과를 말할 수 없는 구체적인 이유다.

## 직접 열람의 분모와 재현

'''
text+=table(['단위','수','의미'],[
 ['엄격 필수 최소 원문',sc['required_minimum_qualified_unique'],'A24 + 당시 공식 매뉴얼/예제/시험/결정14 + 두 외부분야8. B와 후기 대화로 결손을 채우지 않음'],
 ['A / 선정 B / 비선정 B',f"{sc['A_threads']} / {sc['B_selected_threads']} / {sc['B_nonselected_screening_threads']}",'스레드 단위. 댓글 여러 개는 독립 원문 아님'],
 ['공식 자료 원문 / 필수 적격',f"{sc['official_provider_originals_read']} / {sc['official_contemporaneous_manual_test_decision_qualified']}",'구현 소스 단독·판불일치·같은 문서군 보강은 최소수에서 보수적으로 제외'],
 ['외부 분야',f"도서관 {sc['cross_library_reference']}, 공공통계 {sc['cross_public_statistics']}",'원 관측과 절차/프로토콜을 구분; 026의 외부4자료와 중복하지 않음'],
 ['출처 원문 계열 전체',sc['canonical_original_records'],'모든 canonical 행의 합계. frame root만 읽은 추가 후보·제외/상한밖도 포함하므로 핵심연구 표본수 아님'],
 ['원문 읽기 원장 / frame-only',f"{sc['originals_with_named_reading_ledger']} / {sc['frame_only_displayed_roots']}",'근거 유형 차이 보존. 검색요약/실패는 시도원장으로만 처리'],
 ['주 표본 독립 사건 루트',32,'A24/B8; 실제 독립 사람32명이라는 뜻 아님'],
 ['주 표본 관측 댓글',f"root30 A{counts['A_all']['comment_count']}+B{counts['B_all']['comment_count']}={counts['A_all']['comment_count']+counts['B_all']['comment_count']}; root90 A{counts['A_all']['root90_comment_count']}+B{counts['B_all']['root90_comment_count']}={counts['A_all']['root90_comment_count']+counts['B_all']['root90_comment_count']}",'같은 댓글의 변수별 코딩을 댓글수에 재산입하지 않음'],
 ['질문/직접답/권고/실행 사건','question-audit.csv / chains.jsonl / wait-audit.csv','발화·episode·변수·왕복·사례 단위 별도. 실제 재집계 evidence/denominators.json'],
])
text+='''`sources.jsonl`은 원문당 canonical 행, 판·tag·URL mirror는 editions/urls, 확인UTC·읽은절·관측·한계·연결Q/case·중복군·최소산입·다음 자료를 가진다. 미실시 실행은 기술적 지지로 바꾸지 않았다. `SELF_CHECK.md`와 `evidence/acceptance-evidence.json`에서 요구 충족 여부를 각 근거에 연결한다. `INDEPENDENT_REVIEW.md`는 담당자의 자체 재검, 다른 담당자의 배열 재집계, root의 핵심 원문 재독을 구별한다. 원본 cache 없이 재현 가능한 집계 명령은 다음과 같다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/build_analysis.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/build_wait_audit.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/build_comparisons.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/build_sources.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/build_result.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-030/verify.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-030/manifest.json --fetch
```

제품 코드나 당시 사용자 환경의 실행시험은 하지 않았다. 다음 재개 시에는 `PENDING_EXECUTIONS.md`의 고정판·입력·명령과 원작성자 후속 자료를 먼저 확인한다. 기능 회귀 suite/CI 성공을 연구 문서 검산의 성공으로 대신 표시하지 않는다.

| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |
| --- | --- | --- | --- |
| 최초본문 전체0/32, 미래정보 노출6/32. 현재값 중복을 과거 중복으로 확정할 수 없음. | [M01](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341), [DB04 rename](https://github.com/duckdb/duckdb/issues/6943#event-8932902142), [XB08 추가](https://github.com/pydata/xarray/issues/7730#issuecomment-1499263329) | 초기 정보 충족도·재질문 필요성·대조 동등성 | 첫 자료: M01 최초 알림/공개 편집 revision. 다음 자료가 없으면 U등급 유지하며 최초값을 보충하지 않기. |
| 실제 한 변수 답과 자발적 추가 논거·첫 제안·설명 변경이 섞임. 엄격 변경0은 질문 효용0과 다름. | [D02 후속](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686), [MB07 실행](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774) | 물은 변수 하나의 기여·기존 권고 변경·전략 효과 | 첫 자료: D02 지원자가 무엇을 근거로 판단을 바꿨는지 특정한 공개 결정기록. 단일효과가 식별되는 전후 제안 쌍을 새 표집으로 확보. |
| 새 실행의 전체목표 검증·독립 출력·정확판이 부족하고 창 밖 성공은 주 결과에 넣을 수 없음. | [X04 실행](https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571), [XB13 다른 파일](https://github.com/pydata/xarray/issues/7754#issuecomment-1510522371), [XB08 late](https://github.com/pydata/xarray/issues/7730#issuecomment-1709120441) | 기술적 적합과 전체 사용 승인·행동 성공률·대기 비용 | 첫 자료: X04의 원 GeoTIFF/metadata 검증 출력과 당시 rioxarray 판. PENDING_EXECUTIONS의 재현을 실행하고 공개 당사자 결과와 구별. |
'''
(P/'RESULT.md').write_text(text)
print(json.dumps({'case_table_rows':len(case_table),'denominator_rows':len(den_rows),'contrast_rows':len(contrast),'bytes':len(text.encode()),'minimum_sources':sc['required_minimum_qualified_unique']}))
