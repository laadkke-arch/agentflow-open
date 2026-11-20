# AF-RES-013 — HANDOFF

- task_id: `AF-RES-013`
- branch: `work/research-af-res-013`
- owned_path: `docs/workstreams/research/AF-RES-013/`
- status: **BLOCKED — SITE_CAP_CASES**
- research_artifacts: 31사례·62실행·342후보 판정·RESULT·SELF_CHECK까지 커밋 및 원격 게시
- source_commit: `a18d8d2e1575d9b679442134fd0f6f8e17423bfe`
- resume_commit: `caa2a814727dd485ed0eb9bb8530d6b16fab9584`
- last_completed_bundle_commit: `0ba55c1f6c8522738592d8d71ef6f5dfd86338e7` (SELF_CHECK와 검증 원장)

## 1. 인계 상태와 차단 이유

**연구 내용·실행 기록·채점·보고서의 검증은 끝났으나, 전체 인수 조건을 통과했다고 보고하지 않는다.** 사용자가 정한 “같은 사이트 안의 페이지는 최대3개까지만 최소 개수에 넣는다”를 사례에도 문자적으로 적용하면 현재 고정판31개는 모두 GitHub 계열 호스트라3개만 산입되어 사례 최소30개가 미충족이다.

최초 SAMPLING은 이 상한을 비사례 자료에 적용한다는 해석을 사전 명시했다. 하지만 이는 작업자의 해석이며 사용자 승인된 예외가 아니다. 비사례25개·13사이트·최대3개 조건은 실제 충족했다. 사례의 출처를 같은 내용의 mirror로 바꿔 세거나 연구자 해석을 사용자 규칙으로 소급 승인하지 않았다.

`SELF_CHECK.md`의 전체 인수 판정은 BLOCKED이며 `evidence/FINAL_VALIDATION.json`은 `artifact_integrity=passed`, `strict_acceptance=blocked`를 구분한다. 이 파일은 **막히면 이유와 다음 첫 행동을 HANDOFF에 적으라는 사용자 지시의 차단 인계**다. 일반 완료 인계를 위한 SELF_CHECK 통과를 주장하지 않는다. 미해결 조건을 제외한 산출물은 모두 보존했고 기존 커밋·브랜치·원 응답을 초기화하거나 덮어쓰지 않았다.

## 2. 읽은 SHA와 실제 실행 위치

| 입력 | 읽은 SHA / 사용 범위 |
| --- | --- |
| 최초 source_commit | `a18d8d2e1575d9b679442134fd0f6f8e17423bfe`; manifest와 기존 분기 기준 유지 |
| 재개 시 foundation 최신 | `cc6ce55a261e5f3051c7fb9f203d846d65f64e75`; AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF 및 dot-control의 AF-RES-013 항목 |
| 재개 작업 브랜치 | `caa2a814727dd485ed0eb9bb8530d6b16fab9584`; PROGRESS·기존 커밋과 산출물부터 확인 |
| AF-RES-004 | `2b798c7d2b7355b649691c18de196104ceabb0f0`; HANDOFF·PROTOCOL v1.1의 L/E/H/T와 네 라벨 |
| AF-RES-009 | `7f627a81199f06da7f7b15f979e7fef25dd17602`; HANDOFF·GAP §2/§3/§5. 기존 LANDSCAPE 도구 선택 기록은 동결 실행규칙과 함께 유지하며35시스템 재조사 안 함 |
| AF-RES-011 | `478c301b693896e2c6d777f46ac441f071bfdfe8`; HANDOFF §6 입력 접두부 방법론만. 해당 스레드 재사용 안 함 |

이번 재개 실행 위치는 ChatGPT 공유 Linux Cloud workspace의 `/workspace/scratch/013b978f520f/agentflow-open`이다. 세션에 표시된 모델은 **GPT-6 Astra Pro**다. 내부 하위 에이전트 검토도 **내부 별도 검토**라고 표기하며 사람·다른 모델의 검토라고 부르지 않는다.

