"""Materialize the post-seal, human-read response evidence; never revises R0 scores."""
import hashlib
import json
from collect import P, utc

PAIR_SEAL = 'f048885abfbfcca1ffd8840899bf2911cd35da60'
COMMENT_NOTES = {
137958376:'다른 독자가 원 JSON 추가를 요청했다.',
137958556:'다른 독자가 대괄호 수집 표현을 제안했다.',
137960567:'질문자는 Bash 배열로 바꿀 때 첫 값만 남는다고 보고했다.',
137960636:'질문자는 숫자2/단어Breezy만 남는 실패와 full JSON 추가를 보고했다.',
138511257:'다른 독자가 shell 배열 할당식의 문제와 별도 질문 필요를 지적했다.',
137973668:'다른 독자가 jq/JSON과 yq/YAML 경계를 지적했다.',
137974824:'다른 독자가 YAML 입력임을 재확인했다.',
137976008:'다른 독자가 풀 밖 gojq를 제안했다.',
137978485:'다른 독자가 JSON subset과 YAML parser 기능 차이를 설명했다.',
137975317:'질문자는 grid table의 효과가 원하는 것이라고 했으나 당장은 기존 방식, 다음 작업에 사용할 계획이라고 말했다.',
137983221:'다른 독자가 원 HTML 생성기와 다른 수식 형식 확보 가능성을 질문했다.',
137986143:'질문자는 수식이 많아 수동 변환이 불가하다고 사후 명시하고 외부 변환기를 시도하겠다고 말했다.',
137986449:'질문자는 외부 변환 결과에서 수식 wrapper가 없어 일반 텍스트와 구별되지 않는다고 보고했다.',
138328053:'다른 독자가 Quarto issue341과 당시 우회법의 R/Python 범위 차이를 안내했다.',
139051384:'질문자는 제시 코드를 어디에 두는지 되물었으며 chunk option은 아니라고 지적했다.',
139400133:'다른 독자가 해법을 찾았는지 질문했다.',
140265140:'다른 독자가 처음 답에 연결된 이미지에 배치 설명이 있다고 답했다.'}
NOTES = {
 'JN1': dict(primary='map; optional map+select extension', pool='one fixed candidate supports the JSON-array subgoal; the robust Grass-name extension combines two candidates', agreement='문서상 map 배열화와 답의 두 출력은 일치. 질문자 댓글의 최종 Bash native-array 목적과 실행 문제는 별개이며 성공으로 올릴 수 없다.', followup='질문자는 첫 답보다 앞선 댓글에서 Bash 배열 변환 시 첫 숫자2/첫 단어Breezy만 남는다고 보고하고 전체 JSON 추가를 알렸다.', attempt=True, success=False, exact_version=False, next='Bash 선언/할당 명령·shell판·jq판·실제 전체 배열 출력', accepted_outside=None),
 'JN2': dict(primary='yq YAML processor', pool='outside fixed jq function pool', agreement='채택 답의 YAML/JSON 경계는 네 jq 후보의 명시 반박과 일치. yq로 바꾸라는 제안은 풀 밖이다.', followup='질문자 후속 실행·출력 댓글 없음. 현재 채택 표지만 관측.', attempt=False, success=False, exact_version=False, next='사용한 yq 배포/판·동일 helm 출력·version 추출 결과', accepted_outside=True),
 'JE1': dict(primary='to_entries + map with invented source and seq_num', pool='extra jq function plus a JSON demonstration; actual JSONLoader Document API not shown', agreement='답은 JSON 객체 모양을 시연하지만 실제 Document 속성 주입을 증명하지 않는다. source를 가정했다고 명시한다. 두 프로그램은 seq_num을 다르게 계산하며 게시된 [1,1]은 첫 프로그램과 일치한다. jq1.7 보조 실행에서 첫 식 [1,1], 둘째 [1,2]를 확인했다. 고정1.7.1 및 질문자의 JSONLoader 실행은 미확인이다.', followup='질문자 후속 댓글·채택·정확 LangChain판·실행 출력 없음.', attempt=False, success=False, exact_version=False, next='JSONLoader판·content_key/metadata_func 연결 코드·실제 Document 두 개', accepted_outside=None),
 'JE2': dict(primary="jq -c '.Documents[]'", pool='outside fixed four candidates: traversal plus compact serialization', agreement='풀 밖 순회/직렬화가 핵심이라는 사전 판정과 일치. 답의 online demo 링크는 있으나 링크 실행판·질문자 실행은 확인하지 않았다.', followup='첫 답을 쓴 oguz ismail이 다음날 질문 문구/태그를 정리. 질문자 채택·실행 기록 없음.', attempt=False, success=False, exact_version=False, next='원 JSON·jq판·JSONL 각 줄의 parser 검증 및 내부 _rid 보존 출력', accepted_outside=None),
 'PN1': dict(primary='grid_tables footer rows (Pandoc >=3); separate raw LaTeX hline answer for 2.9', pool='accepted primary solution outside four options; optional parse-latex filter mentioned for another route', agreement='현재 채택은 grid-table 입력 형식의 답. 질문자는 원하던 효과라고 말했지만 당장은 기존 방법을 쓰고 다음에 이용하겠다고 명시했다. 채택을 즉시 실행 성공으로 읽으면 틀린다.', followup='원 질문에 Pandoc2.9.2.1 보고. 채택 답은3이상 필요. 질문자 댓글은 향후 사용 계획이며3.x 실행 확인이 아니다.', attempt=False, success=False, exact_version=True, version='pandoc 2.9.2.1 (original problem self-report only)', next='동일 표를 실제 사용판과3.1.11에서 변환한 PDF·엔진·중간선 굵기/색·버전 출력', accepted_outside=True),
 'PN2': dict(primary='manual STEM markup; external HTML-to-Markdown conversion plus manual repair', pool='outside fixed four options', agreement='대량 수식 때문에 수동 방식은 안 된다는 제약이 사후 댓글에서 명시된다. R0/R1 C2로 소급하지 않는다. 질문자는 외부 변환 출력에서 수식 wrapper가 없어 실패한다고 보고했다.', followup='답변자 외부 변환 시연과 질문자 실패 보고를 구별. 정확 프로그램판·완전 성공 출력 없음.', attempt=True, success=False, exact_version=False, next='원 HTML 생성기·대량 수식 표본·reader native AST·수식 경계 보존 출력', accepted_outside=None),
 'PE1': dict(primary='raw LaTeX DefineVerbatimEnvironment/Highlighting xleftmargin', pool='accepted method edits document raw LaTeX; not itself one of the four fixed options', agreement='LaTeX 환경 재정의 경로가 사후 구체화됐지만 고정 옵션만의 성공이나 원 사용판/PDF 결과는 확인되지 않는다. 원 그림 미확인을 해소하지 않는다.', followup='답 후45초에 답변자 tarleb가 질문의 기존 이미지 링크를 본문 이미지로 바꿈. 현재 채택만 있고 질문자 실행 댓글 없음.', attempt=False, success=False, exact_version=False, next='R0 A0Wtm.png 원본·실제 Highlighting 환경/엔진·같은 입력의 여백 측정 PDF', accepted_outside=True),
 'PE2': dict(primary='Quarto callout collapse; later HTML details and Quarto extensions', pool='outside fixed Pandoc option pool', agreement='30일 내 답변0이나 질문댓글1은 있다. 첫 답의 이미지 중심 지시 뒤 질문자는 코드 위치를 되묻는다. 나중의 답/개정을 초기 해법 설명으로 소급하면 틀린다.', followup='질문자 댓글은 chunk option이 아닌 코드의 위치 질문. 성공 출력·설치판 없음. 2026년 추가 답도 별도 시점.', attempt=False, success=False, exact_version=False, next='출력 형식·Quarto판·knitr/Jupyter·생성 AST/HTML·실제 펼침 동작', accepted_outside=None),
}


