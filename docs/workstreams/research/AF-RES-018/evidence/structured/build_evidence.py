from pathlib import Path
from urllib.parse import urlparse
import json

ROOT = Path(__file__).resolve().parent
WINDOW = '2026-11-21T03:49:13Z/2026-11-21T03:54:47Z'
sources = []
def add(id, url, title, version, kind, sections, confirmed, limits, used, field, refs, **extra):
    sources.append(dict(id=id, url=url, accessed_at_utc=WINDOW,
      access_time_precision='UTC reading-session interval; per-request wall-clock timestamps were not exposed or separately captured',
      source_type=kind, title=title, version_or_date=version,
      sections_read=sections, confirmed=confirmed, limits=limits, level='D1',
      used_in=used, body_read=True, counted=True, field=field,
      retrieval='anonymous search-service open; original paper or public author/institution copy',
      tool_refs=refs, **extra))
add('STR01', 'https://worthylab.org/wp-content/uploads/2020/12/grove-et-al_2000.pdf',
    'Clinical Versus Mechanical Prediction: A Meta-Analysis',
    'Grove et al., 2000, Psychological Assessment 12(1):19–30; DOI 10.1037/1040-3590.12.1.19',
    'original_meta_analysis',
    ['pp.19–21: definitions and inclusion criteria', 'results: 136-study comparison, tool lines 303–328', 'discussion: clinical exceptions and information availability, lines 1192–1235'],
    '136개 연구 중 원 논문의 구분 기준으로 기계적 결합이 우세한 연구는 63개, 대체로 비슷한 연구는 65개, 임상적 판단이 우세한 연구는 8개였다. 기계적 결합은 정해진 규칙으로 정보를 합치는 개입이며, 매번 확률적으로 판단하는 절차형 LLM과 같지 않다.',
    '연구·과제·효과 크기가 이질적이며 이 비율을 소프트웨어 추천 개선율로 옮길 수 없다. 동일 검색 예산의 LLM 실험이 아니며 P의 표현 형식만으로 기계적 예측의 효과를 상속하지 않는다.',
    ['Q1','Q8'], 'clinical_vs_mechanical',
    ['turn716200951view0','turn689452656view0','turn689452656view1','turn365848255view6'],
    independent_experiment=False)
add('STR02', 'https://www.ncbi.nlm.nih.gov/sites/books/NBK143241/bin/appa-m1.pdf',
    'A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population',
    'Haynes et al., 2009, NEJM 360:491–499; DOI 10.1056/NEJMsa0810119; WHO-hosted authorized reprint',
    'original_before_after_multicenter_study',
    ['pp.491–494: population, intervention and outcomes', 'pp.497–498: implementation and limitations'],
    '8개 병원에서 도입 전 3,733명과 후 3,955명의 성인 비심장 수술을 관찰했고 입원 중 최대 30일 사망률은 1.5%에서 0.8%, 합병증은 11%에서 7%로 감소했다. 개입에는 체크리스트 외에 현장 지도·교육·피드백과 지역별 조정이 함께 들어갔다.',
    '비무작위 전후 비교라 시간 변화와 동반 개입을 분리하기 어렵다. 효과를 체크리스트 문구 자체의 인과 효과로 읽거나 환자 결과를 추천 정확성에 직접 대입할 수 없다.',
    ['Q1','Q4','Q8'], 'surgical_checklists',
    ['turn244406719view0','turn890239141view4','turn725394632view2'],
    independent_experiment=True)
