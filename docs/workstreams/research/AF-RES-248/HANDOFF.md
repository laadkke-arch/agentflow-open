# HANDOFF — AF-RES-248
**자체 상태: PARTIAL.** 직접 자료 수/분류 하한은 충족(32 counted, 8/9/7/6/2; 최소 5/6/5/3/2). 9개 주셀의 전체 PyPI HTML 표를 끝까지 관측하고 당시판 정책/태그 정의와 분리했으나, 필수 raw JSON 0/3, file-specific requires_python/정확 업로드 UTC 미확인, exact release tag의 목표 wheel 시험 receipt 0/9. 현재 표시 5 positive / 4 no match는 raw JSON/과거 미게시/설치 성공이 아니다. 사용자의 지정 핵심 조건이 비었으므로 DONE 주장하지 않는다. 설치 실험 및 펌웨어 적용 0회. 독립 검토 미실시; 자체 점검과 구분.

## 고정 입력과 결과 SHA
- 통합 시작 4bb9938d31fe7c2bbf97a14c585f4db1fac56717. 계획 7369707441e2eb70e84004ca6cb3bfeefc8b4061에는 248 없음; 최신 진행표 blob 58343d6af38a7c3dd011acec895c4b9b3d4ea7b7로 RUNNING/AF-RES-235 dependency 확인. 235 중앙 DONE, 자체 PARTIAL, 고정 5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126 HANDOFF/RESULT/timeline/consumer 읽음. 238–242 결과 미사용.
- 작업 브랜치 work/research-af-res-248 / docs/workstreams/research/AF-RES-248/만 편집. dot-control.json 변경하지 않음.
- ① 사전 봉인 d974501f90a5c233ade95b6f39dde2fd7de4f8f2.
- ② 직접 원자료 원장 8d0a1cb0996f1493cc97fc64457edccc83c301be.
- ③ matrix ada2639974cd0c69c9cb20e03f5f96d3000610cc; events 79b71a1913124ac32a13721f9cf57fa11f02b407; TABLES f98bcad9dd6fcecbbb15adc7babc0bd953bc1ff0.
- ④ source corrections 89ab76dcfa86996a68748d1288fc0c87eb7f9b76; recommendations 3202b5152e36ac018c547cfccef2a2ff9032907b; events correction f2021c24f7078e952dbbeb74cd9361da32d04100.
- ⑤ RESULT 764f92786036a749886740b25b5ef7ed009f47eb; SELF_CHECK 및 고정 **결과 SHA b55e3a7a283076085b09e70fbb4eacbdc3ae92fd**.
- ⑥ 이 HANDOFF.md는 마지막 단독 커밋; result SHA와 HANDOFF commit 구별.

## 핵심 판단
1. 1.13.1은 3.9/3.10 Linux glibc x86_64 wheel 표시, 3.13 0 표시. 1.14.0은 3.10 wheel 표시, 3.9 최소 조건 위반, 3.13 하한 통과하지만 0 표시. 1.14.1은 3.10/3.13 wheel 표시, 3.9 하한 위반. 3.13 지원 명시 및 wheel 추가 vs classifier 3.12까지만: 정책/파일/metadata 개별 근거 필요. 1.14.0 개발 지원 예정/밤빌드 보고는 stable release wheel과 다름. 
2. 게시 날짜만으로 공지/파일 시각 순서 및 역사적 삭제 여부 결정 금지. glibc 최소 2.17, pip tags, ABI; ordinary cp313 != cp313t. macOS arm64 12+/14+ 별도. sdist ≠ 소스 빌드 성공.
3. B2/B5/B6 개발 빌드/시험 실제 보고는 환경·SHA 차이. 3.13 free-threaded macOS test failure는 1.14.1 GIL Linux 결과 아님. Nikon D850 및 Z6II 모델/기존 C firmware 조건과 다운로드 host Windows/Mac 별도 축.
4. 과거 인용은 old file URL/digest/시간/환경 유지, 신규 답은 현재 지원/정확 artifact 확인 후 선택. 1.14.1을 오늘 최신이라고 자동 추천하지 않음.

