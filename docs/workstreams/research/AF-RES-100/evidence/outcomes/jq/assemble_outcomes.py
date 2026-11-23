"""Build post-seal attribution records from preserved API cache.
Human interpretations are explicit below; no initial judgment is read or changed.
"""
import datetime, hashlib, json, pathlib
P = pathlib.Path(__file__).resolve().parent
C = P / '_cache'
load = lambda name: json.loads((C / name).read_text())
questions = load('questions-items.json')
answers = load('answers-items.json')
revisions = load('revisions-items.json')
comments = load('comments-items.json')
receipts = json.loads((P / 'fetch-receipts.json').read_text())
receipt = {r['label']: r for r in receipts}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
iso = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).isoformat()
sha = lambda text: hashlib.sha256(text.encode()).hexdigest()
case_ids = {79694539: 'J1', 79699191: 'J2', 79711268: 'J3', 79727040: 'J4'}
question_map = {q['question_id']: q for q in questions}
answer_map = {a['answer_id']: a for a in answers}
post_question = {q: q for q in case_ids} | {a['answer_id']: a['question_id'] for a in answers}
SEAL = '5d81bcbeb5f1248fc1dd2ce2d825cf6467353673'
first_access = receipt['questions-1']['checked_utc']

comment_notes = {
140574771: ('제3자가 두 원 JSON과 기대 출력의 최소 예시를 요청한다.', 'missing_input_request'),
140574783: ('제3자가 input[] 대신 inputs[]를 시도하라고 제안한다.', 'suggestion_no_execution'),
140577987: ('질문자는 inputs[]로 바꾸면 jq가 오류 없이 종료하지만 file2 객체의 JOIN은 수행하지 않아 원하는 해결이 아니라고 보고한다.', 'asker_failed_goal_despite_clean_exit'),
140793862: ('질문 97일 뒤 제3자가 비인쇄/제어문자 또는 stream 제어동작을 원인 후보로 추측한다. 재현이나 실제 원인 확인은 없다.', 'post30day_thirdparty_hypothesis'),
140584408: ('제3자가 yq 뒤 sed와 jq를 붙이지 않고 yq만 쓰는 대안을 제안한다.', 'alternative_toolchain'),
140584414: ('제3자가 각 Data 원소를 Name/content 객체로 갱신하는 필터와 외부 데모 링크를 제안한다. 데모는 이 조사에서 열거나 실행하지 않았다.', 'suggestion_no_execution'),
140584425: ('제3자가 map/from_entries로 Data를 하나의 사전으로 바꾸는 다른 필터와 데모를 제안한다. 데모는 열거나 실행하지 않았다.', 'suggestion_no_execution'),
140584449: ('질문자는 sed가 익숙하고 여러 깊이의 +/+@ 이름을 정리하려고 썼다고 설명한다. 두 제안은 각각 null 반복 오류와 content 문자열 인덱싱 오류를 냈다고 보고한다.', 'asker_failed_execution_report'),
140584453: ('질문자는 content=null인 필드를 찾아 CertIssuerName/CertSerialNumber/CertThumbprint 각7, CommandLine11, ParentProcessName2, ProcessName1, ShareLocalPath4, TaskContent1을 보고한다. 전체 원파일과 판은 없다.', 'asker_diagnostic_output_report'),
140584463: ('질문자의 수신자 이름 정정이며 실행·완결 근거가 아니다.', 'communication_correction'),
140610649: ('제3자가 Bash single quote가 변수확장을 막는다고 설명하고 문자열 삽입 형태의 예시를 제안한다. 실제 실행을 확인한 댓글은 아니다.', 'quoting_explanation_suggestion'),
140613089: ('질문자가 변수확장 설명에 감사하며 이해됐다고 말한다. 정확 명령·출력·판을 제시한 실행 영수증은 아니다.', 'asker_generic_positive_feedback'),
140613110: ('질문자는 답의 $@를 JSON 내용 변수로 교체하자 jq가 JSON 문자열을 파일명으로 취급하여 File name too long 오류를 냈다고 보고한다.', 'asker_failed_execution_report'),
140613115: ('답변자가 $@는 스크립트 호출 인수들의 목록이므로 그대로 두라고 정정한다. 답변자 자신의 실행 보고는 없다.', 'answerer_argument_contract_clarification'),
140613190: ('질문자는 $@를 그대로 사용하니 작동하고, 자신의 경우 추가 JSON 파일이 하나라 $1과 같은 결과라고 보고한다. 최종 JSON·argv·환경판 로그는 없다.', 'asker_success_selfreport_partial_identity'),
}

