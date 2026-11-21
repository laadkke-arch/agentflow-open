# 검사 후보 초안: 최초판과 현재 공식 근거의 대조

상태: **DRAFT — 실행 전 부모 검토용**. 이 묶음은 A/P 실행이나 블라인드 판정이 아니다. 지정된 질문 16개의 최초판을 `generate.py --emit`으로 직접 읽었으며 모두 HTTP 200과 동결 해시 일치를 확인했다. 원문 본문·사용자 이름·프로필은 파일에 저장하지 않았다.

## 1. 준비된 후보와 빠진 근접 오답

양성 16개는 모두 고정014 실제 답 정답의 등급2/1에서 가져왔다. 무관 후보 16개는 공식 문서로 대상의 역할을 확인한 뒤 작업자가 구성했다. 48개 검사 슬롯 모두 실제 이름·URL이 있다. T006·T009·T030의 세 빈 슬롯은 `auxiliary_unjudged` 보조 후보로 채웠으며, `grade=null`, 예상 strict-N 역할 결측, strict-N·positive 분모 제외를 유지한다. **현재 엄격N으로 방어 가능한 초안은 10개**이며, 남은 6개를 성공 사례로 채우지 않았다.

| 질문 | 양성 / 등급 | N 슬롯 | 현재 strict-N 분모 | 이유 또는 범위 |
|---|---|---|---|---|
| T001 | Mattermost / 1 | Discord / 역사N | 포함 | 공식 클라이언트 수정·배포 제한과 공개 소스 요구 충돌 |
| T002 | Veusz / 2 | QtiPlot / 역사N | 제외·확인 필요 | 유료 바이너리 배포만으로 현재 비공개 소스를 확정하지 못함 |
| T003 | Bitwarden / 1 | Dashlane web-first / 작업자N | 포함 | 필수 Windows 독립 데스크톱 앱의 종료 |
| T004 | BiblioteQ / 2 | Librarika / 역사N | 포함 | 네트워크 없는 로컬 운영과 클라우드 서비스 충돌 |
| T006 | Discourse / 1 | N 미확보; Question2Answer 미판정 보조 | 제외 | 세부 기능은 Desirable이고 유료도 허용 |
| T007 | SoapUI / 1 | Postman v12 signed-out Lightweight Client / 작업자N | 포함 | Collections 없는 제한 모드. 일반 Postman과 구별 |
| T009 | Django / 1 | N 미확보; Directus 미판정 보조 | 제외 | 후속 MongoDB 조건이 최초판에 없음 |
| T012 | Mifos / 1 | QuickBooks Online / 작업자N | 포함 | 제품 전체의 수정·배포 제한과 공개 소스 요구 충돌 |
| T014 | DaVinci Resolve / 1 | Premiere desktop subscription / 작업자N | 포함 | 지속 사용은 유료. Express·한시 체험과 구별 |
| T017 | SNAP / 1 | LEDA / 역사N, 현재 무효 | 제외 | 현재 소스 재배포 허용 라이선스. 과거 binary-only 판 미특정 |
| T019 | Continue / 1 | Cursor desktop editor / 미확인 진단 후보 | 제외 | 현재 VS Code 통합 전부의 불가를 공식 자료로 확정 못함 |
| T023 | Form Tools / 2 | Power Apps Canvas form / 작업자N | 포함 | Entra 인증 필수. 익명 가능한 Power Pages와 구별 |
| T024 | cofyc/argparse / 1 | Python argparse / 작업자N | 포함 | 동명 파서의 Python 모듈과 C 라이브러리 구별 |
| T026 | SpecFlow / 2 | Cucumber-JVM cucumber-java / 작업자N | 포함 | Java 구현과 기억한 C# 단계 구현을 구별 |
| T029 | log4net / 1 | MSSqlServer-only WriteTo 구성 / 작업자N | 포함 | SQL 실패 시 배치 손실. File sink 추가 구성과 구별 |
| T030 | SDL / 1 | N 미확보; CImg 미판정 보조 | 제외 | 원문이 라이브러리 조합을 허용하며 GPU나 Wayland를 must로 두지 않음 |

확정 여부·문서 범위·원문 위치·실제 gold 포인터는 [checks-draft.json](checks-draft.json)에 있다. 원문상 명시 요구와 공식 제품 범위 사이의 대응은 작업자 판정이며 내부 별도 판정이나 외부 실제 거절로 부르지 않는다. 부가 처리로 적합해질 수 있는 경우에는 해당 후보의 고정 범위를 바꾸지 않은 채 기록해야 한다.

## 2. 가장 중요한 충돌: 과거 N이 현재 N이 아닐 수 있음

### T017 LEDA

