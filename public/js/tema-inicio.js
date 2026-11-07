/* Tema escolhido pela pessoa (a luminária do topo); sem escolha, segue o sistema. Carrega no <head>, sem defer, para
   valer antes de pintar a página. */
try { var t = localStorage.getItem("tema"); if (t === "dark" || t === "light") document.documentElement.dataset.theme = t; } catch (e) {}
/* A hora de quem visita: das 18h às 6h no relógio dela, a obra pronta (a cabana) aparece à noite, com o lampião aceso */
(function () { var h = new Date().getHours(); document.documentElement.dataset.hora = h >= 6 && h < 18 ? "dia" : "noite"; })();
