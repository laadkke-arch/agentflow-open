# Q8 · 다른 분야의 경보와 재확인

## 약물 감시

FDA 공개 보고는 의심 사례에 접근하게 해 주고, EMA 절차는 탐지·검증·확인·우선순위·평가를 차례로 구분한다. PRR은 관심 약물의 보고 중 관심 사건이 차지한 비율을 다른 약물 보고의 같은 비율과 비교한다. ROR은 같은 2×2 표의 오즈비다. 작은 셀, 과소보고와 중복·선택적 증가가 빈도와 정밀도에 영향을 준다. 권고 행동에는 사례 내용과 다른 출처를 대조한다. 저장소 신호가 보이면 원문·영향 범위를 다시 읽는 2단계 절차와 닮았다. 자체 시뮬레이션에서는 신호가 없는 서비스와 조용한 변경을 선별 단계에서 잃는다. [EMA 절차](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf) · [ENCePP 통계 탐지](https://encepp.europa.eu/encepp-toolkit/methodological-guide/chapter-11-signal-detection-methodology-and-application_en) · [FDA 공개 보고 한계](https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-public-dashboard)

## 금융 조기 경보

Sarlin은 희귀 사건의 위기 이전 구간에서 오경보와 놓침의 비용에 각각 가중치를 부여한다. 비위기가 많으면 놓침과 오경보의 조건부 비율만으로 실제 작업량을 설명하기 어렵다. 실험 표본에 비슷한 개수로 넣은 019의 사건과 대조도 자연 기준율이 아니다. 예를 들어 표본에서 재현율 3/7, 거짓양성률 3/7이라면 관측 창의 실제 기준율 1/100에서 기대 정밀도는 1/100이다. 이는 분류 집단이 같다고 가정한 대입이며 실제 발생률을 추정하지 않았다. 운영자는 불필요 원문 검토 비용, 개발자는 EOL 뒤 긴 전환이나 지원 불가를 뒤늦게 발견하는 비용을 따로 봐야 한다. [ECB 작업 논문](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1509.pdf) · [불균형 분류 비교](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0118432)

## 웹 변화와 신선도

Cho와 Garcia-Molina는 바뀌지 않은 사본과 얼마나 오래 낡았는지를 서로 다른 목적함수로 세워 재방문 예산을 비교했다. Fetterly 등의 1.51억 URL 초기 크롤 및 후속 반복은 관측 가능한 본문 변화와 가져오기 실패의 분모가 달라짐을 보여준다. 공개 웹의 페이지 변화는 특정 이유의 상실과 다르다. 제품 설명에 공지가 있거나 LICENSE의 대상 권리가 바뀌면 의미를 분리해서 판정해야 한다. ETag와 조건부 HTTP는 자료를 반복 내려받는 비용을 줄이는 후보로 남는다. 이를 통한 추천 판정의 개선은 측정하지 않았다. [갱신 정책 원문](https://www.researchgate.net/publication/200111226_Effective_page_refresh_policies_for_Web_crawlers) · [반복 크롤 원문](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/02/p97-fetterly.pdf) · [HTTP 의미론](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8.3)

## OSS 중단, 라이선스 및 표시

- Avelino 등의 핵심 작성자 이탈 중 128/315 프로젝트는 연구 창에서 생존했다. 이번 최다 작성자 비율은 코드 파일의 지식 집중이나 후임 교체를 재지 않는다. Coelho·Valente의 104개 실패 표본에서는 더 나은 대안, 노후화, 팀 시간·동기가 서로 다른 경로였다. Khondhu 등은 비활성 프로젝트 이력을 따로 다뤘다. [M01–M05의 원문·한계](sources.json)
- Coelho 등의 2년 특성 분류는 내부 AUC 0.88과 README 명시 부분집합의 recall 108/112를 따로 보였다. Valiev 등의 Cox 모델은 우측 검열과 PyPI 생태계 관계를 고려했다. Xu 등의 AFT preprint는 유지 중단에서 표면 지표보다 여러 조직·기여 정보를 넣어 C-index를 개선했다. 모두 유지 중단 또는 활동을 대상으로 한다. 019는 도구가 활발한 Directus의 같은 날 조건 변경과 장기 공지가 있는 Adobe도 포함한다. [M03·M04·M06](sources.json)
- 파일별 선언을 연구한 Di Penta 등은 루트 파일명 이상의 범위를 본다. JS의 다중 라이선스 연구도 소프트웨어와 비소프트웨어 파일의 혼합을 확인했다. 운영자가 먼저 알 수 있는 값은 변경 관측이다. 전환 방향과 추천에 영향받는 판은 LICENSE 본문·릴리스·상용 허가를 함께 읽어야 한다. [M07·M08·M35](sources.json)
- Python의 명시 폐기 연구는 업데이트가 뜸한 완성 패키지와 공지 부족을 나눈다. Rust yanking 연구는 새 해석에서 문제가 되는 판과 기존 잠금을 구분한다. npm 관리자는 당일 표시를 할 수 있지만 공개 packument는 표시 날짜 이력을 제공하지 않았다. 과거 날짜를 담은 레지스트리 변경 원장이 있으면 좋은 후속 검정 입력이다. [M09·M10·M18·M26·M27](sources.json)
- Cogo 등의 npm 논문은 저자 목록과 IEEE 항목을 찾았다. 읽을 수 있는 본문은 확보하지 못해 산입하지 않았다. 다른 Rust·Python 실증 원문 두 편과 npm 공식 API를 읽었다. 다른 사이트의 동일 논문은 한 건으로 셌다. [실패 기록](sources.json)

## 관점별 비교

| 관점 | 실제 사례와 확인 단위 | 표본이 허용하는 판단 |
| --- | --- | --- |
| 추천 목록 운영자 | C-A07의 Keystone 5 문구가 Keystone 6 검토로 넘어온다. | 낮은 기준율에서는 확인할 건수가 비용을 지배한다. 원문 확인보다 경보가 비싸거나 늦을 수 있다. |
| 추천을 받은 개발자 | Dcoder 운영 종료 때는 이전 앱 링크나 삭제되지 않은 소개로 목적을 채울 수 없다. | 적용 시점에 즉시 확인할 이유와 변경 전에 시간을 주는 공지를 구별한다. |
| 프로젝트 관리자 | Node Sass 표시는 신규 사용자에게 안내하고 기존 사용자는 옛 판을 설치할 수 있다. | 원문이 선언한 패키지·판·시행일을 보존하면 이전 대화의 이유를 검토할 수 있다. |
| 레지스트리 운영자 | npm 판 표기·PyPI 파일 yank·Cargo 잠금 예외가 다르다. CRAN은 검사 실패로도 보관한다. | 상태 현재값, 표시 생성 시간, 배포 상태를 나눠야 서로 비교할 수 있다. |
| 조기 경보 연구자 | 7쌍의 짝 부트스트랩과 점검 시점의 AUC가 있다. | 운영 발생률을 알 수 없고, 확인 가능한 과거만 남는 선택 효과도 있다. |

## 한계

방법·비교 원장에는 실제 본문을 읽은 자료, 접근 실패와 제외 이유, 사이트 상한 및 015 중복을 기록했다. Q8의 다른 분야는 약물 감시, 금융, 웹 갱신 세 분야다. 프로젝트 관리·레지스트리 운영을 그 수에 추가하지 않았다. [자료 원장](sources.json)
