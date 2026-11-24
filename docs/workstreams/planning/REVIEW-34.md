# REVIEW-34 · 기능 링크가 선택에 도움이 됐다고 말할 수 있는 조건

사용자가 찾는 것은 지금 설계 중인 부분에 가져다 쓸 수 있는 기능과 원리, 그리고 그 판단을 확인할 링크다. 이번에 가장 분명하게 답을 바꾼 증거는 배포판의 실행 결과였다. d3-scale에서 같은 문서 절을 둔 채 `null`의 반환값이 바뀌었다. 같은 작성자가 제안을 받아 변경한 증거도 한 건 복원됐지만, 그 제안은 링크 없이 이름으로 전달됐고 바뀐 것은 의존성 선언이었다. 추천 링크 덕분에 최초 작성자가 재작업을 줄였다는 주장은 여전히 미확인이다. [실행 전후 원장][outputs] · [제안·응답·수정 원장][ev133]

## 검토 기준과 새 자료

2026-11-24 UTC 기준이다. `work/planning@f3fd4a8`의 최신 REVIEW-33을 먼저 읽고, 이전 검토가 쓴 통합판 `42260ca`와 현재 `1d65b0b`의 진행표를 ID별로 대조했다. 종전 130행은 모든 필드가 같다. 추가된 네 행은 모두 DONE이다. 현재 전체 134행은 **DONE 132, BLOCKED 2**이며, 연구 132건만 세면 DONE 130과 BLOCKED 2(018·035)다. 나머지 DONE 2건은 연결 시험이다. 중앙 DONE 132행 모두 `acceptance_evidence`가 비어 있다. 각 작업의 실질 완료 범위는 해당 브랜치의 인계·결과·원장으로 판독했다. [33차 누적 검토][prev] · [이전 진행표][old] · [현재 진행표][reg]

| 새 DONE | 등록된 인계판 · 작업자 상태 | 결과 본문판 | 이번에 고정 원장에서 대조한 단위 |
| --- | --- | --- | --- |
| 133 · 코드 리뷰 제안의 귀속 | [b84d3a1 · PARTIAL][h133] | [957fffb][r133] | PR 72, 사건 15, 계약 15행, 출처 108행 중 최소량에 든 고유 저작 35 |
| 134 · 한국어 별칭과 표시 | [a214140 · PARTIAL][h134] | [6a17cf5][r134] | 새 자연 질문 6, 질문×카드 96쌍, 정책별 순위 288행, 출처 186행 중 고유 저작 38 |
| 135 · 기능 링크의 재확인 시점 | [880833d · PARTIAL][h135] | [a6a52f7][r135] | 배포판 91개(지도 64, 축척 27), 축척 26인접쌍, 정책 비용 48행, 출처 48행 중 고유 저작 32 |
| 136 · 답과 추가 원문의 재판독 | [547b592 · PARTIAL][h136] | [a081ca3][r136] | 요청 33절, 답 18개, 근거 연결 원장 22행, 대조 39행, 적격 고유 저작 25(구현 계보를 더 합치면 24) |

조회 당시 네 작업 브랜치의 head는 등록된 인계 SHA와 각각 일치했다. 네 RESULT.md의 Git blob도 표의 별도 결과판과 각각 같았다. 이번 검토는 이 파일과 원장을 다시 읽고 집계한 것이다. 원 저자의 발언은 발언 기록으로, 실행값은 작업자가 남긴 실행·재생 기록으로 평가했다. 134·135에는 지정 checkout 검사의 종료 0 영수증이 있고, 133·136은 웹에서 고정판을 검산했다. 브라우저·패키지 실행과 새 독서 실험은 각 작업자가 남긴 범위까지 인용했다. [133 검사 범위][check133] · [134 검사][check134] · [135 검사][check135] · [136 재집계][check136]

## 1~33차에서 이어 온 제품 판단

