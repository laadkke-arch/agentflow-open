# AF-RES-148 HANDOFF — PARTIAL

- worker: web-pro single context; 실제 작업은 GitHub connector 및 공개 웹 원문 직접 열람, JS 표/해시 검산. 별도 3개 독립 판독 세션 생성 도구 없음. 사용자에게 질문하지 않음. 실제 실행/검사는 원격 읽기 검산만.
- acceptance: **PARTIAL**. 6 provisional events, 6 current snapshots, 18 draft packets, 18 planned allocation rows, 18 not_executed readings, 0/18 actual independent readings, 0/6 confirmed first revisions, 0/6 valid paired experimental comparisons. Q3/7/causal claim not closed.
- sources 38 ledger rows: opened substantive 32 unique work IDs, description-only 1, failed 5. Quota candidates 23 = 6 request, 8 tech, 6 independent, 1 text, 2 music. Required type-capped coverage 21/24, text deficit 2, music deficit 1; stricter common lineage counting may reduce further. Current-body source is not first revision. 6 snapshots actual re-open UTC, older source observation times only session intervals, not fabricated seconds. Folger original Q2 and F1 human verification prevented access; no bypass; score+part exact bar comparison absent. No empirical ratios where denominator 0, no user response rate or time savings.
- provisional product finding: choose minimal original request+selected range+revision+explicit preservation constraints; permit optional bounded related producer/consumer evidence if actually connected and distinguish from inference. No experimental evidence that optional context improves route selection. Mustache, text edition and instrument transposition refute treating visible form as sufficient identity. E4 mismatched functions, E6 patch leakage, E5 compiler unverified.

## Scope and remote verification

Repository laadkke-arch/agentflow-open. Planned base 9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673; actual integration at start 97a1e63cb48ff4900984104e1d2a3760f324eb79, ahead 3 only dot-control changes, branch created from actual. Read AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, central blob ca510baf19a8b34ef45c92f4ad33206e551e3dbf, product RESEARCH_BRIEF; AF-RES-144 depends_on verified at central DONE, fixed HANDOFF 92833407f665a6e28e4292491c261b7e0725c69c and RESULT ad394b702f077bc367b879e4d055fdc76016d0b6 read. Did not rerun 140/144 CSV/YAML or change central control.

| bundle | actual remote commit and representative file re-opened |
|---|---|
| ① rules before external recruitment | 3faeb1fc3e3c209267bf5d3e920a7ce346e18220 SCOPE.md, verified identical |
| ② frame | 09ff021a403e36265ead89056211b543083f75c2 frame.csv, separate CSV repair 0855dd7dd385e3384462f770f51d2a6ab206452e, verified |
| ② original body snapshots and draft inputs | acfa20aff91c9a7ea4256c18fb58b14681e6e753 request-snapshots.jsonl; 0035ba52bbb098f2e541430e6d8aa40da2a4f760 packets.jsonl; verified |
| ③ blocked observations, not fabricated | b1ebe0bfb9efaeba187b9600d27560f5e5b27b34 allocation.csv; f6a3f4178acdf119375a4ae4a0219bf59a7867ad readings.jsonl; a1d70c93a040024d130c61c2cde56dcad35ec70b author-evidence.csv; verified |
| ④ direct source ledger and contrast | ce5c360c4cb2b4c5711603236971716beac465bc sources.jsonl; d0f8854d22290de98e1dc0537aa54b384dfabdc6 supplemental ledger; 41e21ef915682342231b4d35e8a1268dfe1e525a comparisons.csv; 613430f072324626a1fc1407c545f8902c70200a E2 count correction; e4a51517effbf7dd9c80cd34d068f1a71faf4008 contracts.json; verified |
| ⑤ result and check | cde2c875e2ebf57bf1c161c2bee9f5f5ff6d75aa RESULT.md; da7d87dbb42963b76d55f76a0ba4735e8ddd383e SELF_CHECK.md; verified |
| last | HANDOFF.md only; result commit is the commit containing this file (cannot embed its own SHA in content) |

At da7d87dbb42963b76d55f76a0ba4735e8ddd383e remote compare against 97a1e63cb48ff4900984104e1d2a3760f324eb79: ahead 15, behind 0, 12 files all under owned_path; no dot-control changes. At same fixed ref re-opened sources/frame/packets/readings/RESULT; exact counts 38/60/18/18; RESULT starts three required tables and ends exact three weaknesses. No external file writes. Separate commits via contents API directly modify remote (no local push needed).

