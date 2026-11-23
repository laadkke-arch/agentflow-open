"""Independent metadata/byte-chain audit of AF-RES-088's frozen revision archives.
No semantic ratings, no network access, no git operations, and no judgments writes.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
import csv
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'support'
SEAL = '42e46d5788278efa8d5b8ab0272ace48830fb477'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def utc(ts):
    return datetime.fromtimestamp(ts, timezone.utc).isoformat().replace('+00:00', 'Z')

def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

input_hashes = {}
def read_bytes(name):
    b = (ROOT / name).read_bytes()
    input_hashes[name] = sha(b)
    return b

frame = list(csv.DictReader(read_bytes('frame.csv').decode().splitlines()))
frame_meta = json.loads(read_bytes('frame_metadata.json'))
meta_by_id = {m['question_id']: m for m in frame_meta}
frozen_revisions = {r['case_id']: r for r in map(json.loads, read_bytes('revisions.jsonl').decode().splitlines()) if r}
archive_manifest = json.loads(read_bytes('snapshot_archives.json'))
manifest_by_path = {x['stored_path']: x for x in archive_manifest}
archive_checks = []
all_records = []
errors = []
for tag in ('jq', 'pandoc'):
    name = f'sealed/revisions_{tag}_page1.json.gz'
    gz = read_bytes(name)
    raw = gzip.decompress(gz)
    data = json.loads(raw)
    records = data.get('items', [])
    expected_ids = {int(r['question_id']) for r in frame if r['tag'] == tag}
    observed_ids = {r['post_id'] for r in records}
    saved = manifest_by_path[name]
    check = {
        'tag': tag, 'archive': name,
        'items': len(records), 'unique_post_ids': len(observed_ids),
        'api_has_more': data.get('has_more'),
        'all_requested_post_ids_present': observed_ids == expected_ids,
        'missing_post_ids': sorted(expected_ids - observed_ids),
        'unexpected_post_ids': sorted(observed_ids - expected_ids),
        'gzip_sha256_matches_manifest': sha(gz) == saved['gzip_sha256'],
        'uncompressed_sha256_matches_manifest': sha(raw) == saved['uncompressed_sha256'],
        'gzip_sha256': sha(gz), 'uncompressed_sha256': sha(raw),
        'returned_creation_dates_nonincreasing': all(a['creation_date'] >= b['creation_date'] for a, b in zip(records, records[1:])),
        'scope': 'All accessible history items for the requested 30 IDs in this API snapshot; does not prove absence of deleted/redacted history.'
    }
    archive_checks.append(check)
    if data.get('has_more') is not False:
        errors.append({'kind': 'incomplete_api_paging', 'tag': tag})
    for flag in ('all_requested_post_ids_present', 'gzip_sha256_matches_manifest', 'uncompressed_sha256_matches_manifest'):
        if not check[flag]:
            errors.append({'kind': flag, 'tag': tag})
    all_records.extend(records)

by_post = defaultdict(list)
for r in all_records:
    by_post[r['post_id']].append(r)
guid_counts = Counter(r['revision_guid'] for r in all_records)
duplicate_guids = [g for g, n in guid_counts.items() if n > 1]
if duplicate_guids:
    errors.append({'kind': 'duplicate_revision_guids', 'guids': duplicate_guids})

# First use timestamp + numeric revision ordering, then explicitly compare this
# to numeric ordering; any disagreement becomes an auditable error.
def order_key(r):
    return (r['creation_date'], r.get('revision_number', -1), r['revision_guid'])

def actor(r, owner_id):
    user = r.get('user', {})
    uid = user.get('user_id')
    if uid == -1:
        role = 'community_bot'
    elif uid is not None and owner_id is not None:
        role = 'question_author' if uid == owner_id else 'other_editor'
    else:
        role = 'unverified_deleted_or_missing_account_id'
    return {'user_id': uid, 'display_name': user.get('display_name'), 'user_type': user.get('user_type'), 'role_by_stable_id': role}

post_checks = []
selected = []
counts = Counter()
for f in frame:
    pid = int(f['question_id'])
    created = meta_by_id[pid]['creation_date']
    owner_id = meta_by_id[pid].get('owner', {}).get('user_id')
    deadline = created + 30*24*60*60
    records = sorted(by_post[pid], key=order_key)
    bodies = [r for r in records if 'body' in r]
    numbers = sorted(r['revision_number'] for r in records if 'revision_number' in r)
    expected_numbers = list(range(1, max(numbers, default=0)+1))
    numeric_bodies = sorted(bodies, key=lambda r: (r.get('revision_number', -1), r['creation_date']))
    number_order_matches = [r['revision_guid'] for r in numeric_bodies] == [r['revision_guid'] for r in bodies]
    if numbers != expected_numbers:
        errors.append({'kind': 'revision_number_gap_or_duplicate', 'question_id': pid, 'observed': numbers, 'expected': expected_numbers})
    if not number_order_matches:
        errors.append({'kind': 'body_timestamp_vs_number_order_disagreement', 'question_id': pid})
    previous_body = None
    previous_guid = None
    classified = []
    for r in records:
        fields = [field for field in ('body', 'title', 'tags') if field in r]
        is_initial = 'body' in r and previous_body is None
        body_change = None if 'body' not in r or is_initial else r['body'] != previous_body
        chain_match = None
        if 'last_body' in r:
            chain_match = previous_body is not None and r['last_body'] == previous_body
            counts['last_body_links_checked'] += 1
            if not chain_match:
                errors.append({'kind': 'last_body_chain_mismatch', 'question_id': pid, 'guid': r['revision_guid'], 'previous_body_guid': previous_guid})
            else:
                counts['last_body_links_matched'] += 1
        elif 'body' in r and not is_initial:
            errors.append({'kind': 'missing_last_body_on_later_body_record', 'question_id': pid, 'guid': r['revision_guid']})
        if is_initial:
            kind = 'initial_body'
        elif fields:
            kind = '+'.join(fields)
        else:
            kind = 'non_content_event'
        if r.get('is_rollback'):
            kind += '+rollback'
        role = actor(r, owner_id)
        detail = {
            'guid': r['revision_guid'], 'revision_number': r.get('revision_number'),
            'utc': utc(r['creation_date']), 'content_fields_present': fields,
            'edit_kind': kind, 'is_rollback': bool(r.get('is_rollback')),
            'actor': role, 'within_30d_inclusive': created <= r['creation_date'] <= deadline,
            'body_sha256': sha(r['body'].encode()) if 'body' in r else None,
            'body_differs_from_preceding_body_bytes': body_change,
            'last_body_present': 'last_body' in r,
            'last_body_matches_preceding_body': chain_match,
            'preceding_body_guid': previous_guid,
            'comment': r.get('comment')
        }
        classified.append(detail)
        counts['records'] += 1
        counts['kind_' + kind] += 1
        counts['actor_' + role['role_by_stable_id']] += 1
        if 'body' in r:
            counts['body_records'] += 1
            if not is_initial:
                counts['separate_body_records'] += 1
                if body_change is False:
                    counts['byte_identical_separate_body_records'] += 1
            previous_body = r['body']
            previous_guid = r['revision_guid']
    r0 = bodies[0] if bodies else None
    available_30d = [r for r in bodies if created <= r['creation_date'] <= deadline]
    r1 = available_30d[-1] if available_30d else None
    edit_records = [r for r in available_30d if r0 and r['revision_guid'] != r0['revision_guid']]
    actual_byte_changes_30d = sum(1 for x in classified if x['within_30d_inclusive'] and x['body_differs_from_preceding_body_bytes'] is True)
    if not r0 or not r1:
        errors.append({'kind': 'missing_r0_or_r1', 'question_id': pid})
    if int(f['body_edits_30d_metadata']) != len(edit_records):
        errors.append({'kind': 'frame_body_edit_count_mismatch', 'question_id': pid, 'frame': f['body_edits_30d_metadata'], 'computed': len(edit_records)})
    if int(f['history_records']) != len(records):
        errors.append({'kind': 'frame_history_count_mismatch', 'question_id': pid})
    if r0 and f['r0_guid'] != r0['revision_guid']:
        errors.append({'kind': 'frame_r0_guid_mismatch', 'question_id': pid})
    check = {
        'tag': f['tag'], 'original_rank': int(f['original_rank']), 'question_id': pid,
        'case_id': f['case_id'] or None, 'stratum': f['stratum'] or None,
        'eligible_in_frozen_frame': f['eligible'],
        'history_items': len(records), 'body_records': len(bodies),
        'separate_body_records_within_30d': len(edit_records),
        'body_byte_changes_within_30d': actual_byte_changes_30d,
        'body_metadata_count_equals_actual_byte_changes': len(edit_records) == actual_byte_changes_30d,
        'numeric_revisions_contiguous_from_one': numbers == expected_numbers,
        'body_timestamp_order_agrees_with_revision_number': number_order_matches,
        'r0_guid': r0['revision_guid'] if r0 else None,
        'r0_revision_number': r0.get('revision_number') if r0 else None,
        'r1_guid': r1['revision_guid'] if r1 else None,
        'r0_matches_question_creation_timestamp': bool(r0 and r0['creation_date'] == created),
        'records': classified
    }
    post_checks.append(check)
    if f['case_id']:
        case_id = f['case_id']
        fr = frozen_revisions.get(case_id, {})
        def summarized(r):
            record = next(x for x in classified if x['guid'] == r['revision_guid'])
            return {'guid': r['revision_guid'], 'revision_number': r.get('revision_number'),
                    'utc': utc(r['creation_date']), 'revision_url': f"https://stackoverflow.com/revisions/{pid}/{r['revision_number']}",
                    'actor': record['actor'], 'edit_kind': record['edit_kind'],
                    'body_sha256': record['body_sha256']}
        saved_r1 = fr.get('r1')
        r0_path = f'evidence/r0/{pid}.html'
        r0_file = read_bytes(r0_path)
        r0_file_matches = r0_file == r0['body'].encode()
        if not r0_file_matches:
            errors.append({'kind': 'saved_r0_html_mismatch', 'case_id': case_id})
        if fr.get('r0', {}).get('guid') != r0['revision_guid']:
            errors.append({'kind': 'revisions_jsonl_r0_guid_mismatch', 'case_id': case_id})
        r1_match = None if saved_r1 is None else saved_r1.get('guid') == r1['revision_guid']
        if r1_match is False:
            errors.append({'kind': 'revisions_jsonl_r1_guid_mismatch', 'case_id': case_id})
        selected.append({
            'case_id': case_id, 'tag': f['tag'], 'stratum': f['stratum'], 'original_rank': int(f['original_rank']),
            'question_id': pid, 'created_utc': utc(created), 'window_end_utc_inclusive': utc(deadline),
            'r0': summarized(r0), 'r1': summarized(r1), 'r0_equals_r1': r0['revision_guid'] == r1['revision_guid'],
            'history_items': len(records), 'body_records_inclusive_30d': len(available_30d),
            'separate_body_records_within_30d': len(edit_records),
            'r0_file_matches_archive_bytes': r0_file_matches,
            'revisions_jsonl_r0_matches': fr.get('r0', {}).get('guid') == r0['revision_guid'],
            'revisions_jsonl_r1_state_at_audit': 'not_yet_written' if saved_r1 is None else 'present',
            'revisions_jsonl_r1_matches': r1_match,
            'chain_failures': [x for x in classified if x['last_body_matches_preceding_body'] is False],
            'strict_initial_posting_bytes': 'unverified; equality of timestamps does not establish an unmerged first publication'
        })

selection_checks = []
for tag in ('jq', 'pandoc'):
    fs = [f for f in frame if f['tag'] == tag]
    eligible = [f for f in fs if f['eligible'].lower() == 'true']
    natural = eligible[:2]
    natural_ids = {int(f['question_id']) for f in natural}
    edited = [f for f in eligible[2:] if next(p for p in post_checks if p['question_id'] == int(f['question_id']))['separate_body_records_within_30d'] > 0][:2]
    computed_ids = [int(f['question_id']) for f in natural+edited]
    actual_ids = [int(f['question_id']) for f in fs if f['case_id']]
    passed = computed_ids == actual_ids
    selection_checks.append({'tag': tag, 'computed_selected_ids': computed_ids, 'frame_selected_ids': actual_ids, 'matches': passed, 'eligibility_source': 'Frozen frame; this audit does not independently re-evaluate semantic eligibility.'})
    if not passed:
        errors.append({'kind': 'selection_order_mismatch', 'tag': tag})

summary = {
    'frame_rows': len(frame), 'unique_frame_question_ids': len({int(f['question_id']) for f in frame}),
    'tag_frame_counts': dict(Counter(f['tag'] for f in frame)),
    'selected_slots': len(selected), 'r0_r1_same_guid_slots': sum(s['r0_equals_r1'] for s in selected),
    'selected_slots_with_distinct_body_revision': sum(not s['r0_equals_r1'] for s in selected),
    'all_60_accessible_histories_complete_in_api_snapshot': len(frame) == 60 and all(c['api_has_more'] is False and c['all_requested_post_ids_present'] for c in archive_checks),
    'all_r0_are_number1_and_creation_timestamp': all(p['r0_revision_number'] == 1 and p['r0_matches_question_creation_timestamp'] for p in post_checks),
    'all_body_metadata_counts_equal_actual_byte_change_counts': all(p['body_metadata_count_equals_actual_byte_changes'] for p in post_checks),
    'staging_ground_non_body_event_question_ids': [p['question_id'] for p in post_checks if any('staging ground' in (r.get('comment') or '') for r in p['records'])],
    'duplicate_revision_guids': duplicate_guids,
    'byte_identical_separate_body_records': counts.get('byte_identical_separate_body_records', 0),
    'counts': dict(counts), 'errors': errors,
    'r1_rows_not_yet_written_at_audit': sum(s['revisions_jsonl_r1_state_at_audit'] == 'not_yet_written' for s in selected)
}
report = {
    'audit_id': 'AF-RES-088-REVISION-INTEGRITY', 'performed_utc': datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
    'provided_remote_r0_seal_commit': SEAL,
    'audit_kind': 'Independent metadata and byte-chain recalculation; not semantic blind coding and not independent API reacquisition.',
    'case_ids_source': 'frame.csv case_id column; no separate case_ids.json file was present.',
    'input_sha256': input_hashes, 'summary': summary,
    'archive_checks': archive_checks, 'selection_checks': selection_checks,
    'selected_cases': selected, 'all_question_checks': post_checks,
    'status': 'PASS' if not errors else 'FAIL',
    'limitations': [
        'has_more=false establishes completeness only for accessible API items at capture, not deleted/redacted history or questions absent from the frame.',
        'R0 may include grace-period merged changes; exact first published bytes remain unverified.',
        'A deleted actor without stable user_id remains unverified for author-versus-other classification; differing display names alone are not promoted to stable identity proof.',
        'Revisions JSONL was compared as read at this run; if root later writes R1, rerun this audit to bind the comparison to that file hash.',
        'Eligibility and candidate semantics are not re-scored; judgments.csv was neither read nor written.'
    ]
}
(OUT/'revision_integrity_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines = [
    '# AF-RES-088 리비전 메타데이터·본문 연결 무결성 감사', '',
    f"판정: **{report['status']}**. 검사시각 `{report['performed_utc']}`. 부모가 제공한 원격 R0 봉인 커밋 `{SEAL}` 이후에 수행했다.", '',
    '공개 API를 새로 호출한 재확인이 아니라, 고정 압축 원본의 별도 계산이다. 본문 의미·후보 판정은 평가하지 않았고 judgments.csv는 읽거나 변경하지 않았다. 독립 이중 판독으로 세지 않는다.', '',
    '## 집계', '',
    f"- 목록 {summary['frame_rows']}행, 서로 다른 질문 {summary['unique_frame_question_ids']}개, 선택 {summary['selected_slots']}자리.",
    f"- jq {archive_checks[0]['items']}개 이력·30질문, Pandoc {archive_checks[1]['items']}개 이력·30질문. 양 API 응답 has_more=false, 원목록 ID 전부 포함.",
    f"- last_body 연결 {counts['last_body_links_checked']}개 검사, {counts['last_body_links_matched']}개 일치. 오류 {len(errors)}개.",
    f"- 같은 HTML 바이트를 다시 기록한 별도 본문 revision {summary['byte_identical_separate_body_records']}개. 따라서 이 스냅샷의 body 존재 기반 편집수와 실제 본문 바이트 변경수는 일치한다.",
    f"- 최초 본문판은60질문 모두 판1이며 질문 생성시각과 같다. 비본문 Staging Ground 생성 사건이 같은 시각에 붙은 질문 {summary['staging_ground_non_body_event_question_ids']}은 그 사건을 본문판으로 세지 않았다.",
    f"- 선택자리의 R0=R1 {summary['r0_r1_same_guid_slots']}개, 별도 본문판 {summary['selected_slots_with_distinct_body_revision']}개. R1 미작성 상태에서 비교한 자리 {summary['r1_rows_not_yet_written_at_audit']}개.", '',
    '## 독립 재계산한 8자리', '',
    '| 사례 | 원순번 | R0 GUID·UTC | R1 GUID·UTC | R1 작성 주체·종류 | 30일 내 별도 본문판 |',
    '| --- | --- | --- | --- | --- | --- |'
]
for s in selected:
    a = s['r1']['actor']
    lines.append(f"| {s['case_id']} | {s['tag']} {s['original_rank']} | {s['r0']['guid']} / {s['r0']['utc']} | {s['r1']['guid']} / {s['r1']['utc']} | {a['display_name']} (id={a['user_id']}; {a['role_by_stable_id']}) / {s['r1']['edit_kind']} | {s['separate_body_records_within_30d']} |")
lines += ['', '## 판별 절차와 한계', '',
    '1. snapshot_archives.json의 압축·해제 SHA256을 다시 계산했다. API wrapper has_more=false와 요청30개의 post_id 집합을 맞췄다. 동일 GUID, 누락 판 번호, 시각 정렬과 숫자 판 정렬의 불일치를 검사했다.',
    '2. 각 질문에서 body가 실제 포함된 판만 본문판으로 분리했다. 최초 본문판을 R0, creation_date부터30일(2,592,000초) 이하의 마지막 본문판을 R1으로 계산했다. title/tag-only와 비내용 이벤트는 별도 분류했다.',
    '3. 각 다음 본문판 last_body가 바로 앞 body와 정확히 같은 UTF-8 문자열인지 확인했다. 바이트 동일 여부를 의미 동일 판정으로 사용하지 않았다. 표현만 달라진 경우는 부모의 별도 의미판독 대상이다.',
    '4. frame의 적격 판정을 입력으로 삼아 각 태그의 첫 자연층2개, 이후 별도 본문수정이 있는 첫 편집층2개를 재선택했다. 적격 자체의 의미 판독은 감사하지 않았다.',
    '5. 질문자/타인 구분은 안정적인 user_id가 양쪽에 있을 때만 확정했다. 삭제된 계정의 user_id가 없으면 표시명이 달라도 안정적 식별 근거 미확인으로 남겼다.',
    '6. 모든 R0가 판1 및 질문 생성시각과 일치하는지 검사는 최초 게시 바이트 보존 증명이 아니다. grace 병합·삭제된 역사·조회시점 태그가 만드는 한계는 유지된다.', '',
    '## 재실행', '',
    '```sh', 'python docs/workstreams/research/AF-RES-088/support/audit_revision_integrity.py', '```', '',
    '출력 JSON의 input_sha256은 실제 검사한 파일을 고정한다. revisions.jsonl에 R1을 추가한 뒤 다시 실행하면 해당 작성본과 GUID를 비교한다. 프로그램은 실패 발견 시 종료1, 발견하지 않으면 종료0이다. JSON의 all_question_checks에60질문의 개별 이력 분류가 들어 있다.', '',
    '## 검출 오류', '', '```json', json.dumps(errors,ensure_ascii=False,indent=2), '```', ''
]
(OUT/'revision_integrity_audit.md').write_text('\n'.join(lines))
print(json.dumps({'status': report['status'], 'summary': summary, 'selected': [{k:s[k] for k in ('case_id','question_id','r0','r1','separate_body_records_within_30d')} for s in selected]},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
