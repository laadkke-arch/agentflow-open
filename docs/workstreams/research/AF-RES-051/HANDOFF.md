# AF-RES-051#1 인계

**상태 REVIEW_READY.** 통계·교통의 통제 실행과 독립 정답, 세 기록 방식의 대조를 검토할 수 있다. 실제 운영 GTFS의 별도 개정판 감도는 미확인이다.

## 식별과 고정 결과

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-051`, 시도 1, 배정 `codex-cloud`. 실제 실행 위치는 클라우드 Linux 셸과 GitHub다.
- 계획 통합판 `d8c8d029bfb6107520ae74d2a172b2b18840e764`, 실제 시작 통합판 **`522ea9092d4d56ef6db0bd4f707bfc90032e179e`**. AF-RES-047 인계 `a6ef2b0bcb6412d9e6fa7a9eb59b5e863c621ff0`와 판정·반례 `235724aa3189712d65c710d2192dd9c703c1f57e`를 확인했다. [시작 manifest](manifest.json) · [시작 stdout](evidence/session-start.json)
- **결과 SHA `4e1a76cd0ca25bfe616797b623f9ecb435261fcb`.** 필수 표 1은 RESULT 1–18행(16개), 필수 표 2는 20–69행(48개)이다. 수용 원장에도 16/48/192 분모가 있다. [필수 표 1](https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/RESULT.md#L1) · [필수 표 2](https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/RESULT.md#L20) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/evidence/acceptance-evidence.json)
- 고정 결과 확인 영수증과 이 인계의 부모 **`9ba0e376838cb9b505cc5d31d912d462cbfc5e11`**. 시작·마지막 check의 실제 UTC와 출력은 영수증에 있다. 이 문서는 별도의 최종 단독 커밋으로 게시한다. [원격 재열람·검사 영수증](evidence/final-check.json)

| 묶음 | 원격 SHA | 핵심 자료 |
| --- | --- | --- |
| 1 사전 규약 | `30f92ecc300b0579b6aa37f2147d14ad180c4355` | 표본 순서·판정 기준·노출, 16개 구조 정답 |
| 1a 통계 경로 보충 | `014115409c2f80ef0c6f8487af6f08e6df859e8f` | 당시 Git tree와 발행자 문서로 CSV 경로 확정 |
| 2 입력·출처·기준선 | `4fdcb35b9134f41a59fef08fd8dabe5d8b875d76` | 두 원본의 해시·입력 목록, 독립 원문 숫자·짝 예측 |
| 3 관측·반례 | `f32675122e776c3991cdfca56af8c2f711f1aa36` | replay, 59 run·32짝·48 구성·192 사실 판정 |
| 4 결과·검토 | `4e1a76cd0ca25bfe616797b623f9ecb435261fcb` | RESULT, SELF_CHECK, 수용 원장, 별도 재실행 |
| 검증 영수증 | `9ba0e376838cb9b505cc5d31d912d462cbfc5e11` | 고정 SHA GitHub 재열람과 검사 실제 출력 |

## 확인한 내용

- 관측 16/16, 짝 변형 32/32, 추가 감도 11/11, 별도 필드 접근 진단 16/16이다. 전체 재실행은 시각을 뺀 run 59/59가 일치했고 파생 원장 5/5는 바이트도 같았다. 직접 열람 기록 42개, 배당에 넣은 고유 1차 저작 26/22, 접근 실패 10개다. [실행](evidence/execution.json) · [재실행](evidence/repeat-check.json) · [출처](sources.jsonl)
- P0 주 규칙 64보류, P1 16일치·48보류, P2 64일치다. P0의 주소 긍정 지름길에서 거짓 양성 28건, P1의 바이트 동일성을 사용으로 확장한 지름길에서 거짓 양성 16건과 거짓 음성 4건이 나왔다. P2에서 로그를 일부 지운 채 범위가 완전하다고 표기한 보조 시험은 거짓 음성 3건을 냈다. [판정 원장](decisions.csv) · [누락 감도](evidence/receipt-sensitivity.json)
- 통계 주 표본은 공식 Eurostat API의 셸 연결 403 이후 NYC DOHMH 고정 CSV를 사용했다. 3월 19일의 3/24판과 3/25판은 원합 1300과 1331, 보고값 1300이 같다. 공식 GTFS 예제의 방향 0과 1은 각각 두 trip ID이고 집합이 다르다. 예제는 같은 ZIP의 두 Git 스냅샷을 확인했다. [판 대조](evidence/contrasts.md)
- 미확인은 실제 운영 GTFS에서 개정으로 바뀐 같은 서비스일의 두 원 배포판, 운영 캐시와 별도 프로세스/네이티브 I/O다. 원 공개 빌드의 개별 파일 read와 PyPI·npm 서명 신뢰 사슬 검증, 외부 독립 인간 판독은 미실시다. T-C4 통제에서 trip_id 한 값만 바꿨으며 전 피드의 stop_times 참조는 해당 변형의 검증 범위 밖이다. [자체 검토](SELF_CHECK.md) · [빌드 영수증 대조](evidence/attestation-check.json)

## 실행·검사

모두 아래와 같은 진입점으로 Linux Python 3.12.14 및 strace 6.13에서 실행했다. 정확한 원래 인자, 판·파일·시간, 종료 코드는 영수증에서 읽을 수 있다. 고정 결과를 GitHub 연결로 읽고 raw GET 바이트를 checkout과 비교했다. RESULT는 16/48/끝 3행, 구조 검산은 총 317개였다. 고정 SHA에서 `check --fetch`와 `scripts/check.py --require-git`는 각각 exit 0이고 범위 밖 경로·충돌·오류 목록은 비어 있었다. [검사 stdout과 UTC](evidence/final-check.json)

```sh
python -B docs/workstreams/research/AF-RES-051/replay.py --cache /tmp/af-res-051-cache --fetch --output /tmp/af-res-051-replay
python -B docs/workstreams/research/AF-RES-051/score.py --runs-dir /tmp/af-res-051-replay --output /tmp/af-res-051-judgments
python -B docs/workstreams/research/AF-RES-051/render_result.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-051/manifest.json --fetch
python -B scripts/check.py --require-git
```

## 다음 첫 행동과 색인

다음 검토에서는 브랜치의 마지막 커밋과 고정 결과 SHA의 첫 두 표를 재열람한다. 실험의 첫 후속 입력은 같은 서비스일을 포함하면서 게시 시각이 보존된 사업자 정적 GTFS 두 원본이다. MBTA의 원목록과 보관정책부터 대조한다. 기존 셸의 첫 MBTA ZIP 요청은 터널 HTTP 403이었고, 앞·뒤 두 ZIP의 원 배포 바이트는 확보하지 못했다. 두 파일 주소가 확인되면 같은 노선·방향·서비스일을 먼저 고정한다. [MBTA 원목록](https://cdn.mbta.com/archive/archived_feeds.txt) · [보관정책](https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs-archive.md)

```sh
curl -fLsS --max-time 30 https://cdn.mbta.com/archive/archived_feeds.txt -o /tmp/af-res-051-mbta-index.csv
# 같은 서비스일을 포함하는 원본 두 판의 실제 archive_url을 각각 지정한다.
curl -fLsS --max-time 30 "$af051_early_url" -o /tmp/af-res-051-early.zip
curl -fLsS --max-time 30 "$af051_late_url" -o /tmp/af-res-051-late.zip
sha256sum /tmp/af-res-051-early.zip /tmp/af-res-051-late.zip
unzip -p /tmp/af-res-051-early.zip feed_info.txt
unzip -p /tmp/af-res-051-late.zip feed_info.txt
```

**색인 제안** `AF-RES-051 | 동일 해시·경로 사용·필드 읽기·보고값 감도의 분리, 통계/GTFS 16주 실행과 192판정 | docs/workstreams/research/AF-RES-051/RESULT.md | AF-RES-047@a6ef2b0b`.

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 계측 대상 또는 수집 범위의 표시가 잘못되면 P2에도 오판이 생긴다 | P2 64/64와 로컬 미사용 근거를 운영 분석에 적용하는 범위 | [T1-1 누락 감도](evidence/receipt-sensitivity.json) · [PROV Usage](https://www.w3.org/TR/prov-dm/#term-Usage) | 캐시·네이티브 로더가 있는 별도 산출에서 외부 추적과 영수증을 대조 | 수집 누락이 검출되면 해당 사용 판정을 보류한다. 독립 추적으로 닫힌 경로만 확인 범위에 둔다 |
| 국소 교란에서 보고값이 같을 수 있으며 T-C4의 단일 ID 교체는 stop_times를 갱신하지 않는다 | 읽기·입력 기여·보고 감도를 더 큰 변형과 전 피드 적합성에 적용하는 범위 | [S4/T4 짝](evidence/pairs.csv) · [X03/X04](evidence/contrasts.md) | 참조를 보존하는 보류 행의 비키 선택값 하나와 각 반올림 경계에서 독립 변형 | 같은 변환의 유효 입력에서 달라지는 결과가 관측되면 그 변형의 R을 바꾼다 |
| GTFS의 2016/2026 저장소판은 같은 예제 ZIP을 재포함한다 | 실제 운영 사업자의 독립 개정판에 대한 감도 | [T-A-EDITION](runs.jsonl) · [MBTA 발행 원목록](https://cdn.mbta.com/archive/archived_feeds.txt) | 같은 서비스일을 포함하며 게시 시각이 보존된 사업자 ZIP 두 개의 원본 확보 | 양쪽 원본과 동일 노선·서비스일·방향을 확인하면 운영 개정판을 별도 결과로 추가한다 |
