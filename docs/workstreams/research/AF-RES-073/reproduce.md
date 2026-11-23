# AF-RES-073 기록 재검산과 재개

## 공개 기록 검사

공개 작업 브랜치 `work/research-af-res-073`를 별도 checkout으로 읽는다. Python 표준 라이브러리와 Git만 사용한다. 아래 검사기는 원장 연결·분모·예산을 검사하며 검색 품질이나 외부 원문의 진실성을 자동 판정하지 않는다.

```sh
git clone --branch work/research-af-res-073 https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git rev-parse HEAD
python -B docs/workstreams/research/AF-RES-073/evidence/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-073/manifest.json --fetch
git status --porcelain
```

최초 입력·질의 고정판은 `469d8c569e054622567ecf328150898ed384ada1`이다. 최종본의 질의와 그 고정판을 비교한다. 사후 검색 결과를 이 파일에 덮어쓰지 않는다.

```sh
git diff 469d8c569e054622567ecf328150898ed384ada1 HEAD -- docs/workstreams/research/AF-RES-073/queries.jsonl docs/workstreams/research/AF-RES-073/proposals.jsonl
```

모집의 첫8개, 순서와 제외는 frame.csv 및 recruitment/의 Git 명령·원커밋·blob 영수증으로 검산한다. SPEC7의 앞선 생존 브랜치와 SPEC2 경로 재사용은 다른 문서를 같은 파일명으로 합치지 않기 위한 사례다. 현재 master/main의 파일만 다시 보는 것으로 최초판을 검증하지 않는다.

## 검색의 재현 경계

온라인 검색은 시점·색인·개인화·도구 내부 순위의 영향을 받는다. 저장한 최초5순위와 실제 반환 참조가 이번 관측의 입력이며, 현재 같은 질의를 다시 실행하는 것은 새 시점의 추가 연구다. 원검색2회/원문작업6회, Q1R1→Q2R1 순서, 시작 보기의 순환은 SCOPE.md에 고정했다. 실패·중복·미열람을 그대로 재생해야 한다.

원실험 이후 읽은 토론·출시·절차·반례는 phase=postseal 또는 audit다. 새 URL이 이전 원순위에 없으면 그 자료가 얼마나 적합하더라도 원검색의 적중 수에 더하지 않는다. 원실험 읽기 수를 늘리려면 새 별도 층과 비용을 만들어야 한다.

## 미실시 적용 확인

이 과제는 공개 자료 비교다. 세 대상 프로젝트의 코드·운영환경·조직 권한을 바꾸지 않았다. 제품에 적용한 성공, 당시 작성자의 최초 인지, 사용자의 시간 절감은 별도 관측이다. 다음 첫 확인에는 원 요구의 버전·행위 주체·결과 관찰자·고정된 C1/C2를 함께 전달한다. 구체 최소 입력과 미해결은 judgments.csv, decisions.csv, SELF_CHECK.md 및 마지막 HANDOFF.md에서 확인한다.

JEP97을 실제로 시험할 때는 원래 diff와 full schema의 `$schema` required 목록 불일치부터 원 저자의 의도로 확정해야 한다. 어느 쪽을 실행 기준으로 삼았는지 기록하지 않고 성공으로 세지 않는다. 구형 reader, schema 판, 정규/비정규 URI 및 version pair를 고정한 뒤 동일 입력을 두 이행안에 주어야 한다.

## 원판 모집과 미실행 목표 검사

JEP122 첫 PR는 `2b194a3c090fd375321871c47a3de503a0758206`, SPEC9 첫 PR는 `6ddd0d85a8acf184e2e7e35899c0d80af639dc94`, JEP97 첫 PR는 `0f4510266ead738e62f1d9e412d6bb9e7eb7a97d`다. 이는 확보한 최초 생존 PR판이며 Git 이전 창설 원고의 증명은 아니다. JEP97의 실험 C2는 `e2651761a98f673d9c1e05d02e33ac4b3668c736`에서 추가된다. 새 모집에서 첫8 후보의 PR 커밋과 added-file 이력을 모두 대조한 뒤 새 질의를 봉인해야 한다. 원 frame/queries를 사후 교체하지 않는다.

[사후 재개 명령](postseal/P3/NEXT.md)은 nbformat5.7.3·두 validator·실제 구형 앱 설정과 [4개 JSON 입력](postseal/P3/fixtures.json)을 명시한다. [관측 probe](postseal/P3/probe_notebook_compatibility.py)는 구문만 확인했고 실행하지 않았다. 필요한 dependency lock과 실제 구형 앱이 없으면 현대 재구성 환경임을 표시한다. C2의 동일 URI/바이트 해시/버전쌍/alias 구성은 별도 입력이다.

공통 `scripts/check.py`와 `cloud_check.py`는 기본값으로 checkout의 `.workbench`와 실습 결과를 쓴다. 허용 경로 밖 쓰기를 피하기 위해 필요한 공통 검사는 소유 경로 내부의 임시 detached worktree에서 수행하고 로그·SHA 영수증만 보존한다. 작업 checkout에서는 지정 session check와 읽기 전용 evidence/verify.py를 실행한다. 임시 worktree의 검사와 최종 보고서 SHA 검사를 구분한다.
