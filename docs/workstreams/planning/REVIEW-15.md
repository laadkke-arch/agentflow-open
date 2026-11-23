# REVIEW 15 · 추천 링크로 확인한 것과 아직 검증할 수 없는 것

설계자가 지금 받을 수 있는 답은 “이 부품의 이 판에서, 당신의 어느 조건을 어디까지 확인했다”는 것이다. 새로 검토한 네 작업에서 단어 강조를 제공한 조건에서 전체 정답률과 오답 권고 수락률이 함께 높았던 사례를 찾았다. 시간대 패키지 두 판에서는 같은 UTC 순간이 다른 현지 날짜로 표시되는 범위까지 좁혔다. 타 분야 원전이 더 좋은 구현 선택을 만들었는지, 근거 링크를 읽은 사람이 잘못된 부품을 걸러냈는지, 역사적으로 어느 사용자에게 해당 날짜가 표시됐는지는 아직 미확인이다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

## 검토 기준과 인수 범위

2026-11-23 UTC, `work/planning@70c7d71`의 최신 파일 REVIEW-14를 먼저 읽었다. 직전 검토의 통합판 `8036b86`과 이번 통합판 `aa1dc65`의 작업 ID·상태·결과 SHA를 대조했다. 등록은 **54→58**, DONE은 **52→56**, BLOCKED는 **2→2**다. 새 DONE은 **AF-RES-057~060**뿐이며 기존 작업의 결과 SHA 변경은 없었다. 056까지는 직전 검토의 근거를 인수했다. 018은 대화 길이 한도에서 세 번째 시도가 끝났고 035는 첫 시도 중 사이버 보안 위험 가능성 표시로 끝났다. 두 건 모두 중앙 결과 SHA가 없다. [직전 검토][prev] · [직전 진행표][oldreg] · [이번 진행표][reg]

| 새 DONE 작업 | 인계 SHA / 결과 본문 SHA | 작업자가 인계한 범위 |
| --- | --- | --- |
| 057 · 공동 편집 되돌리기 | [71d13fe][h57] / [5c5b529][r57] | 부분 인계. 66개 고유 외부 원저작, 6사례. 원래 판·입력·두 조작·다시 실행(redo)의 공개 출력이 모두 연결된 사례 0/6. [수용 원장][a57] |
| 058 · 설명과 권고 수락 | [fefeb21][h58] / [4265e44][r58] | 부분 인계. 심층 1차 저작 28개. 고정 8자리 중 6연구 선정, 선정층의 정오별 수락 원개수를 식별한 셀 0개. 별도 진단층 두 연구는 원행 결합 가능. [수용 원장][a58] |
| 059 · 패키지와 소비 환경 | [e91b8ab][h59] / [5c975cf][r59] | 부분 인계. 외부 32계보. 레지스트리 해시가 맞는 배포 파일 14/14, 과거 프로세스 출력과 연결된 소비 프로젝트 0/2. [수용 원장][a59] |
| 060 · 검색 용어와 목록 기능 필드 | [87bd036][h60] / [ccde193][r60] | 부분 인계. 직접 읽은 원저작 113개. 48비교, 28개의 서로 다른 요구–후보 쌍, 엄격한 노출 예산을 확인한 경로 81/84. [갱신 수용 원장][a60] |

각 중앙 결과 SHA는 해당 작업 브랜치 끝과 일치했다. 마지막 커밋은 모두 자기 HANDOFF.md 한 파일을 바꿨고 본문 고정판과 인계판의 RESULT.md Git blob도 같았다. 중앙 DONE 56건의 `acceptance_evidence`는 모두 빈 배열이며 새 네 건의 `source_commit`과 `actual_model`은 null이다. 아래 수치는 작업자의 원장에서 예측 열, 정오별 응답, 배포 실행 행, 후보 순위와 창 예산을 다시 집계해 확인했다. 외부 원문 판독·프로그램 실행은 작업자의 기록, 사람의 수행은 원 연구의 자료를 근거로 삼았다. [예측][p57] · [응답][o58] · [실행][run59] · [순위][m60] · [열람 경로][paths60]

## 056까지 이어받는 결론

