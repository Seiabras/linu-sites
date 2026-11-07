// Conferência visual de um site estático (07/11/2026): abre cada página em 390, 820 e 1280 px, no claro e no escuro,
// e reprova se houver rolagem lateral, erro no console, arquivo do próprio site faltando (404) ou falha séria ou
// crítica de acessibilidade (axe). Guarda a captura de página inteira de cada combinação.
//
//   node conferir-visual.mjs --raiz <pasta do site> [--paginas /,/identidade] [--saida capturas]
//                            [--playwright <pasta do pacote>] [--axe <axe.min.js>] [--larguras 390,820,1280]
//                            [--ignorar <expressão>]   (mensagem conhecida do console que não reprova, como o
//                            quadro do Café, que só aceita ser aberto pelo endereço real)
//
// No GitHub Actions: `npm i --no-save playwright@1.63.0 axe-core@4.10.3 && npx playwright install --with-deps chromium`
// e depois este script; as capturas sobem como artefato. No computador, passe --playwright e --axe se não estiverem
// instalados na pasta. O original mora em linuarquivos/modelos/ferramentas/; cada site tem uma cópia em ferramentas/.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith('--')) acc.push([a.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return acc;
}, []));
const raiz = path.resolve(args.raiz || '.');
const paginas = String(args.paginas || '/').split(',');
const larguras = String(args.larguras || '390,820,1280').split(',').map(Number);
const saida = path.resolve(args.saida || 'capturas');
const ignorar = args.ignorar ? new RegExp(args.ignorar) : null;
const exigir = createRequire(path.join(process.cwd(), 'x.js'));
const { chromium } = args.playwright ? createRequire(import.meta.url)(path.resolve(args.playwright)) : exigir('playwright');
const axe = fs.readFileSync(args.axe ? path.resolve(args.axe) : exigir.resolve('axe-core/axe.min.js'), 'utf8');

// servidor estático com a mesma regra do Caddy: {path}, {path}.html, {path}/index.html; senão 404.html
const tipos = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.woff2': 'font/woff2',
  '.txt': 'text/plain', '.xml': 'application/xml', '.ico': 'image/x-icon' };
const faltando = new Set();
const servidor = http.createServer((req, res) => {
  const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const alvo = [p, p + '.html', path.join(p, 'index.html')].map((c) => path.join(raiz, c))
    .find((c) => c.startsWith(raiz) && fs.existsSync(c) && fs.statSync(c).isFile());
  if (!alvo) {
    if (!/favicon/.test(p)) faltando.add(p);
    res.writeHead(404, { 'content-type': tipos['.html'] });
    const erro = path.join(raiz, '404.html');
    return res.end(fs.existsSync(erro) ? fs.readFileSync(erro) : 'não achei');
  }
  res.writeHead(200, { 'content-type': tipos[path.extname(alvo)] || 'application/octet-stream' });
  res.end(fs.readFileSync(alvo));
});
await new Promise((ok) => servidor.listen(0, '127.0.0.1', ok));
const base = `http://127.0.0.1:${servidor.address().port}`;

fs.mkdirSync(saida, { recursive: true });
const nav = await chromium.launch();
const falhas = [];
const avisos = [];
for (const pagina of paginas) {
  for (const tema of ['light', 'dark']) {
    for (const largura of larguras) {
      const nome = `${pagina.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'inicio'}-${largura}-${tema === 'light' ? 'claro' : 'escuro'}`;
      const pg = await nav.newPage({ viewport: { width: largura, height: 900 }, colorScheme: tema, reducedMotion: 'reduce', bypassCSP: true });  // só para injetar o axe; a CSP continua no site
      const erros = [];
      pg.on('pageerror', (e) => erros.push(e.message));
      pg.on('console', (m) => { if (m.type() === 'error' && !/404/.test(m.text())) erros.push(m.text()); });
      // 'load' e não 'networkidle': página com quadro de outro endereço (o Café no Linu Sites) nunca fica parada na rede
      await pg.goto(base + pagina, { waitUntil: 'load' });
      // rola até o fim para as imagens com lazy-load carregarem, e volta
      await pg.evaluate(async () => {
        for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); }
        scrollTo(0, 0);
      });
      await pg.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
      const lateral = await pg.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      if (lateral > 1) falhas.push(`${nome}: rolagem lateral de ${lateral} px`);
      for (const e of erros) if (!ignorar || !ignorar.test(e)) falhas.push(`${nome}: erro no console: ${e}`);
      if (largura === larguras[0] || largura === larguras[larguras.length - 1]) {
        await pg.addScriptTag({ content: axe });
        const r = await pg.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] })).violations
          .map((v) => ({ id: v.id, impacto: v.impact, n: v.nodes.length, onde: v.nodes.slice(0, 2).map((n) => n.target.join(' ')) })));
        for (const v of r) {
          const linha = `${nome}: ${v.id} (${v.impacto}, ${v.n}×) em ${v.onde.join(' | ')}`;
          (v.impacto === 'serious' || v.impacto === 'critical' ? falhas : avisos).push(linha);
        }
      }
      await pg.screenshot({ path: path.join(saida, nome + '.png'), fullPage: true });
      await pg.close();
    }
  }
}
await nav.close();
servidor.close();
for (const f of faltando) falhas.push(`arquivo pedido e não encontrado: ${f}`);

if (avisos.length) console.log(`Avisos (não reprovam):\n  ${[...new Set(avisos)].join('\n  ')}`);
if (falhas.length) {
  console.log(`Reprovado:\n  ${[...new Set(falhas)].join('\n  ')}`);
  process.exit(1);
}
console.log(`Tudo certo: ${paginas.length} página(s) × ${larguras.length} larguras × claro e escuro. Capturas em ${saida}.`);
