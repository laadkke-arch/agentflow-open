# AF-RES-040 Q6·Q7 — 타 분야 식별과 보조 반례

## 범위와 판독 성격

사전 계약 `SCOPE.md`를 읽은 뒤 수행한 보조 조사다. **주 표본 8건의 후보 순위·적격 분모에 이 사례를 삽입하지 않는다.** 문서·운영 레코드를 읽어 관계를 판독했으며 음원을 듣거나 소프트웨어를 교체·실행하지 않았다. 같은 세션 계열의 내부 조사자 한 명이 작성했다. 실제 사용자 효용·독립 사람 판독은 미확인이다.

`sources-X.jsonl`은 직접 열람 고유 원문 **23개**를 산입한다. 도서관 5, 음악 11, 소프트웨어 동일성/배포/비호환 기록 4, 공급자 문서 3개다. 별도 10행은 접근 실패·조회 결과 미확인·보조 운영 검색 화면·범위 밖 원문으로 제외했다. 같은 문서의 반복 조회는 새 원문으로 세지 않았다. `checked_utc`는 원문 판독을 마치고 해당 사실·한계를 원장에 확인해 기록한 시각이다. 원 요청 HTTP 시각이라고 주장하지 않는다.

## 1. 서로 다른 구분을 같은 이름으로 옮기면 생기는 오류