| 설계자가 결정할 질문 | 지금까지의 근거와 이번에 달라진 범위 | 아직 결정할 수 없는 것 |
| --- | --- | --- |
| 다른 분야의 선례를 찾아주면 실제 선택이 바뀌는가 | 010은 분야 단서로 원리 7군을 찾았다. 단서가 없는 033의 144쌍에서는 넓은 지지 1건, 당시판 지지 0건이었다. 022의 미인지→변경→시행은 0/24였다. 109의 시험 제안 27건과 117·121·125·129의 추적에서도 원저자의 늦은 발견과 현장 노동을 잇지 못했다. 129의 NetworkX #8201에서 비순환 경로만 교체됐다. 표준 기능은 최초 구현 뒤에 나왔고 나중에 배웠다고 밝힌 사람은 리뷰어였다. 133에서도 제안의 화자와 수정자가 갈렸다. | 새 시험이나 대안의 발견, 실제 채택, 절약한 사람 시간을 각각 입증해야 한다. |
| 부분 입력에서 어떤 주변 정보를 받을 것인가 | 020은 주장 72/73을 전달했으나 충돌을 다 푼 사례는 2/16이었다. 074의 구성 입력은 추가값으로 8/8 구별됐지만 111의 동의어 변경 뒤 정합은 두 방식 모두 0/6이었다. 119의 자연 도표 6건에서 원요구만으로 정확 0, 인접 기록·직접 참조로 각각 3이었다. 123은 같은 x에서 1px 끌어도 시작 대상에 따라 다른 달이 선택됨을 측정했다. 134에서는 다중 작업자를 꼭 유지할지가 직접 후보 하나의 지위를 바꾼다. | 작성자가 실제로 허용한 값과 연구자가 놓은 두 가정을 구별해야 한다. 질문 한 번의 시간 절감은 미측정이다. |
| 조사 후보 중 무엇을 보여 줄 것인가 | 076의 자연 6요구×20후보는 직접 적격 0, 자료집을 넓힌 080은 자연 1/5·교정 3/5였다. 118에서 표시 직접·일부·충돌은 9·7·15에서 8·0·0으로 줄었다. 122의 자연 진단 10건에 16카드로 완전한 답은 없었다. 126은 공개 10건 별칭 적중 0, 구성한 표현에서는 조사 허용이 직접 3개와 충돌 1개를 함께 들였다. 130은 포럼 첫 글 1건과 적격 기술 원전 7저작에 그쳤다. 134에서 확보한 새 GitHub 6건에도 활성 별칭은 없었다. | 이름 확장의 효과를 보려면 별칭을 실제 쓴 자연 질문이 필요하다. 표시 공석·오표시 감소와 유용한 링크 손실도 함께 세야 한다. |
| 어떤 자료를 보관하고 언제 링크를 다시 열 것인가 | 055는 옛 판단 4/4, 다음 판 판단 0/4를 복원했다. 071은 원문 구간과 설정으로 옛 자료 22/22를 복원했고, 075는 전체 후보가 없어 유일·공동 1위 주장을 각각 16/16 보류했다. 106은 살아 있는 주소에서 옛 예제의 쓰임이 사라지는 사례를 찾았다. 121은 실제 읽은 판 6/6 미확인이었다. 131은 지도 옵션 계약의 경계를 찾았고, 135는 기능 절·구현을 확인하는 비용과 놓침을 입력별로 셌다. | 같은 판의 옛 설명 복원, 현재 입력과의 호환, 후보 전체에 대한 최선 주장은 보관해야 할 근거가 다르다. 일괄·요청 시 검증의 운영 비용은 배포 빈도와 실제 질의에 달려 있다. |
| 원문을 하나 더 주면 무엇이 달라지는가 | 021의 두 절 예산에서 근거 충분은 주소만 6/23, 절 목록 9/23, 맞춘 절 14/23, 잘못 붙인 절 8/23이었다. 034의 부분 시간은 380→57초, 전체는 849→847초였다. 116·120은 후속 정의에 가는 경로를 보였고 124의 추가 시험 후 핵심 처방 수정은 0/6이었다. 128에서 이전 주분류와 일치한 답은 9/18이었다. 132의 독자 한 명이 둘째 면에서 조건부 후보 한 개를 추가했고 136은 그 후보에 필요한 도구 제약과 채점의 한계를 대조했다. | 저자의 수락, 사람의 총 시간, 링크 하나 추가의 평균 효과는 확인되지 않았다. 새 원문이 도구 사용 허용 같은 당사자의 조건을 알려 줄 수 있는지도 따로 판단해야 한다. |
| 다른 부품과 조합하거나 일부만 편집해도 무엇을 보존하는가 | 078은 개별 기능의 결합 실패, 103은 외관 10/10 보존과 8자리 텍스트 선택 소실, 107은 단일 발생 편집에서 공유 정의 0/6·위치 지정 6/6을 보였다. 119·123은 차트의 로컬·공유 상태를 나눴다. 127은 처리 순서에 따라 피처와 지도 중심이 함께 움직였고 131은 순서를 고정했을 때 6.6.1→6.7.0에서 움직이는 대상이 바뀜을 확인했다. 135가 이어받은 지도 실측은 같은 네 판이다. | 복수 피처, 다른 렌더러, 원 저자의 앱에 적용하려면 해당 입력과 보존값을 직접 확인해야 한다. |

