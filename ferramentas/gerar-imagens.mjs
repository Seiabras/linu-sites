// Gera a imagem de compartilhamento (public/img/compartilhar.png, 1200 × 630, de compartilhar.html). Os ícones e
// a logo vêm do app, pelo ferramentas/linu-do-app.py (rode ele antes).
// Precisa do Playwright com o Chromium:  npx playwright@1.56.1 install chromium  e depois
//   node ferramentas/gerar-imagens.mjs
import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const img = path.join(aqui, '..', 'public', 'img');
const navegador = await chromium.launch();

const og = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
await og.goto(pathToFileURL(path.join(aqui, 'compartilhar.html')).href, { waitUntil: 'networkidle' });
await og.evaluate(() => document.fonts.ready);
await og.screenshot({ path: path.join(img, 'compartilhar.png') });

await navegador.close();
console.log('imagens geradas em', img);
