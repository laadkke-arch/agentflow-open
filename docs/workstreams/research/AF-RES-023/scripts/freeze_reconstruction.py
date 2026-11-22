"""Freeze researcher-authored views and a separately stored post-edit key.

This is an internal reading diagnostic, not a historical recommendation dataset.
Run once before readers; --verify only checks the already-frozen hashes.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, random, sys

P = Path(__file__).resolve().parents[1]
E = {x['event_id']: x for x in (json.loads(z) for z in (P/'events.jsonl').read_text().splitlines() if z.strip())}
S = {x['id']:x for x in json.loads((P/'sources.json').read_text())}
cases=[]

def add(eid,url,reason,historical,history,key,current='현재 URL의 HTTP·본문 재조회는 이 카드에 제공되지 않는다.',missing='전체 필드·외부 인용 전수검사는 제공되지 않는다.'):
    ev=E[eid]
    cases.append(dict(event_id=eid,saved_url=url,short_reason=reason,historical=historical,history=history,key=key,current_lookup=current,common_missing=missing,source_pool=ev['source_ids']))

add('MB01','https://musicbrainz.org/release/893fa571-0d95-4a89-a970-a408d1586755',
    'private music CD의 내 유럽판을 찾기 위한 링크.',
    '저장 시점 모델: 2026-08 병합 이후. release893fa571, 11-track CD, DiscID QnV3tLQLJjFu6sEFcbSYh5AstG4-. 실제 원 생성/DiscID 이력131420900·137042427에는 Worldwide/2025가 있었다. 유럽판 matrix와 옛 source ID를 이 저장 표현에 확보하지 못했다.',
    'merge151147443는 2026-08-16 적용. 이후 edit152536177로 Europe release0243a6b1-ee2f-4d39-b0d1-1ee0c77412e6를 만들고 DiscID152589926를 붙였다. 152539607은 retained893fa571의 지역을 US+Canada로 2026-09-01 정정했다. 원 cover-art 파일명의 f0a68a45를 source로 잇는 것은 추론이고 옛 ID 복원은 확인하지 않았다.',
    '의도는 Europe 물리 발매판. retained893fa571=US/Canada, Europe 후보0243a6b1; 동일 DiscID만으로 지역·matrix를 확정하지 않는다. 새 Europe ID를 재생성한 것이며 old source 원상복구/모든 외부 ID 이관은 미확인. 실제 CD matrix를 추가 확인해야 한다.',
    current='retained URL의 현재 표시는 green cover/5 lines small text. HTTP코드 미측정.',
    missing='실물 matrix/사진을 입력받지 못함. f0a68a45 source 매핑은 추론. 당시 외부ID의 전체 provenance 없음.')

add('MB02','https://musicbrainz.org/recording/132ded03-02d3-4dc6-b7d8-2d15ff97ec0f',
    'CD3 첫 곡 Les Princes des villes를 찾기 위한 녹음 링크.',
    '2019-09-04 edit63656996에서 이 ID 이름이 La Groupie du pianiste→Les Princes des villes로 바뀌었다. 저장 문맥은 medium3 track1, 5:27이다. 이전에는 CD2 La Groupie/Rhythm mix, 4:39에 사용되었다(공식 recording history).',
    '2024-09-09 edit115752742는 원 ID의 La Groupie 이름을 복구했다. 115760023은 medium3 track1을 별도 recording05d666f0-ffc8-41ee-8706-2825932b5d26으로 연결했다. 115752723은 취소되었다.',
    '원 추천 문맥은 Les Princes/CD3 track1/5:27이며 corrected recording은05d666f0. 기존132ded03은 La Groupie/Rhythm mix/CD2/4:39. 이름 되돌림과 medium 참조 복구는 별도 동작. 원문에는 이동할 ISRC/AcoustID가 없었다는 편집자 진술만 있다.',
    current='현재 oldID 이름은 La Groupie du pianiste (Rhythm mix); raw HTTP 미확인.')

add('MB03','https://musicbrainz.org/recording/2775d583-3c95-4f65-b856-76c5e1db732f',
    'Интервью B4의 07 녹음을 찾기 위한 링크.',
    '저장 시점 모델은 2019-04 merge60587125 이후. target2775d583 표시는 2:32. 해당 release5aeb8c8f-cd6a-4d43-97e5-fb86b9b35695의 B4 표시는 2:38이다. merge source MBID는 공개 행에 미노출.',
    '2019-09-16 edit63762772는 이 medium B4를 새 recordingaa574fa3-7b00-4096-873d-b812656dd556으로 옮겼다. 편집자는 B4에 오케스트라가 없으며 retained2775d583은 오케스트라판이라고 설명한다. 63972905는 새 recording에 work 관계를 더했다.',
    '추천 문맥은 Интервью B4 2:38의 비오케스트라 녹음, corrected aa574fa3. 동일 노래/제목은 같은 recording을 보장하지 않는다. source 원 MBID, fingerprints 전체 복원, 음원 독립 청취는 미확인.',
    current='현재2775d583은 07, 2:32로 표시된다. HTTP코드 미측정.',
    missing='merge source MBIDs 없음; 오케스트라 차이는 편집자 진술이며 음원 비교 미실행.')

add('MB04','https://musicbrainz.org/recording/7a3eb993-0b45-4ee3-971a-b385e9e92e11',
    'Reamonn의 Back Again 7:34 녹음을 찾는다. 특정 CD 발매판 선택은 요구하지 않는다.',
    '2020 edit68967621 target recording7a3eb993, Reamonn/Back Again7:34; ISRC DEC640300057 및 DEG120300914. 원 source MBID는 미노출. 두 Beautiful Sky edition의 녹음 중복이라는 제안이었다.',
    'merge68967621는 2020-04-17 5yes/0no Applied. 같은 recording을 여러 release가 공유한다. 검열판·기악판·다른 mix면 분리한다는 조건부 토론이 있으나 이 사건의 사후 오병합 정정은 발견하지 못했다.',
    '녹음 검색이라는 한정 목적에는7a3eb993/Back Again/Reamonn7:34로 답할 수 있다. release들은 구별된 채 남는다. 승인된 병합은 음원 동일성 독립검사나 source별ISRC provenance 복원 증명이 아니다.',
    current='직접 읽은 현재 target은 Back Again/Reamonn7:34, ISRC2개, 여러 Beautiful Sky release 연결. raw HTTP 미확인.',
    missing='source MBID 및 source별 외부ID provenance 없음; 사후 정정 키/음원 동일성 독립검사 없음.')

add('MB05','https://musicbrainz.org/release/da729585-32c9-4261-8a30-322d7d414653',
    'Neththara 앨범을 찾기 위한 링크. 데이터가 불완전하면 보완된 항목을 원한다.',
    '2017년 source da729585와 Neththara - Project4 target633a31aa-ed97-49fc-ab70-27f8e97fc5be가 함께 있었다. source는 트랙3·8이 빠졌고 artist 표기가 축약되어 있었다(공식 토론/편집 history).',
    '48434703으로 누락 트랙을 보완한 뒤 48447069 release merge가 2017-10-21 닫혔다. 공식 history는 recordings가 이미 merged였고 release/medium을 합쳤다고 설명한다. old source의 현재 raw redirect는 미확인.',
    '보완된 앨범 대상은633a31aa. 트랙 누락을 곧 다른 실물 판으로 보면 실제 중복을 놓친다. 개별 merge status 접근과 실물 두판 동일성 독립확인은 미완료이므로 완전한 역사복원 성공으로 채점하지 않는다.',
    missing='old source raw route, source별 외부ID provenance, 독립 실물판 정답 키 없음.')

add('MB06','https://musicbrainz.org/recording/fa9c940c-408b-41f0-b746-997e50e36d72',
    'Tu es folle의 AcoustID 지문을 MB 녹음과 함께 조회하려는 링크.',
    '소비자 issue114가 2024-12-31 oldMBID fa9c940c를 인용했다. AcoustID b847e16e-d9ed-4aeb-bc4d-cabe7f16a914; 당시 인용한 Fingerprints target은958820ff-ec99-4aec-8df3-737d699e796e. 관련merge92853437은2022-09-19 Applied이나 그 즉시 target MBID는 공개 행에 없다.',
    '2024 소비자는 old/merged MBID가 별도로 남고 target 지문표가 비었다고 보고. 2025-02 처리 재가동 후 03-05 운영자가 updated·삭제가 replica에 전파되지 않는 문제를 인정했고06-18 재동기화 논의가 이어졌다. 2026현재 읽힌 target은fd416d42-3d40-4a4f-9673-ca1a51fdedab이다. 2022→2024→2026 모든 중간 edit은 미확보.',
    '역사적 소비자 목적은 Tu es folle fingerprint와 MBID의 연결. 2024 target958820ff, 현행fd416d42를 구분한다. 2022 즉시target과 모든replica 정상화는 HOLD/미확인. 카탈로그 병합승인은 소비자 지문/복제메타데이터 정상화를 보장하지 않았다.',
    current='2026현재 AcoustID track은 targetfd416d42 하나를 보이고 2024 Fingerprints URL도 그 target으로 도착한다(웹 도구 관측; HTTP코드 아님).',
    missing='2022즉시 target/중간redirect chain 미확보. 당시 지문 결함은 소비자·운영자 진술이며 재실행 없음. 현재 모든 replica 상태 없음.')

add('ROR01','https://ror.org/000qg0t28',
    'COMTES FHT 회사의 연구조직 등록을 확인하는 연락처 링크.',
    'rc-v1.55/new/000qg0t28.json: COMTES FHT a.s., active, nonprofit. 같은 시기에00hzjtg80은 COMTES FHT company였다. 근거는 ror-updates fixed commit baffbf2b52cf09acd3dc29ef808d91c4a1aca278의 두 changed record; 실제 회사 Contacts도000qg0t28을 인용한다.',
    'issues15331→15407: 언어별 홈페이지 차이를 같은 회사 중복으로 승인. rc-v1.56에서000qg0t28 withdrawn, successor00hzjtg80; 수정2024-11-19, release댓글11-20. 현실 회사합병이 아니라 catalog 중복정리다.',
    '좁은 회사찾기 목적의대상은 같은COMTES, 현재 대표후보00hzjtg80. 과거 catalog record는000qg0t28의withdrawn역사를 남겨야 한다. 현재 resolver HTTP와 소비자 최초작성/수정일을 확인하지 않아 클릭성공·자동이관을 단정할 수 없다.',
    missing='ROR resolver HTTP 미확인; 전체dump 미검증; 회사Contacts 최초작성일/수정일 없음.')

add('ROR02','https://ror.org/01dbbht76',
    'National Center for PTSD Pacific Islands Division 연구 소속을 표시하는 링크.',
    'issue13495의 제안은 본부04xv0vq46와 Pacific Islands Division01dbbht76를 같은 조직으로 묶자는 것이었다. 저장 대상은 division이다. 불변 before/after 전체dump는 확보하지 못했다.',
    '2024-11-05T18:34:53Z 기각댓글은 논문이 이 division을 소속으로 인용하므로 구분을 유지해야 한다고 판단했다. issue종료는2024-12-02. 적용병합이나 rollback이 일어난 증거는 없다.',
    '소속단위01dbbht76/Pacific Islands Division을 유지. 본부04xv0vq46로 대체하면 인용단위를 넓히므로 부적절. 기각판정은 직접확인, 전체dump에서 두record가 불변이었다는 실증은 없음.',
    missing='기각 원문은 있으나 전후 전체dump/해당 논문 원문/현재 HTTP는 미확인.')

add('ROR05','https://ror.org/01sxmzj91',
    'Zürcher Fachhochschule의 옛 기관 평가기록을 확인하고, 가능하면 현재 문의처도 찾는다. 전공·프로그램은 지정하지 않았다.',
    'rc-v1.23에는 active umbrella institution01sxmzj91. EQAR institution205는 옛 ID와2009–2021 평가기록을 보존한다. 이 표현에 특정 후계나 프로그램은 기록하지 않았다.',
    '현실기관 종료는2023(요청/EQAR). issue20329 및 rc-v1.67은2025-06-24 inactive+successors05pmsvm27,02ejkey04,05r0ap620,01awgk221을 기록. 옛외부ID와기관기록을 남긴다.',
    '옛평가기록은01sxmzj91라는 역사대상에 남는다. 현재 문의처는4후계중 목적/프로그램이 없어 하나로 결정할 수 없으므로 병렬후보 또는 HOLD. ③으로도정답후계 하나를 만들지 않는다.',
    missing='문의 프로그램/학과 없음. 전체dump·현재 HTTP·EQAR 최초수정일 없음.')

add('ROR06','https://ror.org/04xjkmz40',
    'Universidad Cuauhtémoc San Luis Potosí 캠퍼스의 연구 소속을 가리키는 링크.',
    'rc-v1.66(2025-05-20)04xjkmz40의 이름/사이트는 San Luis Potosí. issue19416에서 그 ID를 수정했다. 이전Puebla 원판 전체파일은 확보하지 못했다.',
    'issue25805는 본교ID를branch로 바꾼 수정이었다고 판정. rc-v1.72(2025-10-06)04xjkmz40은Puebla parent로 복구되고 SLP child02qmmxm27이신설된다. 본교의기존external IDs는본교에남고 새child에는없다.',
    '저장된SLP소속주장은당시04xjkmz40 metadata가표현했으나 catalog원ID는Puebla본교. 정정후SLP는02qmmxm27. 본교externalIDs를child에자동복사하면안됨; 최초Puebla판/소비자인용복구는미확인.',
    missing='오염 전Puebla 전체record/독립 소비자 사전 인용·현재HTTP 없음.')

add('ROR07','https://ror.org/041xzk838',
    '스페인 Biofisika의 연구기관 정보를 찾으려는 링크.',
    'rc-v1.38(2023-12-07)041xzk838의 이름은Instituto Biofisika, websitebiofisika.org, locationLeioa/Spain. GRIDgrid.419463.d, ISNI0000000417563731, WikidataQ30282132가들어있다. 이외부ID 발급기관본문은제공되지않는다.',
    'issues6693→16454→17073은이탈리아기관ID에스페인정보를넣은오류로판정. rc-v1.60(2025-02-26수정/27배포댓글)은이탈리아Instituto di Biofisica, ibf.cnr.it, CNRparent04zaypm56로복원하지만 location은Leioa/Spain이남는다. 현재CoLab은스페인,OpenAlex는이탈리아로같은ID를설명한다.',
    '원추천의미는스페인기관이지만041xzk838의정정된대상은이탈리아CNR기관. 스페인에알맞은ROR ID는이자료로미확정→HOLD. 역사판은옛주장의내용을복원하지만그주장을옳게만들지는않는다. 이름·부모복원과location정합성은다르다.',
    missing='오류전v1.37원판/외부ID발급기관원문/정확한Spanish대체ROR/실소비자수정날짜없음.')

add('ROR08','https://ror.org/01fva0642',
    'Netrokona University 소속을 설명하는 링크.',
    'issue19286 및rc-v1.66(2025-05-20)01fva0642에Netrokona 이름이들어있다. 별도05ktf0c82의이전명은Sheikh Hasina University. 두record에는서로다른외부ID가있다.',
    'issues21008+21009,rc-v1.68(2025-07-15):01fva0642를Gazipur Digital University/bdu.ac.bd로복구; 실제Netrokona ID05ktf0c82는Netrokona University/neu.ac.bd로이름변경하고Sheikh Hasina를alias로보존한다.',
    'Netrokona소속은05ktf0c82.01fva0642는Gazipur이므로oldlink그대로면의미불일치.05ktf0c82의rename은정상별칭,01fva0642의rename은다른기관혼동이었다.법적개명공고/현재resolver는미확인.',
    missing='정부개명공고원문/실소비자사전인용/현재HTTP없음.')

add('SW01','https://github.com/Homebrew/homebrew-core/blob/master/Formula/tinyfugue.rb',
    'TinyFugue tf-50b8 배포물을 찾는다. 과거 빌드 패치의 완전 재현은 요구하지 않는다.',
    'parent89b2018d807cca3e3f2d127a973991d680c3aa46의Formula/tinyfugue.rb version5.0beta8과기존tiny-fugue5.0b8은같은tf-50b8 upstream archive URL을쓴다. 두recipe의패치/설치옵션은다르다. 파일본문직접확인; archivebytes비교없음.',
    'commit7f379ed5e4135654176204310ae0f24af0826eaa,2011-10-28:중복tinyfugue recipe를삭제하고tiny-fugue로alias를둔다. 기존recipe를유지한다. 실행상설치재현은하지않았다.',
    '배포물찾기목적에tiny-fugue가승인된동일배포물후보. 이름/메타데이터차이를모두분리하면중복을남김. 단순alias는이목적에충분할수있으나현재redirect/설치성공과exactrecipe재현은별도.',
    missing='저장URL은실제옛recipe경로로만든연구보기이며독립소비자가저장한증거아님.현행경로HTTP/설치재현없음.')

add('SW02','https://github.com/Homebrew/homebrew-core/blob/master/Formula/lib/libxml++3.rb',
    'libxml++의 major3 배포물을 찾기 위한 formula 링크. exact 빌드 recipe는 요구하지 않는다.',
    'parent4ea8a912eaa74d7606b2c7307899d7c9faf399c5의libxml++3.rb는3.2.4와고정sourceSHA256을기록한다. fixed parent본문은GitHubconnector로읽었다. HTTP503을받은별도고정URL과본문확보를구분한다.',
    'commiteb1463eb72712952a10ecdfc201592ca4d24a20a,2023-12-26:libxml++3→libxml++@3;formula_renames매핑.전후archiveURL/SHA256/version3.2.4동일. build/homepage에는변경도있다.',
    'major3탐색에는libxml++@3정상alias가충분할수있음. exact3.2.4나oldrecipe를재현하려면fixedparent를유지. 현재oldfile404는역사본문소실을뜻하지않음.',
    current='2026-11-22 old main recipe URL의HTTP404를관측. 고정판본문은별도경로로확보했다는사실만공통제공하며내용/후계는이필드에넣지않음.',
    missing='실제brew설치·업그레이드미실행.현행alias동작HTTP실험없음.')

add('SW03','https://github.com/Homebrew/homebrew-core/blob/master/Formula/gnu-readline.rb',
    'Homebrew에서 GNU readline 6.2.4를 설치할 때 쓰는 formula 링크.',
    'parent e2f98568822c4f3f9b180b77a2ef10236189e2fa에는gnu-readline6.2.4및readlinealias가있다. sourcearchive는GNU readline. 원rename adee5315265cc46aa6a3057071527abb16e1cd94객체는접근불가.',
    'revert8c2998215320942b1329f5b073fad7bfa33e9976,2012-11-11은canonicalname을readline으로복구하고의존recipe이름도돌렸다. 편집자는alias이름의기존keg를canonical로찾지못해작업이깨진다고설명한다.',
    '배포물GNUreadline6.2.4는같으나설치ID/canonicalkeg경계때문에정정판readline을참조해야함. 의미상오병합과이름변경롤백을분리. 실제실패는저자진술,이번설치실험없음.',
    missing='최초rename객체미확보;parent/revert는확보.실제설치·소비자후속인용실험없음.')

add('SW05','https://formulae.brew.sh/formula/postgresql',
    'Rails 개발환경에서 당시 최신 PostgreSQL을 설치하려는 이름 postgresql.',
    'rename직전parent b354eba6f430f0da6b5f8e8d24c25c0411fab517의unversionedpostgresql은14.5. 독립Rails Brewfile은postgresql이라는이름을사용했고후속수정의사유는최신판선택이다.',
    'commit8060df9169055ee1fb9d1d69fd149c3922e864ba,2022-08-27:postgresql→postgresql@14(14.5_1),데이터경로도versioned. Rails commit27cb8c618ca3a96a2817e412bfe48dc29a6acfa3,2024-05-23은이름이14로연결되어최신이아니므로postgresql@16+libpq로고친다.',
    '2022역사배포물은14.5,canonical후계@14.그러나2024Rails최신개발목적정답은@16+libpq.2026최신을추측하지않는다. 관계후계와사용목적대체는별개이며데이터path변경도남겨야함.',
    missing='사용자의DBmigration/설치재현없음.최신이라는시점기준이변하므로2024수정범위만판정.')

add('SW06','https://formulae.brew.sh/formula/tree-sitter',
    'tree-sitter generate 명령으로 parser를 생성하려는 설치 링크.',
    'parent5d3c6448fe87f35290fe191a0f80b9e4c189a63d의tree-sitter0.25.8은library와CLI를함께설치했다. source archive/recipe본문확인. 의도한기능은generate명령이다.',
    'commite5e819e64a3104cabb55d46ea8e80d69aaf76d5b,2025-07-29:tree-sitter는library0.25.8_1,tree-sitter-cli0.25.8신설. irlm/workbench가2026-11-04brew항목을CLI로정정. AgentScript는2026-05CLI필수요건을추가하나당시Homebrew0.26.x와필요0.25.x차이도드러난다.',
    '옛추천기능은CLI generate.현재libraryURL200만으로기능보존되지않음.기능후계tree-sitter-cli,역사판0.25.8을명시하고consumer필요판을검사해야함. latestCLI자동선택은판호환성보장아님.',
    current='2026-11-22T03:13:41.897956Z oldformulaURL HTTP200,내용은library0.27.2. CLI를설치하는recipe가아니다.',
    missing='실제설치/빌드재현없음.소비자reportedfailure와catalogdiff를구분.일반사용목적에서요구CLI판은추가지정필요.')

add('WD01','https://www.wikidata.org/wiki/Q55296215',
    '법원 건물 Q314104의 topic main category(P910)를 가리키는 링크.',
    '건물Q314104의revision936463156에서P910은categoryQ55296215.별도법원institution은Q59165607.외부ID:건물Berlinheritage09066442,기관GND2130826-3;발급기관원문은미제공.',
    '2019-10-24merge1038289881에서category를institution으로합침.10-26bot revision1039041773이건물P910을Q59165607로치환.11-08T10:36undo1048159568로기관merge를되돌리고,10:37에별도consumerundo1048159950으로P910을Q55296215로복구.',
    '정답은categoryQ55296215이며institutionQ59165607와buildingQ314104와다름.원mergeundo만으로P910복원되지않아별도undo필요했다.확인한consumer1건이외전체인용복구/원category자체복원revision은미확인.',
    missing='category자체restoredrevision/모든incominglink전수검사/외부ID발급기관원문없음.현재HTTP미확인.')

manifest_path=P/'evidence/frozen-manifest.json'
if '--verify' in sys.argv:
    m=json.loads(manifest_path.read_text())
    for f,h in m['sha256'].items():
        assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h, f
    print('Frozen files unchanged:',len(m['sha256']))
    raise SystemExit(0)
if manifest_path.exists():
    raise SystemExit('Refusing to replace frozen views/key; use --verify')

ts=datetime.now(timezone.utc).isoformat()
def out(path,obj):
    f=P/path;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

shared={
 'question':'저장 이유가 어느 대상/기능·판을 말하는지 복원하고, 현재/정정판에서 쓸 목적지를 하나 고를 수 있는지 판단하라. 역사적 주장을 복원하는 것과 그 주장이 옳다고 승인하는 것을 구별하라. 제공 정보 밖은 미확인/HOLD로 답하라.',
 'method':'짧은 이유는 실제 사건 문맥에서 연구자가 만든 통제된 보기이며 실제 저장 추천문을 복사한 것이 아니다. URL 문자열은 그대로 노출한다. current_lookup은 세 표현에 동일한 직접관측만 제공한다. 외부 열람 없이 답하라.',
 'missing_rule':'같은 사건에는 같은 원자료 풀과 동일한 접근불가가 적용된다. ②는 역사필드,③은관계/정정이력을 추가한다. 미확인을 실제정보소실로 바꾸지 말라.'
}
order=list(range(len(cases)));random.Random(2301).shuffle(order)
for level in [1,2,3]:
    cards=[]
    for i in order:
        c=cases[i]
        row={k:c[k] for k in ['event_id','saved_url','short_reason','current_lookup']}
        row['common_missing']='공통 원자료 풀에서 미확보한 원판·HTTP·소비자 이력은 어떤 표현에서도 채워 넣지 않았다. 미표시 정보를 실제 정보소실로 간주하지 말라.'
        if level>=2:row['saved_historical_id_version_and_locator']=c['historical']
        if level>=3:row['saved_relationship_and_effective_history']=c['history']
        cards.append(row)
    out(f'reconstruction/views/view-{level}.json',dict(**shared,representation=level,cards=cards))

key=[]
for c in cases:
    key.append({'event_id':c['event_id'],'post_edit_key':c['key'],'key_scope':'자료에 나타난 정정/승인 범위; 원문에 없는 완전한 복원 정답을 만들지 않음','known_missing':c['common_missing'],'source_pool':[{'source_id':s,'url':S[s]['url'],'sections_read':S[s]['sections_read']} for s in c['source_pool']],'historical_input':c['historical'],'history_input':c['history']})
out('reconstruction/key/answer-key.json',{'created_at_utc':ts,'author':'/root; source-exposed internal researcher','cases':key})
paths=[f'reconstruction/views/view-{i}.json' for i in [1,2,3]]+['reconstruction/key/answer-key.json']
manifest={'created_at_utc':ts,'source_exposed_authors':['/root','/root/musicbrainz','/root/ror','/root/software'],'reader_plan':'three fresh fork_turns=none agents, one view each, no other files or web; same model family, not external human blinding','order_seed':2301,'sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in paths},'scoring_rule':'root source-exposed self-check after answers; target and function/version/reason separately PASS/PARTIAL/HOLD/WRONG/UNVERIFIED; unknown key/access kept in denominator; no causal rates'}
out('evidence/frozen-manifest.json',manifest)
with (P/'evidence/exposure-log.jsonl').open('a') as f:
    f.write(json.dumps({'at_utc':ts,'actor':'/root','action':'freeze views separately from key before reader assignment','files':paths,'exposure':'root has seen all sources and key; not blind','sha256':manifest['sha256']},ensure_ascii=False)+'\n')
print(json.dumps({'cases':len(cases),'frozen':paths,'at_utc':ts},ensure_ascii=False))
