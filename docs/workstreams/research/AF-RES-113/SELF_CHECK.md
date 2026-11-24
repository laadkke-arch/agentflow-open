# AF-RES-113 SELF_CHECK — 작업공간 장애 후 재구성본

연구 상태는 **PARTIAL**이다. 고유 자료 배당 24개는 확보했지만, 예정 6요청에서 양쪽 추가 본문을 모두 읽은 비교쌍은 0개다. 9공석과 초록만 도달한 1건을 유효한 비교에서의 효과 0으로 취급하지 않는다. 본문은 연구 근거의 자기점검이며, **최종 결과 SHA에 대한 manifest·저장소 공통 검사 통과를 아직 주장하지 않는다.** 실제 검사는 결과를 원격에 고정한 뒤 `evidence/acceptance-evidence.json`에 기록한다.

## 재구성의 근거와 한계

2026-11-24 약 05:02 UTC에 보고된 scratch 초기화로 아직 커밋하지 않은 이전 SELF_CHECK와 방법론 감사문이 소실됐다. 이 파일은 원격 `d50b27c5b082dbf24f6cb5508dbf9914fc1f12c6`에서 복구된 원장·영수증과 같은 감사자의 대화 기록을 다시 대조해 **새로 작성한 문서**다. 소실된 로컬 파일과 byte가 같다는 주장, 소실 파일을 이미 원격에 커밋했다는 주장은 하지 않는다. 장애·재취득 근거는 `evidence/corrections/workspace-recovery.json`에 있다.

초기 공통은 `96a754e80f9bbeb5f65e544f7e7f81457b245971`, 추가 노출은 `11287afdf0c3a0d990f125b72c4f75e9af42f38f`, 사전 판단은 `0b6287e5359257004900ef4b8e30f7abb7306024`에 보존돼 있다. d50에는 원전 대조, R6 v2 공통 정정, 초기 A/B 판단이 남아 있다. 초기 판독과 사후 정정을 합쳐 처음부터 같은 입력을 읽은 것으로 설명하지 않는다.

복구판의 `sources.jsonl` 95행과 고유 배당 24개를 직접 확인했다. 장애 전 130행까지 보완했다는 대화 기록은 현재 파일의 행수 대신 사용하지 않는다. 복구·재열람에 따라 늘어나는 최종 행수, 고유 저작·사건·URL·시도 수는 **`evidence/source-census.json`**과 그 입력 SHA에서 대사한다. 원장 행수와 직접 읽은 독립 저작 수는 다르다.

## Q1–Q7 근거·반증 점검

