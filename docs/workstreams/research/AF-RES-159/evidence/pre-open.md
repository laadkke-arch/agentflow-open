# 소스와 사전 봉인

2026-11-24 17:04:34 UTC. 한국어·독일어 PO의 이름은 확인했고 내용·번역 상태·MO는 아직 읽지 않았다. 목표 호출의 기능을 소스에서 알아낸 한 사람이 후보들을 판정했다. 패킷을 처음 보는 독립 독자의 응답이나 필요한 질문 수를 관측한 설계는 아니다.

| 판 | 원문 모집 입력 | 관측 |
|---|---|---|
| GIMP 3.0.6 | [태그 미러](https://github.com/GNOME/gimp/tree/GIMP_3_0_6), [소스 버전](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/meson.build#L1-L8), [도메인 목록](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/po/POTFILES.in) | Git 태그의 주 UI 도메인. 670개 기재, 669 파일(중복 1), C/C++ 636·Glade 31(메뉴 원템플릿 2 포함)·AppData 1·Desktop 1. 비어 있지 않은 단수 msgid 5,631, 명시적 멀티 92, 단일 2,115, plural 38. xgettext의 단수·복수 혼용 경고는 로그에 둔다. |
| Inkscape 1.4.3 | [발행 태그](https://gitlab.com/inkscape/inkscape/-/tags/INKSCAPE_1_4_3), [gitlink (type commit)](https://gitlab.com/api/v4/projects/inkscape%2Finkscape/repository/tree?ref=0d15f7504220b00925bc3cb3673fcf44610a17d5&per_page=100), [번역 커밋의 원문 POT](https://gitlab.com/inkscape/translations/-/blob/dd0592f12a5da07802a96b53293bbe12acdf45ff/inkscape.pot) | Debian의 orig tar에서 읽은 POT는 2025-12-23 생성. 번역 저장소의 정확한 gitlink에서 받은 POT와 바이트 일치. tar root 버전은 2025-12-25/0d15f75042. 단수 msgid 10,741, 명시적 멀티 15, 단일 923, plural 38. 발행 소스의 직접 C++ 및 Glade 재추출 대조에서는 발행 POT과 합칠 때 새 멀티 그룹이 생기는 명시적 키를 찾지 못했다. 생성 파일과 확장 리소스의 전체 POT 재빌드는 별도다. |

[모집창](../frame.csv)은 제품별 앞 12와 단일 대조 2, 총 28그룹이다. 앞 6그룹이 모두 두 고정 키를 실제 소비로 이을 수 있어 7–12번은 선택 순서 밖이다. 해당 뒤 12그룹을 실제 바인딩 결측으로 세지 않는다. [전체 멀티 인벤토리와 복수 제외](source-frame.jsonl), [추출 명령 영수증](extraction.json), [호출 원본 판독](call-notes.tsv)을 보존한다. GIMP enum의 생성된 .c를 실행에 소비되는 등록 데이터로 확인했다. 예를 들어 [일반 enum 조회](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/libgimpbase/gimputils.c#L846-L866)에서 문맥으로 조회되며, 렌더링이나 UI 연결이 없는 generated-only 행의 취급과 다르다.

[호출 원장](../calls.csv) 28개에서 후보 함수·등록·분기까지 연결했다. [패킷](../packets.jsonl)과 [판정](../predictions.csv)은 자연 24호출과 대조 4호출 × 2언어 × 5보기로 280줄이다. A/C의 전체 후보 중에 아직 각 기능까지 판독하지 않은 다른 키·기본 키의 원문 참조를 남겼다. I03b는 같은 액션의 툴바·명령·Undo 표현이므로 기능 링크는 핸들러 하나에 모았다. I02a의 같은 키 두 컨트롤과 G06b의 공용 enum에 연결된 두 콤보는 의미가 달라 후보를 유지했다.

B/C는 순수 UTF-8 참조값과 JSON 전달량을 각각 잰다. C 출처 위치는 원장 메타데이터에 있고 입력 payload에는 문자열만 들어 있다. C 하나가 먼 파일에 걸린 B의 위치를 간접 노출하지 않게 C는 자료가 선택된 원문 파일에 속한다. 값은 해당 줄 일부를 발췌할 수 있으므로 시작·끝 바이트를 기록했다. C 역검색으로 같은 파일을 찾아 한 갈래가 우연히 맞아도 소비 관계 확인으로 취급하지 않는 대조를 ④에서 한다. 공유 UI의 다른 속성·다른 도구가 값으로 등장할 수 있다. 선화 감지 옵션 주변 C를 다른 기능과 완전히 독립이라고 볼 수 없는 경우는 민감도로 따로 밝힌다.

[절차](../SCOPE.md)의 도구는 gettext 0.23.1, Python 3.12.14다. GIMP 원문 사이트의 tar 바이트 전송과 Inkscape 공식 다운로드 호스트는 이 환경에서 차단돼 GIMP 발행 태그 미러, Inkscape의 Debian orig tar와 GitLab 고정 커밋을 썼다. 태그·tar·번역의 해시와 배포 MO의 성격은 별도 검산한다.
