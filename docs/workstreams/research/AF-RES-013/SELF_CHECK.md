# AF-RES-013 — SELF_CHECK

## 판정

**산출물·실행 기록·채점·지정 형식 검증은 통과했다. 전체 인수 조건은 `BLOCKED`다.**

남은 한 가지 차단은 사용자 요청의 **같은 사이트 자료는 최소 개수에 최대3개만 산입**한다는 규칙이다. 비사례25개는13사이트·사이트당 최대3개로 충족한다. 그러나 사례 고정판31개는 모두 GitHub 계열 호스트이므로 사례 최소수에도 이 규칙을 문자적으로 적용하면 산입 가능한 것은3개이며 요구된30개에 못 미친다. 최초 SAMPLING에서 비사례에만 상한을 적용한다는 해석을 사전 기록했지만, 그 기록은 사용자 승인된 예외가 아니다.

이 차단을 해소한 것으로 꾸미거나 기존 표집·실행을 삭제하지 않는다. 이미 완료한 31사례·62run·342후보 판정과 결과는 그대로 인계한다. 아래의 내용 검증과 별도로 전체 완료 승인을 주장하지 않는다. 사용자가 지정한 **막히면 이유와 다음 첫 행동을 HANDOFF에 적는 경로**에 따라 차단 인계를 작성한다. 일반 완료 HANDOFF를 쓰기 위한 SELF_CHECK 통과와 구별한다.

결과 보고서 커밋: `3c11a5344d66edf6e6e0bb71bdb670dd2e8fbbe4`.
최종 판정 데이터 커밋: `eaa156ced81cc889990a2ce0e7749e43159bb71f`.
원 실행 보존 커밋: `caa2a814727dd485ed0eb9bb8530d6b16fab9584`.

## 세부 질문별 자기 점검

