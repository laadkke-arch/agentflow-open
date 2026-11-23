# AF-RES-070#1 HANDOFF

## 1. 식별

- 작업 ID / 시도: **AF-RES-070#1**.
- 작업 종류: web-pro; 공개 OSS 이슈의 부분 설계 요청에서 사전 선택한 한 필드의 판별 가능성 연구.
- 역할: 주 연구/통합·검산, rclone·ripgrep·pandoc 병렬 판독과 상호 검토. 실제 새 사람에게 질문·연락·댓글을 보낸 수는0.
- 환경에 표시된 모델: GPT-6 Astra Pro. 실행 cwd: `/workspace/scratch/f1ffe17c302f/agentflow-open`.
- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-070`.
- 계획 기준: `320424d87f99e70c42eeb8cb7211467de27f2c2e`.
- 실제 시작 통합판·계약 base: `76b8c1d15812fbf91b879f8444fd188ae7445802`.
- 인계 직전 마지막 결과/검증 커밋: **`30266f9354134b7aad33596b0acb96209876ce7d`** (C06, 2026-11-23T09:29:05Z).
- 원격에서 완전 본문으로 재열람한 결과 SHA: **같은 C06**.
- 마지막 실제 진행 증거: GitHub 고정SHA 파일18개 완전 본문 일치(2026-11-23 09:29:37 UTC), 원격에서 fetch한 Git tree의144파일 blob 일치(2026-11-23 09:32:15 UTC), C06 계약 check PASS(2026-11-23T09:29:54.522401+00:00).
- PR: 만들지 않음. 작업 브랜치에만 묶음별 커밋.
- 최종 확인 기준 UTC: 2026-11-23 09:32:15 UTC.
- 상태: **PARTIAL**. 기록·원격 검증·인수 절차는 마쳤으나 엄격한 연구 효과 판정의 완료 조건은 충족하지 못했다.
- 이 파일 자체의 commit SHA는 파일이 들어 있는 마지막 커밋 헤더로 확인한다. 자기 SHA를 본문에 재귀적으로 넣지 않는다. 아래 C06은 HANDOFF를 제외한 완전한 결과 스냅샷이다.

## 2. 사용자 요구와 작업 범위

목표는 처음 요청의 목적·인접 단계·금지조건·실행 설정 중 한 필드만 더 알면 같은 두 후보의 권고가 달라지는지를, 새 공개 이슈와 해당 판의 독립 문서/코드/원시험으로 구분하는 것이었다. 입력 폼 또는 질문 정책의 채택을 미리 정하지 않았다.

읽은 기준은 실제 통합판의 AGENTS.md, STATE.md, RESEARCH_BRIEF.md, RESEARCH_WORKFLOW.md, DOT_AUTOMATION.md와 dot-control의070 항목이다. planning 인수는 `work/planning@e4c6a79`의 REVIEW-16이고, 유일 결과 dependency는 **AF-RES-066@`367f29c6eb8f3da36c7728eb133f1cca9078efbf`**의 HANDOFF·RESULT다. 066의 완전 검증0건을 실제 지지0으로 해석하지 않았고, 그 상식 문항·링크를 재감사하지 않았다. 069·071·072 결과는 인수하지 않았다.

쓰기 범위는 **`docs/workstreams/research/AF-RES-070/`만**이었다. 중앙 dot-control.json, 타 작업 브랜치, 계정·유료 API·외부 댓글은 변경하지 않았다. Git 계약과 최종 tree가 이 범위를 확인한다. 공개 원문 전체 임시 캐시는 커밋된 산출물이 아니며 결과의 수량에 추가하지 않는다. 공개 원장은 최소 발췌·원위치·SHA256·opening event 위치로 재개할 수 있게 남겼다.

## 3. 실제 변경과 파일

아래 링크는 전부 결과 SHA C06에 고정한다. `streams/`는 각 조사자의 봉인 A·후속 원장·기록된 오류/시정, `evidence/`는 실제 검증 영수증, `tools/`는 원장 병합·검산·원문 회수 도구다. 전체144파일의 경로·blob hash는 마지막 목록에 있다.

| 파일 | 변경 사항·이유 |
| --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/RESULT.md) | 필수표1·2a/2b·3, 관측 결론, Q1–Q8, 보존 대상 비교, 반례, 약점 정확3 |
| [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SCOPE.md) | 모집·A/B·판·예산·계보·분모 규칙의 최초 사전 커밋 |
| [manifest.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/manifest.json) | 실제 통합판76b8c1d와 유일 dependency066의 작업 계약 |
| [ENROLLMENT.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/ENROLLMENT.csv) | 64개 모집 순번·큐·진입/탈락·최초판 복구·선정12+12 |
| [EVENTS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/EVENTS.csv) | 원글24+댓글103=127개; actor ID·UTC·위치·해시·선후 |
| [VIEWS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/VIEWS.csv) | 24건의 A/B48행; 한 필드·값·가린 정보·같은 후보 |
| [OUTCOMES.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/OUTCOMES.csv) | case24 및 별도 비교/반사실11=35행; 효과/방향/성공/분모 분리 |
| [SOURCES.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SOURCES.jsonl) | 253개 출처/접근 행; 원저작87개=이슈63+공식24; 주장 범위와 한계 |
| [PINS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/PINS.csv) | 48후보에66개의 고정SHA·지정 절 연결; 실제 예산 이탈 구분 |
| [PAIRS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/PAIRS.csv) | 비교 후보10쌍; 기술적 미응답 대비1, 정확 동작 정보무효짝0 |
| [Q_CHECK.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/Q_CHECK.csv) | Q1–Q8별 결과행·근거 절·반례·미확인 재개 자료 |
| [SEARCHES.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SEARCHES.jsonl) | 8개 실제 검색식·UTC·정렬·반환순서 |
| [CASES.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/CASES.json) | 통합 판독24건; body hash·봉인·후속 원행 참조 |
| [COMMITS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/COMMITS.csv) | C01–C05 실행된 묶음; C06은 이 인계문에 추가 고정 |
| [DATA_DICTIONARY.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/DATA_DICTIONARY.md) | 수량/최초판/질문 분모/관측0·미측정·빈 분모 해석 |
| [INTAKE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/INTAKE.md) | 필수 기준 문서와066·planning 인수 및 실제 통합판 |
| [REVIEW.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/REVIEW.md) | 독립 판정 검토, 철회·조건 한정, 최종 원고 점검 |
| [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/REPRODUCE.md) | 미실시 역사적 실행의 판·환경·명령·입력; 최초판 복구 |
| [VALIDATION.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/VALIDATION.md) | 실제 명령·cwd·대상SHA·종료코드·실패/시정·원격 검증 |

## 4. 실제 확인된 결과와 미확인

**원자료 수:** 공개 이슈64개에 접근했다. 실질적으로 읽은63개 이슈와24개 공식 원저작을 산입해 **87개 원저작**이다. 동일 이슈 댓글·GH Archive 사본·같은 매뉴얼의 다른 판을 별개 원작으로 부풀리지 않았다. jq2329는 긴 설치 로그의 일부만 읽어 최소량에서 제외했다.

**모집:** 초기8개×4저장소=32개, 적격31개에서 주3개×4=12슬롯을 고정했고 공석은0이다. 각 저장소 다음8개씩도 순서대로 읽어 진단12개를 별도로 봉인했다. 최초 본문은56/64개를 복구했으며 주12·선정 진단12는 모두 복구됐다. ripgrep 확장8개는 현재 본문만 있어 시간순 최초판 분석에 넣지 않았다.

**판독 결과:** 새 B1건(RG1840), 중복 B2건(RG1808·jq2349), B 없음/불확정21건이다. 새 B는 조건부 후보를 좁힌 사례이며 A의 오답이 B에서 정답으로 바뀐 엄격 개선은 아니다. 중복2건도 엄격 정답 동일로 세지 않는다. **엄격 효과 판정 분모0, 효과율 N/A**다. 개별 미확인 행에0효과를 대입하지 않았다.

**질문:** 연구자가 봉인 보기에서 제안한 질문8개, 생략16개다. 제안8개 중 독립 코드 조건으로 판정 가능한 기술층2개에서 오탐0/2다. 두 행 모두 실제 열람 예산 이탈을 포함하므로 엄격 통제 결과가 아니다. 엄격 예산 준수층의 오탐 분모는0/N/A다. 남은6건을 무응답 때문에 오탐 분모로 넣지 않았다. 실제 새 질문 발송은0건이며 질문 비용은 미측정이다.

**후속 관측:** jq2349는 별개 OP의 작동 보고, jq2394는 명령·출력과 별개 해결 보고, RCL4914는 수정 beta·다른 OS의 성공 로그가 있다. 이들을 한 필드 질문의 인과효과로 만들지 않았다. RG1840 B와 같은 댓글의 성공 표현은 독립 성공 증거로 재사용하지 않았다. PAN7113의 다른 필드 반례가 설명을 바꾼 실제 사건도 보존했다.

**반례와 시정:** RCL4911에서 전체 전송 종료와 개별 버퍼 종료를 같은 조건으로 취급한 오탐1/1 판정을 철회했다. jq2349의 무키 원소가 하나인 축소 예에서는 두 알고리즘이 같은 결과를 낼 수 있다. PAN7003의 앞 단계 파일 생성, RCL4912의 검증 필요, jq2406의 빌드 설정은 선택한 필드만으로 충분하다는 주장에 대한 반례다.

**미실시/미확인:** 역사적 제품 바이너리 실행·완전 환경 재현, 새 사람의 질문 실험, 질문 비용, 완전한 실사용 성공, 정확 동작의 정보 추가 무효 짝은 확보하지 못했다. 후대 원문/제목/댓글 선노출과 실제 추가 절 열람을 보존했고, 두 요건을 함께 충족한 packet은 주2·진단5뿐이다. 공개 실패 접근5건의 정확 UTC는 복구하지 못했다. 이를 이유로 PARTIAL을 유지한다.

## 5. 실제 검증과 증거 수준

- 작업 계약 start는 exit0으로 manifest를 만들었다. 기존 계약의 base·dependency를 바꾸지 않았다.
- 원장·RESULT 검사: `python -B docs/workstreams/research/AF-RES-070/tools/validate.py`, cwd 위 저장소 루트, 대상C05 `f2e13005ff9e0ef8fe307ed48f2d13fbeba1dedc`, exit0, **646개 검사 통과**. 결과 파일별 SHA256은 [evidence/validation.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/evidence/validation.json)에 고정돼 있다.
- 독립 원장 감사는 첫 exit1의 발견과 시정을 남기고 최종 exit0을 얻었다. 별도 판정 검토37개도 통과했다. 문서 근거의 허용 범위와 같은 B 문장의 결과 재사용 여부는 독립 검토자가 원문과 대조했다.
- C02/C03 봉인 파일21개를 각 원격 고정SHA에서 재열람해 실제 바이트의 blob SHA와 모두 일치함을 확인했다. [evidence/seal-verification.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/evidence/seal-verification.json).
- C05에서18개 표/원장/설명 파일의 GitHub 본문을 재열람한 영수증은 [evidence/remote-result-c05.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/evidence/remote-result-c05.json)에 있다. 이어 **최종 C06에서도 같은18개를 다시 완전 본문으로 열어18/18 일치**를 확인했다.
- 최종 C06에서 실제 실행한 계약 검사:

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-070/manifest.json --fetch
```

