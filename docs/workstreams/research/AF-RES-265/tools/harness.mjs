import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const size = 384;
const basisPath = '/three/examples/jsm/libs/basis/';
const textureSlots = [
  'map', 'metalnessMap', 'roughnessMap', 'aoMap', 'normalMap', 'clearcoatNormalMap',
  'anisotropyMap', 'emissiveMap', 'transmissionMap', 'thicknessMap',
];
const message = err => String(err?.message ?? err);

async function hash(bytes) {
  const result = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(result), byte => byte.toString(16).padStart(2, '0')).join('');
}

function describeTexture(texture) {
  const image = texture?.image;
  if (!image) return null;
  return { width: image.width, height: image.height, compressed: Boolean(texture.isCompressedTexture),
    format: texture.format, type: texture.type, levels: texture.mipmaps.length, colorSpace: texture.colorSpace,
    channel: texture.channel, name: texture.name };
}

async function attribute(attr) {
  const width = attr.itemSize;
  const array = attr.isInterleavedBufferAttribute ? attr.data.array : attr.array;
  const componentBytes = array.BYTES_PER_ELEMENT;
  const bytes = new Uint8Array(attr.count * width * componentBytes);
  const raw = new Uint8Array(array.buffer, array.byteOffset, array.byteLength);
  const min = Array(width).fill(Infinity), max = Array(width).fill(-Infinity);
  let first, last;
  for (let i = 0; i < attr.count; i++) {
    const index = attr.isInterleavedBufferAttribute ? i * attr.data.stride + attr.offset : i * width;
    const start = index * componentBytes;
    bytes.set(raw.subarray(start, start + width * componentBytes), i * width * componentBytes);
    const values = Array.from(array.subarray(index, index + width));
    if (i === 0) first = values;
    last = values;
    values.forEach((value, axis) => {
      min[axis] = Math.min(value, min[axis]);
      max[axis] = Math.max(value, max[axis]);
    });
  }
  return { count: attr.count, width, type: array.constructor.name, first, last, min, max,
    logicalBytes: bytes.length, sha256: await hash(bytes) };
}

function traceImages(loader, result) {
  loader.register(parser => {
    const read = parser.loadImageSource;
    const attach = parser.loadTextureImage;
    parser.loadImageSource = function (index, decoder) {
      const def = this.json.images[index];
      const event = { index, decoder: decoder.constructor.name, uri: def.uri ?? null,
        bufferView: def.bufferView ?? null, mimeType: def.mimeType ?? null };
      result.decode.push(event);
      const pending = read.call(this, index, decoder);
      return pending.then(texture => {
        event.decoded = describeTexture(texture);
        return texture;
      }, error => {
        event.error = message(error);
        throw error;
      });
    };
    parser.loadTextureImage = function (texture, image, decoder) {
      const event = { texture, image, decoder: decoder.constructor.name };
      result.textureSelections.push(event);
      const pending = attach.call(this, texture, image, decoder);
      return pending.then(loaded => {
        event.bound = Boolean(loaded);
        return loaded;
      });
    };
    return { name: 'AF_RES_265_READ_TRACE' };
  });
}

function getPixels(gl) {
  const bytes = new Uint8Array(size * size * 4);
  gl.readPixels(0, 0, size, size, gl.RGBA, gl.UNSIGNED_BYTE, bytes);
  return bytes;
}

async function frameStats(base, rgba) {
  const total = size * size;
  let foreground = 0;
  const sum = [0, 0, 0];
  let squareDifference = 0;
  for (let i = 0; i < rgba.length; i += 4) {
    const delta = Array.from({length: 3}, (_, c) => Math.abs(rgba[i + c] - base[i + c]));
    if (Math.max(...delta) < 3) continue;
    foreground++;
    for (let c = 0; c < 3; c++) {
      sum[c] += rgba[i + c];
      squareDifference += delta[c] ** 2;
    }
  }
  const background = Array.from(base.slice(0, 4));
  return { width: size, height: size, format: 'RGBA8 bottom-left first', total,
    foreground, background, pixelsSha256: await hash(rgba), blankSha256: await hash(base),
    meanRGB: foreground ? sum.map(sumChannel => sumChannel / foreground) : null,
    rmsFromBlank: Math.sqrt(squareDifference / (total * 3)) };
}

function stage(renderer) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#171b22');
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(3, 2, 4);
  camera.lookAt(0, 0, 0);
  const light = new THREE.DirectionalLight(0xffffff, 3);
  light.position.set(3, 4, 2);
  const fill = new THREE.DirectionalLight(0xffffff, 1.4);
  fill.position.set(-3, 0.5, -2);
  scene.add(light, fill, new THREE.HemisphereLight(0xe0e8ff, 0x40352e, 0.6));
  const room = new RoomEnvironment();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = pmrem.fromScene(room, 0.04);
  scene.environment = env.texture;
  scene.environmentIntensity = 0.75;
  room.dispose();
  pmrem.dispose();
  return { scene, camera, env };
}

