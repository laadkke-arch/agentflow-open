// WebDriver execute_async_script body. The normal WPT run never loads this file.
const selectors = arguments[0];
const done = arguments[arguments.length - 1];

function wordRects(element) {
  const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
  let text = '';
  const sourceNodes = [];
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.nodeName === 'BR') text += '\n';
    if (node.nodeType !== Node.TEXT_NODE) continue;
    sourceNodes.push({node, start: text.length, end: text.length + node.length});
    text += node.data;
  }

  const range = document.createRange();
  const words = Array.from(text.matchAll(/\S+/gu), (match, i) => {
    const fragments = [];
    const start = match.index;
    const end = start + match[0].length;
    for (const source of sourceNodes) {
      if (start >= source.end || end <= source.start) continue;
      range.setStart(source.node, Math.max(start, source.start) - source.start);
      range.setEnd(source.node, Math.min(end, source.end) - source.start);
      for (const rect of range.getClientRects()) {
        fragments.push({x: rect.x, y: rect.y, width: rect.width, height: rect.height});
      }
    }
    return {index: i + 1, text: match[0], fragments};
  });

  const tolerance = 0.5;
  const yValues = words.flatMap(word => word.fragments.map(rect => rect.y)).sort((a, b) => a - b);
  const rows = [];
  for (const y of yValues) {
    if (rows.length === 0 || y - rows[rows.length - 1].y > tolerance) rows.push({y});
  }
  for (const word of words) {
    for (const rect of word.fragments) {
      rect.line = 1 + rows.findIndex(row => Math.abs(rect.y - row.y) <= tolerance);
    }
  }

  for (const [i, row] of rows.entries()) {
    const line = i + 1;
    const lineWords = words.filter(word => word.fragments.some(rect => rect.line === line));
    const boxes = lineWords.map(word => {
      const fragments = word.fragments.filter(rect => rect.line === line);
      return {left: Math.min(...fragments.map(rect => rect.x)),
              right: Math.max(...fragments.map(rect => rect.x + rect.width))};
    });
    row.line = line;
    row.words = lineWords.map(word => word.index);
    row.text = lineWords.map(word => word.text).join(' ');
    row.advance = Math.max(...boxes.map(box => box.right)) - Math.min(...boxes.map(box => box.left));
    row.gaps = boxes.slice(1).map((box, k) => box.left - boxes[k].right);
  }

  const style = getComputedStyle(element);
  const box = element.getBoundingClientRect();
  const canvas = document.createElement('canvas').getContext('2d');
  canvas.font = `${style.fontSize} ${style.fontFamily}`;
  return {
    width: box.width, height: box.height, x: box.x, y: box.y,
    fontFamily: style.fontFamily, fontSize: style.fontSize, lineHeight: style.lineHeight,
    textWrap: style.textWrap, textWrapStyle: style.textWrapStyle, whiteSpace: style.whiteSpace,
    writingMode: style.writingMode, direction: style.direction,
    canvasSpace: canvas.measureText(' ').width, canvasZero: canvas.measureText('0').width,
    forcedBreakElements: element.querySelectorAll('br').length,
    words, rows,
  };
}

(async () => {
  const elements = selectors.map(selector => {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Selector not found: ${selector}`);
    return element;
  });
  const events = [];
  const describeFace = face => ({family: face.family, status: face.status});
  for (const type of ['loading', 'loadingdone', 'loadingerror']) {
    document.fonts.addEventListener(type, event => {
      events.push({type, at: performance.now(), faces: Array.from(event.fontfaces, describeFace)});
    }, {once: true});
  }
  for (const element of elements) element.getBoundingClientRect();
  const initialFaces = Array.from(document.fonts, describeFace);
  const before = performance.now();
  await document.fonts.ready;
  const after = performance.now();
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  done({
    url: location.href, viewport: [innerWidth, innerHeight], outer: [outerWidth, outerHeight],
    dpr: devicePixelRatio, documentWidth: document.documentElement.clientWidth,
    userAgent: navigator.userAgent, initialFaces, fontEvents: events,
    fontSetStatus: document.fonts.status, readyWaitMs: after - before,
    faces: Array.from(document.fonts, describeFace),
    fontResources: performance.getEntriesByType('resource').filter(entry => /\/fonts\//.test(entry.name)).map(entry => ({
      name: entry.name, responseStatus: entry.responseStatus ?? null, start: entry.startTime,
      responseEnd: entry.responseEnd, decodedBodySize: entry.decodedBodySize, transferSize: entry.transferSize,
    })),
    blocks: elements.map((element, i) => ({selector: selectors[i], ...wordRects(element)})),
  });
})().catch(error => done({error: String(error)}));
