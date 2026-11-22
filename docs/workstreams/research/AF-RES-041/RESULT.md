# AF-RES-041 · 인쇄·악보 원전과 설계 변경

| 사건·기준선 | 변경 전 선택·시점 | 특정 원전·판·쪽 URL | 저자의 연결 발언 URL·날짜 | 달라진 선택·동일 목적 반영 URL | 사슬 판정 | 미확인 접점 |
| --- | --- | --- | --- | --- | --- | --- |
| B01 pdfTeX · 최초안 | [1996 저자 논문](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf) p248 §7에 이미 Multiple Master 폭 축을 문단 줄바꿈에 쓰자는 제안이 있다. 이번에 찾은 최초 남은 제안이며, 원전 노출 전 원안은 **미확인**. | URW, *hz-program: Micro-typography for advanced typesetting*, Hamburg1993. [공인 프랑스어 번역](https://www.numdam.org/item/CG_1997___27_34_0.pdf) p34 각주·pp49,54,56–57을 직접 읽음. Zapf1993 EPODD6(3)283–288은 [기관 서지](https://dblp.dagstuhl.de/db/journals/epodd/epodd6.html) 확인, 영어 원판 본문은 **미확인**. | [Thành2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) §4 p38/저널354: hz 출판물이 영감을 줬으나 구현 정보는 없어 독자 개발했다고 회고. 최초 독서일은 **미확인**. | 같은 논문 §§6.5.1–2 pp69–71 및 [2001 설명](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf) pp146–148에서 폭 확장의 줄바꿈 유지/관여 모드를 구별. 기능 존재는 확인되지만 1996 제안의 방향이 독서 뒤 바뀌었다는 증거는 **미확인**. | 인용과 같은 기능 반영까지. **같은 최초 결정의 인과 확인 아님**. | 정확 영어 제공판 대조, 첫 독서의 위치, 독서 전 다른 최초 선택, 그 선택을 바꾼 연결. |
| B01 pdfTeX · 기존 코드 | 보존 [0.12h](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.2-pdftex-0.12h.tar.gz) `pdftex.ch` L86–190,4554–4601의 primitive·줄바꿈 변경부. 보존목록 mtime1998-03-27; 최초 배포일은 **미확인**. [1998 구현 보고](https://tug.org/TUGboat/tb19-3/tb60than.pdf) p288은 줄을 정한 뒤 PDF text matrix로 조정. | 같은 URW1993 계통의 [1997 번역](https://www.numdam.org/item/CG_1997___27_34_0.pdf) pp49,54,56–57. 번역·도판의 원본 관계는 확인, 최초 제공 영어판은 **미확인**. | [2000 회고](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) p38. 같은 저자의 반복 설명을 독립 증언으로 세지 않음. 특정 코드 변경을 특정 독서에 직접 연결한 당대 기록은 **미확인**. | [0.14f](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz) `pdftex.ch` L5108–5129는 폭·돌출을 후보줄 평가에, L5460–5469는 실제 줄 조정에 넣음. 내부 라벨2000-05-25. [2000 pp69–71](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)의 설명과 대응. | **같은 기능 반영까지**. 기준선을 코드로 옮겨도 엄격 완결은 아님. | 정확 제공판·독서→이 코드 변경의 인과. 보존 archive의 당시 배포본과 바이트 동일성 및 첫 공개일도 **미확인**. |
| B03 LilyPond · 최초안 | [0.0.1 보존 코드](https://lilypond.org/download/sources/v0.0/lilypond-0.0.1.tar.gz) `lilyponddefs.tex` L3–10은 musix20. 파일 mtime1996-10-06. [1997-08-01 발표](https://lilypond.org/website/misc/ANNOUNCE-0.1) L78–84도 MusiXTeX T.73을 요구. 최초 미공개 원안은 **미확인**. | Schubert/Bärenreiter의 후보는 BA5635 및 NSA IV/14b BA5527. [서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf)는 Dürr·©1988·3쇄2008, [ÖAW](https://schubert-digital.acdh-dev.oeaw.ac.at/W-01032.html)는 BA5527 IV/14b 전집의 pp196–218. Müller/Hofmeister는 현행 [FH6064](https://www.hofmeister-musikverlag.com/produkt/etueden-op-64/)/[FH6065](https://www.hofmeister-musikverlag.com/produkt/etueden-op-64-heft-2-12-etueden-fuer-ventilhorn/) 후보. 저자 사용판·쪽은 **미확인**. | [1.0.1 소스](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) `fonts.doc` L11–23, `feta-toevallig.mf` L11–27, ANNOUNCEMENT L14–20: 선호 악보·기호를 명명하고 기존 글꼴 불만과 Feta 제작을 설명. 1998 계열 보존본이며 최초 독서일은 **미확인**. | 같은 배포의 `tex/fetdefs.tex` L8–25 및 accidental 정의로 새 글꼴의 같은 기보 목적을 확인. [2003 저자 논문](https://lilypond.gitlab.io/static-files/media/xivcim.pdf) p4 Fig5는 후대 저장 도판. 최초 원안 변경이나 1997 실제 출력으로 소급하지 않음. | 인용과 같은 기능 반영까지. **같은 최초 결정의 인과 확인 아님**. | 정확 악보판·쪽·독서일, 동일 최초안의 형태 선택과 변경 연결. |
| B03 LilyPond · 기존 코드 | [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz) `mf/feta-toevallig.mf` L2–5,119–167: 이미 Schubert를 본보기로 적은 자작 flat. 최초 원안과 다른 보조 기준선. | 위 Schubert/Müller 후보판. [공식 Müller 샘플](https://www.hofmeister-musikverlag.com/wp-content/uploads/2023/07/FH_6064_NS.png)은 실제 기호를 보여주지만 1997 저자 사용판과 동일한지는 **미확인**. | [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) 같은 파일 L2–5에서 flat의 귀속이 Müller로 바뀜. [1997-10-20 Debian 기록](https://lists.debian.org/debian-changes/1997/10/msg00023.html) HTML L564–573이 공개 가용성의 상한. 독서 후 변경이라는 명시 문장은 **미확인**. | 같은 파일 L114–205: brush/penstroke에서 serif·fill/unfill로 재작성. flat의 오른쪽 extent w#는9/12→.8 interline#, 왼쪽 extent b#는0→1.2 stafflinethickness#. crook_fatness 매개변수는1/4→1/3 interline. 출력 잉크폭 실측은 아님. `Flat/-1/flat` 의미·호출 유지. 1.0.1에도 같은 기능이 남음. | **같은 기능 반영까지**. 동일 기호의 변경은 참, 정확 원전의 인과 완결은 아님. | 정확 제공판·해당 flat·당시 가용성·독서와 수정 이유. double-flat의 코드 변화는 확인되지만 같은 원전의 직접 모방이나 후기 spacing까지 확대하는 인과는 **미확인**. |

| 사건·독자에게 줄 용도 | 원전 조작과 구현 조작 | 찬성 근거 URL·위치 | 반대 근거 URL·위치 | 깨지는 조건 | 반환 카드와 근거 강도 |
| --- | --- | --- | --- | --- | --- |
| B01 · 문단 정렬에서 글자 폭의 작은 여유를 후보줄 평가에 넣는 설계 | hz의 광학 여백, 선택적 자폭 조절, 문단 조판은 구별되는 조작. pdfTeX는 글자 ID를 유지하고 폭 변형 font·확장 허용량을 후보줄 평가와 줄 packing에 반영. | [Karow1997](https://www.numdam.org/item/CG_1997___27_34_0.pdf) pp49,54,56–57; [Thành2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) p38,pp69–71; [0.14f](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz) L5108–5129. | 같은 Karow p38은 새 합자 연구 유보, p54는 흰 내부공간 조절·획 두께 보존. Thành p38은 hz 구현 정보 부재. [1996 p248](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf)은 이미 자폭 활용 방향을 제안. | 획 두께·문자 비율 보존이 필요한데 균일 가로 확대를 동일시할 때. 합자를 입력문자 치환으로 처리할 때. 줄바꿈을 고정해야 하는데 level2를 적용할 때. | [카드 B01](cards.md#b01). 명시적 영감+같은 기능 반영. ‘hz 알고리즘 이식’ 또는 ‘독서 뒤 최초 계획을 전환’은 반환하지 않음. |
| B03 · 기호 의미를 유지하며 획·폭·곡선 변수를 본보기에서 선택하는 설계 | 인쇄본 accidental의 형상 관찰과 Metafont의 변수·윤곽 함수 재설계를 대응. flat은 같은 의미를 유지하면서 본보기 귀속과 형상이 함께 변경. 정확 원판과의 수치 일치는 **미확인**. | [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz) L2–5,119–167 → [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) L2–5,114–205; [2003 도판](https://lilypond.gitlab.io/static-files/media/xivcim.pdf) p4 Fig5. | [1.0.1](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) L25–27의 sharp 획 끝 미채택. [BA5635 서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf)와 [NSA2022 p14](https://schubert-ausgabe.de/download/nga_editionsrichtlinien_7-_fassung_final.pdf)의 편집 추가 임시표 규칙 차이. | 현대 견본을 당시 판으로 대신할 때, 한 기호에서 글꼴 전체로 확대할 때, 편집 추가 표시의 의미·장르·크기·매핑을 무시할 때. | [카드 B03](cards.md#b03). 당대 출처 명명+동일 기호의 코드 변경·반영. 정확 특정 판 복제나 최초안 변경 인과는 보류. |

## 결론의 단위와 수

**엄격 최초안 기준의 완결은 0/2건, 기존 코드로 기준을 이동한 뒤에도 같은 다섯 접점을 요구하면 0/2건이다.** 코드에서 같은 기능의 변화와 반영을 확인한 수는 별도로 **2/2건**이다. 영감·출처 명명과 대응 기능을 함께 제시하는 두 카드는 가능하지만, 두 사건 모두 ‘그 원전을 읽고 동일 최초 계획의 어느 선택을 바꿨는가’까지 닫히지 않았다. 이 2건은 037의 빈 고리를 보강하려고 고른 사례이므로 일반 채택률을 추정하지 않는다.

| 기준·민감도 | 분자/분모 | 무엇을 센 것인가 | 해석 |
| --- | --- | --- | --- |
| SCOPE v1 최초안, 다섯 접점 모두 참 | 0/2 | 같은 최초 결정의 완결 인과 | 037의 최초안 기준을 유지. 미확인은 거짓이 아님. |
| 동일 다섯 접점, 기존 코드로 기준 이동 | 0/2 | 정확 제공 원전에서 그 코드 변경까지의 완결 | 변화 자체를 인과 완결로 승격하지 않음. |
| 출처 명명+같은 기능 반영, 회고의 지위 표시 | 2/2 | B01의 폭 확장, B03의 flat 변경이라는 좁은 기능 증거 | 카드 강도의 상한. 위 두 분자와 다른 확인 단위. |
| 정확 판 대신 출판사·저작 계열만 허용 | 완결 0/2 | 넓은 계열 일치의 민감도 | 판 조건을 완화해도 최초 독서·같은 최초안 변경 연결이 남음. |
| 정확 저자 사용판의 동일 glyph/규칙을 직접 짝지어 계측 | 0/0; 비율 **해당 없음** | 적격 원판–구현 쌍 | 후보 이미지를 정확 사용판으로 오인하지 않으므로 계측 성공률을 만들 수 없음. |

`judgments.csv`에는 4행×5접점의 상태와 각 근거를 적었다. 저자의 포괄적 출처 명명은 참이지만 **엄격 author_link**는 ‘정확 자료의 규칙을 보고 같은 기준선의 선택을 바꿨다’는 연결이어서 미확인이다. 이를 한 칸으로 압축해 인용 자체까지 부정하지 않도록 `author_citation`과 `author_link`를 분리했다.

## Q1 · 어느 원전이며 어느 판을 읽었는가

Thành 논문 pp117–118의 참고문헌40–43은 모두 hz1993 문헌이 아니다. 40은 URW1993 내부 책자, 43은 Hermann Zapf의 EPODD6(3), pp283–288, September1993 논문이다. 41은 Adolf Wild1995의 Gutenberg 연구, 42는 Ian H. Witten1985의 *Elements of computer typography*, IJMMS23(6):623–687이다. 전사는 [묶음② 서지표](evidence/edition-baseline-register.md)에 남겼다. Witten의 본문은 읽지 않았으며 최소수에 넣지 않았다. [Thành 원문](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)

URW 책자와 [Karow1997](https://www.numdam.org/item/CG_1997___27_34_0.pdf)의 관계는 p34 각주로 좁혔다. 저자 허락을 받은 영어→프랑스어 번역이고 그림은 원문에서 스캔했다. 번역자의 `[NDT]` 주석과 1997 본문 조판은 원판과 구분해야 한다. 번역문 자체가 hz 실행 출력이라는 뜻도 아니다. URW 영어 책자 전체는 원본 URL·본문을 확보하지 못해 미열람이고, Zapf 원논문은 확인한 두 URL의 본문 접근에 실패했다. Nottingham 옛 저널 서버, NTNU 소장 주소, dblp·Utah 서지 및 실패 경로를 원장에 남겼다. ‘영어 원판 직접 열람’은 **미확인**이다. 또한 [Karow2015 p97 참고문헌5](https://tug.org/TUGboat/tb36-2/tb113zapf-karow.pdf)는 hz 책자를1992로 적는 반면, [Google Books의 서지](https://books.google.ca/books/about/Hz_program.html?id=Ox4jywAACAAJ&redir_esc=y)는 URW Software & Type,1993,38쪽으로 기록한다. 후대 서지의 연도 오기 또는 다른 판일 가능성은 열려 있으며, 원본 표제·간기 없이 같은 판의 첫 발행연도를 고쳐 쓰지 않는다. 수신 논문의 참고문헌40이1993이라고 적은 사실은 그대로 유지한다.

Schubert의 후보는 출판사 서문과 기관 기록을 통해 Bärenreiter의 1988 Dürr 판 계열까지 좁혔다. 그러나 [공식 미리보기](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf)는 2008 3쇄이며 음악 본문은 없다. [CiNii](https://ci.nii.ac.jp/ncid/BA27399877?l=ja)는 c1988, Dürr, 24쪽 score와 파트를 확인하지만 추출 레코드에 BA번호가 없다. [ÖAW](https://schubert-digital.acdh-dev.oeaw.ac.at/W-01032.html)의 NSA IV/14b pp196–218은 정확한 다음 열람 위치를 준다. 목록상 존재는 저자의 독서를 입증하지 않는다.

Müller의 ‘Etüden für Horn’은 현행 Hofmeister [FH6064 첫 연습곡](https://www.hofmeister-musikverlag.com/wp-content/uploads/2023/07/FH_6064_NS.png)과 [FH6065 첫 연습곡](https://www.hofmeister-musikverlag.com/wp-content/uploads/2023/07/FH_6065_NS.png)을 직접 보았다. 두 권의 제목·편집 표기는 다르며, source comment에 opus·권·판·쪽이 없어 하나를 저자 사용본으로 확정할 수 없다. 2023이라는 URL 경로도 인쇄연도가 아니다. 두 권은 op64 한 저작으로만 세었다.

추가로 읽은 [BA5635 판매자 연결 발췌](https://cdn.nimq.de/data/file/mgsloib/000/027/076/0000270762.pdf)는 마디127–135의 raster 한 쪽이다. m128 성악의 sharp, m129 피아노의 natural, m131 호른의 flat, m132 호른의 natural·sharp를 식별했다. 940×1226 JPEG임은 확인했지만 원인쇄 스캔인지 후대 재조판의 raster인지는 **미확인**이다. 내부 판번호·쪽·간기가 없으므로 최소수에서 제외하고 비교 보강으로만 쓴다. 원본 이미지는 재게시하지 않았다.

## Q2–Q3 · 변경 전 상태와 독서 연결

B01에서 새로 중요한 기록은 [1996 논문 p248](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf)이다. 그때 이미 문단 줄바꿈과 폭 축의 결합을 제안했다. ‘hz를 읽기 전에는 자폭을 전혀 활용하지 않기로 했다’는 원안을 만들어 넣으면 자료와 맞지 않는다. 반대로 hz 첫 독서가 1996보다 앞섰을 수도 있으므로, 이 제안의 존재가 hz 영감 진술을 반박하는 것도 아니다. 확인된 것은 최초 남은 제안의 내용이고, 최초 노출의 시점은 **미확인**이다.

1998 실험은 줄바꿈 후의 조정이고 2000 설명은 후보줄 평가까지 포함한다. [2000 p70](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)은 level1의 한계와 level2로 통합하는 기술적 이유를 말한다. 이것은 구현 단계의 전진을 설명하지만, 1996의 넓은 설계 방향이 외부 독서 때문에 반전됐음을 증명하지 않는다. PDF 출력 동기에 관한 Knuth 메모 언급과 microtype 결정의 동기는 다른 행으로 유지했다.

B03의 교체는 단계적이다. 0.1.13의 dynamics, 0.1.15의 noteheads, 0.1.19의 named-score accidentals, 0.1.23의 flat 재작성, 0.1.27의 Feta 이름을 하나의 날짜로 합치지 않는다. [0.1 변경 기록](https://lilypond.org/website/misc/CHANGES-0.1)과 각각의 배포 소스를 함께 읽었다. 전체 0.1 계열을 변경 전이라고 하거나 1.0을 첫 Feta 구현이라고 부르면 틀린다.

flat의 변경은 두 배포 사이에서 출처 귀속과 도형 정의의 변경이 함께 관측되는 강한 단서다. 이는 같은 버전 경계라는 뜻이며 실제 편집 시각의 동시성을 뜻하지 않는다. 그러나 ‘Schubert에서 Müller로 귀속을 고쳤다’는 관측과 ‘새 Müller 판을 읽은 결과 원래 flat 설계를 바꿨다’는 인과 진술은 다르다. sharp의 Wanske 기울기 주석은 0.1.19→0.1.20에 이미 있으며 flat의 0.1.22→0.1.23보다 이르다. 이 둘을 같은 독서 사건으로 묶지 않았다.

## Q4–Q5 · 같은 조작, 같은 목적, 실제 반영의 범위

| 조작 | 보존하는 값 | 바꾸는 값과 대응 | 직접 확인한 범위 | 적용이 깨지는 조건 |
| --- | --- | --- | --- | --- |
| 광학 여백 | 문자 정체성·문단 내용 | hz의 가상 흰 경계와 자동 kerning; pdfTeX의 글꼴·문자별 돌출량 및 후보줄 반영 | [Karow p49](https://www.numdam.org/item/CG_1997___27_34_0.pdf), [pdfTeX2001 p146](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf), 0.14f 코드 | 외곽선 계산과 수동 계수 설정을 같은 알고리즘으로 부를 때. |
| 자폭과 문단 조판 | 입력 글자 순서·줄맞춤 목적 | hz Ek의 선택적 폭 조절; pdfTeX의 font 변형·stretch/shrink·badness 평가 | Karow pp54,56–57; Thành2000 pp69–71; 0.14f L5108–5129 | 균일 스케일로도 획 두께·내부 공간이 같은 방식으로 보존된다고 가정할 때. |
| 합자·대체 glyph | 의미·읽기 관습은 별도 제약 | Gutenberg의 수단, hz가 보류한 새 합자, pdfTeX의 자폭 확장을 분리 | [Wild1995 pp12–14](https://www.numdam.org/article/CG_1995___22_5_0.pdf), [André1995 p75](https://www.numdam.org/article/CG_1995___22_61_0.pdf), Karow p38 | 입력문자를 합자 문자로 치환해 철자검사·분철까지 보존한다고 가정할 때. |
| flat 형상 | `Flat/-1/flat`의 기보 의미·높이/깊이 | 함수·serif·좌우 extent와 crook_fatness 매개변수 | 0.1.22 L119–167 ↔0.1.23 L114–205; 후대 [2003 Fig5](https://lilypond.gitlab.io/static-files/media/xivcim.pdf) | 작은 현대 샘플의 비율을 1997 donor 수치로 삼거나 모든 accidental에 확장할 때. |
| 악보 편집·배치 | 음높이·시간·편집 출처의 의미 | 임시표 크기/대괄호, 간격, 오선 크기, 페이지 넘김 | [MPA pp6,12](https://mpa.org/wp-content/uploads/2018/06/standard-practice-engraving.pdf), [MOLA2017 pp5–6](https://mola-inc.s3.eu-west-1.amazonaws.com/files/mola3/MOLA-Guidelines-for-Music-Preparation.pdf), NSA2022 p14 | glyph 형상만 보고 연주자의 판독성·편집 의미·실제 출력 조건까지 보장할 때. |

반영 증거는 네 종류로 구분했다. 첫째, **작성 소스 직접 관측**은 0.14f와 LilyPond 배포의 해당 함수다. 둘째, **저자의 출력 보고**는 1998/2000/2001 설명이다. 셋째, **저장 출력 직접 판독**은 1998 Fig1, [2004 Fig2 p37](https://tug.org/TUGboat/tb25-1/thanh.pdf), LilyPond2003 Fig5와 [2006 slide9·16](https://lilypond.gitlab.io/static-files/media/FISL7-slides.pdf)이다. 넷째, **이번 역사 프로그램 재실행은 하지 않았다**. 서로 다른 논문 사이의 입력·글꼴·설정이 같다고 가정하지 않았고, 후대 출력물을 1997 바이너리의 출력으로 소급하지 않았다.

pdfTeX 보존 archive의 출처에도 한계가 있다. [Vieth2007 slide11](https://tug.org/~vieth/papers/bachotex2007/tex-history-talk.pdf)은 해당 구버전 계열 일부를 web2c에서 재구성했고 일부를 미러했다고 설명한다. 내부 버전·정적 코드·논문 대응은 관측할 수 있지만, 확보한 archive가 당시 배포 tarball과 바이트까지 같다는 인증으로 쓰지 않았다. 첫 구현 릴리스가 정확히 어느 버전인지도 **미확인**이다.

## Q6 · 경쟁 설명을 반증한 결과

| 경쟁 설명 | B01에 맞는 부분과 한계 | B03에 맞는 부분과 한계 |
| --- | --- | --- |
| 독자 구현 | Thành2000 p38이 직접 지지한다. 구현 정보 부재는 알고리즘 이식을 약화하지만, 같은 문장의 hz 영감까지 지우지 않는다. | 자작 MF 소스와 함수 재작성은 지지한다. 작품·출판사 명명은 형상 영감과 양립한다. dynamics의 cmbxti10 이력까지 포함해 모든 파일이 무차용이라고 확대하지 않는다. |
| 이미 정한 방향의 정당화 | 1996 제안이 넓은 방향의 선행 존재를 보여준다. 그러나 첫 hz 독서일이 없어 ‘나중에 정당화했다’는 순서 자체는 **미확인**이다. | 1998·2003·2006 설명은 초기 코드보다 뒤지만, 1997 당대 소스에도 출처 명명이 있어 전적으로 후대에 만든 설명이라는 주장은 약하다. |
| 선택적 모방 | hz 자체가 새 합자를 유보했고, pdfTeX와 원전의 형상 보존 방식도 다르다. 같은 목적을 기능별로 골라 구현했다는 설명과 맞는다. | 기호별로 출판사를 나누고 sharp 가로 획 끝의 수평성을 의식적으로 무시한다. 미채택 특징 자체는 명시돼 있으나 그 특징을 관찰한 정확 악보판·쪽과 Wanske 원책의 언급 부재는 **미확인**이다. |
| 후대 회고 | 명시적 영감 연결은 2000 p38 한 계통이다. 기능의 존재는 코드·설명·도판으로 따로 확인된다. | 저자 회고만 있는 사건은 아니다. 1997 주석·버전 변화·Debian 수신 기록이 당대 관측을 제공한다. 그래도 실제 독서→최초안 변경은 닫히지 않는다. |

조판자의 관점에서는 글자 폭만 늘리는 것보다 흰 공간·획·문단·페이지의 상호작용이 중요하다. [Mittelbach·Rowley pp51–54](https://www.ntg.nl/maps/09/14.pdf)는 문단과 페이지 조정의 범위 충돌을 직접 논한다. [Eng의 비평](https://www.typografi.org/justering/gut_hz/gutenberg_hz_english.html)은 Gutenberg의 형태 변형과 현대 자폭 조절을 등치하는 설명을 반박한다. Eng의 미감 판단을 통제된 가독성 실험으로 사용하지 않았다.

악보 판각자·연주자의 관점에서는 한 glyph가 아름다운지와 실제 악보를 읽기 쉬운지가 다르다. [Gould 공식 발췌 pp19,315](https://faber-product-media.s3.amazonaws.com/40c555eb-aa0f-4e02-a7a1-0ec0223f98e4)는 충돌 회피와 읽기 흐름에 따라 beam·줄기 관계를 조절한다. MPA는 임시표에 시간값이 없으므로 기호 폭이 시간 간격을 왜곡하지 않게 한다. MOLA는 오선 크기·페이지 넘김·파트 추출 문제를 다룬다. 모두 적용 한계를 검사하는 비교이며 1997 Feta의 donor로 분류하지 않았다.

다른 음악 소프트웨어의 반대 선택도 확인했다. [Bravura2013의 설계자](https://blog.dorico.com/2013/05/introducing-bravura-music-font/)는 전통 인쇄 미학에 Not-a-set을 본보기로 명명하며, SMuFL 매핑의 호환성 한계를 설명한다. [Petaluma2018](https://blog.dorico.com/2018/05/introducing-dorico-pro-2-and-dorico-elements-2/)는 Real Book의 손필사 스타일을 택하고 본보기에 없는 기호를 새로 설계한다. 따라서 ‘고전 판각체가 모든 장르의 유일한 답’이나 ‘모든 기호에 그대로 복제할 실물 하나가 있어야 한다’는 일반화도 지지되지 않는다. 두 글은 같은 설계자 계통이며 독립 증언 두 명으로 세지 않는다.

## Q7 · 카드의 주장 강도를 바꾸는 조건

사전 규칙은 원격 커밋 `2021e2f236d56073125d940fafe158d2e6ea5c70`의 SCOPE v1에 있다. 핵심 접점 제거 재판독은 **자체 점검**이다. B01에서 Thành2000 p38의 연결 발언을 빼면 구현과 기능 유사성은 남지만 hz 영감의 직접 귀속이 사라져 카드는 기능 비교로 낮아진다. 엄격 완결 수는 원래 0이므로 그대로 0이다. B03에서 `exact_donor`를 빼는 검사는 이미 미확인인 접점을 제거한 것이므로 변화가 없다. 이는 그 접점이 불필요하다는 증거가 아니다.

B01을 최초안 인과 카드로 올리려면 1996 제안 또는 더 이른 원안의 구체적 선택이 첫 hz 독서 전이었다는 날짜 있는 기록과, 독서 후 그 같은 선택을 바꿨다는 진술이 필요하다. 예컨대 폭 활용이라는 넓은 방향이 같더라도 Multiple Master 폭 축의 사용 같은 구체적 선택은 변경 후보가 될 수 있다. 그 연결은 현재 미확인이다. B03은 저자 사용 악보의 판·쪽을 특정하고 0.1.22→0.1.23의 flat 수정과 연결하는 메일·패치 설명이 가장 좁은 다음 접점이다. 정확판을 확인해도 최초 원안의 연결이 저절로 생기지는 않는다.

현재 탐색기의 회수 가능성과 사용자의 첫 노출은 관측하지 않아 모두 **미확인**이다. 검색어·현재 열람 성공 여부는 `frame.csv`에 있지만 이를 과거 발견 가능성이나 검색기 성능으로 변환하지 않았다. 카드 두 개는 `cards.md`에 각각 두 링크·용도·실패 조건·누락 접점을 갖춰 작성했다.

## 자료 수와 검산 범위

고유 산입은 **29저작**이며 단일 배당은 인쇄4, 악보4, 수신10(B01=6/B03=4), 기관4, 반례6, 추가1이다. 서로 다른 22저작만 뽑아도 필수 4+4+8+3+3을 충족하는 목록을 [출처 감사](streams/pdftex/corpus-review.md)에 남겼다. 두 LilyPond 릴리스를 하나의 진화 계통으로 더 엄격히 묶어도 전체28, 수신9(B01=6/B03=3)으로 최소수를 충족한다. 같은 저자의 여러 저작은 독립 증언 수와 다르다.

공인 번역·재인쇄는 원저작 계통 하나로 계산했다. 같은 배포의 여러 파일, 중간 LilyPond 배포, 보존 pdfTeX 코드 미러, 판매자 raster, 반복 열람과 접근 실패는 최소수에 추가하지 않았다. Wild는 Gutenberg 실물을 새로 본 당사자가 아니라 역사분석을 쓴 원저자라는 범위에서 1차 저작으로 분류했다. 출처 수가 충분해도 정확 제공판과 최초 독서의 빈 칸은 채워지지 않는다.

원장 필수 키·중복·참조·CSV 정밀도·네 판독·필수 두 표·짝 분모·세 약점과 커밋 순서는 `SELF_CHECK.md`, `evidence/acceptance-evidence.json`, `evidence/validation.json`에 남긴다. 수신 기능의 새 실행 검증이나 독립 인간 검토를 했다는 뜻은 아니다. 결과·수용 파일의 원격 고정 SHA 재열람과 session check의 실제 결과는 마지막 HANDOFF에 기록한다.

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| W1 · B01의 영어 원판·1992/1993 판 관계와 최초 독서→최초안 변경 연결이 없음 | [Thành2000 p38·pp117–118](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf), [1996 p248](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf), [Karow1997 p34](https://www.numdam.org/item/CG_1997___27_34_0.pdf). B01-I의 exact_donor·author_link·change_same_baseline이 **미확인**. | URW Hamburg1993 영어 책자 및 Zapf EPODD6(3)283–288 원판. 이어 1996 제안 전후 Thành/Sojka/Zlatuška 메일·노트에서 첫 독서와 선택 변경을 한 기록으로 연결. | 원판의 규칙과 날짜 있는 사전 대안·독서·동일 선택 변경이 연결되면 최초안 판정을 재검토. 기능 코드만 더 발견되면 상향하지 않음. |
| W2 · B03 사용 악보의 정확 판·쪽과 명시적 변경 이유가 없음 | [0.1.22 L2–5,119–167](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz), [0.1.23 L2–5,114–205](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz), [BA5635 서문 III](https://www.barenreiter.co.uk/prefaces/9790006493296_Innenansicht.pdf). 같은 flat 변화는 참이나 exact_donor·엄격 author_link는 **미확인**. | 1997 이전 BA5635 또는 BA5527 IV/14b pp196–218의 간기·판면, Müller FH6064/6065의 간기와 flat/double-sharp 쪽. 첫 연결 자료는 0.1.22→0.1.23 패치 설명·작성자 메일. | 저자 사용본과 해당 glyph·수정 규칙이 함께 특정되면 코드 인과를 재검토. 최초안 상향에는 별도 사전 설계 기록도 필요. |
| W3 · 보존 코드·후대 저장 출력·현대 견본은 당시 동일 실행을 보장하지 않음 | [Vieth2007 slide11](https://tug.org/~vieth/papers/bachotex2007/tex-history-talk.pdf), [LilyPond2003 Fig5](https://lilypond.gitlab.io/static-files/media/xivcim.pdf), [Fok README L18–46](https://sources.debian.org/src/lilypond/2.24.1-2/debian/README.Debian/). 버전 진본성·동일 출력·형상 보존 범위가 제한됨. | 당시 배포 해시/서명과 같은 입력·font·설정을 포함한 보관 출력. B01은0.14f, B03은0.1.22/23의 해당 flat 표본을 먼저 요청·확인. 역사 실행은 이번 범위 밖. | 인증된 배포·동일 입력 짝이 확보되면 반영 범위를 강화. 출력 불일치가 확인되면 해당 기능 반영 주장부터 축소하되 영감 진술과 혼동하지 않음. |
