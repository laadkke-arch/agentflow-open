#!/usr/bin/env python3
"""Render RESULT tables from the committed ledger schema, never hand-enter totals."""
import csv
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1]
def rows(name): return list(csv.DictReader((P/name).open()))
packets=[json.loads(s) for s in (P/'packets.jsonl').read_text().splitlines()]
pol={r['row_id']:r for r in rows('policies.csv')}
scores={r['row_id']:r for r in rows('scores.csv')}
criteria={r['case_id']:r for r in rows('criteria.csv')}
counts=json.loads((P/'evidence/ledger-counts.json').read_text())
initial={r['case_id']:r for r in rows('initial-version-review.csv')}
labels={'correct_single':'단일 행동 맞음','conditional_actionable':'조건부 사용 가능','wrong':'틀림','hold':'보류','enumeration_unresolved':'선택 미해결 열거','unjudgeable':'판정 불가'}
def cell(x):
    if x is None:return '미확인'
    if isinstance(x,(list,dict)):x=json.dumps(x,ensure_ascii=False)
    return str(x).replace('\n',' / ').replace('|','\\|')
def table(headers, body):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(cell(c) for c in r)+' |' for r in body])+'\n'
def link(url,label):return f'[{label}]({url})'
def urls(r):return json.loads(r['criterion_urls'])
def goal(p):
    return '중국어 인용부호의 글꼴 문제를 피하면서 서양 글꼴을 분리; 전역 lang 키 유지 의무는 미확정' if p['case_id']=='PAN-N2' else p['goal']
def answer(r):
    rr=json.loads(r['answer_urls'])
    return ('**봉인 당시 원답: 보존 의무 추론은 사후 철회됨. 아래 문구는 현 결론이 아님.** ' if r['case_id']=='PAN-N2' else '')+r['answer']+(' '+', '.join(link(u,'원절'+str(i+1)) for i,u in enumerate(rr)) if rr else '')

evidence_short={
'PAN-N1':'raw HTML 지원과 FORMAT 분기 명세; 요청 필터의 두 실행 출력은 없음.',
'PAN-N2':'Docx addLang의 w:val 설정을 확인; Word 글꼴/인용부호의 두 완성 산출물 없음.',
'PAN-N3':'Table 스타일과 writer 구조 옵션은 다른 단계; 완성 구현·양값 출력 없음.',
'PAN-N4':'번호 재생성 옵션과 Header 읽기 범위; 첨부 원번호와 변환 결과의 독립 대조 없음.',
'GDAL-N1':'SetGeogCS와 SetProjParm 계약만; datum/AUTHORITY 제약을 함께 해결한 출력 없음.',
'GDAL-N2':'ENVI guard와 헤더 발견 전제; 실제 후속은 EMPTY_DIR라는 다른 필드.',
'GDAL-N3':'원보고는 3.2.0/3.2.1 비교; 후보 문서도 3.1.4/3.2.1 혼합. 같은판 출력 대조 아님.',
'GDAL-N4':'-overwrite와 -a_srs 문서에 실패 시 무잔류 보장 없음. 제3자 로그는 별도 관측.',
'PAN-C1':'같은 LaTeX 입력, ±raw_tex → unknown macro를 raw로 남김/생략. 공식 저장 기대값 양성.',
'PAN-C2':'같은 328자 sloppypar 입력, ±raw_tex → 910자 native AST 해시 동일. 저장 기대값 음성.',
'GDAL-C1':'같은 GCP raster·40×40, -rn/-rb. 최근접 예측 픽셀107, bilinear ref111±1. 양성; 역사 실행 아님.',
'GDAL-C2':'같은20×20 입력,40×40/200% → 같은40×40·저장 checksum18784. 목표 수준 음성; 역사 전체 바이트 미확인.'}
unknown={
'PAN-N1':'최초판·설치판·Lua 구현·OP 적용 성공; 지정절 초과 노출.',
'PAN-N2':'최초판·font/quote 완전 재현. literal lang 보존 의무 추론 철회.',
'PAN-N3':'최초판·정확 개발판·미구현 AST 기능·사용 결과.',
'PAN-N4':'최초판·첨부 docx 원번호·보존 의미·적용 성공.',
'GDAL-N1':'최초판·원자료 datum/AUTHORITY·선택 필드 실제값·별개 성공.',
'GDAL-N2':'최초판·실제 header 내용·선택 필드 실제값; 성공은 다른 필드와 같은 댓글.',
'GDAL-N3':'최초판·권위 있는 datum·동일판 후보·실제 수정 성공.',
'GDAL-N4':'최초판·드라이버별 같은판 재현·무잔류 기능·OP 후속.',
'PAN-C1':'기대값 선행 노출; 질문의 목적값과 조작한 flag값을 연구자가 매핑; 2.11.3.2 실행 없음.',
'PAN-C2':'동일 출력 탐색 뒤 선정; 2.11.3.2 실행 없음; fixture 밖 일반화 불가.',
'GDAL-C1':'3.2.1 실행 없음; analytic nearest 가정 명시. 실제 실행은3.10.3.',
'GDAL-C2':'3.2.1 전체 raster/metadata/file 동일성 미확인;20×20 밖 크기는 별개.'}
for cid in initial:
    unknown[cid]=unknown[cid].replace('최초판·','')
