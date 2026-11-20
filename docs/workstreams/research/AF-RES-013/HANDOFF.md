# AF-RES-013 — HANDOFF

- task_id: `AF-RES-013`
- branch: `work/research-af-res-013`
- owned_path: `docs/workstreams/research/AF-RES-013/`
- status: **BLOCKED — SITE_CAP_CASES**
- source_commit: `a18d8d2e1575d9b679442134fd0f6f8e17423bfe`
- last_completed_bundle_commit: `8470805fc3a57d9f8e314e21e97c2c3c8898061b` — SELF_CHECK·검증·차단 근거 보완
- primary_judgment_commit: `eaa156ced81cc889990a2ce0e7749e43159bb71f`
- parallel_review_commit: `8f25019fd4c51b1dd81d0e4a58677e2de22b1216`
- additional_unresolved_analysis: 동일342후보의 일치 집합23행·라벨58행 차이에 대한 전수 합의 재심 미실시

## 1. 인계 상태와 차단 이유

31사례·4계열·정답176항목·A31/B31의 원 응답62개·후보342개와 보고서, 출처, 자기 점검을 원격에 보존했다. **산출물 무결성은 통과했지만 전체 인수 조건은 통과하지 않았다.**

사용자의 “같은 사이트 안의 페이지는 최대3개까지만 최소 개수에 넣는다”를 사례에도 적용하면 현재 고정판31개는 모두 GitHub 계열 호스트여서 **3/30개**만 최소수에 산입할 수 있다. 비사례25개·13사이트·사이트당 최대3개 조건은 충족한다. 최초 SAMPLING은 상한을 비사례에 적용한다고 기록했지만 이는 작업자의 해석이며 사용자 승인된 예외가 아니다. 같은 내용을 mirror로 바꿔 세거나 이 해석을 사후 승인된 규칙으로 바꾸지 않았다.

이 HANDOFF는 **막히면 이유와 다음 첫 행동을 적고 끝내라는 사용자 지시에 따른 차단 인계**다. SELF_CHECK의 `artifact_integrity=passed`와 `strict_acceptance=blocked`를 구별한다. 일반 완료 인계를 위한 전체 SELF_CHECK 통과를 주장하지 않는다.

추가로 같은 원 실행을 다른 작업공간에서 채점한 결과가 발견되었다. 기존 원격 주판정을 유지하고 별도 원본·비교·대표5행 검토를 [비교 부록](evidence/parallel-review-71d498d6556a/README.md)에 보존했다. 정답 일치23행과 라벨58행이 달라 **주표의 숫자는 해당 판정판의 기술값이며 판정자 간 합의값이 아니다.** 어느 한쪽 전체를 정답으로 확정하거나 평균으로 합치지 않았다.

## 2. 읽은 SHA와 실제 실행 위치

| 입력 | 읽은 SHA / 사용 범위 |
| --- | --- |
| 고정 source_commit | `a18d8d2e1575d9b679442134fd0f6f8e17423bfe`; AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·RESEARCH_BRIEF·AF-RES-013 항목 및 최초 분기 기준 |
| AF-RES-004 | `2b798c7d2b7355b649691c18de196104ceabb0f0`; HANDOFF·PROTOCOL의 L/E/H/T와 네 라벨, 처음부터 좁힌 참고 범위 원칙 |
| AF-RES-009 | `7f627a81199f06da7f7b15f979e7fef25dd17602`; HANDOFF·GAP §2/§3/§5와 LANDSCAPE의 기준선 도구 범주.35시스템 재조사 안 함 |
| AF-RES-011 | `478c301b693896e2c6d777f46ac441f071bfdfe8`; HANDOFF §6 입력 접두부 방법론만. 그 스레드 재사용 안 함 |
| 원 실행 보존판 | `caa2a814727dd485ed0eb9bb8530d6b16fab9584`; A31/B31 원 응답·실제 질의·열람·실패 기록 |
| 발견한 원격 후속판 | `eb569f07a3a34ffacf114384ae9b06ad062f5396`; 기존 커밋·PROGRESS·HANDOFF·RESULT·SELF_CHECK·판정 및 코딩 정정을 읽고 유지 |
| 추가 검토·현재 자기 점검 | `8f25019fd4c51b1dd81d0e4a58677e2de22b1216`, `8470805fc3a57d9f8e314e21e97c2c3c8898061b` |

