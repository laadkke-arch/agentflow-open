# REVIEW-41 · 링크 한 개가 증명하는 것과 다음 원문이 필요한 곳

탐색기는 사용자가 만들 소프트웨어의 전체 또는 선택한 부분과 그 목적을 받아, 도움이 되는 완성품·부품·다른 분야 원리의 링크와 적용 이유를 돌려준다. **이번에 새로 DONE이 된 8건은 모두 PARTIAL로 인계됐다.** 그 안에서 실제로 확인할 수 있는 차이가 있다. 한 기관의 분류 오류를 고쳐도 다른 객체의 참조에는 별도 수정이 필요했다. 당사자가 통지 내용을 인용해 티켓을 다시 연 기록도 있었다. 같은 계산기 과제에서는 기존 부품을 그대로 쓴 집단과 수정한 집단의 작업량 차이가 서로 반대 방향이었다. 각각의 근거가 답하는 범위와 아직 권할 수 없는 문장을 아래에 구분했다. [제품 브리프][product] · [연구 운영 규칙][workflow] · [161 필드 원장][fields161] · [163 회신 원장][joins163] · [164 시간 원표][raw164]

## 어디까지 검토했는가

`work/planning@4997e4c`의 최신 파일인 REVIEW-40을 먼저 읽었다. 그 검토의 **마감판** `82c3f51`을 이번 통합판 `53eaa28`과 ID별 모든 필드로 대조했다. 이전 158행은 전부 동일하고 161~168만 추가됐다. 각 행의 `result_commit`은 해당 작업 브랜치의 원격 끝과 일치했다. 그 여덟 소유 경로의 인계·결과·근거 원장을 읽었다. 40차까지의 판단은 직전 REVIEW에서 이어받았다. [직전 누적 검토][r40] · [직전 마감 진행표][before] · [이번 진행표][control] · [두 판의 차이][delta]

| 진행표 고정판 (UTC) | 전체 | DONE | 진행 중 | BLOCKED | 이번 검토에 처음 들어온 DONE |
| --- | ---: | ---: | ---: | ---: | --- |
| 40차 마감 `82c3f51` | 158 | 154 | 0 | 4 | 기준 |
| 41차 `53eaa28` (11월 24일 18:10:31 커밋) | 166 | 162 | 0 | 4 | 161~168 |

현재 DONE 162건은 연구 160건과 연결 시험 2건이다. 중앙 `acceptance_evidence`는 162건 모두 빈 배열이다. 차단된 네 건의 사유도 그대로다. 018은 대화 한도 뒤 인계 미커밋, 035는 기존 Codex 실행 종료 뒤 인계 미확인, 149는 확인한 7주 중 세 유입 경로를 각 6항목씩 복원한 주가 0, 151은 최초 N0 응답·독립 가림 판독·원사용자 비용 증거 미확보다. 이 네 건의 결과물을 다시 열거나 재배정하지 않았다. [진행표의 상태와 사유][control]

| 새 작업 | 중앙 등록 인계판 | 인계가 지정한 결과·자기점검판 | 출처 원장 행 / 작업자가 실질 자료로 센 저작 |
| --- | --- | --- | --- |
| 161 · 참조 복구 | [PARTIAL · 810904a][h161] | [fb1c5e9][r161] | [84 / 26, 이 중 거래·판 이력 2][s161] |
| 162 · 단계적 제공 | [PARTIAL · de55ea1][h162] | [7229b71][r162] | [83 / 43][s162] |
| 163 · 통지와 회신 | [PARTIAL · 360d971][h163] | [48fc585][r163] | [74 / 24, 진입·배경을 포함한 열람 저작은 28][s163] |
| 164 · 재사용 노동 | [PARTIAL · df07150][h164] | [e7908cc][r164] | [38 / 20, 교정 저작 포함 21, 지정 범주 충족 12/22][s164] |
| 165 · 예제 자산 배포 | [PARTIAL · 2c9e649][h165] | [488fd68][r165] | [54 / 22][s165] |
| 166 · 대기열 원리 | [PARTIAL · 8fc8b77][h166] | [f6063d4][r166] | [61 / 42][s166] |
| 167 · 형식 교환 | [PARTIAL · 0d7917c][h167] | [9f1c3cc][r167] | [97 / 56][s167] |
| 168 · 호환성 출전 | [PARTIAL · 5e1010c][h168] | [15e99f8][r168] | [78 / 35, 발행 메타데이터 등 네 저작 제외 시 31][s168] |

이번 검토에서는 고정 커밋의 출처 기록 569행을 JSON으로 읽고 핵심 CSV의 행·범주와 164의 원표 산술을 다시 셌다. 위 오른쪽 열은 각 작업자의 서로 다른 산입 기준을 따른다. 외부 원문 전체를 독립 재판독하거나 당시 프로그램을 재실행한 수치로 사용할 수 없다. 아래의 ‘보고’는 당사자나 시험 저자의 기록, ‘원값’은 해당 작업이 고정 파일·표·revision에서 읽었다는 관측을 뜻한다.

## 40차까지 축적된 판단

