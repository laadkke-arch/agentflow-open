# AF-RES-026 · 사후 통합·집계 교차검토

- 검토자: `/root/sqlite`; 요청자: `/root`.
- 실제 시각 확인: **2026-11-22T05:50:28Z**, `clock.curr_time` 호출 결과.
- 범위: 사후 자료 통합·집계의 교차검토. **독립 이중 원문판독 또는 맹검이 아니다.** SQLite T0/T1을 작성한 동일 담당자가 이미 본 자료와 통합자의 집계 정의를 대조했다.
- 대상: `SCOPE.md`, `ANALYSIS_RULES.md`, `analysis.csv`, `strategy-summary.csv`, `adjudication-overrides.json`, `evidence/metrics.json`, `evidence/source-counts.json`, `evidence/window-audit.json`과 아래 연결 근거. 검토 시점 해시는 [integration-review.json](integration-review.json)에 있다.
- 외부 고유 원문 추가 산입: **0건**. 최종 `RESULT.md`의 문구 검토는 아직 포함하지 않는다.
- 이 기록은 root의 ⑤ 묶음 커밋을 기다린다. 이 기록 자체를 원격 커밋하거나 GitHub에서 재독했다고 주장하지 않는다.

## 검토 결론과 조치의 종류

| ID | 종류 | 확인한 위험 | 현재 처리 |
| --- | --- | --- | --- |
| IR01 | 집계 적용 오류 교정 및 사후 정의 정합화 | 한정된 기술응답을 원래 목표의 전체 사용 승인으로 읽음 | root 수용 및 수정 반영: I4/C4 → I4/C3 → I4/C2 |
| IR02 | 유지할 증거 경계; 새 오류 판정 아님 | 원판 식별24·추가 보강18·미노출23을 같은 증거 수준으로 부름 | 최신 SCOPE의 구분을 확인; 교집합17과 원형 헤더 한계 유지 |
| IR03 | 유지할 변수 회수 경계; 새 오류 판정 아님 | Q 신규 값0을 일반 명확화 답변0으로 읽거나 약한3을 확정 회수로 합침 | 엄격 플래그·이견·분모0 표기를 함께 사용 |
| IR04 | 유지할 비용 경계; 새 오류 판정 아님 | 실제 주 왕복7과 구현1을 중복·시간대·가상 전략 효과로 오독 | 서로 다른 쌍8, 기술 입력만6, 실제/가상 분리 |
| IR05 | 유지할 행동·관측단위 경계; 새 오류 판정 아님 | 진전3을 사용자 채택3으로, 파일 행 수를 사건 수로 읽음 | 행동 세 종류와 원장/발화/검열의 분모를 보존 |

## IR01 · 전체 사용 승인 집계의 두 차례 교정

발견 당시 통합 집계는 같은 사례 목록 `S01/S03/S08/P01`을 I와 C에 적용하여 전체 사용 승인을 **I4/C4**로 세었다. 이 수는 한정된 근거 응답 **I13/C14**와 별개의 지표다. 전체 사용 승인은 원래 목표의 필수조건을 충족하는 특정 사용이 문구와 T0에서 정해지는 경우에 한정한다.

첫 지적은 **S08 C**였다. 봉인된 I는 `?` 바인딩과 나머지 NOT NULL 입력을 함께 말했으나 C는 바인딩/SQL 식별자 갈림만 설명했다. 따라서 S08 C의 좁은 설명은 지지하면서 전체 목표 승인은 제외해야 한다. root는 전략별 목록을 분리하는 **I4/C3** 수정을 수용했다. `adjudication-overrides.json`의 S08 기록 시각은 `2026-11-22T05:46:29.871734+00:00`이다. 이는 원문에서 뒤늦게 얻은 새 사용자 정보가 아니라 집계 적용의 교정이다.

이어 **S03 C**의 경계를 재검토했다. OFF는 최초판의 현재 설정/선호이지 유지가 필수라고 확인된 조건이 아니다. C의 어느 가지를 선택할지 확정되지 않았고 legacy 경로에는 다른 참조 의미 확인도 남아 있다. 계열의 기존 `전체 승인=true`는 가능한 drop/recreate 경로가 존재한다는 넓은 판단이었다. 통합 정의의 엄격한 전체 사용 승인에서는 C를 제외해야 한다는 사후 이견을 root가 수용하여 **I4/C2**로 정했다. S03의 기록 시각은 `2026-11-22T05:48:15.061991+00:00`이다. 가능한 A 가지만 포함하는 넓은 해석의 **C3**은 민감도로 남긴다. 이 단계는 집계 정의의 정합화이며 사전 등록된 판정 변경이나 새로운 작성자 사실의 효과가 아니다.

