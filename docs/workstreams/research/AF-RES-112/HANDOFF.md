# AF-RES-112 인계 — PARTIAL

**수용 판정은 PARTIAL이다.** Godot 자연 요청3건의 A/B 비교와 지정 G2 삭제 대조를 마쳤으나, LilyPond 시간순 모집틀을 확보하지 못해 주3자리가 비었다. 필수 자료 배당은21/24이고 역사판 실행값의 판정 가능 분모는0이다. 검사 통과가 이 연구 결손을 없애지는 않는다.

- 작업 브랜치: `work/research-af-res-112`.
- 쓰기 범위: `docs/workstreams/research/AF-RES-112/`만. 중앙 `dot-control.json`, 통합 브랜치, main은 변경하지 않았다.
- 계획 기준: `c40ef7723d851b628233bfb60dff8dfd292385cf`.
- 실제 시작: `0bcaf7c90f3324447fd1b8bf12c514187ca4776b`. 자기 브랜치가 없어 이 통합판에서 시작했다. 관련 필독 파일의 계획 이후 차이는112 배정 행이며108 입력은 같았다.
- 운영 의존:108 HANDOFF `8b00aaa2eada69044c15784590956eecf5ea6268`, RESULT/pairs/metrics `806cdff845acfb965a1b2f2a641010c2e9604498`. 다른 PLAN#27 작업 파일·검토자·중간 결과에는 의존하지 않았다.
- **검사한 결과 SHA: `e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2`.** [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/RESULT.md).
- **검사 뒤 영수증 SHA: `7fc22b5140bd959def08f4a9fdad9fe3be5ddfc0`.** [고정 검증 영수증](https://github.com/laadkke-arch/agentflow-open/blob/7fc22b5140bd959def08f4a9fdad9fe3be5ddfc0/docs/workstreams/research/AF-RES-112/evidence/final-verification.json). 이 영수증과 본 인계는 앞선 결과 SHA 검사에 포함된 파일이 아니다.

## 인계할 관측

| 구분 | 실제 결과 | 결손·해석 제한 |
| --- | --- | --- |
| 모집 | Godot41본문 중 재게시1제외, 첫40고유 사건의 첫 적격3건 #56680/#57026/#57268 | LilyPond 공식 월별 index/mbox 미확보. 검색0건을 ‘문의 없음’으로 해석하지 않음 |
| 주 비교 | 예정12꾸러미 중6실행; 최대36단계 중18관측·18미모집·0조기종료 | 자연 주사건3/6. 합성 정상/경계 입력은 자연 사건 수에 더하지 않음 |
| 판독 주체 | 같은 설정을 상속한 새 AI 문맥6개, A/B 순서교차; 별도 gold·출처 감사·봉인 후 평가 | 사람이 읽은 실험 아님. 공유 디스크의 절차적 가림, 정확한 provider판/seed 미상 |
| 엄격 쌍 결과 | A만0·B만0·양쪽0·어느 쪽도3·비교불가3 | 세 쌍 모두 경로·노출·최종라벨 동일. 한 줄의 일반 효과/무효를 추정하지 않음 |
| 답의 보정 | 충분한 근거 성공0/6; 위험한 확정0; 정당 보류2; 중요한 미확인을 남긴 조건부4 | gold 라벨일치4/6은 성공이 아님. 역사값 정확도는 분모0/null |
| 비용 | A/B 각각9개봉·7249자·7505B. B추가86+74+73=233자·503B | 능동 제작/판독 시간 미계측. wall time을 사람의 시간 절약으로 환산하지 않음 |
| 보조 대조 | G2 C 새 문맥1개·3단계·3512자·3684B, A/B와 같은 노출·보류 | L2 C미모집. 18자 삭제로74→56자, 길이 비일치. 공통 요청에는 보존조건이 계속 있음 |
| 출처 | 원장97행=직접열람85+접근실패12. 고유1차73, 같은 저작 중복11, 제외재게시1 | 필수층 가능36개 중 배당3/8/6/4=21/24. 저작73은 독립 저자·실험73을 뜻하지 않음 |
| 실행 | 제공 Godot4.7.2에서 import5·관측run9; 원G2는8출력+assertion실패+OSexit0 | 원 역사판0. G1구성4/G2변형2/G3flag변형1은 보조; 후속4포트는 원3재현이 아님 |

G1은 목록→Scene.gd→Path2D.tscn, G2는 ZIP목록 두 구간→filesystem_cache7, G3는 목록→main.gd→main.tscn이었다. 원문 범위와 선택 이유는 [trails.jsonl](trails.jsonl), 단계 판단은 [answers.csv](answers.csv), 조건·비용·음성 대조는 [pairs.csv](pairs.csv)에 있다. 수신자는 G1 자원 수명/실제 load대조, G2 원 .gd/.tres, G3 A_Thing.gd·역사판 복원값을 확인하지 못했다. 각 단계에서 실제 읽은 근거만 성공 평가에 사용했다.

## 반례와 절차상 정정

현재판에서 G1의 load released/preload shared/preload local/load held는 새 점 수0/1/0/1이었다. G2의 동일값 대조4와 UID제거 경로 대조7은 원 입력8과 다르므로 타입 동일성만으로 결과를 설명할 수 없다. G3의 후속4포트는 local=true/false에 따라 재시작값1/0이 갈렸다. 원 역사판을 재현했다고 쓰지 않았다. LilyPond 공통 변수/파트 태그·음악 값 복사, IIIF 작품/Canvas, RFC9110 HEAD/304 예외와 Werkzeug 원 테스트는 별도 보조층이며 주 수신 성공에 더하지 않았다.

모집 규칙은 먼저 원격 봉인했지만, 개별 사건 입력의 원격 봉인 전에 gold 독해를 시작했다. gold 시작 시각 일부는 사후 분 단위 근사치여서 정규화24행의 개별 열람 UTC는null이다. 공통 요청의 조건이 B와 중복되고 최적3개봉 경로의 존재도 따로 입증하지 못했다. 이 한계는 [SELF_CHECK.md](SELF_CHECK.md), [acceptance-evidence.json](evidence/acceptance-evidence.json), [시각 정정](gold-work/clarifications.md)에 남겼다.

원 수신 봉인 이후 만료된 공개 ZIP 서명 쿼리만 제거했고, 실제 노출18개와 선택·판단 내용의 불변을 확인했다. 파생 trails에는 기존 choice 이벤트를 결합했다. G1의 connector 원문주소는 HTTP 최종 리다이렉트 관측이 아니므로 별도로 표시했다. 원 `arrival_confirmed` 표기를 소급 고치지 않고 한정했다. [파생 원장](evidence/ledger-derivation.json), [노출 불변](evidence/exposure-invariance.json), [검토 수정 내역](evidence/report-qa-resolutions.json).

## 고정 결과판 검사

검사 주체는 root, 환경은 제공된 Linux/Python3.12.14의 깨끗한 detached worktree였다. `codex-cloud`는 호출자 라벨이며 외부 계정 연결/GitHub Actions 실행 증명이 아니다. 시작·종료 HEAD는 모두 결과 SHA와 같고 tracked/untracked 상태는 깨끗했다. 결과판 변경179경로는 모두 owned_path 안이었다.

원격 고정 SHA에서 RESULT, metrics, pairs, gold, reproduce, trails, sources의 완전한7파일을 다시 받아 Git blob과 바이트 일치를 확인했다. 보고서 핵심·쌍 원장 전6행·궤적18행의 선택/주소/범위·필수 배당21원문행과 재현 명령을 다시 읽었다. 대표 원문도 다시 열었고 G1 고정 커밋의 두 blob이 실제 A/B 수신 blob과 같음을 확인했다. [고정판 재열람](evidence/remote-result-reread.json), [대표 원문 재열람](evidence/final-primary-reread.json).

| 명령 | 종료값·관측 |
| --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-112/manifest.json --fetch` | 0; 명시 manifest1개 passed, remote_checked. 검사시 통합판814ed0f15473d50a1a176ddd56a0df8a9f746a7e, 계약해시 동일 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0; doctor/acceptance/research-case/original-smoke/sessions 명령5개 모두0 |
| `python -B docs/workstreams/research/AF-RES-112/compile_observations.py --check` | 0; 주12꾸러미·36자리 재계산 일치 |
| `python -B docs/workstreams/research/AF-RES-112/compile_control.py --check` | 0; 보조2꾸러미·6자리 재계산 일치 |
| `python -B docs/workstreams/research/AF-RES-112/build_results.py --check` | 0; pairs/metrics/필수표를 포함한RESULT 일치 |
| `python -B docs/workstreams/research/AF-RES-112/check_study.py` | 0;665근거 참조 범위·자료배당·문맥/입력/도구 해시·필수표 순서/마지막3행 확인 |
| `python -B docs/workstreams/research/AF-RES-112/redact_transport_metadata.py --check` | 0; 현재 JSON의 만료 서명 쿼리 잔존 없음 |
| `node docs/workstreams/research/AF-RES-112/check_reader_runtime.mjs` | 0; 합성2세션의 예산·순서·링크·최종답 제한 통과 |

공통 검사의 자동 세션 발견은 **0개, no_active_sessions/not-executed**였다. 위 manifest 명시 검사1회의 통과와 구별한다. Node 합성 검사는 결과 이전2세션을 최종 게이트에서 다시2세션 실행한 것이며, 총4합성 세션을 주6/보조1독립 수신 문맥에 더하지 않는다. 전체8명령의 stdout/stderr/실행 영수증, 공통 하위 로그와 작업별 receipt는 [final-checks](evidence/final-checks/)에 보존했다. 검사 뒤의 원 로그는 말미 공백까지 그대로 보존했다.

## 묶음별 원격 커밋

모든 행은 자기 브랜치의 원격 GitHub 커밋이며 기대 HEAD 조건으로 갱신했다. 원격 반영은 GitHub ref/고정 파일 재열람과 Git fetch로 확인했다. 셸 push 인증 실패는 계정 변경 없이 지정 GitHub 연결 도구로 처리했다.

| 묶음 | 원격 SHA |
| --- | --- |
| 모집·예산·계약 봉인 | `c8fcd064130259914c782a1f277bddd105711fdd` |
| 모집 입력·제한 판독 전송 | `9d0fd50637c911b003ba421361cf35230e150c30` |
| A/B 꾸러미 별도 봉인 | `d6966cff955134714fa64d0c04c65b53e5216bd4` |
| gold 별도 봉인 | `a31795242cb3e94e4df53bbb7fd34601de8dadb2` |
| 주 수신 궤적·답 봉인 | `dd3c615dc8060a88259af6294848749d042d697f` |
| 지정 삭제 대조 꾸러미 봉인 | `7a6c72b00933db0a7b7b0e7d103eb7c38b6b596c` |
| 대조 수신·전송 메타데이터 정리 | `3d356e09b83894d1c44e30b5532004abecc7a9a2` |
| 출처 감사·반례·실행·독립 평가 | `aa57f0a3917888e0ce194d84a7aa9b52108d87db` |
| **검사 대상 결과판** | **`e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2`** |
| **검사 뒤 영수증** | **`7fc22b5140bd959def08f4a9fdad9fe3be5ddfc0`** |

이 HANDOFF는 위 검사·원격 확인 후 마지막 단독 커밋으로 추가한다. 영수증 안의 ‘마지막 HANDOFF 대기’는 영수증 커밋 시점의 상태이며, 이후 본 파일의 단독 커밋으로 그 단계를 마친다. 본 파일 이후 결과 수정이나 추가 실행을 예정하지 않는다.

## 막힌 이유와 다음 첫 행동

**첫 행동은 LilyPond 공식2022-01 원 index 또는 mbox를 확보해 고정된 시간순 모집틀을 복원하는 것이다.** 기존 실패 영수증은 `recruitment/lilypond/access-receipts.json`에 있다. 원 index가 열리지 않으면 공석을 유지한다. 예를 들어 다음은 원 index 수신을 재개하는 명령이며 아직 성공을 확인한 명령이 아니다.

```sh
mkdir -p docs/workstreams/research/AF-RES-112/cache/lilypond-resume
curl --fail --location --max-time 30 https://lists.gnu.org/archive/html/lilypond-user/2022-01/date.html --output docs/workstreams/research/AF-RES-112/cache/lilypond-resume/2022-01-date.html
```

성공하면 `SCOPE.md`/`protocol-amendment.json`의 기간·질의·정렬로 최초 원질의를 묶고 첫40개를 확정한다. L1–L3 원 목적·보존조건·입력을 원격 봉인한 뒤 새 gold와 새 수신 문맥으로 진행한다. 기존18관측은 고치지 않는다. 독립 문맥을 얻지 못하면 위치 재생/동일인 재판독으로만 표시하고 독립 수신 성공률을 내지 않는다.

미실시 실행은 다음 입력이 있어야 재개할 수 있다. 상세 전체 명령은 [reproduce.md](reproduce.md)와 [HISTORICAL-NEXT.md](gold-work/HISTORICAL-NEXT.md)에 있다. 새 바이너리 설치·계정 변경·유료 API·외부 연락은 수행하지 않았다.

| 미실시 | 필요한 입력 | 실행할 명령·다음 관측 |
| --- | --- | --- |
| G1 원3.4.2 load/preload | 정확한3.4.2 실행파일/해시; 원 repo1a5942e87c2510e6f9fb281ba27f6a257258eb35; 한 호출만 바꾼 복사본; 점/프레임 관측 driver 미작성 | `"$AF112_GODOT_342" --version`, `--help`; 문서의 준비 후 `timeout --signal=TERM 120s "$AF112_GODOT_342" --path "$AF112_HIST/G1-shared-load" res://Scene.tscn`. 반대 preload·local쌍도 같은입력/씬flag로 비교 |
| G2 원4.0-dev.20220118 | 날짜뿐인 개발판의 정확한빌드·바이너리 미확보; 원ZIP e016439485363faaff80376880e71c92b35d7bd390c7da0d5462ca9372f7f9ea; 새캐시 | `python -B docs/workstreams/research/AF-RES-112/gold-work/fetch_examples.py`; 준비 후 `timeout --signal=TERM 15s "$AF112_GODOT_40D" --path "$AF112_HIST/G2-original" res://test.tscn`. 항목별UID/path/instance/value 로거는 별도진단변형으로 추가 |
| G3 원3.4.2/4alpha1 | 원3ZIP 7dfda91dcf0440abcc8769d86b884f69e86e681c935d0d2b1d899d8574da5734; 정확바이너리. alpha1 호환 원입력도 미확보 | 준비 후 `timeout --signal=TERM 15s "$AF112_GODOT_342" --path "$AF112_HIST/G3-original" res://main.tscn`. g3출력 보완본은 별도변형. 후속4포트를 alpha1원입력으로 치환 금지 |
| LilyPond 회귀4개 | 설치된정확2.24.4 실행파일이 없음. 입력URL·해시4개는 regression-receipts.json | reproduce §6의 고정4파일 수신/해시검사 후 `"$LILYPOND_2244" --output=docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-filter docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-filter.ly`와 나머지3입력 실행, 생성악보 검토 |
| Werkzeug 보조 테스트 | 고정6389612fd1ee1bd93579eed5026e8fd471d04abd checkout과 호환 pytest/Werkzeug 환경 | 그 checkout에서 `python -m pytest tests/test_wrappers.py::test_response_304_no_content_length`. 현재는 원 assertion 독해 사례이며 주 성과 검증을 대신하지 않음 |

시간제한 종료124와 OSexit0를 의미적 통과로 해석하지 않는다. 현재판 결과와 원 보고가 충돌하면 판·캐시·입력·stderr를 보존해 비교한다. 색인 갱신은 [INDEX_PROPOSAL.md](INDEX_PROPOSAL.md)의 제안만 남겼다.

## 가장 중요한 불일치·약점과 다음 조사 — 정확히 3건

| 불일치·약점 | 다음 조사·직접 열 자료 | 어느 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| LilyPond의 시간순 모집틀 결손: 자연 요청 3/6, 필수 배당 21/24. Godot 세 사건만 비교 | 공식 2022-01 date/thread index 또는 원 mbox를 먼저 열어 고정 질의·정렬로 첫40개를 복원; 임의 검색 사례로 대체 금지 | L1–L3의 원 요청·인계 링크·보존 조건을 봉인하고 새 A/B 6문맥을 실행하면 분야 비교 분모가 생김 |
| 모든 A/B 및 G2 삭제 대조의 노출이 같음. 공통 요청이 이미 조건을 설명하고 1500자/회 텍스트·ZIP 뷰어가 탐색을 제약 | 같은 원 요청에서 기존 조건은 유지하되 중복 안내와 새로운 탐색 단서를 구분하는 새 사전등록; 실제 브라우저/다른 예산과 별도 비교 | 여러 새 문맥에서 B가 다른 필요한 절에 도달하고 필수조건을 더 복원하며 좁은 안내의 반례 누락도 증가하지 않을 때 안내 효과 판단 변경 |
| 역사판 실행값 분모0; 기준 읽기 시각 일부 근사·입력 원격 봉인보다 gold 독해 선행; 공유 디스크와 힌트 가시성으로 가림 한계 | 고정 원 ZIP/repo와 정확한3.4.2·4.0-dev 빌드로 재실행; 모집 입력 원격 봉인 후 별도 gold·수신 권한과 자동 시각을 계측 | 같은 판·설정에서 수치와 필수조건이 재현되고 봉인·노출 순서를 정확히 입증하면 역사판 미확인과 절차적 제한을 재평가 |