## 다음 첫 행동 — recruitment and independent execution

1. On a new checkout, fetch existing branch; do not recreate/rebase it. Keep the previous frame and exposed drafts, mark correction as a new revision. Raw REST search returns both issues and PRs (do not reuse separate tool search with missing created_at); record complete current data and actual created clocks. Use only public data within limits.
~~~sh
git fetch origin chore/workspace-foundation work/research-af-res-148
git switch --track origin/work/research-af-res-148
git rev-parse HEAD
git diff --name-only 97a1e63cb48ff4900984104e1d2a3760f324eb79...HEAD
for r in jgm/pandoc prettier/prettier; do
  gh api --method GET search/issues -f q="repo:$r created:2024-01-01..2025-12-31" -f sort=created -f order=asc -F per_page=30 -F page=1 --jq '.items[] | [.number,.created_at,.updated_at,.html_url,(has("pull_request")), .title] | @tsv'
done
gh api repos/jgm/pandoc/issues/9296
gh api repos/jgm/pandoc/issues/9305
gh api repos/jgm/pandoc/issues/9308
gh api repos/prettier/prettier/issues/15853
gh api repos/prettier/prettier/issues/15868
gh api repos/prettier/prettier/issues/14234
gh api repos/prettier/prettier/pulls/15870/commits --jq '.[] | {sha,parents:[.parents[].sha],date:.commit.author.date}'
~~~
If local branch already exists use git switch work/research-af-res-148 and check exact remote match. Review current issue edit history/first revision where publicly available. If fewer than 3 eligible in first 30, repeat page=2 only. Sort tied created_at by number. If first PR version is irretrievable, don't manufacture it; record current revision and eligibility gap. E1 attachment URL from R01; E4 get same function as actual/expected, not invented; E6 original issue and first PR parent. Store access status and exact timestamp for each re-open. For workbench session manifest, inspect repository workbench instructions and execute session start/check only if supported by that fixed base, preserving previous commits; not run here.

2. Rebuild actual matched B/C (directly related and unrelated sibling, same ≤800 codepoint budget, cut positions). Preserve original exact artifact and provenance. Separate audit vault (snapshots/expected) and reader packet (opaque ID and only permitted original excerpts; no answer-bearing links). Independent fresh contexts R1,R2,R3 need actual executor support: E1 A/B/C→R1/R2/R3; E2→R2/R3/R1; E3→R3/R1/R2; repeat for E4–6. Reader prompt: choose exactly one direct link/conditional link/one discriminating question/defer, max two contemporaneous official technical sections, log actual open URL, time, output hypothesis, A/B different recommendation or mark unnecessary, prior exposure. Record actual sessions and seal each answer before collector discloses expected. Do not feed this RESULT or HANDOFF to those readers. If no isolated contexts available, remain PARTIAL and never fill missing rows with collector answers.

3. Replay candidate technical gates only in approved disposable environment. Exact inputs in request-snapshots. E2 write author table.md then run Pandoc 3.1.11 `pandoc -t plain table.md`, inspect first/second cell text; compare author-reported removing pre (separate modified input); E3 write code.md from R03 including opening javascript hl_lines="1" fence and run `pandoc -t plain code.md`, then `pandoc -f commonmark -t plain code.md` and brace-attribute version (mark researcher-created); compare code literal, not assumed highlight. E5 write two class A variants separately; exact TS version still unknown, choose explicitly labelled reference TypeScript 5.3.3 if original not available, run `npx --yes --package typescript@5.3.3 tsc --noEmit --pretty false a.ts` then b.ts separately; compare diagnostics and if legal actual emit (use explicit compiler options). E6 use GraphQL 16.8.1 parse of both stable/main union excerpts with full member list; inspect AST types, then separate schema validation (duplicates and absent type definitions). For E4 get actual same function and resolved eslint configuration first; do not declare fix from unrelated addCartItem. Do not install packages or perform local product mutation without approval; commands are handoff inputs, not executed results.

4. Text original: Folger links F04/F05 hit human verification, use authorized institutional source or openly accessible original edition, locate Hamlet 1.2.133 same passage and compare Q2 vs F1 with independent editing documentation. Music: KV498 Mutopia 2014 ID250 ZIP source/PDF (D03), open actual score and clarinet and violin replacement part with same movement/bar; record notated pitches, transposition and concert pitch; source edition/part lineage grouped. D02 XML example is not actual score. Additional unrelated substantive first-party works to satisfy text 3 and music 3; do not count listing or blocked scans.

