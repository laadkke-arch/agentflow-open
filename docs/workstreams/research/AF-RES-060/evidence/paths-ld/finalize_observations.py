"""Assemble the directly reviewed path observations; no supplier code execution."""
from pathlib import Path
import collections
import datetime
import hashlib
import json

HERE = Path(__file__).parent.resolve()
OWNED = HERE.parents[1]
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
ASSIGNMENTS = json.loads((OWNED / "evidence/path-assignment-ld.json").read_text())
REQ = {x["case_id"]: x for x in json.loads((OWNED / "requirements.json").read_text())}
DOCS = json.loads((HERE / "document-records.json").read_text())
EXPOSURE = json.loads((HERE / "preview-exposure.json").read_text())
F1 = {x["catalog_id"]: x for x in json.loads((HERE.parent / "features-ld/features.json").read_text())}

# Each finding was checked against the saved bounded window. These are source
# summaries, not assertions that the source implements a requirement fixture.
FACTS = {
    "SC034-D1": ("Each piece of functionality", "suite는 별도 .Net 라이브러리로 나뉜다. JsonSchema.Net.Data는 instance/external data에 접근하는 vocabulary라고 소개하지만 사용 schema·입력·결과가 없다.", "author_statement"),
    "SC035-D1": ("require(schema.validate(json))", "Product 예시는 id:number/name:string/price:number와 required를 검증하는 Kotlin 호출이다. column_datatype의 세 문자열 enum 및 pii와 columns의 동적 관계는 보이지 않는다.", "author_code_expected_behavior_unexecuted"),
    "SC036-D1": ("JSON::Validator.validate(schema", "Ruby 예시는 required a와 integer 타입에서 a=5는 true, 빈 객체는 false, a=taco는 타입 오류라고 주석에 적는다. 이는 datatype 문자열 enum이나 type라는 데이터 속성·id:string 예제가 아니다.", "author_expected_outputs_unexecuted"),
    "SC038-D1": ("Validating an object", "Lisp 예시는 integer/maximum과 이스케이프 문자를 포함한 속성명의 number 제약이다. 숫자1 대신 문자열1인 객체의 실패 메시지를 제시한다. columns/pii 관계와 허용 datatype 값 목록은 없다.", "author_expected_outputs_unexecuted"),
    "SC039-D1": ("const { valid, errors, annotations }", "Node/browser용 compileSchema/validate와 원격 schema·draft·format 옵션을 소개한다. generic validation 및 schema $ref 옵션은 instance 값에서 enum을 만드는 직접 증거가 아니다.", "author_code_and_statement_unexecuted"),
    "SC040-D1": ("Replace references $ref by their definitions.", "inline은 참조를 정의로 대체하며 check는 jmc/jsonschema/jschon에 위임한다. Person 성별 enum·required 보존·Ajv 연결의 동일 실행 흐름 예시는 없다. compiler도 JSON Model 변환과 별도 런타임을 사용한다.", "author_statement_and_commands_unexecuted"),
    "LD008-D1": ("framing API interfaces", "Ruby JSON::LD는 framing 인터페이스를 명시한다. 창의 구체적 설명은 streaming 및 JSON-LD-star 중심이며 a=1인 객체 선택과 선택 객체의 b/c·credential 보존 입력/출력은 제시하지 않는다.", "author_statement"),
    "SC034-D2": ("An unhandled error", "취득한 playground HTML은 .Net 소개와 오류 placeholder만 제공한다. 브라우저에서 앱을 실행한 것이 아니므로 실제 앱 오류나 기능 부재를 관측했다고 하지 않는다.", "observed_html_shell_not_executed_app"),
    "SC034-D3": ("Explanations and examples", "공식 문서 첫 본문은 설명/예시·release notes·API reference가 sidebar에 있다는 안내다. 이 경로의 두 번째 문서에서 다른 절을 세 번째로 열지 않았다.", "observed_document_landing"),
    "SC035-D2": ("JSON encode/decode classes for Java", "jsonutil의 첫 창은 Java JSON parse/encode 및 JSONValue/JSONArray/JSONObject 설계다. schema 검증기가 아니며, 현재 json-kotlin-schema가 전환했다고 밝힌 이전 기반 라이브러리다.", "author_statement"),
    "SC035-D3": ("This project is no longer being maintained.", "yaml-simple는 유지보수 종료 및 부분 YAML 구현을 명시하고 Anchors/Aliases와 다중 문서 등을 미구현으로 열거한다. YAML 파싱의 한계를 후보 schema 검증 기능의 실패로 옮기지 않는다.", "author_statement"),
    "SC036-D2": (None, "원래 tools.ietf URL의 HTTP 취득403과 같은 URL 웹리더 실패로 문서를 읽지 못했다. 다른 mirror를 골라 후속 링크를 바꾸지 않았다.", "access_failure"),
    "SC036-D3": ("JSON Schema defines the media type", "draft04 core의 앞부분은 문서 목적·memo 상태·저작권·목차다. 같은 Ruby 구현판에 특정 instance 관계나 JSON:API 두조건을 적용한 근거가 아니다. 실제 preview611단어 노출을 별도 표시한다.", "official_definition_front_matter"),
    "SC038-D2": ('"type": ["object", "boolean"]', "2019-09 aggregate meta-schema는 schema 문서의 type을 object/boolean으로 두고 각 vocabulary meta-schema를 $ref로 연결한다. application instance의 column_datatype 값 목록이나 다른 column과의 관계와는 검증 대상이 다르다.", "official_meta_schema_code"),
    "SC039-D2": (None, "Bowtie의 선택된 hash route는 취득 HTML에 읽을 본문이 없다. JavaScript를 실행하지 않았으므로 비교 보고서의 시험 결과를 확인했다고 하지 않는다.", "dynamic_shell_unreadable_route"),
    "SC039-D3": ("schemaNode.validate({ character: \"AB\" })", "같은 README의 Draft Support 창은 validation 시험 주장과 추가 format 설치를 설명하고, remote schema의 character string 길이 위반 AB 예시를 준다. schema 주소를 푸는 $ref는 instance columns/pii 참조가 아니다.", "author_expected_outputs_unexecuted"),
    "SC040-D2": ("json-schema-utils 0.9.24", "PyPI는0.9.24로 표시되고 동일 계열의 inline/check/compiler 소개와 제한을 재게시한다. 선택 commit과 이 배포판의 일치 및 Person enum·required·Ajv 흐름은 확인되지 않는다.", "package_page_and_author_statements"),
    "SC040-D3": ("JSON Schema Utils", "두 번째 정보링크는 원 저장소로 돌아온다. 같은 고정 README 첫500을 재사용하며 새로운 기능 문서로 대체하지 않았다.", "same_cached_provider_window_revisited"),
    "LD008-D2": ("W3C Recommendation", "JSON-LD1.1의 2020-07-16 Recommendation 앞500은 판·저자·문서 목적·상태다. 프레임으로 중첩 객체를 골라 필드를 보존하는 구현 입력/출력 증거가 없다.", "official_specification_front_matter"),
    "LD008-D3": ("Required Ruby Version", "RDF gem 페이지에서 허용 renderer가 잡은 첫 article/heading은 Ruby>=3.0·저자·3.3.4 등 판 목록이다. json-ld gem의 프레임 동작이나 동일 구현판 근거가 아니다.", "package_metadata_only"),
}
WORKS = {
    "SC034-D2": ("supplier-json-everything-json-everything", False),
    "SC034-D3": ("supplier-json-everything-json-everything", False),
    "SC035-D2": ("supplier-pwall567-jsonutil", False),
    "SC035-D3": ("supplier-pwall567-yaml-simple", False),
    "SC036-D2": ("json-schema-core", True),
    "SC036-D3": ("json-schema-core", True),
    "SC038-D2": ("json-schema-core", True),
    "SC039-D2": ("bowtie-implementation-report", False),
    "SC039-D3": ("supplier-sagold-json-schema-library", False),
    "SC040-D2": ("supplier-zx80-json-schema-utils", False),
    "SC040-D3": ("supplier-zx80-json-schema-utils", False),
    "LD008-D2": ("w3c-jsonld11-syntax", True),
    "LD008-D3": ("supplier-ruby-rdf-rdf", False),
}
ENVIRONMENTS = {
    "JS-3": "원질문은 Node/TypeScript Ajv를 직접 묻는다. SC040은 Python CLI와 다른 엔진 위임/코드 생성을 보여주며 이 Ajv 검증 흐름으로의 통합은 미확인이다. 런타임 이름 차이만으로 불가라고 하지 않는다.",
    "JS-4": "원문 Python3.x/jsonschema 환경에서 후보를 호출하는 adapter·사용법은 이 경로에 없다. Kotlin/Ruby/Lisp/.Net/Node라는 공급자 환경은 관측했지만 Python 대안 사용 금지나 영구적 불가능을 가정하지 않는다.",
    "JS-6": "원문 Ajv 웹앱/Drupal10 JSON:API 흐름과 .Net 또는 Ruby 후보의 통합·교체 허용은 미확인이다. 원문이 JavaScript 언어 자체를 선언했다고 바꾸어 적지 않는다.",
    "LD-3": "원문 jsonld package 링크는 jsonld.js이고 이 후보는 Ruby gem이다. 같은 프레임 입력/출력과 교체 허용을 확인하지 못했으며 언어 이름 차이만으로 확정오답 처리하지 않는다.",
}
WHY = {
    "JS-3": "$ref를 인라인하는 보조 기능만으로 C1의 외부 gender enum 적용과 C2의 Person required 보존을 함께 확인할 수 없다. draft04/$id 혼용과 email format guard도 미확인이다.",
    "JS-4": "C1은 같은 instance의 columns 값과 pii를 비교하는 동적 제약이고 C2는 column_datatype 문자열의 제한된 값 집합이다. 일반적인 type/required 검사, schema $ref 또는 규격준수 주장은 두 조건의 직접 근거가 아니다.",
    "JS-6": "C1의 데이터 속성명 type 보존은 미확인이다. C2도 독립적으로 평가했다: SC034는 구체적 object/property string 제약이 없고, SC036은 properties.a.type=integer 및 string 입력 거부만 보여준다. 보통 property 이름을 id로 바꾸는 것과 integer 제약을 string 제약으로 바꾸는 추가 전이는 구분했다. 두조건을 동시에 보여야만 부분을 인정한다는 기준을 쓰지 않았다.",
    "LD-3": "framing이라는 이름은 찾았지만 a=1 객체만 남기는 C1, 그 객체 b/c와 credential 필드를 보존하는 C2의 직접 예제가 없다. 객체 경계와 값 목록을 동일시하거나 streaming writer의 동작을 frame 결과로 옮기지 않았다.",
}
NEXT = {
    "JS-3": "추가 예산에서 원 Ajv 흐름과 선택한 보조도구 판의 연결을 확인하고, 외부 enum·required 보존·draft04/$id·email을 분리한 원문 fixture를 같은 체인에서 검증한다.",
    "JS-4": "추가 예산에서 동일 후보판의 동적 instance 값 제약 API와 세 문자열 enum을 각각 확인한다. datatype은 허용값이지만 pii는 없는 column을 가리키는 근접음성 입력 및 Python 연결 근거가 최소 추가 자료다.",
    "JS-6": "추가 예산에서 type=article,id='1'/'2' 양성과 id=1 근접음성을 같은 구현판으로 확인하고, properties.type이 예약 schema 키워드와 혼동되지 않는 예시 및 원 Ajv 통합 범위를 확인한다.",
    "LD-3": "추가 예산에서 고정 Ruby json-ld 판의 frame API/시험 입력으로 원문 values/context를 재현하고, a=1 선택 후 b/c·credential 보존을 같은 출력에서 검사한다. 원 js 패키지 교체 허용도 별도 조건이다.",
}


