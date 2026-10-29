/* Carrega no <head>, sem defer: marca que tem JavaScript (a tela de boot e as entradas ao rolar só existem
   com ele) e se a página está embutida no simulador do Linu Sites, antes de pintar. */
document.documentElement.classList.add('js');
if (window.top !== window) document.documentElement.classList.add('embutido');
