# AF-RES-241 로컬 재생

체크아웃한 이 경로에서 실행한다. Linux amd64 Docker, 호스트 Node 및 Chromium/ChromeDriver 156.0.8078.79가 관측 환경이다. Docker의 테스트용 이름과 loopback 포트 14642, 14841, 14842가 비어 있는 별도 환경에서 사용한다. [환경 지문](../environment.json)과 [fixture](../fixtures.md)를 먼저 읽는다. 외부 신원 서비스 대신 upstream RSpec mock을 사용한다.

## 공개 이미지와 데이터

```bash
af241_work=$(mktemp -d /tmp/af241-replay.XXXXXX)
mkdir -p "$af241_work/out"
cp ./*.rb ./relay.mjs "$af241_work/"

af241_apply=ghcr.io/dfe-digital/apply-teacher-training-gems-node-modules@sha256:a644493ed041ee6df343a71836dd88d7826aec5b2636ea3bbe1f9b0243fd603b
af241_register=ghcr.io/dfe-digital/register-trainee-teachers@sha256:dfab3b7cf3c6ad822149ba5464855d3b7cd1bc6c78e7c244f789f416b6f6027a
af241_pg=postgres@sha256:ff87138949ad9a46f32ff23bd6852b52ce024a13dffe9b4087be98292cdd3b4f
af241_redis=redis@sha256:352c1fdadc91926edda08f45aeb3f27f37194c2f14101229c0523a11195c96e3
for af241_image in "$af241_apply" "$af241_register" "$af241_pg" "$af241_redis"; do
  docker pull "$af241_image" || break
done

docker network create --internal af241-research
docker run -d --name af241-pg --network af241-research --network-alias postgres \
  -e POSTGRES_USER=af241 -e POSTGRES_PASSWORD=local-test-only "$af241_pg"
docker run -d --name af241-redis --network af241-research --network-alias redis "$af241_redis"
docker exec af241-pg pg_isready -U af241
docker exec af241-redis redis-cli ping

docker run -d --name af241-app --user root --network af241-research --entrypoint sh \
  -e RAILS_ENV=test -e DB_HOSTNAME=postgres -e DB_PORT=5432 -e DB_USERNAME=af241 \
  -e DB_PASSWORD=local-test-only -e SECRET_KEY_BASE=test-only-af-res-241 \
  -e REDIS_URL=redis://redis:6379/0 -e DEFAULT_FEATURE_FLAG_STATE=off \
  -v "$af241_work:/af241-scratch" "$af241_apply" -c 'sleep infinity'
docker run -d --name af241-reg --user root --network af241-research --entrypoint sh \
  -e RAILS_ENV=test -e DB_HOSTNAME=postgres -e DB_PORT=5432 -e DB_USERNAME=af241 \
  -e DB_PASSWORD=local-test-only -e SECRET_KEY_BASE=test-only-af-res-241 \
  -e REDIS_CACHE_URL=redis://redis:6379 \
  -v "$af241_work:/af241-scratch" "$af241_register" -c 'sleep infinity'

docker exec af241-app bundle exec rails db:prepare
docker exec af241-reg bundle exec rails db:prepare
docker exec af241-app sha256sum Gemfile.lock yarn.lock package.json
docker exec af241-reg sha256sum Gemfile.lock yarn.lock package.json
```

Apply 및 Register 원문은 environment.json의 GitHub URL에서 고정 SHA를 직접 fetch해 대조했다. 위 test image는 원문 34개(Apply)·27개(Register)를 byte-level 해시로 맞췄다. 의존성 및 앱 배포본 전체의 서명 검증 범위는 아니다. 실제 조회한 route 출력의 명령과 결과는 [bootstrap](../receipts/bootstrap/commands.txt)에 있다.

## 로컬 Chromium과 실행

이 환경에는 `/usr/bin/chromium`이 있었다. 같은 x86-64 Debian 드라이버를 작업 폴더 아래에 추출해 사용했다.

