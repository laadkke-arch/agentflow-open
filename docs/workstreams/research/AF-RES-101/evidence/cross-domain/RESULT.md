# Q7 보조 교정: 이름·주소와 실제 조작

이 파일은 주 표본 8사건의 모집·후속을 읽지 않은 별도 보조 작업자의 교정이다. 공개 요청 사례, 당시 수신 링크, 질문자의 인지/실행을 추가로 관측한 것이 아니다. 주 A/B 효과 분모에 합산하지 않는다.

## 읽은 판과 실행한 판

| 구분 | 고정 원 자료 | 이번 실제 실행 |
| --- | --- | --- |
| Git | v2.45.2, `bea9ecd24b0c3bf06cab4a851694fe09e7e51408`: [정식 restore 매뉴얼](https://github.com/git/git/blob/bea9ecd24b0c3bf06cab4a851694fe09e7e51408/Documentation/git-restore.txt), [t2070 회귀 시험](https://github.com/git/git/blob/bea9ecd24b0c3bf06cab4a851694fe09e7e51408/t/t2070-restore.sh) | 설치된 Git 2.56.1, 연구자 합성 저장소. 상류 t2070 실행은 미실시. |
| FFmpeg | n7.0.1, `af25a4bfd2503caf3ee485b27b99b620302f5718`: [정식 CLI 문서](https://github.com/FFmpeg/FFmpeg/blob/af25a4bfd2503caf3ee485b27b99b620302f5718/doc/ffmpeg.texi), [상류 FATE 조리법](https://github.com/FFmpeg/FFmpeg/blob/af25a4bfd2503caf3ee485b27b99b620302f5718/tests/fate/ffmpeg.mak) | 설치된 FFmpeg 7.1.5-0+deb13u1, 연구자 합성 1초 영상과 두 음성. n7.0.1 빌드·FATE 원 스위트 실행은 미실시. |

4개 고유 상류 파일을 태그와 실제 40자리 SHA에서 직접 열었으며, 같은 파일의 절이나 별칭 주소를 별도 자료로 세지 않았다. [자료별 원장](../cross-domain-sources.jsonl)에 UTC·파일 blob SHA·판·읽은 위치·확인·한계가 있다. [재현 코드](reproduce.py), [결과 영수증](receipt.json), [모든 명령·stdout/stderr·종료값](commands.jsonl)을 함께 보존했다. 실제 실행 시간은 2026-11-23T21:54:25.025045Z–21:54:26.579425Z, 종료값 0, 의미 있는 대조 7/7이었다. 이는 상류 전체 시험 통과나 2024년 사용자 환경 실측을 뜻하지 않는다.

## Git: 이름을 유지하고 대상·기본 원천을 바꾸는 경우

각 행은 독립적으로 `HEAD=base`, `index=index`, `worktree=worktree`인 같은 합성 입력 상태에서 시작했다. 아래 값은 f.txt의 실제 내용이다.

| 조작 | 실제 index / worktree | 원문과 원 시험 위치 | 무엇이 같고 다른가 |
| --- | --- | --- | --- |
| G1 `git restore --worktree -- f.txt` | `index` / `index` | 매뉴얼 L21–26, L58–64; t2070 L37–45 | 기본 원천 index에서 작업 파일만 복원. index 자체는 유지. |
| G2 `git restore --staged -- f.txt` | `base` / `worktree` | 같은 매뉴얼 절; t2070 L47–55, L66–75 | 대상이 index로 바뀌고 생략된 원천도 HEAD로 바뀜. 작업 파일 수정은 유지. |
| G3 `git restore --source=HEAD --staged --worktree -- f.txt` | `base` / `base` | 매뉴얼 L194–213; t2070 L57–64, L77–85 | 두 대상 모두 HEAD로 복원. |
| G4 `git restore -s@ -SW -- f.txt` | `base` / `base` | 매뉴얼 L203–213 | G3의 다른 표기. G3/G4의 HEAD·index·worktree 실제 결과가 같음. |

원 목적이 “작업 파일 변경은 두고 staging만 취소”라면 G1을 시도했다는 이유로 G2를 제거하면 필요한 대안을 잃는다. 원 목적이 “HEAD에서 두 곳 모두 복원”이라면 G3를 시도한 뒤 G4를 새 조작으로 제시할 근거는 없다. 같은 Git 프로그램이나 같은 매뉴얼 URL은 조작 동일성 판정에 충분하지 않다. 반대로 표기가 다르다는 이유도 신규성의 증거가 아니다.

권할 한 줄 예: **“현재 수정은 남기고 staging만 취소하려면 restore의 `--staged` 절을 보세요; `--worktree`와 대상·기본 원천이 다릅니다.”**

반대 관측: 최초 입력에서 index와 worktree가 이미 HEAD와 같았다면 두 조작 모두 눈에 보이는 변화가 없을 수 있다. unmerged index·submodule·다른 source/pathspec 상태에서 이 작은 대조를 그대로 일반화할 수 없다. “파일이 달라졌다”만 관측하면 index 효과를 잘못 판정하므로 두 상태를 별도로 읽어야 한다.

## FFmpeg: 스트림 선택과 복사·인코딩을 분리하는 경우

입력 생성은 `testsrc2=size=16x16:rate=1:duration=1`, 440Hz/880Hz 각각 1초 sine, 명시 `-map 0:v -map 1:a -map 2:a -c:v ffv1 -c:a pcm_s16le source.mkv`다. 실행에 사용한 원본 SHA-256은 `9c33e1baaac0a9354fb5ef0337f15e7bae9f2c5a89fce9e2f467e181d4011874`. Matroska의 생성 메타데이터 때문에 재생성 파일 해시는 달라질 수 있으며 재현 판정은 codec/stream 목록과 압축 packet hash 대조다.

| 실제 조작(공통 무출력·덮어쓰기 플래그 생략) | 실제 출력 | 확인 근거와 의미 |
| --- | --- | --- |
| F1 `ffmpeg -i source.mkv -c copy auto.mkv` | video 1 + audio 1, 총 2 streams, 45 packets | 공식 문서 L274–300, L313–327. copy는 이미 선택된 스트림 처리 방식이다. 두 번째 음성은 자동으로 선택되지 않음. |
| F2 `ffmpeg -i source.mkv -map 0 -c copy all.mkv` | video 1 + audio 2, 총 3 streams, 89 packets | 공식 문서 L1742–1782, FATE L137–143. mapping이 반환 집합을 바꾼다. “모든 음성 유지” 목적에 F1과 다른 조작. |
| F3 `ffmpeg -i source.mkv -map 0 -codec copy alias.mkv` | F2와 같은 3 streams·89개 packet의 stream_index/data_hash 배열 | 문서 L499–517의 `-c`/`-codec`, FATE L168–170. `-codec`이라는 다른 표기는 새로운 처리 단계가 아님. 파일 전체 byte 일치로 과장하지 않음. |
| F4 `ffmpeg -i source.mkv -map 0 -c:v copy -c:a flac transcoded.mkv` | 총 3 streams 유지, codec `[ffv1, flac, flac]`, 21 packets | 문서 L313–327, L499–517; FATE L188–192의 선택+영상복사+음성인코딩 조합. stream 수는 같아도 처리 방식과 압축 결과가 다름. |

원 목적이 “두 음성을 모두 보존”이라면 F1을 실제 써 봤다는 이유로 같은 프로그램인 F2를 제거하면 유효 대안을 잃는다. 반대로 F2를 이미 시도했다면 F3는 같은 입력·stream selection·codec 처리의 별칭이며 새 대안이라는 설명이 틀린다. `-c copy`만 바꾸어도 모든 입력 스트림이 포함된다는 추론은 문서와 실제 F1 출력에 모두 반박된다.

권할 한 줄 예: **“두 번째 음성을 보존하려면 stream selection의 `-map 0` 절을 보세요; `-c copy`는 선택된 스트림의 재인코딩만 막습니다.”**

반대 관측: 입력에 영상·음성이 각 하나뿐이면 F1/F2의 stream 집합이 같을 수 있다. 출력 컨테이너가 추가 스트림을 지원하지 않으면 F2도 목적을 달성하지 못한다. subtitle encoder·unlabeled complex filtergraph에는 문서가 명시한 선택 예외가 있다. 따라서 “같은 호출이라 효과가 같다”도 입력 상태·출력 허용 조건을 확인하기 전에는 확정할 수 없다.

## 사용자·답변자·편집자가 남길 이유

| 관점 | 남길 이유 | 한 줄에 반드시 남길 정보 | 결정을 바꿀 관측 |
| --- | --- | --- | --- |
| 사용자 | 자신의 필수 출력과 보존 조건을 충족 | 바뀌는 대상/입력 상태/인자와 보존되는 것 | 사용자 제약에 반하는 index/worktree 변경 또는 audio 손실이 관측됨. |
| 답변자 | 같은 제품의 다른 조작으로 문제를 해결 | 원래 시도와 다른 인자·처리 단계 | 이미 같은 입력·인자로 실행한 공개 기록이 발견됨. |
| 링크 편집자 | URL/절은 통합하되 동작 차이는 보존 | “같은 문서의 다른 절” 또는 “다른 표기의 같은 호출” | 고정판에서 별칭 의미가 달라지거나 후보 source가 다른 판을 가리킴. |

위 원리는 A/B 비교의 보조 교정일 뿐이다. 공개 질문자의 신규 인지를 이 문서나 합성 실행으로 추정하지 않는다. 정확한 시도값이 없으면 동일성 미확인으로 남기고, “index만 취소하려는가” 또는 “입력에 음성이 몇 개였는가”처럼 판정을 가르는 한 가지를 묻는 것이 가능하다.

## 미실시 상류 재생의 정확한 다음 입력

Git은 고정판 `bea9ecd24b0c3bf06cab4a851694fe09e7e51408`을 별도 clone/build하여 `make -C t T=t2070-restore.sh`로 원 회귀 시험을 실행한다(상류 빌드 의존성을 먼저 충족해야 함). FFmpeg는 고정판 `af25a4bfd2503caf3ee485b27b99b620302f5718`을 빌드하고 공식 FATE sample corpus의 `h264/wwwq_cut.mp4`, `eac3/csi_miami_stereo_128_spx.eac3`, `mov/fcp_export8-236.mov`를 확보한 뒤 `make fate-copy-psp fate-copy-trac3074 fate-copy-trac236 SAMPLES=/absolute/path/to/fate-suite`를 실행한다. 각각 원 sample bytes·빌드 configure·종료값·ref 출력을 기록해야 이번 연구판 합성 대조와 직접 비교할 수 있다.
