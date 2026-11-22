# AF-RES-025 자체 점검과 별도 판독

## 판정

**REVIEW_READY_WITH_GAPS.** 12개 질문, 24개 실제 경로, 원 72슬롯, 필수 원문 최소수와 Q1–Q7의 직접 근거/반증 기록을 확보했다. 그러나 원 8/24 경로의 최종 세 URL 초과와 가린 세 키의 경로 단어 노출은 고칠 수 없는 실행 이력이다. 최초 원문 복구·역사 가용성의 미확인도 남는다. 사후 표시판이나 계산 검사의 통과로 이 공백을 지우지 않는다.

수용 조건별 bool과 보강/재개 입력은 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 있다. 계산의 무결성, 관측의 정확성, 프로토콜 준수, 제품 효과를 별도 판단한다. 숫자만 맞는 보고서도 원 실험의 결함을 가질 수 있다.

## Q별 주장과 반증 시도

| Q | 주장·관측 | 직접 확인한 위치 | 자기 결론이 틀릴 상황과 찾아본 곳 | 결과·남은 한계 |
| --- | --- | --- | --- | --- |
| Q1 | 답 목록을 고르지 않고 세 원장의 메타데이터에서 첫 적격 12개를 선택 | SCOPE §①; frame 425행; AR-I01–04, CG-I01–03/05, JP-I01–04의 exact commit/Message-ID와 입력 해시 | 이미 구현된 안정화 작업이면 새 설계가 아니므로 RFC3143 최초 전문을 다시 확인; force-push·앞선 fork·JEP72/79 최초판도 복구 시도 | Q08 검색 전에 RFC3146으로 공개 정정. 전체6·부분6 유지. Cargo 현재 라벨과 초기 날짜 집중은 대표성 한계. JEP66 더 이른 blob·Arrow 최초 linked head 미확인 |
| Q2 | 같은 전문·도구·언어·모델·날짜·범위, 경로당 봉인3질의와5원문 시도 | queries24행, search-log의 search_request72행; input-lock과 input-amendment-Q08 | 질의가 뒤늦게 바뀌거나 R에 정답명을 주었는지 원 문자열/순서/원문 해시 비교; 같은 후보 선택 규칙 적용 | 바이트·질의·교대 순서 검산. G/R 문맥 공유, 원8경로 최종 URL 초과. 실제 Pro UI/독립 세션 비교는 미관측 |
| Q3 | 실제 제공 순위·부족·실패·중복·재시도를 남김 | search-log835행; discovery-summary; discovery-open-outcomes130행; 원 receipts | 성공 bool이나 코드 모양 줄번호를 원문으로 오인할 수 있어 raw header/status 재독. 특히 AR-C003/007, CG-C027/028, JP-C017/027 | 본문115·실패8·요약7호출. Cargo unknown bool을 실패0으로 쓰지 않음. 후속 재열람을 원 발견 비용/성공으로 넣지 않음 |
| Q4 | 필수 묶음의 모든 조건을 열고 인용해야 성공 | judgments337행/104묶음/93키, primary-seal; baseline-recount Q11c | 목적은 같아도 값/offset, downcast/common value, matching/receiver readiness, 단일 파일/전체 설계 경계가 다른 후보 보존 | 원72슬롯: 충족2·충돌14·보류53·빈3. 완결2는 기지 호스트 새 부품. minarrow M3 인용 공백은 사후 제한판에서 생겼으며 원본 누락으로 세지 않음 |
| Q5 | 원거리 관계의 대응은 전제·주체·실패 조건까지 필요 | REL01–03: reviews/jupyter-by-arrow/relation-check.json; REL04–05: reviews/cargo-by-jupyter/relation-check.json; CG-C029–031, AR-C017/008; SP-L01/L02/M01/M02 정확 절 | 단조성·trace가 no-feedback를 뜻하는지 a→b→c 반례; 64bit 값/offset 혼동; WIP 카드가 포트 예약을 보장하는지 두 동시작업 반례 | 일부 관계는 유지되지만 완결 신규 원거리0. 보조 네 원문은 주 판정 원격 봉인 뒤 읽고 적중0 추가. IFLA GARR 원문 실패를 운영 자료로 일부 대체 |
| Q6 | 최초 명시·후속 명시·실제 선택·당시 이용 가능성을 구분 | followups 12 decision행/66 history행; AR-H003/004/022, AR-F006/007/020, CG-F102/103/104/014, JP-H001–007/F021 | 호스트 연령을 기능 시점으로 대체하는지 태그/코드/출시일 대조; Q07 요구 삭제, PR70 open, Bright 재개정일, 동명 quiver 계보를 반증으로 점검 | 당시 전체 supported1·정확 후발19·unknown46. 유일한 GCC 부품도 원 인용 미완결. OGC supported 초안을 unknown으로 정정. 당사자 사전 지식·실제 적용 diff는 미확인 |
| Q7 | 이번 상한에서 R의 신규 완결 이득을 관측하지 못함 | pairs24행(12질문×2표시판); metrics48행; literal-top1-summary; report-facts | G가 나은 Q01/Q11 및 개선 없는 Q09/Q12를 원 인용/조건으로 검토; 원제안 노출·메타데이터·가림 누출 질문 제외 | 신규 G0/12·R0/12, 기지 새 부품 G2·R0. 첫 URL만 남기면 G1·R0. 당시 완결 신규/기지 부품0. 효과 동등성·실제 인시 절감은 미확인 |

