# AF-RES-018 implementation notes

## 2026-11-21: separate internal analysis review

An additional internal model agent reviewed the analysis source against `SCOPE.md`, the judging rules, and the claim rules before inspecting any actual experiment results. The review used synthetic numerical inputs and in-memory replacements for file access. It did not read run artifacts, gold grades, generated result metrics, or other AF-RES workstreams. The agent inspected the question metadata only for covariate vocabulary and sample size. After the initial review, the integration owner authorized a structural check of `query_id` and `entity_id` columns in the frozen gold TSV.

The full review, input hashes, original findings, fixes, checks, and unresolved limits are recorded in `analysis/independent-code-review.json`. This is a separate internal agent review. It is neither human review nor an independent-model-family or fresh-execution replication.

### Auxiliary grade-2 entity recovery

`analysis/metrics.py` now emits `grade2_entity_recall_at10_micro`: the sum of uniquely retrieved grade-2 entities divided by the sum of frozen eligible grade-2 entities. This completes the auxiliary measure required by SCOPE section 7. The existing grade-2 question-hit measure remains separate, and the new measure uses the existing paired question-cluster ratio bootstrap.

A synthetic two-question example verifies the denominator distinction: A retrieves one of two grade-2 entities in the first question and none of one in the second, yielding entity recovery `1/3` and question-hit rate `1/2`. P retrieves all three, yielding `1` for both measures. These numbers are fabricated verification inputs, not AF-RES-018 observations.

### Row-valid judging-source ordering sensitivity

`analysis/source_order.py` retains its original external/primary/secondary identity-pool comparisons and adds three explicitly named sensitivities: external versus primary row-valid recall, external versus secondary row-valid recall, and primary versus secondary row-valid recall. Each comparison selects the common eligible question set for the fields it compares. JSON and CSV outputs identify the `comparison_basis` and `analysis_role`.

Identity-pool recall treats an entity as relevant to the internal pool when either condition has a relevant row, then credits the entity's presence in each condition. Row-valid recall uses the same pool denominator but requires the condition's own row to be judged relevant. Both summaries remain available; raw row disagreements are preserved.

A synthetic example demonstrates why both orderings matter. Let external gold contain G, A return X judged internally relevant, and P return X judged N plus G judged 0. External recall favors P; identity-pool recall ties because both returned X; row-valid recall favors A. The revised source-order report emits both the original `one_tie` identity comparison and the additional `reversed` row-valid comparison. Missing secondary coverage remains `unscorable`. No actual AF-RES-018 ordering was inspected during this check.

### Structural and preservation checks

The frozen TSV contains 270 identifier rows and 270 unique entity IDs, with no entity ID reused across questions. This resolves the source review's hypothetical cross-question grade-index collision for the current dataset. Only the question/identifier relationships were examined; no gold grades were aggregated. `analysis/build_observations.py` was left unchanged.

Synthetic checks also confirmed paired question resampling, question-cluster claim ratios, distinct macro/micro recall denominators, null estimates for empty strata, reproducible sampling without replacement from an unchanged claim frame, and the separate handling of all-question and hit-only ranks. The modified Python sources parse successfully.

The two changes are additive reporting fixes. They do not change the selected questions, claim sample, frozen gold, raw runs or judgments, C1–C4 thresholds, H1 point-status logic, or validation gates. The integration owner must run the existing deterministic recomputation and assess the actual result qualifiers. This reviewer did not execute production analysis, assert semantic correctness of actual normalization, or certify the actual freeze and dispatch chronology.

## 명시 코드검색 시도 감사 — 결과 집계 전

analysis/code_search_audit.py는106개 실행의 실제 질의/열람 기록에서 grep.app 또는 GitHub type=code를 대조한다.105/106개에 명시한 코드검색 시도가 있고 P/SX01은 type=repositories만 있다. 이를 코드검색 성공으로 바꾸거나 뒤늦게 질의를 추가하지 않는다. 주 분석53쌍은 보존하고 explicit_code_search_both 민감도에서 SX01쌍을 제외한다. 결과를 본 뒤 고른 제외가 아니며 기준 C1–C4는 그대로다. 접속 성공·완전한 도구 계측을 입증하는 감사는 아니다.

## 주장 인용 위치의 유일성 — 표집 전

claims/prepare.py와 sample.py에 원 응답 안 source_quote가 정확히 한 번 나타나는지 확인하는 게이트를 추가했다. 동일한 짧은 문구가 여러 후보에 반복되는 경우 raw.find가 잘못된 근처 문맥을 넘길 수 있어 추출자에게 실제 후보 문맥까지 인용구간을 확장하도록 했다. 사실 내용·조건·표집 알고리즘·진위 기준은 바꾸지 않았다. 이는 표집과 진위검증 전에 수행하는 원문 위치 무결성 점검이다.
