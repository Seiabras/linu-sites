/* Carrega no <head>, sem defer: marca que tem JavaScript (a tela de boot e as entradas ao rolar só existem
   com ele) e se a página está embutida no simulador do Linu Sites, antes de pintar.
   E escolhe o modo: de dia (6h–18h no relógio de quem visita) a Padaria Aurora, de noite o Café. O botão de sol e
   lua guarda a escolha no navegador; ?modo=dia ou ?modo=noite no endereço vale só para aquela visita.
   A abertura (1/11/2026, a exceção “abertura de identidade” das diretrizes): só na primeira página da sessão
   (sessionStorage; nas outras o <html> ganha .ja-abriu e ela nem aparece) e some com um toque, um clique ou
   Esc, Enter ou espaço. Quem conta os 3 segundos é o script de cada versão. */
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
})();
