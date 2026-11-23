# AF-RES-098 재현·재검산 절차

저장소 최상위에서 실행한다. 이 문서는 결과를 읽고 다시 검산하는 절차이며, 예제 프로그램 실행이나 문서 재빌드는 포함하지 않는다. 실제 검사 대상 SHA·UTC·종료값은 [validation.json](evidence/validation.json)과 마지막 HANDOFF의 기록을 따른다. 아래 명령을 적었다는 사실은 해당 검사를 실행했다는 뜻이 아니다.

## 1. 고정 입력과 사전 봉인

| 용도 | 고정 커밋·파일 | 확인 범위 |
|---|---|---|
| 배정 계획 통합판 | `fcde6becc49120c5be91adf43fb5b4aa42e71d48` | 사용자에게 지정된 계획판 |
| 시작 때 최신 통합판 | `01177554d0fbd33a914ea9c982c348d442d1358d` | `manifest.json`의 base/integration 및 계약 파일 지문 |
| 운영 의존성과 094 인계 | [b09dd21… HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/b09dd21acb2bf9160a5aca5b1075ad6179743e63/docs/workstreams/research/AF-RES-094/HANDOFF.md) | 실제 원격 의존 SHA와 인계 입력 |
| 094 연구 결과 입력 | [082ba3… RESULT](https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/RESULT.md) | 같은 커밋의 `cards.csv`, `evidence/r2-asset-lineage.json`, `evidence/payload-audit.json`도 사용 |
| ① 판·모집·옛 목적 고정 | `c0d31ca194e47fe69bc51dc0ef85d6e346b50774` | `SCOPE.md`, `freeze.json`, `frame.csv`, 각 프로젝트의 모집·선택 기록 |
| ② 새 목록만 본 예측 봉인 | `0df9ea9edbcee995d631eef54b65fd43f73c245f` | `predictions.csv`, `evidence/prediction-seal.json`, 각 프로젝트의 목록 영수증 |
| ③ 실물·본문·발행 계보 | `1c22d31375c334409f859b38fee586b6c2a33b8d` | 본문·PNG·빌드 규칙, 교정·타 분야, 자료 원장 |

