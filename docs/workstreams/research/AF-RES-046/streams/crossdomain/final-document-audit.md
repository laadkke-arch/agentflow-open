# AF-RES-046 · 최종 문서와 최초 공개판 원장 대조

## 범위와 시점

검토자는 같은 연구 작업공간의 별도 AI 역할이다. **외부 독립 인간 판독은 아니다.** RESULT/SELF_CHECK의 서술과 cases/baselines/events/statistics, 최초 공개 head 집계 및 두 stream의 archive 복구 기록을 대조했다. 공개 원문을 새로 수집하거나 기존 연구자의 판정을 직접 수정하지 않았다. 이 감사의 쓰기는 이 파일 하나에 한정했다.

최초 검토 스냅샷은 2026-11-22 22:46:29 UTC였다. 이때 RESULT에는 통합 담당이 이미 고칠 예정이라고 알린 events156 표기가 있었다. 수정된 문서를 22:51:02와 22:53:03 UTC에 다시 읽었다. 아래 입력 지문은 `2026-11-22T22:54:20.300102+00:00`의 작업 중 스냅샷이다. 경로·탭·SHA256을 LF로 연결한 manifest 지문은 `de117ae8bbde002fc40e4d6ee957d9b602f211160b787220aac6ee797a484ff2`이다. 이후 새 원문 복구와 최종 커밋 검증은 별도이다.

|읽은 입력|SHA-256|
|---|---|
| `RESULT.md` | `e2e39c0a3cf17f8125a275149469b4a1b247c1f34062878fb245e497d3d261f7` |
| `SELF_CHECK.md` | `50f29f338a293f40911aeacc5e9c997f5537755f5c5834ae9dd6425e4943c869` |
| `cases.json` | `eee21926005b3bf7f922c8d47808b0501b2d8c0ae78a48efbbbde8a73a5b7bcd` |
| `baselines.csv` | `99bdfc494d9d210535db18442210ecc689a142b4b8cdf32d525678dd23f6a294` |
| `events.csv` | `2199ac8aa9f4bacecd492c4c216a90ba21ca253f7b0fd709579f5bdbf0e142a5` |
| `evidence/statistics.json` | `f2f88fb558032235b61aa3696345ead5595887b3117f828381e04db63ae228a4` |
| `initial-public-heads.csv` | `df989ed77311d2837ee345928c0e47d3da6d0330e854d332957393dffeb31f50` |
| `sources.jsonl` | `daf59c8ef7cadc521aa0152063d549d990e6562384706dfd423efb348f2c9a25` |
| `streams/pandas/initial-public-head-recovery.json` | `0007f0cd5fd75b1f651d8042a13ece5b812bddfd9c6c345c6bc6ba10d0a5e7ad` |
| `streams/pandas/sources-supplement-archive.jsonl` | `acc0dac6671193c765a1589eef410a43a77d19fd9e3c2385666d78c1c355cbb8` |
| `streams/sklearn/initial-public-head-recovery.json` | `d9bf97976623fc7511ec861eea60b8450d60deda9c6121e6f2958de8c3be7ba9` |
| `streams/sklearn/sources-supplement-archive.jsonl` | `2c1af96464f66e2d7c973ad6c3919259eec07bde27f86bdaa7a5a71211ee5fc1` |

## 실제로 발견한 불일치와 정정 확인

