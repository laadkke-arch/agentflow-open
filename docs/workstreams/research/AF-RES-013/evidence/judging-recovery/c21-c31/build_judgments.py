import json,pathlib,datetime
B=pathlib.Path(__file__).resolve().parents[3]
O=pathlib.Path(__file__).resolve().parent
CASES={c['id']:c for c in json.loads((B/'cases/CASES.json').read_text())['cases']}
# Manual semantic decisions, after reading every assigned raw_response and opened_documents.
# codes refer to each original mandatory constraint; N is restricted reference scope, never a claim of full fulfilment.
D={}
def put(cid,baseline,rank,codes,why,bridge,gold=(),label='CONDITIONAL_TRANSFER',date=None,remaining=None):
 D[(cid,baseline,rank)]={'codes':codes,'why':why,'bridge':bridge,'gold':list(gold),'label':label,'date':date,'remaining':remaining}
# C21: callable representation, acquisition and invocation are different design decisions.
put('C21','A',1,'NNP','구체 closure class와 비가상 호출 연산자의 정적 최적화 경로를 제시했다. receiver 기본값을 바꾸자는 대안까지 말한 것은 아니다.','구체 callable 타입을 정적 호출 경로로 보존하고, 동적 wrapper는 별도 선택으로 둔다. const 호출은 referent 불변이나 consuming 호출을 보장하지 않는다.')
put('C21','A',2,'PNN','명시적 개별 environment field의 reference/move 초기화는 per-variable capture clause 대안을 회수한다.','각 캡처 변수를 closure field에 대응시키고 값 이동과 reference 초기화를 구별한다. reference lifetime과 consuming invocation은 다른 규칙으로 연결해야 한다.',('R0114-G05',))
put('C21','A',3,'NPN','cv/lvalue/rvalue receiver의 구별을 environment 접근에 대응시킨 좁은 참고다. 원 실행은 상세 부분이 snippet에 머물렀으나 추가 원문 확인은 성공했다.','const&/비const&/&& receiver를 읽기/변경/이동 가능 접근으로 대응시킨다. &&만으로 single-use가 강제되지는 않으므로 소모 규칙을 별도로 유지한다.')
put('C21','A',4,'PNP','서명 기반 wrapper의 clone과 ref/cref 정책 및 명시적 dispatch 경계가 근거에 있다.','구체 callable을 보존하는 경로와 type-erased wrapper 경로를 선택 가능하게 한다. ref/cref lifetime을 확인하고 clone을 unique ownership으로 취급하지 않는다.')
put('C21','A',5,'PNN','value capture와 shared mutable cell 및 escape 시 복사를 분리하는 부분 메커니즘이다.','일반 캡처→환경의 값, __block→공유 cell, copy/dispose→escape 생명주기 관리로 대응한다. 공유 cell은 exclusive borrow나 consuming call과 같지 않다.')
put('C21','A',6,'NNP','function/context 두 포인터와 scope별 저장소 선택의 표현 대안이다.','환경 포인터와 호출 포인터를 분리하고 local scope와 escaping scope의 저장소 정책을 선택한다. D의 GC를 Rust 소유권으로 그대로 대체했다고 보지 않는다.')
put('C21','A',7,'PNN','살아 있는 stack frame의 지역 변수에 접근하는 borrowed callback의 한정된 사례다. by-value 전체 대안은 아니다.','callback lifetime을 생성 frame 이내로 제한하고 trampoline/function pointer를 전달한다. escaping owned closure 경로에는 적용하지 않는다.')
put('C21','A',8,'NNP','functional interface와 구현 instance의 할당·재사용 자유를 분리한 참고다.','호출 계약을 interface로 고정하되 구체 표현을 구현 선택으로 남긴다. effectively-final local 제한 때문에 mutable borrow/consuming 모드의 완성 대안으로 쓰지 않는다.')
put('C21','B',1,'PNP','copy/reference capture와 const/mutable 호출을 분리한 일반 모델은 확인했다. 후보는 개별 변수 clause나 reference 기본값을 명시적으로 제안하지 않아 gold를 확장하지 않는다.','capture 방식과 invocation mutability를 별도 축으로 두고 구체 closure type을 유지한다. lifetime, 소비 규칙, 실제 inlining 보장은 별도다.')
put('C21','B',2,'NPN','linear closure의 반복 호출 보존과 명시 해제를 구별하는 자원 접근 모델이다.','closure resource를 비소모 호출 뒤 보존하고 마지막에 해제하는 상태 전이를 대응시킨다. linear ownership 자체를 consuming invocation으로 동일시하지 않는다.')
put('C21','B',3,'NNP','context/function delegate와 scope-sensitive 환경 allocation에 한정된 참고다.','local callable과 escaping callable에 공통 interface를 주되 환경 저장소를 분리한다. GC 기반 생존을 Rust의 borrow/ownership 보장으로 대신하지 않는다.')
put('C21','B',4,'PNP','원 응답은 ordinary captures가 by reference라고 명시하므로 reference 기본 캡처 대안을 회수한다. 근거는 2026년 판이다.','reference capture를 기본 acquisition으로 보고 inline/closure iterator 선택을 표현·최적화의 별도 선택으로 대응한다. iterator 접근 규칙은 consuming/read/mutate callable 계약과 다르다.',('R0114-G04',))
# C22: naming alternatives; a word's contract must remain unchanged.
for a,n,items in [('A',6,{
1:('JSR-305의 ThreadSafe 이름과 Immutable와의 분리가 실제 rename 후보에 해당한다.','동일 ThreadSafe 철자를 concurrency-safe shared access의 이름으로 제한한다. Java의 모든 public operation 보장을 Rust trait 의미에 추가하지 않는다.',('R0123-G03',)),
2:('Qt의 동일 instance thread-safe 용어를 사용하되 reentrant와 구별했다.','ordinary shared access와 동일 instance의 concurrent-safe access를 다른 명칭으로 둔다. reentrant나 lock 의무를 trait 뜻으로 대체하지 않는다.',('R0123-G03',)),
3:('readable/immutable/isolated의 구별은 접근 권한과 동시성 허가가 다르다는 반례다.','읽기 view와 writable alias가 공존할 수 있음을 문서에 반영한다. readable/immutable를 trait의 동의어로 바꾸지 않는다.',()),
4:('shared ownership을 thread-safety 계약과 분리하는 명명 구조가 Threadsafe 대안을 뒷받침한다.','shared는 alias/ownership 층에 두고 thread-safe를 concurrency predicate에 쓴다. ref-count 안전성과 pointee 안전성을 구별한다.',('R0123-G03',)),
5:('ThreadSafe suffix가 reference-count/collection 명칭에 합성된 실제 사례다.','기존 trait 의미를 유지하며 concurrency qualifier를 명시한다. suffix가 모든 reachable state의 안전을 보증한다고 확대하지 않는다.',('R0123-G03',)),
6:('D shared는 thread visibility 용어이고 안전성 trait과 같지 않다는 대조를 제공한다.','cross-thread 노출과 alias 가능성을 문서에서 구별한다. synchronization과 barrier를 자동 제공하는 이름으로 이식하지 않는다.',())}),('B',5,{
1:('Qt ThreadSafe 이름과 마지막 translation의 ConcurrentShareable 제안이 Threadsafe/ConcurrentlySharable 명명 대안과 일치한다. 후자는 발견된 이름이 아니라 실행자 추론이다.','동일 instance 안전성을 shared-reference concurrent safety로 제한한다. 최종 문장의 ConcurrentShareable은 Concur­rentlySharable과 같은 명명 의미이며 별도 기존 제품 존재로 세지 않는다.',('R0123-G03','R0123-G08')),
2:('shared ownership과 thread-safety를 다른 층으로 표현하는 이름 설계다.','handle의 공유 수명과 thread-safe operation 계약을 분리한다. 소유와 borrow를 동의어로 바꾸지 않는다.',('R0123-G03',)),
3:('mutable abstraction도 thread-safe일 수 있다는 명명 반례를 제시한다.','interior mutation을 허용하는 trait 설명에 thread-safe를 쓴다. contained object까지 안전하다고 확장하지 않는다.',('R0123-G03',)),
4:('shared/exclusive capability와 concurrency protection 계약의 층 분리이며 특정 gold 이름을 제안한 것은 아니다.','access mode와 안전성 조건을 문서의 별도 명명 층으로 둔다. Locked/Guarded라는 메커니즘명을 marker trait 의미로 바꾸지 않는다.',()),
5:('read-only box와 immutable val, isolated iso를 구별한 반례다. 실제 열린 tutorial의 redirect가 후보 URL로 이어진다.','aliasable readonly view와 immutable/thread-transfer 계약을 분리하여 trait의 범위를 설명한다. Pony actor capability를 Rust trait의 대체 정의로 삼지 않는다.',())})]:
 for k,(why,bridge,gold) in items.items():put('C22',a,k,'PP',why,bridge,gold)
