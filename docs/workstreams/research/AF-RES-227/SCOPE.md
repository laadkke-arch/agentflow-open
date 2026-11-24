# AF-RES-227 범위와 사전 고정

## 기준판과 노출 순서

| 항목 | 고정값 |
| --- | --- |
| 계획 통합판 | `fc095c323d0177401d34f1daa7b4d1c529e2351f` |
| 착수 통합판 | `f3895893e32e2c055cefde446d34f1467fa27b4c` |
| 계획판 대비 | `docs/automation/dot-control.json` 한 파일 변경, 작업 216→227개. 계획판에 AF-RES-227 슬롯이 없고 착수판에서 RUNNING/attempt 1, 직접 의존 AF-RES-210, 브랜치·소유 경로가 확인됐다. AF-RES-210 결과 SHA와 공통 계약 본문은 동일했다. |
| 작업 브랜치·범위 | 새 `work/research-af-res-227`, `docs/workstreams/research/AF-RES-227/`. 최신 통합판과 의존 브랜치의 HEAD를 `workbench.session start … --fetch`로 확인했다. [session.json](session.json) |
| 직접 의존 | 중앙 AF-RES-210은 DONE, 자체 인계는 PARTIAL. 의존 SHA `097948b68f3be1802c06c15c7beccaeb5478c06c`의 입력·기대 수준·네 단계 예측을 그대로 사용한다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/097948b68f3be1802c06c15c7beccaeb5478c06c/docs/workstreams/research/AF-RES-210/HANDOFF.md) |
| 읽기·실행 순서 | GitHub의 운영 지침과 최신 진행표 → 210 인계·입력·범위·예측·결과·반례 → 이 범위와 입력을 커밋 → 공식 소스·시험·원전 원장 커밋 → 순정 실행과 그 영수증 커밋 → 계측·반례와 별도 경로 재생 → 결과·자체점검 → 마지막 인계. |
| 노출 | 210의 R1–R4 공개 기대와 R4 구현 일부가 이미 노출되었다. 210의 M/P 재구성, I 소스 예측, E 공개 기대 대조를 각각 원문대로 보존한다. C1–C4에는 공개 fixture 기대가 없고 210 소스 예측은 이미 읽었다. 이번 순서는 관측 전 판정 규칙 고정이며 블라인드 연구는 미실시다. |

## 선정과 조건

