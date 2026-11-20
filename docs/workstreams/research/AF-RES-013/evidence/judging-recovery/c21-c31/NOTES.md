# C21–C31 후보 판정 — 내부 별도 검토

입력은 원격 `caa2a814727dd485ed0eb9bb8530d6b16fab9584`에서 재개한 31사례 중 C21–C31의 동결 접두부·CASES와 A/B 원 응답이다. 판정자는 **내부 별도 검토**이며 사람·다른 모델·사용자 검증이 아니다. 이 폴더 작성자는 gold를 읽고 채점했다. 검색 기준선을 새로 실행하지 않았고 원 응답/접두부를 수정하지 않았다.

## 단위와 확인

- 11사례 × A/B, 실제 후보 **111행(A72/B39)**을 모두 읽었다. `raw_response`와 `opened_documents`를 후보명과 별개로 읽었다.
- `judgments.json`의 축·라벨은 SCOPE 및 JUDGING_RULES의 L/E/H/T를 사용한다. 추가 `judged_date_status`는 원 `date_status`를 보존하면서 실제 시간 근거를 재평가한 값이다.
- H는 `reference_design`에서 원 응답이 한정한 부분 기여를 판정한다. `not_in_scope`는 source가 처음부터 해결한다고 주장하지 않은 부분이다. 아무 후보도 전체 시스템 구현 성공이나 실제 사용자 효용으로 판정하지 않았다.
- 대부분의 응답이 부분 메커니즘과 caveat를 구체적으로 제공했으므로 CONDITIONAL_TRANSFER가 많다. 이 수는 사람의 만족·채택·더 좋은 대안 수가 아니다.
- 해당 shard의 고유 `(case,gold)` 회수는 A10/B3이며 역사 적격 회수는 A7/B1이다. role 분모는 root의 전체 CASES 집계가 필요하다. 정답 밖 유용 후보 91은 111개 후보 중 행 단위이며 여러 사례에서 같은 자료를 반복 찾은 것이 섞인다. 역사 적격 유용 행은35다.
- `build_judgments.py`는 수작업 판정 매핑을 JSON으로 직렬화하고 누락만 검사한다. 의미적 판정을 자동 생성·검증하는 평가기는 아니다.

## 중요한 경계 판정

