# root의 마지막 원문 대조 · 자체 점검

RESULT 초안 작성 뒤 2026-11-22T20:35:50Z–20:37:13Z에 핵심 공개 URL9개를 순서대로 재개봉했다. 모두 HTTP200이고 본문9개를 받았다. 기존8개는 묶음③의 해시와 일치했고, 추가 Karow2015도 보조 조사 원장의 해시와 일치했다. 실제 시각·bytes·SHA256은 `final-recheck-downloads.json`에 있다. 다음 표는 다운로드 성공만이 아니라 root가 확인한 정확 위치와 판독 범위다.

| 질문 | 다시 읽은 위치·원문 | 실제 판독과 반증 결과 | 범위 |
| --- | --- | --- | --- |
| Q1 | [Thành2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) pp117–118 refs40–43; [Karow1997](https://www.numdam.org/item/CG_1997___27_34_0.pdf)p34; [Karow2015](https://tug.org/TUGboat/tb36-2/tb113zapf-karow.pdf)p97 refs5/10 | refs40·43만1993hz. URW공인번역관계와1992/1993서지불일치를 확인. 영어원판은여전히미열람. | ROOT-R020/021/023. GoogleBooks는20:38:31Z실제링크재개봉해1993·38pp서지만확인(R012). 직접open실패도R014에남김. |
| Q2 | [1996논문](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf) physicalp5/printed248 §7 | 추출텍스트의글꼴encoding이깨져페이지를렌더하여직접읽음. MultipleMaster variablewidthaxis와paragraphbreaking제안존재. 첫독서전이라고추정하지않음. | ROOT-R022; 파일해시동일. 원안·기존구현구별유지. |
| Q3 | [Thành2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)p38; [LilyPond1.0.1](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) `mf/feta-toevallig.mf` L11–27 | 영감과구현정보부재를같은본문에서재확인. 기호별출판물명명과sharp수평끝미채택을재확인. 정확독서→같은최초안변경문장은없음. | ROOT-R021/025; 저자진술이며독립목격증언추가아님. |
| Q4 | Karow1997p54Fig21; [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz)L140–167; [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz)L114–125,188–205 및 `autometric.mf`L46–63,99–110 | Ek의흰공간변경·획보존을본문/그림으로읽음. flat의w#와b#분리및crook_fatness매개변수변경확인. 실제잉크폭으로쓴초안을정정. | ROOT-R023/026/027. 반복열람은산입안함. |
| Q5 | [0.14f](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz) `pdftex.ch`L5108–5129,5460–5469; Thành2000pp69–70; [2001설명](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf)pp146–148 | >1은후보줄평가, >0은실제packing의조정이라는다른조건을확인. 글자·문단목적을유지하나출력재실행은하지않음. | ROOT-R028/021/024. 재구성archive의진본성한계를유지. |
| Q6 | Thànhp38; FetaL25–27; Karowp54; 앞서연도·판면을고정한BA5635서문III와후대NSA지침 | 독자구현은영감부정이아니고,한본보기의모든특징을채택하지않았음을재확인. BA5635현대서문/현행견본을1997사용본으로치환하지않음. | 핵심URL은위재개봉9개에포함. 추가보존도판재독은ROOT-R040–042에별도기록하고정확초시각은미확인으로표시. |
| Q7 | 원격`2021e2f236d56073125d940fafe158d2e6ea5c70`의SCOPE.md; p38발언을제외한0.14f소스및exact_donor를제외한flat비교 | GitHub에서SCOPE를다시읽어blob`d6ad4b3d8a709749c7cf8c3fc862f2923776fc04`·4391문자를확인. 규칙은그대로이며0/2·0/2·기능반영2/2의다른단위를유지. | root자체재판독. 부족한접점을삭제하여긍정으로올리지않음. |

이 표의 ‘없음’은 읽은 범위에서 필요한 연결을 발견하지 못했다는 뜻이다. 모든 미공개 기록의 부재를 증명하거나 인과가 없었다고 반증한 것이 아니다. 특히 정확판·독서일의 미확인은 그대로 남긴다.

## 재판독에서 실제 수정한 것

- Feta의9/12→.8은오른쪽extent매개변수이며왼쪽extent도바뀐다. 전체glyph폭·인쇄잉크폭으로부르지않는다.
- 같은버전경계의귀속·함수공변경은실제편집시각의동시성이나읽은직후수정을증명하지않는다.
- URW원판URL/본문미확보와Zapf의확인URL접근실패를분리했다.
- 1992회고와1993서지의차이를보존하고원본간기없는연도교정을하지않았다.
- 최초안의사전선택은1996제안자체일수도있다. 반드시그보다이른문서만을요구하는추가규칙을만들지않았다.

확인한도판원본과archive는재배포하지않는다. 재개에는원장URL·버전·해시·멤버·쪽을사용한다. 같은작업자의재독·보조세션교차검토이며독립인간검증이나역사프로그램재현이아니다.
