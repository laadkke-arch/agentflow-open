# AF-RES-079 · 첫 판정과 가림 재판독의 대조

## 가림 종료와 고정 입력

이 문서는 가림을 끝낸 뒤 작성한 대조다. 첫 판정과 재판독 원본은 수정하지 않았다. 판독자는 동일한 별도 도구 에이전트 `/root/standards_evidence`이며 인간 검토나 다른 모델의 독립성을 주장하지 않는다.

- 첫 판정: `evidence/first-assessment.json`, 고정 시각 `2026-11-23T11:41:36.238293+00:00`, SHA256 `451e7ee3b76a16b80562147fe164ed5f6b8f904fa1928edeaaa200c61b66c66d`.
- 가림 재판독: `streams/review/blind-review.json`, 완료 시각 `2026-11-23T11:41:51.337317+00:00`, SHA256 `5ec70c5eae00ece48360bd95964eb30e3cfddfc4ff5987f3de9319e75da949b1`.
- 가림 종료 기록: `2026-11-23T11:46:41.136913+00:00`. 부모의 명시적 지시에 따라 첫 판정을 처음 읽은 도구 호출의 종료 시각이다. 첫 노출의 밀리초 단위 정확한 시작 시각을 뜻하지 않는다.
- 대조 완료: `2026-11-23T11:48:10.584496+00:00`. 허용된 두 입력만 대조했고 첫 판정이 참조하는 events/notes/relations와 RESULT는 열지 않았다.
- 첫 판정 파일은 고정 시점에 재판독 결과를 열지 않았다고 기록한다. 이 자체 기록을 보존하며 별도의 외부 시간 감사나 통계적 독립성을 주장하지 않는다.

## 단순 코드 집합과 범위별 의미

단순 대조는 첫 파일의 `decision_codes`와 재판독의 `primary_code + additional_codes`를 집합으로 만든다. 원형 숫자와 일반 숫자 표기를 정규화하고 순서는 무시한다. 조건부 ③은 집합에 넣지 않는다. 첫 파일의 산문에만 적힌 ⑤를 배열에 몰래 추가하지 않는다.

| 사건 | 최초 명시 코드 집합 | 재판독 명시 코드 집합 | 집합 대조 | 단위별 해석 | 처리 |
| --- | --- | --- | --- | --- | --- |
| G01 | {1,4} | {1,4} | 같음 | driver①와 source-container④가 양쪽에서 분리됨 | 수용 + 기록 보완 |
| G02 | {1} | {1,5} | 다름 | 최초 산문에도 후속⑤ 보류가 있으나 배열에는 빠짐 | 보완 후 수용 |
| O01 | {4} | {4} | 같음 | 같은 callable 후속④; ③은 조건부 예시 | 수용 |
| O02 | {2} | {2} | 같음 | 네 fully-qualified 쌍의 별칭②, 사건 수는1 | 수용 |
| C01 | {1,2} | {1,2} | 같음 | project①/namespace②; 배열 순서만 다름 | 수용 + 판 범위 보완 |
| C02 | {4} | {4} | 같음 | 별도 배포물의 fork④; ③은 양쪽 모두 조건부 | 수용 + 출처 권위 보완 |

명시 코드 집합이 같은 사건은 G01·O01·O02·C01·C02이고 다른 사건은 G02다. 이는 여섯 문서 행의 서술적 대조다. **독립 일치율·정확도·통계적 성능으로 해석하거나 백분율로 확장하지 않는다.** G02도 단위를 맞추면 역사적 ID 유지와 후속 미지정 보류라는 뜻이 반대되지 않는다. 두 요약에서 실질적인 관계 방향·식별 단위 충돌은 확인하지 못했다. 이것이 관계의 참 또는 행동 호환성이 검증되었다는 뜻은 아니다.

첫 판정은 관계 요약이며 증거 ID를 제공한다. 재판독은 P1/P2 정적 해석을 더 자세히 담지만 직접 실행하지 않았다. 따라서 이번 대조는 양측의 실행 결과나 기능 적합성의 일치 여부를 판정하지 않는다. 공통으로 남는 보류가 많다는 사실을 가리지 않는다.

## 사건별 수용·보완·미해결

### G01 · 수용 + 기록 보완

**수용한 범위.** Both preserve logical RASDAMAN adapter/driver identity under① and link core distribution source to a separately archived component under④. Neither equates the GDAL adapter with the rasdaman server product or asserts executable drop-in compatibility.

