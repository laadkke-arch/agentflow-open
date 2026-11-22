# AF-RES-030 · 질문·조건부 안내를 설계하기 위한 사례 기반 입력

**설계 후보:** 추가로 물을 변수를 정하기 전에, 그 변수의 두 가능한 값에 따라 사용자의 후보·용도·판단에 필요한 설명·다음 행동 중 무엇이 달라지는지 적는다. 이미 주어진 조건에서 실행할 수 있는 제한된 행동과 근거가 있으면 그 조건과 링크를 먼저 제시할 수 있다. 질문을 생략하는 것과 불확실성을 숨기는 것은 다르다. 이 문서의 규칙은 관측 사례로부터 만든 검토 대상이며, 질문의 인과효과나 최적 질문 횟수가 검증됐다는 뜻은 아니다.

## 판독 범위와 예시의 지위

- 작성자: Matplotlib 계열을 조사한 별도 에이전트 `/root/matplotlib`. 작성일: 2026-11-22 UTC. Matplotlib의 후속을 이미 읽은 상태에서, 다른 두 계열의 `followup-notes.md`·공급자 원장과 `cross/CROSS_DOMAIN.md`, `cross/sources.jsonl`, 봉인된 `ANALYSIS_RULES.md`를 대조한 **결과 인지 상태의 종합 판독**이다. 독립된 맹검 전수 재코딩이나 새로운 참가자 실험이 아니다.
- Matplotlib 사례는 이 작업자의 원문 직접 판독과 재독에 기초한다. Xarray·DuckDB·타 분야 사례의 아래 설명은 각 담당자가 남긴 원문 위치와 판정을 다시 읽은 종합 검토다. 타 분야의 원 대화를 이 작업자가 새로 전수 판독한 것으로 세지 않는다. 추가 직접 확인한 공급자 파일의 범위는 마지막 절에 명시한다.
- **아래 따옴표 안의 사용자용 문장은 모두 연구자가 새로 작성한 예시이며, 원래 지원자의 발화가 아니다.** 전송·실험·사용성 검사는 하지 않았다. 원래 발화는 별도 열의 permalink로 연결하고 한국어로 요약한다. 이 파일에는 원문 영어 문장의 추가 직접 인용을 넣지 않는다.
- A의 표본, 질문으로 선별된 B, B에서 채택되지 않은 스크리닝 사례, 다른 분야 자료를 서로 다른 근거 층으로 유지한다. 집계 총계는 이 문서에서 재사용하지 않는다. 모든 수치 집계와 시간창은 최종 `RESULT.md`와 원장을 따른다.
- 근거 묶음: [봉인 규칙](ANALYSIS_RULES.md), [Matplotlib 판독](streams/matplotlib/followup-notes.md), [Xarray 판독](streams/xarray/followup-notes.md), [DuckDB 판독](streams/duckdb/followup-notes.md), [타 분야 대조](cross/CROSS_DOMAIN.md). 아래 URL은 역사적 사례와 당시 기술 범위의 근거다. 현재 제품 환경에 그대로 적용할 최신 사용 안내로 제시한 것은 아니다.

## 1. 한 문장을 만들기 전에 확인할 분기

