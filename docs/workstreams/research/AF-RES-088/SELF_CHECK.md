# AF-RES-088 자체 검산

**연구 PARTIAL.** 원래8자리·64행·32쌍을 유지했다. 자료 최소량과 표 구조를 채웠더라도 PE1의 옛 그림과 여섯 Pandoc 구현의 필수 의미 근거가 비어 있다. 이 파일은 같은 연구팀의 자기 검산이다. R0/R1 독립 이중맹검, 검색 성능 실험, 원 질문자의 실행 확인으로 부르지 않는다.

## Q별 주장·근거·반증 탐색

| Q | 현재 주장 | 원문 또는 실행행 | 자기 결론이 틀릴 사례를 찾은 경로·발견/공석 | 다음 최소 확인 |
| --- | --- | --- | --- | --- |
| Q1 | R0는 가장 이른 보존 공개 body이다. 생성시각 일치로 즉시 게시 바이트를 확정할 수 없다. | PL01/09/20: API revision 및 편집 정책판; `revisions.jsonl`; `support/revision_integrity_audit.json`:129리비전·51/51 last_body 연결 | Meta302285 제목만 수정, Meta17038 rollback/표현전환을 직접 대조했다. PN1 답의 pre.class 차이는 내용 리비전 없이도 표현이 달라질 반례다. 동시대 첫 바이트는0/8이다. | 질문 생성 당시의 독립 보존 HTML/Markdown·시각·지문 |
| Q2 | 2024-04-01≤생성<2024-07-01, 현재 태그별 첫30·적격60·선택8, 결원0이다. | `raw/frame_*`, `frame.csv`, `frame_metadata.json`, frame source60행 | jq25/27·Pandoc23의 적격 경계를 검토했다. 좁게 제외해도 첫2자연·첫2편집 ID는 동일하다. PE2는 pandoc 태그가 나중에 추가됐다. 삭제/태그이탈 질문은 모른다. | 동일 기간 삭제/태그이력의 합법적 보존 목록; cap 이후 표본은 별도 연구 |
| Q3 | 명시 C1/C2는8개 모두 텍스트상 유지됐다. 입력보완1, raw변화5이다. | `requirements_r0.jsonl`, `requirements_r1.jsonl`, `evidence/r0/`, `evidence/r1/`, `pairs.csv` | JE1 heading/indent, JE2 인라인 코드, PE2 code fence를 대조했다. JN1 전체 JSON 추가는 실제 정보변화다. PE1 URL교체 그림은 미확인이다. 외부 SO60148441은 답 뒤 해법 추가의 실제 반례이며 표본에 넣지 않았다. | PE1 세 이미지 바이트·시각; 그 그림에만 있던 조건/해법 단서 |
| Q4 | 동일 문서판·같은 후보계약에서26확정+6미확인이다. | `candidates.csv`, `judgments.csv`; MAN01–12; `support/resume/gap_audit/audit.md` | map 길이 변화, group_by 하위배열, jq/YAML 파서 경계, Pandoc docx/pptx template 제한, Lua 반환형 및 metadata escaping을 확인했다. 임의 Lua가 있다는 이유로 성공으로 올리지 않았다. PE1 default.latex 출처ID 오류는 후속 정정으로 연결했다. | 여섯 미확인별 실제 handler/template·입력·AST·writer/engine·출력 |
| Q5 | 확정26쌍에서 적합상태 변경0, 명시 다음질문 변경1/32이다. | `pairs.csv`, `metrics.json`, `recalculate.py`; JN1/map의 R0/R1 next_minimum_input | 같은 링크가 같은 안내를 뜻하지 않는 JN1을 찾았다. 미확인→미확인6개와 이미지 미확인을 정오불변으로 세지 않았다. 모든 R1 reason 문자열이 달라도 의미변화32개로 세지 않는다. | 독립 독자가 원판만 보고 코딩한 별도 실험; PE1 이미지 확보 후 전체반환 비교 |
| Q6 | 채택3/8, 원 질문자 완전성공0/8, 정확성공판0/8이다. 답 이후 본문편집2건은 타인이다. | `outcomes.jsonl`, `raw/outcomes/`, `evidence/answers/`; `support/outcome_integrity_audit.json` | PN1은 채택해도 나중에 쓸 계획이라고 했다. PN2 수동불가 제약은 사후댓글이다. PE2는30일 답0지만댓글1이다. 무응답대조78566705와 해법삽입대조60148441은 별도다. JE1 출력불일치라는 초안 주장은 jq1.7 두 실행으로 반박·정정했다. | 질문자 원입력·완전명령·정확판·출력을 연결한 공개 후속 기록 |
| Q7 | 현재 URL만으로 요청 시점·원조건·후보판을 복원할 수 없다. 판ID+조건위치+후보판이 보존력을 높인다. | 표3의24행; CF-S01–17; `support/cross_fields.md`, `support/resume/sources_audit/` | QUIC/TLS의 실제 draft판쌍·후속인용, Transformer v1/v2 수치와 같은v2 내부상충, Kalb–Ramond amplitude정정·양판이 지지하는 parity인용을 대조했다. 정정이 모든 인용을 무효로 만든다는 가설도 반박됐다. | 특정 인용자가 읽은 파일 hash/판 또는 실행 artifact. 번호 없는 인용을 정확판 읽기로 승격하지 않음 |

