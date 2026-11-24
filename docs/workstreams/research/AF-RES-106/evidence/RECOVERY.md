# 재개 자료의 현재 권위와 보존 범위

2026-11-24 재개는 원격 봉인8054c2221d4023ba03c904d96f13928219d36c3d에서 이어졌다. 옛 작업 폴더의 미커밋 자료를 회수했으나 그대로 완료 성과로 취급하지 않았다. 00:16:52 UTC에는 현재 Matplotlib 담당자가 쓰지 않은 `sources.jsonl`, `STAGE3.md`, `finalize_stage3.py`의 갱신이 관측되어 별도 checkout으로 복사했다. 작성 주체는 미확인이다. 회수 원문을 버리거나 기존 브랜치를 초기화하지 않았다.

## 현재 판독/집계

- 주 판독: 각 프로젝트 `lineage-final.json`, `returns-final.json`, `FINAL_AUDIT.md`.
- 통합 원장: root `lineage.csv`, `returns.csv`, `sources.jsonl`; 통합 집계 `counts.json`은 묶음④에서 생성한다.
- 고유 자료수의 권위: `crossdomain/source-count-review.json`의 38-ID allowlist와 `source-reconciliation.json`. 기존 프로젝트 `sources.jsonl`, 옛 stage1의 countable 값과 stage3 incremental count를 합산하지 않는다.
- 기존 `STAGE3.md`, `finalize_stage3.py`(MP), 프로젝트 `sources.jsonl`의 중간 설명/자료수는 회수한 작업 흔적이다. 최종 판독 원장과 불일치할 때 최종 원장을 따른다. 원본 파일·실패 응답·누락 이력은 삭제하지 않았다.
- 독립 검토는 동일 모델 계열의 별도 작업자가 맡았다. 사람이 수행한 검토나 블라인드 재채점으로 부르지 않는다.

`resume-contract.json`은 통합판·의존핀·봉인 불변을, `isolation-snapshot.json`은 복사된 파일과 지문을 기록한다. 이후 원격 갱신은 읽은 head를 조건으로 하며 다른 원격 커밋을 덮어쓰지 않는다.