cwd는 `/workspace/scratch/f1ffe17c302f/agentflow-open`, 대상SHA는 `30266f9354134b7aad33596b0acb96209876ce7d`, 종료코드0, status=`passed`, freshness=`remote_checked`, checked_at=`2026-11-23T09:29:54.522401+00:00`이다. 확인된 통합 HEAD는 `dfe4c46e3e27629d44ff12ec2f613ba4e031c42e`이며 작업 base76b8c1d는 유지했다. outside_paths0, unmerged_paths0, errors0. check의 changed_paths는143개이고 inventory144개와의 차이는 계약 파일manifest.json 한 개뿐임을 직접 대조했다.

- 원격 fetch한 C06 tree를 아래 읽기 전용 명령으로 대조했다. exit0,144/144개 경로와 blob hash 일치, 누락·차이0.

```bash
git ls-tree -r -z 30266f9354134b7aad33596b0acb96209876ce7d -- docs/workstreams/research/AF-RES-070/
```

- HANDOFF 작성 직전 `git --no-optional-locks status --porcelain --untracked-files=all`은 exit0·출력없음이었다. 이 파일만 추가해 마지막 단독 커밋한다. 임시 원문 캐시는 ignored이며 결과물로 취급하지 않는다.
- GitHub API 읽기/커밋은 shell 명령이 아니므로 가상의 종료코드를 붙이지 않았다. 실제 ref·완전 본문 비교·blob hash로 확인했다.

