# REVIEW 14 · 설계자가 링크를 근거로 어디까지 판단할 수 있는가

설계 중인 소프트웨어의 전체나 일부와 목적을 받아, 바로 쓸 제품·부품과 다른 분야에서 빌릴 원리를 찾아 주는 것이 목표다. 지금 가장 구체적으로 돌려줄 수 있는 결과는 **사용자의 어느 조건을 어느 판의 어느 절·시험에서 확인할 수 있는지**다. 이번 차수에는 시간대 자료의 한 시간 차이가 달력의 날짜까지 바꾸는 사례와, 예제를 받은 사람이 제한시간 안에 전체 과제를 통과한 저자 집계를 확보했다. 다른 분야 원전의 추가 판별력, 같은 후보에 이유를 붙였을 때의 사람 판단 개선, 같은 품질의 총 작업시간과 재작업 절감은 아직 미확인이다. [제품 브리프][product] · [연구 운영 규칙][workflow]

## 이번 검토가 인수한 자료

2026-11-23 UTC에 계획 브랜치 `39b42fe`의 최신 번호 REVIEW-13을 먼저 읽었다. 그 검토가 사용한 통합판 `d7e60da`와 이번 통합판 `8036b86`의 진행표를 ID와 상태로 대조했다. 등록 **50→54**, DONE **48→52**, BLOCKED **2→2**다. 신규 DONE은 아래 네 건뿐이다. 052까지의 작업은 직전 검토의 근거와 한계를 이어받았다. 네 작업의 결과 SHA는 각 작업 브랜치 끝과 일치했고 마지막 커밋의 변경 파일은 각각 HANDOFF.md 하나였다. 인계서가 지정한 본문판과 마지막 커밋의 RESULT.md blob도 네 건 모두 같았다. [직전 검토][prev] · [직전 진행표][oldreg] · [이번 진행표][reg]

| 작업 | 인계 / 고정 결과 | 중앙 상태와 작업자가 남긴 수용 범위 |
| --- | --- | --- |
| 053 · 타 분야 원리가 조작을 가르는가 | [9423140][h53] / [87a375d][r53] | 중앙 DONE. 인계에는 **BLOCKED·부분 인계**라고 적었다. 26개 수용 항목 중 요구 5/6, 새 독립 후속 저작 0/6. 직접 읽은 고유 1차 저작 71개의 상당수는 선정에서 제외된 요청 본문이다. [수용 원장][a53] |
| 054 · 제한시간 내 정확 완료 | [425f64d][h54] / [377faca][r54] | 중앙 DONE, 2차 시도에서 부분 인계. 33개 수용 항목. 고유 원저작 23개, 예정 8자리 중 연구 6개, 신규 6자리 중 배정 비교 3개. 별도 개입·과제·루브릭 저작은 1/4다. [수용 원장][a54] · [배당][s54] |
| 055 · 운영판이 변한 뒤의 추천 이유 | [1b86aeb][h55] / [f3faf70][r55] | 중앙 DONE, 인계는 부분 완료. 35개 수용 항목. 배당 산입 37저작. 예정 4판 쌍 중 IANA 2쌍을 실측했고 운영 교통 2쌍은 보류했다. [수용 원장][a55] |
| 056 · 사용자의 표현과 표준 기능명 | [4b7ae5c][h56] / [2f8ec01][r56] | 중앙 DONE, 현재 고정 비교를 마치고 부분 인계. 36개 수용 항목. 고유 1차 저작 109개 중 지정 배당 24/24, 같은 편집 시스템의 저작을 묶는 감도에서는 22/24다. [수용 원장][a56] · [집계][s56] |

