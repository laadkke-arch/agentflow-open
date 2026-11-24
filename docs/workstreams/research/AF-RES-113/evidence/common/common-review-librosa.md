# librosa 공통 시작 절 판독 — 두 번째 링크 개봉 전

판독자: `recruit_librosa`, 별도 자동 문맥. 2026-11-24 UTC. 원 요청과 배포 API 본문·같은 고정판의 해당 docstring만 읽었다. 원 구현, 회귀시험, 예제 페이지, 논문 목적지는 열지 않았다. 상세 원장은 [librosa-common.json](librosa-common.json)이다.

## 고정 입력과 실제 목차 이동

librosa 1.0.1, 태그 커밋 `9caf46a4ecaeb8ea24bb541231065c9f761174ae`를 사용했다. 이 판의 [API 목차](https://librosa.org/doc/1.0.1/api/index.html)에서 R1은 `core.html`(DOM href3) → [Core functionality](https://librosa.org/doc/1.0.1/api/core.html)의 `generated/librosa.stream.html`(href7), R3은 API 목차의 `generated/librosa.segment.recurrence_matrix.html`(href67)로 이동했다. 해당 심벌의 `dl.py.function`만 공통 본문으로 추출했다.

| 요청 | 원 작성자 링크와 연구자 시작점 | 공통 노출 | A | B |
| --- | --- | --- | --- | --- |
| R1 · #1641 | 원 글에는 URL 없음. 연구자가 목차에서 [stream](https://librosa.org/doc/1.0.1/api/generated/librosa.stream.html#librosa.stream)을 찾음 | 5,172 Unicode code points; signature, caveat6개, Parameters, Yields, See also, inline Examples 두 개 | 공석: 연결된 독립 예제 없음 | 공석: 방법 원저작 링크 없음 |
| R2 · #1648 | 원 작성자는 [mir_eval.sonify.pitch_contour](https://craffel.github.io/mir_eval/#mir_eval.sonify.pitch_contour)를 지목. librosa 목표 public symbol은 없음 | 공통 API 자리 공석. mir_eval 목적지는 열지 않음 | 공석 | 공석 |
| R3 · #1651 | 원 작성자 링크 두 개는 과거 segment.py 코드판. 연구자가 목차에서 [recurrence_matrix](https://librosa.org/doc/1.0.1/api/generated/librosa.segment.recurrence_matrix.html#librosa.segment.recurrence_matrix)를 찾음 | 6,857 code points; bandwidth의 문헌목록과 inline Examples까지 포함 | 공석: 연결된 독립 예제 없음 | [Wang et al. DOI](https://doi.org/10.1038/nmeth.2810), 함수 dl의 href10. 아직 개봉하지 않음 |

R1 본문 지문은 `86264ecd29a0880761f82eedf189f93e248f794d4c7d275d2f9c8f0a7c596e1e`, R3은 `093c31078f6b21e103610eb065f1243e86babad9f678a15b6984698fad03108c`이다. 두 페이지는 각각 함수 dl 안에 14개 href가 있다. 실제 배포 HTML 전체에 `Examples using ...` 절이나 gallery thumbnail은 없다. 페이지 메뉴의 `librosa.util.example`, `example_info`, `list_examples` API 링크를 사용 예제 이동으로 간주하지 않았다.

R3의 먼저 나오는 `#z` 문헌은 Zelnik-Manor·Perona의 2004년 저작을 이름으로 소개하지만 원저작 외부 href가 없다. 검색하여 그 빈 링크를 수리하지 않았다. `#w`의 Wang2014 DOI가 문서 순서상 처음 실제로 연결된 원저작이며, `mean_k_avg`와 `mean_k_avg_and_pair` 설명에 방법 계보가 명시되어 있다. 이는 단순 배경 읽을거리와 구별된다.

## 이미 공통 노출이 지지하는 선택과 시험

R1에서는 1.0.1이 자동 표본율 변환을 지원하고 `(block_length * hop_length * native_sr) / sr`의 정수 조건을 명시한다. `sr=None`이면 native rate를 사용한다. 원 글의 `block_length=10, frame_length=hop_length=16000`는 전체 블록 최대160,000표본이다. 가정한 입력이44.1kHz이고 `sr=None`이면 약3.6281초, `sr=16000`이면10초가 된다는 비교는 공통 식에서 이미 나온다. 이 계산은 구성 입력에 대한 예상이고 실행 결과가 아니다. 원 MKV의 codec/native rate나 tokenizer 조건은 아직 알 수 없다.

같은 공통 절은 decoder의 허용 범위를 soundfile 지원 codec으로 제한한다. 따라서 sample-rate·블록 경계를 조정하면 원 글의 unknown-format 오류도 해결된다고 주장할 수 없다. 형식 적합성과 downstream chunk 처리를 따로 검사해야 한다. 끝 블록의 padding 선택, 내부 블록 경계에서 `center=False`, 조기 반복 중단 때 generator `.close()`도 이미 공통 내용이다. 이를 나중에 A/B의 새 발견으로 세면 안 된다.

R1의 STFT inline Example은 stream의 `frame_length=4096, hop_length=1024`를 적지만 분석 호출에는 `librosa.stft(y_block, center=False)`만 적는다. 그 호출의 실제 default frame/hop이 stream 설정과 맞는지는 이번 공통 판독에서 확인하지 않았다. 후속 원전 대조 단계의 명확한 검사 후보다. mel Example은 `n_fft=2048, hop_length=2048`을 명시한다. 이 차이는 예제 페이지를 따로 연 결과가 아니라 공통 절에서 직접 본 코드이다.

R2의 `nan_to_num` 우회, `nancumsum` 제안, frame grid는 모두 원 글에 있다. 목표 public symbol이 없는 자리를 `pyin`이나 현재 구현의 다른 함수로 바꾸지 않았다. 유성·무성 구간의 phase 연속성과 실제 합성파형은 미확인이다.

R3의 scalar NaN-ignore와 individual/pairwise no-neighbor 오류 보존은 이미 원 글의 제안이다. 공통 절은 arithmetic/geometric local scale, 평균-k 거리, pair 거리 추가까지 설명하므로 그 수식도 B 신규 발견이 될 수 없다. 예를 들어 kth 거리1·4와 pair 거리2에서 arithmetic bandwidth2.5의 affinity는 약0.449329, geometric bandwidth2의 affinity는 약0.367879라는 예상은 공통 정의만으로 계산된다. 실제 실행은 하지 않았다.

R3의 구성 시험으로 `data=[[0,0.1,100]], k=1, sym=True, width=1`에서 singleton과 상호 이웃 쌍이 생기는지 먼저 확인한 뒤 scalar/pairwise 실패 책임을 비교할 수 있다. 실제 neighbor graph와 현재 구현 결과는 아직 검증하지 않았다. `full=True`는 width를 무시한다는 사실도 공통 절에 이미 있으므로, 빈 행을 없앤다는 이유만으로 보존 조건을 지키는 수정이라고 받아들일 수 없다.

## 배포 HTML과 같은 태그 docstring 대조

원 소스는 전체 파일을 기계적으로 취득한 뒤 AST로 해당 함수의 docstring만 추출하여 읽었다. source implementation 내용은 판독하지 않았다. 문서와 docstring의 독립 고유 저작 수는 중복 산입하지 않는다.

| 대상 | 같은 고정 SHA 원 소스 범위 | 확인과 한계 |
| --- | --- | --- |
| stream | [librosa/core/audio.py](https://github.com/librosa/librosa/blob/9caf46a4ecaeb8ea24bb541231065c9f761174ae/librosa/core/audio.py), 함수223행, docstring237–384행 | 자동sr·정수 조건·close·codec·블록 식과 inline 예제가 배포 HTML과 의미상 일치. docstring6,150자와 HTML5,172자는 RST/indentation·signature·fragment 추출의 차이이며 byte동일을 주장하지 않음 |
| recurrence_matrix | [librosa/segment.py](https://github.com/librosa/librosa/blob/9caf46a4ecaeb8ea24bb541231065c9f761174ae/librosa/segment.py), 구현 선언375행의 docstring389–579행 | local-scale 정의, 먼저 나오는 unlinked2004 문헌, Wang DOI, full/width와 inline 예제 일치. docstring7,724자와 HTML6,857자는 추출 표면 차이 |

recurrence_matrix의 첫 AST 추출은345행 overload를 집어 docstring이 `None`인 데서 TypeError가 발생했다. 동일 캐시의375행 docstring을 가진 선언을 선택해 재추출했다. 새 원문을 열거나 구현을 판독하지 않았으며 실패·수정 사실은 JSON에 보존했다.

## 이 단계의 대사

- 예정 요청3, 공통 시작 가용2, 공통 시작 공석1.
- 예정 추가 열람6자리: A 가용0, B 가용1, 공석5.
- 추가 링크 실제 열람0, 구현·회귀 독해0, 원 프로젝트 실행0.
- API 목차2개, 공통 함수2개, 같은 태그 docstring2개를 직접 읽었다. 목차와 같은 저작 docstring 재표현으로 자료 하한을 부풀리지 않는다.
- 후속 채택, 2023 당시 입력의 최초판, 현재 원 MKV 실제 호환성과 실제 수치 결과는 미확인이다.
