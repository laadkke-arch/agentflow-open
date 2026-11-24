# REVIEW-28 · 설계자가 받은 링크로 다음 선택을 검증할 수 있는가

부분 설계를 받아 관련 링크를 찾는 제품에서, **후보를 찾았다는 사실만으로 그 링크가 설계 결정을 바꿨다고 말할 수는 없다.** 이번 검색은 공개 요청 6건에서 검증해 볼 선택안 12개와 시험 27개를 남겼다. 원 프로젝트에서 실행한 시험은 0개였다. 한편 고정 자료집에서는 메모가 빈 검색 결과를 채우면서 틀린 기능만 늘렸고, 링크를 받은 독자는 원문 일부를 정확히 읽고도 필수조건 전체를 확인하지 못했다. 다음 회차에서 가를 질문은 세 가지다. 필요한 자료가 애초에 있었는가, 조사자가 실제로 거기에 도달했는가, 읽은 내용이 이 사용자의 이 조작을 지지하는가. [선택안 원장][choices109] · [검색 정답표][truth110] · [수신 결과][pairs112]

## 이번에 인수한 범위

계획 브랜치에서 가장 최근인 [REVIEW-27][prev]을 먼저 읽었다. 그 검토의 중앙 진행표와 2026-11-24에 읽은 통합판을 ID·전체 필드로 대조했다. 기존 106행은 그대로였고 추가된 4행이 모두 DONE이었다. 전체는 **110행 중 DONE 108, BLOCKED 2**다. 연구만 세면 108건 중 DONE 106건, BLOCKED 2건(018·035)이며, 나머지 DONE 두 건은 AF-DOT 연결 시험이다. 중앙 DONE 108행의 `acceptance_evidence`는 모두 빈 배열이다. 새 네 행에서 `result_commit`이 가리킨 SHA는 각각 작업 브랜치 끝과 같았고, 해당 커밋의 변경은 `HANDOFF.md` 한 파일이었다. 네 결과 본문을 각 작업자가 검사한 SHA와 인계 SHA에서 각각 읽어 동일한 내용임을 대조했다. [이전 진행표][old] · [현재 진행표][reg] · [연구 운영 규칙][rules]

| 새 DONE | 등록 인계 SHA | 작업자가 검사한 결과 SHA | 이번에 인수한 판단과 그 경계 |
| --- | --- | --- | --- |
| AF-RES-109 · 일반 검색과 구조 검색 | [e547d88][h109] | [c212aab][r109] | PARTIAL. 12회 검색의 반환 자료와 조건부 선택안을 인수한다. 동일 비용·노출로 우열을 판정할 요청은 0/6이다. |
| AF-RES-110 · 메모와 판을 이용한 색인 | [281b661][h110] | [4e7c060][r110] | PARTIAL. 24기능×6요구의 사전 판정과 한·영 조회 재생을 인수한다. 직접 적격 1기능, 독립 판독자 0명이다. |
| AF-RES-111 · 요청 표현과 근거의 연결 | [c49eb34][h111] | [cf01f72][r111] | PARTIAL. 6사건·36표현·두 방식의 72판정과 실행 전 별도 문맥의 기준 판독이 있다. 자연 요청자가 직접 준 정규화 대상 ID는 0/6이다. |
| AF-RES-112 · URL에 한 줄 더한 인계 | [a44a0e4][h112] | [e3728f8][r112] | PARTIAL. Godot 3사건의 6수신 문맥이 18단계를 수행했다. LilyPond 3자리는 미모집이며 역사판 실행값을 채점할 수 있는 사건은 0건이다. |

새 작업의 HANDOFF·RESULT·자가 점검을 읽고, 109의 36후보 자리와 33판독행, 110의 정답 144행과 조사 순위 864자리, 111의 72판정과 검토한 근거 연결 192개, 112의 6쌍 예정표와 18개 실제 노출을 대조했다. 아래 실행값은 작업자가 보관한 관측이다. 이번 계획에서 재계산한 것은 원장의 분모와 집계이며 제품이나 독자 실험을 새로 실행하지 않았다. 이전 작업의 모집 조건과 결론은 직전 누적 REVIEW에서 인수했다. [109 비용][cost109] · [110 순위][ranks110] · [111 근거 연결][links111] · [112 실제 노출][trails112]

## 설계자가 이어받을 누적 결론

