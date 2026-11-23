"""Normalize already-read diagnostic comments; no remote access or execution of examples."""
from pathlib import Path
import hashlib, json

B = Path(__file__).resolve().parents[1]
S = B / 'streams/jq'
P = B / 'private/jq'
SEAL = '39eec0e2cff033c9d34b55ae20e52880378ac4ef'
READ = '2026-11-23T08:53:30Z'
rows = json.loads((S / 'diagnostics-pre.json').read_text())['rows']
posts, events, outcomes, sources = [], [], [], []
followups = {
    2394: ('OP가 -n을 더한 명령과 세 파일 출력, 별개 후속에서 정상 설계대로 해결됐다는 보고를 남김', 'jq-2394-C1007165070', 'OP_report_with_command_and_output'),
    2406: ('OP가 decnum 빌드 옵션 ON/OFF에 따른 차이를 보고했지만 선택 필드인 실패항목 출력정책 값은 새로 주지 않음', 'jq-2406-C1027839079', 'OP_report_other_field_observed_pair'),
    2331: ('OP는 최신판을 컴파일해 보겠다고 했으나 다음 소비단계 타입조건과 적용 결과는 보고하지 않음', 'jq-2331-C873125139', 'intention_only'),
}
for a in rows:
    n, iid = a['number'], a['issue_id']
    cs = json.loads((P / f'comments-diagnostic-{n}.json').read_text())['comments']
    cs.sort(key=lambda c: (c['created_at'], c['id']))
    events.append(dict(event_id=iid+'-A0', issue_id=iid, actor=a['author'], actor_id=a['author_id'], actor_role='OP', created_utc=a['created_at'], updated_utc=a['created_at'], order=0, original_url=a['original_url'], body_sha256=a['original_body_sha256'], content_location=f"opened event {a['archive_event_id']}; JSONL line {a['archive_line']}", accessed_utc=a['cutoff_A_utc'], phase='A', same_goal=True, selected_field_relation='known_in_A' if a['field_in_A'] else 'unknown_in_A', event_type='original_body', summary=a['goal']))
    for k, c in enumerate(cs, 1):
        op = c['user']['id'] == a['author_id']
        summary = '다른 기여자의 설명·예시·수정 링크'
        relation = 'other_actor_value_not_B'
        if op:
            relation = 'outcome_or_other_field_not_B'
            if c['id'] == 1006818812: summary = '-n을 추가한 실제 명령과 모든 파일 출력 제시; 이전 실행설정의 미확인값을 밝힌 발화는 아님'
            elif c['id'] == 1007165070: summary = '별개 후속에서 해결 및 정상 설계 동작이라고 보고'
            elif c['id'] == 1027839079: summary = 'configure --disable-decnum/--enable-decnum에 따른 결과 차이를 보고; 사전선택 필드 밖'
            elif c['id'] == 873125139: summary = '최신판 컴파일 의도만 밝힘; 소비단계 타입 미응답'
            else: summary = 'OP의 대안 명령·PR 링크·추가 설명; 선택필드 새 값 아님'
        events.append(dict(event_id=f'{iid}-C{c["id"]}', issue_id=iid, actor=c['user']['login'], actor_id=c['user']['id'], actor_role='OP' if op else c.get('author_association','other'), created_utc=c['created_at'], updated_utc=c['updated_at'], order=k, original_url=c['html_url'], body_sha256=hashlib.sha256(c['body'].encode()).hexdigest(), content_location=f'issuecomment-{c["id"]}; full comment read', accessed_utc=READ, phase='post_A_seal', same_goal=op, selected_field_relation=relation, event_type='issue_comment', summary=summary))
    desc, event, level = followups[n]
    status = 'data_absent' if a['question_decision']=='ask' else 'not_applicable_question_skipped'
    p = dict(issue_id=iid, A_seal_sha=SEAL, first_comment_read_utc=READ, raw_timestamp_verification_utc=READ, comment_count=len(cs), pagination='REST page1 returned fewer than100; no further page', selected_field=a['field'], B_status=status, B_value=None, B_actor=None, B_actor_id=None, B_event_id=None, B_utc=None, B_source_url=None, utterance_type='other_question_or_action_response' if n in (2394,2406) else 'different_response_selected_field_absent', added_field_count=0, advice_B='B 자료 없음; A와 같은 후보·판·절을 유지하며 새 필드를 끼워 넣지 않음', recommendation_change='unobservable', accuracy_change='unobservable', new_information=False, actual_followup=desc, actual_followup_event=event, actual_success_level=level, unknowns='실제 질문을 보냈을 때 같은 답을 얻는지·질문비용 미측정; 선택필드 A/B 효과 미관측', same_candidates=True, same_version=True, same_evidence_sections=True)
    if n == 2406: p['unknowns'] += '; OP는1.6이라고 했으나 후속의 decnum 및 유지관리자 회귀설명과 정식1.6 tag 사이 버전 동일성 미확인'
    posts.append(p)
    outcomes.append(dict(outcome_id='OUT-'+iid, issue_id=iid, analysis_layer=a['analysis_layer'], slot=None, comparison_type='no_B', B_status=status, question_decision=a['question_decision'], question_necessity='undecidable' if n==2331 else 'unnecessary_for_selected_field', independent_criterion=n!=2331, independent_evidence='봉인된 A의 실제 명령/기대 출력 및 같은 공식판 지정 절', recommendation_change='unobservable', strict_improvement='not_estimated', table3_outcome='unobservable', resolved_uncertainty=False, independent_followup_event=event, success_level=level, false_positive_denominator=False, false_positive=None, false_positive_reason='질문 미제안' if n!=2331 else '선택필드 무응답이며 원하는 표기 완전달성의 독립 기준 없음; 분모 제외', excluded_counterfactual_count=0, observed_pair_in_A=False, limitations=p['unknowns']))
    sources.append(dict(source_id=f'SRC-JQ-I{n}-DIAG-COMMENTS', lineage_id=f'github-issue-5101141-{n}', kind='issue_comments_same_work', repository_direction='jq', author=';'.join(dict.fromkeys(c['user']['login'] for c in cs)), original_url=f'https://github.com/jqlang/jq/issues/{n}', pinned_url=cs[0]['html_url'] if cs else a['original_url'], version_date=cs[0]['created_at'] if cs else a['created_at'], section_lines=f'all {len(cs)} comments; IDs/hashes/UTC in diagnostic-events.json', accessed_utc=READ, selection_reason='C03 진단 A 봉인 뒤 시간순 읽기', direct_read=True, verified_claim=desc, cannot_determine=p['unknowns'], contrary_or_unknown='후속이 있어도 봉인한 한 필드의 B 값이 없을 수 있음', count_toward_minimum=False, access_status='opened', A_seal_sha=SEAL))

