# Yjs 모집 검토

모든 첫 30개 복원 본문을 직접 읽었다. query-word 결과27개를 모집틀로 쓰지 않았다. 본문 전에 performed title-only audit의381개 기간 issue 중 첫300개 metadata로 substring 첫30개가 확정됐다. 처음 token검색에서 빠진16개가 `title-audit.json`에 있다. PR과 cutoff 밖은 제외했다.

첫 적격 두 자리는 **#157→YN1, #204→YN2**다. #156은 구체 보존내용이 없고 두 그룹화 시도의 실패도 이미 노출했다. #162와#165는 실패 출력만이 아니라 소스 수정 후 작동/통과 진술도 본문에 있어 두조작 답 노출로 제외했다. 본문에 baseline 결과가 있다는 이유만으로 모든 bug를 제외한 것은 아니다. #204는 복사 후123 보존 목표와 사건열이 명시돼 있고, 선정 A/B의gc설정 차이는 본문에 답이 없다. 다만 본문 기대값과 삭제/추가 대조를 이미 읽었으므로 새 exact-text적중의 근거로 쓸 수 없다.

#157의 `this text can not be undone`은 원문 정확 보호 문자열이다. 초기문서와 앞뒤 ordinary edit는 원문에 없다. 원문에서 제안한startSkipping/stopSkipping을 현재제품의 실제 API로 바꾸어 부르지 않는다. 당시 코드를 확인하여 사용가능한origin집합차이로 별도연구입력을 만든다. 당시정식판12.3.3과 contemporaneous prerelease13.0.0-94는 분리한다.

#204의원문은 `// expect ~"Hello 123 World"`라는 근사기대다. 삽입앞공백을연구자가정정해원래정답으로만들지않는다. primitive문자열,새123보존,삭제한Hello복원,redo범위를각각확인한다.

자연층은 API에서현재복원가능한body를읽은것이지,2019/2020년최초bodyrevision을복원한것이아니다. 공개이슈에2024년붙은migration footer는관련없고저장/추적하지않았다. 원bodyhash만남겼다.

진단층초기기계후보testUndoText는push변경을못센heuristic결함이었다. root교차검토에서결과를열기전에수정하여2push+undo의**testInfiniteCaptureTimeout**을선택했다. 원시험에redo는없으므로추가redo는연구자변형이다. 이전후보의input전체를읽은노출은그대로보존한다.
