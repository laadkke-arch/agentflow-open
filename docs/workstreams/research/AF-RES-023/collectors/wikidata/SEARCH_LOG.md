# Wikidata 탐색·열람 경로

2026-11-22 조사, 원장 작성 시각 03:16:48 UTC까지. root 직접 조사; 세부 호출 순서는 세션 도구 기록에 있다.

- web system1: `site.wikidata.org "unmerge" "Q" "merged"`, `site.wikidata.org "incorrectly merged" "restored"`.
- Help:Merge/Split/Redirects 원문 개봉 후 Phabricator T237262로 이동. 정책의 가상 예를 사건으로 세지 않음.
- T237262가 연결한 원 merge1038289881, undo1048159568, consumer rewrite1039041773, consumer undo1048159950 모두 diff/고정판에서 열림. 한 사건 WD01이다. 소비자 수정은 다른 항목 Q314104이지만 같은계보임.
- BankID Q116980761·Q116980735 history, mantra yoga Q16575483 history는 web tool accessible 오류. 2024/04·2021/11 Project chat의 진술은 읽었으나 전후판 사건수에서 제외.
- Q55296215 현재페이지, Q59165607 oldid986442520 단독판, Q314104 oldid936463156 단독판, explicit diff1048159950 URL은 web tool inaccessible. 같은 원자료의 공개 diff가 전후값을 보여 주므로 그 범위만 사용. 직접 열린 `diff=next&oldid=1039041773&title=Q314104`는 결과1048159950이고 그 oldid 고정판도 별도 열림.
- T237899는 성공 merge 뒤 Commons consumer 잔존을 보고하나 해당 원merge revision 미확보. supplement로 보존하며 본표본/consumer분모에서 제외.
- 반증: undo만으로 consumer가 자동복구된다는 가설은 WD01의 별도undo로 반증. 모든분리를 막아야 한다는 가설을 검토하려 portrait 중복 merge 사건을 열었으나 전후원판 부족이라 표본수로 쓰지 않음. 현행 editgroups 개선 때문에 2019의 불편을 2026의 전역능력으로 소급/일반화하지 않음.
- 최초 shell Wikidata403; web가 직접읽은 diff는 정상 지원경로다. HTTP 상태와 문서본문 열람성은 별개 기록.
