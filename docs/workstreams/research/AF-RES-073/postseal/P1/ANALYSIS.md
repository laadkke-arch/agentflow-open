# P1 사후 판독 — Q7·기원·반례

원 검색 원문 수집은 `fbc05801af45f21e60d6901f3293f9af9969ef8d`에서 봉인된 뒤 이 자료들을 읽었다. **원 검색 A/B/C 점수·비용·분자는 바꾸지 않았다.** 사후 작업은 API/열기 14회(메타데이터 전용 3회), 출처 행 7개이며 새 독립 원저작/사건 산입은 보수적으로 2개다. JEP 본문·PR·그에 따른 목록 추가는 모두 `JEP-122` 한 계보로 묶었다.

## 확인한 결론

Jupyter Book의 **조직적 편입은 승인되고 공식 목록에 반영되었다.** [governance PR229](https://github.com/jupyter/governance/pull/229)는 2024-06-27 22:52:05 UTC에 `bb2f862f2312ac78149cbd912fc8030c9cd76693`으로 병합되었고 `list_of_subprojects.md`에 Jupyter Book 한 줄을 추가한다. [같은 날 PR123의 jasongrout 발언](https://github.com/jupyter/enhancement-proposals/pull/123#issuecomment-2195794991)은 SSC와 EC 양쪽의 만장일치를 기록한다. 이것은 저장소별 이전 완료, 표준·프로토콜 적합성, 성능 개선을 입증하지 않는다. 출처 P1-POST-S02/S05.

A에서 읽은 external incubation은 2026년에 처음 생긴 선택이 아니다. [2021년 고정 문서](https://github.com/jupyter/governance/blob/9eb214d2f9a8ea51cb11e2f7e103ddd9213f4106/newsubprojects.md) L24–48,103–112,221–228에서 연동·범위 기준과 외부 incubation을 직접 확인했다. 제안자 Chris Holdgraf가 그 판에서 문서 서론을 수정한 이력도 있다. **문서의 당시 존재와 작성자의 모든 선택 인지는 다르다.** 2024년의 특정 외부 incubation 검토 발언은 찾지 못했다. [6월26일 발언](https://github.com/jupyter/enhancement-proposals/pull/123#issuecomment-2190510463)은 일반 의사결정 규칙을 실제로 인용한다. 출처 S02/S03.

## 날짜·인지·사용·채택을 분리한 표

| 기록 | 발행·판 시점 | 제안자의 선행 인지 | 당시 사용 가능성 | 실제 선택·결과 | 남은 미확인 |
| --- | --- | --- | --- | --- | --- |
| JEP122 issue / PR123 | issue 생성5월3일, PR 생성5월22일; 현재 본문은 후일 수정될 수 있음 | 부분 이전과 별도 조직 선호는 작성자 발언에 명시 | 현재 제안과 당시 논의 존재 | 6월27일 편입 승인, 6월28일 JEP 병합 | 모든 저장소의 이동·권한 기록 |
| New Subproject Process | 고정 commit 2021-09-15 | 작성자가 서론을 편집; 정확한 옵션 검토는 미확인 | 그 판의 integration/scope gate·외부 incubation은 확인 | 이번 사건에서 단계적 incubation 채택은 확인 못함 | 특정 옵션의 검토/기각 회의록 |
| GitHub Enterprise 전환 | [issue219](https://github.com/jupyter/governance/issues/219) 생성5월9일 | 5월7–8일 논의에서 알려지고 별도 조직 보안 우려가 줄었다고 발언 | EC가 생성 및 여러 조직 가입을 보고 | 중앙 정책 관리와 개별 조직 유지라는 운영 환경 변경 | 보안 감사·Book 조직 가입 이벤트 |
| 기술전략 글 | 날짜 모양 URL은5월20일이나 현재 본문 최초/수정 시각은 미확인 | 원 제안의 기술 전환 참조는 이미 알려진 자료 | 현재 글만으로 정확한2024 판은 고정 못함 | Sphinx stewardship 유지 방침과 migration 필요를 명시 | 실제 릴리스 시험과 기능 회귀 결과 |
| 12월 사용자 이의제기 | timestamped comment 2024-12-12 | 사후 사용자 관점 | 해당 없음 | 호환성 우려와 팀 책임 채널로의 안내가 기록됨 | 비판의 기술적 사실 여부는 검증하지 않음 |

## 최초판 보정

[PR123 commits API](https://api.github.com/repos/jupyter/enhancement-proposals/pulls/123/commits?per_page=100)가 반환한 첫 커밋은 모집에 쓴 `2b194a3c090fd375321871c47a3de503a0758206`과 같다. author/committer 시각은 모두 **2024-05-22 02:33:48 UTC**다. 동일 커밋·경로이므로 C1·C2·알려진 대안의 차이는 없다. 두 번째 커밋은 `feaf909c0cbc2cd9da16d814d31500c4b4453fb5`, 같은 날02:48:45 UTC다. 기원 비교는 origin-correction.json에 남겼다.

하지만 첫 Git 판은 창설 당시 판이 아니다. 5월3일 이슈는 이미 Google 초안을 가리키며, 선정 본문은3월 초 작성 시작을 말한다. 그3월 판은 확보하지 않았다. 재개에는 Google 문서 `1AtM3FHcgIfac3G-4eu4eSzZamLjreUofZbNZ6FzpGgM`의2024-03 및2024-05-03 revision export가 필요하다.

동결된 원실험 B receipt의 자동노출 설명 한 줄에는 P1 최초 Git을7월로 잘못 적었다. 원 모집 파일은5월22일로 정확하다. 원 영수증은 수정하지 않고 date-audit.json에 정정했다. 2026년 ONES 자료가 제안보다 후대라는 판정·검색 순서·비용은 영향이 없다.

## 자기 결론을 뒤집는 경로

- **단계적 외부 incubation을 새로 발견했다는 해석**에 대해 오래된 Git 원문을 조회했다. 2021 판에 이미 그 선택이 있어 현재 검색의 새 URL을 당시 제안자에게 새로운 선택으로 단정할 수 없다.
- **별도 조직은 보안 관리와 양립하기 어렵다는 해석**에 대해 당시 토론을 읽었다. [보안 담당자의 우려](https://github.com/jupyter/enhancement-proposals/issues/122#issuecomment-2099210148), [Enterprise 도입 후 우려가 감소했다는 답변](https://github.com/jupyter/enhancement-proposals/issues/122#issuecomment-2099511039), [작성자의 권한 경계 선호](https://github.com/jupyter/enhancement-proposals/issues/122#issuecomment-2099673053)가 함께 있다. 단일 조직 통합만이 가능한 설계였다고 할 수 없다.
- **조직 승인으로 기술적 호환성이 확인되었다는 해석**에 대해 [기술전략 글](https://executablebooks.org/en/latest/blog/2024-05-20-jupyter-book-myst/) L56–69 및 [12월 이의제기](https://github.com/jupyter/enhancement-proposals/pull/123#issuecomment-2539398527)를 읽었다. 이식 단계·일부 기능 변경 가능성은 별도 문제다. 이의제기를 회귀 시험의 사실 결과로 세지 않았다.

## 남은 최소 입력

조직 경계를 검증하려면 승인 당시의 포함/제외 저장소 명세와 각 저장소의 조직·관리자·정책 snapshot이 필요하다. C1은 표준·프로토콜별 적합성 기준과 해당 저장소의 증거가 있어야 확인할 수 있다. 기술 결과는 고정된 Jupyter Book v1/v2 릴리스 및 동일 입력의 migration 시험이 있어야 한다. 그 자료 없이 현재 목록이나 승인 투표만으로 적용 성공을 선언하지 않는다.

이 판독은 같은 작업자의 사후 비교다. 독립 인간 판독, 무힌트 실험, 독립 보안 감사는 없었다. decisions.csv의6행은 사전 선택·사후 기록·인지·당시 가능성·채택·미확인을 별도로 연결한다.
