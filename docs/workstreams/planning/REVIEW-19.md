# REVIEW-19 · 설계에 옮길 수 있는 것과 그 판단을 다시 확인할 자료

**다른 분야의 원리는 개발자가 다음에 가를 선택을 구체화할 수 있다.** 예를 들어 저장소를 넘길 때 접근권만 이전했는지, 수신 조직이 유지 책임까지 받아들였는지를 따로 확인하는 것이다. 새 검색의 세 제안에서 같은 구성의 두 필수조건을 모두 입증한 대안은 0건이었다. 다른 세 연구에서는 한 필드가 동작을 가를 때의 조건부 답, 특정 범위에서 후보가 유일함을 다시 증명할 기록, 찾은 문서가 실제로 보여 준 근거의 범위를 확인했다. 링크의 발견·부분 활용·채택 근거를 구분해야 이후 설계자가 어느 선택을 받아들일지 결정할 수 있다. [073 조건별 원순위][j73] · [074 정책 비교][s74] · [075 재계산][s75] · [076 표시 원장][s76]

## 검토 범위

[REVIEW-18][prev]의 [통합판 39cadb6][old]과 [최종 통합판 0d2b084][reg]의 모든 작업 행을 비교했다. 등록 70→74, DONE 68→72, BLOCKED 2→2다. 기존 70행은 필드까지 같았고 018·035는 BLOCKED다. 이번 중간 확인판 [2557797][mid]에서는 DONE 71·RUNNING 1이었고, 최종판에서는 073 한 행의 상태·결과 SHA·진행 시각만 바뀌었다. 최종 RUNNING은 0이다. 새 DONE 073–076은 중앙에 등록된 결과 SHA에서 각각 인계·결과·세부 원장을 읽었다. 네 인계 커밋은 확인한 브랜치 끝과 일치하고 마지막 변경은 각각 HANDOFF.md 한 파일이다. 중앙 DONE 72행의 수용 근거 배열은 모두 비어 있어 연구 수용은 아래의 개별 원장으로 판정했다. [제품 목적][product] · [연구 운영 규칙][workflow]

| PLAN#18 작업 | 중앙 상태 / 연구자의 인계 판정 | 고정 자료 | 이번 검토에서 사용할 수 있는 범위 |
| --- | --- | --- | --- |
| 073 · 일반·관계·대상/역할 질의 | DONE / 연구 PARTIAL | [인계 28dfa4d][h73] · [결과 6713e47][r73] | 3개 제안·9보기·18질의·90순위. 대상과 역할을 되살린 질의의 부분 근거 및 실패를 보존했다. 세 창설판 모집과 실제 대상 적용은 미확인이다. |
| 074 · 단일 답·조건부 답·질문 | DONE / 연구 PARTIAL, 검토용 인계 | [인계 b25a389][h74] · [연구 결과 34f3a55][r74] | 실제 이슈 8건과 별도 구성 대조 4건. 양쪽 값을 직접 판별할 수 있는 분모는 구성 대조 4건이다. |
| 075 · 존재·유일·공동 1위 재검증 | DONE / REVIEW_READY | [인계 4b2a29b][h75] · [결과 8a8fe9e][r75] | 유한 등록부 둘의 16개 주 전후쌍과 별도 손실 대조. 실제 사용자에게 가장 적합한 후보인지까지는 알 수 없다. |
| 076 · URL·발행자 설명·동작 카드 | DONE / REVIEW_READY | [인계 81b8b2c][h76] · [결과 abe6a4f][r76] | 원자료 20후보에 자연 요청 6건과 교정 요청 6건을 각각 대조. 자연군과 교정군은 서로 다른 질문에 답한다. |

이번 검토에서 073의 90개 판정행 및 사후 결정 원장, 074의 108개 정책행과 075의 288개 점수행, 076의 후보–요구 240쌍과 상위 표시 108자리를 다시 집계했다. 076의 고정 원문을 이용해 오프라인 절차를 두 번 재생하고 순위·표시·비용 등 원장 7개와 표가 보관본과 일치하는지 확인했다. 외부 원문의 현 상태, 새로운 사용자 반응, 원래 사용자의 기기에서의 실행은 이번 검토 관측 범위 밖이다. [074 조건 원장][cr74] · [075 짝 원장][p75] · [076 재현 절차][rep76]

