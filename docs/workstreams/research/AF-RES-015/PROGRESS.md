# AF-RES-015 재개 입력

결과 표 묶음 마지막 SHA는 `2dc9ccc77006cab4d59af01125858e1859a4b625`다. 다음 묶음에서 Directus와 Fly의 과거 날짜 근거를 재확인하고 검사를 기록했다. 검증 묶음의 SHA는 작업 브랜치에서 `git log -1 --format=%H -- docs/workstreams/research/AF-RES-015/VERIFICATION.json`으로 확인한다. [결과](RESULT.md), [자체 점검](SELF_CHECK.md), [검증](VERIFICATION.json)

## 차단과 첫 행동

관리형 환경에서 web.archive.org, archive.softwareheritage.org, api.github.com, api.deps.dev의 첫 익명 GET이 모두 HTTPS CONNECT 403이었다. 접속이 허용된 실행 환경에서 첫 요청의 헤더를 기록하고 아래의 고정 사례를 하나씩 조회한다. 현재의 제한 환경에서는 이 요청을 반복하거나 다른 통로로 시도하지 않는다. 공개 GitHub REST 기본 한도는 IP당 시간당 60회이며 실제 반영에는 응답의 잔량을 따른다. [접근 기록](results/access.json), [GitHub 한도 문서](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)

### 오프라인 재생

```sh
git clone -b work/research-af-res-015 --single-branch https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch --no-tags origin refs/heads/work/research-af-res-011 refs/heads/work/research-af-res-009
p=docs/workstreams/research/AF-RES-015
export PYTHONDONTWRITEBYTECODE=1
python "$p/src/verify.py" --fetch
```

검증 명령은 11개의 고정 분석 출력을 바이트 단위로 다시 만든다. 새로운 Git 관측은 별도 작업 브랜치에서 `python "$p/src/collect.py" then --resume`과 `python "$p/src/fixed_evidence.py" --resume`에 [Git 규칙](data/github-rules.txt), [답 날짜](data/answer-dates.txt), [고정판 질의](data/fixed-evidence-specs.txt)를 공급한다. 태그가 가리키는 판의 소스와 실제 공개 시간을 각각 확인한다.

### 재개 조회와 입력

조회가 허용된 환경에서 한 호스트당 한 요청으로 시작한다. 403·429에서 멈추고 상태·UTC와 Retry-After를 기록한다. CDX가 돌아오면 실제 사본에 같은 범위의 조건이 있는지 읽고, 당시 상태와 첫 변화 구간의 양 끝을 기록한다.

```sh
candidate_url='https://docs.microsoft.com/en-us/office/developer-program/microsoft-365-developer-program'
curl --fail-with-body --silent --show-error --max-time 25 -D - --get 'https://web.archive.org/cdx/search/cdx' \
  --data-urlencode "url=$candidate_url" --data-urlencode from=2018 --data-urlencode to=2020 \
  --data-urlencode output=json --data-urlencode 'fl=timestamp,original,statuscode,digest' --data-urlencode limit=20
curl --fail-with-body --silent --show-error --max-time 25 -D - 'https://archive.softwareheritage.org/api/1/origin/https://github.com/directus/directus/visits/'
curl --fail-with-body --silent --show-error --max-time 25 -D - 'https://api.github.com/rate_limit'
curl --fail-with-body --silent --show-error --max-time 25 -D - 'https://api.deps.dev/v3/systems/npm/packages/angular/versions/1.8.3'
curl --fail-with-body --silent --show-error --max-time 25 -D - 'https://api.securityscorecards.dev/projects/github.com/lettier/gifcurry'
curl --fail-with-body --silent --show-error --max-time 25 -D - 'https://rdap.verisign.com/com/v1/domain/codepundit.com'
```

| 목적 | 우선 조사 입력 | 남길 값 |
| --- | --- | --- |
| Q3 호스팅·요금 | T013.A001 개발자 샌드박스(2018-10-25), T020.A001 Dcoder 무료 범위(2019-11-10), T011.A002 ChangeDetection(2015-01-19), T014.A001 Resolve Studio(2023-07-19). REASONS.jsonl의 원 URL·현재 공식 URL·답 위치를 사용 | 직전·직후 캡처, 날짜, 당시 약정 원문 위치, 적용 판·요금 새 가입 조건, 바뀐 시행 날짜 |
| Q3 Git 전용 고유 답 | T003.A002 Bitwarden 오프라인 배치, T020.A002 Markor 2.8.0에서 Android 8 SD 지원, T043.A030 Rhino 파일과 엔진 라이선스 구분 | 커밋 SHA·파일, 보존 origin/visit, 버전 출시 날짜, 앱·OS·엔진의 정확한 범위 |
| Q4 선행 원값 및 오경보 | T009.A001 Directus, T020.A001 Dcoder, T051.A001 TanStack, T049.A005 nfnt, T043.A002 Almond에 날짜 있는 경보 이력부터 대조 | 신호 원값, UTC, 원장 id, 같은 범위의 판정과 경보 선행 여부. 독립 사건·대조 표본을 추가 |
| Q4 Scorecard·등록 주체 | Gifcurry Maintained 출력, codepundit.com의 두 시점 공개 등록 근거 | 분석 SHA·점수·일자, 두 시점의 공개 등록 자료. 현재 registrar나 갱신일만으로 소유권 변경을 확정하지 않음 |

### 사람 검토 비용과 공통 검사

같은 12개 벤치에서 `python "$p/src/cost.py"`는 B/C의 자동 요청을 새로 실행해 cost-network.jsonl을 쓴다. 기존 관측은 원래 커밋에 두고 재실행 결과를 별도 브랜치에 기록한다. A의 사람이 각 답과 공식 근거를 대조할 때는 체크 시작·종료 UTC, 본문 페이지, 계측 가능한 HTTP, 판정, 근거 위치를 검토자별로 남긴다. C는 같은 항목에서 경보를 받은 것만 대조한다. [고정 벤치](data/cost-bench.txt), [관측 방법](COST.md)

공통 검사기는 검사 checkout의 .workbench에 출력을 쓴다. owned_path 안의 별도 Git checkout과 그 형제 TMPDIR가 필요하다. 명령은 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`이다. 새로운 모델의 독립 인수인계, 사람의 비용 계측, 현행 앱·가격의 계정 검증은 동일한 Git 검사와 분리해서 기록한다.
