# AF-RES-236 HANDOFF

**실제 자체 판정: PARTIAL.** 조사 결과, 자료 원장 및 필수 파일을 커밋했고 고정 결과 SHA에서 재열람했다. 본 모집 공식 링크 후보는 존재하지만 동일인 성공 교체/사전 미인지까지 연결된 완전한 사슬은 없으며, OSM 개별 원본과 최신 control 항목을 직접 읽지 못했다. 자료 총수 충족을 DONE으로 승격하지 않는다.

- 저장소/작업 브랜치: laadkke-arch/agentflow-open / work/research-af-res-236
- 시작 통합 SHA: 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6
- 계획 SHA: 914dbfa789ebec97063ed97130ea2a71c2e9f503
- **고정 결과 SHA: f8d76bcbfed2073733b377a84350a5a01e3cc3fa** (HANDOFF 직전)
- [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/SELF_CHECK.md), [sources](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/sources.jsonl), [frame](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/frame.csv), [chain](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/chain.csv), [rivals](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/rivals.csv), [before](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/before.md), [SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/SCOPE.md)

## 실제 결과

- 본 40/40 댓글 조회 성공(현재 228, 60일 내 174, 빈 창 8). 넓은 공식 URL 후보 3/40, 슬롯 3/6(3 공석); 엄격한 원래 필요 직접 대체 방향만 1/40. 링크 읽기 자기보고 1/3, 직접 사용/선택 교체 산출물 관측 0/3, 사전 미인지와 교체를 모두 뒷받침하는 사슬 관측 0/3. 미관측은 실제 사용 0을 뜻하지 않는다.
- M1 #8785 SurfaceTool.index 유용성 언급, 계속 strip 변환 요청; accidental close는 URL보다 먼저. M2 #8793 Reimport 이미 사용, 읽었으나 설명 불충분. M3 #8803 feature tags는 후속 export 질문; 해결 기대만, 타인 close. S1 #8903 separate 1/2, 이미 문서 읽고 알고 있었으며 시도 후 실패 보고, 타인 duplicate close; 실제 성공 0/1 관측. #9077/#9222의 놀람/감사/미인지 표현은 공식 권고 URL 부재 또는 요구 불일치. 16 보강 screen 전체 검색 결과를 전수 읽은 것이 아님.
- 100 ledger rows / counted 54 / 고유 counted work_id 54. 32 본 discussion, 1 supplemental, 8 fixed docs, 5 engine code, 4 PR, 2 process, 2 OSM original docs. OSM 목표 3 중 2, 원본 사건 0/2: #5502267/#5597274는 미러 후보로만 유지. 원자료 성공 수·독립 사건·모집층을 분리.
- AF-RES-225 고정 5개 파일(d1d8595dd72dcfc809c1045e20d44366bbe30ae5) 읽음, 자체 PARTIAL 유지; 225 권고 URL 없음 vs 236 성공 산출물 없음, 서로 결측 보완으로 인과 사슬 조립 금지. 227–229 중간 결과 사용하지 않음.

## 커밋 / 재검사 영수증

1. 범위/표집: 009a23b3e6f35b9727c044e045bc39686a570c89; 2911fc8de63f5f1ae61fc9c2a90c1f008e6b35dc; before pre-comment 봉인 fb536c8fa26732e7f984e4aead61608338db21e2.
2. 원자료: 57ebd9dcfd25ccf6c3b4dbb5546383a0477c3a28; 4e885d235e41b0d2720f2ff12b0afd973fe106d0; e27b20c1ef32f273df0907da4d5f991beee5f5d9; ba4325cb3d768ece730717573410e4c7d9b45ee8; fixed docs 18e6b7ac1bd8bc243dbf2538cb1f7ccdfa3a65fe; supplement 9bf62d19707150149c8fe356066b2948fc87dab0 / 36bef8e8519a6fc203bce2cad897e91b7033832f; engine 683643c3a92b5f5f89681c2f523f715a7d23ac34; events 2852c99dcb0bb1fd4dee9790bcfc2c6c1e4c65b1; frame classification 00563af6f6f37049e47437101df8ceeb680dbe87; correction 44edcfd0f55b849e8c4963d8fca09a1c9f81142d; consolidated ledger fa1b9356fb1a5e046f3faa7a9736cbf06adc0a5a.
3. 주관측 chain 2de5cbc3c0dc2dd74e8830e993d096c5574652d0.
4. 반례 cf0d20a52dcac21276bfab7c42a414cefee4c093.
5. RESULT 7d7f03080289a6392a4c50a7cd0bc5123d5b3ebc; SELF_CHECK f8d76bcbfed2073733b377a84350a5a01e3cc3fa.
6. 이 HANDOFF만 마지막 단독 커밋.

