# AF-RES-023 진행 기록

## 시작 2026-11-22 03:10 UTC

- 입력 source `7f66165ad68610278df18855e1196a6cf52b035a`, 의존020 `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35`, 계획 `b507fbcab09724a77270e658355f4b661cc35f02`.
- 지정 브랜치 생성, 고정 입력 읽기, manifest 생성 exit0. GitHub 연결 계정은 저장소 소유자 laadkke-arch.
- 첫 커밋 전 익명 HTTP 확인: 03:09:15–18 UTC. musicbrainz.org/search/edits 403, wikidata.org/wiki/Special:Log 403, api.github.com 403, ror.org 403, github.com/ror-community/ror-updates 200, github.com/Homebrew/homebrew-core 200, docs.brew.sh 200. 403은 shell 경로의 결과며 공식 web 열람 도구 지원 여부는 별도 기록한다. 우회하지 않는다.
- Python requests 미설치로 초기 네트워크 확인은 실행 전 실패했다. 표준 urllib로 재실행하여 위 응답을 관측했다. 새 패키지 설치 없음.
- 병렬 담당: musicbrainz / ror / software. root는 Wikidata 보강·자료 통합·분리된 복원 판독·검증·커밋을 맡는다. 모두 같은 모델 계열 내부 조사다.
- 남은 일: 실제 사건18+·정책6+·독립consumer6+의 원문과 전후판; 보기/키 분리; 18×3 비교; 교차 반례; self-check; 최종 handoff.

## 커밋 원장

첫 커밋 자신의 SHA는 저장 뒤 다음 묶음에서 기록한다. 최종 커밋은 HANDOFF 단독이며 자신의 SHA 대신 원격 branch/path와 부모검증판을 안내한다.

## 묶음1 원격 확인

- 원격 scope 커밋 `68269ef22b4b07e751fcc3093361e8d5b390dda9`. GitHub fetch_file로 SCOPE 바이트를 다시 읽고 fetch 후 로컬 HEAD를 같은 커밋으로 맞췄다.
- 최초 로컬 커밋 bf5bd8f는 HTTPS push 인증정보 부재로 원격에 올라가지 않았다. 기존 승인된 GitHub 연결 도구의 tree/commit/branch 동작으로 같은 파일을 저장했다. 새 인증정보·계정·권한은 만들지 않았다. 인계 기준은 위 원격 SHA다.
- Wikidata WD01 실제 merge1038289881→undo1048159568, 별도consumer1039041773→1048159950 확보. 정책3개 직접읽음. 역사페이지 일부가 막혀 해당 후보는 제외원장에 남긴다.
- 추가 공식호스트 shell 관측: phabricator.wikimedia.org/T237262 403(03:15:17Z), commons.wikimedia.org portrait403(03:15:21Z). 웹 본문열람은 성공했으며 HTTP코드와 혼동하지 않았다.

## 묶음2a — Wikidata 원격 저장

- 커밋 `add402d0203693fa2d0c9efc3b07a9e9d9a614fb`; 고정판 events.jsonl을 GitHub에서 다시 읽고 로컬 fetch로 동일 HEAD 확인.
- 다음 소프트웨어 묶음은 core5사건(SW01/02/03/05/06), 보충SW04, 정책3, 독립소비자3. HTTP200이면서 CLI가 빠진 tree-sitter와 현재404인 libxml++3 파일의 고정판 열람을 분리했다.

## 묶음2b — 소프트웨어 원격 저장

- 커밋 `60cb76c1a8f64abe585a99a789833450446ce7af`; 고정판 software/events.jsonl 다시읽기·fetch 확인.
- ROR core6은 ROR01/02/05/06/07/08, 보충03/04. 같은 ID의 대상 오염 정정과 literal merge를 분리한다. release-candidate 고정 JSON과 배포댓글을 구분하며 전체 release dump를 읽은 것으로 쓰지 않는다.
- root가 ROR rc-v1.38/rc-v1.60의041xzk838 고정JSON을 직접 재열람: 이탈리아 이름·도메인·부모로 정정한 파일에도 Spain/Leioa 위치가 남는다. 현재서비스전체오류가 아니라 이 고정파일의 불일치다.
- root가 Homebrew readline rollback 및 tree-sitter split 고정diff, AcoustIDissue114 본문을 재열람했다. 편집자실패설명과 이번실행검증을 분리한다.

