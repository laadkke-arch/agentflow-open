# REVIEW-45 · 어떤 원문이 사용자의 다음 행동까지 뒷받침하는가

개발자가 만들 소프트웨어의 일부와 목적을 주었을 때, 탐색기는 재사용할 부품·서비스·다른 분야의 원리를 찾아 **어느 부분에 왜 쓸 수 있는지** 원문 링크와 함께 돌려준다. 이번에 가장 크게 바뀐 판단은 두 가지다. 번역 초안을 고치는 시간이 줄었다는 주장은 실제 원파일까지 되짚을 수 있게 됐고, 그 파일만으로 검수까지 포함한 총노동을 계산할 수 있는지는 여전히 열려 있다. 추천 문장을 보존하는 데에는 주소와 짧은 설명으로 충분했던 경우도 있고, 외부 사본 없이 그 문장의 원문 구간을 다시 보려면 인용 바이트까지 필요했던 경우도 있다. [제품 브리프][product] · [195 원분절][x195] · [196 저장안별 대조][x196]

44차 마감 뒤 **새로 중앙 DONE이 된 연구는 195~204 열 건**이다. 작성자가 자기 완료 조건을 채웠다고 판정한 것은 196 한 건이고 나머지 아홉 건은 PARTIAL이다. 다음 배정은 즉시 시작할 웹 조사·설계 8건, 즉시 시작할 Codex 검사 2건, 205의 실제 관측을 기다리는 Codex 검사 1건이다. [진행표][control] · [작업자에게 전달할 지시문 11건](NEXT_TASKS-45.json)

## 검토 기준과 증거의 단위

계획 브랜치의 최신 누적 파일은 `work/planning@67ee228`의 REVIEW-44였다. 그 검토를 먼저 읽고, 거기에 명시된 **결과 검토 마감** `0502786`에서 이번 요청의 통합판 `bb14677`까지 진행표를 ID·전체 필드로 대조했다. 44차 본문에는 마감 후 195·196의 중앙 완료를 보았다는 추기가 있었고, 두 인계의 결과 검토는 이번 차수로 넘어왔다. 기존 194행 중 195·196만 RUNNING→DONE이 됐고, 나머지 변경 필드는 두 행의 결과 SHA와 최근 진척 시각이었다. 새로 생긴 11행은 197~207이고 사라진 행은 없다. [직전 누적 검토][r44] · [직전 마감 진행표][oldctl] · [통합판 사이 변경][delta]

| 진행표 커밋·시각(UTC) | 전체 | DONE | RUNNING | BLOCKED | 검토 범위 |
| --- | ---: | ---: | ---: | ---: | --- |
| 44차 · 0502786 · 2026-11-24 20:20:41 | 194 | 188 | 2 | 4 | 186~194까지 결과 반영 |
| 45차 · bb14677 · 2026-11-24 21:01:21 | 205 | 198 | 3 | 4 | 기존 195·196 및 신규 197~204 |

198개 중앙 DONE은 연구 196건과 연결 시험 2건이다. 198개 모두 `acceptance_evidence`는 빈 배열이다. 새 완료 열 건에서 중앙 `result_commit`과 배정 브랜치의 끝이 일치하는지 확인한 다음 그 SHA의 소유 경로에서 인계·결과·자체점검과 근거표를 열었다. 중앙 차단은 018(인계 커밋 전 대화 한도), 035(실행 세션 종료 후 인계 미확인), 149(세 유입 경로의 동일 주간 분모 미확보), 151(최초 N0 응답·독립 가림·원사용자 비용 미확인) 네 건이다. [이번 진행표][control] · [운영 규칙][workflow]

| AF-RES | 자체판정 | 중앙 인계 SHA | 인계서가 지정한 결과·자체점검 SHA | 원장 행 / 작업자 산입 자료 | 판단의 실제 분모 |
| --- | --- | --- | --- | ---: | --- |
| 195 · 번역 노동 | PARTIAL | [a674c67][h195] | [a2fe008][r195] | [70 / 40][s195] | 2언어·8문서·24배정·96조건 분절 |
| 196 · 인용 보존 | DONE | [6147197][h196] | [a7ef347][r196] | [47 / 36][s196] | 실제 4문장·24실측 셀, 별도 통제 7 |
| 197 · 표의 선택 | PARTIAL | [be77f85][h197] | [1f01333][r197] | [69 / 44][s197] | MUI 지명 3자리와 TanStack 자연 3자리의 적격성은 다름 |
| 198 · 무손실 컷 | PARTIAL | [05ae34b][h198] | [bd5a271][r198] | [40 / 27][s198] | 원사건 6개·탐색 경로 12·트랙 자리 18 |
| 199 · HDR 원전 | PARTIAL | [80db1b6][h199] | [a887a30][r199] | [52 / 22][s199] | 원논문 2·소비 구현 2·조작 6자리 |
| 200 · 철회한 판 | PARTIAL | [1ae3b56][h200] | [ba6b4d9][r200] | [44 / 28][s200] | 철회 사건 2·배포판 6·현존 파일명 88 |
| 201 · 인용과 그림 | PARTIAL | [2fc69a2][h201] | [59c1dff][r201] | [65 / 43][s201] | 소비자 논문 4·연결 경로 12 |
| 202 · 언어 모델 | PARTIAL | [cc543b8][h202] | [8ac03b5][r202] | [94 / 42][s202] | 실제 파일 메타데이터 6·모드별 자리 12 |
| 203 · 기존 검사 채택 | PARTIAL | [68dcbe0][h203] | [0ebf9bc][r203] | [94 / 41][s203] | 자연 제안 6·보강 2(경계 1 포함) |
| 204 · 지명 검색 | PARTIAL | [1915a73][h204] | [020e8e4][r204] | [49 / 34][s204] | 운영형태×호출 방식 12·잠정 사건 4 |

