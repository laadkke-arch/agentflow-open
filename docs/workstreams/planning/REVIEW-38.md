# REVIEW-38 · 선례를 발견한 뒤 실제 설계에서 달라진 것

이 탐색기는 만들려는 소프트웨어의 전체 구조 또는 선택한 부분과 목적을 받아, 참고할 제품·서비스·기능·다른 분야의 원리를 원문 링크로 건넨다. 지금까지는 특정 조건에서 어떤 링크가 불완전한지, 어떤 입력·판에서 그 설명이 맞는지까지 시험했다. 사람이 그 링크를 보고 전에 없던 선택을 했는지, 부품을 도입한 팀의 총작업량이 줄었는지는 여전히 열린 질문이다. 38차 일반 계획은 **사람의 전후 설계, 한 요청의 실제 입고 결과, 선택 구간의 실제 변환 출력, 부품을 도입한 팀의 후속 작업**을 각각 증거 단위로 삼는다. [제품 브리프][product] · [연구 운영 규칙][workflow]

## 검토 기준과 진행표

계획 브랜치 `work/planning`의 최신 파일은 `240f00f`의 REVIEW-37이었다. 그 파일이 기준으로 삼은 통합판 `ecdf28e`과 **2026-11-24 15:43:47 UTC**의 `f140af3`에서 진행표 전체를 ID로 대조했다. 기존 146행은 모든 필드가 같았다. 추가된 149~152 네 행은 모두 RUNNING이고 등록 결과 SHA가 없다. **37차 이후 새 DONE은 0건**이다. 현재 150행은 DONE 144(연구 142·연결 시험 2), RUNNING 4, BLOCKED 2다. 차단된 연구는 018의 동일 예산 웹 검색 비교와 035의 호출 경계 값·타입 보존이다. DONE 144행 모두 중앙 `acceptance_evidence`가 빈 배열이므로 행의 상태만으로 실험 수용을 판단할 수 없다. [직전 검토][r37] · [직전 진행표][c37] · [38차 기준 진행표][c38]

37차의 보조 Dot은 149에서 자료 유입 경로와 언어권, 150에서 여러 주소·판본·기능의 동일성 및 정정, 151에서 목록 편입·유보·재심사, 152에서 새 자료 발굴과 기존 자료 점검 예산을 조사한다. 38차 네 작업은 이미 정해진 선례, 부품 또는 입력을 사용한다. 각각 145·146·148·147의 고정 인계로 시작하며 보조 Dot과 표본·작업 브랜치·납품물을 공유하지 않는다. [보조 Dot의 작업 지시][p37]

## 1~37차에서 이어받을 결론

