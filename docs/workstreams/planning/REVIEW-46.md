# REVIEW-46 · 원문이 증명하는 마지막 동작은 어디인가

탐색기가 개발자에게 돌려줄 것은 만들려는 부분에 쓸 수 있는 부품·서비스·다른 분야의 원리, 그 이유, 직접 확인할 원문이다. 이번 검토에서는 **값을 복사하는 호출**, **여러 행을 합친 주장**, **다른 제품으로 옮기는 파일**에서 추천 문장의 한계가 서로 달랐다. Astropy는 같은 입력으로 반환 배열을 고친 뒤 메모리 원본의 첫 값이 0에서 99로 바뀌는 것까지 관측했다. 번역 시간 합계는 정확히 되살려도 다른 분절이 섞인 오류를 놓칠 수 있었다. RSS 이관은 입력 파일과 수신기 코드까지 연결됐지만 실제로 읽음 상태가 남았는지는 아직 확인할 수 없다. [제품 브리프][product] · [배열 전후 값][205raw] · [집계의 통제][207raw] · [이관 필드][215fields]

45차 마감 뒤 **46차 요청 시점까지** 중앙에서 새로 DONE이 된 작업은 **AF-RES-205~215, 11건**이다. 자체 완료는 205·207 두 건이고, 나머지 아홉 건은 PARTIAL이다. 46차에는 독립적으로 시작할 웹 조사·설계 8건과 즉시 실행할 Codex 검사 2건을 배정안에 넣었다. 별도 Codex 검사 1건은 216의 원영수증에 의존한다. 집필 중 216~218도 중앙 DONE이 되어 세 인계와 결과를 추기에 반영했다. 216의 필수 파일 세 개가 확인돼 이 검사까지 착수할 수 있다. 최종 검토 범위는 새 완료 **14건(자체 DONE 5, PARTIAL 9)**이다. [진행표][ctl] · [작업자에게 전달할 11개 지시문](NEXT_TASKS-46.json)

## 이번 검토에 들어온 증거

먼저 계획 브랜치 `7bb2f9e`에서 가장 최근 파일인 REVIEW-45를 읽었다. 그 문서의 **결과 검토 마감**은 `bb14677`이다. 45차 작성 중 205~207이 중앙 완료됐다는 추기가 있지만 그 결과는 이번 차수로 이월됐다. 두 통합판의 작업 행을 ID와 전체 필드로 대조했다. 기존 205행 가운데 205~207 세 행에서만 상태·결과 SHA·최근 진행 시각이 바뀌었다. 새 행은 208~218이고 삭제는 없다. [직전 누적 검토][prev] · [직전 진행표][old] · [이번 진행표][ctl] · [두 통합판의 차이][delta]

| 검토 마감(UTC) | 전체 행 | DONE | RUNNING | BLOCKED | 결과를 읽은 범위 |
| --- | ---: | ---: | ---: | ---: | --- |
| 45차 · 2026-11-24 21:01:21 · bb14677 | 205 | 198 | 3 | 4 | 195~204까지 |
| 46차 요청 · 2026-11-24 21:40:33 · fc095c3 | 216 | 209 | 3 | 4 | 기존 205~207, 새 행 208~215 |
| 46차 결과 검토 최종 · 2026-11-24 22:00:55 · 2a32cb8 | 216 | 212 | 0 | 4 | 마감 후 확정된 216~218도 추기에 반영 |

요청 시점의 209개 중앙 DONE은 연구 207건과 연결 시험 2건이다. 209행 모두 `acceptance_evidence`가 빈 배열이다. 차단 네 건도 전회와 같다. 018은 인계 전 대화 한도, 035는 실행 세션 종료 뒤 인계 미확인, 149는 세 유입 경로가 모두 들어간 동일 주간 분모 미확보, 151은 최초 N0 응답·독립 가림·원사용자 비용 근거 미확인이다. 이 네 건을 이번 신규 완료 분모에 넣지 않았다. [중앙 기록][ctl] · [연구·인계 규칙][workflow]

| AF-RES · 주제 | 작업자 판정 | 배정 브랜치의 인계 SHA | 인계가 지목한 결과 SHA | 원장 행 / 산입 저작 | 판단 단위 |
| --- | --- | --- | --- | ---: | --- |
| 205 · 복사 정책 | DONE | [3853289][h205] | [2786b85][r205] | 41 / 28 | 32셀 중 28셀 실행, 4셀 설치 충돌 |
| 206 · 좌표 원전 | PARTIAL | [94e2c0e][h206] | [7292580][r206] | 55 / 25 | 주점 6자리·4고유점, 별도 충돌점 2 |
| 207 · 집계 보존 | DONE | [ded4731][h207] | [7021737][r207] | 39 / 30 | 실재 문장 6×저장안 2, 통제 4×2 |
| 208 · 반복 일정 | PARTIAL | [4b700b6][h208] | [1593548][r208] | 43 / 30 | 사건 4, 별도 설계 통제 4 |
| 209 · JPEG 검색 | PARTIAL | [187cb91][h209] | [7f67916][r209] | 37 / 33 | 요청 4쌍·개별 검색 8·노출 위치 24 |
| 210 · diff 원리 | PARTIAL | [097948b][h210] | [9c1c8fa][r210] | 34 / 27 | 실제 입력쌍 4, 합성 4, 예측 32행 |
| 211 · 기능 문서 | PARTIAL | [873621f][h211] | [456f63a][r211] | 59 / 38 | 제품 2×목적 3×문서 경로 3 |
| 212 · 링크 이름 | PARTIAL | [98cd710][h212] | [f4b08aa][r212] | 47 / 35 | 정규 12자리, 채택 6·결측 6, 별도 보강 4 |
| 213 · 인용 스타일 | PARTIAL | [425835c][h213] | [b7389f0][r213] | 64 / 39 | 원파일 7, 목적 자리 12×소비자 2 |
| 214 · 표준 기능 채택 | PARTIAL | [81cb775][h214] | [05dcea5][r214] | 60 / 33 | 런타임 제거 패치 4, 문서·타입 대조 2 |
| 215 · RSS 이관 | PARTIAL | [58102fd][h215] | [041af93][r215] | 47 / 38 | 송신 방식 2×필드 6, 별도 사건 4 |

