"""Recalculate expected and actual affected sets from the saved AF-RES-107 evidence."""

import argparse
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image

import controls
import measure
from run import INPUTS, PROTOCOL, ROOT


FIELDS = ['run_id','phase','case','purpose','method','repeat','occurrence','role','expected','observed','changed',
          'exact_expected','coordinates','paint_or_arrow','pixel_probe','source_url','receipt']


def read(path):
    return json.loads(path.read_bytes())


def image(path):
    return np.asarray(Image.open(path).convert('RGB'))


def hexpixel(pixels, xy):
    x,y=xy
    return '#{:02x}{:02x}{:02x}'.format(*pixels[y,x])


def verify_files(folder, receipt):
    assert set(receipt['files'])=={p.name for p in folder.iterdir() if p.name!='receipt.json'}, folder
    for name, file in receipt['files'].items():
        assert (folder/name).stat().st_size==file['bytes'] and measure.digest(folder/name)==file['sha256'], (folder,name)
    if receipt.get('patch'):
        assert measure.digest(ROOT/receipt['patch'])==receipt['patch_sha256'], (folder,'patch SHA')
    source=ROOT/receipt['source']
    assert measure.digest(source)==receipt['original_sha256'], (folder,'source SHA')
    infile=folder/('input'+source.suffix)
    if infile.is_file():
        assert measure.digest(infile)==receipt['edited_input_sha256'], (folder,'edited SHA')


def svg_marker_values(folder, observed, case):
    svg=ET.parse(folder/'rendered.svg').getroot()
    pieces=observed['occurrences']
    screen=image(folder/'screen.png')
    old,new=case['old'],case['new']
    palette_normalized=screen.copy()
    red=palette_normalized[:,:,0]>palette_normalized[:,:,2]
    palette_normalized[red]=palette_normalized[red][:,[2,1,0]]
    for expected,piece in zip(case['occurrences'],pieces,strict=True):
        definition=svg.find(f".//s:marker[@id='{piece['definition']}']",measure.NS)
        triangle=definition.find('s:path',measure.NS)
        pixel=hexpixel(screen,expected['pixel_inner_xy'])
        x0,y0,x1,y1=piece['pixel_box']
        colors=measure.color_count(screen[y0:y1,x0:x1],case,2)
        assert expected['id']==piece['id'] and colors==piece['pixel_counts'], (folder,piece['id'])
        assert piece['color']==measure.rgb(triangle.attrib['fill'])==piece['inner_pixel']==pixel, (folder,piece['id'])
        assert all(abs(x-y)<=0.02 for x,y in zip(expected['expected_svg_xy'],piece['xy'],strict=True)), (folder,piece['id'])
        assert abs(piece['angle']-case['expected_angle_deg'])<=1.0 and piece['color'] in (old,new), (folder,piece['id'])
        assert colors[piece['color']]>=8 and colors[new if piece['color']==old else old]==0, (folder,piece['id'])
    assert observed['harness']['status']==0 and [v['status'] for v in observed['harness']['tests']]==[0], folder
    assert not observed['page_errors'], folder
    return {p['id']:p['color'] for p in pieces},palette_normalized


def graph_values(folder, observed, case):
    svg=ET.parse(folder/'output.svg').getroot()
    graph=svg.find('s:g',measure.NS)
    groups={g.attrib['id']:g for g in graph.findall('s:g',measure.NS) if g.attrib.get('class')=='edge'}
    structure=[measure.xml_shape(g,g.attrib.get('class')=='edge') for g in graph.findall('s:g',measure.NS)]
    assert structure==observed['geometry']['structure'], (folder,'XML geometry')
    screen=image(folder/'screen.png')
    assert len(groups)==len(observed['occurrences']), folder
    dot=read(folder/'output.dot.json')
    nodes={v['_gvid']:v['name'] for v in dot['objects'] if 'name' in v and 'pos' in v}
    dot_edges={frozenset((nodes[e['tail']],nodes[e['head']])):e for e in dot['edges']}
    by_id={v['id']:v for v in case['occurrences']}
    for piece in observed['occurrences']:
        group=groups[piece['svg_id']]
        assert group.findtext('s:title',namespaces=measure.NS)==piece['title'], (folder,piece['id'])
        edge=group.find('s:path',measure.NS)
        read_color=measure.rgb(edge.attrib['stroke'])
        record=dot_edges[frozenset(by_id[piece['id']]['endpoints'])]
        assert read_color==piece['color']==piece['css_color']==measure.rgb(record['color']), (folder,piece['id'])
        if 'arrowheads' in by_id[piece['id']]:
            source_occurrence=by_id[piece['id']]
            assert len(piece['head_shapes'])==source_occurrence['arrowheads'], (folder,piece['id'])
            expected_len='2.5' if source_occurrence['chain_index'] is None else ''
            assert record.get('len','')==expected_len, (folder,piece['id'],'len')
        exact,covered=measure.dot_samples(screen,piece['sample_xy'],case)
        assert exact==piece['pixel_neighborhood_counts'] and covered==piece['aa_neighborhood_counts'], (folder,piece['id'])
        opposite=case['new'] if read_color==case['old'] else case['old']
        assert sum(sample[read_color]>0 for sample in covered)>=2, (folder,piece['id'])
        # In separate controls, changed strokes can cross an unchanged sample.
        if folder.parent.name in ('baseline','matrix') and 'expected_nodes' in case:
            assert all(sample[opposite]==0 for sample in covered), (folder,piece['id'])
    assert len(dot_edges)==len(by_id), (folder,'canonical edges')
    assert not observed['page_errors'], folder
    return {p['id']:p['color'] for p in observed['occurrences']},screen


