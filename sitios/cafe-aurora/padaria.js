// A Padaria Aurora nas versões Bootstrap e Tailwind (1/11/2026): das 6h às 18h (ou pelo botão de sol e lua) o Café vira
// a padaria, como na versão principal. Os textos dos dois modos já estão na página (.so-noite e .so-dia) e o
// padaria.css esconde os do outro; aqui ficam o botão, o pão do "Monte o seu pão" e a farinha no ar.
(() => {
  'use strict';
  const raiz = document.documentElement;
  const $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
  const bloco = $('#textos-cafe');
  const T = Object.assign({ d_pao: ['Pão de Trigo Solar', 'Pão de Centeio da Penumbra', 'Pão Integral de Órbita', 'Brioche Estelar'], d_min: '{n} min' },
    bloco ? JSON.parse(bloco.textContent) : {});
  const reduzido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let modo = raiz.dataset.modo === 'dia' ? 'dia' : 'noite';

  // ---- o pão: as quatro bases são farinhas; a casca doura com o tempo de forno (o mesmo da versão principal)
  const PAES = {
    expresso: { i: 0, h: 34, s: 68, claro: 74, escuro: 30, preco: 3 }, coldbrew: { i: 1, h: 22, s: 42, claro: 56, escuro: 18, preco: 4 },
    matcha: { i: 2, h: 28, s: 52, claro: 62, escuro: 22, preco: 4 }, estelar: { i: 3, h: 40, s: 88, claro: 72, escuro: 34, preco: 5 }
  };
  const form = $('#labForm'), intEl = $('#intensity'), nomeOut = $('#drinkName'), precoOut = $('#drinkPrice'), pao = $('#pao'), forno = $('#forno');
  const preco = (v) => '₡ ' + v.toLocaleString(raiz.lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function atualizarPao() {
    if (modo !== 'dia' || !form || !pao) return;
    const base = form.querySelector('input[name="base"]:checked').value, p = PAES[base], n = Number(intEl.value);
    const marcadas = [...form.querySelectorAll('input[name="top[]"]:checked')];
    const l = p.claro - (n - 1) * (p.claro - p.escuro) / 9;
    pao.style.setProperty('--casca', `hsl(${p.h} ${p.s}% ${l}%)`);
    pao.style.setProperty('--miolo', `hsl(${p.h} ${p.s}% ${Math.min(88, l + 22)}%)`);
    pao.style.height = (104 + n * 3) + 'px';
    pao.classList.toggle('estelar', base === 'estelar');
    for (let k = 1; k <= 4; k++) pao.classList.toggle('com-' + k, marcadas.some((i) => i.dataset.cob === String(k)));
    forno.style.background = `radial-gradient(circle, hsla(${28 + n}, 95%, 58%, ${0.18 + n * 0.03}), transparent 65%)`;
    let nome = `${T.d_pao[p.i]} · ${T.d_min.replace('{n}', 12 + n * 3)}`;
    const nomes = marcadas.map((i) => i.nextElementSibling.querySelector('.so-dia').textContent);
    if (nomes.length) nome += ` + ${nomes.join(' + ')}`;
    nomeOut.textContent = nome;
    precoOut.textContent = preco(p.preco + n * 0.2 + marcadas.length * 1.5);
  }
  // os modificadores aparecem na xícara (com-1 a com-4), de noite, como na versão principal
  const xicara = document.querySelector('.cup-wrap');
  const modificadores = () => {
    if (!form || !xicara) return;
    const marcadas = [...form.querySelectorAll('input[name="top[]"]:checked')];
    for (let k = 1; k <= 4; k++) xicara.classList.toggle('com-' + k, marcadas.some((i) => i.dataset.cob === String(k)));
  };
  if (form) { form.addEventListener('input', modificadores); form.addEventListener('change', modificadores); modificadores(); }
  // o script da versão escreve a bebida primeiro; de dia, o pão escreve por cima
  if (form) { form.addEventListener('input', atualizarPao); form.addEventListener('change', atualizarPao); }

  // ---- a farinha no ar: só de dia, só com movimento, só com a aba à vista
  const tela = document.createElement('canvas');
  tela.className = 'farinha'; tela.setAttribute('aria-hidden', 'true');
  document.body.prepend(tela);
  const ctx = tela.getContext('2d');
  const graos = [];
  let quadro = 0, impar = false, t = 0;
  const grao = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 16;
    const g = c.getContext('2d'), r = g.createRadialGradient(8, 8, 0, 8, 8, 8);
    r.addColorStop(0, 'hsla(34, 45%, 52%, .9)'); r.addColorStop(0.45, 'hsla(34, 45%, 52%, .5)'); r.addColorStop(1, 'hsla(34, 45%, 52%, 0)');
    g.fillStyle = r; g.fillRect(0, 0, 16, 16); return c;
  })();
  function medir() {
    tela.width = innerWidth; tela.height = innerHeight;
    graos.length = 0;
    for (let i = 0; i < (innerWidth < 700 ? 34 : 70); i++) graos.push({ x: Math.random() * tela.width, y: Math.random() * tela.height, r: Math.random() * 1.6 + 0.4, vy: -(Math.random() * 0.22 + 0.06), vx: (Math.random() - 0.5) * 0.14, a: Math.random() * 0.5 + 0.14 });
  }
  function passo() {
    quadro = requestAnimationFrame(passo);
    impar = !impar; if (impar) return; // 30 quadros por segundo
    t += 0.012;
    ctx.clearRect(0, 0, tela.width, tela.height);
    for (const g of graos) {
      g.x += g.vx * 1.5 + Math.sin(t * 2 + g.a * 20) * 0.15; g.y -= g.vy * 1.2;
      if (g.y > tela.height + 20) { g.y = -20; g.x = Math.random() * tela.width; }
      if (g.x < -20) g.x = tela.width + 20; if (g.x > tela.width + 20) g.x = -20;
      ctx.globalAlpha = g.a * 0.8; ctx.drawImage(grao, g.x - g.r * 2.5, g.y - g.r * 2.5, g.r * 5, g.r * 5);
    }
    ctx.globalAlpha = 1;
  }
  function farinha() {
    cancelAnimationFrame(quadro);
    if (modo === 'dia' && !reduzido && !document.hidden) { if (!graos.length) medir(); passo(); } else ctx.clearRect(0, 0, tela.width, tela.height);
  }
  addEventListener('resize', () => { if (graos.length) medir(); }, { passive: true });
  document.addEventListener('visibilitychange', farinha);

  // ---- o botão de sol e lua
  const botao = $('#modo'), corTema = $('meta[name="theme-color"]');
  function aplicar(novo) {
    modo = novo; raiz.dataset.modo = novo;
    if (botao) {
      const rotulo = novo === 'dia' ? botao.dataset.paraNoite : botao.dataset.paraDia;
      botao.setAttribute('aria-label', rotulo); botao.title = rotulo;
    }
    $$('[data-aria-dia]').forEach((el) => {
      if (!el.dataset.ariaNoite) el.dataset.ariaNoite = el.getAttribute('aria-label');
      el.setAttribute('aria-label', novo === 'dia' ? el.dataset.ariaDia : el.dataset.ariaNoite);
    });
    if (corTema) corTema.content = novo === 'dia' ? '#fbf3e4' : '#05030a';
    // o Pico tem tema claro e escuro próprios (data-theme): a padaria usa o claro, o café o escuro
    if (raiz.dataset.theme) raiz.dataset.theme = novo === 'dia' ? 'light' : 'dark';
    if (form) form.dispatchEvent(new Event('change')); // de noite, o script da versão volta a escrever a bebida
    farinha();
  }
  let virando = false;
  if (botao) botao.addEventListener('click', () => {
    if (virando) return;
    const novo = modo === 'dia' ? 'noite' : 'dia';
    try { localStorage.setItem('aurora-modo', novo); } catch (e) { /* sem guardar */ }
    if (reduzido) { aplicar(novo); return; }
    virando = true;
    raiz.classList.add('piscando');
    const virada = document.createElement('div');
    virada.className = 'virada virada--' + novo; virada.setAttribute('aria-hidden', 'true');
    const astro = document.createElement('i'); astro.className = 'virada__astro'; virada.append(astro);
    setTimeout(() => document.body.append(virada), 260);
    setTimeout(() => { raiz.classList.remove('piscando'); aplicar(novo); }, 260 + 650);
    setTimeout(() => { virada.remove(); virando = false; }, 260 + 1300);
  });
  aplicar(modo);
})();