```bash
af241_driver_url='https://deb.debian.org/debian-security/pool/updates/main/c/chromium/chromium-driver_156.0.8078.79-1~deb13u1_amd64.deb'
curl -fLsS "$af241_driver_url" -o "$af241_work/chromium-driver.deb"
printf '%s  %s\n' 4230d073eace82559cab94db62f8b61679a23acfb1016e982b992a94351cd22d "$af241_work/chromium-driver.deb" | sha256sum -c -
dpkg-deb -x "$af241_work/chromium-driver.deb" "$af241_work/driver"
"$af241_work/driver/usr/bin/chromedriver" --port=14642 >"$af241_work/chromedriver.stdout" 2>"$af241_work/chromedriver.stderr" &
node "$af241_work/relay.mjs" "unix:$af241_work/webdriver.sock" tcp:14642 &
node "$af241_work/relay.mjs" tcp:14841 "unix:$af241_work/apply.sock" &
node "$af241_work/relay.mjs" tcp:14842 "unix:$af241_work/register.sock" &
docker exec -d af241-app node /af241-scratch/relay.mjs tcp:14642 unix:/af241-scratch/webdriver.sock
docker exec -d af241-app node /af241-scratch/relay.mjs unix:/af241-scratch/apply.sock tcp:14841
docker exec -d af241-reg node /af241-scratch/relay.mjs tcp:14642 unix:/af241-scratch/webdriver.sock
docker exec -d af241-reg node /af241-scratch/relay.mjs unix:/af241-scratch/register.sock tcp:14842
curl -fsS http://127.0.0.1:14642/status

docker exec -e AF241_RAILS_PORT=14841 -e AF241_CAPTURE_DIR=/af241-scratch/out \
  af241-app bundle exec rspec /af241-scratch/apply_spec.rb --format documentation --order defined \
  >"$af241_work/apply.stdout" 2>"$af241_work/apply.stderr"
printf '%s\n' "$?" >"$af241_work/apply.exit"
docker exec -e AF241_RAILS_PORT=14842 -e AF241_CAPTURE_DIR=/af241-scratch/out \
  af241-reg bundle exec rspec /af241-scratch/register_spec.rb --format documentation --order defined \
  >"$af241_work/register.stdout" 2>"$af241_work/register.stderr"
printf '%s\n' "$?" >"$af241_work/register.exit"

docker exec af241-app bundle exec rspec \
  spec/system/candidate_interface/course_selection/candidate_edits_course_choices_spec.rb --format documentation
```

`AF241_ONLY`로 ID 정규식을 주면 독립 초기 상태의 일부만 실행한다. 예를 들어 Apply의 양성·오류는 `-e AF241_ONLY='^A3-1-(POS|ERR)$'`를 docker exec에 추가한다. 테스트가 0 exit로 끝나도 모델 차이, 양식 에러 및 실제 복귀 URL은 JSON에서 별도로 판정한다.

`harness.rb`는 정상 렌더링된 페이지에서 DOM 원문(anchor/control outerHTML, href, input, label, focus 및 summary row)과 Chrome Accessibility.getFullAXTree의 주요 role raw nodes를 보존한다. AX 원본 node는 ordinal과 backendDOMNodeId로 대상 링크의 live DOM과 연결한다. 스냅샷은 필드·관련 role 중심이며 HTML 페이지 전체나 AT 녹음은 포함하지 않는다. 명시적인 Tab/Enter는 링크에만 적용했고 양식 값에는 일반 WebDriver 입력을 사용했다. GOV.UK radio는 연결된 label을 활성화한다. 다른 테스트/프로덕션과 포트 및 데이터베이스를 공유하지 않는다.

## 반례·깨끗한 재생

```bash
docker exec -e AF241_RAILS_PORT=14841 -e AF241_CAPTURE_DIR=/af241-scratch/out \
  -e AF241_ONLY='^C-A[13]-' af241-app \
  bundle exec rspec /af241-scratch/apply_spec.rb --format documentation --order defined
docker exec -e AF241_RAILS_PORT=14842 -e AF241_CAPTURE_DIR=/af241-scratch/out \
  af241-reg bundle exec rspec /af241-scratch/feedback_spec.rb --format documentation --order defined
```

양성·오류 재생에는 위 Apply 컨테이너 명령의 새 이름 `af241-app-clean`과 `-e TEST_ENV_NUMBER=_af241_clean`, `-e REDIS_URL=redis://redis:6379/2`를 적용했다. `bundle exec rails db:prepare`로 만든 독립 DB는 `bat_apply_test_af241_clean`이었다. Apply용 host relay·container relay의 포트와 소켓을 각각 `14843`, `apply-clean.sock`으로 분리하고 같은 host ChromeDriver·새 브라우저 세션을 사용했다. `AF241_RAILS_PORT=14843`과 `AF241_ONLY='^A3-1-(POS|ERR)$'`로 양성·오류 두 예제를 순서대로 실행했다. [두 재생과 대조의 stdout/stderr/exit](../receipts/controls/)

Register의 후속 Course details 양식에서 일부 input name은 렌더마다 달라진다. 첫 단계 실제 이름은 raw receipt에 그대로 남겼고, 시험의 날짜 재입력은 공개 폼의 안정적인 input ID와 UI 입력을 사용했다. 날짜 미입력으로 발생한 첫 검증 영수증은 [초기 시도](../receipts/attempts/R1-1-S.json)에 있다.
