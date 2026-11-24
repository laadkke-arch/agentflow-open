# AF-RES-114 재현

Python 3.12.14 및 내장 SQLite 3.53.1에서 실행했다. 외부 패키지와 GUI 실행 없이 [고정 카드](catalog.jsonl), [두 언어 요청](queries.jsonl), [교란 계획](evidence/scenarios.json), [원자료 영수증](sources.jsonl)을 읽는다. 비교기는 검색 시 카드·질문만 읽고, 표 생성기가 순위 비노출 판정 원장을 나중에 합친다.

저장소 루트의 깨끗한 결과 커밋에서 실행한다.

```bash
work=docs/workstreams/research/AF-RES-114
scratch=$(mktemp -d /tmp/af-res-114.XXXXXX)
python -B "$work/tools/run_experiment.py" --out "$scratch/replay"
python -B "$work/tools/tables.py" --out "$scratch/tables"
python -B "$work/tools/verify.py" --replay-output "$scratch/replay" --table-output "$scratch/tables"
python -B -m workbench.session check "$work/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B scripts/check.py --require-git
```

DB는 새 출력 폴더의 `scratch/{verified,publisher_partial,clone_missing,filter_missing,box_role_omitted}/build{1,2}.sqlite`다. 순위 원장 10개를 바이트 대조하고 독립 파이썬 계산으로 토큰, 조사 순서, 역할 충돌, 빈 슬롯, 표시 순위, SQL 횟수를 확인한다. 고정 원문 URL과 읽은 절은 각 원장에 있다.

| 층 | 고정 입력 | 재생 범위 |
| --- | --- | --- |
| 목표 매뉴얼 별칭 | `alias_verified` | 2 DB, 자연 예정 96행(실제 검색 0), 탐색 96행, 구성 64행, 한국어 변형 32행 |
| 발행 표기 보조판 | `alias_publisher` | 2 DB, 탐색 96행, 구성 64행, 한국어 변형 32행 |
| 한 기능 교란 3종 | `evidence/scenarios.json` | 조작별 2 DB, 구성 64행씩 |
| 표 1~3 | 첫 재생 원장과 truth 3개 | 빈 요청 분모와 확인된 적격 0을 구별하고, 기능 ID별 순위 변화 구간을 집계 |

`costs.json`에는 입력 파일 SHA와 순위·슬롯의 재생 지문이 각각 있다. 기본/별칭/역할 테이블을 만든 직후 페이지 수를 기록하며 빈 별칭 테이블도 한 페이지다. SQL 문 수는 검색과 역할 읽기에 한정했다.

## 미확인 자연 표본을 복구할 첫 실행

공식 공개 호스트의 다음 GET 응답과, 이를 생성 UTC·원 ID로 고정한 파일이 필요하다. 이 명령은 각 창의 시작 경로다.

```bash
curl -fLsS --get 'https://projects.blender.org/api/v1/repos/blender/blender/issues' \
  --data-urlencode 'state=all' --data-urlencode 'type=issues' \
  --data-urlencode 'limit=50' --data-urlencode 'page=1' \
  -o blender-page-1.json
curl -fLsS --get 'https://bugs.kde.org/rest/bug' \
  --data-urlencode 'product=krita' --data-urlencode 'creation_time=2023-01-01T00:00:00Z' \
  --data-urlencode 'include_fields=id,product,summary,creation_time' \
  --data-urlencode 'limit=1000' --data-urlencode 'offset=0' \
  -o krita-page-0.json
curl -fLsS 'https://bugs.kde.org/rest/bug/464692/comment' -o krita-464692-comment.json
```

Blender API의 지원 상태·페이지 경계를 헤더와 마지막 페이지에서 확인한다. 필요한 모든 페이지에서 created_at, number, title, body를 보존하고 PR을 제외한다. 공개 API의 q가 body 또는 댓글을 포함하는지 판별할 수 없으면 전수 페이징과 로컬 제목·작성자 본문 검사를 적용한다. KDE는 원 ID별 `GET /rest/bug/{id}/comment`에서 작성자 게시 위치를 고정한다. `[2023-01-01, 2026-01-01)`과 SCOPE의 어구 및 생성 UTC·ID 순서를 적용하고, 처음 40건과 경계 다음 건의 제목·본문 해시를 남긴다. 역사적 제출본의 독립 스냅샷이 확보되면 현재판과 대조한다. [Bugzilla REST](https://bugzilla.readthedocs.io/en/5.0.4/api/core/v1/bug.html) · [Forgejo 페이지 규칙](https://forgejo.org/docs/latest/user/api/usage/)

문서 보완에는 Blender 5.3 release의 영어 RST·POT, 한국어 ko/LC_MESSAGES의 발행 revision과 한·영 HTML, Krita 발행 빌드의 RST 및 KDE SVN 한국어 PO revision이 필요하다. Krita 정규 파일명은 [StaticMessages.sh](https://github.com/KDE/documentation-docs-krita-org/blob/1931b5dfda19086f16d4526a65c169a130c68742/StaticMessages.sh)가 만든 docs_krita_org_reference_manual___render_animation.po 및 docs_krita_org_reference_manual___layers_and_masks___filter_layers.po 형태다. 고정판의 원문 키와 번역 키를 대조하고 실제 발행 절에서 두 키의 표시를 확인한다.

UI에서 확인할 최소 입력은 Krita 5.3.0의 기존 PNG File Layer와 Transform Mask를 가진 복제 문서, Blender 5.3.0의 기본 장면과 Box Mask→Viewer 및 연결하지 않은 Double Edge Mask다. Krita에서는 #467257과 #470110에서 ToImageSize 모드, 문서 축소, Advanced Export, 위치 보존을 각각 실행한다. Blender는 #130134의 공개 본문 단계대로 Backdrop을 재현한다.
