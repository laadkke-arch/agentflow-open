function hash(s){let K=[],H=[],p=2;while(K.length<64){let prime=true;for(let j=2;j*j<=p;j++)if(p%j===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(p)%1)*2**32|0);K.push((Math.cbrt(p)%1)*2**32|0)}p++}let a=Array.from(unescape(encodeURIComponent(s)),x=>x.charCodeAt(0)),bits=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(bits/256**j)%256);let r=(x,n)=>(x>>>n)|(x<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w.push(a[i+4*j]<<24|a[i+4*j+1]<<16|a[i+4*j+2]<<8|a[i+4*j+3]);for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(r(x,7)^r(x,18)^(x>>>3))+w[j-7]+(r(y,17)^r(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,I]=H;for(let j=0;j<64;j++){let t1=(I+(r(E,6)^r(E,11)^r(E,25))+((E&F)^(~E&G))+K[j]+w[j])|0,t2=((r(A,2)^r(A,13)^r(A,22))+((A&B)^(A&C)^(B&C)))|0;I=G;G=F;F=E;E=(D+t1)|0;D=C;C=B;B=A;A=(t1+t2)|0}H=H.map((x,j)=>(x+[A,B,C,D,E,F,G,I][j])|0)}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}

const seed="AF-RES-136|fixed|2026-11-24|blind-v1";
const F=["operation","preserve","exception","hold"];
const check=(b,m)=>{if(!b)throw Error(m)};
const jsonl=s=>s.trim().split(/\n/).map(JSON.parse);
function project(answers, assignments, packets, n=6){
  check(answers.length===n*3 && assignments.length===n,"expected 3 answers/case");
  check(new Set(assignments.map(a=>a.slot)).size===n,"duplicate assignment slot");
  check(new Set(assignments.map(a=>a.answer_id)).size===n,"duplicate request id");
  const req=[], rows=[], map=[];
  for(const a of assignments){
    const hits=packets.filter(x=>x.id===a.answer_id);
    check(hits.length===1 && typeof hits[0].request==="string","packet join");
    const request=hits[0].request;
    const r="R-"+hash(seed+"|request|"+a.answer_id).slice(0,10);
    req.push({request_alias:r,request});
    const aa=answers.filter(x=>x.slot===a.slot);
    check(aa.length===3 && new Set(aa.map(x=>x.phase)).size===3,"phase/slot join");
    for(const x of aa){
      check(F.every(k=>typeof x[k]==="string"),"answer field type");
      const blind="B-"+hash(seed+"|answer|"+x.slot+"|"+x.phase+"|"+x.id).slice(0,10);
      const body=Object.fromEntries(F.map(k=>[k,x[k]]));
      const row={alias:blind,request_alias:r,...body};
      check(Object.keys(row).join(",")==="alias,request_alias,"+F.join(","),"allowlist");
      rows.push(row);
      map.push({alias:blind,request_alias:r,slot:x.slot,phase:x.phase,id:x.id,answer_id:a.answer_id,request_hash:hash(request),request_chars:[...request].length,field_receipts:Object.fromEntries(F.map(k=>[k,{sha256:hash(x[k]),chars:[...x[k]].length}])),row_sha256:hash(JSON.stringify(x))});
    }
  }
  check(new Set(rows.map(x=>x.alias)).size===n*3,"alias collision");
  check(new Set(req.map(x=>x.request_alias)).size===n,"request alias collision");
  const rank=(tag,x)=>hash(seed+"|order|"+tag+"|"+x);
  rows.sort((a,b)=>rank("answer",a.alias).localeCompare(rank("answer",b.alias)));
  req.sort((a,b)=>rank("request",a.request_alias).localeCompare(rank("request",b.request_alias)));
  map.sort((a,b)=>rows.findIndex(x=>x.alias===a.alias)-rows.findIndex(x=>x.alias===b.alias));
  return {req,rows,map,assignment_hash:hash(JSON.stringify(map)),request_hash:hash(JSON.stringify(req)),answer_hash:hash(JSON.stringify(rows))};
}
function synthetic(){
  const a=[0,1,2].map(phase=>({slot:9,id:"i",phase,operation:"exact😀",preserve:"p",exception:"e",hold:"h",previous_score:"hidden",url:"hidden"}));
  const b=[{slot:9,answer_id:"p"}],c=[{id:"p",request:"test",answer:"secret",views:["hidden"]}];
  const t=project(a,b,c,1);
  check(t.rows.length===3&&t.rows.every(x=>x.operation==="exact😀"&&!Object.hasOwn(x,"previous_score")&&!Object.hasOwn(x,"url")),"projection");
  check(t.req[0].request==="test"&&Object.keys(t.req[0]).length===2,"request only");
  let rejected=false;try{project([a[0],a[0],a[2]],b,c,1)}catch(e){rejected=true}check(rejected,"duplicate phase accepted");
  rejected=false;try{project(a,b,[...c,...c],1)}catch(e){rejected=true}check(rejected,"duplicate packet accepted");
  check(hash("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","SHA-256 known answer");
  return {passed:true,tests:["3 phase exact","allowlist","duplicate phase reject","duplicate packet reject","SHA256 abc"],note:"metadata hidden; semantic clues not removed"};
}
