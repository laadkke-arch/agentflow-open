# AF-RES-013 — 설계 문서의 선행 사례·대안 기준선

## §1 필수 결과 표

### 표 1 — 사례별 결과

| 사례 ID | 계열 | 원문 주소(고정 판) | 결정일 | 정답 항목 수(완성품·부품·같은 분야 설계·다른 생태계·다른 분야·표준논문) | 기준선 A 적중 | 기준선 B 적중 | 놓친 정답 항목 | 정답원 밖 유용 후보 | 근접 오답 | 깨진·가짜 링크 | 누설·사후 자료 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | Kubernetes KEP | [K0019](https://github.com/kubernetes/enhancements/blob/4921704140fabb9c616607df44e8c1fd6ea96541/keps/sig-apps/19-Graduate-CronJob-to-Stable/README.md) | 2020-10-02 | 0·0·7·0·0·0 | 동일 1/7; 이전 0/7 | 동일 0/7; 이전 0/7 | 공통: G01 Unordered timer list; G02 Ordered timer list; G03 Timer trees; G05 Simple Timing wheels; G06 Hashed Wheel; G07 Hierarchical Wheel / A만: 없음 / B만: G04 Heap based timer | A 5/7 (이전 1); B 4/4 (이전 4) | A 0/8; B 0/4 | A 0/8; B 0/4 | 노출기록 A0·B1; 사후 후보 A1·B0 | 미확인(날짜 A6·B0행은 결정 전 고정 판 확인; 판정 불충분 A2·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C02 | Kubernetes KEP | [K0127](https://github.com/kubernetes/enhancements/blob/a61d587aa5db7c00e727fa4c2598fc1914d9784f/keps/sig-node/127-user-namespaces/README.md) | 2023-02-07 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 Change ownership of all relevant files instead of idmapped mounts; G02 Limit pod count to reserve UID ranges with 64K mappings; G03 Allow container runtimes to choose ID mappings / A만: 없음 / B만: 없음 | A 7/8 (이전 2); B 6/7 (이전 0) | A 1/8; B 1/7 | A 0/8; B 0/7 | 노출기록 A3·B2; 사후 후보 A1·B1 | 미확인(날짜 A4·B6행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C03 | Kubernetes KEP | [K0277](https://github.com/kubernetes/enhancements/blob/e0640b65b0d8180779218b14858c5b129d5ac80b/keps/sig-node/20190212-ephemeral-containers.md) | 2019-04-16 | 0·0·10·0·0·0 | 동일 0/10; 이전 0/10 | 동일 0/10; 이전 0/10 | 공통: G01 Store container specification in PodStatus; G02 Extend existing exec API to execute container images (exec++); G03 Dedicated EphemeralContainer resource and kubelet controller; G04 Allow adding containers by mutating pod specification; G05 Add an Image parameter to exec without spec or status; G06 Attach a volume containing debugging tools; G07 Configure an inactive debug container in advance; G08 Implicit EmptyDir for extracting debug binaries; G09 Separate debug pod sharing target namespaces; G10 Execute troubleshooting binary from node in target namespaces / A만: 없음 / B만: 없음 | A 7/7 (이전 3); B 4/6 (이전 0) | A 0/7; B 1/6 | A 0/7; B 0/6 | 노출기록 A0·B6; 사후 후보 A1·B2 | 미확인(날짜 A3·B4행은 결정 전 고정 판 확인; 판정 불충분 A0·B1행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C04 | Kubernetes KEP | [K0279](https://github.com/kubernetes/community/blob/c2c1ace9963b45522fdb8f8d752b0613baec9f5d/keps/sig-auth/0000-20170814-bounding-self-labeling-kubelets.md) | 2018-11-12 | 0·0·4·0·0·0 | 동일 0/4; 이전 0/4 | 동일 0/4; 이전 0/4 | 공통: G01 Configure allowed labels using API-server files or flags; G02 API object configures allowed label policy; G03 Allow arbitrary labels then add NoSchedule taints; G04 Reject every label except a fixed allowlist / A만: 없음 / B만: 없음 | A 8/8 (이전 2); B 5/5 (이전 2) | A 0/8; B 0/5 | A 0/8; B 0/5 | 노출기록 A0·B0; 사후 후보 A1·B1 | 미확인(날짜 A5·B2행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C05 | Kubernetes KEP | [K0383](https://github.com/kubernetes/community/blob/c5b815bf44dd6f623ef2b4cf80cf5194bcfa38d5/contributors/design-proposals/events-redesign.md) | 2017-09-27 | 0·0·6·0·1·0 | 동일 0/7; 이전 0/7 | 동일 0/7; 이전 0/7 | 공통: G01 Keep deduplication and strengthen batching/backoff/rate limits; G02 Store a list of occurrence timestamps; G03 One aggregate object with nested timestamp-object occurrences; G04 Store in new API group and retain deprecated fields as annotations; G05 Administrative panic switch disables event creation and updates; G06 Impose active-voice subject/object structure for machine-readable events; G07 Center reporting controller and log-grep links for operator debugging / A만: 없음 / B만: 없음 | A 4/7 (이전 3); B 5/9 (이전 4) | A 0/7; B 0/9 | A 0/7; B 0/9 | 노출기록 A0·B0; 사후 후보 A0·B3 | 미확인(날짜 A3·B2행은 결정 전 고정 판 확인; 판정 불충분 A3·B4행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C06 | Kubernetes KEP | [K0495](https://github.com/kubernetes/community/blob/333729bd66910b3c0b45aa74a8a54b5c9075226b/contributors/design-proposals/node/pod-pid-namespace.md) | 2018-01-24 | 0·0·3·0·0·0 | 동일 1/3; 이전 1/3 | 동일 1/3; 이전 0/3 | 공통: G02 Always share PID namespace when runtime supports it; G03 Use annotations then migrate to shared-only namespaces in v2 / A만: 없음 / B만: 없음 | A 4/5 (이전 3); B 3/3 (이전 0) | A 1/7; B 0/4 | A 0/7; B 0/4 | 노출기록 A3·B0; 사후 후보 A1·B1 | 미확인(날짜 A2·B3행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C07 | Python PEP | [P0201](https://github.com/python/peps/blob/8a03f9cff101e1e7c63c85a48cb2487e4839574d/pep-0201.txt) | 2000-08-03 | 0·1·5·1·0·0 | 동일 1/7; 이전 1/7 | 동일 1/7; 이전 0/7 | 공통: G01 map(None, ...); G02 for x in seq1, y in seq2 문법; G03 for x, y in seq1, seq2 문법; G06 __getitem__ 기반 지연 반환 객체; G07 내부·외부 컨테이너 타입을 호출자가 선택 / A만: G05 선택적 pad 인수 / B만: G04 Haskell zip | A 4/4 (이전 1); B 3/3 (이전 3) | A 0/5; B 0/4 | A 0/5; B 0/4 | 노출기록 A0·B1; 사후 후보 A0·B0 | 미확인(날짜 A3·B1행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C08 | Python PEP | [P0202](https://github.com/python/peps/blob/ff898c8e8a69e31b05873ca8c5fdf88dd6ee9c2f/pep-0202.txt) | 2000-07-27 | 0·2·4·0·0·0 | 동일 1/6; 이전 1/6 | 동일 1/6; 이전 1/6 | 공통: G01 map(); G02 filter(); G03 명시적 중첩 for 반복문; G04 괄호 없는 다중 출력식 [x, y for ...]; G05 세미콜론으로 절을 분리하는 구문 / A만: 없음 / B만: 없음 | A 3/3 (이전 0); B 4/4 (이전 0) | A 0/4; B 0/5 | A 0/4; B 0/5 | 노출기록 A0·B0; 사후 후보 A2·B4 | 미확인(날짜 A1·B0행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C09 | Python PEP | [P0204](https://github.com/python/peps/blob/2ec18ca954c8041761f3891c20c092f03471daa3/pep-0204.txt) | 2000-11-01 | 0·2·7·0·0·0 | 동일 2/9; 이전 2/9 | 동일 0/9; 이전 0/9 | 공통: G02 확장 슬라이스의 시작:끝:간격 표기; G04 튜플 범위 구문을 지연 생성기로 구현; G05 일반 리스트 원소와 범위 리터럴을 한 목록에 혼합; G06 리스트 생성 구문 안의 범위를 평탄한 단일 리스트로 합침; G07 리스트 생성 구문 안의 범위를 리스트의 리스트로 보존; G08 범위 결과가 입력 값의 타입을 보존; G09 범위 생성 C 보조 함수를 비공개 구현으로 유지 / A만: 없음 / B만: G01 range() 내장 함수; G03 xrange형 지연 생성기 | A 3/5 (이전 2); B 5/5 (이전 0) | A 1/6; B 0/5 | A 0/6; B 0/5 | 노출기록 A3·B1; 사후 후보 A1·B4 | 미확인(날짜 A1·B1행은 결정 전 고정 판 확인; 판정 불충분 A1·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C10 | Python PEP | [P0354](https://github.com/python/peps/blob/e31746e7fc5689491e7ea0d4a1b9c915358b18db/pep-0354.txt) | 2007-05-18 | 0·0·4·0·0·0 | 동일 1/4; 이전 1/4 | 동일 0/4; 이전 0/4 | 공통: G02 메타클래스로 각각의 열거형 클래스를 생성; G03 열거 값을 정수·문자열 값에 강하게 연결; G04 열거 값의 문자열 키와 순서 인덱스를 숨김 / A만: 없음 / B만: G01 열거형과 값을 하나의 클래스·객체에 결합 | A 3/3 (이전 2); B 1/3 (이전 0) | A 0/5; B 0/3 | A 0/5; B 0/3 | 노출기록 A5·B23; 사후 후보 A0·B1 | 미확인(날짜 A2·B2행은 결정 전 고정 판 확인; 판정 불충분 A0·B2행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C11 | Python PEP | [P0433](https://github.com/python/peps/blob/0efb6d7b3ec34a093a341551d7209aaf6e9dff2b/pep-0433.txt) | 2013-08-28 | 0·0·5·5·0·0 | 동일 1/10; 이전 0/10 | 동일 0/10; 이전 0/10 | 공통: G01 상속 기본값 False 변경 없이 선택적 cloexec만 추가; G02 전역 기본값을 한 방향으로만 변경하는 설정; G04 fork 직후 atfork 콜백으로 디스크립터 닫기; G05 open 모드에 e 플래그 추가; G06 GNU libc fopen의 e 모드; G07 Visual Studio fopen의 N 모드; G08 Perl SYSTEM_FD_MAX에 따른 상속 제한; G09 Ruby의 FD_CLOEXEC 기본 설정 및 일부 되돌림; G10 OCaml Unix.set_close_on_exec 및 프로세스 상속 이슈 / A만: 없음 / B만: G03 비상속을 기본으로 하고 필요한 디스크립터만 상속 | A 8/8 (이전 3); B 6/6 (이전 2) | A 1/9; B 0/6 | A 0/9; B 0/6 | 노출기록 A5·B1; 사후 후보 A4·B4 | 미확인(날짜 A2·B0행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C12 | Python PEP | [P0509](https://github.com/python/peps/blob/fd5c057e268dce0c88fc7fb921e61190b6c2d3bb/pep-0509.txt) | 2016-09-08 | 0·2·6·0·0·0 | 동일 0/8; 이전 0/8 | 동일 0/8; 이전 0/8 | 공통: G01 Python 수준 read-only __version__ 속성; G02 사전 엔트리별 버전 태그; G03 버전을 가진 새 dict 하위 타입 verdict; G04 CPython method cache와 tp_version_tag; G05 Globals / builtins cache issue10401; G06 Cached globals+builtins lookup issue1616125; G07 사전 반복 중 변경 감지 issue19332; G08 PySizer의 dict 엔트리 시간 기록 / A만: 없음 / B만: 없음 | A 4/7 (이전 3); B 2/4 (이전 0) | A 0/7; B 0/4 | A 0/7; B 0/4 | 노출기록 A13·B0; 사후 후보 A1·B1 | 미확인(날짜 A1·B3행은 결정 전 고정 판 확인; 판정 불충분 A3·B2행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C13 | Python PEP | [P0554](https://github.com/python/peps/blob/6aeaba7f23a1ce373e099a2b35db9525dbb11f6d/peps/pep-0554.rst) | 2023-11-28 | 0·2·17·0·0·0 | 동일 0/19; 이전 0/19 | 동일 0/19; 이전 0/19 | 공통: G01 concurrent.futures에 인터프리터 지원 추가; G02 multiprocessing에 인터프리터 지원 추가; G03 채널을 명시적으로 연결·해제하는 메서드; G04 정확히 두 인터프리터 사이의 단방향 pipe API; G05 Queue 기반 API; G06 원래 예외 객체와 traceback을 그대로 전파; G07 원 예외와 traceback을 호출 인터프리터에 복제; G08 원 예외를 프록시하는 RunFailedError 하위 클래스; G09 RunFailedError 대신 RuntimeError 발생; G10 CalledProcessError처럼 경계에서 예외 표현을 변환; G11 Interpreter.excepthook으로 변환을 사용자 정의; G12 경계의 프록시와 err.raise()로 원 traceback 전달; G13 exec가 예외 또는 프록시를 반환; G14 subprocess형 실행 결과 객체 반환; G15 예외를 버리고 실행 스크립트가 채널로 처리; G16 새 인터프리터마다 전용 스레드를 자동 생성; G17 채널을 실제 send/recv할 때만 연결; G18 동시에 여러 Interpreter.exec 호출 허용; G19 RunFailedError.reraise() 또는 __reraise__ 프로토콜 / A만: 없음 / B만: 없음 | A 4/7 (이전 1); B 1/3 (이전 0) | A 0/7; B 0/3 | A 0/7; B 0/3 | 노출기록 A34·B15; 사후 후보 A1·B0 | 미확인(날짜 A5·B3행은 결정 전 고정 판 확인; 판정 불충분 A3·B2행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C14 | Python PEP | [P0563](https://github.com/python/peps/blob/cfa69b62a19c959b70e806591b2c9dbe93fd6e0b/pep-0563.rst) | 2017-12-04 | 0·0·5·0·0·0 | 동일 0/5; 이전 0/5 | 동일 0/5; 이전 0/5 | 공통: G01 annotation을 lambda로 보관하여 함수 지역 상태 유지; G02 클래스에서도 모듈 수준 이름만 사용; G03 __annotations_text__와 지연 __annotations__ 매핑을 병행; G04 -O 실행 옵션으로 annotation 제거; G05 문자열 리터럴 annotation의 내용만 그대로 저장 / A만: 없음 / B만: 없음 | A 4/6 (이전 4); B 3/3 (이전 1) | A 1/6; B 0/3 | A 0/6; B 0/3 | 노출기록 A2·B8; 사후 후보 A0·B0 | 미확인(날짜 A1·B2행은 결정 전 고정 판 확인; 판정 불충분 A1·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C15 | Rust RFC | [R0008](https://github.com/rust-lang/rfcs/blob/ef22d548abb5b85b08a5858cca2781e20e44f4bd/active/0000-new-intrinsics.md) | 2014-04-07 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 dedicated intrinsic attribute with redeclaration; G02 redeclared intrinsic language items; G03 intrinsic ABI coercion or ABI equivalence / A만: 없음 / B만: 없음 | A 2/5 (이전 2); B 2/3 (이전 1) | A 0/5; B 0/3 | A 0/5; B 0/3 | 노출기록 A0·B0; 사후 후보 A1·B1 | 미확인(날짜 A1·B1행은 결정 전 고정 판 확인; 판정 불충분 A3·B1행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C16 | Rust RFC | [R0016](https://github.com/rust-lang/rfcs/blob/12e924bdc86b9954fe249040cb2f1513de02299e/active/0000-more-attributes.md) | 2014-07-15 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 macros and helper-function approximation; G02 attributes restricted to statement expressions; G03 interior versus exterior conditional attributes / A만: 없음 / B만: 없음 | A 6/6 (이전 5); B 5/5 (이전 1) | A 0/6; B 0/5 | A 0/6; B 0/5 | 노출기록 A0·B0; 사후 후보 A0·B1 | 미확인(날짜 A1·B3행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C17 | Rust RFC | [R0042](https://github.com/rust-lang/rfcs/blob/c250f8bb0b249eedc0cbb24fbf1238320770fba1/active/0000-regexps.md) | 2014-04-22 | 0·1·2·0·0·0 | 동일 1/3; 이전 1/3 | 동일 1/3; 이전 1/3 | 공통: G01 backtracking engine with backreferences and zero-width assertions; G03 omit a regular-expression library from the distribution / A만: 없음 / B만: 없음 | A 6/6 (이전 3); B 3/3 (이전 0) | A 0/8; B 0/7 | A 0/8; B 0/7 | 노출기록 A3·B9; 사후 후보 A2·B2 | 미확인(날짜 A1·B2행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C18 | Rust RFC | [R0069](https://github.com/rust-lang/rfcs/blob/471fbe84b2873c9f9bab82e2ca84d5b311458bdb/active/0000-ascii-literals.md) | 2014-06-04 | 0·0·6·1·0·0 | 동일 1/7; 이전 1/7 | 동일 1/7; 이전 0/7 | 공통: G01 numeric byte literals in patterns; G02 cast individual bytes to character values; G03 pattern-capable byte macros; G05 ASCII-specific prefix a; G06 integer-style suffix u8; G07 UTF-8 encoding of literal code points / A만: 없음 / B만: 없음 | A 5/6 (이전 3); B 3/3 (이전 2) | A 0/7; B 0/4 | A 0/7; B 0/4 | 노출기록 A0·B2; 사후 후보 A0·B2 | 미확인(날짜 A3·B0행은 결정 전 고정 판 확인; 판정 불충분 A1·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C19 | Rust RFC | [R0085](https://github.com/rust-lang/rfcs/blob/59bdf1bd683e2872305a895d60406417c61f182c/active/0000-pattern-macros.md) | 2014-05-27 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 expand macros to an entire match-arm left side; G02 expand macros to a complete match arm; G03 procedural macro around the entire match expression / A만: 없음 / B만: 없음 | A 6/6 (이전 4); B 5/5 (이전 2) | A 0/6; B 0/5 | A 0/6; B 0/5 | 노출기록 A0·B0; 사후 후보 A1·B0 | 미확인(날짜 A1·B3행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C20 | Rust RFC | [R0093](https://github.com/rust-lang/rfcs/blob/86456e4b660243850e02dc6e1b134145983e33d3/active/0000-remove-format-intl.md) | 2014-06-11 | 0·2·1·0·0·0 | 동일 2/3; 이전 2/3 | 동일 1/3; 이전 0/3 | 공통: G03 adapt existing format-string syntax for l20n / A만: 없음 / B만: G01 l20n as the localization approach | A 3/3 (이전 3); B 6/6 (이전 3) | A 0/6; B 0/7 | A 0/6; B 0/7 | 노출기록 A0·B0; 사후 후보 A0·B0 | 미확인(날짜 A1·B4행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C21 | Rust RFC | [R0114](https://github.com/rust-lang/rfcs/blob/c3cf523156308cd72a739e0b94eca230ecfa7ff5/active/0000-closures.md) | 2014-07-30 | 0·0·9·0·0·0 | 동일 1/9; 이전 1/9 | 동일 0/9; 이전 0/9 | 공통: G01 general callable-trait syntax sugar; G02 rename callable traits to avoid bare-function confusion; G03 only by-value closures; G04 by-reference capture as the default; G06 retain the proc closure expression; G07 variadic generics instead of tuple arguments; G08 infer the closure receiver mode; G09 a receiver default other than mutable borrowing / A만: 없음 / B만: G05 per-variable borrowing capture clauses | A 3/7 (이전 3); B 2/4 (이전 1) | A 1/8; B 0/4 | A 0/8; B 0/4 | 노출기록 A0·B0; 사후 후보 A0·B1 | 미확인(날짜 A2·B2행은 결정 전 고정 판 확인; 판정 불충분 A3·B2행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C22 | Rust RFC | [R0123](https://github.com/rust-lang/rfcs/blob/1484eb420b0d5f37a7d2828413159a7c22ccb66e/active/0000-share-to-threadsafe.md) | 2014-08-05 | 0·0·8·0·0·0 | 동일 1/8; 이전 1/8 | 동일 1/8; 이전 0/8 | 공통: G01 Concurrent; G02 Synchronized; G04 Parallel; G05 Threaded; G06 Atomic; G07 DataRaceFree; G08 ConcurrentlySharable / A만: 없음 / B만: 없음 | A 3/3 (이전 2); B 3/3 (이전 1) | A 0/6; B 0/5 | A 0/6; B 0/5 | 노출기록 A1·B1; 사후 후보 A0·B0 | 미확인(날짜 A2·B4행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C23 | Swift Evolution | [S0016](https://github.com/swiftlang/swift-evolution/blob/36dd2cc2f0306785af461271feeeab788ca3c430/proposals/0016-initializers-for-converting-unsafe-pointers-to-ints.md) | 2016-03-31 | 0·0·2·1·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 포인터의 intValue 변환 메서드; G02 포인터 타입에 모든 산술·비트 연산 API 추가; G03 복잡한 포인터 조작을 C 코드로 작성 / A만: 없음 / B만: 없음 | A 7/7 (이전 4); B 2/2 (이전 2) | A 0/7; B 0/2 | A 0/7; B 0/2 | 노출기록 A0·B0; 사후 후보 A0·B0 | 미확인(날짜 A3·B0행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C24 | Swift Evolution | [S0018](https://github.com/swiftlang/swift-evolution/blob/7778003344f926a503edbc14f95e2153dad6f7d9/proposals/0018-flexible-memberwise-initialization.md) | 2016-01-13 | 0·0·5·2·0·0 | 동일 3/7; 이전 1/7 | 동일 1/7; 이전 0/7 | 공통: G02 모든 initializer가 자동 참여; G03 initializer가 명시적으로 opt-out; G05 인수는 모두 선언하고 속성 대입만 합성 / A만: G04 initializer보다 덜 공개된 속성의 인수도 합성 / B만: G01 속성별 memberwise 명시 opt-in; G06 Kotlin의 타입 선언 매개변수·속성 문법; G07 Scala의 타입 선언 매개변수·속성 문법 | A 3/5 (이전 1); B 1/3 (이전 0) | A 0/8; B 0/4 | A 0/8; B 0/4 | 노출기록 A0·B1; 사후 후보 A1·B1 | 미확인(날짜 A5·B2행은 결정 전 고정 판 확인; 판정 불충분 A4·B2행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C25 | Swift Evolution | [S0019](https://github.com/swiftlang/swift-evolution/blob/2fdf30579c233ddb26a36a3e1a77bca9d9cef30a/proposals/0019-package-manager-testing.md) | 2016-01-21 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 Xcode형 Sources 옆 FooTests 디렉터리 배치; G02 테스트와 SwiftPM을 완전히 분리; G03 기본 XCTest 지원 없이 테스트 프로토콜만 제공 / A만: 없음 / B만: 없음 | A 7/7 (이전 3); B 7/7 (이전 0) | A 0/7; B 0/7 | A 0/7; B 0/7 | 노출기록 A0·B2; 사후 후보 A1·B1 | 미확인(날짜 A3·B6행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C26 | Swift Evolution | [S0020](https://github.com/swiftlang/swift-evolution/blob/b3c511881a9813105032b10fe6dac4351c6bd078/proposals/0020-if-swift-version.md) | 2016-01-21 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 문자열 리터럴로 버전 지정; G02 비교 연산자 없는 버전 숫자; G03 쉼표로 분리한 버전 인수 목록 / A만: 없음 / B만: 없음 | A 6/6 (이전 6); B 5/5 (이전 2) | A 0/6; B 0/5 | A 0/6; B 0/5 | 노출기록 A0·B1; 사후 후보 A0·B0 | 미확인(날짜 A0·B3행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C27 | Swift Evolution | [S0021](https://github.com/swiftlang/swift-evolution/blob/05ef3a9d51d81be80208a4d8d554a7eef2f8e3b5/proposals/0021-generalized-naming.md) | 2016-01-20 | 0·0·3·0·0·0 | 동일 1/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 프로퍼티 전체 접근 인터페이스를 보존하는 lens; G03 함수 이름에서 비어 있는 인수 레이블의 underscore 생략 / A만: 없음 / B만: G02 _ 자리표시자를 이용한 일반 partial application | A 2/3 (이전 2); B 0/1 (이전 0) | A 1/4; B 1/1 | A 0/4; B 0/1 | 노출기록 A1·B5; 사후 후보 A0·B0 | 미확인(날짜 A1·B1행은 결정 전 고정 판 확인; 판정 불충분 A1·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C28 | Swift Evolution | [S0022](https://github.com/swiftlang/swift-evolution/blob/bf1c86212314ed90e6b615ddf8db8c15eb00e201/proposals/0022-objc-selectors.md) | 2016-01-26 | 0·0·3·0·0·0 | 동일 0/3; 이전 0/3 | 동일 0/3; 이전 0/3 | 공통: G01 type-safe selector 호출 규약; G02 Objective-C형 @selector 표기; G03 특수한 Selector initializer / A만: 없음 / B만: 없음 | A 5/6 (이전 2); B 4/4 (이전 1) | A 1/6; B 0/4 | A 0/6; B 0/4 | 노출기록 A1·B1; 사후 후보 A2·B1 | 미확인(날짜 A2·B2행은 결정 전 고정 판 확인; 판정 불충분 A0·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C29 | Swift Evolution | [S0025](https://github.com/swiftlang/swift-evolution/blob/70116480493c158afc1d815057885ab0615fbebf/proposals/0025-scoped-access-level.md) | 2016-04-01 | 0·0·3·0·0·0 | 동일 1/3; 이전 1/3 | 동일 0/3; 이전 0/3 | 공통: G01 기존 이름 관례·파일 분리와 파일 수준 private 유지; G03 기존 private 명칭을 유지하고 새 modifier 추가 / A만: 없음 / B만: G02 파일 일부를 감싸는 scoped namespace | A 6/6 (이전 5); B 1/2 (이전 0) | A 0/7; B 0/2 | A 0/7; B 0/2 | 노출기록 A0·B0; 사후 후보 A0·B1 | 미확인(날짜 A1·B1행은 결정 전 고정 판 확인; 판정 불충분 A0·B1행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C30 | Swift Evolution | [S0027](https://github.com/swiftlang/swift-evolution/blob/83bdc871121565084645b8fe792874594ae18fed/proposals/0027-string-from-code-units.md) | 2016-02-23 | 0·2·3·0·0·0 | 동일 1/5; 이전 0/5 | 동일 0/5; 이전 0/5 | 공통: G01 현재 API를 유지; G02 mutable String.UTF8View와 UTF16View의 상각 O(1) append; G03 SequenceType의 프로토콜 중심 decode API; G05 String.append 성장 전략과 reserveCapacity 성능 개선 / A만: 없음 / B만: G04 NSString bridge 성능 개선 | A 4/6 (이전 0); B 2/3 (이전 0) | A 0/7; B 0/3 | A 0/7; B 0/3 | 노출기록 A0·B0; 사후 후보 A1·B1 | 미확인(날짜 A6·B2행은 결정 전 고정 판 확인; 판정 불충분 A3·B1행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |
| C31 | Python PEP | [P0386](https://github.com/python/peps/blob/b1c944fbd2c125a63c22a9b94f32d776e0cddc75/pep-0386.txt) | 2010-03-21 | 0·3·0·2·0·0 | 동일 2/5; 이전 2/5 | 동일 0/5; 이전 0/5 | 공통: G03 Setuptools pkg_resources.parse_version; G04 RPM의 날짜 버전에서 일반 숫자 버전으로의 전환; G05 Debian/Ubuntu 패키징의 하이픈 취급 / A만: 없음 / B만: G01 Distutils LooseVersion; G02 Distutils StrictVersion | A 4/5 (이전 1); B 2/2 (이전 0) | A 1/6; B 0/2 | A 0/6; B 0/2 | 노출기록 A2·B2; 사후 후보 A0·B0 | 미확인(날짜 A4·B2행은 결정 전 고정 판 확인; 판정 불충분 A1·B0행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가) |

### 표 2 — 역할별 집계

| 역할 | 정답 항목 수(분모) | 기준선 A 적중(비율) | 기준선 B 적중(비율) | 대표 놓침 사례 ID | 미확인 |
| --- | --- | --- | --- | --- | --- |
| 같은 목적 완성품 | 0 | 동일 0/0 (정의 불가); 이전 0/0 (정의 불가) | 동일 0/0 (정의 불가); 이전 0/0 (정의 불가) | A 해당 없음; B 해당 없음 | 미확인(분모가 있는 별도 표본으로 해당 역할의 회수율 확인) |
| 재사용 부품 | 17 | 동일 8/17 (47.1%); 이전 7/17 (41.2%) | 동일 2/17 (11.8%); 이전 1/17 (5.9%) | A C07, C08, C12, C13, C30; B C07, C08, C09, C12, C13 | 미확인(이 역할의 모집단 성능은 역할별 외부 표본을 추가하여 확인) |
| 같은 분야의 다른 설계 | 146 | 동일 10/146 (6.8%); 이전 6/146 (4.1%) | 동일 5/146 (3.4%); 이전 1/146 (0.7%) | A C01, C02, C03, C04, C05; B C01, C02, C03, C04, C05 | 미확인(이 역할의 모집단 성능은 역할별 외부 표본을 추가하여 확인) |
| 다른 언어·생태계 | 12 | 동일 4/12 (33.3%); 이전 3/12 (25.0%) | 동일 1/12 (8.3%); 이전 0/12 (0.0%) | A C11, C23, C31; B C07, C11, C23, C24, C31 | 미확인(이 역할의 모집단 성능은 역할별 외부 표본을 추가하여 확인) |
| 다른 분야 원리 | 1 | 동일 0/1 (0.0%); 이전 0/1 (0.0%) | 동일 0/1 (0.0%); 이전 0/1 (0.0%) | A C05; B C05 | 미확인(이 역할의 모집단 성능은 역할별 외부 표본을 추가하여 확인) |
| 표준·논문 | 0 | 동일 0/0 (정의 불가); 이전 0/0 (정의 불가) | 동일 0/0 (정의 불가); 이전 0/0 (정의 불가) | A 해당 없음; B 해당 없음 | 미확인(분모가 있는 별도 표본으로 해당 역할의 회수율 확인) |

### 표 3 — 주장 표

| 주장 | 근거 자료 주소 | 확인한 내용 | 반증 시도 | 미확인 |
| --- | --- | --- | --- | --- |
| Q4: 고정 규칙에 따른 역할 정정 후 다른 분야 원리·구조 항목은 1/176(0.57%)이다. | [사례와 최초 값](cases/CASES.json), [정정 근거](evidence/ROLE_CORRECTIONS.json), [내부 별도 검토](evidence/judgments/SECOND_REVIEW.json), [작동 원리 반례](https://www.rfc-editor.org/rfc/rfc8289.html) | KEP 1/34, Python 0/73, Rust 0/39, Swift 0/30. C05의 문법 역할→event field 구조 차용이며 별도 언어학 문헌 인용은 없다. 해당 항목 A/B 회수는 모두0/1. | 최초0/176은 외부 인용을 필요조건처럼 본 과도한 코딩을 원문·변경 없는 규칙으로 정정한 값이다. 최초0/0 회수율은 정의 불가, PySizer까지 넓히면2/176·회수0/2. CoDel은 표본 밖, P433 sterile/C22 Atom은 용어 차용으로 분리한다. | 미확인(이 목적 표본 밖 빈도는 시기·분야별 층화 표본과 경계 재판정으로 확인) |
| Q8: 반대 가설 A의 공식 기각 조건은 이번 결과만으로 판정할 수 없다. | [009 GAP §2·§3·§5](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md), [A 원 응답](runs/A/), [채점](JUDGMENTS.json) | A의 항목 동일성 22/176 (12.5%), 결정 이전 근거 16/176 (9.1%). 사전 지정한 새 절차·허용 오류·검토 시간과의 비교는 이번 실험에 없다. | 낮은 gold 회수가 별도 제품 필요라는 해석을 정답 밖 후보, 본문 내부 설계 비중, 코드검색 가용성, 노출 없는 부분집합으로 반박했다. | 미확인(실제 설계자가 새 절차와 기존 조합을 같은 과제·오류·시간 기준으로 비교) |
| Q8: 반대 가설 B도 공식 기각 또는 채택의 대상 비교가 부족하다. | [009 GAP §3](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md), [B 원 응답](runs/B/), [집계](evidence/AGGREGATES.json) | B의 항목 동일성 8/176 (4.5%), 결정 이전 근거 2/176 (1.1%). 번역자는 새 문맥 내부 모델이며 사람 개발자 번역 실험이 아니다. | 사후 A+B pool union은 동일 24/176, 이전 16/176이나 실제 통합 검색 실행이나 새 절차와의 대조로 취급하지 않는다. | 미확인(동일 목적·허용 오류·시간을 고정한 사람 번역 카탈로그와 새 절차 비교) |
| 정답원은 불완전하나, 더 나은 설계의 발견 건수로 환산할 수 없다. | [C22 리뷰](https://github.com/rust-lang/rfcs/pull/123), [C28 결정 토론](https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1), [후보별 판정](JUDGMENTS.json) | 본문 밖 리뷰 7항목 중 alias 1개를 빼면 2/31사례에서 6개 신규 항목, 확대 pool 182개다. 정답 밖 문서상 유용 후보는 A 146/178, B 105/126행이며 실제 우월성 입증은 0건이다. | C23의 실제 bit/pointer 원문처럼 유용하지만 gold의 내부 선택과 다른 후보를 보존했다. H unknown·위반 후보는 유용 수에서 제외했다. | 미확인(남은 리뷰 전체와 풀 밖 후보를 확장 평가하고 설계자가 유용성·우월성을 확인) |
| 링크 검증 후 제출한 후보에서는 가짜·다른 대상 링크를 관측하지 않았다. | [원 열람 기록](runs/), [URL 감사](evidence/RUN_AUDIT.json), [검증 보완](evidence/judgments/VERIFICATION.json) | A 0/204, B 0/138행. 실패·차단은 따로 보존했으며 403/timeout을 가짜로 세지 않는다. | fragment·redirect·HTTP/HTTPS 차이를 실제 열람과 대조했다. 검색 단계에서 탈락한 링크와 최종 후보의 분모를 분리했다. | 미확인(검증 없는 생성 결과의 가짜율은 별도 조건의 반복 실험으로 확인) |

**읽는 법과 판정자.** 표의 정답 분절·역할은 작업자 코딩이다. 후보 판정은 작업자와 내부 별도 검토이며, `JUDGMENTS.json`의 각 행에 판정자를 적었다. 사람 또는 다른 모델 검토가 아니다. 모든 B 실행은 gold를 주지 않은 새 문맥의 내부 모델이 카탈로그를 번역한 조건이다. 실제 개발자의 번역 성능으로 부르지 않는다.

`동일`은 날짜와 별개로 특정 대상 또는 핵심 설계 선택을 회수한 서로 다른 정답 항목 수, `이전`은 그중 결정일 이전 근거가 확인된 항목 수다. `놓친`은 동일성 기준이며 공통·A만·B만으로 나눈다. G번호는 해당 사례의 gold ID 끝부분으로 `CASES.json`에 전체 이름·원문 위치가 있다. `정답원 밖 유용 후보`의 분모는 비정답 후보 행, `근접 오답`·`깨진·가짜 링크`의 분모는 제출 후보 행이다. 여러 후보가 한 정답을 가리켜도 한 번만 센다. 유용성은 문서로 뒷받침되는 제한된 참고 용도이며 실제 채택·실행 성공을 뜻하지 않는다.

노출기록은 원문·snippet·일반 기억 인식 등 실행자가 보존한 사건 수다. 모든 사건을 확정적인 정답 누설이라고 단정하지 않는다. 사후 후보와 날짜 미확인을 별도로 두며, 날짜 미확인을 역사적 실패 또는 사후 자료로 바꾸지 않는다. 표의 날짜는 사례마다 수락·병합·거절·초안 교체 중 해당 결정 사건이며 구현 출시일과 다를 수 있다. 관측 창은 2026-11-20 UTC의 원 실행 로그, 사례당 상위 최대 15개 후보이며 실제 개수는 §2에 제시한다.

## §2 세부 질문별 답

이번 관측에서 기존 도구는 목적에 인접한 실제 구현·API·설계 패턴을 다수 찾았지만, 문서에 기록된 모든 구체 대안을 재현하지는 못했다. A의 일치 항목은 **22/176**, 결정일 이전 자료로 뒷받침된 항목은 **16/176**이다. B는 각각 **8/176**, **2/176**이다. 이것은 문서 항목 회수율이며 검색의 전체 recall, 설계 성공률 또는 제품 우위의 점수가 아니다. [집계](evidence/AGGREGATES.json)의 실체 항목 34개와 내부 구조 항목 142개를 나누면 이 차이가 특히 중요해진다.

### Q1. 어떤 계열이 문제 문맥과 비교 대상을 분리하는가?

네 계열 모두 정답원으로 구성할 수 있었다. 다만 템플릿의 절 제목과 실제 작성 관행, 그 절이 도입된 시점은 다르다. [계열별 템플릿·원 이력](TEMPLATES.md)에는 실제 열었던 SHA와 Git 작성/통합 날짜를 남겼다.

| 계열 | 입력으로 사용한 문제 부분 | 비교 항목을 추출한 부분 | 직접 확인한 도입 시점 |
| --- | --- | --- | --- |
| Rust RFC | Summary의 목적·Motivation | Alternatives, 결합 Drawbacks/alternatives | Alternatives는 2014-03-10 최초 템플릿에 존재. Rationale and Alternatives는 2017-07-19. Prior art 작성판 2018-02-12, 통합판 2018-02-27. |
| Python PEP | 초기 Abstract/Introduction/Motivation 및 문제만 분리 가능한 Rationale·Goals | 명시 비교가 있는 Rationale, Alternatives, Rejected Ideas, Open Issues | PEP1의 다른 언어·대안 설명 지침은 2000-07-25. PEP12의 실제 Rejected Ideas 등 절 골격 추가는 2019-03-08. |
| Swift Evolution | Introduction·Motivation의 기존 어려움 | Alternatives considered | 2015-11-03 저장소 root 판부터 분리. 저장소 작성일을 최초 인터넷 공개일로 확대하지 않음. |
| Kubernetes KEP | Summary/Background/Motivation/Goals/Non-Goals의 목적·제약 | Alternatives 및 구 design-proposals의 대응 비교 절 | 최초 제안의 작성 2017-08-31/통합 2017-09-26에 Alternatives 존재. Goals/Non-Goals 분리 통합 2017-11-14. 2020년 현 경로 생성은 첫 도입이 아님. |

제목만 잘라서는 충분하지 않다. 오래된 PEP의 Rationale은 문제와 해법을 섞고, 현재판의 Motivation도 리뷰 뒤 수정될 수 있다. 각 접두부는 복구한 수락 전 판의 문제 부분을 요약하고 번호·제목·저자·정답 링크·최종 해법을 제거했다. 이 변환 자체는 작업자의 판단이다. [PEP 지침](https://peps.python.org/pep-0001/), [실제 변경을 논의한 리뷰 기록](TEMPLATES.md#정답원으로서-확인한-한계), [특허 최종 명세서의 사후 입력 문제 M06](https://ceur-ws.org/Vol-1175/CLEF2009wn-CLEFIP-LopezEt2009.pdf)이 서로 다른 종류의 근거다.

이 분리 원칙으로 만든 접두부 **31개**를 A/B에서 각각 **31회** 실행하고, 비교 절의 **176항목**과 별도로 대조했다. 예를 들어 C24의 접두부에는 초기화 할당의 반복, 불변성, 공개 입력과 숨겨진 상태의 경계만 남기고 구체 비교 대안 7개는 주지 않았다. 이렇게 문제 문맥과 비교 절을 분리해 실행할 수 있음은 확인했지만, 작업자의 요약이 원 설계자의 정보 상태를 완전히 재현한다고 보지는 않는다. [C24 접두부](cases/prefix/C24.md), [A 원 응답](runs/A/C24.json), [B 원 응답](runs/B/C24.json), [집계](evidence/AGGREGATES.json).

빈 절도 있었다. 고정 판 K265의 Alternatives는 None이고 K177은 채워지지 않은 지침이며 Rust90에는 비교 절이 없었다. 검색 결과에서 None으로 보인 Rust438·1300은 실제로는 Unresolved questions에 붙은 문구여서 빈 대안 절 반례로 쓰지 않았다. 템플릿 존재가 충분한 정답을 보장한다는 가정을 본문으로 재검사한 결과다. [반례와 원 주소](COUNTEREXAMPLES.md), [원 질의·실패](evidence/counterexamples/SEARCH_LOG.json).

### Q2. 사례 집합은 어떻게 고정했는가?

사례는 **31개**, 본문 정답은 **176개**, 사례별 최소는 **3개**다. Kubernetes 6개, Python 9개, Rust 8개, Swift 8개로 가장 큰 계열도 9/31이다. 계열별 공식 목록·번호순 정렬·건너뛰기 규칙을 먼저 커밋했다. 시드 1313은 실행 순서를 섞는 데 썼으며 모집단에서 무작위 표집했다는 뜻이 아니다. [SAMPLING](SAMPLING.md), [사례별 판·결정 증거](cases/CASES.json), [기계적 구성 점검](evidence/CORPUS_CHECK.json).

| 계열 | 사례 수 | 정답 분모 | A 동일/결정 전 | B 동일/결정 전 |
|---|---:|---:|---:|---:|
| Kubernetes KEP | 6 | 34 | 2/34 · 1/34 | 1/34 · 0/34 |
| Python PEP | 9 | 73 | 8/73 · 7/73 | 2/73 · 1/73 |
| Rust RFC | 8 | 39 | 6/39 · 6/39 | 4/39 · 1/39 |
| Swift Evolution | 8 | 30 | 6/30 · 2/30 | 1/30 · 0/30 |

채택 후 대체·철회 또는 명시적 부분 번복은 **6개**다: C07의 인수 없는 zip 동작, C12의 dict version 사양 철회, C14의 annotation 평가 방식, C21의 capture/receiver 기본·추론, C29의 같은 파일 extension 접근, C31의 version 규칙 대체. 부분 번복을 제안 전체 폐기로 부르지 않았다. C10·C11·C13은 기각/초안 뒤 새 제안으로 바뀐 추가 3개이며, 앞의 6개에 포함하지 않았다. [후속 문서와 이유의 대조](REVERSALS.md).

접두부 최초 커밋은 `8cb2b8e58f7d4278c11073956b31b30ad43aff18`, C14 결정일 정정은 `c9936188a885848a16b55b4e11ac965bd2d0b204`, C31 추가 접두부는 `ba1cc08705e4a1c56fcdb1a8062193ca4748992e`다. 모두 gold 커밋 `f6f59a85949a001792b80260dd454c3fcc714a70`의 선조이고, 해당 커밋의 내용 hash와 실행 파일을 대조한다. [접두부 원장](cases/PREFIX_MANIFEST.json), [최종 검증](evidence/FINAL_VALIDATION.json).

C31은 PEP386의 두 비교기를 한 항목으로 합친 선정 오류를 복구한 추가 사례다. 일부 A 실행이 이미 시작된 뒤였으나 gold 공개 전에 추가 접두부를 먼저 커밋했고 기존 30개를 버리거나 교체하지 않았다. 원래 30개만 남긴 민감도는 A 동일 **20/171**, 이전 **14/171**, B 동일 **8/171**, 이전 **2/171**다. 이 보정을 완벽하게 한 번에 끝난 사전 등록으로 포장하지 않는다. [선정 보정 기록](SAMPLING.md), [민감도](evidence/AGGREGATES.json).

### Q3. 정답 항목은 무엇으로 구성되었는가?

고정한 기능 역할 규칙을 적용하고 C05-G06의 코딩 오류를 정정한 분류는 완성품 0, 재사용 부품 17, 같은 분야의 다른 설계 146, 다른 언어·생태계 12, 다른 분야 원리 1, 표준·논문 0이다. 최초 gold의 값과 경계 문구는 해당 항목의 role_at_initial_gold_commit·boundary_note_at_initial_gold_commit에 보존했다. 정답176개를 추가하거나 삭제하지 않았다. 마지막 범주가 0이라고 논문·표준을 전혀 읽지 않았다는 뜻은 아니다. 인용 형식보다 문서가 가져오는 기능을 우선했다. `role`, `match_kind`, `stance`, `reason`, `added_in_review`, `boundary_note`와 원문 절을 항목마다 보존했다. [CASES](cases/CASES.json), [동결 규칙](SCOPE.md#5-정답-역할항목일치-규칙).

역할과 일치 단위도 다르다. 외부 실체는 **34개**, 내부 구조 선택은 **142개**다. 예컨대 기존 regex library를 바인딩하는 C17-G02는 역할상 부품이지만 특정 제품 이름이 아닌 구성 전략이다. Swift의 버전 숫자를 문자열로 쓰기/비교 연산자를 생략하기/쉼표 인수로 쓰기는 세 내부 선택이다. 아무 version-compatible 도구를 찾았다고 이 세 항목을 찾았다고 세지 않는다. 단순 언어·프로젝트 이름이 같아도 필요한 subsystem이나 선택 구조가 다르면 불일치다.

본문 밖 리뷰 항목은 C22·C28에서 7개를 별도로 추출했다. DRF는 기존 DataRaceFree의 별명이므로 신규 분모는 6개이고 확대 pool은 182개다. C22의 Sync·Tasksafe·Clojure Atom 명칭 비유, C28의 암묵 Selector 변환과 `.selector` 멤버를 확인했다. C27의 lens·partial application처럼 리뷰에서 들어와 이미 본문에 포함된 항목은 본문 정답에 한 번만 센다. 이는 리뷰 추가 여부의 확인 사례이며 모든 항목의 편집 이력이 복원되었다는 뜻은 아니다. [Rust PR123](https://github.com/rust-lang/rfcs/pull/123), [Swift 수락 토론](https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1), [원장](cases/CASES.json).

### Q4. 다른 분야의 원리·구조·용어는 얼마나 인용되는가?

**다른 분야의 원리·구조로 판정한 항목은 정정 후 1/176(0.57%)**이다. KEP **1/34(2.94%)**, Python **0/73**, Rust **0/39**, Swift **0/30**이다. 해당 한 항목에 대한 A/B 회수는 모두 **0/1**이다. 외부 언어학 문헌의 명시적 인용을 발견한 것과는 구별해야 한다. 이는 문서가 다른 분야의 관계를 schema에 사용한 사례이며 독립 이론 논문을 인용한 사례는 아니다. 다른 언어·생태계의 12항목은 그 범주로 남겼고, 표본 밖에서 찾은 자료는 분모에 보태지 않았다. [역할별 표2](RESULT.md#표-2--역할별-집계), [정정 원장](evidence/ROLE_CORRECTIONS.json).

C05-G06은 자연어 능동태의 active component와 직접·간접 목적어 관계를 이벤트 필드에 대응시키는 **구조 차용**이다. 자동 소비자가 각 필드의 대상을 해석하게 하려는 조건을 붙였으나, 당시 소비자를 사람으로 삼는다는 이유로 기각했다. 실제 기계 이해 효과나 언어학 이론의 출처를 입증하지는 않는다. 원문은 단순 장식보다 구체적이다. [고정 KEP 원문](https://raw.githubusercontent.com/kubernetes/community/c5b815bf44dd6f623ef2b4cf80cf5194bcfa38d5/contributors/design-proposals/events-redesign.md), [root 재확인](evidence/judgments/VERIFICATION.json), [기존 후보 판정을 보지 않은 내부 별도 검토](evidence/judgments/SECOND_REVIEW.json).

**왜 최초0을 바꿨는가.** 초기 gold는 외부 학문 인용이 없다는 이유까지 들어 이를 같은 분야 경계로 코딩했다. 그러나 사전 SCOPE §5는 외부 인용을 필요조건으로 두지 않았고, 서로 다른 분야의 관계를 명시적으로 옮긴 경우를 허용한다. 내부 별도 검토의 원문 대조를 받아들여 규칙을 바꾸지 않고 역할만 정정했다. 최초 동결 분류는 **0/176**, 그때의 먼 분야 회수율은 **0/0으로 정의 불가**였음을 기록한다. 같은 dict 자료구조의 profiling에서 최적화 guard로 옮긴 C12-PySizer까지 먼 영역으로 넓히면 **2/176(1.14%)**, 회수는 모두 **0/2**다. 이 세 값은 최초 코딩·정정·넓은 경계 민감도이며 역할 신뢰도 연구나 모집단 추정이 아니다. [정정 전후와 시점](evidence/ROLE_CORRECTIONS.json), [고정 규칙](SCOPE.md).

P433의 sterile 비유와 C22 리뷰의 Clojure Atom은 용어를 가져오며 그 분야의 작동 원리를 채택한 증거가 아니다. 반면 표본 밖 [CoDel RFC8289](https://www.rfc-editor.org/rfc/rfc8289.html)는 제어 이론을 작동 구조에 사용하고, 고전적 PID와 네트워크 조건의 차이도 설명한다. 따라서 타 분야 인용의 형태는 최소한 **용어만 빌림 / 실제 관계·구조를 비교함 / 작동 메커니즘을 구성함**으로 읽어야 한다. [반례 비교](COUNTEREXAMPLES.md), [인용 선택 편향의 다른 분야 근거 M12](https://link.springer.com/article/10.1007/s00799-020-00288-2).

### Q5. 기준선 A는 실제로 무엇을 찾았는가?

31개 접두부 각각을 새 문맥의 내부 하위 에이전트가 읽었다. 모델 표기는 **GPT-6 Astra Pro**, 입력은 실행 규칙과 해당 접두부뿐이었다. 사례별 후보는 **4–9개**, 총 **204개**, 검색 질의는 **6–12회**, 열람 예산 계수는 **12–20**으로 저장했다. 원 응답·문자열·UTC·실패·노출·날짜는 [runs/A](runs/A/)에 있다. 전용 공개 코드 검색은 전 사례에서 시도했으며 HTTP200 응답을 명시한 실행은 **14/31**이다. 나머지 17개는 접근 실패와 웹에 색인된 공개 코드의 fallback을 기록한다. HTTP200 자체가 모든 후보의 코드 근거를 보증하지는 않는다. [실행 감사](evidence/RUN_AUDIT.json).

A는 정답 동일 항목 **22/176**, 결정 이전 근거 **16/176**을 회수했다. 외부 실체는 동일 **12/34**, 이전 **9/34**이고 내부 구조는 동일 **10/142**, 이전 **7/142**이다. 알려진 외부 대상과 문서 내부 선택의 회수 차이는 이 표본에서 분명하지만, 둘의 문제 난도나 검색 가능성이 통제된 실험은 아니다.

구체적으로 C20은 L20n과 gettext+formatting을 회수했다. C17에서는 RE2·PCRE를 바인딩하는 전략을 찾았지만 그 이름만으로 특정 backtracking 기능 조합까지 추가 적중시키지 않았다. C26에서는 GHC의 최소 버전 predicate를 찾았으나 원 응답이 선택한 용도가 버전 조건부 포함이었으므로, 본문에 존재하는 쉼표 인수 표기를 gold로 자동 채점하지 않았다. C23에서는 C의 pointer/integer 변환과 mask/merge 참고를 찾았어도 Swift 제안의 내부 대안은 별개였다. [해당 원 응답](runs/A/), [행별 일치 사유](JUDGMENTS.json).

### Q6. 카탈로그 기준선 B는 무엇을 더하거나 놓쳤는가?

B도 **31개**를 각각 별도의 새 문맥으로 실행했다. 후보는 사례당 **1–9개**, 총 **138개**, 질의 **2–17회**, 보수적 page 계수 **13–25**였다. awesome 목록과 허용한 패턴 카탈로그를 열어 후보를 발견한 뒤 연결된 원문을 검증했다. A 결과나 gold를 주지 않았으며 번역자는 사람 개발자가 아니라 내부 모델이다. [실행 규칙](BASELINE_RULES.md), [B 원 응답과 발견 경로](runs/B/), [감사](evidence/RUN_AUDIT.json).

B의 동일 항목은 **8/176**, 결정 이전 근거는 **2/176**이다. 외부 실체 동일 **2/34**, 내부 구조 동일 **6/142**로 나뉜다. C25에서 Cargo·XCTest·TAP·여러 Swift test library를 찾았지만 FooTests 배치, package manager와의 완전 분리, 기본 XCTest를 빼고 protocol만 제공하는 세 선택은 회수하지 못했다. C19에서 Racket pattern expander와 GHC pattern synonym을 찾았지만 전체 arm의 왼쪽/전체 arm/전체 match를 감싸는 macro라는 세 구별 대안과 같게 세지 않았다.

카탈로그 경로가 있어도 자료의 날짜·범위는 따로 확인해야 했다. C24에서는 attrs 패키지의 2015년 존재와 이 후보가 필요로 하는 frozen·post-init 등의 2016년 후반 기능을 구별했다. C27은 Elixir의 짧은 name/arity capture 하나를 확인했지만 같은 arity·다른 label이라는 핵심 조건을 충족하지 못했다. C10은 카탈로그 이전에 외부 페이지를 연 절차 이탈을 원 기록에 남기고 그 페이지와 항목을 제외했다. 이런 노출이 있었다는 사실까지 삭제한 ‘오염이 전혀 없는 B’로 부르지 않는다. [개별 B 로그](runs/B/), [후보 판정](JUDGMENTS.json).

A+B의 사후 pool 합집합은 동일 **24/176**, 이전 **16/176**이며 B만 더한 동일 항목은 **2개**다. 서로의 결과를 본 뒤 통합 검색을 실행한 것이 아니므로 이 합집합은 AF-RES-009의 전체 조합을 실제 운용한 성능이 아니다.

### Q7. 일치, 유용성, 근접 오답, 링크는 어떻게 분리했는가?

AF-RES-004의 L/E/H/T 값과 네 라벨을 그대로 적용했다. L은 대상 원문 접근, E는 제안한 이유의 지지, H는 접두부 제약별 통과/위반/미확인/원래 범위 밖, T는 전이 대응의 구체성이다. 합산 점수를 만들지 않았다. 거절된 대안을 정확히 찾는 일과 그 대안이 제약에 맞는 일은 다르다. [고정 PROTOCOL](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md), [JUDGMENTS](JUDGMENTS.json).

| 고정 라벨 | A 후보 수/204 | B 후보 수/138 |
|---|---:|---:|
| DIRECT_DOCUMENTED | 8 | 0 |
| CONDITIONAL_TRANSFER | 158 | 117 |
| SURFACE_OR_CONSTRAINT_MISMATCH | 9 | 3 |
| INSUFFICIENT | 29 | 18 |

정답원 밖 유용 후보는 A **146/178행**, B **105/126행**이다. 그중 결정 이전 자료가 확인된 것은 A **79**, B **32행**이다. 원래 답변이 좁힌 참고 부분 때문에 H에 not_in_scope가 있는 유용 후보는 A **50**, B **28행**, 모든 H가 그 제안 범위에서 pass인 후보는 A **96**, B **77행**이다. 이 숫자는 서로 다른 성공 구현의 개수가 아니며 같은 기술이 여러 사례에서 반복될 수 있다. 실제 설계자가 더 좋다고 확인한 후보는 **0건**이다.

경계18행의 첫 검토에 이어7행을 기존 판정표 없이 다시 읽었다. 두 번째 검토에서는 C05의 현재 dedup 유지 조건과 C09의 builtin range 실체를 원 응답에 소급하지 않아 해당 적중을 제거했고, C24의 비공개 속성 공개 builder 입력은 원 후보가 직접 경고한 구조이므로 거절 대안의 회수로 인정했다. 단순히 채택을 권하지 않았다는 이유로 회수에서 뺄 수는 없다. [최초 판정과 정정](evidence/judgments/SECOND_RESOLUTION.json).

B-C20의 Jed는 GNU gettext와 같은 프로젝트가 아니다. 다만 원 응답이 gettext 방식의 context/plural lookup 다음 보간을 명시하여 SCOPE의 **동일 명시 메커니즘** 경로로 G02와 일치한다. 따라서 외부 항목34개에 대한 집계는 모두 같은 프로젝트의 이름을 찾은 횟수라고 읽으면 안 된다. 이 한 unknown-date 행을 프로젝트 동일성만의 기준으로 제외하면 B는 **7/176**, 결정 전 적중은 **2/176**으로 남는다. [분리된 match_basis](JUDGMENTS.json), [이견의 범위](evidence/judgments/SECOND_REVIEW.json).

예를 들어 C12의 RPython guard/fallback은 변경을 감지하는 detector를 확인하지 못하면 유효성 조건을 통과하지 못한다. C02의 gVisor를 UID/GID 매핑 대신 쓰는 제안은 요구된 identity mapping을 제공하지 않는다. C27의 arity 기반 함수 참조도 label-only overload를 구별하지 못한다. 반대로 C23의 bit/pointer 원문처럼 gold 밖에서도 특정 참고 용도는 문서로 지지될 수 있다. 이들을 골드 적중, INSUFFICIENT, 제약 위반, 조건부 참고로 따로 보존했다.

가짜·다른 대상 링크는 최종 검증된 후보 중 A **0/204**, B **0/138**였다. 403·timeout·도구 차단을 가짜로 세지 않았고, 실패한 후보가 제출 전에 제외되었다는 선택 조건도 중요하다. fragment·redirect 차이는 원 로그 및 별도 원문 확인으로 해소했다. 링크가 열린다는 이유만으로 H 또는 인용의 인과적 의존성이 입증되지는 않는다. [URL 보완](evidence/judgments/AUDIT_RESOLUTIONS.json), [CiteEval M13](https://aclanthology.org/2025.acl-long.1574.pdf), [correctness/faithfulness 구별 M14](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/wallat-2025-correctness.pdf).

### Q8. AF-RES-009의 반대 가설 A/B에는 어떤 의미인가?

**009의 공식 기각 조건을 이번 수치만으로 충족했다고 판정할 수 없다.** 그 조건은 사전 고정한 실제 과제·허용 오류·검토 시간에서 기존 조합 또는 목록+개발자 번역이 **새 절차 이상인지** 비교하는 것이다. 이번 연구에는 새 절차 arm, 사람 번역 arm, 실제 설계자의 검토 비용·수정 효과가 없다. 009의 유지 관련 H2도 시험하지 않았다. [GAP §2·§3·§5](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md), [실제 실행 집계](evidence/AGGREGATES.json), [평가 점수와 사용자 효용 M03](https://informationr.net/ir/18-2/paper582.html).

실행 사례 C24에서 B는 Immutables의 비공개 속성·공개 builder 입력 경고를 통해 거절 대안 **1/7**을 회수했다. 선택된 기능의 결정 전 판은 확인되지 않아 역사 적중은 **0/7**이다. 이는 카탈로그 경로가 구체적인 실패 조건을 비교에 가져올 수 있다는 관측이지만, 해당 대안을 채택해야 한다거나 새 절차보다 성과가 좋다는 증거는 아니다. [B-C24 원 응답](runs/B/C24.json), [일치와 날짜 판정](evidence/judgments/B-C24.notes.json), [집계](evidence/AGGREGATES.json).

| 사례 유형 | 이번 관측이 지지하는 범위 | 이번 관측으로 반박하거나 입증하지 못하는 것 |
| --- | --- | --- |
| 알려진 외부 실체·명시 메커니즘 | A/B가 일부 실제 참고를 회수하며 gold 밖에서도 제한된 참고 용도를 제시함 | 모든 필요한 부품을 찾음, 기존 조합이 새 절차보다 느리거나 나쁨 |
| 내부 문법·명명·API 경계 선택 | 목적 수준 검색만으로 기록된 세부 선택을 전부 재현하기 어려웠음 | 낮은 회수율이 별도 제품의 추가 가치임. 기존 검색 후 설계자가 선택을 유도하는 전체 workflow는 비교하지 않음 |
| 먼 분야 원리 | 규칙 적용 정정 후1항목, A/B0/1. 최초0·넓은 경계2와 표본 밖 CoDel을 분리함 | 먼 유추 수요가 없거나, 반대로 미회수 때문에 반드시 제품 수요가 있음 |
| 후속 번복 | 일부 관련 사전 메커니즘을 찾을 수 있었음 | 그 자료가 당시 결정을 바꿨을 것임, 미래 결정을 예측했음 |

따라서 ‘LLM 조합이면 모든 기록 대안을 찾는다’라는 강한 문장은 이 관측과 맞지 않는다. ‘유용한 선행 참고를 제시한다는 넓은 가치는 기존 조합으로 상당 부분 제공된다’는 009의 경계는 정답 밖 후보 때문에 여전히 유효한 대조 가설이다. 두 문장은 같은 주장도, 서로의 논리적 부정도 아니다.

## §3 추가 분석

### 3.1 독립 정답원은 완전한 정답원이 아니다

문서 저자와 리뷰어의 기록은 이번 작업자와 독립적이다. 반면 항목을 나누고 역할·일치를 붙인 작업은 연구자 코딩이다. 리뷰로 확인한 6개 신규 항목은 본문 pool의 실제 누락 하한이지만 2/31사례 밖의 리뷰 전체를 전수 검토한 결론은 아니다. 후보의 조건부 유용성은 또 다른 판정 층이다. 이 둘을 더해 ‘누락 선례가 몇 %’라는 모집단 추정으로 만들지 않았다. [리뷰 pool](cases/CASES.json), [반례](COUNTEREXAMPLES.md).

정답에 없는 더 나은 참고를 찾았는지에 대해서도 강도를 나눈다. 본문 밖에 실제 리뷰 항목이 더 있음은 원문 사실이다. A/B가 gold 밖 유용한 참고를 제시함은 명시된 L/E/H/T 코딩 결과다. 그 참고가 원래 대안보다 실제 결정에 더 낫다는 것은 이 연구에서 관측되지 않았다. 따라서 ‘불완전성은 확인되었지만 우월성의 크기는 미확인’이 정확한 결론이다.

### 3.2 다른 분야의 평가에서 가져올 수 있는 것

| 분야 | 직접 읽은 독립 정답 평가 | 확인한 편향·반례 | 이번 설계 문서 평가에 적용한 조치 |
| --- | --- | --- | --- |
| 특허 | CLEF-IP 개요·참가 분석, NTCIR-4/5 개요·과제 | 심사·허여 목적의 선택적 인용, final claim의 사후 정보, 인용 3개 이상 선정 조건. CLEF-IP에서는 자동 인용 34개 중 13개를 전문가가 비관련으로 본 별도 관측이 있음. | 최초 입력 판을 고정하고 결정 전 자료 여부를 나눔. gold 밖 후보를 판정하되 특허의 법적 relevance 등급을 004 축에 섞지 않음. |
| 법률 | COLIEE 2023 개요 및 공식 task | 판결에서 noticed한 판례가 관측 정답이며 모든 관련 판례의 전수 판정은 아님. 입력의 직접 인용을 가리는 절차가 있음. | 접두부의 직접 항목·번호·링크 제거. 학습 기억 배제와 혼동하지 않음. |
| 학술 | Content-Based Citation Recommendation와 종합 검토 | 실제 인용은 자기 인용·친숙함·인지도·접근성 등의 영향을 받음. 조사한 local 추천 접근 15/17이 실제 인용 재현에 의존. | 기록된 선택 재현과 설계자 효용을 구별. 시기 분할과 과거 근거 확인, 비인용 후보의 별도 판정. |

원문과 비교 범위는 [CROSSFIELD](evidence/methods/CROSSFIELD.md)에 있다. 특히 CLEF-IP의 시스템 순위 비교는 인용 정답/전문가 평가뿐 아니라 주제 집합도 달라져 정답 확장만의 인과 효과라고 할 수 없다. NTCIR-4의 34개 보강 주제는 111개 제출 run 중 30개 run의 풀을 사용했고, 69개 추가 인용 주제 중 2개를 제외해 최종 101개를 평가했다. ‘30팀’으로 잘못 바꾸지 않았다. [M05](https://ceur-ws.org/Vol-1175/CLEF2009wn-CLEFIP-RodaEt2009.pdf), [M07](https://research.nii.ac.jp/ntcir/workshop/OnlineProceedings4/PATENT/NTCIR4-OV-PATENT-FujiiA.pdf), [M09](https://link.springer.com/article/10.1007/s12626-023-00152-0), [M12](https://link.springer.com/article/10.1007/s00799-020-00288-2).

모든 풀 기반 평가가 무효라는 결론도 배제했다. M16은 시험한 조건에서 예상한 일부 편향이 나타나지 않았고, M04는 실제 추가 판정에 근거한 보정의 필요성을 다룬다. 이번 작업은 새로운 점수나 보정을 발명하지 않고, 원 gold 점수와 추가 판정을 분리해 그 한계를 보였다. [M04](https://codalism.com/research/papers/wp09_sigir_pp.pdf), [M16](https://codalism.com/research/papers/wmz10_evia.pdf).

### 3.3 다섯 이해관계자의 질문은 다르다

설계자는 참고가 구현·설명을 얼마나 바꾸는지, 리뷰어는 빠진 대안과 거절 이유가 타당한지를 묻는다. 검색 도구 사용자는 예산 안에 검증 가능한 후보를 얻는지가 중요하다. 정보검색 평가자는 항목 분절·풀 누락·시기·실행 변동을 문제 삼고, 특허 조사자는 특정 날짜 이전의 근거와 여러 문헌의 결합 관계를 따진다. 이번 연구는 검색 실행과 기록 비교까지 관측했으며 이 사람들을 인터뷰하거나 실제 결정의 개선을 관측한 연구는 아니다. [관점별 대응 표](evidence/methods/CROSSFIELD.md#3-다섯-관점에서-달라지는-질문), [실제 리뷰 추가 M27](https://internals.rust-lang.org/t/pre-rfc-trait-for-deserializing-untrusted-input/7519).

### 3.4 시간, 노출, 단회 실행의 민감도

후보 날짜는 A **결정 전 105/사후 23/시점 미확인 76**, B **결정 전 37/사후 34/시점 미확인 67**다. 현재 검색 색인과 현재 카탈로그를 사용했으므로 과거 문서가 확인되어도 그때 같은 검색으로 발견 가능했다고 입증하지 않는다. B의 사람 번역 대체, 전용 코드 검색의 접근 차이, 영어/한국어 접두부, 서로 다른 문서 크기와 find 계수 관행도 A/B의 단순 우열 해석을 제한한다. 한 사례를 한 번 실행했으므로 반복 분산은 추정하지 않았다. [원 실행](runs/), [누설 방법론 M02](https://arxiv.org/pdf/2207.07048), [비결정적 검색 평가 M15](https://codalism.com/research/papers/jwsdc14_sigir.pdf).

어떤 종류든 노출 기록이 있는 실행은 A **13/31**, B **18/31**이다. 모든 기록을 제외한 보수적 부분집합은 A **18사례/93항목**, 동일 **12**, 이전 **8**; B **13사례/60항목**, 동일 **3**, 이전 **1**다. 이 부분집합은 무작위로 나눈 대조군이 아니며, 실제 학습 기억 누설의 발생률을 뜻하지 않는다.

A의 날짜 보완은 4행이며 원 raw date와 판정 date를 모두 남겼다. 원 실행 날짜를 그대로 썼을 때도 이전 적중은 16개이지만 어떤 항목이 그 수에 들어가는지는 다르다. C14의 fragment, C30의 공식 대체 렌더링, B의 redirect는 URL 감사에서 원 로그와 따로 대조했다. [검증 보완](evidence/judgments/VERIFICATION.json), [내부 별도 원문 검토](evidence/judgments/reviewer-a-sources.json), [감사 해소](evidence/judgments/AUDIT_RESOLUTIONS.json).

### 3.5 뒤집힌 결정에서 찾은 것과 못 찾은 것

채택 후 번복 6개와 기각/초안 교체 3개의 후속 이유를 원 A/B 응답과 정성 대조했다. C07의 인수 0개·빈 전치 문제는 단순 zip/shortest-input 예로 회수되었다고 보지 않았다. C12의 mutation-triggered invalidation, C14의 지연 callable, C29의 같은 타입 private 공유처럼 후속 설계와 인접한 사전 메커니즘은 A에서 찾았지만, 미래 구현 변경이나 그 프로젝트의 실제 고통을 예측했다고 할 수 없다. C11의 원자적 close-on-exec는 후속 안전성 논증에 직접 닿는 선례이나 최초 제안이 채택되었다가 뒤집힌 사례가 아니므로 별도 층이다. [9개 비교와 각 B 결과](REVERSALS.md), [구조화 기록](evidence/REVERSAL_JUDGMENTS.json).

이 분석은 후속 문서를 본 작업자가 한 post-hoc 비교다. 새 예측 정확도 지표를 만든 것이 아니고, 원 gold의 분모·결정 시점·일치를 수정하지 않았다.

## §4 가장 중요한 불일치·약점 3건과 다음 조사 제안

### 4.1 선행 사례 검색이라는 질문과 내부 설계 선택이 많은 정답 집합

**무엇이 어긋나거나 약한가:** 176항목 중 142개는 내부 구조 선택이다. Rust 8개가 모두 2014년으로 명시 Prior art 템플릿보다 이르고, ‘3개 이상 대안’ 조건이 비교가 풍부한 문서만 남긴다. 최초 먼 분야0은 문법 구조의 기능을 과도하게 좁힌 코딩 때문에 정정 후1이 되었고, PySizer 경계까지 넓히면2가 된다.

**근거 위치:** §2 Q1–Q4, `cases/CASES.json`의 match_kind·boundary_note, `SAMPLING.md`, `TEMPLATES.md`, `evidence/ROLE_CORRECTIONS.json`, `evidence/judgments/SECOND_REVIEW.json`.

**이것이 틀리면 바뀌는 결론:** 현대의 명시 Prior art 문서에 외부·먼 분야 선례가 더 많다면 현재의 낮은 항목 회수와 1/176은 일반 도구의 실패나 실제 인용 빈도를 대표하지 못한다. 역할 경계가 달라도 이 표본에서 먼 분야가 흔하다는 결론까지 바로 나오지는 않는다.

**다음 조사 제안:** “시기와 절 종류를 나누면 외부·먼 분야 선례의 비율과 회수가 달라지는가?” 필요한 자료는 빈 절까지 포함한 계열별 연속 공식 목록, 최초판·결정판·리뷰다. 최소 **4계열 × 과거/최근 2층 × 10문서 = 80문서**를 먼저 빈도 표본으로 읽고, 그 안의 외부 실체/내부 구조 과제를 구별해 기준선을 반복한다.

### 4.2 본문 밖 참고의 많음과 실제 유용성·우월성 사이의 간격

**무엇이 어긋나거나 약한가:** 본문 밖 리뷰 신규 항목 6개는 독립적인 누락 증거지만, 정답 밖 유용 후보 수는 연구자의 조건부 참고 판정이다. A 50행·B 28행은 좁은 scope 때문에 일부 H가 범위 밖이다. 한 link가 유용한 부분을 제공하는 것과 설계 전체의 필수 조건을 해결하는 것은 다르다. 내부 별도 검토도 같은 세션 모델의 검토이며 사람 효과 검증이 아니다.

**근거 위치:** §1 표3, §2 Q7, `JUDGMENTS.json`, `evidence/judgments/BOUNDARY_REVIEW.json`·`BOUNDARY_RESOLUTION.json`·`SECOND_RESOLUTION.json`, `COUNTEREXAMPLES.md`의 두 번째 반례.

**이것이 틀리면 바뀌는 결론:** 부분 참고가 실제 검토에서 거의 쓰이지 않으면 ‘기존 조합이 넓은 가치를 이미 제공한다’는 지지는 약해진다. 반대로 기록되지 않은 참고가 결정을 실제 개선하면 본문 recall만으로 새 방법을 비교하는 평가는 과소평가가 된다.

**다음 조사 제안:** “본문 밖 후보가 실제 설계자의 판단·수정에 쓰이는가, 아니면 설명상 관련성에 그치는가?” 원문·대안 절을 가린 후보와 실제 작업 중인 목적 문맥, 선택·기각 이유 및 수정 이력이 필요하다. 최소 **20사례의 비정답 후보 100개와 해당 문제를 평가할 목표 설계자 5명**으로 문서상 참고, 실제 채택, 비교 우월성을 따로 기록한다.

### 4.3 현재 웹의 단회 제한 실행과 009의 충분성 기각 조건 사이의 간격

**무엇이 어긋나거나 약한가:** 현재 색인·카탈로그·한 모델·단회 검색을 썼고 전용 코드 검색은 17/31에서 접근 제한이 있었다. 새 문맥은 학습 기억을 제거하지 않는다. A+B 사후 합집합은 통합 운영 실험이 아니며 사람 번역·새 절차·검토 시간 대조가 없다.

**근거 위치:** §2 Q5·Q6·Q8, §3.4, `evidence/RUN_AUDIT.json`, `runs/*/*.json`의 queries/exposures/date_status, 고정 009 GAP §3.

**이것이 틀리면 바뀌는 결론:** 검색 표면·반복·사람의 후처리에서 회수가 크게 좋아지면 낮은 수치를 제품의 미충족 수요로 읽을 근거가 더 약해진다. 반대로 같은 비용에서 새 절차의 검증된 이득이 나오면 그때 009의 추가 가치 가설을 실제로 비교할 수 있다.

**다음 조사 제안:** “같은 실제 과제·허용 오류·검토 시간을 고정했을 때 기존 전체 조합과 카탈로그+개발자 번역이 새 절차 이상인가?” 필요한 자료는 네이티브 코드 검색이 가능한 공개 환경, 버전 고정 문맥, 검토 시간·수정 결과, 사전 고정한 새 절차다. 최소 **새 실제 과제 12개 × 3조건 × 3회 = 108회**를 같은 예산으로 실행하고, 사용자가 검토한 시간과 결정 변화도 별도 수집한다. 기존 31개는 방법 점검용으로만 사용한다.

## §5 한계

- 대상은 번호순·조건부·의도적 대체 사례가 포함된 31개다. 확률 표본이 아니므로 모집단 신뢰구간이나 실제 설계자의 전체 인용 비율을 산출하지 않는다. 제품·표준 역할의 분모 0도 그 역할의 성능 부재를 뜻하지 않는다.
- 사이트당 최대 3개는 사전 SAMPLING에 명시한 대로 **비사례 최소수**에 적용했다. 비사례는 **26개/14사이트**, 단일 사이트 최대 3개다. 사례 31개는 독립 제안서 수로 별도 센다. GitHub 호스팅 사례 자체에도 사이트 상한을 적용하는 문자적 해석에서는 30개 최소수를 충족했다고 할 수 없으며, 그 해석 차이를 숨기지 않는다. [원장과 집계](evidence/SOURCE_COUNT.json).
- 본문 원문 31개 외 비사례 최소수에는 템플릿/절차 4, 방법론 6, 특허·법률·학술 3분야 개요, 009에 없던 생성형 인용 평가 2, 리뷰 원문 5가 포함된다. 수락 공고 M25는 리뷰 5개와 별도다. 모든 실패·snippet·본문 미확인은 excluded로 보존하며 최소수에 넣지 않는다. 개별 지원 열람 수를 독립 자료 수로 부풀리지 않는다.
- 모델의 학습 기억, 동일 모델의 코드화·검토, 접두부 요약 손실, query 언어, 검색서비스의 시점 변동을 제거하지 못한다. 파일 접근 범위는 지시 기반이며 물리적 격리라고 주장하지 않는다.
- 각 사례의 결정 날짜는 명시된 사건에 한정된다. Rust5개는 역사적 merge object 접근 실패 때문에 수락 전 PR head와 공식 merge 시각을 분리했다. Swift25의 실제 결정과 저장소 상태 반영, KEP의 이관 전 결정, PEP의 회고 연도 불일치도 원장에 남겼다.
- date_unknown은 아이디어가 당시 없었다는 뜻이 아니다. 반대로 현재판의 오래된 프로젝트 이름만으로 선택된 기능까지 소급하지 않는다. 역사 적중은 검증된 날짜 하위집합이지 당시 웹을 재현한 성공률이 아니다.
- gold에 없는 후보를 원 gold에 소급 추가하지 않았다. C05-G06 역할 오류는 동일한 규칙으로 정정하고 최초 값·근거·시점을 보존했다. 정답176개 분모와 항목 동일성은 그대로이며 PySizer 등의 추가 경계는 민감도로만 표시했다. 역할 분류의 신뢰도 자체는 이번 범위 밖이다.
- 검색 실행은 실제 D3-run, 페이지/API는 D3-fetch, 고정 코드 읽기는 해당 경우 D2, 문헌은 D1로 구별한다. 후보 소프트웨어를 대상 시스템에 통합·실행한 결과나 설계자의 실제 채택 효과 D4는 없다. 원 논문들의 실험도 재실행하지 않았다.
- 본 작업은 저장·색인·제품 코드·DB/API/검색 스택을 구현하거나 확정하지 않았다. 배포·유료 API·로그인·권한 변경·예약 수집은 수행하지 않았다. 출력과 검증은 owned_path 안에만 남긴다.
