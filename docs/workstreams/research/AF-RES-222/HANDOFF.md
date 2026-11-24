# AF-RES-222 HANDOFF

상태: **PARTIAL** (자료 수 하한 충족, 전거 현행 실레코드 쌍 미확인). 작업자 자체 검토 수행, 독립 검토 미실시. 제품 구현/설치/API 실행/자동 시험 없음.
- 작업 브랜치: work/research-af-res-222
- 실제 착수 SHA: f3895893e32e2c055cefde446d34f1467fa27b4c
- 계획 SHA: fc095c323d0177401d34f1daa7b4d1c529e2351f (착수판 +5, dot-control 변경; 222 실제 RUNNING 항목 및 의존 확인)
- 의존: AF-RES-211 873621fcdeb1bf57c8e6477a0a2c0c9959583a7d, AF-RES-213 425835c2bba66a7002ad281222163024595987f8 (중앙 DONE이나 두 인계의 PARTIAL 조건 유지). 216–218 제외.
- 결과 SHA (HANDOFF 직전): **e6ed02b1ed41eee07a8c81c6728bd434f95fffc8**
- ① d3d0d2c78f8071f39c45a20c0f50411381038ed0 범위·예측
- ② 4d74ad532ff529e2fafd630382aac1a30b211844 원장
- ③ 8cef9a7a2ce052081e7eb5a8554c065c78f7719f 18/36 주관측
- ④ b1ef6d398055d4705ad3aa65101c49f0b781e511 반례/ICU 생성기 정정
- ⑤ e6ed02b1ed41eee07a8c81c6728bd434f95fffc8 RESULT/SELF_CHECK 및 full raw row
- ⑥ HANDOFF 단독 커밋(이 문서 자신의 SHA는 자기참조로 적지 않음)

## 결과와 재열람
대표 파일: RESULT.md (필수 표 1/2, Q1–Q7, 대안, 약점 3), sources.jsonl, names.csv(18), history.csv(6), consumers.csv(36), cards.md, COUNTEREXAMPLES.md, SCOPE.md, SELF_CHECK.md. TABLES.md는 ④ 주관측 중간판이며 최종 판단은 RESULT.md. 정확한 결과 SHA에서 9개 대표 파일 다시 읽음: 54 표 데이터행, Q1–Q7 및 세 약점, BRAKCET 보존, 4.1 실패, ICU correction only 및 0xFFFF, LOC PARTIAL 재확인. RESULT blob 9d657ea88dda2da4c4cad96b42f5158ff49cbd6d; SELF_CHECK blob 4149f3a9fa16174e2ab2d194682f21ce8f5cd762. 비교 결과 착수판 대비 ahead 5/behind 0, 추가 10파일 모두 owned_path. dot-control/다른 작업 미변경. 이 재열람은 GitHub 원문 구조·행·근거 정적 점검이며 독립 평가나 제품 실행 아님.

자료 55행, 직접 성공 35, 산입 32, work_id 25/lineage_id 10. UCD 10, 정책·규격 5, CPython 5, ICU 7, LOC 5. 실패 20, 비산입 성공 3. 6 Unicode 사례 18/18 고정판 관측, 36/36 방향 예상(2 N/A), 실행 0; 13 별칭/소비자. Q6 역사 레코드 전사 n79090096 및 교육 대조 확보, 현행 원본 및 서로 다른 실제 LCCN 2개 미확인. 5.0 직전 4.1 원행 미확인, 6.0/6.1 보존 사본과 원배포 바이트 미대조. UTC 분초 미측정. 실제 consumer binary 미실행. F01–F20 경로/대체 근거 원장 참조.

핵심: 네 correction은 새 code나 Name 교체가 아니라 동일 code의 별도 공식 alias. U+2118/000A/FEFF의 formal aliases는 6.0 0행→6.1 존재; 다른 3 correction은 5.0 최초 관측. 000A <control>은 Name 없음. CPython v3.13.0/15.1.0은 13 alias lookup 예상 수용, name은 원래 Name(000A ValueError/default). ICU 76.1/16.0.0은 I06 고정 생성기에서 correction만 저장, ALIAS choice 네 개 성공 예상, 대조 9개 실패 예상; EXTENDED 합성 이름. 헤더의 U_INVALID_CHAR_FOUND vs I02 U_ILLEGAL_CHAR_FOUND/0xFFFF 불일치. 어느 소비자도 실제 실행한 결과 아님.

