/* ============================================================
   CAFÉ AURORA — JS (com Bootstrap)
   ============================================================ */
(() => {
  'use strict';
  // Os textos no idioma da página (o gerar-cafe.mjs do linu-sites escreve o bloco #textos-cafe); sem ele, em português
  const blocoT = document.getElementById('textos-cafe');
  const T = Object.assign({
    boot: ['Inicializando portal…', 'Calibrando moagem quântica…', 'Sincronizando grãos de Ω-11…', 'Aquecendo reator de vapor…', 'Bem-vindo à fenda.'],
    expresso: 'Expresso Quântico', coldbrew: 'Cold Brew Neural', matcha: 'Matcha do Vazio', estelar: 'Leite de Estrela', nivel: 'Nível',
    news_erro: 'Sinal inválido. Verifique as coordenadas do seu e-mail.', news_ok: 'Sinal recebido. Você será contactado de outra dimensão.'
  }, blocoT ? JSON.parse(blocoT.textContent) : {});
  const precoT = v => '₡ ' + v.toLocaleString(document.documentElement.lang || 'pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });


  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- 1. BOOT ---------- */
  const boot = $('#boot'), bootFill = $('#bootFill'), bootLog = $('#bootLog');
  const steps = (document.documentElement.dataset.modo === 'dia' && T.d_boot) || T.boot;
  // 3 segundos desde o começo da página (pedido de 1/11/2026): a barra enche em 2,6 s e a tela some
  // logo depois. Não roda se a abertura já foi vista nesta sessão (.ja-abriu) ou se a pessoa pulou.
  const raizBoot = document.documentElement;
  const semAbertura = raizBoot.classList.contains('ja-abriu');
  let p = 0, si = 0;
  const bootTimer = semAbertura ? 0 : setInterval(() => {
    if (boot.classList.contains('done')) { clearInterval(bootTimer); return; }
    p = Math.min(100, performance.now() / 900 * 100); // curta desde 4/11/2026 (eram 3 s)
    bootFill.style.width = p + '%';
    const idx = Math.min(steps.length - 1, Math.floor(p / (100 / steps.length)));
    if (idx !== si) { si = idx; bootLog.textContent = steps[idx]; }
    if (p >= 100) { clearInterval(bootTimer); setTimeout(() => boot.classList.add('done'), 150); }
  }, 100);
  // Segurança: nunca travar a página
  if (semAbertura) boot.classList.add('done');
  else setTimeout(() => boot.classList.add('done'), 1400);

  /* ---------- 2. CURSOR ---------- */
  if (!isTouch) {
    const cur = $('#cur'), dot = $('#curDot');
    let mx = innerWidth / 2, my = innerHeight / 2, cx = mx, cy = my;
    addEventListener('pointermove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
    }, { passive: true });
    (function loop() {
      cx += (mx - cx) * 0.16;
      cy += (my - cy) * 0.16;
      cur.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loop);
    })();
    const hov = 'a, button, input, .chip, .card-aurora, .dim__head, .navbar-toggler';
    document.addEventListener('pointerover', e => {
      if (e.target.closest(hov)) cur.classList.add('hovering');
    });
    document.addEventListener('pointerout', e => {
      if (e.target.closest(hov)) cur.classList.remove('hovering');
    });
  }

  /* ---------- 3. CANVAS ---------- */
  const cvs = $('#bg');
  const ctx = cvs.getContext('2d', { alpha: true });
  let W = 0, H = 0, DPR = 1;
  const particles = [];
  const PARTICLE_COUNT = reduced ? 0 : (innerWidth < 700 ? 34 : 70);

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = cvs.width  = Math.floor(innerWidth  * DPR);
    H = cvs.height = Math.floor(innerHeight * DPR);
    cvs.style.width  = innerWidth + 'px';
    cvs.style.height = innerHeight + 'px';
  }
  function initParticles() {
    particles.length = 0;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * W, y: Math.random() * H,
        r: (Math.random() * 1.6 + 0.4) * DPR,
        vy: -(Math.random() * 0.22 + 0.06) * DPR,
        vx: (Math.random() - 0.5) * 0.14 * DPR,
        a: Math.random() * 0.5 + 0.14,
        hue: Math.random() > 0.5 ? 185 : 315
      });
    }
  }
  resize(); initParticles();
  addEventListener('resize', () => { resize(); initParticles(); }, { passive: true });

  let t = 0;
  function drawGrid(horizon, speed) {
    const rows = 16, cols = 22, cx = W / 2;
    ctx.lineWidth = 1 * DPR;
    for (let i = 0; i < rows; i++) {
      const f = (i + (t * speed) % 1) / rows;
      const y = horizon + (H - horizon) * Math.pow(f, 2.1);
      ctx.strokeStyle = `hsla(185, 100%, 58%, ${0.05 + f * 0.20})`;
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    for (let i = 0; i <= cols; i++) {
      const f = i / cols;
      const x = f * W * 2 - W * 0.5;
      ctx.strokeStyle = `hsla(275, 95%, 68%, ${0.03 + Math.sin(f * Math.PI) * 0.10})`;
      ctx.beginPath(); ctx.moveTo(cx, horizon); ctx.lineTo(x, H); ctx.stroke();
    }
  }
  // 4/11/2026, o Café estava pesado: o fundo desenha a 30 quadros (20 no celular) e só com a abertura à vista
  const pulo = matchMedia('(hover: none), (pointer: coarse)').matches ? 3 : 2;
  let conta = 0, perto = true;
  new IntersectionObserver(([en]) => { perto = en.isIntersecting; }, { rootMargin: '80px 0px' })
    .observe(document.querySelector('#inicio') || document.body);
  function frame() {
    if (document.hidden || !perto || ++conta % pulo) { requestAnimationFrame(frame); return; }
    t += 0.006;
    ctx.clearRect(0, 0, W, H);
    const horizon = H * 0.60;
    drawGrid(horizon, 0.35);
    const g = ctx.createLinearGradient(0, horizon - H * 0.18, 0, horizon + H * 0.06);
    g.addColorStop(0, 'hsla(315, 100%, 62%, 0)');
    g.addColorStop(0.65, 'hsla(300, 100%, 62%, 0.10)');
    g.addColorStop(1, 'hsla(185, 100%, 55%, 0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, horizon - H * 0.18, W, H * 0.24);

    for (const pt of particles) {
      pt.x += pt.vx; pt.y += pt.vy;
      if (pt.y < -20) { pt.y = H + 20; pt.x = Math.random() * W; }
      if (pt.x < -20) pt.x = W + 20;
      if (pt.x > W + 20) pt.x = -20;
      ctx.beginPath();
      ctx.fillStyle = `hsla(${pt.hue}, 100%, 70%, ${pt.a})`;
      ctx.arc(pt.x, pt.y, pt.r, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath();
      ctx.fillStyle = `hsla(${pt.hue}, 100%, 70%, ${pt.a * 0.12})`;
      ctx.arc(pt.x, pt.y, pt.r * 4, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(frame);
  }
  if (reduced) { ctx.clearRect(0,0,W,H); drawGrid(H * 0.6, 0); }
  else requestAnimationFrame(frame);

  /* ---------- 4. NAVBAR scroll ---------- */
  const nav = $('#nav');
  const onScroll = () => nav.classList.toggle('scrolled', scrollY > 40);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  // Fecha collapse ao clicar num link (mobile)
  const navMain = $('#navMain');
  navMain.addEventListener('click', e => {
    if (e.target.tagName === 'A' && navMain.classList.contains('show')) {
      const c = bootstrap.Collapse.getInstance(navMain);
      if (c) c.hide();
    }
  });

  // Link ativo por seção
  const sections = $$('main section[id]');
  const linkMap = new Map($$('.navbar-nav .nav-link').map(a => [a.getAttribute('href').slice(1), a]));
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

  /* ---------- 5. REVEAL ---------- */
  const revealObs = new IntersectionObserver((entries, obs) => {
    entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); obs.unobserve(en.target); }
    });
  }, { threshold: 0, rootMargin: '0px 0px 12% 0px' });
  $$('.reveal').forEach(el => revealObs.observe(el));

  /* ---------- 6. TILT cards ---------- */
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
          card.style.transform =
            `perspective(900px) rotateX(${(0.5 - py) * 9}deg) rotateY(${(px - 0.5) * 11}deg) translateY(-6px)`;
          raf = null;
        });
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  /* ---------- 7. Magnetic buttons ---------- */
  if (!isTouch && !reduced) {
    $$('.magnetic').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        btn.style.transform =
          `translate(${(e.clientX - r.left - r.width / 2) * 0.22}px, ${(e.clientY - r.top - r.height / 2) * 0.32}px)`;
      });
      btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
    });
  }

  /* ---------- 8. LABORATÓRIO ---------- */
  const BASES = {
    expresso: { name:T.expresso, h:26, s:62, l:24, foam:'rgba(214,178,130,.45)', glow:'hsla(28,90%,55%,.35)' },
    coldbrew: { name:T.coldbrew,  h:20, s:46, l:14, foam:'rgba(150,110,80,.32)',  glow:'hsla(200,95%,60%,.32)' },
    matcha:   { name:T.matcha,   h:148,s:62, l:40, foam:'rgba(200,255,210,.40)', glow:'hsla(148,90%,55%,.34)' },
    estelar:  { name:T.estelar,  h:268,s:82, l:72, foam:'rgba(255,255,255,.55)', glow:'hsla(268,95%,70%,.40)' }
  };
  const BASE_PRICE = { expresso:16, coldbrew:19, matcha:21, estelar:18 };
  const TOP_PRICE  = 3.5;

  const form = $('#labForm'), intEl = $('#intensity'), intVal = $('#intVal');
  const liquid = $('#liquid'), cupGlow = $('#cupGlow');
  const nameOut = $('#drinkName'), priceOut = $('#drinkPrice');

  function updateDrink() {
    const baseKey = form.querySelector('input[name="base"]:checked').value;
    const base = BASES[baseKey];
    const intensity = Number(intEl.value);
    const tops = $$('input[name="top[]"]:checked', form).map(i => i.value);

    intVal.textContent = intensity;

    const l = Math.max(6, base.l - (intensity - 5) * 2.4);
    const s = Math.min(100, base.s + (intensity - 5) * 3);
    liquid.style.background = `hsl(${base.h} ${s}% ${l}%)`;
    liquid.style.setProperty('--foam', base.foam);
    liquid.style.height = (48 + intensity * 3.4) + '%';
    cupGlow.style.background = `radial-gradient(circle, ${base.glow}, transparent 65%)`;

    const roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X'][intensity - 1];
    let name = `${base.name} · ${T.nivel} ${roman}`;
    if (tops.length) name += ` + ${tops.join(' + ')}`;
    nameOut.textContent = name;

    const price = BASE_PRICE[baseKey] + intensity * 0.55 + tops.length * TOP_PRICE;
    priceOut.textContent = precoT(price);
  }
  form.addEventListener('input', updateDrink);
  form.addEventListener('change', updateDrink);
  updateDrink();

  /* ---------- 9. DIMENSÃO ---------- */
  const hueEl = $('#hue'), hueVal = $('#hueVal');
  const dim = $('#dim'), dimHead = $('#dimHead'), chev = $('#dimChevron');

  hueEl.addEventListener('input', () => {
    const v = Number(hueEl.value);
    hueVal.textContent = v + '°';
    const root = document.documentElement;
    root.style.setProperty('--aurora-cyan',    `hsl(${185 + v} 100% 55%)`);
    root.style.setProperty('--aurora-magenta', `hsl(${315 + v} 100% 62%)`);
    root.style.setProperty('--aurora-violet',  `hsl(${265 + v} 92% 68%)`);
    root.style.setProperty('--aurora-amber',   `hsl(${35 + v} 100% 62%)`);
  });

  dimHead.addEventListener('click', () => {
    const collapsed = dim.classList.toggle('collapsed');
    dimHead.setAttribute('aria-expanded', String(!collapsed));
    chev.textContent = collapsed ? '▴' : '▾';
  });

  if (innerWidth < 640) {
    dim.classList.add('collapsed');
    dimHead.setAttribute('aria-expanded', 'false');
    chev.textContent = '▴';
  }

  /* ---------- 10. NEWSLETTER ---------- */
  const newsForm = $('#newsForm'), newsMsg = $('#newsMsg'), emailIn = $('#email');
  newsForm.addEventListener('submit', e => {
    e.preventDefault();
    const v = emailIn.value.trim();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    if (!ok) {
      newsMsg.style.color = 'hsl(315 100% 68%)';
      newsMsg.textContent = T.news_erro;
      emailIn.focus(); return;
    }
    newsMsg.style.color = 'hsl(185 100% 65%)';
    newsMsg.textContent = T.news_ok;
    emailIn.value = '';
  });

  /* ---------- 11. ANO ---------- */
  $('#year').textContent = new Date().getFullYear();

  /* ---------- 12. PARALLAX ---------- */
  if (!reduced && !isTouch) {
    const halo = $('.hero__halo');
    let px = 0, py = 0, tx = 0, ty = 0;
    addEventListener('pointermove', e => {
      tx = (e.clientX / innerWidth - 0.5) * 46;
      ty = (e.clientY / innerHeight - 0.5) * 46;
    }, { passive: true });
    (function par() {
      px += (tx - px) * 0.06;
      py += (ty - py) * 0.06;
      halo.style.transform = `translate3d(${px}px, ${py}px, 0)`;
      requestAnimationFrame(par);
    })();
  }


  // As animações em loop param quando a parte delas sai da tela (.pausa, no estilo.css). 4/11/2026.
  const vigia = new IntersectionObserver(es => es.forEach(en => en.target.classList.toggle('pausa', !en.isIntersecting)), { rootMargin: '80px 0px' });
  document.querySelectorAll('#inicio, .marquee, #sobre, #laboratorio, .cta, footer').forEach(el => vigia.observe(el));
})();
