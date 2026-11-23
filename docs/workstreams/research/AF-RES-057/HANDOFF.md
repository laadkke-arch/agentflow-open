# AF-RES-057 HANDOFF

## 인계 상태와 고정판

- **작업/작업자:** AF-RES-057 / web-pro.
- **조사 상태:** **PARTIAL**. 확보 가능한 독립 조사·예측 봉인·후속 대조·원시험 로컬 확인·저장과 계약 검사는 마쳤다. 원사건·원본·실제판·완전 공개 A/B 출력의 결손을 아래에 남긴다.
- **저장소/브랜치:** `laadkke-arch/agentflow-open` / `work/research-af-res-057`.
- **result_commit:** `5c5b5299ec57eefde78029a23a62cfb48f508469` — 이 인계 직전 고정 결과판. 결과·수용 원장을 이 SHA에서 GitHub로 다시 열어 대조했다.
- **prediction_seal:** `74dc9f887bc47bc0a92b9a75ea327ffa30aca70b`, 서버 커밋 UTC `2026-11-23T03:32:00Z`.
- **실제 시작판:** `chore/workspace-foundation@3f4d43b19cd76d56983e6f500eebe7010eb3fa51`. 계획판 `8036b862a0f921196dca57e8532df606bf6f1de6`와 구별한다.
- **의존 입력:** AF-RES-053 인계 `94231403b7ce6debd1ee7bb1a34e86e3956c7920`; 결과 `87a375d72c269f921589e98b27265e344a70000d`. control DONE과 그 인계의 부분/BLOCKED 판정은 구별해 인수했다.
- **소유 경로:** `docs/workstreams/research/AF-RES-057/`만 변경. `dot-control.json`은 수정하지 않았다.
- **인계 작성 UTC:** 2026-11-23T04:04:37.057180+00:00. 최종 고정판 재열람과 실제 session check가 끝난 뒤 작성했다. 이 파일만 마지막 단독 커밋으로 올린다. 마지막 커밋 자체의 SHA/시각은 Git 메타데이터에서 확인한다.

**파일 저장 성공과 연구 완전 충족은 별개다.** 현재 PARTIAL의 이유는 도구 실행 차단이 아니라 회복하지 못한 원자료와 비교 단위의 한계다. 이 상태를 완료된 독립 정확도 실험으로 승격하지 않는다.

## 결과 위치와 핵심 판정

[고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/RESULT.md)의 **첫 표는 1~20행(18자료행), 둘째 표는 22~29행(6자료행)**이다. 맨 끝 약점 표는 정확히3자료행이다. Q1~Q7의 근거·반례·설계 대안·사용/중단 조건은 그 사이에 있다. [고정 수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/evidence/acceptance-evidence.json)은28조건을 별도 분자·분모·단위·결손으로 기록한다.

**같은 분야 E와 외부 원전 D의 사전 선택·undo/redo·정상/경계 상태 예측은6/6자리에서 같다.** 상이 예측은 관측0/6이다. 따라서 E보류→D정답, E오답→D정답, D새오답의 조건부 비율은 **분모0으로 해당 없음**이다. 정확률0%나 D의 무용성을 뜻하지 않는다. 공통 API가 이미 가르는 경우가 있었고, 원장의 보류는 결과를 보고 맞힌 예측으로 바꾸지 않았다. [봉인 예측](predictions.csv), [계수](evidence/comparison-counts.json).

구현 선택에는 해당 판의 원점 필터·그룹 경계·마지막 input rule 조건 또는 실제 mapping 수정 링크를 반환한다. 지도·회계 원전은 보이는 문자, 뒤 작성자의 변경, 원기록, 정정 효과, 다음 undo/redo 중 무엇을 보존할지 묻는 참고로 제한한다. 이 질문의 실제 유용성이나 사람의 읽기 시간은 측정하지 않았다. [사례별 반환 링크](return-cards.md).