원장 624행의 JSON과 작업별 source_id 고유성, 위 열 건의 핵심 CSV 29개에서 데이터행과 열 너비를 검산했다. 195의 같은 분절 세 조건을 다시 묶어 비교했고, 196의 실측·결측·통제 분모, 200의 HTML 목록과 빈 flag, 202의 예측·실행 필드를 원행에서 집계했다. **자료 수를 읽을 때 주의할 실제 차이**가 있다. 195·196의 `work_id`는 모든 행에서 각각 작업 ID 하나다. 40·36은 그 필드의 고유 개수가 아니라 작업자가 분류해 산입한 원파일·문서 수다. 196의 재생 영수증에 적힌 원장 44행과 최종 47행의 차이도 추적할 수 있다. 끝의 F07~F09는 공식 PDF 바이트를 받지 못한 세 시도이고 산입은 모두 false다. 이 검토가 독립적으로 다시 계산한 것은 커밋된 표의 값과 관계이며, 외부 프로그램 재실행이나 원사용자 관측은 해당 작업의 영수증 수준으로 표시한다. [195 산입 원장][s195] · [196 최종 원장][s196] · [196 재생 영수증][replay196] · [200 파일표][x200]

## 44차까지 이어지는 제품 판단

| 개발자가 알고 싶은 것 | 지금까지의 근거 | 45차에서 이어 쓰는 판단 |
| --- | --- | --- |
| 전체 설계 없이 무엇을 물을까 | 020은 전달 주장 72/73, 모든 충돌이 풀린 묶음은 2/16이었다. 107은 개별 발생 위치로 편집 6/6, 공유 정의만으로 0/6이었다. 159는 소비자 역할로 48/48을 갈랐다. 189에서 화면 문자열 유지와 추가 검색 방지는 작성자부터 달랐다. | 선택한 대상·다음 동작·보존해야 할 값이 이미 명시돼 있으면 해당 절로 간다. 두 해석이 다른 링크를 필요로 할 때 한 질문을 후보로 둔다. 197의 현재 면과 방문 면 구별이 여기에 더해졌다. |
| 비슷한 이름 밖에서 원리를 찾을 수 있나 | 010은 원분야 단서로 7군을 찾았고 033의 무힌트 144쌍에서 당시판 지지는 0, 145의 독립 초안은 0/16이었다. 166·174·183에 경쟁 예측이 있으나 183의 같은 입력·SHA 공개 실행은 0/16이었다. 191은 CSS 편집 결의와 세 방식 허용을 문헌으로 연결했다. | 원리로 방법을 설명한 것, 힌트 없이 찾은 것, 가까운 대안보다 더 갈라낸 것, 설계자가 실제 선택을 바꾼 것을 각각 묻는다. 199의 두 HDR 원전은 이 중 설명·조작 선택에 증거를 더했다. |
| 단일 링크·택일·필수 조합 중 무엇을 돌려줄까 | 040의 완전 적격은 0/8, 044의 고정 풀에서 두 묶음 방식은 동률이었다. 114의 ‘충돌’ 138건은 118에서 명시 충돌 7·미확인 131로 갈렸다. 146의 48후보는 직접 충족 0·부분 15·충돌 14·미확인 19였다. 193에서 메일 큐 접수와 같은 호스트 사서함 배달은 다른 조건이었다. | 한 주장을 함께 뒷받침하는 문서, 같은 목적의 대안, 함께 작동해야 하는 부품을 별개로 표현한다. 202의 모델·모드와 204의 엔진·운영자는 어떤 두 번째 링크가 필요한지 보여준다. |
| 오래된 답과 현재 쓸 대상을 어떻게 보관할까 | 055는 옛 답 4/4·다음 판 0/4, 147은 과거 답 112/112를 복원했다. 150에서 동일성 값과 근거까지 맞은 쌍은 보관안별 7·9·15/16이었다. 161은 병합 취소 뒤 하류 기록을 별도로 복구했다. 190은 판·면·부분 단서를 붙여 여덟 대상이 모두 유일해졌지만 독립 재탐색은 0/24였다. 192는 인용 논문과 실제 배포판이 달랐다. | 당시 인용과 지금 쓰려는 판·부분을 분리한다. 196의 외부 사본 유무와 201의 소비자측 그림 경로가 어떤 출처를 다시 열어야 하는지 좁혔다. |
| 언제 새 자료를 찾고 기존 이유를 다시 확인할까 | 024의 무효화 11건 중 주기 방식은 11, 신호 방식은 8을 찾았다. 신호는 열람 108회가 적고 전송량은 5,672,462바이트 많았다. 152의 새 자료 15건에서 신호/희소 공급원 방식은 14, 주기는 13이었다. 162·170은 공지·설정·실사용 날짜가 갈렸다. | 신규 발견·기존 이유의 무효화·해당 사용자 환경에서의 접근을 각각 측정한다. 200의 현재 배너, 당시 경고 로그와 업로드 날짜를 별도 시점으로 둔다. |
| 당사자가 알게 되고 선택하거나 실제 해결했나 | 158의 제출 28건은 수신 근거가 아니었다. 163의 발신 35건에 원제출자 재개 보강 1건이 있었다. 180의 자연 8건은 지정 창 안 원제보자 텍스트 후속 0, 022의 미인지→선택 변경→실행은 0/24였다. 194의 PEP 4건 모두 그 연쇄는 0/4였지만 559의 기각 이유에는 기존 helper가 명시됐다. | 접수, 종료, 회신, 동일인의 행동, 같은 조건의 성공을 구분한다. 203은 일반 설정에 대한 새 지식과 구체 옵션 적용을 갈랐다. 관측한 회신이 없으면 효과의 크기도 미확인이다. |
| 재사용이 노동·재작업을 줄였나 | 034에서 한 단계 380→57초, 전체 849→847초였다. 160의 1,061.9인시와 추정 비교값, 164의 공유 직접작성 집단은 별도 처리했다. 172의 전원·동일 기능·시간·독립 검수가 맞은 비교는 0이었다. 181은 터키어 5분절 2,061,853ms·111단어를 찾았으나 24예정 중 1배정만 보였다. | 195가 같은 24자리 원파일을 채웠다. 어느 사람·역할이 어느 시간창에서 일했고 결과물이 같은 품질로 인수됐는지는 다른 질문으로 남는다. |
| 설치·표시·합격 근거로 마지막 동작까지 안내할 수 있나 | 154의 원본 명시 회수 10/10, 기본 다운로드 동일 바이트 6/10이다. 176의 합격 표시 55/55는 한 보고서 재표시였고, 186은 같은 열 시험에서 두 엔진의 판정이 9/10 일치했다. 187은 실제 wheel·쓰기 전파, 188은 기관 원점·점별 공차가 비었다. 188에서 격자를 열고도 다른 수직 연산을 선택한 로그는 있었다. | 같은 입력·판·실효 경로·최종 결과 중 관측된 마지막 단계까지만 약속한다. 198의 경계 재인코딩과 202의 로드 예측, 205·206의 요청 시점 검사가 이 한계를 구체화한다. |

