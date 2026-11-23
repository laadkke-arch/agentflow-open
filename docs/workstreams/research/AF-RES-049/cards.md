# 설계자에게 반환할 문장

## M03 · 색 막대의 설명

> 색 막대의 가운데에 같은 설명을 두려면 `cb.ax.text(.5, .5, ..., transform=cb.ax.transAxes, ha="center", va="center")`를 쓰세요. 3.0.2/Agg의 두 입력에서 축 비율 (.5,.5)과 글자 픽셀을 확인했습니다. 색 막대 한가운데가 아니라 실제 y=.5에 표시할 때에는 세로 좌표를 데이터에 두고, 가로 가운데가 필요하면 `blended_transform_factory(cb.ax.transAxes, cb.ax.transData)`를 쓰세요. 값 .5가 막대의 범위 밖이면 값 .5를 막대 내부 위치로 표시할 수 없습니다.

인쇄의 페이지 여백 중앙 기준과 지도 라벨의 지물 기준은 각각 보존할 대상에 대한 참고다. 같은 목표에서 사용할 API는 3.0.2의 `Axes.text`에도 예시가 있다. 2.2.2의 기본 colorbar 좌표 [0,1]은 두 숫자를 우연히 같은 중앙에 놓았다. [인쇄 §6 Table 1](https://www.w3.org/TR/2013/WD-css3-page-20130314/#margin-boxes) · [Adobe Custom X/Y](https://helpx.adobe.com/indesign/desktop/add-graphics-and-media/transform-and-arrange-objects/create-position-anchored-objects.html) · [Maplex Label Position](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm) · [Axes.text 예제](https://github.com/matplotlib/matplotlib/blob/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/axes/_axes.py#L690) · [G1 관측](evidence/observations.md#m03)

## M02 · 고정 캔버스와 넘치는 범례

> 10×3인치를 유지하면서 넘치는 범례가 데이터 축 배치를 좌우하는 것을 막으려면 `legend.set_in_layout(False)` 뒤에 `tight_layout()`을 호출하세요. 이 입력에서 30개 B의 두 데이터 축은 범례가 없는 대조와 같았고, 범례 이름은 12개가 보였습니다. 계열 이름을 모두 읽어야 한다면 30개 B로는 부족합니다. 그때에는 읽을 공간을 늘리거나 나눠서 배치하세요.

인쇄의 넘침 처리와 지도의 충돌 라벨 우선순위는 같은 B를 권할 수 있다. 둘 다 완전 표시에 비용이 생길 때 무엇을 우선할지 묻는다. QGIS에는 충돌 라벨을 전부 켜고 배치를 수정하는 선택도 있다. CSS는 출력 크기·회전·분할이 허용되는 경우를 별도로 둔다. 현재 재생은 PNG의 글자 판독과 axes bbox를 확인했으며 15색이 반복되는 30계열을 독자가 모두 찾아내는 데 걸리는 시간은 미확인이다. [W3C §8.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/#rend-page) · [QGIS Rendering](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html#rendering-tab) · [3.0.2 Tight Layout Guide](https://matplotlib.org/3.0.2/tutorials/intermediate/tight_layout_guide.html#legends-and-annotations) · [PNG 판독](evidence/png-readback.csv)
