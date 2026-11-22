# Arrow Q01–Q04 후속 결정·당대판 대조

후속 원문 판독과 기록을 완료했다. 실제 소프트웨어 실행은 하지 않았다. 이 단계의 새 자료는 2026-11-22 05:50:22 UTC에 원격 확인된 주 판정 커밋 `d1f506b1dde91e706360846f4c2eac5baabe492e` 뒤에 열었다. 최초 질의·반환·가린 판정은 변경하지 않았다.

## 결과와 범위

`decisions.jsonl`은 4개 원질문, `candidate-history.jsonl`은 그 질문들에서 실제 반환한 고유 후보 19개를 모두 포함한다. 당대의 **전체 필수 조건**을 확인한 후보는 0개, 특정 반환 구현·기능이 후대인 후보는 10개, 부분 기능은 존재했으나 전체 조건 또는 정확한 도입판을 확인하지 못한 후보는 9개다. `not_available`은 명시한 공개 구현·기능 계보에 한정하며 이전의 모든 비공개 아이디어가 없었다는 주장이 아니다. `unknown`도 기능의 부재나 당사자의 미인지를 뜻하지 않는다.

Q01의 `binary_type`와 `list_type`은 2025년 21.0.0 기능이고, Java 큰 버퍼는 2020년 1.0.0 계열에서 이미 일부 지원했다. Q02 작성자는 후속 메일에서 DataFusion `ScalarValue`를 수용했다. DataFusion 이름은 원 검색 Q02-R query3/rank4의 Arrow Array 재수출 결과에 있었지만, `ScalarValue` 동작·근거는 반환되지 않았다. Q03은 일반 재귀 변환기보다 좁은 로컬 테스트 보조 함수로 통합됐으며 Date64 기대 시점 단위도 달라졌다. Q04는 구조의 가능성과 별개로 Parquet 검증 공백 때문에 이행을 보류하고 별도 Arrow2 개발로 전환했다. 자세한 관측은 [FINDINGS.md](FINDINGS.md), 각 사실의 원 URL·정확한 위치는 [EVIDENCE_MAP.md](EVIDENCE_MAP.md)와 [sources.json](sources.json)에 있다.

- `sources.json`: 원문별 위치·확인·한계·계보·산입 여부. 과거판 재열람과 API 메타데이터는 신규 원문 수에서 보수적으로 제외한다. 독립 원질문 사건은 여전히 4개다.
- `receipts/`, `requests-*.json`: 실제 GET·검색 요청, UTC, 응답 해시, 실패, 요청별 벽시간.
- `mail-thread-index.json`: 공식 월별 mbox의 2021-01~04 대상 제목 계열 19개 메시지 메타데이터. 전체 읽기와 메타데이터 열거를 구분한다.
- `cost-summary.json`: 후속 비용만 집계한다. 93개 GET 중 90개 성공·3개 실패, 별도 system1 웹 검색 4회. GET 중 GitHub issue 검색 3개도 별도로 표시했다. 병렬 요청 시간 합은 실제 경과 시간이나 인시가 아니다. 토큰·인시는 미제공이다.
- `source-map.json`: 요청 ID와 AR-F/AR-H 자료 ID 대응.
- `build_followups.py`: 관측한 사실·판정을 재직렬화하고 분모를 계산한다. 소프트웨어 기능을 시험하는 스크립트가 아니다.
- `verification-inputs/`: 아래의 **아직 실행하지 않은** 재개 입력.

`cache/`에는 재다운로드할 수 있는 원문·메일·PDF가 있지만 커밋하지 않는다. 영수증과 고정 URL/Message-ID를 남기며 공개 메일 아카이브라는 사실만으로 전문 재배포 허가를 가정하지 않는다. 새 원문을 내려받을 때는 기존 관측 영수증을 덮어쓰지 말고 별도 재현 디렉터리에서 다음 함수를 호출한다.

```sh
python docs/workstreams/research/AF-RES-025/followups/arrow/fetch.py docs/workstreams/research/AF-RES-025/followups/arrow/requests-01.json
```

위 명령은 원 파일을 덮어쓸 수 있으므로 먼저 이 followup 디렉터리 자체를 재현용 작업 위치에 복사한 다음 실행한다. 응답 해시가 달라질 수 있는 API 목록·현행 문서는 `version`과 고정 commit/blob을 함께 확인한다.

