# REVIEW-17 · 설계 중인 프로젝트에서 발견한 대안과 그 대안을 믿을 근거

**이번 회차의 설계 판단은 외부 자료, 추천받는 프로젝트의 요구, 둘을 이어 주는 근거를 각각 식별할 수 있어야 한다는 것이다.** 한 URL이 반대되는 두 권고에 실제로 제공됐고, 결과표를 조립하는 과정에서 한쪽에만 제공된 근거가 다른 쪽 행에도 들어갔다. 원문과 시작 위치를 정확히 저장해도 해당 부분의 두 필수조건이 충족되는지는 새로운 질문이다. 새 자료에서 끝까지 확인한 것은 이 구분이 필요한 구체적인 경우다. 아직 가장 중요한 제품 질문은 개발자가 원 분야를 알려주지 않아도 실제로 쓸 새로운 선택을 찾는지, 그 이득을 얻는 데 언제 얼마만큼의 자료를 보관하거나 다시 읽어야 하는지다. [권고와 원래 출처 자리][sl66] · [결과 표][r66] · [조건별 판독][ju68] · [제품 브리프][product]

## 기준과 판정

2026-11-23. 계획 브랜치에 있는 최신 [REVIEW-16][prev]을 먼저 읽고, 그 검토의 통합 기준 [028d16f][oldreg]와 이번 기준 [320424d][reg]의 모든 작업을 ID로 대조했다. 등록 62→66건, DONE 60→64건, BLOCKED 2→2건이다. 기존 62행의 변경은 없었다. 018·035는 계속 BLOCKED이며 결과 커밋이 없다. 새 DONE은 아래 네 건뿐이다. **네 건 모두 부분 인계**이고 중앙 DONE 64행의 `acceptance_evidence`는 전부 빈 배열이다. 각 연구의 수용 원장과 산출물을 따로 읽었다. [운영 규칙][workflow]

| 작업 | 중앙 인계판 / 본문판 | 실제 인계한 자료 | 완료되지 않은 핵심 비교 |
| --- | --- | --- | --- |
| 065 · 인쇄 원리와 사진·악보 | [18e4449][h65] / [796e712][r65] | 요구 본문 후보 8건, 현재 설명이 원전을 지목한 구현 1종 | 규칙에 맞게 선정된 최초 요구 0/8, 인용 사건 확보 0/4, 역사적 선택부터 출력까지 연결된 사건 없음 |
| 066 · 권고에 붙은 세 출처 | [367f29c][h66] / [d736df8][r66] | 12문항·24권고·72자리·67주소의 연결, 일부 직접 판독 및 반례 | 당시·현재 134개 판 행의 도착 본문 해시 미기록. 세 링크를 모두 검증해 결론을 낸 권고 0/24 |
| 067 · 빌드·천문 보정의 과거 입력 | [b55c924][h67] / [a4b0c47][r67] | 규격·기록 문서 12건과 소스 업로드 공지 9건, 선언과 실제 읽기에 필요한 근거 구분 | Debian 바이너리 원 빌드 0/4 확보, JWST 원 보정 산출물 0/4 확보. 비교 가능한 원실행이 없어 복원율 산출 불가 |
| 068 · 요구에 쓰인 이름으로 문서 열기 | [2c9642d][h68] / [9d46186][r68] | 12요구·36열람 경로, 고정 배포판 시험 16군·시도 24회 | 두 조건과 환경을 함께 직접 확인한 요구 0/12. 사람이 얻는 이득과 원작성자 실행 환경 미확인 |

네 작업 모두 원장의 결과 SHA가 조사 당시 작업 브랜치 끝과 같았다. 각 마지막 커밋은 HANDOFF.md 한 파일만 추가했고 본문 blob은 직전 커밋과 일치했다. 이번 검토에서 Git 원본 CSV·JSONL의 행·열·조인·분모를 다시 계산했다. 068은 고정 자료의 인덱스·판정·출력 구조 검사도 재실행했다. 외부 사이트의 당시 원문이나 네 연구의 실험 전부를 새로 열고 실행한 것으로 계산하지 않았다. [065 수용][a65] · [066 수용][a66] · [067 수용][a67] · [068 수용][a68]

## 이전 회차에서 이어지는 결론

