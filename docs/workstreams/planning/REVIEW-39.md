# REVIEW-39 · 선례 링크를 받은 뒤 어디까지 달라졌는가

서명된 PDF를 그대로 보관하고 싶다는 요청에는 이제 조건을 붙여 원문을 권할 수 있다. Paperless-ngx v2.2.1의 특정 설정에서 텍스트가 충분한 시험 파일은 OCR 호출 없이 저장됐고 원본으로 되돌아왔다. 같은 설정에서 이미지로만 된 서명 파일은 입고에 실패했다. 반면 선례를 본 사람이 처음으로 설계를 바꿨는지, 부품을 채택한 팀의 총노동이 줄었는지는 이번에도 계산할 수 없었다. 이 구분이 전체 또는 선택한 소프트웨어 구조와 목적을 받아 완성품·기능·타 분야 원리의 링크를 건네려는 탐색기의 현재 출발점이다. [154 결과][r154] · [153 결과][r153] · [156 결과][r156] · [제품 브리프][product]

## 기준판과 신규 인계

먼저 `work/planning`의 최신 REVIEW-38(`c4963e0`)을 읽었다. 거기서 사용한 `f140af3`과 이번 통합 브랜치 `chore/workspace-foundation`의 `ff5a037`(2026-11-24 16:30:09 UTC 커밋)에서 진행표 전체를 ID로 비교했다. 기존 150행은 모든 필드가 같고 153~156 네 행이 DONE으로 추가됐다. **154행 중 DONE 148(연구 146·연결 시험 2), RUNNING 4, BLOCKED 2**다. DONE 148행의 중앙 `acceptance_evidence`는 모두 빈 배열이다. 아래 상태는 각 작업의 실제 인계 판정이다. [직전 검토][r38] · [직전 진행표][c38] · [이번 진행표][c39]

| 신규 작업 | 중앙에 등록된 인계판 | 작업자가 검사하거나 마감한 결과판 | 이번에 재집계한 원전 행 / 산입 고유 단위 |
| --- | --- | --- | --- |
| 153 · 사람의 선례 노출 | [12eb394 · PARTIAL][h153] | [f92048a · 원자료 연결 미완][r153] | 34행 / 20저작. 특허 원면 6건은 제3자 호스팅이라 발행자 호스트 기준에서는 14저작이다. [출처][s153] |
| 154 · 서명 문서 입고 | [0b24a98 · 작업자 COMPLETE, REVIEW_READY][h154] | [b19c8f9 · 새 체크아웃 재생][r154] | 40행 / 31저작. 실행 영수증은 결과판 검사 뒤에 추가했다. [출처][s154] · [검사 영수증][v154] |
| 155 · 선택 구간의 실제 변환 | [9a62426 · PARTIAL][h155] | [1c1e68c · 새 체크아웃 재생][r155] | 47행 / 외부 자산 28개. 같은 음악 출판 계보를 묶으면 26개다. [출처][s155] |
| 156 · 시간대 부품을 바꾼 소비자 | [39a138c · PARTIAL][h156] | [ef71cee · 원격 원장 검산][r156] | 77행 / 29저작. 프로그램 실행·CI 통과를 확인한 원장은 없다. [출처][s156] |

네 작업 모두 등록된 `result_commit`과 해당 작업 브랜치의 조회 당시 끝 커밋이 일치했다. 새 DONE의 HANDOFF·RESULT와 아래에 연결한 원장에서 사례·분모·결측과 수정 이력을 대조했다. 실행 결과는 작업자가 보관한 당시 출력과 영수증에 근거한다. 과거 작업의 수치는 직전 REVIEW의 누적 판단을 이어받았다. 진행 중인 149~152는 자료 유입 경로·언어권, 여러 주소와 기능의 동일성 정정, 목록 편입·유보·재심사, 발굴·재점검 예산을 각각 맡고 있다. 018의 동일 예산 웹 검색 비교와 035의 호출 경계 값·타입 보존은 차단 상태다. [진행표][c39] · [운영 규칙][workflow]

## 1~38차에서 이어지는 설계 판단

