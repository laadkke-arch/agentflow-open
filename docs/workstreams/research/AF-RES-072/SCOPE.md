# AF-RES-072 사전 계획

2026-11-23 · codex-cloud · `laadkke-arch/agentflow-open` · `work/research-af-res-072`

계획판은 `320424d87f99e70c42eeb8cb7211467de27f2c2e`다. 08:22 UTC 시작 조회에서 통합 HEAD `17b9cd4090a924f30ad7a2c8fc24e86b08a0e785`를 읽고 그 SHA에서 브랜치를 만들었다. 계약의 `--fetch`는 뒤이어 AF-RES-069/070 배정 행만 바뀐 `76b8c1d15812fbf91b879f8444fd188ae7445802`를 확인했다. 두 시점은 [작업 계약](manifest.json)에서 각각 base와 integration이다. [AGENTS](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/AGENTS.md) · [상태](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/STATE.md) · [연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/docs/product/RESEARCH_BRIEF.md) · [운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/docs/RESEARCH_WORKFLOW.md) · [Dot](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/docs/DOT_AUTOMATION.md) · [배정 행](https://github.com/laadkke-arch/agentflow-open/blob/17b9cd4090a924f30ad7a2c8fc24e86b08a0e785/docs/automation/dot-control.json)

유일한 의존은 AF-RES-068 인계 `2c9642dff48ec0da2785c2c127d3a906182f7834`다. 그 비교에서는 Ajv와 jsonld.js 후보와 순위를 먼저 고정했다. 첫 도착 창을 36개 읽었고 적격 둘째 열람과 두 사용 조건·환경의 공동확인은 각각 관측 0이었다. 072에서는 공개 자료집 경계를 고정하고 후보 선택과 다음 방문을 다시 관측한다. 기존 12요구와 열린 웹 발견, 입력 계약, 갱신 연구는 비교 분모 밖이다. [인계](https://github.com/laadkke-arch/agentflow-open/blob/2c9642dff48ec0da2785c2c127d3a906182f7834/docs/workstreams/research/AF-RES-068/HANDOFF.md) · [두 표](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/RESULT.md) · [경로](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/routes.csv) · [집계](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/metrics.json) · [노출](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/actual-exposure.json)

## 모집

세 공공 목록을 08:23–08:27 UTC에 확인했다. Java 실용 라이브러리, 표 데이터 교환 규격, 연방 기록 보존은 출발 어휘와 적용 환경이 다르다. 모집은 프로젝트·출판 그룹·문서 목록 단위다. Zotero와 OpenRefine을 이슈 출처로 고른 이유는 서로 다른 공개 데스크톱 설계 맥락과 공식 이슈 목록의 시간 정렬 때문이다. Java와 표 데이터라는 주제의 일반적 근접성을 인지했으며, 이슈 제목·본문·후보를 사용해 자료집 순서를 바꾸지 않았다.

- A 8자리. Apache Commons 홈의 **Apache Commons Proper** 표 위에서 아래로. BeanUtils 1.X/2.X는 같은 계보로 한 자리다. 첫 원문은 ASF가 공개한 소스 저장소의 관측 기본 HEAD에서 `src/site/xdoc/index.xml`, 파일이 없을 때만 `README.md`, `README.txt` 순이다. 발행 목록의 버전 문자열과 소스 HEAD는 별도다. [공식 목록](https://commons.apache.org/#Apache_Commons_Proper)
- W 6자리. CSV on the Web 그룹의 **Recommendations** 전부와 **Notes** 앞 2편. 동일 절 안에서 화면 표시 순서를 쓴다. 그룹의 공개 Git 저장소 `publishing-snapshots`에 있는 날짜판 `Overview.html`을 검색 주소로 쓴다. Primer의 설명서와 Use Cases의 요구서는 별개 편집·목적·발행물이다. 링크된 그림과 데이터 파일, 목록의 번역 및 다른 판은 분모 밖이다. [공식 목록](https://www.w3.org/groups/wg/csv/publications/) · [공개 발행 스냅샷](https://github.com/w3c/csvw/tree/b3f461db0e86a68c019bc1f912e86f3555907e34/publishing-snapshots)
- N 6자리. NARA의 **Record Category Preservation Action Plans** 디렉터리에서 `NARA_PreservationActionPlan_*.md` 파일명 ASCII 오름차순. 여섯 발행 계획은 각기 따로 인용할 수 있는 계획 날짜와 기록 유형, 보존·전환·접근 기준과 독립 본문이 있다. 공통 템플릿, PDF 사본, 스프레드시트의 형식별 행은 세지 않는다. [공식 목록](https://github.com/usnationalarchives/digital-preservation/tree/197bdaab6c152066badea527f1f60dbf6b62a5fe/Digital_Preservation_Record_Categories) · [공식 범위](https://github.com/usnationalarchives/digital-preservation/blob/197bdaab6c152066badea527f1f60dbf6b62a5fe/README.md#record-category-preservation-action-plans)

[자료집 모집틀](corpus-frame.csv)에서 선정·선행 중복 제외 및 예비 순번을 고정한다. 같은 저작의 다른 판·번역·미러와 구성표 행을 별도 원저작으로 세지 않는다. 죽은 링크는 시도와 빈자리를 유지하고 같은 부모의 다음 예비만 쓴다. 조사 시 공식 발행자 공개 원본을 연다. 검색 실험의 고정 주소는 무로그인 GitHub raw의 해당 발행자 SHA path다. GitHub 주소와 다른 호스트에서 발행된 판의 바이트 동일성은 별도 확인 없이는 주장하지 않는다. 이 주소의 공통 노출은 URL, 작품 ID, 소유자, 공개 접근 경계뿐이다.

요청 모집은 두 저장소의 GitHub 공식 이슈 첫 페이지에서 UTC `2024-01-01..2024-06-30`, `is:issue sort:created-asc`다. 시간 동률이면 이슈 번호 오름차순. 각 목록 앞에서 작성자 본문의 한 부분 동작, 식별 가능한 사용 맥락, 명시된 대비·실패 또는 미결정 설계 경계가 읽히는 첫 4건을 쓴다. 하나의 같은 동작을 같은 범위에서 중복 보고한 건은 첫 건만 쓴다. PR·후속 댓글·링크만 있는 보고·재배치 대상이 없는 지원 요청·제품 전체 과제는 제외한다. 설계 작성자의 범위 선택이 미결정이면 경계로 그대로 보존한다. 각 프로젝트 첫 선정은 조정, 나머지 셋은 보류다. [Zotero 공식 목록](https://github.com/zotero/zotero/issues?q=is%3Aissue%20created%3A2024-01-01..2024-06-30%20sort%3Acreated-asc) · [OpenRefine 공식 목록](https://github.com/OpenRefine/OpenRefine/issues?q=is%3Aissue%20created%3A2024-01-01..2024-06-30%20sort%3Acreated-asc)

`requests.jsonl`의 조건은 공개 HTML에 포함된 GitHub issueViewerRoute의 작성자 body에서만 도출한다. 게시물의 시간·현재 bodyVersion·원문 UTF-8 해시를 붙인다. 이전 편집판을 받지 못하면 최초 접수 당시 문장은 미확인이다. 자연 한국어 접수건이 표본 내에 없으면 오프라인 한국어 번역을 따로 재생한다. 번역에서 추가된 의미를 점수로 사용할 수 없으며 같은 이슈를 두 번 세지 않는다. 원문 제목·본문에 이미 언급된 도구나 공급자를 표시한다.

## 판독과 접근 경계

카드 초안 TSV를 08:28:08 UTC에 봉인했다. SHA-256은 `f5c9b0812f876a0ef5c2928f392cd6769a25d1b9599d004a4f5f2804682cf528`다. 이전의 GitHub 이슈 페이지 연결 시험은 본문을 버렸고 이슈 제목·작성자 본문의 열람 및 모집은 카드 봉인 뒤에 했다. 첫 커밋은 이 모집·조건·초안 해시를 담고 카드 데이터는 다음 커밋에서 공개한다. 동일 작업자가 세 역할을 수행하며 자료집 기억 및 프로젝트 이름의 사전 지식이 있다. 판정 단계는 점수·방식·순위를 보기 전 가명 순서로 다시 읽는다. 문서의 고유 표현이 제목과 제품을 드러낼 수 있다.

검색 입력은 `urls.jsonl`, 요청, I/H의 카드 및 해당 경로가 실제 선택한 고정 주소의 본문뿐이다. L의 접근자는 작품의 본문을 선택 이후에만 열며 카드 파일을 읽지 않는다. 가림 판정은 같은 고정 본문에서 만들되 카드·순위·점수를 읽지 않는다. 정답 작업은 `qrels.csv`와 그 판독 기록으로 커밋한다. 순위는 별도 커밋·해시까지 정답을 읽지 않는다. 결합 전 양쪽 입력·출력 해시를 저장한다. 파일 접근 분리는 실행 로직이며 동일 사용자 계정의 OS 보안 격리는 아니다.

보류 6×20의 모든 쌍에서 직접 충족, 일부 조건, 반박, 무관, 미확인을 판단하고 동종·원거리를 별도 열로 기록한다. 원거리 적격은 공여 역할, 수신 역할, 옮길 조작, 전이가 깨지는 때를 모두 설명해야 한다. 판독에서 사용한 원문 절·쪽은 실험의 검색 입력으로 되돌리지 않는다. 결과는 고정 자료집의 재생과 원본 전송 성공·실패를 분리한다. [경로와 한도](RULES.md)
