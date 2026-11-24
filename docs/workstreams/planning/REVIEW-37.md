# REVIEW-37 · 프로젝트에 도움이 될 자료를 어떻게 발견하고 오래 쓸 수 있게 관리할까

이 제품은 만들고 있는 소프트웨어의 전체나 일부와 목적을 받고, 참고할 만한 제품·서비스·기능·원리를 찾아 원문으로 안내한다. 이번 연구 질문은 **어떤 자료가 발견될 기회를 얻고, 그중 무엇이 어떤 설계 요청에 다시 쓰일 수 있도록 남는가**다. 제공자가 원문을 계속 관리하는 경우, 자료가 여러 곳으로 갈라지는 경우, 사용자에게 필요해진 뒤 찾아도 충분한 경우를 모두 설명할 대안이 필요하다. 특정 사이트, 인기도 신호, DB 구조나 수집 방법의 채택은 열려 있다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

## 검토 기준과 새 인계

2026년 11월 25일 한국시간 기준으로 계획 브랜치의 가장 최근 REVIEW-36을 먼저 읽고, 거기서 사용한 통합판과 새 통합판의 작업을 ID로 대조했다. 기존 142행은 그대로였고 새 145~148 네 건이 모두 DONE으로 인계됐다. 전체 146행 중 DONE 144건(연구 142, 연결 시험 2), BLOCKED 2건이다. 018의 동예산 웹 검색 비교, 035의 호출 경계 값·타입 보존이 차단 상태다. 중앙의 DONE 144행에서 acceptance_evidence는 모두 빈 배열이다. 아래에는 각 작업자가 남긴 수용 상태와 검사 범위를 별도로 적었다. 36차까지의 전개는 직전 누적 검토를 이어받았고, 이번 주제에 빠져 있던 발굴·정정·선별·점검 근거는 해당 고정 인계에서 추가로 확인했다. [직전 누적 검토][previous] · [직전 진행표][oldcontrol] · [이번 진행표][control]

| 새 인계 | 실제로 확인된 것 | 결론의 한계와 판단 |
| --- | --- | --- |
| 145 · 선례를 읽은 뒤의 설계 수정 · **PARTIAL** | 모집 80자리에서 8건을 골랐다. 같은 작업자의 사전 초안·수정 8쌍 모두가 판별 시험을 제안했다. 산입한 외부 원전 25저작이다. [인계][h145] · [결과][r145] · [판정 원장][a145] | 독립 두 조건의 유효 비교는 0/8사건, 독립 초안은 0/16자리였다. 제안한 시험의 실제 실행 0건이고 원저자 채택·사람 시간은 미확인이다. 특정 경로가 더 좋은 결정을 유발했다고 말할 근거가 없다. |
| 146 · 내부 검토 깊이와 실제 후보 풀 · **작업자 COMPLETE / REVIEW_READY** | 새 요청 4×12후보의 별도 판독은 직접 0·일부 15·충돌 14·미확인 19였다. 검토 폭 3→8에서 표시된 조건부 링크 1→4, 빈자리 11→8이었다. 추가 세 링크는 모두 같은 서명 PDF 요구에 속했다. [인계][h146] · [결과][r146] · [48쌍 원장][a146] | 세 링크는 원본 보관·명시 원본 회수·바이트 점검에 각각 기여한다. 실제 서명 파일의 입고·유효성은 미확인이다. 25개 판독 중 이견 7개였다. 검토 폭을 늘려 이미 있는 하위 후보를 회수한 것에서 목록 밖 새 후보의 발견 효과를 추정할 수 없다. |
| 147 · 현재 근거와 과거 답의 재생 · **REVIEW_READY** | tzdb·CLDR 2계열 8판 32셀의 실제 원전을 읽었다. 현재판을 정확히 지정한 세 방식 모두 밀집 질의 96건의 값과 근거가 맞았다. 주소의 마지막 값만 이월한 별도 대조에서는 오승인 40/96건이었다. 당시 전달과 근거를 기록한 방식은 64개 고유 입력에 대한 과거 질의 112/112건을 재생했다. [인계][h147] · [결과][r147] · [32셀 원장][a147] | 112건에는 반복 질의가 있다. 관측·결정 이력을 보관할 가치는 요청의 과거 답을 증빙해야 할 때 확인됐다. 미리 보지 않은 12개 인접 경계에서는 변화가 0이었다. 원격 전송량, 운영 중 변경률, 대규모 목록의 최적 확인 주기는 미측정이다. |
| 148 · 선택 구절 및 이웃 문맥 · **PARTIAL** | 잠정 6사건의 현재 본문을 고정하고 전달 패킷 18개를 만들었다. 같은 입력의 기대값을 원저자 현재 본문에서 확인한 것은 3/6건이다. 32개 고유 저작 열람, 종류별 최소치를 적용하면 21/24개 충족이다. [인계][h148] · [결과][r148] · [판독 원장][a148] | 최초 본문 확보 0/6, 실제 독립 판독 0/18, 유효 비교 0/6이다. 한 사례는 서로 다른 함수였고 다른 사례에는 후속 수정이 섞였다. 문맥을 더 주면 추천이 나아진다는 결과나 최적 입력 계약은 미확인이다. |

