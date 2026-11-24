# 저장 레코드와 보기 규칙

E05는 원글의 clipboard JSON 하나만 확보됐다. 요소 버전 59는 개별 레코드의 변경 횟수이며 실행판이 아니다. 붙여 넣을 사각형의 ID와 빈 `boundElements`·`groupIds`는 저장값이다. 사용자가 원글의 재현 절차로 선택한 것은 사각형과 입력할 새 텍스트다. 새 텍스트의 ID와 선택 상태를 재구성할 수 없다. 파서가 보는 단일 사각형을 편집의 대상이라고 등치시키면 사각형 크기 변경 문서를 잘못 추천할 수 있다. [원글 E05](https://github.com/excalidraw/excalidraw/issues/4563) · [타입 v0.11.0](https://github.com/excalidraw/excalidraw/blob/0896892f8ad03f42d1bd8312fe6bd938f6a3f8aa/src/element/types.ts#L39-L153)

M60은 원글의 master 링크를 공식 파일 이력으로 추적한 보조 자연 관측이다. 선행 blob `861bbc6bd3bf…`와 동 작성자의 후속 blob `0f73aa3f94d1…`을 모두 읽었다. 원글의 옛 문자열이 선행 파일에 있고 후속 패치가 그 위치를 바꾼다. release 세 판의 바이트는 후속과 같았다. 원글 작성자가 링크한 자료와 작성자가 직접 업로드한 표본을 분리한다. 앞순번 미확보 후보가 있으므로 M60을 세 본표본에 끼워 넣지 않았다. [파일 이력](https://github.com/musescore/MuseScore/commits/v4.0/src/engraving/tests/repeat_data/repeat14.mscx) · [선행 파일](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/repeat_data/repeat14.mscx#L1490-L1504) · [후속](https://github.com/musescore/MuseScore/commit/30b5aa7b0a9dfd60197fed191304f9f03f59bed7)

## 공통 절단과 재판독

A의 본문 사용 구간은 opening Markdown의 정확한 반열린 문자 위치로 입력에 있다. 작성자가 서술에 붙인 수치·범위 기호도 A에 있다. E05의 기계 직렬화 블록은 작성자 제공 첨부로 분리한다. 강조 태그가 필요한 원문은 opening SHA로 다시 읽을 수 있다.

장면 배열·XML 문서 순서대로 정규화한 레코드에는 원 경로와 저장 필드값을 유지한다. XML occurrence 경로와 MSCX `Jump`의 label→marker 조인은 파서 해석이다. 선택이나 영향력이 추가되는 관계로 처리하지 않는다. 포함된 하위 요소·마디의 표시 번호·장면의 z-order는 참조 필드와 구분한다. Excalidraw는 명시직접/역방향 요소 참조, MSCX는 실제 staff ID 및 명시 jump label, MusicXML은 해당 IDREF만 C 이웃으로 사용한다. 그룹 ID는 레코드의 값으로 남는다. [정규화·보기 코드](tools/structure.py)

두 보기 모두 모든 시작 후보를 같은 순서로 앞에 둔다. 시작 후보를 다 싣지 못하면 평가에서 보류한다. B는 가장 가까운 시작점과 순번 차이가 작은 것부터, C는 직접 참조/역참조 후보를 고른 뒤 원 순번 순서로 둔다. 동률 규칙은 시작 후보 우선과 원 순번이다. A와 한 줄 구분자를 포함한 실제 UTF-8 텍스트의 Unicode 문자 수를 제한하고 네째 레코드 뒤를 자른다. JSON 줄이 중간에서 잘리면 그 줄 전체를 새 근거로 삼지 않는다. 원 순번·원 경로·보인 문자의 좌표·완결 여부·교집합을 원장에 남긴다. B/C 재절단은 기본 두 보기의 짧은쪽 실제 문자열 길이를 상한으로 한다.

업로더가 기록한 값, 명시 선택, 원문에서 연구자가 부여한 시작 힌트, 앱이나 파서가 재구성한 연결을 다른 필드에 남긴다. 비교기에는 보인 본문과 레코드를 옮긴 봉투와 같은 후보 절만 복사한다. 입력의 전체 byte, gold, 보이지 않은 레코드의 필드는 그 봉투에서 제외한다.