|ID|문서의 문제와 정확한 위치|원장과의 차이|22:54 UTC 기준 상태·최소 조치|
|---|---|---|---|
|FD1|최초 RESULT 표1 N-P1 행은 ‘포맷 기대값을 고침’이라고 서술했다.|pandas changes `N-P1-3`, commit `9a740a67b6310f9ddc84efbdcb6e5be0db93cfd2`의 시험 수정은 입력 시각010101/020211→010000/020000이다. 기대 포맷 `%Y%m%d %H%M%S`는 유지된다.|**정정 확인.** 22:51 재판독에서 입력 수정·기대 포맷 유지로 바뀌었다. 시험 실패가 남았다는 뒤 문장과 충돌하지 않는다.|
|FD2|최초 RESULT Q2와 SELF_CHECK의 초기판 복구 설명에는 raw 원본 접근 제한이 가까이 드러나지 않았다.|두 archive 기록은 문서화된 ClickHouse normalized opened-event mirror를 사용했고, 시간별 raw gzip 접근403·원 GitHub event ID 미보존·독립 raw 대조 없음이라는 제한을 명시한다.|**정정 확인.** RESULT Q2 47행은 12/12 복구 바로 옆에 raw 대조0/12와 결합 근거를 적었다. SELF_CHECK 23행에도 같은 제한이 추가되었다. 12/12는 미러와 고정 GitHub diff의 결합 확인이며 원형 raw 이벤트12개 독립 확보가 아니다.|
|FD3|L-P2의 새 opened head는 `87ade9fa…`인데 baseline `parent_sha`에 이전 candidate의 parent/현재 PR diff merge-base인 `80ecde4b…`가 남았다.|pandas archive의 해당 head parent는 공란이었다. root의 `RR-OPEN-P2`는 실제 `87ade9fa…` commit parent가 `cfa3bfd612095be67841e514fa40310997db2945`임을 직접 기록한다. PR base/merge-base와 commit parent는 다른 값이다.|**정정 확인.** 22:51 baseline/initial-public-heads에 cfa3bfd가 반영되었고, 22:53 baseline.source_ids에 RR-OPEN-P2 및 집계 원장의 `head_metadata_source_id` 연결을 확인했다. 옛 SHA·기존 기록은 별도 열로 보존된다.|
|FD4|SELF_CHECK Q2가 root에 없는 `initial-public-head-recovery.json`을 위치로 적었다.|실제 복구 파일은 `streams/pandas/initial-public-head-recovery.json`과 `streams/sklearn/initial-public-head-recovery.json`이며 root 집계는 `initial-public-heads.csv`다.|**정정 확인.** 22:53 재판독에서 실제 세 경로가 모두 명시되었다.|
|FD5|최초 RESULT 검산 목록은 events156이었다.|현재 events는 원156행+opened 복구12행=168행이다. 이 문제는 감사 시작 전부터 통합 담당이 수정 예정이라고 알렸다.|**정정 확인.** RESULT 125행은 events168(원156+opened복원12), 실제 CSV는168자료행이었다. 새로 발견한 오류로 중복 주장하지 않는다.|
|FD6|최초 RESULT N-S4 행·표2·비용 시간선71행, SELF_CHECK Q5 및 statistics는 issue25261의 many hours 진술을 PR 개설 전 자기보고로 단정했다. 시간선에는 이슈 생성시각2022-12-30 18:33:16을 붙였다.|최초 S-SUP-25261/RR-COST는 현재 body이고 본문 최초판 미확인이어서 이슈 개설시각만으로 비용 문구의 게시시각까지 고정할 수 없었다. **이슈가 PR보다 먼저 개설된 것**과 **그 비용 문구가 개설 당시 이미 있었던 것**은 다른 사실이다.|**후속 복구로 해결 확인.** 아래 22:56 이후 부기에서 S-ARCH-COST-25261의 IssuesEvent opened body에 같은 비용 문구가 실제 존재함을 기록에서 직접 대조했다. 사건시각2022-12-30T18:33:16Z와 actor gerardkr가 결합되어 개설 전 소비자 정성 비용이라는 표현을 유지할 근거가 생겼다. 원문 전체가 현재 body와 같은 것은 아니며, 수치 노동·절감으로 승격하지 않는다.|

위 수정은 통합 담당의 완료 보고만 믿은 것이 아니라 수정된 파일을 다시 읽어 확인했다. FD6의 새로운 archive 결과는 최초22:54 지문 스냅샷 뒤에 나왔으므로 다음 부기에 별도 지문과 위치를 남긴다.

### 22:56 이후 추가 원문 기록 대조

`streams/sklearn/successor-publication-recovery.json`의 SHA-256은 `16680ce6c3adaf5cd7141c857b1944be9bb5b457bd633c850a0cf67475b2f63b`, `streams/sklearn/sources-supplement-successors.jsonl`은 `299a57c658838f79af7c2e132b300d54c62dfd6022517f2f1cd3d43600ea481a`다. 후자는2026-11-22T22:56:26.663393+00:00에 읽었으며 이어 전자의 두 items를 직접 읽었다.

