# PLAN 9 · 설계자가 받은 링크로 어떤 결정을 바꿀 수 있는가

분야를 건너 찾은 원리가 설계에 도움이 됐다고 말하려면, 원문이 **어떤 선택을 새로 열어 주었는지** 보여 줄 수 있어야 한다. AF-RES-033에서 두 검색 방식 모두 여덟 설계의 상위 세 결과로 필수조건을 전부 인용하지 못했다. 목록 전체에서 발견한 한 사례도 최초 설계에 이미 적힌 결정을 설명했다. 사람 대상 연구(034)에는 더 빨리 올바른 설명을 찾은 사례가 있지만 채택 뒤의 수정 노동을 비교한 사례는 없었다. 저장한 링크 연구(036)에서는 같은 현재 원문에 과거 이력을 더해도 12건의 유지·교체·보류가 한 번도 바뀌지 않았다. 세 결과의 관측 대상은 각각 **반환된 근거, 사람의 과제 수행, 기존 참조에 대한 판정**이다. [033 반환창][33win] · [034 효과 원장][34effects] · [036 판독 원장][36dec]

이 제품은 만들고 있는 소프트웨어의 전체 또는 일부와 그 목적을 입력받아, 참고할 완성품·서비스·부품·다른 분야의 원리를 링크와 용도로 돌려주는 탐색기다. 줄이려는 비용은 더 나은 해법을 늦게 알아 설계를 다시 하는 일이다. **H1**은 요구·용도·근거를 연결하면 후보 판단이 나아진다는 가설이고, **H2**는 저장한 추천 이유를 재확인하면 오래된 오판을 줄일 수 있다는 가설이다. 입력 계약, DB, 크롤러, 검색 방식과 기본 보관량은 열려 있다. [제품 브리프][product] · [연구 운영 규칙][workflow]

## 읽은 범위와 상태

2026-11-22 UTC, 계획 브랜치 `090e0a3`에서 가장 최근 파일은 REVIEW-8이었다. 거기서 인계받은 DONE 29건에 진행표 `922bf31`의 **033·034·036**이 더해져 등록 34건 중 **DONE 32건, BLOCKED 2건**이다. 세 브랜치 끝은 중앙의 `result_commit`과 일치했다. 아래 표의 ‘결과’는 각 인계서가 별도로 고정한 본문 커밋이다. 기존 29건은 REVIEW-8에서 이어받았고, 이번 세 건은 해당 SHA의 HANDOFF·RESULT·자체 점검·수용 파일 및 세부 원장과 대조했다. 표집·프로그램 실행·외부 원문의 당시 열람은 작업자가 남긴 기록에 근거한다. [REVIEW-8][prev] · [고정 진행표][control]

| 새 DONE | 브랜치 끝(인계) / 본문 결과 | 다시 센 단위 | 직접 읽은 고유 원문¹ | 수용 조건과 남은 결함 |
| --- | --- | --- | ---: | --- |
| 033 · 다른 분야 원리 검색 | [03ff2eb][33h] / [d6ac67a][33r] | 수신 설계 8, 후보 18, 대응 144, 반환 48슬롯 | 30 | 31/33. R04 권고를 필수로 강화했고 T02 제목이 본문에 남았다. [수용 원장][33a] |
| 034 · 사람의 시간·품질 | [f6dc9b8][34h] / [0fe0ae4][34r] | 핵심 연구군 22, 실험 26, 군·과제 기록 74행 중 핵심 71행, 효과 53행 | 30 | 본문판 33/46에서 게시 조건 6개 충족으로 최종 39/46. 검색 추적 4건, 엄격한 자료·원자료 진단 3건 미충족. [본문 수용][34a] · [최종 보충][34final] |
| 036 · 이력의 추가 가치 | [5682b0d][36h] / [ef839d3][36r] | 9프로젝트·12참조, 네 보기 48판독, 후속 기준 12개 | 50 이상 | 28/33. 사전 노출, 대체 표집 경로 소진, 목적 강도, 현재·이력 중복, 날짜 있는 서지 정정 사슬에 공백이 남았다. [수용 원장][36a] |

