# 반례 및 결손 (AF-RES-212)
## 독립적으로 보존할 반례
|ID|입력/원출처|무엇이 초기 판단을 반증하는가|판정/조건|
|---|---|---|---|
|CE1|D05 https://designsystem.digital.gov/components/collection/ L297–573 → L02 https://trumpadministration.archives.performance.gov/sba-wosb-dashboard/ L8–20|명확하고 유일한 이름도 목적지 객체를 틀리게 예고할 수 있다. 대시보드라는 링크가 소개 기사로 감.|대상 구별 성공 기대와 객체 종류 불일치 별도. '여성소유 소기업 대시보드 소개 기사'가 더 정확. 진짜 dashboard 미검증.|
|CE2|D02 https://design-system.service.gov.uk/components/summary-list/ L67–98; W06 https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA8 L34–46|보이는 같은 Change/Read more라도 다른 접근 이름이 가능. D02 href #; W06 두 상대 href 모의 파일.|이름만 다른 구조가 성립하나 실제 다른 목적지 증명 아님. 정규 12자리에서 이름만 같은 실제 다른 목적지는 미확인.|
|CE3|T05 https://evinced.com/blog/screen-readers-101-for-front-end-developers-windows/ L154–162; R01 https://webaim.org/projects/screenreadersurvey/ L339–351|반복 링크명에 관한 기존 시연/이용자 자기보고는 문맥 없는 이름의 어려움과 쉬움을 동시에 보인다.|원 시연 목적지 전수/HTML 및 기기 판 미확인. 효과 크기/성공률 산출 금지. 일부는 문맥/기억으로 해결 가능.|
|CE4|D05 동일 award URL/동일 문구 3개 변형; D12 https://github.com/alphagov/govuk-design-system/issues/5864 L196–203; W02/W09|이름을 전부 고유하게 바꾸면 동일 목적지가 다른 객체처럼 오해된다; 같은 page로 가는 Change를 하나로 합칠 수 있다.|실제 같은 이름·href 대조 3변형(한 화면 3중복은 아님). 동일 PDF 링크 두 역할이면 하나로 합치고 위치를 안내; fragment/target/권한/동작이 다르면 별도.|
|CE5|D03 https://designsystem.digital.gov/components/link/ L212–257|같은 외부 GIF URL이 여러 문구 및 target 동작으로 나타남.|같은 목적지 다른 이름/현재·새 탭의 예시 코드; GIF 원격 객체 미열람. 사용자 동작이 다르면 구별 정보 유지.|
|CE6|W03 https://www.w3.org/TR/2026/WD-accname-1.2-20261104/ §4.2; T06 https://github.com/w3c/wcag/issues/1063 L164–196,228–235,269–283|description만 유일하면 accessible name은 여전히 같은데 일부 목록에서는 title 설명 전달 안 됨.|aria-describedby 유일 설명 variant는 설계 반례; title 보고를 모든 description/AT로 확대 금지. 목록에서 설명이 안정적으로 제공되면 B/D안의 적용 범위 확대.|
|CE7|D09 https://github.com/alphagov/govuk-frontend/issues/1643 L160–184,227,329–335; D10 https://github.com/alphagov/govuk-design-system/issues/5093 L170–199; D11 https://github.com/alphagov/govuk-frontend/issues/7302 L138–169|숨김 접미사 조립에서 공백 소실/중복 제목이 발생. 길이를 늘리는 것만으로 더 좋은 이름이 되지 않음.|D09 사용자/제작자 관측, D10/11 제보/코드; 독립 재시험 아님. 이름 계산 및 실제 발화 별도.|
|CE8|D13 https://github.com/uswds/uswds/pull/5166 L170–221,274–279,353–357,375–381,411–441; W07|prefix pseudo 라벨과 문장부호가 JAWS/Narrator/VO에서 다른 체험을 만들고 RTL/CMS 비용이 생김. 이름의 보이는 label 부분이 사라지면 음성 명령에 불리.|리뷰어 관측(버전·음성 원문·목록 모드 불명)과 개발 지침 분리. hidden suffix/visible prefix 보존을 비교. 사용자 발화로 꾸미지 않음.|
|CE9|P01 https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224697 L337–354; P02→P03|S1 File 등 목적 설명 분리; 한 작품 이름이 전자책/종이책 레코드로 이어져도 객체 유형이 다름. Book은 책 내용 그 자체가 아님.|출판 보충 파일 DOI 500(F04); SFPL 레코드 실제 클릭 확인. 제목/역할/객체 종류/판 구분.|
|CE10|R02 https://webaim.org/projects/screenreadersurvey11/ L311–321; T03/T04|모든 사용자가 링크 목록으로 시작한다는 전제 틀림. UIA/브라우저 및 접근 트리 오류 보고.|긴 페이지 첫 탐색에서 링크 선택 응답 6.7%, 목록 모드 사용률 아님. 연속·heading·검색 보존; 문안 문제를 구현 결함과 혼동하지 않음.|
## 표집 결손 및 갱신
사전 분모 12는 유지. GOV 0/6, USWDS 6/6, 합 6/12; 3/6 예시. D05 동일 페이지 내 세 변형이라 unique URL 2. GOV 링크 예시 #/single; summary-list #; 별도 card 문서 미확인. 실제 서비스 안내로 이동하여 Scotland 및 Wales 목적지 방문(L03–L05), 단 원 HTML/ARIA 미확인이라 2개 정규 슬롯으로 올리지 않음. D05 변형 날짜 표시 Sep 30 2020, L02 기사 Oct 27 2020; 실제 timestamp 차이를 기록하고 표본 값 변경하지 않음. P01/NYPL 보충 파일 실제 열람 실패(F04/F06); Apple rotor 도움말 429(F02/F03). 기존 원장 값 유지: 설명으로 링크명 대체하지 않음.
## 네 관점의 비용
목록 훑기: 핵심 대상+역할이 필요하나 동일 URI 중복/긴 제목은 피로; 문단 연속 읽기: 문장/행 키가 문맥이 되므로 모든 근거를 반복할 이유 없음; 음성 명령: 보이는 말과 name의 일치 및 중복 선택 모호성; 편집자: 목적지 유형/버전/fragment 확인과 제목 중복 유지·번역·CMS 조립 비용. A/B/C/D 각각 실패하는 입력은 cards.md. 독립 검토나 새로운 기기 실험 없음.