**차이와 보완.** No substantive relation difference. Blind review makes logical driver versus source-container identity explicit and highlights the receiver README general3.5 heading versus exact3.7/2023 move evidence. Retain separate driver-ID and source-container relation rows; prefer exact release/move evidence when recording Rasdaman removal edition. Record that extra-driver source is outside integrated build.

**미해결.** Version-compatible extra-driver build, identical rasql input, error outcomes and full required georeferencing/write behavior. First-assessment is a relation summary, so its evidence references are not treated as runtime proof.

**다음 첫 확인.** Pin the old GDAL build and a compatible extra-drivers build; provide the same rasql database fixture and expected values/errors. Before claiming P2, supply an actual implementation supporting required creation and georeferencing.

**③ 취급.** No③ assignment in either asserted set; no mixed record supplied.

근거 위치: 최초판정의 `G01` 행과 가림재판독의 같은 행. 최초 원문 연결은 `G-NEWS-3.7.0, G-issue4808, G-issue4808-comments, G-ras-move-commit, G-ras-doc3.6, G-ras-dest-doc, G-ras-code3.6, G-ras-dest-code, G-extra-readme, G-ras-dest-test`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

### G02 · 보완 후 수용

**수용한 범위.** Both retain the retired ARG identity① and refrain from inventing a successor. The first scope text already calls an unknown future replacement a separate⑤ hold, while its decision_codes array contains only①.

**차이와 보완.** Raw code sets differ: first{1} versus blind{1,5}. This is placement/serialization of a secondary hold, not opposing decisions about ARG identity or a nominated replacement. Use separate structured claims: historical ARG ID→①; replacement target→⑤ with new ID null. Preserve both original files rather than retroactively changing first codes to force equality.

**미해결.** Specific replacement format, default-enable behavior of pre-removal installations, same-input conversions and old-consumer roundtrip. Reviewer-read provider tests explicitly opt into deprecated driver support.

**다음 첫 확인.** Choose a named replacement and old consumer version; run the same ARG input with recorded enablement settings and compare values/dtypes/order/CRS/nodata plus malformed-file errors.

**③ 취급.** No③ assignment. Retirement alone is not evidence that an existing identity record mixed targets.

근거 위치: 최초판정의 `G02` 행과 가림재판독의 같은 행. 최초 원문 연결은 `G-NEWS-3.8.0, G-NEWS-3.9.0, G-issue7920, G-arg-doc-3.7, G-arg-doc-3.8, G-arg-code-3.8, G-arg-reg3.8, G-arg-reg3.9, G-arg-test-3.8`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

### O01 · 수용

**수용한 범위.** Both use④ at function/callable scope. Blind review expands the terse first scope function into public name, version, scale meaning/default and argument adaptation.

**차이와 보완.** No core relation difference. Blind review adds a conditional③ example only if a real record had conflated old/new callable contracts; it does not assert an observed split. Expose the scale inverse mapping and retain old wrapper separately from new callable. Label source-derived numeric examples as predictions. Keep conditional③ outside asserted code sets and error counts.

**미해결.** Full pinned1.4.1/1.5.0 runtime matrix, dtype/NaN/axis/error and warning policies. The first-assessment relation-only summary does not enable a behavioral agreement claim.

**다음 첫 확인.** Run unchanged old call and adapted new call separately on y=[1,3,2], scale defaults and scale=2, followed by frozen empty/singleton/2-D/float32/complex/invalid-axis cases.

**③ 취급.** ③ is a hypothetical remedy contingent on an actual mixed record; none was supplied. It is excluded from raw code-set comparison and observed false-merge counts.

근거 위치: 최초판정의 `O01` 행과 가림재판독의 같은 행. 최초 원문 연결은 `OS-REL-05, OS-PR-11431, OS-ISSUE-11090, OS-DOC-O01-old, OS-DOC-O01-new`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

### O02 · 수용

**수용한 범위.** Both use② for the coordinated naming migration. First explicitly says one recruitment event with four mappings; blind review requires four fully-qualified target pairs and version1.6.0 limits.

**차이와 보완.** No core relation difference. Blind conditional③ concerns only a hypothetical short-name record that confuses scipy.integrate.trapz and scipy.stats.trapz. Keep event count1, mapping count4, and function-specific namespaces. Preserve corrected same-commit _quadrature.py locator and do not infer old-name survival after inspected1.6.0.

