# REVIEW-29 · 어느 링크가 설계자의 선택을 바꿀 수 있는가

부분 설계와 목적을 받아 쓸 만한 기능·부품·원리를 링크로 돌려줄 때, 지금 근거가 가장 분명한 것은 **어디에서 판단이 멈췄는지**다. 새 네 작업에서 예제와 출전을 모두 읽어 비교할 수 있던 요청은 0/6이었다. 한국어 별칭은 구성 대조에서 정답 하나를 더 보여 주면서 충돌하는 후보도 네 개 더 표시했다. 작성자의 도형 파일을 받은 유일한 본 사례에서는 고치려던 텍스트가 파일에 없었다. 목차 단서로 두 사건의 열람 경로가 바뀌었지만, 완전한 답에 도달할 수 있다고 입증한 자연 사건은 0건이었다. 이 네 결과로 실제 사용자의 채택이나 재작업 절감량을 산출할 수 없다. [추가 링크][hops] · [표시 결과][t3] · [실제 입력][cases115] · [독자별 경로][pairs]

## 이번에 인수한 범위

계획 브랜치의 최신 파일 [REVIEW-28][prev]을 먼저 읽고, 거기에 고정된 [이전 진행표][old]와 2026-11-24 UTC의 [통합 진행표][reg]를 ID와 행 전체로 대조했다. 기존 110행에는 변경이 없고 AF-RES-113~116 네 행이 새 DONE이다. 전체 114행 중 DONE 112·BLOCKED 2다. 연구만 세면 112건 중 DONE 110·BLOCKED 2(018·035)이며 나머지 DONE 두 건은 AF-DOT 연결 시험이다. DONE 112행의 중앙 `acceptance_evidence`는 모두 비어 있다. 새 네 작업에는 별도 인계와 검사 기록이 있다.

| 새 DONE | 등록된 인계 커밋 | 작업자가 검사한 결과 커밋 | 이번에 인수한 범위 |
| --- | --- | --- | --- |
| AF-RES-113 · 예제와 출전 | [7a8fa21][h113] | [9351759][r113] | PARTIAL. 12자리의 실제 링크 공급·본문 노출·새 선택 판정과 사후에 읽은 반례. 양쪽 경로의 효과 비교 분모 0. |
| AF-RES-114 · 한·영 용어와 역할 | [9695479][h114] | [4e0d3f8][r114] | PARTIAL. 24기능의 순위 재생과 표본층별 판정. 예정한 시간순 자연 요청 0/6, 해당 요청의 실제 조회 0. |
| AF-RES-115 · 부분 파일과 참조 | [7f853bd][h115] | [0da8f40][r115] | PARTIAL. 원본의 저장 객체·상류 변경과 보기별 판정. 본 자연 1/6, 예정한 본 변형 0/12, 같은 판 편집 앱에서 관측한 효과 0. |
| AF-RES-116 · 링크 옆의 목차 단서 | [23b1460][h116] | [31cc131][r116] | PARTIAL. 공개 요청 6건의 AI 수신 18문맥·54단계와 문서면별 가림 채점. 고정 뷰어에서 완전 답 기회 4건 불가·2건 미확인. |

각 등록 SHA는 읽을 때 해당 작업 브랜치의 끝이었고 마지막 커밋에서 바뀐 파일은 각자의 `HANDOFF.md` 하나였다. 인계판과 검사판에서 읽은 `RESULT.md`의 Git blob도 네 쌍 모두 일치했다. 이번 계획에서는 113의 링크·판정·시험 원장, 114의 세 정답 원장과 표시 집계, 115의 사례·재생·바이트 변경, 116의 쌍·54단계 경로·채점 원장을 대조했다. 아래 ‘실행’은 작업자가 보관한 관측이고, 계획 담당은 이 원장의 수와 구분을 다시 확인했다. 이전 연구의 수치와 해석은 직전 누적 검토에서 인수했다. [연구 운영 규칙][rules] · [이전 누적 검토][prev]

## 이후 설계자가 이어받을 근거

제품의 목적은 이미 있는 해법을 일찍 발견해 설계를 되돌리는 비용을 줄이는 것이다. 사용자가 주는 것은 전체 또는 일부 구조와 달성하려는 목적이다. 후보는 완성품, 기능 한 개, 부품, 서비스, 다른 분야의 원리까지 포함한다. 링크·짧은 이유, 저장할 원문 범위, 필요할 때 추가로 묻는 정보는 비교할 대안이다. DB 구조, 상시 크롤러, AI 전처리, Studio 입력 계약은 모두 미결정이다. [제품 연구 브리프][goal]