## 고정 결과 재열람 및 자체 점검 (실제로 수행)
GitHub fetch_file(ref=b55e3a7a283076085b09e70fbb4eacbdc3ae92fd) 8개 모두 본문 확인: SCOPE.md (837a2f2d34f94eef59820f2065a0896fcb4b8081), sources.jsonl (eb252b2b86da3c8dd9ab0254db8f4567a6fc85ab), matrix.csv (1b02376181f8cb1db6f8dcab2fedc3233a6cc1b1), release-events.csv (7276b731252d0f25afbcc92646834afb0c1bb459), TABLES.md (38450824654d9450d205dbe549c12aaa9f3dc959), recommendations.md (ec3644cea82eed00463a0ccba5b448ea416d5ac6), RESULT.md (87e3c0ada0d7b8c051bd929f7118857a9bfc724f), SELF_CHECK.md (31513cb087a2d5ef1ec620230deae57b4787c006).
- JSONL parse 50/50, unique ID 50, counted 32, lineage 19, failed 8 (J1–J3/D1–D5), category 8/9/7/6/2; 9 작업용 사건군(통계적 독립 주장 안 함).
- CSV matrix 27 unique rows/24 columns, width mismatch 0; main 9 (5 displayed present, 4 no match), sdist 3, mac-control 12, free-threaded 3; events 29 rows/8 columns width mismatch 0; matrix/events source IDs missing 0.
- RESULT first two required table headers exact: 9/8 rows, widths 6/5; last 3 rows width4; Q1–Q7 모두 RESULT/SELF_CHECK 존재. TABLES prefix 동일. 5 positive URLs matrix/RESULT/D-source 일치, filename suffix/64-hex SHA256 형식 정상. 실제 bytes 링크 재검증은 미실시(앞서 binary open 실패).
- compare base→result ahead=10, behind=0, 파일 8개 모두 owned_path added. 다른 경로/진행표 변경 없음. 외부 원자료 재열람은 초기 조사와 ④ 반례 단계에서 수행, 최종 SHA 재열람은 저장된 근거/행/주소 형식 대조; 모든 live source를 재요청하거나 실행 검사를 한 것은 아님. workbench CLI 미실시(직접 저장소 실행환경 없음).

## 다음 첫 행동 (raw JSON 원문이 접근되는 허용된 환경에서)
우선 다음 입력을 네트워크 가능한 실행 담당에게 전달. 이 세션에서는 raw web DisabledError 및 curl DNS 실패. 아래 명령 **미실행**; 설치하지 않고 JSON 및 체크 원문만 읽는다. repo checkout에서 owned_path로만 저장. HTTP 실패 시 stderr/status 기록, 빈 배열로 치환 금지. 
```sh
cd /path/to/agentflow-open
git fetch origin
git checkout work/research-af-res-248
git rev-parse HEAD
p=docs/workstreams/research/AF-RES-248
mkdir -p "$p/receipts"
for v in 1.13.1 1.14.0 1.14.1; do
  date -u +%FT%TZ > "$p/receipts/pypi-$v.time"
  curl --fail --location --show-error --connect-timeout 20 --max-time 90 \
    -D "$p/receipts/pypi-$v.headers" \
    -o "$p/receipts/pypi-$v.json" "https://pypi.org/pypi/scipy/$v/json" \
    2>"$p/receipts/pypi-$v.stderr" || echo "UNOBSERVED $v"
done
python - <<'PY'
import json, hashlib, pathlib, datetime
p=pathlib.Path("docs/workstreams/research/AF-RES-248/receipts")
for v in ("1.13.1","1.14.0","1.14.1"):
    f=p/f"pypi-{v}.json"
    try:
        raw=f.read_bytes(); j=json.loads(raw); a=j["urls"]
        assert isinstance(a,list) and j["info"]["version"]==v
        out={"version":v,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "response_sha256":hashlib.sha256(raw).hexdigest(),"file_count":len(a),
             "info_requires_python":j["info"].get("requires_python"),
             "classifiers":j["info"].get("classifiers"),
             "files":[{k:x.get(k) for k in ("filename","packagetype","requires_python","upload_time_iso_8601","url","digests","yanked","yanked_reason")} for x in a]}
        (p/f"pypi-{v}-inventory.json").write_text(json.dumps(out,ensure_ascii=False,indent=2))
        for x in a:
            print(v,x["filename"],x.get("requires_python"),x.get("upload_time_iso_8601"),x.get("digests"),x.get("url"))
        # Inspect every filename and all expanded interpreter/ABI/platform tags, including abi3.
        # Use pre-existing packaging if available (no install); compare exact environment tags.
        try:
            from packaging.utils import parse_wheel_filename
            from packaging.tags import cpython_tags, compatible_tags
            from packaging.specifiers import SpecifierSet
            # reference baseline glibc 2.17; re-run for actual newer/older glibc, pip and host tags.
            plats=["manylinux_2_"+str(i)+"_x86_64" for i in range(17,4,-1)]+["manylinux2014_x86_64","manylinux2010_x86_64","manylinux1_x86_64","linux_x86_64"]
            for minor in (9,10,13):
                cp="cp3"+str(minor)
                supported=set(cpython_tags(python_version=(3,minor),abis=[cp],platforms=plats)) | set(compatible_tags(python_version=(3,minor),interpreter=cp,platforms=plats))
                cand=[]
                for x in a:
                    if not x["filename"].endswith(".whl"): continue
                    tags=parse_wheel_filename(x["filename"])[3]
                    if not (tags & supported): continue
                    rp=x.get("requires_python")
                    # sample CPython final 3.minor.0; re-evaluate exact patch/prerelease.
                    gate=None if rp is None else SpecifierSet(rp).contains(f"3.{minor}.0")
                    cand.append({"filename":x["filename"],"file_gate":gate,"tags":[str(t) for t in tags & supported],"yanked":x.get("yanked"),"digest":x.get("digests"),"upload_time":x.get("upload_time_iso_8601")})
                print("CELL",v,minor,json.dumps(cand))
        except ImportError:
            print("tag library unavailable; no install; manually inspect all expanded tags")
    except Exception as e:
        print("UNOBSERVED",v,repr(e))
PY
```
예상(HTML 기반): 배열 수 25/25/33, 5 exact/4 no match, 3.13 후보 1.14.1 only, lower bound >=3.9/>=3.10/>=3.10; per-file metadata/정확 UTC는 미확인 예상으로 강제하지 않는다. 배열 count/태그/조건/digest/date 차이면 원행 보존하고 정정 커밋. 원 JSON 전체 bytes+headers+capture UTC+해시를 영수증 단위로 남김; HTML과 중복 집계하지 않음. glibc baseline 2.17은 샘플 비교를 위한 임시 입력이며 정확 환경 미지정. 3.13t는 별도 ABI 및 환경 tags, macOS 12/14 별도 tags. file metadata 읽기는 원 JSON 및 가능하면 공개 PEP 658 metadata endpoint에서 하고 설치/실행하지 않는다. raw array 현재 0이라도 과거 삭제 없음으로 단정 금지. 당시 snapshot, public publication log, release asset 기록 대조. 

