# C11–C20 판정 회복 메모

판정자: **내부 별도 검토**. 실행 모델 표기: **GPT-6 Astra Pro**. 입력 커밋 `caa2a814727dd485ed0eb9bb8530d6b16fab9584`. 기준은 `SCOPE.md`, `JUDGING_RULES.md` 및 동결된 `cases/CASES.json`이다. 후보 이름뿐 아니라 각 run의 `raw_response`, `application_scope`, `constraints_or_caveat`, 실제 `opened_documents`를 읽었다. 기존 baseline을 다시 실행하거나 원 응답·접두부·정답을 수정하지 않았다.

## 범위와 수치

C11–C20의 gold 64개, A 후보 67개, B 후보 47개를 판정했다. `judgments.json`은 **114개 후보마다 정확히 한 행**을 갖는다. 전이 대상·필요 연결·실패 조건을 각 행에 명시했다. 날짜는 원 run의 `pre_decision / post_decision / unknown`을 그대로 보존했다. 새 원문 확인으로 역사 상태를 올리지 않았다.

| 구분 | A | B | 합계/의미 |
|---|---:|---:|---|
| 후보 행 | 67 | 47 | 114 |
| CONDITIONAL_TRANSFER | 62 | 40 | 102 |
| DIRECT_DOCUMENTED | 2 | 1 | 3 |
| INSUFFICIENT | 3 | 6 | 9 |
| gold가 하나 이상 일치하는 후보 행 | 8 | 6 | 14; 중복 후보는 gold 분모에 중복 가산하지 않음 |
| 날짜 무관 고유 primary gold | 7/64 | 3/64 | 원문 내부 구조 대안과 외부 실체 적중을 별도 필드로 구별 |
| 결정 전으로 확인된 고유 primary gold | 4/64 | 2/64 | A와 B를 합쳐 새로운 고유 gold를 더하는 계산이 아님 |
| 사후로 확인된 고유 primary gold | 0 | 1 | B C18 Python byte literal |
| 날짜 미확인 고유 primary gold | 3 | 1 | 역사 적격 실패나 사후와 동의어가 아님 |
| 정답원 밖 문서상 유용 후보 행 | 56 | 35 | 91; 제품 전체 해결·새 대안·더 나음·사용자 효용 검증이 아님 |
| 위 행 중 결정 전 근거 확인 | 33 | 11 | 44; A/B 간 중복 제거 전 후보 수 |
| 확인된 필수조건 위반 / 깨진·허위 반환 링크 | 0 / 0 | 0 / 0 | 좁은 제안 범위 안의 관측; 제외/실패 retrieval와 불확실성은 별도 |

| 사례 | gold 수 | A 후보 수 / 날짜 무관 gold / 결정 전 gold | B 후보 수 / 날짜 무관 gold / 결정 전 gold | 중요 판정 |
|---|---:|---|---|---|
| C11 | 10 | 9 / 1 / 0 | 6 / 0 / 0 | Go의 기본 비상속+명시 보존 구조 G03은 날짜 unknown. FD_CLOEXEC primitive를 선택적 Python API 정책과 혼동하지 않음 |
| C12 | 8 | 7 / 0 / 0 | 4 / 0 / 0 | PyPy method cache는 CPython tp_version_tag 실체와 다름 |
| C13 | 19 | 7 / 0 / 0 | 3 / 0 / 0 | Connection API 선례는 multiprocessing 모듈에 interpreter를 통합하는 대안과 다름 |
| C14 | 5 | 6 / 0 / 0 | 3 / 0 / 0 | 지연 callback/promise는 함수 지역 상태를 남기는 lambda 대안의 핵심 조건까지 회수하지 않음 |
| C15 | 3 | 5 / 0 / 0 | 3 / 0 / 0 | Builtin alias attribute는 재선언·Rust ABI 등가를 자동으로 뜻하지 않음 |
| C16 | 3 | 6 / 0 / 0 | 5 / 0 / 0 | 다른 언어의 국소 annotation은 구체 compiler scope 제약을 나눠 참고 부분으로 평가 |
| C17 | 3 | 8 / 1 / 1 | 7 / 1 / 1 | 기존 엔진 binding G02; 여러 C/C++ 엔진은 같은 gold를 반복 회수 |
| C18 | 7 | 7 / 3 / 2 | 4 / 2 / 1 | Python byte literal은 외부 실체; Go UTF-8과 Erlang numeric binary는 구조 대안 경계 |
| C19 | 3 | 6 / 0 / 0 | 5 / 0 / 0 | Whole boolean matches!는 custom syntax를 받는 procedural whole-match 대안과 다름 |
| C20 | 3 | 6 / 2 / 1 | 7 / 0 / 0 | L20n과 GNU gettext 실체만 일치; gettext-style 다른 구현은 실체 일치 아님 |

