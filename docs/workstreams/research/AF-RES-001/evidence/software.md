# AF-RES-001 — 실제 소프트웨어에서 확인한 입력 손실 반례

확인일: 2026-11-20 KST / 2026-11-19 UTC. 작성자: 주 작성 에이전트.
C01–C10은 서로 다른 본문 자료 10개다. C03의 구/신 버전은 하나의 자료 묶음으로 세었다.
문서 설명(D1)과 구현 관찰(D2)을 구분한다. 외부 소프트웨어·API·모델 실행(D3), 프로젝트 통합(D4)은 수행하지 않았다.
아래 “입력 함의”는 연구자 추론이며 해당 제품이 AgentFlow 입력을 권고했다는 뜻이 아니다.

## C01 — OpenTelemetry Collector Architecture

- 원문: https://opentelemetry.io/docs/collector/architecture/
- 위치/고정성: Pipelines, Receivers, Exporters, Processors. 열람 본문 26–187행. 페이지 표시 최종 변경 2026-03-14. 변경 가능한 문서의 확인일 스냅샷이며 특정 실행 바이너리 검증이 아니다.
- 수준/확인: D1. 여러 pipeline이 receiver나 exporter를 참조할 수 있다. 공유 receiver에서 각 pipeline으로의 전달은 동기 호출이므로 한 processor의 막힘이 다른 pipeline 수신에도 영향을 줄 수 있다고 설명한다. 동일 processor 설정을 여러 pipeline에서 참조하면 pipeline마다 독립 instance/state가 생긴다고 설명한다.
- 입력 함의: 하나의 선택 부분만 받더라도 **공유되는 주변 객체와 영향 경계**가 답을 바꿀 수 있다. 같은 이름을 같은 실행 instance로 합치거나 모든 선을 독립 비동기 전달로 읽으면 안 된다.
- 한계/반례: 전체 Collector 구현·모든 component 동작을 읽지 않았다. 모든 부분 질문에 전체 배포도를 요구해야 한다는 증거는 아니다. 원리 탐색에서는 관련 경계만 부연할 수 있다.

## C02 — OpenTelemetry Collector Resiliency

- 원문: https://opentelemetry.io/docs/collector/resiliency/
- 위치/고정성: Sending queue, Persistent storage, Message queues, Circumstances of data loss; 본문 34–164행. 페이지 표시 최종 변경 2026-01-14.
- 수준/확인: D1. 메모리 queue와 retry, file_storage를 쓰는 영속 queue, 외부 message queue를 구별한다. 영속 queue도 디스크 장애·공간 부족·재시도 한계 등에서 자료 손실을 막는 절대 보장이 아니다. 외부 queue는 운영 복잡성을 추가한다.
- 입력 함의: “재시작에도 덜 잃기”를 “정확히 한 번 전달”로 올리지 않는다. 손실을 줄일 장애 범위, 외부 서비스 추가 금지, 디스크 사용 가능 여부는 서로 다른 조건이다.
- 한계/반례: 이 문서의 일반 기본값을 입력 사용자의 실제 설정으로 채우면 안 된다. 처리량·queue 크기·유실률을 측정하지 않았다. 큐를 늘리는 제안만으로 지연·중복·영구 유실 문제를 모두 해결했다고 판단할 수 없다.

## C03 — Paperless-ngx Configuration, duplicate setting의 버전 차이

- 고정 원문(개발 브랜치 문서): https://github.com/paperless-ngx/paperless-ngx/blob/14252054a150595d89040a02cb510b9f43f4570b/docs/configuration.md
- 고정 원문(v2.20.15): https://github.com/paperless-ngx/paperless-ngx/blob/05e48b23166df7c7afe6f329b460b0511a89496c/docs/configuration.md
- 위치: PAPERLESS_CONSUMER_DELETE_DUPLICATES. 개발 문서 1390–1396행 / 구버전 1147–1152행. 구버전 태그 객체 d9f0bfcc2706305e56405bb6a54ffdd0f521088f가 가리키는 commit을 별도 조회했다.
- 수준/확인: D1. 개발 문서는 v3부터 기본적으로 중복 문서를 허용하며 해당 설정이 켜지면 동일 hash 파일을 소비하지 않고 입력 폴더에서 삭제한다고 설명한다. v2.20.15 문서는 중복 검출 시 원래 파일을 건드리지 않는 동작과 기본 false를 설명한다. **같은 설정명과 false만으로 버전별 결과를 복원할 수 없다.**
- 입력 함의: 기존 제품의 실제 설정을 다룰 때 버전/설정과 원하는 보존 위치를 묻는다. 버전이 없으면 버전별 문서 비교까지만 가능하다.
- 한계/반례: dev HEAD는 출시·배포 버전의 증거가 아니다. 사용자 설치 버전을 추정하지 않았다. 문서 설명과 특정 환경의 실행 결과는 다르다.
- 접근 기록: docs.paperless-ngx.com/configuration/는 웹 open에서 403이었다. 검색 요약을 열람으로 세지 않고, 공식 공개 저장소의 문서를 고정 SHA에서 읽었다.

