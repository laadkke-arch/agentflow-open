| 요구 ID | 목적·제품판 | 보기 N·I·D | 읽은 원문 주소·절 | 두 조작 | 정상·경계 사전 예측 | 후속 실제 출력·주소 | 일치·충돌·미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V01 | 중첩 필드·wrapped facet의 독립 두 y축; 기준5.0.0, 작성자판 미확인 | N | [N](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md) Field / 1) A string representing the data field L28-36 | A=3개 flat 별칭; B=중첩 경로 직접. 같은 입력 안 resolve·집계 유지 | 판별불가. 정상 barley와 경계135행 모두 두 축의 위치를 이 창으로 확정 못함; 알려진 B 실패는 새 예측 아님 | [후속 alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011)는 다른10행·count도 변경. [3alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527)는 resolve/count도 변경. 원135행 A 출력 없음 | 미확인 |
| V01 | 중첩 필드·wrapped facet의 독립 두 y축; 기준5.0.0, 작성자판 미확인 | I | [N](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md) Field / 1) A string representing the data field L28-36; +[I](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/examples/specs/test_aggregate_nested.vl.json) Standalone nested aggregate example L1-36 (72단어·그림0) | A=3개 flat 별칭; B=중첩 경로 직접. 같은 입력 안 resolve·집계 유지 | 판별불가. 정상 barley와 경계135행 모두 두 축의 위치를 이 창으로 확정 못함; 알려진 B 실패는 새 예측 아님 | [후속 alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011)는 다른10행·count도 변경. [3alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527)는 resolve/count도 변경. 원135행 A 출력 없음 | 미확인 |
| V01 | 중첩 필드·wrapped facet의 독립 두 y축; 기준5.0.0, 작성자판 미확인 | D | [N](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md) Field / 1) A string representing the data field L28-36; +[D](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst) Labels introduction / Label with; RST L917-935 displayed words 1-72 (72단어·그림0) | A=3개 flat 별칭; B=중첩 경로 직접. 같은 입력 안 resolve·집계 유지 | 판별불가. 정상 barley와 경계135행 모두 두 축의 위치를 이 창으로 확정 못함; 알려진 B 실패는 새 예측 아님 | [후속 alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011)는 다른10행·count도 변경. [3alias](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527)는 resolve/count도 변경. 원135행 A 출력 없음 | 미확인 |
| V02 | 값 접근과 셀별 표시 제목 동시 보존; 기준5.1.0, 작성자판 미확인 | N | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts) Public CompileOptions interface L24-39 | A=accessor 유지+fieldTitle; B=access escape 삭제 | A만(기준판·공통 조작 조건부). 정상 A/B 값·제목 유지; 경계 A는 접근/표시 분리, B는 접근 보존 실패 | [공개 답](https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846)은 다른 bar 입력·explicit title. [보조 재생](replay/results.json): 연구자 정상 A/B 동일; 경계 A 성공/B compile error, SVG 없음 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| V02 | 값 접근과 셀별 표시 제목 동시 보존; 기준5.1.0, 작성자판 미확인 | I | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts) Public CompileOptions interface L24-39; +[I](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/usage/compile.md) Customized Field Title Formatter L57-72 (68단어·그림0) | A=accessor 유지+fieldTitle; B=access escape 삭제 | A만(기준판·공통 조작 조건부). 정상 A/B 값·제목 유지; 경계 A는 접근/표시 분리, B는 접근 보존 실패 | [공개 답](https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846)은 다른 bar 입력·explicit title. [보조 재생](replay/results.json): 연구자 정상 A/B 동일; 경계 A 성공/B compile error, SVG 없음 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| V02 | 값 접근과 셀별 표시 제목 동시 보존; 기준5.1.0, 작성자판 미확인 | D | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts) Public CompileOptions interface L24-39; +[D](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst) Text tab / text substitutes; RST L945-966 displayed words 85-152 (68단어·그림0) | A=accessor 유지+fieldTitle; B=access escape 삭제 | A만(기준판·공통 조작 조건부). 정상 A/B 값·제목 유지; 경계 A는 접근/표시 분리, B는 접근 보존 실패 | [공개 답](https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846)은 다른 bar 입력·explicit title. [보조 재생](replay/results.json): 연구자 정상 A/B 동일; 경계 A 성공/B compile error, SVG 없음 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| V03 | 고정10행의 zero 범주 라벨만 빨강; 기준5.1.0, 원문 schema2·실제판 미확인 | N | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md) Conditional Axis Properties L119-127 | A=datum.value의 고정 범주 비교; B=datum.resilience 비교 | A만(고정10행). 정상9라벨 A/B 검정; zero1라벨 A 빨강/B 검정. 한 출력의 부분집합 | [작동 진술](https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205)은 그림·판 없음. [보조 SVG A](replay/outputs/V03-fixed-A.svg)/[B](replay/outputs/V03-fixed-B.svg): 1빨강9검정/0빨강10검정 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| V03 | 고정10행의 zero 범주 라벨만 빨강; 기준5.1.0, 원문 schema2·실제판 미확인 | I | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md) Conditional Axis Properties L119-127; +[I](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/examples/specs/line_conditional_axis.vl.json) Standalone conditional axis example L1-39 (114단어·그림0) | A=datum.value의 고정 범주 비교; B=datum.resilience 비교 | A만(고정10행). 정상9라벨 A/B 검정; zero1라벨 A 빨강/B 검정. 한 출력의 부분집합 | [작동 진술](https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205)은 그림·판 없음. [보조 SVG A](replay/outputs/V03-fixed-A.svg)/[B](replay/outputs/V03-fixed-B.svg): 1빨강9검정/0빨강10검정 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| V03 | 고정10행의 zero 범주 라벨만 빨강; 기준5.1.0, 원문 schema2·실제판 미확인 | D | [N](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md) Conditional Axis Properties L119-127; +[D](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst) Using data-defined override for labeling incl. Label Toolbar; RST L1425-1468 displayed words 1-114 (114단어·그림0) | A=datum.value의 고정 범주 비교; B=datum.resilience 비교 | A만(고정10행). 정상9라벨 A/B 검정; zero1라벨 A 빨강/B 검정. 한 출력의 부분집합 | [작동 진술](https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205)은 그림·판 없음. [보조 SVG A](replay/outputs/V03-fixed-A.svg)/[B](replay/outputs/V03-fixed-B.svg): 1빨강9검정/0빨강10검정 | 역사 동일판 미확인; 보조 범주 선택 일치(연구자 조건) |
| L01 | 큰 하단 띠 한 줄 자막 중앙, 작은 띠/무띠 기본 위치; 기준0.15.2·실제판 미확인 | N | [N](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h) ass_set_margins API comment+declaration L356-384 | A=기본 bottom; B=큰 띠에서만 중앙 margin 정책(숫자 미고정) | 판별불가. 정상 B=A는 정책 정의; 큰 띠 중앙 B의 실제 수치·출력 미정 | [후속 설명](https://github.com/libass/libass/issues/588#issuecomment-1028326022)은 정책 가능성. 원첨부는 원하는 비교 도식; 구현된 B·정상/경계 출력 없음 | 미확인 |
| L01 | 큰 하단 띠 한 줄 자막 중앙, 작은 띠/무띠 기본 위치; 기준0.15.2·실제판 미확인 | I | [N](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h) ass_set_margins API comment+declaration L356-384; +[I](https://github.com/Aegisub/aegisite/blob/8dfbd70f89940bf8e327dac80c627b948cb0241c/source/docs/3.2/Styles.html.md) The style editor / Margins L93-100 (87단어·그림1) | A=기본 bottom; B=큰 띠에서만 중앙 margin 정책(숫자 미고정) | 판별불가. 정상 B=A는 정책 정의; 큰 띠 중앙 B의 실제 수치·출력 미정 | [후속 설명](https://github.com/libass/libass/issues/588#issuecomment-1028326022)은 정책 가능성. 원첨부는 원하는 비교 도식; 구현된 B·정상/경계 출력 없음 | 미확인 |
| L01 | 큰 하단 띠 한 줄 자막 중앙, 작은 띠/무띠 기본 위치; 기준0.15.2·실제판 미확인 | D | [N](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h) ass_set_margins API comment+declaration L356-384; +[D](https://www.w3.org/TR/2013/WD-css3-page-20130314/#variable-auto-sizing) 6.3.2.2 Resolving auto widths; HTML L1628-1693 displayed words 1-87 (87단어·그림1) | A=기본 bottom; B=큰 띠에서만 중앙 margin 정책(숫자 미고정) | 판별불가. 정상 B=A는 정책 정의; 큰 띠 중앙 B의 실제 수치·출력 미정 | [후속 설명](https://github.com/libass/libass/issues/588#issuecomment-1028326022)은 정책 가능성. 원첨부는 원하는 비교 도식; 구현된 B·정상/경계 출력 없음 | 미확인 |
| L02 | 동시 흰/노란 자막 내용·시간 보존과 분리; 기준0.17.1, VLC3.0.18만 명시 | N | [N](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_types.h) ASS_Event public structure comment+definition L131-150 | A=원 t·style10/event0; B=흰 event MarginV만 증가(숫자 미고정) | 판별불가. 정상 t 제거는 연구자 보충; 경계 A 실패는 사전 노출, B 이동량·전체 시간 보존 미정 | [후속 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083)은 t 충돌 예외·명시 위치 권고. 원그림 겹침은 이미 알려진 A 실패; B 출력 없음 | 미확인 |
| L02 | 동시 흰/노란 자막 내용·시간 보존과 분리; 기준0.17.1, VLC3.0.18만 명시 | I | [N](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_types.h) ASS_Event public structure comment+definition L131-150; +[I](https://github.com/Aegisub/aegisite/blob/8dfbd70f89940bf8e327dac80c627b948cb0241c/source/docs/3.2/Styles.html.md) The style editor / Margins L93-100 (87단어·그림1) | A=원 t·style10/event0; B=흰 event MarginV만 증가(숫자 미고정) | 판별불가. 정상 t 제거는 연구자 보충; 경계 A 실패는 사전 노출, B 이동량·전체 시간 보존 미정 | [후속 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083)은 t 충돌 예외·명시 위치 권고. 원그림 겹침은 이미 알려진 A 실패; B 출력 없음 | 미확인 |
| L02 | 동시 흰/노란 자막 내용·시간 보존과 분리; 기준0.17.1, VLC3.0.18만 명시 | D | [N](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_types.h) ASS_Event public structure comment+definition L131-150; +[D](https://github.com/qgis/QGIS-Documentation/blob/305f0bb402d3331430ee8490c34f5e2f9d7172fb/source/docs/training_manual/vector_classification/label_tool.rst) 4.2.5 Labeling Lines / curved option through outcome paragraph; RST L222-238 displayed words 1-87 (87단어·그림1) | A=원 t·style10/event0; B=흰 event MarginV만 증가(숫자 미고정) | 판별불가. 정상 t 제거는 연구자 보충; 경계 A 실패는 사전 노출, B 이동량·전체 시간 보존 미정 | [후속 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083)은 t 충돌 예외·명시 위치 권고. 원그림 겹침은 이미 알려진 A 실패; B 출력 없음 | 미확인 |
| L03 | 미충원; 첫18후보 안 세 번째 적격 요구 없음 | N | 미충원; 원문 없음 | 미실시 | 판별불가; 미충원·미실시 | 후속 열람·대조 미실시 | 미충원·미실시 |
| L03 | 미충원; 첫18후보 안 세 번째 적격 요구 없음 | I | 미충원; 원문 없음 | 미실시 | 판별불가; 미충원·미실시 | 후속 열람·대조 미실시 | 미충원·미실시 |
| L03 | 미충원; 첫18후보 안 세 번째 적격 요구 없음 | D | 미충원; 원문 없음 | 미실시 | 판별불가; 미충원·미실시 | 후속 열람·대조 미실시 | 미충원·미실시 |

| 요구 ID | API만으로 판정한 내용 | 같은 분야 예제가 더한 내용 | 타 분야 원전이 더한 내용 | 같은 예산에서 뒤집힌 조작 | 적용이 깨지는 조건 | 설계자에게 줄 링크·용도 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V01 | 중첩 경로 접근은 지원. 복합 facet의 축 배치 승자는 불명 | nested aggregate의 값 접근 예시; dual axis 경계 없음 | QGIS는 속성과 표시 라벨의 대응을 요구; compiler 배치 답 없음 | 관측 0: I=D=판별불가 | 후속 입력·집계·resolve가 함께 달라짐 | [Field](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md)로 경로 문법 확인. [후속 payload](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527)는 차이 확인용; exact A로 재사용 중단 | 원작성판·정상 역사 데이터·135행 A/B 전체 출력 |
| V02 | fieldTitle 옵션 존재만 확인. 경계 예측에는 공통 선택지·창 밖 callback 지식도 들어감 | formatter 용도 설명; titleFormat 오기가 실제 fieldTitle과 다름 | QGIS text substitutes는 접근/표시 분리의 목적을 설명 | 관측 0: 세 보기 모두 A | literal 이름을 accessor로 오인; 한 title을 모든 셀에 복사 | [CompileOptions](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts)+ [Text tab](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst)로 값 접근/표시 변환 책임 분리; 수신판 검증 시 사용 | 작성자판·원래 정상 예제. 보조 정상은 연구자 key-renaming |
| V03 | 축 datum은 label/value/index; resilience 원행 필드를 직접 읽는 B의 근거 없음 | datum.value를 쓰는 조건부 축 예제 | 지물 속성 스타일링은 객체 소유권 질문을 더함; 축에 원행 속성을 추가하지 않음 | 관측 0: 세 보기 모두 A | zero 범주 변경; 구판에서 조건 무시; 모든 라벨 식별로 목표 확대 | [ConditionalAxisProperties](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md)를 먼저 읽고 [scale-domain 설명](https://github.com/vega/vega-lite/issues/7507#issuecomment-856020988)으로 데이터 대응 점검 | 실제 작성자판·일반 데이터용 join. 보조 재생에서 색만 검증 |
| L01 | renderer margin은 screen px. 중앙의 ASS MarginV 수치는 못 정함 | script 좌표 margin·alignment1–9의 기준 | CSS 중앙/overflow·겹침/내용비례 분배; 수평 페이지 규칙 | 관측 0: 세 보기 모두 판별불가 | 화면 px와 PlayRes 혼동; 두 줄/동시 event/zoom; 큰 띠 목표 변경 | [ass_set_margins](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h)와 [CSS §6.3.2.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/#variable-auto-sizing)를 단위·우선순위 명세용으로 사용; 수직 공식으로 적용 중단 | 완성 ASS·frame/띠/폰트·실제판·B 수치 |
| L02 | event에 MarginV·Start/Duration/Layer가 있다는 사실; t 예외는 N창에 없음 | script margin과 bottom 기준; animation/collision 보장 없음 | QGIS 실제 지도는 곡선 지물·가독성 제약으로 일부 라벨 숨김; 자막 내용 보존에는 그대로 적용 불가 | 관측 0: 세 보기 모두 판별불가 | t 제거로 시간변환 변경; 발화/단어 숨김; B 숫자 미정 | [당시 parser](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_parse.c#L668-L726)와 [후속 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083)으로 자동 충돌 예외 확인; 사전 N에 소급하지 않음 | 작성자 libass commit·정상 fixture·B 숫자·전 시간 출력 |
| L03 | 미실시 | 미실시 | 미실시 | 해당 없음: 미충원 | 선정 규칙을 사후 완화하거나 유리한 결과로 대체할 때 | [모집틀](frame.csv)·[제외 사유](streams/libass/selection.md)부터 재개 | 기존 모집틀 안 적격 최초 본문 복원 자료 |

## Q1. 초기 요구에서 꼭 보존할 것은 무엇인가?

**부분 인계다.** 표 1은 예정6요구×3보기의18행, 표 2는 요구별6행이다. 실제 선택은5요구이며 L03을 비워 두었다. 이 범위에서 타 분야 D가 같은 분야 I보다 더 좁힌 사전 예측은 관측0/5다. 공개 후속 자료만으로 작성자의 같은 판·입력·조작을 모두 맞춘 검증은 미확인이다. 별도 연구판 재생 두 요구는 N/I/D가 모두 같은 범주 선택에 도달했다. 이 사실에서 사람이 더 창의적이거나 빨라졌다는 결론을 만들지 않는다.

모집은 UTC 2021-01-01 이상/2025-01-01 미만의 공개 issue, PR 제외, 열린·닫힌 상태 합산이다. 제목의 대소문자를 접은 substring 규칙을 먼저 고정했다. 단어 검색이 복수형·복합어를 놓쳐 Vega 메타데이터400건과 libass 기간 전체200건으로 목록을 대조했다. Vega의 첫40개와 libass의 전체18개 본문을 읽었다. 58개 중 body:null 1개, PR을 가리키는 문장만 있는1개는 실질 최소 저작 수에서 제외한다. [frame.csv](frame.csv), [Vega 선정 기록](streams/vega/selection.md), [libass 선정 기록](streams/libass/selection.md), [원전 집계](evidence/source-counts.json).

| 요구·초기 원문 | 명시된 입력과 목표 | 정상/경계의 차이 | 연구자 추정·보충 및 금지 변경의 근거 |
| --- | --- | --- | --- |
| V01 [#7278](https://github.com/vega/vega-lite/issues/7278), 현재 복원 본문·첨부 asset_data.txt | site별 facet의 bar/line 값과 독립 y축 배치를 보존. 경계 입력135 nested records | 정상 barley는 median(yield)/sum(yield), 경계는 Readability sum/Unit_Key_Message count. 자료·집계·색상도 함께 다름 | 같은 입력 안 A/B의 resolve·집계를 고정한 것은 연구자 통제다. 정상→경계를 nested 하나의 효과로 해석하지 않는다. 저자가 모든 변경을 금지했다고 쓰지 않음 |
| V02 [#7422](https://github.com/vega/vega-lite/issues/7422), 본문 JSON과 PNG 위치 | penguin3행 repeat4×4. literal 점·대괄호 필드의 값과 각 셀 제목/범례 의미를 보존하며 escape 기호를 표시에서 제거 | 특수 이름이 경계. 실제 재생 정상은 같은3행의 일반 이름 복사본 | 외부 정상 예제 자체는 재생하지 않았다. 모든 셀에 한 제목을 복사하지 않고 각 field와 title의 대응을 지키는 조건은 본문 목표를 실행 가능하게 한 통제 |
| V03 [#7507](https://github.com/vega/vega-lite/issues/7507), 본문10행 | resilience=0인 `4. Hygiene & Cleaning` 축 라벨1개를 빨강, 나머지9개를 검정 | 한 출력 안 비zero9개/zero1개. 별도의 정상·경계 실행이 아님 | A의 고정 문자열은 이10행에서만 유효. 미래 어느 범주가 zero인지 자동 추적하거나 모든 라벨의 완전 식별을 보장하는 요구로 확대하지 않음 |
| L01 [#588](https://github.com/libass/libass/issues/588), 본문 비교 조건·원그림 | 작은 띠·무띠에서는 기본 bottom이 좋고, 두 줄을 담는 큰 띠의 한 줄은 중앙에 놓고 싶음 | 띠의 높이와 한 줄/두 줄 구성 | 실제 frame/PlayRes/폰트/ASS/B 수치 없음. 원그림의 원하는 아래쪽 구성은 성공한 엔진 출력이 아님 |
| L02 [#685](https://github.com/libass/libass/issues/685), 본문 ASS·VLC version·원그림 | 두 event는0~5초, 흰 줄에 `\t(1000,1500,\alpha00)`, 흰/노란 글자를 분리하며 내용·시간 유지 | 저자가 t 존재를 경계로 특정. t 제거 정상은 연구자 보충이므로 조건부 충원 | style MarginV10/event0을 구분. t를 없애면 alpha 시간변환도 바뀌므로 그 대조를 원래 animation 요구의 성공으로 세지 않음 |
| L03 | 적격 세 번째 요구 미충원 | 해당 없음 | #598은 본문에 식·workaround·상대 결과가 이미 있음. #600의 Kana나 #835의 줄 길이를 연구자가 정상 대조로 새로 지정해 빈자리를 채우지 않음 |

최초 작성 시점 본문은5요구 모두 복원하지 못했다. current REST body를 이번 세션의 최초 복원 가능 본문으로 썼고, 최초판이라고 부르지 않았다. 후속 timeline에서 #7278/#7422의 옛 제목은 복원했지만 양쪽 모두 후보 단어를 포함해 membership은 변하지 않았다. 나머지 후보의 역사적 제목 순서까지 완전하다고 주장하지 않는다. [SCOPE](SCOPE.md)의 변경 이력과 [후속 복원](streams/vega/outcomes.json)을 함께 남겼다.

## Q2. 두 조작은 실제로 선택 가능했는가?

**참고한 동시대 API판, 작성자의 실행판, 이번 재생판은 별개다.** 공식 tag를 읽었다는 사실만으로 작성자의 runtime을 확정하지 않는다. 사전 선택지 원본은 [operations.json](operations.json), API 조사 뒤 결과 열람 전에 구체화한 변경은 [operation-refinements.json](evidence/operation-refinements.json)에 전후로 보존했다.

| 요구 | 동시대 참고판·직접 위치 | A/B에서 달라지는 속성 | 가용성 판단과 제한 |
| --- | --- | --- | --- |
| V01 | [5.0.0 Field](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md) L28–36; 4.17.0 field 문구도 대조 | 세 nested 속성의 접근 표현만 flat alias로 바꿀지 | 두 표현의 값 접근은 가능. 독립축 배치 bug의 고침은 문법 지원에서 나오지 않는다. 작성자는 schema4만 제공 |
| V02 | [5.1.0 CompileOptions](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts) L24–39 | A는 fieldTitle callback, B는 access 문자열 escape | fieldTitle은 실제 API. usage의 titleFormat 명칭은 오기이며 공통 A를 그 오기로 바꾸지 않음. 표시 변환과 접근 변환의 차이를 고정 |
| V03 | [5.1.0 ConditionalAxisProperties](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md) L119–127 | axis labelColor의 조건식만 value 범주 대 원행 resilience | 5.1.0에서 조건 표현 가능. schema2가 같은 기능을 실행했다는 증거는 없음. 뒤의2.7.0 보조 실행은 두 조건이 모두 버려지는 실제 반례 |
| L01 | [0.15.2 ass.h](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h) L356–384 | 기본 bottom 대 큰 띠에서 수직 margin 중앙 정책 | margin API는 존재하지만 화면 px와 ASS script MarginV는 다름. B의 수치·block 측정·분기 구현을 봉인 전에 고정하지 못해 완성된 두 실행 조작이라고 할 수 없음 |
| L02 | [0.17.1 ass_types.h](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_types.h) L131–150 | 흰 event의 MarginV만0에서 비영으로 | 필드 존재는 확인. 필요한 수치를 못 정했고 style fallback/t 예외는 N창에 없음. 후속 구현을 읽었다고 사전 가용성의 결손을 소급 제거하지 않음 |

실행으로 확인한 것은 연구판5.1.0의 V02/V03 두 요구뿐이다. L01/L02의 두 B가 수치 없이 정책으로 남은 것은 이번 설계의 결손이다. 뒤에서 편한 숫자를 골라 성공시킨 다음 원래 예측의 정답으로 세는 방법을 쓰지 않았다. 명시적 title, `pos`, t 제거, V01의 resolve 삭제는 후속의 제3 해결책이며 봉인 A/B와 구별한다.

## Q3. 수신 분야 정보만으로 어디까지 예측할 수 있는가?

V03의 N은 축 조건이 보는 객체가 label/value/index를 갖는다고 직접 설명한다. 고정10행에서 목표 범주를 `datum.value`로 비교하는 A를 고르는 데 필요한 결정적인 경계는 이 문구에 있다. I의 [조건부 축 예제](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/examples/specs/line_conditional_axis.vl.json) L1–39도 datum.value를 쓰지만 원본 행의 임의 필드를 axis datum에 추가해 주지는 않는다. 이번 보조 출력은 같은 예측을 확인했다.

V02의 N창은 fieldTitle 이름과 타입 위치를 보여 준다. 그 창만으로 callback의 모든 동작과 특수 필드 경계가 설명되지는 않는다. I의 [Customized Field Title Formatter](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/usage/compile.md) L57–72에는 사용 목적이 있으나 titleFormat 오기가 있다. root는 Q2 조사에서 실제 구현·callback 정보를 N창 밖에서도 봤고, 정확 A/B 계약을 세 보기 모두에 제공했다. 따라서 V02의 N=A 예측을 **API 한 절만 독립적으로 읽은 사람의 성과**라고 해석하지 않는다. [cards.csv](cards.csv)의 prior_exposure/outside_window와 [탐색·노출 기록](evidence/search-and-exposure.json)이 이 제한을 담는다.

V01의 nested aggregate 예제는 필드 값 접근을 보여 주지만 wrapped facet+dual axis+문자열 count의 경계는 없다. libass의 I인 [Aegisub3.2 Styles](https://github.com/Aegisub/aegisite/blob/8dfbd70f89940bf8e327dac80c627b948cb0241c/source/docs/3.2/Styles.html.md) L93–100은 script 해상도 단위와 alignment별 margin 방향을 알려 준다. 함께 본 Style editor 그림은 편집기의 설정·미리보기이며, 비디오 frame 안 띠나 두 event 충돌의 실제 출력이 아니다. 두 문서가 동시 event·시간변환·부호/단위 변환을 보장한다고 읽지 않는다.

| 요구 | I 추가창 실제 단어 | D 추가창 실제 단어 | I/D 그림 | 공통 N창 | 제한 |
| --- | ---: | ---: | ---: | ---: | --- |
| V01 | 72 | 72 | 0/0 | 130단어 | code와 문서 산문의 공백 단어는 같은 인지부담을 뜻하지 않음 |
| V02 | 68 | 68 | 0/0 | 33단어 | I 오기 보존; 공통 A와 창 밖 구현 지식이 별도로 있음 |
| V03 | 114 | 114 | 0/0 | 84단어 | I는 시간축 예제, 본문은 명목축·원행 속성 요구 |
| L01 | 87 | 87 | 1/1 | 215표시단어 | N에는 추가창200단어 상한을 적용하지 않음 |
| L02 | 87 | 87 | 1/1 | 54표시단어 | QGIS 실제 지도와 Aegisub UI 그림은 기능·정보밀도가 다름 |

I/D의 추가 상한은 한 절·200단어·그림1점이며 실제 단어·그림 수도5쌍 모두 일치한다. 소스 표시 형식을 정리한 뒤 공백으로 센 값이다. 원문 위치·절단 단어·hash는 [카드](cards.csv), [D 창 기록](evidence/donor-card-windows.json), 각 receiver-candidates에 있다. 중간 문장 절단을 숨기지 않았고, 창 밖 내용을 그 카드가 보여 준 것처럼 쓰지 않는다. 원전군과 탐색 일반 순서는 사전 고정했지만 사례별 정확 질의/tie-break 전체를 별도 사전 커밋하지는 못했다.

## Q4. 다른 분야 원리를 그대로 옮기면 어디서 깨지는가?

| 직접 읽은 선행 원전 | 확인한 규칙·실제 도판 | 수신 요구로 옮길 때 끊기는 연결 |
| --- | --- | --- |
| [W3C CSS Paged Media 2013-03-14 WD](https://www.w3.org/TR/2013/WD-css3-page-20130314/), §6.3.2.2/§6.3.2.4/§6.4, header 예4·6 | 페이지 margin box의 중심과 최소너비, overflow/겹침 사이 우선순위. 원도판을 직접 확인 | L01의 수직 ASS 좌표·글꼴 측정·동시 event·발화 시간에 대한 공식이 아니다. 수평 너비 규칙의 center를 수직 MarginV 수치로 등치할 수 없음 |
| [W3C XSL1.1 2006-12-05 REC](https://www.w3.org/TR/2006/REC-xsl11-20061205/), §4.5/§7.16.13 및 line-area 도판 | nominal/max line rectangle과 wrap-option의 조건 | 줄 영역과 wrap 허용은 자막의 표시 시점·음성 대응·다른 event와의 충돌 회피를 보장하지 않음. 줄 수만 줄이고 내용/시간을 잃으면 수신 목표 실패 |
| [QGIS2.18 User Manual 고정 원본](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst), Labels/Text/Data-defined 절 | 지물 속성·표시 문자열·데이터 기반 스타일을 구분하고 라벨 배치/렌더링 선택을 설명. 원 그림도 확인 | V01의 compiler 축 배치, V02의 JS accessor escape, V03의 axis datum에 원행 속성을 넣는 기능은 보장하지 않음 |
| [QGIS Training Manual 고정 원본](https://github.com/qgis/QGIS-Documentation/blob/305f0bb402d3331430ee8490c34f5e2f9d7172fb/source/docs/training_manual/vector_classification/label_tool.rst), §4.2.5 L222–238 및 최종 지도 | 곡선 라벨 등 설정 뒤 일부 이름이 사라진다는 설명과 실제 지도. 그림 UI는 QGIS2.0.1-Dufour·축척1:4917 | L02의 발화 내용을 숨기면 정적 겹침은 줄여도 목표를 잃는다. 여러 설정이 함께 달라진 도판으로 곡선 하나의 인과 효과·정확 삭제 수를 주장하지 않음 |
| [Ordnance Survey Cartographic Design Principles, 2019 고정판](https://raw.githubusercontent.com/OrdnanceSurvey/GeoDataViz-Toolkit/424bccc4f95f15d354a74c716e62c8592c4b10d3/Cartographic%20Design%20Principles/README.md), Legibility | 지도의 사용 목적에 맞춘 가독성과 표시 선택의 판단을 읽음 | 지도 제작자의 선택적 표시 목표가 모든 자막 event·도표 값을 보존하는 요구와 같지 않음. 실제 판독·채택 효과 자료로 쓰지 않음 |

위 다섯 저작 중 QGIS 두 매뉴얼을 한 계보로 보수적으로 묶어도 인쇄2·지도2로 필수4개를 충족한다. 판·절·도판 관측은 [donor-review](streams/donors/donor-review.md), [figure-observations](streams/donors/figure-observations.json), sources의 D-P/D-M 계보에 있다. 수신 매뉴얼의 다른 장을 D로 세지 않았다.

**무조건 옮기는 규칙의 반례와 카드의 오답은 구분한다.** QGIS의 지물 속성 스타일링을 축 객체에도 그대로 적용해 `datum.resilience`를 읽는 B를 정당화한다면, 5.1.0의 실제 B는 목표 라벨을 검정으로 남긴다. 관측한 것은 B의 실패이고, 그 원인을 객체 문맥 차이로 설명하는 연결은 원문과 API에 근거한 추론이다. 봉인 D는 N의 문맥 제한을 함께 보고 A를 골랐으므로 이를 D의 새 오답으로 세지 않는다. 같은 이유로 지도처럼 자막 일부를 숨기는 조작도 이번 D가 실제 권하거나 실행한 조작이 아니다.

별도 경계 원본도 읽었다. [libass #598](https://github.com/libass/libass/issues/598#issuecomment-1187410504)은 PlayRes·화면 좌표·percent·overscan을 섞었을 때의 실패와 수정식을 보고한다. 최종 성공은 저자 진술이며 GIF는 첫 프레임만 봤다. [#600](https://github.com/libass/libass/issues/600#issuecomment-1055846785)의 두 비교 그림에서는 구두점/괄호 방향·간격이 다르다. 일부 glyph 회전은 실제 세로 조판의 보존 조건을 충족하지 않는다. 두 사례를 선정 규칙 밖의 독립 반례로 남겼으며 동일판 A/B 성공률에 합치지 않았다.

## Q5. 결과를 보기 전에 무엇을 단정했는가?

단계①의 원격 SHA는 `a6b1624c899eacf118c0e01350f52cbd53e21dae`, 단계② 카드·예측 봉인은 `9b13473a76a381fe27d775524aa65416ec28f591`이다. 단계② 서버 commit 시각은 **2026-11-23T01:55:36Z**다. libass 첫 후속 요청 준비는01:56:50.120240Z, Vega 첫 후속 댓글 요청은01:58:10.743Z로 그 뒤다. libass 완료 시각은 별도 기록하지 않았다. [commit-ledger](evidence/commit-ledger.jsonl), [freeze-verification](evidence/freeze-verification.json), 각 followup receipt가 순서를 증명한다.

[predictions.csv](predictions.csv)의18행은 그대로 유지했다. V02/V03의6보기 행은 조건부 A만, V01/L01/L02의9행은 판별불가, 빈L03의3행도 choice=판별불가이되 status=미실시·미충원이다. V03의1/9/10은 원10행에서 정당화한 수치다. 그 밖에는 px/위치 허용차를 뒷받침할 자료가 없어 범주 예측으로 썼다. V02의16셀·48점·32제목은 실행 뒤 센 관측 수이며 사전 수치 예측이 아니다.

원리→수신 속성→관측 연결의 실패 지점도 봉인했다. V01은 속성 접근→값 lookup까지이고 축 배치 연결은 비어 있다. V02는 접근 표현과 표시 표현 분리→정확 field별 title/값 대응이다. V03은 조건이 보는 datum의 소유 필드→목표 identity의 색이다. L01은 center 우선순위→수직 margin 변환에서, L02는 가독성/선택적 표시→모든 event 내용·시간 보존에서 충분한 연결을 얻지 못했다. [cards.csv](cards.csv)의 mapping과 [operation-refinements](evidence/operation-refinements.json)를 대조할 수 있다.

root가 N→I→D를 만들고 전체 파일/API 조사·보조자의 개괄도 일부 먼저 봤다. 세 독립 참가자나 완전 차폐 실험이 아니다. 본문에 이미 있는 실패는 카드의 known_before_seal에 남겼다. 일반 도너 탐색이 A/B 봉인 전 root에게 전달된 노출, V02 callback의 창 밖 지식, 사례별 검색 순서의 불완전한 사전 고정 때문에 출처 자체의 인과 효과는 분리하지 못한다.

## Q6. 후속 자료가 그 예측을 가르는가?

**공개 역사 자료와 이번 보조 실행을 나누면 답이 달라진다.** 공개 자료의5요구×정상/경계×A/B=20논리셀에서 판·입력·조작·새 직접 출력을 모두 맞춘 셀은 관측0/20이다. 이는 실패율0%, 성공률0%, 효과 동률을 뜻하지 않는다. 각 셀에는 무엇이 없어서 판정하지 못했는지 [outcomes.csv](outcomes.csv)와 분야별 outcomes.json에 기록했다. V03의4논리셀도 한 출력의 부분집합이지4독립 실행이 아니다.

| 요구 | 실제 후속에서 확인한 것 | 같은 요구의 검증으로 채점하지 못한 이유 |
| --- | --- | --- |
| V01 | 다른 ecommerce10행의 nested/alias 전후 PNG에서 count 축이 plot 안쪽/왼쪽 대 오른쪽 경계로 달라짐 | 원asset135행과 다름. x만 바꿨다는 설명과 달리 count field도 바뀜. 마지막3alias 입력은 resolve/count/zero 옵션도 바꿈 |
| V02 | 다른 사용자의 dot field 실패 경험과 escaped field+explicit title 제안 | 다른3행 bar 입력. 원repeat의 fieldTitle A 출력 아님. 본문 PNG의 escape 문제는 이미 알려진 baseline |
| V03 | maintainer가 고정 범주 datum.value 조건이 작동한다고 말하고 warn 제거 가능이라 답함 | 코드 진술·종료 처리이며 실제1/9 색 출력·원작성자 실행 수락·runtime 증명이 없음 |
| L01 | 중앙 배치 정책 설명, 두 줄/큰 띠/zoom의 경계, 작성자의 추가 위치 선호 | 요구 도식은 B 실행이 아님. 정상과 경계의 완성 입력/실제 margin 없음 |
| L02 | 후속 답과0.17.1 구현이 t의 collision 예외를 설명. 원그림의 흰/노란 겹침 직접 확인 | 실패는 사전 노출. 실제 libass patch·B margin 값·0~5초 전체 출력 없음. 명시적 pos 권고는 frozen B와 다름 |

Vega 댓글17개/timeline39events, libass 선정 이슈 댓글4개/timeline9events를 읽었다. 이 범위의 연결 PR/commit event는 관측0이며, 번호를 언급하지 않은 패치까지 없다는 뜻은 아니다. [Vega 후속 검토](streams/vega/outcome-review.md), [libass 후속 검토](streams/libass/outcome-review.md). libass 선행 PR384는 미병합, 대체385는2020년 병합을 확인했지만 #588 이전 배경 수정이다. 후속 배당을 채우려고 이를2022년 요구의 해결로 세지 않았다. 같은 이슈의 댓글·첨부는 하나의 요청 저작으로 묶었다.

보조 재생은 결과 열람 전에 고정한 [계획](evidence/replay-plan.md)에 따라 Vega-Lite5.1.0/Vega5.20.2에서 실행했다. V02 정상 A/B는 같은 SVG이고, 경계 A는 각 field 값과 제목 대응을 유지한다. 경계 B는 `Access path missing open bracket: Beak Depth (mm)]`로 compile 실패했다. B의 빈 그림이나0점 출력은 관측하지 않았다. V03은 A=1빨강9검정, B=0빨강10검정이며 SVG와 scenegraph가 일치한다. [재생 결과](replay/results.json), [실행 영수증](replay/render-receipts.json), [셀별·축별 원출력](replay/replay-review.md).

6변형 실행 중5SVG/1compile 실패이며 render 명령의 실제 종료 코드는1이다. 실패를 성공 종료로 덮지 않았다. 분석 명령은0으로 마쳤다. 추가로 출력 뒤 수행한2.7.0/Vega4.4.0 민감도 두 실행은0으로 완료됐고 A/B가 모두 대상10라벨 검정이다. 두 입력 조건은 compiled output에서 사라져 A/B compiled JSON도 byte-identical이다. [sensitivity-results](replay/sensitivity-results.json). compiler와 호환 runtime/의존 묶음을 함께 바꿨으므로 compiler 하나의 격리 효과는 아니다. 원작성자가2.7.0을 썼다는 주장도 아니다.

모든 재생은 현대 Node24.22.3·native canvas 없이 수행했다. 고정 scenegraph가 추정한 글자 폭을 사용하므로 역사적 폰트 픽셀 일치·가독성 실측을 보장하지 않는다. V03의 긴 라벨6개가 줄임표 처리되고 일부 검정 라벨은 원spec 막대가 덮는다. 목표 색 성공을 모든 라벨 완전 식별 성공으로 바꾸지 않는다. [시각 확인과 한계](replay/preview-observations.json).

## Q7. 같은 분야 예제에 비해 새로 확인된 판단이 있는가?

| 요구 | 봉인 I/D | 공개 동일판·입력 비교 | 연구판 보조 비교 | D가 추가한 검증된 선택 |
| --- | --- | --- | --- | --- |
| V01 | 둘 다 판별불가 | 미확인 | 미실시 | 미확인 |
| V02 | 둘 다 A만 | 미확인 | 범주 선택 동률; 정상은 연구자 입력 | 관측0/1 보조 요구. 추가 의미 분리 설명은 있으나 선택 차이 없음 |
| V03 | 둘 다 A만 | 미확인 | 고정10행의 색 선택 동률 | 관측0/1 보조 요구. N이 이미 객체 문맥 경계를 제공 |
| L01 | 둘 다 판별불가 | 미확인 | 미실시 | 미확인 |
| L02 | 둘 다 판별불가 | 미확인 | 미실시 | 미확인 |
| L03 | 미충원 | 미실시 | 미실시 | 해당 없음 |

충원5요구의 선택·정상 예측·경계 예측은 I/D가 모두 같았다(계산5/5). 서로 다른 사전 예측은 관측0/5다. **D의 새 정답 또는 새 오답을 가르는 조건부 분모는0이므로 그 비율은 해당 없음**이다. 공개 자료의 정답 동률은5요구 모두 미확인이고, 별도 보조 조건에서만2요구의 범주 선택 동률이 확인됐다. 18보기 행을18독립 성과로 세지 않는다. [comparison-counts](evidence/comparison-counts.json).

세 가지 반례 요구를 구분해서 답한다. 첫째, 수신 API가 같은 방향을 주는 관측 사례는 V03이다. 둘째, 타 분야 원리를 무조건 옮겨 B를 정당화하면 실패하는 연결은 QGIS의 지물 속성 문맥→axis datum 전이에서 확인된다. 다만 실제 봉인 D는 B를 권하지 않아 **D 새 오답의 관측 사례는 확보하지 못했다**. 셋째, 같은 입력 수준 조작 A가 구판2.7.0과5.1.0에서 다른 출력이 되는 것은 추가 재생에서 관측됐다. libass에서는 선행 margin patch와 외부 엔진 그림까지만 찾았고 동일 ASS의 구판/신판 실제 차이는 미확인이다.

목표 변경과 우연한 동률도 따로 확인했다. V02 정상에서는 조작 A/B가 같은 compiled JSON·SVG를 냈다. V03에서 목표를 색 구분에서 모든 라벨 완전 식별로 바꾸면 줄임표/덮임 때문에 결론이 깨진다. L01 후속의 영상 바로 아래 배치는 처음의 큰 띠 중앙과 다른 목표다. L02에서는 지도식 숨김이나 t 제거로 충돌을 없애도 내용·시간을 보존하지 못한다. 이 차이들을 같은 성공 지표로 합치지 않았다.

더 엄격한 선정 감도에서는 연구자 정상 대조에 의존한 L02를 빼 충원4/6, 별개의 정상/경계 두 입력을 요구해 V03도 빼면3/6이다. 어떤 경우에도 I/D의 상이한 사전 예측은 새로 생기지 않지만, 표본 부족은 더 커진다. Vega 현재40개 안의 exact-word 일치는30/40으로 확인했을 뿐, 별도 exact-word 규칙의 첫40개 전체를 새로 모집한 것은 아니다. 기본 rule를 사후 바꾸어 유리한 결론을 만들지 않았다.

## 대안별 적용 조건과 관점

설계자가 다른 분야 링크를 읽을 실용적 이유에 대한 이번 결론은 **제안**이다. 수신 문서가 두 조작을 모두 허용하고, 추가 원전이 아직 정하지 못한 보존 속성이나 우선순위를 정확히 가르며, 그 연결을 같은 판·입력의 관측으로 확인할 수 있을 때 D를 후보로 줄 수 있다. 이번 표본에서는 그 마지막 구별까지 추가한 사례를 확인하지 못했다. “다른 분야 링크는 쓸모없다”라는 일반 결론으로 확대하지 않는다.

| 관점 | 우선하는 목적 | 이 자료가 주는 링크와 사용 조건 | 적용을 멈출 조건 |
| --- | --- | --- | --- |
| 카드를 선택하는 설계자 | 같은 읽기 예산 안 조작 선택을 좁히기 | V03 axis datum 절, V02 실제 CompileOptions를 먼저 읽고 D는 보존 속성/책임 구분을 명세할 때 사용 | D가 I와 같은 예측만 반복하거나 수신 변수·단위·실패 관측 연결이 없을 때 우월성을 주장하지 않음 |
| 화면 독자 | 도표 값 대응·범주 식별, 자막 내용·순서·시간을 유지 | V03 원출력의 색/줄임표, L02 두 event의 시간·내용을 독립 보존 조건으로 둠 | 중심·겹침 감소 때문에 값 대응이나 발화를 잃을 때 |
| 당시 동작을 보장할 유지보수자 | tag/API 가용성과 호환·재현 | fieldTitle/titleFormat 불일치, t collision 예외,2.7/5.1의 실제 조건 보존 여부를 확인 | schema 문자열만으로 runtime을 추정하거나 제3 조작·새판 성공을 구판 보장으로 제시할 때 |
| 인쇄·지도 원전 제작자 | 페이지 상자 질서, 지정 축척·목적의 지도 가독성 | CSS의 단계별 우선순위, QGIS/OS의 선택적 표기 조건을 원래 매체의 목표와 함께 읽음 | 정적 페이지/지물 규칙이 동적 발화 시간이나 axis datum까지 보장한다고 옮길 때 |

각 카드의 짧은 용도·중단 조건은 표2와 위 표에 있다. D 링크의 역할은 관측되지 않은 창의성·채택·시간 절약을 약속하는 것이 아니다. 추가 단어 수는 맞췄지만 정보밀도·판·예제 유형·노출이 같지 않아 D의 내용만 분리한 인과 효과는 산출하지 않았다.

## 원문·검사·잔여 작업의 수용 상태

source 원장은 **188행**, 보수적 고유 1차 저작은 **71개**다. 검색/실패/내부 결과/재생 도구·metadata를 최소수에서 제외했고, 같은 이슈의 여러 댓글·그림·첨부와 같은 매뉴얼 발췌를 중복 세지 않았다. 고유 수의 다수는 선정에서 제외한 후보 원문이다. 총수22 충족과 필수 역할 배당 충족은 별개다. 계보별 source ID와 행은 [source-counts.json](evidence/source-counts.json)에 있다.

| 필수 배당 | 확인/요구 | 상태·경계 |
| --- | ---: | --- |
| 요청자 선정 원문 | 5/6 | L03 미충원. 최초 작성 본문판은5건 모두 미복원 |
| 동시대 공식 설명·독립 예제 | 5/4 | Vega 문서+구현을 한 계보로 보수화하고 독립 예제2, libass API, Aegisub를 배당 |
| 인쇄·지도 원전 | 4/4 | 인쇄2·지도2. QGIS 두 매뉴얼을 한 계보로 병합한 보수적 수 |
| 새 독립 공개 후속 수정·시험·출력 저작 | 0/6 | 선정 이슈의 후속 논의5개는 요청 저작과 중복. 자체 SVG와 선행 PR을 대신 넣지 않음 |
| 독립 경계/반대 사례 | 2/2 | libass #598/#600. 주표본 밖 사례이며 한계 유지 |

자체 검토는 [SELF_CHECK.md](SELF_CHECK.md)의 Q1~Q7 주장/직접근거/반증/반전 조건/최소 재개 자료에 있다. 같은 모델 보조자의 [사전 방법 검토](streams/donors/method-review.md)와 [후속 원장 교차 검토](streams/vega/final-ledger-review.md), [최종 서술·수용 원장 교차 검토](streams/libass/final-report-review.md)를 실제 수행 범위대로 기록했다. 사람 독립 검토는 미실시다. [validate.py](validate.py)는18ID·5예산쌍·봉인 불변·source 필드/계보·두 표/질문 형식을 검산한다. 이 검사의 통과는 연구 결손의 충족을 뜻하지 않는다. 요건별 분자·분모·단위·파일 행은 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 있다.

최소 재개는 원작성자의 실제 renderer build와 동일 입력·조작의 전체 후속 출력을 확보하는 일이다. V01은135행+역사 barley, V02는원repeat+원래 정상, V03은원10행과 실제patch가 필요하다. L01은완성 ASS/frame/띠/폰트와B계산, L02는VLC 포함 libass commit/폰트/PlayRes와B값이 필요하다. 빈L03를 채우려면 기존 모집틀 안 적격 최초 본문을 복원해야 한다. 규칙 변경이 필요한 경우 별도 사전 프로토콜로 시작하고 이 예측을 사후 수정하지 않는다. 실제 재현 명령·입력·예상 종료 상태는 [replay-review](replay/replay-review.md), 최종 원격 읽기·session check의 실제 영수증과 고정 결과 SHA는 HANDOFF에 남긴다.

## 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 6자리 중1미충원, 최초 본문/실제판 미복원; L02 정상은 연구자 보충 | 여섯 새 요구·당시 동일판을 대표한 비교라는 주장 | [frame.csv](frame.csv) 데이터1~59행; [#685 본문](https://github.com/libass/libass/issues/685); [source-counts](evidence/source-counts.json) requester5/6 | 기존 모집틀의 최초 본문 및 작성자 build·원정상 fixture 확보 | 정해 둔 기준 안 세 번째 libass 요구와 역사판/정상 입력이 복원돼 새 사전 비교를 할 수 있음 |
| 정확 후속20셀은 미확인이고 L01/L02 B값도 사전 미고정; V01 후속은 입력·조작 불일치 | 두 조작의 실제 승패·공개 후속 검증 및 완전 충족 | [outcomes.csv](outcomes.csv)18행; [V01 변형](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527); [L02 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083) | 원판·입력·수치A/B를 붙인 정상/경계 출력/고정시험 확보; 새 수치 선택은 별도 봉인 | 같은 조건의 실제 관측이 두 조작을 가르고, 자료 배당까지 충족. 자체 재생만으로 역사판 결손이 사라지지 않음 |
| I/D 예측이 모두 같고 동일 작성자·창밖 노출·검색순서 제한이 남음 | D 내용 자체가 I보다 새 판별력을 주거나 사람의 시간/창의성을 높인다는 주장 | [cards.csv](cards.csv)18행 prior_exposure/outside_window; [predictions.csv](predictions.csv)18행; [노출 기록](evidence/search-and-exposure.json) | 다른 예측을 만들 수 있는 조건을 새로 사전 고정하고, 순서/노출을 분리한 관측 설계 | I가 내지 못한 D의 서로 다른 사전 예측과 이를 가르는 직접 출력이 함께 생김. 현재5/5 예측 일치만으로 효과 우열은 결정되지 않음 |
