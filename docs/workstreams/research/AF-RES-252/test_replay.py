"""Synthetic inputs for the AF-RES-252 replay and selection rules."""
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

import collect as af

WHEN = "2026-11-25T00:00:00+00:00"
TAGS = ["postgresql", "greatest-n-per-group"]
BEFORE_REQUEST = af.Archive.before_request


def se_body(items, more=False):
    return {"items": items, "has_more": more, "quota_max": 300, "quota_remaining": 290}


def cross_body(items, total, cursor):
    return {"status": "ok", "message-type": "work-list", "message": {
        "items": [{"DOI": doi, "title": ["fixture"]} for doi in items],
        "total-results": total, "next-cursor": cursor,
    }}


class Responses:
    def __init__(self, output):
        self.output = output
        self.directory = output / "receipts"

    def add(self, key, provider, method, endpoint, params, value):
        receipt = key + ".1"
        raw = af.json_bytes(value)
        status, _ = af.status_document(provider, raw, 0, 200, 200)
        metadata = {
            "key": key, "attempt": 1, "id": receipt, "provider": provider, "method": method,
            "url": endpoint + "?" + urlencode(params), "request_parameters": params,
            "utc_start": WHEN, "utc_end": WHEN, "curl_exit": 0, "http_status": 200,
            "connect_status": 200, "response_headers": {},
            "status": status, "body_file": receipt + ".body", "body_bytes": len(raw),
            "body_sha256": af.digest(raw), **{field: value.get(field) for field in af.WRAPPER_META},
        }
        af.save(self.directory, receipt + ".body", raw)
        af.save(self.directory, receipt + ".meta.json", af.json_bytes(metadata))

    def se(self, key, method, endpoint, params, items, more=False):
        self.add(key, "stackexchange", method, af.API + endpoint, params, se_body(items, more))

    def filter(self, purpose):
        fields = sorted(set((af.WRAPPER + " " + af.FILTERS[purpose]).split()))
        self.se("filter-" + purpose, "filter-create", "/filters/create", {
            "base": "none", "include": ";".join(fields), "unsafe": "false",
        }, [{"filter": "fake-" + purpose, "filter_type": "safe", "included_fields": fields}])

    def frame(self, items, page=1, more=False):
        self.se(f"frame-p{page}", "questions", "/questions", {
            **af.FRAME_PARAMS, "page": page, "filter": "fake-frame",
        }, items, more)

    def mutate(self, key, change):
        filename = key + ".1"
        meta_path = self.directory / (filename + ".meta.json")
        body_path = self.directory / (filename + ".body")
        meta = json.loads(meta_path.read_bytes())
        value = json.loads(body_path.read_bytes())
        change(value)
        raw = af.json_bytes(value)
        meta["body_bytes"] = len(raw)
        meta["body_sha256"] = af.digest(raw)
        meta.update({field: value.get(field) for field in af.WRAPPER_META})
        body_path.write_bytes(raw)
        meta_path.write_bytes(af.json_bytes(meta))


def pars(phase, output, seal=None):
    return argparse.Namespace(phase=phase, output=output, seal=seal, retry_failed=False)


def frame_row(qid, seconds, duplicate=False, tags=None):
    row = {"question_id": qid, "creation_date": af.START + seconds, "tags": tags or TAGS}
    if duplicate:
        row.update(closed_reason="Duplicate", closed_date=af.START + seconds + 3600)
    return row


def origin_receipts(fixture, qid, created, title, body, initial):
    fixture.se(f"origin-{qid}", "questions-by-id", f"/questions/{qid}", {
        "site": "dba", "filter": "fake-origin",
    }, [{"question_id": qid, "creation_date": created, "title": title, "body": body}])
    edits = [{"post_id": qid, "creation_date": created + 30, "revision_number": 2,
              "revision_guid": f"edited-{qid}", "title": title, "body": body}]
    if initial is not None:
        edits.append({"post_id": qid, "creation_date": created, "revision_number": 1,
                      "revision_guid": f"initial-{qid}", "title": initial, "body": body})
    fixture.se(f"revisions-{qid}-p1", "revisions", f"/posts/{qid}/revisions", {
        "site": "dba", "filter": "fake-revision", "page": 1, "pagesize": 100,
    }, edits)


def search_receipt(fixture, query, page, items, more=False):
    signature = af.digest(query.encode())[:20]
    key = f"advanced-{signature}-p{page}"
    fixture.se(key, "advanced-search", "/search/advanced", {
        "site": "dba", "q": query, "tagged": "postgresql;greatest-n-per-group",
        "sort": "relevance", "order": "desc", "pagesize": 5, "page": page, "filter": "fake-search",
    }, [{"question_id": qid, "tags": tags} for qid, tags in items], more)
    return key


