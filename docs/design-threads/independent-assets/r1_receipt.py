"""R1 증거 표본용 작은 실행: 크기 상한 대기열 + 일꾼 넷 vs 근접 오답(세마포어 + 미리 만든 작업)."""
import asyncio, json, sys

N = 40

async def bounded_queue_version():
    q = asyncio.Queue(maxsize=8)
    st = {"max_waiting": 0, "in_flight": 0, "max_in_flight": 0, "puts_that_waited": 0, "done": 0}
    async def worker():
        while True:
            item = await q.get()
            if item is None:
                q.task_done(); return
            st["in_flight"] += 1; st["max_in_flight"] = max(st["max_in_flight"], st["in_flight"])
            await asyncio.sleep(0.001)   # 변환(빠름)
            await asyncio.sleep(0.02)    # 저장(느림)
            st["in_flight"] -= 1; st["done"] += 1
            q.task_done()
    before = len(asyncio.all_tasks())
    workers = [asyncio.create_task(worker()) for _ in range(4)]
    tasks_created = len(asyncio.all_tasks()) - before
    for i in iter(range(N)):           # 멈출 수 있는 lazy 입력
        if q.full():
            st["puts_that_waited"] += 1
        await q.put(i)                 # 가득 차면 get()으로 자리가 날 때까지 기다림
        st["max_waiting"] = max(st["max_waiting"], q.qsize())
    for _ in workers:
        await q.put(None)
    await q.join(); await asyncio.gather(*workers)
    st.pop("in_flight"); st["tasks_created_for_work"] = tasks_created
    return st

async def semaphore_all_tasks_version():
    sem = asyncio.Semaphore(4)
    st = {"in_flight": 0, "max_in_flight": 0, "done": 0}
    async def job(i):
        async with sem:
            st["in_flight"] += 1; st["max_in_flight"] = max(st["max_in_flight"], st["in_flight"])
            await asyncio.sleep(0.001); await asyncio.sleep(0.02)
            st["in_flight"] -= 1; st["done"] += 1
    before = len(asyncio.all_tasks())
    tasks = [asyncio.create_task(job(i)) for i in range(N)]   # 모든 입력의 작업을 미리 만듦
    st["tasks_created_for_work"] = len(asyncio.all_tasks()) - before
    await asyncio.gather(*tasks)
    st.pop("in_flight")
    return st

async def main():
    return {"python": sys.version.split()[0], "inputs": N,
            "A_bounded_queue_4_workers": await bounded_queue_version(),
            "B_semaphore_with_all_tasks_precreated": await semaphore_all_tasks_version()}

print(json.dumps(asyncio.run(main()), ensure_ascii=False, indent=2))