094 연구 입력 다섯 파일의 blob을 운영 의존판과 비교한 실제 결과는 [input-contract.json](evidence/input-contract.json)에 있다. 운영 원격 SHA와 연구용 고정 SHA가 다른 이유를 숨기거나 연구 입력을 새 판으로 바꾸지 않는다. 교정 원문은 asciicast 배포 문서 [a79eac83…](https://github.com/r-lib/asciicast/tree/a79eac83fa8ef967ff3d4da9bea1d646291cccb6)와 [92fecbc0…](https://github.com/r-lib/asciicast/tree/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1)이다.

아래는 최초에 사용한 계약 생성 명령이다. 현재 결과판 재검산에서는 기존 봉인 manifest를 유지하고 다음 절의 `check`를 실행한다. 이 `start` 명령을 다시 실행하려면 별도 새 작업 사본에서 계약 생성 효과를 검토해야 한다.

```sh
python -B -m workbench.session start af-res-098 \
  --allow docs/workstreams/research/AF-RES-098/ \
  --dependency work/research-af-res-094=b09dd21acb2bf9160a5aca5b1075ad6179743e63 \
  --output docs/workstreams/research/AF-RES-098/manifest.json --fetch
```

## 2. 결과판의 읽기 전용 검사

HANDOFF에 적힌 **결과판**을 checkout한 깨끗한 작업 사본에서 실행한다. 마지막 인계 전용 커밋의 HEAD와 결과판을 혼동하지 않는다. 각 명령 직전의 `git rev-parse HEAD`, UTC, 명령 종료값을 영수증에 남긴다. 네트워크 영수증을 저장소 안에 먼저 만들면 `--require-clean`의 대상이 달라지므로, 검사가 끝날 때까지 새 `/tmp` 경로를 사용한다.

```sh
git rev-parse HEAD
git status --short
python -B docs/workstreams/research/AF-RES-098/tools/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-098/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`verify.py`의 기본 모드는 출력만 하며 파일을 쓰거나 원격 자료를 열지 않는다. Python 표준 라이브러리와 Git을 사용한다. 검사는 다음을 서로 대조한다.

- ①·② 커밋의 20개 봉인 파일과 현재 파일. CSV의 작업 사본 CRLF와 Git LF 차이만 허용하며, 그 경우 두 SHA와 줄바꿈 차이를 출력한다. 내용 변경은 실패다.
- 1,335개 모집 경로의 프로젝트별 순서·선택, 여섯 고정 목적과 예측, 12자리의 판·참조 해석·P/U/G 값, 원 증거 파일과 바이트 지문.
- 자료 원장의 필수 필드·UTC·URL·중복·실패 제외, 보수적 자료 수와 최소 수, 예측 성패와 확인 가능 분모. 자료 수를 코드에 상수로 넣지 않고 현재 원장으로 계산해 `evidence/counts.json`과 비교한다.
- `fixed_url=null`인 GG 세 개의 변경 가능한 API 목록은 명시된 미확보 상태·한계·조회 URL·UTC·응답 SHA가 모두 있을 때만 허용한다. 불변 URL을 만들어 넣지 않는다.
- RESULT 앞 세 표의 6/12/7행과 끝의 정확히 세 약점 행, SELF_CHECK의 Q1–Q7 각 한 행과 근거 URL.

공통 `cloud_check`가 이 위치의 manifest를 자동 발견하지 않아 개별 검사를 `no_active_sessions` 등으로 건너뛰면 그 사실을 기록한다. 공통 검사의 성공으로 위 명시적 `workbench.session check ... --fetch`를 대체하지 않는다. `--environment codex-cloud`는 검사 옵션이며 실제 로그인 계정이나 실행 환경을 인증하는 증거가 아니다. 구조 검사의 성공도 모든 외부 사실이나 신규 생성 귀속 G를 인증하지 않는다.

## 3. 24개 본문·PNG 재요청과 GitHub 결과판 재열람

다음은 선택적 네트워크 검사다. `AF098_RESULT_SHA`는 앞 절에서 결과판 checkout을 마친 뒤 얻은 실제 40자리 SHA다. 새 임시 디렉터리를 사용하므로 원 영수증을 덮어쓰지 않는다.

```sh
AF098_RESULT_SHA="$(git rev-parse HEAD)"
AF098_AUDIT_DIR="$(mktemp -d /tmp/af-res-098-recheck.XXXXXX)"
python -B docs/workstreams/research/AF-RES-098/tools/verify.py \
  --network --output "$AF098_AUDIT_DIR/network.json"
python -B docs/workstreams/research/AF-RES-098/tools/verify_publication.py \
  --commit "$AF098_RESULT_SHA" \
  --output "$AF098_AUDIT_DIR/github-readback.json"
```

첫 명령은 `lineage.csv`에 있는 12개 본문 URL과 12개 주 PNG URL에서 fragment만 제거해 GET한다. 원 영수증에서 읽은 MIME·길이·SHA를 실제 응답과 비교하고, 요청·완료 UTC·HTTP 상태·리다이렉트 단계·도착 URL을 새 JSON에 남긴다. 리다이렉트가 있다는 이유만으로 실패시키지 않으며 payload 지문이 바뀌면 실패한다. 같은 PNG를 두 판에서 다시 받는 것은 두 주소의 현재 접근성 검사이며 고유 자료 수를 늘리지 않는다. 원 표의 정적 URI 판정과 새 요청의 성공 여부도 구별한다.

PNG 시그니처·치수를 확인하지만 브라우저 DPR이나 JS 실행을 재현하지 않는다. MP의 보조 2x srcset, 모든 부가 다운로드, 전체 외부 자료 원장을 재요청하는 명령도 아니다. HTML 원 바이트가 footer 등 때문에 바뀐 경우에도 exact-byte 검사는 실패하므로, 차이를 조사한 뒤 판정 범위만 갱신하고 원 증거는 보존한다. 공식 ZIP·Corpus 데이터 ZIP은 이 명령으로 내려받지 않는다. 기본 응답 크기 상한은 요청당 16 MiB다.

두 번째 명령은 `--commit`의 40자리 Git 객체를 사용해 GitHub raw의 보고서·원 증거·재현 절차 19개 파일을 다시 열고 `git show`의 blob 바이트와 비교한다. 렌더링 검사나 모든 인용 외부 사이트의 재검증은 아니다. 두 도구 모두 기존 `--output` 파일이 있으면 거부한다.

모든 검사 결과와 종료값을 읽은 다음에만 새 영수증을 owned_path 아래 **새 파일명**으로 복사해 커밋한다. 예를 들어 아래 명령은 대상 파일이 이미 있으면 실패한다.

```sh
python -B - "$AF098_AUDIT_DIR" <<'PY'
from pathlib import Path
import sys
source = Path(sys.argv[1])
target = Path('docs/workstreams/research/AF-RES-098/evidence')
for old, new in [('network.json', 'network-recheck-NEW.json'),
                 ('github-readback.json', 'github-readback-NEW.json')]:
    with (target / new).open('xb') as handle:
        handle.write((source / old).read_bytes())
PY
```

`NEW`는 실제 후속 검사 식별자로 바꾼다. 실패 영수증도 지우지 않고 원인과 영향 범위를 적는다. 검사 뒤 커밋한 영수증의 커밋과 실제 검사 대상 커밋은 같다고 쓰지 않는다.

## 4. Corpus 대용량 파일: 미실시 MD5 검증의 정확한 입력

이 연구에서는 [v1.0 레코드](https://zenodo.org/api/records/11196859)와 [v1.1 레코드](https://zenodo.org/api/records/11216814)의 파일명·길이·선언 체크섬을 읽었다. 아래 두 ZIP, 합계 **3,235,117,257 바이트**, 는 내려받거나 MD5를 재계산하지 않았다. 선언 체크섬은 수신 바이트 검증 결과가 아니다. 이 비용과 미실시는 [cross-domain/audit.json](evidence/cross-domain/audit.json)에 남아 있다.

| 판 | 정확한 파일 content URL | 선언 길이 | 선언 MD5 |
|---|---|---:|---|
| 1.0 | https://zenodo.org/api/records/11196859/files/2024-01-30-data-citation-corpus-v1.0.zip/content | 1,400,187,243 | `7e56ae579f62d432b2fac135d924ac70` |
| 1.1 | https://zenodo.org/api/records/11216814/files/2024-05-10-data-citation-corpus-v1.1.zip/content | 1,834,930,014 | `e2e191e9573a9ee729413df872edd96b` |

아래 명령은 충분한 임시 공간과 전송 여유가 있을 때 후속 확인으로 실행할 입력이다. concept DOI나 최신판 주소로 바꾸지 않는다. 현재 연구에서 실행했다는 뜻이 아니다.

```sh
(
  set -eu
AF098_CORPUS_DIR="$(mktemp -d /tmp/af-res-098-corpus.XXXXXX)"
curl --fail --location --show-error \
  'https://zenodo.org/api/records/11196859/files/2024-01-30-data-citation-corpus-v1.0.zip/content' \
  --output "$AF098_CORPUS_DIR/2024-01-30-data-citation-corpus-v1.0.zip"
curl --fail --location --show-error \
  'https://zenodo.org/api/records/11216814/files/2024-05-10-data-citation-corpus-v1.1.zip/content' \
  --output "$AF098_CORPUS_DIR/2024-05-10-data-citation-corpus-v1.1.zip"
  cd "$AF098_CORPUS_DIR"
  md5sum --check <<'CHECKSUMS'
7e56ae579f62d432b2fac135d924ac70  2024-01-30-data-citation-corpus-v1.0.zip
e2e191e9573a9ee729413df872edd96b  2024-05-10-data-citation-corpus-v1.1.zip
CHECKSUMS
  wc -c 2024-01-30-data-citation-corpus-v1.0.zip 2024-05-10-data-citation-corpus-v1.1.zip
)
```

이 subshell은 `set -eu`로 다운로드나 체크섬 실패를 뒤의 `wc -c` 성공으로 덮지 않고 비정상 종료한다. MD5 일치가 관측되면 해당 파일 수신·체크섬 축만 갱신한다. 두 ZIP의 인용 ID 집합이 같다는 주장은 압축 내부의 실제 스키마·ID 열을 먼저 읽고 별도로 비교해야 한다. MD5가 서로 다르다는 사실만으로 연구 내용의 추가·삭제를 단정하지 않는다. 데이터 프로그램 실행이나 재생성은 요구하지 않는다.

## 5. 재사용하면 안 되는 실행 가정과 남은 첫 확인

`tools/assemble.py`와 프로젝트별 원 수집·보고서 작성 스크립트는 당시 입력·파서·캐시 경로를 보여 주는 증거다. 그대로 재실행하면 봉인 자료, 통합 원장, 후속 검사 기록을 덮어쓸 수 있으므로 이 재검산 절차에서 실행하지 않는다. 검증기는 원 증거의 지문·관계·분모를 읽으며 원 수집과 보고서 작성을 재연하지 않는다. URI 해석·부재 범위의 원 파서와 발췌는 각 `audit.json`, `stage3.md`, 접근 영수증에서 추적한다.

G를 확인하려는 첫 행동은 해당 배포 커밋을 만든 실제 job/manifest를 확보하고 입력 소스·환경·출력 payload SHA의 연결을 읽는 것이다. 기존 Makefile·workflow·copy 규칙은 가능한 절차를 보여 주며 실제 그 실행이 이 바이트를 생성했다는 로그가 아니다. 이름 변경·같은 바이트 반례는 현재 한정 탐색에서 확보하지 못했으므로, 후속 사건을 별도 사전 모집한 뒤 양판 본문·경로·payload를 읽어야 한다. 삭제·접근 실패·정적 참조 없음의 판정을 섞지 않는다.
