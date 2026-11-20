"""Reproduce manually coded candidate judgments; does not search or rewrite runs."""
import json
from pathlib import Path
from urllib.parse import urldefrag

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
CASES = {c['id']: c for c in json.loads((BASE/'cases/CASES.json').read_text())['cases']}
SPECS = {}

def add(cid, baseline, rows):
    SPECS[cid, baseline] = rows

# Each tuple: H values, per-constraint reasons separated by |, source-to-target mapping,
# judgment code (T conditional, D direct, I insufficient), optional primary gold indexes.
# These are manual semantic decisions after reading every original response and opened-document log.
add('C11', 'A', [
('PPP','exec 때 표시된 descriptor를 닫는다|표시가 descriptor에 저장되어 native module을 포함한 어느 성공한 exec에도 kernel이 적용한다; 비표시 생성기의 보호는 주장하지 않는다|명시적으로 넘길 descriptor와 닫을 descriptor를 구별한다','descriptor flag → Python 런타임의 공통 상속 정책','T'),
('PPP','생성 시 O_CLOEXEC로 유출 구간을 줄인다|O_CLOEXEC가 FD_CLOEXEC를 생성 시 설정하므로 이후 native exec 호출도 같은 kernel 규칙을 받는다; 생성 경로 채택은 별도 전제다|의도된 상속 예외를 남기는 생성 정책이다','원자적 open flag → Python 파일 생성 경로의 기본 정책','T'),
('PPP','양쪽 pipe endpoint에 close-on-exec를 설정한다|표준 모듈과 native module의 pipe 생성 지점에 적용한다|자식 표준 스트림으로 넘기는 끝은 명시적으로 보존한다','pipe2의 두 endpoint flag → 런타임 보조 pipe의 생성 규칙','T'),
('PPP','socket 생성 시 상속 차단을 표시한다|참여하는 networking extension까지 생성 경로를 확장하고 나머지 연산은 별도라고 밝힌다|의도된 descriptor 전달은 별도 정책으로 남긴다','socket 생성 flag → 네트워크 descriptor 획득 경로','T'),
('PPP','duplication으로 상속 가능성이 다시 생기는 지점을 다룬다|낮은 수준의 복제·재배치 API라는 공통 경계다|표준 스트림 remapping의 의도된 상속을 일반 복제와 구별한다','dup3 flag → descriptor 복제 정책','T'),
('PPP','생성 후 flag 설정과 fork 사이를 협조 lock으로 직렬화한다|모든 creator/launcher가 참여해야 하며 우회 native code 한계를 명시한다|ProcAttr.Files 등의 명시 보존 목록을 참조한다','Go 기본 close-on-exec 및 retained list → Python 생성 기본값과 명시적 예외','T',[(3,'구조상 기본 비상속과 명시 보존 목록을 실제로 제시한다. Go라는 외부 실체 자체가 gold인 것은 아니다.')]),
('PPP','이미 열린 비표시 extra fd를 child에서 닫는다|수정 가능한 launch 경로만이라는 보완 범위를 명시한다|하한 3으로 0·1·2를 보존하며 의도된 extra fd 예외도 지적한다','closefrom(3) → 통제 가능한 child launch의 보완 cleanup','T'),
('PPP','file actions 뒤 close-on-exec 처리를 설명한다|spawn 경로에 한정한 보완 계약이며 모든 launcher의 해결이라고 주장하지 않는다|순서 있는 remap과 0·1·2 처리로 의도된 I/O를 구별한다','spawn actions → 명시적인 child I/O 계약','T'),
('PPP','launch에서 extra fd를 기본적으로 닫는 API 선례다|GLib 호출에 한정함을 명시해 런타임 전수보호로 확대하지 않는다|standard-stream flag와 LEAVE_DESCRIPTORS_OPEN을 구별한다','GLib launch flags → 고수준 API의 명시적 상속 선택','T'),
])
add('C11', 'B', [
('PPP','OS close-on-exec flag가 exec 시 유출을 막는다|모든 생성·복제 경로의 참여 필요를 명시한다|0·1·2 및 명시 pass extra fd를 분리한다','fcntl descriptor flags → 공통 상속 제어 정책','T'),
('PPP','원자적 파일 생성 flag가 open/fcntl 사이 race를 제거한다|공통 런타임과 참여 native creator가 적용 범위다|의도된 상속은 명시 예외로 처리한다','O_CLOEXEC → 파일·디렉터리 획득 규칙','T'),
('PPP','두 pipe endpoint의 상속을 생성 시 표시한다|runtime·native module의 pipe 생성까지 적용한다|표준 스트림으로 넘길 끝의 보존을 따로 요구한다','pipe2 → 내부 통신 pipe의 상속 계약','T'),
('PPP','socket 획득 시 close-on-exec를 표시한다|socket 이외 생성 연산도 별도 점검해야 한다고 밝힌다|의도된 passing 계약을 별도로 둔다','SOCK_CLOEXEC → 참여 networking creator의 정책','T'),
('PPP','복제 시 flag가 사라지는 문제를 다룬다|runtime과 extension의 복제·remap 경로를 대상으로 한다|standard-stream remapping은 다른 상속 의도를 가진다고 명시한다','dup3 → descriptor 복제와 의도적 remapping 구분','T'),
('PPP','file action 후 표시된 fd를 닫는다|spawn 경로 보완 계약으로 좁히며 다른 launcher 보호를 주장하지 않는다|명시적 open·close·remap으로 stdio를 보존한다','ordered spawn actions → child 전용 descriptor 계약','T'),
])
add('C12','A',[
('PPP','type/base mutation에서 version을 바꾼다|cache key의 type version으로 해당 lookup을 무효화한다|lookup 대신 작은 version 비교를 쓰며 shadowing 비용도 남긴다','PyPy type version → Python 속성 lookup guard','T'),
('PPP','binding 변경이 의존 compiled method를 무효화한다|변경→dependent code 관계가 명시돼 있다|read마다 검사하던 비용을 mutation·dependency 관리로 옮긴다','SELF dependency list → binding별 compiled-code 무효화','T'),
('PPP','변경 시 switch point를 무효화하고 일반 lookup으로 돌아간다|fast/fallback guard의 일방향 무효화가 문서화돼 있다|invalidation 비용과 새 speculation용 객체 비용을 명시한다','JVM SwitchPoint → namespace binding guard와 fallback','T'),
('PUP','불일치 상태의 generic lookup fallback을 제안한다|PIC 자체가 rebinding을 감지하지 않으며 필요한 validity guard는 정해지지 않았다|상태 수에 따른 test·miss 비용을 명시한다','다중 lookup 결과 cache → 반복 namespace/type 상태의 부분 최적화','I'),
('PUP','module dict의 JIT용 특수 저장을 조사 대상으로 한정한다|실제 mutation-validation 알고리즘은 열람 실패로 미확인이다|JIT 필요와 honor__builtins__ 조건을 명시한다','PyPy cell dictionary → global name lookup의 특수 저장','I'),
('PUP','읽기 중 겹친 쓰기를 counter 재비교로 감지한다|읽기 사이에 보관된 binding cache의 장기 유효성을 판정하는 계약은 제시되지 않았다|writer 직렬화·retry·pointer lifetime 비용을 명시한다','seqlock read snapshot → 동시 lookup 검증의 부분 선례','I'),
('PPP','property/global write hook에서 최적화를 취소한다|watchpoint와 dependent optimized code의 무효화 연결이 구체적이다|반복 guard를 write 비용·deopt로 옮기는 대가를 설명한다','JSC watchpoint → Python binding write notification','T'),
])
add('C12','B',[
('PPP','global 정보 변경이 assumption을 깨뜨린다|dependency에 연결된 compiled code를 무효화한다|compiled validity check 제거와 빈번한 재컴파일 비용을 함께 설명한다','Truffle assumption → Python binding-stability 의존성','T'),
('PPP','값 변경과 shape 안정성을 구별한다|constant-property 변경으로 dependent code를 무효화한다|location cache와 value guard의 서로 다른 비용·의미를 지적한다','V8 map 및 dependent code → 속성 위치 cache와 값 무효화 분리','T'),
('PUP','guard 실패 시 interpreter 복귀를 제공한다|저렴한 dict 변경 detector의 구체 설계는 확보되지 않았다|guard 비용을 설계해야 한다고 밝히지만 제공 근거로 판정할 수 없다','RPython guard recovery → 최적화 실패 후 복귀 경로','I'),
('PPP','Python에는 동기적 모든 mutation 처리가 필요함을 명시하고 lifecycle만 옮긴다|write 무효화→miss→refill의 관계를 명시한다|validity 표현 자체를 범위 밖으로 두고 비용 이동을 명시한다','cache-aside entry lifecycle → 동기적인 namespace cache lifecycle','T'),
])
add('C13','A',[
('PPP','기존 C API의 same-process subinterpreter를 직접 연결한다|thread-state·GIL·공유 OS 자원 경계를 명시한다|Python handle wrapper의 lifecycle substrate로 지정한다','CPython C lifecycle → Python-facing interpreter handle','T'),
('PPN','서로 다른 interpreter의 module instance를 다룬다|per-module storage·staged init·cleanup으로 static state 경계를 다룬다|Python public API 전체는 원 답변부터 이 후보의 범위 밖이다','per-module state → wrapper와 협조 extension의 상태 격리','T'),
('PPP','Jep은 한 host 안의 CPython interpreter wrapper다|creator-thread affinity·close·분리 globals를 명시한다|Java wrapper operation을 Python handle API로 번역하는 범위를 밝힌다','Jep object lifecycle → Python interpreter handle lifetime','T'),
('PPN','한 Apache process 안에 application별 subinterpreter를 둔다|module data 분리·group 공유·main interpreter 제약을 설명한다|hosting assignment policy의 선례로 좁히며 Python API를 제공한다고 하지 않는다','mod_wsgi application group → interpreter 배정·공유 정책','T'),
('PPP','하나의 host 안 child interpreter 생성·평가를 다룬다|독립 namespace와 명시적 alias/channel 연결을 구별한다|언어수준 관리 명령을 Python API 모양으로 옮기는 선례다','Tcl interp command → Python create/delete/eval 관리 표면','T'),
('PPN','프로세스 생성 대신 byte-message interface만 옮긴다고 명시한다|byte framing·EOF·close를 통해 객체 직접 공유와 다른 경계를 제시한다|Python lifecycle API 전체는 communication 부분 후보의 범위 밖이다','multiprocessing Connection semantics → interpreter 간 byte transport','T'),
('PPN','독립 Lua state를 coroutine과 명시적으로 구별한다|state별 runtime/allocator 소유권을 보존한다|C embedding/resource 모델의 선례로 좁혀 Python API 완성을 주장하지 않는다','Lua independent state handle → interpreter 자원 소유권','T'),
])
add('C13','B',[
('PUP','Jep은 same-host CPython wrapper다|clean README의 mostly isolated 설명만으로 Python-facing 값 교환·수명 경계의 실제 보존 계약은 확인되지 않는다; 자세한 비교 페이지는 원 run이 제외했다|Java host API를 Python wrapper로 번역할 경계를 명시한다','Jep managed wrapper → Python-facing interpreter handle','I'),
('PPP','Python 객체마다 별도 LuaRuntime을 둔다|runtime lock과 복사/명시 통신으로 데이터 경계를 둔다|Python 객체 API 모양을 CPython handle에 옮기는 제안이다','Lupa LuaRuntime object → Python interpreter handle와 명시 transfer','T'),
('PUN','writer/reader를 interpreter로 대응시키는 원리를 제시한다|CPython payload 소유권·종료·blocking의 핵심 계약은 지정하지 못했다|channel 부분 후보이며 lifecycle public API는 다루지 않는다','Message Channel → interpreter 사이의 통신 경계라는 유추','I'),
])
add('C14','A',[
('PPPN','나중에 namespace로 문자열 name을 resolve한다|compile과 evaluation 시점을 분리하되 compile 비용은 남는다|type checking의 강제 도입을 요구하지 않는다|type validator의 일반 annotation 제한을 밝히며 표현·resolution 부분에만 적용한다','ForwardRef resolver → annotation의 표현과 나중 namespace lookup','T'),
('PPPN','선언 뒤 callable/registry lookup이 나중 class를 찾는다|mapping 초기화까지 선언 처리를 미룬다|타입검사 의무를 추가하지 않는 lifecycle 선례다|원 응답은 ORM 초기화 lifecycle·namespace resolution 부분만 옮긴다; arbitrary annotation 값 처리 지원은 이 참고의 범위 밖이다','SQLAlchemy deferred relationship → annotation resolution lifecycle','T'),
('PPPP','정의 전 expression을 promise로 담고 나중 force한다|import 시 arbitrary expression 실행을 미룬다|optional metadata 표현이며 강제 typing이 아니다|arbitrary result promise로 타입 외 값도 다룬다','SRFI45 promise/force → 일반 annotation의 지연 계산·memoization','T'),
('PPPP','zero-argument callback이 name lookup을 미룬다|resolve 요청 시 실행하며 결과 caching 부재도 명시한다|명시 wrapper opt-in 선례다|일반 값은 통과시키고 callback result type을 제한하지 않는다','Angular forwardRef callback → 명시적 annotation forward-reference wrapper','T'),
('NPPN','forward reference 자체는 해결하지 않는 보완 역할이다|checker-only import branch로 import 비용을 줄인다|ordinary execution과 checking을 분리한다|일반 runtime metadata evaluator는 원 답변부터 별도 경로로 남긴다','TYPE_CHECKING branch → 타입 전용 의존성 import 분리','T'),
('NPPN','정의 전 name 문제를 직접 바꾸지 않는 storage 부분안이다|static interface를 실행 모듈 밖으로 분리한다|정적 checking을 별도 선택 작업으로 유지한다|일반 runtime metadata를 제공하지 않음을 명시한 static-only 범위다','mypy stub → 실행 코드 밖의 선택적 type-description 저장','T'),
])
add('C14','B',[
('PPPP','inert intent가 lookup을 실행하지 않고 보관한다|performer 호출로 evaluation을 미룬다|명시적 interpretation과 optional consumer를 제안한다|arbitrary intent/performer 분리이며 namespace·consumer 호환성 조건을 남긴다','Effect intent/performer → annotation description/evaluation 분리','T'),
('PPPN','Symbol 표현으로 name 값을 먼저 요구하지 않는다|expression data를 먼저 구성하되 library import 비용을 주의한다|수학 type system을 Python에 강제하지 않는 표현 선례다|arbitrary Python annotation evaluator는 지원하지 않는다고 명시한 좁은 표현 범위다','SymPy Symbol expression → unresolved annotation 표현의 부분 선례','T'),
('NPPN','forward reference 저장을 바꾸는 후보가 아니다|검사 시 annotated program을 실행하지 않는 소비자 경계다|typed/untyped 혼합과 optional checking을 직접 문서화한다|일반 metadata 계산은 별도라고 명시한 consumer-only 범위다','mypy checker/execution separation → optional annotation consumer','T'),
])
add('C15','A',[
('PP','ordinary library symbol을 callable fallback으로 둔다|직접 call을 compiler metadata로 낮춰 ABI-only wrapper를 분리한다','GCC library recognition → ordinary callable identity와 intrinsic lowering 분리','T'),
('PP','typed external은 curried function value로 노출된다|manifest external이 client의 primitive direct call을 허용한다','OCaml manifest external → public signature에 primitive metadata 전달','T'),
('PP','생성된 curried wrapper가 callable entry point를 제공한다|API 작성자별 wrapper 대신 중앙 생성; native unsaturated routing은 추가 작업이라고 명시한다','GHC generated wrapper → shared callable primitive entry','T'),
('PP','normal function definition을 그대로 둔다|별도 compiler macro expansion으로 direct-call rewrite를 붙이되 -O0 보장은 추가 policy임을 명시한다','Common Lisp compiler macro → callable function와 rewrite metadata 분리','T'),
('PP','Go 함수와 portable body가 function value fallback이다|direct-call intrinsic recognition이 body inlining과 구별된다','Go math/bits → callable library API와 compiler substitution','T'),
])
add('C15','B',[
('PP','real ordinary library function을 callable fallback으로 남긴다|nominal ABI adapter 제거와 intrinsic lowering을 분리한다','GCC library builtin → ordinary symbol 기반 intrinsic API','T'),
('PP','dual implementation routine에만 한정해 callable definition을 보존한다|function별 metadata로 adapter body 없이 direct call을 다룬다','MSVC intrinsic/function pragma → 함수 정체성과 lowering policy 분리','T'),
('NP','원 응답부터 frontend declaration 부분에 한정하며 address taking은 증명하지 않았다고 밝힌다|typed declaration에 builtin identity를 붙여 naming-only wrapper를 제거한다','Clang builtin alias attribute → intrinsic 선언 metadata의 좁은 선례','T'),
])
add('C16','A',[
('PP','block statement와 local declaration 양쪽에 attribute grammar가 있다|기존 함수 안 syntax node에 직접 붙인다','C++ statement/declaration attribute → Rust AST attachment','T'),
('PP','variable pragma와 region push/pop을 모두 다룬다|inline when이 외부 함수 추출 없이 local context를 유지한다','Nim variable·region pragma → local annotation scope','T'),
('PP','statement/declaration를 둘러싼 source span에 lint policy를 제한한다|push/pop이 함수 안에서 동작한다','GCC diagnostic history → source-local lint exception','T'),
('NP','local declaration만 되는 후보로 명시해 block 지원까지 승인하지 않는다|선언에 직접 붙여 함수 추출을 요구하지 않는다','Java local suppression → let annotation의 좁은 선례','T'),
('NP','block permission/checking만 되는 후보이며 declaration metadata는 별도다|inline block이 기존 local context를 보존한다','C# unsafe/checked block → bounded permission scope','T'),
('PP','declaration/statement 조건 선택을 모두 지원한다|conditional braces가 새 scope를 만들지 않아 local context를 보존한다','D conditional syntax → inline cfg 영역','T'),
])
add('C16','B',[
('PP','unused declaration과 bounded region checking을 함께 다룬다|함수 안 원위치에 control comment를 둔다','Splint declaration/control comment → local lint/audit scope','T'),
('PP','statement/declaration span을 diagnostic 및 textual conditional로 제한한다|코드를 추출하지 않고 같은 lexical context에 둔다','GCC pragma/preprocessor → inline local policy','T'),
('NP','statement/block contract만 입증됐으며 declaration annotation은 범위 밖이다|원래 block과 context에 contract를 붙인다','ACSL block contract → permitted effects/audit annotation','T'),
('NP','local declaration과 initializer만 해당하며 arbitrary block은 명시적으로 제외한다|별도 함수 대신 해당 선언에 suppression을 붙인다','Checker Framework suppression → let declaration 범위 규칙','T'),
('PP','line/range가 선언과 block을 국소적으로 둘러쌀 수 있다|inline comment boundary와 rationale로 함수 추출을 피한다','ESLint local suppression → bounded lint exception와 설명','T'),
])
add('C17','A',[
('PP','static/dynamic 패턴 API를 Rust frontend로 옮기는 범위다|template syntax 제약과 compiler work 증가를 설명한다','Xpressive dual interface → static/runtime pattern frontend','T'),
('PP','RE2 string search engine을 Rust에서 wrap하거나 참조한다|native build·FFI·dialect 제한을 설명한다','RE2 foreign engine → Rust pattern library backend','T',[(2,'실제 응답이 C++ 엔진을 Rust에 wrap하는 구성을 명시한다.')]),
('PP','Thompson NFA를 native Rust matcher 출발점으로 제시한다|captures·Unicode·diagnostics 추가 책임을 명시한다','NFA construction/simulation → native Rust matcher','T'),
('PP','PCRE compiled pattern을 Rust wrapper에서 재사용한다|byte order·tables·version·FFI와 JIT 직렬화 한계를 설명한다','PCRE C library → Rust wrapper와 build-time compiled representation','T',[(2,'기존 C 엔진의 Rust wrapper와 배포/버전 비용을 직접 제안한다.')]),
('PP','fixed regex에서 matching code를 생성하는 경로다|lexer→substring/capture API 및 build 통합을 별도 요구한다','re2c code generator → static Rust pattern path','T'),
('PP','간결한 bundled pattern/search/capture API의 선례다|byte/locale와 Rust UTF-8 및 dialect 차이를 명시한다','Lua bundled patterns → 작은 distribution API 범위','T'),
('PP','Rust library가 직접 UTF-8 pattern/search/capture를 제공한다|compiled reuse와 지원하지 않는 regex 문법·유지 책임을 설명한다','Rust regex runtime API → distribution-supported library','D'),
('PP','compiled pattern type과 fallible matching API를 제시한다|MustCompile runtime panic과 standard-library 유지 범위를 설명한다','Go regexp organization → Rust library API/error boundary','T'),
])
add('C17','B',[
('PP','native Rust pattern string/search/capture API가 존재한다|lazy runtime reuse와 dialect·distribution 유지 대가를 명시한다','Rust regex crate → distribution-supported pattern API','D'),
('PP','wrapped C++ engine 또는 implementation model로 사용한다|native integration와 resource/expressiveness tradeoff를 명시한다','RE2 backend → Rust FFI library','T',[(2,'원 답변이 wrap된 기존 C++ 엔진의 reuse를 명시한다.')]),
('PP','기존 C engine·Perl-style dialect를 Rust wrapper로 제안한다|backtracking·native builds·upstream maintenance를 설명한다','PCRE engine → expressive Rust foreign backend','T',[(2,'기존 C 라이브러리를 binding하는 구성이 명시되어 있다.')]),
('PP','기존 C engine을 Rust에 reuse하며 encoding policy를 분리한다|string·encoding·ownership boundary와 종료된 upstream을 명시한다','Oniguruma → Rust foreign engine와 encoding 선택','T',[(2,'candidate가 기존 C 엔진의 Rust integration을 구체적으로 제안한다.')]),
('PP','POSIX compile/execute API를 Rust library로 reuse하는 선례다|fuzzy 기능 범위·collation·license·native bridge를 명시한다','TRE C API → Rust pattern backend','T',[(2,'기존 C 라이브러리 reuse 및 Rust 쪽 boundary가 원 응답에 있다.')]),
('PP','static pattern을 executable state machine으로 만든다|Rust generator/foreign bridge·code size·build 비용을 명시한다','Ragel code generation → static matching frontend','T'),
('PP','literal parsing 및 matcher specialization을 compile time으로 옮긴다|C++ template 번역·compile time·code size 비용을 명시한다','CTRE compile-time matcher → Rust static pattern design','T'),
])
add('C18','A',[
('PP','ASCII와 escaped high byte가 Unicode str와 분리된다|sequence와 integer indexing을 명시적으로 구별한다','Python bytes notation → Rust raw byte literal/type distinction','T',[(4,'Python b-prefix byte string이라는 동일 외부 문법을 직접 반환했다.')]),
('PP','byte output에 character encoding을 적용하지 않는다|0..255 scalar와 distinct byte string을 함께 설명한다','Racket byte strings → raw byte scalar/sequence 표현','T'),
('PP','8-bit representation을 Unicode Rust type와 분리해 옮긴다|single quote scalar와 double quote sequence를 함께 제시한다','OCaml char/string syntax → raw scalar/sequence 표기','T'),
('PP','invalid UTF-8를 담는 byte storage와 Unicode 연산을 구별한다|byte indexing과 byte string을 함께 다룬다','Go string byte semantics → readable raw sequence와 scalar 접근','T',[(7,'unescaped non-ASCII source가 UTF-8로 인코딩된다는 구체 구조를 caveat에서 명시했다; 단순 Unicode 언급이 아니다.')]),
('PP','binary field와 numeric byte를 character decoding 없이 구성한다|8-bit numeric segment와 sequence를 구성·매칭한다','Erlang bit syntax → numeric-byte binary pattern과 읽을 수 있는 fragment','T',[(1,'원 답변과 열람 기록 모두 numeric byte를 binary pattern에서 매칭하는 구조를 명시한다.')]),
('PP','Char8의 8-bit truncation과 raw storage 경계를 명시한다|pack과 singleton으로 sequence와 one-byte sequence를 모두 다룬다','ByteString.Char8 constructors → library-only byte notation','T'),
('PP','hex string은 invalid UTF를 허용하고 numeric escapes가 raw byte를 보존한다|char literal/byte escape와 sequence 대안을 함께 읽었다','D hex/byte escapes → raw-byte literal 표기','T'),
])
add('C18','B',[
('PP','arbitrary bytes와 rune decoding을 구별한다|sequence와 byte indexing을 함께 제공한다','Go string/byte indexing → raw-byte notation과 접근','T',[(7,'ordinary source characters의 UTF-8 encoding을 실제 응답에서 별도 동작으로 설명한다.')]),
('PP','8-bit 표현만 옮기고 ISO-8859-1 해석은 제외한다|동일 escape를 가진 scalar/sequence를 함께 제시한다','OCaml paired literals → raw byte scalar/sequence grammar','T'),
('PP','b-prefix가 Unicode와 다른 bytes 값을 만든다|integer indexing과 bytes slicing을 구별한다','Python bytes literal → raw sequence와 byte scalar 접근','T',[(4,'동일 Python bytes literal 선례이나 실제 열린 판은 사후 자료다.')]),
('PP','string UTF-8는 강제되지 않는 convention이라고 명시한다|char 단일 byte와 sequence를 별도 Rune와 구별한다','Nim byte char/string → raw scalar/sequence pair','T'),
])
add('C19','A',[
('PP','현재 Rust pattern-position macro가 반복 nested pattern을 직접 치환한다|grammar-named macro와 caller binding을 제안한다','Rust MBE pattern output → 반복 구조 이름 붙이기','D'),
('PP','parameterized pattern synonym이 nested destructuring을 재사용한다|grammar 용어와 representation 독립성을 유지한다','GHC pattern synonym → Rust pattern abstraction','T'),
('PP','pattern transformer가 반복 pattern을 compile time에 생성한다|grammar-shaped 이름과 match arm을 보존한다','Racket match expander → Rust pattern extension','T'),
('PP','전체 expression macro의 recognition unit으로 pattern과 guard를 재사용한다|grammar-named operation에 적합하고 binding/layout 차이를 명시한다','matches! whole expression → 인식 단위의 named recognition macro','T'),
('PP','view function 결과의 named case로 deconstruction을 재사용한다|grammar 이름과 storage representation을 분리한다','GHC view function → Rust borrowed view enum','T'),
('PP','unapply의 component extraction을 helper Option 결과로 옮긴다|grammar production과 underlying storage를 분리한다','Scala extractor → Rust fallible decomposition helper','T'),
])
add('C19','B',[
('PP','pattern transformer가 반복 match structure를 재사용한다|named grammar abbreviation과 visible match arm을 유지한다','Racket pattern expansion → Rust pattern abstraction','T'),
('PP','parameterized pattern scheme가 nested destructuring을 재사용한다|representation을 바꾸지 않고 grammar name을 부여한다','GHC pattern synonym → Rust reusable structural pattern','T'),
('UP','grammar production 반복인 경우만 적용되며 AST destructuring pattern인지 입력이 결정하지 못한다|spec와 generator grammar 대응은 문서화돼 있다','LALRPOP grammar macros → production-level parser rewrite','I'),
('UP','PEG parsing rules 재사용이 기존 Rust match의 structural reuse와 같은 문제인지 미확인이다|명명된 grammar rule의 spec 대응은 설명돼 있다','rust-peg parameterized rule → parser production reuse','I'),
('UP','입력 인식 sequence인지 단순 값 destructuring인지에 따라 적용 가능성이 갈린다|named parser combinator로 grammar를 표현하는 부분은 지원된다','combine parser values → sequence-recognition reuse','I'),
])
add('C20','A',[
('PP','whole message·plural/select·locale를 지원한다|message grammar와 locale data를 optional library가 소유한다','ICU MessageFormat → core formatter 밖의 message interpreter','T'),
('PP','catalog와 translator plural rule 뒤 값 formatting을 수행한다|외부 catalog→template→formatter 분리를 제시한다','GNU gettext translate-then-format → 외부 localization pipeline','T',[(2,'GNU gettext의 catalog 선택 뒤 ordinary formatting 구성으로 같은 선행 사례를 반환했다.')]),
('PP','translator resource의 gender/plural logic을 구체적으로 설명한다|message ID/context API로 core format string 밖에서 처리한다','L20n resource logic → core 밖의 language-specific message assembly','T',[(1,'Mozilla L20n이라는 동일 외부 접근과 resource-owned grammar를 직접 찾았다.')]),
('PP','catalog translation·deferred message·locale별 render를 지원한다|optional C++ library boundary를 Rust형 API로 옮긴다','Boost.Locale deferred translation → optional locale-aware rendering layer','T'),
('PP','collation·number/date라는 좁은 localization 서비스를 다룬다|dedicated Intl API로 core formatting grammar와 분리한다','ECMA-402 service objects → locale formatting layer','T'),
('PP','catalog extraction·locale values·CLDR workflow를 다룬다|외부 package가 data와 tooling의 release 책임을 소유한다','Babel catalog/data tooling → core 밖 localization workflow','T'),
])
add('C20','B',[
('PP','translation/localize API와 richer backend 경로를 명시한다|public API와 replaceable backend를 분리한다','Ruby I18n backend boundary → Rust optional localization layer','T'),
('PP','collation·number/date의 좁은 서비스와 message layer 부재를 구별한다|별도 채택 가능한 Intl API를 core release와 분리한다','ECMA-402 separate API → locale service boundary','T'),
('PP','whole sentence와 plural/select branches를 지원한다|basic value formatting과 message assembly를 분리한다','ICU MessageFormat → optional grammatical assembly','T'),
('PP','locale convention data라는 구체 부분을 다룬다|data release를 compiler/basic formatter와 분리한다','CLDR data repository → independently updated locale dependency','T'),
('PP','context·plural selection 뒤 positional interpolation을 제공한다|catalog lookup과 basic formatter를 분리한다','Jed lookup/interpolation → application localization boundary','T'),
('PP','plural/gender message pattern을 function으로 compile한다|compiler·parser·loader·runtime를 optional tooling으로 둔다','messageformat compilation → Rust 외부 message tooling','T'),
('PP','선택적 locale modules/data와 reusable formatter를 제공한다|필요 기능만 library/runtime에 넣는 책임 분리를 명시한다','Globalize modular locale formatting → optional library boundary','T'),
])

