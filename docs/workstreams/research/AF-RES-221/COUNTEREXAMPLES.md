# 반례 및 정정
## 그림/정규화
NW a ------- N ------- b NE
 |                     |
 W                     E
 |                     |
SW d ------- S ------- c SE
A: N–W, E–S (a,c 각각 고립); B: N–E, S–W (b,d 각각 고립). C=E–W. Array row 증가 방향은 아래; CP default y=row인 Cartesian 표현에서는 화면 위아래가 반대일 수 있다. N,S는 항상 array 기준.
## 독립 반례
1. 같은 부호, 다른 크기: C1/C2 동일 sign mask인데 bilinear A/B, center A/B, fixed skimage A/A. C3에서는 두 products 8,12, center +0.5와 saddle −0.25로 center decider가 bilinear topology와 반대. P가 CP 문서의 default 예측을 교체하는 것이 아니라 보존 목표가 다름.
2. 정확 동률 C4: f=2−4u−4v+8uv=8(u−.5)(v−.5). 영집합은 u=.5 또는 v=.5의 교차; 네 변이 한 연결 성분. 두 폴리라인 A/B 어느 것도 동일 위상은 아님. P01 §2의 비교 분기 자체에는 tie policy가 있어도 mathematical singularity와 분리. C4 둘 다 default strict > 이므로 low 연결 A; 작은 δ를 a에 더하면 Q와 center 모두 양수, 빼면 음수. 정밀도/수치 overflow near Q=0 미측정.
3. 축 반전: 좌우 flip C3 -> (−4,8,−3,1), Q'=−Q=4, D'=−D=−16, saddle 여전히 −.25, center +.5. edge label permutation W↔E, A↔B. 단순 Q sign만 high/low 연결로 해석하면 오류. 회전/행 반전도 edge labels와 orientation 변환 필요. 전체 부호 반전: strict nonzero corner/center면 center/bilinear pairing 동일, fixed-low 교환. C4 exact equality는 부호 반전에도 tie policy가 low를 선택해 pairing 반전 가능.
4. boundary open/mask: C5 2x2 E–W endpoints가 array 외곽이라 open; E01 mask example endpoints (6,.5),(6,1.5) public expected; I02 skip whole affected square; CP corner_mask=True retains available three-corner triangle, cannot force 4-edge pairing. E03 chunk splits output though geometric chain may be same; do not compare ordered output as topology.
5. log mode E05: unshifted [[1,100],[100,1]], positive levels 1.1,9.9,10.1,99.9; center geometric10 vs linear50.5, so level10.1 gives opposite center branch. This test uses explicit Log, not default. Negative/zero controls not legal Log inputs. 
6. Nonambiguous C5, R1, R2: only two crossings. P adds no pair information; edge interpolation location/orientation still determined by docs/code.
## Corrections and weak points
- P01 facsimile p85 appears plus in saddle numerator. Differentiate matrix bilinear form in §2: f=a+(b−a)u+(d−a)v+Duv. Critical point u=(a−d)/D,v=(a−b)/D. Substitute f_s=(ac−bd)/D. P02 Eq2 and P03 face-test explicitly minus. Do not infer typo history; alternate typeset copy unconfirmed. Literal plus yields wrong C1,C3 and falsely nonzero C4. 
- Source count correction: SCOPE_ADDENDUM first clause 25 is typo; arithmetic correct 24 counted =3+5+5+7+4, 33 rows 9 excluded. E07 baseline not seen; count source file only.
- R2 input/expected co-exposed, empty=False for nonempty level .5 (inputs.csv wording “nonempty=True? actual empty=False” means parameter empty=False). CP test_config generated cases precede literal grid criterion; R2 is not proven first across entire repository. Exact numeric expectation absent for primary R2; E03 fixed expected supplement cannot substitute independently.
