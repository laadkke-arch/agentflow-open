"""Assemble the SQLite T0 packet from directly read public originals.

Does not fetch or read follow-up bodies. Never run to overwrite the frozen
packet after the global seal; corrections belong in separate audit files.
"""
import csv
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
meta = json.loads((P / 'root-metadata.json').read_text())
replies = {x['case_id']: x for x in json.loads((P / 'first-reply-metadata.json').read_text())}
now = datetime.now(timezone.utc).isoformat()
base = 'cecbfb981b9a7ccfd59f7bc40a23445a19d020fa'
sql371 = '57acbb1380e3b51476aa8c71d1a881821f8ad5ff'
sql370 = '315e3122c37b2dbe0fb7b3a4c3b9b6961e3bda96'
sql340 = '384f5c26f48b92e8bfcb168381d4a8caf3ea59e7'
pg141 = '0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda'
node502 = '60a022c511a37788e652c271af23174566a80c30'
def gh(repo, ref, file): return 'https://github.com/'+repo+'/blob/'+ref+'/'+file
H = gh('sqlite/sqlite', 'version-3.37.1', 'src/sqlite.h.in')
A = gh('sqlite/sqlite', 'version-3.37.1', 'src/attach.c')
G = 'https://gcc.gnu.org/onlinedocs/gcc-11.2.0/gcc/Overall-Options.html'
T = gh('sqlite/sqlite', 'version-3.34.0', 'test/altertab.test')
L = gh('sqlite/sqlite', 'version-3.34.0', 'src/alter.c')
R = gh('sqlite/sqlite', 'version-3.37.0', 'src/sqlite.h.in')
J = gh('sqlite/sqlite', 'version-3.37.0', 'src/pager.c')
B = gh('sqlite/sqlite', 'version-3.37.1', 'src/sqliteInt.h')
V = gh('sqlite/sqlite', 'version-3.37.1', 'test/autovacuum.test')
PG = gh('postgres/postgres', 'REL_14_1', 'doc/src/sgml/maintenance.sgml')
N = gh('TryGhost/node-sqlite3', 'v5.0.2', 'README.md')

sources=[]
def doc(i, cases, repo, sha, path, date, loc, observed, limit, count=True, kind='provider_document', link=None):
    url=gh(repo,sha,path) if repo else path
    sources.append({'id':i,'related_q':['Q2','Q3','Q5'],'case_ids':cases,'url':url,'published_or_revised':date,'fixed_version':sha,'checked_utc':now,'read_locations':loc,'observed':observed,'limitations':limit,'producer':repo or 'GNU GCC','lineage':(repo or 'GNU GCC')+':'+path,'count_in_minimum':count,'count_reason':'직접 읽은 당시 제공자의 독립 문서/테스트' if count else '같은 저작의 판 비교 또는 구현 보강; 엄격 문서 최소수에는 제외','kind':kind,'message_link':link or url})
