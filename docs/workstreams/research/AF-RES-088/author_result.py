"""Render the required tables from frozen data plus explicitly authored interpretation."""
import csv
import json
from pathlib import Path
P=Path(__file__).resolve().parent

def jl(name):return [json.loads(x) for x in (P/name).read_text().splitlines()]
def csvrows(name):
    with (P/name).open() as f:return list(csv.DictReader(f))
def esc(x):return str(x).replace('|','\\|').replace('\n',' ')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(esc(x) for x in r)+' |' for r in rows])+'\n'
def link(label,url):return f'[{label}]({url})'
def ratio(r):return f'{r["numerator"]}/{r["denominator"]}'+(' · 산출 불가' if not r['denominator'] else '')

EDITOR={
'JN1':'작성자 user1457613이 rev2 전체 JSON 추가; rev3 user7939871 재서식(삭제 계정, stable ID 미확인)',
'JN2':'Starbucks Admin; 후속 yaml 태그만 추가, 본문 별도수정 없음',
'JE1':'Sandeep Singh → 독자 Arun; 제목형 강조·코드 fence/들여쓰기 정리',
'JE2':'sanjanakaranam → 독자/답변자 oguz ismail; 문구·인라인 코드·jquery 태그 정리',
'PN1':'Robert Dodier; 후속 태그만 수정, 본문 별도수정 없음',
'PN2':'Alexey Bogdanov; 전체 이력1행, 별도수정 없음',
'PE1':'Spark가 이미지 URL2회 변경; 독자/답변자 tarleb가 링크→img 표시',
'PE2':'Joe → 독자 Shafee; 깨진 code fence 복구, 뒤 별도 행에 pandoc 태그 추가'}

R1_REASON={
'JN1':'DailyForecasts 항목5개를 포함한 전체 JSON이 추가돼도 값 배열이라는 조건은 유지된다.',
'JN2':'동일 YAML 본문이며 필터 전에 필요한 JSON 파싱 전제가 여전히 성립하지 않는다.',
'JE1':'서식은 달라졌지만 실제 Document API 연결은 여전히 제시되지 않는다.',
'JE2':'인라인 코드/문구만 정리됐고 배열 대신 JSONL이라는 출력 조건은 같다.',
'PN1':'동일 표 본문이며 중간선의 굵기·색과 사용판 보고가 유지된다.',
'PN2':'동일 HTML 수식이며 reader가 보존하는 구조와 Math handler는 추가되지 않았다.',
'PE1':'텍스트의 줄번호·여백·PDF 조건은 같다. 옛 이미지 의미는 미확인이다.',
'PE2':'code fence만 고쳐졌고 출력 접기 목적·writer/AST 결손은 같다.'}

STORAGE={
'JN1':[
 '현재 입력만 보면 map과 full JSON을 처음부터 연결할 위험; JSON/Bash 배열 구별을 되묻는다.',
 'R0의 부분 입력과 R1의 full JSON 추가 시점을 복원한다. map 링크는 같고 전체 입력 재요청 필요만 달라진다.',
 'jq1.7.1 map+C1/C2로 JSON 배열화만 정합. R1에서는 Bash 소비 명령·실제 설치판/출력을 되묻는다.'],
'JN2':[
 '같은 질문 주소와 채택 yq만으로 당시 jq 후보의 실패 전제를 놓칠 수 있다.',
 '본문 R0=R1과 태그-only 수정을 분리하고 YAML 입력 조건을 복원한다.',
 'jq1.7.1 입력 parser 절+네 후보를 연결해 명시 반박; JSON 변환이나 YAML 도구 허용 여부를 묻는다.'],
'JE1':[
 '후속 JSON 데모의 map을 완성된 Document 설정으로 오인할 위험이 있다.',
 '서식 전후 요구가 같음을 복원하지만 매뉴얼판/JSONLoader 계약은 아직 빠져 있다.',
 '고정 네 후보는 Document 속성 주입 범위 밖; JSONLoader판·metadata callback·실제 객체 출력을 요청한다.'],
'JE2':[
 '현재 간결한 질문/답을 처음의 문구와 혼합할 수 있다. 반환할 실제 해법은 Documents[]와 compact output이다.',
 'rev2가 답변자 편집이고 내부 _rid 보존이 R0에도 있었음을 확인한다.',
 '고정 후보의 배열 출력과 요구 JSONL을 구별; 풀 밖 순회/직렬화 링크와 실제 각 줄의 검증을 남긴다.'],
'PN1':[
 '현재 채택 grid-table 답을 질문자의2.9.2.1 즉시 실행 성공으로 오인할 위험이 있다.',
 '본문은 동일하며 원 사용판 보고와3이상 필요 답의 시점을 나눈다.',
 '3.1.11 Lua는 handler/엔진/선 굵기·색 확인 전 조건부; 채택된 grid_tables는 별도 풀 밖 경로로 보관한다.'],
'PN2':[
 '현재 댓글의 대량 수식·수동변환 금지를 원래 본문의 C2로 소급할 위험이 있다.',
 '본문 R0=R1을 복원하되 사후 댓글의 새 제약은 별도 UTC로 붙인다.',
 '3.1.11 Lua는 reader AST·Math handler 확인 전 조건부; 대량 입력과 수식 wrapper 보존을 추가 질문한다.'],
'PE1':[
 '현재 이미지와 채택 raw LaTeX만 남으면 옛 이미지의 정보와 해법 등장 시점을 복원하기 어렵다.',
 '이미지 URL 교체·답변자 embed 시점을 복원하지만 R0 asset 결손은 남는다.',
 '고정 metadata/template/Lua 세 경로는 코드·엔진·PDF 확인 전 조건부. R0 이미지와 여백 측정을 우선 요청한다.'],
'PE2':[
 '2026년 답과 구체화된 현재 첫 답을 2024년30일창에 있던 안내로 오인할 위험이 있다.',
 '질문 rev1/2는 서식차이며30일 내 답0·댓글1과91일 뒤 첫 답을 분리한다.',
 '3.1.11 Lua 조건부에 writer/Quarto판/실행후 AST를 붙인다. code-fold는 R0 단서이며 새 정답 증거가 아니다.']}

