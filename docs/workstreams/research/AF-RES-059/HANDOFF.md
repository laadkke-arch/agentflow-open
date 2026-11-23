# AF-RES-059#1 인계

**부분 완료.** 두 생태계의 공개 배포·내장 자료·로컬 실행 검증과 지정 소비자의 공개 증거 사슬을 고정했다. BLS 원표 두 판을 직접 확인했으며 ALFRED JTSJOL 빈티지의 대응 수치 2셀은 미확인이다. 두 소비 후보의 당시 프로세스 출력도 미확인이다.

## 고정 결과

- **결과 SHA `5c975cf275b90cf8d18a6425c6f00c210febacec`.** 필수 표 1 머리는 1행, 자료는 3–43행이다. 표 2 머리는 45행, 자료는 47–59행이다. 마지막 표의 자료는 140–142행이다. [표 1](https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/RESULT.md#L1) · [표 2](https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/RESULT.md#L45) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/evidence/acceptance-evidence.json)
- 작업 브랜치는 `work/research-af-res-059`, 작성자는 Codex Cloud다. 배정·branch 생성 기준은 `86955003c4a77690b303fc1f17883b76a906dcd5`다. 시작 검사가 fetch한 통합판은 `3f4d43b19cd76d56983e6f500eebe7010eb3fa51`이다. 055 의존 인계 `1b86aeb35a2b93ebcd752d903eb66e702748ba66`, 읽은 결과 `f3faf7002c287d103f380c23d04a344e6d40ebc1`을 고정했다. [작업 계약](manifest.json) · [사전 범위](SCOPE.md)
- 고정 결과의 두 파일을 GitHub 연결과 GitHub raw GET으로 다시 열었다. raw HTTP 200 두 건은 별도 checkout의 바이트와 일치했다. `workbench.session check ... --fetch`는 2026-11-23 03:53:56 UTC에 `remote_checked`, exit 0, 허용 경로 밖 변경 0으로 통과했다. 별도 checkout에서 전체 Workbench 검사도 exit 0이었다. 고정 소스 재실행의 본 72/72, 전환 72/72, 통제 87/87이 커밋된 값·멤버 해시와 다시 일치했고 수용 검사 13묶음을 재계산했다. 검토자는 작성자이며 별도 독립 검토는 미실시다. [고정판 확인 영수증](evidence/final-check.json)

| 묶음 | 원격 SHA | Git 커밋 UTC |
| --- | --- | --- |
| ① 발행창·정렬·도시·UTC·소비자·판정 규칙 | `32b755d93fa1eacf55d4a420840e65f2e2ca88e6` | 2026-11-23 03:17:12Z |
| ② 선정판·배포 파일 해시·상류·사전 기대 | `b4390feeec2ac0a2068a22f3657a4999c8ebf111` | 2026-11-23 03:21:40Z |
| ③ 본·역순·통제·소비 기록 | `b472a314813d4e0d3b49a3e89ecfa1e86692d457` | 2026-11-23 03:41:37Z |
| ④ 두 필수 표와 비용·자체 검토 | `5c975cf275b90cf8d18a6425c6f00c210febacec` | 2026-11-23 03:52:56Z |
| 고정판 재열람·검사 영수증 | `63602f3d2fad3bbb9bc2139e3966afc290803408` | 2026-11-23 03:55:13Z |

## 확인한 내용

- PyPI 5판, npm 4판의 공개 전체 자료를 두 번씩 72/72 읽었다. 함께 받은 sdist를 포함한 14/14 파일이 레지스트리 해시와 맞았다. 오프셋·일시·약칭에서 B21을 바꾼 배포는 PyPI 2023.2와 npm 0.5.42였다. 두 파일은 23:00 EET, 양쪽 전후 파일은 다음날 00:00 EEST다. B23와 뉴욕은 그대로다. npm에서 a를 담은 파일은 선택 창과 양끝에서 관측 0이고 b는 받았다. [배포 원장](editions.csv) · [본 실행](runs.jsonl)
- Grafana 9.4.7의 공개 Linux/amd64 이미지 frontend에는 2022e pack이 있다. npm 0.5.38의 내용과 맞았고 추출 자료를 로컬에서 재생했다. pandas 2.0의 대표 wheel은 `tzdata>=2022.1`까지 확인했다. 과거 사용자에게는 설치·asset 주소와 digest, 실제 로드한 멤버, 같은 UTC의 관측 출력이 더 필요하다. [소비 원장](consumer.csv) · [이미지·재생](evidence/grafana-image.json)
- 외부 직접 열람은 계보 기준 32개다. 비용은 24 저장본의 냉·온 재표시와 재계산 96개를 실측했다. 두 낡은 멤버와 두 archive 대체를 거절했다. 실제 소비판의 정답 분모는 보류했다. [출처](sources.jsonl) · [비용](costs.csv) · [검토](SELF_CHECK.md)

## 재개 첫 행동

ALFRED의 공식 JTSJOL 다운로드 페이지에서 2024-03-06과 04-02가 실제 빈티지 날짜인지 확인하고 같은 2024-01 관측 두 열을 받는다. 이번 셸 GET은 CONNECT 403으로 응답 body 0바이트다. 웹 조회에서 계열·도움말과 BLS의 8,863→8,748천 건은 읽었고 해당 CSV는 열리지 않았다. Cloud Chrome은 페이지 요구조건을 읽지 못했다. 같은 계열·관측일·단위와 두 열의 헤더까지 맞출 수 있으면 통계 수용값 0/2를 갱신한다. [원 발행과 실패](evidence/jolts.json) · [공식 ALFRED 다운로드](https://alfred.stlouisfed.org/series/downloaddata?seid=JTSJOL)

```sh
af059_jolts=$(mktemp -d /tmp/af059-jolts.XXXXXX)
curl -fLsS --max-time 45 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSJOL,JTSJOL&vintage_date=2024-03-06,2024-04-02&cosd=2024-01-01&coed=2024-01-01' \
  -D "$af059_jolts/headers" -o "$af059_jolts/jtsjol.csv"
sha256sum "$af059_jolts/jtsjol.csv"
head -n 2 "$af059_jolts/jtsjol.csv"
```

기대 열은 `observation_date,JTSJOL_20240306,JTSJOL_20240402`, 관측 키는 `2024-01-01`이다. 원 발행일과 비슷한 날짜라는 이유만으로 두 빈티지 값을 채우지 않는다. 확보한 파일은 공식 주소·조회 UTC·헤더·SHA와 함께 비교한다. 다른 사용자 영수증이 발견되면 소스에서 시작해 선언, 잠금, 배포·설치, 로드와 실행을 다시 판정한다. 정확한 배포·이미지 재실행과 검사 명령은 재현 문서에 있다. [재현](reproduce.md)

**색인 제안** `AF-RES-059 | IANA 2023b의 PyPI/npm 도달, B21 두 변경판과 9.4.7 공개 이미지 2022e, 과거 소비자·ALFRED 셀 보류 | docs/workstreams/research/AF-RES-059/RESULT.md | AF-RES-055@1b86aeb3`.
