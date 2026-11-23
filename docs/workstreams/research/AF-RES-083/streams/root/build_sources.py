"""Serialize the investigator's source readings, separate from fetch attempts."""
import json, pathlib
P=pathlib.Path(__file__).resolve().parent
OBS={
 'UP-G38':('W-UP-GDAL-PARQUET','upstream manual','GDAL3.8.0;c46fe7e20e33925735ae4b785752795af72823bc','L18–22,70–77','기본 WKB; GEOARROW와 WKT는 당시 규격 외 확장으로 설명.','manual의 beta1 표기는 같은판 NEWS/writer와 다를 수 있음; 실제 실행 증명 아님.','GEOARROW 문자열과 모든 Parquet 행동의 일괄 동일시를 반증'),
 'UP-G39':('W-UP-GDAL-PARQUET','upstream manual','GDAL3.9.0;bb5ea618e23e498e79e8b8e6bd7215ad94bb2103','L19–20,68–83,125–134','새 GEOARROW는 struct; 구 표현은 GEOARROW_INTERLEAVED. WKB 기본 유지, covering bbox 기본 YES.','정확 consumer 설치판/예제와 연결되지 않으면 그 안내의 실패 증거 아님.','판·설정 단위 alias를 지지, 무조건 이름치환 반증'),
 'UP-G39NEWS':('W-UP-GDAL-RELEASE','upstream release record','GDAL3.9.0;bb5ea618e23e498e79e8b8e6bd7215ad94bb2103','L414–420,489–503','Arrow/Parquet struct 지원, GeoParquet1.1 bbox와 struct 읽기/쓰기 도입.','배포일은 release metadata 별도; 기능 도입 선언은 설치환경 실행 아님.','변경 종류·범위 지지'),
 'UP-S160REL':('W-UP-SCIPY-RELEASE','upstream compatibility announcement','SciPy1.6.0','L52–57,245–246','세 integrate 후계명 선언; 옛 이름은 호환용 잔류. stats의 동음 rename도 별도 namespace.','이후1.14 제거를1.6의 즉시깨짐으로 소급할 수 없음.','유지 가능한 구간을 지지; rename=removal 반증'),
 'UP-S160QUAD':('W-UP-SCIPY-RENAME','upstream fixed implementation','SciPy1.6.0','L7–43,273–279,407–439','numpy trapz를 trapezoid로 수출; 구 wrapper 인자 전달. simpson even=avg.','정적 구현 읽기; 실제 consumer 계산 또는 전체입력 동등성 검증 아님.','판 한정 alias 지지'),
 'UP-S154QUAD-FIX':('W-UP-SCIPY-RENAME','upstream fixed implementation','SciPy1.5.4','L9,257,380','옛 trapz import와 cumtrapz·simps 공개 정의; simps even=avg.','당시 배포환경 설치 미실시.','옛 exact namespace와 인자 존재 지지'),
 'UP-S160TEST':('W-UP-SCIPY-RENAME','upstream fixed tests','SciPy1.6.0','L144–161,164–245,248–266','simps alias 시험과 cumulative alias 시험이 지정 배열/축/초깃값을 비교.','시험 소스만 읽음; 079의 simps/cumtrapz 미실행을 채우지 않음.','근거 적용 입력 제한 지지'),
 'UP-S111REL':('W-UP-SCIPY-RELEASE','upstream compatibility announcement','SciPy1.11.0','L44–48,260–262,981','짝수 표본의 simpson 마지막 구간 방식 변경, even 폐기 예고.','예고1.13과 실제1.14를 구별; 이 파일은 원PR18209와 연결되나 별개의 실행 아님.','수치조건이 명칭보다 넓음을 지지'),
 'UP-S114REL':('W-UP-SCIPY-RELEASE','upstream compatibility announcement','SciPy1.14.0','L228–240,252–260,515,612','옛 세 적분 이름 제거; simpson even 제거 및 keyword-only 사용.','다른 namespace나 보존한 역사 안내를 일괄 수정할 근거 아님.','적용판 및 호출형식 한정 필요 지지'),
 'UP-GP100':('W-UP-GEOPARQUET-SPEC','upstream specification','GeoParquet1.0.0','Geometry columns; encoding; crs','geometry WKB/BYTE_ARRAY 요구, CRS 부재와 null 구별, 독자에게 지원 CRS 확인 권고.','규격≠특정 library binary;1.1은 같은 계보로 합산.','WKB 계약과 native encoding 분리 지지'),
 'UP-GP110':('W-UP-GEOPARQUET-SPEC','upstream specification','GeoParquet1.1.0','Native encodings; Version Compatibility','native는 separated struct; forward compatibility에는 미지원 인식이 허용.','항상 성공적으로 읽는다는 약속 아님.','any version 해석의 한계 지지'),
 'UP-GAFORMAT':('W-UP-GEOARROW-SPEC','upstream specification','current retrieval snapshot2026-11-23','Coordinate separated/interleaved; Serialized encodings','메모리 표현은 struct·FixedSizeList 둘을 구별하며 serialized WKB도 설명.','현재판 설명을2024역사구현 증명으로 소급하지 않음.','GeoArrow/GeoParquet/GDAL option 단위 분리 지지')
}

rows=[];attempts=[]
for line in (P/'acquisition.jsonl').read_text().splitlines():
 a=json.loads(line);sid=a['source_id']
 if not a['acquired']:
  attempts.append({**a,'counts_minimum':False,'reason':'접근실패; 올바른 _quadrature.py 경로는 UP-S154QUAD-FIX에서 별도로 확인'})
  continue
 if sid not in OBS:continue
 lineage,typ,ver,loc,obs,lim,claim=OBS[sid]
 rows.append({'source_id':sid,'lineage_id':lineage,'source_type':typ,'url':a['requested_url'],'fixed_version':ver,'location':loc,'opened_utc':a['opened_utc'],'reader':'root','questions':['Q1','Q2','Q3','Q5','Q7'],'cases':['G04'] if sid.startswith('UP-G') else ['O02'],'observed':obs,'limitations':lim,'supports_or_refutes':claim,'directly_read':True,'countable':True,'downstream_original':False,'sha256':a['sha256'],'http_status':a['status'],'count_reason':'같은 원저작의 여러 판·구현·시험은 lineage_id별 한 번만 산입'} )
(P/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(P/'attempts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in attempts))
print(json.dumps({'source_rows':len(rows),'lineages':len({r['lineage_id'] for r in rows}),'failed_attempts':len(attempts)}))
