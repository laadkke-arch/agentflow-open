"""Conservative reference checks on the shipped request, menu and records only."""
import json
import re
import sys


def complete_records(text):
    return [json.loads(line) for line in text.splitlines(keepends=True) if line.endswith("\n")]


def recommend(packet):
    menu = packet["options"]
    text = packet["request"]
    rows = complete_records(packet["structure"])
    values = {r["path"]: r["value"] for r in rows}
    strings = {p: v.strip() for p, v in values.items() if isinstance(v, str)}
    checked = []
    outcome = "정당 보류"

    def result(links, prediction, ask):
        nonlocal checked
        if not checked:
            checked = [p for p in values if values[p] is not None]
        return {
            "result": outcome,
            "links": [{"id": k, "url": menu[k]["url"]} for k in links],
            "basis_paths": checked,
            "prediction": prediction,
            "needed_value": ask,
        }

    if "v_axis_format" in menu:
        axes = [p for p, v in values.items()
                if isinstance(v, dict) and isinstance(v.get("axis"), dict) and v["axis"].get("formatType")]
        gate = values.get("/config", {})
        checked = axes + (["/config"] if isinstance(gate, dict) and gate.get("customFormatTypes") else [])
        versions = "원 formatter 함수의 구현·등록과 어떤 날짜 표현을 처음 넣었는가"
        if len(checked) > len(axes):
            return result(["v_axis_format", "v_format_registry"], "x guide의 로컬 함수 이름과 공통 활성 gate를 둘 다 확인. 함수/다른 실행 사용처는 미확인.", versions)
        return result(["v_axis_format", "v_format_registry"], "temporal guide 포맷·공통 등록은 구분 가능. 실제 설정/함수 또는 범위는 일부 미확인.", versions)

    if "v_sort" in menu:
        children = [(p, v) for p, v in values.items()
                    if re.fullmatch(r"/layer/\d+/encoding/y", p) and isinstance(v, dict)]
        if len(children) >= 2 and len({json.dumps(v, sort_keys=True) for _, v in children}) == 1:
            outcome = "정확"
            checked = [p for p, _ in children]
            return result(["v_sort", "v_layer"], "공통 y를 유지한다는 조건에서 두 같은 y 정의의 root sort를 제안. 두 mark의 범주 위치가 함께 정렬. 숨은 resolve 및 실제 출력 확인 필요.", "공통 y 축·scale을 계속 공유하는가")
        return result(["v_sort", "v_layer", "v_resolve"], "두 겹의 sort가 같거나 독립 scale로 분리됐는지 확인이 필요.", "두 레이어의 y 설정과 공통 축 유지 요구")

    if "v_translate" in menu:
        encoding = values.get("/encoding/color", {})
        condition = encoding.get("condition", {}) if isinstance(encoding, dict) else {}
        brush = [
            (p, v) for p, v in values.items()
            if re.search(r"/params/\d+$", p) and isinstance(v, dict)
            and isinstance(v.get("select"), dict) and v["select"].get("type") == "interval"
        ]
        tabs = ["v_translate"]
        outcome = "정당 보류"
        message = "마크 위와 빈 캔버스의 brush 이벤트가 달라지는지 확인. 색상 편집으로 동작 수정을 주장할 근거 미확인."
        for p, value in brush:
            if isinstance(condition, dict) and condition.get("param") == value.get("name"):
                checked = [p, "/encoding/color"]
                tabs += ["v_condition"]
                if "/encoding/x" in values and "x" in value["select"].get("encodings", []):
                    checked.append("/encoding/x")
                    tabs.append("v_projection")
                message = "drag brush 정의→축과 조건부 색의 공유 참조가 일부 또는 전부 확인됨. 포인터 시작·끝과 빈 선택 동작 미확인."
                break
        return result(tabs, message, "원 UI 버전 및 실패 pointer 위치와 어떤 색 동작을 유지할지")

    if "m_edge" in menu:
        pairs = re.findall(r"\b([A-Za-z]\w*)\s*-->\s*([A-Za-z]\w*)\b", text)
        source_lines = [p for p, v in strings.items() if re.search(r"\w+\s*-->\s*\w+", v)]
        groups = [p for p, v in strings.items() if v.startswith("subgraph ")]
        checked = source_lines + groups
        why = "작성자가 두 끝점 변경을 이미 설명. 다른 간선과 중첩 그룹을 유지할 의도, 렌더 영향은 미확인."
        if not pairs:
            why = "간선의 한 끝점과 원래 대상 ID가 필요."
        return result(["m_edge", "m_subgraph"], why, "start가 큰 subgraph A를 계속 가리켜야 하는가")

    if "m_alt" in menu:
        alt = [p for p, v in strings.items() if v.startswith("alt ")]
        opt = [p for p, v in strings.items() if v.startswith("opt ")]
        if alt and opt:
            outcome = "정확"
            checked = alt + opt
            return result(["m_seq_label", "m_seq_css"], "조건 뒤 문구는 로컬. 이 alt와 opt는 고정 표시를 쓰고 공유 labelText CSS의 적용 후보 둘 모두에 해당.", "한 조건 문구인가, 여러 그룹 키워드의 표시인가")
        return result(["m_alt", "m_seq_label", "m_seq_css"], "키워드 종류는 글에서 보이지만 실제 사용처를 검증 못함.", "사용 중인 fragment들과 숨길 범위")

    if "m_pie_round" in menu:
        entries = []
        for p, v in strings.items():
            match = re.fullmatch(r'"([^"]+)"\s*:\s*(\d+(?:\.\d+)?)', v)
            if match:
                entries.append((p, match[1], float(match[2])))
        total = sum(n for _, _, n in entries)
        if entries and total and any(v.startswith("pie ") or v == "pie" for v in strings.values()):
            predicted = [round(n / total * 100) for _, _, n in entries]
            reported = re.findall(r"(\d+)%", text)
            if reported and str(sum(predicted)) == reported[-1]:
                outcome = "정확"
                checked = [p for p, _, _ in entries]
                return result(["m_pie_round", "m_pie_values"], f"보이는 원값 합 {total:g}, 독립 반올림 {predicted} 합 {sum(predicted)}. showData는 범례 원값만 바꿈.", "정수 표지 합을 보정할지, 소수/실측 원값을 보여 줄지")
        return result(["m_pie_round", "m_pie_values"], "보고된 합과 원값 및 반올림 체인을 연결할 slice가 필요.", "slice 원값 및 원하는 반올림")

    if "m_direction" in menu:
        return result(["m_direction", "m_orientation"], "그룹 하나 지시와 루트 전체 배치는 별개. 보인 선언만으로 내부 노드에 닿는 외부 간선은 미확인.", "유지할 dotted 교차선과 맞출 정확 cluster 위치")

    outcome = "비교불가"
    return result([], "사용할 후보 메뉴가 없음.", "형식과 판")


def main():
    for line in sys.stdin:
        print(json.dumps(recommend(json.loads(line)), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