## 다음 첫 행동
1. LOC 공식 공개 레코드 접근 가능한 환경에서 n79090096의 010/005/100/400/670 확인. Kate Davis 두 접근점 1951-/1959-를 LOC authority 검색하여 서로 다른 010/URI와 670 원문을 직접 확보; 못 찾으면 가공 사례인지 확인하고 동명 실제 다른 두 개인을 별도 대조로 기록(원래 사례 결측 유지). 현재 id.loc.gov URL 실패는 F18/F19, Twain F06–F08, ad100 F09. 우회 접근·로그인·권한 변경 금지. 두 레코드 확인 후 Q6와 원장 업데이트.
2. 필요 시 Unicode 4.1 공개 배포/NamesList 및 5.0 original NameAliases 원문, 6.0/6.1 zip 내 바이트/행을 비교. 다운로드 실패는 0행으로 표시하지 않는다. 승인일은 정정 제안 문서에서만 확정.
3. 아래 명령은 실행 담당 인계용이며 현 세션에서는 실행하지 않았다. 정확한 판의 기존 환경을 확인하고 맞지 않으면 실행 결과를 혼입하지 말 것. 신규 설치/비용/외부 API 승인 없음.

### Codex 검증 입력 — Python
```bash
python3.13 - <<'PY'
import sys, unicodedata as u
assert sys.version_info[:3] == (3,13,0), sys.version
assert u.unidata_version == '15.1.0', u.unidata_version
rows = [
 (0x01A2,'LATIN CAPITAL LETTER OI',['LATIN CAPITAL LETTER GHA']),
 (0xA015,'YI SYLLABLE WU',['YI SYLLABLE ITERATION MARK']),
 (0x2118,'SCRIPT CAPITAL P',['WEIERSTRASS ELLIPTIC FUNCTION']),
 (0xFE18,'PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRAKCET',['PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRACKET']),
 (0x000A,None,['LINE FEED','NEW LINE','END OF LINE','LF','NL','EOL']),
 (0xFEFF,'ZERO WIDTH NO-BREAK SPACE',['BYTE ORDER MARK','BOM','ZWNBSP'])]
for cp, old, aliases in rows:
    for s in [old or '<control>', *aliases]:
        try: print(hex(cp),'lookup',repr(s),hex(ord(u.lookup(s))))
        except Exception as e: print(hex(cp),'lookup',repr(s),type(e).__name__,str(e))
    try: print(hex(cp),'name',repr(u.name(chr(cp))))
    except Exception as e: print(hex(cp),'name',type(e).__name__,str(e))
    print(hex(cp),'default',repr(u.name(chr(cp),None)))
for s in ['LINE FEED (LF)','<control-000A>','PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRAKCET']:
    try: print('negative/control',repr(s),hex(ord(u.lookup(s))))
    except Exception as e: print('negative/control',repr(s),type(e).__name__)
PY
```
기대: 5개 old→code, 13 alias→code 모두 동일 code, 5 Name 그대로/000A ValueError·default None, LINE FEED (LF) 및 synthetic 이름 KeyError 예상. 실행 기록에 sys.version/UCD, 입력 literal, 반환/예외를 보존. test_ucn.py 고정판 시험은 별도 증거이며 직접 테스트 실행 기록과 구별.