## 이 파일에서 이어받을 전체 흐름

제품의 요청은 소프트웨어 전체 또는 선택한 부분의 구조·목적·지켜야 할 조건이다. 찾을 대상은 완성 제품·서비스와 사이트, 일부 기능, 다른 분야에서 옮겨 쓸 작동 방식이다. 설계자는 링크를 따라가 더 조사할 수 있다. 어떤 입력 형식·DB·검색 방식을 고정할지는 열린 선택이며, 최종 조립자가 대안·반례·조건을 다시 읽을 수 있어야 한다. [제품 연구 브리프][product]

| 설계자의 결정 | 072까지 실제 확인된 것 | 해석의 경계 |
| --- | --- | --- |
| 언제 문맥을 더 받나 | 초기 부분 요청에서 금지 조건이 빠졌다. 020은 주장 72/73을 전달했으나 충돌 완전 해소는 2/16. 070의 실제·진단 24건 중 새 작성자 값은 진단 1건에서 조건부 후보를 좁혔다. | 070은 독립 정오 변화를 판별한 분모가 0이었다. ‘후속 설명이 있었다’만으로 물을 가치나 시간을 계산할 수 없다. |
| 다른 분야에서 무엇을 가져오나 | 010은 분야 단서가 있는 원전에서 7개 원리군을 찾았다. 033의 단서 없는 144쌍은 넓은 지지 1쌍·당시판 지지 0쌍. 069에서는 일반 검색이 Inkscape 수정 위치를, 관계 검색이 Chime의 ‘요청 접수와 말단 적용을 따로 확인’하는 시험 관점을 냈다. | 069의 세 문제에 확인된 두 조건 적합 해법은 0건이었다. 적합 판정 기회가 부족한 행이 많았고 실제 접근도 25 대 33회였다. 적중 수로 개발자가 채택한 새 선택의 수를 대신할 수 없다. |
| 근거가 의사결정에 도움이 되나 | 021의 두 절 예산에서 공식 지지와 근거를 함께 회수한 수는 주소 6/23, 절 목록 9/23, 조건–절 연결 14/23, 오연결 8/23. 066에서는 같은 주소가 반대 권고 양쪽에 붙었고 다른 권고의 출처가 결과행에 섞였다. | 022의 결정 우선층에서 미인지→변경→시행의 완전 연쇄는 0/24. 034에서 부분 선택 중앙시간은 380→57초였지만 전체 과제는 849→847초였다. 실제 채택·재작업 개선은 여전히 미확인이다. |
| 과거 답의 무엇을 다시 보나 | 032의 배포 출발층 12참조에서 현재 용도 유지 9·교체 2·보류 1. 055는 과거 답을 0/4→2/4→4/4까지 복원했지만 다음 판 판단은 모두 0/4였다. 071은 과거 원본을 잃은 통제 22쌍에서 실제 조각·설정을 보관한 보기만 22/22 재계산했다. | 071의 현재 판단은 모든 방식이 새 주소를 받아 거기서 계산했다. 주소 발견이나 후보 전체의 완전성은 측정하지 않았다. |
| 언제 링크만 두고 언제 설명을 더하나 | 060·064·068에서 후보를 찾거나 시작 절을 바꿔도 두 조건의 공동 근거는 자주 비었다. 072의 동결 자료집 6×20에서 카드가 부분 후보 1/6·원거리 원리 1/14를 상위 3에 넣었다. | 072의 자연 직접 적격 분모는 0. 최종 54자리 중 개별 판독 메모는 6개였고 출력 코드가 공동 충족을 0으로 고정했다. 해당 수치로 오추천 방지 효과를 말할 수 없다. |

