# AF-RES-143 최종 인계

**PARTIAL.** 24개 npm 배포의 공개 진입을 두 독립 설치로 시도했다. 비교 가능한 5,370셀쌍은 모두 불변이었고 326셀쌍은 미확인이다. 수치·예외·인수 변화 양성이 없어 검출률은 산출 불가다. simple-statistics 7.8.6 공개 require가 실제로 실패했고 C는 이 값을 잘못 이월했다. D/E/E2는 해당 진입 실패와 복구 경계를 강제했다. d3-array에서 위임을 한 단계 더 읽은 선택지는 실측 변화 없는 경보 두 함수에서만 E와 달랐다. 빈 캐시 순차 질의의 E는 A보다 적게 설치하고 기다렸고, 두 끝판 질의에서는 A가 덜 취득하고 더 빨랐다. [결과](RESULT.md) · [자체 검산](SELF_CHECK.md) · [비용 원자료](costs.csv)

## 기준과 원격 저장

계획 기준 d950356cdfae3edf799870cdeb90b93b5bd4ffd3, 배정 checkout 24d4766a70c3153dbe1ee4f14f202d1b12c94b25, 직후 fetch d35bf54869a828cd76a74cf3075be094f62e5a59, 실제 시작과 manifest 고정 통합판 c088f5af075c3b010102d002e66c84d9263fe5de다. 로컬 work 참조가 작업 브랜치 경로와 충돌해서 별도 GitHub clone을 사용했다. 유일한 등록 선행은 AF-RES-139의 c06598bada3039eae441a9ba49fd28837108873a이고 중앙 DONE과 고정 인계 PARTIAL을 분리했다. 사용 범위는 docs/workstreams/research/AF-RES-143/다. [시작 명령과 입력](evidence/start.json) · [고정 계약](manifest.json) · [139 인계](https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/HANDOFF.md)