¹ 각 과제의 산입 규칙을 적용한 수다. 033은 수신 8·후보 18·별도 현장 4, 034는 소프트웨어 원 연구 15·제품 디자인 3·학습과학 4·별도 원산출물 8을 셌다. 036의 50은 같은 원고의 다른 배포·후기 재열람을 합친 뒤의 하한이다. 중앙에서 DONE 32건의 `acceptance_evidence`는 모두 빈 배열이고 신규 세 건의 `actual_model`·`source_commit`도 비어 있다. 완료 표시는 인계 존재를 확인하는 데 쓰고, 판단의 강도는 작업별 수용 원장을 따른다. [033 직접 열람·한계][33h] · [034 산입표][34counts] · [036 최종 집계][36counts] · [진행표][control]

018은 세 번째 시도에서 대화 길이 한도에 도달했다. 035는 첫 시도가 사이버 보안 위험 가능성 표시로 종료됐다. 둘 다 공식 인계와 결과 SHA가 미확인이다. 따라서 035에 배정했던 Go 값 추출과 외부 배열 소비자 간 전달은 여전히 열린 질문이다. [진행표의 상태·사유][control]

## 앞선 29건에서 이어지는 판단

| 작업 | 지금 쓸 수 있는 근거 | 남아 있는 경계 |
| --- | --- | --- |
| DOT-001·002, RES-001~004, 020 | 작업 인계·복원과 내부 검사가 가능했다. 합성 입력 6건에서 분해가 부정을 누락했고, 2문제의 17질의에서는 동명 도구와 부품이 섞였다. 003은 주소·대상·목적상 대체성을 분리했고 004는 합성 18행의 필수조건과 전이를 판독했다. 020은 73개 주장 중 72개의 전달을 확인했다. | ‘문제 × 후보 × 제안한 용도 × 설정 × 근거’가 판단 단위다. 020의 충돌 16개 중 완전 해소 2, 부분 해소 8, 미해소 6이다. |
| 009~014 | 비교한 시스템 35개가 검색·목록·LLM과 기능을 공유했다. 분야 힌트를 준 010은 본문 24개에서 원리 7군을 찾았다. 011은 실제 61스레드·635답에서 부분 질문 33개 중 10개의 진전을 확인했다. 013의 설계 문서 31개에서 역사적 선례 176개 중 웹 검색은 16개, 목록은 5개를 찾았다. | 011의 전이 답 14개에서 질문자 반응은 미관측이다. 013의 정답 밖 후보 178개 중 170개가 문서상 유용했으나 146개는 같은 분야의 대안이었다. 012의 합성 질의에서 인라인 한계 문구가 늘린 상위 근접 오답(평균 0.394→0.755)은 014의 485자료에서 재현되지 않았다. 별도 필터는 610슬롯의 오답을 5→3으로 줄였지만 새 후보 329개 중 한계 보강은 15개였다. |
| 015~017·019·022 | 015는 500개 추천 이유 중 현재 판정 가능 195개에서 붕괴 14개를 찾았다. 과거를 복원한 83개는 후발 붕괴 5·최초 오류 4였다. 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 017은 늦은 발견 40건 중 두 날짜가 이어진 18건을 확인했다. 022의 결정 우선 표본 24건에서 이미 알던 해법의 조건을 정정한 뒤 시행한 사례는 2건이었다. | 017의 명시적 미인지 2건, 당시 검색 가능성 확인 0건이다. 주 표본의 타 분야 주 관계는 0/40이고 별도 기원 조사에는 7경로가 있었다. 022의 ‘미인지→당시 이용 가능→발견이 결정 변경→시행’은 0/24, 발견 진술로 고른 보조군은 1/9였으며 33건의 절감 노동은 미확인이다. 019의 7쌍에서 사건과 대조에 각각 경보 3건이 울렸고, 알려진 공지 URL을 주면 직접 확인 35/35, 신호 뒤 확인 13/35였다. |
| 021·023 | 후보와 2절 열람 예산을 고정한 021은 주소만·근거 절 목록·요구와 절 연결의 실제 인용 완결이 6/23·9/23·13/23이었다. 023의 카탈로그 18사건에서 목적지 선택은 주소·이유 3, 식별자·판·근거 추가 5, 변경 관계·시점 추가 15건이었다. | 021에서 절을 열기만 한 마지막 값은 14/23, 잘못 연결했을 때 인용 완결은 8/23이었다. 023의 가장 풍부한 보기에는 사후 정정도 들어갔고 실제 자동 복원은 0/18이다. 요청 때 새로 검색(C0), 조건부 링크 보관·재방문(C1), 주장·근거·판정 이력 보관(C2)은 조합할 수 있는 선택지다. |
| 024·028 | 런타임 64이유 × 16분기의 1,024셀은 유지 897·무효 95·최초 오류 16·보류 16이었다. 분기 20회에서 정기 직접 방문은 무효 이유 11/11, 신호 뒤 방문은 8/11을 찾았다. 10회에서는 7/11·0/11, 40회에서는 모두 11/11이었다. 028은 유지층 26이유의 32셀에서 고정 Linux 용도를 재현했다. | 20회 조건에서 두 방식은 총 320요청씩이었지만 신호 방식이 본문을 108개 덜 읽고 약 5.67 MB를 더 받았다. 나머지 유지 865셀은 미실행이고, 대조층에서는 명령·모듈·인수의 정확한 범위가 판정을 바꿨다. |
| 025·029·031 | 025의 원 반환 72슬롯은 지지 2·충돌 14·보류 53·빈칸 3이었다. 새 대상은 두 방식 각 25슬롯에서 인용 완결이 없었다. 029의 새 설계 12건에서 부분 요구의 인용 완결은 공통 검색 2, 추가 웹 검색 4, 제공자 내부 탐색 3건이었다. 031은 알려진 추천 3개를 계약 36행에서 빈 폴더로 재생했다. | 029의 추가 성공은 이미 언급된 대상에서 나왔고 전체 요구 완결은 세 경로 모두 0/12였다. 양 경로 모두 예산을 지킨 8쌍에서는 1·3·1이었다. 031의 36행은 양성 11·대조 21·경계 4이며 6행은 기대를 정정한 뒤 재생했다. Arrow의 특정 Java 수신 값, DataFusion accessor의 일부 타입, Jupyter 메시지 인수까지 확인했다. 대용량 Parquet 종단과 실제 프런트엔드 자동 전달은 미확인이다. |
| 026·030 | 026은 24요청에 세 답변 전략을 고정했다. 실제 발송 0회였다. 030의 최초 요청 표본 24건 중 실제 질문은 8건, 같은 변수의 직접 답은 3건이었다. 질문을 보고 보강한 8건에서는 각각 7건과 6건이었다. | 같은 답변자의 기존 권고 변경과 요청자의 같은 목적 신규 실행까지 이어진 사슬은 직접 답 층에서 0/3·0/6이다. 진단 재현, 첫 구체 제안, 기존 제안 변경을 구분해야 한다. 32사례의 최초 본문 전체판은 미복원이다. |
| 027·032 | 027의 소비자 우선 12참조는 소스 용도 유지 5·실패 보고 2·보류 5였다. 032는 실제 배포 HTML의 외부 참조 12개에서 같은 목적의 href 수정 5건(독립 소스 수정 4건)을 찾았다. 원 참조 12개는 모두 HTTP 200이었다. | 바뀐 href 5개의 현재 판정은 유지 4·교체 1, 그대로인 7개는 유지 5·교체 1·보류 1이었다. 상류 실제 시행→소비자 HTML 출판의 엄격한 날짜쌍은 두 표본에서 0/12·0/6이다. 풍부한 보기의 내부 판정 일치 11/12·5/6에는 현재 내용·수집자 해석·이력이 함께 들어갔다. |

