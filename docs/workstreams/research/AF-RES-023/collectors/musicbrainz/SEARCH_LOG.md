# MusicBrainz 검색 및 접근 기록

관측일: 2026-11-22 UTC. 실제 clock 확인 03:12:26 및 03:16:04. 개별 검색 초 단위 시각은 저장하지 않아 소급 생성하지 않았다. 읽은 원문별 절과 edit ID는 `sources.json`에 있다. 이 collector는 `/root/musicbrainz`, GPT-6 Astra Pro이며 같은 연구팀의 자료 수집자다. 독립 복원 평가자가 아니다.

## 검색 창과 경로

기간을 처음부터 한 연도로 제한하지 않았다. 목적 표집으로 실제 오병합·split·거부·정상 중복을 찾았으며 검색 중 발견한 2017–2026 사건을 선택했다. 검색 결과 snippet은 최소 원문 수에 넣지 않았고, 공식 편집 이력 본문 또는 발언 원문을 연 뒤에만 `counted=true`를 붙였다. 이 표식은 **고유 문서 원장 표식**이며 동일 사건의 여러 화면을 독립 사건·근거로 세라는 뜻이 아니다. root 통합에서는 사건당 대표1개 등 더 보수적으로 다시 센다.

| 검색·열람 경로 | 실제 연 원문/ID | 결과 및 반례 판단 |
| --- | --- | --- |
| system2: `site:musicbrainz.org/edit "merge" "incorrect"`; `"Failed vote"` | 정책 위주로 반환; MB-S01–04 직접 열람 | 실패 투표의 단순 검색은 사건 원문 회수율 낮음. 정책만으로 실제 성공·실패를 채점하지 않음. |
| system1: `site:musicbrainz.org/edit/ "Merge" "Failed vote"`; `site:community.metabrainz.org "wrong merge" edit`; `site:musicbrainz.org/edit/ "unmerge"` | forum815567, edit history152536177/152589926 | private music의 실제 재생성·DiscID 복구 확인. 최초 merge ID 미회수. |
| system2: `site:community.metabrainz.org "unmerge" "edit/"`; `"incorrect merge" "edit"`; `"merge" "rejected"` | forum713181; recording132ded03 history63656996,115752742,115760023,115752723 | merge가 아니었던 ID 재사용을 별도 SPLIT로 분류. 취소된115752723을 성공으로 세지 않음. |
| 같은 검색의 실제 연결 추적 | forum442657; edit60587125; release5aeb8c8f history63762772/63972905 | 오케스트라 유무가 다른 녹음물이라는 진술과 실제 medium 참조 교체를 연결. 원source MBID는 여전히 미노출. |
| system1: `"merge" "voted down" "edit"`; `"Failed" "Edit #"`; `"rejected" "musicbrainz.org/edit"` | forum482731; edit66223421 열기 실패; forum336413; history48434703/48447069 | 정책상 fade/침묵을 같은 것으로 볼 수 있다는 반론을 보존. 실제 거부 상태 미확인이라 본사건 제외. Neththara는 누락을 먼저 고친 뒤 중복 병합한 실제 반례. |
| forum472246의 편집 링크 추적 | edit68967621; recording7a3eb993 | Back Again 5yes0no Applied; 여러 release와 두 ISRC 표시. 다른판=다른recording이라는 과분리의 반례. |
| system2 exact MBID 검색에서 `-site:musicbrainz.org -site:community.metabrainz.org` | 유용한 독립 소비자 결과 없음 | 외부 파일에 같은 ID가 쓰였을 것이라고 추정하지 않음. |
| system1: MusicBrainz merged old MBID beets; beetbox issues; community redirect | acoustid/acoustid-server#114; edit92853437; AcoustIDb847e16e | 실제 소비자 old-ID 잔존과 운영자 재가동·복제 누락 인정 확보. 별도 서비스라도 같은 사건 chain을 피해2건으로 세지 않음. |
| AcoustID issue의 공식 링크 따라가기 | Fingerprints958820ff → fd416d42; current AcoustIDb847e16e | web도구 redirect 보고 및 현행1개MBID 표시. rawHTTP 상태 코드는 미측정. 2024 URL을2022즉시대상으로 소급 안 함. |
| 추가 반례 토론 원문 열람 | forum572207/AcoustID7a7b06b2; forum482379; forum373187; forum714654; edit81215318 | 지문 하나의 복수판, 동명음악인, 수동복원, old-ID잔존, 추가정상merge를 읽음. 주6사건과 별도 보조 자료로 유지. |

## 접근 실패와 공식 대체 경로

