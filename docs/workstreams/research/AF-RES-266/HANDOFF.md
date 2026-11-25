# AF-RES-266 인계

**자체 상태 DONE.** 세 버전 JSON과 Simple에서 83/83개 파일이 조인됐다. 248의 환경표는 양성 5개와 현재 정상 공석 4개 전부 일치했다. 다섯 wheel의 원바이트, ZIP 메타데이터 및 sidecar를 검산했고, 1.14.1 CPython 3.13 GIL의 정확한 양성 파일 하나를 실행했다. 그 시험이 Q7의 로컬 실행 합격 대안이다. 발표 시각보다 앞선 파일은 양성 5/5 및 전체 82/83이다. 1.14.1의 macOS x86_64 CPython 3.12 파일 하나는 발표 뒤 기록으로, 두 호스트의 현재 파일은 동일 SHA-256이다. 당시 동일 파일 CI 5/5, 최초 인덱스 노출 및 삭제·교체 이력은 미확인이다. 독립 검토 미실시.

## 고정 결과와 근거

- 작업 브랜치 `work/research-af-res-266`. 소유 경로 `docs/workstreams/research/AF-RES-266/`. 착수 통합판 `3c32c1b44bd139819485548cb50e69e254288fad`, 248 의존 인계판 `4a690fc68182b8b2792c15d921ed3baeeaa7220e`. [범위·핀](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/SCOPE.md).
- 검사한 고정 결과 **`cf42104d1944d2712d4936ccafd54fcf2f19725a`**. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/RESULT.md), [cells.csv](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/cells.csv), [files.csv](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/files.csv), [release-events.csv](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/release-events.csv).
- [원자료 원장](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/sources.jsonl) 30개 산입. 그룹은 4/5/8/11/2다. [반례·정정](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/COUNTEREXAMPLES.md), [자체 점검](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/SELF_CHECK.md), [재생 절차](https://github.com/laadkke-arch/agentflow-open/blob/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/replay.md).
- 검사 영수증 고정판 **`c951972d12bd9aedc7b4a1016cf13e7e581c0800`**. 명령, 입력 지문, 원 stdout/stderr, 종료 코드 및 출력 SHA-256을 저장했다. 결과 파일에는 변경이 없으며 이 판에서도 빈 폴더 재생이 6/6 일치했다. [검사 영수증](https://github.com/laadkke-arch/agentflow-open/tree/c951972d12bd9aedc7b4a1016cf13e7e581c0800/docs/workstreams/research/AF-RES-266/receipts/checks).

## 검사한 SHA와 범위

아래 네 검사는 고정 결과 `cf42104d1944d2712d4936ccafd54fcf2f19725a`를 사용했다. 저장소 검사는 GitHub에서 새로 clone한 깨끗한 트리에서 수행했다.

| 명령 | 종료 | 실제 범위 |
|---|---|---|
| `bash docs/workstreams/research/AF-RES-266/receipts/verify-replay.sh "$PWD" cf42104d1944d2712d4936ccafd54fcf2f19725a` | 0 | 빈 Git archive 추출 폴더. 저장 입력 SHA-256과 결과 6파일 바이트 일치, 9셀·83파일 및 파일 조인 재생 |
| `python -m workbench.session check docs/workstreams/research/AF-RES-266/session.json --fetch` | 0 | `remote_checked`, 통합판 `6cb99cc0af8ff62035d4ddce1df5cf9bc6906b7c`, 의존 SHA·계약 일치, 검사용 manifest를 제외한 274경로 중 외부 0 |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0 | 깨끗한 동일 SHA, doctor·기존 acceptance와 smoke. 공용 manifest 탐색은 `no_active_sessions`, 개별 계약은 위 명령 확인 |
| `python scripts/check.py --require-git` | 0 | workbench/lab test·demo·export·Git bundle 복원·출처 연결 구조 |

별도로 M9 `5149e3fd2d686e42144a093b206aef01932a0059c2a33ddfa67f5f035bdfe13e`는 CPython 3.13.5 GIL, NumPy 2.1.3, glibc 2.41에서 해시 강제·인덱스 없는 설치 후 import/solve를 통과했다. 다른 네 양성의 로컬 시험은 미실행이다. [로컬 설치·시험 영수증](https://github.com/laadkke-arch/agentflow-open/tree/cf42104d1944d2712d4936ccafd54fcf2f19725a/docs/workstreams/research/AF-RES-266/receipts/local).

## 미확인과 다음 첫 행동

당시 CI를 확인해야 한다면 첫 행동은 1.14.1의 peeled SHA `92d2a8592782ee19a1161d0bf3fc2241ba78bb63`로 보존된 Wheel builder 실행을 조회하는 것이다. 이 세션에서 GitHub REST는 프록시 403, 공개 Checks·태그 검색은 job 행 공석, 개발 Cirrus 원로그는 502였다. REST 접근이 되는 환경에서 아래 입력으로 다시 확인할 수 있다.

```bash
gh api --method GET repos/scipy/scipy/releases/tags/v1.14.1 --jq '{tag_name,published_at}'
gh api --method GET repos/scipy/scipy/actions/workflows/wheels.yml/runs \
  -f head_sha=92d2a8592782ee19a1161d0bf3fc2241ba78bb63 -F per_page=100 --paginate
```

실제 run ID가 나오면 그 run의 `/jobs`와 `/artifacts`를 조회한다. 시험이 사용한 wheel의 파일명·SHA-256을 위 M9와 대조한다. 원 archive가 남으면 그 안의 wheel 자체를 해시한다. 최초 공개/삭제를 확인해야 한다면 최소 입력은 공지 시점 전후 저장된 PyPI 인덱스 본문이나 삭제·업로드 사건 영수증이다. 늦은 macOS 파일의 키는 `scipy-1.14.1-cp312-cp312-macosx_10_13_x86_64.whl`과 `631f07b3734d34aced009aaf6fedfd0eb3498a97e581c3b1e5f14a04164a456d`다. [태그 Checks](https://github.com/scipy/scipy/commit/92d2a8592782ee19a1161d0bf3fc2241ba78bb63/checks), [late GitHub 자산 목록](https://github.com/scipy/scipy/releases/expanded_assets/v1.14.1).

색인에는 ‘AF-RES-266 · 배포 링크 실측 · 248 의존 · 3 PyPI JSON+Simple, 9셀 5/4, 1 exact local run, 역사/CI 미확인’을 고정 결과 링크와 함께 등록할 수 있다.
