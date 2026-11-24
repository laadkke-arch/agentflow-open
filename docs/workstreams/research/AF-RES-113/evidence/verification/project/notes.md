# 원 프로젝트의 사후 대조와 반대 증거

사전 판정 `0b6287e5359257004900ef4b8e30f7abb7306024` 이후에만 구현 본문, 추가 기능, 예제의 뒤 절, 댓글을 읽었다. 이 파일의 발견은 원래 12자리의 성과가 아니다. source_id는 이 폴더의 sources.jsonl 및 최종 통합 원장과 연결된다.

## R1: 디코더, 프레임 크기, 시작점은 서로 다른 문제다

원 글의 MKV 오류는 블록 경계 문제라고 판단할 근거가 없었다. 2023-01-07 유지보수자 댓글은 `load`의 audioread 경로와 `stream`의 libsndfile 경로가 다르다고 명시한다. 현재 1.0.1 소스도 파일을 `sf.SoundFile`로 연다. 따라서 STFT의 패딩이나 표본율을 조절하는 것만으로 원 MKV가 열릴 것이라고 반환하면 잘못이다. 원 파일의 codec/container, 원 환경과 tokenizer 입력 계약은 여전히 없다. [COMMENT-1374574546; V-IMPL-STREAM]

한편 공통 시작 절에는 이미 `center=False` 예제가 있었다. 이것은 A의 추가 정보가 아니다. 예제는 stream에 frame_length=4096, hop_length=1024, block_length=256을 주지만 분석 호출에서는 n_fft와 hop_length를 생략한다. 독립 기능 문서와 고정 소스에서 STFT의 기본값 n_fft=2048, win_length=n_fft, hop_length=win_length//4를 확인했다. [LIB-COMMON-STREAM; V-STFT; V-STFT-SOURCE]

충분히 긴 신호의 완전한 블록 하나는 265216 samples이고 다음 블록 시작은 262144 samples 뒤다. 위 기본 STFT라면 한 블록에 515개 프레임 시작점이 생기고, 인접 완전 블록 사이에 세 시작점이 중복된다. n_fft=4096, hop_length=1024를 함께 명시하면 256개이며 그 중복은 없다. `verify_examples.py`는 이 정수 산술을 실행했다. 실제 파일 decode·STFT 계수 비교를 실행한 것은 아니다. 이 반례는 “center=False만 있으면 전체 신호 처리와 같다”는 과도한 결론을 제한한다. 창 폭/advance/분석 hop을 함께 보존해야 한다. 마지막 짧은 블록과 resampling 상태는 별도 검증 대상이다. [V-R1-FRAMES; executed-checks.json]

현재 1.0.1에는 soxr streaming resampling과 finally에서 소유한 SoundFile을 닫는 구현이 있다. 과거판에 대한 “stream은 resampling이 없다”는 설명을 현재판에 적용하지 않았다. 원 글의 2023 환경이 1.0.1이었다고 주장하지도 않는다. [V-IMPL-STREAM]

## R3: 원 제안이 현재 구현에 있고, 전체 공백은 별도로 거부한다

고정 segment.py의 `__affinity_bandwidth`는 빈 행에 대해 med_k_scalar일 때만 NaN을 넣고 다른 국소 추정은 오류를 낸다. 이어 모든 kth distance가 비유한이면 빈 그래프 오류를 낸 뒤, 그렇지 않을 때만 nanmedian을 반환한다. 이 구분은 원 요청이 이미 제안한 책임 분리와 맞는다. 추가 B 초록에서 알아낸 답이 아니다. [V-IMPL-AFFINITY_BANDWIDTH; REQ-R3]

완전한 librosa 설치 대신 고정 소스에서 해당 함수 정의만 분리해 실행했다. CSR 입력 `[[0,.1,0],[.1,0,0],[0,0,0]]`과 k=1에서 med_k_scalar는 0.1, mean_k와 gmean_k는 마지막 행에 이웃이 없다는 오류였다. 3×3 영 그래프에서는 scalar도 빈 그래프 오류였다. 예외 클래스만 local stand-in으로 제공했다. public recurrence_matrix가 봉인된 후보 data=[[0,.1,100]]에서 정말 이 CSR을 생성하는지는 실행하지 않았다. 따라서 원 제안의 조건부 예상과 이 고립 함수의 관측을 구별한다. [V-R3-PARTIAL; V-R3-EMPTY; executed-checks.json]

선택해서 읽은 test_segment.py의 기존 입력은 normal/random 행렬과 bandwidth 값/배열이다. 이 짧은 읽기 범위에서 원 이슈의 실데이터 Csync는 확보하지 못했다. 테스트 파일 전체에 빈 그래프 검사가 없다는 주장도 하지 않는다. [V-SEGMENT-TESTS]

## R4: 알고리즘의 정의와 API 오류 책임은 다르다

현재 rank.otsu 소스는 2D와 3D를 각각 전용 helper에 보내고 나머지 차원은 정확한 차원 메시지로 거부한다. 원 작성자가 이미 제안한 분기다. 공통 API의 2D/3D 예시만으로도 보존해야 할 정상 사용 범위가 주어졌다. [V-IMPL-OTSU; R4-COMMON; REQ-R4]

A4의 첫 3000자는 median/noise 예제였다. 사후에 같은 페이지의 11300–13200번째 문자 범위를 읽으니 page()+disk(10), brain()+ball(5)의 local Otsu 예제와 global scalar threshold 비교가 있다. 따라서 “갤러리에 Otsu 작동값이 없다”는 일반화는 틀리다. 그러나 그 내용은 원 예산 밖이며, 1D 오류 분기를 고치는 새 선택도 아니다. 본 연구의 부정 판정은 **선택된 초반 노출과 요청 목표**에 한정한다. 그림 픽셀은 읽지 않았다. [V-LATE-HOP-R4-A]

