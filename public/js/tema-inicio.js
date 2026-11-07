/* Tema escolhido pela pessoa (a luminária do topo); sem escolha, segue o sistema. Carrega no <head>, sem defer, para
   valer antes de pintar a página. */
try { var t = localStorage.getItem("tema"); if (t === "dark" || t === "light") document.documentElement.dataset.theme = t; } catch (e) {}
