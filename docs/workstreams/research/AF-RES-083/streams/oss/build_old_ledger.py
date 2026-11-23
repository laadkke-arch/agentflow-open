from pathlib import Path
import csv,json,datetime,hashlib,subprocess
B=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
REPOS={'statsmodels':('statsmodels/statsmodels','v0.12.1','539478470b53bd3e96473b411e1322bb158fd444'), 'astropy':('astropy/astropy','v4.2','01369fb9d230480220dd81813f3fff906f88d52d'), 'sklearn':('scikit-learn/scikit-learn','0.24.0','45a817933ef51a24f0c5863c1026b4fe664b26fa')}
S=[]
def source(sid,slug,path,lineage,kind,lines,case,summary,limit,claim,count=True):
 repo,tag,sha=REPOS[slug]; p=B/'.workbench'/slug/path; raw=p.read_bytes(); content=raw.decode(errors='replace'); a,z=lines
 # Read exact section now, retain hash and locations rather than copied full publication.
 section='\n'.join(content.splitlines()[a-1:z])
 row={'source_id':sid,'lineage_id':lineage,'source_kind':kind,'repository':repo,'tag':tag,'commit':sha,'url':f'https://github.com/{repo}/blob/{sha}/{path}#L{a}-L{z}','path':path,'lines':[a,z],'directly_opened_utc':NOW,'related_questions':['Q1','Q2','Q3','Q5','Q7'],'case_ids':case,'confirmed':summary,'limits_unknowns':limit,'supports_or_refutes':claim,'content_sha256':hashlib.sha256(raw).hexdigest(),'section_sha256':hashlib.sha256(section.encode()).hexdigest(),'counts_as_independent_work':count,'history_http_arrival':'역사적 도착 미확인'}
 S.append(row); return row
