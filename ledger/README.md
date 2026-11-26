# ledger · 확인 장부 코어 (첫 구현 단위)

설계서 [docs/design/final](../docs/design/final/README.md)의 첫 구현 단위(06 3절)다. Python 3.11 이상, 표준 라이브러리와 SQLite FTS5만 쓴다.
구현하면서 드러난 설계 수정점은 [08-implementation.md](../docs/design/final/08-implementation.md)에 쌓는다.

```sh
python3 -I ledger/tests/run.py          # 시험(네트워크 없이 기록 재생)
```

| 경로 | 내용 |
| --- | --- |
| `afledger/ledger.py` | 엔진. 설계 예제 `docs/design/final/db/ledger.py`에서 옮겼다 |
| `afledger/config.py` | 설정 상수와 규칙 판(한 곳) |
| `afledger/sql/` | 공용 장부(`commons.sql`)와 프로젝트 장부(`project.sql`) 스키마 |
| `tests/test_ported.py` | 설계 예제 시험 33개(단언 그대로) |
