"""Stage1 semantic spot checks recorded before new-edition exposure."""
from pathlib import Path
import csv,json,datetime,hashlib
from lxml import html
ROOT=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=list(csv.DictReader((ROOT/'stage1-frame.csv').open()))
reviews={
'gallery/misc/hyperlinks_sgskip.html':('SVG 산점도 점마다 다른 외부 링크를 붙이고 scatter.svg로 저장한다.','plt.scatter, PathCollection.set_urls([BBC,Google,None]), Figure.savefig(\"scatter.svg\")','L1029 import-only 블록을 첫 API방법으로 잘못 고른 파서 오류를 봉인 전에 교정. 첫 실제 예제는 L1034~1038 scatter+set_urls; 뒤의 imshow+set_url image.svg는 두 번째 예제이므로 목적에 합치지 않음. SVG 파일 자체는 이 판에서 연결된 출력으로 확인하지 않았고 대표 자원은 downloadable Python source.'),
'gallery/spines/multiple_yaxis_with_spines.html':('하나의 거리 x축을 공유하며 밀도·온도·속도에 서로 다른 3개 y축과 색을 배치한다.','Axes.twinx 두 번과 twin2.spines.right.set_position(("axes",1.2)); 각 Axes.plot 및 축/눈금 색 지정','첫 그림 1개; 실제 id multiple-yaxis-with-spines. 상이한 y척도와 오른쪽 spine offset 설명·호출 연결.'),
'gallery/lines_bars_and_markers/barchart.html':('G1~G5의 Men/Women 점수를 나란한 막대와 수치 라벨로 비교한다.','Axes.bar(x-width/2,...), Axes.bar(x+width/2,...); Axes.bar_label 두 호출','그림은 코드 뒤 L1058. grouped-bar-chart-with-labels id. 구체 데이터와 grouped-bar 목적은 분리해 보존.'),
'gallery/scales/custom_scale.html':('경도 대비 위도를 Mercator 방식으로 변환하고 극 부근을 제한해 시각화한다.','ScaleBase 상속 MercatorLatitudeScale, Transform/inverted/limit_range_for_scale, register_scale, plt.yscale("mercator")','단순 FuncScale 대안이 본문에 있으나 첫 예제 실제 방법은 사용자 정의 ScaleBase/Transform. 대안 언급을 첫 예제 API로 바꾸지 않음.'),
'gallery/mplot3d/polys3d.html':('서로 다른 lambda의 곡선 아래를 반투명 다각형으로 채워 3차원 깊이 방향에 나열한다.','PolyCollection(verts,...alpha=.7) 후 Axes3D.add_collection3d(...zs=lambdas,zdir="y")','첫 그림1개, generate-polygons-to-fill-under-3d-line-graph id; polygon_under_graph와 probability곡선을 연결.'),
'gallery/shapes_and_collections/ellipse_demo.html':('서로 다른 위치·크기·각도·색·투명도의 타원250개를 같은 축에 배치한다.','patches.Ellipse 목록과 Axes.add_artist, Patch.set_clip_box/set_alpha/set_facecolor','처음 gallery title section이 첫 논리 예제에서 닫히고 페이지 공통 다운로드는 뒤에 있다. section 범위에 download가 없다는 이유로 제외했던 parser를 봉인 전에 교정. 그림/코드는 첫절 내부. 합성 목적은 첫250 타원만.')
}
manual=[]
for r in rows:
    r['author_source_path']='examples/'+r['page_path'].removeprefix('gallery/').removesuffix('.html')+'.py'
    if r['page_path'] not in reviews: continue
    v,a,n=reviews[r['page_path']];r['purpose_visual']=v;r['purpose_api']=a;r['purpose_extraction']='direct static HTML/code review before new paths';r['inspected_directly']='YES'
    b=(ROOT/'.cache'/('old-'+r['page_path'].replace('/','_').replace('.html','')+'.bin')).read_bytes()
    doc=html.fromstring(b);sec=doc.xpath('//section[contains(@class,"sphx-glr-example-title")]')[0]
    preserve=ROOT/'observations'/('old-'+Path(r['page_path']).stem+'-section.html')
    preserve.write_bytes(html.tostring(sec,encoding='utf-8'))
    rec=json.loads((ROOT/'receipts'/('old-'+r['page_path'].replace('/','_').replace('.html','')+'.json')).read_text())
    manual.append({'page_path':r['page_path'],'original_url':r['body_url'],'fragment':r['fragment'],'direct_reread_utc':now,'original_received_utc':rec['received_utc'],'purpose_visual':v,'purpose_api':a,'observation':n,'source_path':r['source_path'],'resource_path':r['old_resource_path'],'first_image_line':r['first_image_line'],'section_start_line':sec.sourceline,'section_snapshot':str(preserve.relative_to(ROOT.parent.parent)),'body_sha256':r['body_sha256'],'limits':'Static HTML and author code; image pixels, examples, browser and G not yet observed.'})
