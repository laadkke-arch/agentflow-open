| 같은 대상·요구 | 멤버 타입·바이트 | 필요한 상대 항목 | 양립·필수·충돌·미확인 | 두 원근거 URL | 범위 |
|---|---|---|---|---|---|
| R1 보존, 대상 미동봉 | current type2, linkname=note.txt, size0, payload 없음 | 추출 후 src/note.txt B(경로 읽기만) | 링크 보존 성립 예측; 읽기는 대상 필수, 빈 루트에서 불성립 | [S01](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi), [T01](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_option_H_upper.c) | 한 멤버, source target 있음; 추출 미실행 |
| R2 보존, 대상 동봉 | current type2/0 bytes; note.txt type0/B | 같은 패키지 target 경로와 readable B | 링크+경로 읽기 보완·양립; current 일반파일 요구와 충돌 | [S01](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi), [T03](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_basic.c) | 두 멤버; 추출 미실행 |
| R3 역참조, 대상 미동봉 | current type0/B 예상 | 생성 시 source target B만 필수; 추출 후 별도 target 없음 | 경로 읽기+단독 bytes 양립; 링크 타입 충돌 | [S01](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi), [T02](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_option_L_upper.c) | 한 멤버; 일반 상대 경로, 역참조 생성; 미실행 |
| R4 역참조, 대상 동봉 | current type0/B 또는 type1/0 bytes, note 반대 가능; 두 독립 regular 가능 조건 별도 | type1이면 data-bearing 상대 멤버, type0이면 없음 | 경로 읽기 양립 예측; 독립 payload 조건부/정확판 미확인; 링크 자체 불성립 | [T09](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at), [C10](https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html) | 두 멤버; GNU order/dedup; -h만으로 두 data 보장 금지 |
| H1 실제 hardlink 두 이름 | 기본 첫 type0/B, 후속 type1/linkname archive 경로, 0 bytes; pax linkdata 예외 | type1 기본은 복원할 inode/상대 data; 추출 후 source pathname 참조 아님 | 동일 inode와 읽기 양립; 독립 data와 inode 관계는 별도; hard-deref는 관계 포기 | [S01](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi), [T10](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Lib/test/test_tarfile.py) | 한 쌍, 두 이름; 실제 hardlink CLI 미실행 |
| X1 같은 current 멤버가 링크 및 regular bytes | type2와 type0, 0과 B>0 동시 지정 불가 | 없음; 대상 추가만으로 같은 멤버 type 변경 못 함 | 논리 충돌 | [S02](https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5), [T00](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/src/tar.h) | 같은 논리 멤버 1개, 같은 이름/시점 t, 같은 최종 엔트리, 산출물 1개; POSIX 2024 원문 보류 |
| X2 같은 이름 멤버 중복 | 두 헤더, 각 type 독립 | 추출 순서/overwrite/filter | 원 계약 변경; 최종 경로 동시 타입 불가 | [S04](https://docs.python.org/3/library/tarfile.html), [T11](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link01.at) | 2개 멤버; 구현별 결과 미실행 |
| X3 보조 파일 또는 두 배포물 | 각각 type2, type0 | 보존판 target 동봉; 수신자 선택 | 다른 경계에서 보완; 원 계약 해소 아님 | [C01](https://github.com/libarchive/libarchive/issues/1034), [C10](https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html) | 이름/패키지 수 변경, 설계 합성 |

| 조합·버린 근거 | 유지할 주장 | 다시 열 결정 | 바꾼 계약·대가 | 회복할 첫 URL |
|---|---|---|---|---|
| P - S02(형식) | C01 요청, T03 추출 기대 | typeflag/linkname/size 규범 문장을 보류 | 일단 링크 객체+대상이라는 목표만; 형식 검증 추가 | https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5 |
| P - C01(요구) | S02 타입 구분, T03 기대 | 실제 보존자가 이 선택을 원한다는 근거 회복 | 선택지로만 남기고 기본값 결정 보류 | https://github.com/libarchive/libarchive/issues/1034 |
| P - T03(시험) | S01/S02 규칙, C01 요구 | 동일 판에서 링크+대상 추출·내용 읽기 기대 약화; 실험 필요 | 새 루트에서 readlink/open 비교 | https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_basic.c |
| D - S01(형식/옵션) | C10 실제 목표, T09 역참조+hardlink 기대 | --hard-dereference 정확 옵션·규격 문장 보류 | data-only acceptance 유지, CLI 채택 보류 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi |
| D - C10(요구) | S01, T09/T10 가능성과 함정 | 실제 배포자가 링크를 전혀 원치 않는다는 판단; C02는 별도 수신 사례로 유지 | regular-only 선택지 유지, 목적 우선순위 미결 | https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html |
| D - T09(시험) | C10 당사자 보고, S01 옵션, T10 다른 도구 기대 | 같은 GNU 소스의 -h dedup 회귀 기대; 동판 재검사 | 독립 payload 검사 필요, 다른 도구 테스트를 대신 쓰지 않음 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at |
| P+D - S02(형식) | C01+C10 다른 목적, T03+T09 기대 | 동일 멤버 강한 충돌의 규격 근거; S04 정책만으로 대체 금지 | 두 산출물의 개념적 대안, 형식 채택 보류 | https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5 |
| P+D - C10(요구) | 보존 요구 C01와 타입 차이, C02/C13 별도 배포 사례 | 두 번째 배포물 실제 원소비자 요구/수신 비용 | P 유지, D는 옵션; 불필요한 이중 생성 피함 | https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html |
| P+D - T09(시험) | 서로 다른 요구, 형식 경계, T03 | standalone의 GNU -h 단독 사용 가능성 및 두 산출물 동일 B 검증 | P/D 검수 분리; D를 type0 검사 전 발행 금지 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at |

**분모와 단위.** 표1: 계획 4셀 + hardlink 대조 1 + 충돌·대안 3=8행. 형식·기대 근거를 읽은 행 8/8, 이번 실행 관측 0/5 (4셀+hardlink), 런타임 미확인 5/5, 정상 공석 0, X1~3은 논리/계약 합성(실행 관측 분모 밖). R1/R2의 0은 링크 payload의 정상 부재 예상이지 미수신 기록이 아니다. R4 type0/type1 선택은 구현/판별 조건 미확인. 표2: 예정 3조합×3제거=9, 작성 9/9, 실행 관측 0/9, 정상 공석 0, 재실행 미확인 9/9. 원장 43행, 산입 고유 34작업(규격·작성자 4, 구현·시험 14, 소비자·결정 10, BagIt 6), 비산입 9(실패 5, 성공 보조 4); 같은 계보의 여러 소스는 독립 재현으로 계산하지 않음. 웹 작업 횟수는 직접 판독 기록 43행, 검색/인덱스/재조회는 별도 정확 횟수 미기록. 개별 UTC 시각 미기록, 원장 기록 UTC와 열람일 보존. U-P, U-D 두 소비자 목표 2/2, 최초 공개 본문 2/2 접근(단 C01 수정 이력 미확인), 원 archive/수신 영수증 0/2. 

## Q1. 실제 요구와 불명 의도

- 링크 객체 보존: [C01](https://github.com/libarchive/libarchive/issues/1034), 2018-07-09 생성, 작성자 16:40:28Z 댓글: “I'm obviously trying to store a symlink.” 링크 자체를 저장하려 했으며 maintainer는 dereference와 header-only를 구분한다. target bytes 동봉 요구, 수신자의 링크 지원, 최종 archive 정상 여부는 판정하지 못함. 이슈 최초 수정판은 복구 미확인. 링크 문자열 데이터와 파일 내용 데이터를 혼동하지 않는다.
- 독립 내용 배포: [C10](https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html) 최초 교차 게시 2015-01-16, L50–56 “store the content of the files itself, avoiding all kind of links”. make dist/ustar, 긴 hardlink 경로 오류 보고, --hard-dereference를 사용. 실제 배포자가 링크 관계 포기와 파일 내용 전달을 선택한 사례. 정확 바이너리 버전 및 원본 archive digest 미수신. 후속 C11/C12 제안 패치 전후는 [정정 메일](https://www.mail-archive.com/bug-automake@gnu.org/msg04229.html) L22; 최초안 폐기, 수정안 수용·검증 미확인.
- [C02](https://github.com/Gentleman-Programming/gentle-ai/issues/4741) L161–177은 비어 있는 내용 배포 오류 보고(321 bytes/regular data 0, 수동 재생성 45.6MB/353 files)이나 숫자는 당사자 진술이며 독립 검증 아님. C05(Kopia), C06(Heroku), C13(Thrift)은 환경 차이. 동일 사용자에게 두 목적이 반드시 함께 발생했다고 주장하지 않는다.

## Q2. 포맷 단위와 raw/추출 차이

T00 posix_header: name 100-byte field offset 0; size 12-byte field offset 124; typeflag 1 byte offset 156; linkname 100-byte field offset 157. [T00](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/src/tar.h) 구현 정의; typeflag는 regular '0'/NUL, hardlink '1', symlink '2'([S02](https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5) L193–219). ustar 일반 파일의 size는 실제 data byte 수, data는 512-byte block padding(패딩은 원 payload 아님); linkname은 링크 경로, 기본 link size0. pax x/g 확장 헤더는 적용 대상 다음 논리 멤버의 속성을 덮거나 보완(S02 L300–311); pathname/linkpath 확장은 새 사용자 파일 하나를 같은 이름으로 동시에 만든 것이 아니다. 최신 [POSIX pax 원문](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html) 403, 구판 [S05 재게시](https://man7.org/linux/man-pages/man1/pax.1p.html) L1318–1463,998–1002의 ustar size와 pax linkdata 예외는 보조. 현행 규범 강도는 보류. T04 [pax test](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/libarchive/test/test_write_format_pax.c) L59–74,162–164 size8/data 12345678 기대, T05 AE_IFREG/AE_IFLNK 분리; raw byte 위치는 T00, T08 size321/0은 reader 기대. T03은 추출 결과이며 archive header 관측으로 바꾸지 않는다.

## Q3. 네 셀과 대상 필요성

고정 입력: source src/note.txt=B (예: 5 bytes NOTE\\n), src/current -> note.txt, ordinary relative path, 변경 없는 snapshot t, 빈 추출 루트, target readable, 권한 및 symlink 지원. A=readlink/lstat 검사, B=open().read() 동일성, C=해당 archive 논리 멤버에 독립 일반 payload와 final lstat regular. 동봉은 원래 target의 archive 멤버 유무, source에서 target 존재와 별개. 표1 R1~R4가 예측. -H와 -L 범위 차이(T01/T02); -L 시 dangling fixture가 링크 유지되는 기대(T02), 하지만 고정 입력은 source target 존재. 실제 extraction이 링크 지원 안 하거나 외부 파일/권한이 있으면 A/B 달라짐. R2에서는 target을 빼면 B만 상실(R1), A는 유지. R3에서는 생성 시 원 bytes가 필요하지만 archive에 원 target 이름은 불필요. R4는 GNU dedup 반례(T09; C03, C10), 따라서 -h+--hard-dereference와 member 검사 필요. 이중 payload와 내용 접근은 서로 다른 acceptance다.

## Q4. 충돌을 증명하는 경계와 풀 수 있는 계약

고정 조건: 이름 src/current, 동일 논리 멤버 1, 동일 시점 t(추출 완료 직후), 동일 최종 POSIX directory entry(같은 루트), 산출물 1개, B>0. L: type2·linkname=note.txt·lstat symlink; D: type0·payload=B·lstat regular. 하나의 1-byte typeflag가 둘일 수 없고 한 시점 lstat 결과의 파일 종류도 동시에 둘일 수 없다. stat(current)가 regular인 경우는 따라간 대상의 type을 관측한 것으로 L과 양립하지만 D를 증명하지 않는다. 이름 중복은 물리 멤버 2개로 변경, S04 getmember 마지막 선택(추출 일반화 금지), S03 -k 기존 보호, T11 자기 링크 중복 시험은 순서 정책 필요성을 지지. 동일 이름을 다른 시간에 재사용해도 t를 바꾼 것이다.
- P: 링크+target 동봉, 보존자와 경로 앱 둘 다 이익; 링크 미지원 수신자/단독 regular 요구면 부적합.
- P + 보조 current.copy: 같은 패키지에서 이름 경계 변경, 앱이 별도 이름을 쓰거나 매핑 필요; 원 경로 regular 요구 그대로라면 실패.
- P와 D 별개 배포물: 같은 snapshot과 검증 manifest, 각각의 수신 목적 보장 대상으로 삼음. 수신자에게 두 파일을 강제하지 않고 필요한 판을 선택; 파일 수 증가·동기화 책임. 단일 산출물 제약이면 철회. C04 기존 디렉터리 링크를 남기는 다른 환경, C06 Windows 배포, C08 archivetar 정책은 다른 요구 경계의 사례. 허용 여부와 비용 실측 없음.

## Q5. 실제 하드링크 대조

동일 inode의 두 이름 src/a, src/b를 생성한 별도 입력. symlink는 다른 경로 문자열을 가진 별도 객체, hardlink는 이름들이 동일 st_dev/st_ino의 regular inode를 가리킨다. 기본 GNU tar는 원본 B 한 번, 이후 type1 linkname(archive name); [S01](https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi) L10235–10327 one/jeden 각 4 bytes 예와 hard-dereference 두 일반 멤버. [T03](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_basic.c) L43–62, [T06](https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/libarchive/test/test_write_disk_hardlink.c) L223–257 inode 기대; T07 대상 누락 경고, T08 size321/0; T10 L2088–2098 dereference=True regular 기대는 CPython 별도 도구. GNU exact --hard-dereference 단위 시험 실행과 동판 결과는 미확인. 복원 후 이름 a 삭제는 b를 dangling으로 만들지 않음(동일 inode의 다른 이름이 남음); 반대로 archive 안 type1 복원은 상대 inode/data resolution 필요. 원본 멤버 포함의 의미는 extractor의 선택 추출/fallback/기존 대상 정책마다 다르므로 전체 archive에서 b만 선택할 때 반드시 실패한다고 일반화 금지. pax linkdata 예외(S05)는 hardlink type1이 항상 payload0이라는 과잉 주장 철회; symlink type2와 regular type0 동시 표현의 반례는 아님. C10, C13은 hardlink도 배포 portability 문제라는 당사자 보고.

## Q6. BagIt의 내용/참조/검증

[RFC8493 B01](https://www.rfc-editor.org/rfc/rfc8493) §1.3, §2.1.3, §2.2.3: complete=요구 파일 존재, valid=complete+checksum 검증. payload manifest는 경로별 checksum. fetch.txt는 absolute URL, 길이 octets 또는 '-', 예정 payload path를 기술한다. fetch의 각 path는 모든 payload manifest에 포함되어야 한다; tag 파일 fetch는 금지. §4.2 예시 data/23364a.tif, 216951362 bytes 및 MD5 값; 예시의 bytes 직접 수신하지 않음. URL만 있다고 현재 payload를 보존했다고 하지 않는다.
- LOC [B04](https://digitalpreservation.gov/series/challenge/data-transfer-tools.html) L40–48 holey bag을 후속 전송 작업으로 기술; [B05](https://digitalpreservation.gov/about/resources.html) L61–91 validator/retriever 도구 역할. 미수신 payload는 계획된 파일, 실제 파일 존재 및 checksum 확인 후 완료. 현재 LOC 운영 적용 및 원영수증 미확인.
- APTrust [B03](https://docs.aptrust.org/preservation-services-docs/workers/ingest/validator/) L644–649 validator는 fetch.txt 불허 및 파일/manifest 확인; [B06](https://docs.aptrust.org/dart-docs/dart3/users/bagit/customizing/) L665–677 제작 도구의 설정과 수신자 정책은 별개. [B02](https://bagit-profiles.github.io/bagit-profiles-specification/) 1.4.0 L55–65 Allow-Fetch.txt, Fetch.txt-Required, Data-Empty는 프로필의 별도 제약. 동일 BagIt lineage로 기관별 인수 조건을 일반화하지 않는다.
- 정상 공석: 실제 0-byte file의 digest/길이와 존재 검증; 미수신: fetch에 기재되었으나 payload 미도착; 미실행: 아직 checksum 검증하지 않음; 적용 밖: 수신 프로필이 fetch 불허; 미확인: 길이 '-' 또는 수신 증거 없음. RFC fetch 참조는 filesystem symlink와 다른 전송 명세다. 두 목적의 양립 여부는 수신 경계와 시점이 결정한다.

## Q7. 제거와 재조합

표2 및 assemblies.md. P/D/P+D 세 묶음의 형식(F), 실제 요구(U), 동판 시험(T)을 하나씩 제거했다. F를 버리면 타입 충돌 규범의 강도를 낮춰도 U 목적 차이는 유지; U를 버리면 기술 가능성은 유지하되 사용자의 우선순위 주장을 철회; T를 버리면 포맷 규칙과 실제 요구는 남아도 구체 도구 예상/회귀를 보류. 회복 URL을 각각 첫 행동으로 지정. 관련 연구 결과를 삭제하거나 설계자에게 미확인 실행 결과를 정답으로 주지 않는다. 비용은 추가 이름/패키지/해시 확인이라는 계약상 의무만, 실제 시간·저장 증가량 미측정. 최종 설계자에게 세 독립 packet과 경계, 선택 조건, 반례, 삭제 후 유지 주장, 복구 URL을 넘기며 한 안을 강제하지 않는다.

## 검증 상태와 제한

자체 상태 PARTIAL: 22 및 4/7/6/5 수량 기준 충족, 두 실제 사용 목적 확보, 4+1 예측/9자리 제거 작성. 다만 2024 POSIX 원규격 및 GNU 공식 현행 문서 직접 접근 실패, GNU --hard-dereference 동판 시험/정확 4셀 실행 미확인, libarchive #1034 수정 전 최초판 확인 미완료. 미러 원저작과 공식판 동일성 단정 금지. 신규 제품 실행하지 않았으며 검증 지시 SELF_CHECK에 남김. 독립 검토 없음. 세 약점 표는 다음의 재개 우선순위다.

| 가장 중요한 불일치·약점 | 영향받는 판단 | 다음 조사의 첫 원자료·행동 | 결론이 바뀌는 관측 |
|---|---|---|---|
| POSIX 2024 403, GNU 현행 공식 매뉴얼 타임아웃; 구판 재게시와 미러 | Q2 규범 및 Q5 pax linkdata 예외의 정확 판 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html 직접 열람, size/typeflag/linkpath/linkdata 대조; GNU 공식 Formats 직접 재시도 | 해당 판이 동일 논리 멤버에서 symlink+일반 payload 허용하거나 hardlink data 규칙 변경 시 범위 수정 |
| GNU -h dedup은 시험 기대 및 오래된 당사자 보고, --hard-dereference 정확판 시험 미실행 | R4 및 H1 독립 bytes, 추출 후 inode | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at 와 승인된 GNU/libarchive 판의 4셀·1쌍 실험 | R4 current type1/0이면 단독 payload 불합격; -h+hard-deref에서 type1 남으면 해당 도구/판 대안 철회 |
| 원 archive·수신 영수증 미수신, C01 초판 수정이력 미확인, 기관 정책의 실제 인수 미관측 | U 요구/현장 성공, BagIt 완료 | https://github.com/libarchive/libarchive/issues/1034 작성자 최초판/댓글 및 archive 제공 여부 확인; C10 원메일·기관 receipt | U-P가 target 내용만 원했다는 작성자 정정 또는 fetch-only 상태를 해당 기관이 완료로 정의하는 고정판 발견 시 계약 재판정 |