# C23: conversion/calling mechanisms are not the gold's exact intValue method or C-helper delegation choices.
put('C23','A',1,'PPP','주소 정수형과 pointer round-trip 규약을 Swift/C 경계에 대응시킨다. C helper로 작업을 넘기자는 gold와는 다르다.','주소 폭을 담는 정수와 명시 변환을 연결하고, 수정된 정수의 pointer 유효성은 ABI 전제로 남긴다. 모든 플랫폼에서 uintptr_t 존재를 가정하지 않는다.')
put('C23','A',2,'PNP','IR ptrtoint/inttoptr의 폭 처리 규칙이 compiler lowering 참고다.','Swift에서 노출할 명시 변환을 IR 변환으로 낮추되 주소 폭과 truncation 정책을 정의한다. C 함수 signature와 공개 API 문법은 이 후보 범위 밖이다.')
put('C23','A',3,'PNP','explicit cast와 충분한 폭의 round-trip 계약을 API에 대응시킨다.','명시적 저수준 conversion syntax를 사용하고 original pointer 복원과 수정한 주소의 유효성을 구별한다. .intValue 메서드 형태까지 찾았다고 세지 않는다.')
put('C23','A',4,'PNP','전체 주소 연산 대신 alignment helper로 좁혀 제안했다.','포인터와 boundary를 alignment 테스트/정렬 helper 인수로 대응한다. 태깅·임의 비트 연산이나 C integer-argument 전체 대안은 아니다.')
put('C23','A',5,'PNP','alignment bits를 이용한 tagged-pointer 표현의 구체 참고다.','사용 가능한 low bits에 tag를 저장하고 추출할 때 mask를 제거한다. alignment가 보장하지 않는 비트나 provenance를 보존하지 않는 변환에는 적용하지 않는다.')
put('C23','A',6,'PNP','pointer↔usize cast 구문으로 일반 정수 연산을 연결하는 언어 설계다.','주소 폭의 정수로 명시 변환해 연산하고 복원한다. 작은 정수 truncation과 aliasing/provenance 조건을 유지한다.')
put('C23','A',7,'PPP','unsafe.Pointer/uintptr와 syscall 인수의 lifetime 제한을 함께 제시한다.','주소 연산과 foreign integer parameter 전달을 같은 식/lifetime 규칙에 연결한다. Go GC의 포인터 추적 규칙을 Swift와 동일하다고 보지 않는다.')
put('C23','B',1,'PPP','C11 변환 계약은 같은 C 언어 자료이나 C helper 작성 대안과 동일하지 않다.','주소 정수 표현과 C 인수를 연결하되 optional uintptr_t와 implementation-defined validity를 별도 전제로 남긴다.')
put('C23','B',2,'PNP','mask merge를 주소의 tag insert/replace에 대응시킨 구체 원리다.','주소 정수를 mask와 merge 연산의 입력으로 삼는다. ABI가 허용한 비트만 쓰고 pointer reconstruction과 lifetime은 별도 규칙으로 남긴다.')
# C24
put('C24','A',1,'PPP','Dart initializing formals는 인수를 선언하고 field 대입만 합성하는 gold의 구조와 일치한다. 외부 discussion의 이름 적중이 아니다.','각 constructor parameter를 기존 final field에 대입하는 합성 부분과 authored initializer list를 결합한다. 인수 선언 M×N과 forwarding은 남는다.',('S0018-G05',))
put('C24','A',2,'PPP','required/all-args constructor generation과 authored constructor 공존을 구체적으로 제시한다.','uninitialized final/non-null fields를 생성 인수로 선택하고 다른 경로는 authored constructor로 유지한다. signature collision과 Java compiler integration 차이를 확인한다.')
put('C24','A',3,'PPP','Scala case-class parameter field 문법이 명시 gold와 동일하다.','생성자 parameter를 immutable field와 생성 copy/apply에 대응한다. 내부 상태와 parameter value semantics를 분리해야 하며 여러 partial initializers를 자동 제공하지 않는다.',('S0018-G07',))
put('C24','A',4,'PPP','supplied/default/derived/lazy attribute를 구별하여 immutable 결과와 authored state를 결합한다.','caller input은 supplied attribute, 내부 상태는 derived/lazy method로 분리한다. cycle과 equality/hash에서 lazy 제외를 확인한다.')
put('C24','A',5,'PPP','Kotlin primary-constructor property 문법은 명시 gold의 같은 대상이다.','val/default parameter와 body property/init block을 연결한다. shallow read-only와 초기화 순서를 유지하고 모든 Swift initializer 유연성을 얻었다고 하지 않는다.',('S0018-G06',))
put('C24','A',6,'PUP','slot input/default/hook의 역할 분리는 확인되나 불변 속성을 어렵게 만들지 않는 규칙이 후보에서 추가 설계로 남는다.','initarg를 노출 입력, initform을 내부 기본값, initialization method를 authored setup에 대응한다. immutable slot/definite initialization을 새로 정하지 않고 통과시킬 수 없다.',label='INSUFFICIENT',remaining='Common Lisp protocol을 불변 Swift stored property에 적용할 초기화 1회·후속 쓰기 금지 규칙을 구체 예제로 제시하면 H2를 재판정한다.')
put('C24','A',7,'PPP','selected constructor/factory를 builder가 호출하므로 mutable staging과 final object 상태를 구별한다.','builder가 입력을 모은 뒤 authored final constructor를 한 번 호출하게 한다. staging 객체를 최종 immutable 객체로 오해하지 않고 extra API 비용을 보존한다.')
put('C24','A',8,'PPP','attrs의 per-field inclusion/default와 frozen 값은 관측한 2016년 후반 기능이다. property별 opt-in 문법으로 일반화하여 gold를 추가하지 않는다.','initializer 포함 여부와 default factory로 외부 입력/내부 상태를 구별하고 frozen instance를 만든다. runtime best-effort immutability를 Swift 정적 보장과 구별한다.')
put('C24','B',1,'PPP','Lombok field assignment 생성과 선택한 constructor/factory 위의 builder가 실제로 확인됐다.','required fields는 합성하고 authored initializer 경로를 유지한다. 2017 Builder.Default를 2016 이전 근거에 섞지 않으며 collision은 오류로 남긴다.')
put('C24','B',2,'PPP','immutable generated value의 supplied/derived 분리가 확인된다. non-public builder 노출은 조건으로 명시됐으며 initializer 인수 합성과 동일한 gold로 세지 않는다.','노출할 supplied attributes와 내부 derived attributes를 명시적으로 나눈다. private visibility만 보고 builder에서도 숨겨진다고 판단하지 않는다.')
put('C24','B',3,'PPP','selected constructor와 property exclusion을 통하여 caller setup을 줄이는 좁은 구성이다.','노출 입력을 선택한 constructor signature와 일치시키고 invariant는 constructor body에 둔다. getter/setter 또는 matching constructor가 없는 형태에 적용하지 않는다.')
put('C24','B',4,'PPP','generated initializer와 post-init, frozen 예외 assignment의 구체 결합을 확인했다.','선택 input과 internal default를 분리하고 post-init에서 derived state를 초기화한다. frozen 객체에 정상 setter를 호출하는 것으로 대체하지 않으며 2016 이후 기능이다.')
# C25: none explicitly chooses 'only a protocol, no default XCTest', so generic framework neutrality is not a gold match.
for a,items in [('A',[
('XCTest 프로젝트 존재와 현재 runner behavior를 구별한다. 선택한 정확한 runner 동작은 역사 판으로 검증되지 않았다.','Swift test executable에서 suite를 실행하고 failure status를 package command에 전달한다. 현재 entry API와 플랫폼 범위를 2016년 API로 backdate하지 않는다.'),
('Cargo의 package test orchestration과 optional harness 변경이 확인됐다.','Swift package graph에서 test targets를 build/run하고 인수를 runner에 전달한다. Rust 속성·rustdoc는 Swift 대응이 필요하며 default harness가 있으므로 gold G03과 같지 않다.'),
('Go의 package command가 test compile/run을 통합한다.','일반 build/install과 같은 package command로 테스트를 실행한다. Go convention과 compilation을 Swift conventions로 번역해야 한다.'),
('CTest executable registration은 framework-independent invocation 참고이며 기본 XCTest 제거를 명시하지 않는다.','test target의 executable과 args/workdir를 등록한 뒤 package build/dependencies와 연결한다. CTest 자체를 Swift dependency manager로 보지 않는다.'),
('npm script hook은 동일 명령 아래 framework 선택을 허용한다. 기본 XCTest를 제거하는 선택은 원 응답에 없다.','manifest test hook→프로세스 실행→exit status를 연결한다. shell/environment/portability 규약이 필요하며 관측 문서는 사후 판이다.'),
('Surefire가 lifecycle test phase와 XML/text 결과를 제공한다.','package lifecycle 단계와 test failure/report를 연결한다. JVM 실행기를 Swift에 그대로 설치하는 제안이 아니라 phase/report 구조의 참고다.'),
('TAP는 결과 스트림의 부분 프로토콜이다. compile/discovery/invocation 없이 testing 전체 protocol-only 대안을 찾았다고 세지 않는다.','producer의 test records와 consumer의 CI/package 결과를 연결한다. discovery/build/run와 exit 정책은 별도 구현해야 한다.')]),('B',[
('Cargo test orchestration을 package command에 대응했다.','package graph와 test target build/run를 연결하고 Swift용 harness/filter 규칙을 정한다. Rust compile attribute를 그대로 채택하지 않는다.'),
('XCTest의 현재 suite entry 및 process outcome을 package workflow에 연결한다.','test runtime을 독립 dependency/test target로 실행하고 failure exit를 package command에 전달한다. framework 선택은 선택이며 당시 APIs는 미검증이다.'),
('TAP13 계획·미완료 run 표시는 결과 수집의 부분 기여다.','runner stream의 plan과 pass/fail을 package 결과 집계로 연결한다. process exit policy와 compile/discovery를 TAP가 제공한다고 하지 않는다.'),
('Quick의 Swift test DSL과 test-target dependency 배치가 확인됐다.','package test target에서 reusable test groups를 실행하고 application binary에는 넣지 않는다. compiler-version compatibility를 확인한다.'),
('np의 publication 전 dependency reinstall/test가 reliability gate의 모델이다.','maintainer release command에 재설치와 테스트를 연결하되 skip 옵션을 드러낸다. 모든 registry publication에 강제된 보장으로 확대하지 않는다.'),
('SwiftCheck input generation과 invariant assertion을 ordinary test suite로 연결한다.','package test dependency로 generator/property를 사용하고 random failure 재현 정보를 남긴다. 유용한 property 작성과 runner orchestration은 별도다.'),
('Spectre runner/reporters는 output 선택의 좁은 기여이며 2021년 기능이다.','같은 test 정의와 reporter interface를 분리하여 human/machine output을 선택한다. 선택 mechanism의 Swift 버전·후기 도입 시점을 보존한다.')])]:
 for rank,(why,bridge) in enumerate(items,1):put('C25',a,rank,'PP',why,bridge,date='unknown' if a=='A' and rank==1 else None)
