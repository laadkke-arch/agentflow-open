# Arrow 후보의 가린 교차 판독 — Cargo 담당 별도 읽기

## 범위와 판정 단위

이 판독은 경로와 순위를 가린 Arrow 후보 **25개**, 인용 패키지 **30개**, 필수 술어 **80개**를 평가했다. 질문 분모는 Q01 8개 후보, Q02 6개, Q03 7개, Q04 4개이다. 질문의 최초 입력 전문 네 개를 모두 읽고 입력 해시를 확인했다. `reviews.jsonl`은 후보마다 모든 패키지와 모든 술어를 포함한다.

권위 입력은 가림 추가판 커밋 `64f2db1004d5e40842a6f347a835964bcb8503ef`의 `blind/arrow.jsonl`이다. 단일 Arrow 파일 SHA256은 `ade09ece0ee7ff48c7cafcd8274ecb5a489a740ec453cd5acc3791eaa21524a0`이다. 진행 담당이 알린 `61211534…53cadd43`은 전체 `blind/packets.jsonl`의 합성 해시이므로 두 값은 서로 다른 파일을 가리킨다.

읽은 범위는 이 패킷, 그 안에 지정된 최초 입력 네 개, 인용된 공급자 원문으로 제한했다. 원 경로의 검색/반환 로그, 경로 대응표, 다른 판독자의 결과, 후속 결정, 도서관·제조 보조 사례는 읽지 않았다. 따라서 여기서는 경로별 승패, 당시 배포 가능성, 후속 선택과의 일치를 계산하지 않는다. 새 후보를 검색하거나 반환 슬롯을 늘리지 않았다.

## 핵심 판정

| 범위 | 결과 | 판정의 한계 |
| --- | --- | --- |
| 완전 열람 및 완전 인용 패키지 | 1/30, B-861f15b42c8d / P-12785fe987ac | 이미 알려진 Arrow의 현재 dev 문서상 조건부 구성이다. 새 대상의 발견으로 세지 않는다. |
| 패키지 상태 | supported 1, hold 15, conflict 14 | 문서/호출 경계의 평가이며 실행 성공률이 아니다. |
| 새 대상 | 12/25 후보; 완전 인용 0/12 | 원 입력의 침묵을 실제 사용자 미인지로 바꾸지 않는다. |
| 술어 수준 | 원 열람으로 지원 13/80; 원 반환 인용으로 지원 12/80 | 패키지 전체 합격과 다르다. |
| 인용 누락 | B-b5d59419429a / P-1e6ea2b61bbd / Q04-M3 | 원 열람은 정렬 설명과 C export 예를 함께 포함하지만 원 반환은 버전 docs만 인용한다. 다른 패키지 P-43b64dadbbad와 별도로 판정했다. |
| 직접 감사 | 21회 열람 요청, 고유 URL 18개, 성공 본문 URL 16개 | rewritten-summary 표시 1개를 추가 제외하여 직접 원문 재열람은 보수적으로 15개이다. 접근 실패는 2개 URL에서 총 3회였다. |

### Q01: offset 숫자보다 방향·표현·파일 조건이 중요하다

B-6f6a81e577af의 `WriteBatchArrow64`는 Arrow buffer를 받아 Parquet에 쓰는 방향이다. Parquet에서 large-offset Arrow를 읽는 요청과 반대이다. B-933cfc0417e0의 `int64`는 정수 값의 폭이며 목록 offsets의 폭이 아니다. B-ee26f02e094d의 FILE offset 역시 외부 파일 위치와 메모리 배열 offsets를 혼동하면 안 된다.

B-1f41797915cf의 목록 전용 사용은 LargeBinary 미지원만으로 거절하지 않았다. 실제 제안한 목록 경계에서는 LARGE_LIST 옵션이 확인된다. 다만 저장된 Arrow schema가 우선하며 Java 전달 근거가 없다. B-a3faef591df3은 저장 schema가 있는 파일로 사용 경계를 한정했으므로 LargeList 복원을 지원한다. 그 인용만으로 Java 전달까지 증명하지는 않는다.

B-861f15b42c8d는 binary/list 옵션, 저장 schema 예외, 64비트 형 정의, Java 수용 경계를 세 인용으로 연결한다. 이는 문서가 제공하는 조건부 구성이다. 실제 큰 buffer를 Java로 넘긴 실행이나 안정판 출시일, 2021 가용성은 별도 미확인이다.

