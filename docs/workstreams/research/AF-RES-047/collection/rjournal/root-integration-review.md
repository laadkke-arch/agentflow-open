# Root 통합 원장 정적 검산 1차

**동일 모델의 별도 문맥에서 수행한 static 검토**다. 외부 독립 판독·눈가림 평가·원 과학 실행 재현이 아니다. Root 파일을 수정하지 않았다. 읽은 파일 SHA256, 관측 시각, finding별 위치·영향·최소 수정·검산 방법은 root-integration-review.json에 있다. 검토 중 다른 분담의 원장은 계속 갱신되므로 고정 최종 결과 SHA에 대한 검토는 아니다.

## 결론

핵심 집계는 보수적으로 분리돼 있다. 자연6의 P4/U1/R0/V0, 보강2의 P2/U1/R외부0/R로컬2/V0, 전체의 candidate value1/strict positive0이 원장과 맞는다. 초기 검토의 필수 배당은8/7/7/2/2였다. **22:46 UTC 재확인에서는 root가 RIR-01~03을 수정·재생성했고, RUC 발행자 보존 원문을 추가해31저작·배당8/8/7/2/2·quota-eligible27을 기록했다.** 원 RUC 입력판 확정과 archive capture는 여전히 분리돼 있다. 아래 초기 관측과 수정 경로를 함께 보존한다.

### RIR-01 · 수정 확인 · A/B 다른 열로 C 값이 유입됨

readings.csv의 RUN A/B visible_values는 결측 처리돼 있다. 그러나 scripts/consolidate.py 232행은 모든 구성에 전체 사례의 field·target_time을,245행은 전체 missing_reason을 넣는다.

* RUN02 A/B field: CHROM의 첫 VCF record 설명에 **POS1, END63267, DP0**이 들어 있다. missing_reason에는 **선택 CHROM1**도 들어 있다. primary값1을 visible_values에서 가려도 다른 열에 이미 노출한 상태다.
* RUN01 A/B field에는 **y4096**, target_time에는 정확한 test/preprocess 로그 시각과 v1/v1.1 차이가 있다.
* 해당 구성들의 자체 evidence 설명은 실행 graph/log/HDF5/VCF 내부를 C에 추가한다고 명시한다.

이 행 전체를 A/B 자료 구성으로 읽으면 경계가 깨진다. 현재 점수는 여전히 낮아 낙관 집계가 생긴 것은 아니지만, “A/B에서 안 보이던 것을 C가 추가했다”는 비교에는 영향을 준다.

최소 수정은 packet용 field/time/missingness와 전체 감사 후 맥락을 나누는 것이다. A/B는 “첫 record의 CHROM”, “첫 logical data column coord_x”라는 중립적 기준을 쓰고, 구체 row 값·로그 시각은 C 또는 별도 auditor_context에 둔다. 전체8슬롯 사례표에는 모든 상세를 유지해도 된다. RUN01/RUN02 A/B packet의 모든 열에서63488/4096/CHROM1/END63267/DP0와 C로그시각의 유출을 재검사한다.

### RIR-02 · 수정 확인 · RUN01 nested U의 뜻이 충돌함

Root cases.json의 RUN01.specific_usage는 false이고 readings.usage_specific도 false다. 이는 외부 발행판 U의 올바른 판정이다. 그런데 RUN01.C.specific_usage는 여전히 true이며 이는 local input 선언을 뜻한다. 같은 이름이 JSON 깊이에 따라 다른 의미를 갖는다.

현재 summary의 외부 U1/2는 맞지만, nested C.specific_usage를 읽는 다른 소비자는 U2/2로 잘못 계산할 수 있다. C의 common specific_usage도 external=false로 정규화하고 local_usage_specific=true 및 collection_original=true를 별도로 보존하는 것이 최소 수정이다. RUN02는 external=true/local=true로 남는다.

### RIR-03 · 재생성 확인 · 최신 R Journal fragment 미반영

