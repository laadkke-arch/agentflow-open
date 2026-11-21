#!/usr/bin/env python3
"""Build metadata-only sampling artifacts. Never writes question or answer bodies."""
import datetime
import json
import pathlib
import re
import subprocess

P = pathlib.Path(__file__).resolve().parent

def read(name):
    return json.loads((P / name).read_text())

def write(name, data):
    (P / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
old = read("new-questions.json")
supp = [q for q in old if q["platform"] == "reddit"]
if supp:
    for i, q in enumerate(supp, 1):
        q["previous_draft_id"] = q["id"]
        q["id"] = f"R{i:03d}"
        q["selected"] = False
        q["exclusion_reason"] = "Absolute publication date is search-extracted only; normal HTML 200 has no post body or date metadata. JSON path already failed 403 and was not retried."
    write("supplementary-reddit-questions.json", supp)

se = {str(x["question_id"]): x for x in read("se-metadata.json") + read("se-extra-metadata.json")}
revs = read("se-revisions.json") + read("se-extra-revisions.json")
initial = {str(x["post_id"]): x for x in revs if x.get("revision_number") == 1 and x["words"] > 0}
hn = {str(x["id"]): x for x in read("hn-metadata.json") + read("hn-extra-metadata.json")}
gh = read("github-metadata.json")[0]
questions = [q for q in old[:13]]

def requirement(target, position, polarity="positive"):
    return {"target": target, "polarity": polarity, "force": "must", "source_position": position}

def base(qid, pid, platform, summary, whole, i5, must, prefs, pos):
    return {"id": qid, "platform_id": pid, "platform": platform, "cohort": "new", "summary": summary,
            "whole_or_part": whole, "I5": i5, "must": must, "preferences": prefs, "source_position": pos,
            "coder": "worker / internal separate sampling agent (same model family)", "full_body_stored": False,
            "selected": True, "date_confirmed_in_direct_source": True}

questions[4] = base("N005", "95499", "softwarerecs",
    "Serve a personal static blog and small projects securely with a simple extensible web server. It must handle HTMX full/partial responses without a separate application server and run on Linux. Alpine, Windows development and no cost are preferences.",
    "part", "present", [requirement(x, "initial body ordered requirements 1-5") for x in ["secure defaults or easy hardening", "serve static files", "HTMX-aware or extensible without separate application server", "as simple/minimalist as possible", "Linux"]],
    ["Alpine Linux", "Windows development or Docker", "free"], "initial body ordered requirements 1-6")
questions += [
    base("N014", "95711", "softwarerecs", "Find a lightweight FAQ engine for Windows Server with headings, bodies, keywords, categories and attachments. Browsing/search should work without login; editing needs authentication, which may be added. Prefer PHP/MySQL and free or inexpensive one-time pricing; SSO is optional.", "whole", "absent",
         [requirement(x, "initial body second list") for x in ["Windows Server", "headings, bodies, keywords, categories and attachments", "browse and search without login", "editing authentication, possibly added by asker", "free or low one-off cost"]], ["PHP and MySQL", "SSO"], "initial body two lists"),
    base("N015", "95481", "softwarerecs", "Modify delivered HTML attributes between browser and internet to let Archiveweb.page capture the original sold eBay listing. Browser userscripts failed. An HTTP(S) rewriting proxy or another effective solution is welcome; it should be documented and avoid requiring a whole Node.js ecosystem.", "part", "present",
         [requirement("modify response HTML before the browser consumes it, or otherwise solve the archive capture failure", "initial body paragraphs 1 and 4-10"), requirement("require a whole Node.js ecosystem", "initial body paragraph 3", "negative")], ["reasonable documentation", "any OS or proxy location"], "initial body paragraphs 1-10"),
    base("N016", "95473", "softwarerecs", "Find a JavaScript library function converting Bash associative-array source stored in a web application's OPFS into the corresponding native JavaScript object. The requested library license is AGPL3; answers should link code rather than reproduce it.", "part", "present",
         [requirement(x, "initial body input/output examples and final licensing paragraph") for x in ["JavaScript callable conversion from Bash associative-array source to native object", "AGPL3 license requested"]], [], "initial body examples and licensing paragraph"),
    base("N017", "50176420", "hackernews", "Replace Firefox on Android after a missing reload-button problem. Require privacy awareness, a usable interface, Google Play installation without building an alpha, and an accessible reload control.", "whole", "absent",
         [requirement(x, "question requirements bullets 1-4") for x in ["Android browser", "privacy aware", "user friendly", "Google Play installation without compiling an alpha", "reload control"]], [], "question body requirements bullets 1-4"),
    base("N018", "50109923", "hackernews", "Find a polished personal email alternative to Proton Mail with a native email application. Prefer modest pricing, a family plan and a custom domain; encryption is optional. Tuta is considered insufficiently polished.", "whole", "absent", [], ["native email app", "not too expensive", "family plan", "encryption optional", "custom domain nice"], "question body sentences 1-7"),
    base("N019", "50325635", "hackernews", "Find an open-weight alternative to the Claude Code workflow, whose terminal interface is used for coding and other tasks. The initial question does not distinguish the harness from its model; preserve that ambiguity rather than importing later clarification.", "whole", "present",
         [requirement("open-weight model alternative", "question title")], ["terminal interface", "coding and noncoding tasks"], "title and initial body"),
    base("N020", "2525", "github_discussions", "Find a local model for Hindsight retain with quality near gpt-oss-20b that runs entirely on an RTX 5060 with 8 GB VRAM, without CPU spill, using Windows and llama.cpp. The current gpt-oss-20b setup spills experts to CPU; candidate families may be smaller or denser.", "part", "present",
         [requirement(x, "question Hardware and Question sections") for x in ["local Windows llama.cpp inference", "fit 8 GB GPU memory without CPU spill"]], ["retain quality near gpt-oss-20b", "smaller or denser model"], "Hardware, Retain and Question sections")
]

for q in questions:
    q.update(selected=True, date_confirmed_in_direct_source=True)
    pid = q["platform_id"]
    if q["platform"] == "softwarerecs":
        m, r = se[pid], initial[pid]
        q.update(url=m["link"], date=datetime.datetime.fromtimestamp(m["creation_date"], datetime.timezone.utc).date().isoformat(),
                 date_basis="Stack Exchange API creation_date and initial revision creation_date", mode="initial_revision", version=r["revision_guid"],
                 revision_guid=r["revision_guid"], revision_number=1, original_fetch_url=r["fetch_url"],
                 revision_loader_url=f"https://api.stackexchange.com/2.3/revisions/{r['revision_guid']}?site=softwarerecs&filter=withbody",
                 original_success=True, initial_revision_recovered=True, sha256=r["text_sha256"], text_sha256=r["text_sha256"],
                 html_sha256=r["html_sha256"], word_count=r["words"], normalization=r["normalization"], source_date_caveat=None,
                 read_at_utc=r["read_at_utc"], answer_eligibility={"answer_count": m["answer_count"], "accepted_answer_id": m["accepted_answer_id"], "rule": "two answers or accepted/self-accepted asker reaction"},
                 planned_execution_input="original_initial_revision_question_only")
    elif q["platform"] == "hackernews":
        m = hn[pid]
        q.update(url=m["url"], date=m["created_at"][:10], date_basis="Algolia HN item created_at", mode="current_original", version="current; first revision unavailable",
                 original_fetch_url=m["fetch_url"], original_success=True, initial_revision_recovered=False, sha256=m["question_sha256"], text_sha256=m["question_sha256"],
                 html_sha256=m.get("question_html_sha256"), word_count=m["question_words"], normalization="se_v1_html_tag_regex_then_html_unescape_preserve_whitespace",
                 source_date_caveat="Publication date is verified; original question-time text cannot be reconstructed from this API.", read_at_utc=m["read_at_utc"],
                 answer_eligibility={"observed_comment_count":len(m["comments"]), "rule":"at least two substantive answers observed"}, planned_execution_input="summary_query")
    else:
        q.update(url=gh["url"], date=gh["date"][:10], date_basis=gh["date_basis"], mode="current_original", version="current; first revision unavailable",
                 original_fetch_url=gh["url"], original_success=True, initial_revision_recovered=False, sha256=gh["question_sha256"], text_sha256=gh["question_sha256"],
                 html_sha256=gh["question_html_sha256"], word_count=gh["question_words"], normalization=gh["normalization"], read_at_utc=gh["read_at_utc"],
                 source_date_caveat="Publication date is verified; edit history at question time was not retrieved.",
                 answer_eligibility={"comments":4,"replies":2,"asker_use_report":True,"rule":"two answers and asker reaction observed"}, planned_execution_input="summary_query")

cases = json.loads(subprocess.check_output(["git", "show", "478c301b693896e2c6d777f46ac441f071bfdfe8:docs/workstreams/research/AF-RES-011/CASES.json"], cwd=P))['cases']
def canonical(url):
    for plat, pat in [('softwarerecs', r'softwarerecs\.stackexchange\.com/questions/(\d+)'), ('hackernews', r'news\.ycombinator\.com/item\?id=(\d+)'), ('reddit', r'/comments/([a-z0-9]+)')]:
        m = re.search(pat, url)
        if m: return plat + ':' + m.group(1)
    return url.rstrip('/')
oldkeys = {canonical(c['url']):c['id'] for c in cases}
dups = [{'qid':q['id'],'old_id':oldkeys[canonical(q['url'])]} for q in questions if canonical(q['url']) in oldkeys]
assert not dups, dups
assert len(questions) == 20
counts = {p:sum(q['platform']==p for q in questions) for p in sorted({q['platform'] for q in questions})}
assert len(counts) >= 3 and max(counts.values()) <= 10
write('new-questions.json', questions)
write('dedup-and-selection.json', {'recorded_at_utc':now, 'fixed_cases_sha':'478c301b693896e2c6d777f46ac441f071bfdfe8','old_cases_checked':len(cases),'selected_count':len(questions),'platform_counts':counts,'duplicates':dups,
      'removed_duplicate':{'platform_id':'95480','old_id':'T019','replacement':'95499'},
      'excluded_after_body_read':[{'url':'https://github.com/vectorize-io/hindsight/discussions/4155','reason':'configuration/fit diagnosis rather than selecting software candidates'}, {'url':'https://github.com/vectorize-io/hindsight/discussions/2199','reason':'predominantly configuration troubleshooting'}, {'url':'https://github.com/orgs/community/discussions/196615','reason':'thread began 2026-05-22 before cutoff'}, {'url':'https://github.com/orgs/jellyfin/discussions/17211','reason':'database feature proposal, not original recommendation request'}, {'url':'https://news.ycombinator.com/item?id=50377058','reason':'eligible title-only alternative request retained as reserve; selected other questions with richer input'}],
      'reddit_status':'Seven directly-read supplementary threads excluded because absolute publication date lacks a direct-source confirmation beyond search metadata.',
      'sampling_limit':'Purposive availability sample, not random or representative; one GitHub repository supplies the third platform.'})
print(json.dumps({'questions':len(questions),'platform_counts':counts,'duplicate_count':len(dups)},ensure_ascii=False))