011 NM04는 질문자의 과거 폐쇄 소스 거절이다. 최초판에도 Free and Open-Source가 있으므로 조건의 시점에는 모순이 없다. 하지만 현재 공식 배포처는 이전 라이선스가 예전 배포판에만 적용된다고 설명하고, Trier의 현재 라이선스는 소스·바이너리 재배포를 허용한다(GA10–GA12).

현재 LEDA를 유지하거나 확인 필요로 남기는 결과를 역사적 N이라는 이유만으로 잘못된 판단으로 세면 판정 기준 자체가 틀릴 수 있다. 부모 지시에 따라 역사N 행을 보존하고 `historical_N_now_invalid`, `eligible_current_strict_N_denominator=false`로 둔다. 과거 binary-only 버전 이름과 그 버전에 직접 적용되는 공식 라이선스를 찾기 전에는 과거 판이라는 문자열만 덧붙여 N으로 고정하지 않는다.

### T002 QtiPlot

011 NM02의 거절은 보존한다. 현재 계약·Pro·다운로드는 유료 바이너리를 확인시켜 주지만, 유료 오픈소스 배포도 가능하므로 이 사실만으로 closed-source를 확정할 수 없다(GA02·GA19–GA21). 현재판의 소스 공개·재배포 라이선스를 직접 확인하기 전까지 현재 strict-N 분모에서 제외한다.

### T004 Librarika

현재 공식 FAQ는 2,000기록까지 무료인 기본 플랜을 명시한다. 따라서 역사 거절의 “무료 아님”을 재사용하지 않는다. 인터넷 기반 클라우드 서비스라는 공식 설명이 네트워크 없는 한 컴퓨터 운영과 충돌하므로 N 자체는 유지할 수 있다(GA05). 같은 결론이라도 이유의 정확성이 달라지는 사례다.

## 3. 최초판에 없는 조건을 넣지 않음

- **T001:** 011 요약의 공개·비공개 방, 스레드, 반응, 검색은 이번 최초판에 없다. 최초판 요구인 클라이언트·서버 OSS, 자체 호스팅, 웹·모바일만 원문 요구로 취급한다.
- **T002:** GUI는 Ideally라는 선호이며 벡터 출력은 최초판에 없다.
- **T006:** 투표·배지·LaTeX·다국어 등을 Desirable에서 강제 조건으로 올리지 않는다. 유료 프레임워크를 허용하는 문장이 있다.
- **T007:** CLI 실행 또는 Postman 형식 내보내기라는 OR를 AND로 바꾸지 않는다.
- **T009:** MongoDB 유지는 후속 답 반박에만 기록되어 있다. 최초판의 Directus strictN 근거로 쓸 수 없다.
- **T017:** C++11 이후는 strict requirement가 아니라고 원문이 완화했다. 유지보수·문서·사용자 수·덜 전염적인 라이선스도 nice-to-have다.
- **T019:** 무료 또는 공개 소스, 관대한 사용량을 무제한·무조건 무료로 바꾸지 않는다.
- **T023:** 언어 순위와 무료는 선호이며 modest licensing을 허용한다.
- **T030:** GLFW+Cairo 조합을 예로 들고 있다. GPU·보조 라이브러리·display server 금지나 Wayland 지원을 새 must로 만들지 않는다.

## 4. grade1 유지와 모든 필수조건 준수는 다른 정답

고정014의 grade1은 실제 추천이 있고 후보별 실질 반박이 기록되지 않은 후보다. 모든 필수조건을 객관적으로 충족한다는 인증이 아니다. 이 차이를 무시하면 올바른 필수조건 검사를 “관련 후보 잘못 거절”로 세는 문제가 생긴다.

- **T007:** 고정011 T007.A001은 curl/JMeter가 OpenAPI를 가져오지 못한다고 답변자가 직접 밝혔음을 기록하지만 고정014에서 두 후보는 grade1이다. 이번 양성은 실제 gold의 SoapUI를 골랐지만 이 라벨 의미의 한계는 남는다.
- **T014:** 고정011의 답은 DaVinci Resolve + JDownloader 조합이다. 고정014는 두 구성요소를 각각 grade1로 매핑했다. Resolve가 편집 역할에서 관련 있다는 것과 URL 다운로드까지 단독 수행한다는 것은 다르다.
- **T024:** 011은 Args의 별칭 미지원 condition_failure를 기록하면서 실제 거절이 없어서 N으로 세지 않았다. 현재 Args3.2.0 문서는 long-form과 single-character shortcut을 지원한다고 명시한다(GA22). 시점·다중 별칭 정의를 확인해야 하며, 이 오래된 기록을 현재 엄격N으로 재사용하지 않는다. 양성은 다른 실제 gold인 cofyc/argparse로 골랐다.
- **T023:** 고정014 Form Tools의 grade2는 공식 채택 매핑에 따른 것이다. 011의 후속 문구는 사용 의향이며 실제 장기 사용 증거로 바꾸지 않는다.
- **T026:** 과거에 쓰던 라이브러리의 이름을 찾은 질문이다. SpecFlow의 현재 신규 도입 적합성과 역사적 식별 정답을 구별한다.

