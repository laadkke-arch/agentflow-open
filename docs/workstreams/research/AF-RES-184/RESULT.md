| 패키지·버전·아키텍처 | 배포 산출 해시·URL | 재빌드 ID·운영자·URL | 비교한 해시 | 판정 | 미확인 |
|---|---|---|---|---|---|
| P01 hello 2.10-5 amd64 (source hello 2.10-5) | `4536aabbb75ec21ffe161099ee4b97274945770bdb0682e25ec322421211ca5e` [D01](https://packages.debian.org/en/trixie/amd64/hello/download); 라이브 후보 | ID·운영자 미확인; [FRP01](https://reproduce.debian.net/amd64/api/v1/builds?name=hello&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P02 hello 2.10-5 arm64 (source hello 2.10-5) | `7a917c7f44fbd3373dff0f35a0b6bdf8ef564ff90579d8b130ff52fbf33fce1f` [D02](https://packages.debian.org/en/trixie/arm64/hello/download); 라이브 후보 | ID·운영자 미확인; [FRP02](https://reproduce.debian.net/arm64/api/v1/builds?name=hello&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P03 sed 4.9-2+deb13u1 amd64 (source sed 4.9-2+deb13u1) | `7071270ed4f6adda55bc4f926347fb847bacaffbdee3dff917bc6006ed7e3775` [D03](https://packages.debian.org/trixie/amd64/sed/download); 라이브 후보 | ID·운영자 미확인; [FRP03](https://reproduce.debian.net/amd64/api/v1/builds?name=sed&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P04 sed 4.9-2+deb13u1 arm64 (source sed 4.9-2+deb13u1) | `c654fa045de8cc722855b8db59990b703cb7299c897c6e187bf949d42df82b62` [D04](https://packages.debian.org/trixie/arm64/sed/download); 라이브 후보 | ID·운영자 미확인; [FRP04](https://reproduce.debian.net/arm64/api/v1/builds?name=sed&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P05 grep 3.11-4 amd64 (source grep 3.11-4) | `2d78ed07d86a530ebf538f05cb2415f37c8daf908596bc32fc2563cc7e88c55a` [D05](https://packages.debian.org/en/trixie/amd64/grep/download); 라이브 후보 | ID·운영자 미확인; [FRP05](https://reproduce.debian.net/amd64/api/v1/builds?name=grep&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P06 grep 3.11-4+b1 arm64 (source grep 3.11-4) | `6f7257fbec0197bd54b2347861ff01e2c4e8411790b0df20242483615324fe66` [D06](https://packages.debian.org/en/trixie/arm64/grep/download); 라이브 후보 | ID·운영자 미확인; [FRP06](https://reproduce.debian.net/arm64/api/v1/builds?name=grep&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P07 gzip 1.13-1+deb13u1 amd64 (source gzip 1.13-1+deb13u1) | `74cf12212beee4ab8d473bdc0107abf9e8cef737492198e2f4944a19f142b0ac` [D07](https://packages.debian.org/trixie/amd64/gzip/download); 라이브 후보 | ID·운영자 미확인; [FRP07](https://reproduce.debian.net/amd64/api/v1/builds?name=gzip&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |
| P08 gzip 1.13-1+deb13u1 arm64 (source gzip 1.13-1+deb13u1) | `02f83e5b4351ab4caa54f0405a334943dcd4986fdce740072bbda7b3c844e1f6` [D08](https://packages.debian.org/trixie/arm64/gzip/download); 라이브 후보 | ID·운영자 미확인; [FRP08](https://reproduce.debian.net/arm64/api/v1/builds?name=gzip&release=trixie) 접근 실패 | 배포 후보만; 재빌드 해시 미확인 | 판정 보류 | 공통 snapshot·원 buildinfo·실행·산출 해시 |

| 표시·원문 | 원 측정 또는 빌드 ID | 관계 | 별도 실행의 직접 근거 | 계보 미상 |
|---|---|---|---|---|
| [amd64 BAD 통계 A03](https://reproduce.debian.net/amd64/stats/trixie/): lam-runtime / lam4-dev / liblam4t64 → [R04](https://reproduce.debian.net/amd64/api/v1/builds/151245/log) | amd64:151245 | 동일 링크의 출력별 상태 fan-out | 2026-03-05 source download 13:38:55Z; dpkg-buildpackage exit 2, 종료 13:55:02Z; 한 빌드 단계 작업 | 각 바이너리 기대/실제 해시·이전 시도 |
| [D06](https://packages.debian.org/en/trixie/arm64/grep/download) ↔ [M02](https://packages.debian.org/de/trixie/arm64/grep/download) | native build ID 미확인; grep_3.11-4+b1_arm64.deb / 426128 bytes / 동일 SHA256 | 언어별 같은 배포 산출물 표시 | 없음; 같은 파일 지문 | 실제 생성 실행과 전송 계보 |
| [R02](https://reproduce.debian.net/amd64/api/v1/builds/282219/log) ↔ [R04](https://reproduce.debian.net/amd64/api/v1/builds/151245/log) | 282219 / 151245 | 같은 worker osuosl44-amd64, 다른 패키지·버전·날짜 | 2026-08-23 의존성 준비 실패 vs 2026-03-05 빌드 실패; 별도 작업 ID와 단계 | 같은 패키지 재시도 관계 아님; 운영 조직 법적 경계 |
| [R03](https://reproduce.debian.net/amd64/api/v1/builds/150526/log) ↔ R04 | 150526 / 151245 | osuosl43-amd64 vs osuosl44-amd64; 같은 공개 서비스 | 실제 dpkg-buildpackage 실패 두 건; 서로 다른 package | 독립 운영 조직과 같은 파일의 성공은 아님 |
| [R01](https://reproduce.debian.net/amd64/api/v1/builds/288711/log) | 288711 | 원 buildinfo HTTP 404 | 조회 실패 로그 하나; 빌드 시작 증거 없음 | worker/시간/실제 수행 |
| [amd64 A03](https://reproduce.debian.net/amd64/stats/trixie/) / [arm64 A04](https://reproduce.debian.net/arm64/stats/trixie/) | 집계; 개별 ID 일부만 | 서로 다른 arch 집계, 전체 성공/실패 사건 수 아님 | 1005 bad binary/799 source vs 1059/827은 집계 단위 차이 | 전체 실행·재시도·운영자 수 |
| [A01](https://reproduce.debian.net/trixie.html) / [A02](https://github.com/kpcyrd/rebuilderd/blob/main/contrib/docs/rebuilderd-v1.yml) | instance + integer build ID 규칙 | dashboard/API/log/artifact는 같은 사건의 다른 읽기 경로일 수 있음 | 주표본 ID를 얻지 못함 | 서비스 deployed 코드판 및 ID history |
| [Arch A09](https://reproducible.archlinux.org/) | 미확인 | 별개 생태계·JS dashboard | 페이지 표시 구조만 확인 | arch API 행·운영자; Debian 수에 불산입 |
| [USGS E01](https://www.usgs.gov/faqs/where-can-i-get-usgs-water-quality-water-chemistry-data-surface-water-andor-groundwater) / [WQP E02](https://www.waterqualitydata.us/portal_userguide/) | 개별 ActivityIdentifier 미확인 | NWIS 원자료를 WQP에서도 제공한다는 기관 설명 | 행 값·시간·사이트·method 매칭 없음 | 같은 원 측정 두 포털 재게시의 실제 사례 |
| [NIST E03](https://www.nist.gov/system/files/documents/srm/SP260-156.pdf) p14 Table 4, p15–16, Appendix D | SRM 1575a Al; NIST INAA / USGS ICPAES; lab 13a/b/c | 동일 표준물질의 기관·방법별 측정; lab 13의 분기들은 한 lab | NIST 575±16 µg/g, USGS 589±29 µg/g; 서로 다른 기관 보고 결과 두 개 | raw measurement/aliquot ID, 장비 원로그 및 모든 독립성 조건 |

| 이용자가 물은 주장 | 대표 원전 | 추가·반대 증거 | 확인한 최소 실행 수 | 확인할 수 없는 것 |
|---|---|---|---|---|
| 지정 바이너리의 동일 snapshot 배포 hash인가? | D01–D08; A08 | F02/F03/F04; 조회 시점 다른 catalogue; C03 binNMU | 확인된 원 빌드 사건 0건(실제 수 미상) | resolved import 및 Packages/Sources hash, 실제 .deb 및 buildinfo |
| 이 파일을 다른 사람이 재현했나? | A05 buildinfo 규칙, A06 debrebuild 비교 규칙 | FBP01–08/FRP01–08 접근 실패 | 주표본 해시쌍 확인 0/8; 원·재빌드 연결 실행 하한 0 | 일치/실패 모두 미판정, 독립 운영자 수 미상 |
| 링크 세 개면 빌드 세 개인가? | A03→R04, 151245 | D06↔M02 동일 파일 표시 | R04 실제 빌드 단계 1건; 다른 동일 ID 표시 2개 추가로 실행 수 증가 없음 | 이전 재시도, 같은 패키지 성공 및 전체 실행 수 |
| 다른 작업 ID/worker는 무엇을 뒷받침하나? | R01–R04 | R01 buildinfo 404; R02 의존성 실패; R03/R04 다른 패키지 | 별개 작업 기록 4개, 빌드 단계 확인 2건 | 같은 키 별도 재시도·성공·조직 독립성 |
| BAD가 바이트 불일치인가? | R01/R02/R03/R04; A02 | P05/P06 source 동일, arch·binary version 다름 | 실제 빌드 단계 실패 2건; 직접 byte mismatch 입증 0 | 실제 재빌드 산출과 비교 피연산자, 미예약·만료 실제 사례 |
| 측정 링크가 많으면 독립 측정이 많은가? | E01/E02/E03 | E04 동일 데이터 포맷; lab 13a/b/c | 소프트웨어 실행 수에 불산입; NIST/USGS 기관별 보고 측정값 2개 | 관측소 행 원 ID·장비·원측정 로그; 독립 조직 전체 조건 |

## Q별 판정 — PARTIAL

**Q1. 대상 고정.** 계획상 동일 trixie main import, 동명 바이너리 8자리 전부 모집표에 있음. 2026-11-24T00:00:00Z는 요청 시각이지 확인된 import가 아니다. F01/F02/FS1–4에서 접근 실패. A08 문서는 요청 시각 이전 import 처리 규칙을 말하므로 실제 해석된 시각을 대체 추정하지 않았다. 후보 SHA256은 배포자 Packages 웹 catalogue의 표기값이지 직접 다운로드 후 계산값이 아니다. D02는 3 days ago, D07/D08은 last month, 나머지는 today crawl로 동일 시점이 아니다. 보정된 판단: grep source 3.11-4 중 P06 binary 3.11-4+b1이며 P05는 3.11-4. 버전은 source와 binary 분리, epoch 및 +bN 보존, Architecture: all은 artifact 자체 arch로 dedup하고 host/build arch를 별도 저장. 한 source에서 다른 바이너리가 나오면 산출 식별자는 각각; 실행 식별자는 공유 가능. A05/A07과 실제 C03, A03/R04가 이 규칙을 지지한다.

**Q2. 배포 원 빌드.** 8개 파일명/해시/크기 후보 확인. buildinfo root disabled 및 8개 직접 후보 URL 접근 실패(F05/FBP01–08); buildd hello/grep F08/F09 실패. 경로 추측 실패는 원본 부재가 아니다. 공식 원 buildinfo 서명, Build-Date/Build-Architecture/Installed-Build-Depends 및 Checksums-Sha256, source hash와 archive 파일 hash 매칭은 모두 미확인. A05는 양식 규칙이지 원 빌드 receipt가 아니다. 원 archive 파일 존재 주장과 구체적 실행의 시각/장소/입력 주장은 분리한다.

**Q3. 재빌드 사건.** A02 API v1 규칙상 build ID integer와 log/artifact/attestation 경로가 있다. 이 버전이 실제 Debian deployment와 같은지는 미확인. A06 debrebuild는 buildinfo의 해시와 생성 artifact를 비교하므로, buildinfo가 가리키는 해시와 당시 배포 Packages 해시 일치도 추가 확인해야 한다. A01은 archive 기반 재빌드, 여러 worker 및 독립 재빌더 필요성을 설명. 대상 API/목록은 F03/F04/FRP01–08 실패, JSON detail F10/F11 실패. 공개 로그 R01–04는 다른 패키지 4개로만 비교했다. R02의 dsc 해시 433ff07730c28d6a4fa0b29f2203c9f0a705957e0d46807f640532a8bd3166c8 는 입력 지문이지 산출 지문이 아니다. 원 산출 해시와 별도 재빌드 결과 연결은 0/8 확인, 기준 2개 미충족.

**Q4. 재게시와 재시도.** A03 통계의 lam-runtime/lam4-dev/liblam4t64 세 링크를 따라가면 동일 원 로그 151245. 숫자 세 개가 아니라 세 표시→한 관측 계보→한 실제 빌드 단계 작업이다. D06/M02는 동일 artifact/version/arch/size/hash이지만 원 실행 ID는 불명: 동일 산출 표시까지 확정, 같은 실행 ID의 중복이라고 확대하지 않음. R02/R04 동일 worker 다른 작업은 별개 기록, 두 건 모두 빌드 수행이라고 할 수 없음. R03/R04는 다른 worker이지만 같은 서비스 namespace; 독립 운영자를 입증하지 못함. 동일 키의 retry ID 쌍은 확인 못했다. A03/A04 두 집계의 각 binary/source 수는 시각과 arch도 달라 합산 성공률 금지. Arch A09는 비교 구조만; JS placeholder로 실행 행 미확인.

**Q5. 실패 분류.** R01 원 .buildinfo HTTP 404는 원 입력 조회 실패(우리 도구 접근 실패 F*와도 구별). R02 dependency resolution/debootsnap 실패는 빌드 준비 실패. R03/R04 dpkg-buildpackage exit 2는 빌드 단계 실패이지 byte mismatch가 아니다. A02 GOOD/BAD 규칙에서 expected artifact 빠짐, 추가, 다른 바이트 등이 BAD가 될 수 있다. 미예약/만료는 시간/상태 이력 없으면 unknown으로 둔다. 실제 동일 키 hash mismatch 사례 미확인. 가짜 mismatch의 구체적 위험은 P05/P06의 source 버전만 같은 다른 binary arch/version과 A03 세 sibling binary labels. 다른 해시가 정상일 수 있으며 한 빌드의 여러 바이너리도 독립 실행이 아니다.

**Q6. 분야 비교.** E01 USGS가 NWIS와 WQP 두 portal에서 제공된다고 설명하고 E02 portal guide는 provider, organization, activity, method/timezone, result 관련 식별 정보를 제시한다. WQX2.2 legacy의 2024-03-11 이후 신규 USGS 자료 누락도 명시되어, portal에 없다고 원 측정 부재로 취급할 수 없다. 실제 한 관측의 양쪽 원 행(기관·ActivityIdentifier·site·시간·analyte·method·unit·value)은 이번에 확보하지 못했다. E04 NIST GLUCOSE.DAT와 GLUCOSE2.DAT는 동일 자료의 서로 다른 형식이라는 기관 목록 설명(행 재검산 없음, 관측소 대체 불가). E03 SP260-156 2004-06, SRM1575a pine needles: Table4 p14 원표 화면에서 Al NIST INAA 575±16 µg/g / USGS ICPAES 589±29 µg/g / certified 580±30 µg/g 확인. 같은 standard의 기관/방법별 값이지 같은 포털 복사본이 아니다. Table5 lab13a/b/c는 동일 lab의 방법 분기; Appendix D lab3 Al 580 mg/kg n=2(1 mg/kg=1 µg/g), 반복측정과 실험실 수 분리. NIST와 USGS 원 측정의 per-aliquot ID·장비별 기록·원 운영 경계 미확인; 기관별 측정 보고 2개까지만. E05 proficiency service 범위 설명은 별도의 실제 측정 보고서로 세지 않음.

**Q7. 주장 문턱.** (a) 페이지/해시 같은 표시의 중복: 동일 artifact key + 지문, 최소 추가 실행 증거 0. (b) 서로 다른 attempt: 같은 instance/native ID가 다르고 실제 시각/단계 확인; 다른 패키지라면 같은 대상 재시도 주장을 금지. (c) 바이트 일치: 고정 배포 키와 buildinfo hash를 재빌드 결과 hash 및 실제 사건으로 조인; 원+재빌드 두 생성 사건을 확인하는 조건. (d) 독립 운영자 두 곳: 서로 다른 조직의 통제·실행 receipt와 동일 비교 키가 필요. 같은 worker 이름 차이나 서로 다른 URL만으로 부족. (e) 확인된 실행 하한과 미상 상한을 분리. 이 조사에서 target 8자리의 실제 실행 수 상한 미상, 확인 하한 0(실제 0이라는 뜻 아님); comparison 4 attempt records, 2 build-stage attempts, 원/재빌드 byte-match 0건 확인. 같은 대상 독립 운영 조직 성공 0건 확인. 따라서 독립 성공률 미산출. 반환 문장별 근거는 claims.csv.

## 상충하는 설명과 선택 조건

- 배포자 관점: 특정 artifact의 공인 지문이 중요. 배포 파일과 buildinfo가 일치하더라도 어떤 독립 운영자도 재현했다는 결론은 별도다.
- 재빌더 관점: 실패 통계를 binary별 집계하는 것은 영향받는 배포 산출물 표시로 유용하다. 그러나 A03의 3 labels→R04는 실행 사건 수로 바꾸면 틀린다. attempt history가 없으면 한 current row가 여러 과거 시도를 압축했는지도 알 수 없다.
- 이용자 관점: 링크가 추가될 때 새로운 검증 범위인지, 다른 표시인지, 반대 근거인지 구별해야 한다. 동일 artifact의 언어별 페이지는 접근성을 높이지 증거의 독립성을 높이지 않는다.
- 정상 대조를 찾기 위해 target 목록/API·buildinfo 후보 8×2, archive version pages 및 buildd를 시도했다. 성공 원 로그·attestation을 얻지 못했으므로, 실패 표본으로 전체 재현률이나 '성공도 모두 같은 작업'을 추론하지 않는다. 같은 키의 다른 환경 재빌드 정상 성공과 재시도 실례는 다음 확보 우선순위다.
- 관측소 포털의 실제 행 조인은 미완; 실험실 보고는 두 기관 측정값과 한 lab의 복수 방법을 함께 보여주는 반례다. 같은 시료와 공통 reference를 공유한 측정은 모든 오차 요인까지 통계적으로 독립이라고 말할 수 없다.

## 조합 조건·비용 (설계 추론, 제품 형식 미결정)

대안 A: 대표 링크+짧은 scope/lineage note만 제공. 유지 비용 적지만 사용자가 실제 실행 수를 묻는 경우 원 기록 조인이 필요. 대안 B: artifact key–event key–display link 관계를 query-time에 추적하고 반대 근거도 연결. 키 정규화, 리다이렉트·만료·version 재검증 비용이 생긴다. 대안 C: 신뢰 조직·입력/산출 지문·서명 receipt까지 확보했을 때만 독립 성공 문장을 반환. 더 느리고 빈 답이 많으나 독립성을 과장하지 않는다. 함께 쓸 수 있는 조건은 A에서 '동일 artifact 표시'와 '실행 미상' 표시, B를 질문에 따라 작동, C는 높은 주장 문턱의 선택 옵션. 특정 DB schema/수집기/검색 최종 UI는 정하지 않는다.

원장 sources.jsonl 70행: 직접 읽은 34행(재게시 중복 4, 제한적 JS 화면 1 포함), 보수적 고유 실질 열람 29. 이 수는 엄격 과제 유형 충족과 다르다. 동일 스냅샷의 배포 당시 원전 0/6; 대상 별도 재빌드 0/6; API/표시·비교 규칙 4/4(좁은 API/표시 자체만 3/4); 비교 로그 4/2(모두 main frame 밖, 동일 키 재시도 미입증); 실제 기관 측정 원보고 1/4. 합계 종류별 최소치 미달. 36 접근 실패는 열람 수 불산입. 확인일은 2026-11-24 UTC 날짜, exact retrieval clock/원본 body digest 미확인.

| 약점 | 영향을 받는 주장 | 다음 조사와 원자료 | 판단이 뒤집히는 관측 |
|---|---|---|---|
| 공통 archive import와 서명된 Packages/Sources, 원 buildinfo 부재 | P01–P08의 동일 시점 배포·원 빌드 연결 | snapshot 월별 import→서명 Release→두 arch Packages 및 Sources→공식 buildinfo/buildd; 지문 저장 | 같은 resolved timestamp의 8자리 및 각 archive hash에 맞는 원 buildinfo receipt가 확인됨 |
| main frame 재빌드 ID·산출 해시/시도 이력/운영자 부족, BAD 비교 표본만 확보 | 적어도 두 파일 byte-match 및 별도 재시도·독립 성공 | 실제 instance API 목록 및 build ID 상세→raw log/artifacts/attestation, 같은 키 시도 목록 및 운영조직 증거 | 두 개 이상 target의 원/재빌드 hash 쌍 + 실제 사건, 동일 키 retry 및 독립 운영자가 직접 확인됨 |
| 관측소 동일 관측 행 부재; 분야 실제 원보고 1/4 | 포털 재게시와 독립 장비/생산자 분리의 실측 일반화 | NWIS와 WQP에서 동일 provider activity/site/analyte/time/method/unit/value 원 행; 추가 기관 PT 결과·measurement ID | 두 portal의 같은 원 ID·값과 서로 다른 실험실 raw measurement ID/장비가 실제로 매칭됨 |
