# Python 모집·원요구 봉인

현재 58개 공개 비포크 pypa 저장소 목록을 고정한 뒤 원순번 1–10의 release/tag와 적격 후보 5개의 마지막 정식 tag를 판독했다. 첫 3자리는 bandersnatch(5), build(9), cibuildwheel(10)이다. 이 선택은 사이트 접근성, CI 성공, 두 요구의 확보 여부를 보기 전에 끝냈다. 후순번 48개는 교체 후보로 검사하지 않았다.

| 자리 | tag / SHA | 실제 문서 안내 | 두 번째 조건 |
| --- | --- | --- | --- |
| P1 bandersnatch | 7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74 | README L18의 en/latest/ 문서 | inspected README/index/CONTRIBUTING/MAINTAINERS에서 미확인 |
| P2 build | 1.3.0 / 60e8752f69178d2b2c3563e9c8fa17aa6e11b12c | README L13·31의 build.pypa.io 문서 | inspected README/index/release/mission에서 미확인 |
| P3 cibuildwheel | v3.3.0 / 63fd63b352a9a8bdcc24791c9dbee952ee9a8abc | README stable 문서·옵션 심층 링크 | L53은 Python 2 등 지원종료 Python을 위한 en/1.x/ 문서로 안내 |

P3의 1.x는 특정 1.x patch 판의 불변 아카이브를 약속한 URL이 아니다. P1/P2의 단일 공개 URL에서 조건 두 개를 만들지 않았다. 각 원문 URL·고정 tag·절·실제 읽은 UTC·지문은 sources.jsonl과 http-receipts.jsonl에, 전체 포함/제외는 frame_updates.json에 있다.

사전 노출: README의 Read the Docs 배지/문서 URL과 tree의 설정파일 이름을 보았다. 실제 설정 내용, 현재 문서 HTML, 공개 배포 로그, 공급자 안내는 이 봉인 단계에서 읽지 않았다. 단 CONTRIBUTING의 nox 문서 build/serve 명령과 패키지 릴리스 정책은 원요구 탐색 중 노출되었다. 이를 문서 게시 성공 근거로 쓰지 않는다.

모집의 시간 한계: 목록은 2026-11-23 현재 소속이다. tag 시점의 조직 소속을 별도로 입증하지 않았다. 공식 GitHub release가 없는 제외 저장소는 공개 tag도 없었다. 외부 서비스에서 있었을 수 있는 발표를 부재로 단정하지 않는다.

선정 3자리를 고정했고 요구 슬롯은 총 6개 중 관측 4개·미확인 2개다. 두 독립 보존 조건의 소비자 자리는 1/3이다. 아직 배포 사실 판정은 없다.