다음으로 공개 GitHub exact SHA 및 공지 raw fields: 
```sh
p=docs/workstreams/research/AF-RES-248/receipts
for v in 1.13.1 1.14.0 1.14.1; do
  curl -fSL --max-time 90 "https://api.github.com/repos/scipy/scipy/releases/tags/v$v" -o "$p/release-$v.json" || echo "UNOBSERVED $v"
done
for sha in 44e4ebaac992fde33f04638b99629d23973cb9b2 87c46641a8b3b5b47b81de44c07b840468f7ebe7 92d2a8592782ee19a1161d0bf3fc2241ba78bb63; do
  curl -fSL --max-time 90 "https://api.github.com/repos/scipy/scipy/commits/$sha/check-runs?per_page=100" -o "$p/checks-$sha-page1.json" || echo "UNOBSERVED checks $sha"
  curl -fSL --max-time 90 "https://api.github.com/repos/scipy/scipy/actions/runs?head_sha=$sha&per_page=100" -o "$p/runs-$sha-page1.json" || echo "UNOBSERVED runs $sha"
done
```
Check pagination Link headers/total_count and each job URL /actions/runs/{run_id}/jobs; save public raw check status/time/target sha/platform/test step/artifact digest. No assumptions about retention and tag events. If missing/denied record exact HTTP status and timestamp; if different SHA/OS/ABI no promotion. Compare actual published_at and file upload UTC. B6 raw CI log link from issue21142 may expire; exact target success requires a matching released build receipt. No pip install, no user runtime tests in this task. If external artifact byte validation needed, separate read-only download and SHA256/ZIP METADATA parsing under permission; do not execute wheel. 
Finally run `git diff --name-only 4bb9938d31fe7c2bbf97a14c585f4db1fac56717...HEAD` and confirm owned_path only; use repo approved checks if necessary with exact command receipt. Any new findings separate commit; keep current SCOPE and old predictions intact. 

## 색인 제안
키워드: release policy, Requires-Python, classifier stale, exact artifact, Python ABI, temporal release, CI provenance, intent historical vs current, Nikon host/device split. 연결 AF-RES-235의 ClaimRevision/ConsumerRule/ChangeEvent 및 별도 artifact inventory/time. 상태 PARTIAL(원 JSON/CI 미확인); 파일 [RESULT.md](RESULT.md), [matrix.csv](matrix.csv), [sources.jsonl](sources.jsonl), [release-events.csv](release-events.csv), [recommendations.md](recommendations.md), [SELF_CHECK.md](SELF_CHECK.md), [SCOPE.md](SCOPE.md). 중앙 dot-control/INDEX 수정은 통합 담당에게 맡김.