이 검토에서는 등록 인계 SHA의 결과 본문과 사건·판정 원장을 대조했다. 145는 8개 판정행에 모두 ‘비교불가’, 146은 48쌍 중 직접 판정 0, 147은 32셀 전부 판독 가능, 148은 18개 판독 슬롯 전부 미실시로 재집계됐다. 실험의 실행·속도·원문을 읽은 횟수는 각 작업이 보존한 기록의 범위에서 인용했다.

## 1~36차에서 이어지는 설계 판단

| 나중 설계자가 결정할 문제 | 현재까지 남은 근거 | 여전히 열린 판단 |
| --- | --- | --- |
| 새 자료를 찾으면 실제 설계가 달라지는가 | 002는 전체 제품·부품·원리를 찾는 경로와 기여 부분을 기록했다. 010은 분야 단서가 있을 때 7개 원리군을 찾았다. 단서 없는 033은 144쌍에서 당시판 지지 0이었다. 022에서 미인지→변경→실행으로 이어진 것은 0/24였다. 141의 Matplotlib 사례에서는 원저자가 링크를 받기 전부터 외부 스텁을 알았다. [002 인계][h2] · [36차 누적 근거][previous] | 발견, 독자의 첫 인지, 시험 제안, 실제 채택과 사람의 절감 시간은 서로 다른 관측이다. 145가 더한 것은 한 독자의 초안 전후다. |
| 요청의 어느 부분이 적격 여부를 바꾸는가 | 020은 73개 중 72개 주장을 전달했으나 충돌을 전부 해결한 경우는 2/16건이었다. 119의 실제 요구 6건은 선택부만 주면 정확 0, 이웃 또는 직접 참조를 주면 각각 3이었다. 144의 csvkit에서는 명령 두 개가 성공해도 유효하지 않은 값 하나 때문에 열이 텍스트로 남았다. 078·103·107·131은 부품의 겉보기 결과가 같아도 다음 조작이나 적용판에서 달라지는 조건을 찾았다. [36차 누적 근거][previous] | 어떤 근거가 특정 요청의 조건을 충족시키는지 판정해야 기능 하나나 타 분야 원리의 쓸모를 알 수 있다. 148이 남긴 조건은 후보이며 독립적인 효과 측정은 열려 있다. |
| 목록을 더 많이 읽거나 묶으면 더 좋은 대안이 나오는가 | 040은 실제 8요구에서 묶음 방법에 따라 부분 근거 8개 또는 6개를 보존했고 완전 적격 요구는 0/8이었다. 044의 관측 8풀에서는 주소 기준과 조건까지 본 방법의 결과가 같았다. 118은 충돌 표시를 걷어내면서 일부 근거도 숨겼다. 142의 잠정 신규층에서 72자리가 비었고 146의 검토 확장 이득은 특정 요구에 집중됐다. [040 인계][h40] · [044 인계][h44] · [36차 누적 근거][previous] | 각 요청에서 일시적으로 표시할지, 장기 목록에서 계속 보존할지, 다른 분야에선 유일한 기능일지는 서로 다른 결정이다. 적격 0건인 표본에서는 완전 대안의 회수율 분모가 없다. |
| 무엇을 저장하면 오해와 과잉 정리를 피할 수 있는가 | 003은 짧은 메모로 충분한 사례와 별도로 정정할 필요가 있는 사례를 함께 남겼다. 023의 실제 18사건 중 허용 병합 5, 정정·분리·되돌림 9, 기타 4였고 그 9건 중 문자 그대로의 오병합 정정은 3건이었다. 055는 옛 판단 4/4, 다음 판 0/4였다. 071은 절·설정으로 옛 사례 22/22를 복원했다. 075는 전체 후보가 빠져 단독/공동 1위 판정을 각각 16/16 보류했다. [003 인계][h3] · [023 인계][h23] · [36차 누적 근거][previous] | 현재 원문에 도달하기, 옛 인용이 가리킨 기능 찾기, 당시 최선이었다는 근거 복원하기는 요구하는 기록량이 다르다. 어디서 비용을 더 낼지는 미결이다. |
| 언제 다시 읽어야 하고 그 비용은 얼마인가 | 019의 엄격 대조 7쌍에서 같은 신호가 사건 3건·대조 3건에 울렸다. 024의 분기 상한 20에서 정기 확인은 무효화 이유 11/11, 신호 뒤 확인은 8/11을 찾았다. 신호 방식은 원문을 108개 덜 읽고도 수신 본문이 5,672,462바이트 더 컸다. 106은 주소가 살아도 예제의 쓰임이 사라진 사례를, 135는 같은 README 아래 출력이 바뀐 사례를 확인했다. 143의 5,696셀쌍에서 값 변화 양성은 0이었지만 공개 진입 실패와 복구는 관측됐다. [019 인계][h19] · [024 인계][h24] · [36차 누적 근거][previous] | 열람 수·네트워크 바이트·사람의 판독·새 자료 발견 지연은 다른 비용이다. 이미 등록된 자료를 보는 예산과 새 공급원을 찾을 예산을 어떻게 나눌지에 관한 운영 근거는 부족하다. |
| 근거가 하나 더 있으면 노동을 덜 수 있는가 | 021에서는 같은 두 절 예산으로 맞는 절을 줬을 때 14/23건, 주소만 줬을 때 6/23건의 근거가 충분했다. 034는 부분 시간 380→57초, 전체 849→847초였다. 140에서 추가 7절이 만든 새 핵심 해결은 0건이었다. [36차 누적 근거][previous] | 사람이 실제로 덜 읽거나 재작업을 피했는지는 기술 원전의 존재와 별도로 관측해야 한다. 채택률이나 운영비의 보편값은 아직 없다. |

