/* Carrega no <head>, sem defer: marca que tem JavaScript (a tela de boot e as entradas ao rolar só existem
   com ele) e se a página está embutida no simulador do Linu Sites, antes de pintar.
   E escolhe o modo: de dia (6h–18h no relógio de quem visita) a Padaria Aurora, de noite o Café. O botão de sol e
   lua guarda a escolha no navegador; ?modo=dia ou ?modo=noite no endereço vale só para aquela visita. */
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
})();