이 표의 수치와 예외는 이전 누적 검토에 실린 고정 근거로 추적할 수 있다. [REVIEW-8의 근거·사례·분모][prev]

## 새 결과에서 달라진 판단

### 033 · 후보가 있었는가, 검색 결과가 그 근거를 보여 줬는가

Rust와 Kubernetes의 최초 제안 8건에 도서관·교통·공식통계 원문을 각 6개씩 대응했다. 분야명을 주지 않고 원문 표현 S와 작동 관계로 다시 쓴 표현 R을 같은 BM25 검색기에 넣었다. 288개 순위에서 상위 세 결과 48슬롯을 다시 세면 교통 35·도서관 9·통계 4다. 반환한 200토큰 창에서 필수조건을 전부 인용할 수 있는 사례는 상위 1·3 모두 S 0/8, R 0/8이다. 전체 문서의 부분 단서까지 허용한 상위 3 결과는 양쪽 모두 있는 질문 4개, S만 1개, R만 1개, 어느 쪽에도 없는 질문 2개다. [순위 원장][33rank] · [실제 반환창][33win] · [질문별 재집계][33count]

세 분야 판정 원장의 144쌍은 **지지 1·충돌 9·부분 50·미확인 84**다. 유일한 R05–L06에서 밴쿠버 공공도서관은 AV 자료 단독 요청과 AV가 딸린 책의 제공관 재량을 구분한다. Kubernetes 원안에는 복합 요청의 접수와 공급자의 실제 제공을 구분하는 결정이 이미 들어 있었다. 두 검색에서 문서는 10·12위였고, 최고 점수 창에는 필요한 분류 절도 없었다. 명시적 접수 허용 문장만 인정하면 이 쌍도 부분으로 내려간다. 따라서 현재판 적격 질문은 넓게 1개(양쪽 모두 놓침), 좁게 0개(조건부 회수율 해당 없음)다. 당시 이용 가능을 확인한 후보는 18개 중 1개이며 당시판으로 엄격 지지한 쌍은 0개다. [도서관 판정][33lib] · [비판적 재판독][33crit] · [수신 최초 제안][kube]

