# AF-RES-019 진행

## 1. 기준과 사전 접근 확인

GitHub에서 chore/workspace-foundation 최신 SHA `ded7f3838fe16f1cf401789e99e957b1ebebff1b`를 고정했다. AF-RES-009와 AF-RES-015의 두 HANDOFF는 진행표의 result_commit에서 열었다. 기준 문서와 연구 운영/제품 범위를 읽었다.

| 호스트 | 경로 | HTTP 응답 순서 | 결과 |
| --- | --- | --- | --- |
| github.com | anonymous git clone | 200, 200, 200, 200 | 접근 |
| gitlab.com | anonymous git clone | 200, 200, 200, 200 | 접근 |
| codeberg.org | anonymous git clone | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| pypi.org | anonymous HTTPS GET | 200, 200 | 접근 |
| registry.npmjs.org | anonymous HTTPS GET | 200, 200 | 접근 |
| crates.io | anonymous HTTPS GET | 200, 200 | 접근 |
| rubygems.org | anonymous HTTPS GET | 200, 200 | 접근 |
| redis.io | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| git-scm.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| web.archive.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| api.github.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| api.deps.dev | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| archive.softwareheritage.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| raw.githubusercontent.com | anonymous HTTPS GET | 200, 200 | 접근 |
| github.blog | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.github.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.npmjs.com | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |
| docs.pypi.org | anonymous HTTPS GET | 403 | 미확인(프록시 CONNECT 또는 원본 실패, 확인은 VERIFICATION.json) |

첫 원격 묶음 이후의 다음 행동은 사건 출처 직접 읽기와 후보 검증이다. 정확한 URL·요청·시각은 VERIFICATION.json에 있다.

## 2. 재검증과 정정

초기 부분 clone이 기본 브랜치 밖 Redis 릴리스 태그를 누락했다. 최초 결과의 Redis T−1개월 마지막 태그 이후 값은 4,847일이었다. 원격 태그 전체를 별도 fetch하는 경로로 바꿨고 원장·경보·주기·비용을 다시 계산했다. 최초 수치는 이력에 남겨 정정 범위를 추적할 수 있다. 임계값이나 사건·대조 표본은 이 수정에서 바꾸지 않았다.

추가 반례 확인에서 npm 다운로드 호스트 api.npmjs.org의 익명 GET 1회가 CONNECT 403이었다. 역사적인 deprecated 상태와 다운스트림 사용량을 별도 자료로 구별했다. 우회 호출은 하지 않았다.
