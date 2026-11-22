# 묶음② · 원전 식별과 변경 전 상태

현재 확인 범위를 봉인한 중간 기록이다. 정확판 조사와 후속 반영 검사는 묶음③에서 계속한다. 조사 순서가 결말 비노출 시험이라는 주장은 하지 않는다. 최초안/코드의 정의는 SCOPE v1을 유지한다.

## B01 제공 저작의 서지

[Thành2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) 논문 pp117–118, 참고문헌40–43에서 직접 확인했다. 40·43만1993 hz 문헌이며41·42는 다른 저작이다.

| 번호 | 저자·서명·발행 | 직접 확인한 판·범위 | 남은 공백 |
| --- | --- | --- | --- |
| 40 | URW. *hz-program: Micro-typography for advanced typesetting*. URW Software Hamburg,1993 | [Karow1997 공식 번역](https://www.numdam.org/item/CG_1997___27_34_0.pdf) p34 각주가1993 내부발행 영문책자·저자허락 번역·원본 그림400dpi 스캔을 연결 | 영문책자 전체·개별 판차·pdfTeX 저자의 최초 독서 날짜는 미확인 |
| 41 | Adolf Wild. *La typographie de la bible de gutenberg*. Cahiers Gutenberg,1995 | [원논문](https://www.numdam.org/article/CG_1995___22_5_0.pdf) §2 pp12–14 | Gutenberg 활자 변형을 현대의 균일 폭스케일과 동일시할 수 없음 |
| 42 | Ian H. Witten. *Elements of computer typography*. International Journal of Man-Machine Studies23(6):623–687,1985 | Thành 참고문헌의 서지 전사 | 이 저작 자체의 본문은 미확인; 최소수에 넣지 않음 |
| 43 | Hermann Zapf. *About micro-typography and the hz-program*. Electronic Publishing—Origination,Dissemination,and Design6(3):283–288,September1993 | [dblp](https://dblp.dagstuhl.de/db/journals/epodd/epodd6.html)의 `journals/epodd/Zapf93`, [Utah](https://ftp.math.utah.edu/pub/tex/bib/epodd.html)의 동일 서지 교차 확인 | 원 발행본 본문 직접 접근은 현 단계 미확인; catalog만으로 본문 열람 처리하지 않음 |

## 동일 사건에 서로 다른 기준선

| 판독 | 확인한 변경 전 상태 | 가장 이른 확인 기록의 성격 | 후속 비교 대상 | 현재 닫히지 않은 접점 |
| --- | --- | --- | --- | --- |
| B01-I | Multiple Master font의 width 축·일정 grayness를 줄맞춤에 쓰는 방향이 이미 제안돼 있음 | [1996 저자논문](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf) §7 p248. 최초 남은 제안이며 모든 미공개 원안의 최초는 아님 | 1998 후처리 실험 및2000/2001 줄바꿈 통합 | hz를 읽기 전 다른 원안을 유지했다가 바꿨다는 같은 저자의 날짜 있는 연결 |
| B01-C | 1998 설명은 줄바꿈 완료 뒤 hbox를 골라 PDF text matrix로 가로 조정 | [1998 저자논문](https://tug.org/TUGboat/tb19-3/tb60than.pdf) p288. 구현 보고·저장 실험 예시, 실제 엔진 소스 열람과 구별 | [2001 운용 원문](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf) pp146–148의 줄바꿈 유지/관여 모드 | 정확한 초기·후속 배포 소스와 hz 독서→그 코드 변경의 연결 |
| B03-I | 초기 목표와 MusiXTeX 사용은 공개 기록에 있음. Feta 이전 미공개 형태 원안은 없음 | [1997-08-01 발표](https://lilypond.org/website/misc/ANNOUNCE-0.1)와0.1.0 배포 | 1.0 발표의 기존 글꼴 불만·Feta 설명 | 특정 악보판의 독서가 같은 최초 형태 선택을 바꿨는지 미확인 |
| B03-C | [0.1.0](https://lilypond.org/download/sources/v0.1/lilypond-0.1.0.tar.gz)의 musix20/musix16. 좁은 flat 비교는 [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz)의 Schubert 귀속·정의 | 실제 고정 배포 소스. 글꼴 전체와 특정 기호의 기준선을 두 부행으로 구별 | [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz)의 Müller flat 귀속·코드 재작성,1.0.1 반영 | 본보기의 정확한 판·쪽과 해당 글리프 직접 대조, 실제 독서 순서 |

## 성급한 교정 금지

- 최초 제안의 발견 시점은 이번 조사 순서이며 당시 저자의 처음 생각한 날짜가 아니다.
- 0.1 계열 전체를 ‘MusiXTeX만’이라고 부르지 않는다. dynamics·noteheads·accidentals가 단계적으로 바뀌었다.
- 판별표의 미확인을 채우려고 후대 자료를 당시 판으로 대체하지 않는다.
- 코드 기준선에서 변화가 발견됐다는 이유로 최초안 기준의 필요조건을 바꾸지 않는다.
