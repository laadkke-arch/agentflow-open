# AF-RES-023 — 병합·별칭·병렬 후보의 적용 경계

이 문서는 제품 DB나 최종 ID 체계를 정하지 않는다. 실제 편집에서 관측한 단위를 기준으로 세 선택의 전제와 실패 조건을 비교한다. 원 카탈로그의 승인, 외부 발급자의 식별 범위, 과거 인용의 의미, 추천 코드의 기능·판 요구를 서로 대신하지 않는다.

| 선택지 | 성립하는 전제 | 실제 반례 | 관측한 유지·이관 단위 | 보류할 부분 |
| --- | --- | --- | --- | --- |
| 엄격 병합 | 같은 층위의 실체를 중복 등록했고, 보존할 판·외부 ID·관계를 구별할 근거가 있다. | MB01은 같은 DiscID여도 지역·matrix가 다른 release였다. WD01의 category와 institution은 건물의 P910 목적에서 대체할 수 없다. | MB05는 누락 트랙 보완 편집48434703과 release 병합48447069를 따로 수행. WD01은 본체undo1048159568 외에 consumer undo1048159950이 필요했다. | 승인된 병합도 음원 동일성·외부 소비자 전체 복구를 증명하지 않는다. |
| 가역 별칭·옛 ID 보존 | 같은 범위의 대상을 찾는 이름만 바뀌거나, 폐기 record에서 해석 가능한 대표 하나로 연결한다. 적용시점과 별칭을 따라도 되는 목적을 알려야 한다. | SW03은 같은 GNU readline이어도 canonical keg 처리 때문에 rename을 되돌렸다. SW05에서 postgresql→@14는 Rails의 나중 최신판 목적을 만족시키지 못했다. | SW02 rename map 1행과 전후 fixed recipe, SW01 삭제 recipe와 alias 및 surviving recipe. exact build를 요구하면 이전 blob을 추가 유지. | alias의 현재 실행 성공을 이번 연구에서 brew 설치로 확인하지 않았다. ROR의 successor 관계를 HTTP redirect라고 부르지 않는다. |
| 관련 후보 병렬 표시 | 하나에서 여러 후계가 나왔거나 서로 다른 층위·프로젝트라서 사용 목적이 있어야 선택할 수 있다. 후보의 역할을 함께 표시한다. | 모든 이름 차이를 별개로 두면 SW01의 같은 tf-50b8 배포물, MB05의 누락 트랙 중복을 남긴다. | ROR05는 옛 기관1+후계4 관계, SW06은 library와 CLI 두 recipe 및 소비자별 필요판. 포크 SW-F01은 원 프로젝트와 포크 두 formula를 같은 tree에 유지. | 후보를 늘리는 것만으로 정답을 고르지 못한다. ROR05의 특정 학과·프로그램, 소프트웨어의 명령/ABI·판 요구가 추가 입력이다. |

