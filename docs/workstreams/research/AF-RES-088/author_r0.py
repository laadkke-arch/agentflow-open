"""Materialize the pre-R1 reading. Deliberately reads only r0_packet.json."""
import csv
import hashlib
import json
import gzip
from datetime import datetime, timezone
from pathlib import Path

P = Path(__file__).resolve().parent
NOW = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

CASES = [
    ('JN1', 'jq', 1, 78253195, 'natural', '날짜별 weather 값들을 대괄호가 있는 배열로 수집', '이미 맞게 추출되는 RainProbability·Grass Value를 유지', 'p1;Query1;Query2;pre1,pre3', 'indexed response/array', 'correct values', 'JSON object.DailyForecasts[]; Day.RainProbability; AirAndPollen[1].Value', 'JSON array; Bash 소비 의도도 언급', '', 'map 시도; -r; 기본 field traversal', '명시 금지 없음'),
    ('JN2', 'jq', 2, 78262117, 'natural', 'helm show chart의 YAML 출력을 파싱해 version 속성 추출', '', 'p1;pre1;pre2;p3', 'retrieve the version attribute', '', 'YAML key/value와 dependencies 목록', 'JSON과 version 값', '', 'jq .; parse error; helm', '명시 금지 없음'),
    ('JE1', 'jq', 5, 78296361, 'edited', 'page_data를 LangChain Document.page_content로 적재', 'page_name·page_url을 Document.metadata의 기존 source·seq_num과 함께 저장', 'h3;h6;pre1 final docs', 'page_content', 'page_name', 'JSON 객체 배열, JSONLoader jq_schema', 'Python Document 객체 목록', '', 'LangChain JSONLoader; jq_schema=.[].page_data', '명시 금지 없음'),
    ('JE2', 'jq', 7, 78305924, 'edited', 'Documents의 각 레코드를 JSON Lines의 한 줄 객체로 출력', '바깥 _rid는 없애고 각 레코드 안의 _rid는 보존', 'p1;p2;pre1;pre2', 'each record its own line', 'not the ones inside', 'root object with Documents array, outer _rid and _count', 'JSONL object per line', '', 'select; map; --slurp; --compact-output 시도', '레코드 내부 _rid 제거 금지'),
    ('PN1', 'pandoc', 1, 78258237, 'natural', 'PDF 표 중간에 열을 가로지르는 연속 수평선 추가', '열 제목 아래 선과 같은 굵기·색으로 표시', 'p1;pre1;last p', 'continuous horizontal rule', 'same thickness and color', 'Markdown pipe table; dash row; PDF screenshot', 'PDF table', 'pandoc 2.9.2.1; pandoc-types 1.20; texmath 0.12.0.2; skylighting 0.8.5', 'pipe table; EM DASH/hyphen; 다른 표형식 허용', '명시 금지 없음'),
    ('PN2', 'pandoc', 2, 78267487, 'natural', '제시한 HTML 수식을 유효한 AsciiDoc asciimath 또는 latexmath stem 블록으로 변환', '', 'p1;pre1;p4;pre2;last p', 'asciimath or latexmath stem block', '', 'nested styled HTML spans representing a formula', 'AsciiDoc stem block preserving that formula', '', 'HTML preprocessing 또는 Pandoc 밖 자체변환도 열어둠', '명시 금지 없음'),
    ('PE1', 'pandoc', 4, 78300525, 'edited', 'PDF 코드 블록의 줄번호를 페이지 여백 안으로 배치', 'Pandoc flavored Markdown에서 PDF를 만드는 경로에 적용', 'p1;code .numberLines;last p', 'line numbers goes outside page margins', 'pandoc flavored markdown', 'Markdown code block {.lang .numberLines}; linked PDF screenshot', 'PDF code block with numbers within margins', '', '기존 pure LaTeX 답 링크; .numberLines', '명시 금지 없음'),
    ('PE2', 'pandoc', 12, 78461996, 'edited', 'Quarto chunk의 출력 결과를 기본 접힘 상태로 두되 독자가 펼쳐 읽을 수 있게 함', '', 'p1;p2..p11', 'folding the output of the chunk', '', 'Quarto Python print and R sessionInfo examples (code fences rendered as paragraphs)', 'rendered report with folded output; writer not specified', '', 'code-fold: true는 코드 접기 비교 단서', '출력 삭제 요구 아님'),
]