## 미실시 검증 1: PyArrow 21 옵션과 저장 schema 우선순위

아래 명령은 작은 입력 3행의 실제 기능 검증이다. 태그는 `apache-arrow-21.0.0`, 배포 패키지는 `pyarrow==21.0.0`이다. 입력은 Binary `[b'ab', null, b'xyz']`와 List<int32> `[[1,null,2],null,[]]`이며, 저장 Arrow schema 유무를 바꿔 두 파일을 쓴다. 옵션이 LargeBinary/LargeList를 선택하고 값·null을 유지하는지, 저장 schema가 있으면 원래 작은 형이 우선하는지 확인한다. 2GiB 초과, Java, 전체 Dataset 기능은 검증하지 않는다. 구현 근거: PR46532·46678 및 21.0.0 core.py의 `binary_type`/`list_type` 절([EVIDENCE_MAP.md](EVIDENCE_MAP.md)).

```sh
python3 -m venv /tmp/af-res025-pyarrow21
/tmp/af-res025-pyarrow21/bin/pip install pyarrow==21.0.0
/tmp/af-res025-pyarrow21/bin/python docs/workstreams/research/AF-RES-025/followups/arrow/verification-inputs/q01_pyarrow21_probe.py --output-dir /tmp/af-res025-q01-fixtures
```

예상 출력은 `no_stored_schema`에서 large_binary/large_list, `stored_schema`에서 binary/list다. `large-types.arrow-stream`도 내보내지만 이는 IPC 입력이며 C Data 포인터 공유 검증과 다르다. 실제 실행 전에는 이 예상치를 관측 결과로 취급하지 않는다.

## 미실시 검증 2: Java C Data 큰 형 import의 공식 테스트

실제 읽은 현재 파일은 `arrow-java`의 `RoundtripTest.java`, Git blob `4d2acbb091af4e563e2a08fc2ae319a57f797f14`다. 확인된 저장소 snapshot은 `7a581880a85358315d05da08296cf570b3643924`(20.1.0-SNAPSHOT, 2026-11-21)다. `vectorRoundtrip` L149–171은 `Data.exportVector` → `Data.importVector`와 allocator 이전을 시험한다. `testLargeVarBinaryVector` L639–661은 문자열과 null, `testLargeListVector` L699–708은 `[1,2]`, `[3,4]`, `[]`를 사용한다. 이는 현재 **Java → C Data 구조 → Java** 경계의 공급자 테스트이며, Python 프로세스에서 Java 프로세스로 포인터를 전달하는 시험이 아니다. 서로 다른 프로세스에 주소 숫자만 넘기면 유효한 공유 메모리 검증이 되지 않는다.

정확한 소스 재독과 고정판 확인 명령:

```sh
git clone --filter=blob:none https://github.com/apache/arrow-java.git /tmp/af-res025-arrow-java
git -C /tmp/af-res025-arrow-java checkout --detach 7a581880a85358315d05da08296cf570b3643924
git -C /tmp/af-res025-arrow-java rev-parse HEAD:c/src/test/java/org/apache/arrow/c/RoundtripTest.java
rg -n 'vectorRoundtrip|testLargeVarBinaryVector|testLargeListVector|arrow.c.jni.dist.dir' /tmp/af-res025-arrow-java/c
```

첫 `rev-parse` 결과가 위 blob과 일치해야 한다. 이 명령들은 소스 재독이며 런타임 검증이 아니다. 해당 snapshot의 요구 JDK/Maven과 `arrow_cdata_jni`를 준비한 환경에서 다음 실제 테스트를 실행한다. `c/pom.xml`은 네이티브 라이브러리 위치를 `${arrow.c.jni.dist.dir}`(기본 `./build`)로 받는다. 본 실행은 JDK·JNI·Maven 환경을 만들지 않았으며 이 명령의 성공을 관측하지 않았다.

```sh
mvn -f /tmp/af-res025-arrow-java/pom.xml -pl c -am -Dtest=RoundtripTest#testLargeVarBinaryVector+testLargeListVector -Dsurefire.failIfNoSpecifiedTests=false test
```