extras = [
 dict(outcome_id='OBS-jq-2394-n', issue_id='jq-2394', analysis_layer='diagnostic_observed_pair_outside_AB', comparison_type='observed_pair', settings='A의 -n 없는 inputs 명령 / OP 후속의 -n 추가 명령', author_event='jq-2394-C1006818812', result='OP 명령·출력에서 첫 파일 포함으로 달라짐; 별개 후속1007165070에서 해결 보고', denominator_inclusion=False, reason='질문 생략 후 행동 대조이며 A의 누락필드 응답 효과 아님'),
 dict(outcome_id='OBS-jq-2406-decnum', issue_id='jq-2406', analysis_layer='diagnostic_observed_pair_outside_AB', comparison_type='observed_pair_author_report', settings='--disable-decnum / --enable-decnum', author_event='jq-2406-C1027839079', result='같은 OP가 두 설정의 결과 차이를 보고; 두 실행의 원출력·동일 revision 미확인', denominator_inclusion=False, reason='봉인한 실패항목 출력정책이 아닌 실행설정; 사후 필드 교체 금지'),
]
for name, data in [('diagnostic-post.json', posts), ('diagnostic-events.json', events), ('diagnostic-outcomes.json', outcomes), ('observed-pairs.json', extras)]:
    (S/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
(S/'sources-diagnostic-post.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
(S/'diagnostic-counterexamples.md').write_text('''# jq 진단과 반례 판독

- #2394: A의 실제 명령에 -n 부재가 있어 질문 생략. OP는 -n을 적용한 명령·출력을 제시하고 별개 댓글에서 해결됐다고 보고했다. 이는 그냥 답하기가 가능한 실제 행동 대조다. 사후에 바뀐 옵션을 최초 상태의 새 B 값으로 바꾸지 않는다. 현재본문의 후대 매뉴얼링크 선노출 때문에 깨끗한 사전판독으로 세지 않는다.
- #2406: A의 기대출력1,3은 실패항목 생략을 이미 규정한다. 그러나 후속에서 OP가 decnum 빌드 설정 차이를 보고했다. 목적필드만으로 실행 버그를 모두 해결할 수 있다는 주장에 대한 반례다. 이를 사전선택 목적필드의 B에 넣지 않는다. OP의1.6명칭과 정식1.6 tag의 일치는 미확인이다.
- #2331: 다음 소비단계의 숫자형 요구 여부를 미리 물었지만 OP는 최신판을 컴파일하겠다는 의도만 남겼다. 후속 댓글이 존재한다는 것과 선택필드 응답은 다르다. 무응답만으로 질문 오탐이나 권고 개선0으로 세지 않는다.

짝 탐색: #2267과 #2406은 같은 숫자문자열 변환/오류후 계속처리 동작이지만, A가 요구하는 실패출력은 각각null/생략으로 다르다. 목적값이 후보를 가르는 대비로만 쓴다. 둘 다 선택필드의 새B가 없어 질문효과의 응답/무응답 대조로는 부적합하다. #2349와#2394는 배열병합이라는 넓은 동작은 같아도 그룹키 보존과 입력소비 단계가 달라 엄격한 정보추가무효 짝을 채우지 않는다.
''')
print(json.dumps({'posts':len(posts),'events':len(events),'outcomes':len(outcomes),'observed_pairs':len(extras)}))
