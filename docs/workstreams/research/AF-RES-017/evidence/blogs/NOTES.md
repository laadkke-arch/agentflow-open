# Blog lane — intermediate collection checkpoint

수집자: 내부 별도 수집 lane, 세션 모델 표기 `GPT-6 Astra Pro`. 주 작업자의 coder-a 동결 전 수집이며 이 파일은 독립 coder-b 응답이 아니다.

첫 체크포인트는 **관측 10개**다. 엄격한 늦은 발견 사례는 B02 한 개이며 B01은 명시적 재발견이지만 결정·발견 월 및 생산 설계 변경이 부족하다. 나머지는 이미 알고 거절한 선택, 후발 대안, 되돌림을 비교하기 위한 통제 관측이다. 이를 엄격 표본 10개로 보고하면 안 된다.

## 가장 강한 양성

B02는 2006-12 원글, 2007-01 독자의 선행 논문 소개, 같은 달 저자의 하루 이식 보고, 2007-03 공개 릴리스, 1977-09 출판사 날짜가 이어진다. 2022 회고가 2007년의 성능 원인을 수정하기 때문에 회고 오류도 직접 비교할 수 있다. 다른 언어 OCaml의 Menhir가 발견 경로지만 실제로 이식한 것은 같은 컴파일러 분야의 Pager 알고리즘이다.

## 비용 분리

Linkerd의 172K/30K LOC, Pebble의 구현 크기, Airbnb React Native 코드 크기는 삭제한 코드가 아니다. 이 숫자를 낭비 LOC로 넣지 않았다. Indeed의 8개월은 종료 공지부터 종료까지, 2000+는 변경 대상 파일 수이다. Prezi의 'most of a year'와 Dropbox의 'weeks'는 정확한 숫자로 바꾸지 않았다.

## 네트워크

`nginx.org/en/CHANGES`: 익명 HTTP200, 2026-11-21T03:54:20.914386+00:00. `api.github.com/repos/pramalhe/ConcurrencyFreaks/git/trees/master?recursive=1`: 익명403. Blogspot Double Instance URL은 도구429; reviewer 글은 Google sorry로 이어져 읽지 못했다. 실패는 sources.excluded에 기록했다. Indeed 직접 urllib403 이후 허용된 웹 도구가 원문 본문을 반환했다.

## 한계 / 다음 단계

이 중간 파일의 official_target_description과 lexical_overlap은 아직 보강하지 않았다. 일부 초기 결정은 연만 알려졌고 발행일을 대신 넣지 않았다. 정당한 자체 구현 5개와 되돌림 3개 후보를 계속 확인하되, 모두 늦은 발견 양성이라고 강제하지 않는다. 공개 회고는 성공한 전환과 당사자 해석을 과대표집할 수 있다.