이번 보존·대조·마감 실행 위치는 ChatGPT 공유 Linux workspace의 `/workspace/scratch/71d498d6556a/agentflow-open`이다. 세션에 표시된 모델은 **GPT-6 Astra Pro**다. 기존 원격 후속판의 실행 위치는 그 HANDOFF에 기록된 `/workspace/scratch/013b978f520f/agentflow-open`이며 두 작업공간을 혼동하지 않는다. 검토자는 **작업자 / 내부 별도 검토**로 표기한다. 사람 또는 다른 모델의 검토라고 부르지 않는다.

이번 대조 단계는 기존62개 baseline을 다시 실행하지 않았다. 최초 run의 접두부·실행규칙만 제공한 새 문맥 및 gold 미열람 표기를 보존했으며, 모든 원 run의 바이트가 caa2a814와 같음을 검사했다. 이 기록은 물리적 파일 접근 격리나 사전학습 기억 제거의 증명이 아니다. B는 사람 대신 새 내부 문맥 모델의 카탈로그 번역이다.

처음 준비한 원격 ref 갱신이 expected-parent 불일치 상황에서 실패한 뒤 fresh fetch로 기존 후속판을 확인했다. 그 판을 덮지 않고 후속 커밋으로 부록을 추가했다. 기존 GitHub 연결의 blob/tree/commit/ref 기능을 사용했고 각 원격 tree가 로컬 staged tree와 일치함을 확인했다. force push·로그인·권한 변경을 하지 않았다. `0cc0fc15c650f8d3ec551202ffe4dbdcef335898`은 ref에 반영하지 못한 준비 commit이며 완료 기준 SHA로 쓰지 않는다. 그 내용과 추가 미커밋 자료는 모두8f25019의 snapshot으로 보존했다.

## 3. Q1–Q8 결론과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계 |
| --- | --- | --- |
| Q1 | Rust·Python·Swift·KEP 모두 목적과 대안을 분리할 수 있고 템플릿 절 도입 이력을 확인했다. | 빈 절·혼합 Rationale·리뷰 중 수정·시대 차이가 있어 절 이름만으로 독립성과 당시 입력을 보장하지 않음. |
| Q2 | 독립 제안31개·4계열, gold176개·각3개 이상, 채택 후 대체/부분 번복6개를 확보했다. | 사이트 상한을 사례에도 적용한 최소수는3/30으로 미충족. 번호순 목적 표본이며 C31 선정 오류 복구도 공개. |
| Q3 | 역할은 완성품0·부품17·같은 분야146·다른 생태계12·다른 분야1·표준논문0이다. | 주판정의 외부 실체/구조 종류는30/146. 별도 snapshot의34/142에는4항목 종류 정정이 반영되지 않았다. 역할과 종류는 별개 축. review-added169개는 미확인으로 유지. |
| Q4 | 정답 집합의 다른 분야 관계 전이는1/176(0.57%), 외부 다른 분야 자료 인용은0/176이다. | 유일한 능동태→Event 필드 구조는 거절 대안이다. 채택 효과·수요·모집단 빈도를 입증하지 않음. 초기0/176과 넓은2/176 민감도도 별도 보존. |
| Q5 | A31회·204후보: 주판정은 날짜 무관23/176, 결정 전16/176; 별도 채점은22/176·16/176이다. | 동일 run의 판정 차이이며 추가 실행 아님. native code endpoint200은14/31이고 나머지는 접근 실패·fallback. |
| Q6 | B31회·138후보: 주판정은 날짜 무관14/176, 결정 전5/176; 별도 채점은8/176·2/176이다. | 카탈로그+내부 모델 번역 조건이며 사람 번역 성능이 아님. 출처에만 있는 기능·명명 의미·구조 일치의 경계가 수치를 바꿈. |
| Q7 | 주판정의 정답 밖 문서상 유용 후보는 A170/178·B109/120이며 gold 적중과 분리했다. | 별도 채점은 A146/178·B105/126. 라벨58행·근접 오답0대12의 이견이 남는다. 실제효용·완성품 성공·합의 점수로 해석하지 않음. |
| Q8 | 기존 조합의 실제 관측은 생겼지만 AF009의 H1/UI 추가 가치를 기각하는 동등 이상 비교 조건은 실행하지 않았다. | 새 절차·허용 오류·검토시간의 사전 비교와 실제 적용이 없다. 낮은 회수율만으로 기존 조합의 무용성이나 새 제품 우위를 판단할 수 없고 H2 유지 가치도 미평가. |

