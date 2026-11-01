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

  // O Café avisa se está de noite (Café Aurora) ou de dia (Padaria Aurora); os textos que falam da bebida viram pão.
  // O texto de dia de cada um fica no data-dia dele (nas 13 línguas desde 1/11/2026); sem ele, nada muda.
  const alvos = [...document.querySelectorAll('#exemplo [data-modo-texto]')];
  const DIA = alvos.some((el) => el.dataset.dia);
  let modoCafe = 'noite';
  const trocarModo = (m) => {
    if (!DIA || (m !== 'dia' && m !== 'noite') || m === modoCafe) return;
    modoCafe = m;
    sim.dataset.modo = m;
    alvos.forEach((el) => {
      const eIframe = el.tagName === 'IFRAME';
      if (!el.dataset.noite) el.dataset.noite = eIframe ? el.title : el.textContent;
      const v = m === 'dia' && el.dataset.dia ? el.dataset.dia : el.dataset.noite;
      if (eIframe) { el.title = v; return; }
      el.textContent = v;
      if (!calmo) el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, easing: 'ease-out' });
    });
  };

  const atualizar = () => {
    contar(base + ligados().reduce((soma, i) => soma + Number(i.dataset.preco), 0));
    mandar();
  };

  sim.addEventListener('change', atualizar);
  // O site embutido avisa quando carregou; aí recebe o que está ligado
  window.addEventListener('message', (e) => {
    if (e.origin !== origemCafe || e.source !== quadro.contentWindow || !e.data || !e.data.cafeAurora) return;
    if (e.data.cafeAurora === 'pronto') { trocarModo(e.data.modo); mandar(); return; }
    if (e.data.cafeAurora.modo) trocarModo(e.data.cafeAurora.modo);
  });
  if (!visivel) {
    new IntersectionObserver((es) => { visivel = es[es.length - 1].isIntersecting; mandar(); }).observe(quadro);
  }
  atualizar();
})();
