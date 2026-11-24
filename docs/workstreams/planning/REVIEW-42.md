# REVIEW-42 · 어느 링크가 사용자의 조건까지 증명하는가

설계 중인 소프트웨어의 일부와 그 목적을 받으면, 탐색기는 기존 제품·부품·다른 분야의 원리 가운데 어느 것을 어디에 쓸 수 있는지 원문 링크로 설명해야 한다. 이번에 가장 분명해진 차이는 **어느 질문에 답하느냐에 따라 같은 링크의 가치가 달라진다**는 점이다. 언어 코드 표는 도구의 치환 규칙을 증명할 수 있고, 악보나 문서의 출력 보존은 실제로 나온 같은 부분을 봐야 하며, 당사자의 수용은 그 사람이 어느 변경에 답했는지까지 확인해야 한다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

**새 DONE은 AF-RES-169~177 아홉 건이고, 아홉 작업자의 자기 판정은 모두 PARTIAL이다.** 176에서는 원 시험 보고 55건의 표시값을 확인할 수 있었다. 171에서는 같은 이슈를 닫은 뒤에도 당사자의 이견이 기록될 수 있었다. 반면 174의 원거리 원리 예측은 적격 비교가 0건이었고, 175에서 특정 건물 객체의 실제 수신값을 원값과 연결한 사례도 0건이었다. 이 네 수치는 각각 다른 종류의 근거를 센다. [171 회신][replies171] · [174 결과 대조][out174] · [175 속성·방향][dirs175] · [176 개별 단언][assert176]

## 검토 기준과 상태

계획 브랜치 `6a9e326`의 최신 누적 파일 REVIEW-41을 먼저 읽었다. 직전 REVIEW가 명시한 통합판과 이번 통합판의 진행표를 작업 ID와 모든 필드로 비교했다. 기존 166행의 변경·삭제는 0건이다. 추가된 9개 행의 `result_commit`이 각각의 원격 작업 브랜치 끝과 같음을 확인한 뒤 그 SHA의 소유 경로에서 HANDOFF, RESULT, 출처 원장과 판정표를 읽었다. 과거 작업의 판단은 REVIEW-41에서 이어받았다. [41차 누적 검토][r41] · [41차 통합판][before] · [42차 통합판][control] · [두 판의 차이][delta]

| 진행표 기준판 · UTC | 전체 | DONE | 진행·대기 | BLOCKED | 새로 읽은 DONE |
| --- | ---: | ---: | ---: | ---: | --- |
| 41차 `53eaa28` | 166 | 162 | 0 | 4 | 기준 |
| 42차 `128f673` · 2026-11-24 18:50:43 | 175 | 171 | 0 | 4 | 169~177 |

DONE 171건은 연구 169건과 연결 시험 2건이다. 171건 모두 중앙 `acceptance_evidence`는 빈 배열이다. 차단된 네 건 중 018은 대화 한도 뒤 인계가 커밋되지 않았고, 035는 실행 종료 후 인계가 확인되지 않았다. 149는 조사한 7주 중 세 유입 경로를 각각 6건 복원한 주가 0이었다. 151은 최초 N0 응답·독립 가림 판독·원사용자 비용이 미확인이다. 이 네 건은 배정하지 않았다. [진행표와 차단 사유][control]

| 새 과제 | 중앙에 기록된 인계판 | 결과·자기점검이 들어 있는 고정판 | 출처 원장 행 / 작업자 산입 기준 |
| --- | --- | --- | --- |
| 169 · 폐기 언어 코드 | [74925ef][h169] | [f5d2b2f][r169] | [127 / 31저작, 연속 저작의 판을 묶으면 22][s169] |
| 170 · 위키 기능 배포 | [8e4ab12][h170] | [0bcf88f][r170] | [84 / 43저작][s170] |
| 171 · 표준 의견 수용 | [f8a9f72][h171] | [2ace301][r171] | [171 / 99저작·96 URL, 엄격한 범주별 하한 22 충족][s171] |
| 172 · 재사용 노동 | [11d9eb0][h172] | [e0dd973][r172] | [57 / 신규 저작 24, 지정 범주 후보 18/22][s172] |
| 173 · 대체 글꼴 | [317d79c][h173] | [95a46b1][r173] | [61 / 35저작][s173] |
| 174 · 지도 원리의 차트 전이 | [347f0c9][h174] | [5154e9c][r174] | [73 / 42저작, 엄격한 지정 종류 17/22][s174] |
| 175 · 건물 모델 교환 | [b36b503][h175] | [357d92b][r175] | [57 / 실질 자료 23저작][s175] |
| 176 · 시험 결과 계보 | [a347a37][h176] | [7f982bc][r176] | [38 / 실질 자료 30저작][s176] |
| 177 · 택일과 동시 요구 | [f3736d4][h177] | [c497934][r177] | [62 / 40저작·판·원사건][s177] |

이번 검토에서 출처 JSONL 730행을 파싱하고 핵심 CSV의 사건·예정 자리·관측 수를 다시 셌다. 예를 들어 171의 자연 WCAG 회신표 39행에는 ‘원제출자 후속 없음’을 표시한 자리 6개가 들어 있다. 174의 모집표 181행 중 검색 반환은 180행이고 마지막 한 행은 미확보 대조 C2다. 176의 단언표 60자리에는 미제출 5자리가 들어 있다. 출처 원장에는 재열람·접근 실패도 있고 작업마다 고유 저작의 산입 규칙이 다르다. 아래에서 실행이나 편집 결과를 말할 때는 원장의 관측과 원저자의 보고를 표시했다. 이번 검토의 검산 범위는 저장소 원장과 인용 위치이며, 외부 연구 전체의 독립 재현은 미실시다. [171 회신][replies171] · [174 모집][frame174] · [176 단언][assert176]