| 묶음 | 원격 SHA 대표 파일 | 확인 |
| --- | --- | --- |
| ① 모집·입력 | [bf899d791ed3 · SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/bf899d791ed37f5afb65058f3dc6a6a982ba0e89/docs/workstreams/research/AF-RES-143/SCOPE.md) | 입력과 비교 규칙 동결. HTTP 200, SHA-256 일치. |
| ② 배포·예측 | [ceaa42a69bbb · predictions.csv](https://github.com/laadkke-arch/agentflow-open/blob/ceaa42a69bbb87b79555bcaafc3767e99558ee8e/docs/workstreams/research/AF-RES-143/predictions.csv) | 첫 공개 함수 실행 전에 원격 재열람. HTTP 200, SHA-256 일치. |
| ③ 두 경로의 출력 | [f28efb4b7d4e · output-pairs.csv](https://github.com/laadkke-arch/agentflow-open/blob/f28efb4b7d4eef14a343029dbfe8d6a4522d8cf0/docs/workstreams/research/AF-RES-143/evidence/output-pairs.csv) | 신호를 읽지 않은 출력 전용 표. HTTP 200, SHA-256 일치. |
| ④ 정책 및 비용 | [6a46b56933d6 · cost-summary.csv](https://github.com/laadkke-arch/agentflow-open/blob/6a46b56933d681192ba6ed91a2c22abe505e52fc/docs/workstreams/research/AF-RES-143/evidence/cost-summary.csv) | 실제 HTTP 본문과 120 배치. HTTP 200, SHA-256 일치. |
| ⑤ 원표·반례·결과 | [b6519bd64941 · RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/b6519bd649411d3485f4a50fb8805d479e181f3b/docs/workstreams/research/AF-RES-143/RESULT.md) | 직접 자료·결측·세 결과 표. HTTP 200, SHA-256 일치. |
| 마지막 인계 | 이 파일의 별도 커밋 | 결과판 검사와 원격 재열람 영수증 포함 |

## 검사와 실제 구조

결과판 b6519bd649411d3485f4a50fb8805d479e181f3b를 깨끗한 checkout에서 검사했다. 별도 캐시 C/D에서 각 24판을 다시 실행했고 두 출력 표와 원 집계가 일치했다. manifest check --fetch, 전체 scripts/check.py, Cloud 공통 검사는 모두 종료 0이다. Git diff 55경로가 소유 범위고 manifest 제외 세션 검사는 54경로를 읽었다. 실측 요청 중 계산된 함수별 경보 1,416개가 봉인과 일치했다. [대상 SHA·입력·명령·종료·stdout/stderr·변경 경로](evidence/acceptance.json)

AF-RES-139의 무결성·정규 출력·공개 로더 절차를 해당 소유 경로에 재사용했다. Acorn 파서 잠금과 호출 위임을 확장했고 npm 공개 파일의 기능 절과 묶음 신호를 온라인 비용 평가에서도 같은 코드로 계산했다. 발표 명부, 정적 예측, 출력 전용 판독, 정책 결합·실측, 교차 분야 자료를 별도 묶음으로 커밋했다. 두 경로의 초기 12초 과정 실패를 보존했고 원 입력을 유지한 250ms 개별 호출 한도로 나머지 셀을 확인했다. 6.1.0/6.1.1은 독립 교정 층이며 옛 30판 스칼라, d3-scale, OpenLayers는 재생하지 않았다. [정적 구성](evidence/static-components.jsonl) · [실행 실패·복구 및 교정](evidence/replay.json) · [실측 구조](replay/README.md)

1,080 배치 질의와 120 실제 캐시 배치에 대해 요청판·근거판·옳음·잘못 이월·보류를 보존했다. 응답 본문 B, 논리로 읽은 B, 캐시 적중, npm 설치, Node와 AST 과정, 벽시계·CPU를 분리했다. 실제 계측은 이 머신과 잠금, 두 질의열에 한정된다. 원전에 대한 하한은 고유 34개로 충족했다. 철도 두 계획 PDF의 새 05:18 열에서 바뀐 Hinton과 유지된 Clapham을 확인했다. ONS 원표 ZIP과 Census ALLDATA 두 본문은 접근 결측이다. Census의 같은 기준일 2023-07-01 변경은 두 원 발행기관의 HTML 발표표에서 확인했고 20개 공통 셀의 불변값은 없었다. [원전 원장](sources.jsonl) · [타 분야 셀](domain-cells.csv) · [접근 실패](evidence/domain-access.json)

색인 제안 — AF-RES-143 · simple-statistics 8판과 d3-array 16판의 판·입력별 이월, 진입 실패 및 실제 캐시 비용 · PARTIAL · 선행 AF-RES-139. [결과](RESULT.md)

## 첫 재개 행동

바이너리 자료 수신이 허용된 실행 환경에서 두 ONS Table 1 ZIP을 각각 직접 열고 SHA-256과 워크북 이름을 고정한다. 이 세션의 Linux HTTPS에서는 두 파일의 CONNECT가 403이고 웹 판독은 ZIP 첨부 타입에서 끊겼다. 새 값이나 시트·셀 주소는 미리 단정하지 않는다.

```sh
scratch=$(mktemp -d /tmp/af143-domain.XXXXXX)
ons='/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/allemployeesashetable1'
for edition in 2023provisional 2023revised; do
  curl -fSsLG 'https://www.ons.gov.uk/file' \
    --data-urlencode "uri=$ons/$edition/ashetable1$edition.zip" \
    -o "$scratch/$edition.zip" || exit
  sha256sum "$scratch/$edition.zip"
  unzip -l "$scratch/$edition.zip"
done
```

두 워크북에서 2023-04-19 기준의 gross annual pay, UK, full-time, both sexes, 1년 이상 근무 조건, median의 £/year와 인접 셀을 맞춘다. XLS는 xlrd, XLSX는 openpyxl의 data_only 모드로 파일명·시트·셀 주소와 숫자를 읽는다. Census 대체 입력은 아래 두 원본 CSV의 STATE=06, POPESTIMATE2022이며 양쪽에 같은 기준일이 있는 열과 인접 셀을 비교한다. 현재 ONS와 Census 원격 응답·결측은 위 원장에 있다.

```sh
for vintage in 2023 2024; do
  curl -fSs "https://www2.census.gov/programs-surveys/popest/datasets/2020-$vintage/state/totals/NST-EST$vintage-ALLDATA.csv" \
    -o "$scratch/NST-EST$vintage-ALLDATA.csv" || exit
  sha256sum "$scratch/NST-EST$vintage-ALLDATA.csv"
done
python - "$scratch" <<'PY'
import csv, sys
from pathlib import Path
for year in (2023, 2024):
    path = Path(sys.argv[1]) / f"NST-EST{year}-ALLDATA.csv"
    with path.open(encoding="latin-1", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["STATE"].zfill(2) == "06":
                print(year, row["STATE"], row["NAME"], row["POPESTIMATE2022"], row["POPESTIMATE2023"])
PY
```

소프트웨어의 출력·점수는 결과판에서 아래 명령으로 다시 읽는다. 비용을 새로 계측할 경우 README의 measure.py를 별도 빈 scratch에서 사용한다.

```sh
task=docs/workstreams/research/AF-RES-143
scratch=$(mktemp -d /tmp/af143-replay.XXXXXX)
python -B "$task/replay/run.py" --label A --scratch "$scratch/A" --out "$scratch/A.jsonl"
python -B "$task/replay/run.py" --label B --scratch "$scratch/B" --out "$scratch/B.jsonl"
python -B "$task/replay/compare.py" --first "$scratch/A.jsonl" --second "$scratch/B.jsonl" --out "$scratch/read"
python -B "$task/replay/audit.py" --rebuilt "$scratch/read" --fresh-run "$scratch/A.jsonl" --fresh-run "$scratch/B.jsonl"
python -B -m workbench.session check "$task/manifest.json" --fetch
```

| 가장 중요한 불일치·약점 | 현재 판정에 미치는 영향 | 다음 조사·찾을 자료 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 326셀쌍 미확인 및 고정 계약의 수치 양성 0 | 가용성 오류는 확인됐지만 E/E2의 수치 검출률은 산출 불가다. | 7.8.6 공개 배포의 다른 지원 진입과 다음 창의 보간 후보를 새 가정으로 고정한다. | 배포 동일성을 검증한 새 수치 변화 또는 정상 공개 로더가 나타난다. |
| 밀집과 희소 실측은 캐시·재시도 단가에 의존한다. | 같은 실행 횟수에서도 중간판 취득이 희소 질의 비용을 바꾼다. | 보류 응답 TTL, 지원 입력 부하, 사전 캐시로 별도 3회 실측한다. | 보존 자료를 공유하면 희소 A/E의 실제 시간·바이트 우열이 바뀐다. |
| ONS 원표와 Census 2022 후속 추계 원본을 읽지 못했다. | 공표 숫자와 임시 시각표에서 원표·실운영으로 적용을 넓힐 수 없다. | 두 ONS ZIP과 Census CSV의 일치 원본 주소를 확보한다. | 같은 추계·급여 셀의 원값 및 같은 표의 인접 유지값이 확인된다. |
