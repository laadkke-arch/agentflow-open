# HANDOFF — AF-RES-200

- 실제 판정: **PARTIAL**. 두 사건×세 목적과 명세/구현·원결정 연결, 출처 유형별 하한 충족. 그러나 file-level Simple/JSON 원시값 접근 실패로 Q2 핵심 미충족. M post1 수정 발표/실제 fix 확인 결손. DONE으로 올리지 말 것. 자체 검토 완료, 독립 검토·실제 설치·pip 실행 없음. 현재 세션의 실제 모델 UI는 검증하지 않음.
- 시작 foundation c860f8240ab7b7077e2d5b63e438ddd83ff69a27, 계획 050278651b11a2a3a49d45baebf41c707c06b700 (ahead4/behind0, dot-control만 차이). assigned branch work/research-af-res-200; AF-RES-192 fixed 60704a5701d1ac1608954d339b5ef8e9e25bcbd2. dot-control blob parse로 실제 192 DONE/result SHA 및 200 RUNNING/dependency 확인. 192 자체 PARTIAL의 archive DOI 결손은 이번 scope 제외.
- **결과 직전 고정 SHA: ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc**. 대표: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/SELF_CHECK.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/sources.jsonl), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/frame.csv), [releases.csv](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/releases.csv), [notices.csv](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/notices.csv), [advice.csv](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/advice.csv), [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/COUNTEREXAMPLES.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/ba6b4d95919ea5e6d7be8d9c1f86c9ebc97d14cc/docs/workstreams/research/AF-RES-200/SCOPE.md).
- 고정 결과 readback: RESULT/SELF_CHECK/sources/releases/advice 다시 읽음; foundation compare ahead12/behind0, 9 files all owned_path, dot-control/index/common path unchanged. 중간 검사 c876dae5cff8d4edf2bc5159b5f215f89b478f42에서 44 unique JSONL IDs, CSV widths all good, 88 visible files + one deleted group placeholder, A01–A06, Q1–Q7, final weaknesses exactly 3. HANDOFF는 별도 최종 커밋.
- 자료: 28 직접 고유 work (release HTML 6/6, rule 6/4, maintainer 5/4, consumer 4/4, crossfield 7/4); 44 ledger rows, 16 excluded/failed/duplicate, 6 coarse lineage, 2 software + 2 publication incident. 유형별 수치 부족 0. file raw data 0/88 flags/reasons and exact upload UTC, target 0/26; version JSON 0/6, M Simple open failed, P Simple file names only (attr stripped). F15 curl DNS failure. 날짜 2024-08-05/03-04 current PyPI display; P Mar9 historical warning log; M exact first warning and historical deletion timestamp unknown. Exact retrieval UTC time not captured (task boundary Nov24/25).
- 핵심: M Windows wheel conditional crash, 삭제→Windows sdist fallback failure 확대→release yank; 24 남은 파일 vs adjacent29/29, Windows tags 0 vs 5/5. Maintainer says sdist/macOS/manylinux functional, downstream builds not yank; musl effect unknown. P plugin legacy path hooks, two API removals restored in 8.1.1, private call_runtest_hook not restored; exact 8.1.0 cached wheel install warning/success observed Mar9. Exact pins are not wildcard, post1 ≠ exact base. A retained artifact may be usable even when new candidate omitted. Six-row advice: new range compatible candidate first, historical/exact original first with dated contextual warning/optional explicit repin, no silent history rewrite. No final DB/product choice.
- **첫 재개 행동:** Codex Cloud 공개 HTTP read-only 환경에서 아래 여섯 version JSON, 두 Simple JSON을 조회하고 파일명 기준 join. HTTP/parse failure 보존, 접근 우회 금지. raw flag 차이와 reason/UTC 업로드 값을 수정 원장에 기록. 현재 flag는 historical change time이 아님. 이어 M01 linked maintainer comments, F11 post1 announcement/tag, historical deleted file list와 existing consumer logs만 확인. 실제 설치/pip 실행 금지. 날짜/파일/repair evidence 뒤집히면 구값과 원자료 및 변경 이유를 별도 커밋. 
- 색인 반영 제안(편집 담당자): AF-RES-200 / PyPI yanked 배포 파일의 목적·환경·버전제약별 경고/대체 / PARTIAL / docs/workstreams/research/AF-RES-200/RESULT.md / AF-RES-192 60704a57... / 핵심 분기와 당시 소비자 근거 있음, per-file raw flags/repair evidence 미확인. dot-control과 index 직접 수정하지 않음.

## 재개 명령과 입력 (미실행)

Codex Cloud의 일반 공개 인터넷/기존 curl·Python3 표준 라이브러리. 유료 API·로그인·권한 우회·설치 금지. 원자료는 /tmp, Git 변경은 owned_path만. 다음 명령은 공개 metadata 조회/검산이지 새 설치가 아니다. 실행 불가 시 HTTP status/error 및 다음 진입점 기록.