| 탐색기가 답할 질문 | 누적 근거와 적용 범위 | 남은 결정 |
| --- | --- | --- |
| 모르던 원리를 찾아 선택을 바꿨는가 | 002는 발견 경로와 실제 기여 부분을 남겼다. 010의 분야 단서로 원리 7군을 찾았지만, 단서 없는 033의 144쌍에서는 당시판 지지가 0이었다. 022의 ‘미인지→결정 변경→시행’은 0/24였고 141의 Matplotlib 작성자는 링크 전부터 외부 타입 스텁을 알았다. 145의 초안 8쌍에서 한 작성자는 새 시험·조건을 6건으로 분류했으나 독립 초안 0/16, 유효한 두 검색 조건 짝 0/8, 대상 시험 실행 0이었다. | 링크가 알려 준 조건, 처음 알게 된 사실, 당시 작성한 수정, 배포된 동작을 각각 입증해야 한다. |
| 선택한 부분에 무슨 문맥을 붙여야 하는가 | 020은 주장 72/73을 전달했어도 모든 충돌 해결은 2/16이었다. 119의 도표 6건은 요구만으로 정확 0, 이웃 또는 직접 참조를 준 보기에서는 각각 3이었다. 103은 외관 10/10을 지켜도 텍스트 선택을 잃었고, 107의 단일 발생 편집은 공유 정의 0/6·위치 지정 6/6이었다. 144는 잘못된 날짜 하나 때문에 성공 종료 뒤에도 열이 Text였다. 148은 같은 입력의 기대 출력 3건을 찾았으나 가림 판독 0/18, 유효 비교 0/6이었다. | 보존할 값과 다음 소비자가 답을 가르는지부터 본다. 전체 프로젝트 제출이나 고정 Studio 입력 계약을 요구할 근거는 부족하다. |
| 더 찾거나 더 읽으면 무엇이 표시되는가 | 040의 8요구는 묶는 법에 따라 부분 근거를 8개 또는 6개 보존했고 완전 적격은 0/8이었다. 044의 관측 8풀에서는 두 묶기 방식이 같았다. 118은 충돌과 일부 지지를 함께 숨겼고 142의 잠정 신규층 표시 72자리는 비었다. 146의 새 요청 4×12후보는 직접 0·일부 15·충돌 14·미확인 19였다. 검토 폭 3→8에서 조건부 표시 1→4였지만 새 링크 셋은 모두 한 요청의 5·7·8위였다. | 목록 밖·낮은 순위·근거 부족·표시 보류를 나눈다. 여러 단계의 링크를 한 요구에 대한 완결된 답으로 엮을 때는 단계 사이의 전제를 확인한다. |
| 가벼운 저장으로 과거 답과 현재 적합성을 복원하는가 | 003에는 짧은 메모로 충분한 경우와 정정이 필요한 경우가 있었다. 023은 18사건 중 허용 병합 5, 정정·분리·되돌림 9(문자 그대로의 오병합 수정 3), 기타 4였다. 055는 과거 판단 4/4·다음 판 0/4, 071은 절·설정으로 과거 22/22를 복원했다. 075에서는 전체 후보가 없어 단독·공동 1위 주장을 각각 16/16 보류했다. 147의 당시 증빙을 보관한 안은 과거 질의 112/112에 답했고 나머지 두 안은 각각 112건 보류했다. | 북마크, 과거 답의 감사, 새 요청 판정, 후보 간 우선순위에는 서로 다른 정보가 든다. 연구 원장의 열은 제품 DB 설계의 확정안이 아니다. |
| 언제 다시 읽고 얼마를 쓰는가 | 019의 동일 신호는 엄격 7쌍 중 사건 3·대조 3건에 울렸다. 024의 분기당 20회에서 정기 확인은 11/11·신호 확인은 8/11의 무효화를 찾았다. 후자가 원문을 108개 덜 읽었으나 본문 수신량은 5,672,462바이트 더 컸다. 135는 같은 README 아래 기본 출력이 바뀌었고, 143은 5,696셀쌍의 수치 변화 양성 없이도 공개 진입의 실패·회복을 관측했다. 147은 인접 24쌍 중 효력값 변화 4를 보았다. 정확판 조회는 현재 요청 96건 전부 맞았지만 주소의 마지막 답만 쓴 대조는 오승인 40·오거절 32·정답 24였다. | 요청판·자료판·실제 변경과 전송·대기·검사 비용을 함께 비교한다. 운영 규모에 맞는 주기와 예산은 열려 있다. |
| 근거를 주면 사람의 작업량이 줄어드는가 | 021의 두 절 열람 예산에서는 근거 충분이 주소만 6/23·맞춘 절 14/23이었다. 034에서 일부 단계 시간은 380→57초, 전체는 849→847초였다. 140의 두 번째 절 7개가 새로 해결한 핵심 조건은 0이었다. | 링크 탐색, 읽기, 실제 구현·호환·검토·운영의 시간 단위를 따로 보존한다. 앞 단계를 줄인 관측으로 전체 순절감을 산출할 수 없다. |

