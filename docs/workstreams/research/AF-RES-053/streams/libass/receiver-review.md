# libass 수신 문헌 검토 · 예측 봉인 전

## 1. 고정 조작과 연구 기준판

단계① 원격 `a6b1624c899eacf118c0e01350f52cbd53e21dae`의 `operations.json`을 먼저 읽었다. 아래 조사는 그 A/B를 유지한다. 댓글·연결 PR·선정 이슈의 후속 release 본문·시험 결과·후속 그림은 열지 않았다. 이 문서는 수신 문헌에 무엇이 있는지를 보고하며 N/I/D 최종 예측은 root가 정한다.

| 요구 | 연구 기준판 | 직접 확인한 판 증거 | 해석 제한 |
| --- | --- | --- | --- |
| L01 #588 | libass 0.15.2, commit `c967a5a3d9ec0d36af1148b3fdf2f307a21dd122` | release metadata 발행 2021-09-12; tag의 공개 header | #588의 실제 libass 판은 미명시. 최신 선행 release를 실제 실행판으로 치환하지 않는다. |
| L02 #685 | libass 0.17.1, commit `e8ad72accd3a84268275a9385beb701c9284e5b3` | release metadata 발행 2023-02-26; tag의 공개 header | 본문은 VLC 3.0.18만 명시. 그 배포본에 포함된 libass commit은 미확인이다. |

같은 분야의 추가 문헌은 Aegisub 공식 3.2 manual을 쓴다. 공식 `Aegisub/aegisite`의 2021-01-16 snapshot `8dfbd70f89940bf8e327dac80c627b948cb0241c`에 Styles·ASS Tags·Style editor 그림이 있다. Styles와 그림의 직전 변경은 2014-06-10 `b69e23a…`, ASS Tags는 2014-06-09 `4934ef9…`다. 이 고정 원전은 두 요청보다 앞선다. 2022 snapshot의 같은 경로 조회는 경로 이동으로 실패하여, 실제로 확인한 2021 원전을 두 카드에 통일했다. [판 영수증](release-metadata.json) · [Aegisub 원문 영수증](aegisub-source-receipts.json)

## 2. 카드 후보와 실제 창

