# AF-RES-032 RESULT·행별 근거 감사

**본문·원장·영수증 대조 16/16 조건 통과. 발견 7건 모두 수정 후 재독했다. 후기 결과 검산 38/38 exit0의 실제 영수증과 45개 입력 hash도 확인했다.** 연구 분모나 유지/교체/보류 판정을 바꿀 잔여 오류는 이 범위에서 찾지 못했다.

검토 시각: 2026-11-22T08:27:53.180641+00:00. RESULT SHA256: `c2c32c79d95cddc6efa1c81f3d7bf25b13e655975e027822d2d8ab0e0eb3e59b`. 18개 행별 문서와 원장·판독·검사 영수증의 입력 hash는 [result-review.json](result-review.json)에 있다. 이번 검토의 Git 명령과 외부 조회는 각각 0회다. 변경한 파일은 이 문서와 JSON뿐이다.

## 필수 표와 실측 분모

| 검토 항목 | 재계산 | 해석·제한 |
| --- | --- | --- |
| 첫 3개 필수 표 | 각각18행; A-D01–06, A-R01–06, B01–06 각각1회 | 헤더 순서·Markdown 열 수 일치 |
| 마지막 약점 표 | 정확히3행; 뒤에 본문 없음 | 필수 형식 충족 |
| 직접 원문 원장 | 395행/고유ID395/최소75 | 범주12+34+1+8+8+5+7. 새 외부 원문 열람 없음 |
| A 배포 관측 | archive123/상태246=HTML211+부재35 | source 종류와 archive URI로 재구성. 부재를 읽은 HTML로 세지 않음 |
| 같은 목적 소스→출판 | A3참조쌍·독립2사건/B1쌍 | knitr 두 행은 같은 commit. 보조7행 산술 모두 일치 |
| 엄격 시행→동일 목적 HTML 출판 | A0/12,B0/6; 조건부 분모0은 해당 없음 | 평균0일·전파율0%·우측 검열로 바꾸지 않음 |
| Q8 L3 A | 유지9·교체2·보류1; 행동 일치11/12 | A-D04 노출 제외10/11. 기준도 보류인 행은 정답 분자 제외 |
| Q8 L3 B | 유지4·교체1·보류1; 행동 일치5/6 | B03 배경 노출 제외4/5. B05 중복/B04 역사 HTML 미확인 유지 |
| 판독 비용 | A source card50,B23; 각 보기 추가 외부 열람0 | A 입력97,612바이트·고유ID46은 본인 L3 영수증과 일치 |
| 링크·행 값 | source ID 링크197개 URL 일치; artifact/member/hash/href 불일치0; 로컬 링크 부재0 | 외부 URL 생존 검사는 하지 않음 |

## 발견과 수정 후 결과