## 판독자의 역할과 실제 수정

초기 검색·자기 판독과 다른 stream을 담당한 같은 모델 에이전트의 교차 판독을 분리했다. 세 판독자는 각자의 원 검색 경로를 채점하지 않았다. 하지만 원문 요약의 해석 표현, 세 키의 G/R 단어, 모델 사전지식은 제거되지 않았다. 이 검토는 사람의 독립 검증·이중맹검·새 사용자 실험이 아니다.

최종 보고서도 세 별도 에이전트가 읽었다. Cargo 담당은 48개 metric행을 scored-slots에서 다시 계산해 불일치0을 확인했다. Jupyter 담당은 익명 관계 파일 링크의 뒤바뀜, XPUB_VERBOSE 조건을 최종 텍스트에 귀속한 문장, 원 질문의 제안 상태를 후보 채택처럼 읽을 수 있는 셀을 지적했다. Arrow 담당은 재작성 요약 두 건, metadata 한 건, 같은 파일 patch 두 건의 원문 산입 오류와 `role` fallback을 지적했다. 모두 공개 정정과 재집계에 반영했다. [final-review.json](evidence/final-review.json)은 지적·처리·한계를 보존한다.

최종 보수적 원문 수는 `source-counts.json`이 단일 집계 원장이다. 판독 중 179라는 잠정값에서 요약/metadata/중복 patch 다섯 건을 제외했다. 같은 사건의 별도 후속 댓글을 최초 초안의 복제라고 부르던 설명도 고쳐 문서 ID와 최소수 그룹 ID를 분리했다. 같은 계보의 별도 문서를 제외하는 보수적 집계이므로 모든 고유 문서를 망라한 수가 아니다. 원문 수는 독립 사건 12건을 늘리지 않는다.

## 재집계 명령

저장소 루트에서 실행한다. 모든 Python 호출에 `-B`를 붙여 소유 경로 밖의 bytecode cache를 만들지 않는다. Arrow 메일 전문의 캐시는 커밋하지 않았으므로 새 checkout에서는 먼저 고정 Message-ID와 SHA-256으로 복구한다.

```bash
python -B docs/workstreams/research/AF-RES-025/streams/arrow/restore_inputs.py
python -B docs/workstreams/research/AF-RES-025/tools/check_inputs.py
python -B docs/workstreams/research/AF-RES-025/tools/audit_baseline.py
python -B docs/workstreams/research/AF-RES-025/tools/normalize_observations.py
python -B docs/workstreams/research/AF-RES-025/tools/assemble_exposures.py
python -B docs/workstreams/research/AF-RES-025/tools/assemble_sources.py
python -B docs/workstreams/research/AF-RES-025/tools/assemble_costs.py
python -B docs/workstreams/research/AF-RES-025/tools/recount.py
python -B docs/workstreams/research/AF-RES-025/tools/literal_top1.py
python -B docs/workstreams/research/AF-RES-025/tools/render_result.py
python -B docs/workstreams/research/AF-RES-025/tools/validate_artifacts.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-025/manifest.json --fetch
```

`restore_inputs.py`는 네트워크 읽기이며 다른 명령과 구분한다. 고정 의존021 자료를 재검산할 때의 다운로드 입력과 해시 범위는 baseline-audit.md를 따른다. 당시 읽은 바이트를 확보하지 못하면 복구 실패로 남기며 다른 텍스트를 같은 입력으로 바꾸지 않는다. `assemble_inputs.py`, `make_blind.py`, 각 stream의 검색 실행기는 새 입력/봉인을 만들 수 있어 단순 검산 순서에 넣지 않았다. 원 질의 재실행은 같은 관측의 재집계가 아니라 새로운 검색이다.

