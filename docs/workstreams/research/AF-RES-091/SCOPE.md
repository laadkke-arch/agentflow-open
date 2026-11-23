# AF-RES-091 #1 · 입력과 판정 계약

## 시작판과 선행판

저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-091`, 허용 경로 `docs/workstreams/research/AF-RES-091/`다. 계획판 `62a80b9f111c695527a8ca87bcb867796d2e96bb`에는 091 행이 아직 없었다. GitHub에서 작업 브랜치 부재와 통합 `f10c81baa98d9bad0407c9af8b4fa91cf9b70f6e`의 RUNNING 행을 확인하고 생성했다. 계약 fetch 때 통합이 `c2709abf8d25163eed75a7553ebcbde966105b55`로 전진했다. 그 변화는 중앙표의 다른 배정 행이었다. 입력 작업 전에 빈 작업 브랜치를 해당 통합판으로 fast-forward하고 그 SHA에서 계약을 다시 생성했다. [고정 통합판](https://github.com/laadkke-arch/agentflow-open/tree/c2709abf8d25163eed75a7553ebcbde966105b55) · [진행표](https://github.com/laadkke-arch/agentflow-open/blob/c2709abf8d25163eed75a7553ebcbde966105b55/docs/automation/dot-control.json) · [계약](manifest.json).

실제 시작판의 AGENTS, STATE, START_HERE, DOT_AUTOMATION, 연구 브리프·운영 규칙 및 중앙표의 091·087 행을 읽었다. 091의 유일한 직접 의존은 DONE인 087의 인계 `36a76b384810730b7d819a5ed469e6e8ded92f8a`다. 087 결과판 `263fe7581cf45eadd1f05139aacaadb27290b86e`의 RESULT, environments, mixed_types, G-WKB/G-native, reproduce, requirements와 설치 영수증을 인수했다. G에서 N의 WKB는 두 원 타입을 복원했고, N의 native는 두 행의 2D 위상을 유지하면서 한 행을 MultiPoint로 바꿨다. G의 원 MultiPoint는 좌표 두 개였다. 이번 B는 좌표 한 개다. [087 인계](https://github.com/laadkke-arch/agentflow-open/blob/36a76b384810730b7d819a5ed469e6e8ded92f8a/docs/workstreams/research/AF-RES-087/HANDOFF.md) · [087 고정 결과·원 파일](https://github.com/laadkke-arch/agentflow-open/tree/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087).

## 수작업 정답

| 입력 | 원 A | 원 B | 원 N · E | T 기대 ID/score | P 기대 ID/score |
|---|---|---|---|---|---|---|
| S0 | Point (117,23) | Point (2,7) | None · POINT EMPTY | A/101, B/NA | A/101 |
| S1 | Point (117,23) | MultiPoint ((2,7)) | None · POINT EMPTY | A/101 | A/101 |
| S2 | Point Z (117,23,135.25) | MultiPoint Z ((2,7,−42.5)) | None · POINT EMPTY | A/101 | A/101 |
| S3 | Point Z (117,23,135.25) | MultiPoint ((2,7)) | None · POINT EMPTY | A/101 | A/101 |

모든 입력의 ID 순서는 A, B, N, E다. nullable `Int64` 속성 `score`는 각각 101, NA, −3, 0이다. N은 결측, E는 존재하는 빈 Point다. EPSG:4326에서 순서는 x/y(경/위도)다. 고정 사각형 [110,20,120,25]는 A를 내부에 두고 B를 외부에 둔다. B를 포함하는 대조 사각형은 실행 격자에 추가하지 않는다. 높이 두 값과 score는 연구자가 정한 합성 입력이다. [입력 JSON](fixtures/inputs.json) · [통제식](fixtures/model.py).

유효·비결측·비어 있지 않은 행에서 T는 `geom_type == "Point"`의 정확한 단수 타입을, P는 `intersects(box(110, 20, 120, 25))`를 평가한다. 두 결과는 ID순이며 score의 null도 보존한다. 지시문의 “두 연산이 같은 답인 S0”는 그대로는 좌표·술어와 모순된다. S0에서 T는 A와 B, P는 A다. 각 술어의 정답이 두 인코딩에서 유지되는지 비교한다. 원 T와 P가 서로 같은 입력은 S1–S3이다.

## 쓰기·읽기와 예상 반례

- N은 GeoPandas 1.0.0 `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1` 소스이며 087 N과 동일한 파일명·SHA-256의 휠을 사용한다. WKB와 geoarrow 한 옵션만 바꾼다. 고정 옵션은 GeoParquet 1.1.0, Parquet 2.6, Snappy, index 제외, covering 제외다.
- 네 논리 입력의 8 쓰기 자리와 자리당 두 독립 reader 프로세스 16자리, 반복 번호별 8 대응쌍을 모집한다. writer 실패가 있으면 해당 경로와 원 예외를 봉인한다. 이때 두 reader 자리는 실행 불가로 기록하며 실제 파일 reader와 집계에서 구분한다. writer 전에 원 행의 WKT·WKB·XY·차원·Z·결측/빈 상태와 원 T/P를 수작업 기대와 검산한다.
- 사전 예상은 WKB 네 셀에서 원 타입·좌표·차원·Z를 보존하고 S0 native에서도 두 술어가 유지된다는 것이다. S1 native에서 A가 MultiPoint로 올라가면 T에서 A가 빠지고 P는 A를 유지할 수 있다. E의 타입은 별도로 검사한다. S2는 유효한 두 Z가 유지될 수 있고, S3는 writer 거절 또는 숫자형 Z 필드의 NaN 같은 다른 표현이 생길 수 있다. S2와 S3에서 비교해야 할 Z는 위상 비교에 포함시키지 않는다.
- file SHA, 복원 여부, 읽기 반복 안정성, XY 벡터/2D 위상, 정확 타입, 차원과 Z, CRS, None/EMPTY, 속성 및 질의 출력은 별도 비교축이다. 파일 단위 결측과 행 단위 결측은 구별한다. 분모 0은 산출 불가다.
- 087 기본 16회, 원 시험 48개, 옛 GDAL 생성·옛 reader 거절과 전체 의존판 탐색은 인수 범위다. 공개 프로젝트 코드는 소비 사례이며 해당 프로젝트의 역사적 배포 파일·호출 환경이나 087 링크로 인한 장애는 미확인이다. 고정판 호출·입력·기대값을 조사하고 외부 실행과 통제식을 별도로 표시한다. 표 데이터와 팔레트의 손실 허용 사례는 주 16자리에 합산하지 않는다.