**미해결.** All four pairs’ executed dtype/axis/error matrix; distribution-specific input for stats.trapezoid. No behavioral agreement can be inferred solely from matching alias codes.

**다음 첫 확인.** Run pinned1.5.4/1.6.0 separately for each fully-qualified pair; use sampled-data fixtures for integrate and appropriate distribution fixtures for stats.

**③ 취급.** ③ remains conditional on an actual record conflating integrate and stats. No such record was provided, so no observed split or false merge is counted.

근거 위치: 최초판정의 `O02` 행과 가림재판독의 같은 행. 최초 원문 연결은 `OS-REL-06, OS-ISSUE-12924, OS-PR-12927, OS-PR-12934, OS-DOC-O02-old, OS-DOC-O02-new`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

### C01 · 수용 + 판 범위 보완

**수용한 범위.** Both preserve project/product identity① and use namespace alias② for0.9, without general numerical compatibility. Code order differs but sets do not.

**차이와 보완.** No core relation difference. Blind review distinguishes inspected0.9 alias behavior from the announced0.11 removal, which was not independently inspected in the packet. Record verified alias edition0.9 and announced termination0.11 in separate fields; do not mark announced termination as observed. Keep project and namespace units separate.

**미해결.** Deep-import behavior, a specified estimator’s before/after data and API errors, and actual alias-removal implementation/version.

**다음 첫 확인.** Choose estimator, dataset and fit parameters; compare0.8/0.9 unchanged/migrated calls. Inspect0.11 implementation only if a verified alias end is needed.

**③ 취급.** No③ asserted or necessary from namespace rename alone.

근거 위치: 최초판정의 `C01` 행과 가림재판독의 같은 행. 최초 원문 연결은 `R002, R005, R026`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

### C02 · 수용 + 출처 권위 보완

**수용한 범위.** Both identify distinct PIL and Pillow distributions linked by④ fork relation and explicitly condition③ on an existing record that mixes distribution/source kit, import namespace or PyPI registry custody.

**차이와 보완.** No core relation difference. Blind review explicitly separates current old-domain authorship,2010 fork notices and2020 registry custody. First summary provides source IDs but not their contents; absence of these details in the summary is not proof the first researcher omitted them. Exclude current pythonware.com page from original-author consent evidence; retain original fork notice/author response and separately dated registry transfer. Mark downstream-preserved old README attribution rather than treating it as original-host capture.

**미해결.** Version-matched installed image input/output and mode/metadata/plugin/core-extension errors. Shared import name and transfer of registry custody do not settle behavior.

**다음 첫 확인.** Pin PIL1.1.7 and a named Pillow version with Python/install environment; compare the same image and plugin/missing-core cases, keeping2010 lineage and2020 registry custody as separate histories.

**③ 취급.** ③ is explicitly conditional in both records. No actual mixed record was supplied; do not label this an observed repair, independent error count or confirmed false merge.

근거 위치: 최초판정의 `C02` 행과 가림재판독의 같은 행. 최초 원문 연결은 `R008, R014, R031, R035, R036`; 실제 URL 목록은 `review-comparison.json` 해당 행에 원형대로 보존했다.

## 조건부 분리와 관측 오류의 구분

이 여섯 사건의 입력에는 실제 기존 혼합 레코드가 없다. O01·O02의 재판독과 C02의 양쪽 기록에 있는 ③은 해당 혼합 레코드가 나중에 확인되었을 때 쓸 수선 규칙이다. 관계가 다른 대상을 발견했다는 사실만으로 그 대상이 이미 한 레코드에 합쳐져 있었다고 추론하지 않는다. 조건부 ③을 완료한 분리, 관측한 거짓 병합, 독립 오류의 분자에 넣지 않는다.

첫 판정 파일에 포함된 G03·G04·O03·O04·C03은 이번 여섯 건의 가림 재판독 범위 밖이다. 이들의 코드와 진위를 추가로 판정하지 않았다. 전체 모집틀의 독립 전수검토도 수행하지 않았다.

## 검사의 범위

두 입력의 SHA256, 여섯 대상 ID, 자연4/대조2 분모, 사건별 처리·미해결·다음 확인 필드를 검사했다. 결과는 `review-comparison.json` 안의 validation에 기록했고 종료값은0이다. 이는 문서 대조 검사다. 새 소프트웨어 실행, 새 웹 원문 확인, 모집 순위 전수감사 또는 권위 있는 정답 확정은 수행하지 않았다.