### 최종 C06 원격 본문 대조

확인 UTC: **2026-11-23 09:29:37 UTC**. API 경로는 각 파일의 `contents/... ?ref=30266f9354134b7aad33596b0acb96209876ce7d`였다. 아래 hash는 실제 로컬 발행 바이트의 Git blob SHA이고, 원격에서 디코딩한 완전 본문이 그 바이트와 일치했다.

| 파일 | 원격 재파싱 행 수 | Git blob SHA | 일치 |
| --- | --- | --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/RESULT.md) | 표 자료행 4/12/12/6/4/4 | `4e2e6f809f6ff55daf03d99476eb4532db840890` | yes |
| [ENROLLMENT.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/ENROLLMENT.csv) | 64 | `71e47aabc2d0033526b9ac3bd3fa2fa31c0352a5` | yes |
| [EVENTS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/EVENTS.csv) | 127 | `e947286cb5cbbb8143f3b8bfdd8ac79ac590fca7` | yes |
| [VIEWS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/VIEWS.csv) | 48 | `984372864323566bebb8e0fcfa3b800e41823c37` | yes |
| [OUTCOMES.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/OUTCOMES.csv) | 35 | `6168ed92c188773a0e3ab73c378e13adc3819f04` | yes |
| [SOURCES.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SOURCES.jsonl) | 253 | `2c1385a29eb1e5e28ebb917e45bd32332b3ffc9f` | yes |
| [PINS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/PINS.csv) | 66 | `5bbf4ab828c2a99a11491304203cee0fdd8a507b` | yes |
| [PAIRS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/PAIRS.csv) | 10 | `17c866e76142745097f7e22b12b9ad7774585811` | yes |
| [Q_CHECK.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/Q_CHECK.csv) | 8 | `05f4e02f083c6252b05294b41a335a54a5fb2fce` | yes |
| [COMMITS.csv](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/COMMITS.csv) | 5 | `ba1c4105ca5ec3dfcc3cc9dd560d286519ed17c1` | yes |
| [manifest.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/manifest.json) | 해당 없음 | `42ff2a6cd6e2f1e36a65565af9a23cc5e43324dd` | yes |
| [CASES.json](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/CASES.json) | 해당 없음 | `ccd3325a16f33dcb8740519247cea34b42fcd4c4` | yes |
| [SEARCHES.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SEARCHES.jsonl) | 8 | `00cd5ea200181307de152b807f121589ffc19568` | yes |
| [DATA_DICTIONARY.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/DATA_DICTIONARY.md) | 해당 없음 | `370105723a2af37a126705573842ba7beb086a28` | yes |
| [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/REPRODUCE.md) | 해당 없음 | `f02838c710dddec8460dceb609a89d051ed6c901` | yes |
| [REVIEW.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/REVIEW.md) | 해당 없음 | `7d72ec07087e742c1a19324c2f388f012d5162d5` | yes |
| [VALIDATION.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/VALIDATION.md) | 해당 없음 | `ad4497a1e25d6b503a5f570817285842256b51df` | yes |
| [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/SCOPE.md) | 해당 없음 | `17c9d9268f1f3619dbd59fb19f414271ff816c98` | yes |