Root RJ01/RJ02/RJ03 B/C는 최신 collection/rjournal/cases.json보다 이전 값이다. 최신 fragment는 A⊆B⊆C의 URL과 이미 알려진 값을 명시적으로 누적했다. Root의 visible_values는 아직 delta 형태다. 점수 변화는 없으며 재생성 후 일치 확인으로 해결된다. 결측 표시가 C에서 실제 값으로 해소되는 것은 별도 상태 변화로 취급하면 된다.

### RIR-04 · 근거 연결 개선 권고 · 메타데이터 최초 행이 최소수 대표임

W-WOMBAT-run의 최소 산입은 R-FR-ZEN-10091550이라는 catalogue metadata 행에 붙어 있다. 더 뒤의 R-ARCHIVE-wombat-aux는 실제 protein-quantification output을 직접 읽었다고 기록한다. 따라서 현재 증거에서 저작 총수30의 부풀림이 입증된 것은 아니다. 그러나 산입된 행만 보면 실제 사례 원문 배당을 충족하는 강한 열람이 보이지 않고, 요약의 “screening metadata add zero” 설명과 어긋나 보인다.

저작별 qualifying_source_ids로 실제 내용 판독 행을 연결하거나 그 행에 대표 credit을 옮기면 된다. Selected CPM run의 최초 metadata 행도 같은 방식으로 정리할 수 있다. 저작당1개·배당1개 원칙과 집계는 유지한다.

### RIR-05 · 정의 개선 권고 · 전체24와 필수 배당24

현재 minimum24_met는 supplementary4를 포함한 전체30으로 계산하고 quota_eligible_unique_works는26이다. 지금은 둘 다24 이상이므로 숫자 오류는 없다. 그러나 향후 필수 배당의 실제 저작이23개이고 일반 보조문서가 추가돼도 minimum24_met=true가 될 수 있다.

일반 direct24와 과제의 quota-eligible24를 따로 이름 붙이고, 각 배당 충족을 추가 필수 gate로 두는 것이 좋다. 현재 publisher7/8을 all_allocations_met=false로 남긴 것은 올바르다.

## 통과한 축

| 축 | 확인 |
|---|---|
| R_local / 외부 R | 두 실행의 local=true, external=false를 cases/readings/summary에 분리. 원 test와 후대 preprocess의 UUID도 합치지 않음. |
| 외부 U / local 선언 | 집계에서 RUN01 local 선언을 외부 U로 세지 않음. RUN02의 정확한 source URL 선언은 바이트 동등성 미확인과 별도로 인정. RJ02 U는1998의16개 filename 범위. |
| 후보값 / 엄격 V | RJ03 후보 동일필드 계산1은 strictV0과 분리. 저자0/386·출력파일 재독을 독립 V로 올리지 않음. |
| 중복 저작 / 배당 | 산입 work_id 중복과 동일 final URL 중복을 관측하지 않음. CRAN16파일·Iris여러판은 각1저작. supplementary는 부족한 publisher 배당을 채우지 않음. |

최종 RESULT·SELF_CHECK·수용 원장이 만들어지면 이 수정 사항과 마지막 고정 SHA 기준으로 한 번 더 비교할 수 있다.

## 22:46 UTC 후속 확인

Root 수정에서 A/B는 중립 field·time 및 구성별 missing_reason을 사용하고, 상세는 packet에서 제외한다고 명시한 audit_only_* 열로 옮겼다. Nested RUN01.C U도 external=false/local=true로 정규화됐다. R Journal 모든 A/B/C는 최신 fragment와 일치한다. 이 세 가지 실질 finding은 해결됐다.

RUC의 보존된 원 발행자 페이지 S-E060이 추가돼 현재 원장280행·고유31저작·필수역할27저작·배당8/8/7/2/2다. 이는 최초 검토 후의 갱신이며 source-count-summary의 all_allocations_met=true와 맞는다. RIR-04의 qualifying source 연결과 RIR-05의 minimum24 이름 명확화는 낮은 우선순위 권고로 남는다. 현재 수의 부풀림을 입증한 오류는 아니다.