OUT = '범위 밖'
REF = '명시 반박'
UNK = '미확인'
YES = '충족'

# One row per case and candidate; reasons are written before any R1 body or answer.
J = {
 'JN1': [
  (OUT,'오답','값 통과/제거는 배열 수집 요구를 수행하지 않는다. select(true)를 덧붙여도 핵심은 외부 배열 생성이다.','수집 자체에 기여하는 후보가 필요'),
  (YES,'정합','.DailyForecasts | map(.Day.RainProbability), 별도 쿼리 map(.AirAndPollen[1].Value)는 선택한 값을 배열로 수집한다. 정렬 순서는 요구하지 않았다.','전체 입력에서 DailyForecasts 배열 및 각 field 존재 확인; Bash 배열과 JSON 배열은 별도'),
  (OUT,'오답','sort_by는 이미 있는 배열의 원소를 정렬할 뿐 nested 값 추출·수집을 하지 않는다. to sort는 배열 확보 뒤의 목적이다.','정렬 키/순서를 추가 요구하면 별도 검토'),
  (REF,'오답','group_by는 그룹별 하위 배열을 출력하므로 요구한 값 배열과 출력 구조가 다르다.','그룹별 배열을 원하는지 원문 수정이 있어야 바뀜')
 ],
 'JN2': [(REF,'오답','주어진 입력은 YAML이며 jq는 필터 전에 JSON을 파싱한다. 이 후보는 YAML→JSON parser가 아니다. -R도 YAML 의미를 파싱하지 않는다.','JSON으로 변환된 입력 또는 외부 YAML parser 허용')]*4,
 'JE1': [
  (OUT,'오답','select는 record 통과/제거만 하며 Document.page_content와 metadata의 결합 API를 제공하지 않는다.','JSONLoader 버전·content_key·metadata callback 계약'),
  (OUT,'오답','map으로 JSON 객체를 만들 수 있어도 실제 Python Document 속성과 기존 metadata 결합은 JSONLoader의 계약이다. 같은 이름 JSON키가 소비자 속성 설정을 증명하지 않는다.','JSONLoader가 결과 객체를 어떻게 소비하는지와 callback 코드'),
  (OUT,'오답','sort_by의 순서 변경은 page_content/metadata 배치를 수행하지 않는다.','JSONLoader의 변환 및 metadata 결합 경로'),
  (OUT,'오답','group_by의 그룹 배열은 Document metadata 주입 기능이 아니다.','JSONLoader의 변환 및 metadata 결합 경로')
 ],
 'JE2': [
  (OUT,'오답','필요한 핵심은 Documents 배열 순회와 한 객체씩 직렬화이다. 모든 record를 통과하는 select는 요구에 기여하지 않는다.','Documents[] 및 compact output 같은 풀 밖 기능 검토'),
  (REF,'오답','map의 직접 출력은 배열이다. 요구는 배열 wrapper 없이 객체 하나당 한 줄이다. 추가 순회/직렬화가 핵심인 구성을 단일 map 성공으로 세지 않는다.','풀 밖 순회·compact serialization 허용'),
  (REF,'오답','sort_by의 직접 출력은 배열이며 JSONL 객체 스트림이 아니다. 정렬은 원문 목적도 아니다.','풀 밖 순회·compact serialization 허용'),
  (REF,'오답','group_by의 직접 출력은 하위 배열들의 배열로, 원하는 객체별 JSONL과 구조가 다르다.','풀 밖 순회·compact serialization 허용')
 ],
 'PN1': [
  (OUT,'오답','메타데이터 설정은 표 내부 원하는 행에 선을 삽입하는 연산이 아니다.','Table/LaTeX 출력 행을 바꾸는 별도 구성'),
  (OUT,'오답','템플릿의 body 바깥 틀/변수 배치는 표 내부 특정 행의 선을 생성하지 않는다. 입력과 무관한 정답 테이블 하드코딩은 계약 밖이다.','표 내부 처리 코드 또는 다른 테이블 입력'),
  (UNK,'조건부','Lua의 Table 처리와 writer별 raw 출력으로 접근할 수 있으나 선 위치·굵기·색을 보존하는 실제 handler와 PDF writer/engine 결과가 없다. 옵션만으로 충족이라 하지 않는다.','3.1.11 AST·Table handler·LaTeX/PDF 엔진·출력 선 대조'),
  (OUT,'오답','standalone은 독립 문서 wrapper이며 PDF에서는 이미 자동이다. 중간 행 선을 추가하지 않는다.','Table/LaTeX 출력 행을 바꾸는 별도 구성')
 ],
 'PN2': [
  (OUT,'오답','metadata 설정은 HTML 수식 span의 의미를 읽어 Math/AsciiDoc stem으로 바꾸지 않는다.','원 HTML→Math AST 변환 경로'),
  (OUT,'오답','template은 writer 본문을 감싸며 nested span 수식을 해석하지 않는다.','원 HTML→Math AST 변환 경로'),
  (UNK,'조건부','Lua는 AST 변환 지점을 제공하지만 HTML reader가 subscript 구조·class를 보존하는지와 Math 생성 handler가 없다. 원 수식 정보가 사라졌다면 뒤 필터로 복원할 수 없다.','같은 HTML의 native AST·Math handler·AsciiDoc 출력'),
  (OUT,'오답','standalone wrapper는 수식 표현의 semantic parsing을 바꾸지 않는다.','원 HTML→Math AST 변환 경로')
 ],
 'PE1': [
  (UNK,'조건부','header-includes 메타데이터가 기본 LaTeX 템플릿에 삽입되는 경로는 있으나 줄번호 여백을 고치는 LaTeX 재정의 코드·엔진 결과가 없다.','실제 highlighting 환경·header-includes 코드·같은 PDF 출력'),
  (UNK,'조건부','고정 default.latex의 highlighting-macros 삽입 지점을 가진 사용자 template로 조정할 수 있는 경로다. 실제 환경 재정의와 PDF 확인 없이는 완전 충족 미확인이다.','사용 template·highlighting style·LaTeX 엔진·여백 측정'),
  (UNK,'조건부','CodeBlock 또는 raw writer 변환은 가능하나 번호와 코드내용을 보존하며 margin 안에 두는 handler·출력 증거가 없다.','CodeBlock AST·handler·PDF 출력 대조'),
  (OUT,'오답','PDF에서 이미 켜지는 standalone은 코드 줄번호의 간격·위치를 변경하지 않는다.','highlighting/LaTeX 레이아웃 구성')
 ],
 'PE2': [
  (OUT,'오답','임의 metadata 키는 Quarto chunk output 접기를 구현하지 않는다. Pandoc 고정 매뉴얼에 해당 키 동작이 없다.','Quarto의 실제 chunk/output 옵션 또는 변환 코드'),
  (OUT,'오답','template의 문서 wrapper는 특정 chunk 출력과 코드의 경계를 식별해 접지 않는다.','chunk-output AST 대상 변환'),
  (UNK,'조건부','HTML writer라면 chunk 출력 Div를 details/summary로 감싸는 Lua 설계가 가능하지만 writer와 실제 AST/handler가 미확인이다.','출력 형식·Quarto가 만든 output Div·Lua handler'),
  (OUT,'오답','독립 문서 생성은 접기 상호작용을 제공하지 않는다.','출력 writer와 chunk-output 접기 구현')
 ]
}