add('STR03', 'https://strathprints.strath.ac.uk/69049/1/Dhami_etal_ACP_2019_The_analysis_of_competing_hypotheses_in_intelligence.pdf',
    'The “analysis of competing hypotheses” in intelligence analysis',
    'Dhami, Belton & Mandel, 2019, Applied Cognitive Psychology; DOI 10.1002/acp.3550; accepted 2019-03-18',
    'original_randomized_process_analysis',
    ['§4 Methods, pp.2–3, lines 155–234', '§5 Results, lines 235–430', 'Discussion'],
    '정보분석가 50명을 ACH/대조 각 25명에 배정했다. 12개 증거를 모두 고려한 분석가는 ACH 23/25명, 대조 17/25명이었지만 ACH 단계 준수와 내부 일관성이 완전하지 않았다.',
    'STR04와 같은 50명·같은 과제를 분석했으므로 독립 재현 두 건으로 세지 않는다. 증거를 더 많이 언급했다는 사실은 최종 판단 정확도 향상의 증거가 아니다.',
    ['Q1','Q4','Q7','Q8'], 'intelligence_analysis',
    ['turn716200951view3','turn365848255view4','turn689452656view2','turn725394632view1'],
    cohort_group='ACH_50_analysts_shared_STR03_STR04', independent_experiment=False)
add('STR04', 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1530E9DAE8F42B2E8FC2B5FE374DB50F/S1930297500006628a.pdf/boosting-intelligence-analysts-judgment-accuracy-what-works-what-fails.pdf',
    'Boosting intelligence analysts’ judgment accuracy: What works, what fails?',
    'Mandel, Karvetski & Dhami, 2018, Judgment and Decision Making 13(6):607–621',
    'original_randomized_accuracy_study',
    ['Methods: 50 analysts, task and random assignment', '§3.1–3.2 Results, lines 568–623'],
    '평균 절대 확률오차는 대조 .21, ACH .26이었고 두 조건 차이 .04의 95% 구간은 −.02~.11, p=.14였다. 이 과제에서 ACH의 정확도 이득은 입증되지 않았다.',
    'STR03과 같은 표본이고 하나의 인공 정보분석 과제다. 비유의 결과는 효과가 정확히 0이라는 동등성 증명이 아니며 전체 절차형 판단의 무용성을 뜻하지 않는다.',
    ['Q1','Q3','Q5','Q8'], 'intelligence_analysis',
    ['turn716200951view4','turn689452656view3','turn365848255view5'],
    cohort_group='ACH_50_analysts_shared_STR03_STR04', independent_experiment=True)
add('STR05', 'https://www.talytica.com/wp-content/uploads/2016/10/Schmidt-and-Hunter-1998-Validity-and-Utility-Psychological-Bulletin.pdf',
    'The Validity and Utility of Selection Methods in Personnel Psychology: Practical and Theoretical Implications of 85 Years of Research Findings',
    'Schmidt & Hunter, 1998, Psychological Bulletin 124(2):262–274',
    'original_meta_analytic_synthesis',
    ['Table 1', 'pp.266–267: interview construction, validity and training performance, lines 665–688'],
    '당시 보정된 직무수행 예측 타당도는 구조화 면접 .51, 비구조화 .38로 제시됐다. 그러나 훈련 성과 예측은 두 방식 모두 약 .35였고 구조화에는 질문·평가기준 설계 비용이 든다.',
    '상관계수이며 정확도 비율이 아니다. 보정 방식과 효과 크기는 STR08의 재검토와 함께 읽어야 하며 과제·성과 변수에 따라 차이가 사라질 수 있다.',
    ['Q1','Q2','Q7','Q8'], 'structured_interviews',
    ['turn365848255view3','turn890239141view3'],
    independent_experiment=False)