| 자리 | 확인한 결과와 반례 | 해석 한계 |
| --- | --- | --- |
| YN1 | 보호 origin 제외 시 정상 undo에 보호 문구가 남는다. 사건 역순에서는 첫 텍스트가 같아도 남은 undo 깊이는0/1로 다르다. 같은 null 원점이면 작성자 이름만으로 보호되지 않는다. | 13.0.0-94 보조판·연구 보충 사건열. 원작성자 설치판/초기값 미확인. |
| YN2 | gc=true 삭제 undo는 `123 World`, gc=false는 `Hello123 World`; 둘의 redo는 `123 World`. | 모든 보기의 사전 판별 불가 유지. private stack 이동과 원문 근사 공백은 공개 계약/새 적중이 아니다. |
| YT1 | 13.6.28 원 opA 기대 `[1,2,3]`를 읽고 원실행기에서도 확인. 연구 opB는 `[]`, redo 둘 다 `[1,2,3,4,5,6]`. 13.0.8 감도에서는 둘 다 `[]`. | 원군에 B/redo 없음. 구판 반례는 사후이며 주 분모에서 제외. |
| PN1 | metadata 연구 변형은 원격 R의 유지/삭제를 가르고 역순은 같은 텍스트·다른 남은 이력을 보인다. 실제 #892 수정은 selection rebasing 오류다. | 원문 선택25..30, 후속 작성자 trace6..13, metadata 보조는 다른 입력/조작. 엄격한 명시 남길 텍스트 모집에서는 제외. |
| PN2 | 즉시 undoInputRule은 `...` 복원, 이어 history.redo는 false/dispatch0. 뒤에 x가 있으면 undoInputRule도 false로 `…x` 유지. | redo 일부는 사전 보류. 실제 작성자 브라우저/schema/timing 미확인. |
| PT1 | 원 기본 그룹 undo는 빈 문단이며 원실행기1개 통과. closeHistory 연구 변형은 a를 남긴다. | E에서 의미적 답 선노출. 'a를 남긴다' 목표·B·redo·원격 b는 연구 확장. |

## 실제 분모와 읽은 자료

| 단위 | 실제 |
| --- | --- |
| 자연 모집 본문 | Yjs 첫30 + PM 해당 후보 전부17 =47; PM 부족13순번은 빈 행으로 보존 |
| 연구 자리/보기 | 자연4 + 진단2 =6자리, A/E/D18행. PN1 엄격 텍스트 감도는5자리/15행 |
| 출처 원장 | 132행 =기존130취득+후속 자체 원시험 실행2. 외부 적격112취득을 병합해 **66고유 원저작** |
| 겹치지 않는 최소 배당 | 요청4 / 제품 API·예제4 / 다른 수정6 / 지도·회계 사례4 / 원연구2 =20저작 |
| 지도/회계 사례 정밀도 | 각2사례를 읽었으며4중3은 수치/객체 상태 확인. 나머지1은 수치 원장이 없는 실제 저자 대사 보고 |
| 추가 창 | E/D6쌍 모두18또는22단어·0도판. 코드 행·절단·창밖 노출은 별도 기록 |
| 봉인 연구 실행 | 26변형 완료; 비보류 상태의 일치와 보류를 구별. 독립 새 정답26개라는 뜻이 아님 |
| 사후 감도 | 8레코드; 의도적으로 보존한 구판 RangeError3개 포함 |
| 마지막 원시험 실행기 확인 | **2개 선택·2개 통과**. 원소스/원 helper의 opA 시험만, 로컬·사후 확인 |
| 원진단 기대값 |2/2 직접 열람; 의미적 답 미노출 조건을 유지한 것은YT1의1/2 |
| 원사건 완전 공개 A/B·redo 연결 | **0/6 확보**, 실패율이 아니라 미확인 자료 연결의 수 |
| 정확 SHA 공개CI 통과 증거 | 확보0; 조회 결과 없음과 테스트 실패/실제 실행 중은 구별 |

