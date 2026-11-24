# AF-RES-184 SELF_CHECK — PARTIAL (작성자 자체점검)

독립 검토 미수행. 증거 원장에 없는 실행·성공·실패를 채우지 않았다. 보조 결과는 사용 가능하나 주 완료 조건은 미충족이다.

| 질문 | 답과 직접 근거 ID/URL | 반증·다른 해석 탐색 | 판정 및 미충족 |
|---|---|---|---|
| Q1 | D01–D08: [hello amd64](https://packages.debian.org/en/trixie/amd64/hello/download) 등 8개 후보 해시, [C03](https://packages.debian.org/trixie/grep) source/binary version, [A08](https://snapshot.debian.org/) import 규칙 | [F02](https://snapshot.debian.org/archive/debian/20261124T000000Z/dists/trixie/Release), F01/FS1–4, 두 arch 목록 F03/F04. grep +b1, 조회 crawl age 서로 다름 | frame/후보 8/8, 동일 resolved import 및 index hash 0/8 확인; Packages/Sources 실제 원문 미확보 |
| Q2 | [A05](https://manpages.debian.org/trixie/dpkg-dev/deb-buildinfo.5.en.html), D01–D08 | [F05](https://buildinfos.debian.net/), FBP01–08 직접 buildinfo 후보 및 F08–09 buildd 조회 실패; 경로 실패가 원본 부재를 뜻하지 않음 | 원 빌드 receipt/서명/날짜/입력/산출 직접 연결 0/8 확인; 실제 수 미상 |
| Q3 | [A02](https://github.com/kpcyrd/rebuilderd/blob/main/contrib/docs/rebuilderd-v1.yml), [A06](https://manpages.debian.org/trixie/devscripts/debrebuild.1.en.html), [R02](https://reproduce.debian.net/amd64/api/v1/builds/282219/log), R01/R03/R04 | target API FRP01–08, 목록 F03/04, detail F10/F11 실패; R02 dsc digest는 input, buildinfo의 기대 해시는 archive hash와 따로 연결 필요 | target ID/산출 해시 0/8 확인; 비교 4 ID, 실제 빌드 단계 2건, 성공/byte pair 미확인 |
| Q4 | [A03](https://reproduce.debian.net/amd64/stats/trixie/) 3 lam labels→[R04](https://reproduce.debian.net/amd64/api/v1/builds/151245/log) 하나; [M02](https://packages.debian.org/de/trixie/arm64/grep/download)와 D06 동일 artifact | R02/R04 동일 worker 다른 패키지, R03/R04 다른 worker 같은 서비스. A04 arch 별도 집계, A09 Arch 별도. 같은 key retry 탐색했으나 목록 접근 실패 | 같은 원 log의 fanout과 언어 재게시 각각 확인; 별개 작업 ID 후보 확인, 동일 패키지 실제 retry/독립 운영조직 확인 못함 |
| Q5 | [R01](https://reproduce.debian.net/amd64/api/v1/builds/288711/log) 입력 404, [R02](https://reproduce.debian.net/amd64/api/v1/builds/282219/log) 의존성, [R03](https://reproduce.debian.net/amd64/api/v1/builds/150526/log) 및 R04 실제 build exit 2 | A02 BAD 유형 다양; P05/P06은 다른 arch 및 binNMU, hash 차이 무의미; buildinfo 404 vs 우리 조회 실패 구별 | 비교 실패 유형 분리. 실제 같은 키 byte mismatch, expired/unscheduled, 정상 성공 대조 미확인 |
| Q6 | [E01](https://www.usgs.gov/faqs/where-can-i-get-usgs-water-quality-water-chemistry-data-surface-water-andor-groundwater), [E02](https://www.waterqualitydata.us/portal_userguide/), [E03](https://www.nist.gov/system/files/documents/srm/SP260-156.pdf) p14 Table4의 NIST/USGS Al 측정 원보고 | E02 legacy 이후 자료 누락, E04 같은 데이터 다른 format, E03 lab13a/b/c 같은 lab의 분기. 동일 관측 행 원자료를 찾지 못함; E05 일반 프로그램 소개만 | 보고값 2개/기관 2개, 실제 원보고 1개; 관측소 두 포털 row join 및 장비 ID 미충족, raw 측정 독립성 미확인 |
| Q7 | claims.csv CL01–CL10, RESULT.md 표3. A03→R04 3 labels→1 event; R01–04 4 records/2 build-stage; D06→M02 same artifact | URL count, binary count, workers count 각각 다른 단위; no target matched success; 양성 정상 대조 못 얻음 | 확인된 하한만, 상한 unknown, 독립 성공률 산출하지 않음. 주표본 목표 두 파일의 해시 연결 0/2 확인(8자리 전체 0/8) |

## 분모·원장 검산

| 유형 | 목표 | 엄격 산입 | 보조/미충족 |
|---|---:|---:|---|
| 동일 배포 시점 Packages/buildinfo/원 빌드 | 6 | 0 | catalogue 8 hashes + 4 context pages; 공통 시점, 원 buildinfo 없음 |
| 별개 대상 재빌드 로그/레코드 | 6 | 0 | 비교군 로그 R01–04는 이 유형에 중복 산입하지 않음 |
| API/대시보드 생성/상태 비교 정의 | 4 | 4 (넓은 규칙 범위) | A01/A02/A03/A06; A06을 실행 비교 도구 규칙으로 좁혀 제외하면 3/4. A04 별도 arch 집계는 중복 생성 규칙이라 엄격 수에 추가하지 않음 |
| 비교·재시도 원 기록 | 2 | 4 | R01–04, 다만 fixed main frame 밖; 동일 키 retry pair 0 확인 |
| 환경·숙련도 실제 원생산/측정 기록 | 4 | 1 | E03; E01/E02/E04/E05는 context, 실측 행 미확보 |
| 전체 | 22 (유형 각각 충족 필요) | 9 (좁게 8) | 13 이상 부족; 보조를 승격시키지 않음 |

- sources.jsonl 70행, ID 70 고유, read 31 + read_limited 3 = 34 응답에서 읽음, 접근 실패 36. duplicate 4 및 독립 비교에서 제한적인 Arch placeholder 1을 빼고 실질 고유 원자료·설명 문서 29. 범위 밖 보조 문서 포함 수이며 엄격 최소 유형과 구별. 명확한 실제 실행 ID는 R01–04의 4개, 실제 빌드 단계 R03/R04 두 건, 원 buildinfo 연계 대상 0건 확인, 대상 성공 해시쌍 0건 확인, 같은 키 독립 조직 성공 0건 확인. 모두 확인 하한이며 전체 실제 수/상한 미상.
- 출전 확인일 UTC 2026-11-24(날짜까지만); 사이트의 게시/크롤 표기 및 로그의 UTC time은 별도 필드. 원 응답 body SHA256/실제 조회 초 단위 시각은 얻지 못함. 배포 후보의 SHA256은 게시된 값, 직접 byte 계산 아님.
- GitHub 커밋 d23afa1dfdc1e75ef5e6a4bd36d9e84433866f20에서 7개 대표 파일을 다시 가져와 connector 반환 텍스트에 대해 JavaScript 자체검산: frame 22 data rows × 11 columns; packages 8 × 18; runs 32 × 22; claims 10 × 10; sources 70 JSONL parse 및 고유 ID 70. frame P01–P08 순서와 packages 일치, 8 hash 문자열 64 hex, runs 부모 키 모두 존재, packages/runs/claims source refs 모두 존재. RESULT 표 data row 8/10/6/3 확인(약점 정확히 3). 이는 connector 응답의 구조 자체점검이지 외부 데이터의 해시 검증이나 독립 검토가 아니다.
- 보정 커밋 626b4a17d8c936654f156cceed0e522c3b9610f4: DC-P01/02/05/06 URL에서 미접근 경로 대신 실제 읽은 /en/ 경로를 사용하고 B-P01–08은 원장의 필터 query 주소로 수정. 판정·개수 동일. 다음 HEAD에서 보정 파일과 본 점검 다시 확인.
- 중간 commit: SCOPE 041411a134b61d7064eed7ec1c1c3ff7f926c1aa; frame af10afc04b9c5e710f9052f528cf1c36d3c47552; packages 0cd72c1b42949dfc65b7bbf237a77de5d96ce0e0; sources 2374c703ea72a25686ffb84459f4330333490f9b; frame 보정 456d9bba554c6ce3150ac166a29e85994cdd9ee8; runs bc138b88249b7e991986a956d9d84318e5204a01; claims 6790209196f0cbaf5ff55526301f79636f81f725; RESULT d23afa1dfdc1e75ef5e6a4bd36d9e84433866f20.
- 로컬 checkout/workbench/외부 raw byte 검사/실제 rebuild 실행하지 않음. GitHub connector commit 및 readback만 사용; 새 빌드 금지 범위 준수. Codex Cloud용 공개 원자료 읽기·검산 명령은 HANDOFF에 기재.
