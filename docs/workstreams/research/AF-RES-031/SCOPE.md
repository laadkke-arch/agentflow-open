# AF-RES-031 범위와 사전 계약

- 시도 AF-RES-031#1, 조사 시작 2026-11-22 07:05 UTC. 저장소 laadkke-arch/agentflow-open, 브랜치 work/research-af-res-031, 소유 경로는 이 폴더다. 계획판 478c539b0fccbb7949ed7d7fbb6bf8810a2ca998, 작업 시작판 172c6bc37bdf91b91c86b9b3be29cb5b44fa4971. 최초 읽기 직후 1dd2555815f5fc4a2e8c7c87e438d058cd4b1a66에서 운영표만 갱신돼 사전 쓰기 전에 최신판으로 이동했다.
- 담당 codex-cloud, 실제 관리형 Linux Debian 13.6 x86-64, 시스템 Python 3.12.14와 Git 2.52.0. 확인 가능한 모델 표기는 GPT-6 기반 Codex이고 계정의 세부 모델 선택 및 추론 강도는 미확인이다. 4 CPU quota, cgroup 메모리 16 GiB, 임시 파일시스템 여유 60 GiB를 관측했다. 실제 실행 시점 자원은 별도 영수증으로 잰다.
- AF-RES-025@cf27e148b96bf3c5a3dc8a2a926db4abcf63f146의 인계·결과·pending·두 followup과 입력 두 파일을 읽었다. AF-RES-028@72a5d7f4fb4489fd183669dea49dc9659d941ca8의 인계·REPLAY·contract-amendments·verification에서 사전 계약과 정규화 출력의 검산 방법을 가져왔다. 통합판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, dot-control, CLOUD_WORKFLOW와 제품 연구 브리프를 읽었다.
- [025 선행 근거](https://github.com/laadkke-arch/agentflow-open/blob/cf27e148b96bf3c5a3dc8a2a926db4abcf63f146/docs/workstreams/research/AF-RES-025/RESULT.md)에서 Q01은 Arrow 호스트의 조건부 현재판 부품, Q02는 원 검색이 놓친 질문자의 표현된 선택, Q11은 최초 초안과 다른 위치를 받는 후대 부품이다. 초기 Arrow 메일은 접근을 시도했고 봉인 당시 원문 복구가 남아 있다. v6.27.0 전후 구현과 최초 JEP 초안은 직접 열었다.
- Python API는 공식 휠 20.0.0·21.0.0, Java는 arrow-java 7a581880a85358315d05da08296cf570b3643924, Rust는 apache/arrow 4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa, Jupyter 수신기는 6.26.0·6.27.0 휠로 고정한다. 송신기 8.6.0과 2021 초안의 위치를 각각 관측한다. Java C Data 임베딩과 노트북 메타데이터 복사는 연구자가 추가하는 연결부다.

## 판정 규칙

- 필수 행은 contracts.jsonl의 식별자로 비교한다. 양성은 소비자 측 정확한 값·형·위치 일치다. 경계 대조는 예측한 예외, 형, fallback 또는 값 부재가 실제로 관측되어야 성립한다. 예상한 반대 대조의 관측은 해당 조건에서의 기각 근거다.
- 실제 원 테스트는 이름과 실행 수까지 확인한다. 종료 0 또는 모듈 로드만 관측한 경우 유효한 시험은 미확인이다. 직접 실행, 공식 동시대 실행 기록, 고정 테스트/소스 정적 판독, 연구자 예시를 구분한다. 성공 판정에는 빈 폴더에서 같은 입력으로 정규화 결과가 재현되어야 한다.
- Python 읽기는 디스크의 스키마 키, 물리 offset 버퍼의 폭·값, 값·부모 null·자식 null을 대조한다. Java IPC와 C Data는 같은 소스 SHA의 실제 소비자에서 형·오프셋·값을 직접 대조한다. 2 GiB 초과 경계는 오프셋 2,147,487,744에서 읽고 명시된 메모리 여유·할당량·touch를 확인할 수 있을 때만 실행한다. 할당 실패·환경 제한은 기능 판정에서 보류한다.
- Rust는 ArrayRef와 유효 인덱스를 넘기며 결과 enum 처리가 필요할 수 있다. 관측 코드는 고정 공급자 accessor를 그대로 호출한다. 고정판에 Cargo.lock이 없으므로 의존 해결 보강 시 조합과 원본 소스 차이를 명시한다. 1.49.0은 당시 stable 근사이며 실제 CI patch 버전은 미확인이다.
- 커널 시작, 서명된 로컬 송신, 수신 do_execute의 sentinel과 인수 제공 여부, reply의 parent ID를 잇는다. 둘 다 없는 대조는 root 빈 사전과 content.metadata 부재를 구별한다. 노트북 파일 셀 id와 전달한 metadata.cellId는 별개다.
- 025의 72슬롯 및 028의 42셀은 역사 관측이다. 임시 파일과 원문 cache는 /tmp에서 유지한다. 새 관측이 원 검색 적중, 실제 도입, 배포, 인시 절감을 보여주는지는 미확인이다.