중앙 DONE 52건의 `acceptance_evidence`는 모두 빈 배열이다. 신규 네 건의 `source_commit`과 `actual_model`도 비어 있다. 수용 여부는 작업별 원장을 따라갔다. 기존 BLOCKED는 018(세 번째 시도에서 대화 길이 한도)과 035(첫 시도에서 사이버 보안 위험 가능성 표시)이고 둘 다 중앙 결과 SHA가 없다. 이 검토에서 다시 센 대상은 GitHub의 예측·결합·실행·슬롯 원장이다. 외부 원문 판독과 프로그램 실행은 작업자의 관측으로, 사람 실험은 원 연구자의 관측으로 인용한다. [진행표][reg] · [053 예측][p53] · [054 결합][j54] · [055 실행][rs55] · [056 슬롯][sl56]

## 052까지 설계자가 이어받을 판단

| 설계 질문 | 누적해서 확인된 것 | 결정을 바꿀 수 있는 한계 |
| --- | --- | --- |
| 전체 프로젝트가 없어도 목적과 제약을 보존하는가 | DOT-001·002에서 세션을 바꿔 인계를 복원했다. RES-001~004의 합성 입력 6건은 부정 조건 누락을, 2문제·17질의는 동명 제품과 부분 기능의 혼동을 보였다. 020의 주장 전달은 72/73이었다. | 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 020의 충돌 16건 중 완전 해소는 2건이다. 026에서 실제 질문 발송은 0건, 030의 자연 24건 중 같은 변수에 직접 답한 3건에서도 같은 답변자의 권고 변경과 요청자의 신규 시행까지 연결된 사례는 0/3이었다. [누적 검토][prev] |
| 비슷한 이름을 넘어 쓸 만한 부품·타 분야 원리를 찾는가 | 009의 비교 대상 35개에는 기능 중복이 있었다. 010은 분야 단서를 받아 24원문에서 원리 7군을 찾았고, 011은 공개 61스레드·635답에서 부분 질문의 진전 10/33을 찾았다. | 타 분야 답 14개에 요청자 반응이 없었다. 012 합성에서 증가한 근접 오답은 014의 실제 자료 485개에서 재현되지 않았다. 013에서 웹/목록의 역사 선례 회수는 16/176·5/176이었다. 025의 72칸은 지지 2·충돌 14·보류 53·빈칸 3, 029 세 탐색법의 전체 완결은 모두 0/12였다. 분야 힌트를 뺀 033은 8요구×18후보에서 엄격 지지가 넓게 보아 1/144, 당시판으로 0이었다. [누적 검토][prev] |
| 선례를 먼저 보았다면 다른 결정을 내렸을까 | 017은 40사건 중 18건에서 두 날짜를 연결했다. 022 결정 우선 2/24에서 이미 알던 대안의 조건을 고쳐 시행했다. 037에서 같은 목적 반영은 결정 우선 7/8, 노출 우선 3/4였다. 041의 두 저자는 선례 계열을 언급했고 046 링크 우선층에서는 같은 작성자·목적 수정이 2/4였다. | 022의 '미인지→당시 가용→결정 변경→시행'은 결정 우선 0/24, 발견 진술 우선 1/9였다. 045에서 정상·경계 모두 판정 가능한 사례는 0건이다. 046 보강층에서 첫 링크를 수정 이유로 명시하고 패치·시험까지 연결한 경우는 0/4였다. 049는 Matplotlib 3.0.2의 좌표 선택에 따른 PNG·예외 차이를 재생했으나 2.2.2에서는 두 조작이 동률이었다. 30개 범례의 축 크기를 지키는 것과 모든 이름을 읽는 것 역시 다른 목표였다. 인쇄·지도 자료만의 기여는 열려 있다. [누적 검토][prev] |
| 요구와 원문 절의 대응이 사람의 일을 줄이는가 | 021의 두 번 열람에서 요구 완결은 주소 6/23, 절 목록 9/23, 요구–절 대응 13/23, 잘못된 대응 8/23이었다. 038은 네 과제와 채점표를 고정했고, 042는 pandas 43/43 출력과 근접 오답 5개를 점검했다. | 038의 사람 참가자는 0명이다. 034에서 NCQ 패키지 선택 중앙값은 380→57초, 전체 과제는 849→847초였다. 050의 고정 연구에서 배정·시간·최종품질을 같은 시행의 원행으로 연결해 새 비교를 할 수 있었던 것은 소프트웨어 0/6·전체 0/8이었다. [누적 검토][prev] |
| 살아 있는 주소의 추천 이유를 언제 다시 확인할까 | 015의 판정 가능한 현재 추천 195개 중 이유 붕괴 14개, 복원한 과거 83개 중 뒤늦은 붕괴 5개·최초 오류 4개였다. 024의 64이유×16분기는 유지 897·무효 95·최초 오류 16·보류 16이었다. | 019의 사건과 대조 7쌍에서는 경보가 각각 3건이었다. 024의 분기 예산 10/20/40회에서 정기 대 신호 후 발견은 7 대 0, 11 대 8, 11 대 11(각 분모 11)이었다. 028의 유지층 실행 확인은 32셀이다. 재확인 주기를 하나로 정할 근거는 부족하다. [누적 검토][prev] |
| 옛 답과 소비자가 실제 쓴 판을 복원할 수 있는가 | 023은 주소·이유 3/18에서 판·근거 추가 5/18, 변경 관계·시점 추가 15/18로 목적지 복원이 늘었다. 032는 참조 12개가 모두 HTTP 200이어도 교체할 이유가 있었다. 039는 옛 발췌를 12/12 재표시했고 043은 정정 우선층에서 옛 판 대조가 2/4→4/4였다. 051 통제의 경로·필드·변환 기록은 64/64 판정과 일치했다. | 027·032에서 상류 시행일→소비 배포일은 0/12·0/6, 039의 두 시점 복원은 C1 0/12·C2 1/12였다. 036의 절약은 모의값이다. 043 자연 소비자의 과거 사용판은 0/4, 047 소비자 우선층에서 외부 입력 연결은 0/6이었다. 051은 수집 목록을 누락하고 완전하다고 표시하자 거짓 음성 3건이 생겼다. [누적 검토][prev] |
| 상위 세 링크가 서로 다른 대안과 빠진 절을 얼마나 보여 주는가 | 031은 36입력 재생으로 기대표 6행을 고쳤다. 040의 URL·상류·부품별 표시는 필수조건 8·6·8개를 보존했다. 044의 보강 4건에서 완전 대안 수는 2·11·1·0, 048의 두 목록에서는 표시 필드가 같은 URL이 묶였다. | 044의 두 클릭 13/14는 여러 가능한 경로의 합이다. 048의 판 확보는 2/9풀이었고 둘 다 후보가 3개뿐이었다. 052 자연층은 사용자 표현과 게시 목록 연결 0/4였다. 보강 bandersnatch 목록에서 상류를 묶자 5번 S3가 드러났지만 관계는 미러의 보완이었다. 독립 목적과 연결된 보강 풀은 0/1이다. [누적 검토][prev] |