| 설계 질문 | 근거가 있는 결론 | 설계자가 아직 선택해야 하는 것 |
| --- | --- | --- |
| 모르던 원리를 찾고 적용할 수 있는가 | 002는 완성품·부품·원리를 발견한 경로와 기여 부분을 기록했다. 010은 분야 단서를 받고 원리 7군을 찾았고, 단서 없는 033의 144쌍에서는 당시판 지지 0이었다. 022의 ‘미인지→결정 변경→시행’은 0/24였다. 141에서 Matplotlib 작성자는 링크를 받기 전 외부 타입 스텁을 알고 있었다. | 출전 제시, 첫 인지, 새 시험 제안, 실제 선택·배포는 따로 입증해야 한다. 이미 알던 부품도 실패 조건을 가르칠 수 있다. [누적 근거][r37] · [145의 판정][ad145] |
| 어느 부분과 문맥을 받아야 하는가 | 020은 주장 72/73을 전달했어도 충돌을 모두 푼 것이 2/16이었다. 119의 공개 도표 6건은 요구만으로 정확 0, 이웃 또는 직접 참조를 주었을 때 각각 3이었다. 103에서는 외관 10/10을 지키면서 텍스트 선택을 잃었고, 107에서는 단일 발생 편집이 공유 정의에서 0/6, 위치 지정에서 6/6이었다. 144의 CSV 열은 잘못된 날짜 하나로 명령 성공 뒤에도 Text로 남았다. | 선택한 객체, 보존할 값, 소비자·다음 조작 중 무엇이 답을 바꿨는지가 필요하다. 전체 프로젝트 제출이나 고정 Studio API는 근거가 쌓인 선택지가 아니다. [36차 검토][r36] · [148의 저자 근거][auth148] |
| 자료를 묶고 더 깊이 읽으면 어떤 답이 살아나는가 | 040의 실제 8요구는 묶기에 따라 부분 근거를 8개 또는 6개 보존했으나 완전 적격은 0/8이었다. 044의 관측 8풀은 두 묶음 방식이 같았다. 118은 충돌을 제거하면서 일부 근거도 숨겼다. 142의 잠정 신규층 72표시 자리는 전부 비었다. | 재고 밖, 점수 0, 낮은 순위, 읽은 뒤 보류는 원인이 다르다. 146이 회수한 세 절을 연결했을 때 사용자 요구 전체가 성립하는지도 별도의 질문이다. [37차 검토][r37] · [표시 전환][tr146] |
| 무엇을 남겨야 다시 꺼내 쓸 수 있는가 | 003에는 짧은 메모로 충분한 사례와 별도 정정이 필요한 사례가 있었다. 023의 18사건은 허용 병합 5, 정정·분리·되돌림 9, 기타 4였고 문자 그대로 오병합을 고친 것은 그 9건 중 3이었다. 055의 옛 판단은 4/4, 다음 판 판단은 0/4였다. 071은 절·설정으로 과거 22/22를 복원했고, 075는 전체 후보가 없어 단독·공동 1위 주장을 각각 16/16 보류했다. | 북마크, 그때 전달한 근거의 감사, 현재 요청의 적합성 및 후보 간 우선순위는 각각 다른 정보를 요구한다. 연구 원장의 열을 제품 DB로 확정할 근거는 없다. [37차 검토][r37] · [147의 비용·복원][cost147] |
| 다시 읽을 시점과 비용은 무엇이 결정하는가 | 019는 같은 신호가 엄격 대조 7쌍의 사건 3·대조 3건에 울렸다. 024의 분기 상한 20에서는 정기 점검 11/11, 신호 점검 8/11로 무효화를 찾았다. 후자는 원문을 108개 덜 읽고 수신 본문은 5,672,462바이트 더 컸다. 135의 같은 README 아래 null 기본 출력이 바뀌었고, 143의 5,696셀쌍에서 수치 변화 양성은 없었어도 공개 진입의 실패·회복은 관측됐다. | 요청 분포와 정확판, 실제 취득·대기·판독 비용을 함께 봐야 한다. 대규모 운영 주기와 예산은 보조 Dot의 미결 과제다. [37차 검토][r37] · [36차 검토][r36] |
| 근거를 하나 더 주면 일을 덜 하는가 | 021에서 두 절을 볼 수 있을 때 근거 충분은 주소만 6/23, 맞춘 절 14/23이었다. 034의 부분 시간은 380→57초였으나 전체는 849→847초였다. 140에서 두 번째로 연 7개 절이 만든 새 핵심 해결은 0건이었다. | 링크를 찾아낸 시간, 읽고 판단한 시간, 구현·검토·호환·운영 노동은 다른 비용이다. 코드 감소량이나 PR 경과시간에서 총노동을 추정할 수 없다. [37차 검토][r37] |

누적 수치 세 가지도 유지한다. 114의 충돌로 분류된 138/144쌍은 118의 명시 반박 기준에서 충돌 7·미확인 131이고 나머지 6은 일부였다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 고유 면은 본문 해시 기준 9개이며, 열람 10회 및 답과 면의 연결 16쌍과 분모가 다르다. [앞선 정정 근거][r36]

## 네 인계에서 어디까지 믿을 수 있는가

아래는 37차에서 이미 DONE으로 집계한 네 작업이다. 이번 일반 계획을 고르는 데 필요한 원장 수치와 인계판을 연결했다. 이 검토에서 원장 행과 범주를 다시 센 부분은 자체 집계다. 소프트웨어 실행과 당시 열람에 관해서는 작업자가 저장한 결과·영수증을 인용한다.

