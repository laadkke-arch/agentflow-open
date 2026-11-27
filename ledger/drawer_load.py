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


# 012 보강 회차 p5 기록(opensource Q3, AR2·BR2·CR2)으로 쓴 012 꼬리표(08 I30). 켜면 D-b 둘에 더해 P5_SLOT_MAP 그대로
# (잡음 쪽 catalog 대상과 같은 칸 대응) 꼬리표를 붙인다. I26의 D-c 둘째 문장 판(CATALOG_KO_SLOTS)과는 따로 센다.
CATALOG_P5_TAGS = False


def catalog_012_p5() -> dict[str, dict]:
    return {json.loads(x)["id"]: json.loads(x) for x in
            (FIX / "af-res-012-p5" / "records.jsonl").read_text(encoding="utf-8").splitlines()}


def tag_p5(L, oid: int, r: dict) -> None:
    """p5 기록 하나(what·principle·scene·쓸모)를 P5_SLOT_MAP대로 꼬리표로 붙인다. 잡음 쪽과 012 쪽이 같은 함수를 쓴다."""
    lang = r.get("lang")
    src_lang = (lang or ["mixed"])[0] if isinstance(lang, list) else (lang or "mixed")
    for field, slot, height, lg in P5_SLOT_MAP:
        texts = [c[field.split(".")[1]] for c in r["claims"]] if field.startswith("claim.") else [r[field]]
        for t in texts:
            if t and t.strip():
                L.tag(oid, slot, height, src_lang if lg == "source" else lg, t, written_from="catalog_description")


# 012 자료집의 한국어 칸별 꼬리표(08 I25, I20의 a). D-c의 둘째 문장(항목마다 한계·주의 문장)을 한국어 breaks_when 꼬리표로 쓴다.
# 첫 문장은 D-b와 같아 summary에 이미 있다. False면 I20까지의 적재(D-b 영어·한국어 summary 둘)
CATALOG_KO_SLOTS = False


def catalog_ko_breaks(e: dict) -> str:
    """D-c 한국어에서 D-b(첫 문장) 뒤에 붙은 한계 문장."""
    head = e["D-b"]["ko"].strip()
    full = e["D-c"]["ko"].strip()
    return full[len(head):].strip() if full.startswith(head) else ""


def preload_catalog(L, at="2026-11-20T00:00:00Z", ko_slots=None, p5_tags=None) -> dict[str, int]:
    ko_slots = CATALOG_KO_SLOTS if ko_slots is None else ko_slots
    p5_tags = CATALOG_P5_TAGS if p5_tags is None else p5_tags
    p5 = catalog_012_p5() if p5_tags else {}
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
        if e["id"] in p5:
            tag_p5(L, oid, p5[e["id"]])
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


# ---- 08 I27: opensource catalog p5 대상으로 채운 실제 잡음(fixtures/catalog-p5, 커밋은 SOURCES.json)
P5_EXCLUDE_SESSIONS = ("AR2", "BR2", "CR2")     # 012 보강 회차(REQUESTS Q3)의 기록은 012 꼬리표 쪽이라 잡음에서 뺀다
P5_SLOT_MAP = (
    # (catalog 칸, 꼬리표 칸, 높이, 언어) — 돌리기 전에 정함(08 I27)
    ("what", "summary", "one_up", "source"),        # 원문 언어 한 줄 소개
    ("principle", "summary", "one_up", "ko"),       # 한국어 원리
    ("scene", "summary", "concrete", "ko"),         # 한국어 적용 장면(장면은 실패 조건이 아니라 쓰임새라 breaks_when에 두지 않는다)
    ("claim.text", "summary", "one_up", "ko"),      # 쓸모 주장(link-index의 use와 같은 자리)
    ("claim.evidence", "summary", "concrete", "mixed"),   # 원문 문장(link-index의 evidence와 같은 자리)
)
# claim.gap(원문에 없는 이식 단계)은 넣지 않는다. 가설이라 원문 쪽 꼬리표가 아니다.


def catalog_p5_rows() -> list[dict]:
    import gzip
    with gzip.open(FIX / "catalog-p5" / "targets.jsonl.gz", "rt", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh]


def catalog_p5_noise_rows(n: int = 20000) -> list[dict]:
    """012 주소(n1의 page가 같은 것)와 012 보강 회차 기록을 뺀 대상 가운데 대상 키의 SHA-1 순으로 앞 n개."""
    import hashlib
    from afledger import normalize
    pages = {normalize.keys(json.loads(x)["url"])["page"]
             for x in (FIX / "af-res-012" / "entries.jsonl").read_text(encoding="utf-8").splitlines()}
    keep = [r for r in catalog_p5_rows()
            if not any(normalize.keys(u)["page"] in pages for u in r["urls"] or [r["url"]])
            and not any(rec.split("-")[0] in P5_EXCLUDE_SESSIONS for rec in r["records"])]
    keep.sort(key=lambda r: hashlib.sha1(r["key"].encode("utf-8")).hexdigest())
    return keep[:n]


def preload_catalog_p5(L, n: int = 20000, at="2026-11-20T00:00:00Z") -> dict[int, dict]:
    """catalog p5 대상 n개를 잡음 관측으로 넣는다. 대상 하나 = 관측 하나. 꼬리표는 P5_SLOT_MAP대로."""
    commit = json.loads((FIX / "catalog-p5" / "SOURCES.json").read_text(encoding="utf-8"))["commit"]
    out = {}
    for r in catalog_p5_noise_rows(n):
        oid, _ = L.observe(url=r["url"] or f"https://catalog.invalid/{r['key']}", edition_key=f"catalog-p5@{commit[:12]}",
                           edition_kind="fetch", position=f"target {r['key']}", at=at, method="intro_only",
                           statement=r["what"] or r["principle"] or r["key"], via="collection",
                           evidence_ref=f"opensource@{commit} {r['file']}#{r['key']}")
        tag_p5(L, oid, r)
        out[oid] = r
    return out