계보는 같은 issue/patch/test/CI와 개정·미러를 합쳤다. PM #892 요청과 수정은 같은 저작이므로20개 배당의 수정 여섯 건에는 다시 넣지 않았다. 기록132행과66저작, 자료 수와6자리 검증 수는 서로 다른 분모다. [출처](sources.jsonl), [최종 계수](evidence/final-counts.json), [별도 계보 감사](streams/donors/final-source-audit.json).

지도 반례는 무제한 '뒤 편집 보존'을 입증하지 않는다. Casablanca의 나중 name:fr는 원 문제 작성자의 변경이며, 다른 사람의 독립 새 기여로 오인하지 않았다. Payap의295 ID 목록 일치는295개 객체 상태 검증이 아니다. 회계 역분개는 원기록이 남아도 연결 필드가 바뀔 수 있고, 잔액 회복과 대사 상태는 다르다. [donor 분석](streams/donors/donor-analysis.md), [자체 반증 점검](SELF_CHECK.md).

## 실행과 검사: 실제 관측 범위

연구 주체는 root 및 같은 모델의 Yjs/ProseMirror/donor 분담자다. 원자료별 실제 독해 위치·시각·독해 주체는 sources.jsonl에 있다. root 단독66저작 독해, 독립 인간 평가 또는 외부 전문가 검토라고 주장하지 않는다. 각 분담자의 최종 검토와 root의 반영 범위는 [root 검토](evidence/root-final-review.json) 및 각 stream의 final-review.md에 남겼다.

