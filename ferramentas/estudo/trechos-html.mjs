// Os trechos que se traduzem numa página dos sites de estudo (04/11/2026). O mesmo percurso serve ao extrator
// (ferramentas/estudo/trechos.mjs), que junta o português, e ao ferramentas/gerar-estudo.mjs, que põe a tradução no
// lugar: assim os dois sempre veem os mesmos trechos.
//
// Um trecho é:
// - um bloco de texto inteiro, com a marcação de dentro da frase (<a>, <strong>, <sup>…), como no extrair.py: o elemento
//   que tem texto e só filhos de dentro da frase;
// - o texto solto que sobra fora dos blocos (ao lado de um <input>, de um <svg>…);
// - um atributo que a pessoa lê ou ouve (alt, title, aria-label, placeholder…), o content das metas de descrição e de
//   compartilhar e o texto da mensagem do WhatsApp;
// - uma cadeia de texto dos blocos <script type="application/json"> e do data-parques (não as que parecem id, nome de
//   arquivo, endereço ou número).
// O que tem {{chave}} já é traduzido pelos textos/<código>.json: um trecho só de chaves não conta.
//
// percorrer(html, trocar) chama trocar(texto, tipo) para cada trecho, na ordem da página, com o texto normalizado
// (espaços juntados). Se trocar devolver uma cadeia, ela entra no lugar do trecho; devolve o html com as trocas.

