"""Record completed self-readings; this script does not perform the reading."""
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
catalog_time='2026-11-22T20:38:31Z'
now=datetime.now(timezone.utc).isoformat()
path=ROOT/'streams/root/sources.jsonl'
rows=[json.loads(line) for line in path.read_text().splitlines()]
by_id={r['source_id']:r for r in rows}
all_sources={r['source_id']:r for r in map(json.loads,(ROOT/'sources.jsonl').read_text().splitlines())}

def add(row):
    by_id[row['source_id']]=row

def base(sid,url,locator,kind,fact,limitation,group,date='미확인',publisher='미확인',stamp=catalog_time):
    return dict(source_id=sid,original_url=url,pinned_url_or_version='2026-11-22 직접 열람 범위; '+locator,
        publisher=publisher,event_or_publication_date=date,checked_utc=stamp,locator=locator,
        source_kind=kind,verified_fact=fact,limitation=limitation,question_ids=['Q1','Q6','Q7'],
        case_ids=['B01'],duplicate_group=group,counted=False,quota_category='excluded',
        observation_type='직접 열람/자체 재판독; 독립 인간 검증 아님')

add(base('ROOT-R011','https://luc.devroye.org/fonts-104548.html','web L13–19 links only','discovery_index',
    'URW책자 GoogleBooks 레코드와 Zapf/Thành/Karow 링크를 직접 확인하여 원본 탐색에 사용.',
    '역사적 설명은2차서술이므로 본 연구의 사실근거·최소수에 사용하지 않음. 원영문본문 링크는 발견하지 못함.',
    'devroye-hz-navigation',publisher='Luc Devroye / McGill affiliation'))
add(base('ROOT-R012','https://books.google.ca/books/about/Hz_program.html?id=Ox4jywAACAAJ&redir_esc=y',
    'record Ox4jywAACAAJ; web L14–22 Title/Author/Publisher/Length','catalogue_record',
    '제목 Hz-program: micro-typography for advanced typesetting; URW Software & Type GmbH.; publisher1993;38pages를 확인.',
    '현재 서지레코드만 읽음. 본문/표제/간기 없음.1992회고와 같은판인지미확인. 필요한기관최소수는다른3저작으로충족하여추가산입안함.',
    'googlebooks-urw-hz1993',date='서지1993; 레코드작성일미확인',publisher='Google Books catalogue / URW attribution'))
add(base('ROOT-R013','https://tug.org/TUGboat/tb36-2/tb113zapf-karow.pdf','web open returned403; no body in this attempt',
    'access_failure','웹열기403. 이후 일반HTTP재개봉에서200·본문확인 성공; ROOT-R020/B01-P019 참조.',
    '이 실패 응답으로본문을읽었다고세지않음. 재개자료는같은TUG원문p97refs5/10.',
    'karow-zapf2015',date='2015',publisher='TeX Users Group',stamp='2026-11-22T20:37:57Z'))
add(base('ROOT-R014','https://books.google.ca/books/about/Hz_program.html?id=Ox4jywAACAAJ&redir_esc=y',
    'direct web reopen unavailable at20:37:57Z; linked click recovered at20:38:31Z',
    'access_failure','직접open경로는읽을수없음; 실제페이지링크를따른click은서지본문을반환.',
    '본문미리보기는없음. 레코드성공과일시적인접근실패를구분하며최소수추가안함.',
    'googlebooks-urw-hz1993',publisher='Google Books',stamp='2026-11-22T20:37:57Z'))

