# QGIS Stage 3 공식 동작 판독

Stage 2 원격 봉인 `4a4aae107be25f71318dbb0c7b7cfa73506c5030` 확인 시각 2026-11-24T00:04:06Z 뒤에만 열었다. 마지막 근거 묶음 작성 시각은 2026-11-24T00:30:53.193619+00:00이다. 공식 QGIS 구현 4개, 서로 다른 상류 시험 2개, 추가 spdep 원 자료 2개를 직접 읽어 외부 고유자료 8개를 기록했다. 실제 취득 URL, UTC, commit, 구간 및 SHA-256은 `sources-part.jsonl`에 있다. 원문 전체는 무시되는 캐시에만 보관한다.

## 판과 증거 층위

QGIS 역사판은 `final-3_34_0` → `ffbdd678812eec460ff02ff73bd36ee7955ac8a5`이고 spdep은 `46c90789e61affa495e1b9139442f4416dc7e7af`의 DESCRIPTION에서 1.3-2를 확인했다. 둘 다 제안 이전 이용 가능한 판이지만 작성자나 답변자의 설치판으로 대체하지 않는다. 원 질문 네 건과 제안자의 실제 판은 미확인이다. QG-T1의 reprex 2.0.2 표시는 R/spdep 버전이 아니다.

상류 시험은 코드의 입력과 기대출력을 읽은 D2이다. C++ 표현식 시험과 Python GDAL 처리 시험은 다른 파일이다. 한 파일 안 BuildVrt/Warp 절을 두 개로 세지 않았다. GDAL 시험의 출력은 명령 문자열이다. 픽셀 결과를 읽거나 그 상류 스위트를 실행한 것처럼 기술하지 않았다.

봉인 전 독립 검토에서 GDAL 시험 구간의 함수 이름을 거꾸로 붙인 위치 표기를 발견해 원문을 다시 읽고 수정했다. testWarp는 L1948에서 시작하고 해상도 10.0 기대 명령은 L2078-L2087이다. testBuildVrt는 L2740에서 시작하고 기본 -separate는 L2747-L2757, SEPARATE=False는 L2769-L2779이다. 실제 입력/기대 명령 판독은 유지하며 출처 위치를 바로잡았다.

별도의 작은 합성 실행 D3은 QGIS 3.40.6, GDAL 3.10.3, /usr/bin/python3에서 수행했다. 반복 라벨은 같은 ROAD 텍스트를 다섯 번 배치했다. 그룹별 Show label 조건은 네 피처를 보존하면서 A/B 각 하나를 남겼고, 배치만으로는 떨어진 A의 중복이 남았다. 이는 다른 입력/현재판의 반례이며 원 사용자 실행이나 인지로 승격하지 않는다. 원 데이터와 옛 환경은 복원하지 않았다.

## 취득 및 실행 실패

추정한 GdalAlgorithmsTest.py는 실제 HTTP 404였다. 고정 commit 디렉터리를 읽어 GdalAlgorithmsRasterTest.py로 수정했고 실패 기록은 그대로 남겼다. 첫 native 실행은 존재하지 않는 OffsetFromPoint enum 속성으로 중단되었다. 로컬 API가 제공하는 Qgis.LabelPlacement.OverPoint로 고쳐 두 번째 실행은 exit 0이었다. AF_NETLINK 권한 경고 다섯 개도 삭제하지 않았고, 완료 실행의 렌더 오류 목록은 비어 있다. 실패 시도는 성공으로 세지 않는다. R/Rscript가 없어 spdep은 문서/구현 판독에 머물렀다.

## 재현

`/usr/bin/python3 -B docs/workstreams/research/AF-RES-105/evidence/qgis-official/native_probe.py`는 설치된 QGIS 환경에서 작은 합성 probe를 다시 실행한다. 결과 파일은 갱신되므로 봉인 결과를 검토할 때에는 저장된 실행 영수증/해시와 구분한다. 파일에는 원 입력, 기대 기능 검사, 관측한 라벨 문자열과 피처 ID, 버전, 캐시 이미지 해시가 있다. 추가 자동 발견 세션을 수행한 것은 아니다.

선택한 네 최초 제안과 초기/제안 봉인 파일은 수정하지 않았다. root 소유 통합 CSV 및 git 작업은 수행하지 않았다.
