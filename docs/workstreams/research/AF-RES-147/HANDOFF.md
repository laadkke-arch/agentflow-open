# AF-RES-147 최종 인계

**REVIEW_READY.** Codex Cloud 시도 1에서 외부 고유 1차 저작 28개를 열고 tzdb·CLDR의 32셀을 모두 판독했다. 세 저장안은 정확판과 요청 범위를 지킨 현재 답에서 모두 일치했다. B와 C는 A의 반복 원문 읽기를 줄였다. C는 밀집의 고유 64입력을 대상으로 과거 답 112건과 당시 근거를 재생했다. A와 B는 요청 ID만 주어진 과거 답을 보류했다. URL의 마지막 값을 재사용한 별도 대조는 밀집 현재 96건 중 오승인 40건을 냈다. [결과](RESULT.md) · [자기 검산](SELF_CHECK.md) · [실측 비용](costs.csv)

## 원격 기준과 확인

저장소는 `laadkke-arch/agentflow-open`, 작업 브랜치는 `work/research-af-res-147`이다. 계획 기준 `9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673`, 실제 시작 `97a1e63cb48ff4900984104e1d2a3760f324eb79`. 계획과 실제 시작 사이 3커밋은 진행표 변경이다. 세션 계약은 버전 2를 고정했다. 등록 선행 AF-RES-143은 중앙 DONE, 고정 인계 PARTIAL이다. 해당 CJS 7.8.6 실패와 두 인접 경계는 조사의 교정 자료다. 활동 범위는 `docs/workstreams/research/AF-RES-147/`이다. [범위·기존 노출](SCOPE.md) · [계약](manifest.json) · [고정 선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/HANDOFF.md) · [교정 행](evidence/calibration.json)

