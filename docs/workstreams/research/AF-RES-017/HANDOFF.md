REVIEW_READY_WITH_GAPS

# AF-RES-017 — 늦은 발견과 재발명 인계

## 1. 상태와 미충족 목록

**검토 가능한 조사 결과와 재현 자료를 커밋했지만, 요청한 독립 정답원40개의 완성을 선언하지 않는다.** SELF_CHECK와 `evidence/acceptance-evidence.json`을 먼저 작성·검증·원격 커밋했다. 수락10조건 중7개는 예,3개는 아니오다. 세 번째 아니오는 아래 두 실질 미충족 때문에 전체 자기 점검을 통과하지 못했다는 절차 조건이다. 요청에 명시된 자료 부재 예외에 따라 이 상태로 인계한다.

| 미충족 | 확인한 상태 | 막힌 이유와 최소 보강 |
| --- | --- | --- |
| 적격 사례40개·계열 다양성 | 관측40개는 a16/b3/c16/e5, 한 계열 최대40%, 한 조직 최대2. 공개 날짜 대리값을 허용한 사건은18개이며 a1/c16/e1로3계열·PR88.9%다. 구체적 발견 근거는4개다. | 나머지22관측의 공개 원문에 최초 선택월·인지월·실제 변경 일부가 없다. 미구현안·종료 계획을 실행 결과로 승격할 수 없다. 기존18의 원 결정 확인과 최소 새 적격22개가 필요하며, 완성 집합에서 계열4·계열당40% 이하를 다시 확인해야 한다. |
| 늦게 알았지만 자체 구현이 옳았던5개 | 자체 구현 정당화9관측 중8개는 이미 알고 거절한 대안. 구현 뒤 발견한 B01은 실험용·미테스트이며 결정월과 생산 적용이 없다. | 당사자의 후기 발견 진술, 양쪽 월, 실제 유지 결과를 모두 갖춘5사건이 필요하다. 기지·거절8개를 이 요구의 양성으로 바꾸지 않았다. |
| SELF_CHECK 전체 통과 | 파일 형식·참조·산술·동결·원격 A 본문 검증32항목은 통과했지만 위 두 실질 조건은 미충족이다. | 형식 검증 성공을 연구 성공으로 바꾸지 않는다. 보강 뒤 수락 조건을 다시 평가해야 한다. |

실제 외부 해법을 채택한 뒤 철회한 사건은 **PR11·PR15·PM04의3건**을 확보했다. PM04는 Consul streaming 기능 비활성화이며 Consul 전체 제거가 아니다. 이3건에서도 초기 무지 때문에 늦게 채택했다는 인과까지 확인한 것은 아니다. 당시 유명함40/40, 역사적 검색 가능성40/40, 회피 가능한 노동시간·금액은 별도 미확인이다. 추가 절차 한계로, 첫 커밋 전에 계획한11호스트를 점검했지만 수집 중 새로 만난 호스트의 익명 응답 확인은 이후 실제 시각에 이루어졌다.

여기서 자료 부재는 **이번에 확보한 공개 기록에 요구된 정보가 없음**을 뜻한다. 세상의 자료를 모두 소진했거나 앞으로 확인할 수 없음을 뜻하지 않는다. 확인되지 않은 월·인지 상태·노동시간을 추정해 채우지 않았으며, 연구 재개에 필요한 첫 입력은 §8에 있다.

## 2. 읽은 SHA와 실행 환경

