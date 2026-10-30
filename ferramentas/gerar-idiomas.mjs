// Gera a página inicial em cada idioma a partir de um modelo só: public/index.html (pt-BR) e public/<pasta>/index.html.
// Os idiomas vão em três regiões, cada uma com a sua moeda, pagamento e contato: Brasil (pt-BR, real), Europa (pt-pt,
// es, ca, nl, en, fr, de, it, euro) e Ásia-Pacífico e internacional (intl, ja, ko, zh-hant, dólar). Mudou um texto, um
// preço ou o HTML, mude em ferramentas/pagina/ e rode:
//   node ferramentas/gerar-idiomas.mjs
// - modelo.html: o HTML, com {{chave}} no lugar de cada texto, {{p.x}} para o preço formatado e {{n.x}} para o número.
// - textos/<código>.json: a região ("regiao"; "padrao": true na página que a representa), outros hreflang que a página
//   atende ("hreflang_extra") e os textos de cada idioma ("textos" vão no HTML; "js" vão para os scripts, no
//   <script type="application/json" id="textos-js">, e também podem aparecer no HTML). Todo idioma tem todas as chaves.
// - precos.json: os preços de cada moeda. Uma moeda com "pendente" ainda gera as páginas, mas não publica; com
//   "provisorio", publica e só avisa.
// Também gera as páginas “Como foi feito” de cada projeto em cada idioma (ferramentas/projetos/) e refaz o sitemap.xml,
// com as alternativas de idioma de todas as páginas.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const pagina = path.join(aqui, 'pagina');
const publico = path.join(aqui, '..', 'public');
const SITE = 'https://sites.linupedia.com.br/';
// A ordem é a do seletor (agrupado por região, nesta ordem); o pt-BR fica na raiz
const ORDEM = process.env.IDIOMAS ? process.env.IDIOMAS.split(',')
  : ['pt-BR', 'pt-PT', 'es-ES', 'ca', 'nl', 'en-GB', 'fr', 'de', 'it', 'en-INTL', 'ja', 'ko', 'zh-Hant'];
const REGIOES = ['brasil', 'europa', 'asia'];
// Um idioma com "rascunho": true (ou ainda sem arquivo) fica fora do site, do seletor e do sitemap
const arquivoDe = (c) => path.join(aqui, 'pagina', 'textos', c + '.json');
const ATIVOS = ORDEM.filter((c) => {
  if (!fs.existsSync(arquivoDe(c))) { console.warn(`fora: ${c} (ainda sem textos)`); return false; }
  if (JSON.parse(fs.readFileSync(arquivoDe(c), 'utf8')).rascunho) { console.warn(`fora: ${c} (rascunho)`); return false; }
  return true;
});
// Quem não bate com nenhum idioma cai no inglês internacional, em dólar (ou, sem ele, no europeu)
const PADRAO = ['en-INTL', 'en-GB'].find((c) => ATIVOS.includes(c)) || ATIVOS[0];

const modelo = fs.readFileSync(path.join(pagina, 'modelo.html'), 'utf8');
const precos = JSON.parse(fs.readFileSync(path.join(pagina, 'precos.json'), 'utf8'));
const idiomas = ATIVOS.map((c) => JSON.parse(fs.readFileSync(arquivoDe(c), 'utf8')));
const erros = [];