| ID·중요도 | 문제와 원근거 | 수정·재독 결과 |
| --- | --- | --- |
| RR-F01·중간 | A-R03의2025-10-30 MDN 소스 경로 수정이 R-U13(2020 고정 본문)을 인용했다. 정확 근거는 [R-U17](https://github.com/mdn/content/commit/2d78abb3e793352e24e976ce0e68c08d817bd7f3)이다. | R-U17로 수정 확인. R-U13은 구 속성/alias 의미 근거 역할만 가짐. |
| RR-F02·중간 | A-R04 원 href에는 fragment가 없는데 ‘옛 anchor’로 서술했다. references A-R04/R-U04가 원문과 redirect를 구별한다. | ‘redirect가 추가한 도착 anchor’, ‘원 raw href에는 fragment가 없었다’로 수정 확인. |
| RR-F03·중간 | 초기 RESULT는 없는 acceptance-evidence.json과 경로 없는 ‘최종 검산 영수증’을 완료처럼 소개했다. | acceptance30조건·24true/6false와 실제 deliverable-check38/38 exit0이 존재하고 RESULT가 구체 경로를 연결. 입력45개 hash 일치. 첫37/38 실패도 보존. |
| RR-F04·중간 | 전 작업 패키지를 재추적하지 않았다는 포괄 문장이 B01 JupyterLab3회 실패 접근 편차와 충돌했다. | A 출발표본 미재사용으로 한정하고 B01 편차를 명시. 실패/후보 비용과 false 조건을 지우지 않음. |
| RR-F05·중간 | B04 old GET429와 독립 canonical GET200을 본문은 구분했지만 row/chain final_url은 canonical이었다. 영수증은 downloads7/8.json, 본문은 CB-S20이다. | 원 final_url=null/status429, separately_opened_canonical_url/status200로 분리 확인. PyPI 업로드를 HTML 출판으로 쓰지 않음. |
| RR-F06·낮음 | A URL 보기의 ‘판독자 전원’은1명 작업자의12행을 다수 판독자로 오해하게 한다. | ‘12행 모두 보류’로 수정 확인. |
| RR-F07·낮음 | 현재 작품명 Airplane Flying이1936년 원 표제처럼 읽힐 수 있었다. X-S06의 당시 표제는 Suprematist composition(after a drawing of1913)이다. | ‘현재 Airplane Flying으로 식별되는 작품’으로 수정 확인. 작품 동일성 판단 방법/한계는 cross 원장에 유지. |

## Q7·Q8·최초 경계 해석

ONS의2021년 수치7.5/7.6/8.7은 서로 다른 통계 판의 값이다. 2023-09-01 공표의1.1%p는 직전7.6 기준이며 2022 연차판7.5를 대입한1.2%p와 다르다. RESULT는 이를 구분한다. 현재 보존된 ONS 웹 원고를2022년 최초 바이트로 단정할 수는 없다. BoE Box C는 당시 개정 전후 논증의 실제 인용이며 같은 소비자 href 수정 전후나2026 최신 GDP를 입증하지 않는다. 근거: X-S01–05 및 collectors/cross/cases.json.

Lowry2012의 실제 역사 인용은1936년 표지 도식이며 작품152의 연대 정정을 인용한 글이 아니다. RESULT는 이를 분리하고1914/1915를 작품연대로만 다루며1937 corrected dummy를 실제 공개 교정판으로 만들지 않는다. 현재 개체 기록과 역사 카탈로그의 역할 비교는 성립하지만 같은 작품 정정 전파 사슬은 미확인이다. 근거: X-S06–08, X-S11. 두 분야는 소프트웨어 분모에서 제외된다.

Q8는 본인이 수행한 A L1→L2→L3 판독 영수증과 일치한다. L3에 현재 사실과 이력이 함께 추가되고 카드에는 수집자의 요약·해석도 있다. 11/12와5/6은 수집자 기준과 내부 판독의 행동 일치이며 이력만의 효과·실사용자 정확도·완전한 무정보 맹검이 아니다. A-D04의 L1/L2 이후 B05 요약 노출과 B03의 이전 curl 배경도 명시됐다. 단순한 보기로도 충분했을 것이라는 설명은 사후 추론으로만 표시된다.

‘최초’는 Python3.8.2–3.8.20, PostgreSQL12.2–12.22, CRAN의 열거·열람한 같은 계열 안으로 제한된다. SQLite5/51, B03 성긴3판, B01/B06 versioned web, B04 역사 HTML 부재는 완전 관측으로 승격되지 않았다. source 수정과 실제 새 HTML, 공식 판 공표와 특정 archive의 최초 HTTP 공개시각을 분리한다.

## 검사 완료 표현의 실제 범위

통합 감사27/27, root fresh GET4/4, 별도 Python/httr archive27·HTML46·DESCRIPTION8 재독은 실제 영수증이 존재한다. 각자 명시한 입력 hash에 대한 검사이므로 이후 B04 정규화 등 바뀐 원장을 과거 검사에 소급하지 않는다.

공통 회귀의 성공 영수증은 [common-retry-execution.json](../../evidence/checks/common-retry-execution.json)과 [common-retry-receipt.json](../../evidence/checks/common-retry-receipt.json)이다. 대상 `6ac3d4d9c11f5a750401535a05caed29ed5daf01`, 5/5 exit0의 clean remote checkout workbench 회귀다. 그 영수증도 이후 RESULT·제품·browser 검증이 아니라고 명시했다. 최초 로컬 object 누락 실패도 보존되어 있다. session-pre-result는 결과 커밋 전 check --fetch이며 마지막 인계 검사를 대신하지 않는다.

후기 문서 검산의 실제 영수증 [deliverable-check.json](../../evidence/deliverable-check.json)은 2026-11-22T08:26:50.280213+00:00에 38/38 exit0을 기록한다. 대상 HEAD는6ac3d4d이며 작업트리의 45개 입력 hash가 현재 파일과 일치했다. 첫 실행은 아직 없는 자기 영수증 링크1건 때문에37/38 exit1이었고 [첫 영수증](../../evidence/deliverable-check-first-run.json)도 남아 있다. 이는 외부 원문의 의미를 새로 검증한 검사가 아니다. RESULT와 SELF_CHECK는 이 후기 검사, 공통 회귀, 아직 남은 원격 고정 결과 재독/HANDOFF 단계를 구분한다.

남은 첫 행동은 **결과를 커밋한 뒤 고정 원격 SHA에서 재독하고 최종 session check를 기록하는 것**이다. 그 뒤 별도 마지막 HANDOFF 커밋은 root가 진행한다. 이는 정상적인 후속 인계 절차이며 미해결 RESULT 감사 결함은 아니다. 이 감사는 아직 실행하지 않은 단계를 통과라고 쓰지 않는다.

## 독립성과 한계

root가 만든 결과·통합 원장에 대한 별도 내부 검토다. 검토자는 Q7, B01/B04/B06 수집과 A 판독을 이미 수행했으므로 자기 자료를 포함한 완전 독립 검토나 외부 사람 검토가 아니다. 모든 행 파일의 구조화 근거·핵심 서술·반대 설명을 읽고 원장과 대조했지만 외부 원문을 새로 열지는 않았다. source ID/URL 일치는 원문 내용의 새 검증과 구분한다. 이후 수정은 JSON의 입력 hash 범위 밖이다.
