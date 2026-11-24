# 두 최소 링크 카드
## 영상: 이진 전경/배경 연결 정책
- 목표: 전경 또는 배경 중 어느 집합이 모서리 접촉을 연결로 보는지 정한다. 입력이 2값이면 threshold는 두 값 사이 중간을 선택. 대각 +와 −가 각각 연결되는 것을 동시에 보장할 수 없다.
- 첫 링크: [scikit-image find_contours Notes](https://scikit-image.org/docs/0.25.x/api/skimage.measure.html#skimage.measure.find_contours), fully_connected / positive_orientation 구분. [ImageJ Wand §19.7](https://imagej.net/ij/docs/guide/146-19.html) 대각선 추적/장벽 반례.
- 최소 설정: low(default) → C1~C4의 양의 NW/SE 분리(A); high → B. orientation 변경은 pair 변화 아님. 마스크·이미지 외곽을 만나는 선은 열림.
- 원전 추가 조건: 사용자가 분류값이 아니라 측정된 연속값의 셀 내부 topology까지 보존하길 요구하거나 고정 연결이 왜 부적절할 수 있는지 묻는 경우. 2값 분할 의도만이면 논문은 정답을 대체하지 않는다.
## 지도/측정 스칼라: 명시한 보간 모델
- 목표: 서로 다른 크기의 실제 측정값을 셀 안에서 연속적으로 보간. 단순 폴리라인이 필요하고 serial 기본값을 받아들인다면 [ContourPy description](https://contourpy.readthedocs.io/en/v1.3.3/description.html) + [z_interp](https://contourpy.readthedocs.io/en/v1.3.3/user_guide/calculate/z_interp.html).
- 원전을 추가해야 할 정확한 조건: 네 변 교차, strict alternating signs, 셀 내부 bilinear model을 목표로 하고 중심 부호와 saddle 부호가 다르거나 고정 대각선과 다를 때. C3 NW8 NE−4 SE1 SW−3, level0, center +.5→B, saddle −.25→A. [Nielson/Hamann §2 pp84–85](https://graphics.stanford.edu/courses/cs164-10-spring/Handouts/paper_p83-nielson.pdf)와 [Custodio §3.1 Eq2](https://www.sci.utah.edu/~etiene/pdf/mc33.pdf) 또는 [Lewiner §4(a)](https://thomas.lewiner.org/pdfs/marching_cubes_jgt.pdf). 원 스캔의 plus 식을 그대로 복사하지 말 것; 후속과 독립 유도는 minus.
- 해석 제한: bilinear 자체가 실제 지형을 복원한다고 단정하지 않는다. [GDALContourGenerateEx](https://gdal.org/en/stable/api/gdal_alg.html) 픽셀 중심, NODATA 및 saddle 두 그림; [GRASS r.contour NOTES/EXAMPLES](https://grass.osgeo.org/grass-stable/manuals/r.contour.html) 등고선 고도 선택과 exact-value backtracking 경고. C4 saddle=level이면 crossing/분기 정책을 따로 요구. 단일 교차는 원전의 추가 판별이 없다.
