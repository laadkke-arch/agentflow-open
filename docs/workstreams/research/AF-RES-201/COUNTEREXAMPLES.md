# AF-RES-201 반증 및 변경 기록

직전 초안 TABLES_DRAFT.md (6562470a548408f69747df95d766e59d070053a0)는 보존, 아래 보정이 RESULT에 우선한다.

| 구판 판단 | 새 관측·판·정확 위치 | 보정 |
|---|---|---|
| C Fig5 코드·캡션만 연결 | [C22](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/paper_assets/paper_makefigures.py#L136-L175) 생성기와 [C26](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/paper.md#L212-L246) manuscript 동일 fig-plotting.png; 임시 PNG 결합. | E3 자산 경로 조인 성립. P01 height=4 vs script 5 vs [C23](https://github.com/retostauffer/python-colorspace/blob/v1.0.0/_quarto/articles/usewith_seaborn.qmd#L51-L74) 문서 aspect=1.5: 같은 그림과 같은 의도를 구분. 렌더 E4 없음. |
| K 설치 선언만 | [C24](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/kdiagram/__init__.py#L22-L65) `_lazy_import`는 실제 import_module을 closure에 담아 이름 등록; required list includes seaborn. | import 실행이나 그림 기능 소비로 승격하지 않는다. tag 내부 fallback 1.3.5.dev0도 version metadata 단독 불충분 사례. |
| K polar violin 함수 미확인 | [C15](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/kdiagram/plot/__init__.py), [C16](https://github.com/earthai-tech/k-diagram/blob/v1.3.4/kdiagram/plot/errors.py#L177-L350) optimized positive/negative KDE→theta/r→ax.fill; basic 분기도 scipy/ax.fill. | 구체적 동명 도형 독자 구현; Fig2(b) generator/mode 미확인 유지. 8 plot modules(C05-07,C16-20)에서 직접 seaborn/sns 토큰 미발견; 프로젝트 전체 부재로 일반화 금지. |
| V module 수준 비교만 | [C21](https://github.com/davibarreira/Vizagrams.jl/blob/v0.2.16/src/marks/boxplot.jl), [C25](https://github.com/davibarreira/Vizagrams.jl/blob/v0.2.16/docs/src/gallery/boxplot.md), C10 L126-131 | Julia BoxPlot 실제 own mark로 역할 분리; 도형 명칭/동일 미학은 API 계보 증거 아님. |
| R 초판·후대 그림 번호 연결 가능성 | C11 vs C14: 2018 savefigs=False, 2019 True; figure12.png vs figureP13.png. | 후대 코드·그림 번호로 초판 행위 증거를 덮지 않는다. |
| 공연 예정 목록=연주 | [M01](https://blogs.loc.gov/music/files/2014/07/2014-2015-Concerts-from-the-Library-of-Congress-Brochure.pdf) pp28-29; [M02](https://blogs.loc.gov/music/files/2014/12/Fine-Program-Final.12.01.2014.pdf) pp27-29,35; [M03](https://blogs.loc.gov/music/2015/05/new-webcasts-available/) L320-332; [M09](https://www.clarecollegechoir.com/previous-engagements) L4369-4375/L4541-4546; M04 media catalog | 같은 공연의 날짜·합창단·장소·작품 매칭, 2015 표기 충돌. 예정 Bernstein은 공개 목록에 없음: 미연주·편집·누락 모두 가능. Britten/Harrison 1942/1955 편곡 별도. 음원 F08/F12 실패, 실제 재생 증거 없음. |

보수 집계: {"paper":4,"code":24,"release":8,"seaborn":3,"music":4} / 총 43 고유 자료, 원장 65행. C08/C26 manuscript는 논문과 내용 중복으로 산입 제외; M04는 직접 원음이 아니라 보강. M09는 공연자 원기록. 원음 없이 녹음 제목을 공연 전체와 동일시하지 않는다. 이번 범위를 넘는 결과 확정이나 제품 구조 결정 없음.