const enderecoDe = (i) => SITE + (i.pasta ? i.pasta + '/' : '');
// um & solto num texto ("English (UK & Europe)") sai como &amp;; as entidades que já vêm escritas ficam como estão
const eComercial = (s) => String(s).replace(/&(?![a-zA-Z]+;|#\d+;)/g, '&amp;');
const aspas = (s) => eComercial(s).replaceAll('"', '&quot;');
const hreflangs = (o) => [o.lang, ...(o.hreflang_extra || [])];
for (const i of idiomas) if (!REGIOES.includes(i.regiao)) erros.push(`${i.codigo}: região "${i.regiao}" não existe`);
for (const r of REGIOES) {
  const padroes = idiomas.filter((i) => i.regiao === r && i.padrao).length;
  if (idiomas.some((i) => i.regiao === r) && padroes !== 1) erros.push(`a região ${r} precisa de uma página "padrao" (tem ${padroes})`);
}

// As chaves do pt-BR são a referência: todo idioma tem as mesmas, nem mais nem menos
const chaves = (i) => [...Object.keys(i.textos).map((k) => 't:' + k), ...Object.keys(i.js).map((k) => 'j:' + k)];
const referencia = new Set(chaves(idiomas[0]));
for (const i of idiomas.slice(1)) {
  const deste = new Set(chaves(i));
  for (const k of referencia) if (!deste.has(k)) erros.push(`${i.codigo}: falta ${k}`);
  for (const k of deste) if (!referencia.has(k)) erros.push(`${i.codigo}: sobra ${k}`);
}

// As páginas “Como foi feito” de cada projeto, no mesmo idioma (public/<pasta>/projetos/<id>.html): o HTML em
// ferramentas/projetos/modelo.html, os dados fixos em projetos.json e os textos em projetos/textos/<código>.json
const modeloProjeto = fs.readFileSync(path.join(aqui, 'projetos', 'modelo.html'), 'utf8');
const { ordem: PROJETOS, fixos } = JSON.parse(fs.readFileSync(path.join(aqui, 'projetos', 'projetos.json'), 'utf8'));
const textosProjetos = Object.fromEntries(idiomas.map((i) => {
  const arquivo = path.join(aqui, 'projetos', 'textos', i.codigo + '.json');
  if (!fs.existsSync(arquivo)) { erros.push(`${i.codigo}: falta ferramentas/projetos/textos/${i.codigo}.json`); return [i.codigo, {}]; }
  const t = JSON.parse(fs.readFileSync(arquivo, 'utf8'));
  for (const id of PROJETOS) if (!t[id]) erros.push(`${i.codigo}: falta o projeto ${id}`);
  return [i.codigo, t];
}));
const lista = (itens) => itens.map((t) => `          <li>${eComercial(t)}</li>`).join('\n');

// O seletor e as alternativas valem para qualquer página: o sufixo é o caminho dentro do idioma ('' na inicial)
const seletorPara = (i, raiz, sufixo) => [
  '        <details class="idiomas">',
  `          <summary title="${aspas(i.textos.idioma_rotulo)}"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3Z" /></svg><span class="idiomas-codigo">${i.curto}</span><span class="so-leitor">: ${aspas(i.textos.idioma_rotulo)}, ${aspas(i.nome)}</span></summary>`,
  '          <div class="idiomas-lista">',
  ...REGIOES.filter((r) => idiomas.some((o) => o.regiao === r)).flatMap((r) => [
    `            <p class="idiomas-regiao" id="regiao-${r}">${eComercial(i.textos['regiao_' + r])}</p>`,
    `            <ul aria-labelledby="regiao-${r}">`,
    ...idiomas.filter((o) => o.regiao === r).map((o) => `              <li><a href="${(raiz + (o.pasta ? o.pasta + '/' : '') + sufixo) || './'}" hreflang="${o.lang}" lang="${o.lang}" data-regiao="${o.regiao}"${o.padrao ? ' data-padrao' : ''} data-sugestao="${aspas(o.sugestao)}" data-fechar="${aspas(o.js.fechar)}"${o === i ? ' aria-current="true"' : ''}>${eComercial(o.nome)}</a></li>`),
    '            </ul>',
  ]),
  '          </div>',
  '        </details>',
].join('\n');
const urlDe = (o, sufixo) => enderecoDe(o) + sufixo;
const padrao = idiomas.find((o) => o.codigo === PADRAO);
const alternativasPara = (sufixo) => [
  ...idiomas.flatMap((o) => hreflangs(o).map((h) => `  <link rel="alternate" hreflang="${h}" href="${urlDe(o, sufixo)}">`)),
  `  <link rel="alternate" hreflang="x-default" href="${urlDe(padrao, sufixo)}">`,
].join('\n');

const avisos = new Set();
const saidas = [];  // [arquivo dentro de public/, html, sufixo do endereço, idioma]
for (const i of idiomas) {
  const tabela = precos[i.moeda];
  if (!tabela) { erros.push(`${i.codigo}: moeda ${i.moeda} sem preços`); continue; }
  if (tabela.pendente) avisos.add(`PENDENTE ${i.moeda}: ${tabela.pendente}`);
  if (tabela.provisorio) avisos.add(`PROVISÓRIO ${i.moeda}: ${tabela.provisorio}`);
  const formato = new Intl.NumberFormat(i.lang, { style: 'currency', currency: i.moeda, maximumFractionDigits: 0 });
  const n = { ...tabela, zero: 0 };
  // o simulador abre com tudo ligado, menos o painel
  n.simulador_inicial = n.apresentacao + n.depoimentos + n.efeitos + n.cores + n.laboratorio + n.assinatura;
  const raiz = i.pasta ? '../' : '';

  // {{p.x}} e {{n.x}} também aparecem dentro dos textos (um preço citado numa dúvida, numa mensagem)
  const precosNo = (s, onde) => s.replace(/\{\{([pn])\.([a-z0-9_]+)\}\}/g, (_, tipo, k) => {
    const v = n[k];
    if (typeof v !== 'number') { erros.push(`${i.codigo}: preço ${tipo}.${k} não existe (${onde})`); return ''; }
    return tipo === 'p' ? formato.format(v) : String(v);
  });
  const js = Object.fromEntries(Object.entries(i.js).map(([k, v]) => [k, precosNo(v, 'js.' + k)]));

  // no HTML, os textos entram como estão (alguns têm <b>), só com as aspas retas escapadas para caber em atributo
  const preencher = (modelo, extras, onde) => precosNo(modelo, onde).replace(/\{\{([a-z0-9_]+)\}\}/g, (_, k, pos, todo) => {
    if (k in extras) return extras[k];
    const v = k in i.textos ? i.textos[k] : js[k];
    if (v === undefined) { erros.push(`${i.codigo}: {{${k}}} sem texto (${onde})`); return ''; }
    // dentro de um atributo (número ímpar de aspas desde o último <), o texto entra com as aspas escapadas
    const tag = todo.slice(todo.lastIndexOf('<', pos), pos);
    const texto = eComercial(precosNo(v, k));
    return (tag.split('"').length % 2 === 0) ? texto.replaceAll('"', '&quot;') : texto;
  });
  const comuns = {
    lang: i.lang,
    moeda: i.moeda,
    og_locale: i.og_locale,
    textos_js: JSON.stringify(js).replaceAll('</', '<\\/'),
    email_assunto: encodeURIComponent(js.assunto),
  };

  const extras = {
    ...comuns,
    raiz,
    url: enderecoDe(i),
    alternativas: alternativasPara(''),
    og_alternativas: idiomas.filter((o) => o !== i).map((o) => `  <meta property="og:locale:alternate" content="${o.og_locale}">`).join('\n'),
    seletor: seletorPara(i, raiz, ''),
    // o Café Aurora do simulador no mesmo idioma (ferramentas/gerar-cafe.mjs)
    cafe_url: 'https://cafe.linupedia.com.br/' + (i.pasta ? i.pasta + '/' : ''),
    // os outros dois sites de estudo também (ferramentas/gerar-estudo.mjs)
    cerrado_url: 'https://cerrado.linupedia.com.br/' + (i.pasta ? i.pasta + '/' : ''),
    abelhas_url: 'https://abelhas.linupedia.com.br/' + (i.pasta ? i.pasta + '/' : ''),
    dados_estruturados: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'ProfessionalService',
      name: 'Linu Sites',
      url: enderecoDe(i),
      logo: SITE + 'img/linu-logo.png',
      image: SITE + 'img/compartilhar.png',
      description: i.textos.descricao,
      inLanguage: i.lang,
      email: 'contato@linupedia.com.br',
      telephone: '+55 61 99667-2610',
      areaServed: i.area_servida,
      availableLanguage: idiomas.map((o) => o.lang),
      parentOrganization: { '@type': 'Organization', name: 'LinuPedia', url: 'https://linupedia.com.br' },
    }).replaceAll('</', '<\\/'),
    whats_inicial: encodeURIComponent(js.ola_conversa),
  };
  saidas.push([path.join(i.pasta, 'index.html'), preencher(modelo, extras, 'modelo'), '', i]);

  // as páginas dos projetos, um nível abaixo (projetos/), com o seletor levando ao mesmo projeto em cada idioma
  const raizProjeto = raiz + '../';
  for (const id of PROJETOS) {
    const p = { ...fixos[id], ...(textosProjetos[i.codigo][id] || {}) };
    if (!p.feito) continue;
    const sufixo = 'projetos/' + id;
    const doProjeto = {
      ...comuns,
      raiz: raizProjeto,
      url: urlDe(i, sufixo),
      alternativas: alternativasPara(sufixo),
      seletor: seletorPara(i, raizProjeto, sufixo),
      x_nome: eComercial(p.nome),
      x_url: p.url,
      x_imagem: p.imagem,
      x_etiqueta: eComercial(p.etiqueta),
      x_resumo: aspas(p.resumo),
      x_desafio: eComercial(p.desafio),
      x_alt: aspas(p.alt),
      x_feito: lista(p.feito),
      x_dentro: lista(p.dentro),
      x_abrir: eComercial(i.textos.proj_abrir.replace('{endereco}', p.endereco)),
      proj_og_titulo: aspas(i.textos.proj_og_titulo.replace('{nome}', p.nome)),
      x_whatsapp: encodeURIComponent(i.textos.proj_whats.replace('{nome}', p.nome)),
    };
    saidas.push([path.join(i.pasta, 'projetos', id + '.html'), preencher(modeloProjeto, doProjeto, 'projeto ' + id), sufixo, i]);
  }
}