## 새 증거가 바꾼 판단과 여전히 얕은 부분

**053 · 다른 분야 원전은 보존할 속성을 설명했지만 이번 표본에서 조작 선택을 더 좁힌 적은 없었다.** Vega-Lite 40건과 libass 18건의 본문에서 예정 6자리 중 5개를 채웠다. 공통 API에 같은 분야 예제 또는 인쇄·지도 원전을 더한 두 보기에서 추가 단어·그림 수를 맞췄다. 두 보기의 선택과 정상·경계 예측은 5/5에서 같았다. 따라서 다른 예측 중 어느 쪽이 맞았는지를 셀 분모는 0이다. 당시 판·입력·조작과 새 출력이 모두 맞은 공개 관측은 0/20논리셀이다. 자막 두 건에서는 바꿀 여백의 값조차 봉인되지 않았고, 같은 작성자가 세 보기와 일부 창 밖 구현 정보를 보았다. [결과][r53] · [예측][p53] · [후속 대조][o53] · [분모][c53]

연구용 Vega-Lite 5.1.0의 2요구·6변형에서는 SVG 5개와 컴파일 실패 1건이 나왔다. V03 고정 10행은 축 객체의 범주를 읽을 때 목표 하나만 빨갛고, 원래 데이터 행의 속성을 읽을 때 빨강이 0개였다. 2.7.0과 호환 런타임을 함께 쓴 사후 대조에서는 둘 다 10개가 검정이었다. 이 사례로 확인된 것은 지정한 입력과 판의 출력 차이다. 지도식 표기를 적용하면 틀릴 수 있지만 봉인한 지도 카드가 실제로 오답을 낸 사례는 확보되지 않았다. [연구판 출력][re53] · [판별·반례][r53]

