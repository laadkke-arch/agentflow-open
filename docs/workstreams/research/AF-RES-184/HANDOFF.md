# AF-RES-184 HANDOFF

**자체 판정: PARTIAL. 독립 검토: 미수행.** 중앙 상태는 편집하지 않았다. 주표본 8자리와 배포자 카탈로그 SHA256 8개를 확보했지만 동일 고정 스냅샷, 원 buildinfo 및 별도 성공 재빌드 산출 해시를 연결하지 못했다. 공개 실패 로그 4건은 주표본 밖의 비교 자료다. 새 재빌드·JSON-LD 시험은 하지 않았다.

- 저장소/브랜치: laadkke-arch/agentflow-open / work/research-af-res-184
- 계획판: 128f673685ec804c526a38e3f89d4d8a43fcd299
- 시작 foundation: 6fa67328360b02bc7e7270d4ad3300bfe0f286bd
- 고정 의존: AF-RES-176 a347a373cdd46910f2cd2cf53419849ba48ee03a, 중앙 DONE/자체 PARTIAL, HANDOFF 직접 읽음.
- **결과 SHA(본 인계 직전 고정판): 094e290cca25942e8dd29f3992b828b1112f748c**. [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/094e290cca25942e8dd29f3992b828b1112f748c/docs/workstreams/research/AF-RES-184/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/094e290cca25942e8dd29f3992b828b1112f748c/docs/workstreams/research/AF-RES-184/SELF_CHECK.md), [sources](https://github.com/laadkke-arch/agentflow-open/blob/094e290cca25942e8dd29f3992b828b1112f748c/docs/workstreams/research/AF-RES-184/sources.jsonl), frame.csv/packages.csv/runs.csv/claims.csv/SCOPE.md. 이 SHA에서 RESULT/runs/SELF_CHECK를 재열람해 보정 반영을 확인했다. GitHub compare로 시작판 대비 ahead 10, behind 0, 추가 파일 8개 전부 owned_path 이내 확인. HANDOFF 자체는 이 결과판 뒤 마지막 commit(자기 commit SHA를 파일 안에 미리 넣을 수 없음).
- 핵심 사용 가능 근거: A03 세 바이너리 표시→R04 단일 native ID 151245(실제 dpkg-buildpackage exit 2); D06/M02 같은 파일명·크기·SHA256의 언어별 재게시; R01~R04 네 ID 중 build-stage 2건, dependency setup 1, buildinfo 404 1. R02/R04 같은 worker 다른 작업, R03/R04 다른 worker 같은 서비스; 같은 대상 retry 및 조직 독립성 아님. C03 P05/P06은 source 동일·binary version/arch 상이. E03 SRM1575a Al의 NIST/USGS 원보고 값 2개와 한 lab의 복수 method 분기.
- 미확인 분모: 동일 snapshot 8/8, archive index digest 8/8, 원 buildinfo/원 실행 연결 8/8, 대상 rebuild ID/산출 hash 8/8, 두 해시 직접 조인 8/8(최소 두 파일 조건 미달), 동일 키 retry 쌍 미확인, 독립 조직 수 미상, 동일 관측소 측정행의 portal 조인 미확인. 사건 수 0은 실제 0으로 해석하지 않는다. 성공률 미산출.
- 직접 열람 응답 34(31 read, 3 limited), 보수적 고유 실질 문서 29(보조 포함). 원장 70행/36 접근 실패, 엄격 유형 0/6 배포 당시, 0/6 target rebuild, 4/4 규칙(좁게 3/4), 4/2 비교(모두 고정 main frame 밖), 1/4 분야 원보고. **종류별 최소치 미달**. 정확 retrieval clock 및 archive/API raw body hash 미확인. 실패 접근 URL/누락 키는 sources.jsonl F*.
- 실제 체크아웃/workbench 명령은 실행 못 함. GitHub connector 반환 파일 텍스트의 CSV/JSONL/표 자체검산과 커밋 readback만 수행. 외부 binary SHA256 직접 계산 및 signature 검증은 미실시. 새 실행으로 과거 실행 증거를 대신하지 말 것.

## 첫 재개 행동 — Codex Cloud, 기존 공개 원자료만 읽기

실행 전 prerequisite: 네트워크에서 snapshot.debian.org/reproduce.debian.net 실제 원문을 읽을 수 있어야 함. 접근이 안 되면 HTTP/오류, 날짜, URL을 보존하고 blocker로 종료. 인증 우회나 유료 자원, 새 빌드, 운영 변경 금지. 아래는 **미실행 명령**이며 Debian 또는 호환 환경(curl, xz, Python3, coreutils, gpgv, Debian archive keyring 설치되어 있는 환경) 기준. 입력은 사전등록 P01–P08과 UTC 요청시각 2026-11-24T00:00:00Z. 임시 원자료는 /tmp, 저장/commit은 owned_path 아래에만 한다.

```sh
git fetch origin
git checkout work/research-af-res-184
git rev-parse HEAD
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd..HEAD
mkdir -p /tmp/af184 && cd /tmp/af184
date -u +%FT%TZ > checked_utc
curl -fLsS -D imports.headers 'https://snapshot.debian.org/archive/debian/?year=2026;month=11' -o imports.html
url='https://snapshot.debian.org/archive/debian/20261124T000000Z/dists/trixie'
curl -fLsS -D InRelease.headers -w '%{url_effective}\n' "$url/InRelease" -o InRelease | tee effective-url
sha256sum imports.html InRelease
gpgv --keyring /usr/share/keyrings/debian-archive-keyring.gpg InRelease
```

기대 관측: 월별 실제 import 목록과 유효 URL/Release 시각을 대조하여 요청 컷오프 이하 최신 실제 import를 확인. effective URL이 요청 시각만 반환하면 실제 import를 추정하지 말고 목록의 timestamp로 확인. 서명 검증이 성공하면 **확인한 import timestamp**로 BASE를 설정, 동일 Release에 연결된 세 index를 다운로드한다. Release가 다른 경로나 compression 형식을 명시하면 명시된 경로 사용. keyring 부재/서명 실패 시 검증 미확인으로 중단.

```sh
# RESOLVED 값은 실제 import 목록 확인 후에만 설정.
: "${RESOLVED:?set verified snapshot import timestamp}"
BASE="https://snapshot.debian.org/archive/debian/$RESOLVED/dists/trixie"
curl -fLsS -D fixed-release.headers "$BASE/InRelease" -o fixed.InRelease
gpgv --keyring /usr/share/keyrings/debian-archive-keyring.gpg fixed.InRelease
for arch in amd64 arm64; do
  curl -fLsS -D "$arch.headers" "$BASE/main/binary-$arch/Packages.xz" -o "$arch.Packages.xz"
done
curl -fLsS -D Sources.headers "$BASE/main/source/Sources.xz" -o Sources.xz
sha256sum fixed.InRelease *.xz
# InRelease SHA256 절의 정확한 경로·크기·SHA256 대조 후에만 추출
python3 - <<'PY'
import lzma
from pathlib import Path
names={'hello','sed','grep','gzip'}
for p in (Path('amd64.Packages.xz'),Path('arm64.Packages.xz'),Path('Sources.xz')):
    for stanza in lzma.open(p,'rt').read().split('\n\n'):
        fields={}
        for line in stanza.splitlines():
            if line and not line[0].isspace() and ': ' in line:
                k,v=line.split(': ',1); fields[k]=v
        if fields.get('Package') in names:
            print(p, {k:fields.get(k) for k in ('Package','Source','Version','Architecture','Filename','SHA256','Directory')})
            # 실제 Sources Checksums-Sha256 multi-line은 전체 stanza 보존
            Path(p.name+'.selected.txt').open('a').write(stanza+'\n\n')
PY
```

기대 관측: 각 arch 4 동명 바이너리, 4 source stanza(없으면 빈자리), Source 필드의 version 또는 생략시 binary version 규칙을 확인. binNMU는 source/binary version을 분리. 당시 archive Filename에 대한 .deb 원문 SHA256을 직접 계산하고 signed Packages 값과 맞춘다. snapshot file URI는 실제 index Filename과 resolved timestamp에서 만들 것. 기존 후보와 다르면 보정 커밋으로 기존 결과의 이유 보존.

다음은 API 접근 및 ID 획득용 명령. A02 OpenAPI에서 현재 endpoint/filter/pagination을 확인하고, name filter가 source인지 binary인지 실제 응답으로 확인한다. 404면 무작정 임의 ID를 생성하지 않는다.

```sh
for arch in amd64 arm64; do
  API="https://reproduce.debian.net/$arch/api/v1"
  curl -fLsS -D "$arch-list.headers" -G "$API/packages/binary" \
    --data-urlencode seen_only=true --data-urlencode release=trixie \
    -o "$arch-list.json"
  for name in hello sed grep gzip; do
    date -u +%FT%TZ > "$arch-$name.checked"
    curl -fLsS -D "$arch-$name.headers" -G "$API/builds" \
      --data-urlencode "name=$name" --data-urlencode release=trixie \
      -o "$arch-$name-builds.json"
  done
done
sha256sum ./*.json
# 확인된 실제 arch와 build id만 설정해 실행
: "${ARCH:?set verified architecture}" "${BUILD_ID:?set observed build ID}"
API="https://reproduce.debian.net/$ARCH/api/v1"
for suffix in '' /log /artifacts; do
  name="${BUILD_ID}${suffix//\//-}"
  curl -fLsS -D "$name.headers" "$API/builds/$BUILD_ID$suffix" -o "$name.body"
done
sha256sum ./*.body
```

ID·운영자·worker·실제 timestamp·원본 buildinfo URL/서명·dsc hash·expected artifact hash·산출 hash·비교 피연산자를 각 log에서 읽는다. artifacts 목록에서 실제 artifact ID와 endpoint를 확인한 후 A02의 attestation 경로를 요청한다. 원 buildinfo 파일은 log에 표시된 URL, 공식 buildd 기록 및 snapshot 원문 링크로 찾아야 한다(FBP* 경로 후보 실패). binary version·arch·filename과 signed Checksums-Sha256을 동일 archive 파일 hash와 연결한다. 최소 두 package의 원/재빌드 산출 비교, 서로 다른 rebuild record 6개 및 같은 키 retry/독립 운영조직 근거를 찾아 sources/runs/claims 갱신. 동일 ID의 복수 표시를 한 lineage로 처리. 실행 ID나 hash 없으면 unknown. 현재 성공 여부를 확인한다고 새 빌드 실행하지 않음.

환경 비교: USGS NWIS/WQP의 공통 provider와 날짜 범위(legacy WQX2.2이면 2024-03-11 이전 자료)에서 실제 같은 site/activity/time/analyte/method/unit/value 행 1개를 두 원 포털에서 확보. 별도 기관 PT 원보고에서 장비·lab·measurement ID와 같은 reference sample을 확인해 부족한 3개 실제 원자료 이상 추가. E03의 단위와 lab13 분기 유지.

작업 폴더에서 자체검산 실행(아직 미실행):
```sh
git status --short
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd..HEAD
python3 - <<'PY'
import csv,json,pathlib
p=pathlib.Path('docs/workstreams/research/AF-RES-184')
f=list(csv.DictReader((p/'frame.csv').open()))
a=list(csv.DictReader((p/'packages.csv').open()))
r=list(csv.DictReader((p/'runs.csv').open()))
j=[json.loads(l) for l in (p/'sources.jsonl').open()]
assert [x['slot'] for x in f[:8]]==[x['slot'] for x in a]
assert len(a)==8
assert len({x['source_id'] for x in j})==len(j)
keys={x['record_id'] for x in r}|{x['slot'] for x in a}
assert all(not x['parent_id'] or x['parent_id'] in keys for x in r)
print(len(f),len(a),len(r),len(j))
PY
```
현재 고정 결과의 기대 출력 22 8 32 70(추가 원자료 후 변경 가능). raw 파일/증거 확인 없이 검산 성공을 내용 검증이나 독립 검토로 부르지 않는다. workbench.session은 실제 checkout에서 AGENTS/RESEARCH_WORKFLOW의 현재 지침을 읽고 적용하되 owned_path 밖 manifest를 commit하지 않는다.

**색인 제안(중앙 파일 미변경):** AF-RES-184 — 재현빌드 표시/실행/운영자 계보와 증거 수의 하한; Debian lam 3표시→1원ID, grep 언어 미러 및 binNMU 반례, NIST/USGS 분야 비교; 고정 배포–성공 재빌드 해시 join 미충족 PARTIAL. 의존 AF-RES-176; 결과 SHA 094e290cca25942e8dd29f3992b828b1112f748c.