## 6. 판단·보류·제외와 충돌 범위

한 필드가 유용하려면 그 필드의 값이 당시 판의 **정확한 행동 조건**과 맞아야 한다. 이미 목적·금지조건이 명시됐거나, 두 설정이 같은 결과를 내거나, 고른 필드가 실제 분기 단위와 다르면 질문을 추가했다는 사실만으로 개선을 주장할 수 없다. 읽은 사례가 이 판단을 뒤집는 경우도 RESULT의 Q6·반례 경로·마지막 약점3개에 연결했다.

미응답 기술 비교는1쌍이고 정확 동작의 정보 추가 무효 짝0쌍, 통제된 효과 짝0쌍이다. 같은 분야처럼 보이는 다른 동작을 억지로 맞추지 않았다. 이 작업에서 입력 폼·질문 정책·실행 제품 변경을 채택하지 않았다. 정책에 대한 사용자 확정 요구를 새로 만들지 않았다.

공개 자료 읽기와 자기 경로 커밋만 수행했다. 중앙 원장·다른 작업 브랜치와의 쓰기 충돌은 없다. 연구자 판단·원문 사실·타인의 시험·동일 OP의 별도 후속을 구분했다. 비용은 문서/절 수로만 보고하며 시간·돈·사용자 부담의 측정치를 만들지 않았다.

## 7. 다음 대화의 첫 행동

1. 원격 `work/research-af-res-070` 최신 SHA를 재조회하고 이 HANDOFF가 마지막 단독 커밋인지 확인한다. 결과 기준은 C06 `30266f9354134b7aad33596b0acb96209876ce7d`다. manifest의 실제 base/dependency와 비교한 뒤 위 check 명령을 실행한다.
2. **첫 구체 원자료 작업:** 정해진 큐에 이미 들어 있으나 최초판을 회수하지 못한 ripgrep 확장행 RG1847부터 opening event를 복구한다. 입력은 repo=`BurntSushi/ripgrep`, number=`1847`, created=`2021-04-15T19:37:15Z`다.

```bash
python -B docs/workstreams/research/AF-RES-070/tools/recover_opened.py BurntSushi/ripgrep 1847 2021-04-15T19:37:15Z docs/workstreams/research/AF-RES-070/private/reproduction/rg-1847-opening.json
```

출력의 `body` 또는 `event.payload.issue.body`를 해시한다. 현재 본문 hash는 `51c002055c9890f4bb5191c53130657b59b5780454d47e939d7ccf77f0862942`이며, 이것을 최초판 hash로 가정하지 않는다. 이어지는 RG 확장7행의 번호·UTC는 ENROLLMENT에 있다.403/404이면 접근 실패로 남기고 우회하지 않는다. 이미 읽은 후속/현재 본문을 회수로 지웠다고 주장하지 않는다.
3. 기전의 실행 확인을 이어가려면 [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/REPRODUCE.md)의 정확한 판·환경·입력으로 별도 연구자 시험을 수행한다. 특히 RG1840의 hidden/parent-ignore와 jq2394의 입력 시작을 확인할 수 있다. 그 결과를 과거 OP 질문 효과나 새로운 B로 재분류하지 않는다.
4. 실제 질문 효과를 연구하려면 기존24건의 사전 필드를 사후 교체하지 않는다. 더 읽지 않은 새 공개 cohort와 새 봉인 규칙이 필요하다. 이번 작업의 다음8 상한을 넘겨 성공 사례를 고르는 일은 하지 않았다. 새 사람에게 질문·연락·댓글을 보내지 않는다.
5. 필요한 미실시 검사와 기대 결과는 REPRODUCE에 있고, 다른 결과 dependency는066 하나뿐이다. 추가 계정·유료 API·권한 변경을 전제로 하지 않는다.