if (erros.length) {
  console.error('Nada foi gravado:\n  ' + [...new Set(erros)].join('\n  '));
  process.exit(1);
}

// Grava só o que mudou e guarda a data de cada página para o sitemap (a de antes, se a página não mudou)
const arquivoSitemap = path.join(publico, 'sitemap.xml');
const sitemapAntes = fs.readFileSync(arquivoSitemap, 'utf8');
const hoje = new Date().toISOString().slice(0, 10);
const datas = {};
let gravados = 0;
for (const [arquivo, html, sufixo, i] of saidas) {
  const destino = path.join(publico, arquivo);
  const url = urlDe(i, sufixo);
  const antes = fs.existsSync(destino) ? fs.readFileSync(destino, 'utf8') : null;
  const anterior = sitemapAntes.match(new RegExp(`<loc>${url.replaceAll('.', '\\.')}</loc>\\s*(?:<xhtml:link[^>]*>\\s*)*<lastmod>([\\d-]+)</lastmod>`));
  if (antes === html && anterior) { datas[url] = anterior[1]; continue; }
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, html);
  datas[url] = hoje;
  gravados++;
}
console.log(`${gravados} páginas gravadas (${saidas.length} no total: a inicial e ${PROJETOS.length} projetos em ${idiomas.length} idiomas)`);

// O sitemap: cada página em cada idioma, com todas as alternativas
const sufixos = ['', ...PROJETOS.map((id) => 'projetos/' + id)];
const linksDe = (sufixo) => idiomas.flatMap((o) => hreflangs(o).map((h) => `    <xhtml:link rel="alternate" hreflang="${h}" href="${urlDe(o, sufixo)}"/>`)).join('\n')
  + `\n    <xhtml:link rel="alternate" hreflang="x-default" href="${urlDe(padrao, sufixo)}"/>`;
const sitemap = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
  ...sufixos.flatMap((sufixo) => idiomas.map((i) => `  <url>\n    <loc>${urlDe(i, sufixo)}</loc>\n${linksDe(sufixo)}\n    <lastmod>${datas[urlDe(i, sufixo)]}</lastmod>\n  </url>`)),
  '</urlset>',
  '',
].join('\n');
if (sitemap !== sitemapAntes) { fs.writeFileSync(arquivoSitemap, sitemap); console.log('gravado sitemap.xml'); }

for (const a of avisos) console.warn(a);