**054 · 저자의 공동 집계 한 건은 제품 설명에 쓸 수 있다.** 050이 인용했던 eXoaDocs의 3 대 1을 054가 원문 §5.3.2의 40분 조건까지 연결했다. 같은 네 java.sql 과제에서 정확 완료는 예제 문서 3/12, 기존 문서 1/12였다. 이 표본의 차이는 +16⅔%p다. 과제 3만 보면 3/12 대 4/12로 방향이 바뀐다. 두 수치는 서로 다른 종점을 답한다. 050의 “새 개인 원행 비교 0”도 유지된다. 054의 결합 원장 10행 중 목표 종점 원행을 결합한 행은 0이고, 여덟 연구 자리 중 저자 공동 집계를 찾은 자리는 하나다. 같은 분모의 두 주변수만으로 새 비자명 범위를 얻은 실측 사례도 없었다. 6,200개 정수 조합으로 공식은 검산됐고, 가상 입력은 −10~+20%p를 허용했다. [저자 원문 §5.3.2·Table XII][exoa] · [조건별 산술][b54] · [결합 원장][j54] · [구성 반례][ca54]

자료가 많아 보여도 필요한 비교가 생기지는 않았다. Newton의 24개 사람×조건 단위에 노트북과 응답은 연결됐지만 원래 기능 판정·최종 제출·시계가 빠졌다. Casdoc 122개 조각에는 문서 형식의 배정 대조가 없다. Blueprint 논문 지정판의 Figure 4는 참조 문장만 있고, 같은 코호트 학위논문의 Fig. 5.4는 따로 정렬한 순위열이다. 사람별 시간과 품질을 이어 주는 그림으로 쓸 수 있다는 앞선 해석은 철회한다. 별개로 교육 원고의 사전평균 4.75와 SAV의 4.573은 판 대응이 미확인이다. 여기에 제품 링크의 설명만 달리한 배정 비교나 동등 품질 총시간을 뒷받침할 자료는 없다. [그림 원전][bluefig] · [054 결과 Q1~Q4][r54] · [수용 원장][a54]

**055 · 동일한 추천 이유라도 적용 순간과 확인 환경이 판정을 바꿨다.** IANA 네 정식 자료판의 채택 바이트는 공지 SHA-512와 일치했다. 2024a→2024b 뉴욕의 겨울·여름 두 순간은 유지됐다. 베이루트 2023a→2023b는 4월 20일 21시 UTC에서 +03→+02로 바뀌어 현지 시각이 다음 날 00시에서 당일 23시로 이동했고, 23시 UTC의 결과는 유지됐다. 2023c는 첫 순간을 원래 값으로 돌렸다. 판독 8/8과 빈 폴더 재실행 8/8은 일치했지만 두 판독기가 같은 zic·TZif를 공유했다. 같은 오래된 파일을 주면 둘 다 같은 오답을 낸 통제가 있다. [판독][rs55] · [대조][x55] · [055 결과][r55]

