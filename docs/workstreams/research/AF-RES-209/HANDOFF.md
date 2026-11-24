# AF-RES-209 HANDOFF
- 상태: **PARTIAL** (검색 도구 응답의 실제 노출 순서 8/8 및 첫 문서 열람 8/8 완료; 원래 검색 사업자의 유기적 순위 확인 0/8, 개별 정확 UTC 0/8, raw snippet 원문 미보존). 원순위가 필수라는 엄격 해석에서는 완료 주장 금지. 반환 순서가 제공되었으므로 별도 검색면 전체 반복 미실시; 다음 작업 첫 행동 아래. 도구 수준 비교 4쌍: 개선 0, 악화 1(#847), 동률 1(#265), 판정불가 2(#703/#774). 단일 목적표본이라 일반화 금지.
- 저장소/브랜치: laadkke-arch/agentflow-open / work/research-af-res-209. 시작 SHA 87ffc1539bcf33da0fccf45eb15982a02d93e409 (계획 bb146773bbffba5e724e8c842951e2c25198c2da 대비 +5/-0 dot-control만 변경), 의존 198 result 05ae34bd0a160ce9ce52658616fad6f0273ea883, 중앙 DONE vs 198 자체 PARTIAL 구분. 최신 control/AGENTS/STATE/workflow/brief/index 및 198 HANDOFF/paths/alternatives 읽음. 205–207 및 LosslessCut/FFmpeg/GDAL 재조사 안 함.
- 마지막 **결과 SHA(이 인계 전)**: 7f67916179ffdbeb4a5cbb459db854ae94bc37d4
- 묶음 1 (질의 사전 동결): 47773aacc4957539115c547cef399641ea166a7a; 2 (모집/원장): 655b7fd65e7bb9d88eedf132782fecb1f471c2ef; 3 (개별 노출·경로·비교): 94c4fb5e1d099eb6483617e3e5c3dda1b79301ff; 4 (반례·IIIF·정정): a8dde3b65f06434f61edec3829834f337465f6b3; 5 (결과/자체점검): 7f67916179ffdbeb4a5cbb459db854ae94bc37d4. HANDOFF는 별도 마지막 커밋. 
- 대표 파일: RESULT.md (필수 3표부터, Q1–7, 대안/반증, 마지막 약점 3건), SCOPE.md, queries.csv (정확 8), frame.csv, sources.jsonl (37 rows), paths.csv (24 positions), matches.csv (4 cases + cross), SEARCH_RECEIPTS.md, COUNTEREXAMPLES.md, SELF_CHECK.md.
- 마지막 결과 SHA에서 위 10개 파일 전부 재조회, JSONL parse/unique/count 검증(33 고유 work_id, 15 lineage_id; 직접 열림34, 중복 1 제외, 403 고유 URL3 비산입), 8개 쿼리 순서 AB BA AB BA/각 B=A+1 token 확인, 24개 노출 URL 모두 RESULT 안에 존재, 첫 열람8, follow 시도5(성공0), 4쌍 matches 대조, D02 재판독 구간 및 LOC 동일 ID 0/90 주소쌍 대조, 필수 표 헤더4 확인. compare start...result ahead5 behind0, 변경 10개 전부 owned_path, dot-control 미변경. 자체 검사만 수행, 독립 검토 없음; 로컬 checkout/manifest/test 실행 안 함.
- 유형별 하한: 지명 4/4, 제작자 자료 7/7, 소비자 5/5, 변경/답변 4/3, IIIF/기관 3/3, 추가 직접 10; 33/22. 댓글 별개 저작이나 동일 사건·계보임을 보존. 자료 판독은 실제 실행/재현/사용자 목적 달성 실측이 아님. 원제보 초기 revision 및 개인 입력 미확인. 정확 도착절, 실패 URL과 수동 대안 분리.

## 다음 작업자의 첫 행동 — native SERP 재조회
queries.csv의 순서 1–8을 그대로 고정하고 실제 공개 검색면의 순위와 원본 응답 캡처/원 URL/표시 문구/UTC 및 세션·지역·언어·정렬을 기록한다. 한 번에 한 질의, 첫 결과 열고 추가 실제 링크 최대 2회, 동일 예산; 오류/리다이렉트 기록. 기존 fast 결과와 섞지 말고 별도 반복 묶음으로 보존. 가능하면 새 평가자에게 원답/기존 결과를 숨긴다. 이 작업은 이미 원제보와 메커니즘 문서를 봤고 비맹검이다. 첫 문서가 #847에 대해 버전·경계 조건을 충족하면 B 악화 결론 바뀔 수 있다; #774 원 입력이 EXIF인지 SPIFF인지 명시되면 해당 사례 판정 가능. 정확 순위가 여전히 없으면 PARTIAL 유지.

## Codex 검증 항목 (이 조사에서는 실행하지 않음)
1. 원장/경로 보존 확인: 승인된 checkout에서
   `git fetch origin work/research-af-res-209`
   `git show 7f67916179ffdbeb4a5cbb459db854ae94bc37d4:docs/workstreams/research/AF-RES-209/RESULT.md`
   `git diff --name-only 87ffc1539bcf33da0fccf45eb15982a02d93e409 origin/work/research-af-res-209`
   JSONL 각 행 파싱·unique work/lineage/포함 조건, csv 8×3과 AB/BA를 재검사. 기대: owned_path만, 33 counted, native rank 0. 원래 SERP raw export가 없으므로 이를 현재 검사로 소급 복원한다고 주장 금지.
2. 별도 승인된 JPEG fixture 실험: 개인 사진 대신 비대칭 화살표/모서리 색·문자, 정상/없는 EXIF 및 1,2–8, 32×32와 33×35, 4:4:4 및 4:2:0, thumbnail 있는 입력, #847 사례 92×32→200×32와 16×16 블록 조건. 원본 복사본만 사용, 실행 전 `jpegtran -version` 및 `exiftool -ver` 기록. 
   `jpegtran -copy all -perfect -rotate 90 input.jpg > rotated.jpg`
   `jpegtran -copy all -trim -rotate 90 input.jpg > trimmed.jpg`
   `jpegtran -copy all -rotate 90 input.jpg > default.jpg`
   `jpegtran -crop 200x32+0+0 -outfile expanded.jpg input92x32.jpg`
   #847의 3.1.0과 R08이 말한 dev/3.2의 실제 고정 commit/release를 확인 후 별도 비교. 기대: perfect는 불가능한 부분 iMCU 입력에서 실패, trim은 경계 감소, crop 확대 동작 버전 차이 가능; 실제 출력의 decoded dimensions/오른쪽 4px/DCT block mapping 검증, 허용 artifact 별도. 계수 비교는 동일 block의 기하 대응·부호/순열을 검사하고 전체 SHA 비교로 대체하지 않음. 반전: 같은 버전·동일 입력의 perfect/trim 규칙 위반, 신버전에도 경계 손실이면 추천을 재평가.
3. 숫자/태그 및 이중 회전: 입력별 새 복사본에서 `exiftool -Orientation=6 copy_a.jpg`, `exiftool -Orientation=8 copy_b.jpg`, `exiftool '-Orientation#=6' copy_c.jpg`, `exiftool -n -Orientation copy_a.jpg copy_b.jpg copy_c.jpg`, `exiftool -G1 -a -s -n copy_c.jpg`. 새 IFD와 기존 IFD로 나누고 쓰기 전후 목록과 JPEG coefficient/metadata/thumbnail 검사. M06 기대: #=6 raw value 6; S04/R05 bare=8은 당시 12.85에서 텍스트 단축형 180→3, 현 버전에서는 재현해야 함. 파일 바이트 해시가 변해도 계수 유지와 혼동 금지. Pillow 12.0.0 기존 `python -m pytest Tests/test_imageops.py -k exif_transpose` (승인된 환경/checkout/기존 dependencies)에서 2–8, absent-tag base, 반복 idempotence. 별도 normal=1과 pixel-rotated tag6 fixture, OpenCV default vs IMREAD_UNCHANGED/IGNORE_ORIENTATION; 기대: tag6 유지 시 존중 뷰어 이중 회전, 무시 뷰어는 다름. 반전: 동일 입력/뷰어에서 모두 같다면 그 구현 동작을 조사. 신규 실행·설치 현재 미실시.
4. IIIF: COUNTEREXAMPLES.md의 LOC 문서 0/90 + info.json 주소를 읽고 capability/응답 치수/형식 비교(승인·rate limits 준수); 실제 마스터 파일을 알 수 없는 공개 기관 API에서 master hash를 추론하지 않는다. 권한 있는 작은 fixture IIIF 서버에서 master hash before/after 및 derivative 요청 log를 검증. 기대: region→size→mirror/rotate→quality→format 반환, 저장소 master는 관리 정책에 따름; master 변하면 별도 관리 설계 문제. 공개 원문만 읽었고 이미지 요청/바이너리 검사는 실행 안 함.

## 색인 반영 제안 (편집하지 않음)
AF-RES-209: JPEG orientation / invariant-aware A/B query, 33 sources, observed 8/8 first paths (native rank unverified), 847 exact A beats B, 265 tie, 703/774 uncertain; separate display/metadata/DCT/edge/pixel/thumbnail and IIIF derivative-vs-master; PARTIAL. Index and central control remain untouched; link RESULT at fixed result SHA and this HANDOFF final commit.