고정 결과 SHA에서 8/8 필수 파일 읽기 확인, source JSONL 100 unique source_id/54 counted/54 distinct work_id, 필수 키 누락 0, frame 40+3 slots+3 vacancies, supplement 1, RESULT 두 필수 헤더·Q1–Q7·마지막 3약점 확인. compare(start...result) ahead 19 behind 0, 변경 파일 18개 모두 owned_path, 외부 0. dot-control 변경 없음. 자체 검사만 시행; 독립 검토·실행 재현 없음.

## 중요한 약점

1. 최신 통합/계획 control blob 크기/접근 문제: fetch_file empty, raw/blob 읽기 실패. 비교 결과 통합은 계획보다 6 ahead, control 파일 +308/-9. 실제 236 항목 및 depends_on 차이는 미확인. 제공된 본문과 225 고정 입력만 사용. 
2. before.md의 workaround 정규식이 'worked around'를 놓친 추출 결함: 후속 before-correction.jsonl 작성, 최초 봉인 수정 안 함. 원래 생성 본문/댓글 편집 이력·작성자의 판·그날 floating HTML 미확인. 노출의 넓은 정의(M2/M3)를 좁은 정의와 분리.
3. 성공 사슬 없음, OSM primary case 접근 실패. 4.2 source/docs는 존재를 지지하지만 개인의 적용·결과를 보장하지 않는다. 원본 OSM 두 사례와 작성자 artifact를 보강해야 한다.

## 다음 첫 행동 — control 입력 복구 후 OSM 원자료

아래 명령은 Codex 인계용(실행하지 않음). 기존 승인된 GitHub 접근, git/gh/jq/curl 사용 환경에서 read-only 확인; 새 유료 API, 계정 변경, 보호 우회 없음. 기존 worktree에 손대지 말고 임시 checkout에서 작업. 기록은 owned_path에만 추가한다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-236
for rev in 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6 914dbfa789ebec97063ed97130ea2a71c2e9f503; do
  git show "$rev:docs/automation/dot-control.json" | jq '.. | objects | select(.id?=="AF-RES-236" or .task_id?=="AF-RES-236")'
done
git diff 914dbfa789ebec97063ed97130ea2a71c2e9f503 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6 -- docs/automation/dot-control.json
# Extract actual depends_on from latest matching object; read each dependency result_commit:.../HANDOFF.md.
for n in 5502267 5597274; do
  curl -fsSL "https://api.openstreetmap.org/api/0.6/notes/$n.json" |
  jq '.features[0].properties | {id,status,comments:[.comments[]|{date,action,uid_present:has("uid")}]}'
done
# Separately compare uid equality in memory only (reporter A/editor B, not names or location).
for n in 8785 8793 8803 8903; do
  gh api --paginate "repos/godotengine/godot-proposals/issues/$n/comments?per_page=100" --jq '.[]|{id,author:.user.login,created_at,updated_at,body,html_url}'
  gh api --paginate "repos/godotengine/godot-proposals/issues/$n/timeline?per_page=100" --jq '.[]|{event,actor:.actor.login,created_at,id}'
