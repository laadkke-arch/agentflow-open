# Inkscape 신규 세 요청 · 사전 모집과 A/B

## 모집 계약

주모집은 `inkscape/inkscape` 공식 GitLab 이슈다. 2021-01-01T00:00:00Z 이상, 2026-01-01T00:00:00Z 이전 생성분에 대해 API `search=clone|duplicate|linked&in=title&order_by=created_at&sort=asc&per_page=100` 세 검색을 실행했다. 검색어를 결합한 URL은 query_receipts.json, 원 metadata는 main_metadata_and_release.json에 있다. 서버의 제목 검색은 stemming을 적용한다. `duplicate`가 `duplication`, `linked`가 `links`에 대응한 행을 그대로 남기며 추가 literal 필터를 사용하지 않았다.

각 쿼리의 전체 반환수는 clone 84, duplicate 37, linked 34이고 모두 다음 페이지가 없다. 각 검색의 반환은 100 미만이므로 첫 30 event의 순서에서 숨은 후속 페이지 문제는 없다. 합집합은 created UTC, 숫자 iid 순이다. 동일 URL은 합치고 동일 생성 UTC·제목의 #2407/#2413은 동일 사건으로 처리하여 #2413 원행과 이유를 보존했다. `frame.csv`는 제외 전 31행, 중복을 뺀 첫 30 event, 선택 3행을 가진다. body를 읽어 적격을 판단한 최초 세 건은 #2225/#2231/#2283이다. 이미 세 자리가 찼으므로 뒤의 행은 후속 자료 유무로 교체하지 않았다. #2379는 선행 AF-RES-089의 사건이라고 별도로 표시했다.

초기 pilot에는 `inkscape/inbox`를 포함한 6검색이 있었다. root가 범위 봉인 전에 공식 본 repo로 확정한 뒤 inbox는 주 모집에서 제외했다. pilot_frame_metadata.json은 그 탐색 이력을 남긴 것이며 두 번째 표본이 아니다. #2283의 이동 전 inbox #4522는 같은 사건의 더 이른 요청 snapshot으로만 사용하고 고유 자료 수는 하나로 센다.

## 최초 본문과 가림의 한계

API 응답에서 title/created/updated/id/description만 선별했다. labels, comments, milestone, 수정 MR와 회귀시험은 별도 요청하지 않았고 A/B 작성에 쓰지 않았다. 다만 최초 웹 검색에 2020년 범위 밖 #1709의 댓글·라벨이 자동 노출되었고, #2283 현재 description에는 나중에 trunk에서 한 번 고쳤다는 문장이 있었다. 전자는 표본 외, 후자는 해당 행의 contamination=true로 남겼다. #2283 판정은 그 문장이 없는 이동 전 inbox #4522 요청 snapshot을 사용했다. 최초 작성 시점의 description version은 세 건 모두 복원하지 못했으며 현재 본문을 최초 원판으로 부르지 않는다.

requests.json에 본문 SHA-256, 최초 확인 가능한 주소, 짧은 원문 발췌, 요약과 사용자판을 보존했다. 전문은 저장하지 않는다. I1/I2의 본문은 모델에 각각 두 번 노출됐고, I3는 current primary와 earlier inbox 본문을 한 번씩 보았다. records_A의 request_read_count=1은 논리적 원문 수로 썼으므로 실제 exposure는 read_budget.json의 2를 사용한다. A snapshot을 고친 것은 아니다.

## 두 후보와 사전 판단

I1: Space stamp와 Edit Duplicate는 원문에 함께 등장하며, 같은 SVG2 text 복사 뒤 각 상자 크기를 고치는 목적에서 비교할 실제 선택지다. 공식 1.0.2 `SelTrans::stamp`와 `ObjectSet::duplicate`는 첫 복사본 생성뿐 아니라 참조 shape를 복사·재연결하는 경로가 다르다. 원문 자체가 stamp의 동시 변경과 개별 편집 요구를 명시하므로 A부터 분리이고 B도 분리다. 실제 frame ID와 resize 출력은 이 코드만으로 관측하지 않았다.

I2: clipboard Link button과 Edit Clone original path LPE는 실제 호출 가능한 두 경로다. 전자는 기존 LPE target의 parameter를 쓰고 후자는 새 target을 만든다. 기존 target ID 보존이 필수인지와 양쪽에서 같은 원본 수정 출력이 나오는지가 비어 A/B 모두 유보다. B 초안의 callback 언급은 원래 후보 절 밖인 것을 root 검토에서 발견해 제거했다. records_B_initial.jsonl과 B_revision_log.json에 원값·시각·이유를 보존했고 판단은 바뀌지 않았다. 최종 B의 I2 next_operation은 양 후보 모두 null이다.

I3: 사용자는 eraser delete로 sprayed clone과 원본을 지우되 남겨야 할 clone을 유지하길 원한다. 같은 입력을 받는 두 번째 해결 후보는 확보하지 못했다. Select+Delete는 selection 입력과 조작을 바꾸고, Spray Copy는 clone 관계를 바꾸므로 대체쌍에 넣지 않았다. 후보2 null, A/B 모두 유보다. 후보 탐색에서 읽은 selection/spray 코드는 반례·배제 근거이며 성공 출력이 아니다.

모든 후보는 1.0.2 태그가 가리키는 `e86c870879310bfb4a9abee3e7fd65aef0408fd7`에 고정했다. 1.0.2+r75+1 배포 패키지가 upstream 태그와 byte-identical하다는 확인은 없다. 이 차이는 사후 채점 때도 유지해야 한다.

## 봉인과 비용

A는 2026-11-23T17:59:32.483756Z에 고정하고 SHA-256 aac2d2d5186128869d8976e14bdc2a4daeb68f6a524fab09b28f6377d0a0e429를 root가 읽어 확인한 뒤 B를 썼다. 같은 연구자가 A 내용과 같은 candidate sections를 보고 B를 채웠다. 독립 코딩 또는 완전 블라인드가 아니다.

최종 B는 2026-11-23T18:02:04.678447Z, SHA-256 5514a7fdf5663998284b6e2dbfed19d108e74a0fd6f82061070fdd7e877098b9다. B에는 새 후보 URL이나 사후 정답을 넣지 않았다. 코드/요청의 기존 cache만 사용했으며 B 작성 중 추가 원문 network open은 0이다. A/B의 최대 두 번 원문 exposure는 read_budget.json에서 확인한다. source discovery에서는 versioned implementation 7개를 열었으나 실제 두 후보 기록과 추가 탐색 원문을 구별한다.

UTF-8 payload는 ensure_ascii=False, separators=(',', ':') 직렬화에 한정한다. A: I1 830, I2 921, I3 611 bytes; B: I1 1748, I2 1637, I3 1028 bytes. judgement와 audit wrapper는 payload 비용에 포함하지 않았다. 이후 결과 정답과 비교하기 전 3×2 자리의 사전 판단만 고정했으며 accuracy는 아직 산출하지 않았다.

## 직접 자료 수

sources.jsonl의 산입 원문은 요청 3, 판 고정 공식 구현 파일 7로 10개다. 여러 절은 같은 파일 하나로 세며, 구현 파일 7개를 독립된 사용자 사건 또는 별도 효과 검증 7개로 세지 않는다. 버전 metadata·검색·pilot 노출은 하한에서 제외했다. 후보 문서와 사후 대조가 같은 파일/계보이면 독립 확인 수에서 제외해야 한다.
