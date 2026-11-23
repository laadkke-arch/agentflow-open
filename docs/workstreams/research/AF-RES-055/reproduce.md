# AF-RES-055 재실행

저장소 루트에서 실행한다. 본판의 고정 입력은 [inputs.json](inputs.json), 후보와 발행판은 [editions.csv](editions.csv), 요구 순서는 [expectations.csv](expectations.csv)다. 원 ZIP이나 tar는 Git에 커밋하지 않는다.

## 원 배포물 확보

타임존 배포 주소에 접근 가능한 셸에서는 아래 명령을 쓴다. 각 판은 전송 경로에 관계없이 `replay.py`에서 바이트 수와 SHA-256 및 IANA 공지 SHA-512를 검증한다.

```sh
af055_cache=/tmp/af055-replay-cache
mkdir -p "$af055_cache"
for af055_tag in 2023a 2023b 2023c 2024a 2024b; do
  curl -fLsS --max-time 60 \
    "https://data.iana.org/time-zones/releases/tzdata${af055_tag}.tar.gz" \
    -o "$af055_cache/tzdata${af055_tag}.tar.gz"
done
sha256sum "$af055_cache"/*.tar.gz
sha512sum "$af055_cache"/*.tar.gz
```

실행 환경에서는 IANA 네 판의 원 주소 GET이 CONNECT 403이었다. 실제 사용한 `2024a`와 대조 `2023c`는 Ubuntu 원본 재배포 주소에서 받았다. 나머지는 발행 공지가 명시한 Git 태그에서 재구성했다. 아래 GNU/Linux 명령은 기록된 태그·tar·데이터 조합을 새 디렉터리에서 다시 만든다. Debian 패키지는 임시 디렉터리에서 파일만 푼다. 실제 실행의 cwd, 버전, 종료 코드, 출력 해시 및 불일치했던 tar 1.35 후보는 [준비 영수증](evidence/preparation.json)에 있다.

```sh
set -e
af055_root=$(mktemp -d /tmp/af055-inputs.XXXXXX)
af055_cache="$af055_root/cache"
mkdir -p "$af055_cache"
git clone --no-checkout --single-branch --branch 2023b \
  https://github.com/eggert/tz.git "$af055_root/tz"
git -C "$af055_root/tz" fetch --no-tags origin \
  refs/tags/2024a:refs/tags/2024a refs/tags/2024b:refs/tags/2024b \
  refs/tags/2023c:refs/tags/2023c
curl -fLsS --max-time 30 \
  'https://deb.debian.org/debian/pool/main/t/tar/tar_1.34+dfsg-1.2+deb12u1_amd64.deb' \
  -o "$af055_root/tar.deb"
printf '%s  %s\n' '24fb92e98c2969171f81a8b589263d705f6b1670f95d121cd74c810d4605acc3' \
  "$af055_root/tar.deb" | sha256sum -c -
dpkg-deb -x "$af055_root/tar.deb" "$af055_root/legacy"
af055_legacy=$(dirname "$(find "$af055_root/legacy" -type f -name tar -perm -100 -print -quit)")
for af055_tag in 2023a 2023b 2023c 2024a 2024b; do
  git -C "$af055_root/tz" worktree add --detach "$af055_root/$af055_tag" "$af055_tag"
  (
    cd "$af055_root/$af055_tag"
    umask 022
    cp /dev/null zic.8.txt
    af055_tar_path="$af055_legacy:$PATH"
    if test "$af055_tag" = 2024b; then af055_tar_path="$PATH"; fi
    PATH="$af055_tar_path" LC_ALL=C TZ=UTC0 make MANTXTS=zic.8.txt \
      VERSION="$af055_tag" "tzdata$af055_tag.tar.gz"
    cp "tzdata$af055_tag.tar.gz" "$af055_cache/"
  )
done
sha512sum "$af055_cache"/*.tar.gz
```

실측은 GNU tar 1.34(2023a/b/c, 2024a)와 1.35(2024b), gzip 1.13, Bash와 GNU make를 사용했다. `MANTXTS=zic.8.txt` 빈 임시 파일은 데이터 tar에 들어가지 않는다. 첫 1.35 후보의 압축을 풀면 2023c·2024a의 멤버 내용과 시간은 같았지만 512 B 헤더의 비장치 major/minor 표현이 달라 tar 자체의 해시가 달랐다. 실제 채택물은 5개 모두 발행자 해시에 일치한다. 별도 서명 신뢰 사슬 검사는 미실시다.

