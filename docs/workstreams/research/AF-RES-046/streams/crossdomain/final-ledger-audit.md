# AF-RES-046 · 최종 원장 AI 대조

## 검토 범위와 스냅샷

검토 역할은 별도 AI 에이전트의 자체 교차 점검이다. 동일 작업공간에서 조사자가 작성한 원장과 통합 코드를 대조했으며 **외부 독립 인간 판독이 아니다.** 다른 조사자의 원문을 새로 검색하거나 추가하지 않았고, 그들의 파일·판정·통합 코드를 수정하지 않았다. 이 감사의 쓰기 대상은 이 파일 하나이다.

첫 읽기 UTC는 `2026-11-22T22:29:02.209947+00:00`이다. 첫 root sources 스냅샷은 239개 영수증/54개 최소수 산입 저작이었고, SHA-256은 `7ccb875e0b20c62a70104b881eb05587e900a8fab942a6680ff0f862bade634d`였다. 조사가 진행 중이므로 이후 수정과 재조립을 다시 읽었다. 22:33:01 UTC에는 416/54, 마지막 후속 대조에는 445/54였다. 영수증 추가와 독립 최소수 산입 저작의 증가는 같은 지표가 아니다.

아래 입력 지문 스냅샷 UTC는 `2026-11-22T22:33:53.189674+00:00`이다. 경로와 SHA-256을 `경로<TAB>SHA-256`으로 이어 붙이고 행 사이에 LF를 둔 manifest의 SHA-256은 `da4dcd30a797e2eb61ab78a716d4585cf0717430e5fb4be904ed24bf8721debb`이다. 원장 작성이 계속되었으므로 이 지문은 영구 최종판을 인증하지 않는다.

|읽은 파일|스냅샷 SHA-256|
|---|---|
| `assemble.py` | `dff5bcc34202ae3b0d7a2dd2b9094ff02ce3cd6a8c260006b25193bcbe211700` |
| `synthesize.py` | `3ec4c3ecc779f20299699f11e109a9b1c1b438ffa607f03f6f258d6f7547883e` |
| `baselines.csv` | `808dd0990a66f63738ba70ecf48e8d04bdc7679b5a1bad432212e164cd751592` |
| `events.csv` | `962f9c058ea61f19de8d879dc166c0105dce3dc0876f1b039544a12c058829ed` |
| `sources.jsonl` | `09c48b822a5ffcf9f167302563174025efa2a002595eb97b406160b238e5cc7b` |
| `cases.json` | `1061f4b038cde4280caad85363c2aef4b3c34ce44281864396ed832e968b1626` |
| `evidence/statistics.json` | `303f685034a51522ec30f7157057d0ee90432dbc09ef89a3c248889480588fdb` |
| `sensitivity.csv` | `ac390f6b7df07fe67eb85a3c3d4e4e63a1ff441c1c283d59669125b8c7487802` |
| `streams/pandas/cases.json` | `924411849f09e25ae7d4afd0223ecfd821bcc684b9626b9d3f3c509391eff143` |
| `streams/pandas/changes.csv` | `9494b2351032dd2dc937c0f9b8c2dae9364cf1d4aab69b740424627ac9312856` |
| `streams/pandas/labor.csv` | `271679ede2550d8970387b5a119d6d9345407c10a8b5af93d53b48b1408eab71` |
| `streams/pandas/sources.jsonl` | `af042e150079f11d176bd5fd9cfce0992bbe5b5e52af6dd8adbec349f9fa6d7a` |
| `streams/pandas/additional-sources.jsonl` | `cb7aa789ebb0f68cdd3b4127619943736f09fcce56e1a8b24a2998e690a2cb76` |
| `streams/sklearn/cases.json` | `8b4217cec888a1fe028964febca7859d7a27727038211db885bd27234cf47180` |
| `streams/sklearn/changes.csv` | `8acd6e2acb4027e3529abfa98fcc97760c815c57f77798f243dd264315fad0b0` |
| `streams/sklearn/labor.csv` | `44a47c7705e683beeb6f01b737e53501c9785099e412b0646ef5b772bb5ac57b` |
| `streams/sklearn/sources-supplement.jsonl` | `8cd3ff118595fddd64e23e1d9725d22203d0ab6d042e1efe7d811c3d1b767413` |
| `streams/sklearn/sources.jsonl` | `9520c62b6ac9ceb648b737af3d5e6cc67284116658752de5a8d2590bfe2441dc` |

