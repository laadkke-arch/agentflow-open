# SELF_CHECK — AF-RES-263 (작성자 자체 점검)

상태 PARTIAL. 원장/표/범위 구조를 원격 고정 결과판에서 다시 읽어 집계했다. 실제 제품 실행, GNU/libarchive 빌드, 외부 reviewer 독립 재현은 하지 않았다. 아래 예상은 모두 미실행이다.

| 질문 | 직접 원근거와 위치 | 자기 결론을 깨는 사례 및 반증 | 미확인·최소 다음 확인 |
|---|---|---|---|
| Q1 | C01 #1034 2018-07-09 16:40:28Z 작성자 댓글; C10 bug#19616 최초 메일 L50–56; C12 L22 | 실제 사용자가 둘 다 같은 목적이라면 C01/C10의 분류 오류; C02 별 배포 필요, C05 외부 source follow; C12 첫 패치 철회 | #1034 초판 edit history 및 target 포함 의도; C10 archive digest와 binary; 두 건의 요청을 원문과 정확판으로 다시 확인 |
| Q2 | T00 struct posix_header offsets; S02 L193–219,300–311; T04 L59–74,162–164; T05 L128–173; T08 L62–76; S05 L998–1002/1318–1463 | pax extension와 type1 linkdata는 단순 zero-data 일반화를 깨뜨림; logical member와 raw extension header 분리 | POSIX 2024 원문 403; GNU 공식판 timeout. 두 URL 재열람, libarchive fixed writer 실제 raw header 비교 |
| Q3 | S01 L10206–10219; T01 L23–71, T02 L23–57, T03 L43–62; T09 link04.at | -h dedup T09, C10; dangling -L fixture T02; pre-existing target C04 다른 boundary | 4셀 0/4 실행; target source 존재·동봉을 분리하고 --hard-dereference 포함 대조, raw header와 final lstat 분리 |
| Q4 | S02 typeflag, T00 1-byte field, S04 L308–323; T11 duplicate self-link, C01/C10 | R2는 두 상위 목적 양립; duplicate name은 두 멤버, extraction order/overwrite 정책에 종속; 다른 이름/시간은 계약 변경 | POSIX 공식 최신판과 실제 extractor duplicate 순서/정책; 다음 실험 2개 멤버의 lstat 각 시점 비교 |
| Q5 | S01 L10235–10327 one/jeden; T06 L131–174,223–257; T07 L27–40; T08 L62–76; T10 L2088–2098 | C03 symlink+hardlink cache 문제, C13 배포 hardlink 실패, S05 pax linkdata 예외 | GNU --hard-dereference 정확판 기존 test/run 미확인; CPython test는 타 도구, 두 실제 이름의 inode/data 검사 |
| Q6 | B01 §1.3/2.1.3/2.2.3/4.2; B02 L55–65; B03 L644–649; B04 L40–48; B05 L61–91; B06 L665–677 | B03 fetch 거부 vs LOC holey 전달; fetch-only 단계와 complete를 같게 보면 틀림 | 실제 기관 receipt/정책 고정판 없음; 발행기관이 적용하는 profile의 checksum, completion receipt 확인 |
| Q7 | S02,C01,T03; S01,C10,T09; assemblies 9행 | 근거 하나 버려도 독립 지지가 남을 수 있음; 상위 목적을 직접 충돌로 기록하면 R2에서 반례 | 제거 9/9 합성, 검증 실측 0/9; 독립 설계자가 recovery URL로 회복 가능한지 별도 판정 |

## 구조 자체 검증 및 수량