| 행 | 판정과 이유 | 바뀔 수 있는 최소 확인 |
|---|---|---|
| C21 A2 | per-member reference/move 초기화를 명시하여 R0114-G05를 structural_design으로 회수 | 원 응답이 개별 field capture를 명시한다는 읽기 범위를 교차검토 |
| C21 B1 | copy/reference capture 일반 모델만 제시. 개별-variable clause나 reference default까지 회수하지 않았다고 보수적으로 판정 | N2859 문서에 기능이 있다는 것과 응답이 그 기능을 제안했다는 것을 구별한 별도 검토 |
| C21 B4 | raw_response의 ordinary captures by reference는 reference-default 대안 R0114-G04와 일치. 2026 Nim 판이라 사후 적중 | 원 source의 default 적용 범위가 모든 closure냐 특정 iterator냐 확인 |
| C21 A3 | 원 실행은 상세 receiver 규칙이 snippet-only. 추가 판정 열람 JR2131-S01에서 lvalue/rvalue/cv receiver 규칙 확인. E는 보강 후 supported | 재현 시 원 실행 E unknown과 판정 보강 E supported를 구분 |
| C22 B1 | ThreadSafe와 최종 translation에 쓴 ConcurrentShareable을 각각 R0123-G03/G08로 일치. 후자는 새 이름 추론이며 이미 있던 정식 trait 이름을 찾았다는 뜻이 아님 | final-response synthesis를 연결된 후보에 귀속하는 일치 규칙을 교차검토. 좁은 민감도에서는 G08 한 항목을 제외할 수 있음 |
| C22 B5 | 후보 URL의 exact 성공 행은 없지만 열린 `/capabilities/reference-capabilities.html`가 후보의 `/reference-capabilities/reference-capabilities.html`로 이동한 기록이 있다. L ok | 원 run의 redirected_url과 읽은 권한 설명 대조 |
| C24 A1 | Dart initializing formals는 parameter를 모두 선언하고 대입만 합성하는 S0018-G05와 구조 일치. discussion URL의 이름 적중은 아님 | CASES match_kind를 structural_design으로 정정할지는 correction.json 참조 |
| C24 A6 | Common Lisp input/default/hook 분리는 있으나 immutable slots의 규칙은 별도 추가로 남음. H2 unknown, INSUFFICIENT | 불변 field의 초기화/쓰기 금지를 구체적으로 연결한 예시 1개 |
| C25 A4/A5/A7 및 B3 | framework neutrality나 결과 protocol만으로 ‘XCTest 기본 지원 없이 protocol만’이라는 S0019-G03을 찾았다고 세지 않음 | 원 후보가 default framework 부재를 명시했는지 확인. source에 기능이 있는 것만으로 확대 금지 |
| C26 A2 | GHC minimum-version predicate라는 기능만 언급. comma-separated version component syntax S0020-G03까지 말한 것은 아님 | 원 응답의 syntax 선택에 대한 명시 여부 확인 |
| C27 A2/A4/B1 | 짧은 callable 생성은 확인되나 same-type/same-arity/different-label 요구의 concrete resolution이 추가 설계로 남음. INSUFFICIENT | 동등 타입·arity의 label 두 개를 각각 선택하는 target syntax/정적 규칙 |
| C28 A2 | @selector 표기 S0022-G02 회수. runtime receiver check와 static class membership를 구별 | compile-time 검증으로 과장하지 않았는지 원문 확인 |
| C29 A5 | module signature로 helper를 숨기는 interface compartment는 useful하지만 원 gold의 scoped namespace와 같은 대안이라고 합치지 않음 | signature를 요구하는 공개 interface와 arbitrary lexical group의 차이 확인 |
| C30 A3 | 후보의 NSString counted initializer/Swift interop route는 G04의 관련 component로 회수하나, functional evidence는 snippet+metadata뿐. E/H unknown. 깨진 링크·가짜 아님 | Apple 본문과 고정 Swift bridge implementation을 읽고 재판정. 더 엄격한 ‘bridge faster 방법 회수’ 정의면 G04도 빼는 민감도 필요 |
| C31 A2/A4 | Debian/RPM comparator를 찾았어도 특정 hyphen 충돌·date→numeric migration gold를 원 응답이 명시하지 않아 G05/G04는 미적중 | 같은 생태계 이름과 특정 failure mechanism의 구별을 교차검토 |
| C31 B2 | SemVer 새 grammar는 명확하나 existing date/distribution spellings의 mapping을 미정으로 남김. H2 unknown, INSUFFICIENT. 알려진 전체 대체 실패를 주장한 후보가 아니므로 near_miss false | date/custom/Debian revision 각 1개를 포함한 migration rules |

## 날짜 정정 — 원값 유지

- C22 A2: original pre_decision → judged unknown. Qt4.7 archive와 2008–2010 copyright footer만으로 exact body의 날짜를 확정하지 않는다. C30의 같은 archive가 unknown인 것과 일관되게 처리한다.
- C25 A1: original pre_decision → judged unknown. 2015 launch가 XCTest 존재는 확인하지만 실제 제안한 suite-runner/exit behavior는 live source에서 읽었다. 존재 날짜와 정확한 동작의 날짜를 분리한다.
- C26 A2: original pre_decision → judged unknown. dated GHC PDF는 snippet만 읽었고 해당 날짜 원문은 열리지 않았다.
- C30 A6: original post_decision → judged unknown. live Java8 문서의 검색 메타데이터 `Published five months ago`를 원문 발행판의 날짜로 확정하지 않는다. 이 정정은 pre_decision으로 올리는 것이 아니다.

## 직접 추가 읽은 자료

`sources.json`에 성공 URL12개와 실패 URL4개를 분리했다. 최초 C21–31 경계검증4개에 C01–10 교차검토 원문3개와 C27 분류 정정 원문1개, 비적중 gold 분류의 원문·토론4개를 추가했다. 마지막 원 메일 JR2131-S12는 JR2131-S11의 해당 reply와 동일 내용이므로 독립 자료 최소 개수에 중복으로 넣지 않는다. 외부 전문·사용자명·프로필은 저장하지 않았다. 추가 문서는 판정 단계의 읽기이며 원 A/B 실행 예산과 로그를 바꾸지 않는다. `SEARCH_LOG.json`은 이 추가 확인에서 검색 질의는0이고 특정 URL 재열람만 했음을 기록한다.