done
```

예상/반전: control 236 최신 entry와 brief 불일치이면 해당 변경 재판정. OSM 원본 action·actor·순서가 mirror와 일치하면 primary 역할 확인; 불일치이면 mirror 주장을 폐기. 원제안자 개인의 사용 여부는 close/action만으로 확정 금지. GitHub 공개 edit history UI에서 최초 revision이 제공될 때만 사전 지식 판정 갱신; 미제공 시 미확인 유지. 60일 창 동일 작성자 공개 artifact에 기존 접근→추천 접근 변경과 정확 기능/판 증거가 있으면 A gate 재검토; 이후 날짜/타인 코드는 통제.

## Codex 재현 후보 (실행하지 않음)

고정 Godot 4.2-stable = 46dc277917a93cbf601bbcf0d27d00f6feeec0d5. 이미 승인된 설치 또는 별도 임시 checkout에서 이 판 바이너리만 사용. `godot --version` 및 `git rev-parse HEAD` 확인; 아래 entrypoint의 fixture 파일을 새로 준비하되 소유 경로 밖 repo 파일 수정 없음. 실행 환경/fixture 미제공으로 명령 자체도 미실행. 기대와 반전을 반드시 분리.

- M1: headless project fixture, 두 삼각형의 여섯 vertex(공유 모서리 두 vertex 동일 attributes; baseline no index), SurfaceTool.begin(Mesh.PRIMITIVE_TRIANGLES), add_vertex, commit_to_arrays 전후 비교. `godot --headless --path "$FIXTURE" --script res://test_index.gd`. 출력 vertex/index 배열 개수·primitive·실행판. 기대 6→4 unique vertices/6 indices, 삼각형 topology 보존; 이미 indexed input은 no-op. UV/normal 다른 공유 좌표 및 disconnected triangles 음성 입력. 기대 실패/실제 VRAM 악화면 최적화 문구 약화; 메모리 측정 별도. 이는 작성자 채택이 아님.
- M2: 4.2 editor 임시 PNG 또는 glTF asset import, 원본 SHA256 기록, import setting(예: texture compression) 바꾸고 Reimport, 원본 hash와 .import 설정/가공 resource 갱신 대조. `godot --editor --path "$FIXTURE"`; 정상 UI entrypoint FileSystem→Import dock→Reimport. 기대 원본 unchanged, 가공물/settings 갱신; 원본 변경되면 문서 해석 재검토. UI 명료성은 별도 관찰.
- M3: fixture project.godot에서 debug/file_logging/enable_file_logging 및 log_path에 linux/android/ios feature override를 설정, 실제 export preset/해당 플랫폼 template 확보 후 `godot --headless --path "$FIXTURE" --export-release "Linux" "$OUT/game.x86_64"` 등 플랫폼별 정상 entrypoint 사용; 정확 preset 이름은 fixture에 맞춤. OS.has_feature 및 ProjectSettings.get_setting_with_override 값을 찍고 로그 경로 확인. Android renderer 및 iOS는 해당 장치/빌드에서만 검증. 플랫폼 override 성공은 systemd redirect/SIGHUP 성공과 별개.
- S1: 두 서로 다른 짧은 AudioStream, AudioStreamPlayer.stream = AudioStreamPolyphonic.new(), polyphony≥2, player.play() 후 get_stream_playback().play_stream 두 번, 둘의 ID 및 is_stream_playing overlap; ordinary player.max_polyphony 및 stream 교체 baseline. `godot --headless --path "$FIXTURE" --script res://test_polyphonic.gd` (dummy audio와 실제 audible 결과 구별). 4.2 API 존재/두 stream 동시 제어 기대, INVALID_ID(-1)/method 없음/기존 stream 중단/설정 보존 실패면 범위 좁힘. 4.3 권고자 샘플을 실행한 것으로 간주하지 않음. 원 제안자의 환경·파일이 없으므로 실제 실패 원인 단정 금지.

## 색인 반영 제안 (직접 변경하지 않음)

AF-RES-236: PARTIAL, Godot official-link 40 frame / 3 broad exposures / 1 strict original-purpose / 0 observed successful author artifacts; separate prior-aware failed S1; OSM docs-only, primary cases pending; sources 54 counted / 100 rows. Keywords: versioned prior art, URL exposure vs click/read, prior knowledge, fit, same actor artifact, rejection, third-party closure, scope sensitivity. 225와 결합해도 직접적인 discovery→substitution 증거는 아직 없음. 중심 상태 파일/색인 변경은 통합 담당자 권한에 맡김.
