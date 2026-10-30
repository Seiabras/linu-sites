// Gera um site de estudo (o Cerrado, as Abelhas) em cada idioma da página principal: sitios/<site>/*.html em pt-BR e
// sitios/<site>/<pasta>/*.html nos outros (pt-pt, es, ca, nl, en, fr, de, it, intl, ja, ko, zh-hant), com os idiomas no
// rodapé. Mudou um texto, mude em ferramentas/estudo/<site>/textos/<código>.json e rode:
//   node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
// - estudo/<site>/modelo/*.html: as páginas com {{chave}} no lugar de cada texto (saem do ferramentas/estudo/extrair.py);
// - estudo/<site>/textos/<código>.json: "textos" vão no HTML; "js" vão para os scripts, no
//   <script type="application/json" id="textos-estudo">. Todo idioma tem as mesmas chaves do pt-BR.
// Os idiomas (código, pasta, lang, nome e rascunho) são os de ferramentas/pagina/textos/.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const site = process.argv[2];
if (!site) { console.error('Diga o site: node ferramentas/gerar-estudo.mjs fotografia-do-cerrado'); process.exit(1); }
const pasta = path.join(aqui, 'estudo', site);
const saida = path.join(aqui, '..', 'sitios', site);
const ENDERECOS = { 'fotografia-do-cerrado': 'https://cerrado.linupedia.com.br/', 'abelhas-sem-ferrao': 'https://abelhas.linupedia.com.br/' };
const ORDEM = ['pt-BR', 'pt-PT', 'es-ES', 'ca', 'nl', 'en-GB', 'fr', 'de', 'it', 'en-INTL', 'ja', 'ko', 'zh-Hant'];

const ler = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const erros = [];
const idiomas = ORDEM.flatMap((c) => {
  const pagina = path.join(aqui, 'pagina', 'textos', c + '.json');
  const textos = path.join(pasta, 'textos', c + '.json');
  if (!fs.existsSync(pagina) || ler(pagina).rascunho) return [];
  if (!fs.existsSync(textos)) { erros.push(`${c}: falta ferramentas/estudo/${site}/textos/${c}.json`); return []; }
  const p = ler(pagina);
  return [{ codigo: c, pasta: p.pasta, lang: p.lang, nome: p.nome, rotulo: p.textos.idioma_rotulo, ...ler(textos) }];
});
const chaves = (i) => [...Object.keys(i.textos).map((k) => 't:' + k), ...Object.keys(i.js).map((k) => 'j:' + k)];
const referencia = new Set(chaves(idiomas[0]));
for (const i of idiomas.slice(1)) {
  const deste = new Set(chaves(i));
  for (const k of referencia) if (!deste.has(k)) erros.push(`${i.codigo}: falta ${k}`);
  for (const k of deste) if (!referencia.has(k)) erros.push(`${i.codigo}: sobra ${k}`);
}

const eComercial = (s) => String(s).replace(/&(?![a-zA-Z]+;|#\d+;)/g, '&amp;');
const paginas = fs.readdirSync(path.join(pasta, 'modelo')).filter((f) => f.endsWith('.html'));
const saidas = [];
for (const arquivo of paginas) {
  const modelo = fs.readFileSync(path.join(pasta, 'modelo', arquivo), 'utf8');
  // a página no outro idioma: index.html vira a pasta, como no endereço de verdade
  const enderecoDe = (o) => ENDERECOS[site] + (o.pasta ? o.pasta + '/' : '') + (arquivo === 'index.html' ? '' : arquivo.replace(/\.html$/, ''));
  const alternativas = idiomas.map((o) => `    <link rel="alternate" hreflang="${o.lang}" href="${enderecoDe(o)}">`).join('\n');
  for (const i of idiomas) {
    const raiz = i.pasta ? '../' : '';
    const links = idiomas.map((o) => {
      const href = (o.pasta ? (i.pasta ? '../' : '') + o.pasta + '/' : raiz || './') + (arquivo === 'index.html' ? '' : arquivo);
      return `<a href="${href || './'}" hreflang="${o.lang}" lang="${o.lang}"${o === i ? ' aria-current="true"' : ''}>${eComercial(o.nome)}</a>`;
    }).join(' · ');
    const extras = {
      lang: i.lang,
      raiz,
      alternativas,
      textos_js: JSON.stringify(i.js).replaceAll('</', '<\\/'),
      idiomas: `<nav class="idiomas-rodape" aria-label="${eComercial(i.rotulo).replaceAll('"', '&quot;')}">${links}</nav>`,
    };
    const html = modelo.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, onde, todo) => {
      if (k in extras) return extras[k];
      const v = i.textos[k];
      if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto (${arquivo})`); return ''; }
      const tag = todo.slice(todo.lastIndexOf('<', onde), onde);
      const texto = eComercial(v);
      return tag.split('"').length % 2 === 0 ? texto.replaceAll('"', '&quot;') : texto;
    });
    saidas.push([path.join(saida, i.pasta, arquivo), html]);
  }
}

if (erros.length) {
  console.error('Nada foi gravado:\n  ' + [...new Set(erros)].join('\n  '));
  process.exit(1);
}
let gravados = 0;
for (const [destino, html] of saidas) {
  if (fs.existsSync(destino) && fs.readFileSync(destino, 'utf8') === html) continue;
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, html);
  gravados++;
}
console.log(`${site}: ${gravados} páginas gravadas (${paginas.length} páginas × ${idiomas.length} idiomas)`);