### Codex 검증 입력 — ICU
기존 ICU 76.1 개발 환경에서 `pkg-config --modversion icu-uc` 및 실제 runtime 버전 확인 후 임시 파일로 수행. 설치·컴파일 미실행; 아래는 재현 명령.
```bash
pkg-config --modversion icu-uc
tmp=$(mktemp -d)
cat > "$tmp/af222.c" <<'C'
#include <stdio.h>
#include <unicode/uchar.h>
#include <unicode/uversion.h>
#include <unicode/utypes.h>
int main(void) {
 UVersionInfo v, uv; char a[U_MAX_VERSION_STRING_LENGTH], b[U_MAX_VERSION_STRING_LENGTH];
 u_getVersion(v); u_getUnicodeVersion(uv); u_versionToString(v,a); u_versionToString(uv,b);
 printf("ICU=%s UCD=%s\n",a,b);
 if(v[0]!=76 || v[1]!=1 || uv[0]!=16 || uv[1]!=0) return 2;
 const UChar32 cp[]={0x01A2,0xA015,0x2118,0xFE18,0x000A,0xFEFF};
 const char *s[][8]={
 {"LATIN CAPITAL LETTER OI","LATIN CAPITAL LETTER GHA",NULL},
 {"YI SYLLABLE WU","YI SYLLABLE ITERATION MARK",NULL},
 {"SCRIPT CAPITAL P","WEIERSTRASS ELLIPTIC FUNCTION",NULL},
 {"PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRAKCET","PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRACKET",NULL},
 {"<control>","LINE FEED","NEW LINE","END OF LINE","LF","NL","EOL",NULL},
 {"ZERO WIDTH NO-BREAK SPACE","BYTE ORDER MARK","BOM","ZWNBSP",NULL}};
 const UCharNameChoice choices[]={U_UNICODE_CHAR_NAME,U_CHAR_NAME_ALIAS,U_EXTENDED_CHAR_NAME};
 for(int j=0;j<6;j++) for(int k=0;k<3;k++){
   UErrorCode e=U_ZERO_ERROR; char buf[256]={0};
   int n=u_charName(cp[j],choices[k],buf,sizeof(buf),&e);
   printf("U+%04X choice=%d name len=%d value=[%s] status=%s\n",(unsigned)cp[j],choices[k],n,buf,u_errorName(e));
   for(int z=0;s[j][z];z++){
     e=U_ZERO_ERROR; UChar32 c=u_charFromName(choices[k],s[j][z],&e);
     printf("U+%04X choice=%d lookup=[%s] returned=U+%04X status=%s\n",(unsigned)cp[j],choices[k],s[j][z],(unsigned)c,u_errorName(e));
   }
 }
 for(int k=0;k<3;k++){UErrorCode e=U_ZERO_ERROR;UChar32 c=u_charFromName(choices[k],"<control-000A>",&e);printf("synthetic choice=%d returned=U+%04X status=%s\n",choices[k],(unsigned)c,u_errorName(e));}
 return 0;
}
C
cc "$tmp/af222.c" -o "$tmp/af222" $(pkg-config --cflags --libs icu-uc)
"$tmp/af222"
```
기대: UNICODE old→code 5, ordinary alias 실패; ALIAS correction 4 성공, control/alternate/abbr 9 실패. UNICODE Name 5/000A empty 0, ALIAS correction 이름 4/000A·FEFF empty 0, EXTENDED ordinary Name 5/000A <control-000A>. Synthetic reverse EXTENDED 성공 예상. 없는 이름 구현 U_ILLEGAL_CHAR_FOUND와 0xFFFF를 헤더 U_INVALID_CHAR_FOUND와 대조. 성공은 UErrorCode 우선. 실제 값이 예상과 다르면 RESULT/consumers.csv의 evidence_kind와 판단을 갱신하며 기존 원문 근거는 보존.

## 색인 반영 제안
Object stable code와 NameClaim(literal, role, release, source/line), historical Citation, LookupClaim(consumer/ucd/choice/direction, expected/observed)을 분리. 검색 별칭은 code로 연결, 표시/인용은 각 목적의 원래 Name/판/근거로 연결. NamesList 주석은 explanation/related relation, 동명이인은 identity 후보로 분리. AF-RES-211(현행 alias ≠ 과거 기능), AF-RES-213(공통 parent ≠ child ID)와 조립 가능한 조건부 설계. PARTIAL 상태 그대로 색인; 중앙 진행표는 수정하지 않음.