표의 과거 수치는 각 원래 모집층·예산에 관한 것이다. 초기 인계 시도부터 069~072까지의 원자료와 정정 근거는 [직전 누적 검토][prev]에 연결돼 있다.

## 새로 확인된 네 가지 결과

### 073 · 대상과 책임 주체를 복원하면 더 구체적인 선례를 찾는가

세 설계 제안의 일반 질의 A, 관계어 위주 B, 대상과 역할을 되살린 C를 비교했다. Jupyter Book의 조직 편입에서 B는 ‘그룹 사이의 이동’을 기하 부품의 이동으로 해석한 결과를 냈다. C는 저장소·유지관리자·관리기구를 되살려 실제 위임·승인 절차를 찾았다. 그 결과 접근권은 넘겼지만 수신 기구가 유지 책임을 받아들이지 않은 저장소를 구별 입력으로 제시할 수 있었다. A의 원래 적격 1건도 해당 절차가 특정 프로토콜 부합과 제외 저장소의 권한 경계를 보증하지 않아 철회했다. 다른 제안에서는 버전 태그를 무시하는 구형 독자와 이전 버전 내용을 실제 생성하는 절차를 가르는 시험 관점이 나왔다. 대상 시스템에서 이를 실행한 횟수는 0이다. [제안별 선택과 반례][choices73] · [조건별 원순위][j73]

세 보기가 각각 반환한 30자리에서 두 조건을 함께 입증한 후보는 모두 0건이었다. 원자료 직접 판독이 연결된 순위는 46자리로, 43회 독해와 그 URL을 다시 연결한 3자리였다. 예산 때문에 미열람한 22자리는 근거 있는 거절에 산입하지 않는다. 원 탐색 70연산은 보기별 22·24·24였고 제안별 7·7·8의 공통 상한을 적용한 순위행은 51/90이었다. 사후 조사 62연산 및 결정 원장 23행은 새 적중 수에 넣지 않았다. “단순히 단어를 보태면 우수하다”는 판단에는 자료가 부족하다. 질의 길이와 동사도 달랐고, 대상·역할을 복원한 보기에서만 두 조건을 충족한 새 대안은 없었다. [예산별 비교][prefix73] · [사후 결정 23행][d73]

모집 단위는 처음 main에 추가된 문서였다. 세 입력 중 첫 생존 PR의 원문과 일치한 것은 JEP122 하나, 창설 원고를 검증한 것은 0건이었다. SPEC9의 첫 PR은 두 조건은 같아도 당시 대안이 달랐다. JEP97의 불변 URI·버전쌍 일대일 요건은 첫 PR에 없었고 3월 14일 추가됐다. 따라서 073의 결과를 ‘원 제안자가 아직 몰랐던 해법을 최초 조건으로 발견했다’로 해석할 수 없다. 077은 이미 알려 준 타 분야 원전을 고정 수신판에서 적용하는 문제를 이어받는다. [입력판 대조][frame73] · [연구 수용][ac73]

### 074 · 한 필드가 동작을 가르는지와 지금 사용자에게 물어야 하는지는 별개다

값을 하나씩 정해 준 4대조×2값에서 단일 답 A는 정답 5·오답 1·보류 2, 조건부 답 B는 단일 정답 4·실행 가능한 조건부 답 4, 질문 C는 값이 주어진 뒤 단일 정답 8이었다. 실제로 분기한 사례는 GDAL의 최근접과 쌍선형 재표본화다. 반면 Pandoc의 두 입력 중에는 옵션이 바뀌어도 같은 AST가 나온 경우가 있었다. 무응답을 가정한 네 대조에서 B는 네 건 모두 다음 행동을 냈고 C는 한 건을 보류했다. 이 비교로 사용자가 실제로 어느 링크를 골랐는지나 질문에 들인 시간은 알 수 없다. [정책 집계][ps74] · [기술 기준][cr74]