누적 수치의 근거 위치는 REVIEW-33에 있다. 별도 정정 두 건도 유지한다. 114의 ‘충돌’ 138/144를 118의 명시 반박 기준으로 읽으면 충돌 7, 미확인 131이며 남은 6은 일부다. 119의 M3994 원형 MG 좌표 y는 11.71875이고 공유 변경 뒤 y는 275다. 연구 기록의 열을 제품 DB의 필드로 채택할지, AI 전처리·상시 수집·AgentFlow 입력 계약이 필요한지는 열려 있다. [누적 근거와 정정][prev] · [제품 목표][goal] · [연구 규칙][wf]

## 새 DONE에서 확인한 것과 근거가 끊긴 곳

### 133 · 같은 작성자의 수정을 입증한 가장 강한 사례에는 링크가 없었다

xarray 본창 24, scikit-image 본창 24, xarray 보충 24에서 PR 72개의 통합 대화 응답을 받았다. 댓글 수 필드 합은 1,043이다. #9618은 반환된 371개 중 앞쪽 비어 있지 않은 댓글 18개를 판독했고, 전체 스레드의 끝까지 확인한 PR은 입증된 것이 없다. 15사건 중 제안 전 부모·첫 수정·병합 코드·같은 작성자 답을 연결한 한 건은 scikit-image #7579다. 병렬 빌드는 먼저 선택됐고 이름 제안 후 의존성 선언이 바뀌었다. xarray #9589의 내부 파서 교체에는 작성자 답과 병합 코드가 있지만 최초 수정 SHA는 미확인이다. 두 사례 모두 링크 전달의 효과를 입증하는 분모에 넣을 수 없다. [PR 모집][frame133] · [사건별 판정][ev133] · [#7579의 제안][pr7579] · [#9589 응답][pr9589]

#7576은 반환형을 경고한 링크 뒤 다른 유지보수자가 기존 matrix 기본값과 array 선택지를 제안했고 병합 코드에 둘 다 남았다. #7575의 대체 PR은 링크보다 약 21시간 반 먼저 열렸고 작성자도 달랐다. #7589에서는 Poisson 설명을 고쳤다는 응답과 최종 문서의 다른 링크가 확인되며 해당 호출은 이미 있었다. 따라서 관찰한 사건에서 **링크를 받은 동일 작성자의 런타임 변경을 직접 귀속한 건수는 0**이고, 모집창 전체의 엄격 적격 링크 수·채택률·노동시간은 미확인이다. 영국 통계청 정정 사례에서도 G7G6의 480→479(천 명)는 판 사이의 차이이고 즉시 정정판과 제보자는 미확인이다. 제보 기관이 표시된 다른 공지에는 여러 수정이 함께 반영됐다. [계약 원장][contracts] · [코드·정정 원표 대조][corrections]

### 134 · 증거가 부족한 카드를 숨기자 조건부로 유용한 링크도 사라졌다