최종 전체 승인 목록은 I=`S01/S03/S08/P01`, C=`S01/P01`이다. S01 C는 이미 T0에 있던 새 파일 목적을 첫 가지에 명시적으로 연결하며, P01 C는 T0에 알려진 부모 행의 조회라는 원래 목표에 적용된다. P01에서 늦게 표명한 데이터 입력 목적을 T0로 소급하지 않았다. 미노출23에서는 S01을 제외하여 **I3/C1**이다. 한정 근거 응답 **I13/C14**와 원 목표 판정에 필요한 T0 사실 **6/24**는 그대로다.

근거: [봉인 문구](../streams/sqlite/frozen-responses.jsonl)의 S08/S03/S01, [SQLite 사례 판정](../streams/sqlite/case-analysis.jsonl)의 S08/S03 strategies, [PostgreSQL 봉인 문구](../streams/postgres/frozen-responses.jsonl)의 P01, [통합 보정](../adjudication-overrides.json)의 S08/S03 및 전략별 승인 목록, [분석 정의](../ANALYSIS_RULES.md)의 전체 사용 승인 경계, [전략 집계](../strategy-summary.csv)의 all_24/strict_unexposed 행.

## IR02 · 24개 원판 식별과 18개 추가 보강은 같은 뜻이 아니다

24건은 공개 보존 전문·artifact/Message-ID·응답 순서를 연결한 원판 식별 수다. 추가 보강18은 SQLite8의 Fossil artifact, curl8의 Hypermail 서버 수신시각, PostgreSQL P04/P05의 첫 답 인용 대조라는 이질적인 근거다. 보강18과 미노출23의 교집합은 **17**이다. S01은 원판이 보강되었지만 답 문구에 노출된 사례다.

PostgreSQL raw RFC822 Received는 **0/8**이다. P04는 실질 질문 전문이 회신 인용과 일치하고 인사·감사·서명은 생략되었다. P05는 본문 전체가 일치한다. 따라서 추가 보강18 전체를 같은 수준의 원형 서버시각·본문 독립 인증이라고 표현하면 안 된다. 원판 미확인0과 그 양극단이 동일하다는 집계는 연구가 채택한 공개 아카이브 식별 기준 아래에서 성립하며 제출시각의 모든 불확실성을 제거하지 않는다.

최신 SCOPE의 구분은 타당하게 유지되어 있다. 권장 표현은 **“공개 보존 전문·식별·응답순서 연결24, 추가 교차근거18, 답 미노출23”**이다.

근거: [SCOPE](../SCOPE.md)의 원판 증거 단락, [metrics](metrics.json)의 extra_original_corroboration/strict_unexposed/unknown_original_extremes, [PostgreSQL T1 노트](../streams/postgres/notes-t1.md)의 원판 보강, [회신 인용 대조](../streams/postgres/initial-quote-crosschecks.json)의 P04/P05, [SQLite 최초 코딩](../streams/sqlite/initial.jsonl)의 S01.

## IR03 · Q의 엄격 신규 값0은 일반 질문에 대한 답0이 아니다

봉인한 같은 변수의 엄격 신규 값은 **0/24**다. 8개 값은 이미 T0에 있었으며16개는 추가 값이 미확정이다. 동시에 실제 다른 변수에 대한 명확화 왕복7개가 관측된다. 따라서 이 연구가 “아무도 추가 질문에 답하지 않았다”거나 “질문은 쓸모없다”는 결론을 주지는 않는다.

약한 해석3은 C05의 부분 기존 workflow, P03의 `local` 지시대상, S04의 COMMIT 주장과 공개재현 불일치다. S04의 원래 FMDB 앱과 공개 C 재현이 완전히 동일한 실행인지는 미확인이며 작성자의 말이 거짓이라고 단정하지 않는다. **0–3은 코딩 민감도**이고 신뢰구간·질문 효과·채택 효과가 아니다.

기계 집계에서는 주의가 하나 더 필요하다. `analysis.csv`의 S04/C05 `q_value_status=author_existing_fact`는 발화 성격을 남긴 값이다. 이 문자열만으로 확정 신규 회수 수를 계산하지 말고 `q_new_author_value_strict`와 `adjudication_note`를 함께 사용해야 한다. 직접 같은 변수 답 하위집합의 분모0은 **비율 해당 없음**이다.

근거: [analysis](../analysis.csv)의 S04/P03/C05 및 Q 플래그, [metrics](metrics.json)의 weak_author_value_sensitivity/direct_answer_denominator, [보정](../adjudication-overrides.json)의 세 사례, [분석 정의](../ANALYSIS_RULES.md)의 Q 값 회수·판독 오류 구분.

