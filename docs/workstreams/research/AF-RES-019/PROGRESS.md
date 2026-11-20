# AF-RES-019 진행

## 1. 기준과 사전 접근 확인

GitHub에서 chore/workspace-foundation 최신 SHA `ded7f3838fe16f1cf401789e99e957b1ebebff1b`를 고정했다. AF-RES-009와 AF-RES-015의 두 HANDOFF는 진행표의 result_commit에서 열었다. 기준 문서와 연구 운영/제품 범위를 읽었다.

| 호스트 | 경로 | HTTP 응답 순서 | 결과 |
| --- | --- | --- | --- |
| github.com | anonymous git clone | 200, 200, 200, 200 | 접근 |
| gitlab.com | anonymous git clone | 200, 200, 200, 200 | 접근 |
| codeberg.org | anonymous git clone | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| pypi.org | anonymous HTTPS GET | 200, 200 | 접근 |
| registry.npmjs.org | anonymous HTTPS GET | 200, 200 | 접근 |
| crates.io | anonymous HTTPS GET | 200, 200 | 접근 |
| rubygems.org | anonymous HTTPS GET | 200, 200 | 접근 |
| redis.io | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| git-scm.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| web.archive.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| api.github.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| api.deps.dev | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| archive.softwareheritage.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| raw.githubusercontent.com | anonymous HTTPS GET | 200, 200 | 접근 |
| github.blog | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.github.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.npmjs.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.pypi.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |

첫 원격 묶음 이후의 다음 행동은 사건 출처 직접 읽기와 후보 검증이다. 정확한 URL·요청·시각은 VERIFICATION.json에 있다.

## 2. 재검증과 정정

초기 부분 clone이 기본 브랜치 밖 Redis 릴리스 태그를 누락했다. 최초 결과의 Redis T−1개월 마지막 태그 이후 값은 4,847일이었다. 원격 태그 전체를 별도 fetch하는 경로로 바꿨고 원장·경보·주기·비용을 다시 계산했다. 최초 수치는 이력에 남겨 정정 범위를 추적할 수 있다. 임계값이나 사건·대조 표본은 이 수정에서 바꾸지 않았다.

추가 반례 확인에서 npm 다운로드 호스트 api.npmjs.org의 익명 GET 1회가 CONNECT 403이었다. 역사적인 deprecated 상태와 다운스트림 사용량을 별도 자료로 구별했다. 우회 호출은 하지 않았다.

## 3. 재개와 고정 원장 재생

분석과 비용 요약은 호스트를 재수집하지 않고 재생할 수 있다. 결과 커밋의 저장소 루트에서 실행한다. 비용 입력은 결과의 cost-receipts.json 중 pages와 full_clones, collection-receipts.json이다. 바이트 일치와 공통 검사 SHA는 VERIFICATION.json에 있다.

```sh
p=docs/workstreams/research/AF-RES-019
python -B -m venv --without-pip /tmp/af-res-019-replay-venv
/tmp/af-res-019-replay-venv/bin/python -B "$p/src/analyze.py" --results /tmp/af-res-019-out
mkdir -p /tmp/af-res-019-replay-bench
python -B - "$p" <<'PY'
from pathlib import Path
import json, shutil, sys
p=Path(sys.argv[1])/"results"
data=json.loads((p/"cost-receipts.json").read_text())
for field,file in (("pages","page-cost.json"),("full_clones","full-cost.json")):
    (Path("/tmp/af-res-019-replay-bench")/file).write_text(json.dumps(data[field]))
shutil.copyfile(p/"collection-receipts.json","/tmp/af-res-019-out/collection-receipts.json")
PY
/tmp/af-res-019-replay-venv/bin/python -B "$p/src/cost.py" --scratch /tmp/af-res-019-replay-bench --results /tmp/af-res-019-out --summarize
python -B "$p/src/verify.py"
```

다음 첫 행동은 CONTROLS.json을 범주, 초기 연도, 작성자 구간, 동시대 지원 근거 결손별로 나누고 최소 33개 추가 엄격 짝을 확보하는 것이다. 운영 Git이 없는 서비스는 날짜 있는 서비스 자료로 별도 비교한다. npm 다섯 사건은 운영자 공지와 동시점 packument의 표기 상태가 필요하다. 다시 얻은 현재 값을 과거 표기로 소급하지 않는다. 각 재개 입력은 RESULT §4와 acceptance-evidence.json에 있다.
