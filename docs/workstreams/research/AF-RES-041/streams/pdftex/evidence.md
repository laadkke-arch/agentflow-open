# B01 직접 판독과 반증

2026-11-22 UTC. 저자 발언·정적 코드 관측·저장 출력 관측·이번 연구의 해석을 구분한다. 역사 프로그램은 실행하지 않았다. 다운로드 사본은 재배포하지 않으며 `sources.jsonl`의 원문 URL·판·해시로 재개한다.

## 1. 원전과 연결 발언

정확한 참고문헌 전사는 `baseline.md`에 있다. [Thành 2000](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) 논문 p38(저널 p354)은 hz 출판물이 개념적 영감이었으나 구현 정보는 얻지 못해 알고리즘을 직접 실험했다고 말한다. 이는 독립적인 **구현**과 양립한다. 독립적인 아이디어 발명이라는 뜻은 아니다. 최초 독서일, 특정 문헌을 받은 날, 읽기 전의 대안은 **미확인**이다. 이 진술은 나중의 동일한 회고 재인용을 더해도 독립 증언 수가 늘지 않는다.

[Karow의 1997 공인 번역](https://www.numdam.org/item/CG_1997___27_34_0.pdf) p34 각주는 원자료가 1993 URW 내부문서이고 저자 허락을 받은 영어→프랑스어 번역임을 밝힌다. 도판은 원자료에서 400dpi로 스캔했고 이 번역문 자체를 hz로 조판하지 않았다고 명시한다. 그러므로 본문과 도판의 계통은 확인되지만 **1993 영어 원판을 직접 읽었다고 기록할 수 없다**. `[NDT]`는 번역자의 추가 설명이다. p57 각주7의 Knuth–Plass 연결도 이 층에 속한다. p34가 함께 명명한 Zapf의 EPODD 논문은 별도 저작이다.

Zapf 1993 영문 논문은 Nottingham의 옛 저널 서버와 NTNU 소장 PDF를 직접 시도했으나 각각503·502/timeout이었다. 검색결과 첫 쪽 텍스트는 본문 열람으로 세지 않았다. 정확한 재개 대상은 Hermann Zapf, EPODD 6(3), pp283–288이며, 원문의 received/revised 날짜도 직접 원판에서 검증해야 한다. URW1993 책자는 공인번역과 원문을 대조해야 한다.

## 2. 변경 전 상태와 같은 기능

| 관측 단위 | 직접 확인한 선택 | 지위와 한계 |
|---|---|---|
| [Sojka·Thành·Zlatuška 1996](https://tug.org/TUGboat/tb17-3/tb52sojk.pdf), p248 §7 | 폭 가변 Multiple Master를 문단 줄바꿈에 넣고 `emergencyfontwidthstretch`를 만들자는 미래 계획 | 이번에 찾은 가장 이른 남은 제안. 벌써 자폭을 줄바꿈에 쓰는 방향이므로 “1996 원안은 자폭 고정이었고 hz를 읽어 처음 방향을 바꿨다”는 설명에 반한다. 평생 최초 아이디어라는 주장은 하지 않는다. |
| 같은 논문 p246 §4, p247 §5 | 1994 Knuth 메모의 영감은 PDF 출력 유도와 연결; 조판 엔진은 기존 TeX 기반 | PDF 출력의 영감을 microtype 결정의 영감으로 바꾸어 쓰면 안 된다. |
| [1997 사용설명서](https://tug.org/TUGboat/tb18-4/tb57than.pdf), p249, pp251–253 | 당시 시각 출력은 DVI와 동일; 대체 정렬/MM 폭은 다음 단계 | 1996보다 뒤의 제안 재진술. primitive 목록 부재만으로 전 프로그램의 기능 부재를 단정하지 않는다. |
| [0.12h archive](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.2-pdftex-0.12h.tar.gz), `web2c-7.2/web2c/pdftexdir/pdftex.ch` L86–190,4554–4601 | 이 change file의 매개변수와 줄바꿈 whatsit 처리는 PDF출력·이미지/form폭 통합; 뒤 버전의 확장·돌출 hook 없음 | 정적 코드 기준선. 보존목록 mtime1998-03-27과 첫 공개일은 구별한다. 이 버전이 hz 첫 독서 **이전**이라는 증거는 없다. |
| [Thành1998](https://tug.org/TUGboat/tb19-3/tb60than.pdf), pp284,288, Fig1 p285 | 줄을 정한 뒤 hbox를 표시하고 PDF text matrix에서 자폭을 조정 | 저자 구현 보고 + 저장 출력 이미지 관측. Fig1 좌우의 줄끝은 같다. 이 논문은 hz를 명명하지 않는다. |
| [0.14f archive](https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz), `web2c-7.3.3/texk/web2c/pdftexdir/pdftex.ch` L4753–4808,5108–5129,5402–5431,5460–5469 | 폭의 stretch/shrink를 active width 7·8에 추가; `pdf_adjust_spacing>1`이면 후보줄 shortfall에 반영, `>0`이면 정한 줄의 hpack에 반영. 돌출은 별도 조건으로 처리 | 직접 읽은 작성 소스. 내부 버전 `0.14f-released-20000525`; 보존목록 mtime2000-09-18. 최초 구현 릴리스라는 증거는 아니다. |
| [2000 논문](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf), §§6.5.1–6.5.2 pp69–71 | level1은 기존 줄바꿈 유지; level2는 폭 여유로 후보줄 평가를 바꿈 | code와 설명이 일치. 이 상태 변경은 1996의 넓은 방향을 거슬러 바꿨다는 증거와 다르다. |
| [Thành2001](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf), pp146–148 | 돌출과 자폭 두 제어, 글자별 설정·폭변형 font 준비와 모드 설명 | 공개 사용법. `0.14h` 경계 서술이 겹치므로 정확 도입일은 이 문장만으로 판정하지 않는다. |
| [Thành2004](https://tug.org/TUGboat/tb25-1/thanh.pdf), p37 Fig2 | 동일 문단의 좌우 출력에서 줄끝·하이픈이 달라짐 | 저장 출력 직접 이미지 판독. 저자 보고·저장 출력·이번 재실행을 구분하며 재실행은 하지 않았다. |

## 3. 같은 목적 안의 다른 조작

[Karow1997](https://www.numdam.org/item/CG_1997___27_34_0.pdf) p49는 가상 경계 문자와 자동 kerning으로 광학 여백을 정렬한다. p54 Fig21과 본문은 Ek가 흰 내부공간의 폭을 바꾸되 획 두께를 유지한다고 설명한다. p56은 모든 글자를 같은 방식으로 늘릴 수 없음을 밝힌다. p38은 새 ligature를 읽기·문자처리·글꼴 수용량 때문에 일단 포기했다. **원전 자체가 역사적 본보기의 모든 수단을 채택하지 않았다.**

[pdfTeX2001](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf)에서는 돌출량은 `lpcode/rpcode`, 글자별 확장성은 `efcode`와 font 확장 설정으로 제어한다. Type1의 FontMatrix, METAFONT 폭 매개변수, MM 축은 서로 다른 글리프 생성 방법이다. 원전의 획 보존을 어느 방법이나 자동으로 보장한다고 일반화하면 틀린다. 입력 문자 순서와 문단 정렬 목적은 유지하지만 모든 글꼴·문자·원전의 glyph 선택 전체를 보존하는 것은 아니다.

1998 Fig1은 같은 줄 경계에서 공백 조정을 보여준다. 2004 Fig2는 후보줄 선택까지 바뀐 출력을 보여준다. 둘을 하나의 전후 실험으로 합쳐서는 안 된다. 서로 다른 논문의 입력·font·설정이며, 각각 논문 안의 좌우 짝만 같은 비교 단위이다.

## 4. 반증 경로와 경쟁 설명

| 설명 | 지지하는 직접 자료 | 약화·범위 제한 |
|---|---|---|
| 알고리즘 독자 구현 | Thành2000 p38의 구현 정보 부재 진술 | hz 영감까지 부정하는 것은 같은 진술과 모순 |
| 이미 정한 방향을 뒷받침 | 1996 p248에서 자폭을 문단 줄바꿈에 넣는 제안이 이미 존재 | hz를 언제 처음 읽었는지 모르므로 “나중에 정당화했다”는 시간 순서는 입증되지 않음 |
| 선택적 모방 | Karow1997 p38의 ligature 유보, p54의 획 보존과 pdfTeX의 font 생성 방법 차이 | 같은 좁은 목적의 기능 대응까지 부정하지는 않음 |
| 후대 회고 | 명시적 핵심 연결은2000 p38;1998논문에는 hz 명명 없음 | 0.14f 코드·2001매뉴얼·저장출력으로 기능 존재는 독립해서 확인 가능 |

[Wild1995](https://www.numdam.org/article/CG_1995___22_5_0.pdf) pp12–14는 Gutenberg의 글자 변형·합자·약어를 분리한다. Fig5에서 이 차이를 직접 봤다. 이는 현대의 기하학적 자폭 확대와 역사적 수단을 등치하는 설명에 반한다. p9는 종이·재단·조판자 차이로 후대의 비례 추론이 확정되지 않음을 설명한다.

[André1995](https://www.numdam.org/article/CG_1995___22_61_0.pdf) p75는 합자를 입력문자로 치환하면 철자검사와 분철이 깨지고, 단순 자간 변경은 합자 내부 간격을 바꾸지 못한다고 설명한다. p74 Fig9를 직접 판독했다. [Mittelbach·Rowley](https://www.ntg.nl/maps/09/14.pdf) pp51–54는 여백·하이픈·문단·페이지 문맥 간 충돌을 서술한다. [Eng2007](https://www.typografi.org/justering/gut_hz/gutenberg_hz_english.html)의 Objections1–3은 형상·획두께·단어간격의 동일시를 반박한다. Eng의 미감 판단을 독립적인 가독성 실험 결과로 쓰지 않는다.

## 5. 판정 제안과 카드의 상한

엄격 최초안 기준 B01의 완결 사슬은 **0/1**이다. 핵심 결손은 **정확 영어 원판의 직접 대조, 첫 독서와 최초 남은 제안 사이 순서, 그 제안의 어떤 선택이 독서 뒤 달라졌는지**이다. 기존 코드에서 새 기능이 생겼다는 비교와 회고를 허용하면 **인용+동일 기능 반영**은1건으로 읽을 수 있지만, 이를 같은 최초 결정의 인과 확인1건으로 바꾸어 세면 안 된다. 0.12h→0.14f는 직접 코드 관측이며 1998→2000 설명만으로 코드를 추정한 것이 아니다.

제거 재판독: Thành2000 p38의 저자 연결을 빼면, 1996계획·1998실험·0.14f코드·2001사용법·2004출력은 남는다. 그러나 어느 원전의 독서가 변경을 야기했는지 판단할 근거가 사라진다. 기능 유사성은 인과를 대신하지 않는다.

반환 카드의 두 링크는 [Karow1997 공인번역 pp49,54,56–57](https://www.numdam.org/item/CG_1997___27_34_0.pdf)과 [Thành2000 §4p38,§6.5pp69–71](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)를 제안한다. 용도는 **문단 정렬에서 글자 폭의 제한된 여유를 후보줄 평가에 더하는 원리**이다. 광학 여백은 별도 선택으로 안내한다. 글꼴 형태를 보존해야 하는 경우, 폭 변형을 허용하지 않는 경우, 입력문자 치환으로 합자를 처리하는 경우에는 그대로 가져오면 안 된다. 첫 노출·현재 탐색기의 회수 가능성은 **미확인**이다.

## 6. 정적 소스 재개 입력

두 archive의 SHA256은 `sources.jsonl` P012·P013에 있다. 다음은 실제 실행한 종류의 정적 열람을 재현하는 명령이며 역사 소프트웨어를 빌드하거나 실행하지 않는다.

[보존사업 담당자 Ulrik Vieth의 2007 발표](https://tug.org/~vieth/papers/bachotex2007/tex-history-talk.pdf) slide11은 pdfTeX 구버전 일부를 web2c에서 재구성했고 일부를 ftp.muni.cz에서 미러했다고 설명한다. 따라서 아래 파일을 당시 배포 tarball과 바이트 동일한 진본이라고 부르지 않는다. 보존된 작성 소스의 기능 대조와 최초 배포물의 진본성은 별도 접점이다.

```sh
python -B - <<'PY'
import io, tarfile, urllib.request, hashlib
items = [
 ('https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.2-pdftex-0.12h.tar.gz', 'web2c-7.2/web2c/pdftexdir/pdftex.ch', 86, 190),
 ('https://ftp.math.utah.edu/pub/tex/historic/systems/pdftex/pdftex-0.xx-web2c/web2c-7.3.3-pdftex-0.14f.tar.gz', 'web2c-7.3.3/texk/web2c/pdftexdir/pdftex.ch', 5108, 5129),
]
for url, member, start, end in items:
    data = urllib.request.urlopen(url).read()
    print(url, hashlib.sha256(data).hexdigest())
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        lines = archive.extractfile(member).read().decode('latin1').splitlines()
        for n in range(start, end + 1):
            print(n, lines[n - 1])
PY
```

이 메모의 재판독은 같은 연구 담당자의 자체 점검이다. 독립 검증자가 한 실험으로 표시하지 않는다.
