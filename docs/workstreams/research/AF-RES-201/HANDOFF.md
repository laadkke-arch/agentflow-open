# AF-RES-201 HANDOFF

status: PARTIAL
result_commit: 59c1dff20dd0cbe72d3d274e8e1c739590d4d768
branch: work/research-af-res-201
base_commit: c860f8240ab7b7077e2d5b63e438ddd83ff69a27
plan_commit: 050278651b11a2a3a49d45baebf41c707c06b700

## 자체 판정

- 핵심 소비자 측 판별은 성공: C Fig5 우측의 sns.displot을 생성기 C22와 manuscript C26의 동일 fig-plotting.png 경로로 연결; 논문 height=4 vs 생성기 5, 문서 aspect=1.5. E3 정적 경로, E4 없음.
- K 비교 인용과 seaborn>=0.11 설치 선언, 지연 로더 등록은 별개; polar violin은 C16의 SciPy KDE와 ax.fill. V 비교 인용과 C21 Julia BoxPlot 자체 구현을 분리. 두 건 모두 특정 published figure 생성 증거는 불충분.
- R v1 2019에는 2021 Waskom DOI가 없지만 C11 코드에 stripplot, boxplot, FacetGrid 등 호출. 후대 v1.1과 저장 조건/파일 번호가 다르다. F13 재조회 403로 v1 alias 전수의 정확 쪽/위치 재검증 불충분. PtitPrince 0.1.3 소스 F06 404. 
- 공연 사례 2014-12-06 LOC Clare College Choir/Graham Ross: M01/02/03/09 네 기관/당사자 자료로 공연·작품·편곡 및 날짜 충돌 파악. 실제 음원 F08/F12 접근 실패. 동일 공연의 녹음 원기록 직접 검증 0/1. Bernstein의 미기재를 미연주로 승격하지 않는다. 
- 산입 43/22: paper 4/4, author code 24/8, release/method 8/4, seaborn 3/2, music records 4/4(실제 원음 0/1 별도 미충족). 원장 65행(22 제외/중복/실패), mentions 26행(미언급 상태 1), usage 14행, routes 12행. 모두 자체 검토, 독립 검토 없음. Q5 완전 참고문헌-only 경쟁제품(본문 미언급) 고정 사례도 미확정. E4 0/4. 개수 하한은 충족하지만 Q6 실제 녹음·Q1 v1 전수 재검증 및 위 결손 때문에 DONE으로 판정하지 않는다.

## 결과 고정 검증

직전 결과 SHA 위의 10개 파일 전부를 GitHub fetch_file로 다시 읽었다. RESULT.md 제목 직후 3개 필수 표의 열 이름 일치, 끝 약점표 정확히 3행, sources JSONL 65행/43 eligible, routes 12행, 주요 문자열 확인. SELF_CHECK는 원장/CSV ID 누락 0을 확인했다. 파일별 blob:
- SCOPE.md bd55134010f8c1a5492f4e759f051465d3261b6a
- RESULT.md 6ac57a95d60eb25a3971a670e9607d4ccbe216bb
- SELF_CHECK.md b87f0869994e4db734d9cdec475dc8e273227c7c
- sources.jsonl b11de683ea3ed0ee14fe2ee56c2b27f190c97944
- frame.csv d00672d2b86d8fcf6acbc97014b027129039ccb3
- mentions.csv 067805dc5be07b01a8642f5078ad35e8d63e61ee
- usage.csv 466bee5cbf7528017c2ec5bc20b5be6e208e3c8c
- routes.csv 033fe2384a019ba0bd18b6bdeea858ed71f8afc4
- COUNTEREXAMPLES.md 999a832067239435b8fc7ca71cef14d05a087866
- TABLES_DRAFT.md ff7e5c455b5a0c3d01ad57a2644f7165662b9af4

base→result GitHub compare ahead 15, behind 0, 10 paths 모두 owned_path. dot-control.json 변경 없음. 이 인계 이후 수정하지 않는다. 최초 scope → 원장 → 핵심 CSV 및 초안 → 반증 및 갱신 → RESULT/SELF_CHECK 순서로 커밋 완료; 마지막 파일은 이 HANDOFF. 시작 시 contents API 큰 JSON 빈 값 문제는 동일 시작 blob 직접 fetch로 해결; AF-RES-192 DONE과 result_commit 확인, HANDOFF 자체 PARTIAL 의미 보존. 

## 재개 첫 행동 및 검증 인계

