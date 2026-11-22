# MusicBrainz collector 인계

상태: **PARTIAL_EVIDENCE_READY**. 사건 6개, 식별·병합 정책 4개와 dump 보강 문서 2개, 본사건과 연결된 독립 소비자 chain 1개를 확보했다. 별도 Stole 소비자 chain은 merge ID와 전후 판을 확정하지 못해 보조 자료로 남겼다. 이 담당의 소비자 2개 목표는 미달이다. root가 전체 표본의 소비자 6개 충족 여부를 판정해야 한다.

## 파일과 실제 분모

| 파일 | 내용과 분모 |
| --- | --- |
| sources.json | 46행. 39개 직접 읽은 원문을 문서 원장상 counted=true로 표시. 3개 접근 실패, 4개 접근 안내·파일 목록은 별도. 39를 독립 사건 수 또는 독립 소비자 수로 쓰면 안 된다. |
| events.jsonl | 6행. CORRECTED_MERGE 2, SPLIT 1, SUCCESS_MERGE 3. 편집 ID·전후 ID·시점·복구 필드·한계·최소 후속 입력을 기록. |
| citations.json | 4행. 본사건 MB06과 연결된 2행은 동일 AcoustID chain이므로 소비자 사례 1개. 나머지 2행은 Stole 보조 자료. |
| SEARCH_LOG.md | 실제 검색식, 직접 열어 본 edit ID, 차단 경로, 반증 결과, 정상 공개 dump 접근 보강. |
| DUMP_FOLLOWUP.md | 실제 HEAD 검사 결과와 미실행 데이터 행 추출의 고정 입력·명령. |

동일 사건의 여러 화면은 root의 보수적 최소 수 집계에서 하나의 사건 계보로 묶는다. 공식 정책 4개도 같은 발급자가 생산했다. 문서를 다시 열어도 새 자료로 세지 않았다.

## 주요 사건

| 사건 | 실제 edit/정정 | 강한 관측 | 복원 판정 한계 |
| --- | --- | --- | --- |
| MB01 private music | merge 151147443 → 새 Europe 152536177, DiscID 152589926, 지역 152539607 | 원 merge Applied와 지역 정정·새 판 생성을 직접 확인. 과거 이미지 파일명에 f0a68a45 MBID가 남는다. | f0a68a45를 source에 매핑한 것은 원장 계보 추론이며 old route는 미확인. 새 ID 생성을 옛 ID 복원으로 부르지 않는다. |
| MB02 La Groupie / Les Princes | 잘못된 rename 63656996 → restore 115752742 + split 115760023 | 실제 라벨 복구와 medium3 트랙1의 새 ID 참조 | merge가 아닌 ID 재사용 사건. 취소 115752723 제외. 외부 소비자 수정 기록 없음. |
| MB03 Vysotsky 07 | merge 60587125 → medium 63762772 + work 63972905 | 실제 merge Applied와 후속 recording 참조 교체 | 오케스트라 차이는 편집자 진술. 원 source MBID·지문 이관 미확인. |
| MB04 Back Again | merge 68967621 | 5 yes / 0 no Applied. 여러 Beautiful Sky 판에서 동일 recording과 ISRC 2개 표시 | source MBID 미노출. 사후 독립 정정 정답표 없음. |
| MB05 Neththara | repair 48434703 → merge 48447069 | 누락 트랙 3·8을 보완한 뒤 16트랙 중복 판 병합 | 개별 status 화면 차단. 공식 history의 닫힘·merge 내용은 확인. 외부 인용 수정 없음. |
| MB06 Tu es folle | merge 92853437; AcoustID #114와 2025년 재가동 | 실제 old MBID 잔존 제보와 운영자의 replication 결함 인정 | live 교정은 현재 관측. 모든 replica 교정·오추천은 미확인. 2022년 즉시 target 미노출. |

## 복원표에 필요한 제한

정정 원문을 읽은 이 collector는 독립 blind rater가 아니다. 이번 파일은 이미 정정 내용을 포함한다. root의 보기 ①②③와 사후 정답표 생성·재독해에서는 열람 순서와 누가 봤는지 기록하고 같은 연구자의 자기 점검이라고 표시해야 한다. 성공 사건의 Applied 상태만으로 원 추천 이유가 완전히 복원됐다고 채점하지 않는다. MB04·05는 `accepted_no_correction_key`, MB01·06은 partial이며 MB02·03은 실제 확인한 정정 범위에 한정된 key가 있다.

공개 화면에 옛 ID가 보이지 않는 것은 서버 원장에 전혀 보존되지 않았다는 증명이 아니다. `ACCESS_UNAVAILABLE`, `HISTORY_NOT_EXPOSED`, `NOT_OBSERVED`, `NO_CORRECTION_KEY`를 구분했다. 소비자의 실제 결함 보고, 기계적으로 잘못 도착할 가능성, 실제 오추천 기록도 별개다.

## 옮길 수 있는 원리와 경계

같은 work가 다른 recording일 수 있고 같은 recording이 여러 release에서 쓰일 수 있다. MB01의 지역·matrix에 따른 발매판 구분은 MB03의 연주·편성에 따른 녹음물 구분과 다른 층이다. 소프트웨어의 프로젝트·기능·배포판과 비교할 수 있지만 MBID 정책을 package ID의 보증으로 옮길 수는 없다. 카탈로그 운영자는 자기 레코드를 합칠 권한이 있어도 AcoustID 복제 소비자의 행을 자동으로 통제하지 못한다(MB06). 모든 차이를 분리 사유로 삼으면 누락 데이터가 만든 실제 중복을 계속 남길 수도 있다(MB05).

## 가장 큰 약점 3개와 다음 확인

1. MB03·04의 source MBID 및 MB06의 정확한 즉시 target은 공개 렌더링에 없다. 다음 입력은 공식 dump의 redirect와 해당 edit_data 행이다. MB01은 이미지 파일명으로 old ID를 회수했으나 merge source 매핑은 여전히 추론으로 표시했다.
2. 본사건의 독립 하위 소비자는 AcoustID 한 chain뿐이다. 다음 입력은 MB01–05의 옛 MBID를 실제로 저장한 공개 파일·태그 로그와 정정 커밋이다. 현재 카탈로그의 내부 medium 참조를 외부 소비자로 세지 않는다.
3. 음원 동일성 및 정정 후 외부 태그의 완전성을 직접 검사하지 않았다. 다음 입력은 공개 비교 음원·실물 판 사진, old ID 태그 표본, 복제판 검증이다. 승인 투표와 현재 URL 표시만으로 모든 추천 이유가 복원됐다고 결론내리지 않는다.
