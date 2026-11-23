# AF-RES-053 최종 문서 교차 검토

## 검토 주체·독립성·범위

검토자는 `/root/libass_frame`이다. root와 **같은 모델**의 보조자이며 이 작업의 libass 모집틀, 수신 카드 조사, 후속 원장 작성에 이미 참여했다. 따라서 별도 사람이 수행한 독립 검토가 아니고, 자신의 앞선 libass 분석을 다시 대조한 부분이 있다. 이 기록을 사람 독립 검토나 완전 차폐 검토로 부르면 안 된다.

새 외부 자료를 열지 않았고 renderer·재생·민감도 실행을 다시 하지 않았다. 이미 저장된 문서와 원장만 읽고 ID·표 행·분모·해시를 집계했다. root 원문은 수정하지 않았으며 발견사항을 메시지로 전달했다. root의 후속 문구 수정을 다시 읽어 확인했다.

검토 시작 snapshot은 `2026-11-23T02:23:53.623857+00:00`이다. 사본과 상세 해시는 ignored `_scratch_not_for_commit/final-review-snapshot/`에 보관했다. 다음 자료를 대조했다.

- RESULT.md, SELF_CHECK.md 전체.
- frozen cards.csv·predictions.csv 18행, outcomes.csv 18행 및 libass outcomes.json 8셀.
- sources.jsonl 188행의 ID·work_id·source 연결과 libass 핵심 source 본문, evidence/source-counts.json의 계보·배당·141개 적격 열람행.
- replay/results.json, replay/sensitivity-results.json, replay/prediction-comparison.csv, replay/output-differences.json, replay/analysis-amendments.json.
- 검토 도중 생성된 evidence/acceptance-evidence.json의26개 요건(02:28:06 UTC 추가 열람).
- evidence/comparison-counts.json, 표시창 `L01-D-window.txt`와 `L02-D-window.txt`의 실제 87단어. 두 창의 SHA256이 cards.csv에 봉인된 값과 일치함을 확인했다.

| 파일 | 검토 시작 SHA256 | 수정 확인 시 SHA256 |
| --- | --- | --- |
| RESULT.md | 35392877fb2a82fdadbdd1873589faae21a53106948cf150324d233b38d983d7 | b60e2681c601da6457a54ce12c944efa60669eae7a834610c77153afe4b2f606 |
| SELF_CHECK.md | a30891e2415f79729c4f2c0d4a8f645903625f8dafc420c386bb32c0682ade87 | 동일 |
| cards.csv | 20ce5c7e01bc5fc8a2b1951262d3be6ce5e1e12c51566d2f3727bd2fcee5e7aa | 수정 없이 동일 |
| predictions.csv | d7e63a27513879e8691d7138efeb7c42c9245093e4bdc808a9e984f9a1e95db5 | 수정 없이 동일 |
| outcomes.csv | fd06097e365dd43d64ce441dcf9172509c2d60e5e8854836e529bae9b29dc413 | 이번 검토에서 수정하지 않음 |
| sources.jsonl | 25f99a8456c8b9befd11d71769dbb31676b6208c5db8de91e05dbe8bcfc699d2 | 이번 검토에서 수정하지 않음 |
| evidence/acceptance-evidence.json | 시작 시 미생성 | 8579b7fb6bb37868df00e2a09ab4517f0269164f27b9478aa64e6037d76e6dc3 |

## 결론

필수 표 18/6행과 원장 ID, 주된 판정, 역사판과 연구판의 구분, L02의 보충 정상 입력과 미정 B 값, 0·해당 없음·미확인의 의미는 서로 맞는다. 검토 시작판에서 **실제 D 표시창보다 넓게 요약한 두 문구**를 발견했다. root가 두 문구와 관련 연결 표현을 좁혔으며 `2026-11-23T02:26:14.688032+00:00`에 수정 내용을 확인했다. frozen 카드·예측·선택 결론을 바꿀 사안은 아니었다.

연구 결손은 해결된 것으로 판정하지 않았다. 선택은5/6, 원작성자판·최초 본문판은 미확인, 새 독립 후속 저작은0/6, L01/L02의 숫자 B는 미고정이다. 이 기록은 문서의 정합성 검토이며 작업의 완전 충족을 인증하지 않는다.

