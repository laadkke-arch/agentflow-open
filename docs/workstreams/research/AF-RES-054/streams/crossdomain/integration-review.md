# 통합 원장 검토 — E01·D01·진단 사례

검토자: `crossdomain_frame` 보조 조사자. 자기 하위 조사 자료와 root 통합 결과를 대조한 **통합 정확성 검토**이며, 연구 전반의 독립 재현 심사라고 부르지 않는다.

검토 시각: 2026-11-23T02:05:22.783547+00:00. 부모가 알려 준 원격 묶음② SHA는 `de1e2b9b0110e1713715e932849d2b9a5c5e1b99`다. 아래 검토는 당시 작업 디렉터리의 여섯 통합 파일을 읽은 것이며, 그 파일들이 위 원격 SHA와 바이트 단위로 같다고 별도 확인한 것은 아니다. 원 파일 수정은 하지 않았다.

## 범위와 판정

`frame.csv`, `endpoints.csv`, `joins.csv`, `bounds.csv`, `evidence/source-counts.json`, `evidence/study-register.json`에서 E01·D01·Pillai 진단 DX-E02·Mathur CAD 진단 DX-D02를 검토했다. 비교 입력은 `streams/crossdomain/`의 선정 고정판, 연구·종점·결합·경계 JSON, 실제 SAV/CSV 집계와 source 원장이다. 본 검토에서 외부 원문을 새로 읽거나 새 저작 수를 추가하지 않았다.

**핵심 분모와 표본의 잘못된 합산은 발견하지 않았다.** E01의 배정 N은 미확인, 공개 분석 N은231로 분리되어 있고, 58/58/57/58 네 셀이 맞다. Pillai의112행 분석 파일 결합을143명 모집 대장 결합으로 승격하지 않았다. D01은 빈 자리로 유지되며 Mathur가 대신 들어가지 않았다. E01에는 이진 통과선·공동 성공·효과 구간을 만들어 넣지 않았다.

저작 수도 적절하게 구분되어 있다. Bichler 논문은 `doi:10.1037/edu0000433`으로 한 번, SAV는 `osf:tquh3-data`로 한 번 세었다. Pillai의 CSV·전략·prompts·사전계획은 `osf:85tye-package` 하나이며 별도 intervention 또는 prereg quota로 늘리지 않았다. Pillai·Mathur 원논문은 `additional_primary`로 분류되어 새 선정 자리를 채우지 않는다. `unique_counted_primary_works=23`과 `full_requirement_status=부분 충족`은 서로 모순되지 않는다. 엄격 새 논문4/6에는 Casdoc의 후속 적격 실패가 주석으로 명시되어 있으므로, 이4를 “적격 비교 연구4개”라고 바꿔 서술하지 않아야 한다.

## 필요한 수정

