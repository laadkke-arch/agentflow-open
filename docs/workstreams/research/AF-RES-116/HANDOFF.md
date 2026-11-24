# AF-RES-116 인수인계 — PARTIAL

## 1. 식별

- 작업 ID / 시도: **AF-RES-116 / #2 재개**. 배정 종류는 `web-pro`이며 실제 수행은 제공된 ChatGPT 클라우드 실행기·GitHub 연결·분리된 AI 문맥이다. 별도 Web Pro 브라우저 세션이나 사람 실험을 관측했다고 주장하지 않는다.
- 실제 모델/주체: 루트 `/root`, 대화 환경이 표시한 GPT-6 Astra Pro. 수신 18개 새 문맥과 평가 2개 새 문맥의 역할·노출은 [resume-roles.json](evidence/resume-roles.json), [독자 시작 기록](evidence/reader-launches.jsonl), [평가 입력 기록](evaluation/input-receipt.json)에 있다. 서비스 내부 모델 식별자를 독립 검증한 것은 아니다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-116`.
- 재개 시작 SHA: `8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473`. 기존 봉인·브랜치·진행 커밋을 보존했다.
- **검사한 결과 SHA: `31cc131279e606c9d691524525cbdbdf7dc7b44a`**. RESULT·원장·재현 절차·SELF_CHECK가 이 커밋에 고정돼 있다.
- **검사 증거 SHA: `b8162d78efb25bf3d92bffc82498b7d00ca22c5e`**. 이 인계 작성 전 마지막 원격 저장/재열람 커밋이다. 그 `evidence/acceptance-evidence.json`의 Git blob `c379212a10e2f25912e64a9a73ce5de11dd45bed`를 다시 읽어 결과 SHA·12명령 통과·미실시 범위를 확인했다.
- 마지막 실제 검증 증거: 고정 결과의 깨끗한 별도 checkout에서 계약·공통·연구 검사 실행, 결과 파일 4개와 대표 원자료 4건 원격 재열람. [acceptance-evidence.json](evidence/acceptance-evidence.json)의 기록 UTC는 `2026-11-24T06:01:57.633781+00:00`이다. 인계 전 원격/로컬 마지막 대조일은 **2026-11-24 UTC**이며 인계 작성 시각은 `2026-11-24T06:08:55Z` 이후다.
- 상태: **PARTIAL**. 저장소 템플릿의 일반 상태명보다 이번 사용자 지정 상태를 우선한다. 산출물 재현 검사는 통과했지만 P3 원 실행 환경·I3 동일 원 JP2·초기 원격 봉인 시각 증빙 한계는 닫지 않았다.
- PR: 생성하지 않았다. 통합·제어표 변경 없이 이 브랜치로 반환한다. 이 파일만 마지막 단독 커밋으로 저장하며 자기 커밋 SHA는 파일 안에 순환 기입하지 않는다.

## 2. 사용자 요구 / 작업 범위

목표는 같은 공식 시작 URL을 받은 후속 조사자에게 원문 조건을 반복한 한 줄(B) 또는 실제 목차 표지를 추가한 한 줄(C)이 무엇을 바꾸는지, 공통 요청만 있는 A와 비교하는 것이다. **답이 닿는가 / 독자가 실제 그곳에 갔는가 / 읽은 근거로 판단이 맞는가**를 따로 관측했다. 자연 여섯 요청을 교정 양성 사례로 교체하지 않았다.

- 허용 쓰기 경로: `docs/workstreams/research/AF-RES-116/`만. `docs/automation/dot-control.json`을 수정하지 않았다.
- 계획 기준: `670ecde1dab07aede6760618a7d907f0cdff185a`. 재개 때 통합 브랜치 `a4e965896fce25b44f0695c91ed7793693b78b11`의 AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·RESEARCH_BRIEF·자기 행을 읽었다. [재개 기록](evidence/resume.json).
- 마지막 `--fetch` 검사 통합 SHA: `53346050bf7962e92f4596892dab33d4e6730f22`. 재개 이후 공통 계약 관련 차이는 제어표 +2/-2뿐이며 공통 지침은 같았다. 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`이다.
- 첫 묶음의 `workbench.session start ... --fetch` 계약과 [manifest.json](manifest.json)을 유지했다. 재개한다고 다시 시작 계약을 만들지 않았다.
- 운영 선행 AF-RES-112: [HANDOFF@a44a0e4](https://github.com/laadkke-arch/agentflow-open/blob/a44a0e4bd8fe4bca6945a2ff40fba7c745e877b8/docs/workstreams/research/AF-RES-112/HANDOFF.md), [RESULT@e3728f8](https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/RESULT.md) 및 같은 결과 SHA의 metrics·pairs·trails를 읽었다. Godot 동일 노출·완전 근거 0/6·부분 10/18·미모집 범위를 확인했고 이전 결원을 다시 모집하지 않았다.
- 이번 회차 다른 세 연구 작업의 출력·선행 실행에 의존하지 않았다. 원 작성자의 링크, 연구자가 만든 공통 시작점, 사후 기준 판독과 보조 반례를 구별했다.

## 3. 실제 변경과 수용 범위

| 파일 / 묶음 | 저장한 내용 | 확인 방법 |
| --- | --- | --- |
| [SCOPE.md](SCOPE.md), [frame.csv](frame.csv), 원문 스냅샷 | 2023–2025 공개 이슈, PR 제외, 본문 table/image 또는 profile/alpha, 도구별 생성 UTC·번호순 첫50개와 선택 첫3개 | 100행 순서 재구성, 선택6개 원문 body hash, 제외 사유 감사 |
| [packets.jsonl](packets.jsonl), [author-exposure.jsonl](authoring/author-exposure.jsonl), 고정 documents/viewer | A/B/C18전문, B/C 같은 문자 수, 원문 대응·새 표지, 실제 제작 노출, 1회 최대1500자 규칙 | 기준 읽기 전 문구 봉인, 동일 corpus/hash, 33개 봉인 파일 불변 확인 |
| [gold.csv](gold.csv), gold-work 두 폴더, [reachability.jsonl](reachability.jsonl) | 동작·보존·예외·판독 주체, 실제 입력 검사, 모든 허용 경로와 증인 | 6그래프 9,209경로 접두 노드·683 사건별 고유 문서면, 50기준mode 전수 재생 |
| [trails.jsonl](trails.jsonl), readers 원답, [answers.csv](answers.csv) | 18꾸러미·54단계 전부의 노출/선택/답/UTC, 단계별 가림 평가 | 54표시 지문 일치, 평가 근거 인용125개 노출 대조, 수신 원답 변경 없음 |
| [pairs.csv](pairs.csv), [metrics.json](metrics.json), [RESULT.md](RESULT.md) | 18짝 비교, 분모·비용·미관측, 필수 표1/표2 54행/표3 18행과 Q1–Q7 | 원장으로 재생성해 고정 파일과 바이트 대조 |
| [sources.jsonl](sources.jsonl), [source-counts.json](analysis/source-counts.json), analogies | 출처·도착·계보·판·UTC·읽은 구간·확인·한계·Q·자료 배당 | 273행, 원 URL143·도착 URL/locator172, 고유37저작; 필수 배당34저작 |
| [SELF_CHECK.md](SELF_CHECK.md), [reproduce.md](reproduce.md), evidence | Q별 근거·반증·결손·판단 변경 조건, 오프라인 재현·미실행 명령, 고정 SHA 검사 | 새 문맥 감사·결과 검토, 원격 파일/원자료 재열람, 12명령 exit0 |

### 받아들일 수 있는 관측

자연 6건×A/B/C의 **18꾸러미·54단계 모두 관측**했다. 조기 종료 0, 미모집 0이다. 사람을 모집하지 않았고 동일 모델 설정을 물려받은 새 AI 문맥을 사용했다. 공유 파일 시스템에서 허용 입력을 절차적으로 제한했으므로 OS 수준의 격리를 검증했다는 뜻은 아니다. 기준 작성자·문구 작성자·수신자·가림 판독자의 실제 노출은 별도 기록으로 남겼다.

사전 정의한 주 목표의 **전체 구간 노출은 0/18**이었다. 완전 답 기준으로 4건은 고정 뷰어/허용 corpus/3회 예산에서 도달 불가이고 P3·I3는 기준 자체가 부족해 미확인이다. 따라서 **확인된 자연 완전 답 reachable 분모는 0**이며 효과율은 `null`이다. 6/6의 주 목표 전구간 불가와 완전 답 기준 4불가/2미확인을 혼동하지 않는다. 사후 위치 진단에서는 같은 fragment 범위 도착 8/18, 주 목표 본문 일부 노출 3/18이며 후자는 모두 I2 Extract의 106/166자다. 나머지60자가 보이지 않았으므로 절 도착과 충분한 답을 구별했다.

가림 평가 결과는 완전 근거 답 **0/18 최종 꾸러미·0/54단계**, 부분 복원 **8/54**, 정당한 보류 flag **54/54**, 문서상 관련 예외 **4/54**, 위험한 확정 **0**이다. 부분과 보류 flag는 중복 가능하다. 배타적 등급은 부분8/보류46이다. 예외4는 I2의 Set→opaque3건과 P3 C의 RTF/figure 경계1건이며 원 자연 입력의 실패를 네 번 재현했다는 뜻이 아니다. 수신 인용95개 중 정확히 노출된94개, 전사 오류1개를 남겼다. 오류를 숨기거나 원답을 다시 쓰지 않았다.

A/B는 **6/6 사건에서 같은 문서면 순서**, A/C와 B/C는 4/6에서 같았다. C는 P1·P3에서 2단계부터 길을 바꿨다. P1 C의 입력 표현 절 도착은 TOC 동작의 근거가 아니어서 자기 ‘부분 확인’을 보류로 낮췄다. I1 C와 I2 A/C의 일반 옵션 설명도 같은 원칙으로 낮췄다. 네 건의 자기보고/평가 차이는 [answers.csv](answers.csv)에 남아 있다.

수신 비용은 A와 B 각각18개봉·25,714자/26,464B, C18개봉·25,655자/26,413B이며 전체 **54개봉·77,083자/79,341B**다. 모든 짝의 개봉 차이는0이다. B/C 한 줄 길이는 사건별87·89·87·91·94·79자로 같고 합계527자씩이며 UTF-8는 B1,204B/C1,116B다. 제작5파일 읽기 이벤트의 공유 wall duration560.956346초에는 처리·대기가 포함되고 잘린 표시 시도도 있었다. 수신 wall duration A247.582408/B292.783088/C268.800095초는 병렬 세션들의 합이며 사람 시간·효과 추정치가 아니다. 제작의 실제 알려진 노출·전체 출력·누락 범위를 [author-exposure.jsonl](authoring/author-exposure.jsonl)과 metrics에서 분리했다.

교정 K1/K2는 수신 전 봉인한 결정론적 재생이다. K1은 같은 시작점에서3회 안에 조작·인코딩 예외를 함께 읽고, K2는 같은 표제의 defaults Reader options로 가면 중요한 예외를 놓친다. D0 시작점만으로 충분한 기본 변환 질문은 사후 동일 작업자 진단이다. Prusa 조립·보수, Yale/Eisenhower/FDR 기록관 사례, 현재 ImageMagick 7.1.1-43 합성 alpha/ICC 반례는 보조층이며 자연 성공 분모에 섞지 않았다.

자료 배당은 요청6 / 기능 정의·구현9 / 별도 회귀·반대 입력6 / 교차 분야13 = **필수 분류34저작**이다. 선별 제외 원문3을 포함하면 전체37로 최소24 및6/8/6/4를 충족한다. 앵커·미러·판·반복은 새 저작으로 세지 않았다. 감사24행·수신54행도 고유 산입0이다. 결과 고정 후 대표 원자료4재열람은 기존 source_id를 가리키는 별도 검증 영수증이며 새 고유 저작을 늘리지 않는다.

## 4. 실제 검증 결과

검사 대상은 모두 **`31cc131279e606c9d691524525cbdbdf7dc7b44a`**다. 고정 SHA의 별도 detached checkout은 검사 전후 깨끗했다. 아카이브14개/952항목을 네트워크 없이 복원했다(950새 복원,2동일). 최종 검사와 앞선 dirty 작업트리 사전 검사를 구별했다.

| 검사 | 실제 명령 / 결과 | 증거·미실시 범위 |
| --- | --- | --- |
| 계약·원격 최신성 | `python -B -m workbench.session check docs/workstreams/research/AF-RES-116/manifest.json --fetch` — exit0 | remote_checked, outside_paths/error 없음. 기록한 최신 통합 SHA와 선행 고정 SHA 확인 |
| 저장소 공통 | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` — exit0 | doctor·acceptance·research-case·original-smoke 통과. registry check-all은 active session0으로 **not-executed**; 위 명시 manifest 검사가 별도로 수행됨 |
| 연구 전수 검산 | `python -B docs/workstreams/research/AF-RES-116/analysis/check_study.py` — exit0 | 봉인33파일, 18경로/54노출, 9,209경로, 50mode, 교정3경로와D0, 평가54/인용125, 원장·표 재구성·링크 검산 |
| 파생물7개 | `analysis/` 아래 `collect_trials.py`, `build_recipient_sources.py`, `build_sources.py`, `build_gold_index.py`, `export_reachability.py`, `prepare_masked_evaluation.py`, `build_results.py`를 각각 `python -B … --check`로 실행 — 전부 exit0 | 정확한 argv·cwd·시각·stdout/stderr hash는 acceptance의 각 항목에 보존 |
| 뷰어·수신 위험 검사2개 | `python -B -m unittest discover -s docs/workstreams/research/AF-RES-116/viewer -p 'test_*.py'`; `python -B -m unittest discover -s docs/workstreams/research/AF-RES-116/analysis -p 'test_collect_trials.py'` — 각각 exit0 | 뷰어10·수신3검사. 구현을 재실행해 독자 원답을 바꾸지 않음 |

총 **12명령 모두 exit0**. 각 명령 주체·입력 SHA·실제 UTC·기간·로그는 [acceptance-evidence.json](evidence/acceptance-evidence.json), [runner.json](evidence/final-checks/result-31cc131/runner.json)에 있다. 중첩 공통 로그10개와 원 경로의 대응도 같은 폴더에 보존했다. `codex-cloud`는 명령에 지정한 환경 표지이며 별도 제품 계정 통합의 증거가 아니다.

결과 SHA에서 RESULT 일부·metrics 전체 반환의 핵심 필드·reproduce 첫 구간·trails r13-s3를 원격 재열람하고 고정 blob/로컬 범위를 대조했다. Pandoc Shared.hs574–592, App.hs368–376, ImageMagick tiff.c1700–1737 및 P2 원 이슈 body도 고정 원자료와 재대조했다. [원격 파일 대조](evidence/remote-file-verification.json), [반환 구간](evidence/remote-result-rereads.json), [대표 원자료 대조](evidence/post-result-source-verification.jsonl), [원 요청 재열람](evidence/post-result-request-reread.json). 반환된 전체 파일을 모두 새로 의미 판독했다고 과장하지 않는다.

### 묶음별 원격 커밋과 노출 순서

| 묶음 | 원격 커밋 SHA | 그때 고정한 것 / 먼저 본 범위 |
| --- | --- | --- |
| 1 | `7a76c8ccefb6243b84e86efce16b62ba8b47ec2d` | 모집·행동·판정 규칙과 session manifest |
| 2 | `878f2e1b8d053f6eea4e3473d5b467ca98476a01` | 100프레임·선택6 원 요청; 성공 답·기준보다 먼저 |
| 3 | `27bdf61aac1c24299401879749fcbca1ce43e8a4` | 고정 문서·TOC·동일 뷰어 |
| 4 | `762fe1fc57b3b5f765f9d13537fa9c15b71b5b80` | B/C 동일 길이·실제 표지. 문구 작성자는 공통 요청·TOC만 허용 |
| 5 | `4e08a1f3ffb53a9dc6abebb1653d9dd2b1a72762` | 도달 그래프·교정 사전 명세; 자연 수신 전 |
| 6 | `8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473` | 기준·원자료·반례. 사용자 지정 재개 시작점 |
| 7 | `ef824a66c1a497441a70b8e2390d692263f7470c` | 재개·지침/선행 확인·수신 작업 경로 정정 |
| 8 | `ca24b65c11a029d603c9e8506b4e2fb72396c600` | Pandoc r01–r09 원 수신 |
| 9 | `47e8d24ad9c0313f6d1a361882198f42307a0d5d` | 전체18/54 원 수신. 이 뒤 가림 평가 입력 생성 |
| 10 | `81892aa60c5fe86ffab8f020503a597b347b9f1a` | 전수 도달성·실제 노출 기계 수출·가림 입력·반복 출처 |
| 11 | `1167bb29101c40d4c7fe4bcc58bbd1e2d746670f` | 가림 판정54·출처/봉인 감사·sources273 |
| 12 | `31cc131279e606c9d691524525cbdbdf7dc7b44a` | **검사 대상 결과**·세 표·Q별 반증·SELF_CHECK·재현 절차 |
| 13 | `b8162d78efb25bf3d92bffc82498b7d00ca22c5e` | **검사 증거**·고정 결과/원자료 원격 재열람·검사 로그. 본 인계 전에 원격 재열람 완료 |

묶음1–12의 기록은 [seals.jsonl](evidence/seals.jsonl)에 있다. 묶음13의 실제 재열람은 위 식별의 blob으로 기록한다. 초기 묶음의 commit/read 순서는 일관되지만 최초 update-ref 원응답이 보존되지 않아 외부 전송시각을 독립 인증할 수는 없다. 초기 캡처/열람/영수증 시각 차이를 지우지 않았다. 그 한계가 오염을 입증한다는 주장도 하지 않는다. 이후 평가자에게 SELF_CHECK·재현 정리를 맡긴 역할 전환은 가림 원판정이 봉인된 뒤이며 원판정 hash는 유지했다. [감사](evidence/audit/), [결과 검토](evidence/result-review.md), [정정 대응](evidence/result-resolutions.json).

### 미실시·미확인: 실제 명령과 필요한 입력

자연 역사판 실행, 사람 선택·시간·채택, 제한 없는 웹 경로의 가능성은 검사하지 않았다. Pandoc 문서는 upstream 고정판이지만 과거 MANUAL.txt의 HTML 변환기는 설치된3.1.11.1이었다. 오프라인 텍스트 뷰어는 당시 브라우저 화면을 재현한 것이 아니다. 역사판 바이너리가 없는 곳을 현재판 실행으로 대체해 완료라고 표시하지 않는다.

먼저 [reproduce.md](reproduce.md)의 아카이브 복원·해시 확인을 수행한다. 아래는 **아직 실행하지 않은** 명령이며 실제 확보한 바이너리 경로를 각 `AF116_…` 변수에 지정한 뒤 판·delegate·입력 hash를 기록해야 한다. 저장소 최상위에서 새 출력 폴더를 만든다. 기존 결과나 원 입력 폴더를 덮어쓰지 않는다.

```sh
AF116_REPO="$(git rev-parse --show-toplevel)"
AF116_OWN="$AF116_REPO/docs/workstreams/research/AF-RES-116"
AF116_REPLAY="$(mktemp -d "$AF116_OWN/handoff-runtime.XXXXXX")"
mkdir "$AF116_REPLAY/pandoc-runtime"
cp "$AF116_OWN/gold-work/pandoc/reproduction-inputs/"* "$AF116_REPLAY/pandoc-runtime/"
cd "$AF116_REPLAY/pandoc-runtime"
```

**P1/P2:** P1은2.19.2와 실제 conditional Lua filter·순서·native Div 보존 요구를, P2는 원 사용판·전체 YAML·키/중복/quoting 정책을 추가 확보한다. 연구 고정판3.8.3의 작은 입력만 통과했다고 원 YAML 전체의 동등성이 검증되는 것은 아니다.

```sh
"$AF116_PANDOC2192" --version
"$AF116_PANDOC2192" P1-original.md --self-contained --toc --output=P1-original.html
"$AF116_PANDOC2192" P1-hierarchy-counter.md --self-contained --toc --output=P1-hierarchy-counter.html
"$AF116_PANDOC2192" P1-raw-wrapper-candidate.md --self-contained --toc --output=P1-raw-wrapper-candidate.html
"$AF116_PANDOC383" --version
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-space-enriched.yaml P2-example.md
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-tab-enriched.txt P2-example.md
"$AF116_PANDOC383" --from=markdown-smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
```

P1은 TOC 항목·heading 계층·native AST·emitted group을 따로 대조한다. 계층을 바꾼 반대 입력이나 raw wrapper 후보의 성공을 원 native Div 보존 성공으로 바꾸지 않는다. P2는 token·Space/NBSP·약어 집합·원 파일 hash를 비교한다. 입력 해시와 상세 대조 기준은 [unexecuted-checks.json](gold-work/pandoc/unexecuted-checks.json)에 있다.

**P3:** 막힌 이유는 실제 원 Quarto/Pandoc 명령·PDF engine·template/filter/resource·TeX/longtable 판과 로그 부족이다. **다음 첫 행동은 원 command·.tex/.log·환경을 회수하는 것**이다. 아래 첫 두 실행은 후속 TeX의 component 재현이며 원 Markdown→PDF 전체 pipeline이 아니다.

```sh
"$AF116_TEX_ENGINE" --version
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
"$AF116_PANDOC21403" --version
"$AF116_PANDOC21403" --from=markdown --to=latex --standalone P3-original-layoutissue.md --output=P3-pandoc-diagnostic.tex
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error P3-upstream-158.tex
```

실제 명령을 확보하면 원 입력/앞 문단 제거/표 제거/표를 다른 figure로 대체한 대조를 비교하고 figure의 다음 페이지 이동, 표 유지, 페이지 본문 영역과 마지막 좌표, 패키지 판·log를 함께 기록한다. 순수 Pandoc 진단이 Quarto YAML을 재현한다고 주장하지 않는다.

**I1/I2:**7.1.1-3/-4의 바이너리·libtiff/delegate·quantum·OS, I1 당시 viewer판, I2 이전7.1.0-28와 mask 의도를 추가 확보한다. 회수된 원 파일과 raw TIFF 검사는 이미 저장돼 있으나 역사 실행과 다르다.

```sh
mkdir "$AF116_REPLAY/imagemagick-runtime"
cp "$AF116_OWN/gold-work/imagemagick/attachments/lena.png" "$AF116_REPLAY/imagemagick-runtime/"
cp "$AF116_OWN/gold-work/imagemagick/attachments/mandril3.jpg" "$AF116_REPLAY/imagemagick-runtime/"
cp "$AF116_OWN/gold-work/imagemagick/attachments/extracted/demo.tif" "$AF116_REPLAY/imagemagick-runtime/"
cd "$AF116_REPLAY/imagemagick-runtime"
"$AF116_IM7113" -version
"$AF116_IM7113" lena.png \( mandril3.jpg -colorspace gray \) -channel-fx '| gray=>meta' meta.tif
"$AF116_IM7113" identify -verbose meta.tif
"$AF116_IM7114" -version
"$AF116_IM7114" identify -verbose demo.tif
"$AF116_IM7114" demo.tif -channel-fx 'meta' extract.png
mkdir "$AF116_REPLAY/imagemagick-mask-runtime"
cp "$AF116_OWN/gold-work/imagemagick/attachments/extracted/demo.tif" "$AF116_REPLAY/imagemagick-mask-runtime/"
cd "$AF116_REPLAY/imagemagick-mask-runtime"
"$AF116_IM7114" demo.tif -channel-fx 'meta=>alpha' -alpha extract extract.png
```

마지막 I2 경로는 unspecified extra plane이 실제 원하는 opacity mask라는 전제에서만 판단한다. I1은 RGB 모든 sample·추가 plane·TIFF 태그·ICC·앱 외관을 분리하고 I2는 원 fourth plane과 추출 값·크기·방향을 대조한다. `identify`와 exit0만으로 보존 성공을 세지 않는다.

**I3:** 원첨부 HTTP/HTTPS와 배포 디렉터리의 실제 회수 실패가 기록돼 있다. **첫 행동은 `dop10rgbi_32_280_5652_1_nw_2021.jp2`의 동일 원본 또는 동일성이 입증된 배포본 회수**다. 같은 이름의 새 tile로 대체하지 않는다. 원 SHA-256, 정확한 tile의 band 정의, colr/ICC/cmap/cdef·codestream,7.1.1-6의 OpenJPEG 판과 독립 component decode가 필요하다.

```sh
"$AF116_IM7116" -version
"$AF116_IM7116" identify -verbose dop10rgbi_32_280_5652_1_nw_2021.jp2
exiftool -G1 -a -s dop10rgbi_32_280_5652_1_nw_2021.jp2
opj_dump -i dop10rgbi_32_280_5652_1_nw_2021.jp2
```

새로 회수한 원본의 별도 작업 폴더에서 실행하고 ExifTool/OpenJPEG 판도 기록한다.4components만으로 RGBA를 추정하지 않으며 ImageMagick의 identify는 독립 band 의미 증거가 아니다. 출력에서 빠진 JP2 box는 원시 dump로 보완해야 한다. 원본 부재는 소프트웨어 불가능 판정과 다르다.

## 5. 판단·근거

**이 연구는 “한 줄이 일반적으로 도움이 된다/안 된다”를 확정하지 않는다.** 원문 조건 반복 B는 A와 전 사건에서 같은 노출이었고, 새 표지 C는 두 사건의 길을 바꿨지만 완전 근거 답을 만들지 못했다. 확인된 완전 답 기회가0인 자연 분모에서 일반 성공률 개선을 계산하지 않는다. 동시에 실제 다른 경로와 교정 증인은 위치 단서가 항상 무의미하다는 일반화도 반박한다.

제품에 반환할 제안은 **위치 표지 + 판/모델/매체 범위 + 적합성을 확인할 다음 검사**를 구분하는 것이다. 이는 원장의 불일치로부터 낸 설계 가설이며 채택 관측이 아니다. D0처럼 시작 절만으로 두 사실이 충분하면 시작 링크만 반환할 수 있다. P1은 Div 표지 뒤 TOC 구성 규칙, I2는 alpha 표지 뒤 TIFF ExtraSamples·원 plane 값, I3는 원본 동일성 검사를 반드시 함께 지정해야 한다. 링크 편집자는 fragment·문서판·본문 지문·동명 표지·접근 실패를 보존할 필요가 있다.

반대 방향의 정정은 원 기록을 보존한 채 반영했다. P1의 여러 heading 일반화는 계층형 반례로 좁혔고, P2의 약어 형식을 YAML 파서와 구별했으며, I1/I2의 ‘alpha’ 보고는 실제 ExtraSamples0을 보고 unspecified meta로 정정했다. P3는 표 제거 성공을 원 목표 해결로 세지 않았고, I3는 RGBI 제품군 설명을 해당 원 파일의 검증으로 쓰지 않았다. Yale 원 편지 접근 실패, Eisenhower reading copy/press release 두 원면의 수정 흔적·도입문 차이와 실제 방송과의 일치 미확인, FDR 발행자의 식별 정정 보고도 각각 한계를 명시했다. [SELF_CHECK.md](SELF_CHECK.md) Q1–Q7에 직접 읽은 URL·절/원장 행·반증·원래/실제 분모·다음 관측이 있다.

공개 원자료와 필요한 재현용 스냅샷·짧은 검증 인용을 사용했다. 인증정보·사적 대화 원문을 결과에 넣지 않았다. 제어표·타 작업 출력은 변경하지 않았고 브랜치 통합은 하지 않았다. 현재 결과는 사용자에게 확정된 제품 채택 요구로 간주하지 않는다.

## 6. 다음 대화의 첫 행동

1. 원격 `work/research-af-res-116` 최신 SHA를 다시 읽고 마지막 커밋이 이 `HANDOFF.md` 단독 변경인지 확인한다. 결과 검사 SHA31cc와 검사 증거b816 이후 차이를 구분한다. 브랜치를 초기화하지 않는다.
2. 첫 열람 자료는 **[RESULT.md@31cc131](https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/RESULT.md)**, 다음은 같은 SHA의 [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/SELF_CHECK.md)와 [reproduce.md](https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/reproduce.md)다. 검사 수용 범위는 [acceptance@b8162d7](https://github.com/laadkke-arch/agentflow-open/blob/b8162d78efb25bf3d92bffc82498b7d00ca22c5e/docs/workstreams/research/AF-RES-116/evidence/acceptance-evidence.json)에서 읽는다.
3. 미완료 첫 작업은 **P3 실제 실행환경 또는 I3 동일 원본 중 회수 가능한 최소 입력을 얻는 것**이다. 입력 SHA·판·출처를 새 묶음에 봉인한 뒤 위 명령과 gold의 동작/보존 조건을 대조한다. 이 입력 없이 완전 gold unknown을 임의로 false/true로 채우지 않는다.
4. 한 줄 효과의 다음 연구는 두 필수 조건과 예외가 실제 예산 안에 있는 새 기회를 먼저 고정하고 독립 반복을 수행한다. 자연 여섯 사건과 이번54단계는 보존한다. 예산·시작점·허용 문서 변경은 새 protocol/별도 층이며 기존 결과 재분류로 처리하지 않는다.
5. 추가 허가를 기다리는 항목은 없다. 막힌 이유는 원 입력·역사 환경·외부 시각 증거 부족이다. 다른 세 연구의 출력·실행을 기다릴 필요도 없다. 운영 선행은 위 AF-RES-112 두 고정 SHA뿐이다.

**색인 제안 한 줄:** `AF-RES-116 | PARTIAL | Pandoc·ImageMagick 자연6·AI18꾸러미/54단계; 완전근거0, 확인된 reachable0(4불가/2미확인), 위치도달과적합성근거분리 | RESULT@31cc131279e606c9d691524525cbdbdf7dc7b44a`.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 확인된 자연 완전 답 기회는0이며 관련 절 도달이 충분한 답으로 이어지지 않았다. | P1 Shared.hs574–592와 Writers/Shared.hs429–456, reachability.jsonl; 새 예산/허용 문서를 별도 봉인. | 두 조건·필수 예외가 실제 예산 안에 보이는 자연 기회와 새 독자의 반복 선택·정답 관측이 생기면 효과 비교가 가능해진다. |
| P3 원 실행 환경과 I3 원 JP2가 없고 원격 초기 봉인 시각의 독립 원응답도 보존되지 않았다. | P3 원 command·.tex/.log·패키지 판, I3 동일 원본과 colr/cmap/cdef·tile band 정의, 보존 가능한 원 봉인 receipt. | 동일성이 확인된 입력·환경으로 기준을 완성하거나 실제 원격 전송 시각 증거를 확보하면 해당 미확인 범위가 줄어든다. |
| 한 모델 계열의 절차적 문맥 분리이며 인간 시간·채택 효과는 관측하지 않았다; 제작 노출 일부는 잘렸다. | readers의18개 events.jsonl, evaluator receipts, author-exposure.jsonl; 새 독립 반복과 비용 계측. | 완전한 제작 노출 기록과 독립 반복에서 비용 대비 근거·오확정의 차이가 재현되면 한 줄의 실용 가치 판단을 갱신한다. |