## 발견사항과 root의 수정

| ID·중요도 | 위치·발견사항 | 직접 대조 근거 | 요청한 수정 | 수정 확인·영향 |
| --- | --- | --- | --- | --- |
| FR-01 · 문구 귀속 | RESULT 표2 L01-D, 시작판 L27의 `최소너비`는 실제 표시한 87단어 창에 없다. 전체 CSS 원전의 후속 규칙과 카드가 실제 보인 정보가 섞였다. | cards.csv L01-D 및 evidence/scratch/L01-D-window.txt. 창 SHA256 6c90a1486165ad30a9687e22a9187a5db6ba16ba1d195b11cf2e54d33f2b47da | 표시창이 가진 중앙, overflow·겹침 최소화, 내용량 비례 분배로 좁힘 | root가 `CSS 중앙/overflow·겹침/내용비례 분배; 수평 페이지 규칙`으로 수정. D의 판별불가·후속 결손은 그대로 |
| FR-02 · 문구 귀속 | RESULT 표2 L02-D, 시작판 L28의 `겹침을 피해`는 해당 창이 제시한 숨김 이유보다 넓다. 원문은 굽은 도로를 따라가면서 읽을 수 있게 만드는 어려움을 설명한다. | cards.csv L02-D 및 evidence/scratch/L02-D-window.txt, 87단어, SHA256 9f2d2888357930817a21be18044808ad42516105dee23b2cd1ef7da155f262ac | 곡선 지물·가독성 제약으로 일부 라벨을 숨긴다고 기록 | root가 표2를 좁히고 Q5 연결도 `가독성/선택적 표시`로 조정. 실제 D가 숨김을 권해 틀렸다는 새 오답 주장은 추가되지 않음 |

FR-01은 공개 원전의 전체 최소너비 규칙 자체가 틀렸다는 지적이 아니라, **같은 예산의 D 카드가 실제 보인 것에 귀속할 수 있느냐**의 수정이다. 두 원문창의 bytes SHA256은 cards.csv의 addition_window_sha256과 일치한다.

## 교차 대조 결과