제품은 만들고 있는 소프트웨어의 **전체 또는 선택한 부분과 목적**을 받아, 완성품과 사이트, 개별 기능, 다른 분야에서 옮겨 볼 원리를 찾아 그 위치로 안내한다. 기존 Studio 입력 형식은 바꿀 수 있다. 비교할 저장 방식에는 요청 시 처음 찾아 읽기, 주소·짧은 설명 저장, 버전·조건별 근거와 판단 이력 추가가 모두 포함된다. 아래는 최신 검토가 인계한 실제 표본의 결과다. 수치와 분모의 해석이 달라질 수 있는 021·030·032는 원 인계를 다시 열어 바로잡았다. 제품 전체의 정확도나 비용으로 확대할 수 없다. [이전 누적 검토와 원자료 위치][prev] · [제품 연구의 열린 선택][product]

| 설계자가 내려야 할 결정 | 064까지 얻은 근거와 남은 한계 |
| --- | --- |
| 어떤 문장과 주변 구조를 받아야 하나 | 초기 6개 합성 입력에서 부정 조건이 누락됐다. 020은 주장 72/73을 전달했지만 충돌 16건 중 완전 해소는 2건이었다. 026의 실제 추가 질문 발송은 0건, 030의 일반 선정층(A)에서는 직접 답변 3건 중 엄격한 권고 변경이 0건, 답변 우선층(B)에서도 직접 답변 6건 중 0건이었다. [030 원표][fix30] 필요 문맥을 계속 늘릴 근거는 부족하다. |
| 분야가 달라도 유용한 원리를 찾을 수 있나 | 010은 분야 단서와 원전 24개로 원리 7군을 찾았다. 011의 타 분야 답 14개에는 요청자 반응이 없었다. 013의 당시 선례 회수는 웹 16/176, 목록 5/176. 033의 분야 단서 없는 144쌍은 넓은 기준 지지 1쌍, 당시판 지지 0쌍이었다. 012의 합성 근접 오답 증가는 014의 실자료 485개에서 재현되지 않았다. |
| 원전이 실제 선택을 바꾸나 | 022의 결정 우선 24건에서 미인지→변경→시행을 모두 이은 것은 0건, 발견 진술 우선 9건에서는 1건이었다. 046의 보강 층에서는 첫 링크를 수정 이유로 명시하고 시험까지 이은 사례가 0/4였다. 061의 두 보기를 실제로 비교한 6행은 예측 차이 0/6이었다. 원전만 새로 맞힌 비율은 비교 분모가 0이라 계산할 수 없다. |
| 근거를 붙여 전달하면 더 나은 판단을 하나 | 021의 두 절 예산에서 공식 지지와 근거를 함께 회수한 건수는 주소만 6/23, 절 목록 9/23, 요구–절 대응 **14/23**, 잘못 대응한 보기 8/23이었다. 직전 검토의 13/23을 원 인계에 맞춰 정정한다. [021 원표][fix21] 034의 패키지 선택 시간은 380→57초였지만 전체 과제는 849→847초였다. 054의 네 과제 정확 완료는 3/12 대 1/12, 단일 과제는 3/12 대 4/12였다. 058은 전체 정답과 오권고 수락이 함께 늘었고, 062의 출처 제공과 자유 검색 권유는 오수락 방향도 달랐다. 038 자체의 실제 참가자는 0명이었다. |
| URL·판·사용 증거 중 무엇을 보관하나 | 015의 현재 판단 가능 이유 195개 중 14개가 무너졌다. 032의 배포 HTML 출발층 12참조에서 현재 용도는 유지 9·교체 2·보류 1이었다. 같은 목적을 향한 배포 링크 자체의 변경은 5/12참조·4사건이었다. 주소 응답만으로 둘을 가를 수 없다. [032 원표][fix32] 023의 과거 이유 복원은 주소·이유 3/18, 판·근거 추가 5/18, 변경 관계·시점까지 15/18. 055는 옛 답을 0/4→2/4→4/4 복원했지만 다음 판 판정은 세 보기 모두 0/4였다. 059의 배포 파일과 063의 원보고를 결합해도 실제 소비 프로세스가 연 파일의 판은 대개 미확인으로 남았다. |
| 후보를 찾고 첫 링크를 주면 두 조건이 확인되나 | 040의 URL·상류·부품별 묶기가 보존한 조건은 8·6·8개였다. 060의 용어·기능 필드 확장은 후보 있는 요구를 기존층 0/8→4/8, 새 층 0/4→2/4로 늘렸지만 고유 28쌍에서 공동 완결은 0이었다. 064에서는 6/11쌍의 첫 주소가 바뀌고 표시 단어는 6,948→5,747로 줄었다. 같은 예산 안에서 두 조건과 환경이 확인된 쌍은 양쪽 모두 0/11이었다. |

