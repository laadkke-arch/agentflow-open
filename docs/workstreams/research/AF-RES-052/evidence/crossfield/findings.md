# Q6 · 이름과 특정 구현을 구별하는 다른 분야 대조

## 조사 범위와 수용 배당

이 파일의 사례는 소프트웨어 자연층·보강층의 8자리, 승격·손실 수, 두 번 열람의 성공률에 넣지 않는다. 녹음의 개별 보존기관 레코드 2개(X01–X02), 서체 발행자의 고정 판별 사용설명서 2개(X03–X04)에만 필수 4개 배당을 준다. HTML/XML은 같은 저작으로 합쳤다. X05–X11은 별도 직접 읽은 보조 자료지만 최소 배당을 부풀리는 데 쓰지 않았다. 실패 XF01–XF05는 직접 원문 수에서 제외한다. 모든 파일은 이 연구의 owned_path 안에만 작성했고 설치·계정 변경·글꼴 실행·녹음 재생은 하지 않았다.

## 녹음 · 같은 곡과 다른 연주는 다른 레코드다

| 원장 ID | 개별 원본 레코드 | 곡과 특정 연주 식별 | 직접 확인한 범위 | 한계 |
| --- | --- | --- | --- | --- |
| X01 / X01M | [UNT Women's Chorus, 1999-12-02](https://digital.library.unt.edu/ark:/67531/metadc84597/) | Foster의 Beautiful Dreamer, track14, 2:56; Women's Chorus; ARK metadc84597; local control 12_02_1999 Women's Chorus | 제목·트랙·연주자·날짜·ARK와 XML 식별 필드. XML lines3–6,49–56,67,77,80–82 | 녹음 미청취. item access=unt. 편곡·악보가 같은지는 미확인 |
| X02 / X02M | [UNT Rinaldi baritone, 2010-01-23](https://digital.library.unt.edu/ark:/67531/metadc89020/) | Foster의 Beautiful Dreamer, track1, 2:41; Joseph W. Rinaldi; Foster 곡에 guitar 기재; ARK metadc89020; local control 01_23_10 Rinaldi | 개별 카탈로그와 XML lines3–6,18,41–43,89,108,111. 연결된 [원 공연 프로그램 p201](https://digital.library.unt.edu/ark:/67531/metadc79476/m1/203/)도 날짜·곡·연주자를 확인(X10) | 녹음 미청취. XML item access=public이나 collection 공통문구에는 접근 제한이 나온다. 재생 실패를 관측한 것으로 쓰지 않는다 |

**확인된 사실:** 두 레코드는 같은 Foster 곡명 아래 서로 다른 연주자·날짜·트랙 길이·영구 식별자를 갖는다. 원문을 통해 식별한 차이이며 음향 비교로 판정한 차이는 아니다. 곡명 검색에는 두 레코드를 하나의 작품 아래 둘 수 있다. '1999년 여성 합창의 그 연주' 또는 '2010년 바리톤과 기타 연주'를 요청하면 대표 목적지가 달라져야 한다. 같은 곡명이거나 같은 보존기관이라는 이유로 한 레코드를 다른 레코드의 증거로 사용하면 요청의 연주 조건이 사라진다.

**반대 방향의 한계:** 공연 차이가 있다고 무조건 별개 곡으로 세면 작품 검색을 과도하게 나눈다. 곡·작곡자 수준의 관련성과 연주·발행물 수준의 동일성은 서로 다른 질문이다. X01의 편곡 표기에는 추가 확인이 필요하므로 '같은 편곡'까지 결론을 확장하지 않는다.

## 서체 · Inter라는 공개 이름은 축 계약을 고정하지 않는다

| 원장 ID | 발행자의 고정 판 | 판별 확인 사항 | 대표를 고를 때 잃으면 안 되는 조건 |
| --- | --- | --- | --- |
| X03 (+X05) | [Inter v3.19, variable.txt](https://github.com/rsms/inter/blob/5fa70f6e8c0ecad97544e19aba2d5062aa8c3e7a/misc/dist/variable.txt#L2-L16) | complete multiaxis Inter / Inter V와 weight만 가변이고 slant는 가변이 아닌 single-axis 배포를 구분한다. Inter와 Inter V의 차이는 family name뿐이라고 명시한다 | v3.19라는 판만으로도 부족하다. slant가 필요한 사용자는 multiaxis flavor까지 지정해야 한다 |
| X04 (+X06) | [Inter v4.0, help.txt](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/help.txt#L13-L44) | variable weight·optical size, 정적 혼합, 별도 upright/italic 파일을 설명한다. [v4.0 발행기록](https://github.com/rsms/inter/releases/tag/v4.0)은 3.x 대비 opsz의 추가와 업그레이드 시 달라지는 모습을 설명한다 | opsz를 쓰는 사용자 문서는 v4의 파일·CSS를 가리켜야 한다. 공개 이름 'Inter'만으로 v3 가변 설명을 대신할 수 없다 |

X05의 공식 v3.19 발행일은 2021-06-18T21:27:50Z, X06의 v4.0 발행일은 2023-11-20T00:11:13Z다. 각 태그는 위 40자리 SHA로 따로 고정했다. 발행기록 본문은 수정될 수 있어 최초 발행 당시의 문장이라고 주장하지 않는다.

**확인된 사실:** 축 지원과 패키지 구성이 판·flavor에 따라 다르다는 발행자의 문서를 직접 읽었다. exact installed family name은 v3의 Inter/Inter V와 v4의 Inter Variable/InterVariable처럼 다르므로 '동일 이름'은 공개 family brand인 Inter 수준이다. 문자 그대로 동일한 내부 폰트 이름이라고 쓰면 안 된다. X09의 [발행자 v4 beta1 발표](https://github.com/rsms/inter/discussions/493)는 opsz 추가와 slnt 제거를 명시하지만, beta 설명을 안정판 바이너리 검사 결과로 바꾸지 않는다. 안정판 파일의 fvar 테이블과 실제 브라우저 동작은 미검사다.

**단순 분할의 반례:** X03은 한 원문에서 다축·단축 flavor와 이름만 다른 Inter V를 함께 설명한다. 이름이 다른 Inter와 Inter V를 독립 구현 둘로 세는 것도 오류다. '각 문서가 한 구현만 설명한다'는 가정 없이 도착 절의 실제 정보 단위를 보아야 한다. 판과 파일이 명시되면 엄격한 C는 v3와 v4를 서로 합치지 않아야 하며, 이 사례는 C가 실제 실패했다는 관측이 아니다.

## 독자 목적에 따른 반환 단위

| 독자·목적 | 충분할 수 있는 대표 | 특정 조건이 붙었을 때 필요한 반환 | 이름 하나로 묶을 때 손상되는 것 |
| --- | --- | --- | --- |
| 설계자: 어떤 사용 가능한 부품·작품이라도 찾기 | 작품·family 개요와 구별 가능한 개별 멤버 | 녹음은 연주자·날짜·트랙; 서체는 판·축·배포 flavor가 있는 멤버 | 독립 대안을 이름 개수로 과대·과소 계수할 수 있음 |
| 사용자 문서 작성자: 이 판에서 이 기능을 쓰는 법 | 해당 판의 사용설명서 | Inter v4 opsz 예제와 같은 판의 CSS/파일 이름; v3.19 slant 요청은 multiaxis 문서 | 최신 이름으로 연결해 옛 판의 설정이 유효하다고 오해할 수 있음 |
| 패키지 유지보수자: 두 부품·파일을 함께 배포하기 | 버전 고정된 설치·통합 절 묶음 | v4 upright/italic 파일과 대응 CSS, 또는 v3 Inter/Inter V의 동시 설치 목적 | 별칭을 새 구현으로 세거나 필요한 두 파일을 대체 가능한 하나로 축소함 |

위는 이 사례에서 도출한 **조건부 제안**이다. 독자가 실제로 선택한 수와 사용성 효과를 측정하지 않았다.

## 반환 카드 예시

- **원문 한 개:** [Inter v3.19 variable 안내](https://github.com/rsms/inter/blob/5fa70f6e8c0ecad97544e19aba2d5062aa8c3e7a/misc/dist/variable.txt#L2-L16) — 한 페이지에서 multiaxis / weight-only / family-name alias를 비교; v4 optical-size 사용법을 요청하면 이 카드만으로 부족.
- **보완 절 묶음:** [Inter v4 설치·파일](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/help.txt#L13-L44) + [같은 판 CSS](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/inter.css#L1-L20) — 광학 크기와 upright/italic 통합; 실제 브라우저·정확한 바이너리 축까지 보증하지 않음.
- **서로 다른 실현 둘:** [1999 Women's Chorus track14](https://digital.library.unt.edu/ark:/67531/metadc84597/) + [2010 Rinaldi track1](https://digital.library.unt.edu/ark:/67531/metadc89020/) — 같은 Foster 곡의 다른 연주 레코드; 같은 편곡·음질·접근 가능성까지 요구하면 추가 확인 필요.

## 원문 재열람 및 재개

`sources.jsonl`에는 질문·발행자·저작 ID·배당·URL·확인 UTC·SHA/절/행·확인 내용·한계·반증/미확인·중복 관계가 있다. `retrieval-receipts.jsonl`과 `font-receipts.jsonl`에는 HTTP200, 바이트 수, SHA256 및 원래 행 위치를 보존했다. 녹음 HTML/XML은 각 한 저작, 같은 폰트 설명서의 fragment도 한 저작이다. 실패한 LOC/Smithsonian 탐색은 성공 자료로 바꾸지 않았다.

다음 최소 확인은 (1) 정확한 음향·편곡이 요구되면 해당 공연의 승인된 녹음·악보를 비교, (2) 정확한 축 계약이 요구되면 고정 v3.19/v4.0 배포 파일의 fvar 표를 읽기다. 이 두 추가 확인 전에도 서로 다른 개별 레코드·판을 이름 하나의 근거로 대체할 수 없다는 범위의 결론은 지지된다.