unknown['PAN-C1']='기대값 선행 노출; 질문의 목적값→조작 flag 매핑. 오늘 수행한 고정판 실행으로 출력은 재현.'
unknown['PAN-C2']='동일 출력 탐색 뒤 선정. 고정판 실행은 재현했으나 fixture 밖 일반화 불가.'
observed={
'PAN-N1':'OP 목적 반복; 선택 필드 새 값·적용 성공 없음.',
'PAN-N2':'OP의 다른 기술 필드 진단; maintainer fix 보고는 OP 성공 아님.',
'PAN-N3':'댓글 없음(조회 시).',
'PAN-N4':'댓글 없음(조회 시).',
'GDAL-N1':'다른 조언을 시도할 계획; 완료 아님.',
'GDAL-N2':'다른 설정 제거로 해결했다는 같은 댓글 보고1건.',
'GDAL-N3':'WKT에 EPSG를 명시할 계획; 완료 아님.',
'GDAL-N4':'제3자 로그; OP 후속 없음.'}

out=['# AF-RES-074 결과 — PARTIAL\n','## 표 1. 요구·후보·독립 기준\n']
t1=[]
for p in packets:
    cid=p['case_id'];nat=p['stratum']=='natural'; c=criteria[cid]
    opening=link(p.get('initial_url') or urls(c)[0],'원요구 현재판' if nat else '공식 고정 시험')
    if nat:opening+='; '+link(initial[cid]['archive_url'],'opened '+initial[cid]['event_id'])
    version=p.get('version') or p['known_values'].get('version',str(p['known_values'].get('versions','v3.2.1')))
    known=p.get('known_field_value',p.get('disclosed_value'))
    if cid=='PAN-N2':known='원문: font/quote 보존 목적; literal lang 의무 미확인(사후 수정)'
    knowntext=('원문 기지값='+str(known)+'; ' if known else '선택값 미확인/가림; ')+p['field']+' → '+str(p['values'])
    ca='; '.join(link(p['candidate'+str(i)]['url'],'후보'+str(i))+' §'+p['candidate'+str(i)]['section']+' — '+p['candidate'+str(i)]['action'] for i in [1,2])
    t1.append([cid+' · '+('자연' if nat else '대조'),opening+'; '+('최초판 사후 회수·목적 일치; ' if nat else '태그 고정; ')+str(version)+'; '+goal(p),knowntext,ca,evidence_short[cid],unknown[cid]])