- 원격 예측 봉인03:32:00Z 뒤에만 보류 assertion을 열었다. 첫 PM03:32:31.973Z / Yjs03:32:32.205236Z. PT1의 E 의미 노출은 이 시간 순서로 지워지지 않는다.
- Yjs npm3판/PM5package의 gitHead와 설치 source bytes를 고정 GitHub source와 대조했다. 현대 Node24.22.3/npm11.19.1을 썼다. 주 재생의 전이 의존성을 역사 CI라고 부르지 않는다.
- 최종 Yjs 원시험은 원 lock(lib0 0.2.99, y-protocols1.0.6)과 원3클라이언트 fixture로 실행했다. 등록206 중 **1개만** 선택했다. PM은 원1.5.0 source/test와 원 helper/schema/assertion을 쓰되 명시한 현대 buildhelper/core로1개만 선택했다. 두 실행 모두 공개CI·원작성자 실행·새 예측 적중이 아니다.
- 구조·분모·출처 ID/참조·단어수·10봉인 hash·표18/6/3·Q·로컬 링크·선택 원시험 기록 검사는 **41/41통과**다. [audit-final](evidence/audit-final.json). 의미 검토나 연구 완전 충족을 자동 보증하지 않는다.
- 1차 session check는 결과표 커밋 `b17ef54bf5e460cb2a7157a12f571a8356fb0a78`에서 실제 종료0/passed였다. [원문 영수증](evidence/session-check-stage4.json).
- 영수증을 포함한 최종 result SHA `5c5b5299ec57eefde78029a23a62cfb48f508469`에서 RESULT·acceptance를 GitHub로 다시 열어 blob 일치를 확인했고, 같은 명령을 다시 실행해 **종료0/passed**를 얻었다. 시작 `2026-11-23T04:01:54.057044+00:00`, 종료 `2026-11-23T04:02:00.575954+00:00`. 외부 경로 변경·미병합 경로·오류는 모두0이다. 당시 integration 최신판은 `5ede35a58c3c7faabcf4a971a8f2c499ed872096`, 시작판은3f4d43…로 그대로 기록된다. 계약 hash는 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`로 일치했다.

최종 재열람의 RESULT blob은 `ce2f056ccf855f96fbb296c9918be6983b827816`, acceptance blob은 `55ffa495c1f960275a50f830263a9ace7f3338da`다. 아래 부록은 그 재열람 영수증과 최종 check의 전체 stdout이다. 앞선 acceptance의 고정판 검사 항목은 이미 검증한 b17e…를 가리키며, 이 인계가 receipt-inclusive 최종5c5b… 검사를 추가한다.

## 부분 상태의 이유·다음 첫 행동

**재개 첫 행동:** YN1 #157의 **원작성자 실제 설치판·초기 문서·일반 편집과 보호 편집의 완전 사건열**을 공공 재현 입력/아카이브에서 확보해 현재 회복 본문과 대조한다. 없으면 그 결손을 유지한다. 현재의 alpha 보조 사례를 원사건으로 바꾸거나 더 늦은 이슈를 소급 선정하지 않는다. 자료 없이 같은 재실행을 반복해도 이 결손은 해결되지 않는다.

| 미충족/미확인 | 시도한 경로와 현재 한계 | 결론을 바꿀 최소 입력/다음 행동 |
| --- | --- | --- |
| 최초 authored body4건, 자연3건의 실제 설치판 | GitHub의 공개 본문·생성/갱신 메타데이터·후속 댓글·태그·API·연결 재현/수정 기록을 조사. updated_at은 본문 수정 증거가 아니며 최초 revision을 모두 복원하지 못함 | dated 최초 body/edit archive와 author lock. PN1은 원25..30 trace가 필요; PN2는 schema/input rule/IME/timing 필요 |
| 동일 원입력·원판·두 조작·redo의 공개 출력 | 원진단 assertion, 연결 수정 diff, 작성자 후속, 정확SHA statuses/check-runs/actions 조회. 주26연구·사후8·원시험2로 별도 확인했지만 원 공개 완전쌍은 없음 | 같은 actor/입력/판/opA/B/redo를 담은 공개 fixture와 raw 출력. 나중 생성한 연구 fixture를 기존 원시험이라고 부르지 않음 |
| 외부 D의 추가 예측 정확도 | 봉인 E/D6/6동일. 짧은18/22단어 창·같은 모델·창밖 지식·일부 선노출 | 새로운 입력과 더 풍부한 donor 창을 평가하려면 **새 프로토콜에서 사전 고정**. 다른 사전 예측과 이를 가르는 미노출 출력이 함께 있어야 조건부 추가 적중을 셈 |
| 회계 두 번째 사례의 수치 원장 | 실제2017대사 보고를 직접 읽었으나 버전·날짜별 split·대사표 수치가 없음 | 그 원장의 익명화된 실제 거래/역분개·날짜·대사 상태. 일반 매뉴얼 수치로 대신하지 않음 |

## 재현 명령과 필요한 입력

저장소 루트, Python3.12+, Node/npm, 공개 GitHub/npm 접근이 전제다. 모든 복원 캐시는 이 작업의 owned path 안에 생성한다. **아래 복원 스크립트의 미래 재실행을 이번에 추가로 수행했다고 주장하지 않는다.** 실제 실행 command/UTC/출력은 각 receipt에 보존했다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-057/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-057/audit.py --phase final
python -B docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.py --install
python -B docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.py --install --include-posthoc-sensitivity
python -B docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/reproduce.py
python -B docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/reproduce.py
```

Yjs 앞 두 replay 명령은 같은 주14변형을 포함하므로 두 명령을 수행했다고28개의 독립 입력으로 세지 않는다. ProseMirror의 주12+사후2, 역사core 사후4를 재현하는 정확 install/run 명령과 입력 lock은 [PM 재현 절차](streams/prosemirror/replay/reproduce.md)에 있다. 그 run.cjs와 run-historical.cjs의 출력 인자는 재실행 때 새 cache 경로로 지정해 원래 evidence를 덮어쓰지 않는 것이 좋다. Yjs 원시험 필터는 `undoredo: infinite capture timeout$`, seed57; PM 원시험 필터는 `^history enables undo$`다. 새 실행의 환경/명령/출력 SHA를 별도 기록한다.

