# AF-RES-264 범위와 사전 판정

## 착수판과 선행 근거

GitHub 저장소 `laadkke-arch/agentflow-open`의 `chore/workspace-foundation`을 가져와 2026-11-25T00:58:42Z에 [착수 ref 조회](receipts/start/remote-refs.txt)를 기록했다. 시작/계약 SHA는 `3c32c1b44bd139819485548cb50e69e254288fad`다. 당시 원격 `work/research-af-res-264` 행은 없었고 작업 브랜치를 이 통합판에서 분리했다. 요청 계획판에는 AF-RES-264 행이 없고, 착수판에서 AF-RES-264 `RUNNING`, `codex-cloud`, 시도 1, manifest `af-res-264`, `depends_on=[AF-RES-243]`, `owned_path=docs/workstreams/research/AF-RES-264/`를 확인했다. 배정 당시 source/result 필드는 null이며 원장 SHA를 대입하지 않았다. [요청 계획판](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/automation/dot-control.json) · [착수 진행표](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/docs/automation/dot-control.json) · [읽은 배정 필드](receipts/start/assignment.json)

착수 기준의 AGENTS, STATE, Dot, 연구 운영, Cloud, START_HERE를 읽었다. 비교에 쓰는 과제 기준은 요청 SHA의 브리프와 연구 운영이다. 진행표와 상위 색인은 통합 담당의 경로다. [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/AGENTS.md) · [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/STATE.md) · [DOT_AUTOMATION.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/docs/DOT_AUTOMATION.md) · [연구 운영 고정판](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/RESEARCH_WORKFLOW.md) · [제품 연구 브리프 고정판](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/product/RESEARCH_BRIEF.md)