## 본판과 비용 실험

다음 실행에서 `af055_cache`는 위에서 얻은 배포물을 담은 폴더다. 실제 첫 경로·두 번째 경로·명령별 stdout은 [실행 영수증](evidence/receipts.json)에 있다. 같은 절차에 새 빈 스크래치와 역순 컴파일을 사용했다.

```sh
af055_task=docs/workstreams/research/AF-RES-055
af055_out=$(mktemp -d /tmp/af055-runs.XXXXXX)
mkdir "$af055_out/cache-repeat"
cp "$af055_cache"/tzdata*.tar.gz "$af055_out/cache-repeat/"
python -B "$af055_task/replay.py" run --cache "$af055_cache" --output "$af055_out/first"
python -B "$af055_task/replay.py" run --cache "$af055_out/cache-repeat" \
  --output "$af055_out/repeat" --reverse-order
python -B "$af055_task/replay.py" package --first "$af055_out/first" \
  --second "$af055_out/repeat" --output "$af055_out/report"
python -B "$af055_task/measure_views.py" --base "$af055_out/first" \
  --cache "$af055_cache" --scratch "$af055_out/views" --output "$af055_out/report"
```

도구는 Python 3.12.14, SQLite와 Debian glibc 2.41의 `zic`·`zdump`, `strace`다. 정확한 버전과 바이너리 SHA-256은 영수증의 tools 필드를 따른다. 시계 입력은 UTC POSIX 초다. 각 아카이브의 멤버를 확인한 뒤 판별 디렉터리에서 `zic -b slim`을 실행하고, 각 UTC를 `zdump -i -t 초,초+1 절대경로` 및 `ZoneInfo.from_file`+UTC→현지로 검산한다. zdump에서 열린 TZif는 strace로 검사한다. 프로그램은 한 초 창 안에 전환이 있는 경우 보류하도록 실패한다. 재실행의 절대경로와 trace 해시는 달라도 읽은 Zone·소스 행·TZif 해시·값은 일치해야 한다.

`measure_views.py`는 냉 캐시의 동일 셸 HTTP 경로와 온 캐시의 기확보 자료를 따로 기록한다. 각 보기마다 새 폴더이며 동일 요청 URL 중복은 제거된다. 조회 값은 GLIBC+Python 둘로 얻는다. 원격 GET을 다시 실행하면 환경 정책과 실행 시간에 따라 비용과 복원율이 달라지므로 냉/온의 실제 측정 기록을 비교 대상으로 보존한다. `views.csv`의 보관 바이트는 [기록 원장](evidence/view-records.jsonl)의 compact UTF-8 객체 바이트다.

## 교통 재개

실측 대체는 원 발행계보와 공통 효력일 기준을 만족하는 두 판을 필요로 한다. 최초 두 후보와 공지 주변 두 주소의 직접 GET 결과는 [확보 원장](evidence/acquisition.json)에 있다. 그대로 재시도할 명령 및 빠진 입력은 [인계](HANDOFF.md)에서 찾는다.

동일 노선·방향·서비스일이 봉인되면 각 ZIP의 해시와 발행자 출처를 기록한 뒤 아래 명령을 두 번 실행한다. `route`는 확정한 문자열 ID이고 `direction`은 0, 1 또는 `missing`이다. 코드가 두 판의 발행계보·연속성·route 개명을 자동 증명하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-055/replay.py gtfs \
  /tmp/af055-transit/old.zip YYYY-MM-DD ROUTE_ID DIRECTION
python -B docs/workstreams/research/AF-RES-055/replay.py gtfs \
  /tmp/af055-transit/next.zip YYYY-MM-DD ROUTE_ID DIRECTION
```

GTFS 통제는 판독 코드로 별도 생성한 `gtfs-controls/old.zip`과 `new.zip`이다. 원표 추적은 `2024-01-08/R/0`의 `calendar.txt` 2–3행, `calendar_dates.txt` 2–3행, `trips.txt` 2·3·5행과 `stop_times.txt` 2–5·8–9행이다. `late`의 25:10은 서비스일 1월 8일의 연장이며 America/New_York 민간 달력으로는 1월 9일 새벽이다. 파일 해시와 두 판독은 [반례 원장](evidence/contrasts.json)에 있다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-055/manifest.json --fetch
```
