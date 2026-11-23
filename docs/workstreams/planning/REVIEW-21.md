# REVIEW-21 · 어느 조건까지 확인해야 이 링크를 권할 수 있는가

같은 악보에서 두 수정안 모두 새 파트의 잘못된 선택색을 없앴다. 둘을 가른 것은 파트 밖에서 음을 복제한 직후의 상태였다. 저장하고 다시 열자 그 차이도 사라졌다. 반대로 문서 사이트에서는 지금 옛판의 HTML과 같은 파일을 받아도, 배포 당시 그 주소에서 독자가 두 조건을 함께 만족했는지까지 복원할 수 없었다. 탐색기가 링크 옆에 쓸 수 있는 주장은 **누가, 어느 판에서, 어떤 조작을 한 뒤, 무엇을 확인했는가**에 달려 있다. [악보 실행표][r81] · [문서 사이트의 요구와 관측][r82]

## 검토 대상과 근거의 범위

2026-11-23 UTC, `work/planning`의 최신 [REVIEW-20][prev]을 먼저 읽었다. 거기서 사용한 [진행표 e7a777f][old]와 이번 [진행표 184137d][reg]의 배열을 ID별로 비교했다. 등록은 78→82, DONE은 76→80, BLOCKED는 2→2였다. 기존 78행은 모든 필드가 같고 018·035가 계속 BLOCKED다. 새 DONE 081–084의 등록 SHA 네 개는 모두 각 작업 브랜치의 끝과 일치했다. 네 커밋 모두 부모의 완결 결과에 HANDOFF.md 한 파일을 추가했다. DONE 80행의 중앙 `acceptance_evidence`는 모두 비어 있다. 이번 네 작업의 **연구 판정은 모두 PARTIAL**이며, 아래에서 어떤 부분을 수용할 수 있는지 구체적으로 적었다.

| 새 DONE · 배정 역할 | 고정 인계 · 결과 | 검토에서 직접 대조한 단위 | 결정을 보류할 지점 |
| --- | --- | --- | --- |
| 081 · codex-cloud | [60d0c8a 인계][h81] · [d9ea545 결과][r81] | 여섯 악보 입력, 세 빌드, 18셀·36회 실행. E05의 원 출력과 별도 화면의 픽셀 기록 | 두 수정안이 일반 메뉴의 다음 편집 대상을 바꾸는지, 신고 설치판에서도 같은지 |
| 082 · web-pro | [1f8bf03 인계][h82] · [1f7a65f 결과][r82] | 222개 저장소 모집표, 요구 12자리, 한 링크·두 링크 안내 12안, 발행 기록 | 역사 시점에 두 약속을 함께 수행한 판, 대안의 실사용 비용과 성공 |
| 083 · web-pro | [f9be0da 인계][h83] · [a73aa21 결과][r83] | 핵심 6자리와 별도 보조층, 세 판의 문단, 두 연구 복사본의 정·역방향 수선 기록 | 같은 상류 함수를 실제로 사용한 하류의 동작, 필수 정정과 운영 오류율 |
| 084 · codex-cloud | [5705a5a 인계][h84] · [73195bd 결과][r84] | 고정 4요청×4셀, 48개의 축별 비교, 5개 이벤트 자리와 실행 원장 | 개설 시점 원문을 주었을 때의 답, 작성자가 성공한 정확한 환경 |

이 검토에서는 081의 종료값·저장 지문·E05의 시점별 flag와 목록, 082의 조건 출처·열람 문서 중복, 083의 핵심/보조 행·발행자 편집·역적용, 084의 판정·비교 가능 쌍을 고정 원장에서 다시 셌다. 실행 횟수는 해당 작업자가 남긴 관측이다. 이번 검토에서 확인한 범위는 저장된 출력과 원장의 재집계까지다. 080까지는 직전 REVIEW의 누적 판단을 사용했다. [081 원장][run81] · [082 판독][path82] · [083 후속판][rev83] · [084 대응쌍][pair84]