이전 수치의 원 출전과 정정 계보는 44차 누적표에 연결돼 있다. 링크+요약, 추가 구조, 요청 시 확인과 주기 갱신, AI 전처리, AgentFlow 입력 계약, 최종 순위·DB는 여전히 비교할 설계 선택지다. [44차 누적표와 신규 아홉 건의 근거][r44] · [제품이 열어 둔 질문][product]

## 새 결과 열 건의 근거와 미달 항목

**195 · 고정 원파일에서 세 조건의 시간과 산출물을 다시 연결했다.** 이탈리아어·터키어 각 107개 본실험 문서의 첫 네 문서에서 계획 파일과 완료 파일이 24/24로 이어진다. 같은 원문마다 서로 다른 세 번역자가 직접 번역(HT) 또는 두 기계 초안의 후편집(PE1·PE2)을 맡았다. 96조건 분절 전부가 저자 파서의 지표와 일치했다. 32개 같은 원문 중 PE1과 PE2가 HT보다 오래 걸린 것은 각각 9개다. 터키어 첫 문서에서 PE2 720,511ms, HT 2,061,853ms였으나 60초 이상 간격을 제외하는 감도에서는 523,317 대 517,066ms로 순서가 바뀐다. 긴 간격의 용도는 기록에 없다. 고정 Hugging Face TSV로 교차 확인한 분절은 언어별 0/48이었다. 최종 산출물에 연결된 독립 검수 키·시간도 0/96이다. 번역자 시간만으로 총노동 절감률을 계산할 수 없다. [24배정][a195] · [96분절][x195] · [원자료 재생 영수증][audit195] · [195 결과][r195]

**196 · 짧은 문장을 재표시하는 일과 원문을 다시 읽는 일의 저장 비용이 달랐다.** A는 주소와 짧은 문장, B는 판·경로·구간 해시까지, C는 정확한 인용 바이트와 위치까지 보존했다. 당시 제출 두 문장과 새 실행 두 문장에서 외부 사본이 없어도 A/B/C 모두 표시 문장·주체·기준일 4/4를 돌려줬다. 원문을 다시 읽고 보관 지문까지 맞춘 것은 C 4/4였다. 고정 사본을 공급하면 A도 원문 4/4를 읽었고 B도 지문 4/4를 맞췄다. 네 문장의 저장량은 1,192 / 2,078 / 5,134바이트다. 36개 예정 셀 중 미실행을 명시한 입력이 원래 없었던 12셀은 결측이다. C에서 인용문과 해시를 함께 바꾼 대조는 내부 일치를 통과하고 별도 정답과 어긋났다. 한 인계·두 시험 키에서 얻은 이 수치로 여러 행의 집계나 원출전의 진위를 보장할 수 없다. [43개 실측·결측·통제행][x196] · [비용][cost196] · [변조·경로 통제 원로그][ctrl196]

**197 · ‘전체 선택’의 대상이 현재 페이지인지 방문한 페이지인지 원작성자가 가른다.** MUI #14070은 둘째 페이지의 행 전부, #14074는 같은 필터에서 이전 페이지에서 체크한 행의 보존을 원했다. 후자는 다른 필터로 바뀌면 맞지 않는 행을 해제하는 처리까지 받아들였다. TanStack에서는 선택 ID가 남아 있는 상태, 현재 로드된 행 객체, 서버가 돌려준 ID 목록이 다른 단계다. 실제 일괄 요청의 수신·처리 ID는 0건이고, 최초 본문의 실제 ID를 같은 작성자의 후속까지 연결한 자리도 0/1이다. TanStack 자연 세 자리는 1잠정·1경계·1결측으로 최초 적격 확정 0/3이다. UI 상태를 보고 업무 서버가 특정 청구서를 처리했다고 쓰면 근거를 넘어선다. [원요구][x197] · [선택·수신 경계][sel197] · [질문과 즉답][route197]

**198 · ‘무손실’은 원하는 프레임과 트랙을 동시에 보장하지 않았다.** LosslessCut v3.44.0 소스는 시작이 키프레임이면 경계 처리를 건너뛰고, 필요한 경우 앞 경계를 인코딩한 뒤 다음 키프레임부터 복사해 잇는 경로를 보여준다. 독립 진입점과 트랙 경계가 맞으면 단순 복사가 충분할 수 있다. #1190의 다음 키프레임 탐색, #1834의 음성 끊김, #2049의 자막 어긋남은 서로 다른 제보다. 여섯 원사건에서 동일 입력의 디코딩 프레임·패킷 지문을 함께 확인한 것은 0/6, 최초 본문판도 0/6이다. 두 경로 여섯 쌍 중 세 쌍은 최종 주소가 같았다. 열두 경로를 사후 열었지만 **개별 질의가 실제로 반환한 첫 URL은 0/12**여서 기술 단어를 넣으면 검색이 나아진다는 주장을 시험하지 못했다. [경계·트랙 18자리][x198] · [실제 탐색·수동 경로][path198] · [대안 다섯 가지][alt198]

