"""Read linked .blend structure with auto-execution disabled; do not save source files."""
import bpy,json,sys,datetime,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[2];output=[]
for bid,role in [('vWxY64rZ','original author preproposal file'),('oDnRekJL','proposer example')]:
 p=P/'.cache/auxiliary-followup'/('blend-file-'+bid+'.bin');bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False)
 r={'bid':bid,'role':role,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reader_runtime':bpy.app.version_string,'bpy_data_file_version_tuple':list(bpy.data.version),'objects':[],'node_groups':[],'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'structural read only; no simulation run or rendered output; current fetched file version not independently historical'}
 for o in bpy.data.objects:r['objects'].append({'name':o.name,'type':o.type,'location':list(o.location),'rotation':list(o.rotation_euler),'vertices':len(o.data.vertices) if o.type=='MESH' else None,'has_animation_data':bool(o.animation_data),'geometry_modifiers':[m.node_group.name if m.node_group else None for m in o.modifiers if m.type=='NODES']})
 for tree in bpy.data.node_groups:
  nodes=[]
  for n in tree.nodes:
   if n.bl_idname in ['FunctionNodeCompare','FunctionNodeAlignEulerToVector','GeometryNodeSimulationInput','GeometryNodeSimulationOutput']:
    d={'name':n.name,'type':n.bl_idname}
    for a in ['axis','pivot_axis','data_type','mode','operation']:
     if hasattr(n,a):d[a]=getattr(n,a)
    vals=[]
    for i in n.inputs:
     if hasattr(i,'default_value') and not i.is_linked:
      v=i.default_value
      try:v=list(v)
      except TypeError:pass
      if isinstance(v,(str,float,int,bool,list)) or v is None:vals.append({'name':i.name,'identifier':i.identifier,'value':v})
    d['unlinked_inputs']=vals;nodes.append(d)
  r['node_groups'].append({'name':tree.name,'node_count':len(tree.nodes),'node_types':sorted(set(n.bl_idname for n in tree.nodes)),'relevant_nodes':nodes})
 output.append(r)
(P/'evidence/auxiliary-followup/blend-inspection.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');print(json.dumps(output,ensure_ascii=False))