# C26
for a,items in [('A',[
('language-mode macro와 parser 앞 조건 선택이 직접 확인됐다.','compiler release와 language mode를 구별하고 inactive syntax를 preprocessing에서 제거한다. 제외 text도 string/comment tokenization은 유효해야 한다.'),
('GHC predicate와 CPP 단계는 확인됐다. comma 성분 문법은 원 응답이 직접 제안하지 않아 syntax gold로 세지 않는다. calendar date는 snippet-only다.','compiler-version predicate의 존재를 먼저 guard하고 version-specific 코드를 CPP에서 선택한다. 외부 CPP와 언어 lexer 상호작용을 확인한다.'),
('feature와 extension 지원 질의를 버전 threshold 대체로 제시한다.','stable capability ID를 조건으로 삼고 old compiler가 모르는 질의의 fallback을 정의한다. 모든 extension을 표준 언어 기능으로 오해하지 않는다.'),
('compatibility macro가 구문 차이 중 대체 가능한 부분을 모은다.','new keyword/declaration을 old equivalent 또는 빈 확장으로 매핑한다. 임의 grammar나 semantic change 전체를 해결한다고 하지 않는다.'),
('Six는 공통 grammar 안의 helpers에 한정한 compatible source 방법이다.','두 버전 모두 parse하는 구문에서 operation 차이를 helper로 모은다. 새로운 grammar는 별도 rewriting/preprocessing이 필요하며 later 1.15 상세는 backdate하지 않는다.'),
('Babel의 opt-in transforms와 preset은 author source 하나에서 target source를 생성한다.','Swift parser/transform과 semantic checks 및 diagnostics를 마련해 버전별 output을 생성한다. JS tool 자체가 Swift를 지원한다고 하지 않는다.')]),('B',[
('PreForM은 language-independent preprocessor라는 명시된 범위가 있다.','package build가 version symbol을 전달하고 incompatible fragment를 compile 전에 제거한다. Swift tokenization과 version detection 연결이 필요하다.'),
('future의 conversion과 helpers는 shared grammar를 만든다.','Swift-specific rewrite를 통해 shared forms를 만들고 남은 차이를 helpers에 모은다. current guide를 과거 그대로라고 하지 않고 날짜가 있는 old change만 구별한다.'),
('Babel의 source-to-source lowering이 source-tree 중복을 줄이는 방법이다.','authoring source 하나에서 target grammar를 생성하도록 parser/transform을 연결한다. target별 semantic equivalence와 diagnostics를 확인한다.'),
('Modernize의 fixers는 기존 소스를 공통 grammar 쪽으로 재작성한다.','Swift-specific syntax fixers와 compatibility calls를 구성한다. output 무오류 보장은 없으므로 compilation/semantic 검증을 유지한다.'),
('Six 1.10의 single-file distribution은 shared grammar helper를 쉽게 포함하는 방법이다.','공통 parseable source와 배포 helper를 연결한다. old parser가 모르는 syntax를 helper 호출만으로 무력화한다고 하지 않는다.')])]:
 for rank,(why,bridge) in enumerate(items,1):put('C26',a,rank,'PPP',why,bridge,date='unknown' if a=='A' and rank==2 else None)