out.append(table(['요구 ID·자연/대조','최초판·목적','이미 안 값/가린 필드','후보 1·2 원문 주소와 절','독립 판별 입력·출력','미확인'],t1))
out.append('\n## 표 2. 모든 값·무응답에서 A/B/C가 주는 답\n')
t2=[]
for p in packets:
    cid=p['case_id']; cr=criteria[cid]
    for branch,branchlabel in [('value1','① '+p['values'][0]),('value2','② '+p['values'][1]),('no_answer','무응답')]:
        rr=[pol[f'{cid}-{x}-{branch}'] for x in 'ABC'];ss=[scores[x['row_id']] for x in rr]
        stat='; '.join(x+'='+labels[s['status']] for x,s in zip('ABC',ss))
        if ss[0]['inconsistent_counterfactual']=='true':stat+='; 현재 원문과 충돌하는 반사실'
        if p['stratum']=='natural':stat+='; 전체 목적의 정오 분모0'
        action='링크 참조(A/B/C)='+ '/'.join(r['displayed_link_references'] for r in rr)+'; C 질문1회 예정, 가상 완료왕복'+rr[2]['completed_reply_rounds_in_scenario']+'회; 실제 대화0회'
        t2.append([cid+' · '+branchlabel,answer(rr[0]),answer(rr[1]),answer(rr[2]),'; '.join(link(u,'기준'+str(i+1)) for i,u in enumerate(dict.fromkeys(urls(cr)))),stat,action,observed.get(cid,'구성 쌍; 사람에게 제시하지 않아 선택 미측정.')])
out.append(table(['요구·값 또는 무응답','A 단일 링크','B 조건부 링크·선택 가능성','C 질문 뒤 답','정답 근거 주소','오류/보류/판정 불가','추가 행동·왕복','실제 사람의 별도 후속'],t2))
out.append('\n## 표 3. 모집층·정책별 분모와 분류\n')
t3=[]
for r in rows('policy-summary.csv'):
    branch={'value1':'①','value2':'②','no_answer':'무응답'}[r['response_branch']]
    tags='맞음 '+r['correct_single']+' / 조건부 '+r['conditional_actionable']+' / 틀림 '+r['wrong']+' / 보류 '+r['hold']+'; 열거 '+r['enumeration_unresolved']+' / 판정 불가 '+r['unjudgeable']
    natural=r['stratum']=='natural'
    missing='확인0·미확인8' if natural else '확인0(조건부 B로 왕복 생략 가능)'
    t3.append([('자연' if natural else '대조')+'·'+r['policy']+'·'+branch,r['total_slots'],'기술 '+r['technical_judgment_denominator']+' / 최초시점 효과0',tags,'과잉 확인'+r['avoidable_questions']+'·미확인'+r['avoidable_question_unknown']+'; 필요 질문 누락 '+missing,'미측정 — A/B/C 제시 없음','완성 산출물·별개 사용 결과 결손; 최초판은 사후 회수' if natural else '구성 기술 시나리오; 사람 효과/빈도 아님'])
