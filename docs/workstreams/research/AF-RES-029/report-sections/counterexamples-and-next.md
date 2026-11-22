## 서로 다른 관점과 사후 반례

설계자에게 중요한 것은 이번에 호출할 동작과 남는 접합이다. Q02의 의미 정규화, Q08의 잘못된 그래프 거절처럼 핵심 기능을 어댑터가 전부 만들어야 하면 유용한 단서여도 부분 완결로 올리지 않았다. 공급자 관점에서는 지원판·장치·변경 가능한 버퍼·명시 configuration이 계약의 일부다. 검색자 관점에서는 요청 수와 실질 본문이 다르며, 판독자 관점에서는 이미 열었던 같은 문서에서도 반환 절 선택이 성공을 바꾼다.

[반증 원장](supplementary/CHALLENGES.md)은 분야명을 지운 입력→출력→상태 관계로 추출/패딩, 감지/회복, 정수/공유 버퍼, 경로 그래프/거절, dtype/값 독립, CPU 배열/공유 저장소, 문자열/엄격 검증을 다시 맞췄다. 같은 list, recover, resolve, result_type, array, NPY_TARGET_VERSION이라는 이름만으로 다른 주체·다른 출력·다른 판을 받아들이지 않았다. 사후 반례는 경로 반환 수나 성공 분자에 추가하지 않았다.

박물관 사례에서는 [Met의 API 운영 문서](https://metmuseum.github.io/)가 유효 objectID 목록과 total을 제공한다. 식별자 열거가 목적이면 목록에서 끝나며, 모든 개별 작품을 여는 비용은 목적을 더 충족하지 않는다. 반대로 [Quail and Millet 객체 기록](https://www.metmuseum.org/art/collection/search/45734)은 Kiyohara Yukinobu, 17세기 후반, 비단 두루마리의 재료·118.4×47.6cm 치수를 제공한다. 제목이나 accessionNumber만으로 그 실물 정보를 대신하지 못한다. 운영 문서는 accessionNumber가 항상 고유하지 않다고 경고하지만, 이 작업은 같은 번호를 공유하는 다른 실물 두 개를 실제 비교한 것으로 쓰지 않는다.

제조사 사례의 [1591XX 카탈로그](https://www.hammfg.com/electronics/small-case/plastic/1591xx)는 표준 brass-insert/M3와 economy self-tapping, flange 변형을 구별한다. 검은 economy 부품 번호 목록만 필요하면 표로 충분하다. 조립에서는 같은 크기 계열이라는 이름이 결합면·나사를 보장하지 않는다. [1591XXASBK 개별 항목](https://www.hammfg.com/part/1591XXASBK)은 99×51×20mm와 M3 교체 나사를 적지만, 카탈로그의 명목 101×51×25mm 및 [실제 도면](https://www.hammfg.com/files/parts/pdf/1591XXASBK.pdf)의 100.90×51.40mm, 높이 25.00mm, #4×1/2 self-tapping 표기와 맞지 않았다. 도면의 PCB 94×44.50mm와 내부 높이 21.00mm도 별도 경계다. 따라서 **개별 페이지까지 내려갔다는 사실 자체가 정답 보증은 아니다.** 어느 자료가 오래됐는지·실제 부품이 무엇인지는 미확인이며 제조사 개정 도면이 다음 첫 자료다. 이 비유로 A/B 적합률을 높이지 않았다.

## 재현·수용·인계 제안

재현은 저장소 루트에서 다음 명령을 쓴다. 원 입력을 다시 검색하거나 다시 표집하지 않고 저장된 원장과 판독을 재결합한다.

~~~sh
python -B docs/workstreams/research/AF-RES-029/recount.py --check
python -B docs/workstreams/research/AF-RES-029/validate_artifacts.py --require-routes --output evidence/recheck-artifacts.json
python -B docs/workstreams/research/AF-RES-029/validate_results.py --output evidence/recheck-results.json
python -B -m workbench.session check docs/workstreams/research/AF-RES-029/manifest.json --fetch
~~~

실제 수행한 검사와 그 대상 SHA·입력 해시·종료 코드는 evidence/local-validation.json, 인계 전 결과 SHA에서의 재검은 evidence/handoff-checks.json에 있다. GitHub 원격 재독은 별도 영수증이다. 미실시 공급자 환경 시험은 [pending-checks](supplementary/pending-checks.md)의 명령·입력·사유를 따른다. 원 자료 보존/재현 통과는 표집 무노출이나 사람 판독의 충족을 뜻하지 않는다. [SELF_CHECK](SELF_CHECK.md)는 방법 질문 Q1–Q8별 주장·반증·남은 미확인을, [acceptance-evidence](evidence/acceptance-evidence.json)는 조건마다 참/거짓과 재개 자료를 남긴다.

공통 색인 반영 제안은 “제품명” 아래에 **호출자/입력/출력·필수 술어·지원판·정확한 API/타입/예제 절·남는 접합·원문 열람과 반환 완결의 별도 상태**를 기록하는 것이다. Q04/Q10처럼 제공자 경계를 바꿔야 하는 경우와 Q11처럼 같은 제공자에서 인용을 완결할 경우를 구별할 근거가 된다. 이 브랜치는 공통 색인이나 dot-control.json을 수정하지 않았다.

다음 첫 행동은 누락된 최초판/노출 영수증과 예산 해석을 분리해 고정한 뒤, 사전 결과를 보지 않는 질문별 새 문맥으로 재실험할 입력 투영을 만드는 것이다. 새 실험의 긍정 수를 요구하지 않으며, 원 12쌍과 실패는 계속 보존한다.