부모 조사자의 추가 요청에 따라 `synthesize.py`, root `cases.json`, `evidence/statistics.json`, `sensitivity.csv`도 읽었다. 22:33:53 스냅샷의 sklearn cases 지문 `8b4217ce…`와 통계에 기록된 이전 입력 지문 `ce5e1259…`는 달랐다. 최신 여섯 sklearn 사례의 링크/동일 작성자/타인 포함/엄격 사슬/관측창/노동/자기보고 일곱 지표는 root cases와 모두 일치했지만, 최종 재생성으로 입력 지문을 맞추는 작업은 별도로 필요하다.

## 발견한 실제 불일치와 처리 상태

|ID|최초 확인한 불일치·위치|영향|후속 확인·최소 조치|
|---|---|---|---|
|D1|초기 `assemble.py` 67–68행은 `sources.jsonl`·`sources-supplement*.jsonl`만 읽어 pandas `additional-sources.jsonl` 두 행을 누락했다. root에는 sklearn 보충 자료도 아직 들어오지 않았다. pandas changes CSV 17행의 `P-C-ce2bedb9f8f1` 등이 root source ID로 해소되지 않았다.|실제로 읽은 후속 패치의 근거 영수증이 통합 원장에서 끊겼다. 최소수는 별개로, 이 두 pandas 추가 자료는 산입 false였다.|통합 담당에게 보고했다. 22:33:01 재판독에서 pandas 두 행과 sklearn 보충 12행의 누락 ID는 없어졌다. 이후 보충 영수증 증가로 최신 총 영수증 445, 최소수 산입 54를 확인했다. 마지막 작성 이후 다시 조립해야 한다.|
|D2|초기 root `baselines.csv`의 sklearn 여섯 `window_end`는 `pending_postfreeze_closure_read`였지만 cases/labor에는 실제 종료창이 있었다. 초기 assemble 135행은 `window_end_90d` 또는 frame에 의존했다.|baseline을 기계적으로 읽으면 관측창을 확정하지 못하고 시간 감도와 사례표가 다른 기록을 사용할 수 있었다.|통합 frame의 종료창 갱신 후 재조립한 여섯 값을 22:33:01 재판독했다. root baseline과 cases/labor의 관측창이 일치했다.|
|D3|pandas `cases.json` L-P1의 `same_author_change.linked_change_already_started_prelink=false`는 같은 파일의 경쟁 설명 및 changes `L-P1-2`와 맥락 없이 읽으면 충돌한다. 타인 핵심 구현 `f516f4f…`/PR51784는 첫 링크 전에 공개되었다.|타인 포함 감도에서 이 false를 ‘선행 수정 없음’으로 사용하면 L-P1을 잘못 남긴다. 동일 작성자 선행 수정과 모든 작성자의 같은 목적 선행 구현이 다른 조건이다.|root cases에서 `prelink_same_author_redesign_confirmed`와 `prelink_any_author_same_purpose_implementation_confirmed`가 분리된 것을 확인했다. L-P1은 false/true, L-P2는 true/true다. 원stream의 좁은 의미를 설명하고 root의 분리된 조건으로 집계해야 한다.|
|D4|sklearn `labor.csv` L-S1의 실제 변경 파일은 처음에 `sklearn/_engine/exceptions.py`였지만 changes `S-C08` 및 source `S-L1-C1`은 `sklearn/exceptions.py`이다.|고친 파일의 실제 범위가 원장 사이에서 달랐다. 사람 시간이나 사슬 개수에는 영향이 없다.|수정 요청 후 22:33:01에 raw labor의 `sklearn/_engine/testing.py;sklearn/exceptions.py`를 직접 확인했다. 최종 root labor도 마지막 재조립본을 사용해야 한다.|
|D5|최신 sklearn cases는 `8b4217ce…`인데 당시 statistics 입력 지문은 `ce5e1259…`였다.|주요 지표가 우연히 같아도 통계 재현 지문이 실제 최종 입력을 가리키지 않는다.|핵심 일곱 지표는 여섯 사례 모두 동일함을 대조했다. sklearn 작업 종료 후 synthesize 재실행, statistics의 input SHA와 실제 파일 SHA 일치를 확인해야 한다.|
|D6|통계의 자연층 `same_author_changes=0`·`any_author_changes=0`는 ‘첫 적격 링크 뒤 변화’ 계산이다. 자연층 원사례에는 N-P1의 실패 리뷰 뒤 코드 수정, N-S3의 유지보수자 시험 변경 등이 있다.|조건을 생략하면 ‘자연층은 수정이 없었다’라는 틀린 결론이 된다. root cases의 자연층 값은 null인데 sensitivity의 ‘confirmed’ 값은 false여서 특히 해석에 주의해야 한다.|필수 표와 통계 설명에 **첫 적격 링크 뒤 같은 목적 변화의 확정수**라고 명시한다. 무링크 자연층의 이 조건부 비율은 분모 0이므로 해당 없음이며, 일반 수정 유무를 0으로 대입하지 않는다.|

