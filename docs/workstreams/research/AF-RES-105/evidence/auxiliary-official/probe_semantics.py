"""Current-runtime semantic contrasts; never reconstruction of an author's environment."""
import os,json,datetime,hashlib,ast,re
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from qgis.core import QgsApplication,QgsGeometry,QgsFeature,QgsExpression,QgsExpressionContext,QgsVectorLayer,QgsExpressionContextUtils,Qgis,QgsDistanceArea,QgsCoordinateReferenceSystem,QgsCoordinateTransformContext,QgsUnitTypes
from osgeo import gdal,ogr
P=Path(__file__).resolve().parents[2];C=P/'.cache/auxiliary-official';C.mkdir(parents=True,exist_ok=True)
app=QgsApplication([],False);app.initQgis()
result={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime':{'QGIS':Qgis.QGIS_VERSION,'GDAL':gdal.VersionInfo('RELEASE_NAME')},'scope':'researcher synthetic geometry only; no author original data; no label-rendering inference','expression_cases':[]}
for label,wkt in [('straight10','LINESTRING(0 0,10 0)'),('bent20','LINESTRING(0 0,10 0,10 10)')]:
 g=QgsGeometry.fromWkt(wkt);f=QgsFeature();f.setGeometry(g);ctx=QgsExpressionContext();ctx.setFeature(f)
 for expression in ['geom_to_wkt(line_substring($geometry,0,0.5))','geom_to_wkt(line_substring($geometry,0.5,0.5))','geom_to_wkt(line_interpolate_point($geometry,0.5))','geom_to_wkt(line_interpolate_point($geometry,length($geometry)/2))','geom_to_wkt(centroid($geometry))','geom_to_wkt(collect_geometries(start_point($geometry),line_interpolate_point($geometry,length($geometry)/2),end_point($geometry)))']:
  e=QgsExpression(expression);v=e.evaluate(ctx);result['expression_cases'].append({'input':label,'wkt':wkt,'expression':expression,'output':v,'error':e.evalErrorString()})
# Same coordinates with an explicit length calculator/unit setting; never presume this was OP's setting.
f=QgsFeature();f.setGeometry(QgsGeometry.fromWkt('LINESTRING(0 0,10 0)'));ctx=QgsExpressionContext();ctx.setFeature(f)
da=QgsDistanceArea();da.setSourceCrs(QgsCoordinateReferenceSystem('EPSG:27700'),QgsCoordinateTransformContext());da.setEllipsoid('NONE')
result['length_units']=[]
for unit in [QgsUnitTypes.DistanceMeters,QgsUnitTypes.DistanceKilometers]:
 for expression in ['$length','length($geometry)']:
  e=QgsExpression(expression);e.setGeomCalculator(da);e.setDistanceUnits(unit);v=e.evaluate(ctx);result['length_units'].append({'expression':expression,'set_distance_unit':QgsUnitTypes.toString(unit),'output':v,'error':e.evalErrorString()})
# Read the v3.8.4 manual code block mechanically without altering it.
s=(C/'gdal-v3.8.4-gotchas.bin').read_text();a=s.index('   from osgeo import ogr',s.index('Certain objects'));b=s.index('\nIf this is not possible',a);snippet='\n'.join(line[3:] if line.startswith('   ') else line for line in s[a:b].splitlines())
try:ast.parse(snippet);result['gdal_manual_literal_parse']={'status':'pass'}
except SyntaxError as e:result['gdal_manual_literal_parse']={'status':'fail','error':str(e),'source_sha256':hashlib.sha256(snippet.encode()).hexdigest(),'source_location':'v3.8.4 python_gotchas.rst lines179–185','correction_needed':'missing closing parenthesis at SetGeometry call; no inference that source code ran'}
gdal.UseExceptions();result['gdal_lifetime_cases']=[]
for mode in ['context','close']:
 path=C/(mode+'.gpkg')
 if path.exists():path.unlink()
 ds=ogr.GetDriverByName('GPKG').CreateDataSource(str(path))
 def populate(ds):
  layer=ds.CreateLayer('points',geom_type=ogr.wkbPoint);feature=ogr.Feature(layer.GetLayerDefn());feature.SetGeometry(ogr.CreateGeometryFromWkt('POINT (3 4)'));layer.CreateFeature(feature)
 if mode=='context':
  with ds as live:populate(live)
 else:populate(ds);ds.Close()
 with gdal.OpenEx(str(path),gdal.OF_VECTOR) as check:
  layer=check.GetLayer();feature=layer.GetNextFeature();result['gdal_lifetime_cases'].append({'mode':mode,'reopened_feature_count':layer.GetFeatureCount(),'reopened_wkt':feature.GetGeometryRef().ExportToWkt(),'input':'one GPKG point (3,4)','file_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
result['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();result['limitations']=['Current QGIS3.40.6/GDAL3.10.3; not author or2024 runtime','Function outputs alone do not demonstrate label visibility, collision settings or geometry-generator units','Equal reopened point content does not imply binary-identical databases, all driver behavior, or OP adoption','No historical software installation or author environment reconstruction']
out=P/'evidence/auxiliary-official/probe-results.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
# Avoid binding destructors after teardown: process exits with app live.