JNI 라이브러리 준비가 안 되어 중단되면 다음 첫 행동은 고정 snapshot의 네이티브 빌드 지침과 경로를 읽고 `arrow.c.jni.dist.dir`에 빌드 결과를 연결하는 것이다.

```sh
rg -n 'arrow_cdata_jni|cmake|jni.dist|C Data' /tmp/af-res025-arrow-java/README.md /tmp/af-res025-arrow-java/c /tmp/af-res025-arrow-java/docs
```

실제 Python → Java C Data 통합은 별도 same-process JNI/embedding fixture가 필요하다. 위 단위 테스트의 통과만으로 그 통합, 2GiB 초과, 2021년 Java C Data 지원을 판정하지 않는다. 역사 부분은 Java1.0.0 `ArrowBuf`의 long index/size와 `nioBuffer()`의 int 제한, 공식 1.0.0 릴리스 기록까지 확인했다. 옛 `TestLargeArrowBuf.java`의 4GiB 수동 시험은 PR6323 patch에서 읽었으나 1.0.0 태그의 추정 경로 3개 중 시험 경로를 확정하지 못했으므로 태그에 존재한다고 꾸며 명령을 만들지 않았다. 정확한 추가 소스 위치를 찾는 첫 명령은 해당 고정 태그를 checkout한 뒤 `rg --files java | rg 'TestLargeArrowBuf|TestLargeVector'`다.

## 미실시 검증 3: 당대 ScalarValue의 실제 공통 접근

고정 커밋은 `4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa`(2021-01-02)이며 소스는 `rust/datafusion/src/scalar.rs`다. `try_from_array` L245–289를 직접 읽었다. 원 파일의 기존 `scalar_list_null_to_array`·`scalar_list_to_array` 테스트는 **enum → array** 방향이다. 질문의 **array → enum** 방향을 실행했다고 혼동하지 않기 위해 별도 입력 `af_res025_scalar_probe.rs`를 제공한다. Boolean/String의 값·null, List<int32>의 `[7,null]`·null을 같은 accessor로 읽고 enum을 비교한다. 최초 사례의 Boolean/String/List 예시에 한정하며 미지원 datatypes, out-of-bounds, 성능, 적용 후 사용자 프로그램을 검증하지 않는다.

```sh
git clone --filter=blob:none https://github.com/apache/arrow.git /tmp/af-res025-arrow-historical
git -C /tmp/af-res025-arrow-historical checkout --detach 4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa
cp docs/workstreams/research/AF-RES-025/followups/arrow/verification-inputs/af_res025_scalar_probe.rs /tmp/af-res025-arrow-historical/rust/datafusion/tests/af_res025_scalar_probe.rs
cargo test --manifest-path /tmp/af-res025-arrow-historical/rust/datafusion/Cargo.toml --test af_res025_scalar_probe common_accessor_boolean_utf8_list -- --exact --nocapture
```

이 검증 입력은 작성했지만 컴파일하거나 실행하지 않았다. 역사 dependency resolution이나 Rust 도구 모음 때문에 실패하면 최초 판의 CI/toolchain/lockfile을 확인해 같은 입력을 재개한다. 실패를 ScalarValue 기능의 실패로 자동 분류하지 않는다. 그 다음 자료 한 건은 질문자 gist의 실제 후속 커밋 또는 작성자가 바꾼 호출부다. 현재 gist history는 단일 revision이라 표현된 선택과 실제 적용 diff 사이 공백은 남아 있다.

## 점검과 남은 판단

후속 코드·자료를 읽은 이 에이전트는 원 Arrow 검색을 수행한 동일 모델 에이전트다. 이번 후속 판독은 사람의 독립 검증이 아니다. 동결된 가린 판독과 별도의 비용·증거층이다. 자료의 재직렬화·분모·참조·해시 점검은 `SELF_CHECK.md`에 있고, 함수 실행의 성공은 주장하지 않는다.

우선순위가 높은 남은 판단은 Q01 실제 Python→Java C Data 통합 및 큰 버퍼 경계, Q02 표현된 선택 이후 실제 코드 변경, Q04 최초 공개 branch head와 Parquet 검증 범위다. 각각의 다음 입력은 위 명령과 `candidate-history.jsonl.next_minimum_check`, `decisions.jsonl.limitations`에 구체적으로 남겼다.