사용자가 제공하려는 것은 소프트웨어 전체 또는 선택한 부분, 이루려는 목적, 지켜야 할 조건이다. 도움이 되는 대상은 완성품·기능·부품·사이트·다른 분야의 원리까지 포함한다. 링크와 짧은 이유를 먼저 주고 상세는 원문에서 읽는 방식도 계속 비교할 수 있다. 작게 시작할 때 어떤 정보가 필요한지는 답하려는 질문에 따라 달라졌다. 제품의 DB·크롤러·AI 전처리·Studio 입력 계약은 미결정이다. [제품 연구 브리프][goal] · [이전 누적 검토][prev]

| 설계자가 내려야 할 판단 | 이전 회차에서 확인한 범위 | 109~112가 더한 근거와 남은 질문 |
| --- | --- | --- |
| 사용자의 원뜻과 선택한 부분을 어떻게 보존할까 | 020은 전달한 주장 72/73에도 충돌을 완전히 해소한 경우가 2/16이었다. 자연 요청의 되묻기 효과(070)는 판정할 분모가 없었다. 구성 입력(074)은 값을 받으면 8/8을 가를 수 있었다. | 111은 어순을 바꿔도 같은 근거가 붙을 수 있고, 대상이나 금지 조건을 바꾸어도 잘못 이어질 수 있음을 보였다. 작성자가 준 부분 구조가 있으면 이 오류가 줄어드는지는 새 입력에서 확인해야 한다. |
| 익숙한 도구와 낯선 원리 중 무엇을 찾았나 | 분야 단서가 있던 010은 원리 7군을 찾았다. 단서 없는 033의 144쌍에는 넓은 지지 1쌍·당시판 지지 0쌍이었다. 069·073은 접수와 적용 등을 가를 시험을 제시했다. 077의 보조 3건에서 핵심 구현 변경은 0건이었다. 101은 아는 제품을 빼면 유효한 다른 조작 세 개도 사라짐을 보였다. | 105의 “처음 알았다”는 두 발언은 좁은 기능에 한정됐고 그 제안을 실행했는지는 미확인이었다. 109의 검색 중 먼 분야 적격 발견은 0개다. 022의 미인지→변경→시행 0/24, 018의 차단 상태와 함께 보면 실제 개발자의 재작업 감소는 여전히 미확인이다. |
| 같은 URL·옛 인용이 현재도 같은 추천일까 | 055는 과거 판단 4/4를 복원했으나 다음 판 판단은 0/4였다. 071은 조각·설정 보관으로 과거 자료 소실 뒤 22/22를 복원했다. 075는 양성의 존재 15/15를 복원했지만 유일성·공동 1위를 증명하는 전체 집합은 각각 16/16 보류했다. | 111은 같은 과거 답·인용을 다시 읽고 철회 후 새 답과 재확인 항목을 남겼다. 한 연결의 실행 결과이며 동시 수정이나 후속 소비자가 재확인을 끝낸 결과는 미확인이다. |
| 어느 판의 어느 절을 반환할까 | 086의 역사적 제공 관측창은 0/9였다. 102의 경로 예측은 실제 8쌍 모두 맞았으나 음성이 없었다. 106은 같은 막대그림 주소에서도 옛 집단 점수를 보여 주는 목적은 사라지고, 묶음 막대의 일반 설명은 남은 사례와, 주소가 옮겨도 목적이 남은 두 사례를 찾았다. 16판의 당시 생성은 미확인이다. | 110에서 같은 버전 숫자라도 결과 코드의 호환 조건과 도구 자체를 실행할 조건이 달랐다. 112에서 현재판의 관측과 당시판 보고값도 갈렸다. 답이 적용되는 대상·판·구간을 함께 확인할 이유다. |
| 자료를 더 모으면 완결된 추천이 늘어날까 | 076의 자연 6요구×20후보에는 직접 양성이 없었다. 080의 목록 확장에서 자연 1/5·교정 3/5가 양성으로 바뀌었다. 078은 단독으로 성공한 두 부품이 연결될 때의 실패를 보였고, 096은 인접 자료를 6/6 노출해도 단독 완결은 0/6이었다. | 110의 6요구 중 5개는 고정 자료집에 직접 답이 없었다. 자료집 범위, 조사 후보, 화면 상위 3개를 따로 세야 어떤 변화가 필요할지 알 수 있다. |
| 한 줄 설명과 후속 열람 비용은 얼마인가 | 021의 두 절 예산에서는 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 연결한 절 8/23이었다. 034의 부분 시간 380→57초와 전체 시간 849→847초는 크게 달랐다. 104의 전용 완결 두 자리는 같은 진단 질문이었고 최종 JOIN을 요구하면 0/15였다. 108의 같은 1,200자에서 근거 충분은 키워드 4/16, 예외 우선 2/16이었다. | 112의 한 줄은 총 233자였고 세 쌍 모두 경로가 같았다. 위치를 바꿔 준 021, 문장을 바꿔 넣은 108, 이미 준 조건을 다시 강조한 112가 측정한 효과는 다르다. 자료 준비·본문 열람·최종 판단·사람의 총 작업시간을 따로 측정해야 한다. |
| 한 부분만 쓸 때 무엇이 함께 바뀌나 | 089는 화면 선택색과 다음 편집 대상을, 091은 같은 지점과 원래 행을 구분했다. 095에서는 옆 표의 선이 소실됐다. 103의 이미지 경로는 외관 10/10을 지켰으나 문장이 있는 8자리에서 텍스트 선택이 사라졌다. 107의 한 발생 편집은 공유 정의 0/6·위치 지정 6/6, 전체 편집은 각각 6/6이었다. | 109의 선 간격 예제는 같은 양 끝을 잇는 평행선과 여러 곳으로 갈라지는 선 중 어느 그림이었는지에 따라 추천이 갈린다. 글·조각·주변 참조 중 어느 것을 받으면 가를 수 있는지가 남는다. |