**199 · 같은 이름과 ‘로컬’이라는 말이 다른 연산을 가리켰다.** 2002 원전과 pfstmo reinhard02는 이웃의 휘도와 선택적 다중 스케일을 다룬다. 2005 광수용체 모형을 인용한 OpenCV 4.10.0에서는 픽셀/전역과 채널/휘도 혼합을 조절한다. 여기서 픽셀의 적응은 공간 반경으로 사용할 수 없다. pfstmo CLI의 phi 기본값 1과 논문의 8도 다르다. 단순 호출법만 원하는 경우에는 가까운 구현 문서가 이미 충분했다. 산입 문서는 22개지만 저자 계열 3/4와 실제 예제·결과 계열 4/5가 미달이다. pfstmo 공식 배포 소스와 거울의 바이트 동일성, 같은 입력·감마에 대한 실측 출력, 사람의 화질 선호는 미확인이다. [원리와 구현 계보][lin199] · [조작별 여섯 행][x199] · [목적별 카드][card199]

**200 · 철회된 릴리스의 링크가 살아 있어도 환경과 목적별 안내가 갈렸다.** matplotlib 3.9.1의 Windows wheel 삭제 뒤 소스 빌드 시도 문제가 커졌다는 유지자 설명과 철회 배너가 있다. 현재 HTML 목록은 대상판 24파일, 양 인접판 각 29파일이다. 대상판에는 Windows 태그가 없고 양옆 판에는 각 5개 있다. 이 차가 삭제 파일 5개의 원목록을 복원하지는 않는다. pytest 8.1.0에는 당시 정확판 캐시 설치의 경고·성공 기록이 있고, 8.1.1이 복구한 일부 훅과 복구하지 않은 private 호출이 구분된다. 정확판을 재현하려는 사람과 새 범위로 설치하는 사람의 첫 링크가 달라질 이유다. 여섯 판의 현존 파일 88개(철회 대상 26개) 전부에서 파일별 원 flag·reason은 미확인이고, matplotlib post1에서 동일 장애가 실제 고쳐졌는지도 비었다. [파일 목록][x200] · [공지·당시 사건][notice200] · [제약별 권고][adv200]

**201 · 논문에서 라이브러리를 언급한 사실과 그림을 만든 함수는 다른 증거를 요구했다.** colorspace Fig. 5 우측은 `sns.displot` 호출과 원고가 같은 `fig-plotting.png`를 가리킨다. 논문 예의 height=4와 생성 스크립트의 5는 달랐고 당시 출력 실행 기록은 없다. k-diagram은 seaborn 의존 선언·지연 로더가 있지만 살핀 polar violin은 SciPy KDE와 `ax.fill`을 사용한다. Vizagrams에는 자체 Julia BoxPlot이 있다. RaincloudPlots 2019 초판 코드는 2021 Waskom DOI보다 앞서도 seaborn을 호출할 수 있었다. 네 출판 사례의 당대 실행-출력 연결은 0/4, 초판의 모든 별칭 위치 재검증과 대조 공연의 원음(0/1)도 미달이다. 근거가 지지하는 최대 범위는 비교문헌, 구체 함수, 그림 생성 경로로 각각 다르다. [언급 26행][men201] · [함수와 그림 14행][x201] · [목적별 경로][route201]

**202 · 여섯 파일의 존재와 엔진 모드 12자리의 실측 사이가 비어 있다.** Tesseract 5.3.0과 세 모음 4.1.0에서 영문·아랍어 모델의 Git blob과 크기를 확인했다. 모음 규칙으로는 7자리 지원 예상(legacy 빌드 조건 1 포함), 5자리 미지원 예상이다. 실제 파일의 내부 구성 판독은 0/6, 해당 엔진판 로드는 0/12다. 파일이 없는 ENOENT, 특정 엔진 구성 누락, 인식 품질 문제를 각 제보가 서로 다른 단계에서 보여준다. 같은 경로에 이름이 같은 사본이 있을 때 성공한 사본의 경로와 지문을 연결한 관측은 없다. 세 주표본 후보의 엄격한 최초성도 0/3 확정이다. 크기가 맞는 다른 판의 dump를 해당 파일의 구성으로 인용할 수 없다. [실제 SHA·모드 예측][x202] · [오류·수정 제보][case202] · [목적별 동반 파일][bundle202]

**203 · 새 설정 방안에 동의한 회신은 있었고 기존 규칙을 적용한 같은 사람의 행동은 확인되지 않았다.** 자연 여섯, 보강 두 자리에서 정확한 링크·당시 이용 가능·사전 미인지·선택 변경·원제안자 행동이 모두 이어진 것은 각각 0/6과 0/2였다. #12495는 일반 설정 가능성을 몰랐다는 발언에서 새 설정 설계 동의로 갔다. #12424의 당시 lifetime 검사는 함수 중심이었고, 나중 구현 헤더 확장을 병합한 사람은 달랐다. 여섯 본문 최초 revision은 0/6이고 날짜·역할이 확실한 엄격 회신 증거는 2/4였다. ‘기존 기능이 당사자를 설득했다’거나 ‘효과가 0’이라고 단정할 근거가 모두 부족하다. [최초 제안][x203] · [행동 연표][time203] · [당대 지원 범위][cov203]

