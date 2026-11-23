# Pillow 실제 반환 링크 초안

## P1 · GIF 자막의 원색·흰 캔버스·검은 글씨

[8.2.0의 RGB 변환](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/Image.py#L862-L901) 후 [expand](https://github.com/python-pillow/Pillow/blob/e0e353c0ef7516979a9aedce3792596649ce4433/src/PIL/ImageOps.py#L365-L379)를 실행하는 순서를 반환한다. 원 작성자가 **테두리를 더하기 전** 변환하면 해결된다고 보고했다. 두 호출은 함께 필요한 단계이며, 전체 GIF 저장색을 검증한 두 완성 대체품으로 합치지 않는다. 고친 GIF·실행판·픽셀값은 미확인이다. [작성자 근거](https://github.com/python-pillow/Pillow/issues/5406#issuecomment-820672806).

## P2 · 투명 P 이미지를 RGBA로 읽기

[8.3.0의 명시 RGBA 분기](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1008-L1017)를 반환한다. 요청이 RGBA를 명시했으므로 자동모드와 묶지 않는다. 원파일의 두 호출 출력을 독립적으로 대조한 검사는 미확인이다. [당시 자동모드 수정](https://github.com/python-pillow/Pillow/pull/5594)은 원판과 수정판의 차이를 설명하는 보조 링크다.

## P3 · RGB 순서의 팔레트 배열을 부착하고 다시 읽기

[배열을 직접 받는 putpalette](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1749-L1776)를 대표로 반환한다. 원 유지관리자가 같은 p를8.2.0/8.3.0에서 읽어 비교했고, 원 작성자도 이 경로가 목적에 충분하다고 수용했다. [ImagePalette 객체 경로](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/ImagePalette.py#L24-L95)는8.3.0의같은p계약에서같이묶을수있지만8.2.0의채널별배열동작까지같다고설명하면안된다. [두판·두경로의원출력](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030).

이 카드는 연구자가 제안한 반환형식이며 실제 사용자에게 제시한 경험이나 절약시간을 측정한 결과가 아니다.
