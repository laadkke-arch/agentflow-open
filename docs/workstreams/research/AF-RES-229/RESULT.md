# AF-RES-229 · pip 24.0의 pytest 철회 파일 선택

| 요청·인덱스 | 대상 플래그·사유 | 실제 선택 파일·SHA | 경고·종료 | 선행·실행 영수증 | 미확인 |
| --- | --- | --- | --- | --- | --- |
| \`pytest==8.1.0\` · baseline | true · 원사유 P | \`pytest-8.1.0-py3-none-any.whl\` · \`ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e\` | 각 stderr 1건 · P · 각 종료 0 | D04/D06 · [r1](receipts/main/pin-target-baseline-r1/) · [r2](receipts/main/pin-target-baseline-r2/) | 실설치·실행 범위 밖 |
| \`pytest==8.1.0\` · unmarked | 속성 없음 · 사유 해당 없음 | \`pytest-8.1.0-py3-none-any.whl\` · \`ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e\` | 선택 경고 0 · 각 종료 0 | D04/D06 · [r1](receipts/main/pin-target-unmarked-r1/) · [r2](receipts/main/pin-target-unmarked-r2/) | 실설치·실행 범위 밖 |
| \`pytest>=8.0.2,<8.1.1\` · baseline | true · 원사유 P | \`pytest-8.0.2-py3-none-any.whl\` · \`edfaaef32ce5172d5466b5127b42e0d6d35ebbe4453f0e3505d96afd93f6b096\` | 선택 경고 0 · 각 종료 0 | D03/D06 · [r1](receipts/main/range-exclusive-baseline-r1/) · [r2](receipts/main/range-exclusive-baseline-r2/) | 실설치·실행 범위 밖 |
| \`pytest>=8.0.2,<8.1.1\` · unmarked | 속성 없음 · 사유 해당 없음 | \`pytest-8.1.0-py3-none-any.whl\` · \`ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e\` | 선택 경고 0 · 각 종료 0 | D04/D06 · [r1](receipts/main/range-exclusive-unmarked-r1/) · [r2](receipts/main/range-exclusive-unmarked-r2/) | 실설치·실행 범위 밖 |
| \`pytest>=8.0.2,<=8.1.1\` · baseline | true · 원사유 P | \`pytest-8.1.1-py3-none-any.whl\` · \`2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7\` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/range-inclusive-baseline-r1/) · [r2](receipts/main/range-inclusive-baseline-r2/) | 실설치·실행 범위 밖 |
| \`pytest>=8.0.2,<=8.1.1\` · unmarked | 속성 없음 · 사유 해당 없음 | \`pytest-8.1.1-py3-none-any.whl\` · \`2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7\` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/range-inclusive-unmarked-r1/) · [r2](receipts/main/range-inclusive-unmarked-r2/) | 실설치·실행 범위 밖 |
| \`pytest==8.1.1\` · baseline | true · 원사유 P | \`pytest-8.1.1-py3-none-any.whl\` · \`2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7\` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/pin-next-baseline-r1/) · [r2](receipts/main/pin-next-baseline-r2/) | 실설치·실행 범위 밖 |
| \`pytest==8.1.1\` · unmarked | 속성 없음 · 사유 해당 없음 | \`pytest-8.1.1-py3-none-any.whl\` · \`2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7\` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/pin-next-unmarked-r1/) · [r2](receipts/main/pin-next-unmarked-r2/) | 실설치·실행 범위 밖 |

표 1의 한 행은 요청식 하나와 페이지 하나의 독립 실행 두 번이다. 대상은 항상 8.1.0 wheel이다. P는 216 V05/I02의 원값 \`See https://github.com/pytest-dev/pytest/issues/12069\`이다. 선행 ID는 [출처 원장](sources.jsonl), URL·해시·플래그·로그는 [16회 행렬](matrix.csv)과 [실행 검산](receipts/main-audit.json)에 있다.

| 경쟁 설명 | 한 변수 통제 | 실제로 뒤집힌 값 | 권고 문구 |
| --- | --- | --- | --- |
| 버전 정렬만으로 배타적 상한의 선택을 설명할 수 있다 | 같은 파일·URL·Python에서 8.1.0의 속성만 제거 | \`<8.1.1\`에서 8.0.2 → 8.1.0, 선택 경고는 양쪽 0 | 신규 범위는 상한과 파일 상태를 함께 확인한다. |
| 정확 핀의 결과가 같으면 경고도 같다 | \`==8.1.0\`에서 같은 속성 제거 | 파일과 SHA가 그대로이며 report flag true → false, stderr 선택 경고 각 1 → 0 | 원파일을 정확히 재현할 때 파일과 철회 사유를 함께 연결한다. |
| 상태를 바꾸면 다른 범위와 핀도 언제나 뒤집힌다 | 포함 상한과 다음판 핀에서 같은 제거 | 두 요청 모두 8.1.1 유지, 선택 경고 0 | 상한이 8.1.1을 허용할 때 그 파일을 대체 후보로 검토한다. |
| 빈 철회 사유나 부재는 같은 신호다 | 정확 요청에서 사유 빈 값 또는 링크 제거 | 보조 2조건 검사 전 | 속성과 링크의 상태를 각각 기록한다. |

표 2의 한 행은 경쟁 설명 하나와 그 설명을 판별하는 통제다.

## Q1–Q7 1차 판독

- **Q1** 중앙과 인계의 의존 SHA가 일치한다. 4개 API 본문 지문과 3개 wheel의 정확 키를 검산했다. D00–D08.
- **Q2** 네 공식 wheel 중 대상 프로젝트 wheel은 3개다. 세 SHA와 METADATA·WHEEL 태그가 일치한다. 등록 파일과 로컬 HTML 속성의 연결은 [pin](inputs.json), [fixture](index/), [입수](receipts/wheel-fetch.json)로 추적한다.
- **Q3** PyPA는 비철회 옵션이 존재하면 철회를 건너뛰도록 하고, 정확 핀 예외·경고에는 재량을 둔다. 이 pip는 적용 후보가 모두 철회이고 정확 핀일 때만 이 인덱스 가지에서 남긴다. R01–R06, P01–P10.
- **Q4** 기본 16/16 모두 report v1 한 건과 로컬 페이지 GET 및 wheel GET 한 건씩이 일치했다. 실패 0. [실행 명령](receipts/main-command.json) · [행렬](matrix.csv)
- **Q5** 오직 기준의 정확 8.1.0에서 stderr 선택 경고가 2회다. 같은 실행 stdout은 Would install이며 전후 배포물 inventory는 pip만 있다. H01의 2024 캐시 로그는 별도 사례다.
- **Q6** 16회는 한 속성을 교체한 실제 비교다. 빈 사유와 링크 부재는 실행 대기 중이다.
- **Q7** 원문 DOI와 철회 공고 DOI 및 색인 관계는 X01–X03에 있다. 별도 DOI의 정정·원문 대조 X05–X06을 다음 묶음에서 판독한다.