add('STR06', 'https://www.jameslindlibrary.org/wp-data/uploads/2010/05/Antman_Lau_Kupelnick_Mosteller_Chalmers_1992.pdf',
    'A comparison of results of meta-analyses of randomized control trials and recommendations of clinical experts. Treatments for myocardial infarction',
    'Antman et al., 1992, JAMA 268:240–248',
    'original_retrospective_cumulative_evidence_comparison',
    ['Methods, lines 160–185', 'Results and discussion, lines 686–784'],
    '심근경색 치료 무작위시험의 누적 메타분석을 전문가 종설·교과서의 권고 시기와 비교했다. 항혈소판제의 일상 사용을 과반수 종설이 권고하기까지 누적 증거와 약 10년 차이가 있었고, 일부 권고는 불리한 시험 결과를 늦게 반영했다.',
    '동일 예산 무작위 비교가 아닌 후향적 분석이다. 출판 지연·자료 이용 가능성·선택 규칙을 통제하지 않았으므로 체계적 검토가 언제나 옳거나 자유 판단이 언제나 뒤처진다는 증거가 아니다.',
    ['Q1','Q2','Q6','Q8'], 'systematic_vs_narrative_evidence',
    ['turn226448292view2','turn725394632view0','turn229237415view5','turn857427359view2'],
    independent_experiment=False)
add('STR07', 'https://meehl.umn.edu/sites/meehl.umn.edu/files/files/043_when_use_heads.pdf',
    'When Shall We Use Our Heads Instead of the Formula?',
    'Meehl, 1957, Journal of Counseling Psychology 4:268–273',
    'primary_methodological_essay',
    ['pp.1–4 of author PDF: formula validation, broken-leg exceptions, absence of mention; lines 44–62 and 79–146'],
    '공식 판단을 뒤집는 예외는 구체적이며 타당한 추가 정보여야 한다는 논의를 읽었다. 어떤 특성이 기록에 언급되지 않은 것과 실제로 없는 것은 다르다는 구별은 확인 불가를 위반으로 바꾸지 않는 규칙에 대응한다.',
    '신규 실험이 아닌 이론 논문이다. 1954년 책 전체를 읽었다는 뜻이 아니며 예외 처리의 정량적 이득을 이 자료로 계산할 수 없다.',
    ['Q1','Q3','Q6','Q8'], 'clinical_vs_mechanical',
    ['turn725394632view4','turn759006432view1'],
    independent_experiment=False)
add('STR08', 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A20984B138319E3D432E643978BF026D/S175494262300024Xa.pdf/revisiting_the_design_of_selection_systems_in_light_of_new_findings_regarding_the_validity_of_widely_used_predictors.pdf',
    'Revisiting the design of selection systems in light of new findings regarding the validity of widely used predictors',
    'Sackett, Zhang, Berry & Lievens, 2023, Industrial and Organizational Psychology 16:283–300; DOI 10.1017/iop.2023.24',
    'original_author_reanalysis_and_methodological_followup',
    ['pp.283–284: range restriction correction', 'Table 1, p.285', 'pp.287–288: selection design', 'pp.292–293: variability and generalization'],
    '재검토된 직무수행 타당도는 구조화 면접 .42, 비구조화 .19였고 구조화의 80% credibility interval(연구별 참효과 분포 범위)은 .18~.66이었다. 과도한 범위 제한 보정을 고쳤으며 평균 순위 외에 상황별 변동과 개발 비용을 강조했다.',
    '2022 원 연구의 PDF는 403으로 못 읽었고, 여기서는 같은 저자들의 2023 본문을 읽었다. 80% credibility interval을 95% 평균 추정 신뢰구간으로 바꾸어 보고하지 않는다. 독립적인 두 번째 신규 실험이 아니다.',
    ['Q1','Q2','Q7','Q8'], 'structured_interviews',
    ['turn594700361view0','turn229237415view4','turn857427359view1'],
    independent_experiment=False)