## 080까지의 결론과 이번 결과가 바꾼 부분

제품의 출발점은 사용자가 만들 소프트웨어의 전체 또는 일부 구조와 목적이다. 답은 곧바로 쓸 완성품·서비스, 가져다 붙일 기능, 설계나 시험에 옮길 타 분야 원리와 그 원문 링크다. 최종 설계자가 각 대안을 따로 채택·교체할 수 있게 조사한다. 자료집의 크기, 링크에 붙일 정보량, 수집·검증 시점, 시스템의 DB와 구현은 열린 결정이다. [제품 브리프][product] · [연구 운영 규칙][workflow]

| 설계 질문 | 080까지 이어진 실제 근거 | 081–084를 반영한 해석 |
| --- | --- | --- |
| 부분 요청에서 무엇을 더 물어야 하나? | 020은 주장 72/73을 전달했지만 충돌 완전 해소는 2/16이었다. 070의 자연 요청 24건에서는 한 답이 정오를 바꿨는지 독립 판정할 분모가 0이었다. 074의 구성 대조 4쌍은 조건 값을 주면 8/8에서 정답이 하나로 줄었지만 자연 요청 8건에서는 두 값의 정오를 함께 확인하지 못했다. | 준비된 것이 문서 원본인지 게시 가능한 HTML인지, 필요한 주소가 최신판인지 고정판인지에 따라 줄 링크나 다음 행동이 달라진다. 082의 P3는 원문이 이미 옛 계열도 요구한다. 그 사용자에게 같은 조건을 되물을 이유는 없다. [082 요구][req82] |
| 다른 분야의 원리가 선택이나 시험을 바꾸나? | 010은 분야 단서에서 원리군 7개를 찾았다. 033의 단서 없는 144쌍 중 넓은 의미의 지지는 1쌍, 당시판 지지는 0이었다. 069·073은 요청 접수와 말단 적용, 저장소 이전과 유지 책임 인수를 구별할 선례를 찾았다. 077의 보조 사례 3건 중 경쟁안은 2건에서 달랐지만 핵심 구현 선택 변화는 0/3, 목표 실행은 0/9였다. | 081은 077의 MuseScore 두 선택을 가르는 한 입력을 찾았다. 외부 원리의 유용성을 시험할 때 사용할 관측이다. 당시 개발자가 그 원전을 보고 선택을 바꿨다는 증거는 계속 비어 있다. [077의 보기별 선택][prev77] · [081 선택 경계][r81] |
| 설명을 더하면 결정과 재작업이 개선되나? | 021의 두 절 열람에서 공식 지지와 근거 회수는 주소만 6/23, 절 목록 9/23, 조건과 절을 연결하면 14/23, 잘못 연결하면 8/23이었다. 066에서는 같은 주소가 반대 권고에도 붙었다. 022의 결정 우선 24건에서 미인지→변경→시행을 모두 관측한 건은 0, 034에서 부분 시간 중앙값은 380→57초였지만 전체는 849→847초였다. 078은 두 합성 작업에서 NULL과 빈 문자열, 디렉터리 경로와 기존 ZIP 멤버 때문에 단독 성공이 결합 성공으로 이어지지 않는 경우를 실행했다. | 082는 같은 문제를 생성한 HTML·게시처·독자가 찾는 판으로 옮겼다. 한 사업자도 여러 단계를 맡을 수 있다. 12안에 대한 실제 대안 배포가 0건이므로 링크 수별 성공률·사람 시간은 산출 불가다. [078 결합 비교][prev78] · [082 발행 근거][pub82] |
| 과거 답과 현재 기능의 관계를 어디까지 복원할 수 있나? | 032의 배포 참조 12건은 유지 9·교체 2·보류 1이었다. 055는 과거 답 4/4까지 복원했지만 다음 판 판단은 0/4였다. 071은 실제 조각과 설정을 보관해 통제 22/22를 재계산했다. 075는 양성 존재 15/15를 복원했어도 유일·공동 1위는 각각 16/16 보류였다. 079의 G04에서 옛 GDAL은 새 struct 파일을 열고도 geometry와 CRS를 잃었고, 판 한정 별칭은 이를 되살리면서 bbox 속성 넷을 더했다. | 083에서 실제 GeoPandas 안내는 PyArrow를 불렀다. 포맷 이름이 같다는 이유로 GDAL의 무음 손실을 이 독자에게 적용할 근거가 없다. 자료를 복원하거나 안내 문구를 되돌릴 수 있는지와 그 권고의 정오는 별도로 판정해야 한다. [079 역사 관측][prev79] · [083 원 레코드][rec83] |
| 검색 범위를 넓히면 쓸 수 있는 기능이 늘어나나? | 060·064·068은 기능명이나 첫 절을 개선해도 두 조건을 함께 지지하는 근거가 자주 비었다. 072의 자연 직접 적격 분모는 0이었다. 076은 자연 6요구×20후보의 직접 양성 0, 교정 직접 양성 5쌍은 세 표시 방식 모두 5/5 회수했다. 080은 참조판에서 좁은 목록의 알려진 비양성이 넓은 목록의 양성으로 바뀐 경우를 비교 가능한 자연 1/5·교정 3/5에서 봤다. 엄격한 개설 본문 기준 48셀은 모두 미확인이었다. | 084의 선택된 네 요청에서는 같은 최초 확보본과 같은 참조판을 두고 범위를 넓히면 3건은 양성, 1건은 기본 조합에 대한 반박을 얻었다. 넓은 원문은 가능한 방법과 피할 방법을 모두 알려 줄 수 있다. 최초 게시 당시의 실제 사용판에서의 회복 효과는 미확인이다. [080 범위와 판][prev80] · [084 셀][cell84] |

