// Gera um site de estudo (o Cerrado, as Abelhas) em cada idioma da página principal: sitios/<site>/*.html em pt-BR e
// sitios/<site>/<pasta>/*.html nos outros (pt-pt, es, ca, nl, en, fr, de, it, intl, ja, ko, zh-hant), com os idiomas no
// rodapé. Mudou um texto, mude em ferramentas/estudo/<site>/textos/<código>.json e rode:
//   node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
// - estudo/<site>/modelo/*.html: as páginas com {{chave}} no lugar de cada texto (saem do ferramentas/estudo/extrair.py);
// - estudo/<site>/textos/<código>.json: "textos" vão no HTML; "js" vão para os scripts, no
//   <script type="application/json" id="textos-estudo">. Todo idioma tem as mesmas chaves do pt-BR.
// Os idiomas (código, pasta, lang, nome e rascunho) são os de ferramentas/pagina/textos/.
//
// Só em português por enquanto (31/10/2026): as páginas listadas em estudo/<site>/so-pt.json saem só em pt-BR (sem
// alternativas nem lista de idiomas), com o texto escrito direto no modelo; e, dentro de qualquer modelo, um trecho
// entre {{?pt-BR}} e {{/pt-BR}} entra só na página em pt-BR.
//
// A tradução do guia novo (04/11/2026): o texto em português escrito direto nos modelos se traduz pelo catálogo
// estudo/<site>/traducoes/<código>.json (o ferramentas/estudo/trechos.mjs junta os trechos). Uma língua com
// "pronto": true e nenhum trecho vazio passa a sair no sabor pt-BR (os {{?pt-BR}} entram, os {{!pt-BR}} saem), com as
// {{chave}} dos textos dela e cada trecho trocado pela tradução, e ganha também as páginas de so-pt.json; essas páginas
// passam a ter as alternativas e a lista de idiomas com o pt-BR e as línguas prontas. Língua não pronta: tudo como antes.
// As frases dos scripts do guia novo ficam em estudo/<site>/scripts-pt.json e vão no #textos-estudo das páginas no
// sabor pt-BR, traduzidas pelo mesmo catálogo.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { percorrer, soNeste, traduzivel, gruposDaPagina, traduzirFrases } from './estudo/trechos-html.mjs';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const site = process.argv[2];
if (!site) { console.error('Diga o site: node ferramentas/gerar-estudo.mjs fotografia-do-cerrado'); process.exit(1); }
const pasta = path.join(aqui, 'estudo', site);
const saida = path.join(aqui, '..', 'sitios', site);
const ENDERECOS = { 'fotografia-do-cerrado': 'https://cerrado.linupedia.com.br/', 'pica-nao-pica': 'https://picanaopica.linupedia.com.br/' };
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

