# AF-RES-031#1 인계 · REVIEW_READY_WITH_GAPS

**고정 결과 SHA 5b06d0158868a3cc790da55546504ddf5a46eecc.** [계약별 실측·재생·반환 링크](https://github.com/laadkke-arch/agentflow-open/blob/5b06d0158868a3cc790da55546504ddf5a46eecc/docs/workstreams/research/AF-RES-031/RESULT.md)

| 실측 분모 | 결과와 소비자 경계 |
| --- | --- |
| Q01 · 15/15 | PyArrow 21은 스키마가 없는 파일에서 두 열의 64비트 오프셋과 값을 반환했다. 작은 스키마를 저장한 파일은 32비트를 유지했고, 20은 명시 인수를 거부했다. 고정 Java의 원본 시험 두 개가 실행됐다. 원 Binary 시험의 논리행 0을 발견해 판정 범위를 좁혔다. Python의 실제 IPC 및 같은 PID C Data를 각각 확인했고, C Data에서 2,147,487,744 위치의 4바이트 tail을 읽었다. |
| Q02 · 9/9 | 고정 4b7cdcb를 Rust 1.49.0에서 복구 lock으로 빌드했다. 025 원 probe 1개, 추가 array→enum 2개, 공급자 역방향 2개가 통과했다. Boolean, Utf8, List와 유효 null이 같은 accessor에서 보였고 Binary는 NotImplemented다. |
| Q11 · 12/12 | 실제 클라이언트 요청 ID를 do_execute와 reply에 연결했다. 6.26은 root cellId만, 6.27은 root metadata와 cellId를 전달했다. content 전용 및 미복사 파일 sentinel은 cell_meta에 닿지 않았다. V1 기대의 반증과 v2를 보존했다. 6.27.0은 PyPI에서 yanked됐고 6.27.1 보조 6/6도 일치했다. |
| 재생 · 36/36 | 최초 및 빈 작업 폴더 정규화 값이 같다. 양성 11·대조 21·경계 4다. 예상한 거부와 값 부재가 분모에 포함된다. 직접 주 사례 3개와 분야 비교 2개다. |
| 직접 원문 · 41/42 산입 | Arrow 15, DataFusion 7, Jupyter 11, 공간정보 및 디지털 보존 8. 현재 직접 열지 못한 2021 Arrow 메일 4통은 시도 원장에 있다. |
| 수용 · 12/13 | 역사 원문 독립 재독 1조건 미달. 필수 주 실행의 미확인은 0/36이며 승인 범위의 역사 적용·종단 대형 파일·운영 앱은 별도 미확인이다. |

## 1. 식별

- 저장소 laadkke-arch/agentflow-open, 작업 브랜치 work/research-af-res-031, 소유 경로 docs/workstreams/research/AF-RES-031/.
- 작업자 codex-cloud. 실제 환경은 관리형 Debian 13.6 x86-64, 표기 GPT-6 기반 Codex다. 세부 모델 선택값과 추론 등급은 미확인이다. 2026-11-22 07:05 UTC에 시작해 07:48 UTC까지 원문을 재확인했고, 원격 재독/인계 확인 시각은 [UTC 영수증](evidence/handoff-checks/readback-utc.txt)에 있다.
- 시작 및 마지막 계약 확인 통합 SHA 172c6bc37bdf91b91c86b9b3be29cb5b44fa4971, 계약 fingerprint 19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc. [작업 manifest](manifest.json)
- 의존 [AF-RES-025@cf27e148b96bf3c5a3dc8a2a926db4abcf63f146](https://github.com/laadkke-arch/agentflow-open/blob/cf27e148b96bf3c5a3dc8a2a926db4abcf63f146/docs/workstreams/research/AF-RES-025/HANDOFF.md), [AF-RES-028@72a5d7f4fb4489fd183669dea49dc9659d941ca8](https://github.com/laadkke-arch/agentflow-open/blob/72a5d7f4fb4489fd183669dea49dc9659d941ca8/docs/workstreams/research/AF-RES-028/HANDOFF.md). PR 주소는 해당 없음이다.

## 2. 작업 범위와 실제 변경

| 산출물 | 재사용 위치 |
| --- | --- |
| 입력과 명시 조건 | SCOPE.md, contracts.jsonl, probes/inputs.json 및 025 공급 입력 2개. 최초 봉인 847df80713786ad260789c46e5474a6002ddb41c. |
| 직접 원문·획득 검증 | sources.jsonl, artifacts.csv, evidence/locks. 접근 실패는 receipts/source-attempts.jsonl. |
| 실측·품질 대조 | observations.jsonl, comparison.csv, 단계별 receipts, [자체 점검](SELF_CHECK.md). |
| 빈 폴더 재개 | [REPLAY](REPLAY.md), replay.sh, [비용](receipts/costs.csv), [재생 검산](evidence/replay-comparison.json). |
| 커밋·수용 | [진행 원장](PROGRESS.md), [조건별 수용](evidence/acceptance-evidence.json), [원격 파일 해시](evidence/handoff-checks/remote-files-sha256.txt). |

## 3. 검증과 원격 재독

고정 결과에서 RESULT·SELF_CHECK·sources·비교·수용 등 8개 원격 파일 바이트를 대조했다. 같은 고정판의 단독 checkout에서 아래 세 명령은 각각 종료 0이었다. 공통 cloud_check는 소유 경로의 manifest를 자동 발견하지 않아 직접 session check로 확인했다. 상속된 운영표의 diff 0과 소유 경로 밖 변경 0을 확인했다. [셸 영수증](evidence/handoff-checks/)

```sh
p=docs/workstreams/research/AF-RES-031
git fetch origin work/research-af-res-031
git show 5b06d0158868a3cc790da55546504ddf5a46eecc:"$p/RESULT.md"
python -B "$p/verify.py"
python -B -m workbench.session check "$p/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

같은 작업자가 최종 원문과 누락을 재검했다. 별도 독립 판독은 미실시다. 검산은 정규화 SHA-256 686cbc7069788fe6abdbc485d36e32bbcaab0bcd8c073e27df61b041909d628a 및 원 실행 영수증 62건을 확인했다. 이 인계의 커밋 자체는 작업 브랜치의 head와 git log -1로 식별한다.

## 4. 다음 첫 행동과 색인 제안

진행 담당은 먼저 작업 브랜치의 head에서 이 인계를 열고 위 고정 결과의 수용 evidence 12/13과 일치시키면 된다. 공통 색인에는 AF-RES-031, 결과·인계 SHA, 주 재생 36/36, 직접 원문 산입 41, 역사 원문 재독 공백을 싣는다. Q01은 조건부 Python/Java 전달 및 대형 C Data 고주소, Q02는 지원 형과 Binary 오류, Q11은 송신 위치와 실제 수신이 핵심 키워드다.

연구를 재개할 때의 첫 행동은 **공식 Apache Arrow dev archive의 2021-01 최초 Q01/Q02와 Q02 제안·수락 raw Message-ID**를 확보하는 일이다. [접근 시도](receipts/source-attempts.jsonl)의 주소와 025 restore_inputs.py의 두 본문 해시를 입력으로 사용한다. 이 자료가 표현된 선택의 근거를 보강한다. 대형 Parquet/IPC 쪽은 REPLAY의 고정 tail을 공유하되 임시 파일과 payload 할당의 한계를 별도로 기록한다. Jupyter 실제 적용은 목표 frontend·판을 고정한 송수신 요청을 첫 자료로 사용한다.

| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |
| --- | --- | --- | --- |
| 1. Java 원 Binary 시험은 논리 0행이다. 2 GiB 실측은 C Data의 고주소 tail 한 행이다. | [A06 원 시험](https://github.com/apache/arrow-java/blob/7a581880a85358315d05da08296cf570b3643924/c/src/test/java/org/apache/arrow/c/RoundtripTest.java#L149-L171) · [count 대조](receipts/java-holder-control/holder-first.json) | 공급자 시험 통과와 실제 데이터 전달의 범위. 대형 Parquet/IPC 경로 | REPLAY의 C Data 2 GiB 입력에서 Parquet row group·압축을 먼저 고정해 IPC/Java tail 종단을 재검 |
| 2. Q01/Q02 2021 메일의 직접 재확인과 질문자 코드 적용은 미확인이다. | [Message-ID 시도](receipts/source-attempts.jsonl) · [D04 고정 구현](https://github.com/apache/arrow/blob/4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa/rust/datafusion/src/scalar.rs#L245-L289) | 당시 수락의 독립 확인, 검색과 실제 적용의 인과관계 | 025 restore_inputs.py Q01 Q02의 hash와 제안·수락 raw 메시지를 확인할 수 있는 Apache archive 경로로 재독 |
| 3. Jupyter의 기본 metadata 경로는 파일 UI와 다르고, 정확한 최초 추천 배포판은 yanked다. | [J11 PyPI 상태](https://pypi.org/project/ipykernel/6.27.0/) · [J08 JEP PR70](https://github.com/jupyter/enhancement-proposals/pull/70) | 사용자 설치판 권고 및 실제 frontend에서의 metadata 전달과 채택 | 실사용 frontend를 고정하고 6.27.1 또는 배포 목표판에 파일 sentinel을 보내 do_execute까지 ID를 연결 |
