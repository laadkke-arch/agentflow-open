# 핵심 관측 (③)

## 호출/사건 경계
- Datasets PR #6976의 실제 첫 부모는 e47a746bcda4b97db2467542b76d3215b3569ff0 (PR 표기 base e59582adc7fcb53a86a8ca8eda7e04a4e7b25bd2와 다름); merge 84d9dea52098c9403efb43d5b542dd6d45000bec, PR head 5c532a94e6e205c8a9516f5aa309686233e05a00. 두 반환 분기 수정. 포럼의 6/23 평가 및 학습 traceback은 같은 L197 일반 반환에서 실패하나 작성자/설치판/객체값 미확인. 12월 fasttext 호출은 다른 사건 후보. H01,H02,F01-F03.
- Astropy #16167은 사용자가 실패한 입력을 제시한 이슈가 아니라 유지자가 정책을 설계한 토론이다. 실제 입력은 미확인. 내부 비교 helper는 부모 cad8a7029b63c190d74c51cf7fa735e55791c3e1→4b727adcd13d73d9f5efcb2105e016453effb4e4; 후속 #16181 첫 부모 cf68c08c5479020e53a52937f587d27ef3f579c6→35d18ce8bd682a36e30a8f7ee86a8d5fac89e2bf (두 번째 부모 f010f718d4ee932a177f72d50b27478f4db1a8a5; PR 표기 base a36f316b22da93b36f222db6bc6772df7b0efe3d는 첫 부모 아님). A01-A03,F04-F10.
- 사건 수: 실제 하류 코드 변경 계보 2(HF/A), patch 3(HF 최초/A 최초/A 후속); 포럼 최초 1명 두 입구(C03,C04), 후속 다른 1명(C08) 동일 사건 매칭 불가; Astropy 설계 이슈 1건, 실제 사용자 입력 사례 0건, fixture 별도(C07). 동일 PR·파일·태그를 독립 사건으로 세지 않는다.

## 시간과 배포 판정 (Q5)
| 프로젝트 | 제안 | 병합 | 이전 태그/파일 | 이후 태그/파일 | 배포 목록 | 사용자 설치·재시험 |
|---|---|---|---|---|---|---|
| Datasets | 2024-06-17 | 06-19 | 2.20.0 98fdc9e78e6d057ca66e58a37f49d6618aab8130, 9570fb1808ca2a46b35da691c033802cd6eb601b; merge 대비 behind8 | 2.21.0 a1b5a32365cd2c6631fa4ad236a881f9f62bf32b, 2dae3a52fd38861512857f366400e85306f80ebd; merge 대비 ahead46 | PyPI 06-13 / 08-14 | 06-23 예외; 06-24 release 예정/1.x 권고; 2.21 설치·재시험 없음 확인 아님(미확인) |
| Astropy | 03-06 #16166; 03-08 #16181 | 03-10; 04-04 | v6.0.1 78cf5340ddf9fe9731906224a638c4888849c93f, 5c1cf2a04a5c791c9b242fdfcfca3a765d957b04; #16166 대비 diverged 263 ahead/575 behind | v6.1.0 e97756f0ecaa401e453745dd34d01980657ffa35, e1582174264f52a1b2cf3142d83ac1c6fae957b8; #16166 ahead188; #16181 ahead43 | PyPI 03-26 / 05-04 | 개별 사용자 기록 미확인 |

D01-D10의 고정 태그 파일과 compare metadata를 읽음. 첫 안정 배포 후보의 전후 코드 확인은 2/2, 모든 prerelease/tag 전수·wheel/sdist 내부·설치·동일 입력 재시험은 미확인. 일반 GitHub release HTML 실패를 PyPI 목록+tag code로 대체. Datasets 2.19.2/3.0.0은 비교용 추가 alias, Astropy v6.0.2 조회 404는 부재 전수 증명 아님.

## 단위 및 증거 구별
직접 관측은 source file/tag metadata/배포 목록에 한정. 행동 직접 실행 0건. 문서 계약, 기존 test assertion, 당사자 보고와 예상은 behaviors.csv에서 별도. Q2의 실제 런타임 Arrow dtype/값과 Astropy 사용자 입력은 모두 미확인. 2.0 ndarray strict와 Astropy Quantity 단위 변환 전체의 strict를 동일시하지 않는다.