## 교차검토

`CROSS_REVIEW.json`은 다른 shard C01–10의 경계16행을 반증 우선으로 검토한 제안이다. 원 shard는 수정하지 않았다. C03 A4의 node-binary 대안 G10 회수 제거, C05 B3의 unresolved semantic grouping H2로 인한 INSUFFICIENT 강등을 제안한다. C03 B5의 H1은 실제 scope가 API-visible diagnostic lifecycle이므로 namespace/filesystem inspection의 pass가 아닌 not_in_scope로 좁히도록 권고했다. C02 A4는 allocator 참고를 pod capability implementation 검증으로 확대하지 않도록 설명을 한정했다. 나머지 구조 경계는 유지 근거를 남겼다.

C11–20 담당자의 역방향 검토에서 C24 A3 Scala는 hidden-state H3를 not_in_scope로 좁히는 제안에 동의했다. root가 교차검토 이력과 최종 판정을 조립하며 이 폴더의 원 개별 판정은 변경하지 않았다. C27 G02도 C24 G05처럼 토론 URL을 가진 syntax 대안이므로 structural_design으로 정정할 것을 `correction.json`에 추가했다.

## 비적중 gold의 분류 일관성

분류 기준은 고정 gold가 비교하는 **대상의 identity**다(SCOPE §5). URL이 forum인지 문서인지, 후보가 적중했는지는 기준으로 사용하지 않는다. 따라서 앞선 S0018-G05와 S0021-G02의 구조 정정은 다음 비적중 두 항목에도 적용해야 한다. 이는 기존 규칙의 일관된 적용이며 항목 추가·분모 변경·역할 변경·적중 추가가 아니다.

| 항목 | 기존 → 제안 | 원문에서 비교하는 대상 | 외부 실체라는 반증 검토 | 근거 |
|---|---|---|---|---|
| S0021-G01 | external_entity → structural_design | getter/setter를 대신해 전체 property interface를 보존하는 lens 접근 형태. 연결된 원 메일은 T → inout U와 recursive writeback, copy-on-write partial update를 설명한다. | lens는 알려진 일반 개념명이지만 여기서 특정 라이브러리·논문·표준을 이름으로 비교하지 않는다. 원 토론 스스로 제안하는 접근 인터페이스를 설명한다. | 고정 SE0021 Alternatives 첫 bullet; JR2131-S08 추가 읽기, JR2131-S11 reply 3, JR2131-S12 원 메일 |
| S0022-G01 | external_entity → structural_design | selector identity와 method signature를 함께 담는 새로운 @convention(selector) 호출 규약. | forum은 D/Objective-C prototype을 영감으로 언급한다. 그러나 동결 gold는 그 외부 prototype이 아니라 제안된 Swift 호출 규약이다. 간접 영감의 외부 실체와 gold target을 합치지 않는다. | 고정 SE0022 Alternatives 첫 대안 JR2131-S09; 원 토론 JR2131-S10 opening/replies |

일치 경계도 그대로 엄격하게 유지한다. lens라는 단어만 같거나 독립 getter/setter가 있다는 것으로 S0021-G01을 회수했다고 세지 않는다. 전체 property access와 mutation/writeback 구조의 대응이 필요하다. selector 이름의 철자 또는 method 존재만 검사하는 도구로 S0022-G01을 회수했다고 세지 않는다. 이 항목의 핵심은 receiver·argument·result type과 selector identity를 결합한 호출 계약이다. 두 항목 모두 기존 비적중 판정을 유지한다.

토론 본문을 읽었지만 사용자 이름·프로필·본문 전문은 저장하지 않았다. source 기록에는 URL·일시·읽은 절·요약·한계만 남겼다. post-specific forum URL 실패와 정상 topic/original archive 성공은 분리 기록했다.

## 한계

주된 불확실성은 구조 일치의 폭과 좁은 reference의 H 적용 경계다. C22-B1의 파생 이름과 C30-A3의 component 회수는 별도 민감도로 남겼다. 단순 이름 유사성, source가 제공하지만 응답이 제안하지 않은 기능, 다른 모델/사람의 독립 검증으로 결과를 확장하지 않는다. 새 source 읽기는 현재 사실 검증이며 과거 검색에 소급 삽입하지 않는다.