## IR04 · 왕복7+구현1의 범위와 달력시간

주 대화 왕복 **7**은 S01 세 쌍, S04 세 쌍, C07의 설계 대상/목적 한 쌍이다. 기술 입력 질문만으로 좁히면 **6**이다. 별도 구현 C06의 한 쌍까지 더한 서로 다른 왕복은 **8**이다. C06 구현쌍도 실제로30일 안이며 별도90일 구현 열에 배치했다는 사실이31–90일에 발생한 사건을 뜻하지 않는다.

전략별 행은 같은 실제 관측을 공유한다. 따라서 I/C/Q의 실제7을 더해21로 만들지 않는다. S04의 일부 대기구간은 겹치므로 합계를 절감 가능한 달력시간으로 해석하지 않는다. 실제 메시지쌍의 대기, 첫 답 지연, 전체 대화 지속기간은 다른 관측이다. 가상 I/C의 추가 왕복0, Q의 답이 온다는 조건 아래 최소1은 전략을 실제 발송하여 측정한 효과가 아니다.

근거: [실제 왕복](actual-roundtrips.json)의 primary_pairs/implementation_pairs/note, [analysis](../analysis.csv)의 primary/technical_only/implementation 열, [전략 행](../strategy.csv)의 actual_roundtrip_counts_shared_across_strategies, [분석 정의](../ANALYSIS_RULES.md)의 분모·비용·검열.

## IR05 · 행동과 자료의 단위를 합치지 않는다

넓은 진전3은 **S01의 새 자가실행 성공1, C05의 기존 workflow 수용1, C06의 공급자 개발1**이다. 이는 사용자 채택3건이 아니다. 답 문구 노출 S01을 뺀 미노출23에서는 외부 사용자의 새 실행 성공이0이다. S04/S08의 실제 실패는 별도 실제 개입에 대한 보고이며 미전송 I/C의 실패가 아니다.

관측 단위는 다음처럼 보존해야 한다.

| 단위 | 직접 대조한 분해 | 잘못된 대체 해석 |
| --- | --- | --- |
| 원문61저작 | 표집 대화24와 제공자·타 분야 자료 | 독립 사람61·채택61 |
| frame149행 | root심사40=포함24+제외16, 답장metadata87, 상한 뒤22 | 적격 root149 또는 root제외72 |
| followup137행 | 공개 발화114, 개정4, 검열 요약11, 미연결 인접 기록8 | 작성자 응답137 또는 독립 후속 사건137 |

`frame.csv`의 family/decision/reason을 직접 다시 대조했다. `source-counts.json`의 단순 `excluded=72`에는 curl 답장56이 포함된다. 최신 SCOPE의 root40·답장87·상한 뒤22 분해가 맞다. `window-audit.json`의 시각 경계 차이3은 검열 요약 행에 관한 것이며 실제 공개 발화의30일 포함 여부가 바뀐 것으로 세지 않는다.

근거: [analysis](../analysis.csv)의 S01/C05/C06 행동 종류와 S04/S08 실패 범위, [metrics](metrics.json)의 all_24/strict_unexposed counts, [전체 원장](../frame.csv), [자료 수](source-counts.json)의 frame_decisions/definition, [창 점검](window-audit.json)의 record_types/clock_origin_boundary_differences, [SCOPE](../SCOPE.md)의 원장·후속 분해.

## 봉인 보존과 남은 검토

이 검토는 canonical 집계 파일 또는 봉인 입력을 직접 수정하지 않았다. root가 수용한 IR01 변경을 최신 파일에서 재독했으며, 이 요청에 따라 새 검토 기록 두 파일만 작성했다. SQLite 두 봉인 파일의 현재 SHA-256을 다시 계산하여 이전 기록과 같음을 확인했다.

| 파일 | 현재 SHA-256 | 이전 봉인 기록과의 관계 |
| --- | --- | --- |
| streams/sqlite/initial.jsonl | 1135277c1fa579ab0be3a2af784e5d52f6fd3c2faeecb5f21e3537464546ef40 | 동일 |
| streams/sqlite/frozen-responses.jsonl | b49397b7d79d056076c7eb6080f49e4b24faabaaddd518824ae2fe06e4b4d690 | 동일 |

전체24건의 원격 봉인 검증은 별도 `t0-seal` 영수증의 범위다. 이 기록으로 독립 중복 원문판독 또는 인과 검증을 주장하지 않는다. 다음 검토는 최종 RESULT/SELF_CHECK가 위 다섯 경계를 실제 문구와 표에 유지했는지 확인하는 것이다.