## 8. 묶음별 커밋

| 묶음 | SHA | 의미 |
| --- | --- | --- |
| C01 | `41fa88918ab89617deb220fd491ad06ca1d29b5f` | 규칙·manifest 먼저 커밋 |
| C02 | `a6e2f47e6cfa52e249f4d648016cf9d324eccae9` | 모집·주 A 및 RG 진단 A 봉인 |
| C03 | `39eec0e2cff033c9d34b55ae20e52880378ac4ef` | 나머지 진단 A 봉인 |
| C04 | `74421df3550bf6a02f1ba82d5f9e8c4bb31fc3db` | 근거·후속·원장·독립 판정 |
| C05 | `f2e13005ff9e0ef8fe307ed48f2d13fbeba1dedc` | 결과·반례·검산 발행 |
| C06 | `30266f9354134b7aad33596b0acb96209876ce7d` | 원격 결과 재검증·계약 영수증 동결 |
| 마지막 | 이 HANDOFF가 들어 있는 단독 커밋 | 결과 C06 재열람 후 HANDOFF.md만 추가 |

## 9. C06 전체 파일 고정 목록

아래 경로는 모두 `docs/workstreams/research/AF-RES-070/`에 상대적이다. 기준SHA `30266f9354134b7aad33596b0acb96209876ce7d`에144개가 있다. HANDOFF 자체는 마지막 커밋에서만 추가되므로 이 목록의 자기 hash를 요구하지 않는다.

