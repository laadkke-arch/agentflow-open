| 표 1 | 파일·설정·차수 | 원항목·필드 값 | 수신 DB 키·값 | 실제 같거나 달라진 값 | 영수증 주소 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| M01 | S02 · false · 초회 | `/items/0` ID …0001<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=1`, `entry.id=1795559071841651`<br>GUID …0001, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M02 | S02 · false · 초회 | `/items/1` ID …0002<br>absent, 별표 토큰, 라벨 Design, art | `feed.id=2`, `entry.id=1795559071841650`<br>GUID …0002, 링크는 원 alternate<br>read=0, 별표=1, 태그 art, Design | 0→1행. URL·GUID·별표·라벨 일치. 누락 읽음 → 0 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M03 | S02 · false · 초회 | `/items/2` ID …0003<br>absent, 별표 토큰, 라벨 [] | `feed.id=3`, `entry.id=1795559071841649`<br>GUID …0003, 링크는 원 alternate<br>read=0, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 누락 읽음 → 0 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M04 | S02 · false · 재수입 | `/items/0` ID …0001<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=1`, `entry.id=1795559071841651`<br>GUID …0001, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M05 | S02 · false · 재수입 | `/items/1` ID …0002<br>absent, 별표 토큰, 라벨 Design, art | `feed.id=2`, `entry.id=1795559071841650`<br>GUID …0002, 링크는 원 alternate<br>read=0, 별표=1, 태그 art, Design | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M06 | S02 · false · 재수입 | `/items/2` ID …0003<br>absent, 별표 토큰, 라벨 [] | `feed.id=3`, `entry.id=1795559071841649`<br>GUID …0003, 링크는 원 alternate<br>read=0, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r0](receipts/S02-r0.json) | 발행자 RSS GUID |
| M07 | S02 · true · 초회 | `/items/0` ID …0001<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=1`, `entry.id=1795559072319973`<br>GUID …0001, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M08 | S02 · true · 초회 | `/items/1` ID …0002<br>absent, 별표 토큰, 라벨 Design, art | `feed.id=2`, `entry.id=1795559072319972`<br>GUID …0002, 링크는 원 alternate<br>read=1, 별표=1, 태그 art, Design | 0→1행. URL·GUID·별표·라벨 일치. 누락 읽음 → 1 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M09 | S02 · true · 초회 | `/items/2` ID …0003<br>absent, 별표 토큰, 라벨 [] | `feed.id=3`, `entry.id=1795559072319971`<br>GUID …0003, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 누락 읽음 → 1 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M10 | S02 · true · 재수입 | `/items/0` ID …0001<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=1`, `entry.id=1795559072319973`<br>GUID …0001, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M11 | S02 · true · 재수입 | `/items/1` ID …0002<br>absent, 별표 토큰, 라벨 Design, art | `feed.id=2`, `entry.id=1795559072319972`<br>GUID …0002, 링크는 원 alternate<br>read=1, 별표=1, 태그 art, Design | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M12 | S02 · true · 재수입 | `/items/2` ID …0003<br>absent, 별표 토큰, 라벨 [] | `feed.id=3`, `entry.id=1795559072319971`<br>GUID …0003, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S02-r1](receipts/S02-r1.json) | 발행자 RSS GUID |
| M13 | S03 · false · 초회 | `/items/0` ID …00b1<br>read 토큰, 별표 토큰, 라벨 Misc | `feed.id=1`, `entry.id=1795559072755393`<br>GUID …00b1, 링크는 원 alternate<br>read=1, 별표=1, 태그 Misc | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S03-r0](receipts/S03-r0.json) | 발행자 RSS GUID |
| M14 | S03 · false · 초회 | `/items/1` ID …00b2<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=2`, `entry.id=1795559072755392`<br>GUID …00b2, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S03-r0](receipts/S03-r0.json) | 발행자 RSS GUID |
| M15 | S03 · false · 재수입 | `/items/0` ID …00b1<br>read 토큰, 별표 토큰, 라벨 Misc | `feed.id=1`, `entry.id=1795559072755393`<br>GUID …00b1, 링크는 원 alternate<br>read=1, 별표=1, 태그 Misc | 같은 행과 표시값 유지. lastSeen → 0 | [S03-r0](receipts/S03-r0.json) | 발행자 RSS GUID |
| M16 | S03 · false · 재수입 | `/items/1` ID …00b2<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=2`, `entry.id=1795559072755392`<br>GUID …00b2, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S03-r0](receipts/S03-r0.json) | 발행자 RSS GUID |
| M17 | S03 · true · 초회 | `/items/0` ID …00b1<br>read 토큰, 별표 토큰, 라벨 Misc | `feed.id=1`, `entry.id=1795559073215687`<br>GUID …00b1, 링크는 원 alternate<br>read=1, 별표=1, 태그 Misc | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S03-r1](receipts/S03-r1.json) | 발행자 RSS GUID |
| M18 | S03 · true · 초회 | `/items/1` ID …00b2<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=2`, `entry.id=1795559073215686`<br>GUID …00b2, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 0→1행. URL·GUID·별표·라벨 일치. 읽음 토큰 → 1 | [S03-r1](receipts/S03-r1.json) | 발행자 RSS GUID |
| M19 | S03 · true · 재수입 | `/items/0` ID …00b1<br>read 토큰, 별표 토큰, 라벨 Misc | `feed.id=1`, `entry.id=1795559073215687`<br>GUID …00b1, 링크는 원 alternate<br>read=1, 별표=1, 태그 Misc | 같은 행과 표시값 유지. lastSeen → 0 | [S03-r1](receipts/S03-r1.json) | 발행자 RSS GUID |
| M20 | S03 · true · 재수입 | `/items/1` ID …00b2<br>read 토큰, 별표 토큰, 라벨 [] | `feed.id=2`, `entry.id=1795559073215686`<br>GUID …00b2, 링크는 원 alternate<br>read=1, 별표=1, 태그 [] | 같은 행과 표시값 유지. lastSeen → 0 | [S03-r1](receipts/S03-r1.json) | 발행자 RSS GUID |

표 1의 한 행은 원항목 하나를 한 수신 설정·차수에 조인한 결과다. 실제 전체 URL·GUID와 태그 키는 [observed.csv](observed.csv)와 영수증에 있다.

| 표 2 | 통제·사용 목적 | 기대 | 관측 | 필요한 송신·수신 절 | 보류 이유 |
| --- | --- | --- | --- | --- | --- |
| C1 | GUID 교차 피드 | [사전 예측](SCOPE.md) | 미실시 | [원장](sources.jsonl) | 통제 실행 뒤 갱신 |
| C2 | alternate/canonical 불일치 | [사전 예측](SCOPE.md) | 미실시 | [원장](sources.jsonl) | 통제 실행 뒤 갱신 |
| C3 | 실제 입력 경로와 이름 | [사전 예측](SCOPE.md) | 미실시 | [원장](sources.jsonl) | 통제 실행 뒤 갱신 |
| C4 | 읽음 상태의 명시적 안읽음 | [사전 예측](SCOPE.md) | 미실시 | [원장](sources.jsonl) | 통제 실행 뒤 갱신 |
| C5 | 수신 쪽 사용자 변경 | [사전 예측](SCOPE.md) | 미실시 | [원장](sources.jsonl) | 통제 실행 뒤 갱신 |
