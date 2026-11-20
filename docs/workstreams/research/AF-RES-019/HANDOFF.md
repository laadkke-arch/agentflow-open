REVIEW_READY_WITH_GAPS

# AF-RES-019 인계

40개 사건, 원문이 확인된 35개 시행일, 40개 비교 행의 연구 묶음을 저장했다. 엄격 대조 7쌍은 작은 표본이다. 대조 요건, 과거 레지스트리 2신호, 비용 성공 80항목, 패키지 폐기 문헌의 사이트 상한 후 두 번째 원문, request 사용량·대체 여부가 남았다. [종료 조건과 재개 입력](evidence/acceptance-evidence.json)

## 고정 입력과 실행 위치

- 시작 커밋은 chore/workspace-foundation의 ded7f3838fe16f1cf401789e99e957b1ebebff1b다. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF 및 dot-control의 AF-RES-019를 GitHub에서 읽었다.
- AF-RES-009 7f627a81199f06da7f7b15f979e7fef25dd17602의 HANDOFF와 FAILURES를 읽었다. AF-RES-015 e39d23c9a7307ba83c974580f60115d90e221084의 HANDOFF, REASONS, SIGNALS, 혼동표·접근·주기 자료, COST, COUNTEREXAMPLES, SCOPE와 sources를 읽었다.
- 작업 위치는 관리형 Codex Cloud Linux의 /workspace/af-res-019이고 모델 표기는 GPT-6 기반 Codex다. 세부 모델 변형과 추론 강도의 별도 표기는 확인되지 않았다. 작업자가 공개 원문을 판정하고 계산을 재현했다.
- 저장소는 laadkke-arch/agentflow-open, 원격 브랜치는 work/research-af-res-019다. 인계 직전 확인 커밋은 aa4b414a80cc83a17781da97a976cb7d14cd1ea5다. 마지막 커밋의 변경 경로는 이 인계 파일 하나다. [고정 계약](manifest.json) · [실행 증거](VERIFICATION.json)

## 결론과 적용 한계

| 세부 질문 | 결론과 범위 |
| --- | --- |
| Q1 사건 | 다섯 유형 각 8건, 서로 다른 일곱 생태계, 정확한 시행일 35건을 기록했다. 공지와 시행일을 모두 얻은 29건에서만 공지 선행 기간을 비교했다. |
| Q2 대조 | 후보 70개를 검토해 엄격 7쌍, 탐색 20행, 서비스 유사 8행, T 미확정 5행을 고정했다. 운영 Git이 없는 서비스의 매치는 판정하기 어렵다. |
| Q3 신호 | 4,160칸에 값 또는 사유가 있다. 네 시점에서 값이 있는 신호 11종이 양쪽에 있다. 과거 deprecated/yanked와 레지스트리 라이선스 변경을 복원할 기록이 부족하다. |
| Q4 선행 | 엄격 A는 사건 3/7, 대조 3/7. 적중 3건 중 2건은 12개월 창 시작부터 경보했다. 전체 태그 확인 후 탐색 A 적중이 18/26에서 13/26으로 바뀌었다. 운영 정밀도는 표본보다 더 낮을 수 있으며 실제 기준율은 미확인이다. |
| Q5 발견 | 35개 시행일의 월 재생에서 원문 직접 35/35, A 후 원문 13/35다. 직접 판단은 공지 이후 중앙 16일이다. 요청 간격과 문서 인지 가정이 있다. |
| Q6 비용 | 80개에 시도해 67개에서 한 경로 이상 성공했다. 직접 HTTP 65쪽, 부분 clone 66개, 레지스트리 36개를 측정했다. 무캐시 외삽은 초기화 상정이며 증분·독립 판독은 남았다. |
| Q7 015 | 기존 이유 500개 중 공개 라이선스 및 관리 상태의 유형 분모 39개, 기능·플랫폼 포함 조건부 상계 361개, 경로 밖 139개다. 초기 오류 4개는 별도다. |
| Q8 비교 | 약물·금융·웹 신선도 세 분야, OSS 실증 다섯 편, 방법·비교 30개를 산입했다. 패키지 폐기 실증 본문 2편 중 1편은 arXiv 상한으로 산입하지 못했다. |

[필수 결과 표](RESULT.md) · [연결](LINK_015.md) · [다른 분야](CROSSFIELD.md)

## 가장 강한 근거 세 건

