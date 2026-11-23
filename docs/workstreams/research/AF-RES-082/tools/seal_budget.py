import pathlib,json,csv,datetime
D=pathlib.Path(__file__).resolve().parents[1]
receipts={r['key']:r for r in map(json.loads,(D/'evidence'/'http-receipts.jsonl').read_text().splitlines())}
loc={'RTD-START':'§Importing the project, Checking the first build, Configuration, Versioning; extracted L154–178,216–246,281–344','RTD-CONFIG':'v2 §build.jobs/build.commands, sphinx/mkdocs; L122–197,581–766','SPHINX-BUILD':'§Synopsis, Description, -M/-b; L44–91','PAGES-SOURCE':'§About publishing sources, branch troubleshooting, custom Actions; L43–94','PAGES-WORKFLOW':'§Upload artifact, Deploying, Linking jobs; L53–91','PKGDOWN-BUILD':'§Usage, General config, Development mode; L46–149'}
obs={
 'RTD-START':'Git repository import leads to managed build then View docs. Dependencies remain project configuration. latest follows default branch; stable and named version activation are distinct controls.',
 'RTD-CONFIG':'Same hosting service invokes Sphinx or MkDocs from their own configurations. Config paths are repo-root-relative. Custom commands bypass predefined build jobs; custom HTML must reach READTHEDOCS_OUTPUT/html.',
 'SPHINX-BUILD':'Sphinx reads sourcedir/conf.py and writes outputdir; make-mode places HTML under outputdir/html. A build command alone does not publish or preserve URL paths.',
 'PAGES-SOURCE':'Pages accepts a selected branch root/docs or a custom workflow that builds, uploads and deploys. It does not provide an R builder implicitly. CNAME in a repository alone does not configure the domain.',
 'PAGES-WORKFLOW':'Artifact upload and deploy are separate dependencies: build needs, pages:write/id-token:write and environment are required. This is not the gh-pages-branch workflow contract.',
 'PKGDOWN-BUILD':'R package docs are generated at docs/ by default. url sets crosslinks/sitemap and deployment metadata. release docs/ and development docs/dev/ distinguish two modes, not all historical release snapshots.'}
lineage={'RTD-START':'OFF-RTD','RTD-CONFIG':'OFF-RTD','SPHINX-BUILD':'OFF-SPHINX','PAGES-SOURCE':'OFF-PAGES','PAGES-WORKFLOW':'OFF-PAGES','PKGDOWN-BUILD':'OFF-PKGDOWN'}
src=[]
for k,r in receipts.items():
 if r['phase']!='budget':continue
 src.append({'source_id':'ROOT-'+k,'lineage_id':lineage[k],'kind':'official_contract','url':r['url'],'version':'current document opened 2026-11-23; not presumed to be 2024–2025 edition','section':loc[k],'opened_at_utc':r['opened_at_utc'],'questions':['Q2','Q3','Q5','Q6','Q8'],'case_ids':['P1','P2','P3'] if k.startswith(('RTD','SPHINX')) else ['R1','R2','R3'] if k.startswith('PKGDOWN') else ['P1','P2','P3','R1','R2','R3'],'observed':obs[k],'limitations':'Supplier capability, not project deployment evidence; historical config and publication must be checked separately. Pages branch/token and custom artifact rules must not be blended.','claim_support':'supports conditional architecture; refutes link count equals stage count','sha256':r['body_sha256'],'phase':'budget','count_as_independent':True})
(D/'evidence'/'root-sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in src))
seen=set();rows=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for p in csv.DictReader((D/'prelinks.csv').open()):
 c=p['case_id'];arm=p['arm'];py=c.startswith('P')
 keys=(['RTD-START','RTD-CONFIG'] if py else ['PAGES-SOURCE','PAGES-WORKFLOW']) if arm=='A' else (['SPHINX-BUILD','PAGES-SOURCE'] if py else ['PKGDOWN-BUILD','PAGES-SOURCE'])
 reused=[]
 for k in keys:reused.append(k in seen);seen.add(k)
 if py and arm=='A':
  verdict='conditional_service_start';reason='One service contract covers generation and publication with Sphinx/MkDocs. Project dependencies and paths still require configuration.'
  req2='unconfirmed_no_second_owner_condition' if c!='P3' else 'conditional: named 1.x version can be activated; whether this project does so remains unverified'
  missing='tag build config; enabled versions; domain/redirect settings; actual successful build and served HTML'
 elif py and arm=='B':
  verdict='conditional_alternative' if c!='P3' else 'hold_native_input_contract'
  reason='Generator output and Pages publication can be connected, but exact project config, URL and hosting authority remain unverified.' if c!='P3' else 'Markdown alone does not prove incompatibility. No native Sphinx configuration/template/extension contract for selected source has been shown; do not silently substitute MkDocs.'
  req2='unconfirmed_no_second_owner_condition' if c!='P3' else 'unconfirmed: two links alone do not define 1.x routing/retention'
  missing='generator dependencies; complete HTML root; source branch versus artifact choice; domain and historical path routing'
 else:
  verdict='conditional_if_html_exists' if arm=='A' else 'conditional_source_to_site'
  reason='Pages can publish complete static HTML, but its two docs do not explain generation from an R package.' if arm=='A' else 'pkgdown documents source-to-docs generation and the Pages link explains publication of the complete output tree.'
  req2='unconfirmed_no_second_owner_condition';missing='R package build dependencies; _pkgdown.yml destination/url; chosen Pages source; permissions/custom domain; current artifact'
 row=dict(p,exposure_1_source_id='ROOT-'+keys[0],exposure_1_url=receipts[keys[0]]['url'],exposure_1_section=loc[keys[0]],exposure_1_reused=str(reused[0]).lower(),exposure_2_source_id='ROOT-'+keys[1],exposure_2_url=receipts[keys[1]]['url'],exposure_2_section=loc[keys[1]],exposure_2_reused=str(reused[1]).lower(),budget_unique_documents=2,case_document_assessments=2,allocated_first_fetches=sum(not x for x in reused),budget_verdict=verdict,budget_reason=reason,condition_2_budget=req2,missing_settings=missing,budget_assessed_at_utc=now,postbudget_evidence='not_opened',same_historical_deployment='unconfirmed',postbudget_verdict='pending')
 rows.append(row)
with (D/'paths.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
summary={'sealed_at_utc':now,'initial_links_commit':'8ba1d686d4c7e50067f9d52bc753a4e02708cd42','cases':6,'arms':12,'max_documents_per_arm':2,'case_document_assessments':24,'unique_documents_read':6,'external_http_requests':6,'redirects':0,'cross_case_document_reuses':18,'first_fetch_allocation':'Fetches were concurrent; allocation in paths.csv is accounting by fixed P1A,P1B,... order, not a claim of chronological network order.','actual_reader':'same root investigator; documents applied to multiple cases, not 12 independent readers','read_windows':['RTD-START 109–188,216–344','RTD-CONFIG 122–197,429–472,570–808','SPHINX-BUILD 44–100','PAGES-SOURCE 43–96','PAGES-WORKFLOW 53–91','PKGDOWN-BUILD 38–185,260–279'],'phase_boundary':'No selected-project deployment config/run/current HTML has been read by root/case investigators before this seal; publication comparison investigator is separate.'}
(D/'evidence'/'budget-seal.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