doc('S-D01',['S01','S02','S05','S08'],'sqlite/sqlite',sql371,'src/sqlite.h.in','2021-12-30T15:30:28Z','L1749–1789; L3351–3400; L4370–4407; L5117–5141','공개 API 계약: 생성 플래그, 연결/statement 직렬화, host parameter와 reset의 범위.','비교판은 OP가 명시하지 않은 환경의 실제 설치판이 아님. 성능 향상·사용 성공을 보증하지 않음.',link=H)
doc('S-D02',['S01'],'sqlite/sqlite',sql371,'src/attach.c','2021-12-30T15:30:28Z','attachFunc L153–167','ATTACH가 연결의 openFlags를 읽고 URI 처리를 거쳐 BtreeOpen에 넘긴다.','구현 정적 판독이며 작성자의 프레임워크나 플랫폼 실행은 하지 않음.',False,'provider_implementation',A)
doc('S-D03',['S02'],None,'GCC 11.2.0',G,'GCC11.2.0 versioned manual; exact page publication/revision date not observed','§3.2, -o file (web L199–203)','-o가 컴파일의 주 산출 파일 이름을 지정한다. 최초 로그의 mysql과 실행 대상 ex1.db를 구별할 근거.','OP의 GCC 실제 버전은 미상; 문서의 예제에서 실행 성공을 추론하지 않음.',link=G)
doc('S-D04',['S03'],'sqlite/sqlite',sql340,'test/altertab.test','2020-12-01T16:14:00Z','tests 9.0–9.5, L276–305','없는 테이블을 참조하는 view 때문에 무관한 rename도 실패하는 공식 테스트가 있다.','읽은 테스트이며 이 세션에서 구판 바이너리를 실행하지 않음. 사용자 migration 전체 성공의 증거 아님.',kind='provider_test',link=T)
doc('S-D05',['S03'],'sqlite/sqlite',sql340,'src/alter.c','2020-12-01T16:14:00Z','renameTableTest L1698–1740','legacy 플래그가 꺼졌을 때 view SELECT를 준비하고 오류를 전파한다.','legacy 사용이 다른 참조를 어떻게 바꾸는지까지 이 절 하나로 보증하지 않음.',False,'provider_implementation',L)
doc('S-D06',['S04'],'sqlite/sqlite',sql370,'src/sqlite.h.in','2021-11-27T14:13:22Z','Last Insert Rowid, L2430–2487 특히 L2476–2477','INSERT 뒤 rowid는 나중 rollback 여부와 구별되므로 rowid 출력은 commit 영수증이 아니다.','S-D01과 같은 API 문서의 과거판; 별도 저작으로 증식하지 않음.',False,'provider_document_version',R)
doc('S-D07',['S04'],'sqlite/sqlite',sql370,'src/pager.c','2021-11-27T14:13:22Z','pager settings design comment L3503–3549','rollback/WAL의 FULL 의미와 MacOSX full-fsync 플래그는 구별된다.','원 구현 안의 설계 설명. iOS 장치의 실제 flush 준수·당시 손실 원인·commit 여부는 별도 미확인.',True,'provider_design_document',J)
doc('S-D08',['S06'],'sqlite/sqlite',sql371,'src/sqliteInt.h','2021-12-30T15:30:28Z','custom-header instruction L184–208','SQLITE_CUSTOM_INCLUDE가 사용자 헤더를, _HAVE_SQLITE_CONFIG_H가 configure 헤더를 포함하는 경로를 정의한다.','OP의 정확한 배포판/빌드명령이 없어 이 비교판을 실제 환경과 동일시하지 않음.',True,'provider_design_document',B)
doc('S-D09',['S06'],'sqlite/sqlite',sql371,'tool/mksqlite3c.tcl','2021-12-30T15:30:28Z','copy_file include-handling L220–250','amalgamator는 중복 include를 주석 처리할 수 있다.','OP의 config.h가 바로 이 분기로 빠졌다는 직접 증거는 없음.',False,'provider_implementation')
doc('S-D10',['S07'],'sqlite/sqlite',sql371,'test/autovacuum.test','2021-12-30T15:30:28Z','tests autovacuum-1.*, L32–69; 7.1–7.3 L610–654','auto_vacuum=1에서 삭제 commit 뒤 파일 페이지 수가 감소하는 테스트를 읽었다.','이번 실행의 측정값이 아닌 저장된 테스트 기대값; 모든 패턴·incremental을 보증하지 않음.',True,'provider_test',V)
doc('S-D11',['S07'],'postgres/postgres',pg141,'doc/src/sgml/maintenance.sgml','2021-11-08T21:58:24Z','routine-vacuuming/recovering-disk-space L156–194','보통 VACUUM도 빈 끝 페이지와 lock 조건에서 OS에 공간을 반환할 수 있고 autovacuum은 VACUUM FULL을 하지 않는다.','현재 14 웹 문서를 탐색에 사용한 뒤 REL_14_1 원문으로 재확인. 다른 PostgreSQL 판/실제 운영값은 미확인.',True,'provider_document',PG)
doc('S-D12',['S08'],'TryGhost/node-sqlite3',node502,'README.md','2021-02-15T14:42:52Z','Usage L24–46; feature parameter binding L51','Node binding의 prepare INSERT (?)와 stmt.run(value) 예제가 SQL 구문과 JS 값을 분리한다.','OP의 패키지판은 미상. 예제 하나로 NOT NULL 전체 입력·실행 성공을 보증하지 않음.',True,'provider_document',N)

def cand(i, use, source, link, version, status):
    s=next(s for s in sources if s['id']==source)
    return {'id':i,'use':use,'url':s['url'],'message_link':link,'version':version,'source_id':source,'t0_verdict':status}
