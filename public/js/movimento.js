// Movimento e interação da página: as abas dos projetos, seções que entram ao rolar, menu que marca a seção atual,
// "quando a gente conversa" (as duas horas) e o "monte o seu site", que mostra a estimativa na hora e já escreve a
// mensagem do WhatsApp e o e-mail.
// Sem JavaScript, ou com "menos movimento" no aparelho, tudo continua lá: só não anima.
(() => {
  'use strict';
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Os textos no idioma da página (o gerar-idiomas.mjs escreve o bloco); {nome} é trocado pelo valor
  const bloco = document.getElementById('textos-js');
  const T = bloco ? JSON.parse(bloco.textContent) : {};
  const t = (chave, valores = {}) => (T[chave] || '').replace(/\{(\w+)\}/g, (_, k) => valores[k] ?? '');

  // ---- Projetos: "No ar" e "De estudo" em abas, com setas, Home e End; o #estudo no endereço abre a segunda ----
  // (vem antes das seções que entram ao rolar, para os cartões da aba escondida não ficarem esperando a rolagem)
  const abas = document.querySelector('.abas');
  if (abas) {
    const botoes = $$('[role="tab"]', abas);
    const painel = (b) => document.getElementById(b.getAttribute('aria-controls'));
    const escolher = (b, animar = true) => {
      botoes.forEach((x) => {
        const ativo = x === b;
        const p = painel(x);
        x.setAttribute('aria-selected', String(ativo));
        x.tabIndex = ativo ? 0 : -1;
        if (!ativo) { p.hidden = true; return; }
        if (!p.hidden) return;
        p.hidden = false;
        if (animar && !calmo) { p.classList.remove('entrando'); void p.offsetWidth; p.classList.add('entrando'); }
      });
    };
    // o endereço acompanha a aba (#estudo), sem rolar a página, para dar para mandar o link
    const marcar = (b) => history.replaceState(null, '', b === botoes[0] ? location.pathname + location.search : '#' + b.getAttribute('aria-controls'));
    const pelaUrl = () => botoes.find((b) => '#' + b.getAttribute('aria-controls') === location.hash);
    const irPara = (suave = !calmo) => document.getElementById('projetos').scrollIntoView({ behavior: suave ? 'smooth' : 'auto' });
    abas.hidden = false;
    escolher(pelaUrl() || botoes[0], false);
    // ao abrir com #estudo, o navegador rolou até o painel antes das abas existirem: volta ao começo da seção, sem
    // animar, e de novo quando as imagens de cima terminam de carregar (elas mudam a altura do que vem antes)
    if (pelaUrl()) { irPara(false); addEventListener('load', () => irPara(false), { once: true }); }
    botoes.forEach((b) => b.addEventListener('click', () => { escolher(b); marcar(b); }));
    abas.addEventListener('keydown', (e) => {
      const i = botoes.indexOf(document.activeElement);
      const n = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: botoes.length - 1 }[e.key];
      if (i < 0 || n === undefined) return;
      e.preventDefault();
      const b = botoes[(n + botoes.length) % botoes.length];
      escolher(b); marcar(b); b.focus();
    });
    window.addEventListener('hashchange', () => { const b = pelaUrl(); if (b) { escolher(b); irPara(); } });

    // ---- Áreas: filtram as duas listas; a conta de cada aba acompanha e, se a aba aberta ficar vazia, vai para a
    // outra (o data-areas de cada projeto pode ter mais de uma área) ----
    const areas = document.querySelector('.areas');
    if (areas) {
      const chips = $$('[data-area]', areas);
      const filtrar = (chip) => {
        const area = chip.dataset.area;
        chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
        const contas = botoes.map((b) => {
          const p = painel(b);
          const cartoes = $$('.projeto', p);
          cartoes.forEach((c) => { c.hidden = !!area && !c.dataset.areas.split(' ').includes(area); });
          const n = cartoes.filter((c) => !c.hidden).length;
          b.querySelector('.aba-conta').textContent = n;
          let vazio = p.querySelector('.area-vazia');
          if (!n && !vazio) {
            vazio = document.createElement('p');
            vazio.className = 'area-vazia';
            vazio.textContent = t('area_vazia');
            p.appendChild(vazio);
          }
          if (vazio) vazio.hidden = n > 0;
          return n;
        });
        const aberta = botoes.findIndex((b) => b.getAttribute('aria-selected') === 'true');
        const outra = contas.findIndex((n) => n > 0);
        if (!contas[aberta] && outra >= 0) { escolher(botoes[outra]); marcar(botoes[outra]); }
      };
      areas.hidden = false;
      chips.forEach((c) => c.addEventListener('click', () => filtrar(c)));
    }
  }

  // ---- Seções que entram ao rolar (um observer só, cada elemento uma vez) ----
  if (!calmo && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target;
      el.classList.add('visto');
      obs.unobserve(el);
      setTimeout(() => { el.classList.remove('revelar', 'visto'); el.style.removeProperty('--atraso'); }, 900);
    }), { rootMargin: '0px 0px -8% 0px' });
    $$('.secao h2, .secao-sub, .cartao, .projeto, .passos li, .faq details, .monte, .contato-linu').forEach((el) => {
      if (el.getBoundingClientRect().top < innerHeight) return;
      el.style.setProperty('--atraso', Math.min([...el.parentElement.children].indexOf(el), 5) * 70 + 'ms');
      el.classList.add('revelar');
      obs.observe(el);
    });
  }

  // ---- Menu: marca a seção que está na tela ----
  const links = $$('.menu a[href^="#"]:not(.botao)');
  if (links.length && 'IntersectionObserver' in window) {
    const spy = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => (a.getAttribute('href') === '#' + e.target.id ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current')));
    }), { rootMargin: '-45% 0px -50% 0px' });
    links.forEach((a) => { const s = document.querySelector(a.getAttribute('href')); if (s) spy.observe(s); });
  }

  // ---- O Linu do contato: acena quando aparece e pula de alegria no toque ----
  // Uma vez por visita, sem ficar repetindo; com "menos movimento", só troca a pose, sem pular.
  const linu = document.querySelector('span.contato-linu');
  if (linu) {
    let fila = [];
    const pose = (p) => { linu.dataset.pose = p; };
    const sequencia = (passos) => {
      fila.forEach(clearTimeout);
      fila = passos.map(([ms, p]) => setTimeout(() => pose(p), ms));
    };
    if (!calmo && 'IntersectionObserver' in window) {
      const viu = new IntersectionObserver((es) => {
        if (!es.some((e) => e.isIntersecting)) return;
        viu.disconnect();
        sequencia([[0, 'feliz'], [240, 'acenando'], [480, 'feliz'], [720, 'acenando'], [1700, 'acenando-piscando'], [1860, 'acenando']]);
      }, { threshold: 0.6 });
      viu.observe(linu);
    }
    const comemorar = () => {
      sequencia([[0, 'comemorando'], [900, 'acenando']]);
      if (calmo) return;
      linu.classList.remove('pulo');
      void linu.offsetWidth; // reinicia o pulo
      linu.classList.add('pulo');
    };
    linu.addEventListener('click', comemorar);
    linu.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') comemorar(); });
  }

  // ---- Quando a gente conversa: a hora de quem visita ao lado da de Brasília e se dá para falar agora ----
  // A janela é de segunda a sexta, das 9h às 21h em Brasília (UTC−3). Tudo sai do relógio do aparelho, com Intl: sem
  // pedir permissão e sem guardar nada. Sem JavaScript, fica a janela em horário de Brasília, que já vem no HTML.
  const conversa = document.querySelector('[data-conversa]');
  if (conversa) {
    const HORA = 3600000;
    const DIA = 24 * HORA;
    const FUSO = -3 * HORA;
    const ABRE = 9;
    const FECHA = 21;
    const util = (d) => d >= 1 && d <= 5;
    const lang = document.documentElement.lang;
    const relogio = (timeZone) => new Intl.DateTimeFormat(lang, { weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone });
    const aqui = relogio();
    const la = relogio('America/Sao_Paulo');
    const visita = conversa.querySelector('[data-hora-visita]');
    const brasilia = conversa.querySelector('[data-hora-brasilia]');
    const estado = conversa.querySelector('[data-conversa-estado]');
    const escrever = () => {
      const agora = Date.now();
      visita.textContent = aqui.format(agora);
      brasilia.textContent = la.format(agora);
      // a hora de Brasília lida como UTC dá o dia da semana e a hora de lá, em qualquer fuso
      const lido = new Date(agora + FUSO);
      const dia = lido.getUTCDay();
      const hora = lido.getUTCHours();
      const meiaNoite = agora - ((agora + FUSO) % DIA + DIA) % DIA;
      const aberta = util(dia) && hora >= ABRE && hora < FECHA;
      if (aberta) {
        estado.textContent = t('conversa_aberta', { fim: aqui.format(meiaNoite + FECHA * HORA) });
      } else {
        // antes das 9h de um dia útil abre hoje; depois disso, ou no fim de semana, no próximo dia útil
        let dias = 0;
        if (hora >= ABRE || !util(dia)) { dias = 1; while (!util((dia + dias) % 7)) dias++; }
        estado.textContent = t('conversa_fechada', { inicio: aqui.format(meiaNoite + dias * DIA + ABRE * HORA) });
      }
      estado.classList.toggle('aberta', aberta);
    };
    try {
      escrever();
      conversa.querySelector('.conversa-agora').hidden = false;
      // o relógio só corre com o bloco na tela e a aba aberta
      let espera = 0;
      let naTela = false;
      const tique = () => { escrever(); espera = setTimeout(tique, 60000 - Date.now() % 60000); };
      const conferir = () => { clearTimeout(espera); if (naTela && !document.hidden) tique(); };
      if ('IntersectionObserver' in window) new IntersectionObserver((es) => { naTela = es[es.length - 1].isIntersecting; conferir(); }).observe(conversa);
      document.addEventListener('visibilitychange', conferir);
    } catch (e) { /* sem o fuso de Brasília no navegador, fica só a janela escrita */ }
  }

  // ---- Monte o seu site: estimativa na hora e a mensagem pronta ----
  // Os preços são os mesmos dos cartões e das dúvidas da página (a partir de; o painel é extra só no site de
  // apresentação). O resto entra na proposta, e a estimativa diz isso em vez de inventar valor.
  const monte = document.querySelector('.monte');
  if (monte) {
    const enviar = document.querySelector('.monte-enviar');
    const whats = document.querySelector('.monte-whats');
    const resumo = monte.querySelector('.monte-resumo');
    const numeros = monte.querySelector('.monte-numeros');
    const total = monte.querySelector('[data-total]');
    const prazo = monte.querySelector('dd[data-prazo]');
    const mensal = monte.querySelector('[data-mensal]');
    const raiz = document.documentElement;
    const dinheiro = new Intl.NumberFormat(raiz.lang, { style: 'currency', currency: raiz.dataset.moeda || 'BRL', maximumFractionDigits: 0 });
    const reais = (v) => dinheiro.format(v);
    let mostrado = 0;
    let quadro = 0;
    const contar = (alvo) => {
      cancelAnimationFrame(quadro);
      if (calmo || !mostrado) { mostrado = alvo; total.textContent = reais(alvo); return; }
      const de = mostrado, inicio = performance.now(), dur = 240;
      const passo = (t) => {
        const k = Math.min(1, (t - inicio) / dur);
        mostrado = Math.round((de + (alvo - de) * (1 - Math.pow(1 - k, 3))) / 10) * 10;
        total.textContent = reais(k === 1 ? alvo : mostrado);
        if (k < 1) quadro = requestAnimationFrame(passo); else mostrado = alvo;
      };
      quadro = requestAnimationFrame(passo);
    };
    const atualizar = () => {
      const tipo = monte.querySelector('input[name="tipo"]:checked');
      const plano = monte.querySelector('input[name="plano"]:checked');
      const anual = monte.querySelector('input[name="anual"]').checked;
      const itens = $$('input[name="item[]"]:checked', monte);
      const linhas = [];
      let valor = 0;
      let extra = '';
      if (tipo && tipo.dataset.preco) {
        valor = Number(tipo.dataset.preco);
        itens.forEach((i) => { if (tipo.value === 'apresentacao' && i.dataset.precoApresentacao) valor += Number(i.dataset.precoApresentacao); });
        const semPreco = itens.filter((i) => !(tipo.value === 'apresentacao' && i.dataset.precoApresentacao) && !(tipo.value !== 'apresentacao' && i.dataset.precoApresentacao));
        if (semPreco.length) extra = t('extra', { itens: semPreco.length === 1 ? t('um_item') : t('n_itens', { n: semPreco.length }) });
        const vez = plano ? Number(plano.value) : 0;
        numeros.hidden = false;
        contar(valor);
        prazo.textContent = tipo.dataset.prazo;
        mensal.textContent = anual ? t('por_ano', { valor: reais(vez * 10) }) : t('por_mes', { valor: reais(vez) });
        resumo.textContent = t('estimativa', { valor: reais(valor), extra });
      } else {
        numeros.hidden = true;
        resumo.textContent = tipo ? t('sem_tipo') : t('escolha');
      }
      if (tipo) linhas.push(t('linha_tipo', { nome: tipo.dataset.nome }));
      if (itens.length) linhas.push(t('linha_itens') + '\n' + itens.map((i) => '- ' + i.value).join('\n'));
      if (plano) linhas.push(t('linha_depois', { nome: plano.dataset.nome, anual: anual ? t('anual') : '' }));
      if (valor) linhas.push(t('linha_estimativa', { valor: reais(valor), extra }));
      const inicio = t('ola') + (linhas.length ? '\n\n' + linhas.join('\n') : '');
      const corpo = inicio + '\n\n' + t('sobre');
      if (enviar) enviar.href = 'mailto:contato@linupedia.com.br?subject=' + encodeURIComponent(t('assunto')) + '&body=' + encodeURIComponent(corpo);
      if (whats) whats.href = whats.href.split('?')[0] + '?text=' + encodeURIComponent(inicio);
      resumo.classList.remove('pulso');
      void resumo.offsetWidth; // reinicia a animação
      if (tipo) resumo.classList.add('pulso');
    };
    monte.addEventListener('change', atualizar);
    atualizar();

    // Os preços de “O que fazemos” levam até aqui com a opção já marcada (tipo=… ou plano=…)
    $$('[data-escolher]').forEach((link) => {
      link.addEventListener('click', () => {
        const [nome, valor] = link.dataset.escolher.split('=');
        const opcao = monte.querySelector(`input[name="${nome}"][value="${valor}"]`);
        if (!opcao) return;
        opcao.checked = true;
        opcao.dispatchEvent(new Event('change', { bubbles: true }));
        // o link já rola até #contato; o foco vai para a opção marcada, para quem usa teclado ou leitor de tela
        setTimeout(() => opcao.focus({ preventScroll: true }), calmo ? 0 : 400);
      });
    });
  }
})();
