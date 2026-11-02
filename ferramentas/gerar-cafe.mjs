// Gera o Café Aurora (o site do simulador) em cada idioma da página principal: sitios/cafe-aurora/index.html (pt-BR)
// e sitios/cafe-aurora/<pasta>/index.html, nas mesmas pastas do Linu Sites (pt-pt, es, ca, nl, en, fr, de, it, intl, ja,
// ko, zh-hant). O simulador de cada idioma abre o Café no mesmo idioma. Mudou um texto ou o HTML do Café, mude em
// ferramentas/cafe/ e rode:
//   node ferramentas/gerar-cafe.mjs
// - cafe/modelo.html: o index.html do Café com {{chave}} no lugar de cada texto;
// - cafe/textos/<código>.json: "textos" vão no HTML (e os nomes das bebidas também no script); "js" só no script, pelo
//   <script type="application/json" id="textos-cafe">. Todo idioma tem as mesmas chaves do pt-BR.
// Os idiomas (código, pasta, lang e rascunho) são os de ferramentas/pagina/textos/. Desde 1/11/2026, as versões
// Bootstrap e Tailwind também saem em cada idioma, dos modelos cafe/modelo-bootstrap.html e cafe/modelo-tailwind.html,
// com os mesmos textos: /bootstrap/ e /tailwind/ em pt-BR, /<pasta>/bootstrap/ e /<pasta>/tailwind/ nos outros.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const cafe = path.join(aqui, '..', 'sitios', 'cafe-aurora');
const CAFE = 'https://cafe.linupedia.com.br/';
const SITES = 'https://sites.linupedia.com.br/';
// IDIOMAS=pt-BR,en-GB gera só esses (para testar um texto novo antes de traduzir os outros)
const TODOS = ['pt-BR', 'pt-PT', 'es-ES', 'ca', 'nl', 'en-GB', 'fr', 'de', 'it', 'en-INTL', 'ja', 'ko', 'zh-Hant'];
const ORDEM = process.env.IDIOMAS ? process.env.IDIOMAS.split(',') : TODOS;
// as alternativas de idioma (hreflang) sempre listam todos, mesmo gerando só alguns
const NO_SITE = TODOS.flatMap((c) => {
  const pagina = path.join(aqui, 'pagina', 'textos', c + '.json');
  if (!fs.existsSync(pagina)) return [];
  const p = JSON.parse(fs.readFileSync(pagina, 'utf8'));
  return p.rascunho ? [] : [{ pasta: p.pasta, lang: p.lang }];
});
// os textos do HTML que o script também usa
const DO_SCRIPT = ['expresso', 'coldbrew', 'matcha', 'estelar', 'nivel', 'editar', 'd_nome', 'lab_add'];

const ler = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const modelo = fs.readFileSync(path.join(aqui, 'cafe', 'modelo.html'), 'utf8');
const VERSOES = ['bootstrap', 'tailwind', 'bulma', 'pico'];
const modeloDe = Object.fromEntries(VERSOES.map((v) => [v, fs.readFileSync(path.join(aqui, 'cafe', `modelo-${v}.html`), 'utf8')]));
// no Bootstrap, o negrito e o itálico dos textos têm classe própria (o gradiente do tema)
const MARCAS = { bootstrap: [['<strong>', '<strong class="e-3791cd">'], ['<em>', '<em class="e-350796">']], tailwind: [], bulma: [], pico: [] };
// o seletor das cinco versões, no rodapé de cada uma: os endereços e qual é a atual
const troca = (atual, dentro) => Object.fromEntries([['puro', ''], ...VERSOES.map((v) => [v, v + '/'])].flatMap(([v, pasta]) => [
  ['v_' + v, (dentro ? '../' : './') + pasta], ['ac_' + v, v === atual ? ' aria-current="page"' : '']]));
const erros = [];
const idiomas = ORDEM.flatMap((c) => {
  const pagina = path.join(aqui, 'pagina', 'textos', c + '.json');
  const textos = path.join(aqui, 'cafe', 'textos', c + '.json');
  if (!fs.existsSync(pagina) || ler(pagina).rascunho) return [];
  if (!fs.existsSync(textos)) { erros.push(`${c}: falta ferramentas/cafe/textos/${c}.json`); return []; }
  const { pasta, lang } = ler(pagina);
  return [{ codigo: c, pasta, lang, ...ler(textos) }];
});

const chaves = (i) => [...Object.keys(i.textos).map((k) => 't:' + k), ...Object.keys(i.js).map((k) => 'j:' + k)];
const referencia = new Set(chaves(idiomas[0]));
for (const i of idiomas.slice(1)) {
  const deste = new Set(chaves(i));
  for (const k of referencia) if (!deste.has(k)) erros.push(`${i.codigo}: falta ${k}`);
  for (const k of deste) if (!referencia.has(k)) erros.push(`${i.codigo}: sobra ${k}`);
}