cases=[
{'id':'S01','hash':'d5ac4dc797','goal':'C 코드의 ATTACH가 없는 파일을 새 DB로 생성하게 한다.','inputs':'메모리 연결, 존재하지 않는 _thingie, SQLITE_OPEN_READWRITE, ATTACH SQL','outputs':'새 DB 파일과 성공 반환값','version':'OP 미명시; 비교 SQLite 3.37.1','platform':'C; Unix형 shell 경로, 정확한 OS 미상','actors':'동기 C 호출자와 같은 sqlite3 연결; CLI는 별도 대조','requirements':[('required','존재하지 않는 대상 DB의 생성','첫 두 bullet 및 끝 질문1–2'),('required','C 경로에서도 ATTACH 사용','끝 질문2'),('unknown','실제 runtime 판과 VFS','본문에 없음'),('conflicting','예제 :memory:와 첫 로그의 저장소 경로가 다름','C zRepoDb 선언과 첫 run log')],'observed_configuration':'SQLITE_OPEN_READWRITE는 현재 코드 사실이지 변경 금지가 아님.','variable':'대상이 없으면 생성해야 하는가','question':'대상 파일이 없을 때 ATTACH가 새 DB를 만들어야 하나요?','utility':'already_stated','uses':[cand('A','연결에 CREATE를 허용한 뒤 ATTACH로 새 파일 생성','S-D02',A,'3.37.1','supported'),cand('B','READWRITE만 유지해 이미 있는 파일만 ATTACH','S-D01',H,'3.37.1','conflict')],'I':f'제시한 코드에는 CREATE가 없습니다. 새 파일이 필요하므로 연결을 READWRITE|CREATE로 열고 ATTACH를 확인하세요. ATTACH는 연결 플래그를 받습니다. {A}','C':f'새 파일 생성이 필요하면 READWRITE|CREATE, 기존 파일만 허용하면 READWRITE를 씁니다. 현재 요청은 첫 경우입니다. {H} {A}','source_ids':['S-D01','S-D02'],'exposure':[{'kind':'search_snippet','url':'https://sqlite.org/forum/forumpost/76963f0026b6b12a','content_seen':'첫 답이 open_v2와 ATTACH의 오류검사를 구별하라는 문장. 해결 전체는 미열람.','effect':'strict pre-outcome comparison excluded; original-version evidence remains confirmed'},{'kind':'pre_first_reply_edit','url':'https://sqlite.org/forum/forumpost/d5ac4dc797?t=s&unf','content_seen':'forumpost가 00:53:57 편집판을 표시했다. 이후 raw에서 00:49:41 원판을 분리했다.','effect':'편집은 첫 답 이전; 원판 hash는 raw 기준'}]},
{'id':'S02','hash':'d822264743','goal':'기존 SQLite DB를 C 프로그램에서 열어 읽는다.','inputs':'mysql.c, gcc -o mysql, ex1.db 경로','outputs':'C 프로그램 실행 및 SQLite 연결','version':'OP 미명시; SQLite 3.37.1/GCC 11.2 문서 비교','platform':'Linux형 bash와 gcc; 정확 OS판 미상','actors':'shell이 C 실행파일을 실행하고 C가 DB파일을 연다','requirements':[('required','C로 기존 DB를 읽는다','첫 단락과 C main'),('required','실행 오류를 고친다','질문과 마지막 run log'),('unknown','실제 데이터 조회 SQL','use the database 주석 뒤 구현 없음')],'observed_configuration':'파일 실행 권한을 이미 부여했다는 것은 작성자 보고. DB파일 실행을 요구조건으로 삼지 않음.','variable':'-o로 만든 실행파일 이름','question':'gcc의 -o 뒤에 지정해 생성한 실행파일 이름이 mysql인가요?','utility':'already_stated','uses':[cand('A','생성한 mysql 프로그램을 실행하고 ex1.db는 sqlite3_open의 입력으로 사용','S-D03',G,'GCC11.2/SQLite3.37.1','supported')],'I':f'로그는 -o mysql로 만든 뒤 ex1.db를 실행했습니다. ./mysql을 실행하고 ex1.db는 sqlite3_open의 파일 인자로 두세요. 아직 코드는 연결만 열며 SELECT는 없습니다. {G}','C':f'mysql이 컴파일 결과라면 ./mysql을 실행합니다. ex1.db가 데이터 파일이면 실행하지 않고 sqlite3_open에 넘깁니다. 두 종류는 현재 로그로 구별됩니다. {G}','source_ids':['S-D01','S-D03'],'exposure':[]},
{'id':'S03','hash':'c9ec666ab9','goal':'테이블 열 타입과 연관 view의 계산식을 함께 migration한다.','inputs':'3.34.0; t(i integer), v; 임시 새테이블, legacy_alter_table=off','outputs':'t(i text) 및 문자열 반복 view, transaction commit','version':'OP SQLite3.34.0; 같은 판 비교','platform':'SQL/CLI; OS 미상','actors':'단일 migration transaction, rename 시 schema 해석','requirements':[('required','열 integer를 text로 바꾸고 view를 문자열 반복식으로 교체','Desired schema migrations 주석'),('required','기존 데이터 전달','step5 INSERT SELECT CAST'),('unknown','legacy_alter_table=OFF를 계속 유지해야 하는가','OFF는 예제 설정; 변경 금지 문장은 없음'),('unnecessary','외래키 관련 단계는 예제에서 n/a','steps1,10,12')],'observed_configuration':'OFF를 금지/필수 제약으로 자동 승격하지 않음. view는 step9에서 원래 교체할 예정.','variable':'legacy 모드를 끌 수 없는 제약 여부','question':'마이그레이션 중에도 legacy_alter_table=OFF를 반드시 유지해야 하나요?','utility':'does_not_change_safe_primary_use','uses':[cand('A','이미 교체할 view를 rename 전에 제거하고 뒤에 재생성','S-D04',T,'3.34.0','supported'),cand('B','legacy 모드로 rename의 view 검사를 바꿀 수 있으나 전체 의미는 추가 확인','S-D05',L,'3.34.0','unknown')],'I':f'원래 바꿀 view를 rename 전에 제거하고 새 테이블 이름이 확정된 뒤 재생성하는 순서를 검토하세요. 3.34.0 테스트는 깨진 view가 rename을 막음을 보입니다. {T}','C':f'OFF를 유지해야 하면 view를 먼저 제거·나중 재생성합니다. 바꿔도 되면 legacy 경로도 후보지만 다른 참조 의미까지 확인해야 합니다. {T} {L}','source_ids':['S-D04','S-D05'],'exposure':[]},
{'id':'S04','hash':'feed150c20','goal':'iOS 강제 재시작 뒤 이미 넣은 행의 보존 경계를 이해한다.','inputs':'트랜잭션 INSERT, 출력 rowid; DELETE journal, FULL sync','outputs':'재부팅 뒤 데이터/rowid 복구','version':'OP3.37.0; 같은 판','platform':'iPhone6S, iOS12.3','actors':'삽입 호출자, transaction, OS/장치 강제 재시작','requirements':[('required','강제 재시작 뒤 데이터 보존 범위를 확인','첫 단락'),('unknown','손실 행 transaction의 COMMIT 성공 여부','rowid 출력만 있으며 COMMIT 없음'),('unknown','각 행별 또는 묶음별 보존 요구','본문에 없음')],'observed_configuration':'FULL 설정은 관측 환경. durable COMMIT가 성공했다는 진술로 대체하지 않음.','variable':'손실 행의 COMMIT가 재시작 전에 성공 반환했는가','question':'사라진 행을 포함한 트랜잭션의 COMMIT가 강제 재시작 전에 성공을 반환했나요?','utility':'answer_needed_to_split_diagnosis_not_sufficient_to_prove_cause','uses':[cand('A','commit 전 INSERT/rowid를 rollback 가능한 중간 상태로 해석','S-D06',R,'3.37.0','unknown'),cand('B','commit 성공 후 손실이면 sync/OS 경계 조사로 보류','S-D07',J,'3.37.0','unknown')],'I':f'원인 판정은 보류합니다. rowid가 나와도 나중에 rollback될 수 있으므로 보존 실패라고 확정하려면 해당 COMMIT 결과가 필요합니다. {R}','C':f'COMMIT 전이면 rowid 출력만으로 보존을 기대할 수 없습니다. 성공 COMMIT 뒤라면 장치·sync 경계 원인을 더 확인해야 합니다. {R} {J}','source_ids':['S-D06','S-D07'],'exposure':[]},
{'id':'S05','hash':'a57b1695d4','goal':'statement를 재사용하면서 reset/clear 비용을 다른 스레드로 옮긴다.','inputs':'같은 연결의 다른 연산과 background reset/clear','outputs':'안전한 재사용; 성능 향상은 바람','version':'OP미명시; SQLite3.37.1 비교','platform':'C API multithreading; OS/빌드 미상','actors':'main이 exec/prepare/step; 다른 thread가 reset/clear; 같은 connection','requirements':[('required','두 thread의 같은 connection 접근이 안전','첫 글 마지막 질문'),('preference','reset/clear 비용 감소와 재사용 성능','처음 두 단락'),('unknown','실효 threading mode','본문에 없음'),('unknown','같은 statement에 대한 논리적 작업 겹침','다른 operations만 명시')],'observed_configuration':'같은 연결이라는 사실은 이미 명시됨. 성능 개선은 mutex 안전성과 별개.','variable':'연결의 실효 serialized mode 여부','question':'그 연결은 FULLMUTEX 등을 포함해 실제로 serialized 모드로 열렸나요?','utility':'answer_needed_to_split_technical_permission','uses':[cand('A','serialized mode의 연결 mutex 아래 서로 다른 thread 호출','S-D01',H,'3.37.1','unknown'),cand('B','multi-thread/no-mutex이면 같은 연결 접근을 앱에서 직렬화','S-D01',H,'3.37.1','unknown')],'I':f'현재 설정만으로 안전 승인은 보류합니다. 같은 연결을 동시에 쓰므로 실제 threading mode를 확인해야 하며, mutex 안전성이 성능 향상을 보장하지는 않습니다. {H}','C':f'serialized이면 연결·statement 접근을 SQLite가 직렬화합니다. multi-thread/no-mutex이면 같은 연결을 앱이 직렬화해야 합니다. 어느 쪽도 성능 향상의 증거는 아닙니다. {H}','source_ids':['S-D01'],'exposure':[]},
{'id':'S06','hash':'aaa53d0db4','goal':'여러 빌드 시스템에서 config.h로 SQLite 설정을 유지한다.','inputs':'동일 디렉터리 config.h; include가 주석 처리된 소스','outputs':'설정 헤더의 정상 반영','version':'OP미명시; SQLite3.37.1 비교','platform':'C build; OS/compiler 미상','actors':'빌드 시스템, amalgamation 또는 원본 소스, 전처리기','requirements':[('required','외부 헤더로 설정 전달','첫 문장'),('prohibited','여러 빌드 시스템을 쓰는 이유를 다시 묻지 않음','Dont ask why 문장'),('unknown','정확한 버전과 소스 배포 형태','본문에 없음')],'observed_configuration':'config.h를 쓰던 방식을 선호한다고 읽되 특정 매크로 변경 금지로 만들지 않음.','variable':'amalgamation과 split source 중 무엇을 컴파일하는가','question':'컴파일하는 것은 배포된 sqlite3.c 한 파일인가요, 원본 src/*.c 파일들인가요?','utility':'narrows_path_but_version_still_missing','uses':[cand('A','SQLITE_CUSTOM_INCLUDE로 사용자 헤더를 명시','S-D08',B,'3.37.1','unknown'),cand('B','split-source configure 경로에서 _HAVE_SQLITE_CONFIG_H로 config.h 포함','S-D08',B,'3.37.1','unknown')],'I':f'설치판과 소스 형태가 없어 기존 include가 사라진 원인은 보류합니다. 비교판 3.37.1에는 SQLITE_CUSTOM_INCLUDE의 별도 헤더 경로가 있습니다. {B}','C':f'sqlite3.c 한 파일을 빌드하면 SQLITE_CUSTOM_INCLUDE 경로를 검토하고, 원본 src/*.c라면 _HAVE_SQLITE_CONFIG_H의 config.h 경로를 확인하세요. 정확한 판도 필요합니다. {B}','source_ids':['S-D08','S-D09'],'exposure':[]},
{'id':'S07','hash':'0aa199be4f','goal':'SQLite와 PostgreSQL autovacuum의 공간 반환 차이를 확인한다.','inputs':'PG는 OS 반환 없음, SQLite는 끝 페이지 이동·반환이라는 주장','outputs':'두 방식의 정확한 비교','version':'OP미명시; SQLite3.37.1/PG14.1 비교','platform':'개념 비교; 배포 OS/실제 설정 없음','actors':'PG daemon과 SQLite transaction/mode; 동일한 실행 주체로 취급하지 않음','requirements':[('required','OS 공간 반환 여부를 비교','전체 본문 마지막 질문'),('unknown','SQLite FULL/INCREMENTAL 중 의도한 모드','본문에 없음'),('unnecessary','특정 운영 인스턴스의 설정','최초 질문은 일반 비교; 운영 실험 요청 없음')],'observed_configuration':'PG는 절대 반환하지 않는다는 첫 주장을 요구조건이 아니라 검증 대상 명제로 코딩.','variable':'PostgreSQL의 일반 VACUUM과 VACUUM FULL 중 어느 사용인가','question':'말씀하신 PG 작업은 autovacuum의 일반 VACUUM인가요, 별도로 실행한 VACUUM FULL인가요?','utility':'already_stated_and_not_needed_for_conceptual_answer','uses':[cand('A','PG autovacuum의 일반 VACUUM과 SQLite FULL의 파일축소를 비교','S-D11',PG,'PG14.1/SQLite3.37.1','supported'),cand('B','별도 PG VACUUM FULL의 전체 재작성/축소와 비교','S-D11',PG,'14.1','conflict')],'I':f'PG가 OS에 전혀 반환하지 않는다는 부분은 수정해야 합니다. 보통 VACUUM도 끝 페이지가 비고 lock 조건이 맞으면 반환할 수 있습니다. {PG}','C':f'PG 일반 VACUUM이면 빈 끝 페이지에서 반환하는 예외가 있고, VACUUM FULL이면 재작성해 축소합니다. autovacuum은 후자를 실행하지 않습니다. SQLite FULL의 축소와 비교하세요. {V} {PG}','source_ids':['S-D10','S-D11'],'exposure':[]},
{'id':'S08','hash':'16b9a233ab','goal':'HTML form 값을 Node.js SQLite INSERT에 전달한다.','inputs':'req.body.duration, JS 변수, VALUES(duration), bind array [C], 여러 NOT NULL 열','outputs':'animalStream 행 삽입','version':'OP package/SQLite미명시; node-sqlite3v5.0.2/SQLite3.37.1 비교','platform':'Node.js Express; OS/Node판 미상','actors':'form POST → JS handler → asynchronous db.run callback','requirements':[('required','form 필드를 테이블 값으로 삽입','첫 문장, HTML form, handler'),('required','NOT NULL 필드에 필요한 값을 제공','CREATE TABLE 선언'),('unknown','실제 사용 package판','본문에 없음')],'observed_configuration':'bare duration은 SQL 문자열 안 식별자이고 JS 변수와 자동 연결되지 않음. 값 바인딩 수정만으로 모든 NOT NULL 열 문제가 끝난다고 하지 않음.','variable':'duration이 JS 값인가 SQL 식별자인가','question':'duration에 넣으려는 것은 req.body.duration의 값인가요?','utility':'already_stated','uses':[cand('A','? 또는 명명 parameter에 JS 값을 바인딩하고 필수 열을 함께 채움','S-D12',N,'v5.0.2','supported'),cand('B','VALUES(duration)을 JS 변수 전달로 그대로 사용','S-D01',H,'3.37.1','conflict')],'I':f'VALUES(duration)은 JS 변수를 읽지 않습니다. ?에 duration 값을 바인딩하고 나머지 NOT NULL 열도 함께 채우세요. 바인딩 예제: {N}','C':f'JS 값이면 ? 등 parameter로 바인딩합니다. SQL 식별자를 의도했다면 현재 INSERT에는 그 값을 읽을 문맥이 없습니다. 이 글의 req.body 값에는 첫 경로가 맞습니다. {N}','source_ids':['S-D01','S-D12'],'exposure':[]},
]
initial=[]; frozen=[]
for x in cases:
    m=meta[x['hash']];url='https://sqlite.org/forum/artifact/'+m['artifact'];cid=x['id']
    req=[{'id':'R'+str(i+1),'kind':k,'text':t,'url':url,'locator':loc} for i,(k,t,loc) in enumerate(x['requirements'])]
    original={'identifier':m['artifact'],'status':'confirmed','evidence':'공식 raw artifact의 SHA3-256이 artifact ID와 일치; D시각/최초 root H/U와 first reply G/I 관계를 확인','url':m['url'],'hash_method':'raw artifact SHA3-256 and W-delimited full-body SHA256','raw_sha256':m['raw_sha256'],'body_sha256':m['body_sha256'],'full_body_read':True,'prior_to_first_reply':True}
    row={'case_id':cid,'family':'S','title':m['title'],'root_url':url,'root_locator':'Fossil artifact W 본문 전체; body-locations.json의 행 위치','submitted_utc':m['submitted_utc']+'Z','timestamp_kind':'Fossil artifact D time; official timeline confirms root event; client wall clock not used','author':m['author'],'original_version':original,'first_reply_utc':replies[cid]['headers']['D']+'Z','goal':x['goal'],'inputs':x['inputs'],'outputs':x['outputs'],'version':x['version'],'platform':x['platform'],'actors':x['actors'],'requirements':req,'observed_configuration':x['observed_configuration'],'candidate_uses':x['uses'],'missing_variable':x['variable'],'frozen_question':x['question'],'question_utility':x['utility'],'input_sha256':m['body_sha256'],'exposure':x['exposure'],'strict_preoutcome_eligible':not any(e['kind']=='search_snippet' for e in x['exposure']),'sources':['S-'+cid]+x['source_ids'],'reader':'/root/sqlite, inherited GPT-6 Astra Pro; same author T0/T1; not independent duplicate coding'}
    initial.append(row)
    msg={k:x[k] for k in ['I','C']};msg['Q']=x['question']
    for k,v in msg.items():
        assert len(v)<=300,(cid,k,len(v))
    frozen.append({'case_id':cid,'input_sha256':m['body_sha256'],'precommit_base_sha':base,**msg,'candidate_ids':[c['id'] for c in x['uses']],'candidate_source_ids':x['source_ids'],'created_utc':now,'reader':'/root/sqlite','followups_read_before_freeze':bool(x['exposure'] and any(e['kind']=='search_snippet' for e in x['exposure'])),'message_chars':{k:len(v) for k,v in msg.items()},'not_actually_sent':True})
    sources.append({'id':'S-'+cid,'related_q':['Q1','Q2','Q3'],'case_ids':[cid],'url':url,'published_or_revised':m['submitted_utc']+'Z','fixed_version':m['artifact'],'checked_utc':m['read_utc'],'read_locations':'W body whole; exact phrase positions in body-locations.json','observed':x['goal']+' '+x['observed_configuration'],'limitations':'최초 글의 당사자 보고이며 실제 환경 실행은 아님. 후속본문은 아직 열지 않음.'+(' S01은 검색 답 한 문장 노출로 엄격 선후 비교에서 분리.' if cid=='S01' else ''),'producer':'SQLite Forum / '+m['author'],'lineage':'forum-thread:'+m['artifact'],'count_in_minimum':True,'count_reason':'고유 최초 요청/대화 1건; 수정판·댓글은 별도 원문으로 늘리지 않음','kind':'conversation'})

