# 신문과 음악의 원자료 대조

## 신문

LOC의 Trek, 1942-12-01, ed-1, image 5는 기관이 지정한 독립 원면 URL을 열었다. 웹 본문·JSON과 shell 다운로드에서 403 또는 접근 실패가 관측됐다. 이전 연구의 가이드 캡처는 이 면을 재판독한 증거에 포함하지 않았다. SCOPE에서 정한 대체 면은 Morning Oregonian, 1900-01-01, ed-1, seq-1이다. [LOC 면](https://www.loc.gov/resource/2008257345/1942-12-01/ed-1/?sp=5) · [N-loc-guide](https://guides.loc.gov/chronicling-america/citations-links) · [N-page](https://oregonnews.uoregon.edu/lccn/sn83025138/1900-01-01/ed-1/seq-1/)

대체 면의 실제 기관 PDF는 검색 도구로 p1의 텍스트 레이어를 읽었고, 보존소의 별도 `ocr.txt`도 열었다. PDF 픽셀이 전달되지 않았고 브라우저 PDF는 터널 연결 오류, 원시 ALTO URL은 웹 도구의 application/xml 미지원과 shell 403이었다. 아래의 L은 텍스트 도구가 매긴 줄 위치다. 판면의 x/y와 원본 글자는 미판독으로 남긴다. [N-pdf](https://oregonnews.uoregon.edu/lccn/sn83025138/1900-01-01/ed-1/seq-1.pdf) · [N-raw](https://oregonnews.uoregon.edu/lccn/sn83025138/1900-01-01/ed-1/seq-1/ocr.txt) · [N-guide](https://oregonnews.uoregon.edu/ocr/)

| 같은 면의 위치 | OCR · PDF 텍스트에서 읽은 값 | 검색값의 비교 | 원면 글자·x/y |
| --- | --- | --- | --- |
| 제목 아래 본문 N-raw L35–36 · N-pdf p1 L21 | `morn` + 줄바꿈 + `ing`, PDF 텍스트는 두 조각 사이에 U+0002가 들어온다 | 관측 구간의 원시 문자열에서 `morning` 연속 검색 실패. 두 조각을 합친 검색 사본에서 성공 | 인쇄면의 하이픈 유무와 실제 위치 미확인 |
| 같은 문장 N-raw L35 · N-pdf p1 L21 | 두 추출문에서 ASCII `Oregonlan`. 기관 페이지의 제목 철자는 Morning Oregonian | raw OCR 페이지에 `Oregonian`으로 검색 도구 find 결과 없음. `Oregonlan`은 L35/L48에 있음. 대상 행에 l→i를 교정한 연구자 검색 사본은 `Oregonian`에 일치 | 기관 제목이 교정 후보를 지지한다. 인쇄된 해당 글리프와 좌표 미확인 |
| 머리말 N-raw L21 · N-pdf p1 L12 | `PORTLAND, OREGON` | 두 추출층에서 정확 검색 일치. 검색 목적의 정규화와 원래 텍스트를 함께 제시해도 이 구절의 선택은 같다 | 두 텍스트층만 대조 |

검색값은 주어진 행의 문자열 비교와 검색 도구의 원시 본문 find다. 기관 검색 인덱스의 어간 처리 여부·적중률은 실행 범위 밖이다. 원면 복원에는 원래 판면의 글자·행 좌표가 필요하다. 검색 사본은 OCR 오류나 줄 분단을 교정할 수 있다. 신문 관측물은 대체 면 raw 1, PDF 텍스트 1, 같은 면의 카탈로그 1, 시각적으로 맞춰 읽은 원면 0/1, ALTO 좌표 0/1이다.

## 음악

R. B. Hall, *Tenth Regiment March*, Garrett Fitzgerald의 Mutopia 2016/12/31-2157 편집판을 읽었다. 1895 Carl Fischer판을 출처로 표기한다. 총보 LilyPond 원전 2개(인쇄용·MIDI용), 별도 파트 원전 4개, 공통 음표 원전 1개를 같은 Git SHA에서 열었다. 인쇄 총보와 위치를 맞추는 기준은 6/8의 시작 마디, 리허설 A 이전이다. LilyPond 2.18.2 파일의 첫 `\relative` 기준과 음정을 적용했고 각 범위는 그 한 마디의 최저·최고음이다. [M-edition](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2157) · [M-lily](https://lilypond.org/doc/v2.24/Documentation/notation/changing-multiple-pitches#transpose)

| m1 성부 | 인쇄 총보·파트에서 읽은 기보 | 실음·마디 내 음역 | 같은 값과 표현 |
| --- | --- | --- | --- |
| Clarinet 1 | 총보 L58–64와 B♭ 파트 L9–25 모두 공통 원전 L339–344의 G5, G♯5. 각각 점4분음표 | MIDI 총보 L33–42의 `\transpose c bes,`는 −2반음. F5, F♯5, 음역 F5–F♯5 | 두 인쇄 경로는 같은 기보, 음고로 비교할 때는 F 계열. 두 경로 모두 6/8과 두 점4분 리듬을 준다 |
| Bass Clarinet | 총보 L82–88와 파트 L9–25 모두 공통 원전 L566–569의 G4, E4 | MIDI 총보 L63–71의 `\transpose c bes,,`는 −14반음. F3, D3, 음역 D3–F3 | 같은 G 글자와 B♭ 계열로도 Clarinet 1과 실음·옥타브가 달라진다 |
| Euphonium · Baritone TC | 총보 L219–223의 bass clef와 Part BC L17–19는 F3, D3. 동편곡 TC 파트 L17–19는 G4, E4 | 공통 원전 L1594–1597, MIDI 총보 L131–135를 적용하면 양쪽 F3, D3. 음역 D3–F3 | 실음·박은 같고 악보의 음자리표·기보음이 달라진다. 연주자가 보는 파트는 사용하는 표기 방식에 따라 달라진다 |

[M-score](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegScore.ly#L58) · [M-midi](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegScoreTransposed.ly#L33) · [M-clar](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegClar1.ly#L9) · [M-bassclar](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegClarBass.ly#L9) · [M-euph-bc](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegBaritoneBC.ly#L9) · [M-euph-tc](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegBaritoneTC.ly#L9) · [M-notes](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/HallRB/TenthRegimentMarch/TenthRegimentMarch-lys/TenthRegiment.ly#L339)

별도 곡인 Lutkin의 *The Lord Bless You and Keep You*에서 성악 악보의 `coun - te -nance`를 붙여 가사 질의 `countenance`에 대응시킬 수 있다. 금관 편집 소스는 해당 가사를 싣지 않고 B♭ 트럼펫 성부와 악기별 기보를 제공한다. 가사 검색의 적합 자료와 금관 연주의 적합 자료가 갈린다. Hall 편집에서 두 점4분음표라는 질문은 B♭ 파트와 해당 총보에서 답이 같다. 화음·조옮김·음역 검산에 MusicXML의 반음 및 옥타브 구분도 확인했다. Hall 음역은 원전 코드에서 계산한 값이며 연주 음원 측정이나 PDF 시각 판독은 하지 않았다. [M-lyrics](https://hymnary.org/media/fetch/95917) · [M-lutkin](https://github.com/MutopiaProject/MutopiaProject/blob/2144afd6f52d56c5b6995b8b589ef1268b3139f0/ftp/LutkinPC/TheLordBlessYou/brass-quartet/brass-quartet.ly#L122) · [M-musicxml](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/transpose/)