| 세부 질문 | 답 한 줄 | 붙은 출처 ID(종류 수) | 반증 시도(쓴 질의·자료와 결과) | 남은 불확실성 |
| --- | --- | --- | --- | --- |
| Q1 | 네 계열은 목적과 대안을 분리하지만 빈 절·리뷰 수정·시대 차이가 있다. | R-TEMPLATE-PRIOR-MERGE, PS-T-SWIFT-INITIAL, PS-T-PEP12, K-TEMPLATE-NOW(템플릿); M26·R-REVIEW-123(토론); M06(평가 분석), 3종류 이상 | K-Q1–4와 번호순 직접 URL 선별, RV-K177-EMPTY 재열람. 실제 Alternatives가 안내 주석만인 사례와 RFC85의 결합 절 제목 누락을 찾았다. | 미확인(Go·TC39·IETF·ADR의 실제 문서와 템플릿 이력을 별도 층으로 조사). 절 도입 날짜는 저장소 이력이지 인터넷 최초 공개의 완전 증명은 아니다. |
| Q2 | 독립 제안31개·4계열·gold176·채택 후 대체6개를 구성했으나 사례 사이트 상한의 문자적 최소수는 미충족이다. | PS-P0201-gold(고정 제안); R0085-PR·R0042-HEAD-DATE(결정/판 metadata); M05·M02(평가·누설 방법론), 3종류 이상 | selection 원장176행의 직접 읽기/부분·자동 검사를 구별하고 P0386의 두 비교기를 잘못 합친 누락을 복구했다. prefix 해시31개와 Git 조상 관계를 독립 재계산했다. | 인수 차단: 동일 호스트31개는 문자적 상한 적용시3개. 최초 SAMPLING의 해석을 사용자 규칙으로 소급 승인할 수 없다. 최소 추가 확인은 요청문과 이 해석의 인수 처리 또는 별도 절차로 최소10사이트의 적격30사례·실행 확보다. |
| Q3 | 역할은0·17·146·12·1·0이며, 종류는 외부 실체30·구조146이다. | PS-P0201-gold·R0085-DOC(제안); R-REVIEW-123·PS-R-S21-LENS(토론), 2종류 | lens·partial application·selector·initializer 토론 URL을 외부 실체처럼 센 오류를 원문으로 반증했다. 비적중 항목에도 같은 정정을 적용했고 original values를 보존했다. | 미확인(169개 항목의 review-added 시점은 해당 최초판→결정판 diff와 연결 토론으로 확인). 별도 리뷰7개 중 alias1개를 뺀 확대 분모182는 본문176과 분리한다. |
| Q4 | 다른 분야 구조 차용1/176, 그 분야 외부 자료 인용0/176이며 실제 채택 효과는 확인하지 못했다. | RV-C05-ACTIVE-VOICE(고정 설계); RV-R123-TERM·PS-R-S21-LENS(리뷰); M12(인용 평가 종합), 3종류 | 재개 직접 탐색 RV-OPEN-RV-R123-TERM 및 C05 원문을 대조했다. 초기0건 분류를1건으로 고쳤지만 Clojure Atom 용어 비유와 다른 언어 문법은 먼 분야로 올리지 않았다. | 미확인(현대 Prior art 절·실제 변경 diff를 층화 표집하여 채택·효과 확인). 이 표본의 낮은 빈도는 수요·무효용의 증거가 아니다. |
| Q5 | A31run·204후보에서 역사 gold16/176, 날짜 무관23/176을 회수했다. | 실행 예외 기준: RESULT 표1·§3.1 수치 + runs/A/C09.json(range/xrange)·C03.json(코드 endpoint/primitive)·C12.json(다른 type cache); M02·M15 보조 | 원 검색326개 문자열과 code API 시도를 감사했다. 비슷한 CPython/PyPy cache를 실체 일치로 올리지 않았고 C08 A1의 상세 의미 근거 날짜를 unknown으로 정정했다. | 미확인(unknown79후보의 cutoff 이전 claim-bearing 판 확인). endpoint HTTP200은14/31이며17개 차단/fallback 때문에 완전 접근 조건의 도구 일반 성능은 판단하지 못한다. |
| Q6 | B31run·138후보에서 역사 gold5/176, 날짜 무관14/176을 회수했다. | 실행 예외 기준: RESULT 표1·§3.1 + runs/B/C05.json(EIP·zap)·C22.json(용어 번역)·C31.json(카탈로그); 목록·원문 경로는 각 run | 목록 제한 질의176개와 실제 열린 discovery_catalogue_url를 대조했다. B12/B22의 성공 수 대신 실패 포함 비용을 확인했고 C05 B3의 미제시 grouping 연결을 유용 수에서 뺐다. | 미확인(unknown67후보의 당시 판 및 사람 번역과의 비교). B는 gold 미열람을 선언한 내부 모델 번역이며 사람·강제격리 검증이 아니다. |
| Q7 | gold 적중과 정답 밖 문서상 유용 A170/178·B109/120을 분리했고 근거부족21/342를 남겼다. | 실행 예외 기준: RESULT 표1·2 + JUDGMENTS의 C03 A4·C05 B3·C13 B1·C30 A3. 고정 AF004 PROTOCOL; M13·M14 평가 논문 | 정확 URL 차이5행을 재열람하고 redirect/alternate path/metadata-only를 구분했다. 내부 교차검토36행 및 작업자 조정으로 과도한 구조 일치와 다른 baseline의 설명 보충을 취소했다. | 미확인(각 remaining_check의 연결 계약·실제 대상 적용). 모든 runtime_observation은 not_performed이며 현재 조건부 참고를 실제효용·완성품성공으로 해석하지 않는다. [같은 실행의 별도 채점](evidence/parallel-review-71d498d6556a/README.md)에서 gold 집합23행·라벨58행 차이가 있어 전수 재심이 필요하며, 주수치는 유지한 snapshot의 기술값이다. |
| Q8 | 기존 조합에 대한 절대 관측은 생겼지만 H1/UI 추가 가치의 기각 조건은 실행하지 않았다. | 고정 AF009 GAP §2·3·5(앞선 연구 입력); M03·M12·M15(평가 논문); RESULT 수치 및 C29 A4 원 실행, 3종류 | C29의 C# partial type과 실제 후속 변경을 대조하여 gold 밖 참고의 반례를 확보했다. 낮은 recall만으로 새 제품 우위를 주장하는 해석을 gold 구성·시간·부분 유용성으로 반증했다. | 미확인(실제 과제·허용 오류·검토시간을 사전 고정한 새 절차와 동등 예산 비교). 다른 분야 gold는1개뿐이고 H2 유지 가치는 범위 밖이다. |

