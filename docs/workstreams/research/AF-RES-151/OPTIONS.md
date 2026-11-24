# OPTIONS — 선별 방법과 조건부 재심사

K=활성 참고 후보(A/B), C에서는 문서상 모든 atom S일 때만 K. H=보존하되 추천 보류. X=비교용 제외(실제 데이터 삭제 아님). atom S=확인 계약/동작, X=명시 불일치, U=미확인. 모두 S라도 문서 수준의 조건부 적격. 실제 실행·채택 아님.
A: 명시 실패 제외, 최대 S, 동률 앞 후보, 나머지 제외. B: 유일 확인 atom 후보 모두 K; 같으면 한 후보 K, 나머지 H; 일부 X 있는 후보도 부분 참고로만 K. C: 완전 확인된 후보 K, 나머지 H, 모든 원문 보존. 동일 후보별 최대3 문서 상한. 판독 비용=문서 근거 슬롯, 실제 시간 아님.
 
| 방법 | 원리와 출처 | 강점 | 실패·전환 조건 |
| --- | --- | --- | --- |
| A 단순 대표 | Debian 이미 포장된 요청 닫기 [D9](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=766891) | 읽을 목록 작아짐; K05 동률 atom 무손실 | K03 Mac 지원 근거 숨김; 새 조건에서 재심사 |
| B 조건별 보존 | F-Droid 기능/fork 구분 [D1](https://fdroid.gitlab.io/jekyll-fdroid/en/docs/Inclusion_Policy/), [D10](https://f-droid.org/en/2024/10/24/twif.html) | K03 OS별 근거 모두 활성 | 일부 X 후보의 부분 참고를 추천으로 오인할 위험 |
| C 가역 보류 | 종자은행 비활성 보관 후 필요 시 반출 [F1](https://www.seedvault.no/2019/09/11/withdrawal-of-icarda-aleppo-seeds-accomplished/), [F2](https://www.croptrust.org/what-we-do/programs/svalbard-global-seed-vault/) | 다음 요구에서 보류 원문 재사용 | 추천 목록에 무차별 노출하면 잡음; URL 변경/비용 미확인 |
| D 추가 대안(비교 미실시) | Met 매각 수익을 희귀 작품 구매에 재배분 [F4](https://www.metmuseum.org/ko/perspectives/building-and-caring-for-the-met-collection) | 보존 기회비용을 다음 증거 확보 예산에 투입 | 물리 공간/매각 수익과 링크는 다름; 소유권·복제 가능성 검증 전 영구 제외 금지 |

재심사: 새 요구의 환경/입출력/라이선스/접근성 변경→보류 원문 역조회. 새 버전/정책/복원→기존 판과 분리. D2→D3 실제 복원은 확인, 수정 diff 미확인. 동일성/재취득 가능성 확정→영구 제외 검토(판·원문·이유 보존). F3 권리 반환은 정당한 소유 관계 회복이지 효용 점수로 이식할 수 없음.
[audit.json](audit.json)에 12 제외 슬롯 역검토, 6 대조, 비용/잡음 구성 계산. 실제 이용자·재취득 노동/시간 미관측. 사전 인지도 노출로 진정한 가림 불성립.
