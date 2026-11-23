# AF-RES-068 인계

**부분 인계.** 봉인한 12요구·36경로에서 두 사용 조건과 환경의 공동 직접 확인은 요구 0/12, 경로 0/36, 고유 위치 창 0/19였다. 첫 주소가 달라진 A↔C 11쌍에서도 공동 이득·손실은 관측 0이다. B는 환경을 세 건 밝혔고 엄격 표시층에서 그중 A01 한 건을 유지했다. 좁은 C는 L04의 포맷·기본 확장에 조건부 환경 전이 한 건을 보였고, A06의 const 시험에 나타난 동등성 한 조건은 사후 진단으로 남겼다. 최초 설명 10건, VuePress 엄격 표시 네 경로, 실제 작성자 런타임 일치는 미확인이다.

## 고정 결과와 재개 파일

아래 고정 결과는 `9d46186a67d6dc328ad2f66539c8d630ee1d08b5`다.

- [표 1. 12요구·A/B/C의 실제 도착과 문서 판정](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/RESULT.md#표-1-12요구abc의-실제-도착과-문서-판정)
- [표 2. 4개 자리·16입력군의 고정판 실행](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/RESULT.md#표-2-4개-자리16입력군의-고정판-실행)
- [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/acceptance-evidence.json)
- [첫 재개 파일](https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/SELF_CHECK.md#첫-재개-명령)에서 Ajv #1872와 jsonld.js #465의 public edit history 또는 UTC opened 원문을 요청한다. GraphQL 403, edit URL 404, GH Archive와 Wayback 접근 불능을 기록했다. 초기 원문을 확보하면 순번·정규화와 C 첫 도착을 다시 비교한다. [탐색 시도](search-log.jsonl) · [재생 명령](reproduce.md)

저장소는 `laadkke-arch/agentflow-open`, 작업 브랜치는 `work/research-af-res-068`, 역할은 codex-cloud다. 배정 당시 실제 통합 HEAD와 시작은 `374dc309454e8847603c133c4c1d1029d63c0c92`, 계획판은 `028d16fee1121f5862efd410b78ec1d79d7080f2`다. 작업 계약은 AF-RES-064 인계 `c522e0165815b02da25b065b4d781e3aee0fbf25`를 고정했다. [manifest](manifest.json) · [064 인계](https://github.com/laadkke-arch/agentflow-open/blob/c522e0165815b02da25b065b4d781e3aee0fbf25/docs/workstreams/research/AF-RES-064/HANDOFF.md)

## 실제 분모

- GitHub 이슈 60+60을 열어 선택 12·작성자 10·정확 배포 명시 3·범위 하한 2·비교판 7을 기록했다. 생성·갱신 시각 일치층은 2/12다. 타임스탬프를 최초 본문의 직접 보관본으로 치환할 수 없다. 167개 주소·133계보 중 최소량에 23계보를 산입했다. 여기에는 다시 읽은 W3C 규격 한 계보가 있다. [모집](frame.csv) · [출처](sources.jsonl)
- 독립 최초 선정 A 12, B 12, C 11이며 C 한 건은 A의 같은 주소다. 첫 창 36/36, 적격 둘째 행동 관측 0, 토큰 예산 36/36, 표시 엄격 32/36이다. 19 위치 창과 18 내용 해시를 구별했다. 가명 창의 독해와 사후 결합을 한 연구자가 수행했다. [경로](routes.csv) · [노출](evidence/actual-exposure.json)
- 계획 16군을 24 프로세스에서 시도했다. 최종 16/16 stdout, 값 평가 12/16, A02의 컴파일 진단 4/16, 모든 사전 기대와 일치 9/16이다. 정확 명시 배포판 시도는 A02 4군이고 값 평가 0/4다. jsonld.js Node24 로드 실패 8군을 보존하고 같은 lock·입력으로 Node14에서 복구했다. A01 draft-07 선언의 예상과 달리 minContains가 적용됐고, L01 full IRI 키에서는 RDF 객체 유형이 바뀌었으며, L02 untyped 값은 별칭과 값·모양이 갈렸다. [실행](runs.jsonl) · [복구](evidence/runtime-recovery/node-release.json)

## 고정 이력과 검사

| 단계 | GitHub SHA | UTC 2026-11-23 | 고정하거나 정정한 것 |
| --- | --- | --- | --- |
| ① | `daf2e459816f9cf4bc5b57dd265ea1dc3972f978` | 07:25:29 | 모집 순서·조건, 세 길과 판정, 네 실행 자리 |
| ② | `69620448a1b4fffe6934e27f983613da58fe015c` | 07:35:27 | 첫 주소·가명 창·경계 8건, 빈 캐시 두 번. Git HTTPS 인증 실패 동안 동일 tree를 GitHub Git Data로 게시했고 로컬 후속을 그 위에 연결했다. |
| ③ 문서 봉인 | `af581213b0f1a5f734171f0b9f6a3aa6981ee414` | 07:40:01 | 가명 판독·실행 전 조건·16입력의 기대 |
| ③ 실행 | `dd41f04279f50cc083c6a442fef5bb32803a49fb` | 07:43:07 | 초기 배포 실행·로더 실패·raw |
| ③ 호환 재실행 | `5e475133d028f250c86b2660669b538de494a9e8` | 07:45:00 | Node14 공식 binary·원 lock, JSON 복사 전환과 단계 로그, 동일 해시의 8입력 재시도 |
| ④ 결과 | `2303024c0f73fd1cefa46b025ce4ada59ea043be` | 08:02:24 | 두 표, 반례·박물관 기록·검산·수용 계획 |
| ④ 검증판 | `9d46186a67d6dc328ad2f66539c8d630ee1d08b5` | 08:04:45 | 계약과 원격 재열람 영수증, #551 body 없음의 null/empty 표기와 재사용 출처 표시 |

Codex Cloud에서 `python -B -m workbench.session check docs/workstreams/research/AF-RES-068/manifest.json --fetch`를 실행했다. 08:03:08 UTC의 결과판 `2303024c0f73fd1cefa46b025ce4ada59ea043be` 종료 0, passed, remote_checked였다. 08:05:27 UTC의 검증판 `9d46186a67d6dc328ad2f66539c8d630ee1d08b5`도 종료 0, passed, remote_checked였다. 통합 ref는 `3859f0a3967318a02dd5c3ee12c15cc89b82d8bb`였고 검증판에서 84개 변경 경로와 빈 outside/unmerged/errors를 확인했다. 검사 범위는 계약과 Git 소유 범위다. [계약 출력](evidence/verification/session-check.json) · [원장 검산](evidence/verification/audit.json)

2026-11-23 08:05:29 UTC에 GitHub 검증판에서 본문·수용 원장·계약 영수증 bytes를 다시 내려받아 Git 객체와 같음을 확인했다. 렌더된 두 표는 데이터 행 12와 16이었다. 최종 본문 blob은 `08b0fd9a17ec82e7b75a39bab3820939c6cd3948`, 수용 원장 blob은 `238b0d3351ea7de35b664b811b90113927904e6b`다. [비교 영수증](evidence/verification/remote-reread.json)

색인에는 ‘공개 이름/넓은 절/README 첫 창의 12요구 고정 비교, 공동 확인 관측 0, 좁은 이름의 사후 부분 이득, 고정 배포 16군, 부분 인계’로 표시하고 두 표와 선행 064를 연결할 수 있다.

## 가장 중요한 불일치·약점 3건

1. **초기 설명 10/12 미확인.** 선두 #1872와 #465부터 최초 edit revision 또는 열린 이벤트 원문을 회수하고, 원 심볼 위치와 첫 6자리 규칙을 다시 적용한다. [첫 재개 명령](SELF_CHECK.md#첫-재개-명령)
2. **lexical 마스크와 실제 표시, 독립 독해의 결손.** A04의 동명과 A06의 빠진 const를 재현하는 새 가림 입력을 만들고, code-group 투영을 고친 두 창을 초기 기대를 모르는 판정자에게 전달한다. [사후 편차](evidence/postseal.json) · [노출](evidence/actual-exposure.json)
3. **작성자 환경과 고정판 실행의 차이.** 네 실행 자리의 당시 lock·Node·import 또는 Playground 판/모드를 확인한다. 같은 SHA 입력에서 A02의 컴파일과 L01/L02의 객체 유형·별칭·배열 보존이 바뀌는지 먼저 본다. [실행 원장](runs.jsonl) · [재생·실행 명령](reproduce.md)