add('STR09', 'https://goal-lab.psych.umn.edu/orgpsych/readings/12.%20Judgment%20&%20Decision%20Making/Kuncel,%20Klieger,%20Connelly%20&%20Ones%20(2013).pdf',
    'Mechanical Versus Clinical Data Combination in Selection and Admissions Decisions: A Meta-Analysis',
    'Kuncel, Klieger, Connelly & Ones, 2013, Journal of Applied Psychology 98(6):1060–1072',
    'original_meta_analysis',
    ['pp.1062–1063: inclusion and coding', 'p.1064: results, lines 355–419', 'Discussion: cross-validation and shrinkage'],
    '17개 연구 25개 표본을 합쳤다. 기계적/총체적 결합의 직무수행 타당도는 .44/.28이지만 비학점 성취에서는 .47/.46으로 비슷했고, 신규 표본에 대한 엄격한 축소 보정 시 두 성과의 우세가 사라졌다.',
    '정보를 정해진 방식으로 결합하는 비교이며 검색 과정의 비교가 아니다. 이용 가능한 자료가 제한되어 범위 제한·측정오차 보정과 모집단 일반화에 한계가 있다.',
    ['Q1','Q2','Q8'], 'clinical_vs_mechanical',
    ['turn229237415view0','turn598648162view1'],
    independent_experiment=False)
add('STR10', 'https://publications.gc.ca/collections/collection_2018/rddc-drdc/D69-50-2017-eng.pdf',
    'Restructuring structured analytic techniques in intelligence',
    'Chang et al., DRDC-RDDC-2017-P113, 2017 author report/reprint; catalogue D69-50/2017E-PDF',
    'primary_methodological_critique',
    ['Introduction, lines 94–122', 'Bias polarity and decomposition, lines 238–293', 'Table 2, lines 349–368'],
    '한 방향의 편향을 막는 절차가 반대 방향의 편향을 만들 수 있고, 분해가 잡음을 추가하며, 정보 품질 점검이 과도한 탐색이나 과소 확신을 부를 수 있다는 기제를 정리한다. 구조화 기법별 유효성 검증의 필요성을 논증한다.',
    '새로운 무작위 효과 실험이 아니라 방법론적 비판이다. 과잉 거절과 검색비용 증가를 검사해야 한다는 가설 근거이며, AF-RES-018에서 그러한 현상이 관찰됐다는 증거는 아니다.',
    ['Q1','Q3','Q7','Q8'], 'intelligence_analysis',
    ['turn115324447view1','turn857427359view0','turn573001518view2','turn573001518view8'],
    independent_experiment=False)
add('STR11', 'https://pdodds.w3.uvm.edu/files/papers/others/2010/devries2010a.pdf',
    'Effect of a Comprehensive Surgical Safety System on Patient Outcomes',
    'de Vries et al., 2010, NEJM 363:1928–1937',
    'original_controlled_before_after_study',
    ['pp.1929–1930: methods and checklist pathway', 'Results', 'pp.1935–1936: limitations and implementation'],
    '개입 병원 6곳과 대조 5곳을 비교했고, 개입 병원 수술 전 3,760명·후 3,820명에서 한 가지 이상 합병증 비율은 15.4%에서 10.6%, 사망률은 1.5%에서 0.8%로 감소했다. 입원부터 퇴원까지 전체 경로를 다루는 프로그램이며 대조 병원에서는 같은 변화가 없었다.',
    '비무작위 전후 비교이고 보고 누락·다중 요소 개입의 가능성이 있다. 단일 짧은 점검표의 효과와 같지 않으며 기초 수준이 높은 곳에서는 언제나 무효라는 단정에도 맞지 않는다.',
    ['Q1','Q4','Q8'], 'surgical_checklists',
    ['turn115324447view0','turn573001518view1','turn573001518view7'],
    independent_experiment=True)
add('STR12', 'https://cris.maastrichtuniversity.nl/ws/files/73012849/merrienboer_2013_checklist_improve_experts_diagnostic.pdf',
    'Checklists improve experts’ diagnostic decisions',
    'Sibbald, de Bruin & van Merrienboer, 2013, Medical Education 47(3):301–308; DOI 10.1111/medu.12080',
    'original_within_subject_expert_diagnostic_experiment',
    ['pp.303–304: 15 experts and ECG task', 'Table 1, p.305', 'p.307: limitations'],
    '15명의 심장 전문가가 어려운 심전도를 판독했다. 검증 조건당 89개 판독에서 순수 교정 오류는 체크리스트 26/134, 비체크리스트 3/148이었지만 검증 시간은 평균 63초/35초, 추가 문자 수는 24/4였다.',
    '전문가·심전도라는 한정된 과제이며 초기 오류 수와 판독 수는 다른 분모다. 정확도 개선을 시간 절감으로 바꿔 말할 수 없고 읽는 사람의 검토 시간을 직접 측정한 연구도 아니다.',
    ['Q1','Q6','Q7','Q8'], 'clinical_diagnostic_checklists',
    ['turn183861057view0','turn573001518view0','turn573001518view3','turn573001518view4'],
    independent_experiment=True)
