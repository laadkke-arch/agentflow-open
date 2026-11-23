# AF-RES-088 재집계와 재개 절차

## 고정 입력과 실행 범위

연구 상태는 PARTIAL이다. 아래 검사는 기록의 연결·분모·지문을 재계산하며 원문의 의미를 자동 판독하지 않는다. 고정 모집 60질문, 선택 8자리, R0/R1 64행, 32쌍을 유지한다. AF-RES-084의 분모에 이번 표본을 합치지 않는다.

| 입력 | 기준 |
| --- | --- |
| 계획 | `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd` |
| 실제 시작·manifest 계약 | `9dcae48a47b05d7ba2a1320444be28f5d0fcd739` |
| 유일한 의존 연구 | `work/research-af-res-084=5705a5a00f07af0f0048237cfa9ba6673fd3e91d` |
| 후보 사전 고정 | `9f8a8f5c0d4ac9f8659374d99e71f3d7a1013712` |
| R0 32행 봉인 | `42e46d5788278efa8d5b8ab0272ace48830fb477` |
| R1 64행·32쌍 봉인 | `f048885abfbfcca1ffd8840899bf2911cd35da60` |
| jq / Pandoc 문서판 | `jq-1.7.1@71c2ab509a8628dbbad4bc7b3f98a64aa90d3297` / `3.1.11@c3038dcd54152c4e18e49db31676b79ee7cc29b2` |

실제 실행 결과와 입력 지문은 `support/resume/validation.json` 및 마지막 `HANDOFF.md`에 있다. 마지막 인계에 적힌 검사 대상 SHA가 검사 범위다. 인계 문서 자체를 그보다 앞선 검사에 포함했다고 보지 않는다.

## 기존 자료만으로 재검산

저장소 루트에서 실행한다. Python 표준 라이브러리만 사용한다. `-B`는 소유 경로 밖 캐시 파일 생성을 피한다.

```bash
af088=docs/workstreams/research/AF-RES-088
python -B "$af088/recalculate.py" --check
python -B "$af088/execution/extract_inputs.py" --check
python -B "$af088/support/audit_revision_integrity.py"
python -B "$af088/support/audit_outcome_integrity.py"
git diff --check
git diff --cached --check
```

앞의 두 명령은 읽기 검사다. 뒤의 두 감사 명령은 동일한 로컬 원시 자료에서 `support/*integrity_audit.json`과 `.md`를 다시 쓰고 검사시각을 갱신한다. 새 웹 열람이나 독립 의미 판독으로 세지 않는다. 명시적으로 원자료를 수정하는 작업이 아니라면 `collect.py`, `collect_outcomes.py`, `author_frame.py`, `author_r0.py`, `author_r1.py`, `author_outcomes.py`는 재실행하지 않는다. 네트워크 수집이나 새 읽기 시각이 생기므로 과거 봉인을 재현하는 명령이 아니다.

검토된 출처 원장 또는 사후 분류를 수정했을 때의 생성 순서는 다음과 같다. R0/R1 판정 변경을 허용하는 절차가 아니다.

```bash
python -B "$af088/assemble_sources.py"
python -B "$af088/recalculate.py" --write
python -B "$af088/author_result.py"
python -B "$af088/recalculate.py" --check
```

`assemble_sources.py`는 `support/sources_*.jsonl`을 합친다. 재개 검토의 하위 원장은 `support/sources_resume.jsonl`에 통합되어 있고 모두 반복 열람으로 제외한다. 실패는 `attempts.jsonl`과 `support/resume/*/attempts*.jsonl`에 보존하며 성공 원자료로 올리지 않는다. 기존의 `MAN-06`/default.latex 대응 정정은 `evidence_corrections.jsonl`의 후속 주석이며 봉인 CSV를 덮어쓰지 않는다.

## 모집·판 선택 산식