source('O-S01','statsmodels','docs/source/gam.rst','O-W-SM-GAM','consumer_guide',(12,63),['O-AUX-SM-GAM'],'독자에게 자동차 weight/hp의 BSplines(df=[12,10],degree=[3,3]) 생성, Gaussian/Poisson GLMGam fit 및 부분효과 plot을 보여 준다. SciPy 적분 심벌이나 그 함수문서 URL은 원 안내에 없다.','예제의 np는 Sphinx conf의 ipython setup에서 제공됨. 설치된 SciPy 판과 당시 실행 output은 이 파일만으로 미확인.','소비자 사용 지시는 실재하나 이름검색 모집에는 잡히지 않음; 안내→BSplines→simps 내부 연결은 보조층이어야 함.')
source('O-S02','statsmodels','statsmodels/gam/smooth_basis.py','O-W-SM-GAM','consumer_implementation',(225,256),['O-AUX-SM-GAM','O-AUX-SM-SIMPS'],'get_covder2는 scipy.integrate.simps를 가져와 d2의 외적을 x 격자와 axis=0으로 적분한다. 구 이름은 실제 내부 호출이다.','내부코드이지 독자에게 배포된 원 안내가 아님. 079 simps 실행은 없으므로 동등성은 미확인.','GAM 문서 무변경과 backend 수정 필요를 분리해야 함.')
source('O-S03','statsmodels','statsmodels/gam/smooth_basis.py','O-W-SM-GAM','consumer_implementation',(445,466),['O-AUX-SM-GAM'],'UnivariateBSplines의 _smooth_basis_for_single_variable가 get_covder2를 호출한다. BSplines _make_smoothers_list(932-947)가 이 smoother를 생성하는 경로도 읽었다.','정적 호출경로이며 원 예제를 실행하지 않았다.','GAM 안내와 내부 simps의 구체 연결.')
source('O-S04','statsmodels','docs/source/gee.rst','O-W-SM-GEE','consumer_guide',(16,38),['O-AUX-SM-GEE'],'독자는 MASS epil 데이터로 Poisson/exchangeable GEE를 fit하고 summary를 출력한다. qic 호출도 integrate.trapz 호출도 안내에 없다.','다른 모델 선택법·wiki 사용은 이 고정 안내에서 검증되지 않음.','같은 GEE 내부 qic 구현의 적분이 바뀌어도 fit/summary 안내 전체를 고칠 근거는 아님.')
source('O-S05','statsmodels','statsmodels/genmod/generalized_estimating_equations.py','O-W-SM-GEE','consumer_implementation',(1620,1701),['O-AUX-SM-GEE'],'qic 메서드는 quasi-likelihood와 QIC 차이를 설명하고 np.linspace(-0.99999,1,10000)에서 qv를 만들어 scipy.integrate.trapz(qv,dx=xv[1]-xv[0])를 호출한다.','QIC 메서드 내부 데이터는 회귀 모형/원데이터에 달림; 안내 예제의 fit는 qic를 요청하지 않는다.079 y=[1,3,2]와 다른 입력.','상류 함수가 내부에 있다는 사실과 안내의 독자 계약을 구분.')
source('O-S06','statsmodels','requirements.txt','O-M-SM-DEPS','dependency_declaration',(1,4),['O-AUX-SM-GAM','O-AUX-SM-GEE'],'SciPy>=1.2, NumPy>=1.15를 선언한다.','하한은 설치판이 아니며 actual lock/build freeze 미확인.','1.6 이전판도 허용되는 배포물에 새 심벌을 무조건 쓰면 지원판 범위가 바뀜.',False)
source('O-S07','astropy','docs/convolution/kernels.rst','O-W-AST-KERNEL','consumer_guide',(315,350),['O-AUX-AST-KERNEL'],'Gaussian1DKernel(3,mode=integrate)을 최고 정밀도가 필요할 때만 권한다. 구현 대상으로 scipy.integrate.quad/dblquad를 명시하며 느리다고 설명한다.','O02 simps/trapz/cumtrapz 대상이 아니다. 독자환경 실제 SciPy 판 미확인.','같은 scipy.integrate namespace라도 다른 기능은 이 명칭 이관의 수정 대상이 아님.')
source('O-S08','astropy','docs/modeling/fitting.rst','O-W-AST-FITTING','consumer_guide',(32,78),['O-AUX-AST-FITTING'],'시드0,200개 좌표[-5,5]의 잡음자료에 Trapezoid1D와 Gaussian1D를 LevMarLSQFitter로 맞추도록 한다.','Trapezoid1D는 모델 형상이지 SciPy 수치적분 함수가 아님.','후계명 trapezoid의 회고검색은 동음/유사명 거짓 연결을 만든다.')
source('O-S09','astropy','docs/modeling/physical_models.rst','O-W-AST-BLACKBODY','consumer_guide',(11,87),['O-AUX-AST-BLACKBODY'],'BlackBody의 온도·scale·spectral radiance 단위를 설명하고10,000K 곡선을 그린다. bolometric_flux는 sigma*T^4/pi로 설명한다. 4.0 이전 BlackBody1D 등은deprecated 안내로 연결한다.','원 안내가 integrate.trapz를 권하지 않음. 별도 test는 구blackbody_nu100K라 이 원예제와 다름.','같은 BlackBody 분야의 테스트를 원 사용예제 동작 증명으로 전용할 수 없다.')
source('O-S10','astropy','astropy/modeling/tests/test_blackbody.py','O-W-AST-BLACKBODY','consumer_test',(60,78),['O-AUX-AST-TRAPZ'],'blackbody_nu(wave,temp)에서wave=np.logspace(0,8,100000) Angstrom,temp100K로계산한flux를 integrate.trapz(flux.value,x=lum.value)로적분하고 sigma*T^4/pi와rtol0.01 비교한다.','고정 테스트를 읽었지만 실행 안 함. 구 함수deprecated 경고 무시, SciPy optional skip.079의3점 입력과 다르다.','기대값/입력은 존재하지만 원 배포 안내6자리에 포함할 수 없는 테스트층이다.')
source('O-S11','astropy','setup.cfg','O-M-AST-DEPS','dependency_declaration',(54,87),['O-AUX-AST-KERNEL','O-AUX-AST-TRAPZ'],'all/docs extras에 scipy>=1.1 선언.','실제 설치판 아님.','trapezoid를 무조건 대입하면1.1지원범위와 충돌할 수 있음.',False)
source('O-S12','astropy','tox.ini','O-M-AST-BUILD','build_configuration',(59,79),['O-AUX-AST-TRAPZ'],'oldestdeps가 scipy==1.1.* 및 NumPy1.17.*를 명시한다.','설정은 실제CI 성공로그나 설치freeze가 아니며patch판도 고정하지 않음.','실제 설치판과 테스트 matrix 선언을 분리.',False)
source('O-S13','astropy','.circleci/config.yml','O-M-AST-BUILD','build_configuration',(36,49),['O-AUX-AST-TRAPZ'],'image-tests job은 pip install scipy -U 뒤 visualization tests를 실행하게 설정되어 있다.','이job은BlackBody test 실행의 증거가 아니고 scipy버전도 미고정.','업그레이드 명령만으로 해당 소비자 예제의 실제SciPy판을 확정하지 않음.',False)
source('O-S14','sklearn','doc/modules/model_evaluation.rst','O-W-SKL-PR','consumer_guide',(760,820),['O-AUX-SKL-AUC'],'average_precision_score는 비보간 AP이며 auc의 사다리꼴 선형보간은 낙관적 평가를 줄 수 있다고 설명한다. precision-recall 예제로 연결한다.','scipy.integrate.trapz를 권하지 않음. 같은 기능/목적의 예제와 한계보로 접음.','수치 적분값과 AP의 의미를 이름교체로 합쳐서는 안 됨.')
source('O-S15','sklearn','examples/model_selection/plot_precision_recall.py','O-W-SKL-PR','consumer_example',(64,142),['O-AUX-SKL-AUC'],'AP와 sklearn.metrics.auc는다른결과이며 두 iris class와 noise feature,LinearSVC score로average_precision을 계산하고 곡선을그린다.','위 사용자 가이드와같은PR평가 목적이므로독립발견중복산입안함.','같은 단어라도 이 예제의함수는 SciPy integrate alias가 아님.')
source('O-S16','sklearn','sklearn/metrics/_ranking.py','O-W-SKL-PR','consumer_implementation',(43,111),['O-AUX-SKL-AUC'],'metrics.auc는 최소2점·단조x를 요구하고 direction*np.trapz(y,x)를사용하며 예시 ROC AUC는0.75다.','numpy.trapz namespace는 scipy.integrate.trapz와 다름; 실제 NumPy 설치판 미확인.','O02의동일대상조인거부를 직접 지지.')
source('O-S17','sklearn','sklearn/_min_dependencies.py','O-M-SKL-DEPS','dependency_declaration',(1,27),['O-AUX-SKL-AUC'],'CPython SciPy>=0.19.1,NumPy>=1.13.3; PyPy에서는SciPy>=1.1.0,NumPy>=1.14.0.','floor일뿐실제build/설치판미확인.','동일SciPy대상임을지원하지않으며판범위만확인.',False)
(B/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in S))
records=[]
for n in range(1,4):
 records.append({'record_id':f'O02-{n}','slot':n,'event':'O02','stratum':'core','status':'VACANT','consumer':None,'original_instruction':None,'reason':'고정된 세 저장소·검색식·옛 정식 태그에서 적격 O02 사용자 안내 검출 0. 안내 전체의 부재 증명은 아님. 역방향 코드 연결·시험·다른 namespace·동음은 보조층으로 분리.','source_ids':[],'installed_scipy_version':'미확인','proposal_score_eligible':False})