def main():
    rr=jl('revisions.jsonl');jj=csvrows('judgments.csv');pp=csvrows('pairs.csv');oo={x['case_id']:x for x in jl('outcomes.jsonl')};m=json.loads((P/'metrics.json').read_text())
    out=['## 표 1 · 공개 본문판과 조건의 전후 근거\n']
    rows=[]
    for r in rr:
        cid=r['case_id'];a,b=r['r0'],r['r1'];same=a['guid']==b['guid']
        revcell=link('이력',r['history_url'])+'; '+link('R0',a['revision_url'])+f' `{a["guid"]}` · {a["revision_utc"]}; '
        revcell+=('R1=R0(전체 이력 확인)' if same else link('R1',b['revision_url'])+f' `{b["guid"]}` · {b["revision_utc"]}')
        c2=a['c2'] or ('없음: '+a['c2_absence_reason'])
        evidence=f'C1 {a["c1"]}; C2 {c2}. R0 {a["evidence_location"]} → R1 {b["evidence_location"]}. '+r['semantic_comparison']['note']
        rows.append([f'{cid} · {"자연" if r["stratum"]=="natural" else "편집"} · {a["tool"]} #{r["original_rank"]} / {r["question_id"]}',revcell,EDITOR[cid],evidence,'가장 이른 보존 공개 본문판 확인. 생성시각 일치, 즉시 게시 바이트는 미확인'+('; 옛 이미지 의미 미확인' if cid=='PE1' else '')])
    out.append(table(['사례·층·원순번','이력 URL·R0/R1 GUID·UTC','작성자·편집 종류','C1·C2의 전후 근거','최초 게시 증거·미확인'],rows))
    out.append('## 표 2 · 같은 후보와 고정 매뉴얼의 32쌍 전부\n')
    rows=[]
    for p in pp:
        cid=p['case_id'];a=next(x for x in jj if x['case_id']==cid and x['candidate_id']==p['candidate_id'] and x['revision']=='R0');b=next(x for x in jj if x['case_id']==cid and x['candidate_id']==p['candidate_id'] and x['revision']=='R1')
        delta='명시 텍스트 조건·해법 단서 불변'
        if cid=='JN1':delta='전체 입력 추가; map은 R0부터 단서'
        if p['condition_or_next_question_changed']=='true':delta+='; 전체 JSON 재요청 → Bash 소비/사용판 질문'
        if cid=='PE1':delta='텍스트 조건 불변; 교체 이미지의 추가 조건·해법 단서는 미확인'
        r1reason=R1_REASON[cid]+(' 두 경로의 값 존재가 전체 입력에서 확인됐으나 jq 실행은 아니다.' if cid=='JN1' and a['candidate_id']=='JQ-map' else '')
        rows.append([f'{cid} / {a["candidate_function"]}',link(a['reference_tag']+' · 절',a['manual_url'])+f' (`{a["reference_sha"]}`; {a["manual_source_ids"]})'+('; default.latex 대응은 MAN-10으로 후속 정정 — [정정원장](evidence_corrections.jsonl)' if cid=='PE1' else ''),f'{a["assessment"]} / {a["return_status"]} — '+a['reason'],f'{b["assessment"]} / {b["return_status"]} — '+r1reason,delta,'실패 경계: '+a['failure_rule']+'; 다음 확인: '+p['missing']])
    out.append(table(['사례·후보 기능','같은 매뉴얼판·근거 절 URL','R0 판정·이유','R1 판정·이유','달라진 단일 조건·해결책 단서','반례·미확인'],rows))
    out.append('## 표 3 · 같은 사례의 세 보관 방식과 실제 응답\n')
    rows=[]
    for r in rr:
        cid=r['case_id'];o=oo[cid];a=r['r0'];b=r['r1']
        answers='; '.join(link('답'+str(x['answer_id'])+' 최초판',x['first_body_url']) for x in o['answers'])
        own=[x for x in o['timeline'] if x['kind']=='public_comment' and x['by_questioner']]
        comments='; '.join(link('질문자 댓글'+str(x['comment_id']),x['url']) for x in own)
        ev=answers+('; '+comments if comments else '')+f'; 현재 채택={o["current_accepted_answer_id"] or "없음"}; '+(link('보고판2.9.2.1',a['revision_url']) if cid=='PN1' else '정확 사용판 미확인')
        methods=[link('현재 질문 주소만',o['observed_current_question_url']),link('R0',a['revision_url'])+' + '+link('R1',b['revision_url'])+' + UTC',link('리비전·조건',a['revision_url'])+' + '+link('고정 후보판','candidates.csv')+' + 인용 위치/지문']
        perspectives=[f'{cid} · 질문자: 원요구 / 편집자: 수정경위 / 검색기: 현재 근거',f'{cid} · 질문자: 당시 입력 / 편집자: 판별 차이 / 검색기: 시점 제한',f'{cid} · 질문자: 조건 충족 / 편집자: 변경 축 / 검색기: 후보판·전제']
        for n in range(3):
            rows.append([perspectives[n],methods[n],STORAGE[cid][n],ev,o['response_interpretation']['agreement'],o['response_interpretation']['next']])
    out.append(table(['사례·관점','보관 방식','반환 링크·조건 또는 되물을 값','실제 응답·채택·사용판 증거 URL','일치·불일치','추가 확인'],rows))
    out.append('## 분모 · 계획과 관측을 분리한 집계\n')
    rows=[['모집 원목록','jq30 + pandoc30','조회시점 태그·생성시각/ID순; 첫30 cap. 양태그 page1 has_more=true, page2 경계 보존'],['적격/선정/미선정','60/60; 선택8; 적격 미선정52; 결원0','jq 자연2+편집2; pandoc 자연2+편집2'],['자연2개 제외 뒤 편집층 후보','jq13/28; pandoc12/28','각 순서 첫2만 선택; 편집 존재를 모집용 메타데이터로만 선열람'],['판정/쌍','64/64행; 공개 본문쌍32/32','문서 정오 비교 가능26/32; 미확인6/32'],['판정 변화','0/26','자연0/14; 편집0/12. 26쌍 중 긍정1·음성25; 독립 질문26개가 아님'],['반환할 추가 질문 변화','1/32','JN1/map; 확정군만의 분모로는1/26; 명시 텍스트 조건 범위'],['직접 원자료','120개; 독립 저작·사건87개','출처기록184행. 같은 질문의 답/댓글은 독립 사건으로 늘리지 않음'],['필수 원자료 하위구성','선정 질문사건8/8; CLI12자료·9저작; 플랫폼17자료·8사건','IETF2/2·학술2/2 판쌍 및 각각 후속 인용. 타분야13자료·9저작'],['사후 응답','질문8; 답11/최초본문11; 답리비전13; 댓글17','답변자의 구체 출력 텍스트3/11 + 서술상 결과보고1/11 = 합집합4/11; 외부 데모/이미지 실행검증0'],['질문자 후속','6댓글/4사례; 후속 시도·실패 보고2/8; 완전 성공 보고0/8','시도는 JN1·PN2. 현재 채택3/8이며 주된 채택해법 풀 밖3/3'],['엄격 원판·실사용','최초게시 바이트0/8; 정확 사용판 보고1/8; 성공+정확판 검증0/8','엄격 최초게시 기준 후보 변화0/0=산출 불가; 도움/시간 절감 인과효과0/0=산출 불가']]
    rows[6]=['직접 원자료',f'{m["sources"]["primary_units"]}개; 독립 저작·사건{m["sources"]["independent_events"]}개',f'출처기록{m["sources"]["records"]}행. 같은 질문의 답/댓글은 독립 사건으로 늘리지 않음']
    out.append(table(['지표','분자/분모 또는 수','해석 경계'],rows))
    rows=[]
    for layer,label in [('natural','자연층'),('edited','편집층')]:
        z=m['strata'][layer]
        rows.append([label,'4/4',ratio(z['body_bytes_changed']),ratio(z['text_requirement_changed']),ratio(z['text_input_information_changed']),f'{z["documentary_comparable_pairs"]}/16',f'{z["r0_assessments"].get("명시 반박",0)}/16 → {z["r1_assessments"].get("명시 반박",0)}/16',ratio(z['body_edit_after_first_answer_cases']),ratio(z['author_edit_after_first_answer_cases']),ratio(z['strict_initial_bytes']),ratio(z['questioner_success_exact_runtime_verified'])])
    out.append(table(['층','선정/계획','본문 바이트 변화','명시 C1/C2 변화','텍스트 입력 보완','비교 가능 쌍','명시 반박 R0→R1','답 이후 본문편집 사례','작성자의 답 이후 편집','엄격 최초게시','성공 실사용판'],rows))
    out.append('자연층에서만 기술적 관측빈도(본문 변경1/4, 명시 조건 변경0/4)를 쓴다. 편집층4/4는 선택 규칙의 결과다. 모든 조건·이미지가 불변이었다는 빈도는 계산하지 않는다(PE1 결손). 이 표의0은 관측/판정된0이며0/0 산출 불가를0%로 바꾸지 않는다. 표3은 보관 계약의 회고 비교이며 세 검색 시스템을 실행한 성능 실험이 아니다.\n')
    out.append(NARRATIVE)
    (P/'RESULT.md').write_text('\n'.join(out))
    print('RESULT tables:',len(rr),len(pp),len(rr)*3,'rows; PARTIAL')