### Q02: 공통 이름과 공통 runtime 호출을 나눴다

B-72121aa5d298은 한 번 L을 정하고 검증한 후 같은 `value/get`를 쓸 수 있어 반복 downcast 감소는 지원한다. 그러나 `TypedArray<L>`의 반환형은 정적으로 정한 L에 의존한다. 임의 `dyn Array`의 String/Boolean/List를 동일 반환 규약으로 읽는 조건에는 맞지 않는다.

B-a1fa7bb168d2의 AsArray는 downcast 문법을 줄인다. 구체 타입을 고르는 호출과 분기는 남는다. Rust Any와 Dynamic 값 용기도 공통 배열 index API를 제공하지 않는다.

B-69175f855707의 Bevy는 원 제안대로 설계 원리로 평가했다. 공통 반사 값, 분류별 getter, dynamic proxy의 관계는 성립한다. 다만 이 overview 인용에는 공통 sequence-index 접근과 세 배열형의 반환 규약이 없다. 이미 구현된 Arrow adapter가 없다는 이유로 원리 후보를 거절한 것은 아니다. B-cfb398d15ce8도 vtable 호출 관계를 인정하지만, 공통 scalar 표현의 실제 설계는 남는다.

### Q03: 입력 생성과 변환 oracle는 별도의 부품이다

B-e9f810131568은 중첩 field metadata, null 확률, 길이, seed를 받는 RecordBatch 생성 계약을 제공한다. 최초 입력은 이미 `random.h/ArrayOf`를 알고 있었으므로 새 대상이 아니다. Table 조립과 요청한 Large*/Date64 재귀 변환은 별도다.

B-93c14012f95c은 고정 seed를 써서 JSON 입력과 expected batch를 만드는 구조이다. ORC를 호출하지 않는 기대값 구성 원리는 지원하지만 고정 schema와 null 확률 0은 일반 generator 조건에 충돌한다. FlatBuffers/SQL의 타입 코드 생성은 데이터 행 생성과 다르다. FastLanes의 nullmap/offset 분해나 Blosc의 null 변환을 정확한 ORC expected로 자동 치환하지 않았다. ORC 수동 row batch는 독립 fixture의 재료가 될 수 있으므로 ORC 자체 문서라는 이유만으로 독립성 위반으로 판정하지 않았다.

### Q04: 정적 타입·동적 타입·FFI·안전 계약은 각각 확인해야 한다

narrow의 runtime arbitrary type non-goal은 요구한 dynamic typing 보존과 충돌한다. 접근 실패를 새 기능 부재로 바꾸지는 않았다. 일반 Rust generics는 타입 T와 runtime DataType 태그를 분리해 둔 응용 설계의 불일치까지 자동으로 막지 않는다.

B-ac7b5f5909e2는 현재 typed buffer constructor, nested List, dyn Array와 supplier의 safe API 계약을 지원한다. formal proof를 제시하지 않았다는 이유만으로 M4를 거절하지 않았다. 그러나 overview의 FFI module 링크는 외부 포인터의 정렬·수명·소유권 전제를 확인한 근거가 아니어서 M3는 보류했다.

minarrow의 enum dispatch와 C export 예는 확인된다. List/Struct가 기여 요청에 등장한다는 사실만으로 미구현을 단정하지 않는다. public constructor의 불변식과 nested 구현은 보류했다. 원 패키지의 0.19.0 정렬 문서는 현재 재접근 실패로 원 관측에 의존하므로, 해당 M3 지원은 직접 재확인된 현재판 사실과 구별한다.

## 열람과 인용의 계산 계약

