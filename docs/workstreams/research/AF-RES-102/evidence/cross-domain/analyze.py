"""Reproduce the Q7 static archive/reference audit; no package code execution."""
from __future__ import annotations
import ast
from collections import Counter
import hashlib
import json
import re
import zipfile
import io
from pathlib import Path
from collect import ROOT, CACHE, RECEIPTS, get, inspect_epub, inspect_wheel, sha, now

PREFIX='evidence/cross-domain/'
EPUB='https://github.com/IDPF/epub3-samples/releases/download/20230704/trees.epub'
EPUB_SHA='46d7e07e1b39b2d0a0245ececaf896edcd9de4b2'
PACKAGING_SHA='5b31c28208dbcef1b089fdf9018910e611d2600f'


def receipt(key):
    return json.loads((RECEIPTS/(key+'.json')).read_text())


def source(id,key,category,publisher,lineage,version,location,observation,supported,refuted,limitations,countable=True,duplicate_reason='',fixed=None,cases=None):
    r=receipt(key)
    return {'source_id':id,'questions':['Q7'],'cases':cases or [],'original_url':r['requested_url'],
            'fixed_url':fixed or r['requested_url'],'accessed_utc':r['finished_utc'],
            'publisher':publisher,'lineage':lineage,'category':category,'version':version,'location':location,
            'sha256':r.get('sha256'),'observation':observation,'claims_supported':supported,
            'claims_refuted':refuted,'limitations':limitations,'countable':countable,
            'duplicate_reason':duplicate_reason,'receipt':PREFIX+'receipts/'+key+'.json'}


