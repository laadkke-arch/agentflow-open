# AF-RES-135 · 검산

같은 Codex 작업자가 배포와 문서, 실행, 집계를 다시 판독했다. 별도 모델·새 대화 검토는 미실시다. 두 Node 경로는 다른 설치 디렉터리와 HTTP 캐시를 쓴 같은 작업자의 실행이다. OpenLayers 원 로그와 비교하는 대상이었던 브라우저는 AF-RES-131의 고정판이다.

| 질문·주장 | 고정 근거 URL·위치 | 결론을 뒤집을 조건 | 실제로 찾아본 반증과 결과 | 남은 미확인·다음 검사 |
| --- | --- | --- | --- | --- |
| **Q1** · 지도 목록+거부 두 계약과 축척 27판의 입력별 답이 구별된다. | [사전 범위](https://github.com/laadkke-arch/agentflow-open/blob/912a1122a7b4b0e20f03e9232ef0959fb5468068/docs/workstreams/research/AF-RES-135/SCOPE.md) · [배포](releases.csv) | 기존 목록 조건의 구간 내 다른 계약, 누락 안정판 또는 추가 공개 순서 역전 | 64/64 모듈과 16개 소스 지문, 27/27 integrity, d3 사전판 3개와 3.2.2 음의 시계 차이 확인. OpenLayers의 10.7.2 공개 순위가 번호와 달랐다. | 이전 registry 스냅샷·미포함 사전판의 출력 미확인. 다른 날짜의 공개·삭제 근거를 대조한다. |
| **Q2** · 현재 HTTP 200과 해당판 기능 절은 다른 관측이다. | [신호 봉인](https://github.com/laadkke-arch/agentflow-open/blob/1db7e6785e6ade12d598766ba740a2d4886ebf57/docs/workstreams/research/AF-RES-135/signals.csv) · [GET 영수증](evidence/current-http.json) | 현재의 열린 주소에서 과거판 절도 식별할 수 있고 판 식자가 일치 | main과 v4.0.2 README를 각 GET 200으로 확인했지만 기능 절은 고정판 1/2에만 있었다. 6.6.1·6.7.0 HTML 본문은 접근 실패, JSDoc 64/64 해소. | 실제 당시 HTTP 응답은 미확인. 날짜와 판 본문을 함께 갖춘 웹 저장본을 찾는다. |
| **Q3** · 6.6.1→6.7.0 두 옵션의 우회와 목록 생략 대조가 갈린다. | [고정 지도 인계](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/HANDOFF.md) · [원 로그 ④ 신판](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.7.0-04-r1.json) · [시간](evidence/chronology.csv) | 같은 hit+조건에서 목록 생략도 우회하거나 10.7.2에 다른 Translate 동작이 있음 | 생략 ②·③의 관련 네 판 16/16 로그에서 geometry 보존, center만 이동. 역전 근처 네 판의 Translate 해시가 일치했다. 예제 설명 commit은 HTML만 변경. | 62개 인접쌍의 두 끝 브라우저 실측 미확인. 범위를 넓힐 때 정확판과 대상 Feature 종류를 먼저 고정한다. |
| **Q4** · 2.1.2→2.2.0과 3.2.3→3.2.4의 입력별 출력 전환이 재생된다. | [실행 고정판](https://github.com/laadkke-arch/agentflow-open/blob/860252f7500a7769baaf52a164ecf71134dbfe85/docs/workstreams/research/AF-RES-135/evidence/replay.json) · [의존 잠금](replay/locks.json) · [null diff](https://github.com/d3/d3-scale/commit/116ac06cd455b253b8df8ed42a3db402e59b401f) | 같은 직접 의존으로 맞추면 역전이 사라지거나 UMD→ESM에서 숫자 값이 바뀜 | 26/26 공유 직접 의존 대조를 실행했고 두 변경과 7개 수치 셀 불변이 같았다. 79/79개 사건이 별도 경로에서 동일하다. | 실제 앱의 다른 lock, interpolation mode, 런타임은 미실시. 추가로 시험할 때 그 버전과 정확 입력을 저장한다. |
| **Q5** · C는 d3 null을 놓치고 D는 대부분을 다시 연다. | [봉인 신호](https://github.com/laadkke-arch/agentflow-open/blob/1db7e6785e6ade12d598766ba740a2d4886ebf57/docs/workstreams/research/AF-RES-135/signals.csv) · [raw 전용 대조](evidence/output-comparison.csv) · [판정](decisions.csv) | 절의 실제 차이 또는 같은 끝값에 중간값이 달라 우회 검증의 손해가 관측됨 | 3.2.3→3.2.4 README 전체 일치, 배포 지문과 출력 변화. 반대로 3.3.0→4.0.0 배포 변화와 14셀 일치. 입력별 전체 순서 보존 삼중 탐색에서 중간값 이탈 0. 브라우저 미확인 62쌍의 두 극단을 재계산. | 전이 의존 한 단계가 바뀐 사례에 대한 평가 미실시. 다음 패키지에서 발행 노트·직접/전이 의존의 신호를 봉인한다. |
| **Q6** · 요청 시 검증은 고정판과 두 끝판에서 실행을 줄일 수 있다. | [사전 입력](https://github.com/laadkke-arch/agentflow-open/blob/912a1122a7b4b0e20f03e9232ef0959fb5468068/docs/workstreams/research/AF-RES-135/replay/inputs.json) · [질의 재생](evidence/query-replay.csv) · [비용](evidence/costs.csv) | 두 판 교차 요청이 일괄보다 더 많은 검증을 하거나 같은 최신 요청에서 다른 답 | 고정판 1회와 두 지원판에서 요청 시 직접 목표 검증이 적었다. d3 최신 매 공개는 A–D별 양쪽 집계가 같고 C는 두 방식에서 최신 5/27개 응답이 틀렸다. 캐시 적중과 이월을 각각 재집계. | 사용자 트래픽·시간 비용 미확인. 실제 질의 순서와 URL 캐시 적중을 별도로 관측한다. |
| **Q7** · 지도와 교통에서 제목·카탈로그 경로보다 판 식자·적용일이 필요하다. | [USGS 판 설명](https://www.usgs.gov/faqs/there-are-multiple-copies-same-map-your-historical-topographic-map-collection-all-have-same) · [11월 공지](https://wsdot.com/FERRIES/SCHEDULE/bulletin.aspx) · [도메인 영수증](evidence/cross-domain.md) | 동일 도엽명·인쇄판에 스캔만 바뀐 사례에서 표식 동일 또는 날짜표와 공지 불일치 | 2/2 카탈로그에서 조사와 인쇄 시계 분리. 원면 개별 요청 실패. 같은 LoC 판의 2개 디지털 크기에서 판·도로·색 표식 일치. 공지가 다른 노선에 통상 목요일을 적용하는 반례를 읽었다. | Vienna 원면 0/2, 기관 재스캔 0/1, 휴일 자체 날짜별 화면 미확인. 두 PDF의 식자·범례부터 연다. |

## 재검사 명령

```sh
python -B docs/workstreams/research/AF-RES-135/replay/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-135/manifest.json --fetch
```

감사는 생성기와 별도 집계에서 91판, 출력 비교 104행, 지도 raw 32행, 판정 11,280행, 질의 840행, 비용 48행, 출처 후보/열람/적격 48/42/32를 대조한다. 로컬 링크 대상, 마지막 표의 정확히 세 자료행, Git 소유 경로도 검사한다. 원격 대표 파일은 각 묶음의 커밋 해시로 GitHub에서 다시 읽었다. [자체 검산 코드](replay/audit.py) · [출처](sources.jsonl)
