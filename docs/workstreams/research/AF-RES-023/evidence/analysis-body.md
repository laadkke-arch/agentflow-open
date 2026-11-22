## 판단 범위와 자료 읽기 방법

**인계 판정은 REVIEW_READY_WITH_GAPS다.** 실제 사건18·고유 원문 최소38·독립 외부 소비자7·비교54행은 확보했으나, 완전한 전후 ID/정정판18건과 날짜가 검증된 소비자 인용6체인은 확보하지 못했다. 정정 사례의 비중과 내부 판독의 한계도 남긴다.

이 연구의 결론은 **대상 기록의 복원, 당시 주장의 복원, 현재 대체 대상의 선택을 분리해야 한다**는 것이다. 같은 링크로 돌아간다는 사실은 기능·판·인용 역할의 보존을 뜻하지 않는다. 반대로 명칭·레코드가 달라도 실제 중복을 정리한 사건이 있어 모든 차이를 분리 사유로 삼을 수도 없다. 이는 이번 목적 표집에서 얻은 판단이며 제품 ID/DB 설계 확정이나 전체 오병합률 추정이 아니다.

본표본은18사건이다. MusicBrainz6, ROR6, Homebrew5, Wikidata1로 시스템당 최대6건이다. 성공 코드는 catalog에서 허용되어 적용된 병합5건을 뜻한다. 정정·분리·되돌림9건 중 좁은 의미의 merge 취소/정정은3건이고, 나머지는 recording 재사용 분리1, software 기능 분리1, 같은 ROR ID의 다른 조직 정보 정정3, canonical rename rollback1이다. 나머지4건은 승계·기각·정상 별칭·버전 승계다. 목표였던 약6:6:6에 비해 정정군에 치우쳤다. 이 차이와 불완전한 전후 ID는 수용 조건에서 미충족으로 남긴다.

`sources.json`에는 원문·고정판·접근 실패·보충 원문135행이 있다. 최소수 계산은 동일 사건 여러 화면을 합쳐 **38개=사건 대표 원문18+정책/지침12+소비자 원장8**만 산입한다. 소비자8중7은 원 catalog와 별개 발행자의 원문이고1은 Wikidata 내부의 별도 소비자 item이다. 이 숫자는135개 독립 확인이나38개 완전 복원 성공을 뜻하지 않는다. `minimum_counted`, `minimum_category`, `lineage`, `sections_read`, `limits`를 함께 보아야 한다.

