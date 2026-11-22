# 미실시 검증과 재개 입력

이 파일은 실행 영수증이 아니다. 문서·코드·공식 테스트의 정적 판독으로 남은 경계를 확인할 명령과 입력이다. 공급자 제품의 전체 도입·성능을 이번 연구에서 실행했다고 주장하지 않는다. 새 실행은 최초 검색/판정과 다른 단계의 영수증으로 저장해야 한다.

## 1. PyArrow 옵션의 실제 입력 의미

현재 AR-K001을 실제 사용하려면 저장 Arrow schema의 우선순위를 확인해야 한다. 이미 준비한 입력은 Binary `[b'ab', null, b'xyz']`, List<int32> `[[1,null,2],null,[]]`의 세 행이며 같은 데이터를 schema 저장/미저장 두 파일로 쓴다. 스크립트와 정확한 예상/비검증 경계는 [Arrow README](followups/arrow/README.md)에 있다. 외부 패키지 설치가 가능한 별도 실행 환경이 필요하다. 이 환경에 설치하지 않았고 성공 여부를 주장하지 않는다.

```bash
AF025_BASE="$PWD/docs/workstreams/research/AF-RES-025"
python3 -m venv "$AF025_BASE/runtime/pyarrow21"
"$AF025_BASE/runtime/pyarrow21/bin/pip" install pyarrow==21.0.0
"$AF025_BASE/runtime/pyarrow21/bin/python" "$AF025_BASE/followups/arrow/verification-inputs/q01_pyarrow21_probe.py" --output-dir "$AF025_BASE/runtime/q01-fixtures"
```

예상: schema 미저장은 large_binary/large_list, schema 저장은 원래 binary/list다. 값과 null을 함께 비교한다. 이 작은 입력 통과는 2GiB 초과·Java·C Data 포인터 수명까지 증명하지 않는다. 출력은 새로운 결과 ID와 도구/버전/시각을 붙여 기록한다.

## 2. Java 경계: IPC, C Data, 2GiB를 구분

읽은 공식 테스트는 arrow-java snapshot `7a581880a85358315d05da08296cf570b3643924`, `RoundtripTest.java` blob `4d2acbb091af4e563e2a08fc2ae319a57f797f14`다. `testLargeVarBinaryVector`와 `testLargeListVector`의 명령은 Arrow README에 있다. 준비된 JDK·Maven·C Data JNI 환경이 필요하며 이번에는 실행하지 않았다.

다음 첫 행동은 그 고정 소스의 build 전제와 테스트 두 개를 먼저 재현하는 것이다. 이는 Java→C Data 구조→Java 경계다. Python이 만든 IPC 파일을 Java로 읽는 시험은 프로세스 간 직렬화 경계이고, Python→Java C Data는 같은 주소 공간/수명 보장을 구현해야 한다. 서로 다른 프로세스 사이에 주소 숫자를 넘기는 것으로 C Data 통합을 검증할 수 없다. 2GiB 초과 fixture는 메모리 예산·allocator·정확한 입력 크기를 정한 별도 실행으로 남긴다.

## 3. Q02의 당대 ScalarValue 호출 경계

고정 코드 `apache/arrow@4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa`의 `rust/datafusion/src/scalar.rs`에서 `try_from_array` L245–289를 읽었다. 입력은 Boolean, Utf8, List와 null이며, 공통 accessor로 읽은 enum 값과 지원하지 않는 타입의 오류를 확인한다. [준비한 Rust 입력](followups/arrow/verification-inputs/)과 고정 checkout·cargo 명령은 Arrow README에 있다.

다음 첫 행동은 공식 당시 테스트와 준비한 입력을 같은 고정 checkout에서 실행해, 호출자 downcast가 없어지는 범위와 내부 type dispatch를 분리하는 것이다. 빌드 의존성·당시 Rust 환경을 이번 연구에서 설치하지 않았다. 이 검증이 성공해도 원 G/R 검색의 적중으로 소급하지 않고 후속 발견의 별도 기능 검증으로 보고한다. 질문자의 실제 코드 적용을 확인하려면 당대 gist 이후 revision 또는 별도 저장소 diff가 더 필요하다.

## 4. GCC10.3의 우선순위·포함 파일·문자열 경계

CG-K011의 역사 supported는 고정 공식 소스/테스트 정적 판독이다. 실행을 재개할 때 `AF025_GCC103`을 checksum까지 확인한 GCC10.3.0 바이너리로 정하고, source root에 main/header를 둔다. main과 header의 `__FILE__`, `__BASE_FILE__`, 같은 root가 포함된 평범한 문자열 리터럴을 각각 출력하도록 한다. [Cargo README](followups/cargo/README.md)의 다음 명령을 쓴다.

```bash
"$AF025_GCC103" --version
"$AF025_GCC103" -g -ffile-prefix-map="$AF025_SOURCE_ROOT"=/AUTO -ffile-prefix-map="$AF025_SOURCE_ROOT"=/USER "$AF025_SOURCE_ROOT/main.c" -o "$AF025_SOURCE_ROOT/out"
"$AF025_SOURCE_ROOT/out"
readelf --debug-dump=info "$AF025_SOURCE_ROOT/out"
readelf --debug-dump=decodedline "$AF025_SOURCE_ROOT/out"
```

사용자 map이 이기고, 포함 파일의 컴파일러 경로도 바뀌며, 일반 문자열은 바뀌지 않아야 한다. 이 명령은 Cargo/Rust drop-in 대안을 시험하지 않는다. 새 감사의 원문이나 실행으로 최초 인용 누락을 소급 보강하지 않는다.

## 5. 남은 문서·판정 검증

- 당시판 전체가 unknown인 후보 46개는 각 `followups/*/candidate-history.jsonl.next_minimum_check`가 구체 자료/태그/테스트 경계를 지정한다. 모든 후보에 추가 검색을 무한 반복하지 않고, 실제 채택 판단에 영향을 주는 한 조건부터 보강한다.
- JEP66의 10초 차이 이전 blob, Arrow Q04의 최초 공개 branch head는 아직 복구하지 못했다. Git commit author time만으로 당시 branch 내용을 확정하지 않는다.
- Cargo 후속 inline review 126개는 읽지 않았다. Q06 최초 후속 언급의 범위를 넓히려면 RFC3127의 inline review 101개를 시간순으로 읽고 2021-06-27보다 이른 GCC/Clang 명시가 있는지 확인한다.
- 공유 문맥·원 URL 예산 초과·가림 누출을 없앤 비교는 새 실행이어야 한다. 재실행자는 `queries.jsonl`에 연결된 동일 최초 전문을 받되 기존 후보·결론을 받지 않아야 하며, 결과를 처음 열기 전에 경로당 최종 URL 세 개의 단위를 다시 봉인한다.
- 실제 인시 절감은 문서 검산으로 얻을 수 없다. 사용자 사전 제품/부품/제약 목록, 반환의 실제 적용, 정확도와 소요시간을 관측하는 별도 과제를 먼저 정의한다.
