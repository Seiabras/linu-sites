/* Carrega no <head>, sem defer: aplica o tema escolhido no botão antes de desenhar a página, para não piscar.
   Sem escolha, vale o do sistema (o CSS cuida disso). */
try { var t = localStorage.getItem('tema'); if (t === 'dark' || t === 'light') document.documentElement.dataset.theme = t; } catch (e) {}
