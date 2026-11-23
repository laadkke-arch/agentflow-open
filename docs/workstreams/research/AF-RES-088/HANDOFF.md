# AF-RES-088 인계

**PARTIAL · 시도 2 · 결과 묶음 원격 커밋 및 검사 완료.** 고정된 첫 보존 공개판과 30일 내 마지막 본문판을 8질문·64행·32쌍으로 비교했다. 확정 문서 적합성 비교26쌍에서 판정 변화는0/26이고, JN1/map의 다음 확인 입력은1/32쌍에서 바뀌었다. 나머지6쌍은 미확인이다. PE1의 옛 이미지와 여섯 Pandoc 구현·입력·출력 근거가 빠져 REVIEW_READY로 올리지 않는다. [필수 세 표와 분모](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/RESULT.md)

작업 브랜치는 `work/research-af-res-088`, 소유 경로는 `docs/workstreams/research/AF-RES-088/`다. 이번 재개에서는 원격 `f048885abfbfcca1ffd8840899bf2911cd35da60`부터 이어졌으며 기존 커밋을 초기화하거나 덮어쓰지 않았다. `dot-control.json`과 다른 과제 경로는 수정하지 않았다.

## 결과와 고정 이력

| 묶음 | 원격 커밋 | 내용 |
| --- | --- | --- |
| ① | `9f8a8f5c0d4ac9f8659374d99e71f3d7a1013712` | 모집·판선택·단일 후보 계약, jq1.7.1/Pandoc3.1.11의 SHA·절 |
| ② | `42e46d5788278efa8d5b8ab0272ace48830fb477` | 시간/ID순 원60목록,8자리, R0 요구와32판정 봉인 |
| ③ | `f048885abfbfcca1ffd8840899bf2911cd35da60` | R1 판독,64행·32쌍, 사후답 열람 전 비교 |
| ④ | [`e173b53f071aabfa749d33ab7da7ce970d5641b5`](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/RESULT.md) | 사후11답·17댓글, 타분야 판쌍, 세 표·분모·자가검산·재현·재개 정정 |
| ⑤ | 이 파일만 추가하는 마지막 단독 커밋 | 검사 대상·실시/미실시·원격 재열람·다음 첫 행동 |

결과 tree는 `c9de7c7058e27b13c594eddc61abe70993e388db`다. GitHub Git objects로 만든 tree가 로컬 index와 정확히 일치한 뒤 부모 f048885에 커밋했다. branch ref는 기대 HEAD를 조건으로 정상 전진시켰고, 원격 fetch 후 로컬도 fast-forward했다.

계획 기준은 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`, 실제 시작/기존 manifest 기준은 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`다. 계획판에 아직088행이 없고 실제 시작판에 배정 행이 있는 차이는 `support/resume/intake_resume.json`에 남겼다. 유일한 선행 연구 AF-RES-084는 `5705a5a00f07af0f0048237cfa9ba6673fd3e91d`의 HANDOFF/events/cells/pairs/metrics/RESULT를 인수했다. 그 연구의 개설본문0/4·엄격0/16·최초확보본10/16과 옛 모집분모는 이번 자료로 채우지 않았다.

## 주요 관측과 재개 정정

- 모집은 jq30·pandoc30, 적격60, 선택8, 결원0이다. 자연층4와 편집층4를 분리한다. 자연층 본문변화1/4·명시조건변화0/4이며 편집층4/4 본문변화는 선정조건이다.
- 확정26쌍의 구성은 충족1·명시반박8·범위밖17이다. 25음성쌍과 같은 질문 내 상관 때문에0/26을 검색품질·일반 수정효과의 안정성으로 해석하지 않는다.
- 출처기록244행 가운데 중복/댓글/반복재열람 등을 제외한 직접 원자료120개, 독립 저작·사건87개다. 선정SO8사건, CLI12자료/9저작, 플랫폼17자료/8사건, IETF2판쌍·학술2판쌍의 원판·다음판·후속인용을 포함한다.
- 현재채택3/8이며 주된 채택해법은 풀밖3/3이다. 질문자 정확 사용판 자기보고1/8, 완전성공0/8, 같은 성공실행의 정확판 확인0/8이다. 엄격 최초게시 바이트도0/8이다. 엄격비교와 인과적 도움/시간절감의0/0은 산출 불가다.
- 읽은 최초답11개의 구체출력 텍스트3개와 별도 서술상 결과보고1개를 나눠 합집합4/11로 정리했다. PN1 답78261053의 작동·한계 보고를 놓친 초안 분류를 바로잡았다.
- JE1 답78299501의 두 식은 별도 jq1.7에서 각각seq_num=[1,1]과[1,2], 종료0을 냈다. 게시 출력은 첫 식과 일치한다. 초안의 출력불일치 주장을 철회했다. 이는 고정jq1.7.1 실험, 실제 LangChain Document 실행, 원 질문자 성공으로 세지 않는다.
- PE1 추가 default.latex URL에 대응하는 자료ID는 MAN-10이다. 일부 봉인행의 MAN-06(HTML5) 연결을 후속 `evidence_corrections.jsonl`과 표2 주석으로 정정했다. 원래64판정 CSV의 바이트는 f048885와 동일하다.

