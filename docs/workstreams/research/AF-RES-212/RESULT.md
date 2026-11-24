# AF-RES-212 추천 링크의 독립 이름·목적 비교

| 예시·앵커 | 표시 문구·주변 문장 | 접근 가능한 이름·출전 | 실제 목적지 URL | 미확인 |
|---|---|---|---|---|
| G1a (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| G1b (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| G2a (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| G2b (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| G3a (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| G3b (예정) | 미확인 | 미확인; https://design-system.service.gov.uk/components/summary-list/ D02 L67–98 및 frame.csv | 미확인 | GOV 정규 예시 적격 0/3; 원 HTML+서로 다른 실제 href pair 불충족 |
| U1a Default | Gears of Government President’s Award winners; 인접 본문은 수상자 공지; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L303–308, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/presidents-winners-press-release/ L01 L6–22; 수상 발표 기사 | 실제 accessibility tree/목록 발화 |
| U1b Default | Women-owned small business dashboard; 인접 SBA 협업 소개; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L333–338, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/sba-wosb-dashboard/ L02 L8–20; dashboard 소개 기사 | dashboard 본체 아님; 샘플 Sep 30 vs 기사 Oct 27; 기기 출력 |
| U2a Media thumbnail | Gears of Government President’s Award winners; 인접 본문은 수상자 공지; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L401–406, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/presidents-winners-press-release/ L01 L6–22; 수상 발표 기사 | 실제 accessibility tree/목록 발화 |
| U2b Media thumbnail | Women-owned small business dashboard; 인접 SBA 협업 소개; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L436–441, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/sba-wosb-dashboard/ L02 L8–20; dashboard 소개 기사 | dashboard 본체 아님; 샘플 Sep 30 vs 기사 Oct 27; 기기 출력 |
| U3a Calendar display | Gears of Government President’s Award winners; 인접 본문은 수상자 공지; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L510–515, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/presidents-winners-press-release/ L01 L6–22; 수상 발표 기사 | 실제 accessibility tree/목록 발화 |
| U3b Calendar display | Women-owned small business dashboard; 인접 SBA 협업 소개; h4 heading | 같은 문구(규칙 기반 기대); https://designsystem.digital.gov/components/collection/ D05 L533–538, https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13 | https://trumpadministration.archives.performance.gov/sba-wosb-dashboard/ L02 L8–20; dashboard 소개 기사 | dashboard 본체 아님; 샘플 Sep 30 vs 기사 Oct 27; 기기 출력 |

| 탐색 방식 | 이름만으로 구별되는 목적 | 소실·과잉 정보 | 관측 근거·판 | 해석 한계 |
|---|---|---|---|---|
| 문단·행·heading 연속 읽기 | 주위 문장/행 키가 결합되면 비교·호출·그림 구별 가능(기대). U 두 대상 구별 | 인접 시각 문장만이면 연결 보장 없음; 모든 근거를 이름으로 반복하면 과잉 | https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html W01 L22–37; https://www.w3.org/WAI/WCAG22/Techniques/failures/F63 W05 L32–51; https://webaim.org/projects/screenreadersurvey11/ R02 L311–321 | 규칙 및 자기보고; 문단 청취 실측 없음 |
| NVDA 요소 목록 (NVDA+F7) | A/C의 기대 이름에 대상과 목적이 있으면 구별 가능; U 두 제목은 서로 다름; 동일 colorspace 이름만으로 서로 다른 역할 미구별 | heading/인접 설명이 각 항목에 제공된다고 가정 못함; title 보고에서 설명 소실; 길이·중복 비용 | https://download.nvaccess.org/documentation/userGuide.html T01 2026.3.1 L1196–1200; https://evinced.com/blog/screen-readers-101-for-front-end-developers-windows/ T05 L154–162; https://github.com/w3c/wcag/issues/1063 T06 L164–196,228–235 | 발행자 명령 안내와 기존 시연/제보; 정확한 description 전달·최신 출력 미확인 |
| VoiceOver 웹 로터 Links (같은 목록 탐색의 다른 구현) | A/C의 기대 이름으로 같은 판정 후보; 실제 rotor 항목 문자열 미확인 | 문단 정보 미전달 가능성; pseudo prefix와 문장부호 반복 | https://support.apple.com/en-euro/guide/voiceover/vo15219/mac T02 L158–168; https://github.com/uswds/uswds/pull/5166 D13 L353–357 | 구성 안내와 VO 4 브라우저 reviewer 관측은 로터 실측이 아님; 상세 guide 429 F02/F03 |
| 보이는 이름 음성 명령 (대조 관점) | A의 대상+목적 visible, C의 visible prefix 유지; 같은 visible label은 선택 모호할 수 있음 | 보이는 말과 aria-label 교체 불일치; 긴 이름 전체 강제의 위험 | https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html W07 L22–43 | 음성 인식·선택 성공률 미측정 |

| 한국어 카드의 목적 | 클릭할 문구 | 보조 설명 | 적용 조건 | 반례·다음 검사 |
|---|---|---|---|---|
| 비교 문헌 | colorspace 논문 — 비교 문헌 | seaborn 관련 비교 배경; https://joss.theoj.org/papers/10.21105/joss.07120.pdf (201 routes C 배경/P01) | A visible로 문단·목록·음성 명령 구별 기대(W01/W02/W07); B는 주변 문맥, C는 숨김 suffix | 사용 증명 아님; 같은 PDF의 Fig.5 링크와 중복이면 통합 |
| 호출 예 | colorspace — seaborn displot 호출 예 | https://github.com/retostauffer/python-colorspace/blob/v1.0.0/_quarto/articles/usewith_seaborn.qmd (201 C23 L51–74); palette 전달 | A/C 대상+호출 역할; B heading 및 문단에 목적 표시; 규칙 기반 기대만 | 실행 주장 금지; 숨김 공백·중복 검사 D09/D10 |
| 실제 출판 그림 | colorspace 논문 — 출판 그림 Fig.5 | https://joss.theoj.org/papers/10.21105/joss.07120.pdf (201 P01 Fig.5); 오른쪽 그림; 생성 경로는 별도 C22 | PDF 동일 목적지인 한 한 링크와 두 위치 안내도 유지; 별도 이미지/검증된 fragment 있을 때 분리 | 생성 코드≠산출물, E4 미확인; fragment·정확 객체·실행 근거 확인 |

## 판정과 분모
**PARTIAL.** 최소 유형별 고유 본문 35/22 (W3C 10/5, tool 6/5, design 13/7, publication 4/3, user 2/2). 원장 47행(35 하한 산입, 5 도착면/보강, 7 실패·본문 부족). 고유 저작/공급 계보/사건을 구분: D05 한 문서 3개 변형, 서로 다른 두 href만 반복; D10/D11 같은 결함 계보. 6개 예정 예시 중 USWDS 3개, GOV 0개, 정규 앵커 6/12(US 6/6, GOV 0/6); strict 도착 URL 고유 2개. 추가 4자리(G-S1/2 #, G-S3/4 서비스 목적지 확인·raw HTML 미확인) 별도. frame.csv 23행(12 예정 +11 screening/jump). 원본 HTML 추출은 게시된 예시 코드, 공백 정규화; runtime DOM/AX tree 아님. 모집 전수/사용자 성공률/음성 출력 측정 없음.
 
## Q1. 실제 객체와 이름
USWDS link/card에서 모의 href/중복 href; collection 세 변형은 실제 같은 2 URL로 간다(D03–D05). Award는 수상 발표, dashboard는 2020-10-27 소개 기사(예시 날짜 9/30과 불일치). 객체 종류를 이름에 붙이지 않으면 명확한 이름도 틀린 목적을 예고한다. GOV links의 단일 #, summary-list의 Change #, 독립 card 접근 실패를 표집 결손으로 유지. D02에서 L03(교사훈련 서비스) 1회 이동, L04/L05 실제 도착; raw anchor/ARIA 확인 못해 보강. 다음 GOV 실제 서비스 DOM/공식 소스 확인, USWDS 실제 서비스 링크 유무 전수 확인. 

## Q2. 세 문자열
표시 텍스트는 렌더링, name은 별도 계산, description은 부가 텍스트. https://www.w3.org/TR/2026/WD-accname-1.2-20261104/ W03 §4.2/4.3.2 및 https://www.w3.org/TR/2026/WD-html-aam-1.0-20261026/ W04 §4.1.13: 이름은 유효 aria-labelledby 참조 순서, aria-label(해당 조건), 링크 subtree, title fallback. 숨김 노드는 기본 제외되나 직접 참조된 숨김 subtree 등 예외. CSS clip/visually-hidden이 실제로 이름 계산에서 제외되지 않아야 suffix가 들어감(W08). description은 aria-describedby→aria-description→이름에 안 쓴 host-language feature→title; name의 대체 아님. U anchor 직접 ARIA 없음, 주변 ul의 aria-label은 참조 없음, media img/time은 별개. G-S1/2 Change+suffix 기대 이름, #로 도착 확인 불가. D09에서 공백이 붙어 들렸다는 반례. 실제 플랫폼 mapping/AX tree 미측정.

## Q3. 두 방식의 노출
T01 요소 목록은 링크 선택/필터; T02 로터는 항목 유형 설정. 이름 중심 기대와 실제 정확 음성 출력을 분리. T05 반복 이름 시연; T06 title이 링크 대화상자에서 사라진 보고는 aria-describedby의 보편 소실 증명 아님. T03 강제 UIA와 T04 브라우저별 이름 오류는 구현/환경 중요성. R02 첫 탐색 선호 heading 67.8%, links 6.7%, continuous read 9.7%; 이것을 링크 목록 사용률/과업 성공률로 바꾸지 않음. R01 같은 이름 다른 목적지에 대한 쉬움·어려움 양쪽 자기보고 존재. 다음 NVDA F7/VO rotor 같은 카드 입력과 연속 읽기 각각 기록, description과 name 항목을 비교(새 시험 미실시).

## Q4. Context와 link-only
W01 2.4.4 A는 프로그램적으로 결정 가능한 문맥 허용, W02 2.4.9 AAA는 이름만으로 목적을 확인할 수 있는 메커니즘. W05 단순 시각적 이웃 문단 실패 조건; W06 Read more 두 href를 aria-label로 구별(모의), W10 자기 id+heading 조합. 같은 accessible name/다른 실제 URL의 정규 구현 대조는 미충족; T05/R01 기존 관측만. 같은 URL 같은 이름은 D05 3변형, 같은 URL 다른 문구/동작 예는 D03 GIF(목적지 미열람). W09 동일 리소스 이웃 링크 합치기, D12 같은 page Change header 통합. 따라서 모든 이름 유일화 금지; link identity와 목적/행동/fragment 별도. 실제 다른 href인데 동일 name인 사례의 원 DOM과 도착면을 다음 조사에서 직접 확보.

## Q5. 이름 길이·편집 비용
D09 2019 공백 제보·Speech Viewer 재현 논의, D10/D11 title 중복과 괄호 문제, D13 2023 USWDS PR에서 pseudo label·구두점·RTL·CMS 편집 제약 및 JAWS/Narrator/VO reviewer 관측. D13 reviewer의 시험 설명을 새 사용자 연구나 링크 목록 측정이라 부르지 않음. D12 서비스 사용 언급의 참가자 수/원자료 부족. R01/02 직접 자기보고 자료. 실제 '너무 긴 이름'을 길이 변수로 통제한 참가자 자료 미확인, 임의 글자수 기준 금지. 음성 명령 W07 visible label 포함/가능하면 접두; 별도 사용성 시험으로 반증.

## Q6. 외부 분야
PLOS P01 https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224697 L105–149,337–354: abstract/full text는 article; S1 File/TIF 그림, S2 File/MP4 동영상의 목적은 주변 설명에 존재. 보충 DOI 접근 실패 F04(500), 실제 파일 확인 못함. SFPL P02 https://sfpl.bibliocommons.com/v2/record/S93C2333799 L92–135 2009 eBook에서 Book 링크 → P03 https://sfpl.bibliocommons.com/v2/record/S93C1616152 L92–128 1991 종이책 카탈로그(같은 제목, 객체/판 다름). 실제 책 내용은 아님. NYPL P04 https://nypl.overdrive.com/media/6147814 L126–165 제목·샘플·포맷 분리; sample 500(F06). 따라서 논문 참고 인용/코드 예/출판 결과를 title 하나로 통일하지 말고 목적과 실제 객체를 함께 표현. publisher 실제 supplement landing/file 재확인이 결손.

## Q7. 대안별 적용 및 반증
A visible 대상+목적: 목록·시각·연속 읽기에 공통, 음성 명령 보이는 이름 대응, 긴 반복과 시각 밀도 비용. B 주변 문장/heading만: 짧고 편집 용이, 연속 읽기에는 프로그램적 관계 확인 필요, 목록에서 역할 사라질 수 있음. C visible prefix + 조건부 숨김 suffix: 반복 Change의 대상 분리 가능, 실제 CSS/ARIA/공백·중복·voice command 확인 필요; 시각 사람은 주변 문맥에 의존. D description-only: 상세 근거 별도 보존, 같은 name 목록에 설명이 보인다는 가정 금지. 카드별 A/B/C 문구와 D 대응은 cards.md. 동일 PDF href의 비교/그림은 한 링크+두 위치 안내 대안 유지. 목적지 객체 검증, name 계산, 주변 설명/근거, href identity 및 열기 행동을 독립 필드 후보로 보존. 사용자가 heading 기반으로 읽거나 목록이 설명까지 안정적으로 노출하면 B/D 적용 확대; 같은 URL/동작이 중복되면 A도 통합; 음성 명령이 visible prefix에도 실패하면 C 재검토. 이 연구만으로 제품 UI 최종 채택/순위 확정하지 않음.

## 추가 분석
네 관점: 목록 사용자는 이름 alone의 정보 손실, 연속 청취자는 근거 반복 비용, 음성 명령자는 label mismatch와 같은 표시명 선택 비용, 편집자는 객체 유형/버전/정확 fragment 및 다국어·CMS/중복 검사 비용. COUNTEREXAMPLES.md CE1–CE10, examples.csv/names.csv의 expected vs observed 열을 연결. 자료 노출: 201 및 목적 세 가지와 가설을 사전에 읽음; 독립/블라인드 코딩 아님. 두 설계 시스템 비교가 단일 USWDS collection 변형에 치우침. 원장 고유 저작 수가 사건수 또는 기기 시험수가 아니다. 사용자 성공률 산출 없음. 다음 직접 관측은 HANDOFF.

| 불일치·약점 | 영향을 받는 결론 | 다음에 열 원자료·조사 | 판정을 바꿀 관측 |
|---|---|---|---|
| GOV 0/6; strict 6/12, US collection 같은 2 href; dashboard 명칭·날짜 불일치 | 양 시스템 비교 및 name-only 반례 일반화 불가; 정확 객체가 핵심 | D02 공식 서비스 example DOM/HTML, GOV 실제 링크 있는 summary card; USWDS 실제 서비스 원 코드; L02 dashboard 도착면 | GOV 적격 3예시 및 실제 동일 name/다른 href가 확인되면 표/역할 대응 수정; dashboard가 직접 객체로 확인되면 기사 판정 수정 |
| AccName/HTML-AAM WD의 기대 이름과 최신 NVDA/VO rotor 출력 간극; 설명만 있는 이름/숨김·길이 실측 없음 | A/C/D의 독서 방식별 판정은 조건부 | T01/T02 exact version + D09/D13 fixture, T06 description-only 비교, 음성 명령/당사자 기록 | 두 목록에서 description이 안정적으로 같이 나옴, suffix가 사라짐/중복됨, visible prefix 음성 선택 실패 시 권고 변경 |
| PLOS supplement/NYPL sample 접근 실패, 201 E3 정적 경로와 실제 출력 구분 | 외부 분야 artifact 대응·Fig.5의 별도 목적지 확정 못함 | P01 공개 supplement 공식 landing/file, P04 샘플, 201 result SHA의 이미 기록된 원본 artifact 참조(재판정 제외) | 직접 공개 산출물 객체/검증 fragment 확인 시 그림 링크 분리; 동일 PDF만 확인되면 통합 유지 |