시간대 네 요구의 과거 답은 원본을 미리 갖추지 않은 조건에서 주소·이유 0/4, 옛 판·해시 추가 2/4, 사용 행까지 추가 4/4로 복원됐다. 같은 조건에서 다음 판 판정은 세 보기 모두 0/4였고, 목록과 자료를 미리 갖춘 조건에서는 각 보기에서 두 목적 모두 4/4였다. 냉 조회 합계 30회 중 실패 28회, 수신 902,540바이트였다. 이 비용은 해당 접근 경로에서 측정됐다. MBTA 보관 목록의 권장 구간은 인접 30쌍에서 겹침 0건, 대표 ZIP 요청은 연결 단계 403이었다. 운영 교통 본판독은 0/8이다. 같은 운행 수라도 구성은 달라진다는 예는 작성 통제에만 있다. 어느 소비자에게 어떤 판이 설치됐는지도 열려 있다. [보기·비용][v55] · [판 후보][d55] · [인계][h55]

**056 · 용어를 보태 후보를 하나 찾았지만 두 조건을 확인할 링크까지는 얻지 못했다.** 현재 태그에서 가져온 80본문의 최초판을 읽고 8요구를 고정했다. JSON Schema 40행과 JSON-LD 22행에 원문 표현과 정의 기반 용어를 각각 대입했다. 후보가 있는 요구는 0/8→1/8, 허용한 두 번 열람 안의 완결은 양쪽 0/8이었다. 48자리의 내역은 무매치 45·풀 소진 2·후보 1이다. 새 후보 SC-032는 미확인이다. 예산 밖 C++ 시험은 허용 datatype 하나를 확인하면서 존재하지 않는 열 이름도 받아들였다. 최초 Python 환경의 동적 열 참조 조건은 여전히 미확인이다. [순위][ra56] · [슬롯][sl56] · [조건별 판정][j56]

LD 목록은 이름만 게시했고, 나중에 공급자 코드에서 확인한 framing은 그 필드에 없었다. 읽기 창을 표시 500단어로 바로잡아도 두 조건 판정은 같았다. 처음부터 L 후보가 0개여서 V에 밀린 기존 후보의 비율은 계산할 수 없다. 한 자리에 세 경로를 별도로 적용해 본 결과를 한 사람이 다섯 번 열어 얻은 성과로 합산할 수도 없다. 8요구는 모두 2021년 초이며 두 질문의 JSON-LD 태그는 생성 뒤 붙었다. 당시 전체 모집단·사람의 클릭이나 실제 채택은 미확인이다. 결과 카드에는 전체 구현 0, 조건부 보완 4, 보류 4가 남았다. [열람 창][w56] · [반환 카드][cards56] · [056 결과][r56]

## 다음 네 작업과 결정 기준

| 독립 작업 | 이번에 고정할 비교 | 설계자가 받을 판단 |
| --- | --- | --- |
| 057 · 공동 편집의 되돌리기 · web-pro | 같은 편집 사건열을 보고 수신 API, 같은 분야 예제, 지도 변경·회계 정정 선례가 예측한 보존 조건을 봉인한 뒤 시험의 기대 상태와 대조한다. | 타 분야 링크가 새로 맞힌 조건, 새로 틀린 조건, 사용자의 우선순위만 물을 수 있는 경우를 가른다. |
| 058 · 근거 설명과 잘못된 권고 수락 · web-pro | 동일 후보·권고에서 설명만 달라진 공개 사람 실험을 찾아 틀린 권고의 수락과 맞는 권고의 수락을 각각 복원한다. | 사람이 근거를 보고 오류를 걸러냈다는 문장을 어떤 과제·분모·대조까지 허용할지 정한다. |
| 059 · 상류 변경과 배포 패키지의 실제 출력 · codex-cloud | 같은 베이루트 두 순간을 공개 Python·JavaScript 패키지 배포본에서 다시 읽고, 배포일·내장 자료판·테스트 설치·역사 소비 기록을 연결한다. | 특정 사용자 환경에 옛 이유가 적용된다고 말하려면 어느 판·파일·설치 근거가 더 필요한지 알 수 있다. |
| 060 · 공급자가 밝힌 기능을 검색할 때의 득실 · web-pro | 고정 목록에 출처 있는 기능명을 추가하는 요인과 질의 확장 요인을 교차한다. 기존 8요구와 봉인 뒤 선정할 새 4자리를 따로 채점한다. | 목록 편집 비용을 들였을 때 같은 두 번 열람 안의 완결·부분·오답·밀림이 어떻게 달라지는지 판정한다. |