question_notes = {
'J1': '현재 질문 본문은 최초 revision과 바이트 동일하다. 추가 완전 원입력·jq판·정확 기대 JOIN출력은 여전히 없다.',
'J2': '현재 질문 본문은 revision2와 동일하다. revision2는 긴 pipeline을 줄 연속으로 정리한 제3자 편집이며 원 데이터 결손을 메우지 않는다.',
'J3': '현재 질문 본문은 최초 revision과 바이트 동일하다. Bash판/Terminal판과 .new 설정 적용 단계는 추가되지 않았다.',
'J4': '현재 질문 본문은 revision5와 동일하다. 질문자가 Tags.Name을 Tags.Key로 정정하고 version 이외 다른 태그도 있으므로 제외식이 아니라 VolName 선택이 필요하다고 추가했다.',
}
revision_notes = {
'770D470B-094C-44A8-8293-5EB88893F4A1': '최초 질문. 두 JSON JOIN의 break 오류와 디버깅 요청; 원입력 전체/판 미제공.',
'77962A23-F898-4295-99B6-0CD81D12DEAF': '최초 질문. evtx→sed→yq→sed→jq 변환 뒤 Name/content 정리와 null 오류; 전체 envelope 결손.',
'9752BCE6-43CD-456A-8925-ED6070AAB5ED': '제3자가 긴 pipeline을 backslash 줄 연속으로만 정리한다. 필드 구조·조건을 새로 제공하지 않는다.',
'C0FE71BE-B69D-428D-A53F-E976CBA5F209': '최초 질문. jq1.7/Ubuntu24.04.2/WSL2와 색 스키마·설정 JSON, Bash 변수 전달 오류를 제공.',
'5C479B29-6078-4E9A-94FE-5EAFC91A3B9C': '최초 질문. prose Tags.name/VolName와 코드 Key=Name 불일치, Iops 결손·관측 null.',
'48A8D560-31D5-4B24-975C-0E55885E4ADB': '제3자가 제목·코드 형식·표기와 prose 필드 대소문자를 편집. Tags.Name/VolName 표현은 남아 있다.',
'1077FDC6-795C-48BE-9C94-3A817759FDFE': '질문자가 only get 표현을 보충. 요구나 데이터 변화는 없다.',
'5CC7382B-45C4-4D80-90F2-3A6CEC9258CC': '제3자가 같은 문장의 중복 공백을 정리. 조건 변화는 없다.',
'9D6F0AC7-7630-4A2F-9890-F26C78B073F1': '질문자가 prose를 Tags.Key=VolName으로 정정하고 다른 태그가 있으므로 version만 제외하는 방식은 부적합하다고 명시. 최초 답보다20분 앞선 후속 원뜻 교정이다.',
'CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A': '첫 답은 질문자의 자기답이다. Event[0-(Event|length)] 또는 Event[0-152]를 배열 길이 지정이라고 해석하고 오류 없이 실행됐다고 주장한다. 모든 Event를 처리했다는 출력은 없고 이후 이 진단을 바꾼다.',
'5931D56D-480F-4826-9124-71C9BDE946CB': '자기답 수정판은 한 Event가 EventData 대신 UserData를 가졌다고 밝히고 ? 선택적 접근/반복을 제안한다. 원 전체 파일/판/최종 변환 JSON은 여전히 없고 후반에는 다른 선택식의 미해결 혼란도 남긴다.',
'BCE0455B-00F3-447C-B891-B03B5B80D1EC': '뒤에 현재 채택된 답의 최초판. sed 제거와 yq XML 옵션을 제안하며 답변자가 만든 단일 Event XML과 JSON을 제시한다. 원 EVTX 전체를 검증한 기록이 아니다.',
'7AFEF78E-3B19-4DE1-8B20-FEB85A0491A7': '현재 채택 답의 수정판은 yq map/from_entries로 Data 사전을 만드는 명령·출력을 추가한다. CommandLine은 null이며 단일 Event 예제다. 전체 다중 Event/원 판/실행 로그는 없다.',
'D0B335C6-803E-4397-9B63-6FB8F341D246': '최초·현재 답이 동일하다. jq inputs로 추가 파일을 읽고 Bash의 인용된 $@를 파일 인수 목록으로 전달하는 대안이다. JSON 내용 변수 자체를 --argjson으로 전달하는 원 시도와 수단이 다르다.',
'53C19479-AE75-4E7C-B257-C76836AE1792': '최초 답은 괄호로 pipe 범위를 한정하고 from_entries.VolName 대안, 배열/객체 출력 예시를 제시한다. Iops는 null이고 사용자판·실제 AWS 호출의 확인은 없다.',
'36D141D1-35DA-4E57-A1DC-E6DBFE382ED4': '현재 답은 comma/pipe 우선순위와 원 코드의 등가 해석 설명을 보충한다. 필터·VolName 선택·null Iops 출력 예시는 최초판과 같다.',
}