## C04 — Paperless-ngx v3 Migration Guide

- 고정 원문: https://github.com/paperless-ngx/paperless-ngx/blob/14252054a150595d89040a02cb510b9f43f4570b/docs/migration-v3.md
- 위치: Duplicate Handling Changes, OCR and Archive File Generation Settings. 전체 반환 문서를 읽었으나 이 연구의 주장 범위는 두 절이다.
- 수준/확인: D1. v3의 중복 허용 변경을 설명한다. OCR 수행 여부와 archive 생성 여부를 분리한 설정 변경도 설명하며, 구설정값의 단순 재사용이 의미 보존을 보장하지 않는 사례다.
- 입력 함의: “기존 동작 유지”가 목표이면 옵션의 이름뿐 아니라 **어떤 결과를 유지할지**가 필요하다. 과거 설계·현재 구현·앞으로의 변경을 별도로 읽어야 한다.
- 한계/반례: 이행을 실행하지 않았고 문서의 모든 변화를 검증하지 않았다. 구성이 명확한 새 설계의 일반 원리 탐색에 이행 버전을 필수 입력으로 요구하지 않는다.
- 접근 기록: 공식 문서 사이트 open 403. 공식 저장소 고정본 열람으로 대체했다.

## C05 — Paperless-ngx Usage, 소비 위치와 보존 위치

- 고정 원문: https://github.com/paperless-ngx/paperless-ngx/blob/14252054a150595d89040a02cb510b9f43f4570b/docs/usage.md
- 위치: The consumption directory와 직전 original document 설명, 146–182행.
- 수준/확인: D1. 원본은 Paperless 내부 파일 구조에 저장되고 archive가 있으면 함께 보존된다. 입력 consumption directory는 임시 위치이며 소비한 파일은 그 위치에서 제거된다고 설명한다. 특정 document action 예외도 명시되어 있다.
- 입력 함의: “원본 보존”을 “원래 입력 폴더의 파일이 그대로 남음”과 동의어로 바꾸면 틀린다. **무엇을 어디에 보존하는가**를 원문에 연결해야 한다.
- 한계/반례: 일반 소비와 중복 거절의 세부 경로는 다르다. 특정 설정만으로 일반 입력 파일의 보존 요구가 해결된다고 말할 수 없다. 별도 복사 단계의 적합성은 제안일 뿐 실행 검증하지 않았다.

## C06 — Automerge Conflicts

- 원문: https://automerge.org/docs/reference/documents/conflicts/
- 위치/고정성: What is a Conflict? 및 getConflicts 설명, 열람 60–114행; 확인일 기준 문서, 라이브러리 빌드 버전은 고정하지 않았다.
- 수준/확인: D1. 같은 property에 동시로 쓴 값 중 한 값이 일반 읽기에 나타나더라도 다른 값은 conflict 정보로 남을 수 있다. getConflicts로 확인할 수 있으며, 이후 해당 property에 대입하면 conflict가 해소된 것으로 취급된다. 문서의 LWW는 벽시계가 아닌 내부 operation ID 기준이다.
- 입력 함의: “같은 상태로 합쳐짐”을 “사람의 의도가 보존되어 충돌 판단이 필요 없음”으로 바꾸지 않는다. 기계적인 수렴과 업무상 선택은 서로 다른 목적이다.
- 한계/반례: 모든 데이터형·사용자 경험을 시험하지 않았다. 서로 다른 property 편집처럼 자동 합치기가 충분한 경우까지 매번 수동 확인을 강제할 근거는 아니다.

## C07 — Automerge Local Storage & Sync

- 원문: https://automerge.org/docs/tutorial/local-sync/
- 위치/고정성: Storage & Network Adapters, Testing Storage and Sync; 61–203행, 확인일 기준 튜토리얼.
- 수준/확인: D1. IndexedDB 저장 adapter와 같은 브라우저/동일 origin의 탭 간 BroadcastChannel network adapter를 별도로 설정한다. 문서 생성은 storage와 network 역할에 각각 연결된다.
- 입력 함의: “브라우저에서 로컬로 동작”만 보고 “외부 전송 없음”이나 “다른 기기와 동기화됨”을 채우면 안 된다. 저장 위치·연결 대상·통신 허용은 다른 정보다.
- 한계/반례: 설치 명령과 예제 실행을 수행하지 않았다. 브라우저 저장의 영구성·용량·데이터 보호를 보장하지 않는다. 원리 소개에 전체 브라우저 사양을 먼저 요구할 이유도 없다.

