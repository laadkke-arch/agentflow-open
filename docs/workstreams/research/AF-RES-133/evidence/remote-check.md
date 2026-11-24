# 원격 검사 영수증 (정식 CLI check 아님)

- 확인 UTC 2026-11-24 (day precision); 고정 검사 입력 6bb60c2debc182aa6656948e2b337e67c4ae31a6; base 67eb3c65404bf70de554bee6eb4c126344a3cd4a.
- GitHub compare base...input: status ahead, ahead_by 12, behind_by 0; changed paths 10; all_owned=true.
- 비교 경로:
- docs/workstreams/research/AF-RES-133/RESULT.md
- docs/workstreams/research/AF-RES-133/SCOPE.md
- docs/workstreams/research/AF-RES-133/SELF_CHECK.md
- docs/workstreams/research/AF-RES-133/contracts.csv
- docs/workstreams/research/AF-RES-133/events.jsonl
- docs/workstreams/research/AF-RES-133/evidence/hunks-and-corrections.md
- docs/workstreams/research/AF-RES-133/evidence/supplement-frame-frozen.csv
- docs/workstreams/research/AF-RES-133/evidence/supplement-frame.csv
- docs/workstreams/research/AF-RES-133/frame.csv
- docs/workstreams/research/AF-RES-133/sources.jsonl
- 고정 검사 입력에서 대표 파일 7개 재열람 성공 (blob SHA):
```text
SCOPE.md e30e52c35ff2d426703080f6993b8c360446e820
frame.csv c53da7b5b47f507321ce226802d3440aec6e11f6
events.jsonl 45a7f43a706d253d2f98f22825d1dcf43411fbed
contracts.csv 77318fe90b2f43a9162a83896dfd917267c92a41
sources.jsonl b4b8b6f5c9e7cbdb48aa7bf9f2e4c2e33938cca7
RESULT.md cf2f494a53a64703d1940b0b69aaeebfd3f9b9d7
SELF_CHECK.md 92a069dea7f6a0447541b96c63623244506bda7f
```
- RESULT 고정 SHA 957fffbe6991cef2c5b78f792bd5ea603b1139cd에서 frame 72 unique, 1043 returned comments, events 15 unique, contracts 15, sources 108 (104 successes / 4 failures, 35 counted unique) 재계산; SELF_CHECK.md에 세부 분모 기록. 9 paths checked at result, 10 paths at self-check input. 이 검사는 JSON parse 및 CSV row/unique/order 확인, 원격 경로 검사에 한정된다. 외부 URL 전체 재열람과 판독 검증은 아님.
- 실제 로컬 시도:
```sh
git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/work/research-af-res-133
```
  stdout 없음; stderr 요지 Could not resolve host: github.com; 종료값 128. checkout 기반 manifest 생성/정식 검사에 이 결과를 성공으로 기록하지 않는다.
- 아래는 **미실시 명령** (stdout/stderr/exit 없음, 실행 안 함). 실제 checkout에서 배정 브랜치의 manifest 유무·base 및 129 의존 대조 후 없을 때만:
```sh
python -B -m workbench.session start af-res-133 --allow docs/workstreams/research/AF-RES-133/ --dependency work/research-af-res-129=86369e7091b3cb58bbea1e3277bee67967afeaa6 --output docs/workstreams/research/AF-RES-133/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-133/manifest.json --fetch
```
- 첫 재개: authenticated checkout에서 배정 브랜치 원격 HEAD와 SCOPE 고정 base/dep 확인. 기존 commit 보존하고 중앙 변경 금지. 72 frame 번호 기준 별도 읽기 (예: #9580 및 대형 #9618) 다음과 같이 pagination:
```sh
repo=pydata/xarray; pr=9618
gh api --paginate "repos/$repo/issues/$pr/comments?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/reviews?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/comments?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/commits?per_page=100"
# inline JSON의 original_commit_id, path, original_line, diff_hunk, in_reply_to_id 보존
# commit sha와 부모 tree 및 동일 조작 첫 hunk 확인: gh api "repos/$repo/commits/$sha"
```
- issue body edits/history는 GraphQL timeline 및 공개 수정 이력에서 확인; API가 반환하지 않으면 결측으로 남긴다. scikit-image도 동일 작업. 원래 SHA 및 Q7 immediate correction판 확보. 이후 새 검사의 실제 명령/stdout/stderr/exit 및 check 대상 SHA를 owned evidence에만 저장. 별도 세션 검토 미실시.