// o catálogo de cada língua: pronta só com "pronto": true e todos os trechos preenchidos
for (const i of idiomas.slice(1)) {
  const arquivo = path.join(pasta, 'traducoes', i.codigo + '.json');
  const catalogo = fs.existsSync(arquivo) ? ler(arquivo) : { pronto: false, trechos: {} };
  i.pronto = catalogo.pronto === true;
  i.trechos = catalogo.trechos || {};
  if (!i.pronto) continue;
  const vazios = Object.entries(i.trechos).filter(([, v]) => typeof v !== 'string' || !v.trim()).map(([k]) => k);
  if (vazios.length) {
    const amostra = vazios.slice(0, 5).map((t) => `“${t.length > 70 ? t.slice(0, 70) + '…' : t}”`).join('; ');
    erros.push(`${i.codigo}: marcado pronto, mas faltam ${vazios.length} trechos em traducoes/${i.codigo}.json (${amostra}${vazios.length > 5 ? '; …' : ''})`);
  }
}
const scriptsPt = path.join(pasta, 'scripts-pt.json');
const scripts = fs.existsSync(scriptsPt) ? ler(scriptsPt) : {};
for (const g of Object.keys(scripts)) for (const i of idiomas) if (g in i.js) erros.push(`${i.codigo}: a chave js "${g}" é também um grupo do scripts-pt.json`);
const prontos = idiomas.filter((i) => i.codigo === 'pt-BR' || i.pronto);
// o que falta num catálogo pronto (o português mudou e o extrator não rodou) vira erro, com a lista
const faltando = new Map();
const traduzirCom = (i) => (texto) => {
  const t = i.trechos[texto];
  if (typeof t === 'string' && t.trim()) return t;
  if (texto in i.trechos) return undefined; // vazio: já está na lista de cima
  if (!faltando.has(i.codigo)) faltando.set(i.codigo, new Set());
  faltando.get(i.codigo).add(texto);
  return undefined;
};
// os endereços absolutos do próprio site (og:url, data-url, a mensagem do WhatsApp) vão para a pasta da língua
const enderecoNaPasta = (html, pastaLingua) => {
  const host = ENDERECOS[site].replace(/^https:\/\//, '').replace(/\/$/, '');
  return html.replace(new RegExp(`(//|%2F%2F)${host.replaceAll('.', '\\.')}/(?!(?:img|css|js|fontes)/)`, 'g'), `$1${host}/${pastaLingua}/`);
};
// o guia sem internet (manifesto e service worker) é só do português, como nas páginas compartilhadas
const semGuiaOffline = (html) => html
  .replace(/^[ \t]*<link rel="manifest"[^>]*><script src="[^"]*js\/offline\.js[^"]*"[^>]*><\/script>\n/gm, '')
  .replace(/<link rel="manifest"[^>]*>/g, '')
  .replace(/<script src="[^"]*js\/offline\.js[^"]*"[^>]*><\/script>/g, '');
// a página que não tem {{idiomas}} (as fichas do Pica) recebe a lista no começo do rodapé, na mesma linha: sem línguas
// prontas, ela fica vazia e a página sai igual
const comIdiomas = (html) => (html.includes('{{idiomas}}') ? html : html.replace(/(<footer class="rodape">\s*<div class="container">)/, '$1{{idiomas}}'));

const eComercial = (s) => String(s).replace(/&(?![a-zA-Z]+;|#\d+;)/g, '&amp;');
const paginas = fs.readdirSync(path.join(pasta, 'modelo')).filter((f) => f.endsWith('.html'));
const soPt = fs.existsSync(path.join(pasta, 'so-pt.json')) ? ler(path.join(pasta, 'so-pt.json')) : [];
for (const f of soPt) if (!paginas.includes(f)) erros.push(`so-pt.json: ${f} não existe em modelo/`);
const saidas = [];
const sobras = [];
for (const arquivo of paginas) {
  const modeloBruto = comIdiomas(fs.readFileSync(path.join(pasta, 'modelo', arquivo), 'utf8'));
  const daPagina = !soPt.includes(arquivo) ? idiomas : traduzivel(modeloBruto) ? prontos : idiomas.slice(0, 1);
  // a página só em português que sobrou na pasta de uma língua que deixou de estar pronta sai
  for (const o of idiomas) if (o.pasta && !daPagina.includes(o)) sobras.push(path.join(saida, o.pasta, arquivo));
  // a página no outro idioma: index.html vira a pasta, como no endereço de verdade
  const enderecoDe = (o) => ENDERECOS[site] + (o.pasta ? o.pasta + '/' : '') + (arquivo === 'index.html' ? '' : arquivo.replace(/\.html$/, ''));
  const alternativas = daPagina.map((o) => `    <link rel="alternate" hreflang="${o.lang}" href="${enderecoDe(o)}">`).join('\n');
  for (const i of daPagina) {
    // a língua pronta usa o sabor pt-BR, com cada trecho em português trocado pela tradução
    const sabor = i.pronto ? 'pt-BR' : i.codigo;
    let modelo = soNeste(modeloBruto, sabor);
    if (i.pronto) modelo = semGuiaOffline(enderecoNaPasta(percorrer(modelo, traduzirCom(i)), i.pasta));
    let js = i.js;
    if (sabor === 'pt-BR') {
      js = { ...i.js };
      for (const g of gruposDaPagina(scripts, modelo)) js[g] = i.pronto ? traduzirFrases(scripts[g], traduzirCom(i)) : scripts[g];
    }
    const raiz = i.pasta ? '../' : '';
    const links = daPagina.map((o) => {
      const href = (o.pasta ? (i.pasta ? '../' : '') + o.pasta + '/' : raiz || './') + (arquivo === 'index.html' ? '' : arquivo);
      return `<a href="${href || './'}" hreflang="${o.lang}" lang="${o.lang}"${o === i ? ' aria-current="true"' : ''}>${eComercial(o.nome)}</a>`;
    }).join(' · ');
    const extras = {
      lang: i.lang,
      raiz,
      alternativas,
      textos_js: JSON.stringify(js).replaceAll('</', '<\\/'),
      idiomas: daPagina.length < 2 ? '' : `<nav class="idiomas-rodape" aria-label="${eComercial(i.rotulo).replaceAll('"', '&quot;')}">${links}</nav>`,
    };
    const html = modelo.replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, onde, todo) => {
      if (k in extras) return extras[k];
      const v = i.textos[k];
      if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto (${arquivo})`); return ''; }
      const tag = todo.slice(todo.lastIndexOf('<', onde), onde);
      const texto = eComercial(v);
      return tag.split('"').length % 2 === 0 ? texto.replaceAll('"', '&quot;') : texto;
    });
    // a linha dos idiomas fica vazia nas páginas só em português: sem espaço sobrando no fim da linha
    saidas.push([path.join(saida, i.pasta, arquivo), html.replace(/^[ \t]+$/gm, '')]);
  }
}

for (const [codigo, lista] of faltando) {
  const amostra = [...lista].slice(0, 5).map((t) => `“${t.length > 70 ? t.slice(0, 70) + '…' : t}”`).join('; ');
  erros.push(`${codigo}: ${lista.size} trechos das páginas não estão no catálogo (rode node ferramentas/estudo/trechos.mjs ${site}): ${amostra}${lista.size > 5 ? '; …' : ''}`);
}
if (erros.length) {
  console.error('Nada foi gravado:\n  ' + [...new Set(erros)].join('\n  '));
  process.exit(1);
}
let apagados = 0;
for (const f of sobras) if (fs.existsSync(f)) { fs.unlinkSync(f); apagados++; }
let gravados = 0;
for (const [destino, html] of saidas) {
  if (fs.existsSync(destino) && fs.readFileSync(destino, 'utf8') === html) continue;
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, html);
  gravados++;
}
const outras = prontos.slice(1).map((i) => i.codigo);
console.log(`${site}: ${gravados} páginas gravadas (${paginas.length - soPt.length} páginas × ${idiomas.length} idiomas, mais ${soPt.length} só em português`
  + `${outras.length ? `, traduzidas também em ${outras.join(', ')}` : ''})${apagados ? `; ${apagados} páginas de línguas não prontas apagadas` : ''}`);
