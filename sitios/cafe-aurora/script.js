/* ============================================================
   CAFÉ AURORA — JS
   O que mudei para o Linu Sites:
   os três laços de animação (cursor, fundo e halo) rodam num quadro só, que para
   quando os efeitos estão desligados ou o site está fora da tela; e o item 13,
   que recebe do simulador quais módulos estão ligados. E o modo dia: das 6h às 18h o
   Café vira a Padaria Aurora (item 14; o inicio.js escolhe o modo antes de pintar).
   ============================================================ */
(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const raiz = document.documentElement;
  const embutido = raiz.classList.contains('embutido');
  let modo = raiz.dataset.modo === 'dia' ? 'dia' : 'noite';
  // Os textos no idioma da página: o ferramentas/gerar-cafe.mjs do linu-sites escreve o bloco #textos-cafe em cada
  // versão (pt-BR na raiz, as outras em /<idioma>/); sem o bloco, ficam estes, em português
  const bloco = $('#textos-cafe');
  const T = Object.assign({
    boot: ['Inicializando portal…', 'Calibrando moagem quântica…', 'Sincronizando grãos de Ω-11…', 'Aquecendo reator de vapor…', 'Bem-vindo à fenda.'],
    expresso: 'Expresso Quântico', coldbrew: 'Cold Brew Neural', matcha: 'Matcha do Vazio', estelar: 'Leite de Estrela',
    nivel: 'Nível',
    news_erro: 'Sinal inválido. Verifique as coordenadas do seu e-mail.',
    news_ok: 'Sinal recebido. Você será contactado de outra dimensão.',
    editar: '✎ Editar textos', terminar: '✓ Terminar',
    painel_aviso: 'Clique num texto e escreva. No painel de verdade, o que você muda fica salvo.',
    d_boot: ['Acendendo o forno…', 'Fechando a fenda…', 'Sovando a massa de Ω-11…', 'Esperando a casca dourar…', 'Bom dia.'],
    d_pao: ['Pão de Trigo Solar', 'Pão de Centeio da Penumbra', 'Pão Integral de Órbita', 'Brioche Estelar'],
    d_min: '{n} min'
  }, bloco ? JSON.parse(bloco.textContent) : {});

  // Um quadro só para todas as animações contínuas; para quando não tem ninguém vendo
  const passos = [];
  let pedido = 0, efeitos = true, visivel = true, perto = true;
  const quadro = () => { passos.forEach(f => f()); pedido = requestAnimationFrame(quadro); };
  const conferirQuadro = () => {
    const rodar = efeitos && visivel && perto && !document.hidden && passos.length > 0;
    if (rodar && !pedido) pedido = requestAnimationFrame(quadro);
    if (!rodar && pedido) { cancelAnimationFrame(pedido); pedido = 0; }
  };
  document.addEventListener('visibilitychange', conferirQuadro);

  /* ----------------------------------------------------------
     1. BOOT SCREEN
     ---------------------------------------------------------- */
  const boot     = $('#boot');
  const bootFill = $('#bootFill');
  const bootLog  = $('#bootLog');

  const steps = modo === 'dia' ? T.d_boot : T.boot;

  // Curta (4/11/2026: “o conteúdo vem lento”; em 1/11 eram 3 s): a barra enche em 0,9 s, a tela some logo
  // depois e o conteúdo já está pintado por baixo. Não roda se a abertura já foi vista nesta sessão (.ja-abriu) ou se a pessoa pulou.
  const raizBoot = document.documentElement;
  const semAbertura = embutido || raizBoot.classList.contains('ja-abriu');
  let p = 0, si = 0;
  const bootTimer = semAbertura ? 0 : setInterval(() => {
    if (boot.classList.contains('done')) { clearInterval(bootTimer); return; }
    p = Math.min(100, performance.now() / 900 * 100);
    bootFill.style.width = p + '%';
    const idx = Math.min(steps.length - 1, Math.floor(p / (100 / steps.length)));
    if (idx !== si) { si = idx; bootLog.textContent = steps[idx]; }
    if (p >= 100) { clearInterval(bootTimer); setTimeout(() => boot.classList.add('done'), 150); }
  }, 100);
  // Segurança: nunca travar a página
  if (semAbertura) boot.classList.add('done');
  else setTimeout(() => boot.classList.add('done'), 1400);

  // A prévia que o simulador do Linu Sites pede (2/11/2026, módulo "Abertura de identidade"): mostra a abertura
  // com a duração escolhida (1,5 ou 3 s), mesmo embutido e mesmo já vista. Pula com toque ou tecla, como a de verdade,
  // e desliga tudo o que ligou ao terminar.
  let previa = null;
  const previaAbertura = (ms) => {
    const dur = Math.min(3000, Math.max(500, Number(ms) || 1500));
    if (previa) previa.fim();
    const passos = raiz.dataset.modo === 'dia' ? T.d_boot : T.boot;
    const t0 = performance.now();
    let i = -1, relogio = 0, trava = 0;
    const fim = () => {
      clearInterval(relogio); clearTimeout(trava);
      boot.removeEventListener('click', fim); removeEventListener('keydown', tecla);
      boot.classList.add('done');
      setTimeout(() => { if (previa === controle) { raiz.classList.remove('previa-abertura'); previa = null; } }, 800);
    };
    const tecla = (e) => { if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fim(); } };
    const controle = { fim };
    previa = controle;
    bootFill.style.width = '0%';
    raiz.classList.add('previa-abertura');
    boot.classList.remove('done');
    relogio = setInterval(() => {
      const k = Math.min(1, (performance.now() - t0) / Math.max(1, dur - 300));
      bootFill.style.width = k * 100 + '%';
      const idx = Math.min(passos.length - 1, Math.floor(k * passos.length));
      if (idx !== i) { i = idx; bootLog.textContent = passos[idx]; }
      if (k >= 1) { clearInterval(relogio); setTimeout(fim, 300); }
    }, 100);
    trava = setTimeout(fim, dur + 600);
    boot.addEventListener('click', fim);
    addEventListener('keydown', tecla);
  };

  /* ----------------------------------------------------------
     2. CURSOR PERSONALIZADO
     ---------------------------------------------------------- */
  if (!isTouch) {
    const cur = $('#cur'), dot = $('#curDot');
    let mx = innerWidth / 2, my = innerHeight / 2;
    let cx = mx, cy = my;

    addEventListener('pointermove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
    }, { passive: true });

    // parado no lugar, não regrava o estilo (antes regravava a cada quadro)
    passos.push(() => {
      if (Math.abs(mx - cx) < 0.1 && Math.abs(my - cy) < 0.1) return;
      cx += (mx - cx) * 0.16;
      cy += (my - cy) * 0.16;
      cur.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
    });

    const hoverables = 'a, button, input, .chip, .card, .dim__head';
    document.addEventListener('pointerover', e => {
      if (e.target.closest(hoverables)) cur.classList.add('hovering');
    });
    document.addEventListener('pointerout', e => {
      if (e.target.closest(hoverables)) cur.classList.remove('hovering');
    });
    document.addEventListener('pointerdown', () => cur.style.transform += ' scale(.8)');
  }

  /* ----------------------------------------------------------
     3. CANVAS — GRADE SYNTHWAVE + PARTÍCULAS
     ---------------------------------------------------------- */
  const cvs = $('#bg');
  const ctx = cvs.getContext('2d', { alpha: true });
  let W = 0, H = 0, DPR = 1;

  const particles = [];
  const PARTICLE_COUNT = reduced ? 0 : (innerWidth < 700 ? 34 : 70);

  // O fundo é suave (linhas finas e brilhos): na resolução da página fica igual e desenha até 9× menos pixels num
  // celular de tela densa. Os brilhos das partículas vão pré-desenhados (um por cor), e o fundo anda a 30 quadros.
  let brilhoHorizonte = null;
  const sprites = {};
  function sprite(hue) {
    const tam = 32, c = document.createElement('canvas');
    c.width = c.height = tam;
    const g = c.getContext('2d');
    const r = g.createRadialGradient(tam / 2, tam / 2, 0, tam / 2, tam / 2, tam / 2);
    r.addColorStop(0, `hsla(${hue}, 100%, 70%, 1)`);
    r.addColorStop(0.25, `hsla(${hue}, 100%, 70%, 1)`);
    r.addColorStop(0.26, `hsla(${hue}, 100%, 70%, .12)`);
    r.addColorStop(1, `hsla(${hue}, 100%, 70%, 0)`);
    g.fillStyle = r;
    g.fillRect(0, 0, tam, tam);
    return c;
  }
  sprites[185] = sprite(185);
  sprites[315] = sprite(315);
  // de dia, a farinha no ar: grãos claros e foscos, sem o brilho do neon
  const farinha = (() => {
    const tam = 16, c = document.createElement('canvas');
    c.width = c.height = tam;
    const g = c.getContext('2d');
    const r = g.createRadialGradient(tam / 2, tam / 2, 0, tam / 2, tam / 2, tam / 2);
    r.addColorStop(0, 'hsla(34, 45%, 52%, .9)');
    r.addColorStop(0.45, 'hsla(34, 45%, 52%, .5)');
    r.addColorStop(1, 'hsla(34, 45%, 52%, 0)');
    g.fillStyle = r;
    g.fillRect(0, 0, tam, tam);
    return c;
  })();

  function resize() {
    DPR = 1;
    W = cvs.width  = Math.floor(innerWidth  * DPR);
    H = cvs.height = Math.floor(innerHeight * DPR);
    cvs.style.width  = innerWidth + 'px';
    cvs.style.height = innerHeight + 'px';
    const horizon = H * 0.60;
    brilhoHorizonte = ctx.createLinearGradient(0, horizon - H * 0.18, 0, horizon + H * 0.06);
    brilhoHorizonte.addColorStop(0, 'hsla(315, 100%, 62%, 0)');
    brilhoHorizonte.addColorStop(0.65, 'hsla(300, 100%, 62%, 0.10)');
    brilhoHorizonte.addColorStop(1, 'hsla(185, 100%, 55%, 0)');
  }

  function initParticles() {
    particles.length = 0;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * W,
        y: Math.random() * H,
        r: (Math.random() * 1.6 + 0.4) * DPR,
        vy: -(Math.random() * 0.22 + 0.06) * DPR,
        vx: (Math.random() - 0.5) * 0.14 * DPR,
        a: Math.random() * 0.5 + 0.14,
        hue: Math.random() > 0.5 ? 185 : 315
      });
    }
  }

  resize();
  initParticles();
  addEventListener('resize', () => { resize(); initParticles(); }, { passive: true });

  let t = 0;

  function drawGrid(horizon, speed) {
    const rows = 16;
    const cols = 22;
    const cx = W / 2;

    // Linhas horizontais em perspectiva
    ctx.lineWidth = 1 * DPR;
    for (let i = 0; i < rows; i++) {
      const f = (i + (t * speed) % 1) / rows;
      const y = horizon + (H - horizon) * Math.pow(f, 2.1);
      const alpha = 0.05 + f * 0.20;
      ctx.strokeStyle = `hsla(185, 100%, 58%, ${alpha})`;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }

    // Linhas verticais convergindo
    for (let i = 0; i <= cols; i++) {
      const f = i / cols;
      const x = f * W * 2 - W * 0.5;
      const alpha = 0.03 + Math.sin(f * Math.PI) * 0.10;
      ctx.strokeStyle = `hsla(275, 95%, 68%, ${alpha})`;
      ctx.beginPath();
      ctx.moveTo(cx, horizon);
      ctx.lineTo(x, H);
      ctx.stroke();
    }
  }

  // De dia: só a farinha caindo devagar, de lado, como no balcão da padaria
  function frameDia() {
    ctx.clearRect(0, 0, W, H);
    for (const pt of particles) {
      pt.x += pt.vx * 1.5 + Math.sin(t * 2 + pt.a * 20) * 0.15;
      pt.y -= pt.vy * 1.2;
      if (pt.y > H + 20) { pt.y = -20; pt.x = Math.random() * W; }
      if (pt.x < -20) pt.x = W + 20;
      if (pt.x > W + 20) pt.x = -20;
      ctx.globalAlpha = pt.a * 0.8;
      ctx.drawImage(farinha, pt.x - pt.r * 2.5, pt.y - pt.r * 2.5, pt.r * 5, pt.r * 5);
    }
    ctx.globalAlpha = 1;
  }

  // 30 quadros por segundo bastam para a grade e as partículas; no celular, 20 (4/11/2026: o Café pesava)
  const pulo = isTouch ? 3 : 2;
  let conta = 0;
  function frame() {
    if (++conta % pulo) return;
    t += 0.012;
    if (modo === 'dia') { frameDia(); return; }

    ctx.clearRect(0, 0, W, H);

    const horizon = H * 0.60;
    drawGrid(horizon, 0.35);

    // Brilho no horizonte
    ctx.fillStyle = brilhoHorizonte;
    ctx.fillRect(0, horizon - H * 0.18, W, H * 0.24);

    // Partículas
    for (const pt of particles) {
      pt.x += pt.vx * 2;
      pt.y += pt.vy * 2;

      if (pt.y < -20) { pt.y = H + 20; pt.x = Math.random() * W; }
      if (pt.x < -20) pt.x = W + 20;
      if (pt.x > W + 20) pt.x = -20;

      // o ponto e o halo (4× o raio) de uma vez, do sprite da cor
      ctx.globalAlpha = pt.a;
      ctx.drawImage(sprites[pt.hue], pt.x - pt.r * 4, pt.y - pt.r * 4, pt.r * 8, pt.r * 8);
    }
    ctx.globalAlpha = 1;
  }

  // Sem movimento: um quadro parado (a grade de noite; de dia, o fundo limpo)
  function fundoParado() {
    ctx.clearRect(0, 0, W, H);
    if (modo === 'noite') drawGrid(H * 0.6, 0);
  }
  if (reduced) {
    fundoParado();
  } else {
    passos.push(frame);
  }

  /* ----------------------------------------------------------
     4. NAV — scroll, mobile e link ativo
     ---------------------------------------------------------- */
  const nav = $('#nav');
  const burger = $('#burger');
  const navLinks = $('#navLinks');

  const onScroll = () => nav.classList.toggle('solid', scrollY > 40);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  burger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
  });

  navLinks.addEventListener('click', e => {
    if (e.target.tagName === 'A') {
      navLinks.classList.remove('open');
      burger.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });

  // Link ativo por seção
  const sections = $$('main section[id]');
  const linkMap = new Map(
    $$('#navLinks a').map(a => [a.getAttribute('href').slice(1), a])
  );

  const navObserver = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        linkMap.forEach(a => a.classList.remove('active'));
        const a = linkMap.get(en.target.id);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });

  sections.forEach(s => navObserver.observe(s));

  /* ----------------------------------------------------------
     5. REVEAL ON SCROLL
     ---------------------------------------------------------- */
  const revealObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        en.target.classList.add('in');
        obs.unobserve(en.target);
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px 12% 0px' }); // entra um pouco antes de aparecer

  $$('.reveal').forEach(el => revealObserver.observe(el));

  // 4/11/2026, o Café estava pesado: com a tela parada, o fundo e as animações em CSS gastavam um terço do processador
  // de um celular simples. O fundo anda só enquanto a abertura (#inicio) está à vista; depois fica parado no último
  // quadro, atrás do texto. As animações em loop param quando a parte delas sai da tela (.pausa, no estilo.css).
  const vigia = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.target.id === 'inicio') { perto = en.isIntersecting; conferirQuadro(); }
    en.target.classList.toggle('pausa', !en.isIntersecting);
  }), { rootMargin: '80px 0px' });
  $$('#inicio, .marquee, #sobre, #laboratorio, .cta, footer').forEach(el => vigia.observe(el));

  /* ----------------------------------------------------------
     6. CARDS — tilt 3D + spotlight
     ---------------------------------------------------------- */
  if (!isTouch && !reduced) {
    $$('.tilt').forEach(card => {
      let raf = null;

      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width;
        const py = (e.clientY - r.top) / r.height;

        card.style.setProperty('--mx', (px * 100) + '%');
        card.style.setProperty('--my', (py * 100) + '%');

        if (raf) return;
        raf = requestAnimationFrame(() => {
          const rx = (0.5 - py) * 9;
          const ry = (px - 0.5) * 11;
          card.style.transform =
            `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-6px)`;
          raf = null;
        });
      });

      card.addEventListener('pointerleave', () => {
        card.style.transform = '';
      });
    });
  }

  /* ----------------------------------------------------------
     7. BOTÕES MAGNÉTICOS
     ---------------------------------------------------------- */
  if (!isTouch && !reduced) {
    $$('.magnetic').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.22;
        const y = (e.clientY - r.top - r.height / 2) * 0.32;
        btn.style.transform = `translate(${x}px, ${y}px)`;
      });
      btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
    });
  }

  /* ----------------------------------------------------------
     8. LABORATÓRIO — SINTETIZADOR DE BEBIDA
     ---------------------------------------------------------- */
  const BASES = {
    expresso: {
      name: T.expresso,
      h: 26, s: 62, l: 24,
      foam: 'rgba(214, 178, 130, .45)',
      glow: 'hsla(28, 90%, 55%, .35)'
    },
    coldbrew: {
      name: T.coldbrew,
      h: 20, s: 46, l: 14,
      foam: 'rgba(150, 110, 80, .32)',
      glow: 'hsla(200, 95%, 60%, .32)'
    },
    matcha: {
      name: T.matcha,
      h: 148, s: 62, l: 40,
      foam: 'rgba(200, 255, 210, .40)',
      glow: 'hsla(148, 90%, 55%, .34)'
    },
    estelar: {
      name: T.estelar,
      h: 268, s: 82, l: 72,
      foam: 'rgba(255, 255, 255, .55)',
      glow: 'hsla(268, 95%, 70%, .40)'
    }
  };

  const BASE_PRICE = { expresso: 16, coldbrew: 19, matcha: 21, estelar: 18 };
  const TOP_PRICE  = 3.5;

  // De dia, as mesmas quatro escolhas são farinhas: a casca vai da cor crua (claro) à bem assada (escuro)
  const PAES = {
    expresso: { i: 0, h: 34, s: 68, claro: 74, escuro: 30, preco: 3 },
    coldbrew: { i: 1, h: 22, s: 42, claro: 56, escuro: 18, preco: 4 },
    matcha:   { i: 2, h: 28, s: 52, claro: 62, escuro: 22, preco: 4 },
    estelar:  { i: 3, h: 40, s: 88, claro: 72, escuro: 34, preco: 5 }
  };

  const form      = $('#labForm');
  const intEl     = $('#intensity');
  const intVal    = $('#intVal');
  const liquid    = $('#liquid');
  const cupGlow   = $('#cupGlow');
  const nameOut   = $('#drinkName');
  const priceOut  = $('#drinkPrice');
  const pao       = $('#pao');
  const forno     = $('#forno');
  const preco = v => '₡ ' + v.toLocaleString(raiz.lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function atualizarPao(baseKey, intensity, marcadas) {
    const p = PAES[baseKey];
    const l = p.claro - (intensity - 1) * (p.claro - p.escuro) / 9;
    pao.style.setProperty('--casca', `hsl(${p.h} ${p.s}% ${l}%)`);
    pao.style.setProperty('--miolo', `hsl(${p.h} ${p.s}% ${Math.min(88, l + 22)}%)`);
    pao.style.height = (104 + intensity * 3) + 'px'; // cresce um pouco no forno
    pao.classList.toggle('estelar', baseKey === 'estelar');
    for (let n = 1; n <= 4; n++) pao.classList.toggle('com-' + n, marcadas.some(i => i.dataset.cob === String(n)));
    forno.style.background = `radial-gradient(circle, hsla(${28 + intensity}, 95%, 58%, ${0.18 + intensity * 0.03}), transparent 65%)`;

    let nome = `${T.d_pao[p.i]} · ${T.d_min.replace('{n}', 12 + intensity * 3)}`;
    const nomes = marcadas.map(i => i.nextElementSibling.querySelector('.so-dia').textContent);
    if (nomes.length) nome += ` + ${nomes.join(' + ')}`;
    nameOut.textContent = nome;
    priceOut.textContent = preco(p.preco + intensity * 0.2 + marcadas.length * 1.5);
    priceOut.dataset.valor = p.preco + intensity * 0.2 + marcadas.length * 1.5;
  }

  function updateDrink() {
    const baseKey = form.querySelector('input[name="base"]:checked').value;
    const base = BASES[baseKey];
    const intensity = Number(intEl.value);          // 1..10
    const marcadas = $$('input[name="top[]"]:checked', form);
    const tops = marcadas.map(i => i.value);

    intVal.textContent = intensity;
    // os modificadores aparecem na xícara (com-1 a com-4), como as coberturas no pão de dia
    const xicara = liquid.closest('.cup-wrap');
    for (let n = 1; n <= 4; n++) xicara.classList.toggle('com-' + n, marcadas.some(i => i.dataset.cob === String(n)));
    if (modo === 'dia') { atualizarPao(baseKey, intensity, marcadas); return; }

    // Cor: mais intenso = mais escuro e saturado
    const l = Math.max(6, base.l - (intensity - 5) * 2.4);
    const s = Math.min(100, base.s + (intensity - 5) * 3);
    const color = `hsl(${base.h} ${s}% ${l}%)`;

    liquid.style.background = color;
    liquid.style.setProperty('--foam', base.foam);
    liquid.style.height = (48 + intensity * 3.4) + '%';
    cupGlow.style.background =
      `radial-gradient(circle, ${base.glow}, transparent 65%)`;

    // Nome
    const roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X'][intensity - 1];
    let name = `${base.name} · ${T.nivel} ${roman}`;
    if (tops.length) name += ` + ${tops.join(' + ')}`;
    nameOut.textContent = name;

    // Preço
    const price = BASE_PRICE[baseKey] + intensity * 0.55 + tops.length * TOP_PRICE;
    priceOut.textContent = preco(price);
    priceOut.dataset.valor = price;
  }

  form.addEventListener('input', updateDrink);
  form.addEventListener('change', updateDrink);
  updateDrink();

  /* ----------------------------------------------------------
     9. PAINEL DE DIMENSÃO (hue shift)
     ---------------------------------------------------------- */
  const hueEl   = $('#hue');
  const hueVal  = $('#hueVal');
  const dim     = $('#dim');
  const dimHead = $('#dimHead');
  const chev    = $('#dimChevron');

  hueEl.addEventListener('input', () => {
    const v = Number(hueEl.value);
    hueVal.textContent = v + '°';
    // as quatro cores de cada modo saem do --desvio no CSS (bloco 0 e bloco 17)
    raiz.style.setProperty('--desvio', v);
  });

  dimHead.addEventListener('click', () => {
    const collapsed = dim.classList.toggle('collapsed');
    dimHead.setAttribute('aria-expanded', String(!collapsed));
    chev.textContent = collapsed ? '▴' : '▾';
  });

  // Três versões (1/11/2026): no celular, o "Pedir agora" do topo (escondido ali) vira um botão preso embaixo,
  // ao alcance do polegar; é uma cópia do link do topo, já no idioma da página
  const pedirTopo = document.querySelector('.nav__right .btn');
  if (pedirTopo && !document.querySelector('.pedir-celular')) {
    const pedir = pedirTopo.cloneNode(true);
    pedir.classList.remove('magnetic');
    pedir.classList.add('pedir-celular');
    const caixa = document.createElement('nav');
    caixa.setAttribute('aria-label', pedirTopo.textContent.trim());
    caixa.append(pedir);
    document.body.append(caixa);
  }
  // o cardápio vira faixa que rola de lado no celular: dá para rolar pelo teclado, com o nome da seção
  const faixa = document.querySelector('.menu-grid');
  const tituloCardapio = faixa && faixa.closest('section') && faixa.closest('section').querySelector('h2');
  if (faixa) {
    faixa.setAttribute('tabindex', '0');
    faixa.setAttribute('role', 'region');
    faixa.setAttribute('aria-label', tituloCardapio ? tituloCardapio.textContent.trim() : 'Menu');
  }

  // Começa recolhido no mobile
  if (innerWidth < 640) {
    dim.classList.add('collapsed');
    dimHead.setAttribute('aria-expanded', 'false');
    chev.textContent = '▴';
  }

  /* ----------------------------------------------------------
     10. NEWSLETTER
     ---------------------------------------------------------- */
  const newsForm = $('#newsForm');
  const newsMsg  = $('#newsMsg');
  const emailIn  = $('#email');

  newsForm.addEventListener('submit', e => {
    e.preventDefault();
    const v = emailIn.value.trim();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

    if (!ok) {
      newsMsg.style.color = 'var(--magenta)';
      newsMsg.textContent = T.news_erro;
      emailIn.focus();
      return;
    }

    newsMsg.style.color = 'var(--cyan)';
    newsMsg.textContent = T.news_ok;
    emailIn.value = '';
  });

  /* ----------------------------------------------------------
     11. ANO NO FOOTER
     ---------------------------------------------------------- */
  $('#year').textContent = new Date().getFullYear();

  /* ----------------------------------------------------------
     12. PARALLAX SUAVE DO HERO (halo)
     ---------------------------------------------------------- */
  if (!reduced && !isTouch) {
    const halo = $('.hero__halo');
    let px = 0, py = 0, tx = 0, ty = 0;

    addEventListener('pointermove', e => {
      tx = (e.clientX / innerWidth - 0.5) * 46;
      ty = (e.clientY / innerHeight - 0.5) * 46;
    }, { passive: true });

    passos.push(() => {
      if (Math.abs(tx - px) < 0.05 && Math.abs(ty - py) < 0.05) return;
      px += (tx - px) * 0.06;
      py += (ty - py) * 0.06;
      halo.style.transform = `translate3d(${px}px, ${py}px, 0)`;
    });
  }

  /* ----------------------------------------------------------
     14. MODO DIA (A PADARIA) E MODO NOITE (O CAFÉ)
     Os textos de cada modo já estão na página (.so-dia e .so-noite) e o
     CSS esconde os do outro; aqui ficam o que muda por atributo, o botão
     de sol e lua e a virada: o neon pisca, o sol nasce (ou a lua desce)
     e o modo troca com a tela coberta.
     ---------------------------------------------------------- */
  const botaoModo = $('#modo');
  const corTema = $('meta[name="theme-color"]');

  function aplicarModo(novo) {
    modo = novo;
    raiz.dataset.modo = novo;
    const outro = novo === 'dia' ? 'noite' : 'dia';
    botaoModo.setAttribute('aria-label', botaoModo.dataset['para' + outro[0].toUpperCase() + outro.slice(1)]);
    botaoModo.title = botaoModo.getAttribute('aria-label');
    $$('[data-aria-dia]').forEach(el => {
      if (!el.dataset.ariaNoite) el.dataset.ariaNoite = el.getAttribute('aria-label');
      el.setAttribute('aria-label', novo === 'dia' ? el.dataset.ariaDia : el.dataset.ariaNoite);
    });
    corTema.content = novo === 'dia' ? '#fbf3e4' : '#05030a';
    // o título da aba acompanha (de dia, a padaria), quando a página tem o texto de dia
    if (!raiz.dataset.tituloNoite) raiz.dataset.tituloNoite = document.title;
    if (T.d_titulo) document.title = novo === 'dia' ? T.d_titulo : raiz.dataset.tituloNoite;
    raiz.dispatchEvent(new Event('modo')); // o simulador do Linu Sites troca os textos dele (bloco 13)
    updateDrink();
    if (reduced) fundoParado();
  }

  let virando = false;
  botaoModo.addEventListener('click', () => {
    if (virando) return;
    const novo = modo === 'dia' ? 'noite' : 'dia';
    try { localStorage.setItem('aurora-modo', novo); } catch (e) {}
    if (reduced || !efeitos) { aplicarModo(novo); return; }
    virando = true;
    raiz.classList.add('piscando');
    const virada = document.createElement('div');
    virada.className = 'virada virada--' + novo;
    virada.setAttribute('aria-hidden', 'true');
    virada.innerHTML = '<i class="virada__astro"></i>';
    setTimeout(() => document.body.append(virada), 260);
    setTimeout(() => { raiz.classList.remove('piscando'); aplicarModo(novo); }, 260 + 650);
    setTimeout(() => { virada.remove(); virando = false; }, 260 + 1300);
  });
  aplicarModo(modo);

  conferirQuadro();

  /* ----------------------------------------------------------
     13. LINU SITES — MÓDULOS DO SIMULADOR
     A página principal manda {cafeAurora: {modulos, visivel}} por
     postMessage (só de sites.linupedia.com.br). Cada módulo desligado vira
     uma classe "sem-..." no <html> (ver o bloco 16 do CSS).
     ---------------------------------------------------------- */
  // O simulador fica no Linu Sites, num endereço diferente do Café: só ele pode ligar e desligar as partes
  const ORIGEM_SIMULADOR = 'https://sites.linupedia.com.br';
  const MODULOS = ['depoimentos', 'efeitos', 'cores', 'laboratorio', 'assinatura', 'pedido', 'cardapio', 'teste', 'reservas', 'fidelidade'];
  // os módulos do site completo (1/11/2026) começam desligados no simulador, até ele dizer quais estão na conta
  if (embutido) ['pedido', 'cardapio', 'teste', 'reservas', 'fidelidade'].forEach(m => raiz.classList.add('sem-' + m));
  const painel = $('#painelDemo');
  const painelBotao = $('#painelBotao');
  const painelAviso = $('#painelAviso');
  const editaveis = () => $$('main h2, main h3, main p, main li, main blockquote')
    .filter(el => !el.closest('form, #labForm, footer .foot__bottom'));

  function editar(ligar) {
    raiz.classList.toggle('editando', ligar);
    editaveis().forEach(el => {
      if (ligar) el.setAttribute('contenteditable', 'true');
      else el.removeAttribute('contenteditable');
    });
    painelBotao.setAttribute('aria-pressed', String(ligar));
    painelBotao.textContent = ligar ? T.terminar : T.editar;
    painelAviso.textContent = ligar ? T.painel_aviso : '';
  }
  painelBotao.addEventListener('click', () => editar(!raiz.classList.contains('editando')));

  addEventListener('message', e => {
    if (e.origin !== ORIGEM_SIMULADOR || !e.data || !e.data.cafeAurora) return;
    const { modulos, visivel: v } = e.data.cafeAurora;
    if (Array.isArray(modulos)) {
      MODULOS.forEach(m => raiz.classList.toggle('sem-' + m, !modulos.includes(m)));
      efeitos = modulos.includes('efeitos');
      const comPainel = modulos.includes('painel');
      painel.hidden = !comPainel;
      if (!comPainel) editar(false);
      raiz.dispatchEvent(new Event('modulos'));
    }
    if (typeof v === 'boolean') visivel = v;
    if (e.data.cafeAurora.verAbertura) previaAbertura(e.data.cafeAurora.verAbertura);
    conferirQuadro();
  });
  // o simulador fica sabendo se o Café está de noite (café) ou de dia (padaria), para falar do pão ou da bebida
  if (embutido) {
    parent.postMessage({ cafeAurora: 'pronto', modo }, ORIGEM_SIMULADOR);
    raiz.addEventListener('modo', () => parent.postMessage({ cafeAurora: { modo } }, ORIGEM_SIMULADOR));
  }

  /* ----------------------------------------------------------
     15. O SITE COMPLETO (1/11/2026): pedido com WhatsApp, filtros e
     detalhes do cardápio, o teste, reservas e o cartão de carimbos.
     Embutido no simulador do Linu Sites, nada disso aparece: o
     simulador só vende o que está na tabela dele. O que a pessoa faz
     fica no localStorage deste navegador.
     ---------------------------------------------------------- */
  if (!$('#pedido')) return; // página antiga, de antes destas partes
  $$('.so-completo').forEach(el => { el.hidden = false; });
  // o Café sem internet: o sw.js fica na raiz do Café (as páginas dos idiomas estão um nível abaixo); no simulador, não
  if (!embutido && 'serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    const raizCafe = new URL(document.querySelector('script[src*="script.js"]').getAttribute('src').replace(/script\.js.*$/, ''), location.href);
    navigator.serviceWorker.register(new URL('sw.js', raizCafe), { scope: raizCafe.href }).catch(() => {});
  }
  const guardado = (k, padrao) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? padrao : v; } catch (e) { return padrao; } };
  const guardar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const f = (txt, dados) => txt.replace(/\{(\w+)\}/g, (_, k) => dados[k] ?? '');
  const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
  const loja = () => modo === 'dia' ? T.d_nome : 'Café Aurora';
  const moeda = v => '₡ ' + Number(v).toLocaleString(raiz.lang, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const cartoes = $$('.menu-grid .card');
  const nomeDe = c => (modo === 'dia' ? c.querySelector('h3 .so-dia') : c.querySelector('h3 .so-noite')).textContent.trim();
  const precoDe = c => Number(modo === 'dia' ? c.dataset.precoDia : c.dataset.precoNoite);
  const filtrosDe = c => (modo === 'dia' ? c.dataset.filtrosDia : c.dataset.filtrosNoite).split(' ');

  // ---- o pedido
  const janelaPedido = $('#pedido');
  let itens = guardado('aurora-pedido', []);
  const listaPedido = $('#pedidoItens'), totalPedido = $('#pedidoTotal'), vazio = $('#pedidoVazio');
  const formPedido = $('#pedidoForm'), feito = $('#pedidoFeito'), seloPedido = $('#pedidoSelo');
  const contadores = () => $$('.pedir-n');
  function desenharPedido() {
    guardar('aurora-pedido', itens);
    const n = itens.reduce((a, i) => a + i.q, 0);
    contadores().forEach(c => { c.textContent = n; c.hidden = n === 0; });
    vazio.hidden = itens.length > 0;
    formPedido.hidden = itens.length === 0;
    $('#pedidoTotalLinha').hidden = itens.length === 0;
    listaPedido.replaceChildren(...itens.map((i, k) => {
      const li = el('li', 'pedido__item');
      const menos = el('button', 'qtd', '−'); menos.type = 'button'; menos.setAttribute('aria-label', f(T.menos, { nome: i.nome }));
      const mais = el('button', 'qtd', '+'); mais.type = 'button'; mais.setAttribute('aria-label', f(T.mais, { nome: i.nome }));
      menos.addEventListener('click', () => { i.q--; if (i.q <= 0) itens.splice(k, 1); desenharPedido(); (listaPedido.querySelector('.qtd') || janelaPedido.querySelector('[data-fechar]')).focus(); });
      mais.addEventListener('click', () => { i.q++; desenharPedido(); listaPedido.children[k].querySelectorAll('.qtd')[1].focus(); });
      const q = el('span', 'pedido__q', String(i.q));
      li.append(el('span', 'pedido__nome', i.nome), el('span', 'pedido__ctl'), el('b', null, moeda(i.preco * i.q)));
      li.children[1].append(menos, q, mais);
      return li;
    }));
    totalPedido.textContent = moeda(itens.reduce((a, i) => a + i.preco * i.q, 0));
    seloPedido.textContent = f(T.selo, { n: guardado('aurora-carimbos', 0) % 10 });
  }
  const aviso = el('p', 'aviso-pedido'); aviso.setAttribute('role', 'status'); aviso.setAttribute('aria-live', 'polite'); document.body.append(aviso);
  let avisoTempo = 0;
  function adicionar(nome, preco) {
    const ja = itens.find(i => i.nome === nome && i.preco === preco);
    if (ja) ja.q++; else itens.push({ nome, preco, q: 1 });
    desenharPedido();
    aviso.textContent = f(T.no_pedido, { nome });
    aviso.classList.add('visivel'); clearTimeout(avisoTempo);
    avisoTempo = setTimeout(() => aviso.classList.remove('visivel'), 2600);
  }
  function abrirPedido() {
    feito.hidden = true; formPedido.hidden = itens.length === 0;
    desenharPedido();
    janelaPedido.showModal();
  }
  // os botões "Pedir agora" (o do topo e o preso embaixo no celular) abrem o pedido, com o número de itens
  $$('.nav__right .btn, .pedir-celular').forEach(b => {
    const n = el('span', 'pedir-n'); n.hidden = true; b.append(' ', n);
    // com o módulo "pedido" desligado no simulador, o botão volta a levar ao laboratório, como antes
    b.addEventListener('click', e => { if (raiz.classList.contains('sem-pedido')) return; e.preventDefault(); abrirPedido(); });
  });
  cartoes.forEach(c => {
    const b = c.querySelector('.card__add');
    const rotulo = () => b.setAttribute('aria-label', f(T.add_aria, { nome: nomeDe(c) }));
    rotulo(); b.addEventListener('click', () => adicionar(nomeDe(c), precoDe(c)));
    b.addEventListener('focus', rotulo);
  });
  $('#labAdd').addEventListener('click', () => adicionar($('#drinkName').textContent.trim(), Math.round(Number($('#drinkPrice').dataset.valor) * 100) / 100));
  $$('.janela [data-fechar]').forEach(b => b.addEventListener('click', () => b.closest('dialog').close()));
  $$('.janela').forEach(d => d.addEventListener('click', e => { if (e.target === d) d.close(); }));

  const nomeIn = $('#pNome'), nomeErro = $('#pNomeErro');
  const validarNome = () => { const ok = nomeIn.value.trim() !== ''; nomeErro.hidden = ok; nomeIn.setAttribute('aria-invalid', String(!ok)); return ok; };
  nomeIn.value = guardado('aurora-nome', '');
  nomeIn.addEventListener('blur', () => { if (nomeIn.value) validarNome(); });
  nomeIn.addEventListener('input', () => { if (nomeIn.getAttribute('aria-invalid') === 'true') validarNome(); });
  formPedido.addEventListener('submit', e => {
    e.preventDefault();
    if (!validarNome()) { nomeIn.focus(); return; }
    guardar('aurora-nome', nomeIn.value.trim());
    const fd = new FormData(formPedido);
    const linhas = [f(T.msg_cab, { loja: loja() }), ...itens.map(i => `${i.q}× ${i.nome} — ${moeda(i.preco * i.q)}`),
      `${T.msg_total}: ${totalPedido.textContent}`, `${T.msg_nome}: ${fd.get('nome').trim()}`, fd.get('como') === 'levar' ? T.msg_levar : T.msg_aqui];
    if (fd.get('hora')) linhas.push(`${T.msg_hora} ${fd.get('hora')}`);
    if (fd.get('obs').trim()) linhas.push(`${T.msg_obs} ${fd.get('obs').trim()}`);
    const link = 'https://wa.me/?text=' + encodeURIComponent(linhas.join('\n'));
    window.open(link, '_blank', 'noopener');
    const carimbos = Math.min(10, guardado('aurora-carimbos', 0) + 1);
    guardar('aurora-carimbos', carimbos);
    itens = []; desenharPedido(); desenharCartao();
    formPedido.hidden = true; vazio.hidden = true; $('#pedidoTotalLinha').hidden = true;
    const de_novo = el('a', 'btn btn--ghost', T.feito_abrir); de_novo.href = link; de_novo.target = '_blank'; de_novo.rel = 'noopener';
    feito.replaceChildren(el('p', null, f(T.feito, { n: carimbos })), de_novo);
    feito.hidden = false; feito.focus();
  });

  // ---- os filtros e os detalhes do cardápio
  const contaMenu = $('#menuConta'), menuVazio = $('#menuVazio');
  let filtro = '';
  function filtrar() {
    let n = 0;
    cartoes.forEach(c => { const ok = !filtro || filtrosDe(c).includes(filtro); c.hidden = !ok; if (ok) n++; });
    contaMenu.textContent = f(T.f_n, { n, total: cartoes.length });
    menuVazio.hidden = n > 0;
  }
  $$('.filtro').forEach(b => b.addEventListener('click', () => {
    filtro = b.dataset.filtro;
    $$('.filtro').forEach(o => o.setAttribute('aria-pressed', String(o.dataset.filtro === filtro)));
    filtrar();
  }));
  filtrar();

  // ---- o teste: três perguntas, e o item do cardápio (do modo de agora) que mais combina
  const janelaQuiz = $('#quiz'), corpoQuiz = $('#quizCorpo');
  function quiz() {
    const perguntas = modo === 'dia' ? T.qz_dia : T.qz_noite;
    const escolhas = [];
    const passo = () => {
      if (escolhas.length === perguntas.length) return resultado();
      const [pergunta, opcoes] = perguntas[escolhas.length];
      const h = el('h3', 'quiz__pergunta', pergunta); h.tabIndex = -1;
      const ops = el('div', 'quiz__opcoes');
      opcoes.forEach(([rot, tag]) => { const b = el('button', 'btn', rot); b.type = 'button'; b.addEventListener('click', () => { escolhas.push(tag); passo(); }); ops.append(b); });
      corpoQuiz.replaceChildren(el('p', 'quiz__passo', f(T.qz_passo, { n: escolhas.length + 1, total: perguntas.length })), h, ops);
      h.focus();
    };
    const resultado = () => {
      const nota = c => escolhas.reduce((a, t) => a + (!t ? 0 : t === 'cafeina' ? !filtrosDe(c).includes('sem-cafeina') : filtrosDe(c).includes(t)), 0);
      const melhor = cartoes.reduce((a, c) => nota(c) > nota(a) ? c : a, cartoes[0]);
      const h = el('h3', 'quiz__nome', nomeDe(melhor)); h.tabIndex = -1;
      const desc = (modo === 'dia' ? melhor.querySelector('p.so-dia') : melhor.querySelector('p.so-noite')).textContent;
      const add = el('button', 'btn btn--magenta', '+ ' + T.lab_add); add.type = 'button';
      add.addEventListener('click', () => { adicionar(nomeDe(melhor), precoDe(melhor)); janelaQuiz.close(); });
      const outra = el('button', 'btn btn--ghost', T.qz_de_novo); outra.type = 'button'; outra.addEventListener('click', quiz);
      const acoes = el('div', 'quiz__opcoes'); acoes.append(add, outra);
      corpoQuiz.replaceChildren(el('p', 'quiz__passo', T.qz_resultado), h, el('p', null, desc), el('p', 'quiz__preco', moeda(precoDe(melhor))), acoes);
      h.focus();
    };
    passo();
  }
  $('#quizAbrir').addEventListener('click', () => { janelaQuiz.showModal(); quiz(); });

  // ---- o cartão de carimbos
  const carimbosEl = $$('#carimbos li'), fidMsg = $('#fidMsg'), fidUsar = $('#fidUsar');
  function desenharCartao() {
    const n = guardado('aurora-carimbos', 0);
    carimbosEl.forEach((li, i) => li.classList.toggle('carimbado', i < n));
    fidMsg.textContent = n >= 10 ? T.fid_premio : f(T.fid_n, { n });
    fidUsar.hidden = n < 10;
  }
  fidUsar.addEventListener('click', () => { guardar('aurora-carimbos', 0); desenharCartao(); fidMsg.textContent = T.fid_usado; });
  desenharCartao();

  // ---- reservas: validação na hora, guardadas neste aparelho e a confirmação pronta para o WhatsApp
  const formReserva = $('#reservaForm'), msgReserva = $('#reservaMsg'), minhas = $('#minhas'), minhasLista = $('#minhasLista');
  const hoje = () => { const d = new Date(); d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); return d.toISOString().slice(0, 10); };
  formReserva.elements.data.min = hoje();
  const regras = {
    nome: c => c.value.trim() !== '',
    pessoas: c => Number(c.value) >= 1 && Number(c.value) <= 8,
    data: c => c.value !== '' && c.value >= hoje(),
    hora: c => {
      const erro = $('#rHoraErro');
      if (!c.value) { erro.textContent = T.r_hora_erro; return false; }
      const [h, m] = c.value.split(':').map(Number), min = h * 60 + m;
      if (modo === 'dia' && (min < 360 || min > 1080)) { erro.textContent = T.r_hora_dia; return false; }
      if (modo !== 'dia' && min >= 240 && min < 360) { erro.textContent = T.r_hora_noite; return false; }
      return true;
    }
  };
  const ERROS = { nome: '#rNomeErro', pessoas: '#rPessoasErro', data: '#rDataErro', hora: '#rHoraErro' };
  const validar = k => { const c = formReserva.elements[k], ok = regras[k](c); $(ERROS[k]).hidden = ok; c.setAttribute('aria-invalid', String(!ok)); return ok; };
  Object.keys(regras).forEach(k => {
    const c = formReserva.elements[k];
    c.addEventListener('change', () => validar(k));
    c.addEventListener('input', () => { if (c.getAttribute('aria-invalid') === 'true') validar(k); });
  });
  formReserva.elements.nome.value = guardado('aurora-nome', '');
  const dataBonita = d => new Date(d + 'T12:00').toLocaleDateString(raiz.lang, { weekday: 'short', day: 'numeric', month: 'short' });
  function desenharReservas() {
    const lista = guardado('aurora-reservas', []).filter(r => r.data >= hoje());
    guardar('aurora-reservas', lista);
    minhas.hidden = lista.length === 0;
    minhasLista.replaceChildren(...lista.map((r, k) => {
      const li = el('li', 'minha');
      const texto = f(T.r_ok, { mesa: r.mesa, pessoas: r.pessoas, data: dataBonita(r.data), hora: r.hora });
      const whats = el('a', 'btn btn--ghost', T.r_whats); whats.target = '_blank'; whats.rel = 'noopener';
      whats.href = 'https://wa.me/?text=' + encodeURIComponent(f(T.r_msg, { loja: r.loja, mesa: r.mesa, pessoas: r.pessoas, data: dataBonita(r.data), hora: r.hora, nome: r.nome }));
      const cancelar = el('button', 'btn btn--ghost', T.r_cancelar); cancelar.type = 'button';
      cancelar.addEventListener('click', () => { const l = guardado('aurora-reservas', []); l.splice(k, 1); guardar('aurora-reservas', l); desenharReservas(); formReserva.elements.nome.focus(); });
      const acoes = el('div', 'minha__acoes'); acoes.append(whats, cancelar);
      li.append(el('p', null, texto), acoes);
      return li;
    }));
  }
  formReserva.addEventListener('submit', e => {
    e.preventDefault();
    const erradas = Object.keys(regras).filter(k => !validar(k));
    if (erradas.length) { formReserva.elements[erradas[0]].focus(); msgReserva.textContent = ''; return; }
    const fd = new FormData(formReserva);
    const r = { nome: fd.get('nome').trim(), pessoas: Number(fd.get('pessoas')), data: fd.get('data'), hora: fd.get('hora'), mesa: fd.get('mesa'), loja: loja() };
    const lista = guardado('aurora-reservas', []); lista.push(r); lista.sort((a, b) => (a.data + a.hora).localeCompare(b.data + b.hora));
    guardar('aurora-reservas', lista); guardar('aurora-nome', r.nome);
    msgReserva.textContent = f(T.r_ok, { mesa: r.mesa, pessoas: r.pessoas, data: dataBonita(r.data), hora: r.hora });
    desenharReservas();
  });
  desenharReservas();

  // o modo (café ou padaria) muda o cardápio: refaz os filtros e o que depende do nome dos itens
  const semFiltro = () => { filtro = ''; $$('.filtro').forEach(o => o.setAttribute('aria-pressed', String(o.dataset.filtro === ''))); filtrar(); };
  new MutationObserver(semFiltro).observe(raiz, { attributes: true, attributeFilter: ['data-modo'] });
  // o simulador desligou os filtros: o cardápio volta inteiro
  raiz.addEventListener('modulos', () => { if (raiz.classList.contains('sem-cardapio')) semFiltro(); });
  desenharPedido();

})();