**204 · 공용 서비스의 이용 조건, 엔진 기능, 오프라인 배포 자산을 같은 이름으로 추천할 수 없다.** 공용 Nominatim에 적용되는 앱 전체 초당 1회 상한과 자동완성 금지는 해당 호스트의 조건이다. 자체 Nominatim에 그 규칙을 복사할 근거는 없고, 그 검색 API가 입력 도중 후보를 보장하는 것도 별개다. Photon은 후보 검색을 지원하지만 공용 데모의 가용성·처리량을 약속하는 수치는 확인되지 않았다. #805는 기존 앱이 오프라인 Photon으로 옮길 수 있는지 묻고 주소·매개변수를 확인한 대화다. 새 상태에서 성공한 결과가 비었다. 네 운영형태×세 요청에 대한 근거표는 있으나 양 프로젝트에서 기간 내 최초 두 건씩이라는 적격 사건은 0/4 확정이다. 34개 자료와 임시 사건 네 건은 실제 이전 성공률의 분모가 될 수 없다. [기능·운영 조건 12자리][x204] · [발신 환경별 네 사건][case204] · [OSMF 공용 호스트 방침](https://operations.osmfoundation.org/policies/nominatim/)

## 서로 어긋난 결론을 어떻게 쓸 것인가

| 겉으로 어긋난 결론 | 근거를 맞춰 보니 달랐던 것 | 탐색기가 줄 수 있는 답과 판정 전환 조건 |
| --- | --- | --- |
| 181은 번역 배정 1자리만 보았고 195는 24자리 전부를 복원했다. 그래도 ‘초안이 더 빠르다’는 결론은 흔들린다. | 앞선 것은 공개 투영, 뒤의 것은 두 원 ZIP이다. 같은 터키어 문서에서도 대기 간격을 처리하는 방법에 따라 시간 순서가 역전된다. | 원파일·조건·시간창과 함께 번역자 기록을 제시한다. 같은 산출물의 독립 인수·검수 노동이 있어야 전체 노동으로 확대한다. [배정][a195] · [시간·역할 경계][bound195] |
| 196에서는 짧은 링크와 설명이 충분하기도 했고 불충분하기도 했다. 201에는 실제 스크립트와 그림 파일명까지 있다. | 표시 문장 확인, 고정 사본에서 원문 읽기, 사본 없이 인용 바이트 대조, 그 코드의 역사적 실행은 네 가지 다른 목적이다. | 문장 재표시에는 간단한 기록을 유지할 수 있다. 실행 경위를 주장하려면 당시 입력·실효판·출력 연결이 필요하다. 여러 관측을 합친 문장의 보존은 207의 별도 판정이다. [196 행렬][x196] · [201 함수·출력][x201] |
| 197의 체크 ID와 198의 ‘lossless’, 202의 모델 목록은 표면상 같은 동작을 완성한 듯 보였다. | ID가 남은 위치는 UI, 독립 진입점은 영상 스트림, SHA는 모델 자산이다. 수신 서버·음성/자막 시간축·실효 언어 모드에서 확인할 값이 따로 있다. | 원요구가 지정한 마지막 경계를 찾아 해당 절을 먼저 준다. 수신 ID나 로드 로그가 없으면 원자료가 끝나는 단계까지 표시한다. [선택][sel197] · [트랙][x198] · [모델][x202] |
| 199에는 원리가 드러난 소스가 있고 203에는 기존 기능을 새로 안 당사자 발언이 있다. | 직접 인용으로 구현 방식은 설명할 수 있다. 일반 설정의 존재를 알게 된 것만으로 특정 제공판을 실제로 적용한 원인을 알 수는 없다. | 설명용 원전, 기능이 이미 있던 판, 당사자 선택 변화의 증거에 다른 추천 문구를 붙인다. [조작 대응][x199] · [행동 연표][time203] |
| 200의 철회판에는 설치 성공 기록이 있고, 204의 오픈소스 검색 엔진에는 공용 자동완성 금지가 있다. | 과거 정확판 캐시 설치와 새 범위 해석, 배포 엔진과 특정 운영자의 API가 각각 다른 객체다. | 요청 목적·환경·운영자를 확인한 뒤 현재 링크와 당시 증거를 함께 보존한다. 현 배너와 현재 방침을 과거 전체 환경으로 확대하지 않는다. [200 실제 사례][notice200] · [204 운영자별 대조][x204] |

## 새 작업의 착수 조건과 분업

웹 작업은 아래 여덟 가지 다른 제품 결정을 다룬다. 같은 사례를 여러 작업자가 재요약하는 일을 줄이기 위해 모집 대상·판정값·반례까지 각각 고정했다. 바로 시작할 열 건은 모두 이미 확정된 197~204 인계만 사용한다. 지명 목적표본으로 처분이 흔한 정도를 추정하지 않고, 실제 검색 비교가 필요한 209에서는 합쳐진 검색 결과가 어느 한 질의의 1위로 들어갈 수 없게 했다. [브랜치·소유 경로·완료 조건·전체 지시문](NEXT_TASKS-45.json)