자연 요청 8건은 두 값에 대한 독립 판별 기준이 없어 정책 정오를 비교할 분모가 0이다. 최초 글 8개를 모두 복원했지만 정책 고정 전에 확인된 것은 0/8이고, 원본과 현재판이 바이트까지 같은 경우는 6/8이다. 후속 사건 35행에서 사전에 택한 필드의 새 값은 없었다. 해결 자기보고 한 건은 연구자가 고른 필드와 다른 환경변수 변경이었다. Pandoc 고정판은 재실행했고 GDAL의 대상 3.2.1은 직접 실행하지 못해 3.10.3 보조 실험을 남겼다. **새 값이 주어졌을 때 정답 8/8**을 실제 사용자에게 물으면 성공한다는 확률로 읽어서는 안 된다. [최초판 확인 시점][initial74] · [후속 사건][events74] · [원 연구 수용][ac74]

### 075 · “이 후보가 있다”와 “다른 적격 후보가 없다”에 필요한 저장량

Pygments와 시간대 등록부에서 자연 변경 8쌍·주입 변경 8쌍을 다뤘다. 288행은 이 16쌍에 주장 세 종류, 저장안 세 개, 옛 원본 보존/소실을 적용한 반복이다. 소실 조건에서 대표 원문 A는 실제 양성 15개 모두의 존재를 복원했고, 옛 적격 후보가 없던 한 건은 보류했다. A로 유일성과 공동 1위 집합을 재계산한 결과는 각각 보류 16/16이다. 모든 판별 키와 순회 영수증을 담은 B, 원자료 전체를 둔 C는 정상 기록 아래 세 주장 각각 16/16을 복원했다. ‘적격 후보가 하나’와 ‘1위가 한 명’도 다르다. 독일 시간대 사례에는 적격 2개와 단독 1위가 함께 있었다. [점수][s75] · [판정 기준 원행][truth75]

누락 대조에서는 후보 수·대표 해시가 그대로여도 공동 1위 구성원이 바뀌었다. LOSS03에서 키와 그 키의 영수증을 함께 바꾸자 B는 유일성을 참으로 오판하고 공동 1위 한 명을 빠뜨렸다. B의 복원은 **어떤 목록을 실제로 전부 읽었다는 기록을 신뢰할 수 있을 때** 성립한다. 작은 두 등록부에서 A/B/C가 16쌍에 저장한 양은 11,147 / 248,178 / 722,011바이트였다. 공유 캐시·압축·서비스 운영비는 미측정이다. 이 결과는 전체 웹에서 가장 좋은 대상을 찾았다는 근거나 두 제품·기능의 동일성 판정이 아니다. [동점 교체][swap75] · [손실 대조][loss75] · [비용][cost75]

### 076 · 후보 회수, 제공한 절, 자연 요구의 직접 적격을 구별해야 한다

자연 6요구×20후보에는 직접 0·부분 10·타 분야 전이 2·반박 4·무관 104쌍이 있었다. 상위 3에서 URL로 시작하는 L은 부분 4/10·전이 0/2, 발행자 한 문장 S는 5/10·1/2, 용도와 동작 카드 E는 4/10·0/2였다. 교정군은 직접 적격 5쌍이 있어 세 방식 모두 5/5를 회수했다. 다섯 쌍은 네 요청에 걸쳐 있고 두 문서가 같은 구현을 가리키는 경우도 있다. 자연군의 직접 회수율은 산출 불가다. **최신 카탈로그와 당시 요청의 판 차이, 필요한 환경, 애초에 빠진 기능 중 무엇 때문인지는 아직 가르지 못했다.** [후보 판정][q76] · [순위][rank76] · [세 표][r76]

072의 빈 판독 기록은 이번에 상당 부분 보완했다. 108개 표시 자리에 기록이 있고 서로 다른 요청·후보·원문 관측 조합은 65개였다. 표시 판정은 보류 99, 반박 9, 두 조건·환경 공동 확인 0이었다. 예를 들어 자연 TIFF 변환 요청에는 발행자 설명의 ‘conversion’ 때문에 언어 메타데이터 정규화 문서가 올라왔다. 교정 요청에서 Pillow의 축소 결과 256×128→100×50을 직접 확인한 64단어 시험 절은 **사후에 골라 연 것**이다. 원 순위의 창에서 확인했다고 산입할 수 없다. 빈 캐시 36개 요청×방식에서 세 번 읽기 전후 상위 3의 집합은 같았고, 내부 순서만 21/36에서 달라졌다. 원문을 더 읽는 효과와 자료집에 적격 후보가 있는지를 분리할 이유다. [표시별 근거][s76] · [사후 대조][target76] · [재생 검사][aud76]