- `items[0]`/`S-ARCH-COST-25261`: response.data[0], IssuesEvent/opened/25261, event2022-12-30T18:33:16Z, actor gerardkr, Describe the bug 둘째 문단. 보존한 비용 문장의 `excerpt_found=true`를 확인했다. `full_opening_body_matches_later_rest_body=false`이므로 비용 문장의 당초 존재와 전체 본문의 동일성을 혼동하지 않는다. raw event ID 미확보, 비수치 시간이라는 한계는 그대로다.
- `items[1]`/`S-ARCH-SUCCESSOR-25605`: response.data[0], PullRequestEvent/opened/25605, head `feaabb7e6f2ccecced7a6847a267ad54b026f8a3`, base `a897a34d7d989bf317de17f80948639c0fd5ecf1`이 기존에 읽은 정확한 두 파일 patch와 연결된다. 정확한 공개 확인 상한은 event2023-02-14T09:22:47Z이며 REST PR created09:22:46Z와 구별해야 한다. 1초 차이는 관측창·타인 포함 분자를 바꾸지 않는다. 원 작성자 ogrisel의 patch로 바뀌지도 않는다.

## 추가로 보완 중인 시간 경계

통합 담당은 pandas 후속 PR52089의 opened head와 `f95152e78c8baa2b1f4e07ecebb31496b3956c65`의 동일성을 추가 확인 중이라고 알렸다. 이는 RESULT의 ‘원 PR 종결45초 전에 같은 목적 patch가 공개되었다’와 연결된다.

현재 기록의 PR 개설시각은2023-03-20 17:37:25, 원 PR 종결은17:38:10이며 차이45초의 산술은 맞다. 그러나 PR 생성시각만으로 특정 SHA가 그때 이미 공개되었다는 연결까지 자동 입증할 수는 없다. 관련 git date도 공개 시각을 대신하지 못한다. 열린 순간의 head/실제 diff와 해당 SHA가 일치하는 원문이 추가되면 이 경계 포함 판정이 강화된다. 실패하면 주창 안에 공개된 정확한 같은 목적 변경의 근거 수준을 다시 표시해야 한다. 이 보완은 부모 조사자가 진행 중이며, 이 감사에서는 아직 새 결과를 독립 재판독하지 않았다.

이는 본 감사에서 네 가지 첫 링크를 다시 골랐다는 뜻이 아니다. 최초 공개판12개 복구와 **후속 PR의 특정 patch 공개 경계**가 서로 다른 검증이라는 점을 기록한다.

## 최초 공개판 복구의 문서·원장 일치

두 archive 기록의 selected6+6을 root `initial-public-heads.csv`, `baselines.csv`, `cases.json`과 직접 조인했다. 12개 슬롯 모두 head와 base가 일치했다. sklearn의 별도 제외 PR25272 복구는 추가 사례로 세지 않았으며, 자연층 앞선 test-only 제외의 재점검으로 남아 있다.

pandas는5개 슬롯의 기존 candidate head가 opened head와 같았고 L-P2에서만 실제 opened head가 달랐다. sklearn L-S1도 링크 전 `a897a34d…`와 최초 opened `39a39ad3…`를 구별했다. N-P2/L-P1 등의 PR base와 diff merge-base가 다른 점을 별도 열에 보존한 것도 확인했다. 개설 이벤트가 PR created_at보다1초 늦는 경우를 새 작업·새 revision으로 세지 않았다.

L-S1은79개 commit·14개 변경 파일을 포함한 공유 branch이며 최초 head는 betatim의 merge이다. archive 복구 기록은 testing helper 전체와 관련 head merge의 속성 변환/시험을 읽었으나14개 파일 본문을 모두 같은 깊이로 판독하지 않았다고 명시한다. RESULT Q2와 표1은 이 공유 branch의 모든 코드를 PR 개설자 ogrisel 혼자 작성했다고 귀속하지 않도록 보완되었다.

원형 raw archive와 original event ID의 미확인은 12/12 복구 설명의 범위를 제한한다. 그렇다고 실제로 읽은 normalized opened 행과 GitHub 고정 diff가 없었던 것으로 취급하지 않았다. 기록상 근거는 `repo+PR번호+opened action+event time+head/base`의 조합이다. 과거 적재기의 정확한2023년판까지 독립 인증한 것은 아니라는 pandas provenance 제한도 남아 있다.

## 핵심 분모와 값의 대조

