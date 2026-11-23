# AF-RES-049 자체 검토

| 질문 | 답과 직접 근거 | 반대 근거 또는 조건 | 남은 결손 | 재개 행동 |
| --- | --- | --- | --- | --- |
| Q1 | I01/I02의 현재 첫 본문·수락 댓글과 045의 requests L3–4/predictions L4–7, 복사 code를 [행별 대응](request-alignment.md)으로 확인했다. | #13600은 제목만 먼저 전송했다. M02 원문은 20개도 포함하고 seed를 지정하지 않았다. | #13600 원 첨부 .01/.1 직접 판독 미확인. #13522의 생성 순간 본문 미확인. | 이슈 본문의 두 PNG를 받아 원본 속성을 확인한다. 본문 생성판이 필요하면 공개 편집 이력을 찾는다. |
| Q2 | [환경](evidence/environment.json)의 실제 import·배포 해시·rc/DPI·font·FreeType와 [명령 영수증](evidence/command-receipts.json) R1/R2/V1/G1. | Windows/TkAgg가 아니고 원 Python 버전·32비트 조건이 다르다. Fontconfig 캐시 경고와 옛 Python의 libc 탐지가 호스트 버전과 다르다. | 원작성자 OS 글꼴·FreeType·NumPy 바이너리. | 당시 GUI 결과가 필요할 때만 Windows/TkAgg의 설치판 및 렌더 조건을 기록해서 반복한다. |
| Q3 | [runs L2–5/L12–15](runs.csv#L2), 실제 limits 및 3시점 anchor. A .5, B 조건부 .505051과 5.050505. | x도 norm.inverse임을 출력 전에 확인. layout 적용이 display 위치를 바꿔도 axes fraction은 그대로였다. | 경계 B의 실제 PNG. 경계 B의 정상 저장은 미시도다. | 3.0.2 원판 결과를 보존하고 별도 guard만 적용한 경계 B PNG를 측정한다. |
| Q4 | [runs L6–11/L16–21](runs.csv#L6), [판독](evidence/png-readback.csv). 10개 10/10, 30개 B/C bbox 차 0px, B 12/30, A 11/30. | 30개 A는 처음보다 축을 줄인 사례가 아니라 layout 거부다. bbox가 걸친 12-l에 픽셀이 없다. 색 반복 때문에 판독과 고유 계열 해독이 다르다. | 읽는 사람의 계열 대응과 더 많은 입력/폰트에서의 손실 시작점. | 고유한 색·모양·이름을 갖는 fixture와 독자 과제에서 의미 손실을 검증한다. |
| Q5 | [짝 비교](evidence/replay-pairs.json) 10/10 상태·geometry 일치. 저장 PNG의 바이트/RGB 9/9 동일, 동일 실패 1/1. M03 PNG/transform 13/13 일치. | 같은 머신과 실행자. 레이아웃 실패 3행의 pixel 판정은 비어 있다. 저장 실패는 관측 0. | 두 번째 호스트 및 다른 사람의 판독. | 분리된 호스트에서 잠금 파일로 실행해 read-only 비교 명령을 사용한다. |
| Q6 | [목적 변경과 판 감도](evidence/observations.md#m03)와 [회귀 C08](sources.jsonl#L15). y=.5는 혼합 좌표에서 보존. 2.2.2 A/B PNG가 같은 factor마다 일치. | .001에서 y=.5는 범위 밖이고 혼합도 실패. xlim 변경은 축 프레임과 색 띠를 분리한다. #13603 rect 호출은 anchor 관측이 없는 crash 체크다. | 특정 경계·norm·가로막대에서 좌표 결과. | 독자가 보존할 값을 고정한 뒤 다른 norm/방향으로 한 요인씩 바꾼다. |
| Q7 | [카드](cards.md) 및 [P01–P04/M01–M04](sources.jsonl), API E05/E06와 동률 M02. 인쇄와 지도에서 유지하는 참조를 확인했다. | 지도에도 보이는 폴리곤 중심 선택이 있고 인쇄에도 문단과 함께 이동하는 anchor가 있다. API만으로 조작을 만들 수 있다. | CS6 지정 쪽 직접 열람, 역사적 영감·원전 채택, 비교 효과와 노동시간. | Adobe PDF 300–301쪽을 확인하고, 같은 목적의 API만 제공한 조건과 도너 제공 조건을 별도 비교한다. |

먼저 고정한 조건과 새 결과를 섞지 않았다. [사전 봉인 ef159f3](https://github.com/laadkke-arch/agentflow-open/commit/ef159f3b81ab210003668be9ffd0faa82c450b09), [출력 전 기준선 a920b78](https://github.com/laadkke-arch/agentflow-open/commit/a920b7835593bf19b7a03ddfe7ccc4bc28456e6d), [관측 4946188](https://github.com/laadkke-arch/agentflow-open/commit/4946188ca809d59277c2766ad7e4d660131c29de)을 구별한다. 첫 원본을 읽었던 045의 다름 3·같음 2·미결정 1은 배경 수치이며 이번 실험률에 쓰지 않았다.

CSS·지도 원전의 서술을 그 자체로 Matplotlib API 검증에 쓰지 않았다. 같은 목적의 추천이 하나로 좁혀진 것과 원리 한쪽의 독점 효과를 구별했다. 소스 판과 PyPI wheel, 같은 OS에서 두 설치, 원작성자 수락을 각각 따로 확인했다. 이 문서는 같은 작업자의 자체 검토다.
