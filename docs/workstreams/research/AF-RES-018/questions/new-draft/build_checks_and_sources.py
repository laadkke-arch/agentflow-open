#!/usr/bin/env python3
"""Record control candidates and directly read evidence; never invent an N label."""
import datetime
import json
import pathlib

P = pathlib.Path(__file__).resolve().parent
def read(n): return json.loads((P/n).read_text())
def write(n,d): (P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
interval = '2026-11-21T03:48:58Z/' + now
qs = read('new-questions.json'); gold = read('gold-draft.json')['rows']
sources = []
def src(sid,url,title,sections,confirmed,limits,used,kind='official_documentation',version='live',at=None):
    sources.append({'id':sid,'url':url,'accessed_at_utc':at or interval,'access_time_precision':'point' if at else 'session interval; exact tool-call second not retained',
                    'source_type':kind,'title':title,'version_or_date':version,'sections_read':sections,'confirmed':confirmed,'limits':limits,'level':'D1','used_in':used,
                    'count_for_method_comparison_literature':False})

for q in qs:
    src('NQ-'+q['id'],q['original_fetch_url'],'Public recommendation question '+q['platform']+':'+q['platform_id'],q['source_position'],
        q['summary'],'Initial revision verified only for Stack Exchange. This source records the request, not candidate capability or truthful claims in replies.',
        ['Q2','Q3',q['id']],kind='public_community_question',version=q['version'],at=q['read_at_utc'])
answers = read('se-answer-evidence.json')
src('NQ-SE-ANSWERS',answers['url'],'Stack Exchange answers for the nine selected new questions','items[].body, answer_id, question_id, is_accepted; 15 answer bodies',
    'Fifteen answers cover nine selected questions; six questions have accepted answers, including explicit self-answers. Candidate entities and use records were mapped by the worker.',
    'Acceptance does not prove current feasibility. Caddy and Pentaho require separate original-constraint/edition interpretation.', ['Q3','Q5','Q8'],kind='public_community_answers',at=answers['read_at_utc'])
for q in qs:
    if q['platform'] in ('hackernews','github_discussions'):
        names = [r['candidate'] for r in gold if r['qid']==q['id']]
        src('NQA-'+q['id'],q['original_fetch_url'],'Public answer records for '+q['platform']+':'+q['platform_id'],'reply bodies and asker responses; individual comment IDs are in gold-draft.json',
            'Observed candidate names: '+', '.join(names)+'. Use/adoption is distinguished from thanks or intent to try.',
            'Worker entity mapping; current snapshot can omit deleted material. Reported use and objective condition satisfaction are distinct.', ['Q3','Q5','Q8',q['id']],kind='public_community_answers',at=q['read_at_utc'])

official = [
 ('NCO01','https://github.com/flameshot-org/flameshot/issues/4503','Flameshot window capture issue','maintainer response, lines 193-237','Maintainer explains that Wayland prevents reliable active-window detection in the discussed 14.0 release-candidate context.','Scope is this build/platform; it does not establish failure on every platform or an optional OS requirement.',['N001'],'issue discussion; April 2026'),
 ('NCO02','https://flameshot.org/docs/advanced/commandline-options/','Flameshot command line options','Usage and Available CLI options','Documented capture modes include GUI region and full/screen capture.','An omitted command alone is not proof that no window-capture workaround exists.',['N001'],'live'),
 ('NCO03','https://github.com/apache/nifi/blob/main/LICENSE','Apache NiFi license','Apache License header and application; lines 846-1169','The Apache NiFi distribution is licensed under Apache 2.0, with separately licensed components.','Commercial support does not change the upstream distribution into non-open-source software. This is a license identity check, not legal advice.',['N004'],'main viewed 2026-11-21'),
 ('NCO04','https://nifi.apache.org/','Apache NiFi overview','data-flow automation overview','NiFi is a data-flow automation product, establishing the same broad ETL/data-integration category.','No claim about this exact ODBC deployment was tested.',['N004'],'live'),
 ('NCO05','https://www.iis.net/','Microsoft IIS official overview','lines 28-30, 66-76','Microsoft identifies IIS as its web server for Windows Server.','Candidate is native IIS for Windows Server, not an added Windows virtual machine on Linux.',['N005'],'live'),
 ('NCO06','https://docs.python.org/3/library/http.server.html','Python http.server documentation','opening warning and handler discussion','The documentation warns that http.server provides only basic security and is not recommended for production.','This warning is not a proof that every customized deployment is impossible; therefore it was not used as the strict N control.',['N005'],'Python 3.15.2 page displayed'),
 ('NCO07','https://discourse.pi-hole.net/t/use-pi-hole-blacklist-to-block-youtube-channels/37022','Pi-hole channel blocking support discussion','question and project response; complete short discussion','The project forum explains that Pi-hole can block the YouTube domain but cannot select individual YouTube channels by DNS.','Dated forum response; scope is standalone DNS blocking, not Pi-hole composed with a browser extension.',['N006'],'2020-08-10'),
 ('NCO08','https://www.mailenable.com/standard_edition.asp','MailEnable Standard Edition','Standard Edition introduction, lines 97-99','MailEnable Standard is installable SMTP, IMAP, POP3 and webmail server software for Windows servers.','The control is the self-administered Standard server, not a managed hosting provider using it.',['N007'],'live'),
 ('NCO09','https://github.com/fail2ban/fail2ban','Fail2Ban README','Installation Required, lines 234-266','The documented installation requires Python or PyPy3 and installs Python-based executable scripts.','Scope is the documented Fail2Ban distribution; alternative rewrites such as fail2zig are separate candidates.',['N010'],'v1.1.2.dev1 README displayed'),
 ('NCO10','https://wisprflow.ai/flow-vs-gboard-typing','Wispr Flow official comparison','offline availability table and explanatory paragraph','Wispr says Flow needs an internet connection on every supported platform and does not provide offline dictation.','Official marketing description; this check covers offline capability, not comparative accuracy or quality.',['N011'],'live; page references September 2026'),
 ('NCO11','https://proton.me/support/custom-domain','Proton Mail custom-domain requirements','prerequisites, lines 212-217','The support page requires a paid Proton plan to add a custom email domain.','The negative is specifically Proton Mail Free; paid Proton Mail and Bridge are not excluded by this fact.',['N012'],'live'),
 ('NCO12','https://github.com/http-party/node-http-proxy','node-http-proxy README','About, Installation and Core Concept, lines 202-278','The proxy is a Node.js programmable library installed with npm and configured through JavaScript.','The question says it should avoid learning a whole Node.js ecosystem; sensitivity analysis should also treat this wording as a preference.',['N015'],'master viewed 2026-11-21'),
 ('NCO13','https://github.com/vorpaljs/bash-parser','bash-parser README','Usage, output AST, license','The library emits a Bash AST and is distributed under MIT.','Neither AST output nor MIT license alone proves uselessness: a wrapper may convert it and compatibility differs from a request for the exact AGPL license. Not promoted to strict N.',['N016'],'master viewed 2026-11-21'),
 ('NCO14','https://ironfoxoss.org/download/','IronFox download methods','Overview and Prerequisites, lines 47-88','The official page lists direct downloads, Accrescent, the project F-Droid repository and Obtainium.','No explicit Google Play exclusion sentence was located; absence from this list alone was not treated as conclusive official proof.',['N017'],'160.0.1 displayed'),
 ('NCO15','https://ironfoxoss.org/docs/faq/','IronFox FAQ','download, F-Droid and Google Play Services sections','The FAQ explains its own F-Droid repository and independence from Google Play Services.','Google Play Services and Google Play distribution are different claims. This page cannot by itself establish the latter.',['N017'],'live'),
 ('NCO16','https://apps.apple.com/us/app/safari/id1146562112','Apple Safari app listing','developer description and Compatibility, lines 49-51 and 199-210','Apple lists Safari as an Apple-device browser; the app package requires iOS 10 or later, with corresponding iPadOS and visionOS requirements.','The control is this Apple Safari package, not a similarly named Android app or remote browser session.',['N017'],'live'),
 ('NCO17','https://www.apple.com/safari/','Apple Safari overview','platform description, lines 33 and 71','Apple says Safari is developed specifically for Apple devices.','No independent privacy/performance comparison is inferred from this marketing page.',['N017'],'live'),
 ('NCO18','https://github.com/openai/gpt-oss','gpt-oss official README','model size and MXFP4 highlights, lines 197-225; reference implementation lines 365-422','The 120b model has 117B parameters and its MXFP4 configuration is described for an 80GB GPU; the official BF16 reference implementation requires multiple H100 GPUs.','The 8GB full-GPU failure is an inference from parameter storage and documented configuration, not a measured run. CPU offload or replacing/altering weights changes the probe scope.',['N020'],'main viewed 2026-11-21'),
 ('NCO19','https://openai.com/index/introducing-gpt-oss/','Introducing gpt-oss','Introduction, lines 56-62','Official release gives 80GB deployment for 120b and 16GB memory deployment for 20b.','A successful configuration is not automatically a minimum-memory proof; the stronger scoped check uses the README/parameter count.',['N020'],'2025-08-05'),
 ('NCO20','https://alignment.anthropic.com/2026/abstractive-red-teaming/','Abstractive red-teaming of language model character','model list, lines 44-46; method and baseline sections','The Anthropic-hosted research classifies Claude Sonnet 4 and other evaluated proprietary models as closed-source.','The study-date classification does not prove present weight-release status; this source alone was not accepted as a strict open-weight exclusion.',['N019'],'March 2026'),
 ('NCO21','https://www.backblaze.com/computer-backup/docs/unsupported-operating-systems','Backblaze unsupported operating systems','Linux/BSD/Unix section, lines 84-86','Backblaze Computer Backup does not support installation on Linux/BSD/Unix.','Do not conflate this product with B2, which can be used by Linux clients; supporting Reddit question excluded for date confirmation.',['R002'],'updated 2026-01-14'),
 ('NCO22','https://sonarr.tv/','Sonarr overview','opening and Features, lines 2-33','Sonarr is an internet PVR with episode download automation.','This classifies the product; it does not imply unlawful use. Supporting Reddit question excluded for date confirmation.',['R003'],'live'),
 ('NCO23','https://one.google.com/about/plans','Google One plans','Basic and 2TB plan storage rows, lines 28-49','The Basic plan is 100GB total, while a separate plan has 2TB total storage.','Do not apply the 100GB limit to Google One as a whole; prices/region were not generalized. Supporting Reddit question excluded.',['R004'],'live'),
 ('NCO24','https://borgbackup.readthedocs.io/en/1.4.0/usage/general.html','Borg 1.4 repository locations','repository URL/local and SSH syntax','Borg 1.4 documentation covers local and SSH repository locations.','S3-mount/adapter compositions may work and newer Borg adds S3; therefore lack of native support was not promoted to a universal strict N.',['R001'],'1.4.0'),
 ('NCO25','https://www.1password.community/1password-at-home-31/does-1password8-support-standalone-vaults-15786','1Password 8 standalone vault support','employee response, lines 33-42','The employee response states that 1Password 8 does not support standalone vaults and identifies 7 as the last version that does.','Version/date scoped. Do not confuse a self-hosted SCIM bridge with vault hosting; supporting Reddit question excluded.',['R007'],'2023-04-19'),
 ('NCO26','https://support.1password.com/regions/','1Password hosting regions','Choose your region, lines 18-30','Account service data is hosted in the US, Canada or EU according to selected region.','This is not by itself an exhaustive proof that no private-hosting offering exists.',['R007'],'live'),
 ('NCO27','https://1password.com/compare/password-manager','1Password product comparison','self-hosting comparison row','The comparison mentions Bitwarden self-hosting.','Table icons were absent in parsed text; cannot infer every compared product capability from the empty cells.',['R007'],'live'),
 ('NCO28','https://learn.microsoft.com/en-us/windows/powertoys/text-extractor','PowerToys Text Extractor','overview and activation, lines 31-42','Text Extractor performs screen OCR and places recognized text on the clipboard; Microsoft points to Snipping Tool for screenshots.','This is an alternative obvious category-negative, not proof of a subtle same-function near miss.',['N001'],'live'),
 ('NCO29','https://www.mailenable.com/mail-server-features.asp','MailEnable feature matrix','SMTP and mail services rows','The product matrix describes mail server services including SMTP, IMAP and POP.','Checkmark images are missing from parsed table; no edition-by-edition feature inference was made from empty cells.',['N007'],'live')
]
for sid,url,title,sec,conf,lim,used,ver in official:
    src(sid,url,title,sec,conf,lim,['Q3']+used,version=ver)

distractions = [
 ('N001','Greenfoot','https://www.greenfoot.org/door','Java teaching environment; name resembles Greenshot.'),
 ('N002','Sourcetree','https://www.sourcetreeapp.com/','Git graphical client; source-name resemblance to Sourcey/documentation tooling.'),
 ('N003','Salt Project','https://saltproject.io/','Infrastructure automation; name collides with PlantUML Salt.'),
 ('N004','Apache Parquet','https://parquet.apache.org/','Data file format; broad data-engineering category but not an ODBC ETL service.'),
 ('N005','Apache OpenOffice','https://www.openoffice.org/','Office suite; Apache-name collision with a web server.'),
 ('N006','MusicBrainz Picard','https://picard.musicbrainz.org/','Music metadata tagging; adjacent media software, not browser channel blocking.'),
 ('N007','Postman','https://www.postman.com/','API development/testing tooling; Postmark-name/API-category resemblance, not an email delivery provider.'),
 ('N008','Buildbot','https://www.buildbot.net/','CI orchestration; BuiltWith-name/backend-tooling resemblance, not external technographics.'),
 ('N009','Electron Cash','https://electroncash.org/','Cryptocurrency wallet; Electron name collision.'),
 ('N010','Guardrails AI','https://guardrailsai.com/','LLM reliability framework; guard/security-name resemblance, not SSH brute-force blocking.'),
 ('N011','Apache OpenWhisk','https://openwhisk.apache.org/','Serverless functions platform; Whisper/Wispr name resemblance, not dictation.'),
 ('N012','FastAPI','https://fastapi.tiangolo.com/','Python web framework; Fastmail name resemblance, not email hosting.'),
 ('N013','Woodpecker email outreach','https://woodpecker.co/','Cold email/outreach service; exact name collision with Woodpecker CI.'),
 ('N014','OpenPBS','https://github.com/openpbs/openpbs','HPC job scheduler; PBS FAQ name resemblance.'),
 ('N015','CharLS','https://github.com/team-charls/charls','JPEG-LS C++ codec; Charles Proxy name resemblance.'),
 ('N016','Google Breakpad','https://chromium.googlesource.com/breakpad/breakpad/','Crash reporting library; crash-related name/category, not Bash data conversion.'),
 ('N017','Brave Search','https://search.brave.com/','Web search engine; same brand as Brave Browser, not an installable Android browser.'),
 ('N018','FastAPI','https://fastapi.tiangolo.com/','Python web framework; Fastmail name resemblance, not an email application/provider.'),
 ('N019','CursorFX','https://www.stardock.com/products/cursorfx/','Windows mouse-cursor customization; Cursor coding-agent name resemblance.'),
 ('N020','QEMU','https://www.qemu.org/','Machine emulator/virtualizer; Qwen-like name, not a language model.')
]
for i,(qid,name,url,reason) in enumerate(distractions,1):
    src('NCD%02d'%i,url,name+' official product description','product overview / README / product-type description',reason,
        'Worker judges irrelevance to this question. This control is grade 0, not a strict near miss; no product execution was performed.', ['Q3',qid])

# Added after question/input freeze: entity identity, not an alteration of input.
entity_sources = [
 ('NCE01','https://getgreenshot.org/','Greenshot','overview lines 23-28','The official description identifies a Windows screenshot application with region/window/fullscreen capture.','2026-11-21T04:15:08Z',['N001']),
 ('NCE02','https://github.com/sourcey/sourcey','Sourcey','README lines 212-254','The README advertises OpenAPI, MCP, Doxygen and Markdown inputs, static HTML output and AGPL-3.0.','2026-11-21T04:15:24Z',['N002']),
 ('NCE03','https://plantuml.com/salt','PlantUML Salt','Salt introduction lines 19-23','Salt is the PlantUML wireframe/graphical-interface subproject.','2026-11-21T04:15:08Z',['N003']),
 ('NCE04','https://pentaho.com/products/pentaho-data-integration/','Pentaho Data Integration','overview lines 121-168','The official product page identifies an ETL/data-orchestration product and multiple deployment environments. Edition used in the accepted answer remains unknown.','2026-11-21T04:15:29Z',['N004']),
 ('NCE05','https://caddyserver.com/','Caddy','overview lines 18-50','Caddy is a web server with automatic certificate management and a configuration API.','2026-11-21T04:15:08Z',['N005']),
 ('NCE06','https://chromewebstore.google.com/detail/blocktube/bbeaicapbccfllodepmimpkgecanonai','BlockTube','publisher description lines 29-34','The publisher describes YouTube channel/video blocking and identifies the source-code project.','2026-11-21T04:15:08Z',['N006']),
 ('NCE07','https://postmarkapp.com/','Postmark','service description and API example lines 123-167; 312-314','Postmark is an email-delivery service with an API and managed SMTP service.','2026-11-21T04:15:24Z',['N007']),
 ('NCE08','https://www.wappalyzer.com/','Wappalyzer','overview lines 2-20','The official product description covers website technology detection and technographics.','2026-11-21T04:15:08Z',['N008']),
 ('NCE09','https://tauri.app/','Tauri','overview lines 18-20 and 90-91','Tauri is an application framework with cross-platform targets.','2026-11-21T04:15:08Z',['N009']),
 ('NCE10','https://www.sshguard.net/','SSHGuard','overview and log-ingestion/detection/firewall sections','SSHGuard monitors attack logs and invokes firewall backends. This is an entity and role check, not a single-binary check.','2026-11-21T04:15:08Z',['N010']),
 ('NCE11','https://handy.computer/','Handy','speech-to-text description and privacy lines 2-30','Handy is a local speech-to-text application; the official description says voice remains on the computer.','2026-11-21T04:15:08Z',['N011']),
 ('NCE12','https://www.fastmail.com/','Fastmail','email-service overview lines 17-40','Fastmail provides email hosting, domain email and applications.','2026-11-21T04:15:14Z',['N012','N018']),
 ('NCE13','https://woodpecker-ci.org/','Woodpecker CI','overview lines 4-18','Woodpecker CI is a CI/CD engine whose steps run in Docker containers.','2026-11-21T04:15:14Z',['N013']),
 ('NCE15','https://www.charlesproxy.com/documentation/tools/rewrite/','Charles Proxy Rewrite Tool','rewrite tool lines 43-49','The tool modifies requests/responses and supports searching/replacing response-body text.','2026-11-21T04:15:14Z',['N015']),
 ('NCE17','https://brave.com/','Brave Browser','browser introduction and Android product navigation','The site identifies the browser separately from Brave Search and lists an Android product.','2026-11-21T04:15:14Z',['N017']),
 ('NCE19A','https://opencode.ai/','OpenCode','overview lines 38-40','OpenCode is a coding-agent harness with provider/model choices, usable through the terminal.','2026-11-21T04:15:14Z',['N019']),
 ('NCE19B','https://openrouter.ai/','OpenRouter','overview and model/API sections lines 15-28,63-69','OpenRouter provides access to multiple model providers through a platform/API.','2026-11-21T04:15:14Z',['N019']),
 ('NCE20','https://github.com/QwenLM/Qwen3.8/blob/main/README.md','Qwen3.8 official README','introduction/news/models lines 168-217','The official repository records Qwen3.8-27B release on 2026-08-14 and names its weights. The reported Q4 artifact is not identified by this page.','2026-11-21T04:15:29Z',['N020']),
 ('NCA02','https://swagger.io/open-source/swagger-ui/','Swagger UI','overview/OAS/customization lines 12-60','Swagger UI generates interactive API documentation from OpenAPI and permits customization.','2026-11-21T04:14:57Z',['N002']),
 ('NCA03','https://wire-dsl.org/','WireDSL','introduction and first example lines 15-66','WireDSL defines wireframes with declarative code and produces image/document exports.','2026-11-21T04:14:57Z',['N003']),
 ('NCA08','https://builtwith.com/','BuiltWith','overview and technology coverage lines 25-68','BuiltWith provides web technology identification and claims broad developer-infrastructure coverage. This weakens a universal frontend-only exclusion.','2026-11-21T04:14:57Z',['N008']),
 ('NCA09','https://electrobun.dev/electrobun/','Electrobun','overview lines 7-34 and 93-98','Electrobun is a desktop application framework with macOS, Windows and Linux targets.','2026-11-21T04:14:57Z',['N009']),
 ('NCA13','https://docs.github.com/en/actions/concepts/runners/github-hosted-runners','GitHub-hosted runners','overview lines 18-42','GitHub-hosted virtual machines execute workflow jobs and commands. The question explicitly allows triggering commands on the home machine over SSH, so cloud execution alone is insufficient for strict exclusion.','2026-11-21T04:14:57Z',['N013']),
 ('NCA14','https://www.phpmyfaq.de/','phpMyFAQ','overview and feature/deployment sections lines 6-50','The FAQ product includes categories, attachments and permissions, and supports PHP with common SQL databases. No categorical incompatibility with the original request was established.','2026-11-21T04:14:57Z',['N014']),
 ('NCA19','https://www.anthropic.com/news/claude-4','Claude Sonnet 4 announcement','model discussion and Claude Code sections lines 60-87','This official announcement identifies Sonnet 4 and its coding/agent role. It does not establish current weight-download availability.','2026-11-21T04:15:29Z',['N019'])
]
for sid,url,title,section,confirmed,at,qids in entity_sources:
    src(sid,url,title,section,confirmed,
        'Current primary description, not an executed feasibility test or a historical-snapshot verification. Product superiority and marketing statistics are not adopted.',
        ['Q3']+qids,at=at)

positive_entities = {
 'N001':('https://getgreenshot.org/',['NCE01'],'official_body_read'),
 'N002':('https://github.com/sourcey/sourcey',['NCE02'],'official_body_read'),
 'N003':('https://plantuml.com/salt',['NCE03'],'official_body_read'),
 'N004':('https://pentaho.com/products/pentaho-data-integration/',['NCE04'],'official_body_read; edition_unresolved'),
 'N005':('https://caddyserver.com/',['NCE05'],'official_body_read'),
 'N006':('https://chromewebstore.google.com/detail/blocktube/bbeaicapbccfllodepmimpkgecanonai',['NCE06'],'publisher_description_read'),
 'N007':('https://postmarkapp.com/',['NCE07'],'official_body_read'),
 'N008':('https://www.wappalyzer.com/',['NCE08'],'official_body_read'),
 'N009':('https://tauri.app/',['NCE09'],'official_body_read'),
 'N010':('https://www.sshguard.net/',['NCE10'],'official_body_read'),
 'N011':('https://handy.computer/',['NCE11'],'official_body_read'),
 'N012':('https://www.fastmail.com/',['NCE12'],'official_body_read'),
 'N013':('https://woodpecker-ci.org/',['NCE13'],'official_body_read'),
 'N014':('https://pacificblue.software/articles/php-faq-system',[],'answer_link_only; official_page_open_failed'),
 'N015':('https://www.charlesproxy.com/documentation/tools/rewrite/',['NCE15'],'official_body_read'),
 'N016':('https://github.com/themartiancompany/crash-js/blob/82351a4c0f01cdc11b7595b6fc299e7b89c4a4f4/crash-js/crash-js#L723',[],'answer_link_only; official_page_open_DisabledError'),
 'N017':('https://brave.com/',['NCE17'],'official_body_read'),
 'N018':('https://www.fastmail.com/',['NCE12'],'official_body_read'),
 'N019':('https://opencode.ai/',['NCE19A','NCE19B'],'official_bodies_read; configured_model_unspecified'),
 'N020':('https://github.com/QwenLM/Qwen3.8/blob/main/README.md',['NCE20'],'official_body_read; exact_Q4_artifact_unresolved')}
auxiliaries = {
 'N002':('Swagger UI standalone','https://swagger.io/open-source/swagger-ui/',['NCA02']),
 'N003':('WireDSL','https://wire-dsl.org/',['NCA03']),
 'N008':('BuiltWith','https://builtwith.com/',['NCA08']),
 'N009':('Electrobun','https://electrobun.dev/electrobun/',['NCA09']),
 'N013':('GitHub-hosted runner','https://docs.github.com/en/actions/concepts/runners/github-hosted-runners',['NCA13']),
 'N014':('phpMyFAQ','https://www.phpmyfaq.de/',['NCA14']),
 'N016':('bash-parser','https://github.com/vorpaljs/bash-parser',['NCO13']),
 'N018':('Proton Mail','https://proton.me/support/custom-domain',['NCO11']),
 'N019':('Claude Sonnet 4','https://www.anthropic.com/news/claude-4',['NCA19','NCO20'])}

positive_names = {'N001':'Greenshot','N002':'Sourcey','N003':'PlantUML Salt','N004':'Pentaho','N005':'Caddy','N006':'BlockTube',
                  'N007':'Postmark','N008':'Wappalyzer','N009':'Tauri','N010':'sshguard','N011':'Handy','N012':'Fastmail',
                  'N013':'Woodpecker CI','N014':'PBS FAQ','N015':'Charles Proxy','N016':'Crash Javascript _from_bash_ass_array',
                  'N017':'Brave Browser','N018':'Fastmail','N019':'OpenCode + OpenRouter','N020':'Qwen3.8-27B Q4'}
negatives = {
 'N001':('Flameshot 14.0 release-candidate on Wayland',['NCO01','NCO02'],'active-window capture','Candidate platform-specific build cannot select the required target window. Optional platform preferences are not promoted to requirements.','confirmed_scoped','Candidate must keep its platform/build scope; this does not reject all Flameshot versions.'),
 'N004':('Apache NiFi upstream distribution',['NCO03','NCO04'],'open-source software prohibited','The upstream distribution is Apache-licensed open source.','confirmed','Commercial support does not remove the explicit open-source prohibition; accepted Pentaho edition must be assessed independently.'),
 'N005':('Microsoft IIS for Windows Server',['NCO05'],'Linux execution','The named native Windows Server web server conflicts with Linux deployment.','confirmed_scoped','Adding a Windows guest OS changes the candidate configuration and violates native Linux interpretation.'),
 'N006':('Pi-hole standalone DNS blocker',['NCO07'],'block ARTE channel while retaining other YouTube','DNS blocking cannot distinguish channels served on the same YouTube domain.','confirmed_scoped','A browser extension added to Pi-hole is a different composed candidate.'),
 'N007':('MailEnable Standard self-administered SMTP server',['NCO08'],'avoid running own SMTP server','The candidate is server software to install and administer, rather than a managed sending API.','confirmed_scoped','A third-party managed MailEnable hosting service is outside this exact control.'),
 'N010':('Fail2Ban official Python distribution',['NCO09'],'no Python dependency','The documented distribution explicitly requires Python or PyPy3.','confirmed','Do not confuse Fail2Ban with independent implementations such as fail2zig.'),
 'N011':('Wispr Flow',['NCO10'],'non-cloud/offline dictation','Official documentation says internet is required on every platform.','confirmed','Scope is offline availability, not transcription quality.'),
 'N012':('Proton Mail Free',['NCO11'],'custom email domain','A paid plan is required for custom domains.','confirmed_scoped','The free-plan qualifier must survive candidate normalization; paid Proton Mail is not this negative.'),
 'N015':('node-http-proxy Node.js library',['NCO12'],'avoid requiring a Node.js ecosystem','Its installation and programming interface require Node.js/npm.','confirmed_scoped','Question says should; repeat the metric with this constraint treated as a preference.'),
 'N017':('Apple Safari iOS application',['NCO16','NCO17'],'Android browser available through Google Play','Apple package requires iOS/iPadOS/visionOS; its native package cannot install as an Android app.','confirmed_scoped','An Android app reusing the Safari name is not Apple Safari.'),
 'N020':('gpt-oss-120b MXFP4 with all weights resident on GPU',['NCO18','NCO19'],'8GB GPU only, no CPU spill','The 117B-parameter MXFP4 model needs far more than 8GB for its full weights; documented reference deployment uses 80GB.','confirmed_scoped','Storage lower-bound inference, not an actual run; offloading or altered weights changes the scoped candidate.')}
unavailable = {
 'N002':('Swagger UI standalone', 'Mixed-document inputs are explicit, but proving impossibility across extensions/composition would require exact version/module support evidence. Do not turn a useful OpenAPI component into a false strict N.'),
 'N003':(None, 'The initial request has no explicit exclusion beyond markup-driven wireframing. A same-category impossibility could not be established without inventing a restriction.'),
 'N008':('BuiltWith or ChatGPT','Asker reports insufficient/hallucinated backend information, but official documentation establishing an exact hard-condition failure was not found.'),
 'N009':(None,'Broad Electron-alternative question has no hard exclusion. A different framework cannot be made a strict N merely for preference differences.'),
 'N013':('GitHub-hosted runner','A hosted runner can invoke SSH on the home machine, which the question explicitly permits. Rejecting it universally would ignore a valid composition.'),
 'N014':('phpMyFAQ','The asker dislikes its speed, bugs and feature count; no stable official categorical impossibility was established. PHP/MySQL are preferences.'),
 'N016':('bash-parser','MIT licensing and AST output are confirmed (NCO13), but a wrapper/compatible integration may solve the goal. Exact-AGPL wording needs interpretation; no legal incompatibility was asserted.'),
 'N018':(None,'Most criteria are preferences and polish is subjective. No same-category hard-condition violation was justified.'),
 'N019':('Claude Sonnet 4','NCO20 calls it closed-source at the study date, but current weight-release status and harness/model distinction were not conclusively checked.')}

checks = []
for q in qs:
    qid = q['id']; name = positive_names[qid]
    grow = next(r for r in gold if r['qid']==qid and r['candidate']==name)
    entity_url,entity_sids,entity_status=positive_entities[qid]
    checks.append({'qid':qid,'slot':'positive','candidate':name,'candidate_url':entity_url,'candidate_url_status':entity_status,'grade':grow['grade'],'status':'external_record_confirmed','origin':'external answer record, worker mapping','evidence_url':grow['evidence_url'],'source_ids':['NQ-'+qid]+entity_sids, 'note':grow['note']})
    if qid in negatives:
        name,sids,condition,reason,status,limit=negatives[qid]
        entity_url=next(s['url'] for s in sources if s['id']==sids[-1])
        checks.append({'qid':qid,'slot':'strict_near_miss','candidate':name,'candidate_url':entity_url,'grade':'N','status':status,'origin':'작업자 구성','source_ids':sids,'violated_condition':condition,'question_position':q['source_position'],'reason':reason,'limits':limit,'checked_at_utc':interval,'strict_N_count_eligible':True,'requires_parent_freeze_review':True})
    else:
        name,reason=unavailable[qid]
        aux_name,aux_url,aux_sids=auxiliaries[qid]
        checks.append({'qid':qid,'slot':'auxiliary_unjudged','requested_slot':'strict_near_miss','candidate':aux_name,'candidate_url':aux_url,'source_ids':aux_sids,'attempted_candidate':name,'grade':None,'status':'auxiliary_unjudged','strict_N_status':'unavailable','origin':'worker attempted construction; auxiliary identity verified','reason':reason,'strict_N_count_eligible':False,'positive_rejection_count_eligible':False,'all_three_requested_roles_met':False,'next_first_action':'Confirm a precise same-category impossibility using an official scoped document, or retain this question as N-ineligible. Judge this auxiliary for completeness but exclude it from both strict-N and positive-rejection denominators.'})
    i,dis=next((i,d) for i,d in enumerate(distractions,1) if d[0]==qid)
    checks.append({'qid':qid,'slot':'irrelevant','candidate':dis[1],'candidate_url':dis[2],'grade':'0','status':'official_product_role_read','origin':'작업자 구성','source_ids':['NCD%02d'%i],'reason':dis[3],'strict_N_count_eligible':False})
write('checks-draft.json',{'status':'draft; parent must freeze before any worker run','created_at_utc':now,'rows':checks,
      'counts':{'slots':len(checks),'positive':20,'irrelevant':20,'confirmed_scoped_N':len(negatives),'N_unavailable':len(unavailable),'auxiliary_unjudged':len(unavailable)},
      'limits':['Eleven scoped strict-N proposals have primary evidence; nine requested N roles remain explicitly unavailable, with separate unjudged auxiliary candidates for actual three-candidate judgments.', 'Grade-0 category negatives and auxiliaries are never substituted for strict N. Auxiliary decisions are excluded from both strict-N and positive-rejection denominators.',
                'Positive controls can have adoption/initial-constraint conflicts; do not replace external grade 2 with a constraint judgment.']})
excluded=[
 {'url':'https://www.postfix.org/overview.html','reason':'web open inaccessible; no body evidence','level':'excluded'},
 {'url':'https://www.postfix.org/','reason':'web open HTTP 402; not retried','level':'excluded'},
 {'url':'https://www.backblaze.com/blog/b2-and-the-backblaze-datacenter/','reason':'web open inaccessible; used separately accessible current product documentation instead','level':'excluded'},
 {'url':'https://support.apple.com/en-us/102665','reason':'web open HTTP 429; not retried','level':'excluded'},
 {'url':'https://www.openpbs.org/','reason':'web open timeout (tool status 400); official GitHub project description used','level':'excluded'},
 {'url':'https://music.youtube.com/','reason':'Only deprecated-browser notice; no product body evidence','level':'excluded'},
 {'url':'https://pacificblue.software/articles/php-faq-system','reason':'web open inaccessible; exact product URL retained from the accepted answer only','level':'excluded','accessed_at_utc':'2026-11-21T04:15:14Z'},
 {'url':'https://github.com/themartiancompany/crash-js/blob/82351a4c0f01cdc11b7595b6fc299e7b89c4a4f4/crash-js/crash-js','reason':'web open DisabledError; exact product/code URL retained from accepted answer only; not bypassed','level':'excluded','accessed_at_utc':'2026-11-21T04:15:14Z'}]
for q in read('supplementary-reddit-questions.json'):
    src('NQ-'+q['id'],q['url'],'Supplementary Reddit recommendation '+q['platform_id'],q['source_position'],q['summary'],
        'Body and replies were directly read, but absolute creation date is search-extracted only. Excluded from the new-question count. Current body is not the initial revision.', ['Q2',q['id']],kind='public_community_question',at=q['read_at_utc'])
for r in read('reddit-date-html.json'):
    excluded.append({'url':r['url'],'reason':'HTML 200 bootstrap contains no question body or date metadata; does not confirm the indexed absolute date','level':'D3-fetch','accessed_at_utc':r['accessed_at_utc']})
write('sources-draft.json',{'sources':sources,'excluded':excluded,'timestamp_note':'API and normal-HTML fetch timestamps are exact request-start observations. Earlier web-tool body reads are bounded by a session interval because exact wall-clock seconds were not retained; no precise times were invented.', 'count_note':'Question, answer, product, and probe sources are execution/sample evidence, not method/comparison-literature quota items.'})
print(json.dumps({'source_entries':len(sources),'probe_slots':len(checks),'verified_scoped_N':len(negatives),'unavailable_N':len(unavailable)}))