1. `raw/frame_jq_page1.json`, `raw/frame_pandoc_page1.json`에서 각 태그 생성 UTC·ID 오름차순 첫 30건을 확인한다. 종료값은 2024-07-01 00:00 UTC 미만이다. `raw/*page2_boundary.json`은 30/31번째 동률과 페이지 끝을 보존한다. 태그는 당시 조회 시점의 현재 분류다.
2. `frame.csv`의 적격 순서 첫 2건이 자연층이다. 그 2건을 제외한 적격 중 `body_edits_30d_metadata > 0`인 첫 2건이 편집층이다. 답·점수·채택은 선정식에 없다. jq/pandoc 중복 ID는 jq에 한 번만 둔다.
3. `sealed/revisions_*.json.gz`를 풀어 `creation_date, revision_number, revision_guid` 순서로 정렬한다. 모든 요청 ID가 있고 `has_more=false`인지 확인한다. 가장 이른 body 기록이 R0이고 생성 뒤 30일 이내 마지막 body가 R1이다. 제목·태그·롤백은 별도 필드로 분류한다.
4. `snapshot_archives.json`의 압축 및 비압축 지문과 각 `evidence/r0`, `evidence/r1` 파일의 UTF-8 SHA-256을 대조한다. 60질문의 129리비전, body111, `last_body` 연결51/51을 검사한다. 누락·삭제되지 않은 모든 원자료를 역사적으로 보장하는 것은 아니다.
5. R0 생성시각 일치8/8과 엄격 최초 게시 바이트0/8은 별개다. 유예 편집을 포함할 수 있으므로 동시대 별도 원바이트 없이는 후자를 올리지 않는다.

## 판정과 분모 산식

`case_id + revision + candidate_id`는 64개 고유 키이고 `case_id + candidate_id`는 32쌍이다. 각 질문·공개판의 후보는 4개다. 각 후보의 문서 SHA, 절 URL, 원 질문 GUID, 실패 조건을 연결한다.

- **문서 비교 가능 쌍:** R0와 R1의 `assessment`가 모두 `미확인`이 아닌 쌍. 26/32이다. `충족` 1, `명시 반박` 8, `범위 밖` 17이다.
- **적합 상태 변화:** 비교 가능 쌍 중 R0와 R1 assessment가 다른 수 / 비교 가능 쌍 수. 현재 0/26, 자연0/14·편집0/12이다. 26개 독립 질문으로 간주하지 않는다.
- **명시한 다음 질문 변화:** `condition_or_next_question_changed=true`인 수 / 계획32쌍. 현재 JN1/map 1/32이며 확정군에 한정하면1/26이다. 연구 주석 `reason`의 문구 변경은 반환 의미 변화로 세지 않는다. PE1 이미지까지 포함한 전체 반환 동등성은 unknown이다.
- **요구·입력·표현 변화:** `text_requirement_change`, `text_input_information_change`, `full_input_information_change`, `visual_equivalence`, raw 지문 차이를 구분한다. 텍스트 C1/C2변화0/8, 입력 보완1/8, raw변화5/8, PE1 전체 입력 미확인1을 하나로 합치지 않는다.
- **자연 발생률:** 자연층4질문에서만 본문변경1/4, 명시조건변경0/4를 기술한다. 편집층4/4는 선정조건이다. 인구집단 추정이나 검색 성능으로 환산하지 않는다.
- **사후 증거:** 답11개·최초답판11개·답리비전13개·댓글17개를 질문자ID·시간으로 연결한다. 채택은 현재표지3/8이고 채택시각은 미확인이다. 원 질문자 완전성공0/8, 정확판자기보고1/8, 같은 성공실행의 정확판검증0/8을 나눈다.
- **답변자 결과:** 구체 출력 텍스트3/11과 별도 작동자기보고1/11을 구분한다. 원 질문자 실행이나 고정판 재연 성공으로 합치지 않는다. 정확한 양성 답ID와 정의는 `outcomes.jsonl`, 재개 사후감사에 있다.
- **0/0:** 엄격 최초게시 비교 또는 인과적 시간절감의 측정 분모가0이면 JSON `value=null`, `status=산출 불가`다. 0%로 출력하지 않는다.

