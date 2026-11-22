# AF-RES-023 고정 입력을 읽은 범위

고정 SHA: `a9178ca95979564fd8801559d90d15db4ddac91b`. 내부 선행 결과이므로 외부 원문 최소수에 산입하지 않는다.

| 입력 | 읽은 위치 | 이번 작업에 적용하는 교정 |
| --- | --- | --- |
| [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md) | 상태·분모·C06/C13/C15/C23/C30·다음 조사 | 18사건/135자료ID를 완전 날짜 사슬 또는 독립 원문135개로 읽지 않음. 외부 날짜 있는 사슬은3개. |
| [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/RESULT.md) | Q3–Q6 | HTTP200, 기능, 과거판, 현재 후계, 소비자 인용 목적은 독립 값. DOI/ID 도착점과 목적 충족을 구별. |
| [citations.csv](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/citations.csv) | 전체13행; SW-D01/D02, MB-C01, WD-C01와 ROR-C01–04 | Rails 소스 수정2024-05-23은 소비자 배포 날짜가 아님. workbench 수정2026-11-04도 설치 실패 재현이 아님. AcoustID의 재가동·닫힘은 replica 전파 완료가 아님. Wikidata 두 undo의1분 차이는 사람의 작업시간이 아님. 현재 ROR 페이지는 최초 인용/정정 날짜를 주지 않음. |
| [reconstruction.csv](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/reconstruction.csv) | 54행의 대상·기능·목적지 판정과 SW 5사건의 visible_information, 부족근거 | SELECT 수를 정확도·운영효과로 재사용하지 않음. 과거 오기록 복원은 그 오기록 승인과 다름. source에 노출된 자기점검은 독립 맹검이 아님. |
| [counts.json](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/evidence/counts.json) | 전체 | primary18, conservative originals38, external consumer7, dated chain4(외부3). '현재 페이지'와 날짜 있는 사슬을 다른 분모로 둠. |

`excluded-prior-events.json`에는 선행 원장의 보조 행까지21개를 보수적으로 제외 목록으로 복사했다. 이 숫자는 선행 주 사건18개를21개로 다시 센 것이 아니다. 신규 A/B의 최소수에서 선행의 주 사건과 명시된 소비자 교정예를 제외한다.