앞 표의 과거 숫자는 각 작업의 원래 모집층과 비교 단위를 유지했다. 080의 48셀 중 네 사례를 골라 다시 본 084의 16셀, 077의 MuseScore 한 사례를 이어받은 081을 새로운 독립 표본으로 합산하면 효과를 부풀리게 된다. [직전 누적 검토][prev] · [084 분모][met84]

## 새 연구 네 건의 수용 범위

### 081 · 선택색, 선택 목록, 다음 편집은 다른 관측이다

역사 병합의 첫 부모 한 판에서 원본 U, 모든 요소 복사 때 선택 비트를 지우는 병합안 G, 새 파트에 한해 지우는 연구안 L을 비교했다. U에서는 새 플루트 파트에서 Inspector가 비어 있는데도 음표가 파랬다. 별도 GUI 두 반복의 플루트 청색 픽셀은 U 65·65, G와 L은 각각 0·0이었다. G/L이 같았던 고정 입력은 5/6이다. 유일하게 달랐던 E05에서는 비링크 성부 복제 직후와 명령 종료 뒤 모두 G의 복제음은 flag=0·목록 밖, L은 flag=1·목록 밖이었다. 원음은 양쪽 모두 선택 목록에 남았다. 재열기 뒤에는 복제음 차이가 사라졌고 여섯 입력 모두 같은 입력 내 세 빌드의 저장 지문이 같았다. [E05 G 원 출력][g81] · [E05 L 원 출력][l81] · [화면 판독][pix81]

부족한 곳은 **그 차이가 사용자가 메뉴를 누른 뒤에도 남아 다음 편집을 바꾸는지**다. 실제 화면을 확인한 조작은 새 파트 생성이고, E05는 `cloneVoice`를 직접 호출했다. E06은 비트를 끄고도 재생 표시용 mark만으로 선택색을 냈다. 알려진 원 시험 21/21 통과와 화면색 모두 후속 편집 대상의 정답을 주지 않는다. 공식 신고 최초 리비전과 원 설치물도 미확인이다. “전역안이 이 복제의 잔류 비트를 제거한다”는 지지되며, “모든 사용 상황에서 더 낫다”는 보류한다. [사례와 사전 예상][case81] · [검산 영수증][verify81] · [당시 병합 논의][mspr]

