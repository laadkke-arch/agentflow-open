# AF-RES-100 진행·재개점

## 재개 확인

- 재개 원격 HEAD: `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f` (① 봉인).
- 재개시 통합 HEAD: `daf01339d0a81a3a8f19fad43b497480aa62515f`. 기존 시작판과 다른 경로는 중앙 진행표뿐이며 수정하지 않았다.
- 연구 입력 096 결과 `1d399f630930d2763459e16509c5224b0cded9a0`, 운영 의존/인계 `fce8d0ded93fe1f13f2c4978ed273c1ceef32934` 유지. 의존 원격 끝도 같다.
- PROGRESS와 ② 판정/접근 원장은 없었다. 기존 모집·조건·순위·32패킷을 다시 만들거나 바꾸지 않았다.

## 현재 묶음 — 동시 원격 갱신 반영

최초 상태 확인 이후 이전 세션이 ② `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`을 원격에 추가했다. 새 원격을 발견하자 이번 재개의 중복 독자 세 문맥을 즉시 중단하고, 그 접근/부분 판정은 `evidence/resume2/duplicate-reading/`으로 분리했다. 주32판정·주접근 원장은 새로 봉인된② 그대로 인수했다. ②를 반복하거나 재작성하지 않는다. 중복 관측을 독립 발견이나 주비용에 더하지 않는다.

누락된 임시 source cache만 고정 URL에서 복구했다. 3,488개 corpus file과 원 질문8개의 바이트 지문을 기존 원장과 대조했다. 캐시 다운로드는 문서 독해가 아니다. `restore_cache.py`는 성공한 봉인 원장을 수정하지 않는다. 첫 복구 시 jq 질문 schema 차이로 실패한 시도와 수리 결과는 `evidence/resume.json`에 남는다.

현재 ③ 공개 후속·밀려난 자료·타 분야와 별도 의미 검토를 `evidence/resume2/` 아래에서 진행한다. 공개 후속 독자는②가 원격에 존재함을 확인한 다음에 시작했다. 주지표 F: A만0/B만1/양쪽4/모두미완결2/비교불가1, S: A만0/B만0/양쪽0/모두미완결7/비교불가1. 의미 검토에서 불리한 근거가 나오면 원판정을 유지한 채 사후 민감도로 보존한다.

## 다음 첫 행동

최신 원격 SHA를 다시 읽고 마지막으로 커밋된 묶음 다음부터 진행한다. `evidence/resume2/outcomes/`, `crossdomain/`, `semantic-review.*`와 밀려난 자료 감사를 확인해③를 완성한다. 이미 완료된②의 독자 읽기를 반복하지 않는다. 기존 원장과 별도 검토의 시간·역할을 구분한다.

## 원격 기록

① `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f`: 기존 모집·조건·순위·패킷 봉인.

② `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`: 32초기판정·별도 근거가용성 감사·16쌍 봉인. 재개 커밋 `54ab626e9a558f0e442d74dad9697b787dec539b`은 e0 위에서 만들었으나 예상HEAD 불일치로 branch에 연결되지 않았다. 그 tree로 원격을 덮어쓰지 않았고, ②에 fast-forward한 뒤 재개 기록만 새 커밋에 싣는다. 상세 `evidence/resume2/concurrency.json`.

## ③ 완료·④ 시작

공개 후속 8건·5답·18댓글(30일)과 수정판을 별도 수집했다. 20 API 요청 실패0이며 사전 판정은 그대로다. 밀려난/추가한24자리와 직접 연 원문36파일의 후속 감사를 보존했다. 통합 source160행 중 최소개수 산입46개: 원 질문8, 주 공식16, 인접 공식10, 독립 상류시험5, 교차분야 공식5+fixture2. 후속 답/댓글 및 중복·빈 시험은 최소개수에서 제외한다.

③에는 `assemble_supplement.py`, `displacement.csv`, `outcomes.csv`, 확장 `sources.jsonl`, `evidence/resume2/{outcomes,crossdomain,semantic-review.*,postseal-access.jsonl,source-audit.md,supplement_annotations.json,failures.jsonl,docker-postseal.json,stage3-validation.json}`을 포함한다. 세 원장 검사는 종료0. ③ 원격 SHA는 다음 묶음 영수증과 최종 인계에 기록한다.

다음 첫 행동은 원격 SHA 확인 후 ④ 필수표·층별 분모·해석 민감도·SELF_CHECK를 원장에서 재계산하는 것이다. 사전 원장·모집·protocol은 바꾸지 않는다. 별도 의미 검토도 주 판정 변경0이다.

## 원래 작업 흐름과 병합 중

원래 작업 흐름의 ③ `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1`과 재개 흐름의 ③ `866ee7a68eec0f5c7077fec364685d6039d5ca75`를 함께 보존한다. 두 흐름 모두② 원판정 변경0이며, 원래 32자리·16쌍만 주 분석이다. 이 통합은 원래 흐름에서 수행하며 RESULT·SELF_CHECK·검사·최종 HANDOFF를 계속 작성 중이다. 중복 독자 로그는 계속 격리한다.