add('STR13', 'https://anaestheticcrisishandbook.com/wp-content/uploads/2015/10/nejm-positive-trial.pdf',
    'Simulation-Based Trial of Surgical-Crisis Checklists',
    'Arriaga et al., 2013, NEJM 368:246–253; DOI 10.1056/NEJMsa1204720',
    'original_randomized_simulation_trial',
    ['pp.247–248: team assignment and simulation design', 'Figure 1, p.249: critical-step failures'],
    '수술실 팀 17개가 106개 모의 위기를 수행했고 각 팀의 절반은 체크리스트, 절반은 기억에 의존하도록 무작위화했다. 중요 단계 누락은 24/371 대 89/379, 보정 위험비 .28(95% 구간 .18~.42)이었다.',
    '분모는 환자나 후보가 아니라 중요 행동 단계다. 모의 상황의 과정 성과이며 실제 사망 감소를 입증하지 않는다. 관측 가능한 위반을 심는 변별력 시험의 설계 유사성만 추론한다.',
    ['Q3','Q4','Q5','Q8'], 'surgical_checklists',
    ['turn183861057view1','turn573001518view5'],
    independent_experiment=True)
add('STR14', 'https://www.academia.edu/94269768/Introduction_of_Surgical_Safety_Checklists_in_Ontario_Canada',
    'Introduction of Surgical Safety Checklists in Ontario, Canada',
    'Urbach et al., 2014-03-13, NEJM 370:1029–1038; DOI 10.1056/NEJMsa1308261; public author-uploaded original article',
    'original_population_before_after_study',
    ['pp.1030–1031: study periods, administrative outcomes and GEE', 'pp.1032–1034 and Tables 1–2: outcomes', 'pp.1035–1037: interpretation, compliance and limitations'],
    '101개 병원의 도입 전 109,341건·후 106,370건 수술에서 사망 .71%→.65%, 합병증 3.86%→3.82%로 유의한 개선을 확인하지 못했다. 본문 Table 2의 보정 전후 비교 p값(.07/.53)과 추가 회귀 분석 p값(.13/.29)은 분석이 다르므로 섞지 않았다. 실행 준수는 병원 자체 보고이고 표준화된 팀 훈련이 의무가 아니었다.',
    '비무작위 전후 설계, 행정자료의 합병증 측정 오류와 실제 준수 수준 미관측이 있다. 전반적 무효성이나 엄격한 동등성의 증거는 아니다. 공개 저자 사본을 읽었으며 NEJM 공식 본문 접근은 403이었다.',
    ['Q1','Q4','Q7','Q8'], 'surgical_checklists',
    ['turn599484801view0','turn960801041view0'],
    independent_experiment=True)

