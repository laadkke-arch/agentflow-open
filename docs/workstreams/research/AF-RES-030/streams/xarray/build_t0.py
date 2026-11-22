from pathlib import Path
import json,csv,hashlib,re,datetime
P=Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
frames={k:json.loads((P/'retrieved'/f'frame-{k}.json').read_text()) for k in ['A1','A2','B']}
roots={x['number']:x for f in frames.values() for x in f['data']['items']}
sel=json.loads((P/'selected-roots.json').read_text())
cur={
7406:('bug',5,'NetCDF를 다시 저장할 때 CF grid_mapping을 보존하면서 dtype를 바꿈','decode_coords=all; tas; xarray2022.3.0/Python3.10.5; dtype=float32 encoding 제공 시 grid_mapping 소실','information in current root What is your issue / input ncdump / two to_netcdf calls','directive',False),
7408:('feature',3,'동일 이름의 새 Zarr 데이터셋을 테스트마다 독립적으로 쓰고 읽음','open_zarr/to_zarr; 개별시험은 동작, 연속쓰기 시 기존변수 갱신으로 인식; cache 초기화 방법 요청','root problem/desired solution/alternatives','conditional_action',False),
7409:('feature',3,'chunked DataArray를 dask dataframe/series로 직접 변환','1D/2D 처리 알고리즘 제안; 2D 초과 ValueError; 임시Dataset 방식은 root에 없음','root problem/solution code','directive',False),
7411:('feature',3,'여러 GeoTIFF를 geospatial metadata 보존하여 open_mfdataset로 열기','rasterio engine/intake_xarray 제안; dask-image에서 지리정보 손실; 실제 호출코드 없음','root problem/solution/alternatives','mixed',True),
9196:('design',4,'DataTree 생성시 입력 parent/children의 원본 변형을 피함','생성·재사용 코드; shallow copy와 parent arg 제거의 두 제안','root examples/suggestions1–2','directive',False),
9197:('bug',5,'private S3의 Zarr store를 open_datatree로 열기','GroupNotFoundError; storage_options 전달누락 제안; xarray2024.6.0/zarr2.18.2; placeholder credentials only','root happened/example/proposed fix/environment','no_substantive_response',False),
9201:('bug',4,'combine_by_coords의 좌표는 있으나 index없는 경우 오류를 정확히 설명','VirtualiZarr shortcut; time coordinate exists but no index; 순수xarray reproducer 가능성','root reproducer/error/desirable message','information_request',True),
9203:('design',2,'Dataset 내부 data/coordinate variables를 별도 dict로 분리','현재 variables dict+coord_names set; shoyer의 이전 설계제안을 TomNicholas가 별도논의로 옮김','root quoted design suggestion and attribution','directive',False),
7710:('usage',3,'기존 Zarr 특정 time region을 새 subset으로 갱신','sel/time slice/update/to_zarr 코드','root','directive',False),
7713:('bug',5,'tuple 입력으로 Variable/IndexVariable 생성','tuple(2,3,45),dim day; list는 작동,tuple은dim오류','root example','directive',False),
7721:('bug',4,'chunked cupy where/fillna에서 scalar dtype 변환 오류 회피','cupy arange/mask,dask chunk; numpy0D scalar로 바뀌어 실패; cupy nan우회','root example/diagnosis','information_request',True),
7722:('bug',5,'missing_value만 있던 NetCDF의 두 번째 roundtrip 저장','missing_value1,_FillValue nan 충돌; 두 정책 제안','root roundtrip','mixed',False),
7723:('bug',5,'명시 _FillValue없는 기본 NetCDF fill값 masking','fill_value=None,미기록원소; 기본값 적용 정책제안','root example','directive',False),
7726:('bug',5,'네트워크 Zarr의 다중 프로세스 read/write를 동기화','region chunk미정렬; localSSD ProcessSynchronizer; 제공예제는 재현실패라고 명시','root happened/example','mixed',True),
7727:('feature',3,'xarray에서 left/right shift 연산자 제공','numpy우회 가능; 초안 branch 제시','root','directive',False),
7730:('bug',5,'cftime 연도 resampling/groupby 성능 회귀','flox on/off와 numpy비교;30년365일 예제/실측; 현재 Environment에 xarray main@f8127fc,flox0.6.10 등 있음. 첫답이전 존재는 미확인','root example/results','information_request',True),
7733:('feature',2,'Blosc2 NDArray를 xarray backend로 사용','netcdf/zarr와 유사한 lazy datasource 희망','root','directive',False),
7737:('bug',4,'align(copy=False)시 복사 피하기','DataArray/groupby year; join outer,copyFalse; source link','root','information_request',False),
7742:('usage',2,'NetCDF char 저장이 만든 추가 차원의 의미 알기','char 저장/읽기; 두 이미지첨부, 코드텍스트 없음','root/image links not decoded in T0','directive',False),
7748:('bug',5,'존재하지않는 dimension.diff에 일관된 오류','DataArray arange10 dim a,diff b; expected exception','root example','mixed',False),
7754:('bug',3,'climate_indices에서 입력 dataset 열기 실패 해결','Python3.11.3; installed IO engines; dependencies 설치 재시도; 실제 file name없음','root traceback/tried installs','mixed',True),
7758:('feature',3,'원격데이터 fetch의 open_dataset timeout 지정','서버 network issue로 script freeze; HEAD request를 대안으로 고려','root problem/alternatives','information_request',True),
7759:('bug',5,'groupby_bins 결과-좌표 순서 일치','2023.4.0 vs2023.3.0, numpy/pandas 비교예제','root','directive',False),
7763:('bug',5,'DataArray concat의 입력순서와 무관한 오류 정책','다른차원 a/b/c 순서별 ValueError 여부;coords default','root example','no_substantive_response',False),
7764:('design',3,'xr.dot에 opt_einsum 선택 지원','np.einsum dropin,monkeypatch;backend kwarg numpy default제안','root','mixed',False),
7766:('bug',5,'groupby_bins 문자열 label과 실제그룹 대응 보존','2023.4.1 fix후 string sort문제;one/two 등 labels','root','no_substantive_response',False),
7767:('usage',4,'xr.where와 DataArray.where의 결과차이 이해','condition da<5; 함수/메서드 인자순서 및 출력차이','root code/outputs','directive',False),
7768:('feature',4,'curvefit의 p0를 experiment_index별로 지정','2D fit;DataArray 초기값;for-loop대안;scipy1.7구분 수정','root example/alternatives','directive',False),
7770:('feature',3,'custom backend 등록의 공개API 확보','BACKEND_ENTRYPOINTS 변경;netcdf globalvar와h5netcdf alignment','root','directive',False),
7772:('bug',4,'큰 NetCDF nbytes 조회의 강제메모리 로딩 피하기','생성코드;8.6GB vs size*dtype itemsize 대조','root example/results','directive',False),
7773:('bug',3,'ubuntu환경에서 OPeNDAP dataset 접근','2개 공개 URL;pip ubuntu failure vs conda WSLsuccess','root example/environments','directive',False),
7780:('bug',5,'numpy/xarray binary operation 반환형의 mypy 인식','x*v / v*x,values 속성; xarray2023.4.2,mypy1.2.0','root example/environment','directive',False),
7782:('bug',5,'DAP Byte를 float32대신 ubyte로 읽기','scfv/scfv_unc;_Unsigned true,_FillValue-1;DDS/DAS','root metadata/example','directive',False),
7789:('usage',4,'Azure Zarr를 account key대신 SAS로 읽기','storage_options.sas_token;account_name/key는 성공;connection_string오류','root example','no_substantive_response',False),
7790:('bug',5,'Zarr roundtrip에서 datetime64 NaT fill보존','NaT/_FillValue encoding;date2023-01-02;readback','root example','directive',False)
}
# (case number, variable, short exact quote, initial value, branch A, branch B, kind)
qdefs=[
(7411,'opening_call','could you post the way you\'re opening the geotiff files?','absent','rioxarray engine direct open succeeds → intake forwarding support','direct rasterio open fails → inspect engine installation/call','input'),
(9201,'pure_xarray_reproducer_meaning','what you mean by making a pure-xarray reproducer?','absent','asks how to remove VirtualiZarr → xarray-only data/index construction guidance','asks where to add test → contribution/testing guidance','goal_interpretation_role_reversal'),
(7721,'question_focus','Is the question about why CuPy wouldn\'t return scalars?','unclear','CuPy scalar-return contract → upstream CuPy explanation','xarray dask/cupy coercion → array dispatch boundary','goal'),
(7726,'xarray_specific_reproduction','Can we get any info this is an xarray-specific issue?','absent','fails only via xarray → xarray read/synchronizer path','also fails in direct zarr → upstream zarr coordination','input'),
(7730,'versions','Thanks can you add version info please','unclear: current root Environment contains versions; pre-first-response timing unconfirmed','old flox/xarray → inspect fixed-version behavior','current versions → current regression triage','environment'),
(7737,'fix_status','is it solved by #7736?','absent','reported fixed → close linked bug','reported not fixed → further fix required','action_confirmation_not_B'),
(7754,'input_location','What exactly did you try to open? A local file?','absent','local file → filename/format inspection','remote input → endpoint/protocol inspection','input'),
(7754,'input_filename','can you provide the name of this file?','absent','matching format/name → inspect actual content/backend','wrong name/path → correct input path','input'),
(7758,'backend','Which backend are you using?','absent','netcdf4/DAP → backend timeout mechanism','zarr/fsspec → filesystem/storage options','environment'),
(7758,'remote_kind','Is it a "real" server or simply a remote filesystem?','absent','service API → protocol/client timeout','remote filesystem → fs-layer timeout','input')
]
# Comments are downloaded but only first nonbot/nonauthor substantive node is used here.
skips={9201:{2202978259},7721:{1498773949}}
firsts={};metadata={}
for n in sel['A']+sel['B']:
 f=next((f for f in [P/'retrieved'/f'comments-{n}-rawconnector.json',P/'retrieved'/f'comments-{n}.json'] if f.exists()),None)
 d=json.loads(f.read_text());metadata[n]=d
 cs=[c for c in d['data'] if c['user']['login']!=roots[n]['user']['login'] and not c['user']['login'].endswith('[bot]') and c['id'] not in skips.get(n,set())]
 firsts[n]=cs[0] if cs else None
