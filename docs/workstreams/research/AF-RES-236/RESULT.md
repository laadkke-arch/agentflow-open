| 제안·시간창 | 사전 필요·알던 대안 | 실제 제시 URL·시각 | 당시판 적격 절 | 같은 사람의 다음 행동·원산출물 | 미확인 |
|---|---|---|---|---|---|
| M1 [#8785](https://github.com/godotengine/godot-proposals/issues/8785), 2024-01-03 16:42:25Z~03-03 16:42:25Z | 넓은 맵 RAM/VRAM 감소; triangle strips/fans 자동화; 현재 workaround No | [댓글](https://github.com/godotengine/godot-proposals/issues/8785#issuecomment-1875706070), clayjohn, 01-03 17:16:55Z → [SurfaceTool.index](https://docs.godotengine.org/en/latest/classes/class_surfacetool.html#class-surfacetool-method-index) | [D01](https://github.com/godotengine/godot-docs/blob/55d4bd80102628845f0c16a15ff187fa2f4682b4/classes/class_surfacetool.rst#L496) vertex array 축소; A04 기존 index이면 no-op; A01/A02 import 단계 index | sammonius [첫 답](https://github.com/godotengine/godot-proposals/issues/8785#issuecomment-1875821247) 실수 종료, [다음](https://github.com/godotengine/godot-proposals/issues/8785#issuecomment-1875865603) 유용성 인정, [이후](https://github.com/godotengine/godot-proposals/issues/8785#issuecomment-1876015267) strip 병용 요구; [마지막](https://github.com/godotengine/godot-proposals/issues/8785#issuecomment-1877257504) addon 가능성. 작성자 파일 관측 없음 | 실제 클릭·실험·선택 교체·index 사전 지식; RAM 절감량 |
| M2 [#8793](https://github.com/godotengine/godot-proposals/issues/8793), 01-04 12:05:25Z~03-04 12:05:25Z | Reimport 버튼 이미 사용; Save로 이름 변경, 원본 저장/내부 import 설정 혼동 | [댓글](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877072086), AThousandShips, 01-04 13:10:13Z → [Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html) | [D02](https://github.com/godotengine/godot-docs/blob/ec71ddb6cc92414fc2f386e9790b747d30b88431/tutorials/assets_pipeline/import_process.rst#L29-L49): 비-native 자원, 설정 변경 후 Reimport; 원본 파일 변경 아님 | Bat-Computer [첫 답](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832) 13:40:07Z 링크 읽었다고 말함, 설명 여전히 불명료; [14:02:53Z](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877143602) 원본 저장 기대 및 명료성 요구 유지. 파일 관측 없음 | 읽기 자기보고 외 클릭 증거, workflow 교체·정확한 이해 지속 여부 |
| M3 [#8803](https://github.com/godotengine/godot-proposals/issues/8803), 01-05 08:44:31Z~03-05 08:44:31Z | systemd 로그 출력/CLI/SIGHUP; 01-06 새 질문으로 iOS·Android·Linux 설정 자동화 | [댓글](https://github.com/godotengine/godot-proposals/issues/8803#issuecomment-1879608615), AThousandShips, 01-06 09:27:20Z → [Feature tags](https://docs.godotengine.org/en/latest/tutorials/export/feature_tags.html) | [D03](https://github.com/godotengine/godot-docs/blob/ee401703f0db24922e4808de7efe46bd809766a9/tutorials/export/feature_tags.rst#L153-L174) feature override; D04 logging keys; 원래 CLI/SIGHUP 불충족 | theromis [14:58:12Z](https://github.com/godotengine/godot-proposals/issues/8803#issuecomment-1879721130) 해결할 듯하다는 미래 표현. 01-22 YuriSizov 종료(T8803). 작성자 파일 관측 없음 | export 적용·실행·원래 서버 로그 해결 |
| M4–M6 | 공석 | 해당 없음 | 해당 없음 | 해당 없음 | 본 모집 내 추가 적격 URL 미관측 |
| S1 별도 [#8903](https://github.com/godotengine/godot-proposals/issues/8903), 01-17 21:03:12Z~03-17 21:03:12Z | 복수 AudioStream 동시 재생, volume/pitch/bus 설정 보존; 이미 Polyphonic 및 Max Polyphony 시도, 직접 노드 생성/free 우회 | [댓글](https://github.com/godotengine/godot-proposals/issues/8903#issuecomment-1896948598), AThousandShips, 01-17 21:50:29Z → [PlaybackPolyphonic](https://docs.godotengine.org/en/stable/classes/class_audiostreamplaybackpolyphonic.html) | [D08](https://github.com/godotengine/godot-docs/blob/5482c93e8701d9c5620237a43d28a1c36f5e79ac/classes/class_audiostreamplaybackpolyphonic.rst), Description 및 play_stream/INVALID_ID; A05 4.2 코드 | amarraff [첫 답](https://github.com/godotengine/godot-proposals/issues/8903#issuecomment-1897450622) 이미 알지만 사용법 모름; [사전 열람 명시](https://github.com/godotengine/godot-proposals/issues/8903#issuecomment-1898495051), [syntax 실패](https://github.com/godotengine/godot-proposals/issues/8903#issuecomment-1898529625), [예제 실패/이의](https://github.com/godotengine/godot-proposals/issues/8903#issuecomment-1898583454). 권고자 zip은 작성자 산출물 아님 | 실행 실제 원인·zip 내용·작성자 최종 해결; 성공 교체 미관측 |
| S2 별도 | 공석 | 해당 없음 | 해당 없음 | 해당 없음 | 긍정 표현이 있는 #9077/#9222는 적격 공식 링크 아님 |

표 1 행 단위: 원제안별 최초 60일 중 최초 공식 기존 기능/동작 문서 링크(넓은 정의), 공석은 사건 수에 불산입. S1은 독립 모집층. 시각은 전부 2024년 UTC. 작성자 식별은 동일 GitHub 공개 login만, 최초 본문은 미복원.

| 사건·모집층 | 존재 | URL 제시 | 직접 사용·선택 변경 | 사전 미인지 근거 | 경쟁 설명·허용 문구 |
|---|---|---|---|---|---|
| M1 본 | 당시 4.2 문서/코드 있음; 목적 일부 | O | 유용성 언급 O; 적용/교체 미확인 | strip 무지 발언은 index에 해당하지 않음 | 기존 importer도 index; strip 변환은 계속 요청. “관련 내장 기능을 제시했고 당사자가 유용성을 인정했다” |
| M2 본(설명) | Reimport 있음 | O | 링크 읽었다는 자기보고 O; 사용 변경 미확인 | 기존 버튼 사용, 메커니즘 오해 | 설명 불충분 및 버튼 UX 논의 지속. “문서를 읽었다고 했으나 선택 변경은 확인되지 않았다” |
| M3 본(후속) | feature tag override 있음 | O | 예상 해결 발언 O; 적용 미확인 | 미확인 | 원래 CLI/SIGHUP와 다른 하위 목표. “플랫폼별 설정 대안을 제시했다” |
| S1 보강 | polyphonic playback 있음(4.2) | O | 시도/실패 자기보고 O; 성공 교체 미확인 | 반대 증거 O: 제안 전 문서 읽음 | setup·서로 다른 stream·version/문서 오해. “알고 있던 기능을 다시 권했지만 당사자가 실패를 보고했다” |
| #9077 보강 통제 | export filter 이름/화면 제시 | X(비공식 screenshot만) | 놀람·감사; 실제 원산출물 미확인 | 놓쳤다는 발언 O | 다른 사람 10월 성공·docs PR을 당사자에게 귀속 금지 |
| #9222 보강 통제 | editor offset 제시 | X | 미인지 발언 후 부적합하다고 설명 | 특정 동작에 대해 O | pixel 편집 != normalized pivot/3D. 새 정보가 있어도 선택하지 않음 |
| OSM 통제 | 상태 전이 API 존재 | 사례 원본 미확인 | 미확인 | 해당 없음 | 다른 사람 close/reopen 가능; mirror는 가설 근거만 |

표 2 행 단위: 사건/통제 1개, 독립 문턱별 판정. O는 공개 관측이며 성공·인과를 의미하지 않는다. X는 관측된 해당 권고에 적격 URL 없음. 미확인과 0 관측을 구별한다.

## 판정: PARTIAL

**본 40개 중 공식 기존 기능/동작 문서 링크 후보 3개(7.5%)**. 6자리 중 3 공석. 이 3개 중 원제안의 목적을 직접 대체할 수 있는 방향 제시만 엄격히 남기면 M1 1개(2.5%; 완전 등가성은 불명). 설명 M2와 후속 하위 질문 M3를 포함한 넓은 모집을 먼저 보존하고 좁은 민감도 분모를 따로 제시한다. 링크 읽기 자기보고 1/3(M2); 같은 작성자의 실제 적용/교체 원산출물 관측 0/3; 직접 사전 미인지와 성공 원산출물이 연결된 완전 사슬 관측 0/3. 관측되지 않은 사용은 미확인이지 실제 사용률 0%가 아니다. 별도 S1 1개 중 권고 전 해당 페이지를 이미 읽었다는 진술 1/1, 후속 실패 자기보고 1/1, 성공 원산출물 관측 0/1. 서로 다른 모집층의 비율을 합산하지 않는다.

## Q1. 원래 필요·사전 대안과 모집

R00의 REST 검색은 2024-01-01~03-31 created asc, 첫 페이지 50개, total_count=470, incomplete_results=false. 번호 tie-break를 적용한 첫 40은 #8764~#8810, 01-01 11:46:20Z~01-06 01:20:50Z; 최초 40 중 봇/PR/관리용으로 제외한 항목 0; #8781은 후일 discussion 전환이지만 신규 제안으로 유지. 10개는 cap 밖. 댓글 조회 40/40 성공, 현재 총 228개, 생성 후 60일 174개, 8개는 이 창 댓글 0개, 32개는 1개 이상, 전체 반환 수/검색 메타데이터 일치 40/40. 삭제 댓글/비공개/검색 시점 후 변경 미확인. frame.csv 및 comments-01~04.jsonl, I8764~I8810.

before.md는 댓글 열람 전 현재 본문을 커밋했다(fb536c8fa26732e7f984e4aead61608338db21e2). 단 workaround 템플릿의 “worked around” 분리형을 추출하지 못한 오류가 있었다. before-correction.jsonl에 후속 원문 재추출, 봉인 이전으로 소급하지 않는다. 현재 본문과 원초 본문의 동치 미확인; G01 편집 이력 가능/삭제 가능. M1 workaround No 및 index 미언급은 무지의 증거가 아님. M2 이미 버튼을 사용, 원본 파일/가공물의 의미를 오해한 사례. M3 원래 systemd 출력과 후속 platform override를 분리. S1 현재 본문과 사후 당사자 발언 양쪽이 이미 알고 있었다고 지지. S1은 결과 표현 검색 후 본문 열람했으므로 사전 독립 봉인 아님.

## Q2. 정확한 URL과 노출

chain.csv는 댓글 permalink/작성자 제공 outbound URL을 별도 열에 보존. I8785/I8793/I8803/S8903의 실제 댓글 본문과 UTC를 확인했다. 최신/안정 alias URL은 당시 서버가 제공한 정확한 HTML이 남아 있다고 가정하지 않는다. 4.2 branch에서 권고 시각 이전 파일 변경 커밋을 직접 열어 D01~D08 고정했다. 발화자가 링크한 URL 자체와 고정 근거의 URL은 다르다. 클릭은 관측 불가; M2의 읽기 발언만 직접 자기보고다. M3의 첫 답 c1878401829는 이름만, URL 권고는 다음날의 별도 질문 후. #8780 screenshot, #8792 제3자 addon, #8769 planned PR, #8806 source code 링크, #9077 screenshot은 공식 기능 설명/공식 데모 URL로 세지 않았다. duplicate proposal 링크만은 별도 통제.

보강은 긍정 표현 검색("didn't know" 0, "works perfectly" 2, "solved my" 0, "I wasn't aware" 0, "that works" 34 중 첫30, "thank you" 40 중 첫30)으로 후보 탐색. main 제외 16개 대화 직접 열람; 결과 선택 편향이 있으므로 분모 16은 스크린일 뿐 발생률 표본 아님. S1은 해당 검색 표현이 있지만 문서 이미 읽음/실패라는 반례가 직접 확인되어 보강에 보존. #8850의 URL은 60일 밖; #9142의 작성자 증거 링크는 60일 밖; #9077, #9222는 적격 URL 없음. 2자리 중 1 공석; 모든 검색 결과를 완전히 스크린했다고 주장하지 않는다.

## Q3. 당시 판에서 적합했나

- M1: D01 L496 및 [A04](https://github.com/godotengine/godot/blob/46dc277917a93cbf601bbcf0d27d00f6feeec0d5/scene/resources/surface_tool.cpp#L749-L773) 4.2-stable(2023-11-29 tag commit)에서 index가 이미 있으면 반환, Vertex 기반 중복 제거/index 배열 생성. [A01 OBJ importer](https://github.com/godotengine/godot/blob/fbaab3cf537a892295aabdfd02c8052e370e6669/editor/import/resource_importer_obj.cpp#L399), [A02 ImporterMesh](https://github.com/godotengine/godot/blob/fbaab3cf537a892295aabdfd02c8052e370e6669/scene/resources/importer_mesh.cpp#L1304) 호출 존재. 이미 index된 mesh에 절약 효과 없음. strip primitive와 다르며 GPU/cache/실제 mesh attribute 구성에 따른 비용은 미실행. 권고자가 더 낫다고 말한 사실과 전 mesh에 우월하다는 실측을 구분.
- M2: D02 L17–23,29–49 source asset과 내부 가공 자원, 비-native import settings의 Reimport; 버튼 이름 변경으로 파일 저장 동작을 만들 수 없다. 원래 요구의 목표가 명료한 UX라면 문서만으로 완전 대체 못함.
- M3: D03 L43–57 플랫폼·debug/release; L101 mobile; L153–174 project settings feature override. [D04](https://github.com/godotengine/godot-docs/blob/3c2eef1f25478421247c272e006c5e60f131ddda/classes/class_projectsettings.rst#L2345) enable_file_logging 기본 false, pc override true, log_path 기본 user://logs/godot.log. 권고 댓글의 .mobile/.android는 예시이고 요청한 Linux 설정 및 Android renderer는 정확한 해당 플랫폼 key 검사가 필요. logrotate/SIGHUP/daemon PID와 등가 아님. OS별 실제 export 미실행.
- S1: D08 Description 및 play_stream에 polyphonic stream 설정, playback 객체 취득, stream·offset·volume·pitch 인자, capacity 도달 INVALID_ID(-1). [A05](https://github.com/godotengine/godot/blob/46dc277917a93cbf601bbcf0d27d00f6feeec0d5/scene/resources/audio_stream_polyphonic.cpp) 구현 존재. 단 일반 stream player의 max_polyphony를 올리는 것과 서로 다른 stream을 동시에 재생하는 것은 구별. 4.2 vs 4.3, playback 초기화, node 설정 계승/버스/공간 음향 요구 확인 필요. [P81858](https://github.com/godotengine/godot/pull/81858) 문서 보강은 2024-04-08 병합(창 밖): 이전 설명 부족 문제를 지지하지만 당시판에 소급하지 않음. 당사자가 보고한 실패를 코드 존재만으로 뒤집지 않는다.
- #8784 D05는 body_entered에 monitoring true 필요, author의 monitorable/monitoring 구별이 기능 적합성에 영향. D06 editor filesystem update/reimport의 목적은 #8806의 tab close와 다름; A03 editor save/pack 코드. D07 타일 종류/IDs는 bulk 편집 요구와 동일하지 않음.

## Q4. 동일인 다음 행동과 원산출물

M1 T8785 timeline: same-author close 17:10:30Z **권고 17:16:55Z보다 앞**, reopen 18:49:10Z, c1875821247 실수 종료라고 직접 설명. 따라서 closed를 권고 성공으로 세면 시간 역전. 19:32:43Z c1875865603 유용성 언급 뒤 21:48:48Z strip 병용 질문, 01-04 addon 가능성. 공개 스레드 내 60일 원산출물 링크 관측 없음. M2 첫 후속 13:40:07Z 문서 읽음과 이전 오해 명시, 14:02:53Z 설명 개선 필요 유지. T8793 close/reopen event 없음. M3 14:58:12Z prospective 표현, T8803 01-22 제3자 close. S1 c1898495051 과거 문서 열람, c1898529625 syntax 실패, c1898583454 예제 실패/이의. T8903 01-18 14:05:59Z 권고자가 duplicate close. 제공된 zip은 권고자 제작·미열람이며 실제 사용/성공 입증 불가. 
반대로 [P87165](https://github.com/godotengine/godot/pull/87165) #8772 원제안자 31이 자신의 아이디어를 2024-01-14 PR로 연결, Windows 10 test 자기보고, fetch 시 open. 그러나 최초 타인의 공식 기존 기능 링크→기존 대체 채택이 아니라 자체 기능 변경 시도; 이 대조로 URL과 산출물 조건을 독립화. P80284 2023-09-26 merged reload 구현이 있어도 FreeLibrary 예외를 해결하지 못한다. P79561 미병합 clipboard PR은 당시 기능 존재 근거 아님. #9077 c1939016324 놀람과 감사; 다른 사람이 10월 성공 언급하고 P97906 문서 수정 링크(직접 PR은 미열람) → 작성자 적용이 아님. #9222 2025 author PR 언급도 최초 60일 밖. 동명 다른 계정 추정/외부 비공개 이력 없음.

## Q5. 기존 사용·거절

#8784 [c1875965584](https://github.com/godotengine/godot-proposals/issues/8784#issuecomment-1875965584): 이전 Godot 3.x에서 Area 스크립트 사용했으나 반복 부담; TIL은 monitoring/monitorable 구분에 한정, 자기 제안도 제한. #8795 [c1877086925](https://github.com/godotengine/godot-proposals/issues/8795#issuecomment-1877086925): 이미 토글을 알지만 영속 기본값이 다름. #8806 [c1878973166](https://github.com/godotengine/godot-proposals/issues/8806#issuecomment-1878973166), [c1879000003](https://github.com/godotengine/godot-proposals/issues/8806#issuecomment-1879000003): update_file/reimport_files 시도 실패, tab close와 resource save 분리. #8764 [c1879566643](https://github.com/godotengine/godot-proposals/issues/8764#issuecomment-1879566643) duplicate close 후 작성자가 이미지 paste 기능 결여 지적. #8797 c1878924802 과거 AudioDriverWASAPI 이해 부족 진술은 링크 노출 없음. #9222 [c1974879897](https://github.com/godotengine/godot-proposals/issues/9222#issuecomment-1974879897) 새 editor offset 발견을 명시하나 원하는 normalized origin 및 3D 요구에 부족. S1의 사전 열람 명시는 제안 전부터 해당 URL 내용을 알고 있던 반증이다. “모르는 기능 발견”의 분모는 이들 모두를 무지로 가정할 수 없다.

## Q6. 지도 편집 비교 (부분 완료)

[O01 Notes](https://wiki.openstreetmap.org/wiki/Notes) resolving/comments: 신고자 외 로그인한 편집자도 해결/중복/무효로 종료할 수 있고, 재열기가 가능. [O02 API](https://wiki.openstreetmap.org/wiki/OpenStreetMap_API) notes comment/close/reopen: 각각 별도 action과 timestamp를 조회할 수 있다. 이는 상태 변화와 신고자의 실제 해결을 분리해야 한다는 구조 근거다.

개별 원본/API 2건 모두 접근 실패. [O-A #5502267](https://www.openstreetmap.org/note/5502267) 공공 버스 472 노선: [미러](https://resultmaps.neis-one.org/osm-notes-info?uid=20159984) lines 63–67은 타인 close 및 changeset 188644739 후보. [O-B #5597274](https://www.openstreetmap.org/note/5597274) 공공 표지 destination_sign relation: 같은 미러 lines 41–49는 신고자 A, 편집자 B가 close 후 확인 요청과 reopen한 후보. 두 후보 모두 원본 날짜/역할/action 재검증 전에는 확정하지 않는다. 개인 위치·실명·좌표 수집하지 않음. O5502267/OA5502267/O5597274/OA5597274 실패 영수증, OM* 미러. 원출처 직접 사건 0/2, 두 원저작 문서 2/3 목표. 같은 미러 페이지 두 표시는 독립 원저작 두 개가 아니다. 지도 신고자의 성공 기준은 대상 시설/표기 수정이 검증된 것, 유지자의 close는 작업 분류일 수 있음. 도구 기능 권고 성공을 이 사례에서 계량하지 않는다.

## Q7. 제품 효용과 경쟁 관점

발견 엔진의 최소 데이터 모델 후보: proposal_id, actor_id, requirement_id, known_before evidence, exposure_permalink, target_url/version, fit conditions, after_actor/action/date, artifact_ref, disposition; 별개 상태 existence/link presented/read reported/tried reported/observed artifact/substitution/prior unawareness. 하나의 evidence type을 다른 칸에 복제하지 않는다. 원본·URL·개인의 선택·사전 인지에 각각 직접/간접/미확인 표시. 링크 제시 성공의 기준은 버전/동작에 맞는 후보이고, 제안자 기준은 자신의 실제 제약에서 동작, 유지자 기준은 중복 제거/유지 비용/기능 경계, 지도 편집자 기준은 실제 지도 데이터의 수정, 신고자 기준은 문제 해결을 확인할 수 있음. 이 기준을 분리해야 한다.

허용 문장: “특정 필요와 관련 있는 당시 존재 기능의 공식 링크를 제시할 수 있다. 이 40개 공개 대화에서는 링크 후보 3개와 읽기 자기보고 1개가 확인되었다. 기존 기능을 이미 알고 있거나 권고를 받은 뒤도 적합하지 않아 거절할 수 있다.” 금지: “링크 때문에 재발명이 감소했다”, “클릭으로 몰랐던 기능을 발견하고 대체했다”, “closed라서 해결”, “40개 중 37개는 관련 기능이 없다.” 225와의 비교: 225 main same-author patch는 있었으나 권고 URL 없음, 236 URL은 있지만 성공 원산출물 없음. 서로의 결측을 합쳐 완전 사슬 하나를 만들지 않는다. 공개 대화 사례의 빈도는 전 Godot/제품 사용자 모집단의 효과가 아님.

## 비용·대안·추가 분석

1. 가벼운 제품: requirement/version→official link, known/fit/risk를 별도 명시; 비용/채택률 미측정. 후보 존재 자체는 유용할 수 있으나 중복·재발명 감소 주장은 검증 필요.
2. 작업형 제품: 공식 데모의 조작 1개와 현재 버전 설정 조건, near-miss를 함께 제공; 재현 후 작성자가 선택·산출물에 직접 연결할 수 있도록 한다. 실제 클릭 telemetry 없이 읽기를 추정하지 않는다.
3. 증거형 연구: 원본 edited-history 복구 후 outcome을 가린 평가자와 후속 검증자를 분리, 40개 고정 frame을 유지. Q3 재현은 격리 Godot 4.2 판에서 동일 입력으로 baseline/대안 측정; Q4는 공개 작성자 링크만 추가. OSM notes action API 대조. 실제 비용과 실행 성능은 미측정.

읽기 분모: sources.jsonl 100행, counted 54 / 고유 work_id 54(32 본 대화, 1 보강 대화, 8 고정 docs, 5 engine code, 4 PR 기록, 2 process docs, 2 OSM 문서), 비산입 46(빈 창, 메타데이터/중복, 보강 스크린, 실패 등). 고유 저작 수와 독립 성공 사건은 다르다. 22 총수, 대화≥8, 고정≥5, 실제 구현/변경 PR≥4, process≥2 충족. OSM 2/3 및 원본 사건 0/2 미달. 실제 사슬 사건 본 3/6, 별도 1/2; 성공 직접 대체 증거 본 0/3·보강 0/1 관측; 실제 결과 미확인. 독립 원인 판정/코드 실행 없음. 4.2 tag SHA 확인했으나 D01~D08은 개별 문서 경로의 해당 시점 이전 SHA; 작성자의 정확한 판과 역사 HTML 미확인. 모든 근거 위치는 ledger 및 chain/rivals 표 참조.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| 최초 생성 본문·편집 이력 및 해당 시기 실제 페이지 판 불확실; before 봉인 추출 결함 | 사전 인지, 시간순 노출, Q1–Q3 | #8785/#8793/#8803/#8903의 공개 edit history와 2024 문서 빌드, before-correction 대조 | 권고 전에 해당 방법을 사용했거나 모르고 있었다는 동일인 원기록 확보; 문서 실제 해당 판 확인 |
| M1 부분 대체, M2 설명, M3 후속 질문; 성공 원산출물 없음, S1 실패 | 링크가 실제 선택을 바꿨다는 Q3–Q7 판단 | 60일 내 동일 작성자 공개 파일·씬·스크립트 링크; 4.2 SurfaceTool, platform settings, playback 비교 실행 | 해당 버전에서 요구 충족하는 재현과 권고 뒤 동일 작성자의 기존 방법 폐기/교체 산출물, 사전 무지 직접 진술이 모두 연결 |
| OSM 원본 접근 실패 및 최신 dot-control entry 본문 미열람 | Q6 직접 사건 및 작업 입력 동일성 | OSM notes 5502267/5597274 JSON의 action/role/time, 통합/계획 SHA의 dot-control JSON에서 236 항목 비교 및 depends_on 인계 | 두 원본의 타인 close/reopen actor·action 확인; 최신 brief/의존성 동일성 또는 변경 범위 확인 |
