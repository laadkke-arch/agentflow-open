"""Read public attached .blend artifacts with scripts disabled; never save them.

Run with Blender --background --factory-startup --disable-autoexec --python THIS.
Raw graph extraction stays in ignored cache; only curated findings enter evidence.
"""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import bpy

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / '.cache' / 'blender-followup'

def plain(value):
    if isinstance(value, bpy.types.ID):
        return {'datablock_name': value.name, 'rna_type': value.bl_rna.identifier}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    try:
        return list(value)
    except TypeError:
        return str(value)

def inspect_one(path):
    opened = dt.datetime.now(dt.timezone.utc).isoformat()
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False, use_scripts=False)
    result = {'file': path.name, 'inspected_utc': opened,
              'loaded_bytes_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'runtime_release': bpy.app.version_string, 'runtime_tuple': list(bpy.app.version),
              'stored_file_version_tuple': list(bpy.data.version),
              'stored_version_limit': 'major/minor/internal subversion, not major/minor/release patch',
              'auto_execute_enabled': bpy.context.preferences.filepaths.use_scripts_auto_execute,
              'autoexec_fail': getattr(bpy.app, 'autoexec_fail', None),
              'node_groups': [], 'objects': []}
    for group in bpy.data.node_groups:
        if group.bl_idname != 'GeometryNodeTree':
            continue
        nodes = []
        for node in group.nodes:
            rec = {'name': node.name, 'label': node.label, 'type': node.bl_idname,
                   'mute': node.mute, 'inputs': [], 'constant_outputs': []}
            for attr in ['data_type','domain','mode','operation','axis','pivot_axis','input_type','is_active_output']:
                if hasattr(node, attr):
                    rec[attr] = plain(getattr(node, attr))
            if hasattr(node, 'node_tree') and node.node_tree:
                rec['group_reference'] = node.node_tree.name
            for index, socket in enumerate(node.inputs):
                rec['inputs'].append({'index': index, 'name': socket.name,
                    'identifier': socket.identifier, 'socket_type': socket.bl_idname,
                    'enabled': socket.enabled, 'linked': socket.is_linked,
                    'default': plain(socket.default_value) if hasattr(socket,'default_value') else None})
            if node.bl_idname in ['ShaderNodeValue','FunctionNodeInputInt','FunctionNodeInputVector']:
                for socket in node.outputs:
                    if hasattr(socket,'default_value'):
                        rec['constant_outputs'].append({'name':socket.name,'value':plain(socket.default_value)})
            nodes.append(rec)
        result['node_groups'].append({'name':group.name,'nodes':nodes,
            'links':[{'from_node':link.from_node.name,'from_socket':link.from_socket.name,
                      'from_identifier':link.from_socket.identifier,
                      'to_node':link.to_node.name,'to_socket':link.to_socket.name,
                      'to_identifier':link.to_socket.identifier} for link in group.links]})
    depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in bpy.data.objects:
        rec={'name':obj.name,'type':obj.type,'modifiers':[],
             'location':list(obj.location),'rotation_euler':list(obj.rotation_euler),'scale':list(obj.scale)}
        for modifier in obj.modifiers:
            rec['modifiers'].append({'name':modifier.name,'type':modifier.type,
                'show_viewport':modifier.show_viewport,
                'node_group':modifier.node_group.name if modifier.type=='NODES' and modifier.node_group else None})
        if obj.type=='MESH':
            rec['base_mesh']={'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons)}
            try:
                evaluated=obj.evaluated_get(depsgraph)
                mesh=evaluated.to_mesh()
                coords=[tuple(v.co) for v in mesh.vertices]
                rec['evaluated_mesh']={'vertices':len(mesh.vertices),'edges':len(mesh.edges),'faces':len(mesh.polygons),
                    'bounds_min':[min(v[i] for v in coords) for i in range(3)] if coords else None,
                    'bounds_max':[max(v[i] for v in coords) for i in range(3)] if coords else None,
                    'material_index_counts':dict(collections.Counter(p.material_index for p in mesh.polygons)),
                    'attributes':[{'name':a.name,'data_type':a.data_type,'domain':a.domain,'length':len(a.data)} for a in mesh.attributes]}
                evaluated.to_mesh_clear()
            except Exception as error:
                rec['evaluation_error']=repr(error)
        result['objects'].append(rec)
    return result

results=[]
for key in ['initial1','initial2','proposal1','linked2']:
    path=CACHE/('original-'+key+'.blend')
    try:
        result=inspect_one(path)
    except Exception as error:
        result={'file':path.name,'error':repr(error)}
    results.append(result)
    print('AF105_ORIGINAL',json.dumps({k:result[k] for k in ['file','runtime_release','stored_file_version_tuple','auto_execute_enabled','objects','error'] if k in result},ensure_ascii=False))
(CACHE/'original-inspection-raw.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