주파일은 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/RESULT.md), [metrics](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/metrics.json), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/SELF_CHECK.md), [reproduce](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/reproduce.md), [판정64행](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/judgments.csv), [32쌍](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/pairs.csv), [출처원장](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/sources.jsonl), [실행 인계](https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/execution/README.md)다. 같은 팀의 세 재개 감사는 `support/resume/` 아래에 있으며 독립 맹검판독/독립 평가자 일치도로 세지 않는다.

## 실제 검사와 종료값

결과 커밋 `e173b53f071aabfa749d33ab7da7ce970d5641b5`의 깨끗한 작업 트리에서 소유 경로 manifest를 명시해 검사했다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-088/manifest.json --fetch
```

```json
{
  "status": "passed",
  "task_id": "af-res-088",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T15:47:36.720142+00:00",
  "checked_out_commit": "e173b53f071aabfa749d33ab7da7ce970d5641b5",
  "task_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "integration_commit": "4eaab7a4ba954026026d2fce59982114f61acbf9",
  "scope_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_path_count": 231,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "exit_code": 0
}
```

| 검사 | 대상·관측 | 종료값 |
| --- | --- | --- |
| workbench.session check --fetch | 결과SHA e173b53; passed/remote_checked; 계약동일; 범위이탈0·충돌0·오류0 | 0 |
| recalculate.py --check | 결과SHA e173b53에서 재실행;60프레임·8사례·64행·32쌍·26확정·6미확인, 후보계약/R0 불변 | 0 |
| execution/extract_inputs.py --check | 결과SHA e173b53에서 재실행;37추출물+인덱스38파일 일치 | 0 |
| audit_revision_integrity.py | 결과 묶음 입력;129리비전·111본문·51/51 last_body,8선정 및 R0/R1 지문 | 0 |
| audit_outcome_integrity.py | 결과 묶음 입력;8질문·11답·13답리비전·17댓글, 시간/부모/채택 연결 | 0 |
| resume outcomes metadata audit | 공식API 재조회11회 모두200/has_more=false;75검사 | 0 |
| 정확판 변환 gate | 설치 jq1.7/Pandoc3.1.11.1은 고정1.7.1/3.1.11과 다름; 고정판 변환0건 | 2 |
| JE1 사후답 variant1/2 보조실행 | 별도 jq1.7, 동일 원JSON, seq_num=[1,1]/[1,2]; 고정판/질문자실행 아님 | 각0 |
| git diff --cached --check | 원추출8파일의 공백12진단을 지문보존 때문에 유지; 작성문서 불필요한 빈 줄은 수정 | 2, 원인 기록 |
| 공백진단 경로·추출물 검산 | 모든 잔여진단은 execution/inputs 원추출물; 별도 일반저작물 진단 없음 | 0 |

검사 stdout/stderr와 입력 지문은 `support/resume/validation.json`, 공백진단 전체는 `support/resume/staged_whitespace.json`에 있다. 위 표의 메타데이터 감사는 의미판정을 자동 증명하지 않는다. 마지막 인계 문서 자체는 앞서 검사한 결과 커밋에 포함되지 않는다. 저장소 전체 제품시험·고정판 Pandoc 변환·원 사용자 실행·검색 순위/탐색시간/인과효과는 미실시 또는 미측정이다.

## 고정 결과의 원격 재열람

2026-11-23T15:48:44.115190Z 완료 체크포인트에 정확 결과SHA의 아래7파일을 GitHub에서 다시 읽고 반환 blob SHA를 로컬 파일과 대조했다. 모두 일치했고 작업트리는 깨끗했다. RESULT SHA-256은 `de1d331f75b90d70784e9e82a78e9e3be3988fd332f4114c33f858b3f3447088`이다.

| 파일 | 원격·로컬 blob SHA | 대조 |
| --- | --- | --- |
| PROGRESS.md | `d79189fb4068c90310ca3266441c8892fb6c8744` | 일치 |
| RESULT.md | `04c8114d10dfd8de1e6b40cd94227e94b714182d` | 일치 |
| metrics.json | `59f1b3e3f3def977a92b516d1d41a624ea7b4396` | 일치 |
| SELF_CHECK.md | `cfcffbd1e5b85d22de00d6ab8ba343b0adae386e` | 일치 |
| reproduce.md | `073515aed980e44cf57ae2fc659e0d3da22ed383` | 일치 |
| judgments.csv | `3f8fce3704bf86df76bac67e9eb4ecda343c3c45` | 일치 |
| manifest.json | `e7acc766d98b7085cfded75fb612bc42e1f0174e` | 일치 |

## 다음 첫 행동과 실행할 입력

**PE1의 R0/중간/R1 이미지와 전체 Markdown을 먼저 확보한다.** 대상은 SO78300525의 R0 GUID `DAD692BA-D95F-4262-8B83-C762CF15C4A9`, R1 GUID `06E686FC-FB2D-4E3B-836C-7CA2CF31DB4E`, 이미지 `A0Wtm.png`·`yQDJv.jpg`·`avk9k.png`다. 알려진 원 호스트 요청은403/1010 또는 웹 접근불가였으며 실패·시각은 `support/resume/gap_audit/attempts.jsonl`에 있다. 차단 우회는 하지 않았다. 합법적으로 보존된 이미지 바이트·당시 시점·SHA를 얻지 못하면 전체 시각비교를 unknown으로 유지한다.

여섯 미확인 쌍에는 각각 handler/template·원입력·AST·writer/확인된PDF엔진·출력이 필요하다. 최소입력과 개별명령은 `execution/README.md`에 있다. 정확판 바이너리를 이미 확보한 환경에서 다음을 실행한다. 자리표시자는 실제 확인한 절대경로로 바꾼다.

```bash
cd docs/workstreams/research/AF-RES-088
export AF088_JQ_BIN=/absolute/path/to/jq-1.7.1
export AF088_PANDOC_BIN=/absolute/path/to/pandoc-3.1.11
python -B execution/reproduce.py --preflight
python -B execution/reproduce.py --run-jn1
```

첫 gate 성공 뒤의 JN1 R1 기대값은 rain=[2,1,7,6,9], grass=[12,12,13,29,69]이며 아직 고정판 관측값이 아니다. 이것만 실행해도 R0의 전체입력·PE1 이미지·원 질문자 실사용판 결손은 그대로다. PDF실험은 실제 엔진을 확인하고 `AF088_PDF_ENGINE`을 export한 뒤 README의 해당 명령을 사용한다. 없는 원입력/handler를 있다고 보고 실행하지 않는다.

## 중앙 색인에 반영할 한 줄

AF-RES-088 · PARTIAL · SO jq/Pandoc8질문·64행·32쌍, 확정26쌍 판정변화0/26·다음질문변화1/32·미확인6, 원자료120/독립87, 엄격최초게시0/8·정확성공판0/8 · 결과 e173b53f071aabfa749d33ab7da7ce970d5641b5 · PE1보존이미지/6구현근거 확보 후 재개; 인계는 이 파일의 마지막 단독커밋.

## 가장 중요한 약점과 판단을 바꿀 관측 — 정확히 3건

1. **즉시 게시 바이트와 PE1 옛 그림이 없다.** 다음 대상은 선택8의 동시대 HTML/Markdown과 PE1의 세 이미지다. 입력은 원URL·GUID·시점·실제바이트·SHA이고, 옛 그림에만 있는 조건 또는 첫 게시와 R0의 바이트 차이가 관측되면 원판/전체의미 판정을 바꾼다.
2. **좁은 후보풀의 음성25쌍·구현 미확인6쌍과 같은 독자의 기억효과가 남는다.** 다음 대상은 여섯 Pandoc 경로의 정확판 입력/handler/template/AST/엔진과 별도 독자의 가린 요구 판독이다. C1/C2를 충족하거나 직접 실패하는 출력, 또는 재현되는 판독 불일치가 판단을 바꾼다. 입력·후보 범위 확장은 별도 분석으로 남긴다.
3. **채택표지만으로 최종 목적 충족과 원 사용판을 확인할 수 없다.** 다음 대상은 JN1 Bash배열 소비, PN1 향후grid-table 사용 등의 원 질문자 공개후속이다. 동일입력·완전명령·정확버전·시각·출력의 사슬이 확보돼야 현재 성공+정확판0/8을 갱신한다. 도움·시간절감은 별도 비교관측이 필요하다.
