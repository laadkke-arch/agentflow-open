# 변경 비교·반례 및 정정 이력

증거 수준: ROR 운영자가 관리하는 **release-candidate 변경 JSON** 직접 판독(고정 SHA 및 blob, ror-release-records.json/rename-records.json에 파싱 보존). Zenodo 릴리스 목록 직접 확인과 티켓의 발행 통지는 별도. 발행 ZIP 전체 원행과 오늘 API는 미수신. RC에 파일이 없다는 것은 그 판의 데이터셋에 원행이 없음을 의미하지 않는다. 상태 필드 도입 자체도 합병과 다르다.

## 1. Sorbonne — 시대를 섞지 않는 변화표

| 사건 | 고정판/위치 | before → after 관측 | 지지/반증 및 미확인 |
|---|---|---|---|
| 2010 PRES → 2015 COMUE → 2018-01-01 대학 통합 | [대학 역사](https://www.sorbonne-universite.fr/en/university/about-us/history) L64–65; [학부 연보](https://lettres.sorbonne-universite.fr/faculte-des-lettres/histoire-de-la-faculte) L60 | 2 대학에서 신설 SU, Paris IV는 Lettres 학부 연속성 | 법령 본문 403; 협의체 법인과 대학 법인 및 연구실 범위를 동일시하지 않음 |
| 2018-11-14 ROR admin.created (SU) | G03/G04 | ROR established=2010, 공식 2018과 다름 | 최초 공개판 이름/관계 미확인; 2010 PRES 가설은 역사 문서와 EQAR의 별도 레코드가 지지하나 ROR 큐레이터 의도 미확인 |
| 2022-12-01 inactive/withdrawn 및 successor/predecessor 도입 | [ROR 변경 공지](https://ror.readme.io/changelog/2022-12-01-organization-status-changes) L29–43 | 상태·관계 어휘 추가 | 2018 합병 당시 현재 어휘를 가정하면 오류 |
| 2026-03-10 #31547/#31548 | [Paris IV](https://github.com/ror-community/ror-updates/issues/31547), [UPMC](https://github.com/ror-community/ror-updates/issues/31548) body/bot comments | 기존 SU 이름 alias 가능성 bot이 지적; inactive 별도 ID + successor 요청 | bot 판독은 과거 실제 원행을 대체하지 않음. UPMC 원문 diff Paris VI alias 있었으나 최종 요청 alias 공란 |
| 2026-03-12 v2.4 | [Zenodo](https://zenodo.org/records/18985120), rc-v2.4 SHA 522eca15e971d3ba2c5b27fe68ea286bc93d38c0 | 공개판 존재 확인; SU 변경 경로 404 | 발행 전 원행/alias/관계 미확인; 404 != 원행 부재 |
| 2026-03-30/31 v2.5 | [Paris IV raw](https://github.com/ror-community/ror-updates/blob/ef8e4bd6dec66084bf5d476f75471fc222315939/rc-v2.5/new/025xed883.json), [UPMC raw](https://github.com/ror-community/ror-updates/blob/ef8e4bd6dec66084bf5d476f75471fc222315939/rc-v2.5/new/01yvrd251.json), [SU raw](https://github.com/ror-community/ror-updates/blob/ef8e4bd6dec66084bf5d476f75471fc222315939/rc-v2.5/updates/02en5vm52.json); [Zenodo](https://zenodo.org/records/19356124) | Paris IV inactive 025xed883 & UPMC inactive 01yvrd251, created 03-30 last_modified 03-31; 각 successor 02en5vm52; SU active 두 predecessor | 4/4 방향 명시, 티켓의 ID·상태·후계 요청과 RC 일치. UPMC alias Paris VI 없음. 공식 ZIP 미수신; 2.4 actual before 미확인 |
| 2026-09-22 v2.13 | [SU raw](https://github.com/ror-community/ror-updates/blob/90401a472e60646984d73611e0816a5452c98c92/rc-v2.13/updates/02en5vm52.json) | 2.5→2.13 SU 동일 id/status, predecessor 둘 유지, relationships 210→211 | SU 역 2방향 유지 확인; 전신 두 v2.13 원행 없음 |
| 2026-11-19 v2.16 | [Zenodo](https://zenodo.org/records/24378467), rc-v2.16 SHA 42804deedcb3a94ee139afd0ed19cfae4c15e9dc | 최신 발행판 목록 | 3자리 모두 v2.16 원행 미수신. 현행이라고 2.5/2.13을 표시 금지 |

### 독립 공급기관의 실제 불일치
[DEQARINST1063](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=1063) L531–588 UPMC: 1971–2018, successor SU, ROR 011htkb76. G02 ROR 자체 RC는 01yvrd251. 둘 다 후보를 기록하되 011htkb76 원행이 열리지 않아 동일/오류/withdrawn/다른 범위 중 어느 것도 단정하지 않는다. [DEQARINST1061](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=1061&limit=20&offset_inst=0&offset_prog=20) L532–588 Paris IV에는 ROR 행 미표기(해당 EQAR 표시에서의 정상 공석). 이는 G01 ROR row 존재와 양립한다. 
[DEQARINST6648](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=6648) L532–596: SU founding 2018, FR0347, ROR 02en5vm52. [DEQARINST4561](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=4561&limit=20&ordering=) L532–578: Association Sorbonne Université founding 2015, FR0808, 동일 ROR 02en5vm52, 2015 두 전신 subunits. 따라서 하나의 ROR link가 서로 다른 역사 기관 범위를 구분하는 충분조건이 아니다. EQAR의 매핑 오류/과거 매핑 갱신 지연/등록기관의 집약된 scope 모두 경쟁 설명. 정정 전 orgs.csv b4b6e6dcd122ed269aaf614a934d4d6d8ffbd1cb의 S1에 EQAR 후보를 잘못 넣었음. 정정판 1ab0330541de1343c6ff5d020b1e05925ae6a37f S2로 이동, S0 범위 충돌, S1 EQAR 공석 기록. 파일 이력 보존. 초기 SCOPE prediction A는 RC에서만 성립하고 오늘 및 두 가족 일반화 철회.

## 2. Aalto — 법적/운영상 계승과 ROR 링크를 분리
[공식 역사](https://www.aalto.fi/en/aalto-university/history) L65–87: 2008 이름/charter, 2010-01-01 3개 대학 운영 통합. [2010 연차 보고서](https://www.aalto.fi/sites/default/files/2018-09/aalto_university_annual_report_english.pdf) p4 업무·사람·학생·자산·권리/채무 이전. [핀란드어 역사](https://www.aalto.fi/fi/aalto-yliopisto/historia) L94–102: TKK는 2010년 Aalto 기술학교로 1년, 2011-01-01 4개 학교로 분리. [경영학교 연보](https://www.aalto.fi/fi/kauppakorkeakoulu/jo-yli-110-vuotta-suunnannayttajana) L145–149: HSE는 Aalto 경영학교, 영어 이름 2012-08-01 변경. 대학 단위 계승은 오늘 특정 연구실 또는 학교의 연락처 선택 근거로 충분하지 않다.
OpenDOAR M05/M06에서 Aalto 020hwjq30 후보 직접 확인. Aalto/HUT/HSE ROR 원행은 미수신. HUT/HSE query 및 GitHub 티켓 검색 실패/미발견은 정상 공석 아님. #21905 ROR 개인 소속 변경 요청은 플랫폼 문의로 종결, 레코드 변경 아님. 두 전신 각각 두 방향 4개 모두 unknown. HUT/HSE ID 없음이라고 쓰지 않는다. 제3 전신 Taideteollinen korkeakoulu (University of Art and Design Helsinki) 모집틀 밖.

## 3. 두 통제, 추가 반례, IANA
**같은 ID rename — Sumy 020kwj692**:
[티켓 #41993](https://github.com/ror-community/ror-updates/issues/41993) L140–159, L285–361: 10-20 완료 통지, 10-21 requester API old name 보고 및 운영자 처리 오류 인정, 재개, v2.16 milestone.
[rc-v2.15](https://github.com/ror-community/ror-updates/blob/90ccc526d897b49d084b1f100f9678a0735d1c3c/rc-v2.15/updates/020kwj692.json) → [rc-v2.16](https://github.com/ror-community/ror-updates/blob/42804deedcb3a94ee139afd0ed19cfae4c15e9dc/rc-v2.16/updates/020kwj692.json). id 고정; active 둘; relationships [] 둘(실제 정상 공석 2판); names old display→new display Sumy State Pedagogical University, old display→alias. last_modified 2026-10-20→11-19. requester가 직접 API 봤다는 증언, 우리 원 API 미수신. 동일 기관을 이름만 갱신하는 RC 관측. 법인 동일성은 requester 주장; 별도 법령 미검증. 규칙 R01 L160. 과거 명칭 그대로 + 동일 ID, 새 표기 검색은 별칭. 완료 티켓만으로 변경 완료라 표시하지 않는 실제 반례.
추가 [#43185](https://github.com/ror-community/ror-updates/issues/43185) 및 [Capital University RC](https://github.com/ror-community/ror-updates/blob/42804deedcb3a94ee139afd0ed19cfae4c15e9dc/rc-v2.16/updates/00h55v928.json) 같은 ID 00h55v928, active, Helwan University alias, Capital University display; 요청 표기의 Egypt 접미어는 실제 display에 없음. 전판/법령 미수신이라 보조만. [#40691](https://github.com/ror-community/ror-updates/issues/40691) SPHI acronym 충돌로 요청 그대로 인코딩 못 한다는 결정; rename의 완료 통제가 아님.

**parent/child — Neuro-SU와 SU**:
[rc-v2.13 Neuro-SU](https://github.com/ror-community/ror-updates/blob/90401a472e60646984d73611e0816a5452c98c92/rc-v2.13/updates/02pgsjq66.json) active facility parent SU 02en5vm52, CNRS 02feahw73, Inserm 02vjkv261; G04 SU child 02pgsjq66, 둘 active, 2/2 명시. [#37559](https://github.com/ror-community/ror-updates/issues/37559) v2.13 반영 통지. 시간 successor 없음. parent/child active reciprocity R01 L150–154, inactive tombstone 비대칭 허용. 자식은 부모와 동일하지 않으며 세 parent의 연구실을 한 대학 크레디트로 대체하면 오류.
**같은 도시·이름 부분**: [PRISM Sorbonne rc-v2.14](https://github.com/ror-community/ror-updates/blob/bed80a9b341577d2f9443336ee7a12130ab7ca5e/rc-v2.14/new/046crpj40.json) active facility, parent Paris 1 Panthéon-Sorbonne 002t25c44, SU 아님. #40466 결정 근거 affiliation usage/funding/employment. 문자열 Sorbonne/Paris는 후보 생성에만.

**IANA** [registry File-Date 2026-11-18](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry):
- Type region; AN Netherlands Antilles; Added 2005-10-16; Deprecated 2011-01-07; Comments see BQ, CW, SX. Preferred-Value 없음(원행 공석, L46170–46176). 3후보 모두 일괄 치환 금지.
- Type region; YD Democratic Yemen; Added 2005-10-16; Deprecated 1990-08-14; Preferred-Value YE (L47472–47482). 단일 preferred 있어도 역사의 동일성을 뜻하지 않음.
- [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646) §3.1.7 L1647–1658, region mapping 의미가 다를 수 있고 기존 content retagging 강제 아님. 검색/정규화와 기록 시점 인용 분리. ROR과 달리 언어 tag 표준이라는 한계. 두 행=한 registry 저작. 
**보존 리포지터리**: P01 원문 UPMC 및 협의체, M01 HAL 현행 SU collection; P03 원문 2009 HUT, M03 Pure 2010 표시. 현재 보관 및 날짜 자체가 다른 경우. 원문과 현대 전거 관계를 별도 저장.

## 4. 관계가 없어지거나 수정될 때
원문 문자열 + DOI/원문 링크는 그대로. ROR 원행마다 observed_at/판/URL 및 relationship edge + from/to direction/유효성 구간 기록. 옛 링크와 오늘 링크의 role를 분리(historic_reference vs current_contact; optional search_alias). 관계 삭제/withdrawn/다중후계/범위 충돌 발생 시 “ROR 판 X에서 B가 A의 successor로 게시”는 역사 관측으로만 남기고 “현재 후계 B” 문장과 자동 추천/rollup은 철회 또는 후보 보류. 원문 출판 ID가 있으면 원문 ID 보존; 없으면 later_link를 original_id에 쓰지 않음. 법적 기관 연혁 링크는 별도 표기(법적 판단과 등록기관 판단 분리). 연구실/저자/논문 전체 이동 금지. 등록기관의 withdrawn 오류 정정과 실제 inactive 종료를 분리. 양방향이 필요 없는 temporal edge의 역방향을 생성하지 않음; UI에서는 추론 표시만 허용하고 원관측과 섞지 않는다.

정정 로그: SCOPE→원자료 후 A는 Sorbonne RC에서만 지지, Aalto는 B의 미수신(누락 아님); P03 portal year 대신 publisher date 채택, 엄격한 earliest selection 실패 인정; #41993 티켓 완료와 RC mismatch 실제 확인; EQAR 후보 위치/협의체 scope 수정(위 고정판). 독립 검토 미실시.