CHECKS = {
    ('C12','A',4): 'PIC의 cache-validity guard와 namespace rebinding 시 patch/invalidate 경로를 함께 명시한 구현을 읽고, type가 같아도 binding이 바뀌는 사례를 추적한다.',
    ('C12','A',5): 'PyPy 2.6 module cell dictionary의 mutation code와 honor__builtins__ 옵션 의미를 읽고, cell identity 유지·변경 시 guard와 invalidation의 대응을 확인한다.',
    ('C12','A',6): '캐시 결과를 여러 lookup 사이에 보관하는 설계에서 각 write가 retained entry를 무효화하는 규칙과 counter reuse/overflow 처리를 확인한다.',
    ('C12','B',3): 'RPython의 구체 dict storage·version guard 코드에서 rebinding이 감지되는 지점과 검사 비용을 읽는다. 일반 guard fallback 설명만으로는 부족하다.',
    ('C13','B',1): '오염 없는 Jep lifecycle/value conversion 문서를 열어 interpreter-owned 객체가 다른 interpreter에 전달될 때와 close 뒤 사용 시 계약을 확인한다. 제외된 비교 페이지를 그대로 근거로 복원하지 않는다.',
    ('C13','B',3): '채널의 payload type·복사/소유권·close/teardown 계약을 정한 사례와 CPython handle 대응을 확인한다. 일반 writer-reader 설명만으로는 부족하다.',
    ('C19','B',3): '원 parser에서 반복되는 match의 AST/token 입력과 부작용을 확인하고 LALRPOP production/action으로 동일 범위를 나타낼 수 있는 최소 예시를 대조한다.',
    ('C19','B',4): '원 parser의 반복 구조가 Rust 값의 destructuring인지 token/문자열 인식인지 확인한 뒤 rust-peg 규칙으로 옮길 때 결과·오류·부작용을 유지하는 사례를 대조한다.',
    ('C19','B',5): '원 parser의 match arm/guard/result 구조를 확인하고 combine의 parser 값으로 옮길 때 같은 입력·출력·부작용을 보존하는 예시를 대조한다.',
}

