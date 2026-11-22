"""Write candid acceptance evidence with file/line locators and explicit gaps."""
from datetime import datetime, timezone
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent
counts = json.loads((P/'evidence/source-counts.json').read_text())
validation = json.loads((P/'evidence/delivery-validation.json').read_text()) if (P/'evidence/delivery-validation.json').exists() else None
verification = json.loads((P/'evidence/verification-receipt.json').read_text()) if (P/'evidence/verification-receipt.json').exists() else None
criteria = []


def ref(file, marker=None):
    lines = (P/file).read_text().splitlines()
    if marker is None:
        return {'file': file, 'start_line': 1, 'end_line': len(lines), 'selector': 'whole file; select case/source IDs as specified in criterion'}
    n = next(i for i, s in enumerate(lines, 1) if marker in s)
    return {'file': file, 'start_line': n, 'end_line': min(n+5, len(lines)), 'selector': marker}


def add(id, question_ids, mandatory, met, numerator, denominator, unit, reason, evidence, missing='', next_first_action=''):
    criteria.append({'id': id, 'question_ids': question_ids, 'mandatory': mandatory, 'met': bool(met),
                     'numerator': numerator, 'denominator': denominator, 'unit': unit, 'reason': reason,
                     'evidence': evidence, 'missing_reason': missing, 'next_first_action': next_first_action})


add('manifest_and_fixed_dependencies', ['Q1'], True, True, 2, 2, 'fixed predecessor SHAs',
    '계획 SHA와 실제 배정 SHA·환경·제공 모델표시를 분리하고 지정 선행 두 SHA를 고정했다.',
    [ref('manifest.json'), ref('evidence/start-receipt.json')])
add('preregistered_consumer_ledgers', ['Q1'], True, True, 2, 2, 'ledgers with query/date/order/cap/fallback',
    '외부 요구 열람 전 원격 규칙 커밋에 원장·검색·기간·생성시각/번호·최초30·상한·대체를 명시했다.',
    [ref('SCOPE.md', '## 1.'), ref('evidence/commits.jsonl')])
add('consumer_frame_and_sealed_requirements', ['Q1'], True, True, 8, 8, 'selected original requests',
    '두 경로 각30노출, 각4선정. 8개 요구·행동·판·허용 대안을 공급자 자료 전에 봉인했고 해시를 보존했다. name_only는0이다.',
    [ref('frame.csv'), ref('evidence/gdal/requirements-G.json'), ref('evidence/sphinx/requirements-S.json'), ref('evidence/pool-freeze.json')])
add('raw_href_prospective_sampling', ['Q2'], True, False, '미확인', 8, 'strict prospective natural-URL pools',
    '요구 봉인과 이후 같은 풀 비교는 유지했으나 자연 href 취득·세부 seed 순회의 완전 전향 등록을 충족하지 못했다.',
    [ref('evidence/sphinx/NOTES.md'), ref('evidence/gdal/NOTES-G.md','## 2.'), ref('RESULT.md','엄격한 자연 링크 실험')],
    'S는 명명 항목으로 만든 #L 링크, S1 seed순서 사전 고정 부재. G HFA 선열람·Java 역사판 역추적.',
    'v2.3.1 doc/contents.rst와 GDAL 역사판 목차의 raw href 순서를 후보 본문 전에 별도 봉인한다.')
add('frozen_pool_slots_and_empty_slots', ['Q2'], True, True, 48, 48, 'six slots per requirement',
    '39개 실제 링크와9개 빈칸, 원 URL·순서·시각·발견 위치를 고정하고 보조 사례를 주풀에 넣지 않았다.',
    [ref('pool.csv'), ref('evidence/pool-freeze.json')])
add('all_candidate_relevant_originals_opened', ['Q2','Q3'], True, True, 39, 39, 'nonempty candidate slots directly read',
    '모든 실제 후보의 지정 절을 직접 읽었다. 전체 긴 파일 모든 행 정독이나 사용자 발견 관측을 뜻하지 않는다.',
    [ref('pool.csv'), ref('sources.jsonl')])
