"""Run separate counterexamples without adding them to the public matrix."""

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

import measure


USE_ROWS = [('isolation',8),('independent',38),('copied',68),('param',98),('cascade',128)]
HISTORY_EDGES = [('a','b'),('c','d'),('b','c'),('a','d'),('a','c')]


def slots():
    main=[{'id':id,'case':id[0],'patch':f'patches/{id}.diff'} for id in
          ('T-args-B','T-local-positive','S-marker-B-shorthand','D-chain-B')]
    main.append({'id':'T-revert','case':'T','patch':'patches/T-one-A.diff','reverse_patch':True})
    for id,patch in [('S-use-base',None),('S-use-edited','patches/S-use-controls.diff')]:
        main.append({'id':id,'case':'S','synthetic_use':True,'source':'evidence/control-inputs/use.svg','patch':patch})
    history={'old':'#000000','new':'#ff0000',
             'occurrences':[{'id':f'{a}->{b}','endpoints':[a,b]} for a,b in HISTORY_EDGES]}
    for id in ('D-history-base','D-history-default','D-history-reassign','D-scope-A'):
        main.append({'id':id,'case':'D','source':'evidence/control-inputs/history.gv','observation_case':history,
                     'patch':None if id=='D-history-base' else f'patches/{id}.diff'})
    return main


def observe_use(path,out,browser_path):
    assets={'/use.svg':('image/svg+xml',path)}
    with sync_playwright() as pw:
        with measure.browser_instance(pw,browser_path) as browser:
            context,page,requested,errors=measure.open_page(browser,assets,'/use.svg',{'width':400,'height':260})
            page.locator('svg').screenshot(path=out/'screen.png')
            svg=page.locator('svg').evaluate('(svg) => new XMLSerializer().serializeToString(svg)')
            (out/'rendered.svg').write_text(svg+'\n',encoding='utf-8')
            values=page.evaluate('''() => [...document.querySelectorAll('svg > :is(use,rect)')].map(e => ({
               id:e.id, href:e.getAttribute('href'), css_fill:getComputedStyle(e).fill,
               variable:getComputedStyle(e).getPropertyValue('--ink'),
               x:e.x.baseVal.value, y:e.y.baseVal.value}))''')
            version=browser.version
            context.close()
    pixels=np.asarray(Image.open(out/'screen.png').convert('RGB'))
    for item in values:
        x,y=int(item['x'])+10,int(item['y'])+10
        item['screen_rgb']='#{:02x}{:02x}{:02x}'.format(*pixels[y,x])
        item['sample_xy']=[x,y]
    return {'occurrences':values,'browser_version':version,'requested_paths':requested,'page_errors':errors}