## 새 근거에서 실제로 갈린 판단

**109 · 두 방식이 같은 수의 아이디어를 내도 검색 성능은 비교할 수 없었다.** Node-RED와 xyflow의 2024년 공개 이슈를 저장소별 첫 80건씩 틀로 고정하고 첫 3건씩을 골랐다. 나머지 154건은 미선별이다. 실험 입력은 작성 시점 원본을 확인하지 못한 현재 글 6개이며 Studio 실사용 요청은 0개다. 일반 검색 A와 구조 검색 B가 각각 15회 질의했으나 명시 개봉은 23회와 29회였다. 원장에서 신규 플래그와 선택/시험 키를 같이 적용하면 방식별 8선택·16시험씩, 두 목록의 합집합은 12선택·27시험이다. 후속 정보에 노출된 R6을 빼면 9선택·22시험이다. 모델 세부판·자동 노출이 확인되지 않았고 후속 내용도 일부 노출돼 엄격한 쌍은 0/6이다. 사후에 읽은 기록보존·제조 자료 네 개를 검색 중 발견 수에 보탤 수 없다. [원 선택과 예상 출력][choices109] · [실제 소비량][cost109] · [사후 타 분야 원전][external109]

예를 들어 yFiles의 평행선 배치는 두 끝점이 같은 선의 간격에는 구체적인 안을 주지만, 원 첨부가 여러 목적지로 갈라지는 구조라면 답이 달라진다. 이 구조를 원 글에서 가르지 못했다. 별도로 같은 6사건에서 패치와 릴리스가 이어진 경우는 3건, 원 작성자의 복구 발언은 1건이었다. 2024년의 후속은 2026년에 만든 추천을 보고 한 행동일 수 없다. **인수할 것은 구별 시험과 조건부 대안이고, 실제 개발자의 채택과 절약 시간은 미확인이다.** [109 결과][r109] · [작성자와 후속 원장][after109]

**110 · 메모는 빈칸을 줄이면서 틀린 대상을 올렸다.** 여섯 공개 요구와 24기능의 144쌍에는 직접 1, 일부 6, 충돌 136, 미확인 1이 있었다. 여섯 영어 요청과 그 한국어 번역으로 조사 12·표시 3의 상한을 고정했다. 영어에서는 주소·제목, 영어 메모 추가, 같은 후보의 적용 조건 재정렬 모두 Paperless의 같은 기능과 두 판 페이지를 찾았다(1/1기능·2/2페이지). 한국어는 세 방식 모두 0/1기능·0/2페이지였다. 회차 하나의 한국어 18표시를 원장과 다시 맞추면 기준은 충돌 2·공석 16, 메모 및 재정렬은 충돌 5·공석 13이다. 일례로 영어의 ENVI 파일 머리글은 편집기 화면의 머리글 요구에서 2위로 올라왔다. [기능별 판정][truth110] · [표시 순위][ranks110]

