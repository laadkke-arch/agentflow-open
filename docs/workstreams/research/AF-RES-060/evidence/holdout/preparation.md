# 새 요구 모집 준비 — 아직 수집하지 않음

작성자 `/root/authority`. 이 파일과 collector는 SCOPE의 모집 규칙을 실행 가능한 절차로 준비한 것이다. 작성 시점에는 새 질문의 metadata·제목·본문 API를 열지 않았다. 공급자 F1 파일도 읽지 않았다. 루트가 단계2의 원격 고정 SHA를 전달하기 전에는 `collect-frame` 또는 `collect-bodies`를 실행하지 않는다.

## 고정 모집틀

- 현재 canonical 태그: `jsonschema`, `json-ld`.
- 생성 시각: UTC 2023-07-01 00:00:00 (`1688169600`)부터 2023-12-31 23:59:59 (`1704067199`)까지.
- 순서: creation_date 오름차순, 동률 question_id 오름차순. 각 분야 첫20건.
- API 수신의 answer_count/score/accepted_answer_id/owner/reputation 등은 출력·캐시 전에 허용목록으로 제거한다. 답/댓글 endpoint를 요청하지 않는다.
- `/questions`의 현재 태그·제목을 모집 metadata로 보존하고 `/posts/{id}/revisions`의 revision_number=1에서 최초 본문·제목·태그를 찾는다. 최초 태그가 없으면 현재 태그로 덮지 않는다.
- 최초 본문 결손을 현재 본문으로 채우지 않는다. 원문 실패 및 첫20의 부족은 미확보/미충원으로 남긴다.

## 동률 경계 처리

API는 creation asc로 가져오되 페이지 내 동률 정렬을 전적으로 신뢰하지 않는다. 첫20의 끝 시각에서 동률을 자르지 않도록 metadata 페이지(최대100건)를 받는다. 이미 관측한 끝 시각이 20번째 시각보다 크거나 모집풀이 소진되면 정렬 후 첫20만 고정한다. 페이지 끝이 경계와 같고 다음 페이지가 있으면 동일 시각의 다음 metadata까지 회수한다. 첫20 이후 metadata는 선정자에게 표시하지 않으며 추가 본문을 열지 않는다. 현재 사이트의 삭제/retag 이전 모집단을 복원한다고 하지 않는다.

## 봉인 확인

실수집 명령은 `stage2-gate.json`이 있고 그 안에 루트가 전달한 40자리 원격 SHA와 `root_confirmed=true`가 있을 때만 동작한다. 이는 입력 순서 실수 방지 장치이며 GitHub 권한이나 승인을 대체하는 장치가 아니다. preparation 단계에서 gate 파일을 만들지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-060/evidence/holdout/collector.py show-plan
# 루트가 단계2 원격 SHA를 확인한 뒤에만:
python -B docs/workstreams/research/AF-RES-060/evidence/holdout/collector.py collect-frame
python -B docs/workstreams/research/AF-RES-060/evidence/holdout/collector.py collect-bodies --tag jsonschema
python -B docs/workstreams/research/AF-RES-060/evidence/holdout/collector.py collect-bodies --tag json-ld
python -B docs/workstreams/research/AF-RES-060/evidence/holdout/collector.py show-bodies --tag jsonschema --start 1 --stop 5
```

## 독해·선정 산출물 틀

`frame.json`은 순서·현재 metadata·시각·gate SHA, `revision-index.json`은 최초 revision의 URL·GUID·본문 해시·현재/최초 태그와 결손, `requests.jsonl`은 요청·HTTP·원응답 해시·backoff·quota의 기술 기록이다. 응답의 사용자 reputation·답 수·점수·채택 답·댓글은 저장하지 않는다.

두 태그 모집틀에 같은 질문이 들어오면 `(tag, question_id)`별 행과 각 원순번을 모두 보존한다. 본문 캐시만 question_id로 공유한다. 두 번째 모집행에는 `body_cache_reused=true`, `reused_from_row`, 동일 `body_work_id`를 남기며 별도 외부 저작으로 더하지 않는다. 최초 본문을 회수/재사용한 사실과 사람이 읽고 적격성을 판정한 사실은 별도이므로 재사용으로 `read_status`를 자동 성공 처리하지 않는다.

`screening.csv`의 예정 열은 `tag,rank,question_id,created_utc,original_url,revision_url,revision_guid,current_tags_json,initial_tags_json,body_sha256,read_status,domain_eligible,C1,C2,environment,environment_basis,explicit_or_code_basis,independent_conditions,eligible,selection,exclusion_or_gap,source_id`다. 실제40본문을 읽은 뒤 채우며 준비 시점의 빈 값을 실제 미충원으로 보고하지 않는다.

본문 원문은 독해 동안만 `.cache/`에 두고 결과 커밋에 포함하지 않는다. 원전 전문을 공개 복제하지 않고 원 URL·revision GUID·SHA256·필요 최소 인용·자체 판정으로 근거를 보존한다. 선정된 첫 적격2건씩은 별도 `requirements-new.json`에 C1/C2·금지 행동·언어/판/옵션·guard·원문 위치·직접문장 대 코드에서 읽은 조건·연구자 양성/근접 음성 예로 정리한다. 기대 답이나 후보수로 교체하지 않는다. 새 L/V 용어는 정의 절을 확인한 후 별도 봉인하며 이 collector는 후보 순위를 계산하지 않는다.
