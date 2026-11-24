#!/usr/bin/env python3
"""Recompute Q7 static link relationships from preserved public source bytes."""
import base64,collections,datetime,hashlib,json,pathlib,urllib.parse
from lxml import etree,html
from PIL import Image
ROOT=pathlib.Path(__file__).parent
J=lambda f:json.loads((ROOT/f).read_text())
def sha(f):return hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
def state(manifest,canvas):return {'id':canvas,'type':'Canvas','partOf':[{'id':manifest,'type':'Manifest'}]}
def encoded(d):return base64.urlsafe_b64encode(urllib.parse.quote(json.dumps(d,separators=(',',':')),safe="~()*!.'").encode('utf-8')).decode().rstrip('=')
def image_info(f):
 with Image.open(ROOT/f) as im:return {'file':f,'format':im.format,'width':im.width,'height':im.height,'sha256':sha(f)}
r=J('rijksmuseum-manifest.json');rc=r['items'][0];ra=rc['items'][0]['items'][0]
f=J('fitzwilliam-manifest.json');fc=f['items'][0];fa=fc['items'][0]['items'][0];comments=fc['annotations'][0]['items']
m=J('fitzwilliam-micrograph-393.json');mc=m['items'][0]
x=etree.parse(str(ROOT/'plos-spark.xml'),etree.XMLParser(resolve_entities=False,no_network=True));h=html.fromstring((ROOT/'plos-spark.html').read_bytes())
figs=[]
for fig in x.xpath('//fig'):
 fid=fig.get('id');hid=fid.replace('.','-');refs=[]
 for ref in x.xpath('//xref[@ref-type="fig"][@rid=$id]',id=fid):
  sec=next(ref.iterancestors('sec'),None);p=next(ref.iterancestors('p'),None);table=next(ref.iterancestors('table-wrap'),None)
  refs.append({'line':ref.sourceline,'sec_id':sec.get('id') if sec is not None else None,'section_title':' '.join(sec.xpath('./title//text()')) if sec is not None else None,'parent_tag':ref.getparent().tag,'table_id':table.get('id') if table is not None else None,'table_caption':' '.join(' '.join(table.xpath('./caption//text()')).split()) if table is not None else None,'paragraph':' '.join(''.join(p.itertext()).split()) if p is not None else None})
 figs.append({'xml_id':fid,'xml_line':fig.sourceline,'direct_graphic':fig.xpath('./graphic/@xlink:href',namespaces={'xlink':'http://www.w3.org/1999/xlink'}),'caption':' '.join(' '.join(fig.xpath('./caption//text()')).split()),'xml_id_occurs_as_html_id':len(h.xpath('//*[@id=$id]',id=fid)),'actual_html_id':hid,'actual_html_id_count':len(h.xpath('//*[@id=$id]',id=hid)),'html_fragment_link':'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#'+hid,'refs':refs})
report={
'computed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'method':'Static parsing of saved IIIF JSON, JATS XML and publisher HTML; raster decode. No browser execution or historic build inference.',
'riiif':{'manifest':r['id'],'context':r['@context'],'canvas_count':len(r['items']),'canvas':rc['id'],'annotation_page':rc['items'][0]['id'],'painting_annotation':ra['id'],'painting_target':ra['target'],'painting_body_id':ra['body']['id'],'thumbnail_id':r['thumbnail'][0]['id'],'thumbnail_used_as_painting_body':r['thumbnail'][0]['id']==ra['body']['id'],'declared_body_width':ra['body']['width'],'declared_body_height':ra['body']['height'],'body_image':image_info('rijksmuseum-painting-body.jpg'),'thumbnail_image':image_info('rijksmuseum-thumbnail.jpg'),'content_state':state(r['id'],rc['id']),'content_state_encoded':encoded(state(r['id'],rc['id']))},
'fitz':{'manifest':f['id'],'context':f['@context'],'canvas':fc['id'],'annotation_page':fc['items'][0]['id'],'painting_annotation':fa['id'],'painting_target':fa['target'],'choice_count':len(fa['body']['items']),'choice_items':[{'id':i['id'],'label':i.get('label'),'format':i['format']} for i in fa['body']['items']],'comment_count':len(comments),'invalid_null_xywh_count':sum('#xywh=null,null,null,null' in str(i.get('target')) for i in comments),'targets':dict(collections.Counter(str(i.get('target')) for i in comments)),'first_comment_id':comments[0]['id'],'first_comment_target':comments[0]['target'],'micrograph_manifest':m['id'],'micrograph_canvas':mc['id'],'micrograph_body':mc['items'][0]['items'][0]['body']['items'][0]['id'],'micrograph_content_state':state(m['id'],mc['id']),'whole_canvas_content_state':state(f['id'],fc['id']),'whole_canvas_content_state_encoded':encoded(state(f['id'],fc['id'])),'meaning':'17 optional imaging resources and 32 commentary entries are separate relations; coordinate arrival and viewer selection were not tested.'},
'plos':{'xml_sha256':sha('plos-spark.xml'),'html_sha256':sha('plos-spark.html'),'dtd_version':x.getroot().get('dtd-version'),'declared_subjects':x.xpath('//article-meta/article-categories//subject/text()'),'fig_count':len(figs),'fig_xref_count':len(x.xpath('//xref[@ref-type="fig"]')),'all_figs_have_xml_id_target':all(x.xpath('//*[@id=$id]',id=e.get('rid')) for e in x.xpath('//xref[@ref-type="fig"]')),'figures':figs,'images':[image_info('plos-figure7.png'),image_info('plos-figure8.png')],'same_fig_reused':'g007 has references in both Results sec022 and Discussion sec025; same target, different explanatory contexts. Five g007 xrefs are four prose references and one table-caption reference; t003 caption names r_Ncut but targets g007, whose figure caption and raster show normalized association. Intended correction is 미확인. g007 and g008 have similar 4-panel boxplot form but different normalized-association and normalized-cut quantities.'}
}
(ROOT/'static-analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'iiif-return-payloads.json').write_text(json.dumps({'rijksmuseum_canvas':report['riiif']['content_state'],'fitzwilliam_whole_canvas':report['fitz']['whole_canvas_content_state'],'fitzwilliam_face_micrograph':report['fitz']['micrograph_content_state'],'limitations':'Exact content-state payloads from observed Manifest/Canvas IDs. Viewer compatibility, UV Choice activation and dynamic focus remain 미확인. No fabricated numeric xywh replaces the null coordinates.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rijks_canvases':report['riiif']['canvas_count'],'fitz_choices':report['fitz']['choice_count'],'fitz_comments':report['fitz']['comment_count'],'fitz_null_targets':report['fitz']['invalid_null_xywh_count'],'plos_figs':report['plos']['fig_count'],'plos_fig_xrefs':report['plos']['fig_xref_count'],'plos_xml_ids_in_html':[z['xml_id_occurs_as_html_id'] for z in figs],'plos_actual_html_ids':[z['actual_html_id_count'] for z in figs]},ensure_ascii=False))
