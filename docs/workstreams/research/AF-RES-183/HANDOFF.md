# HANDOFF — AF-RES-183

**자체 상태 PARTIAL** (외부 실제값 결측). 중앙 dot-control.json 수정 없음. 작업 브랜치 `work/research-af-res-183`, 통합 시작 SHA `6fa67328360b02bc7e7270d4ad3300bfe0f286bd`; 계획 SHA `128f673685ec804c526a38e3f89d4d8a43fcd299`; AF-RES-174 고정 HANDOFF `347f0c96944d074605320027fe8653b0b83a41ad` (중앙 DONE, 자체 PARTIAL). 이번 결과 본체 최종 SHA `b36b477fdded2d6cb8d84f72ae6eb9ef60f2be63` (SELF_CHECK까지; HANDOFF는 그 다음 커밋).

- 사전 scope `d9b9edcf7b1b7d5c6e75f72874ef1fe7b34f3000`; 결과 개봉 전 예측 `7b345f44fee54f60104539f43c37dabb5a410aa4`, UTC 2026-11-24T19:19:06Z. [SCOPE](SCOPE.md)와 [predictions](predictions.csv) 보존. ③ MoneyPHP 관련 README tie 예제 노출(정확한 입력 결과 아님; UTC 날짜 오기 RESULT에서 수정, 정확 초 미상). 나머지 15셀 알려진 결과 미노출. 독립 blind 아님.
- 대표: [RESULT](RESULT.md), [sources](sources.jsonl), [frame](frame.csv), [comparisons](comparisons.csv), [replay-inputs](replay-inputs.json), [advice](advice.csv), [SELF_CHECK](SELF_CHECK.md). RESULT/원장 최종 버전 `51bc163bc40fc326b768648957725b3d7ceaa215`; 자체점검 시 대표 7파일 해당 SHA 재열람 및 구조 검사, 24 예측/16 비교/8 재생/44 ledger/49 frame/3 advice, 일관성 불일치 0. 보수 산입 고유 원자료 24: 구현/시험9, 유지자4, 선거6, 금액5; 유형별 최소 충족. 6 사건(3 의석결정·2 유지보수 계보·1 Stripe 변경 보고), 거래 실제 관측 미확인; 고정입력 공개 독립 관측 0. E06 PDF 텍스트 직접 읽음, 시각 screenshot 실패. Dinero tag date를 공개 시각 대용(404).
- 코드 판독(관측 아님): MoneyPHP v4.8.0 `b358727ea5a5cd2d7475e59c31dfc352440ae7ec`는 H와 같은 8개 작은 정수 벡터, float remainder 및 first-key tie. Dinero.js v1.9.1 `13965e2298c8f0aa5fbbd4b1bdcba449e2b9f8d1`는 N1과 같은 8벡터. ②④⑥에서 N1과 H가 수령자를 갈라놓고 ①⑤⑦⑧에서는 모두 같음. ③ N2가 합계 불일치. 정확 공개 fixture 기대 1/16 (MoneyPHP ③ 관련 노출), 15 미발견; actual 동일 입력/SHA 16 미발견; 유효 분모 0, **적중률 미확인**. 실패 16으로 바꾸지 않음. 근접 정확 설명 자체가 두 구현을 판별; 원거리 링크는 정책/반례의 추가 설명일 수 있으나 사전 우월 증명 없음.
- 범위 검증: 시작 통합 SHA에서 SELF_CHECK SHA까지 GitHub compare 14 ahead/0 behind, 변경 9파일 모두 owned_path 안, 외부 파일 0. HANDOFF 자체는 추가 1파일. workbench manifest/check 및 런타임 시험/독립 심사 미실행. 연구 색인 변경 안 함.

## 첫 재개 행동
1. [comparisons.csv](comparisons.csv)의 ②④⑥ 우선, exact head SHA와 입력/순서/단위/실제 출력이 포함된 유지자 제출 로그 또는 공개 CI artifact를 찾는다. 기존 X02/X03에서 GitHub actions runs total_count=0, X09/X10 combined status pending total_count=0; 비공개/삭제 로그를 추측하지 않는다. 공개 기록을 얻지 못하면 기존 분모 0 유지. v1.9.1 공개시각은 `npm view dinero.js time --json` 및 `npm view dinero.js@1.9.1 gitHead --json`에서 확인(현재 미실행). 결과가 cutoff와 다르면 태그 선택 판단부터 보정한다.
2. Codex Cloud에 새 통제 재생을 위임. 다음 명령은 재현 절차 제안(아직 실행하지 않음). 네트워크·PHP/Node 환경·패키지 설치 가능 여부와 lock 상태를 확인한 뒤 진행. 외부 OSS checkout은 별도 임시 경로; agentflow 저장소의 변경은 owned_path만. replay-inputs.json에 8입력, 통화 USD precision2, A/B/C 순서 및 비교값 포함. PHP 8.3 + ext-bcmath/filter/json, Composer 2를 제안; Dinero 구형 toolchain의 Node 16/npm 8 또는 호환 환경 제안(환경 버전/실패 그대로 기록). R01/R02 manifest는 고정판에서 확인. 정확 런타임, commit, dependency lock SHA256, stdout/stderr, exit code, UTC를 저장. 설치/빌드 실패 시 결과 unknown, fallback 환경 변경 명시. 새 실행은 역사적 공개 실행과 별도 열.