## 새 DONE 네 건에서 무엇을 믿을 수 있나

### 065 · 아이디어의 출처와 역사적 채택 경로

React Photo Album의 현재 설명은 인쇄의 Knuth–Plass에서 얻은 영감을 직접 지목한다. 사진 행의 선택에 목표 높이와의 편차 비용을 사용한다는 대응은 설명할 수 있다. Flickr의 유사성은 연구자의 가설이고, 악보의 강제 줄바꿈과 고정 페이지 요구는 전체를 다시 나누는 방식이 사용자의 의도와 어긋날 수 있는 실례 후보다. 그 작성자가 인쇄 원전을 접한 뒤 설계를 바꿨는지에 대한 증거는 다르다. [대응 4행][me65] · [결과][r65]

모집표의 12행 모두 기간과 최초 순번 검증이 `no`다. 결정표 48행 중 최초 글을 읽은 것은 8행이고, 뒤 40행은 미추적이다. 출처 원장 15행 중 14행은 잠정 산입이고 1행은 제외여서 독립 원저작 20건 조건에 미달한다. 모집표는 12행 모두 중복 없음으로 기입했지만 결과와 인계는 중복 미확인으로 판정했다. 이 자료로 중복률을 계산할 수 없다. 현재 설명의 출처를 활용하는 것은 가능하고, 최초 선정 사건의 대표성이나 사람이 그 원리를 채택한 비율은 평가할 수 없다. [모집표][fr65] · [결정 이력][de65] · [출처][so65]

### 066 · 한쪽에 제공한 근거가 다른 쪽 권고로 이동한 사례

72개 원래 자리는 보존됐다. 그런데 결과 표의 달·심해 정권고 행에 인용한 NASA는 실제 오권고의 S11에만, 폐·피부 정권고 행에서 쓴 USGS는 실제 오권고의 S18에만 제공됐다. 연구자가 공통 배경을 설명할 때는 쓸 수 있는 자료다. 당사자에게 실제 제공된 근거를 계산할 때에는 해당 권고의 세 자리만 써야 한다. 양쪽에 **실제로** 재사용된 5주소에서는 현재판의 양방향 코드가 5/5쌍 모두 같았다. 예컨대 Port Royal의 허가 조건은 반대되는 S68·S71에서 모두 부분으로 표기됐다. 공통 전제가 어느 선택을 지지하는지는 확인해야 한다. [두 정·오 행][mx66] · [자리별 제공물][sl66] · [방향별 명제][cl66]

현재 고유 주소 67개 중 일부 절을 열었다는 행은 30, 별도 확인 전은 19, 차단·빈 응답은 18이다. 당시판의 3개는 062에서 인수한 것이고 64개는 미확인이다. 144개 자리×판 행을 만들었지만 전부 명제 ID가 `P0`이고, 현재 72자리에서 직접 지지는 2자리, 반박도 2자리다. 같은 문항의 여러 자리를 독립적인 권고 성공으로 셀 수 없다. **0/24는 세 출처를 결합한 감사가 끝난 권고 수**다. 피험자의 독해·선택과도 연결되지 않았다. [판별 접근 기록][ve66] · [권고 결합 기록][ad66] · [수용 조건][a66]

### 067 · 최소 저장 필드를 비교할 실물과 평가 분모

규격은 설치됐을 수 있는 의존 목록, 보정 파일 선택 문맥, 특정 파일명에 대해 어떤 주장이 가능한지 설명한다. 실제로 소스 업로드 공지에 `_amd64.buildinfo`라는 이름이 남을 수 있었다. 그래서 이름에 아키텍처가 들어 있다는 사실만으로 어떤 바이너리의 어느 빌드가 그 파일을 읽었는지를 연결하면 틀린다. 연구가 확보한 21개 문서는 규격·아카이브 12개와 소스 업로드 공지 9개다. 지정한 8자리에는 원 출력이 한 건도 들어오지 않았다. [출처][so67] · [5개 영수증][rc67]

모집 CSV를 파싱하니 헤더 14열, 실제 8행은 **전부 13열**이다. 헤더로 읽으면 `output_url`에 ‘모집 미완’이 들어가고 마지막 열이 비어 버린다. 형식 행 수만 세면 놓치는 결함이다. 24개 보기의 ‘실제 제공 필드’는 전부 같은 문자열이고, 옛 출력·입력 라벨·읽은 바이트 3열의 72칸이 모두 미확인이다. 잡을 수 없었던 사례 8건을 8번의 복원 실패로 해석해서는 안 된다. 저장 전략별 차이를 측정하려면 같은 소비 실행의 요청·실제 입력·출력을 직접 관찰할 수 있는 대조군이 필요하다. [모집 CSV][fr67] · [보기 CSV][vi67] · [수용 조건][a67]