- `status`는 각 필수 술어의 supported/conflict/unknown 판정이다. 공급자가 한 말, 제안된 사용, 검토자의 조건부 추론을 `provider_facts`, `researcher_proposed_use`, `reason`으로 분리했다.
- `support_in_original_opened`는 원 패킷에서 실제 열람한 URL·절 묶음이 해당 술어를 지원하는지를 뜻한다.
- `support_in_original_citations`는 같은 근거 묶음 **전체**가 원 반환 인용에 포함되는지를 뜻한다. 하나만 인용했다고 true로 만들지 않는다.
- `opened_complete/cited_complete`는 모든 필수 술어의 앞선 불리언을 AND한 값이다. 각 원 인용 패키지는 변경하지 않고 `returned_citations_unchanged`에 보존했다.
- `current_audit_opened_complete`와 `current_audit_version_observations`는 감사에서 직접 다시 확인한 범위를 별도로 남긴다. 현재 열람을 원 반환 인용에 추가하지 않는다.
- `required_bundle_source_coverage_*`는 URL·절의 형식적 포함 관계이다. 증명의 내용이 맞는다는 의미는 아니다. 원 패킷이 적은 missing 메모에도 불구하고 실제 제안한 좁은 경계에는 충족하는 경우가 있어, 내용 판단을 따로 했다.
- 원 열람/반환 인용이 빈 B-0bd3c02d9d92는 보류를 유지한다. 감사자가 결과로 새 반환 후보를 만들지 않았다.
- `counterexample`은 직접 확인한 제약 또는 그 제약에 넣는 구체 입력이다. 실제 실행은 하지 않았으며 실행한 반례라고 주장하지 않는다.

## 재현성과 노출 한계

같은 source_id가 서로 다른 URL/판을 가리키는 패킷이 있다. S-9ed752c6e926은 59.0.0과 60.1.0, S-30983fd45f2f는 docs.rs 56.2.0과 apache.org 현재 문서에 재사용되어 있다. 이 판독은 source_id만으로 근거를 합치지 않고 **source_id + URL + 절**을 비교한다. 패킷 source metadata의 URL과 패키지 URL이 다르면 원 판을 미확인으로 남겼다.

현재 재조회는 판을 고정하지 못한다. PyArrow의 첫 열람 헤더는 dev39, 같은 URL의 해당 절 열람은 dev153이었다. qio의 원 관측은0.1.0, 감사 PDF는0.1.2이다. 원 관측의 지원 여부는 패킷 기록을 평가한 것으로, 현재판 재열람과 동일하다고 주장하지 않는다. 늦은 문서의 새로운 근거로 최초 인용을 보강하지 않았다.

추가 가림 전 source limitations의 경로 이름을 본 후보는 B-a1fa7bb168d2, B-ac7b5f5909e2, B-e9f810131568 세 개이다. `exposure.json`에 읽은 범위와 문구를 남겼다. 수정 후에도 이 노출을 취소할 수 없으므로 세 키를 완전한 가림으로 주장하지 않는다. source의 버전·한계·required bundle 자체는 패킷에 주어졌으므로 경로/순위 가림이지 최초 작성자의 모든 판단 정보에 대한 가림은 아니다.

판독자는 검색 담당자와 별도 에이전트이지만 **같은 모델 계열의 별도 읽기**이다. 사람의 독립 검증이나 다른 모델에 의한 검증이 아니다. packet-only/failed-reopen 상태를 각 술어에 남겨 재열람한 원문과 구분했다.

## 비용과 파일

감사 요청은 2026-11-22T05:34:53.814Z부터05:36:38.384Z 사이에 이루어졌다. 총 요청별 wall time 합은11,560ms이며 병렬 요청이 있으므로 이것을 전체 연구시간으로 해석하지 않는다. 21회 중 추가 같은 URL 요청은 해당 절을 여는2회와 narrow 재시도1회이다. 검색 질의는0회다. 토큰과 실제 인시는 도구가 제공하지 않아 미확인이다.

`receipts/`는 요청, UTC, elapsed_ms, 응답 헤더/원문 ref, 제공된 행 번호, 응답 JSON의 SHA256을 저장한다. 장문 본문을 재게시하지 않았다. `sources.json`은18개 URL의 확인 내용과 한계를 담고, 직접 읽은 원문은15개로 보수적으로 구분한다. 같은 원문의 감사 재열람이므로 연구 전체의 고유 외부 원문 최소수에는 더하지 않는다.

재집계는 이 디렉터리의 `build-review.py`를 실행한다. 입력은 가림 패킷, 그 안의 최초 입력 네 개, 이 디렉터리의 판독 메모와 영수증뿐이다. `summary.json`이25/30/80 분모와 술어별 인용 누락을 재계산한다. `seal.json`은 제출 파일의 최종 해시를 기록한다.

후속 결정이나 보조 분야 자료를 열기 전에 이 판독을 종료한다.

