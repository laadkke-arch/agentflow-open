# access/ · 원문 접근 측정

[09-source-access.md](../09-source-access.md)의 측정을 다시 돈다. 읽기만 하고, 이 클라우드 환경에서 열린 곳(GitHub raw, 패키지 저장소, GitLab API)만 쓴다.

```sh
bash docs/design/final/access/reach.sh > /tmp/reach.tsv                       # 호스트마다 GET 한 번
python3 -I docs/design/final/access/routes.py ledger/fixtures/catalog-p5/targets.jsonl.gz /tmp/routes.json 40   # 경로 나누기 + 표본 대조(약 10분, 요청 약 850회)
python3 -I docs/design/final/access/post.py ledger/fixtures/catalog-p5/targets.jsonl.gz /tmp/routes.json /tmp/post.json
```

| 파일 | 내용 |
| --- | --- |
| `reach.sh`, `out/reach.tsv` | 2026-11-27T05:33Z 호스트 도달 결과 |
| `routes.py`, `out/routes40.json`, `out/routes40.log` | 경로 나누기(`classify`)와 경로별 표본 40개 대조. 씨앗 20261127. 요청 기록 포함 |
| `post.py`, `out/post40.json` | 놓친 것을 "번역된 인용"과 그 밖으로 나누고 모집단 추정 |
| `out/model_read_probe.md` | 내장 읽기 도구(WebFetch) 눈가림 시험 기록 |

대조 규칙은 이 측정용 임시 규칙이다(NFKC·소문자, rst 역할·마크다운 기호 제거, 낱말 줄 그대로 있으면 exact, 4-gram 80% 이상이면 near). 수집소의 L3 규칙을 대신하지 않는다.