11건 모두 중앙 `result_commit`이 배정 브랜치 끝과 일치했다. 각 SHA의 소유 경로에서 인계와 결과·자체점검을 읽고, 인계가 가리킨 직전 결과 SHA의 RESULT blob도 같은지 확인했다. 해당 경로의 최상위 파일 123개의 Git blob 지문을 확인했다. 출처 원장 526행의 JSON·작업 내 source_id 고유성, CSV 43개의 자료행 1,027개와 열 너비를 검사했다. 작업별 산입 저작을 더하면 356건이다. 같은 저작·사건이 여러 작업에서 쓰일 수 있으므로 전체 독립 사건 수로 해석할 수 없다. 아래의 실행 수는 해당 작업자의 커밋된 원영수증을 읽은 값이다. 이 검토에서는 205의 전후 값, 206의 전송 실패, 207의 통제 등 대표 원영수증과 표의 일치를 확인했다. 독립 재실험이나 과거 이용자의 행동 관측은 미실시다. [205 원로그][205raw] · [206 원로그][206raw] · [207 원로그][207raw] · [209 노출표][209paths] · [212 이름표][212names]

## 45차까지 누적한 제품 판단과 이번 변화

| 개발자가 내릴 결정 | 이전까지 실제로 갈린 경우 | 46차에 이어지는 판단 |
| --- | --- | --- |
| 전체 설계 없이 어느 정보를 묻나 | 020은 전달 주장 72/73을 따라갔지만 모든 충돌이 풀린 묶음은 2/16이었다. 107은 편집할 개별 발생 위치로 6/6, 공유 정의만으로 0/6이었다. 159의 소비자 역할은 48/48을 갈랐고, 189의 화면 문자열/재검색 방지, 197의 현재 면/방문 면은 다른 요구였다. | 208은 화면에 보이는 시각과 원래 회차를, 215는 구독과 글 상태를 갈랐다. 서로 다른 사용자 답이 다른 원문 절을 필요로 할 때 한 질문을 제안할 수 있다. |
| 다른 분야 원리를 왜 붙이나 | 010의 원분야 단서로 7군을 찾았으나 033의 무힌트 144쌍은 당시판 지지 0, 145의 독립 초안은 0/16이었다. 166·174·183은 경쟁 예측을 만들었고, 183의 동일 입력·SHA 공개 실행은 0/16이었다. 191은 색 지각 연구와 CSS 편집 결정, 199는 두 HDR 원전과 다른 조작을 연결했다. | 210의 LIS 원리는 가능한 앵커의 길이를 좁힌다. 동률 해소·후퇴·최종 표시에는 구현을 읽어야 했다. 설명력, 힌트 없는 발견, 추가 적중, 사용자 선호는 별도로 검증한다. |
| 한 링크, 택일, 필수 조합 중 무엇을 주나 | 040의 완전 적격은 0/8, 044의 고정 풀에서 두 묶음 방식은 동률이었다. 114의 충돌 138건은 118에서 명시 7·미확인 131로 갈렸다. 146의 48후보는 직접 충족 0·부분 15·충돌 14·미확인 19였다. 193의 메일 큐와 사서함, 202의 모델과 모드, 204의 엔진과 운영자는 서로 다른 마지막 조건을 가졌다. | 213은 저널 이름·편집할 부모·로캘을, 215는 구독 목록·항목 파일·수신기 처리를 구분했다. 같은 주장을 지지하는 보조문서, 교체 가능한 방법, 반드시 함께 쓰는 부품은 원문 역할에 맞게 보여준다. |
| 당시 답과 지금 쓸 대상을 어떻게 보관하나 | 055는 옛 답 4/4·다음 판 0/4, 147은 과거 답 112/112를 복원했다. 150의 동일성과 근거 동시 일치는 보관안별 7·9·15/16이었다. 161은 병합 취소 뒤 하류 기록을 따로 복구했고, 190의 여덟 위치는 유일해졌으나 독립 재탐색은 0/24였다. 192·201은 인용 대상과 배포판·그림 생성 근거를 갈랐다. | 196의 표시 문장은 A/B/C 모두 4/4 복원했다. 사본 없이 인용 바이트·지문을 확인한 것은 C 4/4였다. 207은 연속된 합계 두 개에서 간단한 표현도 통과했으나 같은 총합의 행 교체에는 추가 선택 기준이 필요함을 보였다. |
| 새 발견과 기존 추천의 갱신 비용을 어떻게 보나 | 024의 무효화 11건은 주기 방식 11, 신호 방식 8이었다. 신호 방식은 열람 108회가 적고 전송량은 5,672,462바이트 많았다. 152의 새 자료 15건은 신호/희소 공급원 방식 14, 주기 방식 13이었다. 162·170에서 공지와 실제 사용 시점이 달랐고 200의 현 배너는 당시 파일별 경고를 복원하지 못했다. | 211의 stable 문서, 숫자판 문서, 고정 소스는 목적에 따라 다른 답을 준다. 현재 응답·현행 본문·당시 도착 절을 구분한다. 216의 파일별 원값은 이 마감에서 아직 결과가 없다. |
| 당사자가 발견하고 실제로 선택을 바꿨나 | 022의 미인지→선택 변경→실행은 0/24, 158의 제출 28건은 수신 입증이 아니었다. 163의 발신 35건에 원제출자 재개 보강 1건, 180의 자연 8건은 지정 창 내 원제보자 텍스트 후속 0이었다. 194의 PEP 4건과 203의 자연 6건·보강 2건에서 완전 사슬은 관측되지 않았다. | 214에는 실제 제거 diff와 지원 환경 변화가 있다. 새 링크로 의사결정이 바뀐 인과와 제품 배포는 별도 근거가 필요하다. 무회신은 행동 부재나 효용 0으로 환산하지 않는다. |
| 재사용이 재작업·사람 노동을 얼마나 줄였나 | 034에서 한 단계는 380→57초, 전체는 849→847초였다. 160의 1,061.9인시와 추정 비교값, 164의 공유 직접작성 집단은 별도였다. 172는 전원·동일 기능·시간·독립 검수를 모두 연결한 비교가 0이었다. 181의 번역 배정 1/24를 195가 24/24로 복원했으나 96조건 분절의 독립 검수 키·시간은 0/96이었다. | 207도 두 총노동 문장을 정당하게 보류했다. 번역자 사건창, 검수자 작업시간, 최종 인수 기준을 같은 산출물에 연결하기 전에는 단계별 측정만 제시한다. |
| 설치·표시·시험 합격에서 어느 동작까지 말할 수 있나 | 154의 명시 원본 회수 10/10과 기본 다운로드 동일 바이트 6/10은 달랐다. 176의 합격 표시 55/55는 한 보고서의 재표시였다. 186은 열 입력에서 두 엔진의 판정 9/10 일치, 187의 실제 wheel, 188의 기관 원점·점별 공차, 198의 경계 재인코딩, 202의 모델 모드 로드는 별도 미결이었다. | 205가 지정 wheel 4개와 가변 원본을 연결했다. 206은 재게시 간 방향을 판별했고 기관 ZIP은 여전히 비었다. 212의 예상 이름, 213의 오프라인 로드, 215의 실제 DB 상태는 실행·당사자 자료가 각각 필요한 지점이다. |