out.append(table(['모집층·정책','전체 자리','독립 판정 가능 분모','맞음·조건부 사용 가능·틀림·보류','과잉 질문/필요 질문 누락','관측한 사용자 선택','미확인'],t3))
out.append('''
표 1은12요구, 표 2는36시나리오(각 A/B/C를 합쳐108원장행), 표 3은18집계행이다. 원장은 [packets.jsonl](packets.jsonl), [policies.csv](policies.csv), [criteria.csv](criteria.csv), [scores.csv](scores.csv), [policy-summary.csv](policy-summary.csv)로 역추적한다. 자연군의 `보류/열거`는 문장을 읽고 분류한 다음 행동이며, 정오 검증을 통과한 완료 수가 아니다. 분모0의 오류0을 오류율0으로 읽으면 안 된다.

대조의 알려진 두 값에서는4쌍×2값×3정책=24개의 기술 판정 시나리오가 있다. 분모는 **그 시나리오의 독립 기준 확보 여부**다. A가 보류한 경우에도 알려진 목표의 기준은 있으므로 분모에 남기되 정답이나 오답으로 바꾸지 않는다. 무응답의 양성 사례는 목표 자체가 선택되지 않았으므로 A/C의 단정·보류를 완료 정오 분모에서 제외한다. 명시적 B가 스스로 조건을 골라 실행할 경로를 남기는지는 별도로 판독할 수 있다. 어떤 행도 실제 사람의 응답확률이나 정책 효과율을 뜻하지 않는다.

## 핵심 판단과 수용 상태

**최종 상태는 PARTIAL이다.** 같은 입력·판에서 값 하나가 출력을 가르는 경우와, 달라도 공통 행동이 충분한 경우를 모두 확인했다. 최초 요청8건은 사후에 모두 복구했고 Pandoc 고정판 실행도 수행했다. 남은 계약 결손은 공유 열람 예산 초과, PAN-C1의 질문 목적값과 조작 설정값 불일치, 기대 출력 노출 뒤의 Pandoc 대조 선정, GDAL-N3의 후보 혼합판이다. 이를 사전 조건을 충족한 실험으로 바꾸지 않았다. 자연군의 완료 기준·사람 후속 효과가 미확인인 것은 별도로 허용된 관측 한계이며, 새 사람 실험을 하지 않았다는 이유로 PARTIAL이라고 판정한 것은 아니다.

**질문의 기술적 판별력과 질문을 해야 할 필요성은 다르다.** 양성2쌍에서는 값에 따라 올바른 명령이 달라지지만, B도 조건을 설명하고 사용자가 자기 목적을 알 때 같은 선택을 전달한다. C가 후보2개를1개로 좁혔다는 사실만으로 B의 오류를 줄였다고 세지 않는다. 음성2쌍에서는 두 명령 표현을 공통 행동으로 정규화할 수 있어 C가 선택을 바꾸지 않는다. 자연군3건은 현재 본문에 목적이 이미 있는데도 이를 다시 묻도록 설계했고, 한 건의 ‘보존 의무’는 연구자의 과한 해석이라 철회했다. 근거는 위12개 기준 행과 아래 Q별 반례다.
''')
out.append(f"\n직접 판독 접근 원장은 **{counts['source_rows']}행**, 지정 네 범주에 산입한 중복 없는 원저작은 **{counts['minimum_independent_works']}개**다. 범주별로 요청 {counts['minimum_by_category']['request']}개, 공식 시험·예제 {counts['minimum_by_category']['test_example']}개, 명세·매뉴얼·변경 공지 {counts['minimum_by_category']['spec_manual']}개, 다른 분야 절차 {counts['minimum_by_category']['crossfield_procedure']}개다. 구현 코드6개를 더한 보수적 직접 원저작 계보는 {counts['direct_independent_works_conservative']}개다. 같은 GDAL 사용자 매뉴얼의 모든 페이지·판을1개로 합쳤고, 댓글·중복 이슈·시험의 입출력 fixture는 새 저작으로 세지 않았다. 이는 원저작 계보 수이며, **선정 자연8건의 최초판은8건 모두 사후 복원**했다. 본문6건은 바이트 동일,2건은 문법·표현 차이만 확인됐다. 실패 접근12행은 과거 실패 시도의 기록을 포함하며 현재 원선정8건이 미회수라는 뜻이 아니다. [sources.jsonl](sources.jsonl), [계수 영수증](evidence/ledger-counts.json).\n")
out.append('\n## Q1. 원래 끝내려던 일과 이미 공개한 값\n')
q1quotes={'GDAL-N1':'semi_major and semi_minor WKT parameters are ignored','GDAL-N2':'gdalinfo works on ENVI / SNODAS File','GDAL-N3':'a change in how GDAL identifies EPSG equivalence','GDAL-N4':'generate an output file when it runs into an error'}
out.append(table(['요구','직접 읽은 짧은 원문·판','목적·입력·산출물 경계'],[[p['case_id'],link(p['initial_url'],'현재 본문')+' — “'+(p.get('initial_quote') or q1quotes[p['case_id']])+'”',goal(p)+'; 알려진 값: '+cell(p['known_values'])] for p in packets if p['stratum']=='natural']))
out.append('''
첫 요청의 exact-hour 아카이브 접근은 처음에8건 모두403이었다. 추가 모집에서 같은 공개 경로의 접근이 성공한 뒤 원래 URL을 일반 HTTPS로 다시 요청해8개 opened 이벤트를 모두 회수했다. **6건은 본문 바이트가 같고, PAN-N2는 두 문법 수정, GDAL-N2는 제목 마크업과 문장 표현 수정만 달랐다. 목적·제약·선택 필드의 의미 변화는0건이다.** 위 인용은 현재 본문 판독으로 기록했고, 이제 최초 본문과의 일치 범위를 [initial-version-review.csv](initial-version-review.csv)에서 함께 확인할 수 있다. 과거403 기록과 실제 사후 회수UTC는 모두 보존했다. 수정 시각만으로 원문 불변을 가정하지 않았다.

초기에 최초판 적격을 확인하지 못했으므로 고정 검색식의 다음12건씩도 읽었다. 추가 모집은 `streams/*/frame-extension.json`의 순번13–24이며, 댓글을 보고 원래8사례를 바꾸거나 정책 효과 분모를 늘리지 않았다. 원선정8건이 뒤늦게 최초판을 회수하고 목적도 일치했으므로 교체할 이유가 없었다. 추가 사례에는 실제로 최초·현재 목적 범위가 달라진 경우도 있어 현재판을 과거로 소급하지 않는 규칙의 필요성을 확인했다.

Git의 최초 예제도 항상 고정 판과 같지 않았다. [parse-raw 최초2017판](https://github.com/jgm/pandoc/blob/47a16065c44eb5028ca9b9e86993fe880ef2a37d/test/command/parse-raw.md)은2.11.3.2의 저장 텍스트와 달라 해당 태그의 기대값을 사용했다. [sloppypar 최초2018판](https://github.com/jgm/pandoc/blob/16523ea3d15f4a6705fc4711d1378a54abbcfe1d/test/command/sloppypar.md)은 고정 판과 전체 파일 해시가 같았다. 같은 예제의 다른 판은 원저작 수를 늘리지 않았다. GDAL은3.2.1에 입력·명령·기대 기준을 고정했으며 해당 시험의 최초 도입판까지 확보했다고 주장하지 않는다. [Git 최초판 대조](streams/pandoc/test-origin.json).
''')
out.append('\n## Q2. 사전 필드·질문·바뀌는 행동\n')
out.append(table(['요구','사전 선택 필드와 질문','값①→②와 행동 변경','사후에 드러난 경계'],[[p['case_id'],p['field']+' — '+p['question'],str(p['values'])+'; '+str(p['candidate1'].get('command'))+' → '+str(p['candidate2'].get('command')),unknown[p['case_id']]] for p in packets]))
out.append((P/'tools/result-analysis.md').read_text())
out.append('\n## Q8. 요구별 비용·남는 행동과 다른 분야 비교\n')
costrows=[]
for r in rows('costs.csv'):
    nat=r['stratum']=='natural'
    wrong='판정 불가/분모0' if nat else r['A_known_wrong']+'→'+r['C_known_wrong']+' (각2값 기준)'
    valid='미확인' if nat else r['potentially_valid_candidate_commands_no_answer']+'명령 / '+r['distinct_valid_action_classes_no_answer']+'행동류'
    links='/'.join(r[x+'_link_references_no_answer'] for x in 'ABC')+'참조; '+ '/'.join(r[x+'_distinct_documents_no_answer'] for x in 'ABC')+'문서'
    fallback='; '.join(x+'='+labels[r[x+'_no_answer_status']] for x in 'ABC')
    costrows.append([r['case_id'],wrong,valid,links,'A0/B0/C1질문 예정; 무응답 완료왕복0',fallback,r['C_avoidable_question']])
out.append(table(['요구','틀린 행동 A→C','무응답의 잠재 유효후보/행동류','검사 링크·문서 A/B/C','추가 왕복','무응답 때 남는 행동','C 과잉 질문'],costrows))
out.append((P/'tools/result-crossfield-ending.md').read_text())
(P/'RESULT.md').write_text('\n'.join(out)+'\n')
print(json.dumps({'result_bytes':(P/'RESULT.md').stat().st_size,'table1_rows':len(t1),'table2_rows':len(t2),'table3_rows':len(t3)},ensure_ascii=False))
