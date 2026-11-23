# AF-RES-085 · 범위와 사전 봉인

계획판은 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`이다. 이 판에는 AF-RES-085 행이 아직 없다. 작업 브랜치가 원격에 없음을 확인한 뒤 AF-RES-085의 RUNNING 행을 포함한 당시 최신 통합판 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`에서 `work/research-af-res-085`를 시작했다. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF 및 통합판의 과제·의존 행을 읽었다. 소유 경로는 `docs/workstreams/research/AF-RES-085/`다. 계약은 v2로 `workbench.session start ... --fetch`가 생성했다. [고정 통합판의 진행표](https://github.com/laadkke-arch/agentflow-open/blob/9dcae48a47b05d7ba2a1320444be28f5d0fcd739/docs/automation/dot-control.json) · [계약과 실험 핀](manifest.json)

유일한 의존은 `work/research-af-res-081=60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc`다. HANDOFF, RESULT 표 2·3, E05/E06 원장, reproduce, 패치와 빌드 지문을 읽었다. 같은 라운드의 다른 연구 결과는 범위 밖이다. 081의 36행·21개 원시험 전수 재실행, 신고자 설치물과 TEI 영향 조사는 이 과제의 분모 밖이다. [081 인계](https://github.com/laadkke-arch/agentflow-open/blob/60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc/docs/workstreams/research/AF-RES-081/HANDOFF.md)

## 독립 변수

- U는 PR #4590 병합 첫 부모 `f4fcf53ff65c56f0efb616a3af209d3faba9b342`다. G는 실제 병합 `16851045c9e50eafb016c5cf4f2733f974e841bf`의 Element 복사 수정이다. L은 AF-RES-081의 새 Excerpt 한정 수정이다. 모든 빌드에 같은 컴파일 호환 변경과 읽기 계측을 적용한다. [G 병합](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) · [081 패치](https://github.com/laadkke-arch/agentflow-open/tree/60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc/docs/workstreams/research/AF-RES-081/patches)
- X1·X2의 두 보표는 0 기반 staff 0·1이고 반열림 범위는 [0,2)다. 한 마디라 Source voice 2(트랙 1)의 E4를 Destination voice 1(트랙 4)로 옮길 수 있고, 단일 성부 두 음 화음은 높은 E4를 트랙 0, 낮은 C4를 트랙 4에 남길 수 있다. 기본 keep/destination 계산이 세 번째 보표까지 가지 않도록 첫 두 보표를 명시적으로 선택한다. 세 번째 staff와 기존 Violin 파트는 독립 대조다. [Explode 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2474-L2613)
- X1의 메뉴 경로는 `CloneVoice(...,1,4,-1,false)`를 거쳐 `cloneVoice(1,4,start,end,false,true)`에 이른다. 마지막 `true`는 선언의 기본 spanner 인자다. 이 악보에 spanner는 없다. E05는 `cloneVoice(0,1,start,end,false,false)`, 같은 staff의 다른 voice에 원본을 유지하는 직접 호출이었다. [CloneVoice::redo](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/undo.cpp#L516-L554) · [기본 인자](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/score.h#L701)
- X3·X4는 같은 악보 bytes를 쓴다. `study-child` tag=2, `shown` mask=3, `hidden` mask=1, 초기 layer는 `shown`이다. 이 판 자체의 `-e`로 노출되는 상태 막대 layer 전환을 사용한다. X3은 master의 같은 손가락 번호를 선택한 다음 숨기고, 새 Flute에서 다시 보인다. X4는 중간에 숨기지 않는다. 다른 기존 Oboe 파트의 음과 master peer를 감시한다. [스위치 호출](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/musescore.cpp#L5326-L5332) · [태그 순회](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/note.cpp#L2229-L2238)

## 다음 편집과 관측 기준

각 입력을 U/G/L에서 새 XDG 상태로 두 번 실행하는 24자리다. 081과 같은 용어로 flag/list/mark는 객체의 선택 비트·실제 선택 membership·재생 mark다. 자식의 mark는 적용되지 않는다. 색·영역은 별도로 기록한다. 위치, pitch, 실제 ticks·duration, score 및 link peer, Fingering 부모·tag·visible로 객체를 대조한다. 포인터는 한 프로세스 안의 이력에만 쓴다.

X1·X2는 메뉴 이후 `6`을 누른다. 메뉴가 남기는 RANGE에서는 `Selection::cr()`가 비어 지속 음가 변경이 없다는 사전 예상이다. 주 판정의 화면을 남긴 다음 목적지 음을 한 번 눌러 `6`을 실행하는 X1-R/X2-R는 마우스로 새 선택을 만든 별도 조건이다. 원상복귀는 바로 앞 편집의 undo index가 늘었을 때만 실행한다. [선택에서 단일 chord/rest 반환](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L140-L159) · [음가 명령](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/score.cpp#L2740-L2767)

X3·X4는 새 파트에서 `V`로 자식의 `VISIBLE`을 바꾸려고 한다. 파란 자식을 사용자 입장에서 선택 대상으로 오인할 수 있다. 실제 목록이 비면 무변화라는 사전 예상이다. X3-R/X4-R의 한 번 재클릭 뒤 같은 `V`는 새 파트 Fingering만 끄고 undo하면 복구되어야 한다. 이 판에서 VISIBLE은 비링크 속성이다. layer tag로 실제 표시 대상이 빠지는 것과 자식의 저장 가능한 visible 속성을 구분한다. [toggle-visible](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L3471-L3483) · [속성 링크 표](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/property.cpp#L49)

메뉴 전, 복제 직후, 재선택/파트 생성 경계, 메뉴 종료, 다음 편집 뒤, 해당 undo 뒤, 저장·새 프로세스 재열기를 읽는다. 사전 의도나 값이 틀리면 입력과 기대값은 그대로 두고 차이를 후속 커밋에 쓴다. X3의 숨은 원본 child flag가 풀리거나, 복제가 없거나, GUI 경로에 도달하지 못하면 각각 독립 기록한다. 그 경우 필요한 연구자 API 주입은 별도 ID로만 집계한다. 재클릭 조건과 음성 대조는 원 24회와 분리한다. [입력·해시·기대값·반증 조건](cases.csv)

동일 bytes·경로·반복에서 G/L 측정이 모두 판독되는 경우만 짝으로 센다. 가능한 G/L 짝 8개와 U 기준 대조 8개를 보존한다. 정상 메뉴와 편집 전후 객체를 식별한 자리만 사용자 편집 판정을 준다. 네 입력의 요구 상태와 두 반복, 기준과 대조가 관측되고 출처 분모를 채우면 REVIEW_READY, 나머지는 PARTIAL이다. 기동 성공, API 호출, 재선택 후 성공은 본 실험의 미도달 자리를 채우지 않는다.