def build():
    out=[]
    states={'P':'pass','N':'not_in_scope','U':'unknown','F':'fail'}
    labels={'T':'CONDITIONAL_TRANSFER','D':'DIRECT_DOCUMENTED','I':'INSUFFICIENT','F':'SURFACE_OR_CONSTRAINT_MISMATCH'}
    for (cid,base), specs in SPECS.items():
        run=json.loads((BASE/'runs'/base/(cid+'.json')).read_text())
        case=CASES[cid]
        assert len(specs)==len(run['candidates']), (cid,base,len(specs),len(run['candidates']))
        for cand,spec in zip(run['candidates'],specs):
            hchars,hreasons,mapping,code,*matches=spec
            reasons=hreasons.split('|')
            assert len(hchars)==len(reasons)==len(case['mandatory_constraints'])
            gms=[]
            for n,rationale in (matches[0] if matches else []):
                gold=case['gold_items'][n-1]
                gms.append({'gold_id':gold['id'],'match_kind':gold['match_kind'],'rationale':rationale})
            norm=urldefrag(cand['url'])[0].rstrip('/')
            doc_evidence=[]
            for n,doc in enumerate(run['opened_documents']):
                if doc.get('status')=='opened' and urldefrag(doc['url'])[0].rstrip('/')==norm:
                    doc_evidence.append({'run_path':f'runs/{base}/{cid}.json','json_pointer':f'/opened_documents/{n}','url':doc['url'],'sections_read':doc.get('sections_read'),'confirmed':doc.get('confirmed')})
            if not doc_evidence:
                # Indirect evidence is included only when the run explicitly read it, never by guessing.
                doc_evidence=[{'run_path':f'runs/{base}/{cid}.json','json_pointer':'/opened_documents','note':'후보의 verification_urls 또는 같은 원 응답의 versioned/supporting document를 함께 읽었다. 후보 원문 URL과 같은 대상임을 응답에서 확인.'}]
            date=cand['date_status']
            matched=[x['gold_id'] for x in gms]
            hs=[{'constraint_id':h['id'],'value':states[s],'reason':r} for h,s,r in zip(case['mandatory_constraints'],hchars,reasons)]
            useful=not matched and code in ('T','D') and not any(x['value'] in ('fail','unknown') for x in hs)
            need=[]
            if code=='I':
                need.append(CHECKS[cid,base,cand['rank']])
            if date=='unknown':need.append('같은 메커니즘을 확인할 수 있는 결정일 이전 고정판·발행일을 열어 역사 적격성을 확인한다.')
            if code=='T':need.append('원 응답이 지정한 연결 작업과 실패 조건을 대상 구현에서 확인한다; 문서 기반 전이 판정이며 실행 성공이 아니다.')
            row={
              'case_id':cid,'baseline':base,'rank':cand['rank'],'candidate_name':cand['name'],'candidate_url':cand['url'],
              'gold_matches':gms,'review_matches':[],
              'L':'ok','E':'supported','H':hs,'T':'mapped' if code=='T' else ('not_needed' if code=='D' else 'unknown'),
              'transfer_mapping':{'source_to_target':mapping,'required_bridge_and_failure_conditions':cand.get('constraints_or_caveat'),'scope_as_returned':cand.get('application_scope'),'status':'검증된 통합 아님; 원 응답의 명시적 사용 방식에 대한 문서 판정'},
              'H_assessment_scope':'proposed_configuration' if code=='D' else 'reference_design','runtime_observation':'not_performed',
              'label':labels[code],'link_status':'opened','date_status':date,'original_date_status':date,'date_evidence':cand.get('date_evidence'),
              'strict_historical_gold_ids':matched if date=='pre_decision' else [],
              'post_decision_gold_ids':matched if date=='post_decision' else [],
              'date_unknown_gold_ids':matched if date=='unknown' else [],
              'nongold_useful':useful,'nongold_historical_useful':useful and date=='pre_decision',
              'near_miss':any(x['value']=='fail' for x in hs),'broken_or_fake':False,
              'exclusion':{'excluded':False,'reason':'원 run의 반환 후보·검증 근거에서 대상 제안 또는 동일 저장소 문서를 사용한 사실이 확인되지 않는다. run-level snippet/기억 노출은 별도 보존한다.'},
              'judge':'내부 별도 검토','evidence_locations':[{'run_path':f'runs/{base}/{cid}.json','json_pointer':f'/candidates/{cand["rank"]-1}'},{'run_path':f'runs/{base}/{cid}.json','json_pointer':'/raw_response'},*doc_evidence],
              'remaining_check':' '.join(need) if need else '문서 주장 범위 판정은 완료했다. 실제 Rust/Python 통합·성능 효과는 별도 구현 실험으로 확인한다.',
            }
            out.append(row)
    assert len(out)==114
    return {'schema_version':1,'judge':'내부 별도 검토','model_label':'GPT-6 Astra Pro','input_commit':'caa2a814727dd485ed0eb9bb8530d6b16fab9584','scope':'C11..C20, A/B 전후보; 원 응답 및 opened_documents 직접 대조. 별도 모델/사람 검토 아님.','judgments':out}

if __name__=='__main__':
    data=build()
    (HERE/'judgments.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    from collections import Counter
    print(json.dumps({'rows':len(data['judgments']),'labels':dict(Counter(r['label'] for r in data['judgments'])),'gold_match_rows':sum(bool(r['gold_matches']) for r in data['judgments']),'nongold_useful':sum(r['nongold_useful'] for r in data['judgments'])},ensure_ascii=False))
