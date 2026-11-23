# 미실시 실행과 재개 입력

상태: 아래 도구 동작 재현은 **미실시**다. 이번 과제는 공개 원자료와 고정판의 좁은 절을 읽고 비교했다. 저장소 원장 검사와 작업 계약 검사는 VALIDATION.md의 실제 실행 항목이다. 아래 재현을 성공시켜도 과거 작성자의 새 B 응답이나 질문의 인과효과를 만들어내지는 않는다.

모든 입력·출력은 저장소의 `docs/workstreams/research/AF-RES-070/private/reproduction/` 아래에서만 만든다. 기존 사용자의 데이터·원격 저장소·계정 설정을 쓰지 않는다. `private/`는 산출물 커밋 대상이 아니다. 결과를 인수하려면 명령·바이너리 버전/빌드 소스 SHA·표준출력/오류 해시·종료코드의 공개 요약을 새 커밋으로 남겨야 한다.

## 1. 계약과 원장 검사

환경: 이 저장소와 `workbench.session` 모듈이 있는 Python 환경. cwd는 저장소 루트다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-070/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-070/tools/validate.py
python -B docs/workstreams/research/AF-RES-070/evidence/ledger_independent_audit.py
```

기존 계약을 재시작하지 말고 manifest의 실제 통합판 `76b8c1d15812fbf91b879f8444fd188ae7445802`와 dependency `367f29c6eb8f3da36c7728eb133f1cca9078efbf`를 먼저 대조한다. 새 계약이 필요한 별도 세션에서만 사용자가 제공한 start 명령을 사용한다.

## 2. 최초 본문 재개

원장 `archive_url`, `archive_event_id`, `archive_line`, `original_body_sha256`를 입력으로 쓴다. 예를 들어 jq2349는 현재 repo가 jqlang/jq이지만 opening event의 repo는 stedolan/jq다. 회수할 한 건의 명령 형식은 다음 스크립트의 `--help`로 확인하며, 아래 명령은 실제 helper의 positional 인수 형식이다.

```bash
python -B docs/workstreams/research/AF-RES-070/tools/recover_opened.py \
  stedolan/jq 2349 2021-09-14T16:15:03Z \
  docs/workstreams/research/AF-RES-070/private/reproduction/jq-2349-opening.json