이 수치의 이전 출전과 정정 이력은 직전 누적 검토로 추적할 수 있다. 링크와 요약, 필요한 경우의 추가 구조, 요청 시 확인과 주기 갱신, AI 전처리, AgentFlow 입력 형식과 최종 검색·저장 구성은 여전히 비교할 설계안이다. [45차 누적표와 이전 원출전][prev] · [제품이 열어 둔 질문][product]

## 신규 결과에서 확인한 것과 부족한 근거

**205 · 반환값이 같아도 원본을 고칠 수 있는지는 호출과 입력에 달렸다.** Datasets 2.20/2.21과 Astropy 6.0.1/6.1의 wheel 4개는 게시 지문과 일치했다. 설치 가능한 28셀의 두 옵션·두 반복 112회에서 반환 94, 호출 예외 18이었고 나머지 4셀은 선언된 의존성 충돌로 실행 전 종료했다. A04-A1에서 `copy=False`는 실제로 첫 원소 0→99를 원본에 전파했고 기본 호출에서는 반환값만 바뀌었다. A04-A2의 읽기 전용 버퍼는 공유됐지만 원본은 바뀌지 않았다. 같은 값·같은 버퍼·쓰기 가능 여부를 각각 안내할 수 있다. 제보자와 같은 환경에서 해결됐는지, 다른 ABI에서도 같은지, 파일을 닫은 뒤 값이 남는지는 이 관측의 범위를 벗어난다. [행렬][205matrix] · [A04 전후 원값][205raw] · [조건별 안내][205advice]

**206 · 밀리미터 차이에 방향이 맞는 사본이 있었지만 기관 원파일의 공차는 비어 있다.** 두 재게시의 정방향 출력은 줄바꿈 제외 40/40행 일치했고 188에서 인용한 6자리·4점은 원래 숫자 토큰까지 재현됐다. X05의 격자표는 다른 사본의 역방향 입력과 40/40행 일치한다. TP31에서 X05와 정방향 출력의 차이는 동 −0.003m·북 +0.004m·높이 −0.001m였다. 발행기관 full ZIP은 작업 환경의 프록시에서 막혀 원 발행 서버 응답과 멤버 바이트를 받지 못했다. 기관 원행은 주점 0/6자리와 충돌점 0/2, 주점별 공차 0/6이다. 상이한 시험 역할이 수치 차이를 설명하는 근거는 생겼지만, 재게시본을 기관 정답이나 통과 공차로 인용하기에는 부족하다. [지점 원표][206points] · [축·방향별 차이][206deltas] · [다운로드 실패 위치][206raw]

**207 · 같은 합계가 다른 분절에서 나왔을 때 단건 인용 방식은 두 통제를 통과시켰다.** 여섯 실재 문장의 12셀에서 두 안 모두 단일행 2개와 연속 합계 2개에 정답, 총노동 주장 2개에 보류였다. 행 교체 통제는 648,615ms·111단어·5분절·1인까지 같았다. 기존 표현 A는 이 교체와 같은 참여자 관측의 복제를 승인했고, 행 선택·그룹·단위·산식·결측 규칙을 추가한 B는 둘 다 보류했다. 단위 오기와 누락을 0으로 채운 사례는 양쪽이 모두 보류했다. B의 여섯 기록 추가 비용은 2,335바이트다. 실재 합계 둘은 한 문서의 연속 구간, 네 통제의 씨앗은 한 합계, 권위 코호트와 추출 행은 같은 계보다. 다른 산출물의 비연속 집계, 코호트 자체가 함께 틀린 상황, 검수 포함 노동은 미확인이다. [주표본과 통제][207matrix] · [통제 원출력][207raw] · [기록별 비용][207cost]

**208 · ‘이번부터’가 가리키는 원래 회차와 이동 후 시간이 달랐다.** Nextcloud #8957의 작성자는 새 시작일을 바꿔도 BYDAY가 옛 요일이어서 읽어본 일정이 어긋났다고 기록했고, 요일 규칙 수정 후 날짜도 적었다. #8450에서는 이미 옮긴 예외의 참석자와 주최자 화면이 달랐다는 보고가 있다. #4862의 첫 글에서는 알림 변경 범위부터 모호했다. 네 사건 모두 원작성자의 원 UID·회차 키와 수신자 payload를 함께 읽은 사례는 0/4다. 이동·취소·요일·서머타임 통제 넷은 예상 결과다. 당시 문서의 두 요청 분할 예도 현행 안내에서 직접 확인하지 못했다. 어느 규칙을 먼저 읽을지는 제시할 수 있지만 실제 초대·알림 보존은 미확인이다. [네 사건][208events] · [방법과 통제][208methods] · [질문·첫 절][208routes]

**209 · 기술 단서를 더한 검색이 첫 링크를 밀어낸 사례가 있었다.** 여덟 질의를 개별 호출해 응답 위치 24개와 첫 링크 열람 8개를 기록했다. 경계 4픽셀을 보존하려는 #847에서 A의 첫 결과는 판별에 필요한 원 이슈였고, iMCU를 넣은 B는 다른 프로젝트 사용법으로 이동했다. #265는 양쪽 모두 원 이슈였다. 도구 순서 기준 개선 0·악화 1·동률 1·판정불가 2쌍이다. 원질문이 1등인 것을 새 해결책 발견으로 계산하면 이득을 부풀린다. 제공자 원순위와 검색별 정확 UTC는 각각 0/8, 표시 문구는 의역, 후속 링크 열람은 0/5회 성공이었다. 실제 검색 UI 순위나 단서 일반 효과는 미확인이다. [질의 동결표][209queries] · [노출·도착 URL][209paths] · [쌍별 판정][209matches]

**210 · 정렬 원리는 가능한 공통 줄의 길이를 제한했고 실제 동률 해소는 구현 문제로 남았다.** R2에서 루트의 후보 8개 중 순서를 지킬 수 있는 길이는 7이다. 공개 Git 시험에는 patience와 histogram의 최종 기대가 같은 경우가 있다. 유일한 줄이 없는 C1의 후퇴, 두 계열 길이가 같은 C2의 기준 줄은 Git과 Breezy 소스에서 서로 다른 예측이 나온다. 4개 실제 입력과 4개 통제의 32행은 단계별 예측이며 동일 입력의 실행 stdout과 내부 선택 로그는 0이다. 본래 문서 단계에서 기대와 구현을 이미 보아 일부 예측은 사후 재구성했다. 사후 보강 두 원파일을 빼면 지정 시험 계열도 4/6이다. 원리가 정답률이나 가독성을 개선했다는 결론은 미확인이다. [입력·기대의 종류][210pairs] · [선노출 표시][210pred] · [원리 대응][210map]