| 제품에서 내려야 할 결정 | 누적 근거 | 아직 열려 있는 선택 |
| --- | --- | --- |
| 먼 분야의 원리를 왜 보여 주는가 | 010은 분야 단서로 원리 7군을 찾았다. 033은 단서 없이 본 144쌍에서 당시판 지지 0, 022는 미인지→선택 변경→시행 0/24, 145는 독립 초안 0/16·유효 검색 짝 0/8이었다. 157은 15,062,721바이트의 Sketchy CSV 196행을 읽었지만 과제 키·개봉 시각·전후 저장판이 없어 핵심 8자리에서 엄격 연결 0이었다. | 원리의 구조적 대응, 실제 선택을 가르는 예측, 개인이 처음 알고 바꾼 행동에는 각각 다른 증거가 필요하다. 62개 같은 배열을 ‘무변경 62회’로 세지 않는다. |
| 부분 구조를 받으면 무엇을 더 물어야 하나 | 020은 주장 72/73을 전달했어도 충돌을 모두 푼 묶음은 2/16이었다. 103은 외관 10/10을 지키고 텍스트 선택을 잃었고 107은 발생 위치를 주면 개별 편집 6/6, 공유 정의로는 0/6이었다. 159의 자연 48자리에서 실제 위치는 기능 46개, 소비 역할은 48개를 갈랐다. 틀린 문맥도 38번 같은 번역 문자열을 돌려줬다. | 사용자가 고를 객체·바로 다음 조작·보존할 속성의 역할을 함께 본다. 159는 한 작성자의 고정판 역참조다. GUI 관찰과 사용자의 이해시간은 비었다. |
| 후보 폭과 표시 수를 어디까지 늘릴까 | 040은 완전 적격 0/8, 044의 8개 후보 풀에서는 두 묶음 방식이 같았다. 114의 ‘충돌’ 138/144를 118 기준으로 다시 보면 명시 충돌 7·미확인 131, 나머지 6은 일부 지지다. 146의 4요구×12후보는 직접 0·일부 15·충돌 14·미확인 19. 검토 폭 3→8에서 더 표시한 세 건은 모두 한 요구의 5·7·8위였다. | 낮은 순위, 자료집 부재, 일부 조건 충족과 명시 반박을 나눈다. 두 부분 링크가 같은 사용자 요구 안에서 함께 성립하는지는 별도다. |
| 무엇을 기억해야 같은 답을 다시 줄까 | 055는 과거 답 4/4·다음 판 0/4, 075는 후보 전체가 없을 때 단독·공동 1위 주장을 각각 16/16 보류했다. 147은 당시 증빙으로 과거 질의 112/112를 복원했다. 150의 A/B/C 세 저장안은 동일성 값과 근거가 함께 맞은 수가 7/9/15(각 16쌍)였다. 안정 절 4개의 재열람 32/32에는 주소 하나가 충분했다. | 현재 같은 대상을 가리키는지, 예전 판을 읽으려는지, 후보 간 우위를 입증하려는지에 따라 필요한 이력과 비용이 달라진다. |
| 새 자료를 찾고 옛 추천을 언제 확인할까 | 024는 정기 점검으로 무효화 11/11, 신호로 8/11을 포착했다. 후자는 원문 열람은 108개 적고 전송량은 5,672,462바이트 많았다. 152의 유보 신규 15건에서 신호/희소 공급원 보장 14, 정기 13. 공통 13건의 지연 중앙값은 높은 예산·주류 수요에서 정기 27시간 대 신호 51시간, 낮은 예산·희소 수요에서는 92.1 대 27시간이었다. | 요청 시 정책의 높은 예산·희소 수요 기본값 309/364와 과거 목록 전체가 같은 비용일 때의 350/364는 조건이 다르다. 현재 계정에서 실제 쓸 수 있는 시점도 공지와 별개다. |
| 사용자 노동까지 얼마나 줄었나 | 034의 한 단계는 380→57초, 전체는 849→847초였다. 140의 둘째 절 7개가 새로 푼 핵심 조건은 0. 156은 Django·pandas 하류 수정은 확인했지만 실측 인시는 12행 모두 미확인이었다. 160의 GOESIM 이식은 1,061.9인시였으나 FORTRAN 198~220인일은 추정이었다. 비교 후보 12행은 소프트웨어 8·교통 2·기록관 2였고 동등 소프트웨어 양팔은 0이었다. | 읽기·도구 적응·검수·납품 이후 지원을 포함하는 범위에 따라 절감의 의미가 달라진다. 단위와 품질이 같은 비교쌍이 우선이다. |

154의 Paperless-ngx v2.2.1에서는 입고 10/16 성공, 그중 명시 원본 10/10 회수, 기본 다운로드 동일 바이트 6/10이었다. 158의 제출 사건 28개에서는 별도 통지 수신·원본 동일 바이트·최종 공개판이 각각 전부 미확인이었다. 155에서는 동일 출력 문자열과 내부 AST 속성이 갈렸고 자연 대조는 0/4였다. 153의 원거리 예시는 독창성·품질 평정과 유용성 평정이 일관되게 같은 방향을 보이지 않았다. 과거 세부 정정도 유지한다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤 275이며, 136의 고유 면 9개·열람 10회·답–면 연결 16쌍은 각기 다른 단위다. 입력 API, 수집기, 저장소 구조, 출력 링크 수는 설계 대안으로 열려 있다. [40차 누적 검토와 원문 색인][r40]