excluded = [
 {'id':'STR-X01','url':'https://www.ucl.ac.uk/medical-sciences','reason':'Haynes paper request redirected to this actual opened faculty landing page; initial request URL was not retained in compacted trace. Successful original reprint is STR02.','level':'D0','body_read':False,'counted':False,'tool_refs':['turn716200951view1']},
 {'id':'STR-X02','url':'https://www.ucl.ac.uk/anaesthesia/sites/anaesthesia/files/urbach-2014.pdf','reason':'Redirected to https://www.ucl.ac.uk/medical-sciences; wrong document. STR14 supplies body.','level':'D0','body_read':False,'counted':False,'tool_refs':['turn716200951view2']},
 {'id':'STR-X03','url':'https://www.nejm.org/doi/full/10.1056/NEJMsa1308261','reason':'HTTP 403 through search-service open. No access-control workaround attempted. Public author copy later found as STR14.','level':'D3-fetch','body_read':False,'counted':False,'tool_refs':['turn365848255view0','turn183861057view2']},
 {'id':'STR-X04','url':'https://citeseerx.ist.psu.edu/document?doi=4d57ade355b1fee8b18921e3be63f04597591efa&repid=rep1&type=pdf','reason':'HTTP 403; Urbach body not obtained here.','level':'D3-fetch','body_read':False,'counted':False,'tool_refs':['turn226448292view0']},
 {'id':'STR-X05','url':'https://www.ices.on.ca/publications/journal-articles/introduction-of-surgical-safety-checklists-in-ontario-canada/','reason':'Author-institution page provides abstract only; not counted as body. Same study as STR14.','level':'D0','body_read':False,'counted':False,'tool_refs':['turn594700361view1']},
 {'id':'STR-X06','url':'https://dash.harvard.edu/entities/publication/925e19ef-d9b6-4d88-b933-21583f35eb2a','reason':'HTTP 429 for paper page; Haynes body obtained from WHO/NCBI instead.','level':'D3-fetch','body_read':False,'counted':False,'tool_refs':['turn365848255view2']},
 {'id':'STR-X07','url':'https://ink.library.smu.edu.sg/lkcsb_research/6894/','reason':'Sackett et al. 2022 landing abstract only. Full text download separately returned 403; STR08 is 2023 author follow-up, not this body.','level':'D0','body_read':False,'counted':False,'tool_refs':['turn890239141view0']},
 {'id':'STR-X08','url':'https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=7893&context=lkcsb_research','reason':'HTTP 403 for 2022 accepted manuscript.','level':'D3-fetch','body_read':False,'counted':False},
 {'id':'STR-X09','url':'https://home.ubalt.edu/NTYGMITC/645/session%204/McDanieletal%20MKUP%201994CriterionValidityInterviewsMeta.pdf','reason':'HTTP 404; body not read.','level':'D3-fetch','body_read':False,'counted':False,'tool_refs':['turn759006432view0']},
 {'id':'STR-X10','url':'https://doi.org/10.1097/sla.0000000000000716','reason':'HTTP 402 Payment Required on DOI route to Haugen 2015. No paid access or access-control workaround.','level':'D3-fetch','body_read':False,'counted':False,'tool_refs':['turn229237415view3']},
 {'id':'STR-X11','url':'https://www.jameslindlibrary.org/mulrow-c-1987/','reason':'Bibliographic page read; original article body not obtained.','level':'D0','body_read':False,'counted':False,'tool_refs':['turn229237415view1']}
]

