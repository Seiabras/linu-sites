// Gera o Café Aurora (o site do simulador) em cada idioma da página principal: sitios/cafe-aurora/index.html (pt-BR)
// e sitios/cafe-aurora/<pasta>/index.html, nas mesmas pastas do Linu Sites (pt-pt, es, ca, nl, en, fr, de, it, intl, ja,
// ko, zh-hant). O simulador de cada idioma abre o Café no mesmo idioma. Mudou um texto ou o HTML do Café, mude em
// ferramentas/cafe/ e rode:
//   node ferramentas/gerar-cafe.mjs
// - cafe/modelo.html: o index.html do Café com {{chave}} no lugar de cada texto;
// - cafe/textos/<código>.json: "textos" vão no HTML (e os nomes das bebidas também no script); "js" só no script, pelo
//   <script type="application/json" id="textos-cafe">. Todo idioma tem as mesmas chaves do pt-BR.
// Os idiomas (código, pasta, lang e rascunho) são os de ferramentas/pagina/textos/. As versões /bootstrap/ e /tailwind/
// ficam só em português.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const cafe = path.join(aqui, '..', 'sitios', 'cafe-aurora');
const CAFE = 'https://cafe.linupedia.com.br/';
const SITES = 'https://sites.linupedia.com.br/';
// IDIOMAS=pt-BR,en-GB gera só esses (para testar um texto novo antes de traduzir os outros)
const ORDEM = process.env.IDIOMAS ? process.env.IDIOMAS.split(',') : ['pt-BR', 'pt-PT', 'es-ES', 'ca', 'nl', 'en-GB', 'fr', 'de', 'it', 'en-INTL', 'ja', 'ko', 'zh-Hant'];
// os textos do HTML que o script também usa
const DO_SCRIPT = ['expresso', 'coldbrew', 'matcha', 'estelar', 'nivel', 'editar'];

const ler = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const modelo = fs.readFileSync(path.join(aqui, 'cafe', 'modelo.html'), 'utf8');
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
const alternativas = idiomas.map((o) => `<link rel="alternate" hreflang="${o.lang}" href="${enderecoDe(o)}">`).join('\n');

const saidas = [];
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
  };
  const html = modelo.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, onde, todo) => {
    if (k in extras) return extras[k];
    const v = i.textos[k];
    if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto`); return ''; }
    const tag = todo.slice(todo.lastIndexOf('<', onde), onde);
    const texto = eComercial(v);
    return tag.split('"').length % 2 === 0 ? texto.replaceAll('"', '&quot;') : texto;
  });
  saidas.push([i, html]);
}

if (erros.length) {
  console.error('Nada foi gravado:\n  ' + erros.join('\n  '));
  process.exit(1);
}
for (const [i, html] of saidas) {
  const destino = path.join(cafe, i.pasta, 'index.html');
  if (fs.existsSync(destino) && fs.readFileSync(destino, 'utf8') === html) continue;
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, html);
  console.log('gravado', path.relative(cafe, destino));
}
