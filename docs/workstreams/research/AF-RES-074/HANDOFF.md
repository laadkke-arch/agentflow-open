# AF-RES-074#1 HANDOFF — PARTIAL / REVIEW_READY

이 인계는 결과 본문과 검증 영수증을 원격에 저장한 뒤 작성했다. **연구 계약의 최종 판정은 PARTIAL**이다. 구조 검사 통과나 기술 대조의 성공을 실험 설계 완료 또는 사람의 질문 효과로 바꾸어 해석하지 않는다. 중앙 `dot-control.json`의 상태는 변경하지 않았다.

## 1. 식별

- 작업 ID / 시도 번호: **AF-RES-074 / #1**
- 작업 종류: **web-pro**
- 실제 모델과 실행 위치: 세션에 고지된 GPT-6 Astra Pro; 제공된 Linux cloud shell `/workspace/scratch/3ae3dbdde3fd/agentflow-open`. GitHub 읽기·커밋은 연결된 `laadkke-arch` 계정의 GitHub 도구로 수행했다. 셸 검사도 직접 실행했다.
- 공개 가능한 작업자 참조: 이 브랜치의 커밋과 아래 실행 영수증. 비공개 작업 조회 ID는 제공되지 않았으므로 만들지 않았다.
- 역할/이슈: AF-RES-074 연구 원작성·통합. Pandoc/GDAL/다른 분야별 모델 작업과 교차 점검을 사용했다. 사람 판독자·새 사람 대상 질문 실험은 **0명/0건**이다.
- 저장소/브랜치: [laadkke-arch/agentflow-open, work/research-af-res-074](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-074).
- 계획 기준 SHA: `39cadb6ecdf62d0b21c0cce67834f2aef3bf6853`.
- 실제 시작 통합 SHA: `817ee771ebfa63d4a177ee12f46b9818a6335308`. 계획 SHA와 같다고 처리하지 않았다.
- **고정 연구 결과 SHA (C07)**: `34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9`.
- **검증 영수증 SHA (C08)**: `64bfa361e1306a96af434e7deeaea3f519562e3a`. C07 이후에는 `COMMITS.csv`와 검증 영수증 4개만 바뀌었다. RESULT·핵심 원장·수용 기록은 C07과 동일하다.
- 마지막 실제 계약 검사 SHA: C07. 검사 시 작업 트리는 깨끗했고 종료값은 0이었다.
- 이 인계 작성 전에 원격에서 읽은 마지막 저장 SHA: C08. 이 파일을 추가하는 **마지막 단독 커밋**은 자기 참조 SHA 대신 Git 이력에서 확인한다.
- 마지막 실제 진행 증거: C07 핵심 18파일을 GitHub에서 다시 받아 정확 바이트·Git blob SHA를 대조한 `evidence/remote-readback.json`, 확인 시각 **2026-11-23T10:58:56.780785+00:00**. 그 영수증 자체도 C08의 GitHub 파일로 재열람했다.
- PR 주소: 생성하지 않았다. 작업 브랜치에 커밋했다.
- 인계 최종 점검 시각(UTC): **2026-11-23 11:04:33 UTC**.
- 작업 인계 상태: **REVIEW_READY**. 연구 수용 상태: **PARTIAL**. 중앙 DONE과는 별개다.

고정 결과는 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/SELF_CHECK.md), [수용 기록](https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/evidence/acceptance-evidence.json)에서 읽는다.

## 2. 사용자 요구/작업 범위

목표는 부분 설계·목적만으로 A의 한 링크/근거 있는 보류, B의 두 조건부 링크, C의 한 필드 질문 중 어느 답이 기술적 선택과 사용자 다음 행동을 지원하는지 비교하는 것이다. 자연 모집과 구성한 기술 대조는 별도 집계했다. C의 값①·값②·무응답은 모두 가상 분기이며, 나중 작성자 발언은 별도의 사건 원장에 두었다.

