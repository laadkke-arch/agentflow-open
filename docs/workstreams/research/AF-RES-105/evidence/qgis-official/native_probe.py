"""Small synthetic QGIS probes; not a reconstruction of any user's environment."""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / '.cache' / 'qgis-official'
OUT = ROOT / 'evidence' / 'qgis-official'
for name in ('qt-runtime', 'profile', 'config'):
    (CACHE/name).mkdir(parents=True, exist_ok=True)
(CACHE/'qt-runtime').chmod(0o700)
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['XDG_RUNTIME_DIR'] = str(CACHE/'qt-runtime')
os.environ['XDG_CONFIG_HOME'] = str(CACHE/'config')
os.environ['QGIS_CUSTOM_CONFIG_PATH'] = str(CACHE/'profile')

from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtGui import QColor, QFont
from qgis.core import (Qgis, QgsApplication, QgsExpression, QgsExpressionContext,
                      QgsExpressionContextUtils, QgsFeature, QgsGeometry,
                      QgsMapRendererParallelJob, QgsMapSettings, QgsPalLayerSettings,
                      QgsPointXY, QgsProject, QgsProperty, QgsRectangle,
                      QgsTextFormat, QgsVectorLayer, QgsVectorLayerSimpleLabeling)
from osgeo import gdal

app=QgsApplication([],False,str(CACHE/'profile'))
app.initQgis()
project=QgsProject.instance()

def configure_labels(layer,field,placement,show_expression=None,repeat=None):
    settings=QgsPalLayerSettings()
    settings.fieldName=field
    settings.placement=placement
    fmt=QgsTextFormat()
    fmt.setFont(QFont('DejaVu Sans',10))
    fmt.setSize(10)
    fmt.setColor(QColor('black'))
    settings.setFormat(fmt)
    if repeat is not None:
        settings.repeatDistance=repeat
        settings.repeatDistanceUnit=Qgis.RenderUnit.MapUnits
    if show_expression:
        properties=settings.dataDefinedProperties()
        properties.setProperty(QgsPalLayerSettings.Show,QgsProperty.fromExpression(show_expression))
        settings.setDataDefinedProperties(properties)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
    layer.setLabelsEnabled(True)
    layer.triggerRepaint()

def render(layer,extent,size,filename):
    settings=QgsMapSettings()
    settings.setLayers([layer])
    settings.setDestinationCrs(layer.crs())
    settings.setExtent(extent)
    settings.setOutputSize(size)
    settings.setOutputDpi(96)
    settings.setBackgroundColor(QColor('white'))
    job=QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    image=job.renderedImage()
    path=CACHE/filename
    assert image.save(str(path))
    result=job.takeLabelingResults()
    labels=result.allLabels() if result is not None else []
    return {'labels':[{'text':p.labelText,'feature_id':int(p.featureId),'rotation':p.rotation} for p in labels],
            'label_count':len(labels),'image_cache':str(path.relative_to(ROOT)),
            'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'render_errors':[str(e.message) for e in job.errors()]}

started=dt.datetime.now(dt.timezone.utc).isoformat()
line=QgsVectorLayer('LineString?crs=EPSG:3857&field=label:string','repeat_probe','memory')
feature=QgsFeature(line.fields())
feature.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(0,0),QgsPointXY(1000,0)]))
feature.setAttributes(['ROAD'])
assert line.dataProvider().addFeatures([feature])[0]
line.updateExtents();project.addMapLayer(line)
configure_labels(line,'label',Qgis.LabelPlacement.Line,repeat=200)
repeated=render(line,QgsRectangle(-50,-100,1050,100),QSize(1100,240),'native-repeat-labels.png')
repeat_texts={x['text'] for x in repeated['labels']}
repeat_checks={'more_than_one_label':repeated['label_count']>1,
               'all_repetitions_keep_same_text':repeat_texts=={'ROAD'},
               'input_feature_count_still_one':line.featureCount()==1}

points=QgsVectorLayer('Point?crs=EPSG:3857&field=Location_Names:string','group_label_probe','memory')
input_rows=[{'name':'A','x':0,'y':0},{'name':'A','x':0,'y':0},
            {'name':'A','x':500,'y':0},{'name':'B','x':0,'y':500}]
features=[]
for row in input_rows:
    feature=QgsFeature(points.fields())
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(row['x'],row['y'])))
    feature.setAttributes([row['name']]);features.append(feature)
assert points.dataProvider().addFeatures(features)[0]
points.updateExtents();project.addMapLayer(points)
before=[(int(f.id()),f['Location_Names'],f.geometry().asWkt()) for f in points.getFeatures()]
configure_labels(points,'Location_Names',Qgis.LabelPlacement.OverPoint)
offset=render(points,QgsRectangle(-100,-100,650,650),QSize(750,750),'native-offset-only.png')
predicate='$id = array_first(array_agg($id,"Location_Names"))'
context=QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(points))
context.setFields(points.fields())
expr=QgsExpression(predicate)
assert not expr.hasParserError(),expr.parserErrorString()
evaluated=[]
for feature in points.getFeatures():
    context.setFeature(feature)
    value=expr.evaluate(context)
    assert not expr.hasEvalError(),expr.evalErrorString()
    evaluated.append({'feature_id':int(feature.id()),'name':feature['Location_Names'],'show_label':bool(value)})
configure_labels(points,'Location_Names',Qgis.LabelPlacement.OverPoint,show_expression=predicate)
filtered=render(points,QgsRectangle(-100,-100,650,650),QSize(750,750),'native-group-show-label.png')
after=[(int(f.id()),f['Location_Names'],f.geometry().asWkt()) for f in points.getFeatures()]
selected_counts=collections.Counter(x['name'] for x in evaluated if x['show_label'])
offset_counts=collections.Counter(x['text'] for x in offset['labels'])
filtered_counts=collections.Counter(x['text'] for x in filtered['labels'])
group_checks={'predicate_selects_exactly_one_per_distinct_name':selected_counts=={'A':1,'B':1},
              'offset_placement_alone_keeps_multiple_A':offset_counts['A']>1,
              'show_label_condition_renders_one_per_name':filtered_counts=={'A':1,'B':1},
              'features_attributes_and_geometries_unchanged':before==after and points.featureCount()==4}

result={'executed_utc':started,'completed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'grade':'D3 synthetic independent execution; not the original user inputs',
        'runtime':{'QGIS':Qgis.QGIS_VERSION,'GDAL':gdal.VersionInfo('--version'),
                   'python':sys.version,'executable':sys.executable,'QT_QPA_PLATFORM':os.environ['QT_QPA_PLATFORM']},
        'repeat_label_probe':{'case_id':'QG-T2','input':{'geometry':'LINESTRING(0 0,1000 0)','crs':'EPSG:3857','label_field':'ROAD','repeat_distance':200,'repeat_unit':'MapUnits'},
                              'expected_functional_checks':repeat_checks,'observed':repeated,
                              'limit':'This names one feature repeatedly; it does not test every possible distance-label expression or prove a general impossibility.'},
        'group_label_probe':{'case_id':'QG-T3','input_rows':input_rows,'crs':'EPSG:3857','predicate':predicate,
                             'predicate_results':evaluated,'offset_only':offset,'with_show_label_predicate':filtered,
                             'expected_functional_checks':group_checks,
                             'limit':'The original linked example field is mapped to Location_Names for this synthetic layer. No ordering guarantee is inferred from array_first.'},
        'all_checks_passed':all(repeat_checks.values()) and all(group_checks.values()),
        'source_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'native-probe-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
if not result['all_checks_passed']:
    raise SystemExit(1)
