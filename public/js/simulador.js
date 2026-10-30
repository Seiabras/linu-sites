// Simulador do Café Aurora (seção "Exemplo"): cada parte ligada ou desligada vai para o site embutido, por
// postMessage e só com o endereço do Café (cafe.linupedia.com.br), e o total muda na hora. Os preços ficam nos data-preco do index.html.
// O site embutido só anima quando aparece na tela: o observer avisa quando ele entra e sai.
(() => {
  'use strict';
  const sim = document.querySelector('.simulador');
  if (!sim) return;
  const quadro = sim.querySelector('iframe');
  // O Café Aurora mora no próprio subdomínio: as mensagens vão e vêm só desse endereço
  const origemCafe = new URL(quadro.src).origin;
  const total = sim.querySelector('[data-simulador-total]');
  const base = Number(sim.dataset.base);
  const calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // a moeda e o jeito de escrever o número são os do idioma da página (<html lang data-moeda>)
  const raiz = document.documentElement;
  const reais = (v) => new Intl.NumberFormat(raiz.lang, { style: 'currency', currency: raiz.dataset.moeda || 'BRL', maximumFractionDigits: 0 }).format(v);
  const ligados = () => [...sim.querySelectorAll('input[name="modulo[]"]:checked')];
  let visivel = !('IntersectionObserver' in window);
  let mostrado = 0;
  let pedido = 0;

  const mandar = () => {
    if (!quadro.contentWindow) return;
    quadro.contentWindow.postMessage({ cafeAurora: { modulos: ligados().map((i) => i.value), visivel } }, origemCafe);
  };

  // O total corre até o valor novo em 240 ms (como no "Monte o seu site")
  const contar = (alvo) => {
    cancelAnimationFrame(pedido);
    if (calmo || !mostrado) { mostrado = alvo; total.textContent = reais(alvo); return; }
    const de = mostrado, inicio = performance.now(), dur = 240;
    const passo = (t) => {
      const k = Math.min(1, (t - inicio) / dur);
      mostrado = k === 1 ? alvo : Math.round((de + (alvo - de) * (1 - Math.pow(1 - k, 3))) / 10) * 10;
      total.textContent = reais(mostrado);
      if (k < 1) pedido = requestAnimationFrame(passo);
    };
    pedido = requestAnimationFrame(passo);
  };

  const atualizar = () => {
    contar(base + ligados().reduce((soma, i) => soma + Number(i.dataset.preco), 0));
    mandar();
  };

  sim.addEventListener('change', atualizar);
  // O site embutido avisa quando carregou; aí recebe o que está ligado
  window.addEventListener('message', (e) => {
    if (e.origin === origemCafe && e.source === quadro.contentWindow && e.data && e.data.cafeAurora === 'pronto') mandar();
  });
  if (!visivel) {
    new IntersectionObserver((es) => { visivel = es[es.length - 1].isIntersecting; mandar(); }).observe(quadro);
  }
  atualizar();
})();
