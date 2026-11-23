"""Produce a source ledger and bounded excerpts from already-read public receipts.

No network, code from sources, or publisher application is executed here.
"""
from pathlib import Path
import hashlib
import io
import json
import posixpath
import struct
import sys
import urllib.parse
import zipfile

ROOT = Path(__file__).parent
EVIDENCE = ROOT / 'evidence'
RAW = EVIDENCE / 'raw'
sys.path.insert(0, str(ROOT.parents[1] / 'tools'))
from http_evidence import now

TAG = '46d7e07e1b39b2d0a0245ececaf896edcd9de4b2'
SAMPLE = 'https://raw.githubusercontent.com/IDPF/epub3-samples/' + TAG + '/30/accessible_epub_3/'

# One entry per direct HTTP retrieval. Mirrors and discovery-only endpoints stay
# visible but do not contribute to the minimum source count.
M = {
 'XF-IIIF-SPEC': ('IIIF-Presentation-3.0', 'cross_spec', True, '3.0.0', '1.2; 5.2; 5.3; 6.3',
  'Manifest embeds Canvas; a Canvas URI may be separately dereferenceable. Referenced, non-embedded resources must dereference. A URI is not automatically a required extra document read.',
  'Canvases may be able to be dereferenced separately from the Manifest',
  'Supports separate scores for embedded description and actual image retrieval.',
  'Specification is a contract, not proof any individual deployment works; publication UTC not stated in inspected header.'),
 'XF-EPUB-SPEC': ('W3C-EPUB-3.3', 'cross_spec', True, '2026-01-13 Recommendation', '3.6; 4.2.6.3.1; 5.6.1; 5.7.1; 6.1.4.3.1',
  'container.xml names the package; manifest enumerates publication resources; spine orders references. Certain remote resource classes are allowed. base can alter relative-link interpretation.',
  'The spine element defines an ordered list of manifest item references',
  'Supports package completeness checks without assuming network-independent execution.',
  'Current 3.3 rules are not retroactively asserted as the conformance verdict for the 3.0 sample; no EPUBCheck or reader execution.'),
 'XF-EPUB-PINNED-SPEC': ('W3C-EPUB-3.3', 'cross_spec', False, '2026-01-13 Recommendation', 'Entire response; pinned URL mirror',
  'Pinned Recommendation URL returns byte-identical HTML to /TR/epub-33/ at this observation.', '',
  'Supports edition identification.', 'Duplicate of XF-EPUB-SPEC; not another unique source.'),
 'XF-IIIF-MANIFEST': ('IIIF-cookbook-0001', 'cross_work', True, 'Presentation 3; current published recipe', '$.items[0].items[0].items[0].body',
  'Published recipe has one embedded Canvas, AnnotationPage and painting Annotation; body names an external PNG 1200x1800. Canvas id and image id have different retrieval roles.',
  'Simplest Image Example (IIIF Presentation v3)',
  'Supports a working published manifest→image example and embedded Canvas sufficiency.',
  'Official sample, not a production cultural-heritage object; viewer JS was not run; no immutable version promise.'),
 'XF-IIIF-IMAGE': ('IIIF-cookbook-0001', 'asset', True, 'Recipe image at observed UTC', 'page1-full.png; PNG IHDR and visual inspection',
  'Actual PNG returned HTTP200 image/png, 128352 bytes, IHDR 1200x1800; image visually shows first-page orientation labels. Dimensions match manifest.',
  'Top of First Page to Display',
  'Confirms referenced payload, beyond a manifest listing.',
  'Static image verified; client interaction and later availability not verified.'),
 'XF-IIIF-CANVAS': ('IIIF-cookbook-0001', 'cross_work', False, 'Observed current response', 'Embedded Canvas id followed as a separate request',
  'Canvas id redirects HTTP301 to https://iiif.io//404.html, final HTTP200 text/html with Page Not Found. Its complete Canvas description remains inside the successful manifest.',
  '404 Page Not Found',
  'Refutes HTTP200 as content success; also refutes requiring every embedded id to resolve before using the manifest.',
  'Error page excluded from source minimum. This is not a failed required image and is not proof the recipe is broken.'),
 'XF-IIIF-PROCESS': ('IIIF-cookbook-process', 'method', True, 'Current process page', 'Process; recipe requirements and Fixtures',
  'Official cookbook process asks for complete standalone examples, actual referenced resources, and links that resolve; shared fixtures are preferred.',
  'All referenced content resources, external annotations and other links should resolve',
  'Supports treating cookbook manifests as published examples rather than invented research fixtures.',
  'A stated maintenance rule does not guarantee every linked resource remains reachable.'),
 'XF-IIIF-INCIDENT': ('InternetArchive-IIIF-61', 'cross_work', True, 'Issue opened 2024-03-04', 'Issue body, naeb-b101-f02-23 manifest and exact tile URL',
  'Reporter gives an actual manifest, Universal Viewer URL and a tile URL with reported browser-console 404. Direct current requests to old host are separately recorded as proxy503.',
  'there are a lot of 404 errors for tiles',
  'Primary reported counterexample: having a manifest is insufficient when required referenced image service fails.',
  '2024 observer report, not this session reproducing the 2024 failure. Does not establish missing source image or specific root cause.'),
 'XF-IIIF-INCIDENT-COMMENTS': ('InternetArchive-IIIF-61', 'cross_work', False, '2024-03-04 to 2024-03-05', 'Comments 1976815191, 1976961665, 1977415223',
  'Collaborator supplies a replacement archive.org image URL. A later comment cautions that old image-generation exceptions can be mapped to404, so broken URL syntax is not established.',
  'probably not broken URLs',
  'Refutes a simplistic root-cause claim while preserving the observed missing-resource symptom.',
  'Same incident as XF-IIIF-INCIDENT, excluded as additional independent source; comments do not prove current old-host failure.'),
 'XF-IIIF-NAEB-MANIFEST': ('InternetArchive-IIIF-61', 'cross_work', False, 'Current request', 'Old host manifest URL from issue',
  'Current fetch returned proxy503 text: upstream connection/reset error before headers.', '',
  'Unconfirmed current service; preserves failed attempt.',
  'Proxy-level response is not a publisher404 and cannot establish service-wide or permanent loss.'),
 'XF-IIIF-OLD-TILE': ('InternetArchive-IIIF-61', 'asset', False, 'Current request', 'Exact old tile URL from issue',
  'Current fetch returned proxy503 with the same upstream-connect message as old manifest.', '',
  'Unconfirmed current payload; no replacement of original failure receipt.',
  'Does not reproduce the historical404 and is excluded from direct-source minimum.'),
 'XF-IIIF-NEW-TILE': ('InternetArchive-IIIF-61', 'asset', True, 'Current replacement endpoint', 'Comment supplied URL; followed redirect to image/iiif/2/...jp2/1024,2048,1024,1024/256,/0/default.jpg',
  'The collaborator-supplied replacement path currently returns HTTP200 image/jpeg, 25134 bytes after301. Static payload succeeds independently of old-host inability.', '',
  'Supports an actual alternative payload, not equivalence to historical failed bytes.',
  'No old payload bytes available for equality comparison; no historical recovery-time claim.'),
 'XF-EPUB-TREE': ('IDPF-Accessible-EPUB-3', 'cross_work', False, 'main tree7651e2002b631e6577fadf7e9e0692fa6efb8746', 'Recursive Git tree for initial file discovery',
  'Lists accessible_epub_3 package, cover, images and container file. Subsequent verification uses the release tag commit, not this moving tree.', '',
  'Discovery only.', 'File listing is not actual payload and contributes no minimum source count.'),
 'XF-EPUB-RELEASES': ('IDPF-Accessible-EPUB-3', 'cross_work', False, 'Release20230704; published2023-07-04T16:09:10Z', 'Release asset accessible_epub_3.epub',
  'Release lists a 4051892-byte EPUB asset. Actual asset was downloaded and parsed separately.', '',
  'Supports publisher release→asset address.', 'Listing is not actual file verification; not counted separately from the package work.'),
 'XF-EPUB-TAG': ('IDPF-Accessible-EPUB-3', 'cross_work', False, TAG, 'refs/tags/20230704',
  'Tag ref points to commit46d7e07e1b39b2d0a0245ececaf896edcd9de4b2.', '',
  'Pins the source comparison.', 'Ref alone does not bind released archive bytes to a build; actual members are compared separately.'),
 'XF-EPUB-PACKAGE': ('IDPF-Accessible-EPUB-3', 'cross_work', True, 'Release20230704; EPUB3.0; ISBN9781449328030', 'ZIP container; META-INF/container.xml; EPUB/package.opf',
  'Direct 4051892-byte ZIP contains38 entries. container.xml points to EPUB/package.opf; all35 manifest resources are present; spine has22 references and manifest has0 remote hrefs.', '',
  'Confirms a real packaged work with locally present dependency files.',
  'Checks declared members, not full EPUB standard conformance, visual reader behavior, scripts or every external hyperlink. Release response MIME is application/octet-stream.'),
 'XF-EPUB-ROOT': ('IDPF-Accessible-EPUB-3', 'asset', True, TAG, '30/accessible_epub_3/META-INF/container.xml',
  'rootfile full-path points to EPUB/package.opf. Tag source LF263 bytes vs release member CRLF269 bytes; newline-normalized text matches.',
  'EPUB/package.opf',
  'Supports package entry resolution and representation-aware comparison.',
  'Raw source and ZIP member are the same logical file and counted once; raw MIME text/plain does not supply EPUB semantic media type.'),
 'XF-EPUB-OPF': ('IDPF-Accessible-EPUB-3', 'asset', True, TAG, '30/accessible_epub_3/EPUB/package.opf; manifest and spine',
  '35 manifest items,22 spine references. cover item resolves to cover.xhtml; cover-image item resolves to covers/9781449328030_lrg.jpg. SourceLF5774 vs ZIPCRLF5867 bytes; normalized text matches.',
  'Accessible EPUB 3',
  'Confirms actual package metadata, beyond release index.',
  'All listed files exist; this does not prove all dependencies were correctly declared or that a reader runs them.'),
 'XF-EPUB-COVER': ('IDPF-Accessible-EPUB-3', 'asset', True, TAG, '30/accessible_epub_3/EPUB/cover.xhtml; figure#cover-image/img',
  'Cover XHTML contains inline CSS and a single local img src=covers/9781449328030_lrg.jpg. SourceLF552 vs ZIPCRLF568 bytes; normalized text matches.',
  'covers/9781449328030_lrg.jpg',
  'Supports static cover sufficiency using only members already inside the downloaded archive.',
  'No separate network image is needed for this cover; full e-reader rendering remains untested.'),
 'XF-EPUB-COVER-IMAGE': ('IDPF-Accessible-EPUB-3', 'asset', True, TAG, '30/accessible_epub_3/EPUB/covers/9781449328030_lrg.jpg',
  'Direct source image and EPUB member are byte-identical820269-byte JPEGs. Visual inspection confirms Accessible EPUB3 cover with goat illustration and Matt Garrish/OReilly labels.',
  'Accessible EPUB 3',
  'Confirms linked image bytes and subject, not merely its path in a list.',
  'Source and extracted member are one logical resource; no second count for extraction.'),
 'XF-EPUB-CH04': ('IDPF-Accessible-EPUB-3', 'asset', True, TAG, '30/accessible_epub_3/EPUB/ch04.xhtml; #conclusion, #best_practices_cover',
  'Chapter4 has local CSS and a local image images/web/epub3_0401.png, plus an explicit external OReilly navigation link. SourceLF4614 vs ZIPCRLF4692 bytes; normalized text matches.',
  'Chapter 4. Conclusion',
  'Distinguishes packaged rendering dependency from optional outward navigation.',
  'The external shop link was not followed; package presence cannot guarantee external-link availability.'),
}

