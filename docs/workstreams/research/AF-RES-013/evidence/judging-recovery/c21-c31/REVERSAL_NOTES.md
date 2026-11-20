# 대체된 결정과 원 응답의 대응 — C21/C29/C31

이 파일의 후속 이유 대응은 primary gold의 적중에 소급 합치지 않는다. gold에 없는 후속 메커니즘을 현재 판정자가 발견한 것과 baseline이 원 prefix로 이미 제시한 것을 구분한다.

| 사례 | 뒤집힌 결정 / 이유 | 기준선이 원 접두부로 찾은 것 | 판정 / 시간 |
|---|---|---|---|
| C21 / R0114 → R0231 | explicit capture/receiver annotation에서 capture/receiver inference로 이동. callable-trait 자체의 폐기는 아님 | A의 C++ explicit per-variable capture는 원 대안 G05를 찾았지만 receiver inference G08을 제시하지 않는다. B Nim의 ordinary reference capture는 G04를 찾지만 receiver/capture inference의 편의성 개선 전체를 찾은 것은 아니다. | 엄격한 후속 이유 해결 적중0. B의 reference-default 관련 단서1은 사후2026 판. 미확인(각 원 응답의 inference 없는 사실을 전체 raw_response와 대조). |
| C29 / S0025 → S0169 | 같은 파일·같은 타입 extensions에 private 권한을 공유하여 lexical-only boundary를 완화 | A4가 C# partial declarations를 제시하고 ‘Partial blocks form one type, so ... share privacy privileges across those blocks’라는 구조를 실제 원 응답에 적었다. 2006 ECMA-334 §10.5.2·§17.1.4를 열어 읽은 기록이 있다. | 결정 전의 reversal-related mechanism 1. 같은 type의 여러 declaration block을 묶는 원리는 찾았지만 Swift same-file restriction, 확장 문맥, 실제 후속 채택 이유의 효용까지 검증한 것은 아니다. primary gold 미적중과 양립. |
| C31 / P0386 → P0440 | 개발 버전 순서·epoch·local identifier·호환 release bounds 등으로 기존 표기 이전을 보강 | A2 Debian의 epoch/new-numbering-scheme, A4 RPM EVR가 epoch라는 후속 관련 요소를 원 응답에 포함한다. A3 Ivy는 qualifier/range 기여가 있으나 PEP440의 특정 바뀐 순서를 제시하지 않는다. B는 Repology/semver ordering만으로 실제 PEP440 후속 변경을 모두 찾지 않았다. | epoch 관련 후보2행, 모두 exact opened doc 날짜 unknown. 결정 전 후속 이유 해결 적중0. epoch는 original PEP gold의 특정 hyphen/date migration 사건을 자동 회수한 것으로 세지 않는다. |

## 근거 위치

- `cases/CASES.json`: C21/C29/C31의 `superseded_by`에 고정 후속 판과 범위가 있다.
- `runs/A/C29.json`: candidate rank4, raw_response item4, opened_documents의 ECMA-334 두 열람 행.
- `runs/A/C31.json`: candidate rank2/4와 raw_response; current Debian/Fedora 문서 날짜 unknown 보존.
- `runs/B/C21.json`: candidate rank4, Nim2.4.2 2026-11-13 date evidence.

## 한계

원래 설계자가 더 일찍 이 후보를 보았다면 결정을 바꾸었을지 또는 재설계 비용이 줄었을지는 관측하지 않았다. 후속 문서와 과거 baseline 후보의 논리 대응은 사후 분석이며, 당시 설계자의 수용도나 인과효과가 아니다.
