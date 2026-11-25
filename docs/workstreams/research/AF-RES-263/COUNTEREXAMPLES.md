# 경쟁 예측에 대한 반례 및 정정

사전 SCOPE의 강한 예측은 D+에서 "두 일반 멤버 가능"으로 두었고 hardlink 최적화 가능성도 명시했다. 조사 후 D+를 **조건부**로 제한했다. 같은 bytes를 저장한다는 말이 각 멤버에 payload가 있다는 의미는 아니다.

| 사전 가설/오독 | 발견한 반례·원위치 | 수정 후 판정 및 반전 조건 |
|---|---|---|
| -h면 언제나 모든 이름에 regular payload | T09 GNU link04.at, -h에서 nlink1 파일과 symlink가 한 regular/한 hardlink로 저장될 기대; C10 최초 메일 L50–56 실제 배포 실패 보고; C03 역사적 캐시 사례 | R4: 0/1 타입 및 순서 의존, K3 미보장. --hard-dereference 또는 raw header 검수 필요; 고정 판에서 둘 다 type0이면 그 설정만 통과 |
| 링크 보존과 경로 읽기는 충돌 | T03 libarchive 기본 시험 L43–62, target+symlink 보존; S01 L10206–10219 | R2는 보완. 대상 누락/권한/지원 실패면 K2만 철회. K3와의 충돌만 유지 |
| 대상 미동봉이면 어떤 경우도 읽기 실패 | C04 libarchive #1152, 이미 존재하는 link/dir를 유지할 추출 요구 | 빈 루트 가정을 고정해야 필요성이 성립; 사전 파일이나 나중에 받은 target 허용시 달라짐 |
| hardlink의 대상은 symlink처럼 계속 경로를 따라감 | T03,T06 동일 inode 기대, S01 hardlink 예제; T07 target missing writer error | 생성/추출 시 링크할 inode 필요; 완료 후 다른 이름 삭제되어도 남은 이름은 regular. source inode 관계와 archive linkname 구분 |
| hardlink는 항상 size0 | S05 구판 POSIX 재게시 pax -o linkdata 규칙, T06 disk writer 데이터 경우 | ustar 기본 size0과 pax linkdata 예외 구분. POSIX 2024 공식 본문 접근 실패, 현행판 확인 보류 |
| duplicate name 두 개면 원 계약 해결 | S04 getmember last; S03 -k; T11 중복 자기 링크 시험 | 물리 멤버 수/추출 정책이 달라짐. 최종 pathname 하나에서 동시에 두 lstat 유형 불가능 |
| 링크 없는 배포만이 실제 유일한 요구 | C01 명시 보존; C05 백업 요청; C10 실제 배포 요구; C13 Thrift 추출 실패 | 요구는 수신 환경/대상에 따라 분리, 강한 충돌은 동일 단위에서만 |
| 공개 패치 최초판이 그대로 최종 | C11 patch 3672979..., C12 62ff854... 작성자 L22 이전판 철회 | 이전 판을 성공 증거로 사용하지 않음. 수용/빌드/배포 결과 미확인 |
| fetch.txt가 있으면 이미 payload 보존 완료 | B01 complete/valid, B03 APTrust validator fetch 거부, B04 LOC holey bag | fetch는 나중 대상의 명세. 미수신/정상 0바이트/프로필 적용 밖/검증 미실행 분리. 두 기관 정책 다름 |

판정 오류 방지: 원래 목적을 비교하되 같은 inode/경로/멤버/아카이브/수신물 간의 단위 변환을 관계로 남긴다. 실제 실행 및 독립 reviewer 반례 탐색은 미실시. C11·C12의 버전 경계는 작성자의 진술이지 GNU release history를 재확인한 사실이 아니다. GNU 공식 최신판 및 POSIX 원규격은 다음 첫 열람 대상.
