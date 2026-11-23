#!/usr/bin/env python3
"""Join immutable predictions to public evidence and a separately labelled replay."""
import csv
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PUBLIC = {
    "V01": ["https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011", "https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527"],
    "V02": ["https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846"],
    "V03": ["https://github.com/vega/vega-lite/issues/7507#issuecomment-854816048", "https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205"],
    "L01": ["https://github.com/libass/libass/issues/588"],
    "L02": ["https://github.com/libass/libass/issues/685"],
    "L03": [],
}
ALTERNATIVES = {
    "V01": "후속은 ecommerce10행이며 x-alias도 count field를, all-flat도 resolve/count 설정을 함께 변경. original135행 exact A의 성공이 아니다. 정상과 경계도 자료·집계·색상이 달라 nested 단독 효과 아님.",
    "V02": "공개 댓글은 다른 bar 입력과 explicit title. 자체 재생 B는 빈 그림이 아니라 compile error. N/I/D 모두 같은 A를 예측하므로 D의 독자적 이득으로 귀속 불가.",
    "V03": "maintainer 코드 진술과 실제 출력은 다르다. 연구 재생은5.1.0/5.20.2이며 원문 schema2의 실제판을 입증하지 않는다. 고정 category predicate는 다른 category가 zero인 미래 데이터에 일반화 불가. 전체 라벨 가독성은 별도 목표.",
    "L01": "원첨부는 요구 도식이며 B 실행 아님. 후속 작성자는 큰 띠에서도 영상 바로 아래 정렬을 추가로 말한다. CSS width centering을 ASS vertical margin 성공식으로 바꿀 수 없음.",
    "L02": "t가 collision 회피를 비활성화하는 기준판 코드는 설명근거. 비영 MarginV가 style을 덮는다는 사실은 충분한 이동량/시간대별 분리 성공을 보장하지 않음. explicit positioning 권고는 frozen B와 다름.",
    "L03": "사전 모집틀에서 적격 세 번째 libass 요구 없음. 제외 이슈나 후속 결과가 좋은 사례로 대체하지 않음.",
}