aux=[
('O-AUX-SM-GAM','statsmodels','docs/source/gam.rst',[12,63],'BSplines의자동차data설정으로Gaussian/Poisson GAM fit·부분효과plot','df_autos[weight,hp];df=[12,10];degree=[3,3];alpha=[21833888.8,6460.38479]','결과모형요약과부분효과; 정확한simps API/적분값은원안내약속아님','scipy.integrate.simps 내부연결','O-S01 O-S02 O-S03 O-S06','지정이름검색은0이며역방향코드연결로찾은보조안내; 본표교체금지'),
('O-AUX-SM-GEE','statsmodels','docs/source/gee.rst',[16,38],'epil 데이터 Poisson/exchangeable GEE fit 후summary','epil/MASS;y~age+trt+base;subject grouping','회귀모형fit/summary; qic적분값을요청하지않음','GEE.qic 안의scipy.integrate.trapz는별도행동','O-S04 O-S05 O-S06','원예제에서qic호출없으므로backend발견을원안내수정으로전용금지'),
('O-AUX-AST-KERNEL','astropy','docs/convolution/kernels.rst',[315,350],'최고정밀도필요시Gaussian1DKernel(3,mode=integrate)','Gaussian1DKernel sigma3,mode=integrate','픽셀전체의함수적분; 느림/최고정밀도조건','scipy.integrate.quad/dblquad','O-S07 O-S11','same namespace but different symbol;O02대상아님'),
('O-AUX-AST-FITTING','astropy','docs/modeling/fitting.rst',[32,78],'Trapezoid1D를잡음자료에LevMarLSQFitter로적합','seed0;x=linspace(-5,5,200);gaussian+noise','fitted model; 수치적분값아님','astropy.modeling.functional_models.Trapezoid1D','O-S08','표시명일치뿐다른객체'),
('O-AUX-AST-BLACKBODY','astropy','docs/modeling/physical_models.rst',[11,87],'BlackBody 곡선평가및bolometric_flux사용','10000K;wavelengthlogspace1000..30000A;1000points;scale10000','spectral radiance단위및sigma*T^4/pi','Astropy BlackBody analytic bolometric_flux','O-S09 O-S10 O-S11','연관test는구blackbody_nu100K100000points;예제와동일하지않음'),
('O-AUX-AST-TRAPZ','astropy','astropy/modeling/tests/test_blackbody.py',[60,78],'BlackBody Planck수치적분테스트(사용안내아님)','wave=logspace(0,8,100000)Angstrom;100K;trapz(flux.value,x=lum.value)','sigma_sb*T^4/pi와rtol0.01','scipy.integrate.trapz','O-S10 O-S11 O-S12','테스트만발견;원안내슬롯에포함금지'),
('O-AUX-SKL-AUC','sklearn','doc/modules/model_evaluation.rst',[760,820],'AP와trapezoidal AUC의평가의미구분','PR점들;예제는iris두class,noise,LinearSVC','AP 비보간; AUC는선형보간이라결과다름','sklearn.metrics.auc→numpy.trapz','O-S14 O-S15 O-S16 O-S17','같은trapz철자다른namespace;가이드와연결예제중복접음')]
for rid,slug,path,lines,instruction,inputs,outputs,target,sids,reason in aux:
 repo,tag,sha=REPOS[slug]
 records.append({'record_id':rid,'slot':None,'event':'O02','stratum':'auxiliary','status':'EXCLUDED_FROM_CORE','consumer':repo,'old_tag':tag,'old_commit':sha,'original_source_url':f'https://github.com/{repo}/blob/{sha}/{path}#L{lines[0]}-L{lines[1]}','path':path,'lines':lines,'original_instruction':instruction,'input':inputs,'required_output_or_setting':outputs,'upstream_target':target,'installed_scipy_version':'미확인','dependency_range':{'statsmodels':'scipy>=1.2','astropy':'optional/all/docs scipy>=1.1','sklearn':'CPython scipy>=0.19.1; PyPy>=1.1.0'}[slug],'source_ids':sids.split(),'exclusion_reason':reason,'history_http_arrival':'역사적 도착 미확인','proposal_score_eligible':False,'079_exact_join':'불일치: 원입력/함수/소비환경이079실행과같지않음;simps/cumtrapz개별실행없음'})