## 재개 검토가 바꾼 것과 그대로 둔 것

1. **JE1 답의 코드 해석 정정:** 첫 프로그램의 `.key`는 `.value` 내부에서 평가되어 두 `seq_num`이1이다. 두 번째 대안은 entry key를 써1·2이다. 보조 jq1.7 실행은 양쪽 종료0이었다. 초안의 “게시 출력과 프로그램이 상충”을 철회하고 “두 프로그램의 seq_num 동작이 다름”으로 고쳤다. 이 사후 답은 R0/R1 채점의 근거가 아니므로64행은 바꾸지 않았다.
2. **답변자 보고의 분류 명료화:** 구체 출력 텍스트와 PN1 답78261053의 추가 작동자기보고를 분리했다. 둘을 원 질문자 실행·정확판 성공으로 올리지 않았다.
3. **PE1 원문 위치 대응 정정:** `manual_additional_urls`의 default.latex 주소는 맞지만 일부 `manual_source_ids`는 HTML5인 MAN-06을 가리켰다. 직접 대응 MAN-10 및 필요 생성경로 MAN-11/12를 후속 `evidence_corrections.jsonl`에 적고 표2에 드러냈다. 사전 CSV를 소급 수정하지 않았다.
4. **표현·집계 보정:** JN1은 “JSON5개”가 아니라 “DailyForecasts 항목5개를 포함한 전체 JSON”이다. 채택과 사용판이 실제로 불일치한다고 단정한 제목을 “채택만으로 확인할 수 없음”으로 고쳤다. 해법삽입대조의 원시 출처3행 중 댓글1은 최종 최소량에서 제외되어2행이다.
5. **관측 범위의 명시:** PE1 텍스트 조건과 전체 이미지 의미를 구분한 시도1의 후속 정정을 검토했다. `full_input_information_change=unknown`을 유지한다. 출처 재열람과 raw표현 중복은120원자료·87사건을 늘리지 않는다.

## 실제 검산 및 미실시

`support/resume/validation.json`은 이번 결과 내용에 대한 명령·입력 hash·stdout/stderr·종료값을 보존한다. 재집계는60프레임·8질문·8후보·64행·32쌍, 원목록 순서, 공개판 지문, R0 봉인 불변, 후보계약 불변, source ID 연결, 표1/2/3의8/32/24행, 약점3개, 소유경로만 변경을 확인한다. 이것은 의미 판단의 자동 검증이 아니다.

정확판 gate는 종료2였다. jq1.7/Pandoc3.1.11.1로 고정1.7.1/3.1.11 실행을 대체하지 않았다. 후속 입력37개 스니펫과 실행명령·성공/반증 관측은 `execution/README.md`에 있다. JE1 사후 코드 두 실행만 버전이 다른 별도 보조검사다. 원 사용자 성공판·검색순위·도움/시간절감·독립 의미 일치도는 미측정이다.

최종 manifest 검사와 정확 결과 SHA의 원격 재열람은 결과 커밋 뒤 수행하며, 그 실제 SHA·종료값·범위는 마지막 단독 `HANDOFF.md`에 기록한다. 자동검사 PASS를 REVIEW_READY로 바꾸는 근거로 쓰지 않는다.


### Staging 이후 공백 검사

`git diff --cached --check` 종료2의 남은12진단은 원문에서 추출한8파일의 공백·끝 빈 줄이다. 원문 지문을 보존하기 위해 변경하지 않았다. 저작한 Markdown의 끝 빈 줄은 수정했다. `support/resume/staged_whitespace.json`에 전체 진단을 남겼고, 모든 진단이 `execution/inputs/`의 보존 추출물에 속하며 `extract_inputs.py --check`가0인지 확인했다. 원문 보존 예외와 일반 작성물 검사를 분리하며 실패를 검사 통과로 바꾸지 않는다.