## 묶음2c — ROR 원격 저장

- 커밋 `c5fb3e8d4e923a94b6f0cf79efc527d8cd2114d1`; 고정판 ROR 사건 원장을 GitHub에서 다시 읽고 fetch했다.
- MusicBrainz MB01의 최초 merge151147443와 retained 지역정정152539607를 보강했다. source f0a68a45는 커버 이미지 파일명 계보에서 추론한 매핑이므로 확정 source href로 취급하지 않는다. MB03/04의 사라진 source MBID와 MB06의2022중간 target은 아직 미확인이다.
- Agent Script issue33을 root가 직접 재열람했다. 옛 formula 이름을 추측하면 library가 설치된다는 사용자 진술은 있지만, 분리 전 저장한 실제 링크의 이력이 아니다. Q5의 엄격한 사전 인용 6건 분모에는 이 기록을 포함하지 않는다.

## 묶음2d — MusicBrainz 원격 저장 및 보기 고정

- 커밋 `64644506d75dad84de350d53d354320d65ae4786`; MusicBrainz events 고정판 GitHub 재열람과 fetch 완료. 원문 46행은 같은 사건 중복화면을 포함하므로 46사건 또는46독립근거로 세지 않는다.
- 통합 본표본은18사건: MusicBrainz6, ROR6, Homebrew5, Wikidata1. 고유원문 최소수는 보수적으로38=사건18+정책12+소비자원장8. 소비자8중외부기관독립은7이며, 날짜가확인된후속체인은4(외부3+Wikidata내부1)다.
- ROR 댓글 created_at을 추가로 확인했으며 PTSD 기각2024-11-05와 issue종료12-02를분리했다. 포크SW-F01와현실기관합병ROR-X1은본18사건에산입하지않고교차분야검증에쓴다.
- 03:36:33 UTC에 보기1/2/3과답안키를분리고정했다. evidence/frozen-manifest.json에SHA256및순서를저장. root/수집자는정답노출. 다음독립문맥3개는한보기씩만읽고답하며,채점은root의자기점검이다.

## 묶음3 준비 — 별도 판독 답안 고정

- 보기/키 고정 원격 commit `7f6fc6f7da84b5a2401e287abb8ec1f1c9ed1837`; manifest를 GitHub에서 다시 읽고 fetch했다.
- reader_1/2/3은 각각 view-1/2/3만읽는 새문맥으로18행씩답했다. 외부/정답미열람은과업제한과자기보고에근거하며외부감사증거는아니다. 입력해시가고정manifest와일치한다.
- 답안54개를채점전별도고정한다. root채점은사후정정원문노출자의자기점검이며서로다른사람의독립맹검이아니다. 다음은6사건씩비교CSV커밋이다.

## Q6 사전 입력 감사와 재판독

- v1 답안 commit `9eb153d6e33f0ee6ef9f6fca8170c3b163d3e5a8`를원격재열람했다. 감사자가발견한경로/공통ID표기3건은v2에서고쳤으나,②관계정보혼합도발견해판독배정전v3를추가고정했다. v2에는판독자가없다.
- v1보기/키/답안을변경하지않는다. v3키는v1과동일SHA256. 차이는protocol-errata에기록. 본표는새판독자3명의v3답안54행이며v1의SELECT수는운영효과근거로사용하지않는다.

## 묶음3 본 비교 답안 고정

- v3보기 commit `5ac71a3821baa0daa0d0e37a2813b629fbc7065e`; GitHub고정manifest다시읽기/fetch확인.
- 새판독자 final_reader_1/2/3의v3답안은18행씩54개. 입력해시는모두고정v3와일치. 이전답안이나정답을읽지않도록제한했고자기보고도보존한다.
- 다음채점에서과거대상/기능판/현재선택을나누고원문키의빈칸은그대로남긴다.

## 비교 입력 최종 대조