| 설계자가 풀 문제 | 확인된 사실 | 결정에 남는 제약 |
| --- | --- | --- |
| 전체 프로젝트 없이도 요청의 목적과 금지 조건을 전달할 수 있는가 | DOT-001·002는 세션을 바꿔 인계를 복원했다. RES-001~004의 합성 입력 6건에서 부정 조건이 빠졌고 2문제·17질의에서 동명 제품과 부분 기능이 섞였다. 020은 주장 72/73을 전달했다. | 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 020의 충돌 16건 중 완전 해소 2건. 026의 실제 추가 질문 발송은 0건, 030의 자연 질문 24건 중 같은 변수에 직접 답한 3건에서도 같은 답변자의 권고 변경과 요청자의 새 시행이 모두 연결된 경우는 0/3이었다. [REVIEW-14][prev] |
| 비슷한 이름 밖에서 부품과 원리를 찾을 수 있는가 | 009에서 비교한 35개 대상에는 기능 중복이 있었다. 010은 분야 단서와 24원문에서 원리 7군을, 011은 공개 61스레드·635답에서 부분 질문의 진전 10/33을 찾았다. | 타 분야 답 14개에는 요청자 반응이 없었다. 012의 합성 근접 오답 증가는 014의 실제 자료 485개에서 재현되지 않았다. 013의 역사 선례 회수는 웹 16/176·목록 5/176, 025의 72칸은 지지 2·충돌 14·보류 53·빈칸 3이었고 029의 세 탐색법은 각각 완결 0/12였다. 033은 분야 단서 없이 8요구×18후보를 비교해 엄격 지지를 넓게 보아 1/144, 당시판으로 0을 얻었다. [REVIEW-14][prev] |
| 원리를 미리 보았다면 결정을 바꾸거나 재작업을 줄였을까 | 022 결정 우선 표본 2/24에서 이미 알던 대안의 조건을 고쳐 시행했다. 037의 같은 목적 반영은 결정 우선 7/8, 노출 우선 3/4였다. 046 링크 우선층에서는 같은 작성자·목적 수정 2/4였다. 049는 Matplotlib 3.0.2의 좌표 선택에 따른 출력·예외 차이를 재생했다. | 미인지·당시 가용·결정 변경·시행까지 이은 022 사례는 결정 우선 0/24, 발견 진술 우선 1/9. 045에서 정상·경계 모두 판정 가능한 사례는 0건, 046의 보강층에서 첫 링크가 수정 이유라고 명시하고 시험까지 연결한 사례는 0/4. 049의 2.2.2에서는 두 조작이 동률이었다. 053의 동종 예제와 인쇄·지도 원전은 채운 5/6자리 모두 같은 예측이었고 원요구와 같은 조건의 새 공개 출력은 0/20논리셀이었다. [REVIEW-14][prev] |
| 어느 정도의 근거를 주면 사람이 일을 더 잘 끝내나 | 021의 두 번 열람에서 요구 완결은 주소만 6/23, 절 목록 9/23, 요구–절 대응 13/23, 잘못 대응시킨 보기 8/23이었다. 042는 pandas 출력 43/43과 근접 오답 5개를 확인했다. 054가 확인한 eXoaDocs 원문에서 40분 안에 같은 네 과제를 정확 완료한 사람은 예제 제공 3/12, 기존 문서 1/12였다. | 038의 사람 참가자는 0명. 034의 NCQ 패키지 선택 중앙값은 380→57초였으나 전체 과제는 849→847초였다. 050의 시간·최종품질 원행 새 결합은 전체 0/8. 054의 단일 과제 3은 3/12 대 4/12로 방향이 바뀌며, Blueprint 그림은 사람별 시간·품질의 결합 자료로 쓸 수 없었다. 동등 품질 총 노동시간과 재작업 절감은 미확인이다. [REVIEW-14][prev] |
| 주소가 살아 있어도 추천 이유를 다시 확인해야 하는가 | 015의 판정 가능한 현재 이유 195개 중 붕괴 14개, 과거 83개 중 뒤늦은 붕괴 5개·최초 오류 4개였다. 032에서는 12참조 모두 HTTP 200이어도 교체할 이유가 있었다. 055의 베이루트 2023b에서 4월 20일 21시 UTC의 현지 날짜가 바뀌고 23시 UTC 결과는 유지됐다. | 019 사건·대조 7쌍의 경보는 각 3건. 024의 분기 예산 10/20/40회에서 정기 대 신호 후 발견은 7 대 0, 11 대 8, 11 대 11(각 분모 11)이었다. 055 교통 운영판 판독은 0/8이고 시간대 두 판독기는 같은 컴파일 결과를 공유했다. 전체 자료의 공통 재확인 주기는 미결정이다. [REVIEW-14][prev] |
| 무엇을 저장하면 과거 답과 그 적용판을 복원하는가 | 023은 주소·이유로 목적지 복원 3/18, 판·근거 추가 5/18, 변경 관계·시점 추가 15/18을 보였다. 039는 옛 발췌를 12/12 재표시했다. 051 통제에서 경로·필드·변환은 64/64 판정과 일치했다. 055 냉 조회의 네 과거 답은 주소·이유 0/4, 옛 판·해시 2/4, 사용 행까지 4/4였다. | 027·032의 상류 시행일→소비 배포일은 0/12·0/6, 043의 자연 소비자 사용판 0/4, 047의 소비 우선층 외부 입력 연결 0/6이었다. 051은 불완전한 목록을 완전하다고 표시하면 거짓 음성 3건이 났다. 055에서 같은 냉 조회로 다음 판 판정은 세 보기 모두 0/4였다. [REVIEW-14][prev] |
| 상위 몇 링크에 실제 대안과 필요한 절이 남는가 | 040의 URL·상류·부품별 표시는 필수조건 8·6·8개를 보존했다. 044의 보강 4건에서 완전 대안 수는 2·11·1·0. 052에서 상류를 묶자 5번 S3가 드러났으나 미러의 보완 관계였다. 056에서 두 목록 62행에 정의 기반 용어를 보태자 후보가 있는 요구가 0/8→1/8이었다. | 044의 두 클릭 13/14는 여러 경로의 합이고 048의 판 확보는 2/9풀이었다. 052 자연층의 사용자 목적과 게시 목록 연결은 0/4. 056의 두 번 열람 완결은 양쪽 0/8이고 유일한 후보의 예산 밖 C++ 시험은 없는 열 이름도 받아들였다. [REVIEW-14][prev] |