2023 댓글은 유지보수자의 동의와 다른 기여자의 PR 작성 의향을 보여 준다. 이것만으로 원 사용자가 연구의 예제/원전을 보고 채택했다고 말할 수 없다. 해당 PR의 변경 내역은 이 대조에서 열지 않았다. [COMMENT-1369883296; COMMENT-1380995824; COMMENT-1381600030]

## R5: 중립값 문구 오류와 예제 자체의 실패를 모두 남긴다

고정 배포 API와 같은 판 source docstring은 min/ignore 경계 설명에 maximum이라는 단어를 사용한다. 반면 실제 함수는 ignore→min으로 바꾸고, helper는 정수 dtype의 최솟값/float의 −∞/bool의 False를 constant 값으로 준다. max reduction에서 중립값이라는 설명과 구현을 함께 보면 문서 문구가 반대다. 소스에는 SciPy의 footprint 반전을 보정하는 반전도 따로 있다. 경계 값 선택과 footprint 방향은 별개의 축이다. [R5-COMMON; V-IMPL-DILATION]

원 문서의 애매함을 실제 숫자로 구별하기 위해 uint8 이미지 `[[7]]`, 대칭·홀수 footprint `[[1,0,1]]`를 설치된 SciPy 1.17.0의 grey_dilation에 입력했다. reflect는 `[[7]]`, constant dtype-min=0은 `[[0]]`, 문구를 문자 그대로 적용한 dtype-max=255는 `[[255]]`였다. complete skimage0.26 API를 실행하지 않았다. 이 footprint에는 중심점이 없으므로 결과가 원값보다 작다는 사실만으로 dilation 오류라고 할 수 없다. [V-R5-BOUNDARY; executed-checks.json; imaging의 Soille 원전 대조]

원 글은 이미 dtype-min 경계와 사용자 mode 선택을 제안했다. 2023-01-14 유지보수자는 기본값 변경보다 mode 노출을 선호했다. 현재 API도 기본 reflect를 유지하며 mode/cval을 제공한다. 사용자의 의도를 “모든 경우 기본값을 min으로 바꾸라”로 좁히면 이 반대 관점을 놓친다. 다만 같은 사람의 실제 코드 변경·원전 채택은 확인하지 않았다. [REQ-R5; COMMENT-1382729471; R5-COMMON]

A5 첫 3000자는 시간축 median/variance 설명이다. 사후 뒤 절에는 diamond(3) opening→dilation→프레임별 inpainting 순서, diamond(1)/disk(3) 대안, 그리고 (x,y)≈(719,1237)의 먼지 점을 opening에서 잃었다는 명시적 실패가 있다. 이 예제는 자신의 실패와 실제 좌표를 주는 강한 반례다. 하지만 비연속/중심이 벗어난 footprint의 영상 외곽 처리 문제를 해결하지는 않는다. 발견 봉인 뒤 읽은 뒤 절이며 처음 경로의 성공으로 바꾸지 않았다. [V-LATE-HOP-R5-A]

다음 gallery인 Morphological Filtering도 직접 읽었다. phantom과 disk(6)의 max/min 및 순서 차이는 유용하지만, 중심이 포함된 연결 footprint의 작동 예를 비연속 footprint 경계 계약에 일반화할 수 없다. 첫 연결 예제 교체가 아닌 사후 반례 자료다. [V-MORPH-GALLERY]

## R2/R6: 공석을 후속 지식으로 메우지 않는다

R2의 현재 댓글에서 원 작성자 bmcfee는 2024-04-03 mir_eval에 NaN 지원 PR을 냈고 librosa의 예정 feature에서 뺀다고 말한다. 모집 당시에는 보지 않았다. 원래 요청된 librosa public symbol이 없다는 공석은 유지한다. 이 발언은 역사적 후속 의향의 증거이며 해당 PR의 실제 변경 및 본 연구 링크의 채택은 미확인이다. [COMMENT-2034816835]

R6 초기 단일 API 보류는 v2에서 정정됐다. 원글의 목표 조작을 literal 순서로 읽으면 outer lch2lab가 먼저다. 고정 공식 공통절1262자를 읽고 A/B 모두 적격 추가 링크 없음으로 대사했다. dtype assertion은 rgb2lab 뒤 lab.dtype이며 lab2.dtype가 아니다. s390x/NumPy1.24.1의 수치 회귀는 실행하지 않았다. [evidence/corrections/R6-v2.json; R6-correction-read.json]

사후 공개 recurrence_matrix의 width guard를 확인하니 처음 제안한 3점 public 입력은 실행 전 거부되는 무효 후보였다. 이를 보존하고 기각한다. 위 3×3 CSR의 helper 실행과 혼동하지 않는다. 후속5점 후보는 아직 미실행이다. [V-R3-PUBLIC-GUARD]

## 실행과 미실시

실제 실행한 것은 창 시작점 산술 1묶음, 분리한 고정 함수 4입력/모드, SciPy 경계 3조건이다. 도구 출력은 executed-checks.json에 있다. 전체 대상 라이브러리 설치, MKV decode/tokenizer, original Csync, s390x roundtrip, 논문 데이터셋 및 전체 gallery는 실행하지 않았다. 필요한 명령·입력은 EXECUTION_PLAN.md에 따로 남긴다.
