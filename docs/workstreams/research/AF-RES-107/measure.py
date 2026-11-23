"""Read vectors, styles and raster evidence for the three fixed originals."""

from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
import json
import math
import re

import fitz
import numpy as np
from PIL import Image, ImageColor
from playwright.sync_api import sync_playwright


NS = {'s': 'http://www.w3.org/2000/svg'}


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def signature(value):
    data = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return sha256(data.encode()).hexdigest()


def rgb(value):
    if value is None:
        return None
    parts = ImageColor.getrgb(value) if isinstance(value, str) else [round(255*v) for v in value]
    return '#'+''.join(f'{v:02x}' for v in parts[:3])


def serial(value):
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (fitz.Point, fitz.Rect, fitz.Quad, list, tuple)):
        return [serial(v) for v in value]
    if isinstance(value, float):
        return round(value, 4)
    return value


def palette(pixels, color, slop=0):
    target = np.array(ImageColor.getrgb(color))
    return np.all(np.abs(pixels.astype(int) - target) <= slop, axis=2)


def color_count(pixels, case, slop=0):
    return {v: int(palette(pixels, v, slop).sum()) for v in (case['old'], case['new'])}


def pdf(path, out, case):
    figures = []
    geometry = []
    preview_ids = {case['single'], case['comparison']}
    with fitz.open(path) as doc:
        for page in doc:
            expected = [e for e in case['occurrences'] if e['page'] == page.number+1]
            drawings = {v['seqno']: v for v in page.get_drawings()}
            pix = None
            for e in expected:
                shaft = drawings.get(e['shaft_seq'])
                head = drawings.get(e['head_seq'])
                if not shaft or not head or len(shaft['items']) != 3:
                    raise ValueError(f"{e['id']}: expected three shaft segments and next arrow")
                if not all(segment[0] == 'l' for segment in shaft['items']):
                    raise ValueError(f"{e['id']}: shaft segment type changed")
                vertices = [shaft['items'][0][1], *(item[2] for item in shaft['items'])]
                points = [p for item in head['items'] for p in item[1:] if isinstance(p, fitz.Point)]
                expected_tip = fitz.Point(*e['arrow_tip'])
                tip = min(points, key=lambda point: point.distance_to(expected_tip))
                delta = max(abs(a-b) for point, prior in zip(vertices+[tip], e['projected_vertices']+[e['arrow_tip']]) for a,b in zip(point, prior))
                figure = {'id':e['id'],'page':e['page'],'seq':[e['shaft_seq'],e['head_seq']],
                          'vertices':serial(vertices),'tip':serial(tip), 'prior_delta_pt':round(delta,5),
                          'shaft':rgb(shaft.pop('color',None)), 'tip_fill':rgb(head.pop('fill',None)),
                          'shaft_width':shaft['width'],'head_segments':serial(head['items'])}
                figure['color'] = figure['shaft'] if figure['shaft']==figure['tip_fill'] else None
                if e['id'] in preview_ids:
                    if pix is None:
                        pix = page.get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False)
                        pix.save(out/f'page-{e["page"]:02}.png')
                    rect = (shaft['rect'] | head['rect']) * fitz.Matrix(1.5,1.5)
                    crop = (max(0,math.floor(rect.x0)-2), max(0,math.floor(rect.y0)-2),
                            min(pix.width,math.ceil(rect.x1)+2), min(pix.height,math.ceil(rect.y1)+2))
                    screen = Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
                    figure['pixel_counts']=color_count(np.asarray(screen.crop(crop)),case)
                    figure['pixel_box']=crop
                figures.append(figure)
            geometry.append({'page':page.number+1,'frame':serial(page.rect),
                             'paths':signature(serial(drawings)), 'text':signature(serial(page.get_text('rawdict'))),
                             'text_stream':page.get_text(),
                             'fonts':[list(v[1:5]) for v in page.get_fonts()]})
        return {'occurrences':figures,'geometry':geometry,'geometry_sha256':signature(geometry),
                'page_count':len(doc), 'metadata':doc.metadata, 'mupdf_pdf_id':doc.xref_get_key(-1,'ID')[1]}


def open_page(browser, assets, entry, viewport):
    context=browser.new_context(viewport=viewport, device_scale_factor=1, offline=True,
                                service_workers='block', color_scheme='light', locale='en-US')
    requested=[]
    def fulfill(route):
        path=urlsplit(route.request.url).path
        requested.append(path)
        item=assets.get(path)
        if item is None:
            route.abort()
        else:
            mime, file=item
            route.fulfill(body=Path(file).read_bytes(), content_type=mime)
    context.route('**/*',fulfill)
    page=context.new_page()
    page.set_default_timeout(10000)
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://af-res-107.invalid'+entry, wait_until='load')
    return context,page,requested,errors


