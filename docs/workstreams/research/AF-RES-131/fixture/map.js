import Feature from 'ol/Feature.js';
import Map from 'ol/Map.js';
import View from 'ol/View.js';
import {noModifierKeys, primaryAction} from 'ol/events/condition.js';
import Point from 'ol/geom/Point.js';
import DragPan from 'ol/interaction/DragPan.js';
import Select from 'ol/interaction/Select.js';
import Translate from 'ol/interaction/Translate.js';
import VectorLayer from 'ol/layer/Vector.js';
import VectorSource from 'ol/source/Vector.js';
import CircleStyle from 'ol/style/Circle.js';
import Fill from 'ol/style/Fill.js';
import Style from 'ol/style/Style.js';
import {VERSION} from 'ol/util.js';

const copy = (coordinate) => coordinate ? coordinate.slice() : null;
const featureId = (feature) => feature?.getId() ?? null;
const layerId = (layer) => layer?.get('researchId') ?? null;
const nextFrame = () => new Promise((resolve) => requestAnimationFrame(resolve));

function prepare(plan, scenario, pin) {
  const target = document.getElementById('map');
  const feature = new Feature({
    geometry: new Point(plan.feature.coordinate),
    draggable: plan.feature.draggable,
  });
  feature.setId(plan.feature.id);
  const parcelStyle = new Style({
    image: new CircleStyle({
      radius: plan.feature.radiusCssPx,
      fill: new Fill({color: plan.feature.fill}),
    }),
  });
  const layer = new VectorLayer({
    source: new VectorSource({features: [feature], wrapX: false}),
    style: parcelStyle,
  });
  layer.set('researchId', plan.feature.layerId);
  const view = new View({...plan.view, constrainResolution: false});
  // 6.0.0 uses a truthiness check for Select.style and lacks condition.all.
  const select = new Select({style: pin.select_null_style ? null : parcelStyle, layers: [layer]});
  const selection = select.getFeatures();
  const condition = (event) => noModifierKeys(event) && primaryAction(event);
  const records = [];
  const nativeIds = new WeakMap();
  const mapIds = new WeakMap();
  let nativeSequence = 0;
  let mapSequence = 0;
  let phase = 'seed';
  let current = null;
  function record(kind, details) {
    records.push({
      seq: records.length + 1,
      phase,
      clockMs: performance.now(),
      kind,
      ...details,
    });
  }
  const translation = {hitTolerance: scenario.hitTolerance};
  if (pin.translate_condition === 'present') translation.condition = condition;
  if (scenario.collection !== 'omitted') translation.features = selection;

  function predicate(name) {
    const accepted = scenario[name] === 'allow';
    if (!scenario.observers) return () => accepted;
    return (...args) => {
      const candidate = name === 'filter' ? args[0] : null;
      const candidateLayer = args[name === 'filter' ? 1 : 0];
      record('configured-callback', {
        ...current, option: name, featureId: featureId(candidate), layerId: layerId(candidateLayer),
        argCount: args.length, featureIsSeed: candidate ? candidate === feature : null,
        layerIsSeed: candidateLayer ? candidateLayer === layer : null, accepted,
      });
      return accepted;
    };
  }
  for (const option of ['filter', 'layers']) {
    if (scenario[option] !== 'omitted' && pin[option + '_with_features'] !== 'option-absent') {
      translation[option] = predicate(option);
    }
  }

  const translate = new Translate(translation);
  const pan = new DragPan({condition});
  const tools = {translate, pan, select};
  const order = plan.interactionOrder.filter((name) => name !== 'translate' || scenario.translateActive);
  const map = new Map({
    target,
    layers: [layer],
    view,
    controls: [],
    interactions: order.map((name) => tools[name]),
    pixelRatio: plan.dpr,
    moveTolerance: plan.moveToleranceCssPx,
  });

  const selectedIds = () => selection.getArray().map(featureId);
  const state = () => ({
    featureId: featureId(feature),
    geometryType: feature.getGeometry().getType(),
    geometry: feature.getGeometry().getCoordinates(),
    selectedIds: selectedIds(),
    center: copy(view.getCenter()),
    resolution: view.getResolution(),
    rotation: view.getRotation(),
    interacting: view.getInteracting(),
    animating: view.getAnimating(),
  });
  const eachFeature = map.forEachFeatureAtPixel;
  const rawHits = (pixel, hitTolerance) => {
    const hits = [];
    eachFeature.call(map, pixel, (candidate, candidateLayer) => {
      hits.push({featureId: featureId(candidate), layerId: layerId(candidateLayer)});
    }, {hitTolerance});
    return hits;
  };
  const casesAtPixel = (pixel) => ({
    atZero: rawHits(pixel, 0),
    atConfiguredTolerance: rawHits(pixel, scenario.hitTolerance),
  });
  const identifyOriginal = (event) => nativeIds.get(event) ?? nativeIds.get(event.originalEvent) ?? null;

  function nativeDetails(event) {
    return {
      originalType: event.type,
      eventTimeMs: event.timeStamp,
      trusted: event.isTrusted,
      target: event.target?.tagName ?? null,
      targetClass: event.target?.getAttribute?.('class') ?? null,
      client: [event.clientX, event.clientY],
      button: event.button,
      buttons: event.buttons,
      pointerType: event.pointerType,
      pointerId: event.pointerId,
      primary: event.isPrimary,
      modifiers: [event.shiftKey, event.altKey, event.ctrlKey, event.metaKey],
      browserDefaultPrevented: event.defaultPrevented,
    };
  }

  if (scenario.observers) {
    for (const type of ['pointerdown', 'pointermove', 'pointerup', 'pointercancel']) {
      document.addEventListener(type, (event) => {
        const nativeId = ++nativeSequence;
        nativeIds.set(event, nativeId);
        const pixel = map.getEventPixel(event);
        record('dom', {
          nativeId,
          ...nativeDetails(event),
          mapPixel: pixel,
          coordinateFromFrame: copy(map.getCoordinateFromPixel(pixel)),
          hits: casesAtPixel(pixel),
          state: state(),
        });
      }, {capture: true, passive: true});
    }
    for (const type of ['pointermove', 'pointerdown', 'pointerdrag', 'pointerup', 'click', 'singleclick']) {
      map.on(type, (event) => {
        const mapId = ++mapSequence;
        mapIds.set(event, mapId);
        // Keep the event's lazy coordinate and pixel getters untouched.
        const pixel = map.getEventPixel(event.originalEvent);
        record('map-event', {
          mapId,
          nativeId: identifyOriginal(event.originalEvent),
          type: event.type,
          eventTimeMs: event.originalEvent.timeStamp,
          mapPixel: pixel,
          coordinateFromFrame: copy(map.getCoordinateFromPixel(pixel)),
          activePointers: event.activePointers?.length ?? null,
          dragging: event.dragging,
          propagationStopped: !!event.propagationStopped,
          state: state(),
        });
      });
    }

    map.forEachFeatureAtPixel = function (pixel, callback, options) {
      const delivered = [];
      const result = Reflect.apply(eachFeature, this, [
        pixel,
        function (candidate, candidateLayer, geometry) {
          const returned = Reflect.apply(callback, this, [candidate, candidateLayer, geometry]);
          delivered.push({
            featureId: featureId(candidate),
            layerId: layerId(candidateLayer),
            callbackTruthy: !!returned,
          });
          return returned;
        },
        options,
      ]);
      record('handler-hit', {
        ...current,
        mapPixel: copy(pixel),
        tolerance: options?.hitTolerance ?? 0,
        hits: delivered,
        returnFeatureId: result instanceof Feature ? featureId(result) : null,
      });
      return result;
    };

    function observeInteraction(name, interaction) {
      for (const method of ['handleEvent', 'handleDownEvent', 'stopDown', 'handleDragEvent', 'handleUpEvent']) {
        const original = interaction[method];
        if (!original) continue;
        interaction[method] = function (...args) {
          const parent = current;
          const event = method === 'stopDown' ? null : args[0];
          current = {mapId: event ? mapIds.get(event) ?? null : parent?.mapId, name, method};
          record('handler-enter', {
            ...current,
            downHandled: method === 'stopDown' ? args[0] : null,
            handlingSequence: this.handlingDownUpSequence ?? null,
            state: state(),
          });
          try {
            const returned = Reflect.apply(original, this, args);
            record('handler-return', {
              ...current,
              returned: returned ?? null,
              handlingSequence: this.handlingDownUpSequence ?? null,
              propagationStopped: event ? !!event.propagationStopped : null,
              browserDefaultPrevented: event ? event.originalEvent.defaultPrevented : null,
              state: state(),
            });
            return returned;
          } finally {
            current = parent;
          }
        };
      }
    }
    Object.entries(tools).forEach(([name, interaction]) => observeInteraction(name, interaction));

    for (const type of ['translatestart', 'translating', 'translateend']) {
      translate.on(type, (event) => record('translate-event', {
        type,
        mapId: mapIds.get(event.mapBrowserEvent) ?? null,
        coordinate: copy(event.coordinate),
        startCoordinate: copy(event.startCoordinate),
        featureIds: event.features.getArray().map(featureId),
        state: state(),
      }));
    }
    select.on('select', (event) => record('select-event', {
      mapId: mapIds.get(event.mapBrowserEvent) ?? null,
      selected: event.selected.map(featureId),
      deselected: event.deselected.map(featureId),
      state: state(),
    }));
    for (const [observable, event, name] of [
      [feature.getGeometry(), 'change', 'geometry'],
      [view, 'change:center', 'center'],
    ]) {
      observable.on(event, () => record('state-change', {...current, value: name, state: state()}));
    }
  }

  function snapshot(client) {
    const mapPixel = client ? map.getEventPixel({clientX: client[0], clientY: client[1]}) : null;
    return {
      phase,
      clockMs: performance.now(),
      state: state(),
      mapPixel,
      coordinateFromFrame: mapPixel ? copy(map.getCoordinateFromPixel(mapPixel)) : null,
      featurePixel: copy(map.getPixelFromCoordinate(feature.getGeometry().getCoordinates())),
      focused: target.contains(document.activeElement),
    };
  }

  map.renderSync();
  const beforeSeed = state();
  if (scenario.collection === 'included') selection.push(feature);
  map.renderSync();
  const rect = map.getViewport().getBoundingClientRect();
  const renderer = layer.getRenderer().constructor.name;
  const initial = {
    beforeSeed,
    afterSeed: state(),
    probes: Object.fromEntries(Object.entries(plan.positions).map(([name, pixel]) => [
      name, casesAtPixel(pixel),
    ])),
    featureStyleDefined: feature.getStyle() != null,
    selectedStyleMatchesPoint: !feature.getStyle() || feature.getStyle() === parcelStyle,
    selectStylePath: pin.select_null_style ? 'null' : 'same-point-style',
    translateOptions: Object.keys(translation),
    radiusCssPx: layer.getStyle().getImage().getRadius(),
    adjustedInteractionOrder: order,
    activeInteractions: order.filter((name) => tools[name].getActive()),
    rect: [rect.left, rect.top, rect.width, rect.height],
    projection: view.getProjection().getCode(),
    renderer,
    dpr: devicePixelRatio,
    timeOriginMs: performance.timeOrigin,
    loadedOlVersion: VERSION,
  };

  return Object.freeze({
    initial,
    snapshot,
    setPhase: (nextPhase) => { phase = nextPhase; },
    afterRender: async (client) => {
      await nextFrame();
      await nextFrame();
      return client ? snapshot(client) : null;
    },
    records: () => records,
  });
}

window.af131 = {prepare};
