# Frame A 방법·식별 기록

메타데이터 동결 `fd80a75d5ee3a77f89291f82fd3fb2b90975be3b` 이후 방법을 심사했다. 최초 25건 중 22건의 원 방법 본문과 1건의 저자 포스터 방법을 읽었다. 2건(A-F17, A-F21)은 출판사·저자/기관·공개 아카이브 경로를 확인했지만 본문이 미확인이다. 결과표 방향과 자료 공개 여부를 적격 조건으로 사용하지 않았다. 검색 스니펫 결과가 우연히 노출되었으므로 완전 눈가림은 아니다.

## 주 슬롯과 네 연결

### A01 — Łajewska et al., SIGIR 2024 (A-F10)

원문: <https://krisztianbalog.com/files/sigir2024-transparent-cis.pdf> §3–4, Tables1–3. 패키지 고정판: <https://github.com/iai-group/sigir2024-transparentCIS/tree/065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d>.

| 연결 | 직접 확인 | 끊긴 열/한계 |
| --- | --- | --- |
| 배정 | §3.1: 사람당 1HIT, 10query; query 순서 무작위. §4.3:273제출 중113주의검사 탈락,160유지,EC별16명 | **조건/HIT 무작위 배정은 미확인**. 배정 코드와 탈락113명의 조건/시행이 공개 파일에 없음 |
| 자극 | `data/input/input_data.csv` Id1–10; `mturk_output.csv`의 `Input.query_id`, `Input.response`. EC1↔EC9, EC3↔EC10의 10문항 응답 본문 문자열이 모두 같음; 각 조건16명에서도 불변 | EC2/4는 본문에 텍스트 단서가 추가되어 완전 문자열 동일성이 아님. 화면 순서/전체 레이아웃 동일성은 실행 앱으로 재검증하지 못함 |
| 참값/출처 | 같은 파일의 `Response good/bad`, `Source`, `Source link`, noise열. EC1/3은 원 단락과 강조 및 외부 절 링크, EC9/10은 없음 | perfect/imperfect는 사실 오류뿐 아니라 편향·불완전성을 섞음. 저자 라벨을 순수 정권고/오권고로 치환할 수 없음. 도착 원문 당시판 전수 검증 미완료 |
| 최종 판단 | `WorkerId` + `Input.query_id` + `Answer.correctness_{id}.option_{1..4}` / `factuality`로 네 선택 평정을 연결 가능. 정확성 평정이 있다는 범위에서 적격 | 최종 선택 답/권고 수락 변수가 **해당 없음**. 평정에 임계값을 정해 수락으로 바꾸지 않음. 따라서 수락 J4 |

비교 강도 I3. EC1/3 대 EC9/10은 출처 제공과 함께 신뢰도·제한 단서가 달라진다. 따라서 링크만의 효과를 식별하지 않는다. 원행 존재는 수락 종점 존재와 다르다.

## A02 잠정 — Kim et al., CHI 2025 (A-F18)

본문 고정판: <https://arxiv.org/pdf/2502.08554v1> §4.1–4.3, Table1, AppendixF(PDFpp23–26). 사전등록: <https://aspredicted.org/bg22-yfw7.pdf> #186271,2024-08-12. A-F17의 앞선 방법이 미확인이므로 두 번째 적격 **확정 순위**라고 부르지 않는다. A03은 채우지 않았다.

| 연결 | 직접 확인 | 끊긴 열/한계 |
| --- | --- | --- |
| 배정 | §4.1.1 및 preregQ4:각 사람8시행,정오×설명×출처의8형식 각1회;12문항 중 어떤 형식이 어떤 문항에 붙는지와 순서 무작위 | 실제 무작위화 코드/문항별 배정 N 미확인.320수집,12제외,308분석; 이전 중도이탈 분모 미확인 |
| 자극 | §4.1.4:정/오 답+설명 쌍24개를 미리 작성; 설명 제거로 무설명형 생성; 각각에 출처3개를 추가. AppendixF는24개의 설명+출처형을 제공 | 동일 문항/답의 출처유무 비교는 생성 절차로 지지. 실행 앱·모든96화면 파일/개별행 조건 매칭 미확인. source URLs는 답 방향에 따라 다를 수 있음 |
| 참값/출처 | AppendixF문항/저자 답키/URL. root의 별도 도착 원문 감사에서 지지·반박·논쟁을 구분 | National Geographic 책 기반 답키와 현재 도착 원문을 구별. brain-size문항의 과학적 반론 등은 root원장 참조.2024당시판 전수 확인 아님 |
| 최종 판단 | §4.1.2 및 preregQ3:Agreement=최종답과Theta답 일치,Accuracy=최종답 정답 여부. binary factual task | 공개 참가자 시행 원행/정수 수락 교차표 미회수. Table1 반올림 평균은 J3; 원개수로 역산 금지. 초기 답이 없어 원래 동의와 AI때문에 변경을 분리할 수 없음 |