(B/'records.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
props=[]
for r in records:
 rid=r['record_id']
 if r['stratum']=='core':
  props.append({'record_id':rid,'stratum':'core','A_action':'hold','A_proposed_change':'원레코드가없어수선안적용불가','B_action':'hold','B_proposed_change':'공석보존','applicable_versions':'해당없음','evidence_ids':'old-search.json','score_eligible':'false','sealed_before_followup':NOW})
 else:
  A='공식수신자매핑이이원안내대상에없으므로보류;원안내문구변경없음'; BA='keep'; Btext='원안내호출과판을보존; O02대상이아니므로이사건에따른변경없음'
  if rid=='O-AUX-AST-TRAPZ':
   A='internal test의integrate.trapz를integrate.trapezoid로일괄치환(부록제안;지원판조건추가없음)'; BA='scoped_alias'; Btext='원test의trapz및old SciPy>=1.1범위를보존;SciPy>=1.6후계별칭은별도연결하되minimum판에서실패하는무조건치환금지;100K100000point기대값수용은미실행'
  elif rid=='O-AUX-SM-GAM':
   BA='scope'; Btext='원BSplines예제는보존하고statsmodels0.12.1안내로명시;내부simps연결과소비자설치판미확인을기록.후속SciPy제거구간은backend검증후별도지원범위수선;원문을simpson호출로바꾸지않음'
  elif rid=='O-AUX-SM-GEE':
   Btext='fit/summary안내를보존;별도qic메서드내부trapz이관을이예제에전파하지않음'
  props.append({'record_id':rid,'stratum':'auxiliary','A_action':'rename' if rid=='O-AUX-AST-TRAPZ' else 'hold','A_proposed_change':A,'B_action':BA,'B_proposed_change':Btext,'applicable_versions':r['old_tag']+';upstream1.6rename;later1.14removal별도','evidence_ids':' '.join(r['source_ids']),'score_eligible':'false','sealed_before_followup':NOW})
with (B/'proposals.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(props[0]));w.writeheader();w.writerows(props)
fr=[]
for i,slug in enumerate(REPOS,1):
 repo,tag,sha=REPOS[slug]; scan=next(r for r in json.loads((B/'old-search.json').read_text()) if r['repository']==slug)
 fr.append({'frame_id':f'O-F{i}','repository_order':i,'repository':repo,'old_tag':tag,'old_commit':sha,'searched_files':scan['searched_files'],'matched_lines':len(scan['matches']),'included':0,'excluded':'코드/시험/다른namespace/동음; 세부 records.jsonl','vacancy_slots':'O02-1;O02-2;O02-3 are event-level remaining slots, not one vacancy per repository'})
with (B/'frame.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(fr[0]));w.writeheader();w.writerows(fr)
(B/'preseal-summary.json').write_text(json.dumps({'opened_utc':NOW,'core_slots':3,'core_selected':0,'core_vacant':3,'auxiliary_records':7,'direct_source_rows':len(S),'independent_downstream_lineages':sorted(set(s['lineage_id'] for s in S if s['counts_as_independent_work'])),'followup_bodies_opened':False,'metadata_only_followup_tags':True,'parent_signal_required_before_followup':True},indent=2,ensure_ascii=False)+'\n')
print('old ledger written',len(S),len(records),len(props))