포럼 ID 64개에서 JSON 원 서버 응답은 확보하지 못했다. HTML로 읽은 첫 글 하나는 홍보였고 나머지 63개와 네 사이트 검색의 32자리는 미확인이다. 별도 GitHub 창에서는 첫 본문 68슬롯(22+24+22), 고유 URL 66개, 재게시를 합친 원문 63계보에서 적격 질문 6건·6저자를 골랐다. 목표 8저자에는 못 미쳤다. 같은 16카드의 96쌍을 전수 판독한 기준은 직접 1·일부 1·충돌 3·미확인 91이었다. 완전 어절(B)과 끝조사 하나 허용(C)은 적격 원문에 활성 별칭 적중이 없어 조사·표시 순위가 전부 같았다. 제외한 글의 ‘가중치를’는 체크포인트를 가리켰다. 가중 표본 인덱스를 내는 카드와의 어휘 일치를 적격 요청의 회복으로 세면 지표가 바뀐다. [모집·분모][count134] · [전수 기준][truth] · [적중 원장][alias]

C에서 원문 출력 근거를 요구하는 Gate로 바꾸자 조사 상위 8은 유지됐다. 표시에서는 원래 18자리 중 비었던 9자리와 더불어, 직접 1·일부 1·충돌 1·미확인 6의 아홉 쌍이 모두 빠졌다. 원절 28개 검토 후 **18/18자리가 공석**이었다. HDF5 배치 질문에서 D07이 내는 인덱스 목록은 요구한 표본 배치와 다르다. 반면 D01은 단일 프로세스를 허용하면 직접 후보이고 병렬성을 꼭 유지해야 하면 일부다. 두 해석 중 저자가 택한 값, Windows에서 원 문제가 풀렸는지, 실제 독자의 클릭·선택은 미확인이다. 같은 판독자가 표시 기준과 전수 기준을 작성했다. 철도에서는 같은 ‘23 St’가 다른 역 ID를, 서지에서는 같은 보들레르 전거가 저자·번역자·주제를 가리켰다. 대상 식별과 현재 역할을 함께 봐야 한다는 사례다. [표시 이동 9쌍][moves] · [원저자 질문][hdf] · [역·전거 대조][role134]

### 135 · 문서 절은 출력 변화를 놓쳤고 넓은 구현 지문은 거의 매번 경보했다

d3-scale 정식 27판·26인접쌍을 14개 입력 셀에서 비교했다. 두 깨끗한 설치 경로에서 각각 79회(기본 27판과 공유 직접 의존을 맞춘 26쌍×2판) 실행했고 대응 벡터 불일치가 없었다. 2.1.2→2.2.0은 6/14셀, 3.2.3→3.2.4는 2/14셀이 변했다. 뒤 경계에서 기본 `null`은 숫자 0→`undefined`, 지정 결측값을 쓸 때는 0→지정값이었다. 그 경계의 README는 바이트가 같고 별도 릴리스 공지는 변경을 알렸다. 수치·clamp·invert 7셀은 26쌍 내내 같았다. [출력 대조][outputs] · [두 실행 영수증][replay135] · [3.2.4 공지][d3note]

135는 알려진 지도 경계에서 신호를 정하고 축척 출력 실행 전에 예측을 봉인했다. 주소·제목만 보는 안은 축척 전환 두 쌍을 모두 놓쳤다. 문서 절 신호 C는 26쌍 중 실제 변화 1·불필요한 경보 5·놓침 1·맞게 생략 19였고, 구현·직접 의존까지 본 D는 2·23·0·1이었다. 최신판을 차례로 요청한 27회 모형에서 C는 22회 올바른 값을 이월하거나 실측했고 5회 틀렸다. D는 27회 모두 맞았지만 매번 실행하는 안보다 줄인 실행은 1회이고 해시 입력 344파일·3,522,075바이트를 읽었다. 이는 저장된 판과 질의열에서 계산한 비용이다. 실제 운영 트래픽·사람 시간은 미측정이다. 지도는 소스 64판 중 63쌍에 계약 변화 1쌍이었으나 양끝 모두 브라우저로 비교한 인접쌍은 **1/63**이다. 135는 131의 실측을 이어 썼다. Vienna 두 도엽은 목록에서 조사·인쇄 연도만 확인했고 원면은 0/2였다. 페리 휴일표의 06:10은 공지가 가리킨 표의 값으로, 해당 날짜의 직접 화면과 실제 운항은 미확인이다. [신호][signals] · [질의별 비용][cost135] · [타 분야 관측 경계][other135]

