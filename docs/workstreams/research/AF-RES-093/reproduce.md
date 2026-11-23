# AF-RES-093 재열람·검사

## 결과판과 명령

최종 `HANDOFF.md`의 **결과 커밋**을 checkout한다. 인계 단독 커밋과 검사 대상 결과 커밋을 혼동하지 않는다. 현재 작업에서는 사용자 PC 설치 없이 제공된 클라우드 checkout을 사용했다.

```sh
git clone --branch work/research-af-res-093 https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git checkout --detach HANDOFF에_적힌_40자리_결과_SHA
git rev-parse HEAD
python -B docs/workstreams/research/AF-RES-093/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-093/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`--environment codex-cloud`는 저장소 검사기의 실행환경 라벨이며 별도 모델·계정 연결을 증명하지 않는다. 실제 명령·대상 SHA·종료값은 인계와 검사 영수증을 따른다. 원 application 동작은 외부 원자료 판독과 구분한다.

`audit.py`는 읽기 전용이다. 6×2 자리, A/B 공통 payload, B의 세 추가 필드, 실제 UTF-8 바이트, 봉인 원본 hash, 모집 30+30 및 선택 3+3, 사후 채점 분모, 출처 중복을 다시 계산한다. CSV는 제목 안 개행을 허용하므로 파일 줄 수로 행 수를 세지 않는다.

`assemble_preseal.py`는 사전 조각을 합친 당시 재현용이다. **최종 결과 위에서 실행하지 않는다.** 실행하면 사후 `judgments.csv`가 사전 미채점 상태로 돌아간다. 꼭 재현하려면 원격 봉인 `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592`의 별도 checkout에서 실행한다. 사후 자료를 본 연구자는 이것으로 새로운 맹검 실험을 만들 수 없다.

## 모집 재열람

- Inkscape: `evidence/inkscape/query_receipts.json`, `main_metadata_and_release.json`, `frame.csv`, `PRESEAL.md`의 API URL·기간·검색 조건. 공식 본 저장소를 대상으로 하고 GitLab title 검색의 stemming을 그대로 보존했다. inbox pilot 자료는 모집분모에서 제외한다. 같은 사건의 이동/중복은 원순번을 지우지 않고 event rank로 묶는다.
- Pillow: `evidence/pillow/search-projections.json`, `frame.csv`, `recruitment.md`의 GitHub REST `search/issues` URL. `is:issue in:title`, 세 검색어 각각, `created:2021-01-01..2025-12-31`, `sort=created&order=asc&per_page=100`이다. 최초 응답은 `incomplete_results=false`였다. 합집합을 생성 UTC·숫자 ID로 정렬한다.
- 두 경우 모두 현재 API 조회는 최초 작성 당시 body를 보증하지 않는다. 저장한 body hash와 원문/이동 전 주소, 수정판 복원 한계를 함께 본다. 새로 생긴 접근제한·본문 수정은 기존 관측을 소급하여 덮어쓰지 않는다.
- GitLab의 공개 이슈 본문/소스 API는 읽혔으나 `/notes`는 401을 반환했다. 공개 이슈 UI의 `/-/issues/<iid>/discussions.json`에서 실제 댓글 원문이 읽힌 범위를 사용한다. 비공개 권한을 요청하거나 우회하지 않았다.

## 사전 봉인 재확인

1. ① `b9f878064bcf27b627a16977c9fa4580268aed3c`에서 `SCOPE.md`, `manifest.json`, `evidence/calibrations.json`을 연다.
2. ② `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592`에서 `records.jsonl`, `judgments.csv`, `evidence/preseal-summary.json`을 연다. 당시 정답은 비어 있어야 한다.
3. 원본 A를 먼저 고정한 hash와 B 초기판·수정판을 대조한다. Inkscape I2 B의 후보 절 밖 callback 언급은 원값을 남기고 봉인 전에 제거했다. A는 수정하지 않았다.
4. I3의 본문 수정 문장 사전 노출, 실제 요청 본문 노출 2회 보정, 같은 연구자의 A→B 순서를 확인한다. 완전 맹검이나 무작위 배정으로 해석하지 않는다.

## 외부 동작의 최소 추가 확인

원 저장소의 소스·시험을 읽은 것은 application을 실행했다는 뜻이 아니다. 최종 Q별 미확인과 정확한 입력은 `SELF_CHECK.md`, 사례 원장은 `judgments.csv`, 타 분야는 `evidence/cross-domain/exact-regression-search.md`를 따른다.

- Inkscape 1.0.2: 원 SVG2 flow-text를 Space stamp 및 Duplicate로 각각 만든 뒤 복제 text-box 하나의 크기만 바꿔 원본/다른 상자의 참조 ID와 geometry를 함께 기록한다. LPE는 기존 target ID가 필수인지 먼저 고정한 동일 SVG에서 clipboard Link와 메뉴 새 target 경로를 비교한다. I3은 같은 eraser 입력의 후보2를 먼저 확보해야 한다.
- Pillow: 8.2.0의 #5406 원 GIF와 전체 caption→save 파이프라인에서 P 경로와 변환 선행 경로의 RGBA 및 팔레트 index를 구분하여 읽는다. #5593은 8.3.0의 같은 P 입력·transparency=0에서 `convert()`와 `convert('RGBA')`의 mode/alpha를 각각 기록한다. #5595는 공개 p와 두 palette 부착 호출의 palette/RGB/index를 확인한다. 현재판으로 바꿔 실행하면 별도 결과로 남긴다.
- Calc 24.2.7.2: 원 `CalcPasteOnly.py`의 D1 값 붙여넣기/E1 수식 붙여넣기 뒤 D2=7·E2=7 및 CalculateHard를 추가해 D1/E1 값·수식 문자열을 모두 기록한다. 예상 0/7은 아직 관측이 아니다.
- Arrow 18.1.0: `TestDictionary.TransposeBasic`, `TransposeTrivial`, `GetValueIndex` 원 시험과 동일 배열에서 논리 문자열 판독 및 `indices == 0` 행 선택을 함께 실행한다. 현 원장에서는 원 assertion 판독과 명세를 적용한 계산을 구분했다.

공개 자료에 근거한 후속 확인안이다. 이 문서의 명령·입력을 적어 두었다고 실행 완료로 세지 않는다.