질문별 출처 종류 또는 실행 예외 기준이 부족한 행, 빈 반증 시도 행은 없다. 숫자는 `evidence/AGGREGATES.json`, 직접 열람의 범위·한계는 `sources.json`, 실제 질의 문자열은 `SEARCH_LOG.json`과 원 `runs`에 있다. 원장이 가진 내용만 검사했으며 새 사용자 반응·실행 효과를 만들어 채우지 않았다.

## 실제 검증과 이견 처리

- `tools/analyze_results.py`: 342후보 전수 키·원 URL·라벨·L/E/H/T·역사 bucket·유용 조건, 종류/역할/사례별 집계를 검사했다. gold identity·분모는 유지했고 날짜 판단을 원 응답의 시점 표시와 구별했다.
- `tools/audit_runs.py`: A31/B31의 원 응답·문맥 입력·예산·목록 발견·코드 검색 시도를 검사했다. A326질의/561열람 비용, B176질의/698원장 행/703보수 비용이다. exact URL 차이5행은 별도 판정 기록으로 해소하거나 근거 부족으로 남겼다.
- `tools/validate_deliverables.py --phase self-check`: CASES 고정 SHA와 gold identity, prefix31 hash 및 선행 조상, 원 run62개 전체 바이트 불변, 표 열/행, Q1–Q8, §4 정확히3건, 로컬 링크, 출처 필드/최소수/사이트 분포, owned_path 범위를 검사한다. `artifact_integrity=passed`와 `strict_acceptance=blocked`를 따로 출력한다.
- 내부 별도 검토3개 문맥이 판정을 나누고 경계36행을 교차검토했다. 다른2개 내부 문맥의 최종 보고서 검토도 수치·내용·과대 해석을 대조했다. 분류 신뢰도 실험 또는 다른 모델/사람 평가라고 부르지 않는다.
- C08 A1의 날짜 정정 뒤 A 최종 후보 날짜는103/22/79(pre/post/unknown), 역사 유용83·역사 gold16은 불변이다. 과거 검토 snapshot의104/22/78과 현재 수치를 혼용하지 않는다.
- Git 계약/소유권 검사는 `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-013/manifest.json --fetch`로 별도 실행하여 passed를 확인했고 `evidence/SESSION_CHECK.json`에 기록했다. 이는 연구의 사이트 상한 차단을 해소하는 검사가 아니다.

## 같은 원 실행의 별도 채점과 재검사

원격 주결과 `eb569f07a3a34ffacf114384ae9b06ad062f5396`과 별도 작업공간 `/workspace/scratch/71d498d6556a/agentflow-open`의 미게시 판정을 대조하고, 주보고서와 주채점을 유지한 채 [별도 채점 부록](evidence/parallel-review-71d498d6556a/README.md)으로 보존했다. 이는 **같은 원 실행에 대한 상관된 내부 별도 검토의 민감도 기록**이다. 새 기준선 실행, 다른 모델·사람의 검증 또는 합의 판정이 아니다. 아래 차이를 반영하여 주보고서의 점수를 새로 확정하거나 평균·통합 점수를 만들지 않았다.

| 지표 | 유지한 주결과 | 별도 snapshot |
| --- | --- | --- |
| A 동일 / 결정 전 적중 | 23/176 · 16/176 | 22/176 · 16/176 |
| B 동일 / 결정 전 적중 | 14/176 · 5/176 | 8/176 · 2/176 |
| A+B 동일 / 결정 전 합집합 | 29/176 · 17/176 | 24/176 · 16/176 |
| 근접 오답 합계 | 0/342 | 12/342 |
| 외부 실체 / 내부 구조 gold 분모 | 30 / 146 | 34 / 142 |

[COMPARISON.json](evidence/parallel-review-71d498d6556a/COMPARISON.json)은 후보342개를 `(baseline, case_id, rank)`로 짝지어 **129행**에서 하나 이상의 비교 필드 차이를 확인했다. H96행, 라벨58행, T26행, gold 일치 집합23행, 날짜7행, E3행의 차이가 있으며 이 수는 서로 겹친다. 주결과의 외부 실체30·구조146 정정과 비사례25개·13사이트 최소수 산입은 유지했다. 별도 snapshot의34·142 및26개·14사이트를 현행 값에 섞지 않는다. 정답 항목의 동일성과 역할, 원 응답의 변화 때문에 생긴 차이로 해석하지 않는다.