### 136 · 두 판독에서 핵심 해결은 유보됐고 후반 채점에는 선노출이 있었다

132가 보존한 6사건×3답을 다른 대화의 판독자가 읽었다. 1차의 문장상 ‘처방 제안 충족’ 3개는 모두 J3 한 사건의 세 단계 답이다. 나머지는 조건부 12, 불명 3이다. 최종 핵심 해결은 여섯 사건 모두 유보였다. 첫 면 뒤에서 최종 답까지의 주분류는 좁은 근거 보강 3, 검사 구체화 1, 조건부 대안 1, 유지 1이다. 조건부 대안은 J2의 fq로, 작성자는 나중에 도구를 추가하고 싶지 않다고 밝혔다. 검사 구체화는 둘째 면을 주지 않은 P3에서도 나왔다. J3의 `sub`를 새 대안으로 분류하면 보강 2·대안 2가 된다. 주장 21개 중 19는 문장상 동의, 2는 부분 동의였다. [가림 판독][rating] · [주장·전환 대조][conc] · [당사자 후속 발언][jq]

원 독자의 실제 열람 이벤트 10회, 고유 본문 9개, 답에 근거 면을 연결한 16쌍은 서로 다른 수다. 2차 예비 결합이 뒤 단계의 면을 먼저 보여 줬다. 최종 표는 답 봉인 전의 열람 이벤트만 다시 연결했지만 판독자가 본 것을 지울 수 없다. 봉인 설명의 ‘고유 8면’은 구조 필드·본문 해시에 따라 **9면**으로 정정한다. 서로 닮은 답을 이미 알아본 12/18을 제외하면 사건당 첫 답만 남아 비교 가능한 단계쌍은 0이다. J1은 같은 명령을 두고도 판정 문턱이 달라졌다. 여섯 이슈와 댓글 19개의 판독에서 후속 요구를 찾았다. 댓글 원장에는 주소와 본문 해시는 있지만 최초 공개·편집 시각과 실제 채택 근거는 미확인이다. Darwin 1872년판은 전사로만 대조했고, Schumann의 동일 편곡 총보와 A·B♭ 파트는 같은 진입·실음을 보존하면서 기보음이 달랐다. 서로 다른 편성 원전은 확보하지 못했다. [근거 연결][support] · [봉인 기록][seal] · [검산][check136] · [타 분야와 한계][r136]

## 다음 작업 네 건

| 독립 작업 · 담당 | 이미 고정된 선행 | 이번 질문을 닫을 관측 | 제품에 남길 선택 |
| --- | --- | --- | --- |
| 137 · codex-cloud | 133 | 기존 8개 PR의 전 스레드·원래 diff·최초 변경을 연결한다. 링크 후 수정과 이름만의 채택·선행 수정·다른 수정자를 동일 단위로 검사한다. | 확인된 변경에만 공로를 붙이고, 관련 근거만 있는 경우 누구에게 어떤 링크를 줄지 표시한다. |
| 138 · codex-cloud | 134 | 실제 한국어 조사 결합이 있는 표본과 중립 표본을 분리해 같은 16카드를 재생한다. 최대 한 장의 조건부 표시가 회복한 직접 후보와 새 충돌을 같이 센다. | 확정 링크·조건부 링크·공석을 가를 조건과 판독 비용을 남긴다. |
| 139 · codex-cloud | 135 | 별도 수치 패키지의 배포 노트와 해당 함수·위임 함수의 변경으로 재확인할 판을 먼저 고르고, 고정 입력 출력과 확인 비용을 대조한다. | 입력별로 직접 검증·이월·재확인할 근거와 비용을 비교한다. |
| 140 · web-pro | 136 | 새 공개 CSV·YAML 요청에서 두 번째 기술 원문으로 알 수 있는 조건과 원저자의 답이 있어야 알 수 있는 조건을, 후속 대화를 보기 전에 구분하고 대조한다. | 링크 하나, 추가 원문 한 개, 질문 한 개, 보류 중 어떤 응답이 정당한지 사례와 반례를 남긴다. |