1. 먼저 P04 고정 DOI 10.12688/wellcomeopenres.15191.1의 공개 v1 PDF를 publisher나 기관 사본에서 합법적으로 열고(403 우회 금지), 40페이지 초판인지 확인한다. 입력 PDF를 로컬에 정당하게 확보한 경우 다음을 실행하여 **위치순 모든 literal, alias, Waskom, caption/ref/thanks**를 원장과 대조: `pdftotext -layout raincloud-v1.pdf raincloud-v1.txt; rg -ni 'seaborn|sns\\.|waskom|facetgrid|ptitprince' raincloud-v1.txt`. 페이지 구분/그림 캡션은 PDF와 직접 대조. 예상: R v1 직접 호출과 2021 DOI 미언급, 추가 alias 또는 쪽 차이가 나오면 mentions 수정. 입력 및 날짜를 명확히 유지한다.
2. LOC 프로그램과 녹음 카탈로그 M01/M02/M03/M04/M09: 실제 원녹음 또는 기관 track/session log를 열고 2014-12-06 19:00 Coolidge / Choir / Graham Ross / Fine Alice Set I 및 Britten Op28 Harrison 1955의 track 식별자·시간·credits를 맞춘다. 링크 https://www.youtube.com/watch?v=c9qJSzl_vcA 는 접근 실패 기록 유지. 게시 2015-05-08 vs 녹음 표기 2015-12-06 불일치 및 Bernstein 미기재는 원 마스터/세션으로만 해결. 접근 불가하면 PARTIAL 유지.
3. 소스 추가 검사(별도 승인된 실행 환경, 외부 OSS checkout만; agentflow-open owned_path 밖에 쓰지 말 것). 이미 접근 가능한 임시 checkout에서 아래 고정 tag 및 blob 일치 확인:
   - colorspace v1.0.0: `git rev-parse v1.0.0:paper_assets/paper_makefigures.py` 기대 973b518937bc4e0cf1fcce42ae974bb6f5e1bde9. `git show v1.0.0:paper.md | rg -n 'fig-plotting|sns.displot'`; generator L136–179, HarzTraffic input, height=5, dpi150. 논문 snippet height4, qmd aspect1.5. 원본 fig-plotting.png를 실제 공개 tag에서 읽어 PDF 그림과 비교. 이미 승인된 역사 환경/lock 존재하는 경우에만 해당 파일을 isolated cwd에서 실행(전체 script 선행 pal3 정의 필요): `cd paper_assets && MPLBACKEND=Agg python paper_makefigures.py`. 생성 결과 dimensions/sha256/log 및 package versions 기록. 환경 부재 시 설치·새 키 금지, 재현 불가로 보고. 새로 재현한 출력과 당시 실행의 증거는 구별.
   - k-diagram v1.3.4: `git rev-parse v1.3.4:kdiagram/plot/errors.py` 기대 ade00a120c99b24897e7b5d1e8228f68caa8d7cb; `git grep -n -i -E 'seaborn|sns\\.|plot_error_violins|paper_fig2\\.png' v1.3.4 --`; paper.md L245의 Fig2 asset 생성기/함수 mode를 찾는다. init blob 0053d257a016da8e0bc68220b03e3216aea409d9; deferred loader 실제 호출은 독립 trace 필요. 이미 설치 승인된 환경이라면 `python -c 'import sys,kdiagram; print("seaborn" in sys.modules)'`은 import 경로만 확인하며 특정 plot 소비 증거 아님. 입력/fig2 generator 발견 후 동일 figure trace를 추가.
   - Vizagrams v0.2.16: `git rev-parse v0.2.16:src/marks/boxplot.jl` 기대 3e9abbe629501223f652f5c25c7ee76b30aa4f50. `git grep -n -i -E 'seaborn|PyCall|PythonCall|BoxPlot' v0.2.16 --`. Published paper figures의 tag generator/manifest 찾기. Zenodo 17340262 접근 제한은 우회 금지.
   - RaincloudPlots v1.0: `git rev-parse v1.0:tutorial_python/raincloud_tutorial_python.ipynb` 기대 219cd76fa172c14630f7446cadb7171fd8d1cd8b. `git show v1.0:tutorial_python/raincloud_tutorial_python.ipynb > /tmp/af201-v1-notebook.json`; `python -c 'import json; n=json.load(open("/tmp/af201-v1-notebook.json")); print([(i,c.get("execution_count"),[o.get("output_type") for o in c.get("outputs",[])],"".join(c.get("source",[]))) for i,c in enumerate(n["cells"]) if "sns." in "".join(c.get("source",[])) or "savefig" in "".join(c.get("source",[]))])'`. 입력 C13 simdat.csv, C12 ptitprince==0.1.3, seaborn>=0.9 (정확 판 불명). 태그/배포 원문에서 PtitPrince 실제 implementation을 확인. notebook 실행/이미지 비교는 정확 승인된 환경에서만; v1.1과 번호 섞지 말 것.
4. 원장 구조를 재검증할 때 `python -c 'import json,csv; p="docs/workstreams/research/AF-RES-201/"; s=[json.loads(x) for x in open(p+"sources.jsonl")]; print(len(s),sum(x["counted"] for x in s)); print(len(list(csv.DictReader(open(p+"routes.csv")))))'` 기대 65,43,12(이 인계판 기준). 이 명령들은 여기서 실행하지 않았다; GitHub connector/JS로 문서 읽기와 형식/ID/경로 확인만 했다.

## 색인 반영 제안 (실제로 수정하지 않음)

AF-RES-201 PARTIAL, 대표 RESULT.md/SELF_CHECK.md; key: consumer-side passage role ≠ install declaration ≠ callable function ≠ same figure generation path ≠ execution observation. C E3 static; R E2; K/V comparator/own geometry. 본문 맥락 vs 구현 vs 정확 산출물 12 routes. Q6 공연 원음 및 R v1 전체 alias 재검증, K/V specific generator 미확인. 중앙 색인·control·merge는 조정자가 담당한다. 최종 제품 구조 또는 추천 순위 미결정.