## 가장 중요한 경계와 반증

1. **Primitive와 정책을 구별했다(C11).** OpenBSD manual의 O_CLOEXEC는 descriptor의 kernel flag를 생성 시 설정한다. 이후 어느 라이브러리나 native extension이 exec를 호출하든 이미 표시된 fd에는 같은 규칙이 적용된다. 따라서 A1/A2의 H2 pass는 단순히 caveat가 있다는 이유가 아니라 OS 동작 근거에 기반한다. 반면 모든 native creator가 플래그를 쓴다는 전수 보장은 없으며 원 응답도 이를 주장하지 않는다. 생성 후 설정 race·협조 lock 우회·표준 스트림 예외는 조건에 남겼다. PEP433의 optional 인자/기본값 변경 대안은 이 primitive 하나와 동일하지 않다. 추가 확인: S03, S05, S12.

2. **같은 원리가 다른 실체를 맞힌 것은 아니다(C12).** PyPy의 type-version cache는 CPython `tp_version_tag`와 구현 프로젝트가 다르다. SELF·SwitchPoint·watchpoint도 별도 유용 선례이지 gold의 이름을 바꾼 답이 아니다. PIC 자체에는 dynamic rebinding 검사 보장이 없고, withcelldict 설정 페이지는 실제 mutation algorithm을 설명하지 않으며, seqlock은 concurrent snapshot 재검사와 장기 보관 cache 무효화의 차이가 있다. 이 세 A 후보와 RPython B3는 INSUFFICIENT다. S02는 이 판단의 반례 가능성을 재검토했으나 부족한 구현 근거를 채우지 못했다.

3. **격리 조심이라는 문구와 실제 경계 계약을 구별했다(C13).** A의 C API, per-module storage, Jep code, mod_wsgi, Tcl, Lua 및 B의 Lupa에는 state·namespace·copy·lifecycle 경계의 구체 열람 기록이 있다. B1 Jep은 clean README의 부분 격리 설명만 남고 자세한 비교 문서가 원 run에서 제외되어, Python-facing 값 교환/수명 계약 H2를 unknown으로 낮췄다. 일반 EIP Message Channel도 payload 소유권·teardown이 구체화되지 않아 INSUFFICIENT다. 같은 이름의 A Jep와 B Jep가 서로 다른 판정인 이유는 실제로 읽은 자료와 주장 범위가 다르기 때문이다.

4. **지연이라는 단어로 Python scope 보존을 추가하지 않았다(C14).** S06의 gold G01은 function-local state를 보존하려는 lambda 대안이다. SQLAlchemy callback, SRFI45 promise, Angular forwardRef는 지연 계산의 구조를 제공하지만 원 응답이 Python local/class namespace 보존의 동일 구조를 제시하지 않았다. 따라서 세 후보 모두 참고상 conditional이지만 G01 적중은 아니다. SQLAlchemy A2는 ORM 초기화 lifecycle·namespace-resolution 부분만 옮긴 원 응답 범위를 따라 H4를 not_in_scope로 제한했다. 내부 별도 교차검토에서도 ORM callable 결과의 class/column 제한을 확인하여 이 축을 좁혔다. S01은 arbitrary result·memoization을 확인하여 효용을 뒷받침하고 S10은 후속 PEP649에 필요한 추가 scope/descriptor 구조를 확인한다. 넓은 '어떤 deferred computation이든 lambda 대안' 규칙으로 바꾸면 A의 gold가 최대 1개 증가하지만 사전의 핵심조건 일치 규칙을 약화한다.

