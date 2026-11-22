REVIEW_READY_WITH_GAPS

# AF-RES-021 인계

## 1. 상태와 핵심 결과

고정 후보 45행을 공개 질문 12개에서 만들었다. pytest, CMake, HTTPX 각 4개이며 전체 선택과 특정 기능 각각 6개다. A/P/M별 판독 135행과 1·2·4절의 두 판정원 집계가 재현된다. 고유 원문 46개를 산입했다. 공개 질문 12, 버전별 공급자 원문 26, 의학 3과 법령 5다. 출처 모두의 날짜·판·정확한 위치·확인 범위는 [자료 원장](sources.json)에 있다.

| 2절 기준 | A | P | M |
| --- | ---: | ---: | ---: |
| 공식 지지와 근거를 함께 회수 | 6/23 | 9/23 | 14/23 |
| 실제 답의 지지와 근거를 함께 회수 | 1/11 | 3/11 | 5/11 |
| 공식 자연 근접 오승인 | 4/14 | 3/14 | 3/14 |
| 공식 지지 행의 근거 도달 | 8/23 | 12/23 | 22/23 |
| 읽은 절/공식 회수 | 88/6 | 88/9 | 88/14 |

M−P의 짧은 예산 이득은 위치 효과에 추가된다. 2절의 공식 질문별 승/무/패는 5/7/0이다. 같은 오승인 총수에서 Q04c가 새로 오승인됐고 Q07d는 충돌로 돌아왔다. 4절의 추가 회수는 공식·실제 답 모두 +1행이며 Q08에 집중됐다. 간선 제거로 45/45행의 M 결과가 P에 수렴했다. 오연결 진단의 공식 2절은 M 8/23으로 P 9/23보다 낮았다. 조건 연결은 이 자료·공통 규칙에서는 특히 짧은 예산에서 유망하다. 사람의 검토 시간·편집자 분리 후 효과·재사용 손익은 아직 관측하지 못했다. [결과](RESULT.md) · [지표](metrics.csv) · [진단](evidence/diagnostics.json)

## 2. 입력, 실행 위치, 원격 확인

| 항목 | 확인 위치 |
| --- | --- |
| 저장소와 작업 브랜치 | `laadkke-arch/agentflow-open` / `work/research-af-res-021`, 쓰기 `docs/workstreams/research/AF-RES-021/` |
| 배정 시 최신 통합 SHA | `2337537f9496cb4175656b019a8c636e5a03d1bc`. 계약 시작 때의 통합 `435a5099a0abb0bb4b3c08d40401d0e304e82153`와 계약 해시가 일치한다. |
| 계획과 고정 의존 | `b507fbcab09724a77270e658355f4b661cc35f02`, AF-RES-020 `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35` HANDOFF 및 C-B07-04·C0/C2·D01/D10. [범위](SCOPE.md) · [계약 manifest](manifest.json) |
| 실제 환경 | Dot 위임의 Codex 공유 Linux x86-64 `/workspace/scratch/af-res-021`, Python 3.12.14. 편집 Codex/GPT-6 계열, 세부 표시 모델 미확인. 판독은 시드 210922의 Python 규칙. |
| 룰·묶음별 저장 | 사전 동결 `44845201e966cc551cb8cd10e9ec56969197bbaa`. 각 입력·로그의 SHA는 [진행표](PROGRESS.md)에 있다. |
| 전체 판독 및 키 공개 | 로그 봉인 `400da5d787a86b8ed58447f892416e6d9916770a` 다음에 채점기가 키를 읽었다. [실행 전 해시와 채점](evidence/score-receipt.json) |
| 결과와 자기 점검 | 결과 검사 `4b384be7dafb6bee975f532b0a17f9b5769d74ff`. 자기 점검 커밋 `f93439d81f698dc0027b17badbf171411016b7e4`의 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/f93439d81f698dc0027b17badbf171411016b7e4/docs/workstreams/research/AF-RES-021/RESULT.md), [자기 점검](SELF_CHECK.md), [수용 배열](evidence/acceptance-evidence.json)을 원격에서 읽었다. |
| 현재 인계 커밋 확인 | 브랜치에서 `git log -1 -- docs/workstreams/research/AF-RES-021/HANDOFF.md`. 인계 직전 원격 개별 계약 검사 종료 0. |

## 3. 검증과 재생

신규 캐시에서 공급자 파일 38개를 내려받아 SHA-256을 대조했다. 질문·카드, 기본 135행 로그와 세 진단 로그의 바이트 또는 SHA가 일치했다. 1,560 CSV 행과 표 1–4, RESULT 마지막 표의 3개 데이터 행을 확인했다. 개별 `workbench.session check --fetch`가 인계 직전 점검 SHA에서 통과했다. 공통 `cloud_check --fetch-contract --require-clean`은 결과 SHA에서 종료 0이었다. 공통 검사 내 전역 manifest 탐색은 `no_active_sessions`였고 개별 검사를 분리 확인했다. [검증 영수증](evidence/verification.json)