def role(user, qid):
    uid = (user or {}).get('user_id')
    if uid == question_map[qid].get('owner', {}).get('user_id'):
        return 'asker'
    if uid in {a.get('owner', {}).get('user_id') for a in answers if a['question_id'] == qid}:
        return 'answerer'
    return 'third_party_editor_or_commenter'

def source(source_id, qid, rec_label, fixed_url, actor, payload, body, confirmed, limits, kind):
    rc = receipt[rec_label]
    return {'source_id': source_id, 'q_numbers': ['Q7'], 'case_id': case_ids[qid],
        'direct_url': rc['url'], 'fixed_url': fixed_url, 'checked_utc': rc['checked_utc'],
        'author_publisher': {'publisher': 'Stack Overflow / Stack Exchange API', 'actor': actor,
                             'role': role(actor, qid), 'tool_maintainer_role_verified': False},
        'lineage': {'question_id': qid, 'kind': kind}, 'version': 'post-seal observation after ' + SEAL,
        'exact_section_payload': payload, 'body_chars': len(body) if body is not None else None,
        'body_sha256': sha(body) if body is not None else None,
        'transport_sha256': rc['transport_sha256'], 'confirmed': confirmed,
        'supports': '사후 행동·원뜻·역할·실행 귀속; 사전 완결 지표에는 사용 금지',
        'limits': limits, 'count_minimum': False, 'count_group': 'post_outcome',
        'duplicate_reason': '후속 원문은 신규 최초 질문/공식자료26 하한에서 제외; 같은 본문의 current/revision은 중복 별도 표기',
        'phase': 'post_seal2', 'allowed_as_initial_evidence': False}

