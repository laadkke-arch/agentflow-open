# Matplotlib 후속 판독 및 반증 메모

| 범위 | 사례 분모 | 첫 실제 질문: 넓은/정보·입력 | 같은 변수 직접 답: 엄격 | 같은 지원자의 명시적 권고 변경 | 새 동일목적 실행 성공/실패 | 공개 관측 불능 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8 | 4/8 · 3/8 | 1/3 질문 사례, 또는 1/8 전체 | 0/1 직접답 사례 | 2/8 · 1/8 | 0/8 |
| 선택 B | 1 | 1/1 · 1/1 | 0/1 | 해당 없음: 직접답0 | 1/1 · 0/1 | 0/1 |
| 선택 밖 B screening audit | 26 | 첫답 기준은 T0에 봉인 | 위 분모에 합치지 않음 | 위 분모에 합치지 않음 | 정성 반례로만 사용 | 0/26 공개댓글 페이지 누락 |

원격 T0 봉인: `9de54923257d613359348c8ccee2ff8225c8a0d8`. 이후에만 작성자 답과 후속을 읽었다. 정보 질문 A는 M01·M07·M08이며 M03의 후보 적합성 평가 질문은 넓은 분모에만 둔다. 같은 변수 직접 답1건은 M01이다. M01 현재 본문에 NumPy1.24가 있고 답은1.24.0이지만, 현재 본문의 값이 첫 응답 전에도 있었는지는 원판 이력이 없어 **미확인**이다. 따라서 현재 본문 중복1/3과 첫 응답 전 확정 중복0/3을 구분한다. 0은 중복이 없었다는 증명이 아니다.

## 질문에서 실제 행동까지: 핵심 판정