1. B03 Firefox Send는 공개 Git에서 시행 전 12개월의 관측 10종이 임계값을 넘지 않았고, 영구 폐쇄 사실은 제작자 2020-09-17 공지에서 확인됐다. 여름에는 별도 임시 중단이 있었다. [공식 공지](https://blog.mozilla.org/en/uncategorized/update-on-firefox-send-and-firefox-notes/) · [일별 신호](signals/DETAILS.json)
2. C-A07 Keystone에서 현재 6의 MIT는 1년 뒤에도 있었다. README의 경보 문구가 가리킨 범위는 별개의 Keystone 5였다. C-E02 Less에서 낮은 커밋·태그 신호가 울려도 같은 기능 설명은 1년 뒤 유지됐다. [반례와 고정판](COUNTEREXAMPLES.md)
3. 날짜가 있는 35개를 같은 창으로 재생했을 때 월 원문 확인의 35건과 월 신호 후 확인의 13건 차이가 있었다. Adobe의 지원 중단 공지는 1,255일 먼저 나왔다. [공식 발표](https://blog.adobe.com/en/publish/2017/07/25/adobe-flash-update) · [발견 기록](results/cadence-events.csv)

## RESULT §4의 세 약점

1. 엄격 대조가 7쌍이다. 시기·범주·활동을 동시에 고정한 비교를 확장해야 한다.
2. 표시의 시간 원장이 없고 먼저 울린 경보 중 일부는 창 시작 전에 이미 켜졌다. 원문 공개 이후의 변화와 독립적인 선행 정보를 구별해야 한다.
3. 초기 Git 및 HTTP 도구 비용을 쟀다. 증분 수집과 신규 원문 해석의 작업자 비용을 별도로 확인해야 결정이 달라질 수 있다.

## 검사와 남은 실행

새 Python 3.12.14 가상환경에서 단위 시험 7개가 통과했다. 분석·비용 출력 8개가 바이트 일치했다. 작업 계약을 원격 fetch로 검사했고 공통 cloud_check는 결과 작성 커밋 e7e70b111ece1a1b2fc4d095f4b525cb167fd32b의 깨끗한 worktree에서 통과했다. 공통 배치는 활성 등록 세션을 찾지 못해 작업 manifest는 직접 검사했다. 이 인계의 형식·근거 파일·경로 범위도 커밋 전에 확인했다. [검증 영수증](VERIFICATION.json) · [자체 점검](SELF_CHECK.md)

다섯 반례 경로를 조사했다. request가 널리 쓰인 역사와 현재 deprecated는 확인했다. 오늘 다운로드 수와 모든 제약을 만족하는 대체 여부는 미확인이다. 동일한 npm 공개 통계 GET은 CONNECT 403이었다. Cogo 저자 PDF와 출판 원문에 접근하지 못했고 Wayback·GitHub API·deps.dev·SWH API도 CONNECT 403이었다. 지원되는 Git·패키지 범위로 대체했다. [반례 명령과 입력](COUNTEREXAMPLES.md) · [차단 기록](PROGRESS.md)

분석 재현과 비용 영수증 재생의 명령·입력은 PROGRESS.md §3에 있다. 짝을 다시 모을 때 쓸 명령은 아래와 같다. CANDIDATES.json에 실제 최초 연도 범위, Git 공개본과 유지의 동시대 판 근거가 있는 후보를 먼저 추가한다.

```sh
p=docs/workstreams/research/AF-RES-019
python -B "$p/src/collect.py" --scratch /tmp/af-res-019-next --match --registry
python -B "$p/src/verify.py"
```

## 색인 변경 제안

| 작업 | 상태와 등록 위치 | 다음 연결 |
| --- | --- | --- |
| AF-RES-019 | REVIEW_READY_WITH_GAPS · work/research-af-res-019 · docs/workstreams/research/AF-RES-019/RESULT.md | 유지 경보 7 엄격 짝·35 날짜 재생을 참고하고, 누락 대조와 날짜 있는 표시 이력을 보강한다. |

## 다음 첫 행동

매칭 원장에서 엄격 조건이 깨진 최초 연도·작성자 구간·사건 부재 확인을 먼저 분류한다. 현재 공개판에 남은 날짜 근거로 추가 엄격 짝을 찾고, Git이 없는 서비스의 공개 지원판과 날짜를 별도 입력으로 고정한다. 상태를 갱신하기 전에 마지막 원격 SHA의 이 파일과 수용 근거를 읽는다. [실제 재개 입력](PROGRESS.md)
