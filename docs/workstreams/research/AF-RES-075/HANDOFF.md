# AF-RES-075#1 · 인계

**REVIEW_READY.** Codex Cloud 셸에서 16전후쌍의 주 판정 288자리, SWAP01 보조 18자리, 손실 16자리와 입력 경계 5개를 실행했다. Q1~Q7에 결과·반례·미확인을 연결했다. 독립 원저작은 23건이며 실패한 접근은 산입하지 않았다. 독립 전수 정답 구현과 같은 작성자의 자체 검산을 수행했다. 별도 외부 검토자 참여는 없었다. [결과](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/RESULT.md) · [수용 근거](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/evidence/acceptance-evidence.json)

## 작업과 근거 SHA

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-075`, 소유 경로 `docs/workstreams/research/AF-RES-075/`.
- 계획 통합 `39cadb6ecdf62d0b21c0cce67834f2aef3bf6853`, 작업 시작 통합 `817ee771ebfa63d4a177ee12f46b9818a6335308`. 유일 의존은 `work/research-af-res-071=f8b3fc86b8eb6ba71e02866b48551245b5dbd95f`다. [고정 작업 계약](manifest.json) · [071 인계](https://github.com/laadkke-arch/agentflow-open/blob/f8b3fc86b8eb6ba71e02866b48551245b5dbd95f/docs/workstreams/research/AF-RES-071/HANDOFF.md)
- 모집·규칙 `4bf53c50f45c68bdb0b2f4128ef2f962bdce9576`, 본 판독 코드 `c9f76e04e003d7707a37cabc7600139941ed85dd`, 실측 원장 `191aee9bc05baca5de7c98cb86c8f7da4ac0fbd3`, 검산한 결과 `8a8fe9e36e02b343740a2a8db478bc587e57f544`. 이 인계는 그 결과를 GitHub에서 다시 대조한 뒤 추가한 마지막 단독 커밋이다. [재현 절차](reproduce.md) · [자체 점검](SELF_CHECK.md)

## 가져갈 판단

옛 원본이 소실되면 선택 원절 중심 A는 긍정 존재를 15/16 재계산했고 유일성·공동 1위에는 각각 16/16 보류했다. 전체 판별 키와 스캔 영수증을 둔 B, 전체 목록을 둔 C는 세 주장 모두 각각 16/16이었다. 보존 조건에서는 세 보기가 세 주장을 모두 재계산했고, 동일 현재 경로를 쓴 현재 판정과 옛 문구 표시는 각각 288/288이었다. [점수 원장](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/scores.csv)

모집 수와 대표 원절 지문을 유지한 SWAP01에서도 공동 1위 ID가 교체됐다. LOSS01에서는 옛 스캔 영수증을 유지해 동률 행 누락을 검출했다. LOSS03은 키와 영수증을 함께 바꿔 B의 잘못된 유일성 선언과 짧은 1위 명단을 재현했다. B를 채택하려면 모집 범위와 영수증의 발행 근거를 확인해야 한다. [SWAP01](evidence/swap.jsonl) · [LOSS01–04](evidence/losses.jsonl)

## 실행 증거

| 실행 | 실제 대상과 종료값 |
| --- | --- |
| `python -B -m workbench.session start af-res-075 --allow docs/workstreams/research/AF-RES-075/ --dependency work/research-af-res-071=f8b3fc86b8eb6ba71e02866b48551245b5dbd95f --output docs/workstreams/research/AF-RES-075/manifest.json --fetch` | Codex Cloud checkout 루트, 시작 `817ee77`, 2026-11-23 10:05:15 UTC, 종료 0. 원격 계약 v2와 허용 경로·071 핀을 생성했다. [manifest](manifest.json) |
| `prepare.py` → `run.py` → `audit.py` | 코드 `c9f76e0`, 서로 다른 빈 디렉터리 2개 및 별도 시간 재생에서 종료 0. 정답·판독·판정·비용 및 투영 41개의 바이트가 일치했다. 합성 입력 및 가변 시각·시간을 분리했다. 공식 두 sdist의 네이티브 측정 22행도 종료 0이다. [실행 영수증](evidence/replay-run.json) · [비교 해시](evidence/cross-check.json) |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-075/manifest.json --fetch` | Codex Cloud checkout 루트, 결과 `8a8fe9e`, 2026-11-23 10:52:04 UTC, 종료 0, `remote_checked`. 당시 통합 `710a83b6fc2f987a4be346e217f9eb4e59090f31`의 계약 지문은 시작과 일치했다. 93개 변경 경로, 범위 이탈·오류 각 0. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 같은 깨끗한 `8a8fe9e`에서 10:52:10 UTC 종료 0. 공통 55, lab 7/9, 원본 smoke 및 Git 복원 검사 통과. 공통 활성 큐 결과는 `no_active_sessions`였고, 개별 075 계약은 위 명령에서 직접 실행했다. |
| 결과 SHA의 GitHub 원문 재열람 | 10:52:19 UTC 종료 0. RESULT·수용 근거·실행·점수·비용·출처 및 다른 핵심 파일 총 24개의 GitHub raw 응답을 새 checkout 및 파일 지문과 대조했다. 새 checkout `8a8fe9e`에서 `audit.py --final`과 빈 출력의 prepare/run/audit 재생도 종료 0이었다. |

원격 대조 SHA-256은 RESULT.md `80dcbe5507e55e8ed849a40b7f269a9a43e808d30bdeaa7e171de62bddb2a288`, runs.jsonl `912e5cd124baca2edb90d6b85f23ef6e1503764e97073d89d70dff5ca1f1980f`, 수용 근거 `9af4aa14b1dc123b4829b8ce1737277b2f3df74428db436ae232be2672d0bb7e`다. [실행 원장](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/runs.jsonl) · [비용](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/costs.csv) · [출처](https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/sources.jsonl)

## 남은 확인과 다음 첫 행동

IANA `zone1970.tab` 원문은 버전 주소에서 웹으로 열었다. 셸에서 2024a/2024b 정식 tarball의 CONNECT가 403으로 실패하여 시험 바이트는 유지관리자 태그 아카이브와 태그 커밋 blob을 대조해 고정했다. 원 배포 tarball 바이트·운영 HTTP 비용은 미측정이다. 첫 행동은 IANA에 닿는 셸에서 [재현 절차의 IANA 블록](reproduce.md#별도-네이티브-확인)에 적은 `curl -fSL` 두 URL과 `tar -xOf ... zone1970.tab`을 실행해 `inputs/TZ-2024a/zone1970.tab`, `inputs/TZ-2024b/zone1970.tab`에 `cmp`하는 것이다. 그 뒤 별도 검토자가 LOSS03의 재봉인 영수증을 독립적으로 바인딩하는 조건을 확인할 수 있다. [확인 한계](SELF_CHECK.md) · [취득 기록](evidence/acquisition.json)

색인 제안은 AF-RES-075 · 두 유한 등록부 / 16쌍 / 3주장×3보기×2조건 / 모집 완전성과 동률 · 재현 가능이다.