def main():
    vega = json.loads((ROOT / "streams/vega/outcomes.json").read_text())
    libass = json.loads((ROOT / "streams/libass/outcomes.json").read_text())
    replay = json.loads((ROOT / "replay/results.json").read_text())
    cases = {r["requirement_id"]: r for r in vega["cases"]}
    for slot in ["L01", "L02"]:
        cases[slot] = {"requirement_id": slot, "cells": [c for c in libass["cells"] if c["requirement_id"] == slot],
                       "needed_to_resume": libass["resume_first_action"]}
    with (ROOT / "predictions.csv").open(newline="") as handle:
        predictions = list(csv.DictReader(handle))
    replays = {r["prediction_id"]: r for r in replay["prediction_comparison"]}
    rows = []
    for pred in predictions:
        slot = pred["requirement_id"]
        case = cases.get(slot, {})
        cells = {(c["input_class"], c["operation"]): c for c in case.get("cells", [])}
        source_ids = sorted({source for c in cells.values() for source in c.get("source_ids", [])})
        row = {"outcome_id": pred["prediction_id"], "requirement_id": slot, "view": pred["view"],
               "frozen_choice": pred["choice"], "public_followup_urls": "; ".join(PUBLIC[slot]),
               "public_source_ids": ";".join(source_ids), "actual_author_runtime": "미확인" if case else "해당 없음·미충원",
               "strict_matching_new_cells": sum(bool(c.get("strict_complete", c.get("matched_new_discriminating_output", False))) for c in cells.values()),
               "logical_cells_reviewed": len(cells), "public_comparison": "미확인" if case else "미실시·미충원",
               "public_author_acceptance": "수락 진술 미확보; 실제 사용결과·수락 부재 미확인" if case else "해당 없음",
               "post_request_implementation_patch": "미확인; 읽은 timeline의 연결 PR/commit 관측 없음" if case else "해당 없음",
               "fixed_public_expected_output": "미확인" if case else "해당 없음",
               "replay_result": "replay/results.json" if pred["prediction_id"] in replays else "미실시",
               "replay_version": "Vega-Lite5.1.0/Vega5.20.2" if pred["prediction_id"] in replays else "해당 없음",
               "replay_comparison": ("보조 재생의 범주 선택 일치; V02 정상은 연구자 key-renaming 입력이며 원작성자 정상 검증 제외" if slot == "V02" else "보조 재생의 범주 선택 일치; V03은 고정10행의 부분집합" if slot == "V03" else "미실시"),
               "alternative_interpretation": ALTERNATIVES[slot],
               "needed_to_resume": case.get("needed_to_resume", "기존 프레임 안 적격 본문 복원 자료 확보; 모집규칙을 바꿀 때 별도 사전 프로토콜·선택지·판정 분모부터 새로 고정"),
               "detailed_cells_path": "streams/vega/outcomes.json" if slot.startswith("V") else "streams/libass/outcomes.json",
               "denominator_note": "N/I/D는 같은 공개관측을 공유한다. 3행을 3개의 독립 출력으로 합산하지 않는다. V03 정상/경계는 한 출력의9/1부분집합."}
        for input_class in ["normal", "boundary"]:
            for operation in ["A", "B"]:
                cell = cells.get((input_class, operation), {})
                key = f"{input_class}_{operation}"
                row[key + "_actual"] = cell.get("observed", cell.get("actual_output", "미실시·미충원"))
                row[key + "_limits"] = cell.get("missing", cell.get("reason", "해당 없음"))
        rows.append(row)
    with (ROOT / "outcomes.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    by_id = {r["prediction_id"]: r for r in predictions}
    same = []
    for slot in cases:
        same.append(all(by_id[slot + "-I"][k] == by_id[slot + "-D"][k] for k in ["choice", "normal_prediction", "boundary_prediction"]))
    def complete(cell):
        return bool(cell.get("strict_complete", cell.get("matched_new_discriminating_output", False)))
    filled_views = sum(pred["requirement_id"] in cases for pred in predictions)
    planned_requirements = {pred["requirement_id"] for pred in predictions}
    complete_cases = sum(len(case["cells"]) == 4 and all(complete(c) for c in case["cells"]) for case in cases.values())
    replay_slots = {r["prediction_id"].split("-")[0] for r in replay["prediction_comparison"]}
    replay_ties = sum(replays[s + "-I"]["categorical_comparison"] == replays[s + "-D"]["categorical_comparison"] == "일치"
                      and replays[s + "-I"]["observed_researcher_choice"] == replays[s + "-D"]["observed_researcher_choice"] for s in replay_slots)
    counts = {"generated_UTC": datetime.now(timezone.utc).isoformat(), "prediction_seal": vega["seal_sha"],
              "planned_requirements": len(planned_requirements), "filled_requirements": len(cases), "unfilled_requirements": len(planned_requirements) - len(cases),
              "planned_view_rows": len(predictions), "filled_view_rows": filled_views, "unfilled_view_rows": len(predictions) - filled_views,
              "public_logical_cells_reviewed": sum(len(c["cells"]) for c in cases.values()),
              "public_exact_new_output_cells_observed": sum(complete(c) for case in cases.values() for c in case["cells"]),
              "public_same_version_input_operation_cases_confirmed": complete_cases,
              "public_selected_cases_unconfirmed": len(cases) - complete_cases,
              "I_D_identical_predictions": {"numerator": sum(same), "denominator": len(same), "unit": "충원 요구; choice+normal+boundary 모두 동일"},
              "I_D_distinct_predictions": {"numerator": len(same) - sum(same), "denominator": len(same), "status": "관측 0"},
              "D_new_correct_conditional_denominator": len(same) - sum(same), "D_new_correct_status": "해당 없음; 서로 다른 사전예측의 조건부 분모0" if all(same) else "서로 다른 사전예측은 별도 원문 대조 필요",
              "public_confirmed_tie_status": "미확인; 예측이 같다는 사실과 실측 정답 동률을 구별",
              "replay_only": {"requirements": len(replay_slots), "view_rows": len(replay["prediction_comparison"]), "attempted_runs": len(replay["observations"]),
                              "svg_successes": sum(r["status"] == "rendered" for r in replay["observations"]),
                              "compile_failures": sum(r["status"] == "compile_failed" for r in replay["observations"]),
                              "confirmed_I_D_ties": replay_ties, "historical_confirmations": 0, "new_public_primary_works": 0,
                              "tie_scope": "보조 재생의 범주 선택만. V02 정상은 연구자 이름변환 대조이며 원작성자 외부 정상 입력의 검증을 포함하지 않음. V03은 한 출력의 부분집합."},
              "sensitivity_denominators": {"reject_researcher_normal_L02": len(set(cases) - {"L02"}), "also_require_two_independent_inputs_excluding_V03": len(set(cases) - {"L02", "V03"})},
              "note": "논리셀·요구·카드행·실행을 서로 바꾸어 세지 않는다. 빈L03는 실측 분모에서 제외한다. 버전 민감도는 별도 사후 탐색."}
    (ROOT / "evidence/comparison-counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"outcome_rows": len(rows), "filled_cases": len(cases), "public_cells": counts["public_logical_cells_reviewed"], "same_I_D": sum(same)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
