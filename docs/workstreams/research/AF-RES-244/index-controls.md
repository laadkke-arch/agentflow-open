# Index controls — AF-RES-244 (④ counterexample)
## 생성자 관점: 참조 관계 vs 실행 관계
정확한 HTML publisher 1.6.1, tag 1.6.1 f159b78dc59f250cdde8fe391a21f0bc871960ad; SG 최소 0.17.1 (비교 태그 v0.17.1 1a1e728df84b7b140989e9a4789c084a086dfbea, 설치판 미확인).
- S1 https://github.com/scikit-learn/scikit-learn/blob/1.6.1/doc/conf.py#L691-L715 : globals 검사 False, 이름 모듈 sklearn, gallery 및 backref 경로. S4 https://github.com/sphinx-gallery/sphinx-gallery/blob/v0.17.1/sphinx_gallery/backreferences.py#L41-L170 : import map과 accessed names 구별; AST 참조는 호출이나 실행 여부가 아니다. L204–289 text role regex, L348–405 thumbnail backrefs.
- S5 https://github.com/sphinx-gallery/sphinx-gallery/blob/v0.17.1/sphinx_gallery/gen_rst.py#L1230-L1259 : globals 조건, normalization, filter; S7 https://github.com/sphinx-gallery/sphinx-gallery/blob/v0.17.1/sphinx_gallery/directives.py#L102-L193 : minigallery 이름 또는 file/glob. R1/R2/R3 published RST 실제 name arguments만, 명시 파일 경로 없음.
- S6 https://github.com/sphinx-gallery/sphinx-gallery/blob/v0.17.1/sphinx_gallery/tests/test_backreferences.py#L181-L279 : 실제 테스트의 implicit print(c), explicit role, non-role/! exclusion을 읽었다. 테스트 기대이지 실행 영수증 아님.
| 조건 | 판독 | 양성/음성 반전 조건 |
|---|---|---|
| from sklearn.neighbors import NearestNeighbors; 그 뒤 아무 참조 없음 | import map만, accessed_names 없음: 음성 후보 | alias 사용 또는 명시 role 추가 시 양성 후보; actual SG test 미실행 |
| import 후 print(NearestNeighbors) | 이름 접근 양성 (S6 print(c) 유사) | 호출이 없어도 index 가능 |
| 코드 없이 설명문 :class:`~sklearn.neighbors.NearestNeighbors` | 명시 role 양성, E1 L292/296 실제 소스와 일치 | role 제거 후 해당 backref 사라질 것으로 예상; 문자열 label L217만은 별도; actual _codeobj 미확인 |
| 평문 NearestNeighbors / inline literal / ! 억제 role | S6 test negative; literal와 role 구분 | default_role 또는 다른 role에 따라 달라짐 |
| fit 후 kneighbors(...) 호출 뒤 값 무대입 | E8 L585–591: precomputed sparse test의 무오류 확인, 두 반환을 버리는 실제 code | 거리·인덱스를 별도 unpack/출력하면 목적 직접성 상승; 실행 여부 미확인 |
| kneighbors(X)[0] | E8 L2155–2166: 거리만 brute와 ball_tree 비교, 행 index 소비 안 함 | [1]도 검증하거나 tuple unpack |
| return_distance=False | I2 L274/I12 L118: 거리가 반환되지 않는 별도 유형(버려진 반환과 구분) | True와 두 배열 소비 |
| 내부 호출/객체 이름 | E1 TSNE internal distance graph (I8), C2 score internal labels (I10,I5), E2 SFS internal score (I7) | user-facing tuple/label을 노출해야 직접 목적 충족 |
| 다른 graph API | E9 KNeighborsTransformer(mode=distance) + precomputed KNC; 함수 kneighbors_graph 사용 아님 | public graph function 명시 |
| graph input axis | G1,G2 sample rows. X.T로 feature graph를 만들면 동일 함수라도 목표 표본 ID와 불일치; 설계 반례, 실행 미실시 | sample rows shape, axes metadata 확인 |
| graph mode | G1,G2 connectivity, distance 없음. G2 평균 대칭화 .5/1 가중치와 I9 metric distance 재계산 | mode=distance 명시, graph.data 비교 |
| 높은 순위 | C1 release highlights 첫 자리, C7 E6 명시 predict grid | 사용자 목적별 rerank; 출판 순위 자체는 품질 판정 아님 |