**211 · 코드가 특정 인수를 받는다는 근거와 그 문단으로 갈 수 있다는 근거는 따로 있다.** 고정판 소스에서 urllib3 1.26.18의 `method_whitelist`와 Pillow 9.5.0의 `Image.ANTIALIAS`는 지원 후 폐기 예정이었고, 각각 2.0.0과 10.0.0에서 제거됐다. 새 이름도 더 오래된 urllib3 1.25.8에는 곧바로 소급할 수 없다. 18경로 중 15개는 본문 또는 고정 파일을 읽었고 Pillow 숫자판 3자리는 실패했다. 렌더링 경로의 실제 HTTP·HTML fragment 확인은 0/12, 역사 목적의 당시 도착지는 0/6이다. DNS 실패에서 404를 추정할 수 없다. 옛 사용자의 호출을 설명하는 고정 소스는 남길 수 있고, 당시 링크가 실제로 연 절은 미확인이다. [판별 호출][211vers] · [18개 목적지][211dest] · [소비자 인용][211cit]

**212 · 디자인 시스템의 예시는 실제로 다른 곳을 여는 링크 쌍의 절반만 제공했다.** 미국 USWDS의 정규 세 예시에서 여섯 앵커를 채웠으나 같은 목적지 두 개가 반복됐다. ‘dashboard’가 가리킨 곳은 대시보드를 소개하는 기사였다. 영국 GOV.UK의 정규 여섯 자리는 `#` 등으로 결측이었고 보강 네 자리는 따로 남았다. 계산한 이름과 설명은 있지만 두 보조기기의 실제 목록 출력은 미측정이다. 채택 링크에서 같은 접근 가능한 이름으로 서로 다른 실제 목적지를 가리키는 쌍도 확보하지 못했다. 숨긴 접미사가 이름을 구별한다는 설계 가설과 실제 사용자의 선택 성공은 별도다. [예시 16행][212examples] · [예상·관측 구분][212names] · [문구 대안][212cards]

**213 · 같은 부모를 가리키는 저널명 두 개가 편집·오프라인 사용에 같은 링크를 요구하지는 않았다.** 고정 XML에서 Nature Biotechnology와 Nature Nanotechnology 별칭은 둘 다 en-GB와 같은 부모를 가리키고 자체 macro/layout은 없었다. 부모 Nature에는 매크로 8개·레이아웃 2개가 있다. Zotero의 번들·숨긴 부모 조회와 Pandoc의 로컬 동명 파일 우선 경로는 고정 소스에서 읽었다. 12자리×2소비자의 24개 판정은 전부 조건부 정적 판정이다. 실제 렌더·캐시 적중·오프라인 성공은 관측되지 않았다. Nature Communications에서 제보→병합→회신이 있었지만 정확 대상 두 저널의 제보는 0/2이고 편집자 승인은 미확인이다. [원파일과 부모][213objects] · [24개 판정][213res] · [다른 저널의 사건][213req]

**214 · 네 제거 패치에서 확인되는 것은 지원 환경을 이유로 제시했다는 사실이다.** DIM은 8.19.0의 지원 하한과 8.19.1의 제거를 연결할 수 있었다. 네 사건에서 태그는 3/4, 레지스트리 게시 기록은 1/4, 최종 소비자 운영 배포는 0/4였다. Blacklight 사례에서는 API에 보이는 base가 최초 제안일보다 늦어 당시 작성자가 알던 코드를 확정할 수 없다. 네 런타임 제거에서 최초 외부 링크→사전 미인지→같은 사람의 선택 변경·실행 사슬도 0/4다. 문서 누락을 새로 안 사례와 타입 선언 제거는 각각 다른 행동이다. 라이브러리가 실제로 줄었다는 사실만으로 탐색기가 뒤늦은 재작업을 줄였다고 말할 수 없다. [변경 이력][214changes] · [행동과 경쟁 설명][214dec] · [판별 지원 정책][214support]

**215 · 별표 파일에서 읽음 값이 빠졌다는 사실과 수신기에서 ‘읽지 않음’이 됐다는 말은 다르다.** 별도 소비자 프로젝트가 공개한 비식별 Inoreader 유래 예제 둘의 5개 항목 모두 별표가 명시돼 있고 읽음은 3개만 명시, 2개는 부재다. 그중 둘째 파일은 형상 예제다. FreshRSS 1.29.1의 고정 소스는 누락 read를 수신 설정에서 채우는 경로를 보여준다. OPML의 피드 URL·폴더, 항목 JSON의 ID·별표·태그는 다른 경로다. 네 고정 이관 사례는 Thunderbird·TT-RSS·FreshRSS 백업·송신기 미상 OPML이었다. 지정한 Inoreader→FreshRSS 동일인 사건은 0/4, 방식×필드의 실측은 0/12다. 별도 수신기인 Obsidian의 긍정 회신은 FreshRSS 결과에 산입할 수 없다. [두 입력의 출처와 한계][215src] · [필드 대조][215fields] · [네 이관 사건][215mig]

## 서로 어긋나 보인 결론과 권고가 바뀌는 조건