| ID·담당 | 선행·착수 상태 | 고정할 자료와 판정 단위 | 사용자의 어느 결정을 바꾸는가 |
| --- | --- | --- | --- |
| 208 · 웹 | 197 · 즉시 | Nextcloud 반복 일정 원제보 4, 예외/연속 변경/시리즈 분할과 경계 통제 4 | 한 회차만 고칠지, 이미 옮겨진 예외를 남긴 채 미래 회차를 바꿀지에 맞는 첫 절 |
| 209 · 웹 | 198 · 즉시 | JPEG 방향·가장자리 요청 4, 원표현/단서 추가 8개의 개별 검색과 실제 도착 절 | 보존할 대상을 검색어에 하나 더 넣었을 때 새로 얻거나 밀려난 첫 링크 |
| 210 · 웹 | 199 · 즉시 | Git patience·histogram 시험 및 Breezy 입력쌍, 카드 정렬 원리와 별도 통제 4 | 가까운 diff 설명에 원전을 추가하면 어떤 공통 줄을 기준으로 삼을지 더 가를 수 있는가 |
| 211 · 웹 | 200 · 즉시 | urllib3·Pillow 두 API 경계, 3목적×3문서 경로×2프로젝트 | 별칭 주소를 유지할지, 이전 판 절로 바꿀지, 개정 이력을 옆에 둘지 |
| 212 · 웹 | 201 · 즉시 | GOV.UK·USWDS 6예시/12앵커, 문단 읽기와 링크 목록, 추천 문구 세 목적 | 주변 문장을 떼어도 비교 문헌·호출 예·산출물을 구별하는 클릭 문구 |
| 213 · 웹 | 202 · 즉시 | CSL 저널 별칭 2·부모·독립 대조와 locale 3, 소비자 Zotero·Pandoc | 저널 양식 표시·직접 편집·오프라인 준비에서 어떤 원파일을 함께 줄지 |
| 214 · 웹 | 203 · 즉시 | HTML dialog polyfill 제거 패치 4, 문서와 타입 제거 대조 2 | 이미 알던 표준의 지원 환경 변화와 링크를 통한 새 발견 중 무엇을 제거 이유로 안내할지 |
| 215 · 웹 | 204 · 즉시 | Inoreader→FreshRSS의 6필드×2출력, 별도 소비자 이관 사건 4 | 구독 주소만 옮길 때와 별표·읽음 상태까지 요구할 때 어떤 송수신 절이 필요한지 |
| 216 · Codex | 200 · 즉시 | 버전 JSON 6·Simple JSON 2, 현재 파일 목록 88과 삭제 집단 1 | 특정 파일에 철회 경고를 적을 수 있는지, 현재 원값과 과거 상태의 경계는 어디인지 |
| 217 · Codex | 202 · 즉시 | 6개 정확 traineddata 내부와 OEM별 12자리×2, 실제 열린 파일과 Init | 정확 언어 파일과 엔진 모드를 함께 갖춘 사용자가 실제로 초기화할 수 있는지 |
| 218 · Codex | **205 · BLOCKED** | 205에서 전파를 관측한 Astropy 호출 1개, FITS 3모드×2경로×2저장 경계, 새 reader | 같은 프로세스의 원본만 바뀐 것인지 닫은 뒤 같은 파일의 픽셀까지 바뀌었는지 |

