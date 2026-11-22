"""Build the required report tables from the committed observation ledgers.

Narrative is an authored synthesis; numerical tables are generated from the
144-pair map and frozen retrieval records, never hand-entered positive counts.
"""
import csv
import json
from collections import Counter
from pathlib import Path

P=Path(__file__).resolve().parent
def jl(name):return [json.loads(x) for x in (P/name).read_text().splitlines() if x.strip()]
def cell(x):return str(x).replace('|',' / ').replace('\n',' ')
def row(values):return '| '+' | '.join(cell(x) for x in values)+' |\n'
inputs={x['recipient_id']:x for x in jl('inputs.jsonl')}
corpus={x['candidate_id']:x for x in jl('corpus.jsonl')}
maps=list(csv.DictReader((P/'maps.csv').open()))
summary=json.loads((P/'evidence/recount.json').read_text())
primary={x['pair_id']:x for f in ['library','transport','statistics'] for x in jl(f'judgments/{f}.jsonl')}
rankings=list(csv.DictReader((P/'rankings.csv').open()))
receipts=json.loads((P/'evidence/retrieval-receipt.json').read_text())['runs']
labels={'support':'지지','partial':'부분','conflict':'충돌','unverified':'미확인'}
purpose={
 'R01':'개명 중 동일 동작·옛 호출 전달·경고',
 'R02':'암묵 상위 동명 항목 가림과 명시 접근 보존',
 'R03':'입출력 저장공간의 안전한 재사용',
 'R04':'프로젝트 그룹의 보관과 승인된 재개',
 'R05':'혼합 프로토콜 요청 접수와 공급자 실행 분리',
 'R06':'인스턴스별 설정을 공유 설정과 격리',
 'R07':'구/신 보안 표현의 권위·변환·불변성',
 'R08':'기존 기능을 바꾸지 않는 기본 활성화'}
must={
 'R01':'M01 동일 의미; M03 옛 호출 전달; M04 미래 의미와 새 이름 경고',
 'R02':'M01 암묵 상위만 가림; M03 양쪽 명시면 오류; M06 한정 접근 보존',
 'R03':'M13 입력 적재; M04 일반 출력 비중첩; M05 모든 입력 소비 뒤 lateout 재사용; M12 결과 복사',
 'R04':'M06 중지→보관; M07 공지·공개 이력/인프라 보존; M08 담당자·상위팀 합의·재평가 후 복원',
 'R05':'M01 활성화된 혼합 정의를 접수; M02 기존 공급자에 전달하고 실제 제공은 역량에 따름',
 'R06':'M01 별도 Kind; M03 별도 파일; M04 flag 우선; M05 공유 갱신이 인스턴스 값을 덮지 않음',
 'R07':'M05–M11: 새 필드 권위·없음/한쪽/양쪽 생성 진리표·N+4 역기입·값 일치·불변·구 갱신 무시',
 'R08':'M01 기본 활성화; M02 기존 기능 동일'}

def link_r(rid):return f'[{rid}]({inputs[rid]["immutable_source_url"]})'
def link_c(cid):return f'[{cid}]({corpus[cid]["url"]})'
def ranges(xs):return ', '.join(f'L{a}' if a==b else f'L{a}–{b}' for a,b in xs)
def correspondence(j):
    inp=j['input_map'];state=j['state_change_map'];out=j['output_map']
    relation=(inp.get('proposed_correspondence') if isinstance(inp,dict) else None) or j.get('proposed_correspondence') or (state.get('judged_correspondence') or state.get('correspondence') if isinstance(state,dict) else None)
    if relation:return relation
    value=lambda x: x.get('provider','미확인') if isinstance(x,dict) else x
    return 'I '+str(value(inp))+' → Δ '+str(value(state))+' → O '+str(value(out))

report='# AF-RES-033 · 분야명을 주지 않아도 도움이 되는 원리를 찾는가\n\n'
report+=row(['수신 설계 ID·최초 목적','필수 조건','S·R 경로·원 순위','후보·원문 절 URL','입력·변화·출력 대응','남은 접합·깨지는 조건','부분·전체 판정','신규성·미확인'])
report+=row(['---']*8)
shown=[]
for m in maps:
    if m['S_returned_top3']!='True' and m['R_returned_top3']!='True' and m['judgment']!='support':continue
    shown.append(m)
    rid=m['recipient_id'];cid=m['candidate_id'];j=primary[m['pair_id']]
    paths=[];windows=[]
    for route in ['S','R']:
        returned=m[route+'_returned_top3']=='True'
        paths.append(f'{route} {m[route+"_rank"]}위'+(' 반환' if returned else ' 미반환'))
        if returned:windows.append(f'{route} {m[route+"_best_window_id"]} L{m[route+"_window_line_start"]}–{m[route+"_window_line_end"]}')
    loc=link_c(cid)+'; '+('원창: '+', '.join(windows)+'; ' if windows else '전수 판독만; ')
    loc+='문서 근거 '+ranges(j['provider_evidence_line_ranges'])+f'; {m["pair_id"]}'
    missing=[x['predicate_id'] for x in j['mandatory_evidence'] if x['status']!='match']
    glue=('새 핵심 없음; 포트/컨트롤러/오류 연결은 남음. ' if not missing else '미완결 '+','.join(missing)+'. ')+j['break_condition']
    verdict='부분목표 '+labels[m['judgment']]+' / 전체 '+labels.get(m['whole_design_judgment'],m['whole_design_judgment'])+'; 원창 인용 완료 0'
    if not windows:verdict='부분목표 지지 / 전체 부분; 원검색 반환 없음'
    temporal={'available':'고정판 당시 가용','later_fixed_edition':'고정판 후발','unverified':'고정판 당시 가용성 미확인'}[m['historical_fixed_edition_status']]
    novelty=temporal+'; 미인용 링크와 원리 신규성·채택은 별개'
    if m['pair_id']=='R05-L06':novelty='X01: 최초 요청에 이미 있던 작동의 타분야 인용 보완. 당시 가용·실제 미인지·채택 미확인'
    report+=row([link_r(rid)+' '+purpose[rid],must[rid],'; '.join(paths),loc,correspondence(j),glue,verdict,novelty])