### 082 · 생성된 파일, 출판자가 보고한 성공, 독자에게 간 판

Python 3프로젝트에서 선택 소스의 HTML 생성 성공 로그를, R 3프로젝트에서는 선택 소스와 연결된 생성 HTML 커밋을 확보했다. R2와 R3의 대표 HTML은 각각 두 파일이 현재 응답과 바이트 단위로 같았다. 전체 6개 주소가 현재 열렸으나 선정 판을 식별한 자리는 3/6이었다. 요구 출처 12칸 중 확인은 7칸이고, 두 조건을 각각 실제 문구로 약속한 곳은 cibuildwheel(P3) 한 곳이다. P3는 현재 지원판과 옛 Python 사용자용 1.x를 나눠 안내했다. R1은 게시하려는 HTML이 이미 준비된 경우와 패키지 원본만 있는 경우에 따라 다음에 필요한 링크가 달라진다. [요구 원장][req82] · [발행 기록][pub82] · [반환 예시][cards82]

출처 원장은 201행이다. A/B 열람은 12안×2문서였으나 고유 문서는 6개이고 재사용은 18회다. P3의 두 태그 빌드와 현재 1.x 응답을 잇는 당시 동시 공개 증거는 0/1이다. R의 최종 Pages 성공은 확인 0/3·미확인 3이며 R1에 배포 객체가 1개 있었다. 이 결손은 과거 배포 실패 횟수를 뜻하지 않는다. 또 P3에서 Sphinx 조립안에는 기존 MkDocs의 플러그인·탐색 경로를 넘기는 계약이 비었다. 동일 조사자의 기술적 안내만으로 두 링크가 사람의 성공률을 올렸다고 단정할 수 없다. [A/B 판독 행][path82] · [집계와 적용 한계][cnt82]

### 083 · 실제로 고친 문구와 동작상 꼭 고쳐야 할 문구

핵심 6자리 중 실제 안내는 2개였다. 둘 다 GeoPandas 0.14.4의 같은 I/O 가이드에 있었고 정확한 GDAL GEOARROW 호출 노출은 0/2였다. 원본·첫 후속·최신판에서 발행자는 한 문단의 메서드 참조를 구체화했고, 다른 문단에서는 금방 낡는 명시 버전 문구를 일반화했다. 수선안 A는 두 건을 보류했고, B는 기존 WKB 왕복 안내를 유지하고 옛 “any version” 문구에는 적용판·인코딩 주석을 붙이자고 했다. 연구 복사본 두 개는 정·역방향 적용으로 옛 바이트와 판정을 복구했다. [버전별 문단과 수정 이유][rev83] · [역적용 영수증][roll83]

같은 가이드 두 문단을 독립 피해 사례 두 건으로 세거나 실제 배포자의 편집을 정답으로 놓으면 두 수선안의 우열이 만들어진다. 원 소비 환경의 설치 근거와 새 기능 실행은 각각 0, A/B 정오 비교 가능 행은 0이어서 오류율은 0/0·산출 불가다. O02 핵심 세 자리는 모두 비었지만 보조층에는 GAM 가이드와 내부 SciPy 이관이 있다. Astropy의 옛 시험을 지운 병합은 SciPy 1.6 발행보다 앞섰다. 이름 검색의 공석을 생태계 전체의 부재로, 후속 삭제를 해당 상류 변경의 결과로 읽을 수 없다. 타 분야 정정·전거 5사건 중 역사 전후 바이트까지 직접 비교한 것은 1건이다. [핵심과 보조층][rec83] · [판정 분모][den83] · [Astropy 당시 병합][astro]

### 084 · 원문에서 쓸 답을 찾는 일과 원 작성자가 쓴 답을 확인하는 일