- 원격 결과 SHA 7a5d1e257081e9977b0c43f1a3385a99f2701f29에서 7 파일 다시 읽음. JSONL 43행 parse 성공, 고유 산입 34, 규격·작성자 4/4, 구현·시험 14/7, 소비자·결정 10/6, BagIt 6/5. 실패 5, 성공 보조 4. 검색 결과/동일 이슈 patch 반복/재게시 규격은 산입 안 함. GNU 원저작 미러(S01,T00,T09–T13)는 출처와 판 제한 명시, 공식 최신판으로 대체하지 않음. 총 검색 및 재조회 횟수/각 정확 UTC 미기록. 직접 판독 기록 단위는 43행; 소스 그룹별 독립 계보는 여러 행일 수 있음.
- requirements.csv 7 data rows (실제 두 건+계약 5), relations.csv 8 data rows (4셀+hardlink+경계 3), assemblies.md 제거 9행. RESULT 시작 필수 표1 exact 6 columns, 표2 exact 5 columns, 마지막 약점 표3 행; 분모 예정/관측/정상 공석/미확인 및 적용 밖 명시. RESULT Q1~Q7 내용 확인. 동일 t/name/member/type/artifact count 조건 명시.
- GitHub compare base f02dd5d726bb85e4acabfed29c433eacfa31810f → 7a5d1e2: ahead 9, behind 0, 변경 7파일 전부 owned_path. dot-control 변경 없음. SCOPE 결과판 후록 07fc6830106a81cde8edde2545c384724a9569cf는 사전판을 덮어쓰지 않고 append. 최종 compare는 HANDOFF 뒤 별도 조회.
- 원자료 최초 공개 본문에서 두 실제 목적 확보했지만 #1034 수정 이전 이력 미확인. BagIt 기관은 2개(LOC, APTrust), 사례 문서 4개(B03–B06), receipt 0. 필요한 현행 규격/동판 기대시험·원자료 검증을 못 채운 부분을 PARTIAL로 남김.

## Codex에 넘기는 정확한 입력과 명령 (미실행)

승인된 격리 환경에서 GNU tar 1.35(공식 release SHA/digest를 확보해 영수증 기재), libarchive v3.8.4 d114ceee6de08a7a60ff1209492ba38bf9436f79 (test files 고정판; build 여부 별도), CPython v3.13.0 60403a5409ff2c3f3b07dd2ca91a7a3e096839c7 대조. GNU 미러 de72aa0cd63a6bb5d206227a609ff113e5b26171는 과거 source expectation 비교 대상이고 1.35와 동판으로 추정하지 말 것. 설치/빌드가 필요하면 권한 있는 실행자가 별도 승인 받은 환경만 사용. 먼저 binary SHA256, version, OS/filesystem, locale, source SHA, permissions, exit status, stderr를 기록. 테스트 fixture는 아래 일반 상대 링크만, 빈 로컬 temp directory, 신뢰된 자체 생성 archive만 추출. -h는 생성에만 사용.

```sh
# 기존 승인 binary의 절대경로를 사용; 실행자 실제 경로 기록
TAR=/path/to/approved/gnu-tar
BSDTAR=/path/to/approved/bsdtar
"$TAR" --version
"$BSDTAR" --version
sha256sum "$TAR" "$BSDTAR"
uname -a
umask 022
W=$(mktemp -d)
cd "$W" || exit 1
mkdir -p src out
printf 'NOTE\n' > src/note.txt
ln -s note.txt src/current
printf 'HARD\n' > src/a
ln src/a src/b
# B = 5 bytes (NOTE LF); H = 5 bytes (HARD LF)
"$TAR" --format=ustar -cf s0.tar src/current
"$TAR" --format=ustar -cf s1.tar src/note.txt src/current
"$TAR" --format=ustar -chf d0.tar src/current
"$TAR" --format=ustar -chf d1.tar src/note.txt src/current
"$TAR" --format=ustar -chf d1-reverse.tar src/current src/note.txt
"$TAR" --format=ustar --hard-dereference -chf d1-independent.tar src/note.txt src/current
"$TAR" --format=ustar -cf h0.tar src/a src/b
"$TAR" --format=ustar --hard-dereference -cf h1.tar src/a src/b
# 동일 source를 libarchive fixed build로 교차 확인; -L는 생성에서 사용
"$BSDTAR" --format=ustar -cf bs-s0.tar src/current
"$BSDTAR" --format=ustar -cf bs-s1.tar src/note.txt src/current
"$BSDTAR" --format=ustar -L -cf bs-d0.tar src/current
"$BSDTAR" --format=ustar -L -cf bs-d1.tar src/note.txt src/current
"$BSDTAR" --format=ustar -cf bs-h0.tar src/a src/b
# GNU/bsdtar 각각 별도 빈 추출 루트. 매 명령 stdout/stderr/exit code 별도 보관.
for f in ./*.tar; do
  name=$(basename "$f" .tar)
  sha256sum "$f"
  "$TAR" -tvf "$f"
  mkdir -p "out/$name-gnu" "out/$name-bsd"
  "$TAR" -xf "$f" -C "out/$name-gnu"
  "$BSDTAR" -xf "$f" -C "out/$name-bsd"
done
```

