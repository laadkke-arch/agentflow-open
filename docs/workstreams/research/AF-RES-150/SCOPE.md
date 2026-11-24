# AF-RES-150#1 연구 범위와 비교 기준

## 2026-11-24 UTC 시작과 기존 노출

- GitHub 최신 `chore/workspace-foundation` 시작 SHA `35ca756d1b18af5d89c3eb53659365c09f1f88e3`. 계획판은 `ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19`. 원격 지정 브랜치가 없음을 `git ls-remote --heads`와 GitHub 브랜치 조회로 확인한 뒤 최신판에서 만들었다. [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/AGENTS.md) · [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/STATE.md) · [DOT_AUTOMATION.md](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/docs/DOT_AUTOMATION.md) · [RESEARCH_WORKFLOW.md](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/docs/RESEARCH_WORKFLOW.md) · [RESEARCH_BRIEF.md](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/docs/product/RESEARCH_BRIEF.md) · [진행표 AF-RES-150](https://github.com/laadkke-arch/agentflow-open/blob/35ca756d1b18af5d89c3eb53659365c09f1f88e3/docs/automation/dot-control.json).
- 고정 선행 인계는 짧은 메모의 성공 조건과 이력의 해석 한계를 보여 주었다. 003의 분류·수작업 사례, 023의 MusicBrainz·ROR·Homebrew·Wikidata 사건 키를 중복 제외에만 사용한다. 자체 모집에서 얻은 기록만 새 결과에 넣는다. [AF-RES-003](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/HANDOFF.md) · [AF-RES-023](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md).
- 범위는 출처 위치·대상 연속성·버전과 부분 기능·정정이다. 순위·가치 점수·재확인 정책·제품 스키마 결정은 별도 과제다. 계약은 이 폴더의 [manifest.json](manifest.json)에 고정했다. 수집·해석·채점은 같은 작업자가 하므로 외부 검토자 차폐 시험은 성립하지 않는다.

## 사전 탐색에서 얻은 작동 원리와 반대 가설

| 먼저 연 원문 | 작동 원리 | 사전에 잡은 반례 가능성 |
| --- | --- | --- |
| [GitHub 이관 규칙](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository#whats-transferred-with-a-repository) | 소유자 전환 뒤 이슈·릴리스·Git 이력과 옛 경로 전달. 대체 경로와 한 줄 설명만 남기는 기준을 시험한다. | GitHub Pages는 별도이며, 옛 경로 재사용은 전달을 없앨 수 있다. 문자 동일성이나 301 하나로 일반 동일성을 추론할 수 없다. |
| [MARC 775](https://www.loc.gov/marc/bibliographic/bd775.html), [Crossmark 등록 §3](https://www.crossref.org/documentation/crossmark/participating-in-crossmark/) | 같은 작품/원 DOI 아래 판 또는 알림마다 자기 주소를 부여하고 연결한다. 판을 고정하면 과거에 본 내용을 보존할 수 있다. | 같은 작품·DOI가 기능·절의 동일성을 보장하지 않는다. 수정 알림이 없거나 한 DOI에서 덮어쓰는 경우가 있다. |
| [Darwin Core Identification](https://dwc.tdwg.org/terms/#identification), [Open Library #6371](https://github.com/internetarchive/openlibrary/issues/6371) | 동일 표본의 재동정에 주체·시점을 따로 붙인다. 도서관의 판 되돌림은 이후 무관한 필드까지 잃을 수 있으므로 변경 관계만 취소하는 대안을 여기서 도출했다. | 거래 로그가 풍부해도 필요한 관계 범위나 결정 주체가 공개되지 않으면 보류가 남는다. 자료가 짧고 안정적이면 별도 관계는 쓰기만 늘린다. |

## 모집과 판정 고정

자연 사건은 날짜 있는 생산자·편집자·판 기록을 직접 열어 하나의 변경 또는 공개 분쟁으로 묶는다. 소프트웨어의 이관·분기·재구현과 문서 판 이동, 작품·판/목록 정정, 표본 재동정, 학술 정정 순으로 찾는다. 예비 후보는 Node/io.js, Hudson/Jenkins, Atom/Pulsar, Compose, IPython/Jupyter, 실제 저장소 이관, 공식 버전·번역 문서, Open Library, Darwin, Haarlem 표본, DOI 정정이다. 관측된 기록과 고정판이 없는 후보는 대체 이유를 남긴다. 안정 대조는 변경 대상의 수와 섞지 않으며, 고정 규격·버전·판 안에서 두 표기가 같은 범위를 가리키는 확인을 우선한다. 바이트 동일성이나 기간 전체의 무변화를 입증하지 못하면 절·판·관측 범위로 제한한다.

대표 원전 최대 60저작과 접근 실패·동저작 대체 주소 최대 20건을 본 비교 모집의 탐색 한도로 둔다. 최소 24저작을 주역할 한 번씩 센다. 당사자 변경 8, 독립 소비자 인용 **또는** 고정판 6, 비소프트웨어 실제 사건 자료 6, 운영 규약·공개 구현 4를 각각 검사한다. 자연 사건 12와 안정 대조 4, 합칠 주소 쌍과 분리할 쌍이 포함될 때 데이터와 기대값을 분석 실행 전에 커밋한다. 원전·사건·발행 주체 수와 고정판/독립 인용 수를 따로 센다. 접근 실패, 미개봉, 검색 요약과 번역/미러가 같은 저작을 중복 대표하는 경우는 하한에서 제외한다.

| 조회 ID | 질문과 시점 | 기대값의 근거 |
| --- | --- | --- |
| F | 이 인용을 처음 따라갔을 때 실제 주소와 판은 무엇인가 | 최초 고정 인용, URL과 핀 |
| L | 지정 시점에 이 인용의 목적에 맞게 읽을 원문 위치는 어디인가 | 위치·절·범위, 연결이 합의되지 않으면 보류 |
| T | 당시 인용이 지목한 기능·판본 구절·표본 주장은 무엇인가 | 최초 판/절의 작동 설명 또는 관찰; 이후 기능으로 치환하지 않는다 |
| A | 그 시점까지 공개된 관련 정정의 주체는 누구인가 | 편집·이관·철회·관계 정정을 실제 발표한 주체; 검색엔진/호스팅 담당과 구별 |

같은 네 조회를 사전과 사후에 질의한다. 공개 시각은 원자료에서 그 사실을 알 수 있는 하한이며 현재 직접 읽은 시각은 원장에 따로 기록한다. 과거 체크포인트에는 공개 전인 정정 행을 기록기에도 보내지 않는다. 사후 저장소에 과거 시점 조회를 다시 걸어 오염 여부를 별도 판정한다. 날짜 해상도가 일 단위이면 같은 날 시각을 발명하지 않는다. 발표가 소급될 때 적용일과 공개일을 모두 기록한다. 기대값은 작업자의 명시적 판독이며 원자료 원문이나 외부 채점자의 판단과 구별한다. 판정에는 내용값과 증거 ID를 함께 쓴다. 보류는 이견/범위 부족에 근거가 있을 때 정당하다. 원전에 알려진 답을 반환하지 못하면 근거 소실, 동치 대상 분리 및 별개 대상 연결은 별도 쌍 판정에서 오분리·오병합, 다른 목적지·주체는 오답으로 센다. 관련 없음·정정 관측 없음·미확인을 구별한다. 수치를 알 수 없으면 미확인, 분모 0은 산출 불가로 쓴다.

## 비교와 반증

- URL+짧은 메모는 같은 URL이 같은 내용으로 남을 때 네 조회의 좁은 요구를 충족할 수 있다. 별칭이나 같은 주소의 개정이 있을 때 손실을 예측한다.
- 공통 키+고정 관측 판은 역사 출처와 기능을 되살리고 중복을 낮출 수 있다. 너무 넓은 외부 식별 키가 별개 판을 붙이는 반례를 찾는다.
- 관계·주체·공개 시점의 변경 이력은 부분 계보, 충돌, 한 연결의 취소를 표현할 수 있다. 빈 관계 또는 모호한 귀속에선 오분리/보류가 남을 수 있고 쓰기와 바이트가 늘어난다.
- 실제 사건의 정정 순서에 따른 재생, 조회 요청 순서 변경, 동일 사건 전달 중복·정정만 역순·트랜잭션 중간 실패·재실행, 고의 오병합/오분리와 취소를 따로 비교한다. 각 필드나 관계의 제거는 한 번에 하나씩 적용한다.
- 생산자는 선언 가능한 동일성, 인용자는 당시 근거, 정정 편집자는 영향을 받는 연결 범위, 후속 설계자는 비용과 누락을 각각 본다. 설명에 이미 노출된 작업자의 가설을 검증하므로 모집 비율을 실제 발생률로 일반화하지 않는다.

비교 설계 문서를 데이터 확정 및 최초 실행에 앞서 커밋한다. [models.md](models.md)에 각 저장 방식의 예정 경계와 단위를 적었다.

## 2026-11-24 보강 조회의 동결

12 자연 사건·4 고정 비교쌍과 최초 두 시점의 기대값을 `b08e46d11fddc578fc6f3a20336cc2014302188c`에서 봉인했다. 첫 구현 동작 확인 후 기존 판정은 유지하고, 보강 조회를 추가했다. N01의 2015-09-10은 Node 4 릴리스 뒤, 통합 발표 전이다. 옛 인용으로 물을 때는 두 문서가 있다고 해서 이 날에 공식 통합 선언을 알고 있었다고 보지 않는다. N03·N06·N12의 새 인용에서는 새 주소·판·기능을 독립적으로 묻는다. 새 주소 행 자체에 붙은 정정 주체만 이 보강 조회의 대상이다. 이전 주소의 이관 공지나 철회자까지 새 관측에 이식하면 오답으로 판정한다.
