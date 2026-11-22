# 실행 보강 조사 변경 원장

이 파일은 관측 뒤 정리·수정한 부분을 보존한다. 사전 규칙은 상위 `SCOPE.md`의 원격 봉인 SHA `5c75f3571ab8473f3fba72d92a70bd201c0cf189`이다. 이 하위 디렉터리는 별도 커밋하지 않았으며 통합 담당자가 묶음에 포함한다.

| 변경 | 원본과 이유 | 영향받는 행 | 원래 집계와 수정 집계 |
|---|---|---|---|
| R-A01 목록의 연결된 예제 디렉터리 확장 | 최초 `frame-metadata-frozen.csv`의 19 노출 중 기간 내 14개였다. SCOPE §3가 허용한 출발 목록의 GitHub examples 링크에서 추가 19 metadata를 읽어 총 38 노출, 기간 내 31개를 보존했다. `metadata-freeze.json`과 최초 프레임은 남겼다. | `frame-expanded-all.csv`, `frame-first30.csv`; 원본 API/경로 순서는 `catalogue-links.json`, `repository-example-tree.json` | 최초14를30으로 가장하지 않았다. 추가 디렉터리에서 앞선 Promort는 비공개 입력, BackTrackBB는 합성 입력이다. RUN01은 첫 적격 후보로 유지되고 RUN02는 확장 프레임의 Wetlab이다. LivePublication의 앞선 적격 여부는 계속 미확인이다. |
| R-A02 first named field의 물리 블록/논리 열 구분 | HDF5의 첫 물리 블록 `is_cancer=False`를 처음 읽었다. 그러나 사전 규칙은 첫 **이름 있는 표 필드**이며 pandas `non_index_axes`가 보존한 원래 논리 열 순서는 `coord_x,coord_y,annot_coverage,is_cancer,...`이다. 따라서 핵심 필드를 `coord_x=63488`로 바로잡았다. `cpm-logical-column-order.json`과 최초 primitive inspection을 모두 남겼다. | RUN01 consumers/cases/readings; `is_cancer=False`는 대안 필드로만 보존 | 수정 전후 strict V=0/1이며 후보판 값 일치로 승격하지 않는다. `coord_x`는 polygon vertex와 같은 필드가 아니다. 상위 변경 원장 A06에도 연결된다. |
| R-A03 사용 선언의 외부/지역 범위 분리 | 초기 specific_usage는 구체 local input 선언을 의미하여2/2였다. 통합 U는 외부 발행판/파일 지목이므로 `specific_usage_external`과 `specific_usage_local`을 추가했다. | RUN01 external=false/local=true; RUN02 external=true/local=true | 원래 local U=2/2를 보존, 외부 U=1/2. R_record_local=2/2, R_canonical_publisher=0/2, strict V=0/2 그대로다. |
| R-A04 기록별 실행 ID 분리 | Wetlab GitHub export와 Zenodo archive가 다른 action/collection UUID를 가진다. CPM v1/v1.1에도 서로 다른 preprocess가 있다. 같은 시작·종료시각이나 output hash만으로 여러 graph를 한 실행 영수증으로 합칠 수 없다. | `runs.csv`를6행으로 분리; Wetlab 핵심 C는 archive 내부 UUID만 사용 | 사례 분모2는 그대로. 지역 실행 연결2/2는 보존하지만 외부 발행판 연결0/2는 유지한다. |
| R-A05 첫 열람과 재열람 시각 구별 | 웹 원문4건의22:32:58은 tool clock 직후 실제 재열람 배치 시작이다. 첫 열람 초를 보존하지 못한 행은 `opened_utc=null`, `first_opened_utc=null`, `checked_utc`/`reopened_batch_started_utc`와 설명으로 바꿨다. | R-CATALOGUE, R-PAPER-WRROC, R-CAM-PAPER, R-LIVEPUB-REPORT; 별도 Live article/AWS는 정확초 미확인 | 직접 원문 열람 사실과 최소수는 그대로, 추정한 최초 UTC는 제거. HTTP range/API의 실제 요청 UTC는 그대로다. |
| R-A06 날짜 동률의 식별자 순 | 메타데이터 날짜에 시각이 붙은 행을 시각까지 정렬했던 원본을 `*-before-day-tie.csv`로 남기고 발행 **일** + 공개 identifier로 재정렬했다. 원본 timestamp 열은 삭제하지 않았다. `frame-day-tie-amendment.json` 참조. | 프레임7–8위,19–24위 | 첫30의 구성, RUN01=5위, RUN02=18위 불변. P2, U_local2, U_external1, R_local2, R_publisher0, V0 모두 불변. |

판과 사용을 확인하지 못한 결과를 성과가 좋은 다른 사례로 교체한 변경은 없다. 최초 배정의 목적·값 선택 규칙은 별도 `RUN01-selection-freeze.json`, `RUN02-selection-freeze.json`에 있으며 후속 값 대조가 성공했는지와 분리된다.