시작 때 GitHub에서 실제 통합판의 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, `docs/automation/dot-control.json`의 자기 항목을 확인했다. 계획판 [RESEARCH_BRIEF.md](https://github.com/laadkke-arch/agentflow-open/blob/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853/docs/product/RESEARCH_BRIEF.md)와 workflow/상태 형식도 대조했다. 실제 시작판 원문 묶음은 [817ee77의 저장소](https://github.com/laadkke-arch/agentflow-open/tree/817ee771ebfa63d4a177ee12f46b9818a6335308), 읽은 원문·판·시각은 `evidence/intake.json`과 `evidence/context-sources.jsonl`에 있다.

유일한 결과 의존은 **AF-RES-070@1a92715786d444f57976082329470a24e2a291b6**다. [070 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/1a92715786d444f57976082329470a24e2a291b6/docs/workstreams/research/AF-RES-070/HANDOFF.md), [070 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/RESULT.md), DATA_DICTIONARY를 선행 결론으로 사용했다. 070의 같은 사건과 질문 효과를 재계수하지 않았다. 다른 PLAN#18 작업은 기다리지 않았다.

유일한 쓰기 경로는 `docs/workstreams/research/AF-RES-074/`다. 다른 세션의 작업 트리·운영 환경을 변경하지 않았다. 중앙 상태·제품 코드·다른 연구 결과는 수정하지 않았다. 새 사람에게 메시지·질문·설문을 보내지 않았다.

### 묶음별 실제 커밋

| 묶음 | SHA | 저장한 결과 |
| --- | --- | --- |
| C01 | 1039968098a103da14a7a9bd77572e8148d6fd58 | 모집 규칙·실제 시작 SHA·계약 |
| C02 | 6a5dda48cc91acd5b3c88c84f32d8108637029ea | Pandoc 자연 요청·선택 필드·답안의 댓글 전 봉인 |
| C03 | 0eb5235cd8f0f3d5ec3bfb92022990ee713d7d1c | GDAL 자연/대조 봉인; Pandoc 대조의 사후 노출 고지 |
| C04 | 4356f70e550fc139f2f4aa0fb3bc2fa548693d68 | 모집·답안의 공통 원장; 다른 분야 원저작·초기 점검 |
| C05 | a884833dccd1ce3b17a1ff1d8bf3e0f3a2a8c932 | 공식 시험·기술 원문·나중 발언; GDAL3.10.3 실행물 |
| C06 | d3e0410a6164909110621092a2798a3a73846c12 | 판정·반례·48건 모집; 최초판 8건 회수; Pandoc 고정판 실행 |
| C07 | 34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9 | 필수 3표·Q1–Q8·SELF_CHECK·수용 기록·재현 입력 |
| C08 | 64bfa361e1306a96af434e7deeaea3f519562e3a | C07 계약 검사·1,441 검산·GitHub CI·18파일 원격 대조 영수증 |

이 문서는 위 묶음 이후 `HANDOFF.md` 한 파일만 바꾸는 마지막 커밋으로 제출한다. 운송용 캐시·다운로드 바이너리·임시 복원 파일은 결과로 세지 않는다. 필요한 입력과 출력 바이트·명령·해시·영수증은 커밋된 파일에 들어 있다.

## 3. 실제 변경

| 파일 | 변경 사항/이유 | 어떻게 확인했나 |
| --- | --- | --- |
| SCOPE.md, manifest.json, frame.csv | 두 저장소의 고정 검색 묶음, 숫자순 첫12와 다음12, 제외·중복·판 상태; 실제 시작판·허용 경로·고정 의존 | 48행=저장소별24행; 선택은 처음의 4건씩 유지; session check 종료0 |
| packets.jsonl, policies.csv | 자연8·대조4의 목적·필드·두 후보·노출; 3정책×3응답=108답안 | 봉인4파일을 C02/C03 바이트와 대조; 모든 분기·키 검사 |
| criteria.csv, initial-version-review.csv | 12요구의 기술 기준; 최초 요청8건의 event ID/URL/해시·현재판 비교 | 8/8 사후 복원, 6건 바이트 일치·2건 표현/서식 차이·목적 변화0 |
| events.csv, sources.jsonl | 35사건과 직접 읽은 166접근 기록; 원저작·판·한계·반례·최소량 산입 사유 | 원저작 65건을 지정4범주로 보수적으로 산입; 재열람·댓글·판·중복은 추가 저작으로 세지 않음 |
| scores.csv, policy-summary.csv, costs.csv | 108판정·18집계·12비용 행; 기술 가능성과 관측 사용 효과의 분모 분리 | 분자/분모·열 수·연결 키·무응답/미측정/접근 실패를 검산 |
| RESULT.md, SELF_CHECK.md, DATA_DICTIONARY.md | 첫3필수 표, Q별 답·반증, 의미 교정, 마지막 약점3건 | 원장 기반 생성·모델 교차 판독·표 열 검사 |
| evidence/acceptance-evidence.json | 충족/부분/미달과 당사자 자료 결손; 중앙 DONE 불변 | 연구 PARTIAL과 구조 PASS 구분 |
| REPRODUCE.md, tools/, 실행 evidence | Pandoc 고정판·GDAL 현재판 실행과 재현 입력; 미실행3.2.1 명령 | 실제 stdout·exit·SHA·base64 TIFF 복원 검사 |
| evidence/session-check.json, validation.json, github-ci.json, remote-readback.json | C07을 대상으로 한 실제 주체·시각·SHA·종료값·원격 일치 | 아래 검증 결과; C08에 저장 |

### 최소량과 표의 분모

- 직접 열어 읽고 지정 최소량에 산입한 독립 원저작은 **65건**이다: 요청 **43**, 공식 시험/예제 **8**, 명세/매뉴얼/지원 공지 **7**, 다른 분야 업무 절차 **7**. 추가 구현 코드 6건은 이 최소량65에서 뺐다.
- 166은 접근 기록 행 수다. 원저작 수가 아니다. 실패 시도12행에는 나중에 회수한 최초판8건의 초기 실패도 포함한다. 이를 현재 미확보 사례12건으로 쓰지 않는다.
- 자연 표본 **8건**, 별도 대조 **4쌍(양성2·음성2)**. 같은 사건의 자연/대조 중복 산입은 없다.
- 원장 **12×3×3=108행**은 표본108명이나 실사용108회를 뜻하지 않는다.
- 자연군의 최초판은8건 모두 얻었지만, 선택 필드 양값의 독립적인 전체 목적 정답이 갖춰지지 않아 엄격한 질문 정오 변화의 분모는 **0**이다. 성공률 0%라고 계산하지 않는다.
- 자연군에서 관측한 새로운 사전 선택 필드 값은 **0건**, 별도 독립 사용 성공 관측도 **0건**이다. 다른 필드 공개와 해결 보고가 같은 발언에 들어 있는 사례는 **1건**이며 둘로 세지 않았다. 실행 의향 발언2건은 성공 증거가 아니다.
- 사람의 A/B/C 선택·소요 시간·응답 확률은 **미측정**이다. 공개되지 않은 값을 부정값으로 대입하지 않았다.

## 4. 실제 검증 결과

### 4.1 계약·원장·원격 저장

실제 시작 명령은 다음과 같으며 종료값0이다. `evidence/session-start.json`에 실제 checkout·base·주체가 있다.

```bash
python -B -m workbench.session start af-res-074 --allow docs/workstreams/research/AF-RES-074/ --dependency work/research-af-res-070=1a92715786d444f57976082329470a24e2a291b6 --output docs/workstreams/research/AF-RES-074/manifest.json --fetch
```

결과 C07을 원격에서 가져와 작업 트리가 깨끗한 상태에서 다음을 수행했다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-074/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-074/tools/validate.py --require-expanded --actor 'root model in supplied cloud shell'
```

계약 검사는 **2026-11-23T10:55:43–10:55:54Z, 종료0, passed, remote_checked**였다. 검사 중 보인 최신 통합판은 `4d5185e75e52f405bfa7d149c32a0cd135395bbd`이고, 내 작업 base는 처음의817ee77로 유지됐다. 경로 이탈·미병합 경로·오류는 모두 빈 목록이다. [session-check.json](https://github.com/laadkke-arch/agentflow-open/blob/64bfa361e1306a96af434e7deeaea3f519562e3a/docs/workstreams/research/AF-RES-074/evidence/session-check.json)에 전체 stdout/종료값을 보존했다.

연구 검산은 **2026-11-23T10:56:10–10:56:11Z, 종료0, 1,441개 통과, 오류0·경고0**였다. 검사 소스 HEAD는C07이다. 행/열·중복·키 조인·분모·봉인·아티팩트 해시·실행 stdout·최초판 원장·표 연결을 검사했다. 구조 PASS는 연구 PARTIAL과 동시에 성립한다. 검사 작성자는 Pandoc 모델 작업자이고 실제 최종 실행자는 root 모델이다. 사람 독립 검증으로 부르지 않는다.

GitHub의 [Collaboration contract / run45160415879](https://github.com/laadkke-arch/agentflow-open/actions/runs/45160415879)는 C07 push에서 **completed/success**였다. 실행 범위는 `python -m workbench.session check-all --fetch`이며, 연구 fixture 실행이나 전체 제품 시험을 수행한 CI라고 주장하지 않는다.

검증 영수증만 추가한 C08의 [동일 계약 CI / run45161068144](https://github.com/laadkke-arch/agentflow-open/actions/runs/45161068144)도 completed/success를 직접 확인했다. 연구 원장 검산의 고정 대상 SHA는 여전히C07이다.

C07의 RESULT·SELF_CHECK·REPRODUCE·manifest·핵심 원장·수용/집계·핵심 실행물 **18파일**을 GitHub에서 명시적 SHA로 다시 열었다. 받은 base64를 디코딩해 로컬 `git show C07:path`와 정확 바이트 비교하고 Git blob SHA도 직접 계산했다. **18/18 일치**, CSV·JSONL·JSON 파싱도 통과했다. [remote-readback.json](https://github.com/laadkke-arch/agentflow-open/blob/64bfa361e1306a96af434e7deeaea3f519562e3a/docs/workstreams/research/AF-RES-074/evidence/remote-readback.json)이 각 파일의 URL·길이·해시·행 수를 고정한다.

초기 셸 push는 자격 증명 부재로 종료128이었다. 자동 승인 거부가 아니었다. 이미 연결된 GitHub 도구로 tree/commit을 만들고 해당 브랜치만 expected-SHA 조건으로 갱신했다. 이후 fetch가 끝난 다음 같은 tree에 soft reset하여 로컬을 맞췄다.

### 4.2 기술 실행

**Pandoc2.11.3.2**: 공식 source `dcbd8d326cce4960e0d736e25e7d00f9057a1fc2`, 공식 릴리스 바이너리로 `parse-raw`, `sloppypar`, `empty_paragraphs`의8 fixture/12 process를 직접 실행했다. **전부 exit0, 기대 stdout 정확 일치**다. 마지막 LF를 제외한 논리적 입력 해시와 실제 stdin/stdout 바이트 해시를 혼동하지 않았다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/run_pandoc_fixed.py --binary docs/workstreams/research/AF-RES-074/evidence/runtime/pandoc-2.11.3.2
```

- 바이너리 SHA256: `762b2b574da6b7da29af1cb13eaeb5d3974a92b10e3d7a1e4ff6614ee5ec4d9b`.
- 공식 배포 자산: https://github.com/jgm/pandoc/releases/download/2.11.3.2/pandoc-2.11.3.2-linux-amd64.tar.gz
- 입력/기대/명령은 `evidence/pandoc-fixed-fixtures.json`, 실제 argv·stdout·exit·해시는 `evidence/pandoc-fixed-run.json`.
- 이는 **이번 세션에서 해당 과거 릴리스를 실행한 영수증**이다. 과거 날짜의 upstream CI 결과가 아니다.

**GDAL3.10.3**: 5개 명령을 직접 실행했고 모두 exit0이다. 고정3.2.1의 원본 입력·reference와 현재판 실행을 구분했다. nearest checksum18784; bilinear19664, reference19694이나 최대 픽셀 차이1로 공식 tolerance를 충족했다. 두 `outsize` 표현은 실제 현재판에서 픽셀·변환·파일 바이트가 같았다. 체크섬 동일/상이만으로 전체 배열 동일/상이로 판단하지 않았다.

- 고정3.2.1 source: `258d73a17b1f7e93c9cf9b60a2411545d51879de`.
- byte.tif SHA256: `59ed6e9dd19291bbdc230092ab7f6bc46fb0537ee4c9eec15dd58021cd9c12be`.
- bilinear reference SHA256: `fbbd267d5c6d5cc0a57e902f81c16fc1123799defa43192680fad88ec99be113`.
- 실행 영수증: `streams/gdal/researcher-run3103.json`.
- 원본·reference·현재판 실행물 **7파일/11,530바이트**를 `evidence/gdal3103-artifacts.json`에 저장했다. 복원 도구를 실제 실행해7개 모두 길이/해시 확인, 종료0이었다.
- **GDAL3.2.1 바이너리는 실행하지 않았다.** 현재판 결과를 고정3.2.1의 실행으로 바꾸어 적지 않았다.

다른 모델의 교차 판독은 실제로 있었다. `streams/crossfield/audit-*.json`에 원문·픽셀·원장·최초판 차이·보고서 교정을 남겼다. 공유 문맥을 가진 비맹검 모델 점검이며 통계적으로 독립된 사람 판정이 아니다. 같은 작성자의 재열람은 자체 점검으로 분류했다.

마지막 인계 초안도 crossfield 모델이 파일을 수정하지 않고 원장·영수증·Git 이력과 대조했다. 원저작/행 수, C07/C08 부모·변경 범위, 검사 종료값과 범위, 미실시 명령의 경로·입력, PARTIAL 이유에서 실제 수치·주장 오류를 발견하지 못했다고 회신했다. 이 추가 점검 역시 비맹검 모델 검토다.

### 4.3 미실시 명령과 정확 입력

미실행의 직접 이유는 이 환경의 GDAL이3.10.3이고3.2.1 실행물·Docker/Podman이 없다는 것이다. 최소 추가 입력은 작동하는 **GDAL3.2.1의 gdalinfo/gdal_translate/gdalwarp 경로와 연결된 PROJ·드라이버 버전 정보**다. 입력 raster는 이미 커밋돼 있다. 아래는 저장소 루트에서 실행할 정확 명령이며, `AF074_GDAL321_BIN`만 실제 경로로 바꾸고 비어 있는 새 출력 디렉터리를 사용한다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/restore_gdal_artifacts.py
AF074_GDAL321_BIN=/absolute/path/to/GDAL-3.2.1/bin
AF074_INPUT=docs/workstreams/research/AF-RES-074/evidence/runtime/restored-gdal3103/byte-input.tif
AF074_OUTPUT=docs/workstreams/research/AF-RES-074/evidence/runtime/gdal321-new-run
mkdir -p "$AF074_OUTPUT"
"$AF074_GDAL321_BIN/gdalinfo" --version
"$AF074_GDAL321_BIN/gdal_translate" -a_srs EPSG:26711 -gcp 0 0 440720.000 3751320.000 -gcp 20 0 441920.000 3751320.000 -gcp 20 20 441920.000 3750120.000 0 -gcp 0 20 440720.000 3750120.000 "$AF074_INPUT" "$AF074_OUTPUT/gcp.tif"
"$AF074_GDAL321_BIN/gdalwarp" -ts 40 40 -rn "$AF074_OUTPUT/gcp.tif" "$AF074_OUTPUT/nearest.tif"
"$AF074_GDAL321_BIN/gdalwarp" -ts 40 40 -rb "$AF074_OUTPUT/gcp.tif" "$AF074_OUTPUT/bilinear.tif"
"$AF074_GDAL321_BIN/gdal_translate" -outsize 40 40 "$AF074_INPUT" "$AF074_OUTPUT/pixels.tif"
"$AF074_GDAL321_BIN/gdal_translate" -outsize 200% 200% "$AF074_INPUT" "$AF074_OUTPUT/percent.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/nearest.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/bilinear.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/pixels.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/percent.tif"
```

nearest/크기 두 표현의 공식 기대 체크섬은18784, bilinear는 저장 reference와 최대 픽셀 차이≤1이다. 전체 파일 동일성은 별도로 비교한다. 실제 UTC·버전·명령·exit·입출력 바이트와 해시를 새로운 영수증에 기록한다. 자세한 fixture와 자연8건의 추가 최소 입력은 [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/REPRODUCE.md)에 있다.

## 5. 판단·근거

### 5.1 현재 지지되는 결론

**기술적으로 값을 구분할 수 있다는 사실만으로 질문 한 왕복이 필요하다고 결론낼 수 없다.** 두 값이 같은 목표 행동을 허용하는 음성 대조에서는 공통 행동을 주면 된다. 두 행동이 달라도 사용자가 자신의 조건을 식별할 수 있고 두 조건이 같은 구성·판의 근거에서 확인되면 B가 바로 실행 가능한 조건부 답이 될 수 있다. 반대로 사용자가 모르는 datum 같은 사실, 실행환경이 결정하는 값, 다른 단계의 제약은 짧은 질문 하나만으로 해결되지 않는다.

대조4쌍×알려진2값의 **정책별8개 기술 시나리오**에서 A는 단일 정답5·오답1·보류2, B는 단일 정답4·조건부 사용 가능4, C는 응답 뒤 단일 정답8이었다. C의8은 실제 응답률이나 인과 효과가 아니며, 음성2쌍에는 그 질문이 필요하지 않았다. 무응답은 별도 층으로 남겼다. B의 조건부4도 실제 독자의 조건 식별 성공을 관찰했다는 뜻이 아니다. 자연군에서는 이 표를 성공률로 이식하지 않았다.

최초 결론에 대한 반례를 찾아 반영했다.

- **PAN-N2**: “중국어 따옴표/서양 글꼴 결과를 유지하고 싶다”를 “전역 lang 키를 반드시 유지해야 한다”로 읽었던 사전 추론을 철회했다. 원문은 다른 해결책을 허용한다. 봉인 답안은 지우지 않고 RESULT 표2의 해당9셀에 철회 사실을 표시했다.
- **GDAL-N2 / #3378**: 선택한 ENVI magic보다 `GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR`가 실제 실패를 설명한 반례다. 작성자의 다른 필드 공개와 해결 보고가 같은 발언이므로 독립 성공2건으로 세지 않았다.
- Pandoc `empty_paragraphs` 시험은 reader와 writer 설정을 함께 맞춰야 하는 경우를 보였다. 한 단계·한 필드 충분성 주장을 제한한다.
- RUSA·LOC·NOAA NCAT·Ordnance Survey·Esri·USPS의7개 업무 원저작은 값의 소유자, 자동 추론/기본값, 둘 다 유효하거나 순차적인 방법, 미완료 상태의 다음 행동을 비교하는 데 사용했다. 실제 서비스 이용자의 시간·응답 확률이나 거래 성공을 관찰했다고 주장하지 않는다.

각 근거의 원 출처·도착 URL·확인 UTC·판·읽은 절·한계·Q 연결은 `sources.jsonl`에 있다. 기술 source는 판 고정 GitHub 원문, 현재 서비스 절차는 확인 시점 원문이다. 원문·공식 기대값·오늘의 실행·모델 추론·실제 후속 발언을 구분했다.

### 5.2 Q별 인계 상태

| 질문 | 수용 상태 | 답과 남은 범위 |
| --- | --- | --- |
| Q1 | 조건부 충족 | 자연8건 최초 event와 현재판 비교 완료. 회수는 사후이므로 봉인 전 판독으로 소급하지 않음; 정확 첨부/전체 목적 시험은 남음 |
| Q2 | PARTIAL | 사전 필드·두 값·후보·답안은 보존했으나 예산·질문/조작 필드 동일성·사전 노출·판 혼합 결함이 있음 |
| Q3 | 기술층 조건부 충족 | 양성2·음성2, 고정 입력/기대/현재 실행을 구분. Pandoc 고정판 실행; GDAL3.2.1은 미실행 |
| Q4 | 설계층 조건부 충족 |108답안, 단일/조건부/나열/오답/보류 분리. 실제 독자 선택은 미측정 |
| Q5 | 범위 내 충족 | 이미 목적이 알려진 자연3건·공통 행동 음성2쌍과 미확인5건을 구분. 미공개 값을 부정으로 대체하지 않음 |
| Q6 | 관측 범위 충족 |35사건의 작성자/제3자·새 값·의향·사용 결과 분리. 새 선택필드0·독립 성공0·다른 필드 해결보고1 |
| Q7 | 충족 | 다른 필드, reader/writer 상호작용, 혼합판, 비배타 대안 반례를 직접 비교 |
| Q8 | 설계 비용 조건부 충족 |12요구별 링크/문서/행동/계획 왕복 비교와7개 타 분야 업무. 실제 시간·확률·A/B/C 사용자 선택은 미측정 |

미확인 자연 효과나 새 사람 실험의 부재만으로 PARTIAL을 붙인 것이 아니다. 사용자는 자연군의 공석·미응답·미확인 보존을 허용했고 새 사람 실험을 제외했다. **아래 실험 설계 조건 미달이 현재 완료를 막는 이유다.**

| 가장 중요한 불일치·약점 (정확히3건) | 다음 조사·필요 입력 | 판단이 바뀔 관측 |
| --- | --- | --- |
| Pandoc의 공통 문서/지정절 예산을 초과한 판독 | 새로운 미노출 입력에서 후보별 문서2·문서별 지정절1을 먼저 봉인; 추가 원문은 별도 층에만 기록 | 허용 노출만으로 두 조건과 행동을 판별하는 답이 재현됨 |
| PAN-C1의 질문은 원하는 보존 결과이고 조작값은 raw_tex 설정인 매핑 불일치 | 질문하는 바로 그 필드의 두 값이 동일 입력·같은판 행동을 가르는 새 대조를 사전 고정 | 같은 필드 값만 바꾸어 정답이 바뀌며 다른 목표/설정 매핑을 요구하지 않음 |
| Pandoc 기대 출력 선노출·음성 equality scan과 GDAL-N3 후보 판 혼합 | 미노출 입력/판독자를 사용한 별도 반복과 동일 SHA 후보; 역사판 실행물은 위 정확 명령으로 추가 | 댓글/기대 이전의 새 봉인 영수증, 같은판 후보·독립 양값 결과, 별도 실행 영수증이 갖춰짐 |

사용자 확정 요구는 모집·범위·예산·기록·비개입·최종 인계 조건이다. 위 질문 정책의 적용 조건과 후속 반복 설계는 연구자의 판단이다. 기존 봉인 파일을 수정해 처음부터 지킨 것처럼 만들지 않는다. 중앙 상태·다른 작업 결과의 변경은 이 결과에 포함되지 않는다. 입력 중 우연히 보인 서비스 키는 공개 결과에 복사하지 않았으며, 원문 식별·요약·해시만 남겼다. 새 유료 자원·운영 배포는 사용하지 않았다.

## 6. 다음 대화의 첫 행동

1. `work/research-af-res-074`의 최신 SHA와 이 HANDOFF, 이슈/PR 유무를 GitHub에서 재조회한다. 새 채팅이 이 파일을 기억한다고 가정하지 않는다.
2. 마지막 실제 검사 대상 **C07=34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9**와 최신 변경 파일을 비교한다. C08은 검증 영수증, 그 다음 커밋은 HANDOFF 한 파일이어야 한다. 이후 누군가 결과를 바꿨으면 그 SHA를 새로 검사한다.
3. **재개할 첫 구체 작업은 Q2의 별도 반복을 위한 미노출 패킷 봉인**이다. 최소 입력은 댓글·정답·기대 출력을 아직 읽지 않은 공식 입력 하나, 질문과 조작이 동일한 필드/두 값, 같은 SHA의 두 후보 원문, 각 후보에 허용한 문서·지정절이다. 새 판독자는 이 허용 패킷만 읽고 A/B/C와 세 응답 분기를 먼저 커밋한다. 기존 8자연 요청을 새 모집으로 다시 세거나 기존 봉인을 교체하지 않는다. 재개 식별자는 `AF-RES-074/Q2-replication`; 입력 기준은C07/C08과 위 새 패킷이다. 기대 결과는3가지 미달 조건을 충족하는 별도 원장이지 과거 기록의 정정 삭제가 아니다.
4. GDAL 역사판 실행을 보강하려면 **3.2.1 바이너리 경로·PROJ/드라이버 정보**를 확보한 뒤 §4.3의 정확 입력/명령을 실행한다. 새 source SHA·실행 주체·exit·출력 바이트를 기록한다. 자연 사례의 전체 목적 판정은 REPRODUCE §6의 사례별 입력이 있을 때만 추가한다.
5. 새 사람에게 질문하는 실험은 포함하지 않는다. 필요한 승인 요청은 현재 없으며, 기존 저장소 읽기·허용 경로 기록·커밋 권한으로 이어갈 수 있다. 새 운영/유료/대인 작업을 이 인계에서 추가 승인한 것으로 해석하지 않는다.
6. 다른 세션의 유일한 결과 의존은 고정 AF-RES-070@1a92715786d444f57976082329470a24e2a291b6이다. 다른 PLAN#18 결과를 기다리지 않는다. 연구 완료 판정과 중앙 DONE 변경을 분리한다.

**현재까지의 자료·실행·검사는 위 범위로 재개 가능하다. 완료 판정을 위해서는 기록된 미달 조건에 맞는 새 입력·봉인·판 고정 증거가 필요하다.**