def scrub_url(value):
    if not isinstance(value, str):
        return value
    if value.startswith('https://release-assets.githubusercontent.com/'):
        return urllib.parse.urlunsplit(urllib.parse.urlsplit(value)._replace(query=''))
    return value

def scrub(value):
    if isinstance(value, dict):
        return {k: scrub(v) for k,v in value.items() if k.lower() not in ('set-cookie',)}
    if isinstance(value, list):
        return [scrub(v) for v in value]
    return scrub_url(value)

sources = []
for sid,meta in M.items():
    path = EVIDENCE/(sid+'.receipt.json')
    receipt = scrub(json.loads(path.read_text()))
    if sid == 'XF-EPUB-PACKAGE':
        receipt['ephemeral_download_query_redacted'] = True
        receipt['redaction_scope'] = 'Public release-asset signed redirect query only; canonical requested URL, endpoint path, response bytes/hash and timestamps preserved.'
    path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    work,category,eligible,version,location,observation,excerpt,support,limits=meta
    fingerprint={k:receipt[k] for k in ('sha256','git_blob_sha1','body_bytes','status','content_type')}
    row={'source_id':sid,'work_id':work,'lineage_id':work,'category':category,
         'original_url':receipt['requested_url'],'published_utc':None,
         'retrieved_utc':receipt['retrieved_utc'],'version':version,'location':location,
         'questions':['Q7'],'cases':['cross_fields'],'observation':observation,
         'excerpt':excerpt,'fingerprint':fingerprint,'support_refute':support,
         'limitations':limits,'reread_url':receipt['requested_url'],'eligible':eligible,
         'receipt_path':str(path.relative_to(ROOT.parents[1])),
         'evidence_path':str((EVIDENCE/(sid+'.excerpt.json')).relative_to(ROOT.parents[1])),
         'observer':'AF-RES-090 cross_fields agent; HTTP and local parsing unless explicitly attributed to reporter'}
    if sid.startswith('XF-EPUB') and sid not in ('XF-EPUB-SPEC','XF-EPUB-PINNED-SPEC','XF-EPUB-TREE'):
        row['published_utc']='2023-07-04T16:09:10Z (release; member metadata dates are separate)'
    if sid in ('XF-EPUB-SPEC','XF-EPUB-PINNED-SPEC'):
        row['published_utc']='2026-01-13 (date only)'
    if sid.startswith('XF-IIIF-INCIDENT'):
        row['published_utc']='2024-03-04T15:09:53Z (issue); comments have individual timestamps in source'
    if sid=='XF-EPUB-PINNED-SPEC': row['duplicate_of']='XF-EPUB-SPEC'
    if sid=='XF-IIIF-INCIDENT-COMMENTS': row['same_incident_as']='XF-IIIF-INCIDENT'
    sources.append(row)
    evidence={'source_id':sid,'recorded_utc':now(),'source_url':receipt['requested_url'],
              'retrieved_utc':receipt['retrieved_utc'],'observations':observation,
              'short_excerpts':[excerpt] if excerpt else [],'limitations':limits,
              'sha256':receipt['sha256'],'full_raw_preserved_in_commit':False}
    (EVIDENCE/(sid+'.excerpt.json')).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')