### 068 · 먼저 보여 준 절, 그 절에서 확인한 조건, 실행 결과

README 시작(A), 기능 표제(B), 요청에 쓰인 이름(C)의 세 경로를 같은 12요구·후보에 적용했다. A와 C는 11/12에서 첫 목적지가 달랐다. 36경로 모두 첫 창만 열렸고 규칙상 적격인 둘째 행동은 0이었다. 19개 위치에 서로 다른 내용 해시가 18개였다. C1·C2의 72개 판정은 전부 미확인이다. B는 환경 전제 3건을 직접 찾았고 실제 표시 엄격층에서는 그중 1건을 유지했다. 검색에서 특정 이름을 찾는 것과 그 부분이 두 조건을 만족하는지를 확인하는 것은 서로 다른 결과다. 정해진 두 번째 행동이 일반 웹 탐색에서도 무용하다고 추정할 수 없다. [경로][rt68] · [조건과 환경][ju68] · [열람 규칙][ru68]

고정 배포판 시험은 16군·24시도였고 봉인한 기대 전부와 일치한 것은 9/16이다. 값 평가 12군, 컴파일 단계 진단 4군이다. 저자가 정확히 적은 배포판을 시험한 A02 네 군은 모두 컴파일 단계에서 멈췄다. 서로 다른 이슈의 환경을 섞어 ‘사용자 요청이 실행에서 9/16 성공했다’고 쓰면 틀린다. 최초 본문이 불확실한 10건, 한 사람이 수행한 가명 판독, 실제 표시를 엄격히 재현하지 못한 4/36경로가 남는다. 인계는 최종 검증판의 원격 재독과 계약 통과를 보고한다. 저장된 두 영수증이 가리키는 판은 앞선 `2303024c`다. 후속 주장은 인계문에 근거한 보고로 남긴다. 재현 문서도 Node 배포 디렉터리로 이동한 뒤 저장소로 복귀하는 줄이 빠졌다. 같은 셸에서 마지막 계약 검사를 실행하려면 저장소 루트로 돌아와야 한다. [재현 절차][repro68] [실행 원장][rn68] · [노출][ex68] · [저장된 재독 영수증][rr68] · [저장된 계약 영수증][ck68]

## 설계에 넘길 판단과 PLAN#17

| 서로 어긋나 보이는 결과 | 설계자가 지금 쓸 수 있는 판단 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 원전의 명시적 귀속은 있고, 과거 채택 사건은 없었다. 분야명이 없는 탐색에서 새 선택을 얻는지도 열려 있다. | 직접 쓸 기능과 타 분야 원리를 모두 찾되, 원리에는 원 역할·대응 동작·깨지는 조건·다음 시험을 붙인다. 실제 채택 이력은 별도 근거에 귀속한다. | 현재 진행형 문제를 먼저 고르고 같은 예산에서 분야 단서를 주지 않은 탐색이 추가한 실행 가능한 선택을 확인한다. |
| 링크를 더하거나 더 좁은 절을 주면 이점이 있으나, 반대 선택도 같은 링크를 공유하거나 전제만 확인된다. | 질문의 선택 범위·필수조건과 각 후보의 적용 구성을 함께 보존한다. 하나의 추가 정보가 두 대안의 판단을 가르는지 비교한다. | 최초 질문에서 고정한 판정을 추후 작성자가 실제로 밝힌 한 필드와 대조한다. 정보가 추가돼도 판단이 같거나 오히려 잘못된 사례를 함께 센다. |
| 과거 설명을 재생할 수 있는 저장 방식이 다음 판의 적합성까지 보장하지 않는다. 더 많이 저장하면 탐색이 쉬워질 수 있지만 처음부터 무엇을 읽었는지에 따라 비용이 달라진다. | 요청·판·실제로 읽은 자료와 답을 별도 키로 연결할 수 있게 하고, 주소만 저장하고 요청 때 읽는 안도 비교에 남긴다. | 변경·무변경에 대한 재판정과 옛 답 재생은 통제 실험에서 측정한다. 발견 성능과 총 취득 비용은 별도 동결 자료에서 요청 시 열람 경로까지 허용해 측정한다. |

