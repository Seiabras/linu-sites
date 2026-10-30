/* Tema escolhido pela pessoa (botão da luz); sem escolha, segue o sistema. Carrega no <head>, sem defer,
   para valer antes de pintar a página.
   E a hora de quem visita: das 18h às 6h no relógio dela, o quarto do Linu aparece à noite, com o lampião
   aceso (data-hora="noite"); quem abre de Tóquio às 22h vê a noite de lá. */
try { var t = localStorage.getItem("tema"); if (t === "dark" || t === "light") document.documentElement.dataset.theme = t; } catch (e) {}
(function () { var h = new Date().getHours(); document.documentElement.dataset.hora = h >= 6 && h < 18 ? "dia" : "noite"; })();
