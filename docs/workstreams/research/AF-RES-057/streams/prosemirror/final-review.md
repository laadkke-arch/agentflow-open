# ProseMirror 최종 초안 사실 대조

- 기록 UTC: 2026-11-23T03:49:34.794823+00:00
- 검토 주체: `/root/prosemirror`, ProseMirror 자료 취득·재생을 수행했던 같은 모델 분담자. 독립 사람 또는 최초 노출이 없는 별도 예측자는 아니다.
- 요청 범위: 최종 초안의 ProseMirror 원사건/연구 변형 구분, opA/opB·undo/redo·이력 상태, 노출 한계, 수치와 인용 파일 경로.
- 수행 범위: 아래 네 초안, 봉인 `predictions.csv`의 PM 9행, `streams/prosemirror/observations.json`, 기존 `replay/results.json`·`replay/historical/results.json`, 이미 취득한 원전의 해당 API·예제·시험 행을 다시 읽었다. 기존 파일의 데이터 대조만 수행했다. 새 제품 실행·추가 인터넷 취득·봉인 파일 수정은 하지 않았다.
- 시작 시각을 별도 계측하지 않아 소급한 시작 UTC는 기록하지 않는다. 이 검토 파일의 기록 시각과 대상 해시로 검토 대상을 특정한다.

## 판정

**PM 사실·출력·분모에 결과를 바꿀 오류를 발견하지 못했다.** 아래 명시된 최종 작성 단계 보완 사항을 제외하면, 공개 원진단 기대값·사후 작성자/수정 기록·연구자 보조 실행을 구분하고 추가 적중을 제한하는 현재 PARTIAL 판정과 일치한다. 이는 Yjs/지도/회계 원전 전체를 독립 재검증했다는 뜻이 아니다.

## 실제 검토한 주장과 근거

| 초안 위치 | 대조 내용 | 결과와 한계 |
| --- | --- | --- |
| RESULT L12–14, L27, L45, L65 | PN1 #892의 명시 목표는 선택25..30/RangeError이고, 상대 텍스트 보존은 추론이다. 역사 기준 history1.0.3은 작성자의 실제 설치판 확정이 아니다. synthetic metadata bool 대조는 실제 rebase 결함 개입과 다르다. | 정확히 구별되어 있다. 봉인 원사건 판정은 판별 불가, 연구 보조 정상 A만·역순 둘 다이다. 엄격 명시 텍스트 감도의 PN1 제외도 유지한다. |
| RESULT L12–14, L106; observations CSV 데이터행 PN1-A/E/D | 정상 opA는 `abcdefghijklmnopqrstuvwxyz0123456789R`, opB는 `abcdefghijklmnopqrstuvwx3456789`; redo는 모두 `abcdefghijklmnopqrstuvwx3456789R`. 역순에서는 동일 복원 텍스트여도 undoDepth A0/B1이다. | 기존 replay와 일치한다. 이 synthetic 실행의 selection은1..1이며, 원문25..30 복원 성공으로 세지 않은 것이 맞다. |
| RESULT L15–17, L28, L65, L67, L107; observations CSV PN2-A/E/D | history.undo와 undoInputRule은 서로 다른 취소 범위의 명령이다. 즉시 opA는 빈 문단, opB는 세 점. opB 뒤 history.redo는 false/dispatch0이다. 뒤 x가 있으면 opB부터 false/dispatch0으로 `…x` 유지한다. | 전부 기존 replay와 일치한다. opB redo와 boundary opA 세부가 봉인 당시 보류였음을 유지한다. 후속 댓글의 추천/이해 진술을 정확 텍스트의 작성자 실행 증거로 높이지 않는다. |
| RESULT L18–20, L29, L47, L73, L99 | PT1 첫 `enables undo` L31–38은 a,b 후 undo→빈 문단만 선언한다. 원군에는 opB/redo가 없다. 다음 별도 시험 L40–47의 redo→ab를 별개 근거로 설명한다. | 원전 행과 맞는다. 연구의 preserve-a 목표·closeHistory 조작·remote-b·redo 확장도 명시되어 있다. |
| RESULT L18–20, L41, L73, L99, L143 | PT1의 별도 E multilevel 예제 전체를 먼저 읽어 그룹 a+b→빈 문단이 의미적으로 노출됐다. | 공개 독해 진단으로 남기고 새 적중을 인정하지 않아 정확하다. 원군의 직접 assertion 취득 시각은 봉인 뒤03:32:31.973Z이나, 그 순서만으로 무노출이 되지 않는다. |
| RESULT L111 | 작성자 JSON trace와 유지보수자 축소 회귀의 역사 core 출력 구별 | 작성자 trace는1.0.3 Position22 오류/1.0.4 `123456789ABCED`·6..15, 축소 회귀는 Position21 오류/`123456789ABCDE`·6..13으로 정확하다. 두 텍스트·선택을 합치지 않는다. |
| RESULT L101, L113, L145, L151; comparison-counts main/posthoc | PM 봉인12변형과 사후6변형은 별도다. 사후6개는 later-core 회귀2개와 역사 core4개이다. | PM 총18기록, 구판 오류3기록이 맞다. wrapper exit0을 모든 제품 실행 성공으로 해석하지 않는다. 신규 실행은 하지 않았다. |
| RESULT L99, L146; comparison-counts public_CI | 정확 SHA의 status/check-runs/actions에서 확보된 기록0과 공개 CI 통과 미확인 | 적절하다. status 응답의 pending/빈 배열을 실제 실패나 실행 중으로 판정하지 않았다. 원 upstream runner 실행은 미실시로 남겨도 맞다. |
| final-counts L76–87, L130–153 | PM 시험군을 한 suite로, issue/fix/repro를 한 사건으로 보수적으로 합친다. #984의 원인/교정 두 패치를 두 작업으로 세지 않는다. #892 요청과 수정의 할당을 중복하지 않는다. | PM50출처행/22고유 계보가 일치한다. 별도 수정 사건은 #892/#984/#1311의3개이며, 불중복 최소 배당의 수정군에는 #984/#1311의2개만 들어간 것이 맞다. |

