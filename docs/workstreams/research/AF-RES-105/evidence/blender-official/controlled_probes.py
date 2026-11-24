"""Small Blender 4.3.2 probes, not reconstruction of a requester's environment.

Run: blender --background --factory-startup --disable-autoexec --python THIS
Only generated in-memory geometry is changed. No .blend is saved.
"""
from pathlib import Path
import datetime as dt
import json
import math
import traceback
import bpy
from mathutils import Euler, Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence/blender-official'

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def obj(name,coords,faces=()):
    mesh=bpy.data.meshes.new(name+'Mesh');mesh.from_pydata(coords,[],faces);mesh.update()
    value=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(value)
    return value

def graph(object,name):
    tree=bpy.data.node_groups.new(name,'GeometryNodeTree')
    tree.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
    tree.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    source=tree.nodes.new('NodeGroupInput');sink=tree.nodes.new('NodeGroupOutput')
    modifier=object.modifiers.new(name,'NODES');modifier.node_group=tree
    return tree,source,sink

def input_socket(node,name):
    matches=[s for s in node.inputs if s.name==name and s.enabled]
    if len(matches)!=1:
        raise ValueError((node.bl_idname,name,[(s.name,s.identifier,s.enabled) for s in node.inputs]))
    return matches[0]

def output_socket(node,name):
    matches=[s for s in node.outputs if s.name==name and s.enabled]
    if len(matches)!=1:
        raise ValueError((node.bl_idname,name,[(s.name,s.identifier,s.enabled) for s in node.outputs]))
    return matches[0]

def store(tree,geometry,name,data_type,domain,value):
    node=tree.nodes.new('GeometryNodeStoreNamedAttribute');node.data_type=data_type;node.domain=domain
    node.inputs['Name'].default_value=name
    tree.links.new(geometry,node.inputs['Geometry']);tree.links.new(value,node.inputs['Value'])
    return node.outputs['Geometry']

def attributes(object,names):
    depsgraph=bpy.context.evaluated_depsgraph_get();evaluated=object.evaluated_get(depsgraph)
    mesh=evaluated.to_mesh(preserve_all_data_layers=True,depsgraph=depsgraph)
    out={}
    for name in names:
        attr=mesh.attributes[name]
        out[name]=[list(x.vector) if hasattr(x,'vector') else x.value for x in attr.data]
    evaluated.to_mesh_clear()
    return out

def grouped_edge_selection():
    reset()
    object=obj('triangle_and_quad',[(0,0,0),(1,0,0),(0,1,0),(3,0,0),(4,0,0),(4,1,0),(3,1,0)],[(0,1,2),(3,4,5,6)])
    tree,source,sink=graph(object,'AF105_grouped_edge_selection')
    island=tree.nodes.new('GeometryNodeInputMeshIsland')
    acc=tree.nodes.new('GeometryNodeAccumulateField');acc.data_type='INT';acc.domain='EDGE'
    input_socket(acc,'Value').default_value=1
    tree.links.new(island.outputs['Island Index'],acc.inputs['Group ID'])
    subtract=tree.nodes.new('ShaderNodeMath');subtract.operation='SUBTRACT';subtract.inputs[1].default_value=1
    tree.links.new(output_socket(acc,'Total'),subtract.inputs[0])
    random=tree.nodes.new('FunctionNodeRandomValue');random.data_type='INT'
    input_socket(random,'Min').default_value=0;random.inputs['Seed'].default_value=0
    tree.links.new(subtract.outputs[0],input_socket(random,'Max'));tree.links.new(island.outputs['Island Index'],random.inputs['ID'])
    equal=tree.nodes.new('FunctionNodeCompare');equal.data_type='INT';equal.operation='EQUAL'
    tree.links.new(output_socket(acc,'Trailing'),input_socket(equal,'A'));tree.links.new(output_socket(random,'Value'),input_socket(equal,'B'))
    negate=tree.nodes.new('FunctionNodeBooleanMath');negate.operation='NOT'
    tree.links.new(output_socket(acc,'Trailing'),negate.inputs[0])
    geometry=source.outputs['Geometry']
    values={'island':('INT',island.outputs['Island Index']),'local_index':('INT',output_socket(acc,'Trailing')),'edge_count':('INT',output_socket(acc,'Total')),'initial_select':('BOOLEAN',negate.outputs[0]),'random_select':('BOOLEAN',equal.outputs['Result'])}
    for name,(dtype,value) in values.items():geometry=store(tree,geometry,name,dtype,'EDGE',value)
    tree.links.new(geometry,sink.inputs['Geometry'])
    data=attributes(object,list(values))
    by_group={}
    for i,group in enumerate(data['island']):
        row=by_group.setdefault(str(group),{'edge_count':0,'initial_indices':[],'random_indices':[]})
        row['edge_count']+=1
        if data['initial_select'][i]:row['initial_indices'].append(data['local_index'][i])
        if data['random_select'][i]:row['random_indices'].append(data['local_index'][i])
    checks=[len(v['initial_indices'])==1 and len(v['random_indices'])==1 for v in by_group.values()]
    assert all(checks) and sorted(v['edge_count'] for v in by_group.values())==[3,4]
    return {'input':'one disconnected triangle and one quad;7edges; Seed0','observed':data,'by_island':by_group,'assertion':'exactly one selected edge per island with either predicate','passed':True,'limits':'Single seed/cardinality check, not a probability-distribution test or original-file reconstruction.'}

