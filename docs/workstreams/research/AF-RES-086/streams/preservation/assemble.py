"""Assemble the directly inspected preservation records; no new network calls."""
import csv, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
E=ROOT/'evidence'

def read(s):
    p=E/s
    if not p.exists() and s.endswith('.json'):p=E/(s[:-5]+'.extract.json')
    return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')

# All quoted snippets below are deliberately short; the receipt hashes describe
# the full downloaded response, while extracts are selected factual fields.
specs={
'PR01':('PR-L-MATPLOTLIB','version_record','record2893252; files[0]; metadata.version','matplotlib v3.1.0의 판 DOI·concept592536·ZIP명·발행자 MD5·크기를 직접 읽음.','ZIP 미다운로드; 발행자 체크섬을 직접 바이트 검증으로 간주하지 않음.',True),
'PR02':('PR-L-MATPLOTLIB','version_record','record3695547; files[0]; metadata.version','matplotlib v3.2.0가 별도 DOI와 다른 ZIP 크기·MD5를 가짐. 같은 concept592536.','현재 조회한 역사 레코드; 2020년 HTTP 응답 영수증 아님.',True),
'PR03':('PR-L-MATPLOTLIB','moving_alias','concept592536 -> record22700776','현재 concept API는 v3.11.2 레코드22700776으로 이동.','별칭/추가 판 관측이며 필수 역사판 원기록 수에 더하지 않음. 이동 연속성 미확인.',False),
'PR06':('PR-L-UMAP','version_record','concept705645 -> record800648; files[0]','현재 concept705645는 record800648로 이동하며 umap_1.1.0.tar.gz 파일 목록을 제공.','metadata.version 필드는 없어서 판 번호는 파일명과 실제 setup.py로 확인.',True),
'PR07':('PR-L-TOMBSTONE','withdrawal_record','record22705920; tombstone','API가410·Record deleted·retracted·2026-09-19T19:02:04.838479Z를 반환하고 파일 목록이 없음.','의도된 철회; 저장소 장애 또는 모든 DOI의 실패로 일반화하지 않음.',True),
'PR08':('PR-L-ZENODO-POLICY','provider_documentation','DOI versioning; Concept DOI resolution','판 DOI와 concept DOI를 구별하고 concept의 최신판 이동을 설명함.','현재 정책; 과거 발행 때의 계약 증거가 아님. PR16의 동일 DOI 파일변경 예외와 함께 읽음.',True),
'PR09':('PR-L-HELLO','archive_snapshot','snapshot a5e907...; hello-2.9.tar.gz,hello-2.10.tar.gz','한 보관 snapshot의 파일명→revision 매핑에 GNU hello2.9와2.10이 함께 존재함.','SWH snapshot은 웹 문서 게시·독자 HTTP 응답의 동시 제공을 증명하지 않음.',True),
'PR10':('PR-L-UMAP','version_record','record60943; files[0]; relations.version','Umap 구판record60943의 umap_1.0.0.tar.gz와 공통 concept705645·version index0를 읽음.','metadata.version 없음; 실제 setup.py의1.0.0로 보강.',True),
'PR11':('PR-L-TOMBSTONE','doi_resolution','DOI22705920 -> records22705920','실제 DOI를 열어도 최종410 tombstone이며 원파일 공개가 회복되지 않음.','PR07과 같은 철회 사건의 다른 표현. 원자료 최소수에는 중복으로 더하지 않음.',False),
'PR16':('PR-L-ZENODO-POLICY','provider_documentation','Manage files; Modify files after publication','현 정책은 발행30일 내 경미한 파일 편집과 최초발행45일 내 재게시를 허용하고 DOI 불변을 설명.','실제 조사한 Umap/matplotlib에서 수정이 발생했다는 증거는 없음.',True),
'PR17':('PR-L-HELLO','archive_revision','revision dbdaa32...; type=tar; synthetic=true; directory','hello2.10의 보관 revision은 synthetic tar이며 directory fd2df12...로 이어짐.','기록된2014-11-16 시각은 SWH synthetic metadata; 원발행자 CI성공·게시시각 아님.',True),
'PR18':('PR-L-HELLO','archive_revision','revision55c14d...; type=tar; synthetic=true; directory','hello2.9의 별도 synthetic tar revision과 directory ec15a3...를 읽음.','2013-10-09 metadata를 발행일로 단정하지 않음. NEWS는2.9를2013-10-10으로 표시.',True),
'PR19':('PR-L-GITORIOUS','archive_snapshot','snapshot e1d8df...; HEAD; refs/heads/master','보관 Gitorious wiki의 HEAD와master가 같은 revision3f39ce...를 가리킴.','같은 이름/내용 매핑은 보관 snapshot 내부 관측; 옛웹URL 정상 응답 증거 아님.',True),
'PR20':('PR-L-HELLO','archive_visit','rsync://ftp.gnu.org/gnu/hello; visit1','2015-08-28T11:13:26Z full visit가 PR09 snapshot을 가리킴.','archive visit의 full은 수집자상태이며 원사이트publish-success나독자요청상태 아님.',True),
'PR21':('PR-L-GITORIOUS','archiver_report','ArchiveTeam Gitorious oldid59702; Status,Archives','복구 작업 참가측의 고정 위키가 읽기전용 미러는2024-09-30까지였다고 표기하고 Saved 상태를 남김.','회고 보고; 현재 직접 요청의proxy503만으로 영구 소실을 단정하지 않음.',True),
'PR23':('PR-L-UMAP','downloaded_archive','umap_1.0.0.tar.gz; umap/setup.py','1,673,515 bytes를 실제 읽어 발행자 MD5와 일치;245회원목록; setup.py version1.0.0.','현재 바이트 검증.2016년 독자의 실제HTTP응답/배포연속성은 미확인.',True),
'PR24':('PR-L-UMAP','downloaded_archive','umap_1.1.0.tar.gz; umap/setup.py','1,868,653 bytes를 실제 읽어 발행자 MD5와 일치;263회원목록; setup.py version1.1.0.','압축파일읽기만 했고코드는실행하지않음;보존내용과빌드/호스팅을구별.',True),
'PR25':('PR-L-HELLO','archive_wrapper_manifest','directory fd2df12...; hello-2.10/','보관 tar의 최상위 hello-2.10 디렉터리를 실제 파일manifest로 잇는 래퍼.','PR29의 동일판manifest로 이어지는 연결정보이며 별도원자료로 중복계수하지 않음.',False),
'PR26':('PR-L-HELLO','archive_wrapper_manifest','directory ec15a3...; hello-2.9/','보관 tar의 최상위 hello-2.9 디렉터리를 실제 파일manifest로 잇는 래퍼.','PR30의 동일판manifest로 이어지는 연결정보이며 별도원자료로 중복계수하지 않음.',False),
'PR27':('PR-L-GITORIOUS','archive_revision','revision3f39ce...; directory6fca7c...','Gitorious wiki revision2015-01-22의 실제 directory를 읽음.','git author/committer 시각은 옛 URL 제공시각이 아님.',True),
'PR28':('PR-L-SWH-POLICY','provider_documentation','Directory API; Response fields; Status Codes','directory API의 파일명·길이·체크섬·target_url 의미와404의범위를읽음.','현재 API계약이지구체적인보존완료증거는아님.',True),
'PR29':('PR-L-HELLO','archive_file_manifest','directory bd2df77...; 30 entries','hello2.10의30개루트항목·configure.ac/NEWS 체크섬과파일길이를직접읽음.','하위전체트리나원tar파일체크섬까지모두검증한것은아님.',True),
'PR30':('PR-L-HELLO','archive_file_manifest','directory3c6120...; 29 entries','hello2.9의29개루트항목·configure.ac/NEWS 체크섬과파일길이를직접읽음.','루트목록과대표내용검증;전체빌드가능성을증명하지않음.',True),
'PR31':('PR-L-GITORIOUS','archive_file_manifest','directory6fca7c...;33 entries;Home.markdown','현재보관소에서wiki33항목과Home.markdown 체크섬·1,319bytes를읽음.','보관소목록은옛gitorious도메인을복구하지않음.',True),
'PR32':('PR-L-HELLO','archived_file','hello2.10 configure.ac;sha1_git30a9d0...','실제configure.ac2,408bytes의SHA256이보관manifest와일치.','이파일의버전은간접생성이므로그자체에2.10문자열이있다고주장하지않음;PR35보강.',True),
'PR33':('PR-L-HELLO','archived_file','hello2.9 configure.ac;sha1_git6b0b19...','실제configure.ac2,156bytes의SHA256이manifest와일치하고AC_INIT에2.9표시.','생성/배포실행은없음.',True),
'PR34':('PR-L-GITORIOUS','archived_file','Home.markdown;sha1_git8f2ec2...','실제wiki본문1,319bytes와SHA256이manifest와일치하며설치·API·WebHooks참조등이남아있음.','본문보존을확인했지만모든wiki페이지와첨부파일까지검증하지않음.',True),
'PR35':('PR-L-HELLO','archived_file','hello2.10 NEWS lines1-3,16','NEWS에2.10(2014-11-16)및2.9(2013-10-10)기록이있고실제4,023bytes가manifestSHA256과일치.','첫줄의미정다음판표시는출판완료판으로세지않음.',True),
}
rows=[]
for sid,(lin,kind,section,obs,lim,count) in specs.items():
    isarchive=sid in ['PR23','PR24']
    r=read(sid+('.manifest.json' if isarchive else '.receipt.json'))
    row={'id':sid,'lineage_id':lin,'kind':kind,'url':r['request_url'],'final_url':r['final_url'],'version_or_section':section,'read_utc':r['completed_utc'],'Q':['Q7'],'cases':['cross-domain'],'claim_ids':['Q7-'+lin],'observed':obs,'observer':'AF-RES-086 preservation worker; provider fields distinguished from direct byte calculation','support_refute':'supports separating identifier,version,file bytes,archive visit and website route; refutes substituting one for another','limitations':lim,'receipt_path':'streams/preservation/evidence/'+sid+('.manifest.json' if isarchive else '.receipt.json'),'counts_original':count,'access_status':r['http_status'],'response_bytes':r['response_bytes'],'download_sha256':r['sha256']}
    rows.append(row)
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))

