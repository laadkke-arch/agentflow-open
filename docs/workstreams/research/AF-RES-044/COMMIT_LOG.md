# AF-RES-044 원격 커밋 기록

| 묶음 | 원격 SHA | 범위 | 원격 확인 |
| --- | --- | --- | --- |
| ① | 0832f18bcb040871fa300db708a67d6f7f8866c7 | manifest, SCOPE v1, pilot-exposure | GitHub update_ref + git fetch |

로컬 git push는 HTTPS credential 부재로 실패했다. 인증된 GitHub 연결의 tree/commit/update_ref로 동일 파일을 저장했다. 로컬 선행 커밋 b3ed7b40d95df7a1b472e850371f5e71b996a221과 원격 커밋은 작성 metadata만 다르며 내용 tree가 같다. 이후 체크아웃을 원격 SHA에 soft align했다. 강제 push·권한 변경은 하지 않았다.
