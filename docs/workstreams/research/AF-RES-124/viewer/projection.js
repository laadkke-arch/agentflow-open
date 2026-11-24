// Execute inside connector filter; never emit unprojected rows.
const parse = s => s.trim().split("\n").map(JSON.parse);
const natural = (rows, id, view) => {
  const matches=rows.filter(r=>r.layer==="natural"&&r.case_id===id&&r.view===view);
  if(matches.length!==1) throw Error("not unique");
  return matches[0];
};
const initial=(rows,ids)=>ids.map(case_id=>({case_id,issue_body:natural(rows,case_id,"B").issue_body}));
const link=(rows,id,view,i)=>{const {title,url}=natural(rows,id,view).links[i];return {title,url}};
const fields=["anchor_url","first_line","last_line","offset","end","characters","body"];
const page=(rows,url,offset=null)=>{
 const hits=rows.filter(r=>r.source_start_anchor===url&&(offset===null||r.offset===offset)).sort((a,b)=>a.offset-b.offset);
 if(!hits.length)return null;
 const r=hits[0];
 if(r.characters>1500||[...r.body].length>1500)throw Error("over budget");
 return Object.fromEntries(fields.map(k=>[k,r[k]]));
};
