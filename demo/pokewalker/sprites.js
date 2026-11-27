// A sprite folder, read in the browser and packed into the dex store the pet
// software reads (`pw_pet::dexstore`). The folder's layout is the one
// `preview/tools/sprite_folder.py` writes and its README describes:
//
//   pokemon/<dex>[-NAME]/front.png      battle picture, at most 96x96
//   pokemon/<dex>[-NAME]/front-2.png    its second frame (optional)
//   pokemon/<dex>[-NAME]/anim.txt       HeartGold animation timing (optional)
//   pokemon/<dex>[-NAME]/walk.png       walking sprite: 8 frames in a row,
//                                       back, front, left, right, two steps each
//   pokemon/<dex>[-NAME]/walk-shiny.png the same in shiny colours (optional)
//   pokemon/<dex>[-NAME]/sleep.png      one frame a facing with the eyes
//                                       closed, walk.png's colours (optional)
//   pokemon/<dex>[-NAME]/knockback.png  square frames: thrown back into the
//                                       wall by a knockout (optional)
//   pokemon/<dex>[-NAME]/cry.wav        the cry, 8-bit mono PCM WAV (optional)
//   room/room.bin                       pet mode's room (optional)
//   park/world.bin                      the open world's trees and buildings (optional)
//   team.txt                            dex numbers to walk with, one a line
//                                       (optional; else the first six)
//
// Pictures are any PNG: their colours are reduced to fifteen here, and any
// pixel more than half transparent is transparent.

export const MAX_FRAME = 96;
const TILE = 8;
const SMALL_W = 32, SMALL_H = 24;
const SCRIPT_LEN = 40;

/// Every file of a folder, from either an <input webkitdirectory> file list
/// or a base URL with an index.json beside it. Answers path -> () => Blob.
export async function folderFromFiles(files) {
  const map = new Map();
  for (const f of files) {
    const p = (f.webkitRelativePath || f.name).split('/');
    const at = p.indexOf('pokemon') >= 0 ? p.indexOf('pokemon') : p.indexOf('room') >= 0 ? p.indexOf('room') : p.length - 1;
    map.set(p.slice(at).join('/'), async () => f);
  }
  return map;
}

export async function folderFromUrl(base) {
  const res = await fetch(`${base}/index.json?v=f4158f6f-1795805886`);
  if (!res.ok) throw new Error(`${base}/index.json: ${res.status}`);
  const index = await res.json();
  const map = new Map();
  const names = ['front.png', 'front-2.png', 'anim.txt', 'walk.png', 'walk-shiny.png', 'sleep.png', 'knockback.png', 'cry.wav'];
  for (const entry of index.pokemon || []) {
    const dir = typeof entry === 'string' ? entry : entry.dir;
    const have = typeof entry === 'string' ? names : entry.files;
    for (const n of have) {
      map.set(`pokemon/${dir}/${n}`, async () => {
        const r = await fetch(`${base}/pokemon/${dir}/${n}`);
        if (!r.ok) throw new Error('missing');
        return r.blob();
      });
    }
  }
  if (index.store) map.set('dex.store', async () => (await fetch(`${base}/dex.store?v=f4158f6f-1795805886`)).blob());
  if (index.room) map.set('room/room.bin', async () => (await fetch(`${base}/room/room.bin?v=f4158f6f-1795805886`)).blob());
  if (index.world) map.set('park/world.bin', async () => (await fetch(`${base}/park/world.bin?v=f4158f6f-1795805886`)).blob());
  if (index.team) map.set('team.txt', async () => new Blob([index.team.join('\n')]));
  return map;
}

/// What a folder holds: species by dex, with names and the files they have.
export function species(folder) {
  const out = new Map();
  for (const path of folder.keys()) {
    const m = path.match(/^pokemon\/0*(\d+)(?:-([^/]+))?\/([^/]+)$/);
    if (!m) continue;
    const dex = Number(m[1]);
    if (!dex || dex > 65535) continue;
    const s = out.get(dex) || { dex, name: (m[2] || '').toUpperCase().slice(0, 15), files: new Map() };
    s.files.set(m[3], folder.get(path));
    out.set(dex, s);
  }
  return out;
}