[대표5행 내부 별도 검토](evidence/parallel-review-71d498d6556a/REPRESENTATIVE_REVIEW.json)는 원 응답의 참고 범위와 출처에 등장하기만 한 객체, 실제 제시한 대상, 명명 정규화의 경계를 다시 읽었다. B-C27-r1에서는 주결과의 보류가 더 지지되고, B-C09-r3·B-C24-r2·B-C22-r1에서는 별도 snapshot의 일치 판정이 고정 규칙에 더 직접적으로 지지되는 이유가 있었다. A-C31-r1은 양쪽 근거 모두 그대로 확정하기 어려웠다. **어느 한 채점 계열이 전부 옳다는 결론을 내리지 않았으며, 모든 대표행은 `unresolved_no_consensus`로 남겼다.** 차이를 본 뒤 고른5행은 오류율이나 신뢰도 추정 표본이 아니다. gold 집합이 다른23행과 라벨이 다른58행 전체의 실질 재심은 미실시다. 따라서 주수치는 유지한 판정 snapshot의 기술값이며, 합의된 정확도나 안정된 유용성 추정치가 아니다.

보존·재검사에서 실제 확인한 내용은 다음과 같다.

- [SNAPSHOT.json](evidence/parallel-review-71d498d6556a/SNAPSHOT.json)과 [VALIDATION.json](evidence/parallel-review-71d498d6556a/VALIDATION.json): 기준 커밋 `caa2a814727dd485ed0eb9bb8530d6b16fab9584`와 다른 owned_path 내부230개 파일·4,752,466바이트의 크기·SHA-256,342개 판정 쌍, 원 실행62개 전체 바이트 불변을 확인했다. 부록은 전체 저장소 복제본이 아니라 차이 snapshot이며 누락된 입력은 부록 README의 논리적 경로 규칙에 따라 기준 커밋에서 읽는다.
- 별도 출처 원장1335행과 제외342건의 연결·필드를 확인했다. 이는 같은 자료의 재열람을 포함한 열람 기록 수이며 독립 문서 수가 아니다. 주결과의 최소수25개에 더하지 않았다.
- `python docs/workstreams/research/AF-RES-013/evidence/parallel-review-71d498d6556a/validate_snapshot.py`와 `python docs/workstreams/research/AF-RES-013/tools/validate_deliverables.py --phase self-check`를 실제 실행한 기록은 각각 부록 VALIDATION과 주 [FINAL_VALIDATION](evidence/FINAL_VALIDATION.json)에 있다. 보존/산출물 무결성은 passed이고 strict acceptance는 SITE_CAP_CASES로 blocked다.
- 같은 작업공간의 [SESSION_CHECK.json](evidence/parallel-review-71d498d6556a/SESSION_CHECK.json)은 session check `--fetch`의 exit0, passed, `remote_checked`, 범위 밖 변경0·미해결 Git 충돌0을 기록한다. 이것은 Git 계약과 소유권의 검사이며 채점 이견이나 사이트 상한을 해소하는 검사가 아니다.

이 재검사는 `snapshot/evidence/FINAL_VALIDATION.json`에 보존된 **예비 data 모드19항목 통과**와 구별한다. 예비 snapshot의 SELF_CHECK 문구를 현재의 완료 승인으로 사용하지 않는다. 현재 전체 인수는 계속 **BLOCKED — SITE_CAP_CASES(문자적 최소수3/30)**다. 원격 게시의 미래 SHA나 마지막 HANDOFF의 아직 수행하지 않은 원격 대조를 이 절에 성공으로 기록하지 않는다.

## 보강할 수 없는 행과 최소 추가 확인

**SITE_CAP_CASES:** 현재 산출물의 고정판 호스트는 GitHub 계열31개다. mirrors나 같은 페이지의 다른 표현을 새 사이트·독립 자료로 바꿔 세지 않는다. 사후에 요청의 상한 예외를 만들거나, 결과를 본 뒤 선정 규칙을 수정해 새 표본을 원래 사전 선정이라고 주장하지 않는다. 현재 31사례의 분석을 더 읽거나 재채점해도 이 산입 조건은 달라지지 않는다.

