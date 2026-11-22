# Jupyter 표집과 앞선 판 추적

원장39 PR metadata를 최초날짜순으로 보았다. #65부분,#66전체,#70부분의 실제앞선fork판,#87전체를 선택한다. #72와#79는 첫 공개 설계가 원PR보다 앞서며 수정가능원글의 최초판을 고정하지 못해 보류했다. 후보검색 결과나 성공 여부는 표집에 쓰지 않았다.

- #70: #68 2021-04-22의 full draft 링크→jflam fork path history→6966750. 원blob51a12f2가6월PR의blob과 동일. date-started2021-02-10은 작성일진술로만 보존.
- #72: #67 2021-01-25 preproposal과 같은2021 설계의 확대. 2018 #26은 Monaco editor에 결합된 별도초안이라는 최초본문 진술. #67의 변경되지 않은 최초body를 확인할 방법을 공개API에서 확보하지 못해 보류.
- #79: 초기Git본문이 notebook6210 comment957169113을 원안으로 지정. comment metadata created2021-11-02/updated2022-04-27 불일치. 본문은 열지 않고 초기revision미복구로 보류.
- #87: 최초PR commit6322120의 전체문서를 사용. 본문에는 앞선동일제안 링크 없음. GitHub의 잔존첫commit 외 유실초안유무는 일반한계다.

API첫커밋의author date와PR생성시각은 별도보존했다. 이미지/GIF는설계텍스트의링크그대로남겼고필수조건근거로추가판독하지않았다. 초기네문서의본문에는기지제품/대안이있으므로questions.jsonl의known_names를잠근다.

## 접근기록

첫 raw.githubusercontent.com 네문서병렬요청은HTTP429로실패했고본문0개. 동일고정파일을GitHub연결도구의공개파일읽기로열었다. LICENSE.md404뒤Git tree에서LICENSE경로확인후동일고정판을읽어BSD3조건을inputs/LICENSE-JUPYTER에보존했다. 원문최소수에는차단·license·metadata를넣지않는다.

## 현재 상태

4원질문과8경로질의를작성했고후보검색은아직0회다. root의원격봉인커밋확인후에만검색한다.