| 작업·등록 인계판 | 확인한 단위 | 확인한 결과 | 얕게 남은 부분과 잘못된 해석 |
| --- | --- | --- | --- |
| 145 · [116eae3 · PARTIAL][h145] | 모집 80, FreeCAD·Joplin 전체/부분 각 4건, R0 사전안·수정안 8쌍. 원전 38행 중 산입 고유 25저작 | 한 작성자의 자기 판정은 새로운 시험·조건 6, 경계 1, 핵심 선택 유지와 후속 경계 시험 1이다. 예컨대 J-P1의 양방향 Tab 포커스 기준은 검색 전에 있던 Tab 시험을 구체화했을 수도 있다. | 8건에 각 한 검색 조건만 노출했고 두 조건의 유효 짝 0/8, 독립 초안 0/16, 실행한 대상 시험 0이다. B 질의 두 건에 이미 알던 ezdxf·SAF가 들어갔고 기록관리·제조 원전은 주 관측 뒤 열었다. 신규 6을 ‘처음 몰랐던 사람이 설계를 바꾼 비율’로 쓸 수 없다. [판정][ad145] · [검색 이력][search145] · [결과][r145] |
| 146 · [9bf267b · 작업자 COMPLETE / REVIEW_READY][h146] | 새 요청 4×12후보의 별도 판독 48쌍, 원전 147행 중 고유 27저작 | 직접 0·일부 15·충돌 14·미확인 19. 표시 3자리를 유지하고 검토 3→8에서 조건부 표시 1→4, 공석 11→8, 검토한 충돌 6→10, 표시된 충돌 0→0이었다. 추가된 P01·P04·L01은 모두 P-A의 5·7·8위였다. | 명시 원본을 돌려받아 해시를 비교하려면 먼저 입고가 성공해야 한다. 해당 판의 서명 파일로 입고·무 OCR·서명 유효성을 시험한 기록은 없다. 판독한 25쌍 중 7개는 게이트와 별도 모델 판독이 달랐다. 세 링크는 한 요청의 세 단계다. 142 자료에서 살아난 직접 1건도 이미 답을 본 좁은 교정 요구였고, 새 6요구에서는 0이었다. [결과][r146] · [판정 원장][truth146] · [전환][tr146] · [정확판 검사][check146] |
| 147 · [30afd11 · REVIEW_READY][h147] | 두 계열 8판·32셀, 인접 판 비교 24쌍, 원전 58행 중 고유 28저작 | 24쌍 중 효력값 변화 4·불변 20. Beirut의 같은 UTC 순간은 2023a EEST→2023b EET→2023c EEST였다. 정확히 요청판을 조회한 A/B/C는 밀집 현재 96건 전부 맞았다. 주소의 마지막 답만 쓴 별도 대조는 오승인 40·오거절 32·정답 24였다. | C는 고유 입력 64개의 과거 질의 112/112에 당시 근거를 돌려줬다. A/B는 각각 112건 보류였다. 추측을 피한 보류지만 ‘당시 전달 증빙 제공’ 계약에서는 원장이 wrong_hold로 채점했다. 미리 보지 않은 인접 12쌍의 값 변화는 0이고, 단절·TTL은 구성 사건이다. 공식 tar/ZIP은 해당 환경에서 열리지 않아 공급자 고정 트리를 사용했다. 준비 때의 전송량은 운영 중 재검증비나 소비자의 이관 노동을 알려주지 않는다. [결과][r147] · [32셀][oracle147] · [답 원장][ans147] · [비용][cost147] · [검사 영수증][check147] |
| 148 · [7afb573 · PARTIAL][h148] | 모집창 60행 중 개별 판독 18, 잠정 6사건, 패킷 18. 출처 38행 중 본문을 연 고유 저작 32, 종류별 하한 충족 21/24 | E2·E3·E5는 같은 입력의 기대 출력을 현재 작성자 본문에서 확인했다. E2는 두 텍스트 셀 중 둘째가 누락된다는 당사자 보고다. E4의 입력 함수는 addCartItem, 기대 출력 함수는 updateCartItem이었다. | 최초판 0/6, 가림 준비가 된 패킷 0/18, 실제 독립 판독 0/18, 유효 비교 0/6이다. E2의 B는 A에 있던 27자를 되풀이했고, 양쪽 추가 분량이 0보다 크고 같은 사례는 E4의 66자/66자뿐이었다. E6은 후속 PR의 변경이 드러난다. 실제 원면 및 총보·파트의 동일 마디 비교도 미완이다. 최소 입력안 두 개는 아직 가설이다. [결과][r148] · [저자 근거][auth148] · [패킷][packs148] · [미실시 원장][reads148] |

## 모순처럼 보였던 세 결과와 다음 관측

| 불일치·약점 | 설명이 갈리는 지점 | 무엇을 보면 판단을 바꿀 수 있는가 |
| --- | --- | --- |
| 참고한 뒤에 작성한 시험은 있지만 독자가 새 결정을 했다는 근거가 약하다. 기술적으로 맞는 부품도 팀의 일을 줄였다고 단정하기 어렵다. | 한 모델의 수정, 사람의 예시 배정·열람, 실제 배포 및 노동을 서로 바꿔 셀 수 없다. 작성자가 이미 알던 기능도 이관·호환에 시간이 든다. | **153**은 기존 공개 사람 실험의 동일 참여자 전후 작품과 대조군을 연결한다. **156**은 이미 알려진 시간대 부품을 도입한 소비자 두 곳에서 없어진 일과 새로 맡은 일을 배포 이력으로 추적한다. |
| 후보를 더 읽자 세 링크가 돌아왔는데도 작성자가 요구한 한 가지 완결된 작업은 확인되지 않았다. | 원본을 보관한다는 약속, 명시 원본을 회수하는 인터페이스, 바이트를 비교하는 절차의 전제가 다르다. 하나는 다른 둘이 시작되기 전에 실패할 수 있다. | **154**는 같은 서명 PDF를 실제로 넣어 입고 결과·OCR 호출·원본과 기본 반환·실패와 재시도를 같은 실행에서 연결한다. 바로 안내할 수 있는 조건과 더 확인할 조건을 남긴다. |
| 차트의 이웃 정보는 실제 선택을 갈랐지만 문서 패킷에서는 관련 문맥을 더한 효과를 측정하지 못했다. | 다른 사례군이고, 한쪽의 ‘이웃’은 이미 본 내용이거나 다른 함수·후속 정답이었다. 출력 결과와 독자의 선택도 서로 다른 측정이다. | **155**는 고정 Pandoc·Prettier 입력에서 실제 소비 조건과 무관한 형제를 구분한다. 동일 선택이 서로 다른 출력에 이르는지 재생하고, 필드 하나로 구분할 수 있는지 확인한다. |