- R1–R4, C1–C4의 순서·배열·원래 요소·기대 수준은 [inputs.json](inputs.json)에 고정한다. 공개 시험에서 유래한 4쌍과 합성 4쌍이다. 입력 문자열을 임의 보정하거나 줄을 제거하면 해당 시행은 결측이다. 216의 PyPI 플래그, 217의 OCR, 218의 FITS, 199의 원과제는 모집 범위 밖이다.
- Git은 [v2.43.0](https://github.com/git/git/tree/v2.43.0) tag object `c089584ac8dedc3aa7c2c404839bc098050298a2` → commit `564d0252ca632e0264ed670534a51d18a689ef5d`. Breezy patiencediff는 [v0.2.13](https://github.com/breezy-team/patiencediff/tree/v0.2.13) tag object `3039783fde723950d36eeafa28b970a63ed59b7c` → commit `834fad2d280fa0634d00d658c61c15d82031f519`. 두 값은 GitHub의 peeled refs에서 읽었다. 실행 시 checkout·빌드·바이너리·Python 모듈 경로와 지문을 재검증한다.
- Git의 모든 기본 시행은 임시 디렉터리의 동일한 상대 경로 `a`, `b`에 UTF-8 LF 바이트를 써서 `git --no-pager diff --no-index --no-ext-diff --no-textconv --no-color --diff-algorithm=… -U3 --indent-heuristic [R1: --ignore-space-at-eol] -- a b`로 실행한다. 알고리즘은 patience, histogram, myers. 시스템·전역 config와 시스템 attributes를 차단한다. 입력 디렉터리에는 저장소와 attributes를 두지 않는다. `LC_ALL=C`, `LANG=C`, `TZ=UTC`, 명시적인 최소 환경을 사용한다. 차이 있음(1), 같음(0), 실행 오류(나머지)를 분리한다.
- Breezy는 `PatienceSequenceMatcher_py`를 직접 넘겨 `get_matching_blocks`와 `unified_diff(n=3)`를 한 새 Python 프로세스에서 부른다. matched blocks는 원본 요소를 사용한다. R4의 원래 문자열 목록에는 LF가 없다. unified diff 출력에는 Git과 같은 LF 투영을 쓰고 그 투영의 matching blocks도 별도로 보존해 일치 여부를 확인한다. Breezy는 정확한 요소 동등성으로 비교한다. R1 고정 배열에는 trailing whitespace가 없으므로 Git의 플래그가 whitespace-only 변경을 숨기는 능력 자체는 별도 통제에서만 평가한다.
- 반복 1과 2는 새 작업 디렉터리와 새 프로세스 두 번이다. 각각 순서는 R1–R4, C1–C4, 각 쌍에서 Git patience/histogram/myers와 Breezy Python. 기본은 32쌍·방법 셀, 실행 64자리이다. 별도 checkout·입력 작업 경로에서 같은 64자리와 비교 통제를 재생한다. 반복과 재생은 같은 표본에 대한 반복 검증이다.
- 표준 출력 stdout 원바이트, stderr, 순서·argv·환경·exit·지문을 영수증으로 저장한다. 서로 다른 도구의 patch header와 hunk range 문법이 달라서 최종 사용자 hunk의 **바이트 동률**과 **의미 동률**을 별도로 적는다. 의미 동률은 순서 있는 hunk별 1-based 구간을 정규화(생략된 count=1), 맥락·삭제·추가 본문과 각각의 줄 위치를 동일하게 비교한다. R2/R3의 공개 기대와 비교할 때는 시험의 header 정체성/파일 이름 정규화만 적용한다. `diff` 1도 유효한 관측이다.
- 재생 지점 및 진단은 각각 별도 분모다. C1–C4에서 Git context 0/3 × indent off/on × 정방향/역방향 완전 교차를 한다. Breezy는 context 0/3 × 정방향/역방향이고 indent 범위 밖이다. 진단은 순정 영수증 보존 이후 임시 소스에 별도 계측한다. 동일 옵션의 순정 stdout과 계측 stdout 바이트를 대조한다. context 및 방향 비교와 공백 대조, upstream 공개 시험·보강 반례는 기본 64에 포함하지 않는다.

## 사전 채점 규칙

- 210의 32행은 원래 비교 단위와 노출대로 모두 연결한다. 방법별 실행 32셀과 210의 단계별 32행은 별도 표다. M/P는 주장된 단위만, I는 예측한 분기/앵커/편집을 각각, E는 공개 기대 수준으로 채점한다. 추정 대상이 없거나 trace가 필요하고 미측정이면 명시한다.
- R1 공개 기대는 Git patience의 `^+.*X` 조건 하나다. R2/R3는 Git patience와 histogram의 공유 full hunk 기준, R2는 +10/-11도 별도다. R4 공개 기대는 Breezy의 원래 0-based 매칭 쌍이다. C1–C4는 기존 공개 expected가 없다.
- C1에서 Git patience의 common-only/no-unique fallback, histogram의 선택 후보·연속 길이, Breezy의 양끝·무매칭은 내부 관측과 최종 편집을 분리한다. Myers tie는 210 미확인이다. C2에서는 A(1,2) 또는 B(2,1) 중 선택과 후보 순회 방향을 직접 확인한다. 최소 길이 또는 개수 적중만으로 특정 증인에 점수를 주지 않는다.
- Git의 root 후보·선택, compaction 전·후 보존 좌표와 사용자가 본 hunk를 구분한다. Breezy의 root `unique_lcs_py`, 재귀적 매치, 표시를 구분한다. Git trace는 순정 빌드를 대체하지 않는다. 진단 전후 stdout 값이 다르면 그 조건의 trace 해석을 보류하고 측정 차이를 남긴다.
- 가능한 반례를 우선 확인한다. 같은 길이·다른 증인(C2), 같은 출력·다른 내부 처리(C1 등), 같은 앵커·다른 context(C4 등), 방향 변경으로 다른 중복 선택(C3 가설), 최소 편집과 유일 앵커 우선 충돌(보강). 차이가 없으면 0과 조건을 적고 더 강한 반례를 따로 찾는다.
- 직접 원자료 하한은 22건이며 210의 입력/예측/범위/대조 4, Git 7, Breezy 5, 원리·타 분야 3, 표시·경쟁 구현 3이다. 독립 저작과 공동 계보·공유 fixture를 구분한다. 시험 스크립트 wrapper와 실제 기대 데이터를 구별하고 같은 원문 링크를 중복 산입하지 않는다. 직접 실패 로그와 대체 원출전도 원장에 기록한다.
- C1/C2 분기·선택이나 기본 시행을 복원하지 못하면 해당 판정을 PARTIAL로 남긴다. 역사적 채택의 인과, 원전의 독립 예측 증가분, 인간 가독성 우위, 성능/merge 품질은 이 검증의 평가 대상 밖이다.

## 관측 중 명확해진 표시 규칙

순정 64자리는 위 사전 기준 그대로 실행했다. 분석 시 의미 hunk는 0-based 시작 오프셋과 길이, 정확한 본문으로 정규화한다. 길이가 0이면 Git은 앞줄 번호를 출력하고 Breezy 0.2.13은 내부 시작 오프셋+1을 출력한다. section label과 파일 헤더는 원바이트 비교에서 보존한다. 이 규칙은 양 출력의 적용 호환을 단정하지 않는다. [Breezy 출력](https://github.com/breezy-team/patiencediff/blob/834fad2d280fa0634d00d658c61c15d82031f519/patiencediff/__init__.py#L81-L98) · [CPython 형식 시험](https://github.com/python/cpython/blob/2abcf904b8dac8c999d2b3aac76681abb333798a/Lib/test/test_difflib.py#L297-L312)

추가 대조는 W1, CE3/4/6/7, C1/C2 경쟁 matcher, R1 -U0을 총 22자리로 분리했다. 원전과 독립 DP 증인 대조는 별도 한 실행의 여러 예다. 진단 144자리와 별도 재생의 범위는 [SELF_CHECK.md](SELF_CHECK.md)에 있다.
