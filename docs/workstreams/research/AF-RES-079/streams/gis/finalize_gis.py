"""Assemble documented observations; never executes or imputes upstream tests."""
from pathlib import Path
import json,re,csv,datetime,hashlib
P=Path(__file__).parent
C=P/'cache'
SHA=json.loads((P/'tag-commits.json').read_text())
receipts=[json.loads(x) for x in (P/'http-acquisition.jsonl').read_text().splitlines()]
R={x['key']:x for x in receipts}
def fixed(u):
 for v,sha in SHA.items():u=u.replace('/v'+v+'/', '/'+sha+'/')
 return u
# Independent work identifiers are intentionally broader than files/versions.
meta={
'extra-readme':('GDAL_LEGACY_README','GDAL extra drivers README','README Other drivers / build requirements','Rasdaman은 not_integrated_in_build에 있고 repository는 미유지·판 호환 무보증이라고 밝힌다. Other drivers 절의 일괄 3.5 설명은 실제 2023 Rasdaman 이관 commit과 다르다.','범용 README의 3.5 문구를 Rasdaman의 실제 제거판으로 사용하면 안 된다.'),
'issue4808':('GDAL_RASDAMAN_ISSUE4808','Rasdaman build and migration issue','issue body; 2021-11-10','기존 Rasdaman driver가 빌드되지 않으며 CMake 작업이 필요하다는 유지관리자 보고다.','3.6 소스 존재가 실행 가능성을 증명하지 않는다.'),
'issue4808-comments':('GDAL_RASDAMAN_ISSUE4808','Rasdaman migration comments','issuecomment-1192341478; issuecomment-1465303489','2022-07-22 자원 부족 보고와 2023-03-12 이관 완료 댓글이 수신 commit ffe0c447을 직접 지목한다.','수신자 팀의 별도 직접 발언 대신 GDAL 유지관리자의 연락 결과 보고다.'),
'ras-move-commit':('GDAL_DRIVER_IMPLEMENTATIONS','Rasdaman receiving commit','ffe0c44714a491eb90ba82d8df74f621ac6003e7 files; author date','2023-03-12 수신 commit이 not_integrated_in_build/rasdaman 소스·문서·시험·CMake 파일을 추가했다.','소스 추가는 build 성공 또는 현재 서비스 지속의 증거가 아니다.'),
'ras-doc3.6':('GDAL_DRIVER_MANUAL','Rasdaman driver documentation','L7-L43','raslib 의존, query-template로 2-D 부분 읽기, georeferencing read/write 미지원이라고 명시한다.','봉인한 CRS/geotransform 필수 요구를 이 기능 자체가 충족하지 못한다.'),
'ras-dest-doc':('GDAL_DRIVER_MANUAL','Rasdaman receiving documentation','L7-L43','수신 저장소 문서가 같은 query-template와 georeferencing 미지원 범위를 보존한다.','문서 이동의 동일성은 실제 연결 시험을 대신하지 않는다.'),
'ras-dest-readme':('GDAL_LEGACY_README','GDAL extra drivers receiving README','ffe0c447 README Other drivers','이관 commit 시점부터 Rasdaman이 not_integrated_in_build 목록에 놓였으며 이전 목록의 3.5 표제를 공유한다.','일괄 표제의 판 범위와 개별 추가 commit을 구별해야 한다.'),
'issue7920':('GDAL_ARG_ISSUE7920','Deprecate ARG format','issue body; 2023-06-10','제안자는 GeoTrellis 등에서 ARG를 더 쓰지 않는 것으로 안다며 GDAL 폐기를 요청한다.','다른 모든 사용자/소프트웨어의 부재를 전수 확인한 자료는 아니다.'),
'arg-doc-3.7':('GDAL_DRIVER_MANUAL','ARG driver documentation','L7-L27','ARG namespace와 raw+JSON 표현, create/createcopy 및 georeferencing capabilities를 기술한다.','표시 capability와 실제 driver 등록 callback을 따로 확인해야 한다.'),
'arg-doc-3.8':('GDAL_DRIVER_MANUAL','ARG driver deprecation documentation','L16-L37','3.9 제거 예정과 다른 일반 format으로 변환하라는 안내. 단일 지정 후속 driver는 없다.','변환은 동일 ID 별칭이 아니며 어떤 converter를 쓰더라도 원 속성 보존은 별도 시험이다.'),
'arg-test-3.8':('GDAL_DRIVER_TESTS','GDAL supplier driver tests','arg.py L48-L51, L77-L140, L174-L194, L270-L328','ARG test는 deprecated-driver YES 설정으로 2×2 data/metadata·geotransform·CreateCopy roundtrip을 정의한다.','시험 정의를 직접 읽었으나 이 세션에서 GDAL3.8 시험을 실행하지 않았다. int16 fixture의 nodata -32768과 driver 상수 -32767도 추가 검증 대상이다.'),
'arg-code-3.8':('GDAL_DRIVER_IMPLEMENTATIONS','GDAL driver implementations','argdataset.cpp L330-L334; L898-L915','ARG 등록 ID·help URL·Open/CreateCopy callback 및 int16 nodata 상수를 확인했다.','정적 코드만으로 전체 오류 경로 또는 binary build를 입증하지 않는다.'),
'parquet-doc-3.7':('GDAL_DRIVER_MANUAL','GDAL Parquet driver documentation','L18-L22; L47-L50','3.7 문서는 beta1 format과 default WKB, GEOARROW의 비표준 확장 성격을 기술한다.','driver logical ID와 format edition을 구별해야 한다.'),
'parquet-doc-3.8':('GDAL_DRIVER_MANUAL','GDAL Parquet 3.8 documentation','L18-L22; L70-L77','3.8 문서도 아직 beta1·experimental이라고 쓰지만 같은판 NEWS/writer/test는 1.0.0을 출력한다.','동일 발행판 내부 문서·구현 불일치이며 문서 한 절만 최종판 근거로 쓰지 않는다.'),
'parquet-doc-3.9':('GDAL_DRIVER_MANUAL','GDAL Parquet 3.9 documentation','L19-L20; L68-L83; L125-L160','GeoParquet1.1 지원, GEOARROW의 struct 의미, 구 GEOARROW의 GEOARROW_INTERLEAVED 이름 이동을 명시한다.','WKB/struct/interleaved 및 소비자 판에 따라 호환 방향이 다르다; SORT_BY_BBOX도 행 순서와 타입 지원에 조건을 붙인다.'),
'parquet-test-3.7':('GDAL_DRIVER_TESTS','GDAL Parquet supplier tests','ogr_parquet.py L473-L545; L555-L595','writer metadata version=1.0.0-beta.1 및 WKB 기대, PointM·invalid compression·두 번째 layer의 예외 기대를 읽었다.','3.7/3.8 test.parquet fixture bytes가 다르므로 같은 경로라는 이유로 동일 입력 실행 비교라 하지 않는다.'),
'parquet-test-3.8':('GDAL_DRIVER_TESTS','GDAL Parquet supplier tests','ogr_parquet.py L550-L622; L632-L674','동일 writer-call 구성에서 기대 version=1.0.0, WKB; PointM/invalid compression 예외 기대가 유지된다.','실제 시험 실행/CI 결과 미관측; 함수의 input fixture 파일도 변경되었다.'),
'parquet-test-3.9':('GDAL_DRIVER_TESTS','GDAL GeoArrow supplier tests','ogr_parquet.py L3574-L3680; L3721-L3805','POINT(1 2), null, empty, point 입력을 두 encoding에 쓰는 시험에서 struct는 null을 None, interleaved는 Point null을 EMPTY로 기대한다.','같은 3.9 판의 구·신 encoding 비교이며 3.8↔3.9 native 실행은 하지 않았다.'),
'parquet-writer3.7':('GDAL_DRIVER_IMPLEMENTATIONS','GDAL Parquet writer implementation','ogrparquetwriterlayer.cpp L350-L363','출력 metadata version 상수가 1.0.0-beta.1이다.','전체 serialization 동작 실행 미관측.'),
'parquet-writer3.8':('GDAL_DRIVER_IMPLEMENTATIONS','GDAL Parquet writer implementation','ogrparquetwriterlayer.cpp L365-L380','출력 metadata version 상수가 1.0.0이다.','full I/O equivalence 증거는 아니며 문서 mismatch만 독립 확인한다.'),
'gp-spec1.0':('GEOPARQUET_SPEC','GeoParquet specification','v1.0.0 Geometry columns / encoding / metadata','공식1.0은 geometry WKB/BYTE_ARRAY와 version 표기를 요구한다.','규격은 해당 GDAL binary가 그대로 구현했다는 보증이 아니다.'),
'gp-spec1.1':('GEOPARQUET_SPEC','GeoParquet specification','v1.1.0 Native encodings / Version Compatibility','1.1은 struct 기반 native geometry를 추가한다. forward compatibility는 옛 reader의 올바른 해석 또는 명시적 미지원 인식도 허용한다.','새 format을 반드시 옛 reader가 성공적으로 읽어야 한다는 보장은 아니다.'),
'jp2lura-doc-3.10':('GDAL_DRIVER_MANUAL','JP2Lura driver documentation','L7-L63; L114-L120','Lurawave 기반 reader/writer, 필수 라이선스 설정과 GeoJP2 default NO를 확인한다.','자연 quota 뒤에 해당하는 보충 사례; 다른 JPEG2000 driver와 자동 병합하지 않는다.'),
'jp2lura-test-3.10':('GDAL_DRIVER_TESTS','JP2Lura supplier tests','L35-L96; L145-L169','SDK/라이선스가 없으면 skip; license 오류는 None; 정상 byte.jp2 checksum50054·좌표계·geotransform을 기대한다.','시험이 존재한다는 것과 실제 라이선스 환경에서 통과했다는 것은 다르다.'),
'rfc108':('GDAL_RFC108','GDAL RFC108 driver removals','L7-L12; L36-L65; L105-L135','3.11 제거 대상과 유지관리 이유, 옛 판으로 돌아갈 수 있도록 삭제 목록을 남기는 정책을 읽었다.','사용자 전수 부재를 확정하지 않으며 문서 자체도 이를 인정한다. 자연quota 뒤 보충 사례.'),
'rfc108-live':('GDAL_RFC108','GDAL RFC108 current revision','Update / Documentation','현재 RFC에는 TIGER와 UK.NTF 제거가3.13에 되돌려졌다는 갱신이 있다. 옛 폐기 판정의 종료판·복구 가능성이 필요하다.','JP2Lura가 복구됐다고 일반화하지 않는다; 원3.11 RFC와 현재판은 같은 저작이다.'),
}
meta['arg-code-3.7']=('GDAL_DRIVER_IMPLEMENTATIONS','ARG3.7 implementation','Open L256-L269; registration L895-L907','3.7 Open has no later deprecation gate; registered Open and CreateCopy callbacks.','소스 판독이며 native 실행 미관측.')
meta['gdal-manager-3.8']=('GDAL_DRIVER_IMPLEMENTATIONS','GDAL3.8 deprecated driver gate','L1187-L1207','GDAL_ENABLE_DEPRECATED_DRIVER_<name> default NO returns failure; explicit YES enables.','정적 코드 판독. 실제 계정/환경 설정은 별도로 기록해야 한다.')
for key in ['ras-code3.6','ras-dest-code','ras-reg3.6','ras-reg3.7','arg-reg3.8','arg-reg3.9','jp2-reg3.10','jp2-reg3.11']:
 meta[key]=('GDAL_DRIVER_IMPLEMENTATIONS','GDAL driver code/registration',{'ras-code3.6':'L700-L716','ras-dest-code':'GDALRegister_RASDAMAN','ras-reg3.6':'L158-L160','ras-reg3.7':'L148-L162 (Rasdaman registration absent)','arg-reg3.8':'L489','arg-reg3.9':'full registry (ARG absent)','jp2-reg3.10':'L190-L191; L518','jp2-reg3.11':'full registry (JP2Lura absent)'}[key],'전후 등록 ID·namespace 및 callback 존재/부재를 판별했다.','registry 소스만으로 binary의 옵션·플러그인·동작 성공을 추정하지 않는다.')