NARRATIVE=r'''## 판정 · PARTIAL

**같은 고정 매뉴얼 후보의 명시 텍스트 조건 판정은 확정 비교26쌍에서 바뀌지 않았다. 그러나 JN1/map은 반환 링크가 같아도 다시 요청할 입력이 달라졌고, PE1의 전체 시각 정보와 여섯 Pandoc 구현 경로는 아직 확정할 수 없다.** 따라서 “현재 질문으로 원래 검색 품질을 안전하게 채점할 수 있다”는 결론은 지지하지 않는다. 여덟 자리와32쌍을 모두 표에 남겼으며 미확인6쌍을 정답·오답 변화율에 넣지 않았다. 자료 최소량과 형식적 판독은 채웠지만 필수 의미 근거의 결손 때문에 REVIEW_READY로 올리지 않는다. [집계](metrics.json), [판정64행](judgments.csv), [쌍32행](pairs.csv).

이 연구는 실제 검색엔진의 순위·재현율 또는 사람의 탐색시간을 측정하지 않았다. 정오라는 말은 사전에 제한한 후보 하나와 명시 조건의 문서상 적합성이다. `범위 밖`은 그 기능 전체가 쓸모없다는 뜻이 아니라 이 단일 후보 계약의 핵심 동작만으로 요구를 충족하지 않는다는 뜻이다. `미확인/조건부`는 실행 성공이 확인된 조건부 정답이 아니다.

### Q1 · 무엇을 첫판이라고 부를 수 있는가

`site/post_id + revision GUID + 순번 + UTC + 편집 주체 + 표현 형식 + 본문 지문`으로 보존된 첫 공개 본문판을 식별했다. 원60질문의 이력129행을 페이지 끝까지 보았고, 본문111행 가운데 뒤 본문51행의 `last_body`가 앞 본문과 모두 일치했다. 선택8의 첫 본문순번은 모두1이고 생성시각과 같다. 그러나 [API revision 정의](https://api.stackexchange.com/docs/types/revision)와 [2022년 편집 정책판](https://meta.stackexchange.com/revisions/21789/26)은 여러 편집의 한 리비전 병합을 설명한다. 생성시각 일치를 게시 직후 바이트의 별도 보존 증거로 올릴 수 없다. [PL01, PL09, PL20; support/revision_integrity_audit.md]

실제 반례도 구별했다. [Meta302285 판2](https://meta.stackexchange.com/revisions/302285/2)는 제목만 바뀌어 본문 수정이 아니다. [Meta17038 이력](https://meta.stackexchange.com/posts/17038/revisions)의 판3은 작성자의 롤백이며, 판1과 본문이 같아도 새 GUID·시각을 갖는다. 이 사건의 CommonMark 변경/롤백 판34–37은 HTML 지문 두 개와 같은 요구를 보인다. 반대로 코드 공백이나 제목 한정이 의미를 바꾸는 경우도 있으므로 공백 제거 해시를 일반 의미 판정기로 쓰지 않았다. [PL11–16; support/platform.md]

표현은 historical `revision.body` HTML끼리 비교했다. 현재 질문의 Markdown으로 과거 HTML을 대신하지 않았다. 사후 PN1 답78260959에서는 보존된 본문판이 하나인데 현재 HTML의 pre class만 달랐다. 이를 별도 내용 편집으로 세지 않았고 렌더링 차이의 생성 원인도 미확인으로 남겼다. [OUT-A-78260959-FIRST; support/outcome_integrity_audit.md]

### Q2 · 모집에서 빠진 것과 표본의 범위

모집 창은 UTC `[2024-04-01, 2024-07-01)`이며 jq→pandoc 순서로 중복 태그를 jq에 한 번 배정한다. 실제60개 ID는 중복이 없었다. 원목록의 각30개와 page1 끝, 동시각 경계 확인용 page2를 보존했다. jq의30번째는78403902/4월29일이며 page2도 더 있는 상태다. Pandoc30번째는78652004/6월21일이고 page2에는4개가 더 있다. “해당 기간 전체 목록”이라 하지 않고 첫30 cap으로 한정한다. [frame.csv; raw/frame_*; ROOT-FRAME-*]

적격은 공개 입력/목적/원하는 출력이 있는 실제 사용 질문으로 넓게 판정했다. jq25의 입력/오류 문제, jq27의 Jenkins 연결, Pandoc23의 파일명 오류 반환은 경계 사례로 이유를 남겼다. 이들을 더 좁게 제외해도 이번 첫2 자연·첫2 편집 선정 ID는 바뀌지 않는다. 원60은 적격60, 그중선정8·미선정52이며 결원은 없다. 답·점수·채택은 모집 필터와 선정 판단에 쓰지 않았다. 제목은 현재본이 기계 응답에 포함됐지만 최초 의미 판독에는 R0 제목/본문만 사용했고 이미 R0에 나온 map/code-fold 등의 단서는 노출 칸에 남겼다. [SCOPE.md; frame.csv; R0_SEAL.md]

태그는 조회 시점 분류다. PE2의 첫 태그는 quarto이며 pandoc는 후속 태그 편집에서 추가됐다. 삭제된 질문, 조회 전에 태그가 빠진 질문,30개 뒤 질문, 보존 이력이 사라진 질문의 원래 분모는 이 조회만으로 알 수 없다. 접근 가능한 첫 공개판을 가진 자료에 유리한 표본이라는 범위를 유지한다. 자연층4개도 임의 추출이 아니라 시간순 첫 질문이어서 전체 Stack Overflow의 수정 발생률을 대표하지 않는다. [API questions](https://api.stackexchange.com/docs/questions), [PE2 이력](https://stackoverflow.com/posts/78461996/revisions).

### Q3 · 바이트·조건·해법 단서를 따로 판독했다

명시 C1/C2는8개 모두 텍스트상 유지됐다. JN1에서는 값 배열화/올바른 값 보존이라는 조건이 유지된 채 전체 JSON이 추가됐다. JE1·JE2·PE2는 서식·문구·태그 정리다. PE1은 이미지가 교체되고 표시 방식이 바뀌었지만 옛 A0Wtm.png 접근은 실패했다. 따라서 기계 기록도 `text_requirement_change=false`, `full_input_information_change=unknown`, `visual_equivalence=unknown`으로 분리했다. “요구 불변”이라는 과도한 일반 필드를 두었다가 같은 팀 방법 리뷰에서 위험을 발견해4번째 묶음에서 범위를 명시했다. R0/R1의64개 판정은 바꾸지 않았다. [revisions.jsonl; refine_semantics.py; support/method_review.md; attempts.jsonl]

C2가 없는 JN2·PN2·PE2에는 독립 조건을 만들지 않았다. PN2의 “대량이라 수동 변환 불가”는 답 뒤 댓글에 추가된 제약이며 R0/R1 C2에 소급하지 않았다. PE2의 code-fold와 JN1의 map은 최초판부터 있던 실패 시도의 단서다. 이 단서가 있다는 사실만으로 후보가 목적을 충족한다고 처리하지 않았다. [requirements_r0.jsonl; OUT-C-137986143]

### Q4 · 고정 문서의 기능과 실제 환경을 분리했다

첫 묶음에서 jq-1.7.1=`71c2ab509a8628dbbad4bc7b3f98a64aa90d3297`, Pandoc3.1.11=`c3038dcd54152c4e18e49db31676b79ee7cc29b2`를 고정했다. `select/map/sort_by/group_by`와 `--metadata/--template/--lua-filter/--standalone`의8절, 입출력과 실패 경계는 [candidates.csv](candidates.csv)에 있다. jq의 기본 필드 접근·리터럴·조건식은 허용하되 다른 후보나 핵심 named 함수의 추가를 단일 후보 성공으로 세지 않았다. Pandoc template 자체 문법/암묵 standalone은 허용하고 Lua handler 코드는 필요 요소로 인정했지만 옵션 이름만으로 임의 변환 성공을 추론하지 않았다. [첫 계약 커밋](https://github.com/laadkke-arch/agentflow-open/commit/9f8a8f5c0d4ac9f8659374d99e71f3d7a1013712)

공식 시험/예제와 변경 사건에서 반례를 찾았다. map은 f가 여러 결과를 내면 길이가 바뀌고, group_by는 하위 배열들을 낸다. sort_by/group_by 상류 시험을 읽었지만 실행했다고 세지 않았다. Pandoc template은 docx/pptx에 적용되는 보편적 스타일 엔진이 아니며, Lua handler 반환형과 reader의 정보 보존에 제약이 있다. jq 큰 정수 수정 #2949, Pandoc3.1.11의 PDF 재실행 회귀 수정은 같은 기능 링크라도 수치/엔진/판 전제가 따로 필요함을 보인다. [MAN-01–12; support/manuals.md]

확정26쌍 중25쌍은 범위 밖/반박이다. 좁은 풀의 음성 판정이 많은 구조에서0변화가 나왔으므로 양질의 실제 답 전체가 수정에 안정적이라고 말할 수 없다. 후보 경계를 넓혀 map+select나 to_entries를 허용하면 답의 분류가 달라질 수 있지만 사후에 계약을 바꾸지 않았다. PN1의2.9.2.1은 질문자 자기보고이고,3.1.11은 연구 참조판이다. 로컬 jq1.7/Pandoc3.1.11.1도 둘과 별개다. 정확판 gate가2로 끝났으므로 고정 참조판 변환을 실행하지 않았고 필요한 명령·입력37개 스니펫을 [execution/README.md](execution/README.md)에 남겼다.

### Q5 · 같은 링크와 같은 반환 내용은 다른 변수다

JN1/map은 두 공개판에서 모두 배열 수집을 설명하는 같은 고정 절이다. R0에서는 전체 JSON을 더 받아야 하고 R1에서는 그 입력이 있으므로 Bash에서 JSON 배열을 어떻게 소비하는지, 실제 jq판과 출력이 무엇인지가 남는다. 링크/문서 판정 변화0과 다음 질문 변화1은 동시에 성립한다. 본문 해시 변화5/8을 정답 변화5/8로 세지 않았다. 여섯 미확인 후보의 라벨이 같다는 사실도6개 성공의 재현을 뜻하지 않는다. [pairs.csv; JN1 두 revision URL; OUT-C-137960636]

R032행을 원격42e46d5에서 다시 읽은 뒤 R1을 읽었다. R1은 역순으로 읽었지만 같은 작업자가 R0를 기억한다. 원 리비전 JSON은 기계 수집 단계에 이미 있었고 의미 노출만 분리했으므로 접근 통제에 의한 이중맹검이 아니다. 답·채택·댓글은 R1 커밋f048885 뒤에 열었다. jq 담당 보조자의 R0 제안과 root의 범위 밖/반박 경계 차이2건도 R0 봉인에 남겼다. 플랫폼 담당의 별도 감사는 메타데이터 검산이며 독립 의미 판독/일치도 점수로 세지 않는다. [commit_log.jsonl; R0_SEAL.md; R1_COMPARISON.md; support/*audit*]

### Q6 · 응답·채택·실행은 어디까지 연결되는가

선정8에 공개 답11, 최초 답 본문11, 현재 공개댓글17을 연결했다. 답 이후 질문 본문편집2건은 JE2와 PE1이며 모두 먼저 답한 타인의 편집이다. 작성자의 답 이후 본문 수정/해법 삽입은 선택8에서0이다. JN1의 전체 입력 추가는 댓글 뒤·첫 답 전에 있었다. PE2는30일 내 답0·질문댓글1, 첫 답은91일 뒤다. 현재 페이지에는2026년 답도 있어 이를2024년의 정보로 소급할 수 없다. [outcomes.jsonl; support/outcome_integrity_audit.md]

채택은 JN2의 yq, PN1의 grid_tables, PE1의 raw LaTeX로3건이며 주된 방법은 모두 고정 풀 밖이다. PN1 질문자는 원하던 효과라고 말하면서도 기존 방법을 계속 쓰고 다음 작업에서 grid table을 쓰겠다고 명시했다. JN1은 Bash 배열 문제, PN2는 수식 wrapper 소실을 후속 보고했다. JE1 답의 JSON 모양은 실제 Document 속성 주입을 확인하지 않는다. 재개 검토에서 초안의 출력불일치 주장을 철회했다. 보조 jq1.7 실행은 첫 프로그램 seq_num=[1,1], 둘째=[1,2]를 보여 주며 게시 출력은 첫 프로그램과 일치한다. 이 두 실행은 고정 jq1.7.1 또는 원 질문자의 JSONLoader 실행이 아니다. [재개 사후감사](support/resume/outcomes_audit/REPORT.md), [실행행](support/resume/outcomes_audit/JE1_answer_variant_run.json). 답변자의 시연·현재 채택 표지·원 질문자의 정확판 성공은 각각 다른 근거다. [OUT-A-*; OUT-C-137975317; OUT-C-137986449; 공식 채택 설명](https://stackoverflow.com/help/accepted-answer).

반례 탐색은 고정 표본을 교체하지 않고 별도로 보존했다. [SO60148441 rev6](https://stackoverflow.com/revisions/60148441/6)은2020-02-13T03:04:59Z 작성자 GutenYe가 while/reverse/join/tostring/-r 해법을 추가한 실제 사건이다. 직전 rev5의 전체 HTML은 rev6의 접두부다. 대응 [peak 답60178790 최초판](https://stackoverflow.com/revisions/60178790/1)은100013초 먼저 있으며 작성자가 감사로 귀속했다. 다만 정확 답 URL은2026년 타인이 추가한 것이므로2020년 직접 링크로 소급하지 않았다. 요구 유지+답 이후 해법 단서 추가가 실제 가능하다는 대조이지8사례의 변경률에 더할 사례가 아니다. [support/solution_insertion_control.md]

공개 무응답 대조도 확인했다. 고정60 중 현재 답0인6건의 댓글을 모두 조회했다. 첫 후보 jq16은 댓글8개가 있어 무응답이 아니었다. Pandoc23/78566705는 답0·댓글0·본문판1개다. 이를 당시 절대 무응답, 사용 포기, 효과 없음으로 바꾸지 않았다. 삭제된 답/댓글과 외부 해결은 미확인이다. 이 별도 목적 대조를8자리/32쌍 또는 자연층 발생률에 합치지 않는다. [support/no_response_control.md]

### Q7 · 현재 주소보다 더 보관해야 하는 것

표3의 비교는 실제 검색기 성능 실험이 아니라 같은 사례의 정보 보존 계약을 대조한 것이다. 질문자는 당시 입력과 실제 최종 목적을, 편집자는 어떤 조건/해법/표현을 바꿨는지를, 링크 검색기는 어떤 후보판의 어떤 동작으로 어떤 조건을 충족한다고 판단했는지를 복원할 수 있어야 한다. 최소 보관 단위는 **판 ID·UTC·표현·지문 + 조건의 짧은 인용/위치 + 후보 SHA·절 + 허용 코드/실패 경계 + 사후 응답의 별도 시점·주체**다. 원 요청·독자 편집·해법 단서·실행 주장을 같은 본문 텍스트에 합치지 않는다.

| 별도 대조 | 실제 판쌍·후속 인용 | 같은 답을 지지하는 조건 | 달라지거나 보류되는 조건 |
| --- | --- | --- | --- |
| IETF QUIC | [transport-27](https://www.ietf.org/archive/id/draft-ietf-quic-transport-27.html)→[28](https://www.ietf.org/archive/id/draft-ietf-quic-transport-28.html); [ATSSS00](https://datatracker.ietf.org/doc/html/draft-bonaventure-quic-atsss-overview-00)은28을 명시 | 클라이언트 Initial UDP payload 최소1200은 동일 | 1200초과는28에서 path+peer 지원 전제가 명시되고 parameter명도 바뀐다. 만료일은2020-08-24→11-21 |
| IETF TLS | [tls13-27](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-27)→[28](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-28); [rfc8447bis00](https://www.ietf.org/archive/id/draft-ietf-tls-rfc8447bis-00.html)은28/2018-03-20을 명시 | binder 실패 시 handshake 중단은 동일 | E.6이 Static RSA에서 PSK identity exposure로 바뀌고 RSA는E.7로 이동. 같은 절번호만 저장하면 오참조 |
| 학술 Transformer | [1706.03762v1](https://arxiv.org/pdf/1706.03762v1)→[v2](https://arxiv.org/pdf/1706.03762v2); [BERTv1](https://arxiv.org/html/1810.04805v1)은NIPS2017출판본을 인용 | attention 중심 구조라는 실제 후속 인용은 유지 | EN-FR 수치 문턱41.1 probe: v1 abstract41.0, v2 abstract41.2/§6.1 41.17/Table2 41.0. 같은v2 내부도 상충해 보류 |
| 학술 Kalb–Ramond | [2401.14452v1](https://arxiv.org/html/2401.14452v1)→[v2](https://arxiv.org/html/2401.14452v2); [fluidsv1](https://arxiv.org/html/2406.01412v1)은버전 없는ID인용 | 후속 논문의 실제 인용인 parity 위반 주장은 양판 지지 | v2가 amplitude 오류를 정정, 최저차수 phase효과만 서술. 정정됐어도 모든 후속 인용이 틀린 것은 아님 |

IETF2건과 학술2건은 모두 원판/다음판/후속 인용을 열었다. 특정 판을 인용했다는 사실은 구현·학습·관측의 실사용판 증거가 아니다. 학술 예의 숫자 문턱은 연구자가 만든 probe다. BERT가 어느 arXiv판을 읽었는지, physics erratum의 출판 DOI가 무엇인지는 확보하지 못했다. [support/cross_fields.md; CF-S01–17; ROOT-REOPEN-CF-*]

### 실행·검산과 이관 경계

원본 지문·페이지 끝·GUID·선정순서·답 시각/주체·R0 불변·후보계약 불변·64행/32쌍·출처 중복 제외는 [reproduce.md](reproduce.md) 절차로 재집계한다. `recalculate.py`는 의미를 자동 분류하지 않는다. 자동검사 PASS와 연구 상태 PARTIAL은 다른 축이다. 첫 검산 스크립트의 상대경로 검사 오류를 수정했고 실제 owned_path 밖 변경은 없었다. 원격 결과 SHA·manifest `check --fetch`의 실제 종료값은 결과 커밋 재열람 후 마지막 단독 [HANDOFF.md](HANDOFF.md)에 기록한다.

재개 시 PE1의 추가 근거 URL(default.latex)은 맞지만 일부 source ID가 HTML5인 MAN-06을 가리키는 오류를 발견했다. 대응은 MAN-10이고 생성경로는 MAN-11/12다. 원64행을 소급 고치지 않고 표2와 [정정원장](evidence_corrections.jsonl)에 후속 대응을 표시했다. 해법삽입대조의 원자료3행 설명도 댓글1 제외 후 최종2개로 정정했다.

초기 계획에는 변경 수의 목표값이 없었다. 실제 의미 변화가 작은 편집층이 뽑힌 결과를 받아들였으며, 대조에서 찾은 더 극적인 사례를 표본에 넣지 않았다. 후속자료를 보고 소급해서 R0 조건/후보판/점수를 고치지 않았다. 선행084의 개설본문0/4·엄격0/16과 최초 확보본10/16은 그대로 별도 과제의 분모로 유지했다. [intake.json; SELF_CHECK.md]

### 약점 1 · 옛 이미지와 즉시 게시 바이트를 복원하지 못했다

**다음 대상:** PE1 질문78300525의 R0 `A0Wtm.png`, 그리고 선택8의 생성 직후 동시대 보존본. **입력:** 출처 시점·원 URL·실제 이미지/HTML 바이트와 SHA256. **판단을 바꿀 관측:** 옛 이미지에 텍스트 밖의 추가 제약/해법 단서가 있으면 PE1 전체 의미 비교를 변경한다. 원 게시 캡처가 R0와 일치하면 엄격 최초게시 확인 분자를 올릴 수 있다. 현재8/8의 생성시각 일치만으로는 올리지 않는다.

### 약점 2 · 좁은 후보풀의 음성25쌍과 구현 미확인6쌍이 안정성 판단을 제한한다

**다음 대상:** PN1/Lua, PN2/Lua, PE1/metadata·template·Lua, PE2/Lua의 정확 참조판 구현 및 별도 의미 판독. **입력:** execution/의 고정 입력, 누락된 전체 Markdown/Quarto AST, handler/template/LaTeX 코드, jq1.7.1·Pandoc3.1.11/엔진 버전. **판단을 바꿀 관측:** C1/C2를 모두 만족하는 출력이면 사후 구현 확인을 추가하고, 명시 실패면 반박 근거를 추가한다. 입력이나 후보 범위를 확장한 실행은 별도 분석으로 남긴다. 같은 작업자의 역순 독해를 독립 판독으로 세지 않는다.

### 약점 3 · 채택만으로 원 사용자의 최종 목표 충족·실행판을 확인할 수 없다

**다음 대상:** JN1의 Bash 배열 소비와 PN1의 향후 grid-table 사용에 관한 원 질문자의 공개 후속 기록. **입력:** 동일 원 입력·완전 명령·정확 프로그램/엔진판·출력·시각이 연결된 기록. **판단을 바꿀 관측:** 모든 배열 원소와 표 선 조건을 만족하는 실제 출력이 확인되면 성공+정확판0/8을 갱신할 수 있다. 채택 체크·답변자 데모·참조 매뉴얼판만으로는 그 분자를 올리지 않는다. 도움과 시간 절감 인과효과는 별도 비교 설계가 있어야 판단한다.
'''

if __name__=='__main__':main()
