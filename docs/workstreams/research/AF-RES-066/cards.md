# 사용자 카드 — 근거가 허용하는 최소 표현 (초안)

## 1. 해당 절에서 방향이 지지된 사례 (조건부)
**'NLM은 SMARCAD1 관련 선천성 무지문증 사례를 설명합니다. 따라서 모든 사람이 지문을 갖고 태어난다는 보편문장은 성립하지 않습니다.'** [원문](https://medlineplus.gov/genetics/understanding/traits/fingerprints/), 본문 genetics paragraph / `S52`. 이 자료는 사건의 빈도·모든 기타 지문 질환을 측정하지 않는다. '본 링크 3개가 완전히 검증'으로 표시하지 않는다.

## 2. 원문이 선택에 반함
**'USGS의 인체 수분표는 폐 약83%, 피부 약64%를 기재하므로 피부가 더 높다는 선택을 반박합니다.'** [원주소](https://www.usgs.gov/special-topics/water-science-school/science/water-you-water-and-human-body), `S18`; 선행 [AF062 당시판 영수증](https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/streams/root/archive-body-verification.json). 측정 기준·장기별 값이 후대 정정될 경우 재검토.

## 3. 일부 명제만 설명
**'NASA 문서는 달을 걸은 사람이 12명임을 설명합니다. 그러나 마리아나 해구의 동일 기준일 고유 방문자 수는 이 절에 없습니다.'** [NASA](https://science.nasa.gov/moon/moon-walkers/), `S11`. '따라서 달이 더 많다'나 '따라서 해구가 더 많다'의 완전 검증은 불가. 기준일/방문 정의를 맞춘 심해 방문 원기록 필요.

## 4. 판·접근 미확인
**'이 원주소의 실험 시점 본문은 확인되지 않았습니다. 현재판 또는 URL 이름만으로 당시 근거 효력을 보장할 수 없습니다.'** 예: [CIA 브라질 원주소](https://www.cia.gov/the-world-factbook/countries/brazil/), `S43`, 현재 다른 안내 페이지로 향하는 관측; 2024 해당 테이블 원문과 보관판 미검증.

## 데이터 필드 제안
`advice_id, proposition_id, provided_url, reached_url, section_locator, version_datetime, accessible_at_cutoff, quote_scope, unit, population, comparison_peer, status, lineage_id, verified_by, unresolved_input`를 분리한다. 소프트웨어 설계의 가설이며 사용자 효과가 검증된 기능은 아님.
