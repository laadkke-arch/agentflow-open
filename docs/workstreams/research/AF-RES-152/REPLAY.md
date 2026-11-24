# 실행과 검산

Linux x86_64의 Codex Cloud에서 Python 3.12.14, 표준 라이브러리와 시스템 curl로 실행했다. 재생·검산·저장 대조는 인터넷 연결 없이 실행된다. 현재 HTTP 표본에는 아래 별도 명령이 필요하다.

## 입력과 해시

[config.json](config.json)은 시작·학습 절단·종료, 상한, 조회 단가, 시드, 독립 요청열, 기존 상태를 고정한다. [events.jsonl](events.jsonl)의 `comparison=true`에 재생 입력 39행이 있다. 목록과 신호의 최초 가시 시각은 `first_observable_utc`에 있다. 발행자 표시에 날짜만 있으면 UTC 하루를 사용하고 다음 날 00시를 재생점으로 삼았다. Cloudflare은 최초 production 커밋을 웹 빌드의 하한으로 남겼다. 당시 목록 캡처가 없는 시각은 가정이다.

공급원별 원자료는 [sources.jsonl](sources.jsonl), Cloudflare 날짜·분류 교집합은 [cohort-cloudflare.csv](cohort-cloudflare.csv)에 있다. Cloudflare production 고정 트리에서 `src/content/changelog`의 front matter 날짜, 폴더의 제품 및 추가 제품, hidden 값을 적용했다. 월별 가장 이른 날짜의 원문 주소가 모집 단위다. 표시일이 파일명과 다를 수 있다. 각 원문의 첫 production 추가는 아래 입력으로 다시 찾는다. [분류 소스](https://github.com/cloudflare/cloudflare-docs/blob/857b749ccd051d2a1e771223e7dcf9384ccdd3dc/src/util/changelog.ts)

```sh
git clone --no-checkout --filter=blob:none --shallow-since=2025-05-25 \
  --branch production https://github.com/cloudflare/cloudflare-docs.git /tmp/af152-cloud-docs
git -C /tmp/af152-cloud-docs ls-tree -r 857b749ccd051d2a1e771223e7dcf9384ccdd3dc src/content/changelog
git -C /tmp/af152-cloud-docs log 857b749ccd051d2a1e771223e7dcf9384ccdd3dc --diff-filter=A \
  --format='%H %cI %s' -- src/content/changelog/workers/2025-11-03-wrangler-output-file.mdx
```

[verification.json](verification.json)은 고정 6개 입력의 SHA-256과 출력 SHA-256을 갖고 있다. 학습용 정규 JSON 전용 해시는 [training.json](training.json)의 `training_prefix_sha256`이다. 현재 표본의 각 응답 해시·시각·실패 상태는 [http-sample.csv](http-sample.csv)에 있다.

## 원장 재생과 두 중단 검사

```sh
p=docs/workstreams/research/AF-RES-152
scratch=$(mktemp -d /tmp/af152-check.XXXXXX)
python -B "$p/replay.py" prefix --out "$scratch/train.jsonl"
python -B "$p/replay.py" --events "$scratch/train.jsonl" fit --out "$scratch/training.json"
cmp "$p/training.json" "$scratch/training.json"
python -B "$p/replay.py" run --training "$scratch/training.json" --out "$scratch/base"
python -B "$p/verify.py" --run-dir "$scratch/base" --out "$scratch/verification.json"
cmp "$p/verification.json" "$scratch/verification.json"
cmp "$p/outcomes.csv" "$scratch/base/outcomes.csv"
cmp "$p/metrics.csv" "$scratch/base/metrics.csv"

python -B "$p/replay.py" prefix --before 2026-02-05T00:00:00Z --out "$scratch/masked.jsonl"
python -B "$p/replay.py" --events "$scratch/masked.jsonl" run \
  --until 2026-02-05T00:00:00Z --out "$scratch/masked"
python -B "$p/replay.py" run --until 2026-02-05T00:00:00Z --out "$scratch/full-prefix"
diff -rq "$scratch/masked" "$scratch/full-prefix"

python -B "$p/replay.py" run --until 2025-11-07T18:00:00Z \
  --checkpoint "$scratch/state.json" --out "$scratch/before-stop"
python -B "$p/replay.py" run --resume "$scratch/state.json" --out "$scratch/resumed"
diff -rq "$scratch/base" "$scratch/resumed"

python -B "$p/recovery.py" --out "$scratch/recovery.json"
cmp "$p/recovery.json" "$scratch/recovery.json"
python -B "$p/cost_model.py" --out "$scratch/costs.csv"
cmp "$p/costs.csv" "$scratch/costs.csv"
```

`prefix`는 보이지 않는 채널 시간을 제거하고 cutoff 뒤 사건을 빼낸 파일을 만든다. `fit`은 그 파일만 읽으며 cutoff 뒤 증거가 있으면 중단한다. `run`은 매시간 해당 채널의 제한된 응답을 정책에 준다. 종료 뒤 관측 시각은 기초 사건 원장에만 남긴다. 중단 체크포인트의 입력 지문도 검사한다. 재개본과 연속본에서 CSV 네 개의 바이트를 비교했다. 첫 시도에서 정렬된 JSON이 요청·열람 CSV의 열 순서를 바꿨다. 두 CSV를 값으로 다시 비교하고 저장할 때 그 순서를 보존한 뒤 바이트 대조를 다시 실행했다.

`verify.py`는 재생 구현을 import하지 않는다. 열람 기록으로 주별 세 예산·신규 발견·검열을 복구한다. 원문 상태 전이와 본문 열람 기록에서 기존 대상 시간·낡음·제외·오경보를 재구성하며, 정책별 실제 요청 시각·질의가 같음을 확인한다. [검산 결과](verification.json)

## 민감도 재현

```sh
for scenario in no-sparse big-catalog late-recovery archive-catalog
do
  python -B "$p/replay.py" run --scenario "$scenario" --out "$scratch/$scenario"
done
{
  head -n 1 "$scratch/no-sparse/metrics.csv"
  for scenario in no-sparse big-catalog late-recovery archive-catalog
  do
    tail -n +2 "$scratch/$scenario/metrics.csv"
  done
} > "$scratch/sensitivity.csv"
cmp "$p/sensitivity.csv" "$scratch/sensitivity.csv"
```

희소층 제거는 curl과 그 시드 4개를 빼고 시각과 총량이 같은 요청을 나머지에 배분한다. 비용 변경은 목록 바이트 ×3, 신호·본문 ×2다. 장애 차수는 12월 Cloudflare 회복과 이에 대한 사후 보고에 48시간을 추가한다. 보관 목록 대조는 같은 단가로 끝까지 목록을 볼 수 있다고 가정한다. 모두 구성 민감도이며 원래 이력과 분리한다.

## 실측과 규모 조건

```sh
python -B "$p/measure.py" --out "$scratch/new-http-sample.csv"
python -B "$p/cost_model.py" --sample "$scratch/new-http-sample.csv" --out "$scratch/new-costs.csv"
```

HTTP 9 표본은 URL당 GET 한 번이다. 리다이렉트·응답 바이트·헤더·벽시간을 curl에서 기록한다. 성공 응답은 5회 로컬 규칙 판독과 5개 빈 SQLite에 원문+메타데이터를 1회씩 쓰고 중앙값을 기록했다. 작은 sqlite 파일의 페이지 오버헤드를 항목당 단가로 외삽하지 않는다. 공개 배포 원본의 TLS 터널에서 세 입력이 403 계층으로 막혔다. 본문 0은 공급자 빈 응답을 뜻하지 않는다. Mozilla, Cloudflare의 운영 원래 배포 주소와 curl 원래 출시표는 열린 외부 네트워크에서 위 명령으로 다시 측정할 입력이다. 비용표는 첫 실측을 고정해 재현하며 실시간 재수집의 벽시간·Atom 본문은 달라질 수 있다.

규모 계산의 단위는 N항목당 하루다. 같은 가정에 데이터 본문 M03–M06 중앙값 또는 M02 HTML을 대입한다. 모든 정책은 0.05 요청/항목·일과 두 집중도인 10% 인기층에 수요 85% 또는 35%를 둔다. O는 매번 본문을 연다. P는 1천 건 단위 목록을 매일, 원문은 7일에 한 번 열고 이 재고로 응답한다. S/F는 목록을 3일마다, 하루 변경률 0.5%에서 본문을 확인하며 로컬 요청 TTL은 7일이다. 요청률 `λ`인 층의 원문 재확인 평균은 포아송 도착의 `λ/(1+7λ)`다. F는 희소 10%를 60일에 한 번 더 읽는다. 목록 크기는 M01을 대리값으로 사용했다. 메타데이터 보존량은 표본 중앙값 × N, S/F는 변화 로그를 30일 더 보존하는 가정이다.

전송 상한 2 GiB/일, 작업자 8시간/일, 본문 1%를 사람 30초씩 추가 판독하는 조건이다. 균등 시간대 요청 중 10%가 GitHub REST 미인증 라우트에 집중될 때 시간당 60회와 대조했다. 현재 GitHub HTML, Atom, raw 전송에 이 REST 한도를 적용하지 않는다. Cloudflare Client API 1200/5분도 공개 변경 목록 한도가 아니다. 실제 혼잡·짧은 요청 집중·조건부 HTTP·병렬 처리·공급자별 분산은 외부 계측이 필요하다. [GitHub REST 제한](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) · [Cloudflare API 제한](https://developers.cloudflare.com/fundamentals/api/reference/limits/)

PLOS 두 PDF는 발행자 첨부를 직접 열 때 도구가 500을 반환했다. 아래 공개 주소가 다시 열리는 실행 위치에서 두 PDF의 판별과 바이트를 추가 확인할 수 있다. [발행자 정정](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003612)

```sh
curl -fSL 'https://journals.plos.org/plosbiology/article/file?id=10.1371%2Fjournal.pbio.3003612.s001&type=supplementary' -o "$scratch/plos-original.pdf"
curl -fSL 'https://journals.plos.org/plosbiology/article/file?id=10.1371%2Fjournal.pbio.3003612.s002&type=supplementary' -o "$scratch/plos-republished.pdf"
sha256sum "$scratch/plos-original.pdf" "$scratch/plos-republished.pdf"
```
