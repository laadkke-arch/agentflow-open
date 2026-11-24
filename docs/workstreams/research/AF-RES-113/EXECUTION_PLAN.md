# AF-RES-113 미실시 실행과 필요한 입력

이 문서의 명령은 다음 작업자를 위한 것이다. 명령을 적은 사실을 실행 성공으로 세지 않는다. 실제 수행한 helper·SciPy backend·산술은 evidence/verification/{project,network,external}의 실행 JSON을 따른다.

## 결과 원장과 계약 검사

HANDOFF의 결과 SHA를 깨끗한 checkout으로 만들고 다음 명령을 저장소 루트에서 실행한다. TMPDIR은 그 checkout의 docs 밖에 둔다. 검사 결과는 입력 SHA·exit·stdout·미실시 범위와 함께 저장한다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-113/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-113/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

## 고정 라이브러리 실험 환경

필요 버전은 librosa1.0.1(9caf46a4ecaeb8ea24bb541231065c9f761174ae), scikit-image0.26.0(ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8)다. 설치는 아래 owned 경로의 분리 venv에 한다. 이 과제에서는 이 설치와 전체 대상 실행을 하지 않았다.

```sh
python -m venv docs/workstreams/research/AF-RES-113/evidence/cache/target-venv
docs/workstreams/research/AF-RES-113/evidence/cache/target-venv/bin/python -m pip install librosa==1.0.1 scikit-image==0.26.0
```

| 요청 | 필요한 입력 | 실행·대조할 명령 또는 정확한 호출 | 판단 변경 관측 |
| --- | --- | --- | --- |
| R1 | 원 filename.mkv bytes, codec/native SR, tokenizer 이름·판·입력 SR·꼬리 처리 계약 | `librosa.load(path,duration=10,sr=16000)`와 `librosa.stream(path,block_length=10,frame_length=16000,hop_length=16000)`를 동일 파일에 실행. decoder 성공 뒤에만 sr=16000 변형과 tokenizer 비교. STFT 별도 구성 입력은 긴 impulse와 F4096/H1024/B256, `stft(block,center=False)` 대 `stft(block,n_fft=4096,hop_length=1024,center=False)`의 프레임 시작·계수를 비교. | codec 지원과 표본율 계약을 만족한 동일 원파일 결과가 나오면 수리 보류를 좁힐 수 있다. |
| R2 | 작성자가 뜻한 target API 또는 독립 기능 경계, voiced/unvoiced f0와 sr/hop, mir_eval 실제 PR diff | 기존 mir_eval pitch_contour와 제안 nancumsum 방식에 동일 f0·시간격자를 넣어 경계 근처 파형/주파수를 비교. API를 지정받기 전에는 pyin으로 대체 실행하지 않는다. | 보존조건이 명시되고 함수가 확정되면 새 모집/공통판으로 진행한다. |
| R3 | 원 Csync 또는 재현 가능한 graph 생성 fixture | `librosa.segment.recurrence_matrix(np.array([[0.,.1,10.,10.1,100.]]),k=1,width=1,sym=True,mode='affinity',bandwidth='med_k_scalar')`와 mean_k/gmean_k를 비교. 최초 3점 후보는 width guard로 무효이므로 쓰지 않는다. 이 5점 후보도 현재 미실행이며 예상 graph를 먼저 출력해 검증한다. | 실제 유효 public 입력에서 부분 빈 행·전체 빈 행과 조건부 오류가 확인되어야 helper 수준 결과를 확대한다. |
| R4 | 1D 원 입력 및 정상2D/3D fixture | `rank.otsu(np.eye(10,dtype=np.uint8).ravel(),disk(3))`, 정상 `rank.otsu(np.eye(10,dtype=np.uint8),disk(3))`, 정상3D `rank.otsu(np.zeros((5,5,5),dtype=np.uint8),ball(1))`의 오류 종류·문구·shape를 비교. | 정상 동작을 보존하며 1D 메시지가 정확한지 확인한다. |
| R5 | 원 비연속 footprint, 64bit 영상, 경계 mode 요구 | `morphology.dilation(np.array([[7]],dtype=np.uint8),footprint=np.array([[1,0,1]],bool),mode=m)`를 m=reflect/min/ignore/constant(cval=0,255)에 실행. 원 64bit 입력에서도 dtype/출력을 비교한다. | 전체 target API가 소스 min 및 backend 관측과 다른 결과라면 반환을 정정한다. |
| R6 | s390x 하드웨어/runner, 원 skimage0.19.3+#6637 commit, NumPy1.24.1 대1.23, Python3.10.9/3.11.1·SciPy1.8.1 | 아래 원 시험 형태를 dtype float16/32/64 각각 실행하고 원 버전·현재판을 분리 기록. 필요한 원 commit/환경이 없으면 과거 재현으로 보고하지 않는다. | 같은 입력의 architecture/version별 차이와 원인·수리가 확인돼야 수치 해결 링크로 승격한다. |

R6 원 시험 핵심은 다음과 같다. dtype assertion 대상은 lab2가 아니라 rgb2lab의 결과 lab이다.

```python
rgb = img_as_float(data.colorwheel()).astype(dtype=dtype, copy=False)
lab = rgb2lab(rgb)
float_dtype = _supported_float_type(dtype)
assert lab.dtype == float_dtype
lab2 = lch2lab(lab2lch(lab))
decimal = 4 if float_dtype == np.float32 else 7
assert_array_almost_equal(lab2, lab, decimal)
```

## 실행한 고립 검사의 재실행

`verify_examples.py`는 고정 segment.py 캐시와 numpy/scipy를 필요로 한다. 소스의 expected SHA256은6f5fc0aa99569f0e1d2f1d42d82b12eb49158243f4736d76b6c26408c0f97f5f다. 캐시 위치는 스크립트의 실제 Path를 따른다. 이것은 전체 librosa/skimage 실행이 아니다.

```sh
python -B docs/workstreams/research/AF-RES-113/verify_examples.py
python -B docs/workstreams/research/AF-RES-113/evidence/verification/network/arithmetic_check.py
python -B docs/workstreams/research/AF-RES-113/evidence/verification/external/counterexample_arithmetic.py
```

외부 실험의 원 데이터·GDAL TIFF·측정 clock 로그는 제공되지 않았다. 원 자료의 실측 주장과 구성 산술을 분리한다. 외부 상세 실행은 evidence/verification/external/execution-plan.md의 입력·예상값을 따른다. 임시 원문 캐시 손실 때문에 동일판 재취득 해시가 다르면 원 노출의 재현 실패로 기록한다.