기준선 A31/B31의 최초 실행은 기존 원격 커밋의 원 응답과 로그에 보존되어 있었고 이번 재개에서는 재실행하지 않았다. 각 run은 접두부와 실행규칙만 입력으로 받은 새 문맥, `gold_seen=false`·`other_runs_seen=false`를 기록한다. 이번 검사는 그 파일·해시·시각·선행 커밋·원 응답 불변을 확인한 것이며 파일 접근 강제 격리나 모델 학습 기억 제거의 증명은 아니다. B의 번역자는 사람 대신 새 내부 문맥 모델이다.

공개 git fetch는 정상 동작했다. 일반 git push의 비대화식 인증은 사용할 수 없어 기존 GitHub 연결의 blob/tree/commit/ref 기능으로 게시했다. 매번 원격 tree와 로컬 staged tree가 같음을 확인하고 expected parent를 지정한 비강제 fast-forward로 같은 작업 브랜치만 전진시켰다. 로그인·권한 변경·force push는 하지 않았다.

## 3. Q1–Q8 결론과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계 |
| --- | --- | --- |
| Q1 | Rust·Python·Swift·KEP 모두 목적/대안 분리가 가능하며 템플릿 도입 이력도 확인했다. | 빈 절·리뷰 수정·혼합 Rationale가 있어 절 이름만으로 독립 정답이나 당시 입력을 보장하지 않음. |
| Q2 | 독립 제안31개·4계열, gold176개·각3개 이상, 엄격 채택 후 대체/부분 번복6개다. | 사례 사이트 상한을 문자 적용하면 최소수 산입3개로 미충족. 번호순 목적 표본이고 C31 선정 오류 복구도 공개. |
| Q3 | 역할 분포는 완성품0·부품17·같은 분야146·다른 생태계12·다른 분야1·표준논문0; 종류는 외부 실체30·구조146이다. | 역할과 종류는 별개 축. 분절·일치는 연구자 코딩이며 review-added 미확인169개를 false로 바꾸지 않음. |
| Q4 | 다른 분야 관계 전이는1/176(0.57%), 외부 다른 분야 자료 인용0/176이다. | 유일한 능동태→Event 필드 구조는 거절 대안이며 채택 효과 없음. 타 분야 수요·유용성의 모집단 추정 아님. |
| Q5 | A204후보의 역사 gold16/176(9.1%), 날짜 무관23/176(13.1%). | 공개 코드 endpoint200은14/31; 나머지 접근 실패/fallback. 날짜 pre/post/unknown103/22/79와 노출을 분리. |
| Q6 | B138후보의 역사 gold5/176(2.8%), 날짜 무관14/176(8.0%). | 사람 번역 평가가 아님. 카탈로그 연결의 pre/post/unknown37/34/67, live 문서의 과거 존재는 자동 인정 안 함. |
| Q7 | 정답 밖 문서상 유용 A170/178·B109/120, 그중 역사 근거 A83/B30. 근거부족21/342를 보존했다. | 대부분 좁은 부분 참고의 CONDITIONAL_TRANSFER이며 실제 구현·설계 효과·더 나은 완성품 성공 수가 아님. |
| Q8 | AF009의 H1/별도 UI 추가 가치를 기각하는 동등 이상 비교 조건은 아직 실행하지 않았다. | 새 절차·허용 오류·검토시간의 사전 비교가 없어 기존 조합 충분성이나 새 제품 우위를 입증/반박하지 않음. H2 유지 가치 미평가. |

A/B 합집합은 역사17/176(9.7%), 날짜 무관29/176(16.5%)다. 두 예산을 합한 사후 집계이며 단일 동일 비용의 새로운 run이 아니다. 다른 분야 항목의 A/B 적중은 각각0/1이다.

확정한 근접 오답과 가짜·다른 대상 링크는 각각0/342다. 이는 무오류·미래 링크 생존의 보장이 아니다. 후보 대부분이 원래부터 부분 참고로 한정되었고 미해결 연결은 INSUFFICIENT로 두었다. URL 대응 차이5행을 확인했고 C30 A3처럼 메타데이터만 열린 행을 본문 지지로 올리지 않았다.

## 4. 가장 강한 근거 3개

