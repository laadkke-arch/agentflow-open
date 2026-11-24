# AF-RES-144 인계

**상태 PARTIAL.** 네 쟁점과 Y4의 예정 실행행을 모두 관측했고, 30개 고유 저작과 두 깨끗한 체크아웃의 재생을 검산했다. 이슈 최초 본문 0/5, 저자 제공 원파일 0/5, 신문 원면의 글자 픽셀·ALTO 좌표 미확보가 남았다. 이 인계는 중앙 과제 상태의 갱신과 별개다.

## 식별과 고정 입력

- AF-RES-144 시도 1, codex-cloud. 저장소 `laadkke-arch/agentflow-open`, 가지 `work/research-af-res-144`, 소유 경로 `docs/workstreams/research/AF-RES-144/`.
- 배정 직후 기존 checkout `24d4766a70c3153dbe1ee4f14f202d1b12c94b25`, 계획 `d950356cdfae3edf799870cdeb90b93b5bd4ffd3`, 실제 시작 `d35bf54869a828cd76a74cf3075be094f62e5a59`. 기존 로컬 `work` ref와 이름 충돌로 별도 clone을 만들었다. 시작 `--fetch`의 통합 SHA는 `c088f5af075c3b010102d002e66c84d9263fe5de`였고 두 기준의 차이는 중앙 진행표 하나였다.
- 통합판 AGENTS, STATE, START_HERE, DOT_AUTOMATION, CLOUD_WORKFLOW, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 AF-RES-144 중앙 행을 읽었다. 유일한 등록 선행 AF-RES-140은 중앙 DONE, 고정 인계 PARTIAL이었다. 여섯 입력의 SHA-256을 따로 고정했다. [140 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/HANDOFF.md) · [140 결과](https://github.com/laadkke-arch/agentflow-open/blob/a43dad1ece967452a996985541773396ea4363a5/docs/workstreams/research/AF-RES-140/RESULT.md) · [입력 지문](evidence/af-res-140-inputs.sha256)

## 단계별 GitHub 저장과 확인

| 묶음 | 원격 SHA | 그 SHA에서 다시 연 대표 경로 |
| --- | --- | --- |
| ① 범위·fixture 등급·판정 | `b9ae34db5eba37eabcbe37eeabc2f9253c9e8ad8` | SCOPE.md |
| ② 공개 시계·판·입력 봉인 | `5cb00ba546cc38c624eff0da1a0b15fb85126397` | timeline.csv |
| ③ CSV 실행·왕복 | `fdb08421ac05d04040bc98b7e998a671d9074007` | evidence/csv-execution.json |
| ④ YAML 실행·독립 판독·Y4 | `519251cb4c19e7ee2e402888790c042eb9e5e235` | evidence/yaml-execution.json |
| ⑤ 타 분야·판정·결과·재집계 | `ad394b702f077bc367b879e4d055fdc76016d0b6` | RESULT.md |
| 결과 커밋의 깨끗한 재생·검사 | `7bbafbf69d8cfb8ab0cd14e8750d544743762422` | evidence/clean-replay.json, GitHub blob `c92ff1aa43366bfeeb535f252eb70bc5c607aed6` |
| 마지막 인계 | 이 파일이 포함된 커밋 | HANDOFF.md |

각 대표 경로를 고정 SHA로 GitHub에서 다시 읽고 그 blob을 로컬 Git과 대조했다. ②의 초기 HTML 봉인과 원시 REST 결측은 그 커밋에 남아 있다. ⑤에서 같은 댓글과 이슈의 REST를 직접 열어 보강했다. 늦게 추가한 상류 식 fixture 1개 외에 ②의 23개 fixture 행은 그대로 유지했다. 모든 원격 변경은 소유 경로 안에 있다. [원격 재확인](evidence/remote-recheck.json)

## 판정과 실제 검증

- **C3**는 공개 샘플에 대체 quote 링크를 줄 수 있다. 탭이 내장된 파일까지 다루려면 수신 quote 방언이 분기를 바꾼다. 저자는 escape 표기를 명시적으로 거절했다. **C4**는 1.0.5에서 유효 날짜 열에 in2csv 기술 절을 줄 수 있다. 불가능한 값 하나를 넣은 대조에서 성공 종료한 두 명령의 통계가 Text로 남았다.
- **Y2**는 .6의 LF×3 오류와 .7 성공에 대해 정확판 수정 링크가 근거를 갖는다. 제3자가 쓴 carriage return 표현과 구성 bytes의 동작이 갈렸고, 명시 null은 .5도 실패했다. 원저자의 소스 빌드 성공은 보고다. **Y3**는 CRLF 코드포인트를 유지할지 LF 블록을 허용할지에 따라 첫 답이 바뀐다. **Y4**의 공개 순서 요청은 concat 원문 하나로 충분했고, 구성 주석·flow 대조에서 루트 대입은 단독 식보다 부모 서식을 더 보존했다. [세 결과표](RESULT.md) · [분기](decisions.csv)
- 116 자료행 중 고유 30저작. 하한은 이슈 5/5, CLI 7/5, 별도 상류 8/6, 계약 2/2, 신문 3/2, 음악 5/2. 21개 댓글 모두 REST 생성·수정 시각, 공개 HTML 앵커 및 현재 SHA-256이 일치했다. 두 댓글의 편집과 C4 제목 변경 3회 확인. 최초 본문 공개 이벤트는 0/5. 140의 질문 후보 4개 중 기술 게이트를 선호로 잘못 본 것은 C4·Y2 2개였고 가상 질문 발송은 0회다. [원장](sources.jsonl) · [시계](timeline.csv) · [원시 REST](evidence/github-rest.json)
- 24개 fixture의 137행을 149개 CLI 호출로 관측했다. 103 성공, 34 실패, 실행 미확인 0. 원저자 버전의 공개 예 재현은 주실험 C3·C4 2/4, 구성/제3자 사례는 Y2·Y3 2/4다. Y4는 비교판 대조 1/1이다. 원저자 제공 파일과 실행 환경 전체의 완전 동일 복원은 0/5다. 구성 결과를 원저자 성공 분모에 넣지 않았다. [입력](fixtures.jsonl) · [실행](runs.jsonl) · [자기 검산](SELF_CHECK.md)
- 결과 SHA `ad394b702f077bc367b879e4d055fdc76016d0b6`를 별도 clone A/B에서 재생했다. 입력 지문·종료·stdout bytes·독립 재해석 137/137 일치. 새 빌드와 기존 빌드의 설치 디렉터리 차이가 en_GB traceback 3행에만 나타났다. C.UTF-8와 en_US.utf8를 각각 비교했다. 초기 bootstrap의 tar 멤버 선택 오류는 정확한 `./yq_linux_amd64`로 수정하고 새 폴더에서 성공했다. [재생과 환경 검증](evidence/clean-replay.json) · [최초 bootstrap 실패](evidence/bootstrap-initial.json)
- 지정 `workbench.session start --fetch` 종료 0. 결과판의 `workbench.session check --fetch`는 2026-11-24 14:10:43 UTC에 종료 0, 상태 passed, 최신 통합 `3303d88b473a9d0c562349ef15e018846573ea9c`, outside_paths 빈 배열이었다. 검사는 Git 계약·범위와 의존 SHA를 대상으로 했다. 제품 테스트 스위트 및 별도 모델의 인계 실험은 미실시다. [시작 영수증](evidence/session-start.json) · [검사 stdout/stderr](evidence/clean-replay.json)
- 작업 구조는 기존 `workbench.session` 계약과 AF-RES-140의 봉인을 재사용했다. `replay/fixtures.py`는 binary 입력 생성·지문을 맡고 `harness.py`는 실행 영수증·파일 변화를 CSV/YAML에서 공용으로 처리한다. 독립 읽기와 사례 판정만 드라이버 두 개에 둔다. 고정 lock, 준비·재집계 명령은 같은 디렉터리에 있다. Git의 실제 경로 검사는 중앙 진행표와 제품 코드가 변경 범위에 들어오지 않았음을 보여 준다. [재생 순서](replay/README.md)

## 첫 재개 행동과 정확한 입력

먼저 원격의 인계 SHA를 다시 읽고, 결과판과 검증판을 확인한다. 공개 열람 경로가 있는 환경에서 아래 시간별 GitHub 이벤트의 `IssuesEvent` 및 `payload.action == "opened"`를 확인한다. 저장소·번호 1194, 1195, 1501, 1506, 1513 및 작성자 일치 후 `payload.issue.body`의 SHA-256을 `timeline.csv`와 대조한다. 지금 환경에서는 해당 시간별 raw archive가 터널 403이었다. 같은 GitHub REST timeline과 events 5쌍에서는 열린 본문 이벤트를 얻지 못했다. C4의 2023-03-19T10:29:12Z rename에서 @ 관련 최초 확인 제목을 얻었으므로 본문 변화와 섞지 않는다. [접근 영수증](evidence/source-access.json)

```sh
af_tmp=$(mktemp -d /tmp/af144-evidence.XXXXXX)
for af_hour in 2023-03-06-15 2023-03-19-10 2023-01-05-14 2023-01-08-15 2023-01-10-18; do
  curl -fsSL "https://data.gharchive.org/$af_hour.json.gz" -o "$af_tmp/$af_hour.json.gz"
  gzip -cd "$af_tmp/$af_hour.json.gz" |
    jq -c 'select(.type=="IssuesEvent" and .payload.action=="opened") | select((.repo.name=="wireservice/csvkit" and (.payload.issue.number==1194 or .payload.issue.number==1195)) or (.repo.name=="mikefarah/yq" and (.payload.issue.number==1501 or .payload.issue.number==1506 or .payload.issue.number==1513))) | {id,created_at,case_number:.payload.issue.number,author:.actor.login,body:.payload.issue.body}'
done
```

신문은 LOC Trek, 1942-12-01 ed-1 image 5의 독립 원면·OCR를 먼저 시도한다. 그 경로의 실패가 지속되면 사전에 고정한 University of Oregon의 대체 면 seq-1을 픽셀과 ALTO로 확인한다. 대체 면에서는 raw OCR L35–36과 PDF p1 텍스트 L21을 이미 읽었다. `morn`/ `ing`, `Oregonlan`/ `Oregonian`, 안정 대조 `PORTLAND`의 위치에 대응하는 페이지 픽셀과 ALTO HPOS/VPOS/WIDTH/HEIGHT를 새로 기록한다. [LOC 원면](https://www.loc.gov/resource/2008257345/1942-12-01/ed-1/?sp=5) · [타 분야 영수증](evidence/domains.md)

```sh
af_page=https://oregonnews.uoregon.edu/lccn/sn83025138/1900-01-01/ed-1/seq-1
curl -fsSL "$af_page.pdf" -o "$af_tmp/oregon-p1.pdf"
curl -fsSL "$af_page/ocr.xml" -o "$af_tmp/oregon-p1.alto.xml"
curl -fsSL "$af_page/ocr.txt" -o "$af_tmp/oregon-p1.ocr.txt"
sha256sum "$af_tmp"/oregon-p1.*
pdftoppm -f 1 -l 1 -r 300 -png "$af_tmp/oregon-p1.pdf" "$af_tmp/oregon-page"
python - "$af_tmp/oregon-p1.alto.xml" <<'PY'
from sys import argv
from xml.etree.ElementTree import parse
for e in parse(argv[1]).iter():
    if e.get("CONTENT", "").strip("-.,").casefold() in {"morn","ing","morning","oregonlan","oregonian","portland"}:
        print(e.attrib)
PY
```

기존 공개 첨부에서 원 CI yaml 또는 저자 `2.yaml`, C3 실제 수신기 방언, C4 원자료를 확보하면 먼저 바이트 지문과 버전·출처 등급을 새 행에 추가한다. 해당 실행을 기존과 동일한 프로브로 비교한다. 140 최초판 0/8, Y1 404, 재실행 전 분모와 현재 PARTIAL 기록을 그대로 보존한다. [CLI 명령과 입력](replay/README.md)

색인 제안 한 줄 — **AF-RES-144 PARTIAL · CSV/yq 네 쟁점과 직접답 대조군에서 버전·바이트·값을 재생한 근거, 링크/수정판/질문 분기, 최초 본문·실물 판면 결측.** [결과](RESULT.md)

| 가장 중요한 불일치·약점 | 현재 판정에 미치는 영향 | 다음 조사·찾을 자료 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 최초 본문 0/5 및 C4 @ 관련 초기 제목 | 21개 후속의 시각은 판독 가능. 저자 요구가 초판에 있었는지는 보류 | GH Archive opened 또는 원 작성의 최초 revision, 현재 SHA와 대조 | 판 사이에 본문이 동일했거나 그때에는 다른 입력/표현 의무였음을 확보 |
| Y2 원 CI와 Y3 원본이 없고 C3/C4 정확 downstream 및 전체 입력 결측 | 정해진 판의 예·대조 실행만 지지하며 원저자 환경 적용·채택은 미확인 | 기존 공개 원파일·다운스트림 방언·RPM 패치 근거를 확인하고 고정 실행기 재생 | .7의 실제 CI 실패, 동일 CRLF literal 왕복, 실제 수신기 열 파손 또는 C4 날짜 열의 다른 월일 |
| LOC 및 대체 원면 픽셀, 대체 면 ALTO 좌표 묶음 결측 | 원시 OCR 검색 비교는 성립하고 인쇄면 원문·배치는 미확정 | Oregon PDF/JP2와 원시 ALTO에 직접 접근해 같은 면의 좌표를 대조 | 원면의 정확 철자와 줄 경계가 실제 OCR의 약점 또는 같은 결과를 확인 |
