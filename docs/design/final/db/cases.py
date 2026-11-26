"""두 사례(A: R1 = AF-RES-012 P03.w, B: EVAL-X1 Pocket)와 장면 2 사례(R2 ii-svn-log)를
확인 장부 구조 v1 엔진으로 끝까지 재생한다.

출처 표시:
  [원장] 저장소 연구 원장의 행. 커밋과 경로를 함께 적는다.
  [설치본] 이 저장소를 실행한 컴퓨터의 CPython 표준 라이브러리 파일(경로, 줄, sha256).
  [영수증] receipts/r1_queue.py를 3.13.18과 3.12.3에서 실행한 출력.
  [열람] 2026-11-26에 공개 규격 원문을 열어 옮긴 짧은 인용.
  [고정 자료] 실제 검색 엔진·판독 모델 대신 이 재생에 넣은 입력. 설계자의 가정이다.

실행: python3 -I cases.py            (요약 출력)
      python3 -I cases.py --json     (전체 결과 JSON)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ledger import Ledger, sha256  # noqa: E402

FIX = HERE / "fixtures"
RECEIPTS = HERE / "receipts"
PROGRAM_SHA = sha256((RECEIPTS / "r1_queue.py").read_text(encoding="utf-8"))

CPY_QUEUES = "https://github.com/python/cpython/blob/main/Lib/asyncio/queues.py"
CPY_LOCKS = "https://github.com/python/cpython/blob/main/Lib/asyncio/locks.py"
PY_CHANGELOG = "https://docs.python.org/3/whatsnew/changelog.html"

# [설치본] /usr/local/lib/python3.13/asyncio/queues.py sha256 9ce87bf6…, /usr/lib/python3.12/asyncio/queues.py sha256 8f020744…
Q313_BOUNDED = ('If maxsize is less than or equal to zero, the queue size is infinite.\n'
                '    If it is an integer greater than 0, then "await put()" will block when\n'
                '    the queue reaches maxsize, until an item is removed by get().')
Q312_BOUNDED = ('If maxsize is less than or equal to zero, the queue size is infinite. If it\n'
                '    is an integer greater than 0, then "await put()" will block when the\n'
                '    queue reaches maxsize, until an item is removed by get().')
Q313_SHUTDOWN = ('Shut-down the queue, making queue gets and puts raise QueueShutDown.\n'
                 '        By default, gets will only raise once the queue is empty.\n'
                 '        All blocked callers of put() and get() will be unblocked.')
Q313_TASKDONE = ('If a join() is currently blocking, it will resume when all items\n'
                 '        have been processed (meaning that a task_done() call was received\n'
                 '        for every item that had been put() into the queue).')
L313_SEM = ('A semaphore manages an internal counter which is decremented by each\n'
            '    acquire() call and incremented by each release() call.  The counter\n'
            '    can never go below zero; when acquire() finds that it is zero, it\n'
            '    blocks, waiting until some other thread calls release().')

L312_SEM = ('A semaphore manages an internal counter which is decremented by each\n'
            '    acquire() call and incremented by each release() call. The counter\n'
            '    can never go below zero; when acquire() finds that it is zero, it blocks,\n'
            '    waiting until some other thread calls release().')

# [열람] OAI-PMH 2.0 (Document Version 2015-01-08) §2.5.1, §2.7.1 / RFC 8493 (2018-10) §2.1.3, §3
OAI_URL = "https://www.openarchives.org/OAI/openarchivesprotocol.html"
OAI_PERSISTENT = "persistent: the repository maintains information about deletions with no time limit."
OAI_NO = "no: the repository does not maintain information about deletions."
OAI_INCLUSIVE = 'Range limits are inclusive: from specifies a bound that must be interpreted as "greater than or equal to"'
RFC8493_URL = "https://www.rfc-editor.org/rfc/rfc8493"
RFC8493_MANIFEST = "Every payload manifest MUST list every payload file name exactly once."
RFC8493_VALID = ("A complete bag where every checksum in every manifest has been successfully verified "
                 "against the corresponding file.")

# [원장] AF-RES-152 @ ba038a0aa589985d5f14549fa55f628f02fa151d events.jsonl / sources.jsonl
KB = "https://support.mozilla.org/en-US/kb/future-of-pocket"
KB_HISTORY = "https://support.mozilla.org/en-US/kb/future-of-pocket/history"
MOZ_BLOG = "https://blog.mozilla.org/en/mozilla/building-whats-next/"
MOZ_FEED = "https://blog.mozilla.org/en/feed/"          # [고정 자료] 공급자 소식 채널 주소는 설계자의 가정
POCKET_HOME = "https://getpocket.com/"                    # [고정 자료] T0 검색 결과 주소
POCKET_EVENTS = [
    # (외부 ID, 채널에서 처음 보인 시각, 판 키, 효력 시각, 원장 출처 ID, 원장 판독문, 대체 효과)
    ("297191", "2025-05-22T12:00:00Z", "rev:297191", "2025-05-22T00:00:00Z", "MO-POCKET-BASE",
     "신규 설치 목록에서 5월 22일 빠짐. 기존 이용자는 재설치할 수 있고 7월 8일 이후 웹은 내보내기 전용, 그 기한은 10월 8일로 공지.",
     "changes_value"),
    ("300072", "2025-07-09T00:00:00Z", "rev:300072", "2025-07-08T00:00:00Z", "MO-POCKET-STOP",
     "저장 종료, 기존 내보내기는 계속(내보내기 전용). 종료와 내보내기 전용 모드가 분리된다.", "invalidates"),
    ("308355", "2025-10-09T00:00:00Z", "rev:308355", "2025-10-08T00:00:00Z", "MO-POCKET-D1",
     "같은 안내의 내보내기 기한이 11월 6일로 갱신됐다.", "changes_value"),
    ("308427", "2025-10-10T00:00:00Z", "rev:308427", "2025-10-09T00:00:00Z", "MO-POCKET-D2",
     "같은 안내의 내보내기 기한이 11월 12일로 다시 갱신됐다.", "changes_value"),
    ("313551", "2025-11-13T00:00:00Z", "rev:313551", "2025-11-12T00:00:00Z", "MO-POCKET-END",
     "데이터 내보내기와 API를 비활성화했고 삭제 대기에 두었다고 발표했다. 도움말 주소는 계속 열린다.", "invalidates"),
]
LEDGER_152 = "AF-RES-152@ba038a0aa589985d5f14549fa55f628f02fa151d sources.jsonl "

# [원장] AF-RES-149 @ bc19a446b02049b8c7569ca5de9da8afce255461 sources.jsonl L56 S-A-W1-1, L51 L10
II_SVN = "https://note.com/just_vole1456/n/ncea39628b332"
II_SVN_READING = ("제작자 게시물: SVN URL 입력, GUI Submit 또는 CLI 1회 실행으로 커밋 이력을 Excel에 출력, "
                  "SVN 없는 PC에서 정적 열람 및 공유; Vector 다운로드 연결")
DIGEST = "https://forest.watch.impress.co.jp/docs/digest/2063126.html"


def load_receipt(L: Ledger, fname: str, ran_at: str) -> tuple[int, dict]:
    d = json.loads((RECEIPTS / fname).read_text(encoding="utf-8"))
    rid = L.receipt(d["runtime"], PROGRAM_SHA, d["input"], d["results"], ran_at)
    return rid, {r["pattern"].split()[0]: r for r in d["results"]}


def edition_matches_runtime(obs, ctx) -> bool:
    if "python/cpython" not in obs["url"]:
        return True
    rt = ctx.get("runtime", "")          # 예: "CPython 3.13"
    ver = rt.split()[-1] if rt else ""
    return obs["edition_key"].lstrip("v").startswith(ver + ".")


# =====================================================================================
# 수집: AF-RES-012 자료집을 "청구 없는 관측"으로 서랍에 넣는다(소개만 봄).
# =====================================================================================
def preload_catalog(L: Ledger, at="2026-11-20T00:00:00Z") -> dict[str, int]:
    ids = {}
    for line in (FIX / "af-res-012" / "entries.jsonl").read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        oid, _ = L.observe(url=e["url"], edition_key="catalog@cb602858", edition_kind="fetch",
                           position="catalog entry", at=at, method="intro_only", quote=e["D-b"]["en"],
                           quote_lang="en", statement=e["D-b"]["ko"], via="collection",
                           evidence_ref=f"AF-RES-012@cb602858 corpus/entries.jsonl#{e['id']}")
        # 012: 한계 문장(D-c)은 근접 오답을 늘렸으므로 검색 꼬리표에는 D-b(무엇이 들어가 무엇이 나오나)만 쓴다.
        L.tag(oid, "summary", "one_up", "en", e["D-b"]["en"], written_from="catalog_description")
        L.tag(oid, "summary", "one_up", "ko", e["D-b"]["ko"], written_from="catalog_description")
        ids[e["id"]] = oid
    return ids


# =====================================================================================
# 사례 A: R1 (AF-RES-012 P03.w)
# =====================================================================================
def p03w():
    for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines():
        q = json.loads(line)
        if q["id"] == "P03.w":
            return q
    raise KeyError("P03.w")


R1_NEEDS = [  # [고정 자료] 접수 단계가 요청에서 뽑은 칸별 필요 문장(영어). 비공개.
    {"slot": "input", "lang": "en", "text": "a lazy input iterator that the producer can pause"},
    {"slot": "output", "lang": "en",
     "text": "the producer waits when the queue is full and puts again only after a worker removes an item"},
    {"slot": "keeps", "lang": "en", "text": "at most eight items wait in the queue and at most four jobs run at once"},
    {"slot": "breaks_when", "lang": "en",
     "text": "tasks are created for every input ahead of time or items move into an unbounded buffer"},
    {"slot": "summary", "lang": "en",
     "text": "bounded waiting work where completion of a worker frees capacity and lets the producer resume"},
]


def case_a(L: Ledger, catalog: dict[str, int]) -> dict:
    out = {}
    p = L.project("A")
    q = p03w()
    t0 = "2026-11-26T01:00:00Z"
    reqs = [
        {"code": "H1", "kind": "must", "text": "대기 큐 안의 항목 수는 최대 8개이고 처리 중 작업은 최대 4개여야 한다."},
        {"code": "H2", "kind": "must_not", "text": "sink가 느려지면 producer가 기다려야 하며, 모든 입력에 대해 task를 미리 만들거나 다른 무제한 buffer로 옮기면 안 된다."},
        {"code": "H3", "kind": "must", "text": "처리 완료/용량 회복을 투입 재개의 근거로 삼고, 단순 시간 경과만으로 처리 중 상한을 넘겨서는 안 된다."},
        {"code": "S1", "kind": "must", "text": "입력이 끝났음을 일꾼에게 알린다(대상 부분 '작업 투입·완료 신호'에서 추론).", "provenance": "inferred"},
        {"code": "X", "kind": "out_of_scope", "text": "전체 RAM byte 상한, producer가 손에 든 한 항목, 변환 내부 메모리, 처리량 향상 수치, 강제 즉시 취소, 장애 복구"},
    ]
    ctx = {
        "runtime": {"value": "CPython 3.13", "provenance": "studio", "source": "프로젝트 실행 환경 설정 [고정 자료]"},
        "producer_pausable": {"value": "yes", "provenance": "explicit"},
        "single_loop": {"value": "yes", "provenance": "explicit"},
        "drop_allowed": {"value": "no", "provenance": "explicit"},
        "workers_fixed": {"value": "yes", "provenance": "studio", "source": "선택 부분의 일꾼 생성 코드 [고정 자료]"},
    }
    req1 = L.intake(p, request_key="R1", rev=1, at=t0, text=q["ko"], selected_part="파이프라인: 작업 투입·완료 신호",
                    requirements=reqs, context=ctx, prior={"known": []}, needs=R1_NEEDS)
    d = L.decide("Queue(maxsize=8)+고정 일꾼 4", "Queue(maxsize=8)+고정 일꾼 4")
    L.interpret(p, req1, "처리 중 4", "동시에 실행 중인 작업 수", "일꾼 수", d, t0)
    out["clarify"] = d

    # 찾기: 서랍(내용어, 칸 둘 이상) + 감사용(기능어 포함) + 새 검색(고정 자료)
    hits = L.search_drawer(p, req1, t0, k=12)
    audit = L.search_drawer(p, req1, t0, k=400, min_slots=1, include_function_words=True, log=False)
    inv = {v: k for k, v in catalog.items()}
    out["drawer"] = [(inv.get(h["obs_id"], h["obs_id"]), h["slots"], h["matched"], h["eligible"]) for h in hits]
    out["drawer_audit_accidents"] = [(inv.get(h["obs_id"]), h["matched"]) for h in audit if h["lexical_accident"]]
    out["drawer_audit_toyota"] = [(h["rank"], h["matched"], h["lexical_accident"]) for h in audit
                                  if h["obs_id"] == catalog["toyota-jit"]]
    out["drawer_content_toyota"] = [(h["rank"], h["matched"], h["eligible"]) for h in
                                    L.search_drawer(p, req1, t0, k=400, min_slots=1, log=False)
                                    if h["obs_id"] == catalog["toyota-jit"]]
    fresh = L.search_fresh(p, req1, t0, {
        "direct": [{"url": "https://docs.python.org/3.13/library/asyncio-queue.html", "why": "asyncio queue bounded"},
                   {"url": "https://docs.python.org/3.13/library/asyncio-sync.html", "why": "semaphore"}],
        "relation": [{"url": "https://pypi.org/pypi/aiolimiter/1.3.0/json", "why": "limit rate asyncio"}],
        "domain_guess": [{"url": "https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.4/README.md",
                          "why": "backpressure demand"},
                         {"url": "https://global.toyota/en/company/vision-and-philosophy/production-system/",
                          "why": "pull production kanban"}],
        "language": [],
    })
    out["fresh_count"] = len(fresh)

    # 확인: 사용자 판(3.13)의 원문 줄 + 실행 영수증
    rid13, r13 = load_receipt(L, "r1_cpython313.json", t0)
    q1, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="L36–38",
                      at=t0, method="read_line", quote=Q313_BOUNDED, quote_lang="en",
                      statement="크기 상한이 양수면 가득 찬 대기열에 put을 await한 쪽은 get으로 항목이 빠질 때까지 기다린다.",
                      flip_position="L36–38 'await put() will block when the queue reaches maxsize'", project=p)
    q2, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="L252–258",
                      at=t0, method="read_line", quote=Q313_SHUTDOWN, quote_lang="en",
                      statement="shutdown()은 대기열을 닫고, 막혀 있던 put·get을 풀며, 기본값에서는 비었을 때 get이 QueueShutDown을 낸다.",
                      flip_position="L252 def shutdown (3.13에서 추가)", project=p)
    q3, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="L227–229",
                      at=t0, method="read_line", quote=Q313_TASKDONE, quote_lang="en",
                      statement="join은 넣은 항목마다 task_done이 와야 끝난다.", project=p)
    s1, _ = L.observe(url=CPY_LOCKS, edition_key="v3.13.18", edition_kind="release", position="L355–358",
                      at=t0, method="read_line", quote=L313_SEM, quote_lang="en",
                      statement="세마포어는 acquire마다 줄고 release마다 느는 계수기이며 0이면 acquire가 기다린다.", project=p)
    ea, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="run:r1_queue.py A",
                      at=t0, method="executed", receipt_id=rid13,
                      statement="대기 최대 {max_waiting}, 처리 중 최대 {max_in_flight}, 작업 객체 {tasks_created}, producer 대기 {producer_waits}회, 끝 신호 {end_signal}".format(**r13["A"]),
                      project=p)
    eb, _ = L.observe(url=CPY_LOCKS, edition_key="v3.13.18", edition_kind="release", position="run:r1_queue.py B",
                      at=t0, method="executed", receipt_id=rid13,
                      statement="근접 오답: 처리 중 최대 {max_in_flight}이지만 작업 객체 {tasks_created}개를 미리 만든다".format(**r13["B"]),
                      project=p)
    ec, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="run:r1_queue.py C",
                      at=t0, method="executed", receipt_id=rid13,
                      statement="일꾼 하나가 get 뒤 task_done 없이 죽으면 join이 1초 안에 끝나지 않는다(남은 미완료 1)", project=p)
    ed, _ = L.observe(url=CPY_LOCKS, edition_key="v3.13.18", edition_kind="release", position="run:r1_queue.py D",
                      at=t0, method="executed", receipt_id=rid13,
                      statement="허가를 작업 생성 전에 얻으면 살아 있는 작업 {max_alive_tasks}개 이하, 대기열 없음".format(**r13["D"]),
                      project=p)
    L.contrast(ea, eb, "입력마다 작업 객체를 미리 만드는가", "아니오(일꾼 4개만)", "예(40개)", rid13)
    L.contrast(ea, ed, "대기열 길이 상한을 직접 정하는가", "예(maxsize 8)", "아니오(대기열 없음)", rid13)
    # 원문 쪽 꼬리표(요청 문장이 아니라 인용에서 쓴다)
    L.tag(q1, "output", "concrete", "en", "await put() blocks when the queue reaches maxsize until get() removes an item")
    L.tag(q1, "keeps", "concrete", "en", "the queue never holds more than maxsize items")
    L.tag(q1, "breaks_when", "concrete", "en", "maxsize less than or equal to zero makes the queue size infinite")
    L.tag(q1, "summary", "one_up", "en", "a bounded queue makes the producer wait while it is full; each get frees one slot")
    L.tag(q2, "output", "concrete", "en", "shutdown makes gets and puts raise QueueShutDown and unblocks waiting callers")
    L.tag(s1, "keeps", "concrete", "en", "a counter that never goes below zero; acquire waits at zero until release")
    out["opens_t0"] = L.opens.get(p, 0)

    # 원리 관문: 공장 끌어당김(Toyota)과 스트림 요청량(Reactive Streams)
    g = L.gate(role_map=[("빈 자리 표", "대기열 자리"), ("아래 공정의 인출", "get")],
               invariant_quote=None,  # 자료집 소개문뿐, 고정판 원문 절 인용 없음
               break_input="일꾼이 끝 신호 없이 죽는다(카드 분실)",
               baseline_prediction="join이 끝나지 않는다", principle_prediction="join이 끝나지 않는다",
               target_doc_states_it=True)
    out["gate_r1"] = g

    # 판정 쪽지
    prem_q = {"producer_pausable": "yes", "workers_fixed": "yes", "drop_allowed": "no"}
    for code in ("H1", "H2", "H3"):
        L.judge(p, req1, code, ea, "Y", "direct", "L4", "영수증 A와 L36–38", t0, premises=prem_q)
    L.judge(p, req1, "S1", q2, "Y", "direct", "L2", "3.13 shutdown 절", t0, premises={"runtime": "CPython 3.13"})
    L.judge(p, req1, "H2", eb, "N", "reference", "L4", "작업 객체 40개", t0)
    L.judge(p, req1, "H1", ed, "U", "transplant", "L4", "대기열 길이를 직접 정하지 않음", t0, premises={"producer_pausable": "yes"})
    L.judge(p, req1, "H2", ed, "Y", "transplant", "L4", "허가를 먼저 얻으면 producer가 기다림", t0, premises={"producer_pausable": "yes"})
    L.judge(p, req1, "H3", catalog["token-bucket"], "N", "reference", "L1", "시간으로 재개(자료집 소개문)", t0)
    L.judge(p, req1, "H3", catalog["pypi-aiolimiter"], "N", "reference", "L1", "처리율 제한(자료집 소개문)", t0)

    readback = "'처리 중 4'를 동시에 실행 중인 작업 수로, '대기 8'을 아직 꺼내지 않은 항목 수로 읽었습니다."
    slot_direct = {
        "kind": "direct", "first": q1, "support": [q2, ea], "flip": [q1, q2], "ladder": "L4",
        "verb": "투입·완료 신호를 따로 만들 필요가 없습니다. 크기 상한 8인 대기열에 일꾼 4개를 고정해 붙이고, 입력이 끝나면 대기열을 닫습니다(Queue.shutdown)",
        "where": "CPython v3.13.18 Lib/asyncio/queues.py L36–38, L252–258",
        "reason": "대기 8·처리 중 4(H1), producer가 put에서 기다리고 작업 객체는 4개뿐(H2), get으로 자리가 날 때만 재개(H3). 실행에서 대기 최대 8, 처리 중 최대 4, producer 대기 8회",
        "with": "[필수] 일꾼 작업을 정확히 4개 만든다(maxsize는 꺼낸 뒤 처리 중인 수를 세지 않는다)",
        "hold": "런타임이 3.13보다 낮으면 끝 신호 부분을 끝 표지로 바꾸고, 일꾼을 항목마다 만들게 되면 이 자리를 철회합니다",
    }
    # 자리 2·3을 열지 않는다. 자리 2는 첫 절이 다른 두 해석이 남거나 필수 묶음 원소에 따로 첫 링크가 있을 때만,
    # 자리 3은 관문을 통과한 원리만. 세마포어 선획득은 H1(대기 8)이 U라 근접 대안으로, 카드 분실 시험은 범위 밖(장애 복구)이라 접는다.
    folded = [
        {"url": L.link(eb), "obs": eb, "condition": "입력마다 작업 객체를 미리 만드는가",
         "reason": "H2 위반: 처리 중은 4지만 작업 객체 40개"},
        {"url": L.link(s1), "obs": s1, "condition": "대기 8을 대기열 길이로 지키는가",
         "reason": "허가를 create_task보다 먼저 얻으면 H2는 지키지만(실행 D: 대기 0, 살아 있는 작업 최대 4) 대기 8 상한은 따로 세야 한다(H1 U)"},
        {"url": L.link(ec), "obs": ec, "condition": "범위 안의 실패 시험인가",
         "reason": "일꾼이 끝 신호 없이 죽으면 join이 끝나지 않는다. 장애 복구는 범위 밖이고 task_done 절(L227–229)이 이미 말한다. 장애 복구가 범위에 들어오면 이 시험부터 연다"},
        {"url": "https://www.rfc-editor.org/rfc/rfc3290.html", "obs": catalog["token-bucket"],
         "condition": "재개 근거가 시간인가", "reason": "H3 위반(자료집 소개문만 봄)"},
        {"url": "https://pypi.org/pypi/aiolimiter/1.3.0/json", "obs": catalog["pypi-aiolimiter"],
         "condition": "재개 근거가 시간인가", "reason": "H3 위반(자료집 소개문만 봄)"},
        {"url": "https://global.toyota/en/company/vision-and-philosophy/production-system/", "obs": catalog["toyota-jit"],
         "condition": "원리 관문", "reason": "; ".join(g["failed"])},
        {"url": "https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.4/README.md",
         "obs": catalog["reactive-streams"], "condition": "원리 관문", "reason": "; ".join(g["failed"])},
    ]
    run1 = L.compose(p, req1, t0, slots=[slot_direct], folded=folded, readback=readback,
                     budget={"opens": L.opens.get(p, 0), "fresh_results": len(fresh)})
    L.channel("python", PY_CHANGELOG, "changelog")
    for o in (q1, q2):
        L.watch(o, PY_CHANGELOG, "asyncio")
    out["run1"] = L.replay(p, run1)
    out["path_log_r1"] = L.path_log(p, req1)

    # ---- 사실 하나가 바뀐다: 배포 대상 런타임이 3.12로 고정됐다(Studio가 알림) ----
    t1 = "2026-12-10T01:00:00Z"
    ctx2 = dict(ctx, runtime={"value": "CPython 3.12", "provenance": "studio", "source": "배포 대상 설정 [고정 자료]"})
    req2 = L.intake(p, request_key="R1", rev=2, at=t1, text=q["ko"], selected_part="파이프라인: 작업 투입·완료 신호",
                    requirements=reqs, context=ctx2, prior={"known": []}, needs=R1_NEEDS)
    carried = L.carry_slips(p, req1, req2, t1, edition_matches_runtime)
    out["carry"] = {"kept": len(carried["kept"]), "dropped": carried["dropped"]}
    before = L.opens.get(p, 0)
    reuse_313 = L.reusable(CPY_QUEUES, "v3.12.3", "L24–26", project=p)
    q1b, _ = L.observe(url=CPY_QUEUES, edition_key="v3.12.3", edition_kind="release", position="L24–26",
                       at=t1, method="read_line", quote=Q312_BOUNDED, quote_lang="en",
                       statement="크기 상한이 양수면 가득 찬 대기열에 put을 await한 쪽은 get으로 항목이 빠질 때까지 기다린다.",
                       flip_position="L24–26 'await put() will block when the queue reaches maxsize'", project=p)
    q2b, _ = L.observe(url=CPY_QUEUES, edition_key="v3.12.3", edition_kind="release", position="Queue.shutdown",
                       at=t1, method="read_line", outcome="not_found", quote=None,
                       statement="3.12.3 queues.py에는 shutdown과 QueueShutDown이 없다.", project=p)
    rid12, r12 = load_receipt(L, "r1_cpython312.json", t1)
    ea2, _ = L.observe(url=CPY_QUEUES, edition_key="v3.12.3", edition_kind="release", position="run:r1_queue.py A",
                       at=t1, method="executed", receipt_id=rid12,
                       statement="대기 최대 {max_waiting}, 처리 중 최대 {max_in_flight}, 작업 객체 {tasks_created}, producer 대기 {producer_waits}회, 끝 신호 {end_signal}".format(**r12["A"]),
                       project=p)
    s1b, _ = L.observe(url=CPY_LOCKS, edition_key="v3.12.3", edition_kind="release", position="L333–336",
                       at=t1, method="read_line", quote=L312_SEM, quote_lang="en",
                       statement="세마포어는 acquire마다 줄고 release마다 느는 계수기이며 0이면 acquire가 기다린다.", project=p)
    ed2, _ = L.observe(url=CPY_LOCKS, edition_key="v3.12.3", edition_kind="release", position="run:r1_queue.py D",
                       at=t1, method="executed", receipt_id=rid12,
                       statement="허가를 작업 생성 전에 얻으면 살아 있는 작업 {max_alive_tasks}개 이하, 대기열 없음".format(**r12["D"]),
                       project=p)
    ec2, _ = L.observe(url=CPY_QUEUES, edition_key="v3.12.3", edition_kind="release", position="run:r1_queue.py C",
                       at=t1, method="executed", receipt_id=rid12,
                       statement="일꾼 하나가 get 뒤 task_done 없이 죽으면 join이 1초 안에 끝나지 않는다(남은 미완료 1)", project=p)
    out["same_sentence_across_editions"] = L.obs(q1)["quote_fp"] == L.obs(q1b)["quote_fp"]
    out["same_semaphore_sentence"] = L.obs(s1)["quote_fp"] == L.obs(s1b)["quote_fp"]
    out["opens_rev2"] = L.opens.get(p, 0) - before
    out["reuse_313_for_312"] = reuse_313
    for code in ("H1", "H2", "H3"):
        L.judge(p, req2, code, ea2, "Y", "direct", "L4", "3.12 영수증 A와 L24–26(3.13과 같은 문장)", t1, premises=prem_q)
    L.judge(p, req2, "S1", q2b, "N", "direct", "L2", "3.12에는 shutdown 없음", t1, premises={"runtime": "CPython 3.12"})
    L.judge(p, req2, "S1", ea2, "Y", "direct", "L4", "끝 표지 None x 4로 끝남", t1, premises={"runtime": "CPython 3.12"})
    slot_direct2 = dict(slot_direct, first=q1b, support=[q2b, ea2], flip=[q1b],
                        verb="투입·완료 신호를 따로 만들 필요가 없습니다. 크기 상한 8인 대기열에 일꾼 4개를 고정해 붙이고, 입력이 끝나면 일꾼 수만큼 끝 표지(None)를 넣습니다",
                        where="CPython v3.12.3 Lib/asyncio/queues.py L24–26 (shutdown은 3.12에 없음)",
                        reason="대기 8·처리 중 4(H1), 작업 객체 4개(H2), get으로 자리가 날 때만 재개(H3). 3.12 실행에서도 대기 최대 8, 처리 중 최대 4",
                        hold="런타임을 3.13 이상으로 올리면 끝 표지 대신 shutdown을 씁니다. 일꾼을 항목마다 만들게 되면 이 자리를 철회합니다")
    L.judge(p, req2, "H2", ed2, "Y", "transplant", "L4", "3.12에서도 허가를 먼저 얻으면 producer가 기다림", t1,
            premises={"producer_pausable": "yes"})
    swap = {s1: s1b, ec: ec2}
    folded2 = [dict(f, url=L.link(swap[f["obs"]]), obs=swap[f["obs"]]) if f.get("obs") in swap else f for f in folded]
    run2 = L.compose(p, req2, t1, slots=[slot_direct2], folded=folded2, readback=readback,
                     budget={"opens": out["opens_rev2"]})
    L.note(p, run1, 1, q2, q2b, "changes_value", t1,
           "요청판 2: 배포 런타임이 3.12로 바뀌어 끝 신호 부분(shutdown)이 성립하지 않는다. 대기열·일꾼 부분은 같은 문장이라 유지.")
    out["run2"] = L.replay(p, run2)
    out["run1_after"] = L.replay(p, run1)

    # ---- 다른 프로젝트 C가 같은 판(3.13)에서 비슷한 일을 묻는다 ----
    pc = L.project("C")
    t2 = "2026-12-12T01:00:00Z"
    reqc = L.intake(pc, request_key="RC", rev=1, at=t2,
                    text="로그 묶음을 느린 디스크에 쓸 때 메모리에 쌓이지 않게 하고 싶다. Python 3.13 asyncio.",
                    selected_part="로그 수집기: 디스크 쓰기 단계", requirements=[
                        {"code": "C1", "kind": "must", "text": "대기 묶음 수 상한"},
                        {"code": "C2", "kind": "must", "text": "쓰기가 느리면 수집 쪽이 기다린다"}],
                    context={"runtime": {"value": "CPython 3.13", "provenance": "studio"}},
                    prior={"state": "none", "known": []},
                    needs=[{"slot": "output", "lang": "en",
                            "text": "the collector blocks when the queue is full until the writer removes an item"},
                           {"slot": "keeps", "lang": "en", "text": "a bounded queue so batches never pile up beyond a limit"}])
    hc = L.search_drawer(pc, reqc, t2, k=5)
    out["project_c_drawer"] = [(h["obs_id"], h["slots"], h["matched"]) for h in hc if h["eligible"]]
    before_c = L.opens.get(pc, 0)
    reuse = L.reusable(CPY_QUEUES, "v3.13.18", "L36–38", project=pc)
    out["project_c_gate"] = L.reuse_gate(reuse, t2) if reuse else None
    if reuse:
        # 같은 판·같은 위치: 다시 읽지 않고 뒤집을 위치(세 줄)만 대조한다. 지문이 같으면 sighting만 남는다.
        L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="L36–38", at=t2,
                  method="read_line", quote=Q313_BOUNDED, quote_lang="en",
                  statement=L.obs(reuse)["statement"], flip_position=L.obs(reuse)["flip_position"], project=pc)
        first = reuse
    else:
        first, _ = L.observe(url=CPY_QUEUES, edition_key="v3.13.18", edition_kind="release", position="L36–38",
                             at=t2, method="read_line", quote=Q313_BOUNDED + " ", quote_lang="en",
                             statement="크기 상한이 양수면 가득 찬 대기열에 put을 await한 쪽은 기다린다.", project=pc)
    out["project_c_reused"] = bool(reuse)
    out["project_c_full_opens"] = L.opens.get(pc, 0) - before_c
    out["project_c_sees_A_slips"] = len(L.inherited(pc, first))

    # ---- 자료집에 답이 없을 때: 같은 요청을 대기열 원문이 서랍에도 새 검색에도 없는 상태로 돌린다 ----
    # [고정 자료] 새 검색 직접 갈래가 동기화 절만 돌려주고, 서랍은 대기열 관측을 갖지 않는다고 둔 변형이다.
    pn = L.project("A_none")
    reqn = L.intake(pn, request_key="R1", rev=1, at=t0, text=q["ko"], selected_part="파이프라인: 작업 투입·완료 신호",
                    requirements=reqs, context=ctx, prior={"state": "none", "known": []}, needs=R1_NEEDS)
    L.interpret(pn, reqn, "처리 중 4", "동시에 실행 중인 작업 수", "일꾼 수", d, t0)
    L.search_fresh(pn, reqn, t0, {
        "direct": [{"url": "https://docs.python.org/3.13/library/asyncio-sync.html", "why": "semaphore"}],
        "relation": [{"url": "https://pypi.org/pypi/aiolimiter/1.3.0/json", "why": "limit rate asyncio"}],
        "domain_guess": [{"url": "https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.4/README.md",
                          "why": "backpressure demand"},
                         {"url": "https://global.toyota/en/company/vision-and-philosophy/production-system/",
                          "why": "pull production kanban"}],
        "language": []})
    folded_none = [f for f in folded if f["obs"] != ec]   # 대기열 join 시험은 대기열이 없으니 뺀다
    run_none = L.compose(pn, reqn, t0, slots=[], folded=folded_none, status="none_verified", readback=readback,
                         next_action=("검증된 생략 후보가 없습니다. 가장 가까운 것은 접힌 2번(허가를 작업 생성보다 먼저 얻기)이고, "
                                      "대기 8(H1)을 따로 세야 합니다. 첫 확인 항목은 길이 상한이 있고 가득 차면 넣는 쪽을 "
                                      "기다리게 하는 표준 라이브러리 대기열 절(H1·H2를 한 번에)입니다."))
    out["no_answer"] = L.replay(pn, run_none)
    return out


# =====================================================================================
# 사례 B: EVAL-X1 (평가 스레드가 afa3c285에 봉인)
# =====================================================================================
X1_TEXT = ("개인 지식관리 웹앱. 웹 클리퍼 → 저장 목록 → 전문 검색 → 공유 페이지. 선택한 부분: 저장 목록 계층. "
           "목적: 저장 목록을 직접 만들고 운영하지 않고 이미 있는 서비스나 부품으로 대신하고 싶다. "
           "R1 저장한 링크·태그·저장일을 언제든 공개 형식으로 내보낼 수 있어야 한다. "
           "R2 외부 서비스가 종료를 발표해도 사용자 목록 전체의 사본이 우리 쪽에 남아 종료 후 30일 동안 조회할 수 있어야 한다. "
           "R3 클리퍼 → 저장 → 검색 순서 유지, 검색 계층은 저장 계층의 추가·삭제를 받아야 한다.")
X1_NEEDS = [
    {"slot": "input", "lang": "en", "text": "saved links with tags and saved dates arriving from a web clipper"},
    {"slot": "output", "lang": "en", "text": "an export in an open format and a stream of additions and deletions for search"},
    {"slot": "keeps", "lang": "en",
     "text": "a full copy on our side stays readable for thirty days after the outside service shuts down"},
    {"slot": "summary", "lang": "en",
     "text": "keep our own copy of records held by an outside service in sync with additions and deletions"},
]


def case_b(L: Ledger) -> dict:
    out = {}
    p = L.project("X")
    t0 = "2025-05-15T00:00:00Z"
    reqs = [
        {"code": "R1", "kind": "must", "text": "사용자가 저장한 링크·태그·저장일을 언제든 공개 형식으로 내보낼 수 있어야 한다."},
        {"code": "R2", "kind": "must", "text": "외부 서비스가 종료를 발표해도 사용자 목록 전체의 사본이 우리 쪽에 남아, 종료 후 30일 동안 사용자가 조회할 수 있어야 한다."},
        {"code": "R3", "kind": "must", "text": "클리퍼 → 저장 → 검색 순서는 유지한다. 검색 계층은 저장 계층의 추가·삭제를 받아야 한다."},
        {"code": "P1", "kind": "prefer", "text": "무료 또는 소규모 비용, 읽기 API 제공."},
        {"code": "X", "kind": "out_of_scope", "text": "클리퍼 화면, 전문 검색 엔진 선택, 읽기 화면."},
    ]
    req = L.intake(p, request_key="X1", rev=1, at=t0, text=X1_TEXT, selected_part="저장 목록 계층",
                   requirements=reqs, context={"users": {"value": "unknown", "provenance": "explicit"}},
                   prior={"known": []}, needs=X1_NEEDS)
    # T0-c: R1의 두 해석(서비스 화면 내보내기 / 읽기 API 가져오기). 첫 절이 다르다.
    # 0단계 요청판 재독: R2(우리 쪽 사본)·R3(추가·삭제 전달)·선호(읽기 API) 칸이 '가져오기'를 정한다 → 고르고 첫 줄에 밝힌다.
    d = L.decide("서비스의 내보내기 도움말 절", "서비스의 읽기 API 절", fields_settle=True)
    L.interpret(p, req, "R1-언제든", "우리 앱이 읽기 API로 가져온다", "사용자가 서비스 화면에서 내보낸다", d, t0)
    out["clarify_T0c"] = d
    out["drawer_t0"] = len([h for h in L.search_drawer(p, req, t0) if h["eligible"]])
    L.search_fresh(p, req, t0, {
        "direct": [{"url": POCKET_HOME, "why": "read later save links tags export"}],
        "relation": [], "language": [],
        "domain_guess": [{"url": OAI_URL, "why": "harvest incremental deleted records"},
                         {"url": RFC8493_URL, "why": "preservation package manifest"}],
    })
    pocket0, _ = L.observe(url=POCKET_HOME, edition_key="fetch:2025-05-15", edition_kind="fetch",
                           position="검색 결과 항목", at=t0, method="intro_only",
                           statement="검색 결과에서 이름과 주소만 확인했다. 내보내기·API 원문은 아직 열지 않았다.", project=p)
    oai, _ = L.observe(url=OAI_URL, edition_key="2.0 (doc 2015-01-08)", edition_kind="release", position="§2.5.1",
                       at=t0, method="read_line", quote=OAI_PERSISTENT + " " + OAI_NO, quote_lang="en",
                       published_at="2015-01-08",
                       statement="저장소가 삭제 정보를 기한 없이 보존하는 수준(persistent)과 보존하지 않는 수준(no)을 구분한다.",
                       flip_position="§2.5.1 deletedRecord 세 수준의 정의", project=p,
                       evidence_ref="인용은 2026-11-26 열람본(문서판 2015-01-08). 출처 행: " + LEDGER_152 + "OP-OAI")
    oai2, _ = L.observe(url=OAI_URL, edition_key="2.0 (doc 2015-01-08)", edition_kind="release", position="§2.7.1",
                        at=t0, method="read_line", quote=OAI_INCLUSIVE, quote_lang="en", published_at="2015-01-08",
                        statement="선택 수확의 날짜 범위는 양 끝을 포함한다. 마지막 수확 시각부터 다시 물어도 빠지는 기록이 없다.",
                        project=p)
    L.tag(oai, "input", "concrete", "en", "records held by a repository with datestamps and deletion markers")
    L.tag(oai, "output", "concrete", "en", "a harvester keeps its own copy up to date by asking only for changes since a date")
    L.tag(oai, "keeps", "concrete", "en", "information about deleted records kept with no time limit when support is persistent")
    L.tag(oai, "breaks_when", "concrete", "en", "the repository does not maintain deletions, so removed records stay in the copy")
    L.tag(oai, "summary", "one_up", "en",
          "keep a separate copy of another service's records in sync, including deletions, by incremental harvesting")
    L.tag(oai, "summary", "one_up", "ko", "다른 서비스가 가진 기록의 사본을 삭제까지 포함해 변경분만 받아 맞춰 둔다")
    g = L.gate(role_map=[("수확기", "우리 앱"), ("저장소", "외부 저장 서비스"), ("삭제 기록", "지운 북마크"),
                         ("날짜 범위", "마지막으로 받은 시각")],
               invariant_quote=OAI_PERSISTENT,
               break_input="서비스가 종료를 공지한 뒤 기한을 바꾸고 내보내기와 API를 닫는다",
               baseline_prediction="공지 뒤 일괄 내보내기가 닫히기 전에 끝나야만 R2가 성립한다",
               principle_prediction="사본이 늘 맞춰져 있으므로 내보내기가 닫혀도 R2가 성립한다",
               target_doc_states_it=False)
    out["gate_x1"] = g
    L.judge(p, req, "R2", oai, "U", "principle", "L2", "원리 관문 통과. 대상 서비스의 변경·삭제 제공은 미확인", t0)
    L.judge(p, req, "R1", pocket0, "U", "direct", "L0", "원문 미판독", t0)
    slots = [
        {"kind": "check", "first": pocket0, "ladder": "L0", "hold": "원문 판독 전에는 지지로 내지 않습니다",
         "verb": "Pocket(직접 쓸 도구 후보, 검증 전)",
         "reason": "읽기 API로 가져오는 해석이면 API 문서의 '변경 이후 목록'과 삭제 신호를, 화면 내보내기 해석이면 내보내기 도움말의 형식과 범위를 먼저 확인합니다"},
        {"kind": "principle", "first": oai, "support": [oai2], "flip": [oai], "contrast": [pocket0], "ladder": "L2",
         "verb": "다른 서비스의 기록을 삭제까지 포함해 변경분만 받아 우리 쪽 사본을 늘 맞춰 둔다(학술 기록 수확 규약)",
         "where": "OAI-PMH 2.0 §2.5.1, §2.7.1",
         "borrow": "마지막으로 받은 시각부터 양 끝을 포함해 다시 묻는 증분 수확, 삭제 기록을 따로 받는 것",
         "recheck": "대상 서비스가 변경 이후 목록과 삭제 신호를 주는지, 호출 한도, 이어읽기 표지의 만료",
         "break": "서비스가 종료 공지 뒤 내보내기와 API를 닫는 경우. 공지 뒤 일괄 내보내기(동종 기준선)는 닫히기 전에 끝나야만 R2가 성립하지만, 늘 맞춘 사본은 그와 무관하다",
         "hold": "대상 서비스가 삭제 정보를 주지 않으면 주기적 전체 내보내기와 차분으로 바꿉니다. R2는 외부 서비스 하나의 기능이 아니라 우리 쪽 사본의 성질입니다"},
    ]
    # BagIt(RFC 8493): 새 검색 분야 추정 갈래에서 왔다. 관문 ①이 반만 맞고 ③에서 흔한 백업 관행과 예측이 같아 닫힌다.
    gb = L.gate(role_map=[("보내는 쪽", "외부 서비스(목록과 지문을 만들지 않음)")], invariant_quote=RFC8493_VALID,
                break_input="보관 중 사본이 손상된다",
                baseline_prediction="지문을 다시 계산해 손상을 찾는다",   # 흔한 백업 관행
                principle_prediction="지문을 다시 계산해 손상을 찾는다",  # 보존 묶음
                target_doc_states_it=False)
    out["gate_bagit"] = gb
    folded0 = [{"url": RFC8493_URL, "condition": "원리 관문",
                "reason": "; ".join(gb["failed"]) + ". 외부 서비스가 목록과 지문을 만들지 않아 역할 짝이 반만 맞는다. "
                          "R2 범위의 시험 하나로 접는다: 받은 사본의 항목 수를 서비스 화면과 맞추고 보관 중 지문을 다시 계산한다"}]
    run0 = L.compose(p, req, t0, slots=slots, folded=folded0, status="partial", readback=(
        "'언제든 내보내기'를 우리 앱이 읽기 API로 가져오는 뜻으로 읽었습니다. 사용자가 서비스 화면에서 내보내는 뜻이면 1번의 두 번째 확인을 먼저 보세요."),
        next_action="Pocket 읽기 API 문서를 열어 '변경 이후 목록'과 삭제 신호가 있는지 확인한다.")
    L.show(p, run0, 1, t0)   # 봉인(prior)이 먼저 있으므로 노출을 쓸 수 있다
    out["run0"] = L.replay(p, run0)
    L.channel("mozilla", MOZ_FEED, "feed")
    L.watch(pocket0, MOZ_FEED, "Pocket", layer="supplier")

    # ---- E1~E5: 채널 차분·공지 기한 → 재확인 → 대체 → 알림 ----
    # 원문이 공지한 기한(원장 판독에서 읽은 값). 새 관측에 감시를 달 때 기한도 단다.
    deadline_of = {"297191": "2025-07-08T00:00:00Z", "300072": "2025-10-08T00:00:00Z",
                   "308355": "2025-11-06T00:00:00Z", "308427": "2025-11-12T00:00:00Z"}
    out["events"] = []
    prev = pocket0
    listing = []
    for ext, seen, key, eff, src, reading, effect in POCKET_EVENTS:
        if ext == "297191":
            new = L.poll(MOZ_FEED, [{"id": "building-whats-next", "title": "Building what's next",
                                     "summary": "Pocket: 신규 다운로드 중단, 7월 8일 서비스 종료, 10월 8일 내보내기 예정",
                                     "url": MOZ_BLOG}], seen)
        else:
            listing.append({"id": ext, "title": f"future-of-pocket revision {ext}", "url": KB, "edition": key})
            # 채널 목록 전체를 다시 받아도 이미 본 ID는 새 항목이 아니다(표시일 창 없음)
            new = L.poll(KB_HISTORY, list(reversed(listing)), seen)
        L.due(seen)   # 같은 관측의 기한 작업은 채널 작업에 합쳐진다
        jobs = L.jobs()
        merged = [j["merged_causes"] for j in jobs if j["merged_causes"]]
        for j in jobs:
            assert L.lease(j["job_id"], seen.replace("00:00:00", "06:00:00"))
            o, _ = L.observe(url=KB, edition_key=key, edition_kind="revision", position="When is Pocket shutting down / dates",
                             at=seen, method="read_line", quote=reading, quote_lang="ko-reading", published_at=eff,
                             statement=reading, flip_position="기한과 가용 범위 문장", via="channel",
                             evidence_ref=LEDGER_152 + src)
            L.supersede(prev, o, effect, known_from=seen, effective_from=eff)
            L.finish(j["job_id"], o)
            if ext == "297191":
                L.channel("mozilla", KB_HISTORY, "revision_history")
                listing.append({"id": ext, "title": f"future-of-pocket revision {ext}", "url": KB, "edition": key})
                L.poll(KB_HISTORY, list(listing), seen)   # 기준선 등록. 이미 읽은 판이라 작업을 만들지 않게 감시는 뒤에 단다
            L.watch(o, KB_HISTORY, deadline=deadline_of.get(ext))
            prev = o
        notes = L.propagate(p, seen)
        if ext == "300072":
            L.judge(p, req, "R3", prev, "N", "direct", "L2", "7월 8일 저장 종료", seen, cause="channel")
        if ext == "313551":
            L.judge(p, req, "R1", prev, "N", "direct", "L2", "내보내기·API 비활성화", seen, cause="channel")
            L.judge(p, req, "R2", prev, "N", "direct", "L2", "내보내기·API 비활성화", seen, cause="channel")
        out["events"].append({"id": ext, "new_items": len(new), "jobs": len(jobs), "merged": merged,
                              "notices": [(n["slot"], n["effect"]) for n in notes]})
    # E-a: 그날 알던 기한
    out["known_2025_10_09"] = L.known_on(KB, "2025-10-09T12:00:00Z")["statement"]
    out["known_2025_10_10"] = L.known_on(KB, "2025-10-10T12:00:00Z")["statement"]
    # T1-b·T2: 지난 답 재생, 새 답
    t2 = "2025-11-13T01:00:00Z"
    out["run0_replay_T2"] = L.replay(p, run0, at=t2)
    out["run0_slots_unchanged"] = [s["sentence"] for s in out["run0_replay_T2"]["slots"]] == \
                                  [s["sentence"] for s in out["run0"]["slots"]]
    run2 = L.compose(p, req, t2, slots=[slots[1]], status="none_verified", readback=None, next_action=(
        "검증된 대체 서비스가 자료집에 없습니다. 후보를 찾을 때 첫 확인 항목은 (1) 읽기 API의 '변경 이후 목록'과 삭제 신호, "
        "(2) 공개 형식 전체 내보내기 보증입니다. 그 전까지 R2는 1번 원리(우리 쪽 사본)로만 지킬 수 있습니다."))
    out["run2"] = L.replay(p, run2)
    out["principle_notices"] = [n for n in out["run0_replay_T2"]["notices"] if n["slot"] == 2]

    # ---- T3: 몇 달 뒤 다른 프로젝트, 다른 이름의 질문 ----
    w = L.project("W")
    t3 = "2026-03-01T00:00:00Z"
    reqw = L.intake(w, request_key="W1", rev=1, at=t3,
                    text="연구실 위키의 '참고문헌 북마크' 부분을 외부 서비스에 맡기고 싶다. 서비스가 문을 닫아도 북마크가 우리 서버에 남아야 한다. 화면은 범위 밖.",
                    selected_part="참고문헌 북마크", requirements=[
                        {"code": "W1", "kind": "must", "text": "서비스가 문을 닫아도 북마크가 우리 서버에 남는다"}],
                    prior={"state": "none", "known": []},
                    needs=[{"slot": "summary", "lang": "en",
                            "text": "keep our own copy of bookmarks held by an outside service so the copy remains if the service closes"},
                           {"slot": "output", "lang": "en", "text": "a copy of every bookmark kept on our own server"}])
    dw = L.decide("우리 쪽 사본을 맞추는 원리의 절", "우리 쪽 사본을 맞추는 원리의 절")
    L.interpret(w, reqw, "W1-남는다", "외부 서비스와 따로 우리 서버에 북마크 전체 사본을 둔다", None, dw, t3)
    hw = L.search_drawer(w, reqw, t3, k=5)
    out["t3_drawer"] = [(L.obs(h["obs_id"])["url"], h["slots"], h["matched"]) for h in hw if h["eligible"]]
    L.search_fresh(w, reqw, t3, {"direct": [], "relation": [], "domain_guess": [], "language": []})  # [고정 자료] 미지
    out["t3_path_log"] = L.path_log(w, reqw)
    # 판단을 새로 쓰기 전, W 장부에 보이는 판단 쪽지 수(X의 쪽지가 흘러들었다면 0이 아니다)
    out["t3_sees_X_slips"] = L.db.execute(f"SELECT count(*) FROM {w}.slip").fetchone()[0]
    t3_slots = []
    if any(h["obs_id"] == oai and h["eligible"] for h in hw):
        # 관측은 재사용하되 판단은 W에서 새로 한다. 감시가 없으므로 뒤집을 위치만 다시 대조한다(같은 문장이면 sighting).
        out["t3_reuse_gate"] = L.reuse_gate(oai, t3)
        L.observe(url=OAI_URL, edition_key="2.0 (doc 2015-01-08)", edition_kind="release", position="§2.5.1",
                  at=t3, method="read_line", quote=OAI_PERSISTENT + " " + OAI_NO, quote_lang="en",
                  published_at="2015-01-08", statement=L.obs(oai)["statement"], project=w)
        out["t3_gate"] = L.gate(role_map=[("수확기", "우리 위키 서버"), ("저장소", "외부 북마크 서비스"),
                                          ("삭제 기록", "지운 북마크")],
                                invariant_quote=OAI_PERSISTENT, break_input="서비스가 문을 닫는다",
                                baseline_prediction="닫기 전에 일괄 내보내기를 끝내야만 W1이 성립한다",
                                principle_prediction="늘 맞춘 사본이 있으므로 닫혀도 W1이 성립한다",
                                target_doc_states_it=False)
        L.judge(w, reqw, "W1", oai, "U", "principle", "L2", "원리 관문 통과(이 프로젝트에서 새로 판단). 맡길 서비스의 변경·삭제 제공은 미확인", t3)
        t3_slots.append({
            "kind": "principle", "first": oai, "support": [oai2], "flip": [oai], "ladder": "L2",
            "verb": "외부 서비스가 가진 북마크의 사본을 삭제까지 포함해 변경분만 받아 우리 서버에 늘 맞춰 둔다(학술 기록 수확 규약)",
            "where": "OAI-PMH 2.0 §2.5.1, §2.7.1",
            "borrow": "마지막으로 받은 시각부터 양 끝을 포함해 다시 묻는 증분 수확, 삭제 기록을 따로 받는 것",
            "recheck": "맡길 북마크 서비스가 변경 이후 목록과 삭제 신호를 주는지, 호출 한도, 이어읽기 표지의 만료",
            "break": "서비스가 문을 닫는 경우. 닫기 전 일괄 내보내기(동종 기준선)는 그 창 안에 끝내야만 W1이 성립하지만, 늘 맞춘 사본은 그와 무관하다",
            "hold": "맡길 서비스가 삭제 정보를 주지 않으면 주기적 전체 내보내기와 차분으로 바꿉니다"})
    run_w = L.compose(w, reqw, t3, slots=t3_slots, status="partial" if t3_slots else "none_verified",
                      readback="'우리 서버에 남는다'를 외부 서비스와 따로 우리 서버에 북마크 전체 사본을 둔다는 뜻으로 읽었습니다.",
                      next_action="맡길 북마크 서비스 후보는 이번 탐색에서 찾지 못했습니다. 후보마다 첫 확인 항목은 "
                                  "(1) 변경 이후 목록과 삭제 신호, (2) 공개 형식 전체 내보내기입니다.")
    out["t3_run"] = L.replay(w, run_w)
    out["t3_inherited"] = len(L.inherited(w, oai))
    return out


# =====================================================================================
# 장면 2: R2 (ii-svn-log를 수집한 날과 몇 달 뒤의 다른 질문)
# =====================================================================================
def case_r2(L: Ledger) -> dict:
    out = {}
    tc = "2026-11-26T03:00:00Z"
    # 수집 흐름(窓の杜 2025-11-13 다이제스트)에서 이미 읽은 한 줄을 청구 없는 관측으로 남긴다. 추가 열람 없음.
    ii, _ = L.observe(url=II_SVN, edition_key="fetch:2026-11-25", edition_kind="fetch", position="author post/release body",
                      at=tc, method="intro_only", quote=None, published_at="2025-11-11", via="collection",
                      statement=II_SVN_READING,
                      evidence_ref="AF-RES-149@bc19a446 sources.jsonl L56 S-A-W1-1 (경로 L51 L10 다이제스트)")
    L.tag(ii, "input", "concrete", "en", "a Subversion repository URL and its commit history", written_from="maker_statement")
    L.tag(ii, "output", "concrete", "en", "the commit history exported to one Excel file", written_from="maker_statement")
    L.tag(ii, "user_without", "concrete", "en", "people on a PC without Subversion can view and share the history",
          audience="SVN 없는 PC에서 열람·공유", written_from="maker_statement")
    L.tag(ii, "summary", "one_up", "en",
          "export a tool's history into one common standalone file that can be viewed and shared on a PC without that tool",
          written_from="maker_statement")
    L.tag(ii, "summary", "one_up", "ko", "도구가 만든 이력을 그 도구가 없는 PC에서도 보고 나눌 수 있는 흔한 파일 하나로 내보낸다",
          written_from="maker_statement")
    out["collection_opens"] = 0
    bag, _ = L.observe(url=RFC8493_URL, edition_key="RFC 8493 (2018-10)", edition_kind="doi", position="§2.1.3, §1.3",
                       at="2026-11-25T01:08:10Z", method="read_line", quote=RFC8493_MANIFEST + " " + RFC8493_VALID,
                       quote_lang="en", published_at="2018-10", via="request",
                       statement="모든 내용 파일을 지문과 함께 목록에 한 번씩 적고, 받은 쪽은 빠진 파일이 없는지(완전)와 모든 지문이 맞는지(유효)를 따로 확인한다.",
                       flip_position="§1.3 complete/valid 정의, §2.1.3 manifest 규칙",
                       evidence_ref="AF-RES-263@d996a675 sources.jsonl B01; 인용은 2026-11-26 열람")
    L.tag(bag, "output", "concrete", "en", "a bag folder with a payload manifest listing every file with a checksum")
    L.tag(bag, "keeps", "concrete", "en", "a receiver can verify every file is present and every checksum matches")
    L.tag(bag, "summary", "one_up", "en", "package files with a checksum list so a receiver can verify nothing changed or went missing")

    p = L.project("B")
    t = "2027-03-02T00:00:00Z"
    text = ("AI 작업 기록을 우리 도구를 설치하지 않은 외부 감리자에게 넘기고 싶다. 감리자는 인터넷이 막힌 PC에서 보고, "
            "넘긴 뒤에는 기록이 바뀌면 안 된다. 대상 부분: 작업 기록 내보내기.")
    req = L.intake(p, request_key="R2", rev=1, at=t, text=text, selected_part="작업 기록 내보내기", requirements=[
        {"code": "B1", "kind": "must", "text": "우리 도구를 설치하지 않은 감리자가 본다"},
        {"code": "B2", "kind": "must", "text": "인터넷이 막힌 PC에서 본다"},
        {"code": "B3", "kind": "must", "text": "넘긴 뒤에는 기록이 바뀌면 안 된다"}],
        prior={"state": "none", "known": []},
        needs=[{"slot": "input", "lang": "en", "text": "work records produced by our tool"},
               {"slot": "output", "lang": "en", "text": "the records exported as one standalone file the receiver can open"},
               {"slot": "user_without", "lang": "en", "text": "an auditor on a PC without our tool and without internet access"},
               {"slot": "keeps", "lang": "en", "text": "the handed over files stay unchanged or the receiver can verify any change"}])
    # 1단계 공통 행동: 읽기 전용으로 넘기고 지문 목록을 따로 보관·전달하면 '고칠 수 없게'와 '고치면 알아채게'를 함께 채운다.
    # 남의 PC에 있는 파일은 형식만으로 고치지 못하게 막을 수 없으므로, 막기 해석이 요구하는 것도 결국 검출이다.
    d = L.decide("변경을 막는 형식의 첫 절", "변경을 검출하는 지문 목록의 첫 절", common_action=True, irreversible=True)
    L.interpret(p, req, "B3-불변", "읽기 전용으로 넘기고 바뀌면 지문 목록으로 알아챈다", "변경 자체를 막아야 한다", d, t)
    out["clarify"] = d
    hits = L.search_drawer(p, req, t, k=5)
    out["drawer"] = [(L.obs(h["obs_id"])["url"], h["slots"], h["matched"]) for h in hits if h["eligible"]]
    L.search_fresh(p, req, t, {"direct": [], "relation": [],
                               "domain_guess": [{"url": RFC8493_URL, "why": "digital preservation package checksum"}],
                               "language": []})   # [고정 자료] 일본어 개인 글은 새 검색에 오지 않는다고 가정
    out["path_log"] = L.path_log(p, req)
    L.judge(p, req, "B3", bag, "Y", "transplant", "L2", "검출 해석에서 지문 목록이 맡는다", t)
    L.judge(p, req, "B1", ii, "U", "transplant", "L1", "제작자 소개문만 봄. 받는 쪽 일반 프로그램으로 열림", t)
    L.judge(p, req, "B3", ii, "N", "reference", "L1", "표 파일은 받은 사람이 고칠 수 있다", t)
    slots = [
        {"kind": "transplant", "first": bag, "ladder": "L2", "verb": "보존 묶음(파일 목록+파일별 지문)으로 넘긴다",
         "where": "RFC 8493 §1.3, §2.1.3", "reason": "지키는 것(넘긴 뒤 변경 검출)",
         "with": "원격 가져오기 목록을 쓰지 않고 내용을 실제로 담는다. 지문 요약은 다른 경로로도 함께 넘긴다",
         "hold": "감리자 PC에서 설치 없이 지문을 확인할 수 없으면 이 자리는 보조로 내려가고 그때 한 번 묻습니다"},
    ]
    if any(h["obs_id"] == ii and h["eligible"] for h in hits):
        slots.append({"kind": "check", "first": ii, "ladder": "L1",
                      "verb": "도구가 만든 기록을 그 도구가 없는 PC에서 열리는 흔한 파일 하나로 내보내는 부분(일본어 개인 도구 ii-svn-log, 2025-11-11 제작자 글)",
                      "reason": "제작자 글의 출력 절에서 무엇을 어떤 파일로 내는지(B1·B2를 채우는 부분)",
                      "with": "입력은 SVN 이력뿐이라 도구 자체는 못 쓴다. 불변(B3)은 1번이 맡는다",
                      "hold": "소개만 보았습니다. 표 파일은 받은 사람이 고칠 수 있으므로 불변 근거로 쓰지 않습니다"})
    run = L.compose(p, req, t, slots=slots, status="partial", readback=(
        "'넘긴 뒤 바뀌면 안 된다'를 두 뜻(고칠 수 없게, 고치면 알아채게) 모두로 읽었습니다. 남의 PC에 있는 파일은 형식만으로 "
        "고치지 못하게 막을 수 없으므로, 읽기 전용으로 넘기고 지문 목록을 따로 보관·전달해 두 뜻을 함께 채웁니다. "
        "감리자 PC에서 설치 없이 지문을 확인할 수단이 없으면 그때 한 번 묻겠습니다."),
        next_action="2번 제작자 글의 출력 절을 연다(원문 1회). 다음 확인: 감리자 PC의 기본 지문 확인 수단.")
    out["run"] = L.replay(p, run)
    out["ii_svn_in_answer"] = any(ii in s["cites"] for s in out["run"]["slots"])
    return out


# =====================================================================================
# 전체 재생과 구성요소 삭제 시험
# =====================================================================================
def run_all(features: dict | None = None) -> dict:
    L = Ledger(features=features)
    catalog = preload_catalog(L)
    try:
        return {"A": case_a(L, catalog), "B": case_b(L), "R2": case_r2(L), "counts": L.counts()}
    finally:
        L.db.close()


def ablation() -> list[dict]:
    base = run_all()
    rows = []
    for name, feats in [("기준(전부 켬)", {}), ("서랍 끔", {"drawer": False}), ("사용 쪽지 끔", {"usage": False}),
                        ("판단 분리 끔", {"split": False})]:
        r = run_all(feats) if feats else base
        rows.append({
            "variant": name,
            "A_first_link_same": r["A"]["run1"]["slots"][1]["sentence"] == base["A"]["run1"]["slots"][1]["sentence"],
            "A_projectC_full_opens": r["A"]["project_c_full_opens"],
            "B_T2_answer_same": [x["sentence"] for x in r["B"]["run2"]["slots"]] ==
                                [x["sentence"] for x in base["B"]["run2"]["slots"]],
            "B_notices_total": sum(len(e["notices"]) for e in r["B"]["events"]),
            "recheck_jobs": r["counts"]["recheck_jobs"],
            "B_principle_false_notices": len(r["B"]["principle_notices"]),
            "B_T3_principle_found": any(OAI_URL == u for u, _, _ in r["B"]["t3_drawer"]),
            "B_T3_inherited_judgments": r["B"]["t3_inherited"],
            "R2_foreign_precedent": r["R2"]["ii_svn_in_answer"],
            "B_known_2025_10_09": r["B"]["known_2025_10_09"],
            "B_T0_replay_unchanged": r["B"]["run0_slots_unchanged"],
        })
    return rows


if __name__ == "__main__":
    res = run_all()
    if "--json" in sys.argv:
        res["ablation"] = ablation()
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    else:
        a, b, r2 = res["A"], res["B"], res["R2"]
        print("A drawer:", a["drawer"][:6])
        print("A audit accidents:", a["drawer_audit_accidents"][:6])
        print("A toyota (with function words):", a["drawer_audit_toyota"], "content only:", a["drawer_content_toyota"])
        print("A project C drawer:", a["project_c_drawer"])
        print("A gate:", a["gate_r1"], "opens t0:", a["opens_t0"])
        print("A carry:", a["carry"], "same sentence:", a["same_sentence_across_editions"], "opens rev2:", a["opens_rev2"])
        print("A project C reused:", a["project_c_reused"], "full opens:", a["project_c_full_opens"])
        print("B clarify:", b["clarify_T0c"], "gate:", b["gate_x1"])
        print("B events:", b["events"])
        print("B known 10-09:", b["known_2025_10_09"])
        print("B T0 replay unchanged:", b["run0_slots_unchanged"], "principle notices:", b["principle_notices"])
        print("B T3 drawer:", b["t3_drawer"], "path:", b["t3_path_log"], "sees X slips:", b["t3_sees_X_slips"])
        print("R2 clarify:", r2["clarify"], "drawer:", r2["drawer"], "path:", r2["path_log"])
        print("counts:", res["counts"])
        for row in ablation():
            print(row)