결론의 약한 지점은 검색 횟수보다 **적격 후보와 검색 표현**이다. 8개 수신 설계가 모두 2020년 1월이고 제공 분야는 미리 정해졌다. S/R의 원토큰 합은 각각 560이지만 유효 고유 검색어 합은 309/348로 달랐고 검색기가 부정어 `not`도 제거했다. 상위 세 문서 집합이 7/8에서 바뀐 사실로 역할·관계 추론 능력이나 자유 웹 성능을 추정할 수 없다. 실제 채택을 입증한 수신 설계도 없다. [방법과 민감도][33r] · [자체 점검][33self]

### 034 · 일찍 찾은 시간과 전체 작업에서 아낀 시간

핵심 22연구군·26실험의 설계 등급은 무작위 또는 순서 균형 비교 19, 비무작위 3, 불명 2, 무대조 2였다. Unakite에서 새 참여자 16명이 모두 정답 설명 3개에 이르기까지 평균은 개입 114.63초·대조 332.56초였다. Strata에서 20명의 재사용 판단은 292.1초·432.7초, 유효 이유는 평균 7.9개·4.5개였다. 특정 과제에서 시간과 관측 품질을 함께 말할 수 있는 예다. 준비자가 표를 만드는 노동, 도구 UI나 추가 정보, 구현 후 재검은 이 값 밖에 있다. [실험·군 원장][34studies] · [효과·분모·원문 위치][34effects]

NCQ의 패키지 선택 중앙값은 380→57초였지만 총 과제 중앙값은 849→847초였다. 기본 도구를 먼저 쓰는 순서였고, 두 중앙값의 차이로 사람별 남은 단계의 노동을 복원할 수 없다. ExampleOverflow의 45분 품질 점추정은 개입 1/4·대조 2/4로 반대 방향이지만 군당 5명이다. Acar의 두 자료원에서 전체 분석 시행의 안전한 기능 완성은 각각 18/52였으며, 기능에 성공한 시행만 분모로 삼으면 보안 비교가 달라진다. ‘전체 작업도 빨라진다’, ‘품질이 동등하다’는 단정은 이 자료를 넘어선다. [효과와 반례][34effects] · [분모 정정][34revs]