네 요청×네 셀을 다시 세면 최초 확보본 기준 양성 3, 반박 2, 해당 범위에 미등재 5, 미확인 6이다. 판독 가능한 10셀 모두 080과 일치한다. 입력판 대비 16쌍은 전부 비교 불가, 확보본에서 소비판만 바꾼 8쌍은 2쌍만 비교 가능하고 변화는 0/2였다. Click의 CN01은 두 판에서 기본 prompt·multiple 조합이 한 줄의 두 이름을 거부한 반면 명령 안에서 명시적으로 분해하면 두 이름이 전달됐다. CLI에 실제 stdin을 준 시험과 처음 CliRunner에서 25초 멈춘 기록도 구별했다. [16셀][cell84] · [48쌍][pair84] · [입력 보정][err84]

attrs AC01에서 작성자는 일반 훅과 `slots=False`가 작동했다고 했지만 예제에서 한 키만 조회했다. 연구자가 재구성한 21.4.0에서는 훅이 두 번 불려도 `int`가 IntRange를 가리키고 `int-range`는 없었다. 후대 참조판에서 두 키를 보존한 것은 전용 훅이었다. 동시대 작성자의 보고와 연구 결과는 판·구성·검사한 키가 달라 보편적 성공/실패를 가를 수 없다. 10개 새 프로세스의 결과가 예상과 맞았지만 개설 본문은 0/4, 편집 대조의 개설 본문은 0/1, 교정 작성자의 정확한 성공판은 0/2였다. 시간 파일 접근 실패와 현재 본문 지문 일치는 최초 본문을 증명하지 못한다. [실행자와 출력][run84] · [이벤트 원장][ev84] · [작성자 보고][attrs]

## 불일치가 바꾸는 판단

| 함께 읽어야 할 결과 | 한쪽을 다른 쪽에 적용하면 생기는 잘못 | 판정을 바꿀 최소 관측 |
| --- | --- | --- |
| 077의 두 판독은 지역 수정을 골랐고 실제 병합은 전역 수정이었다. 081에서는 파트 생성 결과가 같았고 비링크 복제에서만 갈렸다. | 구현 선택이 달랐다는 이유로 파트 요구의 성공까지 달랐다고 할 수 없다. 색만 보면 재생 mark도 선택으로 잘못 읽는다. | 같은 사용자 메뉴에서 복제 직후, 재선택 뒤, 다음 편집 뒤의 대상 ID와 저장값을 잇는다. |
| 078의 결합 성공과 082의 한 서비스 안내, 079의 GDAL 손실과 083의 GeoPandas 유지 제안 | 한 서비스가 두 단계를 맡을 수 있고, 같은 포맷도 호출자가 다를 수 있다. 링크 수·주소·포맷명은 단독으로 종단의 약속을 확정하지 못한다. | 서비스에는 판이 식별되는 당시 응답을, 라이브러리에는 두 소비판에서 읽은 동일 파일의 geometry·CRS·속성을 붙인다. |
| 076의 자연 직접 양성 0, 080의 범위 확대 회복, 084의 참조판 3양성·1반박 | 모집층과 목록판이 다르다. 넓은 문서에서 다른 해법을 찾았다는 사실을 당시 작성자의 채택으로 셀 수 없다. | 같은 요청의 이력이 공개된 두 리비전에서 후보와 매뉴얼판을 고정하고, 요구·기능 적합·작성자 후속 행동을 따로 읽는다. |

## 다음 네 작업

| ID · 담당 | 물려받을 고정 인계 | 끝나면 설계자가 결정할 수 있는 것 |
| --- | --- | --- |
| 085 · codex-cloud | [081][h81] | MuseScore의 실제 메뉴에서 표시와 다음 편집 중 무엇이 달라지는지 확인해 공통 복사 수정의 적용 범위를 정한다. |
| 086 · web-pro | [082][h82] | cibuildwheel과 R archive의 과거 게시 기록 및 두 대조 자리를 보고 최신 별칭·고정판·생성 파일 중 무엇을 어떤 조건으로 보여 줄지 정한다. |
| 087 · codex-cloud | [083][h83] | 같은 네 파일을 GeoPandas 두 판에서 읽고, 옛 안내의 적용 범위와 새 인코딩에서 필요한 조건을 정한다. |
| 088 · web-pro | [084][h84] | jq·Pandoc 질문의 두 공개 리비전으로 같은 후보를 평가해 입력을 보존하거나 다시 물을 조건을 찾는다. |