PM API와 예제 인용 행도 취득 원본으로 확인했다. history1.0.3 `src/history.js` L373–375는 addToHistory=false 제외, inputrules1.2.0 L105–107은 마지막 동작 조건, history1.5.0 L363–366은 closeHistory의 그룹 분리이다. E 인용은 history1.0.3 L83–86,1.3.0 L52–57,1.5.0 L54–58로 실제 창과 일치한다. PN1 E의 `oops!` assertion은 L87의 창 밖 선노출이며, PT1의 a+b→빈 문단은 별도 예제 L59의 창 밖 선노출이다.

## 파일 및 원장 대조

- root `observations.csv`의 PM9행(헤더 포함 줄11–19)의 normal opA/opB 및 boundary JSON을 `replay/results.json`에 저장된 해당 case/variant/op 객체와 대조했다. **불일치0**이다. 세 보기의 반복은 독립9실행이 아니라 같은 PM3사건의 재표현이다.
- 봉인 `predictions.csv`의 PN1/PN2/PT1 각각에서 E와 D의 choice, opA/opB undo, opA/opB redo, preserved_other_edits, normal_prediction, boundary_prediction의8개 필드가 같다. **PM 동일3/3·상이0/3**이다. 전체6자리의 나머지3자리는 이번 검토의 재판정 범위 밖이다.
- root CSV PM9행의 raw_observation_file/research_run_file 경로는 모두 존재한다. RESULT의 고유 로컬 링크47개를 확인했으며 PM 링크 누락은 없다.
- 검토 시 RESULT의 `SELF_CHECK.md`, `evidence/acceptance-evidence.json`, `evidence/audit-final.json` 세 링크 대상은 아직 생성 전이었다. 이는 root가 후속 작성 중인 파일이며 완료 전 경로의 존재와 내용 일치 확인이 필요하다. 이 검토는 그 미래 파일 내용을 승인하지 않는다.

## root에 전달한 보완 사항

1. RESULT 마지막 약점 표 L161의 `자연6자리`는 **전체6자리/자연4자리**로 교정해야 한다. root가 이미 인지한 오기이며 새로운 연구 결과 수정은 아니다.
2. observations.csv `exposure_status`는 봉인 시점의 문자열을 보존한다. PN1의 “No selectedtest assertions ... read”와 PT1의 “original L31 assertions still not opened”는 현재까지 안 읽었다는 뜻이 아니라 **봉인 시점 상태**임을 필드 설명 또는 접두어로 명확히 하면 좋다. 동행 public_test_declared에는 사후 열람 사실이 올바르게 기록돼 있다. 봉인 predictions/cards를 수정할 이유는 없다.
3. 위 세 작성 중인 root 산출물을 생성한 뒤 링크를 최종 확인해야 한다. PM 부분에 추가 제품 실행은 필요하지 않다.

## 검토 대상 내용 해시

| 파일 | SHA-256 |
| --- | --- |
| `RESULT.md` | `fecfdeb5aaa628648fd76afe021a91e3f3b98477af564bd79707162616fa4c09` |
| `observations.csv` | `bc6df0e7d73e5f7b7470e785d7022b2d4de985890d17e9ae7c7fe35bf19cd56b` |
| `evidence/comparison-counts.json` | `5286a9702f1f408a6d5f1638215590c3ceaa43afb0362aad1f3d707437a613a1` |
| `evidence/final-counts.json` | `68d0fb4177d497d869bb0470a8cee0366e153c9175d9378739d1ed6b60dae126` |

이후 root가 수정한 판은 위 해시와 다를 수 있다. 이 파일은 위 초안과 지정 PM 근거를 실제로 본 범위를 기록하며, 최종 원격 SHA 재열람이나 세션 계약 검사를 대신하지 않는다.