| 우선순위 | 파일·행 또는 ID | 현재 상태와 문제 | root 수정 제안 | 직접 대조 근거 |
| --- | --- | --- | --- | --- |
| 높음 | `endpoints.csv` 행17, `E01-final`, `missing_or_withdrawal` | 값 `0`은 `score_missing_analyzed=0`에서 왔지만 통합 열 이름은 철회·결측 전체를 포함한다. 이를 배정군의 결측/철회0으로 읽을 수 있다. | `분석231행의 KPost 결측0; 원래 배정에서 제외·철회 수 미확인`으로 분모와 변수를 써 준다. 원래 배정 결측을0으로 표시하지 않는다. | `endpoints.json` E01-final, `studies.json` denominator_warning, `joins.json` CD-J01 |
| 중간 | `endpoints.csv` 행19, `DX-E02-immediate-delayed` | `N_definition`과 `classification`이 미확인으로 평탄화되어, 이미 확보한 모집143·분석112 및 진단 표본 밖 상태가 `details_json` 안에만 남았다. | `N_definition=모집/참여143; 분석112(Comparison38,Sequential39,Correct35); 원배정·제외 대장 미확보`와 `classification=선정8자리 밖 진단 사례`를 명시한다. 모집143을 확인된 무작위 배정143으로 바꾸지 않는다. | `endpoints.json` DX-E02, `pillai-analysis-aggregate.json`, CD-P02/ CD-D02-A |
| 중간 | `endpoints.csv` 행20, `DX-D02-CAD` | `N_definition=6`만으로는 행의 unit인 `person×interface×design/query`와 수의 단위가 다르다. 같은6명의 교차 수행 및 훈련1200초가 정규 열에서 사라졌다. | `N_definition=사람6; 같은 사람이 두 인터페이스 수행; 질의 시도/정답 분모 미확인`, `training=20분 tutorial/feedback`, `classification=선정8자리 밖 진단 사례`로 명시한다. | `endpoints.json` DX-D02, CD-P03 §5.3/AppendixF |
| 중간 | `bounds.csv` 행29–30, `E01-DIFF-T0/T1` | 두 행의 `condition_or_contrast`가 똑같이 `worked examples − problem solving`이고 분석 분모 열도 미확인이다. 압박 strata와 이미 확인한 분석 N 쌍이 ID/details 밖에 보이지 않는다. | T0에는 `압박 없음: 풀이 예제−문제풀이; 분석57/58`, T1에는 `압박 있음: 풀이 예제−문제풀이; 분석58/58`을 표시한다. 배정 N과 효과 경계는 계속 미확인이다. | `bounds.json` pressure, N_T_analyzed, N_C_analyzed; `bichler-analysis-aggregate.json` |
| 중간 | `frame.csv` 행76, `SLOT-E01`; 행37, `CD-F004` | 실제 metadata 행에는 DOI·2019-12월·대체2020-10월이 있지만 필수 자리 행은 publication/permanent ID가 모두 미확인이고, 본문 열람 후 상태도 미확인이다. 서로 모순되는 날짜를 새로 만든 것은 아니지만 자리→근거 대응에서 확인한 정보를 잃었다. | SLOT-E01에 DOI와 `2019-12(저자 metadata, 월 정밀도); 대체2020-10(Crossref/LMU)`를 연결한다. post-fulltext 상태는 `231개 분석행 확보; 배정 원장/시각/원래 이진 통과 기준 미확인`으로 쓴다. 최초 선정 snapshot의 판단은 고치지 않는다. | `selection.json`, `frame.json` CD-F004, `studies.json` E01 |

### 시간 열의 해석을 유지할 것

`endpoints.csv` 행17의 `deadline_seconds=2100`은 열람 원고의 **약35분 검사 시간**이다. 현재 `clock_limit`에 approximate 설명이 있어 정확한 강제 마감이나 제출 시각이 확인되었다고 계산한 증거는 없다. 다만 생성기가 `deadline_seconds`만 읽어 엄격한 초 단위 마감으로 재사용한다면 오류가 되므로, 정규 열을 `미확인`으로 두고 약2100초를 계획/설명 열로 옮기거나 `deadline_seconds`가 명목 시간도 포함한다는 구분 필드를 붙여야 한다. 45분 연습과35분 최종 검사를 하나의 시간 창으로 합치지 않는다.

### 판과 quota 문구의 해석을 유지할 것

E01의4.75 대4.5733 불일치는 **읽은54쪽 저자 원고와2021년 SAV 판**의 불일치다. 최종 출판본의 확정 오류라는 문장은 이 여섯 통합 파일에서 발견하지 않았으며 앞으로도 그렇게 확대하지 않아야 한다. 원고가 최종 발행본이 아니라는 source 한계를 유지한다.

`strict_allocation.new_original_papers_selected_slots.observed=4`는 “새 자리에서 읽은 원논문4편”이다. 같은 객체 주석대로 원문 확인 후 배정 비교가 남는 연구는3개이고, Casdoc은 선정 lead를 유지한 실패 사례다. `all_new_original_papers_read_including_diagnostics=8`을 선정6자리 충족으로 바꾸면 안 된다. 현재는 이런 확대가 없으므로 source-count 수치 자체의 변경은 요청하지 않는다.

## 검토한 로컬 파일 해시

| 파일 | SHA256 |
| --- | --- |
| frame.csv | `23a8188d48948991f46c5c29fa315869193ec2ca7d71452aacbacf7a9e9c87a3` |
| endpoints.csv | `aa7d7b6d0216a994deac4a5117d697429a14f04a7b1ecc2aaa4c2adb6482e7db` |
| joins.csv | `747939991e5a3154680f2ccc80d3f2ae5bebb849d1ce3b7d68107f35e24c0113` |
| bounds.csv | `3a724d5c2261d213f9533494585e4f01edf78316056f358c0866046ffd8fb55d` |
| evidence/source-counts.json | `834b9c222ad8747a68e1c9d8257ac4e55848bc70c0a110d496c98433c123fe0c` |
| evidence/study-register.json | `066c9e1d434e639e5091640ae24c720105985867f591fcaab08d0e0d52c7972a` |

원장 수정과 이후 재생성은 root가 수행한다. 위 제안을 실제 반영·재검사했다고 이 검토 문서에서 주장하지 않는다.