앞선 수치 정정도 유지한다. 114가 충돌로 분류한 138/144쌍을 118의 명시 반박 기준으로 다시 보면 충돌 7·미확인 131이고 나머지 6은 일부 지지다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 고유 면은 본문 해시 기준 9개이며, 열람 10회와 답–면 연결 16쌍은 별도 분모다. [누적 수치와 근거 위치][r38]

## 새 DONE 네 건의 증거와 결손

**153 · 개인의 설계 변화.** 노출 원장 12행, 전후 후보 11행, 대조 19행을 확인했다. 전후 후보의 `strict_pair`는 11행 모두 0이다. Sketchy의 P2가 동료 그림의 눌린 버튼 모양을 차용했다는 저자 서술은 있다. 첫 작품과 실제 동작 변경은 연결되지 않았다. B09는 중간안과 배정 자극이 있지만 최종 작품이 없고, X11에서 스케치를 실제로 구현한 주체는 연구자다. B06에서는 먼 예시 집단의 독창성·품질 평정이 높았고 B09에서는 먼 예시의 유용성이 낮아졌다. 서로 다른 과제와 평정 축이라 하나의 ‘먼 예시 효과’로 합칠 수 없다. [전후 후보][pairs153] · [노출][ex153] · [대조][ct153]

얕게 남은 지점은 문헌의 수보다 원파일 판독이다. 네 검색의 표시 38행에서 정규층 고유 후보는 A4·B7로, 층별 첫 15개와 확장 30개의 모집을 채우지 못했다. 15,062,721바이트 Sketchy CSV는 존재를 확인했으나 본문을 못 읽었고 Cambridge ZIP과 OSF의 작품·이벤트도 연결하지 못했다. B04의 본문 과제 번호 4·7·12·13과 표의 4·7·11·12도 해소되지 않았다. **유효쌍 0은 개인이 설계를 바꾸지 않았다는 관측이 아니다.** [모집 원장][fr153] · [자료·접근 한계][s153] · [판정][r153]

**154 · 제출부터 회수까지.** 합성 한 페이지 PDF 네 종류 × 두 설정 × 새 상태 두 반복으로 본 실험 16건, 보조 실행 7건을 구분했다. 입고 성공 10건 중 명시 원본은 10건, 기본 응답은 6건에서 입력 바이트와 같았다. 기본 설정에서 서명 텍스트·이미지는 모두 실패(0/4 성공)했다. 아카이브 생략 설정 `always`에서는 서명 텍스트 2/2가 래퍼·문자인식 각 0으로 성공했고, 서명 이미지 2/2는 래퍼가 각각 두 번 호출된 뒤 문자인식 전에 실패했다. 별도 파생 허용 실험에서는 서명 이미지를 입고해 명시 원본을 회수했지만 실제 OCR이 있었고 기본 반환본의 서명은 0개였다. 최초 무 OCR 요구와 저자의 후속 완화는 별개다. [실행 원장][run154] · [성공 입력의 실제 영수증][st154] · [판정][r154]

쓰기 실패→명시 재입고→중복 거절 때 문서 수는 각 반복에서 3→3, 3→4, 4→4였다. 소비 폴더의 실패 사본도 남았다. 이는 운영자 로그·대기 사본·성공 후 원본 회수를 지지한다. 원저자의 실제 업로드 파일, 제출자가 미저장 사실을 어디서 인지했는지, 다중 호스트나 모든 복구 경로는 이 실험 밖이다. 원저자가 요구한 선명한 실패 로그와 별도 외부 알림 수신은 다른 요구다. 통제 인증서에서 확인한 서명 무결성도 실제 수신자의 신뢰 판정까지 보장하지 않는다. [복구 원장][wr154] · [결과·남은 범위][r154]