| 사례 | 관측된 연결 | 보류하거나 제외한 주장 | 증거 |
| --- | --- | --- | --- |
| M01 | NumPy 판 질문 뒤6분7초 만에1.24.0 출력과 경고 활성화 설정을 함께 받음. 같은 지원자가 재현 가능으로 바뀌었다고 확인 | 답 전 사용 제안이 없어 권고 변경은 `no_prior_proposal`. 자발적으로 공개한 `-W always`/pytest 설정과 판 답의 효과를 분리할 수 없음. 공급자PR를 원작성자 실행으로 세지 않음 | [작성자 답](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341), [지원자 재현확인](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368556640), [수리PR](https://github.com/matplotlib/matplotlib/pull/24970) |
| M03 | 후보 `addfont`가 영속 목적에 맞지 않는다는 답 뒤 다른 지원자들의 cache 설명을 받음. 작성자가 cache를 삭제해 작동했다고 보고 | 첫 지원자 story645가 자신의 후보를 바꾼 것이 아니다. 다른 지원자 도움과 작성자의 역질문이 매개. 새 프로세스마다 지속되는지는 미확인이라 성공은 부분목표 수준 | [후보 거절](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1370065191), [cache 설명](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1370331856), [실행보고](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1370892263) |
| M04 | 질문 없이 공식 Tk 예제 링크와 Figure 직접 생성 안내. 작성자가 API를 바꾸자 종료 문제가 해결됐다고 보고 | 실제 머신을 독립 재현하지는 않음. 감사나 close가 아니라 구체적인 API 교체와 결과를 성공 근거로 삼음 | [즉시 안내](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370025244), [작성자 실행](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370981028) |
| M05 | 공개댓글0, 실질 권고 없음 | 접근불능이 아니라 관측된 무응답. 최초 실패 그림을 새로운 후속 실패로 중복 집계하지 않음 | [공개 스레드](https://github.com/matplotlib/matplotlib/issues/28496) |
| M06 | pandas `clear` 구현으로 즉시 진단. 작성자는 원문을 큰 grid로 수정하고 pandas에 신고하겠다고 말함 | 최초 정보량은 개정본 대리값. 신고 계획과 실제 신고를 구분하고, 원문 개정을 새 성공 실행으로 세지 않음 | [지원자](https://github.com/matplotlib/matplotlib/issues/28505#issuecomment-2206991348), [원문 개정 고지](https://github.com/matplotlib/matplotlib/issues/28505#issuecomment-2206992828) |
| M07 | 이전 Seaborn 신고 여부를 물었으나 원작성자 댓글0. 18일 뒤 Seaborn 공급자가 다른 구현 방식과 `move_legend`를 설명 | 제3자 설명은 작성자가 질문한 변수에 답한 것이 아니다. 기존 Legend setter 제안에 성공 실행을 붙이지 않음 | [첫 질문](https://github.com/matplotlib/matplotlib/issues/28511#issuecomment-2211377162), [제3자 설명](https://github.com/matplotlib/matplotlib/issues/28511#issuecomment-2245186842) |
| M08 | loop와 close_event를 제거한 코드도 crash한다는 새 실패 보고. 같은 지원자가 toolkit 통일과 event-loop 제약을 설명 | 요청한 단일 toolkit 재현은 주지 않았고 Tk+macosx는 유지. 부분 입력 뒤 설명 이동을 엄격한 직접답→권고변경으로 세지 않음 | [부분 입력/실패](https://github.com/matplotlib/matplotlib/issues/28513#issuecomment-2211433918), [후속 설명](https://github.com/matplotlib/matplotlib/issues/28513#issuecomment-2214055492) |
| MB09 | 질문과 함께 받은 새 conda 환경 생성 제안을 실행하자 정상이라고1시간31분19초 뒤 보고 | 이전 환경의 실제 package 판은 끝내 답하지 않음. 질문이 유익해서 성공했다고 읽으면 혼합응답의 즉시 행동을 질문 효과로 오인 | [혼합응답](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496053940), [새 환경 성공](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688) |

## 고정 대조와 그 한계

M01→M02는 같은 원장·2023Q1·bug·정보점수5/4 조건으로 T0에 고정된 짝이다. 양쪽 모두 30일 안에 공급자가 코드 수리를 만들었지만 원작성자 설치·실행은 없다. M01의 정보 질문 뒤 재현 확인과 M02의 즉시 설계안 뒤 구현을 비교할 수는 있어도 질문이 결과를 개선했다는 비교가 아니다. 색인 dtype과 wx toolbar는 다른 기술 문제다. [M02 공급자 수리](https://github.com/matplotlib/matplotlib/pull/24869)는 사용자 실행이 아니다.

M08→M06은 같은 원장·2024Q3·bug·현재 본문 점수5/5다. GUI crash와 시계열 plotting은 목적과 복잡도가 다르고 M06 본문은 첫 응답 뒤 개정됐음이 밝혀졌다. 미래 노출 사례를 제외하는 감도에서는 이 짝이 사라진다. M03과 M07에는 같은 분기 usage형 즉답/조건부 대조가 없어 해당 없음으로 둔다. M04는 유익한 질문 없는 실행 반례지만 사전에 고정한 M01의 짝을 M04로 바꾸지 않는다.

## 첫 결론을 깨는 실제 경로: 선택 밖 audit

32건의 핵심 A/B 분석에 들어가지 않은 표본을 양성이 보였다는 이유로 승격하지 않았다. 대신 모든 Matplotlib B 시도27개를 확인했고, 선택 밖26개는 `screening-followups.jsonl`과 `screening-sources.jsonl`에 남겼다.

| 사례 | 처음 결론을 깨는 관측 | 제한 |
| --- | --- | --- |
| MB07 | 첫답은 즉답이지만 뒤에 사용 목적을 물었다. 작성자가 사용자가 추가하는 axes가 canvas 밖에 생기는 도구라고 답했고, 여러 단계 뒤 같은 지원자가 `_tight_bbox` 경로를 알려 줬다. 작성자는 resize 코드를 작성해 범위 밖 항목이 영상에 나온다고 보고 | [목적 질문](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496169583) → [목적 답](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496337035) → [후속 소스 안내](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498195823) → [새 코드·출력 보고](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774). 타 지원자 설명과 작성자 자체 초안이 매개하므로 한 변수 질문의 단독효과는 미확인 |
| MB21 | 실행 중인 동일 shell에 PySide6.5.0이 있다는 직접 답을 받았고, 지원자가 같은 판을 다시 물어도 작성자는 답했다. 여러 실패 시험 뒤 작성자의 debugger 관찰로 Qt5 강제가 드러났고 import 우회가 작동 | [직접 답](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146), [다중 질문](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506278627), [우회 성공](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1522271486). 최초 질문 전 제안 없음, 후속 실험 여러 개, 최종 `qt6` 안내 실행은 미확인 |
| MB27 | GTK/GLib 질문에 처음 GLib1 값을 답했다가 GLib2로 정정. 지원자가 판을 인용해 업데이트를 안내. 자체 빌드 실패 뒤29.7일째 배포판 패키지로 성공 | [첫 값](https://github.com/matplotlib/matplotlib/issues/25688#issuecomment-1516325279), [주체 정정](https://github.com/matplotlib/matplotlib/issues/25688#issuecomment-1517039030), [버전 기반 안내](https://github.com/matplotlib/matplotlib/issues/25688#issuecomment-1521047724), [최종 실행](https://github.com/matplotlib/matplotlib/issues/25688#issuecomment-1546936936). 한 질문의 두 변수, 처음에 잘못 식별한 package, 새 배포판 공급을 분리해야 함 |
| MB06·MB26 | 각각 backend 이름 변경과 다중상속 대신 delegation으로 질문 없는 새 성공 보고 | [MB06](https://github.com/matplotlib/matplotlib/issues/25605#issuecomment-1494308785), [MB26](https://github.com/matplotlib/matplotlib/issues/25685#issuecomment-1509885968). 사후 audit이고 A의 발생률에 넣지 않음 |

MB16은 torch 없이 재현해 달라는 요구에 다른 외부 이미지 파일로 답해 같은 입력 조건을 충족하지 못한다. MB20에서는 원작성자의 PyQt 시험 방법에 답이 없고, 대신 들어온 기여자가 처음에는 TkAgg를 썼다고 나중에 정정했다. 이 둘은 주체·환경·입력 동일성을 확인하지 않은 왕복 집계의 반례다. [MB16 지원자 재요청](https://github.com/matplotlib/matplotlib/issues/25653#issuecomment-1502624883), [MB20 제3자 정정](https://github.com/matplotlib/matplotlib/issues/25671#issuecomment-1549694615).

## 제공자 근거의 판과 범위

`providers.jsonl`은19개 URL 기록이며 자료군으로는16개다. 최소수 산입은13개이고, 같은 font_manager·Legend 문서/구현 및 동일 바이트 Seaborn tag 경로는 중복 산입하지 않았다. 두 수리PR는90일 동일사건 추가 자료, GTK issue는 root만 직접 읽어 별도 보류자료다. 핵심 A8과 선택B1의 스레드9개 및 선택 밖26개를 합치면 이 stream에서 직접 읽은 스레드는35개다. 이를 분석 사례9개, 독립 사람35명, 또는 최소36원문35개로 바꾸지 않는다.

M07의 공식3.8.4 `Legend.set(ncols=...)` 인터페이스는 존재한다. 그러나 같은 판 구현의 setter는 내부 숫자만 저장하고 그리기는 기존 legend box를 사용한다. 실제 열 재배치 실행을 하지 않은 채 API 존재를 완전한 해결 승인으로 확대하지 않았다. `move_legend`의0.13.2 구현은 기존 handle/label로 legend를 다시 만들지만 원작성자의 Seaborn 판과 데이터가 없으므로 조건부 기술 지지만 가능하다. [Legend 구현](https://github.com/matplotlib/matplotlib/blob/v3.8.4/lib/matplotlib/legend.py#L725-L727), [재생성 구현](https://github.com/mwaskom/seaborn/blob/v0.13.2/seaborn/utils.py#L434-L470).

Cartopy0.21 공식 설치 안내는 conda 사용뿐 아니라 conda 환경에서 pip 개발설치도 제시한다. 그러므로 conda와 pip가 함께 보인다는 사실만으로 실패 원인을 확정할 수 없다. MB09에서 새 환경은 실제로 작동했지만 이전 환경의 문제가 어느 판·경로·의존성이었는지는 미확인이다. [당시 설치 안내](https://scitools.org.uk/cartopy/docs/v0.21/installing.html#required-dependencies).

## 비용·원판·검사 한계

엄격한 같은 변수 왕복은 A에서1건, 선택B에서0건이다. 작성자 부분답·후보 평가·행동 응답까지 포함한 대화 왕복은 각각 M01·M03·M08 및 MB09의4개 고유 키이며, 질문한 변수의 회수4건이라는 뜻은 아니다. M01의 답 대기는0.101944시간이다. M08은 댓글 생성까지0.268611시간, 현재 개정 내용이 확실히 존재하는 최종 수정 시각까지0.505278시간이므로 단일 정확한 내용 도착 시각으로 압축하지 않는다. M07은 질문 후30일 동일변수 무응답 검열720시간이다. 클릭·읽기시간·대체노동은 관측하지 못했다.

A의 root30 댓글은31개, root90 댓글은33개다. 뒤의2개는 M03의67·69일째 제3자 접근성 논의이므로 원작성자의 추가 실행이 아니다. 선택B의 댓글은2개다. 공개 댓글 수는 API와 HTML total이 일치하며 M03의 HTML 앞·뒤 pagination은 REST 완전목록으로 보완했다. 이 일치는 과거 삭제된 미표시 댓글이 없었다는 보장이 아니다. 현재 댓글의 `lastEditedAt`과 해시는 `evidence/followup-read-receipts.json`에 연결한다.

원판 완전확인 O는0/8이고 M04의 `plt.figure` 절만 첫답 인용으로 Q다. 미확인 root를 원판이라고 단정했을 때의 결론과 현재본문 관측 결론을 구별해야 한다. 실제 효과에 대한 양끝 가정은 관측된0을 인과효과0으로 바꾸지 못한다. 공개기록에 없는 선택·실행이 모두 성공이었다는 가정에서는 실행성공 상한이 크게 늘지만, 질문 없이도 성공했을 반사실과 기다림을 줄였을 양은 여전히 알 수 없다.

역사 환경의 GUI·PGF·Cartopy 실행을 수행하지 않았다. 필요한 입력은 해당 사례 root의 정확한 코드와 명시판이며, 최초 body 수정 이력을 먼저 확보해야 비교 가능한 실험이 된다. M07의 제한된 기술 검증을 이어간다면 Python3.11에서 `matplotlib==3.8.4`, `seaborn==0.13.2`, `numpy<2`를 고정하고 동일한6개 label의 legend에 `set(ncols=3)`를 적용한 전후 이미지와 `move_legend(..., ncols=3)` 재생성 이미지를 비교한다. 이는 원작성자 행동의 재현이 아니라 공급자 API의 기술 검사다. 실행명령과 입력은 `pending-checks.md`에 둔다.

## Q1–Q8 자체 반증 점검

| 질문 | 주장과 근거 | 뒤집을 조건·찾은 반례 | 남은 미확인 |
| --- | --- | --- | --- |
| Q1 | A분기별 최초4개, B27 연속심사: frame.csv | 선정 뒤 상태/성공으로 교체하지 않음. MB07/MB27 양성을 발견해도 B8 보충 안 함 | 삭제되어 검색 프레임에 안 보이는 과거 root |
| Q2 | current root와 첫 응답을 분리하고 U/Q 유지: initial.field_map·corrections | M06의 사후 원문 개정 고지가 정보량 점수의 시간성 가정을 깨뜨림 | M01 값의 첫 공개시점, 모든 완전원판 |
| Q3 | broad질문과 정보질문을 분리: questions.csv | M03 후보 평가, MB15 개발 수용 질문, M07 제3자 의문형 제안이 모두 같은 종류는 아님 | 원판 차이로 첫 전략 맥락이 변할 가능성 |
| Q4 | B선정은 first response만으로 고정: T0 SHA | 후발 양성 MB07, 순위밖 MB27을 추가하면 표집이 결과에 종속됨 | 다른 표집창에서의 발생률 |
| Q5 | M01만 엄격 같은변수 직접답: chains | MB09 새환경 성공은 이전환경값 답이 아님. MB16 외부파일과 MB20 다른toolkit이 대상을 어긋남 | 실제 실행 interpreter/package, 초기 요구 형성시점 |
| Q6 | 핵심표본 strict 권고변경0, 기술 지지와 실행분리 | M03 다른지원자 도움, MB07의 후발 목적질문+실행, MB27 새제안+후발패키지가0의 일반화를 깨뜨림 | 같은변수 질문의 단독 인과효과 |
| Q7 | 질문없는M04실행 및MB09즉시행동성공 존재 | M01 질문 후 재현이 좋아졌고 MB21 반복질문에도 답이 와서 질문은항상낭비라는결론도 깨짐 | 클릭·노동절약·전략선택 혼란변수 |
| Q8 | 질문문은 정확한 변수·주체·판·시점이 필요 | package목록과실행환경,작동예제와실데이터,부분목표와영속목표 구분을 하지 않으면 답과성공을오집계 | UI질문의 실제효과는 실험/추가관측 필요 |

| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |
| --- | --- | --- | --- |
| 원판이 미복원된 상태에서 현재본문의 이미 있는 값을 최초 중복으로 읽을 위험 | https://github.com/matplotlib/matplotlib/issues/24865 | 질문 전 충분도·중복질문의 비용 | 첫 응답 전 root/title을 보존한 원판 이력 또는 알림 메일 |
| 같은 변수 답 없이도 혼합응답의 행동 실행이 성공하고, 다른 지원자의 도움도 매개 | https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688 | 질문→답→변경→실행의 인과적 해석 | 이전/새 환경의 실제 import 경로와 판 비교 자료 |
| strict 변경0은 작은 고정표본의 관측이며 선택 밖에 질문·행동 연결 반례가 있음 | https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774 | 질문의 유용성에 대한 일반화 | 후발 목적질문이 있는 고정 새표본; MB07의 최초 목적 원판부터 확인 |
