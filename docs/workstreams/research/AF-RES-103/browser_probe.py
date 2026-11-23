"""Open exact local files in fresh Chromium contexts with offline routing."""
from base64 import b64decode
from collections import Counter
from hashlib import sha256
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from playwright.sync_api import Error, sync_playwright

SCRIPT = """async ({queries, extra}) => {
    await document.fonts.ready;
    const imgs = [...document.images];
    const images = await Promise.all(imgs.map(async (im, index) => {
        let decoded;
        try { await im.decode(); decoded = true; } catch { decoded = false; }
        const rect = im.getBoundingClientRect();
        return {index: index + 1, decoded, complete: im.complete,
            src: im.getAttribute('src').startsWith('data:') ?
                im.getAttribute('src').split(',', 1)[0] : im.getAttribute('src'),
            natural: [im.naturalWidth, im.naturalHeight],
            rendered: [rect.x, rect.y + scrollY, rect.width, rect.height],
            alt: im.getAttribute('alt')};
    }));
    const walker = document.createTreeWalker(document.body,
        NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    const order = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (n.nodeName === 'IMG') order.push({image: imgs.indexOf(n) + 1});
        else if (n.nodeType === Node.TEXT_NODE && n.textContent.trim() &&
            !n.parentElement.closest('style,script,template,noscript'))
            order.push({text: n.textContent.replace(/\\s+/g,' ').trim()});
    }
    const find = {};
    for (const query of queries) {
        getSelection().removeAllRanges();
        scrollTo(0,0);
        const found = window.find(query, true, false, true, false, false, false);
        find[query] = {found, selected: getSelection().toString()};
    }
    getSelection().removeAllRanges();
    scrollTo(0,0);
    const colors = {};
    for (const selector of extra) {
        const el = document.querySelector(selector);
        const rect = el.getBoundingClientRect();
        const paint = getComputedStyle(el);
        colors[selector] = {color:paint.color, fill:paint.fill,
            rect:[rect.x, rect.y, rect.width, rect.height]};
    }
    return {images, order, find, colors, body: document.body.innerText,
        headings:[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(x=>x.innerText),
        rendered_body_font:getComputedStyle(document.body).fontFamily,
        viewport:[innerWidth,innerHeight,devicePixelRatio]};
}"""


class Browser:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            executable_path=self.path, headless=True, args=["--no-sandbox"]
        )
        return self

    def __exit__(self, *_):
        self.browser.close()
        self.playwright.stop()

    def probe(self, file, output, label, queries=(), extra=(), try_file=False, per_image=True):
        """Use only document files next to file on the synthetic loopback origin."""
        requests, failures, responses, console = [], [], [], []
        origin = "http://127.0.0.1:8765"
        context = self.browser.new_context(offline=True, viewport={"width":1100,"height":1250},
                                           device_scale_factor=1, service_workers="block")
        def open_page():
            page = context.new_page()
            page.on("request", lambda q: requests.append(q.url))
            page.on("response", lambda r: responses.append([r.url,r.status]))
            page.on("requestfailed", lambda q: failures.append([q.url,q.failure]))
            page.on("pageerror", lambda e: console.append(str(e)))
            return page

        def from_disk(route):
            url = urlsplit(route.request.url)
            target = (file.parent / unquote(url.path).lstrip("/")).resolve()
            if not route.request.url.startswith(origin + "/") or not target.is_relative_to(file.parent):
                route.abort("internetdisconnected")
            elif target.is_file():
                mime = mimetypes.guess_type(target)[0] or "application/octet-stream"
                route.fulfill(status=200, content_type=mime, body=target.read_bytes())
            else:
                route.fulfill(status=404, content_type="text/plain", body=b"Missing local resource")
        context.route("**/*", from_disk)
        page = open_page()
        transport = "local-bytes-offline-loopback"
        file_error = None
        try:
            if try_file:
                try:
                    page.goto(file.as_uri(), wait_until="load", timeout=10000)
                    transport = "file-url-offline"
                except Error as exc:
                    file_error = str(exc)
                    page.close()
                    page = open_page()
            if transport != "file-url-offline":
                page.goto(origin + "/" + file.name, wait_until="load", timeout=10000)
            page.wait_for_function("!document.documentElement.classList.contains('reftest-wait')",
                                   timeout=10000)
            result = page.evaluate(SCRIPT, {"queries":list(queries),"extra":list(extra)})
            captured = output / (label + ".png")
            page.screenshot(path=captured, full_page=len(result["images"]) <= 3, animations="disabled")
            data_hashes = page.evaluate("""() => [...document.images].map(i=>i.getAttribute('src'))""")
            for image, raw in zip(result["images"],data_hashes):
                if raw.startswith("data:image/svg+xml;base64,"):
                    decoded = b64decode(raw.split(",",1)[1],validate=True)
                    image["svg_payload_sha256"] = sha256(decoded).hexdigest()
                if per_image and image["decoded"]:
                    name = f'{label}-img{image["index"]:02d}.png'
                    page.locator("img").nth(image["index"] - 1).screenshot(path=output/name, animations="disabled")
                    image["screenshot"] = name
            result.update({
                "status":"viewed","browser":self.browser.version,"source":file.name,
                "transport":transport,"file_url_error":file_error,"offline":True,
                "requests":requests,"responses":responses,"request_failures":failures,"page_errors":console,
            })
            return result
        except Error as exc:
            return {"status":"unviewable","error":str(exc),"requests":requests,"failures":failures,
                    "file_url_error":file_error,"transport":transport}
        finally:
            context.close()


def inspect_svg(filename):
    root = ET.parse(filename).getroot()
    key = "{http://www.w3.org/1999/xlink}href"
    ids = {e.get("id") for e in root.iter() if e.get("id")}
    hrefs = [e.get(key,e.get("href")) for e in root.iter() if e.get(key) or e.get("href")]
    return {
        "root": root.attrib,
        "tags": dict(Counter(e.tag.split("}")[-1] for e in root.iter())),
        "paint_attributes": dict(Counter(e.get("style","") for e in root.iter() if e.get("style"))),
        "fills": dict(Counter(e.get("fill") for e in root.iter() if e.get("fill"))),
        "strokes": dict(Counter(e.get("stroke") for e in root.iter() if e.get("stroke"))),
        "text_nodes": ["".join(e.itertext()) for e in root.iter() if e.tag.endswith("}text")],
        "data_text": "".join(e.get("data-text","") for e in root.iter()),
        "external_href": [h for h in hrefs if not h.startswith("#")],
        "unresolved_local_href": [h for h in hrefs if h.startswith("#") and h[1:] not in ids],
    }