5. **Attribute와 redeclaration은 별도 조건이다(C15).** Clang builtin_alias가 선언과 compiler builtin을 연결하는 것은 맞다. S11은 특정 ARM/RISC-V intrinsic과 overload resolution에 제한되는 기능임을 확인했다. S07의 gold는 재선언을 계속 허용하거나 ABI 등가/coercion을 추가하는 설계다. B3 원 응답에 이 조건은 없다. B3는 frontend binding 부분의 조건부 참고만 인정하며 function value 증거는 `not_in_scope`다.

6. **Whole expression과 whole match language를 구별했다(C19).** matches!는 패턴 검사 결과를 boolean으로 노출하는 macro다. S08의 G03은 arbitrary arm/custom syntax를 처리하는 procedural macro 대안이며 generic topic 일치로 묶을 수 없다. LALRPOP/rust-peg/combine은 원 parser의 입력이 AST destructuring인지 token recognition인지 모르면 원 반복 match를 옮길 수 있는지 결정하지 못하므로 B3–B5 INSUFFICIENT다. 각 행의 `remaining_check`에는 필요한 실제 parser 범위 확인을 명시했다.

7. **C18 두 구조 적중은 민감도 경계다.** A4와 B1 Go는 byte-oriented string 설명 안에서 unescaped source code point가 UTF-8 bytes가 된다는 동일 변환을 실제로 언급하여 G07로 인정했다. A5 Erlang은 numeric byte constants를 binary pattern에 직접 쓰는 구조를 언급하여 G01로 인정했다. 이들은 다른 생태계 이름의 외부 실체 적중이 아니다. '추천의 중심 이유가 아닌 caveat에 등장한 구조는 제외'라는 더 엄격한 사후 규칙을 사용하면 A의 predecision gold는 4→3, B는 2→1로 변하고, A의 날짜 미확인 G01도 빠진다. 본판정은 원 응답이 실제 제시한 구조라는 사전 기준을 유지한다.

8. **부분 구현 선례의 제약 범위를 제한했다(C16·C17·C20).** Java SuppressWarnings와 C# block scope가 block+local 양쪽을 모두 지원한다고 확대하지 않고, 원 응답이 좁힌 한쪽 scope에서 평가했다. Regex prefix에 선형시간 의무는 없으므로 backtracking 엔진을 자동 오답 처리하지 않았다. Jed의 gettext-style API와 Boost.Locale catalogue 사용은 GNU gettext 실체 자체의 회수가 아니며 기능 확장으로 적중을 추가하지 않았다.

## 링크와 역사 근거

C14 A5의 candidate URL에 붙은 `#typing.TYPE_CHECKING`을 제거한 URL이 원 run `opened_documents`에 성공으로 기록되어 있다. `2017-10-03` footer와 TYPE_CHECKING 절을 읽었으므로 L=ok, 원래 pre_decision을 유지한다. fragment 차이를 가짜 링크로 세지 않는다.

114개 모두 원 run에 같은 문서 또는 fragment를 제거한 같은 URL의 성공 열람 근거가 존재한다. 이는 후보 원문이 열린 관측이며 현재·과거 판 동일성 보장은 아니다. 검색 중 제안서 snippet·기억 노출과 제외 페이지는 원 run에 유지되어 있다. 이 shard의 retained candidate-level leakage 확인과 run 전체의 무오염 여부는 별개다. 금지된 페이지를 제외했다고 run exposure가 사라지지는 않는다.

본 shard에서 새로 직접 읽은 경계/후속 자료는 `sources.json`의 S01–S13이며 요약과 한계만 저장했다. 같은 사이트 자료를 최소개수에 무제한 가산하지 않는다. 두 web 호출의 정확한 초는 남지 않아 UTC 날짜만 적었고 만들어 넣지 않았다. 후속 문서의 과도한 일괄 출력이 읽히지 않은 요청은 증거로 사용하지 않고 필요한 절을 재열람했다.

## Q8: 후속 방향을 찾았는가

기계적으로 합칠 수 있는 비교는 `Q8_SUCCESSORS.json`에 있다. **Primary gold 분모·적중에는 더하지 않는다.**