## 재검산 명령 (미실행; GitHub remote count check above was actually performed)

Run at fixed result checkout before making changes. Python default ASCII escaping differs from JS payload serialization, use ensure_ascii=False and separators as below. Snapshot body hash uses exact CRLF preserved in JSON string, packet excerpts are LF-normalized. The comparison includes stored packet payload hashes; it cannot authenticate historical first revisions or prove lack of leakage.
~~~sh
python3 - <<'PY'
from pathlib import Path
import csv, json, hashlib, collections
d=Path("docs/workstreams/research/AF-RES-148")
def jl(n): return [json.loads(s) for s in (d/n).read_text().splitlines() if s]
def cr(n):
    with (d/n).open(newline="") as f: return list(csv.DictReader(f))
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
sources, packets, reads, snapshots = map(jl, ("sources.jsonl","packets.jsonl","readings.jsonl","request-snapshots.jsonl"))
assert len(cr("frame.csv"))==60
assert len(cr("allocation.csv"))==len(packets)==len(reads)==18
assert len(cr("author-evidence.csv"))==len(cr("comparisons.csv"))==len(snapshots)==6
assert all(sha(x["body"])==x["body_sha256"] for x in snapshots)
by_id={x["eid"]:x for x in snapshots}
for x in packets:
    assert x["source_body_sha256"]==by_id[x["case_id"]]["body_sha256"]
    assert sha(json.dumps(x["payload"], ensure_ascii=False, separators=(",",":")))==x["payload_sha256"]
    assert len(x["payload"]["extra"] or "")==x["extra_chars"]<=800
assert len({(x["case_id"],x["face"]) for x in packets})==18
assert sum(x["ready_for_blind"] for x in packets)==0
assert sum(x["status"]=="not_executed" for x in reads)==18
assert len(sources)==38
assert len({x["work_id"] for x in sources if x["access"]=="opened"})==32
n=collections.Counter(x["category"] for x in sources if x["counts_toward_category_minimum"])
print(n, "type_capped", sum(min(n[k],v) for k,v in {"request":6,"technical":6,"independent":6,"text":3,"music":3}.items()))
print("scores: NA, independent observations 0/18")
PY
git status --short
git diff --name-only 97a1e63cb48ff4900984104e1d2a3760f324eb79...HEAD
~~~
Expected count output type_capped=21, no independent observations; exact hash assertions not yet run with Python. Earlier JS SHA-256 implementation matched abc known test vector, all file contents returned identical after commit. If mismatch, record rather than overwrite first sealed artifact. Final acceptance requires actual first-revision eligibility, independent 18 readings, data origin/type floors and sensitivity recomputation. Central status is coordinator-managed; do not edit it.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
|---|---|---|---|
| 생성순 합집합 불확정 및 최초판 0/6; E1 첨부 미열람, E6 원이슈·최초 커밋 결측 | 첫 3건 선정 및 기대값 독립성 보장 불가 | raw GitHub search/issues 생성순, 개별 생성시각·edit history, #14234 및 #15870 첫 commit parent, E1 첨부 | 실제 최초 30개 순서와 적격 3건씩 재현, 동일 판의 원요구·입력·기대값 확인 |
| 독립 판독 0/18, 완전한 동일 길이 후보는 E4 1/6뿐이며 수집자 선노출 | 이웃의 효과·오승인·질문 감소·시간 절약 및 우월한 계약을 실증할 수 없음 | 실제 세 독립 문맥에 라틴 배정; 원본/기대 접근 분리; 짝 전부 실제 이웃/무관 구간 확보 | 봉인 후 개봉한 18개에서 같은 사건 A/B/C 전환 및 오답을 비교, 노출·결측 제외 재집계 |
| E4 다른 함수, E5 컴파일 미확인, E6 문법과 유효 스키마 구별; 판본 원면 0/2 및 실제 총보·파트 0쌍 | 표현/값 동일성의 과잉 확신 위험; 외부 분야 하한 및 실제 원자료 비교 미달 | 같은 함수/버전 리플레이, TypeScript 진단·emit, GraphQL AST/validation, Folger 허용 접근, Mutopia KV498 실제 총보와 대체 파트 | 원입력과 결과의 의미/표현 분리 검증 및 원면·동일 마디 비교가 반례를 확인하거나 뒤집음 |
