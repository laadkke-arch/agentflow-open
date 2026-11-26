"""R1(AF-RES-012 P03.w) 실행 영수증.

같은 입력(40개 항목, 변환 1ms, 저장 5ms)으로 세 구성을 돌려
대기 항목 수, 처리 중 작업 수, 만든 작업 객체 수, producer가 기다린 횟수를 잰다.

  A  크기 상한 8인 대기열 + 고정 일꾼 4개. 끝 신호는 3.13 이상이면 Queue.shutdown(),
     그보다 낮으면 일꾼 수만큼의 끝 표지(None)를 넣는다.
  B  근접 오답: 동시 실행 수 장치(Semaphore 4) + 입력마다 작업 객체를 미리 만든다.
  C  카드 분실 탐침: A에서 일꾼 하나가 get() 뒤 task_done() 없이 죽으면 join()이 끝나는가.
  D  허가를 작업 생성 전에 얻는 구성: producer가 Semaphore를 먼저 얻고 나서 작업 객체를 만든다.

표준 라이브러리만 쓴다.

제품 단위 1에서 바꾼 것(07 D6c, 08 I5): 요청 수치(항목 수, 대기 상한, 일꾼 수, 시간)를 상수로 박지 않고
표준 입력의 JSON으로 받는다. 그래서 이 프로그램은 공개해도 요청을 드러내지 않고, 지문(sha256)을 공용 장부에 둘 수 있다.
설계 예제 docs/design/final/db/receipts/r1_queue.py와 나머지 동작은 같다.

실행: echo '{"items":40,"maxsize":8,"workers":4,"convert_s":0.001,"save_s":0.005}' | python3 -I r1_queue.py
"""
import asyncio
import json
import sys

_INPUT = json.loads(sys.stdin.read() or "{}") if __name__ == "__main__" else {}
N_ITEMS = int(_INPUT.get("items", 0))
MAXSIZE = int(_INPUT.get("maxsize", 0))
WORKERS = int(_INPUT.get("workers", 0))
CONVERT_S = float(_INPUT.get("convert_s", 0.0))
SAVE_S = float(_INPUT.get("save_s", 0.0))


class Meter:
    def __init__(self):
        self.in_flight = 0
        self.max_in_flight = 0
        self.max_waiting = 0
        self.producer_waits = 0
        self.tasks_created = 0
        self.done = 0

    def enter(self):
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)

    def leave(self):
        self.in_flight -= 1
        self.done += 1


async def work(meter):
    meter.enter()
    try:
        await asyncio.sleep(CONVERT_S)
        await asyncio.sleep(SAVE_S)
    finally:
        meter.leave()


def lazy_inputs():
    for i in range(N_ITEMS):
        yield i


async def pattern_a():
    m = Meter()
    q = asyncio.Queue(maxsize=MAXSIZE)
    has_shutdown = hasattr(q, "shutdown")
    stop_exc = getattr(asyncio, "QueueShutDown", None)

    async def worker():
        while True:
            try:
                item = await q.get()
            except Exception as e:  # QueueShutDown on 3.13+
                if stop_exc is not None and isinstance(e, stop_exc):
                    return
                raise
            if item is None:
                q.task_done()
                return
            await work(m)
            q.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(WORKERS)]
    m.tasks_created += len(workers)
    for item in lazy_inputs():
        if q.full():
            m.producer_waits += 1
        await q.put(item)
        m.max_waiting = max(m.max_waiting, q.qsize())
    await q.join()
    if has_shutdown:
        q.shutdown()
        end_signal = "Queue.shutdown()"
    else:
        for _ in range(WORKERS):
            await q.put(None)
        end_signal = "끝 표지 None x 일꾼 수"
    await asyncio.gather(*workers)
    return {
        "pattern": "A bounded-queue+4-workers",
        "end_signal": end_signal,
        "max_waiting": m.max_waiting,
        "max_in_flight": m.max_in_flight,
        "tasks_created": m.tasks_created,
        "producer_waits": m.producer_waits,
        "done": m.done,
    }


async def pattern_b():
    m = Meter()
    sem = asyncio.Semaphore(WORKERS)

    async def guarded():
        async with sem:
            await work(m)

    tasks = []
    for _ in lazy_inputs():
        tasks.append(asyncio.create_task(guarded()))
        m.tasks_created += 1
    # 미리 만든 작업 객체가 모두 대기 중인 셈이다.
    m.max_waiting = len(tasks) - WORKERS
    await asyncio.gather(*tasks)
    return {
        "pattern": "B semaphore+create-all (near miss)",
        "max_waiting": m.max_waiting,
        "max_in_flight": m.max_in_flight,
        "tasks_created": m.tasks_created,
        "producer_waits": m.producer_waits,
        "done": m.done,
    }


async def pattern_c():
    q = asyncio.Queue(maxsize=MAXSIZE)
    died = {"n": 0}

    async def worker(idx):
        while True:
            item = await q.get()
            if item is None:
                q.task_done()
                return
            if idx == 0 and died["n"] == 0:
                died["n"] = 1
                raise RuntimeError("worker died after get() before task_done()")
            await asyncio.sleep(CONVERT_S + SAVE_S)
            q.task_done()

    workers = [asyncio.create_task(worker(i)) for i in range(WORKERS)]
    for item in lazy_inputs():
        await q.put(item)
    try:
        await asyncio.wait_for(q.join(), timeout=1.0)
        joined = True
    except asyncio.TimeoutError:
        joined = False
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    return {
        "pattern": "C card-loss probe",
        "worker_died": died["n"],
        "join_finished_within_1s": joined,
        "unfinished_after_drain": q._unfinished_tasks,
    }


async def pattern_d():
    m = Meter()
    sem = asyncio.Semaphore(WORKERS)
    alive = {"now": 0, "max": 0}
    tasks = []

    async def run_then_release():
        try:
            await work(m)
        finally:
            alive["now"] -= 1
            sem.release()

    for _ in lazy_inputs():
        if sem.locked():
            m.producer_waits += 1
        await sem.acquire()
        alive["now"] += 1
        alive["max"] = max(alive["max"], alive["now"])
        tasks.append(asyncio.create_task(run_then_release()))
        m.tasks_created += 1
    await asyncio.gather(*tasks)
    return {
        "pattern": "D acquire-before-create",
        "max_waiting": 0,
        "max_in_flight": m.max_in_flight,
        "tasks_created": m.tasks_created,
        "max_alive_tasks": alive["max"],
        "producer_waits": m.producer_waits,
        "done": m.done,
    }


async def main():
    out = {
        "runtime": "CPython " + sys.version.split()[0],
        "input": {"items": N_ITEMS, "maxsize": MAXSIZE, "workers": WORKERS,
                  "convert_s": CONVERT_S, "save_s": SAVE_S},
        "results": [await pattern_a(), await pattern_b(), await pattern_c(), await pattern_d()],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
