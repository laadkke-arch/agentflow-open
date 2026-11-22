# B03 LilyPond 수신 기록 · 전후 코드와 반증

상태: 묶음③ 통합용 연구 기록. 최종 네 판정은 root가 원전 판본 조사와 결합한다. 역사 프로그램 실행은 하지 않았다. 출처 ID는 같은 디렉터리 `sources.jsonl`, 사건·조작의 구조화 행은 `chronology.json`과 `mechanisms.json`, 검색 및 실패 경로는 `frame.json`에 있다.

## 새로 닫힌 기준선과 남은 접점

1997-08-01의 [0.1 발표](https://lilypond.org/misc/ANNOUNCE-0.1) L78–84는 MusiXTeX T.73 fonts가 필요하다고 명시한다. [0.1.0 tar](https://lilypond.org/download/sources/v0.1/lilypond-0.1.0.tar.gz)의 `tex/taupindefs.tex` L11/29는 musix20/musix16을 쓰므로 초기 배포의 기존 글꼴을 직접 특정했다. 더 이른 [0.0.1 tar](https://lilypond.org/download/sources/v0.0/lilypond-0.0.1.tar.gz)의 `lilyponddefs.tex` L3–10도 musix20을 명시한다. 그 파일 mtime는 1996-10-06, 현 배포 index의 날짜는 1996-10-08이다. 이것은 최초 남은 코드이며 최초 미공개 원안·원전 독서 전 상태는 **미확인**이다. [B03-L002,003,025,026]

[1.0.1 tar](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)의 ANNOUNCEMENT L14–20은 기존 글꼴 불만과 새 Feta 제작을 연결하고 L39는 MusiXTeX 불필요를 말한다. 같은 배포의 fonts.doc L11–23은 선호 출판사 악보 모방과 원본 MetaFont 소스라는 저자 설명을 담는다. sharp와 natural은 Schubert/Bärenreiter, double-sharp와 flat은 Müller/Hofmeister로 귀속한다. 판번호·페이지·독서일은 없다.

## 가장 유용한 새로운 전후: flat의 본보기 교체

[0.1.19](https://lilypond.org/download/sources/v0.1/lilypond-0.1.19.tar.gz) `mf/toevallig.mf` L2–5는 flat을 Schubert에 귀속한다. [0.1.22](https://lilypond.org/download/sources/v0.1/lilypond-0.1.22.tar.gz) `mf/feta-toevallig.mf` L2–5까지 그 귀속이 유지된다. [0.1.23](https://lilypond.org/download/sources/v0.1/lilypond-0.1.23.tar.gz) 같은 파일 L2–5는 flat을 Müller에 옮긴다. 직전 두 판의 전체 파일을 직접 비교하여 아래 동시 변경을 확인했다. [B03-L008,011,012]

| 변수·목적 | 0.1.22의 기존 코드 | 0.1.23의 후속 코드 | 판독 범위 |
| --- | --- | --- | --- |
| 기호 정체성 | `Flat`, `-1`, `flat` (L157) | 같은 이름·기호 값 (L191) | 같은 목적·대상 유지, **직접 관측** |
| 도너 귀속 | Schubert/Bärenreiter의 flat (L4) | Müller/Hofmeister의 flat (L5) | 저자 소스 주석, 정확 판·쪽은 **미확인** |
| 도형 생성 | `flat_meta_symbol`/`flat_symbol`, brush·penstroke (L119–152) | `draw_meta_flat`, serif·fill/unfill (L114–185) | 정적 코드 재작성 **직접 관측** |
| 단일 flat 폭 | 9/12 interline (L158) | .8 interline 및 왼쪽 여유 (L192) | 변수 값 변경 **직접 관측**, 출력 계측 아님 |
| 배 두께·줄기 | crook 1/4 interline, bottom stem 5/4·top stem 2 staff thickness (L146–149) | crook 1/3 interline, bottom 1.2·top 2 (L122–124,193) | 같은 기호의 비율 조정 **직접 관측** |
| double flat | 하나를 복제·평행 이동 (L162–166) | 좌폭 .7·우폭 .8·겹침 .05의 두 호출 (L197–205) | 이웃 기호에도 반영되나 본보기의 double-flat 직접 모방은 **미확인** |

이는 동일 기호의 구체적인 전후다. 그러나 귀속 수정이 실제 독서 후 변경의 완전한 진술은 아니며, 정확한 원판 모양과 코드 형상을 대조하기 전 엄격 인과 양성으로 올리지 않는다. 특히 0.1.22는 이미 Schubert를 본보기로 적은 자작 flat이다. 이것을 ‘외부 인쇄물을 알기 전 최초 선택’으로 바꾸면 기준선이 이동한다.

mtime는 0.1.22 파일 1997-10-10, 0.1.23 파일 1997-10-14이다. [Debian 1997-10-20 공개 목록](https://lists.debian.org/debian-changes/1997/10/msg00023.html)의 HTML L564–573은 두 upstream 판을 실제 배포 목록에 싣는다. 따라서 0.1.23의 **공개 가용성은 늦어도 1997-10-20**이다. 파일 날짜를 최초 공개일이나 악보 독서일로 사용하지 않았다. [B03-L018]

## 일부러 따르지 않은 특징

1.0.1 `mf/feta-toevallig.mf` L25–27은 많은 sharp의 가로 획 끝이 수평임을 알면서 Wanske가 언급하지 않으므로 그 특징을 무시한다고 적는다. 외부 본보기의 관찰은 실제 선택을 강제하지 않았다. 정확한 Schubert 원판을 보지 못했으므로 ‘그 판의 끝을 일부러 거부했다’까지 확장하지 않는다. 입증한 것은 저자가 **관찰한 일반 특징을 의식적으로 미채택한 진술**이다. [B03-L001]

별도로 [0.1.19](https://lilypond.org/download/sources/v0.1/lilypond-0.1.19.tar.gz) L37의 sharp slope에 쓰던 beamheight/2가 [0.1.20](https://lilypond.org/download/sources/v0.1/lilypond-0.1.20.tar.gz) L37–39의 Wanske 주석과 beamheight로 바뀐다. 주석은 약 18도를 언급한다. 이 변경은 flat의 0.1.22→0.1.23보다 먼저다. Wanske의 정확한 책 쪽은 **미확인**이므로 책의 규칙 본문까지 닫힌 것으로 세지 않는다. [B03-L008,009]

`Documentation/tex/engraving.bib` L63–70은 Wanske의 *Musiknotation — Von der Syntax des Notenstichs zum EDV-gesteuerten Notensatz*, Schott-Verlag, Mainz, 1988, ISBN 3-7957-2886-x를 특정한다. 같은 서지 L19–29는 Ted Ross, *Teach yourself the art of music engraving and processing*, Hansen House, Miami, 1987이다. 이 서지 확인은 원저작 해당 쪽 직접 열람과 다르다. [B03-L001]

## 날짜와 단계

0.1.0은 MusiXTeX. 0.1.13은 dynamics의 자체 MF, 0.1.15는 자체 noteheads와 기존 MusiXTeX accidentals의 공존, 0.1.19는 named-score accidentals source, 0.1.23은 flat 본보기 귀속·정의 변경, 0.1.27은 feta라는 폰트명이다. 그러므로 0.1 전체를 변경 전으로, 1.0을 첫 Feta 구현으로 쓰면 틀린다.

위 tar member mtime는 파일 작성/보존 날짜다. index의 last-modified와 최초 공개일·사용자의 입수·저자의 독서는 각각 다르다. 원장에는 구분하여 기록했다.

## 반영과 출력 증거의 경계

[2003 저자 논문](https://lilypond.gitlab.io/static-files/media/xivcim.pdf) §4, PDF p3–4와 Fig5를 읽고 p4를 직접 렌더하여 flat·half-notehead·quarter-rest 세 글리프를 판독했다. 위로 두꺼워지는 flat 줄기와 작은 다이아몬드 성격의 notehead, 둥근 rest 끝에 관한 저자 설명과 보존 도판을 연결할 수 있다. 이것은 2003년 저장 출력물이다. 1997년이나 1.0.1 바이너리의 실제 출력이라고 소급하지 않는다. 같은 페이지 Fig6의 optical spacing은 글리프 형상과 별도 기능이다. [B03-L016]

[2006 FISL 슬라이드](https://lilypond.gitlab.io/static-files/media/FISL7-slides.pdf) slide9는 Henle(2001), Bärenreiter(1950), Feta(LilyPond v2.0)의 flat을 실제로 나란히 보여준다. slide16은 1.4/Bärenreiter/2.7.29의 악보 출력 비교다. 두 페이지를 시각적으로 읽었다. 이 연도와 작품 비교를 1997년 Schubert/Müller 판 식별로 대신할 수 없다. 새로운 발표이지만 같은 저자 회고 계통이다. [B03-L017]

[Debian 1997-10-27 목록](https://lists.debian.org/debian-changes/1997/10/msg00031.html) HTML L539–542는 0.1.25 업그레이드 후 일부 글꼴이 보이지 않는 문제의 해결법을 README에 추가했다고 한다. [Anthony Fok의 1999-07-07 서명 README](https://sources.debian.org/src/lilypond/2.24.1-2/debian/README.Debian/) file L18–46는 fontmap 및 stale tfm/pk를 원인으로 설명한다. 소스와 실제 출력 사이에는 설치·매핑·캐시 조건이 더 있다. 이 두 기록은 정상 출력의 보장 범위를 줄이는 반증이다. [B03-L019,020]

## 경쟁 설명과 좁은 외부 비교

| 설명 | 지지하는 관측 | 약화하거나 제한하는 관측 | 현재 해석 |
| --- | --- | --- | --- |
| 독자 구현 | 1.0.1 fonts.doc는 MF 소스를 직접 만들었다고 말한다. flat의 함수가 독자적으로 재작성됐다. | 같은 파일이 출판물·기호를 구체적으로 명명한다. | 구현 독자성과 형상 영감은 양립한다. 모든 글꼴 소스가 무차용이라는 광범위한 주장은 dynamics의 cmbxti10 이력 때문에 별도 검토가 필요하다. |
| 이미 정한 방향의 정당화 | 1998 발표·2003/2006 설명은 초기 코드 뒤에 남은 진술이다. | 1997 코드 자체에 donor 귀속과 flat의 전후 변경이 있다. | 순전한 후대 창작이라는 설명은 약화하지만, 특정 독서가 최초 방향을 바꿨다는 순서는 남아 있지 않다. |
| 선택적 모방 | 기호별로 다른 출판사를 사용하고 sharp의 관찰 특징을 무시한다. double-flat은 별도 변수로 확장한다. | 정확 원판 없이는 어느 세부가 같은지 모두 판별할 수 없다. | 현재 자료에 가장 직접적으로 맞는 설명은 기호별·변수별 선택적 모방이다. |
| 후대 회고 | 같은 저자 논문·발표가 전통 판각의 원리를 재서술한다. | 1997 source attribution과 1997 Debian 배포 수신 기록은 당대 자료다. | 회고만 있는 사건은 아니다. 독립 증언 수를 논문·발표 수만큼 늘리지는 않는다. |

[Bravura 설계자의 2013년 발표](https://blog.dorico.com/2013/05/introducing-bravura-music-font/) §Bravura는 전통 인쇄처럼 둥글고 굵은 기호를 만들면서 실제 본보기로 Not-a-set dry transfer를 명명한다. 같은 모양의 목표가 곧 같은 donor인 것은 아니다. 같은 글에서도 SMuFL 매핑 때문에 일반 Finale/Sibelius에서 그대로 쓸 수 없다고 하며, 저자 답변은 게시된 Sibelius 예가 별도 호환 시험판을 사용했다고 밝힌다. [B03-L021]

[Petaluma의 2018년 발표](https://blog.dorico.com/2018/05/introducing-dorico-pro-2-and-dorico-elements-2/) §Petaluma는 Real Book의 손필사 스타일을 선택하고 원본에 없는 기호를 새로 설계했다. 따라서 ‘기호마다 실물에서 모양을 복제해야 한다’와 ‘고전 판각체가 모든 장르에 유리하다’는 일반화는 성립하지 않는다. 이 두 자료는 B03을 검사하는 비교이며 새 표본 사건이 아니다. [B03-L022]

## 네 접점 판독에 대한 제안

| 기준선 | 정확 donor 판·쪽 | 당시 donor 가용성 | 저자 연결 | 같은 기준선 변경 | 같은 목적 반영 | 허용 문구 |
| --- | --- | --- | --- | --- | --- | --- |
| 최초안 | **미확인** | **미확인**: 정확 판이 고정되지 않음 | 작품·출판사·기호 수준의 명명은 참, 독서 후 최초안 변경 연결은 **미확인** | **미확인**: 0.0.1도 이미 구현이며 사전 미공개 선택은 없음 | Feta 기호 소스와 후대 저장 도판은 참, 최초판 실제 출력은 **미확인** | ‘특정 출판물의 기호를 본보기로 삼았다’와 ‘같은 기능에 반영했다’까지. 최초 계획 변경 인과는 보류. |
| 기존 코드 | **미확인** | **미확인**: 0.1.23 수신 공개 시점은 별도 확인 | 0.1.22→23 flat donor 귀속 변경은 참, 독서 날짜·직접 변경 이유는 **미확인** | 참: 같은 flat의 정적 코드 전후가 있다. earliest code 0.0.1과 flat-specific 0.1.22는 다른 보조 기준선이다. | 참: flat 의미와 같은 생성 호출에 반영. 당시 실행 출력은 **미확인** | ‘같은 기능 반영까지’. 정확 원판을 충족한 완결 인과로 올리지 않는다. |

사전 고정한 B03 `exact_donor` 접점을 제거한 재판독에서도 엄격 완결은 증가하지 않는다. 그 접점은 이미 **미확인**이다. 코드 전후가 명료해졌다고 정확 판 조건을 사후 삭제하면 다른 기준이 된다. 출판사 계열만 허용하는 민감도는 별도 표시가 필요하다.

카드의 두 링크 제안은 [고정 1.0.1 소스](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)와 [도형·원리 설명을 볼 수 있는 2003 저자 논문](https://lilypond.gitlab.io/static-files/media/xivcim.pdf)이다. 용도는 ‘기호 의미는 유지하면서 획 두께·곡선·끝 모양의 변수를 전통 인쇄본에서 골라 설계하는 사례’다. 필요한 조건은 대상 기호·장르·출력 크기·폰트 매핑을 따로 검사하는 것이다. 초기 원판의 정확 재현이나 모든 기호의 보편 규칙을 반환하면 근거보다 강해진다. 최초 노출과 탐색기의 현재 회수 가능성은 관측하지 않았다.

## 저작 수, 검산과 다음 최소 조사

대표 counted 행은 수신 4저작(0.1.0,1.0.1,2003 논문,2006 발표), 독립 발행 1저작(Debian 1997-10-20), 반대·한계 3저작(Fok 1999,Bravura2013,Petaluma2018)이다. 중간 tar·미러·반복 열람·접근 실패·목록·2차 탐색 자료는 추가하지 않았다. 0.1.0/1.0.1을 한 진화 저작으로 묶으면 수신 3, 전체 7이며, 이러한 보수계통 감도를 별도로 보고할 수 있다. 동일 저자가 쓴 2003/2006은 독립 목격 증언 두 명이 아니다.

다음 조사에서 가장 가치 있는 한 건은 **1997-10-14 이전 사용한 Müller/Hofmeister의 정확한 인쇄본 쪽**과 0.1.22→0.1.23 flat 변경을 직접 연결하는 작성자 메일·패치 설명이다. donor의 현대 견본은 당시 본보기 동일성 검증을 대신하지 못한다. 처음부터 Feta를 만들기로 정했는지와 기존 MusiXTeX를 계속 쓰려 했는지는 최초 제안 기록이 있어야 갈린다.
