## AF-RES-113 결과와 수용 범위

**상태는 PARTIAL이다.** 고유 자료 배당 24개와 원장·표의 대사는 충족했다. 그러나 예정된 6요청×2경로 중 적격 추가 링크는 3개, 실제 본문 접두사 도달은 2개, 초록/구독 미리보기 도달은 1개였다. 공석9개가 남았고 양쪽 추가 본문을 모두 읽은 요청은0/6이다. 따라서 A와 B 중 어느 경로가 더 낫다는 효과율은 정의할 수 없다. 추가 노출이 원 요청의 변경·보존 조건을 함께 지지한 새 구현 선택과 새 판별 시험은 각각0개였다. 공석을 ‘효과 없음’으로 바꾸어 세지 않았다. [hops.jsonl; decisions.csv; evidence/source-census.json]

이 연구가 제공하는 설계 입력은 **이미 구현을 찾은 요청에서, 어떤 추가 주소를 실제로 보여 줄 수 있고 그 제한된 본문이 어떤 결정까지 지지하는지**에 관한 사례집이다. 첫 예제나 첫 참고문헌을 항상 덧붙이라는 정책은 이 표본에서 지지되지 않았다. 공통 문서에 이미 있는 예제·선택을 추가 성과로 세면 결론이 달라지고, 원전의 응용 분야를 원리의 발명 분야로 읽으면 전이 계보도 달라진다. 이 두 혼동을 피한 제한된 결과로 사용해야 한다.

계획 기준은 `670ecde1dab07aede6760618a7d907f0cdff185a`, 실제 시작 통합 SHA는 `581b863dfb9f90106c2a07fb749d0cada51b0a25`다. 필요한 정책·브리프 본문은 같고, 그 사이 자기 작업 행의 실행 상태가 바뀌었다. 계약은 manifest.json에 고정했다. AF-RES-109의 인계 `e547d88834ff8adfcea9039e32c48b5be97e1eb3`와 결과 `c212aab782008f263cbee14f6304c029dc82ce3a`의 세 원장을 직접 대조했다. 109의36자리/33링크/조건부12선택/제안27시험 및 사후 외부4자료를 이번 발견 수에 더하지 않았다. 다른 동시 작업의 결과에는 의존하지 않았다. [evidence/start/assignment.json; read-receipt.json; dependency-audit.md]

## Q1. 설계자가 이미 알고 있던 것과 모집의 한계

