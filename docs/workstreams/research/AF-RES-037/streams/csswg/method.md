# CSSWG · 단계1 원장

2018–2024 생성 GitHub issue 7,161개 중 created ascending 최초40 metadata를 받았고, 첫4개가 행동·대안 적격이라 본문 심사는 네 번째에서 종료했다. 나머지36개는 제외 판정이 아니라 상한 뒤 미심사다. 이전 017/022/033 사건과 동일한 CSSWG issue는 없었다.

| 사건 | 최초 원문 | 원안만으로 확인한 선택 |
| --- | --- | --- |
| A-C01 / #2155 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0002.html), 2018-01-01 08:51:05Z | 표 요소 sticky 예외를 없애 스크롤 머리글 유지 |
| A-C02 / #2156 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0012.html), 2018-01-01 12:46:23Z | unknown -webkit pseudo-element 예외 명세화와 구현의 일반 invalidation 사이 선택 |
| A-C03 / #2157 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0020.html), 2018-01-01 14:32:55Z | 표 열 selector 이름을 :nth-column에서 :nth-col로 바꿈 |
| A-C04 / #2158 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0033.html), 2018-01-02 16:55:37Z | ::slotted의 허용 인자를 하나로 줄여 최적화 용이성 확보 |

## 초기판 확인과 정정

현재 API body를 최초판으로 확정하지 않았다. GH Archive는403/도구 접근 실패였고, 같은 W3C의 원 author notification인 `issues.opened` 메일을 직접 열어 네 건의 최초 본문을 복원했다. 생성시각·issue ID·메일 Message-ID·received 시각을 연결했다. GitHub URL과 W3C 알림은 같은 저작이므로 하나로 센다. 제3자 재인용·미러 문헌을 추가 산입하지 않았다.

#2157 현재 본문에는 CSS에서 약어를 흔히 쓰지 않는다는 설명이 추가돼 있다. 최초판에는 그 문장이 없다. #2158 현재 제목에는 :host가 추가됐으나 최초 제목·본문 범위는 ::slotted뿐이다. 초기 분석을 현재 제목의 :host까지 넓히지 않았다. `initial.json`은 원안 요약·해시와 차이를 보존한다. 원문 전체는 비커밋 `cache/`에만 있다.

#2157은 단순 편집 오타가 아닌 공개 selector 문법 명칭의 변경이다. 사용자가 입력할 API 명칭 대안이 식별되므로 포함했다. 다른 해석으로 명칭 변경을 제외할 경우 네 번째 이후를 사후 편입하지 말고, 이 사건을 뺀 A-C3 민감도만 별도 계산해야 한다.

## 노출 편차

네 사례를 root에 선정 보고한 뒤 초기 알림을 찾던 exact-ID 검색이 #2157 후속 회의 결의 스니펫을 반환했다. 이후 archive navigation에서도 Closed 제목이 보였다. 후속 페이지 본문은 열지 않았고 선정은 바꾸지 않았다. 그러나 **A-C03의 결말 완전 미노출 조건은 충족하지 못했다**. `attempts.jsonl` CSS-ATT05/06과 frame 행에 보존한다. 완전 blind 표집으로 보고하면 안 된다.

API response의 상태·수정시각·댓글수 필드는 원 payload에 존재하나 metadata 출력에서는 제거했고 선정에 쓰지 않았다. 최초 메일의 navigation에는 댓글 저자·제목이 보이지만 실제 후속 본문은 단계2 커밋 후까지 읽지 않았다. 당대 원문이 공개됐다는 메일 evidence와 당대 검색색인 여부는 다르며, 후자는 네 건 모두 미확인이다.

## 단계1 종료

`frame.json` 40행(선정4/심사후 탈락0/상한뒤 미심사36), `initial.json` 4행, `sources.jsonl` 원문4행과 `attempts.jsonl` 접근·노출 영수증을 root의 두 번째 커밋으로 봉인한다. 후속 결정·구현·반례 판독은 root의 봉인 확인 메시지 이후 시작한다.