| 점검 | 확인 결과 | 근거·한계 |
| --- | --- | --- |
| 시작 두 필수 표 | 첫 줄부터 표1, 18행·8열. 표2는6행·8열 | RESULT 시작판 L1–29. L03의3보기와 요구1행이 남아 있음 |
| 원장 ID | card/prediction/outcome의 ID집합이 같고18개 고유 | 표1의 V01-N부터 L03-D까지 모두 대응. 표2는 V01/V02/V03/L01/L02/L03 |
| 질문 순서·마지막 약점 | Q1~Q7이 번호순이며 RESULT 마지막 표는 지정5열·약점3행 | 마지막3행 뒤 별도 본문이 없어 끝의 위치도 맞음. HANDOFF는 이 시점 검토 대상 아님 |
| frozen 선택·상태 | A만6행, 판별불가12행. 그중 L03 3행은 미실시·미충원 상태 | choice와 status를 분리한 RESULT Q5, outcomes.csv 및 libass outcomes.json이 맞음 |
| 추가 예산 | 5쌍의 I/D 단어·그림 수가 각각72/0, 68/0, 114/0, 87/1, 87/1로 같다 | N의215단어를 추가창200단어 위반으로 세지 않음. 예제 유형·인지 부담까지 같다고 주장하지 않음 |
| L01 B | 기본 bottom 대 큰 띠 중앙이라는 정책 차이는 남지만 숫자·block 측정·분기 구현은 미고정 | 표1/2, Q2 L57–60, Q6, 마지막 약점에 일관되게 기록. 원하는 도식을 성공 출력으로 세지 않음 |
| L02 정상 | t 제거는 연구자 보충이고 저자 완성 정상 입력·정상 출력은 없다 | 표1 L15–17, Q1 L43, predictions L02 세 보기, outcomes.csv normal_A/B_actual=미관측. t 제거를 animation 보존의 성공으로 세지 않음 |
| L02 B·실제판 | style10/event0과 B의 흰 event 비영 margin을 구분. 필요한 숫자와 libass patch는 미확인 | VLC3.0.18을 libass0.17.1과 동일시하지 않음. 후속 소스의 fallback/t 예외를 N의 사전 근거로 소급하지 않음 |
| 알려진 실패·후속 해설 | 원그림 겹침과 유지보수자 호환 설명, close, 패치·실제 출력이 구분됨 | LA-O03~06/24와 outcomes.csv. PR384/385는2020년 선행 배경으로 남아 후속 배당에 들어가지 않음 |
| 역사판/연구판 | 공개20논리셀은 완전 일치 미확인. 연구판2요구의 범주 선택만 별도 확인 | replay/results의 panel·limits와 RESULT Q2/Q6/Q7이 맞음. 18보기=18독립 출력으로 세지 않음 |
| 5.1.0 재생 수치 | 6변형,5 SVG,1 compile 실패. V02 정상 A/B 동일; V03 A=1빨강9검정, B=0빨강10검정 | results.json·output-differences.json. B compile 실패를 빈 SVG나0점 출력으로 바꾸지 않음. 16셀·48점·32제목은 사전 수치 예측으로 쓰지 않음 |
| 2.7.0 민감도 | 두 대상 y축 모두10검정, 조건식이 compiled output에서 사라짐 | sensitivity-results의 사후 탐색, 같은 입력 bytes, compiler+runtime+dependency 동시변경 한계를 문서에 유지. 작성자 실제판이나 compiler만의 격리 효과로 쓰지 않음 |
| 0·해당 없음·미확인 | I/D 상이 예측0/5는 문서상 실제 비교의 관측0. D만의 새 적중 조건부 분모0의 비율은 해당 없음. 공개 정답 동률은 미확인 | comparison-counts 및 RESULT Q7. 0/20은 완전 일치 자료 확보 수이며 성공률/실패율이 아니라는 설명이 있음 |
| 원문·배당 | 188 source 행/188고유source ID. 원장 work 계보의 primary_eligible canonical 집합71개, 적격 원문행141개 | source-counts와 실제 source ID 연결에 맞고 outcome의 참조source ID 누락 없음. 역할별5/6·5/4·4/4·0/6·2/2이며 초과분으로 결손을 상쇄하지 않음 |
| 수용 원장 | 26개 요건의 상태·분자·분모·단위가 본문 및 집계 원장과 대응 | overall_status=부분 인계, fully_satisfied=false. 표 위치·기존 evidence 파일/행 범위·JSON pointer를 읽어 확인. 아직 없는 HANDOFF 참조2건은 R21/R22의 명시적 미래 대기이며 완료 근거로 쓰이지 않음 |
| 검토자의 독립성 | root·같은 모델 보조자 검토와 사람 독립 검토 미실시를 SELF_CHECK에 명시 | 이번 검토 역시 같은 모델·libass 작성 참여자이며 새로운 사람 자료나 독립 실험을 추가하지 않음 |

## 남은 확인 범위

`evidence/acceptance-evidence.json`은 첫 snapshot에는 없었고 2026-11-23T02:26:35.367010+00:00에 생성됐다. 2026-11-23T02:28:06.666266+00:00에 전체26개 요건을 추가로 읽었다. 연구 결손의 부분 충족/미확인, 조건부 분모0의 해당 없음, 보조 재생 및 사후 민감도의 한정 상태가 RESULT/SELF_CHECK/원장과 일치한다. 기존 파일의 행 범위와 JSON pointer에서 잘못된 참조는 찾지 못했다. R21/R22의 HANDOFF.md 참조는 파일 미생성이지만 둘 다 결과 뒤 대기 상태이므로 현재 성공 증거로 계산되지 않는다.

원격 고정 결과 재열람, 최종 session check, HANDOFF의 최종 약점 표와 SHA 연결은 이번 검토에서 **미실시**다. root가 이후 생성·수행한 자료는 별도 영수증으로 판정해야 한다.

이후 문서에 검토 이력을 연결할 때는 FR-01/02의 원전창 귀속 수정과 선택·예측 불변을 적으면 된다. 위 미확인 연구 결손이 남아 있어 최종 상태는 부분 인계여야 한다.