| 입력 | 읽은 고정 SHA | 사용 범위 |
| --- | --- | --- |
| source_commit, chore/workspace-foundation | `0209117d8ec00af39bd25844d52a18edc7323207` | AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, docs/product/RESEARCH_BRIEF.md, dot-control의 AF-RES-017과 의존 작업 인계. 이 SHA에서 작업 브랜치 생성 |
| AF-RES-009 | `7f627a81199f06da7f7b15f979e7fef25dd17602` | HANDOFF, GAP §5의 H1·H2 정의. 기존35시스템은 재조사하지 않음 |
| AF-RES-010 | `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | HANDOFF, TRANSFER_CASES의 T 형식. 기존 유추 연구 결과를 새 표본으로 재사용하지 않음 |
| AF-RES-013 | `eb569f07a3a34ffacf114384ae9b06ad062f5396` | HANDOFF, CASES의 엄격 채택 후 대체6후보, SAMPLING/BASELINE_RULES 형식. 기존 정답·실행 결과를 재채점하지 않음 |
| AF-RES-016 | `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc` | HANDOFF, CODEBOOK의 S1/S2와 상세 형태 S3.form. 명칭 차이를 명시하고 원 정의를 보존 |
| work/planning 참고 | `b373862baf009f3f8d37ac01b5437530434f7d31` | REVIEW-4 참고. 선행 결과를 근거로 쓸 때는 위 원본 SHA를 읽음 |

- 저장소: `laadkke-arch/agentflow-open`; 브랜치: `work/research-af-res-017`.
- 실제 실행 위치: ChatGPT 공유 Linux Cloud workspace, Bash, `/workspace/scratch/0514a89035ae/agentflow-open`.
- 작업자 모델의 세션 표시: **GPT-6 Astra Pro**. 수집·자료 감사는 같은 상속 모델 계열의 내부 하위 에이전트를 사용했다.
- B 내부 별도 검토의 선택 모델 표기: **gpt-6.2-sol**, fresh context, reasoning effort `high`. A 라벨·RESULT·기존 대화를 전달하지 않고 코드북과 라벨 없는 공통 추출 요약을 줬다. 이는 사람 검토도, 원문을 독립 재추출한 검토도 아니다. 파일 접근 제한은 지시 수준이며 OS 격리가 아니다.
- 쓰기는 `docs/workstreams/research/AF-RES-017/`에 한정했다. dot-control·공통 색인·제품 코드·main은 수정하지 않았다. AF-RES-018~020의 결과를 읽거나 기다리지 않았다.
- 터미널의 `git push`는 저장된 인증이 없어128로 실패했다. 기존 GitHub 연결의 tree/commit/ref 기능으로 동일한 Git tree를 게시하고 fetch로 대조했다. 계정·로그인·권한을 변경하지 않았다.

## 3. Q1–Q8 결론과 적용 한계

관측 탐색 창은1990-01-01~2026-11-21, 날짜 대리값을 포함한18사건의 실제 연도는2006~2025다. 현재 검색 진단은2026-11-21의 색인을 관측했다. 모든 비율의 판정자는 A 작업자이며 B 결과는 별도 보존했다.

| 질문 | 결론 한 줄 | 적용 한계·근거 |
| --- | --- | --- |
| Q1 기록 위치 | 엔지니어링 회고·PR·ADR·사고 보고가 서로 다른 인지·날짜·수정 증거를 제공한다. | `superseded`만으로 실제 외부 채택·철회를 뜻하지 않는다. AD01의 앞선 sqlx안은 미구현이었다. RESULT Q1, R01-fixed/P09-discussion/R04-incident |
| Q2 사례 집합 | 관측40, 월별 공개 대리 사건18, 구체적 발견 근거4를 분리했다. | 명시적 미인지2(B02/PR09)와 발견·재평가 인정2(PR10/PR14)의 강도도 다르다. 40적격 및 후기발견 후 자체구현5 조건 미달. RESULT Q2, evidence/statistics.json |
| Q3 놓친 것의 분류 | A 관계는 재사용 부품23/40, 같은 목적 완성품8/40, 같은 분야 설계6/40, 다른 생태계3/40, 타 분야 원리0/40이다. | 목적표본의 구성이지 전체 수요 비율이 아니다. A/B 형태39/40(97.5%)·기여33/40(82.5%)·관계37/40(92.5%); 세 축 동시29/40(72.5%). 역할·전달 형태 경계가 남는다. coding/agreement.json |
| Q4 당시 존재·발견 가능성 | 존재 yes25/no3/unknown12; 고유 핵심어 겹침 중앙값1(범위0–4). 현재 검색은 본문 검증 hit7/40이다. | 역사적 검색 성공률과 제품 추가 가치0 비율은40/40 미확인. 현행 공식 설명·회고 need를 당시 입력으로 부르지 않는다. RESULT Q4, evidence/EXISTENCE_AND_SEARCH.md |
| Q5 비용 | 수치 관련 변경·사고 지표31/40, 비용 미확인9/40. PR16건 삭제 중앙값125.5줄(2–1737), 사고5건 전체 영향 중앙값1080분(26–4380). | PR에는 테스트·설정·이동 코드가 섞인다. 사고 전체 영향은 무지에 귀속된 비용이 아니다. PM05의 저자26분과 타임라인23분 차이, B15의1주를 보존했다. RESULT Q5 |
| Q6 발견 경로·놓친 이유 | 독자·리뷰어·동료·공식 문서·사고 재평가가 구체적으로 확인된다. | 제안자 자신이 처음 어떻게 찾았는지와 원래 놓친 이유는 자주 없다. 어휘·생태계·분야 경계를 원인으로 단정하지 않았다. 입력 분해·제약 점검·유지 확인과의 연결은 H다. RESULT Q6 |
| Q7 다른 분야 측정 | 의학의 누적 근거, 특허의 선택된 후속 변경, 다중 발견, 사후 판단 편향은 다른 분모·결과를 측정한다. | 이들의 빈도를 소프트웨어 무지율로 가져올 수 없다. 방법·비교 원문28저작 중27개를 최소 수에 산입했고 동일 사이트 최대3을 지켰다. CROSSFIELD, evidence/methods/counts.json |
| Q8 다른 분야 원리 | A/B 모두 관측40의 주 관계 타 분야 원리0; 별도 기원 비교에서는 실제 구조 도입1차 경로7개를 확인했다. | 0/40,0/18,0/4로 수요 부재를 판단할 수 없다. 별도 양성7개를40의 분자에 섞지 않았다. 이름 재인식과 구조 변경을 나눈 M27 반례를 남겼다. CROSSFIELD Q8 |

고정016의 실제 S1은 product/component/principle이어서 `legacy_S1`에 보존했다. 요청한 상세 `형태(S1)`에는 실제016의 S3.form을 사용했으며 data도 원 정의대로 포함했다. S2의 whole은 명시된 선택 범위 전체이지 프로젝트 전체가 아니다. 이 명칭 차이와 관계013의 다대다 대응은 SCOPE·CODEBOOK·RESULT에 명시했다.

## 4. 가장 강한 근거3개

1. **B02 — 같은 분야의 오래된 알고리즘을 독자 경로로 뒤늦게 발견.** [2006-12-29 글과 2007-01 댓글](https://jasone.github.io/2006/12/29/deprogramming-lalr1-bias/)은 검색 실패, Pager 알고리즘·Menhir 안내, 논문을 읽고 하루를 들여 이식한 순서를 연결한다. [2022 회고](https://branchtaken.com/blog/2022/03/21/parsing-retrospective.html)는 앞선 구현 문제를 메모이제이션 오류로 정정한다. 따라서 발견 경로와 이식 노력은 강하지만 과거의 모든 고생이 알고리즘 미인지 때문이라는 해석은 약해진다. 근거 B-S02/B-S03, RESULT 표4·Q5.
2. **PR09 — 작은 표준 라이브러리 기능의 미인지와 실제 변경.** [gulp-run PR10](https://github.com/m19c/gulp-run/pull/10)에서 `path.delimiter`를 몰랐다는 응답과+1/-2 diff가 연결된다. [병합 고정 코드](https://github.com/m19c/gulp-run/blob/95e4412e75a28855e1b95ee6be1c0867955fb9a1/lib/command.js)에서는 삭제된 `isWindows` 선언의 후속 참조도 보인다. 이는 D2의 정적 회귀 우려이며 실행으로 확정한 결함이 아니다. 작은 부품 발견조차 실제 적용 검증이 별도임을 보여준다. 근거 P09-discussion/P09-diff/P09-merge-code.
3. **PR16 — 라이브러리의 존재와 필요한 기능의 존재를 분리해야 하는 반례.** [notify PR40](https://github.com/notify-rs/notify/pull/40)의 대체 대상은 Mio 자체가 아니라 [EventedFd 고정 코드](https://github.com/tokio-rs/mio/blob/13ecc11e39af506402fb0562d5f2999f4d795a56/src/sys/unix/eventedfd.rs)다. 자체 코드의2014-12-13 공개 대리값보다 EventedFd 도입2015-08-26이 늦다. 초기 결정 때 이미 있었던 API를 놓쳤다고 세면 사후 판단 오류가 된다. 근거 P16-target-history/P16-target-code, RESULT Q4.

## 5. RESULT §4의 세 약점과 다음 조사

| 약점 | 틀리면 바뀌는 결론 | 다음 조사 질문·자료·최소 규모 |
| --- | --- | --- |
| 40관측과40적격의 차이 및 후기 발견 뒤 자체 구현의 부족 | 현재 관계 비율과0/40은 독립 정답원40의 수요 분포가 될 수 없다. | 실제 초기 선택과 후기 인지를 모두 갖춘 표본에서 무엇을 놓쳤는가? 기존18의 원 결정 기록을 확인하고 최소 새 적격22개, 전체 계열4·계열당40% 이하, 후기 발견 후 자체구현5개를 확보한다. |
| 관측 비용·현재 검색과 회피 비용·당시 발견 가능성의 차이 | 삭제125.5줄이나 사고1080분을 제품이 줄일 수 있는 비용으로 해석할 수 없다. | 당시 입력을 받은 검색이 실제 선택·검토 시간을 바꾸는가? 결정 전 need20개, 동일20분 제한의 검색/제품 조건, 직접 시간·일정 근거10개를 비교한다. |
| 분류의 역할·전달 형태 경계 및 타 분야0의 해석 | 부품·설계 참고·논문 운반 형태의 경계와 타 분야 몫이 달라질 수 있다. | 관측 범위와 기여를 명시하면 판정이 안정되는가? 불일치11개+구조 전이 양성5+동일 구조 대조2의18개 별도 세트를 새 문맥에서 검증한다. |

## 6. 검증한 것과 미실시

### 직접 검증

- sources.json의 실제 주소·읽은 절·확인·한계·판·UTC·근거 수준과 사례 source ID를 대조했다. 통합243기록은 D1 156/D2 44/D3-fetch 43이며 고정 선행 입력도 포함한다. 이 전체를243개 외부 본문으로 부르지 않았다. 제외96개는 근거 수에서 분리했다.
- 방법·비교 문헌의 산입27저작, 사이트24·최대3, 소프트웨어 실증5/의학3/특허3/다중 발견2/사후 편향2, 실제 구조 도입 일차 경로7을 확인했다. 추가 반례 원저M27은 최소27에 넣지 않았다.
- 40개의 need와 짧은 공식 설명은 각각25단어 이하이며 공개 사용자 프로필·본문 전문을 원장에 저장하지 않았다. need는 회고 자료의 작업자 요약이다.
- A freeze `70fa1b6`이 B 원응답 `d137422`의 조상임을 확인했다. A SHA256 `84243b48d11f6cd60f3bf9576c0324b3c1446dc9aa68763df9cac58a630a21b4`, blind packet SHA256 `0151a940079bd128af033100c0cfe83c701072a00306ef68f93422ea289d050c`를 유지했다. A의 원격 본문과 로컬 UTF-8·Git blob도 일치했다.
- B 원응답40개와 불일치를 수정하지 않고 일치율·kappa를 계산했다. 부정7·긍정3 합성 진단은10/10 예상 판정이며 실제 사례 분모와 분리했다. 주요 코딩 축의80% 단일 값 집중은 없었고, 인기 unknown40/40은 별도 진단으로 경계를 확인했다.
- `analyze.py`, `agreement.py`, `write_result.py`를 순서대로 재실행해 기존 커밋 파일61개가 byte-for-byte 동일함을 확인했다. `evidence/reproducibility.json`에 명령과 결과를 보존했다.
- 표1~4의 정확한 열, 빈칸 없음, §1~§5 순서, 정확히3개 약점, Q1~Q8의2종류 이상 출처·반증 기록, 소유 경로, 비용31+9 분할 등32개 구조 검증을 통과했다. `evidence/validation.json`은 자기 점검 묶음 직전 실행 결과다.

### 미실시와 실행/확인 입력

| 미실시 | 이유 | 재개 명령·입력 |
| --- | --- | --- |
| 결정 당시의 검색 재현·제품 순효과 실험 | 역사 색인·동시기 need·실행 제품 조건을 확보하지 못함. 현재 진단을 대체하지 않음 | `cases/INPUTS.json`의40개 요약을 후보 입력으로만 사용. 아래 §8 명령으로 미확인 후보를 추린 뒤 결정 전 원문을 고정. RESULT §4.2의20개 입력·각20분 조건과 비교 결과표를 사전 등록하고 실행해야 함. 현재 파일로 가상의 결과를 출력하는 명령은 제공하지 않음 |
| PR09의 정적 우려에 대한 런타임 재현 | 원문·고정 코드 조사까지만 했으며 당시 의존성/런타임을 실행하지 않음 | 입력: `m19c/gulp-run`, commit `95e4412e75a28855e1b95ee6be1c0867955fb9a1`, `lib/command.js`, `isWindows`를 참조하는 실행 경로. 해당 고정 판의 package.json과 테스트 실행 명령을 먼저 읽고 그 경로를 호출하는 최소 테스트를 작성해야 함. `git show 95e4412e75a28855e1b95ee6be1c0867955fb9a1:lib/command.js` 및 `git grep -n isWindows 95e4412e75a28855e1b95ee6be1c0867955fb9a1 -- lib/command.js`로 정적 입력 재확인. 해당 저장소를 확보한 경로에서 실행하며 이 주 저장소에는 그 객체가 없음 |
| Lau1992 지정 원저 | NEJM 원문403, 다른 원저3개로 의학 최소 수는 충족 | 향후 정상 접근이 가능한 세션에서 `curl -I -L --max-time 15 'https://www.nejm.org/doi/pdf/10.1056/NEJM199207233270406?articleTools=true'`; 본문을 얻지 못하면 계속 제외. URL과 실패는 evidence/methods/sources.json#excluded |
| Fischhoff1975·Katz/Allen 지정 원저 | 원문 미확보·CMU 리다이렉트·MIT429·CORE403. 로그인하지 않고 중단 | `curl -I -L --max-time 15 'https://qualitysafety.bmj.com/content/12/4/304.full.pdf'`; `curl -I -L --max-time 15 'https://dspace.mit.edu/bitstreams/323d2d31-dd45-4083-8d91-4587f2fa4ecb/download'`; 이번 세션에서는 재시도하지 않음. 정상 공개 저자판을 열면 별도 source 기록을 추가 |

인용·도입 시점만으로 당시 인지도나 무지를 판정하지 않았다. 모든 호스트를 첫 커밋 전에 점검했다는 절차는 충족하지 못했고 PROGRESS와 SELF_CHECK에 남겼다. 유료 API·계정 생성·로그인·네트워크 우회·배포·제품 스택 선정·상시 실행은 수행하지 않았다.

## 7. 커밋 묶음과 색인 변경 제안

| 묶음 | 원격 커밋 | 내용 |
| --- | --- | --- |
| 1 | `9485f37a6b5fb78869468b425850fa49779de847` | 수집 전 SCOPE·SAMPLING과 네트워크 계획 |
| 2 | `ad4c76a4afbca53aa755001f79f7c05e3fe12841` | 첫20관측 |
| 3 | `9f0c34f34db7d05c45c568305aaeccf31f47d1f3` | 관측40 원장 |
| 4 | `510a6e042a620728d4c290a54b2e56a86adf9eed` | 존재·어휘·현재 검색 |
| 5 | `70fa1b691601a0cc9fb751db518fd4c5cad06bf8` | A 동결 |
| 6 | `d137422f1ff322f28bc09434cf50a7f31e31a591` | B 원응답·일치율·비용 단위 감사 |
| 7 | `417b5f65e9ad157732e934cc20c4d0f61256f05c` | CROSSFIELD·방법 문헌 |
| 8 | `4d91eef3ecfb77c0cca15cc42c2e9adda9ff18ef` | RESULT와 생성기 |
| 9 | `a3d2e4d6e7d503ff559467b7083bbccafc130848` | SELF_CHECK·수락 근거·재현 검증 |
| 9 보정 | `d0a2a8361d2eae70f27d06e981a137ecff2a11f0` | 존재 판정 미확인12와 결정월 미확인을 구분한 자기 점검 문구 보정 |
| 10 | 이 HANDOFF만 변경하는 마지막 커밋 | 게시 후 그 고정 SHA의 원격 본문을 다시 읽고 로컬 내용과 Git blob을 비교. 검증 결과와 마지막 SHA는 최종 응답에 보고 |

공통 색인은 수정하지 않았으며 다음 한 행만 제안한다.

| 작업 | 상태 | 결과 경로 | 수락·다음 행동 |
| --- | --- | --- | --- |
| AF-RES-017 | REVIEW_READY_WITH_GAPS | docs/workstreams/research/AF-RES-017/RESULT.md | acceptance_evidence는 evidence/acceptance-evidence.json 그대로 사용. 적격40·후기발견 자체구현5 부족을 유지하고 §8부터 보강 |

## 8. 다음 첫 행동

**새 결론을 쓰기 전에 미확인22후보의 최초 선택월·인지월·실제 결과를 공개 기록으로 연결한다.** 먼저 아래 읽기 전용 명령으로 현재 부족한 항목과 출처를 출력한다. 기존18개도 private 최초 결정일이 아닌 공개 코드 대리값이므로 이어서 확인한다. source_commit·A/B 원응답을 덮어쓰지 않는다.

저장소 루트에서:

```bash
git fetch origin work/research-af-res-017
git switch work/research-af-res-017
python docs/workstreams/research/AF-RES-017/tools/validate.py --no-write --check-handoff
python - <<'PY'
import json
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-017')
cases = json.loads((p / 'cases/CASES.json').read_text())
for case in cases:
    if not case['episode_eligibility']['minimum_dated_episode_criteria_met']:
        print(case['id'], case['decision_date'], case['discovery_date'])
        print(case['primary_urls'])
PY
```

추가 공개 검색의 첫 입력(아직 실행하지 않은 후속 계획): `"after implementing" "discovered" "library"`, `"did not know" "replaced" "custom"`, `"after writing" "found" "still" "library"`, `"ADR" "superseded" "migration"`. 응답 반환 순서·실제 읽은 본문·건너뛴 이유를 현재 방식대로 기록한다. 최소 규모와 필요한 증거는 SELF_CHECK §3·RESULT §4.1에 있다. 기존 기지·거절 사례의 수를 늘려 후기 발견5조건을 채우지 않는다.

새 자료가 확보되면 날짜·인지·실제 변경을 판정하고 사례집을 새로 동결한 뒤, 추가·변경된 근거의 코딩을 새 문맥에서 다시 검토해야 한다. 현재 B 원응답을 결과에 맞춰 수정하지 않는다. 이 인계 커밋 뒤에는 원격 본문을 확인하되 추가 산출물을 남겨 작업 트리를 더럽히지 않는다.