주판정 A+B 합집합은 날짜 무관29/176·결정 전17/176, 별도 채점은24/176·16/176이다. 각각 두 예산을 합친 사후 집계이며 단일 동일 비용 run이 아니다. 양쪽 모두 다른 분야 항목의 A/B 적중은0/1이다.

주판정의 확정 가짜·다른 대상 링크는0/342이며 별도 채점도0/342다. 필터링된 최종 후보에 관한 관측으로, 검색 과정의 실패나 모든 링크의 미래 생존·무오류를 뜻하지 않는다. 날짜·원문·조건 불충분은 각 판정의 remaining_check와 excluded 기록에 남겼다.

## 4. 가장 강한 근거 3개

1. **원천·입력·실행의 추적 가능성:** 고정 제안31개와176항목, 먼저 커밋한 prefix31개, A/B 원 응답62개·342후보가 연결된다. prefix의 세 commit은 모두 최초 gold f6f59a8의 엄격한 조상이며, 대조 단계에서 원 run62개 전체 바이트 불변을 확인했다. 근거: CASES·PREFIX_MANIFEST·RUN_AUDIT·FINAL_VALIDATION.
2. **같은 실행에서 드러난 판정 경계의 크기:** 같은342행 중 일치 집합23행·라벨58행이 다르다. 대표5행에서는 좁힌 참고 범위에 전체 제약을 적용한 문제와, 출처에만 등장한 기능을 회수한 항목으로 센 문제가 양쪽에 있었다. 이는 한 점수만으로 정밀한 제품 우위를 말할 수 없다는 직접 근거다. 근거: 비교 부록의 COMPARISON·REPRESENTATIVE_REVIEW·원 run·동일 SCOPE/004.
3. **관측 인용과 완전한 관련성의 차이:** CLEF-IP/NTCIR·COLIEE·학술 인용 추천의 원문 비교와 실제 설계의 review-only 추가 항목, C29의 C# partial 선언 참고를 함께 확인했다. 정답 밖 참고가 있다는 것과 실제로 더 좋은 결과를 냈다는 것을 분리한다. 근거: M05/M07/M09/M12, CROSSFIELD, RESULT §2–3, runs/A/C29.json.

## 5. RESULT §4의 핵심 약점 3건과 다음 조사

1. **gold 단위와 검색 대상의 불일치:** 주판정 gold176개 중 구조 대안146개이고 Rust8개는 명시 Prior art 절 도입 전이다. 현대의 외부 선례 중심 문서에서도 누락이 유지되는지 최소24사례(4계열×6), 외부 중심/구조 중심12개씩 사전 고정하여 비교한다. 현재 낮은 recall을 제품 일반 성능으로 확대하지 않는다.
2. **현재 웹·역사 증명·도구 접근의 혼합:** 주판정 날짜는 A103/22/79·B37/34/67(pre/post/unknown), 코드 endpoint 성공은14/31이다. 최소12사례×3반복에서 접근 가능한 검색과 고정 역사 corpus를 동일 예산으로 비교해야 탐색 실패와 당시 판 증명 실패를 나눌 수 있다.
3. **조건부 참고와 실제 효용, 판정 이견의 공백:** 주판정318/342는 조건부 전이이고 실제 적용0이다. 추가 비교의23개 일치·58개 라벨 차이를 원 응답과 고정 규칙으로 먼저 재심한다. 그 뒤 최소12개 실제 설계 과제와 사전 오류·시간 기준, 적용 patch 또는 판단 기록으로 기존 A/B와 새 절차를 비교한다. 이번 부록은 이 재심이나 실제 효용 실험을 수행한 결과가 아니다.

