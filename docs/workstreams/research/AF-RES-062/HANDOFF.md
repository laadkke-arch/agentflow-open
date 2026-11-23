# AF-RES-062 인계 — 부분 인계

**상태: 부분 인계(PARTIAL_HANDOFF).** 공개 자료 최소량·필수 산출물·정수 검산·Git 계약 검사는 수행했다. 최초25건의 방법 본문 결손, 잠정 선정순위, 원 배정/최종 수락 원행 및 실제 독해 사건의 결손이 남아 완전 수용으로 표시하지 않는다. Git 검사 통과는 연구 완결 판정과 별개다.

작업자 표기 `web-pro`; 실제 실행/검토 주체는 root AI와 frame_a/frame_b/supplement AI다. 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-062`, 소유 경로 `docs/workstreams/research/AF-RES-062/`에만 새 파일을 썼다. `dot-control.json`, 공통 상태·색인은 수정하지 않았다. 새 참가자 모집과 AF058기존 참가자/D04 원행 재분석, AF054시간 재모집, 기존B03분모 재추정은 하지 않았다.

## 고정판과 먼저 읽을 파일

- **검사·재열람을 마친 고정 결과 SHA:** [`bb3c627bf94f16418e3d71f56b7838b0c60d5e04`](https://github.com/laadkke-arch/agentflow-open/commit/bb3c627bf94f16418e3d71f56b7838b0c60d5e04).
- 결과·수용원장의 본문을 처음 고정한 SHA는 `ec3693ec9a18e7b4a230fba69496a0b5548719d2`다. 위 고정 결과 SHA는 검사 영수증을 더한 판이며 두 본문 바이트가 동일함을 확인했다.
- **첫 필수 표:** [연구·배정·자극·원문·열람·식별범위, RESULT 첫 표](https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/RESULT.md#L1).
- **둘째 필수 표:** [정오별 수락·정답·결측·조건차, RESULT 둘째 표](https://github.com/laadkke-arch/agentflow-open/blob/bb3c627bf94f16418e3d71f56b7838b0c60d5e04/docs/workstreams/research/AF-RES-062/RESULT.md#L12).
- **다음 담당이 가장 먼저 열 파일:** [evidence/acceptance-evidence.json](evidence/acceptance-evidence.json)의 C02A/C02B/C03/C06/C09. 각 결손의 분모, 고정 근거와 최소 재개 행동이 있다. 이어 [RESULT.md](RESULT.md) 첫 두 표와 [SELF_CHECK.md](SELF_CHECK.md)를 읽는다.

시작 통합판은 실제 배정 시점 `chore/workspace-foundation@1e741fd0def88ef56b1060a478d81f1985a4e760`, 계획 기준판은 `aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75`다. 선행 의존성은 `AF-RES-058@fefeb2146c7f63e49d0578f78989be49acd63291`, 인수 본문 고정판은 `4265e446b0e1a22022d68a6f989ebc1d504f3e84`다. [시작 계약](manifest.json)과 [인수 판·해시](evidence/inherited-inputs.json)에 기록했고 기존 코호트·중복 식별에만 사용했다.

## 실제 조사 상태와 분모

| 구분 | 실제 확인 | 미확인·주의 |
| --- | --- | --- |
| A 모집 | 34서지→29범위후보→발행일/DOI순 첫25.원저방법22+저자포스터1,방법근거23/25 | A-F17/F21본문 미회수.검색엔진 반환집합이며 전수검색 아님 |
| B 모집 | 33발견→초기27단위→중복/날짜정정25.원저방법14/25,전구부분2,질문지1,리뷰본문1,리뷰metadata1,실패6 | 잠정코호트합침/앞선방법/실제클릭가능성이 남음.원동결과 정정을 병기 |
| 주6자리 | 방법적격3: A01최초확정,A02잠정,B01잠정.공석A03/B02/B03 | 최초순위 확정은1/6자리.자료많은뒤논문으로공석을채우지않음 |
| 별도 보강 | 7발견/6연도내.적격Aslett1은B01중복 원행보강.신규독립코호트 관측0/최대2자리 | package지향검색이일부논문DataAvailability를거쳤으며repository전체목록 아님 |
| 엄격 독해 최소량 | **47독립외부1차저작**:사람원연구32,원과제/사전등록4,저자데이터/코드패키지4,독립참값원전7. IR사람보고서15/사실확인·문해력14 | 전체출처원장80행.미러·부록·중첩코호트·같은패키지파일·초록·실패는추가산입안함.47편 모두적격접근실험이라는뜻아님 |
| 수락 원개수 | B01관측표본의 양군×정오 **4조건셀**,정오별2대비 복원.동일원행complete-case4셀은감도.추가Study5진단4레코드셀 | 전체최초배정 N/a/m까지확인한목표코호트는0. A02평균8셀은원개수미회수,A01목표수락종점은해당없음 |
| 원문·실제 열람 | Kim72링크자리/67고유URL목록,일부원문직독. USGS/NLM/NASA실험전보관판3건 확인.클릭318/비클릭914저자정수보고 | 링크목록≠독해수. 당시가능내용≠참가자실제노출.클릭/hover/체류≠이해 |

근거 파일은 [frame.csv](frame.csv),[sources.jsonl](sources.jsonl),[개수감사](evidence/source-counts.json),[stimuli.csv](stimuli.csv),[outcomes.csv](outcomes.csv)다. 통합 CSV는 모집74행·자극106행·결과32행이며 각 단위의 뜻이 다르다.

## 채택 가능한 결과

**원문을 열 수 있게 하는 것과 오판 감소를 같은 문장으로 합치면 안 된다.** 같은 답 템플릿에 출처를 붙인 Kim 연구는 오권고 수락 감소를 저자 평균으로 보고하지만 공개 시행 원행/정수 교차표는 회수하지 못했다. Aslett의 검색 권유군에서는 같은 뉴스에 대한 관측 오주장 수락률이 더 높았다. 검색 지시·추가 활동이라는 I2개입을 정확한 링크 한 개의 I1효과로 옮기지 않는다.

| Aslett Study1 우선 관측 표본 | 통제 | 검색 권유 | 차이 |
| --- | --- | --- | --- |
| 정주장 수락=저자키상 최종정답 | 1837/3290 | 2046/3205 | +8.00189%p |
| 오주장 수락 | 356/1188 | 420/1161 | +6.20938%p |
| 오주장 최종정답 | 387/1188 | 367/1161 | −0.96508%p |

이는 원래 조건에 따른 **관측 응답의 기술 비교**다. 원 배정 N과 미관측 m은 미확인이다. 원래 T/FM/CND 세 범주를 보존했으며 CND를 정답으로 세지 않았다. `ResponseId+Article_day` 조인,49항목의 저자 최빈참값키,양군 원행 증인1건씩과8집계행을 독립 코드로 확인했다. [재현·손검산](reproduce.md),[독립 계산](streams/root/independent-calculation.json).

정오키 확인 관측 항목만 합친 정확도는2224/4478→2413/4366(+5.60295%p)로 늘면서 오수락도 늘었다. 이 분모는 미정참값 기사나 미관측 배정자를 포함한 전체정확도가 아니다. 저자complete-case의오수락343/1145→411/1130(+6.41535%p)도 별도로 보존했다. AF058 D04의재집계가아닌새공개코호트의결과다.

Kim의 무설명 출처제공 대비는 오수락78.2%→68.2%(−10.0%p),정수락67.2%→73.4%(+6.2%p)라는 **저자 반올림 평균**이다. 설명을 포함하면 오수락 차이는−5.9%p다. 이를 정수로 역산하지 않았다. 클릭자는 비클릭자와 원래부터 다를 수 있으며, 실제 읽기의 인과효과로 해석하지 않았다.

불리한/null 근거도 남겼다. Vraga의 직접 출처 있음/없음 교정 대비는 저자 보정 p=.24이고, 유리했던 control 대비는 오정보 post 자체가 달랐다. Panizza/Fendt는 모두에게 같은 접근을 주었다. Ding의checking은URLhover이며신뢰평정이최종수락이아니다. USGS/NLM실제원문은오권고를반박하고뇌크기원저에는비판·저자응답이병존한다. [Q별 검토](SELF_CHECK.md),[허용문장](claim-limits.md),[원문 감사](streams/root/source-audit.md).

## 실제 검사와 고정판 재열람

시작 계약 명령을 root AI가 실제 실행해 exit0이었다.

```bash
python -B -m workbench.session start af-res-062 --allow docs/workstreams/research/AF-RES-062/ --dependency work/research-af-res-058=fefeb2146c7f63e49d0578f78989be49acd63291 --output docs/workstreams/research/AF-RES-062/manifest.json --fetch
```

최종 검사 명령은 다음과 같고 **2026-11-23T05:49:11.490422+00:00**, 위 고정 결과 SHA `bb3c627bf94f16418e3d71f56b7838b0c60d5e04`에서 root AI가 직접 실행했다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-062/manifest.json --fetch
```

