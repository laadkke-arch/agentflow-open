# 반례 및 이용자 안내 (④)
## 판단 규칙과 사전예측 정정
- P1–P3은 렌더된 **전체 표**의 각 파일행 및 마지막 separator 확인. 1.13.1 L236–259 24 wheels + 1 sdist, 1.14.0 L241–264 24+1, 1.14.1 L241–272 32+1. 80 wheels + 3 sdists, 83 표시 파일; 이 분모와 raw JSON 0/3을 분리한다. 9셀 5 present/4 HTML no match. abi3, cp313t, 다른 아키텍처 혼용 없음(현재 표시 표 기준). 과거 삭제 파일 및 정확 업로드 UTC·파일 requires_python은 미확인. 주소는 HTML href, D1–D5 binary open 실패.
- 예측의 중심 5/4는 HTML에 부합하나 1.14.0의 3.13을 무조건 “코드 미지원”이라고 단정할 수 없다. B1 2024-06-19 member의 지원 예상, Linux beta2 compile error/해결, 6-20 main testing, 6-21 nightlies 소비자 확인, 8-01 stable ABI 및 NumPy RC 대기가 서로 다른 사건이다. R2 최종 릴리스 노트는 하한만 명시; T2/W2 3.13 classifier/matrix 없음, P2 stable wheel 0. R3/R10은 1.14.1의 3.13 공식 지원+wheel. R8/R9 당시 표는 1.14 행 자체가 없고 최신 R6는 계열 마지막 patch를 기준으로 한 후대 요약이다.
- T3/P3 1.14.1의 classifier는 3.12까지, W3와 R3, P3 cp313 wheel이 동시에 3.13을 지지한다. classifier만으로 reject하면 오류, Requires-Python 하한만으로 accept해도 오류. 3.13 ordinary GIL 사용자에게는 M9 후보 제공하되 3.13t에는 보류.
- 실제 CI의 반증: B2 PR21000 개발 SHA b307ccd에서 wheel built라는 보고가 있었지만 같은 PR Windows wheel 크기 문제 및 macOS 파일명 문제(12_3/12_0), 마지막 commit은 wheel builder 미실행. B4 8/18 릴리스 관리자 Cirrus cp313 미설정 발견, B5 PR21409 aarch64 error와 main merge: 플랫폼/커밋이 다름. B6 2024-07-09T10:14:17Z main free-threaded macOS arm64 CPython 3.13.0b2 시험 실패 기록(Trace/BPT trap 5), 실제 로그 발췌가 있어도 release SHA/Linux GIL 성공 증거가 아님. C1–C3 API 빈 반환 역시 미확인. 별도 실제 사용자의 설치는 0회.
- Sdist 3개 모두 표시. 1.14.0/3.13 metadata 하한 통과 + sdist ≠ 성공 소스 빌드. 정확 버전, 컴파일러/BLAS/LAPACK/NumPy/Cython 및 Python RC 여부 확인(S7). 설치 실험 금지 준수.
- 1.13.1/1.14.0 musllinux_1_1, 1.14.1 musllinux_1_2 태그: glibc x86_64 wheel 대체 불가. macOS arm64 1.13.1 macOS 12+; 1.14.x 12+와 14+ 별개 파일. macOS 12 사용자는 14+ 링크만 주면 실패 조건. 두 manylinux tag는 복합 platform tag OR로 읽고 glibc 2.17+ 및 pip 지원 확인(S3/S5).

## 추천 문장 (환경 및 목적별)
1. 과거 연구 재현: 해당 판의 파일 URL+게시 SHA-256+정확 파일명+날짜를 유지한다. M1/M2/M5/M8/M9는 후보 직링크. 재현 전 원래 Python patch/ABI, NumPy lock, glibc, OS/arch, pip accepted tags, source channel, artifact hash 확인; raw per-file metadata 및 byte 검증 전 확정 성공 문구 금지. 업로드 일자는 정밀 시간 순서를 보장하지 않음.
2. 3.9 + 1.14.x M4/M7: 당시 하한 자체가 부적합. 옛 실험이 1.13.1이라면 M1(옛 링크), 새 프로젝트라면 현재 유지보수와 Python upgrade 선택; 1.13.1을 오늘 최선이라고 단정 금지.
3. 3.13 + 1.13.1/1.14.0 M3/M6: 하한 통과는 맞으나 현재 HTML 대상 wheel 없음. 원래 nightly나 source build라면 정확한 당시 origin/commit/ABI receipt 필요. 새 개발자는 지원되는 최신 호환 판과 실제 파일 우선. 1.14.1은 표본 내 3.13 GIL 전환점이지 현재 최신의 보증 아님.
4. 3.13 + 1.14.1 M9: 공식 지원 추가, cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64 후보. cp313t, aarch64, musl, 구형 glibc 및 pip에는 링크를 재선택. 3.13.0 final은 2024-10-07이어서 8/21 사용 가능 파일이 final interpreter에서 이미 실행됐다고 할 수 없다.
5. 릴리스 관리자: 표시 날짜/원공개 시각/후속 추가 게시/삭제 사건 구별. 파일별 metadata, URL, digest, CI receipt의 결합 필요. 소스 담당에게는 S7의 도구체인과 사전 요구 제공; 바이너리만 원하는 사람에게 sdist를 대안인 것처럼 주지 않는다.

## Nikon 제조사 대조 (N1–N4)
| 설치 대상 | 이전 C firmware | 목표 파일 | 발행일 (제품 목록) | 다운로드 host | 반대 조건 |
|---|---|---|---|---|---|
| D850 | 1.00–1.30 | D850_0131.bin / 1.31 | 2024-04-25 | Windows/Mac OS 선택 | 이미 1.31은 불필요; Windows가 맞아도 Z6II이면 대상 불일치 |
| Z6II | 1.00–1.62 | Z6_2_0170.bin / 1.70 | 2025-06-03 | Windows/Mac OS 선택 | D850 파일 불가; 1.70이면 업데이트 불필요 |
N1 L13–23,77–94; N2 L13–23,133–150; N3/N4 제품별 발행일. 두 모델에서 host OS 조건과 장치/현 firmware를 분리한다. 올바른 다운로드 PC가 올바른 카메라라는 뜻은 아니다. Linux host 제공 경로는 이 공지에서 확인되지 않았지만 .bin이 Linux에서 본질적으로 불가능하다고 단정하지 않음. Windows/Mac 결과 파일 동일명은 동일 digest 증거 아님. 원제조사 업데이트 절차, 전원 및 버전 확인은 별도. 실제 다운로드·장치 설치 미실시. 모델/버전+전송 host+파일 조건은 SciPy의 Python ABI+platform+artifact와 유사하지만 안전한 firmware 설치는 별도의 제조사 절차다.

## 비용과 대안
(A) 지원표+release link만: 유지비 낮으나 classifier 지연/patch 전환/파일 유무 오안내. (B) release+파일별 조건+digest+게시 시각: 조회/저장·갱신 필요; 과거 재현 및 binary-only에 적합, raw 삭제로 당시 불명. (C) CI/실제 receipt까지 결합: 최고 근거지만 로그 보존/정확 build provenance 비용; 사용자 설치 대체 불가. (D) 질문/보류: environment tuple 미확인일 때 안전하나 추가 상호작용. 공식 링크 2개를 병기하고 evidence state/last verified를 기록하는 중간안. 비용 실측 없음; API/데이터 수집 설계만.