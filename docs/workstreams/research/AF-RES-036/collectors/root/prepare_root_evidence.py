"""Preserve directly read Q7 correction evidence; no software case is added."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
D=Path(__file__).resolve().parent;P=D.parents[1]
sys.path.insert(0,str(P/'collectors/gnu'))
from parse_html import parse
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj):(D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
A={a['attempt_id']:a for a in map(json.loads,(D/'attempts.jsonl').read_text().splitlines()) if a.get('operation')=='GET'}
(D/'extracts').mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat()
doc=parse(D/'raw/CX-B16.html');tx=doc['text'];start=tx.index('Printed by Thomas Warren');end=tx.index('--ESTC',start)+len('--ESTC')
excerpt=tx[start:end]
ex16={'source_id':'CX-B16','url':A['ROOT-GET-CX-B16']['url'],'original_body_sha256':doc['member_sha256'],
      'normalization':doc['normalization'],'normalized_text_sha256':sha(tx.encode()),'start_char':start,'end_char':end,
      'exact_excerpt':excerpt,'excerpt_sha256':sha(excerpt.encode()),'read_location':'NULDL000040 Note and Remarks; web lines55-84',
      'license':'metadata explicitly CC0','read_utc':now}
write('extracts/CX-B16.json',ex16)
pdf=(D/'raw/CX-B17.pdf').read_bytes();pt=(D/'raw/CX-B17.txt').read_text()
quote='printed by Thomas Warren and second part (sig. 2C-3D4) by Richard Cotes.'
qstart=pt.index(quote)
meta=parse(D/'raw/CX-B17.html');mt=meta['text']
assert '2016-03-31' in mt and '2016-04-19' in mt
ex17={'source_id':'CX-B17','url':A['ROOT-GET-CX-B17-PDF']['url'],'original_body_sha256':sha(pdf),
      'normalization':'pdftotext -layout; invalid-font-weight warnings, exit0; layout-order text inspected',
      'normalized_text_sha256':sha(pt.encode()),'start_char':qstart,'end_char':qstart+len(quote),
      'exact_excerpt':quote,'excerpt_sha256':sha(quote.encode()),'read_location':'PDF pp1-3; English abstract pp1-2 and opening Japanese discussion p3',
      'metadata_body_sha256':meta['member_sha256'],'metadata_url':A['ROOT-GET-CX-B17-META']['url'],
      'metadata_locations':'repository publication date2016-03-31, deposit2016-04-19, version display2021-03-01; web lines98,183-204',
      'read_utc':now,'full_pdf_retained_in_commit':False,'ornament_image_comparison_replicated':False}
write('extracts/CX-B17.json',ex17)
rows=[{'source_id':'CX-B16','kind':'library_explicit_bibliographic_correction','publisher':'Nagoya University Library / THERS',
       'original_url':ex16['url'],'fixed_url':None,'publication_date':None,'version':'NULDL000040, 1651 head edition, first issue; record update date unconfirmed',
       'checked_utc':A['ROOT-GET-CX-B16']['finished_utc'],'read_utc':now,'read_location':ex16['read_location'],
       'findings':'도서관 Note는 앞부분 A–2B 인쇄자를 Roger Norton으로 보던 귀속이 틀렸다고 명시하고 Thomas Warren·Richard Cotes 및 Takano2016 pp1–17을 근거로 제시한다. 원책1651 표기와 정정 연구2016을 구별한다.',
       'questions':['Q7','Q8'],'case_ids':['CROSS-BIB-CORRECTION'],'limitations':'국립대학 도서관 원자료다. 같은 레코드의 정정 전 snapshot과 변경UTC는 없으므로 정정 전파 지연·레코드 변경일은 알 수 없다. 소프트웨어12개 분모에 포함하지 않는다.',
       'duplicate_group':'NULDL000040-head-edition-catalogue','count_minimum':True,'count_categories':['cross_field_supplement'],
       'body_sha256':ex16['original_body_sha256'],'excerpt_path':'collectors/root/extracts/CX-B16.json','read_status':'necessary_content_confirmed'},
      {'source_id':'CX-B17','kind':'dated_original_bibliographical_research','publisher':'Nagoya University Library Studies / Akira Takano',
       'original_url':ex17['url'],'fixed_url':'https://doi.org/10.18999/annul.13.1','publication_date':'2016-03-31','deposit_date':'2016-04-19',
       'version':'Annals of Nagoya University Library Studies13, pp1–17; publisher version',
       'checked_utc':A['ROOT-GET-CX-B17-PDF']['finished_utc'],'read_utc':now,'read_location':ex17['read_location'],
       'findings':'원 연구의 초록과 문제제기는 head판 장식·손상활자 비교로 A–2B는 Thomas Warren, 2C–3D는 Richard Cotes라고 결론내리며 Roger Norton 귀속을 반박한다. 도서관 정정의 날짜 있는 근거와 제목·권·쪽이 일치한다.',
       'questions':['Q7','Q8'],'case_ids':['CROSS-BIB-CORRECTION'],
       'limitations':'논문 pp1–3의 주장/근거 요약을 직접 읽었으며 모든 장식 도판·활자를 독립 대조하지 않았다. 이것은 head판 연구이며 ornaments판1680/1700/1695 충돌을 해결하지 않는다. HTML초록과PDF를 한 원고로 센다.',
       'duplicate_group':'Takano2016-head-edition-study','count_minimum':True,'count_categories':['cross_field_supplement'],
       'body_sha256':sha(pdf),'excerpt_path':'collectors/root/extracts/CX-B17.json','read_status':'necessary_content_confirmed',
       'observations':[A['ROOT-GET-CX-B17-META'],A['ROOT-GET-CX-B17-PDF']]}]
(D/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows))
(D/'notes.md').write_text('''# Q7 후속 정정 자료

CX-B16 도서관 Note의 명시 정정과 CX-B17 원 연구의 제목·권·쪽·주장을 직접 대조했다. 정정의 학술 근거는 2016-03-31 발행 논문이며 저장소 공개일2016-04-19와 별개다. catalog URL의20230901 숫자는 레코드 정정일로 해석하지 않았다. 같은 레코드의 정정전판/변경UTC는 여전히 미확인이다.

이 보강은 기존 ornaments판의1680/ca1700/1695 충돌과 다른 head판 사례다. 두 판을 같은 수정 사슬로 연결하지 않는다. 본문 도판을 모두 재검증한 서지학적 참값이 아니라, 발행자/소비 도서관의 문헌 관계 확인이다.

실제 판/번역을 지목한 공개 참고문헌 쌍은 기존 CX-B03(NLI1953/Anscombe)–CX-B04(SEP Summer2022의1953p222 및2009별도서지)다. 새 catalog가 SEP에서 사용되었다고 주장하지 않는다.

추가 소비자 후보 Study Series80의 옛PDF URL은 ROOT-GET-CX-B18에서503/98B였다. web open은2025-09-10 저장소 이전 안내를 보여 주었고 새홈페이지는429였다. 검색요약의 옛PDF 문장은 직접 열람 원문에 산입하지 않는다. 다음 첫 원문은 공식 새 저장소의 해당 Study Series80 개별 논문 record이며 실제 본문과 원URL 대응을 확인해야 한다. 이미 확인한 원문 최소수는 이 후보의 성공 여부에 의존하지 않는다.
''')
write('commit-files.json',[str(f.relative_to(P)) for f in [D/'prepare_root_evidence.py',D/'sources.jsonl',D/'attempts.jsonl',D/'notes.md',D/'extracts/CX-B16.json',D/'extracts/CX-B17.json',D/'commit-files.json']])
print(json.dumps({'eligible_new_manuscripts':2,'raw_pdf_bytes':len(pdf),'short_exact_quote_words':len(quote.split())}))