| 질문 | 답 또는 미확인 | 직접 읽은 URL·절 또는 실행 원장 | 반증을 찾은 곳과 확인한 내용 | 원래 분모·실제 분모·결손 | 판단을 바꿀 다음 관측 |
| --- | --- | --- | --- | --- | --- |
| Q1. 이미 아는 안과 앞둔 결정 | 각 프로젝트의 생성순 첫 60건에서 구체적 처리 기능·변경·보존 조건을 갖춘 첫 3건을 선택했다. R1 MKV chunk, R2 f0 합성, R3 scalar/지역 bandwidth, R4 차원 오류, R5 경계 처리, R6 dtype·수치 roundtrip이다. 현재 원글 snapshot이며 작성 당시 원판은 미확인이다. R2의 독립 보존 조건은 경계 사례다. | `frame.csv`, `requests.jsonl`, `evidence/recruitment/*/acquisition.json`; REQ-R1 [#1641](https://github.com/librosa/librosa/issues/1641)의 load/stream/tokenizer, REQ-R2 [#1648](https://github.com/librosa/librosa/issues/1648)의 solution 항목1·2, REQ-R3 [#1651](https://github.com/librosa/librosa/issues/1651)의 scalar/pairwise 구분, REQ-R4 [#6664](https://github.com/scikit-image/scikit-image/issues/6664)의 분기 코드, REQ-R5 [#6665](https://github.com/scikit-image/scikit-image/issues/6665)의 footprint/neutral 값, REQ-R6 [#6670](https://github.com/scikit-image/scikit-image/issues/6670)의 LF19–27. | 첫 적격 전 제외 7행을 다시 대조했다. R2에는 이미 mir_eval 구현이 있으므로 ‘알려진 구현 없음’은 기각한다. Scoop 제거는 변경 요구다. 그것을 보존 조건으로도 세면 안 되며, 기존 합성 유지 자체만으로 별개 보존 조건을 만들지 못한다는 SCOPE 조항과 긴장이 남는다. 사후 댓글·문헌 풍부함으로 표본을 바꾸지 않았다. | 프레임 120=60+60. 정식 판정 13=librosa 8+skimage 5; 선택 6·제외 7·이후 미선별 107. batch 본문 노출은 22이며 정식 판정 13과 다르다. 60번째 생성일은 각각 2023-08-04·2023-04-08이므로 2024 전체 대표성을 주장하지 않는다. | R2의 변경과 구별되는 보존 조건을 원문 문장에 대응시키는 독립 코딩. 엄격 판정에서 부적격이면 새 모집판과 원순서 재선별이 필요하고 임의의 다음 이슈로 교체하면 안 된다. 역사적 지식은 당시 본문판이 있어야 판정할 수 있다. |
| Q2. 같은 시작 절과 분기점 | 고정판은 librosa 1.0.1과 skimage 0.26.0이다. 현재 공통 시작은 5/6. R2만 지정된 librosa public 목표 심벌이 없어 공석이다. R6는 문자순 첫 목표 lch2lab이므로 초기 복합조작 공석을 철회했다. | [librosa API 목차](https://librosa.org/doc/1.0.1/api/index.html), [skimage API 목차](https://scikit-image.org/docs/0.26.x/api/api.html), `evidence/common/*-common.json`, `evidence/corrections/R6-v2.json`, V-R6-COLOR-API [lch2lab 절](https://scikit-image.org/docs/0.26.x/api/skimage.color.html#skimage.color.lch2lab) 전체 1262자·href 6개. | 복수 심벌에 대한 첫 목표 규칙이 있으므로 두 함수라는 사실만으로 R6 대응을 포기한 것은 과도했다. 원글 LF22의 rgb2lab은 입력 준비, LF25가 왕복 목표다. LF24 dtype assert는 lab.dtype이며 최종 lab2 dtype 검사가 아니다. R5 maximum 문구는 배포 HTML과 같은 태그 docstring 양쪽에 있어 단순 HTML 변환 오류 설명도 배제했다. | 초기 공통 4/6→v2 5/6. R6 1262자는 초기 packet에 없던 사후 공통이다. R2 공석은 ‘기능 없음’이 아니라 지정 프로젝트의 목표 심벌 대응 없음이다. 고정 tag와 가변 배포 URL은 같은 종류의 고정점이 아니다. | 원글에서 더 이른 목표 조작임을 보여 주는 직접 근거, 같은 판의 정확한 API 대응, 또는 원본과 다른 본문 지문. R2를 mir_eval이나 pyin으로 바꾸려면 별도 범위판이 필요하다. |
| Q3. 두 번째 열람의 실제 내용 | A의 두 예제 본문 접두사, B의 한 초록/구독 preview를 각 3000 유니코드 문자·그림 0으로 읽었다. R6 v2는 inline 예제만 있고 적격 독립 예제/원저작 연결이 없어 추가 0이다. | `hops.jsonl` 12행, `evidence/hops/`의 도착·추출 보정·지문, `evidence/arms/{A,B}/judgment.json`. [R4-A Rank filters](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_rank_filters.html), [R5-A Cornea](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_cornea_spot_inpainting.html), [R3-B DOI](https://doi.org/10.1038/nmeth.2810)→Nature preview. | R5의 처음 2261자 잘림과 R3 인코딩 문제는 같은 응답 byte에 동일 parser 규칙을 적용해 보정했고 초기 공통 지문은 변하지 않았다. 먼저 적힌 unlinked 논문, 뒤의 더 유용한 gallery, 인접 함수의 출전을 원경로에 편입하지 않았다. R6 EasyRGB는 시작절의 원제안자 귀속 부재로 제외했으며, 열지 않은 목적지가 비원전이라고 단정하지 않았다. | 예정 12·실제 추가 노출 3·본문 접두사 2·초록만 1·공석 9. 초기 공석 원인은 시작 4+링크 5, 정정 후 시작 2+링크 7이다. 최초 추가 독해 9000자와 사후 열람은 별도다. 양쪽 본문 비교쌍은 0/6이다. | 동일 요청·시작·예산 아래 두 적격 본문을 실제 읽은 쌍. 실패 후 미러는 보조 탐색으로 남기며 첫 시행의 도달 상태를 소급 변경하지 않는다. |
| Q4. 새 선택과 구별 입력 | 최초 추가 접두사가 목표 변경과 보존 조건을 함께 지지한 새 선택 0·새 시험 0. 기존 안/시험 13행과 R6 v2 공통 계약 1개를 홉 성과로 세지 않는다. R3의 최초 3점 public 후보는 고정 소스의 width guard 때문에 기각했다. | `decisions.csv`, `evidence/common/baseline-tests.jsonl`, `R6-v2.json`의 R6-V2-COMMON-SHAPE, `evidence/verification/project/executed-checks.json`. [고정 segment.py](https://github.com/librosa/librosa/blob/9caf46a4ecaeb8ea24bb541231065c9f761174ae/librosa/segment.py)의 LF580–670, 특히 LF588–593; 재취득 지문은 `workspace-recovery.json`. | 3점 data=[[0,.1,100]], width=1은 t=3에서 width≥(t−1)//2 조건으로 그래프 전에 거부된다. 이미 실행한 고립 helper의 3×3 CSR 관측과 구별한다. 5점 data=[[0,.1,10,10.1,100]], k=1, width=1, sym=True는 이 guard만 통과하며 public 그래프/affinity는 미실행이다. R1 center=False만으로 창 간격이 맞지 않고, R5 문구상 maximum은 구현 중립값과 반대였다. | 예정 경로 12·추가 노출 3·목표 적합 신규 0. 비교쌍 0이므로 쌍별 효과율은 정의 불가다. 초기 13행 중 3점 후보를 ‘유효 public 최소입력’으로 세면 안 된다. source 관측·구성 예상·부분 실행을 따로 유지한다. | 같은 판의 public recurrence_matrix에 유효 입력을 실행해 실제 neighbor graph와 scalar/pairwise 결과를 확인하는 것. 원 MKV·Csync·s390x 관측이 구성 예상과 다르면 해당 판단을 바꾼다. |
| Q5. 공여 분야와 이동 전제 | 방법 제안자의 원전 6개, 외부 적용/실패 자료 4개를 본문까지 읽었다. 같은 분야 구현, 직접 계보, 분야 간 관계 유사성, 배경 인용을 분리했다. 외부 자료는 전부 사후 검증이다. | 아래 방법 6·외부 4 목록의 source_id·URL·절. NET-METHOD-SNF Online Methods, NET-METHOD-STFT §II–IX, M-IMG-GIL p1607의 border 제외, M-IMG-PYE Eq24, EXT-ACOUST-FARINA2007 §3.4, EXT-MAP-OGC11 부록B.2.2와 EXT-MAP-GDAL33의 Rationale/CompatibilityIssues. | 0 국소척도·빈 이웃·뷰별 표본 ID 불일치, 규칙 표본 전제, sparse footprint를 연속 창으로 바꾸는 support 손실, 중심 창의 미래 참조를 반례로 조사했다. 일정 시계 비율 보정은 불규칙 timestamp를 고치지 않는다. 반 픽셀 위치와 영상 바깥 값 선택도 다른 책임이다. SNF의 유전체 적용을 원리의 최초 분야로 바꾸지 않았다. | 고유 방법 6/6, 외부 4/4=음향측정 2+지도표본화 2. 두 Farina 저작은 같은 저자의 후속, 지도 둘은 표준→구현 계보이며 독립 4집단이 아니다. SNF 방법은 웹 PDF 텍스트로 읽었지만 식의 시각 검사는 실패했다. | 대상의 객체·관계·보존량을 원전의 입력 전제에 직접 연결하는 사례. 실제 불규칙 시간축, 생성기 버전이 알려진 PixelIsPoint, sparse footprint, 같은 표본 ID의 다중 뷰가 최소 입력이다. |
| Q6. 반례와 한 링크의 충분성 | 부정 판정은 첫 연결 링크의 제한된 접두사와 해당 요청에 한정한다. 예제 전체의 무용함, 원전의 일반 우월성은 판정하지 않는다. 공통 절이 이미 선택/시험을 제공하면 추가 링크의 새 역할은 별도로 입증해야 한다. | V-LATE-HOP-R4-A의 문자11300–13200, V-LATE-HOP-R5-A의 뒤 절·실패 좌표, V-MORPH-GALLERY, M-IMG-OTSU §II, M-IMG-GIL §1·6, Farina2000/2007, GDAL RFC33. `evidence/verification/imaging/audit.md`. | 현장 사용자: RFC33 수정은 과거 생성 파일 호환성을 깨뜨릴 수 있다. 구현자: R5 문서와 구현의 중립값 불일치, R1 창/hop 불일치, R3 public guard를 확인했다. 원분야 저자: Farina 후속은 초기 clock 견고성을 제한하고 Gil–Kimmel은 R5가 묻는 경계를 명시적으로 제외한다. Cornea 뒤 절은 실제 잃은 점과 대안을 준다. | 원 요청 6개에 대한 보편 효과는 측정하지 못했다. A2의 뒤 절 재열람은 최초 노출에 합치지 않는다. 링크 부재·초록 부족·본문의 목표 부적합은 서로 다른 실패 원인이다. | 같은 최초 예산 안에서 목표를 가르는 예외·작동값이 발견되거나, 제외 출전이 시작절에서 원저작으로 명시됐다는 직접 증거. 달라진 입력판은 새 판단으로 기록한다. |
| Q7. 반환과 실제 후속 | 실제 시작 URL·추가 링크의 목표 적합성·접근 상태를 함께 반환한다. R1/R3/R4의 공통 시작은 알려진 선택을 설명하지만 실제 수리 보증은 아니다. R2 심벌 대응 보류, R5 문구 모순 주석, R6 shape 계약과 미확인 수치 수리를 구분한다. 원 사용자의 연구 링크 채택은 모두 미확인이다. | `baselines.csv`, `hops.jsonl`, `decisions.csv`; COMMENT-2034816835의 R2 동일 저자 발언, COMMENT-1382729471의 R5 mode 선호, R4 관련 댓글. 최종 반환 표는 같은 6요청·12자리에서 재구성해야 한다. | 현재 코드가 원 제안을 담았다는 사실은 이번 링크로 인한 채택 증거가 아니다. R2의 PR 제출 발언만으로 실제 diff·구현 완료를 확인했다고 할 수 없다. R5는 기본값 변경보다 mode 노출을 선호한 반대 의견이 있다. R3의 무효 3점 후보를 실행 명령으로 그대로 반환하면 안 된다. | 요청 6개를 모두 유지한다. 읽을 수 있는 쌍의 분모는 0; A만/B만/양쪽/둘 다 없음의 관측 0과 비교불가 6을 나눈다. 링크 존재 3·새 결정 0·후속 미확인은 별개다. | 날짜가 맞는 동일 사람의 노출 발언과 실제 변경, 또는 원 요청 입력에서 보존 조건을 지킨 실행 출력. 그런 증거 없이 수리·채택·경로 우열을 확정하지 않는다. |

## 고유 배당 24개의 단위와 실제 읽은 원전

| 배당 | 고유 수 | 산입 ID와 제한 |
| --- | ---: | --- |
| 신규 원 요청 | 6 | REQ-R1…REQ-R6. 현재 공개 opening body이며 작성 당시 최초판은 미확인이다. |
| 원 프로젝트 자료 | 8 | LIB-COMMON-STREAM, LIB-COMMON-RECURRENCE, R4-COMMON, R5-COMMON, HOP-R4-A, HOP-R5-A, V-STFT, V-MORPH-GALLERY. 함수 문서·독립 예제 단위이며 8개 독립 연구집단은 아니다. |
| 방법 제안자 원전 | 6 | 아래 방법 6개. 미러·초록·같은 저작 재열람은 중복 산입하지 않는다. |
| 외부 적용·실패 자료 | 4 | 음향측정 2, 지도표본화 2. 발견 봉인 뒤 읽은 별도 비교자료다. |

같은 함수의 HTML/docstring/구현을 다른 URL이라는 이유로 여러 고유 저작으로 세지 않는다. R6 v2 기능 문서는 미리 정한 project 8개 이외의 검증 단위로 보수적으로 산입하지 않았다. Soille2002 survey, 실패·검색 요약만 읽은 후보도 방법 6개에 넣지 않았다. A 두 갤러리는 본문 접두사를 직접 읽은 자료이며 전체 완독으로 표시하지 않는다. 산입 규칙과 계보를 바꾸면 같은 원장에서 전체 수를 다시 계산해야 한다.

| 방법 근거 ID | 직접 읽은 원문·절 | 확인한 내용과 적용 한계 |
| --- | --- | --- |
| NET-METHOD-SELF | [Zelnik-Manor·Perona2004](https://proceedings.neurips.cc/paper_files/paper/2004/file/40173ea48d9567f1f393b20c855bb40b-Paper.pdf), 전체 8쪽·부록A, Fig2·식1–2 | 국소척도 계보. 중복점의 0척도·빈 이웃 API 계약을 자동 보장하지 않는다. |
| NET-METHOD-STFT | [Allen·Rabiner1977](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/122_unified_approach_to_STFT.pdf), §II–IX, pp1560·1563 수식/그림 | 분석·합성 창과 표본화 조건. MKV 디코더나 불규칙 timestamp 수리 방법은 아니다. |
| NET-METHOD-SNF | [Wang 등2014 기관본](https://mghassem.mit.edu/wp-content/uploads/2015/06/nmeth.2810.pdf), Online Methods의 normalization/update/combining data types | 같은 표본 ID·정의된 이웃의 다중 뷰. 웹 PDF 텍스트는 읽었으나 raw 다운로드/식 시각 확인은 실패했다. 빈 scalar 행 예외 정책은 확인하지 못했다. 최초 B의 초록 한정은 그대로다. |
| M-IMG-OTSU | [Otsu1979 기관본](https://skynet.ecn.purdue.edu/~ace/vip/A_Threshold_Selection_Method_from_Gray-Level_Histograms_otsu.pdf), §I–IV·Eq1–19 | Histogram 목적식은 공간 차원 API의 거부 책임과 다르다. local rank의 dtype·오류 문자열 명세가 아니다. |
| M-IMG-GIL | [Gil–Kimmel2002 저자 기관본](https://www.cs.technion.ac.il/wp-content/ron-kimmel/papers/EfficientMorphology_KimmelGil_PAMI_2002.pdf), §1–3.3, §3.4 일부, §6 | 연속·사각 창, 명시적 border 제외. 전체 증명 완독이나 arbitrary footprint 적용을 주장하지 않는다. |
| M-IMG-PYE | [Pye–Bangham1996 공식 원문](https://www.eurasip.org/Proceedings/Eusipco/1996/paper/pi_12.pdf), 전체 4쪽·Eq1–24 | Flat line·부분 결과의 중립값·시간 방향. 유한 영상 경계나 온라인 지연 계약을 그대로 대체하지 못한다. |

| 외부 분야·근거 ID | 직접 읽은 원문·절 | 확인한 실패 조건과 한계 |
| --- | --- | --- |
| 음향측정·EXT-ACOUST-FARINA2000 | [Farina2000 저자본](https://angelofarina.it/Public/Papers/134-AES00.PDF), §2·§4 일부·§5–7 | 꼬리 접힘과 조화 성분 분리의 시간 조건. 초기 견고성 문장을 후속 실패 관측으로 제한했다. |
| 음향측정·EXT-ACOUST-FARINA2007 | [Farina2007 저자본](https://www.angelofarina.it/Public/Papers/226-AES122.pdf), §3.3–3.5·Figs32–33 | 실제 시계 불일치와 보정. 원시 녹음 재실행은 없고 임의 jitter/샘플 누락 해결로 일반화하지 않았다. |
| 지도표본화·EXT-MAP-OGC11 | [GeoTIFF1.1](https://docs.ogc.org/is/19-008r4/19-008r4.html), §7.2.1·7.3.2, 부록B.2.2·B.5–B.6 | 점/면적 표본과 위치 해석. Informative 부록은 규범 조항과 다르며 영상 바깥 값 정책을 정의하지 않는다. |
| 지도표본화·EXT-MAP-GDAL33 | [GDAL RFC33](https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html), 전체·Rationale/CompatibilityIssues/TestSuite | 명세 재독해로 구현을 고친 설계 기록. 과거 파일의 호환성 손해가 있으며 현재 GDAL 실행은 하지 않았다. |

## 판독자와 노출의 실제 범위

| 역할 | 실제 범위 | 독립성·재구성의 제한 |
| --- | --- | --- |
| 모집자 2개 자동 문맥 | 각각 masked 원글 batch. quota 이후 본문도 총 9개 더 노출됐으며 댓글·상태·참고문헌 목적지는 선별에서 가렸다. | 정식 선택 13행과 실제 본문 22행을 구분한다. 인간 무작위 표본 실험이나 완전한 무과다노출은 아니다. |
| 공통 취득자와 root | 초기 4개 목표 절·같은 docstring·DOM, root는 A/B 양쪽 prefix와 종합 결과를 봤다. skimage 취득자는 인접 함수 일부도 봤다. | 목표 common만 경로 packet에 넣었다. root를 가려진 경로 독자로 세지 않는다. |
| 초기 A 독자 | 6원글·공통 4절·기지안, R4/R5의 A 접두사 각 3000자. packet 59924 byte, 원래 지문 dec38a96…; `A/judgment.json`에 전체 범위가 있다. | 새 자동 문맥이며 외부 열람 0·목표 실행 0·B 노출 없음으로 기록됐다. 인간 학습 효과나 실제 채택을 측정하지 않았다. |
| 초기 B 독자 | 같은 6원글·공통 4절·기지안, R3의 B 초록/preview 3000자. packet 56191 byte, 원래 지문 3e79f554…; `B/judgment.json`에 범위가 있다. | A와 별개 자동 문맥이다. 외부 열람 0·목표 실행 0·A 노출 없음. 방법 본문을 읽었다고 하지 않는다. |
| R6 v2의 같은 A/B 독자 | 초기 문맥을 유지한 원글 2703자·새 공통 1262자·추가 0자 재판독. 최초 완료 보고는 대화에 남았지만 당시 미커밋 판단 파일은 장애로 소실됐다. | d50에 packet receipt와 공통 정정은 남았다. `workspace-recovery.json`은 재취득 원글/공통으로 만든 두 packet의 원래 SHA 일치를 기록한다. 복구 후 같은 독자의 v2 판단 파일 저장·재확인은 이 재구성 시점에 미확인이다. 기존 커밋된 초기 판단과 v2 매핑 정정만 확정 근거로 사용한다. 이전 파일의 byte 동일성이나 새 독립 반복실험을 주장하지 않는다. |
| 사후 원전 독자·root 검증 | network/audio 방법 3, imaging 방법 3+survey, 외부 4, root의 구현·뒤 예제·댓글. | 사전 판정 뒤 검증·반례다. 원경로 발견·추가 열람 성공으로 소급하지 않는다. 읽은 절·그림·실패는 각 sources/receipt에 있다. |
| 이 감사자 | 영상 원전 독자와 같은 문맥이다. 장애 전 원문·원장을 감사했고, 현재 복구된 원장·초기 판단·R6 정정·고정 segment.py LF580–670·재취득 R6 LF17–28을 다시 읽었다. | root와 별도 판단이지만 두 경로의 맹검 독자나 독립 인간 감사자가 아니다. 이 SELF_CHECK와 audit은 새 문서로 재구성했다. |

Git commit metadata에서 추가 노출 봉인 11287의 생성 시각은 2026-11-24 04:14:07 UTC, A 판독 시작은 04:14:38 UTC다. 봉인 커밋이 먼저 존재했다는 것은 확인된다. readback 기록의 04:14:54 UTC는 작성 시각이므로 A 시작 전 readback 완료 시각의 증거로 바꾸지 않는다.

## 반대 증거로 철회하거나 범위를 좁힌 주장

| 초기 해석 또는 반박 대상 | 직접 반대 근거 | 최종 처리 |
| --- | --- | --- |
| R6는 복합 roundtrip이므로 공통 API가 없다. | 원글 LF25와 첫 목표 규칙, V-R6-COLOR-API, R6-v2.json. | 초기 공석 판단을 철회했다. common 5/6으로 정정하고 초기 입력/판단은 보존한다. 공석 총수 불변을 ‘정정 없음’으로 설명하지 않는다. |
| 3점 public 입력으로 R3의 빈 행 scalar 책임을 구별할 수 있다. | 같은 고정 segment.py LF588의 width guard. t=3,width=1은 즉시 거부된다. | public 최소입력 후보를 기각했다. 고립 helper 3×3 CSR 관측은 남기고 5점 후보는 guard만 통과한 미실행 대안으로 둔다. |
| A 첫 3000자에 답이 없으므로 예제 전체에도 작동값·실패 설명이 없다. | 뒤의 local Otsu 2D/3D 입력과 Cornea opening에서 잃은 먼지 좌표·대안. | 예제 일반 무효 주장을 기각한다. 결론은 최초 접두사와 원 목표에 한정하고 뒤 절을 원경로 성과로 올리지 않는다. |
| R5 min/ignore의 maximum 문구를 중립값으로 그대로 쓸 수 있다. | R5-COMMON, V-IMPL-DILATION, V-R5-BOUNDARY의 backend 출력 7/0/255. | 문구와 구현의 불일치를 명시한다. 전체 skimage API·64bit 일반 검증은 미실시다. 중심점 없는 footprint에서 출력 감소 자체를 오류라고 하지 않는다. |

R1 center=False의 충분성은 STFT 기본값·창 시작점 산술로 제한했다. SNF의 유전체 적용을 최초 발명 분야로 읽는 해석은 Online Methods의 앞선 computer-vision 계보로 제한했다. Farina2000의 초기 견고성은 2007 시계 불일치 사례와 함께 읽는다. 어느 것도 최초 홉 신규 0을 긍정 성과로 바꾸지 않는다.

## 자연·구성, 사전·사후 자료의 대사

| 원장층 | 복구 근거에서 확인한 계수 | 합산하면 안 되는 것 |
| --- | ---: | --- |
| 자연 공개 요청 | 6 | batch에 보인 제외/미선별 16본문을 신규 요청에 합치지 않는다. |
| 초기 기지 안·구별 입력 | 13행 | 원글 제안·공통 문서·구성 예상을 홉의 신규 발견으로 세지 않는다. R3 3점 후보의 무효를 표시한다. |
| R6 v2 공통 계약 | 1 | 추가 링크의 새 선택/시험이 아니다. |
| 최초 홉의 목표 적합 신규 선택/시험 | 0 / 0 | 공석·초록 한정을 유효 비교 시행의 효과 0으로 바꾸지 않는다. |
| 사후 구성 제안 | 17행=network 6+imaging 5+external 6 | 같은 메커니즘과 재사용 입력을 17개 독립 채택으로 세지 않는다. |
| 프로젝트 제한 실행 | 창 시작점 산술 1묶음·분리 함수 4조건·SciPy 경계 3조건 | 오디오 decode/STFT 계수, public recurrence 그래프, 전체 skimage 실행과 다르다. |
| 다른 사후 산술 | network 2개·external 4입력의 7assert | 저자 실험·음향 녹음·GDAL 출력을 재현한 것이 아니다. |

장애 전 통합 verification-tests 21행 및 transfer 16주제군을 구성했다는 보고가 있었다. 복구 후 최종 통합 파일과 census를 다시 계산하기 전에는 그 수를 현재 파일의 검산 결과로 주장하지 않는다. 사후 제안 수·통합 검증 행수·같은 선택을 합친 주제군 수·실제 실행 수는 각각 다른 집계다.

## 재현·검사와 남은 게이트

원문 지문은 동일성 검사값이며 원문 자체가 아니다. 보존된 표·DOM·판단·receipt로 선택과 집계를 재계산할 수 있어도 ignored cache의 원문/packet을 지문만으로 역복원할 수는 없다. 이번 장애에서 R6는 원글과 공통을 재취득해 지문이 일치했으므로 원래 packet을 재구성할 수 있었다. 다른 원자료도 모두 같은 방식으로 복구됐다고 일반화하지 않는다. 가변 페이지가 바뀌면 같은 snapshot 또는 고정 소스와 같은 빌드가 필요하다. SNF는 성공한 웹 PDF 텍스트와 실패한 raw PDF 취득을 분리한다.

최종 결과 SHA와 대표 원문 재열람·필수 세 표 재구성·manifest·공통 검사는 이 재구성 시점에 **예정**이다. 실행자는 명령·입력 SHA·출력·종료 코드·미실시 범위를 `evidence/acceptance-evidence.json`에 기록해야 한다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-113/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-113/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

위 명령을 기재한 것이 실행 또는 통과를 뜻하지 않는다. 작업별 검산기의 파일명·인자는 최종 재현 절차와 실제 실행 명령에 맞춰 확인한다. 최소 게이트는 6요청/12자리 대사, R6 초기/정정판 분리, R2 적격성 경계 표시, R3 무효 후보 철회, 자료 24개의 계보 중복 제거, 모든 주장과 근거/미확인 연결, 사후 외부 자료가 최초 발견에 섞이지 않았는지 검사하는 것이다. 전체 라이브러리 설치·원 MKV/tokenizer·원 Csync·s390x 환경·원 논문 데이터셋은 미실시다. 최종 검사 성공도 실제 수리·채택 성공을 의미하지 않는다.


복구 마감 확인: R6-v2 A/B의 동일 독자가 각자 복구 packet만 다시 읽은 R6-v2-judgment.json을 최종 결과 묶음에 포함했다. 두 지문은 기존 receipt와 일치하며 신규 extra/선택/시험/실행/외부열람 모두0이다. 이는 새 독자 효과가 아니라 동일 독자의 재판독이다. 위 재구성 시점의 미확인 표시는 이 확인으로 보완한다.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 양쪽 추가 본문 비교쌍 0/6이며 공석 9와 초록 1 때문에 경로 우열을 측정하지 못했다. | 고정 시작절·12자리 원장과 새로 사전 고정할 동일 요청의 두 적격 원문. | 같은 보존 조건 아래 두 본문이 다른 선택·구별 입력을 직접 지지하면 새 판의 비교가 가능하다. |
| R2 보존 조건은 경계 사례이고 R6 초기 공석과 R3 3점 public 후보는 정정이 필요했다. | #1648 solution1·2, #6670 LF19–27, 고정 segment.py LF580–670, R6 정정·재판독 기록. | 독립 보존 조건 판정 또는 실제 유효 public 입력의 출력이 현재 판단과 다르면 모집·대응·시험의 새 판을 기록한다. |
| 미커밋 문서 소실과 가변 원문 재취득 한계가 있으며 MKV·Csync·s390x는 실행하지 못했다. | workspace-recovery.json, 최종 결과 SHA의 evidence/source-census.json·재현 절차·검사 영수증, 동일 지문 원문과 원 입력 환경. | 원판 재취득/실제 실행이 구성 예상과 다르거나 날짜가 맞는 수리·채택 증거가 나오면 해당 반환·미확인을 정정한다. |
