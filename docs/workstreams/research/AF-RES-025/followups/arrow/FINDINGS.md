# Arrow 후속 계보·당대판 대조 (후속 단계 작업 기록)

각 절의 직접 근거 ID·원 URL·정확한 위치는 [EVIDENCE_MAP.md](EVIDENCE_MAP.md)와 [sources.json](sources.json)에 대응한다.

이 단계는 2026-11-22 05:50:22 UTC 원격 확인된 주 판정 봉인 `d1f506b1dde91e706360846f4c2eac5baabe492e` 다음에 시작했다. 최초 검색 반환·후보·가린 판정을 변경하지 않는다. 새로운 기능 원문을 여기서 찾더라도 검색 적중이나 최초 인용 완전성에 소급 산입하지 않는다.

## Q01: 현재의 설정 옵션은 2021년 답이 아니다

`binary_type`을 추가한 PR46532는 2025-05-27에 `a2941dd9a05666223110e8a879a2a5a226fb620d`로 병합됐다. `list_type`을 추가한 PR46678은 2025-06-04에 `03a1867571ef56bdb8c3842a5c26ed7e1ed94c52`로 병합됐다. 20.0.0의 Python Parquet core에는 두 옵션이 없고 21.0.0에는 둘 다 있다. 공식 21.0.0 발표는 2025-07-17이며, 큰 binary/list를 중간 32bit 형 변환 없이 읽는 기능과 각각 2GiB·2^31 값 제한 회피를 설명한다. 두 옵션은 저장된 Arrow schema가 있으면 무시된다는 조건도 PR diff와 21.0.0 코드에 있다. 따라서 AR-K001의 구체적인 조합은 최초일 2021-01-09에 이용 가능하지 않았다.

Java의 큰 버퍼 경계는 별개다. 1.0.0 발표(2020-07-24)는 큰 버퍼 할당과 LargeVarChar/LargeBinary/LargeList의 C++ 이진 호환 검증을 명시한다. 그 태그의 ArrowBuf에는 long capacity/index가 있다. 다만 `nioBuffer()`는 크기를 int로 변환하므로 모든 Java/ByteBuffer 경로가 큰 버퍼를 받는다는 뜻은 아니다. 이 단계에서는 2021년 Java C Data import까지 검증하지 않았다. 2.0.0 C++ schema 복원 코드는 LargeList 복원 분기를 이미 갖고 있으나, 이것은 외부 Parquet을 임의 대형으로 선택하는 2025년 옵션과 다르다.

후속 메일에서는 유지관리자의 최초 가능성 제안 뒤 질문자가 2.0.0과 master `5f1be953`에서 schema override 실패 재현을 보냈고, ARROW-11353(이관 issue27249)이 생겼다. 2021-01-25 유지관리자는 Python Parquet bindings에 일반적 read-type override가 없고 Dataset이 동일 schema를 요구한다고 설명했다. 이관 issue는 2026-06-26에 재현되지 않는다는 의견으로 닫혔다. 특정 PyArrow 옵션 도입과 그 issue의 정확한 수정판을 동일시하지 않는다. 질문자의 최종 채택은 찾지 못했다.

## Q02: 알려진 host와 뒤에 드러난 부품을 분리

2021-01-28 Andrew Lamb가 고정 커밋 `4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa`의 DataFusion ScalarValue를 제시했고, 질문자는 같은 날 해당 enum이 필요한 것이라고 답했다. 그 커밋은 2021-01-02다. `ScalarValue::try_from_array`는 Boolean/Utf8/List 등 런타임 분기를 내부에 두고 재귀 List 값을 공통 enum으로 만든다. 지원하지 않는 형은 NotImplemented를 반환하므로 모든 Arrow 형의 완전 구현으로 부풀리지 않는다. 질문자의 gist는 2021-01-28 단일 revision이며 StringArray downcast 구현만 있다. ScalarValue로 실제 수정·배포한 diff는 관측하지 못했다.

정정: DataFusion이라는 host 이름 자체가 검색에서 전혀 없었던 것은 아니다. 원 검색 Q02-R query3/rank4는 DataFusion 경로의 Arrow Array re-export였고 동일 원천 중복으로 제외됐다. **ScalarValue라는 다른 동작·부품이 원 반환에 없었다**는 것이 정확한 발견이다. 이 후속 발견을 검색의 신규 적중으로 추가하지 않는다.