add('minimum_unique_primary_originals', ['Q1','Q2','Q3','Q6'], True, counts['counted_unique_documents'] >= 24,
    counts['counted_unique_documents'], 24, 'unique counted primary originals / minimum',
    '동일 원문·별칭·검색·실패를 제외하고 범주를 배타적으로 집계했다. M08에서66→64로 보수적 정정, 사실 원장은 보존.',
    [ref('sources.jsonl'), ref('evidence/source-counts.json'), ref('evidence/amendments.jsonl','M08')])
add('primary_original_mix', ['Q1','Q2','Q3','Q6'], True, counts['minimum_source_mix_met'], 5, 5, 'minimum categories satisfied',
    '소비자8≥8, 공급자22≥8, 동일성/배포/소스18≥4, 도서관5≥2, 음악11≥2. 같은 원문을 두 범주에 산입하지 않았다.',
    [ref('evidence/source-counts.json'), ref('sources.jsonl')])
add('source_ledger_required_schema_and_failures', ['Q1','Q2','Q3','Q6'], True, True, counts['source_rows'], counts['source_rows'], 'records with 14 required keys',
    '필수14키·원 URL·고정판·위치·사실·한계·중복·counted가 있고 실패·검색·미확인도 제외 사유와 함께 남긴다.',
    [ref('sources.jsonl'), ref('evidence/crossfield/access-log.jsonl'), ref('evidence/root/access-log.jsonl')])
add('url_count_separate_from_original_count', ['Q2','Q3'], True, True, 3, 3, 'distinct counting levels',
    '후보 URL32, 판별 접근 키17, 그 키의 고유 원문15를 구분한다. 전체 조사 고유원문64와도 다르다.',
    [ref('evidence/source-counts.json'), ref('RESULT.md','판별 접근 키로서')])
add('relation_entities_roles_and_manual_directions', ['Q3'], True, True, 85, 85, 'nonempty manually coded pairs',
    '주소·상류·부품·판·역할·양방향·근거·한계를 수동 원 판독에 연결한다. 빈 후보35쌍은 unknown, 전체120행이다.',
    [ref('relations.csv'), ref('evidence/analysis-input.json','relation_pairs'), ref('evidence/crossfield/FINAL_METHOD_REVIEW.md','수동 관계')])
add('uniform_directional_scope', ['Q3'], True, False, '미확인', 85, 'pairs in one common directional decision scope',
    'G/S 방향 범위가 다르고 G의 partial 어휘가 사전4값에 추가돼 공통 범위의 방향 비율을 집계하지 않는다.',
    [ref('evidence/amendments.jsonl','M07'), ref('RESULT.md','방향 판정 역시'), ref('relations.csv')],
    'G는 문서 근거 역할 치환, S는 완전 원 요구 대체. 부분 겹침을 yes로 승격하지 않았지만 통일된 비교는 아님.',
    'G2/S1/G4를 같은 목적·판·문서역할 또는 완전요구 범위로 고정해 독립 재판독한다.')
add('24_views_same_input_first_representative', ['Q4'], True, True, 24, 24, 'case-arm views',
    '원6슬롯 순서가 동일하고 최초 대표·최초3그룹을 사용하며 빈자리를 유지한다.',
    [ref('views.jsonl'), ref('evidence/CARDS.md')])
add('equal_declared_three_row_budget', ['Q4'], True, True, 24, 24, 'views with 3 rows / 1 direct link / 80-char cap / 0 extra clicks',
    '동일 후보의 제목·설명 문구와 링크를 유지하며 숨은 사실을 카드에 추가하지 않았다. 동일 상한의 비교다.',
    [ref('SCOPE.md','## 4.'), ref('views.jsonl'), ref('evidence/CARDS.md')])