직접 의존은 AF-RES-243 한 건이다. 중앙 DONE, 작업자 PARTIAL, 중앙 result/HANDOFF 커밋 `001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41`, 인계가 명시한 분석 고정 커밋 `5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88`을 구별한다. 다음 네 파일을 요청한 첫 SHA에서 열고 의존 브랜치 head와 맞췄다. [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41/docs/workstreams/research/AF-RES-243/HANDOFF.md) · [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41/docs/workstreams/research/AF-RES-243/RESULT.md) · [formats](https://github.com/laadkke-arch/agentflow-open/blob/001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41/docs/workstreams/research/AF-RES-243/formats.csv) · [followup](https://github.com/laadkke-arch/agentflow-open/blob/001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41/docs/workstreams/research/AF-RES-243/followup.csv)

`workbench.session start --fetch`의 허용 경로와 원격 의존을 [session.json](session.json)에 고정했다. manifest도 소유 경로에 둔다. 실제 명령과 종료 0은 [착수 영수증](receipts/start/)에 있다.

### 사전 노출

착수·봉인 사이 AF-RES-243 RESULT·formats·followup·HANDOFF에서 #4856/#4853의 원저자 요청과 병합 시점, 2.3 템플릿의 `contentsname` 조건부 및 2.2.3.2의 부재, 선행의 D 실험 예상, EPUB 두 nav/spine 구조와 항목 수를 읽었다. 봉인 시점의 예측은 이 선행 지식에 조건부다. 두 정확판의 실행물·PDF·파서·직접 EPUB 추출은 봉인 뒤에 처음 확인한다. 현 환경의 설치 기본 Pandoc은 3.1.11.1이며 과제 대상으로 쓰지 않는다.

## 입력·단위·범위

- Pandoc jgm 태그 `2.2.3.2`, `2.3` 각각의 Linux x86-64 공식 배포 또는 해당 원코드 빌드. 태그 커밋·다운로드 바이트/실행 파일·`--version`·내장 `--print-default-template=latex`와 태그 `data/templates/default.latex`를 확인한다.
- 고정 [document.md](fixtures/document.md)는 UTF-8이고, 문서 제목 `Field Notes 264`, 두 section과 각 subsection, 본문에 `café`가 있다. 목차 제목 고유 토큰 `Archive Contents 264`은 `--metadata=toc-title:Archive Contents 264`로만 넣는다. 없는 조건에는 해당 인자를 생략한다. `--toc`도 켤 때만 전달한다. Markdown→JSON과 Markdown→standalone LaTeX에 같은 실험 인자를 전달한다. 기본 article·10pt·같은 TeX 패키지/폰트·같은 환경, 같은 파일명, UTC. 사용자 데이터 템플릿은 비어 있는 명시 경로로 격리한다.
- 단위는 두 정확판 × toc off/on × 제목 없음/고유값의 **8셀**, 셀마다 신규 작업 폴더 **2회**로 16번. 모든 PDF 실행은 pdflatex **3패스**로 고정하고 매번 PDF·aux·toc·out·log·fls 및 stdout/stderr/종료를 보존한다. 파일명은 셀과 반복 모두 동일하고 새 폴더 여부를 기록한다. 대조군은 별도 동수 패스, 주행렬 분모에서 제외한다.
- 단위는 또 직접 연 원파일/사건·저작 계보·PDF 실험 3가지로 구분한다. 직접 원자료 하한은 요청·수정·릴리스 4, writer·템플릿·시험 6, TeX/PDF/파서 5, EPUB 패키징/탐색 5. 동일 저작의 미러·복제·실행 반복을 추가 자료로 세지 않는다.
- 현재 제공된 공통 TeX 환경의 통제 실행이다. 원작성자의 설치판·행동과 최초 요청판은 미확인이다. #449/#3555/#4519 역사 GUI, CSS 제목 줄바꿈, 오디오, 운영 저장소·신규 제품 연동은 적용 대상 밖이다. AF-RES-242/251/254/255 과제의 입력·정답·완료는 이 실행의 의존이 아니다.

## 경쟁 예측과 합격표

| 질문 | 우선 가설 | 대안이나 반증 관측 | 합격 기준 |
|---|---|---|---|
| Q1 | 바이너리 두 판의 내장 템플릿이 각 태그 원파일과 대응 | 패키지/사용자 데이터가 다른 템플릿을 로드 | 각 판 tag·asset·executable·실제 추출 일치 여부와 실제 TeX 로드 목록·임베딩 폰트 보존 |
| Q2 | JSON에 키/문구가 들어와도 TeX의 `contentsname`은 2.3+toc+고유값에서만 나타남 | reader/CLI가 값을 버리거나 writer 내 버전 조건이 직접 출력을 제어 | AST 값·헤더 4개, TeX 줄번호와 문맥, 문서 제목 비교 |
| Q3 | toc on일 때만 인쇄 목차 제목과 4개 항목이 최종 PDF에 표시되고 본문 헤더 4개는 유지 | 한 패스에서 항목 공석 또는 클래스에 따라 목차가 페이지를 바꿈 | 각 반복 최종 PDF 페이지/순서와 pass 1–3 원영수증. 본문과 목차 동명 항목 구별 |
| Q4 | 일반 본문 네 책갈피의 Title/부모/목적지가 유지, 페이지 좌표는 목차 공간의 영향을 받을 수 있음 | 클래스가 목차를 자체 책갈피로 등록하거나 패스 누락으로 전체가 공석 | MuPDF와 pypdf 각자 트리·대상(원키, 해석 페이지/좌표, 부모)을 읽고 상이/실패/정상 공석 표시 |
| Q5 | 그 문자열의 override는 템플릿을 따라감 | 교차 템플릿에 writer 문맥 키가 없어 실패하거나 블록 삭제 뒤에도 표시가 남음 | 양방향 교차 + 2.3 조건부 블록만 제거해 TeX와 PDF 두 판독 비교, 실패 원문 보존 |
| Q6 | 기본값 `Contents` 명시/키 생략, toc off, 동일 입력 재실행은 같은 읽기 결과를 낼 수 있으며 해시 일치와는 별도 | 문자열 동일하나 링크 또는 폰트/좌표 변화, 혹은 PDF byte 차이가 날짜·ID 외에도 존재 | 제목·항목·정확한 destination·페이지 배치와 원해시를 별도 비교. 기본값은 TeX article 영어값 가설이며 원로그에서 확인 |
| Q7 | Creative Commons 예제 nav가 spine에 포함되고 La Page Blanche nav는 별도; 각 nav 표제/항목과 spine 순서를 분리 | nav라는 파일명과 실제 manifest/spine 참조가 불일치 | 243의 네 고정 blob을 같은 XML 파서로 추출, nav 표제·toc/page-list·ordered spine·linear와 resolve 경로 보존 |

비교량은 Title·부모 경로·목적지 이름/페이지/모드/좌표와 인쇄 영역·문구·표시 순서다. MuPDF 좌표가 화면 기준일 때 PDF 좌표로 환산해 비교한다. 인쇄 제목이나 항목이 없음을 읽은 경우는 **정상 공석**, parser nonzero·비정상 raw·바이너리 미확보는 **미확인/실패**, 실행하지 않은 것은 **미실행**, EPUB viewer UI나 원사건 성공률은 **적용 대상 밖/미수신**으로 기록한다. 대조는 writer×template swap, 2.3 조건부 삭제, 기본값 명시, 날짜/ID, 최소 책갈피 공석 검사, EPUB 두 개다. 고정판에서 각 실험을 다시 실행해 읽기 관측을 비교한다.
