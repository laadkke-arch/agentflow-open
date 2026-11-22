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
