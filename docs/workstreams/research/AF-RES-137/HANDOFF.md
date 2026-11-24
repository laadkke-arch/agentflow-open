# AF-RES-137 인계

**상태 PARTIAL.** 고정 8 PR의 현재 공개 기록, 61개 조작 사건, 37개 고유 원전, Git 객체, 배포 및 두 재현 실험을 저장했다. 원본 HTTP Link와 GraphQL의 중첩 hasNextPage, G7G6 즉시 대체 CSV의 셀, HMRC/VAT 원표의 절대 수치는 미확인이다. 이 결측을 현재 공개 목록의 0건이나 일반 채택률 분모에 넣지 않았다.

**반환할 핵심 증거.** [xarray #9618 타입 제안](https://github.com/pydata/xarray/pull/9618#discussion_r1911138165)에서 [같은 작성자가 정의를 일부 차용했다고 답했고](https://github.com/pydata/xarray/pull/9618#discussion_r1912819641) [첫 변경 eaf3c731](https://github.com/pydata/xarray/commit/eaf3c731cb8b69b329fe677241544a1337290014)과 2025.1.2 배포판에 세 타입의 합집합을 확인했다. 날짜 비교식은 이전과 일치한다. 최초 인지 발언과 같은 공개 실행 기능의 도입이 함께 확인된 사례는 0건이다. #7579는 코드가 실제로 받아들인 **이름** 제안, #7576은 경고 뒤 **다른 유지보수자**가 보존한 반환 계약, #7589는 기존 Poisson 호출에 대한 문서화와 기존 normalize/clip 보존이다.

## 고정판과 검사

- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-137`, 편집 범위 `docs/workstreams/research/AF-RES-137/`.
- 계획 기준 `1d65b0b7aaef85350df8842dfc05a6be69148b38`, 배정 Git branch 기준 `588e642b99e695e710573b9418b60364d7f3880b`. start의 fetch가 읽은 통합판 `b6255317d161b5d1742bdd7cf1b80a2136cdc786`. 그 사이 dot-control.json만 바뀌고 배정·공통 계약이 같았다. [manifest](manifest.json)와 [사전 고정](SCOPE.md).
- 단일 등록 선행 AF-RES-133. 중앙 DONE과 [고정 인계 PARTIAL b84d3a13](https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/HANDOFF.md), [고정 결과 957fffbe](https://github.com/laadkke-arch/agentflow-open/blob/957fffbe6991cef2c5b78f792bd5ea603b1139cd/docs/workstreams/research/AF-RES-133/RESULT.md)를 읽었다.
- [결과판 ae8b00dad97ba242d7f274a539964cc66c1f1070](https://github.com/laadkke-arch/agentflow-open/blob/ae8b00dad97ba242d7f274a539964cc66c1f1070/docs/workstreams/research/AF-RES-137/RESULT.md). 같은 SHA의 새 checkout에서 2026-11-24 13:07:52Z `workbench.session check --fetch` 종료 0, stderr 0 bytes. 검사 시 통합판 `f6c88993e99ea193749f32544e9d1f34ab721044`, changed_paths 34개 전부 owned. [전체 stdout](evidence/workbench-check.json).
- [검사 영수증판 12ddcc9bfd496f68132cc7996e8e4c60830808](https://github.com/laadkke-arch/agentflow-open/blob/12ddcc9bfd496f68132cc7996e8e4c60830808/docs/workstreams/research/AF-RES-137/evidence/final-check.md). [재집계](evidence/reaggregation.json), [독립 실행 대조](evidence/rerun-comparison.json). 원본 예제 난수의 seed 미지정을 뒤집힌 가정으로 기록했고 고정 입력 결과를 별도로 일치시켰다.

| 묶음 | 커밋 SHA | 그 SHA에서 원격 재열람한 대표 파일 |
|---|---|---|
| 번호·판정 사전 고정 | `db16e146f3550d630d9b8eb1ad0bab9d14ad7e78` | [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/db16e146f3550d630d9b8eb1ad0bab9d14ad7e78/docs/workstreams/research/AF-RES-137/SCOPE.md) |
| 전체 회수·페이지 끝 | `005ff87824bebb94c863829161d3808fa38e4edb` | [coverage.csv](https://github.com/laadkke-arch/agentflow-open/blob/005ff87824bebb94c863829161d3808fa38e4edb/docs/workstreams/research/AF-RES-137/coverage.csv) |
| 사건 및 Git 선후 | `a7987af1dd193dfd80450bcedba3891ec82f47e5` | [Hunk 대조](https://github.com/laadkke-arch/agentflow-open/blob/a7987af1dd193dfd80450bcedba3891ec82f47e5/docs/workstreams/research/AF-RES-137/evidence/reading-and-hunks.md) |
| 배포 계약·실행 | `7033f1ddf7f455f2ecb005e5629ba3b15a8e6f79` | [compatibility.csv](https://github.com/laadkke-arch/agentflow-open/blob/7033f1ddf7f455f2ecb005e5629ba3b15a8e6f79/docs/workstreams/research/AF-RES-137/compatibility.csv) |
| 타 분야·반증 | `53835329e305fff5d7fb08730295dc4ac71e16f2` | [corrections.csv](https://github.com/laadkke-arch/agentflow-open/blob/53835329e305fff5d7fb08730295dc4ac71e16f2/docs/workstreams/research/AF-RES-137/corrections.csv) |
| 필수 표·재집계 | `9e8f54af597d8a9bad39394476de11524fd8c2b5` | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/9e8f54af597d8a9bad39394476de11524fd8c2b5/docs/workstreams/research/AF-RES-137/RESULT.md) |
| 같은 묶음의 원래 링크 대조 | `8f6764091ebb8d9d6d71c4a708b8fe0ae65bd6bb` | [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/8f6764091ebb8d9d6d71c4a708b8fe0ae65bd6bb/docs/workstreams/research/AF-RES-137/sources.jsonl) |
| 최종 결과판·갤러리 반복 해석 보정 | `ae8b00dad97ba242d7f274a539964cc66c1f1070` | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ae8b00dad97ba242d7f274a539964cc66c1f1070/docs/workstreams/research/AF-RES-137/RESULT.md) |
| 최종 결과판 검증 기록 | `12ddcc9bfd496f68132cc7996e8e4c60830808` | [검사 영수증](https://github.com/laadkke-arch/agentflow-open/blob/12ddcc9bfd496f68132cc7996e8e4c60830808/docs/workstreams/research/AF-RES-137/evidence/final-check.md) |

## 실제 수행과 남은 작업

- 25/50 두 회수의 ID와 40개 빈 끝 일치. 440개 본문 판독, 311개 인라인 original SHA·blob, 241개 Git 객체. UI edit history 145개 중 30개에서 90개 fragment를 받았다. 현재와 과거 조회 시계·범위를 [증거](evidence/reading-and-hunks.md)에 고정했다. 타입, 문서, 테스트, 다른 actor, 선행 수정의 반증 비교를 [SELF_CHECK.md](SELF_CHECK.md)에 남겼다.
- 실제 파일 구조는 [coverage.csv](coverage.csv)와 [events.jsonl](events.jsonl)의 공개 회수·사건, [releases.csv](releases.csv)와 [compatibility.csv](compatibility.csv)의 배포·실행, [corrections.csv](corrections.csv)와 [sources.jsonl](sources.jsonl)의 분야 비교·원전, `replay/`의 재현 입력과 `evidence/`의 검증 결과다. 저장소의 workbench manifest 기계 계약을 재사용했다. 별도 upstream PR/조작을 작성하는 일은 없었다.
- 실험 네 프로세스 모두 종료 0. SciPy 1.11.2에서 default matrix 보존, array의 `*` 차, `@` 동일, invalid ValueError를 재현했다. 정상과 경계 RL을 원본 0.25.2 공급판 및 0.26.0에서 반복했다. #7575의 옛 CI 링크 404, CP313t wheel은 ABI·해시만 확인. 오래된 SciPy 1.10.1 wheel은 Python 3.12에서 설치 호환 실패. 실제 사람 노동 시간, 공급자의 전체 upstream test 및 여러 플랫폼 빌드 실행은 미실시.
- 클라우드 데스크톱 스킬을 통한 Chromium도 ONS에서 tunnel 오류였다. 웹 공개 페이지는 확인했고 archive CSV/XLSX bytes는 웹 도구가 처리하지 못했다. 즉시 대체판과 VAT 원표는 표시한 발행판과 원어 그대로 후속 판독이 필요하다. [실패 및 입력](evidence/corrections-and-counterexamples.md).

색인 한 줄 제안 · **AF-RES-137 PARTIAL** · 8개 공개 PR의 스레드·Git·배포 대조에서 #9618 타입 링크 차용과 #7579 이름 채택의 범위를 특정. sparse/RL 재현, ONS 즉시판·raw cursor 보류.

## 첫 재개 행동

위 결과판의 원장을 고정한 채 공식 파일을 다운로드할 수 있는 환경에서 `ONS-G7-29-FAIL`의 URL을 열고 `2022 Q2` 행, 날짜, G7G6 표제/단위를 먼저 추출한다. v27·v28·later edition과 비교한 뒤 Appendix M/D와 HMRC 예외 발행의 현금 수입 원자료로 이동한다. 현재 접근 상태에서 실행하지 못한 다운로드의 정확한 입력은 아래와 같다.

```sh
p=docs/workstreams/research/AF-RES-137
python -B - "$p/sources.jsonl" /tmp/af137-ons <<'PY'
import csv, hashlib, io, json, sys
from pathlib import Path
from urllib.request import urlopen

ledger, dest = Path(sys.argv[1]), Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
names = {
    "ONS-G7-27-FAIL": ".csv", "ONS-G7-29-FAIL": ".csv",
    "ONS-VAT-M29-FAIL": ".xlsx", "ONS-VAT-M30-FAIL": ".xlsx",
    "ONS-VAT-D109-FAIL": ".xlsx", "ONS-VAT-D110-FAIL": ".xlsx",
}
for row in map(json.loads, ledger.read_text().splitlines()):
    sid = row["source_id"]
    if sid not in names:
        continue
    with urlopen(row["url"], timeout=30) as response:
        raw = response.read()
    path = dest / (sid + names[sid])
    path.write_bytes(raw)
    print(path, hashlib.sha256(raw).hexdigest())
    if path.suffix == ".csv":
        values = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
        print(values[:8])
        print([cells for cells in values if "2022 Q2" in cells])
PY
```

Appendix XLSX에서는 sheet별 기간과 `VAT`/ `-J5II`가 있는 행을 읽고 19 September 및 21 October 판의 셀 주소와 £m/£bn 단위를 같은 방식으로 남긴다. HMRC는 [발행 목록](https://www.gov.uk/government/statistics/hmrc-tax-and-nics-receipts-for-the-uk#previous-releases)에서 19 September와 8 October 2025의 현금 기준 판을 별도로 확인한다. 두 판 데이터를 확보하면 ONS 발생 기준의 £2.0bn 부분과 직접 합치지 않는다.

공식 GitHub API 헤더를 받을 수 있는 동일 8 PR 환경에서 다음 명령을 실행한다. #9618부터 시작하고 나머지는 SCOPE의 정확한 번호를 쓴다.

```sh
gh api --include 'repos/pydata/xarray/pulls/9618/comments?per_page=25&page=1'
gh api graphql --paginate -f owner=pydata -f repo=xarray -F pr=9618 -f query='
  query($owner:String!, $repo:String!, $pr:Int!, $endCursor:String) {
    repository(owner:$owner, name:$repo) {
      pullRequest(number:$pr) {
        reviewThreads(first:100, after:$endCursor) {
          pageInfo { hasNextPage endCursor }
          nodes {
            id
            comments(first:100) {
              pageInfo { hasNextPage endCursor }
              nodes { databaseId replyTo { databaseId } createdAt updatedAt }
            }
          }
        }
      }
    }
  }'
```

각 thread 결과가 추가 페이지를 가리키면 그 thread ID의 `node(id)`에서 `comments(after:)`를 독립 조회한다. REST header와 해당 페이지의 ID를 저장하고 여기서 관찰한 311개와 비교한다. 이번 `gh api --include` 호출의 Forbidden은 [영수증](evidence/coverage.md)에 있다.

| 중요한 불일치·약점 | 다음 조사·자료 또는 실험 | 결론을 바꿀 관측 |
|---|---|---|
| 두 크기의 공개 sweep은 일치하나 원시 cursor와 미표시 편집은 미확인 | 동일 8 PR에서 REST Link와 GraphQL reply pageInfo, 미표시 옛 발언 | 공개 이전·이후에 빠졌던 적격 링크 또는 직접 최초 인지 답 |
| 링크 차용은 타입에서 관찰했고 런타임 후보는 이름·타인·선행·보존으로 갈림 | 선행 타입 hunk 및 사용자의 실제 시계·영상으로 동일 조건 시험 | 선행 타입 수정 또는 이름/링크에 대한 같은 작성자의 최초 인지와 동일 실행·배포 |
| ONS 첫 대체판과 VAT 인접판의 동일 셀 미확인 | v27/v28/v29 CSV와 Appendix D/M, HMRC 예외 발행 | 첫 적용 버전의 같은 셀과 기간·범위, 제보 단위와 즉시 정정값 연결 |