queries = [
('system1','Grove Zald Lebow Snitz Nelson 2000 Clinical versus mechanical prediction meta-analysis pdf'),
('system1','Haynes 2009 surgical safety checklist global population pdf Urbach 2014 Ontario'),
('system1','analysis competing hypotheses experiment no benefit accuracy Dhami Mandel pdf'),
('system2','"Introduction of Surgical Safety Checklists in Ontario" filetype:pdf'),
('system2','"A Surgical Safety Checklist" "Haynes" "2009" filetype:pdf -site:ucl.ac.uk'),
('system2','"Schmidt" "Hunter" "1998" validity utility selection methods filetype:pdf'),
('system1','"Urbach" "2014" "checklists" filetype:pdf -site:ucl.ac.uk -site:nejm.org'),
('system1','"Sackett" "Zhang" "Berry" "Lievens" "2022" "Revisiting" pdf'),
('system1','"Antman" "Lau" "1992" "Comparison" "Clinical" pdf'),
('system2','"Urbach" "surgical safety" "pdf" -site:nejm.org -site:pubmed.ncbi.nlm.nih.gov -site:ucl.ac.uk'),
('system2','"A comparison of results of meta-analyses" "pdf" Antman'),
('system2','"Sackett" "2022" "apl0000994" pdf'),
('system2','Meehl clinical statistical prediction 1954 pdf'),
('system1','"NEJMsa1308261" pdf -site:nejm.org -site:researchgate.net -site:ucl.ac.uk'),
('system2','"urbach-2014.pdf"'),
('system2','"surgical" "Urbach" "NEJMsa1308261.pdf"'),
('system2','"structured interviews" "McDaniel" "1994" pdf meta analysis'),
('system2','"Effect of the World Health Organization checklist" "Haugen" "2015" pdf'),
('system1','"Introduction of Surgical Safety Checklists" "filetype:pdf" -site:citeseerx.ist.psu.edu -site:ucl.ac.uk -site:nejm.org'),
('system1','"Urbach" "checklists" "2014" site:clevelandclinic.org'),
('system1','"Sackett" "Revisiting the design of selection systems" 2023'),
('system1','"meta-analyses" "narrative reviews" "conclusions" systematic comparison original study'),
('system2','Kuncel Klieger Connelly Ones 2013 mechanical versus clinical data combination pdf'),
('system2','"medical review article" "Mulrow" "1987" pdf'),
('system2','"Restructuring structured analytic techniques" "pdf"'),
('system2','"Haugen" "2015" "stepped wedge" pdf -site:pubmed.ncbi.nlm.nih.gov'),
('system1','"Urbach" "Introduction" "Checklists" filetype:pdf -site:ucl.ac.uk -site:nejm.org -site:citeseerx.ist.psu.edu'),
('system1','"The Medical Review Article: State of the Science" filetype:pdf'),
('system1','"Effect of the World Health Organization Checklist on Patient Outcomes" "pdf" -site:pubmed.ncbi.nlm.nih.gov'),
('system1','"de Vries" "Effect of a comprehensive surgical safety system" pdf'),
('system1','Urbach 2014 Ontario checklists download pdf'),
('system1','"NEJMsa1308261" -site:nejm.org -site:ncbi.nlm.nih.gov -site:pubmed.ncbi.nlm.nih.gov -site:ucl.ac.uk -site:researchgate.net -site:citeseerx.ist.psu.edu'),
('system1','"Arriaga" "2013" "Simulation-Based Trial" pdf'),
('system2','"Checklists improve experts" "diagnostic decisions" pdf'),
('system2','"Simulation-Based Trial of Surgical-Crisis Checklists" pdf'),
('system2','"Urbach2014" pdf Ontario'),
('system2','"surgical safety checklists" "Ontario" "pdf" Urbach Baxter 1029'),
('system1','"Introduction of Surgical Safety Checklists in Ontario, Canada" filetype:pdf site:edu'),
('system1','"Introduction of Surgical Safety Checklists in Ontario, Canada" "download" -site:nejm.org -site:ucl.ac.uk -site:researchgate.net'),
('system1','"Urbach" "2014" "checklist" "PDF" site:toronto.ca')]

def target_for(q):
    ql=q.lower()
    if any(s in ql for s in ['urbach','ontario','nejmsa1308261']): return ['STR14','STR-X02','STR-X03','STR-X04','STR-X05']
    if 'haynes' in ql: return ['STR02','STR-X01','STR-X06']
    if 'grove' in ql: return ['STR01']
    if 'sackett' in ql: return ['STR08','STR-X07','STR-X08']
    if 'schmidt' in ql: return ['STR05']
    if 'meehl' in ql: return ['STR07']
    if 'antman' in ql or 'comparison of results' in ql or 'narrative reviews' in ql: return ['STR06']
    if 'kuncel' in ql: return ['STR09']
    if 'restructuring' in ql: return ['STR10']
    if 'competing hypotheses' in ql: return ['STR03','STR04']
    if 'de vries' in ql: return ['STR11']
    if 'experts' in ql: return ['STR12']
    if 'arriaga' in ql or 'surgical-crisis' in ql: return ['STR13']
    if 'mcdaniel' in ql: return ['STR-X09']
    if 'haugen' in ql or 'world health organization checklist' in ql: return ['STR-X10']
    if 'mulrow' in ql or 'medical review article' in ql: return ['STR-X11']
    return []