def copy_and_convert():
    reset()
    source=obj('source',[(0,0,0),(1,0,0),(0,1,0)],[(0,1,2)])
    target=obj('target',[(2,0,0),(3,0,0),(2,1,0)],[(0,1,2)])
    tree,group_input,group_output=graph(source,'AF105_translation')
    move=tree.nodes.new('GeometryNodeSetPosition');move.inputs['Offset'].default_value=(0,0,2)
    tree.links.new(group_input.outputs['Geometry'],move.inputs['Geometry']);tree.links.new(move.outputs['Geometry'],group_output.inputs['Geometry'])
    target.modifiers.new('prior_bevel','BEVEL')
    for ob in bpy.context.view_layer.objects:ob.select_set(False)
    source.select_set(True);target.select_set(True);bpy.context.view_layer.objects.active=source
    before=[m.type for m in target.modifiers]
    copied=set(bpy.ops.object.make_links_data(type='MODIFIERS'))
    after=[m.type for m in target.modifiers]
    shared=target.modifiers[0].node_group==tree
    converted=set(bpy.ops.object.convert(target='MESH'))
    result={ob.name:{'type':ob.type,'modifier_count':len(ob.modifiers),'vertex_z':[float(v.co.z) for v in ob.data.vertices]} for ob in bpy.context.selected_objects}
    assert before==['BEVEL'] and after==['NODES'] and shared
    assert all(v['modifier_count']==0 and all(abs(z-2)<1e-6 for z in v['vertex_z']) for v in result.values())
    return {'input':'two mesh triangles; active source has GN translation; target has a pre-existing Bevel','target_stack_before':before,'target_stack_after_copy':after,'node_group_shared':shared,'copy_operator_result':sorted(copied),'convert_operator_result':sorted(converted),'after_visual_geometry_conversion':result,'passed':True,'limits':'Demonstrates replacement of the target stack and baking for two meshes; does not test hundreds of mixed-type original scene objects.'}

def angle_and_pivot():
    reset()
    object=obj('direction_vectors',[(1,0,0),(1,1,0),(0,1,0),(-1,0,0)])
    tree,source,sink=graph(object,'AF105_direction_and_pivot')
    pos=tree.nodes.new('GeometryNodeInputPosition')
    geometry=source.outputs['Geometry']
    for name,operation,angle in [('greater90','GREATER_THAN',math.pi/2),('not_equal0','NOT_EQUAL',0.0)]:
        compare=tree.nodes.new('FunctionNodeCompare');compare.data_type='VECTOR';compare.mode='DIRECTION';compare.operation=operation
        input_socket(compare,'A').default_value=(1,0,0)
        tree.links.new(pos.outputs['Position'],input_socket(compare,'B'))
        compare.inputs['Angle'].default_value=angle
        geometry=store(tree,geometry,name,'BOOLEAN','POINT',compare.outputs['Result'])
    for pivot in ['AUTO','Z']:
        align=tree.nodes.new('FunctionNodeAlignEulerToVector');align.axis='X';align.pivot_axis=pivot
        align.inputs['Rotation'].default_value=(0,0,0);align.inputs['Factor'].default_value=1
        align.inputs['Vector'].default_value=(0,1,1)
        geometry=store(tree,geometry,'pivot_'+pivot,'FLOAT_VECTOR','POINT',align.outputs['Rotation'])
    tree.links.new(geometry,sink.inputs['Geometry'])
    data=attributes(object,['greater90','not_equal0','pivot_AUTO','pivot_Z'])
    axes={key:list(Euler(data[key][0],'XYZ').to_matrix()@Vector((1,0,0))) for key in ['pivot_AUTO','pivot_Z']}
    assert data['greater90']==[False,False,False,True]
    assert data['not_equal0']==[False,True,True,True]
    assert (Vector(axes['pivot_AUTO'])-Vector((0,1,1)).normalized()).length<1e-5
    assert (Vector(axes['pivot_Z'])-Vector((0,1,0))).length<1e-5
    return {'input_angles_degrees':[0,45,90,180],'compare_outputs':{key:data[key] for key in ['greater90','not_equal0']},'align_input':{'axis':'X','initial_euler':[0,0,0],'target_vector':[0,1,1],'factor':1},'aligned_x_axis':axes,'passed':True,'limits':'Generic controlled inputs distinguish operators/pivots; not the auxiliary original input nor a Blender3.6 historical replay.'}

receipt={'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'runtime_release':bpy.app.version_string,'runtime_tuple':list(bpy.app.version),'build_hash':bpy.app.build_hash.decode(errors='replace'),'scope':'three controlled semantic probes; independent of author sessions','probes':{}}
for name,fn in [('BL-T1_grouped_selection',grouped_edge_selection),('BL-T3_copy_convert',copy_and_convert),('aux_direction_pivot',angle_and_pivot)]:
    try:receipt['probes'][name]=fn()
    except Exception as error:receipt['probes'][name]={'passed':False,'error':repr(error),'traceback':traceback.format_exc()}
receipt['ended_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
receipt['all_passed']=all(x['passed'] for x in receipt['probes'].values())
(OUT/'controlled-probes-result.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print('AF105_PROBES',json.dumps(receipt,ensure_ascii=False))
if not receipt['all_passed']:raise SystemExit(1)