분석 제안(H): 외부 등급별 거절률과 공식 must 대조의 옳고 그름을 별도 열로 보고하고, grade1의 복합 답 구성요소 및 알려진 조건 충돌 사례를 포함·제외하는 민감도 분석을 한다. 사전 gold를 소리 없이 변경하지 않는다.

## 5. 이름 정규화와 후보 범위

검사 주입에는 이름·URL·범위를 그대로 써야 한다. 다음을 이름만 보고 합치면 설계한 판별 문제가 사라진다.

| 구별 | 이유 |
|---|---|
| cofyc/argparse 대 Python argparse | 같은 이름, 다른 언어·라이브러리 |
| Stanford SNAP 대 Snap/snapd | 그래프 C++ 라이브러리 대 Linux 패키징 |
| Serilog 전체 대 MSSqlServer-only 구성 | 원문은 Serilog가 요구를 충족한다고 이미 밝힘 |
| Postman 전체 대 v12 signed-out Lightweight Client | 컬렉션 제한은 지정 모드에만 적용 |
| Power Apps Canvas 대 Power Pages | 인증 필수 대 익명 허용 |
| Premiere desktop 대 Express·한시 체험 | 유료 제품과 다른 무료 범위를 분리 |
| Cucumber-JVM 대 SpecFlow·Reqnroll | 같은 BDD 생태계의 다른 언어 구현 |

무관 후보는 목적 수준에서 명확한 다른 제품·컴포넌트를 골랐다. BookStack은 범용 위키로 단순 도서 목록을 작성할 여지가 있어 T004의 최종 방해 후보에서 빼고, 분산 로그 저장소인 Apache BookKeeper를 사용했다. 해당 후보 선택·교체는 모두 실험 전에 이루어졌다.

## 6. 검증과 재개

현재 산출물 재생성:

```bash
python docs/workstreams/research/AF-RES-018/gold/draft-a/build_draft.py
```

직접 실행한 것은 질문 API 읽기·해시 확인, 공식 자료 열람, JSON 생성·정적 검증뿐이다. 소프트웨어 설치, 계정 생성·로그인, 제품 API 실행, A/P 검색 실행, 블라인드 판정을 하지 않았다.

다음 첫 행동은 부모가 N 슬롯 6개의 제외 사유와 후보 범위를 검토하고 gold 동결에 반영하는 것이다. 더 보강한다면 T002의 판별 라이선스, T017의 정확한 과거판, T019의 현재 공식 통합 지원 범위부터 확인한다. T006·T009·T030은 원문상 강제 조건이 아닌 것을 만들어 숫자를 채우지 않는다.

## 한계

현재 공식 문서로 구성한 N은 질문 당시의 상품 상태를 증명하지 않는다. 특히 제품·버전·요금제·단일 구성에 묶인 후보는 주입 시 범위를 생략하면 판정이 무효가 된다. 원문으로부터 C/Python·C#/JVM의 언어 조건을 대조했으나 014 EXCLUSIONS 개념 사전에는 모든 언어가 명시돼 있지 않다는 절차적 한계도 남긴다. 이 초안의 N10개는 부모 검토 전 수치이며 최종 심은 N 분모가 아니다.



## 마지막 보강: 실제 입력 수와 세 역할 완비를 분리

2026-11-21 UTC에 Question2Answer(출처 GA23), Directus(GA24), CImg(GA25)의 공식 본문을 직접 열어 같은 범주의 실체임을 확인했다. Directus와 CImg는 앞서 배제 가능성을 검토한 후보다. 세 후보 모두 `slot=near_miss`, `expected_role=strict_N`, `expected_role_status=missing`, `actual_probe_role=auxiliary_unjudged`로 기록했다. 후보의 실제 판단은 받을 수 있으나 기대 유지/제외 정답을 만들지 않았고, strict-N 거절률과 관련 후보 잘못 거절률의 어느 분모에도 넣지 않는다. CImg의 기존 외부 관련 등급이나 Directus의 기존 등급0을 이 보조 검사의 새 등급으로 복제하지 않았다.

이 보강 후 실제 후보는 48/48개이고 엄격 N은 계속 10/16개이다. 따라서 모든 질문에 양성·엄격 N·무관의 세 역할이 있는 조건은 **미충족**이다. 생성 스크립트와 verification.json은 입력 수 충족과 역할 결측을 별도 검사하며 A/P 실행은 0건이다.