## 새 근거가 바꾼 판단과 얕게 남은 지점

**057 · 같은 undo 결과 뒤에도 서로 다른 다음 행동이 남는다.** 자연 요구 4건과 원시험 2건에서 API+동종 예제와 API+지도·회계 원전의 조작 선택, undo/redo, 정상·경계 예측을 자리별로 대조했다. 여덟 예측 열이 모두 같은 자리가 6/6이므로 **서로 다른 예측 중 타 분야 쪽이 맞은 비율의 분모는 0**이다. Yjs 13.6.28에서는 그룹을 끊고 undo하면 `[1,2,3]`, 끊지 않으면 `[]`였고 redo 뒤에는 양쪽 모두 여섯 원소였다. 13.0.8 보조 비교에서는 양쪽 undo가 빈 배열이었다. 원 API가 이미 설명하는 차이와 추가 원전의 기여를 따로 볼 이유다. [결과][r57] · [예측 열][p57] · [비교 분모][c57]

원시험 둘은 연구자가 원 실행기로 각 한 건씩 통과시켰다. 두 시험 모두 원래 한 조작의 결과만 선언했고 두 번째 조작과 redo는 연구자가 추가했다. 의미적 답을 미리 보지 않은 원시험은 1/2였다. 자연 사례의 당시 설치판·입력까지 포함한 완전 공개 쌍은 확보되지 않았다. 18 또는 22단어로 맞춘 창, 같은 모델의 창 밖 지식, 출력 후 보완 때문에 그런 원전을 읽은 다른 설계자가 같은 선택을 할지는 열려 있다. 원기록을 보존할지, 화면만 복원할지 묻는 데 지도·회계 사례를 쓸 수 있다는 것은 반환 제안이다. [관측 행][ob57] · [반환 카드][cards57]

**058 · 전체 정답과 오답 선별은 다른 방향으로 움직일 수 있다.** 별도 진단층의 리뷰 진위 과제 D04에서 기계 권고만 본 조건과 단어 강조가 더해진 조건은 각각 익명 사람 키 80개·1,600시행이다. 맞는 권고 수락은 908/1,395→1,107/1,395, 틀린 권고 수락은 123/205→152/205였다. 전체 최종 정답은 990/1,600→1,160/1,600(+10.625%p), 틀린 권고 거절은 82/205→53/205(−14.146%p)다. 반대로 Amazon 진단에서는 신뢰도 표시 대 단일 설명 추가의 오수락이 256/736→220/728로 낮아졌다. 이는 서로 다른 과제·조건의 기술 비교다. [응답][o58] · [조건 대비][co58] · [D04 검산][d58]

정작 고정 선정층에서는 8자리 중 소프트웨어·정보검색 2자리와 인접 분야 4자리를 채웠고 원개수 결합은 0셀이다. 같은 엔진이라는 서술로 같은 항목·같은 순위를 확인할 수 없었고 실제 외부 원문 열람을 배정한 비교도 없다. B03의 표는 정권고 8/14(57.1%)인데 두 그림의 정권고 수락·거절 몫은 합계 50%다. 분석 포함표·가중치 없이 일부 두 항목이 빠졌다고 역산할 수 없다. 어려운 미로에서 검증할 경로를 보여 준 효과도 소프트웨어 부품에 원문 링크를 다는 효과로 옮기기에는 자극과 과제가 다르다. [선정·진단 결과와 원자료 위치][r58] · [표본 원장][fr58]