22:51 대조한 root 원장에서는 다음 값들이 문서와 일치했다. 이것은 각 원문에 대한 외부 독립 재실험이 아니라 현재 기록의 교차 일치 확인이다.

|항목|다시 센 값|해석 경계|
|---|---:|---|
|고유 PR 슬롯|12=자연8+링크우선4|후속 PR·추가 제외 사례·타분야 사례를 분모에 추가하지 않음|
|자연층 첫 적격 reviewer URL|0/8|링크 조건부 변화/열람 비율은 해당 없음. 무링크 실제 수정이0이라는 뜻이 아님|
|링크 우선층 URL|4/4|링크 존재로 선정한 층이며 모집단 링크 발생률이 아님|
|동일 작성자·같은 목적 후속 변경|당시 원장 표기2/4|L-P2와L-S2. **최종 확정 검산으로 승인하지 않음:** L-P2의 주창 공개 SHA 연결은 위 후속 보완 대기와 연결됨. 미입증이면 확정1·미확인2로 조정해야 함|
|동일 작성자 변화 미확인|1/4, L-S1|원 작성자의 소실된 후속 branch를 무변경0으로 바꾸지 않음|
|타인 포함 후속 변경|당시 원장 표기4/4|L-P1·L-P2의 선행 착수를 포함하며 첫 링크의 인과효과4건이 아님. L-P2의 주창내 공개 근거가 미입증이면 이 분자도 같은 patch에 의존하므로3확인·1미확인으로 낮춰야 함|
|엄격 첫 링크 사슬|확인0/4|최초판을 복구했어도 작성자 연결 발언·원 작성자 patch 등 다른 고리의 공백은 남음|
|능동 노동 로그·주창 작성자 수치 자기보고·비교쌍|각 확인0|active_human_work_seconds와 saved seconds는 null/미확인.0초로 코딩되지 않음|
|초기 공개 head 미러+고정 diff 복구|12/12|독립 raw archive 대조는0/12|
|events|168=156+12|opened 복구 이벤트는 사례 수를 늘리지 않음|
|자료 영수증/최소수 산입 저작|508/54|영수증 수와 고유 최소 저작 수를 분리|
|필수 타분야 배당|3/4|MusicBrainz 실제 edit 원장0을 전체54개로 대신 충족시키지 않음|

첫 링크 뒤 변화의 행위자 감도2/4→1/3→1/2, 타인 포함4/4→3/3→2/2와 L-S1 미확인1 유지가 당시 statistics에 남아 있었다. L-P2의 경계 보완 결과가 다르면 기본 포함 집계는 함께 바뀌어야 하며, 이 기존 감도를 최종 승인한 것은 아니다. 특히 타인 포함 값을 단순히 ‘링크 있음’에서 true로 만드는 집계는 이 경계가 미확인일 때 사용할 수 없다. 초기판 복구 후에도 명시 읽음·첫 발견 확인0, 첫 링크 엄격0, 측정 가능한 작성자 노동0의 **확인수**를 실제 효과 또는 시간값0으로 승격한 문장은 확인하지 못했다.

RESULT의 마지막 표는 요구된 약점3행으로 끝나며, 본문은 외부 독립 인간 판독을 했다고 주장하지 않는다. 최초 판독의 R01·일부 후속 단서 노출·N-S2 잠정성을 복구 후 삭제한 흔적도 이 문서들에서 찾지 못했다.

## 이 감사의 종료 상태

문서 오류 네 가지와 기지의 events 수 표기는 정정 후 확인했다. 비용 문구의 최초 게시시각은 추가 IssuesEvent 기록으로 보완되었음을 다시 읽었고, 타인 후속 PR25605의 실제 patch 공개 상한도 확인했다. **후속 PR52089의 주창 안 정확한 SHA 공개 연결은 추가 확인 대기다.** 이 때문에 당시 원장의 동일 작성자2/4를 최종 감사 완료 값으로 고정하지 않는다. 52089의 주창 안 공개 버전 근거가 확보되지 않으면 시간창 확정 분자를 낮추고 후속 변화 자체와 주창 포함 여부를 분리해야 한다. 해당 추가 결과가 나온 뒤 최종 표·statistics·원장과 고정 커밋을 다시 읽어야 하며, 이 파일의 최종 부기 이후 수집된 증거까지 판독을 완료했다고 표시하지 않는다.