1. **실제 독립 제안 원천과 보존 실행의 연결:** 31개 고정 제안과176항목, 먼저 커밋된 prefix31, A/B 원 응답62개·502질의·342후보가 연결된다. prefix 최초 `8cb2b8e58f7d4278c11073956b31b30ad43aff18`, C14 정정 `c9936188a885848a16b55b4e11ac965bd2d0b204`, C31 추가 `ba1cc08705e4a1c56fcdb1a8062193ca4748992e`는 모두 첫 gold `f6f59a85949a001792b80260dd454c3fcc714a70`의 엄격 조상이다. 근거: CASES, PREFIX_MANIFEST, 원 runs, FINAL_VALIDATION.
2. **낮은 문서 항목 회수와 부분 참고 가치를 분리한 판정:** 역사 A16/B5와 날짜 무관 A23/B14, 외부 실체/구조 분모30/146을 별도 계산했다. 정답 밖 수를 gold에 섞지 않았고 경계36행 교차검토에서 과도한 구조 일치와 다른 기준선의 설명 보충을 실제로 취소했다. 근거: JUDGMENTS, AGGREGATES, ROOT_ADJUDICATIONS, RESULT §1–3.
3. **완전한 정답이라는 해석의 구체 반례:** C29 A4의2006 C# partial declarations는 원 gold에는 없지만 같은 타입의 선언 조각 사이 private 접근이라는 실제 후속 변경과 부분 대응한다. C05는 실제 구조 차용이나 외부 문헌 인용·채택 효과와는 다르다. 특허 CLEF-IP/NTCIR, 법률 COLIEE, 학술 인용 추천의 원문 비교도 관측 인용과 전체 관련성의 차이를 뒷받침한다. 근거: runs/A/C29.json, 후속 고정판, RV-C05-ACTIVE-VOICE, M05/M07/M09/M12, CROSSFIELD.

## 5. RESULT §4의 세 가지 핵심 약점과 다음 조사

1. **gold와 외부 검색 대상의 단위 불일치:** 구조 대안146개와 오래된 템플릿 시대 편중이 낮은 recall의 대안 설명이다. 다음은2018년 이후4계열×6사례=24사례를 외부 실체 중심/구조 중심12개씩 사전 고정하여 나누어 평가한다.
2. **현재 웹과 역사 증명·도구 접근의 차이:** 시간 unknown과 코드 검색 접근 실패가 함께 있다. 다음은 계열별3개, 총12사례×3반복에서 접근 가능한 검색과 고정 역사 corpus를 분리하고 동일 예산으로 비교한다.
3. **높은 조건부 참고 수와 실제 효용 사이의 공백:** 318/342가 조건부 전이이며 실제 적용0이다. 다음은12개 실제 설계 과제와 사전 오류/시간 기준, 적용 patch 또는 판단 기록을 확보하고 기존 A/B와 새 절차를 같은 예산에서 비교한다. 이 후속 제안은 실행했다고 보고하지 않는다.

## 6. 검증한 것과 미실시

**검증 완료:** 31사례·4계열·최소3gold·엄격 대체6, 31prefix 해시와 선행 조상, 62개 원 run 전체 바이트 불변,342후보 누락/중복/축/수치, 표1–3의 지정 열과31/6/6행, Q1–Q8 근거, 다섯 반례·세 타분야·§4 정확히3건, 로컬 보고서 링크, 출처 필드와 비사례 최소25개·13사이트·최대3, Git 계약/소유권·범위 밖 변경0·충돌0. SELF_CHECK 및 evidence의 FINAL_VALIDATION·RUN_AUDIT·SESSION_CHECK·ACCEPTANCE_EVIDENCE를 참조한다.

**미충족:** SITE_CAP_CASES 한 건. 사례에도 사이트당3개를 적용한 최소수는3/30이다. “조사 내용 검증 통과”를 “전체 인수 조건 통과”로 바꾸지 않았다.

**미실시 또는 범위 밖:** 실제 사용자·설계자 효과, D4 적용, 새 절차와의 비교, 실행 반복 분산, H2 변경 후 유지 가치, 모든 review-added 이력 복원. 이들은 원 보고서의 주장 한계이며 필수 데이터가 없는데 성공으로 채우지 않는다. 코드 변경이 없어 제품 테스트·배포는 하지 않았다. 공통 `scripts/check.py`가 범위 밖 산출물을 만들 수 있는 전체 제품 검사는 수행하지 않았다.

