# AF-RES-038 · Q1~Q7 자체 대조

범위는 자료와 예시 답안의 판별 가능성이다. 사람 효과·시간·신뢰도·합의는 관측하지 않았다. 기준은 사전 원격 SCOPE, 실제 참가자 파일, 직접 열람 원장, 기대 봉인, 별도 문맥 판독을 서로 대조한다. 파일 위치는 최종 `evidence/acceptance-evidence.json`에서 행 단위로 연결한다.

## Q1 — 실제 선택과 표집이 재작업을 판별할 원 요구를 갖는가

**관측:** PDEP1~20, NEP1~20 번호순 40행의 프레임을 남겼다. 네 선택은 P02 build 경계 전체, P04 batch 파싱 부분, P06 scalar 대입 부분, N08 작은 구매집계 전체다. 현행 목차/후속 제목 노출을 숨기지 않았고, 미심사를 부적격으로 바꾸지 않았다. `frame.csv`, `streams/*/selection-*`, `SCOPE.md`가 선정 순서를 보존한다.

**직접 근거:** [P02 최초 formal 판](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md#L10-L32)의 build/parallel/두 후보, [P04 최초 formal 판](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md)의 Abstract·Motivation·Detailed Description, [P06 최초 formal 판](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md)의 Detailed description·fractional 옵션, [N08 첫 복구 formal 판](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L21-L38)의 구매 사용례를 읽었다. source IDs P-S01~03/N-S01.

**반증 경로·수정:** PDEP3와5에서 다른 관행을 두 번째 정답으로 바꾸면 원 목적을 잃어 제외했다. PDEP7의 이관된 초안은 첫 Google 문서를 복구하지 못했다. N08은 [4/10 의견수집](https://mail.python.org/pipermail/numpy-discussion/2010-April/049846.html)과 [4/12 비연속 반복키 예시](https://mail.python.org/pipermail/numpy-discussion/2010-April/049901.html)를 더 찾아 git 추가일과 최초 공개를 분리했다. by month를 연월만 허용하는 해석도 삭제했다. 후대 오류가 있었다는 이유로 이 사례를 선정하지 않았다.

**남은 미확인·뒤집힐 조건:** formal 본문의 절대 첫 공개는 N08에서 미확인이다. 첫 복구판4개와 최초 공개까지 완전히 확인된4개를 동일시하지 않는다. 더 이른 동일 구매문서에서 필수 grouping/통계가 다르면 N08의 기준·적격성을 다시 판정한다. 기존021/034의 모든 개별 문제를 재판독하지 않았으므로 완전한 사례 중복 부재를 증명하지 않는다. P02의 CMake 도구명 중첩은 기록했다.

## Q2 — 링크 제공과 설명 추가가 실제 파일에서 분리되는가

**관측:** 4×5 참가자 파일20개를 만들었다. A는 같은 인터넷에서 검색, B는 중립 제목의 원문 링크3/2/3/3개, C는 그 URL·판·순서에 요구→절과 적용 한계만 더한다. `evidence/material-check.json`은 실제 파일의 URL 배열·문자수·해시와 설명 문단 외 차이 없음, `evidence/public-access.json`은 인증 없는 링크11/11의 HTTP200을 기록한다. 접근 확인은 내용 판독과 별개이며 새 원문으로 세지 않는다.

**직접 근거·반증:** [CMake3.23.3 manual](https://github.com/Kitware/CMake/blob/d566bd962df5b1bf0ec5d16e9e7affe592b8b3eb/Help/manual/cmake.1.rst#L473-L481), [pandas1.4.4 날짜 문서/구현](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py#L703-L773), [정수 guard](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py#L1931-L2009), [NumPy1.4 unique](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py#L95-L181)의 실제 절을 카드에 연결했다. P02의 세 번째 backend 자료는 한쪽 대안을 더 직접 도울 수 있어 선별 묶음의 특성으로 남겼다. P04 C의 경고는 모든 추론이 아니라 해당 판의 옵션으로 좁혔다.

**남은 미확인·뒤집힐 조건:** 의미 검토는 작성자 및 stream 재독이다. C를 권고로 읽는 정도, 초보의 읽기 부담, 링크의 지속 접근은 사람에게 확인하지 않았다. C가 새 조건/완성 답을 준다는 독립 판독이 나오면 해당 파일을 정정하고 판독을 다시 봉인한다. A↔B는 선별·초기 제공 묶음, B↔C는 길이·읽기 부담을 포함한 설명 추가, A↔C는 전체 제공이다. 순수한 선정 알고리즘·의미·길이 각각의 인과효과를 분리하지 못한다.

## Q3 — t1은 새 기능이 아니라 같은 원 요구를 재검하는가

**관측:** `rubric.csv` 12요구에 원판 URL/절/시점, t0 질문, t1 probe, 허용 대안과 기준을 연결했다. P02는 기존 graph와 backend 경로 추적, P04는 같은 알고리즘의 두 날짜 batch, P06은 같은 선언 dtype의3.0/1.5/text, N08은 동일6행 재배열이다. `distribution.json`에서 후대 기준/정답은 배포 제외다.

**직접 근거:** [PEP517 고정판 build_wheel/build_sdist](https://github.com/python/peps/blob/19f2582774070b86cc4f8866d5c751f8cb7c56ee/pep-0517.txt#L198-L284), [공개 날짜 mismatch 시험](https://github.com/pandas-dev/pandas/blob/v2.0.0/pandas/tests/tools/test_to_datetime.py#L2723-L2758), [nullable setter 시험](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/tests/arrays/masked/test_indexing.py#L9-L55), [inverse 복원 시험](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/tests/test_arraysetops.py#L11-L35).

**반증 경로·수정:** [후대 build 전환](https://github.com/pandas-dev/pandas/commit/730439603919b9a38a54477f768b775f1aaf6412)의 import 자동 rebuild, [날짜 새 모드 결정](https://github.com/pandas-dev/pandas/commit/d1095bcd5a43528e195e2d587e6a8691d5ed005f)의 mixed/ISO8601, [NaN 예외 논의](https://github.com/pandas-dev/pandas/issues/54660#issuecomment-1693542083), [빈 그룹 논의](https://github.com/numpy/numpy/issues/834#issuecomment-294114765)를 원 finite/observed-group 계약과 분리했다. 빈 그룹 문제는 후대 처음 생긴 요구라고 주장하지 않는다. 단지 현재 과제의 원 범위 밖이다.

**남은 미확인·뒤집힐 조건:** P02/P06 범위 조작화와 N08 행순서 불변은 직접 원문 문장과 작성자 해석을 구분했다. 독립 원문 검토가 이 조작화를 원 목적 훼손으로 판단하면 해당 과제를 부적격으로 돌린다. 현재 공개 웹에서 후대 답을 자발적으로 찾는 것은 전 군에 가능하며 노출 기록으로 남긴다.

## Q4 — 다른 좋은 답을 받아들이고 그럴듯한 오답을 거절하는가

**관측 절차:** 12개 작성 예시·36요구 셀의 기대를 `a9589eb1ed899da83230e5c6a3ffa30123b7d5f2`에서 봉인했다. `evidence/grade-seal.json`은 입력 해시·분모·기존 작성자 이견을 보존한다. 별도 문맥 판독자는 프로토콜 v1 외에는 `evidence/blind-input.json`만 읽도록 제한했다. 이름을 지운 행동/출력은 남겼으며 파일 접근 제어로 강제된 격리는 아니다. 실제 판독과 조정 결과는 `examples.jsonl`, `evidence/blind-observed.json`, `evidence/grading-comparison.json`에 원형대로 남긴다.

**직접 근거·반증:** [CMake POC](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py)는 패키징 위임 자체를 실패로 보면 안 되는 반례다. [CPython strptime](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst#L1035-L1047)은 배열이 아닌 반환타입도 같은 날짜 계약을 충족하는 근거다. [nullable setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py#L198-L235)는 생성 schema가 다르다는 이유의 오탈락을 막는다. [정렬 인덱스](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py#L579-L666)와 [공개 그룹 집계 논의](https://github.com/numpy/numpy/issues/7265)는 키만 정렬하는 오류의 해석에 사용했다. 그 오류가 유지보수자에게 직접 확정됐다는 주장은 하지 않는다.

**남은 미확인·뒤집힐 조건:** 고정 예시에는 각 과제 두 적격·한 오류를 넣었지만 사람의 답안 다양성·오류 빈도는 모른다. P04의 정당한 inferred MDY strict 오류는 허용 기준에는 있지만 12개에 별도 네 번째 예시로 들어 있지 않다. N08-E3 R2의 partial/fail 이견을 가림 결과로 덮지 않고 원인 하나/파급 여러 셀로 분리한다. 외부 사람의 독립 채점에서 비주류 오탈락 또는 오류 오통과가 남으면 가림 채점표의 준비도를 철회한다.

## Q5 — 빨리 끝남과 포기·미수정·품질 실패를 구별하는가

**관측:** `forms/`에 assignment/exposure/activity/submission/decision/quality/rework/provider-cost/adjudication/deviation/events 양식을 만들었다. 작성 상태 fixture는 최초10개에서 품질미확인·늦은 최초완성 경계2개를 보강해12개를 분류하고 expected/observed를 남겼다. 포기·결측·품질 실패·정답 무수정·새 요구만·원요구 수정·오류 카드·둘 다 무수정·노동 누락·혼합분리불가를 포함한다. 모든 사람 duration과 실제 채택시각은 null이다.

**근거:** [AF034 future-study](https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/future-study.md) §§1–5, [measures](https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/measures.md) §§1–3의 첫 채택/원 요구/전원 분모를 재사용한다. [Wesenberg2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1032003/full) Methods·Results의 체감/단계정답 구분은 빠른 종료를 정답으로 삼지 않을 방법 근거다.

**반증·수정:** 별도 프로토콜 판독에서 첫 채택과 t1 사이의 수정을 누락할 수 있음을 발견해 관측창을 첫 t0 선언 직후부터로 고쳤다. 틀린 선택을 유지한0수정, 누락된 t1, 새 기능만 추가한 경우를 감소 성공으로 세지 않는다. 원래 버린 노동을 t0와 t1에 이중 합산하지 않는다.

**남은 미확인·뒤집힐 조건:** 실제 배정자N=0이므로 품질률/시간효과는 해당 없음 또는 미확인이다. 실제 활동이 누락되면 전원 평균 노동을 계산하지 않거나 사전 유한 경계를 쓴다. 채택자/완료자 조건부 결과만 좋아지면 전원 효율 가설 지지는 철회한다. 상태 fixture의 규칙 일치는 분류 코드 점검이며 사람 신뢰도 추정이 아니다.

## Q6 — 비용 전가·전문성·다른 분야에서 깨지는 조건을 점검했는가

**직접 방법 원문:** 디자인 [Chan2011](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) §§3–4/Table2, [Fu2013](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/md_135_2_021007.pdf) §§3–4, [Vasconcelos2016](https://api.repository.cam.ac.uk/server/api/core/bitstreams/6cd62cf5-a602-48f2-95ed-38a9f61f5644/content) pp5–8; 교육 [McLaren2016](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf) §2/Table2, [Wesenberg2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1032003/full) Methods·Results, [Reisslein2006](https://faculty.engineering.asu.edu/sites/g/files/litvpz5806/files//2020/02/Exp_Rev_LI06.pdf) pp94–97/99–102의 실제 자극·과제·채점 절을 읽었다. 기존034의5개 재독은 새 표본으로 세지 않았다.

**적용·반증:** `streams/methods/methods.md`는 초보/숙련/이미 아는 사람/작성자/유지자/가림 채점자의 관점과 과제별 오류를 연결한다. 그림이 같은데 지시가 다른 디자인 실험은 한 줄 설명도 주의·권고를 바꿀 수 있다는 반례다. near/far와 사전지식 상호작용의 차이는 작은 파싱 성공을 장기 설계에 전용하지 않을 이유다. 아이디어 특징 유사성은 품질 실패와 같지 않다. 공통검사의 학습 효과도 채택 뒤 유지보수 효과와 같지 않다.

**남은 미확인·뒤집힐 조건:** 기전 유추이며 AF038의 시간·제품 효과 추정이 아니다. 전문가의 읽기 부담, 카드 유지비, 비주류 판독비가 소비자 이득을 넘으면 전체 제공의 노동절약 주장을 철회한다. 제공자 시간과 사용 횟수가 없으므로 상각·손익분기를 계산하지 않았다.

## Q7 — 후속 사람이 참여하면 가설을 무엇으로 판정하는가

**준비한 절차:** `measurement.md` §§1–6/8은 사람 또는 팀 배정 단위, 과제·사전인지층 무작위 배정, 군 간 공유 기록, 같은 검색/도구/교육/예산, 채점 가림, 독립 판정 후 조정, 중단·결측을 정의한다. 전원 최종 품질+총 실제 노동이 우선이고 채택자 수정노동/완료자 시간은 별도 분모다. B–A, C–B 두 주대비와 C–A 전체 제공을 분리했다.

**판정·반증:** 같은 품질 기준과 노동 차이 기준을 모두 만족해야 효율 가설을 지지한다. 읽기만 늘거나 오연결 카드가 원 요구 오류를 일으키면 반대 결과로 남긴다. 두 정답이 모두 유지되는 검사를 통과시키되 그 표본의 재작업 감소 효과는 판별할 수 없다고 한다. 034 [future-study](https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/future-study.md)의 잠정 수치를 가져오지 않았다.

**미확인과 첫 행동:** `forms/run-config.json`의 예산·간격·모집·동의·보상·표본수·중단·품질경계·최소 노동차이·추정/다중비교 규칙은 미합의다. 이 값과 외부 사람 채점 검토 전에는 시험을 시작하지 않는다. 첫 재개 자료는 익명12개 입력과 요구별 채점표이며, 사람 두 명의 독립 판독을 봉인한 후 원문 근거로 조정할 계획이다. 이번 작업은 누구에게도 연락하거나 사람을 배정하지 않았다.
