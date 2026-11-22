# 공개 dump 보강: 입력과 미실행 명령

## 실제 확인한 범위

공식 문서와 정상 공개 다운로드 안내를 따라 `20261121-002203` snapshot 목록을 직접 열었다(MB-S40–45). 계정 가입·로그인·인증 변경은 하지 않았다. 공개 목록에는 `mbdump-edit.tar.bz2` 약16G, `mbdump.tar.bz2` 약7G와 checksum이 있다.

Python `urllib.request`로 다음 파일에 HEAD를 실행한 결과는 **HTTP 200, Content-Length 17284315658, application/octet-stream**이었다. 이는 해당 dump 파일의 접근성 관측이며 옛 MBID URL의 HTTP 상태와 무관하다.

- 입력 URL: https://data.metabrainz.org/pub/musicbrainz/data/fullexport/20261121-002203/mbdump-edit.tar.bz2
- 고정 snapshot: `20261121-002203`
- 실제 데이터 행 추출: **미실시**. 이 collector는 목록과 HEAD까지만 확인했다. 원 source ID가 dump에서 복원된다고 주장하지 않는다.

## 다음 실행의 최소 입력

편집 IDs `60587125`, `68967621`, `92853437`, `151147443`의 `edit_data` 원행과, 필요한 경우 `recording_gid_redirect` / `release_gid_redirect`의 해당 행이다. 관련 MBIDs는 events.jsonl의 before_ids와 after_ids에 있다. 원문 데이터에는 편집자의 내용이 섞일 수 있으므로 저장소에는 원장을 통째로 넣지 말고 필요한 ID·판·관계의 요약만 남긴다.

아래 명령은 **기록만 했고 실행하지 않았다**. 실제 archive member와 테이블 형식부터 확인해야 한다. 입력 파일은 위 공식 snapshot에서 받은 원본이어야 한다.

```bash
AF_RES_023_MB_BASE='https://data.metabrainz.org/pub/musicbrainz/data/fullexport/20261121-002203'
AF_RES_023_MB_DIR='docs/workstreams/research/AF-RES-023/collectors/musicbrainz/dump-input'
mkdir -p "$AF_RES_023_MB_DIR"
curl --fail --location --output "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2" "$AF_RES_023_MB_BASE/mbdump-edit.tar.bz2"
curl --fail --location --output "$AF_RES_023_MB_DIR/SHA256SUMS" "$AF_RES_023_MB_BASE/SHA256SUMS"
sha256sum "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2"
rg 'mbdump-edit.tar.bz2' "$AF_RES_023_MB_DIR/SHA256SUMS"
tar --list --bzip2 --file "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2"
```

checksum 두 값을 대조하고 archive member가 실제 `mbdump/edit_data`이며 첫 열이 edit ID인 COPY tab 형식임을 확인한 뒤에만 다음 필터를 실행한다. 아직 그 전제는 이 실행에서 검사하지 않았다.

```bash
tar --extract --bzip2 --to-stdout --file "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2" mbdump/edit_data | awk -F '	' '$1 == 60587125 || $1 == 68967621 || $1 == 92853437 || $1 == 151147443 { print }'
```

출력은 각 edit의 원 source/target을 확인하는 입력이며 자동 복원 성공의 증명이 아니다. 특히 current redirect만으로 당시 어느 기능·판·추천 이유였는지를 소급해서 정하지 않는다.
