# AF-RES-216 자체 점검

검토자는 이 작업을 실행한 Codex다. 저장 원응답을 새 프로세스에서 재집계하고 별도 짧은 검사로 원바이트 지문, 정확 키, 세 표면의 SHA-256을 검산했다. 독립 검토자 검토는 미실시다.

| 질문 | 근거와 자체 판정 | 실제 반례·통제 | 남은 확인·다음 원자료 |
| --- | --- | --- | --- |
| Q1 수신 | V01–V06, I01–I02 8/8 HTTP 200. H01–H06 6/6. MIME·UTC·최종 URL과 원바이트 지문 확인. [API](receipts/api/http.json) · [HTML](receipts/html/http.json) | C18에서 읽지 못한 endpoint를 둘 다 없어진 파일로 처리하지 않음 | 서로 다른 조회의 원자성 미확인. 변경 조사라면 R05의 serial과 당시 저장 응답 확인. [R05 L194–205](https://docs.pypi.org/api/index-api/#get-distributions-for-project) |
| Q2 단위·형 | V02/V05 `info` vs `urls`, I01/I02 `files`. 대상 true/사유 문자열 26, 인접 explicit false 62. [파일 원값](files.csv) | C01, C04–C09에서 결측, 빈 이유, null 및 사유/상태 차이를 구분 | 실제 응답은 네 가지 혼합형이 없는 표본. 혼합 플래그가 보이는 인덱스의 정확 파일을 R02 형과 대조. [R02 L388–423](https://packaging.python.org/en/latest/specifications/simple-repository-api/#project-detail) |
| Q3 정확 조인 | B01 88키, 양쪽 현재 88키, 한쪽만·누락·신규·중복·digest·태그 차이 0. 88개 HTML 해시도 같다. [파일표](files.csv) · [직접 교차 검사](receipts/crosscheck.json) | C10–C17에서 태그·digest, 신규/부재·중복, 같은 이름의 다른 버전, post1 접두사를 대조 | 현행 바이너리 해시 자체는 미확인. 실제 배포물 점검 시 기록된 파일 URL과 해시 사용. |
| Q4 대상/인접과 삭제 | H02/H05 플래그 26/26, 인접 62/62. M01은 삭제 5개 이름·해시를 보고했고 C03은 1개 역사 이용 로그다. [삭제 상세](history-deleted.csv) | 네 인접판에 과거 Yanked 이력 카드가 있어 h1+현재 배너+현재 카드로 축소. sdist와 비Windows도 3.9.1에서 같은 철회 표시 | 삭제 개별 시각과 과거 flag는 미확인. [M01 열거 L461–468](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267225291)의 당시 build/index 기록 필요. |
| Q5 시간과 고장 | B02 날짜와 H02/H05 UTC 필드, M01/M02 발언·로그 UTC 비교. M03/M05/M06의 후판 의도·변경과 당시 결과 구분. 역산 0. [정정](COUNTEREXAMPLES.md) | post1+nightly wheel 성공, post1+자체 빌드와 별도 프로그램 실패. 8.1.0 설치 성공과 ixmp 실패, 8.1.1에도 남은 내부 API 의존 | 첫 파일별 이벤트와 post1 전체 수정 미확인. [F02 원 Windows CI](https://github.com/matplotlib/matplotlib/actions/runs/9789558015), [F03 비교 CI](https://github.com/ianthomas23/mpl-test/actions/runs/10282014029), F04는 현재 404. 보존 로그·당시 serial이 있으면 재대조. |
| Q6 출판 정정 | X01 PLOS 원문 e0291840 04-03와 X02 공고 e0313792 11-08의 링크 및 정정 지목을 확인 | 원문 URL이 열리고 Fig 8·S1 File·문장은 뒤의 정정 대상이다. 주소 생존으로 최신 편집 상태를 판단하면 누락 | 출판사 정책의 예외 일반화는 미실시. [X02 Reference 1, L157–165](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313792)의 실제 대상 범위를 지킨다. |
| Q7 재현·권고 | 합성 18개 개별 행·2개 키 집합 20/20. 두 사건의 각 3개 목적 문구 갱신. [통제 결과](receipts/controls-result.json) · [advice](advice.csv) | exact/wildcard 차이, 배너 기본 제안이 범위 밖인 사례, 미러 누락과 캐시 환경 | 현재 pip·잠금 도구·파일 다운로드는 미확인. [R06 pip 24.0 L299–339](https://github.com/pypa/pip/blob/24.0/src/pip/_internal/resolution/resolvelib/factory.py#L299-L339) 및 해당 사용자의 기록에 범위를 한정. |

## 하한과 분모

| 자료 유형 | 최소 목표 | 직접 연 고유 work | 표집 비고 |
| --- | --- | --- | --- |
| version JSON | 6 | 6 | V01–V06 |
| project Simple JSON | 2 | 2 | I01–I02 |
| release HTML | 6 | 6 | H01–H06 |
| 공식 규칙·구현 | 3 | 7 | R01–R03가 하한 충족, R04–R07 보강 |
| 유지자·당시 소비자 원기록 | 3 | 10 | M01/M02/C01가 하한 충족, 유지자 tag·diff·changelog·도구 답변과 소비자 로그 보강 |
| 출판 원문·공고 | 2 | 2 | X01/X02 한 쌍 |
| 합계 | 22 | 33 | 계획 22/22, 추가 직접 본문 11 |

원장 42행 중 직접 산입 33, 도구에서 본문을 확보하지 못한 자리 5와 선행의 입력 문서 4는 하한에서 뺐다. 산입 work_id 중복 0, lineage_id 8개다. 사건은 소프트웨어 2건과 출판 정정 1건이다. M01 본문·timeline·댓글은 하나의 work이며 GitHub와 PyPI에 있는 파일 링크를 독립 사건으로 더하지 않았다. 시험 fixture는 원장 하한에 산입하지 않았다. [출처 원장](sources.jsonl)

모집표의 계획 파일 키는 88/88 확인, 삭제 집단 1/1은 옛 파일 상세 5개로 보강했다. 현재 합집합은 88이며 대상 26, 인접 62다. 모집표 136자리는 계획 자료 22, 보강 자료 11, 선행 문서 4, 열람 실패 5, 기준 파일 88, 기준 삭제 집단 1, 역사 상세 파일 5다. [모집표](frame.csv) · [기준·판정 규칙](SCOPE.md)

## 실행 증거

- Python 3.12.14와 Git 2.52.0의 Cloud Linux 실행. 실제 명령·UTC·지문·종료코드·stdout/stderr는 영수증의 JSON에 보존했다. 최초 두 수집의 종료코드는 0이었다. [API 실행](receipts/fetch-api.json) · [HTML 실행](receipts/fetch-html.json)
- 커밋 `7ebba73951a10abed1f8c4f600fbaf2711de2104`의 파일을 `git archive`로 새 임시 위치에 풀었다. B01은 고정 SHA의 CSV를 다시 꺼내 읽었다. 새 프로세스의 `files.csv`, 요약, 합성 결과가 기존 파일과 `cmp`에서 같고 출구 0이었다. SHA-256은 각각 `94d9bcd3614e20182a47de7cae7d4abed3e13c6f27923b7cf91adb49f1304ced`, `445172857b25c10cddcbac14a380d675a81022d43ceabf9a93f94ddf71dbd802`, `4560d404201ae45c518292aa50a123fe58b5bc456f244b6a3e01dba901715e35`다. [API·HTML 재생](receipts/reconcile-replay.json) · [합성 재생](receipts/controls-replay.json) · [교차 검사](receipts/crosscheck.json)
- 이 자체 점검은 현재 자료·원자료·코드 출력에 해당한다. 해당 패키지 설치와 결함 재현, 현행 파일 본문 다운로드, 별도 검토자 검토는 미실시다. [재현 범위](SCOPE.md)