### 검증 재현 명령과 입력

아래는 저장된 결과를 검사하는 명령이며 기존 baseline을 재검색하지 않는다. 입력은 이 브랜치의 커밋된 CASES·prefix·runs·JUDGMENTS·RESULT·sources·SEARCH_LOG와 manifest다.

```bash
cd /workspace/scratch/013b978f520f/agentflow-open
python docs/workstreams/research/AF-RES-013/tools/analyze_results.py
python docs/workstreams/research/AF-RES-013/tools/audit_runs.py
python docs/workstreams/research/AF-RES-013/tools/validate_deliverables.py --phase self-check
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-013/manifest.json --fetch
git diff --check
```

첫 세 명령은 owned_path의 파생 검증 JSON만 재생성한다. 마지막 SESSION 검사에 네트워크·git fetch가 필요하다. baseline 원 파일은 수정하지 않는다. 새 후보 생성, 합성 문제, 저장·색인, 계정·유료 API·로그인·권한 변경·상시 실행은 하지 않았다.

역사 날짜 미확인 후보를 추가 확인할 때의 구체 입력은 각 JUDGMENTS 행의 candidate_url, 사례 decision_date, evidence_locations, remaining_check다. 예를 들어 C08 A1은 `https://www.inf.ufes.br/~raulh/ufes/teaching/courses/ds/haskell/haskell98-report/exps.html`의1999 원판 상세 list-comprehension 절과 cutoff2000-07-27을 대조해야 한다. 실패했던 mirror의 HTTP418/500을 우회하지 않는다. dated grammar만으로 상세 semantic 근거 날짜를 대신하지 않는다.

## 7. 원격 보존 커밋과 색인 제안

| 묶음 | 원격 커밋 |
| --- | --- |
| 기존 A31/B31 완료, 재개 기준 | `caa2a814727dd485ed0eb9bb8530d6b16fab9584` |
| 342판정·경계 교차검토·코딩 정정 | `df974def5425a343b16784f78c0641cac3ab4d33` |
| 최종 날짜 판단1행 일관화 | `eaa156ced81cc889990a2ce0e7749e43159bb71f` |
| RESULT·다른 분야 비교 종합·출처·질의 통합 | `3c11a5344d66edf6e6e0bb71bdb670dd2e8fbbe4` |
| SELF_CHECK·검증·차단 근거 | `0ba55c1f6c8522738592d8d71ef6f5dfd86338e7` |

| 색인 변경 제안 | 상태·내용 |
| --- | --- |
| AF-RES-013 | **BLOCKED(자료 사이트 상한의 사례 산입 문제)**; 연구 내용은31사례/62run/342판정과 A16/B5 역사 적중, 다른 분야 구조1/176을 보존. 실제 수정은 하지 않으며 진행 담당이 SELF_CHECK acceptance_evidence와 차단을 함께 옮길 것. |

## 8. 다음 첫 행동과 마지막 절차

**다음 첫 행동:** 진행 담당은 최초 SAMPLING 커밋의 비사례 한정 해석과 사용자 원문의 사이트 상한, FINAL_VALIDATION의 사례 호스트31개를 대조하여 인수 처리를 기록한다. 문자적 상한을 유지하면 최소10사이트의 적격30사례를 별도 사전 고정 절차로 확보하고 prefix→gold→A 전사례/B20이상 실행을 추가해야 한다. 현재 데이터의 출처 명칭을 바꾸는 것으로 해결할 수 없다. 질문·승인 요청을 보내지 않았고 dot-control·공통 색인·main은 바꾸지 않았다.

이 HANDOFF는 SELF_CHECK 커밋 다음에 **이 파일만 단독 커밋**한다. 그 커밋을 원격 브랜치에 반영한 뒤 GitHub에서 해당 SHA의 HANDOFF 본문을 다시 읽고 로컬 바이트와 같음을 확인한다. 자기 자신의 미래 commit SHA나 아직 수행하지 않은 원격 본문 검증 성공을 파일 안에 미리 적지 않는다. 최종 SHA·동일성·작업 트리 상태는 마지막 실행 결과와 응답에서 제공한다.
