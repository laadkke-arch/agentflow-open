# 양판 입력 차이와 경쟁 설명 (단방향, 동일 계보)

직접 읽은 태그 12개(X11–X26, fixtures.csv)를 다시 가져와 전체 Git blob SHA를 비교했다. 전부 다르다. 추가로 `<part-list`부터 `</score-partwise>` 직전까지 잘라 XML 주석과 태그 사이 공백만 제거하여 문자 비교했다(스키마 정규화/C14N 아님, 텍스트 내부 공백 보존). 첫 measure 내부 역시 태그 사이 공백만 제거하여 양판 part별 비교했다. 원문 재열람에 기반한 간단한 대조이지 새 렌더, 대규모 검산, 독립 검토가 아니다.

|시험|blob 동일|part-list 이후 동일|첫 measure 내부 동일|첫 차이와 판정|
|---|---|---|---|---|
|02a|아니오|아니오|아니오|m1 divisions 64→512, 4/4 common→2/2 numeric. normalized rest length 4 quarter units, multiple-rest=2 유지. m4의 더 짧은 rest 및 m6 measure=no 등 변경. 같은 엔진 개선만으로 원인 귀속 금지.|
|02c|아니오|아니오|예|m1–3, m4–18, m19, m20–31. 구판 m31 끝 barline; 신판 그 뒤 m32–34(3, use-symbols=yes). 첫 m1 비교 가능하나 전체 입력 변경. 같은 첫 숫자3과 달라진 glyph, 뒤 15+1 구간 분리.|
|11a|아니오|아니오|예|m7에 print new-system=yes 추가; m1 symbol=common 2/2, m2 4/4 common, m3 2/2 numeric 유지. 두 판 첫 기호 같아도 파일 동일하지 않고 판면 지시는 달라짐.|
|33b|아니오|예|예|DTD/버전·주석 등 외곽 차이; 정규화한 score-part-list 및 전체 2마디 동일. F4→F4, tie와 tied가 둘 다 있음. 이 사례 하나만 전체 음악 본문 동일 대조.|
|33c|아니오|아니오|예|구판 m2 끝 barline; 신판 그 뒤 m3 교차 성부 추가. m1·m2 내용 대조, 구판 겹친 곡선 끝점 미확인, 신판 m2 두 곡선 범위 관측. 입력 추가/판면/변환 변화 경쟁 설명.|
|41i|아니오|아니오|예|part-list에서 P1 약어 abbrv.→Abbrev.; P2 표시 문자열 변경(Overridden Part Name→Part Name 줄바꿈 Override), 약어도 변경. P1 첫 표시 문자열만 대조 가능. 첫 measure 내부 동일은 score-part-list 동일을 뜻하지 않음.|

## 반례와 판별 절차

- 02a/02c: XML의 grouping 지시와 출판의 grouping이 다르다. 구판 02c 첫 3,16,12와 기대 3,15,1,12. 숫자의 총합 31이 맞더라도 독립 m19 표기 없음(편집 가능한 m19가 사라졌다고는 말 못 함). 신판은 3,15,whole-rest,12,3. 02c 구판 3에 고전 glyph, 신판 3 H-bar: 같은 count, 다른 외형. 02a의 meter 변경과 02c tail 추가, 변환기의 병합 선택, 엔진 기본 스타일, build options 모두 경쟁 설명. 하나의 동일 XML을 양판에서 렌더하고 generated .ly와 로그까지 보면 구분 가능.
- 11a: first m1 cut C 양판 같지만 m3 numeric 2/2와 동일 박수 값; 기호만 보면 meter 숫자를 아는 전문 관례가 필요. m7 new-system=yes가 새로 추가됐는데 화면에서 비슷하게 줄을 바꿀 수 있으므로 줄바꿈만으로 print 지시를 복원 못 함.
- 33b: 사양 C8(tie)와 C9(tied)는 소리와 인쇄를 명시 분리. 두 판 같은 곡선이라도 내부 tie 음향 연속은 확인하지 않았다. tied만 있는 입력/양쪽 모두 있는 입력의 같은 곡선은 사양으로부터 가능한 반례이며 여기서 렌더하지 않은 가설이다.
- 33c: 구판 m2 outer 끝점 n4 불분명, 신판 m2 n1→n4 및 n2→n3로 읽힘. 신판 m3의 v2 beat1→v1 beat3은 캡션 기대에도 곡선 식별 못 함; 실패 확정 금지. curve overlap, 축소, 다중 성부 표시, 변환에서 slur discard 등 경쟁. 음표 위치를 기준으로 비교하고 동일 x/y 요구하지 않는다.
- 41i: P2 base part-name은 양판 Part name으로 같으나 표시가 바뀐다. P1/P2 이름이 보인다고 실제 score-part ID/원래 name 문자열이 변환 후 남는 것은 아니다. 반대로 서로 다른 내부 이름에도 같은 display 가능(사양상 가능; 실험 미실시).
- 전자책: Cinderella 1865/George Routledge/DjVu page5, 원면(T8)에는 header·행말 god-/mother·인쇄 쪽수 5; Page 전사(T9)에서는 godmother가 연결되고 header/footer는 따로 있음. 최종 본문(T10)은 그 쪽 경계에 이어지지만 반복 제목과 쪽수는 본문에 삽입되지 않음(T7 규칙). 같은 출처 키가 있어도 페이지 외형과 검색·편집 기능은 별개. 화면을 원면의 종이/제본까지 증명하는 링크로 쓰지 않는다.
- 신문: Trek 1942-12-01 ed1 image5(LOC T5 실제 화면) 오른쪽 'from', 왼쪽 OCR 'frcsn'. T6 page anchor는 같은 면을 식별하고 OCR 일치가 highlight의 전제. raw 원면/T12 직접 URL 접근 실패, 화면 관측 한정. 정답 원문과 검색용 파생물을 별개로 표시.
- 영상: Bentley 직원 보고 T2에서 DVD 메뉴·부가기능이 중요한 경우 원 디스크 image와 추출 영상 둘 다 보존. T3는 FFV1/MKV의 캡션·timecode 제한이 2020→2023 변했다는 기관 보고. 개별 원 디스크와 접근본의 동일 ID 및 실제 재생 대조는 없다. 출판 영상 링크만으로 메뉴·자막·타임코드 보존 여부는 추론 불가. 사례는 인수 정책/위험의 증거이지 구체 손실의 직접 실측은 아님.

## 조립 조건 (설계 대안)

A 링크+판·객체 키(가볍고 탐색 빠름; 사양/캡션만인 항목은 기대에 한정), B A+실제 출력 locator+속성별 관측/미확인(인쇄 독자에 유용, 사람 판독·판 관리 비용), C B+입력 exact hash/변환 중간물/편집 및 음향 실행(편집·연주 검증, 더 큰 비용). A/B/C는 목적별 증거 결합 선택지이지 제품 스키마/수집기 결정 아님. 같은 lineage를 독립 구현으로 세지 않고 버전/입력/관측층을 연결한다. 자동 link refresh는 blob/판면/캡션 변경의 신호만; 실제 재판독은 변경된 목적별 속성에 한정. 비용은 실측하지 않았다.