실제 반환: `status=passed`,exit0,`freshness=remote_checked`,`changed_paths=101`,`outside_paths=[]`,`unmerged_paths=[]`,`errors=[]`. 검사한통합/시작판은`1e741fd0def88ef56b1060a478d81f1985a4e760`,계약SHA256은`19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`다. 앞선본문고정판`ec3693…`의같은명령실행전체출력은 [session-check.json](evidence/session-check.json)에있으며,이단락은검사영수증까지커밋한최종판에서의재검사실측이다.

통합 구조 검사 [artifact-validation.json](evidence/artifact-validation.json)은42항목PASS,로컬Markdown링크173개PASS다. 첫 실행에서B source ID구분자정규화와검사기자체문자열오탐을발견해수정했고실패영수증도 [보존](evidence/artifact-validation-initial.json)했다. 원연구정수는바뀌지않았다.

고정 Git객체를 다음 명령으로 다시 열어 **2026-11-23T05:49:16.193521+00:00**,PASS를확인한뒤이HANDOFF를작성했다.

```bash
python -B docs/workstreams/research/AF-RES-062/review_fixed.py --sha bb3c627bf94f16418e3d71f56b7838b0c60d5e04 --verify-receipts
```

실측검사: RESULT로컬링크81개/수용원장의근거·검사경로39개,끊긴경로관측0;여섯정수대비문자열모두집계와일치;최소량47과부분인계상태일치;workingtree와고정blob바이트일치. 필수표시작행은1과12다. 초기본문고정판의상세재열람영수증은 [fixed-result-review.json](evidence/fixed-result-review.json)에있고,최종판검사에서는새검사영수증경로도모두확인했다.