**같은 환경에서 제품 링크만 달라진 비교는 0연구군, 첫 채택 뒤 실제 수정 노동을 대조한 연구군도 0**이다. 원산출물 8개 중 참여자 시간 원자료는 0개였다. 1주 후 사용 보고, 첫 과제 안에서의 수정, 학생 후검사는 각각 다른 종점이다. 네이티브 색인 최초 30개의 완전한 기록, 일부 보조 질의 순위와 인용망 확인이 빠져 ‘이런 연구가 어디에도 없다’는 결론도 성립하지 않는다. 두 군·두 시점의 연구 구상은 남아 있으나, 공개 근거가 있는 실제 과제지·대조 카드·독립적으로 채점할 답안과 사람의 관측 결과가 다음 단계다. [검색 공백·진단][34final] · [미시행 비교 설계][34future]

### 036 · 현재 근거를 읽는 비용과 과거 근거를 다시 꺼내는 비용

기본 B는 원 href·문맥·판·목적을 포함한다. N은 현재 도착 절이나 필요한 추가 원문, H는 과거판 근거다. 48판독을 참조 ID로 짝지으면 B와 B+H에서 각각 12건 모두 보류였다. B+N과 B+N+H에서 각각 **유지 11·교체 1**로 12쌍의 행동이 모두 같았다. R01에서 H가 과거 tarball 주소를 제시했지만 그 보기에서 대체 절까지 확인하지 못했다. 이후 기준 판독자가 찾은 HTML 주소는 별도 관측이다. 특정판 재현 목적은 G03 한 건이고 B와 N에 이미 2018판이 있었다. 일부 N 카드 5건에는 이력도 있었다. 모든 수집자 해석을 빼거나 외부 독립 정답을 요구하면 적격 분모는 각각 0이다. [네 보기의 행동][36dec] · [기준 원장][36adj] · [참조와 목적][36refs]

첫 수집 157 GET에 판정 봉인 뒤 기준 확인 59 GET가 더해졌다. 재개 감사 10 GET를 포함한 실제 합은 226 GET·248 HTTP 교환·실패 14·최종 응답 본문 263,036,195바이트다. 후속 판독 원장 누락이 정정되면서 비용 분모가 바뀌었다. **두 번째 조회는 모의**였다. 이미 아는 경로에서 N만 다시 구성하면 C1과 C2 모두 17 GET, N과 H의 같은 근거를 복원하면 C1 29 GET 대 C2 17 GET 및 로컬 H 읽기 12회였다. 차이 13,011,463바이트도 모의값이다. 판·문맥을 가진 C1과 H·출처를 더한 C2의 예시 직렬화 크기는 12,153·38,145바이트다. 이 수치로 실서비스 절감액, 사람 판독 시간이나 최적 보관 정책을 정할 수 없다. [비용 범위 정정][36err] · [재개 감사와 실측 범위][36cost] · [모의 재조회][36replay]

## 서로 어긋나는 결론과 다음 네 질문

