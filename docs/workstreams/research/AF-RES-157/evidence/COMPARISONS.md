# 대조와 원작 판독 영수증

## 같은 숫자로 합치면 달라지는 판단

- 실제 각 연구의 전후 결과 방향은 미확인이다. Sketchy의 사람 결과에서 숫자 동률 0은 단일 export 필드를 검사한 값이다. 참가자 원래 저장과 개봉, 직후 저장 사이의 동률·역순·5초/30초 경계는 정의할 수 없다. 연구의 조건·사례·인공 민감도를 [contrasts.csv](../contrasts.csv)에 기록했다. 인공 민감도에서는 주 판정 적격 2쌍과 2tick/다중 허용 판정 적격 2쌍의 합이 같아도 E의 통과와 기존 사례의 분류를 개별 비교해야 한다.
- Delft와 VIS는 access 미확인이다. Sketchy 파일럿은 접근한 파일에서 사건 키와 저장 시계 누락을 관측했다. 어느 연구가 조인은 되고 비교군만 없는지 확인한 실제 사례는 0개다. 실제 연구 참여자의 동일 판 재저장 관측은 미확인이다. 제작 분야의 읽은 필드가 같은 반례와 인공 fixture의 무변경은 별개다.
- 두 저자 사례에서 실제 기능의 시험이 필요한 이유가 다르다. Sketchy의 화살표는 입력 경로를 표현하고 이벤트 인식 조건을 실행하지 않는다. VIS의 막대·비율은 작물/원인 관계 또는 음수 순변화의 자료 정의를 검증하지 않는다. [S42, S44, S56–S58](../sources.jsonl)
- B06의 사례 전사·또 다른 논문 형식은 별도 연구 수로 올리지 않았다. B09의 원문은 자극 데이터베이스가 같은 저자진의 2019 연구에서 왔다고 한다. 연구자가 사전 설명으로 고른 자극은 사후 작품의 원인만으로 모델링할 수 없다. [S34–S38, S49](../sources.jsonl)

## 애니메이션 원파일 실행

| 단계 | 실제 명령 또는 도구 | 입력과 지문 | UTC | 종료 및 누락 |
| --- | --- | --- | --- | --- |
| 3화 및 4화 취득 | `GIT_LFS_SKIP_SMUDGE=1 git clone` 후 `git lfs fetch --include='project-en.blend' --exclude='' origin BEFORE AFTER` | 제작사 공식 GitLab의 아래 프로젝트·SHA, Git 2.52.0 및 LFS 3.6.1 | 2026-11-24 17:13:52–17:15:31Z | 모두 0, 영어 project-en.blend 원본 6개. 바이너리 지문은 [JSON 영수증](production-before-after.json) |
| 검산 | `git show REV:project-en.blend | git lfs smudge > /tmp/.../cut.blend`, `sha256sum`, `blender --background --factory-startup --disable-autoexec /tmp/.../cut.blend --python-exit-code 5 --python replay/animation_timeline.py` | 공개 파일 6개, Blender 4.3.2; Python bpy VSE start/end, source file, channel, mute | 17:15:46–17:15:54Z | smudge 및 Blender 모두 0. 출력 JSON 내용에서 목적 strip만 저장. 프레임 화면·미디어 링크·외부 정보 계측 미실시 |
| 양쪽 원문 | `git diff 8bf0f22^ 8bf0f22 -- scenes/002/002-final.sif`; 파일럿 합산 별도 | Pepper 4화 source XML timing; parent 4fd74aa, commit 8bf0f22 | 17:14:34–17:14:50Z | 0, 24fps canvas의 끝 5s8f→5s12f. 렌더링·3D 효과 자체 미실시 |
| 문헌 원판 | `git clone --depth 1 https://github.com/FrankensteinVariorum/fv-data.git`, `git rev-parse HEAD`, `rg`, `sha256sum` 및 TEI ElementTree | 2debfb706fbe0c1cc2c90b5a75d41b5591aef9c4; S63–S67의 고정 파일 | 17:14:48–17:17:20Z | 0, 1818·1831 Chapter I와 Thomas/MS가 갈리는 C29_app146 실제 원문 직접 비교. 손글씨 이미지 대신 기관 TEI 판독 |
| 규약 지문 | 고정 raw GET 및 `sha256sum` | S52·S54·S55 및 Vega/D3 S57–S58의 버전 URL | 17:17:20–17:17:21Z | 각 curl 0, HTTP 200. 원파일 원본은 Git에 포함하지 않음 |

깃 저장소와 판은 `production-before-after.json`의 `repository`, `before.commit`, `after.commit`으로 재실행할 수 있다. 두 작품의 시간 범위 값은 Blender 읽기 결과, strip 구간은 시작 포함·끝 제외다. 3화의 원 제작 도구 2.79b 대신 4.3.2를 썼고 13프레임 이동 자체의 동기는 확정하지 않았다. 상대 길이와 두 컷의 합은 어느 원점에서도 비교했다. 4화 같은 메타데이터 사례는 `frame_offset`·하위 효과·러시아어 판 및 렌더 프레임까지 불변이라는 뜻을 뒷받침하지 않는다.

## 작업량 계측 범위

지목한 CSV는 15,062,721바이트다. 고정 raw GET의 도구 시간은 1.187371초이고 각각 196개 논리 행과 392개 원 스냅샷 배열을 검사했다. 주 분석은 렌더링 없이 숫자 배열과 버전 구조를 판독한다. 애니메이션 비교는 각각 1MB대 LFS 바이너리만 받았고 전체 3D 제작 파일의 다운로드나 렌더 비용은 추정하지 않았다. 아카이브 접근 실패 시간은 각 URL의 로컬 도구 시도 시간을 뜻하며 이용자의 탐색 비용이나 실험의 과제 시간과 단위가 다르다. 정밀한 조사 인시, 참여자의 링크 이용 시간과 비용, 어떤 링크 표현이 품질을 높이는지는 미측정이다.
