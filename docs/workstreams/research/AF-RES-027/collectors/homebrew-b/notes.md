# B Homebrew 체크포인트

세 원장은 A 봉인 이후 열었다. B-H01=pkg-config, B-H02=python, B-H03=qt. A-H02·A-H06과 중복 연결이며 A 분자·분모를 늘리지 않는다.

마지막 직접 확인: BH-S14. B-H01과 B-H03은 A-H02/A-H06의 소비자 사슬을 연결한다. B-H02는 Borg의 2019 문서, 2020·2021 실제 변경 diff, 2021-07-03 고정판을 직접 읽었다. Python 참조는 유지됐고 다른 설치 기능의 수정만 발견했다. 각 공식 배포시점은 미확인이다. 현재 B 자료에서 공급자 시행→소비자 정정 지연을 계산하지 않는다.

Q3 보조 반례: Qt alias만 바뀌었을 때 같은 Qt5 산출물을 유지했다. 이후 Qt6 전환과 별도 사건이다. Python의 source author date와 committer date 차이는 약51일이며 어느 쪽도 단독으로 사용자 배포시각을 뜻하지 않는다.

B-H02의 'Homebrew 안내 수정'은 선정한 Python 참조의 정정이 아니었다. Borg cask/formula·FUSE 기능의 차이를 Python 수정 성공으로 넘겨 세지 않는다. 과거 Python>=3.5와 나중 >=3.6 요구에는3.8이 문서상 맞지만 실제 같은 판의 설치/테스트 성공은 미확인이다. 배포시점 미확인인 행을365일 우측검열로 위장하지 않았다.

Homebrew PR54912는 merged_at=null이면서 실제 공개 sourcecommit·merge-trigger comment가 존재했다. 한 API 필드만으로 사건 미발생이라 할 수 없다. 반대로 남아 있지 않은 Actions run(404)을 성공이라 메울 수도 없다. BH-Q05에 후속 첫 자료를 적었다.

Q8: 당시 Homebrew는 설치에 쓴 alias와 조회한 formula명을 따로 보존했다(BH-S06/BH-S11). 같은 현재 주소/recipe로 연결돼도 설치 receipt의 이름에 따라 향후 upgrade가 달라질 수 있어, 이 질문에는 참조 문자열·설치 경로·판 정보가 더 필요하다.