def browser_instance(playwright, browser_path):
    return playwright.chromium.launch(executable_path=browser_path, headless=True,
                                      args=['--force-color-profile=srgb','--disable-dev-shm-usage'])


def marker(path,out,case,support,browser_path):
    assets={'/input.html':('text/html; charset=utf-8',path)}
    for name in case['support']:
        assets['/resources/'+name]=('application/javascript; charset=utf-8',support/name)
    with sync_playwright() as pw:
        with browser_instance(pw,browser_path) as browser:
            context,page,requested,errors=open_page(browser,assets,'/input.html',{'width':640,'height':360})
            # testharnessreport loads on the same origin. The full WPT runner is not needed to read the in-page assertions.
            harness=page.evaluate('''() => new Promise((resolve, reject) => {
              setTimeout(() => reject(new Error('testharness completion timeout')), 8000);
              add_completion_callback((tests, status) => resolve({status: status.status,
                 message:status.message, tests:tests.map(t => ({name:t.name,status:t.status,message:t.message}))}));
            })''')
            observed=page.evaluate('''seconds => {
              const root=document.querySelector('svg');
              const host=root.querySelector('#path');
              root.pauseAnimations(); root.setCurrentTime(seconds);
              const hostStyle=getComputedStyle(host);
              const markers=['marker-start','marker-end'].map((attr,i) => {
                const url=hostStyle.getPropertyValue(attr);
                const key=url.match(/#([^"')]+)/)?.[1];
                const definition=document.getElementById(key);
                const triangle=definition.querySelector('path');
                const point=host.getPointAtLength(i===0?0:host.getTotalLength()).matrixTransform(host.getCTM());
                const attributes=Object.fromEntries(['viewBox','markerUnits','markerWidth','markerHeight','refX','refY'].map(k=>[k,definition.getAttribute(k)]));
                return {id:i===0?'m-start':'m-end', attr, url, definition:key, xy:[point.x,point.y],
                  angle:definition.orientAngle.animVal.value, shape:triangle.getAttribute('d'), attributes,
                  fill:getComputedStyle(triangle).getPropertyValue('fill')};
              });
              return {markers, title:document.title, seconds:root.getCurrentTime(),
                host:{d:host.getAttribute('d'),transform:host.getAttribute('transform'),
                  fill:hostStyle.fill, stroke:hostStyle.stroke, strokeWidth:hostStyle.strokeWidth,
                  drawings:[...root.children].map(node=>node.localName)}};
            }''',case['sample_seconds'])
            page.locator('svg').screenshot(path=out/'screen.png')
            (out/'rendered.svg').write_text(page.locator('svg').evaluate('(svg) => new XMLSerializer().serializeToString(svg)')+'\n',encoding='utf-8')
            version=browser.version
            context.close()
    pixels=np.asarray(Image.open(out/'screen.png').convert('RGB'))
    for e,piece in zip(case['occurrences'],observed['markers']):
        piece['color']=rgb(piece.pop('fill'))
        x,y=e['expected_svg_xy']
        left,top,right,bottom=max(0,x-15),max(0,y-15),x+16,y+16
        snippet=pixels[top:bottom,left:right]
        piece['pixel_counts']=color_count(snippet,case,2)
        px,py=e['pixel_inner_xy']
        piece['inner_pixel']='#{:02x}{:02x}{:02x}'.format(*pixels[py,px])
        piece['strong_mask_sha256']=sha256((palette(snippet,case['old'],2)|palette(snippet,case['new'],2)).tobytes()).hexdigest()
        piece['pixel_box']=[left,top,right,bottom]
    normalized=pixels.copy()
    dominant=(normalized[:,:,0]>normalized[:,:,2])
    normalized[dominant]=normalized[dominant][:,[2,1,0]]
    geometry={k:observed[k] for k in ('title','seconds','host')}
    geometry['size']=list(pixels.shape[:2][::-1])
    geometry['markers']=[{k:v for k,v in f.items() if k in {'id','attr','xy','angle','shape','attributes','strong_mask_sha256'}} for f in observed['markers']]
    return {'occurrences':observed['markers'],'harness':harness,'geometry':geometry,
            'geometry_sha256':signature(geometry),'raster_color_normalized_sha256':sha256(normalized.tobytes()).hexdigest(),
            'requested_paths':requested,'page_errors':errors,'browser_version':version}