| 실패 원문 | 실제 관측 | 정상 대체/남은 최소 입력 |
| --- | --- | --- |
| MusicBrainz 일반 shell 요청 | root가403을 관측했다고 공유 | 이 collector는 web search/open의 공식 원문을 사용. shell403을 재시도하거나 우회하지 않음. |
| edit notes 전반 | 공개 edit 화면에서 로그인 요구 | 노트 대신 공개 change/status와 실제 forum원문을 읽음. 노트 내용·투표 이유를 만들어 쓰지 않음. |
| release893fa571 full edits | inaccessible; 두 번 열기 실패 | 새Europe0243... history와 공식 편집검색 결과의131420900/137042427 본문 확인. 최초mergeID는 다음 공식 dump 관련행 필요. |
| edit66223421 및 공식edit검색 조건 | inaccessible/429 | forum482731의 거부보고만 남기고 사건기준 미충족. 다음 입력은 실제 edit상태·양쪽MBID·당시vote내용. |
| direct edit63762772,115760023,48447069,152536177 | 2026-11-22 03:16 이후 직접 URL은 inaccessible | 해당 edit의 실제 변경내용·날짜가 실린 공식 entity history 화면은 직접 열람 성공. URL별 접근 결과를 혼동하지 않음. |
| old recordingfa9c940c 및958820ff overview | inaccessible | issue의958820ff/fingerprints 링크는 도구가fd416d42로 이동 후 원문 열람. HTTP코드는 여전히 미확인. |
| new Les Princes05d666f0 overview | 429 | 원 recording history의115760023 링크 href에서새MBID확인. 생성편집/현행내용검증 필요. |
| old Neththara da729585 | 429 | 두oldURL이 명시된forum와target633a... history로 merge내용확인. rawredirect미확인. |
| recording2775d583 /edits 및7a3eb993 /edits 일부 | 429/inaccessible | release5aeb... history와개별60587125/68967621로필요범위확인. |
| edit115576481 | 429 | 보조forum714654에서거론되지만사건수제외. edit81215318은별도직접열람성공. |
| doc/Merge_Rather_Than_Delete, doc/Merge | 429 | 다른정상공식정책4개직접읽음. 실패페이지snippet은산입제외. |

## 반증의 범위

- **같은 주소면 같은 판이다**는 MB02의 실제 이름 변경·참조 교체 이력 및 MB03의 같은 제목·다른 녹음물 분리와 양립하지 않는다. 다만 이 실행은 HTTP200을 직접 측정하지 않아 '200반례' 숫자로 쓰면 안 된다.
- **조금이라도 다르면 분리한다**는 MB05의 트랙누락 보완 뒤 실제 중복 병합, MB04의 여러release가 같은recording을 공유하는 허용 병합과 충돌한다. 음향동일성은 독립검증하지 않았다.
- **source merge가 끝나면 소비자도 복원된다**는 MB06의 실제 old-ID잔존 제보와 replication누락 인정에 반한다. 마지막 제보 이후2026현재모든replica상태는 미확인이다.
- **역사가 있으면 유일후계를 고른다**는 MB01·MB02·MB03에서 옛 사용목적/판 정보가 없을 경우 성립하지 않는다. 이 연구자의 해석이며 root가 세방식 재독해에서 점검해야 한다.

공개 로그의 목적 표집에서 전체 MusicBrainz 오병합률을 추산하지 않는다. 성공3·정정2·split1의 표본 비율은 검색·선정 결과다. 실제 거부 편집의 원문 회수 실패를 숨기지 않는다.

## 후속 보강: 원 병합 및 정상 공개 dump 경로

root의 before-ID 누락 지적 뒤 `edit68967621`, `edit60587125`, `edit92853437`, `private music musicbrainz.org/edit merge` exact검색을 추가했다. 검색결과만으로 새ID를 확보하지못했다. 두 녹음물 merge source행은 다시열어도 링크번호없는이름만표시된다.

private music forum815567의 post3 공식edit검색링크를따르니 직접entity history URL이실패했던것과달리 실제편집55건본문을읽을수있었다. 원merge151147443(2026-08-09열림,2026-08-16적용,1yes0no), retained지역수정152539607(2026-09-01승인)을확보했다. 과거coverart파일명7개에는f0a68a45-5423-460a-9791-345f900f90d9가남아있다. 동일이미지의후속삭제가893fa571에나타나 source이관계보를추론한다. 공개사용자명이query에들어간전체검색URL은보존하지않고 원edit주소와forum정확한navigation위치를남겼다. oldf0URL직접열기는429, 개인정보없는단순화검색URL은inaccessible였다.

공식Database/Download→MetaBrainz datasets→비로그인공개download링크→공식full export목록을직접열었다. 계정가입·로그인·제한우회없음. 고정snapshot20261121-002203의edit16G/core7G목록까지확인했지만데이터행을추출하지않았다. dump문서가설명하는역사보존과실제개별sourceID가추출되는지는구분한다.

공식 edit dump에 대한 실제 HEAD는 HTTP200, Content-Length17284315658이었다. 따라서 dump접근차단이라고기록하지않는다. 전체다운로드·데이터행추출은미실시이며고정입력과명령은DUMP_FOLLOWUP.md에남겼다.
