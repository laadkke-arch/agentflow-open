# 본 표본과 분리한 적용 반례

| 사례 | K/E 실제 구간과 핵심 범위 | 실제 검산과 한계 |
| --- | --- | --- |
| POSIX fnmatch 선두 점 | K 103–703, 1608–2208. E 103–703, 2062–2662. FNM_PERIOD 문단 2138–2448과 PATHNAME 연결 2450–2586은 E에만 통째로 있다. 플래그 없음 규칙 2694–2780은 양쪽에서 잘렸다. | glibc의 같은 패턴 `?rc`와 `.rc`는 flags=0에서 0, FNM_PERIOD에서는 FNM_NOMATCH(1). 구분 슬래시 앞뒤 조건은 FNM_PATHNAME이 함께 있을 때 달라진다. K의 잘린 문장을 정상 규칙으로 일반화해 0을 단정하면 경계에서 틀린다. 이 적용은 봉인 뒤의 반례다. 공식 도메인 직접 열람 미확인. [POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html) · [재게시 본문](https://man7.org/linux/man-pages/man3/fnmatch.3p.html) · [상류 시험의 고정 mirror](https://github.com/coreutils/gnulib/blob/adbe61f5ee7462a6e479f21d75ce51be919b7550/tests/test-fnmatch.c#L388-L450) |
| SVG fill-rule | K/E 모두 11586–12186, 45684–46284. 부호 있는 합 11880–11992만 보인다. 짝홀 규칙 12394–12468과 표의 초기값 10816–10835는 둘 다 빠졌다. | W3C의 같은 별 경로를 수평 이동한 SVG에서 중심 좌표 (110,155)는 evenodd로 false, (365,155)는 nonzero로 true를 받았다. SVG2 본문은 같은 방향의 교차 2회에 parity와 부호 있는 합이 다른 판정을 할 수 있게 한다. SVG 1.1 원 시험과 WPT 수록본은 한 저작이다. [SVG2 §13.4.2](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty) · [W3C 원 시험](https://www.w3.org/Graphics/SVG/Test/20110816/harness/htmlObject/painting-fill-03-t.html) |
| S3 정렬 보조 진단 | 정상 정렬의 첫 키 선택을 그대로 적용해도, 동점군의 삽입 순서를 그대로 단정할 근거는 없다. E는 주 비교에서 정렬 절을 잃고 일반 SELECT 부작용 없음 문장을 가져왔다. | 동일 두 행과 `ORDER BY 1`에 covering index를 추가했다. 기본 조회는 (2,10),(2,9); 인덱스 계획은 (2,9),(2,10). 실행된 두 순서 모두 허용된다. 이 진단은 주 16입력과 별도다. [SQLite ORDER BY](https://sqlite.org/lang_select.html#orderby) · [실행과 구간 좌표](calibration.json) |

조건의 옳은 유형이 화면에 보이는지와 문장에 사전 표지가 있는지는 다른 조건이다. SVG parity와 SQLite RANGE 비수치 처리에는 고른 표지의 핵심 단어가 없다. F4에서는 접근성 경고의 `must not`이 정상 방향 좌표의 설명을 밀어냈다. 세 보조 판단은 사전 답을 수정하는 데 쓰지 않았다.