| 설계 조건 | 할 수 있는 선택 | 실제 근거와 경계 | 이 규칙을 깨는 경우 |
| --- | --- | --- | --- |
| 목적과 해당 API 사용이 이미 보이며, 제한된 다음 행동을 지지하는 공식 예제가 있음 | 조건을 붙인 안내와 해당 절 링크를 제시한다. 추가 질문이 필요한 다른 목적은 별도로 남긴다. | M04에서는 [Figure 생성 방식 안내](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370025244) 뒤 [작성자의 교체·해결 보고](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370981028)가 있었다. | 사례의 조건과 다른 GUI 구조·종료 원인이면 같은 안내가 충분하지 않다. 질문이 없었다는 사실만으로 다른 상황에서도 충분하다고 결론 내릴 수 없다. |
| 예제의 값과 실제 입력의 값이 다를 수 있고, 두 값이 다른 진단으로 이어짐 | 대상을 실제 실패 입력으로 고정한 한 변수를 묻는다. | DB04의 [따옴표 여부 질문](https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493265260)과 [작성자의 실제 값](https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493302942)은 예제와 실제 파일을 구분해야 함을 보여 준다. | 실제 입력도 예제와 같다고 이미 확인됐다면 같은 질문을 반복할 이유가 약해진다. 직접 답 뒤 같은 지원자의 새 권고는 관측되지 않았다. |
| 같은 변수의 값이 앞선 작성자 답에서 확인됐고 판·대상이 바뀌었다는 근거가 없음 | 확인된 값을 유지하고, 다음 분기를 가르는 다른 변수만 묻는다. | MB21의 [첫 6.5.0 답](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146) 뒤 [버전 재질문](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506278627), [같은 값 재답](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1507190964)은 확정 중복 사례다. | 다른 셸·다른 인터프리터·환경 변경이 실제로 있으면 재확인이 새 정보를 얻을 수 있다. 그 차이를 질문에 명시해야 한다. |
| 현재 본문에는 값이 있지만 첫 응답 전에 있었는지 복원되지 않음 | 현재 값은 이용하되, 과거 질문이 불필요했다고 확정하지 않는다. | M01의 [버전 질문](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368541658)과 [버전·경고 표시 조건을 함께 준 답](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341). 현재 본문과의 중복은 보이나 최초 공개 시점은 미확인이다. | 공개 원판 또는 첫 답 전 인용이 확보되면 확정 중복으로 바뀔 수 있다. API의 `updated_at`만으로는 그 시점을 확정할 수 없다. |
| 사용자가 지원자의 용어를 이해하지 못함 | 같은 변수의 뜻을 일상적인 구분으로 풀어 쓰고, 모름을 허용한다. | XB14는 [backend 답과 용어 불명](https://github.com/pydata/xarray/issues/7758#issuecomment-1509633511) 뒤 [마운트된 NFS 설명에 대한 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509899467)이 이어졌다. | 풀어 쓴 범주가 실제 구조를 잘못 나누면 더 확신에 찬 오답을 만들 수 있다. 로컬 경로 모양만으로 로컬 디스크라 단정하지 않는다. |
| 지원자가 새 기능이나 예제를 실행해 보라고 함 | 기존 값 회수와 새 실행 요청을 구분해서 기록한다. | MB09의 [버전 질문과 새 환경 제안](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496053940) 뒤 [새 환경의 실행 성공](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688)은 옛 실행 환경의 버전 답이 아니다. | 실행 성공이 생겨도 물었던 기존 값은 여전히 미확인일 수 있다. 두 사건을 같은 변수 직접 답으로 합치면 규칙의 성과가 부풀려진다. |
| 답 뒤 첫 제안이 등장하거나, 후보는 같고 설명만 달라짐 | 첫 제안·설명 수정·후속 실행을 각기 기록한다. | D02의 [실패 경험 질문](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1373853388), [경험과 추가 논거를 함께 준 답](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374537619), [설명 재검토](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686). | 답 전 제안이 없으면 `no_prior_proposal`이다. 설명 수정이 자발적으로 추가한 다른 논거를 받아들인 것이라면 질문한 단일 변수에 효과를 귀속할 수 없다. |
| 사용자의 답이 없지만 제한된 기술 확인은 가능함 | 알려진 조건으로 검토할 수 있는 부분을 진행하고, 미응답 변수는 미확인으로 남긴다. | D05는 [timezone 질문](https://github.com/duckdb/duckdb/issues/12784#issuecomment-2200636928)에 작성자 답이 없고, [지원자의 지역 추정](https://github.com/duckdb/duckdb/issues/12784#issuecomment-2200829808)과 [공급자 수정 PR](https://github.com/duckdb/duckdb/pull/12794)이 있었다. | 추정한 지명·시간대를 작성자 값으로 채우거나 공급자 수정을 사용자 실행 성공으로 세면 틀린다. |

## 2. 사용자에게 보일 한 문장 질문·조건부 안내·근거 링크

이 표의 질문과 안내는 **연구자 작성 예시**다. 행마다 질문을 반드시 해야 한다는 뜻이 아니다. 필요한 값이 이미 있으면 질문 칸을 생략하고 조건부 안내만 쓸 수 있다. 자료가 지지하는 범위를 넘는 완전 해결 약속은 붙이지 않는다.

| 예시 ID·적용 조건 | 한 문장 질문 예시 | 한 문장 조건부 안내 예시 | 원 발화·판정 근거 및 제공자 링크 | 두 값이 갈리는 지점·한계 |
| --- | --- | --- | --- | --- |
| DR01 · Tk 안에 넣는 Figure라는 조건이 확인됨 | 질문 생략 | “Tk 창에 넣을 그림이라면 `Figure`를 직접 만들고 이 예제의 `FigureCanvasTkAgg` 연결 방식을 사용하세요.” | 원 발화는 [M04 안내](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370025244)의 한국어 재구성. [공식 3.6.2 Tk 예제](https://matplotlib.org/3.6.2/gallery/user_interfaces/embedding_in_tk_sgskip.html). | Tk 삽입용 생성과 일반 pyplot 관리의 차이가 다음 행동을 가른다. 모든 GUI 종료 문제의 원인이 이것이라고 보장하지 않는다. |
| DR02 · CSV 예제와 실제 실패 파일이 다를 수 있음 | “실제로 실패한 파일의 null 표시는 따옴표 안에 들어 있나요?” | “따옴표가 있는 입력과 없는 입력을 구분해 같은 판에서 확인하고, 아래 테스트가 추가된 판의 기대값과 비교하세요.” | [DB04 질문](https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493265260)·[답](https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493302942). [공식 고정 테스트](https://github.com/duckdb/duckdb/blob/bd98353fbf2356853ad5603c9a9b51f0ea870cb8/test/sql/copy/csv/parallel/test_parallel_csv.test#L27-L55). | 인용 여부와 null 토큰 설정에 따른 입력 경로를 구분한다. 이 테스트는 보고 당시 0.7.1보다 뒤의 공급자 변경이며, 옛 판에 같은 동작을 소급 보장하지 않는다. |
| DR03 · 버전은 이미 같은 실행 셸에서 답했고 backend 선택이 아직 불명 | “문제가 나는 그 셸에서 `matplotlib.get_backend()`는 무엇을 반환하나요?” | “확인된 버전은 유지하고, 선택된 backend와 이 판의 IPython GUI 매핑이 맞는지 먼저 비교하세요.” | [MB21 이미 준 버전](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146), [후속 backend 발견](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1523636888), [당시 IPython 매핑](https://github.com/ipython/ipython/blob/396593e7ad8cab3a9c36fb0f3e26cbf79cff069c/IPython/core/pylabtools.py#L17-L38). | 같은 설치 버전이라도 선택된 backend가 다르면 다음 점검이 달라진다. 이 명령은 연구자 예시이며 원래 첫 질문이 아니다. 특정 magic 명령으로 완전 해결됐다는 작성자 실행은 확인되지 않았다. |
| DR04 · 서버·파일시스템 용어가 전달되지 않음 | “그 파일 경로는 컴퓨터 안의 디스크에 저장된 파일인가요, 아니면 다른 컴퓨터의 저장소를 연결한 경로인가요?” | “연결된 저장소라면 파일 경로와 네트워크 오류를 함께 확인하되, 이 재시도 코드를 데이터 열기 전체의 시간제한으로 해석하지 마세요.” | [XB14 설명 전 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509633511)·[설명 후 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509899467). [netCDF4 접근 경로](https://github.com/pydata/xarray/blob/a4c54a3b1085d7d8ab900f9a645439270327d2c3/xarray/backends/netCDF4_.py#L87-L110)·[재시도 구현](https://github.com/pydata/xarray/blob/a4c54a3b1085d7d8ab900f9a645439270327d2c3/xarray/backends/common.py#L61-L83). | backend와 파일 저장 경로는 다른 변수다. NFS라는 답만으로 HTTP 원격 인덱싱의 재시도 정책을 적용할 수 없고, 전체 API timeout은 미확인이다. |
| DR05 · 현재 입력에 NumPy 버전은 있고 경고 노출 방식이 불명 | “문제가 나는 실행에서는 경고를 항상 표시하도록 설정했나요?” | “NumPy 1.24의 정수 변환 경고와 경고 필터를 나누어 확인하면, 같은 코드에서 경고가 보이는 조건을 비교할 수 있습니다.” | [M01 답의 버전과 자발적 경고 조건](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341). [NumPy 1.24 릴리스 노트](https://numpy.org/doc/1.24/release/1.24.0-notes.html). | 표시·필터 조건이 다르면 관측된 경고 여부가 달라질 수 있다. 이는 사후 발견에서 만든 질문 예시다. 지원자가 실제로 이 질문을 했다는 뜻도, 최초 버전 질문이 확정 중복이었다는 뜻도 아니다. |
| DR06 · 지금 결정할 선호이며 과거 값 회수가 아님 | “이번에는 기존 코드와의 호환성과 특수 처리를 줄이는 것 중 무엇을 우선해 선택할까요?” | “여기서 정한 우선순위는 지금의 선택으로 기록하고, 처음부터 있던 필수 조건과는 구분하겠습니다.” | [XB03 추가 맥락](https://github.com/pydata/xarray/issues/7721#issuecomment-1510169910)·[후속 특수 처리 선호](https://github.com/pydata/xarray/issues/7721#issuecomment-1516251985), [MB01 후발 값 조정](https://github.com/matplotlib/matplotlib/issues/25599#issuecomment-1495047091). | 이 예시는 선택을 돕는 문장이다. 답을 과거부터 고정된 숨은 목표로 쓰지 않는다. 두 선택지가 실제 사용자의 대안을 모두 포함한다는 보장도 없으므로 다른 우선순위를 허용한다. 기술적 정답 문서로 선호를 검증할 수는 없다. |
| DR07 · 새 재현 입력을 만들어야 하는 단계 | “Tk 요소를 뺀 최소 예제에서도 같은 종료 충돌이 나오는지 실행해 주실 수 있나요?” | “단일 GUI 구성에서도 재현되면 그 예제로 원인을 좁히고, 사라지면 두 구성의 차이를 다음 점검 대상으로 삼겠습니다.” | [M08 원 질문](https://github.com/matplotlib/matplotlib/issues/28513#issuecomment-2211418254)·[여전히 두 구성이 섞인 재실행](https://github.com/matplotlib/matplotlib/issues/28513#issuecomment-2211433918). [공식 3.9.1 이벤트 루프 설명](https://matplotlib.org/3.9.1/users/explain/figure/interactive_guide.html). | 새로운 입력·새 실행을 요청하는 문장이므로 기존 환경 사실의 직접 답과 분리한다. 혼합 구성을 유지한 실패 보고는 유용하지만 요청한 조건을 채운 직접 답은 아니다. 재현이 사라져도 혼합이 유일 원인이라는 증명은 아니다. |
| DR08 · 글꼴 후보의 지원 범위와 요구의 차이를 설명해야 함 | “글꼴을 다음 실행에서도 별도 등록 없이 찾는 것이 필수인가요?” | “현재 세션에서 등록하는 용도라면 `addfont`를 볼 수 있지만, 재시작 뒤 자동 검색까지 이 API 하나가 보장한다고 설명하지는 않겠습니다.” | [M03 후보 평가 질문](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1369957180)·[현재 세션만 된다는 답](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1370065191). [3.6.2 API](https://matplotlib.org/3.6.2/api/font_manager_api.html)·[구현](https://github.com/matplotlib/matplotlib/blob/v3.6.2/lib/matplotlib/font_manager.py). | 요구가 이미 분명하면 질문을 생략하고 범위 설명을 한다. M03의 현재 본문에는 지속성 목적이 보인다. 그 최초 공개 시점과 재시작 후의 전체 목표 성공은 미확인이다. |
| DR09 · 같은 입력의 다음 실행은 가능하지만 기존 환경 값은 불명 | 질문 생략 가능 | “독립된 새 환경에서 같은 입력을 실행해 보되, 성공하더라도 이전 환경의 실제 실행 버전이 확인된 것으로 기록하지는 않겠습니다.” | [MB09 질문과 즉시 행동](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496053940)·[새 환경 성공](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688). [당시 Cartopy 설치 안내](https://scitools.org.uk/cartopy/docs/v0.21/installing.html). | 새 환경 성공은 실행 경로 차이를 시사하나 원래 환경의 결함 변수를 하나로 특정하지 못한다. 설치 방식의 공존 자체를 원인으로 단정하지 않는다. |
| DR10 · 요구하는 window 범위가 명시됨 | “원하는 마지막 값은 현재 행까지의 범위인가요, 전체 partition의 마지막인가요?” | “전체 partition의 마지막이 목적이라면 함수 이름뿐 아니라 frame의 끝 범위도 함께 확인하세요.” | [D08 첫 안내](https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203075138)·[작성자 실행](https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203153988)·[지원자의 정정](https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203186542). [당시 공식 window 문서](https://github.com/duckdb/duckdb-web/blob/b0d70dc34c4bbd2685d89ad22b10287f0c217a80/docs/sql/window_functions.md). | 요구 범위가 이미 보이면 질문 없이 안내한다. 실제 D08은 추가 정보 질문 없이 실행을 보고한 사례다. 그 성공이 첫 답의 alias 설명까지 옳다고 승인하지는 않는다. |

DR02·DR04·DR05·DR07은 서로 다른 목적을 가진 질문이다. 각각 실제 입력 확인, 용어 해석 조정, 재현 조건 회수, 새 실행 요청이다. 모두 물음표가 있다고 해서 같은 종류의 정보 편익으로 집계하지 않는다. DR06은 사용자가 지금 선호를 정하도록 돕는 것이며, 기존 선호를 그대로 찾아냈다는 검증과 다르다.

## 3. 답 뒤 무엇이 달라졌는지 보존할 최소 구분

**답변의 존재보다 답의 대상과 순서를 확인한다.** [C-L1 학년 사례, p.269](https://journals.ala.org/index.php/rusq/article/viewFile/3946/4432)에서는 질문해도 되는지에 대한 허락이 학년 값의 답으로 오인될 수 있다. MB09의 새 환경 성공과 X04의 새 호출 성공 역시 실행 보고를 기존 변수의 답으로 오인할 수 있는 소프트웨어 사례다. [X04 실행 댓글](https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571) 뒤 [entrypoint 설명](https://github.com/pydata/xarray/issues/7411#issuecomment-1375736147)이 나왔으므로, 나중 설명이 앞선 성공을 일으켰다는 순서로 쓰지 않는다. [당시 rioxarray 배포 설정](https://github.com/corteva/rioxarray/blob/0.13.3/setup.cfg)은 backend 등록이라는 제한 명제를 지지하며 전체 GeoTIFF·메타데이터 목적의 성공을 보장하지 않는다.

| 기록할 사건 | 인정할 수 있는 것 | 함께 남길 제외·보류 |
| --- | --- | --- |
| 같은 변수·대상·판에 대한 작성자의 값 | 기존 사실의 새 공개 또는 기존 공개 값의 재진술 | 일부 변수만 답함, 다른 입력·버전, 허락, 제3자 추정, 새로 선택한 목표 |
| 답 뒤 처음 구체적인 후보를 제안함 | `no_prior_proposal`; 정보 뒤 첫 제안 | 이전 후보에서 바뀌었다는 표현 금지. 질문이 없었을 때도 같은 제안이 가능했는지 미확인 |
| 같은 후보의 설명·옵션이 달라짐 | 무엇을 얼마나 바꿨는지 구체적인 항목 | 단순 문구 추가와 사용자의 다음 판단을 바꿀 설명을 구분. 실제 수용·실행과 분리 |
| 답 전후 같은 지원자가 답을 명시적으로 받아 다른 행동을 제안함 | 연결된 권고 변경의 후보 | 다른 발신자의 개입, 작성자의 자발적 추가 정보, 공급자 기능 변경을 함께 적음 |
| 작성자가 새 실행의 코드·출력·결과를 보고함 | 해당 입력·목적·판에서의 성공 또는 실패 | 감사, 종료, PR 병합, 공급자 자체 테스트, 다른 파일·다른 Python에서만 성공은 분리 |
| 충분히 읽은 창에 작성자 답이 없음 | 관측창 안의 무응답 | 삭제·페이지 누락·비공개 기록은 관측 불능. 완전 창과 접근 실패를 같은 빈 값으로 쓰지 않음 |

M01에서 답 뒤 지원자가 재현한 것은 진단상의 진전이다. [버전·경고 설정을 함께 준 답](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341)과 [지원자의 재현](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368556640) 사이에서 질문한 버전 한 변수와 자발적으로 준 경고 설정의 기여를 분리할 수 없다. D02에서도 경험 여부에 대한 답과 동시 실행 논거를 한 댓글에서 받은 뒤 설명이 바뀐다. 이렇게 **설명 수준이 달라진 사례**를 후보 교체나 단일 변수의 효과로 바꾸지 않고 남기는 것이 설계 판단에 더 유용하다.

## 4. 규칙의 양쪽을 시험하는 실제 반례

| 반례 묶음 | 관측된 원문 연결 | 어느 단순 결론이 깨지는가 | 남은 미확인·설계 반영 |
| --- | --- | --- | --- |
| MB07 · 처음에는 즉답, 뒤에는 목적 질문 | [나중 목적 질문](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496169583) → [사용자가 축을 바깥에 추가한다는 답](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1496337035) → [같은 지원자의 구현 방향](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498195823) → [작성자 코드의 출력 성공](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774) | 질문은 항상 불필요한 지연이라는 결론이 깨진다. 기존 안내가 목표를 다 설명하지 못한 뒤 목적 공개와 구체적인 다음 행동이 관측됐다. | 다른 지원자의 설명과 작성자 자체 코드가 매개했다. 질문 한 변수만의 효과는 아니다. 최초 답에 질문이 없어 B에 선정되지 않은 스크리닝 사례이며 주 분모에 올리지 않는다. |
| MB21 · 중복 질문에도 답과 실행이 이어짐 | [버전 직접 답](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146) → [같은 버전 재질문](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506278627) → [반복 값과 새 시험 결과](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1507190964) → [구체 import의 새 성공](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1522271486) | 답이 왔으니 질문이 유용했다는 결론과, 중복 질문이 있으면 대화가 반드시 중단된다는 결론이 모두 깨진다. | 중복 값 외에도 여러 테스트·작성자 디버깅·다른 제공자의 설명이 있었다. 반복 질문이 성공에 필요했는지, 생략했을 때 걸릴 시간은 미확인이다. |
| M04·D08 · 추가 정보 질문 없이 구체 실행 | [M04 API 교체·해결](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370981028), [D08 함수·frame 변경 결과](https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203153988) | 사용 전 질문을 하나 더 해야 성공한다는 일반 규칙이 깨진다. | M04는 공식 예제와 좁은 목표가 연결됐다. D08은 링크가 둘이었고 최초 기술 설명의 일부는 나중 정정됐다. 한 링크 전달만의 효과로 단순화하지 않는다. |
| M07·D05 · 질문 무응답과 다른 진행 | [M07 첫 질문](https://github.com/matplotlib/matplotlib/issues/28511#issuecomment-2211377162), [공급자의 대안 설명](https://github.com/matplotlib/matplotlib/issues/28511#issuecomment-2245186842), [D05 공급자 PR](https://github.com/duckdb/duckdb/pull/12794) | 질문에 답이 없으면 지식·코드가 전혀 진행하지 못한다는 결론이 깨진다. | 원 작성자의 질문값·같은 목적 실행은 끝내 미확인이다. 제3자의 진행이 작성자 성공을 대신하지 않는다. M07의 원하는 모양 이미지는 다른 scatterplot이며 원 histogram의 다열 성공이 아니다. |
| XB13 · 다른 입력에서 성공 | [기존 파일 실패와 변수 답](https://github.com/pydata/xarray/issues/7754#issuecomment-1509390748), [다른 파일·다른 Python에서 동작](https://github.com/pydata/xarray/issues/7754#issuecomment-1510522371) | 성공이라는 단어가 있으면 같은 목적의 같은 입력이 해결됐다는 결론이 깨진다. | 입력과 실행 환경이 함께 바뀌었다. 원 파일에서 필요한 engine 시험의 결과는 미확인이다. |
| C-L1 · 질문 없이 정확한 자료 전달, 질문 뒤에는 지시대상만 교정 | [참고상담 논문 pp.264·277·279](https://journals.ala.org/index.php/rusq/article/viewFile/3946/4432): 양식 번호가 명확한 요청에는 링크 전달, 인물 확인 질문에는 다른 인물이라는 직접 답 | 질문 없는 자료 전달을 실패라 할 수 없고, 직접 답만으로 다음 사용 성공을 선언할 수도 없다. | 양식 다운로드·실제 사용, 인물 교정 뒤의 추천은 공개 발췌에서 미확인이다. |
| C-S4 · 정의 설명 뒤 값이 바뀌는 두 방향 | [NHIS 보고서 pp.9–10·17–18](https://wwwn.cdc.gov/QBank/report/Wilmot_2023_NCHS_NHIS1.pdf): 용제 정의 뒤 경험을 떠올린 사례와, 시각재활 질문 뒤 의도 밖 약물·추적진료를 포함한 사례 | 설명을 추가해 긍정 답이 늘면 더 정확한 답을 얻었다는 결론이 깨진다. | 범주 이해 교정과 범주 오염이 모두 가능하다. 답의 방향보다 실제 대상이 정의에 맞는지 확인해야 한다. |

MB07의 기술 지지는 [고정 프레임 크기 구현](https://github.com/matplotlib/matplotlib/blob/8ca75e445d136764bbc28d8db7346c261e8c6c41/lib/matplotlib/animation.py#L352-L360)과 [당시 bbox 조정 구현](https://github.com/matplotlib/matplotlib/blob/v3.7.1/lib/matplotlib/_tight_bbox.py)에서 제한적으로 확인된다. 후자는 내부 API이므로 이 사례의 성공 코드를 그대로 안정된 제품 권고로 만들지 않는다. MB07은 목적 질문이 다음 행동을 구체화하는 장면을 보여 주고, MB21은 이미 답한 환경 값을 다시 받아도 원인 규명이 자동으로 진전하지 않음을 보여 준다. 두 사례를 함께 보아야 질문 유무만을 기준으로 평가하는 오류를 피할 수 있다.

## 5. 목적 회수와 새 선호 형성을 구분하는 설계

“무엇을 원하나요?”라는 질문은 이미 정해진 목표를 드러낼 수도 있고, 사용자가 가능한 대안을 처음 보고 목표를 바꾸게 할 수도 있다. [Census Q18, pp.4-40–4-42](https://www2.census.gov/library/working-papers/2023/adrm/cbsm/rsm2023-12.pdf)에서는 논의·재독 뒤 태도 답이 달라졌으나 정확한 추가 질문과 개인별 계보가 충분히 공개되지 않았다. 같은 보고서의 Q20은 표현 조건 뒤 서로 다른 방향의 태도 변화를 보여 준다. 이 자료만으로 각 개인이 원래 의견을 회상했는지, 새 의견을 형성했는지 구분할 수 없다.

따라서 현재 사용자가 정하는 선호에는 **선택 시각과 제시된 대안**을 붙이고, 회수한 기존 사실에는 **그 사실이 적용된 시점·대상과 확인 근거**를 붙인다. MB01의 후발 여백 값 조정, XB03의 후발 특수 처리 선호, DB07의 기본 구현 외 대안 수용 여부는 모두 시간 표시가 필요한 후보다. 현재 본문을 과거의 선호라고 소급하지 않는다. [DB07 목적 반복 답](https://github.com/duckdb/duckdb/issues/6947#issuecomment-1493849083) 뒤 [index 생성 위치를 묻는 다음 질문](https://github.com/duckdb/duckdb/issues/6947#issuecomment-1494488354)은 목적을 다시 확인하는 것과 실제 구현 분기를 가르는 위치를 확인하는 것이 다른 단계임을 보여 준다.

범주를 먼저 강하게 제시하는 방식에도 반증이 필요하다. [BLS의 공식 여행 면접 절차](https://www.reginfo.gov/public/do/DownloadDocument?objectID=135305101)는 처음 자유회상과 뒤의 누락·중복 확인을 나눈다. 이는 절차 자료이며 실제 사용자의 성공 기록은 아니다. [인지면접 probe 비교 연구](https://majournals.bib.uni-mannheim.de/mda/article/download/2025.02/384/747)의 가상 코딩 예와 실제 면접 집계도 구분해야 한다. 사용자가 제시된 표현에 동의한 답을 자발적으로 그 개념을 사용했다는 증거로 바꾸지 않는다.

## 6. 설계 후보를 뒤집을 검사와 다음 조사

다음 표는 **향후 검사 설계**다. 이 문서 작성 과정에서 새 당사자에게 질문을 보내거나 전략을 무작위 배정하지 않았다. 현재 사례로 인과효과를 추정하지 않으며, 관측된 대기 시간을 클릭·읽기·대체 노동 시간으로 바꾸지 않는다.

| 검사 ID·검사할 주장 | 입력·판정 절차 | 반증 기준 | 다음 첫 자료 또는 실행 |
| --- | --- | --- | --- |
| F01 · 한 변수 질문이 실제로 다른 분기를 가름 | 후속을 가린 요청·첫 응답·당시 제공자 근거를 주고, 질문할 변수와 두 값에 따른 후보·용도·다음 행동을 먼저 적는다. 값별 공식 지지의 범위를 표시한다. | 두 값 모두 같은 제한 행동을 지지하거나 달라진다는 기술 근거가 없는데 의무 질문으로 막으면 규칙을 수정한다. 진단 목적의 새 정보 질문은 `no_prior_proposal`로 따로 평가한다. | 봉인 `questions.csv`의 예상 분기와 `providers.jsonl`의 한계 열을 사례별로 대조한다. 현재 파일을 후속 지식으로 덮지 않는다. |
| F02 · 같은 값 회수와 새 실행을 올바르게 나눔 | MB09·X04·M08·XB13·참고상담의 허락 답을 순서를 보존한 평가 입력으로 사용하고, 변수·대상·판별 답을 채운다. | 새 환경 성공·새 호출·다른 파일 성공·허락을 이전 변수의 직접 답으로 채우면 실패다. 일부 답은 변수별로만 채운다. | [MB09 성공 댓글](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688)과 `chains.jsonl`의 요청 변수부터 읽는다. |
| F03 · 이미 알려진 값을 다시 묻지 않음 | MB21의 첫 버전 답까지만 제공한 조건과, 실제 실행 셸 변경을 명시한 별도 연구자 합성 조건을 나눈다. 합성 조건은 원 관측이 아님을 표시한다. | 셸 변화 없는 조건에서 같은 버전만 재요청하거나, 셸이 달라진 조건에서 옛 값을 무조건 재사용하면 실패다. | [첫 버전 직접 답](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506138146)을 고정 입력으로 한다. 합성 대조는 이후 별도 파일·명세로 만들며 현재 미실시다. |
| F04 · 원판 미확인을 중복 확정으로 바꾸지 않음 | M01·M06·XB08의 current body, 첫 답, 공개 편집 근거를 구분해 판독한다. | 현재 값이 보인다는 이유로 최초 공개 시점까지 확정하거나 `updated_at`만으로 원판을 복원하면 실패다. | M01의 첫 답 이전 제목·본문 공개 이력 또는 당시 인용을 우선 찾는다. 원판이 없으면 U 등급을 유지한다. |
| F05 · 쉬운 설명이 오답을 유도하지 않음 | XB14와 C-S4의 두 방향 사례에서 설명 전후 답의 지시대상을 기록한다. 기술 용어를 쉬운 말로 바꾼 뒤에도 다른 저장 경로나 범주가 빠졌는지 확인한다. | 값은 얻었지만 실제 대상을 잘못 분류하거나 모든 원격 저장소에 같은 timeout 설명을 붙이면 실패다. | [C-S4 pp.9–10·17–18](https://wwwn.cdc.gov/QBank/report/Wilmot_2023_NCHS_NHIS1.pdf)과 XB14 답을 별도로 대조한다. 정확한 자유 probe 원대화가 없다는 한계를 유지한다. |
| F06 · 권고 변경의 연결이 단일 변수에 과잉 귀속되지 않음 | MB07·M01·D02·M03에서 발신자, 자발적 추가 정보, 이전 제안, 새 코드, 공급자 변경을 시간순으로 분리한다. | 다른 지원자의 제안, 답에 추가된 다른 사실, 작성자 자체 코드를 제거해도 같은 변화가 입증된다고 주장하면 실패다. | [MB07 작성자 코드](https://github.com/matplotlib/matplotlib/issues/25608#issuecomment-1498321774)와 앞선 다자 설명을 함께 읽는다. 관측만으로 제거된 세계의 결과를 채우지 않는다. |
| F07 · 질문 없는 안내도 기술적으로 정확해야 함 | M04와 D08에서 제한된 공식 지지, 작성자 실행, 지원자 후속 정정을 따로 판정한다. | 실행 성공을 근거로 최초 설명의 모든 명제까지 승인하거나, 질문이 없다는 이유로 잘못된 안내를 면제하면 실패다. | [D08 후속 정정](https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203186542)과 당시 window 문서의 frame·alias 절을 읽는다. |
| F08 · 미응답·관측 불능·늦은 결과를 나눔 | 완전 관측된 무응답, 삭제·페이지 누락, root+90일 밖의 답을 각각 포함한다. root+30일·root+90일·질문+30일을 따로 마감한다. | 빈 칸을 모두 무응답으로 세거나 XB06의 늦은 질문을 초기 창에 넣고, XB08의 늦은 실행을 root90 성공으로 넣으면 실패다. | `chains.jsonl`의 window 플래그·pagination 영수증과 [XB08 늦은 성능 보고](https://github.com/pydata/xarray/issues/7730#issuecomment-1709120441)를 확인한다. |
| F09 · 질문이 정확도와 비용에 주는 영향은 별도 검증이 필요함 | 향후 동의받은 통제 연구에서는 정답이 확인 가능한 환경·입력 문제를 정보 충분/범주 애매 조건으로 미리 나누고 전략을 배정한다. 같은 입력의 다음 행동 정확도·실행, 추가 왕복, 실제 작업 시간과 벽시계 대기를 각각 잰다. 선호 형성에는 사실 문제의 정답 기준을 억지로 붙이지 않는다. | 쉬운 조건에서는 질문이 정확도를 올리지 않고 지연만 늘 수 있으며, 애매한 조건에서는 질문 생략이 잘못된 행동을 늘 수 있다. 어느 방향도 사전 배제하지 않는다. | [BLS 통제 연구 pp.2–7](https://www.bls.gov/osmr/research-papers/1999/pdf/st990270.pdf)의 정답 있는 가상 상황·실제 면접·과거 비교군 재사용의 차이를 먼저 검토한다. 새 연구는 제안이며 이 과제에서 시행하지 않는다. |

F09의 필요성은 질문이 항상 도움이 없다는 주장과도 다르다. 해당 BLS 연구는 복잡한 범주 매핑에서 정확도 개선과 더 긴 면접을 함께 관측했고, 단순 매핑에서는 원래 정확도가 높았다. 그러나 과거 비교군을 재사용한 부분, 정답이 있는 가상 상황, 실제 GitHub 사용 목적의 차이가 있어 그 효과량이나 분 단위 비용을 이 과제에 옮길 수 없다. [도서관 평가 절차의 Attachment 3](https://libraries.universityofcalifornia.edu/wp-content/uploads/2012/08/24.7_interim_report_july_09_final.pdf)는 질문이 불필요한 경우를 별도로 두고 질문·정보원·설명·종료를 분리하는 평가 구성을 제공한다. 완료된 대화만 평가한 그 표집을 본 조사에 가져오지는 않는다.

## 7. 미확인의 형태와 재개 자료

| 미확인 | 마지막 확인 위치·이유 | 답을 바꿀 다음 자료 하나 |
| --- | --- | --- |
| M01 버전이 첫 답 전에 이미 공개돼 있었는지 | 현재 root와 첫 버전 질문·답; 공개 원판이 복원되지 않음 | 첫 응답 이전 시점의 공개 본문 또는 제목 변경 이력에서 실제 값이 보이는 버전 |
| MB07 목표 질문을 빼도 같은 코드·실행으로 갔을지 | 여러 지원자와 작성자 코드가 개입한 관측 스레드까지 | 후속을 가린 동일 문제의 사전 등록된 비교 연구; 기존 스레드 추가 열람만으로 반사실적 결과는 복원 불가 |
| MB21 반복 버전 질문으로 늘어난 실제 작업량 | 댓글 시각과 반복 값은 확인, 작성자의 클릭·읽기·실제 작업 시간은 없음 | 동일 시각대 작업 시간의 동의받은 측정; 댓글 간 벽시계 시간을 노동으로 대입하지 않음 |
| 쉬운 질문으로 받은 값이 실제 환경·범주와 맞는지 | XB14의 공개 설명·답과 C-S4의 요약 사례; 독립 환경 기록·모든 자유 probe 부재 | 대상·판을 고정한 공개 재현 입력 또는 공개 승인된 익명 원 면접 발췌 |
| 새 선호가 이전에도 존재했는지 | XB03·MB01의 후발 선택, Census 보고서의 전후 태도 요약 | 대안 제시 전의 공개 진술과 동일인 전후 계보; 없으면 지금 형성·확인한 선호로만 기록 |

## 8. 이 파일 작성 중 추가 직접 확인

아래 확인은 설계 문장의 기술 범위를 좁히기 위한 정적 원문 판독이다. 프로그램 실행이나 작성자 환경 재현이 아니다. 이 파일을 신규 실측 사례나 별도 독립 사람 수에 더하지 않는다. 원장 합산 여부는 통합자가 중복 그룹을 확인해 결정한다.

| 자료·URL | 판·직접 읽은 절 | 확인 UTC·SHA256 | 확인한 내용·한계 |
| --- | --- | --- | --- |
| [IPython 공식 소스](https://github.com/ipython/ipython/blob/396593e7ad8cab3a9c36fb0f3e26cbf79cff069c/IPython/core/pylabtools.py) | 고정 커밋 `396593e7ad8cab3a9c36fb0f3e26cbf79cff069c`, L15–65 | 2026-11-22T07:44:24.149665Z; `49f41456b3ef69fd32ac11a599826f20e39a50e8201a904a4b9bc3bdb7705c91` | 이 판의 GUI 이름과 backend 매핑에서 qt·qt5·qt6 선택이 구별됨을 확인. MB21의 설치된 IPython 전체 환경이나 마지막 제안의 실행 성공을 새로 검증한 것은 아님. |
| [DuckDB 공식 CSV 테스트](https://github.com/duckdb/duckdb/blob/bd98353fbf2356853ad5603c9a9b51f0ea870cb8/test/sql/copy/csv/parallel/test_parallel_csv.test) | 고정 커밋 `bd98353fbf2356853ad5603c9a9b51f0ea870cb8`, null 토큰 관련 L32–55 | 2026-11-22T07:44:24.146092Z; `86b4055733021518d5c065c6f52cec63c12d0781e680f14f751652cac853c76a` | null 토큰 설정·parallel 경로별 기대 결과를 다시 읽음. 기존 DP03과 동일 원문이며 새 최소수로 세지 않음. 보고 당시 0.7.1의 동작·CI 실행·작성자 사용은 검증하지 않음. |

작성 과정에서 기존 stream·봉인 파일·집계·Git 상태는 수정하지 않았다. 설계 예시의 실제 전송, 역사적 환경 재현, 새 참가자 검사, 전략 효과 추정은 미실시다. 이 문서가 제공하는 것은 구체적인 질문의 대상·시점·기술 분기와, 그 판단을 틀렸다고 판정할 수 있는 조건이다.
