"""Build post-seal analysis from locally cached public originals; no frozen T0 mutation.

Run from this directory with Python 3. Cached retrieved/ originals are intentionally
not committed; canonical URLs, read sections and SHA256 are in the public ledgers.
This script formats analyst judgements, not an automated causal inference.
"""
from pathlib import Path
import json, csv, hashlib, datetime as dt

P = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
SEAL = '9de54923257d613359348c8ccee2ff8225c8a0d8'
I = {r['case_id']: r for r in map(json.loads, (P/'initial.jsonl').read_text().splitlines())}
SEL = ['X01','X02','X03','X04','X05','X06','X07','X08','XB03','XB06','XB08','XB13','XB14']
T0Q = list(csv.DictReader((P/'questions.csv').open()))

def stamp(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
def iso(d): return d.isoformat().replace('+00:00','Z')
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def write_jsonl(name, rows):
    (P/name).write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
def cached_comments(cid):
    n=I[cid]['issue_number']; fs=list((P/'retrieved').glob(f'comments-{n}*'))
    f=next((f for f in fs if 'rawconnector' in f.name),fs[0])
    return f,json.loads(f.read_text())
C = {cid: cached_comments(cid) for cid in I}
CM = {cid:{c['id']:c for c in x[1]['data']} for cid,x in C.items()}
ROOTS={}
for fn in ['frame-A1.json','frame-A2.json','frame-B.json']:
    ROOTS.update({r['number']:r for r in json.loads((P/'retrieved'/fn).read_text())['data']['items']})

def event(cid, ident, summary, **kw):
    c=CM[cid][ident]; root=stamp(I[cid]['created_at']); t=stamp(c['created_at'])
    return dict(comment_id=ident, url=c['html_url'], at=c['created_at'], updated_at=c['updated_at'],
                author=c['user']['login'], author_association=c.get('author_association','미확인'),
                is_root_author=c['user']['login']==I[cid]['author'], current_body_sha256=sha(c['body'] or ''),
                root_elapsed_hours=round((t-root).total_seconds()/3600,4), within_root30=t<=root+dt.timedelta(days=30),
                within_root90=t<=root+dt.timedelta(days=90), summary=summary, **kw)

def q(cid, ident, qid, variables, summary, kind='information_request', target='root_author', first=False):
    return event(cid,ident,summary,question_id=qid,variables=variables,kind=kind,target=target,
                 question_episode_id=qid,
                 first_substantive_response=first, real_information_request=kind=='information_request',
                 predictions_sealed_before_outcome=first)
def ans(cid, ident, qid, variables, summary, category, strict=False, **kw):
    return event(cid,ident,summary,question_id=qid,variables=variables,category=category,
                 strict_same_variable_answer=strict,**kw)
def rec(cid,ident,summary,before,after,classification,link='none',same_supporter=False,strict=False,**kw):
    return event(cid,ident,summary,before=before,after=after,classification=classification,
                 linkage=link,same_supporter=same_supporter,strict_linked_recommendation_change=strict,**kw)
def run(cid,ident,summary,result,same_target=True,full_goal='미확인',new=True,**kw):
    return event(cid,ident,summary,result=result,same_original_target=same_target,
                 full_original_goal=full_goal,new_execution=new,**kw)

D={cid:dict(questions=[],answers=[],recommendations=[],executions=[],other_events=[],late_history=[],technical_sources=[],unknowns=[]) for cid in SEL}

D['X01'].update(
 recommendations=[rec('X01',1383184222,'명시 encoding이 기존 tas.encoding을 대체하므로 원 encoding dict를 직접 수정하도록 안내.','제안 없음','tas.encoding 자체 수정','no_prior_proposal')],
 technical_sources=['XD01','XD06'],
 unknowns=[dict(fact='작성자의 새 저장 실행과 CF grid_mapping 보존',reason='root90 안에 작성자 후속이 없음',last_url='https://github.com/pydata/xarray/issues/7406#issuecomment-1383184222',next_evidence='작성자가 제안을 적용한 to_netcdf 호출 및 ncdump 출력')])
D['X02'].update(
 questions=[q('X02',1369974685,'X02-later-error',['actual_error','traceback'],'기존 답으로 해결되지 않는다고 인정하고 실제 오류와 traceback을 요청. traceback 문구는 답 뒤 편집됨.')],
 answers=[ans('X02',1370139670,'X02-later-error',[], '다른 버그 때문에 아직 해당 단계에 도달하지 못하며 나중에 제공하겠다고 함. 오류값은 없음.','blocked_pledge_no_value',False)],
 recommendations=[rec('X02',1369732703,'기존 store 덮어쓰기라면 mode=w, 아니면 pytest tmp_path를 조건부 제안.','제안 없음','to_zarr mode=w 또는 tmp_path','no_prior_proposal'),
                  rec('X02',1369974685,'작성자의 자발적 S3+moto 보충을 받아 초기 추정이 맞지 않음을 인정하고 진단자료로 이동.','mode=w / tmp_path','오류와 traceback 요청','next_action_change','explicit_to_unsolicited_fact',True,False)],
 other_events=[event('X02',1369880263,'S3와 moto의 가상 bucket을 해체·재생성하여 파일이 이미 사라졌고 내부 상태만 남는다는 기존 사실을 자발적으로 공개. 앞선 문장에 대응하는 실제 정보 질문 없음.',category='unsolicited_existing_fact_new_disclosure')],
 technical_sources=['XD01','XD02'],
 unknowns=[dict(fact='오류 종류와 원인 및 해결 실행',reason='작성자는 실행을 막은 다른 버그만 알리고 요청된 값을 공개하지 않음',last_url='https://github.com/pydata/xarray/issues/7408#issuecomment-1370139670',next_evidence='S3+moto fixture와 실제 traceback')])
D['X03'].update(
 recommendations=[rec('X03',1381050335,'Dataset.to_dask_dataframe 문서와 임시 Dataset으로 변환하는 방법을 제시.','제안 없음','DataArray→temporary Dataset→to_dask_dataframe','no_prior_proposal')],
 other_events=[event('X03',1398072586,'문서는 봤지만 Dataset 우회는 생각하지 못했다고 인정하고 Series를 얻을 수 있으면 좋겠다고 함. 실제 실행 결과는 없음.',category='verbal_understanding_without_execution'),
               event('X03',1461877047,'제3자가 기능 구현에 관심을 표함.',category='third_party_development_interest'),
               event('X03',1494027739,'제3자가 변환 코드를 제안. 작성자 실행 및 반환 타입의 기술적 정당성은 미확인.',category='third_party_code_proposal')],
 technical_sources=['XD02'],
 unknowns=[dict(fact='DataArray 작성자의 실제 dataframe/Series 변환 성공',reason='제안 이해와 추가 선호만 확인되며 실행·출력 없음',last_url='https://github.com/pydata/xarray/issues/7409#issuecomment-1398072586',next_evidence='작성자의 실제 변환 호출과 반환 타입 출력')])
D['X04'].update(
 questions=[q('X04',1371024876,'X04-opening_call',['opening_call'],'GeoTIFF를 여는 실제 방식을 요청하면서 rioxarray 설치 시 rasterio engine으로 즉시 열도록 조건부 안내.',first=True)],
 answers=[ans('X04',1372480571,'X04-opening_call',['opening_call'],'glob으로 paths를 만든 뒤 안내한 방법으로 전달하니 동작한다고 답함. 처음부터 그렇게 했다는 뜻은 아니며 rasterio를 시도하지 않았다고 회고.','post_advice_execution_answer',False,direct_answer_content=True,existing_value_at_T0='미확인')],
 recommendations=[rec('X04',1371024876,'설치 조건을 둔 rasterio 직접 호출과 필요 시 intake 지원경로를 질문과 함께 제공.','제안 없음','open_mfdataset(paths,engine=rasterio)','no_prior_proposal'),
                  rec('X04',1375736147,'작성자가 덧붙인 문서의 rasterio 누락을 직접 인용하며 동적 entrypoint와 list_engines를 설명. 성공 보고 뒤의 설명이다.','rasterio 직접 호출','같은 호출 + list_engines로 설치 engine 찾기','same_candidate_option_or_explanation','explicit_to_volunteered_docs_gap',True,False,change_follows_execution=True)],
 executions=[run('X04',1372480571,'작성자가 glob 경로목록에 제시된 rasterio 호출을 적용해 동작했다고 보고. 직접 파일 열기 부분목표 성공이며 geospatial metadata 전 항목 검증과 intake 통합 출력은 없음.','success',full_goal='geospatial_metadata_preservation_and_intake_integration_unconfirmed')],
 technical_sources=['XD03','XD05','XD09b'],
 unknowns=[dict(fact='질문 전 opening_call 및 지리정보 전체 보존',reason='답은 안내 후 새 실행을 묘사하고 출력/원본 파일 비교는 제공하지 않음',last_url='https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571',next_evidence='질문 전 실제 호출과 동일 GeoTIFF의 열기 후 CRS/transform 비교')])
D['X05'].update(
 questions=[q('X05',2261543510,'X05-later-copy-semantics',['copy_identity_and_siblings'],'제3자가 DataTree 복사 변경이 기존 bart의 Lisa sibling 관계에 미치는 뜻을 확인. root30 밖의 구현 의미 질문.',kind='design_semantics_request')],
 answers=[ans('X05',2261578914,'X05-later-copy-semantics',['copy_identity_and_siblings'],'원본 bart와 homer.children의 복사본이 다르며 복사본에만 sibling이 생긴다고 설명.','design_semantics_answer',False)],
 recommendations=[rec('X05',2200630262,'같은 개발자가 shallow copy 및 parent argument 제거 두 제안에 동의하고 기존 설계 이유를 설명.','root의 두 제안','두 제안에 대한 동의','no_change')],
 other_events=[event('X05',2218045878,'지원자가 두 PR에서 변경했다고 보고. 사용자 실행 보고와 분리.',category='supplier_feature_development'),event('X05',2336405553,'공급자가 PR9297로 닫힐 사안이라고 언급.',category='supplier_pr_reference')],
 unknowns=[dict(fact='요청자가 새 생성자를 실행해 원본 불변을 검증했는지',reason='PR/설계 답은 있지만 작성자의 실행 없음',last_url='https://github.com/pydata/xarray/issues/9196#issuecomment-2336405553',next_evidence='PR9297 테스트 및 작성자의 동일 예제 출력')])
D['X06'].update(
 other_events=[],
 unknowns=[dict(fact='storage_options 전달 수정의 실행 결과',reason='공개 댓글은 환영 봇뿐이며 작성자의 fork commit 참조는 실행 증거가 아님',last_url='https://github.com/pydata/xarray/issues/9197',next_evidence='fork commit 3fc9d5579e40cec47ea89c3c0e656e493789f80f의 관련 테스트와 작성자 실행 결과')])
D['X07'].update(
 questions=[q('X07',2205973053,'X07-pure_xarray_reproducer_meaning',['pure_xarray_reproducer_meaning'],'초보 기여자가 요청자/유지관리자에게 pure-xarray reproducer의 뜻을 요청. 일반 지원자→사용자 구도와 역할이 반대.',first=True),
            q('X07',2206433913,'X07-requester-asks-experience',['previous_xarray_use'],'원 작성자가 newcomer에게 xarray 사용 경험을 역으로 질문.',target='non_root_author')],
 answers=[ans('X07',2206433913,'X07-pure_xarray_reproducer_meaning',['pure_xarray_reproducer_meaning'],'외부 wrapper를 제거한 최소 예제가 unit test가 될 수 있다는 의도를 설명.','direct_existing_new_disclosure',True)],
 other_events=[event('X07',2292210004,'다른 사람이 drop_indexes를 사용한 순수 xarray 예제로 기존 오류를 재현. 원 요청자의 실행이 아님.',category='third_party_reproduction')],
 technical_sources=['XD04'],
 unknowns=[dict(fact='질문한 newcomer의 다음 코드 선택/실행',reason='해당 질문자 후속이 없고 제3자가 재현을 제출',last_url='https://github.com/pydata/xarray/issues/9201#issuecomment-2292210004',next_evidence='Shripad1020의 해당 재현/패치 제출 또는 실행 보고')])
D['X08'].update(
 questions=[q('X08',2218309083,'X08-parent-coordinate-handling',['coordinate_handling_location'],'제3자가 부모 DataWithCoords가 좌표 처리 대부분을 맡아야 하는지 설계 함의를 질문.',kind='design_semantics_request'),
            q('X08',2338399208,'X08-rephrase-design-intent',['parent_coords_property_interpretation'],'원 작성자가 앞선 제안의 의미를 다시 물음. 원 요청자에게 값을 요구하는 질문이 아님.',kind='design_semantics_request',target='non_root_author')],
 answers=[ans('X08',2338399208,'X08-parent-coordinate-handling',[], 'DataTree/Dataset/DataArray 상속과 coords property를 뜻하는지 되묻고 다른 토론을 연결. 직접 설계값 답은 아님.','clarifying_requestion',False)],
 recommendations=[rec('X08',2201515514,'Coordinates는 variable/index에 접근하는 얇은 wrapper로 유지하는 설계 의견.','root의 dict 분리 제안','Coordinates wrapper 제약 설명','no_prior_proposal')],
 unknowns=[dict(fact='설계 선택과 실제 실행',reason='root90 안은 토론 및 되묻기에 그치고 구현/원 작성자 실행 없음',last_url='https://github.com/pydata/xarray/issues/9203#issuecomment-2338399208',next_evidence='issue9204 연결 댓글의 해당 설계 결정과 결과 테스트')])
D['XB03'].update(
 questions=[q('XB03',1510016072,'XB03-question_focus',['question_focus'],'질문이 CuPy의 scalar 반환에 관한 것인지 맥락을 요청.',first=True),
            q('XB03',1515600072,'XB03-later-preference',['avoid_special_casing'],'array API mixed-library 범위 밖 설명 뒤 특정 라이브러리 special case를 없애려는 선호가 맞는지 확인.')],
 answers=[ans('XB03',1510169910,'XB03-question_focus',['question_focus'],'중첩 dask/cupy의 0D scalar 변환 문제를 재진술하고 array API where가 array만 받는 이유를 보충.','restatement_already_present',True,core_value_present_in_current_root=True,pre_first_version_proven=False,new_qualification='array namespace에서 scalar를 array로 변환해야 하는 이유'),
          ans('XB03',1516251985,'XB03-later-preference',['avoid_special_casing'],'special case 제거를 선호하나 유지에 반대하지 않는다고 답하면서 Python scalar 지원의 호환성 목표를 더 정확히 정의.','preference_temporality_unconfirmed',False,direct_answer_content=True)],
 recommendations=[rec('XB03',1515600072,'같은 응답자가 보충 설명을 인정하고 array API의 혼합 라이브러리 동작은 범위 밖임을 연결. 질문 전에 기술 후보 제안은 없음.','제안 없음','array API issue399 설명 + 선호 재질문','no_prior_proposal','explicit_acknowledgment',True),
                  rec('XB03',1516494141,'다른 지원자가 SciPy의 단일 array type 정책과 xp.asarray 명시 변환을 제안.','다른 지원자의 제안 없음','mixed arrays 제한 및 내부 명시 변환','no_prior_proposal','analyst_inference',False)],
 technical_sources=['XD11'],
 unknowns=[dict(fact='선호가 질문 전에 있었는지 및 실제 후보 채택',reason='답에서 선호를 말했으나 형성 시점은 없고 실행/선택 승인도 없음',last_url='https://github.com/pydata/xarray/issues/7721#issuecomment-1516251985',next_evidence='동일 목표의 질문 전 설계 메모 또는 후속 패치/테스트')])
D['XB06'].update(
 questions=[q('XB06',2316054396,'XB06-xarray_specific_reproduction',['xarray_specific_reproduction'],'16개월 뒤 xarray 고유 문제라는 자료를 요청하고 synchronizer 전달을 제안. 첫 댓글은 작성자 답 이후에도 편집됨.',first=True)],
 answers=[ans('XB06',2318466786,'XB06-xarray_specific_reproduction',[], 'xarray 고유인지 여전히 모르며 기존 tenacity 우회를 계속 쓴다고 답하고 로그를 추가하겠다고 함.','unknown_value_and_retrospective_workaround',False),
          ans('XB06',2331409793,'XB06-xarray_specific_reproduction',[], '새 로그의 오류는 남지만 저장장치와 xarray/zarr 원인 분리는 여전히 모르겠다고 답.','diagnostic_failure_without_requested_discriminator',False,version_changed=True)],
 recommendations=[rec('XB06',2316054396,'synchronizer를 to_zarr에도 전달하고 xarray 고유 여부를 확인하도록 제안.','제안 없음','synchronizer 전달 및 원인 경계 진단','no_prior_proposal')],
 executions=[run('XB06',2331409793,'2024-09-04 로그에서 오류가 계속 발생함을 보고. root의 2022.11.0에서 2024.7.0으로 바뀌었고 새 로그만 late question30에 속함.','failure',full_goal=False,version_changed=True,late_question_extension=True),
             run('XB06',2318466786,'tenacity 우회는 원 게시 시점부터 사용한 것으로 회상됨. 새 채택 성공 아님.','workaround_report',full_goal='미확인',new=False,late_question_extension=True)],
 unknowns=[dict(fact='xarray 고유 재현과 원판 동일환경의 원인',reason='작성자가 원인 판별을 모른다고 하고 후속 판이 달라짐',last_url='https://github.com/pydata/xarray/issues/7726#issuecomment-2331409793',next_evidence='동일 데이터/판에서 direct zarr 대 xarray, SMB 대 local SSD 비교 로그')])
D['XB08'].update(
 questions=[q('XB08',1498971031,'XB08-versions',['versions'],'실행 판 정보를 요청.',first=True)],
 answers=[ans('XB08',1499263329,'XB08-versions',['versions'],'작성자가 본문에 버전 정보를 추가했다고 명시. 현재 root의 버전 표를 첫 답 전 제공 값으로 세면 안 됨.','direct_existing_new_disclosure',True,answer_location='edited_root_environment',exact_historical_table_version='미확인')],
 recommendations=[rec('XB08',1499872700,'동일 지원자가 align/broadcast/transpose 복사와 CFTimeIndex 재검증을 진단하고 flox222 연결. 답 전 기술제안 없음.','제안 없음','복사/CFTimeIndex 진단','no_prior_proposal','temporal_only',True),
                  rec('XB08',1499878014,'정렬된 그룹이므로 engine=flox가 빠르다는 지원자 자신의 벤치마크와 옵션 제시. 버전 답 때문에 선택됐다는 명시 연결 없음.','제안 없음','engine=flox 옵션과 지원자 벤치마크','no_prior_proposal','explicit_to_sorted_groups_not_version_answer',True)],
 other_events=[event('XB08',1505309893,'작성자는 감사만 남김. 새 실행/성능 측정 아님.',category='thanks_only'),event('XB08',1499878014,'지원자의 벤치마크 출력은 존재하나 작성자 실행이 아님.',category='supplier_benchmark')],
 unknowns=[dict(fact='작성자가 추천 옵션을 새로 적용한 실제 성능',reason='작성자 후속은 감사뿐이며 벤치마크는 지원자',last_url='https://github.com/pydata/xarray/issues/7730#issuecomment-1505309893',next_evidence='작성자의 원 데이터/동일 판에서 engine별 실행 결과')])
D['XB13'].update(
 questions=[q('XB13',1508940623,'XB13-input',['input_location','input_filename'],'실제로 여는 대상이 local file인지와 파일 이름을 요청.',first=True),
            q('XB13',1509585164,'XB13-trial-engine',['explicit_netcdf4_trial_result'],'engine=netcdf4를 지정해 시험해 보라는 새 행동 요청.',kind='action_request')],
 answers=[ans('XB13',1509390748,'XB13-input',['input_location','input_filename'],'local file이라고 답하고 실제 .nc 이름 및 독립 open_dataset 호출을 제공.','direct_existing_new_disclosure',True),
          ans('XB13',1510522371,'XB13-trial-engine',[], 'Python과 입력 파일을 바꾸어 해결했다고 함. engine=netcdf4 시험 여부는 답하지 않음.','different_target_and_environment_success',False)],
 recommendations=[rec('XB13',1509585164,'파일 이름을 받은 뒤 netcdf4 engine 명시 시험을 제안. 처음 질문 전에는 실행 후보가 없고 netCDF4 형식이라는 가정은 독립 검증하지 않음.','제안 없음','open_dataset(engine=netcdf4) 진단','no_prior_proposal','implicit_filename_based_inference',True)],
 executions=[run('XB13',1509390748,'같은 파일을 독립 xr.open_dataset 호출로 열었으나 같은 오류가 난다고 보고.','failure',full_goal=False),
             run('XB13',1510522371,'Python3.9로 내리고 다른 파일을 사용하니 동작했다고 보고. 원 파일 성공과 구별.','success',same_target=False,full_goal='original_file_unconfirmed',environment_changed=True)],
 unknowns=[dict(fact='원래 입력 파일의 실제 형식/내용과 해결',reason='다른 파일 성공이며 원 파일은 독립 열기 실패. 공개 SharePoint 링크의 원 데이터는 열지 않음',last_url='https://github.com/pydata/xarray/issues/7754#issuecomment-1510522371',next_evidence='원 파일의 공개 magic bytes/ncdump와 engine=netcdf4 결과')])
D['XB14'].update(
 questions=[q('XB14',1509537842,'XB14-backend-and-remote',['backend','remote_kind'],'backend와 실제 server/remote filesystem 구분을 질문.',first=True),
            q('XB14',1509899180,'XB14-remote-rephrase',['remote_kind'],'remote filesystem은 mounted NFS를 뜻한다고 풀이하고 https처럼 보인다고 확인.',kind='information_request')],
 answers=[ans('XB14',1509633511,'XB14-backend-and-remote',['backend'],'netCDF4라고 답하고 OPeNDAP URL을 주지만 server와 remote filesystem의 차이는 모른다고 함.','direct_existing_new_disclosure',True,partial_variables=['remote_kind']),
          ans('XB14',1509899467,'XB14-remote-rephrase',['remote_kind'],'설명을 듣고 아무 것도 mount하지 않으므로 real server라고 답.','direct_existing_new_disclosure',True)],
 recommendations=[rec('XB14',1509899180,'같은 지원자가 질문에 쓴 용어를 풀이. 기술 후보를 바꾼 것은 아님.','모호한 server/filesystem 질문','mounted NFS 대 HTTPS로 풀이','same_candidate_option_or_explanation','explicit_to_terminology_confusion',True,False),
                  rec('XB14',1516738260,'다른 지원자가 netCDF4 remote access의 기존 retry 구현을 연결하고 설정 가능하지 않다고 설명.','제안 없음','기존 retry 코드 및 설정 한계','no_prior_proposal','explicit_to_backend_context',False)],
 other_events=[event('XB14',1521731294,'작성자가 32–64초 대기는 너무 길며 설정 가능해야 한다고 말함. 새 실행 결과는 아님.',category='later_tolerance_preference')],
 technical_sources=['XD07','XD08'],
 unknowns=[dict(fact='질문 뒤 작성자의 새 timeout/실행 결과',reason='설정 선호가 구체화되지만 작성자 시험 보고가 없음. retry는 open_dataset 전체 timeout 보장이 아님',last_url='https://github.com/pydata/xarray/issues/7758#issuecomment-1521731294',next_evidence='동일 endpoint에서 open/read 단계별 timeout 실측과 설정 적용 결과')])

D['XB08']['late_history']=[
 event('XB08',1709120441,'2023-09-06 원 작성자가 다시 조사하여 numpy maximum.at 원인과 engine=flox 속도 개선을 보고. root+153일 뒤로 root90 및 최초question30 모두 밖이다.',category='late_author_execution_report',same_goal=True,same_input_and_version='미확인',count_in_root30=False,count_in_root90=False),
 event('XB08',1709773599,'지원자가 numpy 문제와 개선판 논의를 연결. 90일 주·후속 분모 밖.',category='late_supplier_explanation',count_in_root30=False,count_in_root90=False)]
D['XB14']['questions'][1]['question_episode_id']='XB14-backend-and-remote'
D['XB14']['questions'][1]['continuation_of']='XB14-backend-and-remote'

PAG={r['issue_number']:r for r in json.loads((P/'pagination-followup-receipts.json').read_text())}
CHAINS=[]
for cid in SEL:
    i=I[cid]; d=D[cid]; root=stamp(i['created_at']); raw=C[cid][1]; comments=raw['data']; human=[c for c in comments if not c['user']['login'].endswith('[bot]')]
    for a in d['answers']:
        qu=next(z for z in d['questions'] if z['question_id']==a['question_id'])
        a['answer_within_root30']=a['within_root30'];a['answer_within_root90']=a['within_root90']
        a['answer_within_question30']=stamp(a['at'])<=stamp(qu['at'])+dt.timedelta(days=30)
        a['wait_hours']=round((stamp(a['at'])-stamp(qu['at'])).total_seconds()/3600,4)
        a['roundtrip_key']=f"{cid}:{qu['comment_id']}:{a['comment_id']}"
        a['question_url']=qu['url']
        episode_start=min(stamp(z['at'])for z in d['questions']if z['question_episode_id']==qu['question_episode_id'])
        a['question_episode_id']=qu['question_episode_id']
        a['episode_elapsed_hours']=round((stamp(a['at'])-episode_start).total_seconds()/3600,4)
    summaries={}
    for window in ['root30','root90']:
        w='within_'+window
        qq=[q for q in d['questions'] if q[w] and q['real_information_request'] and q['target']=='root_author']
        aa=[a for a in d['answers'] if a[w] and a['strict_same_variable_answer'] and a['question_id'] in {q['question_id'] for q in qq}]
        rr=[r for r in d['recommendations'] if r[w] and r['strict_linked_recommendation_change']]
        ee=[e for e in d['executions'] if e[w] and e['new_execution'] and e['is_root_author'] and e['same_original_target']]
        summaries[window]=dict(actual_information_question=bool(qq),question_utterances=len(qq),question_episodes=len({q['question_episode_id']for q in qq}),
            same_variable_direct_answer=bool(aa),strict_answer_variable_count=sum(len(a['variables']) for a in aa),
            direct_new_disclosure=any(a['category']=='direct_existing_new_disclosure'for a in aa),
            restatement_already_present=any(a['category']=='restatement_already_present'for a in aa),
            strict_answer_roundtrips=len({a['roundtrip_key']for a in aa}),
            any_author_reply_roundtrips=len({a['roundtrip_key']for a in d['answers']if a[w] and a['is_root_author'] and a['question_id']in {q['question_id']for q in qq}}),
            linked_recommendation_change=bool(rr),new_execution_success=any(e['result']=='success'for e in ee),
            new_execution_failure=any(e['result']=='failure'for e in ee),chain_success=False,
            no_direct_answer=bool(qq)and not aa,observable_public_comments=True,
            full_goal_success=False,full_goal_success_unknown=any(e['result']=='success'and e['full_original_goal']is not True for e in ee))
    questions_wait=[]
    for qq in d['questions']:
        if not qq['real_information_request'] or qq['target']!='root_author':continue
        aa=[a for a in d['answers']if a['question_id']==qq['question_id']]
        direct=[a for a in aa if a['strict_same_variable_answer']and a['answer_within_question30']]
        questions_wait.append(dict(question_id=qq['question_id'],question_url=qq['url'],
            first_author_reply_hours=min([a['wait_hours']for a in aa],default=None),
            first_strict_direct_answer_hours=min([a['wait_hours']for a in direct],default=None),
            question30_end=iso(stamp(qq['at'])+dt.timedelta(days=30)),
            no_strict_answer_observed_in_question30=not direct,waiting_upper_bound_hours=720,
            late_question_extension=not qq['within_root90'],clicks='미확인',reading_minutes='미확인',substitutable_labor='미확인'))
    tl=P/'retrieved'/f"timeline-{i['issue_number']}.json"
    timeline=json.loads(tl.read_text())if tl.exists()else None
    refs=[]
    if timeline:
        for t in timeline['data']:
            when=t.get('created_at')or t.get('committer',{}).get('date')
            if when and stamp(when)>root+dt.timedelta(days=90):continue
            if t.get('event')in ['cross-referenced','referenced','committed']:
                refs.append({k:t.get(k)for k in ['event','created_at','commit_id','commit_url','source']if k in t})
    row={k:i[k]for k in ['case_id','root_url','issue_number','created_at','author','author_association','first_strategy','request_type','information_score','original_grade','exposure']}
    row.update(sample='A'if not cid.startswith('XB')else'B',t0_seal_sha=SEAL,adjudicator='/root/xarray same worker post-seal reading',checked_utc=NOW,
        exposure_confirmed_after_followup=(cid=='XB08'),
        first_question=i['first_strategy']in['information_request','mixed'],late_first_response=i['late_first_response'],
        windows=dict(root30_end=iso(root+dt.timedelta(days=30)),root90_end=iso(root+dt.timedelta(days=90)),calendar_windows_closed=True),
        observation=dict(status='public_visible_comments_complete',page1_url=raw['url'],page1_count=len(comments),page2_receipt=PAG[i['issue_number']],
            root30_human_comments=sum(stamp(c['created_at'])<=root+dt.timedelta(days=30)for c in human),
            root90_human_comments=sum(stamp(c['created_at'])<=root+dt.timedelta(days=90)for c in human),
            root90_comment_ids=[c['id']for c in human if stamp(c['created_at'])<=root+dt.timedelta(days=90)],
            last_public_comment_url=comments[-1]['html_url']if comments else i['root_url'],
            deleted_content='미확인: 현재 공개 API에는 삭제 본문 복원이 없으며 알려진 누락 흔적은 없음',
            timeline_url=timeline.get('url')if timeline else None,timeline_count=len(timeline['data'])if timeline else None,
            timeline_page2=next(z for z in json.loads((P/'timeline-pagination-receipts.json').read_text())if z['issue_number']==i['issue_number']),
            same_event_references=refs,cross_reference_contents='linked commit/PR 존재만 확인; 테스트/실행을 확인한 것으로 보지 않음'),
        summary=summaries,waiting=questions_wait,**d)
    CHAINS.append(row)
write_jsonl('chains.jsonl',CHAINS)

LATER=[]
for r in CHAINS:
    for qq in r['questions']:
        if qq['first_substantive_response']:continue
        LATER.append(dict(case_id=r['case_id'],sample=r['sample'],root_url=r['root_url'],question_id=qq['question_id'],
            question_at=qq['at'],question_url=qq['url'],questioner=qq['author'],target=qq['target'],variables=';'.join(qq['variables']),
            kind=qq['kind'],real_information_request=qq['real_information_request'],within_root30=qq['within_root30'],
            within_root90=qq['within_root90'],prediction_status='post_outcome_read_no_retrospective_seal',summary=qq['summary']))
with (P/'later-questions.csv').open('w',newline='')as f:
    w=csv.DictWriter(f,fieldnames=list(LATER[0]));w.writeheader();w.writerows(LATER)

CORRECTIONS=[
 dict(correction_id='XC01',case_id='XB08',field='current root versions / exposure',frozen_t0='questions.csv versions value_in_initial=unclear; initial.exposure=false',
      finding='작성자가 첫질문 뒤 버전을 위 본문에 추가했다고 확인. T0 판독은 이 후발 편집을 포함했으므로 confirmed retrospective-value exposure=true.',
      evidence='https://github.com/pydata/xarray/issues/7730#issuecomment-1499263329',effect='초기값이 이미 있었다는 분자에서 제외; 미래 정보 미노출 감도분석에서 제외; 원판 U 유지',modified_frozen=False),
 dict(correction_id='XC02',case_id='X04',field='opening_call answer temporal status',frozen_t0='opening_call absent; direct-open/intake branches sealed',
      finding='답은 제시된 방식으로 새로 실행한 호출이다. 질문 전에 가지고 있던 호출값의 공개로 확정하지 않음.',
      evidence='https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571',effect='strict existing-value answer=false; content-direct expanded sensitivity=true; 새 파일열기 성공은 별도 양성',modified_frozen=False),
 dict(correction_id='XC03',case_id='XB06',field='first comment version / late window',frozen_t0='late first response 2024-08-28; original root U',
      finding='first comment edited 2024-08-29 after author reply; author quoted requested discriminator, providing partial support. 후속 실행은 root2022.11.0과 달리2024.7.0.',
      evidence='https://github.com/pydata/xarray/issues/7726#issuecomment-2318466786',effect='root30/90에는 질문/답/실행 양성 없음; question30 extension 별도; 원인판별은 미확인',modified_frozen=False),
 dict(correction_id='XC04',case_id='X02',field='later question current body',frozen_t0='first response conditional_action retained',
      finding='later error request comment updated19:24:15, author pledge19:21:42. traceback clause timing not fully prior; error request still supported by reply.',
      evidence='https://github.com/pydata/xarray/issues/7408#issuecomment-1369974685',effect='실제 오류요청 존재 유지, exact traceback timing 부분미확인; 값 답변 없음',modified_frozen=False)
]
for c in CORRECTIONS:c.update(checked_utc=NOW,t0_seal_sha=SEAL)
write_jsonl('corrections.jsonl',CORRECTIONS)

# Locations refer to the cached current body present at T0, not a recovered creation-time original.
FIELD={
 'X01': [('goal','present','3,62-69','CF grid mapping을 보존하며 다른 encoding으로 저장'),('tried','present','55-66','원 encoding 저장과 명시 dtype 저장의 비교'),('version_settings_input','present','5-53,57,64,71','NetCDF 구조, decode_coords, dtype, Python/xarray 판'),('desired_output','present','3,60,66-69','grid_mapping과 CF 관련 속성 보존'),('preferences','present','69','자료형 변경이 grid mapping을 없애지 않기를 원함'),('requirements','present','3','CF 적합성'),('prohibitions','absent','1-71','별도 금지 없음')],
 'X02': [('goal','present','3,9','같은 이름 새 Zarr datasets를 테스트마다 독립 사용'),('tried','present','3','단독 테스트 성공, 연속쓰기 오류'),('version_settings_input','partial','3','open_zarr/to_zarr 및 동일 이름; 버전/실데이터/호출 없음'),('desired_output','present','9,13','cached state 없는 독립 테스트 또는 clear method'),('preferences','present','13','undocumented 방법이어도 pointer와 문서화 희망'),('requirements','present','9','테스트 간 cached state 없음'),('prohibitions','absent','1-17','별도 금지 없음')],
 'X03': [('goal','present','3','chunked DataArray의 dask 객체 직접 변환'),('tried','unconfirmed','7-24','제안 코드이며 실행했다고 명시하지 않음'),('version_settings_input','partial','9-23','1D/2D 구현 제안; 판과 실제 데이터 없음'),('desired_output','present','13,23','dask Series 또는 DataFrame'),('preferences','present','3,7','직접 변환과 덜 복잡한 방법 선호'),('requirements','present','15-16','제안 코드의 2D 초과 거절 조건; 제품 전체 필수조건 아님'),('prohibitions','absent','1-24','별도 사용자 금지 없음')],
 'X04': [('goal','present','3,8,12','여러 GeoTIFF를 지리정보 보존하여 열기'),('tried','partial','12','dask-image 대안의 손실 설명; 실제 사용자 호출/실행여부 불명'),('version_settings_input','partial','3,8,12','GeoTIFF/rasterio/intake 이름; 버전/설치목록/호출 없음'),('desired_output','present','12','geospatial information 보존'),('preferences','present','8','intake_xarray의 rasterio 경로 제안'),('requirements','present','12','지리정보 보존 필요'),('prohibitions','absent','1-16','명시적 금지 없음')],
 'X05': [('goal','present','3,28,43-45','DataTree 생성자가 입력을 부수적으로 바꾸지 않게 함'),('tried','present','5-40','parent, child, reuse 예제와 출력'),('version_settings_input','partial','7-40','DataTree 코드와 출력; 정확한 설치판 없음'),('desired_output','present','43-45','shallow copy 및 parent arg 제거'),('preferences','present','43-45','두 설계 권고'),('requirements','present','3','반환과 입력수정을 동시에 하지 않는 관습 주장'),('prohibitions','partial','3,45','입력 변형 회피; parent 제거는 consider 수준')],
 'X06': [('goal','present','3','private S3 Zarr에서 datatree 열기'),('tried','present','3-8,16-27','open_datatree 예제 오류와 과거 신고'),('version_settings_input','present','16-27,68-121','placeholder storage_options와 xarray2024.6.0/zarr2.18.2'),('desired_output','present','10-12,64-66','storage_options를 내려보내어 store 열기'),('preferences','present','44-66','구체 수정안'),('requirements','present','3,12','private S3 접근 옵션 전달'),('prohibitions','absent','1-121','명시적 금지 없음')],
 'X07': [('goal','present','3,91-99','coordinate/index 오류문구 정확화'),('tried','present','7-90','VirtualiZarr 우회 예제와 traceback'),('version_settings_input','partial','5,7-90','입력 코드/옵션/traceback; 정확한 xarray 판 없음'),('desired_output','present','93-97','문제 차원과 index 부재를 포함한 오류문구'),('preferences','present','5,99','pure-xarray repro 및 함수명 개선 제안'),('requirements','partial','3,91','index 없음과 coordinate 없음 구별'),('prohibitions','absent','1-99','별도 금지 없음')],
 'X08': [('goal','present','1,5','Dataset data/coord variables 분리 토론'),('tried','absent','1-8','실행/수정 시도 없음'),('version_settings_input','partial','5','기존 내부 dict/set 설계 설명; 판/입력 없음'),('desired_output','present','5','data_variables/coord_variables 별도 dict'),('preferences','present','5','DataArray와 구조 정합'),('requirements','absent','1-8','필수조건 명시 없음'),('prohibitions','absent','1-8','금지 없음')],
 'XB03': [('goal','present','1,143-153','중첩 cupy/dask의 where와 scalar 변환 지원'),('tried','present','7-20,143-149','plain 성공/chunk 실패/cupy nan 우회'),('version_settings_input','partial','7-20,141,153','입력 예제와 코드 SHA; 설치 판 목록 없음'),('desired_output','present','13-16,146-149','masked array의 동일 결과'),('preferences','present','153','dask 특수처리 축소와 nested duck array 호환'),('requirements','partial','153','다른 duck layer를 깨지 않는 방법'),('prohibitions','absent','1-155','명시적인 금지 없음')],
 'XB06': [('goal','present','3-8,18-20','네트워크 Zarr concurrent region read/write 오류 회피'),('tried','present','3-8,24-99','ProcessSynchronizer 사용 및 재현 실패한 MCVE'),('version_settings_input','present','3-5,24-99,161-218','실제 network와 별도 localSSD sync 경로; 예제와 실제 환경 다름; 설치판'),('desired_output','present','18-20','permission error 없음'),('preferences','absent','1-218','명시적 선호 없음'),('requirements','present','4','chunk 비정렬 region 쓰기 동기화'),('prohibitions','absent','1-218','명시적 금지 없음')],
 'XB08': [('goal','present','3,7','cftime groupby 성능이 기존 naive 구현 이상'),('tried','present','11-42,54-64','flox on/off와 engine 비교'),('version_settings_input','present','11-42,71-127','30년 noleap 예제와 현재 버전 표; 표의 최초시점은 봉인 시 미확인'),('desired_output','present','7','naive 구현에 뒤지지 않는 성능'),('preferences','present','3,7','flox를 끄는 우회보다 정상 가속 기대'),('requirements','absent','1-127','별도 hard constraint 명시 없음'),('prohibitions','absent','1-127','명시적 금지 없음')],
 'XB13': [('goal','present','5,49','climate_indices가 입력 dataset을 열도록 함'),('tried','present','43-48','pip/conda 의존 설치 후 재시도 실패'),('version_settings_input','partial','5,7-40','Python3.11.3, traceback과 IO backends; 실제 filename/형식/입력data 없음'),('desired_output','partial','5,49','오류 해결을 묻지만 성공 출력 구체화 없음'),('preferences','absent','1-49','명시적 선호 없음'),('requirements','absent','1-49','현재 Python판을 고수해야 한다는 조건 없음'),('prohibitions','absent','1-49','명시적 금지 없음')],
 'XB14': [('goal','present','3,7','원격 open_dataset 대기에 timeout 지정'),('tried','present','3','서버 문제 때 script freeze 경험'),('version_settings_input','absent','1-15','backend/판/실제URL/호출/timeout 값 없음'),('desired_output','present','7','지정 시간 뒤 timeout'),('preferences','present','11','HEAD 우회보다 native timeout 선호'),('requirements','partial','7','사용자가 대기 상한 지정 가능해야 함'),('prohibitions','absent','1-15','명시적 금지 없음')]
}
AUD=[]
for cid in SEL:
    i=I[cid];b=ROOTS[i['issue_number']]['body'];h=sha(b)
    AUD.append(dict(case_id=cid,root_url=i['root_url'],t0_seal_sha=SEAL,t0_root_sha256=i['root_sha256'],
        cache_matches_t0=h==i['root_sha256'],audit_utc=NOW,audit_stage='post_outcome_location_audit_not_original_preseal_judgement',
        original_grade=i['original_grade'],temporal_limit='현재 T0 캐시의 절 위치; creation-time 원판 복원이 아님. 후속에서 배운 값을 보충하지 않음.',
        fields=[dict(field=f,status=s,root_body_lines=loc,summary=value,source_url=i['root_url'])for f,s,loc,value in FIELD[cid]],
        first_goal_provenance='shoyer의 issue9063 댓글을 TomNicholas가 가져옴'if cid=='X08'else'root 작성자가 현재 본문에서 공개; 작성 당시 원판 전체는 미확인',
        followup_correction_id='XC01'if cid=='XB08'else None))
write_jsonl('initial-field-audit.jsonl',AUD)

print(json.dumps({'cases':len(CHAINS),'later_questions':len(LATER),'audit_cases':len(AUD),'audit_hashes_all_match':all(x['cache_matches_t0']for x in AUD),
 'A_root30':{k:sum(r['summary']['root30'][k]for r in CHAINS if r['sample']=='A')for k in ['actual_information_question','same_variable_direct_answer','linked_recommendation_change','new_execution_success','new_execution_failure']},
 'B_root30':{k:sum(r['summary']['root30'][k]for r in CHAINS if r['sample']=='B')for k in ['actual_information_question','same_variable_direct_answer','linked_recommendation_change','new_execution_success','new_execution_failure']}},ensure_ascii=False,indent=2))
