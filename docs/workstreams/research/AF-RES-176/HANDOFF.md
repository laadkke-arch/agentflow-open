# AF-RES-176 HANDOFF — PARTIAL

## 실제 상태
PARTIAL (작업자 자기판정; 중앙 진행표 변경 안 함). 같은 시험 정의/서로 다른 제출 단언/동일 단언 재게재를 구별하는 주표본 조인은 완료했으나 과거 실제 실행 독립성, 정확판 반박, 역사적 fail→pass, 환경 특정 관측행은 미확정. 진행 자체는 가능했으므로 BLOCKED 아님. 독립 검토는 시행하지 않았다.

- 작업 브랜치: `work/research-af-res-176`, owned_path `docs/workstreams/research/AF-RES-176/`. 제품 DB·검색 엔진·Studio 연동 선택 보류.
- 계획 통합판 53eaa286136019510f052179f5f51d901bdac858 → 시작 foundation 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc (+2, dot-control만 207줄 추가). 선행 AF-RES-168 중앙 DONE / 고정 인계 5e1010c6698ea43c80e27ca4b73fdb98ee4f2168 / 자체 PARTIAL (exact receipts 0/16).
- 외부 보고 생성판 `8811ba2a3bcae883ac91efacffb70ef08d84e92f` (commit 2025-04-22, header 2025-04-10, HTML blob 244339bbc3c9aee33183a131f8e5a62a6762bbab). 최초 조회 최신 HEAD fd4f7eb41f679fb73a54923143c473c3a1d06093와 manifest 차이가 있어 보정. 보고판은 각 과거 실행의 suite pin이 아님.
- 결과·자기점검을 모두 포함한 **고정 결과 SHA `7f982bc64e67f0abfb457c27b9916fd10c21d039`**. 이 HANDOFF 자체는 별도 후속 커밋이며, 자기 자신 커밋의 SHA는 본문에 넣을 수 없으므로 작업 브랜치 HEAD 및 반환 메시지에서 확인. 결과 SHA compare: 시작 대비 10 commits ahead/0 behind, 8 files 모두 owned_path 안. dot-control 수정 없음.
- 대표 파일: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/SELF_CHECK.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/sources.jsonl), [assertions.csv](https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/assertions.csv), [tests.csv](https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/tests.csv), frame.csv, SCOPE.md, advice.csv.

## 판독 요약 / 미확인 수
- 631 test definitions + 13 report files frame. 양성 6, 음성 4; 주표본 10×3=30 예정/30 판독, 실제 단언 25 pass, 5 C++ compaction 미제출(공석), fail/inapplicable/untested/cantTell 0. 25/25 raw-render match.
- 예정 pair 30, 20 outcome agreement, 0 disagreement, 10 missing pairs. 엄격 동일 조건 독립 실행 합의 **0 확인, 20 미확인**. 실제 과거 실행 수 미상. 25 primary raw assertions 모두 실제 suite SHA/option/log 미확인.
- 보강 30 예정/30 제출, 29 pass+1 fail (Gold A04-5 t0123); 28 reported-outcome agree pairs, 2 disagree. 보강 3 subjects separate; exact historical comparison missing. 6 reported lineages, 0 verified run lineages. 7 report files outside sample not read.
- 자료 38 ledger rows, 30 counted unique original documents (7 suite/spec/gen, 6 submitted reports, 11 implementation docs, 2 change docs, 2 proficiency, 2 environmental structural docs). Environmental matched observation **0**, feed-level evidence 1; strict environmental original-row condition not met. Two proficiency studies distinct report groups, exact instrument/raw receipts missing. 55/55 raw-render match overall, 60/60 test IRI join. Q1–Q7 and 3 weakness rows verified.
- 시험 변경 H01 fromRdf/0027 outside main sample, H02 new expansion tdi13 later; Gold exact same predicate fail→pass not found. Exact historical suite pin/fixture hash and original execution log absent; Guile exact release source and C++ 0.5.0 release tag missing; common engine vs port direct lineage not closed. Full fixture reads not completed (tool-call cap in initial batch). Source ledger records substantive reads, not exhaustive low-level click/retry log. 
- 각 파일 생성판에서 대표 파일을 다시 열고 원장 ID·주소 확인: prereg 2bbbba1e5889c810c59bbcc10b40895338e334d1; first frame 769685a0fe3a11e38aebd1b8df9423fd93303f08; corrected frame 0aee04b45a8b9f8e5f629e842af326911ded8554; scope correction c0d3f05708a3066e25a910458434b40a36782103; assertions 0809972ad37d29d85ce83d717c3366c5414ee1d9; tests 670acc77c24eb90a6a3c91cf9e7bc8464a807616; sources 336b61e32db5bc49554936f40cfceffb9fd2da60; advice 4742986e1f621bd0f6c1876ba22c299bc4946051; result 7d3162736d23565d72bff61d8bbda87dd0e93218; SELF_CHECK 7f982bc64e67f0abfb457c27b9916fd10c21d039.