def observe_again(folder, receipt, case):
    observed=read(folder/'observed.json')
    notes={}
    color_values={}
    screen=None
    if receipt['case']=='T':
        with TemporaryDirectory(prefix='afres107-recheck-') as temp:
            pdf=measure.pdf(folder/'input.pdf',Path(temp),case)
            assert json.loads(json.dumps(pdf))==observed, (folder,'re-extracted PDF')
            for p in Path(temp).glob('page-*.png'):
                assert measure.digest(p)==measure.digest(folder/p.name), p.name
        assert observed['page_count']==case['expected_pages'], folder
        for piece in observed['occurrences']:
            assert piece['prior_delta_pt']<=PROTOCOL['criteria']['T']['coords_abs_pt'], (folder,piece['id'])
            assert piece['color'] in (case['old'],case['new']), (folder,piece['id'],'shaft and tip')
            if 'pixel_counts' in piece:
                assert piece['pixel_counts'][piece['color']]>0, (folder,piece['id'],'screen')
            color_values[piece['id']]=piece['color']
        notes={'creation':observed['metadata']['creationDate'],'modified':observed['metadata']['modDate'],
               'pdf_id':observed['mupdf_pdf_id'],'max_prior_delta_pt':max(e['prior_delta_pt'] for e in observed['occurrences'])}
    elif receipt.get('synthetic_use'):
        screen=image(folder/'screen.png')
        for piece in observed['occurrences']:
            color=hexpixel(screen,piece['sample_xy'])
            assert color==piece['screen_rgb'], (folder,piece['id'])
            color_values[piece['id']]=color
        assert not observed['page_errors'], folder
    elif receipt['case']=='S':
        color_values,screen=svg_marker_values(folder,observed,case)
        notes={'in_page_wpt_tests':observed['harness']['tests'],'angle_at_2s':{
            p['id']:p['angle'] for p in observed['occurrences']}}
    else:
        color_values,screen=graph_values(folder,observed,case)
    return observed,color_values,screen,notes


def raster_difference(case, screen, base, run_id):
    if case=='S':
        return {'color_normalized_screen_equal':bool(np.array_equal(screen,base))}
    if case=='D':
        assert screen.shape==base.shape, (run_id,'screen size')
        old=base.astype(int)
        actual=screen.astype(int)
        diff=np.any(actual!=old,axis=2)
        red=actual[:,:,0]>np.maximum(actual[:,:,1],actual[:,:,2])
        tone=np.abs(actual.min(axis=2)-old.min(axis=2))
        return {'changed_pixels':int(diff.sum()),'changed_without_red_pixels':int((diff&~red).sum()),
                'max_tone_channel_delta':int(tone.max()),'tone_delta_over_2_pixels':int((tone>2).sum())}
    return {}