attempts=[]
for f in sorted(E.glob('PR*.receipt.json')):
    r=json.loads(f.read_text()); r['counts_original']=bool(specs.get(r['id'],[None]*5+[False])[-1]);r['category']='source' if r['id'] in specs else 'search_or_calibration_or_failure'
    if r.get('http_status',500)>=500:r['impact']='해당자료미열람;접근실패를내용소실또는서비스원서버실패로승격하지않음'
    attempts.append(r)
for sid in ['PR23','PR24']:
    r=read(sid+'.manifest.json');attempts.append({k:v for k,v in r.items() if k!='members'}|{'category':'archive_download','counts_original':True})
(ROOT/'attempts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in attempts))

pair=[]
for sid in ['PR01','PR02','PR10','PR06']:
    j=read(sid+'.json'); f=j['files'][0]
    pair.append({'institution':'Zenodo','work':'UMAP' if sid in ['PR10','PR06'] else 'matplotlib','source_id':sid,'record_id':j['id'],'version':j.get('metadata',{}).get('version') or ('1.0.0' if sid=='PR10' else '1.1.0'),'version_basis':'metadata.version' if sid in ['PR01','PR02'] else 'file name and downloaded setup.py','published_date':j['metadata']['publication_date'],'version_doi':j['doi'],'concept_doi':j['conceptdoi'],'file_name':f['key'],'publisher_checksum':f['checksum'],'publisher_size':f['size'],'download_verified':sid in ['PR10','PR06'],'direct_sha256':read(('PR23' if sid=='PR10' else 'PR24')+'.manifest.json')['sha256'] if sid in ['PR10','PR06'] else None})
for sid,mid,raw,version in [('PR17','PR29','PR32','2.10'),('PR18','PR30','PR33','2.9')]:
    rev=read(sid+'.json'); manifest=read(mid+'.json'); f=next(x for x in manifest if x['name']=='configure.ac');r=read(raw+'.receipt.json')
    pair.append({'institution':'Software Heritage','work':'GNU hello','source_id':sid,'version':version,'revision':rev['id'],'synthetic':rev['synthetic'],'revision_date':rev['date'],'snapshot':'a5e907833c4c1dbacb652e6f65fd9f5fdd1dad5a','archive_visit_utc':'2015-08-28T11:13:26+00:00','directory':rev['directory'],'inner_directory':f['dir_id'],'manifest_source':mid,'root_entries':len(manifest),'representative_file':'configure.ac','publisher_sha256':f['checksums']['sha256'],'direct_sha256':r['sha256'],'checksum_equal':r['sha256']==f['checksums']['sha256']})
write(ROOT/'pairs.json',pair)

# Save short factual extracts and remove full HTML/source response copies. Full
# response checksums remain in receipts; extracted files have separate hashes.
snips={
'PR08':'The Concept DOI resolves to the landing page of the latest version of your record.',
'PR11':'Record deleted',
'PR16':'Publishing the draft will not change the DOI.',
'PR21':'Offline (read-only mirror until Sep 30th, 2024)',
'PR28':'Directories are identified by sha1 checksums, compatible with Git directory identifiers.',
'PR32':'AC_INIT([GNU Hello],',
'PR33':'AC_INIT([GNU Hello], [2.9], [bug-hello@gnu.org],,[http://www.gnu.org/software/hello/])',
'PR34':'# Gitorious',
'PR35':'* Noteworthy changes in release 2.10 (2014-11-16) [stable]',
}
for sid in snips:
    f=E/(sid+'.html')
    if not f.exists():continue
    obj={'source_id':sid,'source_url':read(sid+'.receipt.json')['request_url'],'excerpt':snips[sid],'observation':specs[sid][3],'limitation':specs[sid][4],'scope':'Short extraction only; full downloaded response hash in receipt is distinct from this extract hash.'}
    target=E/(sid+'.extract.json');write(target,obj);f.unlink()
    r=read(sid+'.receipt.json');r['body_retained']=False;r.pop('body_path',None);r['extract_path']=target.relative_to(ROOT).as_posix();r['extract_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();write(E/(sid+'.receipt.json'),r)
for sid in ['PR01','PR02','PR03','PR06','PR07','PR10']:
    f=E/(sid+'.json')
    if not f.exists():continue
    j=json.loads(f.read_text())
    if sid=='PR07':
        obj={k:j.get(k) for k in ['status','message']}; t=j.get('tombstone',{});obj['tombstone']={k:t.get(k) for k in ['removal_date','is_visible','removal_reason','deletion_policy']}
    else:
        obj={k:j.get(k) for k in ['id','doi','conceptrecid','conceptdoi','created','modified','status','files']};obj['metadata']={k:j.get('metadata',{}).get(k) for k in ['title','publication_date','version','relations','related_identifiers']};obj['links']={k:j.get('links',{}).get(k) for k in ['self','self_html','doi','parent','parent_doi','files','latest','versions']}
    obj['extraction_note']='Selected factual fields from full API response; full-response checksum is in receipt.'
    target=E/(sid+'.extract.json');write(target,obj);f.unlink()
    r=read(sid+'.receipt.json');r['body_retained']=False;r.pop('body_path',None);r['extract_path']=target.relative_to(ROOT).as_posix();r['extract_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();write(E/(sid+'.receipt.json'),r)

valid=[x for x in rows if x['counts_original']]
attempts=[(read(x['id']+'.receipt.json')|{k:x[k] for k in ['counts_original','category'] if k in x}|({'impact':x['impact']} if 'impact' in x else {})) if (E/(x['id']+'.receipt.json')).exists() else x for x in attempts]
(ROOT/'attempts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in attempts))
cost={'instrumented_logical_gets':len(attempts),'instrumented_response_body_bytes':sum(x['response_bytes'] for x in attempts),'http_200':sum(x.get('http_status')==200 for x in attempts),'http_410_tombstone':sum(x.get('http_status')==410 for x in attempts),'proxy_503':sum(x.get('http_status')==503 for x in attempts),'downloaded_archive_bytes':sum(read(s+'.manifest.json')['response_bytes'] for s in ['PR23','PR24']),'downloaded_archive_count':2,'direct_source_rows':len(rows),'minimum_count_eligible_originals':len(valid),'eligible_lineages':sorted(set(x['lineage_id'] for x in valid)),'required_actual_version_records':6,'actual_version_pairs':3,'institutions':2,'limitation':'Logical application GET count; automatic redirect hops and search-service transport bytes unknown. Pre-instrumentation3 exploratory GETs and web-tool search/open calls are separately logged; never totalled as known bytes.'}
write(ROOT/'costs.json',cost)
print(json.dumps(cost,ensure_ascii=False,indent=2))
