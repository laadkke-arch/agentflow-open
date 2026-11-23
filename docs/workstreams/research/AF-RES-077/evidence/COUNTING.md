# 독립 원저작의 계수 규칙

`SOURCES.jsonl`의 `independent_work_id`는 제목/계보별 named work를 식별한다. 같은 코드베이스의 파일·시험·고정판·수정판, 같은 문서의 절·번역·미러·판은 하나다. 독립 request는 코드와 별개 저작이지만 댓글·그 이슈의 축소 fixture는 추가 저작으로 세지 않는다. 제외된 모집 후보·검색 인덱스·tag·CI metadata·접근 실패는 minimum20에 넣지 않는다.

최종 검토에서는 더 보수적인 `conservative_lineage_id`도 사용한다. **세 대상 제품 모두 같은 규칙**으로 코드와 제품 설명서를 묶는다:

- SHOTCUT-PROXY-GUIDE → SC-CODEBASE.
- MUSESCORE3-HANDBOOK → MS-CODEBASE.
- SIGIL-USER-GUIDE → SG-CODEBASE.

이 밖의 named work는 자기 계보를 유지한다. Kdenlive manual과 Shotcut의 복사된 hash routine을 독립 구현 검증으로 해석하지 않는다. Kdenlive 문서는 별도 설명 원저작으로만 세며 해당 code routine을 추가 저작으로 세지 않았다. `counted_work_units`는 최종 conservative lineage의 첫 eligible row에서만1이다. `named_work_units`는 named work별 첫 row에서만1이다. 따라서 합계가 파일 수나 source row 수에 좌우되지 않는다.

최종 목표치는 **named24 / conservative21**이다. 요청3, 대상 code3, target-support 문서3, 동종3, 제공원전3, 반례/대안9라는 named 분류가24이며 중복군3을 합치면21이다. 이 분류는 통계적 독립 표본 수가 아니다. 모집 적격 primary는 여전히0/3이다.

요청된 “판고정 문서·코드·시험 독립 저작6”은 별도 결손을 유지한다. 대상 관련 named6은 code3+MLT XML+Shotcut proxy guide+Sigil user guide다. conservative 계보는4이고, 당시판이 확실한 독립 code계보는3이다(Sigil의 당시 guide는 그 계보 안에 추가 확인). MLT XML과 Shotcut guide는 현재 snapshot의 hash만 있고 당시판 동등성은 미확인이다. 전체20을 넘겼다는 이유로 이 6자리 층을 충족했다고 쓰지 않는다.

추가 원저작3개는 사후 반례 목적이다: SQLite atomic commit은 복구 정보·flush·여러 파일 조정을, Blender3.6 linked duplicates는 shared data와 local transform 및 shared Action의 예외를, RFC7089 Memento는 현재 식별자와 실제 보관된 과거 상태의 차이를 확인한다. A/B 판독 예산에는 이 추가 열람을 넣지 않았으며 COSTS의 compiler 비용이다.