057~060은 각각 DONE인 053~056 한 건에만 의존한다. 053에서 없던 판별 근거는 시험 기대 상태가 공개된 표본에서, 054에서 분리되지 않던 사람의 판단은 같은 후보를 보여 주는 대조에서 찾는다. 055의 교통 공백은 발행 시각·공통 서비스일을 가진 운영 원본 두 판이 생길 때까지 보류하고, 이번에는 실제로 구할 수 있는 배포본을 따라간다. 060은 검색 규칙을 바꾼 효과와 목록 내용을 바꾼 효과를 분리한다. H1(요구와 근거 절의 연결)과 H2(추천 이유의 보존·재확인)는 별도 판단이다. 새로 검색하기(C0), 주소·판·목적 보관(C1), 발췌·판정 이력 추가(C2) 중 어느 조합이 맞는지는 위 결과와 취득 비용을 보고 결정할 수 있다. [작업별 전체 지시문][next]

[product]: https://github.com/laadkke-arch/agentflow-open/blob/8036b862a0f921196dca57e8532df606bf6f1de6/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/8036b862a0f921196dca57e8532df606bf6f1de6/docs/RESEARCH_WORKFLOW.md
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/39b42fe36567327fddb5c745d8e0a10ba1bca543/docs/workstreams/planning/REVIEW-13.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/d7e60daf1b5b2c918502c407982566369b7149e3/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/8036b862a0f921196dca57e8532df606bf6f1de6/docs/automation/dot-control.json
[next]: NEXT_TASKS-14.json
[h53]: https://github.com/laadkke-arch/agentflow-open/blob/94231403b7ce6debd1ee7bb1a34e86e3956c7920/docs/workstreams/research/AF-RES-053/HANDOFF.md
[r53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/RESULT.md
[a53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/acceptance-evidence.json
[h54]: https://github.com/laadkke-arch/agentflow-open/blob/425f64dda404b4e275acf4eae5ff9244eab36d37/docs/workstreams/research/AF-RES-054/HANDOFF.md
[r54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/RESULT.md
[a54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/evidence/acceptance-evidence.json
[h55]: https://github.com/laadkke-arch/agentflow-open/blob/1b86aeb35a2b93ebcd752d903eb66e702748ba66/docs/workstreams/research/AF-RES-055/HANDOFF.md
[r55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/RESULT.md
[a55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/evidence/acceptance-evidence.json
[h56]: https://github.com/laadkke-arch/agentflow-open/blob/4b7ae5ce472f3a194acaadc950190bb005289441/docs/workstreams/research/AF-RES-056/HANDOFF.md
[r56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/RESULT.md
[a56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/evidence/acceptance-evidence.json
[p53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/predictions.csv
[o53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/outcomes.csv
[c53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/comparison-counts.json
[re53]: https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/replay/results.json
[j54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/joins.csv
[b54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/bounds.csv
[s54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/evidence/source-counts.json
[ca54]: https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/evidence/calculation-check.json
[v55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/views.csv
[x55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/evidence/contrasts.json
[d55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/editions.csv
[rs55]: https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/runs.jsonl
[ra56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/matches.csv
[sl56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/slots.csv
[j56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/judgments.csv
[w56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/windows.csv
[cards56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/cards.md
[s56]: https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/evidence/source-counts.json
[exoa]: https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf
[bluefig]: https://hci.stanford.edu/publications/2010/brandt-dissertation/brandt-dissertation.pdf