재개 흐름의 세 집계 원장 원본은 `evidence/resume2/seal3-ledgers/`에 그대로 남겼다. 통합 sources는303행의 읽기·귀속 기록이며, 최소자료 하한은 원래 감사한32고유자료만 산입한다. 재개160행의 원래 산입 여부도 보존하되 중복 합산하지 않는다. 원래 흐름의5답/4질문/현재채택3질문, 원판·완전입력·필수출력을 함께 확인한 실행0/8은 별도 기계 검토 중이며 실행 실패8건을 뜻하지 않는다.

## ③ 원격 저장 및 ④ 결과 재계산

③ 원격 SHA: `866ee7a68eec0f5c7077fec364685d6039d5ca75` (46파일). `evidence/resume2/seal3-receipt.json`에 변경 경로·blob과 lease 성공을 기록했다. CSV CRLF와 저장소 정규화 때문에 첫 로컬 fast-forward가 거부되어 로컬 복사본을 보호 stash에 남긴 뒤 공개된 원격판으로 fast-forward했다. 커밋/브랜치를 초기화하거나 덮지 않았다.

④ 초안은 필수3표·32자리·16쌍(비교가능14)·24교체자리·46고유자료·115인용 경계를 재계산했다. F B만1/양쪽4/미완결2/비교불가1, S미완결7/비교불가1, F→S손실9이다. 초기/사전변경0, 사후로 주판정수정0. P1helper/native 및 최초태그모집 민감도, J1/J2/P4 엄격조건 민감도를 분리했다.

공식자료 함수명 오기와 두 문서 링크를 수정했다. 외부 절의 긴 원문은 제거하고 URL/구간/hash/의역을 남겼다. 보조 CSV는 LF로 정규화했으나 원판정5파일은 봉인②와 바이트 동일하다. 세부 `stage4-corrections.json`, `crossdomain/audit-stage4.json`.

다음 첫 행동: ④ 결과판을 원격 커밋한 뒤 정확한 결과SHA에서 작업별 check --fetch와 공통 cloud_check를 실행한다. 공통 검사는 쓰기범위 안의 임시 checkout에서 실행할 수 있다. GitHub 결과판의 필수표·원증거·재현절차를 다시 연 뒤 HANDOFF.md만 마지막 단독 커밋한다. 결과판 검사 중에는 주원장을 수정하지 않는다.

## 재개 흐름의 ④ 최종화 조정

원격 병합 `82e21d89eb592769f6f44ed75c9937400a565641`을 fast-forward로 인수했다. 이 커밋은 원래 흐름③ `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1`과 재개③ `866ee7a68eec0f5c7077fec364685d6039d5ca75`를 모두 보존한다. 원판정5파일은 불변이다. 재개 흐름은 이미 작성·별도 검토된 RESULT/SELF_CHECK/재계산기를 끝내고 결과SHA 검사→GitHub 재열람→HANDOFF단독커밋 순서로 완료한다. 두 흐름 자료를 추가 실험 자리나 추가 독립 검증으로 세지 않는다.

최종 sources는 재개160행의 수리판 + 원래흐름143행(ORIGINAL-P3 접두사, 비산입) =303행이다. 최소 개수는 재개에서 원문·한계를 감사한46고유자료만 산입한다. 기존32산입은 다른 보수적 subset이며32+46으로 더하지 않는다. 82e의 세 집계는 해당 고정 Git 커밋에 보존돼 있으며 원래 개별조사 파일도 유지한다. 후속과 밀림의 최종 재현은 assemble_supplement.py, 필수표는 recompute.py를 사용한다. 이전 assemble_evidence.py는 원래③ 재현용이다.

## 원래 흐름의최종canonical인수

`b3f3694b54bb7a85dc7a21e2731841679fc6753c`의RESULT/SELF_CHECK/recompute/46자료계수를최종기준으로인수했다. 원래흐름은이를다시다른집계로덮지않고직접timeline재열람·60entity귀속대조·실행계획·원문반례·검사runner만추가한다. 두집합32/46은28개중복이며합산하지않는다. 초기사전32판정·16쌍은계속불변이다. 최종재현은assemble_supplement.py와recompute.py를사용한다. 이전assemble_evidence.py·원래source-summary는③계수기록이며canonical총량이아니다.

## 통합결과검사완료

보강결과SHA `8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9`에서실제작업별check --fetch와공통cloud_check --require-clean을실행해모두종료0이다. 공통sessions는no_active_sessions로개별작업검사를수행하지않았으므로AF100 manifest는별도직접검사했다. 최신fetch통합SHA는ace1a06a13ea435f5cb6a3e340ad24f03f68ecae,계약/소유범위오류0. 두검사는ownedcache안의동일SHA·clean checkout에서수행했다.

원격80e2d74의기존단독HANDOFF는이력과evidence/resume2/handoff-80e2d74.md에보존했다. 보강29파일후속을3ac381d후보로만든동안도착한이인계를덮지않고8b22a47의부모로연결했다. 최종인계는검사영수증이실린결과판을GitHub에서재열람한후다시마지막단독HANDOFF커밋으로완성한다. 주32판정·16쌍과46자료계수는불변이다.
