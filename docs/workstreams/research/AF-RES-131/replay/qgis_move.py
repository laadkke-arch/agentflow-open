"""QGIS --code entry point for a local memory-layer Move Feature comparison."""

import json
import sys
import traceback

from qgis.PyQt.QtCore import QCoreApplication, QPoint, Qt, QTimer
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import QAction
from qgis.core import Qgis, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsRectangle, QgsVectorLayer
from qgis.utils import iface


def point_layer(name, x, y):
    layer = QgsVectorLayer("Point?crs=EPSG:3857", name, "memory")
    feature = QgsFeature(layer.fields())
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
    success, features = layer.dataProvider().addFeatures([feature])
    assert success and len(features) == 1
    layer.updateExtents()
    QgsProject.instance().addMapLayer(layer)
    return layer, features[0].id()


def xy(layer, fid):
    point = layer.getFeature(fid).geometry().asPoint()
    return [point.x(), point.y()]


def canvas_pixel(canvas, coordinate):
    point = canvas.getCoordinateTransform().transform(QgsPointXY(*coordinate))
    return QPoint(round(point.x()), round(point.y()))


def run_case(name, edit, selected, readonly=False, active_name="a"):
    project = QgsProject.instance()
    first = point_layer("a", 20, 30)
    second = point_layer("b", 65, 72)
    layers = {"a": first, "b": second}
    active, active_fid = layers[active_name]
    canvas = iface.mapCanvas()
    try:
        assert iface.setActiveLayer(active)
        if selected:
            first[0].selectByIds([first[1]])
        if readonly:
            active.setReadOnly(True)
        if edit:
            iface.actionToggleEditing().trigger()
        assert active.isEditable() == edit
        canvas.setExtent(QgsRectangle(0, 0, 100, 100))
        canvas.refresh()
        QTest.qWait(180)
        action = iface.mainWindow().findChild(QAction, "mActionMoveFeature")
        assert action is not None
        before = {key: xy(*item) for key, item in layers.items()}
        selections = {key: item[0].selectedFeatureIds() for key, item in layers.items()}
        start = canvas_pixel(canvas, before[active_name])
        end = canvas_pixel(canvas, [before[active_name][0] + 12, before[active_name][1] + 9])
        assert canvas.viewport().rect().contains(start) and canvas.viewport().rect().contains(end)
        enabled = action.isEnabled()
        active_tool = canvas.mapTool()
        if enabled:
            action.trigger()
            QTest.qWait(80)
            active_tool = canvas.mapTool()
            QTest.mouseClick(canvas.viewport(), Qt.LeftButton, pos=start)
            QTest.mouseMove(canvas.viewport(), end, delay=50)
            QTest.mouseClick(canvas.viewport(), Qt.LeftButton, pos=end)
            QTest.qWait(100)
        after = {key: xy(*item) for key, item in layers.items()}
        result = {
            "id": name, "qgis_version": Qgis.QGIS_VERSION, "active_layer": active_name,
            "editable": active.isEditable(), "read_only": active.readOnly(),
            "selected_before": selections, "feature_ids": {key: item[1] for key, item in layers.items()},
            "move_action_enabled": enabled, "map_tool": active_tool.toolName(),
            "canvas_pixel_start": [start.x(), start.y()], "canvas_pixel_end": [end.x(), end.y()],
            "clicks_sent": 2 if enabled else 0, "before": before, "after": after,
            "changed": {key: max(abs(b - a) for a, b in zip(before[key], after[key])) > 1e-6
                        for key in layers}, "epsilon_map_units": 1e-6,
        }
        print(json.dumps(result), flush=True)
        assert enabled == edit
        assert result["changed"] == {key: edit and key == active_name for key in layers}
    finally:
        if active.isEditable():
            active.rollBack()
        project.removeMapLayer(first[0])
        project.removeMapLayer(second[0])


def execute():
    try:
        run_case("selected-edit-off", edit=False, selected=True)
        run_case("selected-read-only", edit=False, selected=True, readonly=True)
        run_case("unselected-edit-on-direct-hit", edit=True, selected=False)
        run_case("selected-a-active-b-direct-hit", edit=True, selected=True, active_name="b")
    except Exception:
        traceback.print_exc(file=sys.stderr)
        QCoreApplication.exit(1)
    else:
        QCoreApplication.exit(0)


QTimer.singleShot(300, execute)