- C11은 채택 뒤 역전이 아닌 draft 교체다. A6은 비상속 기본과 explicit retained list의 방향을 찾았지만 역사 날짜가 unknown이다. A2는 원자적 constructor primitive를 결정 전 자료로 찾았다. 이것이 PEP446의 Python API 정책 전체를 예측한 것은 아니다.
- C12는 실제 명세 철회다. SELF의 write-triggered dependency invalidation은 결정 전 선례지만 CPython 3.11의 guard 변경·호환성·메모리 이유가 장래의 명세 철회를 일으킨다는 증거는 없다. PEP699는 write watcher를 가능한 필드 재사용의 예로 들고 미래 내부 구현을 확정하지 않는다(S09).
- C13은 draft의 핵심을 줄이는 후속 제안이다. Lifecycle handle과 메시지 선례는 찾았으나 Queue와 executor의 구체 계약이나 재설계 동기를 회수했다는 증거는 없다(S13).
- C14는 채택된 설계의 대체다. 결정 전 SRFI/SQLAlchemy/Angular 선례는 지연 계산 방향을 제공한다. 그러나 후속 PEP649가 2017년 lambda 기각을 재검토하는 핵심은 class/function-local scope를 처리하는 컴파일된 계산 함수와 descriptor의 연결이다. 원 baseline에 이 구체 연결이 없어 후속 설계를 이미 찾았다고 세지 않는다(S06·S10).

## 남은 한계와 판정을 바꾸는 최소 확인

이 판정의 큰 불확실성은 후보의 실제 사용자 효용과 gold 분절/구조 일치 판단이다. 동일 모델 내부 별도 검토이며 독립 사람 평가가 아니다. 91개 문서상 유용 후보가 91개의 새로운 대안이나 더 좋은 답이라는 뜻은 아니다. 좁은 참고 부분이 유용할 수 있다는 판단과 실제 통합·성능 성공은 구별된다.

INSUFFICIENT 9행은 C12 A4/A5/A6/B3, C13 B1/B3, C19 B3/B4/B5다. 모든 행에 부족한 알고리즘·boundary·원 parser 구조 중 무엇을 확인해야 바뀌는지 `remaining_check`로 적었다. 런타임 검증은 수행하지 않았다. 날짜 unknown은 동작 자료의 역사 고정판을 추가 열면 바뀔 수 있지만, 원 run의 상태는 별도 필드로 계속 남겨야 한다.


## C21–C31 추가 교차검토

`CROSS_REVIEW.json`에는 요청한 경계 8행과 Dart의 실제 rank를 확인하기 위한 C24 A1 추가 1행, 총 **9행**의 검토 제안이 있다. C21 A1/A3, C24 A1/A3/B2, C27 A2/A4/B1, C30 A3를 원 응답·열람 로그와 대조했다. 추가 원문 S14–S16을 직접 읽고 같은 sources/SEARCH_LOG에 넣었다.

- C24 A3의 H3를 not_in_scope로 좁히는 축 수정: 원 응답은 immutable case-class construction/copy 선례이며 hidden state는 별도 표현 설계라고 남겼다. Conditional과 Scala 외부 실체 적중은 유지한다. 원 shard 작성자도 동의했다.
- C27 A2의 구조 일치와 INSUFFICIENT 라벨 유지: `_` placeholder로 partial application하는 gold와 구조는 맞지만 label-only overload의 핵심 제약은 미확인이다. Forum 링크를 외부 제품 실체로 코딩한 CASES 분류는 명시적 구조 대안 교정이 필요하다.
- C30 A3의 G04는 본판정에서 제외 권고: counted NSString initializer라는 관련 component의 회수와 느린 Swift bridge를 빠르게 하는 대안의 회수를 구별한다. 더 넓은 component-retrieval 민감도로만 남기는 것이 SCOPE의 '이름만으로 일치 금지'와 일관된다. INSUFFICIENT 및 날짜 unknown은 그대로이며 역사 적격 적중 수에는 변화가 없다.
- C21 receiver qualifier는 실제 hidden receiver의 cv/lvalue/rvalue 구분 및 move 예제가 있어 제한된 접근 방식 선례로 인정한다. 이것이 single-use closure나 독점 borrow 보장을 자체 제공한다는 주장은 아니다. 세 C27 후보의 same-type/same-arity/different-label 연결 unknown은 유지한다.

교차검토 제안은 다른 shard의 원 판정 파일에 직접 반영하지 않았다. parent가 불일치와 민감도를 보존하며 통합할 대상이다.