빈 캐시 자연 요구의 건당 전송은 L 31,565B, S 99,673.2B, E 32,762.7B였다. 교정군도 L의 평균 전송량이 가장 작았다. 이 결과와 072의 카드 이득은 모순이 아니다. 모집 자료·요청·구축비·원문 열람 규칙이 달랐고, 여기서도 자연 부분/전이 회수는 S가 앞섰다. 카드 제작 시간과 실제 요청 분포를 모르는 상태에서 ‘항상 URL만 저장’ 또는 ‘모든 링크를 상세 색인’ 중 하나를 고정할 근거는 부족하다. [비용 원장][cost76] · [전 회차 비교 조건][prev]

## 내부 설계에 남길 판단

사용자가 “프로젝트의 이 부분에서 쓸 만한 것을 찾아 달라”고 했을 때, 같은 URL을 두 요청에서 재사용해도 그 URL이 지지하는 결론은 달라질 수 있다. 이번 결과에서 도출한 저장 대안은 **자료의 정체와 위치**, **그 요청에서 지켜야 하는 조건**, **그 자료의 어느 판·절이 어떤 조건을 얼마나 뒷받침했는지**를 따로 기록해 다시 연결하는 것이다. 예컨대 예전 답이 “이 후보도 가능”이었다면 원절만 남겨 복원할 수 있었지만, “이 후보만 가능”이었다면 당시 조사 범위·판별 키·누락 가능성도 필요했다. 이를 모든 자료에 적용할 보관 규격으로 확정하려면 실제 요청 분포와 비용이 더 필요하다. [서로 다른 주장의 복원][s75] · [실제로 보인 원문 범위][s76]

073에서 얻은 외부 원리는 구현을 고르거나 실패 시험을 하나 더 만드는 데 쓰일 수 있다. 074의 조건부 답은 사용자에게 어떤 값을 물어야 선택이 달라질지 제시할 수 있다. 두 결과에서 아직 비는 관측은 **실제 개발자가 그 자료를 받고 선택을 바꾸었는가**이다. 이후 조립자는 ‘후보 링크 발견’, ‘원문에서 조건 일부 확인’, ‘목표판에서 동작 확인’, ‘원 개발자의 선택·결과 관측’에 각각 근거를 붙여 읽을 수 있어야 한다. [073의 이전판과 적용 한계][h73] · [074의 자연 후속 사건][events74]

## PLAN#19 · 각자 완결되는 네 산출물

| 작업과 담당 | 완성할 산출물 | 단 하나의 선행 인계 | 병렬 실행의 경계와 검산 |
| --- | --- | --- | --- |
| 077 · web-pro | 타 분야 원리를 어느 조작에 옮길 수 있는지, 어떤 입력에서 기각할지 적은 사례집 | [073][h73] | 공여 자료를 먼저 정한 뒤 동종 자료를 제공한 보기와 타 분야 자료를 제공한 보기에서 설계 선택·시험·기각 조건을 비교한다. 073의 발견 순위는 새 검색 성과에 산입하지 않는다. 수신 프로젝트의 고정판과 반례를 중심으로 읽는다. |
| 078 · codex-cloud | 개별적으로 유용한 두 기능의 결합이 조건을 지키는지 재생할 수 있는 호환성 표와 시험 입력 | 074 | 새 공개 도구와 입력으로 두 단계의 단독·결합 결과를 검사한다. 074의 질문 정책을 반복하지 않는다. 정상·경계·실패 시의 출력과 기대값을 독립적으로 검산한다. |
| 079 · web-pro | URL 이동·개명·분기 때 어느 기능 기록을 유지·분리·연결할지 판독한 사례 원장 | 075 | 후보 순위를 정하지 않는다. 옛 기능·새 기능을 두 프로젝트 용도에 대입하고, 주소·이름이 같은데 용도가 갈리는 경우와 반대 경우를 검사한다. |
| 080 · codex-cloud | 자연 요청의 직접 적격 분모를 판·목록 범위별로 설명하는 자료와 재계산 절차 | 076 | 검색 순위·문장 길이를 바꾸는 실험과 분리한다. 고정 후보 목록, 판을 맞춘 목록, 범위를 확장한 목록을 대조해 실제 후보 부재·입증 실패·버전 불일치를 구별한다. |