근거: [MB01 원병합151147443](https://musicbrainz.org/edit/151147443), [MB05 이력](https://musicbrainz.org/release/633a31aa-ed97-49fc-ab70-27f8e97fc5be/edits), [WD01 본체undo](https://www.wikidata.org/w/index.php?diff=1048159568&oldid=1038289881&title=Q59165607&type=revision), [별도 consumer 복구판](https://www.wikidata.org/w/index.php?oldid=1048159950&title=Q314104), [SW03 revert](https://github.com/Homebrew/homebrew-core/commit/8c2998215320942b1329f5b073fad7bfa33e9976), [SW05 실제 소비자 수정](https://github.com/rails/rails/commit/27cb8c618ca3a96a2817e412bfe48dc29a6acfa3), [ROR05 changed record](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v1.67/updates/01sxmzj91.json), [SW06 split](https://github.com/Homebrew/homebrew-core/commit/e5e819e64a3104cabb55d46ea8e80d69aaf76d5b).

## 쌍 A — 음악의 work/recording/release와 소프트웨어의 프로젝트/배포물/기능

**같은 작품은 같은 녹음물이 아니다.** MB03의 `07`은 원 병합60587125가 적용된 뒤, 오케스트라판 2:32와 `Интервью` B4의 비오케스트라판 2:38을 다시 분리했다. medium 참조를 새 recording으로 바꾸는63762772와 work 관계를 붙이는63972905는 서로 다른 변경이다. 음악적 차이는 복구자의 진술이고 이번 연구의 음원 비교가 아니다. 같은 work를 참조하는 두 recording을 합칠 권한은 노래 제목의 일치에서 나오지 않는다. [MB-S11–15, 원병합](https://musicbrainz.org/edit/60587125) · [후속 이력](https://musicbrainz.org/release/5aeb8c8f-cd6a-4d43-97e5-fb86b9b35695/edits).

**같은 upstream 버전도 같은 설치 기능 묶음은 아니다.** SW06은 tree-sitter upstream0.25.8을 유지하면서 Homebrew 배포 범위를 library와 CLI로 나눴다. old formula가 계속200이어도 `generate` 명령을 제공하지 않는다. 이는 새 프로젝트 포크가 아니라 같은 프로젝트의 패키징 분리다. 반면 보충 SW-F01에서는 새 yt-dlp formula가 같은 tree의 youtube-dl과 병렬 존재하며, 고정 upstream README가 파일명·format 정렬·오류처리 기본값 차이를 설명한다. 넓은 목적이 동영상 다운로드라는 사실은 결과·실패처리를 동일하게 만들지 않는다. [SW-S14](https://github.com/Homebrew/homebrew-core/commit/e5e819e64a3104cabb55d46ea8e80d69aaf76d5b) · [SW-FS01](https://github.com/Homebrew/homebrew-core/commit/3e32b083e96a38b8bd09b3516898e77dc05bd518) · [SW-FS03, README19·119–129행](https://github.com/yt-dlp/yt-dlp/blob/418964fa91b1c44e8f6e5fc323932f952cd558b7/README.md).

| 관점 | 음악 사건에서의 질문 | 소프트웨어 사건에서의 질문 |
| --- | --- | --- |
| 원 카탈로그 편집자 | recording 동일성 판단과 release의 지역·matrix 경계를 어느 편집으로 반영했는가? | formula의 이름·설치 산출물·의존성이 어떻게 바뀌었는가? upstream fork와 package split을 구별했는가? |
| 원 식별자 발급자 | MBID가 식별하는 catalog 층을 보존했는가? ISRC/DiscID가 같은 release를 보장한다고 오해하지 않았는가? | formula명·upstream tag·archive hash·실행파일은 서로 어떤 범위인가? ROR나 MBID의 영속 보장을 formula명에 이식할 수 있는가? |
| 옛 인용을 읽는 사람 | `07`의 어느 녹음/판을 골랐던가? 새 녹음 ID로 원 ID까지 복원됐는가? | 옛 링크가 library를 설명해도 내가 원한 generate 명령과 과거판을 찾을 수 있는가? |
| 추천 이유를 판에 묶은 개발자 | 추천 이유에 recording·release·근거 edit를 따로 남겨야 하는가? | CLI 기능과0.25.x 요구를 묶어야 하는가? 정상 rename의 경우에도 exact recipe가 필요한가? |

MB04의 허용 recording 병합과 SW01의 중복 recipe 정리는 반대 방향의 반례다. 다른 release/표기마다 무조건 분리하면 동일 recording의 공유와 동일 archive의 중복을 놓친다. MB04의 source ID provenance와 SW01의 archive bytes 동등성 검사는 미확인이므로, 이 두 사건을 모든 병합의 정당화로 확장하지 않는다. [MB-S17](https://musicbrainz.org/edit/68967621) · [SW-S01](https://github.com/Homebrew/homebrew-core/commit/7f379ed5e4135654176204310ae0f24af0826eaa).

## 쌍 B — 연구기관의 법적/조직 승계와 지식베이스의 참조 역할

ROR01 COMTES는 현실 회사 합병이 아니라 같은 회사의 두 record를 정리한 사건이다. 반대로 ROR-X1은 대학 공식 원문이 PPS와 LIAFA의2016-01-01 합병으로 IRIF가 생겼다고 설명하고, ROR는2026-10-30 요청·11-19 changed record·11-20 release댓글에서 PPS inactive와 IRIF successor를 반영했다. **현실의 조직 변경일, catalog 수정일, 소비자 인용일은 세 날짜**다. 그 사이 모든 중간 판을 확인한 것은 아니다. [ROR-S03](https://github.com/ror-community/ror-updates/issues/15331) · [대학 원문 Recherche136–147행](https://www.informatique.u-paris.fr/ufr/presentation_ufr) · [ROR-X01](https://github.com/ror-community/ror-updates/issues/43488).

ROR02에서 본부와 Pacific Islands Division을 모두 같은 기관으로 묶자는 제안은 소속 인용 단위가 다르다는 이유로 기각됐다. ROR06에서는 같은 대학 브랜드라도 본교와 SLP 캠퍼스의 ID를 다시 나누었다. 이를 WD01의 building/institution/category와 비교하면, 모두 이름의 유사성보다 **그 인용의 관계 자리**가 중요하다. 다만 연구기관의 본부/지부는 현실의 조직 관계이고 Wikidata category는 그 주제를 모으는 지식 표현이다. 지부가 본부에 속한다는 관계와 category가 기관을 주제로 삼는 관계를 같은 후계 edge로 옮기면 안 된다. [ROR-S09, 기각댓글](https://github.com/ror-community/ror-updates/issues/13495#issuecomment-2457897274) · [ROR-S23](https://github.com/ror-community/ror-updates/issues/25805) · [WD-S05](https://www.wikidata.org/w/index.php?diff=1038289881&oldid=986442520&title=Q59165607&type=revision).

| 관점 | ROR의 실제 경계 | Wikidata의 실제 경계 |
| --- | --- | --- |
| 편집자 권한 | 큐레이터는 ROR record를 수정한다. 실제 법적 승계·정부 개명을 창설하지 않는다. | 편집자는 item과 statement를 변경한다. 현실 건물과 기관의 동일성을 투표/merge 도구가 만들어 주지 않는다. |
| ID 발급 범위 | 역사적 조직 ID와 상태를 보존하며 successor가 복수일 수 있다. changed JSON만으로 live API의 동작을 보증하지 않는다. | QID는 item을 가리키며 redirect가 참조의 타입까지 보존하지 않는다. Help:Merge/Redirects는 열람 당시 제안 지침이었다. |
| 소비자 | 과거 소속은 inactive 기관의 인용으로 여전히 맞을 수 있다. 현재 문의처는 목적에 따라 달라진다. | 건물P910은 main category를 요구한다. 기관 item으로 자동치환되면 URL이 살아도 typed relation이 틀린다. |
| 개발자 | 변경 통지를 받아도 이름·위치·부모·외부 ID·인용을 항목별 대조해야 한다. ROR07은 위치가 남았다. | 본체undo 후 incoming relation을 따로 복구해야 한다. WD01에서 그 별도편집1건을 확인했을 뿐 전체 graph 복구는 미확인이다. |

**승계가 하나라도 역사적 주장을 새 조직에 자동 이관할 근거는 별도다.** ROR-X1의 IRIF는 현실 합병의 후계이나 옛 PPS 논문 소속을 모두 IRIF로 바꿔야 한다는 결론은 원문에 없다. ROR05는 네 후계가 있어 현재 문의처 하나를 고를 수도 없다. 이력은 가능한 관계와 시점을 복원하지만 사용 목적을 대신 만들지 못한다. [ROR data structure, Relationships·Status](https://ror.readme.io/docs/ror-data-structure) · [EQAR institution205](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=205).

## 통지·복구의 소비자와 비용 한계

MB06의 MusicBrainz merge, AcoustID live DB, AcoustID replication 소비자는 서로 다른 전달 단계다. 2025-02 처리 재가동이나 issue 닫힘만 보면 성공처럼 보이지만,3월 updated·삭제 전파와6월 재동기화가 계속 논의됐다. ROR의 closed/released 댓글도 소비자 CoLab/OpenAlex의 의미가 동시에 수렴했다는 증거가 아니다. Homebrew의 rename map 역시 Rails Brewfile의 최신판 선택을 대신하지 않았다. [AcoustID#114](https://github.com/acoustid/acoustid-server/issues/114) · [ROR-S33](https://colab.ws/organizations/041xzk838) · [ROR-S34](https://openalex.org/institutions/I4210143448) · [SW-S20](https://github.com/rails/rails/commit/27cb8c618ca3a96a2817e412bfe48dc29a6acfa3).

관측 비용은 편집 ID 수, changed record 수, 이전/이후 blob 수, 이동해야 할 typed relation·consumer 파일 수, 미확인 필드 수로 제시했다. 작업 시간·금액·전체 운영 오병합률은 측정하지 않았다. 무거운 이력 보존이 항상 더 낫다는 결론도 내리지 않는다. exact 판이나 관계가 필요 없는 좁은 검색에서는 정상 별칭이 충분할 수 있고, 전체 이력이 있어도 목표가 지정되지 않은 복수 후계에서는 선택을 보류해야 한다.