Bevy 0.4.0은 2020-12-19에 공개됐고 `List::get(index)->Option<&dyn Reflect>` 및 DynamicList가 이미 있다. 관계 원리는 당대에도 가능했지만 Arrow adapter와 전체 계약은 별도다. quiver의 2018년 0.0.1은 Andy Grove의 Arrow 파일 형식 자리표시자이며 lib.rs는 산술 smoke test뿐이다. 2026년 rerun-io의 TypedArray 구현과 같은 이름이므로 최초 crate 날짜를 현재 부품의 나이로 쓰면 틀린다.

## Q03: 후속 구현은 일반 변환기보다 좁다

PR8648의 GitHub `merged_at`은 null이지만 close event의 실제 ASF 통합 커밋은 `1dc8f94ba7696ca5f7df20f76e6d81e62cdeaa69`(2021-04-19)다. 커밋 메시지의 Closes #8648과 실제 adapter_test.cc diff를 읽었다. 테스트 내부 `GenerateRandomChunkedArray`/`GenerateRandomTable`는 schema·길이·null 확률을 받는다. 기대값은 compute::Cast와 fixed-size binary 전용 변환, LargeList/FixedSizeList의 직접 배열 구성으로 만든다. 이는 ORC writer/read 결과로 기대값을 만들지 않는 경계와 부합한다. 그러나 임의로 중첩한 모든 schema에 대한 일반 재귀 변환기는 이 파일에서 확인되지 않았다. 최종 테스트의 Date64 기대값은 최초 메일의 millisecond가 아니라 nanosecond timestamp다. 따라서 후속 구현을 최초 요구의 모든 술어를 그대로 충족했다고 처리하지 않는다.

Arrow 3.0.0(2021-01-25)의 ArrayOf는 당대에 있었지만 최초부터 알려진 부품이다. 현재 반환의 BatchOf/GenerateBatch 및 JSON GenerateTestCase와 혼동하지 않는다. FastLanes 논문은 2024-07-15 제출, Blosc2의 현재 null 저장 변화는 4.11.0(2026-08-12) 계열이라 당대 추천으로 소급할 수 없다.

## Q04: 구조가 맞아도 검증·이행 경계가 남는다

Arrow2 PR1의 2021-02-11 댓글은 물리/논리형 분리, Buffer를 typed Buffer로 바꾸고 ArrayData 읽기/생성 의존을 단계적으로 제거하는 이행안을 제시한다. NativeType의 unsafe는 정렬·포인터 없는 물리값에 대한 FFI 가정 때문에 필요하다고 설명한다. 02-28 작성자는 IPC 통합 테스트 통과를 보고했지만 Parquet variable-sized 읽기와 기대값 검증 부족 때문에 migration을 보류하자고 했다. 03-04에는 PR을 닫고 별도 저장소를 사용 가능한 구현으로 만드는 쪽으로 전환했다. 이는 작성자 보고이지 이번 실행에서 테스트한 사실이 아니다.

02-08 고정 커밋 `2c515d260633d1ef9b8c8994f23ad42a39f62f77`의 diff에는 FixedSizeList와 Arc<dyn Array>가 추가된다. 이 diff의 slice 구현은 입력 length 대신 offset을 다시 곱해 length를 계산하는 것으로 보이며, 구조적 유사성만으로 당시 구현의 의미적 정확성까지 보장할 수 없다는 코드 판독 반례다(실행 미실시, 안전성 취약점 확정 아님). 첫 메일 당시 실제 branch head는 여전히 복구되지 않았다. 사전 공개 시간의 commit author/committer 값만으로 최초 branch 내용을 확정하지 않는다.

Arrow2 첫 crate 0.1.0은 2021-07-20, narrow 저장소는 2021-05-06/첫 crate는 07-29, minarrow 저장소는 2025-08-11/첫 crate는 08-12다. Arrow-rs ScalarBuffer는 PR1820에서 2022-06-09에 추가됐다. 이 사실들은 최초 제안에 대한 현재 추천과 당대 추천이 달라짐을 보여주며, 현재 후보의 누락 필수 조건을 해결하지는 않는다.

## 관측·반증 한계

당사자 미인지, 실제 인시 절감, 실행 성능, 4GiB Java 메모리 테스트, ScalarValue 적용 후 사용자 코드 diff는 확인하지 않았다. 역사 가용성 supported는 원 제안 사용의 필수 조건 전체에만 사용한다. 부분 기능 존재는 별도 feature_evidence이며, 불완전 인용을 이 후속 자료로 보강하지 않는다. 각 요청의 UTC·status·hash는 receipts에, 정확한 절·원 URL·한계는 sources.json에 연결한다.