## 41차까지 이어지는 제품 판단

| 설계자가 결정할 것 | 앞선 결과에서 근거가 닿은 곳 | 아직 갈리는 조건 |
| --- | --- | --- |
| 먼 분야의 아이디어를 보여 줄 때 | 010은 분야 단서로 원리 7군을 찾았다. 033은 단서 없이 본 144쌍에서 당시판 지지 0, 022는 미인지→선택 변경→시행 0/24, 145는 독립 초안 0/16이었다. 157의 196행 자료에서도 당사자·개봉 시각·전후 작품의 엄격한 연결은 핵심 8자리에서 0이었다. 166은 대기열의 입장 승인과 실제 시작이 다름을 보였지만 48예측 셀의 적격 사전 비교는 0이었다. | 원리 설명, 미노출 입력에서의 경쟁 예측, 사용자가 배워서 실제 선택을 바꾼 사건을 따로 입증해야 한다. |
| 부분 구조와 목적을 받을 때 | 020의 전달 주장은 72/73이었지만 모든 충돌을 푼 묶음은 2/16이었다. 103은 외관 10/10을 보존하며 텍스트 선택을 잃었고 107은 개별 발생 위치가 있으면 편집 6/6, 공유 정의만 주면 0/6이었다. 159는 48자리에서 위치로 기능 46개, 소비 역할로 48개를 갈랐다. | 잘못된 문맥에서도 38번 같은 번역 문자열이 나왔다. 선택 객체·다음 조작·보존 속성을 확인할 수 있는 사례와 실제 사용자 확인을 구분한다. |
| 후보를 얼마나 읽고 몇 개를 보여 줄 때 | 040의 완전 적격은 0/8, 044의 고정 풀에서는 두 묶음 방법이 같았다. 114의 ‘충돌’ 138개를 118의 기준으로 해석하면 명시 충돌 7·미확인 131이다. 146의 48후보는 직접 0·부분 15·충돌 14·미확인 19, 검토 폭을 3→8로 넓혀 새로 표시한 세 건은 한 요구에 몰렸다. | 한 후보의 부분 근거 두 개, 서로 다른 두 후보의 공동 충족, 사용자가 허용한 택일은 별도로 판정한다. |
| 링크의 정체와 과거 답을 기억할 때 | 055는 과거 답 4/4와 다음 판 0/4, 075는 전체 후보가 사라지면 단독·공동 1위 주장 각각 16/16 보류, 147은 당시 증빙으로 과거 답 112/112 복원이었다. 150의 세 저장안은 동일성 값과 근거 동시 일치가 7·9·15/16쌍이었고 안정적인 절의 재열람은 주소 하나로 32/32였다. 161은 Wikidata의 잘못된 병합을 되돌린 뒤 하류 P910에 별도 undo가 필요했음을 보였다. | 원판 인용·현행 후계 선택·순위 재입증에는 필요한 이력이 다르다. 161에서 병합 후 새로 더한 유효 필드를 보존한 관측은 분모가 비었다. |
| 언제 발견·갱신하고 어느 사용자에게 권할 때 | 024에서 정기 점검은 무효화 11/11, 신호는 8/11을 포착했다. 신호는 열람 108개가 적고 전송량은 5,672,462바이트가 많았다. 152의 신규 15건에서 신호/희소 공급원 보장 14, 정기 13이었다. 공통 13건의 지연 중앙값은 높은 예산·주류 수요에서 정기 27시간, 신호 51시간이었고 낮은 예산·희소 수요에서는 92.1시간, 27시간이었다. 162는 공식 철회와 필터/일괄 수정 노출 차이를 확인했다. | 빈도·비용·수요가 정책을 바꾼다. 162의 같은 계정·조작 최초 활성 쌍은 0이었다. 158의 28제출은 수신을 입증하지 못했고, 163은 발신 35건 중 원제출자가 특정 통지 내용을 지목해 재개한 보강 1건을 찾았다. |
| 실제 재작업·사람 노동을 줄였다고 쓸 때 | 034는 한 단계 380→57초, 전체 849→847초였다. 156은 하류 수정과 실측 인시 결측 12행을, 160은 이식 1,061.9인시와 비교 쪽 추정치를 남겼다. 164의 계산기 과제는 24명, 세 집단 각 8명이었다. 직접 작성 대비 제공 부품 그대로 사용은 +33.125, 수정 상속은 −17.5 원척도였다(A에서 각 집단 평균을 뺀 값). | 두 대조는 A를 공유하고 A와 수정 집단 차이는 유의하지 않았다. 원척도의 물리 단위·개인 검수표가 미확인이다. 제공자·검수자·유지 노동까지 합칠 수 있는 조건을 먼저 확인한다. |
| 재사용·교환·호환의 근거를 제시할 때 | 154는 입고 성공 10/16 중 명시 원본 회수 10/10, 기본 다운로드 동일 바이트 6/10이었다. 165는 심사판과 실제 소스/바이너리 목록 양쪽을 지정 파일까지 확인한 사례가 jpeginfo 1/8이었다. 167은 공개 파일/도구 쌍을 지목한 보고 10건을 찾았지만 양판·같은 파일·실제 수신값 직접 연결은 0이었다. 168은 CSS 값 전용 셀 0/16→4/16을 확인했지만 해당판 같은 술어의 실제 실행은 0/16이었다. | 파일 포함, 열림, 필요한 속성 보존, 왕복, 복수 출처의 독립 실행은 서로 다른 질문이다. |