fields=list(rows[0])
with (ROOT/'stage1-frame.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
(ROOT/'stage1-direct-review.json').write_text(json.dumps(manual,ensure_ascii=False,indent=2)+'\n')
summary=json.loads((ROOT/'stage1-summary.json').read_text());summary.update(direct_old_body_reviews=len(manual),direct_materials=len(manual),logical_examples_before_inherited_exclusion=521,redirect_alias_count=36,download_only_count=39,inline_only_remaining=0,stage1_finalized_utc=now)
(ROOT/'stage1-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
control=sorted([r for r in rows if r['eligible']=='YES'],key=lambda r:(r['hash_sha256'],r['old_section_path']))[:4]
(ROOT/'stage1-control-order.json').write_text(json.dumps({'created_utc':now,'rule':'first4 by AF106 hash among remaining old eligible pages; after main selection skip overlaps and continue same hash order; solely material-minimum/control, never main confusion rates','first4':control},ensure_ascii=False,indent=2)+'\n')
ledger=[]
for r in rows:
    if r['access']!='automatic_html_read': continue
    key='old-'+r['page_path'].replace('/','_').replace('.html','');rec=json.loads((ROOT/'receipts'/f'{key}.json').read_text())
    direct=r['inspected_directly']=='YES'
    ledger.append({'source_id':'MP106-'+key,'question':['Q1'],'case':r['page_path'],'original_url':r['body_url'],'immutable_url':r['body_url'],'preserved_path':'evidence/matplotlib/old-observations.json','opened_utc':rec['requested_utc'],'direct_review_utc':now if direct else None,'publisher':'Matplotlib project','lineage':'Matplotlib logical example '+r['page_path'],'version':'3.6.3','location':r['old_section_path'] or r['page_path'],'fingerprint':{'body_sha256':rec['sha256'],'git_blob_verified':r.get('old_git_blob_matches'),'bytes':rec['bytes']},'observed':r['purpose_visual'] if direct else ('Automatic inventory: '+r['eligible']+'; '+r['exclusion']),'supports_or_refutes':'Old purpose/code/resource eligibility; no new-edition conclusion','limitations':'Static-only; no example/browser execution. New edition unopened.','status':'new' if direct else 'automatic_scan','countable':direct,'category':'example_body' if direct else 'automatic_inventory','count_reason':'Directly read original section and code; one work per example' if direct else 'Machine inventory only; excluded from unique primary count','receipt':'evidence/matplotlib/receipts/'+key+'.json'})
for key,path,url in [('old-edition-tree','old-publication-paths.json','https://api.github.com/repos/matplotlib/matplotlib.github.com/git/trees/3252e5b162258de399b9fa614b6854bd9da661f9?recursive=1'),('old-author-tree','old-author-tree.json','https://api.github.com/repos/matplotlib/matplotlib/git/trees/655f616e86e2c0f7724d7c88717d4ac4eb438c57?recursive=1')]:
    rec=json.loads((ROOT/'receipts'/f'{key}.json').read_text())
    ledger.append({'source_id':'MP106-'+key,'question':['Q1'],'case':'population','original_url':url,'immutable_url':url,'preserved_path':'evidence/matplotlib/'+path,'opened_utc':rec['requested_utc'],'publisher':'Matplotlib project','lineage':'3.6.3 publication/source tree metadata inherited AF-RES-102','version':'3.6.3','location':'complete recursive tree','fingerprint':{'sha256':rec['sha256'],'bytes':rec['bytes']},'observed':'Complete old publication/source path inventory, not rendered display','supports_or_refutes':'Q1 complete path denominator','limitations':'Listing does not establish use or G','status':'inherited','countable':False,'category':'deployment_listing','count_reason':'AF-RES-102 fixed publication/source metadata; no new-count credit','receipt':'evidence/matplotlib/receipts/'+key+'.json'})
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(summary,ensure_ascii=False,indent=2))