```sh
git fetch origin
git checkout work/research-af-res-200
git rev-parse HEAD
git diff --name-only c860f8240ab7b7077e2d5b63e438ddd83ff69a27..HEAD
ROOT="$(git rev-parse --show-toplevel)"
OUT="$(mktemp -d /tmp/af-res-200.XXXXXX)"
export ROOT OUT
date -u +%FT%TZ > "$OUT/retrieved_at_utc.txt"
for spec in matplotlib/3.9.0 matplotlib/3.9.1 matplotlib/3.9.1.post1 pytest/8.0.2 pytest/8.1.0 pytest/8.1.1; do
  file="$(printf '%s' "$spec" | tr '/' '_')"
  date -u +%FT%TZ > "$OUT/$file.time"
  curl -fLsS --max-time 30 -D "$OUT/$file.headers" \
    -o "$OUT/$file.json" "https://pypi.org/pypi/$spec/json" \
    2>"$OUT/$file.error" || printf 'FAILED %s\n' "$spec"
done
for proj in matplotlib pytest; do
  date -u +%FT%TZ > "$OUT/$proj-simple.time"
  curl -fLsS --max-time 60 \
    -H 'Accept: application/vnd.pypi.simple.v1+json' \
    -D "$OUT/$proj-simple.headers" -o "$OUT/$proj-simple.json" \
    "https://pypi.org/simple/$proj/" \
    2>"$OUT/$proj-simple.error" || printf 'FAILED %s Simple\n' "$proj"
done
python3 - <<'PY'
import csv, json, os
from pathlib import Path
out = Path(os.environ["OUT"])
root = Path(os.environ["ROOT"])
with (root/"docs/workstreams/research/AF-RES-200/releases.csv").open() as f:
    expected = list(csv.DictReader(f))
expected = [r for r in expected if r["listing_status"] == "listed"]
for project, version in sorted({(r["project"], r["version"]) for r in expected}):
    path = out/f"{project}_{version}.json"
    want = {r["filename"] for r in expected if r["project"] == project and r["version"] == version}
    try:
        data = json.loads(path.read_text())
        files = {f["filename"]: f for f in data["urls"]}
    except (OSError, ValueError, KeyError) as e:
        print(project, version, "UNREADABLE", repr(e))
        continue
    print(project, version, "HTML_COUNT", len(want), "JSON_COUNT", len(files),
          "MISSING", sorted(want-files.keys()), "EXTRA", sorted(files.keys()-want))
    for name, f in sorted(files.items()):
        print(json.dumps({"project": project, "version": version, "filename": name,
            "packagetype": f.get("packagetype"), "yanked_present": "yanked" in f,
            "yanked": f.get("yanked"), "yanked_reason": f.get("yanked_reason"),
            "upload_time_iso_8601": f.get("upload_time_iso_8601"),
            "requires_python": f.get("requires_python")}, ensure_ascii=False))
    try:
        simple = json.loads((out/f"{project}-simple.json").read_text())
        sfiles = {f["filename"]: f for f in simple["files"]}
    except (OSError, ValueError, KeyError) as e:
        print(project, "SIMPLE_UNREADABLE", repr(e)); continue
    for name in sorted(want):
        s = sfiles.get(name)
        print("SIMPLE", name, "ABSENT" if s is None else json.dumps({
             "yanked_present": "yanked" in s, "yanked": s.get("yanked"),
             "upload_time": s.get("upload-time"), "requires_python": s.get("requires-python"),
             "version_JSON_yanked": files.get(name,{}).get("yanked")}, ensure_ascii=False))
PY
```

기대 관측(가설, 실제 값 아님): HTML에서 확인한 24/29/29 및 2/2/2 파일명 join 일치; 대상 release banner와 실제 per-file 표시 일치 여부, raw reason의 정확한 단위 및 JSON vs Simple string/boolean 구분. 한 파일이라도 다르면 기록 수정, 전부 일치해도 과거 flag timestamp로 소급하지 않음. 미존재 필드와 false를 구별. Wheel tag는 filename에서 파싱하되 비교 실제 API filename 기준. 삭제된 Windows wheel 과거 이름·수는 현 JSON 부재만으로 복원 불가. 별도 원문 [M01](https://github.com/matplotlib/matplotlib/issues/28551) / [post1 tag](https://github.com/matplotlib/matplotlib/releases/tag/v3.9.1.post1) 및 당시 기록 탐색. pip 24.0 [factory](https://github.com/pypa/pip/blob/24.0/src/pip/_internal/resolution/resolvelib/factory.py#L304-L325), [tests](https://github.com/pypa/pip/blob/24.0/tests/functional/test_install.py#L2176-L2288)은 문헌 수준 확인 완료, 추가 실행 요청 없음. Contract/session 실행형 검사는 현재 환경에서 미실행이며 다음 작업자가 저장소 기존 규칙을 읽고 수행할 수 있음; 이미 수행한 것처럼 기록하지 않는다.

결과를 업데이트하면 source counts, frame/ledger, files/notice/advice, RESULT/SELF_CHECK 재검토 후 마지막 새 HANDOFF commit. 원시값·M post1 수정 범위 확인 전에는 PARTIAL 유지.