| 판단할 문제 | 이전 회차에서 남은 핵심 근거 | 새 결과까지 반영한 해석 |
| --- | --- | --- |
| 새 해법을 알게 된 것이 실제 선택을 바꿨나 | 분야 단서를 준 010은 원리 7군을 찾았다. 단서 없는 033의 144쌍에서 넓은 지지 1쌍, 당시판 지지 0쌍이었다. 022의 미인지→변경→시행은 0/24였다. 105의 ‘처음 알았다’ 두 발언은 좁은 조작을 가리켰다. | 109는 12선택·27시험을 제안했지만 원 프로젝트 실행은 0건, 같은 노출·비용으로 비교할 요청도 0/6이었다. 113도 6건 모두 반환 뒤 채택이 미확인이다. 어떤 안을 버리거나 제약·시험을 추가한 것도 설계 변화로 볼 수 있는지 당시 결정 기록으로 따져볼 차례다. [이전 검토][prev] · [113 반환 원장][ret] |
| 사용자가 말한 대상·금지 조건을 보존했나 | 020은 주장 72/73을 전달해도 충돌 완전 해소가 2/16이었다. 070은 자연 요청의 되묻기 효과 분모가 없었다. 074는 구성 입력에서 값을 받으면 8/8을 구별했다. 111은 어순 변경 후 기준 정합 A 5/6·B 4/6, 동의어 변경에서는 각각 0/6이었다. | 111에서 자연 작성자가 준 정규화 대상 ID는 0/6이었다. 115의 자연 파일에는 시작 사각형의 진짜 ID가 있었지만 아직 생성하지 않은 텍스트의 ID는 없었다. 사용자에게 받은 시작점, 편집 대상, 함께 보존할 객체가 각각 무엇인지 확인해야 한다. [이전 검토][prev] · [115 검산][ver115] |
| 자료집에 직접 답이 있고 그것이 표시됐나 | 076의 자연 6요구×20후보에는 직접 적격이 없었고, 080의 목록 확장에서 자연 1/5·교정 3/5가 양성으로 바뀌었다. 096은 인접 자료를 6/6 노출해도 단독 완결 0/6이었다. 110은 24기능×6요구 중 직접 1쌍, 영어 조회가 그 기능을 찾고 한국어는 놓쳤다. | 114에서 공식 별칭의 회수 이득과 잘못 채운 자리를 같은 표에서 처음과 끝까지 셀 수 있다. 자료집의 적격 수, 조사 후보 수, 표시한 직접·일부·충돌·공석, 실제 한국어 작성자 수는 각각 다른 분모다. [이전 검토][prev] · [114 층별 표시][t3] |
| 같은 주소·과거 인용으로 현재 판단을 복원할 수 있나 | 055는 과거 판단 4/4, 다음 판 판단 0/4였다. 071은 조각과 설정으로 과거 자료 22/22를 복원했지만 075에서 유일성·공동 1위를 입증하는 전체 집합은 각각 16/16 보류였다. 086의 당시 제공 관측창은 0/9였다. 106은 같은 주소가 일반 설명을 보존하면서 옛 집단 점수라는 목적을 잃은 경우를 찾았다. | 113은 같은 예제의 첫 3,000자와 뒤 절에서 다른 사실을 읽었다. 116은 같은 fragment 안에 도착하고도 필수 구간의 끝을 못 본 사례를 남겼다. 추천의 판·구간·그때 보인 내용·필요한 다음 자료를 구별할 근거가 있다. [이전 검토][prev] · [113 결과][r113] · [116 도달성][reach] |
| 한 줄의 정보가 독자에게 무엇을 더 주었나 | 021의 두 절 예산에서 충분한 판단은 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 108의 같은 1,200자에서 키워드 4/16, 예외 우선 2/16이었다. 112의 Godot 세 쌍은 반복 설명을 받아도 경로가 같았고 완전 근거 0/6이었다. | 116에서도 반복 문구는 6/6 같은 경로였다. 새 목차 표지는 2/6에서 길을 바꿨다. 준비 시간, 실제 노출, 최종 판단, 사람의 전체 작업시간은 여전히 따로 측정해야 한다. 034의 부분 시간 380→57초와 전체 시간 849→847초가 그 차이를 보여 준다. [이전 검토][prev] · [116 비용·판정][metrics] |
| 일부를 바꿀 때 무엇이 같이 바뀌나 | 078은 단독으로 되던 부품을 연결할 때 실패를, 089·091은 선택색과 편집 대상, 같은 지점과 원래 행의 차이를 보였다. 095는 옆 표 선의 소실, 103은 외관 10/10 보존에도 8자리의 텍스트 선택 소실을 보였다. 107에서 한 발생만 고치는 데 공유 정의는 0/6, 위치 지정은 6/6이었다. | 115의 악보 보조 사례에서 고친 것은 파일 속 주석 한 글자였다. 재생 순서의 비교값은 전부터 맞았다. 저장 레코드의 수정, 화면 영향, 후속 조작이나 재생 결과를 각각 관찰해야 한다. [이전 검토][prev] · [115 바이트·참조 대조][prov] |

