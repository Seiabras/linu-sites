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
    var hora = new Date().getHours();
    modo = hora >= 6 && hora < 18 ? 'dia' : 'noite';
  }
  raiz.setAttribute('data-modo', modo);

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

  // O relógio de turno (4/11/2026): é o mesmo lugar, padaria das 6h às 18h e café das 18h às 6h. Diz o que está
  // aberto agora, pelo relógio de quem visita, e quanto falta para a troca. Só aparece no idioma que já tem o texto.
  document.addEventListener('DOMContentLoaded', function () {
    var el = document.getElementById('turno'), bloco = document.getElementById('textos-cafe'), T = {};
    try { T = JSON.parse(bloco.textContent); } catch (e) {}
    if (!el || !T.turno_cafe || !T.turno_padaria) return;
    function dois(n) { return (n < 10 ? '0' : '') + n; }
    function atualizar() {
      var d = new Date(), h = d.getHours(), m = d.getMinutes(), padaria = h >= 6 && h < 18;
      var falta = ((padaria ? 18 : 6) * 60 - (h * 60 + m) + 1440) % 1440;
      var f = falta >= 60 ? Math.floor(falta / 60) + 'h' + dois(falta % 60) : falta + ' min';
      el.textContent = (padaria ? T.turno_padaria : T.turno_cafe).replace('{h}', h + 'h' + dois(m)).replace('{falta}', f);
      el.hidden = false;
    }
    var relogio = 0;
    function ligar() { clearInterval(relogio); relogio = 0; if (!document.hidden) { atualizar(); relogio = setInterval(atualizar, 30000); } }
    ligar();
    document.addEventListener('visibilitychange', ligar);
  });
})();