색인 준비 비용도 달랐다. 같은 SQLite 설정에서 메모를 넣자 DB가 180,224→299,008바이트가 됐다. 보조 판 교체에서는 같은 Python 3.12 조건이 문장 끝 마침표 하나로 재정렬 11위에서 1위에 남는 차이가 났다. 이 보조 결과와 자연 요청을 구분해야 한다. 6요구의 최초 제출판은 모두 미확인이고 판독자는 1명이었다. 한국어 메모·공식 번역어를 색인한 비교도 없었다. “한국어 번역이 쓸모없다”거나 “영어 메모가 모든 분야에서 해롭다”는 결론은 이 실험 범위를 벗어난다. [110 결과][r110] · [교체 입력의 실제 결과][replace110]

**111 · 같은 근거를 유지하는 능력과 옳은 근거를 유지하는 능력이 갈렸다.** rsync와 Inkscape 6사건에서 원문 6개와 작성 변형 30개를 비교했다. 별도 세션에서 실행 전 기준 판정을 고정했다. 어순 교환에서 기준 방식 A와 역할 추정 방식 B 모두 자기 원문과 같은 후보·근거를 6/6 유지했으나, 조건과 근거가 기준 판독과 완전히 일치한 요청은 A 5/6, B 4/6이었다. 동의어로 바꾸면 완전 정합은 각각 0/6이었다. 극성·범위·누락 18변형에서 잘못된 근거 승계는 A 7건·B 5건, 지지하지 않는 근거를 지지로 붙인 요청은 A 2건·B 4건이었다. 한 지표만 보면 B에 대한 판단이 뒤집힌다. F1에서 B가 동작의 시점을 꾸미는 표현을 잘못 묶었고, D3에서는 양쪽 모두 생략된 대상을 옛 근거에 잘못 연결했다. [근거 사용 75개를 포함한 전체 연결][links111] · [변형별 판정·분모][verify111]

72회 판정과 10개 이력 상황의 재생은 해당 고정판에서 확인했다. 자연 작성자가 구조상의 대상 ID를 제공한 사건은 없었고, 모집된 사례도 파일 전송은 모두 rsync, 도면은 모두 Inkscape였다. ExifTool 원포럼의 생성 순서, FreeCAD 이관 전 시각, 한 도면의 원 첨부는 미확인이다. UI에서 사용자가 선택한 부분을 받는 실제 연동에 이 결과를 일반화할 근거는 아직 없다. [111 결과][r111] · [이력 원장][life111]

**112 · 한 줄을 받은 독자도 세 사건 모두에서 같은 경로를 골랐다.** 주 표본은 Godot의 고유 40사건에서 뽑은 첫 적격 3건이다. LilyPond의 공식 월별 모집틀을 확보하지 못해 나머지 세 쌍은 비교불가였다. Godot의 AI 수신 6문맥은 매번 최대 세 번 자료를 열었다. A와 B 각각 9개봉·7,249자였고 세 쌍 모두 노출 순서·최종 등급이 같았다. 근거가 충분한 최종 답 0/6, 정당한 보류 2, 미확인을 남긴 조건부 답 4였다. 최종 등급이 기준과 일치한 4/6이나 정확한 일부 복원 10/18단계를 완전한 성공으로 올리면 안 된다. G2의 두 독자는 ZIP 목록과 캐시까지 읽고 정작 입력값을 가진 원파일을 열지 못했다. [쌍과 공석][pairs112] · [실제 개봉 위치][trails112] · [지원 범위·비용][metrics112]

G2의 같은 값 대조는 현행 실행에서 4였고 원 첨부는 8을 출력하며 assertion이 실패했다. 원 이슈의 역사판 보고값 4를 현행판으로 재현했다고 볼 수 없다. 원문 고유 1차 저작을 73개 셌어도 지정 배당은 21/24였다. 공통 요청에 이미 보존 조건이 들어 있었고, 세 번 안에 두 조건까지 갈 수 있는 경로를 입증하지 못했다. 따라서 결과가 같은 이유를 한 줄의 유무로 단정하기 어렵다. 관측된 것은 선택한 경로의 일치이며 실험 참가자는 AI였다. [112 결과][r112] · [자기 점검과 시각 정정][self112]

## 다음 네 작업과 결정 기준

