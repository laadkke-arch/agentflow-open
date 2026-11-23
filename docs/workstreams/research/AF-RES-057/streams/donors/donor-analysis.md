# 다른 분야의 정정과 보존 — 원전 조사

작성자는 donor 분담 조사자다. 이 문서의 직접 관측은 지도 원문·객체 이력, 회계 저자 예제와 코드, 원논문이다. 선정된 Yjs/ProseMirror 결과는 읽지 않았다. 제품 조작의 정답을 이 문서로 대신할 수 없다.

## 고정 창과 창 밖 읽기

정확 창은 [windows.json](windows.json)에 한 번만 기록했다. 지도18단어는 OSM Change rollback의 원기록 흔적 보존 절, 회계22단어는 GnuCash의 원거래+역분개 동시 존속 절이다. E는 각 자리의 D와 같은 단어 수로 맞춰야 한다. 그림·코드 행은 모두0이다. 당대 가용성을 확인한 지도[2018-03-25 판](https://wiki.openstreetmap.org/w/index.php?title=Change_rollback&oldid=1593604)과 회계[2017-04-29 저자 커밋](https://github.com/Gnucash/gnucash-docs/blob/a996acb04c02cd3ef7112daf0f7c99f6d0cc86b2/help/C/Help_ch_Transactions.xml#L491)에 동일 창이 있다. 현재 문서를 먼저 골랐고 그 뒤 역사판을 대조했으며, 과거 사용자가 읽었다는 뜻은 아니다.

전체 원문을 읽은 조사자가 알고 있는 '뒤 변경의 의미를 판별하라'는 더 강한 지도 원리는 표시 창 밖이다. 이 원리를 예측 근거로 쓰면서18단어 카드만의 효과라 부르면 안 된다. [선택 기록](selection-log.md)에 더 유익한 절로 임의 교체하지 않은 이유와 한계를 남겼다.

## Q4. 실제로 남은 것과 남지 않은 것

| 원전/사례 | 대상·사건과 직접 확인한 상태 | 보존/제거 | 편집기로 가져갈 질문·전이 한계 |
| --- | --- | --- | --- |
| D01/D06 OSM 지침 | [Change rollback](https://wiki.openstreetmap.org/wiki/Change_rollback#Clean_and_dirty_reverts_(conflicts)) 및 [JOSM Reverter](https://wiki.openstreetmap.org/wiki/JOSM/Plugins/Reverter#How_does_it_work?) | 객체 ID·이력과 현재 지도상의 효과는 별개다. JOSM은 뒤 수정이 있으면 충돌을 만들어 검토하게 할 수 있다. | 이력 흔적을 남길 것인가, 현재 객체 내용을 남길 것인가, 뒤 변경이 잘못된 앞 변경에 의존하는가? 이 지침이 특정 CRDT의 출력 문자열을 계산하지 않는다. |
| D04/D05 Casablanca | [원요청](https://community.openstreetmap.org/t/need-help-reverting-a-changeset/123855), [way284293874](https://www.openstreetmap.org/way/284293874/history) | v10의 trunk/100 → v11의 motorway/120 및 태그 변경. v12 다른 작성자가 access=no 제거. v13 name:fr 추가. v14/v15 정정 뒤 태그와 노드 참조는 v10과 동일. 전체 버전은 이력에 남고 name:fr는 제거됐다. | '뒤의 편집을 모두 남긴다'는 일반화가 깨진다. v12 제거 효과가 남아도 v10에도 access가 없으므로 선택적 보존과 단순 복원 중 어느 이유인지 외형만으로 판별되지 않는다. |
| D12/D12H Payap | [DWG의 원문 실행 진술](https://community.openstreetmap.org/t/deletions-around-payap-university-chiang-mai/71883/9), [way224498221 이력](https://www.openstreetmap.org/way/224498221/history) | 삭제30557777과 정정30806377의 객체 ID 집합은295개로 같다. 첫 삭제 way의 v1은 주차장 통로, v2는 삭제, v3은 같은 ID의 복원이며 v1/v3의 표시 여부·태그·노드 참조가 같다. | 이 객체에는 삭제와 복원 사이의 다른 버전이 없다. 한 객체 상태와295개 ID 집합을 확인했으며295개 모든 상태·지리적 타당성은 미확인이다. 깨끗한 복원과 dirty-revert 성공을 같은 종류로 세지 않는다. |
| D03 GnuCash 환불 원장 | [저자 예제7.4](https://www.gnucash.org/docs/v5/C/gnucash-guide/cc-enterpay1.html), 그림7.1·7.2 직접 시각 확인 | Visa500.00 → 구매74.99로574.99 → 환불74.99로500.00. Clothes74.99 →0.00. 구매와 환불 행은 둘 다 존재한다. | 금액 효과의 상쇄와 원기록 삭제는 다르다. 문서 본문에서 글자를 삭제하는 것과 감사 기록에서 연산 흔적을 보관하는 층을 구분해야 한다. GUID/실행판은 그림에서 미확인. |
| D14 GnuCash 대사 실패 보고 | [요청자2017-05-15](https://lists.gnucash.org/pipermail/gnucash-user/2017-May/070671.html), [후속](https://lists.gnucash.org/pipermail/gnucash-user/2017-May/070677.html) | 대사된 거래를 바꾼 뒤 임시 거래를 넣어 대사를 마치고 역분개로 현재 잔액을 복구했다고 보고했다. 이후 대사 시작잔액 문제로1~2개월 같은 임시 조치를 썼다는 설명이 있다. | 현재 값 복원과 다음 처리의 의미는 다를 수 있다. 구체 원장·수치·고정판이 없어 기능 결함으로 확정할 수 없다. 편집기의 같은 문자열·다른 다음 undo 상태에 대응하는 질문만 준다. |

Casablanca의 정확 버전/작성 주체/차이/URL은 [map-case-observations.json](map-case-observations.json)에 있다. 관계가 다른 두 변경의 저자를 동일 주체로 합치지 않았다. 뒤의 name:fr도 문제 작성자 자신의 추가이고, 별도 작성자의 v12는 access 제거다. 서로 다른 두 주체가 각각 독립 내용을 추가한 편집기 시험과 동일 사건이라고 주장하지 않는다.

Payap의 선택 규칙은 원 변경집합 문서 순서의 첫 삭제 way를 이력 열람 전에 정하는 것이었다. [payap-case-observations.json](payap-case-observations.json)에 v1/v2/v3와 비교 범위를 보존했다. 이 결과는 ID와 이력의 존속을 확인하는 정상 대조이며, 뒤 편집 보존의 경계 사례는 Casablanca가 담당한다.

## 회계 원리를 잘못 옮기는 반례

[매뉴얼6.8](https://www.gnucash.org/docs/v5/C/gnucash-manual/trans-reverse.html)의 형식회계 설명은 원거래를 남기라고 권하지만, 같은 매뉴얼은 [수정6.6](https://www.gnucash.org/docs/v5/C/gnucash-manual/trans-edit.html)·[삭제6.7](https://www.gnucash.org/docs/v5/C/gnucash-manual/trans-delete.html)도 명시한다. 따라서 이 문구만으로 GnuCash가 모든 거래의 불변 감사이력을 강제한다고 말할 수 없다.

[D10 엔진 원전](https://lists.gnucash.org/docs/STABLE/group__Transaction.html)의 reverse는 복제된 거래의 split 수치를 반전하고 원거래에 reversed-by 연결을 기록한다. [고정 소스 D10H](https://github.com/Gnucash/gnucash/blob/038405b3700aca653f04fb4f2179f22266146262/libgnucash/engine/Transaction.cpp#L2817)에서도 이 동작과 원거래의 사전 balancing/commit이 보인다. 원기록이 살아 있어도 모든 수치·메타데이터가 불변이라는 뜻은 아니다. void는 유효 수치와 조회·대사 처리에 별도 규칙을 쓰고, unvoid는 복원 기능이다. 같은 잔액이라도 역분개와 void가 같은 기록 상태는 아니다. 코드 설명의 write-only 감사 기능은 미래 가정으로 쓰였으며, 실제 도입 완료 증거가 아니다. 생성 API 페이지의 버전 머리글과 고정 소스의 줄 위치가 달라 정확 빌드 동일성은 주장하지 않고 두 취득을 따로 기록했다.

일반화가 깨지는 조건은 (a) 시간·작성자 단위가 실제 취소 단위와 다름, (b) 원거래의 원자료를 바꿔 계산 기반이 달라짐, (c) 현재 효과만 상쇄했는데 다음 상태/대사/redo가 달라짐, (d) 금액 덧셈처럼 생각했지만 텍스트 위치와 종속 문구는 순서에 민감한 경우다. 이는 자료를 바탕으로 한 전이 가설이며 제품 시험의 관측값이 아니다.

## 원논문이 제공하는 반대 의미론

[Prakash·Knister1992](https://web.eecs.umich.edu/~aprakash/papers/prakash-knister-cscw92.pdf) §4~7은 작성자별 연산 선택, 뒤 연산으로 이동한 위치, 의미적 충돌을 따로 다룬다. 원이력에 반대 연산을 덧붙이며, 독립 연산은 변환하고 종속 연산은 먼저 처리해야 한다는 전제가 있다. 동일 문서 상태와 동일 연산열을 구별하므로, 화면만 비교하는 검증의 부족을 짚는다. 응용 프로그램이 inverse/conflict/transpose를 정확히 제공해야 한다는 조건이 있으며 이 연구가 두 제품 구현을 인증하지 않는다.

[Yu·André·Ignat2015](https://members.loria.fr/CIgnat/files/pdf/YuDAIS15.pdf) §3은 앞 문장과 그 안에 나중에 추가한 부정어를 예로 든다. 앞 문장이 사라졌을 때 부정어만 남기는 것이 무의미할 수 있으므로, 앞 연산에 의미적으로 기대는 문자열을 함께 숨기는 정책을 제안한다. 사용자가 예외를 선택할 수 있는 국소 경우와 원격/동시 상황의 자동 처리도 구분한다. 그러므로 '다른 사람의 모든 글자 보존'은 유일한 보편 정답이 아니다. 원래 사용자 목적이 보존을 요구하면 그 목적을 채점해야 하며, 논문의 기본 정책을 덮어씌우면 안 된다. §6은 형식 증명을 범위 밖으로 명시한다.

## 설계자에게 반환할 때

지도 링크는 변경 이후 다른 사람의 기여를 어떤 단위·의미로 보존할지 묻는 용도로, 회계 링크는 현재 효과와 원기록/정정기록의 존속을 분리하는 용도로 유효하다. API만으로 origin·group 경계가 이미 정해진 자리에서 donor가 같은 예측을 반복하면 구현 선택 근거를 더했다고 세지 않는다. donor가 다른 예측을 냈어도 실제 같은판 결과를 확인하기 전에는 더 정확하다고 판정하지 않는다. 문서 작성자, 공동 편집 상대, 구현자, 지도 편집자, 원장 관리자의 보존 목표는 겹칠 수 있지만 자동으로 같지 않다.

## 배당·검토 범위

고유 외부 저작은 현재11개다. 같은 매뉴얼의 여러 절·시대판·그림, 하나의 지도 사건의 게시글·변경집합·객체 이력은 각각 한 계보로 합쳤다. 직접 사례는 계획4계보/실제4계보(지도2/2·회계2/2)다. 수치 원장 또는 같은 객체 상태를 대조한 사례는3/4이고, 수치 원장 없이 저자 실행 진술을 읽은 사례는1/4다. 지도 각 사건에서 모든 변경 객체의 상태를 검증한 것은0/2이며, 두 경우 모두 선택 객체1개씩만 확인했다. 이 세 수치는 서로 다른 단위다. 우리 재실행으로 원 사용자의 실행을 재현한 사례는0/4(미실시)다. 원논문2편의 관련 절을 직접 읽었으며 성능 실험을 재실행하지 않았다. sources.jsonl26행 가운데 실패3행은 계수에서 제외한다. 이 분담은 전체 연구20저작 하한의 일부이고 여섯 자리 검증 상태를 대리하지 않는다.