meta['ras-dest-test']=('GDAL_DRIVER_TESTS','Rasdaman archived supplier tests','rasdaman.py full test definitions','archived source의 Rasdaman test 입력·server 요구·skip 경계를 직접 읽었다.','rasdaman server 및 raslib가 없고 test 실행 미관측.')
rows=[]; seen=set()
news=json.loads((P/'news-receipts.json').read_text())
for n in news:
 v=n['version'];r=json.loads((C/f'release-{v}.txt').read_text());fid='GDAL_NEWS'
 rows.append({'source_id':'G-NEWS-'+v,'work_id':fid,'counted':fid not in seen,'publisher':'OSGeo/GDAL','title':'GDAL '+v+' release notes','url':n['url'],'opened_url':n['url'],'arrived_url':n['arrived_url'],'fixed_url':fixed(n['url']),'edition':v,'published_utc':r.get('published_at'),'checked_utc':n['retrieved_utc'],'section':'first release heading only; raster/vector sections and release highlights; '+str(n['section_lines'])+' lines','finding':'모집 공지의 변경 문구를 원순위로 검사했다. 첫4는 3.7 Rasdaman, 3.8 ARG, 3.8 GeoParquet1.0, 3.9 GeoParquet1.1이다.','limitations':'동일 NEWS의 여러 판을 독립 저작으로 늘리지 않음; 선언과 실행을 분리.','counterevidence':'Rasdaman 수신README의 포괄적3.5 문구, Parquet3.8 문서 beta1 문구를 다른 원문과 대조.','access':'direct_read','http_status':n['status'],'http_chain':[],'sha256':n['sha256_full'],'count_reason':'공식 릴리스 series 1계보. 이후 판은 추가 산입0.','claim_ids':['Q1','Q2']});seen.add(fid)
