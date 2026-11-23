# 반환 카드 후보

**사진 / RPA**: [Rows Layout](https://github.com/igordanchenko/react-photo-album#how-it-works) — 현재 설명에서 DAG와 제곱 편차를 확인. 여러 장의 목표 행 높이 배분이 문제라면 이 링크를 우선한다. 한 장 끝 행·원본 크기 제한·크롭이 문제면 [issue #121](https://github.com/igordanchenko/react-photo-album/issues/121), [#99](https://github.com/igordanchenko/react-photo-album/issues/99), [Flickr #24](https://github.com/flickr/justified-layout/issues/24)를 우선하고 전체최적화 추천을 보류한다.

**악보 / Verovio·MuseScore**: [Verovio output layout](https://book.verovio.org/advanced-topics/layout-options.html), [MuseScore breaks](https://musescore.org/en/handbook/2/breaks-and-spacers) — 시스템/페이지 수동 지시가 보존 조건이면 구현·판각 지침 우선. [#113](https://github.com/rism-digital/verovio/issues/113)의 한 번만 삽입한 강제 sb, [#515](https://github.com/rism-digital/verovio/issues/515)의 stretch 문제는 원전만으로 보장할 수 없는 반례 후보.

**원전**: [Knuth & Plass 1981](https://gwern.net/doc/design/typography/tex/1981-knuth.pdf) — 문단 전체 분할 비용을 결정하려면 함께 제공; **수신 프로젝트가 당시 채택했다는 주장 금지**.

**사용자에게 묻기**: '사진의 원래 크기·마지막 줄 높이와 악보의 수동 넘김 중 무엇이 반드시 유지되어야 하나요?' 해당 질문이 필요 없는 구체적인 버그라면 곧바로 구현 절을 반환한다.
