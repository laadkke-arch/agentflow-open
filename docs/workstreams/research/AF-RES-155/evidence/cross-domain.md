# Q7 문헌 판본과 악보

## Hamlet 1.2 첫 독백

| 공개 판본의 같은 대목 | 실제 읽은 위치 | 후속 편집 표시와 한계 |
|---|---|---|
| Internet Shakespeare Editions, Eric Rasmussen의 Q2(1604) 디지털 판본 | Act 1, scene 2, 1.2.129 / TLN 313에서 `sallied`. 뒤 1.2.133 / TLN 317에 `w[e]ary` | 현대 편집의 대괄호가 실제 표시된다. 특정 당시 종이의 자형을 이 전사로 인증할 수 없다. [L01 · 실제 본문](https://internetshakespeare.uvic.ca/doc/Ham_Q2/scene/1.2/index.html) |
| Bodleian Arch. G c.7(1623)의 기관 디지털 판본 | 같은 독백 시작 F TLN 297에서 `solid`, TLN 300–301에서 `Selfe-slaughter`와 `weary`. 기관 XML의 `l n`으로 위치 재확인 | 이 디지털 판본은 다른 가까운 행 TLN 287의 `beft`/교정 `best`를 별개 orig/corr로 태그한다. 여기서 본 것은 기관 전사와 그 표현이다. [L02 · 디지털 텍스트와 XML](https://firstfolio.bodleian.ox.ac.uk/ff/ham/1/2) |
| Folger Shakespeare Library, Mowat/Werstine 판 | 1.2.133 / FTLN 0323 `sullied`, 다음 FTLN 0326 `⟨self-slaughter!⟩`, 0327 `⟨weary,⟩`. 2020 갱신본 HTML과 발행 PDF의 인쇄 p.29(파일 19쪽) | 발행 소개는 `sullied`를 Q2 철자 현대화로 명시한다. 단어 자체에는 교정 겹괄호가 붙지 않는다. 꺾쇠는 F1을 선택한 곳을 보존한다. PDF 텍스트 추출에서는 웹에 있던 꺾쇠가 보이지 않아 PDF 자형을 별도 확인해야 한다. HTML과 PDF는 한 발행본으로 센다. [L03 · 실제 본문](https://www.folger.edu/explore/shakespeares-works/hamlet/read/1/2/) [L03-P · 발행 PDF p.29](https://flgr.sh/txtfssHampdf#page=19) [L03-I · 편집자 범례](https://www.folger.edu/explore/shakespeares-works/hamlet/an-introduction-to-this-text/) |

같은 장면이어도 TLN·FTLN 및 장면 내 번호가 각각 다르다. 앞의 퇴장과 뒤 두 행을 함께 맞췄다. 텍스트 독자에 맞춘 Folger의 정상화는 편집자가 정한 결과다. 원 증인의 자형·쉼표·후대 표기를 옮기려는 요청이라면 소장본/면/판독법을 먼저 고정해야 한다. 편집 기호를 보존할 목표면 데이터 추출 경로도 확인한다. 같은 곳의 문학적 의미나 저자의 최종 선호를 이 세 대조로 결정할 수 없다.

이 세 건은 그 기관이 발행한 실제 **디지털 판본 본문** 판독이다. 오래된 종이 원면 2개 목표는 미달(0/2). Folger Q2 원면은 사람 확인 페이지. Bodleian 원면 전체 PDF는 웹 도구의 크기 제한, Cloud 접속은 터널 오류. ISE Garrick Q2 발행 정보 및 장면 p.8은 열렸으나 TLN 313 원면을 시각 판독하지 못했고, HathiTrust Griggs 판 전체 보기에는 403이 났다. 별도의 접근 가능한 원면으로 교차 확인 전까지 원면에서 본 자형이나 잉크 관측은 공석이다. 시도와 발행본 중복은 [sources.jsonl](../sources.jsonl)에 있다.

## Mozart K.498, I Andante m.9

Mutopia 편집 Maurizio Tomasi, `Mutopia-2014/03/28-250`, public domain. 원 대조판은 Breitkopf & Härtel 1879. 발행처의 A4 완성 PDF ZIP은 웹 도구의 ZIP 미지원과 Cloud의 제한된 egress로 내려받지 못했다. 발행처 자체 [고정 GitHub 배포원](https://github.com/MutopiaProject/MutopiaProject/tree/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/MozartWA/KV498/k498/k498-lys)에서 실제 전체 악보와 양 파트를 열었다. 2014 산출의 LilyPond는 2.16.1이다. 아래는 그 공개 악보 소스의 2.24.4 재각보 PDF 1쪽을 직접 시각 판독한 결과다. 목록이나 MusicXML 예시는 배제했다.

| 원자료와 위치 | 눈으로 확인한 기보 | 실음과 판독 |
|---|---|---|
| M01 총보, p.1 시스템 3 마지막 마디. 시작 번호 7부터 두 쉼표 마디 뒤 클라리넷 진입 | 윗보표 Clarinetto in B.의 조표 내림표 1개. m.9 첫음 F5 4분음표 붙임줄→F5 16분음표. 이어 G5/F5/E5/F5 네 64분음표와 A5/F5/C5 세 8분음표 | 클라리넷의 기보 C4는 실음 B♭3. 따라서 해당 첫음은 E♭5, 나머지도 각 기보음보다 온음 아래. [총보 이미지](music/k498-score-I-m7-9.png) |
| M02 B♭ 클라리넷 파트, p.1 첫 시스템 8마디 쉼표 직후 | 조표 내림표 1개와 같은 F5·붙임줄·음가·후속 음렬 | 총보의 해당 관악기 보표와 기보 및 실음 일치. 총보라는 이름만 보고 실음표로 취급하면 틀린다. [클라리넷 이미지](music/k498-clarinet-I-m1-11.png) |
| M03 대체 바이올린 파트, p.1 첫 시스템 8마디 쉼표 직후 | 조표 내림표 3개. E♭5 4분음표 붙임줄→E♭5 16분음표, F5/E♭5/D5/E♭5 네 64분음표, G5/E♭5/B♭4 세 8분음표 | 바이올린 실음은 기보와 같다. 총보 목관의 실음과 순서 및 음가 일치. [바이올린 이미지](music/k498-violin-I-m1-11.png) |

원본 소스에서 [공유 m.9 기보](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/MozartWA/KV498/k498/k498-lys/clarinet-i.ily#L3-L12), [총보의 악기/이조](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/MozartWA/KV498/k498/k498-lys/k498-piano.ly#L18-L26), [파트의 같은 이조](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/MozartWA/KV498/k498/k498-lys/k498-clarinet.ly#L13-L24), [바이올린의 음표 변환](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/MozartWA/KV498/k498/k498-lys/k498-violin.ly#L13-L24)을 확인했다. 보표·파트가 같은 편집 계보이므로 독립된 세 작품이나 재현 세 건으로 환산하지 않는다.

### 음악 재생 기록

- 발행자 원 Git SHA `2144afd6f52d56c5b6995b8b589ef1268b3139f0`, 악보 디렉터리 트리 `81dacb12f0ce4611ad2a9742a90a1f6d0256f61a`. `k498-piano.ly` SHA-256 `8aba7246f6f53f0aa6c2110963bdc9bb00ebb6392a1b4362db2b24e67c22d912`, `k498-clarinet.ly` `abebdfb54345a07344d0c4e0e11c9d6e1bf8596185bd2d68534c9a3992b29302`, `k498-violin.ly` `c177e98f6c0e13b5a95fac6619a7e9d0cd34f14c9ac4e215b4229458f073868c`.
- [LilyPond 2.24.4 Linux x86_64 바이너리](https://gitlab.com/lilypond/lilypond/-/releases/v2.24.4/downloads/lilypond-2.24.4-linux-x86_64.tar.gz) 아카이브 SHA-256 `53bc1df875ee56dabe56ae1f0b4550237e0c9acc837b60f0ef8c42fc35a68641`. 원소스에서 `lilypond -o OUT/k498-piano k498-piano.ly` 종료 0. 동일 형식의 두 원파트는 폐기된 레이아웃 명령 때문에 종료 1. `compressMMRests`는 이 레이아웃 위치에서 임시 시도 종료 1. `convert-ly --from=2.16.0 --to=2.24.4 k498-clarinet.ly` 결과가 제안한 `compressEmptyMeasures`로 줄 하나만 바꾼 사본을 각각 실행해 종료 0. 음표/이조 줄과 공유 `clarinet-i.ily`는 같다.
- PDF SHA-256은 총보 `0b176c5f3ef7ac51903f6302c50552ceb1e38ab7580306f332d7c466fbd044ae`, 클라리넷 `d4bd2244e0b6d8f40ce7bdd2f8b989a65214935f281d11e713b7d182cc81392b`, 바이올린 `084946e3fef87d3d654fdb66c0d36ee6c104f0e4d7740e15e390628981fcf535`. 세 자른 이미지의 지문은 [music/sha256.txt](music/sha256.txt).
- MIDI 출력도 384 ticks/quarter에서 m.9의 여덟 실제 onset (tick,note) `(9216,75) (9696,77) (9720,75) (9744,74) (9768,75) (9792,79) (9984,75) (10176,70)`이었다. 붙임줄의 두 음표머리는 하나의 onset이다. Mido 1.3.3은 기본으로 클라리넷의 9-sharp key-signature 메타값에서 중단했다. 수치 onset 확인에만 Mido의 일시적 인메모리 lookup `_key_signature_decode[(9,0)] = "Eb"`을 사용했다. 기록된 MIDI 바이트는 그대로다. 이조된 키 이름과 소리의 음높이를 다른 층으로 취급해야 하는 별도 반례다. 실제 연주자의 음색 및 조율은 측정하지 않았다.

악보 편집자는 조표·기보음·파트의 표지와 읽기 편한 쉼표를 계약에 맞게 작성한다. 연주자에게 필요한 전달값은 대상 악기와 기보/실음 모드다. MIDI 소비자에게는 이조 뒤 소리뿐 아니라 읽을 수 있는 조표 메타데이터도 별개다. 동형의 렌더링이나 들리는 한 단어만으로 둘을 판정할 수 없다는 점에서 X05와 연결되지만 사람의 이해나 사용자 경험은 비교하지 않았다.