| 두 결과 | 관측 단위를 맞춘 판단 | 제품 답을 바꿀 추가 증거 |
| --- | --- | --- |
| 196의 간단한 설명은 표시 문장에 충분했고 207의 A는 잘못된 행을 승인했다. | 같은 문장 재표시, 외부 사본 없이 원문 재열람, 집계 대상의 동일성은 서로 다른 작업이다. 207의 실재 연속 합계 둘에서는 A/B가 동률이었다. | 한 문장을 다시 표시하는 사람에게는 짧은 안이 가능하다. 여러 지역·기간을 묶은 수치를 요청하면 어떤 행·분모를 골랐는지, 외부 정답까지 같은 계보인지 확인한다. [45차의 196 대조][prev] · [207의 비용과 분모][207matrix] |
| 205에서 쓰기 전파가 성공했는데 215에서는 수신 상태를 단정할 수 없다. 208에서는 원작성자의 수신자 보고까지 있다. | 205에는 같은 프로세스 원본의 전후 값이 있다. 215에는 송신 예제와 파서, 208에는 당사자 진술이 있다. 셋의 마지막 관측 위치가 다르다. | 파일을 닫고 다시 연 값은 218, 읽음/별표를 실제 기록한 DB 값은 228이 담당한다. 작성자 발언을 인용할 때는 발언 출처와 실제 payload 확보 여부를 붙인다. [205 실제 값][205raw] · [208 사건][208events] · [215 필드][215fields] |
| 209에서 더 구체적인 검색어가 손해였고 210에서는 원리가 후보를 좁혔다. | 원 이슈를 재발견한 순서, 원리로 설명 가능한 앵커, 경쟁 구현에서 맞는 앵커, 독자의 편의는 같은 성공 지표가 아니다. | 220은 제공자 순서에서 자기 질문을 제외한 첫 답을 본다. 221은 원전이 예측을 좁히는 입력을, 227은 실제 앵커와 hunk를 본다. [첫 링크][209paths] · [예측 노출][210pred] |
| 206의 40/40 일치는 기관 자료처럼 보이고 211의 성공한 문서 빌드는 링크 접근이 되는 것처럼 보인다. | 재게시의 역입력과 순기대는 다른 객체다. 빌드 성공도 사용자가 누른 시점·URL·fragment까지 증명하지 않는다. | 기관 원ZIP의 멤버·판·공차를 확보하거나, 해당 문서를 당시판 URL/응답과 실제 절까지 이어야 원출처·역사 목적을 표시한다. [206 지점][206points] · [211 목적지][211dest] |
| 212에서는 같은 문구로 다른 자료를 여는 예가 부족했고 213에서는 다른 저널명이 같은 부모를 가리켰다. | 사용자에게 보인 이름, 템플릿이 선택한 목적지, 수정할 실체는 각각 별도다. 읽기·편집·재현의 목적이 같을 때만 링크를 합칠 수 있다. | 222의 정정 이름/정식 이름과 223의 실제 편집 라우트를 보면 어떤 이름을 함께 저장하고 어떤 링크를 나눠야 할지 결정할 수 있다. [212 링크 목적][212examples] · [213 파일 역할][213objects] |
| 214에는 같은 작성자가 실제 패치를 냈는데 발견 효과는 여전히 미확인이다. | 외부 링크를 받기 전부터 네이티브 동작을 사용했거나 지원 하한이 바뀌어 fallback만 지울 수 있다. 알려 준 사람과 변경 시점·최초 코드가 필요하다. | 225는 리뷰 의견 직전 코드, 제시된 도우미, 같은 작성자의 다음 diff를 연결한다. 사전 미인지가 빠지면 ‘제안 뒤 사용’까지만 적는다. [214의 네 설명][214dec] |

## 46차 배정과 착수 조건

각 웹 작업은 독립된 표본·질문·판정값을 가진다. 확정 선행은 중앙 인계 SHA로 고정했고, 각 지시문 자체에 원자료 입구와 세부 질문 7개, 직접 열람할 유형별 하한, 필수 표의 열, 반례, 파일, 중간 커밋과 마지막 인계 점검을 넣었다. 자료 수를 채워도 핵심 관측을 못 했을 때에는 PARTIAL로 남긴다. [전체 배정 JSON](NEXT_TASKS-46.json)

| AF-RES · 담당 | 선행 / 착수 | 조사 대상과 판별 목표 | 반환할 결정 |
| --- | --- | --- | --- |
| 219 · web-pro | 208 / 즉시 | Discourse Meta 네 글의 개인/관리자, 주제/전체, 화면/메일 중 유지할 것 | 즉답이 가능한 조건과 하나만 되물을 질문 |
| 220 · web-pro | 209 / 즉시 | DuckDB CSV 형 추론 원이슈 네 개, 제공자 검색 응답 여덟 개, 자기·중복 질문 제외 첫 답 | 사용자 단어에 보존 단서 하나를 더할지 |
| 221 · web-pro | 210 / 즉시 | 모호한 등고선 셀의 원논문과 두 구현, 실재 입력 2·수치 통제 5 | 구현 사용법만 줄지, 연속장 판별 원리까지 줄지 |
| 222 · web-pro | 211·213 / 즉시 | Unicode 정정 이름 4와 대조 2, 2소비자×3조회 방향 | 옛 인용·새 별칭 검색·정식 이름 표시의 최소 기록 |
| 223 · web-pro | 212 / 즉시 | 영국 교육 서비스 두 곳, 6화면·12앵커의 이름과 실제 편집 필드 | 링크 이름에 어느 필드와 동작을 남길지 |
| 224 · web-pro | 206·207 / 즉시 | ACS 네 카운티·두 결합률, 잘못된 네 합산×세 보관안 | 복합 지역 추천에 남길 변수 역할·분모·지리·판 |
| 225 · web-pro | 214 / 즉시 | pandas 동료 리뷰에서 기존 검사용 도우미 제시와 댓글 직후 패치 | 대안의 존재·실제 사용·발견 인과 중 입증한 문구 |
| 226 · web-pro | 207 / 즉시 | DG21/오류 주석 12자리와 별도 산업 연구의 제작/검수 집계 | 재사용이 줄인 노동을 어느 역할까지 수치화할지 |
| 227 · codex-cloud | 210 / 즉시 | Git·Breezy의 여덟 입력, 네 정책/방법×두 번=64회 | 원리가 예측한 중간 선택이 실제 diff에 남는지 |
| 228 · codex-cloud | 215 / 즉시 | 비식별 파일 둘·수신 설정 둘·초회/재수입, 5항목의 20자리 | 읽음 누락·별표·재가져오기 결과를 어떤 조건으로 권할지 |
| 229 · codex-cloud | **216 / 요청 시 보류 → 추기에서 착수 가능** | 검증된 pytest 세 wheel을 소비하는 pip의 정확 지정/범위 선택·경고 | 그대로 재현할 때와 새로 고를 때 어떤 경고를 줄지 |