const DENTRO_DA_FRASE = new Set(['a', 'b', 'strong', 'em', 'i', 'mark', 'span', 'br', 'small', 'abbr', 'code', 'sup', 'sub', 'q', 'cite', 'time']);
// destes, os que podem ser um bloco sozinhos (um <a> numa lista de links, um <span> com o nome do bicho)
const BLOCO_SOZINHO = new Set(['a', 'span', 'q', 'strong', 'b', 'em']);
const VAZIOS = new Set(['br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'area', 'col', 'wbr', 'base', 'track', 'embed', 'param']);
const ATRIBUTOS = new Set(['alt', 'title', 'aria-label', 'placeholder', 'data-escuro', 'data-claro', 'data-texto', 'data-nome', 'data-busca', 'label']);
const METAS = new Set(['description', 'og:title', 'og:description', 'og:image:alt', 'og:site_name', 'twitter:title', 'twitter:description', 'twitter:image:alt']);
// nos blocos JSON, as chaves que guardam ids separados por espaço (parecem frase, mas o script compara)
const JSON_SEM_TEXTO = new Set(['id', 'lug']);
const LETRA = /[A-Za-zÀ-ÖØ-öø-ɏͰ-ϿЀ-ӿ぀-ヿ一-鿿가-힯]/;

export const normalizar = (s) => s.replace(/\s+/g, ' ').trim();
const semMarcas = (s) => s.replace(/\{\{[^}]*\}\}/g, '').replace(/<[^>]*>/g, '').replace(/&(?:[a-zA-Z]+|#\d+|#x[\da-fA-F]+);/g, '');
export const temTexto = (s) => LETRA.test(semMarcas(s));

// uma cadeia dos dados que é para gente ler: tem letra e não parece endereço, arquivo, id ou classe
export const pareceTexto = (s) => {
  if (!temTexto(s)) return false;
  if (/^(https?:|mailto:|tel:|data:|#|\.{0,2}\/|=)/.test(s)) return false;
  if (/^[^\s"<>]+\.(html?|webp|jpe?g|png|svg|gif|css|js|json|pdf|woff2?)([?#]\S*)?$/i.test(s)) return false;
  return !/^[\p{Ll}0-9_:\/.#=-]+$/u.test(s);
};

// as entidades de que um atributo precisa
const doAtributo = (s) => s.replace(/&(?![a-zA-Z]+;|#\d+;|#x[\da-fA-F]+;)/g, '&amp;').replaceAll('"', '&quot;');
const desfazerAtributo = (s) => s.replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');

// os textos de um valor JSON já lido, em ordem; devolve o valor com as trocas
function percorrerJson(valor, trocar, chave) {
  if (Array.isArray(valor)) return valor.map((v) => percorrerJson(v, trocar, chave));
  if (valor && typeof valor === 'object') {
    const novo = {};
    for (const [k, v] of Object.entries(valor)) novo[k] = percorrerJson(v, trocar, k);
    return novo;
  }
  if (typeof valor !== 'string' || JSON_SEM_TEXTO.has(chave) || !pareceTexto(valor)) return valor;
  // um pedaço de HTML guardado nos dados (os desenhos do “Adivinhe a paisagem”) é percorrido como página
  if (/^\s*</.test(valor)) return percorrer(valor, trocar);
  const t = trocar(normalizar(valor), 'json');
  return typeof t === 'string' ? t : valor;
}

// um bloco JSON inteiro; se nada mudar, devolve o texto como estava (o português fica igual byte a byte)
export function percorrerBlocoJson(texto, trocar) {
  let dados;
  try { dados = JSON.parse(texto); } catch { return texto; }
  let mudou = false;
  const novo = percorrerJson(dados, (t, tipo) => { const r = trocar(t, tipo); if (typeof r === 'string' && r !== t) mudou = true; return r; });
  return mudou ? JSON.stringify(novo) : texto;
}

// a mensagem do WhatsApp é o texto da ficha e o endereço no fim: só o texto é trecho
const WHATSAPP = 'https://wa.me/?text=';
const codificar = (s) => encodeURIComponent(s).replaceAll('%2F', '/').replace(/[!'()*]/g, (c) => '%' + c.charCodeAt(0).toString(16).toUpperCase());

const ETIQUETA = /<!--[\s\S]*?-->|<(script|style)\b[^>]*>[\s\S]*?<\/\1\s*>|<\/?([a-zA-Z][\w:-]*)((?:\s+[^\s=>\/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*\/?>/g;
const ATRIBUTO = /([^\s=>\/]+)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s>]+))?/g;

export function percorrer(html, trocar) {
  // 1. as etiquetas e os textos, em ordem
  const pecas = [];
  let fim = 0;
  for (const m of html.matchAll(ETIQUETA)) {
    if (m.index > fim) pecas.push({ tipo: 'texto', ini: fim, fim: m.index });
    const bruto = m[0];
    let tipo = 'abre';
    if (bruto.startsWith('<!--')) tipo = 'comentario';
    else if (m[1]) tipo = 'bruto';
    else if (bruto.startsWith('</')) tipo = 'fecha';
    pecas.push({ tipo, ini: m.index, fim: m.index + bruto.length, tag: (m[1] || m[2] || '').toLowerCase(), attrs: m[3] || '', fechada: /\/\s*>$/.test(bruto) });
    fim = m.index + bruto.length;
  }
  if (fim < html.length) pecas.push({ tipo: 'texto', ini: fim, fim: html.length });

  // 2. os blocos de texto (a mesma regra do extrair.py)
  const pilha = [];
  const blocos = [];
  for (const p of pecas) {
    if (p.tipo === 'texto') {
      if (temTexto(html.slice(p.ini, p.fim))) for (const e of pilha) e.texto = true;
    } else if (p.tipo === 'abre' || p.tipo === 'bruto') {
      if (pilha.length) pilha[pilha.length - 1].filhosBloco ||= !DENTRO_DA_FRASE.has(p.tag);
      if (p.tipo === 'abre' && !VAZIOS.has(p.tag) && !p.fechada) pilha.push({ tag: p.tag, dentro: p.fim, filhosBloco: false, texto: false });
    } else if (p.tipo === 'fecha' && !VAZIOS.has(p.tag)) {
      if (!pilha.some((e) => e.tag === p.tag)) continue;
      let e;
      while ((e = pilha.pop()).tag !== p.tag) { /* fecha o que ficou aberto */ }
      if (e.texto && !e.filhosBloco && (!DENTRO_DA_FRASE.has(e.tag) || BLOCO_SOZINHO.has(e.tag))) blocos.push([e.dentro, p.ini]);
      if (pilha.length && (e.filhosBloco || !DENTRO_DA_FRASE.has(e.tag))) pilha[pilha.length - 1].filhosBloco = true;
    }
  }
  // só os blocos de fora (um bloco dentro de outro já vai junto)
  blocos.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  const finais = [];
  for (const b of blocos) if (!finais.length || b[0] >= finais[finais.length - 1][1]) finais.push(b);
  const dentroDeBloco = (pos) => finais.some(([a, b]) => pos >= a && pos < b);

  // 3. os trechos, na ordem da página
  const trocas = [];
  const pedir = (ini, fim, texto, tipo, montar = (t) => t) => {
    const t = trocar(texto, tipo);
    if (typeof t === 'string') trocas.push([ini, fim, montar(t)]);
  };
  const naPosicao = new Map(pecas.map((p, i) => [p.ini, i]));
  // o fim da etiqueta que fecha a que abre na peça i (ou -1)
  const fechamento = (i) => {
    const tag = pecas[i].tag;
    let fundo = 0;
    for (let j = i; j < pecas.length; j++) {
      const p = pecas[j];
      if (p.tag !== tag) continue;
      if (p.tipo === 'abre' && !p.fechada) fundo++;
      else if (p.tipo === 'fecha' && --fundo === 0) return j;
    }
    return -1;
  };
  const bloco = (ini, fim) => {
    if (!temTexto(html.slice(ini, fim))) return;
    // sem os espaços das pontas e sem a etiqueta que embrulha tudo (o <a> de um item de menu): o trecho é “Início”,
    // não <a href="index.html">Início</a>
    for (;;) {
      const miolo = html.slice(ini, fim);
      ini += miolo.length - miolo.trimStart().length;
      fim -= miolo.length - miolo.trimEnd().length;
      const i = naPosicao.get(ini);
      if (i === undefined || pecas[i].tipo !== 'abre' || VAZIOS.has(pecas[i].tag) || pecas[i].fechada) break;
      const j = fechamento(i);
      if (j < 0 || pecas[j].fim !== fim) break;
      ini = pecas[i].fim; fim = pecas[j].ini;
    }
    pedir(ini, fim, normalizar(html.slice(ini, fim)), 'texto');
  };
  let proximoBloco = 0;
  for (const p of pecas) {
    while (proximoBloco < finais.length && finais[proximoBloco][0] <= p.ini) {
      bloco(...finais[proximoBloco]);
      proximoBloco++;
    }
    if (dentroDeBloco(p.ini)) continue;
    if (p.tipo === 'texto') bloco(p.ini, p.fim);
    else if (p.tipo === 'bruto' && p.tag === 'script' && /^<script[^>]*type="application\/json"/.test(html.slice(p.ini, p.fim))) {
      const abre = html.indexOf('>', p.ini) + 1;
      const fecha = html.lastIndexOf('</', p.fim);
      const dentro = html.slice(abre, fecha);
      const novo = percorrerBlocoJson(dentro, trocar);
      if (novo !== dentro) trocas.push([abre, fecha, novo.replace(/<\/(script)/gi, '<\\/$1')]);
    } else if (p.tipo === 'abre') {
      const inicioAttrs = html.indexOf(p.attrs, p.ini + 1 + p.tag.length);
      const lista = [...p.attrs.matchAll(ATRIBUTO)].map((a) => ({ nome: a[1].toLowerCase(), valor: a[2], pos: inicioAttrs + a.index + a[0].length - (a[2] || '').length }));
      const de = (nome) => lista.find((a) => a.nome === nome);
      for (const a of lista) {
        if (!a.valor || !/^["']/.test(a.valor)) continue;
        const ini = a.pos + 1;
        const fimValor = a.pos + a.valor.length - 1;
        const valor = a.valor.slice(1, -1);
        if (!temTexto(valor)) continue;
        const meta = p.tag === 'meta' && a.nome === 'content' && METAS.has((de('name') || de('property'))?.valor?.slice(1, -1));
        if (ATRIBUTOS.has(a.nome) || meta || (a.nome === 'value' && pareceTexto(desfazerAtributo(valor)))) {
          pedir(ini, fimValor, normalizar(valor), a.nome === 'content' ? 'meta' : a.nome, doAtributo);
        } else if (a.nome === 'href' && valor.startsWith(WHATSAPP)) {
          const msg = decodeURIComponent(valor.slice(WHATSAPP.length));
          const [, texto, endereco] = msg.match(/^([\s\S]*?)(\s+https?:\/\/\S+)?$/);
          pedir(ini, fimValor, normalizar(texto), 'whatsapp', (t) => WHATSAPP + codificar(t + (endereco || '')));
        } else if (a.nome.startsWith('data-') && /^\s*[[{]/.test(desfazerAtributo(valor))) {
          const novo = percorrerBlocoJson(desfazerAtributo(valor), trocar);
          if (novo !== desfazerAtributo(valor)) trocas.push([ini, fimValor, doAtributo(novo)]);
        }
      }
    }
  }
  while (proximoBloco < finais.length) bloco(...finais[proximoBloco++]);

  // 4. as trocas, de trás para a frente, para as posições valerem
  let saida = html;
  for (const [ini, fim, novo] of trocas.sort((a, b) => b[0] - a[0])) saida = saida.slice(0, ini) + novo + saida.slice(fim);
  return saida;
}

// ---- o que o extrator e o gerador dividem sobre um site

// os trechos {{?código}}…{{/código}} entram só naquele idioma e os {{!código}}…{{/!código}} em todos menos naquele
// (31/10/2026: a inicial e o menu em português já são o guia novo; nas outras línguas, o site continua como estava até
// a tradução). Uma língua pronta usa o sabor pt-BR.
export const soNeste = (modelo, codigo) => modelo
  .replace(/\{\{\?([A-Za-z-]+)\}\}([\s\S]*?)\{\{\/\1\}\}/g, (_, c, dentro) => (c === codigo ? dentro : ''))
  .replace(/\{\{!([A-Za-z-]+)\}\}([\s\S]*?)\{\{\/!\1\}\}/g, (_, c, dentro) => (c === codigo ? '' : dentro));

// a página que não usa {{lang}} (a 404 do Cerrado, que serve o domínio inteiro) fica só em português
export const traduzivel = (modelo) => modelo.includes('{{lang}}');

// as páginas na ordem do catálogo: a inicial primeiro, depois as outras em ordem alfabética
export const ordemDasPaginas = (paginas) => [...paginas].sort((a, b) => (a === 'index.html' ? -1 : b === 'index.html' ? 1 : a.localeCompare(b)));

// as frases dos scripts do guia novo (estudo/<site>/scripts-pt.json: { "guia": { "chave": "texto" } }); cada grupo
// vai no #textos-estudo das páginas que carregam o js/<grupo>.js, com o nome do grupo como chave
export const gruposDaPagina = (scripts, modelo) => Object.keys(scripts).filter((g) => modelo.includes(`js/${g}.js`));

// as cadeias de um grupo de frases, para o catálogo e para a tradução
export function traduzirFrases(valor, trocar) {
  // a frase vai como está (sem juntar espaços: um espaço no começo ou no fim faz parte dela)
  if (typeof valor === 'string') { if (!temTexto(valor)) return valor; const t = trocar(valor, 'script'); return typeof t === 'string' ? t : valor; }
  if (Array.isArray(valor)) return valor.map((v) => traduzirFrases(v, trocar));
  if (valor && typeof valor === 'object') return Object.fromEntries(Object.entries(valor).map(([k, v]) => [k, traduzirFrases(v, trocar)]));
  return valor;
}
