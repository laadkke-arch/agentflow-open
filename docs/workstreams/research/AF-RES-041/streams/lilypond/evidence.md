# B03 LilyPond 수신 기록 · 묶음② 중간 기록

상태: 조사 중. 최종 판정은 root가 원전 판본 조사와 결합한 뒤 한다. 역사 프로그램 실행은 하지 않았다.

## 새로 닫힌 기준선과 남은 접점

1997-08-01의 [0.1 발표](https://lilypond.org/misc/ANNOUNCE-0.1) L78–84는 MusiXTeX T.73 fonts가 필요하다고 명시한다. [0.1.0 tar](https://lilypond.org/download/sources/v0.1/lilypond-0.1.0.tar.gz)의 `tex/taupindefs.tex` L11/29는 musix20/musix16을 쓰므로 초기 배포의 기존 글꼴을 직접 특정했다. 이것은 최초 미공개 원안은 아니다.

[1.0.1 tar](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)의 ANNOUNCEMENT L14–20은 기존 글꼴 불만과 새 Feta 제작을 연결하고 L39는 MusiXTeX 불필요를 말한다. 같은 배포의 fonts.doc L11–23은 선호 출판사 악보 모방과 원본 MetaFont 소스라는 저자 설명을 담는다. sharp와 natural은 Schubert/Bärenreiter, double-sharp와 flat은 Müller/Hofmeister로 귀속한다. 판번호·페이지·독서일은 없다.

## 가장 유용한 새로운 전후: flat의 본보기 교체

[0.1.19](https://lilypond.org/download/sources/v0.1/lilypond-0.1.19.tar.gz) `mf/toevallig.mf` L2–5는 flat을 Schubert에 귀속한다. [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz) `mf/feta-toevallig.mf` L2–5까지 그 귀속이 유지된다. [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) 같은 파일 L2–5는 flat을 Müller에 옮긴다. 동시에 0.1.19 L116–164의 brush/penstroke 함수는 0.1.23 L114–205의 serif·fill/unfill 함수로 바뀌었다. 부호 의미는 flat으로 유지되고 폭·곡선·줄기/배의 두께 구성은 달라진다.

이는 동일 기호의 구체적인 before/after다. 그러나 귀속 수정이 실제 독서 후 변경의 완전한 진술은 아니며, 정확한 원판 모양과 코드 형상을 대조하기 전 엄격 인과 양성으로 올리지 않는다. 0.1.22→0.1.23의 함수 차이 전체와 공개시점 상한은 다음 묶음에서 더 확인한다.

## 일부러 따르지 않은 특징

1.0.1 `mf/feta-toevallig.mf` L25–27은 많은 sharp의 가로 획 끝이 수평임을 알면서 Wanske가 언급하지 않으므로 그 특징을 무시한다고 적는다. 외부 본보기의 관찰은 실제 선택을 강제하지 않았다. 0.1.19 L37의 sharp slope에 쓰던 beamheight/2가 0.1.23 L37–39의 Wanske 주석과 beamheight로 바뀌는 별도 기호 수정도 있다. 두 변경을 하나의 최초 악보 독서 사건으로 합치지 않는다.

## 날짜와 단계

0.1.0은 MusiXTeX. 0.1.13은 dynamics의 자체 MF, 0.1.15는 자체 noteheads와 기존 MusiXTeX accidentals의 공존, 0.1.19는 named-score accidentals source, 0.1.23은 flat 본보기 귀속·정의 변경, 0.1.27은 feta라는 폰트명이다. 그러므로 0.1 전체를 변경 전으로, 1.0을 첫 Feta 구현으로 쓰면 틀린다.

위 tar member mtime는 파일 작성/보존 날짜다. index의 last-modified와 최초 공개일·사용자의 입수·저자의 독서는 각각 다르다. 원장에는 구분하여 기록했다.

## 저작 수와 재배포

현재 직접 기록17행, counted4: 0.1.0 배포,1.0.1 배포,2003 저자논문,2006 저자발표다. 경계 검사용0.1.12–27은 직접 읽었어도 최소수에서는 추가하지 않았다.0.1.0/1.0.1을 한 진화 저작으로 묶으면 보수계통3개다. 2003/2006은 별도 저작이나 동일 저자의 회고이며 독립 증언 수를 늘리지 않는다. 원장·노트는 아직 후속 자료를 추가할 예정이다.
