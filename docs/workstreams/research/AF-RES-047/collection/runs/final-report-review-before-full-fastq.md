# AF-RES-047 실행층 최종 보고 검토

## 범위와 독립성

`RESULT.md`, `contradictions.md`, `readings.csv`에서 CPM/Wetlab 및 두 AUX의 수치·실행 ID·판 차이, U_external/R_local/V, A/B 표시 범위를 검토했다. 같은 모델의 별도 검토 문맥이며 원 실행층 조사 담당자의 재판독이다. **외부 독립 판독이나 맹검은 아니다.** root 파일은 수정하지 않았다. 검토 시각·원본 파일 SHA256·각 근거는 `final-report-review.json`에 있다.

## 판단

핵심 RUN 수치·UUID·분모 오류는 찾지 못했다. C에서 P2/2, U_external1/2, U_local2/2, R_local2/2, R_external0/2, strict V0/2와 기록 재독2/2가 원장과 맞는다. CPM 소비 archive의 판 비교를 외부 발행판 비교로 바꾸지 않았고, Wetlab prefix 일치를 전체 FASTQ 동일/정정 성공으로 승격하지 않았다. AUX LivePublication/WOMBAT는 핵심 분모에서 분리됐다.

초기 검토에서 아래 두 중간 우선순위 지적을 전달했고 부모는 생성 스크립트에 반영했다고 응답했다. 실제 재생성 파일 확인 전에는 해결 완료로 단정하지 않는다.

| ID | 최초 관측 | 영향·권고 | 상태 |
|---|---|---|---|
| RUN-REVIEW-01 | RUN02 A/B `purpose`에 chromosome1 gVCF가 표시되지만 C의 새 값은 CHROM=1이다. `visible_values`는 잘 가려졌어도 목적 parameter로 같은 답이 미리 보인다. | A/B는 공개 variant-calling 목적만 남기고 전체 목적은 `audit_only_full_purpose`로 옮긴다. 목적 parameter와 실제 출력값 재독을 분리하면 C−B의 정보 증가를 과장하지 않는다. strict V0 집계는 변하지 않는다. | 부모가 `scripts/consolidate.py` packet_purpose 수정 보고; 재생성 확인 대기 |
| RUN-REVIEW-02 | RUN01 A/B `target_time`의 v1.1 release2023-06-29는 API의 created 날짜다. 두 판의 publication_date는 모두2023-02-25다. | publication_date와 record created를 정확히 분리하고 최초 공개일로 추정하지 않는다. | 부모가 `scripts/consolidate.py` target_time 수정 보고; 재생성 확인 대기 |
| RUN-REVIEW-03 | RUN01/02 C의 `C_slot_status`는 실제 C 존재 상태 대신 absent run 일반 경고 문구다. | `present: archive graph/log/output directly inspected; external linkage unconfirmed`처럼 보유 상태를 명시하면 결측 C와 혼동하지 않는다. | 낮은 우선순위 명료화 권고 |
| RUN-REVIEW-04 | 설명에서 test.log라는 약칭을 쓰지만 정확한 archive member는 prov_test.log다. 정확 주소 칸에는 제대로 적혀 있다. | 파일 이름으로 제시할 때 prov_test.log로 통일한다. 사실·판정·집계에는 영향이 없다. | 낮은 우선순위 명료화 권고 |

## 직접 대조한 주요 근거

- `cpm-logical-column-order.json`과 HDF5 inspection: coord_x63488/y4096, 물리 block의 is_cancer와 구별.
- 두 CPM metadata와 test/preprocess logs: 원 test ID는 같고 preprocess ID·시각은 다름. v1.1 preprocess가 원 test 뒤라는 한계를 유지.
- 두 Wetlab metadata: archive action bdfcc6a4…/collection dcc0e6bb…와 GitHub action2f5723c2…를 별도 graph로 유지.
- `wetlab-vcf-inspection.json`, stdout line6, stderr cutadapt 명령 lines80–108 및 BWA lines255–285: 같은 보관물 안의 input/output 실행 선언과 checksum. 독립 계보 증명이 아님.
- `wetlab-fastq-prefix-comparison.json`: archive487611787/publisher413005346바이트, 첫20 decoded records의 제한된 동일성.
- `cpm-edition-comparison.json`과 `cpm-input-edition-comparison.json`: 동일 prediction/test log, 바뀐 input bytes/preprocess, 검사한33 arrays 내용 동일. 전체 metadata-only 변경으로 단정하지 않은 문장이 적절함.
- `auxiliary-evidence.json`: WOMBAT 실제 action·RAW/FASTA·40행 protein output; LivePublication 외부 원입력 정체 결측. core 표본/strict V로 전용하지 않음.

고정 URL·같은 바이트·특정 실행의 실제 미사용을 동시에 확인한 음성례는 여전히 미충족으로 정확히 표시됐다. 독립 strict V를 늘릴 근거를 이번 재판독에서 새로 발견하지 않았다.

## 재생성 확인

최종 확인 결과는 JSON의 `final_recheck`와 이 절에 추가한다. 외부 원문 최소수를 추가하거나 원 실행을 재실행한 검토는 아니다.

### 실제 재생성 재확인

2026-11-22T23:00:40.757272+00:00에 root `readings.csv`의 RUN01/02 A/B 네 행을 다시 읽었다. RUN-REVIEW-01은 RUN02 visible purpose에서 chromosome1이 제거되고 audit_only_full_purpose에 보존되어 해결됐다. RUN-REVIEW-02는 두 판의 metadata publication_date=2023-02-25와 v1.1 record created=2023-06-29가 분리되어 해결됐다. 초기 지적과 원 snapshot SHA는 그대로 보존했다. 새로운 root 파일 SHA는 JSON final_recheck에 있다. 낮은 우선순위 명료화 두 건만 권고로 남고, strict V/R_external 집계는 변하지 않는다.

추가 확인: RUN-REVIEW-03의 두 C_slot_status도 실제 local 실행 기록 보유와 외부 연결 결측을 명시하도록 수정되어 해결됐다. RUN-REVIEW-04의 남은 약칭 위치는 JSON remaining_exact_locations에만 남겼으며 판정/집계에는 영향이 없다.