sources = []
outcomes = []
for qid, cid in case_ids.items():
    q = question_map[qid]
    cutoff = q['creation_date'] + 30 * 86400
    ars = sorted([a for a in answers if a['question_id'] == qid], key=lambda a: (a['creation_date'], a['answer_id']))
    pids = [qid] + [a['answer_id'] for a in ars]
    rvs = sorted([r for r in revisions if r['post_id'] in pids], key=lambda r: (r['creation_date'], r.get('revision_number', 0), r['revision_guid']))
    cms = sorted([c for c in comments if c['post_id'] in pids], key=lambda c: (c['creation_date'], c['comment_id']))
    qr = sorted([r for r in rvs if r['post_id'] == qid and 'body' in r], key=lambda r: (r['creation_date'], r.get('revision_number', 0)))
    qsid = 'POST-' + cid + '-QCUR'
    sources.append(source(qsid, qid, 'questions-1', 'https://stackoverflow.com/questions/' + str(qid),
        q.get('owner'), 'question_id=' + str(qid) + '; body plus current accepted_answer_id metadata', q['body'],
        question_notes[cid] + ' 현재 accepted_answer_id=' + str(q.get('accepted_answer_id')) + '.',
        ['채택 시각·과거 채택 변경은 이 endpoint로 확인되지 않음', '현재 보이는 질문·답만 포함하며 삭제/비공개 기록은 미확인',
         '현재 본문은 마지막 body-bearing revision과 SHA-256 동일; 채택 metadata는 해당 revision에 고정된 값이 아님'], 'current_question'))
    answer_records = []
    for a in ars:
        body_r = sorted([r for r in rvs if r['post_id'] == a['answer_id'] and 'body' in r], key=lambda r: (r['creation_date'], r.get('revision_number', 0)))
        sid = 'POST-' + cid + '-ACUR-' + str(a['answer_id'])
        summary = revision_notes[body_r[-1]['revision_guid']]
        sources.append(source(sid, qid, 'answers-1', 'https://stackoverflow.com/a/' + str(a['answer_id']),
            a.get('owner'), 'answer_id=' + str(a['answer_id']) + '; current body/is_accepted', a['body'],
            summary + ' 현재 is_accepted=' + str(a.get('is_accepted')) + '.',
            ['현재 본문은 마지막 body-bearing revision과 동일하므로 중복 원문', '표시된 출력만으로 실제 동일판/입력 실행을 확인하지 않음', '답변자의 도구 유지관리자 지위는 확인하지 않음'], 'current_answer'))
        answer_records.append({'answer_id': a['answer_id'], 'author': a.get('owner'), 'role': role(a.get('owner'), qid),
            'created_utc': iso(a['creation_date']), 'within_30_days': a['creation_date'] <= cutoff,
            'is_accepted_current': a.get('is_accepted', False), 'first_preserved_revision': body_r[0]['revision_guid'],
            'first_revision_matches_creation_timestamp': body_r[0]['creation_date'] == a['creation_date'],
            'current_body_revision': body_r[-1]['revision_guid'], 'current_equals_last_body_revision': body_r[-1]['body'] == a['body'],
            'current_source_id': sid, 'earliest_source_id': 'POST-REV-' + body_r[0]['revision_guid'],
            'current_summary': summary, 'exact_same_version_input_output_execution_confirmed': False})
    revision_records = []
    for r in rvs:
        guid = r['revision_guid']
        sid = 'POST-REV-' + guid
        body = r.get('body')
        note = revision_notes.get(guid, '선택한 API 필터에서 body가 없는 revision metadata. body 변경·투표 종류·채택 시각을 임의 해석하지 않음.')
        payload = 'post_id=' + str(r['post_id']) + '; revision_guid=' + guid + '; '
        payload += 'body Unicode half-open [0,' + str(len(body)) + ')' if body is not None else 'body-absent metadata only'
        sr = source(sid, qid, 'revisions-1', 'https://stackoverflow.com/revisions/' + guid + '/view-source', r.get('user'), payload, body, note,
            ['최초 보존 revision을 실제 최초 삭제 전 상태라고 보증하지 않음', 'body 없는 항목은 선택필터가 보여준 metadata만 확인',
             '원 질문의 R0나 동일 current body는 이미 읽은 원문의 재열람이며 추가 최소자료로 세지 않음'], 'post_revision')
        sr['event_utc'] = iso(r['creation_date'])
        sr['revision_number'] = r.get('revision_number')
        sr['payload_sha256'] = sha(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
        sources.append(sr)
        revision_records.append({'post_id': r['post_id'], 'revision_guid': guid, 'revision_number': r.get('revision_number'),
            'revision_type': r.get('revision_type'), 'created_utc': iso(r['creation_date']), 'has_body': body is not None,
            'author': r.get('user'), 'role': role(r.get('user'), qid), 'within_30_days': r['creation_date'] <= cutoff,
            'source_id': sid, 'summary': note})
    comment_records = []
    for c in cms:
        note, claim = comment_notes[c['comment_id']]
        sid = 'POST-COMMENT-' + str(c['comment_id'])
        url = c.get('link') or 'https://stackoverflow.com/questions/' + str(qid) + '#comment' + str(c['comment_id']) + '_' + str(c['post_id'])
        sr = source(sid, qid, 'comments-1', url, c.get('owner'), 'comment_id=' + str(c['comment_id']) + '; post_id=' + str(c['post_id']) + '; body [0,' + str(len(c['body'])) + ')',
            c['body'], note, ['삭제 댓글·과거 댓글 수정 이력은 API 현재 목록만으로 복원되지 않음', '자기보고와 실제 원실행 로그를 구분', '링크된 demo/옛 질문은 열거나 실행하지 않음'], 'comment')
        sr['event_utc'] = iso(c['creation_date'])
        sources.append(sr)
        comment_records.append({'comment_id': c['comment_id'], 'post_id': c['post_id'], 'url': url,
            'author': c.get('owner'), 'role': role(c.get('owner'), qid), 'created_utc': iso(c['creation_date']),
            'within_30_days': c['creation_date'] <= cutoff, 'claim_type': claim, 'summary': note, 'source_id': sid,
            'body_sha256': sha(c['body'])})
    ask_comments = [c for c in comment_records if c['role'] == 'asker' and c['within_30_days']]
    ask_answers = [a for a in answer_records if a['role'] == 'asker' and a['within_30_days']]
    ask_q_edits = [r for r in revision_records if r['post_id'] == qid and r['role'] == 'asker' and r['within_30_days'] and r.get('revision_number', 0) and r['revision_number'] > 1]
    outcomes.append({'schema': 'af-res-100-post-outcome-jq-v1', 'case_id': cid, 'question_id': qid,
        'seal2_sha': SEAL, 'initial_judgments_changed': False, 'first_post_outcome_access_utc': first_access,
        'question_created_utc': iso(q['creation_date']), 'asker_followup_cutoff_utc_inclusive': iso(cutoff),
        'asker': q.get('owner'), 'tool_maintainer_role_verified_for_any_person': False,
        'current_accepted_answer_id': q.get('accepted_answer_id'), 'acceptance_observed_utc': receipt['questions-1']['checked_utc'],
        'acceptance_event_time': 'unknown; current metadata is not a dated acceptance history',
        'first_visible_answer_id': ars[0]['answer_id'] if ars else None,
        'first_visible_answer_missing_reason': None if ars else 'API returned zero visible answers; deleted/private answers cannot be ruled out',
        'question_current_source_id': qsid, 'question_current_summary': question_notes[cid],
        'answers': answer_records, 'revisions': revision_records, 'comments': comment_records,
        'asker_comment_within30d': bool(ask_comments), 'asker_comment_count_within30d': len(ask_comments),
        'asker_self_answer_within30d': bool(ask_answers), 'asker_question_edit_within30d': bool(ask_q_edits),
        'asker_any_followup_within30d': bool(ask_comments or ask_answers or ask_q_edits),
        'strict_same_version_input_output_execution_confirmed': False,
        'history_completeness': 'Only API-visible public posts/revisions/comments; deletion, prior acceptance times and edited/deleted comment history remain unknown.'})

analyses = {
'J1': {'execution_attribution': '질문자 실패 자기보고: inputs[]는 clean exit를 주지만 JOIN 목적을 이루지 못했다. 원판·두 전체파일·정확 출력 미확인.',
       'same_version_input_output': {'version': 'unknown', 'input': 'partial original file2 excerpt; full file1/file2 absent', 'output': 'asker reports missing JOIN; no exact final JSON'},
       'postseal_sensitivity': '오류 제거를 성공으로 삼으면 질문자의 명시 반박과 충돌한다. 사전 주 조건인 디버깅 다음 단계와 최종 JOIN 성공을 계속 분리한다.',
       'failure_condition': '원 두 파일의 소비 순서·중간값을 확인하지 않고 input을 inputs로 바꿔 오류만 없애면 JOIN 자체를 놓칠 수 있다.'},
'J2': {'execution_attribution': '첫 자기답의 성공은 나중에 다른 원인 설명으로 수정됐다. 수정 자기답도 원판·전체 Security.json·최종 변환 JSON 없이 진단/부분 처리 자기보고다. 현재 채택 yq 답은 답변자의 단일 Event XML 예제 출력이며 원 evtx 파이프라인 검증이 아니다.',
       'same_version_input_output': {'version': 'all actual tool versions unknown', 'input': 'asker reports additional UserData event absent from R0; accepted answer uses author-created single-Event XML', 'output': 'accepted-answer example Data dictionary and null CommandLine; no asker full transformed file'},
       'postseal_sensitivity': '사후 드러난 EventData 자체 결손까지 전체 이벤트 요구에 포함하면 content만 검사하는 처리는 충분하지 않을 수 있다. 최초 자기답의 Event[0-(length)]는 길이 지정 반복이 아니라 음수 단일 인덱스라는 정적 해석(jq 고정 매뉴얼 Array Index/Array Slice); 실행은 하지 않았다.',
       'failure_condition': 'EventData가 없는 UserData 이벤트를 content 결손과 혼동하거나 단일 인덱스의 무오류 실행을 전체 이벤트 변환으로 세면 안 된다.'},
'J3': {'execution_attribution': '질문자는 원 설명에 감사한 뒤 별도 답의 $@를 JSON 내용으로 바꿔 실패했다고 보고했다. 답변자가 파일 인수 목록이라고 설명한 후 질문자는 추가 JSON 파일1개에서 성공했다고 보고했다. 최종 파일·argv·동일판 기록이 없어 엄격 실행 확인은 아니다.',
       'same_version_input_output': {'version': 'R0 says jq1.7/Ubuntu24.04.2/WSL2; later success does not log versions', 'input': 'same thread, one additional colorscheme JSON file self-reported; exact executed bytes absent', 'output': 'success/same-as-$1 self-report; no resulting settings.json bytes'},
       'postseal_sensitivity': '사전 본문순서 규칙이 고른 출력 소비자 Windows Terminal과 실제 후속이 설명하는 Bash argv 경계가 다르다. Bash5.2 보조문서로 사후 반환은 개선할 수 있지만 미등록 Bash를 B에 소급 넣거나 초기 승패를 바꾸지 않는다.',
       'failure_condition': '파일명 인수인 "$@" 자리에 JSON 내용 문자열을 넣으면 jq는 이를 파일명으로 해석한다; 반환 설명에서 파일명과 JSON 내용의 계약을 구분해야 한다.'},
'J4': {'execution_attribution': '현재 채택과 답변자의 명령/출력 예시만 확인됐다. 질문자 댓글·실행 자기보고는 없다. 질문자 revision5가 Key=VolName 의도를 분명히 한 것은 원뜻 근거이며 실행 근거가 아니다.',
       'same_version_input_output': {'version': 'jq/AWS CLI actual versions unknown', 'input': 'answer uses sample fields; original AWS response remains truncated and Iops absent', 'output': 'answerer shows array/object outputs with Iops=null; no asker reproduction'},
       'postseal_sensitivity': '질문자의 후속 Tags.Key=VolName 정정은 봉인한 주 해석을 사후 지지한다. Name이라는 failed-code 문자 그대로를 요구하는 민감도와 구별한다. 누락 Iops를 숫자로 보충하지 않는다.',
       'failure_condition': 'pipe 범위를 괄호로 묶지 않아 sibling 값까지 태그 필터로 보내거나, VolName 대신 version 제외/Name 선택으로 바꾸면 원 요구를 놓친다.'},
}
JQ_URL = 'https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml'
returned = {
'J1': [{'url': JQ_URL + '#L3238-L3304', 'section': 'input/inputs; debug/debug(msgs); input_filename/input_line_number', 'status': 'same fixed main-tool manual, return-section verification after seal'}],
'J2': [{'url': JQ_URL + '#L441-L559', 'section': 'Optional Object Identifier-Index; Array Index vs Slice; .[]?', 'also_read_section': 'from_entries L1157–1169; update assignment L3410–3431', 'status': 'same fixed main-tool manual'},
       {'url': 'https://stackoverflow.com/revisions/7AFEF78E-3B19-4DE1-8B20-FEB85A0491A7/view-source', 'section': 'yq XML prefix/content options and Data dictionary example', 'status': 'post-outcome alternate toolchain; answerer-created single Event, not original full-input execution'}],
'J3': [{'url': JQ_URL + '#L240-L263', 'section': '--arg/--argjson/--slurpfile; inputs L3249–3259; shell quoting L93–110', 'status': 'same fixed main-tool manual'},
       {'url': 'https://ftp.gnu.org/gnu/bash/bash-5.2.tar.gz', 'section': 'archive member bash-5.2/doc/bashref.texi: Single/Double Quotes L439–472; Special Parameters L1850–1870; Word Splitting L2725–2767', 'status': 'supplemental outside all initial packets; fixed prequestion Bash5.2, actual Bash version unknown'}],
'J4': [{'url': JQ_URL + '#L561-L621', 'section': 'Comma, Pipe, Parenthesis; from_entries L1157–1169', 'status': 'same fixed main-tool manual; requirements clarification remains separate'}],
}
views = {
'J1': {'reader': 'debug 절부터 두 입력의 소비 순서·중간값을 확인하고 clean exit와 성공 JOIN을 구분한다.', 'maintainer': '오류 발생 위치와 불완전 입력이 어떤 진단을 막는지 드러낸다.', 'search_editor': '단순 inputs 교체 답을 해결 완료로 요약하지 않고 입력/진단 절을 함께 표시한다.'},
'J2': {'reader': '먼저 EventData/Data envelope 결손을 구분한다. yq 대안은 원 pipeline 변경으로 명시한다.', 'maintainer': 'null content와 다른 이벤트 종류(UserData)로 인한 Data 배열 부재를 별도 실패조건으로 설명한다.', 'search_editor': '첫 자기답의 성공보고와 수정판의 원인교정을 함께 보존하며 accepted yq 예제를 원 evtx 재현으로 쓰지 않는다.'},
'J3': {'reader': '추가 파일명과 JSON 내용 변수의 계약을 먼저 구분하고 Bash $@ 절을 연다.', 'maintainer': 'argv 생성 단계에서 실패하는지 출력 설정 소비 단계에서 실패하는지 나눈다.', 'search_editor': '최초 본문에서 먼저 나온 소비 앱보다 실제 실패 경계 설명이 더 적절할 수 있으나 사후 선택임을 표시한다.'},
'J4': {'reader': '괄호/파이프 범위와 Key=VolName 선택을 읽는다. Iops null은 제공 입력의 결손으로 둔다.', 'maintainer': '키/값 원형과 태그 다중성은 유지하고 외부 API를 실행한 것처럼 쓰지 않는다.', 'search_editor': '채택 배지·답변자 출력과 질문자 원뜻 수정·실행 확인을 다른 칸에 둔다.'},
}
for o in outcomes:
    o.update(analyses[o['case_id']])
    o['returned_links'] = returned[o['case_id']]
    o['perspectives'] = views[o['case_id']]

def ranges(path, spans):
    raw = path.read_bytes(); text = raw.decode(); lines = text.splitlines(True)
    out = []
    for start, end in spans:
        a = sum(map(len, lines[:start-1])); b = sum(map(len, lines[:end]))
        out.append({'lines_inclusive': [start, end], 'chars_half_open': [a,b], 'bytes_half_open': [len(text[:a].encode()), len(text[:b].encode())]})
    return out

jr = json.loads((P / 'jq-manual-receipt.json').read_text())
sources.append({'source_id':'POST-JQ-MANUAL', 'q_numbers':['Q7'], 'case_id':['J1','J2','J3','J4'],
 'direct_url':jr['url'],'fixed_url':jr['fixed_url'],'checked_utc':jr['checked_utc'], 'author_publisher':'jqlang upstream',
 'lineage':'jq1.7.1 pinned commit71c2ab509a8628dbbad4bc7b3f98a64aa90d3297; canonical v1.7 manual',
 'version':'1.7.1','body_sha256':jr['sha256'],'exact_section_payload':ranges(C/'jq-1.7.1-manual.yml',[(87,110),(240,267),(437,519),(520,621),(1157,1193),(3231,3308),(3410,3446)]),
 'confirmed':'debug는 입력을 유지하면서 stderr 진단을 만들며 input/inputs는 소비 입력이 다르다. 선택적 접근/반복, 단일 정수 인덱스와 colon slice 차이, from_entries의 Key/Name/Value 지원, parenthesis grouping, JSON/파일 인수 옵션과 update-assignment를 확인했다.',
 'supports':'사후 반환 절 선택 및 J2 자기답의 단일 인덱스/전체반복 혼동에 대한 정적 반례',
 'limits':['실제 원사용자 환경 실행 아님','이미 사전 corpus의 같은 문서이므로 독립 신규 자료가 아님','사후 해석을 봉인 판단에 소급하지 않음'],
 'count_minimum':False,'count_group':'post_outcome_supplemental','duplicate_reason':'same frozen canonical manual; one source despite several sections/cases','phase':'post_seal2','allowed_as_initial_evidence':False})
br = json.loads((P/'bash-manual-receipt.json').read_text()); bi = json.loads((P/'bash-release-receipt.json').read_text())
sources.append({'source_id':'POST-BASH-RELEASE-INDEX','q_numbers':['Q7'],'case_id':'J3','direct_url':bi['url'],'fixed_url':None,'checked_utc':bi['checked_utc'],'author_publisher':'GNU official distribution server','lineage':'GNU Bash release archive index','version':'index snapshot at access UTC','body_sha256':bi['sha256'],'exact_section_payload':'FTP HTML L143 bash-5.2.tar.gz timestamp2022-09-26; L154 bash-5.3.tar.gz current timestamp2025-07-30','confirmed':'5.2 archive index timestamp predates J3(2025-07-23). Current5.3 archive timestamp does not alone establish availability before J3, so 5.2 was used.','supports':'supplemental manual version is conservatively prequestion','limits':['index is mutable; timestamp is artifact metadata rather than a full release-history proof','actual requester Bash version unknown'],'count_minimum':False,'count_group':'post_outcome_supplemental','duplicate_reason':'metadata only; no minimum source credit','phase':'post_seal2','allowed_as_initial_evidence':False})
sources.append({'source_id':'POST-BASH52-MANUAL','q_numbers':['Q7'],'case_id':'J3','direct_url':br['url'],'fixed_url':br['url'],'checked_utc':br['checked_utc'],'author_publisher':'GNU Bash / Free Software Foundation','lineage':'official Bash5.2 release archive member '+br['member'],'version':'5.2; requester actual Bash version unknown','archive_sha256':br['archive_sha256'],'body_sha256':br['document_sha256'],'exact_section_payload':ranges(C/'bashref-5.2.texi',[(435,474),(1824,1883),(2725,2775)]),'confirmed':'single quotes preserve literal characters; double quotes allow parameter expansion while suppressing word splitting; quoted $@ expands each positional argument separately. This explains why replacing a filename argument list with JSON content changes the jq input contract.','supports':'J3 post-outcome returned-link improvement at Bash argv boundary','limits':['outside all32 initial packets','prequestion5.2 is a comparison source, not verified requester Bash version','manual semantics and asker self-report, not a new execution measurement'],'count_minimum':False,'count_group':'post_outcome_supplemental','duplicate_reason':'one new supplemental manual; multiple read sections count once and give no26-source minimum credit','phase':'post_seal2','allowed_as_initial_evidence':False})

(P/'outcomes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in outcomes))
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
summary={'seal2_sha':SEAL,'first_outcome_access_utc':first_access,'written_utc':now,'questions':len(outcomes),
 'visible_answers':len(answers),'question_cases_with_visible_answer':sum(bool(o['answers']) for o in outcomes),
 'current_accepted_cases':sum(o['current_accepted_answer_id'] is not None for o in outcomes),
 'asker_comment_or_selfanswer_within30d_cases':sum(o['asker_comment_within30d'] or o['asker_self_answer_within30d'] for o in outcomes),
 'asker_any_followup_including_question_edits_within30d_cases':sum(o['asker_any_followup_within30d'] for o in outcomes),
 'strict_same_version_input_output_confirmed_cases':sum(o['strict_same_version_input_output_execution_confirmed'] for o in outcomes),
 'visible_revision_items':len(revisions),'body_bearing_revision_items':sum('body' in r for r in revisions),'visible_comments':len(comments),
 'post30day_comments':sum(not c['within_30_days'] for o in outcomes for c in o['comments']),
 'sources_rows':len(sources),'minimum_counted':sum(s['count_minimum'] for s in sources),'original_user_command_runs':0,'aws_calls':0,
 'notes':['No initial protocol/packet/judgment changed','API-visible histories are not proof that deleted/private records never existed','Current acceptance times unknown; votes not collected or treated as execution']}
(P/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
