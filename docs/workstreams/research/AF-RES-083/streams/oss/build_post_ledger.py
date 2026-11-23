from pathlib import Path
import json,csv,hashlib,datetime
B=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
VERS=json.loads((B/'versions.json').read_text())['rows']
ACQ=[json.loads(l) for l in (B/'postseal-acquisition.jsonl').read_text().splitlines()]
S=[]
def src(sid,repo,role,path,lines,lineage,cases,summary,limit,claim,kind='consumer_guide'):
 v=next(x for x in VERS if x['repository']==repo and x['role']==role);r=next(x for x in ACQ if x['repository']==repo and x['role']==role and x['path']==path and x.get('status')==200)
 raw=(B/r['cache_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256'];text=raw.decode();a,z=lines;section='\n'.join(text.splitlines()[a-1:z]);assert section
 S.append({'source_id':sid,'lineage_id':lineage,'source_kind':kind,'repository':repo,'tag':v['tag'],'commit':v['commit'],'url':f'https://github.com/{repo}/blob/{v["commit"]}/{path}#L{a}-L{z}','path':path,'lines':[a,z],'directly_opened_utc':NOW,'acquired_utc':r['acquired_utc'],'sealed_before_acquisition_commit':'35d7e18024cced8cc81f9397b65e90e0e74bb907','related_questions':['Q3','Q4','Q5','Q7'],'case_ids':cases,'confirmed':summary,'limits_unknowns':limit,'supports_or_refutes':claim,'content_sha256':r['sha256'],'section_sha256':hashlib.sha256(section.encode()).hexdigest(),'counts_as_independent_work':True})
sm='statsmodels/statsmodels';ast='astropy/astropy';sk='scikit-learn/scikit-learn'
src('O-P01',sm,'first','docs/source/gam.rst',(12,63),'O-W-SM-GAM',['O-AUX-SM-GAM'],'v0.12.2의 GAM 가이드는 옛 v0.12.1 파일 전체와 bytes가 같다. BSplines와 Gaussian/Poisson fit 지시를 그대로 발행했다.','당시 실제 docs build 환경·소비자 실행은 미확인.','SciPy1.6 명칭 이관 뒤 모든 안내가 즉시 바뀐 것은 아님.')
src('O-P02',sm,'latest','docs/source/gam.rst',(12,65),'O-W-SM-GAM',['O-AUX-SM-GAM'],'v0.15.0에서도 BSplines와 두 GAM fit 핵심 예제는 동일하다. 뒤의 kfold 최적화에 rng seed와 인자를 추가했다.','이 RNG 수정의 이유는 별도 commit에서 확인; SciPy 적분 명칭 수선으로 세지 않는다.','핵심 안내 유지와 부가 예제 변경을 분리.')
src('O-P03',sm,'first','docs/source/gee.rst',(16,38),'O-W-SM-GEE',['O-AUX-SM-GEE'],'v0.12.2 GEE 가이드 파일 전체가 옛 판과 동일하다.','QIC 내부 trapz를 이 fit/summary 안내에 적용한 검증은 아님.','행동별 변경 전파 범위가 필요.')
src('O-P04',sm,'latest','docs/source/gee.rst',(16,38),'O-W-SM-GEE',['O-AUX-SM-GEE'],'v0.15.0의 epil Poisson/exchangeable fit/summary 예제 문단도 동일하다. 다른 API 목록은 늘고 링크가 정리되었다.','원문 유지가 모든 실행환경의 성공을 보증하지 않음.','내부 QIC의 적분 이름 변경을 안내 전체의 정정 필요로 옮길 수 없음.')
src('O-P05',sm,'first','statsmodels/gam/smooth_basis.py',(240,258),'O-W-SM-GAM',['O-AUX-SM-GAM'],'v0.12.2의 get_covder2는 simps import와 위치 인자 x 호출을 유지한다.','정적 판독이며 simps 입력 실행은 없음.','1.6 이관 직후에 구 심벌을 유지한 실제 배포 source.','consumer_implementation')
src('O-P06',sm,'latest','statsmodels/gam/smooth_basis.py',(390,433),'O-W-SM-GAM',['O-AUX-SM-GAM'],'v0.15.0은 scipy.integrate.simpson 및 x=x로 호출하지만 docstring 설명에는 여전히 scipy.integrate simps가 남는다.','docstring은 사람이 쓴 설명이지만 등록된 핵심 안내 모집에서는 내부코드 보조층. 결과값 호환 미실행.','backend 수선 후 설명의 옛 심벌이 잔존하는 불일치.','consumer_implementation')
src('O-P07',sm,'first','statsmodels/genmod/generalized_estimating_equations.py',(1680,1701),'O-W-SM-GEE',['O-AUX-SM-GEE'],'v0.12.2 QIC는 trapz(qv,dx=...)를 유지한다.','GEE guide의 fit는 qic를 부르지 않음.','내부 호출과 원 사용 지시를 분리.','consumer_implementation')
src('O-P08',sm,'latest','statsmodels/genmod/generalized_estimating_equations.py',(1861,1885),'O-W-SM-GEE',['O-AUX-SM-GEE'],'v0.15.0 QIC는 scipy.integrate.trapezoid를 직접 import하여 계산한다.','입력 qv는 회귀/모형 설정에 의존하며 079의 3점과 다름.','실제 source가 바뀌었어도 같은 fit 안내가 바뀔 필요를 자동 증명하지 않음.','consumer_implementation')
src('O-P09',ast,'first','docs/convolution/kernels.rst',(281,316),'O-W-AST-KERNEL',['O-AUX-AST-KERNEL'],'v4.0.5의 Discretization 문단은 v4.2의 quad/dblquad 및 최고정밀도 조건을 그대로 유지한다.','4.0.5는 더 늦게 나온 maintenance line이지4.2에서 연속진화한 판이라고 단정할 수 없음.','태그 시간순과 코드 계보를 분리해야 함.')
src('O-P10',ast,'latest','docs/convolution/kernels.rst',(325,360),'O-W-AST-KERNEL',['O-AUX-AST-KERNEL'],'v8.0.3에서도 같은 Discretization 안내 문단과 호출이 유지된다.','O02 이관 대상은 아니며 전체 파일의 다른 예제는 변경되었다.','같은 scipy.integrate namespace의 다른 함수에 이관을 전파하면 안 됨.')
src('O-P11',ast,'first','docs/modeling/fitting.rst',(32,78),'O-W-AST-FITTING',['O-AUX-AST-FITTING'],'v4.0.5의 모델 fitting 문서 파일은 old4.2와 bytes 동일하다.','SciPy 적분의 후속 이름과 무관한 Trapezoid 모델.','후계 표시명 검색의 동음 제외를 지지.')
src('O-P12',ast,'latest','docs/modeling/fitting.rst',(100,146),'O-W-AST-FITTING',['O-AUX-AST-FITTING'],'v8.0.3 예제는 TRFLSQFitter, default_rng와 maxiter=200을 사용한다. Trapezoid1D 모형은 여전히 같은 이름이다.','이 문서의 수정은 실제 확인했지만 O02 이관이 이유라는 설명은 없고 대상 함수도 다르다.','어떤 후속 수정이든 상류 이름 이관의 정정으로 세는 오류를 반박.')
src('O-P13',ast,'first','docs/modeling/physical_models.rst',(11,87),'O-W-AST-BLACKBODY',['O-AUX-AST-BLACKBODY'],'v4.0.5 BlackBody 문단과 예제는old4.2와동일하다. bolometric_flux 분석식 및deprecated기능안내연결도 남아 있다.','시계열첫후속이같은minorline아님.','다른 유지보수판의 원래 안내 보존을 확인.')
src('O-P14',ast,'latest','docs/modeling/physical_models.rst',(11,79),'O-W-AST-BLACKBODY',['O-AUX-AST-BLACKBODY'],'v8.0.3의10,000K BlackBody 평가와sigma*T^4/pi 설명은유지되며plot구문이정리되고deprecated단락은없다.','이문단을삭제된100K oldblackbody_nu 시험의대체실행근거로쓰지않음.','겉으로같은BlackBody분야여도입력/모델이달라증거전용불가.')
src('O-P15',ast,'first','astropy/modeling/tests/test_blackbody.py',(59,77),'O-W-AST-BLACKBODY',['O-AUX-AST-TRAPZ'],'v4.0.5 test_blackbody_scipy는100K/100000point integrate.trapz와1%허용오차를유지한다.','실행안함.현재v8.0.3에서는이경로404이며삭제diff를별도확인.','구이름유지는실제배포판에존재했으나그사실은정확출력수용이아님.','consumer_test')
src('O-P16',sk,'first','doc/modules/model_evaluation.rst',(760,820),'O-W-SKL-PR',['O-AUX-SKL-AUC'],'0.24.1 모델평가가이드파일전체는old0.24.0과bytes동일하다.','numpy.trapz 기반이지SciPyintegrate구심벌직접안내아님.','등록모집의대상제외유지.')
src('O-P17',sk,'latest','doc/modules/model_evaluation.rst',(957,977),'O-W-SKL-PR',['O-AUX-SKL-AUC'],'1.9.1도 AP 비보간·AUC 선형보간의 차이를 유지하고 Chen2024 interpolation 비교를 덧붙였다.','수학적정의가남은사실은모든환경의수치동등실행증거가아님.','backend이관과독자가택하는평가지표의의미를분리.')
src('O-P18',sk,'latest','examples/model_selection/plot_precision_recall.py',(65,78),'O-W-SKL-PR',['O-AUX-SKL-AUC'],'AP와trapezoidal AUC가다른결과를낸다는243문자문단은old/first/latest에서동일하다.','같은목적의가이드/예제는한계보로접었음.','두의미를한함수/한표시명으로합치면안됨.')
src('O-P19',sk,'first','sklearn/metrics/_ranking.py',(88,110),'O-W-SKL-PR',['O-AUX-SKL-AUC'],'0.24.1의auc는direction*np.trapz(y,x)를사용한다.','SciPy제거영향을직접주장할수없음.','같은trapz철자도namespace확인필수.','consumer_implementation')
src('O-P20',sk,'latest','sklearn/metrics/_ranking.py',(14,114),'O-W-SKL-PR',['O-AUX-SKL-AUC'],'1.9.1의auc는scipy.integrate.trapezoid를직접import하여사용한다.','이것은후속backend선택변경이며옛지시가처음부터SciPytarget이었다는증거가아님.','새판의목적지를옛작성시대상으로소급하면잘못된연결.','consumer_implementation')
src('O-P21',sm,'first','statsmodels/gam/tests/test_penalized.py',(429,510),'O-W-SM-GAM',['O-AUX-SM-GAM'],'TestGAMMPGBS는df_autos와기저차원12/10을쓰지만constraints=center,include_intercept=True와별도alpha를쓴다. Rmgcv기대penalty matrix등을비교한다.','원GAM가이드예제는같은constraints/alpha가아니므로이시험을그예제의정확한통과로전용할수없음.실행안함.','후속소비자시험도정확입력조인이필요.','consumer_test')
src('O-P22',sm,'latest','statsmodels/gam/tests/test_penalized.py',(561,650),'O-W-SM-GAM',['O-AUX-SM-GAM'],'latestTestGAMMPGBS에도center/intercept/별도alpha,동일R결과비교가남는다. FormulaManager와thread-safety/localmodel수정이있다.','동일test이름이지원가이드예제와동일입력아님;native미실행.','최신판test존재만으로구안내동작을승인하지않음.','consumer_test')
# Publisher events: same migration chain stays one lineage, not one source per commit.
for i,e in enumerate(json.loads((B/'publisher-events.json').read_text()),1):
 S.append({'source_id':f'O-E{i:02d}','lineage_id':e['lineage_id'],'source_kind':'publisher_change_record','url':e['url'],'commit':e['commit'],'section':'commit message and named changed-file hunks; publisher-events.json#'+e['publisher_diff_id'],'directly_opened_utc':e['directly_opened_utc'],'related_questions':['Q4','Q5','Q7'],'case_ids':[e['publisher_diff_id']],'confirmed':e['confirmed'],'limits_unknowns':e['limits_unknowns'],'supports_or_refutes':'사후 수정 관측·당사자 이유; 수정 필요성·실행수용과 분리','counts_as_independent_work':True})
for e in json.loads((B/'publisher-prs.json').read_text()):
 linked=next(x for x in json.loads((B/'publisher-events.json').read_text()) if x['publisher_diff_id']==e['publisher_diff_id'])
 S.append({'source_id':'O-PR-'+str(e['number']),'lineage_id':linked['lineage_id'],'source_kind':'publisher_pull_request','url':e['url'],'section':'description; merged_at; milestone','directly_opened_utc':e['directly_opened_utc'],'related_questions':['Q4','Q7'],'case_ids':[e['publisher_diff_id']],'confirmed':e['body_read']+'; merged_at='+str(e['merged_at'])+'; milestone='+str(e['milestone']),'limits_unknowns':e['limit'],'supports_or_refutes':linked['confirmed'],'counts_as_independent_work':True})
# Fixed-tag release notes are same event lineage, not extra independent events.
for sid,file,repo,tag,path,lines,lineage,summary in [('O-P23','SM-0141-RELEASE.txt',sm,'v0.14.1','docs/source/release/version0.14.1.rst',(89,98),'O-W-SM-MIGRATION','0.14.1의maintenance항목이PR8940을포함한다. 1.6이관직후first0.12.2와실제수선포함출시판을구별.'),('O-P24','AST-43-CHANGES.txt',ast,'v4.3','CHANGES.rst',(309,316),'O-W-AST-BLACKBODY-REMOVAL','4.3릴리스변경기록은deprecated modeling.blackbody제거와PR10972를명시한다.1.6명칭이관으로정정한기록이아님.')]:
 raw=(B/'.workbench/postseal'/file).read_bytes();a,z=lines;section='\n'.join(raw.decode().splitlines()[a-1:z]);assert section
 S.append({'source_id':sid,'lineage_id':lineage,'source_kind':'publisher_release_record','url':f'https://github.com/{repo}/blob/{tag}/{path}#L{a}-L{z}','tag':tag,'path':path,'lines':lines,'directly_opened_utc':NOW,'related_questions':['Q4','Q7'],'case_ids':[lineage],'confirmed':summary,'limits_unknowns':'고정 release tag 원문을 읽음. 날짜나 테스트통과를 이 한 문장으로 확정하지 않음.','supports_or_refutes':'발행판과코드수정시점연결','content_sha256':hashlib.sha256(raw).hexdigest(),'counts_as_independent_work':True})
(B/'postseal-sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in S))
R=[]
for n in range(1,4):
 R.append({'record_id':f'O02-{n}','stratum':'core','first_followup':None,'latest_followup':None,'observed_revision':'VACANT_NOT_APPLICABLE','publisher_diff_ids':'','A_evaluation':'적용불가','B_evaluation':'공석유지','independent_criterion':'원안내없음','denominator_eligible':'false','source_ids':'old-search.json','unknowns':'등록된검색에서검출0;이범위밖안내부재를증명하지않음'})
entries=[
('O-AUX-SM-GAM','v0.12.2@cce93db5277ce2618dafdc84c42186bbafe2a6b6','v0.15.0@278ff9950636cdd4939b4055e339a8e681d79cab','first파일동일;latest핵심BSplines/fit문단유지,부가kfold RNG추가;backend별칭및xkwarg수정','PUBLISHER-SM-MIGRATION;PUBLISHER-SM-KWARG;PUBLISHER-SM-FLOOR;PUBLISHER-SM-GUIDE-RNG','보류:원안내에대체할심벌없음','버전범위·내부호출을분리한보존은source와맞으나동작수용보류','명시된source import/argument와원안내행은확인;정확예제native없음','O-P01 O-P02 O-P05 O-P06 O-P21 O-P22 O-E01 O-E02 O-E03 O-E04 O-P23','최신docstring의simps잔존;testcenter/alpha차이;정확설치판미확인'),
('O-AUX-SM-GEE','v0.12.2','v0.15.0','first파일동일;latestfit/summary문단동일;별도QICbackendtrapz→trapezoid','PUBLISHER-SM-MIGRATION','보류:원안내에구적분명없음','fit/summary와QIC분리유지가원문에부합','원안내가qic를요청하지않음','O-P03 O-P04 O-P07 O-P08 O-E01','원안내실행미확인;QIC결과를이예제성공으로전용불가'),
('O-AUX-AST-KERNEL','v4.0.5@f6339626a47981137a469481997752a239188bc7','v8.0.3@b31ef844b284a16ce40ad44468de233ccf8be052','discretization문단유지','', '보류:quad/dblquad에O02수신매핑없음','O02이관으로변경하지않는유지지지','정확namespace/symbol이O02와다름','O-P09 O-P10','서로다른maintenance계보의first태그;runtime정밀도미검증'),
('O-AUX-AST-FITTING','v4.0.5','v8.0.3','first파일동일;latestTRFLSQFitter/default_rng/maxiter수정','', '보류:Trapezoid1D는수치적분심벌아님','O02를이유로한변경은적용외','모형과적분함수의타입/namespace가다름','O-P11 O-P12','실제문서수정은관측했으나그원인을O02라고하는근거없음'),
('O-AUX-AST-BLACKBODY','v4.0.5','v8.0.3','BlackBody주예제유지;plot정리·deprecated단락삭제','PUBLISHER-AST-REMOVE','보류:원안내대상에O02단일수신매핑없음','안내와구test입력을분리하는보존지지','oldguide10000K1000point와test100K100000point차이','O-P13 O-P14 O-E05 O-PR-10972 O-P24','원안내actualbuild미확인'),
('O-AUX-AST-TRAPZ','v4.0.5','v8.0.3','first구trapz시험유지;latest파일삭제,4.3deprecated모듈제거사건','PUBLISHER-AST-REMOVE','정적지원판충돌:trapezoid도입1.6전지원판을무조건치환;core오류율에합산안함','옛지원판/별칭범위보존은선언과맞음;실제수치동등미실행','Astropy>=1.1선언+SciPy1.6도입원문/079관계;원격실행없음','O-S10 O-S11 O-S12 O-P15 O-E05 O-PR-10972 O-P24','삭제사유는4.0deprecated이며merge2020-11-02로SciPy1.6발행전.현재test로대체하지않음'),
('O-AUX-SKL-AUC','0.24.1@c6512929fbee7232949c0f18cfb28cf3b5959df9','1.9.1@866c0f51e7560ef0303cbcc5f159df5382ea9e3f','first가이드/예제파일동일;AP대AUC문단유지;backend는np.trapz→SciPyfallback→직접trapezoid','PUBLISHER-SK-MIGRATE;PUBLISHER-SK-FLOOR','보류:oldtarget은numpy.trapz이며O02그대로대상아님','옛namespace보존/새이관관계별도기록지지','구소비자가실제호출한namespace와새소비판을직접확인','O-P16 O-P17 O-P18 O-P19 O-P20 O-E06 O-E07 O-PR-27140','PR본문interpolate오타대실제diffintegrate;내부실행수용미확인')]
for x in entries:
 rid,first,last,obs,diffs,A,Bv,criterion,sids,unknown=x
 R.append({'record_id':rid,'stratum':'auxiliary','first_followup':first,'latest_followup':last,'observed_revision':obs,'publisher_diff_ids':diffs,'A_evaluation':A,'B_evaluation':Bv,'independent_criterion':criterion,'denominator_eligible':'false','source_ids':sids,'unknowns':unknown})
with (B/'revisions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(R[0]));w.writeheader();w.writerows(R)
# Re-readable paragraph comparison; hashes prove same selected text, not same software outputs.
checks=[]
for slug,path,a,z,drop in [('statsmodels','docs/source/gam.rst','The following illustrates','# Optimal',''),('statsmodels','docs/source/gee.rst','The following illustrates','Several notebook',''),('astropy','docs/convolution/kernels.rst','Discretization','Normalization','.. _kernel_normalization:\n'),('astropy','docs/modeling/physical_models.rst','.. _blackbody-planck-law:','Drude1D',''),('sklearn','examples/model_selection/plot_precision_recall.py','AP and the trapezoidal','Precision-recall curves','')]:
 hashes={}
 for role in ['old','first','latest']:
  prefix='scikit-learn' if slug=='sklearn' else slug
  p=B/'.workbench'/slug/path if role=='old' else B/'.workbench/postseal'/prefix/role/path
  txt=p.read_text();seg=txt[txt.index(a):txt.index(z,txt.index(a))];seg=seg.replace(drop,'') if drop else seg;seg=seg.strip();hashes[role]=hashlib.sha256(seg.encode()).hexdigest()
 checks.append({'repository':slug,'path':path,'start_marker':a,'end_marker':z,'normalization':'strip outer whitespace'+(';remove exactly '+repr(drop) if drop else ''),'hashes':hashes,'old_equals_first':hashes['old']==hashes['first'],'old_equals_latest':hashes['old']==hashes['latest']})
(B/'paragraph-comparison.json').write_text(json.dumps({'checked_utc':NOW,'checks':checks,'limit':'원문지정문단의bytes/선언비교;제품행동/실행검사아님'},indent=2,ensure_ascii=False)+'\n')
print('postsource',len(S),'revision',len(R),'core denominator',sum(x['denominator_eligible']=='true' for x in R))