| 고정 본문 | SHA256 |
| --- | --- |
| RESULT.md | `bbaedf66be2c3231f85d564bb1395a81247640effddabac3de1848b045dcc721` |
| evidence/acceptance-evidence.json | `8f683b27ded5e88d4ce1fda33fc492b6d9750ec1cc0f8bf2e4bc6136624209c3` |

최종판 재열람 직후 Git작업트리는깨끗했다.이후추가하는파일은이HANDOFF하나이며마지막단독커밋으로남긴다.그커밋자체의SHA는저장소branchHEAD/Git로그로확인한다.

## 재현 명령·입력과 미실시

저장소루트에서실행하며공개원행은ignored캐시에만받는다.명령·입력해시·실제조인열은 [reproduce.md](reproduce.md)에있다.

```bash
python -B docs/workstreams/research/AF-RES-062/streams/supplement/aggregate_aslett.py --fetch
python -B docs/workstreams/research/AF-RES-062/streams/root/independent_recount.py
python -B docs/workstreams/research/AF-RES-062/streams/a/audit_transparent_cis.py --fetch
```

첫두명령의입력은저자Git `7b4ffee080be622e06f6197bfd095a3e4faebd16`의`Study_1_df_FM.csv`,`Search_Exp_Misl_False.csv`,`Study_1_df_T.csv`,`Fact_Checker_Data_Master.csv`및분리된Study5두파일이다.세번째입력은TransparentCIS `065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d`의`data/input/input_data.csv`와`results/user_study_output/mturk_output.csv`다.모두실제실행·해시검사된경로다.

완전배정범위계산은필요입력이없어미실시다.필요입력은Aslett의원배정·문항제시·주의검사/중도탈락명부와Kim의동일시행배정·정오키·권고·최종선택·제외mask 또는저자정수교차표다.아직없는열이름을실제파일열처럼가정한계산명령은만들지않았다.입력이도착하면먼저코드북/실제열을읽어 [요청스키마](claim-limits.md)의역할에매핑하고현재스크립트에배정분모결합을추가해야한다.