records=[];frows=[]
for sample,nums in [('A',sel['A']),('Bscreen',sel['B'])]:
 for i,n in enumerate(nums,1):
  x=roots[n]; c=firsts[n]; typ,score,goal,values,location,strategy,bok=cur[n];cid=f'X{i:02}' if sample=='A' else f'XB{i:02}'
  body=x.get('body') or ''; fquote=c['body'] if c else ''
  quote_bol=re.findall(r'^>\s*(.+)$',fquote,re.M)
  quote_match=[s for s in quote_bol if s.strip() and s.strip() in body]
  grade='Q' if (quote_match or n==7406) else 'U'
  exp=n==7406
  r={'case_id':cid,'sample':sample,'project':'pydata/xarray','root_url':x['html_url'],'issue_number':n,'created_at':x['created_at'],'root_updated_at':x['updated_at'],'checked_utc':metadata[n]['checked_utc'],'author':x['user']['login'],'author_association':x['author_association'],'maintainer_requester':x['author_association'] in ['MEMBER','OWNER','COLLABORATOR'],'quarter':'2023Q1' if n in sel['A'][:4] else '2024Q3' if sample=='A' else '2023-04','request_type':typ,'information_score':score,'goal':goal,'initial_values':values,'initial_location':location,'root_sha256':hashlib.sha256(body.encode()).hexdigest(),'original_grade':grade,'original_limit':'미확인: 현재 root; API updated_at은 본문편집시각 아님; public HTML root edit history 미제공','root_first_compatibility':'partial_quote_support' if grade=='Q' else 'semantically_compatible_unversioned' if c else 'no_external_response','exposure':exp,'exposure_note':'현재본문 Edit가 있고 HTML metadata 정규식에서 Closing now. Feel free to reopen 후대문구 노출' if exp else '후속 본문 미열람. 현재 root가 원판인지 미확인.','first_strategy':strategy,'first_response_id':c['id'] if c else None,'first_response_url':c['html_url'] if c else None,'first_response_at':c['created_at'] if c else None,'first_response_updated_at':c['updated_at'] if c else None,'first_responder':c['user']['login'] if c else None,'first_response_summary':{'7406':'encoding dict replaces prior settings; change tas.encoding directly','7408':'mode=w conditional plus tmp_path alternative; I wonder rhetorical suggestion','7409':'documentation pointer and temporary Dataset implementation suggestion; Have you seen rhetorical','7411':'requests actual opening call; conditional rioxarray action and intake referral','9196':'accepts design proposals; explains origin of constructor argument','9197':'no external substantive response','9201':'new contributor asks original requester/maintainer what pure-xarray reproducer means; role reversal','9203':'Coordinates는 variables와 indexes에 접근하는 얇은 wrapper를 유지해야 한다',
'7710':'to_zarr의 region 인자와 문서 링크를 제공',
'7713':'tuple이 단일 object array로 변환됨을 설명하며 np.array wrapping 가능성 언급',
'7721':'CuPy가 scalar를 반환하지 않는 것이 질문인지 맥락 확인',
'7722':'missing_value가 있으면 _FillValue를 추가하지 않는 대안을 제안하고 표준준수 여부 논의',
'7723':'missing-value 표시 없이는 자동 masking이 값의 표현범위와 integer dtype을 바꾼다는 기존 논의 인용',
'7726':'synchronizer는 zarr에 전달된다며 xarray 특유의 문제라는 재현정보 요청',
'7727':'연산자 추가 PR을 받을 의향 표현',
'7730':'버전 정보 요청',
'7733':'external backend 등록 문서와 tutorial 링크 제공',
'7737':'기존 PR로 해결됐는지 확인 요청; 새 시행/결과 확인형',
'7742':'문자열 encoding 문서로 안내',
'7748':'존재하지 않는 차원에 대한 수학적0/오류 정책의 설계 대안 논의',
'7754':'backend는 발견됐으므로 어떤 입력을 열었는지 local여부·파일명 요청',
'7758':'backend와 원격 서비스/파일시스템 종류 요청',
'7759':'버그 확인 후 bugfix release 예정 보고',
'7763':'실질 타인응답 없음',
'7764':'opt_einsum 도입 지지와 함수인자 대안 제시',
'7766':'실질 타인응답 없음',
'7767':'xr.where 함수의 인자순서를 조정한 예제와 동일출력 제공',
'7768':'apply_ufunc의 args로 DataArray를 전달하여 broadcasting하도록 설계 제안',
'7770':'공개 entrypoints 등록 문서 두개 제공',
'7772':'일반 duck array nbytes 위임 이유와 순수 netCDF 비정상 메모리 사용을 구분하고 stack 진단 권고',
'7773':'xarray를 배제한 netCDF4.Dataset 새 실행을 요청',
'7780':'typing overload와 반대 연산자 fallback의 의미를 설명; 원문제 해결 미검사라고 명시',
'7782':'_FillValue masking에 따른 float 변환을 설명하고 encoding 조회 또는 mask_and_scale=False 안내',
'7789':'실질 타인응답 없음',
'7790':'NaT 숫자 encoding 및 encoding dict/비복호화 조회 예제를 설명'}.get(str(n), '실질 타인응답 없음'),'first_response_current_body_sha256':hashlib.sha256(c['body'].encode()).hexdigest() if c else None,'b_question_eligible':bok if sample=='Bscreen' else None,'b_screen_rank':i if sample=='Bscreen' else None,'late_first_response':bool(c and (datetime.datetime.fromisoformat(c['created_at'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(x['created_at'].replace('Z','+00:00'))).days>90),'prior_self_supplement':n in [9201,9203],'prior_self_supplement_note':'#9201 author offers pure-xarray reproducer help after assignment-only comment; #9203 author asks whether coord dict could be xr.Coordinates; both before first substantive other response' if n in [9201,9203] else None,'sealed_before_outcomes':True,'adjudicator':'xarray stream author; not independent double coding'}
  records.append(r)
  frows.append({'frame_id':cid,'sample':sample,'project':'pydata/xarray','issue_number':n,'root_url':x['html_url'],'created_at':x['created_at'],'title':x['title'],'author':x['user']['login'],'eligibility':'included_A' if sample=='A' else 'eligible_B_root','reason':'specific storage API behavior, not generic test administration' if n==7408 else 'separate design discussion quoted from previous author; retain original goal provenance' if n==9203 else 'specific user/design/API purpose','b_screen_rank':i if sample=='Bscreen' else '', 'first_question_eligible':bok if sample=='Bscreen' else '', 'selection_used_outcomes':False})
# Entire retrieved candidate index: screened exclusions + metadata-only tails.
for frame_name,data in frames.items():
 for rank,x in enumerate(data['data']['items'],1):
  n=x['number']
  if n in sel['A']+sel['B']:continue
  actual_excluded=n in {int(k) for k in sel['B_exclusions']}
  selected_stop=sel['B'][-1] if frame_name=='B' else sel['A'][3] if frame_name=='A1' else sel['A'][-1]
  frows.append({'frame_id':f'{frame_name}-candidate-{rank:03}','sample':'Bscreen' if frame_name=='B' else 'A-frame','project':'pydata/xarray','issue_number':n,'root_url':x['html_url'],'created_at':x['created_at'],'title':x['title'],'author':x['user']['login'],'eligibility':'excluded' if actual_excluded else 'after_stop_not_screened','reason':sel['B_exclusions'].get(str(n),'after prespecified fourth A / 27th B eligible root; only metadata may have been displayed'),'b_screen_rank':'','first_question_eligible':'','selection_used_outcomes':False})
with (P/'initial.jsonl').open('w') as f:
 for r in records:f.write(json.dumps(r,ensure_ascii=False)+'\n')
fields=list(frows[0])
with (P/'frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(frows)
qs=[]
for n,var,quote,present,a,b,kind in qdefs:
 r=next(r for r in records if r['issue_number']==n); c=firsts[n]
 qs.append({'question_id':r['case_id']+'-'+var,'case_id':r['case_id'],'sample':r['sample'],'issue_number':n,'root_url':r['root_url'],'question_url':c['html_url'],'question_comment_id':c['id'],'question_at':c['created_at'],'questioner':c['user']['login'],'variable':var,'quote':quote,'value_in_initial':present,'predicted_value_a_action':a,'predicted_value_b_action':b,'question_kind':kind,'first_strategy':r['first_strategy'],'request_type':r['request_type'],'information_score':r['information_score'],'original_grade':r['original_grade'],'exposure':r['exposure'],'b_question_eligible':r['b_question_eligible'],'sealed_utc':now,'outcomes_read':False})
with (P/'questions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(qs[0]));w.writeheader();w.writerows(qs)
sources=[]
for r in records:
 sources.append({'source_id':'SRC-'+r['case_id'],'type':'public GitHub issue thread','publisher':'pydata/xarray; public participants '+r['author'],'url':r['root_url'],'version':r['created_at']+'; retrieved current body; no original body revision proof','checked_utc':r['checked_utc'],'sections':['root: '+r['initial_location'],'first substantive other response: '+str(r['first_response_url'])],'observed':r['goal']+'; '+r['first_response_summary'],'limitations':r['original_limit']+'; following comments deliberately unread at T0. No adoption/outcome inference.','linked_Q_cases':['Q1','Q2','Q3','Q4',r['case_id']],'duplicate_group':'github:pydata/xarray:'+str(r['issue_number']),'count_minimum':r['sample']=='A','count_group':'A_thread' if r['sample']=='A' else 'B_screen_separate','direct_read':True,'adjudicator':'xarray stream author'})
with (P/'source-ledger.jsonl').open('w') as f:
 for r in sources:f.write(json.dumps(r,ensure_ascii=False)+'\n')
(P/'T0_NOTES.md').write_text('''# xarray T0 판독 — 후속 미열람

A8: 2023Q1 #7406/#7408/#7409/#7411; 2024Q3 #9196/#9197/#9201/#9203. 네 번째 적격까지 선별. 이후 A #7413/#7414/#9204/#9207 본문이 한 배치에 불필요하게 출력되었으나 선정8건이나 그 결과를 대체하지 않았고 각 후보를 after_stop_not_screened로 둔다. 전체 search page100건씩은 내려받았지만 metadata-only tail은 직접원문수에 산입하지 않는다.

B27: 2023-04 전체 순서에서6제외 후 #7790까지. 첫 실질 응답에 직접 환경/입력/목적을 묻는 적격 XB03/#7721, XB06/#7726, XB08/#7730, XB13/#7754, XB14/#7758. B는 root가 M/X/D interleave로 최종8개를 고른다. 최초 실질답이 root+90일 밖인 XB06도 결과나지연으로 제거하지 않는다.

원판: API root updated_at/HTML bodyVersion은 원본 복원이 아니다. root lastEditedAt/edit history 미제공. #7406의 첫 답 code 인용은 제한적 Q 보강이며 본문전체원판확정이 아니다. #7406 root Edit 및 metadata 정규식에서 후대 'Closing now. Feel free to reopen'이 실제로 노출되어 exposure=true, 엄격미노출집합에서 제외. 이후 HTML은 root path만 파싱했다. 다른 사례도 원판미확인을 원판확정으로 바꾸지 않는다.

#7408은 저장API open_zarr/to_zarr의 새/기존 dataset 구분 및 cached-state 사용법 문제이므로 포함. #9203은 shoyer가 이전 대화에서 처음 공개한 설계제안을 TomNicholas가 독립논의로 옮겼다는 provenance를 보존. 유지관리자·반복작성자 sensitivity 필수. #9201의 첫 실질 타인응답은 newcomer가 maintainer/requester에게 pure-xarray reproducer 의미를 되묻는 역방향이다. 일반 지원자→사용자 누락정보 요청으로 평탄화하지 않는다.

비질문 경계: #7409 Have you seen 문장은 링크와 제안을 주는 수사적 포인터. #7408 I wonder 는 tmp_path 권고. #7730은 첫 출력에서 접힌 Environment를 생략해 버전없음으로 초안했으나 봉인 전 재독에서 main@f8127fc/flox0.6.10 등을 확인했다. current-root-present지만 first-response 이전 존재는 미확인으로 교정했다. 새 정보로 세지 않는다. #7737 fixed 여부는 trial/outcome confirmation이므로 B의 기존환경/목표/입력질문 아님. #7773 netcdf4.Dataset 실행요청은 새로운 진단행동 요청. #7722/#7748/#7764 hypothetical design proposals는 B의 직접 정보요청 아님. #7721 최초 ping/ #9201 할당요청은 실질답에서 제외하고 그 다음 직접질문까지 읽음.

retrieved/는 원문 재다운로드 캐시이며 프로그램만 받아둔 미열람 후속 댓글을 포함한다. 원격 봉인에 포함시키지 않는다. 다음 단계 전 root stage2 SHA를 기다린다. 각 변수 예상분기는 questions.csv에 미열람 상태에서 고정했다.
''',encoding='utf8')
print(json.dumps({'A':sum(r['sample']=='A' for r in records),'B_screen':sum(r['sample']=='Bscreen' for r in records),'B_question_eligible':[r['case_id'] for r in records if r['b_question_eligible']],'question_rows':len(qs),'sources_counted':sum(s['count_minimum'] for s in sources),'written_utc':now},ensure_ascii=False))