async function pixels(blob) {
  const bmp = await createImageBitmap(blob);
  const c = new OffscreenCanvas(bmp.width, bmp.height);
  const g = c.getContext('2d');
  g.drawImage(bmp, 0, 0);
  return g.getImageData(0, 0, bmp.width, bmp.height);
}

/// Up to fifteen colours for every opaque pixel of `images`, by merging the
/// two nearest until few enough are left, weighted by how often each shows.
function reduce(images) {
  const counts = new Map();
  for (const im of images) {
    const d = im.data;
    for (let i = 0; i < d.length; i += 4) {
      if (d[i + 3] < 128) continue;
      const k = (d[i] << 16) | (d[i + 1] << 8) | d[i + 2];
      counts.set(k, (counts.get(k) || 0) + 1);
    }
  }
  let cs = [...counts].map(([k, n]) => ({ r: k >> 16, g: (k >> 8) & 255, b: k & 255, n }));
  while (cs.length > 15) {
    let best = [Infinity, 0, 1];
    for (let a = 0; a < cs.length; a++) for (let b = a + 1; b < cs.length; b++) {
      const d = (cs[a].r - cs[b].r) ** 2 + (cs[a].g - cs[b].g) ** 2 + (cs[a].b - cs[b].b) ** 2;
      if (d < best[0]) best = [d, a, b];
    }
    const [, a, b] = best, A = cs[a], B = cs[b], n = A.n + B.n;
    cs[a] = { r: (A.r * A.n + B.r * B.n) / n, g: (A.g * A.n + B.g * B.n) / n, b: (A.b * A.n + B.b * B.n) / n, n };
    cs.splice(b, 1);
  }
  return cs.map(c => [Math.round(c.r), Math.round(c.g), Math.round(c.b)]);
}

function nearest(pal, r, g, b) {
  let best = 1, bd = Infinity;
  for (let i = 0; i < pal.length; i++) {
    const d = (pal[i][0] - r) ** 2 + (pal[i][1] - g) ** 2 + (pal[i][2] - b) ** 2;
    if (d < bd) { bd = d; best = i + 1; }
  }
  return best;
}

/// One region of an image as 4-bit indices into `pal` (slot 0 transparent),
/// placed at `(ox, oy)` in a `w` x `h` frame.
function indices(im, sx, sy, sw, sh, pal, w, h, ox, oy) {
  const out = new Uint8Array(w * h);
  for (let y = 0; y < sh; y++) for (let x = 0; x < sw; x++) {
    const tx = ox + x, ty = oy + y;
    if (tx < 0 || ty < 0 || tx >= w || ty >= h) continue;
    const i = ((sy + y) * im.width + sx + x) * 4;
    if (im.data[i + 3] < 128) continue;
    out[ty * w + tx] = nearest(pal, im.data[i], im.data[i + 1], im.data[i + 2]);
  }
  return out;
}

function pack4(idx) {
  const out = new Uint8Array(Math.ceil(idx.length / 2));
  for (let i = 0; i < idx.length; i++) out[i >> 1] |= i % 2 === 0 ? idx[i] & 15 : (idx[i] & 15) << 4;
  return out;
}

const up = (n, t) => Math.ceil(n / t) * t;

