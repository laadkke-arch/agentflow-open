# NumPy 원문 판독과 범위 점검

## 결론과 직접 판독 범위

NEP1~20 번호순 원장을 기록했으며 첫 적격 소비자 과제는 N08이다. N08은 구매기록의 그룹 정체성 → 행 소속 → 네 집계 → 라벨 결과라는 작은 전체 흐름이다. 원 NEP의 새 API 채택 정책 전체를 평가하지 않는다. 선정 봉인의 원문은 [selection-freeze.md](selection-freeze.md), 과제 입력·정답·의사코드는 [cases.json](cases.json), 개별 직접 열람은 [sources.jsonl](sources.jsonl)에 있다.

고유 외부 원문 최소수에 보수적으로 산입한 것은 8개다: 첫 복구 제안 1, 당대 공식 문서 파일 3, 공개 테스트 파일 2, 후속 논의 2. 동일 파일의 여러 함수·댓글과 1.4.x HTML 렌더를 별개 원문으로 늘리지 않았다. 다른 NEP 머리말·탈락 후보 초기판·git 이력은 원장에는 남기되 최소수에는 산입하지 않았다. 모든 counted=true 문서는 해당 위치를 직접 읽었다. checks timestamp는 자료 재대조 후 원장 기록 시각이다.

## 원판·당대 대안과 독립 기준

N-S01의 최초 추가 commit은 2010-04-29이며 본문 날짜는 2010-04-27이다. 더 이른 공개 메일에서 같은 초안을 입증하지 못했으므로 earliest_recovered, first_public_unverified를 유지한다. N-S09에서 v1.4.0 tag와 2009-12-28 commit을 확인했다. 제공 링크 3개는 이 고정 source 버전이다. 후대 빌드된 공식 1.4.x HTML을 당시 공개판으로 소급하지 않았다.

두 방법은 이름만 다르지 않다. G1은 키 정렬에 따른 값을 함께 재배열하고 연속 구간을 감소한다. G2는 고유키의 역색인으로 원래 위치에서 각 그룹을 골라 감소한다. G2에서 빈도만 세는 bincount로 수량 합/최소/최대가 모두 생긴다고 주장하지 않는다. 두 방법 모두 세 grouping과 네 통계를 끝까지 제공해야 한다. 테스트 N-S05는 실제 비정렬 반복 입력과 역색인 기대값을 가지며 N-S06은 구간 합 감소를 별도로 검사한다. 그러나 둘은 구매 집계 전체의 공식 정답표가 아니며 같은 NumPy 프로젝트에 속한다. 카드-기준의 파일 독립성은 있고 프로젝트/기관 독립성은 없다.

## 최초 결론을 깨는 경로

후속 #7265 원글과 6개 댓글을 읽었다. 순서가 이미 정렬된 경우와 정렬/그룹 색인 생성까지 포함한 경우의 비교는 다르고, NaN 의미와 데이터 복사는 실행시간 비교도 바꾼다. 이 기록은 카드가 빠른 함수를 가리킨다는 이유만으로 종단간 선택/준비 노동이 줄어든다고 볼 수 없음을 뒷받침한다. 해당 게시 실행시간은 사람 시간으로 사용하지 않는다.

댓글 200538631의 groupby2_1d 및 groupby4_1d는 키를 정렬한 뒤 원순서 값의 구간을 줄인다. 원 작성자의 단조 linspace 시험은 그 오류를 가린다. 일반 비정렬 입력에서 깨진다는 것은 본 연구의 코드 판독 추론이다. 유지관리자가 확인한 오류라고 쓰지 않는다. cases.json의 BAD1은 이 실패 형태를 채택하며 입력은 연구자가 별도로 작성한 구매행이다. t0 상품 AA의 참 합은 16, 잘못된 절차는 14다. t1에서 같은 6행 순서만 바꾸면 잘못된 절차의 AA 합은 15로 바뀌지만 참 합은 16이다.