두 저장소의 2023-01-01–2024-12-31 UTC 생성 공개 이슈에서 PR을 제외하고 `(created_at, number)` 순으로 첫60개씩 고정했다. 검색 결과 전체164개와340개 중 각각100개를 받아60/61 경계를 확인했으며 동시각 경계는 없었다. 첫60의 마지막 날짜가 librosa는2023-08-04, scikit-image는2023-04-08이므로 이 표본이2024년까지 고르게 대표한다고 주장하지 않는다. [frame.csv; evidence/recruitment/*/acquisition.json]

정식 순서 판정은 librosa8행과 scikit-image5행이다. 선정은 각각순번2/5/8과2/3/5, 제외는7행, quota 이후 미선별은107행이다. 다만 batch 출력으로 실제 본문은10+12=22개가 모집자에게 노출됐다. 이 과다 노출과 root가 인접 이슈/함수 일부를 본 사실을 숨기지 않았다. 후속댓글·상태·수락·참고문헌 목적지를 모집 근거로 쓰지 않았고, 별도의 A/B 독자에게는 정해진 공통 입력만 전달했다. [recruitment-review.json; SCOPE.md; imaging/audit.md]

여섯 원글은 현재 공개 body의 해시가 있는 스냅샷이다. 생성시각과 현재 body가 최초 작성판임은 다른 사실이며, updated_at도 본문 수정시각의 증거는 아니다. 원 작성자가2023년에 현재2026 문서 내용을 알고 있었다는 주장을 하지 않는다. 판정 시점은 고정 문서판을 이번에 읽은 시점이다.

선정 요청에는 이미 상당한 해법이 있었다. R2의 nancumsum, R3의 scalar nanmedian/국소 오류 구분, R4의2D/3D/else 분기, R5의 dtype-min 또는 mode 노출은 원 작성자가 제안한 안이다. 이들을 추가 링크가 새로 만든 선택으로 세지 않았다. R2는 기존 mir_eval 합성이 거의 적합하다는 문장을 보존 조건으로 읽은 경계 사례다. NaN 경계 scoop 제거는 변경 요구이므로 보존 조건으로 다시 세면 안 된다. 엄격한 독립 보존 조건이 필요하다는 다른 판독은 이 선정에 이의를 제기할 수 있다. 원 봉인을 유지하고 사후에 편리한 다음 이슈로 교체하지 않았다. [REQ-R1…R6; baselines.csv; SELF_CHECK.md Q1]

## Q2. 공통 시작점과 정정된 대응

계획일 전 안정 release와 태그를 직접 확인해 librosa1.0.1(`9caf46a4ecaeb8ea24bb541231065c9f761174ae`), scikit-image0.26.0(`ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8`)를 택했다. 원 작성자의 링크와 연구자가 공식 API 목차에서 찾은 링크를 구분했다. R1·R3·R4·R5의 전체 function절은 각각5172·6857·1384·3407자였고, signature부터 inline example까지 같은 공통 입력으로 주었다. 배포 HTML의 gallery href를 원 source docstring만으로 추정하지 않았다. [evidence/start/*-releases.json; *-tag.json; evidence/common/]

R2에는 원 작성자의 [mir_eval.sonify.pitch_contour](https://craffel.github.io/mir_eval/#mir_eval.sonify.pitch_contour)가 있다. 공석 이유는 구현을 못 찾았기 때문이 아니라, 지정한 librosa API 목차로 대응할 새 public 심벌이 원글에 없기 때문이다. upstream 출력 예시인 pyin으로 바꾸지 않았다.

R6의 초기 보류는 감사에서 정정했다. 복합 왕복식이라는 이유만으로 공통 API를 비워 두었으나, 규칙의 문자순 첫 목표는 `lch2lab(lab2lch(lab))`의 lch2lab이다. 고정 API에서 [lch2lab 전체1262자](https://scikit-image.org/docs/0.26.x/api/skimage.color.html#skimage.color.lch2lab)를 찾아 별도v2 공통으로 봉인하고, 같은 A/B 독자가 자기 경로 입력만 다시 읽었다. 이는 새 인간 독자 실험이 아니다. source·anchor·See also·EasyRGB bare math URL·Wikipedia 두 주소를 전수 기록했다. EasyRGB 목적지는 열지 않았으며, 시작절에서 원방법 제안자/원표준으로 귀속하지 않았다는 이유로 B에 넣지 않았다. 사이트 자체가 원저작이 아니라고 단정한 것은 아니다. [evidence/corrections/R6-v2.json; evidence/arms/*/R6-v2-judgment.json]

그 결과 공통 시작은4/6→5/6으로 바뀌었다. 초기 공석 원인은 시작4자리+링크5자리였고, 정정 뒤에는 시작2자리+적격 링크7자리다. 총공석9가 같다는 이유로 정정이 없었다고 설명하지 않는다. 초기 공통/판정은96a754e8/0b6287e5에 그대로 남아 있다.

## Q3. 실제 한 번의 추가 열람