def main():
    now = utc()
    packet = json.loads((P/'outcome_packet.json').read_text())
    assert packet['answer_exposure_after_commit'] == PAIR_SEAL
    cases = [json.loads(x) for x in (P/'revisions.jsonl').read_text().splitlines()]
    result, sources = [], []
    (P/'evidence/answers').mkdir(parents=True, exist_ok=True)
    for c in cases:
        cid, qid = c['case_id'], c['question_id']
        q = next(x for x in packet['questions'] if x['question_id'] == qid)
        answers = sorted([a for a in packet['answers'] if a['question_id']==qid], key=lambda x:(x['creation_date'],x['answer_id']))
        postids = {qid}|{a['answer_id'] for a in answers}
        comments = sorted([x for x in packet['comments'] if x['post_id'] in postids],key=lambda x:(x['creation_date'],x['comment_id']))
        first_time = answers[0]['creation_date'] if answers else None
        cutoff = q['creation_date'] + 30*86400
        aa, timeline = [], []
        for r in c['revision_editors']:
            timeline.append(dict(kind='question_revision', utc=r['utc'], guid=r['guid'], number=r['number'], user=r['user'], body=r['body'], title=r['title'], tags=r['tags'], is_rollback=r['is_rollback']))
        for a in answers:
            aid = a['answer_id']
            rr = sorted([r for r in packet['answer_revisions'] if r['post_id']==aid and 'body' in r],key=lambda r:(r['creation_date'],r.get('revision_number',0),r['revision_guid']))
            r = rr[0]
            path = f'evidence/answers/{aid}_first.html'
            (P/path).write_text(r['body'])
            u = f'https://stackoverflow.com/revisions/{aid}/{r["revision_number"]}'
            demo_kind = 'printed output' if aid in (78266070,78299501) else ('answerer reports external converter output' if aid==78269109 else ('answerer describes working result and line-placement limitation' if aid==78261053 else 'no concrete output or explicit observed-result prose'))
            x = dict(answer_id=aid, author=r.get('user'), answer_created_utc=utc(a['creation_date']), first_body_guid=r['revision_guid'], first_body_number=r['revision_number'], first_body_utc=utc(r['creation_date']), first_body_url=u, first_body_path=path, first_body_sha256=hashlib.sha256(r['body'].encode()).hexdigest(), historical_body_revisions=len(rr), current_body_differs_from_first=a['body']!=r['body'], current_is_accepted=a.get('is_accepted',False), accepted_time='unknown', within_30d=a['creation_date']<=cutoff, answerer_demo_kind=demo_kind, answerer_textual_result_evidence=aid in (78266070,78299501,78269109), answerer_concrete_output_text=aid in (78266070,78299501,78269109), answerer_prose_result_report_only=aid==78261053, answerer_result_report=aid in (78266070,78299501,78269109,78261053), externally_linked_demo_or_image=aid in (78305953,78260959,78261053,78854242,79918498), external_demo_opened_or_run=False, questioner_run_verified=False, exact_success_runtime_verified=False)
            aa.append(x)
            for ar in rr:
                timeline.append(dict(kind='answer_body_revision',utc=utc(ar['creation_date']),answer_id=aid,guid=ar['revision_guid'],number=ar.get('revision_number'),user=ar.get('user')))
            sources.append(dict(source_id=f'OUT-A-{aid}-FIRST',independent_event_id=f'SO-{qid}',kind='answer earliest preserved body',url=u,version=r['revision_guid'],location='first historical answer body; command/output and qualifications',direct_read_utc=now,read_time_basis='root reading completion checkpoint after paired judgment seal',questions=['Q6'],cases=[cid],claim_ids=['post-seal actual response','acceptance vs execution','outside-pool alternatives'],confirmed=NOTES[cid]['agreement'],observer='answer author; root reads preserved body; no local execution',evidence_relation='qualifies presealed documentary judgments; does not overwrite them',limitations='first preserved answer bytes may include grace edits; linked demo/image not executed or inspected; current acceptance timestamp unknown',count_primary=True,primary_unit=f'SO-ANSWER-{aid}-REV-{r["revision_guid"]}',snapshot_path=path))
        for cm in comments:
            cu=f'https://stackoverflow.com/questions/{qid}#comment{cm["comment_id"]}_{cm["post_id"]}'
            timeline.append(dict(kind='public_comment',utc=utc(cm['creation_date']),comment_id=cm['comment_id'],post_id=cm['post_id'],user=cm.get('owner'),edited=cm.get('edited'),body_html=cm['body'],url=cu,within_30d=cm['creation_date']<=cutoff,by_questioner=cm.get('owner',{}).get('user_id')==q.get('owner',{}).get('user_id')))
            sources.append(dict(source_id=f'OUT-C-{cm["comment_id"]}',independent_event_id=f'SO-{qid}',kind='public comment',url=cu,version=f'comment {cm["comment_id"]}; created {utc(cm["creation_date"])}; current edited={cm.get("edited")}',location='comment body',direct_read_utc=now,questions=['Q6'],cases=[cid],claim_ids=['public follow-up timing and evidence level'],confirmed=COMMENT_NOTES[cm['comment_id']],observer=cm.get('owner',{}).get('display_name','unknown'),evidence_relation='public statement only; author role preserved in timeline',limitations='comment edit history/deleted comments unavailable; not independent from question event; no execution verification',count_primary=False,primary_unit=f'SO-COMMENT-{cm["comment_id"]}',exclusion_reason='conservative count: comments supplement their question event, not extra minimum-source units'))
        bodies_after=[]
        for r in c['history_metadata']:
            if r['has_body'] and r.get('revision_number',0)>1 and first_time is not None and r['creation_date']>first_time:
                bodies_after.append(dict(guid=r['revision_guid'],number=r['revision_number'],utc=utc(r['creation_date']),user=r.get('user'),by_questioner=r.get('user',{}).get('user_id')==q.get('owner',{}).get('user_id')))
        own_comments=[x for x in timeline if x['kind']=='public_comment' and x['by_questioner']]
        result.append(dict(case_id=cid,question_id=qid,stratum=c['stratum'],read_utc=now,read_after_pair_commit=PAIR_SEAL,observed_current_question_url=q['link'],question_created_utc=utc(q['creation_date']),current_answer_count=q['answer_count'],answer_records=len(answers),answers_within_30d=sum(a['creation_date']<=cutoff for a in answers),comments_within_30d=sum(x['creation_date']<=cutoff for x in comments),question_comments_within_30d=sum(x['creation_date']<=cutoff and x['post_id']==qid for x in comments),current_accepted_answer_id=q.get('accepted_answer_id'),acceptance_time='unknown; current marker only',first_answer_utc=utc(first_time) if first_time else None,question_body_edits_after_first_answer=bodies_after,author_body_edits_after_first_answer=sum(x['by_questioner'] for x in bodies_after),author_solution_insertion_after_answer=0,author_followup_comments=len(own_comments),questioner_followup_attempt_reported=NOTES[cid]['attempt'],questioner_complete_success_reported=NOTES[cid]['success'],questioner_exact_tool_version_reported=NOTES[cid]['exact_version'],questioner_exact_version=NOTES[cid].get('version'),questioner_success_with_exact_runtime_verified=False,answerer_textual_result_count=sum(x['answerer_textual_result_evidence'] for x in aa), answerer_concrete_output_text_count=sum(x['answerer_concrete_output_text'] for x in aa), answerer_prose_result_report_only_count=sum(x['answerer_prose_result_report_only'] for x in aa), answerer_result_report_count=sum(x['answerer_result_report'] for x in aa),accepted_primary_solution_outside_pool=NOTES[cid]['accepted_outside'],response_interpretation=NOTES[cid],answers=aa,timeline=sorted(timeline,key=lambda x:(x['utc'],x['kind'])),limitations=['public/deleted material selection; no acceptance history','comment text read now, not historical comment byte archive','answerer demonstration does not establish questioner execution','same reader; answer evidence never substituted for sealed R0/R1 judgments']))
    (P/'outcomes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in result))
    (P/'support/sources_outcomes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    print('outcomes',len(result),'answer sources',sum(x['count_primary'] for x in sources),'comment support records',sum(not x['count_primary'] for x in sources))


if __name__=='__main__': main()