# C27: necessary label disambiguation must not be silently dropped.
put('C27','A',1,'PPP','full keyword selector identity는 인수 타입 없이 label-different method 이름을 구별한다.','compound name의 모든 label을 identity로 보존하고 receiver binding/static signature check를 별도 연결한다. SEL 이름 자체를 typed bound callable로 취급하지 않는다.')
put('C27','A',2,'PUP','underscore placeholder로 익명 adapter를 생성하는 gold 대안은 회수했다. 그러나 label-only overload의 적용 규칙은 원 응답에서 미확인이다.','labeled abbreviated call을 forwarding callable로 낮춘다. expected type 또는 explicit placeholder type이 필요하며 동일 타입/다른 label 구별의 target rule이 미완이다.',('S0021-G02',),label='INSUFFICIENT',remaining='동일 인수 타입·다른 label 두 overload를 Scala식 placeholder로 각각 선택하는 Swift 의미 규칙/예시를 고정하면 H2를 재판정한다.')
put('C27','A',3,'PPP','Smalltalk keyword symbol은 모든 label segment를 identity에 포함한다.','colon-terminated selector segments를 interned full-name key로 대응하고 Swift compiler의 resolution/binding으로 연결한다. symbol을 callable implementation으로 동일시하지 않는다.')
put('C27','A',4,'PUP','arity 식별은 같은 arity와 다른 label을 분리하지 못한다. 제안은 grammar 참고로 좁혀서 near-miss 오주장으로 세지 않지만 필요한 richer identity가 미정이다.','짧은 name/arity reference를 forwarding closure로 desugar하는 문법을 참고할 수 있다. label-aware identity는 원 후보에서 구체 해결하지 않은 추가 설계다.',label='INSUFFICIENT',remaining='arity를 대체/확장할 전체 label identity와 동일 arity 반례 두 개의 resolution 규칙을 제시하면 H2를 재판정한다.')
put('C27','B',1,'PUP','Elixir name/arity capture는 label-only 구별에 직접 대응하지 않는다. 추가 identity field를 labels로 번역한다는 추론은 있으나 resolution 규칙이 남는다.','compact capture syntax의 추가 identity를 Swift labels에 대응시킬 수 있으나 same-arity overload와 foreign-selector mapping은 별도 규칙이 필요하다.',label='INSUFFICIENT',remaining='전체 label sequence를 capture identity로 사용하는 문법과 동일 arity/타입 overload 2개의 정적 resolution을 고정하면 H2를 재판정한다.')
# C28
put('C28','A',1,'NPN','nameof가 검증된 source identifier에서 name을 생성하는 좁은 component이다.','qualified symbol lookup을 먼저 수행해 오타·없는 선언을 거절한다. 출력 source name을 ObjC selector로 바꾸는 mapping은 별도다.')
put('C28','A',2,'PPN','@selector spelling은 gold의 Objective-C 표기 대안을 그대로 회수했다. 동적 receiver check라는 한계도 명시했다.','compound selector literal→SEL→respondsToSelector 검사로 연결한다. SEL은 클래스 공통 이름이며 Swift rename mapping이나 compile-time class membership을 보장하지 않는다.',('S0022-G02',))
put('C28','A',3,'NPN','typed member pointer로 misspelling/signature 오류를 거절하지만 typed SEL 호출 규약 자체는 아니다.','checked class-qualified method reference를 callback registration에 연결한다. Qt pointer/metadata를 ObjC SEL로 바꾸는 bridge가 필요하다.')
put('C28','A',4,'PPP','typed expression에서 declaration identity를 얻고 bridge metadata를 찾는 부분 경로다.','checked lambda의 MethodCallExpression에서 선택 method를 추출한 뒤 importer metadata로 외부 selector를 조회한다. Swift compiler 지원이 필요하고 expression tree 그대로 이식은 아니다.')
put('C28','A',5,'PNP','declaration에 foreign spelling을 보존하는 metadata가 이름 mapping의 원리다. typo 검증 자체는 처음부터 별도라고 명시한다.','host method에 ObjC spelling을 부착해 checked reference가 선언 metadata를 조회하게 한다. attribute string의 검증은 이 후보만으로 해결되지 않는다.')
put('C28','A',6,'NPN','visible declaration을 찾는 selector warning의 부분 기여다.','selector expression을 보이는 method declaration과 대조하여 없는 이름을 경고한다. intended receiver class와 imported rename mapping은 별도다.')
put('C28','B',1,'PPN','receiver-aware selector check는 README에서 확인했다. typed selector calling-convention gold의 같은 실체는 아니다.','특정 receiver가 selector를 선언했는지 compile-time 검사한다. Swift importer의 source-to-runtime name mapping을 별도 연결하고 ARC 의존성을 보존한다.')
put('C28','B',2,'PPP','typed method reference에서 generated runtime index로의 mapping을 갖춘 관련 구조다.','compiler가 method를 검사하고 generated metadata가 runtime identifier를 만든다. Qt signal index와 ObjC SEL의 형식/lookup은 구별한다.')
put('C28','B',3,'PNP','공통 interface에서 언어별 이름을 생성하는 mechanism이 확인됐다.','declaration identity를 공통 모델에 두고 Swift/ObjC 표면 이름을 생성 metadata로 연결한다. arbitrary imported APIs에는 importer 또는 generator 통합이 필요하다.')
put('C28','B',4,'PPP','resource string 대신 typed generated accessor를 쓰는 설계 전이다.','imported method metadata에서 class-scoped Swift identifiers를 생성하여 spelling errors를 compiler missing-symbol로 바꾼다. collisions와 API 변경 regeneration을 처리하며 resource tool 자체의 SEL 지원은 주장하지 않는다.')
# C29
for a,items in [('A',[
('Scala enclosing-template와 object-local 권한은 source-file 경계와 다르다.','member owner/receiver를 access check에 사용하고 companion·extension 권한을 명시한다. private[this]를 일반 type-private와 같다고 하지 않는다.'),
('C++ private와 friendship은 같은 파일의 unrelated type 접근을 거절한다.','declaring type과 explicit friend 집합을 permission boundary로 사용한다. 이름이 lookup에 보이는 것과 access 허용 및 completion filtering을 구별한다.'),
('Java SE8 top-level-class private는 옆 top-level class를 차단한다.','enclosing top-level class를 정적 access domain으로 삼는다. nested class 허용 범위와 Swift extension는 별도 결정이다.'),
('C# partial declarations가 같은 type의 private 권한을 공유한다. 나중 Swift의 extension 간 private 공유 재설계를 앞서 검토할 수 있는 구체 사례다.','여러 declaration block을 동일 type identity로 묶어 private access를 결정한다. 같은 파일 조건과 unrelated type 차단은 Swift에서 별도 명시하며 원 gold에는 소급 추가하지 않는다.'),
('OCaml signature restriction은 helper를 숨기는 interface compartment이다. Swift scoped namespace와 공개 interface 형식이 달라 이름만 같다고 적중 처리하지 않는다.','structure를 정의할 때 signature로 제한해 공개 binding으로 raw implementation을 누출하지 않는다. explicit interface 작성 비용과 nested grouping이 추가된다.'),
('Eiffel selective export는 모든 same-file code 대신 지정 client에게 접근을 준다.','secret/export client set을 compiler access rule에 연결한다. client descendants와 qualified/unqualified call 차이를 보존한다.'),
('Clang code는 declaring/access context를 실제로 비교하는 구현 참고다.','declaration에 access를 기록하고 enclosing context와 owner/friend를 비교해 진단한다. C++의 맥락/친구 규칙을 Swift에 맞춰야 하며 실행 검증은 없다.')]),('B',[
('Ada private declarative region은 명시적 interface/implementation 경계의 한 사례다.','private list를 target class/extension visibility 영역에 대응하되 child-unit 권한을 Swift에 자동 부여하지 않는다. community 2022 rendering의 한계를 보존한다.'),
('Pony field privacy는 compiler-enforced type boundary이며 method privacy는 더 넓다는 한계를 명시했다.','underscore field를 type-owned private state로 대응한다. methods의 module/package visibility를 class-only 보호로 확대하지 않는다.')])]:
 for rank,(why,bridge) in enumerate(items,1):put('C29',a,rank,'PPP',why,bridge)