| 묶음 | 원격 커밋 및 대표 파일 | 관측 |
| --- | --- | --- |
| ① 범위·판정 규칙 | [12642de7367d · SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/12642de7367d186bf2ef008af53126439363184c/docs/workstreams/research/AF-RES-147/SCOPE.md) | 원자료 값 전에 봉인. 원격 HTTP 200·내용 일치 |
| 보정 01 · 아카이브 | [942576ff4ca1 · corrections.md](https://github.com/laadkke-arch/agentflow-open/blob/942576ff4ca113c1932373bbb5e5a300a58e4fdc/docs/workstreams/research/AF-RES-147/evidence/corrections.md) | 바이너리 경로 터널 403, 공급자의 고정 트리 사용. HTTP 200·내용 일치 |
| ② 모집·기준 입력 | [f0b208c90e14 · selection.json](https://github.com/laadkke-arch/agentflow-open/blob/f0b208c90e14d8c67575c8ea90ee68beb5d5c883/docs/workstreams/research/AF-RES-147/replay/selection.json) | 8판·8키 및 32셀 예정. 출력 판독 전 HTTP 200·내용 일치 |
| ③ 주 관측 | [2ec7477d7f24 · oracle.csv](https://github.com/laadkke-arch/agentflow-open/blob/2ec7477d7f24f331b63fda472eb93571a40ac703/docs/workstreams/research/AF-RES-147/oracle.csv) | 32셀의 원시값·효력값·위치, 준비 입력 지문. HTTP 200·내용 일치 |
| ④ 대조·반증·비용 | [2fc3511490d6 · receipts.json](https://github.com/laadkke-arch/agentflow-open/blob/2fc3511490d63345aa82910dc0585ba99f9efbdb/docs/workstreams/research/AF-RES-147/evidence/receipts.json) | 두 DB, 실패·역순·가림·비용 원장. HTTP 200·내용 일치 |
| 보정 02 · 다른 프로젝트 계수 | [828ca6e6854c · receipts.json](https://github.com/laadkke-arch/agentflow-open/blob/828ca6e6854c3a0cf7464dc11cd59c383a17ce07/docs/workstreams/research/AF-RES-147/evidence/receipts.json) | 판단 저장소와 분리한 출처 귀속 계수와 출처 행 보충. HTTP 200·내용 일치 |
| ⑤ 결과표·자기 검산 | [667e59888343 · SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/667e59888343b49fb5a1228425578db3e0688c0b/docs/workstreams/research/AF-RES-147/SELF_CHECK.md) | Q1–Q7 양방향 반례와 분모. HTTP 200·내용 일치 |
| 보정 03 · 검사 대상 결과판 | [3a6794815cae · RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/3a6794815caedd96f06752e042f11143f664861d/docs/workstreams/research/AF-RES-147/RESULT.md) | 같은 latn 기호의 역할과 별칭 검사의 범위를 명확히 했다. HTTP 200·내용 일치 |
| 새 checkout 검증 | [d8947e670a84 · acceptance.json](https://github.com/laadkke-arch/agentflow-open/blob/d8947e670a8464b45c4c81f65d2167803e723b1d/docs/workstreams/research/AF-RES-147/evidence/acceptance.json) | 정확한 검사판·명령·지문·경로·종료코드. HTTP 200·내용 일치 |
| 최종 인계 | [작업 브랜치 HANDOFF.md](https://github.com/laadkke-arch/agentflow-open/blob/work/research-af-res-147/docs/workstreams/research/AF-RES-147/HANDOFF.md) | 이 파일만 담은 마지막 커밋 |

## 검사 결과

결과 SHA `3a6794815caedd96f06752e042f11143f664861d`를 새 GitHub checkout에서 검사했다. 로컬 Linux x86_64, Python 3.12.14, SQLite 3.53.1 환경이다. 2026-11-24 15:22:42 UTC에 검증 영수증을 썼다. 작업 계약은 최신 통합 `2825d51d3e7ed28a966f6f161022c7383adbf2e6`을 fetch했고, manifest를 뺀 28개 경로와 고정 선행을 확인했다. 별도 공통 검사와 Cloud 검사는 모두 종료 0이다. 공통 검사의 `check-all`에는 기본 경로의 활성 세션이 없었고, AF-RES-147의 manifest는 지정 경로에서 직접 검사했다. 공통 55개, 기존 lab 7·9개, demo, export, Git bundle 복원, 연구 출처 연동과 원본 smoke가 포함됐다. [검사 로그·범위](evidence/acceptance.json)

```sh
task=docs/workstreams/research/AF-RES-147
python -B -m workbench.session start af-res-147 --allow "$task/" --dependency work/research-af-res-143=61823fd1c98b52d44833bdada4c89708133b528a --output "$task/manifest.json" --fetch
python -B -m workbench.session check "$task/manifest.json" --fetch
python -B scripts/check.py --require-git
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

첫 명령은 시작판에서 manifest를 만들 때 실행했다. 나머지 세 검사와 [재생 절차](replay/README.md)는 위 결과판에서 실행했다. 새 checkout에서 8개 아카이브를 다시 받아 213,933,449 HTTP 본문 B와 원래 SHA-256을 대조했다. 평가자 원장과 보조 판독, 답·가림·전후 원장, 두 빈 DB 영수증의 바이트가 일치했다. 비용의 ms 열을 제거한 나머지도 일치했다. 평가자 파일을 복사하지 않은 경로에서 조회 실행만 수행해 종료 0을 확인했다. 사건열 SHA-256은 `1a5492de92edf1806c8bb90ab9fe64995c5df38379db6002f8a644635bb0abe9`, 정답 CSV는 `28d6b386c3eb9d337ad35bd2ff57cd4260fb93291d167fd94ad18672b32f16d9`다. 두 빈 DB의 경과 제외 원시 지문은 모두 `7d38b0646127063aaf39e19173fcd83c0fe854f944b2136d298d147873a31d62`다. [원자료 지문](evidence/artifacts.json) · [실험 판정 범위](evidence/receipts.json) · [새 검사](evidence/acceptance.json)

## 다음 첫 행동

수용 검토에서 RESULT의 2023b 과거 거절 복원과 구성 S-ALT-B의 현재 역할 오승인을 각각 [답 원장](answers.csv)과 [가림 원장](ablation.csv)에서 다시 찾는다. 이 두 요구가 실제 제품 질문에 함께 있는지를 확인하는 것이 설계 선택의 첫 단계다. 정확판 현재값 조회 중심이면 B가 기준 후보이고, 실제 전달값과 근거 복원이 필요하면 C의 추가 비용과 맞바꿀 범위가 드러난다. 색인 제안은 ‘AF-RES-147 · 동일 공개 URL의 판·입력·보류 분리 및 과거 전달 재생 · REVIEW_READY · 선행 AF-RES-143’이다. [결과판](RESULT.md)

공급자 배포 경로의 바이트 대응이 필요하면 해당 호스트가 열리는 실행 위치에서 다음 입력을 받는다. IANA는 고정 발표 메일의 SHA-512와 대조하고 같은 멤버의 규칙을 확인한다. Unicode ZIP은 지정 XML 멤버의 SHA-256과 상속 계단을 대조한다. 두 유지보수판은 정식 Git 태그가 배포 주소다. 정확한 다음 재생 명령은 README에 있다. [공식 입력과 고정 커밋](editions.csv) · [재현 명령](replay/README.md)

```sh
scratch=$(mktemp -d /tmp/af147-official.XXXXXX)
for edition in 2023a 2023b 2023c 2023d; do
  for kind in tzdata tzcode; do
    leaf="$kind$edition.tar.gz"
    curl -fsSL "https://data.iana.org/time-zones/releases/$leaf" -o "$scratch/$leaf" || exit
    sha512sum "$scratch/$leaf"
  done
done
for edition in 43 44; do
  curl -fsSL "https://www.unicode.org/Public/cldr/$edition/core.zip" -o "$scratch/cldr-$edition.zip" || exit
  unzip -p "$scratch/cldr-$edition.zip" common/main/en_ZA.xml | sha256sum
done
```

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 공식 tar·ZIP은 실행 환경에서 터널 403. 공급자가 고정한 Git 트리의 대응 원본 사용 | 32셀과 파생 TZif는 검사했다. 바이너리 포장, 서명·첫 파일 공개 순간은 미확인 | 위 공식 아카이브 입력과 발표별 SHA-512, ZIP XML 경로를 확인 | 동일한 판 번호의 패키지가 다른 규칙·키·상속 경로 또는 효과 값을 가짐 |
| 미열람 12 인접 셀에서 효력 값 변화 0. 캐시 키 충돌과 단절은 구성 사례 | 필드 손실의 기전은 확인했다. 무공지 검출률과 실제 장애율은 산출 불가 | 새로운 발표 창에서 공지 없이 변하는 셀과 공급자 재발행을 같은 절차로 확인 | 다른 데이터의 공지 없는 변경 또는 새 판이 옛 답·타 프로젝트에 미치는 영향 확인 |
| 로컬 재생, 제공된 발표 피드와 3틱 TTL 및 고정 SQLite | 최소 사례와 실측 앱 비용은 확인했다. 런타임 외부 송수신·사람 비용·현업 대기 분포는 미측정 | 같은 사건열을 실제 HTTP·재검증·실패 회복 trace와 함께 재계측 | 현재값 우선의 B와 감사·복원용 C의 대가 또는 retry와 TTL의 순서가 달라짐 |