**059 · 사용 가능한 배포판까지는 추적됐고 실제 사용자의 로드는 미확인이다.** PyPI 5판·npm 4판의 4입력을 앞뒤 순서로 읽은 기록이 72/72 일치했다. 정방향에서 베이루트 2023-04-20 21:00 UTC가 현지 당일 23:00이 된 배포는 `tzdata 2023.2`와 `moment-timezone 0.5.42` 둘뿐이다. 전후 배포는 다음 날 00:00, 같은 지역 23:00 UTC와 뉴욕 두 순간은 유지됐다. b판 게시부터 다음 정식판까지는 PyPI 약 4일 11시간, npm 약 7일 4시간이었다. 끝 두 판만 보면 중간 변경을 놓친다. [배포 원장][ed59] · [판별 입력·출력][run59] · [공개 기간][r59]

Grafana 9.4.7 Linux/amd64 공개 이미지에서 추출한 2022e 자료는 npm 0.5.38의 정규화 내용과 맞는다. pandas 2.0 wheel의 선언은 `tzdata>=2022.1`이다. 같은 b wheel을 설치하고도 호스트 파일 우선 조회는 +03, 패키지 fallback은 +02였다. 두 프로젝트의 과거 사용자 프로세스에서 어떤 자료를 읽었는지는 미확인이다. 별도 분야의 BLS 2024년 1월 공석은 두 발행 표에서 8,863→8,748천 건으로 정정됐지만 공석률은 5.3%로 같았다. 대응 ALFRED 빈티지 셀은 0/2 확인이다. 원본 실측과 보관처·소비자 판을 각각 표시해야 한다. [소비 기록][cn59] · [이미지][im59] · [통제][ct59] · [통계 원표와 결손][j59]

**060 · 검색 결과가 늘어난 위치와 증거가 끊긴 위치를 분리할 수 있다.** 원문 질의(L)·표준어 확장(V)과 게시 필드(F0)·공급자 기능 추가(F1)를 교차했다. L×F0, V×F0, L×F1, V×F1 순으로 후보가 있는 요구는 기존 8건에서 **0·1·3·4**, 새 4건에서 **0·1·0·2**였다. 144개 표시 자리에서 18개가 채워졌고 무매치 111개·풀 소진 15개였다. 전체 매치 43회는 고유 요구–후보 28쌍이다. 같은 경로에서 두 조건을 확인한 쌍은 0, 조건부 부분은 1, 미확인은 27이었다. V 질의를 고정하고 필드만 넓혔을 때 기존 후보 SC-032가 JS-4의 1위→11위로 밀리는 경우도 있었다. 밀린 후보의 정답 여부는 미확인이다. [순위][m60] · [슬롯][sl60] · [조합 집계][cs60]

유일한 부분 근거는 JS-6의 Ajv 예제에서 문자열 속성 `bar`를 `id`로 개명할 수 있다는 조건이다. 원문 글자 그대로만 인정하면 부분도 0이다. 원 Ajv판·Drupal 결합, 두 양성 입력·숫자 id 근접음성의 실행은 미확인이다. 같은 첫 창을 세 경로에서 본 것을 세 성공으로 세지 않았다. SC-036의 한 미리보기에서 500단어 대신 611단어를 보여 두 경로가 초과했고, 상속한 다른 JSON 한 창의 경계도 불명이다. 필드 편집에는 본문 요청 72회, 메타데이터 요청 최소 190회가 들었다. 여기서 정확도·사람의 읽기 시간·채택률을 구할 수 없다. [열람 경로][paths60] · [비용][cost60] · [미실행 시험 입력][fx60]

## 다음 네 작업이 바꿀 결정