## 원문 할당과 동일 저작

최신 통합 원장에 기록된 최소수 산입 54개를 `work_id`로 직접 다시 묶었을 때 중복 산입은 0이었다. 초기 판에서도 산입 true의 URL·source_id·원 work_id 중복은 없었다. 단일 PR 본문/일반 댓글과 별도 review ID, 동일 commit의 여러 파일을 구별하는 통합 규칙을 확인했다. 이 검산은 원장상의 저작 식별이 일관적인지를 확인한 것이며 모든 원문의 저작 경계를 새로 독립 판독한 것은 아니다.

|배당|현재 최소수 산입|사용자 최소 배당과의 관계|
|---|---:|---|
|PR 원 제안·초기 구현 출처|10|최소 8 이상. 역사적 구현 회수와 최초 공개 head 입증은 별도이다.|
|별도 review ID의 설계 결정/리뷰|14|최소 5 이상. 같은 review 안 여러 inline을 추가 저작으로 계산하지 않는다.|
|commit 또는 시험 변경|21|최소 6 이상. 동일 commit의 파일 여러 개는 한 저작이다.|
|링크가 가리킨 원대상|6|최소 3 이상. 현재판 열람이 과거 시점 가용성을 자동 입증하지 않는다.|
|MusicBrainz 운영 규칙|1|읽은 규칙 배당이다. 특정 edit의 원장·노트·적용 이력 배당을 대신하지 못한다.|
|MusicBrainz 실제 편집 원장|0|필수 분야 자료가 미달이다. 공개 포럼의 당사자 진술을 원장으로 승격하지 않았다.|
|OpenStreetMap changeset 원장|1|해당 배당 확인. 같은 원장 여러 댓글은 한 저작이다.|
|OpenStreetMap 객체 버전|1|해당 배당 확인. 같은 객체 여러 버전은 한 저작으로 보수 산입한다.|
|합계|54|총수 26 이상은 충족하지만, 분야 필수 배당은 3/4로 미충족이다.|

따라서 **54 ≥ 26이라는 전체 수량 충족으로 MusicBrainz ledger 부족을 해소할 수 없다.** sources의 `X-MB06`은 공개 포럼 대화이고 `adjacent_music_discussion_not_required_edit_ledger`로 산입 false다. `X-MB01`의 편집 노트 규칙, 별도 서비스 운영 설명 또는 일반 문서를 더 세더라도 특정 편집의 앞뒤·적용 상태라는 미충족을 메우지 못한다. 원장의 접근 실패/검색요약/재방문을 최소수로 세도록 바뀐 징후는 확인하지 못했다.

## 12사례와 행위자·시간순서 감도

두 stream cases는 각각 여섯 사례, root baseline/cases는 자연층 8개+링크 우선층 4개의 고유 슬롯이었다. successor PR·관련 issue·공개 리뷰 수는 이 12사례 분모에 추가되지 않았다. 자연층 첫 적격 reviewer 링크는 0/8, 링크 우선층은 4/4이다. 링크 우선으로 선별한 4/4를 링크의 일반 발생률로 해석할 수 없다.

|링크 우선층 계산 규칙|링크 사례 분모|동일 작성자·같은 목적 후속 변화 확정|동일 작성자 변화 미확인|타인 포함 변화 확정|엄격 첫 링크 사슬|
|---|---:|---:|---:|---:|---:|
|고정 네 사례 전체|4|2|1|4|0|
|동일 작성자가 같은 설계 변경을 미리 시작한 L-P2 제외|3|1|1|3|0|
|타인까지 포함해 같은 목적 구현이 미리 시작된 L-P1·L-P2 제외|2|1|1|2|0|