## 새 결과에서 확인한 사실과 근거가 끊긴 곳

**113 · 예제 본문 두 개와 출전 초록 한 개를 읽었다.** 두 프로젝트의 첫 60건씩을 모집틀로 고정하고 순서대로 13건을 판독해 6건을 골랐다. 107건은 할당 뒤 미선별이다. R6 대응을 고치자 공통 시작 문서가 4개에서 5개가 됐다. 추가 링크 12자리는 시작 공석 2·링크 공석 7·예제 본문 접두사 2·출전 초록만 1이었다. 실제 3회 열람은 각 3,000자로, 12판정행의 새 선택·새 시험은 모두 0이다. 별도로 확인한 21개 시험·검증행은 중복 선택을 합치면 16군이며 전부 사후 조사다. 원장에서는 시작 링크만 반환 3건·보류 3건이다. [열람 원장][hops] · [선택 판정][d113] · [사후 시험][test113] · [반환 원장][ret]

따라서 예제와 출전의 상대 효과는 미확인이다. ‘예제에는 실패 사례가 없다’는 설명은 같은 gallery 뒤쪽의 먼지 점 소실 사례와 맞지 않는다. 반대로 그 실패는 첫 3,000자 밖에 있어 당시 독자가 본 근거로 쓸 수 없다. R5의 경곗값 설명은 문서의 maximum과 구현의 ignore→min이 충돌한다. 보관된 SciPy 관측과 skimage 공개 호출 전체의 결과도 구별해야 한다. 원 작성자가 훗날 무엇을 바꿨는지, 후속 조치가 이 반환 때문인지는 별도 근거가 필요하다. [113 결과와 반대 입력][r113]

**114 · ‘정답 하나 추가’와 ‘충돌 네 개 추가’가 같은 표시 정책에서 함께 일어났다.** Blender·Krita의 지정된 첫 40건과 40/41 경계를 확보하지 못해 본 자연 144쌍은 전부 공석이다. 따로 확보한 탐색 6건×24기능은 직접 0·일부 6·충돌 138, 구성 4건×24기능은 직접 2·일부 2·충돌 92다. 엄격한 매뉴얼 판에서는 같은 번역 키의 근거가 없어 추가 별칭이 0개였다. 발행자의 앱 번역·한국어 HTML까지 허용한 보조판의 한국어 구성 대조에서 별칭을 켜면 표시한 직접 적격이 1/2→2/2, 확인된 충돌 표시가 2→6이었다. Box Mask가 조사 밖에서 표시 1위로 올라왔고 Clone Layers는 영문 심벌만으로도 찾았다. [예정 자연 원장][nat114] · [탐색 판정][expl] · [구성 판정][ctr] · [표시 집계][t3]

근거의 역할이 어긋난 후보에 벌점을 줘도 그 빈자리는 다른 오답이 채울 수 있다. 영어 탐색층의 충돌 표시가 13→15였고, Box Mask의 출력 태그 하나를 뺀 교란에서는 직접 적격이 조사 1위에 남으면서도 표시 밖으로 밀렸다. 자연 한국어 작성자와 독립 의미 판독은 각각 0이다. ‘한국어 사용자가 더 잘 찾는다’와 ‘충돌에 벌점을 주면 결과가 좋아진다’는 이 자료로 뒷받침되지 않는다. [후보 전수 추적][tr114] · [114 결과][r114]

