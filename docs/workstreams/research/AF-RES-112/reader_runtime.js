// AF-RES-112 bounded web-view reader. Evaluated only inside functions.exec.
// API: await readerOp({session:'r01', action:'start'|'open'|'next'|'back'|'click'|'judge'|'finish', ...})
// All page data stays inside program memory except emitted, counted slices.
globalThis.readerOp = async function (arg) {
  const root = '/workspace/scratch/5c61d6dbe4ea/agentflow-open/docs/workstreams/research/AF-RES-112';
  if (!/^r[0-9]{2}$/.test(arg.session)) throw new Error('invalid session');
  const dir = root + '/readers/' + arg.session;
  const key = 'af112-reader-' + arg.session;
  let s = load(key);
  const cp = x => Array.from(x);
  const utf8 = x => encodeURIComponent(x).replace(/%[A-F\d]{2}/g, 'x').length;
  async function writeEvent(obj) {
    s.events = (s.events || 0) + 1;
    const value = {...obj, session:arg.session, at_utc:new Date().toISOString()};
    const body = JSON.stringify(value, null, 2) + '\n';
    const path = dir + '/events/' + String(s.events).padStart(2, '0') + '.json';
    const p = '*** Begin Patch\n*** Add File: ' + path + '\n' + body.split('\n').map(l => '+'+l).join('\n') + '\n*** End Patch';
    const saved=await tools.apply_patch(p);
    if (saved && saved.isError) throw new Error('event saving failed');
    store(key,s);
  }
  function parse(result, requested) {
    const raw = result.content.filter(c=>c.type==='text').map(c=>c.text).join('\n');
    const ref = raw.match(/【(turn[^】\s]+(?:view|search)[^】\s]*)】/);
    const total = raw.match(/Total lines:\s*(\d+)/);
    const lines = [...raw.matchAll(/^L(\d+): ?(.*)$/gm)].map(m=>({line:Number(m[1]),text:m[2]}));
    const arrivalMatch = raw.match(/^[^\n]*\((https?:\/\/[^\n]+)\)\s*$/m);
    const arrival = arrivalMatch ? arrivalMatch[1] : requested;
    let body = lines.length ? lines.map(l=>l.text).join('\n') : raw;
    return {ref:ref?ref[1]:null,requested,arrival,arrival_confirmed:!!arrivalMatch,total_lines:total?Number(total[1]):null,lines,body,cursor:0,source_raw:raw,fragment_resolution:'unverified',visible_ids:[]};
  }
  function locate(page, pos) {
    let offset=0;
    for (const line of page.lines) {
      const n=cp(line.text).length+1;
      if(pos<offset+n) return {line:line.line,column:pos-offset};
      offset+=n;
    }
    return {line:page.lines.length?page.lines[page.lines.length-1].line:null,column:null};
  }
  async function getPage(url) {
    if(/^https:\/\/github\.com\/.*\.zip$/.test(url)) return await getArchive(url,null);
    const github=url.match(/^https:\/\/github\.com\/([^/]+)\/([^/#]+)(?:\/(.*))?$/);
    if(!github) {
      return parse(await tools.mcp__codex_apps__search_service_web_run({open:[{ref_id:url}],response_length:'long'}),url);
    }
    const owner=github[1], repo=github[2], tail=github[3]||'';
    let result, transport=url, links={};
    if(!tail || tail.startsWith('tree/')) {
      const m=tail.match(/^tree\/([^/]+)(?:\/(.*))?$/);
      transport='https://api.github.com/repos/'+owner+'/'+repo+'/contents'+(m&&m[2]?'/'+m[2]:'')+(m?'?ref='+encodeURIComponent(m[1]):'');
      result=await tools.mcp__codex_apps__github_fetch({link_id:'link_6afeba07d38881919e7e632c521ab112',url:transport});
      let entries;
      try {entries=JSON.parse(result.structuredContent.content);}catch(e){entries=null;}
      if(Array.isArray(entries)) {
        const listing=['# '+owner+'/'+repo+(m&&m[2]?'/'+m[2]:''),'Repository directory listing.'];
        entries.forEach((entry,i)=>{links[i]=entry.html_url;listing.push('【'+i+'†'+entry.name+'】 '+entry.type+' ('+entry.html_url+')');});
        const body=listing.join('\n');
        return {ref:null,requested:url,arrival:url,arrival_confirmed:true,total_lines:listing.length,lines:listing.map((text,line)=>({line:line+1,text})),body,cursor:0,source_raw:body,transport_url:transport,transport:'GitHub contents API rendered directory',link_targets:links,fragment_resolution:'unverified',visible_ids:[]};
      }
    } else if(tail.startsWith('blob/')) {
      const m=tail.match(/^blob\/([^/]+)\/(.*?)(?:#.*)?$/);
      if(m) result=await tools.mcp__codex_apps__github_fetch_file({link_id:'link_6afeba07d38881919e7e632c521ab112',repository_full_name:owner+'/'+repo,ref:m[1],path:m[2]});
    }
    if(!result) result=await tools.mcp__codex_apps__github_fetch({link_id:'link_6afeba07d38881919e7e632c521ab112',url});
    const data=result.structuredContent||{};
    const body=data.error||data.content||result.content.filter(x=>x.type==='text').map(x=>x.text).join('\n');
    const lines=body.split('\n').map((text,line)=>({line:line+1,text}));
    return {ref:null,requested:url,arrival:data.display_url||url,arrival_confirmed:!!data.display_url,total_lines:lines.length,lines,body,cursor:0,source_raw:body,transport_url:transport,transport:'GitHub connector source view',source_blob_sha:data.sha||null,link_targets:links,fragment_resolution:'unverified',visible_ids:[],retrieval_error:!!(result.isError||data.error)};
  }
  async function getArchive(url,entry) {
    const shell=s=>"'"+s.replace(/'/g,"'\\''")+"'";
    let command='timeout 28s python -B '+shell(root+'/read_archive.py')+' '+shell(arg.session)+' '+shell(url);
    if(entry!==null) command+=' --entry '+shell(entry);
    let receipt=await tools.exec_command({cmd:command,yield_time_ms:1000,max_output_tokens:12000});
    let stdout=receipt.output;
    while(receipt.session_id) {
      receipt=await tools.write_stdin({session_id:receipt.session_id,chars:'',yield_time_ms:1000,max_output_tokens:12000});
      stdout+=receipt.output;
    }
    let result;
    try {result=JSON.parse(stdout);}catch(e){result={error:'archive retrieval did not return complete JSON; exit '+receipt.exit_code};}
    let body, targets={};
    if(result.entries) {
      const rows=['# ZIP directory'];
      result.entries.forEach((x,i)=>{targets[i]=x.name;rows.push('【'+i+'†'+x.name+'】 '+x.bytes+' bytes');});
      if(result.listing_truncated) rows.push('Listing limit reached.');
      body=rows.join('\n');
    } else body=result.text||result.error||'No decoded text';
    const lines=body.split('\n').map((text,line)=>({line:line+1,text}));
    return {ref:null,requested:url,arrival:result.metadata?.arrival_url||url,arrival_confirmed:!!result.metadata,total_lines:lines.length,lines,body,cursor:0,source_raw:body,transport:'bounded ZIP directory or UTF-8 entry',transport_url:url,source_blob_sha:result.source_sha256||result.metadata?.sha256||null,archive_metadata:result.metadata||null,archive_url:url,archive_entry:entry,archive_targets:targets,link_targets:{},fragment_resolution:'not_applicable_archive',visible_ids:[],retrieval_error:!!result.error};
  }
  if(arg.action==='start') {
    if(s) throw new Error('session already initialized');
    const read=await tools.exec_command({cmd:'cat '+dir+'/input.json',max_output_tokens:5000});
    if(read.exit_code!==0) throw new Error('packet missing');
    const input=JSON.parse(read.output);
    s={input,opens:0,chars:0,bytes:0,events:0,awaiting_judgment:false,finished:false,page:null,pages_by_step:{}};
    await writeEvent({type:'start',input,model:'inherited GPT-6 Astra Pro; exact provider runtime not exposed',context:'fork_turns=none',allowed_operations:['open','next','back','click','judge','finish']});
    text({request:input.request,url:input.url,hint:input.hint||'',budget:{opens:3,codepoints:4500,per_open:1500},instructions:'First action open. After each exposure submit judge before moving. click requires a visible numeric link id. No search/find/guessed URL or other file access. Cite source-view coordinates. final answer once.'});
    return;
  }
  if(!s || s.finished) throw new Error('inactive session');
  if(arg.action==='judge') {
    if(!s.awaiting_judgment) throw new Error('no unjudged exposure');
    if(!['바로 사용','조건부','부적합','보류'].includes(arg.disposition)) throw new Error('invalid disposition');
    await writeEvent({type:'judgment',step:s.opens,disposition:arg.disposition,answer:arg.answer,citations:arg.citations||[],counterexample:arg.counterexample||'',unknown:arg.unknown||'',prior_knowledge:arg.prior_knowledge||'',next_action:arg.next_action||'',reason:arg.reason||''});
    s.awaiting_judgment=false;store(key,s);text({saved:true,step:s.opens,remaining_opens:3-s.opens,remaining_characters:4500-s.chars});return;
  }
  if(arg.action==='finish') {
    if(s.awaiting_judgment) throw new Error('judge before finishing');
    await writeEvent({type:'final',opens:s.opens,codepoints:s.chars,utf8_bytes:s.bytes,disposition:arg.disposition,answer:arg.answer,citations:arg.citations||[],counterexample:arg.counterexample||'',unknown:arg.unknown||'',prior_knowledge:arg.prior_knowledge||'',stop_reason:arg.stop_reason||'',early_stop_positions:3-s.opens});
    s.finished=true;store(key,s);text({saved:true,complete:true,opens:s.opens,characters:s.chars,utf8_bytes:s.bytes});return;
  }
  if(s.awaiting_judgment) throw new Error('must save judgment before next opening');
  if(s.opens>=3 || s.chars>=4500) throw new Error('budget exhausted');
  const reason=arg.reason||'';
  if(!reason) throw new Error('action reason required');
  let fetched=false, error=null;
  const prior=s.page;
  if(arg.action==='open') {
    if(s.opens!==0) throw new Error('open only allowed initially');
    await writeEvent({type:'choice',next_step:s.opens+1,action:'open',requested_url:s.input.url,reason});
    s.page=await getPage(s.input.url);fetched=true;
  } else if(arg.action==='next' || arg.action==='back') {
    if(!s.page) throw new Error('no document');
    await writeEvent({type:'choice',next_step:s.opens+1,action:arg.action,requested_url:s.page.arrival,reason});
    if(arg.action==='back') s.page.cursor=Math.max(0,s.page.cursor-3000);
    if(s.page.cursor>=cp(s.page.body).length) {
      const last=s.page.lines.length?s.page.lines[s.page.lines.length-1].line:null;
      if(last!==null && s.page.total_lines!==null && last+1<s.page.total_lines) {
        const r=await tools.mcp__codex_apps__search_service_web_run({open:[{ref_id:s.page.ref||s.page.arrival,lineno:last+1}],response_length:'long'});
        s.page=parse(r,s.page.arrival);fetched=true;
      } else {error='end of available rendered source view';}
    }
  } else if(arg.action==='click') {
    const source=arg.from_step?s.pages_by_step[Number(arg.from_step)]:s.page;
    if(!source || (!source.ref && !source.link_targets) || !source.visible_ids.includes(Number(arg.id))) throw new Error('link was not visible in selected earlier source view');
    await writeEvent({type:'choice',next_step:s.opens+1,action:'click',link_id:Number(arg.id),from_step:arg.from_step||null,source_ref:source.ref,requested_url:source.arrival,reason});
    const archiveClick=!!(source.archive_targets && source.archive_targets[Number(arg.id)]);
    if(archiveClick) s.page=await getArchive(source.archive_url,source.archive_targets[Number(arg.id)]);
    else if(source.link_targets && source.link_targets[Number(arg.id)]) s.page=await getPage(source.link_targets[Number(arg.id)]);
    else {
      const r=await tools.mcp__codex_apps__search_service_web_run({click:[{ref_id:source.ref,id:Number(arg.id)}],response_length:'long'});
      s.page=parse(r,source.arrival);
    }
    fetched=true;
    const host=u=>{const m=u.match(/^https?:\/\/([^/#?]+)/);return m?m[1].replace(/^www\./,''):null;};
    if(!archiveClick && host(s.page.arrival)!==host(s.input.url)) error='off-site arrival rejected; no destination body exposed';
  } else throw new Error('unsupported action');
  s.opens++;
  const page=s.page;
  const start=page.cursor;
  const remaining=Math.min(1500,4500-s.chars);
  const shown=error?cp(error).slice(0,remaining).join(''):cp(page.body).slice(start,start+remaining).join('');
  const end=start+cp(shown).length;
  page.cursor=error?start:end;
  for(const m of shown.matchAll(/【(\d+)†/g)) if(!page.visible_ids.includes(Number(m[1])))page.visible_ids.push(Number(m[1]));
  s.pages_by_step[s.opens]=page;
  s.chars+=cp(shown).length;s.bytes+=utf8(shown);s.awaiting_judgment=true;
  const event={type:'exposure',step:s.opens,action:arg.action,requested_url:page.requested,arrival_url:page.arrival,arrival_confirmed:page.arrival_confirmed,fragment:(page.arrival.split('#')[1]||''),fragment_resolution:page.fragment_resolution,source_ref:page.ref,transport:page.transport||'web source service',transport_url:page.transport_url||null,source_blob_sha:page.source_blob_sha||null,archive_metadata:page.archive_metadata||null,archive_entry:page.archive_entry||null,source_view_start:locate(page,start),source_view_end:locate(page,end),capture_codepoint_start:start,capture_codepoint_end:error?start:end,exposed_codepoints:cp(shown).length,exposed_utf8_bytes:utf8(shown),cumulative_codepoints:s.chars,cumulative_utf8_bytes:s.bytes,visible_link_ids:page.visible_ids,source_service_call:fetched,reexposure_possible:arg.action==='back',error:error||(page.retrieval_error?'source retrieval failed':null),exposed_text:shown};
  await writeEvent(event);
  text(event);
};
