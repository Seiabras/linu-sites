/* Menu do celular: o botão abre e fecha o painel com os links; fecha ao escolher um link, ao tocar fora e com Esc. */
(function () {
  "use strict";

  var menu = document.querySelector(".menu");
  var botao = document.querySelector(".menu-abrir");
  if (!menu || !botao) return;

  function abrir(sim) {
    menu.classList.toggle("aberto", sim);
    botao.setAttribute("aria-expanded", sim ? "true" : "false");
    botao.setAttribute("aria-label", sim ? "Fechar o menu" : "Abrir o menu");
  }

  botao.addEventListener("click", function () {
    abrir(!menu.classList.contains("aberto"));
  });
  menu.addEventListener("click", function (e) {
    if (e.target.closest(".menu-links a")) abrir(false);
  });
  document.addEventListener("click", function (e) {
    if (menu.classList.contains("aberto") && !menu.contains(e.target)) abrir(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && menu.classList.contains("aberto")) {
      abrir(false);
      botao.focus();
    }
  });
})();