#834에서는 반복 경계의 동작을 기존 계약으로 유지하자는 입장, 빈 CSR행, 겹치는 구간, 새 start/stop API 요구를 읽었다. 원 ticket 자체는 2006이므로 빈 그룹이라는 요구가 역사적으로 후대에 처음 생겼다고 말하지 않는다. 단지 N08의 관측 구매 그룹 원요구 밖인 조건으로 분리한다. 빈 그룹의 min/max·NaN·대형 수치 정밀도·성능·여러 연도 해석을 t1에 추가하지 않았다.

## 노출·정정

- 현재 NEP 목차의 final/deferred/rejected 상태와 NEP1~20 머리말, NEP1/10/12/19 일부 이력을 선택 전에 보았다. 완전히 눈가림된 전향 표집이라고 주장하지 않는다.
- 초기 번호별 탈락 사유는 잠정 판독 후 첫 복구판을 다시 읽어 확인했다. NEP1~7의 추가 git 추적은 N08 봉인 후 보강이었다. 제외를 소급해 더 강한 최초판 확실성으로 바꾸지 않았다.
- 2026-11-22의 정정: selection-freeze는 월을 연월이라고 적었지만 원문은 by month여서 연도 경계를 정하지 않는다. 원 문구를 보존하고 아래 correction note를 붙였다. t0/t1 모두 year=2010이며 month와 (year,month)를 모두 허용한다. 선정 분모 20, 선정 1, 예시 3, 요구 3은 변하지 않는다.
- BAD1은 키-값 대응의 주 오류 하나다. 네 통계 연산 자체는 있다. 예상 R2=partial, R3=fail이며 다른 판독자가 R2=fail로 볼 경우 연산 의미와 완성 출력의 판정 범위를 실제 불일치로 기록해야 한다. 단일 주 원인의 파급을 두 독립 결함으로 과대계수하지 않는다.

## 실패 주소·검색 범위·다음 확인

1. 최초 공개 메일: search query `site.mail.python.org/pipermail/numpy-discussion "group" "April" "2010" "reduceby"` 및 `"numpy" "reduceby" "2010"`. 현행/후대 NEP와 재인용만 확인했고 동일 2010-04-27 초안 메일은 찾지 못했다. GitHub doc/neps/groupby_additions.rst history의 최초 추가판으로 대체했다. 다음 첫 자료: https://mail.python.org/archives/list/numpy-discussion@python.org/ 의 2010-04-27~30 Travis Oliphant groupby 제안 thread와 본문.
2. GitHub 이슈 검색 첫 호출에 is:issue가 없어 422였다. `https://api.github.com/search/issues?q=repo%3Anumpy%2Fnumpy%20groupby%20is%3Aissue&sort=created&order=asc&per_page=30`으로 고쳐 20개 이슈 제목을 보고 #7265, #834 본문을 직접 읽었다. 검색 결과 스니펫 자체는 count 제외다.
3. NEP1은 doc/npy-format.txt가 2008-08-23 source-tree 이동이어서 2007 첫판까지 미복구다. 다음 자료는 해당 commit의 이전 경로와 2007 mail archive. N08 선정 적격 여부의 근거로 쓰지 않았다.
4. NEP5는 wiki import commit이어서 원 wiki 작성일 미확인. 다음 자료는 scipy.org/scipy/numpy/wiki/GeneralLoopingFunctions의 공식 보존 이력. 거기에 두 대안이 있다고 가정하지 않았다.

## 실행과 미확인

이 분담에서 실행한 것은 JavaScript의 단순 키별 모음으로 6행의 정답 숫자와 BAD1 출력 대조를 계산한 탁상 점검이다. 사람이나 역사적 NumPy 실행을 흉내내지 않았다. 1.4.0의 공식 테스트는 읽기만 했다. 필요하면 후속 담당이 Python 2.x와 NumPy 1.4.0 환경에서 `numpy/lib/tests/test_arraysetops.py::TestAso.test_unique`, `numpy/core/tests/test_ufunc.py::TestUfunc.test_reduceat_shifting_sum`을 실행할 수 있으나 이는 이번 사람시험 준비도에 새로 합의된 필수 실행 게이트가 아니다.

