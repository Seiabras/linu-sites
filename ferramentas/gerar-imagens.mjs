// Gera a imagem de compartilhamento (public/img/compartilhar.png, 1200 × 630, de compartilhar.html). Os ícones e
// a logo vêm do app, pelo ferramentas/linu-do-app.py (rode ele antes).
// Gera também as capas do portfólio (public/img/projetos/<nome>.webp, 960 × 600, de capas/<nome>.html), com a arte e as
// fontes dos repositórios vizinhos em ~/Documentos/projetos. O WebP sai pelo ImageMagick.
// Precisa do Playwright com o Chromium:  npx playwright@1.56.1 install chromium  e depois
//   node ferramentas/gerar-imagens.mjs         (tudo)
//   node ferramentas/gerar-imagens.mjs capas   (só as capas)
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import os from 'node:os';
import path from 'node:path';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const img = path.join(aqui, '..', 'public', 'img');
const navegador = await chromium.launch();

if (process.argv[2] !== 'capas') {
  const og = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
  await og.goto(pathToFileURL(path.join(aqui, 'compartilhar.html')).href, { waitUntil: 'networkidle' });
  await og.evaluate(() => document.fonts.ready);
  await og.screenshot({ path: path.join(img, 'compartilhar.png') });
}

// A LinuPedia e a Trupe têm desenho e letra, que o WebP sem perda guarda nítidos; o Minhocão é uma cena com granulado
const CAPAS = { linupedia: ['-define', 'webp:lossless=true'], trupe: ['-define', 'webp:lossless=true'], minhocao: ['-quality', '80'] };
for (const [nome, opcoes] of Object.entries(CAPAS)) {
  const pagina = await navegador.newPage({ viewport: { width: 960, height: 600 } });
  await pagina.goto(pathToFileURL(path.join(aqui, 'capas', nome + '.html')).href, { waitUntil: 'networkidle' });
  await pagina.evaluate(() => document.fonts.ready);
  const png = path.join(os.tmpdir(), `capa-${nome}.png`);
  await pagina.screenshot({ path: png });
  execFileSync('magick', [png, ...opcoes, '-define', 'webp:method=6', path.join(img, 'projetos', nome + '.webp')]);
}

await navegador.close();
console.log('imagens geradas em', img);