facts={
'B01-P019':('printedp97 References5,10','후대책자연도1992와기존1993서지가불일치. 원판간기없이같은판발행연도를고치지않음.'),
'B01-P001':('physical/thesisp38,pp69–70,pp117–118 refs40–43','hz영감·구현정보부재,level1/2,정확참고문헌전사를다시확인. 최초독서일은없음.'),
'B01-P004':('physicalp5/printedp248 §7; visual rendering also checked','폭축MultipleMaster와문단줄바꿈제안이이미존재. 최초hz독서전이었다는증거는아님.'),
'B01-P006':('printedp34footnote,p54Fig21;pp49,56–57','공인번역관계와Ek의흰내부공간변경·획두께보존을본문/도판으로재확인.'),
'B01-P003':('printedpp146–148; font expansion primitives and modes','돌출과자폭의별도제어·확장font준비·줄바꿈유지/관여설명을확인.'),
'B03-L001':('mf/feta-toevallig.mf L11–27; fonts.docL11–23','출판사·작품·기호귀속과sharp수평끝미채택comment를재확인.'),
'B03-L011':('mf/feta-toevallig.mf L1–5,140–167; autometric.mf extent semantics','같은flat의기존귀속·crook_fatness·set_char_box(0,9/12…)와기호정체성확인.'),
'B03-L012':('mf/feta-toevallig.mf L1–5,114–125,188–205; autometric.mfL46–63,99–110','Müller귀속과윤곽함수·w#/b#·crook_fatness변경. 전체잉크폭실측과구별.'),
'B01-P013':('web2c-7.3.3/texk/web2c/pdftexdir/pdftex.ch L5108–5129,5460–5469','>1후보줄계산과>0줄packing분리를직접재확인. 역사실행없음.'),
}
receipts=json.loads((ROOT/'evidence/final-recheck-downloads.json').read_text())
for i,receipt in enumerate(receipts,20):
    original=all_sources[receipt['source_id']]
    row={k:v for k,v in original.items() if k not in ['reading_record','stream_quota_category']}
    row.update(source_id=f'ROOT-R{i:03d}',checked_utc=receipt['checked_utc'],counted=False,
        quota_category='excluded',source_kind='primary_body_self_recheck',
        locator=facts[receipt['source_id']][0],verified_fact=facts[receipt['source_id']][1],
        observation_type='root 직접 재개봉·정적판독; 같은작업 자체점검',
        duplicate_group=original['duplicate_group'],artifact_sha256=receipt.get('sha256','미확인'),
        original_source_id=receipt['source_id'],access_result=receipt['access'])
    row['limitation']='반복열람으로최소수제외. '+original['limitation']
    add(row)

for number,sid,locator,fact in [
    (40,'ED001','printedIII; cachedpublisherPDF visual re-read','Dürr·BA5527추출·©1988·3쇄2008·편집추가임시표smallprint를직접재판독.'),
    (41,'ED020','single raster page m127–135; voice128,piano129,horn131–132','보표별sharp/natural/flat은식별. 내부판번호·쪽·간기는없어정확역사판면으로판정못함.'),
    (42,'ED007','officialFH6064 whole450×620 sample,study1','제목·작곡가op64·연습곡·기호·FH6064footer직접재판독. 저해상도라curve/serif정량대조안함.'),
]:
    original=all_sources[sid]
    row={k:v for k,v in original.items() if k not in ['reading_record','stream_quota_category']}
    row.update(source_id=f'ROOT-R{number:03d}',checked_utc=now,counted=False,quota_category='excluded',
        source_kind='cached_primary_body_self_recheck',locator=locator,verified_fact=fact,
        observation_type='앞서원URL에서받은보존본문을root가시각재판독;새HTTP요청아님',original_source_id=sid)
    row['limitation']='반복열람으로최소수제외. '+original['limitation']
    add(row)
path.write_text(''.join(json.dumps(by_id[key],ensure_ascii=False)+'\n' for key in sorted(by_id)))
for sid in ['ROOT-R013','ROOT-R040','ROOT-R041','ROOT-R042']:
    by_id[sid]['logged_utc']=now
    by_id[sid]['checked_utc']='미확인'
    by_id[sid]['review_date_utc']='2026-11-22'
    by_id[sid]['limitation']+=' 이 반복/실패 판독의 정확한 초 단위 시각은 미기록이므로 미확인으로 둠. 원다운로드 시각은 원래 source_id와 receipts 참조.'
path.write_text(''.join(json.dumps(by_id[key],ensure_ascii=False)+'\n' for key in sorted(by_id)))

frame_path=ROOT/'streams/root/frame.csv'
frame=list(csv.DictReader(frame_path.open()))
frame=[row for row in frame if row['frame_id']!='R-F09']
frame.append(dict(frame_id='R-F09',case_id='B01',function='exact English donor edition',baseline='initial/code donor identity',
 original_candidate='URW1993 brochure and possible1992label',query_or_entry='"URW" "hz-program" "1993" brochure library; exacttitle PDF',
 catalog_or_publisher='TUG official; McGill navigation; GoogleBooks catalogue',search_utc=catalog_time,
 url='https://books.google.ca/books/about/Hz_program.html?id=Ox4jywAACAAJ&redir_esc=y',
 access_result='catalogue1993/38pp read; originalbody unavailable;2015authorreference1992contradiction',
 decision_or_exclusion='navigation/catalogue/failure and latepaper supplementary only; no additionalminimumcount',
 source_ids='ROOT-R011;ROOT-R012;ROOT-R013;ROOT-R014;B01-P019;B01-P095'))
with frame_path.open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(frame[0]),lineterminator='\n');writer.writeheader();writer.writerows(frame)
print('root ranges',len(by_id),'final reopened bodies',len(receipts),'successes',sum(r['access'].startswith('success') for r in receipts))
