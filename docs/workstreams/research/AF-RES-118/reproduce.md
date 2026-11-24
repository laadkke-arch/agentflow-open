# AF-RES-118 재현

저장소 루트에서 Python 3.12.14, 내장 SQLite 3.53.1, Git으로 수행했다. 외부 Python 패키지는 정책 재생에 필요 없다. 114의 저장소 고정 참조와 118의 결과 체크아웃을 입력으로 사용한다.

```bash
af118=docs/workstreams/research/AF-RES-118
git fetch --no-tags origin refs/heads/work/research-af-res-114:refs/remotes/origin/work/research-af-res-114
af118_tmp=$(mktemp -d /tmp/af118-replay.XXXXXX)
python -B "$af118/replay.py" run --repo "$PWD" --out "$af118_tmp/first"
python -B "$af118/replay.py" run --repo "$PWD" --out "$af118_tmp/second"
for name in slots.csv metrics.json; do
  cmp "$af118_tmp/first/$name" "$af118_tmp/second/$name"
  cmp "$af118/$name" "$af118_tmp/first/$name"
done
for name in table1.csv table3.csv perturbations.csv policy-scans.csv; do
  cmp "$af118/evidence/$name" "$af118_tmp/first/$name"
  cmp "$af118_tmp/first/$name" "$af118_tmp/second/$name"
done
python -B "$af118/evidence/verify-aggregates.py"
git diff --check
python -B -m workbench.session check "$af118/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B scripts/check.py --require-git
```

각 run 호출은 두 개의 새 SQLite 기본 DB와 교란별 조회 DB를 만든다. 첫 보존 단계는 선행 [고정 검사 결과](https://github.com/laadkke-arch/agentflow-open/tree/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114)의 114 모듈을 그대로 읽어 어휘 조회·동점·역할 스캔을 계산한다. 그 뒤 입력의 두 해시와 보관된 11 순위 40행을 대조한다. B/C는 호출마다 분리된 작업 경로에서 [정책 보기](policy-view.jsonl)와 [원절 주석](policy-clauses.json)의 두 파일로 실행한다. 판정·시험 출력 파일은 선택 하위 프로세스의 인수나 입력 디렉터리에 들어가지 않는다. 선택이 끝난 뒤 기준판독을 결합한다.

- `capture.py`는 고정판을 새로 읽어 카드·요구·원순위·역할 스캔·공석을 대사한다. 입력 SHA-256은 [inputs.jsonl](inputs.jsonl) meta와 [대사 영수증](evidence/baseline-reconciliation.json)에 있다.
- `replay.py`는 A/B/C 선택, 역할 누락과 표제 누락의 고정 및 재조회 효과, 별도 채점과 집계를 수행한다. [정책 스캔](evidence/policy-scans.csv)에는 왜 조작·보존 근거가 빠졌는지가 있다.
- [지표](metrics.json)의 기본 비교는 전체 층별 집계를 보존한다. 교란은 변경된 관측값 전후와 재생 해시를 저장하고, [원장](evidence/perturbations.csv)에 변동하지 않은 경우까지 176행으로 남긴다.
- [독립 산술](evidence/verify-aggregates.py)은 선택기를 불러오지 않고 114 넓은 원장의 조사/표시와 118 표시 위치를 비교한다. 내용 판독과 본 실행의 사람은 같다.

## 미실시 원본 실행

이 세션의 Blender 실행 파일은 4.3.2였다. 아래 입력은 Blender 5.3 고정판 기준이다. 테스트 바이너리를 전달할 수 있는 공식 원격과 그 판의 빌드가 필요하다. 첫 목표는 EXR 원본 본체와 Blender의 직접 연결 사례다.

```bash
af118_blender_pin=02f0899d78e374b63e7181d9061e1f7ab03419cc
af118_blender_src=/path/to/blender-checkout
af118_blender_build=/path/to/matching-blender-build
git -C "$af118_blender_src" checkout --detach "$af118_blender_pin"
git -C "$af118_blender_src" lfs fetch origin "$af118_blender_pin" --include='tests/files/imbuf_io/multilayer/108980.exr,tests/files/compositor/filter/**'
git -C "$af118_blender_src" lfs checkout tests/files/imbuf_io/multilayer/108980.exr tests/files/compositor/filter/
sha256sum "$af118_blender_src/tests/files/imbuf_io/multilayer/108980.exr"
ctest --test-dir "$af118_blender_build" -N -R 'compositing_node_group|compositor_cpu_filter|bf_blenkernel'
ctest --test-dir "$af118_blender_build" --output-on-failure -R 'compositing_node_group|compositor_cpu_filter|bf_blenkernel'
```

EXR의 고정 LFS OID는 `17f316283ca8d8287f3f7782eca296a16a7d592d8216a04d70cebf1261b76c64`이며 본체는 361,743바이트다. 3개 우선 필터 fixture의 본체와 PNG OID는 [S-LFS 원장 행](sources.jsonl)에 있다. 현재 [GitHub raw](https://raw.githubusercontent.com/blender/blender/02f0899d78e374b63e7181d9061e1f7ab03419cc/tests/files/imbuf_io/multilayer/108980.exr)는 포인터를 전달했다. [공식 Blender 프로젝트](https://projects.blender.org/blender/blender.git)에서 확인해야 한다. 작성자 보고 재개봉은 공개 원문 [#128731](https://projects.blender.org/blender/blender/issues/128731)의 첫 게시물과 공식 API를 사용한다.

```bash
curl -fLsS 'https://projects.blender.org/blender/blender/issues/128731' -o /tmp/af118-128731.html
curl -fLsS 'https://projects.blender.org/api/v1/repos/blender/blender/issues/128731' -o /tmp/af118-128731.json
```

Krita 5.3 고정판 `148ce5cfc24252922e3866e67af91c12f17b2e08`의 테스트 지원으로 빌드한 경로를 사용한다. Clone의 no_blur/with_blur와 Filter Mask의 MIN/MAX_SELECTED 입력 및 PNG는 [heldout](heldout.csv)에 고정했다.

```bash
af118_krita_build=/path/to/matching-krita-build
ctest --test-dir "$af118_krita_build" -N -R '(kis_adjustment_layer|kis_clone_layer|kis_filter_mask)_test'
QT_QPA_PLATFORM=offscreen ctest --test-dir "$af118_krita_build" --output-on-failure -R '(kis_adjustment_layer|kis_clone_layer|kis_filter_mask)_test'
```

참조 PNG 네 장은 고정 원본 URL에서 내려받아 Pillow로 크기·픽셀을 읽었다. 앱 테스트나 사용자 GUI 실행과 분리한다. GUI에서 보존 차이를 확인하려면 Krita #467257의 입력 PNG로 File Layer를 추가해 ToImageSize 모드와 No Scaling에서 각각 문서 50% 축소와 Advanced Export PNG 50%를 실행하고, #470110의 1920×1080→500×281 변형 마스크 상대 위치를 비교한다. Blender #130134은 Box Mask→Viewer와 연결하지 않은 Double Edge Mask를 같은 장면에 두고 확인한다. 외부 EXR pass 판독은 #128731의 각 패스를 따로 저장해 앱과 판, 파일 형식 및 채널 이름을 기록한다.