for r in receipts:
 key=r['key'];m=meta.get(key);ok=r['access']=='read_success';family=m[0] if m else 'SUPPORT_METADATA';count=bool(ok and m and family not in seen and key!='ras-move-commit')
 if count:seen.add(family)
 url=r['requested_url'];ed=next((v for v in SHA if '/v'+v+'/' in url), 'retrieval snapshot')
 row={'source_id':'G-'+key,'work_id':family,'counted':count,'publisher':'GeoParquet contributors' if key.startswith('gp-') else 'OSGeo/GDAL','title':m[1] if m else key,'url':url,'opened_url':url,'arrived_url':r.get('arrived_url'),'fixed_url':fixed(url),'edition':ed,'checked_utc':r['checked_utc'],'section':m[2] if m else ('HTTP response/metadata only; not counted' if ok else 'failed response'),'finding':m[3] if m and ok else ('접근/메타데이터 확인만. 독립 저작 수 산입하지 않음.' if ok else r.get('error')),'limitations':m[4] if m else '다른 문서의 판·API metadata·실패 접근을 추가 원저작으로 세지 않는다.','counterevidence':m[4] if m else '분모 밖의 접근 기록.','access':'direct_read' if m and ok else r['access'],'http_status':r.get('status'),'http_chain':r['redirect_chain'],'sha256':r.get('sha256'),'count_reason':'별도 목적의 원저작 1계보, 같은 판/절/미러·test/code 같은 series는 중복 제외.' if count else 'same-work edition/section/support metadata/access failure; 0','claim_ids':['Q1','Q2','Q3','Q5','Q7']}
 rows.append(row)