137은 범위를 줄여 실제 귀속을 깊게 확인하고, 138은 어휘가 작동할 기회가 있는 독립 표본을 만든다. 139는 알려진 경계를 설명한 규칙을 다른 패키지에서 시험한다. 140은 같은 18답을 다시 채점하는 비용을 새 원저자의 요구를 확인하는 데 쓴다. 각 작업은 이미 저장된 선행 한 건으로 시작할 수 있다. [34차 작업자 지시문](NEXT_TASKS-34.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/f3fd4a89c61328592b6e094a62faff0bc2f95bb2/docs/workstreams/planning/REVIEW-33.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/42260ca230e028e1303667be943b861a1d5953e4/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/1d65b0b7aaef85350df8842dfc05a6be69148b38/docs/automation/dot-control.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/1d65b0b7aaef85350df8842dfc05a6be69148b38/docs/product/RESEARCH_BRIEF.md
[wf]: https://github.com/laadkke-arch/agentflow-open/blob/1d65b0b7aaef85350df8842dfc05a6be69148b38/docs/RESEARCH_WORKFLOW.md
[h133]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/HANDOFF.md
[r133]: https://github.com/laadkke-arch/agentflow-open/blob/957fffbe6991cef2c5b78f792bd5ea603b1139cd/docs/workstreams/research/AF-RES-133/RESULT.md
[h134]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/HANDOFF.md
[r134]: https://github.com/laadkke-arch/agentflow-open/blob/6a17cf5265e6f13155407c3785906b048982a12f/docs/workstreams/research/AF-RES-134/RESULT.md
[h135]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/HANDOFF.md
[r135]: https://github.com/laadkke-arch/agentflow-open/blob/a6a52f73843d8340024cdefb9c6cba7b0b73621c/docs/workstreams/research/AF-RES-135/RESULT.md
[h136]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/HANDOFF.md
[r136]: https://github.com/laadkke-arch/agentflow-open/blob/a081ca3d619c6aa6676cd1ec9d8e8a33bb739ebb/docs/workstreams/research/AF-RES-136/RESULT.md
[ev133]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/events.jsonl
[frame133]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/frame.csv
[contracts]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/contracts.csv
[corrections]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/evidence/hunks-and-corrections.md
[check133]: https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/evidence/remote-check.md
[pr7579]: https://github.com/scikit-image/scikit-image/pull/7579#discussion_r1797237861
[pr9589]: https://github.com/pydata/xarray/pull/9589#discussion_r1795004788
[count134]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/recount.json
[truth]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/truth.csv
[alias]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/alias-audit.csv
[moves]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/transitions.csv
[hdf]: https://github.com/HwangToeMat/VDSR_Pytorch_HTM/issues/1#issue-714769321
[role134]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/domain-identities.csv
[check134]: https://github.com/laadkke-arch/agentflow-open/blob/a21414017323dbd7a090b1e7b62f070d4fa1a1ab/docs/workstreams/research/AF-RES-134/evidence/session-check.json
[outputs]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/evidence/output-comparison.csv
[replay135]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/evidence/replay.json
[signals]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/signals.csv
[cost135]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/evidence/costs.csv
[other135]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/evidence/cross-domain.md
[check135]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/evidence/acceptance.json
[d3note]: https://github.com/d3/d3-scale/releases/tag/v3.2.4
[rating]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/blind-ratings.jsonl
[support]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/support.csv
[conc]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/concordance.csv
[seal]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/evidence/second-seal.json
[check136]: https://github.com/laadkke-arch/agentflow-open/blob/547b59212c164c904705ed0abea46f8e9a7d4a02/docs/workstreams/research/AF-RES-136/evidence/remote-recheck.json
[jq]: https://github.com/jqlang/jq/issues/2530#issuecomment-1411829108
