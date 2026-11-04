// O Café Aurora sem internet (1/11/2026). Gerado pelo ferramentas/gerar-cafe.mjs do linu-sites: não edite à mão.
// Páginas: primeiro a rede, e a cópia guardada se não houver sinal. Arquivos: a cópia guardada. Uma cache, com limite.
const VERSAO = 'cafe-96e7a07609';
const BASE = ["./","index.html","estilo.css?v=21","script.js?v=16","inicio.js?v=4","icone.png","img/icone-192.png","img/icone-512.png","manifest.webmanifest","fontes/orbitron.woff2","fontes/rajdhani-400.woff2","fontes/rajdhani-500.woff2","fontes/rajdhani-600.woff2","fontes/rajdhani-700.woff2"];
const LIMITE = 150;
self.addEventListener('install', (e) => { e.waitUntil(caches.open(VERSAO).then((c) => c.addAll(BASE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith('cafe-') && k !== VERSAO).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
async function aparar(cache) { const ks = await cache.keys(); for (let i = 0; i < ks.length - LIMITE; i++) await cache.delete(ks[i]); }
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const cache = await caches.open(VERSAO);
    if (req.mode === 'navigate') {
      try { const r = await fetch(req); if (r.ok) cache.put(req, r.clone()).then(() => aparar(cache)); return r; }
      catch { return (await cache.match(req, { ignoreSearch: true })) || (await cache.match('index.html')) || Response.error(); }
    }
    const guardado = await cache.match(req);
    if (guardado) return guardado;
    const r = await fetch(req);
    if (r.ok) cache.put(req, r.clone()).then(() => aparar(cache));
    return r;
  })());
});