각 작업이 인수하는 다른 연구의 결과는 표에 적힌 고정판 한 건뿐이다. 네 결과는 각 작업의 전용 브랜치와 경로에 저장된다. 빈 사례를 성공으로 채울 필요는 없다. 어떤 원자료를 어디까지 확인했는지 남겨야 나중에 결과를 조립할 수 있다. 파일명·표 열·커밋 순서·완료 검사는 [배정용 JSON][next]에 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/621ece3d7f0085c7580b347c1c04312942e63497/docs/workstreams/planning/REVIEW-18.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853/docs/automation/dot-control.json
[mid]: https://github.com/laadkke-arch/agentflow-open/blob/2557797688727637fc0479a0cb369e313b80aa12/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/0d2b08431067e8d87212a66ecb27657c65722a59/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/0d2b08431067e8d87212a66ecb27657c65722a59/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/0d2b08431067e8d87212a66ecb27657c65722a59/docs/RESEARCH_WORKFLOW.md
[h73]: https://github.com/laadkke-arch/agentflow-open/blob/28dfa4d14ce33f0f98c823f83c20347d60c0e64e/docs/workstreams/research/AF-RES-073/HANDOFF.md
[r73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md
[j73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/judgments.csv
[choices73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md#L164-L178
[prefix73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md#L106-L122
[d73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/decisions.csv
[frame73]: https://github.com/laadkke-arch/agentflow-open/blob/28dfa4d14ce33f0f98c823f83c20347d60c0e64e/docs/workstreams/research/AF-RES-073/HANDOFF.md#L5-L18
[ac73]: https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/acceptance-evidence.json
[h74]: https://github.com/laadkke-arch/agentflow-open/blob/b25a389ef33094fde4982a6198fd5649076ccd66/docs/workstreams/research/AF-RES-074/HANDOFF.md
[r74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/RESULT.md
[s74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/scores.csv
[cr74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/criteria.csv
[ps74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/policy-summary.csv
[initial74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/initial-version-review.csv
[events74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/events.csv
[ac74]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/evidence/acceptance-evidence.json
[h75]: https://github.com/laadkke-arch/agentflow-open/blob/4b2a29b63f691eebb6613f20e2deb4954b41cfdb/docs/workstreams/research/AF-RES-075/HANDOFF.md
[r75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/RESULT.md
[s75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/scores.csv
[p75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/pairs.csv
[truth75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/evidence/truth.jsonl
[swap75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/evidence/swap.jsonl
[loss75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/evidence/losses.jsonl
[cost75]: https://github.com/laadkke-arch/agentflow-open/blob/8a8fe9e36e02b343740a2a8db478bc587e57f544/docs/workstreams/research/AF-RES-075/costs.csv
[h76]: https://github.com/laadkke-arch/agentflow-open/blob/81b8b2c5274d09505b4e98c12ddadde803a323cd/docs/workstreams/research/AF-RES-076/HANDOFF.md
[r76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/RESULT.md
[s76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/slots.csv
[rep76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/reproduce.md
[q76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/qrels.csv
[rank76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/ranks.csv
[target76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/evidence/targeted-windows.jsonl
[aud76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/evidence/audit.json
[cost76]: https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/costs.csv
[next]: NEXT_TASKS-19.json