```

복구 후 `payload.issue.body`의 UTF-8 SHA256을 A 원장과 대조한다. 시간순 주 분석에 넣지 못한 ripgrep9–16은 ENROLLMENT의 repo/number/created_utc를 같은 helper에 주어 복구부터 재개한다. 현재 본문과 최초판이 같다고 가정하지 않는다. HTTP403/404가 나면 실패를 기록하고 접근제한을 우회하지 않는다.

## 3. ripgrep 제외 이유의 독립 기전 시험

환경: 12.1.1 소스 `7cb211378a2ac6d421c5f6f3f71411937af23136`로 빌드한 `rg`. Rust 빌드 환경과 바이너리의 출처 확인이 필요하다. 이 과제에서는 해당 바이너리를 준비하지 않았다. `RG_BIN`에는 검증한 바이너리의 절대 경로를 넣는다. 아래는 새 로컬 fixture이며 원 이슈의 실제 환경 복제가 아니다.

```bash
mkdir -p docs/workstreams/research/AF-RES-070/private/reproduction/rg-fixture/.git
mkdir -p docs/workstreams/research/AF-RES-070/private/reproduction/rg-fixture/.child
printf '%s\n' '*.txt' > docs/workstreams/research/AF-RES-070/private/reproduction/rg-fixture/.gitignore
printf '%s\n' 'needle' > docs/workstreams/research/AF-RES-070/private/reproduction/rg-fixture/.child/hit.txt
```

cwd를 새 fixture의 `.child`로 바꾼 뒤 각각 별도 종료코드를 기록한다.

```bash
"$RG_BIN" --version
"$RG_BIN" --debug --hidden -l needle .
"$RG_BIN" --debug --hidden --no-ignore-parent -l needle .
```

판별할 것: hidden 해제만으로 부모 ignore 규칙까지 해제되는지. 실패할 수 있는 조건: git 저장소 인식·실제 설정파일·환경변수·버전이 달라지면 원치 않은 다른 규칙이 개입한다. 두 실행의 debug 원출력에서 적용 규칙을 확인하기 전에는 성공으로 분류하지 않는다. 실행 결과는 새 연구자 시험으로 표시하고 RG1840의 과거 실사용 성공으로 귀속하지 않는다.

## 4. jq 입력 시작과 목적의 별도 시험

환경: jq1.6 소스 `2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e`의 빌드된 바이너리. `JQ_BIN`에는 해당 절대 경로를 넣는다. 설치명 `jq-1.6`만으로 Fedora 등 패키지의 실제 소스/decnum 설정까지 같다고 가정하지 않는다.

```bash
mkdir -p docs/workstreams/research/AF-RES-070/private/reproduction/jq-fixture
printf '%s\n' '[1]' > docs/workstreams/research/AF-RES-070/private/reproduction/jq-fixture/foo.json
printf '%s\n' '[2]' > docs/workstreams/research/AF-RES-070/private/reproduction/jq-fixture/bar.json
printf '%s\n' '[3]' > docs/workstreams/research/AF-RES-070/private/reproduction/jq-fixture/baz.json
```

cwd를 이 fixture로 바꿔 각각 실행한다.

```bash
"$JQ_BIN" --version
"$JQ_BIN" '[inputs | input_filename]' foo.json bar.json baz.json
"$JQ_BIN" -n '[inputs | input_filename]' foo.json bar.json baz.json
"$JQ_BIN" -n '["1","a","2"] | map(try tonumber catch null)'
"$JQ_BIN" -n '["1","a","2"] | map(try tonumber)'
```

첫 대조는 입력 소비 단계이며 jq2394의 선택 필드와 연결된다. 뒤 대조는 null 자리를 보존하는 목적과 실패 항목을 생략하는 목적을 구분한다. jq2267의 실제 회귀는 `a17dd3248a666d01be75f6b16be37e80e20b0954` 빌드를 별도로 준비해 같은 입력으로 시험해야 한다. jq2406의 decnum ON/OFF는 **동일 소스 SHA와 컴파일 옵션**을 먼저 고정해야 하며, 현재 공개 스레드의 “1.6” 문자열만으로 같은 판이라고 할 수 없다.

## 5. Pandoc 완전 문서와 단편

환경: Pandoc2.11.3 `ec0ec4af7ca74bd6cce7ba69cdbeb615e62f5794`의 바이너리. `PANDOC_BIN`에 해당 절대 경로를 넣는다.

```bash
mkdir -p docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture
printf '%s\n' 'alpha' > docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture/input.md
"$PANDOC_BIN" --version
"$PANDOC_BIN" -f markdown -t icml docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture/input.md -o docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture/fragment.icml
"$PANDOC_BIN" --standalone -f markdown -t icml docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture/input.md -o docs/workstreams/research/AF-RES-070/private/reproduction/pandoc-fixture/document.icml
```

출력 template/header의 차이를 확인하는 시험이다. 실제 InDesign 열기·그림·링크 보존 성공은 별도 환경과 원 입력이 필요하며 이 시험으로 대신하지 않는다. Pandoc7013의 당시 URL 서버 응답,7003의 앞 단계가 생성하는 전체 파일군,7113의 실제 옵션 방향은 당시 원자료가 더 필요하다. 임의의 현재 URL로 바꾸어 시험해 과거 동작을 확정하지 않는다.

## 재개 첫 행동

먼저 최종 결과 SHA에서 표2의 **RG1840과 PAN7013** A 봉인·고정 근거·노출 이탈을 재대조한다. 이 두 판별 조건을 새로운 효과 사례로 승격하려면, 정해진 공개 모집 경로에서 최초판을 회수하고 아직 댓글을 읽지 않은 새 사례의 A를 다시 봉인해야 한다. 기존24건의 선택 필드를 후속 내용을 보고 바꾸는 방식은 사용하지 않는다.
