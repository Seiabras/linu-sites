/* Carrega no <head>, sem defer: marca que tem JavaScript (a tela de boot e as entradas ao rolar só existem
   com ele) e se a página está embutida no simulador do Linu Sites, antes de pintar.
   E escolhe o modo: de dia (6h–18h no relógio de quem visita) a Padaria Aurora, de noite o Café. O botão de sol e
   lua guarda a escolha no navegador; ?modo=dia ou ?modo=noite no endereço vale só para aquela visita.
   A abertura (1/11/2026, a exceção “abertura de identidade” das diretrizes): só na primeira página da sessão
   (sessionStorage; nas outras o <html> ganha .ja-abriu e ela nem aparece) e some com um toque, um clique ou
   Esc, Enter ou espaço. Quem conta o tempo (0,9 s desde 4/11/2026) é o script de cada versão. */
(function () {
  var raiz = document.documentElement, modo = null;
  raiz.classList.add('js');
  if (window.top !== window) raiz.classList.add('embutido');
  try { modo = new URLSearchParams(location.search).get('modo'); } catch (e) {}
  if (modo !== 'dia' && modo !== 'noite') {
    try { modo = localStorage.getItem('aurora-modo'); } catch (e) {}
  }
  if (modo !== 'dia' && modo !== 'noite') {
    var horaAgora = new Date().getHours();
    modo = horaAgora >= 6 && horaAgora < 18 ? 'dia' : 'noite';
  }
  raiz.setAttribute('data-modo', modo);

  // As escolhas do painel de acessibilidade (recursos.js, 18/11/2026) valem antes de pintar, sem piscar
  try {
    var a = JSON.parse(localStorage.getItem('aurora-acessibilidade'));
    if (a) {
      raiz.setAttribute('data-texto', String(a.texto || 0));
      ['contraste', 'links', 'fonte', 'espaco', 'parado'].forEach(function (k) { if (a[k]) raiz.classList.add('a11y-' + k); });
    }
  } catch (e) {}

  var jaAbriu = false;
  try {
    jaAbriu = sessionStorage.getItem('aurora-abertura') === '1';
    sessionStorage.setItem('aurora-abertura', '1');
  } catch (e) {}
  if (jaAbriu) raiz.classList.add('ja-abriu');
  else document.addEventListener('DOMContentLoaded', function () {
    var boot = document.getElementById('boot');
    if (!boot) return;
    function pular() { boot.classList.add('done'); document.removeEventListener('keydown', tecla); }
    function tecla(e) {
      if (boot.classList.contains('done')) document.removeEventListener('keydown', tecla);
      else if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pular(); }
    }
    boot.addEventListener('click', pular);
    document.addEventListener('keydown', tecla);
  });

  // A hora no jeito de cada língua (26/11/2026): fmt_hora ("{h}h{mm}", "{hh}:{mm}", "{h12} {ap}"…), fmt_hora_cheia
  // (a hora redonda), fmt_dur (quanto falta) e fmt_ap (AM e PM, só onde se usa) vêm do #textos-cafe.
  function hora(tpl, h, m, T) {
    var d = function (n) { return (n < 10 ? '0' : '') + n; }, ap = T.fmt_ap || ['', ''];
    return String(tpl || '{h}h{mm}').replace('{hh}', d(h)).replace('{h12}', h % 12 || 12).replace('{h}', h)
      .replace('{mm}', d(m)).replace('{m}', m).replace('{ap}', h < 12 ? ap[0] : ap[1]);
  }

  // O relógio de turno (4/11/2026): é o mesmo lugar, padaria das 6h às 18h e café das 18h às 6h. Diz o que está
  // aberto agora, pelo relógio de quem visita, e quanto falta para a troca. Só aparece no idioma que já tem o texto.
  document.addEventListener('DOMContentLoaded', function () {
    var el = document.getElementById('turno'), bloco = document.getElementById('textos-cafe'), T = {};
    try { T = JSON.parse(bloco.textContent); } catch (e) {}
    if (!el || !T.turno_cafe || !T.turno_padaria) return;
    function atualizar() {
      var d = new Date(), h = d.getHours(), m = d.getMinutes(), padaria = h >= 6 && h < 18;
      var falta = ((padaria ? 18 : 6) * 60 - (h * 60 + m) + 1440) % 1440;
      var f = falta >= 60 ? hora(T.fmt_dur, Math.floor(falta / 60), falta % 60, T) : (T.d_min || '{n} min').replace('{n}', falta);
      el.textContent = (padaria ? T.turno_padaria : T.turno_cafe).replace('{h}', hora(T.fmt_hora, h, m, T)).replace('{falta}', f);
      el.hidden = false;
    }
    var relogio = 0;
    function ligar() { clearInterval(relogio); relogio = 0; if (!document.hidden) { atualizar(); relogio = setInterval(atualizar, 30000); } }
    ligar();
    document.addEventListener('visibilitychange', ligar);
  });

  // A luz da padaria (26/11/2026). De noite, o “Sintonizar dimensão” gira o matiz de tudo (o script de cada versão
  // escreve o --desvio). De dia, o mesmo controle vira “Sintonizar a luz”: a hora do sol no turno da padaria, de -70
  // (6h, amanhecer rosado) a 0 (meio-dia, luz neutra) e 70 (18h, fim de tarde dourado). Aqui saem as --luz-* que o
  // CSS do modo dia usa (estilo.css bloco 17 e padaria.css), e o --desvio fica com o valor da noite. Cada modo guarda
  // o seu valor; de dia, o controle começa na hora de agora. Serve às cinco versões, porque todas carregam este arquivo.
  document.addEventListener('DOMContentLoaded', function () {
    var hue = document.getElementById('hue'), val = document.getElementById('hueVal'), dim = document.getElementById('dim');
    if (!hue) return;
    var T = {}, L = {};
    try { T = JSON.parse(document.getElementById('textos-cafe').textContent); L = T.luz || {}; } catch (e) {}
    // amanhecer, meio-dia e fim de tarde; entre eles, a mistura
    var PONTOS = [
      { h: -14, s: -12, l: 4, tinta: [249, 230, 229], p: 0.7, sepia: 0.06, foto: -12, sat: 0.9, bri: 1.04 },
      { h: 0, s: 0, l: 0, tinta: [251, 243, 228], p: 0, sepia: 0, foto: 0, sat: 1, bri: 1 },
      { h: 6, s: 12, l: -8, tinta: [245, 216, 172], p: 0.75, sepia: 0.32, foto: -6, sat: 1.25, bri: 0.97 }
    ];
    var FUNDO = [251, 243, 228], FUNDO2 = [244, 230, 204];
    var PROPS = ['--luz-h', '--luz-s', '--luz-l', '--luz-bg', '--luz-bg2', '--luz-sepia', '--luz-foto', '--luz-sat', '--luz-bri'];
    var ariaDim = dim && dim.getAttribute('aria-label'), ariaHue = hue.getAttribute('aria-label');
    // o título e o rótulo (data-luz="titulo" e "rotulo" no modelo): de dia, o texto do js.luz; de noite, o de sempre
    var trocas = Array.prototype.map.call(document.querySelectorAll('[data-luz]'), function (n) {
      return { n: n, noite: n.textContent, dia: L[n.getAttribute('data-luz')] };
    });
    function textos(dia) { trocas.forEach(function (t) { if (t.dia) t.n.textContent = dia ? t.dia : t.noite; }); }
    function modo() { return raiz.getAttribute('data-modo') === 'dia' ? 'dia' : 'noite'; }
    function agora() {
      var d = new Date(), h = d.getHours() + d.getMinutes() / 60;
      return h >= 6 && h <= 18 ? Math.round((h - 12) / 6 * 70) : 0;
    }
    var valores = { noite: Number(hue.value) || 0, dia: agora() }, atual = modo();
    function mistura(a, b, k) { return a + (b - a) * k; }
    function rgb(base, tinta, p) {
      return 'rgb(' + base.map(function (c, i) { return Math.round(mistura(c, tinta[i], p)); }).join(' ') + ')';
    }
    function horaDaLuz(v) {
      var h = 12 + v / 70 * 6, inteira = Math.floor(h), min = Math.round((h - inteira) * 4) * 15;
      if (min === 60) { inteira++; min = 0; }
      return { h: h, texto: min ? hora(T.fmt_hora, inteira, min, T) : hora(T.fmt_hora_cheia || T.fmt_hora, inteira, 0, T) };
    }
    function momento(h) {
      var m = L.momentos || [];
      for (var i = 0; i < m.length; i++) if (h < m[i][0]) return m[i][1];
      return m.length ? m[m.length - 1][1] : '';
    }
    function aplicar() {
      var v = Number(hue.value) || 0;
      valores[modo()] = v;
      if (modo() !== 'dia') {
        PROPS.forEach(function (p) { raiz.style.removeProperty(p); });
        if (ariaDim) dim.setAttribute('aria-label', ariaDim);
        if (ariaHue) hue.setAttribute('aria-label', ariaHue);
        hue.removeAttribute('aria-valuetext');
        textos(false);
        return;
      }
      textos(true);
      var t = v / 70, a = t < 0 ? PONTOS[0] : PONTOS[2], k = Math.abs(t), z = PONTOS[1];
      function q(nome) { return mistura(z[nome], a[nome], k); }
      raiz.style.setProperty('--desvio', valores.noite); // a dimensão da noite fica como estava
      raiz.style.setProperty('--luz-h', q('h').toFixed(1));
      raiz.style.setProperty('--luz-s', q('s').toFixed(1) + '%');
      raiz.style.setProperty('--luz-l', q('l').toFixed(1) + '%');
      raiz.style.setProperty('--luz-bg', rgb(FUNDO, a.tinta, a.p * k));
      raiz.style.setProperty('--luz-bg2', rgb(FUNDO2, a.tinta, a.p * k * 0.8));
      raiz.style.setProperty('--luz-sepia', q('sepia').toFixed(3));
      raiz.style.setProperty('--luz-foto', q('foto').toFixed(1) + 'deg');
      raiz.style.setProperty('--luz-sat', q('sat').toFixed(3));
      raiz.style.setProperty('--luz-bri', q('bri').toFixed(3));
      var hr = horaDaLuz(v), nome = momento(hr.h), texto = nome ? hr.texto + ' · ' + nome : hr.texto;
      if (val) val.textContent = texto;
      hue.setAttribute('aria-valuetext', texto);
      if (L.aria) hue.setAttribute('aria-label', L.aria);
      if (L.aria_dim && dim) dim.setAttribute('aria-label', L.aria_dim);
      raiz.dispatchEvent(new CustomEvent('luz', { detail: q('h') }));
    }
    // o script de cada versão também ouve o "input" e escreve o --desvio: este ouvinte vem depois e corrige de dia
    hue.addEventListener('input', aplicar);
    function trocouModo() {
      var m = modo();
      if (m === atual) return;
      atual = m;
      hue.value = valores[m];
      hue.dispatchEvent(new Event('input', { bubbles: true }));
    }
    new MutationObserver(trocouModo).observe(raiz, { attributes: true, attributeFilter: ['data-modo'] });
    if (modo() === 'dia') { hue.value = valores.dia; hue.dispatchEvent(new Event('input', { bubbles: true })); }
  });
})();