## 노출 사건 사전

| 연구/사건 | 실제 정의·증거 | 허용되는 해석 |
| --- | --- | --- |
| Kim source offered | 각 참가자4개 source조건, 각 응답3개 링크. 외부 자체검색은 하지 말라고 요청(§4.1.1) | 제공 배정; 자동 열림이나 강제 독해 아님 |
| Kim `SourceClick` | 1개 이상 링크를 클릭했으면TRUE (§4.1.2; preregQ3) | 클릭 발생; 어느 문단을 읽고 이해했는지는 미확인 |
| Kim `Time` | 질문을 본 때부터 Next까지 분 (§4.1.2) | 질문 전체 체류시간. 원문 탭 체류/스크롤 시간과 다름 |
| Kim 선택 클릭층 | §4.3.2:318clicked,914notclicked/sourceoffered1232; 클릭층 정권고164/오권고154 | 원래 배정과 다른 자발 행동층. 인과적 클릭 효과 미식별 |
| TransparentCIS `Answer.p_clicked_details` | raw문자열에 `source_details_{id}` 및 timestamp; 처리코드엔 최종출력에서 주석 처리 | 원시 기록 문자열의 비공백을 셀 수 있음. 토글/열기/닫기 event정의가 없어서 읽기로 해석 불가 |
| TransparentCIS `Answer.p_clicked_links` | URL 또는 일반 `Sources` 라벨 및 timestamp가 섞인 원시 문자열 | 링크 관련 기록. 일반라벨은 item별 조인키가 아니며 현재패키지에 client event사전 없음.35/128명 비공백은 독해 수가 아님 |

## 반례와 경계

Traceable Texts(A-F20)는 원문을 이미 두 군 모두 보여 주며 hover문구 대응만 바꾼다. HILL(A-F07)은 출처 UI 선호가 높아도 실제 오판 감소를 측정하지 않는다. Guidance Source Matters(A-F16)의 'source'는 AI/전문가/집단이라는 권고자 이름이며 데이터 원문은 모두에게 같다. MATSA(A-F14)와 Multi-Level Explanations(A-F23)도 원문 대신 강조 방법을 바꾼다. 이런 논문을 링크 접근 실험으로 세면 모집틀이 달라진다.

Kim의 Table1에서 설명은 출처가 없는 오답 조건의 수락 평균을78.2%에서82.8%로 높이며, 출처가 있는 오답 조건에서도68.2%에서76.9%로 높인다. 이는 출처 제공의 배정 대비와 구별한 설명 구성의 반례이며 정수 복원 결과가 아니다. TransparentCIS의 noisy source는 같은 주제라도 응답을 지지하지 않는 단락을 의도적으로 제공한다(§4.1); 원문이 있다는 사실만으로 주장에 대한 증거가 되지 않는다.

## 최소 재개 입력

1. A-F17·A-F21의 원 방법/보충판 공개 접근 또는 합법적인 파일을 회수해 첫3순위를 확정한다. publisher403, authorabstract, ResearchGate 요청화면, CDX조회는 `archive-attempts*.json`/검색원장에 남겼다.
2. Kim Study2의 participant×question×condition×advice×truth×final_answer×exclusion 원행 및 코드북/정정판이 필요하다. 공개 패키지를 아직 찾지 못했다는 사실은 존재하지 않는다는 뜻이 아니다.
3. TransparentCIS 실제 client 이벤트 코드,113탈락자의 조건표, source 당시판/정답키 평가 기준이 필요하다. 현재 수락 종점 부재는 더 많은 평정 원행으로 해결되지 않는다.
