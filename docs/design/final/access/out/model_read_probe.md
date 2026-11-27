# 모델 판독 눈가림 시험 (2026-11-27 05:2xZ)

이 클라우드 세션의 셸(`curl`, `urllib`)은 `docs.python.org`·`support.mozilla.org`에 닿지 않는다(프록시 거절, [reach.tsv](reach.tsv)). 같은 세션의 Claude Code 내장 읽기 도구(WebFetch)는 두 주소를 200으로 읽었다. WebFetch는 원문 바이트가 아니라 "페이지를 마크다운으로 바꾼 뒤 작은 모델이 질문에 답한 글"을 돌려준다. 그래서 기대값을 알려 주지 않고(눈가림) 앵커만 주어 물었고, 답을 따로 얻은 원천과 비교했다.

| 물은 것 | 돌아온 답 | 비교한 원천 | 결과 |
| --- | --- | --- | --- |
| `docs.python.org/3.13/library/asyncio-queue.html`의 `class asyncio.Queue(maxsize=0)` 바로 아래 첫 두 문장을 글자 그대로 | "A first in, first out (FIFO) queue." / "If maxsize is less than or equal to zero, the queue size is infinite." (기울임이 빠졌다고 스스로 밝힘) | `raw.githubusercontent.com/python/cpython/3.13/Doc/library/asyncio-queue.rst` L28–L31: `A first in, first out (FIFO) queue.` / `If *maxsize* is less than or equal to zero, the queue size is infinite.` | 2/2 일치(꾸밈 표시 제외) |
| `support.mozilla.org/en-US/kb/future-of-pocket/history`의 첫 다섯 개정 행(날짜, 개정 번호, 설명) | 317710(2026-01-08, "See Bug 2008808"), 313578(2025-11-12, 링크 문구·사소한 수정), 313551(2025-11-12, "Sunset info updated per data deletion"), 308427(2025-10-09, "Changed to November 12."), 308355(2025-10-08, "Changed sunset to November 6.") | [`ledger/fixtures/unit2/x1_events.json`](../../../../../ledger/fixtures/unit2/x1_events.json)(연구 원장 AF-RES-152 판독을 옮긴 기록): 308355, 308427, 313551 | 겹치는 3개 모두 일치. 기록에 없는 새 개정 2개(313578, 317710) |
| `docs.softwareheritage.org/user/faq/` | 본문 대신 봇 차단 화면("Access Denied", Anubis) | 없음 | 봇 차단 실패 종류의 실제 예 |

읽는 법. 표본이 작다(문장 2, 개정 행 3). 모델이 요약하며 꾸밈을 버렸고, 날짜는 페이지 표시 시각이라 시간대가 붙지 않았다. 이 경로는 "모델이 그렇게 읽었다"는 결속(m)까지만 준다. 바이트·지문이 없어서 기록 재생과 판 비교에 쓸 수 없다. 09 문서 4.7절의 규칙대로 확인 단계 L3로 세지 않고, 교차 확인 재료로만 쓴다.
