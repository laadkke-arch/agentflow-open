"""실행 영수증 러너(06 3.1, 07 D6c).

지정한 Python 판(예: "3.13", "3.12.3")으로 작은 프로그램을 돌려 입력·출력·런타임·프로그램 지문을 낸다.
- 해석기는 PATH와 표준 위치에서 python3.X를 찾는다. 원하는 판을 찾지 못하거나 수정 판까지 정했는데 다르면
  실제로 돈 판을 영수증에 적고 exec_log.note에 그 사실을 남긴다. 판을 꾸며 쓰지 않는다.
- 요청 수치는 프로그램 상수가 아니라 표준 입력 JSON으로 넘긴다. 영수증 본문(입력·출력)은 프로젝트 장부에,
  공용에는 지문만 간다(Ledger.receipt(p=)).
- 실행은 가져오기와 따로 센다(Ledger.executed, exec_log).
- mode="replay"면 fixtures/exec의 기록을 읽는다. 시험은 이 모드로 돌아 특정 해석기가 없어도 된다.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

RUNNER_ID = "py-receipt-runner/1"
SEARCH_DIRS = ("/usr/local/bin", "/usr/bin")


class ReplayMiss(LookupError):
    pass


def find_python(want: str) -> tuple[str | None, str | None]:
    """원하는 판의 해석기 경로와 실제 판. want는 '3.13' 또는 '3.12.3'."""
    minor = ".".join(want.split(".")[:2])
    cands = [shutil.which(f"python{minor}")] + [f"{d}/python{minor}" for d in SEARCH_DIRS]
    for c in cands:
        if c and Path(c).exists():
            v = subprocess.run([c, "-I", "-c", "import platform;print(platform.python_version())"],
                               capture_output=True, text=True, timeout=30).stdout.strip()
            if v:
                return c, v
    return None, None


def edition_for(want: str) -> str | None:
    """런타임 맥락(예: 'CPython 3.13')을 CPython 고정판 태그로. 이 러너가 실제로 돌릴 판의 태그를 고른다(08 I7)."""
    _path, v = find_python(want.split()[-1])
    return f"v{v}" if v else None


class ReceiptRunner:
    def __init__(self, mode: str = "replay", fixtures: str | Path | None = None):
        assert mode in ("live", "record", "replay")
        self.mode, self.dir = mode, Path(fixtures) if fixtures else None

    def _key(self, program_sha: str, inp: dict, want: str) -> str:
        body = json.dumps([program_sha, inp, want], sort_keys=True)
        return hashlib.sha256(body.encode()).hexdigest()[:24]

    def run(self, program: str | Path, inp: dict, want: str, *, timeout: float = 120.0) -> dict:
        program = Path(program)
        src = program.read_text(encoding="utf-8")
        psha = hashlib.sha256(src.encode("utf-8")).hexdigest()
        k = self._key(psha, inp, want)
        if self.mode == "replay":
            f = self.dir / f"{k}.json" if self.dir else None
            if not f or not f.exists():
                raise ReplayMiss(f"no recorded execution for {program.name} {want}")
            return json.loads(f.read_text(encoding="utf-8")) | {"replayed": str(f)}
        path, version = find_python(want)
        rec = {"runner": RUNNER_ID, "program": program.name, "program_sha256": psha, "input": inp,
               "runtime_wanted": want, "interpreter": path, "runtime_ran": None, "ok": False, "note": None,
               "output": None}
        if not path:
            rec["note"] = f"python{want} 해석기를 찾지 못했다"
        else:
            p = subprocess.run([path, "-I", str(program)], input=json.dumps(inp), capture_output=True, text=True,
                               timeout=timeout)
            if p.returncode == 0:
                out = json.loads(p.stdout)
                rec |= {"output": out, "ok": True, "runtime_ran": out.get("runtime")}
            else:
                rec["note"] = f"종료 코드 {p.returncode}: {p.stderr[-400:]}"
            ran = (rec["runtime_ran"] or f"CPython {version}").split()[-1]
            if want.count(".") == 2 and ran != want:
                rec["note"] = ((rec["note"] or "") + f" 원한 판 {want} 대신 {ran}에서 돌았다").strip()
            elif not ran.startswith(want):
                rec["note"] = ((rec["note"] or "") + f" 원한 판 {want} 대신 {ran}에서 돌았다").strip()
        if self.mode == "record" and self.dir:
            self.dir.mkdir(parents=True, exist_ok=True)
            (self.dir / f"{k}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                               encoding="utf-8")
        return rec


def record_receipt(L, p: str, req: int, rec: dict, at: str) -> int | None:
    """러너 결과를 장부에 쓴다. 영수증은 실제로 돈 판으로 적는다."""
    rid = None
    if rec["ok"]:
        rid = L.receipt(rec["runtime_ran"], rec["program_sha256"], rec["input"], rec["output"], at, p=p)
    L.executed(p, req, runtime_wanted=rec["runtime_wanted"], runtime_ran=rec["runtime_ran"],
               program_sha256=rec["program_sha256"], at=at, ok=rec["ok"], receipt_id=rid, note=rec["note"])
    return rid
