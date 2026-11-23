"""Write the prespecified problem and query records, before search execution."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
observations = {r['frame_id']: r for r in map(json.loads, (ROOT/'evidence/body-observations.jsonl').read_text().splitlines())}
problems = [
 {'problem_id':'P1','frame_id':'F1-01','project':'JupyterLab','issue_number':19647,
  'symptom':'새 설치에서 disable한 항목이 다음 CLI 호출의 구판 전환에 다시 잡혀 lock 상태까지 바뀜.',
  'goal':'새 disable은 lock 상태를 바꾸지 않으며 기존 구판 전환과 구별된다.',
  'goal_span':'body L3-L13, L47-L59',
  'conditions':[{'id':'P1-C1','text':'새 disable 이후 원래 lock 상태가 그대로여야 한다.','source_span':'L47-L49','basis':'author_explicit'},
                {'id':'P1-C2','text':'기존 disabled 목록이 비어 있고 빈 하위 사전이 읽기 때 제거되어도 다음 실행의 새 항목을 구판 항목으로 오인하지 않아야 한다.','source_span':'L53-L59','basis':'constraint_from_author_reported_cause'}],
  'boundary_input':'page_config 없음/disabled 비어 있음 → disable 한 번 → 새 프로세스 enable. sys_prefix와 system 경로가 같은 경우/다른 경우를 모두 구분.',
  'boundary_span':'L17-L45, L63-L65',
  'open_design_choice':'전환 완료와 미실행을 영속적으로 어떻게 구분하고 새 항목의 상태와 분리할 것인가.',
  'choice_is_researcher_interpretation':True,
  'prior_choice':'연구자 가정: 현재 설정 저장부에 전환 완료를 구분하는 최소 수정 후 재현 순서를 회귀 검사. 원 개발자의 실제 결정 기록은 없음.',
  'prior_exposure':['현재 원문의 함수명/원인/빈 사전 표식 실패/4.1 전환/Windows 경로 조건','일반적인 버전·완료 표식과 한 번만 실행하는 전환 개념은 조사 전 알고 있음','065 인계의 인쇄→사진 귀속을 읽었으나 본 문제 후보로 재사용하지 않음'],
  'not_new':['원문에 적힌 원인 재발견','빈 lockedExtensions 사전의 실패','완료 표식이라는 일반 발상'],
  'branch_B_removed':['JupyterLab','jupyter labextension','disabledExtensions','lockedExtensions','Python','Windows','jupyter_server.config_manager.recursive_update'],
  'branch_B_preserved':['과거 항목에 한 번만 적용할 복사','신규 비활성 상태와 별도 잠금 상태','빈 초기 집합','재실행','빈 사전의 소실'],
  'branch_B_loss_risk':'운영체제별 경로 계층/CLI 에러 문구를 없애므로 같은 경로 alias 문제를 단독으로 해결하지 못할 수 있음.'},
 {'problem_id':'P2','frame_id':'F2-04','project':'Home Assistant Core','issue_number':180207,
  'symptom':'Hub Mini 뒤 Battery Doorbell에 묶인 Chime가 별도 기기/볼륨 entity로 노출되지 않음.',
  'goal':'현재 Hub→Doorbell→Chime 연결에서 실제 Chime 볼륨을 제어할 수 있다.',
  'goal_span':'body L3-L18, L40-L50',
  'conditions':[{'id':'P2-C1','text':'현재 Hub→Battery Doorbell→Chime 연결을 유지한 채 Chime 제어를 노출한다.','source_span':'L3-L18, L40-L48','basis':'author_reported_topology_and_goal'},
                {'id':'P2-C2','text':'부모 Doorbell 볼륨과 구별되는 실제 Chime 볼륨을 바꾼다. 별도 기기 또는 Doorbell 소속 entity 모두 허용.','source_span':'L35, L42-L45','basis':'author_explicit_alternatives_and_negative_test'}],
  'boundary_input':'vendor 앱에서는 paired leaf가 동작하지만 root 진단 Chimes={}이고 이미 있는 부모 볼륨 둘 다 leaf를 바꾸지 못함.',
  'boundary_span':'L20-L39',
  'open_design_choice':'leaf를 별도 기기로 발견할지, 부모 소속 capability/entity로 표현할지와 그 leaf 명령 경로.',
  'choice_is_researcher_interpretation':False,
  'prior_choice':'연구자 가정: 현 연동의 진단과 기기별 discovery 응답을 비교하고 지원되는 leaf API가 있는지 먼저 확인. 실제 원 개발자 결정은 미측정.',
  'prior_exposure':['원문에 있는 기기명/펌웨어/연결도/별도 기기 또는 부모 entity라는 두 표현안','일반적인 부모-자식 모델과 Home Assistant entity 개념은 알고 있음','정확한 Reolink API의 지원 범위/사용할 부품은 미확인'],
  'not_new':['별도 기기 또는 부모 entity라는 표현 자체','Chimes={} 재확인','Doorbell 볼륨을 다시 시험하자는 제안'],
  'branch_B_removed':['Home Assistant','Reolink','Home Hub Mini','Battery Doorbell','Chime','volume','펌웨어 이름'],
  'branch_B_preserved':['root→중간 기기→paired leaf','root는 중간까지만 열거','leaf는 원 앱에서 동작','부모 속성 제어와 leaf 제어의 비동일성','별도 leaf identity 또는 부모 소속 속성 허용'],
  'branch_B_loss_risk':'볼륨이라는 구체 속성과 사유 프로토콜/펌웨어 제한이 빠져 일반 discovery 원리를 직접 부품으로 오판할 위험.'},
 {'problem_id':'P3','frame_id':'F3-03','project':'Inkscape','issue_number':13819,
  'symptom':'Undo History 세 열에 제목이 없어 초보 사용자가 의미를 구분하기 어려움.',
  'goal':'좁은 Undo History 대화상자에 도구 아이콘·행동 수·행동의 열 제목을 제공한다.',
  'goal_span':'body L8-L32',
  'conditions':[{'id':'P3-C1','text':'도구 아이콘·행동 수·행동이라는 세 열 의미를 초보 사용자에게 제목으로 드러낸다.','source_span':'L20-L30','basis':'author_explicit'},
                {'id':'P3-C2','text':'작은 기존 대화상자 공간에서 표시해야 한다. 둘째 열의 긴 표현 또는 짧은 표현 선택은 열려 있다.','source_span':'L28-L32','basis':'author_explicit_qualitative_constraint'}],
  'boundary_input':'둘째 제목의 긴 표현은 공간을 넘고 짧은 Number만으로는 무엇을 세는지 모호할 수 있는 폭. 원문은 수치 폭/글꼴/언어별 한계를 주지 않음.',
  'boundary_span':'L20, L28-L32; 구체 폭과 모호성 시험은 연구자 가설',
  'open_design_choice':'세 제목의 길이·노출 방식·열 폭을 어떻게 정해 의미와 공간 제약을 함께 지킬 것인가.',
  'choice_is_researcher_interpretation':True,
  'prior_choice':'연구자 가정: 원문 제안 세 제목을 현재 위젯에 넣고 둘째 제목 두 표현의 실제 폭을 비교. 원 개발자의 실제 선택은 미측정.',
  'prior_exposure':['원문의 Tool Icon / No. of Actions 또는 Number / Action이라는 제안','일반적인 열 제목·줄바꿈·축약·도움말·접근성 이름 개념은 알고 있음','잠정적으로 다음 순번 QR 입력 보존 문제를 읽었으나 본 문제 검색에는 사용하지 않음','정확한 GTK4 열 제목 동작/치수는 읽지 않음'],
  'not_new':['열 제목을 추가한다는 요청','원문에 적힌 제목 문자열','긴 제목을 짧게 바꾼다는 일반 발상'],
  'branch_B_removed':['Inkscape','Undo History','GTK4','gtkmm','Linux Mint','소프트웨어 버전'],
  'branch_B_preserved':['세 열의 icon/count/action 의미','초보 사용자에게 제목으로 설명','좁은 공간','긴 명칭과 짧은 명칭의 선택'],
  'branch_B_loss_risk':'실제 desktop widget 및 undo action 의미를 없애면 web table 제안을 직접 사용 가능한 부품으로 잘못 판단할 위험. 고정 폭 수치가 없어 C2는 조건부다.'}
]
query_text = {
 'P1': {'A':['JupyterLab disabledExtensions lockedExtensions migration empty configuration','jupyter labextension disable locks extension migration','JupyterLab page_config migration marker recursive_update empty dictionary'],
        'B':['old records need state copied once new records must not be copied empty collection loses completion state','repeated startup cannot distinguish never processed from processed empty persistent state','disable operation must not change separate locked state old records transition empty dictionaries removed']},
 'P2': {'A':['Home Assistant Reolink Home Hub Mini battery doorbell chime volume discovery','Reolink API chime list empty hub doorbell volume control','Home Assistant Reolink chime device entity battery doorbell hub support'],
        'B':['root discovers intermediate device but paired leaf missing control capability through hierarchy','discover paired descendant device empty list parent attribute does not control child attribute','expose leaf device as separate identity or parent property through intermediate controller preserve command target']},
 'P3': {'A':['Inkscape Undo History dialog column headings narrow GTK4','GTK4 ColumnView column title header ellipsize minimum width','Inkscape undo history action count column header tool icon'],
        'B':['narrow three column history table icon count action headings novice understanding','short versus descriptive column labels limited width number of actions header','show column meaning in small space persistent labels icons counts actions']}
}
for p in problems:
    p['source_observation'] = observations[p['frame_id']]
    p['strict_layer_eligible'] = False
    p['observed_layer_eligible'] = True
    p['novelty_definition'] = '명시 사전 노출 원장에 없고 질의 동결 후 처음 읽은 문서/구체 기능에 한정; 모델 학습 데이터나 원 개발자에게 새로움을 주장하지 않음.'
    p['search_order'] = ['A','B'] if int(p['problem_id'][1:])%2 else ['B','A']
(ROOT/'problems.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in problems))
queries=[]
for p in problems:
    for arm in ['A','B']:
        for n,q in enumerate(query_text[p['problem_id']][arm],1):
            queries.append({'query_id':f'{p["problem_id"]}-{arm}-Q{n}','problem_id':p['problem_id'],'arm':arm,'query_number':n,'query':q,'engine':'system2_search_query','language':'English','domain_filter':None,'recency_filter':None,'top_slots':5,'open_unique_originals_cap_per_arm':5,'immutable_after_commit':True})
(ROOT/'queries.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in queries))
for arm in ['A','B']:
    folder=ROOT/'arms'/arm;folder.mkdir(parents=True,exist_ok=True)
    packet=[]
    for p in problems:
        value={'problem_id':p['problem_id'],'goal':p['goal'],'conditions':p['conditions'],'boundary_input':p['boundary_input'],'queries':[q for q in queries if q['arm']==arm and q['problem_id']==p['problem_id']]}
        if arm=='A':
            value.update(project=p['project'],issue_number=p['issue_number'],original_issue_url=p['source_observation']['url'],prior_exposure=p['prior_exposure'],prior_choice=p['prior_choice'])
        else:
            # Rephrase all source-specific names in the B packet, retaining the frozen relations.
            btexts={
             'P1':('과거 항목에 한 번 적용되는 상태 복사가 이후 새 항목의 독립 상태를 바꾸지 않는다.',[
               '새 비활성화가 별도 잠금 상태를 바꾸지 않는다.','초기 항목 집합이 비어 있고 빈 하위 사전이 제거되어도 재실행 때 새 항목을 과거 항목으로 오인하지 않는다.'],
               '빈 영속 설정→한 항목 비활성화→새 프로세스에서 활성화. 저장 경로의 계층 둘이 같은 경로인 경우와 다른 경우.'),
             'P2':('root→중간 기기→paired leaf 연결을 유지한 채 leaf 속성을 제어한다.',[
               '현재 3단 연결을 유지하면서 leaf 제어를 노출한다.','부모 속성과 구별되는 실제 leaf 속성을 바꾼다. 별도 identity 또는 부모 소속 property 표현을 모두 허용한다.'],
               '원 앱에서는 paired leaf가 동작하지만 root의 leaf 목록은 비어 있고 부모 속성 두 제어는 leaf 속성을 바꾸지 못한다.'),
             'P3':('좁은 기록 대화상자에서 세 열의 의미를 제목으로 드러낸다.',[
               'icon·count·action 세 열 의미를 초보 사용자에게 제목으로 설명한다.','작은 기존 공간에 표시한다. count의 긴 명칭과 짧은 명칭 선택은 열려 있다.'],
               '긴 제목은 넘치고 짧은 숫자 명칭은 세는 대상을 설명하지 못할 수 있는 폭. 원문 수치 폭은 미제공.')}
            goal,conds,boundary=btexts[p['problem_id']]
            value.update(goal=goal,conditions=[{'id':f'{p["problem_id"]}-C{i+1}','text':t} for i,t in enumerate(conds)],boundary_input=boundary)
        packet.append(value)
    (folder/'input.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
print('wrote 3 problem records, 18 frozen query records, separated arm packets; no search executed')
