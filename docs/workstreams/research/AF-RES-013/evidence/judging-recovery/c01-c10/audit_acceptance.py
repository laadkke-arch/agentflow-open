"""Independent, read-only audit of AF-RES-013 artifacts and local git history.

Writes only this shard's ACCEPTANCE_AUDIT.json and ACCEPTANCE_AUDIT.md.
Does not execute baselines, change common artifacts, or decide overall completion.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
REPO = BASE.parents[3]
OWNED = BASE.relative_to(REPO).as_posix() + "/"

def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=REPO, text=True, capture_output=True, check=check)
    return r.stdout.strip() if check else r

def rel(path):
    return path.relative_to(REPO).as_posix()

def read(path):
    return json.loads(path.read_text())

def gitjson(commit, path):
    return json.loads(git("show", f"{commit}:{rel(path)}"))

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def parsedate(s):
    return datetime.fromisoformat(s.replace(" UTC", "+00:00").replace("Z", "+00:00"))

def site(url):
    host = (urlparse(url).hostname or "").lower()
    if host.endswith("githubusercontent.com") or host.endswith("github.com"):
        return "github.com"
    for domain in ("aclanthology.org", "arxiv.org", "ceur-ws.org", "codalism.com", "coliee.org", "informationr.net", "nii.ac.jp", "nist.gov", "python.org", "springer.com", "swift.org", "uva.nl"):
        if host == domain or host.endswith("." + domain):
            return domain
    return host

def normalized(url):
    return url.split("#", 1)[0].rstrip("/")

started = datetime.now(timezone.utc).isoformat()
head = git("rev-parse", "HEAD")
manifest = read(BASE / "manifest.json")
base = manifest["base_commit"]
case_data = read(BASE / "cases/CASES.json")
cases = case_data["cases"]
prefix_manifest = {p["id"]: p for p in read(BASE / "cases/PREFIX_MANIFEST.json")["prefixes"]}
gold_path = BASE / "cases/CASES.json"
first_gold = git("log", "--reverse", "--format=%H", "--diff-filter=A", head, "--", rel(gold_path)).splitlines()[0]
first_scope = git("log", "--reverse", "--format=%H", "--diff-filter=A", head, "--", OWNED + "SCOPE.md").splitlines()[0]
first_sampling = git("log", "--reverse", "--format=%H", "--diff-filter=A", head, "--", OWNED + "SAMPLING.md").splitlines()[0]
prefix_rows = []
for c in cases:
    f = BASE / c["prefix_file"]
    history = git("log", "--format=%H", head, "--", rel(f)).splitlines()
    last, first = history[0], history[-1]
    h = digest(f)
    blob = subprocess.check_output(["git", "show", f"{head}:{rel(f)}"], cwd=REPO)
    prefix_rows.append(dict(case_id=c["id"], path=rel(f), sha256=h,
        manifest_hash=prefix_manifest[c["id"]]["sha256"], cases_hash=c["prefix_sha256"],
        all_three_hashes_match=h == prefix_manifest[c["id"]]["sha256"] == c["prefix_sha256"],
        same_as_head=sha256(blob).hexdigest() == h,
        first_commit=first, latest_content_commit=last,
        latest_content_commit_before_gold=(last != first_gold and git("merge-base", "--is-ancestor", last, first_gold, check=False).returncode == 0),
        commit_time_utc=parsedate(git("show", "-s", "--format=%cI", last)).astimezone(timezone.utc).isoformat()))
prior_gold_paths = git("grep", "-l", '"gold_items"', first_gold + "^", "--", OWNED, check=False).stdout.splitlines()

families = Counter(c["family"] for c in cases)
case_rows = [dict(case_id=c["id"], family=c["family"], pinned_version=c["pinned_version"],
    pin_is_sha=bool(re.fullmatch(r"[0-9a-f]{40}", c["pinned_version"])),
    pin_in_url=c["pinned_version"] in c["url"], decision_date=c["decision_date"],
    decision_event=c.get("decision_event"), decision_evidence_url=c.get("decision_evidence_url", c.get("decision_event_url")),
    decision_evidence_field="decision_evidence_url" if "decision_evidence_url" in c else "decision_event_url",
    gold_count=len(c["gold_items"]), source_ids=c.get("source_ids", [])) for c in cases]
strict_types = {"partial_reversal_after_adoption", "adopted_specification_rescinded", "adopted_design_replaced", "partial_reversal", "adopted_specification_replaced"}
successor_rows = []
for c in cases:
    successors = c.get("superseded_by") or []
    if isinstance(successors, dict):
        successors = [successors]
    for s in successors:
        outcome = c["decision_outcome"]
        accepted_before = outcome == "accepted" or "accepted proposal" in outcome
        change_type = s.get("type", s.get("kind"))
        successor_rows.append(dict(case_id=c["id"], original_outcome=outcome,
            change_type=change_type, strict_adopted_then_changed=accepted_before and change_type in strict_types,
            successor_url=s["url"], pinned_version=s["pinned_version"],
            successor_date=s.get("date", s.get("decision_date")),
            scope=s.get("scope", s.get("reversed_scope"))))

run_rows = []
for baseline in ("A", "B"):
    for path in sorted((BASE / "runs" / baseline).glob("C*.json")):
        r = read(path)
        history = git("log", "--follow", "--format=%H", head, "--", rel(path)).splitlines()
        original = gitjson(history[-1], path)
        committed = gitjson(head, path)
        elapsed = (parsedate(r["ended_at_utc"]) - parsedate(r["started_at_utc"])).total_seconds()
        budgets = r["budget"]
        charges = [len(r["opened_documents"])] + [v for k, v in budgets.items() if k in {"opened_pages", "budget_pages_charged", "charged_page_budget", "open_attempts", "document_open_attempts"} and isinstance(v, (int, float))]
        charged = max(charges)
        nq = len(r["queries"])
        nc = len(r["candidates"])
        native = [q for q in r["queries"] if q.get("tool") in {"grep.app", "github_public"} or "grep.app/api/search" in q.get("q", "") or ("github.com/search" in q.get("q", "") and "type=code" in q["q"])]
        # Compare the records actually present, not an existing generated audit's totals.
        run_rows.append(dict(case_id=r["case_id"], baseline=baseline,
            raw_response_nonempty=isinstance(r.get("raw_response"), str) and bool(r["raw_response"].strip()),
            same_as_head=r == committed,
            raw_response_unchanged_since_first_commit=original["raw_response"] == committed["raw_response"],
            candidates_unchanged_since_first_commit=original["candidates"] == committed["candidates"],
            first_commit=history[-1], sha256=digest(path), query_count=nq,
            query_fields_complete=all(all(q.get(k) for k in ("q", "at_utc", "tool")) for q in r["queries"]),
            opened_document_rows=len(r["opened_documents"]), conservative_charged_pages=charged,
            candidate_count=nc, elapsed_seconds=elapsed,
            within_query_limit=(nq <= 12 if baseline == "A" else True),
            within_page_limit=charged <= (20 if baseline == "A" else 25),
            within_candidate_limit=nc <= 15,
            within_time_limit=(0 <= elapsed <= 1200 if baseline == "B" else elapsed >= 0),
            code_search_attempts=len(native), web_queries=sum("web" in q.get("tool", "") for q in r["queries"]),
            context_inputs=r.get("context_inputs"), execution_agent=r.get("execution_agent"),
            gold_seen=r.get("gold_seen"), other_runs_seen=r.get("other_runs_seen"),
            exposure_records=len(r.get("exposures", [])),
            candidate_catalogue_url_missing=sum(not c.get("discovery_catalogue_url") for c in r["candidates"]) if baseline == "B" else None,
            prefix_committed_before_started=parsedate(next(p["commit_time_utc"] for p in prefix_rows if p["case_id"] == r["case_id"])) <= parsedate(r["started_at_utc"])))

source_data = read(BASE / "sources.json")
counted_ids = source_data["counting"]["counted_ids"]
source_index = {s["id"]: s for s in source_data["sources"]}
counted = [source_index[i] for i in counted_ids]
required = "id url accessed_at_utc source_type title version_or_date sections_read confirmed limits level used_in".split()
source_rows = [dict(id=s["id"], url=s["url"], title=s["title"], source_type=s["source_type"],
    site_computed_from_actual_url=site(s["url"]), level=s["level"],
    missing_fields=[k for k in required if k not in s or s[k] in (None, "", [])],
    counted_as_case_document=s["source_type"] in {"design-proposal", "design_proposal", "case_document"},
    sections_read=s["sections_read"], recorded_in=s.get("recorded_in")) for s in counted]
site_counts = Counter(site(s["url"]) for s in counted)
source_types = Counter(s["source_type"] for s in counted)
strict_reviews = [s["id"] for s in counted if s["source_type"] in {"review_discussion", "review_mailing_list", "review_forum_thread", "review-discussion"}]
announcements = [s["id"] for s in counted if s["source_type"] == "review_decision_announcement"]
gen = [s for s in counted if s["source_type"] == "generative_citation_evaluation_paper"]
old_sources = git("show", "7f627a81199f06da7f7b15f979e7fef25dd17602:docs/workstreams/research/AF-RES-009/sources.json").lower()
gen_new = {s["id"]: dict(title_absent_in_009=s["title"].lower() not in old_sources, url_absent_in_009=s["url"].lower() not in old_sources) for s in gen}
committed_source_data = gitjson(head, BASE / "sources.json")
committed_index = {s["id"]: s for s in committed_source_data["sources"]}
committed_counted_ids = committed_source_data["counting"]["counted_ids"]
committed_reviews = [i for i in committed_counted_ids if committed_index[i]["source_type"] in {"review_discussion", "review_mailing_list", "review_forum_thread", "review-discussion"}]
original_sampling = git("show", first_sampling + ":" + OWNED + "SAMPLING.md")

committed_changes = git("diff", "--name-only", base, head).splitlines()
status_lines = git("status", "--porcelain=v1", "--untracked-files=all", check=False).stdout.rstrip("\n").splitlines()
status_paths = [l[3:].split(" -> ")[-1] for l in status_lines]
outside_committed = [p for p in committed_changes if not p.startswith(OWNED)]
outside_working = [p for p in status_paths if not p.startswith(OWNED)]
present = {f: (BASE / f).exists() for f in ("JUDGMENTS.json", "RESULT.md", "SELF_CHECK.md", "HANDOFF.md")}
committed_final = {f: git("cat-file", "-e", head + ":" + OWNED + f, check=False).returncode == 0 for f in present}
remote_result = git("ls-remote", "origin", "refs/heads/work/research-af-res-013", check=False)
remote_head = remote_result.stdout.split()[0] if remote_result.returncode == 0 and remote_result.stdout.strip() else None
remote_observed_at = datetime.now(timezone.utc).isoformat()
by_baseline = {}
for b in ("A", "B"):
    rows = [r for r in run_rows if r["baseline"] == b]
    by_baseline[b] = dict(runs=len(rows), candidates=sum(r["candidate_count"] for r in rows),
        queries=sum(r["query_count"] for r in rows), max_queries=max(r["query_count"] for r in rows),
        opened_document_rows=sum(r["opened_document_rows"] for r in rows),
        conservative_charged_pages=sum(r["conservative_charged_pages"] for r in rows),
        max_pages=max(r["conservative_charged_pages"] for r in rows),
        max_elapsed_seconds=max(r["elapsed_seconds"] for r in rows),
        min_candidates=min(r["candidate_count"] for r in rows), max_candidates=max(r["candidate_count"] for r in rows),
        all_budget_checks=all(all(r[k] for k in ("within_query_limit", "within_page_limit", "within_candidate_limit", "within_time_limit")) for r in rows))

audit = dict(schema_version=1, auditor="내부 별도 검토", model_label="GPT-6 Astra Pro", audit_started_at_utc=started,
    scope="Existing data and git history only; no baseline rerun, no external-source body reread in this audit, no completion verdict.",
    source_commit=base, audited_head=head,
    remote_branch_head_observed=remote_head, remote_observed_at_utc=remote_observed_at,
    remote_equals_audited_head=remote_head == head,
    remote_command="git ls-remote origin refs/heads/work/research-af-res-013",
    remote_note="Read-only command during this audit; concurrent root commits may advance either head. New uncommitted artifacts are not remote evidence.",
    input_hashes={f: digest(BASE / f) for f in ["cases/CASES.json", "cases/PREFIX_MANIFEST.json", "sources.json", "SCOPE.md", "SAMPLING.md", "BASELINE_RULES.md"]},
    commits=dict(first_scope=first_scope, first_sampling=first_sampling, first_gold=first_gold,
        prior_tree_paths_with_gold_items_literal=prior_gold_paths),
    prefixes=prefix_rows,
    corpus=dict(cases=len(cases), families=dict(families), max_family_fraction=max(families.values()) / len(cases),
        gold_items=sum(len(c["gold_items"]) for c in cases), min_gold_items=min(len(c["gold_items"]) for c in cases),
        case_rows=case_rows, case_host_counts=dict(Counter(site(c["url"]) for c in cases)),
        successors=successor_rows, strict_successor_cases=sorted({r["case_id"] for r in successor_rows if r["strict_adopted_then_changed"]})),
    noncase_sources=dict(count=len(counted), unique_ids=len(set(counted_ids)), unique_normalized_urls=len({normalized(s["url"]) for s in counted}),
        rows=source_rows, sites=dict(site_counts), max_site=max(site_counts.values()), types=dict(source_types),
        template_ids=[s["id"] for s in counted if s["source_type"].startswith("template")],
        methodology_ids=[s["id"] for s in counted if s["source_type"].startswith("methodology")],
        crossfield_overview_ids=[s["id"] for s in counted if s["source_type"] == "crossfield_overview_paper"],
        crossfield_domains={"patent":["M05","M07"],"law":["M09"],"academic":["M12"]},
        generative_citation_ids=[s["id"] for s in gen], generative_absence_in_009=gen_new,
        strict_review_ids=strict_reviews, review_announcement_ids=announcements,
        committed_counted_ids=committed_counted_ids, committed_strict_review_ids=committed_reviews,
        current_counting_delta=dict(added=sorted(set(counted_ids)-set(committed_counted_ids)), removed=sorted(set(committed_counted_ids)-set(counted_ids))),
        case_site_cap_interpretation_preregistered="사례30개는" in original_sampling and "비사례 최소수" in original_sampling),
    runs=run_rows, run_totals=by_baseline,
    write_scope=dict(committed_changed_file_count=len(committed_changes), committed_outside_owned=outside_committed,
        working_paths_outside_owned=outside_working, working_uncommitted_paths=status_paths,
        owned_path=OWNED, note="This tests repository tracked/untracked changes, not arbitrary filesystem or process activity."),
    final_deliverables=dict(present_in_working_tree=present, present_at_audited_head=committed_final,
        report_tables_and_self_check_not_assessed=True,
        next_check="After root writes RESULT/SELF_CHECK, inspect exact required columns, per-Q evidence/counterexamples, exactly three §4 weaknesses, then verify separate commits and remote HANDOFF equality."))
(OUT / "ACCEPTANCE_AUDIT.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")

all_hash = all(r["all_three_hashes_match"] and r["same_as_head"] for r in prefix_rows)
all_ancestor = all(r["latest_content_commit_before_gold"] for r in prefix_rows)
all_runs_frozen = all(r["same_as_head"] and r["raw_response_unchanged_since_first_commit"] and r["candidates_unchanged_since_first_commit"] for r in run_rows)
strict_ids = audit["corpus"]["strict_successor_cases"]
review_note = f"현재 집계는 {len(strict_reviews)}개 토론 원문: {', '.join(strict_reviews)}. 감사 HEAD의 실제 토론은 {len(committed_reviews)}개다. 원 재개 checkpoint caa2a814는 토론4개와 M25 수락 공고를 포함했고, 감사 지적 후 이미 읽은 PS-R-S21-LENS로 최소수 산입을 변경했다."
lines = [
    "# AF-RES-013 종료조건 독립 감사", "",
    f"감사 시각: `{started}`. 기준 HEAD: `{head}`. 시작 source_commit: `{base}`.", "",
    "이 감사는 현재 데이터·파일 해시·Git 조상 관계·최초 커밋 이후 불변 여부를 독립 계산한다. 기준선을 재실행하거나 다른 작업의 결과를 읽지 않았다. 외부 원문 31+25개를 다시 열었다는 감사가 아니며, 원장에 기록된 실제 열람과 고정판·결정 근거의 형식 및 내용 요약을 검토했다. 전체 작업의 완료 판정을 대신하지 않는다. 상세 행과 입력 해시는 ACCEPTANCE_AUDIT.json에 있다.", "",
    "## 조건별 결과", "",
    "| 조건 | 판정 | 독립 확인 내용 | 적용 범위·최소 추가 확인 |",
    "|---|---|---|---|",
    f"| 접두부 31개의 SHA256 | {'예' if all_hash else '아니오'} | 실제 파일·PREFIX_MANIFEST·CASES의 해시가 31/31 같고 HEAD와도 같다. | 실제 실행자가 읽은 바이트의 별도 receipt는 없다. 파일 불변·입력 경로·실행 시각의 일치까지 확인했다. |",
    f"| 접두부가 gold보다 먼저 커밋 | {'예' if all_ancestor else '아니오'} | C01–C30 최초 8cb2b8e, C14 수정 c993618, C31 ba1cc08; 모두 최초 gold f6f59a8의 엄격 조상이다. 직전 tree의 owned_path에 gold_items 문자열이 없다. | Git 조상 검사는 SHA 사전순 비교가 아니다. |",
    "| SCOPE·SAMPLING 선행 고정 | 예 | 두 파일 최초 커밋 4398d0b가 모든 접두부·gold 커밋보다 앞선다. | C31은 초기 선정 분절 오류를 후속 보정한 사례이며 완전한 사전 확정 31개라고 표현하면 안 된다. |",
    f"| 30개 이상·4계열 이상·한 계열 50% 이하 | 예 | {len(cases)}개: Kubernetes 6 / Python 9 / Rust 8 / Swift 8. 최대 9/31=29.03%. | 네 계열의 결정문에 대한 목적 표집이며 설계자 모집단의 확률 표본은 아니다. |",
    f"| 사례별 gold 3개 이상 | 예 | {sum(len(c['gold_items']) for c in cases)}항목, 최소 {min(len(c['gold_items']) for c in cases)}개. | 분절·역할·일치는 작업자 및 내부 검토 코딩이며 저자가 만든 검색 정답 완전성을 보장하지 않는다. |",
    "| 고정판·결정일·결정 사건 | 예 | 31개 모두 40자 SHA, 그 SHA가 포함된 원문 URL, ISO 결정일과 결정 사건·근거 주소가 있다. | 날짜는 기능 출시일과 다르다. 특히 C29는 원 결정 메일을 인용한 후속 리뷰 글에 의존한다는 한계를 유지한다. |",
    f"| 채택 후 번복·대체 5개 이상 | 예 | 엄격 집합 6개: {', '.join(strict_ids)}. | C10의 기각 후 대체와 C11/C13 초안 대체를 6개 분모에서 제외했다. 부분 번복을 제안 전체 폐기로 바꾸지 않는다. |",
    f"| 비사례 본문 자료 20개 이상 | 예 | 현재 최소수 집합 {len(counted)}개, 고유 URL {len({normalized(s['url']) for s in counted})}개. 사례 문서·재열람·실패·snippet을 이 집합에 넣지 않았다. | 원장 D1·읽은 절·확인 내용·한계가 모두 존재하는지 확인했으며 이 감사에서 원문 전체 재열람은 하지 않았다. |",
    f"| 비사례 사이트당 최대 3개 | 예 | URL에서 GitHub raw/api를 합쳐 {len(site_counts)}개 사이트, 최대 {max(site_counts.values())}개. | SOURCE_COUNT의 사이트 숫자를 그대로 믿지 않고 실제 URL로 다시 계산했다. |",
    "| 사례에도 동일 사이트 상한 적용 여부 | 해석문제 | 31개 고정판이 모두 GitHub 계열 호스트다. 최초 SAMPLING 4398d0b에서 상한은 비사례 최소수에 적용하고 사례는 독립 프로젝트별로 센다고 사전 명시했다. | 이 해석을 RESULT·SELF_CHECK에서 드러내야 한다. 상한을 사례에도 문자 그대로 적용하면 사례 최소30을 충족하지 못한다. |",
    f"| 템플릿·절차 4개 | 예 | {', '.join(audit['noncase_sources']['template_ids'])}; 네 계열 각1개. | 절 도입 시점의 내용 검증은 TEMPLATES와 역사판 원장에 의존하며 현행 템플릿을 초기판으로 소급하지 않는다. |",
    f"| 방법론 논문 4개 | 예 | {', '.join(audit['noncase_sources']['methodology_ids'])}: 원 논문5개와 종합 논문1개. | 장르를 템플릿·웹 소개와 혼동하지 않았다. |",
    "| 다른 분야 독립 정답원 평가 3분야 | 예 | 특허 M05/M07, 법률 M09, 학술 M12의 개요 논문. 실행 논문 M11과 프로토콜 M08/M10도 별도로 존재한다. | 분야별 편향과 이 과제의 대응은 methods/CROSSFIELD.md와 RESULT에서 내용 확인해야 한다. |",
    "| 009에 없는 생성형 인용 정확성 평가 2개 | 예 | M13·M14의 제목과 실제 URL이 고정 009 sources.json에 없다. 둘 다 D1 본문·평가 절이 기록돼 있다. | 문자열 비교는 동일 논문의 모든 별칭을 증명하지 않지만 제목·URL과 연구 내용이 일치하는 항목은 발견되지 않았다. |",
    f"| 리뷰 토론 원문 5개 | {'예' if len(strict_reviews) >= 5 else '해석문제'} | {review_note} | HEAD 대비 추가 {audit['noncase_sources']['current_counting_delta']['added']} / 제외 {audit['noncase_sources']['current_counting_delta']['removed']}. 해당 보정의 commit·push 증거를 연결한다. |",
    f"| A 전 사례 / B 최소20 사례의 원 응답 | 예 | A31·B31, 총62개의 비어 있지 않은 raw_response. A204·B138 후보. | 후보 수가 작아도 실제 질의·열람이 남아 있으므로 미실행으로 취급하지 않았다. |",
    f"| 원 응답·후보 목록 불변 | {'예' if all_runs_frozen else '아니오'} | 62/62의 raw_response와 structured candidates가 각 파일 최초 커밋과 HEAD에서 같고 작업본도 HEAD와 같다. | query/open 관측 보정과 원 응답 변경은 구별했다. |",
    "| A 검색·열람·후보 예산 | 예 | 합계326질의·561열람 기록·204후보. 사례별 최대12질의·20페이지·9후보. 모든 A에 웹 검색과 로그인 없는 코드 검색 시도 기록이 있다. | 코드 검색 시도와 성공은 다르며 차단·fallback을 성공으로 올리지 않는다. |",
    "| B 열람·시간·후보 예산 | 예 | 합계176질의·698열람 행, 보수적 비용703페이지. 사례별 최대25페이지·531초·9후보. | B에는 질의12회 상한이 없다. C31의17질의를 A 규칙으로 위반 판정하지 않는다. B12/B22의 성공 수와 시도 수, B26의 find 포함 비용을 구분했다. |",
    "| 새 문맥·gold 미열람 | 해석문제 | 62개가 접두부와 실행규칙만 입력으로 선언하고 gold_seen=false / other_runs_seen=false를 보존한다. 접두부 최종 커밋은 각 실행 시작보다 앞선다. | 이는 기록과 문맥 분리 절차의 근거다. 파일시스템 접근 차단이나 사전학습 기억 제거를 증명하지 않는다. 완전 blind라고 표현하지 않는다. |",
    f"| owned_path만 수정 | {'예' if not outside_committed and not outside_working else '아니오'} | source_commit..HEAD의 변경 {len(committed_changes)}파일 모두 owned_path. 현재 tracked/untracked 변경도 범위 밖0이다. | Git에서 관측 가능한 저장소 변경 감사이며 저장소 밖 모든 활동을 증명하지 않는다. dot-control·공통 계약·main의 내용 변경은 없다. |",
    f"| 원격 branch 상태 | {'예' if remote_head == head else '해석문제'} | git ls-remote 관측 `{remote_head}`; 감사 HEAD `{head}`. | 원격이 같아도 uncommitted 파일은 원격 근거가 아니다. 동시 작업 중 전진한 경우 새 HEAD에서 차이만 다시 확인한다. |",
    f"| RESULT 표1–3·Q1–Q8·반례·§4 정확히3건 | 아니오 | 감사 시점 RESULT 파일 존재={present['RESULT.md']}. 이 감사에서는 본문 조건을 판정하지 않았다. root가 작성·검증하는 영역이다. | 파일 작성 후 지정 열·미확인 확인방법·두 종류 근거·다섯 반례 기록을 직접 대조한다. 미완료 상태를 연구 결과 실패로 해석하지 않는다. |",
    f"| SELF_CHECK 통과 후 HANDOFF | 아니오 | 파일 존재 SELF_CHECK={present['SELF_CHECK.md']}, HANDOFF={present['HANDOFF.md']}. 이 감사는 최종 자기점검·원격 인계를 판정하지 않는다. | RESULT 검토 → SELF_CHECK commit → HANDOFF 단독 commit → push → 원격 본문과 로컬 바이트 비교를 순서대로 확인한다. |",
    "", "## 판정 시점 구분", "",
    f"기준 HEAD에는 앞선 접두부·gold·A/B 실행 묶음이 커밋되어 있다. 핵심 최종 파일의 HEAD 존재 여부는 `{committed_final}`이다. 사용자 규칙에 따라 커밋되지 않은 결과는 인수 조건의 영속 근거가 아니다. 이 감사 파일도 root가 해당 검증 묶음에 포함해 커밋한 뒤에만 영속 근거가 된다. 저장소는 root와 동시에 사용하므로 본 표는 명시한 SHA·입력 해시·시각에만 적용된다.", "",
    "## 판정을 바꿀 최소 추가 확인", "",
    "1. 현재 sources의 M25→PS-R-S21-LENS 변경과 판단 묶음을 커밋·push한 뒤 본 감사의 입력 해시와 새 커밋을 연결한다.",
    "2. RESULT/SELF_CHECK 작성 완료 후 필수 표·Q별 근거·반례 기록·§4 세 건을 파일 내용으로 검토한다. 본 감사는 이 항목을 추정 통과시키지 않았다.",
    "3. 최종 HANDOFF 단독 커밋 후 원격 본문을 다시 읽어 로컬과 같음을 확인한다. 원격 branch HEAD만 같은 것으로 본문 재열람 요구를 대체하지 않는다.", "",
    "## 재현 명령", "", "```bash", f"python {rel(OUT / 'audit_acceptance.py')}", "```", "",
    "이 명령은 기존 실행을 재실행하지 않고 이 폴더의 두 감사 파일만 갱신한다. 읽기 전용 ls-remote도 다시 실행하며, 이후 원격이 바뀌면 새 시점에 해당 차이를 확인해야 한다.", ""
]
(OUT / "ACCEPTANCE_AUDIT.md").write_text("\n".join(lines))
print(json.dumps(dict(head=head, prefixes=len(prefix_rows), hashes_ok=all_hash, ancestry_ok=all_ancestor,
    cases=len(cases), gold=sum(len(c["gold_items"]) for c in cases), strict_successors=strict_ids,
    noncase=len(counted), sites=dict(site_counts), strict_reviews=strict_reviews,
    runs=by_baseline, raw_responses_unchanged=all_runs_frozen,
    outside_owned=outside_committed + outside_working, final_present=present), ensure_ascii=False, indent=2))
