# AF-RES-199 HANDOFF

**실제 판정: PARTIAL.** 핵심 원리/조작 판별은 성립하나 자료 유형 하한 A 1개·C 1개 부족 및 exact pfstmo 배포 소스 동일성 미확인. 합계 산입 22개로 유형 부족을 대체하지 않음. 동시 과제 불필요. 제품 최종 구조/순위는 미결정.

- 계획판 050278651b11a2a3a49d45baebf41c707c06b700; 시작판 c860f8240ab7b7077e2d5b63e438ddd83ff69a27(계획 +4, -0; dot-control 변경만). 191 result_commit 19ae6c6d17cc8adecec948d7103b7d3e81e428b6 읽음.
- 브랜치 work/research-af-res-199. 결과가 든 직전 SHA **a887a30241cd0daf0b1c1345681f5adcce9a69a3**. ① d684fcdac9cd4b273a51c99884e3a006a5133f95, ② 34ae74457dc7785d5993c03b9047f9defd79afb7, ③ 36ecf49e9ade424730750ad9ccb542fbc964b785, ④ 484d1e8a92c91959087d1628017edced97bb1edd, ⑤ a887a30241cd0daf0b1c1345681f5adcce9a69a3. 이 HANDOFF만 ⑥ 마지막 커밋.
- 대표 파일: [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [SCOPE.md](SCOPE.md), [frame.csv](frame.csv), [sources.jsonl](sources.jsonl), [lineage.csv](lineage.csv), [operators.csv](operators.csv), [cards.csv](cards.csv).
- 직전 SHA에서 위 8파일을 직접 재조회; JSONL 파싱 52행/고유 source_id 52, 산입 22, 15 failed, 8 normalized lineage_id, 13 case_id(독립 실험 수 아님), frame 54행=52+결손 2, 조작 6/카드 3, RESULT 필수 3헤더 순서 및 마지막 표 약점 3행 확인. GitHub compare 시작→직전 ahead 5/behind 0, 변경 8파일 모두 owned_path. dot-control 수정 없음. 실행/독립검토/workbench manifest 실행 없음(직접 connector 작업).
- A3/4: A01·A02 원논문 본문, A07 독립 저자 후속 논문. A08 전사된 발표자료는 원저자판 파일 미확인, A09 논문 중복, A14 Utah source 접근 불가. B9/7: B07/B08 고정 mirror 포함, 제외 시에도 정확 버전 기록 7; mirror의 official release byte identity는 미확인. C4/5: C02 입력 출전, C05 원해설 목록, C07 구현자 후속 수정 설명, C08 고정 테스트 사양. 실제 binary/실행 비교 없음. C01 직접 403 재확인; C06 독립 비교는 고정 소비자 저자 아님. D4/4(단일 negative 1건; D01 원지시 facsimile 노출량 직접 판독 못함), E2/2. 선호도/화질 우위 미판정.

## 남겨진 핵심 판단

1. 2002 A01 §3 Eq1–9 → pfstmo reinhard02 key .18/선택적 multi-scale --scales, phi CLI 1 vs paper 8. 공간 이웃/scale-based adaptation. Eq1 인쇄 표기와 실제 geometric mean은 A07로 의도 확인, Eq8 비교/인덱스 exact 동일성 미확인. 단일 Y 휘도 매핑 및 XYZ 공통 배율, channel/light adaptation knob 없음.
2. 2005 A02 §3 Eq2–7, Fig7 → OpenCV 4.10.0 RD05 인용 및 tonemap.cpp L219–250: f=exp(-intensity), 자동 m, pixel/global 및 채널/휘도 혼합. O2 local=픽셀, 공간 반경 아님. paper §4 Fig9 spatial extension은 API 미노출. C07 후속 PR은 반복 호출 설정 변이 문제 수정(고정 4.10.0에는 수정 미반영). 이름/목적 동일≠연산 동일. 근접 문서로 단순 호출 선택은 완료되는 반례 존재.
3. 인화자의 영역별 의도는 D01–04가 뒷받침하되 원지시 초/마스크 미측정. 원전 설명/호출/공개 결과 목적별 링크를 분리하고, 한 링크로 충분하면 불필요한 원전 링크를 강제하지 않는다.

## 재개 첫 행동과 미실행 검증

먼저 공식 pfstools 2.2.0 tarball 및 Debian 2.2.0-9 source에서 reinhard02 두 파일을 확보하고 고정 mirror 7cd588d9ee56fee3190c82916a9fd9c9971d6a3b와 비교한다. 원저자 원본 source 또는 발표 PPT를 A 추가 1개, MPI 구현자 원페이지/다른 독립 결과 원해설을 C 추가 1개로 확보하되 재게시/동일 그림 제외. MPI https://resources.mpi-inf.mpg.de/tmo/reinhard02/index.html 403, Utah https://www.cs.utah.edu/~reinhard/cdrom/source.html 접근 실패. 직접 열람 가능 경로가 생기면 우선 그 원본·판·설정·출력 확인. https://pfstools.sourceforge.net/ upstream release 및 https://sources.debian.org/src/pfstools/2.2.0-9/ 재개 출발점. D01 원 printing instructions 고해상도 확인은 추가 작업.

다음 명령은 Codex용 **미실행 제안**. 설치·다운로드·빌드 승인 및 네트워크/환경 확보 후 별도 임시 디렉터리에서 수행; 이번 조사 브랜치의 타 파일 수정 금지. Debian trixie deb-src 2.2.0-9이 있을 때:

```sh
mkdir -p /tmp/af-res-199-check && cd /tmp/af-res-199-check
apt source pfstools=2.2.0-9
git clone https://github.com/flyingfalling/pfstools.git mirror
git -C mirror checkout --detach 7cd588d9ee56fee3190c82916a9fd9c9971d6a3b
for f in tmo_reinhard02.cpp pfstmo_reinhard02.cpp; do
  sha256sum pfstools-2.2.0/src/tmo/reinhard02/"$f" mirror/src/tmo/reinhard02/"$f"
  diff -u pfstools-2.2.0/src/tmo/reinhard02/"$f" mirror/src/tmo/reinhard02/"$f"
done
dpkg-query -W pfstmo pfstools
```

기대: 차이 유무와 정확 위치를 보존하고 Eq8/scale index/CLI defaults/zero guards를 재판정. apt source 경로와 설치판은 실제 출력 확인 후 사용. 원 tarball/패치의 SHA도 별도 보존. 설치된 pfstmo가 확인된 2.2.0-9일 때 C02 원입력 memorial.hdr의 SHA256 기록 후 다음 명령. 실제 출력과 동일 gamma/입력으로 비교, 각 오류/exit status 기록.

```sh
sha256sum memorial.hdr
pfsin memorial.hdr | pfstmo_reinhard02 --key .18 | pfsgamma -g 2.2 | pfsout global.png
pfsin memorial.hdr | pfstmo_reinhard02 --scales --key .18 --phi 1 | pfsgamma -g 2.2 | pfsout local-phi1.png
pfsin memorial.hdr | pfstmo_reinhard02 --scales --key .18 --phi 8 | pfsgamma -g 2.2 | pfsout local-phi8.png
# --phi 0 / --key 0 의 exit 및 stderr도 별도 기록.
```

OpenCV 고정 버전: 승인 후 임시 venv에서 opencv-python==4.10.0.84 및 numpy<2 설치, wheel 버전·hash와 cv2.getBuildInformation 기록. 공식 tag 소스와 wheel 빌드 동일성은 별도 확인. 입력은 32x32, 채널별 양의 서로 다른 값, float32, deterministic permutation. 코드가 예측하는 getter 0→1→exp(-1), 새 instance에서 역순열 출력 일치(오차 허용), 균일 이미지 NaN 가능성 시험. 결과를 미리 참으로 간주하지 않음.

```sh
python -m venv /tmp/af-res-199-cv
. /tmp/af-res-199-cv/bin/activate
python -m pip install 'opencv-python==4.10.0.84' 'numpy<2'
python - <<'PY'
import cv2 as cv, numpy as np
assert cv.__version__ == '4.10.0', cv.__version__
rng=np.random.default_rng(199)
x=rng.uniform(.1,100,(32,32,3)).astype(np.float32)
p=rng.permutation(32*32)
perm=x.reshape(-1,3)[p].reshape(x.shape).copy()
def new(): return cv.createTonemapReinhard(1.,0.,1.,0.)
def run(op,a): return op.process(a.copy())
o=new()
print('initial',o.getIntensity())
y=run(o,x); print('after1',o.getIntensity())
z=run(o,x); print('after2',o.getIntensity())
print('repeat max abs',np.max(np.abs(y-z)))
fresh=run(new(),x)
yp=run(new(),perm).reshape(-1,3)[np.argsort(p)].reshape(x.shape)
print('permutation max abs',np.max(np.abs(fresh-yp)))
for a in [np.ones_like(x),np.zeros_like(x)]:
    try: print('constant finite',np.isfinite(run(new(),a)).all())
    except cv.error as e: print('constant error',e)
PY
```

C08의 golden test 입력·기대값은 opencv_extra 4.10.0의 실제 testdata 경로를 찾아 binary SHA를 고정. C10 기존 잘못된 경로 404; cv 하위 경로 후보 검토. 비교 시 RGB 순서/휘도식/정규화/출력 gamma의 동일성 여부를 기록. pfstmo에 동일 multiset의 spatial permutation을 적용하려면 원 EXR/PFS 입력 생성 및 XYZ 변환을 검증한 뒤 global vs scales 비교. 공간 픽셀 배치가 바뀌어도 OpenCV는 fresh object에서 동일 multiset 통계(부동소수 오차 제외)로 동일 대응 픽셀 출력이 예상되며, pfstmo local은 달라질 수 있다는 가설. 실제 검증 전 단정 금지. 사람 화질 선호는 별도 실험.

## 색인 반영 제안

AF-RES-199 (PARTIAL) — HDR의 Reinhard02 photographic exposure/local scale vs Reinhard05 photoreceptor intensity/pixel-global/channel adaptation; 동일 이름 오전이와 API 미노출, fixed-version mutation, print intent 구분. RESULT/lineage/operators/cards의 조작 중심 링크 설계 참고. A·C 각 1개 부족 및 pfstmo exact release 소스 대조가 해결될 때만 DONE 재판정. dot-control 및 색인 파일은 이 작업에서 직접 변경하지 않음.