```sh
# agentflow checkout에서 시작, replay 파일 절대경로
export INPUTS="$(pwd)/docs/workstreams/research/AF-RES-183/replay-inputs.json"
test -f "$INPUTS"
TMP="$(mktemp -d)"
git clone https://github.com/moneyphp/money.git "$TMP/money"
cd "$TMP/money"
git checkout --detach b358727ea5a5cd2d7475e59c31dfc352440ae7ec
git rev-parse HEAD
php -v; php -m; composer --version
composer install --no-interaction --no-scripts
if test -f composer.lock; then sha256sum composer.lock; fi
vendor/bin/phpunit tests/MoneyTest.php
php -r 'require "vendor/autoload.php"; $j=json_decode(file_get_contents(getenv("INPUTS")),true); foreach($j["inputs"] as $c){$m=new Money\Money($c["amount_minor"],new Money\Currency("USD")); $v=array_map(fn($x)=>(int)$x->getAmount(),$m->allocate($c["weights"])); echo json_encode(["id"=>$c["id"],"ordered_ids"=>$c["ordered_recipients"],"vector"=>$v,"sum"=>array_sum($v)]),PHP_EOL;}'
git clone https://github.com/dinerojs/dinero.js.git "$TMP/dinero"
cd "$TMP/dinero"
git checkout --detach 13965e2298c8f0aa5fbbd4b1bdcba449e2b9f8d1
git rev-parse HEAD
node -v; npm -v
# lock 없으면 npm install --ignore-scripts 로 대체하고 재현성 하락 기록
npm ci --ignore-scripts
if test -f package-lock.json; then sha256sum package-lock.json; fi
npm test -- --runInBand test/unit/dinero.spec.js
npm run build
node -e 'const fs=require("fs"),mod=require("./build/cjs/dinero.js"),Dinero=mod.default||mod,j=JSON.parse(fs.readFileSync(process.env.INPUTS,"utf8")); for(const c of j.inputs){let v=Dinero({amount:c.amount_minor,currency:"USD",precision:2}).allocate(c.weights).map(x=>x.getAmount());console.log(JSON.stringify({id:c.id,ordered_ids:c.ordered_recipients,vector:v,sum:v.reduce((a,b)=>a+b,0)}))}'
```

예상 관측(실행이 맞으면): replay 파일 code_inferred_not_observed의 벡터, sum=T, zero=0. 각 입력에서 예외도 수집하고 하나 실패해도 나머지 입력을 별도 실행(위 루프는 첫 예외에 종료하므로 필요시 입력별 try/catch 추가). ①↔② 동일 ID 재매핑, ⑤↔⑥ 및 ⑦↔⑧ 증분 확인; 별도의 구성 반례 (4→5,[5,3,1])는 H 단조성 한계 확인용이며 8자리 분모에 넣지 않는다. MoneyPHP float/near tie와 ID순 변경, 환불 원 지급 추적은 후속 대조 후보. 설치/명령 출력과 expected 비교를 분리.
3. 필요한 경우 workbench CLI help에서 manifest 출력/의존 옵션 확인 후 `python -m workbench.session start --help`, `python -m workbench.session check --help` 수행; 지정 owned_path 밖에 쓰지 않는다. 연구 결과/로그는 새 커밋으로 보정. 본 작업에서 해당 명령은 실행하지 않았다.

## 색인 제안
AF-RES-183 — 의석 최대 분수 나머지 ↔ 금액 allocate 잔여 단위 수령자 판별; MoneyPHP H 유사 / Dinero N1(고정판 코드 추론), 예측 8×3·원자료24·공개 실행 분모0(PARTIAL), 순서/동률/단조성·환불 제약별 링크 후보와 재생 입력 제공.