def dump_csv(path, rows):
    with (P/path).open('w', newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    packets=json.loads((P/'r0_packet.json').read_text()) if (P/'r0_packet.json').exists() else json.loads(gzip.decompress((P/'r0_packet.json.gz').read_bytes()))
    candidates=list(csv.DictReader((P/'candidates.csv').open()))
    reqs=[]; revisions=[]; judgments=[]
    (P/'evidence/r0').mkdir(parents=True,exist_ok=True)
    for case,tool,rank,qid,stratum,c1,c2,loc,ex1,ex2,inp,out,env,clue,forbid in CASES:
        q=next(x for x in packets if x['question_id']==qid and x['tag']==tool)
        r=q['r0']; body=r['body']; fp=f'evidence/r0/{qid}.html'; (P/fp).write_text(body)
        url=f'https://stackoverflow.com/revisions/{qid}/{r["revision_number"]}'
        req=dict(case_id=case,tool=tool,question_id=qid,original_rank=rank,stratum=stratum,revision='R0',guid=r['revision_guid'],revision_number=r['revision_number'],created_utc=q['created_utc'],revision_utc=datetime.fromtimestamp(r['creation_date'],timezone.utc).isoformat().replace('+00:00','Z'),revision_url=url,c1=c1,c2=c2,c2_absence_reason='' if c2 else '원문에 독립된 별도 제약이 명시되지 않음',evidence_location=loc,short_excerpt_c1=ex1,short_excerpt_c2=ex2,input_structure=inp,desired_output=out,stated_environment=env,solution_clues=clue,explicit_prohibitions=forbid,read_by='root; jq frame eligibility additionally checked by manuals subagent',direct_read_utc=NOW,answers_exposed=False,r1_body_exposed=False,body_path=fp,raw_sha256=hashlib.sha256(body.encode()).hexdigest(),lf_sha256=hashlib.sha256(body.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest(),format='API revision.body HTML',strict_initial_bytes='미확인',strict_initial_reason='별도 동시대 게시 바이트 증거 없음; grace 병합 가능')
        reqs.append(req)
        revisions.append(dict(case_id=case,site='stackoverflow',question_id=qid,stratum=stratum,original_rank=rank,history_url=f'https://stackoverflow.com/posts/{qid}/revisions',question_created_utc=q['created_utc'],history_complete=True,history_records=q['history_records'],separate_body_edits_30d=q['separate_body_edits_30d'],r0=req,r1=None,history_metadata=q['history_metadata'],initial_bytes_verified=False,r1_read_after_r0_commit=None))
        cc=[x for x in candidates if x['tool']==tool]
        for cand,(state,disposition,reason,next_input) in zip(cc,J[case]):
            c2state='해당 없음' if not c2 else YES if state==YES or case in ['JE2','PE1'] else OUT if case=='JE1' else UNK
            extra='https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L78-L89' if case=='JN2' else 'https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/data/templates/default.latex#L249-L251;https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/data/templates/default.latex#L397-L399' if case=='PE1' else ''
            judgments.append(dict(case_id=case,question_id=qid,stratum=stratum,revision='R0',candidate_id=cand['candidate_id'],candidate_function=cand['function'],reference_tag=cand['tag'],reference_sha=cand['tag_sha'],question_revision_guid=r['revision_guid'],question_url=url,question_evidence_location=loc,c1=c1,c2=c2,c1_status=state,c2_status=c2state,assessment=state,return_status=disposition,reason=reason,configuration=('.DailyForecasts | map(.Day.RainProbability); .DailyForecasts | map(.AirAndPollen[1].Value)' if case=='JN1' and cand['function']=='map' else ''),requires_user_code=('yes' if cand['candidate_id'] in ['PD-lua-filter','PD-template'] else 'conditional' if case=='PE1' and cand['candidate_id']=='PD-metadata' else 'no'),manual_url=cand['section_url'],manual_additional_urls=extra,manual_source_ids=cand['source_ids'],failure_rule=cand['failure_rule'],next_minimum_input=next_input,execution='not executed; documentary adjudication',read_utc=NOW,r1_or_answers_exposed='false'))
    (P/'requirements_r0.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in reqs))
    (P/'revisions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in revisions))
    dump_csv('judgments.csv',judgments)
    print('R0 cases',len(reqs),'judgments',len(judgments),'R1 and answers not read')


if __name__=='__main__':
    main()