## 6. 검증한 것과 미실시

**검증 완료:** 31사례·4계열·각3gold·채택 후 대체6; prefix31 해시와 선행 조상; 원 run62개 전체 바이트 불변;342후보 키·축·수치; 지정 표1–3의 열과31/6/6행; Q1–Q8 근거; 다섯 반례·세 타분야·§4 정확히3건; 보고서 로컬 링크; 비사례25개·13사이트·최대3; owned_path 범위 밖 변경0·충돌0. 주보고서의 표 셀은 기존 원격판과 동일하다.

**추가 보존 검증:** snapshot230파일·4,752,466bytes의 hash와 크기, compact342판정과62개 상세 파일의 값, 원 출처 보조 원장1335열람 기록·제외342건을 검사했다. 이 수는 중복 가능한 열람 기록이며1335개 독립 자료나 최소수로 세지 않는다. 별도 원장의 최소수26/14사이트와 주원장의25/13사이트는 산입 집합이 다르므로 합산하지 않는다. 차이는 M25·M27 대 PS-R-S21-LENS다. snapshot의 SELF_CHECK와19개 data gate는 당시 예비 상태이며 현행 인수 판단을 대체하지 않는다.

**실제 재검사:** 주 `validate_deliverables.py --phase self-check`와 부록 `validate_snapshot.py`가 무결성 통과·전체 인수 차단을 출력했다. `workbench.session check ... --fetch`는 exit0, passed, remote_checked, 범위 밖0·충돌0을 반환했다. 해당 원 기록은 부록 SESSION_CHECK.json에 있다. 이 검사는 사이트 상한이나 채점 이견을 해소하는 검사가 아니다.

**미충족:** SITE_CAP_CASES 한 건 — 문자적 최소수3/30. **추가 미해결:** 같은 후보의 일치23행·라벨58행 전수 재심. 대표5행 검토를 전수 합의로 부르지 않는다.

**미실시 또는 범위 밖:** 실제 사용자·설계자 효과, D4 적용, 새 절차 비교, 반복 분산, H2 유지 가치, 모든 review-added 이력 복원. 코드·제품·배포·공통 색인은 변경하지 않았으며 새 유료 API·계정·로그인·권한 변경·예약 실행을 하지 않았다. 범위 밖 파일을 만들 수 있는 전체 제품 검사는 수행하지 않았다.

## 7. 검증 재현 명령과 필요한 입력

현재 작업공간에서의 재현 명령이다. baseline을 재검색하지 않으며 첫 네 명령은 현재 owned_path의 파생 보고서/검증 원장만 재생성한다. 입력은 이 브랜치의 CASES·prefix·runs·JUDGMENTS·RESULT·sources·SEARCH_LOG·manifest와 비교 부록 snapshot이다.

```bash
cd /workspace/scratch/71d498d6556a/agentflow-open
python docs/workstreams/research/AF-RES-013/tools/analyze_results.py
python docs/workstreams/research/AF-RES-013/tools/audit_runs.py
python docs/workstreams/research/AF-RES-013/evidence/parallel-review-71d498d6556a/validate_snapshot.py
python docs/workstreams/research/AF-RES-013/tools/validate_deliverables.py --phase self-check
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-013/manifest.json --fetch
git diff --check
```

채점 재심의 구체 입력은 `evidence/parallel-review-71d498d6556a/COMPARISON.json`의 baseline·case_id·rank·fields, 해당 `runs/<A|B>/<id>.json`의 원 응답, 고정 접두부, CASES의 gold/필수 제약,004 PROTOCOL이다. 우선 대표 B-C27-r1, A-C31-r1, B-C09-r3, B-C24-r2, B-C22-r1을 읽으면 양방향 문제를 확인할 수 있다. 전체23/58행을 재심하기 전 어느 쪽 수치도 합의 점수로 승격하지 않는다.