| 독립 작업 / 작업자 | 앞선 공백과 이번 비교 | 결과에 따라 설계자가 돌려줄 것 |
| --- | --- | --- |
| AF-RES-061 · 타 분야 원리의 적용 경계 / web-pro | 053과 057에서 추가 예측이 갈리지 않았다. 물리 원리를 적용한다고 알려진 그래프 배치와 화면 애니메이션에서 명시 차용, 실제 구현, 원식이 깨지는 조건을 별도 증거로 찾는다. | 구현의 직접 근거, 개념 설명용 원전, 적용을 중단할 반례를 구분한 링크. |
| AF-RES-062 · 검증할 원문과 사람의 판단 / web-pro | 058의 강조·신뢰도 대비에는 실제 원문 열람 배정이 없었다. 정보검색·사실 확인 실험에서 같은 주장에 대한 원문 제공 배정과 자발 클릭을 나누고 정오별 선택을 복원한다. | 자료 제공·실제 노출·최종 선택 중 어느 단계까지 사람 효과를 말할 수 있는지 적은 설명. |
| AF-RES-063 · 과거 실행에 사용한 자료판 / web-pro | 059의 배포·이미지 조사에서 두 소비자의 당시 실행은 미확인이었다. 날짜 변환을 보고한 사람의 출력과 보관된 실행 로그에서 출발해 같은 실행의 입력·로드·판을 역추적한다. | 실제 사용판이 확인된 경우, 후보판만 좁혀진 경우, 사용자에게 다음 증거를 요청할 경우. |
| AF-RES-064 · 같은 후보에서 첫 링크의 위치 / codex-cloud | 060의 기능 필드는 후보를 늘렸으나 공동 조건 완결은 없었다. 12요구·V×F1 순위를 고정하고 첫 링크만 구현 절로 바꾼 보기와 기존 진입점을 같은 예산에서 재생한다. | 일반 진입점과 정확한 절 중 어느 것이 어떤 조건을 입증하는지, 실제 시험과 문서가 충돌하는 경우. |

061~064는 각각 완료된 057~060 한 건만 인수한다. 같은 차수의 결과가 들어와야 시작하는 작업은 없다. H1은 조건을 근거 절에 연결했을 때의 판단, H2는 판이 변한 뒤 옛 이유의 보존·재확인이다. 새 검색, 주소·판·목적 보관, 발췌·판정 이력 추가 중 어느 조합을 쓸지는 반환하려는 판단과 측정 비용에 달려 있다. [작업별 전체 지시문][next]

[product]: https://github.com/laadkke-arch/agentflow-open/blob/aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75/docs/RESEARCH_WORKFLOW.md
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/70c7d71c6d8858fc2c4e94c91ccaf0999d449700/docs/workstreams/planning/REVIEW-14.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/8036b862a0f921196dca57e8532df606bf6f1de6/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75/docs/automation/dot-control.json
[next]: NEXT_TASKS-15.json
[h57]: https://github.com/laadkke-arch/agentflow-open/blob/71d13fea95bae733939d36463a671f659a5651d2/docs/workstreams/research/AF-RES-057/HANDOFF.md
[r57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/RESULT.md
[a57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/evidence/acceptance-evidence.json
[h58]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md
[r58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/RESULT.md
[a58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/evidence/acceptance-evidence.json
[h59]: https://github.com/laadkke-arch/agentflow-open/blob/e91b8abe3eee98d469ae80d7ca152ff08047c8d9/docs/workstreams/research/AF-RES-059/HANDOFF.md
[r59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/RESULT.md
[a59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/evidence/acceptance-evidence.json
[h60]: https://github.com/laadkke-arch/agentflow-open/blob/87bd0362f7adce5a5e002036dc71a6fc93eeead1/docs/workstreams/research/AF-RES-060/HANDOFF.md
[r60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/RESULT.md
[a60]: https://github.com/laadkke-arch/agentflow-open/blob/4f4433960b581caad353322da298fa465258979e/docs/workstreams/research/AF-RES-060/evidence/acceptance-evidence.json
[p57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/predictions.csv
[c57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/evidence/comparison-counts.json
[ob57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/observations.csv
[cards57]: https://github.com/laadkke-arch/agentflow-open/blob/5c5b5299ec57eefde78029a23a62cfb48f508469/docs/workstreams/research/AF-RES-057/return-cards.md
[o58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/outcomes.csv
[co58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/contrasts.csv
[d58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/streams/root/independent-calculation.json
[fr58]: https://github.com/laadkke-arch/agentflow-open/blob/4265e446b0e1a22022d68a6f989ebc1d504f3e84/docs/workstreams/research/AF-RES-058/frame.csv
[ed59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/editions.csv
[run59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/runs.jsonl
[cn59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/consumer.csv
[im59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/evidence/grafana-image.json
[ct59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/evidence/controls.jsonl
[j59]: https://github.com/laadkke-arch/agentflow-open/blob/5c975cf275b90cf8d18a6425c6f00c210febacec/docs/workstreams/research/AF-RES-059/evidence/jolts.json
[m60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/matches.csv
[sl60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/slots.csv
[paths60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/paths.csv
[cs60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/evidence/comparison-summary.json
[cost60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/evidence/cost-audit.json
[fx60]: https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/evidence/next-checks/js6-fixtures.json
