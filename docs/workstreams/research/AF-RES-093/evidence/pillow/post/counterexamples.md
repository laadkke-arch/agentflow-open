# Pillow Q6 · 네 반례 축과 세 관점

모든 행은 신규 P1–P3 정확도 분모와 분리한다. 원시험을 직접 읽었으나 실행하지 않았다. 사실과 추론을 각 칸에 표시한다.

| 반례 축 | 직접 원자료·입력·관측 또는 기대 | 생산자 | 편집을 이어갈 사용자 | 링크 목록 정리자 | 판정을 바꿀 최소 관측 |
|---|---|---|---|---|---|
| 화면과 alpha만 필요하면 두 표현이 충분 | [test_putpalette_with_alpha_values](https://github.com/python-pillow/Pillow/blob/a9372d5cf0aa6a56f6e4aa5399f01b2485b1012f/Tests/test_image_putpalette.py#L50-L64), PIL-POST5. **시험 사실:** transparent.gif의 info 투명 인덱스를 RGBA 팔레트의 alpha로 옮긴 뒤, convertRGBA 결과가 원 expected와 같음을 assert | RGBA로 읽을 소비자에게 동등한 결과를 제공 가능 | 다음 작업이 info의 원 투명 번호를 직접 읽는다면 표현 차이를 알아야 함 | 표시·RGBA 소비 목적에 한해 대표 링크를 남김. 모든 metadata 계약의 대체품으로 합치지 않음 | 양 표현을 같은 합성기에 넣었을 때 RGBA가 다르거나, 소비자가 원 info key의 존재를 요구하는 입력 |
| 색을 유지하면서도 index로 고르는 대상은 바뀜 | [11.3.0 remap 구현](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/src/PIL/Image.py#L2103-L2191), PIL-CE6 + [원 시험](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/Tests/test_image.py#L686-L701), PIL-CE1. **시험 사실:** swap[1,0] 후 transparency 0→1. **코드 추론:** 픽셀과 팔레트를 함께 치환하므로 RGBA 소비자는 색을 유지하지만 숫자 0을 고르는 소비자는 다른 색 항목을 고름 | 팔레트 최적화·재배열을 같은 모양으로 납품 가능 | 원 index가 class label이면 대응표 보존 또는 변환 금지 필요 | 색만 읽는 조건과 원 숫자 label 조건을 별도로 설명 | 같은 판에서 nonidentity swap 전후 RGBA와 raw index 0의 좌표를 함께 assert한 자료. 현재 원시험에는 전체 RGBA 비교가 없음 |
| 이름·경로가 달라도 읽기 결과는 같음 | [P3 유지관리자 출력](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030), PIL-POST3. **보고 사실:** 8.3.0에서 팔레트 객체와 raw 배열의 getpalette 결과가 같고, raw 경로의 dirty 재로딩 후에도 유지 | 새 RGBRGB 순서의 p를 공급 | 8.3.0 getpalette 검증에는 두 경로를 쓸 수 있음. 8.2 지원이면 raw를 선택 | 8.3.0 한정으로 묶고, 버전 간 대표 링크는 raw putpalette | 같은 p에서 양 경로를 각각 dirty 또는 저장 후 비교해 한쪽만 달라지는 결과. 현재 dirty는 두 경로를 독립 비교한 출력이 아님 |
| 원 정보가 합쳐지면 필드로 복구 불가 | [test_transparent_colors_equal](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/Tests/test_image_quantize.py#L127-L136), PIL-CE2. **시험 사실:** 투명 검정과 투명 흰색을 quantize하면 같은 P index. **추론:** 출력 팔레트·index만으로 어느 원 숨은 RGB였는지 유일하게 복구 불가 | 표시만 보존하는 축약은 충분할 수 있음 | 이후 alpha 편집으로 숨은 RGB를 드러내거나 원 raw값으로 분류하려면 원본·sidecar 필요 | 이미 없어진 정보를 설명 필드가 복구한다는 링크는 권하지 않음 | 출력에 원 raw RGB·식별자가 별도로 저장되어 역변환 가능한 파일. 이 원시험에는 그런 보존 계약 없음 |

## 이 원리가 실패하는 실제 판

[Pillow #6349](https://github.com/python-pillow/Pillow/issues/6349), PIL-CE3는 9.1.1에서 RGBA 팔레트의 두 항목을 바꾼 뒤 PNG로 저장하면 투명도가 사라진다고 보고했다. [PR6350](https://github.com/python-pillow/Pillow/pull/6350), PIL-CE4는 remap이 RGB만 반환하던 부분에 RGBA 지원을 더했다. 따라서 ‘인덱스와 팔레트를 함께 바꾸면 모양이 언제나 같다’는 판 불문 주장은 틀린다. 수정의 identity 시험도 모든 nonidentity 입력을 증명하지 않는다. 11.3.0의 적용 코드와 9.1.1 사건을 혼합 채점하지 않았다.

[Pillow #6263 유지관리자 예제](https://github.com/python-pillow/Pillow/issues/6263#issuecomment-1116052542), PIL-CE5는 `convert('P', palette=...)`와 `quantize(palette=...)`의 비슷한 인자명이 같은 계약을 뜻하지 않음을 보인다. 사용자가 원하는 index 0/1을 이미 명시했으므로 ‘색만 중요한가요?’를 다시 묻지 않고 지정 팔레트를 따르는 quantize 예제를 반환할 수 있다. 이 사건에서 양 경로의 모든 RGBA 픽셀까지 동일한지는 확인하지 못했다.

## 한 번의 질문이 필요한 경우

팔레트 재배열 요청에 원 숫자 index 보존이 없다면 **‘뒤에서 팔레트 번호 자체로 픽셀을 고르나요, RGBA 색만 사용하나요?’**를 한 번 물을 수 있다.

- RGBA 색만 사용한다는 답: 고정 수정판의 [remap_palette](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/src/PIL/Image.py#L2103-L2191)와 RGBA 비교 조건을 제시한다.
- 원 번호로 고른다는 답: 원 번호·재배열 대응표를 보존해야 한다. 기존 remap 링크 하나로 대체 가능하다고 합치지 않고, 숫자가 바뀌는 [원 시험](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/Tests/test_image.py#L686-L701)도 함께 제시한다.

P2의 RGBA 결과 조건은 원문에 있어 다시 묻지 않는다. P3는 후속에서 raw 배열로 충분하다는 답을 이미 얻었다. P1의 색 보존도 원문에 있으므로 반복 질문 대신 전체 두 후보 결과와 수행판의 확인이 부족함을 설명한다.

탐색 범위는 선택한 3개 issue의 후속 전체, PR5594·5599·5606, #6349·PR6350, #6263, 고정 11.3.0의 test_image·test_image_quantize 및 수정 PR의 putpalette·GIF 시험이다. 이 범위 밖의 모든 팔레트·codec·OS에서 반례가 없다고 주장하지 않는다.
