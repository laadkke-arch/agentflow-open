# AF-RES-239 실행 전 고정

## 착수 근거

2026-11-24 22:58–23:00 UTC에 GitHub 통합 첫 조회 및 재조회. 시작 `64e139f16309e41e30f9ec634eabe17fef908bbd`에서 `work/research-af-res-239`를 만든다. 명시된 계획판 `914dbfa789ebec97063ed97130ea2a71c2e9f503` 자체에는 AF-RES-239 행이 없다. 5개 뒤 커밋의 차이는 `docs/automation/dot-control.json` 한 파일(+308/-9)이며 `b4cf83f`가 47차 AF-RES-239 행을 추가했고 `64e139f`가 RUNNING/attempt 1로 전환했다. AF-RES-239의 직접 의존은 AF-RES-221 하나이며 해당 행과 결과 SHA는 계획판과 시작판에서 같다. 독립적으로 고정된 배열, 수준, 예측의 변경은 관측하지 않았다. [계획→착수 diff](https://github.com/laadkke-arch/agentflow-open/compare/914dbfa789ebec97063ed97130ea2a71c2e9f503...64e139f16309e41e30f9ec634eabe17fef908bbd)

통합판 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW 및 239·221 진척 행, 실행·협업 절차, 제품 브리프·프로토콜을 확인했다. 221은 중앙 DONE이면서 [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/78a561e00cb9130430bdee7b5c053f740122e973/docs/workstreams/research/AF-RES-221/HANDOFF.md)에서는 PARTIAL이다. 221의 직접 열람·정적 비교와 실행 0·독립 정답 0이라는 자체 판정을 유지한다. 221의 HANDOFF, RESULT, inputs.csv, predictions.csv, I_FREEZE.csv를 그 SHA에서 직접 읽었다. 세 CSV 원본을 [baseline](baseline/)에 바이트 그대로 보존한다. `session.json`은 `workbench.session start … --fetch` 결과에 작업 브랜치 조회값을 붙인 것이다. 공통 검사에서 해석하는 통합 브랜치·허용 경로·의존 SHA 필드는 생성값 그대로다.

## 모집과 제외

- 일곱 고정 입력은 221의 다섯 수치 통제 C1–C5와 원시험의 R1/R2. C1–C5는 2×2 전체, R1/R2는 원래 8×8/7×7 격자 전체를 호출하고 선택 quad는 (r0,c0)=(0,0)이다. R1은 221 인계 재생의 float32와 L 교집합 11개 0, R2는 float64와 고정 격자를 사용한다. R1/R2의 수준은 0.5, 나머지는 0.
- 두 엔진은 scikit-image 0.25.2 `find_contours`, ContourPy 1.3.3 `contour_generator(name="serial").lines`. 기본 28회는 일곱 입력×두 엔진×두 새 프로세스다. scikit-image 기본 옵션은 생략하고 ContourPy는 `name`만 지정한다. R1 `positive_orientation="high"`와 R2 `line_type` 원시험의 동적 변환 비교는 원형 재생에 분리한다. 공통 CPU/OS·NumPy 버전은 이번 실행판의 선택이며 221에는 실행/설치 환경 지문이 없다.
- 사전 등록 통제는 `inputs.json`의 13가지 변경 시나리오다. 양 엔진 대상 10가지와 엔진 지정 3가지로 23개 API 호출을 계획한다. 원시험과 깨끗한 환경 재생을 별도 기록한다. 보간 모델 비교는 오직 표준화한 선택 quad의 네 변과 그 안의 연결에 해당한다.
- 직접 읽는 원저작의 하한은 22개로 고정한다. 221 입력·예측·분석 3, scikit-image 태그 구현·시험·API 계약/배포 5, ContourPy 동종 5, bilinear·모호면 원논문과 후속 연구 4, 지형/디지털 영상 규칙과 원예 5. 성공한 다른 저작만 합산하며 같은 논문의 판형·검색 결과·접속 실패는 별도 행으로 남긴다. 같은 코드나 실험에서 파생한 자료, 동일 입력의 반복, 원형 대비 상대 시험은 별개 검증 사건으로 합산하지 않는다.
- AF-RES-227–229의 결과, 다른 알고리즘의 기본값 일반화, 원전의 역사적 영향·독자 선호, 실측 지형 정확도·성능 우열은 범위 밖이다. 실측 지형·영상 자료는 선택 목적과 경계를 확인하는 데 쓴다.

## 노출과 비교 단위

1. 이 커밋을 GitHub에서 확인한 뒤 태그 구현·시험·배포 원문 및 독립 논문/도메인 원자료를 열고 실제 호출한다. 시작 전 확인의 노출은 위 저장소 절차와 221 자료에 한정됐다. 이 연구는 이미 알려진 예측의 새 실행 검산이며 221의 사전노출 순서를 반복하거나 독립 블라인드 평가를 주장하지 않는다.
2. `[NW,NE,SE,SW]`는 행 배열 `[[NW,NE],[SW,SE]]`로 올린다. scikit-image (row,column)은 (column,row)로 축을 바꾸고, ContourPy는 기본 `x=arange(cols)`, `y=arange(rows)`와 (x,y) 그대로 둔다. 선택 quad 원점만 빼서 (u,v) 단위 정사각형으로 놓는다. N/E/S/W는 각각 v=0, u=1, v=1, u=0이다. 배열 N은 작은 row다. 지도 북쪽은 실제 좌표에 따라 정해진다.
3. A=N–W + E–S, B=N–E + S–W, C=E–W. 전체 원 폴리라인의 연속 구간을 quad에 잘라 연결을 복구한다. 방향, 선분/정점 순서, 중복, 내부 끝점, 정확한 꼭짓점과 한 변을 따라가는 구간을 별도로 기록한다. 꼭짓점은 모든 입사 변을 함께 표시하고, 단일점 접촉·동일 변을 따라가는 조각을 더해 가짜 관통쌍을 만들지 않는다. C3/C4는 단위셀 직교 경계와 손계산 좌표 비교로 별도 재구성한다.
4. 221의 M/P/I 기본 예측은 (scikit-image, ContourPy) 순으로 C1=A/A, C2=A/B, C3=A/B, C4=A/A, C5=C/C다. C1–5의 P 보간값은 A/B/A/X/C이다. R1 E–S/E–S, R2 N–W/N–W는 co-exposure 이후 재구성이다. `I_FREEZE.csv`의 두 R 행은 미확인 상태를 유지한다. E 정확 기대는 R1 scikit-image 원시험 1건이다. R2 동일 엔진 상대 비교, 통제 E 미확인, 221의 0개 독립 정답은 별도로 보고한다.
5. C3의 `m=+0.5`와 `s=-0.25`, C2의 반례, C4 `s=0`에서 수학적 X와 두 선분의 차이를 검산한다. 부호·축을 뒤집을 때 방향과 무방향 변 쌍을 구분한다. 평균/안장점의 이론적 일치는 구현 내부 경로 계측과 구별한다.
6. 원좌표와 출처 원장, 시작/종료·프로세스·폴리라인 증거를 먼저 보존한다. 그 뒤 주관측, 통제·정정, 최종 RESULT/SELF_CHECK, 고정 결과판 검증과 마지막 HANDOFF를 순서대로 각각 저장한다.