selected_hashes={x['hash'] for x in cases}
for h,m in meta.items():
    if h in selected_hashes or 'artifact' not in m: continue
    sources.append({'id':'S-X-'+h,'related_q':['Q1'],'case_ids':[],'url':'https://sqlite.org/forum/artifact/'+m['artifact'],'published_or_revised':m['submitted_utc']+'Z','fixed_version':m['artifact'],'checked_utc':m['read_utc'],'read_locations':'W body whole; root-metadata.json contains raw/body hash','observed':'최초 root 본문을 열어 부분 설계/사용 질문인지 심사: '+m['title'],'limitations':'후속은 열지 않고 적격 판정만 함. 제외 이유는 frame.csv. 제외 원문을 주 표본 수로 세지 않음.','producer':'SQLite Forum / '+m['author'],'lineage':'forum-thread:'+m['artifact'],'count_in_minimum':False,'count_reason':'전수 심사 원장 중 제외된 최초 글; 핵심24대화 최소수 밖','kind':'screened_excluded_conversation'})
for d in json.loads((P/'ledger-metadata.json').read_text()):
    day=d['url'][-2:]
    sources.append({'id':'S-L'+day,'related_q':['Q1','Q3'],'case_ids':[],'url':d['url'],'published_or_revised':'2022-01-'+day+' historical event section; current rendering','fixed_version':d.get('sha256'),'checked_utc':d.get('read_utc',now),'read_locations':'2022 section; Post/Reply/Edit metadata only','observed':'최초 게시와 수정/답 사건을 시각·artifact·계정으로 구별; 본문/성공 여부는 사용하지 않음.','limitations':'달력의 현재 렌더링이며 삭제된 본문을 복구하거나 원 작성자의 실제 신원을 증명하지 않음.','producer':'SQLite Fossil forum','lineage':'SQLite Forum timeline','count_in_minimum':False,'count_reason':'모집 메타데이터; 대화/제공자문서 최소수에 더하지 않음','kind':'sampling_ledger'})