def element_row(slot, phase, occurrence, color, wanted, old, original, folder):
    case=slot['case']
    rect=occurrence.get('vertices',occurrence.get('xy',occurrence.get('sample_xy')))
    if case=='T':
        pos={'page':occurrence['page'],'seq':occurrence['seq'],'vertices':rect,'tip':occurrence['tip']}
        shape={'shaft':occurrence['shaft'],'tip_fill':occurrence['tip_fill']}
    elif case=='S':
        pos={'xy':rect,'angle':occurrence.get('angle')}
        shape={k:occurrence[k] for k in ('definition','url','href','css_fill','variable') if k in occurrence}
    else:
        pos={'title':occurrence['title'],'svg_id':occurrence['svg_id'],'d':occurrence['paths'],'screen_xy':rect}
        shape={'labels':occurrence['labels'],'head_shapes':occurrence['head_shapes'],'css_color':occurrence['css_color']}
    return {'run_id':slot['id'],'phase':phase,'case':case,'purpose':slot.get('purpose'),
            'method':slot.get('method'),'repeat':slot.get('repeat'),'occurrence':occurrence['id'],
            'role':'target' if wanted!=old else 'preserve','expected':wanted,'observed':color,
            'changed':color!=old,'exact_expected':color==wanted,'coordinates':json.dumps(pos,ensure_ascii=False),
            'paint_or_arrow':json.dumps(shape,ensure_ascii=False),
            'pixel_probe':json.dumps(occurrence.get('pixel_counts',occurrence.get('aa_neighborhood_counts',occurrence.get('screen_rgb')))),
            'source_url':original['url'],'receipt':folder+'/receipt.json'}


def control_expected(occ):
    return {'T-args-B':['g12','g21'],'T-local-positive':['g12'],'T-revert':[],
            'S-marker-B-shorthand':['m-start','m-end'],'S-use-base':[],
            'S-use-edited':['isolation-1','independent-1','copied-1','param-1'],
            'D-chain-B':[f'e{i:02}' for i in range(1,15)],'D-history-base':[],
            'D-history-default':['b->c'],'D-history-reassign':['a->b'],'D-scope-A':['a->d']}[occ]


def collect(evidence):
    rows=[]
    elements=[]
    results={}
    reference={}
    for phase,slots in [('baseline',PROTOCOL['baseline_slots']),('matrix',PROTOCOL['main_slots']),('controls',controls.slots())]:
        assert {p.name for p in (evidence/phase).iterdir() if p.is_dir()}=={s['id'] for s in slots}, phase
        for slot in slots:
            case_id=slot['case']
            original=INPUTS['cases'][case_id]
            case=slot.get('observation_case',original)
            path=f'evidence/{phase}/{slot["id"]}'
            folder=evidence/phase/slot['id']
            receipt=read(folder/'receipt.json')
            verify_files(folder,receipt)
            assert receipt['id']==slot['id'] and receipt['case']==case_id, folder
            row={'phase':phase,'receipt':path+'/receipt.json',**receipt}
            if receipt['exit']:
                row['verdict']='output_missing'
                rows.append(row)
                continue
            observed,actual,screen,notes=observe_again(folder,receipt,case)
            if 'source' not in slot:
                ids=[e['id'] for e in original['occurrences']]
                assert set(actual)==set(ids) and len(actual)==len(ids), folder
            else:
                ids=list(actual)
            if phase=='baseline':
                target=[]
                if slot['repeat']==1:
                    reference[case_id]=(observed,screen)
                assert receipt['original_sha256']==receipt['edited_input_sha256'], folder
            elif phase=='matrix':
                target=ids if slot['purpose']=='all' else [case['single']]
            else:
                target=control_expected(slot['id'])
                if slot['id']=='T-revert':
                    assert receipt['original_sha256']==receipt['edited_input_sha256'], folder
            changed=[id for id in ids if actual[id]!=case['old']]
            wrong=[id for id in changed if id not in target]
            hits=[id for id in target if actual[id]==case['new']]
            structure=None
            differences={}
            if 'source' not in slot:
                base_observed,base_image=reference[case_id]
                structure=observed['geometry_sha256']==base_observed['geometry_sha256']
                differences=raster_difference(case_id,screen,base_image,slot['id'])
            elif slot['id'].startswith('D-'):
                if slot['id']=='D-history-base':
                    reference['D-history']=(observed,screen)
                base_observed,base_image=reference['D-history']
                structure=observed['geometry_sha256']==base_observed['geometry_sha256']
                differences=raster_difference(case_id,screen,base_image,slot['id'])
            raster_ok=(differences.get('color_normalized_screen_equal',True) and
                       differences.get('tone_delta_over_2_pixels',0)==0 and differences.get('changed_without_red_pixels',0)==0)
            if slot['id']=='S-marker-B-shorthand':
                mid=hexpixel(image(folder/'screen.png'),(50,15))
                differences['additional_marker_mid_at_50_15']=mid
                assert mid=='#ff0000' and not raster_ok, folder
            verdict=('pass' if len(hits)==len(target) and not wrong and structure is not False and raster_ok else 'purpose_fail') if phase!='controls' else 'observed'
            if phase=='controls':
                assert hits==target and not wrong, (folder,'control set')
            seen={e['id']:e for e in observed['occurrences']}
            for id in ids:
                wanted=case['new'] if id in target else case['old']
                elements.append(element_row(slot,phase,seen[id],actual[id],wanted,case['old'],original,path))
            files=receipt['files']
            screens=[files[n]['sha256'] for n in sorted(files) if n=='screen.png' or n.startswith('page-')]
            semantic={'geometry':observed.get('geometry_sha256'),'colors':actual,'screens':screens,
                      'in_page_wpt_tests':notes.get('in_page_wpt_tests')}
            result={
                'targets':target,'hits':hits,'target_n':len(target),'wrong':wrong,'sibling_n':len(ids)-len(target),
                'changed':changed,'occurrence_count':len(ids),'geometry_preserved':structure,'raster':differences,
                'notes':notes,'semantic_sha256':measure.signature(semantic),'verdict':verdict,
                'raw_sha256':files[receipt['result']]['sha256'],'observation':path+'/observed.json',
                'output':path+'/'+receipt['result'],'source_url':original['url']}
            results[slot['id']]=result
            rows.append({**row,**result})
    return rows,elements,results


