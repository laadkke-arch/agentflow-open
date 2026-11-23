# AF-RES-067#1 HANDOFF — **부분 인계 / 원산출물 미확보**

## 1. 식별 및 고정 결과

- 배정 작업자: web-pro; 실제 수행 주체: 이 ChatGPT 세션, 연결된 GitHub 파일/커밋 도구와 공개 웹 원문 열람. 별도 웹 Pro UI 모델 선택 검증 미실시. 사용자 PC에 설치·실행 없음.
- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-067`; 실측 분기 기준 SHA `374dc309454e8847603c133c4c1d1029d63c0c92`, 계획 통합 기준 SHA `028d16fee1121f5862efd410b78ec1d79d7080f2`.
- 선행 AF-RES-063 HANDOFF `8e348bb1306d5243b0a5ff8ebae773707d2dcfb4`; 본문 고정판 `86403f9082bfebe9eafefe00e673942380041761` 확인.
- **HANDOFF 이전 마지막 고정 결과 SHA: `a4b0c47959aa234719f13b3fa6ee76e019c187c6`**. 이 인계는 고정판 이후 **단독 마지막 커밋**으로 작성하므로 자신의 커밋을 본문에서 순환 참조하지 않음.
- [필수 표 1·2, 가장 중요한 3약점](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/RESULT.md) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/evidence/acceptance-evidence.json) · [다음 첫 재개 파일 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/SCOPE.md) · [8자리 frame](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/frame.csv) · [24개 views](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/views.csv) · [읽은 출처](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/sources.jsonl) · [실패 경로](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/search-log.jsonl) · [실측 커밋·검산 기록](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/WORK_LOG.md).
- 공통 진행표, dot-control.json, main, 다른 작업 경로 **수정하지 않음**. dot-control에서 067 항목은 GitHub file 응답 길이0으로 못 대조했으며 blob `af867733d1cbfac88f181845bbf1dac56089bf91`만 수신. 최신 규칙 파일 4종과 선행 HANDOFF를 읽었음.

## 2. 실제 결과 및 분모

- **외부 직접 연 원출처 21개**: 규격/기록 원전 12개, 개별 Debian *source acceptance* 9개. 계보는 21개 문서·발행 사건으로 분류했다. **그러나 요청된 4개 Debian 원 amd64 .deb 빌드 사건과 4개 JWST NIRCam Level 2 _cal.fits 원 처리 사건은 모두 미확보.** source acceptance에 `_amd64.buildinfo`가 있더라도 `Architecture: source` upload를 바이너리 빌드로 취급하지 않았다. source acceptance 9개를 동일판 재빌드 9개라 부르지 않는다.
- **8/8 예약된 고정 자리**, 원 카탈로그의 날짜+원 ID 정렬로 배정된 *확정 사건* 0/8; Debian 실제 binary build logs **관측 0/4 확보**, JWST 원제품 FITS header **관측 0/4 확보**. 0은 조사하여 얻은 수이지 역사 실행 부재가 아니다. 원목록 반환수/페이지/전역 최초 두 건은 미확인.
- **24/24 V0/V1/V2 형식 행**을 남겼지만 원 output 귀속 실제 평가 **0/24 가능**. input label/실제 읽은 bytes/output 동일run 확정 0/8. 수신 HTTP byte, 총 비용, 정확도, 보정 결과 과학 타당성 미확인.
- 규격 원문에는 `Installed-Build-Depends`가 영향 가능 설치 목록이며 `CRDS_CTX`는 맵 context, `R_FLAT`은 파일명임을 명시. 같은 처리의 *선택*과 원 소비 프로세스가 읽은 *파일 바이트*를 동일하다고 하지 않았다.
- 지정 최소20 직접 읽기 *수적* 조건은 충족하지만 요구된 원처리/빌드 사례 형태, 재빌드·재처리 6건, 강한 사용 증거, 전체 모집·정렬·검사 및 독립 검토 **미충족**. 완전 수용 불가.

## 3. 실제 GitHub 검산과 미실시 검사

- 마지막 출처·표·수용 원장 고정 커밋 `a4b0c47959aa234719f13b3fa6ee76e019c187c6`의 원격 GitHub `fetch_file`을 직접 재열람했다. RESULT blob `65340a9ad14223a15270d42bf1ccb8f81e5df8f8`, acceptance blob `ab592775555017249e43221b558d921b74b8895d`. frame=8행, views=24행, sources=21행, 수용조건=14개, RESULT 표1=8행 표2=24행 최종 약점=3행을 문자열/행 수로 점검. 수행 주체는 현재 세션이며 독립 검토 **아님**.
- `python -B -m workbench.session start ... --fetch` **미실시**, `python -B -m workbench.session check ... --fetch` **미실시**. 실행 소스 SHA/종료값/표준출력 **해당 없음**. `manifest.json` 미생성. 이유: 현재 GitHub 연결은 원격 컨텐츠 API이며 컨테이너의 `git ls-remote`에서 `Could not resolve host: github.com`; GitHub checkout 안에서의 Python 명령 실행 불가. 거짓 통과 판정 없음.
- 인계 문서는 마지막 단독 커밋이므로 위 결과 SHA의 검사가 인계문 자체를 검증했다고 말하지 않음.

## 4. 다음 첫 행동 — 자료·검사 우선순위

1. [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/SCOPE.md)의 **start 명령**을 인터넷되는 저장소 checkout의 이 브랜치에서 실행해 `manifest.json`을 같은 owned_path에 생성·커밋. 의존 063 result_commit과 통합 기준 실제 SHA를 검사하고 `dot-control.json`에서 067 원 항목을 직접 확인.
2. **Debian:** 공식 buildd/archive/snapshot에서 jq와 pandoc의 2024–25 amd64 binary build 완료 원목록을 모두 받되 선택 기준일과 timestamp 필드를 명시; date+run ID로 첫2씩 고정하고 원 `.deb`, 원 buildd attempt/log, `.changes`, `.buildinfo`를 연결. 원본 위치는 [탐색 실패 원장](https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/search-log.jsonl); 가장 먼저 재요청할 곳은 `https://buildd.debian.org/status/package.php?p=jq` 및 `https://buildd.debian.org/status/package.php?p=pandoc`. 성공 여부를 추정하지 않음.
3. **JWST:** MAST 공식 서비스에서 공개 `NIRCam` 영상·Level2·F200W/F444W·`_cal.fits` product 목록을 필터별 날짜+product ID로 정렬하고 첫 두 개씩 보존. `t_obs_release`와 file creation/processing time 구별; 원 header 블록의 CAL_VER/CRDS_CTX/R_FLAT/STEP_STATUS와 처리 이력, 원 context mapping을 확보. MAST 공식 [products API](https://mast.stsci.edu/viz/docs/products.html) 및 [metadata API](https://outerspace.stsci.edu/spaces/MASTDOCS/pages/150113030/API%2Bfor%2BJWST%2BMetadata). 실제 API 조회 대상/파라미터/응답수/제외/스냅샷을 저장.
4. 두 표와 views·receipts·alternatives 원장에 확보된 사건만 채우고 바이트 다운로드·digests 및 원 historical read hash를 구별. 실행하지 않은 프로그램을 원저자 실행이라고 해석하지 않음. 동일판 rebuild/reprocessing 사건 6개 원본을 별도 보조로 찾아 반례 검정.
5. 실제 `python -B -m workbench.session check docs/workstreams/research/AF-RES-067/manifest.json --fetch`를 수행한 주체·입력 manifest/대상 SHA·exit·stdout/stderr 기록. 고정 결과 커밋의 원격 `RESULT.md` 및 acceptance 다시 열어 비교한 다음에만 새로운 HANDOFF를 마지막 단독 커밋으로 작성.

공통 연구 색인 반영 제안: `AF-RES-067 — 부분 인계 / 21공식원전 직접열람; 주 build0/4+cal0/4, 슬롯8, 보기24, 입력 바이트 사용 귀속0/8, check 미실시, fixed a4b0c47959aa234719f13b3fa6ee76e019c187c6` 및 위 두 필수 표 링크. 색인 편집은 배정·통합 담당 몫.

## 5. 가장 중요한 불일치·약점 정확히 3건과 다음 조사

1. **Source acceptance ≠ binary build:** signed `_amd64.buildinfo`를 담은 source 업로드만으로 원 `.deb` run·출력 hash 연결 불가. 다음 조사: buildd 원 attempt+binary changes+deb+buildinfo 조인 ([jq 근거](https://tracker.debian.org/news/1508449/accepted-jq-171-3-source-into-unstable/)).
2. **MAST 제품 자체의 공백:** 원 4개 cal FITS header 및 정렬 모집 결과 없음. 다음 조사: MAST public product list를 기준일+원 ID로 고정하고 동일제품 재처리 이력과 per-product calibration header 읽기 ([MAST 명세](https://mast.stsci.edu/viz/docs/products.html)).
3. **선언/파일명/해시와 과거 실제 읽기 불일치:** installed package 또는 R_FLAT 라벨은 consumer-side read digest가 아님. 다음 조사: 같은 run의 입력 파일 read hash와 원 출력 hash를 동시에 보관한 영수증 확보 ([dpkg 정의](https://manpages.debian.org/testing/dpkg-dev/deb-buildinfo.5.en.html), [R_FLAT 정의](https://archive.stsci.edu/jwst/keyword/build8.0/meta_ref_file_flat_name.html)).