원배정N/a/m미확인상태의범위계산,평균에서정수역산,반복시행을독립으로둔새유의성검정은미실시다. Fendt SAV파싱/R원회귀재실행은미실시이며동일접근·평정종점이라는탈락판정에필요하지않다.원앱의실시간배포/개별사용자이해를새실험으로검사하지않았다.새B03mask/정오표의전수공개조사도미실시이며이번인수에서회수한새정정자료는없다.

## 묶음 커밋 이력

시각은UTC로환산했다.정정은원래고정판을지우지않고후속파일에병기했다. [커밋원장](evidence/commit-history.json)은본문고정까지,아래는검사고정까지포함한다.

| 묶음 | 실제 SHA | UTC 시각 | 변경 이유 |
| --- | --- | --- | --- |
| ①규칙·계약 | `27dc28648c125186d1b79c5e629c97210e57b23e` | 2026-11-23 05:07:19 | 결과비선정모집·적격·결측규칙,실제시작계약/인수판 |
| ①S메타데이터 | `6ce6976dac1758109ca6678bb1aa5a19f953d175` | 05:08:46 | package-first후보동결 |
| ①B메타데이터 | `10de6313282ba8cfeeec75057050056ef8b74bad` | 05:09:15 | B발행순후보동결 |
| ①A메타데이터 | `fd80a75d5ee3a77f89291f82fd3fb2b90975be3b` | 05:09:31 | A첫25후보동결 |
| ②원문·역사판 | `037df9b9ee49a41271813f5577ad00cda29a3b5a` | 05:16:46 | 직접도착절/반례/역사판감사;후속NASA정정병기 |
| ③원행정수 | `6bb798aa31b7021d965f0e45446f089e12b89f39` | 05:20:19 | Aslett관측수락·CND복원과root독립검산 |
| ②·③최종stream | `aaa8c8a4c01a86fddcdba8b5f666fbd928490bcc` | 05:39:00 | 모든방법·자극·패키지·반례·정정원장고정 |
| ④통합표·허용문장·수용 | `ec3693ec9a18e7b4a230fba69496a0b5548719d2` | 05:45:52 | 필수두표/정수·평균분리/주장한계/Q별자체검토/수용원장 |
| 검사·고정판재열람 | `bb3c627bf94f16418e3d71f56b7838b0c60d5e04` | 05:48:41 | 실제sessioncheck/고정blob재열람영수증;본문변경없음 |

## 색인 추가 제안

기존 `docs/research/INDEX.md`의지침에따라아래항목을색인편집담당에게제안한다.소유범위밖색인은직접고치지않았다.

| 고유 ID | 답하는 질문 | 현재 상태 | 파일 | 핵심 의존·충돌 |
| --- | --- | --- | --- | --- |
| AF-RES-062 | 검증할독립원문제공/검색격려가정오별수락·최종정확도를어떻게바꾸는가;배정과실제열람구분 | **부분 인계**:47저작직독,방법미회수/잠정선정,관측정수1코호트,완전배정분모미확인 | `docs/workstreams/research/AF-RES-062/HANDOFF.md`와`RESULT.md` | AF058은중복확인용. Kim저자평균의오수락감소와Aslett관측정수의오수락증가를동일개입으로합산금지.원문내용/참값논쟁·클릭자선택편향 유지 |

## 가장 중요한 세 약점 → 바로 대응하는 다음 조사

1. **최초순위·방법 결손:** A2/B6본문과B부분방법·코호트식별이남음 → `frame.csv`의해당DOI/next_input에서공개원방법·보충판·동일코호트교차표를먼저회수하고첫25순서로재판정한다.
2. **정오별배정수락 결손:** Kim공개원행미회수/A01목표종점해당없음/Aslett원배정N·m미확인 → Kim시행원행또는정수교차표와Aslett배정·제시·탈락명부를확보해양군N/a/m를같은시행으로연결한다.
3. **원문함의·실제독해 결손:** 당시절의부분검증·참값논쟁·자발클릭선택이남음 → 저자당시판/정정과정확한도착절,load·체류·스크롤·이해사건을문항에연결한뒤실무오판감소주장을다시판정한다.
