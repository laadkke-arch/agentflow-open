# 독자에게 돌려줄 링크와 한 줄 이유

## I1 · 찍어 둔 텍스트 상자를 각각 고치기

[Inkscape 1.0.2 Duplicate의 참조 shape 복사·재연결](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/selection-chemistry.cpp#L433-594)을 대표 후보로 반환한다. 원문에서 독립 크기 변경을 이미 요구했으므로 다시 묻지 않는다. [stamp](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/seltrans.cpp#L530-595)는 같은 목적의 검증된 대체품으로 묶지 않으며, [당시 설명](https://gitlab.com/inkscape/inkscape/-/issues/2225#note_508328484)으로 shape-inside 예외를 연결한다. 사용자 배포판의 paired resize 출력은 미확인이다.

## I2 · 원본 path를 고칠 때 연결 path도 바뀌게 하기

[기존 LPE target에 clipboard 원본을 연결하는 버튼](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/live_effects/parameter/item.cpp#L248-280)과 [선택 원본으로 새 LPE path를 만드는 메뉴](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/selection-chemistry.cpp#L2937-3002)를 조건과 함께 남긴다. 1.0.2 clipboard 버튼의 invalid ID 재현 및 [MR2570 수정](https://gitlab.com/inkscape/inkscape/-/merge_requests/2570)은 별도 시점의 근거다.

한 번만 물을 질문: **기존 복제 path의 ID와 이미 붙은 속성·효과를 유지해야 하나요, 새 연결 path를 만들어도 되나요?**

- 기존 target 유지: 버튼 경로와 clipboard 수정 근거를 유지한다. 1.0.2에서 작동한다고 보증하지 않으며 해당 판 수정/시험이 필요하다.
- 새 target 허용: 직접 메뉴 경로를 우선 후보로 보여 준다. 원본 하나를 선택해 새 target을 만드는 코드라는 이유를 붙인다. 버튼과 완전 대체라고 확정하지 않는다.

## I3 · sprayed clone과 원본을 지우는 작업

[Eraser Delete의 touched/selected 대상 처리](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/ui/tools/eraser-tool.cpp#L664-838)와 [원작성자의 selection 조건 정정](https://gitlab.com/inkscape/inkscape/-/issues/2283#note_531299709), [후속 crash 수정 MR4079](https://gitlab.com/inkscape/inkscape/-/merge_requests/4079)를 연결한다. 이미 선택된 원본 때문에 clone이 지워지지 않았다는 조건은 후속에서 밝혀졌으므로 같은 질문을 다시 하지 않는다. 후보2는 비워 두고 다른 입력인 Select+Delete나 clone을 copy로 바꾸는 방안을 조용히 대체품으로 넣지 않는다.

## 단순 도형의 독립 객체가 목적일 때

[일반 unlink](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/src/selection-chemistry.cpp#L2701-2789)와 [recursive unlink의 원 시험](https://gitlab.com/inkscape/inkscape/-/blob/e86c870879310bfb4a9abee3e7fd65aef0408fd7/testfiles/src/object-set-test.cpp#L450-519)은 단순 primitive의 type·개수와 해당 시험의 다음 원본 선택까지만 묶음 근거가 있다. group 자식 clone까지 끊어야 한다면 recursive 조건을 별도 링크로 남긴다.

실제 사용자에게 이 카드를 보여 준 경험, 클릭 절약, 시간 절약은 관측하지 않았다.