window.afProbe = async () => {
  const check = async target => {
    try {
      const response = await fetch(target);
      await response.arrayBuffer();
      return { status: response.status };
    } catch (error) { return { error: message(error) }; }
  };
  return { absent: await check('/asset/absent-probe.bin'),
    external: await check('https://example.invalid/af-res-265') };
};

window.afRun = async config => {
  const result = { three: THREE.REVISION, geometry: [], materials: [], decode: [],
    textureSelections: [], manager: [], callbacks: [], draw: null, frame: null };
  let renderer, ktx, env;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: false, alpha: false, preserveDrawingBuffer: true,
      powerPreference: 'low-power' });
    renderer.setSize(size, size, false);
    renderer.setPixelRatio(1);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.NoToneMapping;
    document.body.appendChild(renderer.domElement);
    const gl = renderer.getContext();
    const debug = gl.getExtension('WEBGL_debug_renderer_info');
    result.graphics = {
      version: gl.getParameter(gl.VERSION), vendor: debug && gl.getParameter(debug.UNMASKED_VENDOR_WEBGL),
      renderer: debug && gl.getParameter(debug.UNMASKED_RENDERER_WEBGL), colorSpace: renderer.outputColorSpace,
      toneMapping: renderer.toneMapping,
    };
    const manager = new THREE.LoadingManager();
    manager.onStart = (url, loaded, total) => result.manager.push({event: 'start', url, loaded, total});
    manager.onError = url => result.manager.push({event: 'error', url});
    manager.onProgress = (url, loaded, total) => result.manager.push({event: 'progress', url, loaded, total});
    manager.onLoad = () => result.manager.push({event: 'load'});
    const loader = new GLTFLoader(manager);
    traceImages(loader, result);
    if (config.decoder) {
      ktx = new KTX2Loader(manager).setTranscoderPath(basisPath).setWorkerLimit(1).detectSupport(renderer);
      loader.setKTX2Loader(ktx);
      result.decoder = {transcoderPath: basisPath, workerConfig: ktx.workerConfig};
    }
    let asset;
    try {
      asset = await new Promise((resolve, reject) => loader.load('/asset/' + config.entry, asset => {
        result.callbacks.push('onLoad');
        resolve(asset);
      }, undefined, error => {
        result.callbacks.push('onError');
        reject(error);
      }));
      result.load = 'resolved';
    } catch (error) {
      result.load = 'rejected';
      result.error = message(error);
      return result;
    }
    let rendered = [];
    const meshes = [];
    asset.scene.traverse(node => { if (node.isMesh) meshes.push(node); });
    result.extensionsRequired = asset.parser.json.extensionsRequired ?? [];
    for (const mesh of meshes) {
      const assoc = asset.parser.associations.get(mesh) ?? {};
      const material = mesh.material;
      const slots = Object.fromEntries(textureSlots.filter(slot => material[slot]).map(slot => {
        const texture = material[slot];
        const index = asset.parser.associations.get(texture)?.textures ?? null;
        const selection = result.textureSelections.find(event => event.texture === index && event.bound);
        return [slot, { ...describeTexture(texture), textureIndex: index, imageIndex: selection?.image ?? null }];
      }));
      result.materials.push({mesh: assoc.meshes ?? null, primitive: assoc.primitives ?? null,
        index: asset.parser.associations.get(material)?.materials ?? null,
        type: material.type, name: material.name, color: material.color?.toArray(), slots,
        transmission: material.transmission ?? null, clearcoat: material.clearcoat ?? null,
        anisotropy: material.anisotropy ?? null});
      result.geometry.push({ mesh: assoc.meshes ?? null, primitive: assoc.primitives ?? null, name: mesh.name,
        POSITION: await attribute(mesh.geometry.getAttribute('position')), indices: await attribute(mesh.geometry.index) });
      mesh.onBeforeRender = () => rendered.push({ mesh: assoc.meshes, primitive: assoc.primitives, name: mesh.name });
    }
    if (config.render) {
      const room = stage(renderer);
      env = room.env;
      const {scene, camera} = room;
      renderer.render(scene, camera);
      const blank = getPixels(gl);
      const bounds = new THREE.Box3().setFromObject(asset.scene);
      const extent = bounds.getSize(new THREE.Vector3());
      const center = bounds.getCenter(new THREE.Vector3());
      const scale = 2 / Math.max(extent.x, extent.y, extent.z);
      const unit = new THREE.Group();
      unit.scale.setScalar(scale);
      unit.position.copy(center).multiplyScalar(-scale);
      unit.add(asset.scene);
      scene.add(unit);
      rendered = [];
      renderer.render(scene, camera);
      const rgba = getPixels(gl);
      result.draw = { callbacks: rendered, ...renderer.info.render, glError: gl.getError(),
        bounds: [bounds.min.toArray(), bounds.max.toArray()], uniformScale: scale };
      result.frame = await frameStats(blank, rgba);
      result.png = renderer.domElement.toDataURL('image/png');
    }
    return result;
  } catch (error) {
    result.harnessError = message(error);
    return result;
  } finally {
    env?.dispose();
    ktx?.dispose();
    renderer?.dispose();
  }
};