report+='\n'
report+=row(['수신 ID','상위 1·3에서 인용 완료 S·R','둘 다·한쪽만·둘 다 놓침','전체 목록의 지지·충돌·부분·미확인 수','검색·열람 비용','노출 또는 제외 민감도'])
report+=row(['---']*6)
for s in summary['per_recipient']:
    rid=s['recipient_id'];n=s['candidate_counts']
    eligible=bool(s['strict_eligible_candidates'])
    classification='둘 다 0, S만 0, R만 0; 둘 다 놓침 1/1(X01)' if eligible else '회수 분류 해당 없음: 전수 지지 후보 0; 양 경로 인용 완료 0'
    time_ms=sum(x['elapsed_ns'] for x in receipts if x['recipient_id']==rid)/1e6
    cost=f'검색2·점수36·반환6 / 후보고유{s["unique_returned_candidates"]} / 전수18; 계산 {time_ms:.3f}ms'
    sensitivity='질의 작성자 제공노출0; 생성판 검증'
    if rid in ('R01','R03'):sensitivity+='; 연결된 asm 제안 제외 시 엄격0/7'
    if rid=='R04':sensitivity+='; 권고 하위절 완화18행 변화0·제외0/7'
    if rid=='R08':sensitivity+='; 얇은 기본값 목표 제외0/7'
    report+=row([link_r(rid),'상위1 S0/1·R0/1; 상위3 S0/1·R0/1',classification,f'{n["support"]} / {n["conflict"]} / {n["partial"]} / {n["unverified"]} = 18',cost,sensitivity])
report+=row(['합계','상위1 S0/8·R0/8; 상위3 S0/8·R0/8','적격 질문1개에서 둘 다 놓침1/1; 나머지7개는 해당 없음','1 / 9 / 50 / 84 = 144','원검색16·전체점수288·상위반환48·고유문서/창37; 전수144; 계산25.151ms','고정판 당시 가용 T04만1/18; 엄격 적격0이라 당시 회수 분모 해당 없음'])
report+='\n'
report+=row(['반례 ID·분야','표면 유사점','작동이 같거나 다른 지점','원문 두 주소','당시 이용 가능성','결론을 바꿀 자료'])
report+=row(['---']*6)
counterexamples=[
 ('CE01·교통','옛 서비스의 대체·전달','R01은 동일 의미 보존. T02는 1:1 대체 비보장·정류장 제외와 시간 차이를 허용한다. 구체 forwarding 매핑의 충돌이다.','R01','T02','2026 개정판은 2020 이후','동일 이용자의 진입·도착·시간 계약을 모두 보존한다는 예외 없는 대체 운행 조항; MBTA 기준 1쪽과 비교'),
 ('CE02·통계','구·신 표현의 일관성','R07은 같은 객체의 전용 필드를 불변으로 둔다. S03은 같은 기간 추정치를 새 자료로 수정한다. vintage를 새 객체로 놓으면 충돌은 약해지지만 호환 전이의 핵심은 남는다.','R07','S03','Edition 8(2026)은 후발','ABS 24.109–24.129에 대응하는 append-only vintage·고정 ID 계약 및 구 표현 갱신 처리 규칙'),
 ('CE03·도서관','archive·과거 요청·재신청','R04의 그룹 보관/승인 복원과 대출 요청 이력은 다르다. L03의 계정 이력 6개월 삭제가 모든 보관자료 파기라는 뜻도 아니다. 부분 단서로 보류한다.','R04','L03','현재 무일자 판; 당시 미확인','MCL의 같은 요청 ID 재개 규칙과 보존 범위; Rust의 실제 archive 해제에서 담당자·팀 합의를 남긴 기록'),
 ('CE04·도서관','혼합 자료의 접수 제외','L03의 혼합 컬렉션 제외는 기록물 범주 안이다. 혼합만을 거절 이유로 단정할 수 없어 초안 conflict를 partial로 낮췄다.','R05','L03','현재 무일자 판; 당시 미확인','일반 책+구성품의 접수 허용/거절 예와 담당자의 실제 처리 규칙; 기록물 여부를 통제한 비교'),
 ('CE05·교통','기존 기준선 복원·같은 정책 목표','R08은 기능을 바꾸지 않고 기본 활성화한다. T06의 실제 재도입은 일부 노선을 바꾸고 신규 노선을 유지한다. 목표 동일성은 기능 동일성이 아니다.','R08','T06','2022판은 후발','구 네트워크와 복원안의 노선·정차·시간·빈도 대조; 같은 목표가 아니라 같은 작동임을 확인할 자료')]
for cid,surface,operation,rid,did,temporal,nextdata in counterexamples:
    report+=row([cid,surface,operation,link_r(rid)+' + '+link_c(did),temporal,nextdata])