RESULT의 네 표는 `tools/render_result.py`가 `returns-raw.jsonl`, `judgments.csv`, `metrics.csv`, `pairs.csv`, `literal-top1-summary.json`, `sources.json`에서 생성한다. 해석은 `analysis/interpretation.md`에서 오며, 숫자 placeholder는 source/history 집계로 채운다. 생성 후 같은 행의 합계·분모·최종 약점3행을 validator가 확인한다. 생성 스크립트가 판독의 사실성을 증명하는 것은 아니다.

## 실제 검증과 미실시의 경계

저장소 계약 검사는 `evidence/session-check.json`에 원 출력과 종료코드를 기록한다. 현재 통합 브랜치가 시작판 이후 움직였어도 계약 fingerprint와 owned path가 일치하는지 확인한다. 별도 stream 검산은 Arrow355, Cargo 기록 검산, Jupyter1016개로 이루어졌으며, 서로 다른 검사 항목이므로 이를 독립된 기능 테스트 수로 더하지 않는다.

최종 통합 검산은 2026-11-22 06:32 UTC에 **1,146/1,146 통과**, 최초 입력 검사는 **219/219 통과**했고, 고정021 재집계18행은 저장 결과와 일치했다. 계약 검사는 exit0/passed이며 조회한 통합 SHA `01394a47888fba39e3babf6ad0249a1a37ace76c`에서도 contract fingerprint가 같고 outside_paths/unmerged_paths가 비어 있었다.

공급자 runtime·대형 파일·Java JNI·사용자 시간 실험은 실행하지 않았다. 필요한 명령·고정 태그·입력은 [pending-checks.md](pending-checks.md)와 후속 README에 있다. 이 연구의 결론은 정적 문서·코드·테스트 원문 판독과 실제 검색 실행에 한정된다. 원 입력/조건의 지원이 미확인인 후보를 구현 실패라고 단정하지 않는다.

한 번의 `workbench.session check --help` 호출이 작성한 소유 경로 밖 Python cache 세 개는 timestamp로 자기 생성물임을 확인해 제거했다. 기록은 `evidence/runtime-cache-cleanup.json`에 남기고 이후 `-B`/`PYTHONDONTWRITEBYTECODE=1`을 사용했다. 공통 추적 파일은 수정하지 않았으며 dot-control도 그대로다.

공개 파일 검사에서 Jupyter 후속 요청32개에 내부 연결 선택자가 남은 것을 발견해 현재 파일의 request 필드만 가렸다. URL·시각·응답 해시·판정은 유지했다. 인증 토큰으로 확인된 값은 아니지만 불필요한 내부 식별자라 제거했다. 이미 커밋된 `0a61785...` 이력은 재작성하지 않았으므로 과거 사본까지 삭제했다고 주장하지 않는다. 정정은 `followups/jupyter/amendments/JP-AMEND-002.json`에 있으며 현재 공개 산출물 재검사에서는 해당 값 패턴0이다.

## 값의 뜻

| 값 | 뜻 | 예 |
| --- | --- | --- |
| 0건 | 정해진 관측 분모에서 세는 사건이 없었음 | 완결 신규 원거리 적중0; 신규 주 지표0/12 |
| 해당 없음 | 그 행의 대상/단위가 적용되지 않음 | 빈 슬롯에는 후보의 출시판이 없음 |
| 관측 실패 | 실제 요청을 했으나 원문·본문을 확보하지 못함 |404, 빈 본문, 접근 실패 영수증 |
| 미확인/unknown | 관측 자료로 특정 명제를 결정하지 못함 | 당시 전체 기능46후보, 실제 인시 절감 |
| not_available | 정확히 반환된 기능/공개판이 최초일보다 후발임을 확인 | PyArrow21 옵션, ipykernel6.27 cell_meta |
| 보류 | 원 필수 조건의 지원이나 인용이 불완전함 | Node의 후속 클라이언트 연결 기록 P3 |

최종 원격 수용 근거·자체 점검을 먼저 커밋하고 읽은 뒤에만 HANDOFF를 작성한다. 그 고정 결과 SHA와 마지막 인계 SHA는 HANDOFF/PROGRESS 및 원격 영수증으로 확인한다.
