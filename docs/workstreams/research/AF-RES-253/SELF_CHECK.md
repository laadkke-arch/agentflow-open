# AF-RES-253 자체 점검

판정 **PARTIAL**. 주 axe 실행·반전·별도 폴더 재생과 원자료 하한 충족. 날짜판과 RFC의 원 게시 HTML・DOM・브라우저 도착은 같은 Cloud egress 제한으로 미확인이다. 독립 검토는 미실시다.

| 질문 | 직접 근거·영수증 | 결론을 뒤집을 사례를 찾은 곳과 결과 | 남은 미확인 |
| --- | --- | --- | --- |
| Q1 | W20·W21·W22, F01–F03, [HTTP 영수증](receipts/pages/) | 원페이지 본문 열람과 source receipt를 함께 읽었다. 실제 CONNECT 403은 프록시 hop. 작성판 태그 G03도 보았고 ReSpec source 포함을 확인. | 3 origin HTTP·redirect·type·바이트·지문 |
| Q2 | W04–W09, D01, G01–G03, [anchors.csv](anchors.csv)와 [앵커 통제](receipts/pages/controls/) | 작성 Parsing 2.2에서 제거 H4에도 section ID와 Chromium 도착. 합성으로 legacy·중복·ID 우선순위·다른 name·없는 ID 모두 실제 검사. W09 해설에 제거 표시와 옛 전문의 일부가 공존. | 날짜판 exact DOM 6, 출판 문서 위치, 배너의 실제 DOM |
| Q3 | A09, N01–N02, D03, [빌드](receipts/builds/builds.json), [환경](receipts/runs/environment.json), [235 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/HANDOFF.md) | 태그 이름만 비교하면 다른 바이너리를 쓸 수 있다. Git tag→registry gitHead→SRI→tar member→설치 JS→axe.version과 testEngine.version을 비교. DOM과 옵션은 case 24행 대조. | 독립 build, 정확한 과거 사용자 설치판 |
| Q4 | A01–A10, O01–O04, P01–P02, D03·D05, X01·X02, [rules.csv](rules.csv) | 4.8 default/wcag2a의 두 ID 공석과 explicit violations를 각각 확인. ARIA I와 default 부수 V를 확인. alt 없는 노드 V와 alt 있는 노드 P가 같은 rule로 공존. | 추가 브라우저/제품 wrapper 및 전반 적합성 |
| Q5 | D02·D04, W10·W11, [CDP·axe 원값](receipts/runs/aria-controls/) | 같은 중복의 span 순서 반전은 이름을 바꿔도 V/I를 유지. 두 유일화 통제가 이름 정확도를 달리하면서 같은 P. backendNodeId를 해당 문서의 span 순서와 비교. | AT 발화, 다른 엔진, 실제 사용 목적 |
| Q6 | R01–R06, F04–F05, [RFC 대조](replay.md#rfc-공식-html-대조) | RFC 8174 헤더 Updates 및 §2를 확인. 9110·9112 양쪽의 Obsoletes와 서로 다른 범위를 읽어 단일 자동 대체의 반례를 확인. | RFC 2119·8174의 origin HTML target 2 |
| Q7 | [비교 JSON](receipts/replay/comparison.json), [별도 폴더 기록](receipts/replay/), [재현 명령](replay.md) | 원 axe JSON fingerprint는 8/8 다름. timestamp만 제외 시 8/8 같음. 합성·작성 앵커 7/7 원 dump 재생 같음. 재생 전 정책 재확인. | 원 게시 8 fragment 재생, 반복 환경 바깥의 안정성 |

## 관측 분모

| 단위 | 예정 | 관측 | 공석·결측 |
| --- | ---: | ---: | --- |
| 최초 WCAG 원페이지 HTTP/바이트 | 3 | 0 | 미확인 3. CONNECT 단계 실패 영수증 3 |
| 최초 WCAG 공식 본문 절 | 6 | 6 | 결측 0 |
| 최초 WCAG 원 게시 HTML parse/Chromium :target | 6 | 0 | 미확인 6. Chromium 오류 영수증 6 |
| axe 공식 tarball / 실행 JS | 2 / 2 | 2 / 2 | 결측 0 |
| 주 axe.run / 호출×대상 rule | 24 / 96 | 24 / 96 | 결측 0. 적용 불가 60, 미보고 16, 한 셀의 V/P 병존 6 |
| 같은 브라우저 ARIA 통제 | 원 입력·반전·유일화 18 / 추가 6 | 18 / 6 | 결측 0 |
| RFC 2119/8174 공식 본문 및 헤더 | 2 | 2 | 결측 0 |
| RFC 원 게시 HTML parse/Chromium :target | 2 | 0 | 미확인 2. HTTP/Chromium 오류 영수증 2 |
| 대표 재생 axe / 원 게시 WCAG / RFC | 8 / 6 / 2 | 8 / 0 / 0 | 원 게시 8 미확인. 권한 상태 재확인과 실패 증거 보존 |
| 별도 합성/작성 소스 앵커·재생 | 7 / 7 | 7 / 7 | 결측 0. 합성의 :target 공석 2는 정상 관측 |

[원장](sources.jsonl) 51행 중 열람 46, 원바이트 경로 실패 5, 성공했으나 같은 저작 또는 작성 소스인 9행은 중복 제외다. 고유 37개, 원천 계보 10개다. 하한 대비 3/3 W3C 날짜판, 5/3 정오·결정·재발행, 12/8 axe 규칙·시험·결정, 4/3 브라우저·계산 이름·실행 API, 6/3 RFC를 확인했다. 별도 해설 3, 배포 레지스트리 2, 소비자 맥락 2도 원장은 독립 저작으로 센다.

날짜가 확인된 사건 16건은 REC 최초 3건 W20–W22, 제거 병합 W07, 2.0/2.1 노트 결의 W06, 2.1 정오표 항목 W05, 2.1 재발행 W08, axe 4.7.2·4.8.0 발행 2건 A09, 두 규칙 변경 병합 P01·P02, RFC 2119·8174·7322 발행 3건 R01·R02·R04, RFC 7230의 분기 개편 R05·R06 한 건, 소비 제품 채택 X02다. 2.0 #13 개별 최초일은 미확인이고 X01 제보는 관측 사례다. 사건 단위는 통계적 독립성 가정 없는 작업 이력이다. 같은 사건의 구현·시험·배포 자료 및 실행 receipt를 여러 독립 사건으로 세지 않았다.

## 고정 결과에서 확인할 항목

RESULT의 첫 두 표는 6행×6열, 24행×6열이 원행과 맞아야 한다. 마지막 약점 세 행은 4열을 사용한다. 표 2의 원 JSON과 case JSON, 각 Q의 원장 ID·근거·반증·미확인, CSV 및 재생 간의 노드와 결과 분류를 대조한다. 허용 경로 전체와 커밋별 변경을 확인하고, 고정 결과판을 다시 읽은 checker 범위와 종료 결과는 마지막 인계에 기록한다.
