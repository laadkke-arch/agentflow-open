| 원사건·최초판 | 파일 단위·시간 원점 | 유지할 것·원문 위치 | 봉인한 첫 안내 | 나중의 동일인 증거 | 미확인 |
|---|---|---|---|---|---|
| I3402 #3402 (2022-08-19; 최초 revision 미확인) | clip 별 파일; 원점 미명시 | 별개 트랙의 clips, clip name; title/body | 두 조건부: M01 Tracks/Labels, M02 point/region; native clip 옵션 없음을 명시 | 동일인 댓글 0; 타인 C3402에서 질문·플러그인 제안 | 이름 충돌/공백/채널/OS/판; **판별불가** |
| I4811 #4811 (2023-06-19; 최초 revision 미확인) | label 전 구간 별 파일 여부; 구간 경계 | 기존 기본 off; body Expected behavior, alpha 2e235de, Win10 | 즉답: M01 Include audio before first label = off; Case 3은 on | C4811 #1627690036 2023-07-09T11:38:28Z, alpha 796e0db Windows에서 fixed로 보인다고 재시험 | PCM, 정확 전체 SHA, clean preferences; **유지** |
| I5302 #5302 (2023-10-03; 최초 revision 미확인) | track별 독립 mono/stereo 파일; 원점 미명시 | 다른 track 미혼합; body Steps/Expected/Actual; 3.3.3 정상 보고 | 즉답 M01 Tracks, Labels와 구분; 회귀 확인 | C5302 #1744624004, #1746468973: new exporter PR 지목 및 tested; P02 selectedOnly 전달 수정 | retest build/PCM/시작점·길이; **유지** |
| I5797 #5797 (2023-12-18; 최초 revision 미확인) | 원하는 label track의 region/복수 track/선택 label; 각 label 경계 | Beat Finder 상단은 제외, 아래 song ranges 사용; body steps/expected | 두 조건부 M01 uppermost label track + M02 Moving Tracks, 복수/일부 native 제한 | 동일인 댓글 0; C5797 #1963022495 타인 관련 이슈 언급 | 복수 줄 합치기/중복 구간 정책/실제 파일; **판별불가** |

표 1: 한 행은 지명 이슈의 원작성자-원요구 1자리이다. 날짜는 REST created_at의 UTC, 최초 revision 보장은 아니다. 판정은 첫 안내의 절과 동일인 후속 설명의 양립 여부이지 파일 생성 성공이 아니다. 4 예정 / 4 현재 body 단독 판독 / 0 최초 revision 확정 / 2 동일인 후속 / 2 결측. 유지 2·반전 0·판별불가 2. 질문에 대한 실제 응답 0/4; 가림 적중률 산출하지 않음. petersampsonaudacity의 두 이슈는 다른 요청 자리이다.

| 바뀐 조건 | 답 A의 원문 절 | 답 B의 원문 절 | 질문·즉답·두 링크 | 비용·반전 사례 |
|---|---|---|---|---|
| I3402 clip vs whole track | M02 point/region + M01 Labels; clip workaround에 한함 | M01 Tracks | 두 조건부; clip 요구가 명시되어 되묻지 않음 | clip-only 요구를 track-only로 대체하면 손실; 질문 1턴, native 부재 해결 못 함 |
| I4811 첫 label 이전 구간 포함 여부 | M01 Include audio before first label, Case 3 | M01 Cases 1/2 및 off | 즉답 off: 원문이 명시 | on이면 별도 pre-label 파일; default와 현재 UI 상태 다름 |
| I5302 track별 독립 vs label별 mix | M01 Tracks | M01 Labels | 즉답 Tracks, 회귀 분리 | track 명시되어 질문 비용 1턴; bug는 질문으로 고칠 수 없음 |
| I5797 한 label stream vs 여러/일부 | M01 uppermost label track + M02 Moving Tracks | M01 limitation + M02 label editing (수동 재구성, 가설) | 두 링크 조건부 | 순서 바꾸기만으로 여러 label stream 내보내기 못 함 |
| 시간축 통제 C1: project 0 vs 각 첫 clip | M03 Trim blank space before first clip off; E01/E02 | M03 같은 절 on; E01/E02 | 한 질문은 옵션 값을 바꾸나 링크 자체는 같은 절: 즉답/두 조건부가 적절할 수 있음 | F01/F03과 F05의 서로 반대 목적, 같은 옵션 경로 |
| 이름 통제 C3: 파일명 vs title tag | M01 Naming files | M04 Metadata Editor | 한 질문: 파일 탐색기 이름인가, 플레이어/속성의 제목·태그인가? | F04 태그와 title·파일명을 분리; 분할 설정 변경 불필요 가능 |

표 2: 한 행은 분기를 뒤집는 조건 하나(가설 포함). 처음 4행은 봉인 기록 first-routes.md의 사후 대조이며 뒤의 두 행은 일반화 통제. 링크는 sources.jsonl ID로 추적. 질문 1회는 대화 비용이지 실행 시간 실측 아님.

## 주관측
- 질문의 우선순위: 이미 파일 단위가 원문에 있으면 먼저 그 절에 연결하고, 미확인 시간축은 두 옵션의 의미를 함께 제시한다. 단위 자체가 불명일 때 “파일마다 한 track/clip의 소리를 독립시키려는가, 아니면 프로젝트의 특정 시간 구간을 들리는 트랙과 함께 내보내려는가?”가 다른 첫 절을 만든다. 공통 기준 0 유지와 각 clip 시작 정렬은 같은 Trim 절의 반대 값일 수도 있다.
- F01·F03 정렬 유지와 F05 짧은 파일 목적의 반대 사례가 실제로 확인된다. F02는 top label 한계, F04는 이름/태그 혼동이다. 다른 사람의 후속은 원작성자 결과가 아니다.
- 3.3.3과 3.4.2/3.5.0은 구별한다. E01–E04와 P02는 코드·변경 근거, 실행 관측은 아니다.
- 다음 단계: 코드·문서 충돌과 반례, 독립 입력을 상세화하고 Q1–Q7, 자체 점검을 고정한다.
