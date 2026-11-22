#!/usr/bin/env python3
"""Render the required tables from preserved observations and scored rows."""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag

BASE = Path(__file__).resolve().parents[1]


def jl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(cell(v) for v in r) + ' |' for r in rows])


def main():
    questions = {r['id']: r for r in jl(BASE / 'questions.jsonl')}
    raw = jl(BASE / 'returns-raw.jsonl')
    scored = jl(BASE / 'evidence/scored-slots.jsonl')
    slots = [r for r in scored if r['variant'] == 'raw_three_candidates']
    strict = [r for r in scored if r['variant'] == 'strict_three_source_urls']
    smap = {r['slot_id']: r for r in slots}
    sources = {r['source_id']: r for r in json.loads((BASE / 'sources.json').read_text())}
    counts = json.loads((BASE / 'evidence/source-counts.json').read_text())
    discovery = json.loads((BASE / 'evidence/discovery-summary.json').read_text())
    exposure = json.loads((BASE / 'evidence/exposure-summary.json').read_text())
    budgets = json.loads((BASE / 'evidence/return-url-budget.json').read_text())
    over = {r['question_id'] + '-' + r['route'] for r in budgets if r['original_exceeded_three_urls']}
    metrics = list(csv.DictReader((BASE / 'evidence/metrics.csv').open()))
    pairs = list(csv.DictReader((BASE / 'pairs.csv').open()))
    history = [r for p in sorted((BASE / 'followups').glob('*/candidate-history.jsonl')) for r in jl(p)]
    decisions = {r['question_id']: r for p in sorted((BASE / 'followups').glob('*/decisions.jsonl')) for r in jl(p)}
    judgments = list(csv.DictReader((BASE / 'judgments.csv').open()))
    top1 = json.loads((BASE / 'evidence/literal-top1-summary.json').read_text())
    requests = list(csv.DictReader((BASE / 'search-log.csv').open()))
    open_outcomes = list(csv.DictReader((BASE / 'evidence/discovery-open-outcomes.csv').open()))

    def refs(citations, sections=False):
        seen = set(); out = []
        for c in citations:
            key = (c.get('url'), c.get('section') if sections else None)
            if not c.get('url') or key in seen:
                continue
            seen.add(key)
            label = c.get('source_id', '원문')
            if sections:
                label += ': ' + c.get('section', '절 미확인')
            out.append(f'[{label}]({c["url"]})')
        return '; '.join(out) or '미확인: 직접 인용 없음'

    short_purpose = {
        'Q01': 'Parquet 가변길이 열을 64비트 offset으로 읽고 Java에서 사용',
        'Q02': '호출자 downcast 없이 Array 인덱스의 공통 값 읽기',
        'Q03': '무작위 표와 ORC 왕복 검증의 독립 기대값 변환',
        'Q04': 'typed buffer·중첩 배열·FFI를 포함한 공개 안전성 재설계',
        'Q05': '환경별 위치가 바뀌는 로컬 의존 경로의 이름 기반 해석',
        'Q06': '컴파일 안에서 경로를 지우되 사용자 remap 우선순위 보존',
        'Q07': '비공개 패키지 index·API·download 인증 및 redirect 경계',
        'Q08': '버전별 추가 전용 feature 이행과 생성 결과의 재이행 방지',
        'Q09': '첫 실행 전에 출력 구독 준비를 확인',
        'Q10': '프로세스가 포트를 확보한 뒤 주소 회신·후속 연결까지',
        'Q11': '코드 문법과 분리된 셀 metadata를 실행 주체에게 전달',
        'Q12': '조합별 명세 복제 없이 입력·검증·인자화·실행',
    }
    table1 = []
    for qid, q in questions.items():
        route_cells = []
        for route in ('G', 'R'):
            rows = sorted([r for r in raw if r['question_id'] == qid and r['route'] == route], key=lambda r: r['rank'])
            parts = []
            for r in rows:
                if not r.get('candidate_id'):
                    parts.append(f'{r["rank"]}. 빈 슬롯 — {r.get("empty_reason", "해당 경로의 반환 후보 부족")}')
                else:
                    parts.append(f'{r["rank"]}. {r["candidate_id"]} {r["target_name"]} ({refs(r.get("returned_citations", []))})')
            if qid + '-' + route in over:
                parts.append('† 원 실행 3 URL 초과; 사후 제한판 별도')
            route_cells.append(' / '.join(parts))
        known = ', '.join(q['known_names'])
        new_count = {route: sum(r['valid_current_new_target'] for r in slots if r['question_id'] == qid and r['route'] == route) for route in ('G', 'R')}
        aux = {route: sum(r['valid_current_known_new_use'] for r in slots if r['question_id'] == qid and r['route'] == route) for route in ('G', 'R')}
        table1.append([qid + ' · ' + ('전체' if q['scope'] == 'whole' else '부분'),
                       f'[{short_purpose[qid]}]({q["initial_url"]}); 최초 명시: {known}',
                       *route_cells, f'새 대상 G{new_count["G"]}/3·R{new_count["R"]}/3; 기지 호스트 새 부품 G{aux["G"]}·R{aux["R"]}',
                       '무(양쪽 신규 완결 0); 당시 신규 완결 0. 미확인을 부재로 판정하지 않음' + ('; 현재 새 부품 보조 지표는 G 승' if aux['G'] > aux['R'] else '')])

    example_ids = ['Q01-G-1', 'Q01-G-3', 'Q01-R-3', 'Q02-G-1', 'Q02-G-3',
                   'Q03-R-1', 'Q04-G-2', 'Q04-G-3', 'Q05-R-2', 'Q06-G-2',
                   'Q07-G-1', 'Q07-R-3', 'Q08-R-1', 'Q08-R-3',
                   'Q09-R-1', 'Q09-R-2', 'Q10-R-1', 'Q11-G-1', 'Q12-G-3', 'Q12-R-1']
    table2 = []
    for sid in example_ids:
        r = smap[sid]; q = questions[r['question_id']]
        js = [j for j in judgments if j['blind_key'] == r['blind_key'] and j['package_key'] == r['package_key']]
        proof = '; '.join(f'{j["condition_id"]} 열{int(j["original_opened_support"] == "True")}/인용{int(j["original_cited_support"] == "True")}' for j in js)
        reasons = '; '.join(j['condition_id'] + ': ' + j['reason'] for j in js if j['provider_status'] != 'support')
        if not reasons:
            reasons = '현재 제안 사용 경계에서 필수 조건의 원 인용 묶음 완결. 실제 통합 실행은 미실시.'
        if sid == 'Q04-G-2':
            reasons += ' 사후 3 URL판은 README를 잃어 M3 열1/인용0; 원 반환 자체의 누락이 아님.'
        d = decisions.get(r['question_id'], {})
        choice = d.get('decision_status', '미확인: 후속 기록 미합류')
        table2.append([f'{r["candidate_id"]} · {r["route"]}{r["original_rank"]} · {r["blind_key"]}',
                       r['proposed_use'],
                       '; '.join(c['id'] + ': ' + c['predicate'] for c in q['mandatory_predicates']) + f'; 최초 {q["date"]}; 당시 {r["historical_availability"]}; 관측판 {r["current_version"]}',
                       refs(r['original_returned_citations'], sections=True), proof,
                       reasons + '; 원 질문의 제안 상태: ' + choice + ' (이 후보의 채택을 뜻하지 않음)'])
    table2.append(['전체 분모', '원 72슬롯/반환 합집합 66후보 + 열람 후 미반환 27후보 = 가린 93키',
                   '104 인용 묶음 × 각 최초 필수 조건 = 337 조건행',
                   '[candidates.csv](candidates.csv), [judgments.csv](judgments.csv), [후속 기록](followups/)',
                   '공급자·질문자·연구자 열 분리; 열/인용 두 conjunction 별도 계산',
                   '예시 외 전체 행·근접 오답·미확인은 CSV/JSONL에 보존'])

    cost_by_route = {}
    for route in ('G', 'R'):
        rr = [r for r in requests if r['route'] == route]
        cost_by_route[route] = {
            'search_requests': sum(r['event_type'] == 'search_request' for r in rr),
            'provided_results': sum(r['event_type'] == 'search_result' for r in rr),
            'first_opens': sum(r['event_type'] == 'open_attempt' for r in rr),
            'retries': sum(r['event_type'] == 'retry' for r in rr),
            'section_reads': sum(r['event_type'] == 'same_original_section_read' for r in rr),
            'normalized_failure_true_only_not_total': sum(r['event_type'] in ('open_attempt','retry','same_original_section_read') and r['failure_reported'].lower() == 'true' for r in rr),
            'receipt_audited_access_failures': sum(r['outcome'] == 'access_failure' for r in open_outcomes if r['route'] == route),
            'receipt_audited_summary_only': sum(r['outcome'] == 'summary_only' for r in open_outcomes if r['route'] == route),
            'search_wall_ms': sum(float(r['wall_ms'] or 0) for r in rr if r['event_type'] == 'search_request'),
            'open_wall_ms': sum(float(r['wall_ms'] or 0) for r in rr if r['event_type'] in ('open_attempt','retry','same_original_section_read')),
        }
    table3 = []
    labels = {'raw_three_candidates': '원 반환', 'strict_three_source_urls': '사후 3 URL판'}
    groups = {'all': '전체', 'whole': '전체 설계', 'part': '부분 동작', 'exclude_focal_exposure': '원제안/가능 후속 노출 제외', 'exclude_metadata_and_focal': '메타데이터까지 제외', 'exclude_mask_leak_questions': '가림 단어 노출 질문 제외'}
    facts_metric_rows = []
    for m in metrics:
        # Full denominator rows plus top1-candidate and exposure sensitivities.
        if m['top_k'] == '1' and m['group'] != 'all':
            continue
        route = m['route']; k = int(m['top_k'])
        data = slots if m['variant'] == 'raw_three_candidates' else strict
        ps = [p for p in pairs if p['variant'] == m['variant']]
        common = sum(len(json.loads(p['all_returned_common_candidate_ids'])) for p in ps)
        exclusive = sum(len(json.loads(p[f'all_returned_{route}_exclusive_candidate_ids'])) for p in ps)
        identities = f'전체 반환 공통{common}·{route}독점{exclusive}' if m['group'] == 'all' and k == 3 else '전체 공통/독점은 pairs.csv'
        cost = cost_by_route[route]
        costtext = (f'질의{cost["search_requests"]}, 최초 열람{cost["first_opens"]}, 재시도{cost["retries"]}, 절 추가{cost["section_reads"]}; 제공결과{cost["provided_results"]}; 원문 접근실패{cost["receipt_audited_access_failures"]}·요약만{cost["receipt_audited_summary_only"]}; 계측 합계 검색{cost["search_wall_ms"]/1000:.3f}s·열람{cost["open_wall_ms"]/1000:.3f}s'
                    if m['variant'] == 'raw_three_candidates' and m['group'] == 'all' and k == 3 else '동일 실행의 부분집계/표시판; 비용 재가산 안 함')
        table3.append([f'{route} · {labels[m["variant"]]} · {groups[m["group"]]} · 상위{k}후보',
                       f'질문{m["question_denominator"]}; 슬롯{m["slot_denominator"]}',
                       f'신규 성공 {m["current_success_questions"]}/{m["question_denominator"]}; 유효 슬롯 {m["current_valid_slots"]}/{m["slot_denominator"]}; 검증 신규 공통/독점0; {identities}',
                       f'근접 오답{m["conflict_slots"]}; 보류{m["hold_slots"]}; 빈{m["empty_slots"]}', costtext,
                       f'기지 새 부품 현재{m["known_new_use_current_slots"]}·당시{m["known_new_use_historical_slots"]}; 당시 전체 가용성 미확인 비빈 슬롯{m["historical_unknown_nonempty_slots"]}. 상위1후보는 첫 URL과 다름'])
        facts_metric_rows.append(m)
    for route, v in top1['by_route'].items():
        table3.append([route + ' · 첫 고유 URL 하나만', f'질문{v["questions"]}; 반환 URL 최대12',
                       f'신규 성공 {v["current_new_success"]}/12; 검증 신규 공통/독점0',
                       '후보 재정렬 없음; 원래 인용했던 동일 URL의 여러 절 유지',
                       '추가 조회0; 사후 기계적 민감도',
                       f'기지 새 부품 현재{v["current_known_use_success"]}/12·당시{v["historical_known_use_success"]}/12; ' + ('Q01의 3문서 조합은 탈락하고 Q11 단일 파일은 유지' if route == 'G' else '첫 URL 제한으로 새롭게 충족하는 후보 없음')])

    table4 = [
        ['Q1 · 답을 기준으로 고르지 않은 표본, 단 한정된 원장', '[SCOPE.md](SCOPE.md) §①; [frame.csv](frame.csv); [입력 봉인](evidence/input-lock.json); [최초 원문 위치](questions.jsonl)',
         '425 메타데이터 행; Arrow/Cargo/Jupyter 각4 = 12, 전체6·부분6. 최초 원문12. 2021–2024 정렬 후 앞선 적격부터 취해 실제 사례는2021–2022에 집중.',
         'JEP72/79 최초판 복구 실패 제외; RFC3143 이미 구현된 안정화 대상 확인 후 Q08을 사전 공개 정정. 성공 사례 기준 선택하지 않음.',
         '완전 모집틀 대표성 미확인. Cargo 현재 T-cargo 라벨/Arrow 초반 월 범위의 누락 감사와 JEP66 10초 차이의 앞선 blob이 바꿀 최소 자료.'],
        ['Q2 · 동일 입력·도구의 봉인 질의 비교', '[queries.jsonl](queries.jsonl); [검색 영수증](search-log.csv); [범위 정정](SCOPE-AMENDMENTS.md)',
         '24 경로·72 고정 질의; 전 문서 입력 해시 같음; 영어·공개 웹·동일 모델·system1 동일. 질문별 G/R 선행 순서 교대. 24경로 모두5개 최초 원문 시도.',
         '원 반환 8/24 경로가 3 URL 초과. 원본 보존하고 동일 순서의3 URL판 계산. G의 추론을 금지하지 않았고 R에 후보명·정답 분야를 주지 않음.',
         '동일 세션 기억과 일반 Web Pro 제품 UI 비교는 미확인. 새 독립 문맥으로 문자 그대로3 URL을 먼저 봉인한 재실행이 필요.'],
        ['Q3 · 본 결과·실패·중복을 분모에 유지', '[search-log.csv](search-log.csv); [discovery-summary.json](evidence/discovery-summary.json); [노출 원장](evidence/exposure-events.csv)',
         '제공결과633, 최초10 이내616, 부족104슬롯/49질의, 80중복 표기. 최초 원문120·재시도7·동일 원문 절3. 원제안/가능 후속 적중21건/6질문.',
         '재작성 요약·실패 페이지는 직접 원문 최소수에서 제외. DataFusion 이름은 Array 재수출로 나왔지만 ScalarValue 다른 동작은 반환되지 않음.',
         '공개 검색엔진 전역순위·토큰·과금 미확인. 관측순위는 도구 제공순서; 검색 당시의 전체 SERP를 복원하는 자료는 없음.'],
        ['Q4 · 링크가 있어도 모든 필수 조건 인용 필요', '[judgments.csv](judgments.csv); [주 판정 봉인](evidence/primary-seal.json); [021 재검산](evidence/baseline-recount.json)',
         '93키·104묶음·337조건. 새 대상 완결 G0/36·R0/36; 알려진 호스트 새 부품 G2/36·R0/36. 원 반환 지위2충족·14충돌·53보류·3빈.',
         'Hardwood roadmap, qio 값/offset 혼동, narrow 동적 형 비목표, OGC matching/준비 주체 차이 보존. 021 Q11c 전체인용 적용 시2절 M14→13.',
         '가린 판독3키에 경로 단어 선노출; 별도 같은 모델 판독은 독립 인간 검증이 아님. 새 블라인드 판독과 실행 경계 테스트가 판단을 바꿀 자료.'],
        ['Q5 · 단어 일치와 관계 대응 구분', '[익명 관계 판독](relation-check/); [REL01–03](reviews/jupyter-by-arrow/relation-check.json); [REL04–05](reviews/cargo-by-jupyter/relation-check.json); [보조 관계](supplements/relations.json)',
         '원거리 관계 익명 점검5건; 필수 조건 전체가 충족된 신규 원거리 반환0. 도서관2·제조2 원문은 주 판정 봉인 후만 읽음; 검색 적중에0 추가.',
         '추적 관계가 있어도 새 출력의 재규칙 입력을 막지 못함; idempotent 합집합은 a→b→c 이행을 막지 않음. WIP 제한은 포트 예약을 보장하지 않음.',
         '원 분야 이름 제거는 논리 점검이지 인간 전이 성능 실험이 아님. 동일 조건의 실제 실행 trace와 도입 비용이 최소 추가 자료.'],
        ['Q6 · 처음 기록됨·이용 가능함·당사자 앎은 다름', '[후속 결정 12사례](followups/); [novelty-units.json](evidence/novelty-units.json); [candidate-history](candidates.csv)',
         f'반환 합집합 후보 {len(history)}개 당시판 대조; 후속 {len(decisions)}질문. 현재 완결 부품2건은2023/2025 기능으로2021 당시 사용 불가. 최초의 정확한 부품명 부재는 미인지 증거 아님.',
         'Q02 당대 ScalarValue 제안·질문자 동의, Q07 최종 HTTPS 요구 삭제, Q11 JEP70 미병합과 별도 ipykernel 기능을 분리.',
         '현재 문서+태그만으로 전체 당시 동작을 확인하지 못한 후보는 unknown. 사용자 사전 목록/당대 테스트/정확한 최초 branch blob이 필요한 자료.'],
        ['Q7 · 같은 상한의 주 지표에서 R 개선 관측 안 됨', '[pairs.csv](pairs.csv); [metrics.csv](evidence/metrics.csv); [literal-top1-summary](evidence/literal-top1-summary.json)',
         '주 지표 R승0·무12·G승0(양쪽 완결 신규0). 새 부품 보조 지표 G승2·무10·R승0. 첫 URL만 남기면 G의 새 부품2→1. 노출 제외6질문과 엄격4질문도 신규0:0.',
         'Q01/Q11은 현재 부품 찾기에서G만 완결; Q09/Q12는 R 관계어가 목적을 닮아도 준비 주체/전체 실행 경계 부족. 반례를 찾아 원 판정을 보존.',
         '효과 동등성·실제 인시 절감 미확인. 작은 목적표본·공유 문맥·고정 첫5원문·원 URL 예산 위반으로 일반화 불가. 별도 사용자 시간 관측이 필요.'],
    ]

    rendered = '# AF-RES-025 · 힌트 없이 찾는 설계 선례 — 실제 검색과 조건별 근거 대조\n\n'
    rendered += table(['질문 ID·전체/부분','최초 목적·이미 명시된 대안','G 상위 3개와 근거 URL','R 상위 3개와 근거 URL','근거를 완전히 인용한 신규 후보','승·무·패·미확인'], table1) + '\n\n'
    rendered += table(['후보 ID·경로·순위','해당 부분과 제안 사용','필수 조건·당시 판','조건별 근거 URL·절','연 절·인용한 절','충돌·보류·후속 선택'], table2) + '\n\n'
    rendered += table(['경로·예산·집단','질문·슬롯 분모','검증된 신규·공통·독점','근접 오답·빈 슬롯','조회·열람·비용','민감도·미확인'], table3) + '\n\n'
    rendered += table(['Q 번호·주장·적용 범위','근거 원문 URL·정확한 절 또는 실행 영수증','확인한 내용·분자·분모','반례를 찾은 곳과 결과','미확인·판단을 바꿀 최소 자료'], table4) + '\n\n'
    body = (BASE / 'analysis/interpretation.md').read_text()
    def source_link(match):
        sid = match.group(1)
        return f'[{sid}]({sources[sid]["source_url"]})' if sid in sources else match.group(0)
    body = re.sub(r'\[([A-Z]{2,3}-[A-Z]\d{2,3})\](?!\()', source_link, body)
    body = body.replace('{{COUNTED_ORIGINALS}}', str(counts['counted_unique_direct_originals']))
    body = body.replace('{{SOURCE_OBSERVATIONS}}', str(counts['observation_rows']))
    body = body.replace('{{HISTORY_COUNTS}}', json.dumps(dict(Counter(r['historical_availability'] for r in history)), ensure_ascii=False))
    rendered += body
    (BASE / 'RESULT.md').write_text(rendered.rstrip() + '\n')

    facts = {
        'table1_questions': len(table1), 'table2_example_rows': len(example_ids),
        'table2_all_condition_rows': len(judgments), 'table3_rows': len(table3), 'table4_questions': len(table4),
        'counted_originals': counts['counted_unique_direct_originals'], 'source_observations': counts['observation_rows'],
        'history_unique_candidates': len(history), 'history_status': dict(Counter(r['historical_availability'] for r in history)),
        'followup_question_events': len(decisions), 'raw_route_costs': cost_by_route,
        'table3_metrics_inputs': facts_metric_rows, 'literal_top1_route_inputs': top1['by_route'],
        'raw_distant_by_question_route': {qid + '-' + route: len({r['candidate_id'] for r in slots if r['question_id'] == qid and r['route'] == route and r['candidate_class'] == 'distant_principle'}) for qid in questions for route in ('G','R')},
        'all_primary_ties_are_no_verified_success': True,
        'rendering_is_not_new_adjudication': True,
    }
    (BASE / 'evidence/report-facts.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in facts.items() if k not in ('table3_metrics_inputs','raw_distant_by_question_route')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