with (P/'sources.jsonl').open('w') as f:
 for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
# Full lexical screening record plus contextual format-version match.
selected={('3.7.0',37):'G01',('3.8.0',25):'G02',('3.8.0',510):'G03',('3.9.0',492):'G04'}
q=[];seq=0
for notice_rank,n in enumerate(news,1):
 v=n['version'];ls=(C/f'NEWS-{v}.md').read_text().splitlines()
 for lineno,line in enumerate(ls,1):
  if not re.search(r'renam|mov|replac|deprecat|remov|merge|split|version|alias|provider|Updated uris|GRIB2@|GeoParquet 1\.1',line,re.I):continue
  seq+=1;eid=selected.get((v,lineno),'');decision='selected' if eid else 'excluded';reason='first eligible independent event under sealed frame' if eid else 'API/implementation/option/dependency change; not driver identity or file-format edition'
  if (v,lineno)==('3.7.0',261):reason='tile-matrix resource URI, not driver identity or file-format edition'
  if 'GRIB2@' in line:reason='decoding table revision, not GRIB file-format edition or driver ID'
  if (v,lineno) in [('3.8.0',191),('3.9.0',25)]:reason='duplicate ARG retirement announcement; first eligible 3.8 highlight retained';decision='duplicate'
  if (v,lineno)==('3.9.0',493):reason='same GeoParquet1.1 change decision as L491-L493';decision='duplicate'
  if notice_rank>=4:
   decision='after_quota';reason='read within cap; four earlier eligible changes already fill natural slots; no replacement'
  q.append({'candidate_id':f'G-F{seq:03}','original_rank':seq,'notice_rank':notice_rank,'release':v,'published_utc':json.loads((C/f'release-{v}.txt').read_text()).get('published_at'),'line':lineno,'source_url':fixed(n['url'])+f'#L{lineno}','text':line,'decision':decision,'event_id':eid,'reason':reason})
with (P/'recruitment.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(q[0]));w.writeheader();w.writerows(q)
(P/'recruitment-summary.json').write_text(json.dumps({'seal_local':'60114f7','seal_remote_same_tree':'dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead','finalized_utc':'2026-11-23T11:35:48.215082+00:00','notice_cap':5,'notices_read':5,'next_notice_not_recruited':'3.12.0','natural_allocated':4,'selected':[x for x in q if x['decision']=='selected'],'eligibility_correction':'Rasdaman was provisionally questioned based on receiving README saying removed in3.5. Direct3.6 registry+source,3.7 absence,and 2023-03-12 receiving commit disprove exclusion. Final selection follows unchanged sealed rule. JP2Lura returns to after-quota supplement.','source_works_counted':len([x for x in rows if x['counted']]),'source_works':sorted(seen)},ensure_ascii=False,indent=2)+'\n')
print('source rows',len(rows),'independent works',len([x for x in rows if x['counted']]),'screened candidates',len(q),'selected',[(x['event_id'],x['original_rank']) for x in q if x['event_id']])