이 표의 숫자는 새 statistics와 root cases에 맞았다. L-S1의 동일 작성자 변화는 **미확인 1건**이며 ‘수정 안 함’으로 0 대입하지 않았다. L-P1은 복구한 원PR 기록에서 동일 작성자 후속 수정이 관측되지 않은 경우와 구별된다. 타인 포함 4/4에는 기존 대안의 후속 보정·실제 merge가 포함되므로 ‘링크가 네 번 새 수정을 일으켰다’라는 뜻이 아니다.

30일 창의 링크 우선층에는 L-S1·L-S2의 두 링크만 남는다. 슬롯 분모는 여전히 4이고, 링크가 창 안에 있는 조건부 분모는 2이다. 동일 작성자 변화는 슬롯 기준 1/4, 창 안 링크 기준 1/2; 타인 포함 변화는 2/4와 2/2다. 60일·90일은 네 링크와 동일 작성자 2·타인 포함 4로 돌아온다. L-P2 후속 PR52089의 공개 patch는 원PR 종결 직전이지만 merge는 그 이후이므로, 주 창 내 patch와 종결 후 merge를 합쳐 완성된 주 창 내 배포 사슬로 만들면 안 된다. 해당 한계는 pandas changes `L-P2-6`에 남아 있다.

일반적인 사전 실패·광범위 작업과 ‘이 정확한 후속 수정의 선행 patch’를 구별하는 것이 필요하다. L-S1/L-S2의 기존 문제·작업만으로 실제 같은 수정이 링크 전에 시작되었다고 새 확정 판정을 만들지는 않았다.

## 사람 노동과 선택 한계

양쪽 labor 원장의 12개 관측창에 대해 종료시각−시작시각을 재계산했고, 기록된 경과 초 12개가 모두 일치했다. 이 계산은 작업시간 검증이 아니다. 원장에는 표본 작성자의 주 창 내 능동 작업 로그 0건, 수치적 소요시간 자기보고 0건, 동등 품질의 사람 시간 비교쌍 0건으로 기록되어 있다. saved seconds는 null/미확인이지 0초가 아니다. 프로그램 benchmark, CI 실행, 주말, commit 수를 인간 시간으로 환산한 값은 이 원장들에서 발견하지 못했다.

다만 `S-SUP-25261`은 소비자 gerardkr의 PR 개설 전 ‘many hours’ 디버깅 자기보고를 기록한다. 이는 수치가 특정되지 않은 다른 사람의 선행 비용이며 표본 작성자의 링크 후 수정 시간에 넣을 수 없다. 그러므로 최종 문구는 **“이 12표본의 관측창 안에서 작성자의 측정 가능한 노동시간을 확보하지 못했다”**가 맞다. 조사 전체 어디에도 사람이 들인 시간의 언급이 없다고 쓰면 이 자료와 충돌한다.

N-S2는 선정 시점 잠정성과 이후 review1233732288을 통한 `d5a1cbaf…` 회수 기록이 함께 유지되어야 한다. 현재 역사적 구체 구현 12개 회수라는 집계와 최초 공개 head 입증 0개라는 집계는 양립한다. R01의 선별 도중 수정, L-P2/L-S1의 후속 reviewer 발언 노출, 현재 body의 최초판 동일성 미확인은 최종 통계가 만들어졌다고 없어지지 않는다. 이 항목들의 상세 판정은 같은 디렉터리의 `selection-audit.md`에 남아 있다.

## 재개 첫 행동

최종 원문·사례 파일 작성이 멈춘 뒤 마지막 `assemble.py`와 `synthesize.py`를 순서에 맞게 재실행하고, 통계의 입력 지문·root baseline 관측창·root labor 경로를 다시 확인한다. 그다음 결과와 수용 원장에 MusicBrainz ledger 미충족, 최초 공개 head 미확인, 완전 결과 가림 미충족을 유지했는지 대조한다. 이 감사에서 해결된 결합 오류를 다시 열린 결함으로 보고할 필요는 없지만, 부분 충족을 완전 충족으로 바꾸는 근거로 사용해서도 안 된다.

