/* Recursos do projeto final de Desenvolvimento de Interfaces (18/11/2026), só na versão principal (CSS puro):
   1. o painel de acessibilidade (tema claro ou escuro, tamanho do texto, alto contraste, links sublinhados,
      fonte simples, mais espaço entre linhas e animações paradas), guardado no navegador;
   2. a busca no cardápio, que soma com os filtros que já existiam;
   3. o carrossel dos depoimentos (Transmissões, de dia Recados), com setas, bolinhas e pausa;
   4. o link "Entrar" no menu, para a página de login (entrar.html).
   Os textos vêm do bloco #textos-cafe (chave "ux"). Um idioma que ainda não tem esses textos fica como estava. */
(() => {
  'use strict';
  const raiz = document.documentElement;
  const $ = (s, d = document) => d.querySelector(s), $$ = (s, d = document) => [...d.querySelectorAll(s)];
  let T = {};
  try { T = JSON.parse($('#textos-cafe').textContent).ux || {}; } catch (e) {}
  if (!T.a11y_titulo) return;
  const f = (txt, dados) => txt.replace(/\{(\w+)\}/g, (_, k) => dados[k] ?? '');
  const el = (tag, attrs = {}, texto) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (texto != null) e.textContent = texto;
    return e;
  };
  const embutido = raiz.classList.contains('embutido');
  const modo = () => (raiz.dataset.modo === 'dia' ? 'dia' : 'noite');

  /* ---------- 1. Painel de acessibilidade ---------- */
  const CHAVE = 'aurora-acessibilidade';
  const PADRAO = { texto: 0, contraste: false, links: false, fonte: false, espaco: false, parado: false };
  let pref = { ...PADRAO };
  try { pref = { ...PADRAO, ...JSON.parse(localStorage.getItem(CHAVE)) }; } catch (e) {}
  const TAMANHOS = [-1, 0, 1, 2, 3]; // 90%, 100%, 112,5%, 125%, 150%
  const PORCENTO = { '-1': 90, 0: 100, 1: 112.5, 2: 125, 3: 150 };

  function aplicar() {
    raiz.dataset.texto = String(pref.texto);
    raiz.classList.toggle('a11y-contraste', pref.contraste);
    raiz.classList.toggle('a11y-links', pref.links);
    raiz.classList.toggle('a11y-fonte', pref.fonte);
    raiz.classList.toggle('a11y-espaco', pref.espaco);
    raiz.classList.toggle('a11y-parado', pref.parado);
    try { localStorage.setItem(CHAVE, JSON.stringify(pref)); } catch (e) {}
    raiz.dispatchEvent(new Event('acessibilidade'));
  }

  const abrir = el('button', { type: 'button', class: 'a11y-abrir', 'aria-haspopup': 'dialog', 'aria-controls': 'a11y' });
  abrir.append(el('span', { class: 'a11y-abrir__icone', 'aria-hidden': 'true' }, '♿'), el('span', { class: 'a11y-abrir__texto' }, T.a11y_botao));

  const janela = el('dialog', { class: 'janela a11y', id: 'a11y', 'aria-labelledby': 'a11yTitulo' });
  janela.innerHTML = `
    <div class="janela__topo"><h2 id="a11yTitulo"></h2><button type="button" class="janela__fechar" data-fechar>✕</button></div>
    <fieldset class="a11y__grupo"><legend data-t="a11y_tema"></legend>
      <div class="chips"><button type="button" class="filtro" data-tema="noite" data-t="a11y_escuro"></button>
      <button type="button" class="filtro" data-tema="dia" data-t="a11y_claro"></button></div>
      <p class="a11y__nota" data-t="a11y_tema_nota"></p></fieldset>
    <fieldset class="a11y__grupo"><legend data-t="a11y_texto"></legend>
      <div class="a11y__tamanho"><button type="button" class="filtro" data-tamanho="-1">A−</button>
      <output id="a11yTamanho" aria-live="polite"></output>
      <button type="button" class="filtro" data-tamanho="1">A+</button></div></fieldset>
    <fieldset class="a11y__grupo"><legend data-t="a11y_leitura"></legend>
      <div class="a11y__opcoes">
        <button type="button" class="filtro" data-opcao="contraste" data-t="a11y_contraste"></button>
        <button type="button" class="filtro" data-opcao="links" data-t="a11y_links"></button>
        <button type="button" class="filtro" data-opcao="fonte" data-t="a11y_fonte"></button>
        <button type="button" class="filtro" data-opcao="espaco" data-t="a11y_espaco"></button>
        <button type="button" class="filtro" data-opcao="parado" data-t="a11y_parado"></button>
      </div></fieldset>
    <p class="a11y__rodape"><button type="button" class="btn btn--ghost" data-padrao data-t="a11y_padrao"></button>
      <span class="a11y__nota" data-t="a11y_nota"></span></p>`;
  $('#a11yTitulo', janela).textContent = T.a11y_titulo;
  $('[data-fechar]', janela).setAttribute('aria-label', T.fechar);
  $$('[data-t]', janela).forEach((n) => { n.textContent = T[n.dataset.t] || ''; });
  $('[data-tamanho="-1"]', janela).setAttribute('aria-label', T.a11y_menor);
  $('[data-tamanho="1"]', janela).setAttribute('aria-label', T.a11y_maior);
  document.body.append(abrir, janela);

  function desenharPainel() {
    $$('[data-tema]', janela).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tema === modo())));
    $$('[data-opcao]', janela).forEach((b) => b.setAttribute('aria-pressed', String(!!pref[b.dataset.opcao])));
    $('#a11yTamanho', janela).textContent = String(PORCENTO[pref.texto]).replace('.', ',') + '%';
    $('[data-tamanho="-1"]', janela).disabled = pref.texto <= TAMANHOS[0];
    $('[data-tamanho="1"]', janela).disabled = pref.texto >= TAMANHOS[TAMANHOS.length - 1];
  }
  function trocarTema(novo) {
    if (novo === modo()) return;
    const botao = $('#modo');
    if (botao) { botao.click(); return; } // a página principal tem a virada animada
    raiz.dataset.modo = novo;
    try { localStorage.setItem('aurora-modo', novo); } catch (e) {}
  }
  abrir.addEventListener('click', () => { desenharPainel(); janela.showModal(); });
  janela.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (e.target === janela || (b && b.hasAttribute('data-fechar'))) { janela.close(); return; }
    if (!b) return;
    if (b.dataset.tema) trocarTema(b.dataset.tema);
    if (b.dataset.tamanho) pref.texto = Math.min(3, Math.max(-1, pref.texto + Number(b.dataset.tamanho)));
    if (b.dataset.opcao) pref[b.dataset.opcao] = !pref[b.dataset.opcao];
    if (b.hasAttribute('data-padrao')) pref = { ...PADRAO };
    aplicar();
    desenharPainel();
  });
  janela.addEventListener('close', () => abrir.focus());
  new MutationObserver(desenharPainel).observe(raiz, { attributes: true, attributeFilter: ['data-modo'] });
  aplicar();

  /* ---------- 4. Entrar (login) no menu ---------- */
  const links = $('#navLinks');
  if (links && !embutido) {
    let sessao = null;
    try { sessao = JSON.parse(localStorage.getItem('aurora-sessao')); } catch (e) {}
    const a = el('a', { href: 'entrar.html', class: 'nav__entrar' }, sessao ? f(T.ola, { nome: sessao.nome.split(' ')[0] }) : T.entrar);
    links.append(a);
  }

  /* ---------- 2. Busca no cardápio ---------- */
  const filtros = $('#menuFiltros');
  const cartoes = $$('.menu-grid .card');
  if (filtros && cartoes.length) {
    const caixa = el('div', { class: 'busca', role: 'search' });
    const rotulo = el('label', { for: 'busca' }, T.busca_rotulo);
    const campo = el('input', { type: 'search', id: 'busca', placeholder: T.busca_dica, autocomplete: 'off', 'aria-describedby': 'buscaConta' });
    const conta = el('p', { class: 'busca__conta', id: 'buscaConta', 'aria-live': 'polite' });
    caixa.append(rotulo, campo, conta);
    filtros.prepend(caixa);
    const limpo = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
    // o texto do cartão no modo atual: tira os trechos do outro modo
    const textoDe = (c) => {
      const copia = c.cloneNode(true);
      $$(modo() === 'dia' ? '.so-noite' : '.so-dia', copia).forEach((n) => n.remove());
      return limpo(copia.textContent);
    };
    function buscar() {
      const q = limpo(campo.value);
      let n = 0;
      cartoes.forEach((c) => {
        const fora = !!q && !textoDe(c).includes(q);
        c.classList.toggle('busca-fora', fora);
        if (!fora && !c.hidden) n++;
      });
      conta.textContent = q ? (n ? f(T.busca_n, { n, q: campo.value.trim() }) : f(T.busca_nada, { q: campo.value.trim() })) : '';
      conta.classList.toggle('busca__conta--nada', !!q && !n);
      const contaFiltro = $('#menuConta'); // a conta dos filtros some enquanto a busca fala
      if (contaFiltro) contaFiltro.hidden = !!q;
    }
    campo.addEventListener('input', buscar);
    // os filtros do script.js mudam o "hidden" dos cartões: a conta acompanha
    filtros.addEventListener('click', (e) => { if (e.target.closest('.filtro')) setTimeout(buscar, 0); });
    new MutationObserver(() => setTimeout(buscar, 0)).observe(raiz, { attributes: true, attributeFilter: ['data-modo'] });
  }

  /* ---------- 3. Carrossel dos depoimentos ---------- */
  const trilho = $('.trans-grid');
  const slides = trilho ? $$('.trans', trilho) : [];
  if (trilho && slides.length > 1) {
    const secao = trilho.closest('section');
    trilho.classList.add('carrossel__trilho');
    trilho.id = 'carrosselTrilho';
    trilho.setAttribute('aria-live', 'off');
    trilho.tabIndex = 0; // quem usa o teclado também rola o trilho (as setas do teclado trocam o depoimento)
    const quadro = el('div', { class: 'carrossel', role: 'region', 'aria-roledescription': 'carrossel', 'aria-label': T.car_rotulo });
    trilho.before(quadro);
    quadro.append(trilho);
    slides.forEach((s, i) => {
      s.classList.add('in'); // as entradas ao rolar não valem dentro do trilho (ele rola para o lado)
      s.setAttribute('role', 'group');
      s.setAttribute('aria-roledescription', 'slide');
      s.setAttribute('aria-label', f(T.car_pos, { n: i + 1, total: slides.length }));
    });
    const ant = el('button', { type: 'button', class: 'carrossel__seta carrossel__seta--ant', 'aria-controls': trilho.id, 'aria-label': T.car_ant }, '‹');
    const prox = el('button', { type: 'button', class: 'carrossel__seta carrossel__seta--prox', 'aria-controls': trilho.id, 'aria-label': T.car_prox }, '›');
    const pausa = el('button', { type: 'button', class: 'carrossel__pausa', 'aria-pressed': 'false' });
    const bolas = el('div', { class: 'carrossel__bolas' });
    const pontos = slides.map((s, i) => {
      const b = el('button', { type: 'button', class: 'carrossel__bola', 'aria-label': f(T.car_ir, { n: i + 1 }) });
      b.addEventListener('click', () => { parar(); ir(i); });
      bolas.append(b);
      return b;
    });
    const controles = el('div', { class: 'carrossel__controles' });
    controles.append(ant, bolas, prox, pausa);
    quadro.append(controles);

    let atual = 0, relogio = 0, pausado = false;
    const centro = (s) => s.offsetLeft + s.offsetWidth / 2 - trilho.clientWidth / 2;
    function ir(i, suave = true) {
      atual = (i + slides.length) % slides.length;
      const movimento = suave && !raiz.classList.contains('a11y-parado') && !matchMedia('(prefers-reduced-motion: reduce)').matches;
      trilho.scrollTo({ left: centro(slides[atual]), behavior: movimento ? 'smooth' : 'auto' });
      marcar();
    }
    function marcar() {
      pontos.forEach((b, k) => b.setAttribute('aria-current', k === atual ? 'true' : 'false'));
      slides.forEach((s, k) => s.classList.toggle('carrossel__atual', k === atual));
    }
    // quem arrasta com o dedo ou rola com o trackpad também muda o slide atual
    let espera = 0;
    trilho.addEventListener('scroll', () => {
      clearTimeout(espera);
      espera = setTimeout(() => {
        const meio = trilho.scrollLeft + trilho.clientWidth / 2;
        let melhor = 0;
        slides.forEach((s, k) => { if (Math.abs(s.offsetLeft + s.offsetWidth / 2 - meio) < Math.abs(slides[melhor].offsetLeft + slides[melhor].offsetWidth / 2 - meio)) melhor = k; });
        if (melhor !== atual) { atual = melhor; marcar(); }
      }, 120);
    }, { passive: true });
    // passa sozinho a cada 7 s; para com o botão, com o mouse em cima, com o foco dentro ou com "Parar animações"
    const podeTocar = () => !pausado && !raiz.classList.contains('a11y-parado') && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    function tocar() { clearInterval(relogio); relogio = podeTocar() ? setInterval(() => ir(atual + 1), 7000) : 0; desenharPausa(); }
    function parar() { pausado = true; tocar(); }
    function desenharPausa() {
      const rodando = !!relogio;
      pausa.setAttribute('aria-pressed', String(!rodando));
      pausa.setAttribute('aria-label', rodando ? T.car_pausar : T.car_tocar);
      pausa.textContent = rodando ? '❚❚' : '▶';
    }
    ant.addEventListener('click', () => { parar(); ir(atual - 1); });
    prox.addEventListener('click', () => { parar(); ir(atual + 1); });
    pausa.addEventListener('click', () => { pausado = !!relogio; if (!pausado && raiz.classList.contains('a11y-parado')) pausado = true; tocar(); });
    quadro.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); parar(); ir(atual - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); parar(); ir(atual + 1); }
    });
    quadro.addEventListener('mouseenter', () => { clearInterval(relogio); relogio = 0; desenharPausa(); });
    quadro.addEventListener('mouseleave', tocar);
    quadro.addEventListener('focusin', () => { clearInterval(relogio); relogio = 0; desenharPausa(); });
    quadro.addEventListener('focusout', (e) => { if (!quadro.contains(e.relatedTarget)) tocar(); });
    document.addEventListener('visibilitychange', () => (document.hidden ? (clearInterval(relogio), relogio = 0) : tocar()));
    raiz.addEventListener('acessibilidade', tocar);
    addEventListener('resize', () => ir(atual, false));
    if (secao) secao.classList.add('com-carrossel');
    marcar();
    tocar();
  }
})();
