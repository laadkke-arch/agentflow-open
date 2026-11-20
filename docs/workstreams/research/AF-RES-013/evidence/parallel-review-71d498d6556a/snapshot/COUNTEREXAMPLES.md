# 반례 탐색과 판정 경계

이 파일은 처음 가능한 결론을 뒤집으려 한 실제 탐색을 묶는다. 원 질의·열람 시각·실패는 `SEARCH_LOG.json`, `evidence/counterexamples/SEARCH_LOG.json`, 각 `runs`의 원 기록에 있다. 별도 반례를 찾았다고 사전 동결한 31개 사례나 176개 정답 항목의 존재·동일성을 바꾸지 않았다. C05-G06의 역할 오류 정정은 최초 값과 함께 별도 기록한다. 사례 밖의 의도적 반례는 빈도 분모에 더하지 않는다.

## 1. 비교 절은 항상 쓸 수 있는 정답원인가

**그렇지 않다.** 번호순 스크리닝은 비교 항목 3개 미만·절 부재·빈 템플릿을 실제 제외했다. [KEP265 고정판](https://raw.githubusercontent.com/kubernetes/enhancements/ebf37575297a991155890e7f1fae7c62bbee7ca0/keps/sig-network/265-ipvs-based-load-balancing/README.md)의 Alternatives는 `None`뿐이다. [KEP177](https://raw.githubusercontent.com/kubernetes/enhancements/ebf37575297a991155890e7f1fae7c62bbee7ca0/keps/sig-storage/177-volume-snapshot/README.md)은 안내 주석만 남아 있다. [Rust RFC90](https://raw.githubusercontent.com/rust-lang/rfcs/f43d5789b838fb0d80962e3d4b45fb9ddfcc9a07/text/0090-lexical-syntax-simplification.md)은 Summary·Motivation·Detailed design·Drawbacks 뒤에 독립 비교 절이 없다. 출처 ID는 CE-K265-EMPTY, CE-K177-EMPTY, CE-R90-MISSING이다.

찾는 과정 자체의 반례도 보존했다. `site:github.com/rust-lang/rfcs "Alternatives" "None."` 결과에서 보인 RFC438·1300을 직접 열자 `None`은 Unresolved questions 소속이었다. 두 문서의 실제 Alternatives에는 각각 ad-hoc grammar 처리, wrapper coercion·변경하지 않기 등의 대안이 있었다. 검색 snippet을 정답원 품질의 근거로 쓰지 않았다(CE-R438-FALSE-POSITIVE, CE-R1300-FALSE-POSITIVE).

이것은 빈 절의 존재 증거다. 전체 제안서에서 빈 절의 비율, 저자가 대안을 전혀 검토하지 않았다는 주장, 리뷰 전체에 대안이 없다는 주장은 아니다. `SAMPLING.md`의 목적 표본과 전체 모집단을 구별해야 한다.

## 2. 본문에 없는 후보는 무용한가, 더 나은가

**본문 불일치와 무용성은 같지 않다.** 예를 들어 C23의 A는 C11 포인터-정수 변환 계약·LLVM 포인터 태그 구조 등 주소 조작을 설계할 구체 참고를 냈고, B는 C11과 mask merge를 실제 카탈로그 경로로 찾았다. 본문 정답은 `intValue` 메서드, 포인터 타입의 모든 연산 API, 복잡한 작업을 C에 넘기는 선택이다. C의 계약을 Swift에 옮기는 것은 마지막 선택과 다르므로 이 후보를 정답 적중으로 올리지 않았다. 원 응답의 좁은 적용·실패 조건을 유지한 L/E/H/T 판정과 정답 일치를 분리했다.

리뷰 원문도 본문의 유한성을 보여 준다. C22와 C28의 본문 밖 리뷰 항목은 7개이며 DRF/DataRaceFree 별명을 중복 제거하면 신규 항목 6개다. 따라서 본문 176개를 리뷰까지 확장한 구별 항목은 182개다. 이것은 새 검색 결과의 주관적 유용성 판정과 별개인, 원문으로 확인한 본문 누락의 작은 하한이다. 리뷰가 모든 관련 선례를 망라한다는 뜻도 아니다.

추가 비사례 리뷰 M27에서는 기존 `Pod` 부품을 리뷰어가 제시하고 제안자가 size/alignment 검사와 변환 방향을 대조했다. 실제 검토의 구체성을 보여 주지만, 이 추가 사례를 176개 또는182개 분모에 포함하지 않는다.

정답원 밖 후보의 최종 분모·분자는 `RESULT.md` §1–3과 `evidence/AGGREGATES.json`에서 후보 단위와 사례 단위로 따로 보고한다. 문서 조건을 통과한 참고 후보가 실제 결정을 개선했다는 사용자 증거는 없다. **‘더 나은 선례를 발견했다’는 강한 반례는 미확인(동일 설계 과제에서 기존 대안과 추가 후보의 제약·검토시간·결정 수정 효과를 비교해야 함)**으로 남긴다. 유용한 누락 후보를 더 좋은 해법으로 바꾸어 쓰지 않는다.

## 3. 뒤집힌 결정을 처음 입력만으로 예상할 수 있었는가

추적 단위는 후속 문서의 명시 이유와 원 응답의 실제 추천이다. 이미 알고 있는 후속 문서를 입력에 넣거나, 후보 문서의 모든 내용을 사후에 원 응답으로 간주하지 않는다. 채택 후 변경 6건과 초안·기각 후 대체 3건을 `REVERSALS.md`에 분리한다.

핵심 대조는 C07의 빈 입력 처리, C12의 dict 버전 필드 유지 필요성 변화, C14의 지연 평가 범위, C21의 closure capture 추론, C29의 같은 파일 extension 접근, C31의 배포 버전 표기 확장이다. 관련 원리를 발견한 것, 후속 결정을 촉발한 이유를 언급한 것, 미래 요구 변화를 예측한 것은 서로 다른 결과다. 모든 후속 링크는 `cases/CASES.json`의 `superseded_by`에 고정했다. 그 후속 자료 자체를 결정 전 적중으로 계산하지 않는다.

## 4. 잘못된 링크를 실제로 내었는가

모든 원 응답의 후보 URL과 열람 기록을 `tools/audit_runs.py`로 연결하고, 정확한 URL이 없는 행은 별도 내부 검토자가 문서·fragment·redirect를 직접 재확인했다. 확인 근거는 `evidence/judgments/*sources.json`에 남겼다. A-C14 rank5의 TYPE_CHECKING fragment는 base 문서와 같은 대상을 가리키는지 추가 확인한 예다. 단순 문자열 불일치를 다른 대상 링크로 판정하지 않았다.

검색·열람 중 403·DisabledError·timeout·일부 404는 `excluded`와 원 실행에 남아 있다. 이 실패를 출력 후보의 가짜 링크 수로 합산하지 않는다. 최종 후보의 404/410, 존재하지 않는 대상, 다른 문서를 가리키는 경우와 도구 접근 실패를 구별하는 `link_status`가 채점 근거다. 전체 URL을 미래에도 열 수 있다고 보장하지 않는다.

## 5. 다른 분야 원리는 모두 장식인가

**실제로 설계 선택에 쓰인 반례가 있다.** 표본 밖 [RFC8289 CoDel](https://www.rfc-editor.org/rfc/rfc8289.html)의 §3.3은 큐가 선형·시불변·단일입출력이라는 전제를 만족하지 않아 고전 PID를 직접 적용하기 어렵다고 설명한다. 이어 상태공간 제어와 확률적 적응을 선택하고 §5.6의 역제곱근 drop 일정으로 연결한다. 제어공학의 원리와 실패 전제를 네트워크 큐로 옮긴 설계 판단이며 단어 차용보다 강하다(CE-CODEL). 제어공학과 네트워크 소프트웨어의 분야 경계에는 연구자 판단이 개입한다.

반대로 [PEP433 고정판](https://raw.githubusercontent.com/python/peps/0efb6d7b3ec34a093a341551d7209aaf6e9dff2b/pep-0433.txt)의 `sterile`은 파일 디스크립터 상속 매개변수 이름 후보를 생식 관련 용어로 설명한다. 생물학의 메커니즘·구조·성능 전제를 가져오지 않는다(CE-TERM-P433). Rust RFC123 리뷰의 Clojure atom 비유도 이번 비교에서는 명명의 직관이며 원자물리학 원리 전이가 아니다(R-REVIEW-123).

**표본 안의 구조 차용은 초기 분류를 바로잡게 했다.** C05의 K0383-G06은 자연어 능동태의 active component·direct/indirect object 관계를 event field에 대응시켜 자동 소비자가 필드의 대상을 해석하도록 하는 schema 대안이다. 인간 소비를 우선한다는 이유로 기각되었으므로 단순 장식과 같지 않다. 최초 코딩은 외부 언어학 문헌 인용이 없다는 점까지 들어 같은 분야 설계로 보았지만, SCOPE §5에는 그런 필요조건이 없다. 원문을 읽은 내부 별도 검토와 작업자의 재대조로 **다른 분야 원리**로 정정했다. 최초 role·boundary_note는 CASES에 보존했고 [정정 원장](evidence/ROLE_CORRECTIONS.json)에 변경 이유·시점을 남겼다.

정정 후 주 집계는 **1/176(0.57%)**, KEP **1/34(2.94%)**, A/B 회수 모두 **0/1**이다. 이는 외부 언어학 논문이 실제 인용되었다는 주장이나 기계 이해 효과의 실증이 아니다. 최초 동결값0/176과 그 회수율0/0(정의 불가)도 보존했다. 같은 runtime의 profiling에서 optimization으로 이동한 PySizer까지 먼 분야로 넓히면 **2/176(1.14%)**, 모두0/2다. 이는 분류 민감도이며 신뢰도 실험·모집단 추정이 아니다. [root 재열람](evidence/judgments/VERIFICATION.json), [내부 별도 검토](evidence/judgments/SECOND_REVIEW.json).

따라서 ‘다른 분야에서 얻는 것이 없다’는 초기 강한 해석은 지지되지 않는다. 반대로 의도적으로 찾은 CoDel을 더해 표본 빈도를 높이지 않는다. term-only 사례도 설명상 도움이 될 수 있지만 실제 설계자 효과는 관측하지 않았다.

## 한계

반례 탐색은 목적 지향적이며 모집단 비율 추정이 아니다. 결과가 없는 질의도 보존했고, 원문을 열지 못한 결과는 본문 근거 수에서 제외했다. 각 기준선은 단회 실행이며 재시도하면 다른 후보가 나올 수 있다. 정답원 밖 후보의 유용성은 연구자 문서 판정이고 실제 적용은 하지 않았다. 반복·사용자 효과·정답원 전체 완전성은 후속 조사 대상이다.