## 첫 재개 행동
1. **과거 제출의 실제 suite pin 및 실행 영수증 찾기**: 보고 원파일과 submission PR/commit history에서 archive SHA와 CI job/log URL을 역추적. 우선 A04-5 (Gold t0123 fail)와 A04-1/2/3 pass의 원 제출 시점(2020-04-06/12, 2020-06-17, 2024-05-20)을 맞춘다. 새 실행은 과거 사실 증거가 아니다. 일치하는 시험판·입력·기대 오류·processingMode/ordered/loader/비교 방식과 독립 실행 로그가 나오면 pair 판정 변경. Gold fail→pass 및 stable ID expected 변화 vs pure move history를 조사. Guile v1.0.0 exact archive, C++ 2024-05-20 source commit부터 확인.
2. Environmental E01: USGS NWIS와 WQP WQX2.2에서 2024-03-11 이전 동일 USGS site/sample/analyte record, 활동 ID·시간대·단위·method·qualifier·value를 맞춘 두 실제 원 export 확보. WQP guide S29의 Table7 metadata 기준. 신규 export가 동일 키에 합류할 때만 재게시 관측으로 인정.
3. 별도 Codex Cloud에 다음 읽기/검증 명령과 고정 입력을 넘긴다. 이 웹 세션에서는 명령을 실행하지 않았다.

```sh
git clone https://github.com/w3c/json-ld-api.git
cd json-ld-api
git checkout 8811ba2a3bcae883ac91efacffb70ef08d84e92f
git rev-parse HEAD
git log --all --follow -- reports/jsonld-gold-earl.ttl
git log --all --follow -- tests/expand/0123-in.jsonld
git log --all -- tests/expand-manifest.jsonld tests/compact-manifest.jsonld
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:tests/expand-manifest.jsonld
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:tests/compact-manifest.jsonld
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:reports/guile-jsonld-earl.ttl
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:reports/java-jsonp-ld-earl.ttl
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:reports/jsonld-cpp.report.ttl
git show 8811ba2a3bcae883ac91efacffb70ef08d84e92f:reports/jsonld-gold-earl.ttl
git log --all --since=2020-04-01 --until=2020-06-18 -- reports/
git log --all --since=2024-05-01 --until=2024-06-01 -- reports/
```

검사 입력: 이 브랜치 7f982bc64e67f0abfb457c27b9916fd10c21d039의 tests.csv, assertions.csv, frame.csv, sources.jsonl 및 위 고정 W3C manifest/report. Python/RDFLib 또는 Ruby RDF로 Turtle을 정식 파싱하고 test IRI+subject(+release, assertor, date)의 중복·누락·outcome·mode 조인을 체크. manifest sequence 10개와 raw assertion 60자리/55 실제, primary 25/5 및 raw/render 55/55 일치 기대. SHA가 다른 역사 파일은 새 층으로 저장. fixture를 sha256sum 또는 git hash-object로 비교하되 입력 콘텐츠/option 변경 시 동일 술어 판정 보류. 과거 보고판 근거 확보 후 별도 재실행을 시행할 수 있으나 이전 제출 증빙과 혼동 금지. 로그/원 파일이 없으면 미확인 유지. 동시 작업자와 중앙 파일을 변경하지 말 것.

색인 제안: 동일 JSON-LD 시험에 대한 원 EARL–렌더–구현–실행 계보 분리 / 25/30 주표본 pass와 5 미제출, 보강 단독 fail, 엄격 독립실행 0 확인(PARTIAL) → AF-RES-176/RESULT.md 및 sources.jsonl.