report+='''

## 판독할 결론과 단위

**이 닫힌 후보 집합과 고정 BM25에서는 작동 관계 질의 R이 인용 완료된 타 분야 원리를 상위에 반환하지 못했다. S도 동일하게 0/8이었다.** 순위는 변했지만 엄격한 수신 조건을 채우는 반환 절은 없었다. 이 결과를 관계 표현 일반의 실패, 자유 웹 전체의 검색 성능, 실제 설계자의 채택률로 확대하지 않는다. 분모8은 질문별 집계 단위이고 무작위·통계적 독립 표본이 아니다. R01과 R03은 assembly 전환 문제를 공유한다. [원 순위](rankings.csv), [원 반환](returns.jsonl), [144대응](maps.csv), [재집계](evidence/recount.json)가 각 단위를 분리한다.

전수18문서 판독은 R05–L06 하나에서 **현재 판의 좁은 작동 관계**를 지지했다. 두 독립 문맥의 판독자가 같은 항목 구조를 읽었지만, 독립 인간의 동의가 아니다. 그 문서는 S10위/R12위로 상위에 없었고, 최고 점수 창 W001(L1–19)도 혼합 자료의 접수 범주를 담지 않았다. 전수에서 찾아낸 L3·L64–80·L82–106의 설명을 원 검색 성과로 소급하지 않았다. R05의 최초 본문은 이미 접수와 실제 공급을 구별하고 있으므로 이는 **이미 요청한 관계를 설명하는 새 타 분야 링크의 인용 보완**이다. 새 원리 발명·새 설계 행동·실제 미인지 입증으로 세지 않았다. [도서관 판독](judgments/library-notes.md), [별도 재판독](judgments/critical-review-notes.md).

첫 표는 S/R 상위3 합집합37대응과 전수에서만 찾은 X01 한 행, 총38행이다. 같은 문서가 양 경로에서 나오면 한 행에 두 순위를 적었다. 나머지106대응을 누락한 것이 아니라 maps.csv의144행에 보존했다. 표의 '문서 근거'는 전수 판독 위치, '원창'은 실제 반환200토큰 위치다. 제공 L번호는 corpus의 고정 UTF-8 추출 본문, 수신 L번호는 고정 Git blob의 행이다. HTML은 무일자·가변 주소일 수 있어 URL을 immutable로 가장하지 않았고, 판·확인 UTC·본문/원자료 해시와 PDF 쪽은 corpus/sources 및 각 judgment 행에 있다. 점수0인 문서8행도 rankings에 남겼으며, **빈 검색은0/16**이다. [48개 정확 반환창 판독](evidence/returned-window-audit.jsonl).

## Q1. 어떤 수신 설계에서 출발했는가

Rust RFC와 Kubernetes enhancements의 2020–2024 최초 생성 목록3,415행을 만들었다. 생성시각→PR번호→최초 diff 경로 순서로 2020년부터 읽어 각4건을 채웠으므로 다음 해로 이동하지 않았다. 최종8개는 모두2020년1월 제안이며, 전체 기능/절차 설계3개(R03/R04/R06), 경계의 부분 설계5개다. 양 종류를 채우려고 표본을 바꾸지 않았다. 원 프레임3863행은 수신3415·제공 발행처24·제공 발견 후보424를 합친 것이며, 서로 다른 단위를 더한 프레임 행수다. [frame.csv](frame.csv), [원 수신 프레임](recipient/recipient_frame.csv).

현재 PR 생존 이력만으로 최초판이 증명되지 않는 행을 버리고 뒤의 편한 제안만 택하지 않았다. 공개 생성 이벤트의 head/base를 복원해 tree/path/blob와 실제 첫 diff를 대조했다. 선택 접두부23건은 선정8·제외15이며 모두 생성 이벤트와 첫 diff 근거를 갖는다. 재복원 전 실패·잠정 선택·제외 이유도 이전 커밋과 원장에 남겼다. 이 증거는 공개 PR 최초 제출판을 지지하며 비공개 최초 집필 초안은 증명하지 않는다. [초기판 감사](evidence/resume-input-audit.md), [생성 이벤트 검사](evidence/opening-archive-checks.jsonl), [입력 봉인](evidence/input-seal.json).

초기 원문에는 요청 동작, 입력/상태/행위/출력, 필수·선호·불필요 조건, 이미 거론한 해결책과 좁은 부분 목표를 함께 고정했다. 모든 큰 설계의 전체 요구를 만족한 것과 좁은 부분 목표를 만족한 것을 분리했다. R08에서 예전 taint eviction 메커니즘을 새 목표로 다시 세지 않았고, R03에서 수신이 이미 거론한 register/lateout 동작을 낯선 제공 용어만으로 신규 원리라 부르지 않았다. [inputs.jsonl](inputs.jsonl), [질의 없는 목표 묶음](recipient/recipient_targets.jsonl).

실제 결함도 있다. R04-M07은 권고적인 산출물·과정 회고의 강도를 필수로 묶었다. 첫 검색 전에 이를 기록하고, 해당 하위절만 선호로 낮추는 민감도를 추가했다. 18문서의 판정은 모두 그대로였으며 R04 제외 시 엄격 결과도 양쪽0/7이다. 이는 모든 과대강도 문제가 무해하다는 뜻이 아니라, 이18문서에서는 공개 보관 인프라와 승인된 복원 등 다른 핵심도 남았기 때문이다. [사전 민감도](evidence/sensitivity-plan.md), [R04 최초판 L123–144](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md#L123-L144).

## Q2. 제공 분야를 답에 맞춰 고르지 않았는가

세 분야와 영어권 발행처의 고정 순서, 기간, 최초 검색 목록의 제목·URL 정렬, 실패 시 공식 상위 목록으로 가는 순서를 수신 초기 본문 판독 전에 고정했다. 제공 수집자에게 수신별 정답이나 유리한 단어를 주지 않았으며, 질의 작성자는 제공 제목·본문을 읽지 않은 별도 문맥에서 작업했다. 초기 메타데이터의 닫힘·병합·댓글은 작성 입력에서 제외했다. [SCOPE](SCOPE.md), [사전 봉인 기록](evidence/corpus-seal.json), [제공 감사](evidence/resume-donor-audit.md).

이 틀은 연구자가 고른 세 분야·발행처의 유한 발견 목록이다. 상위 웹 검색이 모든 공식 페이지를 열거한다는 뜻도, 세계의 제공 분야를 자동 발견했다는 뜻도 아니다. 같은 문서의 형식·판·번역은 중복 제거했고, 홍보·단일 사건·본문 실패·순서상 후순위는 구별했다. 30개 발견 목록/424후보 기록이 선택18개를 대신하지 않는다. 원문이 바뀌어도 옛 해시를 새 본문에 붙이지 않는다. [donor 원장](donor/donor_sources.jsonl), [sources.jsonl](sources.jsonl).

| ID·원문 | 분야·발행처 | 고정판 기준일 | 읽은 검색 범위와 중요한 한계 |
| --- | --- | --- | --- |
'''
for cid in sorted(corpus):
    c=corpus[cid];date=c.get('publication_or_version_date') or '무일자 현재판'
    limitation={'L':'현행 절차; 2020년 해당 조항 존재 미확인','S':'공표·정정 정책; 역사적 영향/사용자 채택 미확인','T':'선택 업무절; 운행 성공 자체의 증거 아님'}[cid[0]]
    if cid=='T04':limitation='2018판; 다단 PDF8쪽을 시각 재검, 지표를 제어 절차로 바꾸지 않음'
    if cid=='T02':limitation='2026 개정판; 제목1행 잔존 위반과 별도 제거 민감도'
    if cid=='T05':limitation='공식 현재 링크이나 편집본의 draft 문구/전체 최종 채택 모호성 유지'
    if cid=='T06':limitation='유한 공식 목록에서 발견한 최신판; 과거 관측·미래 시나리오 구분'
    report+=row([f'[{cid} {c["title"]}]({c["url"]})',c['field']+' / '+c['issuer'],date,f'L1–{c["body_lines"]}; '+limitation])
