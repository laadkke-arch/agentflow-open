"""Build paired counts, costs and the three required tables from sealed ledgers.

Semantic assessments are explicit independent-review inputs, not inferred from a
matching disposition string. --check compares every generated output byte.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from compile_observations import read_jsonl, rows_to_csv

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text())


def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '| ' + ' | '.join(headers) + ' |\n| ' + ' | '.join(['---'] * len(headers)) + ' |\n' + ''.join('| ' + ' | '.join(md(x) for x in row) + ' |\n' for row in rows)


def time_diff(start, end):
    return round((datetime.fromisoformat(end.replace('Z', '+00:00')) - datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds(), 3)


def overlap(exposures):
    seen = defaultdict(set)
    repeated = 0
    for e in exposures:
        key = (e['requested_url'], e.get('archive_entry'), e.get('source_blob_sha'))
        indexes = set(range(e['capture_codepoint_start'], e['capture_codepoint_end']))
        repeated += len(indexes & seen[key])
        seen[key] |= indexes
    return repeated


def build():
    packets = read_jsonl(ROOT / 'packets.jsonl')
    trails = read_jsonl(ROOT / 'trails.jsonl')
    answers = list(csv.DictReader((ROOT / 'answers.csv').open()))
    control_answers = {int(a['step']): a for a in csv.DictReader((ROOT / 'control-answers.csv').open()) if a['status'] == 'observed'}
    gold = {r['case_id']: r for r in csv.DictReader((ROOT / 'gold.csv').open())}
    reviews = load('adjudication/assessments.json')
    control_review = load('adjudication/control-assessment.json')
    control_trails = read_jsonl(ROOT / 'control-trails.jsonl')
    control_packets = read_jsonl(ROOT / 'negative-packets.jsonl')
    control_final = control_review['sessions'][0]
    finals = {r['session']: r for r in reviews['sessions']}
    stages = {(r['session'], r['step']): r for r in reviews['stages']}
    notes = load('result-notes.json')
    allocation = load('audit-sources/allocation.json')
    sources = read_jsonl(ROOT / 'sources.jsonl')
    assert len(sources) == allocation['counts']['input_ledger_rows'] == 97
    assert len({s['source_id'] for s in sources}) == 97
    assert sum(s['unique_primary'] for s in sources) == 73
    assert sum(s['allocated_required24'] for s in sources) == 21
    assert len({s['unique_work_id'] for s in sources if s['unique_primary']}) == 73
    for field in ['source_id', 'original_url', 'arrival_url', 'author_lineage', 'version_date',
                  'accessed_at_utc', 'exact_locator', 'findings', 'limitations', 'opposite_observation',
                  'unknown', 'questions', 'experiment_rows', 'unique_primary']:
        assert all(field in s for s in sources), field
    for record in allocation['input_ledgers']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    assert (ROOT / 'sources.jsonl').read_bytes() == (ROOT / 'audit-sources/sources.normalized.jsonl').read_bytes()
    assert len(answers) == 36 and len(trails) == 18
    summaries = {r['session']: r for r in load('evidence/reader-summaries.json')}
    pair_rows, case_rows = [], []
    for cid in ['G1', 'G2', 'G3', 'L1', 'L2', 'L3']:
        ps = {p['condition']: p for p in packets if p['case_id'] == cid}
        assert set(ps) == {'A', 'B'}
        ready = all(p['status'] == 'ready' for p in ps.values())
        pair = {'case_id': cid, 'layer': 'main', 'A_session': ps['A']['packet_id'],
                'B_session': ps['B']['packet_id'], 'judgeable_case': ready and gold[cid]['decision_judgeable'] == 'true',
                'historical_value_judgeable': gold[cid]['historical_value_judgeable'] == 'true',
                'A_supported_success': '', 'B_supported_success': '', 'outcome': 'incomparable',
                'A_opens': 0, 'B_opens': 0, 'A_codepoints': 0, 'B_codepoints': 0,
                'A_utf8_bytes': 0, 'B_utf8_bytes': 0, 'A_final': '', 'B_final': '',
                'same_exposed_text_and_order': '', 'same_final_label': '', 'pair_shared_codepoints': 0,
                'A_within_session_reexposed_codepoints': 0, 'B_within_session_reexposed_codepoints': 0,
                'dangerous_final_count': 0, 'justified_hold_final_count': 0, 'partial_conditional_final_count': 0,
                'B_hint_codepoints': ps['B'].get('hint_codepoints', 0),
                'B_hint_utf8_bytes': ps['B'].get('hint_utf8_bytes', 0),
                'maker_active_seconds': '', 'A_wall_seconds': '', 'B_wall_seconds': '',
                'C_session': 'r13' if cid == 'G2' else 'r14' if cid == 'L2' else '',
                'C_status': 'completed' if cid == 'G2' else 'not_recruited' if cid == 'L2' else 'not_prespecified',
                'C_opens': len(control_trails) if cid == 'G2' else 0,
                'C_codepoints': sum(t['exposed_codepoints'] for t in control_trails) if cid == 'G2' else 0,
                'C_utf8_bytes': sum(t['exposed_utf8_bytes'] for t in control_trails) if cid == 'G2' else 0,
                'C_hint_codepoints': len(control_packets[0]['hint']) if cid == 'G2' else 0,
                'C_same_length': False if cid == 'G2' else '',
                'C_supported_success': control_final['supported_success'] if cid == 'G2' else '',
                'C_final': control_final['final_disposition'] if cid == 'G2' else '',
                'C_same_exposed_text_as_B': '',
                'C_interpretation': 'hint repetition removed; preservation remains in common request' if cid == 'G2' else '',
                'navigation_status': 'not_recruited', 'next_observation': '공식 월별 index/mbox를 복원하고 고정 모집틀을 완성'}
        if ready:
            assert ps['A']['url'] == ps['B']['url']
            assert ps['A']['request'] == ps['B']['request']
            assert urlsplit(ps['A']['url']).fragment == urlsplit(ps['B']['url']).fragment
            assert ps['A']['hint'] == '' and len(ps['B']['hint']) <= 140 and '\n' not in ps['B']['hint']
            ex = {}
            for condition, packet in ps.items():
                sid = packet['packet_id']
                review = finals[sid]
                ex[condition] = sorted([t for t in trails if t['session'] == sid], key=lambda t: t['step'])
                pair[condition + '_supported_success'] = review['supported_success']
                pair[condition + '_opens'] = len(ex[condition])
                pair[condition + '_codepoints'] = sum(t['exposed_codepoints'] for t in ex[condition])
                pair[condition + '_utf8_bytes'] = sum(t['exposed_utf8_bytes'] for t in ex[condition])
                pair[condition + '_final'] = review['final_disposition']
                pair[condition + '_within_session_reexposed_codepoints'] = overlap(ex[condition])
                pair[condition + '_wall_seconds'] = time_diff(summaries[sid]['started_at_utc'], summaries[sid]['finished_at_utc'])
                pair['dangerous_final_count'] += int(review['dangerous_certainty'])
                pair['justified_hold_final_count'] += int(review['justified_hold'])
                pair['partial_conditional_final_count'] += int(review['justified_residual_withholding'])
                assert pair[condition + '_codepoints'] == review['exposed_codepoints']
            pair['same_exposed_text_and_order'] = all(a['exposed_text'] == b['exposed_text'] and a['capture_codepoint_start'] == b['capture_codepoint_start'] and a.get('archive_entry') == b.get('archive_entry') for a, b in zip(ex['A'], ex['B'])) and len(ex['A']) == len(ex['B'])
            pair['same_final_label'] = pair['A_final'] == pair['B_final']
            if cid == 'G2':
                pair['C_same_exposed_text_as_B'] = len(control_trails) == len(ex['B']) and all(a['exposed_text'] == b['exposed_text'] for a, b in zip(control_trails, ex['B']))
                assert pair['C_same_exposed_text_as_B']
            pair['pair_shared_codepoints'] = pair['A_codepoints'] if pair['same_exposed_text_and_order'] else 0
            a, b = pair['A_supported_success'], pair['B_supported_success']
            pair['outcome'] = 'both' if a and b else 'A_only' if a else 'B_only' if b else 'neither'
            pair['navigation_status'] = 'three_opens_unconfirmed' if not (a or b) else 'supported_after_navigation'
            pair['next_observation'] = notes['cases'][cid]['next']
            n = notes['cases'][cid]
            case_rows.append([cid + ' / ' + n['layer'], f"[{n['request_summary']}]({gold[cid]['request_url']}); {n['version_short']}",
                              f"A=[원 URL]({ps['A']['url']}); B=같은 URL + ‘{ps['B']['hint']}’ ({len(ps['B']['hint'])}자)",
                              n['gold_summary'] + '; ' + n['gold_locator'], n['unknown']])
        else:
            case_rows.append([cid + ' / 주·공석', '2022–2025 공식 모집틀의 순번 확정 불가',
                              'A/B 모두 미구성; 다른 사건으로 대체하지 않음', '보류 / gold 판정 분모 제외',
                              '공식 월별 index·mbox 접근 결손; 존재하는 요청 수 자체 미확인'])
        pair_rows.append(pair)
    totals = Counter(p['outcome'] for p in pair_rows)
    costs = {}
    for c in ['A', 'B']:
        ps = [p for p in packets if p['condition'] == c and p['status'] == 'ready']
        ts = [t for t in trails if t['condition'] == c]
        costs[c] = {'packets': len(ps), 'opens': len(ts),
                    'body_codepoints': sum(t['exposed_codepoints'] for t in ts),
                    'body_utf8_bytes': sum(t['exposed_utf8_bytes'] for t in ts),
                    'common_request_codepoints': sum(p['common_request_codepoints'] for p in ps),
                    'common_request_utf8_bytes': sum(p['common_request_utf8_bytes'] for p in ps),
                    'url_codepoints': sum(p['url_codepoints'] for p in ps),
                    'url_utf8_bytes': sum(p['url_utf8_bytes'] for p in ps),
                    'hint_codepoints': sum(p['hint_codepoints'] for p in ps),
                    'hint_utf8_bytes': sum(p['hint_utf8_bytes'] for p in ps),
                    'active_authoring_seconds': None, 'active_reading_seconds': None,
                    'reader_wall_seconds_sum': round(sum(p[c + '_wall_seconds'] for p in pair_rows if p['judgeable_case']), 3)}
    metrics = {'task_id': 'AF-RES-112', 'status': 'PARTIAL',
               'main': {**load('evidence/observation-counts.json'), 'planned_unique_cases': 6,
                        'recruited_unique_cases': 3, 'conditional_documentary_judgeable_cases': 3,
                        'historical_value_judgeable_cases': 0, 'historical_accuracy': None,
                        'pair_outcomes': {k: totals.get(k, 0) for k in ['A_only','B_only','both','neither','incomparable']},
                        'same_exposure_pairs': sum(p['same_exposed_text_and_order'] is True for p in pair_rows),
                        'same_final_label_pairs': sum(p['same_final_label'] is True for p in pair_rows),
                        'grade_label_match_not_success': reviews['aggregate']['final_grade_label_matches'],
                        'supported_success_sessions': sum(r['supported_success'] for r in finals.values()),
                        'dangerous_certainty_sessions': sum(r['dangerous_certainty'] for r in finals.values()),
                        'justified_holds_sessions': sum(r['justified_hold'] for r in finals.values()),
                        'limited_conditionals_with_unknowns': sum(r['justified_residual_withholding'] for r in finals.values()),
                        'partial_reconstruction_stages': sum(r['exact_partial_reconstruction'] for r in stages.values()),
                        'stage_dispositions': dict(Counter(r['disposition'] for r in stages.values())),
                        'within_reader_reexposed_codepoints': sum(p['A_within_session_reexposed_codepoints'] + p['B_within_session_reexposed_codepoints'] for p in pair_rows),
                        'between_A_B_repeated_codepoints': sum(p['pair_shared_codepoints'] for p in pair_rows),
                        'failed_opens': sum(t['error'] is not None for t in trails)},
               'source_counts': allocation['counts'], 'source_quota_buckets': allocation['buckets'],
               'costs': costs, 'control': {**load('evidence/control-counts.json'), **control_review['aggregate'],
                                          'same_exposed_text_as_main_G2_B': True,
                                          'intervention': '18 codepoints deleted from B hint, preservation still in common request',
                                          'same_length': False},
               'provenance': {'independent_ai_main_contexts': 6, 'independent_ai_control_contexts': 1,
                              'human_recipients': 0, 'os_isolation': False,
                              'configured_model': 'inherited GPT-6 Astra Pro; exact provider runtime/seed unavailable',
                              'source_rows_with_null_gold_open_time': sum(s['source_id'].startswith('GOLD:') and s['accessed_at_utc'] is None for s in sources),
                              'first_gold_read_before_remote_input_seal': True,
                              'all_packets_and_gold_committed_before_main_reads': True,
                              'main_reader_seal_before_gold_open_by_root': True,
                              'main_text_unchanged_after_transport_metadata_redaction': True},
               'interpretation': 'Descriptive observed counts only. No population rate, long-term time saving, causal B benefit, or historical value accuracy is estimated.'}
    assert metrics['main']['pair_outcomes'] == {'A_only': 0, 'B_only': 0, 'both': 0, 'neither': 3, 'incomparable': 3}
    assert metrics['main']['main_total_exposed_codepoints'] == 14498
    assert metrics['main']['main_total_exposed_utf8_bytes'] == 15010
    assert metrics['main']['within_reader_reexposed_codepoints'] == 0
    stage_rows = []
    for answer in answers:
        sid, step, cid = answer['session'], int(answer['step']), answer['case_id']
        if answer['status'] != 'observed':
            if step == 1:
                stage_rows.append([f"{cid}/{answer['condition']} ({sid}) / 1–3 미실행", '도착·본문 없음', '공석 / 판단 없음', '수신자 미생성; 보류를 관측한 것으로 세지 않음', '0회·0자·0B'])
            continue
        t = next(x for x in trails if x['session'] == sid and x['step'] == step)
        review = stages[(sid, step)]
        start, end = t['source_view_start'], t['source_view_end']
        locator = f"[{t['capture_codepoint_start']},{t['capture_codepoint_end']})자; L{start['line']}:{start['column']}–L{end['line']}:{end['column']}"
        dest = f"[{t.get('archive_entry') or '도착 URL'}]({t['arrival_url']})"
        if not t['http_final_url_observed']:
            dest = f"[connector 원문주소]({t['arrival_url']}); [전송 요청]({t['transport_url']}); HTTP 최종 도착은 미노출"
        if t.get('archive_entry'):
            dest += ' / ZIP member `' + t['archive_entry'] + '`'
        dest += '; fragment=' + (t['fragment'] or '없음') + '; ' + locator
        stage_rows.append([f"{cid}/{answer['condition']} ({sid}) / {step}", dest,
                           review['disposition'] + '; 독자 반대 가능성: ' + answer['counterexample'],
                           notes['cases'][cid]['stages'][str(step)] + '; 전체 필수조건 충분=아니오',
                           f"누적 {step}회 / {t['cumulative_codepoints']}자 / {t['cumulative_utf8_bytes']}B"])
    for t in control_trails:
        stage_rows.append([f"G2/C (r13, 보조) / {t['step']}",
                           f"[도착 URL]({t['arrival_url']}); {t.get('archive_entry') or 'ZIP 목록'}; [{t['capture_codepoint_start']},{t['capture_codepoint_end']})자; fragment 없음",
                           control_answers[t['step']]['disposition'] + '; 독자 반대 가능성: ' + control_answers[t['step']]['counterexample'],
                           notes['cases']['G2']['stages'][str(t['step'])] + '; 전체 근거 불충분',
                           f"누적 {t['step']}회 / {t['cumulative_codepoints']}자 / {t['cumulative_utf8_bytes']}B"])
    stage_rows.append(['L2/C (r14, 보조) / 1–3 미실행', '없음', '공석', '미관측', '0회·0자·0B'])
    outcome_ko = {'neither': '어느 쪽도 1', 'incomparable': '비교불가 1', 'A_only': 'A만 1', 'B_only': 'B만 1', 'both': '양쪽 1'}
    pair_table_rows = [[p['case_id'] + f" / 조건 분모 {int(p['judgeable_case'])}; 역사값 {int(p['historical_value_judgeable'])}",
                        outcome_ko[p['outcome']],
                        f"위험 확정 {p['dangerous_final_count']}; 명시적 정당 보류 {p['justified_hold_final_count']}; 미확인 남긴 조건부 {p['partial_conditional_final_count']}",
                        f"B 추가 {p['B_hint_codepoints']}자·{p['B_hint_utf8_bytes']}B; 능동 제작시간 미계측" if p['judgeable_case'] else '미구성',
                        p['next_observation']] for p in pair_rows]
    pair_table_rows.append(['주 계획6 / 조건 분모3 / 역사값 분모0', 'A만0 · B만0 · 양쪽0 · 어느 쪽도3 · 비교불가3',
                            '수신6: 위험0 · 정당 보류2 · 제한적 조건부4', f"B 추가 합{costs['B']['hint_codepoints']}자·{costs['B']['hint_utf8_bytes']}B; 시간효과 미추정", 'LilyPond 모집틀 복원, 역사판 실행, 별도 사전등록 반복'])
    pair_table_rows.append(['보조 G2 1 / L2 공석1; 주 분모 미산입', 'C와 A/B 노출·최종 보류 동일', 'C 위험0 · 정당 보류1', 'C56자·122B; B에서18자 삭제, 길이 비일치', '공통 요청에도 남은 조건을 고려해 반복 강조 삭제 효과로만 해석'])
    tables = '## 표 1. 사건·층 / 원 요청·판 / 링크와 한 줄 / 기준·출처 절 / 모르는 점\n\n' + table(['사건·층','원 요청·판','링크와 한 줄','기준·출처 절','모르는 점'], case_rows)
    tables += '\n## 표 2. 사건·방식·읽기 횟수 / 실제 도착·노출 / 판정·반례 / 정확 절·불충분 / 비용\n\n' + table(['사건·방식·읽기 횟수','실제 도착 URL·노출 범위','판정·반례','정확 절·불충분','비용'], stage_rows)
    tables += '\n## 표 3. 고유 사건·판정 가능 분모 / 쌍 비교 / 확정·보류 / 제작 비용 / 다음 확인\n\n' + table(['고유 사건·판정 가능 분모','A만·B만·양쪽·어느 쪽도·비교불가','위험한 확정·정당 보류','꾸러미 제작 비용','다음 확인'], pair_table_rows)
    tables += '\n표의 원장은 `frame.csv`, `packets.jsonl`, `gold.csv`, `trails.jsonl`, `answers.csv`, `pairs.csv`이며 의미 판정은 `adjudication/assessments.json`에 있다. 실제 노출 문자열·좌표와 판단의 연결은 각 `readers/rXX/events/`에 보존한다. ZIP 도착 URL은 만료된 서명 쿼리만 제거한 공개 객체 주소이다. G1의 connector 원문주소와 API 전송 요청은 기록됐으나 HTTP 리다이렉트 최종 도착은 관측되지 않았다. 원 helper의 arrival_confirmed=true를 HTTP 확인으로 해석하지 않는다. `evidence/ledger-derivation.json`은 선택/이유 결합과 이 메타데이터 한정을 설명한다. 원 URL·리다이렉트·원문 해시는 유지하며 `evidence/transport-redaction.json`과 `evidence/exposure-invariance.json`이 원 봉인과의 차이를 설명한다. 문자 범위는 0부터 시작하는 반열린 Unicode codepoint 구간이며 바이트는 UTF-8이다. 표2의 공석 1–3 한 행은 실제 관측 3건이 아니다.\n'
    result = tables + '\n' + (ROOT / 'analysis.md').read_text().rstrip() + '\n\n## 가장 중요한 불일치·약점과 다음 조사 — 정확히 3건\n\n' + table(['불일치·약점','다음 조사·직접 열 자료','어느 관측이면 판단이 바뀌나'], notes['weaknesses'])
    return {'pairs.csv': rows_to_csv(pair_rows, list(pair_rows[0])),
            'metrics.json': json.dumps(metrics, ensure_ascii=False, indent=2) + '\n',
            'RESULT.md': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build()
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.read_text() == content, name
        else:
            path.write_text(content)
    print(json.dumps({'status': 'passed', 'mode': 'check' if args.check else 'rebuild',
                      'generated': list(outputs), 'status_is_not_research_acceptance': True}))
