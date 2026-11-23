# 반환 카드

- **문서 전체 두 겉선 제거.** Quarto 1.4.553에서 무인수/두 인수 빈 재정의가 모두 두 표에 적용됐다. 대조 내부선과 셀은 유지되고 간격은 줄었다. [D-Z-1](evidence/matrix/D-Z-1/) · [D-T-1](evidence/matrix/D-T-1/) · [P-HEADER-T](evidence/probes/P-HEADER-T/)
- **한 표에만 적용.** 첫 표를 TeX 그룹으로 감싼 두 Qmd는 두 번째 표의 3선과 셀을 보존했다. [P-LOCAL-Z](evidence/probes/P-LOCAL-Z/) · [P-LOCAL-T](evidence/probes/P-LOCAL-T/)
- **writer에서 확인할 것.** 빈 헤더의 top/bottom, 실헤더의 midrule을 생성하는 위치를 찾는다. 생성 호출과 최종 PDF를 함께 설명하려면 실제 로드·정의도 확인한다. [D-O-1](evidence/matrix/D-O-1/) · [D-T-1](evidence/matrix/D-T-1/)
- **raw tabular 경계를 점검.** 두 필수 인수는 다음 두 토큰을 받는다. 실제 noalign 빈 그룹에서 동률이고 Stable의 앞 글자나 다음 종료 명령이 오는 예에서 결과가 달라졌다. [P-TRACE-T](evidence/probes/P-TRACE-T/) · [P-TABULAR-T](evidence/probes/P-TABULAR-T/) · [P-BARE-BOTTOM-T](evidence/probes/P-BARE-BOTTOM-T/)