| 다음 작업 | 동결된 선행 | 답할 질문과 후속 설계 결정 |
| --- | --- | --- |
| 069 · web-pro | 065 | 원 분야를 알려주지 않은 실제 개발 문제에서 일반 탐색에 없던 부품·원리를 찾는가. 발견과 적용 가설을 구분할 기준을 얻는다. |
| 070 · web-pro | 066 | 부분 요청에서 주변 정보 한 가지가 후보 판단을 가르는가. Studio가 처음 넘길 필드와 나중에 물을 필드의 범위를 좁힌다. |
| 071 · codex-cloud | 067 | 실제 읽은 입력과 출력을 관찰할 수 있는 같은 실행에서 어떤 저장 필드가 과거 답과 변경 뒤 판단을 복원하는가. 이력과 재점검의 비용을 비교한다. |
| 072 · codex-cloud | 068 | 질문이 온 뒤 URL의 본문을 여는 방식과 용도 정보를 미리 보관하는 방식이 같은 탐색 예산에서 어떤 결과와 비용을 내는가. 자료집의 기본 저장량·취득 시점을 판단한다. |

네 작업은 서로의 새 결과·계정·사람 응답을 기다리지 않는다. 069는 열린 웹의 새 후보, 070은 요청 맥락, 071은 시간에 따른 동일 실행과 근거, 072는 고정 자료집의 검색·취득 비용을 다룬다. 사람의 실제 선택이나 노동시간 개선을 관측하지 않은 비교는 그 효과까지 입증하지 않는다. 각 작업의 모집 순서, 판별 자료, 표 열, 중간 커밋과 완료 조건은 [작업자에게 전달할 지시문][next]에 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/e4c6a79f4fd1f4e3028b4407cf1c7433fe2eacd9/docs/workstreams/planning/REVIEW-16.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/028d16fee1121f5862efd410b78ec1d79d7080f2/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/320424d87f99e70c42eeb8cb7211467de27f2c2e/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/320424d87f99e70c42eeb8cb7211467de27f2c2e/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/320424d87f99e70c42eeb8cb7211467de27f2c2e/docs/RESEARCH_WORKFLOW.md
[next]: NEXT_TASKS-17.json
[h65]: https://github.com/laadkke-arch/agentflow-open/blob/18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d/docs/workstreams/research/AF-RES-065/HANDOFF.md
[r65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/RESULT.md
[a65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/evidence/acceptance-evidence.json
[me65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/mechanisms.csv
[fr65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/frame.csv
[de65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/decisions.csv
[so65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/sources.jsonl
[h66]: https://github.com/laadkke-arch/agentflow-open/blob/367f29c6eb8f3da36c7728eb133f1cca9078efbf/docs/workstreams/research/AF-RES-066/HANDOFF.md
[r66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/RESULT.md
[a66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/evidence/acceptance-evidence.json
[sl66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/slots.csv
[mx66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/RESULT.md#L13-L16
[cl66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/claims.csv
[ve66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/versions.csv
[ad66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/advice.csv
[h67]: https://github.com/laadkke-arch/agentflow-open/blob/b55c9248fa56a67b99ec3430734e7c41e16196c9/docs/workstreams/research/AF-RES-067/HANDOFF.md
[r67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/RESULT.md
[a67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/evidence/acceptance-evidence.json
[so67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/sources.jsonl
[rc67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/receipts.csv
[fr67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/frame.csv
[vi67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/views.csv
[h68]: https://github.com/laadkke-arch/agentflow-open/blob/2c9642dff48ec0da2785c2c127d3a906182f7834/docs/workstreams/research/AF-RES-068/HANDOFF.md
[r68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/RESULT.md
[a68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/acceptance-evidence.json
[ju68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/judgments.csv
[rt68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/routes.csv
[ru68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/rules.json
[rn68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/runs.jsonl
[ex68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/actual-exposure.json
[rr68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/verification/remote-reread.json
[ck68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/evidence/verification/session-check.json
[repro68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/reproduce.md#L47-L64
[fix21]: https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/HANDOFF.md#L9-L17
[fix32]: https://github.com/laadkke-arch/agentflow-open/blob/b4dcf0a1ca3f2066629869ac1a9347ad2f5717df/docs/workstreams/research/AF-RES-032/HANDOFF.md#L7-L16
[fix30]: https://github.com/laadkke-arch/agentflow-open/blob/3f77073d6294b739bb340b23e3c4c10640c5b08c/docs/workstreams/research/AF-RES-030/HANDOFF.md#L3-L7