const enderecoDe = (i) => CAFE + (i.pasta ? i.pasta + '/' : '');
// um & solto vira &amp; (as entidades já escritas ficam); dentro de atributo, as aspas retas também
const eComercial = (s) => String(s).replace(/&(?![a-zA-Z]+;|#\d+;)/g, '&amp;');
const alternativas = NO_SITE.map((o) => `<link rel="alternate" hreflang="${o.lang}" href="${enderecoDe(o)}">`).join('\n');

const saidas = [];
const preencher = (molde, i, extras, marcas = []) => molde.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, onde, todo) => {
  if (k in extras) return extras[k];
  let v = i.textos[k];
  if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto`); return ''; }
  for (const [a, b] of marcas) v = v.replaceAll(a, b);
  const tag = todo.slice(todo.lastIndexOf('<', onde), onde);
  const texto = eComercial(v);
  return tag.split('"').length % 2 === 0 ? texto.replaceAll('"', '&quot;') : texto;
});
for (const i of idiomas) {
  const js = { ...i.js, ...Object.fromEntries(DO_SCRIPT.map((k) => [k, i.textos[k]])) };
  const extras = {
    lang: i.lang,
    raiz: i.pasta ? '../' : '',
    url: enderecoDe(i),
    alternativas,
    linu_sites: SITES + (i.pasta ? i.pasta + '/' : ''),
    textos_js: JSON.stringify(js).replaceAll('</', '<\\/'),
    preco_ini: (21.5).toLocaleString(i.lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
    stat2_num: new Intl.NumberFormat(i.lang, { style: 'percent', minimumFractionDigits: 1 }).format(0.984),
    up: i.pasta ? '../' : '',
    ...troca('puro', false),
  };
  const html = modelo.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, onde, todo) => {
    if (k in extras) return extras[k];
    const v = i.textos[k];
    if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto`); return ''; }
    const tag = todo.slice(todo.lastIndexOf('<', onde), onde);
    const texto = eComercial(v);
    return tag.split('"').length % 2 === 0 ? texto.replaceAll('"', '&quot;') : texto;
  });
  saidas.push([path.join(i.pasta, 'index.html'), html]);
  for (const v of VERSOES) {
    const end = (o) => CAFE + (o.pasta ? o.pasta + '/' : '') + v + '/';
    const extrasV = {
      ...extras,
      url: end(i),
      alternativas: NO_SITE.map((o) => `<link rel="alternate" hreflang="${o.lang}" href="${end(o)}">`).join('\n'),
      base: i.pasta ? `../../${v}/` : '',
      up: i.pasta ? '../../' : '../',
      ...troca(v, true),
    };
    saidas.push([path.join(i.pasta, v, 'index.html'), preencher(modeloDe[v], i, extrasV, MARCAS[v])]);
  }
}

if (erros.length) {
  console.error('Nada foi gravado:\n  ' + erros.join('\n  '));
  process.exit(1);
}
for (const [arquivo, html] of saidas) {
  const destino = path.join(cafe, arquivo);
  if (fs.existsSync(destino) && fs.readFileSync(destino, 'utf8') === html) continue;
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, html);
  console.log('gravado', path.relative(cafe, destino));
}

// O Café sem internet (1/11/2026): o sw.js guarda a página principal e o que ela usa; os outros idiomas e as versões
// Bootstrap e Tailwind entram na cache quando a pessoa os abre. A versão da cache muda quando muda qualquer arquivo.
import crypto from 'node:crypto';
const BASE_OFF = ['./', 'index.html', 'estilo.css?v=13', 'script.js?v=12', 'inicio.js?v=3', 'icone.png', 'img/icone-192.png', 'img/icone-512.png',
  'manifest.webmanifest', 'fontes/orbitron.woff2', 'fontes/rajdhani-400.woff2', 'fontes/rajdhani-500.woff2', 'fontes/rajdhani-600.woff2', 'fontes/rajdhani-700.woff2'];
const hash = crypto.createHash('sha256');
for (const a of BASE_OFF.filter((a) => !a.endsWith('/'))) hash.update(fs.readFileSync(path.join(cafe, a.split('?')[0])));
for (const [arquivo, html] of saidas) hash.update(arquivo + html);
const versao = 'cafe-' + hash.digest('hex').slice(0, 10);
const sw = `// O Café Aurora sem internet (1/11/2026). Gerado pelo ferramentas/gerar-cafe.mjs do linu-sites: não edite à mão.
// Páginas: primeiro a rede, e a cópia guardada se não houver sinal. Arquivos: a cópia guardada. Uma cache, com limite.
const VERSAO = '${versao}';
const BASE = ${JSON.stringify(BASE_OFF)};
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
`;
if (!fs.existsSync(path.join(cafe, 'sw.js')) || fs.readFileSync(path.join(cafe, 'sw.js'), 'utf8') !== sw) { fs.writeFileSync(path.join(cafe, 'sw.js'), sw); console.log('gravado sw.js', versao); }