정답 자료는 참가자에게 제공하지 않는다. root는 cases.json의 participant_common, t0.records, t1.records, cards에서 참가자 파일을 만들고 references/examples와 후속 issue URLs는 채점 자료에만 둔다. 별도 문맥 판독과 사람 간 합의는 아직 이 분담에서 수행하지 않았다. 사람이 수행한 값은 없음이며 시간은 미확인이다.

## 최종 작성자 수치 점검 보강

JavaScript 정답 작성 후 Python 3의 별도 두 절차 구현으로 동일 수치를 다시 확인했다. G1/G2 각각 t0/t1의 28/28 통계 셀이 단순 키별 모음 참조와 같다. BAD1은 t0 17/28, t1 24/28 셀이 다르다. 행 자료와 원래 수량은 두 시점에서 동일하다. 이 수치는 작성자 자기점검이며 다른 채점자나 사람 결과가 아니다. 원인 R3 하나의 파급을 통계 셀 수만큼 오류 사건으로 세지 않는다. 세부 stdout은 author-check.json에 기록했다. 역사적 NumPy 1.4.0 환경은 실행하지 않았다. JSONL의 내용 없는 마지막 행을 제거했으며 근거·후보·예시 분모는 바뀌지 않았다.

## 추가 연대 반증 · 공식 archive 직접 열람

웹 도구의 URL open은 실패했으나 shell urllib는 mail.python.org의 공식 April/May thread를 HTTP200으로 읽었다. 제목 groupby만 찾으면 놓친다. 저자별 제목을 따라 4/10 'Proposal for new ufunc functionality'의 의견수집과 4/12~13 후속 논의를 직접 읽었다(N-M01~05). 저자는 정식 proposal/patch 이전 논의라고 쓰고 실제 group-by/segment 기능을 제시한다. 4/12는 비연속 반복키 [0,1,0,1,2,0,0,2,2]에 대한 합 [17,6,22]를 원 저자가 직접 설명한다. 4/13에는 문자열키를 정수라벨로 바꾸는 구성도 원 용도를 보존한다고 판단한다. 이는 R3 근거를 강화하고 'git 추가가 절대 최초 공개제안'이라는 해석을 반증한다. 원래 earliest_recovered 경고를 삭제하지 않고 formal NEP 첫 복구판과 사전 공개 논의를 분리했다.

4/27~30의 formal 문서 게시를 더 좁혀 확인하기 위해 공식 April mbox504개에서 해당 Date69개를 골라 본문 groupby|reduceby|group-by|groupby_additions|purchases를 검색했다. 일치한 한 건은 4/28 recarray grouping 방법 메일(N-M06)로 NEP 게시메일이 아니었다. 69개 전체를 직접 읽었다고 세지 않는다. 정식 구매사례 문서의 절대 첫 공개 시각은 여전히 미확인이다. April.txt.gz는404였고 archive root의 실제 Text 링크 April.txt로 대체했다. old mail.scipy.org 주소는503이었으며 mail.python.org에서 성공했다.

새 메일 여섯 개와 archive조회 세 개를 sources에 남겼지만 같은 제안 thread/보충 탐색으로 모두 counted=false다. 핵심 고유원문8·후보20·선정1·예시3은 그대로다. 이 추가 판독은 선정 뒤의 연대·반증 보강이며 선택을 순수 전향적으로 만들지 않는다. 마지막 원장을 통합할 때 sources의 새 행과 cases/frame의 chronology amendment를 포함해야 한다. 다음 최소 자료는 4/29 git commit의 원 SVN 공개 로그 또는 이 formal NEP 링크를 실제로 게시한 당시 목록 메시지다.
