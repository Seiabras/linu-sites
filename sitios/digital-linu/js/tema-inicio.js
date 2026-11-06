/* Tema escolhido pela pessoa (botão do sol e da lua); sem escolha, segue o sistema. Carrega no <head>, sem defer,
   para valer antes de pintar a página. A chave é a mesma do Linu Sites ("tema"), mas cada endereço guarda a sua. */
try { var t = localStorage.getItem("tema"); if (t === "dark" || t === "light") document.documentElement.dataset.theme = t; } catch (e) {}
document.documentElement.classList.add("js");