네 작업은 각각 완료된 선행판 하나와 공개 원자료로 시작한다. 088은 두 회차에서 확보하지 못한 GitHub 개설 시각의 본문을 다시 구하는 대신 리비전이 공개된 별도 표본에서 **공개된 판 사이의 변화**를 측정하도록 설계했다. 080·084의 빈칸은 그대로 남는다. 배정 JSON에는 각 작업의 모집 단위, 필수 표, 직접 열람할 원자료, 반례, 중간 커밋과 인계 전에 재계산할 분모가 들어 있다. [다음 작업 지시문](NEXT_TASKS-21.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/07e0f4082847641d216cec5cfcd1ad9e198f85b9/docs/workstreams/planning/REVIEW-20.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/e7a777f2c13b626532b5828591d6388743688b34/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/184137d2f257f5d1a7ef584e0f3a6b35f3d280cd/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/184137d2f257f5d1a7ef584e0f3a6b35f3d280cd/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/184137d2f257f5d1a7ef584e0f3a6b35f3d280cd/docs/RESEARCH_WORKFLOW.md
[mspr]: https://github.com/musescore/MuseScore/pull/4590
[astro]: https://github.com/astropy/astropy/pull/10972
[attrs]: https://github.com/python-attrs/attrs/issues/971#issuecomment-1159394251
[h81]: https://github.com/laadkke-arch/agentflow-open/blob/60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc/docs/workstreams/research/AF-RES-081/HANDOFF.md
[r81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/RESULT.md
[h82]: https://github.com/laadkke-arch/agentflow-open/blob/1f8bf039ad4f9a38b99764a11f72b515facef39c/docs/workstreams/research/AF-RES-082/HANDOFF.md
[r82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/RESULT.md
[h83]: https://github.com/laadkke-arch/agentflow-open/blob/f9be0dacdb51603c72f30abd452ce9d349d0ca3b/docs/workstreams/research/AF-RES-083/HANDOFF.md
[r83]: https://github.com/laadkke-arch/agentflow-open/blob/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/RESULT.md
[h84]: https://github.com/laadkke-arch/agentflow-open/blob/5705a5a00f07af0f0048237cfa9ba6673fd3e91d/docs/workstreams/research/AF-RES-084/HANDOFF.md
[r84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/RESULT.md
[run81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/runs.jsonl
[g81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/evidence/runs/14-E05-G/r1/stdout.jsonl
[l81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/evidence/runs/15-E05-L/r1/stdout.jsonl
[pix81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/evidence/desktop-pixels.json
[case81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/cases.csv
[verify81]: https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/evidence/verify.json
[req82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/requirements.csv
[path82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/paths.csv
[pub82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/deployments.jsonl
[cnt82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/evidence/outcome-counts.json
[cards82]: https://github.com/laadkke-arch/agentflow-open/blob/1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41/docs/workstreams/research/AF-RES-082/cards.md
[rec83]: https://github.com/laadkke-arch/agentflow-open/blob/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/records.jsonl
[rev83]: https://github.com/laadkke-arch/agentflow-open/blob/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/revisions.csv
[roll83]: https://github.com/laadkke-arch/agentflow-open/blob/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/evidence/rollback-receipt.json
[den83]: https://github.com/laadkke-arch/agentflow-open/blob/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/evidence/denominators.json
[cell84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/cells.csv
[pair84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/pairs.csv
[run84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/runs.jsonl
[ev84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/events.jsonl
[met84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/metrics.json
[err84]: https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/evidence/fixture-correction.md
[prev77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/VIEWS.csv
[prev78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/comparisons.csv
[prev79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/streams/gis/historical/observations.jsonl
[prev80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/matches.csv