| 상대 경로 | Git blob SHA | bytes |
| --- | --- | --- |
| .gitignore | `9ac82515de41923b9d0ce0e5f8a1b910f05eeaea` | 23 |
| CASES.json | `ccd3325a16f33dcb8740519247cea34b42fcd4c4` | 102828 |
| COMMITS.csv | `ba1c4105ca5ec3dfcc3cc9dd560d286519ed17c1` | 872 |
| DATA_DICTIONARY.md | `370105723a2af37a126705573842ba7beb086a28` | 7410 |
| ENROLLMENT.csv | `71e47aabc2d0033526b9ac3bd3fa2fa31c0352a5` | 45977 |
| EVENTS.csv | `e947286cb5cbbb8143f3b8bfdd8ac79ac590fca7` | 72047 |
| INTAKE.md | `a410e685fbe92ec7b97477d6e2ddc4c9751c211d` | 3579 |
| OUTCOMES.csv | `6168ed92c188773a0e3ab73c378e13adc3819f04` | 21433 |
| PAIRS.csv | `17c866e76142745097f7e22b12b9ad7774585811` | 4535 |
| PINS.csv | `5bbf4ab828c2a99a11491304203cee0fdd8a507b` | 21613 |
| Q_CHECK.csv | `05f4e02f083c6252b05294b41a335a54a5fb2fce` | 4336 |
| REPRODUCE.md | `f02838c710dddec8460dceb609a89d051ed6c901` | 7445 |
| RESULT.md | `4e2e6f809f6ff55daf03d99476eb4532db840890` | 52232 |
| REVIEW.md | `7d72ec07087e742c1a19324c2f388f012d5162d5` | 12745 |
| SCOPE.md | `17c9d9268f1f3619dbd59fb19f414271ff816c98` | 12387 |
| SEARCHES.jsonl | `00cd5ea200181307de152b807f121589ffc19568` | 22113 |
| SOURCES.jsonl | `2c1385a29eb1e5e28ebb917e45bd32332b3ffc9f` | 403656 |
| VALIDATION.md | `ad4497a1e25d6b503a5f570817285842256b51df` | 10499 |
| VIEWS.csv | `984372864323566bebb8e0fcfa3b800e41823c37` | 60033 |
| evidence/adjudication-audit.json | `a88ed0a1a6de8f6d5c5b66749dd48b2773fe909d` | 13123 |
| evidence/git-lock-recovery.json | `d70c50410d7ae51448136ebff668b54639fdc678` | 317 |
| evidence/ledger-independent-audit-first.json | `388f517233762601a0032e32a48cc703d578c5bd` | 11948 |
| evidence/ledger-independent-audit.json | `a47db5a64c55f4efc4cbc75c01517b955d475ed6` | 14981 |
| evidence/ledger-summary.json | `e5f55c2cd2d95aa19cd397738ee53a3e4736ef91` | 2086 |
| evidence/ledger_independent_audit.py | `3e40d8765070ce5df42670d82dc8f1e38dcac98c` | 17618 |
| evidence/remote-result-c05.json | `0b580d3cb726840a165d3844398688da44d00137` | 8362 |
| evidence/scope-c04.json | `290eb8316a76de203a2b3ff0b204bcfe25198d9a` | 10466 |
| evidence/scope-c05.json | `1de377691750884a53236d197601019c8da0a5d9` | 10788 |
| evidence/seal-verification.json | `44a9b5c665b0c7d58a68783a385db0bc5f1a0b68` | 8616 |
| evidence/session-check-c04.json | `9111b3fb69fd016a572a65796bf64c0bf7a44131` | 720 |
| evidence/session-check-c05.json | `28f4439bf0c6039a00bcc454a74c015efc1c2a42` | 11743 |
| evidence/session-start.json | `647dbccaaaca2a107928588ac52453bb2d900101` | 644 |
| evidence/source-audit.json | `79acdd5cd24ba28b757df0805650d263a10d3d80` | 34640 |
| evidence/validation.json | `235f4adc56bc82776c7f5e1ba387acd2b7dc033e` | 68682 |
| manifest.json | `42ff2a6cd6e2f1e36a65565af9a23cc5e43324dd` | 1736 |
| streams/jq/A.md | `ca1b339ad486bec2a1592378078a97164cfd0428` | 1639 |
| streams/jq/counterexamples.md | `4638e8aa1288e30c993ae008f5106ee0bbbadf76` | 1921 |
| streams/jq/diagnostic-counterexamples.md | `24cda9b2f23c2907c36057fae1bf9f0e691568d0` | 1610 |
| streams/jq/diagnostic-events.json | `a92ee3262df21ed3cda1527caa1a6323e6943965` | 15275 |
| streams/jq/diagnostic-outcomes.json | `542542d9570e6ff372ae5488674774438f867aa1` | 3314 |
| streams/jq/diagnostic-post.json | `e4153acc5286ab6f2326ff4b5dad5b2f22c1a612` | 4238 |
| streams/jq/diagnostics-A.md | `3116ef61aec9272c390339390888902734e69c67` | 847 |
| streams/jq/diagnostics-enrollment.json | `56219aad2c441ade129f39e221803e1c22a11941` | 9361 |
| streams/jq/diagnostics-pre.json | `b6c57b814a3cec139b341f579ce228eaae62d569` | 7027 |
| streams/jq/enrollment.json | `63fc6866d145400929f1036b9ab9dc662ff4eec1` | 9154 |
| streams/jq/events.json | `e2b59115d98c2dcc4343eb3b7956f276135da5e5` | 8190 |
| streams/jq/observed-pairs.json | `4a91c049cd7bf7ccb216c106ec11c1e003e105bf` | 1095 |
| streams/jq/outcomes.json | `f7fb50b2083ea4d91a3aaa55faeb89e3a8f8805c` | 3332 |
| streams/jq/post.json | `8894fd096169cb25133db695694d6a5fd657f414` | 4115 |
| streams/jq/pre.json | `3f38f703706b2a848fcf80b8ad33b27e519e9194` | 8503 |
| streams/jq/sources-access.jsonl | `c9da37e2351f2b627a210de6a1dc7536515af91d` | 4190 |
| streams/jq/sources-diagnostic-post.jsonl | `fc22e79be1bc5e6392e4299f8b4be15bf882faef` | 3365 |
| streams/jq/sources-diagnostics-pre.jsonl | `31daefe39882f11652bb0c0a123b5861c013133b` | 9137 |
| streams/jq/sources-post.jsonl | `31402770ec9a4702bbecca09ce0dfccfdef09411` | 3422 |
| streams/jq/sources-pre.jsonl | `8761e87c4ebdad41d01add9fe4c9d0d7e8e0f278` | 14801 |
| streams/jq/sources-supplement.jsonl | `3b43d045d43555e46e9b0e8e74f0961c8d591f3a` | 1593 |
| streams/pandoc/A.md | `6f0260173d1776f16c15ab4a1c219246046b3f31` | 3014 |
| streams/pandoc/DIAGNOSTIC_A.md | `76292460c5fe85d395d5dccc889822dd85d67642` | 1168 |
| streams/pandoc/DIAGNOSTIC_RESULT.md | `04e19a62c4bfd6d710c2bd33ffca4b21f5095168` | 3731 |
| streams/pandoc/access-diagnostic.jsonl | `19a6012b38123c5bad8f657ce97d522e76466e30` | 3781 |
| streams/pandoc/access-time-addendum.json | `951882b67a5c025e4e0312bcfbbe59c9d5f2e389` | 918 |
| streams/pandoc/access.jsonl | `1508b5fd986ee88045d7a86669b8e01f6d3eab82` | 5617 |
| streams/pandoc/counterexamples.md | `f73db93476090d8d0ee1f3adff84d371c1c52055` | 3728 |
| streams/pandoc/diagnostic-events.json | `b41ad4be07c66d7f99e799c8c132243c2d872d40` | 15014 |
| streams/pandoc/diagnostic-outcomes.json | `16be5d4f7cf7975f67188c4d1dfbbc4ab67fda75` | 4013 |
| streams/pandoc/diagnostic-pairs.json | `454869f9e4a1490fbf51bacf5ac3771239fa0a2f` | 1553 |
| streams/pandoc/diagnostic-pins-post.json | `224e6826a028d16e767376fe26ae04f8c68f05f5` | 1344 |
| streams/pandoc/diagnostic-post.json | `7ba3b9d905032d1e87497765a0e0034b0265a8b2` | 6855 |
| streams/pandoc/diagnostic-pre.json | `9551927dab29f96170daccfe6a4010621ce9d896` | 9503 |
| streams/pandoc/enrollment-diagnostic.json | `4a8320edbd03845951a2acc1af25260a4a61afab` | 11656 |
| streams/pandoc/enrollment.json | `72b4bcd8a68215700596eed7e6f790908367fe44` | 11757 |
| streams/pandoc/events.json | `24133e83eb74f8e7c130d6f0e5487bde8d58c743` | 19768 |
| streams/pandoc/outcomes.json | `80dbf106cc9b856f6476cdabed79f43940c8a492` | 4356 |
| streams/pandoc/pins-post.json | `a790a3a1f88eb6a0f823ec0422f3106ef7f2b100` | 1429 |
| streams/pandoc/pins.json | `d79101d7dd1c713d0583e89a6761890c3736ca9f` | 2561 |
| streams/pandoc/post.json | `2d96f7fed05f11dbe6ad67d89fdf8a466069ff58` | 8032 |
| streams/pandoc/pre.json | `0a1ee9c8c7ab96525690d01898a027d4d04a33d6` | 11121 |
| streams/pandoc/sources-diagnostic-post.jsonl | `93a0ee73b0c421f48aa2bbaa3e10431725fa4665` | 4343 |
| streams/pandoc/sources-diagnostic-pre.jsonl | `fecf09e38065b009ed0762893df058f3358cb1e0` | 16171 |
| streams/pandoc/sources-post.jsonl | `fd783c2088f55ab58bdcc9d2ad53197cb89fa0dd` | 3628 |
| streams/pandoc/sources-pre.jsonl | `6d51177c1be4ba3746ff6759d4ad2a25c9c1a08e` | 22075 |
| streams/pandoc/version-release.json | `ccdf96772cb0401badeeb075c27325fb78df7bae` | 276 |
| streams/rclone/A.md | `69b12b2d2b998a2852ae47e75a8c52e345fa9125` | 4343 |
| streams/rclone/access.jsonl | `161099e17ab86a693a692c8903efeb066312fd65` | 24178 |
| streams/rclone/apply_post_review.py | `404bfadb86d3edd28eb10559fdc22d48be785701` | 4949 |
| streams/rclone/build_diagnostics_post.py | `3ff0490d84802e6bfa079941cd5190fd807b71c2` | 14466 |
| streams/rclone/build_diagnostics_pre.py | `674baf82d82828fa9784e230ccd34f4b9afa648b` | 14631 |
| streams/rclone/build_post.py | `46011ba4eae396f97bb893852b17d0d2055eddf4` | 18382 |
| streams/rclone/build_pre.py | `4bd0e98dd5bfa9670fa416beab83c4878b1c2f70` | 19843 |
| streams/rclone/collect_pre.py | `dfb3054bfc3c31d9864ba6bac2365509065fc71d` | 3920 |
| streams/rclone/counterexamples.md | `a9197dff01d823efd473316853662a1e8bd93dc8` | 3875 |
| streams/rclone/diagnostic-enrollment.json | `2975cc92597c393584f71fc6b60914e97b0b4dcc` | 7826 |
| streams/rclone/diagnostic-events.json | `1941247af53b8b795798ef1df382491f59c8eca6` | 9936 |
| streams/rclone/diagnostic-outcomes.json | `07494bed8c15cfe07328d6398c4f8e3acc0a7991` | 3147 |
| streams/rclone/diagnostic-pairs.json | `8e2d113f31e5a5baacbf5ed323a935e9f577c9dd` | 1607 |
| streams/rclone/diagnostic-pins-post.json | `aeee7d0722cef07ee51b65002dc9706f8878ffaf` | 1600 |
| streams/rclone/diagnostic-post.json | `b98364607ca90fb88aa64a0ed3f7e16edf653714` | 3990 |
| streams/rclone/diagnostic-result.md | `d5315dbc1a9e201547ce7da518ab967b993ef315` | 2418 |
| streams/rclone/diagnostics-A.md | `70c9f32027b0be449529a170e86bf807cbab9523` | 1103 |
| streams/rclone/diagnostics-pre.json | `01c4a8d006107dbb54755061a4df584853153f91` | 8385 |
| streams/rclone/enrollment.json | `6a4a1a7ae147f5cdd048d61b82b331f5baa490e3` | 11351 |
| streams/rclone/events.json | `bc2a9391cd37ae078fae56c2cfe4d673c6367ce3` | 19725 |
| streams/rclone/local-validation-final.json | `4ee213cb5da2d890b5dc85e87d80e75b1e62e904` | 2353 |
| streams/rclone/outcomes.json | `a12cb779e1eeb3f868582c103ac4af4cf741ea9c` | 4141 |
| streams/rclone/pins-post.json | `5df7751ab9fca3ec00a448937a07c08d57ad7102` | 1889 |
| streams/rclone/pins.json | `57d85876998f2cb39124dfdd868e92f8bd7de1ae` | 1981 |
| streams/rclone/post-adjudication-review.md | `ee2c47e0415e822954ba00f7c85a0ce1e26814d1` | 1207 |
| streams/rclone/post-local-validation.json | `6d8b95ed641f89fe156194d4d0a7928dd89d372f` | 2701 |
| streams/rclone/post.json | `6b0803065325592bcbced24f265215034be5b9aa` | 6169 |
| streams/rclone/pre.json | `8d69928a4eac3b41348d888ea5fc4131a6196d67` | 15380 |
| streams/rclone/recover_opening.py | `4f2fe9d4b07d5f16d1df235a9c7f52fdfc2046b2` | 3237 |
| streams/rclone/source-access-failures.jsonl | `57ddfcd3dff1a19c7bb23d914e44c59fda0bc0ea` | 1796 |
| streams/rclone/source-diagnostics-post.jsonl | `3778f2d78fae6b4a13c462eff42910c1b704c9dd` | 3321 |
| streams/rclone/source-diagnostics-pre.jsonl | `652a935ca3bfec8752fbdd716c2be3e5d2d4046a` | 19500 |
| streams/rclone/source-post.jsonl | `0c967b7f413345c4fc2af6d66ef00aadb8a79d9c` | 3837 |
| streams/rclone/source-pre.jsonl | `a85e451901e5d9736eb02219806fa81a7981fabb` | 22656 |
| streams/rclone/title-provenance.json | `7a471b638e947e7e954b3bb5ead45f112802df35` | 8358 |
| streams/ripgrep/A.md | `ed5807bf004a469f1684ababe468585411b267ff` | 2839 |
| streams/ripgrep/access.jsonl | `8951abf4ed732206a624ea6f77b56ec68a29b6db` | 9596 |
| streams/ripgrep/build_post.py | `d3b3b7b87506bce2087ab8a17942645784a2d09e` | 18499 |
| streams/ripgrep/build_pre.py | `dce31515d5a5b08a3512904a0b3287176f3105b2` | 25133 |
| streams/ripgrep/counterexamples.md | `a83f7f1474b1f1019d3ebf050f57e73945596a96` | 4521 |
| streams/ripgrep/cross-review.json | `9dde2b3fec8f240aeb35aad011554e7b27dd0007` | 12517 |
| streams/ripgrep/enrollment.json | `31affe3e5912a197058126b3e48b449c19d3cfdd` | 24515 |
| streams/ripgrep/events.json | `106a1f809e495e3b6f559bb1c00814dd2772bf50` | 18134 |
| streams/ripgrep/outcomes.json | `a20296962d66d05f7fdd8af301bf7cf924a1d29c` | 12628 |
| streams/ripgrep/pairs.json | `4483deb71a2860c2d4512f8dd10e67966ffa75f3` | 1471 |
| streams/ripgrep/pins-post.json | `1068eb73eb4a96c95ef1565ab9fe22a1ec520c8e` | 2093 |
| streams/ripgrep/pins.json | `4d4209c729898ed659e51152a6c0573a77d52b35` | 7446 |
| streams/ripgrep/post.json | `b9c4cbde50929144f5a260195f60b0522e600ee4` | 26322 |
| streams/ripgrep/pre.json | `9bfda117bc112330417076ed3543cda676c45f21` | 21113 |
| streams/ripgrep/q-check.csv | `5b5c764683418d2cd62bcd21e73d4e3c9172c881` | 1816 |
| streams/ripgrep/queue.json | `8371ed4a47c81e992562367c212ce7078b83c831` | 5429 |
| streams/ripgrep/recover_opened.py | `f31b9d12ce8c81a07faaf59630c5e4263450a6fe` | 2922 |
| streams/ripgrep/sources-post.jsonl | `f25e195c822981478c976ff8ebd4f57348816ac2` | 10058 |
| streams/ripgrep/sources-pre.jsonl | `b13d70ea2278eef630f6a11c5c5a3a236dadb637` | 23191 |
| streams/ripgrep/validate_post.py | `2332659749192af7ac97994fac12386592e0e06d` | 7874 |
| streams/ripgrep/validation-post.json | `83da2b5122b3fcfbf48638b6dbdcb21694b40df8` | 10862 |
| tools/build_jq_diagnostics.py | `74975d7cd1b9db51bf6b02bcdd7d306a72e15f97` | 9315 |
| tools/build_ledgers.py | `160ae33dc4e59714b665e6648123b96b5692921f` | 27118 |
| tools/build_result.py | `653ffefc34cfec186f1b6d7556c316edeb550f0d` | 32638 |
| tools/merge_sources.py | `488ad90307858b677aca1d6fcff5388f4c60914d` | 23791 |
| tools/recover_opened.py | `03393e929991e015dec2a8615eab9e4f1b78fc31` | 3202 |
| tools/validate.py | `0085570fa4e81b8d78c9376565361a67bee5c12e` | 7920 |