작업자에게 줄 출발점으로 반복 일정의 제공자 예제, JPEG 제작자의 처리 설명, Git의 고정 테스트, 문서 호스트의 버전 설명을 확인했다. 접근성은 W3C의 링크 목적과 NVDA 요소 목록, CSL은 표준의 부모 스타일 정의, 네이티브 대화상자는 실제 제거 PR, 피드 이전은 발행자 OPML 설명과 수신기 이슈에서 시작한다. 이들은 조사 입구이며, 표의 각 가설을 입증한 수로 미리 세지 않는다. [반복 일정](https://developers.google.com/workspace/calendar/api/guides/recurringevents) · [JPEG 제작자 문서](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/doc/usage.txt) · [Git 고정 테스트](https://github.com/git/git/blob/v2.43.0/t/t4033-diff-patience.sh) · [문서 버전](https://docs.readthedocs.com/platform/stable/versions.html) · [링크 목적](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html) · [NVDA](https://download.nvaccess.org/documentation/userGuide.html) · [CSL](https://docs.citationstyles.org/en/stable/specification.html) · [대화상자 PR](https://github.com/hashicorp/design-system/pull/1977) · [피드 내보내기](https://www.inoreader.com/help/pro/output-feeds/what-is-opml-used-for) · [수신기 원제보](https://github.com/FreshRSS/FreshRSS/issues/5583)

**205~207은 요청 시 모두 Codex RUNNING이고 중앙 결과 SHA가 null이다.** 205는 네 wheel과 8환경·32자리에서 값·버퍼 공유·원본 쓰기를 검사한다. 206은 영국 발행기관 개발자 팩의 주점 네 개와 충돌 대조점 두 개의 원수치·기준면·공차를 검사한다. 207은 195의 번역 원행과 196에서 단건 복원에 통과한 표현을 이용해, 합계가 같아도 선택 행·분모·단위가 어긋난 설명을 가려내는 검사다. 207 행의 예전 계획 차단 사유에는 ‘195·196 RUNNING’이 남아 있지만 현재 `status`는 RUNNING이고 두 선행의 SHA는 이미 기록됐다. 웹 208~215는 이 입력과 판별 목표를 모두 비켜간다. 216·217의 분모도 각각 PyPI 파일과 OCR 초기화로 고정했다. [요청 시점 중앙 기준][control] · [세 검사의 원래 배정][p44]

218은 205 중앙 DONE, 고정 SHA의 HANDOFF, 정확한 환경·호출·가변 원본의 전후 값이 담긴 Astropy 양성 영수증을 받아야 착수한다. 쓰기 전파가 관측된 셀이 하나도 없다면 이 파일 영속성 검사의 선행 전제도 성립하지 않는다. 206의 기관 발행값을 인용하는 공차 후속과 207의 결과로 복수행 근거 저장안을 비교하는 후속은 이번 착수 목록에 올리지 않았다. 각각 기관 원행 또는 실제 통과·오판 셀이 나온 뒤에야 다음 질문을 정할 수 있다. [205~207의 요청 시점 인계 상태][control] · [218의 정확한 착수 요건](NEXT_TASKS-45.json)

**마감 뒤 상태 변경.** 21:18:40 UTC의 통합판 `3d8ae63`에서 205·206이 중앙 DONE으로 전환됐고, 21:23:02 UTC의 `75dcc53`에서 207도 DONE으로 전환됐다. 진행표가 가리키는 인계 SHA는 각각 `3853289`, `94e2c0e`, `ded4731`이다. 위의 결과 검토와 배정 가능 여부는 요청 시점 `bb14677`에서 동결했다. 다음 누적 검토자는 `bb14677` 이후의 이 세 인계를 읽으면 된다. 218을 배정할 때에는 205 인계의 Astropy 양성 셀까지 확인해야 한다. [205·206 상태 변경](https://github.com/laadkke-arch/agentflow-open/blob/3d8ae6326a1cd0ab7771aed68ef7022eb4b4faf1/docs/automation/dot-control.json) · [207 상태 변경](https://github.com/laadkke-arch/agentflow-open/blob/75dcc53e8a4f9b1f7af35e817d0e63cbbc7cd9d3/docs/automation/dot-control.json)

## 다음 판정을 바꿀 약점 세 건

| 중요한 약점 | 지금 남아 있는 오판 가능성 | 다음 확인과 그때 달라질 답 |
| --- | --- | --- |
| 사용자가 밟은 경로를 연구자가 나중에 고른 경로로 대신하기 쉽다. | 197·204는 ‘최초 적격’ 분모를 복구하지 못했고, 198의 12개 실제 재열람에는 개별 검색 첫 노출이 없다. 203의 설정 동의도 같은 사람의 실제 적용을 증명하지 못한다. | 209에서 쿼리별 순서·원주소를 따로 보존한다. 214에서는 적용 전 부모판과 발언·패치 순서를 연결한다. 노출이나 인과가 없으면 검색 이득과 발견 효과는 미확인으로 둔다. |
| 배포·문서·UI에서 확인한 한 단계가 실제 끝단 보장으로 읽힌다. | 200에는 88개 파일별 철회 원값, 202에는 6파일의 내부 구성과 12회 로드, 197에는 수신 ID가 빠졌다. | 216이 두 API 원값을, 217이 실제 파일·구성과 초기화를 연결한다. 208·215는 원요구와 같은 사건의 수신 상태가 있을 때만 그 단계를 안내한다. 동일 파일이 다음 프로세스에서도 바뀌었다는 주장은 218의 원경로·픽셀 관측이 있어야 한다. |
| 문장이나 합계를 다시 제시할 수 있어도 믿을 근거와 노동 범위가 비어 있다. | 195의 96행에는 검수 키·시간이 없고, 196의 네 문장은 묶음과 지문을 함께 바꾸면 자체 대조가 통과한다. 201도 정적 생성 경로에서 당시 실행으로 이어지지 않았다. | 기다리고 있는 207의 행·분모 오판을 받아 보존 요건을 갱신한다. 번역 노동에는 같은 산출물의 별도 인수 기록과 검수 시간, 그림에는 당시 실행과 산출물을 잇는 기록이 필요하다. 확보 전에는 단계별 사실과 미확인을 각각 반환한다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/RESEARCH_WORKFLOW.md
[control]: https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/automation/dot-control.json
[r44]: https://github.com/laadkke-arch/agentflow-open/blob/67ee2284362827b72d2e807cb0f11dcb170cde26/docs/workstreams/planning/REVIEW-44.md
[p44]: https://github.com/laadkke-arch/agentflow-open/blob/67ee2284362827b72d2e807cb0f11dcb170cde26/docs/workstreams/planning/NEXT_TASKS-44.json
[oldctl]: https://github.com/laadkke-arch/agentflow-open/blob/050278651b11a2a3a49d45baebf41c707c06b700/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/050278651b11a2a3a49d45baebf41c707c06b700...bb146773bbffba5e724e8c842951e2c25198c2da
[h195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/HANDOFF.md
[s195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/sources.jsonl
[x195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/segments.csv
[a195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/assignments.csv
[bound195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/bounds.csv
[audit195]: https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/receipts/05.md
[r195]: https://github.com/laadkke-arch/agentflow-open/blob/a2fe008274607a4383e90a61d23a74938874d499/docs/workstreams/research/AF-RES-195/RESULT.md
[h196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/HANDOFF.md
[s196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/sources.jsonl
[x196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/matrix.csv
[cost196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/costs.csv
[ctrl196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/receipts/controls.jsonl
[replay196]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/receipts/replay.json
[r196]: https://github.com/laadkke-arch/agentflow-open/blob/a7ef347e91b4a54427023e6eb2bacb57f5bd208a/docs/workstreams/research/AF-RES-196/RESULT.md
[h197]: https://github.com/laadkke-arch/agentflow-open/blob/be77f8550bbfcc1eaba2e8422b9d96101392a08d/docs/workstreams/research/AF-RES-197/HANDOFF.md
[s197]: https://github.com/laadkke-arch/agentflow-open/blob/be77f8550bbfcc1eaba2e8422b9d96101392a08d/docs/workstreams/research/AF-RES-197/sources.jsonl
[x197]: https://github.com/laadkke-arch/agentflow-open/blob/be77f8550bbfcc1eaba2e8422b9d96101392a08d/docs/workstreams/research/AF-RES-197/requests.csv
[sel197]: https://github.com/laadkke-arch/agentflow-open/blob/be77f8550bbfcc1eaba2e8422b9d96101392a08d/docs/workstreams/research/AF-RES-197/selection.csv
[route197]: https://github.com/laadkke-arch/agentflow-open/blob/be77f8550bbfcc1eaba2e8422b9d96101392a08d/docs/workstreams/research/AF-RES-197/answers.csv
[r197]: https://github.com/laadkke-arch/agentflow-open/blob/1f01333bcac478e879ce1c61bbd5310c4fbbc127/docs/workstreams/research/AF-RES-197/RESULT.md
[h198]: https://github.com/laadkke-arch/agentflow-open/blob/05ae34bd0a160ce9ce52658616fad6f0273ea883/docs/workstreams/research/AF-RES-198/HANDOFF.md
[s198]: https://github.com/laadkke-arch/agentflow-open/blob/05ae34bd0a160ce9ce52658616fad6f0273ea883/docs/workstreams/research/AF-RES-198/sources.jsonl
[x198]: https://github.com/laadkke-arch/agentflow-open/blob/05ae34bd0a160ce9ce52658616fad6f0273ea883/docs/workstreams/research/AF-RES-198/cuts.csv
[path198]: https://github.com/laadkke-arch/agentflow-open/blob/05ae34bd0a160ce9ce52658616fad6f0273ea883/docs/workstreams/research/AF-RES-198/paths.csv
[alt198]: https://github.com/laadkke-arch/agentflow-open/blob/05ae34bd0a160ce9ce52658616fad6f0273ea883/docs/workstreams/research/AF-RES-198/alternatives.csv
[r198]: https://github.com/laadkke-arch/agentflow-open/blob/bd5a271b699dc57c02da13f56c9465b1090c087b/docs/workstreams/research/AF-RES-198/RESULT.md
[h199]: https://github.com/laadkke-arch/agentflow-open/blob/80db1b64c7fa9e6c1ccaf131813a0f10cd879aca/docs/workstreams/research/AF-RES-199/HANDOFF.md
[s199]: https://github.com/laadkke-arch/agentflow-open/blob/80db1b64c7fa9e6c1ccaf131813a0f10cd879aca/docs/workstreams/research/AF-RES-199/sources.jsonl
[x199]: https://github.com/laadkke-arch/agentflow-open/blob/80db1b64c7fa9e6c1ccaf131813a0f10cd879aca/docs/workstreams/research/AF-RES-199/operators.csv
[lin199]: https://github.com/laadkke-arch/agentflow-open/blob/80db1b64c7fa9e6c1ccaf131813a0f10cd879aca/docs/workstreams/research/AF-RES-199/lineage.csv
[card199]: https://github.com/laadkke-arch/agentflow-open/blob/80db1b64c7fa9e6c1ccaf131813a0f10cd879aca/docs/workstreams/research/AF-RES-199/cards.csv
[r199]: https://github.com/laadkke-arch/agentflow-open/blob/a887a30241cd0daf0b1c1345681f5adcce9a69a3/docs/workstreams/research/AF-RES-199/RESULT.md
[h200]: https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/HANDOFF.md
[s200]: https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/sources.jsonl
[x200]: https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/releases.csv
[notice200]: https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/notices.csv
[adv200]: https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/advice.csv
[r200]: https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/RESULT.md
[h201]: https://github.com/laadkke-arch/agentflow-open/blob/2fc69a2d9092330e30097c018427a45b1bd7d0d9/docs/workstreams/research/AF-RES-201/HANDOFF.md
[s201]: https://github.com/laadkke-arch/agentflow-open/blob/2fc69a2d9092330e30097c018427a45b1bd7d0d9/docs/workstreams/research/AF-RES-201/sources.jsonl
[x201]: https://github.com/laadkke-arch/agentflow-open/blob/2fc69a2d9092330e30097c018427a45b1bd7d0d9/docs/workstreams/research/AF-RES-201/usage.csv
[men201]: https://github.com/laadkke-arch/agentflow-open/blob/2fc69a2d9092330e30097c018427a45b1bd7d0d9/docs/workstreams/research/AF-RES-201/mentions.csv
[route201]: https://github.com/laadkke-arch/agentflow-open/blob/2fc69a2d9092330e30097c018427a45b1bd7d0d9/docs/workstreams/research/AF-RES-201/routes.csv
[r201]: https://github.com/laadkke-arch/agentflow-open/blob/59c1dff20dd0cbe72d3d274e8e1c739590d4d768/docs/workstreams/research/AF-RES-201/RESULT.md
[h202]: https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/HANDOFF.md
[s202]: https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/sources.jsonl
[x202]: https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/models.csv
[case202]: https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/cases.csv
[bundle202]: https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/bundles.csv
[r202]: https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/RESULT.md
[h203]: https://github.com/laadkke-arch/agentflow-open/blob/68dcbe0047d2c0653e39cafe65f98d541acb9eb0/docs/workstreams/research/AF-RES-203/HANDOFF.md
[s203]: https://github.com/laadkke-arch/agentflow-open/blob/68dcbe0047d2c0653e39cafe65f98d541acb9eb0/docs/workstreams/research/AF-RES-203/sources.jsonl
[x203]: https://github.com/laadkke-arch/agentflow-open/blob/68dcbe0047d2c0653e39cafe65f98d541acb9eb0/docs/workstreams/research/AF-RES-203/proposals.csv
[time203]: https://github.com/laadkke-arch/agentflow-open/blob/68dcbe0047d2c0653e39cafe65f98d541acb9eb0/docs/workstreams/research/AF-RES-203/timeline.csv
[cov203]: https://github.com/laadkke-arch/agentflow-open/blob/68dcbe0047d2c0653e39cafe65f98d541acb9eb0/docs/workstreams/research/AF-RES-203/coverage.csv
[r203]: https://github.com/laadkke-arch/agentflow-open/blob/0ebf9bcc82d63a415e86711014099dc6a54f67cd/docs/workstreams/research/AF-RES-203/RESULT.md
[h204]: https://github.com/laadkke-arch/agentflow-open/blob/1915a735edd7f432f5a6d3de858049c98a1fcf83/docs/workstreams/research/AF-RES-204/HANDOFF.md
[s204]: https://github.com/laadkke-arch/agentflow-open/blob/1915a735edd7f432f5a6d3de858049c98a1fcf83/docs/workstreams/research/AF-RES-204/sources.jsonl
[x204]: https://github.com/laadkke-arch/agentflow-open/blob/1915a735edd7f432f5a6d3de858049c98a1fcf83/docs/workstreams/research/AF-RES-204/surfaces.csv
[case204]: https://github.com/laadkke-arch/agentflow-open/blob/1915a735edd7f432f5a6d3de858049c98a1fcf83/docs/workstreams/research/AF-RES-204/cases.csv
[r204]: https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/RESULT.md