add('literal_equal_description_length', ['Q4'], True, False, '미확인', 24, 'views with identical actual description length',
    '설명은80자 상한이며 서로 다른 대표의 실제 글자수는 같지 않다. 더 강한 사용자 조건을 충족했다고 보고하지 않는다.',
    [ref('views.jsonl'), ref('RESULT.md','설명은 동일한 80자 상한')],
    'SCOPE는 인위적 패딩 없이 상한을 고정했으며 실제 길이까지 같게 만들지 않았다.',
    '기존 카드 원문을 보존하고 새 반복비교에서 실제 문자수·제목 포함 여부를 사전 고정한다.')
add('required_result_tables_and_three_final_weaknesses', ['Q1','Q3','Q4','Q5','Q7'], True, True, 2, 2, 'leading required tables',
    'RESULT 제목 직후 핵심 관계10행, 이어24보기 표. 마지막 표는 W1/W2/W3 세 행이며 조사 첫 자료·결론 반전 조건을 담는다.',
    [ref('RESULT.md','| 요구 ID·목적·판 |'), ref('RESULT.md','| 요구 ID | 방식 |'), ref('RESULT.md','## 9.')])
add('full_pool_support_before_representative_readout', ['Q5'], True, True, 8, 8, 'requirements with original atoms and pool support coding',
    '25필수 atom과 공급자 근거 지원을 보기 계산 전에 수동 라벨링했다. 풀 지원8·미지원17, 완전 경로0을 분리한다.',
    [ref('evidence/analysis-input.json'), ref('evidence/gdal/coding-G.json'), ref('evidence/sphinx/coding-S.json')])
add('conditional_and_all_case_denominators', ['Q5'], True, True, 72, 72, 'loss rows with explicit denominators',
    '완전 적격 분모0은 해당 없음. 완전 답변0/8·부분/미확인 요구 수와 부분 atom 보존을 별도 보고한다.',
    [ref('losses.csv'), ref('evidence/recount-summary.json'), ref('RESULT.md','## 1.')])
add('paired_rows_losses_duplicates_and_returns', ['Q5'], True, True, 24, 24, 'paired case-comparison details',
    '8건×A/B,A/C,B/C의 atom 교집합·차집합·같은 집합 여부와 완전답변을 보존한다. G2/S1 손실, G4 반례, 적격 귀환0, 기능중복0과 문서반복을 구분한다.',
    [ref('evidence/recount-summary.json','paired_details'), ref('losses.csv'), ref('RESULT.md','같은 8건의 짝')])
add('complete_alternative_effect_observed', ['Q5'], False, False, 0, 8, 'requirements with a complete eligible path in the frozen pool',
    '부정적 결과를 숨기지 않았다. 이 조건은 효과 판정의 노출 범위이며 음성 관측 자체를 위조된 미실행으로 취급하지 않는다.',
    [ref('evidence/analysis-input.json'), ref('losses.csv')],
    '원 풀에서 완전 대안을 입증하는 경로가 없어 C의 적격 귀환 우위를 관측할 수 없다.',
    '고정 요구의 부족 atom을 확인한 뒤 새 전향 표본을 설계한다. 기존8건은 교체하지 않는다.')
add('library_and_music_primary_comparison', ['Q6'], True, True, 16, 4, 'library/music primary originals / minimum combined',
    '도서관5와 음악11, 구체 판/녹음/발매 레코드 및 제공자·소비자·편집자 관점을 대조하고 적용 추론을 구별한다.',
    [ref('evidence/crossfield/CROSSFIELD.md'), ref('evidence/crossfield/sources-X.jsonl'), ref('RESULT.md','## 5.')])
add('counterexamples_separate_from_main_pool', ['Q6','Q7'], True, True, 4, 4, 'requested stress categories located with bounded claims',
    '같은 상류 다른 행동, 한URL 여러부품, fork/설정 차이, 별도 구현의 제한 호환을 보조 원장으로 비교한다. 주풀에는 삽입하지 않는다.',
    [ref('evidence/crossfield/stress.jsonl'), ref('evidence/sphinx/stress-S.jsonl'), ref('evidence/root/stress-R.jsonl'), ref('RESULT.md','## 6.')])
