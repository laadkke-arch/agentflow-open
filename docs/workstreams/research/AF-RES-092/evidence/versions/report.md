# AF-RES-092 인접 단계 기준판 메타데이터

본문 검색 전에 공개판 선택만 조사했다. 실제 설치판·출력 성공은 전부 미확인이다. 아래는 현재 공개된 릴리스 기록에서 복원한 선택이며 삭제된 릴리스의 부재까지 보장하지 않는다.

| 부품 | R0 이전 기준판 | commit SHA | 공개 UTC | 바로 다음 안정판/한계 |
| --- | --- | --- | --- | --- |
| rmarkdown | [v2.26](https://github.com/rstudio/rmarkdown/releases/tag/v2.26) | 561be5a7c7fde2b76a5649624d0c56373b8d86fa | 2024-03-05T22:38:05Z | v2.27 2024-05-20T21:43:18Z |
| Eisvogel | [2.4.2](https://github.com/Wandmalfarbe/pandoc-latex-template/releases/tag/2.4.2) | cd58c398c7fbcca53ae891759e3bced71b37d84c | 2023-11-25T14:20:36Z | v2.5.0 2024-10-03T12:38:00Z |
| Quarto | [v1.4.553](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.4.553) | 466d959674507930685b2c977e878495932152ba | 2024-04-03T18:08:19Z | v1.4.554 2024-05-01T21:50:57Z |
| Better BibTeX | [v6.7.174](https://github.com/retorquere/zotero-better-bibtex/releases/tag/v6.7.174) | 0fcbd1ba96b8ec61fb4704ca7e2a32d89d5cc390 | 2024-04-11T12:15:22Z | v6.7.176 2024-04-23T20:17:49Z |
| CSL documentation | [v1.0.2](https://github.com/citation-style-language/documentation/releases/tag/v1.0.2) | ea75983cc9f409a88ede93878d9525a734dbeb63 | 2021-10-22T22:29:30Z | 현재 공개 릴리스 메타데이터를 되읽은 결과이며 당시 설치판 또는 삭제된 릴리스 부재를 증명하지 않는다. |
| fontspec | [v2.9a](https://ctan.org/ctan-ann/id/mailman.6477.1707925238.3764.ctan-ann%40ctan.org) | a4be8a1359997e72612532882acaa64bb86e0566 | 2024-02-14T15:40:36Z | CTAN release announcement date and current tag SHA are independently observed; contemporaneous exact archive bytes not acquired. |
| booktabs | [1.61803398](https://ctan.org/ctan-ann/id/mailman.3249.1579100757.2586.ctan-ann%40ctan.org) | 미확인 | 2020-01-15T15:04:53Z | package internal Jan 12 date not checked; mirrors.ctan.org .dtx request returned HTTP402, so no file fingerprint/immutable archive SHA yet. |

## 선택 경계

- rmarkdown, Eisvogel, CSL: 100개 요청의 응답이 각각 46/29/2건으로 끝나는 전체 공개 release 목록을 읽었다.
- Quarto: 페이지 1–3의 300개 기록을 기계적으로 비교했다. 2024-04-10 v1.5.29는 prerelease라 제외한다. v1.4.553 이후의 첫 stable은 pins.json에 보존했다. 탐색용 page4도 메타데이터만 저장했다.
- Better BibTeX: 페이지 1–3의 300개 기록을 비교했다. v6.7.174의 annotated tag object와 실제 commit SHA를 구분한다.
- fontspec: GitHub release 목록은 2024-04-27 이전 기록이 없어서 CTAN 공지(2024-02-14)와 다음 공지(2024-04-28)를 사용했다. v2.9a의 패키지 표기 날짜는 2024-02-13이며 공지 시각과 다르다.
- booktabs: 현재 공식 CTAN 버전과 2020-01-15 공지를 연결했다. .dtx 다운로드는 HTTP402로 실패해 내부 날짜·바이트 SHA는 공석이다.

## 노출과 계산

이 작업의 메타데이터 조회는 A/B의 후보 본문 검색·열람 예산과 별도다. sources 최소 26건/매뉴얼8건을 메타데이터로 채우지 않도록 provenance의 counted_direct는 false다. CTAN 공개판을 확인하는 웹 검색/공지가 일반 기능 요약을 함께 노출했으나, 본 연구자가 신규 질문이나 해답을 읽지는 않았고 그 기능 요약을 root에 전달하지 않았다.

파일: pins.json은 사용판 봉인 후보, provenance.jsonl은 확인/실패 원장, 나머지 JSON은 내용 없이 줄인 release/tag 메타데이터 영수증이다. 코드·설치·매뉴얼·질문별 해법은 조사하지 않았다.