다음 첫 행동은 진행 담당이 `SAMPLING.md`의 최초 커밋 `4398d0b`와 이 요청의 사이트 규칙, `evidence/FINAL_VALIDATION.json`의 호스트 분포를 함께 대조하여 **이 사례 집합을 인수할 수 있는지 기록하는 것**이다. 문자적 규칙을 유지하면 최소10개 사이트의 적격 사례30개를 새 절차로 먼저 고정하고 접두부·gold·A 전사례/B20이상 실행을 추가로 확보해야 한다. 이는 현재 결과의 출처 링크를 바꾸거나 미확인 칸을 채우는 작업으로 대신할 수 없다. 질문이나 승인 요청을 보내지 않았고 dot-control은 수정하지 않았다.

## 끝내도 되는 조건 — acceptance_evidence

| 조건 | 충족 여부 | 근거 위치 |
| --- | --- | --- |
| 4개 이상 계열·30개 이상 사례·대체 결정5개 이상 | **아니오(문자적 사이트 산입 규칙)** | 독립 문서 구성은31개/4계열/채택 후 대체6개로 충족: CASES·AGGREGATES. 그러나 원문31개가 같은 사이트라 최소수 산입은3개: FINAL_VALIDATION.blockers 및 SOURCE_COUNT. |
| 사례마다 정답 항목3개 이상 | 예 | CASES31개 모두 최소3개, 합계176; FINAL_VALIDATION 및 ACCEPTANCE_AUDIT. |
| 모든 사례 A 원 응답, B20개 이상 | 예 | A31/B31, 원 응답62개·후보342개; RUN_AUDIT.coverage, 원 파일 불변 해시. |
| 접두부 커밋이 gold 커밋보다 앞섬 | 예 | 8cb2b8e/c993618/ba1cc08 → f6f59a8의 Git 조상 관계와 prefix31 해시; FINAL_VALIDATION.prefixes. |
| 지정 표1–3의 열·내용과 미확인 확인 방법 | 예 | RESULT §1, 31×13·6×6·6×5; FINAL_VALIDATION.tables, REPORT_REVIEW 두 문맥. |
| Q1–Q8 출처2종류 이상 또는 실행 수치표+구체 사례 | 예 | 위 자기 점검8행, RESULT §2, 각 출처 원장과 실행. |
| 다른 분야의 독립 정답원 평가3건 원문 비교 | 예 | 특허 M05/M07, 법률 M09, 학술 M12와 보조 M06/M08/M10/M11; RESULT §3.3·CROSSFIELD. |
| 반례 다섯 가지의 실제 탐색 기록 | 예 | RESULT §3.4, SEARCH_LOG, selection 원장, REVERSAL/Q8_SUCCESSORS 및 URL 감사. |
| RESULT §4의 불일치·약점 정확히3건과 다음 조사 | 예 | 각 건에 문제/근거/결론 영향/질문·자료·최소 규모가 있음; FINAL_VALIDATION. |
| 사례 외20개 이상과 세부 자료 종류·사이트 상한 | 예 | 최소25·13사이트·최대3; 템플릿4·방법론6·타분야3분야·새 인용평가2·실제 리뷰토론5. SOURCE_COUNT 및 sources. |
| 같은 원 실행의 별도 채점 자료와 미해결 이견 보존 | 예(보존·공개; 합의 재심 미실시) | parallel-review-71d498d6556a의230파일 hash·342판정 쌍·62원 실행 불변 검증. gold 집합23행·라벨58행 차이와 대표5행의 unresolved_no_consensus를 공개했고, 주보고서 수치·기존 인수 판정을 유지. |
| SELF_CHECK 전체 인수 조건 통과 | **아니오** | SITE_CAP_CASES 한 건이 남는다. 연구 내용·산출물 검사는 통과했으나 사용자 규칙에 대한 예외 승인은 없으므로 차단 인계한다. |

HANDOFF 단독 커밋과 그 원격 본문 재열람은 이 파일의 커밋 다음에 수행할 마지막 절차다. 아직 발생하지 않은 commit SHA나 검증 결과를 이 파일에 성공으로 미리 기록하지 않는다. 최종 원격 본문 대조 결과는 실행 출력과 마지막 응답에서 알린다.
