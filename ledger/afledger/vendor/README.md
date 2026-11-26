# vendor

| 파일 | 출처 | 고정 |
| --- | --- | --- |
| `rcore_normalize.py` | [laadkke-arch/opensource `tools/rcore/normalize.py`](https://github.com/laadkke-arch/opensource/blob/7c8f9860a6f1f39951ef6c2f2a4cfc4d8a5881bf/tools/rcore/normalize.py) | 커밋 `7c8f9860a6f1f39951ef6c2f2a4cfc4d8a5881bf`, blob `1132b02225f8757e5a1e82b628c16b21bf584f82`, 규칙 판 n1 |

바이트 그대로 둔다. 고치지 않는다(시험 `test_p0.NormalizeN1.test_vendored_file_is_byte_identical`이 blob 해시를 확인한다).
규칙을 바꿔야 하면 출처 저장소에서 판을 올리고(n2) 다시 가져온다. 이 저장소에서 덧붙이는 규칙은 `afledger/normalize.py`에 둔다.
같은 blob이 opensource의 `dot-a`·`dot-b`·`dot-c`·`claude/project-thread-a3oi3x`(머리 `9c091fc1`) 모두에 있다.