def evidence(document):
    needle, summary, kind = FACTS[document["id"]]
    lines = []
    if document["window_file"] and needle:
        text = (HERE / document["window_file"]).read_text()
        for number, line in enumerate(text.splitlines(), 1):
            if needle in line:
                lines.append(number)
        assert lines, (document["id"], needle)
    return {
        "source_id": document["source_id"],
        "url": document["fixed_url"] or document["original_url"],
        "window_file": "evidence/paths-ld/" + document["window_file"] if document["window_file"] else None,
        "window_lines": lines,
        "confirmed_within_window": summary,
        "evidence_type": kind,
        "C1_support": False,
        "C2_support": False,
        "interpretation": "Confirms only the stated narrower fact or access limitation; exact requirement predicate remains unconfirmed.",
    }


def main():
    source_rows = []
    for doc in DOCS:
        doc["observed_utc"] = NOW
        doc["budget_status"] = "within_500_word_window"
        doc["actual_exposed_document_words"] = doc["words"]
        if doc["id"] == "SC036-D3":
            doc["budget_status"] = "overexposed_611_of_500"
            doc["actual_exposed_document_words"] = 611
            doc["exposure_audit"] = "evidence/paths-ld/preview-exposure.json"
            doc["acquired_utc"] = json.loads((HERE / "ietf-retry-receipt.json").read_text())["utc"]
        elif doc["id"] == "SC034-D2":
            doc["status"] = "read_html_shell_with_error_placeholder; app_not_executed"
        elif doc["id"] == "LD008-D3":
            doc["status"] = "directly_read_package_metadata_only"
            doc["implementation_version"] = "rdf dependency page3.3.4; not json-ld3.3.2"
        elif doc["status"] == "bounded_window_prepared_for_direct_read":
            doc["status"] = "directly_read_bounded_window"
        if doc["id"] == "SC040-D2":
            doc["implementation_version"] = "json-schema-utils0.9.24; source-commit linkage unconfirmed"
        if doc["id"] == "SC035-D3":
            doc["implementation_version"] = "yaml-simple1.19 described in pinned README; separate dependency"
        if doc["id"].endswith("D1"):
            work = F1[doc["catalog_id"]]["work_id"]
            reused = F1[doc["catalog_id"]]["reused_056_work"]
        else:
            work, reused = WORKS[doc["id"]]
        fact = evidence(doc)
        source_rows.append({
            "source_id": doc["source_id"], "work_id": work,
            "kind": doc["role"], "lineage": (
                "Same fixed provider work as F-" + doc["catalog_id"] if doc["id"].endswith("D1")
                else "Selected first/second body link; repeated README/API/standard editions are grouped by work_id."
            ),
            "Q": ["Q5", "Q6", "Q7"],
            "case_ids": sorted({a["case_id"] for a in ASSIGNMENTS if a["catalog_id"] == doc["catalog_id"]}),
            "catalog_id": doc["catalog_id"],
            "original_url": doc["original_url"], "fixed_url": doc["fixed_url"],
            "edition": doc.get("edition") or doc.get("implementation_sha") or doc.get("implementation_version") or "acquired response hash; provider-version linkage unconfirmed",
            "retrieved_utc": doc.get("acquired_utc") or F1[doc["catalog_id"]].get("acquired_utc"),
            "read_utc": NOW if doc["words"] else None,
            "read_time_precision": "Recorded after bounded direct review; not an exact per-screen event timestamp",
            "locus": {"window_file": fact["window_file"], "lines": fact["window_lines"], "words": doc["words"]},
            "confirmed": fact["confirmed_within_window"],
            "scope_and_limits": "Only the recorded document window. No provider execution, no third document, no inference from general compliance to a specific instance predicate. " + ("Actual preview exceeded500; this record is not protocol-compliant." if doc["id"] == "SC036-D3" else ""),
            "evidence_type": fact["evidence_type"],
            "counter_evidence_ids": [],
            "counter_search_result": "Related examples and explicit limits read; no direct contradiction of the exact requirement predicate established.",
            "read_status": doc["status"],
            "existing_work_reused": reused,
            "current_study_work_reuse": not doc["id"] in {"SC035-D2", "SC035-D3", "LD008-D3", "SC039-D2"},
            "eligible_for_new_primary_minimum": doc["id"] in {"SC035-D2", "SC035-D3"},
            "sha256": doc["hash"], "hash_kind": doc.get("hash_kind", "acquired_raw_bytes"),
            "window_sha256": doc["window_hash"],
            "budget_status": doc["budget_status"],
            "actual_exposed_document_words": doc["actual_exposed_document_words"],
            "reader": "features_ld/path_reader",
        })
    by_id = {x["id"]: x for x in DOCS}
    observations = []
    for assignment in ASSIGNMENTS:
        case = assignment["case_id"]
        catalog = assignment["catalog_id"]
        prefix = catalog.replace("-", "")
        for path in ["P1", "P2", "P3"]:
            documents = [by_id[prefix + "-D1"]]
            if path != "P1":
                extra = by_id.get(prefix + "-D" + path[-1])
                if extra:
                    documents.append(extra)
                else:
                    documents.append({
                        "source_id": None, "original_url": None, "fixed_url": None,
                        "implementation_sha": None, "implementation_version": None,
                        "window_file": None, "words": 0, "hash": None,
                        "actual_exposed_document_words": 0,
                        "status": "no_eligible_second_information_link",
                        "budget_status": "not_applicable_missing_link",
                    })
            direct = [evidence(d) for d in documents if d.get("id")]
            over = any(d["budget_status"].startswith("overexposed") for d in documents)
            same = path == "P1" or (catalog in {"SC-039", "SC-040"} and path == "P3")
            if catalog == "SC-038" and path == "P3":
                same = True
            copies = []
            for d in documents:
                copy = dict(d)
                if copy.get("window_file"):
                    copy["window_file"] = "evidence/paths-ld/" + copy["window_file"]
                copies.append(copy)
            observations.append({
                "case_id": case, "catalog_id": catalog, "path_id": path,
                "layer": REQ[case]["layer"],
                "C1_requirement": REQ[case]["C1"],
                "C2_requirement": REQ[case]["C2"],
                "question_url": REQ[case]["url"],
                "documents": copies,
                "C1_status": "unconfirmed", "C2_status": "unconfirmed",
                "environment_status": "unconfirmed",
                "environment_detail": ENVIRONMENTS[case],
                "same_implementation_version": same,
                "same_implementation_version_note": (
                    "Only fixed provider response(s); exact C1/C2 evidence is still absent."
                    if same else "Second source is another library, a standard, dynamic landing, or an unbound package edition; it cannot supply missing provider-condition evidence."
                ),
                "guard_status": "unconfirmed",
                "guard": REQ[case]["guard"],
                "judgment": "unconfirmed",
                "rationale": WHY[case] + " " + (direct[-1]["confirmed_within_window"] if path != "P1" and len(direct) > 1 else "첫창만으로 두조건 직접 확인에 이르지 못했다.") + (" 실제611/500 단어 초과노출은 미확인 판정과 별도로 프로토콜 위반이다." if over else ""),
                "direct_evidence": direct,
                "counterexample": {
                    "source": "requirements.json frozen at stage3",
                    "fixtures": REQ[case]["contrast_examples"],
                    "status": "researcher_contract_probe_not_run_on_this_supplier",
                    "observed_implementation_failure": False,
                    "scope": "Near-negative inputs identify what evidence is missing. They are not results from executing the candidate.",
                },
                "execution_status": "not_executed; document examples and author expected outputs only",
                "observed_utc": NOW,
                "budget_status": "overexposed_611_of_500" if over else "within_registered_document_and_window_limits",
                "exposure_audit": "evidence/paths-ld/preview-exposure.json" if over else None,
                "cost": {
                    "logical_document_actions": sum(bool(d.get("source_id")) for d in documents),
                    "registered_window_words": sum(d["words"] for d in documents),
                    "actual_exposed_unique_document_words": sum(d["actual_exposed_document_words"] for d in documents),
                    "extra_unique_words_beyond_window": sum(max(0, d["actual_exposed_document_words"] - d["words"]) for d in documents),
                    "shared_network_responses": True,
                },
                "comparison_ids": assignment["comparison_ids"],
                "comparison_ranks": assignment["ranks"],
                "next_minimum_evidence": NEXT[case],
            })
    assert len(observations) == 27
    assert len({(o["case_id"], o["catalog_id"], o["path_id"]) for o in observations}) == 27
    assert all(len(o["documents"]) <= 2 for o in observations)
    assert sum(o["budget_status"] == "overexposed_611_of_500" for o in observations) == 2
    for doc in DOCS:
        if doc["window_file"]:
            text = (HERE / doc["window_file"]).read_text().rstrip("\n")
            assert len(text.split()) == doc["words"]
            assert hashlib.sha256(text.encode()).hexdigest() == doc["window_hash"]
    (HERE / "observations.json").write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n")
    (HERE / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in source_rows))
    (HERE / "document-records.json").write_text(json.dumps(DOCS, ensure_ascii=False, indent=2) + "\n")
    unique_files = {d["window_file"]: d["words"] for d in DOCS if d["window_file"]}
    summary = {
        "stage3_sha": "5d01a6208edd9f8a20be7b31f7b545cef2200597",
        "reviewed_utc": NOW,
        "case_provider_pairs": len(ASSIGNMENTS), "providers": len({a["catalog_id"] for a in ASSIGNMENTS}),
        "paths": len(observations),
        "judgments": dict(collections.Counter(o["judgment"] for o in observations)),
        "complete": 0, "partial": 0, "confirmed_wrong": 0, "unconfirmed": 27,
        "truth_judgable_denominator": 0, "accuracy": "not_calculable; no truth-confirmed candidate",
        "strictly_budget_compliant_paths": 25,
        "overexposed_paths": [{k: o[k] for k in ["case_id", "catalog_id", "path_id", "budget_status"]} for o in observations if o["exposure_audit"]],
        "logical_document_actions": sum(o["cost"]["logical_document_actions"] for o in observations),
        "logical_registered_window_words": sum(o["cost"]["registered_window_words"] for o in observations),
        "logical_actual_unique_document_words_with_overexposure": sum(o["cost"]["actual_exposed_unique_document_words"] for o in observations),
        "document_source_records": len(DOCS),
        "distinct_nonempty_window_files": sum(w > 0 for w in unique_files.values()),
        "unique_saved_window_words": sum(unique_files.values()),
        "first_provider_cached_window_words": 3500,
        "additional_preview_display_body_words": EXPOSURE["body_display_words"],
        "additional_preview_unique_over_window_words": EXPOSURE["excess_body_words"],
        "preview_tool_and_navigation_tokens": EXPOSURE["preview_whitespace_tokens_including_tool_wrapper"] - EXPOSURE["body_display_words"],
        "new_body_transport_requests": sum(d["physical_body_requests"] for d in DOCS),
        "new_metadata_requests": sum(d.get("metadata_requests", 0) for d in DOCS),
        "new_successful_body_responses_including_shells": 10,
        "same_cached_provider_responses": 7,
        "same_response_second_document_actions": ["SC039-D3 fragment", "SC040-D3 self return"],
        "missing_second_link_paths": ["JS-4/SC-038/P3"],
        "research_status": "observations_complete_for_assigned_pairs; strict_protocol_partial_due_to_two_overexposed_paths",
        "supplier_execution_count": 0,
        "cost_units_note": "Network requests, distinct saved windows, per-pair/per-path logical readings, preview repeats, and excess unique words are separately counted. Repeated UI redisplays are not exhaustively instrumented.",
    }
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
