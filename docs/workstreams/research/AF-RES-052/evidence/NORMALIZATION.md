# 관측 원장 통합 규칙

봉인된 입력은 `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e`에 있다. `assemble_results.py`는 그 입력을 수정하지 않고 두 분야의 관측 파일을 통합한다. Python의 P-S1-Un과 root P-S1-Rn은 같은 원순번이며, diagnostic D-P1도 같은 별칭 규칙을 따른다.

`evidence.csv`는37행이다. 자연 요구8개 조건과 미충원3자리의 상태11행, Python 관측11행, Markdown 진단15행을 포함한다. `paths.csv`는177행이나177회 실험이라는 뜻이 아니다. 빈 자리의 상태21행과 경로156행(P-S1 49, D-P1 57, D-M1 50)이다. D-P1 중8행은 미해결 시작 URL 또는 hop 자리이며, 구체화된49행에도 접근 실패·부분 창은 남아 있다. 같은 도착 창을 A/B/C에 재사용한 분석으로 사람의 클릭 시행은 없다.

CSV의 빈 scalar는 미확인/null이다. 관측한 빈 ID 집합은 JSON `[]`다. 숫자0과 null은 서로 대체하지 않는다. 빈 자연 반환의 ID 수0은 후보 생태계에 구현이 없다는 뜻이 아니다. 시행이 없을 때의 최대와 조건부 비율은 해당 없음이다. 사전 목적 미연결 P-S1의 완결·증감은 null이다. D-M1 현재 문서 창의 완결 관측0과 역사판 미확인은 별개다.

`assemble_sources.py`는 원문 원장의 필드명 차이만 정규화하고 origin_file/origin_line을 유지한다. 최소 배당은 보수적인24개 source ID로 명시한다. 요구4, 목록/작성규칙4, 공급자8, 릴리스/시험4, 타분야4다. 추가 AWS 기능 페이지2개, remark 홈페이지, Compose 예제, remark 통합시험 등은 직접 읽은 배경으로 남긴다. 같은 매뉴얼의 저장 장, README 재게시, 같은 녹음의 HTML/XML, 라우팅/도착에 재사용한 README는 중복 산입하지 않는다.

실패 행은 URL·시도·오류·결론을 바꿀 최소 자료를 유지한다. PY-FRAG-07은 새 저작이 아니라 매뉴얼의-h 링크 정확 도착 미확인 기록으로 PY-O01에 중복 연결한다. Markdown의 도구별 첫 실패3건은 `evidence/markdown/observation-failures.jsonl`에서 같은 정확 HTTP URL의 후속 성공과 연결된다. 원문 자체를 못 읽은13개 실패/정확도착 미확인 행과 혼동하지 않는다.

M-FAIL-955의 원래 한계 문장에 들어간 `NM1`은941 실패 기록의 템플릿 표기였다. 원파일을 덮어쓰지 않고 root 정규화에서 M-N2의 raw HTML 첨부 결손이라고 바로잡았다. 요구선정·키·대표·조건·결론은 바뀌지 않는다. Python D-P1 초기 작업 메시지의55구체화 표현은 최종 원장에서49구체화+8미구체화로 정정됐으며 실제 원장 수를 따른다.

`evidence/ledger-index.json`의 line은 CSV header를 포함하는1-based 레코드 행 번호다. CSV 셀의 JSON은 한 물리행으로 직렬화했으며 sources.jsonl은 행마다 한 JSON이다. 모든 ID가 재구성의 기준이며 자연/보강/진단/맥락은 layer 열로 구별한다. 원문 열람 창의 위치와 SHA는 각 domain arrivals에 보존한다.