def main():
    epub_bytes,epub_rec=get('trees.epub',EPUB)
    epub=inspect_epub(epub_bytes)
    (ROOT/'trees-audit.json').write_text(json.dumps(epub,ensure_ascii=False,indent=2)+'\n')
    z=zipfile.ZipFile(io.BytesIO(epub_bytes));r=epub['renditions'][0]
    text_paths=[n for n in z.namelist() if n.endswith(('.xhtml','.css','.js'))]
    literal_cover_hits={n:[i for i,l in enumerate(z.read(n).decode().splitlines(),1) if 'cover.jpg' in l] for n in text_paths}
    body_ref_counts={}
    for x in r['xhtml']:
        t=z.read(x['path']).decode()
        body_ref_counts[x['path']]={
            'img':len(re.findall(r'<img\b',t)), 'picture':len(re.findall(r'<picture\b',t)),
            'srcset':len(re.findall(r'\bsrcset\s*=',t)), 'svg_image':len(re.findall(r'<(?:\w+:)?image\b',t)),
            'object':len(re.findall(r'<object\b',t)), 'data_url':t.count('data:'),
            'canvas':len(re.findall(r'<canvas\b',t)), 'script_src':len(re.findall(r'<script\b[^>]*\bsrc=',t)),
            'base_element':len(re.findall(r'<base\b',t)), 'xml_base':t.count('xml:base')}
    epub_source_comparison=[]
    for member,key in [('EPUB/titlepage.xhtml','trees-titlepage.xhtml'),('EPUB/package.opf','trees-package.opf')]:
        raw,rec=get(key,f'https://raw.githubusercontent.com/IDPF/epub3-samples/{EPUB_SHA}/30/trees/{member}')
        packaged=z.read(member)
        epub_source_comparison.append({'member':member,'source_url':rec['requested_url'],'source_sha256':sha(raw),
                                      'package_member_sha256':sha(packaged),'bytes_equal':raw==packaged,
                                      'equal_after_CRLF_to_LF':raw.replace(b'\r\n',b'\n')==packaged.replace(b'\r\n',b'\n'),
                                      'source_CRLF_count':raw.count(b'\r\n'),'package_CRLF_count':packaged.count(b'\r\n')})
    release_bytes,_=get('build-1.2.2.post1.json','https://pypi.org/pypi/build/1.2.2.post1/json')
    release=json.loads(release_bytes);file=next(x for x in release['urls'] if x['filename'].endswith('.whl'))
    wheel_bytes,wheel_rec=get(file['filename'],file['url']);wheel=inspect_wheel(wheel_bytes)
    wheel.update({'pypi_declared_sha256':file['digests']['sha256'],'pypi_digest_matches':sha(wheel_bytes)==file['digests']['sha256'],
                  'download_url':file['url'],'pypi_uploaded_utc':file['upload_time_iso_8601']})
    (ROOT/'wheel-audit.json').write_text(json.dumps(wheel,ensure_ascii=False,indent=2)+'\n')
    wz=zipfile.ZipFile(io.BytesIO(wheel_bytes));code=wz.read('build/__main__.py').decode()
    tree=ast.parse(code);entry=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='entrypoint')
    wheel_detail={'entrypoint_function_lines':[entry.lineno,entry.end_lineno],
                  'entrypoint_function_source_summary':'entrypoint invokes main(sys.argv[1:]); AST parsed only',
                  'main_module_guard_lines':[448,449],
                  'console_script_count':sum(e['group']=='console_scripts' for e in wheel['declared_entrypoints']),
                  'declared_entrypoint_count':len(wheel['declared_entrypoints']),
                  'declared_entrypoint_unique_object_count':len({e['object_reference'] for e in wheel['declared_entrypoints']}),
                  'archive_has_pyproject_build_wrapper':any(n.endswith('/pyproject-build') or n=='pyproject-build' for n in wz.namelist()),
                  'record_present_non_entrypoint_example':'build-1.2.2.post1.dist-info/LICENSE',
                  'function_call_was_executed_by_audit':False,
                  'historical_runtime_execution':'미확인'}
    assertions={
        'epub_hash_fixed':sha(epub_bytes)=='4fbaa5713555ea104b2aed8fc6182700225416b0ab5369f0cb7293d486bb718f',
        'epub_manifest_all_local_members_exist':all(x['present'] for x in r['manifest']),
        'cover_manifest_present':any(x['id']=='cover' and x['properties']=='cover-image' and x['present'] for x in r['manifest']),
        'cover_no_literal_reference_in_3_xhtml_1_css_4_js':all(not v for v in literal_cover_hits.values()),
        'every_xhtml_has_one_canvas_and_four_script_refs':all(x['canvas']==1 and x['script_src']==4 for x in body_ref_counts.values()),
        'wheel_hash_matches_pypi':wheel['pypi_digest_matches'],
        'wheel_19_record_rows_18_valid_hashes':len(wheel['record_entries'])==19 and sum(x['digest_matches'] is True for x in wheel['record_entries'])==18,
        'wheel_all_nonempty_sizes_match':all(x['size_matches'] is not False for x in wheel['record_entries']),
        'wheel_record_no_unlisted_member':not wheel['zip_unlisted'],
        'wheel_entrypoint_module_and_function_exist':all(e['module_present'] for e in wheel['declared_entrypoints']) and entry.lineno==444}
    if not all(assertions.values()):raise AssertionError(assertions)
    audit={
        'task':'AF-RES-102','question':'Q7','role':'supplementary cross-domain cases, excluded from the 12-pair/24-position main sample',
        'created_utc':now(),'method':'Direct public HTTP bytes, ZIP/XML/INI/CSV parsing, full member digest checks; source code is read/AST-parsed, never imported or executed.',
        'epub':{'case_id':'CD-EPUB-TREES','package_url':EPUB,'release_tag':'20230704','source_tag_sha':EPUB_SHA,
                'package_receipt':PREFIX+'receipts/trees.epub.json','member_audit':PREFIX+'trees-audit.json',
                'container_full_path':'EPUB/package.opf','manifest_count':len(r['manifest']),'spine_count':len(r['spine']),
                'package_member_count':epub['member_count'],'chosen_section':'EPUB/titlepage.xhtml body#titlepage L28–41; canvas L29; script src L6–9',
                'cover':{'path':'EPUB/cover.jpg','mime_from_signature':'image/jpeg','bytes':len(z.read('EPUB/cover.jpg')),
                         'sha256':sha(z.read('EPUB/cover.jpg')),'dimensions_px':[400,393],
                         'visual_inspection':'Black stylized leafy tree silhouette on white; inspected locally with view_image, not an EPUB reader.',
                         'P_included':'YES','U_in_chosen_body':'NO','G_generated_for_release':'미확인',
                         'negative_scope':'No author-specified cover.jpg reference in three complete XHTML files, style.css, or four packaged JS files; metadata marks it as cover-image. This does not deny a reader bookshelf/cover preview use.',
                         'minimum_reversal':'An author-defined reference or dynamic path resolving to cover.jpg from the chosen body, or a scoped reader trace demonstrating such use.'},
                'actual_body_mechanism':{'canvas_count':1,'script_references':['script/jquery-1.3.2.js','script/SnakeCollection.js','script/Snake.js','script/tree.js'],
                                         'tree_js_reference':'EPUB/script/tree.js L10–23, L33–47 selects #canvas, gets 2D context, constructs Snake/SnakeCollection and schedules drawing',
                                         'drawing_primitive':'EPUB/script/Snake.js L39–50 uses arc/fill; no JPEG is substituted for the canvas',
                                         'static_reference_U':'YES','reader_rendering_or_JS_execution':'미확인'},
                'reference_form_counts':body_ref_counts,'literal_cover_hits':literal_cover_hits,
                'source_package_comparison':epub_source_comparison,
                'limitations':['No reader, JavaScript, EPUBCheck, or creation pipeline execution. The package declares EPUB 3.0; applying shared path/reference concepts is not a full EPUB 3.3 conformance certification.',
                               'Reader may use cover-image metadata outside the selected content body. Randomized canvas rendering is not byte-identical to the cover JPEG or necessarily repeatable.']},
        'wheel':{'case_id':'CD-WHEEL-BUILD','package_url':file['url'],'release_metadata_url':'https://pypi.org/pypi/build/1.2.2.post1/json',
                 'package_receipt':PREFIX+'receipts/'+file['filename']+'.json','member_audit':PREFIX+'wheel-audit.json',
                 'package_version':'1.2.2.post1','package_bytes':len(wheel_bytes),'package_sha256':sha(wheel_bytes),
                 'P_package_members':'YES','entrypoint_declaration_links_to_packaged_function':'YES','installation':'미확인','entrypoint_runtime_execution':'미확인','G_exact_release_build_generation':'미확인',
                 'details':wheel_detail,
                 'counterexample_scope':'All 19 members are listed in RECORD, but metadata advertises one console script and one pipx.run name pointing to one callable. LICENSE membership is not an entrypoint. No wrapper named pyproject-build is in this ZIP; metadata alone is not its installation or execution receipt.',
                 'minimum_reversal':'An actual environment-specific installation record plus invocation/log/exit result tied to this distribution hash, or a different wheel whose metadata no longer names the inspected function.'},
        'auxiliary_exploration':{'childrens-literature':'10 ZIP members, 7 manifest items, all 3 XHTML in spine; no non-spine XHTML found. Preserved as search evidence, excluded from source minimum and main sample.',
                                 'file':PREFIX+'childrens-literature-audit.json'},
        'corrections':[{'issue':'Initial generic fragment-only URL resolution joined the directory instead of retaining the document.',
                        'fix':'resolve now returns the source document when urlsplit(relative).path is empty. Childrens supplementary audit regenerated. No Trees cover/canvas or wheel conclusion changed.'}],
        'assertions':assertions,
        'not_performed':['No reader rendering or JS execution','No wheel installation, imported package, entrypoint run, build reconstruction, or historical build-job search in this Q7 subtask','No ggplot2/Matplotlib new body, image, or CI access'],
    }
    (ROOT/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    rows=[]
    rows.append(source('CD-E01','epub-33.html','epub_spec','W3C/IDPF','RULE-EPUB-CORE','3.3 REC 2026-01-13','§4.2.6.2–3 container; §5.2 URLs; §5.6 manifest; §5.7 spine',
       'Container full-path is relative to container root; manifest inventory and spine ordering are distinct relationships.',
       ['CD-EPUB-TREES path resolution and inventory-vs-reading order distinction'],['Manifest inclusion alone proves the exact body embeds a resource'],
       'Normative linkage rules, not an observation of a reader. This exact core Recommendation was already used in AF-RES-098; excluded conservatively from the new-material minimum.',False,'Inherited normative work from AF-RES-098; reread for this new sample',cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E02','epub-rs-33-20241017.html','epub_spec','W3C','RULE-EPUB-READING-SYSTEMS','3.3 REC 2024-10-17','§4 OCF processing; §6.4 Scripting',
       'Container inspection can be separate from reader rendering. Script support is contextual; unsupported scripting requires fallback handling.',
       ['Inspecting Trees ZIP and script references does not demonstrate a rendered canvas'],['All included scripted content must have been executed or rendered'],
       'No particular reader tested. The normative specification is a different work from the core authoring specification.',cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E03','trees.epub','epub_package','IDPF/epub3-samples; OPF contributor mgylling','PUB-EPUB-TREES','release 20230704, package EPUB 3.0','META-INF/container.xml → EPUB/package.opf → EPUB/titlepage.xhtml L6–9/L28–41; cover.jpg; script/tree.js',
       '75,717B ZIP; 12 members; manifest 9/spine 3. cover.jpg is included (32,681B, JPEG 400×393) but is not referenced by the selected body; its canvas references four scripts. Same tag titlepage source differs from ZIP only by 41 CRLF line endings.',
       ['P=YES with chosen-body JPEG U=NO; actual body uses canvas/scripts','Body/source equivalence can hold with different bytes'],['Included cover JPEG is necessarily the canvas picture','A source tag alone fixes package member byte identity'],
       'No reader/JS/EPUBCheck/build execution. Cover metadata could be used by a reader outside this body; G remains 미확인.',cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E04','epub-release.json','release_record','IDPF/epub3-samples','PUB-EPUB-20230704','20230704','asset trees.epub, 75,717B; published_at',
       'Official release lists the downloaded Trees asset and other samples.', ['Trees archive provenance'],[],
       'A release asset list does not establish payload generation. This release event was already in AF-RES-098.',False,'Same release event as prior Cole case; Trees payload counted separately',cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E05','epub-tag.json','release_record','IDPF/epub3-samples','PUB-EPUB-20230704','20230704','object.sha',
       'Release tag points at commit '+EPUB_SHA+'.',['Pinned source provenance'],[], 'A tag record does not prove how the ZIP was produced.',False,'Provenance for same release event',fixed='https://api.github.com/repos/IDPF/epub3-samples/git/commits/'+EPUB_SHA,cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E06','epub-tree.json','deployment_listing','IDPF/epub3-samples','PUB-EPUB-TREES',EPUB_SHA,'30/trees; truncated=false',
       'Complete tree includes the Trees source members, used to locate titlepage and OPF.', ['Pinned source file locations'],[],
       'Tree names do not establish final archive bytes or runtime display.',False,'Supporting inventory for the one package case',cases=['CD-EPUB-TREES']))
    for n,key,loc,obs in [('CD-E07','trees-titlepage.xhtml','body#titlepage L28–41','1,375B LF source and 1,416B CRLF package member are equal after CRLF→LF; source SHA differs from package SHA.'),
                         ('CD-E08','trees-package.opf','manifest L15–25; spine L26–30','2,080B OPF source exactly matches package member; cover-image declaration and three spine items are distinct.')]:
        rows.append(source(n,key,'example_source','IDPF/epub3-samples','PUB-EPUB-TREES',EPUB_SHA,loc,obs,['Archive/source linkage for Trees'],[],
                           'No build-run attribution. Counted as the same Trees work, not extra source material.',False,'Same package work/member already counted as CD-E03',cases=['CD-EPUB-TREES']))
    rows.append(source('CD-E09','childrens-literature.epub','epub_package','IDPF/epub3-samples','PUB-EPUB-CHILDRENS-LITERATURE','20230704','container/OPF/3 XHTML',
       'Exploratory archive: 10 members, manifest 7 and spine 3. All three XHTML are in spine; did not supply a non-spine-XHTML counterexample.',
       ['Negative search outcome retained'],['This explored package contains a non-spine XHTML'],
       'Only exploration, not the chosen Q7 package; no reader execution.',False,'Excluded by conservative Q7 selection; no source-minimum inflation',cases=['CD-EPUB-EXPLORATION']))
    rows.append(source('CD-W01','wheel-spec.rst','wheel_spec','PyPA','RULE-WHEEL-DISTRIBUTION',PACKAGING_SHA,'source/specifications/binary-distribution-format.rst L234–254',
       'Wheel .dist-info must include METADATA, WHEEL and RECORD; RECORD lists members and secure hashes, with its own row unhashed.',
       ['Member and digest validation scope for build wheel'],['RECORD is an execution log'],
       'Distribution rules do not establish historical installation/execution. HTML is a moving rendering of the same normative work.',cases=['CD-WHEEL-BUILD']))
    rows.append(source('CD-W02','entrypoints-spec.rst','wheel_spec','PyPA','RULE-ENTRY-POINTS',PACKAGING_SHA,'source/specifications/entry-points.rst L10–15, L82–90, L126–146',
       'entry_points.txt advertises group/name/object references; console scripts obtain wrappers at installation and call functions when invoked.',
       ['Declaration, installation and execution are separate observations'],['An entrypoint declaration proves the function already ran'],
       'No installation or invocation is performed in this study.',cases=['CD-WHEEL-BUILD']))
    rows.append(source('CD-W03',file['filename'],'wheel_package','PyPA build maintainers / PyPI','PUB-PYPA-BUILD','1.2.2.post1','build-1.2.2.post1.dist-info/RECORD, entry_points.txt; build/__main__.py L444–449',
       '22,950B wheel matches PyPI SHA-256. 19 members/19 RECORD rows, 18 nonempty digests and sizes valid. console_scripts pyproject-build and pipx.run build both refer to build.__main__:entrypoint; function exists at L444–445. The ZIP contains no pyproject-build wrapper.',
       ['Member presence and declared callable linkage; wrapper can be absent from wheel despite an entrypoint declaration'],['19 RECORD members imply 19 entrypoints','Declared metadata is a past runtime execution receipt'],
       'No package installation/import/execution or build-job proof. Historical execution and exact build generation remain 미확인.',cases=['CD-WHEEL-BUILD']))
    rows.append(source('CD-W04','build-1.2.2.post1.json','release_record','PyPI / PyPA build maintainers','PUB-PYPA-BUILD','1.2.2.post1','urls[filename=build-1.2.2.post1-py3-none-any.whl]',
       'Official version JSON declares wheel URL, 22,950B size and SHA-256 matching received archive.', ['Fixed package origin and digest declaration'],[],
       'Distribution metadata does not record installation, callable execution or build environment.',False,'Same release event/work as CD-W03; kept as provenance receipt',cases=['CD-WHEEL-BUILD']))
    for n,key,paired in [('CD-W05','wheel-spec.html','CD-W01'),('CD-W06','entrypoints-spec.html','CD-W02')]:
        rows.append(source(n,key,'wheel_spec','PyPA','RULE-PYTHON-PACKAGING-SPECS','observed 2026-11-23','Relevant sections, also read in pinned RST',
       'Rendered official specification read; semantic rule is also recorded from pinned source.', ['Canonical readable rule URL'],[],
       'Moving latest URL; source commit is separately pinned but a historical site build binding is not claimed.',False,'Same normative work as '+paired,cases=['CD-WHEEL-BUILD']))
    rows.append(source('CD-W07','packaging-head.json','publication_record','PyPA','RULE-PYTHON-PACKAGING-SPECS',PACKAGING_SHA,'commit.sha / commit.committer.date',
       'Pinned the documentation source HEAD at '+PACKAGING_SHA+' after reading the live official specification.', ['Fixed source revision for cited rules'],[],
       'Does not certify exact live HTML build input.',False,'Source pin for CD-W01/CD-W02, not an additional material',fixed='https://api.github.com/repos/pypa/packaging.python.org/commits/'+PACKAGING_SHA,cases=['CD-WHEEL-BUILD']))
    (ROOT/'sources.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows))
    counts=Counter(x['category'] for x in rows if x['countable'])
    (ROOT/'source-counts.json').write_text(json.dumps({'rows':len(rows),'countable':sum(counts.values()),'categories':dict(counts),
        'epub_minimum_spec_plus_selected_package':counts['epub_spec']+counts['epub_package'],'wheel_minimum_spec_plus_selected_package':counts['wheel_spec']+counts['wheel_package'],
        'same_release_event':'EPUB release tag event is same as inherited Cole; excluded. New Trees package is a different work.','inherited_core_spec':'EPUB core REC 2026-01-13 reread but excluded; distinct RS REC 2024-10-17 counted.','all_inside_main_12_pairs':False},ensure_ascii=False,indent=2)+'\n')
    failed=[]
    for path in RECEIPTS.glob('*.json'):
        rec=json.loads(path.read_text())
        if rec.get('error'):failed.append({'receipt':PREFIX+'receipts/'+path.name,**rec})
    (ROOT/'failures.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in failed))
    print(json.dumps({'assertions':assertions,'countable_materials':dict(counts),'all_countable':sum(counts.values()),'failures':len(failed)},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