조사 입구도 작업마다 다르다. 예를 들어 220은 순위가 있는 GitHub 이슈 검색의 공개 JSON 응답, 221은 실제 면의 모호성을 다룬 논문과 제작자 문서, 224는 인구조사국의 공표 변수와 계산 사례, 226은 CRITT의 연구 목록에서 출발한다. 이 링크들은 작업자가 검증할 표본의 입구다. 실제 성립 여부는 아직 이 배정안의 결과가 아니다. [검색 제공자 규약](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests) · [등치면 원논문](https://graphics.stanford.edu/courses/cs164-10-spring/Handouts/paper_p83-nielson.pdf) · [ContourPy 설명](https://contourpy.readthedocs.io/en/stable/description.html) · [ACS 변수 사전](https://api.census.gov/data/2023/acs/acs5/groups/B23025.html) · [ACS 기관 실례](https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_researchers_handbook_2020_ch05.pdf) · [CRITT 공개 연구](https://sites.google.com/site/centretranslationinnovation/tpr-db/public-studies)

### 요청 시점에 진행 중인 216~218

| 기존 Codex 작업 | 이미 배정된 대상·판별 목표 | 46차의 의존 경계 |
| --- | --- | --- |
| 216 · RUNNING, 결과 SHA 없음 | matplotlib·pytest 여섯 판, 두 종류 API의 현존 88파일별 철회 플래그·사유·파일 목록. 삭제 집단은 별도다. | 즉시 웹 작업은 파일 철회와 pip 선택을 다루지 않는다. **229만** 216의 중앙 DONE, 고정 SHA의 인계, pytest 세 판 wheel 이름·해시·원응답 플래그/사유·시각이 서로 연결된 뒤 착수한다. 이 조건이 비면 계속 보류한다. |
| 217 · RUNNING, 결과 SHA 없음 | Tesseract 5.3.0, 정확 언어 파일 6개·OEM 0/1 12자리의 내부 구성·실제 열린 경로·초기화. | 이번 신규 작업에는 해당 파일·모드가 없다. 초기화된 바로 그 조합에 의존하는 인식 성능 비교는 217의 성공 셀·빌드·입력 지문이 생긴 뒤에야 정의할 수 있다. |
| 218 · RUNNING, 결과 SHA 없음 | 205의 양성인 Astropy 호출을 받아 FITS 열기 모드·접근 경로·저장 경계 뒤 새 reader의 동일 픽셀을 검사. | 205의 첫 적격 A01-A1.false에 원본 전파가 있어 218의 착수 근거가 충족됐다. 중앙 행에 남은 옛 block_reason은 205 미완료였던 계획 시점의 기록이다. 재열기 이후 파일 상태를 근거로 하는 후속은 218의 모드별 전후 파일·픽셀 영수증에 의존한다. |

요청 시점의 진행 상태와 결과 SHA를 기준으로 배정했다. 계획 브랜치에는 제안 두 파일을 둔다. 실제 작업 배정과 중앙 상태 변경은 별도 진행 절차를 따른다. [요청 시점 진행표][ctl] · [216~218의 기존 지시문][tasks45] · [205 양성 원영수증][205raw]

### 마감 후 확정된 세 인계와 229의 착수 판정

2026-11-24 22:00:55 UTC 통합판 `2a32cb8`에서 216~218 세 행 모두 DONE으로 바뀌었다. 세 배정 브랜치 끝과 중앙 SHA를 맞춘 뒤, 각 소유 경로의 인계·결과·자체점검·원장을 읽고 대표 CSV의 행을 다시 셌다. 세 작업 모두 자체 DONE이다. 위 웹 여덟 건의 자료와 판정 기준은 요청 시점에 고정한 그대로다. **다음 누적 검토의 결과 마감 기준은 이 통합판**이다. [마감 후 진행표][afterctl]

| AF-RES | 인계 / 결과 | 실제로 확인한 것 | 아직 주장할 수 없는 것 |
| --- | --- | --- | --- |
| 216 · PyPI | [9a306b7][h216] / [e2b7670][r216] | 기존 88파일 전부가 파일명·SHA256으로 두 API와 연결됐다. 철회 대상 26개는 같은 사유, 인접판 62개는 양쪽 모두 명시 false였다. 별도 삭제 집단에서 유지자가 보고한 Windows wheel 5개의 이름·해시도 복구했다. | 두 API와 현재 HTML은 같은 발행 계보다. 개별 파일의 최초 경고·삭제 시각, 당시 전파, 소비자 설치 성공은 별도다. [파일 원표][216files] · [삭제 집단][216deleted] |
| 217 · OCR | [822f1c0][h217] / [89af301][r217] | 6파일 구성·실제로 열린 경로 확인. 지정한 Debian Tesseract 5.3.0-2 빌드의 12모드 자리×2회에서 14회 Init 0/exit 0, 10회 Init −1/exit 1이었다. OEM1은 여섯 파일 모두, OEM0은 tessdata 영어만 성공했다. 202의 예측 7/5와 일치한다. | 지정 파일을 읽고 초기화한 조건까지다. 다른 빌드·제보자 환경·인식 정확도는 미확인이다. [실행표][217runs] · [구성표][217comp] |
| 218 · FITS | [ee90bf6][h218] / [9403bd6][r218] | 205의 실제 A01-A1.false를 이은 무스케일 PrimaryHDU에서 24/24회 메모리 0→99. 종료 후 새 reader가 같은 원경로에서 읽은 값은 update 8회에서 99, readonly·copyonwrite 16회에서 0이었다. 헤더만 바뀐 대조와 새 경로로 쓰는 경우도 따로 있다. | 이 Astropy 6.0.1/NumPy 1.26.4 환경에서의 가시성이다. 전원 상실·경쟁 쓰기·압축 또는 스케일된 영상의 지속성은 미검사다. [픽셀 전후 원표][218pixels] · [반례][218controls] |

**229의 선행은 충족됐다.** 216의 보관된 V04·V05·V06 버전 응답, I02 Simple 응답, HTTP 수신 시각, 결합표를 대조했다. pytest 8.0.2·8.1.0·8.1.1 wheel 세 개의 SHA256이 두 API와 결합표에서 모두 일치했다. 8.1.0의 버전 응답은 true와 #12069 사유를, Simple 응답은 동일한 사유 문자열을 갖는다. 양옆은 false다. 따라서 최종 JSON은 229를 `depends_on: ["AF-RES-216"]`인 `READY_NOT_STARTED`로 두고 고정 인계와 세 지문을 brief에 넣었다. pip를 실행해 경고나 선택을 관측하는 것이 229의 새 작업이다. [두 API의 원응답·수신 시각][216http] · [결합표][216files] · [최종 배정 JSON](NEXT_TASKS-46.json)

## 다음 결정을 바꿀 중요한 약점 세 건

| 약점 | 지금 잘못 안내할 수 있는 것 | 다음 확인과 판단 전환 조건 |
| --- | --- | --- |
| 원본 노출·같은 사람의 행동을 복구하지 못한 연구가 많다. | 209의 원질문 재발견을 새 발견으로, 210의 사후 예측을 독립 적중으로, 214의 제거 패치를 링크가 일으킨 선택으로 셀 수 있다. | 220에서 원순서와 자기 제외 후 첫 절, 221에서 단계별 예측 봉인, 225에서 최초 의견과 같은 사람의 다음 diff를 확인한다. 연결이 빠진 사건의 인과와 독립 효과는 미확인으로 둔다. |
| 발행·설명·수신 사이에 빠진 경계가 있다. | 206의 사본을 기관 기준값으로, 211의 빌드를 당시 fragment 성공으로, 212의 예상 이름을 실제 사용으로, 215의 읽음 부재를 수신기에서 false로 안내할 수 있다. | 206은 발행기관 full ZIP의 해당 멤버와 공차 지침, 211은 당시 URL의 보존 응답·HTML id가 필요하다. 223은 실제 편집 라우트, 228은 같은 항목의 DB 전후 값까지 연결한다. 현재 실패는 과거 부재와 구분한다. |
| 합계의 수치가 맞아도 모집단과 총노동이 맞는지 알 수 없다. | 207에서 반복된 코호트로 만든 정답과 통제는 함께 틀릴 수 있다. 번역자 사건 시간을 독립 검수나 인수 노동까지 포함한 절감률로 바꿀 수도 있다. | 224는 기관 원행의 분자·분모·지리 키를 고정하고 226은 다른 자료의 출력↔주석↔검수 시간↔인수를 따라간다. 같은 품질로 인수한 산출물에 두 역할의 시간이 연결될 때만 비교 범위를 넓힌다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/fc095c323d0177401d34f1daa7b4d1c529e2351f/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/fc095c323d0177401d34f1daa7b4d1c529e2351f/docs/RESEARCH_WORKFLOW.md
[ctl]: https://github.com/laadkke-arch/agentflow-open/blob/fc095c323d0177401d34f1daa7b4d1c529e2351f/docs/automation/dot-control.json
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/7bb2f9e36d5915ebaf73d79b2a6dde44c07dbdf1/docs/workstreams/planning/REVIEW-45.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/bb146773bbffba5e724e8c842951e2c25198c2da...fc095c323d0177401d34f1daa7b4d1c529e2351f
[tasks45]: https://github.com/laadkke-arch/agentflow-open/blob/7bb2f9e36d5915ebaf73d79b2a6dde44c07dbdf1/docs/workstreams/planning/NEXT_TASKS-45.json
[h205]: https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/HANDOFF.md
[r205]: https://github.com/laadkke-arch/agentflow-open/blob/2786b85b692ce28ef20f6904aa56c1bff1f4365d/docs/workstreams/research/AF-RES-205/RESULT.md
[205raw]: https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/receipts/A04/runs.jsonl
[205matrix]: https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/matrix.csv
[205advice]: https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/advice.csv
[h206]: https://github.com/laadkke-arch/agentflow-open/blob/94e2c0ebe8fe36ad66ee1c23c05a91b3ae787db2/docs/workstreams/research/AF-RES-206/HANDOFF.md
[r206]: https://github.com/laadkke-arch/agentflow-open/blob/7292580b919335d196b54fbfa3b8cc8ba327f5f6/docs/workstreams/research/AF-RES-206/RESULT.md
[206raw]: https://github.com/laadkke-arch/agentflow-open/blob/94e2c0ebe8fe36ad66ee1c23c05a91b3ae787db2/docs/workstreams/research/AF-RES-206/receipts/publisher-attempt.txt
[206points]: https://github.com/laadkke-arch/agentflow-open/blob/94e2c0ebe8fe36ad66ee1c23c05a91b3ae787db2/docs/workstreams/research/AF-RES-206/points.csv
[206deltas]: https://github.com/laadkke-arch/agentflow-open/blob/94e2c0ebe8fe36ad66ee1c23c05a91b3ae787db2/docs/workstreams/research/AF-RES-206/deltas.csv
[h207]: https://github.com/laadkke-arch/agentflow-open/blob/ded4731e82fd2e9efd1e10cec6c60f2dd55f7259/docs/workstreams/research/AF-RES-207/HANDOFF.md
[r207]: https://github.com/laadkke-arch/agentflow-open/blob/70217375b704529d9cac0c84addbbc3942ea8b66/docs/workstreams/research/AF-RES-207/RESULT.md
[207raw]: https://github.com/laadkke-arch/agentflow-open/blob/ded4731e82fd2e9efd1e10cec6c60f2dd55f7259/docs/workstreams/research/AF-RES-207/receipts/controls.jsonl
[207matrix]: https://github.com/laadkke-arch/agentflow-open/blob/ded4731e82fd2e9efd1e10cec6c60f2dd55f7259/docs/workstreams/research/AF-RES-207/matrix.csv
[207cost]: https://github.com/laadkke-arch/agentflow-open/blob/ded4731e82fd2e9efd1e10cec6c60f2dd55f7259/docs/workstreams/research/AF-RES-207/costs.csv
[h208]: https://github.com/laadkke-arch/agentflow-open/blob/4b700b6a8ab597f7561508a7feb2f94035220996/docs/workstreams/research/AF-RES-208/HANDOFF.md
[r208]: https://github.com/laadkke-arch/agentflow-open/blob/159354879a1c88755dc2b9424f2ff10a88f6a697/docs/workstreams/research/AF-RES-208/RESULT.md
[208events]: https://github.com/laadkke-arch/agentflow-open/blob/4b700b6a8ab597f7561508a7feb2f94035220996/docs/workstreams/research/AF-RES-208/events.csv
[208methods]: https://github.com/laadkke-arch/agentflow-open/blob/4b700b6a8ab597f7561508a7feb2f94035220996/docs/workstreams/research/AF-RES-208/methods.csv
[208routes]: https://github.com/laadkke-arch/agentflow-open/blob/4b700b6a8ab597f7561508a7feb2f94035220996/docs/workstreams/research/AF-RES-208/routes.csv
[h209]: https://github.com/laadkke-arch/agentflow-open/blob/187cb91aa385ac7c403749e82d9646ffb1ebd135/docs/workstreams/research/AF-RES-209/HANDOFF.md
[r209]: https://github.com/laadkke-arch/agentflow-open/blob/7f67916179ffdbeb4a5cbb459db854ae94bc37d4/docs/workstreams/research/AF-RES-209/RESULT.md
[209queries]: https://github.com/laadkke-arch/agentflow-open/blob/187cb91aa385ac7c403749e82d9646ffb1ebd135/docs/workstreams/research/AF-RES-209/queries.csv
[209paths]: https://github.com/laadkke-arch/agentflow-open/blob/187cb91aa385ac7c403749e82d9646ffb1ebd135/docs/workstreams/research/AF-RES-209/paths.csv
[209matches]: https://github.com/laadkke-arch/agentflow-open/blob/187cb91aa385ac7c403749e82d9646ffb1ebd135/docs/workstreams/research/AF-RES-209/matches.csv
[h210]: https://github.com/laadkke-arch/agentflow-open/blob/097948b68f3be1802c06c15c7beccaeb5478c06c/docs/workstreams/research/AF-RES-210/HANDOFF.md
[r210]: https://github.com/laadkke-arch/agentflow-open/blob/9c1c8fa669247f859381370759fd35eb8107165d/docs/workstreams/research/AF-RES-210/RESULT.md
[210pairs]: https://github.com/laadkke-arch/agentflow-open/blob/097948b68f3be1802c06c15c7beccaeb5478c06c/docs/workstreams/research/AF-RES-210/pairs.csv
[210pred]: https://github.com/laadkke-arch/agentflow-open/blob/097948b68f3be1802c06c15c7beccaeb5478c06c/docs/workstreams/research/AF-RES-210/predictions.csv
[210map]: https://github.com/laadkke-arch/agentflow-open/blob/097948b68f3be1802c06c15c7beccaeb5478c06c/docs/workstreams/research/AF-RES-210/mapping.csv
[h211]: https://github.com/laadkke-arch/agentflow-open/blob/873621fcdeb1bf57c8e6477a0a2c0c9959583a7d/docs/workstreams/research/AF-RES-211/HANDOFF.md
[r211]: https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/RESULT.md
[211vers]: https://github.com/laadkke-arch/agentflow-open/blob/873621fcdeb1bf57c8e6477a0a2c0c9959583a7d/docs/workstreams/research/AF-RES-211/versions.csv
[211dest]: https://github.com/laadkke-arch/agentflow-open/blob/873621fcdeb1bf57c8e6477a0a2c0c9959583a7d/docs/workstreams/research/AF-RES-211/destinations.csv
[211cit]: https://github.com/laadkke-arch/agentflow-open/blob/873621fcdeb1bf57c8e6477a0a2c0c9959583a7d/docs/workstreams/research/AF-RES-211/citations.csv
[h212]: https://github.com/laadkke-arch/agentflow-open/blob/98cd710af3470b8908545ed2a542a5a1df7907c0/docs/workstreams/research/AF-RES-212/HANDOFF.md
[r212]: https://github.com/laadkke-arch/agentflow-open/blob/f4b08aa627c834e4ceb2da232869411470c0e06d/docs/workstreams/research/AF-RES-212/RESULT.md
[212examples]: https://github.com/laadkke-arch/agentflow-open/blob/98cd710af3470b8908545ed2a542a5a1df7907c0/docs/workstreams/research/AF-RES-212/examples.csv
[212names]: https://github.com/laadkke-arch/agentflow-open/blob/98cd710af3470b8908545ed2a542a5a1df7907c0/docs/workstreams/research/AF-RES-212/names.csv
[212cards]: https://github.com/laadkke-arch/agentflow-open/blob/98cd710af3470b8908545ed2a542a5a1df7907c0/docs/workstreams/research/AF-RES-212/cards.md
[h213]: https://github.com/laadkke-arch/agentflow-open/blob/425835c2bba66a7002ad281222163024595987f8/docs/workstreams/research/AF-RES-213/HANDOFF.md
[r213]: https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/RESULT.md
[213objects]: https://github.com/laadkke-arch/agentflow-open/blob/425835c2bba66a7002ad281222163024595987f8/docs/workstreams/research/AF-RES-213/objects.csv
[213res]: https://github.com/laadkke-arch/agentflow-open/blob/425835c2bba66a7002ad281222163024595987f8/docs/workstreams/research/AF-RES-213/resolutions.csv
[213req]: https://github.com/laadkke-arch/agentflow-open/blob/425835c2bba66a7002ad281222163024595987f8/docs/workstreams/research/AF-RES-213/requests.csv
[h214]: https://github.com/laadkke-arch/agentflow-open/blob/81cb77570c6bb620316be4d1fb98d47276e5303c/docs/workstreams/research/AF-RES-214/HANDOFF.md
[r214]: https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/RESULT.md
[214changes]: https://github.com/laadkke-arch/agentflow-open/blob/81cb77570c6bb620316be4d1fb98d47276e5303c/docs/workstreams/research/AF-RES-214/changes.csv
[214dec]: https://github.com/laadkke-arch/agentflow-open/blob/81cb77570c6bb620316be4d1fb98d47276e5303c/docs/workstreams/research/AF-RES-214/decisions.csv
[214support]: https://github.com/laadkke-arch/agentflow-open/blob/81cb77570c6bb620316be4d1fb98d47276e5303c/docs/workstreams/research/AF-RES-214/support.csv
[h215]: https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/HANDOFF.md
[r215]: https://github.com/laadkke-arch/agentflow-open/blob/041af93d09f687dc008203f0a5ca04b00ec2d334/docs/workstreams/research/AF-RES-215/RESULT.md
[215src]: https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/sources.jsonl
[215fields]: https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/fields.csv
[215mig]: https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/migrations.csv
[afterctl]: https://github.com/laadkke-arch/agentflow-open/blob/2a32cb8a661539308320cf985fc5584588203d52/docs/automation/dot-control.json
[h216]: https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/HANDOFF.md
[r216]: https://github.com/laadkke-arch/agentflow-open/blob/e2b767089a72c2e58c1a360d524f2b0d71df8ca9/docs/workstreams/research/AF-RES-216/RESULT.md
[216files]: https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/files.csv
[216deleted]: https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/history-deleted.csv
[216http]: https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/receipts/api/http.json
[h217]: https://github.com/laadkke-arch/agentflow-open/blob/822f1c0be41ca7ffc463669aa3e2b2076389f6e4/docs/workstreams/research/AF-RES-217/HANDOFF.md
[r217]: https://github.com/laadkke-arch/agentflow-open/blob/89af301cc161dd22a13b7c8aa47e8c2ed4c75f44/docs/workstreams/research/AF-RES-217/RESULT.md
[217runs]: https://github.com/laadkke-arch/agentflow-open/blob/822f1c0be41ca7ffc463669aa3e2b2076389f6e4/docs/workstreams/research/AF-RES-217/runs.csv
[217comp]: https://github.com/laadkke-arch/agentflow-open/blob/822f1c0be41ca7ffc463669aa3e2b2076389f6e4/docs/workstreams/research/AF-RES-217/components.csv
[h218]: https://github.com/laadkke-arch/agentflow-open/blob/ee90bf610bae4f03b260aba9cf5d5418720767ee/docs/workstreams/research/AF-RES-218/HANDOFF.md
[r218]: https://github.com/laadkke-arch/agentflow-open/blob/9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f/docs/workstreams/research/AF-RES-218/RESULT.md
[218pixels]: https://github.com/laadkke-arch/agentflow-open/blob/ee90bf610bae4f03b260aba9cf5d5418720767ee/docs/workstreams/research/AF-RES-218/persistence.csv
[218controls]: https://github.com/laadkke-arch/agentflow-open/blob/ee90bf610bae4f03b260aba9cf5d5418720767ee/docs/workstreams/research/AF-RES-218/COUNTEREXAMPLES.md