def xml_shape(element, strip_edge_paint=False):
    attrs=dict(element.attrib)
    tag=element.tag.split('}')[-1]
    if strip_edge_paint and tag in ('path','polygon','polyline','ellipse'):
        attrs.pop('stroke',None)
        if attrs.get('fill') not in (None,'none'):
            attrs.pop('fill')
    return [tag,attrs,element.text.strip() if element.text else '',[xml_shape(child,strip_edge_paint) for child in element]]


def svg_graph(path,out,case,browser_path):
    root=ET.parse(path).getroot()
    graph=root.find('s:g',NS)
    edge_map={frozenset(e['endpoints']):e['id'] for e in case['occurrences']}
    elements=[]
    structure=[]
    edge_order=[]
    nodes=[]
    for group in graph.findall('s:g',NS):
        kind=group.attrib.get('class')
        structure.append(xml_shape(group,kind=='edge'))
        title=group.findtext('s:title',namespaces=NS)
        labels=[node.text for node in group.findall('s:text',NS)]
        if kind=='node':
            nodes.append({'title':title,'labels':labels})
        if kind=='edge':
            title_parts=re.split(r'--|->',title)
            key=edge_map.get(frozenset(title_parts), title)
            edges=group.findall('s:path',NS)
            head=group.findall('s:polygon',NS)+group.findall('s:ellipse',NS)+group.findall('s:polyline',NS)
            elements.append({'id':key,'title':title,'svg_id':group.attrib['id'],'paths':[e.attrib['d'] for e in edges],
                             'color':rgb(edges[0].attrib['stroke']),'head_shapes':[serial(e.attrib) for e in head],
                             'labels':labels})
            edge_order.append(key)
    geometry={'view':root.attrib,'graph':graph.attrib,'structure':structure,'background':xml_shape(graph.find('s:polygon',NS)),
              'edge_order':edge_order,'node_labels':nodes}
    assets={'/output.svg':('image/svg+xml',path)}
    with sync_playwright() as pw:
        with browser_instance(pw,browser_path) as browser:
            context,page,requested,errors=open_page(browser,assets,'/output.svg',{'width':1400,'height':1450})
            measurements=page.evaluate('''() => {
              const root=document.documentElement;
              const rect=root.getBoundingClientRect();
              return Object.fromEntries([...root.querySelectorAll('g.edge')].map(group => {
                const path=group.querySelector('path'); const len=path.getTotalLength();
                const samples=[.30,.50,.70].map(f => {
                  const p=path.getPointAtLength(f*len).matrixTransform(path.getScreenCTM());
                  return [p.x-rect.left,p.y-rect.top];
                });
                return [group.id,{samples,stroke:getComputedStyle(path).stroke}];
              }));
            }''')
            page.locator('svg').screenshot(path=out/'screen.png')
            version=browser.version
            context.close()
    pixels=np.asarray(Image.open(out/'screen.png').convert('RGB'))
    for element in elements:
        data=measurements[element['svg_id']]
        element['css_color']=rgb(data['stroke'])
        element['sample_xy']=serial(data['samples'])
        element['pixel_neighborhood_counts'], element['aa_neighborhood_counts']=dot_samples(pixels,element['sample_xy'],case)
    return {'occurrences':elements,'geometry_sha256':signature(geometry),'geometry':geometry,
            'raster_tone_normalized_sha256':sha256(pixels.min(axis=2).tobytes()).hexdigest(),
            'screen_size_px':list(pixels.shape[:2][::-1]),'requested_paths':requested,
            'page_errors':errors,'browser_version':version}


def dot_samples(pixels, points, case):
    """Count solid and antialiased stroke pixels near three visible path points."""
    exact=[]
    covered=[]
    for x,y in points:
        x,y=round(x),round(y)
        roi=pixels[max(0,y-2):y+3,max(0,x-2):x+3]
        exact.append(color_count(roi,case,2))
        r,g,b=np.moveaxis(roi.astype(int),-1,0)
        dark=roi.min(axis=2)<=200
        neutral=roi.max(axis=2).astype(int)-roi.min(axis=2)<=2
        red=(r-np.maximum(g,b)>=25)&(np.abs(g-b)<=2)
        covered.append({'#000000':int((neutral&dark).sum()),'#ff0000':int(red.sum())})
    return exact,covered