add('unconditional_distinct_implementation_substitution', ['Q7'], False, False, 0, 1, 'unconditional full replacement proof',
    'libjpeg-turbo의 공급자 호환 선언과 예외를 확인했지만 모든 소비계약의 무조건 완전 대체를 입증하지 않았다.',
    [ref('evidence/crossfield/CROSSFIELD.md','XT3'), ref('evidence/RUNBOOK.md','타 분야와 호환 구현')],
    '고정 IJG 원판·실제 소비 호출·바이너리 실행이 없고 역방향 확장 예외가 있다.',
    'IJG v6b 원판과 소비 호출·입력·빌드 조건을 먼저 확보한다.')
add('single_factor_sensitivity_and_click_upper_bound', ['Q4','Q7'], True, True, 48, 48, 'sensitivity rows in addition to 24 primary rows',
    'U8/Vg8/Vr8/K24를 분리하고 원순서·대표를 유지한다. K-list와 전원문 상한을 구분해 B 부분근거2개의 회복 및 추가11문서 가정을 보인다.',
    [ref('losses.csv'), ref('evidence/amendments.jsonl'), ref('RESULT.md','## 4.')])
add('unknown_and_cross_version_exposure', ['Q7'], False, False, 0, 8, 'requirements exposing unknown identity or multiple candidate versions',
    '39후보가 모두 동일성 확인이고 요구별 후보판1개이므로 U/Vg 무변화를 안전성 증거로 쓰지 않는다.',
    [ref('evidence/source-counts.json'), ref('evidence/crossfield/FINAL_METHOD_REVIEW.md','민감도와 분모')],
    'U/Vg에 실제 변경 대상이 없다.', '새 전향 표본에서 미확인·여러 판이 자연 노출되도록 원장 범위를 사전 설계한다.')
add('member_and_meaning_metadata_restorable', ['Q7'], True, True, 24, 24, 'views reconstructable to six original slots with retained metadata',
    'all_groups·잘린그룹·빈슬롯에서 원6멤버/순서를 되살리고 analysis-input/pool/relations로 URL·용도·판·역할·근거·정정을 연결한다.',
    [ref('views.jsonl'), ref('evidence/analysis-input.json'), ref('pool.csv'), ref('relations.csv'), ref('RESULT.md','## 7.')])
add('human_click_adoption_or_blind_validation', ['Q4','Q5','Q7'], False, False, 0, 8, 'requirements with observed human/independent outcomes',
    '내부 경로별 단일 판독과 root 대조·정적 검토를 사람 효용·독립 블라인드 관측으로 부르지 않는다.',
    [ref('evidence/crossfield/FINAL_METHOD_REVIEW.md'), ref('SELF_CHECK.md'), ref('evidence/RUNBOOK.md','엄격한 표시')],
    '실제 사용자·클릭·채택·제품 실행을 관측하지 않았다.', '별도 공통판정·노출·총클릭 예산을 고정해 독립 반복조사를 한다.')
add('actual_two_click_proof', ['Q4','Q7'], False, False, 0, 24, 'views with actual total-two-click observation',
    'K의 모든 멤버 원문 열람은 접근 상한이며 링크 목록 노출과 원문 판독을 구별한다.',
    [ref('losses.csv'), ref('RESULT.md','K-list'), ref('evidence/RUNBOOK.md','엄격한 표시')],
    '형제 목록을 펼친 뒤 모든 원문을 읽는 비용을 실제 총두클릭으로 제한하지 않았다.', '총클릭의 정의와 원문을 여는 동작을 고정한 별도 화면 시험이 필요하다.')
add('recount_and_artifact_validation', ['Q1','Q2','Q3','Q4','Q5','Q6','Q7'], True,
    validation is not None and validation['status'] == 'passed',
    validation['checks_passed'] if validation else 0, validation['checks_total'] if validation else '미실행', 'artifact consistency checks',
    '원순서·예산·해시·원문 수·표/행·복원·범위·수치·recount byte equality를 검사한다. 연구 절차의 미충족과 별개다.',
    [ref('evidence/delivery-validation.json')] if validation else [ref('evidence/verify_delivery.py')],
    '' if validation else '수용 파일을 만든 뒤 최초 검산을 실행할 예정.', 'python -B docs/workstreams/research/AF-RES-040/evidence/verify_delivery.py')