/// A species' battle picture as a `PWPET4` pack (`pw_pet::pet`).
export async function encodePet(s) {
  const f1 = s.files.get('front.png');
  if (!f1) return null;
  const a = await pixels(await f1());
  const f2 = s.files.get('front-2.png');
  const b = f2 ? await pixels(await f2()).catch(() => a) : a;
  const w = Math.min(MAX_FRAME, up(Math.max(a.width, b.width), TILE));
  const h = Math.min(MAX_FRAME, up(Math.max(a.height, b.height), TILE));
  const pal = reduce([a, b]);
  const frame = im => indices(im, 0, 0, Math.min(im.width, w), Math.min(im.height, h), pal, w, h,
    Math.floor((w - Math.min(im.width, w)) / 2), h - Math.min(im.height, h));
  const big = [frame(a), frame(b)];
  const small = big.map(f => {
    const out = new Uint8Array(SMALL_W * SMALL_H);
    const k = Math.max(w / SMALL_W, h / SMALL_H, 1);
    for (let y = 0; y < SMALL_H; y++) for (let x = 0; x < SMALL_W; x++) {
      const fx = Math.floor(x * k), fy = Math.floor(y * k);
      if (fx < w && fy < h) out[y * SMALL_W + x] = f[fy * w + fx];
    }
    return out;
  });
  let script = new Uint8Array(SCRIPT_LEN).fill(0xff);
  const anim = s.files.get('anim.txt');
  if (anim) {
    try {
      const hex = (await (await anim()).text()).trim();
      if (/^[0-9a-f]{80}$/i.test(hex)) script = Uint8Array.from(hex.match(/../g), x => parseInt(x, 16));
    } catch (_) { }
  }
  const parts = [];
  const head = new Uint8Array(34);
  head.set(new TextEncoder().encode('PWPET4\0\0'), 0);
  const dv = new DataView(head.buffer);
  dv.setUint16(8, s.dex, true);
  head[10] = 5;
  dv.setUint16(12, 20, true);
  dv.setUint16(14, 20, true);
  head.set(new TextEncoder().encode((s.name || '').slice(0, 15)), 16);
  head[32] = w; head[33] = h;
  parts.push(head, pack4(big[0]), pack4(big[1]), pack4(small[0]), pack4(small[1]));
  const p = new Uint8Array(48);
  pal.forEach((c, i) => p.set(c, 3 * (i + 1)));
  parts.push(p, script);
  const fk = s.files.get('knockback.png');
  if (fk) {
    try {
      const k = await pixels(await fk());
      const side = k.height, n = Math.floor(k.width / side);
      if (side > 0 && side <= 128 && k.width % side === 0 && n > 0 && n <= 12 && (side * side) % 2 === 0) {
        parts.push(Uint8Array.of(side, side, n));
        for (let i = 0; i < n; i++) parts.push(pack4(indices(k, i * side, 0, side, side, pal, side, side, 0, 0)));
      }
    } catch (_) { }
  }
  return concat(parts);
}

/// A species' walking sprite as a follower record (`pw_pet::dexstore::Follower`).
export async function encodeFollower(s) {
  const f = s.files.get('walk.png');
  if (!f) return null;
  const im = await pixels(await f());
  const fw = Math.floor(im.width / 8), fh = im.height;
  if (!fw || fw > 255 || fh > 255 || (fw * fh) % 2) return null;
  const pal = reduce([im]);
  const frames = [];
  for (let k = 0; k < 8; k++) frames.push(pack4(indices(im, k * fw, 0, fw, fh, pal, fw, fh, 0, 0)));
  const fz = s.files.get('sleep.png');
  if (fz) {
    try {
      const sl = await pixels(await fz());
      if (sl.width === fw * 4 && sl.height === fh) {
        for (let k = 0; k < 4; k++) frames.push(pack4(indices(sl, k * fw, 0, fw, fh, pal, fw, fh, 0, 0)));
      }
    } catch (_) { }
  }
  let shinyPal = null;
  const fs = s.files.get('walk-shiny.png');
  if (fs) {
    try {
      const sh = await pixels(await fs());
      if (sh.width === im.width && sh.height === im.height) {
        const sums = pal.map(() => [0, 0, 0, 0]);
        for (let i = 0; i < im.data.length; i += 4) {
          if (im.data[i + 3] < 128 || sh.data[i + 3] < 128) continue;
          const k = nearest(pal, im.data[i], im.data[i + 1], im.data[i + 2]) - 1;
          sums[k][0] += sh.data[i]; sums[k][1] += sh.data[i + 1]; sums[k][2] += sh.data[i + 2]; sums[k][3]++;
        }
        shinyPal = sums.map((t, i) => t[3] ? [t[0] / t[3], t[1] / t[3], t[2] / t[3]].map(Math.round) : pal[i]);
      }
    } catch (_) { }
  }
  const head = new Uint8Array(4 + 48);
  head[0] = fw; head[1] = fh; head[2] = frames.length; head[3] = shinyPal ? 1 : 0;
  pal.forEach((c, i) => head.set(c, 4 + 3 * (i + 1)));
  const parts = [head, ...frames];
  if (shinyPal) {
    const p = new Uint8Array(48);
    shinyPal.forEach((c, i) => p.set(c, 3 * (i + 1)));
    parts.push(p);
  }
  return concat(parts);
}

