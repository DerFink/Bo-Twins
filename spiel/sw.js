/* Gasballon-Simulator: Service Worker (eigener Geltungsbereich /spiel/, eigene Zwischenspeicher mit Vorsatz gb-)
   - App-Dateien: zuerst Netz, sonst Zwischenspeicher (das Spiel startet auch ohne Empfang)
   - Bibliotheken (Leaflet, Schriften): einmal laden, dann aus dem Zwischenspeicher
   - Kartenkacheln: nur was angezeigt wurde, wird gespeichert und beim nächsten Mal nicht erneut geladen
   Vorlage: Service Worker der Tracker-App (v6) */
const VER = 'v20';
const SHELL = 'gb-shell-' + VER;
const LIBS = 'gb-libs-' + VER;
const TILES = 'gb-tiles-' + VER;
const MAX_TILES = 5000;   // ca. 100 MB Obergrenze, älteste werden verworfen

const SHELL_FILES = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];
const LIB_URLS = [
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
  'https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap'
];
const TILE_HOST = /(^|\.)(tile\.openstreetmap\.org)$/;
const LIB_HOST = /(^|\.)(cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/;

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const shell = await caches.open(SHELL);
    await shell.addAll(SHELL_FILES);
    const libs = await caches.open(LIBS);
    for (const u of LIB_URLS) {
      try { const r = await fetch(u, {mode: 'cors'}); if (r.ok) await libs.put(u, r); }
      catch (err) { try { await libs.put(u, await fetch(u, {mode: 'no-cors'})); } catch (e2) {} }
    }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('gb-') && ![SHELL, LIBS, TILES].includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (TILE_HOST.test(url.hostname)) { e.respondWith(tile(req)); return; }
  if (url.origin === location.origin) { e.respondWith(shell(req)); return; }
  if (LIB_HOST.test(url.hostname)) { e.respondWith(lib(req)); return; }
  // alles andere (später Wetter, Orte, Routing) geht direkt ins Netz
});

async function shell(req) {
  const cache = await caches.open(SHELL);
  try {
    const res = await fetch(req, {cache: 'no-cache'});   // immer beim Server nachfragen
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

let puts = 0;
async function trim(cache) {
  if (++puts % 50) return;
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_TILES; i++) await cache.delete(keys[i]);
}
async function tile(req) {
  const cache = await caches.open(TILES);
  const hit = await cache.match(req.url);
  if (hit) return hit;
  try {
    const res = await fetch(req.url, {mode: 'cors', credentials: 'omit'});
    if (res.ok) cache.put(req.url, res.clone()).then(() => trim(cache));
    return res;
  } catch (err) {
    try { return await fetch(req); } catch (e2) { return Response.error(); }
  }
}