| 카드 | 원문·절 | 실제 보여 줄 내용의 범위 | 단어·그림 | 창 밖에 둔 내용 |
| --- | --- | --- | --- | --- |
| L01-N | [0.15.2 ass.h L356–384](https://github.com/libass/libass/blob/c967a5a3d9ec0d36af1148b3fdf2f307a21dd122/libass/ass.h#L356-L384), ass_set_margins API 한 절 | frame margin의 pixel 단위, video와 renderer frame 사이의 거리, positive/negative 공간, black bar에서의 사용·잘림 한계, 함수 선언 | 215 단어·그림 0 | frame size, line-position 기본값, ASS_Style.MarginV, 실제 block 계측 방법 |
| L02-N | [0.17.1 ass_types.h L131–150](https://github.com/libass/libass/blob/e8ad72accd3a84268275a9385beb701c9284e5b3/libass/ass_types.h#L131-L150), ASS_Event 한 절 | Dialogue 한 줄에 대응하는 구조와 Start/Duration/Layer/MarginV/Text 등 필드 | 54 단어·그림 0 | margin 방향·0의 뜻·style 상속·collision 조건·t의 효과 |
| L01-I | [Styles L93–100](https://github.com/Aegisub/aegisite/blob/8dfbd70f89940bf8e327dac80c627b948cb0241c/source/docs/3.2/Styles.html.md#L93-L100), The style editor/Margins | script pixel 단위·정렬별 수직 기준을 설명하는 한 문단과 같은 절의 Style editor 설정 예 그림 | 추가 87 단어·그림 1 | Alignment 별도 문단, ASS Tags, 타 이슈 및 실제 전체 frame 출력 |
| L02-I | L01-I와 같은 선행 절 | 같은 문단·같은 설정 그림. 적용 대상은 흰 event MarginV와의 연결 여부다. | 추가 87 단어·그림 1 | animation 및 collision implementation 설명 |

I의 그림은 단순 장식이 아니라 수치 설정·preview가 있는 실제 편집 예다. 직접 판독한 값은 Left 150, Right 150, Vert 25, Alignment 2 선택, Gill Sans MT 32, 두 줄 preview다. 그러나 preview에는 전체 video frame이나 letterbox가 없으며 collision 결과도 없다. 따라서 **수신 분야 선행 설정 예제는 확보했지만, 같은 요구의 경계 출력 예제가 있는 것은 아니다.** 그림의 다른 style 값도 보이므로 실제 노출은 87단어보다 넓다. D의 그림 유무·추가 분량과 함께 예산 차이를 기록해야 한다.

N에는 사용자가 정한 200단어 추가창 상한을 적용하지 않았다. I/D의 상한은 각각 200단어·그림 한 점이다. 여기서 87단어는 도너와의 실제 단어 수 일치까지 뜻하지 않는다. `receiver-candidates.json`에 원문/표시창 hash, 절단 위치, 단어 계산식과 그림 hash가 있다. 원문은 ignored scratch의 `L01-N-window-original.txt`, `L01-N-window-shown.txt`, `L02-N-*`, `L01-I-*`, `L02-I-*`에 있다. 한글 요약을 원문처럼 보여 주지 않는다.

## 3. A/B의 가용성과 N의 한계

**L01.** API의 frame margin과 ASS의 MarginV는 서로 다른 값을 다룬다. 앞의 값은 출력 frame과 비디오 사이의 화면 pixel 거리다. 뒤의 값은 style/event에 속하며 I는 이를 script-resolution pixels로 설명한다. 두 층을 같은 숫자로 취급할 수 없다. N은 regular event를 black bar에 놓을 가능성을 설명하지만 큰 띠를 식별하고 자막 block의 높이를 측정해 가운데로 옮기는 완성 절차를 제공하지 않는다. B 정책 자체는 caller의 계산을 요구한다. 함수와 MarginV 필드의 존재만으로 그 계산·좌표 변환·정확한 중앙 출력이 보장됐다고 쓰면 안 된다.

N 밖에서 확인한 0.15.2 `ass_set_line_position` 설명의 기본값은 0/bottom이다. 이것을 N 창이 제공한 추가 판별력으로 세면 안 된다. 또한 원문은 정확한 띠 높이·폰트·style margin을 주지 않으므로 중앙 오차의 px 허용차를 이 자료로 만들 수 없다. I의 middle alignment에서 vertical margin이 무의미하다는 조건은 모든 중앙 정렬 조작이 같은 목표를 이룬다는 일반화를 막는다.

**L02.** public ASS_Event에는 MarginV가 timing·text와 독립된 필드로 있다. B가 event MarginV만 바꾸고 t·시각·Layer를 그대로 두는 입력 표현은 가능하다. 다만 N 한 절은 그 숫자가 실제 화면에서 어느 방향으로 움직이는지 설명하지 않는다. I는 bottom alignment의 수직 margin 기준을 제공하지만 style 예제다. event override의 0 상속 처리와 animation의 충돌 판정은 이 두 창에서 직접 확인하지 못했다.

원래 #685 sample은 style MarginV=10, 각 Dialogue event MarginV=0이다. 고정 A의 'MarginV=10'은 원문 style값이라는 뜻으로 읽어야 한다. B는 흰 event MarginV만 nonzero로 지정하는 후보다. 원문이 주지 않은 PlayRes와 font metrics 없이 '몇 px면 충분하다'는 숫자는 만들 수 없다. 충돌이 사라졌더라도 timing/alpha 변화를 버렸다면 원래 목표의 성공으로 세지 않는다.

## 4. 검색 순서·첫 적격 절

1. libass 0.15.2/0.17.1 tag의 tree 경로를 읽고 margin/position/alignment/collision 이름의 공식 예제를 찾았다. 이 파일명 조건을 충족한 예제는 없었다. `compare/test`의 기대 PNG는 열지 않았다.
2. 공식 renderer 예제 `test/test.c`의 init 절을 직접 읽었다. frame size와 font provider 설정은 있지만 고정 A/B의 margin 정책 예는 없어 I 후보에서 제외했다. 실행하거나 출력 그림을 열지 않았다.
3. Aegisub 3.2 manual의 navigation에서 Editing styles가 ASS Override Tags보다 먼저 있다. Styles의 The style editor에서 첫 Margins 절을 찾았다. 같은 절에 실제 수치 설정·preview 그림이 있어 해당 문단+그림을 첫 적격 I로 삼았다. 다른 예제를 본 뒤 더 유리한 것을 고르지 않았다.
4. 같은 manual의 ASS Tags/Animated transform은 Q2의 카드 밖 점검으로 읽었다. alpha가 변형 가능한 태그이며 t1/t2가 line 시작 기준 ms라고 설명한다. 고정 파일 전체에서 collision 문자열은 발견되지 않았다. 이는 구현에 예외가 없다는 증거가 아니며 이 절을 I 창에 더하지 않는다.
5. live 3.2 URL을 먼저 읽은 뒤 공식 Git snapshot·파일 변경 시각을 확보했다. live와 과거판의 동일성을 전체 manual에 확장하지 않고 카드 원문은 고정 Git 판에서만 추출했다.

## 5. 사전 노출·실패·분모

- 일반 웹 검색으로 manual 저장소명을 찾는 과정에서 Aegisub 현행 release, 다른 프로젝트의 subtitle 예제와 별도 이슈 snippet이 함께 노출됐다. 지정 libass 이슈의 댓글/후속 출력은 아니며 카드·근거 배당에는 사용하지 않는다. 특히 후대 editor 옵션·다른 정렬 문의를 이 A/B의 당시 가용성 증거로 사용하지 않는다.
- 기존 공개 REST core 한도가 60/60으로 소진되어 release metadata GET이 403이었다. 이미 제공된 사용자 GitHub connector에서 같은 공개 metadata를 읽었다. release 본문은 표시하지 않았고 새로운 계정·토큰·권한을 만들지 않았다.
- 옛 manual의 두 장·그림·live 미러는 **Aegisub 3.2 manual 한 저작**, libass의 두 tag·두 public header는 **libass public API 한 저작**으로 센다. 수신 공식/독립 예제 배당에 libass 쪽에서 확보한 고유 저작은 **2**다. 비선정 `test/test.c`는 직접 읽은 별도 공식 예제이지만 적격 I 배당 수를 부풀리는 데 사용하지 않는다.
- root는 원문 창·그림을 읽고 최종 예측을 고정해야 한다. 현재 자료로 historical runtime 동일성, 중앙 위치 수치, t 포함 collision 예외, B의 실제 경계 성공을 확인했다고 할 수 없다.