## 출처 최소량과 중복 제외

원장 각 행에 원 URL·판·절, 실제 읽은 UTC, 관측 주체, 확인 내용, 관련 Q/사례/주장, 지지·반증과 한계가 있다. `count_primary=true`인 고유 `primary_unit` 수를 직접 원자료로 센다. 그 집합의 고유 `independent_event_id` 수를 독립 저작·사건으로 센다. 같은 질문의 답·댓글은 SO 질문의 같은 event ID를 쓴다. 댓글·중복 API표현·미러·실패·재개 재열람은 새 원자료 수를 늘리지 않는다.

현재 보수 집계는 원자료120, 독립사건87이다. 요구 최소24/20을 넘으며 선택 질문8사건, CLI12자료/9저작, 플랫폼17자료/8사건, IETF2판쌍·프리프린트2판쌍의 원판·다음판·후속 인용을 포함한다. 출처 행 전체 수는 반복확인을 포함하므로 `metrics.json.sources.records`를 따로 읽는다. 행 수를 독립성으로 쓰지 않는다.

## 정확판 변환을 직접 하지 못한 이유와 명령

설치된 jq1.7 및 Pandoc3.1.11.1은 고정1.7.1/3.1.11과 달랐다. `execution/reproduce.py --preflight`는 종료2를 반환했고 고정판 변환은 실행하지 않았다. 여섯 Pandoc 미확인은 정확판뿐 아니라 handler/template·전체 원입력·AST·writer/engine·출력도 필요하다. 입력37개 스니펫과 추가로 받아야 할 입력, argv·예상·관측 기준은 `execution/README.md`에 있다. 설치나 외부 유료 API 호출은 하지 않았다.

JE1 사후 답 코드의 의심을 해소하려고 설치된 **jq1.7**에서 두 답 프로그램만 보조 실행했다. 양쪽 종료0, 첫 프로그램seq_num `[1,1]`, 둘째 `[1,2]`였다. 이는 게시 출력과 첫 프로그램이 맞는다는 정정 근거다. 고정1.7.1 실험, LangChain Document 실행, 원 질문자의 실행 또는 연구64행의 새 점수로 세지 않는다. 실행행은 `support/resume/outcomes_audit/JE1_answer_variant_run.json`에 있다.

## 원격 계약·완료 검사

결과를 자기 브랜치에 커밋한 뒤 정확 SHA로 다시 가져와 파일 지문을 대조한다. GitHub Git objects를 쓰는 경우에도 부모는 실제 읽은 원격 HEAD, ref 갱신은 expected SHA를 조건으로 하고 최종 tree가 로컬 index와 같은지 확인한다. 기존 history를 초기화하거나 force push하지 않는다.

```bash
python -B -m workbench.session check "$af088/manifest.json" --fetch
```

이 검사가 성공해야 `remote_checked`라고 기록한다. 기존 `manifest.json`은 최초 실행의 `workbench.session start` 산출물을 유지한다. 재개했다고 덮어쓰지 않는다. 같은 계약의 변경이 없었는지, 작업경로 이탈0인지, 의존 branch=SHA가 맞는지 실제 출력으로 확인한다. 마지막 HANDOFF 단독 커밋에는 결과 SHA·검사 대상/종료값·원격 재열람·미실시와 첫 다음 행동을 남긴다.


## 보존 입력의 공백 진단

최종 staging 뒤 `git diff --cached --check`는 종료2를 반환했다. 저작한 Markdown 세 파일의 불필요한 끝 빈 줄은 제거했지만, `execution/inputs/`의 원문 추출파일8개에서 진단12개(행 끝 공백10, 끝 빈 줄2)는 원문대로 유지했다. 추출 지문 검사는0이며 이 공백을 지우면 보존 계약을 깨뜨린다. 전체 진단과 경로 판정은 `support/resume/staged_whitespace.json`에 있다. 이를 무조건 통과로 숨기지 않고, 모든 남은 진단이 보존 입력에만 있는지 별도 검사했다.