reopen_ok = verification is not None and verification.get('remote_reopen', {}).get('both_match_local') is True
add('committed_result_and_acceptance_reopened', ['Q7'], True, reopen_ok, 2 if reopen_ok else 0, 2, 'files reread at fixed remote result SHA',
    'RESULT와 acceptance를 원격 결과 커밋에서 다시 읽고 blob/내용을 대조한다.',
    [ref('evidence/verification-receipt.json','remote_reopen')] if verification else [ref('evidence/commits.jsonl')],
    '' if reopen_ok else '첫 결과 커밋 이후 수행할 최종 절차다.', '결과 커밋의 RESULT.md와 evidence/acceptance-evidence.json을 고정SHA로 다시 연다.')
session_ok = verification is not None and verification.get('session_check', {}).get('exit_code') == 0
add('workbench_session_check_fetch', ['Q7'], True, session_ok, 1 if session_ok else 0, 1, 'specified final session check',
    '지정된 session check --fetch의 실제 종료 코드·stdout/stderr·검사 HEAD를 기록한다.',
    [ref('evidence/verification-receipt.json','session_check')] if verification else [ref('evidence/RUNBOOK.md','workbench.session check')],
    '' if session_ok else '고정 결과 커밋 재열람 뒤 실행할 예정.', 'python -B -m workbench.session check docs/workstreams/research/AF-RES-040/manifest.json --fetch')

payload = {
    'schema_version': 1, 'task_id': 'AF-RES-040', 'status': 'REVIEW_READY_WITH_GAPS',
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'claim_boundary': 'document-based reconstruction; no software/user/audio execution; not a general C superiority result',
    'result_stage_sha': verification.get('result_commit') if verification else 'pending first result-stage commit',
    'final_protocol': 'After this acceptance update is committed, reopen RESULT and acceptance at that fixed SHA; check it; write HANDOFF in a separate last commit. Final receipt is reported in HANDOFF without rewriting this file.',
    'counts': counts,
    'outcome': {'complete_answerable_by_arm': {'A': 0, 'B': 0, 'C': 0}, 'all_requirement_denominator': 8,
                'eligible_requirement_denominator': 0, 'conditional_complete_recall': '해당 없음',
                'required_atoms_total': 25, 'pool_supported_atoms': 8, 'unsupported_atoms': 17,
                'preserved_atoms': {'A': 8, 'B': 6, 'C': 8}, 'merge_hidden_atoms_B': ['G2.A2','S1-A1'],
                'revived_complete_eligible_alternatives': 0, 'views': 24, 'loss_rows': 72, 'relation_rows': 120},
    'criteria': criteria,
    'mandatory_met': sum(c['mandatory'] and c['met'] for c in criteria),
    'mandatory_total': sum(c['mandatory'] for c in criteria),
    'unmet_mandatory': [c['id'] for c in criteria if c['mandatory'] and not c['met']],
    'unobserved_effect_domains': [c['id'] for c in criteria if not c['mandatory'] and not c['met']],
    'prioritized_weaknesses': [
        {'id':'W1','scope':'zero complete eligibility; name-only and U/Vg no exposure','first_source':'https://github.com/OSGeo/gdal/issues/2169'},
        {'id':'W2','scope':'prospective raw-href traversal, literal description length, actual click limit','first_source':'https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst'},
        {'id':'W3','scope':'single internal classification, nonuniform directional scope, bounded compatibility and restoration','first_source':'https://musicbrainz.org/edit/115752742'}]
}
(P/'evidence/acceptance-evidence.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:payload[k] for k in ['status','mandatory_met','mandatory_total','unmet_mandatory']}, ensure_ascii=False))