# C30
put('C30','A',1,'PPP','validated Vec adoption과 valid-input borrowed lossy path를 구별했다.','bounds가 있는 owned buffer를 검증한 뒤 same allocation의 String으로 이동한다. foreign ownership/layout이 다르면 재사용을 보장하지 않고 repair allocation을 허용한다.')
put('C30','A',2,'PPP','explicit input/output length와 strict/substitution error policy가 있는 bulk converter이다.','selected byte span과 destination capacity를 decoder에 전달한다. representation 변경용 storage와 optional sizing pass는 필요하며 lenient variant를 validation과 바꾸지 않는다.')
put('C30','A',3,'UUU','정확한 counted initializer의 행위는 snippet만 있고 열린 HTML/Markdown은 metadata만 확인됐다. 기존 Foundation interop 경로는 named component로 회수했으나 성능 개선은 입증하지 못했다.','NSString counted decode→Swift interop 경로를 검토 대상으로 지목했다. 실제 length/NUL/error 동작과 Swift bridge cost는 보강해야 한다.',('S0027-G04',),label='INSUFFICIENT',remaining='Apple initializer 본문과 해당 Swift bridge 구현/고정 판을 읽어 NUL·encoding·복사 여부 및 bridge 비용을 확인하면 E/H를 재판정한다.')
put('C30','A',4,'PPP','explicit size 경로와 sentinel default 경로를 구별했고 error replacement/suppression을 명시했다.','정확한 buffer length로 UTF decoding을 호출한다. negative size/default나 다른 convenience constructor의 NUL behavior를 섞지 않고 엄격 rejection 필요시 별도 계약을 둔다.')
put('C30','A',5,'PPP','begin/end 범위와 encoding/policy를 받는 bulk conversion이다.','framing parser가 결정한 범위를 decode에 전달하고 출력 storage와 error policy를 선택한다. backend 지원 encoding과 boundary code-unit 절단을 확인한다.')
put('C30','A',6,'PPP','bounded ByteBuffer→CharBuffer의 incremental decode/finalize를 제시했다. search metadata만으로 post-decision을 확정한 날짜는 재판정한다.','chunk boundary와 underflow/overflow를 보존하고 final input 뒤 flush/finalize한다. partial sequences·output capacity 관리가 필요하다.',date='unknown')
put('C30','A',7,'PPP','checked iterator-range conversion과 explicit repair/output 관리의 제한을 보존한다.','input begin/end와 preallocated/capacity-managed output iterator를 연결한다. unchecked variants나 반복 reallocating back insertion을 안전·빠른 경로로 동일시하지 않는다.')
put('C30','B',1,'PPP','counted input/NUL flag와 error returns, decomposition/reencoding의 storage 제어를 확인했다.','explicit count로 interior NUL을 보존하고 낮은 수준의 caller buffer API를 선택한다. convenience map allocation과 optional text transformation은 별도다.')
put('C30','B',2,'NPP','StringRef는 bounded storage/ownership의 부분 기여이며 Unicode validation을 제공한다고 주장하지 않는다.','pointer+length와 copy/borrow 선택을 노출하고 borrow lifetime을 보장한다. Unicode validator/decoder는 별도 단계로 연결하며 raw view를 유효 Unicode로 승격하지 않는다.')
put('C30','B',3,'PPP','validating SIMD bulk conversion과 caller storage가 명시된 사후 구현 참고다.','input count와 encoding을 validating converter에 전달하고 destination capacity를 제공한다. assume-valid API를 대체하지 않고 Swift storage ownership을 별도 연결한다.')
# C31
put('C31','A',1,'PPP','StrictVersion과 LooseVersion은 둘 다 실제 comparator를 명시해 두 gold 실체를 회수한다. loose의 prerelease 순서 실패도 보존한다.','기존 parser/comparator를 baseline으로 비교 test를 만들고 constrained/prerelease 규칙과 permissive legacy 처리의 차이를 분리한다. LooseVersion을 semantic ordering의 무조건 정답으로 채택하지 않는다.',('P0386-G01','P0386-G02'))
put('C31','A',2,'PPP','Debian epoch/upstream/revision 비교는 확인되나 setuptools와 hyphen 의미가 다르다는 특정 gold 비교는 원 응답에 없다.','numeric/text run comparator와 upstream/distribution fields를 Python adapter에 대응하고 scheme-change에는 epoch를 분리한다. punctuation/prerelease/revision mapping은 명시 계약으로 남긴다.')
put('C31','A',3,'PPP','Ivy의 semantic comparator와 pluggable special-word 정책 및 ranges가 확인됐다. date-order 대안의 부적합을 명시적으로 제외했다.','producer/consumer가 공통 latest strategy를 정하고 비교 결과에 inclusive/exclusive bounds를 적용한다. upload date를 의미 순서로 쓰지 않는다.')
put('C31','A',4,'PPP','RPM EVR/rpmvercmp는 distribution comparator지만 날짜→일반 숫자로 전환하는 gold 반례를 원 응답에서 직접 제시하지 않는다.','EVR fields와 numeric/alpha segments를 adapter 비교 계약으로 매핑한다. malformed labels, missing epoch, 비대칭 edge cases를 사전에 검증한다.')
put('C31','A',5,'PPP','Gem version objects와 requirement predicates를 분리하여 actual comparison을 보여 준다.','버전 parser/canonical comparison와 operator bounds를 연결한다. arbitrary legacy spelling과 prerelease를 자동 호환으로 취급하지 않고 mapping tests를 둔다.')
put('C31','A',6,'PPP','Maven ComparableVersion은 혼합 token의 구현 comparator이며 범위 metadata만 있는 후보와 다르다.','numbers/text/separators를 canonical comparison에 넣고 known/unknown qualifier 순서를 정한다. Python/OS separator semantics는 대조 확인을 전제로 둔다.')
put('C31','B',1,'PPP','Repology는 heterogeneous spelling의 실제 comparator와 bound sentinel을 제시한다.','numeric/alphabetic components와 release ranks를 비교하고 bounds로 interval membership를 판단한다. heuristic suffix collapse와 ordering≠API compatibility를 보존한다.')
put('C31','B',2,'PUP','SemVer의 deterministic ordering은 확인되나 기존 날짜/배포판 표기의 mapping을 후보가 추가 필요로 남긴다. 이 후보를 heterogeneous legacy 비교의 유용성 통과로 자동 승격하지 않는다.','producer가 채택한 grammar 안에서는 numeric/prerelease precedence로 범위를 계산한다. legacy/distribution versions의 구체 migration mapping이 없고 compatibility declaration 검증이 필요하다.',label='INSUFFICIENT',remaining='날짜 버전·Debian revision·비정형 prerelease 각 1개를 포함한 실제 기존 문자열을 SemVer에 정보 손실 없이 정규화하는 규칙을 고정하면 H2를 재판정한다.')