## 일반 계획의 배정

| ID·담당 | 유일한 선행 | 작업자가 넘길 독립 결과 |
| --- | --- | --- |
| AF-RES-153 · web-pro | 145 | 사람이 받은 자극, 사전·사후 설계, 적용한 연산과 무변경·악화 사례를 연결한 표. 비교군이 없는 결과에는 인과효과를 계산하지 않는다. |
| AF-RES-154 · codex-cloud | 146 | 서명·텍스트 유무가 다른 PDF의 실제 입고와 반환을 두 새 환경에서 검사한 원장. 파일 해시, 서명 무결성, OCR 호출, 실패 로그를 각각 판정한다. |
| AF-RES-155 · codex-cloud | 148 | 선택한 문서 구간이 같을 때 관련 생산자·소비자 조건으로 달라지는 실제 변환 출력과 기술적으로 필요한 최소 입력 예 두 안. |
| AF-RES-156 · web-pro | 147 | Django·pandas의 부품 전환 제안·패치·시험·배포·후속 부담을 연결한 원장. 코드량·경과일·당사자가 밝힌 작업시간에 각각 자기 단위를 유지한다. |

네 지시문에는 작업별 자료 하한과 조사창, 필수 결과표, 반례, 분모 재집계, 중간 커밋과 인계 기준이 들어 있다. [PLAN#38 작업 지시문](NEXT_TASKS-38.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/f140af3179b7d9271710778104ccee5b4812e2ef/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/f140af3179b7d9271710778104ccee5b4812e2ef/docs/RESEARCH_WORKFLOW.md
[r37]: https://github.com/laadkke-arch/agentflow-open/blob/240f00fd7c1385c6f606f521b64e0b3663436a2d/docs/workstreams/planning/REVIEW-37.md
[p37]: https://github.com/laadkke-arch/agentflow-open/blob/240f00fd7c1385c6f606f521b64e0b3663436a2d/docs/workstreams/planning/NEXT_TASKS-37.json
[r36]: https://github.com/laadkke-arch/agentflow-open/blob/45124eaaba085ecab86bfe96c68db26fcdfdcb1c/docs/workstreams/planning/REVIEW-36.md
[c37]: https://github.com/laadkke-arch/agentflow-open/blob/ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19/docs/automation/dot-control.json
[c38]: https://github.com/laadkke-arch/agentflow-open/blob/f140af3179b7d9271710778104ccee5b4812e2ef/docs/automation/dot-control.json
[h145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/HANDOFF.md
[r145]: https://github.com/laadkke-arch/agentflow-open/blob/2f41c8650ff45e531ce501118cc8b28296c74db9/docs/workstreams/research/AF-RES-145/RESULT.md
[h146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/HANDOFF.md
[r146]: https://github.com/laadkke-arch/agentflow-open/blob/91b10340abca933bb2696ff7372c3168999892ac/docs/workstreams/research/AF-RES-146/RESULT.md
[h147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md
[r147]: https://github.com/laadkke-arch/agentflow-open/blob/3a6794815caedd96f06752e042f11143f664861d/docs/workstreams/research/AF-RES-147/RESULT.md
[h148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/HANDOFF.md
[r148]: https://github.com/laadkke-arch/agentflow-open/blob/cde2c875e2ebf57bf1c161c2bee9f5f5ff6d75aa/docs/workstreams/research/AF-RES-148/RESULT.md
[ad145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/adjudication.csv
[search145]: https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/discovery.jsonl
[truth146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/truth.csv
[tr146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/transitions.csv
[check146]: https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/evidence/checks.json
[oracle147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/oracle.csv
[ans147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/answers.csv
[cost147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/costs.csv
[check147]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/evidence/acceptance.json
[auth148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/author-evidence.csv
[packs148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/packets.jsonl
[reads148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/readings.jsonl
