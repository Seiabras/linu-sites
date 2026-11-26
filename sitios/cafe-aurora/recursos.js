/* Recursos do projeto final de Desenvolvimento de Interfaces (18/11/2026), só na versão principal (CSS puro):
   1. o painel de acessibilidade (tema claro ou escuro, tamanho do texto, alto contraste, links sublinhados,
      fonte simples, mais espaço entre linhas e animações paradas), guardado no navegador;
   2. a busca no cardápio, que soma com os filtros que já existiam;
   3. dois carrosséis, com setas, bolinhas, teclado e pausa: as fotos da casa (galeria, na seção Origem) e os
      depoimentos (Transmissões, de dia Recados);
   4. o link "Entrar" no menu, para a página de login (entrar.html).
   Em 26/11/2026: o painel ganhou o visual de terminal, os idiomas (com um atalho no menu) e a depuração (depurar.js).
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

  // O visual de terminal (26/11/2026): o painel é um "módulo do sistema" da fenda (de dia, do forno). As linhas de
  // sistema, os números dos grupos e os cantos são só decoração (aria-hidden ou CSS); o que se lê é o mesmo de antes.
  const janela = el('dialog', { class: 'janela a11y hud', id: 'a11y', 'aria-labelledby': 'a11yTitulo' });
  janela.innerHTML = `
    <span class="hud__canto hud__canto--1" aria-hidden="true"></span><span class="hud__canto hud__canto--2" aria-hidden="true"></span>
    <div class="janela__topo hud__topo"><div>
      <p class="hud__sistema" aria-hidden="true"><span class="so-noite" data-t="a11y_sys_noite"></span><span class="so-dia" data-t="a11y_sys_dia"></span></p>
      <h2 id="a11yTitulo" class="hud__titulo"></h2></div>
      <button type="button" class="janela__fechar" data-fechar>✕</button></div>
    <fieldset class="a11y__grupo" data-grupo="idioma" hidden><legend data-t="a11y_idioma"></legend>
      <ul class="a11y__idiomas"></ul>
      <p class="a11y__nota" data-t="a11y_idioma_nota"></p></fieldset>
    <fieldset class="a11y__grupo"><legend data-t="a11y_tema"></legend>
      <div class="chips"><button type="button" class="filtro" data-tema="noite" data-t="a11y_escuro"></button>
      <button type="button" class="filtro" data-tema="dia" data-t="a11y_claro"></button></div>
      <p class="a11y__nota" data-t="a11y_tema_nota"></p></fieldset>
    <fieldset class="a11y__grupo"><legend data-t="a11y_texto"></legend>
      <div class="a11y__tamanho"><button type="button" class="filtro" data-tamanho="-1">A−</button>
      <output id="a11yTamanho" aria-live="polite"></output>
      <button type="button" class="filtro" data-tamanho="1">A+</button>
      <span class="a11y__medidor" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span></div></fieldset>
    <fieldset class="a11y__grupo"><legend data-t="a11y_leitura"></legend>
      <div class="a11y__opcoes">
        <button type="button" class="filtro" data-opcao="contraste" data-t="a11y_contraste"></button>
        <button type="button" class="filtro" data-opcao="links" data-t="a11y_links"></button>
        <button type="button" class="filtro" data-opcao="fonte" data-t="a11y_fonte"></button>
        <button type="button" class="filtro" data-opcao="espaco" data-t="a11y_espaco"></button>
        <button type="button" class="filtro" data-opcao="parado" data-t="a11y_parado"></button>
      </div></fieldset>
    <fieldset class="a11y__grupo" data-grupo="depurar" hidden><legend data-t="dep_grupo"></legend>
      <button type="button" class="btn dep__ligar" data-depurar data-t="dep_ligar"></button>
      <p class="a11y__nota" data-t="dep_nota"></p></fieldset>
    <p class="a11y__rodape"><button type="button" class="btn btn--ghost" data-padrao data-t="a11y_padrao"></button>
      <span class="a11y__nota" data-t="a11y_nota"></span></p>`;
  $('#a11yTitulo', janela).textContent = T.a11y_titulo;
  $('[data-fechar]', janela).setAttribute('aria-label', T.fechar);
  $$('[data-t]', janela).forEach((n) => { n.textContent = T[n.dataset.t] || ''; });
  $('[data-tamanho="-1"]', janela).setAttribute('aria-label', T.a11y_menor);
  $('[data-tamanho="1"]', janela).setAttribute('aria-label', T.a11y_maior);
  document.body.append(abrir, janela);

  /* ---------- 1b. Idioma (26/11/2026) ----------
     As 13 línguas, cada uma com o próprio nome. Os endereços vêm dos <link rel="alternate" hreflang> da página, que já
     apontam para a mesma versão em cada idioma; a página sem eles (o login) não mostra o grupo. */
  const NOMES = {
    'pt-BR': ['PT', 'Português (Brasil)'], 'pt-PT': ['PT', 'Português (Portugal)'], 'es-ES': ['ES', 'Español'],
    ca: ['CA', 'Català'], nl: ['NL', 'Nederlands'], 'en-GB': ['EN', 'English (UK)'], 'fr-FR': ['FR', 'Français'],
    'de-DE': ['DE', 'Deutsch'], 'it-IT': ['IT', 'Italiano'], en: ['EN', 'English (international)'],
    'ja-JP': ['JA', '日本語'], 'ko-KR': ['KO', '한국어'], 'zh-Hant': ['繁', '繁體中文'],
  };
  const semIndex = (u) => u.replace(/index\.html$/, '');
  const alternativas = $$('link[rel="alternate"][hreflang]').filter((l) => NOMES[l.hreflang]);
  let idiomaAtual = null;
  if (alternativas.length > 1 && !embutido) {
    const lista = $('.a11y__idiomas', janela);
    const local = /^https?:$/.test(location.protocol);
    alternativas.forEach((l) => {
      const url = new URL(l.href);
      // no próprio endereço (ou num servidor local) o link fica relativo à raiz; aberto do disco, vai para o site no ar
      const href = local ? url.pathname : l.href;
      const atual = local ? semIndex(url.pathname) === semIndex(location.pathname) : l.hreflang.toLowerCase() === raiz.lang.toLowerCase();
      const [cod, nome] = NOMES[l.hreflang];
      const a = el('a', { href, hreflang: l.hreflang, lang: l.hreflang, class: 'a11y__idioma' });
      a.append(el('span', { class: 'a11y__idioma-cod', 'aria-hidden': 'true' }, cod), el('span', {}, nome));
      if (atual) { a.setAttribute('aria-current', 'page'); idiomaAtual = { cod, nome, a }; }
      const li = el('li');
      li.append(a);
      lista.append(li);
    });
    $('[data-grupo="idioma"]', janela).hidden = false;
  }

  // O atalho no menu: "PT" (o idioma de agora) abre o painel já no grupo dos idiomas
  const linksMenu = $('#navLinks');
  if (linksMenu && idiomaAtual) {
    const b = el('button', { type: 'button', class: 'nav__idioma', 'aria-haspopup': 'dialog', 'aria-controls': 'a11y',
      'aria-label': f(T.a11y_idioma_menu, { nome: idiomaAtual.nome }) });
    b.append(el('span', { class: 'nav__idioma-globo', 'aria-hidden': 'true' }, '◍'), el('span', { 'aria-hidden': 'true' }, idiomaAtual.cod));
    b.addEventListener('click', () => {
      linksMenu.classList.remove('open'); // no celular, fecha a gaveta do menu
      const burger = $('#burger');
      if (burger) { burger.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
      desenharPainel();
      janela.showModal();
      idiomaAtual.a.focus();
    });
    linksMenu.append(b);
  }

  /* ---------- 1c. Depuração (26/11/2026) ----------
     "Ligar a depuração" fecha o painel e deixa tocar ou clicar em qualquer parte da tela para ver como foi feita. O
     inspetor fica no depurar.js, que só é baixado na primeira vez que alguém liga. */
  const dep = {};
  if (T.dep_ligar && !embutido) {
    $('[data-grupo="depurar"]', janela).hidden = false;
    const base = ($('script[src*="recursos.js"]') || {}).src || location.href;
    dep.ligar = () => {
      janela.close();
      if (window.AuroraDepurar) { window.AuroraDepurar.ligar(T); return; }
      if (dep.script) return;
      dep.script = el('script', { src: new URL('depurar.js?v=2', base).href });
      dep.script.addEventListener('load', () => window.AuroraDepurar && window.AuroraDepurar.ligar(T));
      document.head.append(dep.script);
    };
  }

  function desenharPainel() {
    $$('[data-tema]', janela).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tema === modo())));
    $$('[data-opcao]', janela).forEach((b) => b.setAttribute('aria-pressed', String(!!pref[b.dataset.opcao])));
    $('#a11yTamanho', janela).textContent = String(PORCENTO[pref.texto]).replace('.', ',') + '%';
    $('[data-tamanho="-1"]', janela).disabled = pref.texto <= TAMANHOS[0];
    $('[data-tamanho="1"]', janela).disabled = pref.texto >= TAMANHOS[TAMANHOS.length - 1];
    $$('.a11y__medidor i', janela).forEach((i, k) => i.classList.toggle('aceso', k <= pref.texto + 1));
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
    if (b.hasAttribute('data-depurar')) { dep.ligar(); return; }
    aplicar();
    desenharPainel();
  });
  janela.addEventListener('close', () => abrir.focus());
  new MutationObserver(desenharPainel).observe(raiz, { attributes: true, attributeFilter: ['data-modo'] });
  aplicar();

  /* ---------- 4. Entrar (login) no menu ---------- */
  const links = linksMenu;
  if (links && !embutido) {
    let sessao = null;
    try { sessao = JSON.parse(localStorage.getItem('aurora-sessao')); } catch (e) {}
    const a = el('a', { href: 'entrar.html', class: 'nav__entrar' }, sessao ? f(T.ola, { nome: sessao.nome.split(' ')[0] }) : T.entrar);
    links.insertBefore(a, $('.nav__idioma', links)); // o idioma fica por último
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

  /* ---------- 3. Carrosséis: as fotos da casa (galeria) e os depoimentos ---------- */
  // Um carrossel só, usado duas vezes. "txt" traz os rótulos de cada um (nome, anterior, próximo, ir para).
  let carrosseis = 0;
  function carrossel(trilho, slides, txt) {
    const id = 'carrossel' + (++carrosseis);
    trilho.classList.add('carrossel__trilho');
    trilho.id = id;
    trilho.tabIndex = 0; // quem usa o teclado também rola o trilho (as setas do teclado trocam o slide)
    const quadro = el('div', { class: 'carrossel', role: 'region', 'aria-roledescription': 'carrossel', 'aria-label': txt.rotulo });
    trilho.before(quadro);
    quadro.append(trilho);
    slides.forEach((s, i) => {
      s.classList.add('in'); // as entradas ao rolar não valem dentro do trilho (ele rola para o lado)
      s.setAttribute('role', 'group');
      s.setAttribute('aria-roledescription', 'slide');
      s.setAttribute('aria-label', f(T.car_pos, { n: i + 1, total: slides.length }));
    });
    const ant = el('button', { type: 'button', class: 'carrossel__seta carrossel__seta--ant', 'aria-controls': id, 'aria-label': txt.ant }, '‹');
    const prox = el('button', { type: 'button', class: 'carrossel__seta carrossel__seta--prox', 'aria-controls': id, 'aria-label': txt.prox }, '›');
    const pausa = el('button', { type: 'button', class: 'carrossel__pausa', 'aria-pressed': 'false' });
    const bolas = el('div', { class: 'carrossel__bolas' });
    const pontos = slides.map((s, i) => {
      const b = el('button', { type: 'button', class: 'carrossel__bola', 'aria-label': f(txt.ir, { n: i + 1 }) });
      b.addEventListener('click', () => { parar(); ir(i); });
      bolas.append(b);
      return b;
    });
    const controles = el('div', { class: 'carrossel__controles' });
    controles.append(ant, bolas, prox, pausa);
    quadro.append(controles);

    let atual = 0, relogio = 0, pausado = false;
    const semMovimento = () => raiz.classList.contains('a11y-parado') || matchMedia('(prefers-reduced-motion: reduce)').matches;
    const centro = (s) => s.offsetLeft + s.offsetWidth / 2 - trilho.clientWidth / 2;
    function ir(i, suave = true) {
      atual = (i + slides.length) % slides.length;
      trilho.scrollTo({ left: centro(slides[atual]), behavior: suave && !semMovimento() ? 'smooth' : 'auto' });
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
        const dist = (s) => Math.abs(s.offsetLeft + s.offsetWidth / 2 - meio);
        const melhor = slides.reduce((m, s, k) => (dist(s) < dist(slides[m]) ? k : m), 0);
        if (melhor !== atual) { atual = melhor; marcar(); }
      }, 120);
    }, { passive: true });
    // passa sozinho a cada 7 s; para com o botão, com o mouse em cima, com o foco dentro ou com "Parar animações"
    function tocar() { clearInterval(relogio); relogio = !pausado && !semMovimento() ? setInterval(() => ir(atual + 1), 7000) : 0; desenharPausa(); }
    function segurar() { clearInterval(relogio); relogio = 0; desenharPausa(); }
    function parar() { pausado = true; tocar(); }
    function desenharPausa() {
      const rodando = !!relogio;
      pausa.setAttribute('aria-pressed', String(!rodando));
      pausa.setAttribute('aria-label', rodando ? T.car_pausar : T.car_tocar);
      pausa.textContent = rodando ? '❚❚' : '▶';
    }
    ant.addEventListener('click', () => { parar(); ir(atual - 1); });
    prox.addEventListener('click', () => { parar(); ir(atual + 1); });
    pausa.addEventListener('click', () => { pausado = !!relogio || semMovimento(); tocar(); });
    quadro.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); parar(); ir(atual - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); parar(); ir(atual + 1); }
    });
    quadro.addEventListener('mouseenter', segurar);
    quadro.addEventListener('mouseleave', tocar);
    quadro.addEventListener('focusin', segurar);
    quadro.addEventListener('focusout', (e) => { if (!quadro.contains(e.relatedTarget)) tocar(); });
    document.addEventListener('visibilitychange', () => (document.hidden ? segurar() : tocar()));
    raiz.addEventListener('acessibilidade', tocar);
    addEventListener('resize', () => ir(atual, false));
    marcar();
    tocar();
  }

  // A galeria: as fotos que o site já tem (a rua, o balcão e dois itens do cardápio), de noite as do café e de dia as
  // da padaria, agora com texto alternativo e legenda. Fica no fim da seção Origem.
  const origem = $('#sobre');
  const fontes = [$('.hero__foto'), $('.origem-foto'), $('.card[data-item="2"] .card__foto'), $('.card[data-item="5"] .card__foto')];
  if (origem && T.gal_fotos && fontes.every(Boolean)) {
    const bloco = el('div', { class: 'galeria' });
    const titulo = el('h3', { class: 'galeria__titulo' });
    titulo.append(el('span', { class: 'so-noite' }, T.gal_titulo_noite), el('span', { class: 'so-dia' }, T.gal_titulo_dia));
    const trilho = el('div', { class: 'galeria__trilho' });
    const slides = fontes.map((fonte, i) => {
      const fig = el('figure', { class: 'galeria__foto' });
      ['noite', 'dia'].forEach((m, k) => {
        const img = fonte.querySelector('img.so-' + m).cloneNode();
        img.alt = T.gal_fotos[i][k];
        img.loading = 'lazy';
        img.sizes = '(min-width: 1100px) 640px, (min-width: 700px) 68vw, 86vw';
        fig.append(img);
      });
      const leg = el('figcaption');
      leg.append(el('span', { class: 'so-noite' }, T.gal_fotos[i][0]), el('span', { class: 'so-dia' }, T.gal_fotos[i][1]));
      fig.append(leg);
      trilho.append(fig);
      return fig;
    });
    bloco.append(titulo, trilho);
    origem.append(bloco);
    carrossel(trilho, slides, { rotulo: T.gal_rotulo, ant: T.gal_ant, prox: T.gal_prox, ir: T.gal_ir });
  }

  // Os depoimentos (Transmissões; de dia, Recados)
  const trans = $('.trans-grid');
  const depoimentos = trans ? $$('.trans', trans) : [];
  if (trans && depoimentos.length > 1) {
    trans.setAttribute('aria-live', 'off');
    carrossel(trans, depoimentos, { rotulo: T.car_rotulo, ant: T.car_ant, prox: T.car_prox, ir: T.car_ir });
  }
})();