## 저자 vs 개발자
E4 원문 설명 20 nearest neighbors와 실제 L55 k30 불일치: 이 기록의 인자값은 실행 코드 30을 우선. E6 L62–86 명시 predict 응답으로 class-coded grid를 그림에 쓰므로 C2의 binary probability plot과 다르다; 다만 임의 사용자의 개별 입력·레이블 회수 코드가 아니라 그리드 시각화. E8 L1444–1473은 함수 dual mode 실제 assert 코드(미실행)로 G1/G2의 결손을 메움. I11 L290–309는 거리와 인덱스를 실제 후속 LOF 계산에 소비하는 양성 구현이지만 N1 예제가 이를 보여 준다는 근거가 아니다. I13/I14 파일에서 kneighbors 직접 호출 탐색은 발견 못함, 전수 검사는 아니다. 예제 author 의도(성능/특징선택/비교/구조)와 사용자 목적(짧은 실행 가능한 조각)의 직접성을 별도 태그.

## Q6: MeSH 실제 두 원레코드의 보존 사본
M1 https://dtd.nlm.nih.gov/ncbi/pubmed/doc/out/250101/att-MajorTopicYN-c.html L6–20: Y/N default N, publication에서 유의미한 점인지 표시. M2 https://pubmed.ncbi.nlm.nih.gov/help/ L1732–1755: [majr]와 [mh], descriptor/subheading 조합, hierarchy expansion. M3 https://dataguide.nlm.nih.gov/classes/edirect-for-pubmed/samplecode4.html Major Topics 숙제: Descriptor Y 또는 Qualifier Y의 조합을 major로 추출. M4 https://dataguide.nlm.nih.gov/classes/intro/samplecode.html Version 3: check tag가 major일 수도 있음. M5 DTD DescriptorName 예제 N은 실제 PMID 전체 레코드 아님.
| 원레코드·계보 | 실제 XML locator | DescriptorName text | MajorTopicYN | qualifier/주의 |
|---|---|---|---|---|
| PMID12091962, MEDLINE, Owner KIE, revised 2007-11-15; M6 | [pubmed1.xml L60–99](https://github.com/biopython/biopython/blob/biopython-185/Tests/Entrez/pubmed1.xml#L60-L99) L63 | Acquired Immunodeficiency Syndrome | Y | 사본 DTD 2008, raw record attribute |
| 동일 PMID | L72 | Humans | N | 같은 기록 내 N |
| 동일 PMID | L96 | Prisoners | Y | Y가 복수일 수 있음 |
| PMID11748933, MEDLINE, Owner NLM, revised 2006-11-15; M7 | [pubmed2.xml L101–140](https://github.com/biopython/biopython/blob/biopython-185/Tests/Entrez/pubmed2.xml#L101-L140) L101 | Animals | N | 사본 DTD 2008 |
| 동일 PMID | L108–109 | Cryopreservation | N | QualifierName methods Y; descriptor N만으로 조합 not major 판정하면 틀림 |
| 동일 PMID | L135 | Sperm Motility | Y | descriptor 직접 Y |
| 보강 PMID9997 M8, Owner NLM | [pubmed1.xml L230–240](https://github.com/biopython/biopython/blob/biopython-185/Tests/Entrez/pubmed1.xml#L230-L240) L233–234 | Chromatium | N | QualifierName enzymology Y |
NLM bibliographic records → historical PubMed XML → Biopython test fixture carrier → tagged file blob (M6/M7). 원래 NLM 제공시점/다운로드 영수증 미확인. 자료 2개(별개 PMID) 역사적 XML 필드 직접 읽음, current provider direct 0/2. F1–F8 접근 실패/본문 차단, 정상 0 record 아님. DTD 2025와 2008 fixture 버전을 혼합하지 않음. strict source count에서 사본 제외; XML 원응답 2개 확보 필요. 교육 문서 예시나 현행 HTML 별표는 raw XML 대체 불가. 의료 판단이 아니라 색인 구조 비교. 주제 중심성의 flag는 코드의 실행/소비/목적 적합성 flag와 다른 의미 축이다.

## 미실행 검증 입력
- SG 통제: 정확한 release build SG 버전부터 확인; 동일 config inspect_global_variables=False, doc_module=sklearn. 최소 gallery (1) unused import (2) print class (3) explicit role only (4) plain text only (5) actual fit/kneighbors discarded (6) explicit file path directive; 각 _codeobj 및 *.examples, HTML anchor 순서, stdout/stderr를 보관. 가설: (2)(3)(5) 양성, (1)(4) 음성, (6) 명시 포함; 실제 반전되면 S4–S7 해석을 변경. N1 role 삭제/복원 차이로 유입 경로 확인.
- Graph: E8 L1444–1473 X=[[0,1],[1.01,1],[2,0]], k1, connectivity self True -> eye; distance self False -> [[0,1.01,0],[1.01,0,0],[0,1.40716026,0]]. k2 양 mode는 소스 assert. 반환 shape/CSR/data/indices 확인; 동점 없는 fixture. 동일 sample X.T 별도 feature graph 반례 입력이며 본표 아님. 정확판 테스트 실행과 version/return/exit/receipt는 HANDOFF.