## 새 결과에서 실제 근거가 닿은 곳

### 161과 162 · 옛 참조를 되살리는 일, 오늘 쓸 수 있음을 확인하는 일

**161.** Wikidata 보강 사례에서 기관 Q59165607의 잘못된 병합 직후에 undo가 왔다. 건물 Q314104의 P910은 별도 봇이 Q55296215→Q59165607로 바꾸고, 기관 쪽 복구 1분 뒤의 별도 undo에서 옛 값으로 돌아갔다. 22개 필드행 중 값을 연결한 7개는 대상 3개 수정·기존 무관 필드 4개 유지였다. 두 객체의 이력은 한 사건 계보다. 병합 후 **독립적으로 추가된** 유효 필드를 지킨 사례는 분모 0이다. Open Library #6371의 제목·설명·표지·주제 손실 네 행은 보고 수준이다. 거래 42049802와 작품 OL14863262W 판 24~26을 잇는 구성원 기록은 없었다. 자연 모집에서 OL 첫 16자리의 연속 원판 0, Wikidata의 예정 순위 16자리도 미복원이다. 현재 자료로는 원판 한 절을 재확인하거나 특정 하류 관계의 별도 복구를 안내할 수 있다. 일반적인 선택 복구의 무손실 보장은 유보한다. [거래 원장][trans161] · [필드 원장][fields161] · [기관 취소 revision](https://www.wikidata.org/w/index.php?diff=1048159568&oldid=1038289881) · [원 손실 보고](https://github.com/internetarchive/openlibrary/issues/6371)