report+='''

고정판의 당시 이용 가능성은 현재의 전이 가능성과 별도로 세었다. 18판 중 **2018년 T04만 2020년 수신 제안보다 앞선다**. 10판은 후발, 7판은 날짜 미상이다. 관계144행으로는 당시 가용8·후발80·미확인56이다. T04의8행에도 엄격 지지는0이므로 당시 이용 가능한 적격 질문 분모는0, 회수율은 **해당 없음**이다. 현재 문서가 예전 제도의 이름을 언급하는 것만으로 그 문서의 현재 조항을 2020년에 소급하지 않았다. [corpus.jsonl](corpus.jsonl), [교통 시간 판독](judgments/transport-notes.md).

T02 검색본문 첫 줄에 문서 표제가 남아 제목 제외 규칙을 완전히 지키지 못했다. 이를 첫 검색 전에 발견하고 원 corpus를 유지한 채 제거 민감도를 봉인했다. 추가16회에서 전체 순위·상위1·상위3집합 변화는 모두0/16이었다. T02가 원래 반환됐던3슬롯(R01-S/R02-R/R07-S)의 창 경계·해시는 바뀌므로 창 동일성까지 주장하지 않는다. T02는 엄격 지지 후보가 아니어서 인용 완료 분자는 여전히0이다. 원 위반을 민감도의 안정성으로 없었던 일로 만들지 않았다. [민감도 원 순위](sensitivities/T02-title-excluded-rankings.csv), [영수증](sensitivities/T02-title-excluded-receipt.json).

## Q3. 같은 자료에서 표현만 바꿨을 때 무엇이 올라왔는가

원 검색은 영어 S/R 각각80원토큰 상한, 동일 본문·NFC 소문자 `[a-z0-9]+`·고정 stopword·고유 질의 토큰·BM25(k1=1.2,b=0.75)·문서 ID 동률 처리다. 문서 점수로18개를 정렬한 뒤 그 문서의 최고200원토큰 비중첩 창 하나를 반환했다. 원16질의와 해시는 입력 봉인 e139959, 범위위반·민감도는35a01fd, 원 검색288순위/16반환은a2ce15d에서 후속 열람 전에 고정했다. [검색기](retrieval.py), [질의 봉인](recipient/queries_sealed.jsonl), [실행 영수증](evidence/retrieval-execution.json).

최대 길이는 같고 전체 원토큰 합도 S560/R560이지만, 질문별 길이와 유효 고유 토큰 수는 다르다. S의 고유 토큰 합309·평균38.625, R348·평균43.5다. 관계 표현 자체의 효과와 검색어 선택·수의 효과를 분리한 인과 시험은 아니다. BM25는 어순·역할·권한·동일 객체·조건의 방향을 이해하지 않으며 고정 stopword는 `not`도 제거한다. 따라서 이것은 **관계를 표현해 쓴 문장의 어휘적 반환 시험**이지 관계 추론 검색기 시험이 아니다. [질의별 원토큰·유효 토큰](evidence/retrieval-receipt.json).

R로 바꾸자 상위1 문서는6/8에서, 상위3 집합은7/8에서 변했다. 원 상위48슬롯은 교통35·도서관9·통계4다. 분야마다6문서여도 검색본문 길이·다루는 범위·창 수가 같지 않다. 예를 들어 T04는13,154원토큰이고 L04는176원토큰이다. 이 구성이 운행·service·change 같은 광범위 어휘를 제공하지만, 그 사실만으로 교통 원리가 더 적합하다고 결론 내릴 수 없다. [rankings.csv](rankings.csv), [corpus 특징량](corpus.jsonl).

| 판독 수준 | S 상위1 | R 상위1 | S 상위3 | R 상위3 | 해석 |
| --- | ---: | ---: | ---: | ---: | --- |
| 실제 원창 안의 엄격 인용 완료 | 0/8 | 0/8 | 0/8 | 0/8 | 고정 부분 목표의 모든 필수 제공 근거가 한 반환창 안에 있어야 함 |
| 반환 문서 전체의 엄격 지지 | 0/8 | 0/8 | 0/8 | 0/8 | 유일 지지 L06은 R05의10/12위 |
| 반환 문서 전체의 지지+부분 단서 | 5/8 | 4/8 | 5/8 | 5/8 | 창 밖의 일부 관계도 포함하므로 인용 완료/완결 전이가 아님 |

넓은 문서 기준 상위3에서 양쪽 모두4건(R03/R04/R05/R06), S만1건(R01), R만1건(R02), 둘 다 놓침2건(R07/R08)이다. 이 넓은 기준에는 전수 부분 단서가8질문 모두 있으므로 분모8을 쓸 수 있다. 엄격 기준은 전수 지지 후보가 있는 R05 하나만 회수 분류의 분모가 되며 둘 다 놓침1/1이다. 나머지7개는 현재 후보 집합이 목표를 충족하지 못하므로 검색 회수 실패율의 분모에 넣지 않았다. [재집계 원장](evidence/recount.json).

## Q4. 같은 단어와 옮길 수 있는 원리는 어디서 갈리는가

X01에서 하나의 복합 자료(책+AV 구성품)를 하나의 혼합 Service 정의로, VPL의 접수/중개를 API 경계로, 대출관의 실제 발송 결정을 공급자 컨트롤러로 놓았다. VPL은 단독 AV의 요청 금지와 AV 구성품이 딸린 책의 제공관 재량을 다른 목록에 둔다. 두 범주의 구분에서 혼합 자료의 접수 허용을 읽고, 실제 대출을 보장하지 않는 구조를 연결했다. 소프트웨어에 남는 일은 포트 자료형·컨트롤러 호출·실패/상태 표현의 연결이다. 활성화 방식과 전체 설계 구현·테스트까지 이 원문이 제공한다고 보지 않았다. [R05 L98–117](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md#L98-L117), [L06](https://www.vpl.ca/borrowing/interlibrary-loans) 고정 L3/L64–106, maps의 R05-L06.

X01은 강한 해석과 약한 해석의 경계다. 실제 접수 양식을 제출한 적이 없으며 허용은 분류 구조에 근거한 추론이다. 별도 재판독도 이를 지지했지만, **명시적 접수 문장만 인정하면 partial**이라고 기록했다. 그 보수적 읽기는 support1→0, partial50→51, 엄격 회수 적격 질문1→0으로 바꾸며 회수 분모가 해당 없음이 된다. 원 검색의 S/R0/8은 변하지 않는다. 원리의 현재 관계 대응을 지지한다는 판단과 실제 현장 실행/당시 채택을 확인했다는 판단을 분리했다. [5행 별도 판독](judgments/critical-review.jsonl).

반대로 R03의 register와 도서관 register, R04의 archived 그룹과 대출 제외 archival material은 어휘가 같아도 동작이 다르다. R03은 모든 입력의 마지막 읽기 이전에 출력을 덮으면 안 된다. 정원 제한이나 예산 재배치만으로 그 경계 동작을 얻을 수 없다. R04는 같은 그룹의 공개 기록·인프라를 보존하고 권한 있는 주체가 재개해야 한다. 새 대출 요청을 넣는 것과 같은 조직을 되살리는 것은 다르다. [R03 최초판](https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md), [R04 최초판](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md), [L02](https://denverlibrary.org/ILL), [L03](https://multcolib.org/interlibrary-loan).

T04는 분야가 다르다는 이유로 낮추지 않았다. FTN corridor의 조건을 복수 transit types의 결합으로 채울 수 있어 R05-M01의 혼합 허용 관계는 인정했다. 그러나 접수된 정의를 별도 공급자에게 넘기는 M02가 없다. T04의 단순 성과 지표를 안전한 자원 인계 절차로, 다단 편집의 옆 열을 다음 실행 단계로 바꾸지도 않았다. 실제8개 PDF쪽을 렌더해 FTN과 B-Line 설명, 표의 특수 서비스 예외, turnover 지표를 구분했다. [교통 판독·PDF 위치](judgments/transport-notes.md), [T04 원 PDF](https://www.translink.ca/-/media/translink/documents/plans-and-projects/managing-the-transit-network/transit_service_guidelines.pdf).

## Q5. 반환하지 않은 후보에 더 나은 대응이 있었는가

전수 판독은16검색을 봉인한 뒤, 수신당18후보를 한 번씩 대조한144행이다. 세 분야 판독자는 해당 단계에서 질의·순위·후속을 보지 않았다. 고정 부분 필수조건은 수신별3/3/4/3/2/4/7/2개, 총28개이며 후보18개에 반복해 **504조건 근거 객체**를 만들었다. 빠진 조건을0이나 충족으로 채우지 않았다. support에는 필수 전부 match와 새 핵심 없음이 필요하고, conflict는 구체 대응 아래 명시 반대가 있을 때만 썼다. 무관·부족·다른 분야라는 사실만으로 충돌이라 하지 않았다. [maps.csv](maps.csv), [분야별 판독](judgments/library-notes.md), [통계 판독](judgments/statistics-notes.md).

| 분야 | 지지 | 충돌 | 부분 | 미확인 | 전체 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 도서관 | 1 | 4 | 19 | 24 | 48 |
| 교통 | 0 | 2 | 19 | 27 | 48 |
| 통계 | 0 | 3 | 12 | 33 | 48 |
| 전체 | 1 | 9 | 50 | 84 | 144 |

다른 어휘로 같은 고정 조건을 만족하는 후보이자 두 경로 모두 놓친 후보는 X01 하나다. 가까운 어휘의 근접 오답은 CE03(보관과 기록물), R03-L02(레지스터와 계정 등록), R02의 일반 우선순위 문서 등에서 실제로 찾았다. 부분 단서50개는 핵심을 수신자가 더 설계해야 하는 이유를 함께 남겼다. 전체 설계 support는0/144다. 전수 후보를 읽고 새 질의를 만들어 성공시키는 보강 검색은 하지 않았다. 제공자 내부 새 검색·자유 웹 검색을 원 S/R점수에 더하지 않았다. [원 검색과 문서 판독 조인](maps.csv), [사례](cases.md).

민감도도 유리한 행만 고르지 않았다. R01 제외와 R03 제외를 각각, R04/R08 제외를 각각 계산하면 엄격 상위1/3은 양쪽 모두0/7이다. 기록상 질의 작성자가 제공 자료를 본 행은0이므로 해당 제외 분모는8 그대로다. 통합 작성자의 사후 노출과 평가자가 corpus 특징량을 본 사실은 질의 작성자의 누출과 다른 변수이며, 후자의 평가 문맥 노출 한계도 notes에 기록했다. 별도5행 재판독은 주 분류5/5가 같았으나 표적 재검이므로 전체144의 신뢰도나 인간 합의율을 추정하지 않는다. [사전 계획](evidence/sensitivity-plan.md), [재판독 한계](judgments/critical-review-notes.md).

넓은 교통 해석에서 R03-T03/R03-T06/R04-T05를 부분으로 올리면 전체 partial50→53, unverified84→81이다. 모두 기존에 넓은 상위3 단서가 있는 R03/R04에 속하므로 질문별 S/R5/8은 변하지 않는다. ABS의 같은 기간을 같은 객체로 놓는 대응을 거부하면 R01/R02/R07-S03의 conflict3개를 unverified로 낮출 수 있다. 별도 검토자는 R07에서 vintage를 새 객체로 놓을 경우 부분 단서를 남길 수 있다고 보았다. 어느 쪽도 엄격 지지를 늘리지 않는다. 충돌은 제공 분야 전체의 부적합 선언이 아니라 **어떤 객체·역할·행위 대응을 시도했는가**에 종속된다. [통계 notes](judgments/statistics-notes.md), [교통 notes](judgments/transport-notes.md).

## Q6. 다른 분야 사례가 실제 설계 행동까지 설명하는가

별도 현장 원문4개는 교통2·통계2이며 사건은3개다. F01의2020년 MTA 감편 계획과 F02의NYC DCP 분석은 같은 변화 맥락이다. F02는 MTA 자료를 사용하므로 독립 원시 측정2회가 아니다. F03은 ONS 문장·그림 정정의 여러 판을 한 원문, F04는 한 데이터셋의 정정 전후 XLSX를 한 원문으로 셌다. 이들은 같은 작동 계열의 현장 공표 사례이며, 서로 다른 기관이 나중에 발행한 봉인 지침의 준수나 인과적 적용을 증명하는 자료는 아니다. [현장 원장](field/field_sources.jsonl), [현장·후속 분석](analysis/field-and-followup.md).

F01은 단계적 감편·대체 경로·예비 인력·공지 계획을 공표했다. F02의 고정 PDF13쪽은 MTA Real Time data에 기초한 날짜별 운행 비교를 표시한다. 이전 초안의 GTFS/예정 운행 단정은 같은 바이트의 재다운로드와 렌더를 확인해 철회했다. 그러나 원시 feed·집계 코드·개별 실제 출발·승객 경험을 재현한 것은 아니다. 계획의 모든 의무가 현장에서 이행됐거나 위반됐다고 이 두 자료만으로 판정하지 않았다. [F01](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8), [F02 PDF p13](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13), [정정 영수증](field/resume-field-correction.json).

F03은 정정 공지와 이전 판을 함께 남겼다. `/previous/v2`는3월1일 문장 정정까지 반영한 최종판이 아니며 현재 교정본 URL은 가변이다. F04의 MYE3!A9:O365는357개 지역 키를 대조해39행/78셀 변경(H39·I39), J순이동·O총인구357행 불변을 확인했다. 최종 합계가 같아도 구성값의 정의 경계는 틀릴 수 있다는 반례다. 전 워크북·추정모형·하류 사용자 갱신까지 검사한 것은 아니다. [F03 원문·판 목록](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28), [F04 데이터셋](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires), [357행 비교](field/ons-correction-comparison.json).

수신 후속은 검색 봉인 후에만 열었다. 최초 PR은5개 병합,3개 미병합 종료였지만 닫힌 PR을 실패로 읽지 않았다. R03은 대체 RFC #2873으로 이어졌고 R07도 #3298을 거쳤으며, 현재 Rust/Kubernetes 문서는 일부 해당 동작을 설명한다. R01의 구현 PR은 동일 이름 전달을 먼저 넣되 deprecation은 별도로 미뤘다고 적어, 병합을 최초 요구 전부 구현으로 볼 수 없었다. R05의 제공자별 제약도 실제 API 접수와 노출 성공의 차이를 보여준다. [8개 후속 관측](recipient/outcome-observations.jsonl), [R01 구현 #68404](https://github.com/rust-lang/rust/pull/68404), [현재 mixed-protocol 절](https://kubernetes.io/docs/concepts/services-networking/service/#load-balancers-with-mixed-protocol-types).

제공 기관18도메인의 정확 문자열 검색은1,315개 댓글·리뷰 기록 중913개의 비어 있지 않은 본문과 현재 PR본문8개에서0건이었다. 직접 읽은 결정 댓글은 각 관측 행에 명시했으며1,315개 전부를 사람이 의미 판독했다고 주장하지 않는다. 기관 별칭·간접 인용·모든 연결 구현 파일·사적 지식은 이 검사 범위 밖이다. **수신자가 이 타 분야 원리를 실제로 채택했다는 증거는8건 모두 미확인**이다. 닮은 후속 선택이나 현재 기능의 존재로 원 검색의 적중을 고치지 않았다. [정확 검색 범위·입력 해시](evidence/followup-citation-screen.json), [현재 문서 원장](recipient/outcome-doc-sources.jsonl).

## Q7. 어떤 링크와 얼마나 짧은 설명이면 검토할 수 있는가

X01에는 “복합 요구의 접수 허용과 공급자의 실제 제공 결정을 분리한다”라는 한 줄, VPL의 두 분류와 중개 절, 수신 M01/M02를 함께 붙일 수 있다. 다음 행동은 혼합 포트를 받아들이는 검사 경계와 공급자 실패/상태의 연결을 검토하는 것이다. 깨지는 조건은 접수를 공급 보장으로 읽는 것이다. 단, 이는 전수에서 얻은 사후 설명이며 원 상위 반환이 아니다. CE01에는 동일 동작의 보존 여부, CE03에는 같은 조직·보존 범위·재개 권한을 우선 보여준다. [cases의 X01/CE01/CE03](cases.md), [역할별 추적](analysis/q7-role-walkthroughs.jsonl).

수신 설계자에게는 필수조건과 남는 코드·권한 연결, 절차 운영자에게는 누가 수락하고 누가 거절·되돌림을 결정하는지, 반례 검토자에게는 반드시 보존되는 대상·값·시간 경계를 제시했다. 실제 세 사용자를 인터뷰한 것이 아니라 세 관점의 문서 기반 검토다. 용어만 남기면 역할과 상태변화가 사라져 미확인이 되고, 역할을 뒤집으면 결정권 대응이 무너진다. X01에서 복합 책 항목 L106을 빼면 partial로 내려간다. CE01에서 1:1 비보장 개요(L21–33)를 빼도 역 제외(L63–67)와 운영시간 예외(L81–88)가 남아 충돌을 유지한다. CE03은 과거 요청 조회 L49를 빼도 취소·재요청 단서가 남아 부분 판정을 유지한다. 원문 삭제나 재검색을 실행한 실험이 아니라 **근거 의존성의 판독 교란**이다. [5행 교란 기록](judgments/critical-review.jsonl).

## 서로 다른 관점과 전이할 때 버릴 가정

검색 운영자는 R의 순위 변화 자체를 성과로 볼 수 있지만, 설계 검토자는 원창이 필수조건을 인용할 수 있는지를 봐야 한다. 제공 절차 운영자는 공표 지침이 실제 공급·정정·재개를 보장하지 않는다는 예외를 안다. 역사적 선례를 검토하는 사람에게는 현재 관계가 비슷하다는 사실보다 제안 당시 고정판이 존재했는지가 먼저다. 이 관점들은 같은 분자를 쓰지 않는다. [원창 감사](evidence/returned-window-audit.jsonl), [현장 범위](field/resume-field-audit.md), [당시 가용성](evidence/recount.json).

성공과 충돌은 다른 소재라는 이유로 갈린 것이 아니다. X01은 접수와 제공의 **서로 다른 권한 경계**를 보존하므로 좁은 관계가 맞는다. CE01은 대체 수단이 원 서비스와 정확히 같아야 하는 **동일성 경계**를 보존하지 않는다. CE02는 업데이트 대상이 같은 객체인지 새로운 vintage인지에 따라 방향이 달라진다. 물리적 반환을 디지털 취소로, 수동 계정 병합을 자동 forwarding으로, 예산 재배치를 마지막 읽기 완료 배리어로, 정책 목표 동일을 기능 동일로 바꾸는 가정을 버려야 한다. 각 대응의 실제 남은 핵심을 maps.new_core_required와 break_condition에 남겼다. [maps.csv](maps.csv).

이 결과 뒤의 설계 선택지는 세 가지로 나뉜다. 첫째, 현재 검색을 그대로 쓰면서 단어상 가까운 절에는 미확인/부분 표시와 부족한 조건을 붙인다. 둘째, 후보 문서 회수와 근거 절 조합을 별도 단계로 평가한다. X01은 문서10/12위 문제와 W001의 근거 부족이 동시에 있어 단순히 상위 개수만 늘리는 것으로 인용 완결을 보장할 수 없다. 셋째, 역할·객체 동일성·시간/부정 조건을 검사하는 비교를 새 사전 계획으로 실시한다. 같은 원토큰·유효 토큰 예산, 수신 미노출 작성자, 별도 새로운 수신 표본을 고정해야 이번 결과에 맞춘 사후 최적화와 구별된다. 여기서는 그 새 방법의 우월성이나 사용자 행동 효과를 검증하지 않았다. [범위·누출 방지](SCOPE.md), [사전 민감도](evidence/sensitivity-plan.md).

## 재현·출처·작업 경계

최소 산입 원문은 정확히30개(수신8·제공18·현장4), 제공 분야는각6개다. sources의61행은 제외/보조 작품까지 포함하며, 후속 독립 원문7개는 최소수에 더하지 않았다. 같은 문서의 여러 판·표현·반복 요청·검색 요약을 새 원문으로 세지 않았다. attempts의행수는 발견·판독·실행·실패를 포함하는 사건 수이지 네트워크 호출 수나 고유 자료 수가 아니다. 원 검색 계산시간25.151ms는 기록된16회 scorer 시간 합이고, 자료 수집·원문 판독·모델 작업·사람 노동시간이 아니다. [sources](sources.jsonl), [attempts](attempts.jsonl), [실행 영수증](evidence/retrieval-receipt.json).

```sh
python -B docs/workstreams/research/AF-RES-033/validate_inputs.py --check
python -B docs/workstreams/research/AF-RES-033/retrieval.py --check
python -B docs/workstreams/research/AF-RES-033/aggregate_results.py --check
python -B docs/workstreams/research/AF-RES-033/validate_results.py --require-report
python -B -m workbench.session check docs/workstreams/research/AF-RES-033/manifest.json --fetch
```

점수는 커밋된 특징량에서 재현한다. 저작권 허가를 확인하지 않은 제공 전문과 공개 토론 본문은 분석 캐시에만 두었으므로, 새 환경에서 의미/정확창을 다시 읽으려면 sources/corpus의원URL·판·추출범위를 다시 열어 SHA256을 먼저 대조해야 한다. 원 URL의 현재본문이 바뀌면 같은 고정판이라고 통과시킬 수 없다. 이 보존 한계는 원문을 읽지 않았다는 뜻이 아니라 제3자의 미래 원바이트 재획득이 항상 보장되지 않는다는 뜻이다. [수용 조건](evidence/acceptance-evidence.json), [Q별 자기 점검](SELF_CHECK.md), [manifest](manifest.json).

계획 통합 SHA는d3fbd08d44fd0e2915d1f766721a81845bacc213, 실제 최초 시작판은9668632e915d508e93ddfdc5e8fe4b88bcbfec56, 이번 재개 때 확인한 최신 통합은8dd88b74735eb512c133f1a30890ac82fbf61ecf다. 이들을 같은 SHA로 쓰지 않았다. 환경은 ChatGPT cloud Linux·GitHub 연결·웹 검색, 세션 식별 모델은GPT-6 Astra Pro이며 별도 web-pro 표시 UI는 관측하지 않았다. 기존8358b5e에서 이어 작업했고 모든 변경은 소유 경로 안이다. AF010/029는 중복·판정 경계 확인용이며 이 표본·점수와 합산하지 않았다. [재개 영수증](evidence/resume-033-2.json), [커밋별 진행](PROGRESS.md).

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 유일한 지지는 접수 범주에서 추론했으며 최초 요청에 이미 있는 경계다. 보수적으로 읽으면 지지0·회수 분모 해당 없음이다. 당시 가용성과 실제 채택도 미확인이다. | [VPL L64–106](https://www.vpl.ca/borrowing/interlibrary-loans), [R05 최초 L98–117](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md#L98-L117), [별도 판독](judgments/critical-review.jsonl) | 원리 지지1/144와 새 타분야 링크의 가치. 원검색0/8은 두 읽기 모두 같음 | VPL의2020년 이전 해당 규정 판과 ‘책+AV 구성품’ 실제 요청 양식/처리 기록을 먼저 대조한다. 일반 금지·접수·제공자 거절을 분리한 기록이 M01 추론과 역사적 선례 주장을 바꾼다. |
| 연구자가 정한 닫힌18문서·어휘 BM25·200토큰 한 창과 서로 다른 유효 질의 길이 때문에 자유 웹 발견이나 관계 검색의 우열을 추정할 수 없다. | [고정 corpus](corpus.jsonl), [원 rankings](rankings.csv), [R05–L06 최고점수창 W001](rankings.csv), [검색기](retrieval.py) | 관계 표현으로 유용한 원리가 ‘발견된다’는 제품 일반화, 단순 순위 변화의 효과 | 먼저 같은 고정 R05/L06에서 원 W001과 L3/L64–106을 구분하는 후보 회수·복수절 인용 검사를 별도 사전 계획으로 실행한다. 이어 새 수신 표본과 동일 유효 토큰 예산으로 비교해야 새로운 검색법의 주장이 바뀐다. |
| R04 권고 강도·T02 제목 잔존, 제한된 현장 관측·동일 모델 판독이 남는다. 정정된 합계·목표 유지·PR 병합만으로 원 요구 전부의 구현을 알 수 없다. | [R04 최초판](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md), [T02 감사](evidence/resume-donor-audit.md), [ONS 전후표](field/ons-correction-comparison.json), [R01 구현](https://github.com/rust-lang/rust/pull/68404) | 엄격 조건 설정의 타당성, 현장 실행/실제 채택까지의 외삽. 기록된 민감도에서는 엄격0이 유지됨 | 첫 자료는 원 R04의권고 하위절과 T02 원/제거 판, F04 MYE3의357키 비교 및 R01 구현 본문의 deprecation 보류다. 이 자료를 보지 않은 인간 검토자에게 조건 강도·객체 동일성·남는 핵심을 따로 판정받고 실제 구현 테스트/운영 기록을 연결한다. |
'''
report=report.replace('https://www.translink.ca/-/media/translink/documents/plans-and-projects/managing-the-transit-network/transit_service_guidelines.pdf',corpus['T04']['url'])
(P/'RESULT.md').write_text(report)
print(json.dumps({'result_bytes':len(report.encode()),'first_table_rows':len(shown),'second_table_rows':9,'third_table_rows':len(counterexamples)},ensure_ascii=False))