def comparisons(results):
    repeats=[]
    for case in 'TSD':
        labels=['base']+[f'{purpose}-{method}' for purpose in ('one','all') for method in 'AB']
        for label in labels:
            a,b=(results.get(f'{case}-{label}-{n}') for n in (1,2))
            repeats.append({'pair':f'{case}-{label}','both_outputs':bool(a and b),
                            'semantic_same':None if not a or not b else a['semantic_sha256']==b['semantic_sha256'],
                            'raw_same':None if not a or not b else a['raw_sha256']==b['raw_sha256'],
                            'unavailable_reason':None if a and b else 'one or both outputs unavailable',
                            'creation_dates':[r['notes'].get('creation') for r in (a,b) if r]})
    methods=[]
    for case in 'TSD':
        for purpose in ('one','all'):
            a,b=(results.get(f'{case}-{purpose}-{method}-1') for method in 'AB')
            methods.append({'case':case,'purpose':purpose,'both_outputs':bool(a and b),
                            'semantic_same':None if not a or not b else a['semantic_sha256']==b['semantic_sha256'],
                            'raw_same':None if not a or not b else a['raw_sha256']==b['raw_sha256'],
                            'A_only':[] if not a or not b else [id for id in a['changed'] if id not in b['changed']],
                            'B_only':[] if not a or not b else [id for id in b['changed'] if id not in a['changed']]})
    return {'repetition':repeats,'purpose_method_comparison':methods,'runs':results}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,default=ROOT/'evidence')
    cli.add_argument('--write',action='store_true',help='write result ledgers for the committed evidence')
    args=cli.parse_args()
    runs,elements,results=collect(args.evidence)
    verification=comparisons(results)
    frozen=args.evidence.resolve()==(ROOT/'evidence').resolve()
    if args.write:
        if not frozen:
            cli.error('--write is reserved for the committed evidence directory')
        (ROOT/'runs.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in runs),encoding='utf-8')
        with (ROOT/'elements.csv').open('w',encoding='utf-8',newline='') as file:
            output=csv.DictWriter(file,FIELDS,lineterminator='\n')
            output.writeheader()
            output.writerows(elements)
        (args.evidence/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    elif frozen:
        assert verification==read(args.evidence/'verification.json'), 'verification ledger changed'
        assert runs==[json.loads(line) for line in (ROOT/'runs.jsonl').read_text().splitlines()], 'run ledger changed'
        with (ROOT/'elements.csv').open(encoding='utf-8',newline='') as file:
            assert list(csv.DictReader(file))==[{k:'' if v is None else str(v) for k,v in row.items()} for row in elements], 'element ledger changed'
    primary=[r for r in runs if r['phase']=='matrix']
    print(json.dumps({'baseline_runs':sum(r['phase']=='baseline' for r in runs),'matrix_runs':len(primary),
        'controls_runs':sum(r['phase']=='controls' for r in runs),'observed_element_rows':len(elements),
        'outcomes':{key:sum(r['verdict']==key for r in primary) for key in ('pass','purpose_fail','output_missing')},
        'paired_semantic':sum(r['semantic_same'] is True for r in verification['repetition']),
        'paired_with_output':sum(r['both_outputs'] for r in verification['repetition'])},ensure_ascii=False))
    return int(any(r['exit'] for r in runs))


if __name__=='__main__':
    raise SystemExit(main())