(ROOT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))

package=zipfile.ZipFile(io.BytesIO((RAW/'XF-EPUB-PACKAGE.bin').read_bytes()))
member_map={'XF-EPUB-ROOT':'META-INF/container.xml','XF-EPUB-OPF':'EPUB/package.opf',
            'XF-EPUB-COVER':'EPUB/cover.xhtml','XF-EPUB-COVER-IMAGE':'EPUB/covers/9781449328030_lrg.jpg',
            'XF-EPUB-CH04':'EPUB/ch04.xhtml'}
assets=[]
for source in sources:
    sid=source['source_id']
    if source['category']!='asset' and sid not in ('XF-IIIF-CANVAS','XF-IIIF-MANIFEST','XF-EPUB-PACKAGE'):
        continue
    receipt=json.loads((EVIDENCE/(sid+'.receipt.json')).read_text())
    row={'asset_id':sid+'-ASSET','source_id':sid,'work_id':source['work_id'],
         'file':member_map.get(sid,urllib.parse.urlsplit(receipt['requested_url']).path),
         'original_url':receipt['requested_url'],'hosting_location':urllib.parse.urlsplit(receipt['final_url']).netloc,
         'directly_read':receipt['status']==200,'manual_reconstruction':False,
         'browser_executed':False,'retrieved_utc':receipt['retrieved_utc'],
         'mime_observed':receipt['content_type'],'sha256':receipt['sha256'],
         'body_bytes':receipt['body_bytes'],'anchor':None,'observation':source['observation'],
         'limitations':source['limitations'],'reader_main_denominator':False}
    if sid in member_map:
        raw=(RAW/(sid+'.bin')).read_bytes(); member=package.read(member_map[sid])
        row.update({'fixed_source_commit':TAG,'package_source_id':'XF-EPUB-PACKAGE',
                    'archive_member_bytes':len(member),'archive_member_sha256':hashlib.sha256(member).hexdigest(),
                    'archive_exact_match':raw==member,
                    'archive_newline_normalized_match':raw.replace(b'\r\n',b'\n')==member.replace(b'\r\n',b'\n'),
                    'normalization':'CRLF→LF only; raw hashes retained separately',
                    'same_logical_file_counted_once':True})
    if sid=='XF-IIIF-IMAGE':
        row['png_ihdr_dimensions']=list(struct.unpack('>II',(RAW/(sid+'.bin')).read_bytes()[16:24]))
    if sid=='XF-IIIF-CANVAS':
        row.update({'directly_read':False,'classification':'separate identifier request returns soft404; complete Canvas is embedded',
                    'inline_payload_in':'XF-IIIF-MANIFEST','extra_reads_required_for_embedded_canvas':0})
    if sid=='XF-EPUB-COVER': row['dependency']='covers/9781449328030_lrg.jpg (archive-local, relative to EPUB/cover.xhtml); CSS inline'
    assets.append(row)
(ROOT/'assets.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in assets))

counts={'recorded_utc':now(),'direct_receipt_rows':len(sources),'eligible_unique_materials':sum(x['eligible'] for x in sources),
        'independent_work_lineages':len({x['lineage_id'] for x in sources if x['eligible']}),
        'eligible_by_category':{c:sum(x['eligible'] and x['category']==c for x in sources) for c in sorted({x['category'] for x in sources})},
        'logical_http_gets':len(sources),'received_entity_bytes':sum(x['fingerprint']['body_bytes'] for x in sources),
        'exclusions':'Includes failed attempts and duplicate mirrors in request cost, but not source minimum. Web search and view_image calls are outside measured HTTP byte cost.',
        'human_time_measured':False,'main_traversal_count_contribution':0}
(ROOT/'counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False,indent=2))