| 판단에 걸리는 근거 | 어떤 차이를 판별할 것인가 | 다음 독립 작업 |
| --- | --- | --- |
| 010·017에서는 타 분야 원리와 기원 경로를 찾았고, 029·033에서는 새 원리가 설계 행동을 바꾼 인용 완결 사례를 찾기 어려웠다. | 사례를 출처명으로 뽑았는지 먼저 공개하고, 당대 출처·기존 결정·달라진 선택·반영 증거를 연결할 수 있는가? | **037 · web-pro** — 처음 설계를 보고 뽑은 사건과 저자가 출처를 명시한 사건을 분리해 전이 사례와 반례를 구축한다. |
| 021의 근거 연결과 034의 도구 묶음은 좁은 과제에서 도움을 주었다. 022·034에는 채택 후 노동을 비교할 측정값이 없다. | 링크를 골라 준 기여와 설명을 붙인 기여를 나눠, 같은 요구의 최초·재검 품질을 실제로 채점할 준비가 됐는가? | **038 · web-pro** — 공개 결정 4건으로 세 보기의 실제 과제지·근거·정답과 예외를 제작한다. 사람의 효과는 추후 시험에서 판정한다. |
| 023·032의 풍부한 보기에서 판정이 늘었고, 036은 현재 내용을 같게 하자 이력 추가의 행동 변화가 0/12였다. 이력 재구성 비용은 모의에서만 차이가 났다. | 같은 저장물만 받아 실제로 다시 찾을 때, 현재 용도 판정과 과거 근거 복원이 각각 몇 번의 요청으로 어디까지 되는가? | **039 · codex-cloud** — 036의 12참조에서 C1·C2 저장물만 전달한 재조회를 실행하고 위치 발견·본문·비용을 실측한다. |
| 003·020은 주소·대상·용도를 분리했지만 같은 저장소의 서로 다른 부품을 한 카드로 접었을 때 잃는 근거는 측정하지 않았다. | 세 자리를 줄 때 중복 제거로 다른 대안이 살아나는 경우와, 필수 부품·판·용도가 숨는 경우를 무엇으로 가를 수 있는가? | **040 · web-pro** — 새 소비자 요구와 고정 링크 목록에서 URL·프로젝트·용도별 묶음의 실제 표시 결과와 오병합을 비교한다. |

037은 과거 결정의 증거, 038은 향후 사람 비교에 쓸 자료, 039는 같은 저장물의 실제 재조회, 040은 지금 반환할 결과의 묶음을 맡는다. 네 작업의 입력은 이미 DONE인 고정 커밋이다. 서로의 산출물 없이 시작할 수 있다. [작업별 지시문·산출물·수용 조건](NEXT_TASKS-9.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/922bf3171cab62f30469720ac80327ad3f24fbf9/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/922bf3171cab62f30469720ac80327ad3f24fbf9/docs/RESEARCH_WORKFLOW.md
[control]: https://github.com/laadkke-arch/agentflow-open/blob/922bf3171cab62f30469720ac80327ad3f24fbf9/docs/automation/dot-control.json
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/090e0a34e5041285b08c634c2fb4baa130b1d5e8/docs/workstreams/planning/REVIEW-8.md
[33h]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/HANDOFF.md
[33r]: https://github.com/laadkke-arch/agentflow-open/blob/d6ac67ae199b8205772587bcf7d583559aff44b4/docs/workstreams/research/AF-RES-033/RESULT.md
[33a]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/acceptance-evidence.json
[33win]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/returned-window-audit.jsonl
[33rank]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/rankings.csv
[33count]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/recount.json
[33lib]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/judgments/library.jsonl
[33crit]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/judgments/critical-review.jsonl
[33self]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/SELF_CHECK.md
[kube]: https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md#L98-L117
[34h]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/HANDOFF.md
[34r]: https://github.com/laadkke-arch/agentflow-open/blob/0fe0ae4510e0052031919c748972dcf4bd4a7cbc/docs/workstreams/research/AF-RES-034/RESULT.md
[34a]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/evidence/acceptance-evidence.json
[34final]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/evidence/acceptance-finalization.json
[34counts]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/evidence/counts.json
[34effects]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/effects.csv
[34studies]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/studies.csv
[34revs]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/REVISIONS.md
[34future]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/future-study.md
[36h]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/HANDOFF.md
[36r]: https://github.com/laadkke-arch/agentflow-open/blob/ef839d30d300e20f092dd7f0d57542f0773b77f8/docs/workstreams/research/AF-RES-036/RESULT.md
[36a]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/evidence/acceptance-evidence.json
[36counts]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/evidence/final-counts.json
[36dec]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/decisions.csv
[36adj]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/adjudication.csv
[36refs]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/references.jsonl
[36err]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/ERRATA.md
[36cost]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/evidence/resume-cost-summary.json
[36replay]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/evidence/replay-summary.json