고정 입력은 AF-RES-020의 [B19](https://github.com/laadkke-arch/agentflow-open/blob/856e6b40ae12d43197a6f02f7bf6ab7a7506fd35/docs/workstreams/research/AF-RES-020/bundles/B19.md), [RESULT Q1·Q3](https://github.com/laadkke-arch/agentflow-open/blob/856e6b40ae12d43197a6f02f7bf6ab7a7506fd35/docs/workstreams/research/AF-RES-020/RESULT.md), [DECISIONS D04–D06](https://github.com/laadkke-arch/agentflow-open/blob/856e6b40ae12d43197a6f02f7bf6ab7a7506fd35/docs/workstreams/research/AF-RES-020/DECISIONS.md)이다. 이 입력의 정의나 DOI/ID 일반 소개는 새 외부 사례 수에 넣지 않았다. 실행·모델·배정 SHA·사전 코딩은 [SCOPE.md](../AF-RES-023/SCOPE.md)에 있다.

## Q1. 실제로 일어난 편집

**하나의 ‘병합’이라는 말로18건을 묶으면 중요한 차이가 사라진다.** MusicBrainz MB04·05·06은 공개 edit/history에 적용된 병합이 보인다. 특히 MB04의5yes/0no, MB06의3yes/0no는 표결 및 적용 사실이며 실체 동일성의 독립 검증 수가 아니다. MB03은0yes/0no로 적용된60587125 뒤63762772에서 실제 medium 참조를 다른 recording으로 옮겼다. 편집 규칙의 존재만으로 성공을 채점하지 않았다. [MB-S17, Changes·Votes·Status](https://musicbrainz.org/edit/68967621) · [MB-S22, Status](https://musicbrainz.org/edit/92853437) · [MB-S12](https://musicbrainz.org/edit/60587125) · [MB-S13,63762772](https://musicbrainz.org/release/5aeb8c8f-cd6a-4d43-97e5-fb86b9b35695/edits).

ROR01은 중복을 withdrawn으로 만들고 successor를 지정한 catalog 병합이다. ROR02는 제안을 기각한 실제 판단 기록이며 완료 병합이 아니다. ROR06–08은 ID끼리 합친 기록이 아니라 **같은 ID에 다른 조직의 속성을 넣은 오류를 정정**한 사건이다. 이를 literal merge undo 분자에 넣지 않았다. ROR05는 기관 종료와 복수 후계를 연결한다. 고정 파일은 `ror-updates@baffbf2…`의 release-candidate changed JSON이며 전체 배포 dump/live API를 확인한 것과 구별한다. [ROR-S03](https://github.com/ror-community/ror-updates/issues/15331) · [ROR-S09, 기각댓글](https://github.com/ror-community/ror-updates/issues/13495#issuecomment-2457897274) · [ROR-S23](https://github.com/ror-community/ror-updates/issues/25805) · [ROR-S38](https://github.com/ror-community/ror-updates/issues/21008).

Homebrew SW01은 중복 formula를 삭제하고 alias를 유지했다. SW02는 동일3.2.4 archive의 이름을 versioned formula로 바꾼 정상 rename이다. SW03은 기능적 설치 문제를 이유로 canonical 이름을 되돌렸으며 의미상 실체의 오병합과 다르다. SW06은 하나의 배포 recipe가 제공하던 library와 CLI를 실제로 갈랐다. WD01은 category와 institution을 합친 뒤 undo했고 별도 consumer의 typed relation도 다시 고쳤다. [SW-S01](https://github.com/Homebrew/homebrew-core/commit/7f379ed5e4135654176204310ae0f24af0826eaa) · [SW-S04](https://github.com/Homebrew/homebrew-core/commit/eb1463eb72712952a10ecdfc201592ca4d24a20a) · [SW-S07](https://github.com/Homebrew/homebrew-core/commit/8c2998215320942b1329f5b073fad7bfa33e9976) · [SW-S14](https://github.com/Homebrew/homebrew-core/commit/e5e819e64a3104cabb55d46ea8e80d69aaf76d5b) · [WD-S05](https://www.wikidata.org/w/index.php?diff=1038289881&oldid=986442520&title=Q59165607&type=revision).

정책과 편집 결과는 별도 원문으로 읽었지만 대부분 같은 생산자 계보다. ROR 공식 정책이 successor에 현실 승계와 오류 record 교체를 모두 허용한다는 사실만으로 특정 successor의 사용 목적 대체성이 증명되지는 않는다. 독립 반대 근거는 Rails·AcoustID·EQAR 등 소비자 기록에서 보강한다. [ROR-S01, Relationships·Status](https://ror.readme.io/docs/ror-data-structure) · [MB-S01, Steps](https://musicbrainz.org/doc/How_to_Merge_Releases) · [SW-S17](https://docs.brew.sh/Rename-A-Formula).

## Q2. 같은 것으로 본 층위와 반대 판단

[identity-layers.csv](../AF-RES-023/identity-layers.csv)는18사건 각각 URL, catalog entity, work/recording/release 또는 현실 대상, 조직/부서, 프로젝트/배포물/판, 기능, 목적상 대체성, 제안 근거, 반대 근거, 원 외부 ID 대상을 독립 열로 둔다. ‘없음’과 ‘미확인’을 구별하고, 명시적 반대 의견이 없으면 연구자가 반대 투표를 지어내지 않았다.

MB01은 같은 DiscID가 지역·matrix가 다른 물리 release의 병합을 정당화하지 못한 사례다. MB04는 서로 다른 Beautiful Sky 발매판이 하나의 recording을 공유할 수 있다는 반대 사례다. MB05에서 트랙3·8 누락은 처음 병합을 막았지만, 누락을 보완한 뒤 같은 앨범을 합쳤다. **속성 차이를 실물 차이로 볼지 불완전한 입력으로 볼지 판단한 원문**이 있어야 두 방향의 오류를 구별할 수 있다. [MB-S05–08·37–39, MB01](https://musicbrainz.org/edit/151147443) · [MB-S16–18, MB04](https://musicbrainz.org/edit/68967621) · [MB-S19–21, MB05](https://musicbrainz.org/release/633a31aa-ed97-49fc-ab70-27f8e97fc5be/edits).

ROR02의 제안자는 본부와 division을 같은 조직으로 보았지만 큐레이터는 논문 소속의 단위를 보존했다. ROR06의 같은 대학 브랜드는 Puebla와 SLP를 같은 ID에 넣을 근거가 되지 않았다. WD01의 건물, 운영 기관, Wikimedia category는 이름이 겹쳐도 P910이라는 관계 자리에서 교체할 수 없다. 기관/부서는 현실 조직 관계이고 category는 지식 표현이므로 둘을 단일한 일반 후계 관계로 취급하지 않는다. [ROR-S09](https://github.com/ror-community/ror-updates/issues/13495) · [ROR-S23](https://github.com/ror-community/ror-updates/issues/25805) · [WD-S06, undo 요약·삭제 statement](https://www.wikidata.org/w/index.php?diff=1048159568&oldid=1038289881&title=Q59165607&type=revision).

SW01은 다른 recipe 이름이 같은 tf-50b8 source를 가리킨 경우다. 그러나 recipe의 패치·설치옵션까지 같지는 않았다. SW06은 같은 upstream0.25.8이어도 CLI 설치 범위가 변했다. 보충 SW-F01의 yt-dlp와 youtube-dl은 넓은 용도가 겹쳐도 서로 다른 upstream archive·버전·기본 동작을 갖고 병렬 등록되었다. 포크 등록을 alias 제안의 기각으로 바꾸어 서술하지 않았다. [SW-S01–03](https://github.com/Homebrew/homebrew-core/commit/7f379ed5e4135654176204310ae0f24af0826eaa) · [SW-S14–16](https://github.com/Homebrew/homebrew-core/pull/231544) · [SW-FS01–03](https://github.com/Homebrew/homebrew-core/commit/3e32b083e96a38b8bd09b3516898e77dc05bd518).

외부 식별자에 대해서는 catalog의 원 필드와 이관 범위를 기록했지만 ISRC·GRID·ISNI·GND·문화재 ID 발급기관의 원문을 전수 재검증하지 않았다. 따라서 해당 값이 보존됐다는 관측과 실제 대상이 같다는 발급자 판단을 구별한다. 이 한계를 바꿀 최소 입력은 사건별 원 발급자 고정 record와 catalog edit 직전 필드 provenance다.

## Q3. 전후 ID, 판, HTTP는 어디를 가리켰는가

**이번에 직접 관측한200 반례는 SW06이다.** `https://formulae.brew.sh/formula/tree-sitter`는2026-11-22T03:13:41.897956Z에200이었지만 읽힌 범위는 library0.27.2였다. split 이전0.25.8 recipe에는 CLI 설치가 있었다. HTTP 생존과 `tree-sitter generate`라는 추천 기능의 생존은 다르다. [http-observations.json](../AF-RES-023/collectors/software/http-observations.json), [SW-S15, fixed parent](https://github.com/Homebrew/homebrew-core/blob/5d3c6448fe87f35290fe191a0f80b9e4c189a63d/Formula/t/tree-sitter.rb), [SW-S14, CLI 제거·신규 formula](https://github.com/Homebrew/homebrew-core/commit/e5e819e64a3104cabb55d46ea8e80d69aaf76d5b).

반대 방향은 SW02다. 현재 old main의 `Formula/lib/libxml++3.rb`는404였지만 rename 직전 고정 parent의 본문은 GitHub connector에서 확보했다. 그 별도 fixed URL에 대한 HTTP 시도는503이었으므로 ‘고정판 HTTP200’이라고 쓰지 않았다. 파일이 현재 경로에서 사라진 것과 역사적 source blob을 읽을 수 없는 것은 다르다. major3 검색 목적에는 정상 alias가 충분할 수 있지만 exact3.2.4 recipe 주장에는 fixed parent와 근거 줄이 필요하다. [SW-S05](https://github.com/Homebrew/homebrew-core/blob/4ea8a912eaa74d7606b2c7307899d7c9faf399c5/Formula/lib/libxml%2B%2B3.rb) · [SW-S04, rename map·recipe](https://github.com/Homebrew/homebrew-core/commit/eb1463eb72712952a10ecdfc201592ca4d24a20a).

MB06은2022 병합,2024 소비자 보고 target958820ff,2026현재 targetfd416d42를 분리한다. 현재 도착점을2022 즉시 target으로 소급하지 않는다. ROR07은v1.38의 스페인 metadata와v1.60의 이탈리아 이름·도메인·부모를 같은041xzk838에서 보지만, 이를 모두 그 ID가 원래 적법하게 식별한 대상이라고 승인하지 않는다. 역사판을 보존하면 **어떤 잘못된 주장이 저장되었는지**도 복원할 수 있다. [MB-S23](https://github.com/acoustid/acoustid-server/issues/114) · [ROR-S28](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v1.38/updates/041xzk838.json) · [ROR-S31](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v1.60/updates/041xzk838.json).

ROR05의1→4, SW06의1→2, MB05/ROR01/SW01의여럿→하나, SW02의하나→하나를 사건 원장에 따로 기록했다. ROR와 MusicBrainz의 웹 본문 열람은 raw HTTP 측정이 아니다. shell403, 웹 도구의 성공, 실제 redirect 관측, 역사 record의 상태를 하나의 ‘링크 정상’ 값으로 합치지 않았다.

## Q4. 분리·취소는 무엇을 복구했는가

[restoration.csv](../AF-RES-023/restoration.csv)는18×5=90개 항목에 라벨, 외부 ID, 인용, 판, 복수 후계의 관측/한계를 기록한다. 수집자의 `AUTO/auto`는 **표시된 자료에서 해당 값의 기계적 추출이 가능하다는 해석**이다. 자동 복구 프로그램을 실행한 사건은0/18이고,90칸을 전수 무손실 복원 성공으로 채점하지 않는다. 원문 접근 실패와 관계 미기록을 실제 소실로 합산하지 않았다.

WD01의 기관 merge undo는2019-11-08 10:36이고, 건물P910의 소비자 undo는10:37이다. 순서상 본체를 되돌린 후 별도 소비자 변경이 필요했다는 사실은 보이지만, 표시된1분을 작업 소요시간으로 계산하지 않는다. 확인한 잘못된 관계는1건이며 전체 incoming graph 복구는 미확인이다. category 자체의 복원 revision도 확보하지 못했다. [WD-S06](https://www.wikidata.org/w/index.php?diff=1048159568&oldid=1038289881&title=Q59165607&type=revision) · [WD-S07](https://www.wikidata.org/w/index.php?diff=1039041773&oldid=936463156&title=Q314104&type=revision) · [WD-S09](https://www.wikidata.org/w/index.php?oldid=1048159950&title=Q314104).

ROR07은 이름·사이트·부모가 복구돼도 location이 남을 수 있음을 보여 준다. v1.60 changed JSON은 이탈리아 이름/ibf.cnr.it/CNR parent와 Spain/Leioa를 동시에 가진다. 이는 **그 고정 파일의 속성 불일치**이고2026 현재 ROR API 전체가 같은 오류를 갖는다는 판정이 아니다. CoLab의 스페인 설명과 OpenAlex의 이탈리아 설명도 현재 다른 발행자가 같은 ID를 달리 읽는다는 관측이다. 최초 복제 시점·어느 변경을 반영했는지·정정 날짜는 미확인이다. [ROR-S30–31](https://github.com/ror-community/ror-updates/issues/17073) · [fixed JSON](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v1.60/updates/041xzk838.json) · [ROR-S33](https://colab.ws/organizations/041xzk838) · [ROR-S34](https://openalex.org/institutions/I4210143448).

MB01은 Europe 새 release0243a6b1을 만들어 DiscID를 다시 붙이고 retained893fa571을US/Canada로 정정했다. 옛 source f0a68a45를 되살렸다고 쓰지 않았다. 이 ID는 커버 파일명 계보로 추론했고 merge 행의 source href와 current route를 직접 확인하지 못했다. MB03 역시 새 recording을 만든 것이 source MBIDs·모든 지문·외부 인용의 원상복구를 뜻하지 않는다. MB02의 라벨복원115752742와 medium 참조변경115760023은 둘 다 직접 읽은 별도 동작이다. [MB-S06·38·39](https://musicbrainz.org/release/0243a6b1-ee2f-4d39-b0d1-1ee0c77412e6/edits) · [MB-S10](https://musicbrainz.org/recording/132ded03-02d3-4dc6-b7d8-2d15ff97ec0f/edits).

성공 취소의 좁은 범위는 실제 diff로 말할 수 있다. WD01 P910 값, MB02 medium 참조, SW03 canonical formula명은 확인한 판에서 돌아왔다. 반면 외부 인용 전수와 fingerprint replication은 다른 소비자 작업이다. [Wikidata Help:Split, incoming links](https://www.wikidata.org/wiki/Help:Split_an_item)와 [Help:Merge, Unmerging](https://www.wikidata.org/wiki/Help:Merge)는 이 과제를 설명하지만 그 설명 자체를 사건 성공의 대체 증거로 사용하지 않았다. 같은 Wikidata 생산자이며 Help:Merge는 제안 지침 상태였다.

## Q5. 실제 참조자의 영향

`citations.csv`에는 보충을 포함해13행이 있다. 엄격한 고유 소비자 원장8행 중 외부 발행자 독립7행은 AcoustID issue114, COMTES Contacts, EQAR institution205, CoLab, OpenAlex, Rails Brewfile, irlm/workbench tools.tsv다. 나머지1행은 Wikidata의 별도 건물item이다. 같은 AcoustID track과 issue는 두 소비자 피해로 세지 않았다. science.eus는 파생 metadata임을 표시하고 최소수에서는 제외했다. AgentScript issue33은 분리 뒤 이름을 추측했을 때의 실패 보고라 분리 전 저장 링크 원장 수에서는 제외했다.

| 소비자·근거 | 확인한 작성 문맥과 후속 기록 | 말할 수 없는 것 |
| --- | --- | --- |
| MB-C01 / MB-S23, AcoustID | 2024-12-31 old MBID와 target Fingerprints를 인용한 결함 보고. 2025-02 재가동,3월 updated·삭제 전파 문제 인정,6월 재동기화 논의. | 2022 즉시 target·모든 replica 최종 정상화·실제 오태깅 피해 |
| SW-D01 / SW-S20, Rails | 2024-05-23 Brewfile diff에서 postgresql→postgresql@16+libpq. 원문은 rename이14를 선택하므로 최신판 목적에 맞지 않는다고 설명. | 사용자 DB 손상·업그레이드 재현·2026최신판 |
| SW-D02 / SW-S21, irlm/workbench | 2026-11-04 tools.tsv의 brew 패키지를 tree-sitter-cli로 수정. 논리 도구/실행파일 문맥 유지. | 실제 사용자의 설치 실패·비용·판 호환성 전수검증 |
| WD-C01 / WD-S07–09 | P910 값이 category→institution으로 바뀌고2019-11-08 별도undo로 복구된 불변 diff. | 외부기관 독립 확인·모든 incoming link 복구·사람의 오추천 피해 |
| ROR-C01 / ROR-S08, COMTES | 회사 Contacts가 withdrawn000qg0t28을 인용. 현재 회사찾기 문맥을 직접 읽음. | 최초 삽입일·소비자 수정일·현재 resolver 클릭결과 |
| ROR-C02 / ROR-S20, EQAR | 옛 ZFH ID, 종료2023, 네 후계와 역사 평가기록을 함께 보존. | 처음 이관한 날짜·특정 프로그램의 현재 문의처 |
| ROR-C03·04 / ROR-S33·34, CoLab/OpenAlex | 동일041xzk838을 각각 스페인/이탈리아 기관으로 설명. | 어느 원판을 언제 복제했는지·소비자의 실제 정정·잘못된 논문 귀속 피해 |

직접 원문: [AcoustID](https://github.com/acoustid/acoustid-server/issues/114), [Rails fixed diff](https://github.com/rails/rails/commit/27cb8c618ca3a96a2817e412bfe48dc29a6acfa3.patch), [workbench fixed diff](https://github.com/irlm/workbench/commit/3c93157225ada89394f8939f24fcb4baa98d8d92), [Wikidata fixed correction](https://www.wikidata.org/w/index.php?oldid=1048159950&title=Q314104), [COMTES](https://www.comtesfht.com/contacts), [EQAR](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=205), [CoLab](https://colab.ws/organizations/041xzk838), [OpenAlex](https://openalex.org/institutions/I4210143448).

따라서 **7개 외부 독립 소비자 원문을 열었다는 조건과,6개의 날짜 있는 사전·사후 인용 이력을 확보했다는 조건은 다르다.** 날짜가 있는 후속 chain은4개이며 그중 외부3개, 불변 전후 인용 diff는Rails·workbench·Wikidata3개다. ROR4개는 현재 인용의 문맥은 읽었으나 최초 작성일/수정일이 없으므로 역사적 영향 검증에서는 미확인으로 남는다. 실제 사람에게 발생한 오추천 피해는 본18사건 모두 미확인이다. AcoustID metadata 결함 및 AgentScript의 build 실패는 보고된 기능 문제이며 이번 실행의 재현 결과가 아니다. [SW-S22, Issue2](https://github.com/salesforce/agentscript/issues/33).

## Q6. 세 저장 표현은 무엇을 복원했는가

초기 보기/키를2026-11-22T03:36:33Z에 분리 고정하고 commit `7f6fc6f7da84b5a2401e287abb8ec1f1c9ed1837`에 저장했다. 첫 답안은 `9eb153d6e33f0ee6ef9f6fca8170c3b163d3e5a8`에 고정했다. 그 뒤 감사에서 URL 경로 불일치, 현재 target의 ID 표기 차이,②의 관계 정보 혼합을 발견했다. 초기 파일은 보존하고 [protocol-errata.md](../AF-RES-023/evidence/protocol-errata.md)에 영향을 기록했다. 공통 입력을 맞춘v2에는 판독자를 배정하지 않았다. 역사 값과 변경 판단을 추가 분리한v3를2026-11-22T03:49:53Z에 고정하고 commit `5ac71a3821baa0daa0d0e37a2813b629fbc7065e`에 저장했다. 새 문맥 판독자3명의v3답안은 `ae3315ba734067f57ed98702e50636e5c5cd87f9`에 고정했다.

원문-보기 대조에서 MB05 생존target과 SW03 정정후6.2.4가 **원문에는 있지만③요약에서 빠진 오류**도 확인했다. 두 값만 보완한v4를 `c2f3f3c2d2056fe1a34546154f3590a46c7391eb`에 고정한 뒤 추가 새 문맥3명이 해당 두 사건만 읽었다. 답안은 `fadda010c9ddf714be861dc3888666db705d23b6`에 고정했다. 최종54행은 **v3의16사건48행+v4의2사건6행**이다. 이어받은16사건은 visible card SHA256과 공통 질문·방법·누락 규칙이 같음을 검사했다. 한 번에54행을 새로 실행한 시험으로 표현하지 않는다. 사후 키는 처음과 같은SHA256이다.

각 새 문맥 판독자는 한 표현만 허용받고 외부 조회와 다른 파일 읽기를 금지받았다. 파일 해시·시각·읽은 자료 자기보고와 답안을 보존한다. 원문 수집자와 root는 이미 정정에 노출됐으므로 **채점과 통합 결론은 연구자의 자기 점검**이다. 같은 모델 계열의 분리된 내부 판독을 인간/외부 독립 맹검으로 부르지 않는다. 첫 시도의 입력 결함을 숨기거나 첫 SELECT 수를 이력 효과로 쓰지 않았다.

짧은 추천 이유18개는 사건 문맥에서 연구자가 만든 통제된 보기다. 실제 역사 추천문18개를 발견한 것이 아니다. 실제 소비자 인용은 별도 `citations.csv`에 남긴다. v3의 모든 표현은 동일 사건·동일 이유·동일 현재 조회 관측을 사용한다. ②는 역사 ID/판/근거 절,③은 관계/유효시점 이력과 그 정정 판단을 더한다. 외부 원문이 미확보인 부분을③에 가상 정답으로 보충하지 않았다. 이력에 사후 판단도 포함되므로 순수한 ID 저장 효과나 토큰 수 통제 실험이 아니다.

채점은 옛 대상, 기능·판·이유, 현재 목적지 선택을 구별한다. 역사적 잘못된 metadata를 재현하는 것은 그 metadata를 승인하는 PASS가 아니다. `HOLD`는 필요한 정보가 없어서 선택을 보류한 결과이며 틀린 대상을 선택한 `WRONG`과 다르다. 정답 키 자체가 불완전한 MB01/03/04/05/06과 ROR의 부분 판정은 분모18에서 빼지 않는다. 각 판독 답안의 전체 텍스트·키·오류·추가 입력은54행 `reconstruction.csv`에 있다. 아래 집계는 그 자기 점검의 읽기 성과일 뿐 저장 방식의 운영 정확도 향상률이 아니다.

{{RECONSTRUCTION_SUMMARY}}

위 SELECT는 판독자가 고른 코드이며 성공 수가 아니다. MB03①은 B4 관계를 검증하지 않았다고 단서를 달면서도 retained2:32를 선택해 실제 정정 대상과 어긋났다. ROR05②는 현재 후계가 아니라 EQAR의 역사 평가기록만 선택했다. ROR06②도 v1.66의 과거 SLP 표기만 선택한 답이다. 이를 현재 정답을 단정한 오류로 과장하지 않았지만, 정정후 SLP 목적지에 재사용하면 잘못된 본교 ID가 된다. SW03②의 조건부 선택도 역사 recipe만 가리킨다. 이러한 범위 차이는 `destination_verdict`와 `destination_assessment`에 남긴다.

단순 링크가 충분한 반례는 MB04의 좁은 녹음 검색이다. 현재 retained URL과 짧은 이유가 이미 Reamonn/Back Again7:34를 특정하며 물리 CD 판을 요구하지 않는다. 이는 source ID provenance까지 복원한 성공과 다르다. 정상 alias의 구조적 반례는 SW02다. 같은3.2.4 archive를 major3 이름으로 찾는 목적에는 alias가 충분할 수 있으나, 이번 old file404 환경에서 실제 클릭만으로 alias를 따라간 실험은 수행하지 않았다.

이력이 충분해도 하나를 고를 수 없는 반례는 ROR05다. 네 후계를 알고도 프로그램이 없다. ROR07에서는 당시 스페인 정보가 기록돼 있었다는 사실과 원 ID가 이탈리아 기관이라는 정정을 모두 알아도, 스페인 기관의 정답 ROR를 확보하지 못했으므로 보류한다. SW05는 canonical successor@14를 아는 것과2024 Rails의 최신판 목적에 맞는@16을 고르는 것이 다르다. SW06은 CLI successor를 선택한 뒤에도0.25.x 요구가 남는다.

‘모든 차이를 분리’하는 판단의 반례는 SW01·MB05에서 유지했다. alias를 무조건 지우거나 불완전한 중복을 영구 분리하면 같은 배포물/발매판 탐색을 악화시킬 수 있다. 반대로 MB01/03의 실제 판/녹음 차이를 이름·DiscID·공유 work 하나로 덮으면 과거 주장의 범위가 바뀐다. 어느 결론이 나와야 통과한다는 조건을 두지 않았다.

## Q7. 다른 분야로 옮길 수 있는 원리와 경계

상세 비교는 [alternatives.md](../AF-RES-023/alternatives.md)에 있다. 쌍 A는 MB03/04/01의 work·recording·release와 SW06의 프로젝트·library/CLI 및 SW-F01의 포크·판을 비교한다. 쌍 B는 ROR01/02/05/06·ROR-X1의 중복/본부·지부/승계와 WD01의 category·institution·building을 비교한다. 각 쌍에서 원 편집자, 원 식별자 발급자, 과거 인용 독자, 추천을 판에 묶는 개발자의 네 관점을 따로 기록했다.

옮길 수 있는 원리는 **인용이 요구한 역할과 판을 변경 관계와 함께 보존하고, 자동 이관의 범위를 필드/소비자 단위로 검사하는 것**이다. 음악의 동일 work가 recording 병합을 허용하지 않는 것처럼, 같은 프로젝트의 source가 library/CLI의 기능 대체성을 허용하지 않는다. 다만 음악 release의 지역·matrix 경계를 소프트웨어에 그대로 대응시키지는 않는다. 소프트웨어에서는 설치 산출물·ABI·명령과 exact version이 별도의 관측 단위다.

현실 기관 합병과 catalog 중복 병합도 다르다. PPS+LIAFA→IRIF는2016-01-01 현실 합병을 대학 원문에서 확인했고 ROR의2026 반영과 분리했다. COMTES는 현실 합병 근거 없이 같은 회사의 중복 record를 정리한 경우다. 이력 관계가 같아 보인다는 이유로 과거 논문 소속을 현재 후계로 모두 치환할 수 없다. [ROR-X03, Recherche136–147행](https://www.informatique.u-paris.fr/ufr/presentation_ufr) · [ROR-X01](https://github.com/ror-community/ror-updates/issues/43488) · [ROR-S03](https://github.com/ror-community/ror-updates/issues/15331).

영구 식별자의 보장 범위는 각 시스템의 읽은 문서에 한정했다. MusicBrainz는 entity 종류와 merge redirect를 설명하지만 여러 release가 같은 recording을 쓸 수 있다. ROR는 historical record와 status/successor를 보존하며 복수 successor를 허용한다. Wikidata의 merge/redirect 안내는 열람 당시 제안 지침이며 관계 타입 보존을 실제 도구 실행으로 보증하지 않는다. Homebrew의 읽은 rename/version 문서는 formula명을 영구적인 기능/판 식별자로 보장하지 않는다. [MB-S04](https://musicbrainz.org/doc/MusicBrainz_Identifier) · [ROR-S01](https://ror.readme.io/docs/ror-data-structure) · [WD-S03](https://www.wikidata.org/wiki/Help:Redirects) · [SW-S18](https://docs.brew.sh/Versions).

엄격 병합은 같은 층위의 중복에서, 가역 별칭은 좁은 탐색 목적과 해석 가능한 한 대상에서, 병렬 후보는 복수 후계/포크/기능 분기에서 검토할 수 있다. 비용은 실제 편집 ID, changed JSON, alias/rename map, 전후 blob, consumer 수정 파일 수로만 관측했다. 시간·금액·생산성·전체 실패율은 측정하지 않았다. 따라서 이 연구가 제안하는 다음 선택은 특정 DB 채택이 아니라 **역사 주장과 현재 추천을 동시에 검증할 작은 후속 표본**이다.

## 반증 탐색·미확인의 재개 위치

각 `collectors/*/SEARCH_LOG.md`에 검색어·실제 열어 본 edit/issue·기각 후보를 남겼다. MusicBrainz의 거절 보고66223421은 개별 상태 접근이 막혀 주 사례로 세지 않았다. Jimmie Rodgers/Carter Family 분리 질문, 동명 음악인, Stole 지문/판 토론은 실제 전후 edit가 부족해 보충으로 남겼다. Wikidata의 BankID·mantra·Greengrass와 Commons propagation도 관련 논의는 읽었으나 원 revision 연결이 부족해18건에 더하지 않았다. Homebrew eigen3 alias의6분7초 뒤 삭제는 이유가 없으므로 ‘오병합 성공 정정’으로 세지 않았다.

MusicBrainz 공식20261121-002203 edit dump는 HEAD200,17,284,315,658바이트까지 확인했다. 전체 내려받기와 edit_data/redirect 행 추출은 수행하지 않았다. 접근 차단으로 위장하지 않고, 필요한4개 edit ID와 정확한 입력·미실행 명령을 [DUMP_FOLLOWUP.md](../AF-RES-023/collectors/musicbrainz/DUMP_FOLLOWUP.md)에 남긴다. 현재 snapshot에서 필요한 edit_data가 존재하는지부터 검사해야 하며 현재 redirect만으로 과거 target을 소급하면 안 된다.

가장 작은 다음 보강은 MB60587125·68967621·92853437·151147443의 원 source/target 행, ROR의 해당 전체 release dump 검증, ROR 소비자4곳의 최초 인용·정정 고정판이다. 접근 불가인 원문과 실제 관계를 보존하지 않은 원문을 별개로 채점한 뒤에만 복원 충분성 판단을 넓힐 수 있다.