A4는 [Rank filters](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_rank_filters.html), A5는 [Cornea inpainting](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_cornea_spot_inpainting.html), B3는 [Wang 논문의 DOI](https://doi.org/10.1038/nmeth.2810)가 실제 문서 순서로 선택됐다. R3의 더 앞선 Zelnik-Manor 서지는 외부 href가 없었으므로 검색으로 복구하지 않았다. R4의 Wikipedia는 원저작 링크에서 제외했다. 메뉴·바닥글·source·See also·inline example을 독립 추가 예제로 세지 않았다. [hops.jsonl; common DOM 원장]

세 시행 모두 추가 explicit open1회, 보이는 main/article의 첫3000 Unicode codepoints, 그림0개였다. Nature는 DOI 뒤 자동 이동을 거쳐 초록·구독 preview에 도달했다. 그림 제목은 그림을 읽은 것으로 세지 않았다. 원문 방법이 보이지 않았으므로 이 시행은 방법 본문 접근 실패다. 나중에 기관 PDF의 Online Methods를 읽은 것은 사후 보조 탐색이며 원 시행을 성공으로 바꾸지 않았다.

HTML 추출기에서는 R5의 긴 Plotly script로 초기 본문이2261자로 잘렸고, R3에는 인코딩 문제가 있었다. 같은 수신 byte에 UTF-8/huge_tree/deep-copy 보정을 적용했으며 추가 HTTP 열람이나 내용 위치 선택을 하지 않았다. 두 새 독자는 보정된3000자만 받았다. 공통 네 본문 지문은 보정 전후 같았다. 원 추출·새 추출 해시와 이유를 함께 보존했다. [evidence/hops/extraction-correction.json]

고정 시행의 응답 byte와 elapsed 합은 census에 따로 기록한다. 읽은 본문9000자와 네트워크로 받은 전체 HTML 크기는 다르다. 세 요청은 병렬이었으므로 elapsed의 합을 사용자 대기시간으로 해석하지 않는다. token·금전 비용은 관측하지 못했으며0으로 쓰지 않았다.

## Q4. 무엇이 새 선택을 갈랐고 무엇은 기존 안이었나

두 초기 독자는 서로 다른 새 자동 문맥이었다. 같은 원글·공통절·기지안과 자기 경로의 추가 본문만 읽었고 외부 열람·목표 실행은0이었다. root는 양쪽을 종합해 보았으므로 독립 독자로 세지 않는다. 판정 파일에는 실제 읽은 파일/byte 범위/해시가 있다. 원전 대조 전0b6287e5에서 결론과 시험 목록을 고정했다. [evidence/arms/; PREJUDGMENT.md]

A4의 초반은 camera에 salt/pepper noise를 넣고 여러 반경의 median을 보는 내용이다. A5의 초반은60×1440×1440 uint16 OCT sequence에서 정지한 먼지와 움직이는 조직을 구분하려는 시간 median/variance다. 각각 다른 구현 문제에는 유용할 수 있으나, R4의 차원 오류 책임이나 R5의 영상 외곽 기여를 새로 결정하지 않는다. B3 초록은 자료형별 graph를 합친다는 순서를 보여 주지만 R3의 scalar/국소 bandwidth 예외를 바꾸는 규칙이 없다. 따라서 목표에 맞는 추가 신규성은0이다. [R4-A; R5-A; R3-B 판독행]

사후 프로젝트 대조에서는 다음과 같이 기존 판단을 검증하거나 제한했다.

| 대상 | 원전/고정 소스의 실제 확인 | 구성 입력·실행 또는 미실시 | 최종 한계 |
| --- | --- | --- | --- |
| R1 | [STFT1.0.1](https://librosa.org/doc/1.0.1/api/generated/librosa.stft.html)은 n_fft2048, hop512 기본값. 공통 stream 예제는 F4096/H1024를 쓰면서 분석 호출에 두 값을 생략한다. | 완전 stream블록265216 samples에서 기본 분석515프레임 대 맞춘 분석256프레임, 인접블록 중복시작3 대0을 정수 산술로 확인. | center=False만으로 같은 분석 격자가 되지 않는다. 실제 MKV decode/STFT 계수는 실행하지 않았다. |
| R3 | [고정 segment.py](https://github.com/librosa/librosa/blob/9caf46a4ecaeb8ea24bb541231065c9f761174ae/librosa/segment.py)의 scalar는 빈 일부 행을 허용하고 전체 빈 graph는 거부한다. | 3×3 CSR의 고립 helper 실행에서 scalar0.1, mean_k/gmean_k 오류, 전체 영 graph 오류를 관측. | 봉인했던3점 **public** 후보는 width guard를 통과하지 못해 기각했다. helper의3×3 CSR과 public 생성은 다른 시험이다. 후속5점 후보는 EXECUTION_PLAN에 있다. |
| R4 | [고정 rank 구현](https://github.com/scikit-image/scikit-image/blob/ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8/src/skimage/filters/rank/generic.py)은2D/3D dispatch 후 다른 차원을 명시적으로 거부한다. | 원글의1D 재현과 정상2D/3D 비교는 후속 명령으로 남김. | 원 작성자의 제안과 현재 코드가 맞아도 이번 링크의 채택 증거가 아니다. |
| R5 | [고정 gray.py](https://github.com/scikit-image/scikit-image/blob/ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8/src/skimage/morphology/gray.py)는 ignore→min, 정수 최솟값/float−∞를 쓴다. 문서는 maximum이라고 적는다. | uint8[[7]], footprint[[1,0,1]]에서 설치된 SciPy backend는 reflect7, constant0은0, literal255는255. | complete skimage 실행은 아니다. 중심점이 없는 footprint에는 항상 원값 이상이라는 성질도 보장되지 않는다. |
| R6 | v2 공통절은 shape/channel/hue 계약을 준다. 원 회귀의 dtype assertion은 rgb2lab 뒤 lab.dtype에 있다. | colorwheel·dtype별 decimal4/7 원 시험은 미실행. 수정 수치 출력이나 원인 함수는 제시하지 않는다. | shape 검사를 통과해도 수치 회귀는 실패할 수 있다. 원문에 없는 lab2.dtype assertion을 추가해 원시험으로 부르지 않는다. |

실제 실행 영수증은 project/executed-checks.json, network/arithmetic-result.json, external/arithmetic-checks.json이다. 이들은 원 논문 실험이나 전체 라이브러리 실행의 대체가 아니다. 동일 선택의 표현 차이는 transfer.csv의16주제군으로 합쳤다. 사후 제안17행과 프로젝트4검증군의 합21행은 verification-tests.csv에 남겨 원자료·예상·실행 범위를 추적할 수 있다. 원 추가 링크의 새 시험0에 이 수를 더하지 않았다.

## Q5. 원 분야, 계보, 옮길 수 있는 전제

고유 배당은 요청6, 프로젝트8, 방법 원전6, 외부4다. 프로젝트8은 서로 다른 기능 문서5개(stream, recurrence_matrix, rank.otsu, dilation, stft)와 독립 예제3개(Rank filters, Cornea, Morphological Filtering)다. 같은 함수 HTML·docstring·구현을 별도 저작으로 늘리지 않았다. R6 정정 문서, 다른 회귀 입력, survey, 미러·재열람·metadata는 추가 기록으로 남겼지만 배당24에 더하지 않았다. ‘본문까지 읽음’은 기록한 관련 절을 읽었다는 뜻이며 모든 저작의 전 페이지를 완독했다는 뜻은 아니다. [sources.jsonl의 unique_counted/read_status/section_read]

| 방법 제안자의 원저작 | 직접 읽은 방법과 대상 | 옮길 수 없는 주장 |
| --- | --- | --- |
| [Zelnik-Manor·Perona2004](https://proceedings.neurips.cc/paper_files/paper/2004/file/40173ea48d9567f1f393b20c855bb40b-Paper.pdf) | 지역척도, Fig2/식1–2와8쪽 본문·부록. K번째 이웃 거리로 척도를 정함. | 이웃 부재나 중복점의0척도를 자동 해결하지 않는다. [NET-METHOD-SELF] |
| [Wang 등2014 SNF](https://mghassem.mit.edu/wp-content/uploads/2015/06/nmeth.2810.pdf) | Online Methods의 자기포함 이웃·정규화·결측 측정 대치·다중view 확산. | 시간 제외 뒤 고립 graph 행의 scalar 예외와 결측 측정은 다르다. 원 PDF 수식 조판은 시각 확인 실패. [NET-METHOD-SNF] |
| [Allen·Rabiner1977](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/122_unified_approach_to_STFT.pdf) | STFT 분석/합성, OLA와 창·표본화 조건.7쪽과 핵심 식/그림. | 변환 길이, 프레임 시작, 합성 가중치가 다르다. tokenizer가 역변환을 요구한다고 가정하지 않는다. [NET-METHOD-STFT] |
| [Otsu1979](https://skynet.ecn.purdue.edu/~ace/vip/A_Threshold_Selection_Method_from_Gray-Level_Histograms_otsu.pdf) | Histogram 두 클래스의 분리 목적식, §I–IV·Eq1–19. | Histogram 정의로 ndarray의1D 금지 또는 허용을 결정할 수 없다. [M-IMG-OTSU] |
| [Gil·Kimmel2002](https://www.cs.technion.ac.il/wp-content/ron-kimmel/papers/EfficientMorphology_KimmelGil_PAMI_2002.pdf) | 연속 창의 효율 알고리즘, 사각/hyperbox 확장. p1607은 border를 제외. | 비연속 footprint 또는 실제 영상 외곽 정책의 보증이 아니다. [M-IMG-GIL] |
| [Pye·Bangham1996](https://www.eurasip.org/Proceedings/Eusipco/1996/paper/pi_12.pdf) | Flat line 최대 연산과 부분 결과 결합,4쪽·Eq1–24. | 부분 신호 밖−∞와 대상 영상 API 경계는 다른 계약이다. centered 변환에는 시간 가용성 조건도 필요하다. [M-IMG-PYE] |

SNF는 유전체 응용을 다루지만 원문은 컴퓨터 비전·영상처리의 다중view 학습을 계보로 명시한다. 이 사례를 ‘유전체에서 발명한 원리를 음향으로 옮겼다’고 분류하면 안 된다. 앞선2012 논문 자체의 우선권은 이번에 검증하지 않았다. 같은 분야의 다른 구현은 대상과 보존량이 같은지, 다른 분야의 같은 원리는 관계를 보존하면서 입력 전제를 옮길 수 있는지, 배경 인용은 실제 방법 귀속이 있는지로 구분했다. 이름만 같은 경우나 대응관계가 없는 경우는 우연한 유사성으로 기각했다. [NET-METHOD-SNF Online Methods; transfer.csv]

외부 네 저작은 발견 봉인 뒤에만 열었다. 음향 두 저작은 같은 저자의 서로 다른 원자료이고, 지도 두 저작은 표준과 구현 설계의 직접 계보다. 독립 네 집단의 재현 실험이라고 부르지 않는다.

| 외부 분야·원자료 | 실제 관측과 이동 전제 | 기각 또는 제한한 전이 |
| --- | --- | --- |
| 음향 측정 [Farina2000](https://angelofarina.it/Public/Papers/134-AES00.PDF) | sweep 역합성의 순환 꼬리·조화 성분 분리 시간 조건. | 블록 support 검산에는 도움되지만 MKV decoder 선택을 주지 않는다. [EXT-T1/T6] |
| 음향 측정 [Farina2007](https://www.angelofarina.it/Public/Papers/226-AES122.pdf) | §3.4의 별도 재생/녹음 clock, 약8.5ms skew와 보정의 실측 사례. | 일정 비율의 clock 보정이 샘플 유실·불규칙 timestamp를 복원하는 것은 아니다. [EXT-T2] |
| 지도 표본화 [GeoTIFF1.1](https://docs.ogc.org/is/19-008r4/19-008r4.html) | point/cell 및 raster→model 위치 관계. 규범 조항과 informative 부록을 구별. | 좌표 기준점과 외부 경계 값은 다른 책임이다. 불규칙 격자에 고정 반칸 보정을 일반화하지 않는다. [EXT-T3] |
| 지도 표본화 [GDAL RFC33](https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html) | 명세 재독 후 half-pixel 해석을 고친 실제 설계 기록과 이전 생성 파일의 호환성 문제. | 표준대로 고친 값이 사용자가 보존하려던 과거 출력과 같다는 보장은 없다. [EXT-T4] |

예를 들어 작업자가 구성한 PixelIsPoint tiepoint(100,200), signed spacing(10,−10)은 GDAL corner(95,205)를 뜻한다. tiepoint를 corner로 오인하면 첫 center가(105,195)가 된다. 이는 산술 확인이며 실제 GDAL 실행 결과가 아니다. 마찬가지로 불규칙 시간의 위상, 순환 꼬리 접힘, sparse footprint의2 대100, 미래표본 사용의0 대9/10은 원전의 실험처럼 쓰지 않았다. [verification-tests.csv; 각 source_observations/predicted_outputs]

## Q6. 가장 강한 반대 사례

**현장 사용자 관점:** 정확한 원전을 추가해도 기존 출력 보존을 해칠 수 있다. RFC33은 원 명세에 맞추는 수정이 과거 GDAL 생성 파일의 위치 의미를 바꾼다는 문제를 직접 적는다. R5 원 글의 유지보수자도 기본값 전면 변경보다 mode 노출을 선호했다. 따라서 결과에는 ‘무엇을 고치는가’와 ‘무엇을 유지하는가’를 같이 돌려줘야 한다. [EXT-MAP-GDAL33; COMMENT-1382729471]

**도구 구현자 관점:** 예제의 설정값과 기본값, source의 사전조건이 실제 선택을 막을 수 있다. R1 stream 예제와 STFT 기본값의 격자 차이, R3의 잘못된3점 public 후보, R5의 maximum 문구와 min 구현이 그 사례다. 논문 링크만 추가하면 이 오류를 해결했다는 인상을 줄 위험이 있다. 이미 시작 절에 있는2D/3D 예제를 다시 추가 클릭의 성과로 세는 것도 중복이다. [V-STFT; V-R3-PUBLIC-GUARD; V-IMPL-DILATION]

**원 분야 저자 관점:** 자신의 정리·알고리즘이 어느 입력에서 성립하는지에 대한 제한이 먼저다. Gil–Kimmel의 border 제외, Pye–Bangham의 연속 line support, Otsu의 histogram과 API 차원 구분, Farina 후속 저작의 clock 실패는 그 한계를 보여 준다. 원 분야명이나 같은 연산 이름만으로 전이를 인정하지 않았다.

반대로 **예제가 이미 예외와 실제 작동값을 준다는 반례도 찾았다.** Rank filters의 뒤 절에는2D/3D local Otsu 입력이 있고, Cornea 뒤 절에는 opening 단계에서 (719,1237) 부근 먼지 점을 잃었다는 실패와 footprint 대안이 있다. 그러므로 ‘예제 전체에는 예외가 없다’는 결론은 기각했다. 다만 그 절은 처음3000자 밖이고 원 목표인1D 오류/경계 정책을 새로 해결하지 않으므로 원 판정0은 유지한다. [V-LATE-HOP-R4-A; V-LATE-HOP-R5-A]

이번에는 A/B가 같은 저작·그림을 반복하는 **성공 쌍 자체가 없었다.** 따라서 중복 그림으로 인한 실제 효과 감소를 측정했다고 말하지 않는다. 구조상 inline example의 공통 노출, 같은 논문의 초록/기관본, HTML/docstring 재열람이 중복임은 확인했으며 한 저작으로만 산입했다. 찾지 못한 반례는 ‘없다’가 아니라 검사한 이 범위에서 미확인이다.

## Q7. 제품이 반환할 조건

이 표본의 실제 권고는 시작 링크만3건(R1/R3/R4), 보류3건(R2/R5/R6)이다. R5/R6의 검토 주소를 표에 남겼다고 해결 링크로 확정한 것은 아니다. 출전·예제 링크가 있다는 사실, 새 결정을 얻었다는 사실, 사용자가 채택했다는 사실을 각각 다른 필드로 반환해야 한다. 이 정책 제안은 제품 실험으로 검증된 효과가 아니라 사례에서 도출한 설계 가설이다. [returns.csv]

| 반환 유형 | 적용 조건 | 이번 관측 |
| --- | --- | --- |
| 시작 링크만 | 공통절에 목표와 보존조건을 판정할 정보가 있고 추가 첫 링크가 새로운 목표 선택을 지지하지 않음. 미해결 부분은 명시. | R1/R3/R4. 수리 성공 보장은 아님. |
| 예제 추가 | 실제 노출된 예제의 허용 본문에 원 입력을 보존하는 값·예외·구별시험이 추가됨. | 적격 신규 사례 없음. 뒤 절의 가치는 별도 예산/새 판에서 확인할 대상. |
| 출전 추가 | 원저작 귀속과 접근이 확인되고 방법 전제가 원 입력에 맞으며 새 단위·순서·책임을 지지함. | R3-B는 초록 한정으로 보류. 사후 본문도 scalar 예외 계약을 직접 주지 않음. |
| 둘 다 | 같은 요청에서 두 추가 본문이 서로 다른 선택을 지지하고 같은 저작/그림의 중복이 아님. | 비교 가능한 쌍0이므로 관측 없음. |
| 보류 | 심벌 대응, 입력 보존, 출전 귀속, 본문 접근 또는 문서/구현 일치가 충분하지 않음. | R2/R5/R6. 최소 다음 입력은 EXECUTION_PLAN.md와 SELF_CHECK에 있음. |

자연 후속 댓글은 발견 봉인 뒤 별도로 읽었다. R2의 같은 원 작성자는2024-04-03 mir_eval PR을 냈다고 말하지만 실제 diff를 확인하지 않았고2026 연구 링크를 본 후의 채택도 아니다. R4의 기여 의향, R5의 mode 선호, 현재 구현의 존재도 이번 반환의 인과 증거로 바꾸지 않았다. 실제 후속 채택은6건 모두 미확인이다. [followup_context source행]

## 검산, 재현, 남은 실행

첫 세 표는 baselines.csv·hops.jsonl·decisions.csv·returns.csv에서 재생성한다. `python -B docs/workstreams/research/AF-RES-113/recalculate.py --check`는120프레임·6요청·12자리·24고유 배당·외부2+2·표의 일치·postseal 전이의 발견 credit0을 대사한다. 전체 출처 주소 수, 선언한 work/event ID 수, 출처 읽기 attempt ID 수, 예정 시행 수와 실제 추가 열람 수는 evidence/source-census.json에서 서로 구분한다. 그 work/event ID 전체 수에는 내부 지침과 navigation 기록도 들어가므로24개 연구 배당이나 독립 실험 수로 바꾸어 읽지 않는다.

SELF_CHECK는 Q1–Q7의 근거·반증·분모·판단 변경 관측을 채웠다. 이 결과를 먼저 원격 SHA로 고정한 뒤 그 SHA에서 원격 파일과 대표 원문을 재열람하고 manifest check, 공통 cloud_check, 작업별 검산을 실행한다. 실제 실행 여부·입력 SHA·명령·exit·미실시 범위는 별도 acceptance-evidence.json 및 마지막 HANDOFF에 기록한다. 이 결과 본문에 명령이 있다는 사실은 검사 통과 증거가 아니다.

원격 지문/DOM/원장으로 결과 집계를 재구성할 수 있다. 그러나 원문 전체와 reader packet은 임시 cache여서 지문만으로 원판을 복원할 수 없다. 가변 배포 URL의 본문이 바뀌면 동일 snapshot 또는 고정 source와 동일 문서 build가 필요하다. 실행하지 못한 complete 라이브러리, 원 MKV/tokenizer, original Csync, s390x/NumPy1.24.1, 논문 원시 실험, GDAL 파일의 구체 명령과 필요한 입력은 EXECUTION_PLAN.md에 남겼다.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 양쪽 추가 본문을 읽은 쌍0/6, 공석9와초록1 때문에 A/B 우열을 판정할 수 없다. | 같은 고정 시작절의12자리와 새로 사전 고정할 두 적격 원문 경로. | 같은 보존조건에서 두 본문이 서로 다른 선택과 구별 입력을 직접 지지하면 새 판의 비교가 가능하다. |
| R2 보존조건은 선별 경계사례이고 R6 초기공석·R3의3점public후보는 정정됐다. | #1648 원글, R6-v2 기록, 고정 segment.py의width guard와5점후보. | 독립 보존조건 코딩 또는 실제유효입력 관측이 다르면 모집·대응·시험 판정을 새 판에서 바꾼다. |
| 문서/구현 불일치와 원판 복구·실환경 실행 결손이 남았다. | R5 고정 gray.py, 같은지문의 원문snapshot, EXECUTION_PLAN과원MKV·Csync·s390x환경. | 실제 입력의 결과가 예상과 다르거나 날짜가 맞는 동일사용자의 실제변경이 확인되면 반환·미확인을 정정한다. |