저장소 루트, Python 3.12, 영어 원본을 읽을 수 있는 GitHub raw 네트워크에서 다음 명령으로 재생한다. 키를 복사하지 않은 `blind`에 카드 입력을 만들고 검증기가 기본·진단 실행을 먼저 재생한 뒤 채점한다. 네트워크 제한 시 `evidence/documents.json`의 고정 `raw_url` 바이트를 파일명 `id`로 캐시에 공급한다.

```sh
study=docs/workstreams/research/AF-RES-021
scratch=$(mktemp -d)
python -I "$study/replay.py" index --cache "$scratch/raw" --stage "$scratch/blind"
python -I "$study/replay.py" build --stage "$scratch/blind" --receipt "$scratch/prepared.json"
python -I "$study/evidence/verify.py" --stage "$scratch/blind" --scratch "$scratch/out"
python -m workbench.session check "$study/manifest.json" --fetch
```

재생 입력은 [판본 원장](evidence/documents.json), [질문](cases.jsonl), [카드 계획](evidence/card-plan.jsonl)이며 별도 집계에서 [정답 두 종류](keys.jsonl)를 쓴다. 판독기는 실제 답, 공급자 정답, 자료 원장에는 접근하지 않았다. 편집자는 동일 공개 답과 공급자 파일을 알아 위치 선택의 편향이 남는다.

## 4. 수용 공백과 다음 첫 행동

수용 근거는 12/16 충족이다. 공개 질문 12건을 열었고, 공개 편집 필드를 직접 확인한 GitHub issue 1건, 편집 표시가 보이지 않았던 Discussions 7건, 공개 수정 원판이 열리지 않은 CMake 4건으로 남았다. 블라인드 판독은 원 질문 전문 대신 원문 발췌와 요구를 받았다. 자연 오답은 작업 분류 14행이나 당시 초기 명시를 보수적으로 요구하면 11행이다. 세부 표시 모델도 미확인이다. [판정 배열](evidence/acceptance-evidence.json)

다음 담당의 첫 행동은 위 원격 커밋의 수용 배열을 열고 CMake #1264·1978·6510·9029의 첫 게시 revision과 최초 답 시각을 확보하는 것이다. 공개 읽기 전용 HTML에서는 본문·후속은 읽혔다. 확인 가능한 첫 입력은 서버에서 보존한 게시 #1의 번호·revision과 차이 또는 답 이전에 저장된 날짜 있는 스냅샷이다. GitHub Discussions에서도 수정 시각/이력을 확인하는 공개 자료를 찾아 현재 본문과 대조한다. 원판이 확인되면 제목·본문 전체를 키 없는 입력에 넣고 기존 발췌 기반 로그를 보존한 채 새 시험을 구분한다. 그 전에 미확인 원판을 정답으로 바꾸지 않는다.

색인 제안은 `AF-RES-021 · 고정 후보/같은 읽기 예산의 위치 및 조건 대응 · REVIEW_READY_WITH_GAPS · RESULT.md` 한 행이다. 의존은 AF-RES-020의 제안 사용·근거 판정 축이며 범위는 H1의 후보 확인 단계다. 진행 담당은 바로 위 네 공백을 넘겨 수용을 보류할 수 있다.

## 5. 중요한 약점 세 가지와 다음 조사

| 약점 | 다음 조사와 최소 입력 |
| --- | --- |
| 원 질문 수정 이력과 전문이 없으면 어떤 문장이 답 이전의 필수였는지 달라질 수 있다. | CMake 네 게시의 첫 revision, GitHub 공개 편집판과 첫 답 시각을 복구한다. 전문 투입 재생에는 original raw 필드와 고정 해시를 추가하고 엄격 자연 근접 오답 1행 이상을 사전 표집한다. |
| 올바른 절을 찾아도 Q04c의 동기 조건, Q06b의 표준 범위처럼 판독 술어의 대상이 어긋난다. | 새 12질문에 버전·호출 종류·최소/정확 모드 대조를 포함하고 별도 검토자 두 명이 용도와 조건 주체, 모순의 정확한 절을 봉인한다. 단계별 도달과 오승인을 기록한다. |
| 답을 읽은 한 편집자의 대응과 도구 시간만 관측했다. Q09b는 일부 오연결이 P보다 불리함을 보여준다. | 새 문서에서 키를 보지 않은 편집자 두 명, 여러 판독자, 공통 1·2·4절 예산을 사용한다. 작성·재검 시간과 처음/반복 사용의 회수를 분리하고 오연결 발생과 복구 비용을 기록한다. |
