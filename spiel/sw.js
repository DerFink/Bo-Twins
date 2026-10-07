/* The Bo Twins: Service Worker
   - App-Dateien: zuerst Netz, sonst Zwischenspeicher (App startet auch ohne Empfang)
   - Bibliotheken (Leaflet, Chart.js, Tailwind, Schriften): einmal laden, dann aus dem Zwischenspeicher
   - Kartenkacheln: nur was angezeigt wurde, wird gespeichert und beim nächsten Mal nicht erneut geladen
   - Routing-Abfragen gehen immer direkt ins Netz */
const VER = 'v6';   // v6: Luftfahrtkarte (open flightmaps) mit auf 14 Tage begrenztem Zwischenspeicher; v5: Startdatei wird immer beim Server geprüft
const SHELL = 'bt-shell-' + VER;
const LIBS = 'bt-libs-' + VER;
const TILES = 'bt-tiles-' + VER;
const MAX_TILES = 5000;   // ca. 100 MB Obergrenze, älteste werden verworfen

const SHELL_FILES = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];
const LIB_URLS = [
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js',
  'https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap'
];
const TILE_HOST = /(^|\.)(tile\.openstreetmap\.org)$/;
const OFM_HOST = /(^|\.)(newaydata\.com)$/;                   // open flightmaps: Luftfahrtdaten dürfen nicht lange veralten
const OFM_PERIOD = 14 * 24 * 3600 * 1000;
const ofmName = () => 'bt-ofm-' + Math.floor(Date.now() / OFM_PERIOD);
const LIB_HOST = /(^|\.)(cdnjs\.cloudflare\.com|cdn\.tailwindcss\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net)$/;

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const shell = await caches.open(SHELL);
    await shell.addAll(SHELL_FILES);
    const libs = await caches.open(LIBS);
    for (const u of LIB_URLS) {            // Bibliotheken schon bei der Installation holen
      try { const r = await fetch(u, {mode: 'cors'}); if (r.ok) await libs.put(u, r); }
      catch (err) { try { await libs.put(u, await fetch(u, {mode: 'no-cors'})); } catch (e2) {} }
    }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('bt-') && ![SHELL, LIBS, TILES, ofmName()].includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (TILE_HOST.test(url.hostname)) { e.respondWith(tile(req)); return; }
  if (OFM_HOST.test(url.hostname)) { e.respondWith(ofmTile(req)); return; }
  if (url.origin === location.origin) { e.respondWith(shell(req)); return; }
  if (LIB_HOST.test(url.hostname)) { e.respondWith(lib(req)); return; }
  // alles andere (z. B. Straßenrouting) geht direkt ins Netz
});

async function shell(req) {
  const cache = await caches.open(SHELL);
  try {
    const res = await fetch(req, {cache: 'no-cache'});   // immer beim Server nachfragen, nicht den Browser-Cache nehmen
    if (res.ok) cache.put(req, res.clone());
    return res;
  } catch (err) {
    return (await cache.match(req, {ignoreSearch: true})) || (await cache.match('./index.html')) || Response.error();
  }
}

async function lib(req) {
  const cache = await caches.open(LIBS);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok || res.type === 'opaque') cache.put(req, res.clone());
  return res;
}

const keyOf = u => u;
let puts = 0;
function note(m) {
  self.clients.matchAll().then(cs => cs.forEach(c => c.postMessage(Object.assign({type: 'tile'}, m))));
}
async function trim(cache) {
  if (++puts % 50) return;
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_TILES; i++) await cache.delete(keys[i]);
}
async function tile(req) {
  const cache = await caches.open(TILES);
  const key = keyOf(req.url);
  const hit = await cache.match(key);
  if (hit) { note({hit: 1}); return hit; }
  try {
    const res = await fetch(req.url, {mode: 'cors', credentials: 'omit'});
    if (res.ok) {
      cache.put(key, res.clone()).then(() => trim(cache));
      const len = +res.headers.get('content-length');
      if (len) note({net: 1, bytes: len});
      else res.clone().arrayBuffer().then(b => note({net: 1, bytes: b.byteLength}));
    }
    return res;
  } catch (err) {
    try { const res = await fetch(req); note({net: 1, bytes: 20000}); return res; }
    catch (e2) { return Response.error(); }
  }
}

async function ofmTile(req) {                       // eigener Zwischenspeicher je 14 Tage; ältere werden gelöscht
  const name = ofmName();
  caches.keys().then(ks => ks.forEach(k => { if (k.startsWith('bt-ofm-') && k !== name) caches.delete(k); }));
  const cache = await caches.open(name);
  const hit = await cache.match(req.url);
  if (hit) { note({hit: 1}); return hit; }
  try {
    const res = await fetch(req.url, {mode: 'cors', credentials: 'omit'});
    if (res.ok) {
      cache.put(req.url, res.clone()).then(() => trim(cache));
      const len = +res.headers.get('content-length');
      if (len) note({net: 1, bytes: len});
      else res.clone().arrayBuffer().then(b => note({net: 1, bytes: b.byteLength}));
    }
    return res;
  } catch (err) {
    try { const res = await fetch(req); note({net: 1, bytes: 20000}); return res; }
    catch (e2) { return Response.error(); }
  }
}