이 수치의 사례와 정정 이력은 41차 누적 검토에 연결돼 있다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 정의 변경 뒤 275였고, 136의 9개 고유 면·10회 열람·답과 면의 연결 16쌍은 따로 센 값이다. 153의 독창성·품질 평정과 유용성 평정은 방향이 일관되게 같지 않았고, 155의 출력 문자열과 내부 AST 속성도 갈렸다. 이 근거들은 입력 API, 저장 구조, 수집기 가동 방식, 최종 반환 링크 수를 고정하지 않는다. [직전 검토와 근거 색인][r41]

## 새 아홉 결과의 관측과 한계

### 169~171 · 대상, 배포 위치, 당사자를 식별하는 근거

**169 · 기술적 치환과 사용자의 언어 선택.** 보강층의 단일 후계 네 건은 IANA의 Preferred-Value와 CLDR/ICU 대응이 맞았다. 분할 네 건은 IANA Comments가 각각 후보 둘을 가리키는데 CLDR은 한 값으로 정규화했다. 예를 들어 `leg`는 `enl` 또는 `enx`로 이어질 수 있고 CLDR의 값은 `enl`이다. WALS의 Enxet 개별 레코드는 `enx`와 출전을 실제로 표시한다. 그러나 그 레코드가 과거 `leg`였다가 고쳐졌다는 전후 쌍은 없었다. 고정판의 4+4 alias 추가와 단일 후계 기대 테스트 4건은 확인했다. 자연 모집 순위 0/12, 지정 ISO 원결정 0/8, 실제 라이브러리 실행 0/8이다. 역사 인용·도구의 검색 키·자료가 가리키는 언어 중 무엇이 목적인지에 따라 답이 갈린다. [변경 12행][changes169] · [소비자 33행][cons169] · [CLDR 변경 원문](https://github.com/unicode-org/cldr/commit/d6fc7eac94df0673ecc6cab071b32efdec5cf18f) · [WALS 개별 레코드](https://wals.info/languoid/lect/wals_code_lng)

**170 · 특정 위키에 배포한 것과 편집자가 저장한 것.** DiscussionTools의 2020년 2월 18일 네 위키 설정·운영 동기화는 질의 옵션을 쓰는 시험이었다. 3월 31일에는 베타 선택 설정이 따로 배포됐다. 17개 관측 구간에서 양 끝이 있는 2행은 아랍어·헝가리어 위키에서 새로고침 뒤 링크가 나타난 같은 QA 보고다. 저장을 확인한 구간으로 바꾸면 안 된다. 헝가리어 위키 revision 22880382는 답글이 추가되고 태그가 달린 실물이지만, 당시 태그 허용 방식과 불명인 화면·역할 때문에 첫 UI 저장일을 확정할 수 없다. 잠정 설정·운영로그 8자리, 최초 모집순위 확정 0/8, 같은 계정·조건에서 마지막 저장 실패→첫 저장 성공 0쌍이다. 사이트 설정 철회는 한 건 확인했다. [설정·배포 원장][dep170] · [구간별 조건][interval170] · [태그가 붙은 편집](https://hu.wikipedia.org/w/index.php?diff=prev&oldid=22880382) · [제출이 성공한 듯 보인 실패 보고](https://phabricator.wikimedia.org/T245694)

**171 · 편집자의 처분과 제안자의 수용.** WCAG 여섯 건은 원제출자가 한 사람이다. 33개 공개 댓글에서 그 사람의 후속 답은 0건이었다. XPath 마지막 CR의 예정 여섯 자리는 원번호 목록부터 확보하지 못했다. 따라서 12자리 모두 당사자 입장은 미확인이지만, 앞 여섯은 공개 창을 읽었고 뒤 여섯은 모집도 미완이라는 차이가 있다. 보충 W803은 회신 내용에 만족한 예, W805는 닫힌 이슈에 이견이 남은 예, W806은 부분 수용과 제3자 재개 요구가 갈린 예다. X30007에서 당사자가 특정 문구에 동의한 메일을 X30006의 다른 회신 또는 뒤에 시작한 마지막 CR에 붙이면 시점·대상이 모두 어긋난다. 99저작을 읽어도 자연층 동의율은 추정할 수 없다. [의견 원장][comments171] · [회신 원장][replies171] · [W803의 당사자 회신](https://github.com/w3c/wcag21/issues/803#issuecomment-379070994) · [X30007 원메일](https://lists.w3.org/Archives/Public/public-qt-comments/2016Dec/0017.html)

### 172~174 · 사람의 노동, 화면의 보존, 외부 원리의 기여

**172 · 측정 서식이 완성된 부분과 실제 노동 비교.** 직접 작성·기성 reader 사용·어댑터 추가의 세 경로에 CSV 과제 X(일반 파싱 8 fixture)와 Y(두 열 강제 11 fixture)를 설계했다. 같은 사람의 겹친 활성 구간은 합집합, 다른 사람의 노동은 합산하며, 실패·중단은 배정 분모에 둔다. OC 원행은 조정된 2,610초와 검수·유효성을 구분할 수 있었고, CITR의 8명×30분에서는 목표를 찾은 사람이 0명이었다. 제공자와 사용자 모두의 절감은 계산할 수 없다. 19개 적용 행 중 5개는 설계 예이고, 원 모집 24자리 복원은 0, 지정 유형 후보는 18/22, 물리 단위·동일 기능·전원 배정·독립 검수가 다 갖춰진 비교는 0이다. ‘70인분’은 두 작업자가 겹쳐 일하는 예시의 산술이다. [프로토콜][proto172] · [원행과 설계 예][cases172] · [OC 원표](https://github.com/ValentinBourcier/OC-EXP-REPLICATION/blob/v1.0.0/data/data.csv)

**173 · 출하할 글꼴과 같은 문서에서 보이는 결과.** LibreOffice 4.4.0.3의 설치 규칙은 Carlito·Caladea의 각 네 스타일을 명시한다. 지정한 정확판 배포 아카이브를 직접 확인한 수는 0/4다. O01에서 개발자는 Carlito가 차트 시험값을 유지하고 Liberation Sans가 오류를 감췄다고 보고했다. 같은 이름의 PPTX가 수정됐고 앞뒤 숫자·렌더러·폰트 파일은 고정되지 않았다. O02에서는 글꼴과 허용오차가 함께 바뀌었다. O04의 18쪽과 17쪽은 ‘기대값’과 ‘관측 보고’여서 글꼴 A/B의 실측쌍으로 세면 안 된다. 관측표 13행 중 같은 문서의 엄격한 글리프·줄·쪽 비교는 지정 4자리에서 0이었다. 대체 링크를 읽을 이유와 동일 출력이 필요한 사람이 확인할 파일을 안내할 수 있다. [대체 결정][subs173] · [관측 13행][out173] · [차트 시험 변경 원문](https://github.com/LibreOffice/core/commit/ec73b2894009a4cbb3446f8370b3de7bbbd5a35f)

**174 · 지도의 기준이 차트의 선택을 새로 가르는가.** 지물에 글자를 올바르게 귀속시키는 기준, 생략 표시, 의미상 중요한 이름의 보호는 설계자가 물어볼 구체 조건이다. 하지만 Vega #3558의 이동은 반응형 좌표 계산으로, ggrepel #125의 숨긴 글자와 남은 점 장애물은 도구 자체 규칙으로 설명할 수 있었다. 검색 180행은 고유 이슈 160건이었고, 입력 12자리 중 11은 본문을 읽을 때 이미 결과가 드러났고 1은 입력이 비었다. 4규칙×12자리=48행을 커밋했어도 `valid_pair`가 참인 결과는 0/12다. 직접 본 이미지 네 장은 세 사건에 속한다. 별도로 출판한 같은 조건의 결과 유형 0/4였고 엄격한 지도 배치 결정은 3/4였다. 외부 원리의 예측력과 무단서 발견 효과는 여전히 미확인이다. [사전 예측][pred174] · [실제 판정][out174] · [Vega 제보](https://github.com/vega/vega/issues/3558) · [ggrepel 제보](https://github.com/slowkow/ggrepel/issues/125)

### 175~177 · 값이 전달됐는가, 몇 번 확인했는가, 함께 쓸 수 있는가

**175 · 같은 객체의 값과 시험 집계.** GeoBIM 원문 본문은 파생 단위 항목 누락을 7/16으로 보고했고, 같은 표의 절대수·비율 블록에 표시된 열은 각각 14개였다. 원장은 제출 파일명 후보 15개를 특정했지만 파일 내용 0/6, 설문 응답자와 표 열의 연결은 미확인이다. 다른 구조해석 논문의 표 7은 RFEM→SAP에서 재료 P·하중 E, 반대 방향에서는 재료 F·하중 P로 보고한다. 본문의 ‘문제 없음/하중만 손실’ 서술과도 범위가 다르다. 50 kN/m와 25 kN은 입력 설명에 있는 값이며 양쪽이 별도로 만든 모델의 동일 객체 수신값은 확인되지 않았다. 여덟 자리에서 판·객체·원값·수신값이 다 맞은 것은 0, 실제 왕복도 0이다. 규격·정성 등급은 방향을 다시 물을 근거가 된다. [모델·제출 후보][models175] · [방향 원장][dirs175] · [GeoBIM 원논문](https://doi.org/10.1111/tgis.12709) · [구조해석 교환 시험 표 7](https://www.mdpi.com/2076-3417/11/23/11430)

**176 · 표시, 제출, 실행을 세는 단위.** 보고 생성판의 시험 정의 631개에서 선택한 10개와 주표본 3구현은 30자리다. 원 단언 25개는 PASS, C++ compaction 5개는 미제출이다. 주표본 쌍 30개 중 보고값 일치 20·비교 상대 없음 10이다. 보충 3구현의 30개는 PASS 29·FAIL 1이고 실패는 Gold v0.3.0의 expansion t0123이다. 전체 원보고→표시는 55/55 일치했다. 주표본의 같은 조건·독립 실행 쌍은 **0개 확인, 20개 미확인**이다. 당시 시험 SHA·옵션·실행 로그가 비어 있어 서로 다른 보강 제출 날짜의 이견을 동일 조건 반박으로 올릴 수 없다. 시험 ID가 유지돼도 기대값이 바뀐 예는 주표본 밖의 fromRdf/0027이었다. [시험 정의][tests176] · [단언 원장][assert176] · [원 EARL 제출](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl)

**177 · 원질문의 대안과 같은 빌드의 양립.** mdBook #676은 팝업 없는 단일 페이지나 검색 중 하나를 허용한다. MkDocs M1에서는 핵심 설정 하나로 해결됐다는 작성자 보고가 있다. 반대로 print-site와 privacy를 함께 쓴 사례는 두 순서에서 외부 자산 문제가 남았고, 또 다른 사례는 PDF 생성 후 outline 단계에서 실패했다. J7의 제공 PDF에서는 원작성자가 사이드바 outline을 확인했으나 본문 목차와는 다른 기능이다. 최초 요청 14개, 조합 20행, 응답 비교 16행이 있고, 모집표 281행은 포함 14·제외 또는 보조 27·미판독 240이다. 최초 수정 전 원문 14건, 같은 정확 설치판의 공동 출력 직접 검증, 자연 요청에서 두 링크가 필수이고 공동 성공까지 연결된 사례 모두 미확인이다. 단독·조합·되묻기를 나눌 수는 있지만 일반 양립률 또는 사용자 정확도를 계산할 근거는 없다. [원요구 14건][req177] · [조합 20행][comb177] · [원작성자의 대안](https://github.com/rust-lang/mdBook/issues/676) · [두 플러그인의 자산 문제](https://github.com/timvink/mkdocs-print-site-plugin/issues/101)

## 다음 배정 9건

진행표에 실작업 상태가 남아 있는 연구는 0건이다. 아래 여덟 웹 과제는 서로 결과를 기다리지 않는다. 아홉 번째는 입력과 엔진판이 이미 고정된 실행 검사다. 대기열의 병렬 실행 한도는 진행 담당이 적용하며, 여기서 말하는 독립성은 데이터 의존 관계에 관한 것이다. 배정안의 상태는 모두 `READY_NOT_STARTED`다. 각 작업자는 자기 brief 하나에서 선행 커밋, 표본, 열어 볼 1차 자료 종류·하한, 7개 세부 질문, 표의 열, 반례, 중간 커밋, 완료/부분 인계 기준을 확인할 수 있다. [전체 배정 배열](NEXT_TASKS-42.json) · [진행표][control]

| ID · 담당 · 완료된 선행 | 조사 대상과 판정 단위 | 실제로 달라지는 결정 |
| --- | --- | --- |
| 178 · 웹 · 169 | 폐기된 Python LooseVersion을 사용한 소비자 호출부. 지명한 이슈/PR에서 부모 코드·변경·시험·배포로 이어지는 실자료 문자열. | 현대 표준 버전만 받는지, 과거 비표준 문자열도 받아야 하는지에 따라 같은 후계 링크가 충분한지 판정한다. |
| 179 · 웹 · 170 | CPython의 SQLite 빌드와 실제 Python 연결. 설치판·런타임·SQL 식·출력을 한 조작으로 묶는다. | 상류 기본 기능을 소개할 때와 그 사용자 환경에서 지정 함수가 작동했다고 말할 때의 근거를 가른다. |
| 180 · 웹 · 171 | VS Code 두 종료 마일스톤의 고정 범위 bug 이슈. 원제보·수정·재시험 메시지의 주체와 같은 찾기/탐색 동작. | 검증 표시에서 유지자 확인, 다른 테스터 재시험, 원제보자의 부분/전체 해결 중 어느 문장을 꺼낼 수 있는지 정한다. |
| 181 · 웹 · 172 | DivEMT의 두 언어·각 4개 문서. 직접 번역/두 초안 후편집에서 배정·시간·최종 출력·평가가 같은 행에 연결되는지 본다. | 재사용으로 줄었다고 말할 수 있는 노동창과 검수까지 포함하려면 필요한 원표를 정한다. |
| 182 · 웹 · 173·175 | 공개 MusicXML 여섯 입력과 LilyPond 두 출판판. 같은 마디·기호에 대응하는 XML과 실제 그림이 단위다. | 인쇄용 링크가 증명하는 속성과 편집·재생을 보장하기 위해 여전히 필요한 파일을 가른다. |
| 183 · 웹 · 174 | 고정 숫자 입력 8개, 금액 배분 2개 구현, 의석 배분 원리. 예측을 동결한 뒤 같은 수령자에 대한 구현·시험·공개 결과를 비교한다. | 총액이 같은 상황에서 먼 분야 자료가 나머지 한 단위의 수령자를 새로 구별하는지, 가까운 설명으로 충분한지 정한다. |
| 184 · 웹 · 176 | Debian trixie 패키지 4개×2아키텍처의 이미 공개된 배포·재빌드 기록. 빌드 ID·운영자·산출 해시가 단위다. | 표시 여러 개 중 어디를 대표 원전으로 삼고 실제 별도 빌드를 몇 건까지 확인했다고 적을지 결정한다. |
| 185 · 웹 · 177 | PNG·ZIP 소비자의 flate2 의존 여부를 비교할 네 태그 및 실제 하류 의존성 그래프. 같은 대상·판에서 선택된 backend와 사용자의 순수 Rust 조건. | 독립 경로 두 개를 함께 권할 수 있는지, 택일이면 하나로 충분한지, 확인할 빌드 대상이 무엇인지 정한다. |
| 186 · Codex Cloud · 176 | W3C 보고판의 10개 시험, 고정 Gold·JS 엔진, 매번 새 프로세스로 2회씩. 예정 40행에 원 출력·오류·채점 영수증을 남긴다. | 오늘 같은 시험판에서 두 엔진이 실제 낸 값과 재실행 일치 여부를 판별한다. 과거 제출이 어떤 환경에서 실행됐는가는 별도 미확인으로 둔다. |

이번에는 광범위한 ‘최초 몇 건’ 대신 해당 질문에 맞게 분모를 작게 고정했다. 178은 세 소비자 계보의 목적 표본, 180은 두 마일스톤의 최초 30개 bug 안에서의 조사, 183은 성능·빈도 추정에 쓸 수 없는 구성 입력이다. 184는 같은 기준시각의 배포물과 예전 재빌드 기록을 해석하고, 186은 다른 도메인의 고정된 엔진으로 새 실행을 만든다. 179는 단일 실행이 사용한 SQLite를, 185는 여러 의존 경로가 한 target에 합쳐졌는지를 묻는다. 자료 접근 실패와 사건 부재, 고유 문서 수와 독립 관측 수는 각각 별도 열로 남긴다.

과제 선정을 위해 모집 가능한 원전 입구를 확인했다. PEP 632의 이전 안내와 실제 소비자 PR, VS Code의 원작성자 확인 절차, DivEMT 저자 배포본, LilyPond의 두 버전 시험집, Debian의 재빌드 색인, Cargo의 기능 합성 규칙이 있다. 이 확인은 사건별 실제 수신값이나 효과 판정을 대신하지 않는다. [소비자 PR](https://github.com/scikit-learn-contrib/scikit-learn-extra/pull/141) · [VS Code 확인 절차](https://github.com/microsoft/vscode/wiki/Automated-Issue-Triaging) · [DivEMT 저자 자료](https://github.com/gsarti/divemt) · [LilyPond 출판 시험집](https://lilypond.org/doc/v2.26/input/regression/musicxml/collated-files.html) · [Debian trixie 재빌드](https://reproduce.debian.net/trixie.html) · [Cargo 기능 규칙](https://doc.rust-lang.org/cargo/reference/features.html)

## 바로 시작할 수 있는 검사와 선행 자료가 필요한 검사

186은 176에 이미 있는 10개의 정규 시험 IRI와 W3C 시험판 `8811ba2`를 쓴다. Go v0.3.0의 커밋 `0dbcf4d`, JS v3.1.0 태그가 가리키는 커밋 `30f9067`을 별도로 확인했다. 첫 실행 20개와 새 프로세스에서 반복한 20개를 구분하고, 새 불합격도 결과로 보존한다. 사양 오류 코드가 맞은 음성 시험과 엔진을 설치하지 못한 경우에는 다른 상태를 준다. [선행 시험 목록][tests176] · [Go 고정판](https://github.com/piprate/json-gold/tree/0dbcf4d641a409700208f66945c0d2af7754fba9) · [JS 고정판](https://github.com/digitalbazaar/jsonld.js/tree/30f9067c40066519c917721b8ca4a374eabf15e7)

| 따로 남긴 일 | 필요한 선행 자료 또는 시작 조건 | 이후 확인 가능한 범위 |
| --- | --- | --- |
| 169 정규화와 172 CSV 계약 | 169의 8개 코드·ICU 67.1/68.1, 172의 X/Y fixture와 Python 3.12.10은 이미 명시돼 있다. 독립된 Codex 검사 후보로 보존한다. 언어 의도에는 원결정·실제 개별 태그 수정, 노동 효과에는 배정·역할별 실측이 추가로 필요하다. | 해당 판의 API 반환 또는 parser 합격 범위까지. 라이브러리 기본값으로 자료의 언어를 확정하거나 parser 성공으로 인시를 산출할 수 없다. |
| 170·171의 과거 당사자 | 같은 위키·역할·설정에서의 마지막 실패와 실제 저장, 또는 XPath 마지막 CR의 의견 목록과 같은 원제출자·대상·시점의 회신. | 공개된 특정인의 당시 행동·입장까지. 오늘 재생하거나 다른 회차·제3자의 답을 가져와 대신할 수 없다. |
| 173 글꼴, 174 차트 | 원문서 지문·두 글꼴판·렌더러/옵션·기대 속성이 필요하다. 174의 옛 차트는 고정 폰트·화면·label ID로 사후 회귀만 가능하다. 사전 비교에는 다른 미노출 입력과 결과 개봉 전 예측 SHA가 필요하다. | 같은 입력의 문자·줄·쪽 또는 레이블별 변화. 설계자가 실제 원리를 보고 바꿨는지는 당사자 증빙이 필요하다. |
| 175 IFC | 우선 공개 설문 XLSX와 해당 논문 표 열·제출 파일을 연결한다. 원 Myran IFC, 원본·수신판, GlobalId/물리량·옵션이 맞아야 Codex가 같은 객체를 대조할 수 있다. | 특정 방향의 같은 값·단위 보존. 역방향과 왕복은 별도 입력과 실제 재수입이 필요하다. |
| 177 및 이번 조건부 재생 | J5/J7의 정확한 두 플러그인·lock·기대 공동 출력이 선행한다. 183은 예측 커밋 뒤 실제 태그·가중치·동률 규칙을, 185는 실제 같은 하류 그래프·target·명령·기대 산출물을 인계한 후 Codex가 재생한다. | 특정 빌드 조합의 산출물 또는 특정 입력의 수령자. 사용자의 의도와 과거 실행 여부에는 별도 자료가 필요하다. |

[169 입력][h169] · [170 관측 조건][h170] · [171 회차][h171] · [172 프로토콜][proto172] · [173 보존 조건][h173] · [174 노출·화면 조건][h174] · [175 모델 조인][h175] · [177 재생 조건][h177]

## 판단을 가장 크게 바꿀 불일치 세 건

| 불일치·약점 | 현재 허용되는 주장 | 다음 조사와 판정을 바꿀 관측 |
| --- | --- | --- |
| 편집·배포 시스템이 정한 값과 최종 이용자가 원한 값이 갈린다. | 169에서 기술적 기본 후계 한 개와 언어 후보 두 개가 공존했고, 170은 사이트 설정, 171은 편집 처리와 일부 보강 사례의 당사자 태도까지 확인했다. 177의 택일 요청에는 부분 후보 한 개가 충분할 수 있다. | 178의 실제 하류 호출·입력, 179의 같은 연결에서 실행한 SQL, 180의 원제보자 재시험, 185의 명시 요구와 실효 그래프를 연결한다. 같은 대상의 관측이 없으면 문장의 주어·범위를 좁힌다. |
| 같은 이름·같은 표·여러 배지가 값 보존이나 독립 실행을 과장할 수 있다. | 173은 대체 글꼴 사용 보고, 175는 방향별 정성 등급, 176은 같은 원 단언의 재표시를 입증한다. 엄격한 동일 문서·객체·과거 실행이 서로 다른 위치에서 비어 있다. | 182는 같은 마디의 실제 그림, 184는 별도 빌드 ID와 같은 바이너리 해시, 186은 정확판의 새 출력·오류를 확보한다. 과거 제출과 신규 실행은 계속 다른 행에 둔다. |
| 자료·후보·예측 수가 많아도 노동이나 선택의 개선량은 남지 않을 수 있다. | 172에서 전원·시간·검수가 결합한 재사용 대조는 0, 174에서 유효 예측 비교는 0이다. 146에서 후보를 더 본 효과는 한 요구에 집중됐다. | 181은 배정부터 평가까지 추적 가능한 노동창을, 183은 두 규칙이 갈린 미노출 입력의 실제 수령자를 찾는다. 같은 결과·예측 실패·자료 결측도 분모에 남겨 어떤 근거가 있어야 개선을 말할 수 있는지 밝힌다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/128f673685ec804c526a38e3f89d4d8a43fcd299/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/128f673685ec804c526a38e3f89d4d8a43fcd299/docs/RESEARCH_WORKFLOW.md
[r41]: https://github.com/laadkke-arch/agentflow-open/blob/6a9e3266837549edc764c6bc3a403edfbc45d252/docs/workstreams/planning/REVIEW-41.md
[before]: https://github.com/laadkke-arch/agentflow-open/blob/53eaa286136019510f052179f5f51d901bdac858/docs/automation/dot-control.json
[control]: https://github.com/laadkke-arch/agentflow-open/blob/128f673685ec804c526a38e3f89d4d8a43fcd299/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/53eaa286136019510f052179f5f51d901bdac858...128f673685ec804c526a38e3f89d4d8a43fcd299
[h169]: https://github.com/laadkke-arch/agentflow-open/blob/74925efaf7bd95177273bcdc01cd18cbf1b18057/docs/workstreams/research/AF-RES-169/HANDOFF.md
[r169]: https://github.com/laadkke-arch/agentflow-open/blob/f5d2b2f95f8c6cf9c69f0f9b901780e91703e4b4/docs/workstreams/research/AF-RES-169/RESULT.md
[s169]: https://github.com/laadkke-arch/agentflow-open/blob/74925efaf7bd95177273bcdc01cd18cbf1b18057/docs/workstreams/research/AF-RES-169/sources.jsonl
[changes169]: https://github.com/laadkke-arch/agentflow-open/blob/74925efaf7bd95177273bcdc01cd18cbf1b18057/docs/workstreams/research/AF-RES-169/changes.csv
[cons169]: https://github.com/laadkke-arch/agentflow-open/blob/74925efaf7bd95177273bcdc01cd18cbf1b18057/docs/workstreams/research/AF-RES-169/consumers.csv
[h170]: https://github.com/laadkke-arch/agentflow-open/blob/8e4ab12e3deac49a04817e17163987365171d2bb/docs/workstreams/research/AF-RES-170/HANDOFF.md
[r170]: https://github.com/laadkke-arch/agentflow-open/blob/0bcf88f8c3ce224cc2ecaef66c7b4e5d1110c516/docs/workstreams/research/AF-RES-170/RESULT.md
[s170]: https://github.com/laadkke-arch/agentflow-open/blob/8e4ab12e3deac49a04817e17163987365171d2bb/docs/workstreams/research/AF-RES-170/sources.jsonl
[dep170]: https://github.com/laadkke-arch/agentflow-open/blob/8e4ab12e3deac49a04817e17163987365171d2bb/docs/workstreams/research/AF-RES-170/deployments.csv
[interval170]: https://github.com/laadkke-arch/agentflow-open/blob/8e4ab12e3deac49a04817e17163987365171d2bb/docs/workstreams/research/AF-RES-170/intervals.csv
[h171]: https://github.com/laadkke-arch/agentflow-open/blob/f8a9f723a7acd15ec33664c684a48b3e2bada46b/docs/workstreams/research/AF-RES-171/HANDOFF.md
[r171]: https://github.com/laadkke-arch/agentflow-open/blob/2ace3010d630021286e1ee8200869d70d31fcb3c/docs/workstreams/research/AF-RES-171/RESULT.md
[s171]: https://github.com/laadkke-arch/agentflow-open/blob/f8a9f723a7acd15ec33664c684a48b3e2bada46b/docs/workstreams/research/AF-RES-171/sources.jsonl
[comments171]: https://github.com/laadkke-arch/agentflow-open/blob/f8a9f723a7acd15ec33664c684a48b3e2bada46b/docs/workstreams/research/AF-RES-171/comments.csv
[replies171]: https://github.com/laadkke-arch/agentflow-open/blob/f8a9f723a7acd15ec33664c684a48b3e2bada46b/docs/workstreams/research/AF-RES-171/replies.csv
[h172]: https://github.com/laadkke-arch/agentflow-open/blob/11d9eb0d498e8f9e7fa6eaa5f3425c2ce588d0f2/docs/workstreams/research/AF-RES-172/HANDOFF.md
[r172]: https://github.com/laadkke-arch/agentflow-open/blob/e0dd973a4f79c8c8faa9390b70bb4deceb2ef47d/docs/workstreams/research/AF-RES-172/RESULT.md
[s172]: https://github.com/laadkke-arch/agentflow-open/blob/11d9eb0d498e8f9e7fa6eaa5f3425c2ce588d0f2/docs/workstreams/research/AF-RES-172/sources.jsonl
[proto172]: https://github.com/laadkke-arch/agentflow-open/blob/11d9eb0d498e8f9e7fa6eaa5f3425c2ce588d0f2/docs/workstreams/research/AF-RES-172/PROTOCOL.md
[cases172]: https://github.com/laadkke-arch/agentflow-open/blob/11d9eb0d498e8f9e7fa6eaa5f3425c2ce588d0f2/docs/workstreams/research/AF-RES-172/worked-cases.csv
[h173]: https://github.com/laadkke-arch/agentflow-open/blob/317d79c74935afae00d1fd4c6b4ea33a840f7fb0/docs/workstreams/research/AF-RES-173/HANDOFF.md
[r173]: https://github.com/laadkke-arch/agentflow-open/blob/95a46b1769b23478586455f1d88866f4ce839a4f/docs/workstreams/research/AF-RES-173/RESULT.md
[s173]: https://github.com/laadkke-arch/agentflow-open/blob/317d79c74935afae00d1fd4c6b4ea33a840f7fb0/docs/workstreams/research/AF-RES-173/sources.jsonl
[subs173]: https://github.com/laadkke-arch/agentflow-open/blob/317d79c74935afae00d1fd4c6b4ea33a840f7fb0/docs/workstreams/research/AF-RES-173/substitutions.csv
[out173]: https://github.com/laadkke-arch/agentflow-open/blob/317d79c74935afae00d1fd4c6b4ea33a840f7fb0/docs/workstreams/research/AF-RES-173/outputs.csv
[h174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/HANDOFF.md
[r174]: https://github.com/laadkke-arch/agentflow-open/blob/5154e9cf1e8d4f4f819b92814edafd035ffca765/docs/workstreams/research/AF-RES-174/RESULT.md
[s174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/sources.jsonl
[frame174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/frame.csv
[pred174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/predictions.csv
[out174]: https://github.com/laadkke-arch/agentflow-open/blob/347f0c96944d074605320027fe8653b0b83a41ad/docs/workstreams/research/AF-RES-174/outcomes.csv
[h175]: https://github.com/laadkke-arch/agentflow-open/blob/b36b50399f7851fb785744576f4906e7fdadd963/docs/workstreams/research/AF-RES-175/HANDOFF.md
[r175]: https://github.com/laadkke-arch/agentflow-open/blob/357d92b426841bdae9a9ff7f258df3e535e476ed/docs/workstreams/research/AF-RES-175/RESULT.md
[s175]: https://github.com/laadkke-arch/agentflow-open/blob/b36b50399f7851fb785744576f4906e7fdadd963/docs/workstreams/research/AF-RES-175/sources.jsonl
[models175]: https://github.com/laadkke-arch/agentflow-open/blob/b36b50399f7851fb785744576f4906e7fdadd963/docs/workstreams/research/AF-RES-175/models.csv
[dirs175]: https://github.com/laadkke-arch/agentflow-open/blob/b36b50399f7851fb785744576f4906e7fdadd963/docs/workstreams/research/AF-RES-175/directions.csv
[h176]: https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/HANDOFF.md
[r176]: https://github.com/laadkke-arch/agentflow-open/blob/7f982bc64e67f0abfb457c27b9916fd10c21d039/docs/workstreams/research/AF-RES-176/RESULT.md
[s176]: https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/sources.jsonl
[tests176]: https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/tests.csv
[assert176]: https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/assertions.csv
[h177]: https://github.com/laadkke-arch/agentflow-open/blob/f3736d4dfaed02b5be20aac6601c0bc6c34af689/docs/workstreams/research/AF-RES-177/HANDOFF.md
[r177]: https://github.com/laadkke-arch/agentflow-open/blob/c497934b4ee9c840fa4f3105741ef80dc9b39242/docs/workstreams/research/AF-RES-177/RESULT.md
[s177]: https://github.com/laadkke-arch/agentflow-open/blob/f3736d4dfaed02b5be20aac6601c0bc6c34af689/docs/workstreams/research/AF-RES-177/sources.jsonl
[req177]: https://github.com/laadkke-arch/agentflow-open/blob/f3736d4dfaed02b5be20aac6601c0bc6c34af689/docs/workstreams/research/AF-RES-177/requirements.csv
[comb177]: https://github.com/laadkke-arch/agentflow-open/blob/f3736d4dfaed02b5be20aac6601c0bc6c34af689/docs/workstreams/research/AF-RES-177/combinations.csv
