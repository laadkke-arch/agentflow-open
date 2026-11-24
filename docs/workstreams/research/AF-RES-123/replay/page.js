/* Read-only probes for the V8628 browser replay. Input is driven in drive.cjs. */
(() => {
  const mount = document.querySelector('#viz');
  const eventTypes = `pointerover pointerenter pointermove pointerdown pointerup pointerout pointerleave
    pointercancel gotpointercapture lostpointercapture mouseover mouseenter mousemove mousedown mouseup
    mouseout mouseleave click dblclick auxclick contextmenu dragstart dragend dragenter dragover
    dragleave drop wheel touchstart touchmove touchend touchcancel`.trim().split(/\s+/);
  const viewTypes = ['mouseover', 'mousemove', 'mouseout', 'mousedown', 'mouseup', 'click', 'dblclick'];
  const events = [];
  const snapshots = [];
  const nativeIds = new WeakMap();
  const loads = [];
  let phase;
  let step;
  let view;
  let compiled;
  let hasTranslate;
  let nextNativeId = 0;

  const frame = () => new Promise(requestAnimationFrame);
  const clone = value => JSON.parse(JSON.stringify(value ?? null));
  const groupPosition = item => [item?.x ?? 0, item?.y ?? 0];
  const monthValue = value => value == null ? null : +value;

  function bounds(item, offset = [0, 0]) {
    const b = item?.bounds;
    return b ? [b.x1 + offset[0], b.y1 + offset[1], b.x2 + offset[0], b.y2 + offset[1]] : null;
  }

  function markIdentity(item) {
    if (!item?.mark) return null;
    const {name, marktype, role, interactive} = item.mark;
    return {name: name ?? null, marktype, role, interactive: interactive ?? null};
  }

  function groupChain(item) {
    const chain = [];
    for (let group = item; group?.mark; group = group.mark.group) {
      chain.push({mark: markIdentity(group), offset: groupPosition(group)});
    }
    return chain;
  }

  function effectOffset(group) {
    const chain = groupChain(group);
    return chain.reduce(([x, y], entry) => [x + entry.offset[0], y + entry.offset[1]], [0, 0]);
  }

  function describeItem(item) {
    const mark = markIdentity(item);
    if (!mark) return null;
    return {
      mark, parents: groupChain(item.mark.group), bounds: bounds(item),
      position: groupPosition(item),
      month: monthValue(item.datum?.month_date),
      weather: item.datum?.weather ?? null
    };
  }

  function domPath(target) {
    const path = [];
    for (let el = target; el instanceof Element && path.length < 9; el = el.parentElement) {
      path.push({
        tag: el.localName, id: el.id || null, class: el.getAttribute('class'),
        role: el.getAttribute('role'), aria: el.getAttribute('aria-label')
      });
    }
    return path;
  }

  function surface() {
    return mount.querySelector('svg, canvas');
  }

  function coordinateSystem() {
    const node = surface();
    const rect = node.getBoundingClientRect();
    const padding = view.padding();
    const origin = view.origin();
    const pixelWidth = node.localName === 'canvas' ? node.width : node.width.baseVal.value;
    const pixelHeight = node.localName === 'canvas' ? node.height : node.height.baseVal.value;
    const [scaleX, scaleY] = [rect.width / pixelWidth, rect.height / pixelHeight];
    const plotOrigin = [
      rect.left + node.clientLeft + (padding.left + origin[0]) * scaleX,
      rect.top + node.clientTop + (padding.top + origin[1]) * scaleY
    ];
    return {
      rect: [rect.left, rect.top, rect.width, rect.height], pixelSize: [pixelWidth, pixelHeight],
      scale: [scaleX, scaleY], plotOrigin, padding, origin, dpr: devicePixelRatio,
      viewport: [innerWidth, innerHeight], zoom: visualViewport.scale,
      plotSize: [view.width(), view.height()]
    };
  }

  function plotPoint(client) {
    const {plotOrigin, scale} = coordinateSystem();
    return client.map((value, i) => (value - plotOrigin[i]) / scale[i]);
  }

  function record(channel, event, item) {
    if (!phase) return;
    const nativeId = nativeIds.get(event) ?? ++nextNativeId;
    nativeIds.set(event, nativeId);
    const client = [event.clientX, event.clientY];
    const plot = plotPoint(client);
    const unit = view.signal('unit');
    const offset = effectOffset(unit);
    events.push({
      sequence: events.length + 1, nativeId, phase, step, channel, type: event.type,
      vegaType: channel === 'vega' ? event.vegaType : null,
      time: event.timeStamp, observedAt: performance.now(), trusted: event.isTrusted,
      client, screen: [event.screenX, event.screenY], browserOffset: [event.offsetX, event.offsetY],
      plot, coordinatesInCurrentUnit: plot.map((value, i) => value - offset[i]),
      button: event.button ?? null, buttons: event.buttons ?? null, detail: event.detail ?? null,
      pointerType: event.pointerType ?? null, pointerId: event.pointerId ?? null,
      modifiers: {alt: event.altKey, ctrl: event.ctrlKey, meta: event.metaKey, shift: event.shiftKey},
      defaultPreventedAtCallback: event.defaultPrevented, target: domPath(event.target),
      activeElement: domPath(document.activeElement), item: describeItem(item)
    });
  }

  function traverse(mark, parents, callback) {
    for (const item of mark?.items ?? []) {
      callback(item, parents);
      if (mark.marktype === 'group') {
        for (const child of item.items ?? []) {
          traverse(child, [parents[0] + (item.x ?? 0), parents[1] + (item.y ?? 0)], callback);
        }
      }
    }
  }

  function inspectScene() {
    const bars = [];
    const axes = [];
    const brush = {};
    traverse(view.scenegraph().root, [0, 0], (item, offset) => {
      if (item.mark?.name === 'marks') {
        bars.push({
          key: `${+item.datum.month_date}:${item.datum.weather}`, month: +item.datum.month_date,
          weather: item.datum.weather, count: item.datum.__count,
          countStart: item.datum.__count_start, countEnd: item.datum.__count_end,
          bounds: bounds(item, offset), fill: item.fill, item: describeItem(item)
        });
      }
      if (['axis-label', 'axis-title'].includes(item.mark?.role)) {
        axes.push({
          role: item.mark.role, text: item.text, x: item.x + offset[0], y: item.y + offset[1],
          opacity: item.opacity ?? null, font: item.font
        });
      }
      if (['drag_brush_brush', 'drag_brush_brush_bg'].includes(item.mark?.name)) {
        brush[item.mark.name] = {
          bounds: bounds(item, offset), rect: [item.x, item.y, item.x2, item.y2],
          fill: item.fill, stroke: item.stroke ?? null, mark: markIdentity(item)
        };
      }
    });
    bars.sort((a, b) => a.month - b.month || a.weather.localeCompare(b.weather, 'en-US'));
    return {bars, axes, brush};
  }

  function scaleDetails() {
    const x = view.scale('x');
    const y = view.scale('y');
    const color = view.scale('color');
    return {
      bands: x.domain().map(value => ({value: +value, start: x(value), end: x(value) + x.bandwidth()})),
      xStep: x.step(), yDomain: y.domain(), yRange: y.range(),
      colors: Object.fromEntries(color.domain().map(value => [value, color(value)]))
    };
  }

  function sample() {
    const {bars, axes, brush} = inspectScene();
    const store = view.data('drag_brush_store');
    const source = view.data('source_0');
    const aggregate = source.map(d => [
      +d.month_date, d.weather, d.__count, d.__count_start, d.__count_end
    ]).sort((a, b) => a[0] - b[0] || a[1].localeCompare(b[1], 'en-US'));
    const unit = view.signal('unit');
    return {
      plot: coordinateSystem(), visual: clone(view.signal('drag_brush_x')),
      dataExtent: view.signal('drag_brush_month_date')?.map(monthValue) ?? null,
      projected: store[0]?.values[0]?.map(monthValue) ?? null,
      tupleStore: clone(store), fieldDefinition: clone(view.signal('drag_brush_tuple_fields')),
      translateAnchor: hasTranslate ? clone(view.signal('drag_brush_translate_anchor')) : null,
      translateDelta: hasTranslate ? clone(view.signal('drag_brush_translate_delta')) : null,
      unit: {chain: groupChain(unit), offset: effectOffset(unit)},
      brush, axes, scales: scaleDetails(), aggregate,
      geometry: bars.map(b => [b.key, b.count, b.bounds]),
      fills: Object.fromEntries(bars.map(b => [b.key, b.fill]))
    };
  }

  function raster() {
    const node = surface();
    return node.localName === 'canvas' ? node.toDataURL() : node.outerHTML;
  }

  window.af123 = {
    async prepare(input) {
      const face = new FontFace(input.fontFamily, `url(data:font/ttf;base64,${input.fontBase64})`);
      document.fonts.add(await face.load());
      const loader = vega.loader();
      loader.load = async uri => {
        loads.push(uri);
        if (uri !== 'data/seattle-weather.csv') throw new Error(`unexpected data URL: ${uri}`);
        return input.csv;
      };
      compiled = vegaLite.compile(input.spec, {config: {font: input.fontFamily}}).spec;
      hasTranslate = compiled.signals.some(signal => signal.name === 'drag_brush_translate_anchor');
      const logger = vega.logger(vega.Warn);
      view = new vega.View(vega.parse(compiled), {
        renderer: input.renderer, loader, logger
      }).initialize(mount);
      await view.runAsync();
      if (input.observers) {
        for (const type of eventTypes) document.addEventListener(type, e => record('dom', e), true);
        for (const type of viewTypes) {
          view.addEventListener(type, (e, item) => record('vega', e, item));
        }
      }
      await frame();
      const {bars, axes, brush} = inspectScene();
      return {
        compiled, loads, timeOrigin: performance.timeOrigin, system: coordinateSystem(),
        bars, axes, brush, scales: scaleDetails(), raster: raster(),
        versions: {vega: vega.version, vegaLiteEmbedded: vegaLite.version},
        font: document.fonts.check(`12px "${input.fontFamily}"`),
        lang: navigator.language, timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        userAgent: navigator.userAgent
      };
    },
    begin(message) {
      ({phase, step} = message);
      return performance.now();
    },
    async observe(client) {
      const raf = await frame();
      const first = sample();
      const hitAfter = client ? domPath(document.elementFromPoint(...client)) : null;
      const raf2 = await frame();
      const next = sample();
      const nextChanges = Object.fromEntries(
        Object.entries(next).filter(([key, value]) => JSON.stringify(value) !== JSON.stringify(first[key]))
      );
      const snap = {phase, step, raf, raf2, hitAfter, first, nextChanges};
      snapshots.push(snap);
      return snap;
    },
    collect() {
      return {events, snapshots, finalRaster: raster()};
    }
  };
})();
