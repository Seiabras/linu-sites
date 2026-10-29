// Movimento e interação da página: seções que entram ao rolar, menu que marca a seção atual
// e o "monte o seu site", que mostra a estimativa na hora e já escreve a mensagem do WhatsApp e o e-mail.
// Sem JavaScript, ou com "menos movimento" no aparelho, tudo continua lá: só não anima.
(() => {
  'use strict';
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
    const reais = (v) => 'R$ ' + v.toLocaleString('pt-BR');
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
        if (semPreco.length) extra = ` + ${semPreco.length === 1 ? 'um item' : semPreco.length + ' itens'} na proposta`;
        const vez = plano ? Number(plano.value) : 0;
        numeros.hidden = false;
        contar(valor);
        prazo.textContent = tipo.dataset.prazo;
        mensal.textContent = anual ? reais(vez * 10) + ' por ano' : reais(vez) + ' por mês';
        resumo.textContent = 'Estimativa: a partir de ' + reais(valor) + extra;
      } else {
        numeros.hidden = true;
        resumo.textContent = tipo ? 'Sem problema: a conversa ajuda a escolher o tipo.' : 'Escolha o tipo para ver uma estimativa';
      }
      if (tipo) linhas.push('Tipo: ' + tipo.dataset.nome);
      if (itens.length) linhas.push('Precisa ter:\n' + itens.map((i) => '- ' + i.value).join('\n'));
      if (plano) linhas.push('Depois de pronto: ' + plano.dataset.nome + (anual ? ', pagando o ano' : ''));
      if (valor) linhas.push('Estimativa do site: a partir de ' + reais(valor) + extra);
      const corpo = 'Olá! Quero um site.' + (linhas.length ? '\n\n' + linhas.join('\n') : '') + '\n\nSobre o meu negócio: ';
      if (enviar) enviar.href = 'mailto:contato@linupedia.com.br?subject=' + encodeURIComponent('Quero um site') + '&body=' + encodeURIComponent(corpo);
      if (whats) whats.href = whats.href.split('?')[0] + '?text=' + encodeURIComponent(corpo.replace(/\n\nSobre o meu negócio: $/, ''));
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
