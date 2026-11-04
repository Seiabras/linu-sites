// Junta os trechos do guia novo que ainda saem só em português e põe em dia o catálogo de cada língua (04/11/2026):
//   node ferramentas/estudo/trechos.mjs pica-nao-pica
// Lê os modelos no sabor pt-BR (as páginas de so-pt.json e os trechos {{?pt-BR}} das compartilhadas) e as frases do
// scripts-pt.json, e grava:
// - estudo/<site>/traducoes/<código>.json, um por língua: { "pronto": false, "trechos": { "<português>": "<tradução>" } }.
//   O que é novo entra vazio, o que sumiu do português sai, o que já estava traduzido fica. A ordem é a das páginas
//   (a inicial primeiro, depois em ordem alfabética, e as frases dos scripts no fim).
// - estudo/<site>/traducoes/onde.json: onde cada trecho aparece (as páginas e, se não for texto da página, o tipo:
//   alt, meta, json…), na mesma ordem, para quem traduz. Não se edita à mão.
// Rodar de novo sem mudar o português não muda nada. Depois de traduzir uma língua inteira, ponha "pronto": true e rode
// o ferramentas/gerar-estudo.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { percorrer, soNeste, traduzivel, ordemDasPaginas, gruposDaPagina, traduzirFrases } from './trechos-html.mjs';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const site = process.argv[2];
if (!site) { console.error('Diga o site: node ferramentas/estudo/trechos.mjs pica-nao-pica'); process.exit(1); }
const pasta = path.join(aqui, site);
if (!fs.existsSync(path.join(pasta, 'modelo'))) { console.error(`Não achei ferramentas/estudo/${site}/modelo/`); process.exit(1); }
const ler = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const ORDEM = ['pt-PT', 'es-ES', 'ca', 'nl', 'en-GB', 'fr', 'de', 'it', 'en-INTL', 'ja', 'ko', 'zh-Hant'];
const linguas = ORDEM.filter((c) => {
  const p = path.join(aqui, '..', 'pagina', 'textos', c + '.json');
  return fs.existsSync(p) && !ler(p).rascunho;
});

// 1. os trechos em português, na ordem, com onde aparecem
const onde = new Map();
const anotar = (texto, pagina, tipo) => {
  if (!onde.has(texto)) onde.set(texto, { paginas: [], tipos: new Set() });
  const o = onde.get(texto);
  if (!o.paginas.includes(pagina)) o.paginas.push(pagina);
  if (tipo !== 'texto') o.tipos.add(tipo);
};
const scriptsPt = path.join(pasta, 'scripts-pt.json');
const scripts = fs.existsSync(scriptsPt) ? ler(scriptsPt) : {};
const paginas = ordemDasPaginas(fs.readdirSync(path.join(pasta, 'modelo')).filter((f) => f.endsWith('.html')));
for (const arquivo of paginas) {
  const modelo = fs.readFileSync(path.join(pasta, 'modelo', arquivo), 'utf8');
  if (!traduzivel(modelo)) continue;
  percorrer(soNeste(modelo, 'pt-BR'), (texto, tipo) => anotar(texto, arquivo, tipo));
}
for (const [grupo, frases] of Object.entries(scripts)) traduzirFrases(frases, (texto) => anotar(texto, `js/${grupo}.js`, 'texto'));

// 2. o mapa de onde cada trecho aparece
const resumo = ({ paginas: p, tipos }) => {
  const lista = p.length > 3 ? `${p.slice(0, 3).join(', ')} e mais ${p.length - 3}` : p.join(', ');
  return tipos.size ? `${lista} (${[...tipos].join(', ')})` : lista;
};
const gravar = (destino, dados) => {
  const texto = JSON.stringify(dados, null, 2) + '\n';
  if (fs.existsSync(destino) && fs.readFileSync(destino, 'utf8') === texto) return false;
  fs.mkdirSync(path.dirname(destino), { recursive: true });
  fs.writeFileSync(destino, texto);
  return true;
};
const pastaTraducoes = path.join(pasta, 'traducoes');
let mudados = 0;
mudados += gravar(path.join(pastaTraducoes, 'onde.json'), Object.fromEntries([...onde].map(([t, o]) => [t, resumo(o)])));

// 3. o catálogo de cada língua
const palavras = (t) => t.replace(/<[^>]*>/g, ' ').split(/\s+/).filter((p) => /\p{L}/u.test(p)).length;
const total = onde.size;
const totalPalavras = [...onde.keys()].reduce((s, t) => s + palavras(t), 0);
console.log(`${site}: ${total} trechos únicos, ${totalPalavras} palavras`);
for (const c of linguas) {
  const destino = path.join(pastaTraducoes, c + '.json');
  const antes = fs.existsSync(destino) ? ler(destino) : { pronto: false, trechos: {} };
  const trechos = {};
  for (const t of onde.keys()) trechos[t] = typeof antes.trechos?.[t] === 'string' ? antes.trechos[t] : '';
  const saiu = Object.keys(antes.trechos || {}).filter((t) => !onde.has(t)).length;
  const novos = [...onde.keys()].filter((t) => !(t in (antes.trechos || {}))).length;
  mudados += gravar(destino, { pronto: antes.pronto === true, trechos });
  const faltam = Object.entries(trechos).filter(([, v]) => !v.trim());
  const nota = [novos && `${novos} novos`, saiu && `${saiu} saíram`].filter(Boolean).join(', ');
  console.log(`  ${c.padEnd(8)} ${faltam.length ? `faltam ${faltam.length} (${faltam.reduce((s, [t]) => s + palavras(t), 0)} palavras)` : 'completo'}`
    + `${antes.pronto ? ', marcado pronto' : ''}${nota ? ` · ${nota}` : ''}`);
}
console.log(mudados ? `${mudados} arquivos gravados em ferramentas/estudo/${site}/traducoes/` : 'nada mudou');