| 배정 | 완료된 선행 | 새로 가를 판단 | 성공 여부와 무관하게 넘겨야 할 것 |
| --- | --- | --- | --- |
| 113 · web-pro | 109 | 가까운 구현 하나에서 예제와 명시한 출전 중 어느 링크를 한 번 더 열어야 다른 설계 선택을 얻나 | 공개 부분 요청 6자리의 같은 시작 절, 양쪽 실제 도착, 새 선택을 구별하는 입력과 원전의 반례. 출전이 없거나 시작 절만으로 충분한 경우도 남긴다. |
| 114 · codex-cloud | 110 | 한국어 직접 답을 놓친 원인이 자료집 결원, 대역어 누락, 다른 대상의 동명 중 어디인가 | 새 24기능에서 공식 한·영 대역어와 역할 재정렬을 각각 켜고 끈 네 방식의 순위·비용. 자연 요청과 직접 적격이 있는 대조를 따로 재생한다. |
| 115 · codex-cloud | 111 | 실제 첨부의 시작 객체와 한 단계 참조가 있으면 다른 부분에 근거를 잘못 잇는 일을 줄이나 | 도면·악보의 요청문, 직렬화 이웃, 참조 이웃을 같은 후보 절에 대조한 선택·영향 집합. 파일 전체로도 의도가 정해지지 않는 경우를 보존한다. |
| 116 · web-pro | 112 | 같은 URL에서 반복 설명과 새로운 위치 단서가 실제 열람과 답을 달리하는가 | 문서 변환·이미지 처리 6자리에서 세 번 안의 도달 증거, 세 보기의 실제 경로·답·반례·준비 비용. 도달 불능과 읽었지만 틀린 판단을 구분한다. |

113은 이미 발견한 가까운 구현에서 **무엇을 더 발견하는가**, 114는 고정 목록에서 **무엇을 보여 주는가**, 115는 받은 부분이 **어느 객체를 가리키는가**, 116은 같은 URL을 받은 뒤 **무엇을 확인했는가**를 맡는다. 각각 완료된 선행 하나와 별도 공개 입력으로 시작한다. 새 작업들 사이에 먼저 끝나야 할 작업은 없다. [배정용 JSON][next]

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/a385051ad6db7bce9df9c2b98409162293b71ed5/docs/workstreams/planning/REVIEW-27.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/c40ef7723d851b628233bfb60dff8dfd292385cf/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/670ecde1dab07aede6760618a7d907f0cdff185a/docs/automation/dot-control.json
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/670ecde1dab07aede6760618a7d907f0cdff185a/docs/RESEARCH_WORKFLOW.md
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/670ecde1dab07aede6760618a7d907f0cdff185a/docs/product/RESEARCH_BRIEF.md
[next]: NEXT_TASKS-28.json
[h109]: https://github.com/laadkke-arch/agentflow-open/blob/e547d88834ff8adfcea9039e32c48b5be97e1eb3/docs/workstreams/research/AF-RES-109/HANDOFF.md
[r109]: https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/RESULT.md
[h110]: https://github.com/laadkke-arch/agentflow-open/blob/281b661f9b17e07483f20834859fa157b4846c75/docs/workstreams/research/AF-RES-110/HANDOFF.md
[r110]: https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/RESULT.md
[h111]: https://github.com/laadkke-arch/agentflow-open/blob/c49eb343ca0f74006cd3f748a1ec48b67615cedf/docs/workstreams/research/AF-RES-111/HANDOFF.md
[r111]: https://github.com/laadkke-arch/agentflow-open/blob/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111/RESULT.md
[h112]: https://github.com/laadkke-arch/agentflow-open/blob/a44a0e4bd8fe4bca6945a2ff40fba7c745e877b8/docs/workstreams/research/AF-RES-112/HANDOFF.md
[r112]: https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/RESULT.md
[choices109]: https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/choices.csv
[cost109]: https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/costs.csv
[external109]: https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/external-transfer.csv
[after109]: https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/aftermath.csv
[truth110]: https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/truth.csv
[ranks110]: https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/ranks.csv
[replace110]: https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/evidence/replacement.json
[links111]: https://github.com/laadkke-arch/agentflow-open/blob/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111/links.csv
[verify111]: https://github.com/laadkke-arch/agentflow-open/blob/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111/evidence/verification.json
[life111]: https://github.com/laadkke-arch/agentflow-open/blob/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111/lifecycle.csv
[pairs112]: https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/pairs.csv
[trails112]: https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/trails.jsonl
[metrics112]: https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/metrics.json
[self112]: https://github.com/laadkke-arch/agentflow-open/blob/e3728f89f3f93d6a10fdcc62bbcd80ad8fda1ac2/docs/workstreams/research/AF-RES-112/SELF_CHECK.md
