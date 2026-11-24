# AF-RES-241 자체 점검

## 분모와 판정

| 항목 | 예정 | 관측 | 결측 또는 범위 |
| --- | ---: | ---: | --- |
| 고정 원 화면과 공존하는 앵커 | 4 화면 / 8 앵커 | 4 / 8 | 0 / 0. AF-RES-223의 Register 결측 4자리는 본 표본에서 제외 |
| Chromium 기본 여정 | 16 | 16 | 0. Apply 12, Register 4. 새 초기 fixture 기준 S/B 요약행 동치 8/8 |
| 정상 진입 DOM/AX와 Tab/Enter·편집 필드·기존값 | 16 | 16 | 0. 관측 이름의 공백은 raw 보존 |
| 지정 값 변경과 전후 모델·복귀 | 저장 8 | 8 | 0. 단일 leaf 변경 3/8. 추가 값이나 FK·초기화는 결과로 남김 |
| 미수정 즉시 복귀 | Back 8 | 8 | 0. 앱 Back 사용 8. 브라우저 Back은 별도 대조 1 |
| 기존 A2 작성 기대 | 2 | 2 | 0. 실제 upstream 독립 RSpec example은 1 |
| 별도 반례 브라우저 예제 | 5 | 5 | 0. A1 동일 이름 한 쌍의 두 활성화, 중간 주소·브라우저 Back·공유 feedback 두 예제 |
| 깨끗한 별도 DB 양성·오류 | 2 | 2 | 0. 독립 초기 상태의 서로 다른 두 번호 입력 |
| 도서관 고정 서지·목록 | 2 | 2 | 0. 같은 연도 다른 판 1건은 별도 대조 |
| 도서관 holding ID·거래 대상·버튼 AX | 고정 두 서지에서 확인 가능한 범위 | 각 확인 0/2 | 미확인 각 2. 실제 거래 0건 |
| 실제 AT 발화·사용자 선택률 | 본 검산 범위에서 수집하지 않음 | 0 | 발화·선택률 미확인 |

기본 실험 16, 별도 브라우저 예제 5, 깨끗한 양성·오류 2, upstream RSpec example 1을 독립 실행 단위로 기록했다. 같은 예제의 분기·두 링크 클릭, 파일 수, 재실행, 원격 공개 서지 확인은 서로 다른 분모다. [journeys.csv](journeys.csv) · [controls.csv](controls.csv)

원장 109행, 고유 source_id 109와 입력 work_id 109. 산입 원저작 78개, 산입 계보 66개다. 원저작 기준 component/view 18, route/controller/form/factory 35, 기존 시험/공식 실행지침 10, 규격/브라우저/GOV 5, 서지/운영 10이다. 실패 경로 기록 6행은 산입에서 제외했다. 미산입에 배정·선행 자료 및 빌드 입구를 포함했다. 원장의 UTC는 처음 연 초까지 알 수 없는 경우 도구 관측 시간창이다. 검색 결과 목록의 스니펫은 성공 저작 수에 포함하지 않았다. [sources.jsonl](sources.jsonl)

## Q별 조합·반증