/// The largest cry taken: a few seconds at the cartridge's rate.
const MAX_CRY_BYTES = 64 * 1024;

/// A cry WAV as the dex store keeps it: 8-bit *signed* mono PCM and its rate
/// (`pw_graphics::wav`). Anything but 8-bit mono PCM is not a cry.
export async function encodeCry(s) {
  const f = s.files.get('cry.wav');
  if (!f) return null;
  const b = new Uint8Array(await (await f()).arrayBuffer());
  const dv = new DataView(b.buffer, b.byteOffset, b.byteLength);
  const tag = at => String.fromCharCode(b[at], b[at + 1], b[at + 2], b[at + 3]);
  if (b.length < 12 || tag(0) !== 'RIFF' || tag(8) !== 'WAVE') return null;
  let at = 12, rate = 0;
  while (at + 8 <= b.length) {
    const id = tag(at), len = dv.getUint32(at + 4, true);
    if (at + 8 + len > b.length) return null;
    if (id === 'fmt ') {
      if (dv.getUint16(at + 8, true) !== 1 || dv.getUint16(at + 10, true) !== 1 || dv.getUint16(at + 22, true) !== 8) return null;
      rate = Math.min(65535, dv.getUint32(at + 12, true));
    } else if (id === 'data') {
      if (!rate) return null;
      const pcm = b.slice(at + 8, at + 8 + Math.min(len, MAX_CRY_BYTES)).map(v => v ^ 0x80);
      return { pcm, rate };
    }
    at += 8 + len + (len & 1);
  }
  return null;
}

/// Every species of a folder as one dex store (`PWDEX2`).
export async function buildStore(list, onProgress) {
  const dexes = [...list.keys()].sort((a, b) => a - b);
  if (!dexes.length) return null;
  const first = dexes[0], count = dexes[dexes.length - 1] - first + 1;
  const packs = new Array(count).fill(null), fols = new Array(count).fill(null), cries = new Array(count).fill(null);
  let done = 0;
  for (const dex of dexes) {
    const s = list.get(dex);
    packs[dex - first] = await encodePet(s).catch(() => null);
    fols[dex - first] = await encodeFollower(s).catch(() => null);
    cries[dex - first] = await encodeCry(s).catch(() => null);
    if (onProgress) onProgress(++done, dexes.length);
  }
  const headLen = 16 + 16 * count;
  let at = headLen;
  const head = new Uint8Array(headLen);
  const dv = new DataView(head.buffer);
  head.set(new TextEncoder().encode('PWDEX2\0\0'), 0);
  dv.setUint16(8, first, true);
  dv.setUint16(10, count, true);
  const body = [];
  for (let i = 0; i < count; i++) {
    const p = packs[i];
    dv.setUint32(16 + 16 * i, p ? at : 0, true);
    dv.setUint32(20 + 16 * i, p ? p.length : 0, true);
    if (p) { body.push(p); at += p.length; }
  }
  for (let i = 0; i < count; i++) {
    const c = cries[i];
    dv.setUint32(24 + 16 * i, at, true);
    dv.setUint16(28 + 16 * i, c ? c.rate : 0, true);
    if (c) { body.push(c.pcm); at += c.pcm.length; }
  }
  const folAt = at;
  dv.setUint32(12, folAt, true);
  const table = new Uint8Array(8 * count);
  const tv = new DataView(table.buffer);
  at += table.length;
  const folBody = [];
  for (let i = 0; i < count; i++) {
    const f = fols[i];
    tv.setUint32(8 * i, f ? at : 0, true);
    tv.setUint32(8 * i + 4, f ? f.length : 0, true);
    if (f) { folBody.push(f); at += f.length; }
  }
  return concat([head, ...body, table, ...folBody]);
}

function concat(parts) {
  const out = new Uint8Array(parts.reduce((n, p) => n + p.length, 0));
  let at = 0;
  for (const p of parts) { out.set(p, at); at += p.length; }
  return out;
}