**115 · 파일에 들어 있는 객체와 사람이 바꾸려는 객체가 갈렸다.** 두 트래커의 시간순 60건씩은 확보했다. 그러나 구조 후보 주소·대체 주소를 조사한 100회 중 터널 거부 99회·기타 HTTP 오류 1회였다. 이 결과로 외부 자료의 만료를 판정할 수 없다. 본 자연 6자리에서 쓸 수 있던 것은 E05 하나였다. 세 보기 중 구조를 준 두 보기는 같은 사각형 382자를 보았고, 새 텍스트와 정확한 실행판을 확인하지 못해 세 보기 모두 보류했다. 본 자연 비교는 3/18자리, 원래 계획한 변형 입력 12개의 비교는 0/36자리다. 길이를 맞추고 직접 참조 보기만 정확한 두 건 CE·CM은 모두 합성 대조다. [사례와 공석][cases115] · [보기별 분모][ver115]

원글이 공식 테스트 자료를 링크한 별도 M60에서는 두 보기 모두 주석의 저장 위치를 찾았다. 앞뒤 59,855바이트 중 한 바이트가 `10`→`19`의 차이를 냈고 C++ 기대열은 전부터 19였다. 실제 앱의 화면·재생 효과는 미확인이다. 두 경로에서 45자리씩 같은 결과가 나왔다는 재현성과 자연 사용자의 선택을 맞혔다는 주장은 다른 근거를 요구한다. [상류 패치와 기대열][prov] · [재생 기록][replay115]

**116 · 길을 바꾼 독자와 답을 확인한 독자를 따로 셀 수 있다.** Pandoc·ImageMagick 공개 요청 6건을 A(링크), B(같은 조건을 반복), C(새 목차 표지)로 인계했다. 각 보기에서 세 번씩 열어 18문맥·54단계를 모두 관측했다. A/B의 문서면은 6/6 같았다. C는 P1·P3에서 두 번째 열람부터 다른 문서면을 골랐다. 선언한 목표와 같은 fragment를 본 문맥은 8/18, 목표 본문 일부를 본 문맥은 I2 세 개(각 106/166자), 전체를 본 문맥은 0/18이다. 같은 문서면이 여러 표지를 갖는 경우도 있어 행동 문자열과 실제 노출을 구분했다. [쌍별 경로][pairs] · [54개 실제 노출][trail] · [도달성 원장][reach]

세 번 안에 완전한 답을 입증할 수 있는 자연 사건은 **확인 0·도달 불가 4·기준 미확인 2**다. 마지막 둘은 P3 원 실행 환경과 I3 동일 JP2 원본이 결손이다. 가림 채점에서 완전 근거 0/54단계, 부분 복원 8/54, 정당한 보류 표지 54/54였다. 부분과 보류는 중복되며 배타 등급은 부분 8·보류 46이다. 전체 비용은 54열람·77,083자였고 사람의 작업시간은 미측정이다. 읽을 수 있는 예산 안에 두 조건이 모두 있는 경우를 따로 모집해야 단서 간 완전 답 효과를 비교할 수 있다. [단계별 채점][ans] · [비용·기준·교정 경로][metrics]

## 다음 네 작업과 판단 기준

| 배정 | 완료된 선행 | 다음 설계자가 새로 알 수 있는 것 | 결론을 제한하거나 뒤집는 관측 |
| --- | --- | --- | --- |
| 117 · web-pro | 113 | 채택하지 않은 외부 선례가 어떤 대안 배제·제약·회귀시험을 실제 결정 기록에 남겼는가. 공개 설계안의 초안·링크 최초 등장·후속 변경을 잇는다. | 근거가 링크보다 앞서거나 설명만 덧붙였으면 ‘링크로 바뀐 결정’의 수에서 뺀다. |
| 118 · codex-cloud | 114 | 고정된 한·영 후보에서 세 자리를 채우거나 근거 부족 자리를 비울 때 어느 직접 적격·부분 근거·충돌을 잃고 얻는가. | 슬롯을 줄여 틀린 답과 함께 정답까지 숨기는 경우를 같은 예산·같은 사례에서 센다. |
| 119 · codex-cloud | 115 | 원 작성자가 공개 본문에 넣은 도표 사양에서 한 객체와 공유 정의를 가를 최소 입력은 무엇인가. 저장 대상과 실제 렌더 결과를 비교한다. | 원문이 중의적이거나 참조 한 단계로 다른 사용처의 변화를 놓치면 부분 파일이 있어도 보류한다. |
| 120 · web-pro | 116 | 공식 기능 절에 바로 가는 링크와 경계 조건을 검사하는 두 번째 자료가, 실제 답이 가능한 경우 독자의 최종 판단을 바꾸는가. | 기회가 있는 요청에서도 사용자가 두 번째 자료를 안 열거나, 맞는 위치에서 다른 판·대상을 확정하면 손실로 남긴다. |

