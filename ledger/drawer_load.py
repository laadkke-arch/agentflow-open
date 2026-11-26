"""서랍 미리 채우기(수집 흐름 대신 고정 자료). 단위 3의 수집 흐름이 아니다. 시험·측정·R1 실행이 같이 쓴다.

- 012 자료집 156항목: 청구 없는 관측(소개만 봄)과 영어·한국어 summary 꼬리표(D-b). 설계 예제 cases.preload_catalog와 같다.
- 같은 분야 잡음: opensource link-index의 F01(작업 대기열과 역압) 행. 관측은 소개만 봄, 꼬리표는 use(한국어)와 evidence.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"


# 012 자료집의 한국어 칸별 꼬리표(08 I25, I20의 a). D-c의 둘째 문장(항목마다 한계·주의 문장)을 한국어 breaks_when 꼬리표로 쓴다.
# 첫 문장은 D-b와 같아 summary에 이미 있다. False면 I20까지의 적재(D-b 영어·한국어 summary 둘)
CATALOG_KO_SLOTS = False


def catalog_ko_breaks(e: dict) -> str:
    """D-c 한국어에서 D-b(첫 문장) 뒤에 붙은 한계 문장."""
    head = e["D-b"]["ko"].strip()
    full = e["D-c"]["ko"].strip()
    return full[len(head):].strip() if full.startswith(head) else ""


def preload_catalog(L, at="2026-11-20T00:00:00Z", ko_slots=None) -> dict[str, int]:
    ko_slots = CATALOG_KO_SLOTS if ko_slots is None else ko_slots
    ids = {}
    for line in (FIX / "af-res-012" / "entries.jsonl").read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        oid, _ = L.observe(url=e["url"], edition_key="catalog@cb602858", edition_kind="fetch",
                           position="catalog entry", at=at, method="intro_only", quote=e["D-b"]["en"],
                           quote_lang="en", statement=e["D-b"]["ko"], via="collection",
                           evidence_ref=f"AF-RES-012@cb602858 corpus/entries.jsonl#{e['id']}")
        L.tag(oid, "summary", "one_up", "en", e["D-b"]["en"], written_from="catalog_description")
        L.tag(oid, "summary", "one_up", "ko", e["D-b"]["ko"], written_from="catalog_description")
        if ko_slots and catalog_ko_breaks(e):
            L.tag(oid, "breaks_when", "concrete", "ko", catalog_ko_breaks(e), written_from="catalog_description")
        ids[e["id"]] = oid
    return ids


def link_index_rows() -> list[dict]:
    with open(FIX / "link-index" / "link_index.tsv", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"))


def preload_noise(L, problem="F01", at="2026-11-20T00:00:00Z") -> dict[int, dict]:
    """link-index의 한 문제 행을 서랍에 넣는다. 돌려주는 값: 관측 ID → 행."""
    out = {}
    for r in link_index_rows():
        if r["problem"] != problem:
            continue
        oid, _ = L.observe(url=r["url"], edition_key=f"link-index@{r['commit'][:12]}", edition_kind="fetch",
                           position=f"record {r['record']}", at=at, method="intro_only", statement=r["use"],
                           via="collection", evidence_ref=f"opensource@{r['commit']} {r['file']}#L{r['line']}")
        L.tag(oid, "summary", "one_up", "ko", r["use"], written_from="catalog_description")
        if r["evidence"].strip():
            L.tag(oid, "summary", "concrete", "mixed", r["evidence"], written_from="source_quote")
        out[oid] = r
    return out


def preload_all_link_index(L, at="2026-11-20T00:00:00Z") -> dict[int, dict]:
    """link-index의 모든 문제 행을 서랍에 넣는다(실제 잡음). 돌려주는 값: 관측 ID → 행."""
    out = {}
    for r in link_index_rows():
        oid, _ = L.observe(url=r["url"], edition_key=f"link-index@{r['commit'][:12]}", edition_kind="fetch",
                           position=f"record {r['record']}", at=at, method="intro_only", statement=r["use"],
                           via="collection", evidence_ref=f"opensource@{r['commit']} {r['file']}#L{r['line']}")
        L.tag(oid, "summary", "one_up", "ko", r["use"], written_from="catalog_description")
        if r["evidence"].strip():
            L.tag(oid, "summary", "concrete", "mixed", r["evidence"], written_from="source_quote")
        out[oid] = r
    return out


def preload_synthetic(L, n: int, *, seed: int = 11, at="2026-11-20T00:00:00Z") -> list[int]:
    """합성 잡음 n개(07 R-6의 2만 개 규모용). link-index의 실제 use·evidence 문장을 반씩 잘라 고정 씨앗으로 다시 섞는다.
    어휘가 같은 분야라 실제 잡음보다 쉽지 않다. 주소는 합성 표시(synthetic.invalid)를 단다."""
    import random
    rows = link_index_rows()
    rng = random.Random(seed)
    halves = []
    for r in rows:
        for t in (r["use"], r["evidence"]):
            w = t.split()
            if len(w) >= 6:
                halves += [" ".join(w[: len(w) // 2]), " ".join(w[len(w) // 2:])]
    ids = []
    for i in range(n):
        a, b, c = rng.choice(halves), rng.choice(halves), rng.choice(halves)
        oid, _ = L.observe(url=f"https://synthetic.invalid/noise/{seed}/{i}", edition_key="synthetic", edition_kind="fetch",
                           position="synthetic", at=at, method="intro_only", statement=f"{a} {b}", via="collection")
        L.tag(oid, "summary", "one_up", "ko", f"{a} {b}", written_from="catalog_description")
        L.tag(oid, "summary", "concrete", "mixed", c, written_from="source_quote")
        ids.append(oid)
    return ids