- v3답안원격commit `ae3315ba734067f57ed98702e50636e5c5cd87f9` 확인. 원문은있지만보기에서생략된MB05생존target/SW03정정후버전2개를발견했다. 해당값을추가한v4의2사건을새문맥으로재판독한다. 다른16사건48행은카드해시일치로이전답안을유지한다.
- 이는실제관계미보존을찾은결과가아닌연구보기작성오류이며protocol-errata에구별했다. 이보강후선택적추가실험은멈추고표·검사·인계로진행한다.

## 두 사건 재판독 완료

- v4입력원격commit `c2f3f3c2d2056fe1a34546154f3590a46c7391eb` 고정manifest재열람/fetch확인. 감사자가MB05생존target과SW03정정후6.2.4를기존원문원장으로재확인했다. 다른16건에서같은유형누락을추가발견하지못했다.
- 새repair_reader_1/2/3답안각2행을고정한다. 입력해시/공통질문/방법/누락규칙이계획과일치. 최종비교는16×3이전행+2×3재판독=54행이고단일54행재실행이라고쓰지않는다.

## 비교 묶음3a — 음악6사건×3

- 재판독답안 commit `fadda010c9ddf714be861dc3888666db705d23b6`를GitHub에서다시읽고fetch했다.
- MB01–06의18행자기점검완료. MB03①은B4라는문맥을추가검증하지않았다고단서를달면서retained2:32를SELECT했으므로요청대상과다른선택으로기록했다. 사람이실제로오추천을받았다는결과는아니다.
- MB04는단순URL/짧은이유만으로좁은recording목적을찾는반례. MB01③도실물matrix없이는조건부다. MB05의카드누락수정전HOLD와최종재판독은별도답안파일로보존한다.

## 비교 묶음3b — ROR6사건×3

- 음악비교 원격commit `b2879a0e669268ca4a7fdfada63bb7d3ed8570c6`; B01.json고정판재열람/fetch확인.
- ROR01/02/05/06/07/08의18행추가,누적12사건36행. ROR06②의SELECT는당시v1.66판재현에제한되어있으므로현재정답이라고단정한오류로과장하지않았다. 이값을정정후SLP ID로재사용하면부적합이라는경계를기록했다.
- ROR05②의SELECT는EQAR역사평가기록만가리킨다. 현재문의처까지선택한것으로합산하지않는다. ③도목적이없어후계하나를고르지못한다. ROR07스페인정답ID는③에도미확인이다.

## 비교 묶음3c — 소프트웨어5+Wikidata1

- ROR비교 원격commit `db9d7fe9bace6cd45ee6c76fbd9aa0ddeda945c9`; B02.json고정판재열람/fetch확인.
- 마지막6사건18행을추가해최종18×3=54행이다. 목적지SELECT/HOLD/CONDITIONAL은판독자코드를그대로보존하고,역사기록만선택한행과현재/정정목적선택을분리했다.
- SW01②는같은배포물URL이라는고정정보만으로좁은목적후보를선택했다. SW02③은정상alias,SW06③은기능후계와판조건을구별한다. WD01은본체undo와P910복구를따로복원한다.
- 다음:필수표4개/교차분야보고서,원장정합검사와session check,SELF_CHECK/acceptance선행commit,그뒤HANDOFF단독commit.

## 묶음4 — 교차 분야·마지막 자기 점검

- 마지막비교commit `d05b7269a0eeff7a0958de5c58dba9744e4a2a5a`; B03.json고정판재열람/fetch확인.
- RESULT의필수4표와끝약점3행,독립식별열18/복원필드90,교차분야2쌍·네관점을작성했다. 내부감사자는최종54행의원답안/보기동일성과숫자·판정범위를대조했고추가실질오류를찾지못했다.
- 정합검사41항목exit0. 초기CSV boolean대소문자검사기오류1건은수정후재실행했고실제데이터숫자는바뀌지않았다. session check --fetch도04:07:39 UTC에exit0/remote_checked.
- Q1–Q7핵심원문7개를마지막재열람했다. RORv1.60의위치잔존과WDP910별도undo,MBmerge상태,AcoustID후속문제,libxml3.2.4고정본문,포크기본값차이를다시확인했다.
- SELF_CHECK/acceptance를이묶음에서먼저커밋한다. 그뒤에만HANDOFF를작성해단독최종커밋하며,상태는REVIEW_READY_WITH_GAPS다.
