"""Create the fixed edits, with natural opening bytes kept immutable."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def read(id, index, suffix):
    return (FIXTURES / "original" / f"{id}-{index}.{suffix}").read_bytes()


def replace_once(raw, before, after):
    if raw.count(before) != 1:
        raise ValueError(f"expected one occurrence of {before!r}")
    return raw.replace(before, after, 1)


def encode_json(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()


def prepare():
    edits = []

    def group(id, layer, engine, suffix, baseline, variants, main_path=None):
        for variant, (raw, path, before, after, expected, preserve) in variants.items():
            if variant == "base" and main_path:
                path_on_disk = FIXTURES / "original" / main_path
                assert path_on_disk.read_bytes() == raw
            else:
                path_on_disk = FIXTURES / "input" / f"{id}-{variant}.{suffix}"
                path_on_disk.write_bytes(raw)
            edits.append({
                "id": id, "layer": layer, "engine": engine, "variant": variant,
                "file": path_on_disk.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "input_bytes": len(raw), "derived_from": baseline,
                "edit": {"path": path, "before": before, "after": after},
                "predicted": expected, "preserve": preserve,
            })

    v55 = read("V8625", 1, "jsonc")
    local = b'"formatType": "customFormatter"'
    global_gate = b'"customFormatTypes": true'
    v55_edits = {
        "base": (v55, None, None, None, "JSON 파싱 단계 실패 예상", "원 쉼표와 모든 바이트"),
        "local": (replace_once(v55, local, b'"formatType": "time"'), "/encoding/x/axis/formatType",
                  "customFormatter", "time", "쉼표가 남아 원판 JSON 파싱 실패 예상", "날짜 문자열, 집계, config"),
        "shared": (replace_once(v55, global_gate, b'"customFormatTypes": false'), "/config/customFormatTypes",
                   True, False, "쉼표가 남아 원판 JSON 파싱 실패 예상", "x 선언, 날짜 문자열과 집계"),
    }
    group("V8625", "natural-exact-reported", "v55", "jsonc", "V8625",
          v55_edits, "V8625-1.jsonc")
    norm = {k: (re.sub(rb",(?=\s*[}\]])", b"", val[0]), *val[1:]) for k, val in v55_edits.items()}
    norm["base"] = (norm["base"][0], None, None, None, "등록 함수가 빠져 런타임 오류 예상", "원 문자열과 모든 값")
    norm["local"] = (*norm["local"][:4], "표준 시간 형식으로 축 실행 예상", "bar 집계와 원 날짜")
    norm["shared"] = (*norm["shared"][:4], "custom format 차단 후 공통 실행 경로 예상", "bar 집계와 원 날짜")
    group("V8625P", "normalized-diagnostic", "v55", "json", "V8625 plus trailing commas removed", norm)

    baseline = read("V8627", 3, "json")
    spec = json.loads(baseline)
    order = ["D", "A", "E", "B", "C"]
    local = copy.deepcopy(spec)
    local["layer"][0]["encoding"]["y"]["sort"] = order
    shared = copy.deepcopy(spec)
    inherited = copy.deepcopy(shared["layer"][0]["encoding"].pop("y"))
    other = shared["layer"][1]["encoding"].pop("y")
    assert inherited == other
    inherited["sort"] = order
    shared["encoding"] = {"y": inherited}
    group("V8627", "natural-schema-substitute", "v417", "json", "V8627-3", {
        "base": (baseline, None, None, None, "공유 y 스케일에서 원 순서 관측", "두 레이어와 다섯 행"),
        "local": (encode_json(local), "/layer/0/encoding/y/sort",
                  spec["layer"][0]["encoding"]["y"]["sort"], order,
                  "같은 y를 쓰므로 두 레이어의 순서 위치에 파급될 수 있음", "text의 저장 sort와 색 구분"),
        "shared": (encode_json(shared), ["/encoding/y", "/layer/0/encoding/y", "/layer/1/encoding/y"],
                   [None, other, other], [inherited, None, None],
                   "양쪽이 하나의 D/A/E/B/C 순서를 상속", "bars/text의 field, group 색, mark 속성"),
    }, "V8627-3.json")

    baseline = read("V8628", 1, "json")
    spec = json.loads(baseline)
    local = copy.deepcopy(spec)
    local["encoding"]["color"]["value"] = "steelblue"
    shared = copy.deepcopy(spec)
    shared["params"][0]["select"]["translate"] = False
    group("V8628", "natural-date-substitute", "v56", "json", "V8628-1 + data 2.5.3", {
        "base": (baseline, None, None, None, "비활성 brush 기준 SVG와 Vega 이벤트 저장", "data, config, brush와 color"),
        "local": (encode_json(local), "/encoding/color/value", "lightgray", "steelblue",
                  "fallback에 걸리는 bar만 색 후보가 바뀜. 초기 empty predicate에 따라 효과 공석 가능",
                  "brush 동작과 active 조건, chart 구조"),
        "shared": (encode_json(shared), "/params/0/select/translate", None, False,
                   "이동 이벤트 스트림이 달라짐. 정지 SVG에서 마크 차이는 예상하지 않음",
                   "month projection, color condition과 데이터"),
    }, "V8628-1.json")

    m3981 = read("M3981", 1, "mmd")
    group("M3981", "natural-date-substitute", "m93", "mmd", "M3981-1", {
        "base": (m3981, None, None, None, "원 저자는 빈 출력 보고. 대체판 재현 여부 미확인", "두 연결과 그룹"),
        "local": (replace_once(m3981, b"start --> A\r\n", b"start --> AA\r\n"),
                  "/line/10", "start --> A", "start --> AA",
                  "start의 목적 ID만 바뀜. 주변 기하는 새로 계산", "AA→AB3 및 그룹의 소속"),
        "shared": (replace_once(m3981, b"flowchart TB", b"flowchart LR"),
                   "/line/1", "flowchart TB", "flowchart LR",
                   "전역 방향만 바뀌며 문제 끝점은 동일", "두 간선의 endpoint와 AA 소속"),
    }, "M3981-1.mmd")

    m3982 = read("M3982", 1, "mmd")
    style = b'%%{init: {"themeCSS": ".labelText { visibility: hidden !important; }"}}%%\r\n'
    group("M3982", "natural-date-substitute", "m93", "mmd", "M3982-1", {
        "base": (m3982, None, None, None, "alt와 opt의 고정 라벨 및 조건 본문", "원 순서와 메시지"),
        "local": (replace_once(m3982, b"alt is sick", b"alt If sick"), "/line/3/condition",
                  "is sick", "If sick", "조건 문자열만 바뀌고 alt 고정 표지와 opt 유지", "else, opt, messages, actors"),
        "shared": (style + m3982, "/line/1/init/themeCSS", None, style.decode().strip(),
                   "CSS로 labelText를 모두 가려 alt, opt 양쪽에 영향, 분기 조건과 메시지는 존재",
                   "alt 및 opt의 제어 관계, 조건·메시지"),
    }, "M3982-1.mmd")

    m3987 = read("M3987", 1, "mmd")
    group("M3987", "natural-date-substitute", "m93", "mmd", "M3987-1", {
        "base": (m3987, None, None, None, "독립 정수 반올림 [33,35,33], 합 101", "세 입력값 및 제목"),
        "local": (replace_once(m3987, b'"Dogs" : 80', b'"Dogs" : 79'), "/line/2/value",
                  80, 79, "합 100이 될 수 있으나 Dogs 원값 위반, 분모와 세 호의 비율도 달라짐", "Cats, Rats 저장값 및 제목"),
        "shared": (replace_once(m3987, b"pie title", b"pie showData title"), "/line/1/showData",
                   None, True, "범례 세 개에 원값 추가. 퍼센트 합 101은 남음", "세 원값, 같은 호와 퍼센트"),
    }, "M3987-1.mmd")

    m3994 = read("M3994", 1, "mmd")
    subgroup = b"subgraph AG [Ancient Greek]\r\n"
    group("M3994", "natural-outside-quota", "m93", "mmd", "M3994-1", {
        "base": (m3994, None, None, None, "AG/MG cluster 위치와 dotted edges 관측", "원 topology와 label"),
        "local": (replace_once(m3994, subgroup, subgroup + b"direction BT\r\n"), "/line/3/direction",
                  None, "BT", "그룹 밖 node 연결 때문에 국소 적용이 무시될 수 있음", "MG 명세, dotted edge와 노드 내용"),
        "shared": (replace_once(m3994, b"graph LR", b"graph TB"), "/line/1", "graph LR", "graph TB",
                   "전체 배치 변경 예상", "노드 label, edge endpoint, dotted 기호"),
    }, "M3994-1.mmd")

    c01 = b'''flowchart LR
    AA1["Stage"]
    AB3["Stage"]
    AA1 --> End
    AB3 --> End
    classDef phase fill:#86efac,stroke:#166534
    class AA1,AB3 phase
'''
    group("C01", "constructed", "m93", "mmd", "M3981 IDs AA1 and AB3, identical labels and class added", {
        "base": (c01, None, None, None, "동일 Stage, 서로 다른 ID와 두 연결", "End"),
        "local": (replace_once(c01, b'AA1["Stage"]', b'AA1["Stage (local)"]'),
                  "/line/2/label", "Stage", "Stage (local)", "AA1 label 한 곳. 레이아웃 연쇄 이동 가능", "AB3 label 및 두 class 사용"),
        "shared": (replace_once(c01, b"#86efac", b"#fbbf24"),
                   "/line/6/classDef/phase/fill", "#86efac", "#fbbf24",
                   "AA1, AB3 fill 둘 다 바뀜", "두 label 및 End fill/edge endpoint"),
    })

    c02 = b'''flowchart LR
    AA1["First"] --> AB3
    AA1["Latest"] --> End
'''
    group("C02", "constructed", "m93", "mmd", "M3981 terminal IDs, repeated AA1 edge use and declaration", {
        "base": (c02, None, None, None, "하나의 AA1과 두 간선, 마지막 label 적용 예상", "AB3와 End"),
        "local": (replace_once(c02, b'"First"', b'"First (edited)"'), "/line/2/label",
                  "First", "First (edited)", "앞 선언의 레코드 바뀌나 유효 AA1 표시 그대로", "두 간선과 Latest 표지"),
        "shared": (replace_once(c02, b'"Latest"', b'"Shared"'), "/line/3/label",
                   "Latest", "Shared", "두 간선이 같은 AA1 표시를 공유", "AB3, End, 두 endpoints"),
    })

    c03_data = json.loads(read("V8627", 3, "json"))
    dataset = c03_data["datasets"][c03_data["data"]["name"]][:3]
    encoding = {"x": {"field": "names", "type": "nominal"}, "y": {"field": "values", "type": "quantitative"}}
    c03 = {"data": {"values": dataset}, "encoding": encoding, "layer": [
        {"mark": {"type": "bar", "opacity": 0.6}},
        {"mark": {"type": "point", "filled": True, "color": "#e11d48", "size": 80}},
    ], "config": {"mark": {"color": "#2563eb"}}}
    c03_local = copy.deepcopy(c03)
    c03_local["layer"][1]["mark"]["color"] = "#a21caf"
    c03_shared = copy.deepcopy(c03)
    c03_shared["config"]["mark"]["color"] = "#15803d"
    group("C03", "constructed", "v417", "json", "V8627 first dataset A/B/C, point override and mark config", {
        "base": (encode_json(c03), None, None, None, "bar 공통 파랑, point 로컬 빨강", "데이터 A/B/C"),
        "local": (encode_json(c03_local), "/layer/1/mark/color", "#e11d48", "#a21caf",
                  "point만 보라색", "bar 파랑, 세 좌표"),
        "shared": (encode_json(c03_shared), "/config/mark/color", "#2563eb", "#15803d",
                   "bar만 녹색. point 로컬 빨강이 공유 기본값보다 우선", "point 빨강과 세 좌표"),
    })
    (FIXTURES / "operations.json").write_text(json.dumps(edits, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    prepare()
