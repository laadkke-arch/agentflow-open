"""Add section anchors and inspected-attachment receipts before the T0 seal.

Reads only cached root bodies; never reads follow-up comments. Do not rerun after
the parent has sealed T0, except into a separately named correction artifact.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import datetime
import json

P = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
roots = {r['case_id']: r for r in json.loads((P / 'cache/selected-roots.json').read_text())}
initial = [json.loads(s) for s in (P / 'initial.jsonl').read_text().splitlines()]
for r in initial:
    body = roots[r['case_id']]['root_body'].splitlines()
    starts = [(i + 1, line.lstrip('#').strip()) for i, line in enumerate(body) if line.startswith('#')]
    sections = {title: {'start_line': start, 'end_line': starts[j + 1][0] - 1 if j + 1 < len(starts) else len(body)} for j, (start, title) in enumerate(starts)}
    def loc(*names):
        return [{'section': n, **sections[n]} for n in names if n in sections]
    r['field_map'] = {
        'basis': 'current-description lines, SHA256 recorded above; original edition unresolved',
        'goal': {'summary': r['original_goal'], 'locations': loc('Bug summary', 'Problem', 'Summary', 'Expected outcome', 'Suggested improvement')},
        'already_tried': {'summary': r['already_tried'], 'locations': loc('Bug summary', 'Problem', 'Code for reproduction', 'Actual outcome', 'Additional information')},
        'version_settings_input': {'summary': r['known_values'], 'locations': loc('Bug summary', 'Problem', 'Code for reproduction', 'Matplotlib Version', 'Matplotlib Backend', 'Python version', 'Operating system', 'Additional information')},
        'desired_output': {'summary': r['original_goal'], 'locations': loc('Expected outcome', 'Suggested improvement', 'Proposed fix', 'Proposed solution', 'Summary', 'Problem')},
        'preference_requirement_prohibition': {'summary': '별도 필수/선호/금지의 강도는 미확인; 명시한 출력 목적만 기록', 'locations': loc('Bug summary', 'Problem', 'Expected outcome')},
    }
    if r['case_id'] == 'M03':
        r['field_map']['preference_requirement_prohibition'] = {'summary': 'systemwide 설치 권한 없음은 제약; import 때 기억할 font directory는 요청; 어떤 현행 버전 해결책이든 허용', 'locations': [{'section': 'Problem', 'start_line': 9, 'end_line': 9}, {'section': 'Suggested improvement', 'start_line': 13, 'end_line': 13}]}
    if r['case_id'] == 'M07':
        r['field_map']['preference_requirement_prohibition'] = {'summary': '약100종 범례를3열로 나누려는 목표; 첨부는 scatterplot3열 예시이고 histplot 실행결과는 아님; 코드에는ncol=1이 남아 있음', 'locations': [{'section': 'Bug summary', 'start_line': 3, 'end_line': 3}, {'section': 'Code for reproduction', 'start_line': 13, 'end_line': 13}, {'section': 'Expected outcome', 'start_line': 28, 'end_line': 28}]}
    if r['case_id'] == 'M08':
        r['field_map']['preference_requirement_prohibition'] = {'summary': 'retina-quality는 선호; close 후 stop 및 run button 재실행은 명시 기대; Tkagg 금지라고 쓰지는 않음', 'locations': [{'section': 'Bug summary', 'start_line': 3, 'end_line': 3}, {'section': 'Expected outcome', 'start_line': 86, 'end_line': 86}]}
    r['section_mapping_utc'] = now
(P / 'initial.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in initial))

receipts = json.loads((P / 'evidence/attachment-receipts.json').read_text())
notes = {
    ('M02', 1): '확대 선택 아이콘 뒤 zoom rect 상태문자가 추가 toolbar 버튼 위에 겹친다.',
    ('M02', 2): '같은 toolbar 영역에서 상태문자가 없고 추가 버튼이 가려지지 않는 기대 예시다.',
    ('M05', 1): 'x축0–8에서 상승 선만 보이며 그 아래 hatch가 보이지 않는다.',
    ('M05', 2): '상승 선 아래 사선 교차 hatch가 전체 삼각형 영역에 보인다.',
    ('M07', 1): 'stacked histogram 오른쪽에 실질 label이 없는 작은 빈 범례만 보인다.',
    ('M07', 2): '같은 histogram에 긴 단일열 scientific-name 범례가 위쪽과 그래프를 크게 덮는다.',
    ('M07', 3): '기대 예시는 다른 scatterplot이며 scientific-name 범례3열을 보여 준다. histogram의 성공 실행을 증명하지 않는다.',
}
for rec in receipts:
    u = urlsplit(rec.get('resolved_url', rec['url']))
    rec['resolved_url'] = urlunsplit((u.scheme, u.netloc, u.path, '', ''))
    rec['resolved_url_note'] = 'temporary redirect query omitted; cite stable original attachment URL'
    n = int(str(rec['attachment']).split('-')[-1]) if not isinstance(rec['attachment'], int) else rec['attachment']
    rec['directly_viewed_utc'] = now
    rec['observed'] = notes[(rec['case_id'], n)]
    rec['limitations'] = '현재 제공되는 첨부 bytes; 최초 게시 당시 동일 버전인지 미확인. 같은 스레드 부속물로 최소 원문수에 별도 산입하지 않음.'
(P / 'evidence/attachment-receipts.json').write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + '\n')

failures = []
for r in initial:
    if r['sample'] != 'A':
        failures.append({'case_id': r['case_id'], 'url': f"https://api.github.com/repos/matplotlib/matplotlib/issues/{r['issue_number']}/comments?per_page=100", 'http_status': 403, 'failure': 'public REST shared unauthenticated rate limit; not an empty discussion', 'attempted_utc': 'exact original failure timestamp not persisted; before corresponding HTML receipt, 2026-11-22 session', 'recorded_utc': now, 'fallback_receipt': f"evidence/{r['case_id']}-html-receipt.json", 'count_minimum': False})
(P / 'evidence/rest-failures.json').write_text(json.dumps(failures, ensure_ascii=False, indent=2) + '\n')
with (P / 'T0_NOTES.md').open('a') as out:
    out.write('\n루트 첨부7개를 실제 열어 보았다. M07 기대이미지는 다른 scatterplot3열 범례이며 histogram 해결 출력으로 보지 않는다. 첨부hash와 직접 관측은 evidence/attachment-receipts.json, section별 current-body 줄 매핑은 initial.field_map에 기록했다. B REST 실패의 정확한 최초 UTC는 보존되지 않았으며 이를 이후 HTML 확인시각과 혼동하지 않는다.\n')
print('T0 section mappings, attachment inspection, 27 failure attempts recorded')