아래 Python을 별도 scratch로 저장 후 위 W에서 실행; ustar 고정판 raw header와 final path 결과를 분리한다. JSONL 영수증에 raw 512 block offset, typeflag, size, linkname, payload digest; lstat 종류, inode/dev, readlink, open data digest 또는 errno, extraction return code를 join. pax 확장 적용/중복은 이 단순 ustar parser의 범위 밖; pax 전용 parser 및 x/g record 별도 보완.

```python
from pathlib import Path
import os, stat, json, hashlib
def digest(b): return hashlib.sha256(b).hexdigest()
for p in sorted(Path('.').glob('*.tar')):
    b=p.read_bytes(); i=0
    while i+512<=len(b):
        h=b[i:i+512]
        if not any(h): break
        name=h[:100].split(b'\0')[0].decode()
        prefix=h[345:500].split(b'\0')[0].decode()
        n=int(h[124:136].rstrip(b'\0 ').strip() or b'0',8)
        typ=h[156:157].decode(); link=h[157:257].split(b'\0')[0].decode()
        print(json.dumps(dict(archive=p.name, offset=i, name=(prefix+'/' if prefix else '')+name,
            typeflag=typ, size=n, linkname=link, payload_sha256=digest(b[i+512:i+512+n]))))
        i+=512+((n+511)//512)*512
for d in sorted(Path('out').iterdir()):
    for name in ['current','note.txt','a','b']:
        p=d/'src'/name
        try:
            s=p.lstat(); islink=stat.S_ISLNK(s.st_mode)
            v=dict(root=str(d),name=name,type='symlink' if islink else 'regular' if stat.S_ISREG(s.st_mode) else 'other',
                   dev=s.st_dev,inode=s.st_ino,nlink=s.st_nlink,linkname=os.readlink(p) if islink else None)
            try: v.update(read_sha256=digest(p.read_bytes()))
            except OSError as e: v.update(read_errno=e.errno)
        except OSError as e: v=dict(root=str(d),name=name,lstat_errno=e.errno)
        print(json.dumps(v))
```

예상: s0 current type2/size0/readlink note.txt/open ENOENT, s1 동일 link+open B; d0 type0 size5/open B, d1/reverse는 type0/1 위치 차이 허용(모두 regular final), d1-independent 두 type0/5 expected; h0 두 final inode 동일, h1 각 type0/5 및 다른 inode 예상. 각 반전 기준: s0가 대상 없는 빈 루트에서 B를 제공하면 실제 형식/환경 재검토; s1 link를 잃으면 preserve contract 실패; d0가 type1 또는 link이고 독립 B 없으면 D 실패; d1-independent에 type1이 남으면 해당 도구/판의 제안 철회; h0 inode 다르면 관계 보존 실패; h1 같은 inode면 hard-deref 결과의 관계 재검토. -L의 정확 header dedup 여부는 미확인이라 고정 예상값 대신 원영수증 보고. 모든 결과는 actual/expected 컬럼 별도. 정확판 GNU hard-dereference 공개 시험 원파일도 추가 확보하고 빌드/실행은 승인 범위에서만. BagIt은 원기관 profile/receipt 없이 새 ingest 실험하지 않는다.
