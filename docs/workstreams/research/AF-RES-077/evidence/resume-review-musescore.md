# 재개 후 MuseScore·TEI 검토

검토자: `/root/review_musescore`, 같은 모델 계열의 사후 재판독 문맥. 기준 결과판: `2f7e07542b4a59839556e00c9e266179150b21a3`. 기록 시각: 2026-11-23 12:33:49 UTC. 기존 A/B 입력·선택·모집·시험 원장은 수정하지 않았다. 이 검토는 새 눈가림 판독, 독립 효과 표본, 목표 실행이 아니다.

## 결론과 필수 정정

기존 핵심 판정은 유지된다. MuseScore 주 모집 자리는 공석이고, MS-N/E/X의 목표 프로그램 실행은 0/3이다. TEI는 증거본 식별과 적용 범위를 설명하며, 명령의 역연산이나 잃어버린 음높이의 복원을 제공하지 않는다. A/B는 모두 새 파트의 생성 경계에서 선택 flag를 지우는 안을 골랐고, 실제 병합은 모든 Element 복사를 대상으로 하는 다른 범위였다.

다만 **원 tracker를 전혀 읽지 못했다는 현재형 문구는 정정해야 한다.** 이번 [공식 tracker #281441](https://musescore.org/en/node/281441) web open에서 검색 서비스가 보관한 본문을 반환했다. 해당 응답은 crawl을 `1.3 years ago`라고 표시했다. 후속 줄 단위 재요청 2회는 HTTP 403이었다. 따라서 실시간 원 서버 재취득 성공이나 최초판 전체 확보라고 쓰지 않는다.

반환된 공식 페이지의 저자 표시는 **ericfontainejazz**, 작성 표시 시각은 **2019-01-08 19:55**이다. 페이지가 표시한 시각의 시간대는 확인되지 않았다. `Reported version`은 **3.0**이며 본문은 **3.0 release 및 2.3.2**에서도 발생한다고 보고한다. 원 동작은 새 score를 만들고 notes를 선택한 뒤 parts를 생성하면 파트의 notes가 실제 Selection에 없으면서 파랗게 남는 것이다. 본문은 선택했다가 해제하면 표시가 사라진다고 설명한다. 이미지 2개의 링크가 있지만 이미지 바이트를 열거나 실행을 재현하지 않았다. 문서 하단 첫 이력은 2019-01-16 04:45의 제목 변경을 드러냈다. 그 뒤 전체 이력은 이번 재요청 실패로 읽지 못했다. 현재 본문과 최초 게시 본문의 동일성은 미확인이다.

이 자료가 알려 주는 날짜는 [PR #4590](https://github.com/musescore/MuseScore/pull/4590)의 2019-01-16 생성보다 이르다. 따라서 고정 소스 **v3.0.1 `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`**는 **PR 전날의 맥락판**이라고 쓸 수 있지만, **원 요구 이전판**이라고 쓸 수 없다. 원 보고의 3.0/2.3.2와 이 고정판의 동등성도 입증되지 않았다. 봉인판은 그대로 두고 사후 정정으로 연결해야 한다. 이 새 열람에도 undo·reopen·범위 밖 성부/파트 보존이라는 작성자 요구는 없다. 주 표본을 채울 수 없으며, 모집을 소급 변경하지 않는다.

## 원문과 고정 소스의 대조

| 항목 | 이번 확인 | 한계 |
|---|---|---|
| 최초 10건 | 저장된 canonical 두 검색 응답에서 number로 합치고 `(created_at, number)`로 정렬해 `4525,4529,4534,4535,4541,4542,4553,4565,4570,4590`을 재계산했다. 기존 FRAME와 일치한다. | 검색을 재모집하지 않았다. 현재 GitHub 검색 결과 전체의 완전성을 새로 검증한 것은 아니다. |
| 요구 주체 | PR 현재 본문은 ericfont의 복제된 선택 표시 문제를 지지한다. 이번 tracker 캐시는 ericfontainejazz의 보고를 확인한다. | 서로 다른 서비스의 두 handle을 별도 신원 확인 없이 동일 계정이라고 단정하지 않는다. CONTRIBUTOR 표시는 유지보수자 요구를 뜻하지 않는다. |
| 대상판 | [v3.0.1 tag API](https://api.github.com/repos/musescore/MuseScore/git/ref/tags/v3.0.1)를 재열람해 위 commit SHA를 확인했다. | 원 reporter의 정확한 실행 바이너리가 아니다. |
| 시행 지점 | [고정 element.cpp](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/element.cpp)의 `Element::Element(const Element&)`는 `_flags`를 그대로 복사한다. `linkedClone()`은 별도 Link 명령을 등록한다. | source inspection은 GUI 결과가 아니다. |
| 실제 채택 | [PR changed files](https://api.github.com/repos/musescore/MuseScore/pulls/4590/files)는 element.cpp의 SELECTED 제거 한 줄, 시험 변경 0개를 반환한다. PR 재열람은 merge SHA `16851045c9e50eafb016c5cf4f2733f974e841bf`, 2019-03-07T09:53:22Z를 확인한다. | 채택 사실은 보존 조건 전부의 성공 또는 A/B 노출의 효과가 아니다. |
| 판독 봉인 | MS common/A/B packet과 두 reader JSON의 SHA-256이 VIEWS의 값과 일치한다. 원문 문자수는 A949/B1571, common5319이다. | 최대 2,000자 예산은 같지만 실제 노출량은 다르다. B packet은 2,438 Unicode 문자/2,444 UTF-8 bytes이므로 서로 다른 단위를 혼동하지 않는다. |

## TEI 전이와 동종 대조

[TEI P5 4.8.0](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html)은 2024-09-02 revision `4e6e41b0b`라는 헤더를 반환했다. [제공된 live URL](https://tei-c.org/release/doc/tei-p5-doc/en/html/TC.html)은 4.12.0, 2026-07-28 revision `113e933e2`이다. 이를 2019년 개발자가 받은 자료라고 해석할 수 없다.

실제 절은 **13.1.2 Readings `#TCAPLR`**, **13.1.4.3 The Witness List `#TCAPWL`**이다. SOURCES의 13.1.4.3을 단순히 Witness Information이라 부르는 것은 상위절 13.1.4의 제목과 섞인 작은 표기 오류다. 최종 결과에서는 정확한 하위절 제목을 쓴다. witness 식별자, reading의 증거본 귀속, 해당 위치에서 비활성인 증거본을 제외해야 하는 조건을 확인했다. 이 모델을 selection·음악 link·track 범위의 구분에 참고할 수 있지만, 특정 C++ 변경 위치와 undo 기록은 연구자 추론 및 이미 주어진 대상 코드에서 나온다. 원전은 전역 copy reset과 국소 excerpt reset의 우열을 결정하지 않는다.

[MuseScore 3 Handbook](https://musescore.org/en/print/book/export/html/278625)의 Parts Overview·Save Parts와 Undo and redo를 재열람했다. 음악 데이터 공유, 파트별 표시 설정, score 안의 저장 및 undo 기능 설명은 기존 A의 근거 범위와 일치한다. 이 live handbook에는 3.6.2 등의 후대 내용이 섞여 있어 고정 3.0.1의 역사적 설명으로 환산할 수 없다. 같은 분야 문서만으로도 공유 음악 내용과 표시 범위를 구별할 수 있으므로 TEI만의 새로운 핵심 선택이 있었다는 주장은 지지되지 않는다.

## 실제 파일과 오판 조건

원 고정판의 `tst_parts.cpp`, `tst_links.cpp` 등의 source 및 저장된 `.mscx`를 읽었다. 재계산에서 `part-breath-uadd.mscx`는 `part-empty-parts.mscx`와 byte-identical이고, add reference의 Breath는 2개, 입력/undo reference는 0개였다. 세 파일에 `selected`나 `undo` 태그는 없었다. 이것은 **기대 출력 파일 간 관계**이며, 실제 프로그램 출력이 아니다. `saveCompareScore`의 전체 score 비교도 undo 구현이 전체 snapshot을 쓴다는 뜻이 아니다.

MS-E는 생성 직후의 clone selected flag와 파트 Selection 목록을 반드시 함께 관찰해야 한다. 마지막 reopen만 보면 transient flag가 사라져 구현 차이가 지워질 수 있다. 추가로 `Element::curColor`는 selected **또는 Note::mark()**에 따라 선택색을 돌려주며 printing/drop-target 경로도 있다. 따라서 색상만으로 selected=true라고 판정하면 오판 가능하다. harness는 mark/drop-target/printing 상태를 통제하고 실제 flag·목록·색을 각각 기록해야 한다. 이는 새 시험 성공이 아니라 후속 관찰 규약이다.

MS-N/E에는 P2의 중간 독립 변경이나 오래된 snapshot이 없으므로 whole-state와 scoped undo는 모두 같은 결과를 낼 수 있다. MS-X는 기록이 없는 과거값을 만들어내지 않는지의 음성대조로 적절하지만 두 정당한 구현을 가르지 않는다. 기존 빈 stack guard와 새 MasterScore 로딩 source는 이 한계를 지지한다. 목표 실행·원시험 실행·후보 구현은 이번에도 0이다.

## 다음 첫 행동과 실행 인계

현재 가능한 첫 행동은 원 tracker의 확보된 캐시 범위와 새 시간순서를 E5 및 최종 Q1/Q7에 반영하는 것이다. 이후 실제 목표 실행을 하려면 기존 `postseal/musescore/RUNBOOK.md`의 환경을 준비하고, 위 SHA checkout에서 MS-E의 생성 직후 관찰을 갖춘 구체적 score/harness를 먼저 작성해야 한다. 원시험 재실행 명령은 준비된 build의 `build.debug/mtest`에서 다음과 같다.

```bash
QT_QPA_PLATFORM=vnc xvfb-run -a ctest -j2 --output-on-failure \
  -R '^(tst_parts|tst_links|tst_exchangevoices|tst_readwriteundoreset|tst_element)$'
```

이는 원시험 명령이며 아직 존재하지 않는 MS-N/E/X harness의 실행 명령이 아니다. 현재 source copies는 완전한 build checkout이 아니다. 출력 XML·stdout/stderr·종료코드를 확보하기 전 성공을 부여하지 않는다.

## 검토 비용·독립성

외부 read 대상 호출은 **16회**다: web open/find 12회와 GitHub read 4회. 원문 또는 메타데이터를 받은 요청 12회, 검색어 불일치 find 2회, tracker 후속 HTTP403 2회다. 고유 URL은 8개다. HTTP 내부 재시도 횟수·원시 다운로드 bytes·토큰·정확한 per-call UTC는 관측하지 못했다. 기록 UTC는 위이며 모든 읽기는 같은 UTC 일자였다. 새 계보 산입은 0이며 tracker/PR은 같은 MS-REQUEST-4590 계보로 묶는 것이 보수적이다. 이 검토의 원문 재열람은 봉인 A/B 노출이나 비용에 추가하지 않고 재개 후 검토 비용으로만 센다. 상세 source records와 요청별 목록은 동명 JSON에 있다.