공개 과거 CI 증거는 로컬 실행으로 만들 수 없다. 재조회할 정확 endpoint/입력 SHA는 [Yjs ci-probes](streams/yjs/ci-probes.json), [PM post-read-receipts](streams/prosemirror/post-read-receipts.json)에 있다. 반환 레코드가 없으면 그대로 미확인이다. 원문 최초판·실제 설치판처럼 명령만으로 복원되지 않는 입력은 위 표의 결손으로 유지한다.

`assemble_preseal.py` 또는 stream의 preseal/case 생성기를 실행해 봉인 파일을 덮어쓰지 않는다. root의10개 봉인 hash와 실제 창/예측은 바꾸지 않는다. 새 분석·새 창·새 사례는 별도 사전 계획과 커밋을 만든다.

## 원격 커밋 이력

| 단계 | 원격 SHA | 서버 커밋 UTC |
| --- | --- | --- |
| ①a 모집·비교 프로토콜 | `55893f8fff261f2a1a043a7df8c146ccf4f49ed8` | 2026-11-23T03:18:52Z |
| ①b 태그·시험 경로·donor 순서 | `80896a0b27323b6b077b21d0686b4b72917da7b9` | 2026-11-23T03:19:26Z |
| ①c 모집·차폐·사전 교정 | `6867acdb5b83e257f0938e31f40d019cbc6a3d29` | 2026-11-23T03:28:32Z |
| ② 사례·조작·카드·18예측 봉인 | `74dc9f887bc47bc0a92b9a75ea327ffa30aca70b` | 2026-11-23T03:32:00Z |
| ③ 보류 출력·후속·재생·반례 | `ed5aeaf1b714dfd5f77ce3051bca0d3db8e0b601` | 2026-11-23T03:47:45Z |
| ④ 두 표·출처·자체 검토·원시험 확인 | `b17ef54bf5e460cb2a7157a12f571a8356fb0a78` | 2026-11-23T03:58:20Z |
| ④ 검증 영수증·최종 결과판 | `5c5b5299ec57eefde78029a23a62cfb48f508469` | 2026-11-23T04:01:08Z |

위 모두 작업 브랜치에 올린 커밋이다. 초기 Git push 인증 실패 후 GitHub connector의 tree/commit/update_ref를 사용하고 실제 remote object를 fetch하여 같은 tree임을 확인했다. 쓰기 범위를 확대하거나 공통 control 파일을 수정하지 않았다. 이 문서는 검사 뒤 작성한 마지막 단독 파일이며, 마지막 커밋이 이 파일만 바꾸는지와 원격 readback/작업트리 상태를 마감 때 다시 확인한다.

## 최종 고정판 재열람 영수증

```json
{
  "result_commit": "5c5b5299ec57eefde78029a23a62cfb48f508469",
  "remote_commit_UTC": "2026-11-23T04:01:08Z",
  "files": [
    {
      "path": "docs/workstreams/research/AF-RES-057/RESULT.md",
      "remote_blob_sha": "ce2f056ccf855f96fbb296c9918be6983b827816",
      "read_UTC": "2026-11-23T04:01:35.939Z",
      "local_blob_sha": "ce2f056ccf855f96fbb296c9918be6983b827816",
      "exact_blob_match": true,
      "sha256": "15a7886085e7db39813c839ed02546f8e80c70e4b45be692b30a6a88653eae7e"
    },
    {
      "path": "docs/workstreams/research/AF-RES-057/evidence/acceptance-evidence.json",
      "remote_blob_sha": "55ffa495c1f960275a50f830263a9ace7f3338da",
      "read_UTC": "2026-11-23T04:01:35.940Z",
      "local_blob_sha": "55ffa495c1f960275a50f830263a9ace7f3338da",
      "exact_blob_match": true,
      "sha256": "eef61be2a2a3e6762a947dda456aadd51a2942bc4a52de1c7d234a5db35156ab"
    }
  ]
}
```