역사 시점 확인은 각 candidate_url·decision_date·remaining_check를 입력으로 claim-bearing 과거 release/commit/판을 대조한다. 예를 들어 C08 A1의 Haskell98 list-comprehension 상세 의미 절과 cutoff2000-07-27을 대조해야 한다. 실패한 mirror의 차단을 우회하거나 dated grammar만으로 상세 의미의 날짜를 대신하지 않는다.

새 사이트 표집에는 기존 SAMPLING·SOURCE_COUNT의 호스트 분포, 최소10개 사이트의 적격 사례 목록·고정판·결정일·3개 이상 비교항목이 필요하다. 먼저 새 절차를 커밋하고 새 prefix→gold→A 전사례/B20이상 순서를 지켜야 한다. 현재 링크 명칭 변경이나 사후 mirror 추가로 대체할 수 없다.

## 8. 원격 보존 커밋과 색인 제안

| 묶음 | 원격 커밋 |
| --- | --- |
| SCOPE·SAMPLING 사전 고정 | `4398d0beed321e9de19e0268fdfcfb09aef2a19c` |
| 최초 prefix30 / C14 날짜 정정 / C31 추가 | `8cb2b8e58f7d4278c11073956b31b30ad43aff18` / `c9936188a885848a16b55b4e11ac965bd2d0b204` / `ba1cc08705e4a1c56fcdb1a8062193ca4748992e` |
| 최초 gold·템플릿 | `f6f59a85949a001792b80260dd454c3fcc714a70` |
| A31 완료 / B31 완료 | `0e7b6c34a3e490f94355048563979defe3bbf45b` / `caa2a814727dd485ed0eb9bb8530d6b16fab9584` |
| 기존342판정 / 날짜1행 정정 | `df974def5425a343b16784f78c0641cac3ab4d33` / `eaa156ced81cc889990a2ce0e7749e43159bb71f` |
| 기존 RESULT / SELF_CHECK / 차단 HANDOFF | `3c11a5344d66edf6e6e0bb71bdb670dd2e8fbbe4` / `0ba55c1f6c8522738592d8d71ef6f5dfd86338e7` / `eb569f07a3a34ffacf114384ae9b06ad062f5396` |
| 병렬 채점 원본·비교·주보고서 이견 고지 | `8f25019fd4c51b1dd81d0e4a58677e2de22b1216` |
| SELF_CHECK·검증·차단 근거 보완 | `8470805fc3a57d9f8e314e21e97c2c3c8898061b` |

| 색인 변경 제안 | 상태·내용 |
| --- | --- |
| AF-RES-013 | **BLOCKED(SITE_CAP_CASES)**;31사례/62run/342판정과 다른 분야 구조1/176을 보존. 주판정 A16/B5 역사 적중에는 별도 채점 A16/B2 및 일치23·라벨58행 이견을 함께 표시. 실제 공통 색인 수정은 하지 않으며 SELF_CHECK의 미충족과 이견을 함께 인계. |

## 9. 다음 첫 행동과 마지막 절차

**다음 첫 행동:** 최초 SAMPLING의 비사례 한정 해석과 사용자 사이트 규칙, 실제31개 호스트 분포를 대조하여 인수 상태를 기록한다. 문자적 규칙을 유지하면 별도 사전 선정으로 최소10사이트의 적격30사례와 필요한 실행을 확보해야 한다. 이어서 새 우위 주장 전에 비교 부록의23개 일치·58개 라벨 차이를004의 같은 규칙으로 재심한다. 질문·승인 요청을 보내지 않았으며 dot-control·공통 색인·main은 수정하지 않았다.

이 파일은 자기 점검 보완 커밋 다음에 **HANDOFF.md만 단독 커밋**한다. 그 SHA를 원격 브랜치에 반영한 뒤 GitHub의 고정 SHA 본문을 다시 읽어 로컬 바이트와 비교한다. 자기 자신의 미래 SHA나 아직 수행하지 않은 원격 대조 성공을 이 파일에 미리 적지 않는다. 마지막 SHA·원격 본문 동일성·작업 트리 상태는 실행 출력과 최종 응답에 제공한다.