**155 · 같은 조각을 넘긴 다음 단계.** 20경로 두 번의 원장 40행은 실제 실행 38, 동일 함수가 없어 실행 전 보류한 E4 2행이다. 하위 명령 132회가 모두 종료 0이었다. 그런데 Pandoc 3.1.11의 #9305는 AST에 둘째 셀 문자열을 두고도 plain 출력에서 그 값을 잃었다. #9308은 CommonMark reader와 중괄호 속성 경로의 plain이 같아도 `hl_lines`의 AST 보존이 달랐다. X05에서 기본 Mustache escape는 사전 예측과 달리 블록 경계를 지켰고 원시 백틱 문자는 잃었다. 비이스케이프 대입을 별도로 구성했을 때에만 포맷 우선 경로에서 중첩 블록이 갈라졌다. 검사할 보존값을 먼저 정할 이유가 생겼다. [실행 원장][run155] · [사전 예측][pred155] · [결과][r155]

이 결과로 실제 사용자에게 반드시 어떤 필드를 요구해야 하는지는 정해지지 않았다. 자연 짝은 0/4였다. 같은 A에서 갈린 구성 대조 3행과 음성 2행은 한 X05 사건을 여러 각도에서 본 것이다. E2·E3의 B는 A가 이미 준 27자·23자를 반복했고, 유일한 동량 B/C의 E4는 입력 함수와 기대 함수부터 달랐다. X05 원작성자의 실제 엔진·설정·소비자 조합은 미확인이다. 역사 문헌은 인쇄 원면 0/2, 악보는 원 배포 PDF 없이 공개 소스를 재각보했다. 사람의 이해와 질문 절감은 측정하지 않았다. [자연·구성 대조 원장][dist155] · [출처 판독][s155]

**156 · 부품 채택 뒤 옮겨 간 노동.** 확인 가능한 것은 변경의 종류와 부담 주체다. Django는 선택 지원→기본 전환→호환 종료를 거쳤고 D6 핵심 코드 +6/−66줄은 5.0 배포의 어댑터 정리다. 하류 자동 수정기는 잘못된 import를 만들어 후속 보정이 필요했다. pandas의 key 기반 최적화 뒤 파일이 제공한 시간대 규칙과 이름이 다를 때 13시간 어긋난 사례는 **저자 보고**이며 후속 fallback 변경은 실제 패치다. 119와 11.3ms도 보고자의 실행시간이다. 기존 구현은 이미 pytz를 쓰고 있었다. 두 프로젝트가 처음부터 새 시간대 엔진을 만들려다 그만뒀다는 근거는 없다. [변경 원장][chg156] · [하류 사건][ds156] · [결과][r156]

시간 원장 12행의 `human_time`은 11행이 missing, 나머지 한 행도 unknown이다. 같은 납품물·기간에서 양쪽 노동을 측정한 쌍은 0이다. Django 첫 여섯 직접 커밋 중 D6 배포는 4.0~4.2 창 밖이었고 pandas는 직접 사건군 5개 중 병합 확인 4개였다. 기본 전환 후 두 번째 기능판은 기준일에 미관측이다. 수정 원장에 따라 P4 후속은 **P5/P8**로 읽어야 한다. P7의 직렬화 사건을 해당 최적화 탓으로 돌릴 수 없다. 교통 시간표의 24시 이후 표기는 예정 시각이며, 방송 기록의 제작일·방송일은 서로 다른 값이다. 실제 운행 시각이나 offset 없는 역사적 시분초를 이들로 대체할 수 없다. [시간 원장][cost156] · [범위·귀속 보정][corr156]

## 다음 작업과 판정을 바꿀 관측

| 독립 작업·담당 | 출발 근거 | 다음 작업자가 넘길 수 있는 판단 |
| --- | --- | --- |
| 157 · codex-cloud | 153 | 지정된 공개 연구 보관소의 원파일에서 익명 사건을 재구성한다. 동일인·과제·직전 작품·실제 개봉·직후 작품이 이어진 쌍과 첫 결측 위치를 제시한다. |
| 158 · web-pro | 154 | Paperless와 Dataverse의 공개 사용자 사건에서 접수번호, 최종 저장, 제출자에게 보인 실패, 명시 재시도를 구별한다. 어떤 단계까지 한 링크나 보충 근거로 안내할 수 있는지 문장으로 남긴다. |
| 159 · codex-cloud | 155 | 두 편집기의 같은 배포판에서 동일 UI 문구가 쓰인 실제 호출들을 찾아, 원문 위치·역할 한 필드가 기능 링크를 가르는 경우와 같은 번역에도 역할이 다른 반례를 재생한다. |
| 160 · web-pro | 156 | 공개 소프트웨어 작업시간 원장과 프로젝트 원보고서를 먼저 모집한다. 한쪽에서 확인한 단계 소계, 같은 납품물을 위한 양쪽의 비교, 미측정인 후속 노동을 구분해 비용 문장을 작성한다. |