def destination_receipts(fixture, qid, aid, count, accepted):
    item = {
        "question_id": qid, "answer_count": count, "title": f"fixture {qid}",
        "body": "<blockquote>Possible duplicate <a href='/questions/950'>earlier</a></blockquote><p>target</p>",
    }
    if accepted:
        item["accepted_answer_id"] = aid
    fixture.se(f"destination-{qid}", "questions-by-id", f"/questions/{qid}", {
        "site": "dba", "filter": "fake-destination",
    }, [item])
    fixture.se(f"answer-{aid}", "answers-by-id", f"/answers/{aid}", {
        "site": "dba", "filter": "fake-answer-body",
    }, [{"question_id": qid, "answer_id": aid, "body": "<pre><code>SELECT true</code></pre>"}])


def cross_page(fixture, key, page, ids, total, cursor_in, cursor_out):
    fixture.add(f"crossref-{key}-p{page}", "crossref", "works", af.CROSSREF, {
        **af.CROSSREF_QUERIES[key], "sort": "score", "order": "desc", "rows": 2, "cursor": cursor_in,
    }, cross_body(ids, total, cursor_out))


class ReplayTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="af252-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.fixture = Responses(self.output)
        guard = patch.object(af.Archive, "before_request", side_effect=AssertionError("No network in fixtures"))
        guard.start()
        self.addCleanup(guard.stop)

    def test_wrapper_http_vs_verified_empty(self):
        self.assertEqual(af.status_document("stackexchange", b"", 56, 0, 403)[0], "proxy_connect_failed")
        self.assertEqual(af.status_document("stackexchange", b"", 6, 0, 0)[0], "transport_failed")
        self.assertEqual(af.status_document("stackexchange", b"", 0, 200, 200)[0], "invalid_json_object")
        self.assertEqual(af.status_document("stackexchange", b'{"items":[]}', 0, 200, 200)[0], "invalid_wrapper")
        self.assertEqual(af.status_document("stackexchange", b"{}", 22, 429, 200)[0], "http_error")
        err = b'{"error_id":502,"error_name":"throttle_violation","error_message":"fixture"}'
        self.assertEqual(af.status_document("stackexchange", err, 22, 400, 200)[0], "api_error")
        raw = af.json_bytes(se_body([]))
        self.assertEqual(af.status_document("stackexchange", raw, 18, 200, 200)[0], "incomplete_transfer")
        self.assertEqual(af.status_document("stackexchange", raw, 0, 200, 200)[0], "ok_empty")

    def test_normal_zero_frame_needs_actual_matching_filter_and_wrapper(self):
        self.fixture.filter("frame")
        self.fixture.frame([])
        result = af.run(pars("frame", self.output))
        self.assertEqual(result["frame_rows"], 0)
        self.assertEqual(result["last_has_more"], False)
        self.assertTrue((self.output / "frame.csv").is_file())
        rows, queries, stats = af.origins(af.Archive(self.output, offline=True))
        self.assertEqual((queries, stats["provider_rows_observed"]), ([], 0))
        manifest = af.packet_artifacts({"origins": [], "routes": [], "destinations": []}, [], [], True)
        self.assertEqual(len(manifest["reader/origins.jsonl"]), 0)
        self.assertEqual(json.loads(manifest["packet-manifest.json"])["status"], "ready")
        self.assertIn("frame.csv", rows)
        self.fixture.mutate("filter-frame", lambda payload: payload["items"][0]["included_fields"].remove(".items"))
        with self.assertRaisesRegex(af.Missing, "included_fields differs"):
            af.frames(af.Archive(self.output, offline=True))

    def test_quota_and_method_backoff_survive_a_restart(self):
        self.fixture.filter("frame")
        self.fixture.mutate("filter-frame", lambda payload: payload.update(quota_remaining=0))
        now = datetime.fromisoformat(WHEN) + timedelta(seconds=1)
        url = af.API + "/unexecuted-fixture"
        with patch.object(af, "utc", return_value=now):
            with self.assertRaisesRegex(af.Missing, "Quota exhausted"):
                BEFORE_REQUEST(af.Archive(self.output), "stackexchange", "questions", url)
            self.fixture.mutate("filter-frame", lambda payload: payload.update(quota_remaining=290, backoff=120))
            archive = af.Archive(self.output)
            with self.assertRaisesRegex(af.Missing, "2026-11-25T00:02:00"):
                BEFORE_REQUEST(archive, "stackexchange", "filter-create", url)
            BEFORE_REQUEST(archive, "stackexchange", "questions", url)

    def test_frame_boundary_through_next_page_and_candidate_cap(self):
        self.fixture.filter("frame")
        self.fixture.frame([frame_row(1000 + i, i, i <= 13) for i in range(1, 101)], more=True)
        self.fixture.frame([frame_row(1000 + i, min(i, 120)) for i in range(101, 201)], page=2, more=True)
        self.fixture.frame([frame_row(5, 120), frame_row(6, 121)], page=3)
        rows, result = af.frames(af.Archive(self.output, offline=True))
        self.assertEqual((len(rows), rows[-1]["question_id"], rows[-1]["raw_position"]), (120, 5, 201))
        self.assertEqual((result["boundary_rows"], result["last_page"]), (82, 3))
        self.assertEqual((result["candidate_rows"], result["duplicate_rows_above_cap"]), (12, 1))
        self.fixture.mutate("frame-p2", lambda payload: payload["items"][0].update(tags=["postgresql"]))
        with self.assertRaisesRegex(af.Missing, "outside the two-tag frame"):
            af.frames(af.Archive(self.output, offline=True))

    def positive_packet(self):
        for purpose in af.FILTERS:
            self.fixture.filter(purpose)
        origins = [frame_row(1000 + i, i, True) for i in range(4)]
        self.fixture.frame(origins)
        titles = ["Edited LATERAL approach", "SQL postgres", "How can I rank newest candidates?", "Which final keys appear?"]
        body = (
            '<aside class="js-post-notice">This question already has an answer here.</aside>'
            "<p>Need complete rows. <a href='https://dba.stackexchange.com/a/9000'>named answer</a></p>"
            "<table><tr><th>group</th><th>time</th></tr><tr><td>A</td><td>12</td></tr></table>"
            "<pre><code>SELECT DISTINCT ON (k) v FROM items</code></pre>"
        )
        for item, title in zip(origins, titles):
            qid = item["question_id"]
            original = "How can I find last row per group &amp; more?" if qid == 1000 else None
            origin_receipts(self.fixture, qid, item["creation_date"], title, body, original)
        self.search_key = search_receipt(self.fixture, "find last row per", 1, [
            (1000, TAGS), (4000, TAGS[:1]), (4001, TAGS[1:]), (4002, TAGS[:1]), (4003, TAGS[:1]),
        ], more=True)
        search_receipt(self.fixture, "find last row per", 2, [(7001, TAGS), (4010, TAGS[:1])])
        search_receipt(self.fixture, "rank newest candidates", 1, [])
        search_receipt(self.fixture, "which final keys appear", 1, [(7002, TAGS)])
        for qid, ids in [(1000, [7001, 7002]), (1001, [1001, 7001]), (1002, None), (1003, [])]:
            details = {} if ids is None else {"original_questions": [{"question_id": dest} for dest in ids]}
            self.fixture.se(f"duplicate-{qid}", "questions-by-id", f"/questions/{qid}", {
                "site": "dba", "filter": "fake-duplicate",
            }, [{"question_id": qid, "closed_reason": "duplicate", "closed_details": details}])
        destination_receipts(self.fixture, 7001, 9199, 4, False)
        destination_receipts(self.fixture, 7002, 9750, 3, True)
        self.fixture.se("answer-meta-7001-p1", "answers-on-question", "/questions/7001/answers", {
            "site": "dba", "filter": "fake-answer-meta", "sort": "votes", "order": "desc",
            "page": 1, "pagesize": 100,
        }, [{"question_id": 7001, "answer_id": aid, "score": score, "creation_date": created}
            for aid, score, created in [(9203, 5, 80), (9200, 5, 70), (9199, 5, 70), (9100, 4, 60)]])
        self.assertEqual(af.run(pars("origins", self.output))["unsealed_query_rows"], 4)
        with self.assertRaisesRegex(af.Missing, "full Git commit"):
            af.run(pars("routes", self.output))
        for command in (
            ("init", "-q", "-b", "fixture"),
            ("add", "frame.csv", "frame-stats.json", "queries.csv"),
            ("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Seal origins"),
        ):
            result = af.git(self.output, *command)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.seal = af.git(self.output, "rev-parse", "HEAD").stdout.decode().strip()
        result = af.run(pars("routes", self.output, self.seal))
        self.assertEqual(result["new_gets"], 0)
        return result["packet"]

    def test_packet_seal_and_reparse_shared_self_and_vacant_paths(self):
        manifest = self.positive_packet()
        self.assertEqual([row["records"] for row in manifest["reading_order"]], [4, 2, 14])
        mapping = json.loads((self.output / "mapping.json").read_bytes())
        self.assertEqual((mapping["paired_same_answer"], mapping["physical_answer_bodies"],
                          mapping["logical_answer_bodies"]), (1, 2, 3))
        self.assertEqual([route["route"]["status"] for route in mapping["routes"]], [
            "selected", "selected", "vacant_self_first", "vacant_under_two_tokens",
            "vacant_no_nonself_in_subset", "vacant_array_absent", "vacant_empty", "selected",
        ])
        self.assertEqual(mapping["routes"][0]["route"]["selected_position"]["raw_position"], 6)
        self.assertEqual(mapping["destinations"][0]["answer_id"], 9199)
        self.assertEqual(mapping["destinations"][1]["answer_id"], 9750)
        self.assertNotIn("answer_metadata_receipts", mapping["destinations"][1])
        self.assertEqual(mapping["origins"][0]["input_version"], "initial_revision")
        self.assertEqual(mapping["origins"][1]["input_version"], "current_no_complete_initial")
        origin_view = (self.output / "reader" / "origins.jsonl").read_text()
        self.assertNotIn("SELECT DISTINCT", origin_view)
        self.assertNotIn("named answer", origin_view)
        self.assertNotIn("already has an answer", origin_view)
        self.assertIn("A | 12", origin_view)
        self.assertIn("[method redacted]", origin_view)
        self.assertIn("SELECT true", (self.output / "reader" / "destinations.jsonl").read_text())
        self.assertEqual(af.run(pars("replay", self.output, self.seal))["packet"], manifest)

    def test_replay_catches_one_raw_record_missing_after_valid_hash(self):
        self.positive_packet()
        self.fixture.mutate(self.search_key, lambda payload: payload["items"].pop(2))
        with self.assertRaisesRegex(af.Missing, "Reparse differs"):
            af.run(pars("replay", self.output, self.seal))

    def test_replay_catches_array_reordering_after_valid_hash(self):
        self.positive_packet()
        self.fixture.mutate("duplicate-1000", lambda payload:
                            payload["items"][0]["closed_details"]["original_questions"].reverse())
        with self.assertRaisesRegex(af.Missing, "Reparse differs"):
            af.run(pars("replay", self.output, self.seal))

    def test_seal_catches_origin_title_changed_without_opening_targets(self):
        self.positive_packet()
        self.fixture.mutate("revisions-1000-p1", lambda payload: payload["items"][-1].update(title="Rank instead"))
        with self.assertRaisesRegex(af.Missing, "Seal differs on queries.csv"):
            af.run(pars("replay", self.output, self.seal))

    def test_crossref_cursor_reparse_and_reordered_records(self):
        cross_page(self.fixture, "shannon", 1, ["10.0000/a", "10.0000/b"], 3, "*", "next-1+")
        cross_page(self.fixture, "shannon", 2, ["10.0000/B", "10.0000/c"], 3, "next-1+", "next-2")
        cross_page(self.fixture, "kuhn-1900", 1, [], 0, "*", "present-even-when-empty")
        result = af.run(pars("crossref", self.output))
        self.assertEqual(result["kuhn-1900"]["status"], "normal_zero")
        self.assertEqual(len(result["kuhn-1900"]["pages"]), 1)
        self.assertEqual(result["shannon"]["pages"][1]["cursor_in"], "next-1+")
        self.assertEqual(result["shannon"]["pages"][1]["duplicate_dois"], ["10.0000/b"])
        self.assertEqual(af.run(pars("replay-crossref", self.output)), result)
        self.fixture.mutate("crossref-shannon-p1", lambda payload: payload["message"]["items"].reverse())
        with self.assertRaisesRegex(af.Missing, "Reparse differs"):
            af.run(pars("replay-crossref", self.output))

    def test_crossref_empty_items_with_nonzero_total_is_not_a_verified_zero(self):
        cross_page(self.fixture, "shannon", 1, ["10.0000/a"], 1, "*", "short")
        cross_page(self.fixture, "kuhn-1900", 1, [], 7, "*", "nonzero")
        result = af.crossref(af.Archive(self.output, offline=True))
        self.assertEqual(result["shannon"]["status"], "short_page")
        self.assertEqual(result["kuhn-1900"]["status"], "incomplete")
        self.assertIn("nonzero total", result["kuhn-1900"]["reason"])

    def test_title_stopword_and_occurrence_order(self):
        record = af.title_query("SQL How can I get a GROUP BY &amp; row_number x2 x2?")
        self.assertEqual(record["query"], "get group by row_number")
        self.assertEqual(json.loads(record["method_terms"]), ["GROUP BY", "row_number"])
        self.assertEqual(json.loads(record["excluded_tokens_and_reasons"])[-2:], [[10, "x2", "limit"], [11, "x2", "limit"]])
        self.assertEqual(af.title_query("is A postgres")["query_state"], "vacant_under_two_tokens")


if __name__ == "__main__":
    unittest.main(verbosity=2)
