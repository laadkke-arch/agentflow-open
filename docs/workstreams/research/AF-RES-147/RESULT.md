## 표 1

| 계열·질의·셀 키 | 안정 URL·고정판·절 | 사건 시점·사용자가 보존할 값 | 원전 판독값·가용성 | 자연/구성·미확인 |
| --- | --- | --- | --- | --- |
| tzdb · TZ-A · Asia/Beirut | [IANA](https://www.iana.org/time-zones) · [2023b Rule/Zone](https://github.com/eggert/tz/blob/71faa2a55db2c9f21f4099b58c28536673982e0a/asia#L2722-L2729) · [2023c Rule/Zone](https://github.com/eggert/tz/blob/ddb8cf09d54ecc486ed6665edcdd642abccd4eef/asia#L2750-L2759) | 2023-03-26 12:00 UTC. P1은 UTC 순간, P2는 EEST 문자열을 보존 | 2023a +03:00 EEST → 2023b +02:00 EET → 2023c·d +03:00 EEST. 네 TZif 정상 판독 | 자연 변화 두 경계. 2023b P1은 14:00으로 표시. P2의 EEST 보존은 거절 |
| tzdb · TZ-N · 같은 Zone의 인접 순간 | [IANA](https://www.iana.org/time-zones) · [2023b Zone](https://github.com/eggert/tz/blob/71faa2a55db2c9f21f4099b58c28536673982e0a/asia#L2728-L2729) | 2023-03-19 12:00 UTC. 같은 두 보존조건 | 4판 모두 +02:00 EET. 사용자 조건에 따라 P1 승인, P2 거절 | 자연 대조. 동일 파일 개정이 모든 시점의 답을 바꾸지 않았다 |
| tzdb · TZ-U1 / TZ-U2 · Chicago / Shanghai | [IANA](https://www.iana.org/time-zones) · [2023a Chicago](https://github.com/eggert/tz/blob/f24b84a13556c12441dd55c323f9a8fd3b6fbbee/northamerica#L443) · [2023a Shanghai](https://github.com/eggert/tz/blob/f24b84a13556c12441dd55c323f9a8fd3b6fbbee/asia#L653-L655) | 2023-01-15 12:00 UTC. P1은 현지 시각, P2는 CST 문자열 확인 | 4판 모두 Chicago −06:00 CST, Shanghai +08:00 CST | 자연 미열람 대조. 같은 약어로 지역·오프셋을 판별할 수 없다 |
| CLDR · CL-A · en_ZA/latn/decimal | [CLDR 목록](https://cldr.unicode.org/index/downloads) · [43 en_ZA](https://github.com/unicode-org/cldr/blob/66d15bfc1b4762b38bf1330319534e237d4670a3/common/main/en_ZA.xml#L241) · [43.1 en_ZA](https://github.com/unicode-org/cldr/blob/37d524354422f46731db74f3bd6b3f46516c3ced/common/main/en_ZA.xml#L241) · [44 en](https://github.com/unicode-org/cldr/blob/9ffd5f7e749b838c67f5feaf85f67f9d1554303f/common/main/en.xml#L4947) | 43→43.1→44. P1은 12.5의 값, P2는 U+002C를 보존 | U+002C → U+002E → U+002E. 44부터 로컬 상속 표시, 실제 원점 en | 자연 변화 한 경계, 값 유지·원점 변경 한 경계 |
| CLDR · CL-N · en_ZA/latn/group | [CLDR 목록](https://cldr.unicode.org/index/downloads) · [43](https://github.com/unicode-org/cldr/blob/66d15bfc1b4762b38bf1330319534e237d4670a3/common/main/en_ZA.xml#L242) · [43.1](https://github.com/unicode-org/cldr/blob/37d524354422f46731db74f3bd6b3f46516c3ced/common/main/en_ZA.xml#L242) · [44 en](https://github.com/unicode-org/cldr/blob/9ffd5f7e749b838c67f5feaf85f67f9d1554303f/common/main/en.xml#L4948) | 같은 symbols 부모. P1은 1234, P2는 U+002C 보존 | U+00A0 → U+002C → U+002C. 43.1에서 쉼표는 그룹 역할 | 자연 인접. 이 셀도 공지에서 범위가 노출됐다 |
| CLDR · CL-U1 / CL-U2 · ar_EG/arab/group, de_DE/latn/decimal | [CLDR 목록](https://cldr.unicode.org/index/downloads) · [43 ar](https://github.com/unicode-org/cldr/blob/66d15bfc1b4762b38bf1330319534e237d4670a3/common/main/ar.xml#L6051) · [44 root](https://github.com/unicode-org/cldr/blob/9ffd5f7e749b838c67f5feaf85f67f9d1554303f/common/main/root.xml#L3040) · [de 경로](oracle.csv) | 두 번호 체계와 각자의 기호 역할. P1 표시에는 해당 체계의 글리프 사용 | 그룹 U+066C, 소수 U+002C 모두 4판 유지. ar_EG의 실제 원점만 44에서 ar→root | 자연 미열람 대조. en_US/latn/group의 U+002C와 de_DE 소수의 U+002C는 값이 같고 역할이 다르다 |
| 선행 교정 · CAL-143-785/786/787 | [7.8.6 npm 배포](https://registry.npmjs.org/simple-statistics/-/simple-statistics-7.8.6.tgz) · [고정 인계의 원장 행](evidence/calibration.json) | 고정 CJS require, quantile/vec-duplicates/p0/direct | 7.8.5와 7.8.7에서 벡터 [8, 1, 8, 3.5, 1]. 7.8.6은 두 실측에서 MODULE_NOT_FOUND로 값 미확인 | 선행 관측 인용. 새 32셀과 구성 실패에서 분리 |
| 단위·분모·결측 | [발표와 경계판](editions.csv) · [32셀 원본 위치·raw trace](oracle.csv) | 2계열×4판×4셀. 8 공지·8 인접·16 미열람 예정 | 32개 판독·0셀 결측. 24 인접 판/셀 비교 중 효과 변화 4·불변 20 | 최초 공개 초 및 두 CLDR 유지보수판의 정식 XML 발표 시각 미확인. 공식 tar/ZIP과 태그 아카이브의 바이트 동일성 미확인 |

## 표 2

| 저장안·가린 필드·사건 ID | 당시 전달값·현재 적용 판정 | 기대값·실제값·근거판 | 오승인/잘못 보류/정당 보류·이유 | 반례 URL |
| --- | --- | --- | --- | --- |
| C · 전체 · D-tzdb-2023c-TZ-A-OLD-P2 | 당시 EET, EEST 보존 거절. 2023c 현재 값 EEST는 승인 | 옛 기대·실제 EET, 근거판 2023b | 정상 복원. 최신판의 같은 요청 승인이 옛 거절에 영향을 주지 않았다 | [2023b 규칙](https://github.com/eggert/tz/blob/71faa2a55db2c9f21f4099b58c28536673982e0a/asia#L2722-L2729) |
| A-url · D-tzdb-2023b-TZ-U2-P1 | Shanghai의 현지시각으로 15:00 승인 | 기대 20:00. 실제 URL의 첫 2023a Beirut +03:00 근거를 사용 | 오승인. URL은 같지만 지역·순간·판 모두 다름 | [Shanghai Zone](https://github.com/eggert/tz/blob/71faa2a55db2c9f21f4099b58c28536673982e0a/asia#L653-L655) |
| C · 관측 판 · S-NEW-OBS | 새 프로젝트에서 12,5 승인 | 기대 12.5 f2, 실제 f1의 쉼표. 판 열은 가려짐 | 오승인. 최신 f2의 새 요청에 옛 관측 사용 | [구성 원문 f1/f2](replay/fixture_source.json) |
| C · 세부 위치 · S-ALT-B | 그룹 쉼표를 소수 기호로 승인 | 기대 역할 불일치 거절. 실제 section-a 소수 쉼표의 12,5, f1 | 오승인. 같은 판·논리 키의 다른 절에서 문자는 같고 역할은 다름 | [구성 원문 dual](replay/fixture_source.json) · [LDML 번호 기호](https://www.unicode.org/reports/tr35/tr35-69/tr35-numbers.html#Number_Symbols) |
| C · 입력 키 · S-INPUT | 같은 프로젝트의 변경된 문자 보존도 승인 | 기대 마침표 보존 거절. 실제 기존 쉼표 보존 승인을 f1에서 사용 | 오승인. 입력 JSON은 남고 이 재생의 캐시 키에서 비교하지 않음 | [요청 원장](events.jsonl) |
| C · 요청판 · S-NEXT | latest 요청에 쉼표 형식 12,5 승인 | 기대 12.5 f2, 실제 12,5 f1 | 오승인. 정확한 개별 관측이 있어도 옛 요청 캐시를 읽음 | [구성 원문 f1/f2](replay/fixture_source.json) |
| C · 관측 시각 · S-KNOWN-BEFORE | 틱 1 기준으로 이미 안다고 응답 | 기대 관측 없음, 실제 틱 2의 f1 값을 사용 | 시점 오판. 현재 적용값이 맞아도 당시의 지식으로 소급할 수 없다 | [관측 시점·틀](events.jsonl) · [Memento §2.1](https://www.rfc-editor.org/rfc/rfc7089.html#section-2.1) |
| C · 실패 종류 · S-T4 / S-ABS2 | 첫 일시 실패 재사용에서 유형 불명. 또 다른 요청은 여전히 보류 | 기대 temporary 및 key_absent. 실제 S-T4 이유 미분류. S-ABS2는 재취득 후 f1 부재 확인 | 정당 보류, 잘못된 이유 2건과 불필요한 재취득 1건 증가. 두 사건의 회복 여부가 다름 | [실패 주입](replay/provider.py) · [HTTP 캐시 §4](https://www.rfc-editor.org/rfc/rfc9111.html#section-4) |
| C · 근거 연결 · S-H-DUP-PROOF | 두 모델 모두 당시 12,5와 승인 재생 | 기대 f1 source-b. 연결 가림 후 값·상태 일치, 실제 어떤 출처를 택했는지 공란 | 값 재생 성공, 증빙 결손. source-a도 같은 답을 낼 수 있음 | [구성 원문 same](replay/fixture_source.json) · [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/#qualifiedRevision) |
| B/C · S-RECON / S-OUT-NOW | B는 원 입력·컷오프로 f1 후보를 계산. C는 당시 승인·근거를 재생. f3 현재 적용은 보류 | B의 후보와 C 저장값은 12,5. 현재 f3은 접근 단절로 보류 | C 현재 정당 보류. B 후보는 실제 전달 증거 부족 | [구성 요청 및 원장](events.jsonl) |
| 단위·분모·결측 | [답 원장](answers.csv) · [단일 필드 가림 전수](ablation.csv) · [사건 전후](evidence/transitions.jsonl) | 밀집 첫 실행 모형/정책당 현재 96건(64 프로젝트 입력+32 재시도) 및 과거 112건(64 유일 입력). 구성·역순 각 37개 질의 | C 완전안 밀집 112/112 재생. A/B의 112건 보류는 당시 전달 증빙 결손. 표에는 네 오승인 유형·지식 오류·보류 비용·근거 손실의 예를 표시 | 7개 가림을 같은 네 질의열에 적용. 원전 32셀 결측 0. 미지 선호·근거 손실은 출력 수치 결측과 별도 |

## 표 3

| 질의열·캐시 | 중복·회복·다른 프로젝트 영향 | 조회·취득·저장 bytes·경과 | 이득이 있었던 최소 필드·대가 | 설계 가설·미측정 |
| --- | --- | --- | --- | --- |
| 첫 등록·북마크, 3안 | 주소만 저장. 첫 카탈로그 보류, 북마크 URL 반환, 취득 0 | IANA 한 URL의 등록 직후 논리 40 B 공통. A/B/C 파일 20,480 / 28,672 / 40,960 B | 주소만으로 링크 보관 충족. 빈 스키마의 페이지 비용만 다름 | 취득·문서 희소성을 모르는 등록에서는 관측 필드가 즉시 이득을 주지 않았다 |
| 밀집 · 요청 재시도 · 최초/보존 | A/B 현재 오승인 0, 과거 112 보류. C 현재 오승인 0, 과거 112 재생 | 212 질의/상태. 최초 A/B/C 취득 96/32/32, 파일 open 186/62/62, 읽기 B 37,163,112/12,387,704/12,387,704. 논리 309/8,275/58,335 B. 최초 536.474–581.069 / 211.931–221.542 / 306.704–367.632 ms. 보존 취득 96/0/0 | 정확판·셀 관측은 B부터 재사용. C의 요청은 B보다 50,060 B 더 저장하고 과거 답을 증명 | 같은 prepared 소스, Python 3.12.14·SQLite 3.53.1, 응용 프로그램 파일 read |
| 양끝 · 요청 재시도 · 최초/보존 | 매 비교 대상의 A/B 과거 보류 48, C 재생 48. 판 교체는 중간에도 동일 | 100 질의/상태. 최초 A/B/C 취득 48/16/16, 읽기 B 18,581,559/6,193,853/6,193,853, 논리 309/4,189/29,053 B. 최초 314.169–314.653 / 121.231–137.225 / 158.365–170.015 ms. 보존 취득 48/0/0 | C의 역추적 비용은 B보다 24,864 B. 중간 두 판은 발표 피드를 받았고 원문 읽기는 0 | 양끝 판에도 동일 요청 재시도와 두 프로젝트가 있어 B가 재사용 |
| 구성 · C · off / retry / TTL 3틱 | 중복 전달 쓰기 0. off/retry는 틱 5 회복, TTL은 두 회복 건을 틱 5에 보류하고 틱 6 회복 | 각 37 질의. 취득 30/20/18, 원문 읽기 20,925/12,555/12,555 B. 논리 19,742/17,418/16,864 B. DB 61,440/53,248/53,248 B. 31.816–32.665 / 31.482–32.847 / 34.678–35.994 ms | 정확 범위와 실패 종류를 기록하니 retry가 10회 절감. 한시 보류는 2회 더 줄였고 읽기 B는 동일 | TTL 3틱과 두 회복 입력만 시험. 실제 장애 분포·재시도 과금 미측정 |
| 구성 · A-url · retry | 중복 전달 쓰기 1, 틱 6 첫 실패 고착 1, 다른 프로젝트의 다른 키 근거 사용 5, 늦은 f1이 f2 두 요청 오염 | 37 질의. 취득 7 / 5,022 B. 논리 452 B, DB 20,480 B, 8.277–8.777 ms | 취득 비용은 낮고 오승인 11·잘못 보류 7건. A의 정확 재취득과는 다른 정책 | 같은 링크 마지막 응답의 무제한 재사용을 분리 검증 |
| 단위·분모·결측 | [두 번의 레코드](costs.csv) · [실행 대조](evidence/receipts.json) · [취득·전처리](evidence/artifacts.json) | 배치당 질의 건, 앱 취득·open 건, B, SQLite 페이지 4,096 B, 경과 ms 2회 범위. 136배치/회×2 | 논리·물리 저장과 런타임 소스 읽기는 별도. 8개 Git 아카이브의 HTTP 응답 본문 합 213,933,449 B | 런타임 외부 전송·사람 시간·자동 발견 피드의 원가 미측정. 전처리·HTTP는 별도 영수증 |

## Q1 · 무엇을 되묻는가

안정 URL은 등록 주소다. 정확한 답에는 발행판과 입력의 위치가 뒤따른다. tzdb 2023b·d의 공식 이력 날짜와 UTC 발표 메일 날짜는 하루 차다. 2023c는 과거 2023a 값을 돌려줬지만 2023b의 값을 되돌리는 신규 정식 발행이었다. CLDR 43.1과 44.1은 정식 목록에 있고 공급자가 Git 태그를 배포 주소로 준다. 44의 초기 JSON npm 44.0.0과 정식 44.0.1에는 게시일 차이가 있다. 44.1의 numbers-full과 core npm도 9일 차다. 번호·데이터·포장·공개시각을 각각 기록해야 공급자가 하나의 날짜나 채널로 수렴하지 않아도 발행순을 재검토할 수 있다. [Q1-TZ · IANA 발표 및 날짜](editions.csv) · [Q1-CLDR · Unicode 모집 판정](evidence/recruitment.md) · [출처 원장](sources.jsonl)

## Q2 · 어떤 값을 판독했나

tzdb의 원시 `STDOFF`·`SAVE`·`EE%sT`는 로컬 오프셋과 최종 약어의 재료다. 각 판의 zic으로 fat TZif를 컴파일했다. 독립 평가 경로가 그 파일을 GNU date로 열었고 재생은 Python `ZoneInfo.from_file`를 사용했다. Chicago와 Shanghai의 CST는 14시간 차이다. 같은 판에서 `PRC`와 `Asia/Shanghai`는 동일 TZif이고 호환 별칭은 별도 위치에서 확인했다. 두 CLDR 판독기는 선택한 숫자 경로의 판별 부모 상속을 적용했다. 언어 별칭 sh→sr_Latn은 보조 원문에서 확인했다. CL-U1은 43.1의 `ar` 리터럴에서 44의 `root` 리터럴로 원점이 바뀌었고 U+066C는 그대로다. en_ZA의 43 소수와 en_US의 그룹은 같은 latn에서 ASCII 쉼표의 역할이 다르다. 고정 en Gregorian `hm` 기본의 U+202F와 43.1의 `alt=ascii` U+0020은 동시에 유효한 경로다. 이 둘을 값 하나로 정규화하면 공백의 보존 요구를 검증할 수 없다. [Q2-TZ · zic FORMAT](https://github.com/eggert/tz/blob/f24b84a13556c12441dd55c323f9a8fd3b6fbbee/zic.8#L536) · [Q2-CLDR · LDML 상속](https://www.unicode.org/reports/tr35/tr35-69/tr35.html#Parent_Locales) · [별칭·날짜·로캘 대조](evidence/origin-comparisons.json)

24개 인접 비교에서 tzdb 공지 3중 2, CLDR 공지 3중 1, CLDR 인접 3중 1에서 효력 값이 바뀌었다. 앞의 CLDR 인접 영향도 공지에 드러나 있었다. tzdb 인접 3쌍과 미열람 12쌍은 값 변화가 0이어서 해당 층의 변화 감지율은 산출 불가다. 값 불변이면서 원점만 바뀐 3쌍은 효력 값 변화 분자에 더하지 않았다. CPython·Go의 TZif 시험과 Babel·ICU의 번호 체계 시험은 각각 구현 계약을 확인하는 출처다. 이 실험에서 해당 외부 테스트 스위트를 실행하지 않았다. [Q2-IMPL · 네 독립 구현 원장](sources.jsonl) · [24쌍 재집계](evidence/receipts.json)

## Q3 · 어느 시점에 적을 것인가

등록에서는 URL만 받았다. 링크 열기와 첫 카탈로그 상태에 추가 관측이 필요하지 않았다. 정확한 자료를 열었을 때 관측에 원래 URL, 공급자 판, 논리 키·원문 위치, 확인시각, 결과 또는 구분된 실패를 남기면 같은 출처를 여러 프로젝트가 재사용할 수 있다. B는 이 수준에서 정확판 현재 질의와 보수적인 음성 캐시를 지원했다. 새 버전을 알려주는 피드는 관측 과정과 분리했다. 이전에 전달한 답을 회수해야 할 때 C의 전달 기록에 요청판, 프로젝트, 입력·보존조건, 선택한 관측과 전임 응답을 연결했다. 같은 관측에서 의미가 다른 두 프로젝트 판정을 만들었다. [Q3-LAYERS · SQLite 저장안](schemas.sql) · [판과 계열 URI의 구별](https://www.w3.org/TR/2017/REC-dwbp-20170131/#VersionIdentifiers) · [관측·결정의 관계](https://www.w3.org/TR/2013/REC-prov-o-20130430/#qualifiedRevision)

## Q4 · 어떤 재사용이 틀렸는가

A의 정확판 재취득, B의 정확판 관측, C의 근거 연결은 첫 밀집 96개와 양끝 48개의 현재 응답에서 모두 값과 근거가 일치했다. URL만으로 마지막 값을 이월한 A-url은 밀집에서 오승인 40·잘못 거절 32를 냈다. 다른 키/절 근거 사용 72 중 24건은 다른 프로젝트의 취득이었다. 과거 질의 112건에서 A/B의 안전한 보류는 실제 전달의 증빙을 요구하는 서비스 조건을 충족하지 못했다. C는 64개의 고유 입력에 대해 같은 답을 별도 결과로 남겼다. 처음 요청에 정해진 숫자값을 보존하는 일과 문자·약어를 그대로 보존하는 일은 서로 다른 결정이었다. B의 S-RECON에서는 호출자가 요청 조건과 컷오프를 제공해 같은 값을 다시 계산했고, C에서만 실제 전달 근거를 재생했다. [Q4-EQUAL · 사건 원장](events.jsonl) · [Q4-HISTORY · 기대값·당시값·현재값](answers.csv) · [Memento의 과거 자원](https://www.rfc-editor.org/rfc/rfc7089.html#section-2.1)

## Q5 · 실패가 유효한 범위

AF-RES-143의 7.8.6은 기록된 진입 방식의 실패다. 이번 구성의 즉시 재시도 가능 오류, 정상 parse에서 키가 없는 상태, 요구조건 미지, 접근 단절과 따로 두었다. 요청 시 재시도 C는 회복 즉시 S-T5와 S-FIRST5를 응답하고 관측 범위가 정확한 부재·고정 진입 실패만 유지했다. TTL은 두 회복을 한 틱 늦췄다. A-url에서 최초 실패를 얻은 S-FIRST는 마지막 틱에도 회복하지 않았다. A-url의 늦은 f1은 S-LATE-NOW와 S-LATE-P2에 옛 성공을 썼고 순서를 역전하면 오류가 나타나는 요청 위치가 바뀌었다. B/C는 같은 packet을 두 번 쓰지 않았고 C의 과거 답과 현재 f2에는 순서 영향이 없었다. f1이 컷오프 이전에 도착했는지는 순서에 따라 정확히 달라졌다. 불명 선호는 데이터가 있어도 보류했다. [Q5-FAIL · 구성 전후 원장](evidence/transitions.jsonl) · [Q5-CAL · 143 교정](evidence/calibration.json) · [HTTP의 캐시 키·음성 결과](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.1)

## Q6 · 필드가 빠졌을 때 바뀐 것

위치·관측 판·입력 키·요청판 각각에 오승인 사례가 있었다. 관측 시각은 적용값보다 과거 지식 여부를 지켰고, 실패 종류는 단순 보류보다 실패 설명·재취득 비용을 바꿨다. 관측 ID 연결이 없을 때 C가 보유한 값·결과는 재생 가능했지만 값이 같은 두 출처 중 사용한 쪽을 증명하지 못했다. 반대로 단순 북마크는 주소만으로 해결됐다. 신청자가 원래 입력을 제공하고 한 관측만 가능한 경우 B가 같은 값도 재구성했다. 입력 키의 손실은 필드 비교를 생략한 구현에서의 결과이며, 저장한 입력 본문을 다시 비교하는 정책에 같은 오류 수를 적용할 수 없다. 새 f3 열기가 실패해도 f1 성공의 과거 답과 f1 실패의 과거 보류는 복원됐다. [Q6-FIELDS · 가림 전수](ablation.csv) · [키 직렬화의 판 일관성 한계](https://peps.python.org/pep-0615/#pickle-serialization)

## Q7 · 어느 비용에서 이득이 바뀌는가

공급자 관점에서 43.1→44의 U+066C를 읽는 값 전용 소비자는 상속 원점 변경에 따른 답 수정이 없었다. 정확한 절을 인용하는 소비자는 같은 값의 근거가 달라졌으므로 관측을 갱신할 이유가 생겼다. 운영자 관점에서 URL 한 번 저장하는 사용에는 A/B/C의 논리값이 같고 물리 비용은 A가 작았다. 두 프로젝트의 반복 현재 질의에서 B는 A 대비 밀집 기준 24,775,408 로컬 B를 덜 읽고 7,966 논리 B를 더 저장했다. 전달 복원이 필요하면 C는 B와 같은 원문 분량을 읽으며 112건의 근거가 있는 과거 답을 제공했다. 전달 증빙 없이 현재 적합성만 요구하면 같은 질의에서 B의 SQLite 파일은 C보다 밀집 73,728 B 작았다. 비용 경과는 각 환경의 원문 파일 구성, 동기 쓰기, 캐시의 특성을 포함한다. [Q7-COST · 실제 비용](costs.csv) · [Q7-PREP · 준비 계측](evidence/artifacts.json)

교통 안내에는 발행·효력·갱신을 구별할 결과가 있다. National Rail의 같은 정기 주소는 5월판과 12월판의 시행기간을 안내하고 당일판의 전날 22:00 마감 기준을 따로 둔다. Bath Spa–Westbury 공지는 신고 15:59와 정상화·갱신 23:08을 동시에 보존한다. NSW TrainLink에서는 같은 출발 시각에도 수하물 위탁의 마감과 일반 승객의 도착 권고가 다르다. 통계/표준 쪽에서 BIPM은 영어와 프랑스어의 소수 표기 관행을 구별하고 SI 그룹에 점·쉼표를 쓰지 않는다. Eurostat은 사용자 화면에서 소수·그룹 기호 충돌을 해소한다. ONS는 같은 수치 시퀀스의 표기 정밀도를 요구한다. 가져올 수 있는 것은 시각·값과 표현·역할의 분리다. 실제 열차 운행, 원통계의 교정, 개인별 화면 설정은 이 근거 범위 밖이다. [Q7-DOMAINS · 정기 시각표](https://www.nationalrail.co.uk/travel-information/timetable-changes/) · [Bath Spa 사건](https://www.nationalrail.co.uk/disruptions/bath-spa-20261122/) · [NSW 승차 조건](https://transportnsw.info/regional-travel/booking-information/preparing-for-your-trip) · [CGPM 결의 10](https://www.bipm.org/en/committees/cg/cgpm/22-2003/resolution-10) · [Eurostat 구분문자](https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/data-selection-display/format-options) · [ONS 숫자 작성](https://service-manual.ons.gov.uk/content/numbers/writing-numbers)

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 공식 tar/ZIP 경로는 터널 403. 공급자 대응 Git 커밋으로 판독 | 선택한 원본 규칙·XML의 값은 확인했다. 패키지 빌드 또는 서명·채널 동일성은 미확인 | [IANA 서명 포함 원본](https://data.iana.org/time-zones/releases/)과 [Unicode Public ZIP](https://www.unicode.org/Public/cldr/43/)의 원본 경로에서 동일 셀 확인 | 같은 판·셀의 효력 값 또는 상속 경로가 Git 원본의 결과와 다름 |
| 미열람 12 경계에서 변화 0. 동일 판이나 위치에 대한 충돌은 통제 사례 중심 | 선택 열에서 필드 손실의 기전은 확인했다. 일반 변경 발견 능력과 운영 장애율의 분모는 없다 | 새로운 발표 창과 동일판 수정·재발행이 있는 다른 데이터 공급자로 고정 입력 비교 | 공지 없는 양성 또는 동명판 아래 서로 다른 원전이 동일 정책의 응답을 갈라놓음 |
| 발행 피드 제공, 로컬 준비 소스, SQLite 1환경, TTL 3틱 | 구체적 읽기·저장·보류 비용은 관측했다. 사람 비용·외부 전송·실제 TTL 최적합은 미측정 | 같은 읽기와 증빙 요구로 실제 HTTP 재검증 및 장애 trace 재생 | 원격 지연·변동 배치에서 B/C 또는 재시도/TTL의 실측 우열이 바뀜 |