각 과제는 한 개의 고정 DONE 인계만 필요하다. 157의 비식별 연구 사건, 158의 제출자 사건, 159의 고정 편집기 호출부, 160의 노동 원장은 서로 자료를 기다리지 않는다. [배정용 JSON](NEXT_TASKS-39.json)

| 중요한 불일치·약점 | 현재 판단이 갈리는 이유 | 다음 조사에서 결론을 바꿀 관측 |
| --- | --- | --- |
| 선례의 차용 사례와 개인의 새로운 결정 사이에 빈칸이 있다. | 배정, 실제 개봉, 같은 작품의 변경, 다른 사람이 구현한 결과가 섞이면 차용률도 인과효과도 정할 수 없다. | **157**에서 같은 익명 ID의 실제 시간순 쌍과 무노출·무변경 대조가 나오면 해당 연구·작품에서만 변경 판정을 갱신한다. |
| 기술적으로 이어지는 단계가 요청자의 최종 결과까지 보장하지 않는다. | 154는 성공한 문서에서야 원본을 회수했고 155는 같은 표시 문자 아래 소비자에 따라 다른 동작을 관측했다. 저장·사용자 인지와 글자·실제 기능은 각각 다른 종점이다. | **158**은 같은 제출의 접수와 종료·복구 증빙을, **159**는 같은 원문 선택의 두 실제 바인딩과 한 필드의 구별력을 확인한다. 한 절이나 원문 위치만으로 충분했던 경우도 남긴다. |
| 어댑터 일부가 줄어도 팀 전체 노동이 줄었는지 알 수 없다. | 삭제한 줄·밀리초·릴리스 경과일과 개발자·운영자의 인시는 단위와 관측 기간이 다르다. | **160**에서 기능·품질·기간이 같은 대안의 실제 투입과 채택 후 후속 노동이 함께 확인될 때만 그 범위의 차이를 계산한다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8/docs/RESEARCH_WORKFLOW.md
[r38]: https://github.com/laadkke-arch/agentflow-open/blob/c4963e069bee8394335460d4039f71b9443a76f5/docs/workstreams/planning/REVIEW-38.md
[c38]: https://github.com/laadkke-arch/agentflow-open/blob/f140af3179b7d9271710778104ccee5b4812e2ef/docs/automation/dot-control.json
[c39]: https://github.com/laadkke-arch/agentflow-open/blob/ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8/docs/automation/dot-control.json
[h153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/HANDOFF.md
[r153]: https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/RESULT.md
[s153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/sources.jsonl
[h154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/HANDOFF.md
[r154]: https://github.com/laadkke-arch/agentflow-open/blob/b19c8f966e3f5ae95c0f8714ebcd09122dabdc35/docs/workstreams/research/AF-RES-154/RESULT.md
[s154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/sources.jsonl
[h155]: https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/HANDOFF.md
[r155]: https://github.com/laadkke-arch/agentflow-open/blob/1c1e68c33507139561abe5160f6f29600ecb81ca/docs/workstreams/research/AF-RES-155/RESULT.md
[s155]: https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/sources.jsonl
[h156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/HANDOFF.md
[r156]: https://github.com/laadkke-arch/agentflow-open/blob/ef71cee3114731142a50b06eb63efb9d250b5934/docs/workstreams/research/AF-RES-156/RESULT.md
[s156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/sources.jsonl
[pairs153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/pairs.csv
[ex153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/exposures.csv
[fr153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/frame.csv
[ct153]: https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/contrasts.csv
[run154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/runs.jsonl
[v154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/evidence/verification/summary.json
[wr154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/evidence/runtime/R1-A/write-retry.json
[st154]: https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/evidence/runtime/R1-A/R1-A-ST/receipt.json
[run155]: https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/runs.jsonl
[dist155]: https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/distinctions.csv
[pred155]: https://github.com/laadkke-arch/agentflow-open/blob/9a62426f9a989c3c0fff513f66a63d68484cbe3c/docs/workstreams/research/AF-RES-155/predictions.csv
[chg156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/changes.csv
[cost156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/effort.csv
[ds156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/downstream.csv
[corr156]: https://github.com/laadkke-arch/agentflow-open/blob/39a138ca2b02e2c4f790efe197f6d33d41237878/docs/workstreams/research/AF-RES-156/SCOPE_CORRECTION.md
