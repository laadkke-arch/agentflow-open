# AF-RES-201 SELF_CHECK

판정 PARTIAL. 자체 점검(독립 검토 미실시). 산입 자료 기준과 출력 생성 실행 증거의 차이를 적용.

| 요구 | 실제/목표 | 판정 |
|---|---:|---|
| 고정 출판판 | 4/4 | P01–P04 모두 직접 텍스트; P04 초기 직접 열람, publisher 403 및 후속 재조회 실패 보존 |
| 저자 코드/노트북/환경/그림 | 24/8 | tag source 24; C08/C26 논문 manuscript 중복 제외; C14 후대판 대조 |
| 발행·배포·방법 | 8/4 | T01–T08 별개 문서, 같은 배포 사건은 합산하지 않음 |
| seaborn | 3/2 | S01 논문, S02/S03 API archive; 설치판 증거 아님 |
| 공연 관련 원자료 | 4/4 | M01/02/03/09 (브로슈어, 프로그램, 기관 제작 공개 목록, 공연자 일정) 같은 사건 1; 실제 오디오 원기록 0/1로 미달, M04 catalog 제외 |
| 합계 | 43/22 | 문서 개수 하한 충족; Q6 실제 원기록 결손 |
| source/frame | 65/65 | 43 yes, 22 excluded/failed/duplicate; ID 중복 0; frame ID 누락 0 |
| mentions | 26행 | C8 K2 V2 R14(미언급 상태 1 포함); R 전체 alias 정확 위치 재확인 불가 |
| usage | 14행 | E2+E3 C, R E2 및 conditional paths, K E1/lazy+non-seaborn geometry, V own mark; E4 0 |
| routes | 12/12 | unique case×purpose 12/12 |
| 원장 연결 | 105개 ID 참조, missing 0 | 0 missing (CSV parse JS 검증, 별도 Python 검사 미실행) |
| 고유 계보 | 6 | C,K,V,R,S,M-Clare; 소비자 사건 4 + 음악 주 사건 1 + S upstream context; 보강 M-Bartok/M-Frost 별도 사건 산입 제외. 자료 수는 사건 수 아님 |
| E4 실행 증명 | 0/4 | 어떤 정확한 출판 그림도 동일 실행 로그를 관측하지 않았음. 요구상 E2까지만 허용. |

| Q | 직접 근거/위치 | 반례 찾은 원자료 | 결손/반증 |
|---|---|---|---|
| Q1 | [P01](https://joss.theoj.org/papers/10.21105/joss.07120.pdf) p1/p5/p6; [P02](https://joss.theoj.org/papers/10.21105/joss.08661.pdf) p1/p7; [P03](https://joss.theoj.org/papers/10.21105/joss.09037.pdf) p1/p7; [P04](https://www.research.unipd.it/retrieve/51d20577-f084-42f5-b411-281063d883e6/2019_Raincloud_plots_a_multi_platform.pdf) p14-20 | P01 비교+구현, P02/03 비교, P04 DOI 없음 | 비교=사용 반증; R 위치 전수 보류; 감사 없음 주장 조회 범위 한정 |
| Q2 | [T01](https://zenodo.org/records/14004295), [T02](https://zenodo.org/records/17855722), [T03](https://github.com/openjournals/joss-reviews/issues/9037), [T04](https://zenodo.org/records/1402959), [T05](https://zenodo.org/records/3368186), [T06](https://discovery.ucl.ac.uk/id/eprint/10178652/1/Allen_Raincloud%20plots.%20A%20multi-platform%20tool%20for%20robust%20data%20visualization_VoR.pdf), [S01](https://joss.theoj.org/papers/10.21105/joss.03021.pdf) | C14 후대판, C24 fallback | tag/date와 실행 버전 분리; 정확 설치 미확인 |
| Q3 | [C01](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/setup.py), [C04](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/pyproject.toml), [C24](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/kdiagram/__init__.py), [C12](https://github.com/RainCloudPlots/RainCloudPlots/blob/v1.0/requirements.txt), [C11](https://github.com/RainCloudPlots/RainCloudPlots/blob/v1.0/tutorial_python/raincloud_tutorial_python.ipynb), [C21](https://github.com/davibarreira/Vizagrams.jl/blob/v0.2.16/src/marks/boxplot.jl) | C05–07,C16–20 static plot modules; C23 doc | core/예제/lazy/indirect 구별; 전체 project no-call 증명 없음 |
| Q4 | [C22](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/paper_assets/paper_makefigures.py#L136-L179), [C26](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/paper.md#L246), P01 Fig5; C08 L245; C11 cells3,7,14,30 | C23 aspect, C14 save flag/title | E3 C figure path 성립, R candidate only; E4 0 |
| Q5 | [C16](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/kdiagram/plot/errors.py#L177-L350), [C21](https://github.com/davibarreira/Vizagrams.jl/blob/v0.2.16/src/marks/boxplot.jl), [C25](https://github.com/davibarreira/Vizagrams.jl/blob/v0.2.16/docs/src/gallery/boxplot.md), P02/03 | 같은 violin/BoxPlot name 자체 구현, R API no DOI, C23 doc | ref-only(본문 미언급 경쟁제품) 사례 미확정, K 전체 미호출 아님 |
| Q6 | [M01](https://blogs.loc.gov/music/files/2014/07/2014-2015-Concerts-from-the-Library-of-Congress-Brochure.pdf) pp28–29, [M02](https://blogs.loc.gov/music/files/2014/12/Fine-Program-Final.12.01.2014.pdf) pp27–29,35, [M03](https://blogs.loc.gov/music/2015/05/new-webcasts-available/) L320–332, [M09](https://www.clarecollegechoir.com/previous-engagements) L4369–4375/4541–4546 | M04 media date, F08/F12 failed, M05 other program | 연도 불일치 및 Bernstein 녹음 목록 미기재; 원녹음 직접 청취/세션 로그 미확인 |
| Q7 | routes.csv 12자리; RESULT 표3 | V/K background single link suffices, C22/P01 and R C11/C14 exact artifact | 목적별 링크는 설계 판단, 사용자 실험 미실시 |

검증: 원장 JSONL을 JS JSON.parse로 전행 읽음; CSV 모든 행을 quoted fields parser로 검사 및 ID/unique route 점검. raw output 재현, 외부 repo 전체 checkout/grep/AST, PDF full-text 재검증 및 녹음 청취는 실행하지 않았다. 모든 기록의 checked_at_utc는 확인 일자 수준; 초 단위 없음. 소스 65행은 실제 관측과 실패 중심이며 공개 페이지 landing/검색 preview 등 일부 탐색 흔적은 별도 세지 않았다. K/V의 이미지 원본 파일 및 해당 figure generator 미열람, PtitPrince tag F06 실패, F03 archive 제한. 고정 결과 SHA에서 대표 파일 재열람을 HANDOFF 전에 수행. 제품/순위 결정 보류.
