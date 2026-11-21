#!/usr/bin/env python3
"""Encode external answer records separately from search-worker question input."""
import datetime
import json
import pathlib

P = pathlib.Path(__file__).resolve().parent
questions = json.loads((P / 'new-questions.json').read_text())
qmap = {q['id']:q for q in questions}
rows = []

def add(qid, grade, names, answer_id, note='Substantive answer candidate; no candidate-specific rebuttal observed.'):
    for name in names.split('|'):
        q = qmap[qid]
        if q['platform'] == 'softwarerecs':
            url = 'https://softwarerecs.stackexchange.com/a/' + str(answer_id)
        elif q['platform'] == 'hackernews':
            url = 'https://news.ycombinator.com/item?id=' + str(answer_id)
        else:
            url = q['url'] + '#discussioncomment-' + str(answer_id)
        rows.append({'qid':qid,'candidate':name,'grade':str(grade),'answer_id':str(answer_id),'evidence_url':url,
                     'note':note,'judge':'worker applying AF-RES-014 rules to external public answer records',
                     'record_type':'external answer/use record, worker entity mapping','observed_through_utc':'2026-11-21',
                     'constraint_compliance_is_separate':True,'product_claims_independently_verified':False})

add('N001',1,'Greenshot',95815)
add('N001',1,'CaptureGraphicsWin2D',95806)
add('N001',1,'Spectacle',95799)
add('N002',1,'Sourcey',95779,'Two answers name the same product (95779, 95796); count once. Community recommendation does not verify the advertised mixed-source support.')
add('N003',2,'PlantUML Salt',95774,'Accepted answer ID in Stack Exchange API.')
add('N003',1,'WireDSL',95773)
add('N004',2,'Pentaho',95542,'Accepted answer; edition unspecified. Preserve grade 2 separately from no-open-source constraint and commercial-support interpretation.')
add('N004',1,'Debezium with Red Hat support',95541,'Commercial support recommendation; no explicit reply refuting it. Open-source prohibition can conflict with this answer, so keep the independent constraint label.')
add('N005',2,'Caddy',95593,'Accepted self-answer reports finding and configuring Caddy; minimalism relaxed and Alpine replaced by Ubuntu. This is an adoption/initial-requirement mismatch, not a reason to erase grade 2.')
add('N006',1,'BlockTube|YouTube Channel Blocker|ReVanced',95528)
add('N006',1,'SmartFilter',95705,'Developer self-recommendation; no adoption evidence. Treat as grade 1 only.')
add('N007',1,'Postmark',48358203)
add('N007',0,'SendGrid',48358203,'Answer explicitly recommends against this provider.')
add('N007',1,'Amazon SES',48358368)
add('N007',1,'GoodSender',48358552)
add('N007',1,'Resend',48360028)
add('N008',1,'Bloomberry|Wappalyzer',48942919)
add('N008',0,'ChatGPT',48885847,'Asker says it hallucinated and only gave frontend stack information; this is observed refutation, not an official universal impossibility claim.')
add('N009',1,'Tauri|Electrobun|React Native Desktop|Flutter',49478059)
add('N009',1,'iced|egui',49478167)
add('N009',1,'MoBrowser|Wails',49478425)
add('N009',1,'Dioxus Native',49479578)
add('N009',1,'Electron',49481432,'Existing product defended as a practical answer; original question does not expressly forbid it.')
add('N009',1,'Slint',49481704)
add('N009',1,'Sciter',49482707)
add('N009',1,'pywebview',49485567)
add('N009',1,'Avalonia UI',49486214)
add('N009',1,'wry + winit',49494055)
add('N010',2,'sshguard',49483633,'Asker replaced fail2ban on one machine; 49484417 reports working and a dozen binaries, 49519572 continued satisfaction. The one-binary request and adoption record conflict.')
add('N010',1,'OpenSSH 10+ native blocking approach',49477786)
add('N010',1,'fail2zig',49501943)
add('N010',1,'WireGuard|Tailscale',49509683,'Alternative exposure-control approach rather than a drop-in log-ban daemon; judge role and initial constraints separately.')
add('N011',1,'FluidVoice',49809811)
add('N011',1,'Handy|VoiceInk|Glimpse',49809997)
add('N011',1,'Clarifyfor.me',49810392)
add('N011',1,'Monologue|Superwhisper',49810496)
add('N011',1,'MacWhisper',49810525)
add('N011',1,'Careless Whisper',49810609)
add('N011',1,'Scribe (resolveworks)',49810675)
add('N011',1,'yapsnap',49810798)
add('N011',1,'HEX (anomalyco)',49812991)
add('N011',1,'OpenSuperWhisper',49815368)
add('N011',1,'Rambler|Eloquence',49815789,'Recommended mobile dictation options; exact product/version identity needs separate validation.')
add('N011',1,'Typewave AI',49816417)
add('N012',1,'Fastmail|iRedMail|Mailcow',49261740)
add('N012',1,'Proton Mail + Bridge',49261773,'Asker considers price and export; no explicit use report.')
add('N012',1,'Infomaniak',49261871)
add('N012',1,'iCloud+',49262583,'Asker later says not an Apple user; this is a compatibility caveat, not proof the service cannot work.')
add('N013',1,'Argo Events + Argo Workflows on k3s',48583456)
add('N013',1,'GitHub Actions self-hosted runner',48583468)
add('N013',1,'GitLab CI',48584159)
add('N013',1,'Woodpecker CI',48584304)
add('N013',1,'Gitea Actions',48585637)
add('N013',1,'Jenkins',48588114)
add('N013',1,'Forgejo Actions|Tekton',48589380)
add('N014',2,'PBS FAQ',95729,'Accepted self-answer: asker wrote and deployed the requested FAQ replacement. Product claims in the answer are not yet independently checked.')
add('N015',2,'Charles Proxy',95482,'Accepted answer recommends the response rewrite tool; price was not a mandatory free requirement in this question.')
add('N016',2,'Crash Javascript _from_bash_ass_array',95474,'Accepted self-answer reports writing the requested function; source links identify function revisions.')
add('N017',1,'Google Chrome',50176757)
add('N017',1,'Brave Browser',50178557)
add('N017',1,'Firefox with refresh menu/pull-to-refresh',50176791,'Answer corrects the claimed missing function; no asker response establishes whether the specific bug was solved.')
add('N017',0,'IronFox',50176634,'Recommender explicitly admits absence from Play Store, in conflict with the named distribution requirement; retain as proposed negative, not unqualified grade 1.')
add('N018',1,'Fastmail',50110037)
add('N018',1,'ByteMail',50270244)
add('N018',1,'Scape',50285740)
add('N019',1,'Cursor|Pi',50326653)
add('N019',1,'OpenCode + OpenRouter|Hermes',50325704,'Harness alternatives; a harness has no model weights. Open-weight requirement must be checked on the configured model, not the harness license.')
add('N019',1,'GLM-5.x|Kimi 3.x',50327601,'Model family names preserved as stated; not independently verified as current release identities.')
add('N019',1,'DeepSeekHarness + DeepSeek Flash',50327614)
add('N019',1,'OpenCode Go plan',50325749)
add('N020',1,'LFM2-1.2B-Extract',17516963)
add('N020',1,'LFM2.5-8B-A1B|Gemma 4 12B',19558148,'Candidate models suggested for testing; answer itself flags tight 8GB fit for Gemma. No benchmark execution or independent fit validation.')
add('N020',2,'Qwen3.8-27B Q4',19588781,'Asker explicitly reports using it after buying an RTX 3090 with 24GB VRAM. Adopted outcome changes the original fixed-hardware setting; do not relabel outcome as nonadoption. Official Qwen README NCE20 dates the model release 2026-08-14, later than the 2026-07-02 question; report a question-date-availability sensitivity separately.')

doc = {'rules_sha':'42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9','rules_path':'docs/workstreams/research/AF-RES-014/qrels/RULES.md',
       'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'draft for parent review before gold freeze',
       'source':'external answers/use records with worker candidate mapping','rows':rows,
       'limits':['Historical relevance is different from current feasibility or claim truth.', 'Comments offering only thanks or future intent were not promoted to grade 2.',
                 'HN reply trees were read recursively. GitHub page includes 4 comments and 2 replies; earlier revisions were unavailable.',
                 'Grade 1 recall denominator can include conditional/component recommendations; parent should retain explicit role annotations.',
                 'The initial question and later selected outcome can describe different constraints. Report sensitivity rather than overwrite either source.']}
(P/'gold-draft.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'gold_rows':len(rows),'grade2':sum(r['grade']=='2' for r in rows),'questions':len({r['qid'] for r in rows})}))
