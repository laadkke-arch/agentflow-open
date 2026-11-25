"""Project the committed observations into CSV and the two lead Markdown tables."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / 'receipts/pages'
RUNS = ROOT / 'receipts/runs'
BUCKETS = {
    'violations': 'V', 'incomplete': 'I', 'passes': 'P', 'inapplicable': 'NA',
}
FOCUS = {
    'plain': 'duplicate-id', 'active': 'duplicate-id-active',
    'aria': 'duplicate-id-aria', 'control': 'image-alt',
}
BODIES = {
    ('W20', '4.1.1'): ('Parsing', 'A · 원 요구 4조건'),
    ('W20', '1.1.1'): ('Non-text Content', 'A · 동등 목적 · Controls → Guideline 4.1'),
    ('W21', '4.1.1'): ('Success Criterion 4.1.1 Parsing', 'A · 원 요구 4조건'),
    ('W21', '1.1.1'): ('Success Criterion 1.1.1 Non-text Content', 'A · 동등 목적 · Controls → SC 4.1.2'),
    ('W22', '4.1.1'): ('Success Criterion 4.1.1 Parsing (Obsolete and removed)', '제거 표지와 이유'),
    ('W22', '1.1.1'): ('Success Criterion 1.1.1 Non-text Content', 'A · 동등 목적 · Controls → SC 4.1.2'),
}
EDITIONS = {'W20': '2.0 · 2008-12-11', 'W21': '2.1 · 2018-06-05', 'W22': '2.2 · 2023-10-05'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_csv(name, rows):
    with (ROOT / name).open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def rel(path):
    return path.relative_to(ROOT).as_posix()


def table_row(cells):
    return '| ' + ' | '.join(str(cell).replace('|', '/').replace('\n', ' ') for cell in cells) + ' |'


def project_anchors(inputs):
    rows, table = [], []
    for edition in inputs['pages']:
        sid = edition['id']
        http_path = PAGES / f'{sid}.http.json'
        http = read_json(http_path)
        for target in edition['targets']:
            fragment, sc = target['fragment'], target['sc']
            browser_path = PAGES / 'browser' / f'{sid}--{fragment}.json'
            browser = read_json(browser_path)
            parser = browser['parser']
            live = browser['live']
            heading, body = BODIES[(sid, sc)]
            proxy_headers = [b['statusLine'] for b in http['responseHeaders']]
            error = live.get('error', '').splitlines()
            row = {
                'source_id': sid, 'edition': EDITIONS[sid], 'sc': sc,
                'fragment': fragment, 'requested_url': f"{edition['url']}#{fragment}",
                'origin_http_status': http['status'] or None,
                'observed_status_lines': json.dumps(proxy_headers),
                'content_type': http['contentType'],
                'origin_response_final_url': http['finalUrl'] if http['status'] else None,
                'reported_redirects': http['redirects'] if http['status'] else None,
                'bytes': http['bytes'], 'sha256': http['sha256'],
                'id_count': parser['idCount'] if parser else None,
                'eligible_count': parser['eligibleCount'] if parser else None,
                'legacy_name_count': parser['legacyNameCount'] if parser else None,
                'other_name_count': parser['otherNameCount'] if parser else None,
                'match_data': json.dumps(parser['matches'], ensure_ascii=False) if parser else None,
                'published_body_heading': heading, 'published_body_state': body,
                'browser_status': live['loadStatus'],
                'browser_target': json.dumps(live.get('match')) if live['loadStatus'] == 'observed-html' else None,
                'browser_heading': live.get('heading'), 'browser_scroll_y_px': live.get('scrollY'),
                'browser_http_bytes_equal': browser['originBytesAgreeWithLive'],
                'browser_receipt': rel(browser_path), 'http_receipt': rel(http_path),
                'blocked_steps': ' / '.join(browser['blocked']),
                'first_browser_error_line': error[0] if error else None,
            }
            rows.append(row)
            receipt = f'[{sid} HTTP]({rel(http_path)}) · [Chromium]({rel(browser_path)})'
            if http['status']:
                http_cell = f"{http['status']} · {http['bytes']} B · `{http['sha256']}`"
            else:
                http_cell = 'CONNECT 403 · origin 상태·지문 미확인'
            if parser:
                element = parser['predictedTarget']
                element_cell = (
                    f"{element['tag']} · {element['heading']} ({parser['eligibleCount']}개)"
                    if element else '선택 대상 0개'
                )
            else:
                element_cell = f'요소 미확인 · 본문 {heading}'
            if live['loadStatus'] == 'observed-html':
                browser_cell = f"{live['match']} · scrollY {live['scrollY']} px"
            else:
                browser_cell = '미확인 · 터널 단계 실패'
            table.append((
                f"[{EDITIONS[sid]} #{fragment}]({row['requested_url']})",
                http_cell, element_cell, browser_cell, body, receipt,
            ))
    return rows, table


def outcome(raw, rid):
    return {
        name: next(entry for entry in raw[name] if entry['id'] == rid)
        for name in BUCKETS if any(entry['id'] == rid for entry in raw[name])
    }


def expectation(version, fixture, mode, rid):
    disabled = version == '4.8.0' and rid in ('duplicate-id', 'duplicate-id-active')
    if disabled and mode in ('default', 'wcag2a'):
        return set(), None, f'{mode} 미보고'
    if rid != FOCUS[fixture]:
        return None, None, '235에서 이 조합의 결과를 고정하지 않음'
    if rid == 'image-alt':
        return {'violations', 'passes'}, 'wcag111', '235 wcag111 · 사전 V/P 가설'
    if version == '4.8.0' and rid == 'duplicate-id-aria':
        return {'incomplete'}, 'wcag412', '235 incomplete · wcag412'
    return {'violations'}, 'wcag411', '235 violation · wcag411'


def project_runs(inputs):
    rows, table = [], []
    replay_path = ROOT / 'receipts/replay/comparison.json'
    replay = read_json(replay_path)['axe'] if replay_path.exists() else {}
    for build in inputs['builds']:
        version = build['version']
        for fixture in inputs['fixtures']:
            for mode in inputs['modes']:
                key = f'{version}--{fixture}--{mode}'
                path = RUNS / f'{key}.json'
                case_path = RUNS / f'{key}.case.json'
                case = read_json(case_path)
                raw = read_json(path) if case['status'] == 'observed' else None
                shown = []
                focus_counts = dict.fromkeys(BUCKETS.values(), 0)
                missing = 0
                statement = '미확인'
                for rid in inputs['ruleIds']:
                    findings = outcome(raw, rid) if raw else {}
                    tags = list(next(iter(findings.values()))['tags']) if findings else []
                    nodes = {
                        name: [node['target'] for node in result['nodes']]
                        for name, result in findings.items()
                    }
                    node_html = {
                        name: [node['html'] for node in result['nodes']]
                        for name, result in findings.items()
                    }
                    expected, expected_tag, premise = expectation(version, fixture, mode, rid)
                    if raw is None:
                        delta = '미확인'
                    elif expected is None:
                        delta = '비교 기대 없음'
                    else:
                        same = set(findings) == expected and (expected_tag is None or expected_tag in tags)
                        delta = '일치' if same else '차이'
                        if rid == 'image-alt' and same:
                            delta = 'wcag111 일치, 노드별 V/P 추가 관측'
                    if rid == FOCUS[fixture]:
                        statement = f'{premise} · {delta}'
                    for name, targets in nodes.items():
                        label = BUCKETS[name]
                        focus_counts[label] += 1
                        if targets:
                            selectors = ', '.join(' › '.join(target) for target in targets)
                            shown.append(f'{label} `{rid}` → `{selectors}`')
                    if not findings:
                        missing += 1
                        why_absent = '원인 미확인'
                        if raw and expected == set():
                            why_absent = 'enabled=false' if mode == 'default' else 'wcag2a 태그 제외'
                    else:
                        why_absent = ''
                    rows.append({
                        'run_key': key, 'version': version, 'fixture': fixture, 'mode': mode,
                        'rule_id': rid, 'kinds': '+'.join(findings) or ('not-reported' if raw else 'unobserved'),
                        'tags': json.dumps(tags), 'node_targets': json.dumps(nodes), 'node_html': json.dumps(node_html),
                        'absence_reason': why_absent,
                        'expectation': premise, 'delta': delta, 'raw_json': rel(path) if raw else '',
                        'case_json': rel(case_path),
                    })
                if mode != 'default':
                    replay_cell = '대표 범위 밖'
                elif key in replay:
                    comparison = replay[key]
                    norm = '일치' if comparison['normalizedEqual'] else '차이'
                    replay_cell = f"[정규화 {norm}](receipts/replay/comparison.json)"
                else:
                    replay_cell = '미실시 · 예정'
                if raw:
                    focused = '/'.join(str(value) for value in focus_counts.values())
                    all_counts = '/'.join(str(len(raw[name])) for name in BUCKETS)
                    classes = f'대상 {focused} · 미보고 {missing} · 전체 {all_counts}'
                    raw_link = f'[JSON]({rel(path)}) · [조건]({rel(case_path)})'
                else:
                    classes = '미확인'
                    raw_link = f'[실패]({rel(case_path)})'
                table.append((
                    f'{version} · {fixture} · {mode}', ' / '.join(shown) or '대상에서 보고 노드 0',
                    classes, replay_cell, statement, raw_link,
                ))
    return rows, table


def main():
    inputs = read_json(ROOT / 'inputs.json')
    anchor_rows, anchor_table = project_anchors(inputs)
    rules_rows, rule_table = project_runs(inputs)
    write_csv('anchors.csv', anchor_rows)
    write_csv('rules.csv', rules_rows)
    for number, labels, intro, rows in [
        (1, ['날짜판·fragment', 'HTTP·파일 지문', '실제 일치 요소·절 제목', '브라우저 도착', '본문 상태', '영수증·미확인'],
         '한 행은 W3C 최초 날짜판의 fragment 하나다. 3판×2기준=6행. 셸과 Chromium 원격 탐색을 각각 시도했다. 본문 상태는 공식 원페이지 텍스트에서 읽은 6절의 판정이다.', anchor_table),
        (2, ['axe 판·입력·모드', '실제 rule·노드', '4종 결과 분류', '동일 조건 재생', '235 기대와 차이', '원 JSON'],
         '한 행은 한 새 문서의 axe.run 호출이다. 2판×4입력×3모드=24행. V/I/P/NA는 violations/incomplete/passes/inapplicable의 규칙 항목 수 순서다. 대상은 지정 4 ID이며 전체 수에는 그 밖의 규칙이 포함된다. 한 규칙이 다른 노드의 V와 P에 함께 나올 수 있다. NA의 노드 배열은 비어 있고 미보고는 네 배열 모두에 없는 것이다. [rules.csv](rules.csv)는 호출×규칙 96행으로 태그·노드·공석을 기록한다.', rule_table),
    ]:
        print(f'# 표 {number}\n\n{intro}\n')
        print(table_row(labels))
        print(table_row(['---'] * len(labels)))
        for row in rows:
            print(table_row(row))
        if number == 1:
            print()


if __name__ == '__main__':
    main()