| 원문·구체 레코드 | 관측한 관계 | 소비자가 구별해야 하는 목적 | 소프트웨어로 옮길 때의 한계 |
| --- | --- | --- | --- |
| [IFLA LRM 2017-12](https://www.ifla.org/wp-content/uploads/2019/05/assets/cataloguing/frbr-lrm/ifla-lrm-august-2017_rev201712.pdf), LRM-E3 pp.23–25; §5.2 p.87 — X-L01 | 저작의 표현과 구현·소장본을 구분한다. 같은 표현을 얼마나 잘게 구별할지는 목적과 식별 가능성에 좌우된다. | 작품을 찾는 목적과 특정 번역·표현을 찾는 목적이 다르다. | software project→work라는 고정 대응은 가설이다. 같은 프로젝트 안의 독립 호출, 여러 프로젝트의 같은 규격 구현에는 별도 관계가 필요하다. |
| [LoC BIBFRAME 모델](https://www.loc.gov/bibframe/docs/bibframe2-model.html), Work/Instance/Item; [2019 운영 매뉴얼](https://www.loc.gov/catworkshop/bibframe/Training/Bf2.0/2019/bf-2019-3.html), Unit6 — X-L02·03 | BIBFRAME의 Work는 언어 등도 담고, 매뉴얼은 RDA Work와 Expression의 대응을 설명한다. | 어떤 기술 층에서 같은 자료를 찾고 연결하는지 알아야 한다. | 두 분야가 `Work`라는 같은 필드명을 사용해도 의미 단위가 같다고 합칠 수 없다. |
| [Illinois 1813년판](https://exhibits.library.illinois.edu/s/rbml/item/1104), Descriptive Information; [Yale 1813·1832년판 쌍](https://onlineexhibits.library.yale.edu/s/publication-and-prejudice/item/13314), Identifier/Source — X-L04·05 | Yale는 *Pride and Prejudice*와 *Elizabeth Bennet: or, Pride and Prejudice*를 발행 연도·발행처와 함께 한 URL에 기록한다. | 작품명 탐색에는 묶음이 유용하지만 특정 판·소장본을 찾는 사람에게는 연도·식별자가 필요하다. | 한 URL이 여러 판을 설명한다. URL 수를 부품 수 또는 배포판 수로 쓰면 틀린다. 두 판의 전체 본문 동일성은 이번에 검증하지 않았다. |
| [MusicBrainz Recording](https://musicbrainz.org/doc/Recording), Definition/Examples — X-M01 | 한 녹음에 여러 발매 track이 연결되고 원녹음과 remix는 별도 녹음으로 관리한다. | 곡의 작곡자, 특정 음향 버전, 특정 발매를 찾는 목적이 갈린다. | 동일 용도만으로 구현을 합칠 수 없다. 목적상 대체 가능성과 동일 구현이라는 관계를 따로 둬야 한다. |

LRM의 구분을 그대로 채택할 필요는 없다. 이 자료들에서 가져올 수 있는 원칙은 **식별자가 속한 층과 소비자 목적을 함께 명시하라**는 것이다. 반대로 도서관의 `판`을 소프트웨어 버전 문자열 하나로 옮기면 ABI, 빌드 옵션, 입력 wrapper, 읽기/쓰기 방향을 놓친다. 이는 이번 조사자의 적용 추론이며 도서관 문서가 소프트웨어 계약을 정의한 것은 아니다.

## 2. 음악의 같은 표기·다른 표기 반례

| 판단 대상 | 직접 읽은 실제 레코드와 위치 | 판단·보존할 구분 |
| --- | --- | --- |
| **다른 표기, 같은 녹음** | [Beatmasters remix recording](https://musicbrainz.org/recording/023b1e14-0e7e-4dc1-9ab4-9ef4f0e70ce0)의 Appears on releases: `Beatmaster mix`, `Beatmasters mix`, 대소문자가 다른 표기가 같은 MBID에 연결된다. — X-M05, lines75–93 | 표기만으로 별도 결과를 만들면 같은 녹음을 반복할 수 있다. 특정 발매를 선택할 때에는 발매 식별자·날짜·track을 남겨야 한다. 음향 동일성을 독립 확인한 결과가 아니라 카탈로그가 그렇게 연결한 사실이다. |
| **같은 작품, 다른 녹음·리믹스** | [Into the Blue work](https://musicbrainz.org/work/adfdfa6c-fa04-3571-aa2c-a13a99e64e96)의 Recordings에 [원녹음](https://musicbrainz.org/recording/9ce76fe1-769f-481a-afbb-3b9b81c6f433)과 위 remix가 별도 MBID로 연결된다. — X-M04·05·06 | 특정 remix를 요구하는 소비자에게 작품 하나의 최초 녹음을 대표로 주면 필요한 버전을 숨긴다. 작품의 저자만 필요하면 작품 대표로 충분할 수 있다. |
| **한 발매, 여러 버전** | [Into the Blue release](https://musicbrainz.org/release/0e99c968-f511-4d74-9650-1c1a06de79b2)의 Tracklist에 Beatmasters mix와 Sound Factory mix가 별도 track으로 나온다. — X-M07, lines70–105 | 발매 단위가 녹음 단위를 대신하지도 않는다. 공급자·패키지 단위로 묶었을 때 내부 기능을 숨기는 경우의 유사 사례다. |

[공식 Recording 제목 지침](https://musicbrainz.org/doc/Style/Recording)의 Title 절은 실제 track들의 표기를 대표 제목 선정에 사용한다(X-M02). 이 절 이후 조회는 429였기 때문에, 열람하지 못한 절의 내용을 독립 근거로 사용하지 않았다. *Hallelujah*·Britney Spears 후보는 원 관계를 충분히 얻지 못해 제외했고, 이미 읽은 공식 Recording 문서가 직접 링크한 Moby 예로 이동했다. 표본을 주 분석에 끼워 넣지 않은 보조 사례 탐색이다.

## 3. 제공자·소비자·편집자는 다른 손실을 본다

| 관점 | 필요한 구분 | 이번 직접 근거 | 남은 미확인 |
| --- | --- | --- | --- |
| 제공자·식별자 관리자 | 같은 엔터티의 중복 참조를 줄이되, 별개 층의 관계를 보존한다. | LoC 운영 매뉴얼 Unit8은 기존 Work/Instance 존재 여부에 따라 새 Instance 연결과 추가 사본을 구별한다. MusicBrainz [Merge](https://musicbrainz.org/doc/Merge)는 같은 타입의 엔터티를 합치고 참조를 target으로 보낸다. — X-L03·X-M08 | 두 운영체제의 전체 데이터 오류율과 자동 중복 탐지 성능 |
| 소비자 | 원하는 표현·녹음·발매·설정이 처음부터 구별돼야 한다. | 1813/1832 서지 쌍과 원녹음/remix 레코드 쌍. — X-L04·05·X-M04–07 | 실제 검색 이용자가 한 화면에서 선택하는 시간·정확도 |
| 편집자 | 원 member, 관계, 필드 귀속과 정정 이유를 복원해야 한다. | [오귀속 정리 사건](https://community.metabrainz.org/t/unmerging-recording/713181) posts1–4와 [잘못 붙은 track을 먼저 분리하라는 토론](https://community.metabrainz.org/t/best-way-to-handle-a-recording-that-should-be-merged-but-contains-wrong-tracks-as-well/683297) posts6–9. — X-M10·11 | 모든 정정이 완료됐는지, 소요 시간, 자동 unmerge의 일반적 부재 여부 |

MusicBrainz의 Merge 안내는 충돌 필드에서 target 값을 유지하고 참조를 그쪽으로 돌린다고 명시한다. [녹음 병합 안내](https://musicbrainz.org/doc/How_To_Merge_Recordings)는 대표의 기본 정보와 다른 녹음의 식별자·발매 연결이 합쳐지는 방식을 설명한다(X-M03·08). 두 페이지에는 문서팀 미검토 표시가 있으므로 이를 구현 전체에 대한 검증으로 확대하지 않았다.

오귀속 사건의 편집자는 원래 *La Groupie du pianiste*였던 녹음에 다른 track이 붙었다고 보고했다. 연결된 운영 검색 원장에서 edit `115752742`의 이름 교정과 종료 시각은 확인했다(X-M12). 개별 edit 페이지는 열리지 않아 **전체 분리 복원 성공은 미확인**으로 남겼다. 다른 토론에서는 track 재연결 뒤에도 ISRC·관계·AcoustID가 잘못 귀속됐는지 따로 확인하라고 설명한다. 명칭이 같은 `track`도 MusicBrainz와 AcoustID에서 같은 객체를 뜻하지 않는다는 반론이 나온다(X-M11). 이 부분 역시 해당 편집자들의 1차 토론 기록이지 모든 사건에 대한 정량 검정은 아니다.

## 4. 소프트웨어 보조 반례: 같은 키가 충분한 범위와 깨지는 경계

`stress.jsonl`의 XT1–XT7은 아래 조건을 기계적으로 다시 읽을 수 있도록 주소·부품·판·양 방향·미확인으로 나눈 원장이다. 방향 `left_to_right`는 **left를 쓰던 소비자가 명시된 같은 목적에서 right로 교체할 수 있는가**를 뜻한다.

| 보조 사례 | 원문·절 | 확인된 구분 | 반대 조건·미확인 |
| --- | --- | --- | --- |
| XT1: 하나의 URL에 PNG 읽기·쓰기 | [Cairo 1.12.4 PNG Support](https://www.cairographics.org/manual-1.12.4/cairo-PNG-Support.html), Synopsis와 개별 호출 — X-T03 | 같은 원문에 반대 방향 함수가 있다. URL 하나가 부품 하나가 아니다. 원문 전체를 볼 수 있으면 한 링크로 양쪽 근거를 보존할 수도 있다. | 대표가 특정 절만 보여 주는 UI라면 다른 방향을 놓칠 수 있다. 실제 UI/클릭은 시험하지 않았다. |
| XT2: 같은 상류의 다른 출력 | 위 PNG Support와 [PDF Surfaces](https://www.cairographics.org/manual-1.12.4/cairo-PDF-Surfaces.html), Description/판 제한 — X-T03·04 | PNG 출력과 여러 페이지 PDF 벡터 출력은 요구 형식·호출 순서가 다르다. PDF 문서는 읽기 기능을 입증하지 않는다. | 도구명만 필요한 목적에는 Cairo 한 묶음도 충분하다. 실제 빌드의 backend 포함 여부는 미확인이다. |
| XT3: 다른 구현의 제한된 공통 계약 | [libjpeg-turbo 3.1.3 README](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/af9c1c268520a29adf98cad5138dafe612b3d318/README.md), Using/Mathematical Compatibility — X-T01 | 공급자는 v6b API/ABI 호환을 선언한다. 공통 API 범위로 요구를 고정하면 별개 구현을 대안으로 비교할 근거가 된다. | **무조건 완전 대체는 입증하지 못했다.** IJG 원판·소비 바이너리 실행은 하지 않았다. 4:4:0·floating DCT 출력 예외와 빌드·runtime 조건을 포함하면 판정이 달라진다. |
| XT4: 한 방향만 성립하는 확장 | 같은 README의 Colorspace Extensions/In-Memory Managers — X-T01; [Official Binaries](https://libjpeg-turbo.org/Documentation/OfficialBinaries), Included Features — X-T07 | 기존 v6b 호출에서 확장 구현으로 가는 조건부 대체와, 확장 호출을 쓰는 소비자가 기존 구현으로 되돌아가는 경우가 다르다. | 비지원 colorspace에는 오류가 명시돼 있다. 확장 미사용 소비자로 범위를 좁히면 역방향 판정도 조건부로 돌아올 수 있다. |
| XT5·XT6: fork와 빌드 모드 | [zlib-ng 2.2.4 PORTING](https://github.com/zlib-ng/zlib-ng/blob/860e4cff7917d93f54f5d7f0bc1d0e8b1a3cb988/PORTING.md), compat/native 및 Changes from zlib — X-T02 | 같은 프로젝트에서도 native와 compat의 헤더·symbol·연결이 다르다. fork는 할당 메모리와 압축 스트림이 달라질 수 있다. | 같은 압축 목적이어도 정확한 출력 길이·고정 allocator 예산을 요구하면 교체에 실패한다. 문서상의 설명이며 실행 결과가 아니다. |
| XT7: 프로젝트명과 API명이 겹침 | [libjpeg-turbo의 이름 설명](https://www.libjpeg-turbo.org/About/TurboJPEG), 본문 — X-T06 | TurboJPEG는 API이고 libjpeg-turbo는 프로젝트다. 과거 다른 기반의 TurboJPEG 구현도 있었다고 공식 설명이 명시한다. | 해당 과거 구현은 비활성이라고 적혀 있어 오늘 쓸 수 있는 대안으로 집계하지 않는다. |

[zlib 공식 매뉴얼](https://zlib.net/manual.html)은 열람 시 1.4판이었고 zlib wrapper·gzip·raw deflate를 구분했다(X-T05). **이 판을 zlib-ng 2.2.4 이식 문서의 검증된 호환 상대라고 추정하지 않는다.** 이 시간 차이는 두 링크를 이름만으로 같은 판의 같은 계약이라고 묶으면 생기는 또 다른 한계다.

## 5. 되돌릴 수 있는 표시 묶음에 대한 조건부 제안

아래는 원문에서 확인한 사실에 기초한 적용 가설이다. 최종 제품 저장 구조를 확정하지 않는다.

| 보관안 | 충분할 수 있는 조건 | 부족해지는 조건 |
| --- | --- | --- |
| 원 URL과 원 순서만 보존 | 원문이 안정적이고 한 URL의 여러 기능을 다시 읽을 수 있으며, 표시 묶음이 원본을 수정하지 않는다. XT1처럼 문서 전체가 필요한 방향 둘을 함께 제공한다. | URL의 같은 판·다른 용도·증거 역할을 다시 추론해야 할 때. 추가 조회 없이 이전 판정을 재현해야 할 때. |
| 원 member와 부품·용도·판·근거 역할 보존 | 표시 그룹을 해제해 원 후보와 판독 범위를 다시 나눌 필요가 있다. 대표·숨김 이유·규칙 판도 같이 남긴다. | 별도 구현 사이 대체를 동등 그룹으로 저장하면 방향·조건을 잃는다. XT3·4처럼 교체 계약이 비대칭인 경우가 남는다. |
| 방향과 조건이 붙은 관계까지 보존 | 상류·fork·wrapper·규격 구현을 비교하고, 같은 원문이 여러 주장에 사용된다. | 정교한 관계를 만들었다는 사실만으로 사용자 가치나 판독 재현성이 검증되는 것은 아니다. 작성·유지 부담은 이번에 측정하지 않았다. |

오병합 해제는 두 수준을 구별해야 한다. **표시만 묶고 원 member를 유지했다면** 이전 후보 목록과 순서는 재생성할 수 있다. 그러나 target 속성을 덮고 관계를 옮기는 **원자료 병합까지 했다면**, URL 목록만으로 각 속성의 이전 귀속을 복원할 수 있다는 보장이 없다. MusicBrainz의 실제 정정 논의가 후자의 위험을 보여 준다. AF-RES-040은 전자의 표시 비교이므로 후자의 복구 비용을 이 작업의 사용자 비용으로 계산하지 않는다.

## 6. 반증 경로와 남은 공백

단순 묶음이 유리한 반례를 의도적으로 확인했다. 작품의 저자만 필요한 소비자는 work 대표가 충분할 수 있고, PNG 읽기·쓰기 모두 같은 문서에 있으면 URL 하나가 근거 둘을 제공한다. 반대로 정교한 구분도 필요 없는 기능·비활성 구현까지 첫 화면에 남기면 자리를 소모한다. 이는 보조 사례의 조건부 해석이며 주 표본에 효과 수치를 더하지 않는다.

| 미확인·약점 | 영향받는 판단 | 다음 최소 확인 |
| --- | --- | --- |
| XT3의 무조건 완전 대체는 없음: 공급자의 범위 제한 선언만 확인했다. | 다른 공급자라는 이유만으로 대체 불가라고 할 수는 없지만, 전역 동등성도 승인할 수 없다. | 고정 IJG v6b 원문과 소비자의 실제 호출·빌드·입력 조건을 먼저 읽고, 문서 범위 밖 요구가 없는지 확인한다. 실제 실행은 별도 지정 입력으로 한다. |
| MusicBrainz 카탈로그 연결을 음향 동등성과 동일시할 수 없다. | XM1의 같은 녹음 판정은 카탈로그 관측 범위에만 유효하다. | 동일 track 쌍의 공개적으로 이용 가능한 원 음원 또는 운영자가 남긴 동일성 증거를 대조한다. |
| edit 원장은 한 이름 정정만 확인했다. 전체 split 성공은 미확인이다. | 원자료 병합에서 복구가 필요하다는 근거는 있으나 복원율·소요 비용을 주장할 수 없다. | MusicBrainz edit115752742와 사건의 split 편집들 각각의 old/new 관계를 다시 읽는다. |

접근 실패·대체 경로는 `access-log.jsonl`과 sources의 X-F01–08, X-M12, X-T08에 남겼다. 저작권 보호 자료의 본문을 대량 복제하지 않았고, 필요한 사실·위치와 제한만 요약했다.