sources.append({'id':'S-M01','related_q':['Q1','Q3'],'case_ids':[],'url':'https://sqlite.org/forum/help?cmd=/forumpost','published_or_revised':'Fossil2.29 2026-11-20 current help','fixed_version':'Fossil 525a137617','checked_utc':now,'read_locations':'query parameters t=s,t=y,raw,hist,unf','observed':'단일 글과 수정이력 표시 옵션. 실제 최초판은 raw artifact로 확인했다.','limitations':'현재 도구 지침이며 2022 동작/사용조건 근거는 아님.','producer':'SQLite Fossil forum','lineage':'Fossil help','count_in_minimum':False,'count_reason':'수집 방법 설명','kind':'method_document'})
for name,rows in [('initial.jsonl',initial),('frozen-responses.jsonl',frozen)]:
    (P/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(P/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')

selected={x['hash']:x['id'] for x in cases}
excluded={
'd7338bf490':'fuzzing crash 재현 보고; 사용자의 부분 설계 선택/지원 질문 없음',
'befb9b54fd':'컴파일 경고 로그만; desired behavior/다음 행동 질문 없음',
'50244de629':'fuzzing crash PoC만; 부분 사용 목적/조건 질문 없음',
'2831335356':'fuzzing crash PoC만; 부분 사용 목적/조건 질문 없음',
'b4bfe62fe6':'본인이 제시한 결함 진단·패치/전체 rewrite 제안; 사용자 지원 질문이 아님',
'e920ac6771':'fuzzing crash PoC만; 부분 사용 목적/조건 질문 없음',
'422136a69c':'extension 발표/사용 권유',
'5bdc81e0a3':'authorizer 결함 제보만; 실제 보호 목표/부분 설계 질문 없음',
'45fc04f7da':'프로젝트의 SQL 확장 수용 정책 질문; 한 사용/상호작용 선택이 아님',
'255a66fa35':'eval 결함 진단만; 구체 사용자 사용 목표/질문 없음',
'eee7476d60':'별도 논문형 article 발표/범용 피드백 요청',
'ddb109bdf9':'이미 설명한 동작을 문서에 추가해 달라는 편집 요청',
'e7fd2c3f00':'매크로명 오타/불일치 제보',
}
ledgers=json.loads((P/'ledger-metadata.json').read_text())
roots=[e for l in ledgers for e in l.get('events',[]) if e['kind']=='Post']
roots.sort(key=lambda x:(x['date'],x['time'],x['artifact_prefix']))
frames=[]
for i,e in enumerate(roots,1):
    h=e['artifact_prefix'];m=meta.get(h,{})
    decision='selected' if h in selected else 'excluded' if h in excluded else 'not_screened_after_cap'
    frames.append({'frame_id':'SF'+str(i).zfill(3),'family':'S','month':e['date'][:7],'order':i,'submitted_utc':m.get('submitted_utc',e['date']+'T'+e['time']+':00')+'Z','title':e['title'],'url':'https://sqlite.org/forum/artifact/'+m.get('artifact',h),'decision':decision,'reason':('최초 적격 요청; 결말 미사용' if decision=='selected' else excluded.get(h,'원장 메타데이터만 읽음; 8건 상한 뒤 본문 심사 안 함')),'case_id':selected.get(h,''),'initial_status':'raw_original_confirmed' if m.get('artifact') else 'not_read','ledger_url':e['ledger_url']})
with (P/'frame.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(frames[0]));w.writeheader();w.writerows(frames)
assert len(initial)==8 and len(selected)==8
assert len([r for r in frames if r['decision']=='selected'])==8
receipt={'created_utc':now,'protocol_commit':base,'case_count':8,'strategy_messages':24,'original_versions_confirmed':8,'strict_preoutcome_eligible':7,'exposed_case_ids':['S01'],'screened_roots':21,'excluded_before_cap':13,'root_metadata_after_cap':len(frames)-21,'source_records':len(sources),'counted_sources':sum(s['count_in_minimum'] for s in sources),'files_sha256':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['initial.jsonl','frozen-responses.jsonl','frame.csv','sources.json']},'followups_opened':False,'exception':'S01 search-result snippet; explicitly excluded from strict chronology comparison'}
(P/'t0-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