**162.** GitHub의 한 조직에서 issue-type 필터가 보인 날에도 일괄 수정은 보이지 않았고, 이후 직원의 수정 공지 뒤 당사자 재시험은 찾지 못했다. Google의 같은 공지에는 Rapid Release 완료 뒤 철회와 Scheduled Release 중단이 기록됐다. 구성한 14개 질의에서 ‘공지 날짜만’ 쓴 답은 당사자 보고와 3건, 공식 조건·집단 상태와 3건 충돌했고, 2건 일치·6건 정답 미확인이었다. 조건과 관측을 함께 읽은 답은 당사자 보고에 맞는 4·공식 조건에 맞는 4·보류 6이었다. 이는 설계한 보기에서의 개수다. 자연 20자리 중 태그 내 잠정 6, 빈자리 14, 복원된 전체 모집창 0/4였다. 동일 계정·설정·조작에서 처음 활성화되기 전 부재와 이후 성공을 이은 엄격쌍은 0이었다. 수리 전후 두 사례의 시각을 신규 출시 시각으로 쓸 수 없다. [질의별 14행][ad162] · [관측 18행][obs162] · [GitHub 당사자·운영자 기록](https://github.com/orgs/community/discussions/148715) · [Workspace의 수정 공지](https://workspaceupdates.googleblog.com/2023/12/easy-access-to-people-documents-blocks-in-google-docs.html)

### 163과 164 · 특정 사람의 반응과 노동을 어디까지 말할 수 있는가

**163.** 선택된 통지 36행 중 생성·발신 기록은 35였다. 원제출자 표적 19, 종료자 확인 16(원제출자와 같은 사람이 종료자 역할을 한 1행 포함), 표적 미상 1이다. Debian #1020248에서 원제출자는 첫 종료 통지의 시각·내용을 지목하고 재개했다. 같은 티켓의 두 번째 종료에 그 답장을 붙이면 시점이 뒤집힌다. 특정 내용의 인지·행동은 이 보강 사건 1건, 수신함 전달은 **36행 모두 미확인**이다. 자연 모집 20자리를 기준일에 배정한 수는 0이었고 30일 관찰창 전체를 복원하지 못했다. 운영 조직별 관측도 Debian만 있다. 따라서 이 원장에서 이용자 반응률을 계산할 수 없다. 규약으로 생성 조건, 개별 로그로 발신, 당사자 회신으로 특정 내용에 대한 행동까지 문장의 강도를 올릴 수 있다. [통지 원장][nt163] · [조인 13행][joins163] · [당사자의 재개 답장](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1020248#97)

**164.** Lattanzi 실험 2의 동일 후위표기 계산기 과제에서 세 집단은 각 8명이었다. 24행 모두 설계·라이브러리·코딩·디버깅을 더한 값이 원표 총계와 맞는다. 평균은 직접 구현 A 98.125, 제공 스택 사용 B 65, 수정 상속 C 115.625다. A−B는 +33.125, A−C는 −17.5 원척도이며 같은 A 집단을 두 번 썼다. A와 C의 유의한 차이는 검출되지 않았다. 표의 ‘Hours’, 단위 없는 부록 G.1, 기록 양식의 시간 범위 사이 관계가 확인되지 않아 분이나 인시로 환산할 근거가 없다. 저자는 모두 합격했다고 했지만 개별 검수표와 제출 코드는 미취득이다. 모집 16자리의 DBLP 원순서도 복원되지 않았고 엄격한 물리 단위·동등 품질 대조는 0이다. ‘기성 부품을 쓰면 빨라진다’는 안내에는 그대로 쓸 때와 고쳐 쓸 때, 공급자 노동, 인수 수준이 빠져 있다. [24명 원자료][raw164] · [비교 원장][contrast164] · [원 학위논문 부록](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content#page=182)

### 165와 166 · 대체 자산과 다른 분야 원리를 권하는 조건

**165.** jpeginfo v1.7.1에는 프로그램 고지와 별도로 시험 사진의 NC-SA 고지가 있었다. Debian의 repack 보고와 같은 심사판의 소스 test 디렉터리·amd64 바이너리 목록에서 지정 JPG 부재를 연결했다. darkslide 6.0.0-2에서는 실제 WOFF2 포함을 보았지만 원 글꼴과 이를 포괄하는 권리 근거는 미확인이다. 공개 배포 사례 8건 중 정확한 심사판과 목록이 맞은 것은 2건, 소스와 바이너리 양쪽을 지정 경로까지 확인한 것은 jpeginfo 1건이다. FreeCAD의 CC0 표명 뒤 제외 항목이 삭제된 사실도 실제 바이너리의 글꼴 확보와 구별해야 한다. 자연 20자리의 원순위는 0건 복원, 파일 단위 상류 원전은 5/6, 실제 파일 교체 뒤 판단이 바뀐 완결 사례도 없었다. 이 자료는 한 배포자의 당시 처리 범위와 고지를 설명한다. [파일 16행][assets165] · [처분 8건][dec165] · [상류 시험 사진 고지](https://github.com/tjko/jpeginfo/blob/v1.7.1/test/README) · [Debian repack 기록](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1064380)

**166.** Kueue #407에서 합산 CPU 할당량 안에 들어온 C는 노드마다 남은 자원에는 맞지 않았다. C의 입장 승인과 실제 시작을 같은 ‘다음 작업’으로 세면 D가 막힌 이유가 달라진다. Slurm의 backfill에는 상위 작업의 예상 시작을 늦추지 않는 조건이 이미 있으므로 관측소의 보호 시간창을 덧붙여도 같은 예측이 나올 수 있다. 도서관의 원순번 보존·유예·만료는 설계자가 확인할 조건을 추가했다. 그러나 자연 10자리 확정 0, 보충 12건 중 동시에 대기하는 두 작업의 상태가 엄격하게 나온 것은 이미 노출된 1건이다. 12개 행 × 4규칙의 **48개 예측 셀**과 후속 12행 모두에서 사전 비교 적격은 0이었다. 도서관·관측소 모두 개별 두 작업의 배정 기록은 각 0/2다. 공개 운용 규칙과 집계는 읽었지만 외부 원리만이 맞힌 새 선택은 확인되지 않았다. [사전 예측][pred166] · [후속 판정][out166] · [Kueue #407](https://github.com/kubernetes-sigs/kueue/issues/407) · [당시 Slurm 규칙](https://github.com/SchedMD/slurm/blob/slurm-23-02-7-1/doc/html/sched_config.shtml#L53-L80)

### 167과 168 · 같은 규격 또는 여러 사이트가 지지하는 주장의 크기

**167.** IFC 사건 I04의 송신 파일에서 FOOT=0.3048m, precision=0.0001을 직접 읽었다. 수신 프로그램판은 비어 있다. I10에는 Archicad 24 add-on 3008과 Bonsai fcee54c, 고정 IFC ZIP과 경계 형상 차이 보고가 있지만 ZIP 속 값과 실제 수신 출력을 직접 맞추지는 못했다. 38개 교환 후보의 보고층에서 도구 두 개와 파일명/값이 연결된 11건은 전체 파일 미공개인 I13을 포함한다. I18은 별도 비공개 원본 사례다. 전체 공개 파일을 요구하면 10건(악보 6·IFC 4), 양판과 고정 공개 파일이 특정된 보고는 I10 1건, 정확판·같은 파일·실제 수신값의 직접 조인은 0, 완결 왕복도 0이었다. 보강된 구조해석 시험 논문이 보고한 정·역방향 하중의 차이는 방향을 확인할 근거다. 역방향이 같은 파일의 왕복이었는지는 따로 입증해야 한다. [교환 원장][ex167] · [속성 43행][prop167] · [I10 원보고](https://github.com/IfcOpenShell/IfcOpenShell/issues/6113) · [양방향 시험 논문](https://doi.org/10.3390/app112311430)

**168.** 8개 CSS 속성·값×데스크톱 제품 2종에서 정확한 값 전용 셀은 2024 고정판 0/16, 2025판 4/16이었다. 추가된 셀은 serif와 normal의 소급 상세화다. Chrome 131·Firefox 133에서 해당 값의 렌더가 그해 처음 가능해졌다는 의미를 부여할 근거는 없다. 두 사이트의 옛 구문 주석이 같은 Mozilla Hacks 글을 가리킨 것은 확인했지만 다른 모든 셀도 같은 관측에서 왔다는 주장은 미확인이다. 정식 모집 순위 0/16, 당시 화면 보존본 0/32, 대상판·같은 술어의 실제 실행 증빙 0/16이었다. 0은 확보한 수다. 원래 실행된 횟수는 알 수 없다. BLS/FRED의 같은 실업률 계열과 공항 관측 메시지·표의 단위 환산은 같은 원천을 여러 화면에 표시할 수 있다는 대조다. 한 속성의 지원과 특정 값의 실제 동작은 각각 다른 원문이 필요하다. [주장 16행][claims168] · [출전 28행][prov168] · [collector를 인용한 PR](https://github.com/mdn/browser-compat-data/pull/26792) · [추정한 지원판을 밝힌 PR](https://github.com/mdn/browser-compat-data/pull/28265)

여덟 건에 공통된 약점은 원문 개수가 많아도 모집한 대상과 판별할 대상이 만나지 않은 곳이 있다는 점이다. 161의 실제 판 이력 2개는 한 사건, 164의 원척도 대조 2개는 한 실험, 166의 보충 48셀은 실제 결과가 확인된 48작업이 아니다. 167의 링크 원장은 7행이며, 결과표에 제시한 구체 목적 6개와 마지막 교환 수락 기준 행을 구별해야 한다. 168의 여러 사이트 표시는 같은 실행의 수를 알려 주지 않는다. 따라서 이들 결과를 더한 성공률은 만들 수 없고, 원문 한 건이 충분한 질문과 추가 관측이 필요한 질문은 분명하게 가를 수 있다. [161 거래][trans161] · [164 비교][contrast164] · [166 예측][pred166] · [167 링크][links167] · [168 관측][obs168]

## 다음 웹 작업 9건

여덟 인계의 핵심 결측에는 각각 다른 공개 자료를 배정했다. 아홉 번째는 후보 두 개에 부분 근거가 있을 때 원질문이 ‘둘 중 하나’와 ‘같은 빌드에서 둘 다’ 중 무엇을 요구했는가를 다룬다. 이것을 판별해야 검색 전에 원뜻을 보존하고 검색 뒤 두 링크를 함께 권할 수 있다. 아래 선행 ID는 모두 `53eaa28`에서 DONE이다. 같은 회차의 다른 작업 결과가 없어도 각 조사에 착수할 수 있다. 배정 상태는 제안 단계인 `READY_NOT_STARTED`다. [아홉 작업의 개별 brief](NEXT_TASKS-41.json) · [진행표][control]

| ID · 선행 | 모집 대상과 고유 판정 단위 | 끝내면 무엇을 결정할 수 있는가 |
| --- | --- | --- |
| 169 · 161 | ISO 639-3 변경 결정→IANA 레코드→CLDR/실제 소비자. 분할된 옛 언어 코드 한 개와 하류 대응 한 건. | 원문 재열람에 한 주소면 되는지, 현재 언어 도구를 권할 때 여러 후계·문맥 질문이 필요한지 정한다. |
| 170 · 162 | Wikimedia 공개 위키의 DiscussionTools·VisualEditor. 사이트·역할·표면·조작이 같은 배포 전후 관측. | 발표, 특정 위키의 기본 설정, 그 위키에서 실제 저장할 수 있었던 시점을 각각 어느 원문이 지지하는지 정한다. |
| 171 · 163 | WCAG와 XPath의 공식 의견처리 회차. 의견·편집 답변·원제출자 회신·최종 절의 같은 변경. | 직접 확인한 문장이 ‘변경됐다’, ‘내용을 인지했다’, ‘그 수정에 동의했다’ 중 어디까지인지 정한다. |
| 172 · 164 | 공개 소프트웨어 실험의 과제지·노동 기록·합격표. 직접 구현, 기성 부품 사용, 수정 사용 세 경로의 측정 설계. | 중단·인수·생산자·후속 노동을 분리한 양식에 원자료를 대입해 비교 가능한 차이와 보류해야 할 절감을 정한다. |
| 173 · 165 | LibreOffice·TeX Live에서 대체 글꼴을 선택한 사건. 같은 문서의 문자·줄·페이지라는 실제 요구 속성. | 파일 교체 근거만 줄 때와 원문서에서 레이아웃 보존까지 안내할 때의 링크를 정한다. |
| 174 · 166 | 비지도 Vega·ggrepel 차트의 가려진 입력과 공개 출력. 개별 레이블을 옮기거나 숨기는 근접 규칙과 지도 제작 원전의 경쟁 예측. | 지도 원문을 더해 새 선택·실패 조건이 드러난 행과 가까운 구현 설명만으로 충분한 행을 가른다. |
| 175 · 167 | GeoBIM 및 구조해석 교환 시험의 저자 공개 입력·참여자 제출·원표. 특정 객체/속성의 방향별 값. | 규격이 표현할 수 있는 것, 도구에서 실제 넘어간 것, 원래 도구에 되돌아온 것의 근거를 구별한다. |
| 176 · 168 | JSON-LD expansion·compaction 공개 시험과 구현별 EARL 결과. 같은 시험·옵션의 제출 단언과 구현/실행 계보. | 여러 표시가 한 제출을 옮겼는지, 서로 다른 구현에서 같은 결과가 관측됐는지에 따라 대표 원전과 반례를 고른다. |
| 177 · 146 | MkDocs·mdBook의 HTML·PDF·인쇄·오프라인 요청. 작성자의 논리 조건과 같은 빌드에서의 플러그인 양립. | 단독 링크·양립하는 링크 두 개·요구 확인 한 질문 중 어느 답에 증거가 있는지 정한다. |

169의 값은 **분할 뒤 대상의 신원**, 175는 **같은 파일 안 속성의 방향별 보존**, 176은 **같은 시험을 실제로 수행한 계보**다. 170은 사이트의 조작 시점, 171은 제출자 자신의 입장이다. 173·174는 이미 지정된 자산 또는 원리가 보존하거나 바꾸는 결과를 보고, 177은 들어온 원문 자체가 허용한 대안의 범위를 본다. 각 brief에 고정 선행 SHA, 자료 모집창·담당 경로, 서로 다른 7개 세부 질문, 고유 원자료 22개 하한과 종류, 필수 결과표 3개와 열 이름, 반례와 중간 커밋 순서를 넣었다. 원목록 접근 실패와 실제 음성 결과는 분리하고, 결과가 노출된 입력은 사전 예측 분모에서 제외한다. [배정 JSON](NEXT_TASKS-41.json)

배정 전에 일부 원자료의 진입점도 확인했다. 169의 ISO 등록기관 포털은 직접 열람이 막혔고, IANA의 언어 서식과 IETF 등록 메일 색인은 열렸다. 170에는 Gerrit 관리 화면을 대체할 공식 설정 미러와 운영 로그를 붙였다. 175는 저자의 재출력 파일과 개별 소프트웨어 보고가 별도 레코드로 공개되어 있고, 176은 시험별 표시에서 개별 구현 보고로 들어갈 수 있다. 여기서 확인한 것은 모집을 시작할 주소까지다. 사건별 값·회신·실행 결과의 판정은 각 작업자의 몫이다. [IANA 등록 서식](https://www.iana.org/assignments/lang-subtags-templates) · [설정 미러](https://github.com/wikimedia/operations-mediawiki-config) · [운영 로그](https://sal.toolforge.org/) · [GeoBIM 재출력](https://zenodo.org/records/3964368) · [GeoBIM 제출 보고](https://zenodo.org/records/3964445) · [JSON-LD 구현 보고](https://w3c.github.io/json-ld-api/reports/)

**별도 실행의 선행.** 지금 명시된 정확판의 공개 묶음을 정적으로 읽는 검사는 작게 떼어낼 수 있다. 165의 rqrr 0.9.0/0.9.1은 두 실제 배포 아카이브를 확보한 뒤 포함 파일을 대조할 수 있다. 이 검사로 알 수 있는 것은 포함 목록까지다. 167의 I10은 고정 ZIP·객체 키와 수신 라이브러리 정확판이 갖춰지면 단방향 형상 검사가 가능하다. M05 왕복에는 최초 Finale 판과 원본·편집본 구분이 더 필요하다. 168의 CSS 재생은 브라우저 정확 빌드·동일 OS·폰트 fixture·판독할 실제 값이 선행한다. 174는 노출 전 예측과 고정 뷰포트, 177은 함께 쓰는 플러그인 두 판·같은 입력·기대 출력이 확보돼야 실행을 맡길 수 있다. 이 실행과 반복 검사는 Codex Cloud의 후속 범위다. 과거 개인의 활성 시각, 동의, 경험했던 노동은 당시 당사자 기록이 필요하다. [165 재개 자료][h165] · [167 재개 자료][h167] · [168 재개 자료][h168]

## 판단을 가장 크게 바꿀 불일치 세 건

| 불일치·약점 | 현재 사용자에게 말할 수 있는 범위 | 다음 조사와 판단을 바꿀 관측 |
| --- | --- | --- |
| 편집·배포 시스템의 성공 표시와 하류 대상 또는 당사자에게 일어난 일이 다르다. | 161의 하류 참조에는 별도 undo가 필요했다. 162는 공식 철회와 당사자의 일부 조작을 확인했지만 개인 최초 활성 구간은 비었다. 163은 같은 통지의 내용을 지목한 재개 1건을 확인했다. | 169는 분할 코드가 실제로 바뀐 하류 기록, 170은 같은 위키·조작의 부재와 성공, 171은 정확히 같은 편집 제안에 대한 원제출자의 수락·이의를 찾는다. 이 연결이 없으면 판정 주체를 좁힌다. |
| 같은 이름·파일 수·표시 수가 같은 속성 보존이나 독립 확인을 뜻하는지 알 수 없다. | 165의 정확판 양쪽 목록은 1/8, 167의 원파일·양판·수신값 직접 연결은 0, 168의 동일 술어 원실행은 0/16이다. 각 사건의 고지·입력값·편집 기록 자체는 인용할 수 있다. | 173의 같은 문서에서 대체 전후 줄/문자, 175의 같은 객체·방향의 실제 수신값, 176의 서로 다른 원 단언·구현 계보가 있으면 해당 속성이나 독립 확인까지 문장을 넓힌다. |
| 더 많은 후보나 흥미로운 원리를 주는 것과 선택·총노동이 좋아지는 것 사이에 비교가 없다. | 164의 한 실험에서 두 재사용 방식의 표본 차이 방향은 갈렸고 단위는 미확인이다. 166의 유효 예측 분모는 0, 146에서는 검토 폭을 늘린 이득이 한 요구에 몰렸다. | 172는 같은 인수 수준의 세 경로와 실패를 포함하는 노동 양식을, 174는 원거리/근접 규칙이 실제로 갈리는 미노출 출력을, 177은 ‘택일/동시’ 원문과 같은 빌드의 양립 증거를 남긴다. 집단 효과는 이 설계 이후의 실측이 필요하다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/53eaa286136019510f052179f5f51d901bdac858/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/53eaa286136019510f052179f5f51d901bdac858/docs/RESEARCH_WORKFLOW.md
[r40]: https://github.com/laadkke-arch/agentflow-open/blob/4997e4cb08dcf799bd5e3f0c44a6a17e0d303141/docs/workstreams/planning/REVIEW-40.md
[before]: https://github.com/laadkke-arch/agentflow-open/blob/82c3f5133debf2b8c333ce542750db6b4340ce99/docs/automation/dot-control.json
[control]: https://github.com/laadkke-arch/agentflow-open/blob/53eaa286136019510f052179f5f51d901bdac858/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/82c3f5133debf2b8c333ce542750db6b4340ce99...53eaa286136019510f052179f5f51d901bdac858
[h161]: https://github.com/laadkke-arch/agentflow-open/blob/810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1/docs/workstreams/research/AF-RES-161/HANDOFF.md
[r161]: https://github.com/laadkke-arch/agentflow-open/blob/fb1c5e91209a77554e2e6f6c3e16a6aa59a23917/docs/workstreams/research/AF-RES-161/RESULT.md
[s161]: https://github.com/laadkke-arch/agentflow-open/blob/810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1/docs/workstreams/research/AF-RES-161/sources.jsonl
[trans161]: https://github.com/laadkke-arch/agentflow-open/blob/810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1/docs/workstreams/research/AF-RES-161/transactions.csv
[fields161]: https://github.com/laadkke-arch/agentflow-open/blob/810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1/docs/workstreams/research/AF-RES-161/fields.csv
[h162]: https://github.com/laadkke-arch/agentflow-open/blob/de55ea13566bc88f497dec2bfa4b0752406aea06/docs/workstreams/research/AF-RES-162/HANDOFF.md
[r162]: https://github.com/laadkke-arch/agentflow-open/blob/7229b7170b0239afcdd7e2624eb4bd8b1fad5140/docs/workstreams/research/AF-RES-162/RESULT.md
[s162]: https://github.com/laadkke-arch/agentflow-open/blob/de55ea13566bc88f497dec2bfa4b0752406aea06/docs/workstreams/research/AF-RES-162/sources.jsonl
[ad162]: https://github.com/laadkke-arch/agentflow-open/blob/de55ea13566bc88f497dec2bfa4b0752406aea06/docs/workstreams/research/AF-RES-162/advice.csv
[obs162]: https://github.com/laadkke-arch/agentflow-open/blob/de55ea13566bc88f497dec2bfa4b0752406aea06/docs/workstreams/research/AF-RES-162/observations.csv
[h163]: https://github.com/laadkke-arch/agentflow-open/blob/360d971487259cb22496406fd3ef71e0654340c1/docs/workstreams/research/AF-RES-163/HANDOFF.md
[r163]: https://github.com/laadkke-arch/agentflow-open/blob/48fc58551204344983d34ab54648765f47c9ce57/docs/workstreams/research/AF-RES-163/RESULT.md
[s163]: https://github.com/laadkke-arch/agentflow-open/blob/360d971487259cb22496406fd3ef71e0654340c1/docs/workstreams/research/AF-RES-163/sources.jsonl
[nt163]: https://github.com/laadkke-arch/agentflow-open/blob/360d971487259cb22496406fd3ef71e0654340c1/docs/workstreams/research/AF-RES-163/notifications.csv
[joins163]: https://github.com/laadkke-arch/agentflow-open/blob/360d971487259cb22496406fd3ef71e0654340c1/docs/workstreams/research/AF-RES-163/joins.csv
[h164]: https://github.com/laadkke-arch/agentflow-open/blob/df07150fcb13ab153e6472490787f3f970173a35/docs/workstreams/research/AF-RES-164/HANDOFF.md
[r164]: https://github.com/laadkke-arch/agentflow-open/blob/e7908cc08278e815fc4bf7b57d41c58f4cf571cc/docs/workstreams/research/AF-RES-164/RESULT.md
[s164]: https://github.com/laadkke-arch/agentflow-open/blob/df07150fcb13ab153e6472490787f3f970173a35/docs/workstreams/research/AF-RES-164/sources.jsonl
[raw164]: https://github.com/laadkke-arch/agentflow-open/blob/df07150fcb13ab153e6472490787f3f970173a35/docs/workstreams/research/AF-RES-164/lattanzi-raw.csv
[contrast164]: https://github.com/laadkke-arch/agentflow-open/blob/df07150fcb13ab153e6472490787f3f970173a35/docs/workstreams/research/AF-RES-164/contrasts.csv
[h165]: https://github.com/laadkke-arch/agentflow-open/blob/2c9e6495c19079006eb5612a3ee76a09d5c5f1da/docs/workstreams/research/AF-RES-165/HANDOFF.md
[r165]: https://github.com/laadkke-arch/agentflow-open/blob/488fd6819154748ad37d70e64ccdc0f24b345ccb/docs/workstreams/research/AF-RES-165/RESULT.md
[s165]: https://github.com/laadkke-arch/agentflow-open/blob/2c9e6495c19079006eb5612a3ee76a09d5c5f1da/docs/workstreams/research/AF-RES-165/sources.jsonl
[assets165]: https://github.com/laadkke-arch/agentflow-open/blob/2c9e6495c19079006eb5612a3ee76a09d5c5f1da/docs/workstreams/research/AF-RES-165/assets.csv
[dec165]: https://github.com/laadkke-arch/agentflow-open/blob/2c9e6495c19079006eb5612a3ee76a09d5c5f1da/docs/workstreams/research/AF-RES-165/decisions.csv
[h166]: https://github.com/laadkke-arch/agentflow-open/blob/8fc8b7706840b670aa258f5f8e32c2a6864c0370/docs/workstreams/research/AF-RES-166/HANDOFF.md
[r166]: https://github.com/laadkke-arch/agentflow-open/blob/f6063d40306435e09f2c7df277692b69db6cc2d3/docs/workstreams/research/AF-RES-166/RESULT.md
[s166]: https://github.com/laadkke-arch/agentflow-open/blob/8fc8b7706840b670aa258f5f8e32c2a6864c0370/docs/workstreams/research/AF-RES-166/sources.jsonl
[pred166]: https://github.com/laadkke-arch/agentflow-open/blob/8fc8b7706840b670aa258f5f8e32c2a6864c0370/docs/workstreams/research/AF-RES-166/predictions.csv
[out166]: https://github.com/laadkke-arch/agentflow-open/blob/8fc8b7706840b670aa258f5f8e32c2a6864c0370/docs/workstreams/research/AF-RES-166/outcomes.csv
[h167]: https://github.com/laadkke-arch/agentflow-open/blob/0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7/docs/workstreams/research/AF-RES-167/HANDOFF.md
[r167]: https://github.com/laadkke-arch/agentflow-open/blob/9f1c3ccda5a4afe75da47645fca8746d352e5c8e/docs/workstreams/research/AF-RES-167/RESULT.md
[s167]: https://github.com/laadkke-arch/agentflow-open/blob/0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7/docs/workstreams/research/AF-RES-167/sources.jsonl
[ex167]: https://github.com/laadkke-arch/agentflow-open/blob/0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7/docs/workstreams/research/AF-RES-167/exchanges.csv
[prop167]: https://github.com/laadkke-arch/agentflow-open/blob/0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7/docs/workstreams/research/AF-RES-167/properties.csv
[links167]: https://github.com/laadkke-arch/agentflow-open/blob/0d7917cc6ba0a2a0d161a3f45a1d9763030a90e7/docs/workstreams/research/AF-RES-167/links.csv
[h168]: https://github.com/laadkke-arch/agentflow-open/blob/5e1010c6698ea43c80e27ca4b73fdb98ee4f2168/docs/workstreams/research/AF-RES-168/HANDOFF.md
[r168]: https://github.com/laadkke-arch/agentflow-open/blob/15e99f8b2fc9057556327bb4f8649efda8c9c521/docs/workstreams/research/AF-RES-168/RESULT.md
[s168]: https://github.com/laadkke-arch/agentflow-open/blob/5e1010c6698ea43c80e27ca4b73fdb98ee4f2168/docs/workstreams/research/AF-RES-168/sources.jsonl
[claims168]: https://github.com/laadkke-arch/agentflow-open/blob/5e1010c6698ea43c80e27ca4b73fdb98ee4f2168/docs/workstreams/research/AF-RES-168/claims.csv
[prov168]: https://github.com/laadkke-arch/agentflow-open/blob/5e1010c6698ea43c80e27ca4b73fdb98ee4f2168/docs/workstreams/research/AF-RES-168/provenance.csv
[obs168]: https://github.com/laadkke-arch/agentflow-open/blob/5e1010c6698ea43c80e27ca4b73fdb98ee4f2168/docs/workstreams/research/AF-RES-168/observations.csv