117은 실제 설계 결정의 기록, 118은 고정 후보의 표시, 119는 원 입력의 대상, 120은 반환 뒤의 판독을 맡는다. 각각 완료된 선행 하나와 자기 입력만으로 시작하며 결과를 서로 기다릴 필요가 없다. 표본 모집, 반례, 열람 원장, 필수 표, 커밋과 인계 기준은 각 작업자가 단독으로 읽을 수 있도록 [NEXT_TASKS-29.json](NEXT_TASKS-29.json)에 넣었다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/0be34498f73876fd77867622bf997d4cbc89a0ff/docs/workstreams/planning/REVIEW-28.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/670ecde1dab07aede6760618a7d907f0cdff185a/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/101426a5e76154bb89b642dd9bd3c52fc1229c30/docs/automation/dot-control.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/101426a5e76154bb89b642dd9bd3c52fc1229c30/docs/product/RESEARCH_BRIEF.md
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/101426a5e76154bb89b642dd9bd3c52fc1229c30/docs/RESEARCH_WORKFLOW.md
[h113]: https://github.com/laadkke-arch/agentflow-open/blob/7a8fa21da69d141a7288662b7b556370529259a9/docs/workstreams/research/AF-RES-113/HANDOFF.md
[r113]: https://github.com/laadkke-arch/agentflow-open/blob/9351759623393c87038033de2adf9865a9f7abcc/docs/workstreams/research/AF-RES-113/RESULT.md
[h114]: https://github.com/laadkke-arch/agentflow-open/blob/9695479c8e9e3c36488f3d0376f197733e05ef3e/docs/workstreams/research/AF-RES-114/HANDOFF.md
[r114]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/RESULT.md
[h115]: https://github.com/laadkke-arch/agentflow-open/blob/7f853bd85c57ad3657a7bed4962a3c8eaeed8433/docs/workstreams/research/AF-RES-115/HANDOFF.md
[r115]: https://github.com/laadkke-arch/agentflow-open/blob/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115/RESULT.md
[h116]: https://github.com/laadkke-arch/agentflow-open/blob/23b14602ad6d400be6e00966815812a6b36cb0e6/docs/workstreams/research/AF-RES-116/HANDOFF.md
[r116]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/RESULT.md
[hops]: https://github.com/laadkke-arch/agentflow-open/blob/9351759623393c87038033de2adf9865a9f7abcc/docs/workstreams/research/AF-RES-113/hops.jsonl
[d113]: https://github.com/laadkke-arch/agentflow-open/blob/9351759623393c87038033de2adf9865a9f7abcc/docs/workstreams/research/AF-RES-113/decisions.csv
[test113]: https://github.com/laadkke-arch/agentflow-open/blob/9351759623393c87038033de2adf9865a9f7abcc/docs/workstreams/research/AF-RES-113/verification-tests.csv
[ret]: https://github.com/laadkke-arch/agentflow-open/blob/9351759623393c87038033de2adf9865a9f7abcc/docs/workstreams/research/AF-RES-113/returns.csv
[nat114]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/truth.csv
[expl]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/evidence/truth-exploratory.csv
[ctr]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/evidence/truth-controls.csv
[t3]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/evidence/table3.csv
[tr114]: https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/evidence/table2.csv
[cases115]: https://github.com/laadkke-arch/agentflow-open/blob/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115/cases.csv
[ver115]: https://github.com/laadkke-arch/agentflow-open/blob/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115/evidence/verification.json
[prov]: https://github.com/laadkke-arch/agentflow-open/blob/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115/evidence/provenance.json
[replay115]: https://github.com/laadkke-arch/agentflow-open/blob/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115/evidence/replays.json
[pairs]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/pairs.csv
[ans]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/answers.csv
[metrics]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/metrics.json
[reach]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/reachability/coverage-v1/coverage-summary.json
[trail]: https://github.com/laadkke-arch/agentflow-open/blob/31cc131279e606c9d691524525cbdbdf7dc7b44a/docs/workstreams/research/AF-RES-116/trails.jsonl