| 질문 | 확인한 원근거와 수치 | 반증·미확인 |
| --- | --- | --- |
| Q1 | A18·A19·R14·R15, 실제 lock 및 선택 소스 61/61 일치. 두 Rails DB/route와 공개 mock 로그인 성공. [지문](environment.json) | 초기 APK HTTP 403 및 Selenium 저장 공간 부족. 호스트 엔진으로 복구. Node 선언과 이미지 버전 다름. 두 실제 운영판·다른 역할은 미확인 |
| Q2 | A01·A03·A04·R03, W01–W03. 공존 4/4, 대상 DOM/AX 16/16. raw AX U+00A0, description 없음 16/16. [원행](journeys.csv) | A1 동일 이름 ID 11/12에 AX 원문 동일. 키보드 탐색과 브라우저 이름을 발화로 일반화하지 않음 |
| Q3 | A24·A07·R18, 실제 href→첫 편집 16/16, 필드 16/16. [A3-2](receipts/journeys/A3-2-S.json) · [R1-1](receipts/journeys/R1-1-S.json) | A3 주소의 첫 입력은 address_type이고 Register Course의 첫 입력은 training_route. BODY는 필드 초점이 아니며 다른 화면·엔진의 자동 초점은 미확인 |
| Q4 | A08–A11·A25–A27·R08–R10·R19·R22. S 8개 intent 모두 반영, 전후와 중간 관측. [모델 차이](journeys.csv) | option FK, 보이지 않은 빈 line4, 지원금 초기화와 과목/연령을 포함. R1-1의 재입력 뒤에도 섹션 접힘. A2 cache 인스턴스 직접 조회 미확인 |
| Q5 | A12·A26·R21. B 8/8의 정상 앱 Back에서 모델·요약값 보존, 브라우저 Back 대조 1/1. [중간 대조](receipts/controls/C-A3-MID.json) | UK를 그대로 계속한 뒤 Back에서 GB 보존에 실패. 이후 페이지 및 비UK 분기까지 일반화 미실시 |
| Q6 | A16·A29 기존 2가지 기대/1 example, R23–R28 양식 대조 2/2, 양성·오류 재생 2/2. [기존 stdout](receipts/controls/apply-a2-spec.stdout) · [공유 폼](receipts/controls/C-R-F1.json) · [깨끗한 재생](receipts/controls/apply-clean-final.stdout) | 동일 목적지에서 form name 일부는 렌더마다 바뀌고 스타일 때문에 radio 자동 선택·날짜 입력의 초기 시험 위치가 틀렸다. 실제 앱 답과 하네스 실패를 분리 |
| Q7 | L01–L10. 고정 공개 서지 2/2, 같은 연도 추가 한 건. [읽기 전용 기록](receipts/controls/library.json) | 재고와 action은 스냅샷. 실제 holding, 전자 제공자 pool, 예약 요청 및 발화 미확인. 직접 경로 에러의 회복 및 미회복은 F04–F06 |

## 재실행과 검토 범위

- Apply의 초기 12예제에는 좁은 radio CSS 선택을 잘못 적용한 하네스 실패 3개가 있었다. 실제 필드가 있는 원출력에서 관찰된 실패와 라벨 클릭 수정 뒤 성공 로그를 유지했다. 주소는 첫 저장에서 돌아온 화면과 뒤이어 실제 원 화면에 도착한 단계를 분리했다. [초기 및 수정 영수증](receipts/attempts/)
- Register에서는 처음에 안정적인 input ID 대신 보호된 임시 DOM name을 예상해 날짜 입력이 빠졌다. 첫 실패 경로에는 실제 form validation과 error summary를 남겼고, 후속 재입력은 정상 날짜 필드에 입력했다. 최종 확인은 오류 없는 원 URL 도착까지 확인했다. [초기 여정](receipts/attempts/R1-1-S.json) · [최종 여정](receipts/journeys/R1-1-S.json)
- 앞선 실행에서는 A2 funding 기본값 및 Register의 합성 요약행 일부가 달랐다. 최종 실험의 seed와 화면 조건을 고정한 뒤 S/B 요약행 전체를 비교했다. 모델의 생성 ID와 시각을 독립 초기 상태의 동치 값으로 요구하지 않았다. [fixture](fixtures.md) · [최종 Apply](receipts/attempts/apply-fixed.stdout) · [최종 Register](receipts/attempts/register-fixed.stdout)
- 새 Apply 컨테이너 및 분리 DB에서 양성과 오류를 실행했고, 최종 replay script로 다시 만든 별도 DB에서 두 입력을 재생했다. 성공은 새 값과 실제 review, 오류는 예전 값·편집 URL·error summary DIV focus로 판정했다. [재생 명령](replay/README.md) · [최종 DB 준비](receipts/controls/apply-clean-final-db.stdout)
- `replay/validate.py`로 16 raw/CSV 및 공존·모델·복귀·반례·근거 ID, 고유 수와 링크, RESULT의 필수 두 표와 마지막 약점 3건을 대조했다. 기계 점검은 제품 기능 시험과 별도다. 독립 작성자 검토는 미실시이며 이 기록은 자체 점검이다.
