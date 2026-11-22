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


## R-A07 / root A10 — 전체 FASTQ 비교가 바꾼 입력 연결

최초 prefix 검사는 두 gzip의 첫20 records만 확인했다. 부모가 전체 비교를 요청하여 `python -B docs/workstreams/research/AF-RES-047/collection/runs/verify_full_fastq.py --perform`를2026-11-22T23:00:16Z–23:09:38Z에 실행했다. 약0.9GB 입력을 스트리밍했고 전체 파일 복사본을 저장하지 않았다. 실행 당시 원본과 SHA `a94b06e7c85b4c3aa69e010edde97f7a3f7ce88e5026d18b415c4d5c8ba6bb3a`를 별도 snapshot/receipt에 보존했다.

전체 archive R1 SHA256은 같은 archive File 선언과 같았다. 실측 archived gzip MD5 `52f3ed344d88278c703faa1280818ce1`은 독립 NIST `HG001-part2.md5` **388행**의 정확 full flow-cell/R1 경로와 일치했다. 현재 served gzip MD5 `24ba6bb88db052d4bf64ac98131d6005`는 목록과 다르지만 두 객체의 완전 decoded1409966879bytes/SHA256은 같다. 목록의 전체 SHA는 최초 열람과 동일했고, 동명 다른 flow-cell의116/254행은 다른 MD5였다.

따라서 현재 publisher gzip의 byte mismatch만으로 원 실행의 외부 입력 연결을 보류한 초기 판단을 수정했다. user/SCOPE는 당대 runID+input 명세/당사자 구체 기록을 허용하므로 별도 machine-I/O 영수증을 필수로 추가하지 않는다. 같은 Zenodo archive의 action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`만 R_external=1로 올렸다. GitHub의 다른 UUID는0을 유지한다. raw FASTQ에 없는 CHROM output의 독립 재계산은 없으므로 V=0이다.

| 항목 | 원래 | 수정 후 | 보존/근거 |
|---|---|---|---|
| 보강 R_external |0/2|1/2 (RUN02 selected Zenodo action)|cases/readings/runs/summary before-full-fastq snapshots; full comparison+publisher manifest+same archive graph|
| 보강 V 및 V 조건부 R |0/2; 해당 없음(분모0)|0/2;0/1|선정 CHROM을 다른 필드로 바꾸지 않음|
| P / U_external / R_local |2/2 /1/2 /2/2|동일|사용 선언/지역 연결을 별도로 유지|
| 객체 표현 |current gzip bytes mismatch; prefix20 같음|current gzip bytes mismatch 유지; publisher-declared representation match=true; full decoded content match=true|wetlab-full-fastq-interpretation.json|
| source 기록/최소수 |87행/8저작|90행/8저작|새 직접 열람3행 모두 count0; 원 publisher/consumer 같은 저작|

`cases-before-full-fastq.json`, 각 CSV·summary·sources·findings의 같은 접미사 snapshot과 기존 prefix evidence를 보존했다. `publisher-focused-fields.json`의 초기 suffix filter는 BSD MD5(path)=digest 형식에서 빈 목록을 만들었지만 이전 원 source receipt는 세 matching line을 보존하고 있었다. 재독 후116/254/388행을 정확히 연결했으며 이 수정도 숨기지 않는다. 표본·선정 순서·고정 CHROM 필드는 바꾸지 않았다.
