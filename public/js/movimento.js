// Movimento e interação da página: seções que entram ao rolar, menu que marca a seção atual
// e o "monte o seu pedido", que já escreve o e-mail com o que a pessoa escolheu.
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
    $$('.secao h2, .secao-sub, .cartao, .projeto, .passos li, .monte, .contato-linu').forEach((el) => {
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

  // ---- Monte o seu pedido: as escolhas viram o e-mail ----
  const monte = document.querySelector('.monte');
  if (monte) {
    const enviar = document.querySelector('.monte-enviar');
    const resumo = monte.querySelector('.monte-resumo');
    const atualizar = () => {
      const marcados = $$('input:checked', monte).map((i) => i.value);
      const corpo = marcados.length
        ? 'Olá! Quero um site com:\n' + marcados.map((m) => '- ' + m).join('\n') + '\n\nSobre o meu negócio: '
        : 'Olá! Quero um site.\n\nSobre o meu negócio: ';
      enviar.href = 'mailto:contato@linupedia.com.br?subject=' + encodeURIComponent('Quero um site') + '&body=' + encodeURIComponent(corpo);
      resumo.textContent = marcados.length ? `${marcados.length} ${marcados.length === 1 ? 'item escolhido' : 'itens escolhidos'}` : 'Escolha o que o site precisa ter';
      resumo.classList.remove('pulso');
      void resumo.offsetWidth; // reinicia a animação
      if (marcados.length) resumo.classList.add('pulso');
    };
    monte.addEventListener('change', atualizar);
    atualizar();
  }
})();