# Conservative historical-source correction: archive identity/copyright footer alone does not date exact Qt text.
D[('C22','A',2)]['date']='unknown'
D[('C22','A',2)]['why']+=' 원 실행의 날짜 근거는 Qt 4.7 archive 명칭과 2008–2010 copyright footer뿐이며 정확한 본문 판 날짜는 확인하지 못했다.'

CODE={'P':'pass','N':'not_in_scope','U':'unknown','F':'fail'}
J=[]
for cid in [f'C{x:02}' for x in range(21,32)]:
 c=CASES[cid]
 gold={g['id']:g for g in c['gold_items']}
 for a in ['A','B']:
  r=json.loads((B/f'runs/{a}/{cid}.json').read_text())
  for cand in r['candidates']:
   k=(cid,a,cand['rank']);d=D[k];assert len(d['codes'])==len(c['mandatory_constraints']),k
   matched=[]
   for gid in d['gold']:
    g=gold[gid]
    kind=g.get('match_kind','external_entity')
    if gid in ['S0018-G05','S0021-G02']:kind='structural_design'
    matched.append({'gold_id':gid,'match_kind':kind,'rationale':d['why']})
   judged=d['date'] or cand['date_status']
   if judged not in ['pre_decision','post_decision','unknown']:raise ValueError(judged)
   ids=[m['gold_id'] for m in matched]
   evidence=[f'runs/{a}/{cid}.json#candidates/rank={cand["rank"]}',f'runs/{a}/{cid}.json#raw_response']
   urls={cand['url']}
   extra_keys=['verification_source_urls','verification_sources','verification_chain']
   for ek in extra_keys:
    if isinstance(cand.get(ek),list):urls.update(cand[ek])
   for n,doc in enumerate(r['opened_documents']):
    if doc['url'] in urls or doc.get('redirected_url') in urls:evidence.append(f'runs/{a}/{cid}.json#opened_documents/{n}')
   if cid=='C21' and a=='A' and cand['rank']==3:evidence.append('evidence/judging-recovery/c21-c31/sources.json#JR2131-S01')
   if cid=='C22' and a=='B' and cand['rank']==5:
    for n,doc in enumerate(r['opened_documents']):
     if 'tutorial.ponylang.io/capabilities/reference-capabilities' in doc['url']:evidence.append(f'runs/B/C22.json#opened_documents/{n}')
   unknown=(d['label']=='INSUFFICIENT')
   e='unknown' if cid=='C30' and a=='A' and cand['rank']==3 else 'supported'
   useful=not ids and not unknown and e=='supported'
   h=[]
   for con,code in zip(c['mandatory_constraints'],d['codes']):
    val=CODE[code]
    reason=d['why']+' '+('이 조건의 전체 구현은 처음부터 후보가 주장한 좁은 사용 범위 밖이다.' if val=='not_in_scope' else 'reference_design에서 제시된 부분/조건에 대한 판정이며 전체 구현 성공은 아니다.' if val=='pass' else d['remaining'] or '원 응답이 필수 연결을 추가 설계로 남겼다.')
    h.append({'constraint_id':con['id'],'value':val,'reason':reason})
   row={
    'case_id':cid,'baseline':a,'rank':cand['rank'],'candidate_name':cand['name'],'candidate_url':cand['url'],
    'gold_matches':matched,'review_matches':[],'L':'ok','E':e,'H':h,
    'T':'mapped' if not unknown else 'unknown','transfer_mapping':{'source_mechanism':cand['reason'],'target_scope':cand.get('application_scope'),'bridge_and_failure_conditions':d['bridge'],'source_caveat':cand.get('constraints_or_caveat')},
    'H_assessment_scope':'reference_design','runtime_observation':'not_performed','label':d['label'],
    'link_status':'reachable_metadata_only' if e=='unknown' else 'redirected_primary_verified' if cid=='C22' and a=='B' and cand['rank']==5 else 'opened_primary',
    'date_status':cand['date_status'],'original_date_status':cand['date_status'],'judged_date_status':judged,
    'date_evidence':cand.get('date_evidence'),'date_correction_reason':None if not d['date'] else d['why'],
    'strict_historical_gold_ids':ids if judged=='pre_decision' else [],'post_decision_gold_ids':ids if judged=='post_decision' else [],'date_unknown_gold_ids':ids if judged=='unknown' else [],
    'nongold_useful':useful,'nongold_historical_useful':useful and judged=='pre_decision','near_miss':False,'broken_or_fake':False,'exclusion':None,
    'judge':'내부 별도 검토','evidence_locations':evidence,
    'remaining_check':d['remaining'] or ('고정된 cutoff 이전 판의 동일 mechanism 본문을 열면 역사 적격성을 확인할 수 있다.' if judged=='unknown' else '실제 Swift/Rust/Python 적용은 별도 prototype으로 조건과 경계를 검증한다.'),
    'judgment_note':d['why'],'run_exposure_count':len(r.get('exposures',[]))
   }
   if cid=='C21' and a=='A' and cand['rank']==3:row['baseline_evidence_limit']='원 실행의 detailed receiver rules는 snippet-only; E supported는 판정 단계의 원문 보강으로 확보했다. 원 실행 예산/원 응답은 변경하지 않았다.'
   J.append(row)
expected=sum(len(json.loads((B/f'runs/{a}/C{x:02}.json').read_text())['candidates']) for x in range(21,32) for a in ['A','B'])
assert len(J)==expected==len(D),(len(J),expected,len(D))
(O/'judgments.json').write_text(json.dumps({'schema_version':1,'judge':'내부 별도 검토','scope':'C21–C31; original A/B responses unchanged; explicit manual decisions in build_judgments.py','judgments':J},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(J),'A':sum(j['baseline']=='A' for j in J),'B':sum(j['baseline']=='B' for j in J),'labels':{v:sum(j['label']==v for j in J) for v in sorted(set(j['label'] for j in J))},'nongold_useful':sum(j['nongold_useful'] for j in J),'strict_nongold_useful':sum(j['nongold_historical_useful'] for j in J),'gold_case_pairs':{a:len({(j['case_id'],m['gold_id']) for j in J if j['baseline']==a for m in j['gold_matches']}) for a in ['A','B']}},ensure_ascii=False))
