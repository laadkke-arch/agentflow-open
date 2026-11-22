# 묶음③ · 같은 기능의 반영과 반례

## 확인된 조작

B01의 보존 [0.14f 소스](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz) `pdftex.ch` L5108–5129는 돌출과 폭 확장을 각각 조건문으로 나누고 후보줄의 shortfall 계산에 넣는다. L5460–5469는 정한 줄의 실제 packing을 다룬다. [2000 논문](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) pp69–70의 level1/level2 설명과 맞는다. 1998 저장 도판의 줄끝 보존과 2004 도판의 줄끝 변화는 각 논문 안의 같은 입력 짝에서 읽었으며, 서로 다른 두 논문의 출력물을 통제된 전후 실험처럼 합치지 않았다.

B03의 [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz)와 [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) `mf/feta-toevallig.mf`를 직접 대조했다. 같은 flat 의미·호출을 유지하며 본보기 귀속, 함수, 폭, 곡선 두께가 함께 바뀌었다. 그보다 이른 sharp 기울기 변경과 나중 optical spacing은 다른 행이다. [Debian 1997-10-20 기록](https://lists.debian.org/debian-changes/1997/10/msg00023.html)은 두 버전이 늦어도 그때 공개 유통됐음을 확인한다.

## 강한 설명에 반하는 관측

| 가정 | 반하는 원문·관측 | 판정에 주는 제한 |
| --- | --- | --- |
| hz 알고리즘을 pdfTeX에 이식했다 | Thành2000 p38은 구현 정보가 없었다고 말한다. Karow1997 p54의 Ek는 흰 내부공간을 조절하며 획을 보존한다. | 개념적 영감과 알고리즘 이식은 구별해야 한다. |
| 1996 원안은 자폭 활용을 배제했다 | [1996 원문](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf) p248 §7은 이미 폭 축을 문단 줄바꿈에 넣는 방향을 제안한다. | 원전 독서 전 대안과 독서 후 최초 계획 변경은 별도 증거가 필요하다. |
| Feta는 본보기의 모든 특징을 따랐다 | [1.0.1 소스](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) `feta-toevallig.mf` L25–27은 sharp 획 끝의 관찰 특징을 의도적으로 무시한다. | 선택적 모방은 직접 지지되나 그 특징을 특정 Schubert 인쇄본의 특정 기호로 고정하는 일은 미확인이다. |
| 한 출판사의 현재 기호 규칙은 과거판에도 같다 | [BA5635 서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf)는 편집 추가 임시표를 작은 활자로, [NSA2022 p14](https://schubert-ausgabe.de/download/nga_editionsrichtlinien_7-_fassung_final.pdf)는 정상 크기 대괄호로 구분한다. | 판·쇄·편집 층을 확인하지 않으면 의미가 바뀔 수 있다. |
| 보기 좋은 기호를 바꾸면 실제 출력도 보장된다 | [Fok의 README](https://sources.debian.org/src/lilypond/2.24.1-2/debian/README.Debian/) file L18–46의 fontmap·tfm/pk 문제, [Bravura 설계자](https://blog.dorico.com/2013/05/introducing-bravura-music-font/)의 매핑 호환성 설명 | 코드 존재, 저장 도판, 설치된 프로그램 출력은 다른 확인 단위다. |

직접 읽은 원저작·기관 기록을 단일 범주로 합치면 29저작이다. 42개 탐색 경로, 36개 시간 사건, 18개 조작 비교를 통합 CSV에 남겼다. 이는 새 표본 사건의 추가가 아니다. 외부 비교는 고정된 B01·B03 두 사건을 반증하는 용도로만 사용했다.

CSV는 Artifact Tool의 텍스트 셀을 통해 작성했다. 날짜 문자열의 정밀도를 보존하도록 text format을 먼저 지정했고, Python csv로 원자료 행과 완전 일치를 확인했다. Artifact Tool의 CSV 재입력은 ISO 시각을 Date로 정규화하므로 그 변환 횟수를 별도 기록했다. 이는 연구의 인과를 검증하는 테스트가 아니라 행·구분자·원문 시각 보존 점검이다.