## 최종 계약 검사 원문

실행 주체 root, cwd `/workspace/scratch/9ecab2fc200b/agentflow-open`, command:

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-057/manifest.json --fetch
```

종료 코드0, stderr는 빈 문자열. stdout SHA256 `0f009a08a2b914026f79b5169cb9732424de3d2e60480597e197e73adf9d6c55`. 아래는 `5c5b5299ec57eefde78029a23a62cfb48f508469`에서 반환된 전체 stdout이다.

<details>
<summary>최종 session check 전체 JSON</summary>

```json
{
  "status": "passed",
  "task_id": "af-res-057",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T04:02:00.562564+00:00",
  "checked_out_commit": "5c5b5299ec57eefde78029a23a62cfb48f508469",
  "task_base_commit": "3f4d43b19cd76d56983e6f500eebe7010eb3fa51",
  "integration_commit": "5ede35a58c3c7faabcf4a971a8f2c499ed872096",
  "scope_base_commit": "3f4d43b19cd76d56983e6f500eebe7010eb3fa51",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-057/.gitignore",
    "docs/workstreams/research/AF-RES-057/RESULT.md",
    "docs/workstreams/research/AF-RES-057/SCOPE.md",
    "docs/workstreams/research/AF-RES-057/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-057/assemble_postseal.py",
    "docs/workstreams/research/AF-RES-057/assemble_preseal.py",
    "docs/workstreams/research/AF-RES-057/audit.py",
    "docs/workstreams/research/AF-RES-057/build_acceptance.py",
    "docs/workstreams/research/AF-RES-057/build_report.py",
    "docs/workstreams/research/AF-RES-057/cards.csv",
    "docs/workstreams/research/AF-RES-057/cases.json",
    "docs/workstreams/research/AF-RES-057/events.csv",
    "docs/workstreams/research/AF-RES-057/evidence/acceptance-evidence.json",
    "docs/workstreams/research/AF-RES-057/evidence/audit-final.json",
    "docs/workstreams/research/AF-RES-057/evidence/audit-sealed.json",
    "docs/workstreams/research/AF-RES-057/evidence/card-metadata-corrections.csv",
    "docs/workstreams/research/AF-RES-057/evidence/card-windows.json",
    "docs/workstreams/research/AF-RES-057/evidence/commit-ledger.jsonl",
    "docs/workstreams/research/AF-RES-057/evidence/comparison-counts.json",
    "docs/workstreams/research/AF-RES-057/evidence/comparison-protocol.json",
    "docs/workstreams/research/AF-RES-057/evidence/execution-context.json",
    "docs/workstreams/research/AF-RES-057/evidence/final-counts.json",
    "docs/workstreams/research/AF-RES-057/evidence/fixed-result-verification.json",
    "docs/workstreams/research/AF-RES-057/evidence/governance-read.json",
    "docs/workstreams/research/AF-RES-057/evidence/postseal-amendments.json",
    "docs/workstreams/research/AF-RES-057/evidence/prediction-freeze.json",
    "docs/workstreams/research/AF-RES-057/evidence/root-D-preparation.json",
    "docs/workstreams/research/AF-RES-057/evidence/root-exposure.json",
    "docs/workstreams/research/AF-RES-057/evidence/root-final-review.json",
    "docs/workstreams/research/AF-RES-057/evidence/root-map-recheck.json",
    "docs/workstreams/research/AF-RES-057/evidence/root-source-rechecks.json",
    "docs/workstreams/research/AF-RES-057/evidence/seal-remote-readback.json",
    "docs/workstreams/research/AF-RES-057/evidence/session-check-stage4.json",
    "docs/workstreams/research/AF-RES-057/evidence/upstream-verification-plan.json",
    "docs/workstreams/research/AF-RES-057/frame.csv",
    "docs/workstreams/research/AF-RES-057/observations.csv",
    "docs/workstreams/research/AF-RES-057/predictions.csv",
    "docs/workstreams/research/AF-RES-057/return-cards.md",
    "docs/workstreams/research/AF-RES-057/sources.jsonl",
    "docs/workstreams/research/AF-RES-057/streams/donors/build_ledger.py",
    "docs/workstreams/research/AF-RES-057/streams/donors/donor-analysis.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/final-review.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/final-source-audit.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/final-source-audit.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/map-case-observations.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/method-review.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/payap-case-observations.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/preoutcome-prediction-review.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/preoutcome-review-exposure.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/sealed-ledger-audit.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/sealed-ledger-review.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/selection-log.md",
    "docs/workstreams/research/AF-RES-057/streams/donors/selection-protocol.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/source-counts.json",
    "docs/workstreams/research/AF-RES-057/streams/donors/sources.jsonl",
    "docs/workstreams/research/AF-RES-057/streams/donors/windows.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/E-selection-log.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/api-display.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/body-read-metadata.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/build_cases.py",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/cases.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/fetch-log.jsonl",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/fetch_public.py",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/final-review.md",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/frame.csv",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/guide-historical-pin.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/masking-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/metadata-freeze.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/observations.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/outcome-review.md",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/post-read-receipts.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/recruitment-title-audit.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/recruitment-title-metadata.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/refine_cards.py",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/install-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/install.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/install.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/package-lock.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/package.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/results.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/run-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/run.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/run.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/install-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/install.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/install.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/package-lock.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/package-provenance.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/package.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/reproduce.md",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/results.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run-historical.cjs",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run.cjs",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/source-runtime-check.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/source-counts.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/sources.jsonl",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/stream-validation.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/tag-date-refinement.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/test-input-masked.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/build.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/build.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/buildhelper-0.1.5.metadata.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/buildhelper-0.1.5.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/environment.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/execution-file-hashes.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/execution-receipts.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/install-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/install.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/install.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/metadata-read-receipts.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/original-package.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/package-lock.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/package.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/reproduce.py",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/source-fixture.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/test-builder-1.1.1.metadata.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/test-builder-1.1.1.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/test.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/test.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/verification.json",
    "docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/verification.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/api-read-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/body-read-timestamps.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/build_cases.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/build_postseal.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/build_preseal.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/cases.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/ci-probes.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/diagnostic-before-selection-masked.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/diagnostic-input-masked.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/diagnostic-mask-initial-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/diagnostic-mask-receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/diagnostic-selection-correction.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/final-review.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/frame.csv",
    "docs/workstreams/research/AF-RES-057/streams/yjs/history-commit-metadata.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/mask_test.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/metadata-freeze.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/natural-versions.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/observations.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/outcome-review.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/postseal-first-read.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/postseal-ledger-errata.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/recruitment-review.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN1.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN1.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN1.stdout.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN2.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN2.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YN2.stdout.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1-sensitivity-1308.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1-sensitivity-1308.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1-sensitivity-1308.stdout.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/YT1.stdout.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/dependency-lock-13.0.0-94.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/dependency-lock-13.0.8.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/dependency-lock-13.6.28.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.0-94.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.0-94.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.0-94.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.8.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.8.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.0.8.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.6.28.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.6.28.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/install-13.6.28.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/package-pin-verification.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/replay/sensitivity-plan.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/research_replay.cjs",
    "docs/workstreams/research/AF-RES-057/streams/yjs/sources.jsonl",
    "docs/workstreams/research/AF-RES-057/streams/yjs/title-audit.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/title-frame.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/README.md",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/acquisition.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/install.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/install.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/install.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/reproduce.py",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/run-plan.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/run.receipt.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/run.stderr.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/run.stdout.txt",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/source-integrity.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/upstream-file-pins.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/upstream-package-lock.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/upstream-package.json",
    "docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/verification.json"
  ],
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

</details>