이전 수치의 정정도 이어간다. 114의 ‘충돌’ 138/144는 118의 명시 반박 기준에서 충돌 7·미확인 131이었고 나머지 6은 일부였다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 본문 해시 기준 고유 면 9개, 열람 10회, 답과 면의 연결 16쌍은 서로 다른 단위다. [누적 정정 근거][previous]

## 이번 배정에서 풀 세 가지 불일치

| 불일치·약점 | 지금 말할 수 있는 범위 | 다음 조사에서 판단을 바꿀 관측 |
| --- | --- | --- |
| 조사 깊이를 늘리니 부분 후보는 돌아왔지만 목록 밖의 좋은 후보를 얼마나 놓쳤는지는 알 수 없다. | 146은 이미 들어 있던 자료에 대해 검토 예산의 효과를 측정했다. 145의 다른 분야 원전 일부는 발견을 끝낸 뒤 대조용으로 골랐다. | 다른 언어·분야의 독립 유입 경로에서 똑같은 요구와 열람 예산으로 처음 얻은 유용한 후보, 겹친 후보, 소득이 없던 경로까지 확인한다. |
| 중복을 줄이는 편집이 어떤 요청의 유일한 대안을 지울 수 있다. | 023의 카탈로그 정정, 040·044의 화면에 남은 후보, 147의 과거 답을 재생한 이력은 서로 다른 결과를 측정했다. | 동일성과 추천 가치를 따로 대조한다. 여러 번 들어온 한 대상을 합친 뒤 옛 인용을 복원할 수 있는지와, 낮게 평가한 별개의 후보가 다른 요구에서 참고 가치를 갖는지는 각각 원자료로 판단한다. |
| 원문을 제공자가 갱신하면 독자가 최신 내용을 읽을 수 있지만, 예전에 찾은 이유가 지금도 성립하는지는 별도 문제다. | 024의 주기 비교와 147의 정확판 관측은 제한된 자료와 예산에서만 결과를 냈다. 구성된 장애 시계열도 실제 사이트의 중단율은 알려주지 않는다. | 신규 발행·접근 복구·살아 있는 주소의 내용 변화·장기 안정 사례를 같은 시간축에 놓고, 상시 재고를 거의 두지 않는 방식까지 포함해 지연·오판·비용을 비교한다. |