log = dict(task='AF-RES-018', component='other-field structured versus free judgment evidence',
  accessed_at_utc=WINDOW, time_precision='Session interval; exact per-query wall times unavailable. Query strings and order were preserved from tool calls.',
  queries=[dict(sequence=i, engine=engine, query=q, purpose='Find original evidence and counterexamples; locate public author/institution copies without access-control circumvention', selected_record_ids=target_for(q)) for i,(engine,q) in enumerate(queries,1)],
  open_records=[dict(id=s['id'],url=s['url'],body_read=s['body_read'],result='Original paper body read',tool_refs=s['tool_refs']) for s in sources]+excluded,
  counterexample_searches=[
    dict(hypothesis='Structure necessarily improves accuracy',queries=[3,25],result_ids=['STR03','STR04','STR10'],result='More evidence coverage and non-improving accuracy coexist; mechanisms for overcorrection are hypotheses, not new trial results.'),
    dict(hypothesis='Checklists reliably improve ordinary-practice outcomes',queries=[2,4,7,10,14,15,16,19,20,27,31,32,36,37,38,39,40],result_ids=['STR14'],result='Named Ontario null study obtained and read; contrasts with STR02 and STR11.'),
    dict(hypothesis='Accuracy gains imply less review work',queries=[34],result_ids=['STR12'],result='Checklist error correction improved while verification time and output length increased.'),
    dict(hypothesis='Structured methods win equally for every outcome',queries=[6,8,12,17,21,23],result_ids=['STR05','STR08','STR09'],result='Training and non-GPA outcomes, shrinkage and between-context variability limit a universal advantage claim.'),
    dict(hypothesis='A formal rule should reject every missing condition',queries=[13,25],result_ids=['STR07','STR10'],result='Non-mention is not absence; overshooting corrections are a possible mechanism to test.')],
  network_approval_event=dict(action='tools.write_stdin on anonymous-host-probe session 57463',
    result='Auto-review rejected output retrieval; no retry or workaround',
    stated_reason='Reviewer described a web.archive.org probe and blocked-host bypass risk.',
    observed_command_hosts=['citeseerx.ist.psu.edu','ink.library.smu.edu.sg','www.jameslindlibrary.org','meehl.umn.edu','home.ubalt.edu','goal-lab.psych.umn.edu','www.ices.on.ca','publications.gc.ca','doi.org','pdodds.w3.uvm.edu','cris.maastrichtuniversity.nl','anaestheticcrisishandbook.com'],
    discrepancy='web.archive.org was not present in the submitted command; nevertheless the rejected action was not repeated. Output and response codes from that process are unavailable.',
    retained_evidence='NETWORK.json has the eight earlier successful observations. Normal public search/open body retrieval remains separately recorded.',
    reported_to_parent=True))

(ROOT/'sources.json').write_text(json.dumps(dict(sources=sources,excluded=excluded,counting_policy=dict(body_required=True,same_site_cap=3,documents=14,empirical_vs_methodological='STR07 and STR10 are primary theoretical/methodological work, not new empirical experiments; original meta-analyses retained as method/comparison literature.',shared_cohorts=['STR03 and STR04 use the same 50 analysts.'],own_results='No AF-RES-018 A/P outcomes are known to this literature contributor.')),ensure_ascii=False,indent=2)+'\n')
(ROOT/'SEARCH_LOG.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(sources),'excluded':len(excluded),'queries':len(queries),'output_paths':[str(ROOT/'sources.json'),str(ROOT/'SEARCH_LOG.json')]},ensure_ascii=False))