## C08 — Automerge Network Sync

- 원문: https://automerge.org/docs/tutorial/network-sync/
- 위치/고정성: Collaborating over the internet, Network Not Required; 61–110행, 확인일 기준 문서.
- 수준/확인: D1. 인터넷 peer와 동기화하는 network adapter를 추가할 수 있다. 로컬에 있거나 이미 읽은 자료는 연결이 끊긴 동안에도 수정할 수 있고, 연결 회복 후 변경을 교환한다. 튜토리얼의 공개 sync server는 production 신뢰성/자료 안전 보장이 없다고 명시한다.
- 입력 함의: “오프라인에서도 편집”은 “절대 통신하지 않음”과 다르다. 오프라인 수정과 이후 동기화를 시간 조건으로 보존하면, “offline” 하나의 불리언으로 생기는 오해를 피할 수 있다.
- 한계/반례: 연결이 영구히 없는데 원격 사용자가 현재 변경을 즉시 보는 요구를 이 문서가 해결하지 않는다. 공개 데모 서버를 사용자의 운영 환경으로 전제하지 않는다.

## C09 — RFC 9110, HTTP Semantics

- 원문: https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3
- 고정 버전/위치: RFC 9110, June 2022, §15.3.3 202 Accepted. 해당 본문 3327–3331행.
- 수준/확인: D1(표준). 202는 처리 접수와 미완료를 나타내며 나중에 실제로 처리되지 않을 수도 있다. HTTP 상태코드만으로 비동기 작업의 후속 완료가 다시 전달되는 기능은 없다.
- 입력 함의: “접수됨”을 “완료됨”으로 변환하지 않는다. jobId, callback, 상태조회 경로는 실제 입력에 있거나 별도로 확인된 범위만 기술한다.
- 한계/반례: 202만으로 callback·polling·jobId 존재를 추정하지 않는다. 표준을 읽었지 특정 서비스가 표준을 준수함을 실행 확인한 것은 아니다.

## C10 — Paperless-ngx consumer.py, pre_check_duplicate

- 고정 원문: https://github.com/paperless-ngx/paperless-ngx/blob/14252054a150595d89040a02cb510b9f43f4570b/src/documents/consumer.py
- 위치: pre_check_duplicate 1052–1103행, 호출부 run 1114–1126행; blob c060368b4da2fdba099f38892b4369a4f6c90c3c.
- 수준/확인: D2(구현 관찰). checksum 또는 archive_checksum이 같은 기존 문서를 찾는다. CONSUMER_DELETE_DUPLICATES 조건 안에서 input_doc.original_file을 unlink하고 중복 예외를 발생시키는 경로를 읽었다. run이 이 검사를 호출하는 것도 확인했다.
- 입력 함의: “중복 문서 등록 방지”와 “입력 파일 삭제 금지”는 실제로 별개의 효과다. 같은 “중복 처리” 키워드로 합치면 필수 제약을 잃는다.
- 한계/반례: 해당 경로만 읽었으며 설정 로딩·동시 처리·파일시스템 장애·끝까지의 task orchestration은 실행하지 않았다. 모든 입력 경로의 보존을 인증하지 않는다.

## 조사 질문과 좁은 관측의 재사용

처음 검색은 공식 도메인에 한정해 “Collector resiliency persistent queue”, “Paperless consumption duplicates”, “Automerge conflicts local sync”, “RFC 9110 202 Accepted”로 진행했다. 결과 목록은 본문 열람 수에 넣지 않았다. 이후 공식 본문 또는 고정 GitHub 문서를 열어 위 주장의 범위만 확인했다.

이 자료는 후보 제품의 우열 평가가 아니다. 동일한 사용자의 짧은 표현이 서로 다른 결과를 뜻할 수 있는 지점을 찾는다. 입력 대안은 이 오류를 막는 데 쓰일 정보를 비교하되, 원문에 없는 주변 기술·운영 사실을 채우지 않는다.

## 초기 가설을 바꾼 점

“대상 부분 + 한 줄 목적이면 충분”은 원리 탐색의 출발점으로만 남긴다. C05/C10은 대상 자료의 위치와 부작용이 빠지면 뜻이 뒤집히는 반례, C03/C04는 동일 옵션 이름이 버전에 따라 다른 결과를 내는 반례다. C06/C08은 넓은 단어(충돌 해결·오프라인)가 여러 의미를 담는 반례다. 반대로 이런 상세 정보가 미상이라는 이유로 전체 원리 탐색을 중단할 필요는 없다. 정확한 구성·적합 판정과 일반적 원리 비교의 주장 범위를 달리한다.