## 다음 작업과 인계물

| 작업 | 작업자가 독립적으로 답할 질문 | 나중 설계자가 비교할 자료 |
| --- | --- | --- |
| AF-RES-149 · web-pro | 서로 다른 언어와 분야에서 아직 모르던 유용한 자료가 어떤 경로로 들어오는가? | 동일 예산 유입 경로표, 단독 기여와 중복, 미발견 사례, 다른 분야에서 가져온 발굴 방식 |
| AF-RES-150 · codex-cloud | 여러 주소·판본·부분 기능의 관계가 바뀔 때 무엇을 같은 것으로 기억할 수 있는가? | 실제 정정 전후 이력을 여러 저장 방식으로 재생한 조회 원장, 오병합과 되돌림의 비용 |
| AF-RES-151 · web-pro | 비슷한 후보를 어떤 요구에서 남기고 보류하거나 재심사할 이유가 있는가? | 요구별 대안 비교 원장, 낮은 평가가 뒤집힌 조건, 유일한 기능을 잃거나 중복 보존한 비용 |
| AF-RES-152 · codex-cloud | 새 자료 발굴과 기존 자료 점검의 시점·예산을 어떻게 배분할 수 있는가? | 공개 사건을 이용한 시간순 재생, 이용 분포·예산별 지연과 오판, 소규모 실측과 대규모 추정의 경계 |

네 작업은 각각 별도의 브랜치·소유 경로·모집틀을 쓰며 선행 입력은 이미 인계된 고정 커밋이다. 각 작업자는 서로 다른 현장에서 대안을 먼저 발굴한 뒤 비교 기준을 고정한다. 합리적인 단순 대안, 아무 차이도 나오지 않은 결과, 예상한 우열이 뒤집힌 사례도 다음 설계자에게 전달한다. 조사·원장·검산·인계의 구체적인 지시와 필수 표는 배정 파일에 있다. [작업자별 PLAN#37 원문](NEXT_TASKS-37.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19/docs/RESEARCH_WORKFLOW.md
[previous]: https://github.com/laadkke-arch/agentflow-open/blob/45124eaaba085ecab86bfe96c68db26fcdfdcb1c/docs/workstreams/planning/REVIEW-36.md
[oldcontrol]: https://github.com/laadkke-arch/agentflow-open/blob/9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673/docs/automation/dot-control.json
[control]: https://github.com/laadkke-arch/agentflow-open/blob/ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19/docs/automation/dot-control.json
[h2]: https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/HANDOFF.md
[h3]: https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/HANDOFF.md
[h19]: https://github.com/laadkke-arch/agentflow-open/blob/034ba6e2360301be23c49c66cf42af5c36f9e534/docs/workstreams/research/AF-RES-019/HANDOFF.md
[h23]: https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md
[h24]: https://github.com/laadkke-arch/agentflow-open/blob/4af1300841c1c39f9ef6e76d78579034d1ae0c51/docs/workstreams/research/AF-RES-024/HANDOFF.md
[h40]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/HANDOFF.md
[h44]: https://github.com/laadkke-arch/agentflow-open/blob/6c8c025284215c7749921619cb09c89643886276/docs/workstreams/research/AF-RES-044/HANDOFF.md
[h145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/HANDOFF.md
[r145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/RESULT.md
[a145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/adjudication.csv
[h146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/HANDOFF.md
[r146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/RESULT.md
[a146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/truth.csv
[h147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md
[r147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/RESULT.md
[a147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/oracle.csv
[h148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/HANDOFF.md
[r148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/RESULT.md
[a148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/readings.jsonl
